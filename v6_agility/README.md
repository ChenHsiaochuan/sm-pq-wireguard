# v6 — 抗量子密码敏捷性（Crypto Agility）版

> 本目录在 v5（SM2 + SM3 + SM4-GCM/GFNI 数据平面加速 + ML-KEM/McEliece 混合后量子
> WireGuard）基础上，实现**抗量子 KEM 敏捷性**：可在运行时通过**单一外部接口**自由
> 切换用于密钥封装的后量子算法，无需重编译、无需中断正在运行的系统。
>
> - **敏捷的维度**：每次会话的**临时 KEM**（默认 ML-KEM-512 = FIPS 203）；静态身份
>   KEM（Classic McEliece）作为锚点固定。
> - **单一外部接口**：环境变量 `WG_KEM_SUITE`（启动期）+ 程序化 `set_active_suite_*`
>   API（运行期活体切换，不影响已建立的会话）。
> - **逐握手协商**：每条 InitHello/RespHello 携带 1 字节套件标识 `f_suite`。
> - **已登记 6 个 KEM、跨 3 个家族**：ML-KEM-512/768/1024（FIPS 203）、Kyber-512
>   （round 3）、HQC-128（编码）、FrodoKEM-640-AES（LWE）。
>
> **关于 FIPS 203/204/205/206**：只有 **FIPS 203（ML-KEM）是 KEM**；FIPS 204/205/206
> 是数字签名标准，**不能做密钥封装**，因此 KEM 敏捷性是在多个 KEM 之间切换，而非替换
> 为 204/205/206。详见 [`AGILITY.md`](AGILITY.md)。
>
> v5 的 GFNI+AVX2 SM4-GCM 数据平面加速（见 [`OPTIMIZATION.md`](OPTIMIZATION.md)）原样
> 继承——敏捷性只触及握手控制平面。
>
> 复现：
> ```bash
> cd artifacts_implementation
> cargo test  --release --features hybrid                          # 正确性（62 passed）
> cargo run   --release --features hybrid -- -b 10                 # 逐套件握手基准（敏捷性演示）
> WG_KEM_SUITE=hqc-128 cargo run --release --features hybrid -- -b 5  # 经外部接口切换 KEM
> ```
> 核心代码：
> [`artifacts_implementation/src/wireguard_hybrid/handshake/agility.rs`](artifacts_implementation/src/wireguard_hybrid/handshake/agility.rs)。

---

# Artifacts for Usenix'25 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"

This repository contains all required software to reproduce results from paper "A Tale of Two Worlds, a Story of WireGuard Hybridization".

## Licence

GNU General Public License v3[^0].


## Architecture

Folder *artifacts_evaluation* concerns the symbolic evaluation of WireGuard (with fix for anonymity based on psk), PQ-WireGuard, PQ-WireGuard⋆ and Hybrid-WireGuard with the help of SAPIC+, ProVerif, Tamarin and DeepSec. The second folder *artifacts_implementation* concerns the Rust implementation of WireGuard, PQ-WireGuard⋆ and Hybrid-WireGuard. Each folder contains a README.md file that explains how to install all the dependencies (SAPIC+, ProVerif, Tamarin, DeepSec used for symbolic evaluation, Python package sympy used for the CNF computations on the one hand, and Rust on the other hand). Our target is to ensure reproducibility of our results on a fresh Ubuntu Server 24.04.2 LTS.

## References

[^0]: https://www.gnu.org/licenses/gpl-3.0.html