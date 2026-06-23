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
                os.remove(ext2_file)

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


#def update_pv_file(ext):


os.chdir(".")
search_and_copy('cannot be proved', ".pv", ".pv.log", ".", "./resolve_simple")
"""
search_and_copy('cannot be proved', ".pv", ".pv.1log", ".", "./resolve_simple")
search_and_copy('cannot be proved', ".pv", ".pv.2log", ".", "./resolve_simple")
search_and_copy('cannot be proved', ".pv", ".pv.3log", ".", "./resolve_simple")
search_and_copy('cannot be proved', ".pv", ".pv.4log", ".", "./resolve_simple")
search_and_copy('cannot be proved', ".pv", ".pv.5log", ".", "./resolve_simple")
search_and_copy('cannot be proved', ".pv", ".pv.6log", ".", "./resolve_simple")
search_and_copy('cannot be proved', ".pv", ".pv.7log", ".", "./resolve_simple")
search_and_copy('cannot be proved', ".pv", ".pv.8log", ".", "./resolve_simple")
search_and_copy('cannot be proved', ".pv", ".pv.9log", ".", "./resolve_simple")
search_and_copy('cannot be proved', ".pv", ".pv.10log", ".", "./resolve_simple")
search_and_copy('cannot be proved', ".pv", ".pv.11log", ".", "./resolve_simple")
search_and_copy('cannot be proved', ".pv", ".pv.12log", ".", "./resolve_simple")
search_and_copy('cannot be proved', ".pv", ".pv.13log", ".", "./resolve_simple")
search_and_copy('cannot be proved', ".pv", ".pv.14log", ".", "./resolve_simple")
"""

replace_string_in_files("./resolve_simple", "in(att,(=sxI, (sidI_1:bitstring, (dhpekI_1:bitstring, (kempekI_1:bitstring, (ct1_1:bitstring, (astat_1:bitstring, (ats_1:bitstring, macI1_1:bitstring))))))));", "in(att,(=sxI, (sidI_1:bitstring, (dhpekI_1:bitstring, (kempekI_1:bitstring, (ct1_1:bitstring, (astat_1:bitstring, (ats_1:bitstring, macI1_1:bitstring))))))));\n\t\t\tnew stp1_1[]:bitstring;\n\t\t\tevent eTest( stp1_1, astat_1 );\n\n")
replace_string_in_files("./resolve_simple", "noselect x:bitstring; attacker(exp(g,x)).", "noselect x:bitstring; attacker(exp(g,x)).\naxiom x: bitstring, y: bitstring, z: bitstring; event(eTest(x, y)) && event(eTest(x, z)) ==> y = z.\n\n")
replace_string_in_files("./resolve_simple", "event eRevRe(bitstring).", "event eRevRe(bitstring).\nevent eTest(bitstring,bitstring).\n\n")


generate_command_file("./resolve_simple/", "wireguard_command")

