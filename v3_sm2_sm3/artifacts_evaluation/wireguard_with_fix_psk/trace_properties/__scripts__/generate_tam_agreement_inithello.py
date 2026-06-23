from generate_tam2 import input_filename, variable_mapping_agreement, extract_and_write_expression, generate_tamarin_lemma_body_agreement

lemma_header_agreement_inithello = """lemma Agreement_Inithello:\nall-traces\n\"\nAll #i ldhi ldhr dheki dhekr psk ck.\n(RRec(ck, ldhi, ldhr, dheki, dhekr, psk)@i) & not(Ex #j1. (ISend(ck, ldhi, ldhr, dheki, psk)@j1))\n==> \n\n     (\n"""


def generate_tamarin_lemma_agreement_inithello(expression, variable_mapping_agreement, output_filename):
    lemma_body_agreement_inithello = generate_tamarin_lemma_body_agreement(expression, variable_mapping_agreement)
    with open(output_filename, 'w') as f:
        f.write(lemma_header_agreement_inithello+lemma_body_agreement_inithello)



extract_and_write_expression(input_filename, "agreement_inithello.cnf", "agreement_inithello")


generate_tamarin_lemma_agreement_inithello("agreement_inithello.cnf", variable_mapping_agreement, "agreement_inithello.lemma")