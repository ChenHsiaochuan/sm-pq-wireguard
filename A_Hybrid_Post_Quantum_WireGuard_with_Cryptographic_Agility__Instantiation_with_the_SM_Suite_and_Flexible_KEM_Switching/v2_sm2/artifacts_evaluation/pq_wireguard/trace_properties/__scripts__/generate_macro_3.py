#!/usr/bin/env python3.6
'''
Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
'''


import fileinput

import sys

import os

import itertools

import shutil

path = "macro"

if os.path.exists(path):
	os.chdir(path)
	for file in sorted(os.listdir()):
		os.remove(file)
	os.chdir("..")
	os.rmdir(path)
if not os.path.exists(path):
	os.makedirs(path)

shutil.copy(r"wireguard_peer_initiator_reference.spthy", r"macro/wireguard_peer_initiator_reference.spthy")
shutil.copy(r"wireguard_process_reference.spthy", r"macro/wireguard_process_reference.spthy")
shutil.copy(r"wireguard_peer_responder_reference.spthy", r"macro/wireguard_peer_responder_reference.spthy")

os.chdir(path)


#all_trusted

with open('wireguard_peer_initiator_reference.spthy', 'r') as infile:
	filedata = infile.read()

filedata = filedata.replace("// beginning of initiator process", "#ifdef all_trusted // beginning of initiator process")
filedata = filedata.replace("// end of initiator process", "#endif // end of initiator process")

with open('wireguard_peer_initiator_reference.spthy.all_trusted', 'w') as outfile:
	outfile.write(filedata)

infile.close()
outfile.close()

with open('wireguard_process_reference.spthy', 'r') as infile:
	filedata = infile.read()

filedata = filedata.replace("// beginning of process", "#ifdef all_trusted // beginning of process")
filedata = filedata.replace("// end of process", "#endif // end of process")

with open('wireguard_process_reference.spthy.all_trusted', 'w') as outfile:
	outfile.write(filedata)

infile.close()
outfile.close()


with open('wireguard_peer_responder_reference.spthy', 'r') as infile:
	filedata = infile.read()

filedata = filedata.replace("// beginning of responder process", "#ifdef all_trusted // beginning of responder process")
filedata = filedata.replace("// end of responder process", "#endif // end of responder process")

with open('wireguard_peer_responder_reference.spthy.all_trusted', 'w') as outfile:
	outfile.write(filedata)

infile.close()
outfile.close()


keys = ["ka", "ra", "tpkr", "psk"]

L1c = list(itertools.combinations(keys, 1))

"""
L2c = list(itertools.combinations(keys, 2))
L3c = list(itertools.combinations(keys, 3))
L4c = list(itertools.combinations(keys, 4))
L5c = list(itertools.combinations(keys, 5))
L6c = list(itertools.combinations(keys, 6))
L7c = list(itertools.combinations(keys, 7))
L8c = list(itertools.combinations(keys, 8))
L9c = list(itertools.combinations(keys, 9))
"""

def replace(L):


	print(len(L))
	
	cstr = "_"
	for i in range(0, len(L)):
		if i < len(L)-1:
			cstr = cstr+L[i][0]+"_"
		else:
			cstr = cstr+L[i][0]



	for l in L:


		print(cstr)

		with open('wireguard_peer_initiator_reference.spthy', 'r') as infile:
			filedata = infile.read()

		filedata = filedata.replace("// beginning of initiator process", "#ifdef untrusted_"+l[0]+"_"+l[1]+"_"+l[2]+"_"+l[3]+"_"+l[4]+"_"+l[5]+"_"+l[6]+"_"+l[7]+" // beginning of initiator process")
		filedata = filedata.replace("// end of initiator process", "#endif // end of initiator process")

		if ((l[0] == "pkr") | (l[1] == "pkr") | (l[2] == "pkr") | (l[3] == "pkr") | (l[4] == "pkr") | (l[5] == "pkr") | (l[6] == "pkr") | (l[7] == "pkr")):
			filedata = filedata.replace("Initiator(~ltkI, pkI, pkR, ", "Initiator(~ltkI, pkI, ")
			filedata = filedata.replace("// pkr input", "in(<'responder', pkR>); // pkr input")
		if ((l[0] == "precomp_i") | (l[1] == "precomp_i") | (l[2] == "precomp_i") | (l[3] == "precomp_i") | (l[4] == "precomp_i") | (l[5] == "precomp_i") | (l[6] == "precomp_i") | (l[7] == "precomp_i")):
			#filedata = filedata.replace("sisr, ~psk, empty, zero_1) =", "~psk, empty, zero_1) =")
			filedata = filedata.replace("let sisr = (pkR)^~ltkI in // precompi input", "in(<'precompi', sisr>); // precompi input")
		if ((l[0] == "eki") | (l[1] == "eki") | (l[2] == "eki") | (l[3] == "eki") | (l[4] == "eki") | (l[5] == "eki") | (l[6] == "eki") | (l[7] == "eki")):
			filedata = filedata.replace("new ~ekI;", "in(~ekI);")
			filedata = filedata.replace("| (RevealEki(~ekI))", "// | (RevealEki(~ekI))")
			filedata = filedata.replace("(   // This parallelizes ekI compromise", "// (   // This parallelizes ekI compromise")
			filedata = filedata.replace(")     // This parallelizes ekI compromise", "// )     // This parallelizes ekI compromise")

		with open('wireguard_peer_initiator_reference.spthy.untrusted_'+l[0]+'_'+l[1]+'_'+l[2]+'_'+l[3]+'_'+l[4]+'_'+l[5]+'_'+l[6]+'_'+l[7], 'w') as outfile:
			outfile.write(filedata)

		infile.close()
		outfile.close()

		with open('wireguard_process_reference.spthy', 'r') as infile:
			filedata = infile.read()

		filedata = filedata.replace("// beginning of process", "#ifdef untrusted_"+l[0]+"_"+l[1]+"_"+l[2]+"_"+l[3]+"_"+l[4]+"_"+l[5]+"_"+l[6]+"_"+l[7]+" // beginning of process")
		filedata = filedata.replace("// end of process", "#endif // end of process")
		if ((l[0] == "ltki") | (l[1] == "ltki") | (l[2] == "ltki") | (l[3] == "ltki") | (l[4] == "ltki") | (l[5] == "ltki") | (l[6] == "ltki") | (l[7] == "ltki")):
			filedata = filedata.replace("new ~ltkI;", "in(~ltkI);")
			filedata = filedata.replace("| RevealLtki(~ltkI)", "// | RevealLtki(~ltkI)")
			filedata = filedata.replace("| RevealPub('g'^~ltkI)", "// | RevealPub('g'^~ltkI)")
			filedata = filedata.replace("| RevealPre(~ltkI, ~ltkR)", "// | RevealPre(~ltkI, ~ltkR)")
		if ((l[0] == "ltkr") | (l[1] == "ltkr") | (l[2] == "ltkr") | (l[3] == "ltkr") | (l[4] == "ltkr") | (l[5] == "ltkr") | (l[6] == "ltkr") | (l[7] == "ltkr")):
			filedata = filedata.replace("new ~ltkR;", "in(~ltkR);")
			filedata = filedata.replace("| RevealLtkr(~ltkR)", "// | RevealLtkr(~ltkR)")
			filedata = filedata.replace("| RevealPub('g'^~ltkR)", "// | RevealPub('g'^~ltkR)")
			filedata = filedata.replace("| RevealPre(~ltkI, ~ltkR)", "// | RevealPre(~ltkI, ~ltkR)")
		if ((l[0] == "pki") | (l[1] == "pki") | (l[2] == "pki") | (l[3] == "pki") | (l[4] == "pki") | (l[5] == "pki") | (l[6] == "pki") | (l[7] == "pki")):
			filedata = filedata.replace("~ltkR, 'g'^~ltkI, 'g'^~ltkR, ", "~ltkR, 'g'^~ltkR, ")
		if ((l[0] == "pkr") | (l[1] == "pkr") | (l[2] == "pkr") | (l[3] == "pkr") | (l[4] == "pkr") | (l[5] == "pkr") | (l[6] == "pkr") | (l[7] == "pkr")):
			filedata = filedata.replace("~ltkI, 'g'^~ltkI, 'g'^~ltkR, ", "~ltkI, 'g'^~ltkI, ")
		if ((l[0] == "psk") | (l[1] == "psk") | (l[2] == "psk") | (l[3] == "psk") | (l[4] == "psk") | (l[5] == "psk") | (l[6] == "psk") | (l[7] == "psk")):
			filedata = filedata.replace("new ~psk;", "in(~psk);")
		if ((l[0] == "precomp_i") | (l[1] == "precomp_i") | (l[2] == "precomp_i") | (l[3] == "precomp_i") | (l[4] == "precomp_i") | (l[5] == "precomp_i") | (l[6] == "precomp_i") | (l[7] == "precomp_i")):
			filedata = filedata.replace("// precompi output", "out(<'precompi', ('g'^~ltkR)^~ltkI>); // precompi output")
			#filedata = filedata.replace("('g'^~ltkR)^~ltkI, ", "")
			filedata = filedata.replace("| RevealPre(~ltkI, ~ltkR)", "// | RevealPre(~ltkI, ~ltkR)")
		if ((l[0] == "precomp_r") | (l[1] == "precomp_r") | (l[2] == "precomp_r") | (l[3] == "precomp_r") | (l[4] == "precomp_r") | (l[5] == "precomp_r") | (l[6] == "precomp_r") | (l[7] == "precomp_r")):
			filedata = filedata.replace("// precompr output", "out(<'precompr', ('g'^~ltkI)^~ltkR>); // precompr output")
			#filedata = filedata.replace("('g'^~ltkI)^~ltkR, ", "")
			filedata = filedata.replace("| RevealPre(~ltkI, ~ltkR)", "// | RevealPre(~ltkI, ~ltkR)")

		with open('wireguard_process_reference.spthy.untrusted_'+l[0]+'_'+l[1]+'_'+l[2]+'_'+l[3]+'_'+l[4]+'_'+l[5]+'_'+l[6]+'_'+l[7], 'w') as outfile:
			outfile.write(filedata)

		infile.close()
		outfile.close()

		with open('wireguard_peer_responder_reference.spthy', 'r') as infile:
			filedata = infile.read()

		filedata = filedata.replace("// beginning of responder process", "#ifdef untrusted_"+l[0]+"_"+l[1]+"_"+l[2]+"_"+l[3]+"_"+l[4]+"_"+l[5]+"_"+l[6]+"_"+l[7]+" // beginning of responder process")
		filedata = filedata.replace("// end of responder process", "#endif // end of responder process")

		if ((l[0] == "pki") | (l[1] == "pki") | (l[2] == "pki") | (l[3] == "pki") | (l[4] == "pki") | (l[5] == "pki") | (l[6] == "pki") | (l[7] == "pki")):
			filedata = filedata.replace("Responder(~ltkR, pkI, pkR, ", "Responder(~ltkR, pkR, ")
			filedata = filedata.replace("// pki input", "in(<'initiator', pkI>); // pki input")
		if ((l[0] == "precomp_r") | (l[1] == "precomp_r") | (l[2] == "precomp_r") | (l[3] == "precomp_r") | (l[4] == "precomp_r") | (l[5] == "precomp_r") | (l[6] == "precomp_r") | (l[7] == "precomp_r")):
			#filedata = filedata.replace("srsi, ~psk, empty, zero_1) =", "~psk, empty, zero_1) =")
			filedata = filedata.replace("let srsi = (pkI)^~ltkR in // precompr input", "in(<'precompr', srsi>); // precompr input")
		if ((l[0] == "ekr") | (l[1] == "ekr") | (l[2] == "ekr") | (l[3] == "ekr") | (l[4] == "ekr") | (l[5] == "ekr") | (l[6] == "ekr") | (l[7] == "ekr")):
			filedata = filedata.replace("new ~ekR;", "in(~ekR);")


		with open('wireguard_peer_responder_reference.spthy.untrusted_'+l[0]+'_'+l[1]+'_'+l[2]+'_'+l[3]+'_'+l[4]+'_'+l[5]+'_'+l[6]+'_'+l[7], 'w') as outfile:
			outfile.write(filedata)

		infile.close()
		outfile.close()

replace(L1c)

os.remove("wireguard_peer_initiator_reference.spthy")
os.remove("wireguard_process_reference.spthy")
os.remove("wireguard_peer_responder_reference.spthy")

listfiles=sorted(os.listdir())

with open("wireguard_macro.spthy", "w") as outfile:
	for file in listfiles:
		with open(file, "r") as infile:
			outfile.write(infile.read())

shutil.copy(r"wireguard_macro.spthy", r"../wireguard_macro.spthy")



for file in sorted(os.listdir()):
	os.remove(file)

os.chdir("..")

os.rmdir(path)
