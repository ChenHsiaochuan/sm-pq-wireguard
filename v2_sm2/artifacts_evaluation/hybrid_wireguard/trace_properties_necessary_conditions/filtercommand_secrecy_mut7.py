#!/usr/bin/env python3.6
'''
Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
'''



input_file = 'process_read_access/secrecy_mut7/wireguard_command'   
output_file = 'process_read_access/secrecy_mut7/wireguard_command_filtered' 

keywords = ["secrecy_mut7_psk.pv", "secrecy_mut7_ldhi_ldhr_precompi.pv", "secrecy_mut7_ldhi_dhekr.pv", "secrecy_mut7_ldhr_dheki.pv", \
            "secrecy_mut7_dheki_dhekr.pv", "secrecy_mut7_kemltki_ra.pv", "secrecy_mut7_kemltki_ra.pv", "secrecy_mut7_kemltkr_rb.pv", \
            "secrecy_mut7_kemeki_re.pv"]

with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    for line in infile:
        if any(keyword in line for keyword in keywords):
            outfile.write(line)