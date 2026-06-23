# 混合后量子 WireGuard 密钥交换流程说明（X25519 版） + SM2 对比

**文档目的**：说明原始 X25519 + ML-KEM + McEliece 混合握手的完整密钥交换流程，并指出替换为 SM2 后的差异点。

---

## 一、协议总览

### 1.1 协议标识符

```
Noise_IKpsk2_25519_ChaChaPoly_BLAKE2s     ← X25519 版
Noise_IKpsk2_SM2_ChaChaPoly_BLAKE2s       ← SM2 版（仅此字符串不同）
```

### 1.2 角色与符号

| 符号 | 含义 |
|------|------|
| I | Initiator（发起方） |
| R | Responder（响应方） |
| S_priv / S_pub | 长期静态 DH 密钥对 |
| E_priv / E_pub | 临时 DH 密钥对（每次握手新生成） |
| S_pub_pq / S_priv_pq | 静态 KEM 密钥对（McEliece-460896） |
| E_pub_pq / E_priv_pq | 临时 KEM 密钥对（ML-KEM-512） |
| Q | 32 字节预共享密钥 PSK |
| C | Chain key（HKDF 链） |
| H | Handshake hash（用作 AEAD 关联数据） |
| ‖ | 字节拼接 |

### 1.3 密码原语清单

| 原语 | X25519 版 | SM2 版 |
|------|-----------|--------|
| 经典 DH | X25519 | **SM2 ECDH** |
| 临时 KEM | ML-KEM-512 | ML-KEM-512（不变） |
| 静态 KEM | Classic-McEliece-460896 | Classic-McEliece-460896（不变） |
| AEAD | XChaCha20-Poly1305 | XChaCha20-Poly1305（不变） |
| 流加密 | ChaCha20 | ChaCha20（不变） |
| Hash | Blake2s | Blake2s（不变） |
| KDF | HKDF-Blake2s | HKDF-Blake2s（不变） |

---

## 二、X25519 版完整握手流程

### 2.1 阶段 0：初始化

双方各自计算（无通信）：

```
C₀ = HASH("Noise_IKpsk2_25519_ChaChaPoly_BLAKE2s")
H₀ = HASH(C₀ ‖ "WireGuard v1 zx2c4 Jason@zx2c4.com")
```

预先持有：
- 自身静态密钥对 (S_priv, S_pub)、(S_priv_pq, S_pub_pq)
- 对方静态公钥 S_pub_R、S_pub_R_pq
- 共享 PSK Q
- 预计算 SS = X25519(S_priv_I, S_pub_R)（双方均可计算同值）

---

### 2.2 阶段 1：Initiator 构造 InitHello

**Step 1**：扩展握手 hash 绑定接收方身份
```
H = HASH(H₀ ‖ HASH(S_pub_R ‖ S_pub_R_pq))
```

**Step 2**：生成临时密钥对
```
(E_priv, E_pub) = X25519_Generate()
(E_pub_pq, E_priv_pq) = ML-KEM-512.Keygen()
```

**Step 3**：吸收临时公钥到 chain key
```
C = KDF1(C₀, E_pub ‖ E_pub_pq)
```

**Step 4**：第 1 次 DH，掩盖 KEM 密文
```
DH1 = X25519(E_priv, S_pub_R)            ← 临时-静态 DH
k = KDF1(0³², DH1)
(static_ct_pq, shk1) = McEliece.Encap(S_pub_R_pq)
msg.f_static_ct_pq = ChaCha20(k, static_ct_pq)   ← 用 DH1 加密 KEM 密文
```

**Step 5**：第 1 次混合 — DH1 与 KEM1 共享秘密合并
```
H = HASH(H ‖ msg.f_ephemeral ‖ msg.f_ephemeral_pq)
(C, k) = KDF2(C, DH1 ‖ shk1)
```

**Step 6**：用派生密钥加密"我的身份"（自身静态公钥哈希）
```
msg.f_static = AEAD-Seal(k, nonce=0, ad=H, pt=HASH(S_pub_I ‖ S_pub_I_pq))
H = HASH(H ‖ msg.f_static)
```

**Step 7**：第 2 次混合 — 静态-静态 DH + KEM 公钥绑定 + PSK
```
(C, k) = KDF2(C, SS ‖ HASH(S_pub_I_pq ‖ S_pub_R_pq) ‖ Q)
```

**Step 8**：用派生密钥加密时间戳/计数器
```
msg.f_timestamp = AEAD-Seal(k, nonce=0, ad=H, pt=k_send_counter)
H = HASH(H ‖ msg.f_timestamp)
```

**Step 9**：发送 InitHello，本端进入 `InitiationSent { eph_priv, eph_priv_pq, hs=H, ck=C }` 状态

**InitHello 报文结构**：
```
[type:4][sender:4][f_ephemeral:32][f_ephemeral_pq:800]
[f_static_ct_pq:156][f_static:32+16][f_timestamp:16+16][macs:32]
总计：1156 字节（X25519 版）
```

---

### 2.3 阶段 2：Responder 处理 InitHello + 构造 RespHello

#### 2.3.1 处理 InitHello

**Step 1-3**：重做发起方的 1-3，计算同样的 H 与 C₁

**Step 4**：第 1 次 DH（响应方视角）
```
DH1 = X25519(S_priv_R, msg.f_ephemeral)        ← 同值
k = KDF1(0³², DH1)
static_ct_pq = ChaCha20⁻¹(k, msg.f_static_ct_pq)
shk1 = McEliece.Decap(S_priv_R_pq, static_ct_pq)
(C, k) = KDF2(C, DH1 ‖ shk1)
```

**Step 5**：解密 `msg.f_static`，拿到对方身份哈希 → 查出 peer
```
peer_pk_hash = AEAD-Open(k, ...)
peer = device.lookup(peer_pk_hash)
```

**Step 6**：第 2 次混合
```
H = HASH(H ‖ msg.f_static)
(C, k) = KDF2(C, peer.SS ‖ HASH(S_pub_R_pq ‖ peer.S_pub_pq) ‖ Q)
```

**Step 7**：解密 `msg.f_timestamp`，做防重放检查
```
k_received = AEAD-Open(k, ...)
peer.check_replay_flood(k_received)             ← 必须 > 上次记录值
```

#### 2.3.2 构造 RespHello

**Step 8**：生成响应方临时密钥
```
(E_priv_R, E_pub_R) = X25519_Generate()
```

**Step 9**：双 KEM 封装
```
(eph_ct_pq, shk2) = ML-KEM-512.Encap(peer.eph_pub_pq)         ← 临时 PQ
(static_ct_pq, shk3) = McEliece.Encap(peer.S_pub_pq)          ← 静态 PQ
```

**Step 10**：第 1 次响应方 DH，加密 McEliece 密文
```
DH3 = X25519(E_priv_R, peer.S_pub_I)            ← 临时-静态
k = KDF1(0³², DH3)
msg.f_static_ct_pq = ChaCha20(k, static_ct_pq)
```

**Step 11**：吸收响应方临时公钥与 ML-KEM 密文
```
C = KDF1(C, E_pub_R ‖ eph_ct_pq)
H = HASH(H ‖ msg.f_ephemeral ‖ msg.f_ephemeral_ct_pq)
```

**Step 12**：第 3 次混合 — 临时-临时 DH + 临时 KEM
```
DH2 = X25519(E_priv_R, peer.eph_pub_I)
C = KDF1(C, DH2 ‖ shk2)
```

**Step 13**：第 4 次混合 — 临时-静态 DH + 静态 KEM
```
C = KDF1(C, DH3 ‖ shk3)
```

**Step 14**：PSK 二次混入
```
(C, τ, k) = KDF3(C, Q)
H = HASH(H ‖ τ)
```

**Step 15**：发送空 AEAD 作为完成确认
```
msg.f_empty = AEAD-Seal(k, nonce=0, ad=H, pt=ε)
```

**Step 16**：派生传输密钥
```
(K_recv_R, K_send_R) = KDF2(C, ∅)
```

**RespHello 报文结构**：
```
[type:4][sender:4][receiver:4][f_ephemeral:32][f_ephemeral_ct_pq:768]
[f_static_ct_pq:156][f_empty:0+16][macs:32]
总计：1064 字节（X25519 版）
```

---

### 2.4 阶段 3：Initiator 处理 RespHello

发起方对称地重做响应方的 Step 8-16，最终：
- 计算出同样的 chain key C
- 派生 `(K_send_I, K_recv_I) = KDF2(C, ∅)`，方向与响应方相反
- 验证 `f_empty` AEAD 解密成功 → 握手完成

**对称性保证**：`K_send_I == K_recv_R`、`K_recv_I == K_send_R`，双方进入数据传输阶段。

---

## 三、Chain Key 演进总览图

```
┌─────────────────────────────────────────────────────────────────┐
│                     InitHello 处理后                              │
├─────────────────────────────────────────────────────────────────┤
│ C₀ = HASH(CONSTRUCTION)                                         │
│ C₁ = KDF1(C₀, E_pub_I ‖ E_pub_I_pq)                             │
│ C₂ = KDF2(C₁, DH1 ‖ shk1).ck      ← 第1次混合：经典 + KEM       │
│ C₃ = KDF2(C₂, SS ‖ H_pq ‖ Q).ck    ← 第2次混合：静态 + 绑定 + PSK│
├─────────────────────────────────────────────────────────────────┤
│                     RespHello 处理后                              │
├─────────────────────────────────────────────────────────────────┤
│ C₄ = KDF1(C₃, E_pub_R ‖ eph_ct_pq)                              │
│ C₅ = KDF1(C₄, DH2 ‖ shk2)         ← 第3次混合：临时-临时 + ML-KEM│
│ C₆ = KDF1(C₅, DH3 ‖ shk3)         ← 第4次混合：临时-静态 + KEM   │
│ C₇ = KDF3(C₆, Q).ck               ← PSK 二次混入                 │
├─────────────────────────────────────────────────────────────────┤
│ (K_recv, K_send) = KDF2(C₇, ∅)                                  │
└─────────────────────────────────────────────────────────────────┘
```

**混合安全性**：会话密钥的安全性由 X25519、ML-KEM、McEliece、PSK **任一不被攻破** 即可保证。

---

## 四、SM2 版与 X25519 版的差异

### 4.1 差异总览

| 维度 | X25519 版 | SM2 版 |
|------|-----------|--------|
| **协议字符串** | `Noise_IKpsk2_25519_ChaChaPoly_BLAKE2s` | `Noise_IKpsk2_SM2_ChaChaPoly_BLAKE2s` |
| **DH 算法** | X25519（Montgomery 曲线） | SM2 ECDH（Weierstrass 曲线） |
| **公钥编码** | 32 B 裸字节 | 33 B SEC1 压缩点 |
| **DH 输出** | 32 B（u 坐标） | 32 B（x 坐标） |
| **InitHello 大小** | 1156 B | **1157 B**（+1 B） |
| **RespHello 大小** | 1064 B | **1065 B**（+1 B） |
| **私钥构造** | 任意 32 B 字节均合法 | 必须为有效标量（剔除 0 与 ≥ n） |
| **Rust 库** | `x25519_dalek` | `sm2 + elliptic-curve` |
| **rand_core 版本** | 0.5 | 0.6 |

### 4.2 协议流程层面：完全相同

**关键观察**：握手的 9 步 InitHello + 16 步 RespHello **结构完全一致**，所有 KDF 调用顺序、Hash 顺序、AEAD 调用顺序都不变。

仅以下三处涉及具体替换：

| Step | X25519 | SM2 |
|------|--------|-----|
| 临时密钥生成 | `(E_priv, E_pub) = X25519_Keygen()` | `(E_priv, E_pub) = SM2_Keygen()` |
| 临时-静态 DH | `DH1 = X25519(E_priv, S_pub_R)` | `DH1 = SM2_ECDH(E_priv, S_pub_R)` |
| 静态-静态 DH | `SS = X25519(S_priv_I, S_pub_R)` | `SS = SM2_ECDH(S_priv_I, S_pub_R)` |

### 4.3 编码层面的差异（影响消息格式）

```
X25519 公钥：32 字节裸字节
            ┌──────────────────────────────────┐
            │  u-coordinate (256-bit, LE)      │
            └──────────────────────────────────┘

SM2 公钥（SEC1 压缩）：33 字节
            ┌─────┬────────────────────────────────┐
            │ tag │  x-coordinate (256-bit, BE)    │
            │0x02 │                                │
            │/0x03│                                │
            └─────┴────────────────────────────────┘
              ↑
              y 的奇偶性指示符
```

**影响范围**：所有携带公钥的字段、所有"公钥 ‖ 其他"的拼接缓冲区、所有 hex 序列化/反序列化代码。

### 4.4 工程实现差异

#### (1) 私钥生成
```rust
// X25519：任意 32 字节都可
let sk = StaticSecret::from([0x3f; 32]);

// SM2：必须有效标量，硬编码字节高概率失败
let sk = DhSecretKey::random(&mut OsRng);   // 推荐
// 或拒绝采样：
loop {
    let mut bytes = [0u8; 32];
    rng.fill_bytes(&mut bytes);
    if let Ok(sk) = DhSecretKey::from_slice(&bytes) { break sk; }
}
```

#### (2) 公钥序列化
```rust
// X25519：直接拷贝
let pk_bytes: [u8; 32] = pk.to_bytes();

// SM2：通过 SEC1 编码
let pk_bytes: [u8; 33] = pk.to_encoded_point(true)
                          .as_bytes().try_into().unwrap();
```

#### (3) DH 调用
```rust
// X25519：方法调用风格
let shared = sk.diffie_hellman(&pk);
let bytes: [u8; 32] = shared.to_bytes();

// SM2：函数式风格
use elliptic_curve::ecdh::diffie_hellman;
let shared = diffie_hellman(sk.to_nonzero_scalar(), pk.as_affine());
let bytes: [u8; 32] = (*shared.raw_secret_bytes()).into();
```

#### (4) RNG 兼容性
- `x25519_dalek` 使用 `rand_core 0.5`
- `sm2`（via `elliptic-curve`）使用 `rand_core 0.6`
- 解决方案：在测试与基准中引入 `rand_oqs::rngs::OsRng as OsRng08`（rand 0.8 = rand_core 0.6 兼容）

### 4.5 安全性层面：等价保证

| 属性 | X25519 | SM2 |
|------|--------|-----|
| 安全级别 | 128-bit | 128-bit |
| 抗量子 | ❌ | ❌（同样需 PQ KEM 兜底） |
| 前向安全 | ✓（临时密钥） | ✓（临时密钥） |
| KCI 抗性 | ✓ | ✓ |
| 混合保证 | 任一原语不破即安全 | **完全相同** |

**结论**：SM2 版与 X25519 版在协议安全性上**等价**，差异仅在底层椭圆曲线选择（中国国密 vs 西方标准）。

### 4.6 性能差异（实测数据）

| 指标 | X25519 版（原版） | SM2 版（本工作） | Δ |
|------|-----------------|----------------|---|
| InitHello 大小 | 1156 B | 1157 B | **+1 B** |
| RespHello 大小 | 1064 B | 1065 B | **+1 B** |
| InitHello 构造时延 | ~0.30 ms | 0.291 ms | ≈ 持平 |
| RespHello 构造时延 | ~28 ms | 27.859 ms | ≈ 持平 |

**结论**：消息开销与时延几乎不变，主要开销由 ML-KEM/McEliece 主导，SM2 vs X25519 在该场景下性能等价。

---

## 五、关键代码位置对照

| 协议步骤 | 源码位置 |
|---------|---------|
| 初始 chain key | `noise.rs::initial_ck()` / `initial_hs()` |
| 公钥序列化 | `noise.rs::pk_to_bytes()` / `pk_from_bytes()` |
| ECDH 计算 | `noise.rs::shared_secret()` |
| Initiator 构造 | `noise.rs::create_initiation()` |
| Responder 处理 Init | `noise.rs::consume_initiation_first_part()` / `_second_part()` |
| Responder 构造 Resp | `noise.rs::create_response()` |
| Initiator 处理 Resp | `noise.rs::consume_response()` |
| 静态-静态 DH 预计算 | `device.rs::update_ss()` |
| 临时密钥随机生成 | `noise.rs::random_sm2_sk()`（SM2 版独有） |

---

## 六、汇报关键句

> **"X25519 版与 SM2 版的协议骨架完全相同——同样的 9 步 Init + 16 步 Resp，同样的 4 次 KDF 混入，同样的混合安全性保证。差异只在三处：用 SM2 ECDH 替换 X25519、公钥编码从 32B 变 33B、协议字符串声明替换。这意味着我们既保留了原论文的全部安全分析结论，又完成了国密合规化。"**

---

## 附：消息格式对照

### InitHello

| 字段 | 字节数 | X25519 版 | SM2 版 |
|------|-------|-----------|--------|
| type | 4 | 0x01 | 0x01 |
| sender | 4 | sender id | sender id |
| f_ephemeral | **32 / 33** | X25519 公钥 | **SM2 SEC1 公钥** |
| f_ephemeral_pq | 800 | ML-KEM-512 公钥 | 同 |
| f_static_ct_pq | 156 | McEliece 密文（ChaCha20 加密） | 同 |
| f_static | 48 | AEAD(身份哈希 32 + tag 16) | 同 |
| f_timestamp | 32 | AEAD(计数器 16 + tag 16) | 同 |
| macs | 32 | mac1 16 + mac2 16 | 同 |
| **总计** | | **1156** | **1157** |

### RespHello

| 字段 | 字节数 | X25519 版 | SM2 版 |
|------|-------|-----------|--------|
| type | 4 | 0x02 | 0x02 |
| sender | 4 | sender id | sender id |
| receiver | 4 | initiator id | initiator id |
| f_ephemeral | **32 / 33** | X25519 公钥 | **SM2 SEC1 公钥** |
| f_ephemeral_ct_pq | 768 | ML-KEM 密文 | 同 |
| f_static_ct_pq | 156 | McEliece 密文（ChaCha20 加密） | 同 |
| f_empty | 16 | AEAD(空 + tag 16) | 同 |
| macs | 32 | mac1 16 + mac2 16 | 同 |
| **总计** | | **1064** | **1065** |
