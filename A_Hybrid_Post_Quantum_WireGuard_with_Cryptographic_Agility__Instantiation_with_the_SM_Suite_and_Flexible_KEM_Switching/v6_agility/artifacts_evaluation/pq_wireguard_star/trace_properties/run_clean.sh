#!/bin/sh

#
# Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
#

cd queries

rm -f *.spthy

cd ..

rm -Rf process_read_access
rm -Rf process_write_access
rm -Rf tamarin

rm -Rf __scripts__/__pycache__


rm -f *.lemma
rm -f *.cnf
rm -f *.dnf
rm -f results.cnfdnf

