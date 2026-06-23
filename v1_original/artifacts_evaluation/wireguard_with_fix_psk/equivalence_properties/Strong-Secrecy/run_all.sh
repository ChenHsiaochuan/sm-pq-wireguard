#!/bin/sh

#
# Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
#

start_time=$(date +%s)

echo "Evaluate ProVerif files"

eval $(opam env)

proverif proverif-strong-secrecy-Psk-DH-Eic.pv > proverif-strong-secrecy-Psk-DH-Eic.pv.log
proverif proverif-strong-secrecy-Psk-Eic-Erc.pv > proverif-strong-secrecy-Psk-Eic-Erc.pv.log
proverif proverif-strong-secrecy-Psk-Sic-Eic.pv > proverif-strong-secrecy-Psk-Sic-Eic.pv.log
proverif proverif-strong-secrecy-Psk-Sic-Erc.pv > proverif-strong-secrecy-Psk-Sic-Erc.pv.log
proverif proverif-strong-secrecy-Psk-Src.pv > proverif-strong-secrecy-Psk-Src.pv.log
proverif proverif-strong-secrecy-Sic-Src-Eic-Erc.pv > proverif-strong-secrecy-Sic-Src-Eic-Erc.pv.log

end_time=$(date +%s)

elapsed_time=$((end_time - start_time))

hours=$((elapsed_time / 3600))
minutes=$(((elapsed_time % 3600) / 60))
seconds=$((elapsed_time % 60))

printf "Execution time: %02d:%02d:%02d (hh:mm:ss)\n" $hours $minutes $seconds
