#!/usr/bin/env python3.6
'''
Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
'''


from sympy.logic.boolalg import to_dnf
from sympy.logic.boolalg import to_cnf
from sympy import symbols



Ru, Rv, Rx, Ry, Rc, Ki, Kr, Ti, Tr, Ra, Rb, Re, Ka, Kb, Ke, Rs = symbols("Ru, Rv, Rx, Ry, Rc, Ki, Kr, Ti, Tr, Ra, Rb, Re, Ka, Kb, Ke, Rs")

def generate_models_queries_1(data):
	pos = data.find('&')
	after = data[pos + 1:].strip()
	befor = data[:pos - 1].strip()
	
	dnf = to_dnf(after, simplify=True, force=True)
	print(str(befor)+" : "+str(dnf))


def generate_models_queries_2(data):
	pos1 = data.find('|')
	before1 = data[:pos1 - 1].strip()

	pos2 = before1.find('&')
	after2 = before1[pos2 + 1:].strip()
	before2 = before1[:pos2 - 1].strip()

	print(str(before2)+" : "+str(after2))



cnf = "Rs & (Ka | Ki | Ra) & (Ka | Ki | Tr)"
dnf = "(Ka & Rs) | (Ki & Rs) | (Ra & Rs & Tr)"
print(dnf)

generate_models_queries_1(cnf)
generate_models_queries_2(dnf)
pos1 = dnf.find('|')
after = dnf[pos1 + 1:].strip()
generate_models_queries_2(after)
pos1 = after.find('|')
after2 = after[pos1 + 1:].strip()
generate_models_queries_2(after2)