from generate_tam2 import input_filename, variable_mapping_secrecy, extract_and_write_expression, generate_tamarin_lemma_body_secrecy

lemma_header_secrecy_rsk7pfs = """lemma Secrecy_RSK7PFS:\nall-traces\n\"\nAll #i #j ldhi ldhr dheki dhekr psk ck.\n(RConfirm(ck, ldhi, ldhr, dheki, dhekr, psk)@i & K(ck)@j & not(Ex #j1. RevPsk(psk)@j1 & (#j1 < #i)) & not(Ex #j2. RevLDH(ldhr)@j2 & (#j2 < #i)) &
 not(Ex #j2. RevLDH(ldhi)@j2 & (#j2 < #i)) & not(Ex #j1. RevPre(ldhr, ldhi) @j1 & (#j1 < #i)) & not(Ex #j1. RevPre(ldhi, ldhr) @j1 & (#j1 < #i)))\n==> \n\n     (\n"""

def generate_tamarin_lemma_secrecy_rsk7pfs(expression, variable_mapping_secrecy, output_filename):
    lemma_body_secrecy_rsk7pfs = generate_tamarin_lemma_body_secrecy(expression, variable_mapping_secrecy)
    with open(output_filename, 'w') as f:
        f.write(lemma_header_secrecy_rsk7pfs+lemma_body_secrecy_rsk7pfs)


extract_and_write_expression(input_filename, "secrecy_rsk7pfs.cnf", "secrecy_rsk7pfs")


generate_tamarin_lemma_secrecy_rsk7pfs("secrecy_rsk7pfs.cnf", variable_mapping_secrecy, "secrecy_rsk7pfs.lemma")