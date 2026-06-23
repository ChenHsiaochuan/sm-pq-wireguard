# SM2 + ML-KEM 混合后量子 WireGuard 实施汇报

**项目**：USENIX'25 混合后量子 WireGuard 国密化改造
**目标**：将原协议中的 X25519 ECDH 替换为国密 SM2，构建 SM2 + ML-KEM-512 + Classic-McEliece-460896 + PSK 的四重混合握手
**日期**：2026-04

---

## 一、研究背景与目标

### 1.1 背景

USENIX 2025 论文 *"Hybridizing WireGuard"* 提出了一种后量子安全的 WireGuard 变体，使用 **X25519 + ML-KEM-512 + Classic-McEliece-460896** 的混合握手机制：即便量子计算机攻破了经典椭圆曲线密码，会话密钥仍受后量子 KEM 保护。

### 1.2 国密替换动机

X25519 是西方主导的椭圆曲线标准，在国内合规场景（金融、政务、关基）中需替换为国密 SM2（GB/T 32918）。本工作目标：

- **保留**原项目的混合后量子安全性
- **替换**经典 ECDH 部分为 SM2
- **保留**原项目的两个对照模块（`wireguard/`、`wireguard_pq_star/`），便于性能与安全对比

### 1.3 最终目标

实现 **SM2 + ML-KEM-512 + Classic-McEliece-460896 + PSK** 的四重混合握手协议原型，并通过完整的端到端测试。

---

## 二、技术方案与挑战识别

### 2.1 SM2 与 X25519 的关键差异

| 维度 | X25519 | SM2 | 工程影响 |
|------|--------|-----|---------|
| 曲线类型 | Montgomery | Weierstrass | API 不同 |
| 公钥编码 | 32 字节裸字节 | 33 字节 SEC1 压缩 | **消息格式 +1 字节** |
| 私钥构造 | 任意 32B 字节均合法 | 必须为有效标量 | 测试不能用硬编码字节 |
| DH 输出 | 32B | 32B（x 坐标） | 不变 |
| Rust 库 | `x25519_dalek` | `sm2` + `elliptic-curve` | 依赖重组 |
| RNG 版本 | rand_core 0.5 | rand_core 0.6 | **版本冲突需绕过** |

### 2.2 三个潜在踩坑点（提前识别）

1. **公钥长度变化**：32B → 33B 影响所有缓冲区拼接 → 拆分常量为 `SIZE_SM2_POINT=33` 与 `SIZE_DH_SHARED_SECRET=32`
2. **测试硬编码失效**：原 X25519 测试用固定字节作密钥，SM2 不允许 → 改用 `random()` 随机生成
3. **RNG 版本冲突**：项目用 rand_core 0.5，SM2 需 0.6 → 编写辅助函数 `random_sm2_sk` 用 `fill_bytes + from_slice` 桥接

---

## 三、实施方法论：分层定位 + 增量验证

### 3.1 全局影响面分析

通过 `grep -rn "x25519_dalek\|StaticSecret\|PublicKey" src/` 全局扫描，定位所有 X25519 引用点，按调用层次分组：

| 层次 | 文件数 | 角色 |
|------|--------|------|
| 密码参数 | 1 | 常量、宏定义 |
| 协议核心 | 1 | 握手 DH 计算（最复杂） |
| 消息格式 | 1 | 公钥字节大小 |
| 设备状态 | 2 | KeyState、Peer 结构体 |
| WG 包装层 | 4 | 类型透传 |
| 配置接口 | 3 | UAPI 序列化 |
| 测试与基准 | 3 | 密钥生成更新 |
| 依赖 | 1 | Cargo.toml |
| **总计** | **16** | |

### 3.2 自底向上分层改造

#### 阶段 1：依赖与常量（地基）
- `Cargo.toml`：新增 `sm2 = "0.13"` + `elliptic-curve = { features = ["ecdh"] }`
- `crypto_params.rs`：新增 `SIZE_SM2_POINT`、`SIZE_DH_SHARED_SECRET`，更新协议标识符为 `Noise_IKpsk2_SM2_ChaChaPoly_BLAKE2s`

#### 阶段 2：密码核心（noise.rs）
- 替换 import：`use x25519_dalek::*` → `use sm2::*`
- 新增 4 个辅助函数：
  - `pk_to_bytes`：SM2 PublicKey → 33B SEC1 压缩
  - `pk_from_bytes`：33B → SM2 PublicKey
  - `shared_secret`：SM2 ECDH 调用 + 零点检查
  - `random_sm2_sk`：绕过 rand_core 版本差异
- 按上下文分别替换原 `SIZE_X25519_POINT`：
  - 公钥拼接 → `SIZE_SM2_POINT`（4 处）
  - DH 输出拼接 → `SIZE_DH_SHARED_SECRET`（8 处）

#### 阶段 3：状态结构（device.rs / peer.rs）
- `KeyState.sk` 与 `KeyState.pk` 类型替换
- `update_ss()` 改用 `diffie_hellman(sk.to_nonzero_scalar(), peer.pk.as_affine())`
- `Peer.pk`、`State::InitiationSent.eph_sk` 类型替换

#### 阶段 4：包装层（wireguard.rs / peer.rs / timers.rs / workers.rs）
纯类型透传，机械替换。

#### 阶段 5：配置接口（config.rs / uapi/get.rs / uapi/set.rs）
- `Configuration` trait 签名更新
- `set.rs`：解析 hex 时使用新的 33B + KEM 长度
- `get.rs`：序列化 SM2 公钥用 `to_encoded_point(true).as_bytes()`

#### 阶段 6：测试与基准
- 硬编码字节密钥 → `DhSecretKey::random(&mut OsRng08)`
- 引入 `rand_oqs::rngs::OsRng as OsRng08` 作为 SM2 用 RNG（绕过版本不匹配）

### 3.3 编译器引导的迭代式调试

每完成一个阶段就运行 `cargo build`，让编译器报错指引下一处修改。该循环跑了约 4 轮：

| 轮次 | 主要错误 | 解决方案 |
|------|---------|---------|
| 1 | `sm2` 没有 `ecdh` feature | 直接依赖 `elliptic-curve` 启用 ecdh |
| 2 | `crypto_params.rs` 宏重复定义（历史残留） | 删除重复块 |
| 3 | `raw_secret_bytes().into()` 类型推断失败 | 加 `(*ref).into()` 解引用 |
| 4 | `rand_core` 版本冲突 | 引入 `rand_oqs::rngs::OsRng` + `random_sm2_sk` 辅助 |

**这种"让编译器引导"的方式比一次性手工梳理高效得多**——Rust 强类型系统几乎不会漏改一处。

---

## 四、密钥交换协议详解

### 4.1 混合方式：交替拼接 + 串行 KDF 混入 chain key

**不是**两次独立握手，**也不是**最终大拼接，而是**双轨并行 + 每步混入链式密钥派生**。

### 4.2 三段 KEM + 三次 DH 的组合

| 类型 | 公式 | 用途 |
|------|------|------|
| DH1 | SM2 ECDH(eph_I, static_R) | 临时-静态 DH |
| DH2 | SM2 ECDH(eph_I, eph_R) | 临时-临时 DH（前向安全） |
| DH3 | SM2 ECDH(static_I, static_R) | 静态-静态 DH（身份认证） |
| KEM1 | McEliece 静态封装 → shk1 | 静态 PQ 认证 |
| KEM2 | ML-KEM 临时封装 → shk2 | 临时 PQ 前向安全 |
| KEM3 | McEliece 静态封装 → shk3 | 加强静态 PQ 认证 |
| PSK | 32 字节预共享 | 额外量子保险 |

### 4.3 Chain Key 演进流程

```
C₀ = HASH("Noise_IKpsk2_SM2_ChaChaPoly_BLAKE2s")
C₁ = KDF1(C₀, eph_I_pub ‖ eph_I_pq_pub)
C₂ = KDF2(C₁, DH1 ‖ shk1).ck                ← 第1次混合：SM2 + McEliece
C₃ = KDF2(C₂, DH3 ‖ HASH(spk_pq) ‖ psk).ck   ← 第2次混合：SM2 静态 + PQ绑定 + PSK
C₄ = KDF1(C₃, eph_R_pub ‖ eph_R_ct_pq)
C₅ = KDF1(C₄, DH2 ‖ shk2)                    ← 第3次混合：SM2 临时 + ML-KEM
C₆ = KDF1(C₅, DH1' ‖ shk3)                   ← 第4次混合：SM2 + McEliece
C₇ = KDF3(C₆, PSK).ck                        ← PSK 二次混入

(K_recv, K_send) = KDF2(C₇, ∅)
```

### 4.4 安全性保证

最终会话密钥的熵 ≥ max(经典秘密, PQ 秘密, PSK)：

- 量子攻破 SM2，但 ML-KEM/McEliece 未破 → **密钥仍安全**
- 经典攻破 ML-KEM/McEliece，但 SM2 未破 → **密钥仍安全**
- 两者都破，但 PSK 未泄露 → **密钥仍安全**

**特别设计**：McEliece 密文用 DH1 派生的 ChaCha20 密钥包裹后才传输——攻击者要拿 PQ 握手材料，必先攻破 SM2。

---

## 五、验证与结果

### 5.1 三级验证

| 级别 | 命令 | 目的 | 结果 |
|------|------|------|------|
| 编译 | `cargo build` | 类型与依赖正确 | **0 错误** |
| 单元 | `cargo test wireguard_hybrid` | 协议逻辑正确 | **16/16 通过** |
| 集成 | `cargo run -- -b 5` | 端到端握手 | **完整通过** |

### 5.2 关键测试用例

| 测试 | 覆盖内容 |
|------|---------|
| `handshake_no_load` | 10 次完整握手，验证双方派生同一会话密钥 |
| `handshake_under_load` | 7 步带 Cookie 的握手，验证 DoS 保护 |
| `unique_shared_secrets` | SM2 静态共享秘密各对独立 |
| `test_pure_wireguard` | 虚拟 TUN+UDP，端到端 40 个加密 IP 包逐字节校验 |
| `precomputed_chain_key/hash` | 协议初始常量计算正确性 |
| `test_cookie_reply` | DoS Cookie 加解密 |

### 5.3 性能基准

```
Hybrid-WireGuard (SM2 + ML-KEM-512 + McEliece-460896):
  InitHello message size:    1157 bytes  (原版 X25519: 1156 B，+1 B)
  RespHello message size:    1065 bytes  (原版 X25519: 1064 B，+1 B)
  InitHello construction:    0.291 ms (std = 0.019 ms)
  RespHello processing:      27.859 ms (std = 0.709 ms)
```

**结论**：消息体积仅增 1 字节（公钥 32→33B），握手延迟与原版 ML-KEM 混合版本可比，性能开销可忽略。

---

## 六、工程交付与改动规模

### 6.1 改动规模

- **修改文件**：16 个 Rust 源文件
- **新增依赖**：2 个 crate（`sm2` + `elliptic-curve`）
- **零侵入对照模块**：`wireguard/`、`wireguard_pq_star/` 保持原样，可直接对比
- **新增文档**：`CHANGES_SM2.md` 详细记录全部 16 处改动

### 6.2 文件清单

| 类别 | 文件 |
|------|------|
| 依赖 | `Cargo.toml` |
| 密码参数 | `wireguard_hybrid/handshake/crypto_params.rs` |
| 协议核心 | `wireguard_hybrid/handshake/noise.rs` |
| 消息格式 | `wireguard_hybrid/handshake/messages.rs` |
| 设备状态 | `wireguard_hybrid/handshake/device.rs`, `peer.rs` |
| WG 包装层 | `wireguard_hybrid/wireguard.rs`, `peer.rs`, `timers.rs`, `workers.rs` |
| 配置接口 | `configuration_hybrid/config.rs`, `uapi/get.rs`, `uapi/set.rs` |
| 测试 | `wireguard_hybrid/tests.rs`, `handshake/tests.rs`, `handshake/macs.rs`, `device.rs` (内嵌测试) |
| 基准 | `wireguard_hybrid/benchs.rs` |

---

## 七、研究价值与后续工作

### 7.1 研究价值

1. **完整可复现**的国密版混合后量子 VPN 原型
2. **方法论可迁移**：本工作的"分层定位 + 编译器引导"方法可复用于其他国密化改造
3. **基线作用**：为后续国密 + 后量子组合密码协议研究提供对比基准

### 7.2 后续可拓展方向

- 替换 ML-KEM 为国密 PQC 候选（如格基算法的国密版本）
- 加入 SM3 哈希（替换 Blake2s）、SM4 加密（替换 ChaCha20-Poly1305），实现"全国密 + 后量子"协议
- 在真实 Linux TUN 设备上做端到端吞吐与时延测试
- 形式化验证混合协议在符号模型下的安全性

---

## 八、汇报核心要点（一页版）

**做了什么**
将 USENIX'25 混合后量子 WireGuard 的经典曲线 X25519 替换为国密 SM2，形成 SM2 + ML-KEM + McEliece + PSK 四重混合握手协议。

**怎么做的**
分层定位影响面（16 个文件），按"依赖→密码核心→状态→接口→测试"自底向上改造，借助 Rust 编译器迭代调试。

**遇到了什么**
- SM2 与 X25519 公钥长度不同（33 vs 32 字节）→ 拆分常量
- rand_core 版本不兼容 → 编写桥接辅助函数
- SM2 私钥不能用硬编码字节 → 测试改用随机生成

**结果如何**
- 16 项单元测试全部通过
- 端到端握手延迟 ~28ms，消息体积仅增 1 字节
- 安全性：经典 SM2 / 后量子 KEM / PSK 任一不破即会话密钥安全
- 完整修改文档 `CHANGES_SM2.md` 与本汇报已交付
