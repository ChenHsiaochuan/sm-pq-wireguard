# v5 — GFNI/AVX2 国密 SM4-GCM 数据平面加速版

> 本目录在 v4（SM2 + SM3 + SM4-GCM + 后量子混合 WireGuard）基础上，依据国密性能优化
> 论文综述对 **SM4-GCM 数据平面**做了硬件加速：用 Intel **GFNI + AVX2** 8 路并行实现
> SM4 S 盒，配合 **CLMUL** GHASH，并将路由收发改为原地（in-place）加解密。
>
> **实测：SM4-GCM 吞吐 96 MB/s → 393 MB/s（约 4×），且与 v4 逐字节兼容、全部测试通过。**
> 详见 [`OPTIMIZATION.md`](OPTIMIZATION.md)。核心代码：
> [`artifacts_implementation/src/wireguard_hybrid/sm_crypto/`](artifacts_implementation/src/wireguard_hybrid/sm_crypto/)。
>
> 复现：
> ```bash
> cd artifacts_implementation
> cargo test  --release --features hybrid                                            # 正确性（全绿）
> cargo test  --release --features hybrid -- --ignored --nocapture sm4_gcm_throughput # 吞吐对比
> cargo run   --release --features hybrid -- -b 5                                      # 端到端握手基准
> ```

---

# Artifacts for Usenix'25 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"

This repository contains all required software to reproduce results from paper "A Tale of Two Worlds, a Story of WireGuard Hybridization".

## Licence

GNU General Public License v3[^0].


## Architecture

Folder *artifacts_evaluation* concerns the symbolic evaluation of WireGuard (with fix for anonymity based on psk), PQ-WireGuard, PQ-WireGuard⋆ and Hybrid-WireGuard with the help of SAPIC+, ProVerif, Tamarin and DeepSec. The second folder *artifacts_implementation* concerns the Rust implementation of WireGuard, PQ-WireGuard⋆ and Hybrid-WireGuard. Each folder contains a README.md file that explains how to install all the dependencies (SAPIC+, ProVerif, Tamarin, DeepSec used for symbolic evaluation, Python package sympy used for the CNF computations on the one hand, and Rust on the other hand). Our target is to ensure reproducibility of our results on a fresh Ubuntu Server 24.04.2 LTS.

## References

[^0]: https://www.gnu.org/licenses/gpl-3.0.html