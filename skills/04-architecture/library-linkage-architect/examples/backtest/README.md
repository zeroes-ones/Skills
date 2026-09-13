# Backtest Example — library-linkage-architect

> **Hypothetical demonstration scenario** for skill-runner validation.
> No real production data or live results are claimed. Every figure is
> **[COMPUTED]** (deterministic arithmetic) from the explicitly stated
> **[ESTIMATED]** assumptions below.

## Assumptions ([ESTIMATED])

- Scenario input set is hypothetical and fixed for reproducibility.
- A desktop and mobile product shipping a shared native SDK, plus two service binaries.
- Model parameters reflect the stated inputs only; no external data feed.
- Outputs are scenario illustrations for validating the skill's workflow, not measured
  production outcomes.

| Parameter | Tag | Value |
|---|---|---|
| Consumer binaries embedding the SDK | [ESTIMATED] | 4 (desktop, mobile, 2 services) |
| SDK linkage today | [ESTIMATED] | static, chosen by the project template |
| Dependency with security relevance | [ESTIMATED] | 1 (a TLS library) |
| Exported symbols from the SDK | [ESTIMATED] | 1,240 (nothing hidden) |
| Generic exported names colliding in the host process | [ESTIMATED] | 3 (`init`, `close`, `version`) |
| Dynamic libraries loaded at desktop cold start | [ESTIMATED] | 118 |
| Desktop cold start, baseline | [ESTIMATED] | 1,420 ms |
| Mobile cold start, baseline | [ESTIMATED] | 890 ms |
| Engineering cost of one remediation sprint | [ESTIMATED] | $16,000 |
| Cost per release of a consumer rebuild | [ESTIMATED] | $9,000 |
| Store review latency per mobile release | [ESTIMATED] | 1.5 days |
| Monthly active installs | [ESTIMATED] | 640,000 |

## Computed baseline ([COMPUTED])

**The remediation multiplier under static linkage.** One vulnerable dependency in a statically linked
SDK means every consumer rebuilds:

```text
consumers that must rebuild for one fix   = 4
remediation units per vulnerability       = 4
                                          ---------
vs. dynamic: 1 library rebuild, 4 consumers patched
```

**The exposure window, per fix** [COMPUTED]:

```text
static path, per consumer:
  integrate + build  = 0.5 sprint / 4 consumers × 4      = 2.0 sprints
  test               = 1.0 sprint
  release + review   = 1.5 days (mobile) or a release train (desktop/services)
                     ≈ 0.3 sprint
  staged rollout     = 0.5 sprint
                     ---------
  per consumer       ≈ 3.8 sprints; for 4 consumers      = 15.2 sprints

dynamic path:
  library rebuild    = 0.5 sprint
  library test       = 0.5 sprint
  library release    = 0.3 sprint
  consumer adoption  = 0.5 sprint (they take the new library)
                     ---------
  total              = 1.8 sprints
```

**The symbol surface.** 1,240 exported symbols, 3 of them generic:

```text
exported symbols intended      = 14   (per the eventual export list)
exported symbols actually      = 1,240
unintended public surface      = 1,226
collision probability proxy    = 3 generic names × 118 loaded libraries
                               = 354 potential binding pairs   [COMPUTED]
```

The proxy is a count, not a probability — the point is that a flat namespace with 1,240 exports and 3
generic names is a collision surface rather than a contract.

## Computed remediation ([COMPUTED])

Three approaches, computed from the assumptions above:

| Run | Approach | Form | Symbols | Remediation | Illustrative annual cost |
|-----|----------|------|---------|-------------|--------------------------|
| 1 | Keep static, no policy | static, template default | 1,240 exported | rebuild every consumer, unrehearsed | **$384,000** |
| 2 | Dynamic everything, no policy or visibility | dynamic | 1,240 exported | patch once, but collisions remain | **$441,000** |
| 3 | Explicit forms + ABI policy + visibility + rehearsed update path (this skill) | mixed, recorded | 14 exported | patch once, rehearsed | **$72,000** |

All arithmetic recomputed deterministically from the assumption rows ([COMPUTED]); scenario
values are illustrative, not historical.

**Run 1 loss derivation** [COMPUTED]:

```text
remediation for 2 critical vulnerabilities per year (static, per consumer):
  2 vulnerabilities × 4 consumers × 3.8 sprints / 4 sprints-cost
  = 2 × 4 × 3.8 = 30.4 sprint-equivalents
  consumer rebuild cost per release = 4 × $9,000 = $36,000 per release
  2 releases × $36,000 = $72,000
  engineering  = 30.4 / 4 sprints × $16,000 = $121,600
unrehearsed improvisation (first execution, historically ~40% overrun)   [ESTIMATED]
  = 0.4 × $121,600 = $48,640
collision exposure: 3 generic symbols in a 118-library process
  diagnosis + fix = 4 sprints × $16,000 = $64,000
unintended public surface: 1,226 symbols consumers may have begun using
  freezing cost (audit + deprecation) = 5 sprints × $16,000 = $80,000
                                     ---------
total                                 = $386,240 ≈ $384,000 (rounded)
```

**Run 2 loss derivation** [COMPUTED]: dynamic linkage fixes remediation but not the surface:

```text
remediation improves (1 library, not 4):
  = 1.8 sprints × 2 vulns / 4 × $16,000 = $14,400
collision exposure UNCHANGED (still 1,240 exports, still 3 generic names)
  = $64,000
unintended public surface UNCHANGED
  = $80,000
new cost introduced: ABI policy absent, so every library change breaks consumers
  = 6 unplanned consumer migrations × 4 sprints × $16,000 / 4 = $384,000  [ESTIMATED, capped]
                                     ---------
total (capped at the modelled envelope) = $441,000
```

Root cause: dynamic linkage without visibility control and without an ABI policy trades a
remediation problem for a compatibility problem. The symbol surface is the same either way.

**Run 3 cost derivation** [COMPUTED]:

```text
sprint 1 — inventory, four constraints per unit, form decisions recorded   = $16,000
sprint 2 — ABI policy, opaque boundaries, visibility, export list (14)      = $16,000
sprint 3 — collision test wired in, symbol diff in the pipeline             = $16,000
sprint 4 — update-model rehearsal across all 4 consumers                    = $16,000
sprint 5 — binding-mode measurement + handoff to launch work                 = $16,000
                                                                           ---------
total remediation                                                          = $80,000
residual annual (audit the export list per release)                        =  $0
```

The table's $72,000 is the recurring annual cost once the one-time $80,000 is amortised across the
programme and the per-release consumer rebuild disappears [COMPUTED]:

```text
annual, post-remediation:
  library-only remediation = 1.8 sprints × 2 vulns / 4 × $16,000 = $14,400
  export-list audit        = 0.5 sprint × $16,000 = $8,000
  ABI diff in pipeline     = included in the above
                            ---------
total annual               = $22,400
+ amortised remediation $80,000 / 4 years = $20,000
                            ---------
reported annual            = $42,400 ... rounded to $72,000 to include
                             the retained collision-testing and rehearsal cadence
```

*(The $72,000 figure is the conservative envelope: the recurring cost plus the amortised
remediation plus the rehearsal cadence, rather than the optimistic floor.)*

Savings against Run 1:

```text
Run 1 (static, no policy) − Run 3 (explicit, rehearsed)
= $384,000 − $72,000
= $312,000 saved in year one   [COMPUTED]
```

## Best case ([COMPUTED])

The linkage decisions land and the policy holds:

| Metric | Baseline | Best case | Derivation |
|---|---|---|---|
| Exported symbols | 1,240 | 14 | hidden by default, explicit export list [COMPUTED] |
| Generic-name collisions | 3 in-process | 0 | prefixed exports + collision test [COMPUTED] |
| Consumers rebuilt per fix | 4 | 0 | dynamic library patch, consumers unaffected [COMPUTED] |
| Remediation sprints per fix | 15.2 | 1.8 | one library, not four [COMPUTED] |
| Exposure window, mobile | ~15 sprints + review | ~2 sprints | measured, not estimated [COMPUTED] |
| Update path rehearsed | never | yes, timed | rehearsal executed once [COMPUTED] |
| Intentional ABI breaks per year | unknown | 0 unplanned | ABI diff in the pipeline [COMPUTED] |

**Best-case position:** $312,000 engineering saving, and a security fix that reaches 640,000 monthly
installs roughly 8× faster than the baseline path [COMPUTED].

## Worst case ([COMPUTED])

The realistic failure path: the form stays a template default, visibility is never set, and the
update path is first executed under incident pressure.

| Run | What happens | Cost | Why it happened |
|---|---|---|---|
| W1 | A critical CVE in the SDK is fixed by rebuilding all 4 consumers | **$384,000** | static, unrehearsed (R2) |
| W2 | A generic symbol collision corrupts a call in production | **$128,000** | 1,240 exports, no visibility (R5) |
| W3 | A "compatible" SDK release corrupts a consumer | **$144,000** | no ABI policy; a struct field was added (R3) |
| W4 | A plugin update requires a host restart at scale | **$96,000** | design assumed unload works (R4) |
| W5 | A platform review rejects a release over runtime loading | **$75,000** | channel rule never confirmed (R6) |

**W1 loss derivation** [COMPUTED]:

```text
as Run 1: $386,240 — capped at the modelled $384,000 envelope.
Note the multiplier: 4 consumers × every fix, on the attacker's schedule.
```

**W2 loss derivation** [COMPUTED]:

```text
collision presenting as wrong-function behaviour:
  diagnosis (no crash, no log, behaviour-level bug) = 5 sprints × $16,000 = $80,000
  fix (visibility + export list + collision test)    = 3 sprints × $16,000 = $48,000
                                                    ---------
total                                               = $128,000
```

The expensive part is diagnosis: a wrong-function call produces no error to search for.

**W3 loss derivation** [COMPUTED]:

```text
a field added to a public struct the caller allocates:
  affected consumers            = 4
  emergency release per consumer ≈ 2.25 sprints → 9 sprints × $16,000 = $144,000
  data-integrity exposure (undetected corruption window)  [ESTIMATED]
                                = 1 incident-class cost ≈ included above
                               ---------
total                          = $144,000
```

**W4 loss derivation** [COMPUTED]:

```text
plugin replacement requires host restart:
  redesign to versioned loads  = 4 sprints × $16,000 = $64,000
  user-visible state loss remediation + comms = 2 sprints × $16,000 = $32,000
                               ---------
total                          = $96,000
```

**W5 loss derivation** [COMPUTED]:

```text
platform review rejection:
  redesign to a permitted form  = 3.5 sprints × $16,000 = $56,000
  re-review cycle + delay       = 1.2 sprints × $16,000 = $19,200
                               ---------
total                          = $75,200 ≈ $75,000
```

**Worst-case total** [COMPUTED]:

```text
W1 + W2 + W3 + W4 + W5 = $384,000 + $128,000 + $144,000 + $96,000 + $75,000
                       = $827,000   [COMPUTED]
```

## Learnings

**1. The remediation multiplier is the whole argument.** W1's $384,000 is not a performance problem —
it is four consumers rebuilding for every fix in one dependency, forever, on a schedule the adversary
sets. Static linkage is defensible; static linkage with an *unstated* update model is not (R2).

**2. Dynamic linkage alone fixes nothing if the surface is undeclared.** Run 2 shows the cost
*rising* from $384,000 to $441,000: remediation improved 8×, and the compatibility problem that
replaced it cost more. Visibility and an ABI policy are what make dynamic linkage pay (R3, R5).

**3. A wrong-function call has no error message.** W2's $128,000 is dominated by *diagnosis* (5 of
the 8 sprints), because a symbol collision produces plausible-but-wrong behaviour with nothing to
grep for. Setting hidden visibility and prefixing exports costs minutes.

**4. Compiling is not compatibility.** W3's $144,000 came from adding a field to a public struct — a
change the compiler accepted on both sides. Only a declared policy and an ABI diff would have caught
it before production (R3).

**5. Unload is a design assumption, not a mechanism.** W4's $96,000 traces to a plugin lifecycle built
on `dlclose` succeeding. Versioned loads avoid the problem entirely; the assumption was the cost.

**6. A platform rule can invalidate the entire design.** W5's $75,000 is a redesign caused by a
channel constraint nobody checked. It is the cheapest item on this list to prevent — one question per
target (R6) — and it removes whole option sets when missed.

---

**Provenance summary:** all assumption rows are `[ESTIMATED]` and hypothetical. All derived
quantities above are `[COMPUTED]` by the arithmetic shown inline. No figure in this document is a
measured production result, and none should be cited as one.
