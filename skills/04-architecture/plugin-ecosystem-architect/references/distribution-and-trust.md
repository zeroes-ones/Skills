# Distribution and Trust

<!-- STANDARD: 3min -- publishing, signing, verification, review and revocation -->

## Why this decides the platform's abuse surface

Who can publish, and what is verified about them, determines what a hostile party can do at scale. Every
other control — capabilities, isolation, revocation — assumes you know *which* extension you are dealing
with.

## The publishing models

| Model | Who publishes | Required controls | Ecosystem velocity |
|---|---|---|---|
| **First-party only** | your team | none beyond your own process | not an ecosystem |
| **Reviewed publishers** | vetted organisations | publisher identity, review, signing keys | moderate |
| **Open, signed** | anyone with a verified identity | identity verification, automated scanning, signing | high |
| **Open, unsigned** | anyone | none | highest abuse surface |

**Unsigned is not a serious option for a public platform**, because a compromised update is
indistinguishable from a legitimate one. Signing is the minimum that makes the rest enforceable.

## Signing and verification

```text
Publisher                    Host
─────────                    ────
build artefact               fetch artefact + signature
sign with publisher key  →   verify signature against the trusted key set
                              ├── verified   → check revocation → install/update
                              └── unverified → refuse, with a clear reason
```

| Requirement | Why |
|---|---|
| Every artefact signed | otherwise an update can be substituted in transit or at the source |
| The host verifies before executing | verification after load is theatre |
| Keys are identified per publisher | revocation by publisher is then possible |
| Key rotation is supported | a compromised key must be replaceable without re-registering everyone |
| Verification failure is a refusal, not a warning | a warning is a prompt to click through |

**The key-rotation path is the one teams omit**, and it is what makes a publisher compromise recoverable.

## Automated scanning

Review cannot scale to an open ecosystem, so automated scanning carries most of the load:

| Scan | Catches |
|---|---|
| Manifest validation | malformed or missing declarations, unexpected capabilities |
| Static analysis for the extension's language | obvious malicious patterns, credential harvesting |
| Dependency analysis | vulnerable or prohibited transitive dependencies |
| Capability-versus-behaviour mismatch | an extension that requests nothing and attempts network access |
| Binary/signature integrity | tampered or unexpected artefacts |
| Known-bad signatures/hashes | previously revoked artefacts reappearing |

**The capability-versus-behaviour check is the highest-value one**, because it catches the class the
capability model is designed for: an extension doing what it did not declare. If enforcement is correct
the attempt fails at runtime, but detecting it at publish time is better.

## The review question

Review does not scale to every submission, so decide *what* is reviewed rather than whether:

| Reviewed | Not reviewed |
|---|---|
| Anything requesting high-impact capabilities | extensions using only low-impact capabilities |
| First submission from a new publisher | updates from a publisher with a track record |
| Anything flagged by automated scanning | extensions passing all automated checks |
| High-install extensions | long-tail extensions |

**State the review model publicly**, so publishers know what to expect and users know what has been
checked. An unstated review process is a source of dispute in both directions.

## Revocation, revisited

The distribution-side counterpart to the lifecycle's revoke (see `lifecycle.md`):

| Element | Detail |
|---|---|
| A published revocation list | signed, and checked by hosts |
| A defined check cadence | how often, and what happens when unreachable |
| Publisher-level revocation | for a compromised account, not just a single artefact |
| Version-level revocation | for a bad release where the publisher is otherwise fine |
| User communication | what was revoked, and why, in plain terms |
| A publisher appeal path | otherwise revocation is unilateral and the ecosystem notices |

## Platform rules to confirm

Distribution rules are the constraint that most often invalidates a designed model (R6-adjacent — the
platform-constraint check). Confirm per channel and per product category:

| Rule area | The question |
|---|---|
| Third-party code | may the host load code that did not ship with it? |
| Bundled runtimes | may you ship a sandbox runtime? |
| Signing | must every loaded unit be signed, and by whom? |
| Review | is there a mandatory review, and what does it cover? |
| Update mechanism | may the host update extensions outside the channel's process? |
| Content policy | what may an extension do or contain? |
| Data handling | what must the platform declare about third-party data flows? |

**A forbidden model is not a choice.** Confirm before designing the distribution, as the cost of
redesigning it is high and late.

## Trust communication to users

| Surface | Content |
|---|---|
| Install | publisher, capabilities, whether the extension is reviewed |
| Extension list | version, publisher, current capabilities, state |
| Update | what changed, especially capability expansion |
| Revocation | what stopped working, and why |
| Publisher page | identity, verification status, other extensions, history |

**The verification badge distinction matters:** "verified publisher" means identity is confirmed, not
that the code is safe. Conflating the two creates liability and misplaced trust. Be precise in the
wording.

## Checklist

- [ ] The publishing model is chosen and published
- [ ] Every artefact is signed, and the host verifies before executing
- [ ] Publisher keys are identified, and key rotation is supported
- [ ] Verification failure is a refusal, not a dismissible warning
- [ ] Automated scanning covers manifest, static analysis, dependencies and capability-behaviour mismatch
- [ ] The review model is stated publicly, and what it does and does not cover
- [ ] A revocation list exists, signed, with a defined check cadence and offline behaviour
- [ ] Publisher-level revocation is possible, not only per-artefact
- [ ] An appeal path exists for publishers
- [ ] The channel's distribution rules were confirmed before the model was designed
- [ ] User-facing trust language distinguishes identity verification from safety
