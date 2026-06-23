#!/usr/bin/env bash
#
# run_namespace_matrix.sh -- real UDP/TUN end-to-end handshake matrix for
# SM-PQ-WireGuard v6, sweeping ephemeral-KEM suite x MTU x loss x reorder.
#
# For each cell it builds two network namespaces (smwg-a, smwg-b) joined by a
# veth pair, applies `tc netem` (MTU via the link, loss/reorder via qdisc) to
# the path between them, and runs $ROUNDS handshakes. Each round invokes
# $SMWG_E2E_COMMAND, which MUST:
#   - start peer A in netns smwg-a, peer B in netns smwg-b;
#   - configure static SM2 + static Classic McEliece + PSK + endpoint +
#     allowed-IPs + the selected $WG_KEM_SUITE;
#   - push at least one packet through the PROTECTED TUNNEL (not the veth path);
#   - tear both peers down;
#   - print the handshake wall-clock latency in milliseconds to stdout;
#   - exit 0 only on success, nonzero on timeout / tunnel loss / crash / auth
#     failure (the harness maps the exit code to a status, see below).
#
# If $SMWG_E2E_COMMAND is unset, the harness runs a FALLBACK SMOKE CHECK that
# only pings across the bare veth path. The smoke check exercises the netem
# profile and the matrix plumbing but is NOT a tunnel handshake; rows it emits
# are tagged status=smoke and MUST NOT be reported as end-to-end results.
#
# Requires root (ip netns, tc). Outputs:
#   $OUT/handshake_samples.csv   suite,mtu,loss_pct,reorder_pct,round,status,handshake_ms
#   $OUT/run.log                 per-cell progress
#
set -u

SUITES="${SUITES:-ml-kem-512 ml-kem-768 ml-kem-1024 kyber-512 hqc-128 frodo-640-aes}"
MTUS="${MTUS:-1280 1420 1500}"
LOSSES="${LOSSES:-0 1 3}"
REORDERS="${REORDERS:-0 5}"
ROUNDS="${ROUNDS:-100}"
OUT="${OUT:-$PWD/results/full_tunnel}"
NS_A="${NS_A:-smwg-a}"
NS_B="${NS_B:-smwg-b}"
VETH_A="${VETH_A:-veth-a}"
VETH_B="${VETH_B:-veth-b}"
IP_A="${IP_A:-10.55.0.1}"
IP_B="${IP_B:-10.55.0.2}"
HS_TIMEOUT="${HS_TIMEOUT:-10}"   # seconds per handshake attempt

if [ "$(id -u)" -ne 0 ]; then
    echo "ERROR: must run as root (ip netns / tc). Re-run under sudo." >&2
    exit 2
fi
mkdir -p "$OUT"
SAMPLES="$OUT/handshake_samples.csv"
LOG="$OUT/run.log"
echo "suite,mtu,loss_pct,reorder_pct,round,status,handshake_ms" > "$SAMPLES"
: > "$LOG"

log() { echo "$(date -Iseconds) $*" | tee -a "$LOG" >&2; }

teardown() {
    ip netns del "$NS_A" 2>/dev/null || true
    ip netns del "$NS_B" 2>/dev/null || true
}
trap teardown EXIT

setup_cell() {
    local mtu="$1" loss="$2" reorder="$3"
    teardown
    ip netns add "$NS_A"; ip netns add "$NS_B"
    ip link add "$VETH_A" netns "$NS_A" type veth peer name "$VETH_B" netns "$NS_B"
    ip -n "$NS_A" addr add "$IP_A/24" dev "$VETH_A"
    ip -n "$NS_B" addr add "$IP_B/24" dev "$VETH_B"
    ip -n "$NS_A" link set "$VETH_A" mtu "$mtu" up
    ip -n "$NS_B" link set "$VETH_B" mtu "$mtu" up
    ip -n "$NS_A" link set lo up
    ip -n "$NS_B" link set lo up

    # netem on both egress directions: loss% and reorder%
    local nem=""
    [ "$loss" != "0" ] && nem="$nem loss ${loss}%"
    [ "$reorder" != "0" ] && nem="$nem delay 1ms reorder $((100-reorder))% ${reorder}%"
    if [ -n "$nem" ]; then
        # shellcheck disable=SC2086
        ip netns exec "$NS_A" tc qdisc add dev "$VETH_A" root netem $nem
        # shellcheck disable=SC2086
        ip netns exec "$NS_B" tc qdisc add dev "$VETH_B" root netem $nem
    fi
}

# Map an exit code from the E2E command to a status label.
status_for() {
    case "$1" in
        0)   echo ok ;;
        124) echo timeout ;;   # GNU timeout
        10)  echo loss ;;
        11)  echo auth_fail ;;
        *)   echo crash ;;
    esac
}

run_real_round() {
    local out rc
    out="$(NS_A="$NS_A" NS_B="$NS_B" IP_A="$IP_A" IP_B="$IP_B" \
           VETH_A="$VETH_A" VETH_B="$VETH_B" WG_KEM_SUITE="$WG_KEM_SUITE" \
           timeout "$HS_TIMEOUT" "$SMWG_E2E_COMMAND" 2>>"$LOG")"
    rc=$?
    local st; st="$(status_for "$rc")"
    local ms=""
    [ "$st" = ok ] && ms="$(printf '%s' "$out" | grep -oE '[0-9]+(\.[0-9]+)?' | tail -1)"
    echo "$st,$ms"
}

run_smoke_round() {
    # bare-veth reachability only; NOT a tunnel handshake
    local start end ms rc
    start=$(date +%s.%N)
    ip netns exec "$NS_A" timeout "$HS_TIMEOUT" ping -c1 -W2 "$IP_B" >/dev/null 2>&1
    rc=$?
    end=$(date +%s.%N)
    if [ "$rc" -eq 0 ]; then
        ms=$(awk "BEGIN{printf \"%.3f\",($end-$start)*1000}")
        echo "smoke,$ms"
    else
        echo "loss,"
    fi
}

MODE="real"; [ -z "${SMWG_E2E_COMMAND:-}" ] && MODE="smoke"
log "matrix start: mode=$MODE suites=[$SUITES] mtus=[$MTUS] loss=[$LOSSES] reorder=[$REORDERS] rounds=$ROUNDS"
[ "$MODE" = smoke ] && log "WARNING: SMWG_E2E_COMMAND unset -> FALLBACK SMOKE CHECK (veth ping), not a tunnel."

for suite in $SUITES; do
  export WG_KEM_SUITE="$suite"
  for mtu in $MTUS; do
    for loss in $LOSSES; do
      for reorder in $REORDERS; do
        setup_cell "$mtu" "$loss" "$reorder"
        log "cell suite=$suite mtu=$mtu loss=$loss reorder=$reorder"
        for r in $(seq 1 "$ROUNDS"); do
          if [ "$MODE" = real ]; then line="$(run_real_round)"; else line="$(run_smoke_round)"; fi
          echo "$suite,$mtu,$loss,$reorder,$r,$line" >> "$SAMPLES"
        done
      done
    done
  done
done

log "matrix done -> $SAMPLES"
echo "$SAMPLES"
