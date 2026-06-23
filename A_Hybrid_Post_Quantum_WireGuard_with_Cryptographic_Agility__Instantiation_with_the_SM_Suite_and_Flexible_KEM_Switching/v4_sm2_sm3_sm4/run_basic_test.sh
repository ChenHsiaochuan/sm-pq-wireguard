#!/bin/sh

tamarin-prover --version
tamarin-prover test
eval $(opam env --safe); proverif -help
deepsec -help
cargo --version

cd artifacts_evaluation
sh run_clean_all.sh

cd pq_wireguard_star/trace_properties
sh run_all.sh
grep '^CNF for' results.cnfdnf | sed 's/^CNF for //'