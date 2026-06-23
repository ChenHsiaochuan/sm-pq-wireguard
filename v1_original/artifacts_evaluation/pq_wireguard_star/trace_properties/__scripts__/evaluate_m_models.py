#!/usr/bin/env python3.6
'''
Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
'''


import os
import sys

def generate_spthy_w(logfile, spthyfile, newspthyfile):
	with open(logfile) as infile1:
		Lines = infile1.readlines()
		for line in Lines:
			if " is true." in line:
				with open(spthyfile, 'r') as infile2:
					filedata = infile2.read()
					if "eRevPsk" in line:
						filedata = filedata.replace("in(~psk);", "new ~psk; event Honestpsk(~psk);")
						filedata = filedata.replace(" && (attacker(ck)@j).", " && event(eHonestpsk(psk)) && (attacker(ck)@j).")
						filedata = filedata.replace(" && (attacker(ck)@z).", " && event(eHonestpsk(psk)) && (attacker(ck)@z).")
						filedata = filedata.replace(" ==> ", " && event(eHonestpsk(psk)) ==> ")


					if "eRevDHEki" in line:
						filedata = filedata.replace("in(~dhekI);", "new ~dhekI; event Honestei('g'^~dhekI);")
						filedata = filedata.replace(" && (attacker(ck)@j).", " && event(eHonestei(dheki)) && (attacker(ck)@j).")
						filedata = filedata.replace(" && (attacker(ck)@z).", " && event(eHonestei(dheki)) && (attacker(ck)@z).")
						filedata = filedata.replace(" ==> ", " && event(eHonestei(dheki)) ==> ")


					if "eRevKEMEki" in line:
						filedata = filedata.replace("in(~kemekI);", "new ~kemekI; event Honestei(pk(~kemekI));")
						filedata = filedata.replace(" && (attacker(ck)@j).", " && event(eHonestei(kempeki)) && (attacker(ck)@j).")
						filedata = filedata.replace(" && (attacker(ck)@z).", " && event(eHonestei(kempeki)) && (attacker(ck)@z).")
						filedata = filedata.replace(" ==> ", " && event(eHonestei(kempeki)) ==> ")


					if "eRevDHEkr" in line:
						filedata = filedata.replace("in(~dhekR);", "new ~dhekR; event Honester('g'^~dhekR);")
						filedata = filedata.replace(" && (attacker(ck)@j).", " && event(eHonester(dhekr)) && (attacker(ck)@j).")
						filedata = filedata.replace(" && (attacker(ck)@z).", " && event(eHonester(dhekr)) && (attacker(ck)@z).")
						filedata = filedata.replace(" ==> ", " && event(eHonester(dhekr)) ==> ")


					if "eRevLdhi" in line:
						filedata = filedata.replace("in(~ldhI);", "new ~ldhI; event Honesti('g'^~ldhI);")
						filedata = filedata.replace(" && (attacker(ck)@j).", " && event(eHonesti(ldhi)) && (attacker(ck)@j).")
						filedata = filedata.replace(" && (attacker(ck)@z).", " && event(eHonesti(ldhi)) && (attacker(ck)@z).")
						filedata = filedata.replace(" ==> ", " && event(eHonesti(ldhi)) ==> ")


					if "eRevLdhr" in line:
						filedata = filedata.replace("in(~ldhR);", "new ~ldhR; event Honestr('g'^~ldhR);")
						filedata = filedata.replace(" && (attacker(ck)@j).", " && event(eHonestr(ldhr)) && (attacker(ck)@j).")
						filedata = filedata.replace(" && (attacker(ck)@z).", " && event(eHonestr(ldhr)) && (attacker(ck)@z).")
						filedata = filedata.replace(" ==> ", " && event(eHonestr(ldhr)) ==> ")



					if "eRevKEMLtki" in line:
						filedata = filedata.replace("in(~kemltkI);", "new ~kemltkI; event Honesti(pk(~kemltkI));")
						filedata = filedata.replace(" && (attacker(ck)@j).", " && event(eHonesti(kemltki)) && (attacker(ck)@j).")
						filedata = filedata.replace(" && (attacker(ck)@z).", " && event(eHonesti(kemltki)) && (attacker(ck)@z).")
						filedata = filedata.replace(" ==> ", " && event(eHonesti(kemltki)) ==> ")


					if "eRevKEMLtkr" in line:
						filedata = filedata.replace("in(~kemltkR);", "new ~kemltkR; event Honestr(pk(~kemltkR));")
						filedata = filedata.replace(" && (attacker(ck)@j).", " && event(eHonestr(kemltkr)) && (attacker(ck)@j).")
						filedata = filedata.replace(" && (attacker(ck)@z).", " && event(eHonestr(kemltkr)) && (attacker(ck)@z).")
						filedata = filedata.replace(" ==> ", " && event(eHonestr(kemltkr)) ==> ")


					if "eRevRa" in line:
						filedata = filedata.replace("in(~ra);", "new ~ra; event Honestra(~ra);")
						filedata = filedata.replace(" && (attacker(ck)@j).", " && event(eHonestra(ra)) && (attacker(ck)@j).")
						filedata = filedata.replace(" && (attacker(ck)@z).", " && event(eHonestra(ra)) && (attacker(ck)@z).")
						filedata = filedata.replace(" ==> ", " && event(eHonestra(ra)) ==> ")


					if "eRevRb" in line:
						filedata = filedata.replace("in(~rb);", "new ~rb; event Honestrb(~rb);")
						filedata = filedata.replace(" && (attacker(ck)@j).", " && event(eHonestrb(rb)) && (attacker(ck)@j).")
						filedata = filedata.replace(" && (attacker(ck)@z).", " && event(eHonestrb(rb)) && (attacker(ck)@z).")
						filedata = filedata.replace(" ==> ", " && event(eHonestrb(rb)) ==> ")


					if "eRevRe" in line:
						filedata = filedata.replace("in(~re);", "new ~re; event Honestre(~re);")
						filedata = filedata.replace(" && (attacker(ck)@j).", " && event(eHonestre(re)) && (attacker(ck)@j).")
						filedata = filedata.replace(" && (attacker(ck)@z).", " && event(eHonestre(re)) && (attacker(ck)@z).")
						filedata = filedata.replace(" ==> ", " && event(eHonestre(re)) ==> ")




					if "eRevPre" in line:
						filedata = filedata.replace("in(sisr);", "let sisr = (dhpkR)^~ldhI in")
						filedata = filedata.replace("in(srsi);", "let srsi = (dhpkI)^~ldhR in")


				with open(newspthyfile, 'w') as outfile:
					outfile.write(filedata)




def generate_logfiles(logfile, outdir):
	#directory = os.path.dirname(logfile)
	name, extension = os.path.splitext(os.path.basename(logfile))
	with open(logfile, "r") as infile:
		i = 0
		for line in infile:
			if " is true" in line:
				i += 1
				outfile = str(os.path.join(outdir, f"{name}_{i}{extension}"))
				with open(outfile, "w") as out_file:
					out_file.write(line)
				out_file.close


def generate_pv_w(file_to_read, file_to_write):
	with open(file_to_read, 'r') as infile:
		filedata = infile.read()
		filedata = filedata.replace("free att:channel.\n", "set preciseActions = true.\nfree att:channel.\n")

	with open(file_to_write, 'w') as outfile:
		outfile.write(filedata)