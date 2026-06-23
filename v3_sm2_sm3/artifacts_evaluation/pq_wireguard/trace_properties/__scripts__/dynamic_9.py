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
S3c = list(itertools.combinations(subkeys, 3))
S4c = list(itertools.combinations(subkeys, 4))
S5c = list(itertools.combinations(subkeys, 5))
S6c = list(itertools.combinations(subkeys, 6))
S7c = list(itertools.combinations(subkeys, 7))
S8c = list(itertools.combinations(subkeys, 8))


#result = r"RESULT event(eRConfirm(kemltki,kemltkr,ldhi,ldhr,kemeki,dheki,dhekr,psk_4,tpkr,ka_2,k_2,kb_2,ra_2,re_2,ck_2))@i ==> (event(eIConfirm(kemltki,kemltkr,ldhi,ldhr,kemeki,dheki,dhekr,psk_4,tpki,ka_2,k_2,kb_2,rb_2,ck_2))@j && i > j) ||"
#replace = ""
result = r"RESULT(.*?)==>"
replace = ""


with open("wireguard_command_1.1log", "r") as infile:
	filedata = infile.read()
	newfiledata = re.sub(result, replace, filedata)
	#filedata = filedata.replace("RESULT event(eI_SK7(ck_2,ldhi,ldhr,dheki,dhekr,psk_4))@i && attacker(ck_2)@j ==>", "")
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


with open("wireguard_command_9", "r") as infile, open('wireguard_command_9_1', 'w') as outfile:
	for line in infile :
		if not any(key in line for key in rep_comb):
			outfile.write(line)

#os.remove("wireguard_command_1.lg")

with open("wireguard_command_2.2log", "r") as infile:
	filedata = infile.read()
	newfiledata = re.sub(result, replace, filedata)
	#filedata = filedata.replace("RESULT event(eI_SK7(ck_2,ldhi,ldhr,dheki,dhekr,psk_4))@i && attacker(ck_2)@j ==>", "")
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


with open("wireguard_command_9_1", "r") as infile, open('wireguard_command_9_2', 'w') as outfile:
	lines = infile.readlines()
	filtered_lines = []
	for line in lines :
		if not any(all( word in line for word in keys) for keys in rep_comb2):
			filtered_lines.append(line)
	outfile.writelines(filtered_lines)

#os.remove("wireguard_command_9_1")
#os.remove("wireguard_command_2.lg")


with open("wireguard_command_3.3log", "r") as infile:
	filedata = infile.read()
	newfiledata = re.sub(result, replace, filedata)
	#filedata = filedata.replace("RESULT event(eI_SK7(ck_2,ldhi,ldhr,dheki,dhekr,psk_4))@i && attacker(ck_2)@j ==>", "")
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


with open("wireguard_command_9_2", "r") as infile, open('wireguard_command_9_3', 'w') as outfile:
	lines = infile.readlines()
	filtered_lines = []
	for line in lines :
		if not any(all( word in line for word in keys) for keys in rep_comb3):
			filtered_lines.append(line)
	outfile.writelines(filtered_lines)

#os.remove("wireguard_command_9_2")
#os.remove("wireguard_command_3.lg")


with open("wireguard_command_4.4log", "r") as infile:
	filedata = infile.read()
	newfiledata = re.sub(result, replace, filedata)
	#filedata = filedata.replace("RESULT event(eI_SK7(ck_2,ldhi,ldhr,dheki,dhekr,psk_4))@i && attacker(ck_2)@j ==>", "")
	with open("wireguard_command_4.lg", "w") as outfile:
		outfile.write(newfiledata)
infile.close()
outfile.close()

comb4 = []

with open("wireguard_command_4.lg", "r") as infile:
	for line in infile:
		for keys in S4c:
			if ("is true" in line) and (keys[0] in line) and (keys[1] in line)  and (keys[2] in line)   and (keys[3] in line):
				comb4.append(keys)
infile.close()


rep_comb4 = []
for item in comb4:
	replaced_item = tuple(replacement.get(elem, elem) for elem in item)
	rep_comb4.append(replaced_item)


with open("wireguard_command_9_3", "r") as infile, open('wireguard_command_9_4', 'w') as outfile:
	lines = infile.readlines()
	filtered_lines = []
	for line in lines :
		if not any(all( word in line for word in keys) for keys in rep_comb4):
			filtered_lines.append(line)
	outfile.writelines(filtered_lines)

#os.remove("wireguard_command_9_3")
#os.remove("wireguard_command_4.lg")

with open("wireguard_command_5.5log", "r") as infile:
	filedata = infile.read()
	newfiledata = re.sub(result, replace, filedata)
	#filedata = filedata.replace("RESULT event(eI_SK7(ck_2,ldhi,ldhr,dheki,dhekr,psk_4))@i && attacker(ck_2)@j ==>", "")
	with open("wireguard_command_5.lg", "w") as outfile:
		outfile.write(newfiledata)
infile.close()
outfile.close()

comb5 = []

with open("wireguard_command_5.lg", "r") as infile:
	for line in infile:
		for keys in S5c:
			if ("is true" in line) and (keys[0] in line) and (keys[1] in line)  and (keys[2] in line) and (keys[3] in line)  and (keys[4] in line):
				comb5.append(keys)
infile.close()


rep_comb5 = []
for item in comb5:
	replaced_item = tuple(replacement.get(elem, elem) for elem in item)
	rep_comb5.append(replaced_item)


with open("wireguard_command_9_4", "r") as infile, open('wireguard_command_9_5', 'w') as outfile:
	lines = infile.readlines()
	filtered_lines = []
	for line in lines :
		if not any(all( word in line for word in keys) for keys in rep_comb5):
			filtered_lines.append(line)
	outfile.writelines(filtered_lines)

#os.remove("wireguard_command_9_4")
#os.remove("wireguard_command_5.lg")


with open("wireguard_command_6.6log", "r") as infile:
	filedata = infile.read()
	newfiledata = re.sub(result, replace, filedata)
	#filedata = filedata.replace("RESULT event(eI_SK7(ck_2,ldhi,ldhr,dheki,dhekr,psk_4))@i && attacker(ck_2)@j ==>", "")
	with open("wireguard_command_6.lg", "w") as outfile:
		outfile.write(newfiledata)
infile.close()
outfile.close()

comb6 = []

with open("wireguard_command_6.lg", "r") as infile:
	for line in infile:
		for keys in S6c:
			if ("is true" in line) and (keys[0] in line) and (keys[1] in line)  and (keys[2] in line) and (keys[3] in line)  and (keys[4] in line)   and (keys[5] in line):
				comb6.append(keys)
infile.close()


rep_comb6 = []
for item in comb6:
	replaced_item = tuple(replacement.get(elem, elem) for elem in item)
	rep_comb6.append(replaced_item)


with open("wireguard_command_9_5", "r") as infile, open('wireguard_command_9_6', 'w') as outfile:
	lines = infile.readlines()
	filtered_lines = []
	for line in lines :
		if not any(all( word in line for word in keys) for keys in rep_comb6):
			filtered_lines.append(line)
	outfile.writelines(filtered_lines)

#os.remove("wireguard_command_9_5")
#os.remove("wireguard_command_6.lg")


with open("wireguard_command_7.7log", "r") as infile:
	filedata = infile.read()
	newfiledata = re.sub(result, replace, filedata)
	#filedata = filedata.replace("RESULT event(eI_SK7(ck_2,ldhi,ldhr,dheki,dhekr,psk_4))@i && attacker(ck_2)@j ==>", "")
	with open("wireguard_command_7.lg", "w") as outfile:
		outfile.write(newfiledata)
infile.close()
outfile.close()

comb7 = []

with open("wireguard_command_7.lg", "r") as infile:
	for line in infile:
		for keys in S7c:
			if ("is true" in line) and (keys[0] in line) and (keys[1] in line)  and (keys[2] in line) and (keys[3] in line)  and (keys[4] in line)   and (keys[5] in line)  and (keys[6] in line):
				comb7.append(keys)
infile.close()


rep_comb7 = []
for item in comb7:
	replaced_item = tuple(replacement.get(elem, elem) for elem in item)
	rep_comb7.append(replaced_item)


with open("wireguard_command_9_6", "r") as infile, open('wireguard_command_9_7', 'w') as outfile:
	lines = infile.readlines()
	filtered_lines = []
	for line in lines :
		if not any(all( word in line for word in keys) for keys in rep_comb7):
			filtered_lines.append(line)
	outfile.writelines(filtered_lines)

#os.remove("wireguard_command_9_6")
#os.remove("wireguard_command_7.lg")


with open("wireguard_command_8.8log", "r") as infile:
	filedata = infile.read()
	newfiledata = re.sub(result, replace, filedata)
	#filedata = filedata.replace("RESULT event(eI_SK7(ck_2,ldhi,ldhr,dheki,dhekr,psk_4))@i && attacker(ck_2)@j ==>", "")
	with open("wireguard_command_8.lg", "w") as outfile:
		outfile.write(newfiledata)
infile.close()
outfile.close()

comb8 = []

with open("wireguard_command_8.lg", "r") as infile:
	for line in infile:
		for keys in S8c:
			if ("is true" in line) and (keys[0] in line) and (keys[1] in line)  and (keys[2] in line) and (keys[3] in line)  and (keys[4] in line)   and (keys[5] in line)  and (keys[6] in line) and (keys[7] in line):
				comb7.append(keys)
infile.close()


rep_comb8 = []
for item in comb8:
	replaced_item = tuple(replacement.get(elem, elem) for elem in item)
	rep_comb8.append(replaced_item)


with open("wireguard_command_9_7", "r") as infile, open('wireguard_command_9_opt', 'w') as outfile:
	lines = infile.readlines()
	filtered_lines = []
	for line in lines :
		if not any(all( word in line for word in keys) for keys in rep_comb8):
			filtered_lines.append(line)
	outfile.writelines(filtered_lines)

#os.remove("wireguard_command_9_7")
#os.remove("wireguard_command_8.lg")



