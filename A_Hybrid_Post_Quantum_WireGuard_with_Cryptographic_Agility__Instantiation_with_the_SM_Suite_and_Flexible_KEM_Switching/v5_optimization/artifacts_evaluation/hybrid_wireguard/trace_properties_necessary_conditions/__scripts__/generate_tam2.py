
import re


input_filename = 'results.cnfdnf'  


variable_mapping_agreement = {
    "psk": "(Ex #j{j}. RevPsk(psk)@j{j} & (#j{j} < #i))",
    "dhsisr": ("(Ex #j{j1}. RevPre(ldhi, ldhr) @j{j1} & (#j{j1} < #i)) | "
               "(Ex #j{j2}. RevPre(ldhr, ldhi) @j{j2} & (#j{j2} < #i))"),
    "erc": "(Ex #j{j}. RevDHE(dhekr)@j{j} & (#j{j} < #i))",
    "eic": "(Ex #j{j}. RevDHE(dheki)@j{j} & (#j{j} < #i))",
    "src": "(Ex #j{j}. RevLDH(ldhr)@j{j} & (#j{j} < #i))",
    "sic": "(Ex #j{j}. RevLDH(ldhi)@j{j} & (#j{j} < #i))",
    "sipq": "(Ex #j{j}. RevKEMLtk(kemltki)@j{j} & (#j{j} < #i))",
    "srpq": "(Ex #j{j}. RevKEMLtk(kemltkr)@j{j} & (#j{j} < #i))",
    "eipq": "(Ex #j{j}. RevKEMEki(kemeki)@j{j} & (#j{j} < #i))",
    "rr": "(Ex #j{j}. RevRa(ra)@j{j} & (#j{j} < #i))",
    "ri": "(Ex #j{j}. RevRb(rb)@j{j} & (#j{j} < #i))",
    "re": "(Ex #j{j}. RevRe(re)@j{j} & (#j{j} < #i))"
}


variable_mapping_secrecy = {
    "psk": "(Ex #j{j}. RevPsk(psk)@j{j} & (#j{j} < #j))",
    "dhsisr": ("(Ex #j{j1}. RevPre(ldhi, ldhr) @j{j1} & (#j{j1} < #j)) | "
               "(Ex #j{j2}. RevPre(ldhr, ldhi) @j{j2} & (#j{j2} < #j))"),
    "erc": "(Ex #j{j}. RevDHE(dhekr)@j{j} & (#j{j} < #j))",
    "eic": "(Ex #j{j}. RevDHE(dheki)@j{j} & (#j{j} < #j))",
    "src": "(Ex #j{j}. RevLDH(ldhr)@j{j} & (#j{j} < #j))",
    "sic": "(Ex #j{j}. RevLDH(ldhi)@j{j} & (#j{j} < #j))",
    "sipq": "(Ex #j{j}. RevKEMLtk(kemltki)@j{j} & (#j{j} < #j))",
    "srpq": "(Ex #j{j}. RevKEMLtk(kemltkr)@j{j} & (#j{j} < #j))",
    "eipq": "(Ex #j{j}. RevKEMEki(kempeki)@j{j} & (#j{j} < #j))",
    "rr": "(Ex #j{j}. RevRa(ra)@j{j} & (#j{j} < #j))",
    "ri": "(Ex #j{j}. RevRb(rb)@j{j} & (#j{j} < #j))",
    "re": "(Ex #j{j}. RevRe(re)@j{j} & (#j{j} < #j))"
}



def extract_and_write_expression(input_filename, output_filename, target_label):
    with open(input_filename, 'r') as f:
        lines = f.readlines()
    
    expression = None
    pattern = rf'CNF for {target_label}: (.*)'
    
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


def generate_tamarin_lemma_body_agreement(expression_file, variable_mapping_agreement):

    with open(expression_file, "r") as file:
        expression = file.read().strip()

    if(expression == "\u2205"):
        lemma_body = []
        lemma_body += "\n\n     )\n\""
        return lemma_body
    else:

        terms = re.findall(r'\w+|[&|()]+', expression)
        j_counter = 1
        output_lines = []
        current_line = []


        for term in terms:
            if term in variable_mapping_agreement:
                template = variable_mapping_agreement[term]
                if '{j1}' in template and '{j2}' in template:
                    result = template.format(j1=j_counter, j2=j_counter + 1)
                    j_counter += 2
                else:
                    result = template.format(j=j_counter)
                    j_counter += 1
                current_line.append(result)
            elif term == '&':
                output_lines.append(' '.join(current_line) + ' &')
                current_line = []
            else:
                current_line.append(term)

        # Add final line
        if current_line:
            output_lines.append(' '.join(current_line))

        # Indent all lines (including first)
        final_output = '    ' + '\n    '.join(output_lines)
        final_output += "\n     )\n\""

    return final_output



def generate_tamarin_lemma_body_secrecy(expression_file, variable_mapping_secrecy):

    with open(expression_file, "r") as file:
        expression = file.read().strip()

    if(expression == "\u2205"):
        lemma_body = []
        lemma_body += "\n\n     )\n\""
        return lemma_body
    else:

        terms = re.findall(r'\w+|[&|()]+', expression)
        j_counter = 1
        output_lines = []
        current_line = []


        for term in terms:
            if term in variable_mapping_secrecy:
                template = variable_mapping_secrecy[term]
                if '{j1}' in template and '{j2}' in template:
                    result = template.format(j1=j_counter, j2=j_counter + 1)
                    j_counter += 2
                else:
                    result = template.format(j=j_counter)
                    j_counter += 1
                current_line.append(result)
            elif term == '&':
                output_lines.append(' '.join(current_line) + ' &')
                current_line = []
            else:
                current_line.append(term)

        # Add final line
        if current_line:
            output_lines.append(' '.join(current_line))

        # Indent all lines (including first)
        final_output = '    ' + '\n    '.join(output_lines)
        final_output += "\n     )\n\""

    return final_output
