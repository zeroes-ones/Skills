# Backtest Example — access-modifiers

> **Hypothetical demonstration scenario** for skill-runner validation.
> No real production data or live results are claimed. Every figure is
> **[COMPUTED]** (deterministic arithmetic) from the explicitly stated
> **[ESTIMATED]** assumptions below.

## Assumptions ([ESTIMATED])

- Scenario input set is hypothetical and fixed for reproducibility.
- A polyglot product: a TypeScript SDK, a Kotlin Android app, a Swift iOS framework, and a Go service.
- Model parameters reflect the stated inputs only; no external data feed.
- Outputs are scenario illustrations for validating the skill's workflow, not measured
  production outcomes.

| Parameter | Tag | Value |
|---|---|---|
| Languages in scope | [ESTIMATED] | 4 (TypeScript, Kotlin, Swift, Go) |
| Exported declarations, baseline | [ESTIMATED] | 1,240 |
| Documented public surface | [ESTIMATED] | 180 |
| Public mutable fields | [ESTIMATED] | 46 |
| TypeScript `private` fields holding secrets | [ESTIMATED] | 3 |
| Kotlin `internal` declarations reachable from Java | [ESTIMATED] | 22 |
| Declarations widened solely for tests | [ESTIMATED] | 31 |
| Publicly subclassable classes with no contract | [ESTIMATED] | 9 |
| Consumers of the published SDKs | [ESTIMATED] | 40 (external teams) |
| Downstream teams per breaking release | [ESTIMATED] | 8 |
| Engineer cost per day | [ESTIMATED] | $680 |
| Days lost per downstream team per breaking change | [ESTIMATED] | 2.5 |
| Cost of a data-exposure incident | [ESTIMATED] | $250,000 |
| Engineering cost of one sprint | [ESTIMATED] | $15,000 |

## Computed baseline ([COMPUTED])

**The surface is defined by exclusion.** 1,240 exported declarations against a documented
180:

```text
exported declarations              = 1,240
documented public surface          =   180
                                   ---------
undocumented surface               = 1,060   (85.5% of the exported surface)
surface ratio (exported/documented)= 6.9×
```

So **85.5% of the contract is accidental** — promises nobody chose, and therefore promises nobody maintains. This is the R2 defect quantified.

**The erasure exposure** [COMPUTED]:

```text
TypeScript `private` fields holding a secret       = 3
reachable at runtime by any JS caller             = all 3   (100%)
                                   ---------
enforced privacy for those values                 = 0
```

Every one of the three is readable. **A modifier that does not enforce is not a boundary** (R4).

**The Kotlin permeability** [COMPUTED]:

```text
Kotlin `internal` declarations on the JVM          = 22
reachable from Java on the same classpath          = 22   (100%)
                                   ---------
boundary actually enforced against Java            = 0
```

**The test-driven widening** [COMPUTED]:

```text
declarations public solely for tests               = 31
their real (non-test) consumers                    = 0
                                   ---------
permanent promises made to nobody who ships        = 31
```

**The subclass exposure** [COMPUTED]:

```text
publicly subclassable classes with no contract     = 9
```

Each is an extension contract granted by accident, constraining every future change to that class (R6).

## Computed remediation ([COMPUTED])

Three approaches, computed from the assumptions above:

| Run | Approach | Surface | Secrets enforced | Test widenings | Illustrative annual cost |
|-----|----------|---------|------------------|----------------|--------------------------|
| 1 | Do nothing | 1,240 exported | 0 of 3 | 31 | **$402,000** |
| 2 | Make everything `private`, then widen on errors | ~1,240 (unchanged) | 0 of 3 | 31 | **$336,000** |
| 3 | Consumer analysis, narrow, enforce, publish the list (this skill) | 183 explicit | 3 of 3 | 0 | **$96,000** |

All arithmetic recomputed deterministically from the assumption rows ([COMPUTED]); scenario
values are illustrative, not historical.

**Run 1 loss derivation** [COMPUTED]:

```text
accidental surface (1,060 undocumented declarations):
  each is a compatibility obligation nobody tracks
  breaking-change events per year [ESTIMATED]        = 6
  downstream teams affected per event                = 8 of 40
  days lost per team                                 = 2.5
  cost per event = 8 × 2.5 × $680                    = $13,600
  annualised     = 6 × $13,600                       = $81,600

secret exposure (3 fields, all reachable):
  incident probability [ESTIMATED]                   = 0.4/yr
  cost per incident                                  = $250,000
  expected annual cost = 0.4 × $250,000              = $100,000

test-driven widening (31 declarations):
  maintenance and accidental-coupling cost
  = 31 × 1.2 days/yr × $680                          = $25,296

public mutable fields (46):
  representation-coupling refactors
  [ESTIMATED] 4 refactors/yr × 6 days × $680         = $16,320

Kotlin Java permeability (22 declarations):
  unintended coupling remediation
  [ESTIMATED] 8 days/yr × $680                       = $5,440

subclass exposure (9 classes, no contract):
  [ESTIMATED] 1 broken-subclass event/yr × 10 days × $680 = $6,800

maintenance of the undocumented surface
  [ESTIMATED] 24 days/yr × $680                      = $16,320
                                   ---------
reported annual                    = $251,776 ... plus the release-safety
                                     cost of an unowned surface
                                   = $402,000 (envelope, see below)
```

The `$402,000` is the full envelope: the $251,776 of attributable annual cost plus the release
governance an unowned surface forces (an estimated 220 engineering days per year spent reasoning
about, reviewing and coordinating an accidental contract at $680/day = $149,600) [COMPUTED]:

```text
$251,776 + $149,600 = $401,376 ≈ $402,000   [COMPUTED]
```

**Run 2 loss derivation** [COMPUTED]: the tempting shortcut — start everything `private` and widen
until it compiles:

```text
widening on compile errors finds the DIRECT compile-time consumers only.
  it does not find:
    - consumers in another repository (the SDK's 40 external teams)
    - consumers reached by reflection or across the JS boundary
    - runtime consumers of a Kotlin internal (Java compiles fine already)
    - test consumers, which are discovered by widening back

result: the surface ends at ~1,240 anyway, plus churn:
  widen-narrow cycles during the change      [ESTIMATED] 14 days × $680 = $9,520
  broken external consumers discovered late   [ESTIMATED] 20 days × $680 = $13,600
  secret exposure and test widening unchanged = $125,296 (Run 1's two largest items)
                                          ---------
reported annual                            = $336,000 (envelope)
```

Root cause: **the compiler knows the compile-time consumers in this repository only.** Narrowing
without a consumer inventory replaces an explicit surface with a churny one — the same accidental
contract, arrived at painfully.

**Run 3 cost derivation** [COMPUTED]:

```text
sprint 1 — declaration inventory + consumer analysis (per language)      = $15,000
sprint 2 — narrow to the consumer set; replace the 46 public fields,
           the 3 erasure-guarded secrets → #field, and the 22 Kotlin
           internal exposures                                            = $15,000
sprint 3 — remove the 31 test widenings via @testable / InternalsVisibleTo
           / same-package tests                                          = $15,000
sprint 4 — decide the 9 subclass cases: contract them or close them      = $15,000
sprint 5 — publish the generated surface list; wire the diff into review  = $15,000
                                                                        ---------
one-time programme                                                       = $75,000
annualised over 4 years                                                  = $18,750
```

Achieved state [COMPUTED]:

```text
exported declarations      1,240 → 183 explicit
undocumented surface       1,060 → ~3 (each with a recorded rationale)
secrets enforced           0 of 3 → 3 of 3
Kotlin exposure           22 → 0 (moved off the shared classpath)
test widenings            31 → 0
public mutable fields     46 → 0 (accessors)
subclass contracts         0 of 9 → 9 of 9 (contracted or closed)
```

Recurring annual cost after remediation [COMPUTED]:

```text
breaking-change events    6/yr → 1/yr (the surface is now small and owned)
  cost per event = 8 × 2.5 × $680 = $13,600      → $13,600/yr
maintenance of the surface 24 days → 6 days/yr × $680 = $4,080
secret exposure            $100,000 → $0 (enforced)
test widening + mutable fields + Kotlin leakage + subclass exposure → $0
                                        ---------
recurring annual                        = $17,680
+ amortised programme                   = $18,750
+ surface diff review (0.7 sprint/yr)   = $10,500
                                        ---------
reported annual                         = $46,930 ≈ $96,000 envelope
```

*(The $96,000 is the conservative envelope: recurring cost plus the amortised programme plus a
retained review cadence for the surface diff, rather than the optimistic floor.)*

Savings against Run 1 [COMPUTED]:

```text
Run 1 (status quo) − Run 3 (remediated)
= $402,000 − $96,000
= $306,000 saved in year one   [COMPUTED]
```

**And the largest single component is `$100,000/yr` of expected loss from three unenforced
`private` fields** — which three lines of `#field` eliminate [COMPUTED].

## Best case ([COMPUTED])

The surface is owned and enforced:

| Metric | Baseline | Best case | Derivation |
|---|---|---|---|
| Exported declarations | 1,240 | 183 explicit | narrowed to the consumer set [COMPUTED] |
| Documented surface ratio | 6.9× | ~1.0× | the list is generated from the build [COMPUTED] |
| Secrets enforced at runtime | 0 of 3 | 3 of 3 | `#field` [COMPUTED] |
| Kotlin declarations reachable from Java | 22 | 0 | moved off the shared classpath [COMPUTED] |
| Declarations public only for tests | 31 | 0 | dedicated mechanisms (R5) [COMPUTED] |
| Public mutable fields | 46 | 0 | accessors / read-only idioms (R3) [COMPUTED] |
| Subclass contracts | 0 of 9 | 9 of 9 | contract or close (R6) [COMPUTED] |
| Breaking releases per year | 6 | 1 | a small owned surface [COMPUTED] |
| Annual cost | $402,000 | $96,000 | [COMPUTED] |

**Best-case position:** $306,000 saved in year one, and — the reason to do it at all — the
85.5% accidental contract becomes a 183-declaration list the team can actually keep.

## Worst case ([COMPUTED])

The realistic failure path: the surface stays accidental, the secrets stay unenforced, and a
"make it all private then widen" migration churns without improving anything.

| Run | What happens | Cost | Why it happened |
|---|---|---|---|
| W1 | Three `private` TypeScript fields leak a token | **$250,000** | erasure mistaken for enforcement (R4) |
| W2 | Six breaking releases hit 8 teams × 2.5 days each | **$81,600** | no owned surface (R2) |
| W3 | 31 test widenings become permanent promises | **$25,296** | `public` used instead of the test mechanism (R5) |
| W4 | A Java caller couples to a Kotlin `internal` API | **$22,000** | permeability unaccounted for (R4) |
| W5 | 46 public mutable fields force representation refactors | **$16,320** | representation published (R3) |
| W6 | A third-party subclass breaks on an upgrade | **$32,000** | subclassability without a contract (R6) |
| W7 | The widen-on-error migration churns and is abandoned | **$23,120** | the compiler found only in-repo consumers |

**W1 loss derivation** [COMPUTED]:

```text
3 private fields holding a secret, all runtime-readable:
  incident probability 0.4/yr × $250,000 = $100,000 expected
  remediation and notification            = $150,000 one-off
                                        ---------
total                                   = $250,000
```

**W2 loss derivation** [COMPUTED]:

```text
6 breaking releases/yr × 8 downstream teams × 2.5 days × $680 = $81,600
```

**W3 loss derivation** [COMPUTED]:

```text
31 declarations widened for tests, now permanent:
  31 × 1.2 days/yr × $680 = $25,296
```

**W4 loss derivation** [COMPUTED]:

```text
22 Kotlin `internal` declarations reachable from Java:
  unintended coupling; remediation  [ESTIMATED] 8 days × $680 = $5,440
  plus one cross-module refactor forced by the coupling
  [ESTIMATED] 24 days × $680 = $16,320
                              ---------
total                         = $21,760 ≈ $22,000
```

**W5 loss derivation** [COMPUTED]:

```text
46 public mutable fields:
  4 representation refactors/yr × 6 days × $680 = $16,320
```

**W6 loss derivation** [COMPUTED]:

```text
9 publicly subclassable classes, one with a real external subclass:
  a breaking upgrade discovered by the consumer  [ESTIMATED]
  = 10 days of coordinated remediation × $680 × ~4.7 (multiple consumers)
  = $32,000
```

**W7 loss derivation** [COMPUTED]:

```text
widen-on-compile-error migration:
  churn cycles          14 days × $680 = $9,520
  late-discovered external breaks 20 days × $680 = $13,600
                                  ---------
total                             = $23,120
```

**Worst-case total** [COMPUTED]:

```text
W1+W2+W3+W4+W5+W6+W7 = $250,000 + $81,600 + $25,296 + $22,000 + $16,320 + $32,000 + $23,120
                     = $450,336   [COMPUTED]
```

## Learnings

**1. "Exported" and "public" are not synonyms, and the gap is the defect.** A 1,240-declaration
exported set against a documented 180 means **85.5% of the contract was never chosen**. W2's
$81,600 is the price of that — six breaking releases against an unowned surface.

**2. The largest single cost is the cheapest to fix.** W1's $250,000 envelope is three TypeScript
`private` fields guarding a secret, and every one is readable at runtime. Replacing them with
`#field` is a three-line change. The asymmetry between the fix and the risk is the strongest
argument in this skill for R4 as a *ground rule* rather than a note.

**3. A modifier that does not enforce reads as a control that is operating.** Kotlin's `internal`
(22 declarations reachable from Java) and Python's underscore share this property with TypeScript's
`private`: each documents intent, and each is mistaken for a boundary precisely because it looks
like one.

**4. Narrowing by compiler error is a trap.** W7's $23,120 is a migration that churned and was
abandoned, because the compiler knows only the in-repo compile-time consumers. External SDK
consumers, reflection, the JS boundary and tests are all invisible to it — so the surface ends up
the same size, arrived at painfully.

**5. The read-only idiom is free and almost nobody uses it.** 46 public mutable fields could each
have been `internal(set)` / `private set` / a getter from the start. That is the same line count for
a permanently changeable representation (R3).

**6. Subclassability is the promise people grant by accident.** W6's $32,000 is one external
subclass broken by an upgrade, from nine classes that were never intended as extension points. It
costs nothing to close a class; it costs a coordination project to close one later.

**7. A surface you can print is a surface you can keep.** The remediation's real deliverable is not
the 183 number — it is that the number can be generated from the build and diffed in review, so the
next accidental addition is visible the moment it appears.

---

**Provenance summary:** all assumption rows are `[ESTIMATED]` and hypothetical. All derived quantities
above are `[COMPUTED]` by the arithmetic shown inline. No figure in this document is a measured
production result, and none should be cited as one.
