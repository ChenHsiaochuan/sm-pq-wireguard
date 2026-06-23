#!/bin/sh

#
# Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
#

MAXJOBS=$(nproc)

eval $(opam env)

dojob()
{
	parallel --jobs $JOBS < wireguard_command_$1_opt

	mkdir resolve_simple
	python3 resolve_cannot_be_proved_simple_precise2.py
	cd resolve_simple
	if [ -f "wireguard_command" ]
	then
		parallel --jobs $MAXJOBS < wireguard_command
	fi

	rename "s/.log/.$1log/" ./*

	find . -maxdepth 1 -type f -name "*.pv" -exec cp -t ../ {} +
	find . -maxdepth 1 -type f -name "*.$1log" -exec cp -t ../ {} +

	cd ..
	mv resolve_simple resolve_simple_$1

	cat *.pv.$1log | grep "RESULT" > wireguard_command_$1.$1log
	python3 ../../__scripts__/dynamic_$2.py

	JOB2=$(wc -l < wireguard_command_$2_opt)
	JOBS=$(( $MAXJOBS < $JOB2 ? $MAXJOBS : $JOB2 ))

	if [ $JOB2 -eq 0 ] 
	then
		exit 0
	fi
}

arg1="$1"

cp __scripts__/resolve_cannot_be_proved_simple_precise2.py process_read_access/${arg1}/

cd process_read_access/${arg1}

parallel --jobs 1 < wireguard_command_0

file="wireguard_${arg1}_0.pv"
log_file="wireguard_${arg1}_0.pv.0log"
old_string="const g:bitstring."
new_string="set preciseActions = true.\nconst g:bitstring."

if grep -qE '^RESULT.*cannot be proved' "$log_file"; then
    rm "$log_file"
    sed -i "s|$old_string|$new_string|g" "$file"
    parallel --jobs 1 < wireguard_command_0
fi

cat *.pv.0log | grep "RESULT" > wireguard_command_0.0log

while IFS= read -r line; do
    if echo "$line" | grep -q "^RESULT"; then
        if echo "$line" | grep -q "is true"; then
            exit 0
        else
			JOB1=$(wc -l < wireguard_command_1)
			JOBS=$(( $MAXJOBS < $JOB1 ? $MAXJOBS : $JOB1 ))

			for num in $(seq 1 13); do
			    next_num=$((num+1))
			    dojob $num $next_num
			done
        fi
    fi
done < "wireguard_${arg1}_0.pv.0log"
