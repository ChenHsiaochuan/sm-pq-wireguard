//! Crypto-agility layer for the post-quantum *ephemeral* KEM (v6).
//!
//! # What this module gives us
//!
//! v1–v5 hard-wired a single ephemeral KEM (ML-KEM-512, i.e. FIPS 203 level 1)
//! at *compile time* via a `const oqs::kem::Algorithm`. Replacing it meant
//! editing source and recompiling — which violates the definition of crypto
//! agility:
//!
//! > *"Crypto agility describes the capabilities needed to replace and adapt
//! >  cryptographic algorithms for protocols, applications, software, hardware,
//! >  and infrastructures **without interrupting the flow of a running
//! >  system** to achieve resiliency."*
//!
//! v6 turns the ephemeral KEM into a value selected at **run time** through a
//! single external interface (see [`set_active_suite_by_name`] /
//! [`init_from_env`]). Every InitHello / RespHello now carries a one-byte
//! **suite identifier** on the wire, so the two peers negotiate the KEM
//! per-handshake: the initiator stamps the suite it chose, the responder
//! decapsulates with exactly that algorithm. Changing the active suite affects
//! only *new* handshakes; sessions already running keep their keys. Nothing has
//! to be recompiled or restarted.
//!
//! # Why the *ephemeral* KEM (and not the static one)
//!
//! The handshake uses two KEMs:
//!   * a **static** KEM (Classic McEliece) bound to each peer's long-term
//!     identity — changing it means re-issuing identity keys out-of-band, so it
//!     is a deployment-time anchor, not a per-session knob; it stays fixed here.
//!   * an **ephemeral** KEM (ML-KEM by default) generated fresh per handshake —
//!     this is the forward-secret, per-session encapsulation and the natural,
//!     meaningful axis of agility. v6 makes *this* one agile.
//!
//! # A note on FIPS 203 / 204 / 205 / 206
//!
//! Only **FIPS 203 (ML-KEM)** is a Key Encapsulation Mechanism. FIPS 204
//! (ML-DSA), FIPS 205 (SLH-DSA) and the draft FIPS 206 (FN-DSA / Falcon) are
//! **digital-signature** standards and cannot perform key encapsulation, so
//! they are not drop-in replacements for the KEM. Agility *for key
//! establishment* therefore means switching among KEMs: the whole FIPS 203
//! family (ML-KEM-512/768/1024) plus other NIST KEM families (code-based HQC,
//! lattice FrodoKEM, the legacy Kyber naming, …). This module registers exactly
//! those.

use std::sync::atomic::{AtomicU8, Ordering};

use oqs::kem::Algorithm;

use super::types::PQError;

/// Family bucket, purely for human-readable reporting.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum KemFamily {
    /// Module-Lattice KEM, FIPS 203 (standardized ML-KEM).
    MlKem,
    /// Pre-standard Kyber naming (round-3 parameters), kept for migration demos.
    Kyber,
    /// Code-based (Hamming Quasi-Cyclic), NIST round-4 / 2025 backup KEM.
    Hqc,
    /// Plain-LWE conservative KEM (FrodoKEM).
    FrodoKem,
}

/// A selectable ephemeral-KEM suite. `id` is the byte that travels on the wire.
#[derive(Clone, Copy, Debug)]
pub struct EphemeralKemSuite {
    /// On-wire identifier (stable across versions; never reuse a value).
    pub id: u8,
    /// liboqs algorithm to instantiate.
    pub alg: Algorithm,
    /// Short stable token used by the external selection interface, e.g. `ml-kem-768`.
    pub token: &'static str,
    /// Human / standards label for reports and logs.
    pub label: &'static str,
    /// Family bucket.
    pub family: KemFamily,
}

// ---------------------------------------------------------------------------
// Registry — the set of KEMs an operator may switch between at run time.
//
// All suites share the same *static* KEM (Classic McEliece, the identity
// anchor); only the ephemeral KEM varies. Add a new KEM by appending an entry
// here and, if it is larger than the current bounds, bumping the MAX_* limits
// below. No other code changes are required — that is the point of agility.
// ---------------------------------------------------------------------------

/// FIPS 203, ML-KEM-512 (NIST security category 1). Default; identical crypto to v5.
pub const SUITE_ML_KEM_512: EphemeralKemSuite = EphemeralKemSuite {
    id: 0x01,
    alg: Algorithm::MlKem512,
    token: "ml-kem-512",
    label: "FIPS 203 ML-KEM-512 (NIST L1)",
    family: KemFamily::MlKem,
};

/// FIPS 203, ML-KEM-768 (NIST security category 3).
pub const SUITE_ML_KEM_768: EphemeralKemSuite = EphemeralKemSuite {
    id: 0x02,
    alg: Algorithm::MlKem768,
    token: "ml-kem-768",
    label: "FIPS 203 ML-KEM-768 (NIST L3)",
    family: KemFamily::MlKem,
};

/// FIPS 203, ML-KEM-1024 (NIST security category 5).
pub const SUITE_ML_KEM_1024: EphemeralKemSuite = EphemeralKemSuite {
    id: 0x03,
    alg: Algorithm::MlKem1024,
    token: "ml-kem-1024",
    label: "FIPS 203 ML-KEM-1024 (NIST L5)",
    family: KemFamily::MlKem,
};

/// Legacy Kyber-512 (round-3 parameters), for "migrate off the pre-standard
/// name onto FIPS 203" demonstrations.
pub const SUITE_KYBER_512: EphemeralKemSuite = EphemeralKemSuite {
    id: 0x11,
    alg: Algorithm::Kyber512,
    token: "kyber-512",
    label: "Kyber-512 (round 3, pre-FIPS)",
    family: KemFamily::Kyber,
};

/// HQC-128 — code-based KEM, NIST round-4 / 2025 backup selection.
/// Cross-family proof: different math *and* a 64-byte shared secret.
pub const SUITE_HQC_128: EphemeralKemSuite = EphemeralKemSuite {
    id: 0x21,
    alg: Algorithm::Hqc128,
    token: "hqc-128",
    label: "HQC-128 (code-based, NIST L1)",
    family: KemFamily::Hqc,
};

/// FrodoKEM-640-AES — conservative plain-LWE KEM.
/// Cross-family proof: ~9.7 KB ciphertext and a 16-byte shared secret, showing
/// the framework is fully size- and secret-length-agnostic.
pub const SUITE_FRODO_640_AES: EphemeralKemSuite = EphemeralKemSuite {
    id: 0x31,
    alg: Algorithm::FrodoKem640Aes,
    token: "frodo-640-aes",
    label: "FrodoKEM-640-AES (conservative LWE)",
    family: KemFamily::FrodoKem,
};

/// The full registry. Order is the reporting / sweep order.
pub const REGISTRY: &[EphemeralKemSuite] = &[
    SUITE_ML_KEM_512,
    SUITE_ML_KEM_768,
    SUITE_ML_KEM_1024,
    SUITE_KYBER_512,
    SUITE_HQC_128,
    SUITE_FRODO_640_AES,
];

/// Default active suite — matches v5 exactly (ML-KEM-512 / FIPS 203 L1).
pub const DEFAULT_SUITE_ID: u8 = SUITE_ML_KEM_512.id;

// ---------------------------------------------------------------------------
// Compile-time upper bounds on the agile (ephemeral) KEM field sizes.
//
// The in-memory message structs reserve MAX-sized buffers so a single struct
// type can hold any registered suite; only the *used* prefix is serialized onto
// the wire, so the actual datagram stays compact for small suites. These bounds
// must cover every entry in REGISTRY — validated at run time by
// `validate_registry()` against liboqs' reported sizes.
//
// Current maxima come from FrodoKEM-640-AES (public key / ciphertext / secret
// key) and HQC-128 (shared secret = 64 B).
// ---------------------------------------------------------------------------

/// Upper bound on an ephemeral KEM public key (FrodoKEM-640-AES = 9616 B).
pub const MAX_EPHEMERAL_KEM_PUB_KEY: usize = 9616;
/// Upper bound on an ephemeral KEM ciphertext (FrodoKEM-640-AES = 9720 B).
pub const MAX_EPHEMERAL_KEM_CIPHERTEXT: usize = 9720;
/// Upper bound on an ephemeral KEM secret key (FrodoKEM-640-AES = 19888 B).
pub const MAX_EPHEMERAL_KEM_SECRET_KEY: usize = 19888;
/// Upper bound on an ephemeral KEM shared secret (HQC = 64 B).
pub const MAX_EPHEMERAL_KEM_SHARED_SECRET: usize = 64;

/// Concrete byte lengths of one suite, as reported by liboqs.
#[derive(Clone, Copy, Debug)]
pub struct KemLengths {
    pub public_key: usize,
    pub secret_key: usize,
    pub ciphertext: usize,
    pub shared_secret: usize,
}

impl EphemeralKemSuite {
    /// Is this algorithm actually compiled into the linked liboqs?
    pub fn is_available(&self) -> bool {
        self.alg.is_enabled()
    }

    /// Query liboqs for this suite's byte lengths. `None` if disabled.
    pub fn lengths(&self) -> Option<KemLengths> {
        let kem = oqs::kem::Kem::new(self.alg).ok()?;
        Some(KemLengths {
            public_key: kem.length_public_key(),
            secret_key: kem.length_secret_key(),
            ciphertext: kem.length_ciphertext(),
            shared_secret: kem.length_shared_secret(),
        })
    }
}

/// Look up a suite by its on-wire id.
pub fn suite_by_id(id: u8) -> Option<EphemeralKemSuite> {
    REGISTRY.iter().copied().find(|s| s.id == id)
}

/// Look up a suite by its external token (case-insensitive, `_`/`-` agnostic).
pub fn suite_by_token(token: &str) -> Option<EphemeralKemSuite> {
    let norm = |s: &str| s.trim().to_ascii_lowercase().replace('_', "-");
    let want = norm(token);
    REGISTRY.iter().copied().find(|s| norm(s.token) == want)
}

// ---------------------------------------------------------------------------
// The single external interface: one process-wide selector.
//
// `ACTIVE_SUITE_ID` is the live setting consulted by every *new* initiation.
// It can be set at start-up from the environment (`init_from_env`) and changed
// while the daemon runs (`set_active_suite_by_name` / `set_active_suite_id`)
// without touching existing sessions — i.e. agility "without interrupting the
// flow of a running system".
// ---------------------------------------------------------------------------

static ACTIVE_SUITE_ID: AtomicU8 = AtomicU8::new(DEFAULT_SUITE_ID);

/// Environment variable that selects the ephemeral KEM at start-up.
pub const ENV_VAR: &str = "WG_KEM_SUITE";

/// The suite a freshly-created initiation will advertise and use.
pub fn active_suite() -> EphemeralKemSuite {
    let id = ACTIVE_SUITE_ID.load(Ordering::Relaxed);
    suite_by_id(id).unwrap_or(SUITE_ML_KEM_512)
}

/// Set the active suite by on-wire id. Rejects unknown or unavailable suites.
pub fn set_active_suite_id(id: u8) -> Result<EphemeralKemSuite, PQError> {
    let suite = suite_by_id(id).ok_or(PQError::UnknownKemSuite)?;
    if !suite.is_available() {
        return Err(PQError::KemSuiteUnavailable);
    }
    ACTIVE_SUITE_ID.store(id, Ordering::Relaxed);
    Ok(suite)
}

/// Set the active suite by external token, e.g. `"ml-kem-768"` or `"hqc-128"`.
/// This is the primary human/ops-facing selection call.
pub fn set_active_suite_by_name(token: &str) -> Result<EphemeralKemSuite, PQError> {
    let suite = suite_by_token(token).ok_or(PQError::UnknownKemSuite)?;
    set_active_suite_id(suite.id)
}

/// Initialize the active suite from `$WG_KEM_SUITE` (if set & valid).
/// Returns the suite actually in effect. Invalid values fall back to the
/// default and surface an error string for logging.
pub fn init_from_env() -> Result<EphemeralKemSuite, String> {
    match std::env::var(ENV_VAR) {
        Ok(val) if !val.trim().is_empty() => match set_active_suite_by_name(&val) {
            Ok(suite) => Ok(suite),
            Err(_) => Err(format!(
                "{}=\"{}\" is not a known/available KEM suite; using default {}",
                ENV_VAR,
                val,
                active_suite().token
            )),
        },
        _ => Ok(active_suite()),
    }
}

/// Validate that every *available* registered suite fits within the compile-time
/// MAX_* bounds. Called once at start-up; a failure means a registry entry was
/// added without bumping the bounds.
pub fn validate_registry() -> Result<(), PQError> {
    for suite in REGISTRY {
        if let Some(l) = suite.lengths() {
            if l.public_key > MAX_EPHEMERAL_KEM_PUB_KEY {
                return Err(PQError::EphemeralKemExceedsBound);
            }
            if l.ciphertext > MAX_EPHEMERAL_KEM_CIPHERTEXT {
                return Err(PQError::EphemeralKemExceedsBound);
            }
            if l.secret_key > MAX_EPHEMERAL_KEM_SECRET_KEY {
                return Err(PQError::EphemeralKemExceedsBound);
            }
            if l.shared_secret > MAX_EPHEMERAL_KEM_SHARED_SECRET {
                return Err(PQError::EphemeralKemExceedsBound);
            }
        }
    }
    Ok(())
}

/// The registered suites that are actually compiled into this build's liboqs.
pub fn available_suites() -> Vec<EphemeralKemSuite> {
    REGISTRY.iter().copied().filter(|s| s.is_available()).collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn registry_within_bounds() {
        validate_registry().expect("a registered suite exceeds the MAX_* bounds");
    }

    #[test]
    fn ids_and_tokens_are_unique() {
        for (i, a) in REGISTRY.iter().enumerate() {
            for b in &REGISTRY[i + 1..] {
                assert_ne!(a.id, b.id, "duplicate suite id 0x{:02x}", a.id);
                assert_ne!(a.token, b.token, "duplicate token {}", a.token);
            }
        }
    }

    #[test]
    fn default_is_ml_kem_512() {
        assert_eq!(active_suite().alg, Algorithm::MlKem512);
        assert_eq!(DEFAULT_SUITE_ID, 0x01);
    }

    #[test]
    fn lookup_roundtrips() {
        assert_eq!(suite_by_token("ML_KEM_768").unwrap().id, 0x02);
        assert_eq!(suite_by_id(0x21).unwrap().token, "hqc-128");
    }
}
