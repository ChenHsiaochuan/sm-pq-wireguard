from generate_tam2 import input_filename, variable_mapping_secrecy, extract_and_write_expression, generate_tamarin_lemma_body_secrecy

lemma_header_secrecy_isk7 = """lemma Secrecy_ISK7:\nall-traces\n\"\nAll #i #j ldhi ldhr dheki dhekr psk ck.\n(IConfirm(ck, ldhi, ldhr, dheki, dhekr, psk)@i & K(ck)@j)\n==> \n\n     (\n"""

def generate_tamarin_lemma_secrecy_isk7(expression, variable_mapping_secrecy, output_filename):
    lemma_body_secrecy_isk7 = generate_tamarin_lemma_body_secrecy(expression, variable_mapping_secrecy)
    with open(output_filename, 'w') as f:
        f.write(lemma_header_secrecy_isk7+lemma_body_secrecy_isk7)


extract_and_write_expression(input_filename, "secrecy_isk7.cnf", "secrecy_isk7")


generate_tamarin_lemma_secrecy_isk7("secrecy_isk7.cnf", variable_mapping_secrecy, "secrecy_isk7.lemma")