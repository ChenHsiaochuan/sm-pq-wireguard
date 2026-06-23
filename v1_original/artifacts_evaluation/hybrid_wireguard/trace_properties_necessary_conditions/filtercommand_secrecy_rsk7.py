#!/usr/bin/env python3.6
'''
Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
'''



input_file = 'process_read_access/secrecy_rsk7/wireguard_command'   
output_file = 'process_read_access/secrecy_rsk7/wireguard_command_filtered' 

keywords = ["secrecy_rsk7_psk.pv", "secrecy_rsk7_ldhi_ldhr_precompi.pv", "secrecy_rsk7_ldhi_dhekr.pv", \
            "secrecy_rsk7_kemltki_ra.pv"]

with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    for line in infile:
        if any(keyword in line for keyword in keywords):
            outfile.write(line)