#!/usr/bin/env bash
#
# configure_peer.sh -- push one peer's config into a running v6 SM-PQ-WireGuard
# daemon through its UAPI socket. Run as root (the daemon's socket lives under
# /var/run/wireguard/ and the hybrid keys are ~1 MB of hex, so this avoids
# hand-typing the `set=1` transcript).
#
# Required env:
#   PRIV_FILE        own private_key hex file   (from keygen_hybrid, field 1)
#   PEER_PUB_FILE    peer's public_key hex file (from keygen_hybrid, field 2)
#   PSK_FILE         shared preshared_key hex   (same file on BOTH machines)
#   LISTEN_PORT      this side's UDP port,        e.g. 51820
#   PEER_ALLOWED_IP  peer's tunnel ip/cidr,       e.g. 10.66.0.2/32
# Optional:
#   PEER_ENDPOINT    peer's reachable ip:port,    e.g. 192.168.1.42:51820
#                    OMIT this on the responder side: the daemon learns the
#                    peer's address from the incoming handshake (roaming), so a
#                    peer that only ever dials in (e.g. behind NAT) needs no
#                    endpoint configured here.
#   KEEPALIVE        persistent keepalive seconds (default 25; 0 disables)
#   DEV              tun device name (default wg0)
#
set -euo pipefail
DEV="${DEV:-wg0}"
SOCK="/var/run/wireguard/${DEV}.sock"
KEEPALIVE="${KEEPALIVE:-25}"
: "${PRIV_FILE:?}" "${PEER_PUB_FILE:?}" "${PSK_FILE:?}"
: "${LISTEN_PORT:?}" "${PEER_ALLOWED_IP:?}"

[ -S "$SOCK" ] || { echo "no daemon socket at $SOCK -- is the daemon running for dev '$DEV'?" >&2; exit 1; }
command -v nc >/dev/null || { echo "need netcat (apt install netcat-openbsd)" >&2; exit 1; }

PRIV=$(tr -d '[:space:]' < "$PRIV_FILE")
PEER=$(tr -d '[:space:]' < "$PEER_PUB_FILE")
PSK=$(tr  -d '[:space:]' < "$PSK_FILE")

# Build the set=1 transcript; include endpoint= only when PEER_ENDPOINT is set.
TRANSCRIPT="set=1
private_key=$PRIV
listen_port=$LISTEN_PORT
public_key=$PEER
preshared_key=$PSK"
if [ -n "${PEER_ENDPOINT:-}" ]; then
    TRANSCRIPT="$TRANSCRIPT
endpoint=$PEER_ENDPOINT"
fi
TRANSCRIPT="$TRANSCRIPT
persistent_keepalive_interval=$KEEPALIVE
allowed_ip=$PEER_ALLOWED_IP"

printf '%s\n\n' "$TRANSCRIPT" | nc -U -q1 "$SOCK"
# A successful apply prints:  errno=0
