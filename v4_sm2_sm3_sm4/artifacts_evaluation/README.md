# Symbolic evaluations

This directory gathers symbolic evalutions of WireGuard[^0] (with fix for anonymity based on psk), PQ-WireGuard[^1], PQ-WireGuard^* (see paper, section 4) and Hybrid-WireGuard (see paper, section 5) protocols, with the help of SAPIC+, ProVerif, Tamarin and DeepSec proof assistants. The following properties are verified:
* Trace properties with SAPIC+, ProVerif and Tamarin:
    * Message agreement, including Key Compromise Impersonation resistance
    * Resistance against Unknown Key Share attacks, both unilateral and bilateral
    * Key secrecy, including key Perfect Forward Secreccy, key mutual secrecy
    * Session uniqueness
* Observational equivalence properties with SAPIC+, ProVerif and DeepSec:
    * Anonymity
    * Srong secrecy

All results are currently reproductible on a fresh Ubuntu Server LTS 24.04.2 setup[^2].


## Licence

GNU General Public License v3[^3].

## Content 

This directory containts four folders, *wireguard_with_fix_psk*, *pq_wireguard*, *pq_wireguard_star* and *hybrid_wireguard*, each corresponding to a dedicated protocol. Then each of these directories contains two folders, *trace_properties* concerns the analysis of trace properties (key secreccy, PFS, message agreement, session uniqueness, UUKS/BUKS) with the help of SAPIC+, ProVerif and Tamarin provers, while *equivalence_properties* concerns the analysis of equivalence properties (anonymity, strong secrecy) with the help of SAPIC+, ProVerif and DeepSec provers.


## Prerequisites

This project uses the following:
* Tamarin release version 1.10.0[^4]
* Maude version 3.5[^5]
* ProVerif version 2.05[^6].
* Python version 3.12.3 [^7].
* Package sympy[^8].
* GNU parallel[^9].
* Deepsec version 2.0.2[^10]


To install them, run:
```
sh run_install-dep-tam-pv-deep.sh
``` 

Then folder ```$HOME/.local/bin/``` shall be sourced:

```
echo 'export PATH="$HOME/.local/bin/:$PATH"' >> ~/.bashrc
source ~/.bashrc
```


## References

[^0]: https://www.wireguard.com
[^1]: https://eprint.iacr.org/2020/379.pdf
[^2]: https://ubuntu.com/download/server
[^3]: https://www.gnu.org/licenses/gpl-3.0.html
[^4]: https://tamarin-prover.github.io/
[^5]: https://maude.cs.illinois.edu/wiki/The_Maude_System
[^6]: https://bblanche.gitlabpages.inria.fr/proverif/
[^7]: https://www.python.org/downloads/
[^8]: https://www.sympy.org/en/index.html
[^9]: https://www.gnu.org/software/parallel/
[^10]: https://deepsec-prover.github.io
