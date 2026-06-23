use std::thread;
use std::time::{Duration, Instant};
use meansd::MeanSD;
use rand_core::{CryptoRng, OsRng, RngCore};
use rand_oqs::rngs::OsRng as OsRng08;
use sm2::SecretKey as DhSecretKey;
use crate::wireguard_hybrid::handshake::crypto_params::{EPHEMERAL_KEM_ALG, SIZE_HASH, STATIC_KEM_ALG};
use crate::wireguard_hybrid::handshake::Device;

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

pub fn benchmark_hybrid_handshake(nb_iter: u32) {
    let (pk1_hash, mut dev1, _pk2_hash, mut dev2): (_, Device<usize>, _, _) =
        setup_devices(&mut OsRng, &mut OsRng, &mut OsRng);
    let (_pk1_hash2, _dev1b, pk2_hash, _dev2b): (_, Device<usize>, _, _) =
        setup_devices(&mut OsRng, &mut OsRng, &mut OsRng);

    // Re-setup with correct references (use a single setup call)
    drop(dev1);
    drop(dev2);
    drop(_dev1b);
    drop(_dev2b);

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

    println!("Hybrid-WireGuard: (static kem: {}, ephemeral kem: {})", STATIC_KEM_ALG, EPHEMERAL_KEM_ALG);

    let mut meansd_init = MeanSD::default();
    let mut meansd_resp = MeanSD::default();

    let mut init_size: Vec<usize> = Vec::new();
    let mut resp_size: Vec<usize> = Vec::new();

    for _i in 0..nb_iter {
        // create initiation
        let now = Instant::now();
        let msg1 = dev1.begin(&mut OsRng, &hash2).unwrap();
        let t = now.elapsed().as_secs_f64() * 1000.0;
        meansd_init.update(t);

        init_size.push(msg1.len());

        // process initiation and create response
        let now = Instant::now();
        let (_, msg2, ks_r) = dev2
            .process(&mut OsRng, &msg1, None)
            .expect("failed to process initiation");
        let t = now.elapsed().as_secs_f64() * 1000.0;
        meansd_resp.update(t);

        let ks_r = ks_r.unwrap();
        let msg2 = msg2.unwrap();

        resp_size.push(msg2.len());

        // process response and obtain confirmed key-pair
        let (_, _msg3, ks_i) = dev1
            .process(&mut OsRng, &msg2, None)
            .expect("failed to process response");
        let ks_i = ks_i.unwrap();

        dev1.release(ks_i.local_id());
        dev2.release(ks_r.local_id());

        // avoid initiation flood detection
        wait();
    }

    for e in &init_size {
        assert_eq!(e, &init_size[0]);
    }
    for e in &resp_size {
        assert_eq!(e, &resp_size[0]);
    }

    dev1.remove(&hash2).unwrap();
    dev2.remove(&hash1).unwrap();

    println!("InitHello message size: {:?} bytes\nRespHello message size: {:?} bytes", init_size[0] + 48, resp_size[0] + 48);

    println!("InitHello construction time: {:.3} ms (std = {:.3} ms)", meansd_init.mean(), meansd_init.sstdev());
    println!("InitHello consumption time + RespHello construction time: {:.3} ms (std = {:.3} ms)", meansd_resp.mean(), meansd_resp.sstdev());
}