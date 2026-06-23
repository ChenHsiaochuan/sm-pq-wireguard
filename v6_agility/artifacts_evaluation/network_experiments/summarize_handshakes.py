#!/usr/bin/env python3
"""
summarize_handshakes.py -- reduce raw full-tunnel handshake samples to a
per-cell success-rate / latency-percentile table.

Input  (handshake_samples.csv), one row per handshake attempt:
    suite,mtu,loss_pct,reorder_pct,round,status,handshake_ms
        status      : ok | timeout | loss | crash | auth_fail | error
        handshake_ms: wall-clock ms to a completed tunnel handshake; blank for
                      any non-"ok" status.

Output (handshake_summary.csv), one row per (suite,mtu,loss,reorder) cell:
    suite,mtu,loss_pct,reorder_pct,rounds,successes,success_rate,
    p50_ms,p95_ms,p99_ms,fail_timeout,fail_loss,fail_crash,fail_auth,fail_other

Percentiles are computed over the SUCCESSFUL handshakes only (nearest-rank,
the same convention the paper's latency tables use). A cell with zero
successes reports blank percentiles and a 0.0 success rate -- it is never
silently dropped.

Usage:
    summarize_handshakes.py results/full_tunnel/handshake_samples.csv \
        > results/full_tunnel/handshake_summary.csv
    # or read stdin:
    cat samples.csv | summarize_handshakes.py
"""
import csv
import sys
from collections import defaultdict


def nearest_rank(sorted_vals, pct):
    """Nearest-rank percentile (pct in [0,100]); sorted_vals non-empty."""
    if not sorted_vals:
        return None
    import math
    k = max(1, math.ceil(pct / 100.0 * len(sorted_vals)))
    return sorted_vals[k - 1]


def main(argv):
    src = open(argv[1], newline="") if len(argv) > 1 and argv[1] != "-" else sys.stdin
    reader = csv.DictReader(src)
    required = {"suite", "mtu", "loss_pct", "reorder_pct", "status"}
    if reader.fieldnames is None or not required.issubset(set(reader.fieldnames)):
        sys.exit("input is missing required columns: %s" % sorted(required))

    cells = defaultdict(lambda: {"lat": [], "n": 0,
                                 "timeout": 0, "loss": 0, "crash": 0,
                                 "auth_fail": 0, "other": 0, "ok": 0})
    for row in reader:
        key = (row["suite"], row["mtu"], row["loss_pct"], row["reorder_pct"])
        c = cells[key]
        c["n"] += 1
        status = (row.get("status") or "").strip().lower()
        if status == "ok":
            c["ok"] += 1
            raw = (row.get("handshake_ms") or "").strip()
            if raw:
                try:
                    c["lat"].append(float(raw))
                except ValueError:
                    pass
        elif status in ("timeout", "loss", "crash", "auth_fail"):
            c[status] += 1
        else:
            c["other"] += 1

    w = csv.writer(sys.stdout)
    w.writerow(["suite", "mtu", "loss_pct", "reorder_pct", "rounds",
                "successes", "success_rate", "p50_ms", "p95_ms", "p99_ms",
                "fail_timeout", "fail_loss", "fail_crash", "fail_auth",
                "fail_other"])
    for key in sorted(cells):
        suite, mtu, loss, reorder = key
        c = cells[key]
        lat = sorted(c["lat"])
        n, ok = c["n"], c["ok"]
        rate = (ok / n) if n else 0.0

        def fmt(v):
            return "%.3f" % v if v is not None else ""

        w.writerow([suite, mtu, loss, reorder, n, ok, "%.4f" % rate,
                    fmt(nearest_rank(lat, 50)),
                    fmt(nearest_rank(lat, 95)),
                    fmt(nearest_rank(lat, 99)),
                    c["timeout"], c["loss"], c["crash"], c["auth_fail"],
                    c["other"]])

    if src is not sys.stdin:
        src.close()


if __name__ == "__main__":
    main(sys.argv)
