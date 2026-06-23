#!/usr/bin/env python3.6
'''
Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
'''

import re

from sympy.logic.boolalg import to_dnf
from sympy.logic.boolalg import to_cnf
from sympy import symbols


Ru, Rv, Rx, Ry, Rc, Rs = symbols("Ru, Rv, Rx, Ry, Rc, Rs")


replacement_table = [
    ("(event(eRevPsk(psk", "Rs"),
    ("event(eRevPsk(psk", "Rs"),
    ("(event(eRevLDH(ldhi))", "Ru"),
    ("event(eRevLDH(ldhi))", "Ru"),
    ("(event(eRevLDH(ldhr))", "Rv"),
    ("event(eRevLDH(ldhr))", "Rv"),
    ("(event(eRevDHE(dheki))", "Rx"),
    ("event(eRevDHE(dheki", "Rx"),
    ("(event(eRevDHE(dhekr))", "Ry"),
    ("event(eRevDHE(dhekr", "Ry"),
    ("(event(eRevPre(ldhi,ldhr))", "Rc"),
    ("event(eRevPre(ldhi,ldhr))", "Rc"),
    ("(event(eRevPre(ldhr,ldhi))", "Rc"),
    ("event(eRevPre(ldhr,ldhi))", "Rc")
]


paper_table = [
    ("Rs", "psk"),
    ("Ru", "sic"),
    ("Rv", "src"),
    ("Rx", "eic"),
    ("Ry", "erc"),
    ("Rc", "dhsisr"),
]

def res2dnf(arg1):
	with open(arg1, 'r', encoding="utf-8") as infile, open(arg1+'.dnf', 'w') as newfile:
		Lines = infile.readlines()
		Len = len(Lines)
		i = 0
		for line in Lines:
			pattern = r"RESULT(.*?)==> "
			line = re.sub(pattern, "", line)

			line = line.replace(" is true.", "")

			for replacement in replacement_table:
				line = line.replace(replacement[0], replacement[1])

			pattern = r"_\d"
			line = re.sub(pattern, "", line)

			line = line.replace("||", "|")

			line = "("+line
			if(i != Len-1):
				line = line.replace("\n", ") & ")
				i = i+1
			else:
				line = line.replace("\n", ")")

			pattern = r"\(  R"
			line = re.sub(pattern, r"(R", line)


			pattern = r"\(  \("
			line = re.sub(pattern, r"(", line)

			pattern = r"\(\("
			line = re.sub(pattern, r"(", line)

			pattern = r"\)\)\)"
			line = re.sub(pattern, r")", line)


			pattern = r"\)\) \|"
			line = re.sub(pattern, r"|", line)


			newfile.write(line)


	with open(arg1+'.dnf', 'r') as infile, open('results.cnfdnf', 'a') as resfile:
		data = infile.read()
		if(data == 'NULL'):
			resfile.write("DNF for secrecy_rsk7: \u2205\n")
			resfile.write("CNF for secrecy_rsk7: \u2205\n")
		else:
			dnf = to_dnf(data, simplify=True, force=True)
			cnf = to_cnf(data, simplify=True, force=True)
			for old, new in paper_table:
				dnf = re.sub(rf"\b{old}\b", new, str(dnf))
				cnf = re.sub(rf"\b{old}\b", new, str(cnf))
			resfile.write("DNF for secrecy_rsk7pfs: "+str(dnf)+"\n")
			resfile.write("CNF for secrecy_rsk7pfs: "+str(cnf)+"\n")

res2dnf("process_read_access/secrecy_rsk7pfs/wireguard_secrecy_rsk7pfs.pv.log")

