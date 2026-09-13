# Measurement

<!-- STANDARD: 3min -- HEART, SUS, task success, time on task, and instrumentation -->

## Why measurement is the whole discipline

Without measurement, a quality practice degrades into re-litigating taste every quarter. With it,
findings become attributable and improvements become defensible. This is R5: a proposed
improvement without a baseline and a metric is a hypothesis — and should be labelled one.

## The instrument set

| Instrument | Measures | Cost | Use for |
|---|---|---|---|
| **Task success rate** | Can users accomplish the task | Low — needs instrumentation | The primary outcome |
| **Time on task** | How long it takes | Low | Efficiency regressions |
| **Error rate** | How often users fail or misfire | Low | Error-prevention work |
| **HEART signals** | Happiness, Engagement, Adoption, Retention, Task success | Medium | Product-level quality tracking |
| **SUS** | Perceived usability, 0–100 | Low — 10 items | A comparable opinion, from users |
| **Single Ease Question** | One-item perceived difficulty | Very low | After each task in a study |
| **Task-level abandonment** | Where users give up | Low | Finding the failing step |
| **Heuristic scorecard** | Craft conformance | Medium | Finding defects, not proving outcomes |

The important pairing: **the scorecard finds defects; the outcome metrics prove the fixes.** A
rising heuristic score with flat task success means the right things were not fixed.

## Task success — the primary metric

Define success per task, before measuring. Ambiguity here is why "did it improve?" is unanswerable.

```text
Task: "Find last quarter's invoice for Acme and download the PDF"
Success: the PDF is downloaded, without assistance
Partial:  the invoice is located but not downloaded
Failure:  the invoice is not located, or the task is abandoned

Measured as: success rate = successes / attempts
Baseline:    62% [VERIFIED] — instrumented release 2.5, n=4,180
Target:      85%
Owner:       checkout team
```

Every field matters. "Success" without a definition is not measurable; a rate without a baseline
cannot show improvement; a target without an owner does not move.

## The HEART framework

A structure for choosing signals so the metrics cover the experience rather than only the funnel.

| Dimension | Question | Example signal |
|---|---|---|
| **Happiness** | Do users feel good about it? | SUS, satisfaction rating, ease question |
| **Engagement** | How deeply do they use it? | Frequency/depth of key feature use per session |
| **Adoption** | Are new users taking it up? | First-use rate of the feature within N days |
| **Retention** | Do they come back? | Return rate for the task's user cohort |
| **Task success** | Can they accomplish it? | Success rate, time on task, error rate |

The value of the framework is **coverage**: a product can have excellent engagement and terrible
task success (a compelling but frustrating tool), or excellent task success and poor retention (a
tool that solves a one-time problem). Choosing at least one signal per dimension forces the
question to be asked.

## SUS

The System Usability Scale is ten items, scored to 0–100, and its value is comparability — the
same instrument across products and over time.

| Score band | Interpretation |
|---|---|
| Above ~80 | Users rate it highly; a strong result to defend |
| ~68 | Around the average of the many products measured with the instrument |
| ~50 and below | Users rate it poorly; treat as a priority signal |

Band guidance is practitioner convention derived from large collected datasets; quote it as a
comparison aid, not as a standard, and confirm current interpretation guidance before citing a
specific cut-off.

SUS is a *perception* metric. It is not a substitute for task success, and a high SUS with a low
success rate means users like it and cannot use it.

## Instrumentation

```text
Task:   find_invoice
Events:
  - task_started     {entry_point, user_cohort}
  - step_completed   {step_id, elapsed_ms}
  - task_succeeded   {elapsed_ms}
  - task_failed      {reason: not_found | abandoned | error}
  - task_abandoned   {last_step_id, elapsed_ms}
Properties: device_class, network_class, locale, app_version
```

Rules:

1. **Instrument outcomes, not just page views.** "Screen viewed" cannot answer "did they succeed".
2. **Record the failure reason.** A failure rate without reasons cannot be prioritised.
3. **Record the last step for abandonment.** That is where the defect lives.
4. **Include device and network class.** Perceived performance and success both vary with them.
5. **Version the events.** A change in definition invalidates the trend.

## Attribution

Establishing that a change caused a movement is harder than observing a movement.

| Risk | Control |
|---|---|
| Seasonality | Compare against a matched prior window, not just the last period |
| Release mix | Hold other changes out of the comparison window |
| Traffic mix | Segment by cohort and source |
| Selection bias | Prefer randomised rollout where feasible |
| Instrumentation change | Never change event definitions in the same window as the measured change |

If attribution is not defensible, say so. An unattributed improvement reported as a result is the
Anti-Hallucination failure this skill most often faces.

## Reporting

```markdown
## Quality report — <release> — <date>

**Baseline:** captured <date>, interface version <version>
**Metric:** task success, <task set>, n=<n>

| Task | Baseline | Now | Δ | Owner |
|---|---|---|---|---|
| find_invoice | 62% | 74% | +12 | checkout |
| add_payment_method | 71% | 69% | −2 | payments |

**Scorecard:** mean 2.1 → 3.0; S1 7 → 0
**SUS:** 61 → 74 (n=312) [VERIFIED]
**Confounders:** release 2.7 also changed the search backend; `find_invoice` may be affected.
**Unchanged:** time on task moved within noise for both tasks.
```

The `Confounders` line is what makes the report honest. Every real measurement has one.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Measuring only page views | Cannot answer whether the task succeeded |
| No defined success per task | The rate is meaningless and disputed |
| Reporting a metric without a baseline | Improvement cannot be attributed (R5) |
| SUS as the only metric | Perception without outcome |
| Scorecard as the only evidence | Craft without user effect |
| Changing event definitions mid-comparison | Invalidates the trend |
| Reporting a lift as measured when it is modelled | Anti-Hallucination failure; label estimates |
| No owner on a metric | It does not move |
| No review date | The metric is collected once and forgotten |
