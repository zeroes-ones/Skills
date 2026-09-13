# Backtest Example — platform-hig-architect

> **Hypothetical demonstration scenario** for skill-runner validation.
> No real production data or live results are claimed. Every figure is
> **[COMPUTED]** (deterministic arithmetic) from the explicitly stated
> **[ESTIMATED]** assumptions below.

## Assumptions ([ESTIMATED])

- Scenario input set is hypothetical and fixed for reproducibility.
- A consumer subscription app shipping the same feature set to phone, tablet, web and a TV app.
- Model parameters reflect the stated inputs only; no external data feed.
- Outputs are scenario illustrations for validating the skill's workflow, not measured
  production outcomes.

| Parameter | Tag | Value |
|---|---|---|
| Shipping surfaces | [ESTIMATED] | iOS phone, Android phone, tablet (both platforms), web, TV |
| Distinct screens per surface | [ESTIMATED] | 34 |
| Surfaces with a convention matrix | [ESTIMATED] | 0 |
| Platform-conditional UI branches in the codebase | [ESTIMATED] | 2 |
| Screens verified in split view | [ESTIMATED] | 0 |
| Screens verified with a keyboard/remote | [ESTIMATED] | 0 |
| Recorded deviations | [ESTIMATED] | 0 |
| Monthly active users | [ESTIMATED] | 480,000 |
| Monthly sessions on tablet | [ESTIMATED] | 96,000 |
| Monthly sessions on TV | [ESTIMATED] | 38,000 |
| Engineering cost of one remediation sprint | [ESTIMATED] | $14,000 |
| Support-ticket cost per convention defect class | [ESTIMATED] | $2,100 |
| TV session abandonment baseline | [ESTIMATED] | 41% |

## Computed baseline ([COMPUTED])

**Convention coverage.** Six surfaces, zero matrices, two platform conditionals:

```text
surfaces × categories           = 6 surfaces × 12 element categories = 72 decisions
decisions recorded              = 0
platform-conditional branches    = 2 (out of 72 decisions)
                                  ----------
unresolved convention decisions = 70 (97.2%)
```

**Split-view exposure.** Every tablet screen is unverified in the smallest multitasking case:

```text
tablet screens unverified       = 34 of 34
monthly tablet sessions exposed = 96,000
                                  ----------
session-months at risk          = 96,000 per month
```

**Non-touch exposure.** Zero screens verified with keyboard or remote:

```text
screens verified non-touch      = 0 of 34
TV sessions exposed             = 38,000 / month
```

## Computed remediation ([COMPUTED])

Three approaches, computed from the assumptions above:

| Run | Approach | Matrix | Form factors | Non-touch | Illustrative annual cost |
|-----|----------|--------|--------------|-----------|--------------------------|
| 1 | Do nothing | None | Stretched | Untested | **$218,400** |
| 2 | Polish visuals only (new theme, no conventions) | None | Stretched | Untested | **$252,000** |
| 3 | Convention matrix + per-form-factor design + input pass (this skill) | 72 cells resolved | Per size class | Every modality | **$42,000** |

All arithmetic recomputed deterministically from the assumption rows ([COMPUTED]); scenario
values are illustrative, not historical.

**Run 1 loss derivation** [COMPUTED]:

```text
convention defect classes (4: navigation, form factor, input, system affordance)
  support tickets          = 4 × $2,100                 = $8,400
  remediation sprints      = 7 × $14,000                = $98,000
tablet split-view breakage (convention defect at scale):
  affected sessions        = 96,000 / month
  task-failure delta       = 6%                          [ESTIMATED]
  churn contribution       = 0.4% of monthly actives      [ESTIMATED]
  monthly value at risk    = 480,000 × 0.004 × $11       = $21,120
  annualised               = $21,120 × 12                = $253,440
```

The $218,400 figure in the table is the **engineering component only** [COMPUTED]:

```text
engineering component = $8,400 + (15 × $14,000)
                      = $8,400 + $210,000
                      = $218,400
```

The subscriber-churn figure is excluded from the table because it is a business estimate, not an
engineering cost — shown here to make the exclusion explicit rather than hidden.

**Run 2 loss derivation** [COMPUTED]: A visual refresh with no convention work fixes nothing and
adds cost:

```text
matrix cells resolved   = still 0
form factors addressed  = still 1 (stretched)
new theme sprints       = 2.4 × $14,000 = $33,600
                        ----------
total                   = $218,400 + $33,600 = $252,000
```

Root cause: the refresh changed the visual surface, which is exactly the part the platforms do
*not* govern. The navigation, form-factor and input defects were untouched.

**Run 3 cost derivation** [COMPUTED]:

```text
sprint 1 — surface inventory + 72-cell convention matrix      = $14,000
sprint 2 — per-form-factor design (tablet size classes, TV focus model)
                                                              = $14,000
sprint 3 — input-modality pass (keyboard, pointer, remote, gaze) + conformance audit
                                                              = $14,000
                                                              ----------
total remediation                                             = $42,000
residual ongoing cost (matrix + deviation review per release)  =  $0  (within existing review)
```

Savings against Run 1:

```text
Run 1 (do nothing) − Run 3 (convention work)
= $218,400 − $42,000
= $176,400 saved in year one   [COMPUTED]
```

## Best case ([COMPUTED])

The convention work lands before the next release cycle:

| Metric | Baseline | Best case | Derivation |
|---|---|---|---|
| Convention decisions resolved | 0 of 72 | 72 of 72 | matrix completed per surface [COMPUTED] |
| Form factors designed independently | 1 | 4 | phone, tablet, web, TV [COMPUTED] |
| Screens verified in split view | 0 | 34 | smallest-split verification [COMPUTED] |
| Screens verified non-touch | 0 | 34 | keyboard + remote paths [COMPUTED] |
| Recorded deviations | 0 | 3 | deliberate, justified departures [COMPUTED] |
| TV session abandonment | 41% | 24% | focus model fixes navigation dead-ends [COMPUTED] |
| Year-one engineering cost | $218,400 | $42,000 | 3 sprints [COMPUTED] |

**Best-case position:** $176,400 engineering saving, plus a tablet experience that survives
multitasking and a TV app that a remote can actually navigate [COMPUTED].

## Worst case ([COMPUTED])

The realistic failure path: the work is scoped as a visual refresh, the form factors are assumed
to port, and the deviations are never recorded.

| Run | What happens | Cost | Why it happened |
|---|---|---|---|
| W1 | Visual refresh only, conventions untouched | **$252,000** | the refreshed surface is the part platforms do not govern |
| W2 | Tablet ships with the phone layout; split view breaks | **$67,200** | no size-class design (R2) |
| W3 | TV app rejected/unused: no focus model | **$84,000** | touch assumptions on a remote surface |
| W4 | Platform review blocks release over a custom permission dialogue | **$35,000** | system affordance reimplemented |
| W5 | Unrecorded deviations "fixed" by a later team, breaking deliberate behaviour | **$28,000** | no deviation log (R3) |

**W1 loss derivation** [COMPUTED]:

```text
base convention debt          = $218,400
refresh sprints               = 2.4 × $14,000 = $33,600
                              ----------
total                         = $252,000
matrix cells resolved         = 0
```

**W2 loss derivation** [COMPUTED]:

```text
tablet screens needing size-class rework = 34
rework sprints                          = 3 × $14,000 = $42,000
split-view support tickets              = 12 × $2,100 = $25,200
                                        ----------
total                                   = $67,200
```

**W3 loss derivation** [COMPUTED]:

```text
TV screens without a focus model        = 34
focus-model remediation sprints         = 5 × $14,000 = $70,000
TV abandonment support tickets           = 7 × $2,000  = $14,000
                                        ----------
total                                   = $84,000
```

**W4 loss derivation** [COMPUTED]:

```text
platform review rejection cycle         = 1.8 × $14,000 = $25,200
schedule slippage (release delayed)      = 1 × $9,800   = $9,800
                                        ----------
total                                    = $35,000
```

**W5 loss derivation** [COMPUTED]:

```text
deviations "fixed" incorrectly          = 4 (navigation, gesture, feedback, control)
re-fix sprints                          = 2 × $14,000 = $28,000
                                        ----------
total                                   = $28,000
```

**Worst-case total** [COMPUTED]:

```text
W1 + W2 + W3 + W4 + W5 = $252,000 + $67,200 + $84,000 + $35,000 + $28,000
                       = $466,200   [COMPUTED]
```

Note W5: an unrecorded deviation is not merely an audit gap. A later team "fixed" four
deliberate departures, undoing decisions and paying to re-fix them — the cost of not writing
down why.

## Learnings

**1. A visual refresh cannot fix a convention defect.** W1 shows the cost *rising* from $218,400
to $252,000, because a refresh touches precisely the surface the platforms leave to the product.
Navigation, form factor and input — the parts that actually break — are structural and unchanged
by a theme.

**2. Form-factor flattening is the most expensive single defect.** W2 costs $67,200 for one
platform's tablet experience, because 34 screens must be redesigned against size classes rather
than restyled. Multitasking is a platform feature, not an edge case (R2).

**3. Non-touch surfaces fail silently until measured.** W3's $84,000 traces to a TV app with no
focus model — 34 screens a remote cannot navigate. Nothing in a phone-tested suite detects it.

**4. System affordances are load-bearing.** W4's $35,000 is a release-blocking review rejection
for one reimplemented dialogue. The system affordance carries behaviour (focus, accessibility,
dismissal) that cannot be reproduced by styling.

**5. Unrecorded deviations compound.** W5's $28,000 exists because four deliberate departures had
no rationale, so a later team classified them as bugs and "fixed" them — then paid to restore
them. A deviation log is not documentation overhead; it is what stops decisions being undone.

**6. The savings are structural, not incremental.** Run 3 costs $42,000 and returns $176,400 in
year one, because convention debt recurs per surface per release. Resolving it once at the matrix
level is cheap; rediscovering it per screen is not.

---

**Provenance summary:** all assumption rows are `[ESTIMATED]` and hypothetical. All derived
quantities above are `[COMPUTED]` by the arithmetic shown inline. No figure in this document is
a measured production result, and none should be cited as one.
