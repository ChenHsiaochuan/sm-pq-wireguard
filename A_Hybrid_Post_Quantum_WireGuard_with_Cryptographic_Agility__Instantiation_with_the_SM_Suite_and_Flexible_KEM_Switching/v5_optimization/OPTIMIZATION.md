# v5 性能优化：GFNI + AVX2 国密 SM4-GCM 数据平面加速

本版本（v5）在 v4（SM2 + SM3 + SM4-GCM + McEliece/ML-KEM 混合后量子 WireGuard）
基础上，依据《国密算法 SM2/SM3/SM4 性能优化论文综述》中**阶段二（数据平面核心贡献）**
的结论，对 SM4-GCM 数据平面进行了硬件加速优化。

所有改动仅限 `workspace/v5_optimization/`，与 v4 完全隔离，便于对比与回退。

---

## 1. 优化目标与论文映射

综述将 SM4-GCM 数据平面列为最高优先级优化项。v4 的实测瓶颈来自外部 `sm4-gcm 0.1.2`
crate：

| 组件 | v4 实现 | 问题 |
|------|---------|------|
| SM4 分组加密 | `sm4 0.5`（RustCrypto 纯软件查表/字操作，逐块） | 无 SIMD，单块串行 |
| GHASH | `ghash` crate（已含 CLMUL，但每包 `new`/`update_padded` 有拷贝开销） | — |
| 调用方式 | 每包 `Vec` 分配 + 拷回 | 堆分配抖动 |

对应综述论文：

- **Weiji Guo, ePrint 2022/1154** — *Efficient Constant-Time Implementation of SM4 with
  Intel GFNI*：用 `vgf2p8affineqb` + `vgf2p8affineinvqb` 一对指令计算 SM4 S 盒，
  AVX2 下达 2.62 cpb。**→ 本版本 SM4 核心。**
- **mjosaarinen/sm4ni** & **scnucrypto/OptimizedSM4** — SM4 S 盒与 AES 域求逆仿射同构。
  **→ GFNI 仿射常数的理论依据。**
- **Intel CLMUL 白皮书 (Gueron & Kounavis)** — PCLMULQDQ 实现 GHASH。
  **→ 经由 CLMUL 后端的 `ghash` crate 实现（运行时检测 PCLMULQDQ）。**

目标硬件：Intel i7-13700（Raptor Lake），支持 `gfni / avx2 / vaes / pclmulqdq /
vpclmulqdq`（无 AVX-512）。

---

## 2. 实现概述

新增内建模块 `src/wireguard_hybrid/sm_crypto/`（不再依赖外部 `sm4-gcm`/`sm4`/`ctr`
crate 于热路径）：

```
sm_crypto/
├── mod.rs    # 公开 API（drop-in 兼容 sm4-gcm crate）
├── sm4.rs    # SM4：GFNI+AVX2 8 路并行 + 可移植标量回退
└── gcm.rs    # SM4-GCM（CLMUL GHASH）+ in-place 热路径 + SM4-CTR
```

### 2.1 SM4 S 盒 = 一对 GFNI 仿射指令（`sm4.rs`）

SM4 的 8-bit S 盒与 AES 的 S 盒同样基于 GF(2⁸) 求逆，二者仿射同构。GFNI 指令
`GF2P8AFFINEINVQB` 在 **AES 多项式 0x11B** 下完成「求逆 + 仿射」。因此：

```
tau(x) = GF2P8AFFINEINV( GF2P8AFFINE(x, M1, C1), M2, C2 )
```

其中（已对全部 256 个输入**穷举验证**与官方 SM4 S 盒逐字节一致）：

```
M1 lane = 0xa7ac65de3de94796   C1 = 0x69
M2 lane = 0x75f1228d6c1e85c9   C2 = 0xd3
```

每轮 32 字节（8 个分组的同一字）只需两条 GFNI 指令即可完成 4×8 个 S 盒查表；
线性变换 L 用 `vpslld/vpsrld/vpxor` 的循环移位实现。

**8 路并行**：将 8 个分组转置为「按字」布局（`cols[j]` = 8 个分组的第 j 字），
32 轮全程在 256-bit 寄存器上 SIMD 运算，再转置写回。
（`encrypt8_gfni`，`#[target_feature(enable="avx2,gfni")]`）

**回退**：无 GFNI/AVX2 的 CPU（或非 x86）自动走标量 `encrypt_block`
（同一份代码用于密钥扩展、H=E(0)、E(J0)、CTR 尾块）。运行时检测结果缓存于原子变量。

### 2.2 SM4-GCM（`gcm.rs`）

- 构造严格遵循 NIST SP 800-38D，**与被替换的 `sm4-gcm` crate 逐字节一致**
  （H = SM4ₖ(0)；12 字节 nonce 时 J0 = nonce‖0x00000001；
  tag = GHASHₕ(AAD‖C‖len) ⊕ SM4ₖ(J0)）。
- GHASH 复用 CLMUL 加速的 `ghash` crate（实测 GHASH-only 1364 MB/s，证实走的是
  PCLMULQDQ 硬件后端，而非软件回退）。
- **In-place 热路径**：`sm4_gcm_encrypt_inplace` / `sm4_gcm_decrypt_inplace`
  直接在报文缓冲区内原地加解密并写 tag，消除每包 `Vec` 分配与拷回。
  路由层 `router/send.rs`、`router/receive.rs` 已改用 in-place 接口。
- 解密 tag 校验使用 `subtle::ConstantTimeEq` 常数时间比较（原 crate 用 `!=`，非常数时间）。

### 2.3 SM4-CTR（握手 KEM 流加密）

`sm4_ctr128be_apply` 用同一 GFNI 核心实现 `Ctr128BE`，替换 `noise.rs` 中
`ctr::Ctr128BE<sm4::Sm4>`，用于包裹静态 KEM 密文流。

---

## 3. 改动文件清单

| 文件 | 改动 |
|------|------|
| `src/wireguard_hybrid/sm_crypto/{mod,sm4,gcm}.rs` | **新增**：GFNI SM4 + CLMUL GCM |
| `src/wireguard_hybrid/mod.rs` | 注册 `sm_crypto` 模块 |
| `src/wireguard_hybrid/router/send.rs` | 改用 `sm4_gcm_encrypt_inplace`（原地，零分配） |
| `src/wireguard_hybrid/router/receive.rs` | 改用 `sm4_gcm_decrypt_inplace` |
| `src/wireguard_hybrid/handshake/noise.rs` | SEAL/OPEN + CTR 改用内建模块 |
| `src/wireguard_hybrid/handshake/crypto_params.rs` | XSEAL/XOPEN 改用内建模块 |
| `Cargo.toml` | 新增 `ghash = "0.5"` 直接依赖 |

握手协议字符串 `Noise_IKpsk2_SM2_SM4GCM_SM3`、报文格式、KDF 等**完全不变**，
因此 v4 与 v5 节点可互通（AEAD 输出逐字节一致）。

---

## 4. 实测结果（i7-13700）

SM4-GCM 加密 1420 B 报文 × 50000 次：

| 实现 | 吞吐 | 相对基线 |
|------|------|----------|
| v4：`sm4-gcm` crate（标量 SM4） | **96 MB/s** | 1.00× |
| v5：内建 GFNI+AVX2（分配版本） | **383 MB/s** | **3.97×** |
| v5：内建 GFNI+AVX2（in-place 热路径） | **393 MB/s** | **4.07×** |

诊断数据：原始 SM4-CTR keystream（含密钥扩展）615 MB/s；GHASH-only 1364 MB/s
（确认 CLMUL 硬件后端生效）。

复现：
```bash
cd artifacts_implementation
cargo test --release --features hybrid -- --ignored --nocapture sm4_gcm_throughput
```

---

## 5. 正确性验证

`cargo test --release --features hybrid` 全部通过（54 单测 + sm_crypto 专项）：

- **SM4 官方测试向量**（GB/T 32907-2016）标量路径 KAT。
- **GFNI 8 路 ⟷ 标量** 逐分组一致；GFNI lane-0 复现官方向量。
- **BouncyCastle SM4-GCM 测试向量**（与原 `sm4-gcm` crate 同一组）——
  证明与被替换实现**逐字节兼容**。
- **in-place ⟷ 分配版本** 在 0/1/15/16/17/127/128/129/1420 B 各长度逐字节一致，
  且 in-place 解密往返还原。
- 篡改 tag 被拒；CTR 往返（跨多个 8-块组 + 尾块）正确。
- 完整混合握手 + 路由收发单测全绿；`-b` 端到端基准正常运行，报文尺寸与 v4 一致。

---

## 6. 未纳入的优化（理由）

- **SM3 SIMD（消息扩展 AVX2）**：综述指出 SM3 仅用于握手 KDF/HMAC（32–64 B 输入），
  数据平面不使用 SM3，AVX2 并行无可测收益，故未实现（高成本、零收益）。属综述阶段四范畴。
- **SM2 握手加速（广义梅森模约减 / 固定基 comb）**：需 fork `sm2` crate 的有限域后端
  或 FFI 至铜锁/Tongsuo，工程量大且独立，属综述**阶段三**，本版本聚焦阶段二数据平面。
- **进一步提升 SM4-GCM 吞吐至 GB/s**：需按会话缓存 SM4 轮密钥与 H（避免每包密钥扩展）、
  SIMD 转置、自研 VPCLMULQDQ GHASH 聚合约减。这些需改动 `KeyPair` 结构，风险较高，
  列为后续工作；当前 4× 已在保持 drop-in 兼容与全部测试通过的前提下达成。

---

## 7. 参考文献

1. Weiji Guo. *Efficient Constant-Time Implementation of SM4 with Intel GFNI and Arm NEON.*
   IACR ePrint 2022/1154.
2. M.-J. Saarinen. *sm4ni: AES-NI Instructions Can Implement SM4.* 2018.
3. scnucrypto/OptimizedSM4（华南师范大学密码团队），密码学报。
4. S. Gueron, M. Kounavis. *Intel Carry-Less Multiplication Instruction and its Usage for
   Computing the GCM Mode.* Intel White Paper.
5. GFNI 仿射常数推导：emmansun/gmsm「SM4 with GFNI」。
