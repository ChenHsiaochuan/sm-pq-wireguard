#!/bin/sh

#
# Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
#


for file in proverif-anonymity-*.log; do
    result=$(grep 'RESULT' "$file")
    name=$(basename "$file" .pv.log)
    echo "$name:"; echo "$result"
done
