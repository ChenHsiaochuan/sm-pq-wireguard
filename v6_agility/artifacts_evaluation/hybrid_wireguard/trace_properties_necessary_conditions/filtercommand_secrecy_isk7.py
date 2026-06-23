#!/usr/bin/env python3.6
'''
Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
'''



input_file = 'process_read_access/secrecy_isk7/wireguard_command'   
output_file = 'process_read_access/secrecy_isk7/wireguard_command_filtered' 

keywords = ["secrecy_isk7_psk.pv", "secrecy_isk7_ldhi_ldhr_precompi.pv", "secrecy_isk7_ldhr_dheki.pv", \
            "secrecy_isk7_kemltkr_rb.pv"]

with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    for line in infile:
        if any(keyword in line for keyword in keywords):
            outfile.write(line)