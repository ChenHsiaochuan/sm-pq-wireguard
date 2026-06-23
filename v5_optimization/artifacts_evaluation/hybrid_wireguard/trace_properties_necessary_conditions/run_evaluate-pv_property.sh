#!/bin/sh

MAXJOBS=$(nproc)

arg1="$1"

python3 filtercommand_$1.py

eval $(opam env)

cp __scripts__/resolve_cannot_be_proved_simple_precise.py process_read_access/${arg1}/
cp __scripts__/resolve_cannot_be_proved_global_precise.py process_read_access/${arg1}/


cd process_read_access/${arg1}

JOB1=$(wc -l < wireguard_command_filtered)
JOBS=$(( $MAXJOBS < $JOB1 ? $MAXJOBS : $JOB1 ))

parallel --jobs $JOBS < wireguard_command_filtered

mkdir resolve_simple
python3 resolve_cannot_be_proved_simple_precise.py
cp resolve_cannot_be_proved_global_precise.py resolve_simple/
cd resolve_simple
#echo "Resolve cannot be proved queries with precise"
if [ -f "wireguard_command" ]
then
	parallel --jobs $MAXJOBS < wireguard_command
fi

mkdir resolve_global
python3 resolve_cannot_be_proved_global_precise.py

cd resolve_global
#echo "Resolve cannot be proved queries with global precise"
if [ -f "wireguard_command" ]
then
	parallel --jobs $MAXJOBS < wireguard_command
fi


find . -maxdepth 1 -type f -name "*.pv" -exec cp -t ../ {} +
find . -maxdepth 1 -type f -name "*.log" -exec cp -t ../ {} +

cd ..

rename "s/.log/.$1log/" ./*

find . -maxdepth 1 -type f -name "*.pv" -exec cp -t ../ {} +
find . -maxdepth 1 -type f -name "*.$1log" -exec cp -t ../ {} +

cd ..


