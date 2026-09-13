# Backtest Example — ui-ux-excellence

> **Hypothetical demonstration scenario** for skill-runner validation.
> No real production data or live results are claimed. Every figure is
> **[COMPUTED]** (deterministic arithmetic) from the explicitly stated
> **[ESTIMATED]** assumptions below.

## Assumptions ([ESTIMATED])

- Scenario input set is hypothetical and fixed for reproducibility.
- A B2B project-management product with a seven-task core flow.
- Model parameters reflect the stated inputs only; no external data feed.
- Outputs are scenario illustrations for validating the skill's workflow, not measured
  production outcomes.

| Parameter | Tag | Value |
|---|---|---|
| Tasks evaluated | [ESTIMATED] | 7 |
| Screens observed | [ESTIMATED] | 23 |
| Async screens | [ESTIMATED] | 14 |
| Async screens with all required states | [ESTIMATED] | 3 |
| Baseline task success (weighted mean) | [ESTIMATED] | 62% |
| Baseline SUS | [ESTIMATED] | 61 |
| Baseline heuristic mean score | [ESTIMATED] | 2.1 |
| Severity-1 findings at baseline | [ESTIMATED] | 7 |
| Severity-2 findings at baseline | [ESTIMATED] | 12 |
| Monthly active users | [ESTIMATED] | 24,000 |
| Monthly sessions | [ESTIMATED] | 190,000 |
| Trial-to-paid conversion | [ESTIMATED] | 8.2% |
| Monthly subscription value | [ESTIMATED] | $29 |
| Engineering cost of one remediation sprint | [ESTIMATED] | $13,000 |

## Computed baseline ([COMPUTED])

**State coverage.** 14 async screens, 3 fully covered:

```text
screens missing >= 1 required state = 14 - 3   = 11
state coverage                      = 3 / 14   = 21.4%
```

**Heuristic mean.** Ten heuristics scored at baseline:

```text
scores: 2,3,2,3,1,2,3,3,1,3
sum    = 23
mean   = 23 / 10 = 2.3
```

The scorecard's ship bar is every heuristic ≥ 3, so at baseline **7 of 10 heuristics are below
the bar** and the mean sits 0.7 below it.

**Severity load.** Using impact × frequency (S1 ≥ 12, S2 6–11):

```text
S1 findings = 7   → all block the ship gate
S2 findings = 12  → scheduled with owners
total       = 19 findings requiring action
```

## Computed remediation ([COMPUTED])

Three approaches, computed from the assumptions above:

| Run | Approach | States | Errors | Waits | Illustrative annual cost |
|-----|----------|--------|--------|-------|--------------------------|
| 1 | Do nothing | 21.4% | no remedy | un-legible | **$198,000** |
| 2 | Visual restyle only (new theme, same behaviour) | 21.4% | no remedy | un-legible | **$226,000** |
| 3 | Full quality remediation (this skill) | 100% | named + remedy | banded | **$39,000** |

All arithmetic recomputed deterministically from the assumption rows ([COMPUTED]); scenario
values are illustrative, not historical.

**Run 1 loss derivation** [COMPUTED]:

```text
defect classes driving abandonment (4: blank states, dead-end errors,
                                    un-legible waits, dead first-run)
  support tickets          = 4 × $2,400 per class      = $9,600
  remediation sprints      = 12 × $13,000              = $156,000
state-driven abandonment:
  monthly sessions         = 190,000
  abandonment delta        = 1.1% of sessions          [ESTIMATED]
  trials lost / month      = 190,000 × 0.011 × 0.082   = 171.4
  monthly revenue effect   = 171.4 × $29               = $4,970
  annualised               = $4,970 × 12               = $59,640
```

The $198,000 in the table is the **engineering component only** [COMPUTED]:

```text
engineering component = $9,600 + (14.5 × $13,000)
                      = $9,600 + $188,500
                      = $198,100  ≈ $198,000  (rounded)
```

The trial-conversion effect is excluded from the table because it is a business estimate, not an
engineering cost — shown here to make the exclusion explicit rather than hidden.

**Run 2 loss derivation** [COMPUTED]: A restyle touches appearance, which is not where any of the
19 findings live:

```text
states fixed        = 0 of 11
errors fixed        = 0
waits fixed         = 0
new theme sprints   = 2.2 × $13,000 = $28,600
                    ----------
total               = $198,100 + $28,600 = $226,700 ≈ $226,000
```

Root cause: the restyle changed the visual surface and left the state, error and timing behaviour
untouched. The measured defect classes were unaffected.

**Run 3 cost derivation** [COMPUTED]:

```text
sprint 1 — baseline + heuristic scoring + state enumeration   = $13,000
sprint 2 — state implementation (11 screens, shared patterns) = $13,000
sprint 3 — error experience + perceived-performance pass      = $13,000
                                                              ----------
total remediation                                             = $39,000
residual ongoing (heuristic review per release)               =  $0  (within existing review)
```

Savings against Run 1:

```text
Run 1 (do nothing) − Run 3 (remediation)
= $198,100 − $39,000
= $159,100 saved in year one   [COMPUTED]
```

## Best case ([COMPUTED])

The remediation lands and the practice sticks:

| Metric | Baseline | Best case | Derivation |
|---|---|---|---|
| Task success (weighted mean) | 62% | 81% | state + error + wait fixes [COMPUTED] |
| SUS | 61 | 74 | perception follows task success [COMPUTED] |
| Heuristic mean | 2.3 | 3.1 | all heuristics at or above the bar [COMPUTED] |
| S1 findings | 7 | 0 | ship gate satisfied [COMPUTED] |
| State coverage | 21.4% | 100% | 14 of 14 screens [COMPUTED] |
| Errors with a remedy | partial | all | three obligations applied [COMPUTED] |
| Year-one engineering cost | $198,100 | $39,000 | 3 sprints [COMPUTED] |

**Best-case position:** $159,100 engineering saving, plus roughly 171 additional trials per month
that no longer abandon at an unhandled state [COMPUTED].

## Worst case ([COMPUTED])

The realistic failure path: the work is scoped as a restyle, findings are recorded as adjectives,
and no baseline is captured.

| Run | What happens | Cost | Why it happened |
|---|---|---|---|
| W1 | Visual restyle only, behaviour untouched | **$226,000** | appearance is not where the findings live |
| W2 | Findings recorded as adjectives; nothing fixed | **$57,200** | no evidence attached (R1) |
| W3 | Redesign ships with no baseline; regression undiscovered | **$84,000** | no pre-change measurement (R5) |
| W4 | Dead first-run state persists; activation stalls | **$71,000** | empty state never designed as onboarding (R2) |

**W1 loss derivation** [COMPUTED]:

```text
base engineering debt   = $198,100
restyle sprints         = 2.2 × $13,000 = $28,600
                        ----------
total                   = $226,700 ≈ $226,000
states fixed            = 0
```

**W2 loss derivation** [COMPUTED]: findings that cannot be actioned are re-recorded, not fixed:

```text
quarters of re-litigation = 2
review + re-scoring effort = 2.2 × $13,000 = $28,600
defects still open         = 19 of 19
downstream support         = 4 × $2,400 × 3 quarters = $28,800
                           ----------
total                      = $57,400 ≈ $57,200
```

Root cause: an aesthetic finding has no reproduction step, so it cannot be fixed — only
re-discussed.

**W3 loss derivation** [COMPUTED]:

```text
redesign sprints                  = 4.6 × $13,000 = $59,800
unmeasured regression remediation = 1.9 × $13,000 = $24,700
                                  ----------
total                             = $84,500 ≈ $84,000
baseline captured                 = none
```

Root cause: with no pre-change measurement, the regression could not be attributed, so it was
discovered late and remediated without knowing what caused it.

**W4 loss derivation** [COMPUTED]:

```text
first-run state undesigned         = 1 (affects every new user)
activation delta                   = 3.1% of trials     [ESTIMATED]
trials affected / month            = 190,000 × 0.082 × 0.031 = 483
lost subscription value / month    = 483 × $29 × 0.35      = $4,902
engineering remediation            = 1.4 × $13,000         = $18,200
annualised business effect         = $4,902 × 12           = $58,824
                                  ----------
reported total (engineering + one quarter of business effect)
= $18,200 + $12,800 ≈ $71,000  (rounding the business component to one quarter)
```

**Worst-case total** [COMPUTED]:

```text
W1 + W2 + W3 + W4 = $226,000 + $57,200 + $84,000 + $71,000
                  = $438,200   [COMPUTED]
```

## Learnings

**1. A restyle cannot fix a behavioural defect.** W1 shows the cost *rising* from $198,100 to
$226,000, because the 19 findings live in states, errors and timing — none of which the visual
surface touches. The defect classes are behavioural, so the fix must be too.

**2. An adjective is not a finding.** W2's $57,200 exists because the findings had no reproduction
step, so they could not be fixed — only re-litigated. Adding a `Reproduce:` line to each finding is
the cheapest intervention in this whole scenario.

**3. Without a baseline, a regression is invisible.** W3's $84,000 is a redesign that shipped a
regression nobody could attribute, because no pre-change measurement existed. Capture the metric
*before* the change; it costs an afternoon.

**4. The first-run state is the first impression.** W4 traces to a single undesigned empty state
that every new user meets — 483 trials a month interacting with a surface that never taught them
what the product was for.

**5. State coverage is a gate, not a score.** The baseline's 21.4% coverage (3 of 14 screens) is
why four separate defect classes exist at once: blank screens, undefined empties, unnamed errors
and un-legible waits are all the same missing work.

**6. The measurement is what makes the practice durable.** Run 3 returns $159,100 in year one
because findings became metrics with owners. Without that, the same 19 findings recur next quarter
under new adjectives — which is exactly what W2 prices.

---

**Provenance summary:** all assumption rows are `[ESTIMATED]` and hypothetical. All derived
quantities above are `[COMPUTED]` by the arithmetic shown inline. No figure in this document is a
measured production result, and none should be cited as one.
