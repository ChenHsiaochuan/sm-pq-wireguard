#!/usr/bin/env python3.6
'''
Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
'''

from generate_tam2 import input_filename, variable_mapping_secrecy, extract_and_write_expression, generate_tamarin_lemma_body_secrecy

lemma_header_secrecy_isk7pfs = """lemma Secrecy_ISK7PFS:\nall-traces\n\"\nAll #i #j kemltki kemltkr ldhi ldhr kempeki dheki dhekr psk rb ra re ck.\n(IConfirm(ck, kemltki, kemltkr, ldhi, ldhr, kempeki, dheki, dhekr, psk, h(rb), h(ra), h(re))@i & K(ck)@j & not(Ex #j1. RevPsk(psk)@j1 & (#j1 < #i)) & not(Ex #j2. RevLDH(ldhr)@j2 & (#j2 < #i)) &
 not(Ex #j2. RevLDH(ldhi)@j2 & (#j2 < #i)) & not(Ex #j3. RevPre(ldhr, ldhi) @j3 & (#j3 < #i)) & not(Ex #j3. RevPre(ldhi, ldhr) @j3 & (#j3 < #i)) & not(Ex #j4. RevKEMLtk(kemltki)@j4 & (#j4 < #i)) &
 not(Ex #j4. RevKEMLtk(kemltkr)@j4 & (#j4 < #i))  )\n==> \n\n     (\n"""

def generate_tamarin_lemma_secrecy_isk7pfs(expression, variable_mapping_secrecy, output_filename):
    lemma_body_secrecy_isk7pfs = generate_tamarin_lemma_body_secrecy(expression, variable_mapping_secrecy)
    with open(output_filename, 'w') as f:
        f.write(lemma_header_secrecy_isk7pfs+lemma_body_secrecy_isk7pfs)


extract_and_write_expression(input_filename, "secrecy_isk7pfs.dnf", "secrecy_isk7pfs")


generate_tamarin_lemma_secrecy_isk7pfs("secrecy_isk7pfs.dnf", variable_mapping_secrecy, "secrecy_isk7pfs.lemma")