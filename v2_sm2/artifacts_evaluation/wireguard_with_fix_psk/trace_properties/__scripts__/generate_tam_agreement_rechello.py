from generate_tam2 import input_filename, variable_mapping_agreement, extract_and_write_expression, generate_tamarin_lemma_body_agreement

lemma_header_agreement_rechello = """lemma Agreement_Rechello:\nall-traces\n\"\nAll #i ldhi ldhr dheki dhekr psk ck.\n(IKeys(ck, ldhi, ldhr, dheki, dhekr, psk)@i) & not(Ex #j1. (RKeys(ck, ldhi, ldhr, dheki, dhekr, psk)@j1))\n==> \n\n     (\n"""

def generate_tamarin_lemma_agreement_rechello(expression, variable_mapping_agreement, output_filename):
    lemma_body_agreement_rechello = generate_tamarin_lemma_body_agreement(expression, variable_mapping_agreement)
    with open(output_filename, 'w') as f:
        f.write(lemma_header_agreement_rechello+lemma_body_agreement_rechello)


extract_and_write_expression(input_filename, "agreement_rechello.cnf", "agreement_rechello")


generate_tamarin_lemma_agreement_rechello("agreement_rechello.cnf", variable_mapping_agreement, "agreement_rechello.lemma")