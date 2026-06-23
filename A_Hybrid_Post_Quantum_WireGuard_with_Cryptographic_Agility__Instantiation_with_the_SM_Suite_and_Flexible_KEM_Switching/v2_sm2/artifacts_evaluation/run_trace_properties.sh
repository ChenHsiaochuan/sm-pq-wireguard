#!/bin/sh

#
# Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
#


cd wireguard_with_fix_psk/trace_properties
sh run_all.sh
echo "CNFs for trace properties for WireGuard with fix for anonymity based on psk"
grep '^CNF for' results.cnfdnf | sed 's/^CNF for //'

cd ../../pq_wireguard/trace_properties
sh run_all.sh
echo "CNFs for trace properties for PQ-WireGuard"
grep '^CNF for' results.cnfdnf | sed 's/^CNF for //'

cd ../../pq_wireguard_star/trace_properties
sh run_all.sh
echo "CNFs for trace properties for PQ-WireGuard*"
grep '^CNF for' results.cnfdnf | sed 's/^CNF for //'

cd ../../hybrid_wireguard/trace_properties_sufficient_conditions
sh run_all.sh
cd ../trace_properties_necessary_conditions
sh run_all.sh
echo "CNFs for trace properties for Hybrid-WireGuard"
grep '^CNF for' results.cnfdnf | sed 's/^CNF for //'
