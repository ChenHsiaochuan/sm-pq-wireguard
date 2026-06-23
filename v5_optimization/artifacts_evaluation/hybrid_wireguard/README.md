# Symbolic evaluation of Hybrid-WireGuard

## Trace properties evaluation - necessary conditions

In folder *trace_properties_necessary_conditions*, run:
```
sh run_clean.sh
sh run_generate-pv.sh
sh run_evaluate-pv.sh
sh run_generate-spthy-m.sh
sh run_evaluate-pv-m.sh
sh run_generate-cnf-dnf.sh
``` 

This will generate all ProVerif files for adversary with 'read' access to cryptographic keys, evaluate these files, generate the necessary ProVerif files to account for adversary with 'write' access to cryptographic keys, evaluate these files, compute CNF and DNF for each evaluated property, generate Tamarin files from computed DNF. 


To run all previous scripts in a single commmand, simply run:
```
sh run_all.sh
``` 

Evaluation of ProVerif files is adaptive (see paper, Section 4.1)

Algorithms that implement adaptive analyses are Python scripts, included in *__script__* folder.

Once evaluation is finished, each folder contains a file named *results.cnfdnf*, which contains all computed CNF and DNF, for each property.

*results.cnfdnf* shall contain:
```
DNF for unilateral_responder: ∅
CNF for unilateral_responder: ∅
DNF for unilateral_initiator: ∅
CNF for unilateral_initiator: ∅
DNF for bilateral: ∅
CNF for bilateral: ∅
DNF for uniqueness_initiator: ∅
CNF for uniqueness_initiator: ∅
DNF for uniqueness_responder: ∅
CNF for uniqueness_responder: ∅
DNF for secrecy_isk7: (srpq & psk & src) | (ri & psk & src) | (srpq & dhsisr & psk & eic) | (srpq & psk & sic & eic) | (ri & dhsisr & psk & eic) | (ri & psk & sic & eic)
CNF for secrecy_isk7: psk & (srpq | ri) & (src | eic) & (dhsisr | sic | src)
DNF for agreement_inithello: (dhsisr & psk) | (psk & sic) | (psk & src)
CNF for agreement_inithello: psk & (dhsisr | sic | src)
DNF for secrecy_rsk7: (sipq & psk & sic) | (rr & psk & sic) | (sipq & dhsisr & psk & erc) | (sipq & psk & src & erc) | (rr & dhsisr & psk & erc) | (rr & psk & src & erc)
CNF for secrecy_rsk7: psk & (sipq | rr) & (sic | erc) & (dhsisr | sic | src)
DNF for agreement_rechello: (srpq & psk & src) | (ri & psk & src) | (srpq & dhsisr & psk & eic) | (srpq & psk & sic & eic) | (ri & dhsisr & psk & eic) | (ri & psk & sic & eic)
CNF for agreement_rechello: psk & (srpq | ri) & (src | eic) & (dhsisr | sic | src)
DNF for agreement_confirm: (sipq & psk & sic) | (rr & psk & sic) | (sipq & dhsisr & psk & erc) | (sipq & psk & src & erc) | (rr & dhsisr & psk & erc) | (rr & psk & src & erc)
CNF for agreement_confirm: psk & (sipq | rr) & (sic | erc) & (dhsisr | sic | src)
DNF for secrecy_mut7: (sipq & srpq & eipq & psk & sic & eic) | (sipq & srpq & eipq & psk & src & erc) | (sipq & srpq & re & psk & sic & eic) | (sipq & srpq & re & psk & src & erc) | (sipq & eipq & ri & psk & sic & eic) | (sipq & eipq & ri & psk & src & erc) | (sipq & ri & re & psk & sic & eic) | (sipq & ri & re & psk & src & erc) | (srpq & eipq & rr & psk & sic & eic) | (srpq & eipq & rr & psk & src & erc) | (srpq & rr & re & psk & sic & eic) | (srpq & rr & re & psk & src & erc) | (eipq & rr & ri & psk & sic & eic) | (eipq & rr & ri & psk & src & erc) | (rr & ri & re & psk & sic & eic) | (rr & ri & re & psk & src & erc) | (sipq & srpq & eipq & dhsisr & psk & eic & erc) | (sipq & srpq & dhsisr & re & psk & eic & erc) | (sipq & eipq & ri & dhsisr & psk & eic & erc) | (sipq & ri & dhsisr & re & psk & eic & erc) | (srpq & eipq & rr & dhsisr & psk & eic & erc) | (srpq & rr & dhsisr & re & psk & eic & erc) | (eipq & rr & ri & dhsisr & psk & eic & erc) | (rr & ri & dhsisr & re & psk & eic & erc)
CNF for secrecy_mut7: psk & (sipq | rr) & (srpq | ri) & (eipq | re) & (sic | erc) & (src | eic) & (eic | erc) & (dhsisr | sic | src)
DNF for secrecy_isk7pfs: (sipq & srpq & eipq & psk & sic & eic) | (sipq & srpq & eipq & psk & src & erc) | (sipq & srpq & re & psk & sic & eic) | (sipq & srpq & re & psk & src & erc) | (sipq & eipq & ri & psk & sic & eic) | (sipq & eipq & ri & psk & src & erc) | (sipq & ri & re & psk & sic & eic) | (sipq & ri & re & psk & src & erc) | (srpq & eipq & rr & psk & sic & eic) | (srpq & eipq & rr & psk & src & erc) | (srpq & rr & re & psk & sic & eic) | (srpq & rr & re & psk & src & erc) | (eipq & rr & ri & psk & sic & eic) | (eipq & rr & ri & psk & src & erc) | (rr & ri & re & psk & sic & eic) | (rr & ri & re & psk & src & erc) | (sipq & srpq & eipq & dhsisr & psk & eic & erc) | (sipq & srpq & dhsisr & re & psk & eic & erc) | (sipq & eipq & ri & dhsisr & psk & eic & erc) | (sipq & ri & dhsisr & re & psk & eic & erc) | (srpq & eipq & rr & dhsisr & psk & eic & erc) | (srpq & rr & dhsisr & re & psk & eic & erc) | (eipq & rr & ri & dhsisr & psk & eic & erc) | (rr & ri & dhsisr & re & psk & eic & erc)
CNF for secrecy_isk7pfs: psk & (sipq | rr) & (srpq | ri) & (eipq | re) & (sic | erc) & (src | eic) & (eic | erc) & (dhsisr | sic | src)
DNF for secrecy_rsk7pfs: (sipq & srpq & eipq & psk & sic & eic) | (sipq & srpq & eipq & psk & src & erc) | (sipq & srpq & re & psk & sic & eic) | (sipq & srpq & re & psk & src & erc) | (sipq & eipq & ri & psk & sic & eic) | (sipq & eipq & ri & psk & src & erc) | (sipq & ri & re & psk & sic & eic) | (sipq & ri & re & psk & src & erc) | (srpq & eipq & rr & psk & sic & eic) | (srpq & eipq & rr & psk & src & erc) | (srpq & rr & re & psk & sic & eic) | (srpq & rr & re & psk & src & erc) | (eipq & rr & ri & psk & sic & eic) | (eipq & rr & ri & psk & src & erc) | (rr & ri & re & psk & sic & eic) | (rr & ri & re & psk & src & erc) | (sipq & srpq & eipq & dhsisr & psk & eic & erc) | (sipq & srpq & dhsisr & re & psk & eic & erc) | (sipq & eipq & ri & dhsisr & psk & eic & erc) | (sipq & ri & dhsisr & re & psk & eic & erc) | (srpq & eipq & rr & dhsisr & psk & eic & erc) | (srpq & rr & dhsisr & re & psk & eic & erc) | (eipq & rr & ri & dhsisr & psk & eic & erc) | (rr & ri & dhsisr & re & psk & eic & erc)
CNF for secrecy_rsk7pfs: psk & (sipq | rr) & (srpq | ri) & (eipq | re) & (sic | erc) & (src | eic) & (eic | erc) & (dhsisr | sic | src)
DNF for secrecy_mut7pfs: (sipq & srpq & eipq & psk & sic & eic) | (sipq & srpq & eipq & psk & src & erc) | (sipq & srpq & re & psk & sic & eic) | (sipq & srpq & re & psk & src & erc) | (sipq & eipq & ri & psk & sic & eic) | (sipq & eipq & ri & psk & src & erc) | (sipq & ri & re & psk & sic & eic) | (sipq & ri & re & psk & src & erc) | (srpq & eipq & rr & psk & sic & eic) | (srpq & eipq & rr & psk & src & erc) | (srpq & rr & re & psk & sic & eic) | (srpq & rr & re & psk & src & erc) | (eipq & rr & ri & psk & sic & eic) | (eipq & rr & ri & psk & src & erc) | (rr & ri & re & psk & sic & eic) | (rr & ri & re & psk & src & erc) | (sipq & srpq & eipq & dhsisr & psk & eic & erc) | (sipq & srpq & dhsisr & re & psk & eic & erc) | (sipq & eipq & ri & dhsisr & psk & eic & erc) | (sipq & ri & dhsisr & re & psk & eic & erc) | (srpq & eipq & rr & dhsisr & psk & eic & erc) | (srpq & rr & dhsisr & re & psk & eic & erc) | (eipq & rr & ri & dhsisr & psk & eic & erc) | (rr & ri & dhsisr & re & psk & eic & erc)
CNF for secrecy_mut7pfs: psk & (sipq | rr) & (srpq | ri) & (eipq | re) & (sic | erc) & (src | eic) & (eic | erc) & (dhsisr | sic | src)

```

## Trace properties evaluation - sufficient conditions

In folder *trace_properties_sufficient_conditions*, run:

```
sh run_clean.sh
sh run_evaluate-pv.sh
sh run_evaluate-tam.sh
``` 

This will evaluate all ProVerif and Tamarin files. 

To run all previous scripts in a single commmand, simply run, in each folder:
```
sh run_all.sh
``` 

## Observational equivalence properties evaluation

In folder *equivalence_properties*, run:

```
sh run_clean.sh
cd Anonymity
sh run_evaluate-pv.sh
cd ../Strong-Secrecy
sh run_evaluate-pv.sh
cd ..
``` 

This will evaluate all ProVerif files for anonymity and strong secrecy properties.

To run all previous scripts in a single commmand, simply run:
```
sh run_all.sh
``` 
