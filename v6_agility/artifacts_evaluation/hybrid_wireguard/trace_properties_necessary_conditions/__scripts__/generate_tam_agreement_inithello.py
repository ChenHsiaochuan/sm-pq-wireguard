#!/usr/bin/env python3.6
'''
Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
'''

from generate_tam2 import input_filename, variable_mapping_agreement, extract_and_write_expression, generate_tamarin_lemma_body_agreement

lemma_header_agreement_inithello = """lemma Agreement_Inithello:\nall-traces\n\"\nAll #i kemltki kemltkr ldhi ldhr kempeki dheki dhekr psk rb ra re ck.\n(RRec(ck, kemltki, kemltkr, ldhi, ldhr, kempeki, dheki, dhekr, psk, h(rb), h(ra), h(re))@i) & not(Ex #j1. (ISend(ck, kemltki, kemltkr, ldhi, ldhr, kempeki, dheki, psk, h(rb))@j1))\n==> \n\n     (\n"""

def generate_tamarin_lemma_agreement_inithello(expression, variable_mapping_agreement, output_filename):
    lemma_body_agreement_inithello = generate_tamarin_lemma_body_agreement(expression, variable_mapping_agreement)
    with open(output_filename, 'w') as f:
        f.write(lemma_header_agreement_inithello+lemma_body_agreement_inithello)



extract_and_write_expression(input_filename, "agreement_inithello.dnf", "agreement_inithello")


generate_tamarin_lemma_agreement_inithello("agreement_inithello.dnf", variable_mapping_agreement, "agreement_inithello.lemma")