from generate_tam2 import input_filename, variable_mapping_agreement, extract_and_write_expression, generate_tamarin_lemma_body_agreement

lemma_header_agreement_confirm = """lemma Agreement_Confirm:\nall-traces\n\"\nAll #i ldhi ldhr dheki dhekr psk ck.\n(RConfirm(ck, ldhi, ldhr, dheki, dhekr, psk)@i) & not(Ex #j1. (IConfirm(ck, ldhi, ldhr, dheki, dhekr, psk)@j1))\n==> \n\n     (\n"""

def generate_tamarin_lemma_agreement_confirm(expression, variable_mapping_agreement, output_filename):
    lemma_body_agreement_confirm = generate_tamarin_lemma_body_agreement(expression, variable_mapping_agreement)
    with open(output_filename, 'w') as f:
        f.write(lemma_header_agreement_confirm+lemma_body_agreement_confirm)


extract_and_write_expression(input_filename, "agreement_confirm.cnf", "agreement_confirm")


generate_tamarin_lemma_agreement_confirm("agreement_confirm.cnf", variable_mapping_agreement, "agreement_confirm.lemma")