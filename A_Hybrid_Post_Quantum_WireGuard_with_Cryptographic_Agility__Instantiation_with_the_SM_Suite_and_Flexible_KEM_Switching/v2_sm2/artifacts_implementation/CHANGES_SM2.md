# SM2 替换 X25519 修改文档

## 背景

将 `wireguard_hybrid` 模块中的 **X25519 ECDH** 替换为 **SM2 ECDH**（中国国密标准 GB/T 32918），
实现 SM2 + ML-KEM-512 的混合握手协议。`wireguard` 和 `wireguard_pq_star` 模块保持不变。

---

## 密码学变化

| 角色 | 原版 | SM2 版 |
|------|------|--------|
| 临时 DH | X25519（32 字节公钥）| SM2 ECDH（33 字节压缩公钥） |
| 静态 DH | X25519（32 字节公钥）| SM2 ECDH（33 字节压缩公钥） |
| DH 共享密钥输出 | 32 字节 | 32 字节（不变） |
| 临时 PQ KEM | ML-KEM-512 | ML-KEM-512（不变） |
| 静态 PQ KEM | Classic-McEliece-460896 | Classic-McEliece-460896（不变） |
| 协议标识符 | `Noise_IKpsk2_25519_ChaChaPoly_BLAKE2s` | `Noise_IKpsk2_SM2_ChaChaPoly_BLAKE2s` |

---

## 修改文件清单

### 1. `Cargo.toml`
- **新增**：`sm2 = "0.13"`
- **新增**：`elliptic-curve = { version = "0.13", features = ["ecdh", "arithmetic"] }`（sm2 0.13 未启用 ecdh 特性，需直接依赖）
- **保留**：`x25519-dalek`（wireguard、wireguard_pq_star 模块仍然使用）

### 2. `src/wireguard_hybrid/handshake/crypto_params.rs`
- 新增常量 `SIZE_SM2_POINT = 33`（SM2 压缩公钥字节数）
- 新增常量 `SIZE_DH_SHARED_SECRET = 32`（ECDH 输出字节数，SM2 与 X25519 相同）
- 移除常量 `SIZE_X25519_POINT`（拆分为上述两个常量）
- 协议 CONSTRUCTION 字符串更新为 `Noise_IKpsk2_SM2_ChaChaPoly_BLAKE2s`
- `INITIAL_CK` / `INITIAL_HS` 改为运行时函数计算（避免硬编码哈希值）

### 3. `src/wireguard_hybrid/handshake/messages.rs`
- `f_ephemeral` 字段大小：`SIZE_X25519_POINT(32)` → `SIZE_SM2_POINT(33)`
- 更新相关默认值初始化和测试数据

### 4. `src/wireguard_hybrid/handshake/noise.rs`（核心改动）
- 移除 `use x25519_dalek::...`
- 新增 `use sm2::...`（类型别名 `DhSecretKey`, `DhPublicKey`）
- 新增 `use elliptic_curve::ecdh::diffie_hellman`（直接依赖 elliptic-curve crate）
- 新增辅助函数 `random_sm2_sk()`：绕过 rand_core 版本差异，用字节生成 SM2 私钥
- 重写 `shared_secret()`：使用 `elliptic_curve::ecdh::diffie_hellman`
- 新增辅助函数 `pk_to_bytes()`、`pk_from_bytes()`
- 所有缓冲区拼接中的 `SIZE_X25519_POINT` 分别替换为：
  - 公钥上下文 → `SIZE_SM2_POINT`（4 处）
  - DH 输出上下文 → `SIZE_DH_SHARED_SECRET`（8 处）
- `INITIAL_CK` / `INITIAL_HS` 常量引用改为函数调用

### 5. `src/wireguard_hybrid/handshake/device.rs`
- 替换 `use x25519_dalek::...` 为 `use sm2::...`
- `KeyState.sk`: `StaticSecret` → `DhSecretKey`
- `KeyState.pk`: `PublicKey` → `DhPublicKey`
- `update_ss()`：使用 SM2 ECDH 替换 `key.sk.diffie_hellman(&pk)`
- `set_sk()` / `get_sk()` 签名更新
- `add()` 方法中的 `diffie_hellman` 调用更新
- `hash_static_keys()` 使用 `pk_to_bytes()` 序列化公钥

### 6. `src/wireguard_hybrid/handshake/peer.rs`
- 替换 `use x25519_dalek::...` 为 `use sm2::...`
- `Peer.pk`: `PublicKey` → `DhSecretKey`（类型替换）
- `State::InitiationSent.eph_sk`: `StaticSecret` → `DhSecretKey`
- `peer.pk.as_bytes()` 调用替换为 `pk_to_bytes(&peer.pk)`

### 7. `src/wireguard_hybrid/handshake/tests.rs`
- 替换 x25519 密钥生成为 SM2 密钥生成
- 更新 `setup_devices` 函数签名

### 8. `src/wireguard_hybrid/benchs.rs`
- 替换 x25519 密钥生成为 SM2 密钥生成

### 9. `src/configuration_hybrid/uapi/set.rs`
- 替换 `use x25519_dalek::...` 为 `use sm2::...`
- 更新公钥/私钥解析（字节偏移从 `32` 改为 `SIZE_SM2_POINT` / `SIZE_SM2_POINT-1`）
- `StaticSecret::from(sk)` → `DhSecretKey::from_bytes(&sk.into()).unwrap()`
- `PublicKey::from(pk)` → `DhPublicKey::from_sec1_bytes(&pk).unwrap()`

### 10. `src/configuration_hybrid/config.rs`
- 替换类型签名中的 `StaticSecret` / `PublicKey` 为 `DhSecretKey` / `DhPublicKey`

### 11. `src/configuration_hybrid/uapi/get.rs`
- 替换 `p.public_key.to_bytes()` → `p.public_key.to_encoded_point(true).as_bytes()`（SM2 公钥序列化）
- 更新缓冲区大小从 `32` 到 `SIZE_SM2_POINT` / `SIZE_SM2_POINT-1`

### 12. `src/wireguard_hybrid/wireguard.rs`
- 替换 `use x25519_dalek::...` 为 `use sm2::...`
- `set_key()` / `get_sk()` / `add_peer()` 签名更新

### 13. `src/wireguard_hybrid/peer.rs`
- 替换 `use x25519_dalek::PublicKey` 为 `use sm2::PublicKey as DhPublicKey`
- `PeerInner.pk` 类型更新

### 14. `src/wireguard_hybrid/timers.rs`
- 替换 `use x25519_dalek::PublicKey` 为 `use sm2::PublicKey as DhPublicKey`
- `Timers::new()` 参数类型更新

### 15. `src/wireguard_hybrid/workers.rs`
- 替换 `use x25519_dalek::PublicKey`
- `HandshakeJob::New` 枚举成员类型更新

### 16. `src/wireguard_hybrid/handshake/macs.rs`
- 移除未使用的 `use x25519_dalek::...` 和 `SIZE_X25519_POINT` 导入

---

## 消息格式变化

| 消息字段 | 原大小 | 新大小 | 说明 |
|----------|--------|--------|------|
| `NoiseInitiation.f_ephemeral` | 32 B | 33 B | SM2 压缩公钥 |
| `NoiseResponse.f_ephemeral` | 32 B | 33 B | SM2 压缩公钥 |
| InitHello 总大小 | 1156 B | 1157 B | +1 字节 |
| RespHello 总大小 | 1064 B | 1065 B | +1 字节 |

---

## 安全性说明

- SM2 基于 256 位椭圆曲线，安全级别与 X25519（128-bit） 相当
- SM2 是 Weierstrass 曲线（非 Montgomery），公钥需使用 SEC1 压缩编码（33 字节）
- DH 共享密钥输出仍为 32 字节（曲线 x 坐标），与原协议兼容
- 混合安全性依然成立：只要 SM2 或 ML-KEM 任一不被攻破，会话密钥安全
- 协议标识符已更新，防止与原版协议混淆

---

## 构建命令

```bash
source "$HOME/.cargo/env"
RUSTFLAGS="-L /opt/homebrew/opt/openssl@3/lib" cargo build
RUSTFLAGS="-L /opt/homebrew/opt/openssl@3/lib" cargo run -- -b 10
```

---

## 修改日志

| 日期 | 内容 |
|------|------|
| 2026-04-16 | 初始实现：SM2 ECDH 替换 X25519，完成全部 16 个文件修改 |
| 2026-04-16 | 构建验证通过：`cargo build` 零错误；16 项 wireguard_hybrid 单元测试全部通过；benchmark 正常运行输出 InitHello=1157B，RespHello=1065B |
