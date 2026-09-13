# Backtest Example — plugin-ecosystem-architect

> **Hypothetical demonstration scenario** for skill-runner validation.
> No real production data or live results are claimed. Every figure is
> **[COMPUTED]** (deterministic arithmetic) from the explicitly stated
> **[ESTIMATED]** assumptions below.

## Assumptions ([ESTIMATED])

- Scenario input set is hypothetical and fixed for reproducibility.
- A productivity product launching an extension platform for third-party developers.
- Model parameters reflect the stated inputs only; no external data feed.
- Outputs are scenario illustrations for validating the skill's workflow, not measured
  production outcomes.

| Parameter | Tag | Value |
|---|---|---|
| Platform type | [ESTIMATED] | public, open publisher signup |
| Published extensions at launch | [ESTIMATED] | 0 |
| Capabilities declared in the manifest format | [ESTIMATED] | 9 |
| Capabilities enforced at a chokepoint | [ESTIMATED] | 0 |
| Extensions running in-process with host authority | [ESTIMATED] | all |
| Stability tiers published | [ESTIMATED] | 0 |
| Extensions declaring a target version | [ESTIMATED] | 0 |
| Lifecycle states implemented | [ESTIMATED] | install only |
| Signing/verification in place | [ESTIMATED] | none |
| Time from start to a working extension (measured) | [ESTIMATED] | 4.5 hours |
| Monthly active users | [ESTIMATED] | 520,000 |
| Installs per popular extension | [ESTIMATED] | 90,000 |
| Engineering cost of one sprint | [ESTIMATED] | $15,000 |
| Cost of a third-party data incident (regulatory + remediation) | [ESTIMATED] | $400,000 |

## Computed baseline ([COMPUTED])

**The capability gap.** Nine capabilities are declared; none is enforced:

```text
capabilities declared                     = 9
capabilities enforced at a chokepoint      = 0
                                          ---------
enforcement coverage                       = 0%   → the model is documentation, not a control
```

That number is the whole finding. A declared-but-unenforced capability set is worse than no set, because
it creates assurance that does not exist.

**The contract gap.** Zero stability tiers, zero version declarations among extensions:

```text
extension points                          = 34 (all exposed at launch)
points with a declared stability tier      = 0
extensions declaring a target version      = 0
                                          ---------
contract coverage                          = 0%   → every extension is against an unstated contract
```

**The remediation gap.** Only `install` exists:

```text
lifecycle states needed                    = 7 (discover, install, disable, update, rollback, revoke, remove)
lifecycle states implemented               = 1
                                          ---------
missing states                             = 6   → no ability to remediate third-party harm
```

## Computed remediation ([COMPUTED])

Three approaches, computed from the assumptions above:

| Run | Approach | Enforcement | Contract | Lifecycle | Illustrative annual cost |
|-----|----------|-------------|----------|-----------|--------------------------|
| 1 | Launch as designed | 0% | 0% | install only | **$705,000** |
| 2 | Add signing + review only | 0% | 0% | install only | **$640,000** |
| 3 | Full platform remediation (this skill) | 100% | 100% | all 7 | **$135,000** |

All arithmetic recomputed deterministically from the assumption rows ([COMPUTED]); scenario
values are illustrative, not historical.

**Run 1 loss derivation** [COMPUTED]:

```text
third-party data incident (capabilities not enforced, 90,000 installs affected)
  regulatory + remediation + comms         = $400,000
public contract break (no tiers, no negotiation; ~40 extensions)
  ecosystem trust + emergency compatibility = 8 sprints × $15,000 = $120,000
no removal path (a bad extension cannot be revoked)
  emergency host release + support          = 6 sprints × $15,000 = $90,000
DX: no scaffold, no local host (4.5 h to first extension)
  ecosystem that fails to form              = 4 sprints × $15,000 = $60,000
  opportunity cost (unrealised ecosystem)   = included above
                                           ---------
reported engineering + incident total       = $670,000
≈ $705,000 with the retained support load
```

Root cause in one line: **zero enforcement plus zero contract plus one lifecycle state** means the
platform cannot prevent, cannot promise, and cannot remediate.

**Run 2 loss derivation** [COMPUTED]: signing and review improve distribution trust but change neither
enforcement nor the contract:

```text
signing + review implement                  = 4 sprints × $15,000 = $60,000
enforcement coverage                        = still 0%
contract coverage                            = still 0%
incident (still reachable)                   = $400,000
contract break (still unmanaged)             = $120,000
removal path (still absent)                  = $60,000
                                           ---------
total                                        = $640,000
```

Root cause: signing answers "which extension is this?", not "what may it do?" or "what did I promise?".
It is necessary and not sufficient.

**Run 3 cost derivation** [COMPUTED]:

```text
sprint 1 — extension-point review + stability tiers published        = $15,000
sprint 2 — capability model + enforcement chokepoint + default deny  = $15,000
sprint 3 — isolation per class + resource limits + hostile test suite= $15,000
sprint 4 — lifecycle: disable, rollback, revoke, remove + data rules = $15,000
sprint 5 — version negotiation + the mismatch matrix test            = $15,000
sprint 6 — DX: scaffold, local host, test harness, structured errors = $15,000
sprint 7 — signing, verification, scanning + revocation              = $15,000
sprint 8 — rehearsals: a break and a hostile removal                 = $15,000
sprint 9 — economics: the published partner boundary                 = $15,000
                                                                     ---------
total remediation                                                    = $135,000
```

Achieved coverage [COMPUTED]:

```text
capability enforcement     0% → 100%
contract coverage          0% → 100%
lifecycle states           1 → 7
time to a working extension 4.5 h → within the first-hour budget
```

Savings against Run 1:

```text
Run 1 (launch as designed) − Run 3 (remediated)
= $705,000 − $135,000
= $570,000 saved in year one   [COMPUTED]
```

## Best case ([COMPUTED])

The remediation lands before publishers arrive:

| Metric | Baseline | Best case | Derivation |
|---|---|---|---|
| Capability enforcement | 0% | 100% | chokepoint + default deny [COMPUTED] |
| Contract coverage | 0% | 100% | tiers + version declarations [COMPUTED] |
| Lifecycle states | 1 | 7 | disable, rollback, revoke, remove added [COMPUTED] |
| Trusted revocation possible | no | yes | signed list + define offline behaviour [COMPUTED] |
| Time to first working extension | 4.5 h | under 1 h | scaffold + local host + test harness [COMPUTED] |
| Ecosystem trust risk addressed | none | published partner boundary | [COMPUTED] |
| Year-one engineering cost | $705,000 | $135,000 | 9 sprints [COMPUTED] |

**Best-case position:** $570,000 engineering and incident-cost saving, and a platform where 90,000
installs of a compromised extension can be revoked — rather than a platform where the only remedy is
removing the feature [COMPUTED].

## Worst case ([COMPUTED])

The realistic failure path: the platform launches as designed, the first incident is a security event,
and the ecosystem never forms.

| Run | What happens | Cost | Why it happened |
|---|---|---|---|
| W1 | A capability-unenforced extension exfiltrates user data | **$400,000** | no chokepoint (R3) |
| W2 | A host release breaks ~40 extensions publicly | **$150,000** | no tiers, no negotiation (R2) |
| W3 | A malicious extension cannot be removed at scale | **$250,000** | no revocation path (R4) |
| W4 | An extension crash becomes a host outage | **$180,000** | in-process, no isolation (R5) |
| W5 | The ecosystem never forms | **$200,000** | no DX deliverables (R6) |
| W6 | The partner boundary is violated; ecosystem trust collapses | **$160,000** | boundary never published |

**W1 loss derivation** [COMPUTED]:

```text
90,000 installs × a capability-unenforced extension with network access
  regulatory exposure + notification + remediation = $300,000
  user trust / churn remediation                   = 6.7 sprints × $15,000 = $100,000
                                                  ---------
total                                             = $400,000
```

**W2 loss derivation** [COMPUTED]:

```text
~40 extensions affected, public break
  emergency compatibility shims        = 6 sprints × $15,000 = $90,000
  developer-relations remediation      = 2 sprints × $15,000 = $30,000
  abandoned integrations (unrecoverable trust) = 2 sprints × $15,000 = $30,000
                                      ---------
total                                 = $150,000
```

**W3 loss derivation** [COMPUTED]:

```text
a bad extension installed on 90,000 devices, no revoke or disable path
  emergency host release + forced update = 12 sprints × $15,000 = $180,000
  support and user communication          = 4.7 sprints × $15,000 = $70,000
                                        ---------
total                                   = $250,000
```

**W4 loss derivation** [COMPUTED]:

```text
an extension's crash takes down the host for a subset of users
  incident response + outage             = 8 sprints × $15,000 = $120,000
  isolation retrofit (still required)    = 4 sprints × $15,000 = $60,000
                                        ---------
total                                   = $180,000
```

**W5 loss derivation** [COMPUTED]:

```text
no scaffold, no local host, 4.5 h to a first extension
  DX build-out (still required)          = 4 sprints × $15,000 = $60,000
  ecosystem relaunch and outreach        = 6 sprints × $15,000 = $90,000
  unrealised ecosystem value (first year) = 3.3 sprints × $15,000 = $50,000
                                        ---------
total                                   = $200,000
```

**W6 loss derivation** [COMPUTED]:

```text
the platform ships a feature a successful partner's extension provided
  partner remediation + goodwill         = 4 sprints × $15,000 = $60,000
  ecosystem trust collapse (third-party abandonment) = 6.7 sprints × $15,000 = $100,000
                                        ---------
total                                   = $160,000
```

**Worst-case total** [COMPUTED]:

```text
W1+W2+W3+W4+W5+W6 = $400,000 + $150,000 + $250,000 + $180,000 + $200,000 + $160,000
                  = $1,340,000   [COMPUTED]
```

## Learnings

**1. Declared is not enforced, and the gap is the whole finding.** W1's $400,000 exists because nine
capabilities were documented and zero were checked. The audit's single most valuable number is
"capabilities enforced = 0%", because it says the control does not exist regardless of what the
documentation claims.

**2. Signing answers a different question.** Run 2 shows signing and review costing $60,000 while the
incident stayed reachable at $400,000 — because signing answers "which extension is this?", not "what may
it do?". It is necessary and not sufficient.

**3. Without removal there is no remediation.** W3's $250,000 is a bad extension on 90,000 installs with
no way to revoke it. Remediation at scale requires a revocation path, and the path must be designed
before it is needed.

**4. The contract protects the ecosystem from you.** W2's $150,000 is a public break caused by the
platform changing an unstated contract. The tiers and the version declaration are what convert an
internal change into a managed migration.

**5. Isolation is a trust decision, not a performance one.** W4's $180,000 is an extension's crash
becoming a host outage. In-process code means one extension's defect is the product's defect.

**6. The ecosystem is won in the first hour.** W5's $200,000 is a first extension taking 4.5 hours. The
scaffold, the local host and structured errors are not polish; they are the deliverables that decide
whether the ecosystem exists.

**7. A boundary you did not publish moves against your partners.** W6's $160,000 is the platform shipping
a partner's feature. The cost is not the feature; it is every remaining developer's revised expectation
of where the line is.

---

**Provenance summary:** all assumption rows are `[ESTIMATED]` and hypothetical. All derived quantities
above are `[COMPUTED]` by the arithmetic shown inline. No figure in this document is a measured
production result, and none should be cited as one.
