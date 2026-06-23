#!/usr/bin/env python3.6
'''
Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
'''


import itertools

subkeys = ["kemltki", "kemltkr", "kemeki", "ra", "rb", "re", "psk"]

S1c = list(itertools.combinations(subkeys, 1))
S2c = list(itertools.combinations(subkeys, 2))
S3c = list(itertools.combinations(subkeys, 3))
S4c = list(itertools.combinations(subkeys, 4))
S5c = list(itertools.combinations(subkeys, 5))
S6c = list(itertools.combinations(subkeys, 6))
S7c = list(itertools.combinations(subkeys, 7))

sets_list = [S1c, S2c, S3c, S4c, S5c, S6c, S7c]

with open('wireguard_unilateral_responder_export_queries.spthy', 'w') as f:


	f.write('#ifdef all_trusted'+'\n\n')
	f.write('export queries:'+'\n\n')
	f.write('"'+'\n\n')
	f.write("")
	f.write("")

	f.write("query kemltki:bitstring, kemltkr:bitstring, kemltki':bitstring, kempeki:bitstring, psk:bitstring, ck:bitstring, rb:bitstring, ra:bitstring, re:bitstring;"+'\n')
	f.write("event(eRConfirm(ck, kemltki', kemltkr, kempeki, psk, h(rb), h(ra), h(re))) && event(eHonestK(kemltkr)) && event(eHonestK(kemltki)) && event(eHonestpsk(psk)) && event(eIConfirm(ck, kemltki, kemltkr, kempeki, psk, h(rb), h(ra), h(re)))"+'\n')
	f.write("==> ((kemltki = kemltki'))."+'\n\n')

	for l in sets_list:

		for j in range(0, len(l)):

			query = "query i:time,j:time,z:time, kemltki:bitstring, kemltkr:bitstring, kemltki':bitstring, kempeki:bitstring, psk:bitstring, ck:bitstring, rb:bitstring, ra:bitstring, re:bitstring"
			event ="==> ((kemltki = kemltki')) || "
			for i in range(1, len(l[0])+1):
				
				if (l == S1c) or (i == len(l[0])):
					#query +=' j'+str(i)+':time'
					event =event+'event(eRevPri('+l[j][i-2]+'))'
				else:
					#query +=' j'+str(i)+':time, '
					event =event+'event(eRevPri('+l[j][i-2]+')) || '
			f.write(query+';\n')
			f.write("event(eRConfirm(ck, kemltki', kemltkr, kempeki, psk, h(rb), h(ra), h(re))) && event(eHonestK(kemltkr)) && event(eHonestK(kemltki)) && event(eHonestpsk(psk)) && event(eIConfirm(ck, kemltki, kemltkr, kempeki, psk, h(rb), h(ra), h(re)))"+'\n')
			f.write(event+'.\n\n')

	f.write('"'+'\n\n')
	f.write('#endif'+'\n\n')



with open('wireguard_unilateral_responder_export_queries.spthy', 'r') as f:
	fdata = f.read()
fdata = fdata.replace('eRevPri(psk', 'eRevPsk(psk')
fdata = fdata.replace('eRevPri(kemltki', 'eRevKEMLtk(kemltki')
fdata = fdata.replace('eRevPri(kemltkr', 'eRevKEMLtk(kemltkr')
fdata = fdata.replace('eRevPri(kemeki', 'eRevKEMEki(kempeki')
fdata = fdata.replace('eRevPri(rb', 'eRevRb(rb')
fdata = fdata.replace('eRevPri(ra', 'eRevRa(ra')
fdata = fdata.replace('eRevPri(re', 'eRevRe(re')

with open('wireguard_unilateral_responder_export_queries.spthy', 'w') as f:
	f.write(fdata)