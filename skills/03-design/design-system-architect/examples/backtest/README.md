# Backtest Example — design-system-architect

> **Hypothetical demonstration scenario** for skill-runner validation.
> No real production data or live results are claimed. Every figure is
> **[COMPUTED]** (deterministic arithmetic) from the explicitly stated
> **[ESTIMATED]** assumptions below.

## Assumptions ([ESTIMATED])

* Scenario input set is hypothetical and fixed for reproducibility.
* A two-platform consumer product (one native mobile platform, one other) sharing a token source,
  with three hand-written design documents and one generated one.
* Model parameters reflect the stated inputs only; no external data feed.
* Outputs are scenario illustrations for validating the skill's workflow, not measured
  production outcomes.

| Parameter | Value | Tag |
|---|---|---|
| Screens reading a raw primitive swatch | 8 | [ESTIMATED] |
| Controls rendering divergent sizes across the two platforms | 8 | [ESTIMATED] |
| Hand-written design documents restating token values | 3 | [ESTIMATED] |
| Distinct hardcoded design values in screens | 47 | [ESTIMATED] |
| Shipping releases per year | 4 | [ESTIMATED] |
| Support tickets per design-defect class per year | 6 | [ESTIMATED] |
| Cost per support ticket | $1,200 | [ESTIMATED] |
| Loaded engineering cost per sprint (10 working days) | $12,000 | [ESTIMATED] |
| Expected shippings per year of a raw-primitive (light-mode-unreadable) release | 0.5 | [ESTIMATED] |
| Cost of one unreadable-appearance release (hotfix, store delay, re-audit) | $18,000 | [ESTIMATED] |
| Expected shippings per year of a control below its platform floor | 0.25 | [ESTIMATED] |
| Cost of one below-floor ship (audit, remediation, release review) | $24,000 | [ESTIMATED] |

## Computed baseline ([COMPUTED])

**Run 1 — do nothing: keep the ad-hoc system.**

```text
raw-primitive screen migration    = 8 files × 0.5 day   =  4 days = 0.4 sprint
cross-platform divergence fix     = 8 controls × 0.75 d =  6 days = 0.6 sprint
stale-doc wrong implementations   = 4 releases × 1.5 d  =  6 days = 0.6 sprint
below-floor accessibility re-audit= 3 days              =  3 days = 0.3 sprint
                                                    ----------------
sprint-equivalent rework                            =  1.9 sprints = $22,800
design-defect support tickets       = 6 × $1,200                     =  $7,200
                                                    ----------------
recurring annual run-rate                                           = $30,000

expected tail cost (undetected defects that ship):
  unreadable-appearance release     = 0.5  × $18,000                =  $9,000
  below-floor hit target            = 0.25 × $24,000                =  $6,000
                                                    ----------------
expected tail                                                       = $15,000

Run 1 annual cost = $30,000 + $15,000                                = $45,000
```

The tail term is the part a run-rate model misses: neither defect class is visible to the compiler,
the test suite, or a reviewer's own device, so their expected cost is incurred rather than zero.

## Computed remediation ([COMPUTED])

Three approaches, computed from the assumptions above:

| Run | Approach | Tiers | Cross-platform | Docs | Illustrative year-one cost |
|-----|----------|-------|----------------|------|----------------------------|
| 1 | Do nothing | mixed; screens reach primitives | one vocabulary per platform | 3 hand-written, 1 generated | **$45,000** |
| 2 | Restyle, no system | unchanged | divergence widens | unchanged | **$72,600** |
| 3 | This skill | three tiers, roles only | one role vocabulary, rank-asserted | generated, drift-gated | **$27,600** |

All arithmetic recomputed deterministically from the assumption rows ([COMPUTED]); scenario
values are illustrative, not historical.

**Run 2 loss derivation** [COMPUTED] — restyling without a system keeps the ad-hoc structure and
widens it:

```text
hardcoded values      = 47 → 59   (+12 new values added per screen)
new divergences       = 4 controls × 0.75 day = 3 days = 0.3 sprint       =  $3,600
convergence sprints   = 2 sprints × $12,000                               = $24,000
Run 1 baseline                                                            = $45,000
                                                    ----------------
Run 2 = $45,000 + $24,000 + $3,600                                        = $72,600
```

Root cause: the restyle adds values without removing the reason they multiply. The documentation is
still hand-written, so it is one release further out of date, and the cross-platform divergence grows
because four more controls now have a size only one platform's author chose.

**Run 3 cost derivation** [COMPUTED]:

```text
sprint 1 — token source, tier assignment, role vocabulary, per-platform
           resolution, rank assertion                    = 1.0 sprint = $12,000
sprint 2 — generator + drift gate (0.5), conformance gates
           + firing proofs (0.5)                          = 1.0 sprint = $12,000
                                                    ----------------
one-time remediation                                              = $24,000
residual ongoing (token maintenance + gate triage)                =  $3,600 / yr
                                                    ----------------
year one                                                          = $27,600
steady state                                                      =  $3,600 / yr
```

Savings against Run 1:

```text
year one        = $45,000 − $27,600 = $17,400
steady state    = $45,000 −  $3,600 = $41,400 per year
```

## Best case ([COMPUTED])

The system lands in one pass, every gate reads its vocabulary from the generated artifact on the
first attempt, and every firing proof succeeds immediately.

| Metric | Baseline | Best case | Derivation |
|---|---|---|---|
| Tiers | mixed; primitives reachable from screens | three, screens read roles only | one writable source, one role vocabulary [COMPUTED] |
| Cross-platform divergence | 8 controls | 0 outside tolerance | one role per control, rank-asserted [COMPUTED] |
| Hand-written design documents | 3 | 0 | each converted to a rendering of the source [COMPUTED] |
| Design-defect tickets | 6 / yr | 1 / yr | the gates catch the class before it ships [COMPUTED] |
| One-time remediation | — | $18,000 | 1.5 sprints instead of 2 [COMPUTED] |
| Residual ongoing | — | $2,400 / yr | smaller triage load [COMPUTED] |
| Year-one cost | $45,000 | **$20,400** | $18,000 + $2,400 [COMPUTED] |

**Best-case net position:** $24,600 saved in year one, and the two tail defect classes fall to
near-zero expected cost because a gate is watching the class that had no signal.

## Worst case ([COMPUTED])

The realistic failure path: the work is scoped as "add a tokens file", the tiers are not separated,
and the gate is built in a way that reports everything.

| Run | What happens | Cost | Why it happened |
|---|---|---|---|
| W1 | Tokenise everything, no tiers | **$63,000** | screens still read primitives; docs still hand-written |
| W2 | One severity for the colour gate; 80 findings; gate switched off | **$69,000** | the gate exists, catches nothing, and manufactures confidence |
| W3 | Unify the floors into one hit-target token | **$24,000** | one platform ships below its own published minimum |
| W4 | Commit the generated target, never prove the drift gate fires | **$30,000** | a release ships a stale generated artifact |

**W1 loss derivation** [COMPUTED]:

```text
tokenisation work (centralise 47 values, no tier separation)  = 1.5 sprints = $18,000
Run 1 annual cost unchanged (screens still reach primitives)                = $45,000
                                                    ----------------
W1 = $18,000 + $45,000                                                      = $63,000
```

The work is real and buys nothing: centralising values without separating tiers leaves the
primitive reachable, which is the only property that mattered.

**W2 loss derivation** [COMPUTED]:

```text
build the gate with one severity                = 2 sprints = $24,000
gate produces 80 findings, mostly legitimate scrims and overlays
gate switched off after two releases; the defect classes it covered are unmitigated
Run 1 annual cost returns in full                            = $45,000
                                                    ----------------
W2 = $24,000 + $45,000                                       = $69,000
```

W2 is the most expensive outcome in the table, and the one that looks the most successful: a
conformance gate exists, and its clean report is read as coverage.

**W3 loss derivation** [COMPUTED]:

```text
one floor token applied to both platforms
one platform ships a hit area below its published minimum
accessibility audit + remediation + release review
  = 2 sprints                                                       = $24,000
                                                    ----------------
W3                                                                  = $24,000
```

The saving that produced it was one token.

**W4 loss derivation** [COMPUTED]:

```text
generated target committed but never consumed or checked
a release ships a stale target; the divergence is found by a user
diagnosis + hotfix                          = 2 sprints = $24,000
support tickets for the release                          =  $6,000
                                                    ----------------
W4                                                       = $30,000
```

The drift gate existed from day one; it had simply never been shown reporting drift, so its clean
run proved nothing.

## Learnings ([COMPUTED] from the scenario, not measured)

1. **The tier separation is the whole value, not the centralisation.** W1 costs $63,000 and changes
   nothing, because a centralised value that a screen can still reach directly is the same defect
   with a nicer file.
2. **A gate that reports everything is the most expensive outcome available (W2).** Its cost exceeds
   doing nothing, because it is paid for *and* it removes the pressure to look.
3. **The tail terms dominate the run rate.** $15,000 of the $45,000 baseline is expected cost from
   defect classes that no compiler, test, or reviewer sees — which is precisely why those classes
   need a signal rather than a habit.
4. **One token can cost $24,000 (W3).** Unifying two published accessibility floors looks like
   tidiness and is a decision to under-serve one platform.
5. **A drift gate that has never fired is decoration (W4).** The firing demonstration is not
   ceremony; it is the only evidence the check is connected to anything.
6. **The steady-state return ($41,400/yr) is larger than the year-one return ($17,400).** The
   one-time remediation is the cost of entry, and the recurring value is that the design system stops
   being a document and becomes a property of the build.

## What this scenario does not claim

The figures are engineering-cost arithmetic from stated assumptions. No revenue, conversion, or
retention effect is included, because those are business estimates rather than engineering costs —
and including them would make the comparison look stronger for reasons the arithmetic does not
support. The two platforms are described generically; the platform floors, text styles, and vendor
slots named in the skill's references must be confirmed against the installed SDKs before use.
