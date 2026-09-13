# Reconciliation

<!-- STANDARD: 3min -- comparing internal accounting against provider invoices, and what variance means -->

## Why the invoice is the only ground truth

Everything internal — run-state, spans, dashboards — is a *model* of the bill. The invoice is the
bill. Internal accounting that is never reconciled is a model nobody has checked, and models drift.

```text
Internal:  $398.20 for the period
Invoice:   $410.61 for the period
Variance:  +3.1%  → within an accepted band; the model is sound

Internal:  $12
Invoice:   $31,400
Variance:  +261,567%  → something is not being measured at all
```

The second case is the failure this file exists to catch, and it is invisible without reconciliation.

## The reconciliation procedure

```text
1. Fix the window FIRST: the provider's billing period is not your calendar month.
   Match the provider's boundaries, not yours.
2. Pull internal total for that window, from run-state or spans.
3. Pull the invoice total for the same window, per model where the invoice breaks it down.
4. Compare per model, not only in total — a total can hide two offsetting errors.
5. Record the variance and the date.
6. Investigate any variance outside the band.
7. Investigate a SUDDENLY SMALLER variance too — it can mean reporting broke.
```

**Step 1 is the most common source of false variance:** comparing a calendar month against a billing
period that starts mid-month produces a discrepancy that looks like a leak and is not.

## What the variance means

| Variance | Likely cause | Action |
|---|---|---|
| within ±5% | normal: rounding, cache credits, timing | record and move on |
| 5–20% consistently high | an unmeasured path: a client-side call, a retry outside the runner, a batch job | find the unmeasured path |
| 5–20% consistently low | double-counting, or a cache discount you are not applying | check the aggregation and the rate |
| > 20% | a whole workload unmeasured, or a wrong rate | treat as a defect; the accounting is not trustworthy for decisions |
| suddenly ~0% after a period of variance | reporting broke | check that runs are still being recorded at all |
| changing wildly month to month | the window or the rate basis differs | fix the window and the rate first |

**A *falling* variance deserves the same attention as a rising one.** The intuitive reading —
"our accounting got better" — is wrong about half the time.

## The accepted band

State it, so "within tolerance" is a number and not a feeling.

```text
Accepted band: ±5% of the invoice, per period, per model where possible.
Outside the band: investigated before the numbers are used for a decision.
```

**Why a band and not zero:** timing differences, cache credits applied at the provider's boundary,
rounding at six decimal places, and mid-period price changes all produce small differences that are
not defects. Chasing them wastes effort and produces no insight.

## Per-model reconciliation

The total hides offsetting errors:

```text
Model A:  internal $210  invoice $280   (+33%)   ← a real gap
Model B:  internal $188  invoice $130   (−28%)   ← a real gap
Total:    internal $398  invoice $410   (+3%)    ← looks fine

Netting to acceptable is not the same as being correct.
```

Break down by model — or by the coarsest dimension the invoice offers — before declaring the
variance acceptable.

## What reconciliation catches that nothing else does

| Defect | Caught by reconciliation |
|---|---|
| A whole workload unmeasured (`measured: false` forever) | yes — the invoice is larger than the model |
| A client path outside the accounting | yes |
| A wrong price rate | yes, as a proportional gap on one model |
| Double-counting a retried call | yes, as a negative variance |
| Cache credits not applied | yes, as a consistent positive variance |
| A stopped reporter | yes, as a sudden drop to ~0% |
| A window mismatch | yes, and it disappears when the window is fixed |

## The reconciliation log

Keep it. The trend is more informative than any single month.

| Period | Internal | Invoice | Variance | Note |
|---|---|---|---|---|
| 2026-06 | $362.10 | $371.40 | +2.6% | baseline |
| 2026-07 | $388.04 | $410.61 | +5.8% | new workflow not tagged; found and fixed |
| 2026-08 | $402.11 | $409.88 | +1.9% | in band |
| 2026-09 | $11.20 | $418.30 | +3634% | reporter stopped on the 3rd; fixed and re-run |

The 2026-09 row is the value of the log: a single month's number says "huge variance", the log says
"the reporter broke on the 3rd", which is a five-minute fix.

## How often

| Volume | Cadence | Why |
|---|---|---|
| Any spend that matters to a budget | monthly, at minimum | matches the billing cycle |
| A production fleet | weekly, on a sampled window | catches a break before a month's spend is unaccounted |
| A new workflow | at first billing period after launch | validates the accounting before it is trusted |
| After any model or price change | immediately | the rate assumption changed |

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Reconciling the calendar month against a billing period | produces false variance every time |
| Comparing only totals | two offsetting errors net to acceptable |
| Chasing variance to zero | wastes effort on timing and rounding that are not defects |
| Ignoring a falling variance | often means the reporter broke |
| No accepted band | every difference becomes a debate |
| No reconciliation log | cannot distinguish a one-off from a trend |
| Reconciling once, at launch | the accounting drifts from the moment it is left alone |

## Checklist

- [ ] The reconciliation window matches the provider's billing period, not the calendar month
- [ ] Internal totals are compared per model, not only in aggregate
- [ ] An accepted band is stated (typically ±5%)
- [ ] A variance outside the band is investigated before the numbers inform a decision
- [ ] A suddenly smaller variance is investigated as a possible reporting failure
- [ ] A reconciliation log is kept, because the trend reveals what one month cannot
- [ ] Reconciliation runs on the cadence the spend warrants, and immediately after a price change
- [ ] The variance is reported alongside any figure that is used for a budget decision
