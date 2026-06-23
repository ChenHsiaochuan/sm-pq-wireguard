#!/usr/bin/env python3.6
'''
Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
'''

from generate_tam2 import input_filename, variable_mapping_secrecy, extract_and_write_expression, generate_tamarin_lemma_body_secrecy

lemma_header_secrecy_mut7 = """lemma Secrecy_mut7:\nall-traces\n\"\nAll #i #j #k kemltki kemltkr ldhi ldhr kempeki dheki dhekr psk rb ra re ck.\n(RConfirm(ck, kemltki, kemltkr, ldhi, ldhr, kempeki, dheki, dhekr, psk, h(rb), h(ra), h(re))@i &\n IConfirm(ck, kemltki, kemltkr, ldhi, ldhr, kempeki, dheki, dhekr, psk, h(rb), h(ra), h(re))@j & K(ck)@k)\n==> \n\n     (\n"""

def generate_tamarin_lemma_secrecy_mut7(expression, variable_mapping_secrecy, output_filename):
    lemma_body_secrecy_mut7 = generate_tamarin_lemma_body_secrecy(expression, variable_mapping_secrecy)
    with open(output_filename, 'w') as f:
        f.write(lemma_header_secrecy_mut7+lemma_body_secrecy_mut7)


extract_and_write_expression(input_filename, "secrecy_mut7.dnf", "secrecy_mut7")


generate_tamarin_lemma_secrecy_mut7("secrecy_mut7.dnf", variable_mapping_secrecy, "secrecy_mut7.lemma")