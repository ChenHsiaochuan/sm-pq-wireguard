#!/bin/sh

start_time=$(date +%s)

JOBS=6

echo "Generate CNF and DNF, see results.cnfdnf file"

rm -f results.cnfdnf

dirs="secrecy_isk7 secrecy_isk7pfs secrecy_rsk7 secrecy_rsk7pfs secrecy_mut7 secrecy_mut7pfs \
agreement_inithello agreement_rechello agreement_confirm \
uniqueness_initiator uniqueness_responder \
unilateral_initiator unilateral_responder bilateral"

for dir in $dirs; do
  outfile="wireguard_${dir}.pv.log"

  (
    cd "process_read_access/$dir" || exit
    cat *.*log | grep "RESULT" | grep "is true" | sort -u > "$outfile"
  )
done

parallel --jobs "$JOBS" < wireguard_command_generate_cnf_dnf

end_time=$(date +%s)

elapsed_time=$((end_time - start_time))

hours=$((elapsed_time / 3600))
minutes=$(((elapsed_time % 3600) / 60))
seconds=$((elapsed_time % 60))

printf "Execution time: %02d:%02d:%02d (hh:mm:ss)\n" $hours $minutes $seconds