#!/usr/bin/env python3.6
'''
Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
'''


from sympy.logic.boolalg import to_anf
from sympy.logic.boolalg import to_dnf
from sympy.logic.boolalg import to_cnf
from sympy import symbols

import fileinput

import sys

import os

import re

result1 = r"RESULT(.*?)==>"
result2 = r"is true."
replace = ""

#(event(eRevKEMLtkr(kemltkr))@j1 && j > j1)

resultKEMLtkr = r"(event(eRevKEMLtkr(.*?).*?).*?)"
replaceKEMLtkr = "Rr"

def main(arg1):

	with open(arg1) as infile, open(arg1+'.new', 'w') as newfile:
		filedata = infile.read()
		newfiledata = re.sub(result1, replace, filedata)
		newfiledata = re.sub(result2, replace, newfiledata)
		newfiledata = re.sub(resultKEMLtkr, replaceKEMLtkr, newfiledata)


		for line in newfiledata:

			#print line
			#if 'false' not in line and 'cannot be proved' not in line:

			linetxt = line.replace("||", "|")
			#linetxt = linetxt.replace("is true.", "")




			linetxt = linetxt.replace("(event(eRevTpki(tpki))@j1 && i > j1)", "Ri")
			linetxt = linetxt.replace("(event(eRevTpki(tpki))@j2 && i > j2)", "Ri")
			linetxt = linetxt.replace("(event(eRevTpki(tpki))@j3 && i > j3)", "Ri")
			linetxt = linetxt.replace("(event(eRevTpki(tpki))@j4 && i > j4)", "Ri")

			linetxt = linetxt.replace("(event(eRevTpkr(tpkr))@j1 && i > j1)", "Rr")
			linetxt = linetxt.replace("(event(eRevTpkr(tpkr))@j2 && i > j2)", "Rr")
			linetxt = linetxt.replace("(event(eRevTpkr(tpkr))@j3 && i > j3)", "Rr")
			linetxt = linetxt.replace("(event(eRevTpkr(tpkr))@j4 && i > j4)", "Rr")

			
			linetxt = linetxt.replace("(event(eRevTpki(tpki))@j1 && j > j1)", "Ri")
			linetxt = linetxt.replace("(event(eRevTpki(tpki))@j2 && j > j2)", "Ri")
			linetxt = linetxt.replace("(event(eRevTpki(tpki))@j3 && j > j3)", "Ri")
			linetxt = linetxt.replace("(event(eRevTpki(tpki))@j4 && j > j4)", "Ri")

			linetxt = linetxt.replace("(event(eRevTpkr(tpkr))@j1 && j > j1)", "Rr")
			linetxt = linetxt.replace("(event(eRevTpkr(tpkr))@j2 && j > j2)", "Rr")
			linetxt = linetxt.replace("(event(eRevTpkr(tpkr))@j3 && j > j3)", "Rr")
			linetxt = linetxt.replace("(event(eRevTpkr(tpkr))@j4 && j > j4)", "Rr")



			linetxt = linetxt.replace("(event(eRevRa(ra_2))@j1 && j > j1)", "Ra")
			linetxt = linetxt.replace("(event(eRevRa(ra_2))@j2 && j > j2)", "Ra")
			linetxt = linetxt.replace("(event(eRevRa(ra_2))@j3 && j > j3)", "Ra")
			linetxt = linetxt.replace("(event(eRevRa(ra_2))@j4 && j > j4)", "Ra")
			linetxt = linetxt.replace("(event(eRevRa(ra_2))@j5 && j > j5)", "Ra")
			linetxt = linetxt.replace("(event(eRevRa(ra_2))@j6 && j > j6)", "Ra")
			linetxt = linetxt.replace("(event(eRevRa(ra_2))@j7 && j > j7)", "Ra")

			linetxt = linetxt.replace("(event(eRevRe(re_2))@j1 && j > j1)", "Re")
			linetxt = linetxt.replace("(event(eRevRe(re_2))@j2 && j > j2)", "Re")
			linetxt = linetxt.replace("(event(eRevRe(re_2))@j3 && j > j3)", "Re")
			linetxt = linetxt.replace("(event(eRevRe(re_2))@j4 && j > j4)", "Re")
			linetxt = linetxt.replace("(event(eRevRe(re_2))@j5 && j > j5)", "Re")
			linetxt = linetxt.replace("(event(eRevRe(re_2))@j6 && j > j6)", "Re")
			linetxt = linetxt.replace("(event(eRevRe(re_2))@j7 && j > j7)", "Re")
			linetxt = linetxt.replace("(event(eRevRe(re_2))@j8 && j > j8)", "Re")


			linetxt = linetxt.replace("(event(eRevRe(re_2))@j1 && i > j1)", "Re")
			linetxt = linetxt.replace("(event(eRevRe(re_2))@j2 && i > j2)", "Re")
			linetxt = linetxt.replace("(event(eRevRe(re_2))@j3 && i > j3)", "Re")
			linetxt = linetxt.replace("(event(eRevRe(re_2))@j4 && i > j4)", "Re")
			linetxt = linetxt.replace("(event(eRevRe(re_2))@j5 && i > j5)", "Re")
			linetxt = linetxt.replace("(event(eRevRe(re_2))@j6 && i > j6)", "Re")
			linetxt = linetxt.replace("(event(eRevRe(re_2))@j7 && i > j7)", "Re")
			linetxt = linetxt.replace("(event(eRevRe(re_2))@j8 && i > j8)", "Re")


			linetxt = linetxt.replace("(event(eRevRa(ra_2))@j1 && i > j1)", "Ra")
			linetxt = linetxt.replace("(event(eRevRa(ra_2))@j2 && i > j2)", "Ra")
			linetxt = linetxt.replace("(event(eRevRa(ra_2))@j3 && i > j3)", "Ra")
			linetxt = linetxt.replace("(event(eRevRa(ra_2))@j4 && i > j4)", "Ra")
			linetxt = linetxt.replace("(event(eRevRa(ra_2))@j5 && i > j5)", "Ra")
			linetxt = linetxt.replace("(event(eRevRa(ra_2))@j6 && i > j6)", "Ra")
			linetxt = linetxt.replace("(event(eRevRa(ra_2))@j7 && i > j7)", "Ra")

			linetxt = linetxt.replace("(event(eRevRb(rb_2))@j1 && j > j1)", "Rb")
			linetxt = linetxt.replace("(event(eRevRb(rb_2))@j2 && j > j2)", "Rb")
			linetxt = linetxt.replace("(event(eRevRb(rb_2))@j3 && j > j3)", "Rb")
			linetxt = linetxt.replace("(event(eRevRb(rb_2))@j4 && j > j4)", "Rb")
			linetxt = linetxt.replace("(event(eRevRb(rb_2))@j5 && j > j5)", "Rb")
			linetxt = linetxt.replace("(event(eRevRb(rb_2))@j6 && j > j6)", "Rb")
			linetxt = linetxt.replace("(event(eRevRb(rb_2))@j7 && j > j7)", "Rb")


			linetxt = linetxt.replace("(event(eRevRb(rb_2))@j1 && i > j1)", "Rb")
			linetxt = linetxt.replace("(event(eRevRb(rb_2))@j2 && i > j2)", "Rb")
			linetxt = linetxt.replace("(event(eRevRb(rb_2))@j3 && i > j3)", "Rb")
			linetxt = linetxt.replace("(event(eRevRb(rb_2))@j4 && i > j4)", "Rb")
			linetxt = linetxt.replace("(event(eRevRb(rb_2))@j5 && i > j5)", "Rb")
			linetxt = linetxt.replace("(event(eRevRb(rb_2))@j6 && i > j6)", "Rb")
			linetxt = linetxt.replace("(event(eRevRb(rb_2))@j7 && i > j7)", "Rb")

			"""
			linetxt = linetxt.replace("(event(eRevKa(ka_2))@j1 && i > j1)", "Ra")
			linetxt = linetxt.replace("(event(eRevKa(ka_2))@j2 && i > j2)", "Ra")
			linetxt = linetxt.replace("(event(eRevKa(ka_2))@j3 && i > j3)", "Ra")
			linetxt = linetxt.replace("(event(eRevKa(ka_2))@j4 && i > j4)", "Ra")
			linetxt = linetxt.replace("(event(eRevKa(ka_2))@j5 && i > j5)", "Ra")
			linetxt = linetxt.replace("(event(eRevKa(ka_2))@j6 && i > j6)", "Ra")
			linetxt = linetxt.replace("(event(eRevKa(ka_2))@j7 && i > j7)", "Ra")
			linetxt = linetxt.replace("(event(eRevKb(kb_2))@j1 && i > j1)", "Rb")
			linetxt = linetxt.replace("(event(eRevKb(kb_2))@j2 && i > j2)", "Rb")
			linetxt = linetxt.replace("(event(eRevKb(kb_2))@j3 && i > j3)", "Rb")
			linetxt = linetxt.replace("(event(eRevKb(kb_2))@j4 && i > j4)", "Rb")
			linetxt = linetxt.replace("(event(eRevKb(kb_2))@j5 && i > j5)", "Rb")
			linetxt = linetxt.replace("(event(eRevKb(kb_2))@j6 && i > j6)", "Rb")
			linetxt = linetxt.replace("(event(eRevKb(kb_2))@j7 && i > j7)", "Rb")
			"""
			linetxt = linetxt.replace("(event(eRevK(k_7))@j1 && i > j1)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_7))@j2 && i > j2)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_7))@j3 && i > j3)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_7))@j4 && i > j4)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_7))@j5 && i > j5)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_7))@j6 && i > j6)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_7))@j7 && i > j7)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_7))@j8 && i > j8)", "Rk")


			linetxt = linetxt.replace("(event(eRevK(k_7))@j1 && j > j1)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_7))@j2 && j > j2)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_7))@j3 && j > j3)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_7))@j4 && j > j4)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_7))@j5 && j > j5)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_7))@j6 && j > j6)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_7))@j7 && j > j7)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_7))@j8 && j > j8)", "Rk")


			linetxt = linetxt.replace("(event(eRevK(k_3))@j1 && j > j1)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_3))@j2 && j > j2)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_3))@j3 && j > j3)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_3))@j4 && j > j4)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_3))@j5 && j > j5)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_3))@j6 && j > j6)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_3))@j7 && j > j7)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_3))@j8 && j > j8)", "Rk")

			linetxt = linetxt.replace("(event(eRevK(k_2))@j1 && j > j1)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_2))@j2 && j > j2)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_2))@j3 && j > j3)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_2))@j4 && j > j4)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_2))@j5 && j > j5)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_2))@j6 && j > j6)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_2))@j7 && j > j7)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_2))@j8 && j > j8)", "Rk")


			linetxt = linetxt.replace("(event(eRevK(k_3))@j1 && i > j1)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_3))@j2 && i > j2)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_3))@j3 && i > j3)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_3))@j4 && i > j4)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_3))@j5 && i > j5)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_3))@j6 && i > j6)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_3))@j7 && i > j7)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_3))@j8 && i > j8)", "Rk")

			linetxt = linetxt.replace("(event(eRevK(k_2))@j1 && i > j1)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_2))@j2 && i > j2)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_2))@j3 && i > j3)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_2))@j4 && i > j4)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_2))@j5 && i > j5)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_2))@j6 && i > j6)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_2))@j7 && i > j7)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_2))@j8 && i > j8)", "Rk")

			"""
			linetxt = linetxt.replace("(event(eRevKa(ka_2))@j2 && j > j2)", "Ra")
			linetxt = linetxt.replace("(event(eRevKa(ka_2))@j3 && j > j3)", "Ra")
			linetxt = linetxt.replace("(event(eRevKa(ka_2))@j4 && j > j4)", "Ra")
			linetxt = linetxt.replace("(event(eRevKa(ka_2))@j5 && j > j5)", "Ra")
			linetxt = linetxt.replace("(event(eRevKa(ka_2))@j6 && j > j6)", "Ra")
			linetxt = linetxt.replace("(event(eRevKa(ka_2))@j7 && j > j7)", "Ra")
			linetxt = linetxt.replace("(event(eRevKb(kb_2))@j2 && j > j2)", "Rb")
			linetxt = linetxt.replace("(event(eRevKb(kb_2))@j3 && j > j3)", "Rb")
			linetxt = linetxt.replace("(event(eRevKb(kb_2))@j4 && j > j4)", "Rb")
			linetxt = linetxt.replace("(event(eRevKb(kb_2))@j5 && j > j5)", "Rb")
			linetxt = linetxt.replace("(event(eRevKb(kb_2))@j6 && j > j6)", "Rb")
			linetxt = linetxt.replace("(event(eRevKb(kb_2))@j7 && j > j7)", "Rb")
			"""
			linetxt = linetxt.replace("(event(eRevK(k_2))@j2 && j > j2)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_2))@j3 && j > j3)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_2))@j4 && j > j4)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_2))@j5 && j > j5)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_2))@j6 && j > j6)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_2))@j7 && j > j7)", "Rk")
			linetxt = linetxt.replace("(event(eRevK(k_2))@j8 && j > j8)", "Rk")



			linetxt = linetxt.replace("(event(eRevPri(pki))@j1 && i > j1)", "Ru")
			linetxt = linetxt.replace("(event(eRevPri(pki))@j2 && i > j2)", "Ru")
			linetxt = linetxt.replace("(event(eRevPri(pki))@j3 && i > j3)", "Ru")
			linetxt = linetxt.replace("(event(eRevPri(pki))@j4 && i > j4)", "Ru")
			linetxt = linetxt.replace("(event(eRevPri(pki))@j5 && i > j5)", "Ru")
			linetxt = linetxt.replace("(event(eRevPri(pki))@j6 && i > j6)", "Ru")

			linetxt = linetxt.replace("(event(eRevPri(pki))@j1 && i_4 > j1)", "Ru")


			linetxt = linetxt.replace("(event(eRevPri(pkr))@j1 && i > j1)", "Rv")
			linetxt = linetxt.replace("(event(eRevPri(pkr))@j2 && i > j2)", "Rv")
			linetxt = linetxt.replace("(event(eRevPri(pkr))@j3 && i > j3)", "Rv")
			linetxt = linetxt.replace("(event(eRevPri(pkr))@j4 && i > j4)", "Rv")
			linetxt = linetxt.replace("(event(eRevPri(pkr))@j5 && i > j5)", "Rv")
			linetxt = linetxt.replace("(event(eRevPri(pkr))@j6 && i > j6)", "Rv")

			linetxt = linetxt.replace("(event(eRevPri(pkr))@j2 && i_4 > j2)", "Rv")

			

			linetxt = linetxt.replace("(event(eRevPri(peki))@j1 && i > j1)", "Rx")
			linetxt = linetxt.replace("(event(eRevPri(peki))@j2 && i > j2)", "Rx")
			linetxt = linetxt.replace("(event(eRevPri(peki))@j3 && i > j3)", "Rx")
			linetxt = linetxt.replace("(event(eRevPri(peki))@j4 && i > j4)", "Rx")
			linetxt = linetxt.replace("(event(eRevPri(peki))@j5 && i > j5)", "Rx")
			linetxt = linetxt.replace("(event(eRevPri(peki))@j6 && i > j6)", "Rx")

			linetxt = linetxt.replace("(event(eRevPri(peki))@j3 && i_4 > j3)", "Rx")



			linetxt = linetxt.replace("==> (event(eRevPri(pki))@j1 && j > j1)", "Ru")
			linetxt = linetxt.replace("==> (event(eRevPri(pki))@j2 && j > j2)", "Ru")
			linetxt = linetxt.replace("==> (event(eRevPri(pki))@j3 && j > j3)", "Ru")
			linetxt = linetxt.replace("==> (event(eRevPri(pki))@j4 && j > j4)", "Ru")
			linetxt = linetxt.replace("==> (event(eRevPri(pki))@j5 && j > j5)", "Ru")
			linetxt = linetxt.replace("==> (event(eRevPri(pki))@j6 && j > j6)", "Ru")

			linetxt = linetxt.replace("==> (event(eRevPri(pkr))@j1 && j > j1)", "Rv")
			linetxt = linetxt.replace("==> (event(eRevPri(pkr))@j2 && j > j2)", "Rv")
			linetxt = linetxt.replace("==> (event(eRevPri(pkr))@j3 && j > j3)", "Rv")
			linetxt = linetxt.replace("==> (event(eRevPri(pkr))@j4 && j > j4)", "Rv")
			linetxt = linetxt.replace("==> (event(eRevPri(pkr))@j5 && j > j5)", "Rv")
			linetxt = linetxt.replace("==> (event(eRevPri(pkr))@j6 && j > j6)", "Rv")

			linetxt = linetxt.replace("==> (event(eRevPri(peki))@j1 && j > j1)", "Rx")
			linetxt = linetxt.replace("==> (event(eRevPri(peki))@j2 && j > j2)", "Rx")
			linetxt = linetxt.replace("==> (event(eRevPri(peki))@j3 && j > j3)", "Rx")
			linetxt = linetxt.replace("==> (event(eRevPri(peki))@j4 && j > j4)", "Rx")
			linetxt = linetxt.replace("==> (event(eRevPri(peki))@j5 && j > j5)", "Rx")
			linetxt = linetxt.replace("==> (event(eRevPri(peki))@j6 && j > j6)", "Rx")


			linetxt = linetxt.replace("(event(eRevPri(pki))@j1 && j > j1)", "Ru")
			linetxt = linetxt.replace("(event(eRevPri(pki))@j2 && j > j2)", "Ru")
			linetxt = linetxt.replace("(event(eRevPri(pki))@j3 && j > j3)", "Ru")
			linetxt = linetxt.replace("(event(eRevPri(pki))@j4 && j > j4)", "Ru")
			linetxt = linetxt.replace("(event(eRevPri(pki))@j5 && j > j5)", "Ru")
			linetxt = linetxt.replace("(event(eRevPri(pki))@j6 && j > j6)", "Ru")

			linetxt = linetxt.replace("event(eRevKEMLtki(kemltki))@j1 && j > j1", "Ru")
			linetxt = linetxt.replace("(event(eRevKEMLtki(kemltki))@j1 && j > j1)", "Ru")
			linetxt = linetxt.replace("(event(eRevKEMLtki(kemltki))@j2 && j > j2)", "Ru")
			linetxt = linetxt.replace("(eRevKEMLtki(kemltki))@j3 && j > j3)", "Ru")
			linetxt = linetxt.replace("(eRevKEMLtki(kemltki))@j4 && j > j4)", "Ru")
			linetxt = linetxt.replace("(eRevKEMLtki(kemltki))@j5 && j > j5)", "Ru")
			linetxt = linetxt.replace("(eRevKEMLtki(kemltki))@j6 && j > j6)", "Ru")



			linetxt = linetxt.replace("event(eRevLtki(pki))@j1 && j > j1", "Ru")
			linetxt = linetxt.replace("(event(eRevLtki(pki))@j1 && j > j1)", "Ru")
			linetxt = linetxt.replace("(event(eRevLtki(pki))@j2 && j > j2)", "Ru")
			linetxt = linetxt.replace("(event(eRevLtki(pki))@j3 && j > j3)", "Ru")
			linetxt = linetxt.replace("(event(eRevLtki(pki))@j4 && j > j4)", "Ru")
			linetxt = linetxt.replace("(event(eRevLtki(pki))@j5 && j > j5)", "Ru")
			linetxt = linetxt.replace("(event(eRevLtki(pki))@j6 && j > j6)", "Ru")

			linetxt = linetxt.replace("(event(eRevKEMLtki(kemltki))@j1 && i > j1)", "Ru")
			linetxt = linetxt.replace("(event(eRevKEMLtki(kemltki))@j2 && i > j2)", "Ru")
			linetxt = linetxt.replace("(event(eRevKEMLtki(kemltki))@j3 && i > j3)", "Ru")
			linetxt = linetxt.replace("(event(eRevKEMLtki(kemltki))@j4 && i > j4)", "Ru")
			linetxt = linetxt.replace("(event(eRevKEMLtki(kemltki))@j5 && i > j5)", "Ru")
			linetxt = linetxt.replace("(event(eRevKEMLtki(kemltki))@j6 && i > j6)", "Ru")


			linetxt = linetxt.replace("(event(eRevLtki(pki))@j1 && i > j1)", "Ru")
			linetxt = linetxt.replace("(event(eRevLtki(pki))@j2 && i > j2)", "Ru")
			linetxt = linetxt.replace("(event(eRevLtki(pki))@j3 && i > j3)", "Ru")
			linetxt = linetxt.replace("(event(eRevLtki(pki))@j4 && i > j4)", "Ru")
			linetxt = linetxt.replace("(event(eRevLtki(pki))@j5 && i > j5)", "Ru")
			linetxt = linetxt.replace("(event(eRevLtki(pki))@j6 && i > j6)", "Ru")


			linetxt = linetxt.replace("(event(eRevPri(pkr))@j1 && j > j1)", "Rv")
			linetxt = linetxt.replace("(event(eRevPri(pkr))@j2 && j > j2)", "Rv")
			linetxt = linetxt.replace("(event(eRevPri(pkr))@j3 && j > j3)", "Rv")
			linetxt = linetxt.replace("(event(eRevPri(pkr))@j4 && j > j4)", "Rv")
			linetxt = linetxt.replace("(event(eRevPri(pkr))@j5 && j > j5)", "Rv")
			linetxt = linetxt.replace("(event(eRevPri(pkr))@j6 && j > j6)", "Rv")

			linetxt = linetxt.replace("(event(eRevKEMLtkr(kemltkr))@j1 && i > j1)", "Rv")
			linetxt = linetxt.replace("(event(eRevKEMLtkr(kemltkr))@j2 && i > j2)", "Rv")
			linetxt = linetxt.replace("(event(eRevKEMLtkr(kemltkr))@j3 && i > j3)", "Rv")
			linetxt = linetxt.replace("(event(eRevKEMLtkr(kemltkr))@j4 && i > j4)", "Rv")
			linetxt = linetxt.replace("(event(eRevKEMLtkr(kemltkr))@j5 && i > j5)", "Rv")
			linetxt = linetxt.replace("(event(eRevKEMLtkr(kemltkr))@j6 && i > j6)", "Rv")

			linetxt = linetxt.replace("event(eRevKEMLtkr(kemltkr))@j1 && j > j1", "Rv")
			linetxt = linetxt.replace("(event(eRevKEMLtkr(kemltkr))@j1 && j > j1)", "Rv")
			linetxt = linetxt.replace("(event(eRevKEMLtkr(kemltkr))@j2 && j > j2)", "Rv")
			linetxt = linetxt.replace("(event(eRevKEMLtkr(kemltkr))@j3 && j > j3)", "Rv")
			linetxt = linetxt.replace("(event(eRevKEMLtkr(kemltkr))@j4 && j > j4)", "Rv")
			linetxt = linetxt.replace("(event(eRevKEMLtkr(kemltkr))@j5 && j > j5)", "Rv")
			linetxt = linetxt.replace("(event(eRevKEMLtkr(kemltkr))@j6 && j > j6)", "Rv")


			linetxt = linetxt.replace("(event(eRevLtkr(pkr))@j1 && i > j1)", "Rv")
			linetxt = linetxt.replace("(event(eRevLtkr(pkr))@j2 && i > j2)", "Rv")
			linetxt = linetxt.replace("(event(eRevLtkr(pkr))@j3 && i > j3)", "Rv")
			linetxt = linetxt.replace("(event(eRevLtkr(pkr))@j4 && i > j4)", "Rv")
			linetxt = linetxt.replace("(event(eRevLtkr(pkr))@j5 && i > j5)", "Rv")
			linetxt = linetxt.replace("(event(eRevLtkr(pkr))@j6 && i > j6)", "Rv")

			linetxt = linetxt.replace("event(eRevLtkr(pkr))@j1 && j > j1", "Rv")
			linetxt = linetxt.replace("(event(eRevLtkr(pkr))@j1 && j > j1)", "Rv")
			linetxt = linetxt.replace("(event(eRevLtkr(pkr))@j2 && j > j2)", "Rv")
			linetxt = linetxt.replace("(event(eRevLtkr(pkr))@j3 && j > j3)", "Rv")
			linetxt = linetxt.replace("(event(eRevLtkr(pkr))@j4 && j > j4)", "Rv")
			linetxt = linetxt.replace("(event(eRevLtkr(pkr))@j5 && j > j5)", "Rv")
			linetxt = linetxt.replace("(event(eRevLtkr(pkr))@j6 && j > j6)", "Rv")


			linetxt = linetxt.replace("(event(eRevPri(peki))@j1 && j > j1)", "Rx")
			linetxt = linetxt.replace("(event(eRevPri(peki))@j2 && j > j2)", "Rx")
			linetxt = linetxt.replace("(event(eRevPri(peki))@j3 && j > j3)", "Rx")
			linetxt = linetxt.replace("(event(eRevPri(peki))@j4 && j > j4)", "Rx")
			linetxt = linetxt.replace("(event(eRevPri(peki))@j5 && j > j5)", "Rx")
			linetxt = linetxt.replace("(event(eRevPri(peki))@j6 && j > j6)", "Rx")

			linetxt = linetxt.replace("(event(eRevKEMEki(kempeki))@j1 && i > j1)", "Rx")
			linetxt = linetxt.replace("(event(eRevKEMEki(kempeki))@j2 && i > j2)", "Rx")
			linetxt = linetxt.replace("(event(eRevKEMEki(kempeki))@j3 && i > j3)", "Rx")
			linetxt = linetxt.replace("(event(eRevKEMEki(kempeki))@j4 && i > j4)", "Rx")
			linetxt = linetxt.replace("(event(eRevKEMEki(kempeki))@j5 && i > j5)", "Rx")
			linetxt = linetxt.replace("(event(eRevKEMEki(kempeki))@j6 && i > j6)", "Rx")

			linetxt = linetxt.replace("(event(eRevKEMEki(kempeki))@j1 && j > j1)", "Rx")
			linetxt = linetxt.replace("(event(eRevKEMEki(kempeki))@j2 && j > j2)", "Rx")
			linetxt = linetxt.replace("(event(eRevKEMEki(kempeki))@j3 && j > j3)", "Rx")
			linetxt = linetxt.replace("(event(eRevKEMEki(kempeki))@j4 && j > j4)", "Rx")
			linetxt = linetxt.replace("(event(eRevKEMEki(kempeki))@j5 && j > j5)", "Rx")
			linetxt = linetxt.replace("(event(eRevKEMEki(kempeki))@j6 && j > j6)", "Rx")


			linetxt = linetxt.replace("(event(eRevEki(peki))@j1 && i > j1)", "Rx")
			linetxt = linetxt.replace("(event(eRevEki(peki))@j2 && i > j2)", "Rx")
			linetxt = linetxt.replace("(event(eRevEki(peki))@j3 && i > j3)", "Rx")
			linetxt = linetxt.replace("(event(eRevEki(peki))@j4 && i > j4)", "Rx")
			linetxt = linetxt.replace("(event(eRevEki(peki))@j5 && i > j5)", "Rx")
			linetxt = linetxt.replace("(event(eRevEki(peki))@j6 && i > j6)", "Rx")

			linetxt = linetxt.replace("(event(eRevEki(peki))@j1 && j > j1)", "Rx")
			linetxt = linetxt.replace("(event(eRevEki(peki))@j2 && j > j2)", "Rx")
			linetxt = linetxt.replace("(event(eRevEki(peki))@j3 && j > j3)", "Rx")
			linetxt = linetxt.replace("(event(eRevEki(peki))@j4 && j > j4)", "Rx")
			linetxt = linetxt.replace("(event(eRevEki(peki))@j5 && j > j5)", "Rx")
			linetxt = linetxt.replace("(event(eRevEki(peki))@j6 && j > j6)", "Rx")


			linetxt = linetxt.replace("(event(eRevPri(pekr))@j1 && i > j1)", "Ry")
			linetxt = linetxt.replace("(event(eRevPri(pekr))@j2 && i > j2)", "Ry")
			linetxt = linetxt.replace("(event(eRevPri(pekr))@j3 && i > j3)", "Ry")
			linetxt = linetxt.replace("(event(eRevPri(pekr))@j4 && i > j4)", "Ry")
			linetxt = linetxt.replace("(event(eRevPri(pekr))@j5 && i > j5)", "Ry")
			linetxt = linetxt.replace("(event(eRevPri(pekr))@j6 && i > j6)", "Ry")

			linetxt = linetxt.replace("(event(eRevEkr(pekr))@j1 && i > j1)", "Ry")
			linetxt = linetxt.replace("(event(eRevEkr(pekr))@j2 && i > j2)", "Ry")
			linetxt = linetxt.replace("(event(eRevEkr(pekr))@j3 && i > j3)", "Ry")
			linetxt = linetxt.replace("(event(eRevEkr(pekr))@j4 && i > j4)", "Ry")
			linetxt = linetxt.replace("(event(eRevEkr(pekr))@j5 && i > j5)", "Ry")
			linetxt = linetxt.replace("(event(eRevEkr(pekr))@j6 && i > j6)", "Ry")

			linetxt = linetxt.replace("(event(eRevEkr(pekr))@j1 && j > j1)", "Ry")
			linetxt = linetxt.replace("(event(eRevEkr(pekr))@j2 && j > j2)", "Ry")
			linetxt = linetxt.replace("(event(eRevEkr(pekr))@j3 && j > j3)", "Ry")
			linetxt = linetxt.replace("(event(eRevEkr(pekr))@j4 && j > j4)", "Ry")
			linetxt = linetxt.replace("(event(eRevEkr(pekr))@j5 && j > j5)", "Ry")
			linetxt = linetxt.replace("(event(eRevEkr(pekr))@j6 && j > j6)", "Ry")


			linetxt = linetxt.replace("(event(eRevPri(pekr))@j1 && j > j1)", "Ry")
			linetxt = linetxt.replace("(event(eRevPri(pekr))@j2 && j > j2)", "Ry")
			linetxt = linetxt.replace("(event(eRevPri(pekr))@j3 && j > j3)", "Ry")
			linetxt = linetxt.replace("(event(eRevPri(pekr))@j4 && j > j4)", "Ry")
			linetxt = linetxt.replace("(event(eRevPri(pekr))@j5 && j > j5)", "Ry")
			linetxt = linetxt.replace("(event(eRevPri(pekr))@j6 && j > j6)", "Ry")


			linetxt = linetxt.replace("(event(eRevPsk(psk_3))@j1 && i > j1)", "Rs")
			linetxt = linetxt.replace("(event(eRevPsk(psk_3))@j2 && i > j2)", "Rs")
			linetxt = linetxt.replace("(event(eRevPsk(psk_3))@j3 && i > j3)", "Rs")
			linetxt = linetxt.replace("(event(eRevPsk(psk_3))@j4 && i > j4)", "Rs")
			linetxt = linetxt.replace("(event(eRevPsk(psk_3))@j5 && i > j5)", "Rs")
			linetxt = linetxt.replace("(event(eRevPsk(psk_3))@j6 && i > j6)", "Rs")
			linetxt = linetxt.replace("(event(eRevPsk(psk_4))@j1 && i > j1)", "Rs")
			linetxt = linetxt.replace("(event(eRevPsk(psk_4))@j2 && i > j2)", "Rs")
			linetxt = linetxt.replace("(event(eRevPsk(psk_4))@j3 && i > j3)", "Rs")
			linetxt = linetxt.replace("(event(eRevPsk(psk_4))@j4 && i > j4)", "Rs")
			linetxt = linetxt.replace("(event(eRevPsk(psk_4))@j5 && i > j5)", "Rs")
			linetxt = linetxt.replace("(event(eRevPsk(psk_4))@j6 && i > j6)", "Rs")
			linetxt = linetxt.replace("(event(eRevPsk(psk_4))@j7 && i > j7)", "Rs")
			linetxt = linetxt.replace("(event(eRevPsk(psk_4))@j8 && i > j8)", "Rs")
			linetxt = linetxt.replace("(event(eRevPsk(psk_4))@j9 && i > j9)", "Rs")


			linetxt = linetxt.replace("event(eRevPsk(psk_3))@j1 && j > j1", "Rs")
			linetxt = linetxt.replace("(event(eRevPsk(psk_3))@j1 && j > j1)", "Rs")
			linetxt = linetxt.replace("(event(eRevPsk(psk_3))@j2 && j > j2)", "Rs")
			linetxt = linetxt.replace("(event(eRevPsk(psk_3))@j3 && j > j3)", "Rs")
			linetxt = linetxt.replace("(event(eRevPsk(psk_3))@j4 && j > j4)", "Rs")
			linetxt = linetxt.replace("(event(eRevPsk(psk_3))@j5 && j > j5)", "Rs")
			linetxt = linetxt.replace("(event(eRevPsk(psk_3))@j6 && j > j6)", "Rs")
			linetxt = linetxt.replace("(event(eRevPsk(psk_3))@j7 && j > j7)", "Rs")
			linetxt = linetxt.replace("(event(eRevPsk(psk_3))@j8 && j > j8)", "Rs")
			linetxt = linetxt.replace("(event(eRevPsk(psk_3))@j9 && j > j9)", "Rs")
			linetxt = linetxt.replace("event(eRevPsk(psk_4))@j1 && j > j1", "Rs")
			linetxt = linetxt.replace("(event(eRevPsk(psk_4))@j1 && j > j1)", "Rs")
			linetxt = linetxt.replace("(event(eRevPsk(psk_4))@j2 && j > j2)", "Rs")
			linetxt = linetxt.replace("(event(eRevPsk(psk_4))@j3 && j > j3)", "Rs")
			linetxt = linetxt.replace("(event(eRevPsk(psk_4))@j4 && j > j4)", "Rs")
			linetxt = linetxt.replace("(event(eRevPsk(psk_4))@j5 && j > j5)", "Rs")
			linetxt = linetxt.replace("(event(eRevPsk(psk_4))@j6 && j > j6)", "Rs")
			linetxt = linetxt.replace("(event(eRevPsk(psk_4))@j7 && j > j7)", "Rs")
			linetxt = linetxt.replace("(event(eRevPsk(psk_4))@j8 && j > j8)", "Rs")
			linetxt = linetxt.replace("(event(eRevPsk(psk_4))@j9 && j > j9)", "Rs")

			linetxt = linetxt.replace("(event(eRevPre(pki,pkr))@j1 && i > j1)", "Rc")

			linetxt = linetxt.replace("(event(eRevPre(pki,pkr))@j3 && i > j3)", "Rc")
			linetxt = linetxt.replace("(event(eRevPre(pki,pkr))@j4 && i > j4)", "Rc")

			linetxt = linetxt.replace("(event(eRevPre(pki,pkr))@j1 && j > j1)", "Rc")
			linetxt = linetxt.replace("(event(eRevPre(pki,pkr))@j2 && j > j2)", "Rc")
			linetxt = linetxt.replace("(event(eRevPre(pki,pkr))@j3 && j > j3)", "Rc")
			linetxt = linetxt.replace("(event(eRevPre(pki,pkr))@j4 && j > j4)", "Rc")
			linetxt = linetxt.replace("(event(eRevPre(pki,pkr))@j5 && j > j5)", "Rc")


			linetxt = linetxt.replace("(event(eRevPre(pki,pkr))@j4 && i_4 > j4)", "Rc")
			linetxt = linetxt.replace("(event(eRevPre(pki,pkr))@j3 && i_4 > j3)", "Rc")

			


			linetxt = linetxt.replace("RESULT event(IKeys(pki,pkr,peki,pekr,psk_3,ck_2))@i |", "")
			linetxt = linetxt.replace("RESULT event(IKeys(pki,pkr,peki,pekr,psk,ck_2))@i |", "")			
			linetxt = linetxt.replace("RESULT event(IKeys(pki,pkr,peki,pekr,psk_4,ck_4))@i |", "")			
			linetxt = linetxt.replace("RESULT event(IKeys(pki,pkr,peki,pekr,psk_4,ck_2))@i |", "")			

			linetxt = linetxt.replace("RESULT event(IKeys(pki,pkr,peki,pekr,psk_3,ck_2))@i", "")
			linetxt = linetxt.replace("RESULT event(IKeys(pki,pkr,peki,pekr,psk,ck_2))@i", "")
			linetxt = linetxt.replace("RESULT event(IKeys(pki,pkr,peki,pekr,psk_4,ck_4))@i", "")
			linetxt = linetxt.replace("RESULT event(IKeys(pki,pkr,peki,pekr,psk_4,ck_2))@i", "")

 
			linetxt = linetxt.replace("RESULT event(eRRec(pki,pkr,peki,k1,k2) |", "")
			linetxt = linetxt.replace("RESULT event(eRRec(pki,pkr,peki,k1,k2)  |", "")

			linetxt = linetxt.replace("RESULT event(eRRec(pki,pkr,peki,k1,k2)", "")

			linetxt = linetxt.replace("RESULT event(eRConfirm(pki,pkr,peki,pekr,psk_3,ck_2))@i  |", "")

			linetxt = linetxt.replace("RESULT event(eRConfirm(pki,pkr,peki,pekr,psk_3,ck_2))@i |", "")

			linetxt = linetxt.replace("RESULT event(eRConfirm(pki,pkr,peki,pekr,psk_3,ck_2))@i", "")

			linetxt = linetxt.replace("==> event(RKeys(pki,pkr,peki,pekr,psk_3,ck_2))@j1 && i > j1", "")
			linetxt = linetxt.replace("==> event(RKeys(pki,pkr,peki,pekr,psk_3,ck_2))@j6 && i > j6", "")
			linetxt = linetxt.replace("==> event(RKeys(pki,pkr,peki,pekr,psk_3,ck_2))@j && i > j", "")


			linetxt = linetxt.replace("==> (event(eISend(pki,pkr,peki,k1,k2))@j && i > j) ", "")
			linetxt = linetxt.replace("==> event(eISend(pki,pkr,peki,k1,k2))@j && i > j", "")


			linetxt = linetxt.replace("==> (event(RKeys(pki,pkr,peki,pekr,psk_3,ck_2))@j1 && i > j1)", "")
			linetxt = linetxt.replace("==> (event(RKeys(pki,pkr,peki,pekr,psk_3,ck_2))@j2 && i > j2)", "")			
			linetxt = linetxt.replace("==> (event(RKeys(pki,pkr,peki,pekr,psk_3,ck_2))@j3 && i > j3)", "")
			linetxt = linetxt.replace("==> (event(RKeys(pki,pkr,peki,pekr,psk_3,ck_2))@j4 && i > j4)", "")
			linetxt = linetxt.replace("==> (event(RKeys(pki,pkr,peki,pekr,psk_3,ck_2))@j5 && i > j5)", "")
			linetxt = linetxt.replace("==> (event(RKeys(pki,pkr,peki,pekr,psk_3,ck_2))@j6 && i > j6)", "")
			linetxt = linetxt.replace("==> (event(RKeys(pki,pkr,peki,pekr,psk_3,ck_2))@j && i > j)", "")
			linetxt = linetxt.replace("==> (event(RKeys(pki,pkr,peki,pekr,psk,ck_2))@j && i > j)", "")
			linetxt = linetxt.replace("==> (event(RKeys(pki,pkr,peki,pekr,psk_4,ck_4))@j && i > j)", "")
			linetxt = linetxt.replace("==> (event(RKeys(pki,pkr,peki,pekr,psk_4,ck_2))@j && i > j)", "")



			linetxt = linetxt.replace("==> (event(eIConfirm(pki,pkr,peki,pekr,psk_3,ck_2))@j1 && i > j1)", "")
			linetxt = linetxt.replace("==> event(eIConfirm(pki,pkr,peki,pekr,psk_3,ck_2))@j1 && i > j1", "")
			linetxt = linetxt.replace("==> (event(eIConfirm(pki,pkr,peki,pekr,psk_3,ck_2))@j3 && i > j3)", "")
			linetxt = linetxt.replace("==> event(eIConfirm(pki,pkr,peki,pekr,psk_3,ck_2))@j6 && i > j6", "")
			linetxt = linetxt.replace("==> (event(eIConfirm(pki,pkr,peki,pekr,psk_3,ck_2))@j && i > j)", "")
			linetxt = linetxt.replace("==> event(eIConfirm(pki,pkr,peki,pekr,psk_3,ck_2))@j && i > j", "")


			linetxt = linetxt.replace("RESULT event(I_Time(ts,pki,pkr,peki))@i && attacker(ts)@j ==>", "")
			linetxt = linetxt.replace("RESULT event(R_Time(ts,pki,pkr,peki))@i && attacker(ts)@j", "")
			linetxt = linetxt.replace("==> event(eRevPri(pki))@j1", "| Ru")
			linetxt = linetxt.replace("==> event(eRevPri(pkr))@j1", "| Rv")



			linetxt = linetxt.replace("(event(eRevPre(pki,pkr))@j2 && i > j2)", "Rc")
			linetxt = linetxt.replace("(event(eRevPre(pki,pkr))@j5 && i > j5)", "Rc")

			
			linetxt = linetxt.replace("event(eRevPre(pki,pkr))@j2", "Rc")
			linetxt = linetxt.replace("event(eRevPre(pki,pkr))@j3", "Rc")
			linetxt = linetxt.replace("event(eRevPre(pki,pkr))@j4", "Rc")


			linetxt = linetxt.replace("event(eRevPri(pkr))@j2", "Rv")
			linetxt = linetxt.replace("event(eRevPri(peki))@j2", "Rx")
			linetxt = linetxt.replace("event(eRevPri(peki))@j3", "Rx")

			linetxt = linetxt.replace("==>", "")

			linetxt = linetxt.replace("(Ru)", "Ru")
			linetxt = linetxt.replace("(Rv)", "Rv")

			newfile.write(linetxt)
	infile.close()
	newfile.close()

	
	if os.stat(arg1+'.new').st_size != 0:
		with open(arg1+'.new') as infile, open(arg1+'.inter', 'w') as newfile:
			data = "("
			firstline = infile.readline()
			if firstline.startswith(' | '):
				data = data + firstline.rstrip('\n')[3:]
			else:
				data = data + firstline.rstrip('\n')	
			data = data + ")"
			if data.startswith(' | '):
				data = data[3:]
			for line in infile:
				if line.startswith(' | '):
					linetxt = line[3:]
					linetxt = linetxt.replace("\n", "")
					data = data + " & "+ " (" + linetxt + ") "
				else:
					linetxt = line.replace("\n", "")
					data = data + " & "+ " (" + linetxt + ") "
			newfile.write(data)	
		#resdnf = to_dnf(data, simplify=True, force=True)
		#print("DNF =", resdnf)
		#rescnf = to_cnf(data, simplify=True, force=True)
		#print("CNF =", rescnf)

	infile.close()
	newfile.close()


	with open('prefix.txt') as infile, open('prefix.inter', 'w') as newfile:
		data = infile.readline()
		if ('all_trusted' in data):
			datacomp = ""
			newfile.write(datacomp)
		if ('_ltki' in data):
			datacomp = " & Mu"
			newfile.write(datacomp)
		if ('_ltkr' in data):
			datacomp = " & Mv"
			newfile.write(datacomp)
		if ('_pki' in data):
			datacomp = " & Du"
			newfile.write(datacomp)
		if ('_pkr' in data):
			datacomp = " & Dv"
			newfile.write(datacomp)
		if ('_eki' in data):
			datacomp = " & Mx"
			newfile.write(datacomp)
		if ('_ekr' in data):
			datacomp = " & My"
			newfile.write(datacomp)
		if ('_precomp_i' in data):
			datacomp = " & Mi"
			newfile.write(datacomp)
		if ('_precomp_r' in data):
			datacomp = " & Mr"
			newfile.write(datacomp)
		if ('_psk' in data):
			datacomp = " & Ms"
			newfile.write(datacomp)
	infile.close()
	newfile.close()

	with open('prefix.inter') as infile, open('prefix.comp', 'w') as newfile:
		datacomp = infile.readline()
		datacomplete = datacomp[3:]
		newfile.write(datacomplete)
	infile.close()
	newfile.close()


	with open(arg1+'.comp', 'w') as newfile:
		if os.stat(arg1+'.new').st_size != 0:
			with open(arg1+'.inter', 'r') as infile:
				datacomp = infile.read()
		else:
			datacomp = ""
		newfile.write(datacomp)
	infile.close()
	newfile.close()


	Ru, Rv, Rx, Ri, Rr, Rk, Ra, Rb, Rs = symbols("Ru, Rv, Rx, Ri, Rr, Rk, Ra, Rb, Rs")


	with open(arg1+'.cnf', 'w') as newfile:
		with open('prefix.comp', 'r') as infile2:
			if os.stat(arg1+'.new').st_size != 0:
				with open(arg1+'.comp', 'r') as infile:
					data = infile.read()
					cnf = to_cnf(data, simplify=True, force=True)
					#cnf = data
				if((str(cnf)[0] == "R") | ((str(cnf)[0] == "(") & (str(cnf)[1] == "R"))):
					if os.stat('prefix.comp').st_size !=0:
						newfile.write(infile2.read()+" & ("+str(cnf)+")")
					else:
						newfile.write("("+str(cnf)+")")
				else:
					newfile.write(str(cnf))
			else:
				if os.stat('prefix.comp').st_size !=0:
					newfile.write(infile2.read())
				else:
					newfile.write("")
	infile.close()
	newfile.close()

	
	Ru, Rv, Rx, Ri, Rr, Rk, Ra, Rb, Rs = symbols("Ru, Rv, Rx, Ri, Rr, Rk, Ra, Rb, Rs")


	with open(arg1+'.dnf', 'w') as newfile:
		if os.stat(arg1+'.cnf').st_size != 0:
			with open(arg1+'.cnf', 'r') as infile:
				data = infile.read()
				dnf = to_dnf(data, simplify=True, force=True)
				newfile.write(str(dnf))
		else:
			newfile.write("")
	
	

if __name__ == "__main__":
    main(sys.argv[1])