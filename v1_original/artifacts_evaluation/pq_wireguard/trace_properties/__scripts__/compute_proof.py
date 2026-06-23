#!/usr/bin/env python3.6
'''
Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
'''


import os

from subprocess import PIPE, Popen, DEVNULL

TAMARIN="~/.local/bin/tamarin-prover"
#PROVERIF="proverif"
#PROVERIF="../../../../../proverif2.04/./proverif"

def update_files(file_to_read, file_to_write):

	with open(file_to_read, 'r') as infile:
		filedata = infile.read()
		filedata = filedata.replace("type nat.\n", "")
		filedata = filedata.replace("new dhekI_1:bitstring;", "new dhekI_1[]:bitstring;")
		filedata = filedata.replace("new rb_1:bitstring;", "new rb_1[]:bitstring;")
		filedata = filedata.replace("new kemekI_1:bitstring;", "new kemekI_1[]:bitstring;")
		filedata = filedata.replace("new sidI_1:bitstring;", "new sidI_1[]:bitstring;")
		filedata = filedata.replace("new ts_1:bitstring;", "new ts_1[]:bitstring;")
		filedata = filedata.replace("new firstI_1:bitstring;", "new firstI_1[]:bitstring;")
		filedata = filedata.replace("new messageI1_1:bitstring;", "new messageI1_1[]:bitstring;")

		filedata = filedata.replace("new ra_1:bitstring;", "new ra_1[]:bitstring;")
		filedata = filedata.replace("new sidR_1:bitstring;", "new sidR_1[]:bitstring;")
		filedata = filedata.replace("new stp1_1:bitstring;", "new stp1_1[]:bitstring;")
		filedata = filedata.replace("new messageR0_1:bitstring;", "new messageR0_1[]:bitstring;")
		filedata = filedata.replace("process", "axiom x: bitstring, y: bitstring, z: bitstring; event(eTest(x, y)) && event(eTest(x, z)) ==> y = z."+'\n\n'+"process")
		#filedata = filedata.replace("process", "axiom x: bitstring, y: bitstring, z: bitstring; event(eTest(x, y)) && event(eTest(x, z)) ==> y = z."+"\n\n"+"noselect x:bitstring; attacker(exp(g,x))."+'\n\n'+"process")

	with open(file_to_write, 'w') as outfile:
		outfile.write(filedata)


def update_files_pfs(file_to_read, file_to_write):

	with open(file_to_read, 'r') as infile:
		filedata = infile.read()
		filedata = filedata.replace("type nat.\n", "")
		filedata = filedata.replace("new ekI_1:bitstring;", "new ekI_1[]:bitstring;")
		filedata = filedata.replace("new sidI_1:bitstring;", "new sidI_1[]:bitstring;")
		filedata = filedata.replace("new ts_1:bitstring;", "new ts_1[]:bitstring;")
		filedata = filedata.replace("new firstI_1:bitstring;", "new firstI_1[]:bitstring;")
		filedata = filedata.replace("new messageI1_1:bitstring;", "new messageI1_1[]:bitstring;")

		filedata = filedata.replace("new sidR_1:bitstring;", "new sidR_1[]:bitstring;")
		filedata = filedata.replace("new stp1_1:bitstring;", "new stp1_1[]:bitstring;")
		filedata = filedata.replace("new messageR0_1:bitstring;", "new messageR0_1[]:bitstring;")
		#filedata = filedata.replace("process", "axiom x: bitstring, y: bitstring, z: bitstring; event(eTest(x, y)) && event(eTest(x, z)) ==> y = z."+"\n\n"+"noselect x:bitstring; attacker(exp(g,x))."+'\n\n'+"process")
		#filedata = filedata.replace("(RevealPsk(psk_1))", "(phase 1; RevealPsk(psk_1))")
		filedata = filedata.replace("(RevealLtkr(ltkR_1))", "(phase 1; RevealLtkr(ltkR_1))")
		filedata = filedata.replace("(RevealLtki(ltkI_1))", "(phase 1; RevealLtki(ltkI_1))")
		filedata = filedata.replace("(RevealTpki(tpkI_1))", "(phase 1; RevealTpki(tpkI_1))")
		filedata = filedata.replace("(RevealTpkr(tpkR_1))", "(phase 1; RevealTpkr(tpkR_1))")
		#filedata = filedata.replace("(RevealPre(ltkI_1, ltkR_1))", "(phase 1; RevealPre(ltkI_1, ltkR_1))")

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



def generate_files_agrrement(filename, path):
	word = "query"
	count = 0
	with open(filename, 'r') as f:
	    for line in f:
	        words = line.split()
	        for i in words:
	            if(i==word):
	                count=count+1

	for i in range(0,count):
		with open(filename, 'r') as infile:
			with open("../"+path+"/"+filename[:-3]+"_"+str(i)+".pv", 'w') as outfile:
				lines = infile.readlines()
				for index in range(0, len(lines)):
					if word in lines[68]:
						if(index < 68):
							outfile.write(lines[index])
						if(index == 68+4*i):
							outfile.write(lines[index])
						if(index == 68+4*i+1):
							outfile.write(lines[index])
						if(index == 68+4*i+2):
							outfile.write(lines[index])
						if(index == 68+4*i+3):
							outfile.write(lines[index])
						if(index>=68+count*4):
							outfile.write(lines[index])
					if word in lines[69]:
						if(index < 69):
							outfile.write(lines[index])
						if(index == 69+4*i):
							outfile.write(lines[index])
						if(index == 69+4*i+1):
							outfile.write(lines[index])
						if(index == 69+4*i+2):
							outfile.write(lines[index])
						if(index == 69+4*i+3):
							outfile.write(lines[index])
						if(index>=69+count*4):
							outfile.write(lines[index])
					if word in lines[67]:
						if(index < 67):
							outfile.write(lines[index])
						if(index == 67+4*i):
							outfile.write(lines[index])
						if(index == 67+4*i+1):
							outfile.write(lines[index])
						if(index == 67+4*i+2):
							outfile.write(lines[index])
						if(index == 67+4*i+3):
							outfile.write(lines[index])
						if(index>=67+count*4):
							outfile.write(lines[index])
		with open("../"+path+"/wireguard_command", "a") as outfile:
			outfile.write("proverif"+" "+filename[:-3]+"_"+str(i)+".pv"+" > "+filename[:-3]+"_"+str(i)+".pv.log"+"\n")

def generate_files_secrecy(filename, path):
	word = "query"
	keys = ["kemltki", "kemltkr", "tpki", "tpkr", "kemeki", "ra", "rb", "re", "psk"]

	count = 0
	with open(filename, 'r') as f:
	    for line in f:
	        words = line.split()
	        for i in words:
	            if(i==word):
	                count=count+1

	for i in range(0,count):
		with open(filename, 'r') as infile:
			with open("../"+path+"/"+filename[:-3]+"_"+str(i)+".pv", 'w') as outfile:
				lines = infile.readlines()
				for index in range(0, len(lines)):
					if word in lines[68]:
						if(i==0):
							if(index < 68):
								outfile.write(lines[index])
							if(index == 68+4*i):
								outfile.write(lines[index])
							if(index == 68+4*i+1):
								outfile.write(lines[index])
							if(index == 68+4*i+2):
								outfile.write(lines[index])
							#if(index == 69+4*i+3):
								#outfile.write(lines[index])
							if(index>=68+count*4):
								outfile.write(lines[index])
						else:
							if(index < 68):
								outfile.write(lines[index])
							if(index == 68+4*i-1):
								outfile.write(lines[index])
							if(index == 68+4*i):
								outfile.write(lines[index])
							if(index == 68+4*i+1):
								outfile.write(lines[index])
							if(index == 68+4*i+2):
								outfile.write(lines[index])
							#if(index == 69+4*i+3):
								#outfile.write(lines[index])							
							if(index>=68+count*4):
								outfile.write(lines[index])
					if word in lines[69]:
						if(i==0):
							if(index < 69):
								outfile.write(lines[index])
							if(index == 69+4*i):
								outfile.write(lines[index])
							if(index == 69+4*i+1):
								outfile.write(lines[index])
							if(index == 69+4*i+2):
								outfile.write(lines[index])
							#if(index == 69+4*i+3):
								#outfile.write(lines[index])
							if(index>=69+count*4):
								outfile.write(lines[index])
						else:
							if(index < 69):
								outfile.write(lines[index])
							if(index == 69+4*i-1):
								outfile.write(lines[index])
							if(index == 69+4*i):
								outfile.write(lines[index])
							if(index == 69+4*i+1):
								outfile.write(lines[index])
							if(index == 69+4*i+2):
								outfile.write(lines[index])
							#if(index == 69+4*i+3):
								#outfile.write(lines[index])							
							if(index>=69+count*4):
								outfile.write(lines[index])
					if word in lines[67]:
						if(i==0):
							if(index < 67):
								outfile.write(lines[index])
							if(index == 67+4*i):
								outfile.write(lines[index])
							if(index == 67+4*i+1):
								outfile.write(lines[index])
							if(index == 67+4*i+2):
								outfile.write(lines[index])
							#if(index == 69+4*i+3):
								#outfile.write(lines[index])
							if(index>=67+count*4):
								outfile.write(lines[index])
						else:
							if(index < 67):
								outfile.write(lines[index])
							if(index == 67+4*i-1):
								outfile.write(lines[index])
							if(index == 67+4*i):
								outfile.write(lines[index])
							if(index == 67+4*i+1):
								outfile.write(lines[index])
							if(index == 67+4*i+2):
								outfile.write(lines[index])
							#if(index == 69+4*i+3):
								#outfile.write(lines[index])							
							if(index>=67+count*4):
								outfile.write(lines[index])
		with open("../"+path+"/wireguard_command", "a") as outfile:
			outfile.write("proverif"+" "+filename[:-3]+"_"+str(i)+".pv"+" > "+filename[:-3]+"_"+str(i)+".pv.log"+"\n")



"""
def generate_files_secrecy_pfs(filename):
	word = "query"
	count = 0
	with open(filename, 'r') as f:
	    for line in f:
	        words = line.split()
	        for i in words:
	            if(i==word):
	                count=count+1

	for i in range(0,count):
		with open(filename, 'r') as infile:
			with open("../secrecy_isk6_fast_new_10/"+filename[:-3]+"_"+str(i)+".pv", 'w') as outfile:
				lines = infile.readlines()
				for index in range(0, len(lines)):
					if word in lines[69]:
						if(i==0):
							if(index < 69):
								outfile.write(lines[index])
							if(index == 69+4*i):
								outfile.write(lines[index])
							if(index == 69+4*i+1):
								outfile.write(lines[index])
							if(index == 69+4*i+2):
								outfile.write(lines[index])
							#if(index == 69+4*i+3):
								#outfile.write(lines[index])
							if(index>=69+count*4):
								outfile.write(lines[index])
						else:
							if(index < 69):
								outfile.write(lines[index])
							if(index == 69+4*i-1):
								outfile.write(lines[index])
							if(index == 69+4*i):
								outfile.write(lines[index])
							if(index == 69+4*i+1):
								outfile.write(lines[index])
							if(index == 69+4*i+2):
								outfile.write(lines[index])
							#if(index == 69+4*i+3):
								#outfile.write(lines[index])							
							if(index>=69+count*4):
								outfile.write(lines[index])
					if word in lines[68]:
						if(i==0):
							if(index < 68):
								outfile.write(lines[index])
							if(index == 68+4*i):
								outfile.write(lines[index])
							if(index == 68+4*i+1):
								outfile.write(lines[index])
							if(index == 68+4*i+2):
								outfile.write(lines[index])
							#if(index == 69+4*i+3):
								#outfile.write(lines[index])
							if(index>=68+count*4):
								outfile.write(lines[index])
						else:
							if(index < 68):
								outfile.write(lines[index])
							if(index == 68+4*i-1):
								outfile.write(lines[index])
							if(index == 68+4*i):
								outfile.write(lines[index])
							if(index == 68+4*i+1):
								outfile.write(lines[index])
							if(index == 68+4*i+2):
								outfile.write(lines[index])
							#if(index == 69+4*i+3):
								#outfile.write(lines[index])							
							if(index>=68+count*4):
								outfile.write(lines[index])
					if word in lines[69]:
						if(i==0):
							if(index < 69):
								outfile.write(lines[index])
							if(index == 69+4*i):
								outfile.write(lines[index])
							if(index == 69+4*i+1):
								outfile.write(lines[index])
							if(index == 69+4*i+2):
								outfile.write(lines[index])
							#if(index == 69+4*i+3):
								#outfile.write(lines[index])
							if(index>=69+count*4):
								outfile.write(lines[index])
						else:
							if(index < 69):
								outfile.write(lines[index])
							if(index == 69+4*i-1):
								outfile.write(lines[index])
							if(index == 69+4*i):
								outfile.write(lines[index])
							if(index == 69+4*i+1):
								outfile.write(lines[index])
							if(index == 69+4*i+2):
								outfile.write(lines[index])
							#if(index == 69+4*i+3):
								#outfile.write(lines[index])							
							if(index>=69+count*4):
								outfile.write(lines[index])
		with open('../secrecy_isk6_fast_new_10/wireguard_command', "a") as outfile:
			outfile.write("proverif"+" "+filename[:-3]+"_"+str(i)+".pv"+" > "+filename[:-3]+"_"+str(i)+".pv.log"+"\n")
"""

def tamarin_proverif_agreement_inithello(value):

	command = TAMARIN+" --derivcheck-timeout=0 -D"+value+" wireguard_agreement_macro.spthy +RTS -N1 -RTS -m=proverif > wireguard_agreement_inithello_"+value+".p"
	process = Popen(command, stdout=PIPE, stderr=None, shell=True)
	output = process.communicate()[0]

	update_files('wireguard_agreement_inithello_'+value+'.p', 'wireguard_agreement_inithello_'+value+'.pv')

	os.remove('wireguard_agreement_inithello_'+value+'.p')
	
	generate_files_agrrement('wireguard_agreement_inithello_'+value+'.pv', 'agreement_inithello')


def tamarin_proverif_agreement_rechello(value):

	command = TAMARIN+" --derivcheck-timeout=0 -D"+value+" wireguard_agreement_macro.spthy +RTS -N1 -RTS -m=proverif > wireguard_agreement_rechello_"+value+".p"
	process = Popen(command, stdout=PIPE, stderr=None, shell=True)
	output = process.communicate()[0]

	update_files('wireguard_agreement_rechello_'+value+'.p', 'wireguard_agreement_rechello_'+value+'.pv')

	os.remove('wireguard_agreement_rechello_'+value+'.p')
	
	generate_files_agrrement('wireguard_agreement_rechello_'+value+'.pv', 'agreement_rechello')


def tamarin_proverif_agreement_confirm(value):
	
	command = TAMARIN+" --derivcheck-timeout=0 -D"+value+" wireguard_agreement_macro.spthy +RTS -N1 -RTS -m=proverif > wireguard_agreement_confirm_"+value+".p"
	process = Popen(command, stdout=PIPE, stderr=None, shell=True)
	output = process.communicate()[0]

	update_files('wireguard_agreement_confirm_'+value+'.p', 'wireguard_agreement_confirm_'+value+'.pv')

	os.remove('wireguard_agreement_confirm_'+value+'.p')
	
	generate_files_agrrement('wireguard_agreement_confirm_'+value+'.pv', 'agreement_confirm')


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

	update_files('wireguard_secrecy_isk7_'+value+'.p', 'wireguard_secrecy_isk7_'+value+'.pv')

	os.remove('wireguard_secrecy_isk7_'+value+'.p')
	
	generate_files_secrecy('wireguard_secrecy_isk7_'+value+'.pv', 'secrecy_isk7')


def tamarin_proverif_secrecy_isk6_pfs(value):
	
	command = TAMARIN+" -D"+value+" wireguard_secrecy_macro.spthy +RTS -N1 -RTS -m=proverif > wireguard_secrecy_isk6_pfs_"+value+".p"
	process = Popen(command, stdout=DEVNULL, stderr=DEVNULL, shell=True)
	output = process.communicate()[0]

	update_files_pfs('wireguard_secrecy_isk6_pfs_'+value+'.p', 'wireguard_secrecy_isk6_pfs_'+value+'.pv')

	os.remove('wireguard_secrecy_isk6_pfs_'+value+'.p')
	
	generate_files_secrecy('wireguard_secrecy_isk6_pfs_'+value+'.pv', 'secrecy_isk6_pfs')


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

	update_files('wireguard_secrecy_rsk7_'+value+'.p', 'wireguard_secrecy_rsk7_'+value+'.pv')

	os.remove('wireguard_secrecy_rsk7_'+value+'.p')
	
	generate_files_secrecy('wireguard_secrecy_rsk7_'+value+'.pv', 'secrecy_rsk7')


def tamarin_proverif_secrecy_rsk6_pfs(value):
	
	command = TAMARIN+" -D"+value+" wireguard_secrecy_macro.spthy +RTS -N1 -RTS -m=proverif > wireguard_secrecy_rsk6_pfs_"+value+".p"
	process = Popen(command, stdout=DEVNULL, stderr=DEVNULL, shell=True)
	output = process.communicate()[0]

	update_files_pfs_r('wireguard_secrecy_rsk6_pfs_'+value+'.p', 'wireguard_secrecy_rsk6_pfs_'+value+'.pv')

	os.remove('wireguard_secrecy_rsk6_pfs_'+value+'.p')
	
	generate_files_secrecy('wireguard_secrecy_rsk6_pfs_'+value+'.pv', 'secrecy_rsk6_pfs')



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
