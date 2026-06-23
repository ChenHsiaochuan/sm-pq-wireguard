#!/bin/sh

#
# Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
#

start_time=$(date +%s)

eval $(opam env)

echo "Evaluate ProVerif files for adversary with 'read' access to cryptographic keys"

sh run_evaluate-pv_property.sh uniqueness_initiator &
sh run_evaluate-pv_property.sh uniqueness_responder &
sh run_evaluate-pv_property.sh unilateral_initiator &
sh run_evaluate-pv_property.sh unilateral_responder &
sh run_evaluate-pv_property.sh bilateral &
sh run_evaluate-pv_property.sh secrecy_isk7 &
sh run_evaluate-pv_property.sh secrecy_rsk7 &
sh run_evaluate-pv_property.sh secrecy_mut7 &
sh run_evaluate-pv_property.sh agreement_inithello &
sh run_evaluate-pv_property.sh agreement_rechello &
sh run_evaluate-pv_property.sh agreement_confirm &
sh run_evaluate-pv_property.sh secrecy_isk7pfs &
sh run_evaluate-pv_property.sh secrecy_rsk7pfs &
sh run_evaluate-pv_property.sh secrecy_mut7pfs &
wait

end_time=$(date +%s)

elapsed_time=$((end_time - start_time))

hours=$((elapsed_time / 3600))
minutes=$(((elapsed_time % 3600) / 60))
seconds=$((elapsed_time % 60))

printf "Execution time: %02d:%02d:%02d (hh:mm:ss)\n" $hours $minutes $seconds