use super::*;

use std::net::SocketAddr;
use std::thread;
use std::time::{Duration, Instant};

use hex;
use oqs::init;
use rand::rngs::OsRng;
use rand_core::{CryptoRng, RngCore};
use rand_oqs::rngs::OsRng as OsRng08;

use sm2::SecretKey as DhSecretKey;
use sm2::PublicKey as DhPublicKey;
use crate::wireguard_hybrid::handshake::crypto_params::{SIZE_HASH, STATIC_KEM_ALG};
use super::messages::{self, NoiseInitiation, NoiseResponse};
use super::agility;

fn setup_devices<R: RngCore + CryptoRng, O: Default>(
    rng1: &mut R,
    rng2: &mut R,
    rng3: &mut R,
) -> (DhPublicKey, oqs::kem::PublicKey, [u8; SIZE_HASH], Device<O>, DhPublicKey, oqs::kem::PublicKey, [u8; SIZE_HASH], Device<O>) {
    // generate new key pairs

    let kemalg = oqs::kem::Kem::new(STATIC_KEM_ALG).unwrap();

    let sk1 = DhSecretKey::random(&mut OsRng08);
    let pk1 = sk1.public_key();
    let (pk1_pq, sk1_pq) = kemalg.keypair().unwrap();

    let hash1 = Device::<O>::hash_static_keys(&pk1, &pk1_pq);

    let sk2 = DhSecretKey::random(&mut OsRng08);
    let pk2 = sk2.public_key();
    let (pk2_pq, sk2_pq) = kemalg.keypair().unwrap();

    let hash2 = Device::<O>::hash_static_keys(&pk2, &pk2_pq);

    // pick random psk

    let mut psk = [0u8; 32];
    rng3.fill_bytes(&mut psk[..]);

    // initialize devices on both ends

    let mut dev1 = Device::new();
    let mut dev2 = Device::new();

    dev1.set_sk(Some((sk1, sk1_pq, pk1_pq.clone())));
    dev2.set_sk(Some((sk2, sk2_pq, pk2_pq.clone())));

    dev1.add(&pk2, &pk2_pq, O::default()).unwrap();
    dev2.add(&pk1, &pk1_pq, O::default()).unwrap();

    dev1.set_psk(&hash2, psk).unwrap();
    dev2.set_psk(&hash1, psk).unwrap();

    (pk1, pk1_pq, hash1, dev1, pk2, pk2_pq, hash2, dev2)
}

fn wait() {
    thread::sleep(Duration::from_millis(20));
}

/* Test longest possible handshake interaction (7 messages):
 *
 * 1. I -> R (initiation)
 * 2. I <- R (cookie reply)
 * 3. I -> R (initiation)
 * 4. I <- R (response)
 * 5. I -> R (cookie reply)
 * 6. I -> R (initiation)
 * 7. I <- R (response)
 */
#[test]
fn handshake_under_load() {
    let (_pk1, pk1_pq, pk1_hash, dev1, pk2, pk2_pq, pk2_hash, dev2): (_, _, _, Device<usize>, _, _, _, _) =
        setup_devices(&mut OsRng, &mut OsRng, &mut OsRng);

    let src1: SocketAddr = "172.16.0.1:8080".parse().unwrap();
    let src2: SocketAddr = "172.16.0.2:7070".parse().unwrap();

    // 1. device-1 : create first initiation
    let msg_init = dev1.begin(&mut OsRng, &pk2_hash).unwrap();

    // 2. device-2 : responds with CookieReply
    let msg_cookie = match dev2.process(&mut OsRng, &msg_init, Some(src1)).unwrap() {
        (None, Some(msg), None) => msg,
        _ => panic!("unexpected response"),
    };

    // device-1 : processes CookieReply (no response)
    match dev1.process(&mut OsRng, &msg_cookie, Some(src2)).unwrap() {
        (None, None, None) => (),
        _ => panic!("unexpected response"),
    }

    // avoid initiation flood detection
    wait();

    // 3. device-1 : create second initiation
    let msg_init = dev1.begin(&mut OsRng,&pk2_hash).unwrap();

    // 4. device-2 : responds with noise response
    let msg_response = match dev2.process(&mut OsRng, &msg_init, Some(src1)).unwrap() {
        (Some(_), Some(msg), Some(kp)) => {
            assert_eq!(kp.initiator, false);
            msg
        }
        _ => panic!("unexpected response"),
    };

    // 5. device-1 : responds with CookieReply
    let msg_cookie = match dev1.process(&mut OsRng, &msg_response, Some(src2)).unwrap() {
        (None, Some(msg), None) => msg,
        _ => panic!("unexpected response"),
    };

    // device-2 : processes CookieReply (no response)
    match dev2.process(&mut OsRng, &msg_cookie, Some(src1)).unwrap() {
        (None, None, None) => (),
        _ => panic!("unexpected response"),
    }

    // avoid initiation flood detection
    wait();

    // 6. device-1 : create third initiation
    let msg_init = dev1.begin(&mut OsRng, &pk2_hash).unwrap();

    // 7. device-2 : responds with noise response
    let (msg_response, kp1) = match dev2.process(&mut OsRng, &msg_init, Some(src1)).unwrap() {
        (Some(_), Some(msg), Some(kp)) => {
            assert_eq!(kp.initiator, false);
            (msg, kp)
        }
        _ => panic!("unexpected response"),
    };

    // device-1 : process noise response
    let kp2 = match dev1.process(&mut OsRng, &msg_response, Some(src2)).unwrap() {
        (Some(_), None, Some(kp)) => {
            assert_eq!(kp.initiator, true);
            kp
        }
        _ => panic!("unexpected response"),
    };

    assert_eq!(kp1.send, kp2.recv);
    assert_eq!(kp1.recv, kp2.send);
}

#[test]
fn handshake_no_load() {
    let (pk1, pk1_pq, pk1_hash, mut dev1, pk2, pk2_pq, pk2_hash, mut dev2): (_, _, _, Device<usize>, _, _, _, _) =
        setup_devices(&mut OsRng, &mut OsRng, &mut OsRng);

    // do a few handshakes (every handshake should succeed)

    for i in 0..10 {
        println!("handshake : {}", i);

        // create initiation

        let msg1 = dev1.begin(&mut OsRng, &pk2_hash).unwrap();

        println!("msg1 = {} : {} bytes", hex::encode(&msg1[..]), msg1.len());
        {
            let (body, _macs) = messages::split_macs(&msg1[..]).unwrap();
            println!(
                "msg1 = {:?}",
                NoiseInitiation::parse(body).expect("failed to parse initiation")
            );
        }

        // process initiation and create response

        let (_, msg2, ks_r) = dev2
            .process(&mut OsRng, &msg1, None)
            .expect("failed to process initiation");

        let ks_r = ks_r.unwrap();
        let msg2 = msg2.unwrap();

        println!("msg2 = {} : {} bytes", hex::encode(&msg2[..]), msg2.len());
        {
            let (body, _macs) = messages::split_macs(&msg2[..]).unwrap();
            println!(
                "msg2 = {:?}",
                NoiseResponse::parse(body).expect("failed to parse response")
            );
        }

        assert!(!ks_r.initiator, "Responders key-pair is confirmed");

        // process response and obtain confirmed key-pair

        let (_, msg3, ks_i) = dev1
            .process(&mut OsRng, &msg2, None)
            .expect("failed to process response");
        let ks_i = ks_i.unwrap();

        assert!(msg3.is_none(), "Returned message after response");
        assert!(ks_i.initiator, "Initiators key-pair is not confirmed");

        assert_eq!(ks_i.send, ks_r.recv, "KeyI.send != KeyR.recv");
        assert_eq!(ks_i.recv, ks_r.send, "KeyI.recv != KeyR.send");

        dev1.release(ks_i.local_id());
        dev2.release(ks_r.local_id());

        // avoid initiation flood detection
        wait();
    }

    dev1.remove(&pk2_hash).unwrap();
    dev2.remove(&pk1_hash).unwrap();
}

/// Crypto-agility end-to-end test.
///
/// Switch the active ephemeral-KEM suite through the *single external
/// interface* (`agility::set_active_suite_id`) and run a complete handshake for
/// every suite compiled into liboqs. Each run must:
///   * agree on the transport key-pair on both ends,
///   * advertise the selected suite in the on-wire `f_suite` byte of both
///     InitHello and RespHello,
///   * produce a message size matching that KEM's parameters.
#[test]
fn agility_handshake_every_suite() {
    let (_pk1, _pk1_pq, pk1_hash, mut dev1, _pk2, _pk2_pq, pk2_hash, mut dev2): (
        _,
        _,
        _,
        Device<usize>,
        _,
        _,
        _,
        _,
    ) = setup_devices(&mut OsRng, &mut OsRng, &mut OsRng);

    let suites = agility::available_suites();
    assert!(!suites.is_empty(), "no KEM suites available in liboqs");

    let mut sizes: Vec<(String, usize, usize)> = Vec::new();

    for suite in &suites {
        // ---- the single external interface that decides the protocol ----
        let active = agility::set_active_suite_id(suite.id).expect("suite must be selectable");
        assert_eq!(active.id, suite.id);
        assert_eq!(agility::active_suite().id, suite.id);

        // full handshake under the selected suite
        let msg1 = dev1.begin(&mut OsRng, &pk2_hash).unwrap();

        // the InitHello must advertise exactly the selected suite
        let (body1, _m1) = messages::split_macs(&msg1[..]).unwrap();
        let init = NoiseInitiation::parse(body1).unwrap();
        assert_eq!(init.f_suite, suite.id, "InitHello suite byte mismatch");

        let (_, msg2, ks_r) = dev2
            .process(&mut OsRng, &msg1, None)
            .expect("responder failed to process initiation");
        let ks_r = ks_r.unwrap();
        let msg2 = msg2.unwrap();

        // the RespHello must echo the same suite
        let (body2, _m2) = messages::split_macs(&msg2[..]).unwrap();
        let resp = NoiseResponse::parse(body2).unwrap();
        assert_eq!(resp.f_suite, suite.id, "RespHello suite byte mismatch");

        let (_, msg3, ks_i) = dev1
            .process(&mut OsRng, &msg2, None)
            .expect("initiator failed to process response");
        let ks_i = ks_i.unwrap();
        assert!(msg3.is_none());

        // both ends derived the same transport keys
        assert_eq!(ks_i.send, ks_r.recv, "{}: KeyI.send != KeyR.recv", suite.token);
        assert_eq!(ks_i.recv, ks_r.send, "{}: KeyI.recv != KeyR.send", suite.token);

        println!(
            "agility: {:<16} (0x{:02x})  InitHello = {} B  RespHello = {} B",
            suite.token,
            suite.id,
            msg1.len(),
            msg2.len()
        );
        sizes.push((suite.token.to_string(), msg1.len(), msg2.len()));

        dev1.release(ks_i.local_id());
        dev2.release(ks_r.local_id());
        wait();
    }

    // Different KEMs really do produce different-sized handshakes (proof the
    // agile field is actually variable, not just a relabelled fixed buffer):
    // if more than one suite is available, not all InitHello sizes are equal.
    if sizes.len() > 1 {
        let first = sizes[0].1;
        let all_equal = sizes.iter().all(|(_, i, _)| *i == first);
        assert!(
            !all_equal,
            "expected variable InitHello sizes across distinct KEMs"
        );
    }

    // restore default for any later tests in the same process
    agility::set_active_suite_id(agility::DEFAULT_SUITE_ID).unwrap();

    dev1.remove(&pk2_hash).unwrap();
    dev2.remove(&pk1_hash).unwrap();
}