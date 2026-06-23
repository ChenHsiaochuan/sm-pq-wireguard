#!/usr/bin/env python3.6
'''
Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
'''

from generate_tam2 import input_filename, variable_mapping_agreement, extract_and_write_expression, generate_tamarin_lemma_body_agreement

lemma_header_agreement_rechello = """lemma Agreement_Rechello:\nall-traces\n\"\nAll #i kemltki kemltkr ldhi ldhr kempeki dheki dhekr psk rb ra re ck.\n(IKeys(ck, kemltki, kemltkr, ldhi, ldhr, kempeki, dheki, dhekr, psk, h(rb), h(ra), h(re))@i) & not(Ex #j1. (RKeys(ck, kemltki, kemltkr, ldhi, ldhr, kempeki, dheki, dhekr, psk, h(rb), h(ra), h(re))@j1))\n==> \n\n     (\n"""

def generate_tamarin_lemma_agreement_rechello(expression, variable_mapping_agreement, output_filename):
    lemma_body_agreement_rechello = generate_tamarin_lemma_body_agreement(expression, variable_mapping_agreement)
    with open(output_filename, 'w') as f:
        f.write(lemma_header_agreement_rechello+lemma_body_agreement_rechello)


extract_and_write_expression(input_filename, "agreement_rechello.dnf", "agreement_rechello")


generate_tamarin_lemma_agreement_rechello("agreement_rechello.dnf", variable_mapping_agreement, "agreement_rechello.lemma")