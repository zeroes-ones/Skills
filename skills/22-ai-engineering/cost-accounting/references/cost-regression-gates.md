# Cost Regression Gates

<!-- STANDARD: 3min -- delta gating, baselines, and separating price drift from usage drift -->

## The rule

**Gate on the delta, not on an absolute number.** An absolute cap either becomes trivially loose as
prices fall, or fails for reasons unrelated to your change as prices rise. A delta compares your
candidate against a baseline measured the same way.

## Why an absolute cap fails

```text
Cap: $0.20 per successful run.  Workflow measures $0.19.

Six months later, a model price rise pushes the same usage to $0.21.
→ the gate fails, and nothing about the code changed.
→ the team raises the cap to $0.25 to unblock, with no review.
→ the gate now tolerates a 24% regression.

That is how an absolute gate becomes decorative.
```

A delta gate answers the question the team actually cares about: **did this change make it worse?**

## The baseline

```text
baseline = median cost_per_success over N runs on the reference revision
```

| Property | Requirement |
|---|---|
| Method | identical to the candidate's (same cohort, same measurement status) |
| Revision | recorded — a commit SHA, so the baseline is reproducible |
| N | enough that the median is stable; state it |
| Pricing | the price basis and its date, so a price change can be separated |
| Refresh | re-baselined deliberately, with the cause recorded |

**A baseline without its revision is not a baseline.** It cannot be re-measured, so nobody can tell
whether the candidate or the baseline moved.

## The comparison

```text
delta = (candidate − baseline) / baseline

Gate:  fail when delta > threshold        (a regression)
Warn:  when delta > threshold/2           (drift, before it becomes a failure)
Note:  when delta < −threshold            (an improvement; re-baseline after confirming)
```

| Threshold | Use |
|---|---|
| 10% | tight; suits a stable workflow with a measured baseline and a stable price |
| 25% | the usual default; absorbs normal variance without hiding real regressions |
| 50% | loose; appropriate only where the workload is inherently variable |

**Set the threshold from the measured variance**, not from taste: run the baseline twice and look at
the spread. A workflow that varies ±18% between identical runs cannot be gated at 10% without
flapping.

## Separating price drift from usage drift

The single most useful diagnostic in a cost gate, because the two have opposite remedies.

```text
cost = tokens × price

Cost rose 30%. Which term moved?
├── tokens flat, price up      → a PRICE change. The remedy is routing or the
│                                contract, not the code. Re-baseline deliberately
│                                and record the price date.
├── tokens up, price flat      → a USAGE change. The code or the model changed
│                                something. Attribute it (attribution.md).
├── both moved                 → attribute each share; report them separately.
└── neither moved, cost rose   → a measurement problem. Check `measured` and
                                 reconcile against the invoice.
```

**Report the two deltas separately.** "Cost/run +30%" is not actionable. "Price +30%, tokens flat" is
immediately actionable — and points at `finops-engineer`, not at the code.

## What else the gate should assert

Cost alone is not enough; a change that halves cost by doubling failures is a regression.

| Dimension | Assert | Why |
|---|---|---|
| cost / success | not worse than the threshold | the headline |
| success rate | within its own variance band | stops a cheap-failure "win" |
| quality score | within its own band | stops a completion-only grader hiding quality loss |
| retry rate | not worse | the multiplier on per-call cost |
| escalation rate | not worse | the most expensive per-unit cost |

**The five together are the gate.** Any one alone is gameable; the set is not.

## Where the gate runs

| Level | Cadence | Signal |
|---|---|---|
| Per change | on every PR touching a workflow, prompt or model route | catches causes on the change that introduced them |
| Nightly | the full task set on the main branch | catches drift CI cannot see (variance, environment) |
| Per release | before a release | the release go/no-go input |
| Continuous | the production metric | catches what neither preview sees |

**Prefer per-change where the cost is fast to measure** — a graph workflow with a small task set can
run its cost check in the same pipeline. Where it is slow, nightly plus a production metric is the
honest alternative, stated as such.

## Handling a legitimate regression

Sometimes a cost rise is correct: a capability was added, quality improved, a task got harder.

```text
A gate failure is one of three things:
  1. A defect           → fix it
  2. A price change     → re-baseline, with the date and the cause recorded
  3. A deliberate trade → record the reason and raise the baseline with a review date

The failure the gate exists to prevent is a FOURTH case: raising the threshold
without recording which of the three it was.
```

## Reporting shape

```text
Cost gate — <workflow> — <date>

Baseline:   <rev> @ <price-date>, median over 20 runs           $0.0615 / success
Candidate:  <rev> @ <price-date>, median over 20 runs           $0.0447 / success
Delta:      −27.3%   (threshold: fail > +25%, warn > +12.5%)

| Dimension       | Baseline | Candidate | Δ        | Status |
|-----------------|----------|-----------|----------|--------|
| cost / success  | $0.0615  | $0.0447   | −27.3%   | PASS   |
| success rate    | 78%      | 76%       | −2.0 pt  | PASS   |
| quality         | 3.4/5    | 3.3/5     | −0.1     | PASS   |
| retries / run   | 1.4      | 1.4       | 0        | PASS   |
| escalations     | 6%       | 6%        | 0        | PASS   |

Price split: tokens −29.2%, price 0%  → a USAGE reduction, not a price effect.
Verdict: genuine improvement; re-baseline after this release.
```

The `Price split` line is what makes the report trustworthy: without it, a reader cannot tell whether
the team improved the code or merely benefited from a cheaper model.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Absolute cap instead of a delta | fails on price changes, then gets loosened to the point of uselessness |
| A baseline with no revision | cannot be reproduced, so a movement cannot be attributed |
| Threshold set by taste | flaps if too tight, hides regressions if too loose |
| Cost asserted alone | a cheap-failure change passes |
| Price drift attributed to code | the wrong team investigates, and the wrong fix is applied |
| Threshold raised without recording the cause | the gate decays silently into a formality |
| Comparing across different measurement methods | the delta includes the method change |

## Checklist

- [ ] The gate compares a delta against a baseline, not an absolute cap (R4)
- [ ] The baseline records its revision, run count, method and price date
- [ ] The threshold derives from the measured variance, not from taste
- [ ] Price drift and usage drift are reported separately
- [ ] The gate asserts cost/success **and** success rate, quality, retries and escalations (R3)
- [ ] A gate failure is classified as defect, price change, or recorded trade — never silently loosened
- [ ] The gate runs per change where fast enough, and says so explicitly where it does not
- [ ] An improvement triggers a deliberate re-baseline rather than leaving a stale baseline
