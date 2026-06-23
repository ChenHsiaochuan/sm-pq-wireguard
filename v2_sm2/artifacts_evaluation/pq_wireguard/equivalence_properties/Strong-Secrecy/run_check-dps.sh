#!/bin/sh

#
# Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
#


for file in deepsec-strong-secrecy-*.log; do 
    result=$(grep 'Result' "$file" | sed -E 's/Result query [0-9]+: //; s/Verified in.*//') name=$(basename "$file" .dps.log)
    echo "$name:"; echo "$result" 
done
