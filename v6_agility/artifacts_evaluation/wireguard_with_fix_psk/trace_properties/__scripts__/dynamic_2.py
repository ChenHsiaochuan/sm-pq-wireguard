#!/usr/bin/env python3.6
'''
Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
'''


import os
import re
import itertools

subkeys = ["eRevLDH(ldhi)", "eRevLDH(ldhr)", "eRevPre", "eRevDHE(dheki)", "eRevDHE(dhekr)", "eRevPsk"]
replacement = {"eRevLDH(ldhi)": "_ldhi", "eRevLDH(ldhr)": "_ldhr", "eRevPre": "_precompi", "eRevDHE(dheki)": "_dheki", "eRevDHE(dhekr)": "_dhekr", "eRevPsk": "_psk"}


combinations_dict = {
    1: [(key,) for key in subkeys],
    2: list(itertools.combinations(subkeys, 2)),
    3: list(itertools.combinations(subkeys, 3)),
    4: list(itertools.combinations(subkeys, 4)),
    5: list(itertools.combinations(subkeys, 5)),
}

comb_results = {}
rep_comb_results = {}

result = r"RESULT(.*?)==>"
replace = ""

def extract_combinations(filename, combinations_list):
    results = []
    with open(filename, "r") as infile:
        for line in infile:
            if "is true" in line:
                for combo in combinations_list:
                    if all(key in line for key in combo):
                        results.append(combo)
    return results


def generate_replacement(index):
    with open(f"wireguard_command_{index}.{index}log", "r") as infile:
        filedata = infile.read()
        newfiledata = re.sub(result, replace, filedata)
        with open(f"wireguard_command_{index}.lg", "w") as outfile:
            outfile.write(newfiledata)

    comb = extract_combinations(f"wireguard_command_{index}.lg", combinations_dict[index])
    comb_results[index] = comb

    rep_comb = [replacement.get(event[0], event[0]) for event in comb]
    rep_comb_results[index] = rep_comb

    os.remove(f"wireguard_command_{index}.lg")


def generate_optimize(index):
    with open(f"wireguard_command_{index}", "r") as infile, open(f'wireguard_command_{index}_opt', 'w') as outfile:
        for line in infile:
            if not any(key in line for key in rep_comb_results[index-1]):
                outfile.write(line)


generate_replacement(1)
generate_optimize(2)