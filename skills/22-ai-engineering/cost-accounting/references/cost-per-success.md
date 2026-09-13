# Cost Per Success

<!-- DEEP: 5+min -- why the outcome-paired metric is the only decision metric, with the arithmetic -->

## The argument in one example

```text
Run A:  $0.10 per call, 60% success  → a success costs $0.10 / 0.60 = $0.167
Run B:  $0.16 per call, 85% success  → a success costs $0.16 / 0.85 = $0.188
```

Run A looks 37% cheaper per call. Run B fails less often. If a failure costs nothing more (no retry,
no escalation), A is genuinely cheaper per *successful* outcome.

Now add the retry, which is what actually happens:

```text
Run A:  60% succeed on attempt 1; the other 40% retry
        expected attempts per success = 1 / 0.60 = 1.67
        expected cost per success     = $0.10 × 1.67 = $0.167

Run B:  85% succeed on attempt 1
        expected attempts per success = 1 / 0.85 = 1.18
        expected cost per success     = $0.16 × 1.18 = $0.188
```

Still A. But now add a second failure mode — the ones that exhaust their retry budget and escalate:

```text
Run A:  of the 40% that retry, 30% exhaust and escalate
        escalation cost = 3 extra calls + a human gate ≈ $0.42
        cost per success = 0.167 + (0.40 × 0.30 × 0.42 / 0.60) = 0.167 + 0.084 = $0.251

Run B:  of the 15% that retry, 10% exhaust
        cost per success = 0.188 + (0.15 × 0.10 × 0.42 / 0.85) = 0.188 + 0.0074 = $0.195
```

**B is now 22% cheaper per successful outcome** while being 60% more expensive per call. That is the
whole argument: per-call cost is not a proxy for the thing you care about — on a workload with
retries and escalation, it points the wrong way.

## The formula

```text
cost_per_success = total_spend_for_the_cohort / successful_outcomes_in_the_cohort
```

Two properties make it the right metric:

1. **It absorbs the failure rate.** You cannot make it better by making failures cheaper, because
   failed attempts still spend and do not add to the denominator.
2. **It matches the business question.** Nobody buys calls. They buy completed tasks.

**State the cohort.** "Cost per success" over one run is undefined; over N runs it is a mean, and the
N matters as much as the number.

## What the metric exposes that others hide

| Hidden cost | Per-call metric | Cost per success |
|---|---|---|
| Cheap-but-flaky model | looks like a win | shows as a loss |
| Retry storm | invisible | counted in the numerator |
| Escalation to a human gate | invisible | counted, and usually dominant |
| Caching that stops hitting | invisible | counted as extra calls |
| A prompt that makes runs longer | partially visible | fully visible |
| Fewer nodes, same outcome | invisible | a clear win |

## Companion metrics

Cost per success is the headline; these diagnose it. Report them together.

| Metric | Formula | Tells you |
|---|---|---|
| **Cost per success** | total spend / successes | the decision metric |
| **Success rate** | successes / runs | the denominator's driver |
| **Retry rate** | runs with ≥2 attempts / runs | how much of the spend is repetition |
| **Escalation rate** | runs reaching a gate / runs | the most expensive per-unit cost |
| **Attempts per success** | Σattempts / successes | the multiplier on per-call cost |
| **Cost per attempt** | total spend / Σattempts | the per-call family, correctly scoped |

**"Cost per attempt" is the honest version of "cost per call".** It is a legitimate metric — it
measures the unit you can actually optimise with `token-efficiency` — as long as it is never
presented as the outcome cost.

## The failure mode: cost per success with a quality blind spot

```text
Run A: $0.20 per success, 90% success, answers rated 3.1/5
Run B: $0.14 per success, 90% success, answers rated 2.2/5
```

B is cheaper per *success as defined by the grader*. If the grader only checks completion, B wins and
quality degrades silently. So:

**Pair cost per success with the quality score.** The pair is the metric:

| | Cost/success | Quality | Verdict |
|---|---|---|---|
| A | $0.20 | 3.1/5 | acceptable |
| B | $0.14 | 2.2/5 | a saving on paper, a regression in practice |

The `agent-eval-pipeline` owns the quality score; this skill owns the pairing. Neither alone is
sufficient.

## Comparing two configurations

```text
1. Fix the cohort: same task set, same run count, same period.
2. Both sides measured the same way (same method, same measurement status).
3. Report: cost/success, success rate, retry rate, quality score.
4. Report the DELTA on cost/success, not the absolute numbers.
5. Hold the price constant, or state the price change separately.
```

**Step 5 is the one that gets skipped.** A model swap changes the price *and* the success rate; a
comparison that does not separate them attributes a price change to the code, or vice versa.

## The worked comparison

```text
Before: 4-node pipeline, 1 model
  cost/run         $0.0480    success 78%    retries 1.4 avg
  cost/success     $0.0615    quality 3.4/5

After: 3-node pipeline, 2 models (cheaper on the high-volume node)
  cost/run         $0.0340    success 76%    retries 1.4 avg
  cost/success     $0.0447    quality 3.3/5

Reading: cost/success fell 27%, run cost fell 29%, success fell 2 points and
quality 0.1 — both within the noise of a 20-run cohort. A genuine saving.
The lever was node count (the run-level family), not per-call tuning.
```

That final line matters: the change that produced the saving was structural, and a report that does
not say so leaves the reader looking for a prompt-level cause that does not exist.

## Reporting shape

```text
Cost per successful outcome — <workflow> — <date>

Cohort: 20 runs, <task set>, <period>. Method: executor-reported usage ([VERIFIED]).
Price basis: <provider> rates as of <date>.

|                 | Before | After | Δ      |
|-----------------|--------|-------|--------|
| cost / success  | $0.0615| $0.0447| −27.3% |
| cost / run      | $0.0480| $0.0340| −29.2% |
| success rate    | 78%    | 76%   | −2.0 pt (within noise) |
| retries / run   | 1.4    | 1.4   | 0      |
| quality score   | 3.4/5  | 3.3/5 | −0.1   |

Verdict: a genuine reduction. The lever was node count, not per-call cost.
```

## Checklist

- [ ] The headline metric is cost per successful outcome, not per call or per step (R3)
- [ ] The cohort (task set, run count, period) is stated with the number
- [ ] The success rate is reported alongside the cost, always
- [ ] The quality score is paired with it, so a completion-only grader cannot hide a regression
- [ ] Retry rate and attempts-per-success are reported as the diagnostics
- [ ] "Cost per attempt" is used where a per-call figure is genuinely wanted, and labelled as such
- [ ] Comparisons hold the cohort and the price constant, or state the price change separately
- [ ] A saving claim names the lever family (run-level or per-call), so the reader knows where to look
