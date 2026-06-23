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

def update_files(file_to_read, file_to_write):

	with open(file_to_read, 'r') as infile:
		filedata = infile.read()
		filedata = filedata.replace("type nat.\n", "")
		filedata = filedata.replace("new sidI_2:bitstring;", "new sidI_2[]:bitstring;")
		filedata = filedata.replace("new ts_2:bitstring;", "new ts_2[]:bitstring;")
		filedata = filedata.replace("new firstI_2:bitstring;", "new firstI_2[]:bitstring;")
		filedata = filedata.replace("new messageI1_2:bitstring;", "new messageI1_2[]:bitstring;")
		filedata = filedata.replace("new sidR_2:bitstring;", "new sidR_2[]:bitstring;")
		filedata = filedata.replace("new messageR0_2:bitstring;", "new messageR0_2[]:bitstring;")
		filedata = filedata.replace("new stamp_2:bitstring;", "new stamp_2[]:bitstring;")
		filedata = filedata.replace("new ra_2:bitstring;", "new ra_2[]:bitstring;")
		filedata = filedata.replace("new rb_2:bitstring;", "new rb_2[]:bitstring;")
		filedata = filedata.replace("new re_2:bitstring;", "new re_2[]:bitstring;")
		filedata = filedata.replace("new kemekI_2:bitstring;", "new kemekI_2[]:bitstring;")


	with open(file_to_write, 'w') as outfile:
		outfile.write(filedata)


def update_files_lateral(file_to_read, file_to_write):

	with open(file_to_read, 'r') as infile:
		filedata = infile.read()
		filedata = filedata.replace("type nat.\n", "")


	with open(file_to_write, 'w') as outfile:
		outfile.write(filedata)



def update_files_pfs(file_to_read, file_to_write):

	with open(file_to_read, 'r') as infile:
		filedata = infile.read()
		filedata = filedata.replace("type nat.\n", "")
		filedata = filedata.replace("new sidI_2:bitstring;", "new sidI_2[]:bitstring;")
		filedata = filedata.replace("new ts_2:bitstring;", "new ts_2[]:bitstring;")
		filedata = filedata.replace("new firstI_2:bitstring;", "new firstI_2[]:bitstring;")
		filedata = filedata.replace("new messageI1_2:bitstring;", "new messageI1_2[]:bitstring;")
		filedata = filedata.replace("new sidR_2:bitstring;", "new sidR_2[]:bitstring;")
		filedata = filedata.replace("new messageR0_2:bitstring;", "new messageR0_2[]:bitstring;")
		filedata = filedata.replace("new stamp_2:bitstring;", "new stamp_2[]:bitstring;")
		filedata = filedata.replace("new ra_2:bitstring;", "new ra_2[]:bitstring;")
		filedata = filedata.replace("new rb_2:bitstring;", "new rb_2[]:bitstring;")
		filedata = filedata.replace("new re_2:bitstring;", "new re_2[]:bitstring;")
		filedata = filedata.replace("new kemekI_2:bitstring;", "new kemekI_2[]:bitstring;")
		filedata = filedata.replace("(RevealPsk(psk_2))", "(phase 1; RevealPsk(psk_2))")
		filedata = filedata.replace("(RevealKEMLtk(kemltkR_2))", "(phase 1; RevealKEMLtk(kemltkR_2))")
		filedata = filedata.replace("(RevealKEMLtk(kemltkI_2))", "(phase 1; RevealKEMLtk(kemltkI_2))")
		filedata = filedata.replace("(RevealTpk(tpkI_2))", "(phase 1; RevealTpk(tpkI_2))")
		filedata = filedata.replace("(RevealTpk(tpkR_2))", "(phase 1; RevealTpk(tpkR_2))")


	with open(file_to_write, 'w') as outfile:
		outfile.write(filedata)


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

Sc = S1c+S2c+S3c+S4c+S5c+S6c+S7c+S8c+S9c


def generate_files_agreement(filename, path):

	with open(filename, 'r') as f:
		content = f.read()
		words = content.split()
		words = re.findall(r'\b\w+\b', content)
		count = words.count(word)

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
	
	with open("../"+path+"/wireguard_command_0", "a") as commandfile0:
		commandfile0.write("proverif"+" "+filename[:-3]+"_0.pv"+" > "+filename[:-3]+"_0.pv.0log"+"\n")
	commandfile0.close()

	with open("../"+path+"/wireguard_command", "r") as commandfile:
		lines = commandfile.readlines()
		for index in range(0, len(lines)):
			if lines[index].count('_') in range(6, 33, 2):
				numb = str(lines[index].count('_')//2 -2)
				#print(numb)
				with open("../"+path+"/wireguard_command_"+numb, "a") as commandfile1:
					commandfile1.write(lines[index])
				commandfile1.close()
				with open("../"+path+"/wireguard_command_"+numb, "r") as infile:
					content = infile.read()
					new_content = content.replace(".log", "."+numb+"log")
				infile.close()
				with open("../"+path+"/wireguard_command_"+numb, "w") as outfile:
					outfile.write(new_content)
				outfile.close()

	with open("../"+path+"/wireguard_command_1", "r") as infile, open("../"+path+"/wireguard_command_1_opt", "w") as outfile:
		content = infile.read()
		outfile.write(content)

def generate_files_uniqueness(filename, path):

	with open(filename, 'r') as f:
		content = f.read()
		words = content.split()
		words = re.findall(r'\b\w+\b', content)
		count = words.count(word)

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

	with open("../"+path+"/wireguard_command_0", "a") as commandfile0:
		commandfile0.write("proverif"+" "+filename[:-3]+"_0.pv"+" > "+filename[:-3]+"_0.pv.0log"+"\n")
	commandfile0.close()


	with open("../"+path+"/wireguard_command", "r") as commandfile:
		lines = commandfile.readlines()
		for index in range(0, len(lines)):
			if lines[index].count('_') in range(6, 33, 2):
				numb = str(lines[index].count('_')//2 -2)
				#print(numb)
				with open("../"+path+"/wireguard_command_"+numb, "a") as commandfile1:
					commandfile1.write(lines[index])
				commandfile1.close()
				with open("../"+path+"/wireguard_command_"+numb, "r") as infile:
					content = infile.read()
					new_content = content.replace(".log", "."+numb+"log")
				infile.close()
				with open("../"+path+"/wireguard_command_"+numb, "w") as outfile:
					outfile.write(new_content)
				outfile.close()

	with open("../"+path+"/wireguard_command_1", "r") as infile, open("../"+path+"/wireguard_command_1_opt", "w") as outfile:
		content = infile.read()
		outfile.write(content)



def generate_files_unilateral(filename, path):

	with open(filename, 'r') as f:
		content = f.read()
		words = content.split()
		words = re.findall(r'\b\w+\b', content)
		count = words.count(word)

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

	with open("../"+path+"/wireguard_command_0", "a") as commandfile0:
		commandfile0.write("proverif"+" "+filename[:-3]+"_0.pv"+" > "+filename[:-3]+"_0.pv.0log"+"\n")
	commandfile0.close()


	with open("../"+path+"/wireguard_command", "r") as commandfile:
		lines = commandfile.readlines()
		for index in range(0, len(lines)):
			if lines[index].count('_') in range(6, 33, 2):
				numb = str(lines[index].count('_')//2 -2)
				#print(numb)
				with open("../"+path+"/wireguard_command_"+numb, "a") as commandfile1:
					commandfile1.write(lines[index])
				commandfile1.close()
				with open("../"+path+"/wireguard_command_"+numb, "r") as infile:
					content = infile.read()
					new_content = content.replace(".log", "."+numb+"log")
				infile.close()
				with open("../"+path+"/wireguard_command_"+numb, "w") as outfile:
					outfile.write(new_content)
				outfile.close()

	with open("../"+path+"/wireguard_command_1", "r") as infile, open("../"+path+"/wireguard_command_1_opt", "w") as outfile:
		content = infile.read()
		outfile.write(content)



def generate_files_bilateral(filename, path):

	with open(filename, 'r') as f:
		content = f.read()
		words = content.split()
		words = re.findall(r'\b\w+\b', content)
		count = words.count(word)

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

	with open("../"+path+"/wireguard_command_0", "a") as commandfile0:
		commandfile0.write("proverif"+" "+filename[:-3]+"_0.pv"+" > "+filename[:-3]+"_0.pv.0log"+"\n")
	commandfile0.close()


	with open("../"+path+"/wireguard_command", "r") as commandfile:
		lines = commandfile.readlines()
		for index in range(0, len(lines)):
			if lines[index].count('_') in range(2, 29, 2):
				numb = str(lines[index].count('_')//2 -1)
				#print(numb)
				with open("../"+path+"/wireguard_command_"+numb, "a") as commandfile1:
					commandfile1.write(lines[index])
				commandfile1.close()
				with open("../"+path+"/wireguard_command_"+numb, "r") as infile:
					content = infile.read()
					new_content = content.replace(".log", "."+numb+"log")
				infile.close()
				with open("../"+path+"/wireguard_command_"+numb, "w") as outfile:
					outfile.write(new_content)
				outfile.close()

	with open("../"+path+"/wireguard_command_1", "r") as infile, open("../"+path+"/wireguard_command_1_opt", "w") as outfile:
		content = infile.read()
		outfile.write(content)

	
def generate_files_secrecy(filename, path):

	count = 0
	with open(filename, 'r') as f:
	    for line in f:
	        words = line.split()
	        for i in words:
	            if(i==word):
	                count=count+1
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

	with open("../"+path+"/wireguard_command_0", "a") as commandfile0:
		commandfile0.write("proverif"+" "+filename[:-3]+"_0.pv"+" > "+filename[:-3]+"_0.pv.0log"+"\n")
	commandfile0.close()


	with open("../"+path+"/wireguard_command", "r") as commandfile:
		lines = commandfile.readlines()
		for index in range(0, len(lines)):
			if lines[index].count('_') in range(6, 33, 2):
				numb = str(lines[index].count('_')//2 -2)
				#print(numb)
				with open("../"+path+"/wireguard_command_"+numb, "a") as commandfile1:
					commandfile1.write(lines[index])
				commandfile1.close()
				with open("../"+path+"/wireguard_command_"+numb, "r") as infile:
					content = infile.read()
					new_content = content.replace(".log", "."+numb+"log")
				infile.close()
				with open("../"+path+"/wireguard_command_"+numb, "w") as outfile:
					outfile.write(new_content)
				outfile.close()

	with open("../"+path+"/wireguard_command_1", "r") as infile, open("../"+path+"/wireguard_command_1_opt", "w") as outfile:
		content = infile.read()
		outfile.write(content)


def tamarin_proverif_uniqueness_initiator():

	command = TAMARIN+" --derivcheck-timeout=0 -Dall_trusted wireguard_uniqueness_initiator_macro.spthy +RTS -N1 -RTS -m=proverif > wireguard_uniqueness_initiator.p 2> /dev/null"
	process = Popen(command, stdout=PIPE, stderr=None, shell=True)
	output = process.communicate()[0]

	update_files('wireguard_uniqueness_initiator.p', 'wireguard_uniqueness_initiator.pv')

	os.remove('wireguard_uniqueness_initiator.p')
	
	generate_files_uniqueness('wireguard_uniqueness_initiator.pv', 'uniqueness_initiator')


def tamarin_proverif_uniqueness_responder():

	command = TAMARIN+" --derivcheck-timeout=0 -Dall_trusted wireguard_uniqueness_responder_macro.spthy +RTS -N1 -RTS -m=proverif > wireguard_uniqueness_responder.p 2> /dev/null"
	process = Popen(command, stdout=PIPE, stderr=None, shell=True)
	output = process.communicate()[0]

	update_files('wireguard_uniqueness_responder.p', 'wireguard_uniqueness_responder.pv')

	os.remove('wireguard_uniqueness_responder.p')
	
	generate_files_uniqueness('wireguard_uniqueness_responder.pv', 'uniqueness_responder')



def tamarin_proverif_unilateral_initiator():

	command = TAMARIN+" --derivcheck-timeout=0 -Dall_trusted wireguard_macro_u.spthy +RTS -N1 -RTS -m=proverif > wireguard_unilateral_initiator.p 2> /dev/null"
	process = Popen(command, stdout=PIPE, stderr=None, shell=True)
	output = process.communicate()[0]

	update_files_lateral('wireguard_unilateral_initiator.p', 'wireguard_unilateral_initiator.pv')

	os.remove('wireguard_unilateral_initiator.p')
	
	generate_files_unilateral('wireguard_unilateral_initiator.pv', 'unilateral_initiator')


def tamarin_proverif_unilateral_responder():

	command = TAMARIN+" --derivcheck-timeout=0 -Dall_trusted wireguard_macro_u.spthy +RTS -N1 -RTS -m=proverif > wireguard_unilateral_responder.p 2> /dev/null"
	process = Popen(command, stdout=PIPE, stderr=None, shell=True)
	output = process.communicate()[0]

	update_files_lateral('wireguard_unilateral_responder.p', 'wireguard_unilateral_responder.pv')

	os.remove('wireguard_unilateral_responder.p')
	
	generate_files_unilateral('wireguard_unilateral_responder.pv', 'unilateral_responder')



def tamarin_proverif_bilateral():

	command = TAMARIN+" --derivcheck-timeout=0 -Dall_trusted wireguard_macro_u.spthy +RTS -N1 -RTS -m=proverif > wireguard_bilateral.p 2> /dev/null"
	process = Popen(command, stdout=PIPE, stderr=None, shell=True)
	output = process.communicate()[0]

	update_files_lateral('wireguard_bilateral.p', 'wireguard_bilateral.pv')

	os.remove('wireguard_bilateral.p')
	
	generate_files_bilateral('wireguard_bilateral.pv', 'bilateral')



def tamarin_proverif_agreement_inithello():

	command = TAMARIN+" --derivcheck-timeout=0 -Dall_trusted wireguard_macro.spthy +RTS -N1 -RTS -m=proverif > wireguard_agreement_inithello.p 2> /dev/null"
	process = Popen(command, stdout=PIPE, stderr=None, shell=True)
	output = process.communicate()[0]

	update_files('wireguard_agreement_inithello.p', 'wireguard_agreement_inithello.pv')

	os.remove('wireguard_agreement_inithello.p')
	
	generate_files_agreement('wireguard_agreement_inithello.pv', 'agreement_inithello')


def tamarin_proverif_agreement_rechello():

	command = TAMARIN+" --derivcheck-timeout=0 -Dall_trusted wireguard_macro.spthy +RTS -N1 -RTS -m=proverif > wireguard_agreement_rechello.p 2> /dev/null"
	process = Popen(command, stdout=PIPE, stderr=None, shell=True)
	output = process.communicate()[0]

	update_files('wireguard_agreement_rechello.p', 'wireguard_agreement_rechello.pv')

	os.remove('wireguard_agreement_rechello.p')
	
	generate_files_agreement('wireguard_agreement_rechello.pv', 'agreement_rechello')


def tamarin_proverif_agreement_confirm():
	
	command = TAMARIN+" --derivcheck-timeout=0 -Dall_trusted wireguard_macro.spthy +RTS -N1 -RTS -m=proverif > wireguard_agreement_confirm.p 2> /dev/null"
	process = Popen(command, stdout=PIPE, stderr=None, shell=True)
	output = process.communicate()[0]

	update_files('wireguard_agreement_confirm.p', 'wireguard_agreement_confirm.pv')

	os.remove('wireguard_agreement_confirm.p')

	generate_files_agreement('wireguard_agreement_confirm.pv', 'agreement_confirm')


def tamarin_proverif_secrecy_isk7():
	
	command = TAMARIN+" --derivcheck-timeout=0 -Dall_trusted wireguard_macro.spthy +RTS -N1 -RTS -m=proverif > wireguard_secrecy_isk7.p 2> /dev/null"
	process = Popen(command, stdout=PIPE, stderr=None, shell=True)
	output = process.communicate()[0]

	update_files('wireguard_secrecy_isk7.p', 'wireguard_secrecy_isk7.pv')

	os.remove('wireguard_secrecy_isk7.p')
	
	generate_files_secrecy('wireguard_secrecy_isk7.pv', 'secrecy_isk7')


def tamarin_proverif_secrecy_isk7pfs():
	
	command = TAMARIN+" --derivcheck-timeout=0 -Dall_trusted wireguard_macro.spthy +RTS -N1 -RTS -m=proverif > wireguard_secrecy_isk7pfs.p 2> /dev/null"
	process = Popen(command, stdout=DEVNULL, stderr=DEVNULL, shell=True)
	output = process.communicate()[0]

	update_files_pfs('wireguard_secrecy_isk7pfs.p', 'wireguard_secrecy_isk7pfs.pv')

	os.remove('wireguard_secrecy_isk7pfs.p')
	
	generate_files_secrecy('wireguard_secrecy_isk7pfs.pv', 'secrecy_isk7pfs')


def tamarin_proverif_secrecy_mut7():
	
	command = TAMARIN+" --derivcheck-timeout=0 -Dall_trusted wireguard_macro.spthy +RTS -N1 -RTS -m=proverif > wireguard_secrecy_mut7.p 2> /dev/null"
	process = Popen(command, stdout=PIPE, stderr=None, shell=True)
	output = process.communicate()[0]

	update_files('wireguard_secrecy_mut7.p', 'wireguard_secrecy_mut7.pv')

	os.remove('wireguard_secrecy_mut7.p')
	
	generate_files_secrecy('wireguard_secrecy_mut7.pv', 'secrecy_mut7')


def tamarin_proverif_secrecy_mut7pfs():
	
	command = TAMARIN+" --derivcheck-timeout=0 -Dall_trusted wireguard_macro.spthy +RTS -N1 -RTS -m=proverif > wireguard_secrecy_mut7pfs.p 2> /dev/null"
	process = Popen(command, stdout=DEVNULL, stderr=DEVNULL, shell=True)
	output = process.communicate()[0]

	update_files_pfs('wireguard_secrecy_mut7pfs.p', 'wireguard_secrecy_mut7pfs.pv')

	os.remove('wireguard_secrecy_mut7pfs.p')
	
	generate_files_secrecy('wireguard_secrecy_mut7pfs.pv', 'secrecy_mut7pfs')


def tamarin_proverif_secrecy_rsk7():
	
	command = TAMARIN+" --derivcheck-timeout=0 -Dall_trusted wireguard_macro.spthy +RTS -N1 -RTS -m=proverif > wireguard_secrecy_rsk7.p 2> /dev/null"
	process = Popen(command, stdout=PIPE, stderr=None, shell=True)
	output = process.communicate()[0]

	update_files('wireguard_secrecy_rsk7.p', 'wireguard_secrecy_rsk7.pv')

	os.remove('wireguard_secrecy_rsk7.p')
	
	generate_files_secrecy('wireguard_secrecy_rsk7.pv', 'secrecy_rsk7')


def tamarin_proverif_secrecy_rsk7pfs():
	
	command = TAMARIN+" --derivcheck-timeout=0 -Dall_trusted wireguard_macro.spthy +RTS -N1 -RTS -m=proverif > wireguard_secrecy_rsk7pfs.p 2> /dev/null"
	process = Popen(command, stdout=DEVNULL, stderr=DEVNULL, shell=True)
	output = process.communicate()[0]

	update_files_pfs('wireguard_secrecy_rsk7pfs.p', 'wireguard_secrecy_rsk7pfs.pv')

	os.remove('wireguard_secrecy_rsk7pfs.p')
	
	generate_files_secrecy('wireguard_secrecy_rsk7pfs.pv', 'secrecy_rsk7pfs')
