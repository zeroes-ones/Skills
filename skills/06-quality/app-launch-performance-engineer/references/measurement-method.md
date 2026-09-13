# Measurement Method

<!-- STANDARD: 3min -- how to measure repeatably, and how to compare honestly -->

## Why the method is a deliverable

Every rule in this skill that involves a number (R1, R5) exists because a launch figure without a
method is unusable: it cannot be reproduced, cannot be compared, and cannot be argued with. The
method is therefore part of the result, not an implementation detail.

**The method definition, in full:**

```text
Mode          cold | warm | hot        (and how you produced it)
Device class  the class, named         (and why it is representative)
Cache state   cleared | retained       (and what exactly was cleared)
Run count     ≥10                      (or more, stated)
Reported      median and p90           (never the best run)
Instrument    the tool                 (and its version)
Conditions    thermal, background, network — anything that could shift the result
```

## Controlling the conditions

| Condition | How to control | Why it matters |
|---|---|---|
| Process state | kill/force-stop between cold runs | otherwise you measure warm |
| Cache state | clear it, or state that you did not | a warm cache hides network and disk cost |
| Device temperature | let it cool between batches | a warm device throttles, inflating later runs |
| Background load | quiet the device; disable sync | a background task inflates the median |
| Power state | same power mode across runs | low-power mode changes clock speed |
| Network | throttle to a stated profile, or fix it | otherwise variance dominates |
| Instrument | one tool, one version | comparing across tools compares the tools |

**The temperature issue is the one most often missed** on mobile: a batch of 20 runs warms the device,
and the later runs are slower for reasons unrelated to your change. Interleave the control, or cool
between batches.

## Median, p90, and why not the mean

| Statistic | Use it for | Do not |
|---|---|---|
| **Median** | the typical experience; the number to report | misread it as the worst case |
| **p90 / p95** | the tail, which is what complaints describe | ignore it; the tail is where the pain is |
| **Mean** | almost nothing here | use it — a single outlier skews it, and launch distributions are skewed |
| **Best run** | establishing the floor, for diagnostics only | ever report it as the result |

```text
20 runs:  1180, 1195, 1210, 1225, 1240, 1240, 1255, 1260, 1270, 1285,
          1300, 1310, 1320, 1345, 1360, 1390, 1425, 1470, 1560, 1890

median = 1285    p90 = 1470    best = 1180    mean = 1321

Report:  median 1,285 ms, p90 1,470 ms
Never:   "1,180 ms" (best) or "1,321 ms" (mean hides the tail behind a smooth number)
```

## Comparing before and after honestly

The method holds still; the change does not. Four rules:

```text
1. Same instrument, same version.
2. Same device class (ideally the same physical device).
3. Same mode, same cache state, same conditions.
4. Enough runs that the delta exceeds the noise — and say what the noise is.
```

**Establish the noise floor first.** Run the unchanged build twice, back to back, and look at the
spread. If two identical runs differ by 60 ms, a claimed 40 ms improvement is noise.

```text
Baseline run A   median 2,410   p90 3,380
Baseline run B   median 2,455   p90 3,410
                  Δ median 45 ms → the noise floor is ~45 ms
After the fix    median 2,180   p90 3,050
                  Δ from baseline 230 ms → outside the noise floor ✅
```

Reporting the noise floor is what separates a measured improvement from a hopeful one.

## The comparison traps

| Trap | What it produces |
|---|---|
| Different device for before/after | the device difference, disguised as your change |
| Cache cleared for the baseline only | your "improvement" is the cache |
| Fewer runs after the change (it was faster, so you stopped early) | optimism, not measurement |
| Measuring at a different time of day (thermal, network) | environmental drift as signal |
| Changing two things at once | unattributable |
| Using the profiler's own overhead inconsistently | instrument cost as signal |
| A CI runner that varies between builds | noise read as a regression |

**The two-things-at-once trap is the most common** in practice. If you also upgraded a dependency
while changing initialisation, you cannot attribute the result. Change one thing, measure, then change
the next.

## Making it reproducible

```text
A reviewer must be able to reproduce your number without asking you anything.
Therefore record:
  - the exact command or the manual steps
  - the build/commit measured
  - the device (model class, and ideally the specific unit)
  - OS/runtime version
  - the run count and the reported statistics
  - anything that would shift the result, including what you could not control
```

If a step cannot be scripted (a manual launch), say so — an unstated unscriptable step is how a
measurement becomes unreproducible.

## Recording the result

```markdown
### Launch measurement — <surface> — <date>

| Field | Value |
|---|---|
| Build | <commit> |
| Mode | cold (process force-stopped between runs) |
| Device | <class>, <model>, <OS version> |
| Cache | cleared (app cache + assets) |
| Runs | 20 |
| Instrument | <tool> <version> |
| Conditions | device cooled between batches; airplane-mode off, WiFi fixed |
| Noise floor | 45 ms (two baseline runs) |

| Metric | Median | p90 | Budget | Status |
|---|---|---|---|---|
| TTID | 1,240 ms | 1,690 ms | 800 / 1,150 | over |
| TTFD | 3,410 ms | 4,120 ms | 1,800 / 2,600 | over |

**Conclusion:** TTFD is 1.6 s over budget; the gap between TTID and TTFD
(2.2 s) points at Phase 3, not Phase 1. Fix belongs in deferred work
and data sequencing.
```

## Checklist

- [ ] Mode, device class, cache state, run count, instrument and conditions are all recorded (R1)
- [ ] The process state is controlled so the intended mode is actually measured
- [ ] At least 10 runs; median and p90 reported
- [ ] The best run is never reported as the result
- [ ] The noise floor is established before any improvement is claimed
- [ ] One change at a time, with the control re-measured
- [ ] Before/after use the identical instrument, device, mode and cache state (R5)
- [ ] The method is written with the number, so a reviewer can reproduce it
- [ ] Anything uncontrollable is stated rather than omitted
