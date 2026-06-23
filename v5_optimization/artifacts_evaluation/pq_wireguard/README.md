# Symbolic evaluation of PQ-WireGuard

## Trace properties evaluation

In folder *trace_properties*, run:
```
sh run_clean.sh
sh run_generate-pv.sh
sh run_evaluate-pv.sh
sh run_generate-spthy-m.sh
sh run_evaluate-pv-m.sh
sh run_generate-cnf-dnf.sh
``` 
This will generate all ProVerif files for adversary with 'read' access to cryptographic keys, evaluate these files, generate the necessary ProVerif files to account for adversary with 'write' access to cryptographic keys, evaluate these files, compute CNF and DNF for each evaluated property. Note: we don't evaluate Tamarin files in these cases as models do not rely on *diffie-hellman* builtin.

To run all previous scripts in a single commmand, simply run:
```
sh run_all.sh
``` 

Evaluation of ProVerif files is adaptive (see paper, Section 4.1)

Algorithms that implement adaptive analyses are Python scripts, included in *__script__* folder.

Once evaluation is finished, each folder contains a file named *results.cnfdnf*, which contains all computed CNF and DNF, for each property.

*results.cnfdnf* shall contain:
```
DNF for uniqueness_initiator: ∅
CNF for uniqueness_initiator: ∅
DNF for bilateral: eipq | re
CNF for bilateral: eipq | re
DNF for uniqueness_responder: ∅
CNF for uniqueness_responder: ∅
DNF for unilateral_initiator: (sipq & eipq & psk) | (sipq & re & psk) | (eipq & rr & psk & sigr) | (rr & re & psk & sigr)
CNF for unilateral_initiator: psk & (sipq | rr) & (sipq | sigr) & (eipq | re)
DNF for secrecy_isk7: (srpq & psk) | (ri & psk & sigi)
CNF for secrecy_isk7: psk & (srpq | ri) & (srpq | sigi)
DNF for unilateral_responder: (srpq & eipq & psk) | (srpq & re & psk) | (eipq & ri & psk & sigi) | (ri & re & psk & sigi)
CNF for unilateral_responder: psk & (srpq | ri) & (srpq | sigi) & (eipq | re)
DNF for agreement_inithello: psk
CNF for agreement_inithello: psk
DNF for secrecy_rsk7: (sipq & psk) | (rr & psk & sigr)
CNF for secrecy_rsk7: psk & (sipq | rr) & (sipq | sigr)
DNF for agreement_rechello: (srpq & psk) | (ri & psk & sigi)
CNF for agreement_rechello: psk & (srpq | ri) & (srpq | sigi)
DNF for agreement_confirm: (sipq & psk) | (rr & psk & sigr)
CNF for agreement_confirm: psk & (sipq | rr) & (sipq | sigr)
DNF for secrecy_isk7pfs: (sipq & srpq & eipq & psk) | (sipq & srpq & re & psk) | (sipq & eipq & ri & psk & sigi) | (sipq & ri & re & psk & sigi) | (srpq & eipq & rr & psk & sigr) | (srpq & rr & re & psk & sigr) | (eipq & rr & ri & psk & sigi & sigr) | (rr & ri & re & psk & sigi & sigr)
CNF for secrecy_isk7pfs: psk & (sipq | rr) & (sipq | sigr) & (srpq | ri) & (srpq | sigi) & (eipq | re)
DNF for secrecy_mut7: (sipq & srpq & eipq & psk) | (sipq & srpq & re & psk) | (sipq & eipq & ri & psk & sigi) | (sipq & ri & re & psk & sigi) | (srpq & eipq & rr & psk & sigr) | (srpq & rr & re & psk & sigr) | (eipq & rr & ri & psk & sigi & sigr) | (rr & ri & re & psk & sigi & sigr)
CNF for secrecy_mut7: psk & (sipq | rr) & (sipq | sigr) & (srpq | ri) & (srpq | sigi) & (eipq | re)
DNF for secrecy_rsk7pfs: (sipq & srpq & eipq & psk) | (sipq & srpq & re & psk) | (sipq & eipq & ri & psk & sigi) | (sipq & ri & re & psk & sigi) | (srpq & eipq & rr & psk & sigr) | (srpq & rr & re & psk & sigr) | (eipq & rr & ri & psk & sigi & sigr) | (rr & ri & re & psk & sigi & sigr)
CNF for secrecy_rsk7pfs: psk & (sipq | rr) & (sipq | sigr) & (srpq | ri) & (srpq | sigi) & (eipq | re)
DNF for secrecy_mut7pfs: (sipq & srpq & eipq & psk) | (sipq & srpq & re & psk) | (sipq & eipq & ri & psk & sigi) | (sipq & ri & re & psk & sigi) | (srpq & eipq & rr & psk & sigr) | (srpq & rr & re & psk & sigr) | (eipq & rr & ri & psk & sigi & sigr) | (rr & ri & re & psk & sigi & sigr)
CNF for secrecy_mut7pfs: psk & (sipq | rr) & (sipq | sigr) & (srpq | ri) & (srpq | sigi) & (eipq | re)
```

## Observational equivalence properties evaluation

In folder *equivalence_properties*, run:

```
sh run_clean.sh
cd Anonymity
sh run_evaluate-pv.sh
sh run_evaluate-dps.sh
cd ../Strong-Secrecy
sh run_evaluate-pv.sh
sh run_evaluate-dps.sh
cd ..
``` 

This will evaluate all ProVerif and DeepSec files for anonymity and strong secrecy properties.

To run all previous scripts in a single commmand, simply run:
```
sh run_all.sh
``` 
