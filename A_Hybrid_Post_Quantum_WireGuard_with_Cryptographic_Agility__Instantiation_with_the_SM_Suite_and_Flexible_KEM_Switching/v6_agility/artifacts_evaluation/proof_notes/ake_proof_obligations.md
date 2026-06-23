# AKE Proof Obligations for SM-PQ-WireGuard v6

This note makes the security theorem (Theorem 1 in Section 4.2 / Appendix A)
reviewer-auditable by defining every term in the real-or-random (RoR) AKE
experiment precisely. It is a companion to the paper, not a replacement for
it; all equation and section references point to the paper.

---

## 1. Protocol participants

A **protocol instance** is a pair of stateful machines — initiator role $I$
and responder role $R$ — each parameterised by the static identity of both
parties and an optional pre-shared key $\psi$.  The set of all instances is
$\Pi$, indexed by $s \in [\pi]$ for some polynomial $\pi = \pi(\lambda)$.

---

## 2. Key material

### Static keys

Each party $U \in \{I, R\}$ holds a long-term keypair for each of the two
static mechanisms:

| Identifier | Description | Reveal query |
|------------|-------------|--------------|
| $\mathit{sk}_{U_\mathit{DH}}$ | SM2 static secret key | `RevealStaticSM2(U)` |
| $(\mathit{sk}_{U_q},\, \mathit{pk}_{U_q})$ | Classic McEliece 460896 static KEM keypair | `RevealStaticKEM(U)` |

### Ephemeral keys (per-session)

Generated fresh for each handshake:

| Identifier | Description | Reveal query |
|------------|-------------|--------------|
| $(e, E)$ | Initiator ephemeral SM2 keypair ($E = eG$) | `RevealEphemeralSM2(s)` |
| $(e', E')$ | Responder ephemeral SM2 keypair ($E' = e'G$) | `RevealEphemeralSM2(s)` |
| $(e_q, E_q)$ | Initiator ephemeral KEM keypair (suite-selected) | `RevealEphemeralKEM_sk(s)` |
| $r_q$ | KEM encapsulation randomness (responder-side) | `RevealKEMCoins(s)` |
| $\psi$ | Pre-shared key | `RevealPSK(s)` |

---

## 3. Session state

**Session identifier** (`sid`): a canonical bit-string that uniquely identifies
one handshake attempt. Defined as:

$$\mathit{sid} := H(\mathit{pk}_{I_\mathit{DH}} \Vert \mathit{pk}_{R_\mathit{DH}} \Vert E \Vert E' \Vert \mathit{ct}_2 \Vert \mathit{ct}_3)$$

where $H = \mathrm{HMAC\text{-}SM3}(\cdot)$. All six components are public
after the handshake completes.

**Peer identifier** (`pid`): the static identity hash used by the v6 binary,
$\mathit{pid}(U) := H(\mathit{pk}_{U_\mathit{DH}} \Vert \mathit{pk}_{U_q})$
(matches `hash_static_keys` in `configuration_hybrid/config.rs`).

**Accepted session**: session $s$ for role $R$ has *accepted* once
`Resp` has emitted $(k_{r\to i}, k_{i\to r})$ and $\tau$ without aborting. For
role $I$, accepted means `Init` has verified the responder's MAC $\tau$ and
derived the same session keys.

**Matching session**: sessions $s$ (initiator) and $s'$ (responder) are
*matching* if $\mathit{sid}(s) = \mathit{sid}(s')$ and $\mathit{pid}$ records
agree (each records the other as the intended peer).

**Partnered session**: $s$ and $s'$ are *partnered* if they are matching and
both have accepted. The session key of a partnered pair must be identical (by
protocol correctness).

**Test session**: the session $s^*$ chosen by the adversary for the RoR
challenge. The experiment calls `Test(s*)` which either returns the real session
key $k_{s^*}$ (bit $b=0$) or an independent uniform $k^* \leftarrow
\{0,1\}^{256}$ (bit $b=1$).

---

## 4. Reveal queries

The adversary may issue the following queries at any point (including before,
during, or after the test):

| Query | What is returned | Freshness impact |
|-------|-----------------|-----------------|
| `RevealSessionKey(s)` | the session key of $s$ | if $s = s^*$ or $s$ is the partner of $s^*$: breaks freshness |
| `RevealStaticSM2(U)` | $\mathit{sk}_{U_\mathit{DH}}$ | breaks freshness if neither ephemeral nor static-KEM leg holds |
| `RevealStaticKEM(U)` | $\mathit{sk}_{U_q}$ | breaks $\textsf{F3}$; does *not* break forward secrecy after the session terminates if $\textsf{F1}$ or $\textsf{F2}$ holds |
| `RevealEphemeralSM2(s)` | $e$ or $e'$ of session $s$ | breaks $\textsf{F1}$ for session $s$ |
| `RevealEphemeralKEM_sk(s)` | $e_q$ of session $s$ | breaks $\textsf{F2}$ for session $s$ |
| `RevealKEMCoins(s)` | $r_q$ used for $\mathit{ct}_2$ in session $s$ | equivalent to `RevealEphemeralKEM_sk` when combined with $E_q$ |
| `RevealPSK(s)` | $\psi$ of session $s$ | breaks all freshness predicates if PSK is the sole binding |

---

## 5. Freshness predicates

Session $s^*$ is *fresh* if `RevealSessionKey(s*)` and `RevealSessionKey(s')`
have not been called (where $s'$ is the partner of $s^*$ if one exists), and at
least one of the three conditions below holds:

$$\textsf{F1}\;(\text{SM2 leg}):\ \neg\mathrm{RevealEphemeralSM2}(s^*) \land \neg\mathrm{RevealStaticSM2}(I) \land \neg\mathrm{RevealStaticSM2}(R)$$

$$\textsf{F2}\;(\text{ephemeral KEM leg}):\ \neg\mathrm{RevealEphemeralKEM\_sk}(s^*) \land \neg\mathrm{RevealKEMCoins}(s^*)$$

$$\textsf{F3}\;(\text{static KEM leg}):\ \neg\mathrm{RevealStaticKEM}(I) \land \neg\mathrm{RevealStaticKEM}(R)$$

**Ordinary secrecy** (the main claim): $s^*$ is fresh under $\textsf{F1} \lor \textsf{F2} \lor \textsf{F3}$.

**Forward secrecy** after later static-key compromise: if both static keys are
later compromised (`RevealStaticSM2` and `RevealStaticKEM` for both parties),
the session key of any already-accepted session $s^*$ remains secret provided
$\textsf{F1}$ (ephemeral SM2) or $\textsf{F2}$ (ephemeral KEM) held at the
time of acceptance. This is *ephemeral* forward secrecy; it does **not** hold
if the ephemeral randomness was also compromised before the session accepted.

---

## 6. Authentication and agreement claims

**Mutual entity authentication**: if $I$ accepts with peer-identity
$\mathit{pid}(R)$ and session-id $\mathit{sid}$, then $R$ ran an instance with
$\mathit{pid}(I)$ and the same $\mathit{sid}$ (and vice versa). This is
modelled by the `eISend` / `eRAccept` correspondence in the ProVerif
agility model and by the agreement lemmas in the full Tamarin/ProVerif
development.

**Implicit key authentication**: both parties derive identical session keys
$(k_{r\to i}, k_{i\to r})$ if and only if the session is partnered. Follows
from correctness of the KEM and ECDH plus the injectivity of HMAC-SM3 in the
ROM.

---

## 7. Non-goals (KCI and post-compromise security)

**Key-compromise impersonation (KCI)**: SM-PQ-WireGuard does *not* resist KCI
in general. If the initiator's static SM2 key $\mathit{sk}_{I_\mathit{DH}}$
is compromised, an adversary can impersonate an arbitrary responder to $I$.
This is a known limitation of the Noise IKpsk2 pattern. KCI resistance is not
claimed.

**Post-compromise security (PCS)**: once both static keys are compromised,
future sessions are attackable even if ephemeral keys are fresh. There is no
ratchet mechanism. PCS is not claimed. (Ephemeral forward secrecy *is* provided
for *past* sessions, as described in Section 5 above.)

---

## 8. Suite-agility scope

The theorem is parameterised by the choice of KEM. The reduction holds for any
IND-CCA-secure KEM in the ephemeral slot ($\KEMe$) or the static slot ($\KEMs$).
The ProVerif agility model (`agility_suite_model.pv`) verifies the
runtime suite-binding property (that the ephemeral-KEM suite selector is
authenticated and bound into the transcript) separately from the IND-CCA
reduction. The static-KEM slot is fixed (Classic McEliece 460896) and is
**not** subject to runtime agility; this note's security claim does not change
if the static slot is later made agile, but the suite-binding argument would
need to be re-examined for that slot.
