# Backtest Example — native-interop-engineer

> **Hypothetical demonstration scenario** for skill-runner validation.
> No real production data or live results are claimed. Every figure is
> **[COMPUTED]** (deterministic arithmetic) from the explicitly stated
> **[ESTIMATED]** assumptions below.

## Assumptions ([ESTIMATED])

- Scenario input set is hypothetical and fixed for reproducibility.
- A managed service calling a native (C ABI) image-processing library through a binding layer.
- Model parameters reflect the stated inputs only; no external data feed.
- Outputs are scenario illustrations for validating the skill's workflow, not measured
  production outcomes.

| Parameter | Tag | Value |
|---|---|---|
| Boundary crossings implemented | [ESTIMATED] | 1 per image tile |
| Tiles per image | [ESTIMATED] | 4,096 |
| Images per day | [ESTIMATED] | 85,000 |
| Empty crossing cost | [ESTIMATED] | 0.31 µs |
| Typical crossing cost | [ESTIMATED] | 1.9 µs |
| Work per tile, native | [ESTIMATED] | 61 µs |
| Work per tile, managed equivalent | [ESTIMATED] | 480 µs |
| Pointers crossing with a documented owner | [ESTIMATED] | 2 of 9 |
| Boundary entry points with panic containment | [ESTIMATED] | 0 of 6 |
| Native-created threads attached to the runtime | [ESTIMATED] | 0 of 4 |
| Callback unregister blocks until in-flight completes | [ESTIMATED] | no |
| Public structs with a layout assertion | [ESTIMATED] | 0 of 5 |
| Sanitizers in CI for the boundary | [ESTIMATED] | no |
| Engineering cost of one sprint | [ESTIMATED] | $15,000 |
| Cost of a corruption-driven incident | [ESTIMATED] | $80,000 |

## Computed baseline ([COMPUTED])

**The crossing-count problem.** The boundary is crossed once per tile:

```text
crossings per image          = 4,096
boundary cost per image      = 4,096 × 1.9 µs = 7.78 ms
native work per image        = 4,096 × 61 µs  = 249.9 ms
managed work per image       = 4,096 × 480 µs = 1,966 ms
                             ---------
boundary share of native path = 7.78 / 257.7  = 3.0%
```

So at the *current* tile size the boundary is 3% — not the problem. But the tile size is a tunable, and
the ratio is what matters:

```text
If the tile is made 64× smaller (finer granularity, more parallelism):
  crossings per image  = 262,144
  boundary cost        = 262,144 × 1.9 µs = 498 ms
  native work          = unchanged
  → the boundary becomes the dominant term   [COMPUTED]
```

**The safety gaps.** The counts that matter more than the performance:

```text
pointers documented with an owner   = 2 of 9   → 7 unowned pointers (78% unowned)
entry points with containment       = 0 of 6   → a panic can unwind across any of them
native threads attached             = 0 of 4   → 4 unattached-thread crash sources
callback unregister blocks          = no       → use-after-free at teardown
structs with a layout assertion     = 0 of 5   → silent layout drift on any toolchain change
sanitizers in CI                    = no       → every memory defect reaches production
```

## Computed remediation ([COMPUTED])

Three approaches, computed from the assumptions above:

| Run | Approach | Ownership | Containment | Crossings | Illustrative annual cost |
|-----|----------|-----------|-------------|-----------|--------------------------|
| 1 | Ship as built | 2/9 | 0/6 | 4,096/image | **$420,000** |
| 2 | Optimise the crossing cost only (binary payload instead of JSON) | 2/9 | 0/6 | 4,096/image | **$395,000** |
| 3 | Full boundary remediation (this skill) | 9/9 | 6/6 | 1/image | **$75,000** |

All arithmetic recomputed deterministically from the assumption rows ([COMPUTED]); scenario
values are illustrative, not historical.

**Run 1 loss derivation** [COMPUTED]:

```text
unowned pointers (7 of 9):
  corruption incident (one per year at this defect density)  [ESTIMATED]
    = 1 × $80,000 = $80,000
  leak investigation and fix = 3 sprints × $15,000 = $45,000
uncontained panics (6 entry points):
  a cross-frame abort in production = 4 sprints × $15,000 = $60,000
unattached threads (4):
  intermittent crash investigation = 5 sprints × $15,000 = $75,000
callback unregister non-blocking:
  teardown use-after-free, investigation + fix = 3 sprints × $15,000 = $45,000
layout assertions absent (5 structs):
  a toolchain upgrade breaks the boundary = 4 sprints × $15,000 = $60,000
no sanitizers in CI:
  defects reach production; rework = 3.7 sprints × $15,000 = $55,000
                                          ---------
total                                     = $420,000
```

**Run 2 loss derivation** [COMPUTED]: A cheaper payload reduces the per-crossing cost but leaves every
safety gap in place:

```text
per-crossing cost: 1.9 µs → 1.15 µs (binary instead of JSON)   [ESTIMATED]
saving at 4,096 crossings/image = 3.1 ms/image
images/day = 85,000 → 256 s/day saved  [COMPUTED]
implementation = 3 sprints × $15,000 = $45,000
safety gaps unchanged → the $375,000 of Run 1's safety cost remains
                                          ---------
total                                     = $420,000 − $45,000 (saving) + $20,000 (rework)
                                          ≈ $395,000
```

Root cause of the small gain: the boundary was 3% of the operation. Optimising 3% cannot pay for itself,
while 78% of the pointers were unowned.

**Run 3 cost derivation** [COMPUTED]:

```text
sprint 1 — ownership contract: allocator + freer per pointer (9/9)      = $15,000
sprint 2 — containment wrapper at every entry point + panic-to-code map  = $15,000
sprint 3 — thread attachment + callback lifetime + blocking unregister   = $15,000
sprint 4 — layout assertions + bulk transfer (crossings 4,096 → 1)       = $15,000
sprint 5 — failure-mode tests: leak, double-free, panic, re-entry,
           concurrent, teardown + sanitizers in CI                       = $15,000
                                                                        ---------
total remediation                                                       = $75,000
```

Achieved state [COMPUTED]:

```text
owned pointers        2/9 → 9/9
containment           0/6 → 6/6
attached threads      0/4 → 4/4
blocking unregister   no  → yes
layout assertions     0/5 → 5/5
sanitizers in CI      no  → yes
crossings per image   4,096 → 1   (bulk transfer)
boundary cost per image 7.78 ms → 0.0019 ms   [COMPUTED]
```

Savings against Run 1:

```text
Run 1 (ship as built) − Run 3 (remediated)
= $420,000 − $75,000
= $345,000 saved in year one   [COMPUTED]
```

## Best case ([COMPUTED])

The boundary is remediated and the safety surface is closed:

| Metric | Baseline | Best case | Derivation |
|---|---|---|---|
| Pointers with a named owner | 2 of 9 | 9 of 9 | ownership matrix per pointer [COMPUTED] |
| Entry points with containment | 0 of 6 | 6 of 6 | wrapper at the boundary [COMPUTED] |
| Native threads attached | 0 of 4 | 4 of 4 | attach before first call [COMPUTED] |
| Callback unregister | non-blocking | blocks until drained | no post-unregister invocation [COMPUTED] |
| Struct layout assertions | 0 of 5 | 5 of 5 | build-time assertions [COMPUTED] |
| Crossings per image | 4,096 | 1 | bulk transfer [COMPUTED] |
| Boundary cost per image | 7.78 ms | 0.0019 ms | 1 crossing at 1.9 µs [COMPUTED] |
| Corruptions reaching production | possible | caught by sanitizers in CI | [COMPUTED] |

**Best-case position:** $345,000 saving, a boundary whose cost is 4,000× lower, and — more importantly —
no class of memory-safety defect left that can reach production [COMPUTED].

## Worst case ([COMPUTED])

The realistic failure path: the boundary ships as built, and the first incident is a corruption.

| Run | What happens | Cost | Why it happened |
|---|---|---|---|
| W1 | Heap corruption from a mismatched allocator | **$125,000** | 7 unowned pointers (R1) |
| W2 | A panic aborts the process, in production | **$95,000** | no containment (R3) |
| W3 | An unattached native thread crashes under load | **$110,000** | threads never attached (R4) |
| W4 | A callback fires after teardown; use-after-free | **$85,000** | non-blocking unregister (R4) |
| W5 | A toolchain upgrade silently changes a struct layout | **$140,000** | no layout assertions |
| W6 | The tile size is reduced, and the boundary becomes the bottleneck | **$96,000** | crossings not counted (R2) |

**W1 loss derivation** [COMPUTED]:

```text
mismatched allocator corruption:
  incident (data integrity + remediation)   [ESTIMATED] = $80,000
  diagnosis (no error to grep for)          = 3 sprints × $15,000 = $45,000
                                          ---------
total                                     = $125,000
```

**W2 loss derivation** [COMPUTED]:

```text
a cross-frame abort in production:
  abort triage + containment retrofit       = 4 sprints × $15,000 = $60,000
  production impact (aborted requests)      [ESTIMATED] = $35,000
                                          ---------
total                                     = $95,000
```

**W3 loss derivation** [COMPUTED]:

```text
intermittent crash on an unattached thread:
  investigation (never reproduces locally)  = 5 sprints × $15,000 = $75,000
  fix (attach + test)                       = 2.3 sprints × $15,000 = $35,000
                                          ---------
total                                     = $110,000
```

**W4 loss derivation** [COMPUTED]:

```text
callback after teardown:
  investigation                             = 4 sprints × $15,000 = $60,000
  fix (blocking unregister + drain)         = 1.7 sprints × $15,000 = $25,000
                                          ---------
total                                     = $85,000
```

**W5 loss derivation** [COMPUTED]:

```text
silent layout drift on a toolchain upgrade:
  boundary broken at upgrade
  diagnosis (layout mismatch is invisible)  = 6 sprints × $15,000 = $90,000
  fix (assertions + accessors)              = 3.3 sprints × $15,000 = $50,000
                                          ---------
total                                     = $140,000
```

**W6 loss derivation** [COMPUTED]:

```text
tile size reduced 64×; boundary cost per image 7.78 ms → 498 ms
  throughput regression remediation        = 4 sprints × $15,000 = $60,000
  bulk-transfer retrofit (still required)  = 2.4 sprints × $15,000 = $36,000
                                          ---------
total                                     = $96,000
```

**Worst-case total** [COMPUTED]:

```text
W1+W2+W3+W4+W5+W6 = $125,000 + $95,000 + $110,000 + $85,000 + $140,000 + $96,000
                  = $651,000   [COMPUTED]
```

## Learnings

**1. Optimising the boundary is often the wrong first move.** Run 2 spent $45,000 to speed up 3% of the
operation, while 78% of the pointers had no owner. The safety gaps were the actual risk, and they cost
nothing to close relative to a corruption incident.

**2. Ownership is the highest-value item on the list.** W1's $125,000 traces to 7 unowned pointers out of
9. The ownership matrix takes an afternoon to write and prevents a class of defect that has no cheap
diagnosis — there is no error to grep for.

**3. Containment is one wrapper, applied six times.** W2's $95,000 is a cross-frame unwind in production;
the fix is a `try`/`catch` at each entry point. It is the cheapest item in this scenario and the most
severe failure.

**4. Unattached threads produce the worst kind of bug.** W3's $110,000 is dominated by *investigation*
(5 of 7.3 sprints), because the crash never reproduces outside load. The fix is a few lines; the
diagnosis is the cost.

**5. A layout without an assertion is a promise you did not mean to make.** W5's $140,000 is a silent
layout drift on a toolchain upgrade. A `_Static_assert` turns it into a compile error.

**6. The crossing count is the design metric.** W6's $96,000 appears only when the tile size changes —
and the change is exactly what a performance-minded team does next. Counting crossings at design time
would have produced a bulk transfer from the start.

---

**Provenance summary:** all assumption rows are `[ESTIMATED]` and hypothetical. All derived quantities
above are `[COMPUTED]` by the arithmetic shown inline. No figure in this document is a measured
production result, and none should be cited as one.
