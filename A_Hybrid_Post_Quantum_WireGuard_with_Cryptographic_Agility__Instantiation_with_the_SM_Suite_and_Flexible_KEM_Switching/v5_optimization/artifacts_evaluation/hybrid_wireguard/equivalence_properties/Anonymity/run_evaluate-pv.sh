#!/bin/sh

#
# Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
#

start_time=$(date +%s)

MAXJOBS=$(nproc)
MAXJOBS=$(( MAXJOBS > 8 ? MAXJOBS - 8 : 1 ))

echo "Evaluate ProVerif files"

eval $(opam env)

proverif proverif-anonymity-responder-all-dh.pv > proverif-anonymity-responder-all-dh.pv.log
proverif proverif-anonymity-responder-all-pq.pv > proverif-anonymity-responder-all-pq.pv.log
proverif proverif-anonymity-responder-no-reveal.pv > proverif-anonymity-responder-no-reveal.pv.log
proverif proverif-anonymity-responder-Src-Srq.pv > proverif-anonymity-responder-Src-Srq.pv.log
proverif proverif-anonymity-responder-Srq-Eic.pv > proverif-anonymity-responder-Srq-Eic.pv.log
proverif proverif-anonymity-initiator-no-reveal.pv > proverif-anonymity-initiator-no-reveal.pv.log
proverif proverif-anonymity-responder-Eic-Ri.pv > proverif-anonymity-responder-Eic-Ri.pv.log
proverif proverif-anonymity-responder-Psk.pv > proverif-anonymity-responder-Psk.pv.log
proverif proverif-anonymity-responder-Sic-Erc-Siq-Srq-Eiq-Ri-Rr-Re.pv > proverif-anonymity-responder-Sic-Erc-Siq-Srq-Eiq-Ri-Rr-Re.pv.log
proverif proverif-anonymity-responder-Sic-Src-Eic-Erc-Siq-Eiq-Rr-Re.pv > proverif-anonymity-responder-Sic-Src-Eic-Erc-Siq-Eiq-Rr-Re.pv.log
proverif proverif-anonymity-responder-Src-Ri.pv > proverif-anonymity-responder-Src-Ri.pv.log
proverif proverif-anonymity-initiator-all-dh.pv > proverif-anonymity-initiator-all-dh.pv.log
proverif proverif-anonymity-initiator-all-pq.pv > proverif-anonymity-initiator-all-pq.pv.log
proverif proverif-anonymity-initiator-Sic-Siq.pv > proverif-anonymity-initiator-Sic-Siq.pv.log
proverif proverif-anonymity-initiator-Sic-Src-Eic-Erc-Eiq-Re.pv > proverif-anonymity-initiator-Sic-Src-Eic-Erc-Eiq-Re.pv.log
proverif proverif-anonymity-initiator-Src-Eic-Siq-Eiq-Rr-Re.pv > proverif-anonymity-initiator-Src-Eic-Siq-Eiq-Rr-Re.pv.log
proverif proverif-anonymity-initiator-Src-Ri.pv > proverif-anonymity-initiator-Src-Ri.pv.log
proverif proverif-anonymity-initiator-Src-Srq.pv > proverif-anonymity-initiator-Src-Srq.pv.log
proverif proverif-anonymity-initiator-Erc-Siq.pv > proverif-anonymity-initiator-Erc-Siq.pv.log
proverif proverif-anonymity-initiator-Psk.pv > proverif-anonymity-initiator-Psk.pv.log
proverif proverif-anonymity-initiator-Sic-Erc-Srq-Eiq-Ri-Re.pv > proverif-anonymity-initiator-Sic-Erc-Srq-Eiq-Ri-Re.pv.log
proverif proverif-anonymity-initiator-Sic-Rr.pv > proverif-anonymity-initiator-Sic-Rr.pv.log
proverif proverif-anonymity-initiator-Eic-Ri.pv > proverif-anonymity-initiator-Eic-Ri.pv.log
proverif proverif-anonymity-initiator-Eic-Srq.pv > proverif-anonymity-initiator-Eic-Srq.pv.log
proverif proverif-anonymity-initiator-Erc-Rr.pv > proverif-anonymity-initiator-Erc-Rr.pv

end_time=$(date +%s)

elapsed_time=$((end_time - start_time))

hours=$((elapsed_time / 3600))
minutes=$(((elapsed_time % 3600) / 60))
seconds=$((elapsed_time % 60))

printf "Execution time: %02d:%02d:%02d (hh:mm:ss)\n" $hours $minutes $seconds
