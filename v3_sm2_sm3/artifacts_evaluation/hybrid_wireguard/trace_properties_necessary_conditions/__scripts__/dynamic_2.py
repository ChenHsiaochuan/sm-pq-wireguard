#!/usr/bin/env python3.6
'''
Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
'''


import os

import re

import itertools

subkeys = ["eRevKEMLtki", "eRevKEMLtkr", "eRevLdhi", "eRevLdhr", "eRevPre", "eRevTpki", "eRevTpkr", "eRevKEMEki", "eRevDHEki", "eRevDHEkr", "eRevRa", "eRevRb", "eRevRe", "eRevPsk"]
replacement = {"eRevKEMLtki": "_kemltki", "eRevKEMLtkr": "_kemltkr", "eRevLdhi": "_ldhi", "eRevLdhr": "_ldhr", "eRevPre": "_precompi", "eRevTpki": "_tpki", "eRevTpkr": "_tpkr", "eRevKEMEki": "_kemeki", "eRevDHEki": "_dheki", "eRevDHEkr": "_dhekr", "eRevRa": "_ra", "eRevRb": "_rb", "eRevRe": "_re", "eRevPsk": "_psk"}

S2c = list(itertools.combinations(subkeys, 2))

#RESULT event(eRConfirm(kemltki,kemltkr,ldhi,ldhr,kemeki,dheki,dhekr,psk_4,tpkr,ka_2,k_2,kb_2,ra_2,re_2,ck_2))@i ==> (event(eIConfirm(kemltki,kemltkr,ldhi,ldhr,kemeki,dheki,dhekr,psk_4,tpki,ka_2,k_2,kb_2,rb_2,ck_2))@j && i > j) ||

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

#print(comb)


rep_comb = []
for event in comb:
	rep_comb.append(replacement.get(event, event))

#print(rep_comb)

os.remove("wireguard_command_1.lg")

with open("wireguard_command_2", "r") as infile, open('wireguard_command_2_opt', 'w') as outfile:
	for line in infile :
		if not any(key in line for key in rep_comb):
			outfile.write(line)


