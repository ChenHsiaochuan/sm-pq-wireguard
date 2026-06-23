#!/bin/sh

#
# Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
#

start_time=$(date +%s)

echo "Generate Tamarin Files"

dirs="secrecy_isk7 secrecy_isk7pfs agreement_inithello agreement_rechello agreement_confirm"
dirs_h="secrecy_rsk7 secrecy_rsk7pfs secrecy_mul7 secrecy_mul7pfs agreement_confirm"
diruniqueness_initiator="uniqueness_initiator"
diruniqueness_responder="uniqueness_responder"
files="wireguard_secrecy_isk7.spthy wireguard_secrecy_rsk7.spthy wireguard_secrecy_mut7.spthy wireguard_agreement_inithello.spthy wireguard_agreement_rechello.spthy wireguard_agreement_confirm.spthy wireguard_uniqueness_initiator.spthy wireguard_uniqueness_responder.spthy"


intro="process_empty/wireguard_intro.spthy"
intro_h="process_empty/wireguard_intro_h.spthy"
initiator="wireguard_peer_initiator_reference.spthy" 
responder="wireguard_peer_responder_reference.spthy" 
process="wireguard_process_reference.spthy"
end="process_empty/wireguard_end.spthy"

rm -R -f tamarin

mkdir tamarin


for dir in $dirs; do

	file_path="tamarin/wireguard_${dir}.spthy"
	python3 __scripts__/generate_tam_${dir}.py
	lemma="${dir}.lemma"

    cat "$intro" > "$file_path"
    cat "$initiator" >> "$file_path"
    cat "$responder" >> "$file_path"
    cat "$process" >> "$file_path"
    cat "$lemma" >> "$file_path"
    cat "$end" >> "$file_path"

done


for dir in $dirs_h; do

    file_path="tamarin/wireguard_${dir}.spthy"
    python3 __scripts__/generate_tam_${dir}.py
    lemma="${dir}.lemma"

    cat "$intro_h" > "$file_path"
    cat "$initiator" >> "$file_path"
    cat "$responder" >> "$file_path"
    cat "$process" >> "$file_path"
    cat "$lemma" >> "$file_path"
    cat "$end" >> "$file_path"

done



for dir in $diruniqueness_initiator; do

    file_path="tamarin/wireguard_${dir}.spthy"
    cat "$intro" > "$file_path"
    cat "$initiator" >> "$file_path"
    cat "$responder" >> "$file_path"
    cat "$process" >> "$file_path"
    echo "lemma Uniqueness_Initiator:\nall-traces\n\"\nAll #i ldhi ldhr dheki dhekr psk ck.\n(IConfirm(ck, ldhi, ldhr, dheki, dhekr, psk)@i) ==> not(Ex dheki2 dhekr2 #j1. (IConfirm(ck, ldhi, ldhr, dheki2, dhekr2, psk)@j1) & not(#j1 = #i))\n\"\n" >> "$file_path"
    cat "$end" >> "$file_path"

done

for dir in $diruniqueness_responder; do

    file_path="tamarin/wireguard_${dir}.spthy"
    cat "$intro" > "$file_path"
    cat "$initiator" >> "$file_path"
    cat "$responder" >> "$file_path"
    cat "$process" >> "$file_path"
    echo "lemma Uniqueness_Responder:\nall-traces\n\"\nAll #i ldhi ldhr dheki dhekr psk ck.\n(RConfirm(ck, ldhi, ldhr, dheki, dhekr, psk)@i) ==> not(Ex dheki2 dhekr2 #j1. (RConfirm(ck, ldhi, ldhr, dheki2, dhekr2, psk)@j1) & not(#j1 = #i))\n\"\n" >> "$file_path"
    cat "$end" >> "$file_path"

done


rm -f *.lemma
rm -f *.cnf
rm -f *.dnf

end_time=$(date +%s)

elapsed_time=$((end_time - start_time))

hours=$((elapsed_time / 3600))
minutes=$(((elapsed_time % 3600) / 60))
seconds=$((elapsed_time % 60))

printf "Execution time: %02d:%02d:%02d (hh:mm:ss)\n" $hours $minutes $seconds