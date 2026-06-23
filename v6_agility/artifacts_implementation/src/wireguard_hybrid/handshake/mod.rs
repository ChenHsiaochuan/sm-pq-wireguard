/* Implementation of the:
 *
 * Noise_IKpsk2_25519_ChaChaPoly_BLAKE2s
 *
 * Protocol pattern, see: http://www.noiseprotocol.org/noise.html.
 * For documentation.
 */

mod device;
mod macs;
mod messages;
mod noise;
mod peer;
mod ratelimiter;
mod timestamp;
mod types;

pub mod agility;
pub mod crypto_params;


#[cfg(test)]
mod tests;
// publicly exposed interface

pub use device::Device;
pub use messages::{MAX_HANDSHAKE_MSG_SIZE, TYPE_COOKIE_REPLY, TYPE_INITIATION, TYPE_RESPONSE};

// Crypto-agility (v6): runtime selection of the ephemeral post-quantum KEM.
// Callers reach these through `handshake::agility::*`; the re-export is a
// convenience for external users of the handshake API.
#[allow(unused_imports)]
pub use agility::{
    active_suite, available_suites, init_from_env, set_active_suite_by_name, set_active_suite_id,
    suite_by_id, suite_by_token, EphemeralKemSuite, KemFamily, ENV_VAR, REGISTRY,
};
