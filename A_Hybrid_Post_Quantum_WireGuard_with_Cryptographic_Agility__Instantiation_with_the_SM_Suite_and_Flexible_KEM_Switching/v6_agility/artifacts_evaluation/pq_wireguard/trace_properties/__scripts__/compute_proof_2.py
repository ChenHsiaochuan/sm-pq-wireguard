#!/usr/bin/env python3.6
'''
Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
'''


import os

import sys

import re

import itertools

from subprocess import PIPE, Popen, DEVNULL

TAMARIN="~/.local/bin/tamarin-prover"
#PROVERIF="proverif"
#PROVERIF="../../../../../proverif2.04/./proverif"

def update_files(file_to_read, file_to_write):

	with open(file_to_read, 'r') as infile:
		filedata = infile.read()

		#filedata = filedata.replace("free att:channel.\n", "set preciseActions = true.\nfree att:channel.\n")

		filedata = filedata.replace("type nat.\n", "")
		filedata = filedata.replace("new dhekI_1:bitstring;", "new dhekI_1[]:bitstring;")
		filedata = filedata.replace("new ra_1:bitstring;", "new ra_1[]:bitstring;")
		filedata = filedata.replace("new rb_1:bitstring;", "new rb_1[]:bitstring;")
		filedata = filedata.replace("new re_1:bitstring;", "new re_1[]:bitstring;")
		filedata = filedata.replace("new ka_1:bitstring;", "new ka_1[]:bitstring;")
		filedata = filedata.replace("new kb_1:bitstring;", "new kb_1[]:bitstring;")
		filedata = filedata.replace("new ke_1:bitstring;", "new ke_1[]:bitstring;")
		filedata = filedata.replace("new kemekI_1:bitstring;", "new kemekI_1[]:bitstring;")
		filedata = filedata.replace("new sidI_1:bitstring;", "new sidI_1[]:bitstring;")
		filedata = filedata.replace("new ts_1:bitstring;", "new ts_1[]:bitstring;")
		filedata = filedata.replace("new firstI_1:bitstring;", "new firstI_1[]:bitstring;")
		filedata = filedata.replace("new messageI1_1:bitstring;", "new messageI1_1[]:bitstring;")

		#filedata = filedata.replace("new ra_1:bitstring;", "new ra_1[]:bitstring;")
		#filedata = filedata.replace("new re_1:bitstring;", "new re_1[]:bitstring;")
		filedata = filedata.replace("new sidR_1:bitstring;", "new sidR_1[]:bitstring;")
		#filedata = filedata.replace("new stp1_1:bitstring;", "new stp1_1[]:bitstring;")
		filedata = filedata.replace("new messageR0_1:bitstring;", "new messageR0_1[]:bitstring;")


	with open(file_to_write, 'w') as outfile:
		#outfile.write("set preciseActions = true.\n")
		outfile.write(filedata)


def update_files_without_precise(file_to_read, file_to_write):

	with open(file_to_read, 'r') as infile:
		filedata = infile.read()
		#filedata = filedata.replace("free att:channel.\n", "set preciseActions = true.\nfree att:channel.\n")
		filedata = filedata.replace("type nat.\n", "")
		filedata = filedata.replace("fun decaps(bitstring,bitstring):bitstring.\n", "")
		filedata = filedata.replace("fun encaps(bitstring,bitstring):bitstring.\n", "")

		filedata = filedata.replace("new dhekI_1:bitstring;", "new dhekI_1[]:bitstring;")
		filedata = filedata.replace("new ra_1:bitstring;", "new ra_1[]:bitstring;")
		filedata = filedata.replace("new rb_1:bitstring;", "new rb_1[]:bitstring;")
		filedata = filedata.replace("new re_1:bitstring;", "new re_1[]:bitstring;")
		filedata = filedata.replace("new ka_1:bitstring;", "new ka_1[]:bitstring;")
		filedata = filedata.replace("new kb_1:bitstring;", "new kb_1[]:bitstring;")
		filedata = filedata.replace("new ke_1:bitstring;", "new ke_1[]:bitstring;")
		filedata = filedata.replace("new kemekI_1:bitstring;", "new kemekI_1[]:bitstring;")
		filedata = filedata.replace("new sidI_1:bitstring;", "new sidI_1[]:bitstring;")
		filedata = filedata.replace("new ts_1:bitstring;", "new ts_1[]:bitstring;")
		filedata = filedata.replace("new firstI_1:bitstring;", "new firstI_1[]:bitstring;")
		filedata = filedata.replace("new messageI1_1:bitstring;", "new messageI1_1[]:bitstring;")

		#filedata = filedata.replace("new ra_1:bitstring;", "new ra_1[]:bitstring;")
		#filedata = filedata.replace("new re_1:bitstring;", "new re_1[]:bitstring;")
		filedata = filedata.replace("new sidR_1:bitstring;", "new sidR_1[]:bitstring;")
		#filedata = filedata.replace("new stp1_1:bitstring;", "new stp1_1[]:bitstring;")
		filedata = filedata.replace("new messageR0_1:bitstring;", "new messageR0_1[]:bitstring;")

		#filedata = filedata.replace("reduc forall k:bitstring, m:bitstring;   ladec(laenc(m, pk(k)), k) = m.", "reduc forall k:bitstring, m:bitstring;   ladec(laenc(m, pk(k)), k) = m[private].")




		#filedata = filedata.replace("reduc forall k:bitstring, m:bitstring;   checkmac(k, m, mac(k, m)) = okay.", "reduc forall k:bitstring, m:bitstring;   checkmac(k, m, mac(k, m)) = okay.\nletfun aenc1(m:bitstring, pu:bitstring) = aenc((m, h(m)), pu).\nletfun adec1(c:bitstring, pr:bitstring) = adec(c, pr).\nletfun encaps(pu:bitstring, k:bitstring) = (aenc1(k, pu), h(k)).\nletfun decaps(pr:bitstring, c:bitstring) = h(adec(c, pr)).\n\n")

		'''
		letfun aenc1(m:bitstring, pu:bitstring) = aenc((m, h(m)), pu).
		letfun adec1(c:bitstring, pr:bitstring) = adec(c, pr).
		letfun encaps(pu:bitstring, k:bitstring) = (aenc1(k, pu), h(k)).
		letfun decaps(pr:bitstring, c:bitstring) = h(adec(c, pr)).
		'''


	with open(file_to_write, 'w') as outfile:
		#outfile.write("set preciseActions = true.\n")
		outfile.write(filedata)


def update_files_with_precise(file_to_read, file_to_write):

	with open(file_to_read, 'r') as infile:
		filedata = infile.read()
		#filedata = filedata.replace("free att:channel.\n", "set preciseActions = true.\nfree att:channel.\n")
		filedata = filedata.replace("fun decaps(bitstring,bitstring):bitstring.\n", "")
		filedata = filedata.replace("fun encaps(bitstring,bitstring):bitstring.\n", "")

		filedata = filedata.replace("new dhekI_1:bitstring;", "new dhekI_1[]:bitstring;")
		filedata = filedata.replace("new ra_1:bitstring;", "new ra_1[]:bitstring;")
		filedata = filedata.replace("new rb_1:bitstring;", "new rb_1[]:bitstring;")
		filedata = filedata.replace("new re_1:bitstring;", "new re_1[]:bitstring;")
		filedata = filedata.replace("new ka_1:bitstring;", "new ka_1[]:bitstring;")
		filedata = filedata.replace("new kb_1:bitstring;", "new kb_1[]:bitstring;")
		filedata = filedata.replace("new ke_1:bitstring;", "new ke_1[]:bitstring;")
		filedata = filedata.replace("new kemekI_1:bitstring;", "new kemekI_1[]:bitstring;")
		filedata = filedata.replace("new sidI_1:bitstring;", "new sidI_1[]:bitstring;")
		filedata = filedata.replace("new ts_1:bitstring;", "new ts_1[]:bitstring;")
		filedata = filedata.replace("new firstI_1:bitstring;", "new firstI_1[]:bitstring;")
		filedata = filedata.replace("new messageI1_1:bitstring;", "new messageI1_1[]:bitstring;")

		#filedata = filedata.replace("new ra_1:bitstring;", "new ra_1[]:bitstring;")
		#filedata = filedata.replace("new re_1:bitstring;", "new re_1[]:bitstring;")
		filedata = filedata.replace("new sidR_1:bitstring;", "new sidR_1[]:bitstring;")
		#filedata = filedata.replace("new stp1_1:bitstring;", "new stp1_1[]:bitstring;")
		filedata = filedata.replace("new messageR0_1:bitstring;", "new messageR0_1[]:bitstring;")

		#filedata = filedata.replace("reduc forall k:bitstring, m:bitstring;   ladec(laenc(m, pk(k)), k) = m.", "reduc forall k:bitstring, m:bitstring;   ladec(laenc(m, pk(k)), k) = m[private].")


		#filedata = filedata.replace("reduc forall k:bitstring, m:bitstring;   checkmac(k, m, mac(k, m)) = okay.", "reduc forall k:bitstring, m:bitstring;   checkmac(k, m, mac(k, m)) = okay.\nletfun aenc1(m:bitstring, pu:bitstring) = aenc((m, h(m)), pu).\nletfun adec1(c:bitstring, pr:bitstring) = adec(c, pr).\nletfun encaps(pu:bitstring, k:bitstring) = (aenc1(k, pu), h(k)).\nletfun decaps(pr:bitstring, c:bitstring) = h(adec(c, pr)).\n\n\n\n")


		filedata = filedata.replace("in(att,(=sxI, (sidI_1:bitstring, (dhpekI_1:bitstring, (kempekI_1:bitstring, (ct1_1:bitstring, (astat_1:bitstring, (ats_1:bitstring, macI1_1:bitstring))))))));", "in(att,(=sxI, (sidI_1:bitstring, (dhpekI_1:bitstring, (kempekI_1:bitstring, (ct1_1:bitstring, (astat_1:bitstring, (ats_1:bitstring, macI1_1:bitstring))))))));\n\t\t\tnew stp1_1[]:bitstring;\n\t\t\tevent eTest1( stp1_1, kempekI_1);\n\n")
		filedata = filedata.replace("noselect x:bitstring; attacker(exp(g,x)).", "noselect x:bitstring; attacker(exp(g,x)).\naxiom x: bitstring, y: bitstring, z: bitstring; event(eTest1(x, y)) && event(eTest1(x, z)) ==> y = z.\n\n")
		filedata = filedata.replace("event eRevTpkr(bitstring).", "event eRevTpkr(bitstring).\nevent eTest1(bitstring,bitstring).\n\n")


	with open(file_to_write, 'w') as outfile:
		#outfile.write("set preciseActions = true.\n")
		outfile.write(filedata)


def update_files_pfs(file_to_read, file_to_write):

	with open(file_to_read, 'r') as infile:
		filedata = infile.read()
		#filedata = filedata.replace("free att:channel.\n", "set preciseActions = true.\nfree att:channel.\n")
		filedata = filedata.replace("type nat.\n", "")
		filedata = filedata.replace("new dhekI_1:bitstring;", "new dhekI_1[]:bitstring;")
		filedata = filedata.replace("new ra_1:bitstring;", "new ra_1[]:bitstring;")
		filedata = filedata.replace("new rb_1:bitstring;", "new rb_1[]:bitstring;")
		filedata = filedata.replace("new re_1:bitstring;", "new re_1[]:bitstring;")
		filedata = filedata.replace("new ka_1:bitstring;", "new ka_1[]:bitstring;")
		filedata = filedata.replace("new kb_1:bitstring;", "new kb_1[]:bitstring;")
		filedata = filedata.replace("new ke_1:bitstring;", "new ke_1[]:bitstring;")
		filedata = filedata.replace("new kemekI_1:bitstring;", "new kemekI_1[]:bitstring;")
		filedata = filedata.replace("new sidI_1:bitstring;", "new sidI_1[]:bitstring;")
		filedata = filedata.replace("new ts_1:bitstring;", "new ts_1[]:bitstring;")
		filedata = filedata.replace("new firstI_1:bitstring;", "new firstI_1[]:bitstring;")
		filedata = filedata.replace("new messageI1_1:bitstring;", "new messageI1_1[]:bitstring;")

		#filedata = filedata.replace("new ra_1:bitstring;", "new ra_1[]:bitstring;")
		#filedata = filedata.replace("new re_1:bitstring;", "new re_1[]:bitstring;")
		filedata = filedata.replace("new sidR_1:bitstring;", "new sidR_1[]:bitstring;")
		#filedata = filedata.replace("new stp1_1:bitstring;", "new stp1_1[]:bitstring;")
		filedata = filedata.replace("new messageR0_1:bitstring;", "new messageR0_1[]:bitstring;")

		#filedata = filedata.replace("in(att,(=sxI, (sidI_1:bitstring, (dhpekI_1:bitstring, (kempekI_1:bitstring, (ct1_1:bitstring, (astat_1:bitstring, (ats_1:bitstring, macI1_1:bitstring))))))));", "in(att,(=sxI, (sidI_1:bitstring, (dhpekI_1:bitstring, (kempekI_1:bitstring, (ct1_1:bitstring, (astat_1:bitstring, (ats_1:bitstring, macI1_1:bitstring))))))));\n\t\t\tnew stp1_1[]:bitstring;\n\t\t\tevent eTest1( stp1_1, dhpekI_1);\n\n")
		#filedata = filedata.replace("noselect x:bitstring; attacker(exp(g,x)).", "noselect x:bitstring; attacker(exp(g,x)).\naxiom x: bitstring, y: bitstring, z: bitstring; event(eTest1(x, y)) && event(eTest1(x, z)) ==> y = z.\n\n")
		#filedata = filedata.replace("event eRevTpkr(bitstring).", "event eRevTpkr(bitstring).\nevent eTest1(bitstring,bitstring).\n\n")


		filedata = filedata.replace("(RevealPsk(psk_1))", "(phase 1; RevealPsk(psk_1))")
		filedata = filedata.replace("(RevealKEMLtkr(kemltkR_1))", "(phase 1; RevealKEMLtkr(kemltkR_1))")
		filedata = filedata.replace("(RevealKEMLtki(kemltkI_1))", "(phase 1; RevealKEMLtki(kemltkI_1))")


	with open(file_to_write, 'w') as outfile:
		outfile.write(filedata)


def update_files_pfs_r(file_to_read, file_to_write):

	with open(file_to_read, 'r') as infile:
		filedata = infile.read()
		filedata = filedata.replace("type nat.\n", "")
		#filedata = filedata.replace("new ekI_1:bitstring;", "new ekI_1[]:bitstring;")
		filedata = filedata.replace("new sidI_1:bitstring;", "new sidI_1[]:bitstring;")
		filedata = filedata.replace("new ts_1:bitstring;", "new ts_1[]:bitstring;")
		filedata = filedata.replace("new firstI_1:bitstring;", "new firstI_1[]:bitstring;")
		filedata = filedata.replace("new messageI1_1:bitstring;", "new messageI1_1[]:bitstring;")

		filedata = filedata.replace("new ekR_1:bitstring;", "new ekR_1[]:bitstring;")
		filedata = filedata.replace("new sidR_1:bitstring;", "new sidR_1[]:bitstring;")
		filedata = filedata.replace("new stp1_1:bitstring;", "new stp1_1[]:bitstring;")
		filedata = filedata.replace("new messageR0_1:bitstring;", "new messageR0_1[]:bitstring;")
		#filedata = filedata.replace("process", "axiom x: bitstring, y: bitstring, z: bitstring; event(eTest(x, y)) && event(eTest(x, z)) ==> y = z."+"\n\n"+"noselect x:bitstring; attacker(exp(g,x))."+'\n\n'+"process")
		filedata = filedata.replace("(RevealPsk(psk_1))", "(phase 1; RevealPsk(psk_1))")
		filedata = filedata.replace("(RevealLtkr(ltkR_1))", "(phase 1; RevealLtkr(ltkR_1))")
		filedata = filedata.replace("(RevealLtki(ltkI_1))", "(phase 1; RevealLtki(ltkI_1))")
		filedata = filedata.replace("(RevealPre(ltkI_1, ltkR_1))", "(phase 1; RevealPre(ltkI_1, ltkR_1))")

	with open(file_to_write, 'w') as outfile:
		outfile.write(filedata)

def generate_files_unilateral(filename, path):

	word = "query"


	subkeys = ["kemltki", "kemltkr", "tpki", "tpkr", "kemeki", "ra", "rb", "re", "psk"]

	S1c = list(itertools.combinations(subkeys, 1))
	S2c = list(itertools.combinations(subkeys, 2))
	S3c = list(itertools.combinations(subkeys, 3))
	S4c = list(itertools.combinations(subkeys, 4))
	S5c = list(itertools.combinations(subkeys, 5))
	S6c = list(itertools.combinations(subkeys, 6))
	S7c = list(itertools.combinations(subkeys, 7))
	S8c = list(itertools.combinations(subkeys, 8))
	S9c = list(itertools.combinations(subkeys, 9))
	#S10c = list(itertools.combinations(subkeys, 10))
	#S11c = list(itertools.combinations(subkeys, 11))
	#S12c = list(itertools.combinations(subkeys, 12))
	#S13c = list(itertools.combinations(subkeys, 13))
	#S14c = list(itertools.combinations(subkeys, 14))


	Sc = S1c+S2c+S3c+S4c+S5c+S6c+S7c+S8c+S9c


	#count = -2

	with open(filename, 'r') as f:
		content = f.read()
		words = content.split()
		words = re.findall(r'\b\w+\b', content)
		count = words.count(word)

	    #for line in f:
	        #words = line.split()
	        #for i in words:
	            #if(i==word):
	                #count=count+1
	f.close()
	


	firstquery = -1
	with open(filename, 'r') as f:
	    for i, line in enumerate(f, start=1):
	    	if word in line:
	    		firstquery = firstquery+i
	    		break
	f.close()

	for i in range(0,count):
		with open(filename, 'r') as infile:
			with open("../"+path+"/"+filename[:-3]+"_"+str(i)+".pv", 'w') as outfile:
				lines = infile.readlines()
				for index in range(0, len(lines)):
					if word in lines[firstquery]:
						if(index < firstquery):
							outfile.write(lines[index])
						if(index == firstquery+4*i):
							outfile.write(lines[index])
						if(index == firstquery+4*i+1):
							outfile.write(lines[index])
						if(index == firstquery+4*i+2):
							outfile.write(lines[index])
						if(index == firstquery+4*i+3):
							outfile.write(lines[index])
						if(index>=firstquery+count*4):
							outfile.write(lines[index])
	
	for i in range(1,count):
		with open("../"+path+"/"+filename[:-3]+"_"+str(i)+".pv", 'r') as infile:
			fdata = infile.read()
			key = ""
			for j in range(0, len(Sc[i-1])):
				key = key+"_"+Sc[i-1][j]
			with open("../"+path+"/"+filename[:-3]+key+".pv", 'w') as outfile:
				outfile.write(fdata)
			infile.close()
			os.remove("../"+path+"/"+filename[:-3]+"_"+str(i)+".pv")
			with open("../"+path+"/wireguard_command", "a") as commandfile:
				commandfile.write("proverif"+" "+filename[:-3]+key+".pv"+" > "+filename[:-3]+key+".pv.log"+"\n")
			commandfile.close()

	with open("../"+path+"/wireguard_command", "r") as commandfile:
		lines = commandfile.readlines()
		#print(len(lines))
		for index in range(0, len(lines)):
			if lines[index].count('_') == 10:
				with open("../"+path+"/wireguard_command_1", "a") as commandfile1:
					commandfile1.write(lines[index])
				commandfile1.close()
				with open("../"+path+"/wireguard_command_1", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".1log")
				infile.close()
				with open("../"+path+"/wireguard_command_1_opt", "w") as outfile:
					outfile.write(new_content)
				outfile.close()

			if lines[index].count('_') == 12:
				with open("../"+path+"/wireguard_command_2", "a") as commandfile2:
					commandfile2.write(lines[index])
				commandfile2.close()

				with open("../"+path+"/wireguard_command_2", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".2log")
				infile.close()
				with open("../"+path+"/wireguard_command_2", "w") as outfile:
					outfile.write(new_content)
				outfile.close()

			if lines[index].count('_') == 14:
				with open("../"+path+"/wireguard_command_3", "a") as commandfile3:
					commandfile3.write(lines[index])
				commandfile3.close()

				with open("../"+path+"/wireguard_command_3", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".3log")
				infile.close()
				with open("../"+path+"/wireguard_command_3", "w") as outfile:
					outfile.write(new_content)
				outfile.close()


			if lines[index].count('_') == 16:
				with open("../"+path+"/wireguard_command_4", "a") as commandfile4:
					commandfile4.write(lines[index])
				commandfile4.close()

				with open("../"+path+"/wireguard_command_4", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".4log")
				infile.close()
				with open("../"+path+"/wireguard_command_4", "w") as outfile:
					outfile.write(new_content)
				outfile.close()


			if lines[index].count('_') == 18:
				with open("../"+path+"/wireguard_command_5", "a") as commandfile5:
					commandfile5.write(lines[index])
				commandfile5.close()


				with open("../"+path+"/wireguard_command_5", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".5log")
				infile.close()
				with open("../"+path+"/wireguard_command_5", "w") as outfile:
					outfile.write(new_content)
				outfile.close()


			if lines[index].count('_') == 20:
				with open("../"+path+"/wireguard_command_6", "a") as commandfile6:
					commandfile6.write(lines[index])
				commandfile6.close()

				with open("../"+path+"/wireguard_command_6", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".6log")
				infile.close()
				with open("../"+path+"/wireguard_command_6", "w") as outfile:
					outfile.write(new_content)
				outfile.close()


			if lines[index].count('_') == 22:
				with open("../"+path+"/wireguard_command_7", "a") as commandfile7:
					commandfile7.write(lines[index])
				commandfile7.close()

				with open("../"+path+"/wireguard_command_7", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".7log")
				infile.close()
				with open("../"+path+"/wireguard_command_7", "w") as outfile:
					outfile.write(new_content)
				outfile.close()



			if lines[index].count('_') == 24:
				with open("../"+path+"/wireguard_command_8", "a") as commandfile8:
					commandfile8.write(lines[index])
				commandfile8.close()

				with open("../"+path+"/wireguard_command_8", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".8log")
				infile.close()
				with open("../"+path+"/wireguard_command_8", "w") as outfile:
					outfile.write(new_content)
				outfile.close()


			if lines[index].count('_') == 26:
				with open("../"+path+"/wireguard_command_9", "a") as commandfile8:
					commandfile8.write(lines[index])
				commandfile8.close()

				with open("../"+path+"/wireguard_command_9", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".9log")
				infile.close()
				with open("../"+path+"/wireguard_command_9", "w") as outfile:
					outfile.write(new_content)
				outfile.close()


			if lines[index].count('_') == 28:
				with open("../"+path+"/wireguard_command_10", "a") as commandfile8:
					commandfile8.write(lines[index])
				commandfile8.close()

				with open("../"+path+"/wireguard_command_10", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".10log")
				infile.close()
				with open("../"+path+"/wireguard_command_10", "w") as outfile:
					outfile.write(new_content)
				outfile.close()


			if lines[index].count('_') == 30:
				with open("../"+path+"/wireguard_command_11", "a") as commandfile8:
					commandfile8.write(lines[index])
				commandfile8.close()

				with open("../"+path+"/wireguard_command_11", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".11log")
				infile.close()
				with open("../"+path+"/wireguard_command_11", "w") as outfile:
					outfile.write(new_content)
				outfile.close()


			if lines[index].count('_') == 32:
				with open("../"+path+"/wireguard_command_12", "a") as commandfile8:
					commandfile8.write(lines[index])
				commandfile8.close()

				with open("../"+path+"/wireguard_command_12", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".12log")
				infile.close()
				with open("../"+path+"/wireguard_command_12", "w") as outfile:
					outfile.write(new_content)
				outfile.close()


			if lines[index].count('_') == 34:
				with open("../"+path+"/wireguard_command_13", "a") as commandfile8:
					commandfile8.write(lines[index])
				commandfile8.close()

				with open("../"+path+"/wireguard_command_13", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".13log")
				infile.close()
				with open("../"+path+"/wireguard_command_13", "w") as outfile:
					outfile.write(new_content)
				outfile.close()

			if lines[index].count('_') == 36:
				with open("../"+path+"/wireguard_command_14", "a") as commandfile8:
					commandfile8.write(lines[index])
				commandfile8.close()

				with open("../"+path+"/wireguard_command_14", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".14log")
				infile.close()
				with open("../"+path+"/wireguard_command_14", "w") as outfile:
					outfile.write(new_content)
				outfile.close()
	

		commandfile.close()
	



def generate_files_bilateral(filename, path):

	word = "query"


	subkeys = ["kemltki", "kemltkr", "tpki", "tpkr", "kemeki", "ra", "rb", "re", "psk"]

	S1c = list(itertools.combinations(subkeys, 1))
	S2c = list(itertools.combinations(subkeys, 2))
	S3c = list(itertools.combinations(subkeys, 3))
	S4c = list(itertools.combinations(subkeys, 4))
	S5c = list(itertools.combinations(subkeys, 5))
	S6c = list(itertools.combinations(subkeys, 6))
	S7c = list(itertools.combinations(subkeys, 7))
	S8c = list(itertools.combinations(subkeys, 8))
	S9c = list(itertools.combinations(subkeys, 9))
	#S10c = list(itertools.combinations(subkeys, 10))
	#S11c = list(itertools.combinations(subkeys, 11))
	#S12c = list(itertools.combinations(subkeys, 12))
	#S13c = list(itertools.combinations(subkeys, 13))
	#S14c = list(itertools.combinations(subkeys, 14))


	Sc = S1c+S2c+S3c+S4c+S5c+S6c+S7c+S8c+S9c


	#count = -2

	with open(filename, 'r') as f:
		content = f.read()
		words = content.split()
		words = re.findall(r'\b\w+\b', content)
		count = words.count(word)

	    #for line in f:
	        #words = line.split()
	        #for i in words:
	            #if(i==word):
	                #count=count+1
	f.close()
	


	firstquery = -1
	with open(filename, 'r') as f:
	    for i, line in enumerate(f, start=1):
	    	if word in line:
	    		firstquery = firstquery+i
	    		break
	f.close()

	for i in range(0,count):
		with open(filename, 'r') as infile:
			with open("../"+path+"/"+filename[:-3]+"_"+str(i)+".pv", 'w') as outfile:
				lines = infile.readlines()
				for index in range(0, len(lines)):
					if word in lines[firstquery]:
						if(index < firstquery):
							outfile.write(lines[index])
						if(index == firstquery+4*i):
							outfile.write(lines[index])
						if(index == firstquery+4*i+1):
							outfile.write(lines[index])
						if(index == firstquery+4*i+2):
							outfile.write(lines[index])
						if(index == firstquery+4*i+3):
							outfile.write(lines[index])
						if(index>=firstquery+count*4):
							outfile.write(lines[index])
	
	for i in range(1,count):
		with open("../"+path+"/"+filename[:-3]+"_"+str(i)+".pv", 'r') as infile:
			fdata = infile.read()
			key = ""
			for j in range(0, len(Sc[i-1])):
				key = key+"_"+Sc[i-1][j]
			with open("../"+path+"/"+filename[:-3]+key+".pv", 'w') as outfile:
				outfile.write(fdata)
			infile.close()
			os.remove("../"+path+"/"+filename[:-3]+"_"+str(i)+".pv")
			with open("../"+path+"/wireguard_command", "a") as commandfile:
				commandfile.write("proverif"+" "+filename[:-3]+key+".pv"+" > "+filename[:-3]+key+".pv.log"+"\n")
			commandfile.close()

	with open("../"+path+"/wireguard_command", "r") as commandfile:
		lines = commandfile.readlines()
		#print(len(lines))
		for index in range(0, len(lines)):
			if lines[index].count('_') == 8:
				with open("../"+path+"/wireguard_command_1", "a") as commandfile1:
					commandfile1.write(lines[index])
				commandfile1.close()
				with open("../"+path+"/wireguard_command_1", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".1log")
				infile.close()
				with open("../"+path+"/wireguard_command_1_opt", "w") as outfile:
					outfile.write(new_content)
				outfile.close()

			if lines[index].count('_') == 10:
				with open("../"+path+"/wireguard_command_2", "a") as commandfile2:
					commandfile2.write(lines[index])
				commandfile2.close()

				with open("../"+path+"/wireguard_command_2", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".2log")
				infile.close()
				with open("../"+path+"/wireguard_command_2", "w") as outfile:
					outfile.write(new_content)
				outfile.close()

			if lines[index].count('_') == 12:
				with open("../"+path+"/wireguard_command_3", "a") as commandfile3:
					commandfile3.write(lines[index])
				commandfile3.close()

				with open("../"+path+"/wireguard_command_3", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".3log")
				infile.close()
				with open("../"+path+"/wireguard_command_3", "w") as outfile:
					outfile.write(new_content)
				outfile.close()


			if lines[index].count('_') == 14:
				with open("../"+path+"/wireguard_command_4", "a") as commandfile4:
					commandfile4.write(lines[index])
				commandfile4.close()

				with open("../"+path+"/wireguard_command_4", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".4log")
				infile.close()
				with open("../"+path+"/wireguard_command_4", "w") as outfile:
					outfile.write(new_content)
				outfile.close()


			if lines[index].count('_') == 16:
				with open("../"+path+"/wireguard_command_5", "a") as commandfile5:
					commandfile5.write(lines[index])
				commandfile5.close()


				with open("../"+path+"/wireguard_command_5", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".5log")
				infile.close()
				with open("../"+path+"/wireguard_command_5", "w") as outfile:
					outfile.write(new_content)
				outfile.close()


			if lines[index].count('_') == 18:
				with open("../"+path+"/wireguard_command_6", "a") as commandfile6:
					commandfile6.write(lines[index])
				commandfile6.close()

				with open("../"+path+"/wireguard_command_6", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".6log")
				infile.close()
				with open("../"+path+"/wireguard_command_6", "w") as outfile:
					outfile.write(new_content)
				outfile.close()


			if lines[index].count('_') == 20:
				with open("../"+path+"/wireguard_command_7", "a") as commandfile7:
					commandfile7.write(lines[index])
				commandfile7.close()

				with open("../"+path+"/wireguard_command_7", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".7log")
				infile.close()
				with open("../"+path+"/wireguard_command_7", "w") as outfile:
					outfile.write(new_content)
				outfile.close()



			if lines[index].count('_') == 22:
				with open("../"+path+"/wireguard_command_8", "a") as commandfile8:
					commandfile8.write(lines[index])
				commandfile8.close()

				with open("../"+path+"/wireguard_command_8", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".8log")
				infile.close()
				with open("../"+path+"/wireguard_command_8", "w") as outfile:
					outfile.write(new_content)
				outfile.close()


			if lines[index].count('_') == 24:
				with open("../"+path+"/wireguard_command_9", "a") as commandfile8:
					commandfile8.write(lines[index])
				commandfile8.close()

				with open("../"+path+"/wireguard_command_9", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".9log")
				infile.close()
				with open("../"+path+"/wireguard_command_9", "w") as outfile:
					outfile.write(new_content)
				outfile.close()


			if lines[index].count('_') == 26:
				with open("../"+path+"/wireguard_command_10", "a") as commandfile8:
					commandfile8.write(lines[index])
				commandfile8.close()

				with open("../"+path+"/wireguard_command_10", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".10log")
				infile.close()
				with open("../"+path+"/wireguard_command_10", "w") as outfile:
					outfile.write(new_content)
				outfile.close()


			if lines[index].count('_') == 28:
				with open("../"+path+"/wireguard_command_11", "a") as commandfile8:
					commandfile8.write(lines[index])
				commandfile8.close()

				with open("../"+path+"/wireguard_command_11", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".11log")
				infile.close()
				with open("../"+path+"/wireguard_command_11", "w") as outfile:
					outfile.write(new_content)
				outfile.close()


			if lines[index].count('_') == 30:
				with open("../"+path+"/wireguard_command_12", "a") as commandfile8:
					commandfile8.write(lines[index])
				commandfile8.close()

				with open("../"+path+"/wireguard_command_12", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".12log")
				infile.close()
				with open("../"+path+"/wireguard_command_12", "w") as outfile:
					outfile.write(new_content)
				outfile.close()


			if lines[index].count('_') == 32:
				with open("../"+path+"/wireguard_command_13", "a") as commandfile8:
					commandfile8.write(lines[index])
				commandfile8.close()

				with open("../"+path+"/wireguard_command_13", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".13log")
				infile.close()
				with open("../"+path+"/wireguard_command_13", "w") as outfile:
					outfile.write(new_content)
				outfile.close()

			if lines[index].count('_') == 34:
				with open("../"+path+"/wireguard_command_14", "a") as commandfile8:
					commandfile8.write(lines[index])
				commandfile8.close()

				with open("../"+path+"/wireguard_command_14", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".14log")
				infile.close()
				with open("../"+path+"/wireguard_command_14", "w") as outfile:
					outfile.write(new_content)
				outfile.close()
	

		commandfile.close()
	




def generate_files_agreement(filename, path):

	word = "query"


	subkeys = ["kemltki", "kemltkr", "tpki", "tpkr", "kemeki", "ra", "rb", "re", "psk"]

	S1c = list(itertools.combinations(subkeys, 1))
	S2c = list(itertools.combinations(subkeys, 2))
	S3c = list(itertools.combinations(subkeys, 3))
	S4c = list(itertools.combinations(subkeys, 4))
	S5c = list(itertools.combinations(subkeys, 5))
	S6c = list(itertools.combinations(subkeys, 6))
	S7c = list(itertools.combinations(subkeys, 7))
	S8c = list(itertools.combinations(subkeys, 8))
	S9c = list(itertools.combinations(subkeys, 9))
	#S10c = list(itertools.combinations(subkeys, 10))
	#S11c = list(itertools.combinations(subkeys, 11))
	#S12c = list(itertools.combinations(subkeys, 12))
	#S13c = list(itertools.combinations(subkeys, 13))
	#S14c = list(itertools.combinations(subkeys, 14))


	Sc = S1c+S2c+S3c+S4c+S5c+S6c+S7c+S8c+S9c


	#count = -2

	with open(filename, 'r') as f:
		content = f.read()
		words = content.split()
		words = re.findall(r'\b\w+\b', content)
		count = words.count(word)

	    #for line in f:
	        #words = line.split()
	        #for i in words:
	            #if(i==word):
	                #count=count+1
	f.close()
	


	firstquery = -1
	with open(filename, 'r') as f:
	    for i, line in enumerate(f, start=1):
	    	if word in line:
	    		firstquery = firstquery+i
	    		break
	f.close()

	for i in range(0,count):
		with open(filename, 'r') as infile:
			with open("../"+path+"/"+filename[:-3]+"_"+str(i)+".pv", 'w') as outfile:
				lines = infile.readlines()
				for index in range(0, len(lines)):
					if word in lines[firstquery]:
						if(index < firstquery):
							outfile.write(lines[index])
						if(index == firstquery+4*i):
							outfile.write(lines[index])
						if(index == firstquery+4*i+1):
							outfile.write(lines[index])
						if(index == firstquery+4*i+2):
							outfile.write(lines[index])
						if(index == firstquery+4*i+3):
							outfile.write(lines[index])
						if(index>=firstquery+count*4):
							outfile.write(lines[index])
	for i in range(1,count):
		with open("../"+path+"/"+filename[:-3]+"_"+str(i)+".pv", 'r') as infile:
			fdata = infile.read()
			key = ""
			for j in range(0, len(Sc[i-1])):
				key = key+"_"+Sc[i-1][j]
			with open("../"+path+"/"+filename[:-3]+key+".pv", 'w') as outfile:
				outfile.write(fdata)
			infile.close()
			os.remove("../"+path+"/"+filename[:-3]+"_"+str(i)+".pv")
			with open("../"+path+"/wireguard_command", "a") as commandfile:
				commandfile.write("proverif"+" "+filename[:-3]+key+".pv"+" > "+filename[:-3]+key+".pv.log"+"\n")
			commandfile.close()

	with open("../"+path+"/wireguard_command", "r") as commandfile:
		lines = commandfile.readlines()
		#print(len(lines))
		for index in range(0, len(lines)):
			if lines[index].count('_') == 10:
				with open("../"+path+"/wireguard_command_1", "a") as commandfile1:
					commandfile1.write(lines[index])
				commandfile1.close()
				with open("../"+path+"/wireguard_command_1", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".1log")
				infile.close()
				with open("../"+path+"/wireguard_command_1_opt", "w") as outfile:
					outfile.write(new_content)
				outfile.close()

			if lines[index].count('_') == 12:
				with open("../"+path+"/wireguard_command_2", "a") as commandfile2:
					commandfile2.write(lines[index])
				commandfile2.close()

				with open("../"+path+"/wireguard_command_2", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".2log")
				infile.close()
				with open("../"+path+"/wireguard_command_2", "w") as outfile:
					outfile.write(new_content)
				outfile.close()

			if lines[index].count('_') == 14:
				with open("../"+path+"/wireguard_command_3", "a") as commandfile3:
					commandfile3.write(lines[index])
				commandfile3.close()

				with open("../"+path+"/wireguard_command_3", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".3log")
				infile.close()
				with open("../"+path+"/wireguard_command_3", "w") as outfile:
					outfile.write(new_content)
				outfile.close()


			if lines[index].count('_') == 16:
				with open("../"+path+"/wireguard_command_4", "a") as commandfile4:
					commandfile4.write(lines[index])
				commandfile4.close()

				with open("../"+path+"/wireguard_command_4", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".4log")
				infile.close()
				with open("../"+path+"/wireguard_command_4", "w") as outfile:
					outfile.write(new_content)
				outfile.close()


			if lines[index].count('_') == 18:
				with open("../"+path+"/wireguard_command_5", "a") as commandfile5:
					commandfile5.write(lines[index])
				commandfile5.close()


				with open("../"+path+"/wireguard_command_5", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".5log")
				infile.close()
				with open("../"+path+"/wireguard_command_5", "w") as outfile:
					outfile.write(new_content)
				outfile.close()


			if lines[index].count('_') == 20:
				with open("../"+path+"/wireguard_command_6", "a") as commandfile6:
					commandfile6.write(lines[index])
				commandfile6.close()

				with open("../"+path+"/wireguard_command_6", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".6log")
				infile.close()
				with open("../"+path+"/wireguard_command_6", "w") as outfile:
					outfile.write(new_content)
				outfile.close()


			if lines[index].count('_') == 22:
				with open("../"+path+"/wireguard_command_7", "a") as commandfile7:
					commandfile7.write(lines[index])
				commandfile7.close()

				with open("../"+path+"/wireguard_command_7", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".7log")
				infile.close()
				with open("../"+path+"/wireguard_command_7", "w") as outfile:
					outfile.write(new_content)
				outfile.close()



			if lines[index].count('_') == 24:
				with open("../"+path+"/wireguard_command_8", "a") as commandfile8:
					commandfile8.write(lines[index])
				commandfile8.close()

				with open("../"+path+"/wireguard_command_8", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".8log")
				infile.close()
				with open("../"+path+"/wireguard_command_8", "w") as outfile:
					outfile.write(new_content)
				outfile.close()


			if lines[index].count('_') == 26:
				with open("../"+path+"/wireguard_command_9", "a") as commandfile8:
					commandfile8.write(lines[index])
				commandfile8.close()

				with open("../"+path+"/wireguard_command_9", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".9log")
				infile.close()
				with open("../"+path+"/wireguard_command_9", "w") as outfile:
					outfile.write(new_content)
				outfile.close()


			if lines[index].count('_') == 28:
				with open("../"+path+"/wireguard_command_10", "a") as commandfile8:
					commandfile8.write(lines[index])
				commandfile8.close()

				with open("../"+path+"/wireguard_command_10", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".10log")
				infile.close()
				with open("../"+path+"/wireguard_command_10", "w") as outfile:
					outfile.write(new_content)
				outfile.close()


			if lines[index].count('_') == 30:
				with open("../"+path+"/wireguard_command_11", "a") as commandfile8:
					commandfile8.write(lines[index])
				commandfile8.close()

				with open("../"+path+"/wireguard_command_11", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".11log")
				infile.close()
				with open("../"+path+"/wireguard_command_11", "w") as outfile:
					outfile.write(new_content)
				outfile.close()


			if lines[index].count('_') == 32:
				with open("../"+path+"/wireguard_command_12", "a") as commandfile8:
					commandfile8.write(lines[index])
				commandfile8.close()

				with open("../"+path+"/wireguard_command_12", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".12log")
				infile.close()
				with open("../"+path+"/wireguard_command_12", "w") as outfile:
					outfile.write(new_content)
				outfile.close()


			if lines[index].count('_') == 34:
				with open("../"+path+"/wireguard_command_13", "a") as commandfile8:
					commandfile8.write(lines[index])
				commandfile8.close()

				with open("../"+path+"/wireguard_command_13", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".13log")
				infile.close()
				with open("../"+path+"/wireguard_command_13", "w") as outfile:
					outfile.write(new_content)
				outfile.close()

			if lines[index].count('_') == 36:
				with open("../"+path+"/wireguard_command_14", "a") as commandfile8:
					commandfile8.write(lines[index])
				commandfile8.close()

				with open("../"+path+"/wireguard_command_14", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".14log")
				infile.close()
				with open("../"+path+"/wireguard_command_14", "w") as outfile:
					outfile.write(new_content)
				outfile.close()


		commandfile.close()

	
def generate_files_secrecy(filename, path):
	word = "query"
	word = "query"


	subkeys = ["kemltki", "kemltkr", "tpki", "tpkr", "kemeki", "ra", "rb", "re", "psk"]

	S1c = list(itertools.combinations(subkeys, 1))
	S2c = list(itertools.combinations(subkeys, 2))
	S3c = list(itertools.combinations(subkeys, 3))
	S4c = list(itertools.combinations(subkeys, 4))
	S5c = list(itertools.combinations(subkeys, 5))
	S6c = list(itertools.combinations(subkeys, 6))
	S7c = list(itertools.combinations(subkeys, 7))
	S8c = list(itertools.combinations(subkeys, 8))
	S9c = list(itertools.combinations(subkeys, 9))
	#S10c = list(itertools.combinations(subkeys, 10))
	#S11c = list(itertools.combinations(subkeys, 11))
	#S12c = list(itertools.combinations(subkeys, 12))
	#S13c = list(itertools.combinations(subkeys, 13))
	#S14c = list(itertools.combinations(subkeys, 14))


	Sc = S1c+S2c+S3c+S4c+S5c+S6c+S7c+S8c+S9c

	with open(filename, 'r') as f:
		content = f.read()
		words = content.split()
		words = re.findall(r'\b\w+\b', content)
		count = words.count(word)

	    #for line in f:
	        #words = line.split()
	        #for i in words:
	            #if(i==word):
	                #count=count+1
	f.close()

	firstquery = -1
	with open(filename, 'r') as f:
	    for i, line in enumerate(f, start=1):
	    	if word in line:
	    		firstquery = firstquery+i
	    		break
	f.close()

	for i in range(0,count):
		with open(filename, 'r') as infile:
			with open("../"+path+"/"+filename[:-3]+"_"+str(i)+".pv", 'w') as outfile:
				lines = infile.readlines()
				for index in range(0, len(lines)):
					if word in lines[firstquery]:
						if(i==0):
							if(index < firstquery):
								outfile.write(lines[index])
							if(index == firstquery+4*i):
								outfile.write(lines[index])
							if(index == firstquery+4*i+1):
								outfile.write(lines[index])
							if(index == firstquery+4*i+2):
								outfile.write(lines[index])
							#if(index == firstquery+1+4*i+3):
								#outfile.write(lines[index])
							if(index>=firstquery+count*4):
								outfile.write(lines[index])
						else:
							if(index < firstquery):
								outfile.write(lines[index])
							if(index == firstquery+4*i-1):
								outfile.write(lines[index])
							if(index == firstquery+4*i):
								outfile.write(lines[index])
							if(index == firstquery+4*i+1):
								outfile.write(lines[index])
							if(index == firstquery+4*i+2):
								outfile.write(lines[index])
							#if(index == firstquery+1+4*i+3):
								#outfile.write(lines[index])							
							if(index>=firstquery+count*4):
								outfile.write(lines[index])
					if word in lines[firstquery+1]:
						if(i==0):
							if(index < firstquery+1):
								outfile.write(lines[index])
							if(index == firstquery+1+4*i):
								outfile.write(lines[index])
							if(index == firstquery+1+4*i+1):
								outfile.write(lines[index])
							if(index == firstquery+1+4*i+2):
								outfile.write(lines[index])
							#if(index == index+1+4*i+3):
								#outfile.write(lines[index])
							if(index>=firstquery+1+count*4):
								outfile.write(lines[index])
						else:
							if(index < firstquery+1):
								outfile.write(lines[index])
							if(index == firstquery+1+4*i-1):
								outfile.write(lines[index])
							if(index == firstquery+1+4*i):
								outfile.write(lines[index])
							if(index == firstquery+1+4*i+1):
								outfile.write(lines[index])
							if(index == firstquery+1+4*i+2):
								outfile.write(lines[index])
							#if(index == index+1+4*i+3):
								#outfile.write(lines[index])							
							if(index>=firstquery+1+count*4):
								outfile.write(lines[index])
					if word in lines[firstquery+2]:
						if(i==0):
							if(index < firstquery+2):
								outfile.write(lines[index])
							if(index == firstquery+2+4*i):
								outfile.write(lines[index])
							if(index == firstquery+2+4*i+1):
								outfile.write(lines[index])
							if(index == firstquery+2+4*i+2):
								outfile.write(lines[index])
							#if(index == firstquery+1+4*i+3):
								#outfile.write(lines[index])
							if(index>=firstquery+2+count*4):
								outfile.write(lines[index])
						else:
							if(index < firstquery+2):
								outfile.write(lines[index])
							if(index == firstquery+2+4*i-1):
								outfile.write(lines[index])
							if(index == firstquery+2+4*i):
								outfile.write(lines[index])
							if(index == firstquery+2+4*i+1):
								outfile.write(lines[index])
							if(index == firstquery+2+4*i+2):
								outfile.write(lines[index])
							#if(index == firstquery+1+4*i+3):
								#outfile.write(lines[index])							
							if(index>=firstquery+2+count*4):
								outfile.write(lines[index])
		infile.close()
		
	for i in range(1,count):
		with open("../"+path+"/"+filename[:-3]+"_"+str(i)+".pv", 'r') as infile:
			fdata = infile.read()
			key = ""
			for j in range(0, len(Sc[i-1])):
				key = key+"_"+Sc[i-1][j]
			with open("../"+path+"/"+filename[:-3]+key+".pv", 'w') as outfile:
				outfile.write(fdata)
			infile.close()
			os.remove("../"+path+"/"+filename[:-3]+"_"+str(i)+".pv")
			with open("../"+path+"/wireguard_command", "a") as commandfile:
				commandfile.write("proverif"+" "+filename[:-3]+key+".pv"+" > "+filename[:-3]+key+".pv.log"+"\n")
	commandfile.close()

	with open("../"+path+"/wireguard_command", "r") as commandfile:
		lines = commandfile.readlines()
		for index in range(0, len(lines)):
			if lines[index].count('_') == 10:
				with open("../"+path+"/wireguard_command_1", "a") as commandfile1:
					commandfile1.write(lines[index])
				commandfile1.close()
				with open("../"+path+"/wireguard_command_1", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".1log")
				infile.close()
				with open("../"+path+"/wireguard_command_1_opt", "w") as outfile:
					outfile.write(new_content)
				outfile.close()

			if lines[index].count('_') == 12:
				with open("../"+path+"/wireguard_command_2", "a") as commandfile2:
					commandfile2.write(lines[index])
				commandfile2.close()

				with open("../"+path+"/wireguard_command_2", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".2log")
				infile.close()
				with open("../"+path+"/wireguard_command_2", "w") as outfile:
					outfile.write(new_content)
				outfile.close()

			if lines[index].count('_') == 14:
				with open("../"+path+"/wireguard_command_3", "a") as commandfile3:
					commandfile3.write(lines[index])
				commandfile3.close()

				with open("../"+path+"/wireguard_command_3", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".3log")
				infile.close()
				with open("../"+path+"/wireguard_command_3", "w") as outfile:
					outfile.write(new_content)
				outfile.close()


			if lines[index].count('_') == 16:
				with open("../"+path+"/wireguard_command_4", "a") as commandfile4:
					commandfile4.write(lines[index])
				commandfile4.close()

				with open("../"+path+"/wireguard_command_4", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".4log")
				infile.close()
				with open("../"+path+"/wireguard_command_4", "w") as outfile:
					outfile.write(new_content)
				outfile.close()


			if lines[index].count('_') == 18:
				with open("../"+path+"/wireguard_command_5", "a") as commandfile5:
					commandfile5.write(lines[index])
				commandfile5.close()


				with open("../"+path+"/wireguard_command_5", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".5log")
				infile.close()
				with open("../"+path+"/wireguard_command_5", "w") as outfile:
					outfile.write(new_content)
				outfile.close()


			if lines[index].count('_') == 20:
				with open("../"+path+"/wireguard_command_6", "a") as commandfile6:
					commandfile6.write(lines[index])
				commandfile6.close()

				with open("../"+path+"/wireguard_command_6", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".6log")
				infile.close()
				with open("../"+path+"/wireguard_command_6", "w") as outfile:
					outfile.write(new_content)
				outfile.close()


			if lines[index].count('_') == 22:
				with open("../"+path+"/wireguard_command_7", "a") as commandfile7:
					commandfile7.write(lines[index])
				commandfile7.close()

				with open("../"+path+"/wireguard_command_7", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".7log")
				infile.close()
				with open("../"+path+"/wireguard_command_7", "w") as outfile:
					outfile.write(new_content)
				outfile.close()



			if lines[index].count('_') == 24:
				with open("../"+path+"/wireguard_command_8", "a") as commandfile8:
					commandfile8.write(lines[index])
				commandfile8.close()

				with open("../"+path+"/wireguard_command_8", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".8log")
				infile.close()
				with open("../"+path+"/wireguard_command_8", "w") as outfile:
					outfile.write(new_content)
				outfile.close()


			if lines[index].count('_') == 26:
				with open("../"+path+"/wireguard_command_9", "a") as commandfile8:
					commandfile8.write(lines[index])
				commandfile8.close()

				with open("../"+path+"/wireguard_command_9", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".9log")
				infile.close()
				with open("../"+path+"/wireguard_command_9", "w") as outfile:
					outfile.write(new_content)
				outfile.close()


			if lines[index].count('_') == 28:
				with open("../"+path+"/wireguard_command_10", "a") as commandfile8:
					commandfile8.write(lines[index])
				commandfile8.close()

				with open("../"+path+"/wireguard_command_10", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".10log")
				infile.close()
				with open("../"+path+"/wireguard_command_10", "w") as outfile:
					outfile.write(new_content)
				outfile.close()


			if lines[index].count('_') == 30:
				with open("../"+path+"/wireguard_command_11", "a") as commandfile8:
					commandfile8.write(lines[index])
				commandfile8.close()

				with open("../"+path+"/wireguard_command_11", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".11log")
				infile.close()
				with open("../"+path+"/wireguard_command_11", "w") as outfile:
					outfile.write(new_content)
				outfile.close()


			if lines[index].count('_') == 32:
				with open("../"+path+"/wireguard_command_12", "a") as commandfile8:
					commandfile8.write(lines[index])
				commandfile8.close()

				with open("../"+path+"/wireguard_command_12", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".12log")
				infile.close()
				with open("../"+path+"/wireguard_command_12", "w") as outfile:
					outfile.write(new_content)
				outfile.close()


			if lines[index].count('_') == 34:
				with open("../"+path+"/wireguard_command_13", "a") as commandfile8:
					commandfile8.write(lines[index])
				commandfile8.close()

				with open("../"+path+"/wireguard_command_13", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".13log")
				infile.close()
				with open("../"+path+"/wireguard_command_13", "w") as outfile:
					outfile.write(new_content)
				outfile.close()

			if lines[index].count('_') == 36:
				with open("../"+path+"/wireguard_command_14", "a") as commandfile8:
					commandfile8.write(lines[index])
				commandfile8.close()

				with open("../"+path+"/wireguard_command_14", "r") as infile:
					content = infile.read()
				new_content = content.replace(".log", ".14log")
				infile.close()
				with open("../"+path+"/wireguard_command_14", "w") as outfile:
					outfile.write(new_content)
				outfile.close()


		commandfile.close()


def tamarin_proverif_unilateral_initiator(value):

	command = TAMARIN+" --derivcheck-timeout=0 -D"+value+" wireguard_unilateral_initiator_macro.spthy +RTS -N1 -RTS -m=proverif > wireguard_unilateral_initiator_"+value+".p"
	process = Popen(command, stdout=PIPE, stderr=None, shell=True)
	output = process.communicate()[0]

	update_files_without_precise('wireguard_unilateral_initiator_'+value+'.p', 'wireguard_unilateral_initiator_'+value+'.pv')

	os.remove('wireguard_unilateral_initiator_'+value+'.p')
	
	generate_files_unilateral('wireguard_unilateral_initiator_'+value+'.pv', 'unilateral_initiator')


def tamarin_proverif_unilateral_responder(value):

	command = TAMARIN+" --derivcheck-timeout=0 -D"+value+" wireguard_unilateral_responder_macro.spthy +RTS -N1 -RTS -m=proverif > wireguard_unilateral_responder_"+value+".p"
	process = Popen(command, stdout=PIPE, stderr=None, shell=True)
	output = process.communicate()[0]

	update_files_without_precise('wireguard_unilateral_responder_'+value+'.p', 'wireguard_unilateral_responder_'+value+'.pv')

	os.remove('wireguard_unilateral_responder_'+value+'.p')
	
	generate_files_unilateral('wireguard_unilateral_responder_'+value+'.pv', 'unilateral_responder')


def tamarin_proverif_bilateral(value):

	command = TAMARIN+" --derivcheck-timeout=0 -D"+value+" wireguard_bilateral_macro.spthy +RTS -N1 -RTS -m=proverif > wireguard_bilateral_"+value+".p"
	process = Popen(command, stdout=PIPE, stderr=None, shell=True)
	output = process.communicate()[0]

	update_files_without_precise('wireguard_bilateral_'+value+'.p', 'wireguard_bilateral_'+value+'.pv')

	os.remove('wireguard_bilateral_'+value+'.p')
	
	generate_files_bilateral('wireguard_bilateral_'+value+'.pv', 'bilateral')



def tamarin_proverif_agreement_inithello(value):

	command = TAMARIN+" --derivcheck-timeout=0 -D"+value+" wireguard_agreement_macro.spthy +RTS -N1 -RTS -m=proverif > wireguard_agreement_inithello_"+value+".p"
	process = Popen(command, stdout=PIPE, stderr=None, shell=True)
	output = process.communicate()[0]

	update_files_without_precise('wireguard_agreement_inithello_'+value+'.p', 'wireguard_agreement_inithello_'+value+'.pv')

	os.remove('wireguard_agreement_inithello_'+value+'.p')
	
	generate_files_agreement('wireguard_agreement_inithello_'+value+'.pv', 'agreement_inithello')


def tamarin_proverif_agreement_rechello(value):

	command = TAMARIN+" --derivcheck-timeout=0 -D"+value+" wireguard_agreement_macro.spthy +RTS -N1 -RTS -m=proverif > wireguard_agreement_rechello_"+value+".p"
	process = Popen(command, stdout=PIPE, stderr=None, shell=True)
	output = process.communicate()[0]

	update_files_without_precise('wireguard_agreement_rechello_'+value+'.p', 'wireguard_agreement_rechello_'+value+'.pv')

	os.remove('wireguard_agreement_rechello_'+value+'.p')
	
	generate_files_agreement('wireguard_agreement_rechello_'+value+'.pv', 'agreement_rechello')


def tamarin_proverif_agreement_confirm(value):
	
	command = TAMARIN+" --derivcheck-timeout=0 -D"+value+" wireguard_agreement_macro.spthy +RTS -N1 -RTS -m=proverif > wireguard_agreement_confirm_"+value+".p"
	process = Popen(command, stdout=PIPE, stderr=None, shell=True)
	output = process.communicate()[0]

	update_files_without_precise('wireguard_agreement_confirm_'+value+'.p', 'wireguard_agreement_confirm_'+value+'.pv')

	#os.remove('wireguard_agreement_confirm_'+value+'.p')

	generate_files_agreement('wireguard_agreement_confirm_'+value+'.pv', 'agreement_confirm')


def tamarin_proverif_agreement_transport_itor(value):
	
	command = TAMARIN+" --derivcheck-timeout=0 -D"+value+" wireguard_agreement_macro.spthy +RTS -N1 -RTS -m=proverif > wireguard_agreement_transport_itor_"+value+".p"
	process = Popen(command, stdout=PIPE, stderr=None, shell=True)
	output = process.communicate()[0]

	update_files('wireguard_agreement_transport_itor_'+value+'.p', 'wireguard_agreement_transport_itor_'+value+'.pv')

	os.remove('wireguard_agreement_transport_itor_'+value+'.p')
	
	generate_files_agrrement('wireguard_agreement_transport_itor_'+value+'.pv', 'agreement_transport_itor')


def tamarin_proverif_agreement_transport_rtoi(value):
	
	command = TAMARIN+" --derivcheck-timeout=0 -D"+value+" wireguard_agreement_macro.spthy +RTS -N1 -RTS -m=proverif > wireguard_agreement_transport_rtoi_"+value+".p"
	process = Popen(command, stdout=PIPE, stderr=None, shell=True)
	output = process.communicate()[0]

	update_files('wireguard_agreement_transport_rtoi_'+value+'.p', 'wireguard_agreement_transport_rtoi_'+value+'.pv')

	os.remove('wireguard_agreement_transport_rtoi_'+value+'.p')
	
	generate_files_agrrement('wireguard_agreement_transport_rtoi_'+value+'.pv', 'agreement_transport_rtoi')


def tamarin_proverif_secrecy_isk6(value):
	
	command = TAMARIN+" --derivcheck-timeout=0 -D"+value+" wireguard_secrecy_macro.spthy +RTS -N1 -RTS -m=proverif > wireguard_secrecy_isk6_"+value+".p"
	process = Popen(command, stdout=PIPE, stderr=None, shell=True)
	output = process.communicate()[0]

	update_files('wireguard_secrecy_isk6_'+value+'.p', 'wireguard_secrecy_isk6_'+value+'.pv')

	os.remove('wireguard_secrecy_isk6_'+value+'.p')
	
	generate_files_secrecy('wireguard_secrecy_isk6_'+value+'.pv', 'secrecy_isk6')


def tamarin_proverif_secrecy_isk7(value):
	
	command = TAMARIN+" --derivcheck-timeout=0 -D"+value+" wireguard_secrecy_macro.spthy +RTS -N1 -RTS -m=proverif > wireguard_secrecy_isk7_"+value+".p"
	process = Popen(command, stdout=PIPE, stderr=None, shell=True)
	output = process.communicate()[0]

	update_files_without_precise('wireguard_secrecy_isk7_'+value+'.p', 'wireguard_secrecy_isk7_'+value+'.pv')

	os.remove('wireguard_secrecy_isk7_'+value+'.p')
	
	generate_files_secrecy('wireguard_secrecy_isk7_'+value+'.pv', 'secrecy_isk7')


def tamarin_proverif_secrecy_mut7(value):
	
	command = TAMARIN+" --derivcheck-timeout=0 -D"+value+" wireguard_secrecy_macro.spthy +RTS -N1 -RTS -m=proverif > wireguard_secrecy_mut7_"+value+".p"
	process = Popen(command, stdout=PIPE, stderr=None, shell=True)
	output = process.communicate()[0]

	update_files_without_precise('wireguard_secrecy_mut7_'+value+'.p', 'wireguard_secrecy_mut7_'+value+'.pv')

	os.remove('wireguard_secrecy_mut7_'+value+'.p')
	
	generate_files_secrecy('wireguard_secrecy_mut7_'+value+'.pv', 'secrecy_mut7')


def tamarin_proverif_secrecy_isk7pfs(value):
	
	command = TAMARIN+" -D"+value+" wireguard_secrecy_macro.spthy +RTS -N1 -RTS -m=proverif > wireguard_secrecy_isk7pfs_"+value+".p"
	process = Popen(command, stdout=DEVNULL, stderr=DEVNULL, shell=True)
	output = process.communicate()[0]

	update_files_pfs('wireguard_secrecy_isk7pfs_'+value+'.p', 'wireguard_secrecy_isk7pfs_'+value+'.pv')

	os.remove('wireguard_secrecy_isk7pfs_'+value+'.p')
	
	generate_files_secrecy('wireguard_secrecy_isk7pfs_'+value+'.pv', 'secrecy_isk7pfs')


def tamarin_proverif_secrecy_rsk6(value):
	
	command = TAMARIN+" --derivcheck-timeout=0 -D"+value+" wireguard_secrecy_macro.spthy +RTS -N1 -RTS -m=proverif > wireguard_secrecy_rsk6_"+value+".p"
	process = Popen(command, stdout=PIPE, stderr=None, shell=True)
	output = process.communicate()[0]

	update_files('wireguard_secrecy_rsk6_'+value+'.p', 'wireguard_secrecy_rsk6_'+value+'.pv')

	os.remove('wireguard_secrecy_rsk6_'+value+'.p')
	
	generate_files_secrecy('wireguard_secrecy_rsk6_'+value+'.pv', 'secrecy_rsk6')


def tamarin_proverif_secrecy_rsk7(value):
	
	command = TAMARIN+" --derivcheck-timeout=0 -D"+value+" wireguard_secrecy_macro.spthy +RTS -N1 -RTS -m=proverif > wireguard_secrecy_rsk7_"+value+".p"
	process = Popen(command, stdout=PIPE, stderr=None, shell=True)
	output = process.communicate()[0]

	update_files_without_precise('wireguard_secrecy_rsk7_'+value+'.p', 'wireguard_secrecy_rsk7_'+value+'.pv')

	os.remove('wireguard_secrecy_rsk7_'+value+'.p')
	
	generate_files_secrecy('wireguard_secrecy_rsk7_'+value+'.pv', 'secrecy_rsk7')


def tamarin_proverif_secrecy_rsk7pfs(value):
	
	command = TAMARIN+" -D"+value+" wireguard_secrecy_macro.spthy +RTS -N1 -RTS -m=proverif > wireguard_secrecy_rsk7pfs_"+value+".p"
	process = Popen(command, stdout=DEVNULL, stderr=DEVNULL, shell=True)
	output = process.communicate()[0]

	update_files_pfs('wireguard_secrecy_rsk7pfs_'+value+'.p', 'wireguard_secrecy_rsk7pfs_'+value+'.pv')

	os.remove('wireguard_secrecy_rsk7pfs_'+value+'.p')
	
	generate_files_secrecy('wireguard_secrecy_rsk7pfs_'+value+'.pv', 'secrecy_rsk7pfs')


def tamarin_proverif_secrecy_mut7pfs(value):
	
	command = TAMARIN+" -D"+value+" wireguard_secrecy_macro.spthy +RTS -N1 -RTS -m=proverif > wireguard_secrecy_mut7pfs_"+value+".p"
	process = Popen(command, stdout=DEVNULL, stderr=DEVNULL, shell=True)
	output = process.communicate()[0]

	update_files_pfs('wireguard_secrecy_mut7pfs_'+value+'.p', 'wireguard_secrecy_mut7pfs_'+value+'.pv')

	os.remove('wireguard_secrecy_mut7pfs_'+value+'.p')
	
	generate_files_secrecy('wireguard_secrecy_mut7pfs_'+value+'.pv', 'secrecy_mut7pfs')



def tamarin_proverif_secrecy_isk_itor(value):
	
	command = TAMARIN+" --derivcheck-timeout=0 -D"+value+" wireguard_secrecy_macro.spthy +RTS -N1 -RTS -m=proverif > wireguard_secrecy_isk_itor_"+value+".p"
	process = Popen(command, stdout=PIPE, stderr=None, shell=True)
	output = process.communicate()[0]

	update_files('wireguard_secrecy_isk_itor_'+value+'.p', 'wireguard_secrecy_isk_itor_'+value+'.pv')

	os.remove('wireguard_secrecy_isk_itor_'+value+'.p')
	
	generate_files_secrecy('wireguard_secrecy_isk_itor_'+value+'.pv', 'secrecy_isk_itor')


def tamarin_proverif_secrecy_isk_itor_pfs(value):
	
	command = TAMARIN+" --derivcheck-timeout=0 -D"+value+" wireguard_secrecy_macro.spthy +RTS -N1 -RTS -m=proverif > wireguard_secrecy_isk_itor_pfs_"+value+".p"
	process = Popen(command, stdout=PIPE, stderr=None, shell=True)
	output = process.communicate()[0]

	update_files_pfs('wireguard_secrecy_isk_itor_pfs_'+value+'.p', 'wireguard_secrecy_isk_itor_pfs_'+value+'.pv')

	os.remove('wireguard_secrecy_isk_itor_pfs_'+value+'.p')
	
	generate_files_secrecy('wireguard_secrecy_isk_itor_pfs_'+value+'.pv', 'secrecy_isk_itor_pfs')


def tamarin_proverif_secrecy_isk_rtoi(value):
	
	command = TAMARIN+" --derivcheck-timeout=0 -D"+value+" wireguard_secrecy_macro.spthy +RTS -N1 -RTS -m=proverif > wireguard_secrecy_isk_rtoi_"+value+".p"
	process = Popen(command, stdout=PIPE, stderr=None, shell=True)
	output = process.communicate()[0]

	update_files('wireguard_secrecy_isk_rtoi_'+value+'.p', 'wireguard_secrecy_isk_rtoi_'+value+'.pv')

	os.remove('wireguard_secrecy_isk_rtoi_'+value+'.p')
	
	generate_files_secrecy('wireguard_secrecy_isk_rtoi_'+value+'.pv', 'secrecy_isk_rtoi')

def tamarin_proverif_secrecy_isk_rtoi_pfs(value):
	
	command = TAMARIN+" --derivcheck-timeout=0 -D"+value+" wireguard_secrecy_macro.spthy +RTS -N1 -RTS -m=proverif > wireguard_secrecy_isk_rtoi_pfs_"+value+".p"
	process = Popen(command, stdout=PIPE, stderr=None, shell=True)
	output = process.communicate()[0]

	update_files_pfs('wireguard_secrecy_isk_rtoi_pfs_'+value+'.p', 'wireguard_secrecy_isk_rtoi_pfs_'+value+'.pv')

	os.remove('wireguard_secrecy_isk_rtoi_pfs_'+value+'.p')
	
	generate_files_secrecy('wireguard_secrecy_isk_rtoi_pfs_'+value+'.pv', 'secrecy_isk_rtoi_pfs')



def tamarin_proverif_secrecy_rsk_itor(value):
	
	command = TAMARIN+" --derivcheck-timeout=0 -D"+value+" wireguard_secrecy_macro.spthy +RTS -N1 -RTS -m=proverif > wireguard_secrecy_rsk_itor_"+value+".p"
	process = Popen(command, stdout=PIPE, stderr=None, shell=True)
	output = process.communicate()[0]

	update_files('wireguard_secrecy_rsk_itor_'+value+'.p', 'wireguard_secrecy_rsk_itor_'+value+'.pv')

	os.remove('wireguard_secrecy_rsk_itor_'+value+'.p')
	
	generate_files_secrecy('wireguard_secrecy_rsk_itor_'+value+'.pv', 'secrecy_rsk_itor')


def tamarin_proverif_secrecy_rsk_itor_pfs(value):
	
	command = TAMARIN+" --derivcheck-timeout=0 -D"+value+" wireguard_secrecy_macro.spthy +RTS -N1 -RTS -m=proverif > wireguard_secrecy_rsk_itor_pfs_"+value+".p"
	process = Popen(command, stdout=PIPE, stderr=None, shell=True)
	output = process.communicate()[0]

	update_files_pfs_r('wireguard_secrecy_rsk_itor_pfs_'+value+'.p', 'wireguard_secrecy_rsk_itor_pfs_'+value+'.pv')

	os.remove('wireguard_secrecy_rsk_itor_pfs_'+value+'.p')
	
	generate_files_secrecy('wireguard_secrecy_rsk_itor_pfs_'+value+'.pv', 'secrecy_rsk_itor_pfs')



def tamarin_proverif_secrecy_rsk_rtoi(value):
	
	command = TAMARIN+" --derivcheck-timeout=0 -D"+value+" wireguard_secrecy_macro.spthy +RTS -N1 -RTS -m=proverif > wireguard_secrecy_rsk_rtoi_"+value+".p"
	process = Popen(command, stdout=PIPE, stderr=None, shell=True)
	output = process.communicate()[0]

	update_files('wireguard_secrecy_rsk_rtoi_'+value+'.p', 'wireguard_secrecy_rsk_rtoi_'+value+'.pv')

	os.remove('wireguard_secrecy_rsk_rtoi_'+value+'.p')
	
	generate_files_secrecy('wireguard_secrecy_rsk_rtoi_'+value+'.pv', 'secrecy_rsk_rtoi')


def tamarin_proverif_secrecy_rsk_rtoi_pfs(value):
	
	command = TAMARIN+" --derivcheck-timeout=0 -D"+value+" wireguard_secrecy_macro.spthy +RTS -N1 -RTS -m=proverif > wireguard_secrecy_rsk_rtoi_pfs_"+value+".p"
	process = Popen(command, stdout=PIPE, stderr=None, shell=True)
	output = process.communicate()[0]

	update_files_pfs_r('wireguard_secrecy_rsk_rtoi_pfs_'+value+'.p', 'wireguard_secrecy_rsk_rtoi_pfs_'+value+'.pv')

	os.remove('wireguard_secrecy_rsk_rtoi_pfs_'+value+'.p')
	
	generate_files_secrecy('wireguard_secrecy_rsk_rtoi_pfs_'+value+'.pv', 'secrecy_rsk_rtoi_pfs')


"""
def tamarin_proverif_secrecy_isk6_pfs(value):
	
	command = TAMARIN+" -D"+value+" wireguard_secrecy_macro.spthy -m=proverif > wireguard_secrecy_isk6_pfs_"+value+".p"
	process = Popen(command, stdout=PIPE, stderr=None, shell=True)
	output = process.communicate()[0]


	with open('wireguard_secrecy_isk6_pfs_'+value+'.p', 'r') as infile:
		filedata = infile.read()

		filedata = filedata.replace("type nat.\n", "")
		filedata = filedata.replace("new ekI_1:bitstring;", "new ekI_1[]:bitstring;")
		filedata = filedata.replace("new sidI_1:bitstring;", "new sidI_1[]:bitstring;")
		filedata = filedata.replace("new ts_1:bitstring;", "new ts_1[]:bitstring;")
		filedata = filedata.replace("new firstI_1:bitstring;", "new firstI_1[]:bitstring;")
		filedata = filedata.replace("new messageI_1:bitstring;", "new messageI_1[]:bitstring;")

		filedata = filedata.replace("new sidR_1:bitstring;", "new sidR_1[]:bitstring;")
		filedata = filedata.replace("new stp1_1:bitstring;", "new stp1_1[]:bitstring;")
		filedata = filedata.replace("new messageR_1:bitstring;", "new messageR_1[]:bitstring;")
		#filedata = filedata.replace("process", "axiom x: bitstring, y: bitstring, z: bitstring; event(eTest(x, y)) && event(eTest(x, z)) ==> y = z."+"\n\n"+"noselect x:bitstring; attacker(exp(g,x))."+'\n\n'+"process")
		filedata = filedata.replace("process", "noselect x:bitstring; attacker(exp(g,x))."+'\n\n'+"process")

		filedata = filedata.replace("(RevealPsk(psk_1))", "(phase 1; RevealPsk(psk_1))")
		#filedata = filedata.replace("(RevealLtkr(ltkR_1))", "(phase 1; RevealLtkr(ltkR_1))")
		#filedata = filedata.replace("(RevealLtki(ltkI_1))", "(phase 1; RevealLtki(ltkI_1))")


	with open('wireguard_secrecy_isk6_pfs_'+value+'.pv', 'w') as outfile:
		outfile.write(filedata)

	os.remove('wireguard_secrecy_isk6_pfs_'+value+'.p')

	generate_files_secrecy('wireguard_secrecy_isk6_pfs_'+value+'.pv', 'secrecy_isk6_pfs_fast_new')
"""
