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
#shutil.copy(r"KEMlibrary.splib", r"macro/KEMlibrary.splib")

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


#untrusted

#keys = ["ltki", "ltkr", "pki", "pkr", "eki", "ekr", "precomp_i", "precomp_r", "psk"]

keys = ["tpkr", "ra", "ka", "psk"]


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

def replace_1(L):

	for l in L:

		with open('wireguard_peer_initiator_reference.spthy', 'r') as infile:
			filedata = infile.read()

		filedata = filedata.replace("// beginning of initiator process", "#ifdef untrusted_"+l[0]+" // beginning of initiator process")
		filedata = filedata.replace("// end of initiator process", "#endif // end of initiator process")

		if (l[0] == "pkr"):
			filedata = filedata.replace("Initiator(~ltkI, pkI, pkR, ", "Initiator(~ltkI, pkI, ")
			filedata = filedata.replace("// pkr input", "in(<'responder', pkR>); // pkr input")
		if (l[0] == "precomp_i"):
			#filedata = filedata.replace("sisr, ~psk, empty, zero_1) =", "~psk, empty, zero_1) =")
			filedata = filedata.replace("let sisr = (pkR)^~ltkI in // precompi input", "in(<'precompi', sisr>); // precompi input")
		if (l[0] == "eki"):
			filedata = filedata.replace("new ~ekI;", "in(~ekI);")
			filedata = filedata.replace("| (RevealEki(~ekI))", "// | (RevealEki(~ekI))")
			filedata = filedata.replace("(   // This parallelizes ekI compromise", "// (   // This parallelizes ekI compromise")
			filedata = filedata.replace(")     // This parallelizes ekI compromise", "// )     // This parallelizes ekI compromise")

		with open('wireguard_peer_initiator_reference.spthy.untrusted_'+l[0], 'w') as outfile:
			outfile.write(filedata)

		infile.close()
		outfile.close()

		with open('wireguard_process_reference.spthy', 'r') as infile:
			filedata = infile.read()

		filedata = filedata.replace("// beginning of process", "#ifdef untrusted_"+l[0]+" // beginning of process")
		filedata = filedata.replace("// end of process", "#endif // end of process")
		if (l[0] == "ltki"):
			filedata = filedata.replace("new ~ltkI;", "in(~ltkI);")
			filedata = filedata.replace("| RevealLtki(~ltkI)", "// | RevealLtki(~ltkI)")
			filedata = filedata.replace("| RevealPub('g'^~ltkI)", "// | RevealPub('g'^~ltkI)")
			filedata = filedata.replace("| RevealPre(~ltkI, ~ltkR)", "// | RevealPre(~ltkI, ~ltkR)")
		if (l[0] == "ltkr"):
			filedata = filedata.replace("new ~ltkR;", "in(~ltkR);")
			filedata = filedata.replace("| RevealLtkr(~ltkR)", "// | RevealLtkr(~ltkR)")
			filedata = filedata.replace("| RevealPub('g'^~ltkR)", "// | RevealPub('g'^~ltkR)")
			filedata = filedata.replace("| RevealPre(~ltkI, ~ltkR)", "// | RevealPre(~ltkI, ~ltkR)")
		if (l[0] == "pki"):
			filedata = filedata.replace("~ltkR, 'g'^~ltkI, 'g'^~ltkR, ", "~ltkR, 'g'^~ltkR, ")
		if (l[0] == "pkr"):
			filedata = filedata.replace("~ltkI, 'g'^~ltkI, 'g'^~ltkR, ", "~ltkI, 'g'^~ltkI, ")
		if (l[0] == "psk"):
			filedata = filedata.replace("new ~psk;", "in(~psk);")
			filedata = filedata.replace("| RevealPsk(~psk)", "// | RevealPsk(~psk)")

		if (l[0] == "tpkr"):
			filedata = filedata.replace("new ~tpkr;", "in(~tpkr);")
			filedata = filedata.replace("| RevealTpkr(~tpkR)", "// | RevealTpkr(~tpkR)")

		if (l[0] == "tpki"):
			filedata = filedata.replace("new ~tpki;", "in(~tpki);")
			filedata = filedata.replace("| RevealTpki(~tpkI)", "// | RevealTpki(~tpkI)")


		if (l[0] == "precomp_i"):
			filedata = filedata.replace("// precompi output", "out(<'precompi', ('g'^~ltkR)^~ltkI>); // precompi output")
			#filedata = filedata.replace("('g'^~ltkR)^~ltkI, ", "")
			filedata = filedata.replace("| RevealPre(~ltkI, ~ltkR)", "// | RevealPre(~ltkI, ~ltkR)")
		if (l[0] == "precomp_r"):
			filedata = filedata.replace("// precompr output", "out(<'precompr', ('g'^~ltkI)^~ltkR>); // precompr output")
			#filedata = filedata.replace("('g'^~ltkI)^~ltkR, ", "")
			filedata = filedata.replace("| RevealPre(~ltkI, ~ltkR)", "// | RevealPre(~ltkI, ~ltkR)")

		if (l[0] == "rb"):
			filedata = filedata.replace("new ~rb;", "in(~rb);")
			filedata = filedata.replace("| (RevealRb(~rb))", "// | (RevealRb(~rb))")


		with open('wireguard_process_reference.spthy.untrusted_'+l[0], 'w') as outfile:
			outfile.write(filedata)

		infile.close()
		outfile.close()

		with open('wireguard_peer_responder_reference.spthy', 'r') as infile:
			filedata = infile.read()

		filedata = filedata.replace("// beginning of responder process", "#ifdef untrusted_"+l[0]+" // beginning of responder process")
		filedata = filedata.replace("// end of responder process", "#endif // end of responder process")

		if (l[0] == "pki"):
			filedata = filedata.replace("Responder(~ltkR, pkI, pkR, ", "Responder(~ltkR, pkR, ")
			filedata = filedata.replace("// pki input", "in(<'initiator', pkI>); // pki input")
		if (l[0] == "precomp_r"):
			#filedata = filedata.replace("srsi, ~psk, empty, zero_1) =", "~psk, empty, zero_1) =")
			filedata = filedata.replace("let srsi = (pkI)^~ltkR in // precompr input", "in(<'precompr', srsi>); // precompr input")
		if (l[0] == "ekr"):
			filedata = filedata.replace("new ~ekR;", "in(~ekR);")
			filedata = filedata.replace("( // This parallelizes ekR compromise", "// ( // This parallelizes ekR compromise")
			filedata = filedata.replace(") // This parallelizes ekR compromise", "// ) // This parallelizes ekR compromise")
			filedata = filedata.replace("| (RevealEkr(~ekR))", "// | (RevealEkr(~ekR))")

		if (l[0] == "ra"):
			filedata = filedata.replace("new ~ra;", "in(~ra);")
			filedata = filedata.replace("| (RevealRa(~ra))", "// | (RevealRa(~ra))")

		if (l[0] == "ka"):
			filedata = filedata.replace("let ka = kdf1(<~ra, ~tpkR>) in", "in(ka);")
			filedata = filedata.replace("| (RevealKa(ka))", "// | (RevealKa(ka))")



		with open('wireguard_peer_responder_reference.spthy.untrusted_'+l[0], 'w') as outfile:
			outfile.write(filedata)

		infile.close()
		outfile.close()

def replace_2(L):

	for l in L:

		with open('wireguard_peer_initiator_reference.spthy', 'r') as infile:
			filedata = infile.read()

		filedata = filedata.replace("// beginning of initiator process", "#ifdef untrusted_"+l[0]+"_"+l[1]+" // beginning of initiator process")
		filedata = filedata.replace("// end of initiator process", "#endif // end of initiator process")

		if ((l[0] == "pkr") | (l[1] == "pkr")):
			filedata = filedata.replace("Initiator(~ltkI, pkI, pkR, ", "Initiator(~ltkI, pkI, ")
			filedata = filedata.replace("// pkr input", "in(<'responder', pkR>); // pkr input")
		if ((l[0] == "precomp_i") | (l[1] == "precomp_i")):
			#filedata = filedata.replace("sisr, ~psk, empty, zero_1) =", "~psk, empty, zero_1) =")
			filedata = filedata.replace("let sisr = (pkR)^~ltkI in // precompi input", "in(<'precompi', sisr>); // precompi input")
		if ((l[0] == "eki") | (l[1] == "eki")):
			filedata = filedata.replace("new ~ekI;", "in(~ekI);")
			filedata = filedata.replace("| (RevealEki(~ekI))", "// | (RevealEki(~ekI))")
			filedata = filedata.replace("(   // This parallelizes ekI compromise", "// (   // This parallelizes ekI compromise")
			filedata = filedata.replace(")     // This parallelizes ekI compromise", "// )     // This parallelizes ekI compromise")

		with open('wireguard_peer_initiator_reference.spthy.untrusted_'+l[0]+'_'+l[1], 'w') as outfile:
			outfile.write(filedata)

		infile.close()
		outfile.close()

		with open('wireguard_process_reference.spthy', 'r') as infile:
			filedata = infile.read()

		filedata = filedata.replace("// beginning of process", "#ifdef untrusted_"+l[0]+"_"+l[1]+" // beginning of process")
		filedata = filedata.replace("// end of process", "#endif // end of process")
		if ((l[0] == "ltki") | (l[1] == "ltki")):
			filedata = filedata.replace("new ~ltkI;", "in(~ltkI);")
			filedata = filedata.replace("| RevealLtki(~ltkI)", "// | RevealLtki(~ltkI)")
			filedata = filedata.replace("| RevealPub('g'^~ltkI)", "// | RevealPub('g'^~ltkI)")
			filedata = filedata.replace("| RevealPre(~ltkI, ~ltkR)", "// | RevealPre(~ltkI, ~ltkR)")
		if ((l[0] == "ltkr") | (l[1] == "ltkr")):
			filedata = filedata.replace("new ~ltkR;", "in(~ltkR);")
			filedata = filedata.replace("| RevealLtkr(~ltkR)", "// | RevealLtkr(~ltkR)")
			filedata = filedata.replace("| RevealPub('g'^~ltkR)", "// | RevealPub('g'^~ltkR)")
			filedata = filedata.replace("| RevealPre(~ltkI, ~ltkR)", "// | RevealPre(~ltkI, ~ltkR)")
		if ((l[0] == "pki") | (l[1] == "pki")):
			filedata = filedata.replace("~ltkR, 'g'^~ltkI, 'g'^~ltkR, ", "~ltkR, 'g'^~ltkR, ")	
		if ((l[0] == "pkr") | (l[1] == "pkr")):
			filedata = filedata.replace("~ltkI, 'g'^~ltkI, 'g'^~ltkR, ", "~ltkI, 'g'^~ltkI, ")	
		if ((l[0] == "psk") | (l[1] == "psk")):
			filedata = filedata.replace("new ~psk;", "in(~psk);")
			filedata = filedata.replace("| RevealPsk(~psk)", "// | RevealPsk(~psk)")
		if ((l[0] == "precomp_i") | (l[1] == "precomp_i")):
			filedata = filedata.replace("// precompi output", "out(<'precompi', ('g'^~ltkR)^~ltkI>); // precompi output")
			#filedata = filedata.replace("('g'^~ltkR)^~ltkI, ", "")
			filedata = filedata.replace("| RevealPre(~ltkI, ~ltkR)", "// | RevealPre(~ltkI, ~ltkR)")
		if ((l[0] == "precomp_r") | (l[1] == "precomp_r")):
			filedata = filedata.replace("// precompr output", "out(<'precompr', ('g'^~ltkI)^~ltkR>); // precompr output")
			#filedata = filedata.replace("('g'^~ltkI)^~ltkR, ", "")
			filedata = filedata.replace("| RevealPre(~ltkI, ~ltkR)", "// | RevealPre(~ltkI, ~ltkR)")

		with open('wireguard_process_reference.spthy.untrusted_'+l[0]+'_'+l[1], 'w') as outfile:
			outfile.write(filedata)

		infile.close()
		outfile.close()

		with open('wireguard_peer_responder_reference.spthy', 'r') as infile:
			filedata = infile.read()

		filedata = filedata.replace("// beginning of responder process", "#ifdef untrusted_"+l[0]+"_"+l[1]+" // beginning of responder process")
		filedata = filedata.replace("// end of responder process", "#endif // end of responder process")

		if ((l[0] == "pki") | (l[1] == "pki")):
			filedata = filedata.replace("Responder(~ltkR, pkI, pkR, ", "Responder(~ltkR, pkR, ")
			filedata = filedata.replace("// pki input", "in(<'initiator', pkI>); // pki input")
		if ((l[0] == "precomp_r") | (l[1] == "precomp_r")):
			#filedata = filedata.replace("srsi, ~psk, empty, zero_1) =", "~psk, empty, zero_1) =")
			filedata = filedata.replace("let srsi = (pkI)^~ltkR in // precompr input", "in(<'precompr', srsi>); // precompr input")
		if ((l[0] == "ekr") | (l[1] == "ekr")):
			filedata = filedata.replace("new ~ekR;", "in(~ekR);")
			filedata = filedata.replace("( // This parallelizes ekR compromise", "// ( // This parallelizes ekR compromise")
			filedata = filedata.replace(") // This parallelizes ekR compromise", "// ) // This parallelizes ekR compromise")
			filedata = filedata.replace("| (RevealEkr(~ekR))", "// | (RevealEkr(~ekR))")


		with open('wireguard_peer_responder_reference.spthy.untrusted_'+l[0]+'_'+l[1], 'w') as outfile:
			outfile.write(filedata)

		infile.close()
		outfile.close()


replace_1(L1c)


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