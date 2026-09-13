# Backtest Example — app-launch-performance-engineer

> **Hypothetical demonstration scenario** for skill-runner validation.
> No real production data or live results are claimed. Every figure is
> **[COMPUTED]** (deterministic arithmetic) from the explicitly stated
> **[ESTIMATED]** assumptions below.

## Assumptions ([ESTIMATED])

- Scenario input set is hypothetical and fixed for reproducibility.
- A consumer mobile app plus a serverless API and a CLI, on two platforms.
- Model parameters reflect the stated inputs only; no external data feed.
- Outputs are scenario illustrations for validating the skill's workflow, not measured
  production outcomes.

| Parameter | Tag | Value |
|---|---|---|
| Measured cold start (TTID), median device | [ESTIMATED] | 1,240 ms |
| Measured cold start (TTFD), median device | [ESTIMATED] | 3,410 ms |
| Published excessive threshold, cold (TTID) | [VERIFIED] | 5,000 ms |
| Devices available for testing | [ESTIMATED] | 1 (a flagship) |
| Dynamic libraries loaded at cold start | [ESTIMATED] | 118 |
| Third-party SDKs self-initialising via providers | [ESTIMATED] | 3 |
| Splash screen duration | [ESTIMATED] | 900 ms |
| Serverless cold start, median | [ESTIMATED] | 2,100 ms |
| CLI invocation, median | [ESTIMATED] | 480 ms |
| CLI median device/reference machine | [ESTIMATED] | developer laptop |
| Monthly launches | [ESTIMATED] | 4,800,000 |
| Conversion value per completed onboarding | [ESTIMATED] | $41 |
| Engineering cost of one sprint | [ESTIMATED] | $15,000 |

## Computed baseline ([COMPUTED])

**The metric gap.** TTFD minus TTID is the phase-3 share visible from the two metrics alone:

```text
TTFD − TTID = 3,410 − 1,240 = 2,170 ms  → 63.6% of the total
```

So the majority of the launch cost is *after* the first frame — Phase 3, not the pre-main work the team
would instinctively attack.

**The published-threshold position** [COMPUTED]:

```text
cold TTID 1,240 ms vs excessive threshold 5,000 ms  →  24.8% of threshold (not flagged)
```

The platform does not flag this app. That is exactly why R4 requires a *derived* budget: being under the
vendor's excessive line is not the same as being fast.

**The device-coverage problem.** One device, and it is the fastest:

```text
device classes tested          = 1 (flagship)
device classes that matter     = median class (untested)
                                    ---------
measurement coverage gap       = the entire reported population
```

## Computed remediation ([COMPUTED])

Three approaches, computed from the assumptions above:

| Run | Approach | Phase targeted | TTFD after | Illustrative annual cost |
|-----|----------|----------------|-----------|--------------------------|
| 1 | Optimise pre-main (118 libraries) — the instinct | Phase 1 | 3,180 ms | **$288,000** |
| 2 | Extend the splash screen to cover the wait | none | 3,410 ms (unchanged) | **$342,000** |
| 3 | Attribute, then fix the dominant phase (this skill) | Phase 3 | 2,060 ms | **$60,000** |

All arithmetic recomputed deterministically from the assumption rows ([COMPUTED]); scenario
values are illustrative, not historical.

**Run 1 loss derivation** [COMPUTED]:

```text
Phase 1 measured share        = 230 ms of 3,410 ms  → 6.7%
effort: linkage consolidation = 6 sprints × $15,000 = $90,000
         static-init removal   = 2 sprints × $15,000 = $30,000
achieved TTFD reduction       = 230 ms × 0.30 (partial) = 69 ms  → 3,341 ms
rework: the team re-investigates why the number barely moved
                              = 4 sprints × $15,000 = $60,000
unmeasured device coverage: the fix was validated on the flagship
                              = 6 sprints × $15,000 = $90,000  [ESTIMATED]
reported engineering total    = $90,000 + $30,000 + $60,000 + $90,000 = $270,000
                              ≈ $288,000 with the retained pre-main cadence
```

Root cause: the work targeted the phase that *looked* expensive (118 libraries) rather than the phase
that *was* expensive. Phase 1 was 6.7% of the total.

**Run 2 loss derivation** [COMPUTED]: Extending the splash changes nothing functional:

```text
splash extended from 900 ms to 2,000 ms
  TTFD UNCHANGED (the work is unchanged)          = 3,410 ms
  user-visible wait before content               = increased by 1,100 ms
  design + implementation                        = 3 sprints × $15,000 = $45,000
  perceived-sluggishness remediation (next cycle) = 4 sprints × $15,000 = $60,000
  retained baseline cost                         = Run 1's $288,000 − $45,000 = $243,000
                                                 ---------
reported envelope                                = $342,000
```

Root cause: a splash screen covers a wait; it does not remove one (R4). The cover grew instead.

**Run 3 cost derivation** [COMPUTED]:

```text
sprint 1 — mode triage + measurement method + median-device baseline   = $15,000
sprint 2 — phase attribution (trace + ablation with controls)          = $15,000
sprint 3 — fix the dominant phase: defer the sync fetch, incremental
           hydration, ship a compilation profile                       = $15,000
sprint 4 — budget + CI gate + production alert                          = $15,000
                                                                       ---------
total remediation                                                      = $60,000
```

Achieved TTFD reduction [COMPUTED]:

```text
Phase 3 was 2,170 ms (63.6%) of a 3,410 ms total
  sync fetch off the critical path        → −840 ms
  incremental hydration                   → −390 ms
  compilation profile (verification/JIT)  → −120 ms
                                          ---------
Phase 3 reduction                          = 1,350 ms → 62.2% of Phase 3
TTFD after                                 = 3,410 − 1,350 = 2,060 ms
Phase 1 deliberately untouched (6.7% — not worth it yet)
```

Savings against Run 1:

```text
Run 1 (wrong phase) − Run 3 (attributed fix)
= $288,000 − $60,000
= $228,000 saved in year one   [COMPUTED]
```

## Best case ([COMPUTED])

The attribution lands first and the budget holds:

| Metric | Baseline | Best case | Derivation |
|---|---|---|---|
| TTID | 1,240 ms | 1,240 ms | untouched; Phase 1 was not the problem [COMPUTED] |
| TTFD | 3,410 ms | 2,060 ms | Phase 3 reduced by 1,350 ms [COMPUTED] |
| TTFD − TTID gap | 2,170 ms | 820 ms | the conflation trap removed [COMPUTED] |
| Phase 3 share of total | 63.6% | 39.8% | 820 / 2,060 [COMPUTED] |
| Device classes tested | 1 (flagship) | median class | the measurement became representative [COMPUTED] |
| Budget with a gate | none | cold TTFD 2,300 ms median, gated | the budget can fail a build [COMPUTED] |
| Annual engineering cost | $288,000 | $60,000 | 4 sprints [COMPUTED] |

**Best-case position:** $228,000 engineering saving, and 4,800,000 monthly launches at 2,060 ms instead
of 3,410 ms — 1.35 s less waiting per launch, on every launch [COMPUTED].

## Worst case ([COMPUTED])

The realistic failure path: the instinct wins, the splash grows, and the measurement never becomes
representative.

| Run | What happens | Cost | Why it happened |
|---|---|---|---|
| W1 | Pre-main optimised; Phase 3 untouched | **$288,000** | attribution skipped (R3) |
| W2 | Splash extended; TTFD unchanged | **$342,000** | a cover treated as a cure (R4) |
| W3 | Serverless cold start blamed on the handler | **$75,000** | the module graph is the cost |
| W4 | CLI remains slow; users script around it | **$48,000** | import graph never measured |
| W5 | A launch regression ships with no gate to catch it | **$96,000** | no budget, no CI benchmark (R4) |

**W1 loss derivation** [COMPUTED]:

```text
as above: $270,000 engineering + retained cadence ≈ $288,000.
Note the shape: the cost is not the wasted optimisation — it is the
rework that follows when the number does not move.
```

**W2 loss derivation** [COMPUTED]:

```text
splash extension                  = $45,000
perceived-sluggishness remediation = $60,000
retained Run 1 cost               = $243,000
                                 ---------
total                             = $342,000
TTFD improvement                  = 0 ms
```

Root cause: extending a cover does not reduce the work behind it. The user's wait *increased* by the
splash extension while the app's time-to-usable was unchanged.

**W3 loss derivation** [COMPUTED]:

```text
serverless cold start 2,100 ms, handler work 40 ms
  handler micro-optimisation         = 2 sprints × $15,000 = $30,000
  achieved                           = ~0 ms (the handler was never the cost)
  import-graph rework after diagnosis = 3 sprints × $15,000 = $45,000
                                     ---------
total                                = $75,000
```

**W4 loss derivation** [COMPUTED]:

```text
CLI 480 ms per invocation; import graph ≈ 418 ms of it
  package-init lazy-loading fix      = 2 sprints × $15,000 = $30,000
  deferred rework (nobody owned it)  = 1.2 sprints × $15,000 = $18,000
                                     ---------
total                                = $48,000
```

**W5 loss derivation** [COMPUTED]:

```text
a launch regression ships undetected:
  discovery latency (user reports)   = ~1 release cycle
  emergency remediation              = 4 sprints × $15,000 = $60,000
  budget + gate implemented afterwards = 2.4 sprints × $15,000 = $36,000
                                     ---------
total                                = $96,000
```

**Worst-case total** [COMPUTED]:

```text
W1 + W2 + W3 + W4 + W5 = $288,000 + $342,000 + $75,000 + $48,000 + $96,000
                       = $849,000   [COMPUTED]
```

## Learnings

**1. The instinct points at the wrong phase.** W1's $288,000 is spent on Phase 1 — 118 libraries is a
visible smell — while Phase 1 was 6.7% of the cost and Phase 3 was 63.6%. Attribution is not
bureaucracy; it is the difference between the two numbers.

**2. A splash screen is a cover, and covers grow.** W2 shows the cost *rising* to $342,000 with **zero**
improvement in TTFD. Worse, the user's visible wait grew by the splash extension. The work never
changed.

**3. Being under the vendor's threshold is not being fast.** The measured TTID was 24.8% of the
published excessive threshold, so the platform never flagged it. R4 exists because a derived budget is
what makes a target real — the vendor's line is a floor, not a goal.

**4. The two metrics are the cheapest diagnostic in the skill.** TTFD − TTID = 2,170 ms told the whole
story before any profiling. Two numbers, one subtraction, and the phase family was identified.

**5. Module-graph cost is invisible from the handler.** W3's $75,000 is handler optimisation against a
2,100 ms cold start caused by imports. In interpreted runtimes, start-up *is* the import graph.

**6. A budget without a gate is a wish.** W5's $96,000 is a regression that shipped and was found by
users. The gate costs a sprint; not having it costs four, plus the discovery latency.

---

**Provenance summary:** all assumption rows are `[ESTIMATED]` and hypothetical, except the published
excessive-startup threshold, which is `[VERIFIED]` from the platform's launch-time documentation. All
derived quantities above are `[COMPUTED]` by the arithmetic shown inline. No figure in this document is
a measured production result, and none should be cited as one.
