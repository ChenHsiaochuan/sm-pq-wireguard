#!/bin/sh

#
# Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
#


cd wireguard_with_fix_psk/equivalence_properties/Strong-Secrecy
sh run_all.sh

cd ../../../pq_wireguard/equivalence_properties/Strong-Secrecy
sh run_all.sh

cd ../../../pq_wireguard_star/equivalence_properties/Strong-Secrecy
sh run_all.sh

cd ../../../hybrid_wireguard/equivalence_properties/Strong-Secrecy
sh run_all.sh
