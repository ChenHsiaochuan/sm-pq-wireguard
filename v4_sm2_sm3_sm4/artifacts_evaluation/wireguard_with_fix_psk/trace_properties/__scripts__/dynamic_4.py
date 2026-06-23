#!/usr/bin/env python3.6
'''
Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
'''


import os

import re

import itertools

subkeys = ["eRevLDH(ldhi)", "eRevLDH(ldhr)", "eRevPre", "eRevDHE(dheki)", "eRevDHE(dhekr)", "eRevPsk"]
replacement = {"eRevLDH(ldhi)": "_ldhi", "eRevLDH(ldhr)": "_ldhr", "eRevPre": "_precompi", "eRevDHE(dheki)": "_dheki", "eRevDHE(dhekr)": "_dhekr", "eRevPsk": "_psk"}

S2c = list(itertools.combinations(subkeys, 2))
S3c = list(itertools.combinations(subkeys, 3))


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


rep_comb = []
for event in comb:
	rep_comb.append(replacement.get(event, event))


with open("wireguard_command_4", "r") as infile, open('wireguard_command_4_1', 'w') as outfile:
	for line in infile :
		if not any(key in line for key in rep_comb):
			outfile.write(line)


with open("wireguard_command_2.2log", "r") as infile:
	filedata = infile.read()
	newfiledata = re.sub(result, replace, filedata)
	with open("wireguard_command_2.lg", "w") as outfile:
		outfile.write(newfiledata)
infile.close()
outfile.close()

comb2 = []

with open("wireguard_command_2.lg", "r") as infile:
	for line in infile:
		for keys in S2c:
			if ("is true" in line) and (keys[0] in line) and (keys[1] in line):
				comb2.append(keys)
infile.close()

rep_comb2 = []
for item in comb2:
	replaced_item = tuple(replacement.get(elem, elem) for elem in item)
	rep_comb2.append(replaced_item)


with open("wireguard_command_4_1", "r") as infile, open('wireguard_command_4_2', 'w') as outfile:
	lines = infile.readlines()
	filtered_lines = []
	for line in lines :
		if not any(all( word in line for word in keys) for keys in rep_comb2):
			filtered_lines.append(line)
	outfile.writelines(filtered_lines)



with open("wireguard_command_3.3log", "r") as infile:
	filedata = infile.read()
	newfiledata = re.sub(result, replace, filedata)
	with open("wireguard_command_3.lg", "w") as outfile:
		outfile.write(newfiledata)
infile.close()
outfile.close()

comb3 = []

with open("wireguard_command_3.lg", "r") as infile:
	for line in infile:
		for keys in S3c:
			if ("is true" in line) and (keys[0] in line) and (keys[1] in line)  and (keys[2] in line):
				comb3.append(keys)
infile.close()

rep_comb3 = []
for item in comb3:
	replaced_item = tuple(replacement.get(elem, elem) for elem in item)
	rep_comb3.append(replaced_item)


with open("wireguard_command_4_2", "r") as infile, open('wireguard_command_4_opt', 'w') as outfile:
	lines = infile.readlines()
	filtered_lines = []
	for line in lines :
		if not any(all( word in line for word in keys) for keys in rep_comb3):
			filtered_lines.append(line)
	outfile.writelines(filtered_lines)

os.remove("wireguard_command_1.lg")
os.remove("wireguard_command_2.lg")
os.remove("wireguard_command_3.lg")
os.remove("wireguard_command_4_1")
os.remove("wireguard_command_4_2")


