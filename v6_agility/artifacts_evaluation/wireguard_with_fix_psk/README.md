# Symbolic evaluation of WireGuard with fix PSK

## Trace properties evaluation

In folder *trace_properties*, run:

```
sh run_clean.sh
sh run_generate-pv.sh
sh run_evaluate-pv.sh
sh run_generate-spthy-m.sh
sh run_evaluate-pv-m.sh
sh run_generate-cnf-dnf.sh
sh run_generate-tam.sh
sh run_evaluate-tam.sh
``` 
This will generate all ProVerif files for adversary with 'read' access to cryptographic keys, evaluate these files, generate the necessary ProVerif files to account for adversary with 'write' access to cryptographic keys, evaluate these files, compute CNF and DNF for each evaluated property, generate Tamarin files from computed DNF and finally evaluate Tamarin files. 


To run all previous scripts in a single commmand, simply run:
```
sh run_all.sh
``` 

Evaluation of ProVerif files is adaptive (see paper, Section 4.1)

Algorithms that implement adaptive analyses are Python scripts, included in *__script__* folder.

Once evaluation is finished, each folder contains a file named *results.cnfdnf*, which contains all computed CNF and DNF, for each property.

*results.cnfdnf* shall contain:

```
DNF for bilateral: ∅
CNF for bilateral: ∅
DNF for unilateral_initiator: ∅
CNF for unilateral_initiator: ∅
DNF for unilateral_responder: ∅
CNF for unilateral_responder: ∅
DNF for uniqueness_initiator: ∅
CNF for uniqueness_initiator: ∅
DNF for uniqueness_responder: ∅
CNF for uniqueness_responder: ∅
DNF for agreement_inithello: (dhsisr & psk) | (psk & sic) | (psk & src)
CNF for agreement_inithello: psk & (dhsisr | sic | src)
DNF for agreement_rechello: (psk & src) | (dhsisr & psk & eic) | (psk & sic & eic)
CNF for agreement_rechello: psk & (src | eic) & (dhsisr | sic | src)
DNF for agreement_confirm: (psk & sic) | (dhsisr & psk & erc) | (psk & src & erc)
CNF for agreement_confirm: psk & (sic | erc) & (dhsisr | sic | src)
DNF for secrecy_isk7: (psk & src) | (dhsisr & psk & eic) | (psk & sic & eic)
CNF for secrecy_isk7: psk & (src | eic) & (dhsisr | sic | src)
DNF for secrecy_rsk7: (psk & sic) | (dhsisr & psk & erc) | (psk & src & erc)
CNF for secrecy_rsk7: psk & (sic | erc) & (dhsisr | sic | src)
DNF for secrecy_mul7: (psk & sic & eic) | (psk & src & erc) | (dhsisr & psk & eic & erc)
CNF for secrecy_mul7: psk & (sic | erc) & (src | eic) & (eic | erc) & (dhsisr | sic | src)
DNF for secrecy_isk7pfs: (psk & sic & eic) | (psk & src & erc) | (dhsisr & psk & eic & erc)
CNF for secrecy_isk7pfs: psk & (sic | erc) & (src | eic) & (eic | erc) & (dhsisr | sic | src)
DNF for secrecy_rsk7pfs: (psk & sic & eic) | (psk & src & erc) | (dhsisr & psk & eic & erc)
CNF for secrecy_rsk7pfs: psk & (sic | erc) & (src | eic) & (eic | erc) & (dhsisr | sic | src)
DNF for secrecy_mul7pfs: (psk & sic & eic) | (psk & src & erc) | (dhsisr & psk & eic & erc)
CNF for secrecy_mul7pfs: psk & (sic | erc) & (src | eic) & (eic | erc) & (dhsisr | sic | src)
```

## Observational equivalence properties evaluation

In folder *equivalence_properties*, run:

```
sh run_clean.sh
cd Anonymity
sh run_all.sh
cd ../Strong-Secrecy
sh run_all.sh
cd ..
``` 

This will evaluate all ProVerif files for anonymity and strong secrecy properties.

To run all previous scripts in a single commmand, simply run:
```
sh run_all.sh
``` 
