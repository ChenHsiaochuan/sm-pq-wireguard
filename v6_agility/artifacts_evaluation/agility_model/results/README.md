# Auxiliary Agility Model — ProVerif Results

Raw logs for the two-suite cryptographic-agility model. These are the actual
ProVerif outputs, not paraphrases; regenerate with `../run_proverif.sh`.

## Environment

| Item | Value |
|------|-------|
| ProVerif | 2.05 (`Proverif 2.05. Cryptographic protocol verifier`) |
| Host | Linux 6.18.x x86_64 (WSL2) |
| Run date | 2026-06-23T16:03:43+08:00 |
| Runtime (each model) | < 0.02 s wall clock |
| Peak RSS | ≈ 10.5 MiB |

Full fingerprint: [`agility_environment.txt`](agility_environment.txt).

## Scope

The model checks **runtime ephemeral-KEM suite binding only** — that the
one-byte suite selector `f_suite` is authenticated (under PSK-keyed mac1) and
mixed into the KDF transcript, so an active Dolev-Yao attacker cannot downgrade
the selector or splice a ciphertext from one suite into a session negotiated
for another. It does **not** model static-KEM agility (the static slot is the
fixed Classic McEliece identity anchor) and does **not** re-prove the main
key-secrecy / forward-secrecy lemmas (covered by the full ProVerif/Tamarin
development).

## Positive model — `agility_suite_model.pv`

Log: [`agility_suite_model.pv.log`](agility_suite_model.pv.log) (stderr empty).

| Query | Verdict | Meaning |
|-------|---------|---------|
| `event(eRAccept(sidx,s)) ==> event(eISend(sidx,s))` | **TRUE** | The responder only accepts the suite the initiator authenticated (suite agreement). |
| `not event(Bad)` | **TRUE** | No cross-suite / downgrade acceptance; no fallback path reachable. |
| `not attacker(secret_payload)` | **TRUE** | Tunnel payload stays secret under the negotiated suite. |

All three expected positive verdicts hold.

> **Model note.** InitHello and RespHello carry distinct message-type tags
> (`mt1`, `mt2`), mirroring the WireGuard wire format (`message_type` byte
> `0x01` vs `0x02`). This domain separation is load-bearing: without it the two
> handshake messages are structurally identical tuples, and ProVerif correctly
> treats a RespHello MAC as a usable InitHello MAC — which defeats the
> suite-agreement correspondence. The tags model the real protocol's
> per-message-type framing; they are not an added countermeasure.

## Negative regression model — `agility_suite_regression_bad.pv`

Log: [`agility_suite_regression_bad.pv.log`](agility_suite_regression_bad.pv.log) (stderr empty).

This model removes the response-suite binding: the suite byte travels in a
cleartext field **outside** the MAC-covered transcript. Expected and observed:

| Query | Verdict | Meaning |
|-------|---------|---------|
| `event(eRAccept(sidx,s)) ==> event(eISend(sidx,s))` | cannot be proved | Suite agreement breaks once the suite is unauthenticated. |
| `not event(Bad)` | **false → `event(Bad)` REACHABLE** | The attacker flips the cleartext suite byte and the responder accepts a suite the initiator never sent (downgrade / cross-suite confusion). ProVerif reconstructs the attack trace. |
| `not attacker(secret_payload)` | TRUE | Payload confidentiality survives (IND-CCA KEM), but **authentication/agreement is broken** — which is the point of the regression. |

The pair (positive TRUE, negative `Bad` REACHABLE) is what makes the
suite-binding claim falsifiable: the positive verdict is not vacuous, because
deleting the binding demonstrably reintroduces the downgrade.

## Verdict gate

`run_proverif.sh` exits 0 only if the positive model yields 3 TRUE results
**and** the negative model reaches `Bad`. Last run: `OVERALL: PASS`
(see [`run_proverif.stdout.log`](run_proverif.stdout.log)).

## File inventory

- `agility_environment.txt` — date / uname / ProVerif version
- `agility_suite_model.pv.log`, `.err` — positive model raw output
- `agility_suite_regression_bad.pv.log`, `.err` — negative model raw output
- `run_proverif.stdout.log`, `run_proverif.stderr.log` — driver transcript
- `README.md` — this summary
