
import re


input_filename = 'results.cnfdnf'  


variable_mapping = {
    "psk": "RevPsk(psk)",
    "sic": "RevLDH(ldhi)",
    "dhsisr": "RevPre(ldhi, ldhr)",
    "erc": "RevDHE(dhekr)",
    "eic": "RevDHE(dheki)",
    "src": "RevLDH(ldhr)",
    "sipq": "RevKEMLtk(kemltki)",
    "eipq": "RevKEMEki(kemeki)",
    "srpq": "RevKEMLtk(kemltkr)",
    "rr": "RevRa(ra)",
    "ri": "RevRb(rb)",
    "re": "RevRe(re)",
}


def extract_and_write_expression(input_filename, output_filename, target_label):
    with open(input_filename, 'r') as f:
        lines = f.readlines()
    
    expression = None
    pattern = rf'DNF for {target_label}: (.*)'
    
    for line in lines:
        match = re.search(pattern, line)
        if match:
            expression = match.group(1).strip()
            break
    
    if expression:
        with open(output_filename, 'w') as f:
            f.write(f'{expression}')
    else:
        print(f"No matching expression found for {target_label}.")


def generate_tamarin_lemma_body(expression_file, variable_mapping):

    with open(expression_file, "r") as file:
        expression = file.read().strip()

    if(expression == "\u2205"):
        lemma_body = []
        lemma_body += "\n\n     )\n\""
        return lemma_body
    else:

        terms = expression.split(" | ")
        tamarin_terms = []

        for term_index, term in enumerate(terms):
            sub_terms = term.replace("(", "").replace(")", "").split(" & ")
            quant_vars = [f"#j{i+1}" for i in range(len(sub_terms))]
            conditions = " & ".join([f"({variable_mapping[t]} @{quant_vars[i]})" for i, t in enumerate(sub_terms)])
            indices = " & ".join([f"({q} < #i)" for q in quant_vars])
            quantifier_stmt = f"Ex {' '.join(quant_vars)}. "
            tamarin_terms.append(f"        ({quantifier_stmt}{conditions} & {indices})")

        lemma_body = " | \n".join(tamarin_terms)
        lemma_body += "\n\n     )\n\""

        return lemma_body
