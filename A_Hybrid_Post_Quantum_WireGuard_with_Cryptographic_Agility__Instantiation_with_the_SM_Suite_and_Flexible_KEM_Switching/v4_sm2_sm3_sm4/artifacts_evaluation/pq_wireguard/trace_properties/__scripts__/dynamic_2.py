#!/usr/bin/env python3.6
'''
Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
'''


import os

import re

import itertools

subkeys = ["eRevKEMLtk(kemltki)", "eRevKEMLtk(kemltkr)", "eRevTpk(tpki)", "eRevTpk(tpkr)", "eRevKEMEki", "eRevRa", "eRevRb", "eRevRe", "eRevPsk"]
replacement = {"eRevKEMLtk(kemltki)": "_kemltki", "eRevKEMLtk(kemltkr)": "_kemltkr", "eRevTpk(tpki)": "_tpki", "eRevTpk(tpkr)": "_tpkr", "eRevKEMEki": "_kemeki", "eRevRa": "_ra", "eRevRb": "_rb", "eRevRe": "_re", "eRevPsk": "_psk"}

S2c = list(itertools.combinations(subkeys, 2))

result = r"RESULT(.*?)==>"
replace = ""


with open("wireguard_command_1.1log", "r") as infile:
	filedata = infile.read()
	newfiledata = re.sub(result, replace, filedata)
	with open("wireguard_command_1.lg", "w") as outfile:
		outfile.write(newfiledata)
infile.close()
outfile.close()

comb = []
with open("wireguard_command_1.lg", "r") as infile:
	for line in infile:
		for keys in subkeys:
			if ("is true" in line) and (keys in line):
				comb.append(keys)
infile.close()

#print(comb)


rep_comb = []
for event in comb:
	rep_comb.append(replacement.get(event, event))

with open("wireguard_command_2", "r") as infile, open('wireguard_command_2_opt', 'w') as outfile:
	for line in infile :
		if not any(key in line for key in rep_comb):
			outfile.write(line)


