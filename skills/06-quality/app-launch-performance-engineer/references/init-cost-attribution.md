# Init-Cost Attribution

<!-- DEEP: 5+min -- the phase model: pre-main, first-frame, to-interactive -->

## Why attribution is a ground rule

A total launch time tells you the size of the problem and nothing about its cause. R3 exists because
every launch investigation that skips attribution eventually fixes the wrong thing — and because the
largest term is usually in code that runs *before* the app's own instrumentation can see it.

The phase model below is the working instrument. Attribute every launch cost to exactly one phase,
and any residual stated explicitly.

## The phase model

```
t_process_start ─────────────────────────────────────────────────────────▶ t_interactive

  ├── PHASE 1: PRE-MAIN ─────────┤
  │   process creation            │
  │   loader work                 │   ← linkage, library count
  │   relocations / binding       │   ← binding mode
  │   static initializers         │   ← the app's and its dependencies'
  │   framework / runtime init    │   ← framework choice and version
  │   system-service wait         │   ← platform, partly outside control
  ├── PHASE 2: FIRST FRAME ───────┤
  │   root layout / composition   │   ← hierarchy depth and complexity
  │   theme & asset inflation     │   ← initial theme, bundled assets
  │   blocking data on the path   │   ← sync fetch before render
  │   → TTID here                │
  ├── PHASE 3: TO-INTERACTIVE ────┤
  │   deferred main-thread work   │   ← post-frame work not moved off-thread
  │   state hydration            │   ← synchronous rehydration
  │   code verification / JIT     │   ← no compilation profile
  │   → TTFD here                │
  └───────────────────────────────┘
```

**Phase 1 is the one that hides.** It runs before `main`, so the app's own instrumentation cannot
measure it from inside the app; you need a loader-level trace or an ablation.

## Attribution methods, ranked by effort

| Method | What it gives | Effort | When to use |
|---|---|---|---|
| **Phase trace from the platform profiler** | a per-phase breakdown with timings | low-medium | whenever the platform provides one — start here |
| **Ablation (remove and re-measure)** | the true cost of a component, in situ | medium | when no trace exists, or when the trace is ambiguous |
| **Instrumentation of the app's own init** | the app's controllable share | low | always, alongside one of the above |
| **Static inspection** (counting initializers, libraries, providers) | a candidate list, not a measurement | very low | to build the ablation list |
| **A loader statistics dump** | relocations, resolutions, library count | low | for Phase 1 specifically |

### Ablation, done properly

Ablation is the most reliable method when a trace is unavailable, and it is easy to do wrong.

```text
For each candidate in the static-inspection list:
  1. Measure the current cold start (median of ≥10 runs) — the control.
  2. Remove or defer exactly ONE candidate.
  3. Measure again with the identical method.
  4. Record the delta.
  5. Restore, and verify the control is reproduced (the device may have changed).
Keep the method constant throughout (R5), and re-run the control periodically to catch drift.
```

**The discipline that makes it work:** one change at a time, and the control re-measured. Ablation
without a control attributes device warm-up and background load to the component you removed.

### Attributing Phase 2 with the right lever

| Symptom | Attribute to | Measure by |
|---|---|---|
| First frame late, process start fast | root layout / theme / assets | a trace of the first frame's work |
| A long block before anything renders | blocking data or synchronous work | the trace's pre-frame segment |

### Attributing Phase 3 with the right lever

| Symptom | Attribute to | Measure by |
|---|---|---|
| First frame fast, interaction dead | deferred main-thread work | main-thread trace after first frame |
| Interaction blocked by a specific feature | hydration of that feature | disable and re-measure that feature |
| Gradual improvement after launch | JIT/verification warm-up | compare a first run to a second |
| Slow on first run only, fast after | profile-guided compilation absent | ship a profile and compare |

## The residual

Phases will not sum exactly to the total. The honest treatment:

```text
measured total                = 1,420 ms
sum of attributed phases      = 1,180 ms
unattributed residual         =   240 ms (16.9%)

State the residual. Do NOT distribute it across phases to make the numbers tidy —
 that fabricates attribution and produces a plan aimed at nothing.
```

A large residual usually means: a phase was missed (system-service wait is common), the trace's
granularity is too coarse, or the measurement noise is larger than assumed.

## Reading the attribution to a fix

| Attribution result | The family of fixes |
|---|---|
| Phase 1 dominates | fewer libraries, fewer initializers, deferred init, linkage change |
| Phase 2 dominates | simplify root layout, defer data, trim the initial theme |
| Phase 3 dominates | move work off the main thread, sequence it later, ship a compilation profile |
| Phase 1+2 large, Phase 3 small | this is a genuine init problem; the linkage and init work applies |
| Phase 1 small, Phase 2+3 large | the linkage is fine; this is application structure — do not touch the linkage |

The last two rows are why attribution comes before the fix. The instinct after a slow launch is to
look at linkage and dependencies, and that is right only about half the time.

## Worked example

```
Cold start, median device, 20 runs, cache cleared.

Total (TTFD)             3,410 ms
TTID                     1,240 ms

Phase 1 (pre-main)         890 ms   26.1%   ← 118 libraries, 6 static initializers
Phase 2 (first frame)      350 ms   10.3%   ← root layout + theme
Phase 3 (to-interactive) 1,930 ms   56.6%   ← post-frame hydration + a sync fetch
Residual                   240 ms    7.0%   ← system-service wait, stated

Reading: Phase 3 dominates. The linkage is NOT the primary problem.
Fix order: (1) remove the sync fetch from the critical path,
           (2) make hydration incremental,
           (3) only then look at Phase 1.
```

The instinct would have been to attack Phase 1 (118 libraries is a visible smell). The measurement
says Phase 3 pays three times as much. **That is the value of attribution.**

## Checklist

- [ ] Every claimed cost is assigned to a phase, with a measurement behind the assignment (R3)
- [ ] Phase 1 is measured with a loader trace or ablation, not inferred from source
- [ ] Ablation changes one thing at a time, with the control re-measured
- [ ] The unexplained residual is stated, not distributed
- [ ] The dominant phase is identified before any fix is chosen
- [ ] The fix family matches the dominant phase
- [ ] The method is held constant across the whole attribution exercise (R5)
- [ ] The attribution is recorded with the total, so the arithmetic can be checked
