#!/bin/sh

#
# Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
#

start_time=$(date +%s)

MAXJOBS=$(nproc)

echo "Evaluate DeepSec files"

rm -f *.dps.log

deepsec -q deepsec-strong-secrecy-Psk-Ri-Ti.dps > deepsec-strong-secrecy-Psk-Ri-Ti.dps.log
deepsec -q deepsec-strong-secrecy-Psk-Srq.dps > deepsec-strong-secrecy-Psk-Srq.dps.log

sed -i 's/\x1b\[[0-9;]*[mK]//g' *.dps.log

end_time=$(date +%s)

elapsed_time=$((end_time - start_time))

hours=$((elapsed_time / 3600))
minutes=$(((elapsed_time % 3600) / 60))
seconds=$((elapsed_time % 60))

printf "Execution time: %02d:%02d:%02d (hh:mm:ss)\n" $hours $minutes $seconds
