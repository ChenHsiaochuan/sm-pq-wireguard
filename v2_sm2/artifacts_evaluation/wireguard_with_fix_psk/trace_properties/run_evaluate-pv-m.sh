#!/bin/sh

#
# Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
#


start_time=$(date +%s)

JOBS=$(nproc)

echo "Evaluate ProVerif files for adversary with 'write' access to cryptographic keys"

cd process_write_access

dirs="secrecy_isk7 secrecy_rsk7 secrecy_mut7 agreement_inithello agreement_rechello agreement_confirm uniqueness_initiator uniqueness_responder unilateral_initiator unilateral_responder bilateral"

for dir in $dirs; do
  rm -f "$dir/log/*" "$dir/pv/*" "$dir/spthy/*"
done

cd ..

for dir in $dirs; do
	python3 __scripts__/evaluate_m_models_property.py ${dir}
	cd process_write_access/${dir}/pv
	eval $(opam env)
	parallel --jobs $JOBS < wireguard_command &
	cd ../../../
done

wait

end_time=$(date +%s)

elapsed_time=$((end_time - start_time))

hours=$((elapsed_time / 3600))
minutes=$(((elapsed_time % 3600) / 60))
seconds=$((elapsed_time % 60))

printf "Execution time: %02d:%02d:%02d (hh:mm:ss)\n" $hours $minutes $seconds