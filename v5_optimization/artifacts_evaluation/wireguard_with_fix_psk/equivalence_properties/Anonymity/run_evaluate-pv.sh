#!/bin/sh

#
# Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
#

start_time=$(date +%s)

MAXJOBS=$(nproc)
MAXJOBS=$(( MAXJOBS > 8 ? MAXJOBS - 8 : 1 ))

eval $(opam env)

echo "Evaluate ProVerif files"

parallel --jobs $MAXJOBS < wireguard_command_evaluate_pv

end_time=$(date +%s)

elapsed_time=$((end_time - start_time))

hours=$((elapsed_time / 3600))
minutes=$(((elapsed_time % 3600) / 60))
seconds=$((elapsed_time % 60))

printf "Execution time: %02d:%02d:%02d (hh:mm:ss)\n" $hours $minutes $seconds
