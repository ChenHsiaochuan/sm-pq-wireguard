//! In-tree, hardware-accelerated国密 (SM) symmetric crypto for the SM2/SM3/SM4
//! hybrid WireGuard data plane and handshake.
//!
//! This module replaces the external `sm4-gcm` / `sm4` / `ctr` crates on the
//! hot path with an SM4 core that uses Intel **GFNI + AVX2** (8-way parallel
//! S-box) and a **CLMUL**-backed GHASH, with portable scalar fallbacks. See
//! `sm4.rs` and `gcm.rs` for details and the optimization references.

pub mod gcm;
pub mod sm4;

pub use gcm::{
    sm4_ctr128be_apply, sm4_gcm_aad_decrypt, sm4_gcm_aad_encrypt, sm4_gcm_decrypt_inplace,
    sm4_gcm_encrypt_inplace, Sm4Key, SIZE_TAG,
};
