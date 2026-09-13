# Calibration Recipes — making a verdict carry signal

> A verdict is a measurement, so it needs a known-good reference. These recipes build the
known-bad set and the four numbers that say whether a validator is awake.

---

## Calibration recipes

A verdict is a measurement, so it needs a known-good reference — the same way a test needs a failing
case to be meaningful. R5 exists because an uncalibrated validator produces a verdict *shape* with no
verdict *content*.

### Build the known-bad set

```
Sources of known-bad cases, in order of value:
  1. Historical failures that actually escaped (the highest-value cases — they beat your validator once)
  2. Post-incident review findings
  3. Near-misses that a human caught
  4. Deliberately seeded defects (must include at least one subtle one)
Minimum viable size: 10 cases. Below that, the measured rejection rate is noise.

For each case record: the artifact, why it is bad, and the class of defect.
The class matters — a validator that only rejects one class has one check, not five.
```

### Measure the four numbers

| Number | Definition | What it tells you |
|--------|-----------|-------------------|
| **True rejects** | Known-bad cases the validator rejects / total known-bad | Sensitivity — is it awake? |
| **False rejects** | Known-good artifacts it rejects / total known-good | Precision — is it usable, or just noisy? |
| **Rejection rate** (live) | Rejections / total in production, **per artifact class** | Drift — has it become a rubber stamp? |
| **Agreement with human** | Where a human also judged, do the verdicts match? | Calibration against the anchor |

### The two failure signatures

```
rejection_rate ≈ 0 on consequential work
    → the producer is either perfect (rare) or the validator sees nothing (common).
      Check wiring first: does the validator receive the artifact at all?
      Then criteria: can any artifact fail them?
      Then boundary: did it adopt the producer's reasoning (R2)?

rejection_rate ≈ 100 on consequential work
    → the criteria are mis-specified against the intent, or the producer is not attempting
      the task. Neither is fixed by moving a threshold. Fix upstream.
```

### Re-calibrate on model change

Calibration is model-specific: agreement measured under one model does not transfer to another. A
model swap without re-calibration silently invalidates every prior approval — a *silent-recall*
failure, the most expensive kind, because the system keeps saying yes.

---
