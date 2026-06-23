#!/usr/bin/env python3.6
'''
Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
'''


import os
import sys
from subprocess import PIPE, Popen

TAMARIN = "~/.local/bin/tamarin-prover"
LOG_COUNT = 10  


def generate_spthy_w(logfile, spthyfile, newspthyfile):
	with open(logfile) as infile1:
		Lines = infile1.readlines()
		for line in Lines:
			if " is true." in line:
				with open(spthyfile, 'r') as infile2:
					filedata = infile2.read()
					if "eRevPsk" in line:
						filedata = filedata.replace("in(~psk);", "new ~psk;")

					if "eRevKEMEki" in line:
						filedata = filedata.replace("in(~kemekI);", "new ~kemekI;")

					if "eRevKEMLtk(kemltki" in line:
						filedata = filedata.replace("in(~kemltkI);", "new ~kemltkI;")

					if "eRevKEMLtk(kemltkr" in line:
						filedata = filedata.replace("in(~kemltkR);", "new ~kemltkR;")

					if "eRevTpk(tpkr" in line:
						filedata = filedata.replace("in(~tpkR);", "new ~tpkR;")
						#filedata = filedata.replace("in(ka);", "let ka = h(<~ra, tpkR>) in")

					if "eRevTpk(tpki" in line:
						filedata = filedata.replace("in(~tpkI);", "new ~tpkI;")
						#filedata = filedata.replace("in(kb);", "let kb = h(<~rb, tpkI>) in")

					if "eRevRb" in line:
						filedata = filedata.replace("in(~rb);", "new ~rb;")
						#filedata = filedata.replace("in(kb);", "let kb = h(<~rb, tpkI>) in")

					if "eRevRa" in line:
						filedata = filedata.replace("in(~ra);", "new ~ra;")
						#filedata = filedata.replace("in(ka);", "let ka = h(<~ra, tpkR>) in")

					if "eRevRe" in line:
						filedata = filedata.replace("in(~re);", "new ~re;")
						#filedata = filedata.replace("in(ke);", "let ke = h(~re) in")

				with open(newspthyfile, 'w') as outfile:
					outfile.write(filedata)



def generate_logfiles(logfile, outdir):
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


def main(profile):
    base_dir = f"process_write_access/{profile}"
    log_dir = os.path.join(base_dir, "log/")
    spthy_ref_file = os.path.join(base_dir, f"wireguard_{profile}.spthy")
    spthy_dir = os.path.join(base_dir, "spthy/")
    pv_dir = os.path.join(base_dir, "pv/")

    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(spthy_dir, exist_ok=True)
    os.makedirs(pv_dir, exist_ok=True)

    for i in range(LOG_COUNT):
        log_path = f"process_read_access/{profile}/wireguard_command_{i}.{i}log"
        if os.path.exists(log_path):
            generate_logfiles(log_path, log_dir)

    name, extension = os.path.splitext(os.path.basename(spthy_ref_file))
    for i, file_name in enumerate(os.listdir(log_dir), start=1):
        file_path = os.path.join(log_dir, file_name)
        out_spthy_file = os.path.join(spthy_dir, f"{name}_{i}{extension}")
        out_p_file = os.path.join(spthy_dir, f"{name}_{i}.p")
        out_pv_file = os.path.join(pv_dir, f"{name}_{i}.pv")

        generate_spthy_w(file_path, spthy_ref_file, out_spthy_file)

        command = f"{TAMARIN} --derivcheck-timeout=0 {out_spthy_file} +RTS -N1 -RTS -m=proverif > {out_p_file} 2> /dev/null"
        process = Popen(command, stdout=PIPE, stderr=None, shell=True)
        process.communicate()

        generate_pv_w(out_p_file, out_pv_file)

    command_script_path = os.path.join(pv_dir, "wireguard_command")
    with open(command_script_path, "a") as command_file:
        for file in os.listdir(pv_dir):
            if file.endswith(".pv"):
                command_file.write(f"proverif {file} > {file}.log\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_wireguard_analysis.py <profile>")
        print("Example profiles: secrecy_rsk7, secrecy_isk7, agreement_confirm")
        sys.exit(1)
    main(sys.argv[1])
