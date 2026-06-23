# SM-PQ-WireGuard —  Hybrid Post-Quantum WireGuard with Cryptographic Agility

This repository accompanies the paper:

> **"A Hybrid Post-Quantum WireGuard with Cryptographic Agility:
> Instantiation with the SM Suite and Flexible KEM Switching"**

It contains the complete implementation and formal verification artifacts
for **SM-PQ-WireGuard**, the first hybrid post-quantum WireGuard handshake
that unifies GM/T standards compliance (SM2, SM3, SM4) with cryptographic
agility—supporting flexible switching of the ephemeral KEM across six
candidates (ML-KEM-512/768/1024, Kyber-512, HQC-128, Frodo-640-AES)
without protocol-level changes.

---

##  Repository Structure

```
.
├── v1_original/          # Baseline: X25519 + ML-KEM-512 + Classic McEliece
├── v2_sm2/               # SM2 ECDH replaces X25519 (classical layer)
├── v3_sm2_sm3/           # + SM3 hash replaces BLAKE2s
├── v4_sm2_sm3_sm4/       # + SM4-GCM/SM4-CTR replaces ChaCha20-Poly1305
├── v5_optimization/      # + GFNI+AVX2 SM4-GCM data-plane acceleration
└── v6_agility/           # + Cryptographic agility for the ephemeral KEM
```

Each version is self-contained and can be built and tested independently.

### What's inside each version?

| Directory | Purpose |
|---|---|
| `artifacts_implementation/` | Rust implementation (handshake + data plane) |
| `artifacts_evaluation/` | SAPIC⁺ / ProVerif / Tamarin / DeepSec formal models |
| `dockerfile` | Docker build environment |
| `run_basic_test.sh` | Quick smoke-test script |
| `run_docker_clean.sh` | Docker cleanup helper |

v5 adds `OPTIMIZATION.md`; v6 adds `AGILITY.md`, `FORMAL_VERIFICATION_RESULTS.md`,
and `TWO_DEVICE_TEST.md`.

---

##  Paper-to-Code Mapping

| Paper Section | Corresponding Code |
|---|---|
| §3 (Design) — Algorithms 1 & 2 (handshake) | `artifacts_implementation/src/wireguard_hybrid/handshake/` |
| §3.4 — MAC1/MAC2 via HMAC-SM3 | `handshake/macs.rs` |
| §3.4 — Nonce partitioning for SM4-GCM | `handshake/noise.rs` + `handshake/messages.rs` |
| §3.5 — Agility framework (KEM switching) | `handshake/agility.rs` (v6 only) |
| §4.2 — Symbolic verification (ProVerif/Tamarin) | `artifacts_evaluation/` in each version |
| §5 — Performance evaluation | `src/benchmarks/` + data-plane microbenchmarks |

---

##  Quick Start (v6 — Agility)

### Prerequisites

- **Rust** ≥ 1.80 (with `rustup`)
- **liboqs** ≥ 0.10 (post-quantum KEMs)
- **clang** / **cmake** (for C dependencies)
- **Docker** (optional, for formal verification)

### Build & Test

```bash
cd v6_agility/artifacts_implementation

# Install system dependencies (Ubuntu/Debian)
./run_install-dep-rust-clang.sh

# Build with hybrid features
cargo build --release --features hybrid

# Run all tests
cargo test --release --features hybrid
```

### Switching the Ephemeral KEM (Cryptographic Agility)

v6 supports runtime KEM selection via an environment variable—no recompilation needed:

```bash
# Default: ML-KEM-512 (FIPS 203, NIST Level 1)
WG_KEM_SUITE=ml-kem-512    cargo run --release --features hybrid

# Upgrade to stronger lattice KEMs
WG_KEM_SUITE=ml-kem-768    cargo run --release --features hybrid   # NIST Level 3
WG_KEM_SUITE=ml-kem-1024   cargo run --release --features hybrid   # NIST Level 5

# Cross-family diversity
WG_KEM_SUITE=kyber-512     cargo run --release --features hybrid   # Kyber (round 3)
WG_KEM_SUITE=hqc-128       cargo run --release --features hybrid   # Code-based
WG_KEM_SUITE=frodo-640-aes cargo run --release --features hybrid   # Unstructured LWE
```

The static identity KEM (Classic McEliece-460896) remains fixed across all suites.

| Suite ID | KEM | Family | NIST Level | Handshake Size (InitHello/RespHello) |
|---|---|---|---|---|
| `ml-kem-512` | ML-KEM-512 | Lattice (MLWE) | 1 | 1110 / 1018 B |
| `ml-kem-768` | ML-KEM-768 | Lattice (MLWE) | 3 | ~1.3 / 1.4 KiB |
| `ml-kem-1024` | ML-KEM-1024 | Lattice (MLWE) | 5 | ~1.7 / 1.9 KiB |
| `kyber-512` | Kyber-512 | Lattice (MLWE) | 1 | 1110 / 1018 B |
| `hqc-128` | HQC-128 | Code-based | 1 | ~2.8 / 4.6 KiB |
| `frodo-640-aes` | FrodoKEM-640-AES | LWE | 1 | ~5.4 / 9.7 KiB |

> Only ML-KEM-512 and Kyber-512 fit within the IPv6 MTU (1280 B);
> larger suites rely on IP fragmentation.

### Two-Device End-to-End Test

See `v6_agility/TWO_DEVICE_TEST.md` for a step-by-step guide to running
SM-PQ-WireGuard between two real machines (WSL ↔ Mac/Docker), including
iperf3 encrypted throughput testing and live KEM switching.

---

##  Version Evolution

| Version | Classical DH | Hash | Symmetric | PQ-KEM(s) | Key Feature |
|---|---|---|---|---|---|
| **v1** | X25519 | BLAKE2s | ChaCha20-Poly1305 | ML-KEM-512 + McEliece | Baseline hybrid PQ-WireGuard |
| **v2** | SM2 | BLAKE2s | ChaCha20-Poly1305 | ML-KEM-512 + McEliece | GM/T classical curve |
| **v3** | SM2 | SM3 (HMAC) | ChaCha20-Poly1305 | ML-KEM-512 + McEliece | GM/T hashing (inc. MAC1/MAC2 reconstruction) |
| **v4** | SM2 | SM3 | SM4-GCM/SM4-CTR | ML-KEM-512 + McEliece | Full GM/T suite |
| **v5** | SM2 | SM3 | SM4-GCM (GFNI+AVX2) | ML-KEM-512 + McEliece | 4–6× data-plane speedup |
| **v6** | SM2 | SM3 | SM4-GCM (GFNI+AVX2) | McEliece (static) + **agile** (6 options) | Cryptographic agility |

---

##  Formal Verification

The `artifacts_evaluation/` directory in each version contains
**SAPIC⁺** models that auto-generate input for three back-ends:

| Tool | Purpose | Coverage |
|---|---|---|
| **ProVerif** | Trace properties + observational equivalence | CNF compromise conditions, anonymity, strong secrecy |
| **Tamarin** | Independent cross-check (full DH equational theory) | 11/11 trace lemmas verified |
| **DeepSec** | Bounded equivalence (PQ-only reference protocols) | Completeness for the bounded fragment |

### Running Verification

```bash
cd v6_agility/artifacts_evaluation

# Install dependencies (Tamarin + ProVerif + DeepSec)
./run_install-dep-tam-pv-deep.sh

# Trace properties (ProVerif)
./run_trace_properties.sh

# Strong secrecy
./run_strong_secrecy.sh

# Anonymity (observational equivalence)
./run_anonymity.sh
```

> The models across v1–v6 are byte-identical (`diff -rq` confirmed).
> Agility is purely in the implementation layer; the symbolic model
> treats KEMs abstractly, so all suites inherit the same security guarantees.

---

##  Performance Highlights (v6, i7-13700)

| Metric | WireGuard | SM-PQ-WireGuard | Overhead |
|---|---|---|---|
| Handshake (responder) | 0.18 ms | 1.17 ms | Dominated by SM2 ECDH (~1.0 ms) |
| Wire-format overhead | — | **+1 byte** | SM2 SEC1 (33 B) vs X25519 (32 B) + `f_suite` |
| Data plane (1280 B MTU) | 2230 MiB/s | 517 MiB/s (GFNI+AVX2) | ~4.3× (HW SM4 engine can close) |
| Agility dispatch cost | — | < 1 μs | Atomic load + `match` |

---

##  License

GPL v3 — see each version's source headers.

---

##  Citation

If you use this code in your research, please cite:

```bibtex
@article{chen2025smpqwireguard,
  title   = {A Hybrid Post-Quantum WireGuard with Cryptographic Agility:
             Instantiation with the SM Suite and Flexible KEM Switching},
  author  = {Xiaochuan Chen and Yifan Zheng and Taolong Su and Feng Zhang and Zhe Liu},
  journal = {Science China Information Sciences},
  year    = {2026}
}
```
