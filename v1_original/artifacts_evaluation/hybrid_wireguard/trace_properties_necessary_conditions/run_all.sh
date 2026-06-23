#!/bin/sh

#
# Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
#

sh run_clean.sh
sh run_generate-pv.sh
sh run_evaluate-pv.sh
sh run_generate-spthy-m.sh
sh run_evaluate-pv-m.sh
sh run_generate-cnf-dnf.sh
sh run_evaluate-tam.sh