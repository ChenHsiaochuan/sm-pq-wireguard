#!/usr/bin/env bash
#
# run_full_tunnel_once.sh -- one full SM-PQ-WireGuard v6 tunnel handshake
# across two network namespaces, driven entirely through the userspace
# binary's UAPI socket. This is the reference $SMWG_E2E_COMMAND for
# run_namespace_matrix.sh.
#
# Contract (see run_namespace_matrix.sh):
#   in : NS_A NS_B IP_A IP_B VETH_A VETH_B WG_KEM_SUITE (from the matrix)
#   out: prints handshake latency in ms on success
#   rc : 0 ok | 10 tunnel packet loss | 11 auth failure | other crash
#
# WIRE/KEY FORMAT (hybrid build, from configuration_hybrid/uapi):
#   static KEM    = Classic McEliece 460896
#   private_key   = hex( SM2_secret[32] || McE_secret[13608] || McE_public[524160] )   # 537800 B
#   public_key    = hex( SM2_point[33]  || McE_public[524160] )                         # 524193 B
#   preshared_key = hex( psk[32] )
# Keys are set with `set=1\nprivate_key=..\n...` written to /var/run/wireguard/<dev>.sock.
#
# THE ONE DEPLOYMENT-SPECIFIC PIECE: generating a matching hybrid keypair.
# The v6 binary has no `genkey` subcommand, so this wrapper expects a helper
# that emits the three hex blobs. Point $SMWG_KEYGEN at it; it must print:
#       <private_key_hex> <public_key_hex>
# for one fresh identity per call. A reference helper can be a 20-line Rust
# example using sm2::SecretKey::random + oqs Kem(ClassicMcEliece460896).keypair
# and hex-encoding in the layout above. Until that helper exists on the host,
# this wrapper exits 11 (auth_fail) with a clear message, so the matrix records
# the gap honestly rather than reporting a fake success.
#
set -u
: "${NS_A:?}" "${NS_B:?}" "${IP_A:?}" "${IP_B:?}" "${VETH_A:?}" "${VETH_B:?}"
: "${WG_KEM_SUITE:?}"

BIN="${SMWG_BIN:-$PWD/../../artifacts_implementation/target/release/wireguard-rs-pq}"
DEV="${DEV:-smwg0}"
PORT_A="${PORT_A:-51820}"
PORT_B="${PORT_B:-51821}"
TUN_A="${TUN_A:-10.66.0.1}"
TUN_B="${TUN_B:-10.66.0.2}"
WGNS_DIR=/var/run/wireguard

die_auth() { echo "$*" >&2; exit 11; }

command -v "$BIN" >/dev/null 2>&1 || [ -x "$BIN" ] || die_auth "binary not found/executable: $BIN (build with: cargo build --release --features hybrid)"

if [ -z "${SMWG_KEYGEN:-}" ]; then
    die_auth "SMWG_KEYGEN not set: no hybrid (SM2+ClassicMcEliece) keygen helper available on this host. See header. Recording status=auth_fail so the matrix does not fabricate a success."
fi

read -r SK_A PK_A < <("$SMWG_KEYGEN")
read -r SK_B PK_B < <("$SMWG_KEYGEN")
PSK="$(head -c32 /dev/urandom | xxd -p -c256)"

uapi_set() { # $1 = netns, $2 = dev, $3 = config text
    ip netns exec "$1" sh -c "printf '%s\n\n' \"$3\" | nc -U -q1 ${WGNS_DIR}/$2.sock"
}

start_peer() { # $1 ns $2 dev $3 tunip $4 listenport $5 sk $6 peerpub $7 endpoint $8 allowed
    local ns="$1" dev="$2" tunip="$3" port="$4" sk="$5" peerpub="$6" ep="$7" allowed="$8"
    ip netns exec "$ns" "$BIN" -f "$dev" &  # foreground daemon, TUN+UAPI
    local pid=$!
    for _ in $(seq 1 50); do [ -S "${WGNS_DIR}/$dev.sock" ] && break; sleep 0.05; done
    ip -n "$ns" addr add "$tunip/24" dev "$dev"
    ip -n "$ns" link set "$dev" up
    uapi_set "$ns" "$dev" "set=1
private_key=$sk
listen_port=$port
public_key=$peerpub
preshared_key=$PSK
endpoint=$ep
persistent_keepalive_interval=0
allowed_ip=$allowed/32"
    echo "$pid"
}

cleanup() {
    [ -n "${PID_A:-}" ] && kill "$PID_A" 2>/dev/null
    [ -n "${PID_B:-}" ] && kill "$PID_B" 2>/dev/null
    wait 2>/dev/null
    rm -f "${WGNS_DIR}/${DEV}.sock"
}
trap cleanup EXIT

t0=$(date +%s.%N)
PID_B=$(start_peer "$NS_B" "$DEV" "$TUN_B" "$PORT_B" "$SK_B" "$PK_A" "$IP_A:$PORT_A" "$TUN_A")
PID_A=$(start_peer "$NS_A" "$DEV" "$TUN_A" "$PORT_A" "$SK_A" "$PK_B" "$IP_B:$PORT_B" "$TUN_B")

# Force a handshake by pushing one packet THROUGH the tunnel (tun ip -> tun ip).
if ip netns exec "$NS_A" timeout "${HS_TIMEOUT:-10}" ping -c1 -W3 "$TUN_B" >/dev/null 2>&1; then
    t1=$(date +%s.%N)
    awk "BEGIN{printf \"%.3f\n\",($t1-$t0)*1000}"   # handshake+first-RTT latency, ms
    exit 0
else
    # distinguish: did the daemon die (crash) vs no tunnel reply (loss)?
    kill -0 "$PID_A" 2>/dev/null && kill -0 "$PID_B" 2>/dev/null || { echo "peer crashed" >&2; exit 1; }
    echo "no reply through tunnel" >&2
    exit 10
fi
