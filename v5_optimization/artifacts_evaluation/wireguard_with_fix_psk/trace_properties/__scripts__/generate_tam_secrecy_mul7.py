from generate_tam2 import input_filename, variable_mapping_secrecy, extract_and_write_expression, generate_tamarin_lemma_body_secrecy

lemma_header_secrecy_mul7 = """lemma Secrecy_mul7:\nall-traces\n\"\nAll #i #j #k ldhi ldhr dheki dhekr psk ck.\n(RConfirm(ck, ldhi, ldhr, dheki, dhekr, psk)@i &\n IConfirm(ck, ldhi, ldhr, dheki, dhekr, psk)@k & K(ck)@j)\n==> \n\n     (\n"""

def generate_tamarin_lemma_secrecy_mul7(expression, variable_mapping_secrecy, output_filename):
    lemma_body_secrecy_mul7 = generate_tamarin_lemma_body_secrecy(expression, variable_mapping_secrecy)
    with open(output_filename, 'w') as f:
        f.write(lemma_header_secrecy_mul7+lemma_body_secrecy_mul7)


extract_and_write_expression(input_filename, "secrecy_mul7.cnf", "secrecy_mul7")


generate_tamarin_lemma_secrecy_mul7("secrecy_mul7.cnf", variable_mapping_secrecy, "secrecy_mul7.lemma")