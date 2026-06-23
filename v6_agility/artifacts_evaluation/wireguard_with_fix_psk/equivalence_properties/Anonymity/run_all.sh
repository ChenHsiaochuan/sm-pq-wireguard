#!/bin/sh

#
# Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
#

start_time=$(date +%s)

echo "Evaluate ProVerif files"

eval $(opam env)

proverif proverif-anonymity-initiator-Eic.pv > proverif-anonymity-initiator-Eic.log
proverif proverif-anonymity-initiator-Erc-Sic.pv > proverif-anonymity-initiator-Erc-Sic.pv.log
proverif proverif-anonymity-initiator-no-reveal.pv > proverif-anonymity-initiator-no-reveal.pv.log
proverif proverif-anonymity-initiator-Psk.pv > proverif-anonymity-initiator-Psk.pv.log
proverif proverif-anonymity-initiator-Src.pv > proverif-anonymity-initiator-Src.pv.log                
proverif proverif-anonymity-responder-Eic.pv > proverif-anonymity-responder-Eic.pv.log                
proverif proverif-anonymity-responder-Erc-Sic.pv > proverif-anonymity-responder-Erc-Sic.log                
proverif proverif-anonymity-responder-no-reveal.pv > proverif-anonymity-responder-no-reveal.log        
proverif proverif-anonymity-responder-Psk.pv > proverif-anonymity-responder-Psk.pv.log
proverif proverif-anonymity-responder-Src.pv > proverif-anonymity-responder-Src.pv.log

end_time=$(date +%s)

elapsed_time=$((end_time - start_time))

hours=$((elapsed_time / 3600))
minutes=$(((elapsed_time % 3600) / 60))
seconds=$((elapsed_time % 60))

printf "Execution time: %02d:%02d:%02d (hh:mm:ss)\n" $hours $minutes $seconds
