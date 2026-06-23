import re

from sympy.logic.boolalg import to_dnf
from sympy.logic.boolalg import to_cnf
from sympy import symbols


Ki, Kr, Ti, Tr, Kx, Ra, Rb, Re, Rs = symbols("Ki, Kr, Ti, Tr, Kx, Ra, Rb, Re, Rs")


replacement_table = [
    ("(event(eRevTpk(tpki", "Ti"),
    ("(event(eRevTpk(tpkr", "Tr"),
    ("event(eRevTpk(tpki", "Ti"),
    ("event(eRevTpk(tpkr", "Tr"),
    ("(event(eRevPsk(psk", "Rs"),
    ("event(eRevPsk(psk", "Rs"),
    ("(event(eRevKEMLtk(kemltkr", "Kr"),
    ("event(eRevKEMLtk(kemltkr", "Kr"),
    ("(event(eRevKEMLtk(kemltki", "Ki"),
    ("event(eRevKEMLtk(kemltki", "Ki"),
    ("(event(eRevKEMEki(kempeki", "Kx"),
    ("event(eRevKEMEki(kempeki", "Kx"),
    ("(event(eRevRa(ra", "Ra"),
    ("(event(eRevRb(rb", "Rb"),
    ("(event(eRevRe(re", "Re"),
    ("event(eRevRa(ra", "Ra"),
    ("event(eRevRb(rb", "Rb"),
    ("event(eRevRe(re", "Re"),

]


paper_table = [
    ("Rs", "psk"),
    ("Rb", "ri"),
    ("Ra", "rr"),
    ("Re", "re"),
    ("Ki", "sipq"),
    ("Kr", "srpq"),
    ("Kx", "eipq"),
    ("Ti", "sigi"),
    ("Tr", "sigr"),
]


def res2dnf(arg1):
	with open(arg1) as infile, open(arg1+'.dnf', 'w') as newfile:
		Lines = infile.readlines()
		Len = len(Lines)
		i = 0

		for line in Lines:

			pattern = r"RESULT(.*?)\|\|"
			line = re.sub(pattern, "", line)

			pattern = r"\(event(.*?)j\) \|\|"
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

			pattern = r"\)\)\)"
			line = re.sub(pattern, r")", line)


			pattern = r"\)\) \|"
			line = re.sub(pattern, r"|", line)


			pattern = r"\( \|"
			line = re.sub(pattern, r"(", line)

			
			newfile.write(line)


	with open(arg1+'.dnf', 'r') as infile, open('results.cnfdnf', 'a') as resfile:
		data = infile.read()
		if(data == 'NULL'):
			resfile.write("DNF for unilateral_responder: \u2205\n")
			resfile.write("CNF for unilateral_responder: \u2205\n")
		else:
			dnf = to_dnf(data, simplify=True, force=True)
			cnf = to_cnf(data, simplify=True, force=True)
			for old, new in paper_table:
				dnf = re.sub(rf"\b{old}\b", new, str(dnf))
				cnf = re.sub(rf"\b{old}\b", new, str(cnf))
			resfile.write("DNF for unilateral_responder: "+str(dnf)+"\n")
			resfile.write("CNF for unilateral_responder: "+str(cnf)+"\n")

res2dnf("process_read_access/unilateral_responder/wireguard_unilateral_responder.pv.log")
