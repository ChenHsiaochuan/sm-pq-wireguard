#!/usr/bin/env python3.6
'''
Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
'''


output_file = 'process_read_access/uniqueness_initiator/wireguard_command_filtered' 

with open(output_file, 'w') as outfile:
    line = "proverif wireguard_uniqueness_initiator_0.pv > wireguard_uniqueness_initiator_0.pv.log"
    outfile.write(line)