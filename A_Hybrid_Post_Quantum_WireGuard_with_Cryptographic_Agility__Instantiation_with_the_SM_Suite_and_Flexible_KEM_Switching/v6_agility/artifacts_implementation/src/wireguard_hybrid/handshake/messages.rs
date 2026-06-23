#[cfg(test)]
use hex;

#[cfg(test)]
use std::fmt;

use std::mem;

use byteorder::{ByteOrder, LittleEndian};
use zerocopy::byteorder::U32;
use zerocopy::{AsBytes, ByteSlice, FromBytes, LayoutVerified};

use crate::wireguard_hybrid::handshake::agility::{
    self, EphemeralKemSuite, MAX_EPHEMERAL_KEM_CIPHERTEXT, MAX_EPHEMERAL_KEM_PUB_KEY,
};
use crate::wireguard_hybrid::handshake::crypto_params::{
    SIZE_HASH, SIZE_SM2_POINT, SIZE_STATIC_KEM_CIPHERTEXT, SIZE_XNONCE,
};
use super::types::*;

const SIZE_MAC: usize = 16;
const SIZE_TAG: usize = 16; // poly1305 / gcm tag

const SIZE_COOKIE: usize = 16; //

const SIZE_TIMESTAMP: usize = 16;

/// Full 32-byte mac footer (mac1 ‖ mac2) appended to every handshake message.
pub const SIZE_MACS: usize = 2 * SIZE_MAC;

/// On-wire size of the one-byte ephemeral-KEM suite selector (v6 agility).
pub const SIZE_SUITE: usize = 1;

pub const TYPE_INITIATION: u32 = 1;
pub const TYPE_RESPONSE: u32 = 2;
pub const TYPE_COOKIE_REPLY: u32 = 3;

const fn max(a: usize, b: usize) -> usize {
    let m: usize = (a > b) as usize;
    m * a + (1 - m) * b
}

// ---------------------------------------------------------------------------
// Worst-case message sizes.
//
// Unlike v1–v5 the post-quantum fields are no longer a single fixed length: the
// ephemeral KEM is chosen at run time, so the *upper bound* is taken over every
// registered suite (the agility::MAX_* constants). The actual datagram is
// compact — only the bytes the active suite needs are serialized (see
// `NoiseInitiation::serialize`).
// ---------------------------------------------------------------------------

const INIT_FIXED: usize = 4    // f_type
    + 4                        // f_sender
    + SIZE_SUITE               // f_suite
    + SIZE_SM2_POINT           // f_ephemeral (SM2, 33)
    + SIZE_STATIC_KEM_CIPHERTEXT // f_static_ct_pq (McEliece, fixed)
    + (SIZE_HASH + SIZE_TAG)   // f_static
    + (SIZE_TIMESTAMP + SIZE_TAG); // f_timestamp

const RESP_FIXED: usize = 4    // f_type
    + 4                        // f_sender
    + 4                        // f_receiver
    + SIZE_SUITE               // f_suite
    + SIZE_SM2_POINT           // f_ephemeral (SM2, 33)
    + SIZE_STATIC_KEM_CIPHERTEXT // f_static_ct_pq (McEliece, fixed)
    + SIZE_TAG;                // f_empty

/// Largest possible InitHello (largest ephemeral KEM public key + macs).
pub const MAX_INITIATION_SIZE: usize = INIT_FIXED + MAX_EPHEMERAL_KEM_PUB_KEY + SIZE_MACS;
/// Largest possible RespHello (largest ephemeral KEM ciphertext + macs).
pub const MAX_RESPONSE_SIZE: usize = RESP_FIXED + MAX_EPHEMERAL_KEM_CIPHERTEXT + SIZE_MACS;

pub const MAX_HANDSHAKE_MSG_SIZE: usize = max(
    max(MAX_RESPONSE_SIZE, MAX_INITIATION_SIZE),
    mem::size_of::<CookieReply>(),
);

/* ------------------------------------------------------------------------- */
/* Cookie reply — KEM-independent, kept as a fixed zero-copy struct.          */
/* ------------------------------------------------------------------------- */

#[repr(packed)]
#[derive(Copy, Clone, FromBytes, AsBytes)]
pub struct CookieReply {
    pub f_type: U32<LittleEndian>,
    pub f_receiver: U32<LittleEndian>,
    pub f_nonce: [u8; SIZE_XNONCE],
    pub f_cookie: [u8; SIZE_COOKIE + SIZE_TAG],
}

impl CookieReply {
    pub fn parse<B: ByteSlice>(bytes: B) -> Result<LayoutVerified<B, Self>, HandshakeError> {
        let msg: LayoutVerified<B, Self> =
            LayoutVerified::new(bytes).ok_or(HandshakeError::InvalidMessageFormat)?;
        if msg.f_type.get() != (TYPE_COOKIE_REPLY as u32) {
            return Err(HandshakeError::InvalidMessageFormat);
        }
        Ok(msg)
    }
}

impl Default for CookieReply {
    fn default() -> Self {
        Self {
            f_type: <U32<LittleEndian>>::new(TYPE_COOKIE_REPLY as u32),
            f_receiver: <U32<LittleEndian>>::ZERO,
            f_nonce: [0u8; SIZE_XNONCE],
            f_cookie: [0u8; SIZE_COOKIE + SIZE_TAG],
        }
    }
}

/* ------------------------------------------------------------------------- */
/* Mac footer — fixed 32 bytes, appended after the (variable) noise body.     */
/* ------------------------------------------------------------------------- */

#[derive(Copy, Clone)]
pub struct MacsFooter {
    pub f_mac1: [u8; SIZE_MAC],
    pub f_mac2: [u8; SIZE_MAC],
}

impl Default for MacsFooter {
    fn default() -> Self {
        Self {
            f_mac1: [0u8; SIZE_MAC],
            f_mac2: [0u8; SIZE_MAC],
        }
    }
}

impl MacsFooter {
    /// Append the 32-byte mac footer onto an already-serialized noise body.
    pub fn append_to(&self, buf: &mut Vec<u8>) {
        buf.extend_from_slice(&self.f_mac1);
        buf.extend_from_slice(&self.f_mac2);
    }
}

/// Split a complete handshake message into `(noise_body, mac_footer)`.
///
/// mac1/mac2 are always the trailing 32 bytes; everything before them is the
/// noise body that the macs cover and that `NoiseInitiation`/`NoiseResponse`
/// know how to parse.
pub fn split_macs(msg: &[u8]) -> Result<(&[u8], MacsFooter), HandshakeError> {
    if msg.len() < SIZE_MACS {
        return Err(HandshakeError::InvalidMessageFormat);
    }
    let split = msg.len() - SIZE_MACS;
    let (body, footer) = msg.split_at(split);
    let mut macs = MacsFooter::default();
    macs.f_mac1.copy_from_slice(&footer[..SIZE_MAC]);
    macs.f_mac2.copy_from_slice(&footer[SIZE_MAC..]);
    Ok((body, macs))
}

/* ------------------------------------------------------------------------- */
/* Inner noise messages — variable length, suite-aware (de)serialization.     */
/*                                                                            */
/* In memory each KEM field reserves a MAX-sized buffer so one struct type can */
/* hold any suite; only the active suite's prefix is written on the wire.      */
/* ------------------------------------------------------------------------- */

#[derive(Copy, Clone)]
pub struct NoiseInitiation {
    pub f_type: u32,
    pub f_sender: u32,
    /// Ephemeral-KEM suite selector — the v6 on-wire agility signal.
    pub f_suite: u8,
    pub f_ephemeral: [u8; SIZE_SM2_POINT],
    pub f_ephemeral_pq: [u8; MAX_EPHEMERAL_KEM_PUB_KEY],
    pub f_static_ct_pq: [u8; SIZE_STATIC_KEM_CIPHERTEXT],
    pub f_static: [u8; SIZE_HASH + SIZE_TAG],
    pub f_timestamp: [u8; SIZE_TIMESTAMP + SIZE_TAG],
}

#[derive(Copy, Clone)]
pub struct NoiseResponse {
    pub f_type: u32,
    pub f_sender: u32,
    pub f_receiver: u32,
    /// Ephemeral-KEM suite selector — echoes the initiator's choice.
    pub f_suite: u8,
    pub f_ephemeral: [u8; SIZE_SM2_POINT],
    pub f_ephemeral_ct_pq: [u8; MAX_EPHEMERAL_KEM_CIPHERTEXT],
    pub f_static_ct_pq: [u8; SIZE_STATIC_KEM_CIPHERTEXT],
    pub f_empty: [u8; SIZE_TAG],
}

impl Default for NoiseInitiation {
    fn default() -> Self {
        Self {
            f_type: TYPE_INITIATION,
            f_sender: 0,
            f_suite: agility::DEFAULT_SUITE_ID,
            f_ephemeral: [0u8; SIZE_SM2_POINT],
            f_ephemeral_pq: [0u8; MAX_EPHEMERAL_KEM_PUB_KEY],
            f_static_ct_pq: [0u8; SIZE_STATIC_KEM_CIPHERTEXT],
            f_static: [0u8; SIZE_HASH + SIZE_TAG],
            f_timestamp: [0u8; SIZE_TIMESTAMP + SIZE_TAG],
        }
    }
}

impl Default for NoiseResponse {
    fn default() -> Self {
        Self {
            f_type: TYPE_RESPONSE,
            f_sender: 0,
            f_receiver: 0,
            f_suite: agility::DEFAULT_SUITE_ID,
            f_ephemeral: [0u8; SIZE_SM2_POINT],
            f_ephemeral_ct_pq: [0u8; MAX_EPHEMERAL_KEM_CIPHERTEXT],
            f_static_ct_pq: [0u8; SIZE_STATIC_KEM_CIPHERTEXT],
            f_empty: [0u8; SIZE_TAG],
        }
    }
}

/// Resolve the suite byte to a registered suite.
fn resolve_suite(id: u8) -> Result<EphemeralKemSuite, HandshakeError> {
    agility::suite_by_id(id).ok_or(HandshakeError::InvalidMessageFormat)
}

fn eph_pub_len(suite: &EphemeralKemSuite) -> Result<usize, HandshakeError> {
    suite
        .lengths()
        .map(|l| l.public_key)
        .ok_or(HandshakeError::InvalidMessageFormat)
}

fn eph_ct_len(suite: &EphemeralKemSuite) -> Result<usize, HandshakeError> {
    suite
        .lengths()
        .map(|l| l.ciphertext)
        .ok_or(HandshakeError::InvalidMessageFormat)
}

impl NoiseInitiation {
    /// The ephemeral KEM suite advertised by this message.
    pub fn suite(&self) -> Result<EphemeralKemSuite, HandshakeError> {
        resolve_suite(self.f_suite)
    }

    /// Serialize to the compact wire form (no mac footer).
    pub fn serialize(&self) -> Result<Vec<u8>, HandshakeError> {
        let suite = self.suite()?;
        let pk_len = eph_pub_len(&suite)?;
        let mut buf = Vec::with_capacity(INIT_FIXED + pk_len);
        let mut tmp = [0u8; 4];
        LittleEndian::write_u32(&mut tmp, self.f_type);
        buf.extend_from_slice(&tmp);
        LittleEndian::write_u32(&mut tmp, self.f_sender);
        buf.extend_from_slice(&tmp);
        buf.push(self.f_suite);
        buf.extend_from_slice(&self.f_ephemeral);
        buf.extend_from_slice(&self.f_ephemeral_pq[..pk_len]);
        buf.extend_from_slice(&self.f_static_ct_pq);
        buf.extend_from_slice(&self.f_static);
        buf.extend_from_slice(&self.f_timestamp);
        Ok(buf)
    }

    /// Parse the compact noise body (mac footer already stripped).
    pub fn parse(bytes: &[u8]) -> Result<Self, HandshakeError> {
        if bytes.len() < 9 {
            return Err(HandshakeError::InvalidMessageFormat);
        }
        let f_type = LittleEndian::read_u32(&bytes[0..4]);
        if f_type != TYPE_INITIATION {
            return Err(HandshakeError::InvalidMessageFormat);
        }
        let f_sender = LittleEndian::read_u32(&bytes[4..8]);
        let f_suite = bytes[8];
        let suite = resolve_suite(f_suite)?;
        let pk_len = eph_pub_len(&suite)?;

        let expected = INIT_FIXED + pk_len;
        if bytes.len() != expected {
            return Err(HandshakeError::InvalidMessageFormat);
        }

        let mut msg = NoiseInitiation::default();
        msg.f_type = f_type;
        msg.f_sender = f_sender;
        msg.f_suite = f_suite;

        let mut o = 9;
        msg.f_ephemeral.copy_from_slice(&bytes[o..o + SIZE_SM2_POINT]);
        o += SIZE_SM2_POINT;
        msg.f_ephemeral_pq[..pk_len].copy_from_slice(&bytes[o..o + pk_len]);
        o += pk_len;
        msg.f_static_ct_pq
            .copy_from_slice(&bytes[o..o + SIZE_STATIC_KEM_CIPHERTEXT]);
        o += SIZE_STATIC_KEM_CIPHERTEXT;
        msg.f_static.copy_from_slice(&bytes[o..o + SIZE_HASH + SIZE_TAG]);
        o += SIZE_HASH + SIZE_TAG;
        msg.f_timestamp
            .copy_from_slice(&bytes[o..o + SIZE_TIMESTAMP + SIZE_TAG]);
        Ok(msg)
    }
}

impl NoiseResponse {
    /// The ephemeral KEM suite advertised by this message.
    pub fn suite(&self) -> Result<EphemeralKemSuite, HandshakeError> {
        resolve_suite(self.f_suite)
    }

    /// Serialize to the compact wire form (no mac footer).
    pub fn serialize(&self) -> Result<Vec<u8>, HandshakeError> {
        let suite = self.suite()?;
        let ct_len = eph_ct_len(&suite)?;
        let mut buf = Vec::with_capacity(RESP_FIXED + ct_len);
        let mut tmp = [0u8; 4];
        LittleEndian::write_u32(&mut tmp, self.f_type);
        buf.extend_from_slice(&tmp);
        LittleEndian::write_u32(&mut tmp, self.f_sender);
        buf.extend_from_slice(&tmp);
        LittleEndian::write_u32(&mut tmp, self.f_receiver);
        buf.extend_from_slice(&tmp);
        buf.push(self.f_suite);
        buf.extend_from_slice(&self.f_ephemeral);
        buf.extend_from_slice(&self.f_ephemeral_ct_pq[..ct_len]);
        buf.extend_from_slice(&self.f_static_ct_pq);
        buf.extend_from_slice(&self.f_empty);
        Ok(buf)
    }

    /// Parse the compact noise body (mac footer already stripped).
    pub fn parse(bytes: &[u8]) -> Result<Self, HandshakeError> {
        if bytes.len() < 13 {
            return Err(HandshakeError::InvalidMessageFormat);
        }
        let f_type = LittleEndian::read_u32(&bytes[0..4]);
        if f_type != TYPE_RESPONSE {
            return Err(HandshakeError::InvalidMessageFormat);
        }
        let f_sender = LittleEndian::read_u32(&bytes[4..8]);
        let f_receiver = LittleEndian::read_u32(&bytes[8..12]);
        let f_suite = bytes[12];
        let suite = resolve_suite(f_suite)?;
        let ct_len = eph_ct_len(&suite)?;

        let expected = RESP_FIXED + ct_len;
        if bytes.len() != expected {
            return Err(HandshakeError::InvalidMessageFormat);
        }

        let mut msg = NoiseResponse::default();
        msg.f_type = f_type;
        msg.f_sender = f_sender;
        msg.f_receiver = f_receiver;
        msg.f_suite = f_suite;

        let mut o = 13;
        msg.f_ephemeral.copy_from_slice(&bytes[o..o + SIZE_SM2_POINT]);
        o += SIZE_SM2_POINT;
        msg.f_ephemeral_ct_pq[..ct_len].copy_from_slice(&bytes[o..o + ct_len]);
        o += ct_len;
        msg.f_static_ct_pq
            .copy_from_slice(&bytes[o..o + SIZE_STATIC_KEM_CIPHERTEXT]);
        o += SIZE_STATIC_KEM_CIPHERTEXT;
        msg.f_empty.copy_from_slice(&bytes[o..o + SIZE_TAG]);
        Ok(msg)
    }
}

/* Debug formatting (for testing purposes) */

#[cfg(test)]
impl fmt::Debug for NoiseInitiation {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "NoiseInitiation {{ type = {}, sender = {}, suite = 0x{:02x}, ephemeral = {}, static = {}, timestamp = {} }}",
            self.f_type,
            self.f_sender,
            self.f_suite,
            hex::encode(&self.f_ephemeral[..]),
            hex::encode(&self.f_static[..]),
            hex::encode(&self.f_timestamp[..]),
        )
    }
}

#[cfg(test)]
impl fmt::Debug for NoiseResponse {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "NoiseResponse {{ type = {}, sender = {}, receiver = {}, suite = 0x{:02x}, ephemeral = {}, empty = {} }}",
            self.f_type,
            self.f_sender,
            self.f_receiver,
            self.f_suite,
            hex::encode(&self.f_ephemeral[..]),
            hex::encode(&self.f_empty[..]),
        )
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn cookie_reply_identity() {
        let mut msg = CookieReply::default();
        msg.f_receiver.set(554442);
        msg.f_nonce = [7u8; SIZE_XNONCE];
        msg.f_cookie = [9u8; SIZE_COOKIE + SIZE_TAG];
        let buf: Vec<u8> = msg.as_bytes().to_vec();
        let msg_p = CookieReply::parse(&buf[..]).unwrap();
        assert_eq!(msg_p.f_receiver.get(), 554442);
        assert_eq!(msg_p.f_nonce, [7u8; SIZE_XNONCE]);
    }

    // Round-trip the (variable-length) noise messages for every available suite.
    #[test]
    fn noise_init_roundtrip_all_suites() {
        for suite in agility::available_suites() {
            let pk_len = eph_pub_len(&suite).unwrap();
            let mut msg = NoiseInitiation::default();
            msg.f_sender = 0x11223344;
            msg.f_suite = suite.id;
            for (i, b) in msg.f_ephemeral.iter_mut().enumerate() {
                *b = i as u8;
            }
            for (i, b) in msg.f_ephemeral_pq[..pk_len].iter_mut().enumerate() {
                *b = (i % 251) as u8;
            }
            msg.f_static_ct_pq = [0xAB; SIZE_STATIC_KEM_CIPHERTEXT];
            msg.f_static = [0xCD; SIZE_HASH + SIZE_TAG];
            msg.f_timestamp = [0xEF; SIZE_TIMESTAMP + SIZE_TAG];

            let wire = msg.serialize().unwrap();
            assert_eq!(wire.len(), INIT_FIXED + pk_len);
            let back = NoiseInitiation::parse(&wire).unwrap();
            assert_eq!(back.f_sender, msg.f_sender);
            assert_eq!(back.f_suite, suite.id);
            assert_eq!(back.f_ephemeral, msg.f_ephemeral);
            assert_eq!(
                &back.f_ephemeral_pq[..pk_len],
                &msg.f_ephemeral_pq[..pk_len]
            );
            assert_eq!(back.f_timestamp, msg.f_timestamp);
        }
    }

    #[test]
    fn noise_resp_roundtrip_all_suites() {
        for suite in agility::available_suites() {
            let ct_len = eph_ct_len(&suite).unwrap();
            let mut msg = NoiseResponse::default();
            msg.f_sender = 1;
            msg.f_receiver = 2;
            msg.f_suite = suite.id;
            for (i, b) in msg.f_ephemeral_ct_pq[..ct_len].iter_mut().enumerate() {
                *b = (i % 253) as u8;
            }
            let wire = msg.serialize().unwrap();
            assert_eq!(wire.len(), RESP_FIXED + ct_len);
            let back = NoiseResponse::parse(&wire).unwrap();
            assert_eq!(back.f_receiver, 2);
            assert_eq!(back.f_suite, suite.id);
            assert_eq!(
                &back.f_ephemeral_ct_pq[..ct_len],
                &msg.f_ephemeral_ct_pq[..ct_len]
            );
        }
    }

    #[test]
    fn parse_rejects_unknown_suite() {
        let mut bytes = vec![0u8; 9];
        LittleEndian::write_u32(&mut bytes[0..4], TYPE_INITIATION);
        bytes[8] = 0xFE; // not registered
        assert!(NoiseInitiation::parse(&bytes).is_err());
    }
}
