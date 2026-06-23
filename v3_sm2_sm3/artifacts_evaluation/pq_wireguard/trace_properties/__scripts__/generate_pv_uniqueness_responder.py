#!/usr/bin/env python3.6
'''
Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
'''


import os
import itertools

from subprocess import PIPE, Popen

from compute_proof_3 import tamarin_proverif_uniqueness_responder

EMPTY="process_empty/"
QUERIES="queries/"

INTRO=EMPTY+"wireguard_intro.spthy"

MACRO="wireguard_macro.spthy"

END=EMPTY+"wireguard_end.spthy"

SECRECY_SPTHY="process_read_access/uniqueness_responder/wireguard_uniqueness_responder_macro.spthy"

SECRECY_QUERIES=QUERIES+"wireguard_uniqueness_responder_export_queries.spthy"

path = "process_read_access/uniqueness_responder"

if os.path.exists(path):
	os.chdir(path)
	for file in sorted(os.listdir()):
		os.remove(file)
	os.chdir("..")
	os.rmdir(path)
if not os.path.exists(path):
	os.makedirs(path)


listfiles=[INTRO, MACRO, SECRECY_QUERIES, END]

with open(SECRECY_SPTHY, "w") as outfile:
	for file in listfiles:
		with open(file, "r") as infile:
			outfile.write(infile.read())


os.chdir(path)

tamarin_proverif_uniqueness_responder()