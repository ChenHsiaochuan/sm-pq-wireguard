# End-to-End Network Experiment Artifact

Harness for exercising the SM-PQ-WireGuard v6 handshake — including the
oversized HQC/FrodoKEM messages and the fragmentation/reassembly path — over a
real UDP/TUN datapath under MTU, loss, and reordering conditions.

## What is measured here vs. what needs a root host

This artifact has two layers, kept strictly separate so nothing is overstated:

| Layer | Status on this host | What it shows |
|-------|--------------------|---------------|
| **Handshake microbenchmark** (`--kem-summary`, in-process) | **MEASURED** (300 rounds, real) | Per-suite handshake CPU latency and exact on-wire message sizes. No network. |
| **Full-tunnel netns matrix** (`run_namespace_matrix.sh` + `run_full_tunnel_once.sh`) | **PENDING ROOT HOST** | Real two-namespace UDP/TUN handshake under `tc netem`, success rate + p50/p95/p99. |

The full netns/`tc netem` matrix requires root (`ip netns`, `tc`), which is not
available non-interactively on the build host. The harness is complete and
runnable; the exact reproduce command is below. **Until it is run on a root
host, treat per-cell tunnel success rates and tunnel-path latencies as not yet
measured** — only the microbenchmark numbers below are real here.

## Measured microbenchmark (real)

300 rounds, interleaved suites, 13th-gen Intel i7-13700, static KEM = Classic
McEliece 460896. Raw: [`results/microbench/kem_summary_300.csv`](results/microbench/kem_summary_300.csv);
summary: [`results/microbench/handshake_microbench_summary.csv`](results/microbench/handshake_microbench_summary.csv).

| Suite | Family | Init (ms) | Respond (ms) | Init B | Respond B | Fits 1280-B MTU |
|-------|--------|-----------|--------------|--------|-----------|-----------------|
| ml-kem-512   | ML-KEM   | 0.67 | 1.31 | 1110 | 1018 | **yes** |
| kyber-512    | Kyber    | 0.79 | 1.49 | 1110 | 1018 | **yes** |
| ml-kem-768   | ML-KEM   | 0.77 | 1.43 | 1494 | 1338 | no (fragments) |
| ml-kem-1024  | ML-KEM   | 0.83 | 1.55 | 1878 | 1818 | no (fragments) |
| hqc-128      | HQC (code) | 2.59 | 3.45 | 2559 | 4683 | no (fragments) |
| frodo-640-aes| FrodoKEM (LWE) | 0.87 | 1.49 | 9926 | 9970 | no (fragments) |

Confirms the design claim: only the default ML-KEM-512 and Kyber-512 suites keep
both handshake messages within the IPv6 minimum MTU (1280 B); ML-KEM-768/1024,
HQC-128 (up to 4.6 KiB), and Frodo-640 (≈9.9 KiB) exceed it and rely on IP
fragmentation. Code-based HQC also carries the ≈2 ms extra compute the paper
notes; the other suites are within run-to-run noise of each other.

## Reproduce the full-tunnel matrix (root host)

```bash
cd workspace/v6_agility/artifacts_evaluation/network_experiments
# Provide a hybrid (SM2 + Classic McEliece) keygen helper first; see
# run_full_tunnel_once.sh header for the exact private/public key byte layout.
sudo env \
  SUITES="ml-kem-512 ml-kem-768 ml-kem-1024 kyber-512 hqc-128 frodo-640-aes" \
  MTUS="1280 1420 1500" LOSSES="0 1 3" REORDERS="0 5" ROUNDS="100" \
  OUT="$PWD/results/full_tunnel" \
  SMWG_KEYGEN="$PWD/keygen_hybrid" \
  SMWG_E2E_COMMAND="$PWD/run_full_tunnel_once.sh" \
  ./run_namespace_matrix.sh

python3 summarize_handshakes.py \
  results/full_tunnel/handshake_samples.csv \
  > results/full_tunnel/handshake_summary.csv
```

Without `SMWG_E2E_COMMAND`, `run_namespace_matrix.sh` runs a **fallback smoke
check** (bare-veth ping under the same netem profile). Smoke rows are tagged
`status=smoke` and are explicitly *not* tunnel results.

### Exit-code / status mapping (`run_full_tunnel_once.sh` → matrix)

| Exit | Status | Meaning |
|------|--------|---------|
| 0    | `ok`       | tunnel handshake completed and a packet crossed the protected tunnel; latency printed in ms |
| 124  | `timeout`  | handshake did not complete within `HS_TIMEOUT` (default 10 s) |
| 10   | `loss`     | tunnel up but no reply through it (fragmentation/packet loss) |
| 11   | `auth_fail`| configuration/auth failure (incl. missing `SMWG_KEYGEN` helper) |
| other| `crash`    | a peer process died |

The one deployment-specific piece is `SMWG_KEYGEN`: the v6 binary ships no
`genkey` subcommand, so the wrapper expects a helper that prints
`<private_key_hex> <public_key_hex>` in the documented layout
(`private_key = SM2_secret[32] ‖ McE_secret[13608] ‖ McE_public[524160]`;
`public_key = SM2_point[33] ‖ McE_public[524160]`, Classic McEliece 460896).
If it is absent the wrapper exits 11 so the matrix records the gap honestly
rather than fabricating a success.

## Files

- `run_namespace_matrix.sh` — netns + `tc netem` sweep; real-tunnel or smoke mode
- `run_full_tunnel_once.sh` — reference `$SMWG_E2E_COMMAND`; drives the binary via UAPI
- `summarize_handshakes.py` — `handshake_samples.csv` → success-rate + p50/p95/p99
- `results/environment.txt` — host/toolchain fingerprint
- `results/microbench/` — measured handshake microbenchmark (real)
- `results/full_tunnel/` — populated by the matrix run on a root host
