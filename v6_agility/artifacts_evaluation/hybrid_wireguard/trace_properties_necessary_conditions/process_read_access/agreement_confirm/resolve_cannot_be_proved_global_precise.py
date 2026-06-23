#!/usr/bin/env python3.6
'''
Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
'''


import os
import shutil
from glob import glob

def search_and_copy(string_to_search, ext1, ext2, source_folder, destination_folder):
    # Find files with extension ext2
    ext2_files = glob(os.path.join(source_folder, f"*{ext2}"))

    for ext2_file in ext2_files:
        with open(ext2_file, 'r') as file:
            content = file.read()
            ext2_file = os.path.basename(ext2_file).lstrip("./")
            if string_to_search in content:
                ext1_file = os.path.splitext(ext2_file)[0] 
                #+ f'{ext1}'
                #print(ext1_file)
                shutil.copy(ext1_file, destination_folder)

def replace_string_in_files(directory, old_string, new_string):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            with open(filepath, 'r') as file:
                content = file.read()
            modified_content = content.replace(old_string, new_string)
            with open(filepath, 'w') as file:
                file.write(modified_content)

def generate_command_file(directory, command_file):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            with open(directory+"wireguard_command", "a") as commandfile:
                commandfile.write("proverif"+" "+filename+" > "+filename+".log"+"\n")


os.chdir(".")
search_and_copy('cannot be proved', ".pv", ".pv.log", ".", "./resolve_global")


replace_string_in_files("./resolve_global", "event eTest( stp1_1, astat_1 );", "")
replace_string_in_files("./resolve_global", "axiom x: bitstring, y: bitstring, z: bitstring; event(eTest(x, y)) && event(eTest(x, z)) ==> y = z.", "")
replace_string_in_files("./resolve_global", "event eTest(bitstring,bitstring).", "")
replace_string_in_files("./resolve_global", "const g:bitstring.", "set preciseActions = true.\nconst g:bitstring.")


generate_command_file("./resolve_global/", "wireguard_command")

