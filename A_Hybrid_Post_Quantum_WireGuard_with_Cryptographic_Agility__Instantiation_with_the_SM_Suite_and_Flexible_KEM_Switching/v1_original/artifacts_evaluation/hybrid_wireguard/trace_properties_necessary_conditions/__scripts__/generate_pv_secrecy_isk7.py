#!/usr/bin/env python3.6
'''
Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
'''


import os
from subprocess import PIPE, Popen
from compute_proof_3 import tamarin_proverif_secrecy_isk7

INTRO="process_empty/wireguard_intro.spthy"
END="process_empty/wireguard_end.spthy"

MACRO="wireguard_macro.spthy"

SPTHY="process_read_access/secrecy_isk7/wireguard_macro.spthy"

QUERIES="queries/wireguard_secrecy_isk7_export_queries.spthy"

path = "process_read_access/secrecy_isk7"

if os.path.exists(path):
	os.chdir(path)
	for file in sorted(os.listdir()):
		os.remove(file)
	os.chdir("..")
	os.rmdir(path)
if not os.path.exists(path):
	os.makedirs(path)


listfiles=[INTRO, MACRO, QUERIES, END]

with open(SPTHY, "w") as outfile:
	for file in listfiles:
		with open(file, "r") as infile:
			outfile.write(infile.read())


os.chdir(path)

tamarin_proverif_secrecy_isk7()