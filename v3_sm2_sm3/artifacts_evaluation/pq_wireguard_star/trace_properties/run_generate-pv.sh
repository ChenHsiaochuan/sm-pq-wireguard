#!/bin/sh

#
# Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
#

start_time=$(date +%s)

echo "Generate ProVerif files for adversary with 'read' access to cryptographic keys"

JOBS=6

mkdir process_read_access

python3 __scripts__/generate_macro_5.py

python3 __scripts__/generate_macro_u.py

cd queries

sh run_generate-export-queries.sh

cd ..

parallel --jobs $JOBS < wireguard_command_generate_pv

rm -f wireguard_macro.spthy
rm -f wireguard_macro_u.spthy

end_time=$(date +%s)

elapsed_time=$((end_time - start_time))

hours=$((elapsed_time / 3600))
minutes=$(((elapsed_time % 3600) / 60))
seconds=$((elapsed_time % 60))

printf "Execution time: %02d:%02d:%02d (hh:mm:ss)\n" $hours $minutes $seconds