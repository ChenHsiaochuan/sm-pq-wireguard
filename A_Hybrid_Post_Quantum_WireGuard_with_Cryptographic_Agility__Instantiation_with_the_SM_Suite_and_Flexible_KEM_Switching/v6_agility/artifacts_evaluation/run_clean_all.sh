#!/bin/sh

cd hybrid_wireguard/equivalence_properties
sh run_clean.sh
cd ../trace_properties_necessary_conditions
sh run_clean.sh
cd ../trace_properties_sufficient_conditions
sh run_clean.sh

cd ../../pq_wireguard/equivalence_properties
sh run_clean.sh
cd ../trace_properties
sh run_clean.sh

cd ../../pq_wireguard_star/equivalence_properties
sh run_clean.sh
cd ../trace_properties
sh run_clean.sh

cd ../../wireguard_with_fix_psk/equivalence_properties
sh run_clean.sh
cd ../trace_properties
sh run_clean.sh
