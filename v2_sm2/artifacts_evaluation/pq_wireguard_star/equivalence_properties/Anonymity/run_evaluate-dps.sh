#!/bin/sh

#
# Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
#

start_time=$(date +%s)

MAXJOBS=$(nproc)

echo "Evaluate DeepSec files"

rm -f *.dps.log

deepsec -q deepsec-anonymity-initiator-Psk.dps > deepsec-anonymity-initiator-Psk.dps.log
deepsec -q deepsec-anonymity-initiator-Ri.dps > deepsec-anonymity-initiator-Ri.dps.log
deepsec -q deepsec-anonymity-initiator-Rr.dps > deepsec-anonymity-initiator-Rr.dps.log
deepsec -q deepsec-anonymity-initiator-Siq.dps > deepsec-anonymity-initiator-Siq.dps.log
deepsec -q deepsec-anonymity-initiator-Srq.dps > deepsec-anonymity-initiator-Srq.dps.log
deepsec -q deepsec-anonymity-responder-Psk.dps > deepsec-anonymity-responder-Psk.dps.log
deepsec -q deepsec-anonymity-responder-Ri.dps > deepsec-anonymity-responder-Ri.dps.log
deepsec -q deepsec-anonymity-responder-Srq.dps > deepsec-anonymity-responder-Srq.dps.log

sed -i 's/\x1b\[[0-9;]*[mK]//g' *.dps.log

end_time=$(date +%s)

elapsed_time=$((end_time - start_time))

hours=$((elapsed_time / 3600))
minutes=$(((elapsed_time % 3600) / 60))
seconds=$((elapsed_time % 60))

printf "Execution time: %02d:%02d:%02d (hh:mm:ss)\n" $hours $minutes $seconds
