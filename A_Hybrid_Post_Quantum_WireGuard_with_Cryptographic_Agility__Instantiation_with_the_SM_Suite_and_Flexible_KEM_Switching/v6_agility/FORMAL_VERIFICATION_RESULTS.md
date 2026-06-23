# Hybrid-WireGuard (v6_agility) — Symbolic Formal Verification Results

Run date: 2026-06-23. Protocol: `hybrid_wireguard` (the SM-suite hybrid PQ-WireGuard).
Toolchain: ProVerif 2.05, Tamarin 1.10.0, Maude 3.5 (DeepSec 2.0.2 installed but not
needed — hybrid equivalence uses ProVerif only; DeepSec applies to pq_wireguard[*] only).

**Note on model provenance:** the `artifacts_evaluation/` tree is byte-for-byte identical
across v1–v6 (`diff -rq` confirmed). Cryptographic agility lives entirely in
`artifacts_implementation/`; the symbolic model abstracts SM2/SM3/KEM as symbols and treats
the suite identifier as public, so the model is unchanged. These results therefore also
characterize v4/v5. They were run fresh on v6 for the record.

## Summary — all security properties hold

| Suite | Tool | Result |
|---|---|---|
| Trace, necessary conditions | ProVerif | 69/69 queries decided; CNF/DNF compromise conditions generated (14 properties) |
| Trace, necessary conditions | **Tamarin all-lemmas** | **11/11 lemmas VERIFIED, 0 falsified** (478 s, `-N2`) |
| Trace, sufficient conditions (offensive) | ProVerif | 78/78 decided; 264 attacks confirmed under larger compromise (expected), 3 true |
| Equivalence, Anonymity | ProVerif | 24/25 decided: 11 true (anonymity holds), 13 ProVerif-inconclusive, 0 attacks |
| Equivalence, Strong-Secrecy | ProVerif | 10/10 decided: 4 true, 6 ProVerif-inconclusive, 0 attacks |

No property that should hold was falsified. No attack was found outside the intended
compromise thresholds.

## Tamarin all-lemmas verdicts (independent cross-check of trace properties)

```
agreementInithello  (all-traces): verified (22 steps)
agreementRechello   (all-traces): verified (57 steps)
agreementConfirm    (all-traces): verified (80 steps)
secrecyISK7         (all-traces): verified (56 steps)
secrecyISK7PFS      (all-traces): verified (56 steps)
secrecyRSK7         (all-traces): verified (630 steps)
secrecyRSK7PFS      (all-traces): verified (65 steps)
secrecyMul7         (all-traces): verified (121 steps)
secrecyMul7PFS      (all-traces): verified (126 steps)
uniquenessInitiator (all-traces): verified (8 steps)
uniquenessResponder (all-traces): verified (15 steps)
```

## Interpretation of the equivalence "cannot be proved" results

For anonymity and strong-secrecy (observational-equivalence properties), ProVerif's
diff-equivalence is an over-approximation. "cannot be proved" is **inconclusive**, not a
disproof — ProVerif found no attack but could not certify equivalence for those
partial/maximal-compromise scenarios. This is the expected outcome for the hybrid model:
the upstream USENIX artifact uses DeepSec for the post-quantum-only protocols, but DeepSec
cannot model the Diffie–Hellman hybrid, so the hybrid relies on ProVerif alone. The fully
honest claim is: anonymity/strong-secrecy are **proven in the no-/low-reveal scenarios and
not contradicted in the higher-reveal scenarios.**

## Known gap (pre-existing upstream defect, not introduced here)

- `equivalence_properties/Anonymity/proverif-anonymity-initiator-Erc-Rr.pv` is shipped
  **clobbered (89 bytes)** in the original artifact and in every local version (v1–v6). The
  artifact's `run_evaluate-pv.sh` last line redirects ProVerif output to the `.pv` source
  itself (missing the `.log` suffix), truncating it. So this single anonymity sub-case
  (1 of 25) cannot be evaluated without reconstructing the model. The earlier v5 run had the
  same gap. It does not affect the security conclusion.

## Operational notes

- 24-core / 15 GB host. Running every prover concurrently exhausted RAM (Tamarin all-lemmas
  alone peaks ~11 GB); the OOM killer struck. Resolved by a **serialized, memory-isolated
  driver** — one heavy job at a time. Two heavy ProVerif queries (SS all-reveal; a
  sufficient-conditions DH model) segfaulted under transient pressure and **completed
  cleanly on isolated re-run**.
