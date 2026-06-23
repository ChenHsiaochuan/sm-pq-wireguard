#!/bin/sh

#
# Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
#

start_time=$(date +%s)

echo "Generate ProVerif files for adversary with 'write' access to cryptographic keys"

dirs="secrecy_isk7 secrecy_rsk7 secrecy_mut7 agreement_inithello agreement_rechello agreement_confirm uniqueness_initiator uniqueness_responder unilateral_initiator unilateral_responder bilateral"
files="wireguard_secrecy_isk7.spthy wireguard_secrecy_rsk7.spthy wireguard_secrecy_mut7.spthy wireguard_agreement_inithello.spthy wireguard_agreement_rechello.spthy wireguard_agreement_confirm.spthy wireguard_uniqueness_initiator.spthy wireguard_uniqueness_responder.spthy wireguard_unilateral_initiator.spthy wireguard_unilateral_responder.spthy wireguard_bilateral.spthy"


intro="process_empty/wireguard_intro.spthy"
initiator="wireguard_peer_initiator_m_reference.spthy" 
responder="wireguard_peer_responder_m_reference.spthy" 
process="wireguard_process_m_reference.spthy"
exportbegin="process_empty/wireguard_export_queries_begin.spthy"

noselect="noselect x:bitstring; attacker(exp(g,x))."
queryintro="query ldhi:bitstring, ldhr:bitstring, dheki:bitstring, dhekr:bitstring, psk:bitstring, ldhi':bitstring, ldhr':bitstring, dheki':bitstring, dhekr':bitstring, psk':bitstring, ck:bitstring;"

query_secrecy_isk7="event(eI_SK7(ck, ldhi, ldhr, dheki, dhekr, psk)) && attacker(ck)."
query_secrecy_rsk7="event(eR_SK7(ck, ldhi, ldhr, dheki, dhekr, psk)) && attacker(ck)."
query_secrecy_mut7="event(eRConfirm(ck, ldhi, ldhr, dheki, dhekr, psk)) && event(eIConfirm(ck, ldhi, ldhr, dheki, dhekr, psk)) && attacker(ck)."
query_agreement_inithello="event(eRRec(ck, ldhi, ldhr, dheki)) ==> event(eISend(ck, ldhi, ldhr, dheki))."
query_agreement_rechello="event(eIKeys(ck, ldhi, ldhr, dheki, dhekr, psk)) ==> event(eRKeys(ck, ldhi, ldhr, dheki, dhekr, psk))."
query_agreement_confirm="event(eRConfirm(ck, ldhi, ldhr, dheki, dhekr, psk)) ==> event(eIConfirm(ck, ldhi, ldhr, dheki, dhekr, psk))."
query_uniqueness_initiator="event(eIConfirm(ck, ldhi, ldhr, dheki, dhekr, psk)) && event(eIConfirm(ck, ldhi, ldhr, dheki', dhekr', psk)) ==> ((dheki = dheki') && (dhekr = dhekr'))."
query_uniqueness_responder="event(eRConfirm(ck, ldhi, ldhr, dheki, dhekr, psk)) && event(eRConfirm(ck, ldhi, ldhr, dheki', dhekr', psk)) ==> ((dheki = dheki') && (dhekr = dhekr'))."
query_unilateral_initiator="event(eRConfirm(ck, ldhi, ldhr, dheki, dhekr, psk)) && event(eIConfirm(ck, ldhi, ldhr', dheki', dhekr', psk')) ==> (ldhr = ldhr')."
query_unilateral_responder="event(eRConfirm(ck, ldhi, ldhr, dheki, dhekr, psk)) && event(eIConfirm(ck, ldhi', ldhr, dheki', dhekr', psk')) ==> (ldhi = ldhi')."
query_bilateral="event(eRConfirm(ck, ldhi, ldhr, dheki, dhekr, psk)) && event(eIConfirm(ck, ldhi', ldhr', dheki', dhekr', psk')) ==> ((ldhi = ldhi') && (ldhr = ldhr'))."


exportend="process_empty/wireguard_export_queries_end.spthy"

end="process_empty/wireguard_end.spthy"

rm -R -f process_write_access

mkdir process_write_access

index=0
for dir in $dirs; do
    file=$(echo $files | cut -d ' ' -f $((index + 1)))
    index=$((index + 1))

    # Create necessary directories
    mkdir -p "process_write_access/$dir/log"
    mkdir -p "process_write_access/$dir/pv"
    mkdir -p "process_write_access/$dir/spthy"

    file_path="process_write_access/$dir/$file"

    # Start creating the file
    cat "$intro" > "$file_path"
    cat "$initiator" >> "$file_path"
    cat "$responder" >> "$file_path"
    cat "$process" >> "$file_path"
    cat "$exportbegin" >> "$file_path"

    echo "$noselect" >> "$file_path"
    echo "$queryintro" >> "$file_path"

    case "$dir" in
        secrecy_isk7) echo "$query_secrecy_isk7" >> "$file_path" ;;
        secrecy_rsk7) echo "$query_secrecy_rsk7" >> "$file_path" ;;
        secrecy_mut7) echo "$query_secrecy_mut7" >> "$file_path" ;;
        agreement_inithello) echo "$query_agreement_inithello" >> "$file_path" ;;
        agreement_rechello) echo "$query_agreement_rechello" >> "$file_path" ;;
        agreement_confirm) echo "$query_agreement_confirm" >> "$file_path" ;;
        uniqueness_initiator) echo "$query_uniqueness_initiator" >> "$file_path" ;;
        uniqueness_responder) echo "$query_uniqueness_responder" >> "$file_path" ;;
        unilateral_initiator) echo "$query_unilateral_initiator" >> "$file_path" ;;
        unilateral_responder) echo "$query_unilateral_responder" >> "$file_path" ;;
        bilateral) echo "$query_bilateral" >> "$file_path" ;;
        *)
            echo "Unknown directory: $dir"
            ;;
    esac

    cat "$exportend" >> "$file_path"
    cat "$end" >> "$file_path"
done

end_time=$(date +%s)

elapsed_time=$((end_time - start_time))

hours=$((elapsed_time / 3600))
minutes=$(((elapsed_time % 3600) / 60))
seconds=$((elapsed_time % 60))

printf "Execution time: %02d:%02d:%02d (hh:mm:ss)\n" $hours $minutes $seconds