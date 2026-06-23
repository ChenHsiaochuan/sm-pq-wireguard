#!/bin/sh

#
# Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
#

start_time=$(date +%s)

echo "Evaluate Tamarin files"

tamarin-prover --derivcheck-timeout=0 tamarin/wireguard_uniqueness_initiator.spthy  --prove > tamarin/wireguard_uniqueness_initiator.spthy.log 2> /dev/null
tamarin-prover --derivcheck-timeout=0 tamarin/wireguard_uniqueness_responder.spthy  --prove > tamarin/wireguard_uniqueness_responder.spthy.log 2> /dev/null
tamarin-prover --derivcheck-timeout=0 tamarin/wireguard_agreement_inithello.spthy  --prove > tamarin/wireguard_agreement_inithello.spthy.log 2> /dev/null
tamarin-prover --derivcheck-timeout=0 tamarin/wireguard_agreement_rechello.spthy  --prove > tamarin/wireguard_agreement_rechello.spthy.log 2> /dev/null
tamarin-prover --derivcheck-timeout=0 tamarin/wireguard_agreement_confirm.spthy  --prove > tamarin/wireguard_agreement_confirm.spthy.log 2> /dev/null
tamarin-prover --derivcheck-timeout=0 tamarin/wireguard_secrecy_isk7.spthy  --prove > tamarin/wireguard_secrecy_isk7.spthy.log 2> /dev/null
tamarin-prover --derivcheck-timeout=0 tamarin/wireguard_secrecy_rsk7.spthy  --prove > tamarin/wireguard_secrecy_rsk7.spthy.log 2> /dev/null
tamarin-prover --derivcheck-timeout=0 tamarin/wireguard_secrecy_mul7.spthy  --prove > tamarin/wireguard_secrecy_mul7.spthy.log 2> /dev/null
tamarin-prover --derivcheck-timeout=0 tamarin/wireguard_secrecy_isk7pfs.spthy  --prove > tamarin/wireguard_secrecy_isk7pfs.spthy.log 2> /dev/null
tamarin-prover --derivcheck-timeout=0 tamarin/wireguard_secrecy_rsk7pfs.spthy  --prove > tamarin/wireguard_secrecy_rsk7pfs.spthy.log 2> /dev/null
tamarin-prover --derivcheck-timeout=0 tamarin/wireguard_secrecy_mul7pfs.spthy  --prove > tamarin/wireguard_secrecy_mul7pfs.spthy.log 2> /dev/null

end_time=$(date +%s)

elapsed_time=$((end_time - start_time))

hours=$((elapsed_time / 3600))
minutes=$(((elapsed_time % 3600) / 60))
seconds=$((elapsed_time % 60))

printf "Execution time: %02d:%02d:%02d (hh:mm:ss)\n" $hours $minutes $seconds
