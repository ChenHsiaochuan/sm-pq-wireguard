// keygen_hybrid.rs -- generate one hybrid (SM2 + Classic McEliece 460896)
// identity keypair for the v6 SM-PQ-WireGuard binary, in the exact hex layout
// the UAPI `set=1` parser (configuration_hybrid/uapi/set.rs) expects.
//
// Output: one line, two space-separated hex blobs:
//     <private_key_hex> <public_key_hex>
//
// Layout (matches set.rs / get.rs):
//   private_key = SM2_secret[32] || McE_secret[13608] || McE_public[524160]   = 537800 B
//   public_key  = SM2_point[33]  || McE_public[524160]                        = 524193 B
//
// Build & run:
//   cargo run --release --features hybrid --example keygen_hybrid
//   (or just: cargo run --release --example keygen_hybrid)

use sm2::elliptic_curve::sec1::ToEncodedPoint;
use sm2::SecretKey as DhSecretKey;
use rand_oqs::rngs::OsRng as OsRng08;

const STATIC_KEM_ALG: oqs::kem::Algorithm = oqs::kem::Algorithm::ClassicMcEliece460896;

fn main() {
    oqs::init();
    let kem = oqs::kem::Kem::new(STATIC_KEM_ALG).expect("init Classic McEliece 460896");

    // SM2 static DH keypair.
    let sk = DhSecretKey::random(&mut OsRng08);
    let pk = sk.public_key();

    // Classic McEliece 460896 static KEM keypair.
    let (pk_pq, sk_pq) = kem.keypair().expect("McEliece keypair");

    // private_key = SM2_secret[32] || McE_secret[13608] || McE_public[524160]
    let mut priv_blob: Vec<u8> = Vec::new();
    priv_blob.extend_from_slice(sk.to_bytes().as_slice());
    priv_blob.extend_from_slice(sk_pq.as_ref());
    priv_blob.extend_from_slice(pk_pq.as_ref());

    // public_key = SM2_point[33] || McE_public[524160]
    let mut pub_blob: Vec<u8> = Vec::new();
    pub_blob.extend_from_slice(pk.to_encoded_point(true).as_bytes());
    pub_blob.extend_from_slice(pk_pq.as_ref());

    println!("{} {}", hex::encode(priv_blob), hex::encode(pub_blob));
}
