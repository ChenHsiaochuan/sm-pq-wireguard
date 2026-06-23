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