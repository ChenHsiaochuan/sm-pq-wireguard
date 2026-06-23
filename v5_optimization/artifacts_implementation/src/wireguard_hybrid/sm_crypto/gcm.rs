//! SM4-GCM and SM4-CTR built on the optimized [`Sm4`] block cipher.
//!
//! This is a drop-in replacement for the `sm4-gcm` crate's
//! `sm4_gcm_aad_encrypt` / `sm4_gcm_aad_decrypt` / `Sm4Key` API, but with:
//!
//!   * the GFNI+AVX2 8-way SM4 core for the CTR keystream (vs. the crate's
//!     scalar, one-block-at-a-time software SM4), and
//!   * allocation-light, in-place buffer handling on the data-plane hot path.
//!
//! GHASH is computed with the CLMUL-accelerated RustCrypto `ghash` crate
//! (PCLMULQDQ backend, runtime-detected) — the same primitive the original
//! `sm4-gcm` crate used, so the construction is bit-compatible and the
//! BouncyCastle GCM test vectors continue to pass.
//!
//! Construction follows NIST SP 800-38D exactly (matching the replaced crate):
//!   H   = SM4_K(0^128)
//!   J0  = nonce || 0x00000001            (for the 12-byte nonce fast path)
//!   C   = P  xor  CTR_{inc32(J0)}(...)
//!   tag = GHASH_H(AAD || C || len) xor SM4_K(J0)

use ghash::universal_hash::{KeyInit, UniversalHash};
use ghash::GHash;
use subtle::ConstantTimeEq;

use super::sm4::Sm4;

pub const SIZE_TAG: usize = 16;
const BLOCK: usize = 16;

/// 16-byte SM4 key. Drop-in for `sm4_gcm::Sm4Key`; zeroized on drop.
pub struct Sm4Key(pub [u8; 16]);

impl Drop for Sm4Key {
    fn drop(&mut self) {
        // best-effort wipe of key material
        for b in self.0.iter_mut() {
            unsafe { core::ptr::write_volatile(b, 0) };
        }
        core::sync::atomic::compiler_fence(core::sync::atomic::Ordering::SeqCst);
    }
}

#[inline(always)]
fn inc32(ctr: u128) -> u128 {
    let lsb = (ctr as u32).wrapping_add(1);
    (ctr & !0xffff_ffffu128) | lsb as u128
}

/// Derive the GCM pre-counter block J0.
fn derive_j0(h: &[u8; 16], nonce: &[u8]) -> u128 {
    if nonce.len() == 12 {
        let mut j = [0u8; 16];
        j[..12].copy_from_slice(nonce);
        j[15] = 1;
        return u128::from_be_bytes(j);
    }
    // General case: J0 = GHASH_H(IV || 0^(s+64) || [len(IV)]_64)
    let mut gh = GHash::new(h.into());
    gh.update_padded(nonce);
    let mut len_block = [0u8; 16];
    len_block[8..].copy_from_slice(&((nonce.len() as u64) * 8).to_be_bytes());
    gh.update_padded(&len_block);
    let tag = gh.finalize();
    u128::from_be_bytes(tag.into())
}

#[inline]
fn len_block(aad_len: usize, msg_len: usize) -> [u8; 16] {
    let mut b = [0u8; 16];
    b[0..8].copy_from_slice(&((aad_len as u64) * 8).to_be_bytes());
    b[8..16].copy_from_slice(&((msg_len as u64) * 8).to_be_bytes());
    b
}

/// In-place GCM CTR: encrypt `buf` using counter blocks starting at
/// `inc32(j0)` (i.e. the first data block uses J0 + 1), 8 blocks at a time.
fn ctr_xor_gcm(cipher: &Sm4, j0: u128, buf: &mut [u8]) {
    let mut ctr = j0;
    let mut off = 0usize;
    let full = buf.len() / BLOCK;

    let mut done = 0usize;
    while done < full {
        let g = core::cmp::min(8, full - done);
        let mut ks = [[0u8; 16]; 8];
        for slot in ks.iter_mut().take(g) {
            ctr = inc32(ctr);
            *slot = ctr.to_be_bytes();
        }
        cipher.encrypt8(&mut ks);
        for k in 0..g {
            let chunk = &mut buf[off + k * BLOCK..off + (k + 1) * BLOCK];
            for (c, s) in chunk.iter_mut().zip(ks[k].iter()) {
                *c ^= *s;
            }
        }
        off += g * BLOCK;
        done += g;
    }

    // trailing partial block
    let rem = buf.len() - off;
    if rem > 0 {
        ctr = inc32(ctr);
        let mut ks = ctr.to_be_bytes();
        cipher.encrypt_block(&mut ks);
        for (c, s) in buf[off..].iter_mut().zip(ks.iter()) {
            *c ^= *s;
        }
    }
}

fn ghash_aad_ct_len(h: &[u8; 16], aad: &[u8], ct: &[u8]) -> [u8; 16] {
    let mut gh = GHash::new(h.into());
    gh.update_padded(aad);
    gh.update_padded(ct);
    gh.update_padded(&len_block(aad.len(), ct.len()));
    gh.finalize().into()
}

/// SM4-GCM authenticated encryption, fully in place — the data-plane hot path.
///
/// `buf` is laid out as `plaintext || 16 bytes of tag scratch`: on return the
/// plaintext region holds the ciphertext and the trailing 16 bytes hold the
/// tag. No heap allocation, no copy-back (cf. the allocating `..._aad_encrypt`).
pub fn sm4_gcm_encrypt_inplace(key: &Sm4Key, nonce: &[u8], aad: &[u8], buf: &mut [u8]) {
    debug_assert!(buf.len() >= SIZE_TAG);
    let n = buf.len() - SIZE_TAG;
    let cipher = Sm4::new(&key.0);
    let h = cipher.encrypt_zero();
    let j0 = derive_j0(&h, nonce);

    ctr_xor_gcm(&cipher, j0, &mut buf[..n]);
    let s = ghash_aad_ct_len(&h, aad, &buf[..n]);
    let mut ej0 = j0.to_be_bytes();
    cipher.encrypt_block(&mut ej0);
    for i in 0..SIZE_TAG {
        buf[n + i] = s[i] ^ ej0[i];
    }
}

/// SM4-GCM authenticated decryption, in place. `buf` is `ciphertext || tag`;
/// on success the plaintext occupies `buf[..returned_len]` and the tag region
/// is left untouched (caller zeroes it). Returns the plaintext length.
pub fn sm4_gcm_decrypt_inplace(
    key: &Sm4Key,
    nonce: &[u8],
    aad: &[u8],
    buf: &mut [u8],
) -> Result<usize, ()> {
    if buf.len() < SIZE_TAG {
        return Err(());
    }
    let n = buf.len() - SIZE_TAG;
    let cipher = Sm4::new(&key.0);
    let h = cipher.encrypt_zero();
    let j0 = derive_j0(&h, nonce);

    let s = ghash_aad_ct_len(&h, aad, &buf[..n]);
    let mut ej0 = j0.to_be_bytes();
    cipher.encrypt_block(&mut ej0);
    let mut tag = [0u8; SIZE_TAG];
    for i in 0..SIZE_TAG {
        tag[i] = s[i] ^ ej0[i];
    }
    if tag.ct_eq(&buf[n..]).unwrap_u8() != 1 {
        return Err(());
    }
    ctr_xor_gcm(&cipher, j0, &mut buf[..n]);
    Ok(n)
}

/// SM4-GCM authenticated encryption. Returns `ciphertext || tag`.
/// (Allocating convenience wrapper used by the fixed-size handshake buffers.)
pub fn sm4_gcm_aad_encrypt(key: &Sm4Key, nonce: &[u8], aad: &[u8], message: &[u8]) -> Vec<u8> {
    let mut out = Vec::with_capacity(message.len() + SIZE_TAG);
    out.extend_from_slice(message);
    out.extend_from_slice(&[0u8; SIZE_TAG]);
    sm4_gcm_encrypt_inplace(key, nonce, aad, &mut out);
    out
}

/// SM4-GCM authenticated decryption. Input is `ciphertext || tag`.
/// (Allocating convenience wrapper used by the fixed-size handshake buffers.)
pub fn sm4_gcm_aad_decrypt(
    key: &Sm4Key,
    nonce: &[u8],
    aad: &[u8],
    ciphertext: &[u8],
) -> Result<Vec<u8>, ()> {
    let mut buf = ciphertext.to_vec();
    let n = sm4_gcm_decrypt_inplace(key, nonce, aad, &mut buf)?;
    buf.truncate(n);
    Ok(buf)
}

/// SM4 in 128-bit big-endian counter mode (CTR128BE), in place.
///
/// Drop-in for `ctr::Ctr128BE<sm4::Sm4>` as used to wrap the static-KEM
/// ciphertext stream: block `i` keystream = SM4_K(IV + i), full 128-bit
/// big-endian increment, first block uses the IV unchanged.
pub fn sm4_ctr128be_apply(key: &[u8; 16], iv: &[u8; 16], buf: &mut [u8]) {
    let cipher = Sm4::new(key);
    let mut ctr = u128::from_be_bytes(*iv);
    let mut off = 0usize;
    let full = buf.len() / BLOCK;

    let mut done = 0usize;
    while done < full {
        let g = core::cmp::min(8, full - done);
        let mut ks = [[0u8; 16]; 8];
        for slot in ks.iter_mut().take(g) {
            *slot = ctr.to_be_bytes();
            ctr = ctr.wrapping_add(1);
        }
        cipher.encrypt8(&mut ks);
        for k in 0..g {
            let chunk = &mut buf[off + k * BLOCK..off + (k + 1) * BLOCK];
            for (c, s) in chunk.iter_mut().zip(ks[k].iter()) {
                *c ^= *s;
            }
        }
        off += g * BLOCK;
        done += g;
    }

    let rem = buf.len() - off;
    if rem > 0 {
        let mut ks = ctr.to_be_bytes();
        cipher.encrypt_block(&mut ks);
        for (c, s) in buf[off..].iter_mut().zip(ks.iter()) {
            *c ^= *s;
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    // Test vectors from BouncyCastle (same set the original sm4-gcm crate ships).
    #[test]
    fn bouncycastle_vectors() {
        let data: &[([u8; 16], Vec<u8>, Vec<u8>, &[u8], &str)] = &[
            ([0u8; 16], vec![0u8; 12], vec![], b"A", "3c0a0922976fa15e835bc96750e730d967"),
            ([0u8; 16], vec![0u8; 12], vec![], b"hello world",
             "1587c6137e306fed6a6a5f49539b6dd6fe2b7872c3279636db07c2"),
            ([0u8; 16], vec![0xffu8; 12], vec![], b"Hello World!",
             "cba3523bdf74096f3de1f9160a5adb7bf385dea4d50c910e663ec75a"),
            ([0xffu8; 16], vec![0xffu8; 12], vec![], b"Hello World!",
             "99eb1206b5b2a9f9c7d7ec4a81de507f5d79938a10ccd91da68d2fb1"),
            ([0xffu8; 16], vec![0xffu8; 12], vec![0xaau8, 0xbbu8, 0xccu8], b"Hello World!",
             "99eb1206b5b2a9f9c7d7ec4a7be091388b3049363189e64a47d20c19"),
            ([0xffu8; 16], vec![0xffu8; 12], vec![0u8, 1u8, 2u8, 3u8], b"Hello World!",
             "99eb1206b5b2a9f9c7d7ec4ac157a74de0381b3aa170385a113d4f31"),
            ([0u8; 16], vec![0u8; 12], vec![],
             &b"Hello World!Hello World!Hello World!Hello World!Hello World!Hello World!"[..],
             "3587c6137e304fed6a6a5fc0f78e01e5ea4b604843929848601d4b1600e35c1\
              987a30fd521f6b8f66e950cfb735ca19ab45bd8d050a06b2d560a5927a5611f76\
              82cd8c6db56ab52dae82a6db190c54ff8299ac7d339f92db"),
        ];

        for (key, nonce, aad, message, expected) in data {
            let k = Sm4Key(*key);
            let enc = sm4_gcm_aad_encrypt(&k, nonce, aad, message);
            assert_eq!(hex::encode(&enc), expected.replace(['\n', ' '], ""));

            let dec = sm4_gcm_aad_decrypt(&Sm4Key(*key), nonce, aad, &enc).unwrap();
            assert_eq!(&dec, message);
        }
    }

    #[test]
    fn inplace_matches_allocating() {
        let key = [0x5au8; 16];
        let nonce = [0x11u8; 12];
        let aad = [0xde, 0xad, 0xbe, 0xef];
        for len in [0usize, 1, 15, 16, 17, 127, 128, 129, 1420] {
            let msg: Vec<u8> = (0..len).map(|i| (i * 7) as u8).collect();
            // allocating reference
            let reference = sm4_gcm_aad_encrypt(&Sm4Key(key), &nonce, &aad, &msg);
            // in-place
            let mut buf = msg.clone();
            buf.extend_from_slice(&[0u8; SIZE_TAG]);
            sm4_gcm_encrypt_inplace(&Sm4Key(key), &nonce, &aad, &mut buf);
            assert_eq!(buf, reference, "inplace encrypt mismatch at len {}", len);
            // in-place decrypt round-trip
            let n = sm4_gcm_decrypt_inplace(&Sm4Key(key), &nonce, &aad, &mut buf).unwrap();
            assert_eq!(&buf[..n], &msg[..], "inplace decrypt mismatch at len {}", len);
        }
    }

    #[test]
    fn tamper_is_rejected() {
        let k = Sm4Key([7u8; 16]);
        let nonce = [1u8; 12];
        let mut enc = sm4_gcm_aad_encrypt(&k, &nonce, &[], b"secret payload");
        let last = enc.len() - 1;
        enc[last] ^= 1;
        assert!(sm4_gcm_aad_decrypt(&Sm4Key([7u8; 16]), &nonce, &[], &enc).is_err());
    }

    /// Data-plane throughput comparison: old `sm4-gcm` crate (scalar SM4) vs
    /// the in-tree GFNI+AVX2 implementation. Also re-checks that both produce
    /// byte-identical ciphertext (bit-compatibility across the swap).
    ///
    /// Run with: `cargo test --release --features hybrid -- --ignored --nocapture sm4_gcm_throughput`
    #[test]
    #[ignore]
    fn sm4_gcm_throughput() {
        use std::time::Instant;

        let key = [0x42u8; 16];
        let nonce = [0x24u8; 12];
        // WireGuard-sized packets (1420 B payload typical) x many iterations
        let pkt = vec![0xa5u8; 1420];
        let iters = 50_000usize;
        let total_bytes = (pkt.len() * iters) as f64;

        // correctness: identical ciphertext old vs new
        let new_ct = sm4_gcm_aad_encrypt(&Sm4Key(key), &nonce, &[], &pkt);
        let old_ct = sm4_gcm::sm4_gcm_aad_encrypt(&sm4_gcm::Sm4Key(key), &nonce, &[], &pkt);
        assert_eq!(new_ct, old_ct, "in-tree output must match sm4-gcm crate");

        // warmup
        for _ in 0..1000 {
            let _ = sm4_gcm_aad_encrypt(&Sm4Key(key), &nonce, &[], &pkt);
        }

        let mut acc = 0u8;

        let t = Instant::now();
        for _ in 0..iters {
            let c = sm4_gcm_aad_encrypt(&Sm4Key(key), &nonce, &[], &pkt);
            acc ^= c[0];
        }
        let new_secs = t.elapsed().as_secs_f64();

        // in-place (data-plane hot path): reuse one buffer, no per-packet alloc
        let mut buf = vec![0u8; pkt.len() + SIZE_TAG];
        let t = Instant::now();
        for _ in 0..iters {
            buf[..pkt.len()].copy_from_slice(&pkt);
            sm4_gcm_encrypt_inplace(&Sm4Key(key), &nonce, &[], &mut buf);
            acc ^= buf[0];
        }
        let inplace_secs = t.elapsed().as_secs_f64();

        let t = Instant::now();
        for _ in 0..iters {
            let c = sm4_gcm::sm4_gcm_aad_encrypt(&sm4_gcm::Sm4Key(key), &nonce, &[], &pkt);
            acc ^= c[0];
        }
        let old_secs = t.elapsed().as_secs_f64();

        let mbps = |secs: f64| total_bytes / secs / (1024.0 * 1024.0);
        println!("\n=== SM4-GCM throughput (1420 B packets, {} iters) ===", iters);
        println!(
            "  old (sm4-gcm crate, scalar SM4):    {:8.1} MB/s  ({:.3}s)",
            mbps(old_secs),
            old_secs
        );
        println!(
            "  new (in-tree GFNI+AVX2, allocating):{:8.1} MB/s  ({:.3}s)  {:.2}x",
            mbps(new_secs),
            new_secs,
            old_secs / new_secs
        );
        println!(
            "  new (in-tree GFNI+AVX2, in-place):  {:8.1} MB/s  ({:.3}s)  {:.2}x",
            mbps(inplace_secs),
            inplace_secs,
            old_secs / inplace_secs
        );
        println!("  (acc={})\n", acc);
    }

    #[test]
    fn ctr_roundtrip_and_long() {
        let key = [9u8; 16];
        let iv = [0u8; 16];
        // length spanning multiple 8-block groups + partial tail
        let mut buf: Vec<u8> = (0..200u32).map(|i| i as u8).collect();
        let orig = buf.clone();
        sm4_ctr128be_apply(&key, &iv, &mut buf);
        assert_ne!(buf, orig);
        sm4_ctr128be_apply(&key, &iv, &mut buf);
        assert_eq!(buf, orig);
    }
}

#[cfg(test)]
mod bench_ceiling {
    use super::*;
    use std::time::Instant;
    #[test]
    #[ignore]
    fn ctr_only_ceiling() {
        let key=[1u8;16]; let iv=[0u8;16];
        let mut buf=vec![0u8;1420];
        for _ in 0..2000 { sm4_ctr128be_apply(&key,&iv,&mut buf); }
        let iters=50_000usize;
        let t=Instant::now();
        for _ in 0..iters { sm4_ctr128be_apply(&key,&iv,&mut buf); }
        let s=t.elapsed().as_secs_f64();
        let mb=(buf.len()*iters) as f64/s/(1024.0*1024.0);
        println!("\n  raw SM4-CTR (incl keysched, no ghash/alloc): {:.1} MB/s\n", mb);
    }
}

#[cfg(test)]
mod bench_ghash {
    use super::*;
    use std::time::Instant;
    #[test]
    #[ignore]
    fn ghash_only() {
        let h=[7u8;16]; let data=vec![0xa5u8;1420]; let iters=50_000usize;
        for _ in 0..2000 { let _=ghash_aad_ct_len(&h,&[],&data); }
        let t=Instant::now();
        let mut acc=0u8;
        for _ in 0..iters { let r=ghash_aad_ct_len(&h,&[],&data); acc^=r[0]; }
        let s=t.elapsed().as_secs_f64();
        let mb=(data.len()*iters) as f64/s/(1024.0*1024.0);
        println!("\n  GHASH-only (ghash crate, incl new+finalize per call): {:.1} MB/s (acc={})\n", mb, acc);
    }
}
