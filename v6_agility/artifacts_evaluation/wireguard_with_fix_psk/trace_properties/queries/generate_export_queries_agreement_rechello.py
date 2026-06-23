#!/usr/bin/env python3.6
'''
Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
'''


import itertools


subkeys = ["ldhi", "ldhr", "precompi", "dheki", "dhekr", "psk"]

S1c = list(itertools.combinations(subkeys, 1))
S2c = list(itertools.combinations(subkeys, 2))
S3c = list(itertools.combinations(subkeys, 3))
S4c = list(itertools.combinations(subkeys, 4))
S5c = list(itertools.combinations(subkeys, 5))
S6c = list(itertools.combinations(subkeys, 6))

sets_list = [S1c, S2c, S3c, S4c, S5c, S6c]

with open('wireguard_agreement_rechello_export_queries.spthy', 'w') as f:


	f.write('#ifdef all_trusted'+'\n\n')
	f.write('export queries:'+'\n\n')
	f.write('"'+'\n\n')
	f.write("")
	f.write("noselect x:bitstring; attacker(exp(g,x))."+"\n")

	f.write('query ldhi:bitstring, ldhr:bitstring, dheki:bitstring, dhekr:bitstring, psk:bitstring, ck:bitstring;'+'\n')
	f.write('event(eIKeys(ck, ldhi, ldhr, dheki, dhekr, psk))'+'\n')
	f.write('==> event(eRKeys(ck, ldhi, ldhr, dheki, dhekr, psk)).'+'\n\n')

	for l in sets_list:

		for j in range(0, len(l)):

			query = "query ldhi:bitstring, ldhr:bitstring, dheki:bitstring, dhekr:bitstring, psk:bitstring, ck:bitstring"
			event ='==> event(eRKeys(ck, ldhi, ldhr, dheki, dhekr, psk)) || '
			for i in range(1, len(l[0])+1):
				
				if (l == S1c) or (i == len(l[0])):
					#query +=' j'+str(i)+':time'
					event =event+'event(eRevPri('+l[j][i-2]+'))'
				else:
					#query +=' j'+str(i)+':time, '
					event =event+'event(eRevPri('+l[j][i-2]+')) || '
			f.write(query+';\n')
			f.write('event(eIKeys(ck, ldhi, ldhr, dheki, dhekr, psk))'+'\n')
			f.write(event+'.\n\n')

	f.write('"'+'\n\n')
	f.write('#endif'+'\n\n')



with open('wireguard_agreement_rechello_export_queries.spthy', 'r') as f:
	fdata = f.read()
fdata = fdata.replace('eRevPri(psk', 'eRevPsk(psk')
fdata = fdata.replace('eRevPri(ldhi', 'eRevLDH(ldhi')
fdata = fdata.replace('eRevPri(ldhr', 'eRevLDH(ldhr')
fdata = fdata.replace('eRevPri(dheki', 'eRevDHE(dheki')
fdata = fdata.replace('eRevPri(dhekr', 'eRevDHE(dhekr')
fdata = fdata.replace('eRevPri(precompi', 'eRevPre(ldhi, ldhr)) || event(eRevPre(ldhr, ldhi')

with open('wireguard_agreement_rechello_export_queries.spthy', 'w') as f:
	f.write(fdata)
