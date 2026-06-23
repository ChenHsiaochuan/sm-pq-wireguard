#!/usr/bin/env python3.6
'''
Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
'''

from generate_tam2 import input_filename, variable_mapping_agreement, extract_and_write_expression, generate_tamarin_lemma_body_agreement

lemma_header_agreement_confirm = """lemma Agreement_Confirm:\nall-traces\n\"\nAll #i kemltki kemltkr ldhi ldhr kempeki dheki dhekr psk kb ba ke ck.\n(RConfirm(ck, kemltki, kemltkr, ldhi, ldhr, kempeki, dheki, dhekr, psk, h(rb), h(ra), h(re))@i) & not(Ex #j1. (IConfirm(ck, kemltki, kemltkr, ldhi, ldhr, kempeki, dheki, dhekr, psk, h(rb), h(ra), h(re))@j1))\n==> \n\n     (\n"""

def generate_tamarin_lemma_agreement_confirm(expression, variable_mapping_agreement, output_filename):
    lemma_body_agreement_confirm = generate_tamarin_lemma_body_agreement(expression, variable_mapping_agreement)
    with open(output_filename, 'w') as f:
        f.write(lemma_header_agreement_confirm+lemma_body_agreement_confirm)


extract_and_write_expression(input_filename, "agreement_confirm.dnf", "agreement_confirm")


generate_tamarin_lemma_agreement_confirm("agreement_confirm.dnf", variable_mapping_agreement, "agreement_confirm.lemma")