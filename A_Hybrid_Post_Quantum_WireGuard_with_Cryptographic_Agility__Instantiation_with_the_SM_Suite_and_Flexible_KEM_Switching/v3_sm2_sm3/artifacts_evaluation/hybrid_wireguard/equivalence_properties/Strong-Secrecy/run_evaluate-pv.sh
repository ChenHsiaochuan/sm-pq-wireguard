#!/bin/sh

#
# Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
#

start_time=$(date +%s)

MAXJOBS=$(nproc)
MAXJOBS=$(( MAXJOBS > 8 ? MAXJOBS - 8 : 1 ))

echo "Evaluate ProVerif files"

eval $(opam env)

proverif proverif-strong-secrecy-all-dh.pv > proverif-strong-secrecy-all-dh.pv.log
proverif proverif-strong-secrecy-all-pq.pv > proverif-strong-secrecy-all-pq.pv.log
proverif proverif-strong-secrecy-no-reveal.pv > proverif-strong-secrecy-no-reveal.pv.log
proverif proverif-strong-secrecy-Psk-DH-Eic-Ri.pv > proverif-strong-secrecy-Psk-DH-Eic-Ri.pv.log
proverif proverif-strong-secrecy-Psk-DH-Eic-Srq.pv > proverif-strong-secrecy-Psk-DH-Eic-Srq.pv.log
proverif proverif-strong-secrecy-Psk-Sic-Eic-Ri.pv > proverif-strong-secrecy-Psk-Sic-Eic-Ri.pv.log
proverif proverif-strong-secrecy-Psk-Sic-Eic-Srq.pv > proverif-strong-secrecy-Psk-Sic-Eic-Srq.pv.log
proverif proverif-strong-secrecy-Psk-Src-Ri.pv > proverif-strong-secrecy-Psk-Src-Ri.pv.log
proverif proverif-strong-secrecy-Psk-Src-Srq.pv > proverif-strong-secrecy-Psk-Src-Srq.pv.log
proverif proverif-strong-secrecy-Sic-Src-Eic-Erc-Siq-Srq-Eiq-Ri-Rr-Re.pv > proverif-strong-secrecy-Sic-Src-Eic-Erc-Siq-Srq-Eiq-Ri-Rr-Re.pv.log

end_time=$(date +%s)

elapsed_time=$((end_time - start_time))

hours=$((elapsed_time / 3600))
minutes=$(((elapsed_time % 3600) / 60))
seconds=$((elapsed_time % 60))

printf "Execution time: %02d:%02d:%02d (hh:mm:ss)\n" $hours $minutes $seconds
