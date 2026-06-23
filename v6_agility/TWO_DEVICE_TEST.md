# 两台真机跑通 v6 SM-PQ-WireGuard 完整流程（WSL + Mac 专用版）

> 你的环境：**你用 WSL2（Windows），同学用 Mac 笔记本。** 本手册按这个组合定制，
> 不需要改任何系统环境。

## 为什么是这个拓扑（先理解，再照做）

本工程的守护进程 `wireguard-rs-pq` 是**纯 Linux 程序**（`main.rs` 里非 Linux 直接退出），
而且配置走 UAPI socket、用 SM2 + Classic McEliece 混合身份。两个硬约束决定了角色分工：

| 约束 | 结论 |
|------|------|
| Mac **不能原生跑**这个 Linux 二进制 | 同学的 Mac 必须把它放进一个 **Linux 容器（Docker）** 里跑 |
| WSL2 **入站 UDP 很难**（Windows 的 portproxy 只支持 TCP，转发 UDP 要折腾镜像网络） | 让 WSL **只做发起方（出站）**，WSL2 出站天然可用，完全不碰 Windows 端口转发 |
| Mac 上 Docker 可以 `-p 51820:51820/udp` 轻松发布 UDP 端口 | 让 **Mac 做响应方**，对 WSL 可达 |
| 本实现支持 **endpoint roaming**（收到握手就记住对端地址，见 `workers.rs:218`） | Mac 响应方**不需要预先知道 WSL 的地址**，WSL 先发起即可 |

**最终角色：**

```
角色                 隧道内 IP      UDP 监听口          说明
WSL（你）            10.66.0.1     51820（仅出站）     握手发起方 initiator
Mac（同学，Docker）   10.66.0.2     51820（已发布）     握手响应方 responder
```

## ⚠️ 唯一的网络前提：两台在同一局域网

WSL 要能访问 **Mac 的局域网 IP**。所以 **两台电脑必须连同一个路由器 / 同一个 Wi‑Fi**。
- Mac 查自己的局域网 IP：`ipconfig getifaddr en0`（Wi‑Fi）或 `ipconfig getifaddr en1`。
- 验证：WSL 里 `ping <Mac的局域网IP>` 能通，基本就 OK。
- 如果不在同一网络（各自不同 Wi‑Fi）：最简单是**两台都连同一个手机热点**；否则需要一台有公网 IP 的云主机做中转（本手册不展开）。

---

# Part A — Mac 端（同学操作，响应方，跑在 Docker 里）

> 前提：Mac 装了 **Docker Desktop** 并已启动；Mac 上有本工程代码（含本次新增的
> `examples/keygen_hybrid.rs`、`mac_responder.Dockerfile`）。若同学的副本较旧，把这两个
> 新文件同步过去即可。

### A1. 构建镜像（首次几分钟，liboqs 要从源码编）

```bash
cd workspace/v6_agility/artifacts_implementation
docker build -f ../mac_responder.Dockerfile -t smwg-responder .
```

### A2. 启动容器（发布 UDP 51820，挂一个目录用于交换密钥）

```bash
mkdir -p ~/smwg-keys
docker run -it --rm --name smwg \
  --cap-add NET_ADMIN --device /dev/net/tun \
  -p 51820:51820/udp \
  -v ~/smwg-keys:/keys \
  smwg-responder bash
# 若提示 /dev/net/tun 不存在，把 `--cap-add NET_ADMIN --device /dev/net/tun` 换成 `--privileged`
```

> 现在你在容器内（一个 root 的 Linux shell）。`~/smwg-keys` ↔ 容器内 `/keys` 是同一个目录，
> 方便把公钥拷出去 AirDrop / 发给你。

### A3. 生成 Mac 自己的身份密钥（容器内）

```bash
/build/target/release/examples/keygen_hybrid > /keys/mac_id.txt
cut -d' ' -f1 /keys/mac_id.txt > /keys/mac_private.hex   # 私钥 537800 B
cut -d' ' -f2 /keys/mac_id.txt > /keys/mac_public.hex    # 公钥 524193 B（约 1MB）
```

把 `~/smwg-keys/mac_public.hex` 发给你（你会把它存成 `peer_public.hex`）。

### A4. 启动守护进程（容器内，前台保活）

```bash
RUST_LOG=info /build/target/release/wireguard-rs-pq -f wg0
# 看到 "Crypto agility: ephemeral KEM = ml-kem-512 ..." 即启动成功，保持这个窗口别关
```

### A5. 另开一个容器 shell 做配置（Mac 新终端）

```bash
docker exec -it smwg bash
```
在这个新 shell 里（**等你把 WSL 的公钥 `wsl_public.hex` 和共享 `psk.hex` 放进 `~/smwg-keys` 之后**再执行）：

```bash
# 隧道内地址
ip addr add 10.66.0.2/24 dev wg0
ip link set wg0 up

# 写入对端(=WSL)配置。响应方【不设 endpoint】，靠 roaming 学习 WSL 地址。
PRIV=$(tr -d '[:space:]' < /keys/mac_private.hex)
PEER=$(tr -d '[:space:]' < /keys/wsl_public.hex)
PSK=$(tr  -d '[:space:]' < /keys/psk.hex)
printf 'set=1\nprivate_key=%s\nlisten_port=51820\npublic_key=%s\npreshared_key=%s\npersistent_keepalive_interval=25\nallowed_ip=10.66.0.1/32\n\n' \
  "$PRIV" "$PEER" "$PSK" | nc -U -q1 /var/run/wireguard/wg0.sock
# 成功输出： errno=0
```

Mac 端就绪。下面看 Part B 你这边，握手由你发起。

---

# Part B — WSL 端（你操作，发起方，原生跑）

### B1. 准备依赖 + 编译（一次性）

```bash
# 确认有 TUN（一般 WSL2 自带）：
ls -l /dev/net/tun || sudo modprobe tun

sudo apt install -y netcat-openbsd iproute2 iputils-ping xxd iperf3
cd workspace/v6_agility/artifacts_implementation
. "$HOME/.cargo/env"
cargo build --release --features hybrid                            # 守护进程
cargo build --release --features hybrid --example keygen_hybrid    # 密钥助手
```

> **必须带 `--features hybrid`**——线缆格式取决于它，两端要一致。

### B2. 生成你的身份密钥 + 生成共享 PSK（你来生成 PSK，两台共用）

```bash
cargo run --release --features hybrid --example keygen_hybrid > my_id.txt
cut -d' ' -f1 my_id.txt > my_private.hex
cut -d' ' -f2 my_id.txt > my_public.hex     # 发给同学，存成他那边的 wsl_public.hex

head -c32 /dev/urandom | xxd -p -c256 > psk.hex   # 共享 PSK，发给同学放进 ~/smwg-keys/psk.hex
```

**密钥交换汇总**（公钥约 1MB，用文件传输，别复制粘贴）：
- 你 `my_public.hex`  → 同学存成 `~/smwg-keys/wsl_public.hex`
- 同学 `mac_public.hex` → 你存成 `peer_public.hex`
- `psk.hex` → 两边内容必须**完全相同**

### B3. 启动守护进程（前台保活，新开终端）

```bash
cd workspace/v6_agility/artifacts_implementation
sudo RUST_LOG=info ./target/release/wireguard-rs-pq -f wg0
```

### B4. 配置隧道地址 + 对端（你这边要填 Mac 的 endpoint）

```bash
cd ../artifacts_evaluation/network_experiments
sudo ip addr add 10.66.0.1/24 dev wg0
sudo ip link set wg0 up

# 发起方【要设 endpoint】= Mac的局域网IP:51820
sudo env DEV=wg0 \
  PRIV_FILE=../../artifacts_implementation/my_private.hex \
  PEER_PUB_FILE=../../artifacts_implementation/peer_public.hex \
  PSK_FILE=../../artifacts_implementation/psk.hex \
  LISTEN_PORT=51820 \
  PEER_ENDPOINT=<Mac的局域网IP>:51820 \
  PEER_ALLOWED_IP=10.66.0.2/32 \
  ./configure_peer.sh
# 成功输出： errno=0
```

---

# Part C — 触发握手 + 验证 + 数据传输

### C1. 由你（WSL，发起方）触发握手

```bash
ping -c4 10.66.0.2
```
- 第一个包触发后量子混合握手（Noise IKpsk2 + ML‑KEM‑512 临时 KEM + Classic McEliece 身份）。
- 两台守护进程日志应出现握手发起/响应、`Adding keypair`、`keepalive` 等。

### C2. 查状态（任一端）

```bash
# WSL：
printf 'get=1\n\n' | sudo nc -U -q1 /var/run/wireguard/wg0.sock | \
  grep -E 'last_handshake_time_sec|rx_bytes|tx_bytes'
# Mac 容器内同理（去掉 sudo）
```
`last_handshake_time_sec` 非 0 + ping 有回包 = **握手成功，隧道已通**。

### C3. 真实加密数据传输（SM4‑GCM 数据平面）

```bash
# Mac 容器内（在 A5 那个 docker exec shell 里）起服务端：
iperf3 -s -B 10.66.0.2
# WSL 这边打流：
iperf3 -c 10.66.0.2 -t 10
```
吞吐就是 SM4‑GCM（v5 GFNI+AVX2 加速）穿隧道的实际加密速度。

### C4.（可选）体验 v6 密码敏捷性

发起方（WSL）启动守护进程时加环境变量切换临时 KEM 套件，逐握手协商：
```bash
sudo WG_KEM_SUITE=kyber-512 RUST_LOG=info ./target/release/wireguard-rs-pq -f wg0
# 可选：ml-kem-768 / ml-kem-1024 / hqc-128 / frodo-640-aes
# 后几个报文超 1280B 会走 IP 分片，正好测分片/重组路径。保险起见两端设同一套件。
```
换套件后需重启两端守护进程并重新执行各自的配置步骤。

---

## 出问题时排查（WSL+Mac 专项）

| 现象 | 多半原因 / 处理 |
|------|----------------|
| WSL `ping <Mac局域网IP>` 不通 | 两台不在同一 Wi‑Fi；或 Mac 防火墙拦截。先解决基础可达性再继续 |
| 握手不动、`last_handshake_time_sec=0` | ① Mac 的 `-p 51820:51820/udp` 没发布或容器没在跑；② endpoint IP 写错；③ Mac 系统防火墙拦 UDP 51820 |
| `docker run` 报 `/dev/net/tun` 不存在 | 改用 `--privileged` 启动容器 |
| `errno!=0` | 公钥/私钥文件搞反、hex 长度不对（私钥应 1075600 字符、公钥 1048386）、没用 `--features hybrid` 编译 |
| 容器内守护进程起不来 | 缺 `--cap-add NET_ADMIN`；设备名 `wg0` 占用（换 `wg1`） |
| 握手成功但 ping 偶尔丢 | 用了大报文套件（hqc/frodo/ml‑kem‑1024）分片+MTU，先用默认 ml‑kem‑512 验证连通 |
| Mac 收不到 WSL 回包 | WSL 是 NAT 后的发起方，确保 WSL 侧 `persistent_keepalive=25`（脚本默认已设）保活 NAT 映射 |

> 对照：工程自带 `run_full_tunnel_once.sh` 是在**单机两个 netns** 内自动跑同一套流程，
> 可先在任一台 Linux 上单机自测一遍，确认二进制本身没问题，再做这次两机联调。
