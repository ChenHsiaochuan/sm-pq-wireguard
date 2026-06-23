# v6 抗量子密码敏捷性（Crypto Agility）

本版本（v6）在 v5（SM2 + SM3 + SM4-GCM/GFNI 数据平面加速 + ML-KEM/McEliece
混合后量子 WireGuard）基础上，实现**抗量子密码（KEM）敏捷性**：可在运行时通过
**单一外部接口**自由切换用于密钥封装的后量子算法，无需重新编译、无需中断正在运行的
系统。

所有改动仅限 `workspace/v6_agility/`，与 v5 完全隔离，便于对比与回退。

> **敏捷性定义（采用本工程的设计目标）**
> *"Crypto agility describes the capabilities needed to replace and adapt
> cryptographic algorithms for protocols, applications, software, hardware, and
> infrastructures **without interrupting the flow of a running system** to
> achieve resiliency."*

---

## 0. 先澄清一个关键问题：FIPS 203 / 204 / 205 / 206

工程当前用于**临时密钥封装**的算法是 **FIPS 203（ML-KEM，旧称 Kyber）**，参数为
ML-KEM-512（NIST 安全等级 1）。这与 v5 完全一致。

| 标准 | 算法 | 类型 | 能否做密钥封装(KEM)？ |
|------|------|------|----------------------|
| **FIPS 203** | ML-KEM (Kyber) | **KEM** | ✅ 能 |
| FIPS 204 | ML-DSA (Dilithium) | 数字签名 | ❌ 不能 |
| FIPS 205 | SLH-DSA (SPHINCS+) | 数字签名 | ❌ 不能 |
| FIPS 206（草案） | FN-DSA (Falcon) | 数字签名 | ❌ 不能 |

**FIPS 204/205/206 是数字签名标准，不能用于密钥封装**，因此不能作为 KEM 的"替换
算法"。密钥封装层面的敏捷性，正确含义是在**多个 KEM**之间切换：

- 整个 **FIPS 203 家族**：ML-KEM-512 / 768 / 1024（NIST 等级 1/3/5）；
- 其他 NIST KEM 家族：**HQC**（基于编码，2025 备份选择）、**FrodoKEM**（保守
  LWE）、以及旧称 **Kyber**（round-3，用于"从预标准迁移到 FIPS 203"演示）。

v6 的敏捷注册表正是登记了上述这些 KEM。（若未来要把签名算法也做成敏捷的，那属于
"认证敏捷性"，是另一条正交的维度，可在静态身份层引入 ML-DSA/SLH-DSA 混合签名，
不在本版本范围内。）

---

## 1. 敏捷的是哪一个 KEM？

握手用到**两个** KEM：

| 角色 | 算法 | 绑定对象 | 是否敏捷 |
|------|------|----------|----------|
| **静态 KEM（身份锚）** | Classic McEliece-460896 | 每个对端的长期身份密钥 | ❌ 固定 |
| **临时 KEM（每次会话）** | ML-KEM-512（默认） | 每次握手新生成、前向安全 | ✅ **运行时敏捷** |

- **静态 KEM** 与长期身份绑定，更换它意味着带外重签发身份密钥，属于"部署期锚点"，
  不适合做"每次通信"的开关，因此 v6 保持固定。
- **临时 KEM** 是每次握手新鲜生成的、提供前向安全的那一把封装——这才是"敏捷性"
  真正有意义、且"按每次通信选择"成立的维度。v6 让**它**敏捷。

这样既满足了"自由切换不同抗量子算法做密钥封装、仅通过一个外部接口决定每次通信用哪
个协议"的要求，又不破坏混合后量子的双 KEM 安全框架。

---

## 2. 单一外部接口

选择当前临时 KEM 套件的唯一逻辑接口是进程级的 `ACTIVE_SUITE_ID`（一个原子量），
有两种使用方式：

1. **启动期（运维接口）**——环境变量 `WG_KEM_SUITE`：
   ```bash
   WG_KEM_SUITE=ml-kem-768   ./wireguard-rs-pq wg0     # 启动即生效
   WG_KEM_SUITE=hqc-128      ./wireguard-rs-pq wg0
   ```
   非法值会回退到默认并打印告警，不会崩溃。

2. **运行期（活体切换，不中断系统）**——程序化 API：
   ```rust
   use wireguard_hybrid::handshake::agility;
   agility::set_active_suite_by_name("frodo-640-aes")?;  // 之后的新握手立即采用
   agility::set_active_suite_id(0x03)?;                  // 等价：按 on-wire id 选
   let cur = agility::active_suite();                    // 查询当前
   ```
   切换只影响**之后发起的新握手**；已经建立的会话继续使用其原有密钥——这正是
   "without interrupting the flow of a running system"。

每条 InitHello / RespHello 在线缆上携带一个字节的**套件标识 `f_suite`**，因此是
**逐握手协商**：发起方盖上自己选的套件，响应方就用这个套件解封装。

---

## 3. 注册表与可扩展性

`src/wireguard_hybrid/handshake/agility.rs` 中的 `REGISTRY`：

| on-wire id | token | 算法 | 家族 | NIST 等级 | 共享密钥长度 |
|-----------|-------|------|------|----------|------|
| 0x01 | `ml-kem-512`    | ML-KEM-512 (FIPS 203)   | 格 (MLWE) | 1 | 32 B |
| 0x02 | `ml-kem-768`    | ML-KEM-768 (FIPS 203)   | 格 (MLWE) | 3 | 32 B |
| 0x03 | `ml-kem-1024`   | ML-KEM-1024 (FIPS 203)  | 格 (MLWE) | 5 | 32 B |
| 0x11 | `kyber-512`     | Kyber-512 (round 3)     | 格 (MLWE) | 1 | 32 B |
| 0x21 | `hqc-128`       | HQC-128                 | **编码** | 1 | **64 B** |
| 0x31 | `frodo-640-aes` | FrodoKEM-640-AES        | **LWE** | 1 | **16 B** |

**新增一个 KEM 只需在 `REGISTRY` 追加一行**（必要时调大 `MAX_*` 上界），其余代码
全部无需改动——这正是敏捷框架的价值。`validate_registry()` 在启动时核对每个已启用
套件的 liboqs 实际尺寸不超过 `MAX_*` 编译期上界；`available_suites()` 过滤出当前
liboqs 真正编译进来的算法（用 `OQS_KEM_alg_is_enabled`），不可用的自动跳过。

> 注：三个家族、三种不同的共享密钥长度（32/64/16 字节）并存，证明框架对算法家族
> 与密钥长度都是**完全无关（agnostic）**的。

---

## 4. 线缆格式：从"定长结构体"到"套件感知的紧凑序列化"

v1–v5 的握手消息是 `#[repr(packed)]` 定长结构体 + zerocopy 解析，KEM 字段写死为
单一算法的长度。要敏捷，就必须允许临时 KEM 字段变长。v6 的做法：

- 内存中 `NoiseInitiation` / `NoiseResponse` 为临时 KEM 字段保留 **MAX 上界**大小的
  缓冲区，使**一个结构体类型能容纳任意套件**；
- 但**只把当前套件实际需要的前缀**序列化到线缆上（`serialize()`），因此小套件
  （如 ML-KEM-512）的报文依旧紧凑，不为大套件付费；
- 解析时先读 `f_suite`，据此查 liboqs 得到该套件各字段精确长度，再做**精确长度
  校验**地切分（`parse()`，长度不符即 `InvalidMessageFormat`）；
- 32 字节 mac1‖mac2 始终是报文尾部，`split_macs()` 先剥离它再解析 noise 体。

变长的临时 KEM **共享密钥**（HQC 64B、ML-KEM 32B、Frodo 16B）在 KDF 混入时按实际
长度拼接（用 `Vec` 而非定长数组），双方因 `f_suite` 一致而拼接出逐字节相同的 KDF
输入。

**新增字段**：InitHello / RespHello 各多 1 字节 `f_suite`。
**静态 KEM 密文**字段（McEliece，156B）与 SM4-CTR 包裹方式保持不变。

### 各套件实测报文尺寸（i7-13700，本机复现）

```
ephemeral KEM    InitHello RespHello   标准
ml-kem-512            1110      1018    FIPS 203 ML-KEM-512  (NIST L1)
ml-kem-768            1494      1338    FIPS 203 ML-KEM-768  (NIST L3)
ml-kem-1024           1878      1818    FIPS 203 ML-KEM-1024 (NIST L5)
kyber-512             1110      1018    Kyber-512 (round 3, pre-FIPS)
hqc-128               2559      4683    HQC-128 (code-based)
frodo-640-aes         9926      9970    FrodoKEM-640-AES (conservative LWE)
```

报文尺寸随 KEM 真实变化，证明敏捷字段确实是变长的，而非"换了标签的定长缓冲区"。

---

## 5. 协议骨架与安全性

- **Noise 构造串不变**：`Noise_IKpsk2_SM2_SM4GCM_SM3`。敏捷性由 on-wire 套件字节
  协商，不写入协议名，因此 SM2/SM3/SM4 安全框架、4 次 KDF 混入、KEM 链顺序与 v4/v5
  完全相同——保留原论文的全部安全分析。
- **降级抵抗**：
  1. `f_suite` 被 **mac1** 覆盖；本实现 mac1 以 **PSK** 派生密钥（`HASH(LABEL_MAC1,
     psk)`）做 HMAC-SM3，外部攻击者无 PSK 无法伪造 → 篡改套件字节即破坏 mac1。
  2. `f_suite` 还被**显式混入握手转录哈希** `H`（`HASH(H, [suite_id])`，发起/响应
     两侧对称）→ 篡改套件字节会让双方转录不一致，握手直接失败。
  3. 发起方把自己选的套件存入握手状态，响应必须**回显相同套件**，否则按
     `InvalidState` 拒绝。
  三重保证使"静默降级"无法发生。
- **混合保证不变**：临时 KEM ⊕ 静态 McEliece ⊕ SM2 ECDH，任一不破即安全；切换临时
  KEM 不影响 McEliece/SM2 提供的兜底。

---

## 6. 改动文件清单

| 文件 | 改动 |
|------|------|
| `handshake/agility.rs` | **新增**：KEM 套件注册表、运行时选择器、MAX 上界、环境变量接口、尺寸校验 |
| `handshake/messages.rs` | 临时 KEM 字段改为 MAX 缓冲 + `f_suite`；新增套件感知的 `serialize`/`parse`/`split_macs`；CookieReply/Mac footer 不变 |
| `handshake/noise.rs` | 临时 KEM 的 keygen/encap/decap 改为按"活动/线缆套件"运行时实例化；共享密钥变长拼接；套件经状态贯穿到响应；套件字节绑定进转录哈希 |
| `handshake/peer.rs` | `State::InitiationSent` 增加 `suite_id` |
| `handshake/device.rs` | 收发改用紧凑 `serialize`/`parse` + `split_macs` |
| `handshake/types.rs` | 新增 3 个敏捷性错误码 |
| `handshake/mod.rs` | 注册并导出 `agility` |
| `handshake/tests.rs` | 新增 `agility_handshake_every_suite`：逐套件跑完整握手并校验 |
| `wireguard_hybrid/benchs.rs` | 基准改为**逐套件扫描**，打印每个 KEM 的握手时延与报文尺寸 |
| `main.rs` | 启动时 `validate_registry()` + `init_from_env()`，打印当前套件与可用列表 |

v5 的 GFNI+AVX2 SM4-GCM 数据平面加速（见 `OPTIMIZATION.md`）**原样继承**，敏捷性
只触及握手控制平面，不影响数据平面性能。

---

## 7. 正确性验证

```bash
cd artifacts_implementation
cargo test  --release --features hybrid           # 62 passed, 0 failed, 3 ignored
cargo run   --release --features hybrid -- -b 10  # 逐套件握手基准
WG_KEM_SUITE=hqc-128 cargo run --release --features hybrid -- -b 5
```

- `agility::tests`：注册表在 MAX 上界内、id/token 唯一、默认 ML-KEM-512、查表往返。
- `messages::tests`：6 个套件的 Init/Resp 紧凑序列化逐字节往返；拒绝未知套件。
- `handshake::tests::agility_handshake_every_suite`：对**每个可用套件**跑完整
  Init→Resp→确认握手，断言双端传输密钥一致、线缆套件字节正确、不同 KEM 产生不同
  报文尺寸。
- 既有 54 项混合握手/路由/单元测试在敏捷化后**全绿**。

---

## 8. 后续可扩展方向

- **加入更多 KEM**：BIKE（需开启 `oqs` 的 `bike` feature）、NTRU-Prime、HQC-192/256、
  FrodoKEM-976/1344；仅追加注册表项 + 调 `MAX_*`。
- **认证敏捷性（正交维度）**：在静态身份层引入 FIPS 204 (ML-DSA) / FIPS 205
  (SLH-DSA) 混合签名，与本 KEM 敏捷性组合成完整的"双敏捷"后量子套件协商。
- **UAPI 活体切换**：把 `set_active_suite_by_name` 暴露为 UAPI 配置键，实现运维通过
  `wg set` 风格命令在线切换。
- **策略化协商**：响应方可对发起方的套件做白名单/最低安全等级策略（目前响应方信任
  发起方选择并回显）。
