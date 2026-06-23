use std::thread;
use std::time::{Duration, Instant};
use meansd::MeanSD;
use rand_core::{CryptoRng, OsRng, RngCore};
use rand_oqs::rngs::OsRng as OsRng08;
use sm2::SecretKey as DhSecretKey;
use crate::wireguard_hybrid::handshake::agility;
use crate::wireguard_hybrid::handshake::crypto_params::{SIZE_HASH, STATIC_KEM_ALG};
use crate::wireguard_hybrid::handshake::Device;
use crate::wireguard_hybrid::sm_crypto::{
    sm4_gcm_decrypt_inplace, sm4_gcm_encrypt_inplace, Sm4Key, SIZE_TAG,
};

#[allow(dead_code)]
fn setup_devices<R: RngCore + CryptoRng, O: Default>(
    _rng1: &mut R,
    _rng2: &mut R,
    rng3: &mut R,
) -> ([u8; SIZE_HASH], Device<O>, [u8; SIZE_HASH], Device<O>) {
    let kemalg = oqs::kem::Kem::new(STATIC_KEM_ALG).unwrap();

    let sk1 = DhSecretKey::random(&mut OsRng08);
    let pk1 = sk1.public_key();
    let (pk1_pq, sk1_pq) = kemalg.keypair().unwrap();

    let hash1 = Device::<O>::hash_static_keys(&pk1, &pk1_pq);

    let sk2 = DhSecretKey::random(&mut OsRng08);
    let pk2 = sk2.public_key();
    let (pk2_pq, sk2_pq) = kemalg.keypair().unwrap();

    let hash2 = Device::<O>::hash_static_keys(&pk2, &pk2_pq);

    let mut psk = [0u8; 32];
    rng3.fill_bytes(&mut psk[..]);

    let mut dev1 = Device::new();
    let mut dev2 = Device::new();

    dev1.set_sk(Some((sk1, sk1_pq, pk1_pq.clone())));
    dev2.set_sk(Some((sk2, sk2_pq, pk2_pq.clone())));

    dev1.add(&pk2, &pk2_pq, O::default()).unwrap();
    dev2.add(&pk1, &pk1_pq, O::default()).unwrap();

    dev1.set_psk(&hash2, psk).unwrap();
    dev2.set_psk(&hash1, psk).unwrap();

    (hash1, dev1, hash2, dev2)
}

fn wait() {
    thread::sleep(Duration::from_millis(20));
}

/// Benchmark the hybrid handshake under **every** registered & available
/// ephemeral-KEM suite. The single external interface
/// (`agility::set_active_suite_id`) selects the per-handshake KEM at run time;
/// the static identity KEM (Classic McEliece) stays fixed across all rows.
pub fn benchmark_hybrid_handshake(nb_iter: u32) {
    // Static identity keys are independent of the (agile) ephemeral KEM, so we
    // set the devices up once and reuse them across every suite.
    let kemalg = oqs::kem::Kem::new(STATIC_KEM_ALG).unwrap();
    let sk1 = DhSecretKey::random(&mut OsRng08);
    let pk1 = sk1.public_key();
    let (pk1_pq, sk1_pq) = kemalg.keypair().unwrap();
    let hash1 = Device::<usize>::hash_static_keys(&pk1, &pk1_pq);

    let sk2 = DhSecretKey::random(&mut OsRng08);
    let pk2 = sk2.public_key();
    let (pk2_pq, sk2_pq) = kemalg.keypair().unwrap();
    let hash2 = Device::<usize>::hash_static_keys(&pk2, &pk2_pq);

    let mut dev1: Device<usize> = Device::new();
    let mut dev2: Device<usize> = Device::new();

    dev1.set_sk(Some((sk1, sk1_pq, pk1_pq.clone())));
    dev2.set_sk(Some((sk2, sk2_pq, pk2_pq.clone())));

    dev1.add(&pk2, &pk2_pq, 0).unwrap();
    dev2.add(&pk1, &pk1_pq, 0).unwrap();

    let suites = agility::available_suites();

    println!(
        "Hybrid-WireGuard crypto agility — static KEM anchor: {}",
        STATIC_KEM_ALG
    );
    println!(
        "Agile ephemeral KEM: {}/{} registered suites available in this liboqs build\n",
        suites.len(),
        agility::REGISTRY.len()
    );
    println!(
        "{:<16} {:>9} {:>9} {:>11} {:>9} {:>11} {:>9}   {}",
        "ephemeral KEM", "InitHello", "RespHello",
        "Init(ms)", "InitSD", "Resp(ms)", "RespSD", "standard"
    );
    println!("{}", "-".repeat(104));

    for suite in &suites {
        // ---- single external interface selecting the protocol ----
        agility::set_active_suite_id(suite.id).expect("suite selectable");

        let mut meansd_init = MeanSD::default();
        let mut meansd_resp = MeanSD::default();
        let mut init_size: Vec<usize> = Vec::new();
        let mut resp_size: Vec<usize> = Vec::new();

        for _i in 0..nb_iter {
            let now = Instant::now();
            let msg1 = dev1.begin(&mut OsRng, &hash2).unwrap();
            meansd_init.update(now.elapsed().as_secs_f64() * 1000.0);
            init_size.push(msg1.len());

            let now = Instant::now();
            let (_, msg2, ks_r) = dev2
                .process(&mut OsRng, &msg1, None)
                .expect("failed to process initiation");
            meansd_resp.update(now.elapsed().as_secs_f64() * 1000.0);

            let ks_r = ks_r.unwrap();
            let msg2 = msg2.unwrap();
            resp_size.push(msg2.len());

            let (_, _msg3, ks_i) = dev1
                .process(&mut OsRng, &msg2, None)
                .expect("failed to process response");
            let ks_i = ks_i.unwrap();

            dev1.release(ks_i.local_id());
            dev2.release(ks_r.local_id());
            wait();
        }

        // within one suite, every handshake has identical size
        for e in &init_size {
            assert_eq!(e, &init_size[0]);
        }
        for e in &resp_size {
            assert_eq!(e, &resp_size[0]);
        }

        println!(
            "{:<16} {:>9} {:>9} {:>11.3} {:>9.3} {:>11.3} {:>9.3}   {}",
            suite.token,
            init_size[0],
            resp_size[0],
            meansd_init.mean(),
            meansd_init.sstdev(),
            meansd_resp.mean(),
            meansd_resp.sstdev(),
            suite.label,
        );
    }

    // restore default
    agility::set_active_suite_id(agility::DEFAULT_SUITE_ID).unwrap();

    dev1.remove(&hash2).unwrap();
    dev2.remove(&hash1).unwrap();
}

/// Application-payload sweep for the *end-to-end* latency figures.
///
/// For every registered & available ephemeral-KEM suite we measure two REAL,
/// independent costs and add them:
///
///   * the per-suite **handshake** cost — `Init(ms)` = building InitHello on the
///     initiator (`dev1.begin`), `Resp(ms)` = consuming InitHello and building
///     RespHello on the responder (`dev2.process`); this is a fixed per-suite
///     offset, exactly the columns reported by `benchmark_hybrid_handshake`.
///   * the **data-plane** cost of moving an application payload of `n` bytes
///     through the v5/v6 in-tree GFNI+CLMUL SM4-GCM AEAD — `sm4_gcm_encrypt_*`
///     on the sender (initiator), `sm4_gcm_decrypt_*` on the receiver
///     (responder). This is identical across suites (the data plane is KEM
///     agnostic), so it contributes the same slope to every line.
///
/// End-to-end latency on a side = handshake(suite) + dataplane(payload). The
/// initiator figure uses (begin + encrypt); the responder figure uses
/// (process + decrypt). Output is CSV on stdout:
///
///   role,suite,token,family,payload_bytes,handshake_ms,dataplane_ms,total_ms
///
/// so the plotting script consumes only真实 measured numbers.
pub fn benchmark_payload_latency(nb_iter: u32) {
    // ---- static identity setup (KEM-agnostic), reused across suites ----
    let kemalg = oqs::kem::Kem::new(STATIC_KEM_ALG).unwrap();
    let sk1 = DhSecretKey::random(&mut OsRng08);
    let pk1 = sk1.public_key();
    let (pk1_pq, sk1_pq) = kemalg.keypair().unwrap();
    let hash1 = Device::<usize>::hash_static_keys(&pk1, &pk1_pq);

    let sk2 = DhSecretKey::random(&mut OsRng08);
    let pk2 = sk2.public_key();
    let (pk2_pq, sk2_pq) = kemalg.keypair().unwrap();
    let hash2 = Device::<usize>::hash_static_keys(&pk2, &pk2_pq);

    let mut dev1: Device<usize> = Device::new();
    let mut dev2: Device<usize> = Device::new();
    dev1.set_sk(Some((sk1, sk1_pq, pk1_pq.clone())));
    dev2.set_sk(Some((sk2, sk2_pq, pk2_pq.clone())));
    dev1.add(&pk2, &pk2_pq, 0).unwrap();
    dev2.add(&pk1, &pk1_pq, 0).unwrap();

    // ---- application-payload sweep (log-spaced), bytes ----
    let payloads: [usize; 11] = [
        64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536,
    ];

    // ---- data-plane cost per payload size (KEM-agnostic), measured once ----
    let key = Sm4Key([0x11u8; 16]);
    let nonce = [0u8; 12];
    let aad: [u8; 0] = [];
    let mut enc_ms = [0f64; 11];
    let mut dec_ms = [0f64; 11];
    for (pi, &n) in payloads.iter().enumerate() {
        // iterate more for small payloads so timing is stable
        let dp_iter: u32 = ((8_000_000 / n.max(1)) as u32).max(500);

        // encrypt: buf = plaintext(n) || tag scratch
        let mut buf = vec![0u8; n + SIZE_TAG];
        // warmup
        for _ in 0..64 {
            sm4_gcm_encrypt_inplace(&key, &nonce, &aad, &mut buf);
        }
        let mut m_enc = MeanSD::default();
        for _ in 0..dp_iter {
            let now = Instant::now();
            sm4_gcm_encrypt_inplace(&key, &nonce, &aad, &mut buf);
            m_enc.update(now.elapsed().as_secs_f64() * 1000.0);
        }
        enc_ms[pi] = m_enc.mean();

        // decrypt: buf now holds ciphertext||tag from the last encrypt above
        let ct = buf.clone();
        let mut dbuf = ct.clone();
        for _ in 0..64 {
            dbuf.copy_from_slice(&ct);
            let _ = sm4_gcm_decrypt_inplace(&key, &nonce, &aad, &mut dbuf);
        }
        let mut m_dec = MeanSD::default();
        for _ in 0..dp_iter {
            dbuf.copy_from_slice(&ct);
            let now = Instant::now();
            let _ = sm4_gcm_decrypt_inplace(&key, &nonce, &aad, &mut dbuf);
            m_dec.update(now.elapsed().as_secs_f64() * 1000.0);
        }
        dec_ms[pi] = m_dec.mean();
    }

    let suites = agility::available_suites();

    // ---- per-suite handshake offsets (real), measured ROUND-ROBIN ----
    // Timing each suite in one contiguous block lets CPU turbo/thermal drift
    // separate the suites as much as the algorithm does (e.g. ML-KEM-768 can
    // look "faster" than ML-KEM-512 — non-physical, since both are dominated by
    // the same fixed static-McEliece encapsulation). Interleaving the suites
    // every round spreads each suite's samples across the whole run, so drift
    // averages out and what remains is the true per-suite ephemeral-KEM cost.
    let mut m_init: Vec<MeanSD> = (0..suites.len()).map(|_| MeanSD::default()).collect();
    let mut m_resp: Vec<MeanSD> = (0..suites.len()).map(|_| MeanSD::default()).collect();

    // brief warmup round (touch every suite once; discard timings)
    for (_si, suite) in suites.iter().enumerate() {
        agility::set_active_suite_id(suite.id).expect("suite selectable");
        let msg1 = dev1.begin(&mut OsRng, &hash2).unwrap();
        let (_, msg2, ks_r) = dev2.process(&mut OsRng, &msg1, None).unwrap();
        let (ks_r, msg2) = (ks_r.unwrap(), msg2.unwrap());
        let (_, _m3, ks_i) = dev1.process(&mut OsRng, &msg2, None).unwrap();
        dev1.release(ks_i.unwrap().local_id());
        dev2.release(ks_r.local_id());
        wait();
    }

    for _round in 0..nb_iter {
        for (si, suite) in suites.iter().enumerate() {
            agility::set_active_suite_id(suite.id).expect("suite selectable");

            let now = Instant::now();
            let msg1 = dev1.begin(&mut OsRng, &hash2).unwrap();
            m_init[si].update(now.elapsed().as_secs_f64() * 1000.0);

            let now = Instant::now();
            let (_, msg2, ks_r) = dev2
                .process(&mut OsRng, &msg1, None)
                .expect("failed to process initiation");
            m_resp[si].update(now.elapsed().as_secs_f64() * 1000.0);

            let ks_r = ks_r.unwrap();
            let msg2 = msg2.unwrap();
            let (_, _msg3, ks_i) = dev1
                .process(&mut OsRng, &msg2, None)
                .expect("failed to process response");
            let ks_i = ks_i.unwrap();
            dev1.release(ks_i.local_id());
            dev2.release(ks_r.local_id());
            wait();
        }
    }

    // CSV header
    println!("role,suite,token,family,payload_bytes,handshake_ms,dataplane_ms,total_ms");

    for (si, suite) in suites.iter().enumerate() {
        let hs_init = m_init[si].mean();
        let hs_resp = m_resp[si].mean();
        let family = format!("{:?}", suite.family);

        for (pi, &n) in payloads.iter().enumerate() {
            // initiator side: build InitHello + encrypt payload as sender
            println!(
                "init,{},{},{},{},{:.6},{:.6},{:.6}",
                suite.id, suite.token, family, n, hs_init, enc_ms[pi], hs_init + enc_ms[pi]
            );
            // responder side: process InitHello+build RespHello + decrypt payload
            println!(
                "respond,{},{},{},{},{:.6},{:.6},{:.6}",
                suite.id, suite.token, family, n, hs_resp, dec_ms[pi], hs_resp + dec_ms[pi]
            );
        }
    }

    agility::set_active_suite_id(agility::DEFAULT_SUITE_ID).unwrap();
    dev1.remove(&hash2).unwrap();
    dev2.remove(&hash1).unwrap();
}

/// Per-suite handshake comparison for the *crypto-agility cost* figure.
///
/// The ephemeral-KEM choice is the **only** thing that differs between suites
/// (the static-McEliece anchor and the SM4-GCM data plane are identical), so to
/// show the difference cleanly we strip the data plane entirely and report just
/// the handshake, per role, with its sample standard deviation and the on-wire
/// message size. Suites are measured ROUND-ROBIN so CPU drift averages out.
///
/// CSV: role,suite,token,family,handshake_ms,handshake_sd,onwire_bytes
pub fn benchmark_kem_summary(nb_iter: u32) {
    let kemalg = oqs::kem::Kem::new(STATIC_KEM_ALG).unwrap();
    let sk1 = DhSecretKey::random(&mut OsRng08);
    let pk1 = sk1.public_key();
    let (pk1_pq, sk1_pq) = kemalg.keypair().unwrap();
    let hash1 = Device::<usize>::hash_static_keys(&pk1, &pk1_pq);

    let sk2 = DhSecretKey::random(&mut OsRng08);
    let pk2 = sk2.public_key();
    let (pk2_pq, sk2_pq) = kemalg.keypair().unwrap();
    let hash2 = Device::<usize>::hash_static_keys(&pk2, &pk2_pq);

    let mut dev1: Device<usize> = Device::new();
    let mut dev2: Device<usize> = Device::new();
    dev1.set_sk(Some((sk1, sk1_pq, pk1_pq.clone())));
    dev2.set_sk(Some((sk2, sk2_pq, pk2_pq.clone())));
    dev1.add(&pk2, &pk2_pq, 0).unwrap();
    dev2.add(&pk1, &pk1_pq, 0).unwrap();

    let suites = agility::available_suites();
    let mut m_init: Vec<MeanSD> = (0..suites.len()).map(|_| MeanSD::default()).collect();
    let mut m_resp: Vec<MeanSD> = (0..suites.len()).map(|_| MeanSD::default()).collect();
    let mut init_bytes = vec![0usize; suites.len()];
    let mut resp_bytes = vec![0usize; suites.len()];

    // warmup
    for suite in suites.iter() {
        agility::set_active_suite_id(suite.id).expect("suite selectable");
        let msg1 = dev1.begin(&mut OsRng, &hash2).unwrap();
        let (_, msg2, ks_r) = dev2.process(&mut OsRng, &msg1, None).unwrap();
        let (ks_r, msg2) = (ks_r.unwrap(), msg2.unwrap());
        let (_, _m3, ks_i) = dev1.process(&mut OsRng, &msg2, None).unwrap();
        dev1.release(ks_i.unwrap().local_id());
        dev2.release(ks_r.local_id());
        wait();
    }

    for _round in 0..nb_iter {
        for (si, suite) in suites.iter().enumerate() {
            agility::set_active_suite_id(suite.id).expect("suite selectable");

            let now = Instant::now();
            let msg1 = dev1.begin(&mut OsRng, &hash2).unwrap();
            m_init[si].update(now.elapsed().as_secs_f64() * 1000.0);
            init_bytes[si] = msg1.len();

            let now = Instant::now();
            let (_, msg2, ks_r) = dev2
                .process(&mut OsRng, &msg1, None)
                .expect("failed to process initiation");
            m_resp[si].update(now.elapsed().as_secs_f64() * 1000.0);

            let ks_r = ks_r.unwrap();
            let msg2 = msg2.unwrap();
            resp_bytes[si] = msg2.len();
            let (_, _msg3, ks_i) = dev1
                .process(&mut OsRng, &msg2, None)
                .expect("failed to process response");
            dev1.release(ks_i.unwrap().local_id());
            dev2.release(ks_r.local_id());
            wait();
        }
    }

    println!("role,suite,token,family,handshake_ms,handshake_sd,onwire_bytes");
    for (si, suite) in suites.iter().enumerate() {
        let family = format!("{:?}", suite.family);
        println!(
            "init,{},{},{},{:.6},{:.6},{}",
            suite.id, suite.token, family, m_init[si].mean(), m_init[si].sstdev(), init_bytes[si]
        );
        println!(
            "respond,{},{},{},{:.6},{:.6},{}",
            suite.id, suite.token, family, m_resp[si].mean(), m_resp[si].sstdev(), resp_bytes[si]
        );
    }

    agility::set_active_suite_id(agility::DEFAULT_SUITE_ID).unwrap();
    dev1.remove(&hash2).unwrap();
    dev2.remove(&hash1).unwrap();
}
