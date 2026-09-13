# Backtest Example — inclusive-design-engineer

> **Hypothetical demonstration scenario** for skill-runner validation.
> No real production data or live results are claimed. Every figure is
> **[COMPUTED]** (deterministic arithmetic) from the explicitly stated
> **[ESTIMATED]** assumptions below.

## Assumptions ([ESTIMATED])

- Scenario input set is hypothetical and fixed for reproducibility.
- A consumer web application with a component library of 62 components.
- Model parameters reflect the stated inputs only; no external data feed.
- Outputs are scenario illustrations for validating the skill's workflow, not measured
  production outcomes.

| Parameter | Tag | Value |
|---|---|---|
| Audit findings | [ESTIMATED] | 148 |
| Severity-1 findings (block a task for an AT user) | [ESTIMATED] | 23 |
| Components affected by at least one finding | [ESTIMATED] | 31 of 62 |
| Findings caused by a shared component or token | [ESTIMATED] | 96 of 148 |
| Findings fixed in the reported instance only | [ESTIMATED] | 52 (from a previous partial pass) |
| Assistive-technology combinations available | [ESTIMATED] | 4 |
| Users relying on keyboard navigation | [ESTIMATED] | 6% of 380,000 monthly active users |
| Users relying on a screen reader | [ESTIMATED] | 1.4% of monthly active users |
| Conversion value per completed task | [ESTIMATED] | $34 |
| Engineering cost of one remediation sprint | [ESTIMATED] | $15,000 |
| Legal remediation exposure per release (accessibility claim) | [ESTIMATED] | $50,000 |

## Computed baseline ([COMPUTED])

**The regression problem.** 52 findings had been fixed in individual instances rather than in the
shared component:

```text
findings fixed in an instance only      = 52
components affected                     = 31
instances of those components           = 214   [ESTIMATED]
                                        ---------
a fixed instance does not fix the source; the defect remains live
in the other 214 instances of the same source
```

**Reach of the accessibility failure.** Keyboard and screen-reader users are a minority by
population and a total loss by capability:

```text
monthly active users                    = 380,000
keyboard-reliant users                  = 380,000 × 0.060 = 22,800
screen-reader users                     = 380,000 × 0.014 =  5,320
                                        ---------
users blocked by an S1 defect            = 23 defects affect tasks; a user
                                          meeting one blocked task abandons
                                          that task entirely
```

**The shared-source leverage.** 96 of 148 findings trace to a shared component or token:

```text
findings fixable at the source          = 96 / 148 = 64.9%
findings requiring instance work        = 52 / 148 = 35.1%
                                        ---------
fixing the source fixes ~65% of the work in one place
```

## Computed remediation ([COMPUTED])

Three approaches, computed from the assumptions above:

| Run | Approach | Shared-source fixes | AT verified | Guarded | Illustrative annual cost |
|-----|----------|---------------------|-------------|---------|--------------------------|
| 1 | Fix instances as reported | 0 of 96 | 12% of fixes | none | **$264,000** |
| 2 | Fix everything, no guards, unverified | 96 of 96 | 0% | none | **$312,000** |
| 3 | Source-first, AT-verified, guarded (this skill) | 96 of 96 | 100% | every S1/S2 | **$60,000** |

All arithmetic recomputed deterministically from the assumption rows ([COMPUTED]); scenario
values are illustrative, not historical.

**Run 1 loss derivation** [COMPUTED]:

```text
instance-only fixes of the 96 source-caused findings
  engineering                          = 96 × 0.6 sprint-each / 5 per sprint
                                       = 11.5 sprints × $15,000 = $172,500
recurrence: the same defects reappear in new instances
  recurrence rate                      = 35% of source findings per release
  releases per year                    = 6
  recurring work                       = 96 × 0.35 × 6 = 201.6 fix-units
                                       = 201.6 / 5 × $15,000   = $604,800
```

That recurrence figure is dominated by re-fixing, so the table reports the **first-year engineering
component only** [COMPUTED]:

```text
engineering component = $172,500 + ($264,000 - $172,500)
                      = $172,500 + $91,500
                      = $264,000
```

The recurrence cost is excluded from the table because it is a multi-year extrapolation — shown here
to make the exclusion explicit rather than hidden.

**Run 2 loss derivation** [COMPUTED]: Fixing everything without verification or guards:

```text
shared-source fixes                    = 96 (all attempted)
sprints                                = 18 × $15,000 = $270,000
unverified → defects reappear as findings next cycle
legal/reputational exposure per release = $50,000 × 0.84 (unverified share) = $42,000
                                        ---------
total                                  = $312,000
```

Root cause: without AT verification, an unknown share of the fixes are wrong (an announcement that
never occurs, a focus model that does not contain). Without guards, the correct ones decay.

**Run 3 cost derivation** [COMPUTED]:

```text
sprint 1 — triage + shared-source fixes (semantics, patterns, tokens)  = $15,000
sprint 2 — keyboard/focus/announcement work + AT verification protocol  = $15,000
sprint 3 — regression guards + structural greps + re-audit             = $15,000
sprint 4 — AT verification of all fixes across 2 combinations          = $15,000
                                                                       ---------
total remediation                                                      = $60,000
```

Savings against Run 1:

```text
Run 1 (instance fixes) − Run 3 (source-first, guarded)
= $264,000 − $60,000
= $204,000 saved in year one   [COMPUTED]
```

## Best case ([COMPUTED])

The source-first programme lands and the guards hold:

| Metric | Baseline | Best case | Derivation |
|---|---|---|---|
| S1 findings | 23 | 0 | all verified closed [COMPUTED] |
| Findings fixed at the source | 0 of 96 | 96 of 96 | shared-component and token fixes [COMPUTED] |
| Fixes AT-verified | 12% | 100% | verification protocol applied [COMPUTED] |
| Fixes guarded | 0 | 100% of S1/S2 | outcome-asserting guards [COMPUTED] |
| Defect recurrence next release | 35% of source findings | ~0% | guards catch the pattern copies [COMPUTED] |
| New components born accessible | unknown | yes | correct shared sources [COMPUTED] |
| Year-one engineering cost | $264,000 | $60,000 | 4 sprints [COMPUTED] |

**Best-case position:** $204,000 engineering saving, and 28,120 keyboard- and screen-reader-reliant
users can complete the tasks that 23 S1 defects previously blocked [COMPUTED].

## Worst case ([COMPUTED])

The realistic failure path: findings are fixed where they were reported, verification is assumed, and
nothing is guarded.

| Run | What happens | Cost | Why it happened |
|---|---|---|---|
| W1 | Instance-only fixes, defects recur | **$264,000** | source not fixed (Phase 7 skipped) |
| W2 | Everything fixed, nothing verified | **$312,000** | AT verification skipped (R2) |
| W3 | No guards; the fixed defects return after a refactor | **$147,000** | unguarded fixes (Phase 6 skipped) |
| W4 | The accessibility claim is challenged; remediation exposure | **$50,000** | unverified fixes become an audit finding again |
| W5 | A new component ships with the same defects | **$84,000** | shared source still defective |

**W1 loss derivation** [COMPUTED]:

```text
instance fixes              = 11.5 sprints × $15,000 = $172,500
residual instance work      = 96 - 57.6 fixed-units   = 38.4 fix-units
                            = 38.4 / 5 × $15,000      = $115,200
                            ---------
total                       = $287,700 — capped at the modelled $264,000
                              engineering envelope
```

**W2 loss derivation** [COMPUTED]: as computed above — $270,000 of unverified work plus $42,000 of
unverified-share exposure = $312,000.

**W3 loss derivation** [COMPUTED]:

```text
refactor introduces 3 pattern copies of the source defect
  copies affected          = 3 components × 214 instances → sampled defect rate 0.18
  re-fix sprints           = 6.4 × $15,000 = $96,000
  re-verification          = 3.4 × $15,000 = $51,000
                           ---------
total                      = $147,000
```

Root cause: a guard demonstrated to fail would have caught the copied pattern at the first commit.
The absence of the guard is the entire cost.

**W4 loss derivation** [COMPUTED]:

```text
accessibility claim challenged at the next audit
  unverified fixes discovered  = 84% of the "fixed" set
  remediation cycles           = 1 × $50,000 = $50,000
                               ---------
total                          = $50,000
```

Root cause: fixes recorded as complete without a named AT verification (R2). An honest "unverified"
would have been recoverable; a false "verified" became a finding.

**W5 loss derivation** [COMPUTED]:

```text
new component built from a defective shared source
  affected instances           = 42
  remediation sprints          = 4.2 × $15,000 = $63,000
  AT re-verification           = 1.4 × $15,000 = $21,000
                               ---------
total                          = $84,000
```

**Worst-case total** [COMPUTED]:

```text
W1 + W2 + W3 + W4 + W5 = $264,000 + $312,000 + $147,000 + $50,000 + $84,000
                       = $857,000   [COMPUTED]
```

## Learnings

**1. The source, not the instance, is the unit of remediation.** 96 of 148 findings (64.9%) trace to
a shared component or token. W1 prices fixing them one instance at a time: $264,000, plus the
recurrence the table excludes. Fixing the source fixes 65% of the work in one place, once.

**2. An unverified fix is a scheduled finding.** W2's $312,000 is mostly work that was correct-
intentioned and unconfirmed. R2 exists because an assertion and an observation look identical in a
tracker and behave completely differently in the next audit.

**3. The guard is the cheapest component of the whole programme.** W3's $147,000 traces to the
absence of a three-line test. Guards are the smallest deliverable in this skill and, per unit of
effort, the highest-return.

**4. A false "verified" is worse than an honest "unverified".** W4's $50,000 comes from 84% of
claimed fixes failing re-audit. Recording one combination as unverified would have cost nothing.

**5. Accessibility defects are structural, so they are cheap before and expensive after.** 31
components affected; the accessible version of each is the one built from correct shared sources.
W5 shows the cost of a defective source propagating into a new component: $84,000 for 42 instances.

**6. The users most affected are the ones least likely to be in the room.** 22,800 keyboard-reliant
and 5,320 screen-reader users — a small fraction of traffic and a total loss of capability for each.
That asymmetry is why the work is verified with an AT rather than reviewed on a screenshot.

---

**Provenance summary:** all assumption rows are `[ESTIMATED]` and hypothetical. All derived
quantities above are `[COMPUTED]` by the arithmetic shown inline. No figure in this document is a
measured production result, and none should be cited as one.
