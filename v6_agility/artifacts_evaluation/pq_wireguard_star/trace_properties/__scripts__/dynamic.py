#!/usr/bin/env python3.6
'''
Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
'''


import os

#import itertools

subkeys = ["kemltki", "kemltkr", "tpki", "tpkr", "kempeki", "ra", "rb", "psk"]


with open("wireguard_command_1.log", "r") as infile:
	filedata = infile.read()
	filedata = filedata.replace("RESULT event(eI_SK7(ck_2,kemltki,kemltkr,kempeki,psk_4,tpki,ka_2,k_2,kb_2,ra_2))@i && attacker(ck_2)@j ==>", "")
	with open("wireguard_command_1.lg", "w") as outfile:
		outfile.write(filedata)
infile.close()
outfile.close()
comb = []

with open("wireguard_command_1.lg", "r") as infile:
	for line in infile:
		for keys in subkeys:
			if ("is true" in line) and (keys in line):
				comb.append(keys)
infile.close()


with open("wireguard_command_2", "r") as infile, open('wireguard_command_2_opt', 'w') as outfile:
	for line in infile :
		if not any(key in line for key in comb):
			outfile.write(line)

