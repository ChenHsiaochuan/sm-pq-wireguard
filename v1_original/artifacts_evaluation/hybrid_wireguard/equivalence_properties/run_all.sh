#!/bin/sh

#
# Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
#

sh run_clean.sh

cd Anonymity
sh run_evaluate-pv.sh

cd ../Strong-Secrecy
sh run_evaluate-pv.sh

cd ..

