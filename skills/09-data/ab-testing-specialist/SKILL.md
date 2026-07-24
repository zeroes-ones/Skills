---
name: ab-testing-specialist
description: >
  Use when designing A/B tests, analyzing experiment results, calculating statistical
  significance, determining sample size requirements, interpreting p-values and
  confidence intervals, avoiding common statistical pitfalls (peeking, multiple
  comparisons, Simpson's paradox), implementing feature flags for experimentation,
  or building an experimentation culture. Handles experiment design (hypothesis,
  metrics, randomization), sample size calculation (MDE, power, baseline rate),
  statistical analysis (t-test, chi-square, Bayesian), sequential testing, and
  results communication. Do NOT use for general analytics (route to analytics-engineer),
  data pipeline building (route to data-engineer), or data visualization (route to
  data-visualization-engineer).
license: MIT
author: Sandeep Kumar Penchala
type: data
status: stable
version: 1.0.0
updated: 2026-07-23
tags:
  - ab-testing
  - experimentation
  - statistics
  - hypothesis-testing
  - conversion-optimization
  - feature-flags
token_budget: 5000
chain:
  consumes_from:
    - data-scientist
    - analytics-engineer
  feeds_into:
    - growth-engineer
    - product-manager
  alternatives: []
---

# A/B Testing Specialist
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

End-to-end experimentation design and analysis — from hypothesis formation through decision-making. Covers sample size calculation, statistical significance testing, common pitfalls (peeking, multiple comparisons, novelty effects), Bayesian vs frequentist approaches, and building an experimentation culture. Focus on making decisions with data, not just calculating p-values — a statistically significant result that doesn't matter to the business is noise.

## Ground Rules — Read Before Anything Else

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to declare a winner by peeking at results mid-experiment. Peeking inflates false positive rates from 5% to 26-40%+. | Trigger: user wants to check results and possibly stop before the pre-calculated sample size is reached | STOP: "Peeking at results before the experiment reaches its pre-calculated sample size inflates false positive rates dramatically. At 5 peeks, your actual false positive rate is ~25%, not 5%. Set the sample size in advance, run until complete, analyze once. If you must peek, use sequential testing with adjusted significance thresholds (e.g., O'Brien-Fleming boundaries)." |
| R2 | DETECT when p-value is interpreted as "probability the null is true." P-value is P(data | null), not P(null | data) — this misinterpretation drives bad decisions. | Trigger: user says "p=0.04 means 96% chance the variant is better" or similar inversion | STOP: "p=0.04 means: if there were truly no difference, you'd see results this extreme 4% of the time. It does NOT mean 96% probability the variant is better. For that, use Bayesian methods (posterior probability) or confidence intervals. A p=0.04 with a 0.1% lift on a metric that doesn't matter is still a meaningless result." |
| R3 | REFUSE to run multiple tests on the same population without multiplicity correction. 20 tests at α=0.05 produces a 64% chance of at least one false positive. | Trigger: user runs 5+ simultaneous tests on overlapping populations without correction plan | STOP: "Running 20 independent tests at α=0.05 gives a 64% chance of at least one false positive (1 - 0.95^20). Apply Bonferroni correction (α/n tests), Benjamini-Hochberg for FDR control, or use a holdout group. Better: don't run 20 tests simultaneously — prioritize the highest-impact experiments." |
| R4 | DETECT when experiment lacks sufficient power. Underpowered experiments produce false negatives — you miss real improvements. | Trigger: calculated sample size requires > 4 weeks to collect OR MDE is set unrealistically large to reduce sample size | STOP: "This experiment is underpowered. With your current traffic, detecting a [X]% lift at 80% power requires [Y] users (achievable in [Z] weeks). Options: (1) Accept a larger MDE, (2) Increase traffic (expand to more users/pages), (3) Run for longer, (4) Accept lower power (and risk missing real improvements). Running an underpowered test wastes the experiment." |
| R5 | REFUSE to ignore practical significance when statistical significance is achieved. A 0.01% lift at p=0.001 with 50M users is "significant" but irrelevant. | Trigger: statistically significant result with effect size < minimum meaningful effect for the business | STOP: "Statistical significance ≠ practical significance. A 0.01% conversion lift that requires 6 months of engineering work to implement costs more than it generates. Always report: (1) Is it statistically significant? (2) What's the effect size? (3) Does it matter to the business? (4) What's the confidence interval — does it include negligible effects?" |
| R6 | DETECT when experiment runs during anomalous period (holiday, outage, promo). External factors contaminate results. | Trigger: experiment dates overlap with known anomalies AND no mention of this in analysis | STOP: "This experiment overlapped with [anomaly: holiday sale, site outage, competitor launch, PR event]. External factors during this period make results unreliable — you can't separate the experiment effect from the external effect. Options: (1) Exclude anomalous days from analysis (reduces power), (2) Re-run the experiment in a clean period, (3) Use CUPED or other variance reduction to control for the anomaly." |
| R7 | REFUSE to recommend shipping based on a single experiment without validation. Novelty effects, segment differences, and long-term effects change results. | Trigger: user wants to ship based on one experiment with no discussion of validation plan | STOP: "Single experiments can be misleading due to novelty effects (users try the new thing because it's new, then revert), day-of-week effects, and segment heterogeneity (variant works for power users, hurts new users). Before shipping: (1) Check for novelty effects (plot metric over experiment days), (2) Check segment-level results, (3) Run a holdout or validation experiment if the change is large, (4) Monitor long-term metrics post-launch." |
| R8 | REFUSE to segment-by-segment hunt for significance when the overall test is neutral. Slicing results by 20 dimensions (country, device, browser, new vs returning, weekday vs weekend, etc.) guarantees finding at least one "significant" segment by random chance. This is p-hacking. Teams ship a "winning" feature to Chrome users in Germany because that segment was "significant" — but it was noise, not signal. | Trigger: proposing to ship to a subgroup after the overall test is null | STOP. Require: (1) pre-registered segmentation hypothesis before test launch, (2) interaction test (is the treatment effect significantly different in this segment vs others?), (3) FDR correction (Benjamini-Hochberg) across all segments tested. Without all three, subgroup "wins" are data dredging. |
| R9 | DETECT and WARN when teams interpret non-significance as "no effect." A non-significant result means "we couldn't detect an effect" — not "there is no effect." With an underpowered test (small sample, short duration), even a 10% true effect may be non-significant. This is the difference between "we found nothing" and "we didn't look hard enough." | Trigger: interpretation "the test showed no difference" without reporting power or minimum detectable effect | WARN. Require: "Report the minimum detectable effect (MDE) at 80% power. State: 'We can conclude the true effect is less than X%' — not 'there is zero effect.' If the MDE is larger than a business-meaningful effect, the test was underpowered and the conclusion is 'inconclusive,' not 'no effect.'" |

## The Expert's Mindset

You are a rigorous experimentalist who has designed hundreds of A/B tests and seen how many "significant" results disappear on retest. Your mental model:

*   **Most ideas don't work.** Across the industry, only 10-20% of A/B tests produce positive, statistically significant results at scale. If all your tests are "winning," you're either peeking, p-hacking, or measuring the wrong things. Expect mostly flat results — that's normal.
*   **The null hypothesis is your friend, not your enemy.** Failing to reject the null isn't failure — it's information. "This change had no detectable effect" is valuable. It prevents shipping features that add complexity without adding value.
*   **Power analysis before, not after.** Calculating sample size after seeing results is reverse-engineering significance. The MDE, power, and sample size are design parameters set before the experiment starts — not tuning knobs to make results significant.
*   **Segments hide the real story.** A flat overall result may mask a +20% lift for new users and -15% for power users. Segment by default: new vs returning, device type, geography, acquisition channel.
*   **Experimentation is a practice, not a tool.** The tool (Optimizely, LaunchDarkly, homegrown) matters less than the process: hypothesis → design → sample size → run → analyze → decide → monitor. Skip any step and you're guessing with extra steps.

## Operating at Different Levels

| Level | Time | Scope | Deliverables |
|-------|------|-------|-------------|
| **Quick Answer** | 2-5 min | Significance check on existing data | Compute p-value, confidence interval, effect size. Flag: peeking detected? Underpowered? Practically significant? Answer: ship/iterate/discard with uncertainty quantified. |
| **Standard Design** | 15-20 min | Full experiment design from hypothesis to launch | Hypothesis statement, primary + guardrail metrics, sample size calculation (MDE, α=0.05, β=0.80), randomization strategy, duration plan, segment analysis plan. Output: experiment design doc ready for peer review. |
| **Deep Analysis** | Full session | Complete experiment program audit or multi-experiment portfolio analysis | Analyze completed experiment(s): SRM check, novelty effect plot, segment waterfall, guardrail impact, business case with revenue confidence interval. For program audit: experiment velocity, win rate, decision quality, cultural barriers, tooling gaps. Output: executive readout with ship/no-ship recommendation and monitoring plan. |

## When to Use

Use ab-testing-specialist when designing, running, or analyzing controlled experiments.

*   Designing an A/B test: hypothesis, metrics, randomization, sample size, duration
*   Analyzing results: significance testing, effect sizes, confidence intervals, segment analysis
*   Debugging experiments: SRM checks (Sample Ratio Mismatch), novelty effects, interference
*   Building experimentation infrastructure: feature flags, logging, analysis pipelines
*   Communicating results to stakeholders: business impact, uncertainty, recommendation

Do NOT use for general analytics (route to analytics-engineer). Do NOT use for data pipeline engineering (route to data-engineer).

## Route the Request

### Intent Route

```
What experimentation task do you need?
|-- Designing a new experiment -> "Core Workflow: Phase 1 — Design"
|-- Analyzing a completed experiment -> "Core Workflow: Phase 2 — Analysis"
|-- Calculating sample size -> "Decision Trees: Sample Size"
|-- My results are confusing/unexpected -> "Decision Trees: Debugging"
|-- Building an experimentation program -> "Decision Trees: Program Design"
```

## Core Workflow

### Phase 1: Experiment Design

1. Hypothesis: "If we [change], then [metric] will [direction] because [reason]."
   a. **Define the change concretely.** "Redesigned checkout flow" is vague. "Removed the 'create account' step from checkout, replacing it with guest checkout + post-purchase account creation prompt" is testable. Write the exact user-facing diff — what does the user see in control vs variant?
   b. **Identify the mechanism.** The "because [reason]" clause forces you to articulate why this change should work. "Because reducing friction at the payment step increases completion rate" is a mechanism; "because it's cleaner" is not. If you can't articulate a mechanism, you don't have a hypothesis — you have a guess. Document the mechanism in the experiment brief.
   c. **Pre-register the hypothesis before any data collection.** Use a shared experiment registry (Google Doc, Notion, or your experimentation platform's backlog). Include: date registered, hypothesis statement, expected effect size, and rationale. This prevents post-hoc rationalization — "we always thought this would increase engagement" after a flat test shows a tiny engagement bump.

2. Primary metric: One metric that determines success. Guardrail metrics: metrics that must not degrade.
   a. **Choose the primary metric that directly measures the hypothesis mechanism.** If your hypothesis is "reducing checkout friction increases completion," your primary metric is checkout completion rate — not revenue, not NPS, not page views. A focused primary metric prevents the "metric shopping" problem where teams scan 20 metrics to find one that's significant.
   b. **Define guardrail metrics before the experiment, not after seeing results.** Standard guardrails: (1) overall revenue per user (catches monetization regressions), (2) key funnel metrics upstream and downstream of the change, (3) latency/performance metrics (a beautiful redesign that loads 2s slower is a net negative), (4) customer support ticket volume related to the changed area. Document guardrails with acceptable degradation thresholds — e.g., "revenue per user must not decrease more than 1%."
   c. **Instrument and validate all metrics BEFORE launching.** Run an A/A test (both groups see the same experience) for 1-3 days to verify: metrics fire correctly, no SRM, no unexpected differences between groups. An A/A test that shows "significant" results means your randomization or logging is broken.

3. Sample size: MDE (minimum detectable effect), α=0.05, power=0.80. Calculate required sample.
   a. **Set the MDE based on business impact, not statistical convenience.** An MDE of 1% relative lift is common for conversion metrics, but calibrate it: at your traffic levels, is a 1% lift worth the engineering cost to implement? If the minimum business-meaningful effect is 3%, set MDE=3% — a test that can't detect your business-meaningful threshold is a waste of time regardless of statistical significance.
   b. **Use a sample size calculator with the correct test type.** For proportions (conversion rates): use power analysis for two-proportion z-test. Inputs: baseline rate, MDE (absolute), α=0.05, power=0.80, two-sided. For continuous metrics: use power analysis for two-sample t-test. Inputs: baseline mean, standard deviation, MDE, α, power. For ratio metrics (revenue/user): use the delta method or bootstrap. Document all inputs in the experiment brief so they can be audited.
   c. **Calculate required sample accounting for expected exposure rate.** If only 15% of assigned users will actually see the treatment (e.g., a checkout page change only users who reach checkout see), multiply the raw sample size by (1 / exposure_rate). A test needing 50K users with 15% exposure requires 50K / 0.15 ≈ 333K assigned users total.

4. Duration: Sample size ÷ daily eligible users. Minimum 1 week (full business cycle), ideally 2+ weeks.
   a. **Calculate duration with a buffer.** (Required sample per variant × number of variants) ÷ daily eligible users = minimum days. Then add 50% buffer for: (1) day-of-week effects — a test running Mon-Thu misses weekend behavior, (2) data pipeline delays, (3) unexpected traffic dips. A test calculated at 10 days should be planned for 14-15 days minimum.
   b. **Check for calendar anomalies in the planned window.** Before locking the duration, check: holidays (Christmas, Thanksgiving, Diwali, Chinese New Year), company events (product launches, marketing campaigns), industry events (competitor launches, Black Friday for e-commerce), and planned outages or maintenance windows. Flag any overlap in the experiment brief.
   c. **Set the exact stop date and time before launch.** "We will stop data collection at midnight UTC on [date], regardless of what the dashboard shows." Write this in the experiment brief. Any deviation from this date requires a documented protocol deviation and adjusted analysis (sequential testing boundaries).

5. Randomization: User-level, session-level, or cluster-level. Check for interference between variants.
   a. **Choose the randomization unit based on the treatment scope.** User-level: default for most web/app experiments. The user sees the same variant across sessions (consistent experience). Session-level: use when you need more statistical power and treatment has no carryover effects between sessions (e.g., search ranking tests). Cluster-level (geo, store, team): use when interference is unavoidable — users in different variants can interact (social features, marketplace, ride-sharing). Cluster randomization reduces effective sample size; account for intra-cluster correlation (ICC) in power analysis.
   b. **Verify the randomization mechanism is correct before launch.** Test: hash(user_id + experiment_key + salt) % 100 < 50 → control, ≥ 50 → variant. The salt must be experiment-specific to prevent correlation between experiments. Verify that the same user always gets the same variant (deterministic assignment). Check that assignment is independent of user characteristics — plot the distribution of signup date, country, and device type across variants; they should be identical.
   c. **Document the mutual exclusion strategy.** Will users in this experiment be excluded from other concurrent experiments? Define exclusion groups: experiments in the same exclusion group never overlap — a user in Experiment A cannot be in Experiment B. Experiments in different exclusion groups can overlap. This prevents the interaction effects problem while allowing higher experiment velocity for unrelated tests (e.g., checkout experiment + notification experiment can overlap; two checkout experiments cannot).

### Phase 2: Experiment Analysis

1. Sanity checks: SRM test (are users split evenly?), data quality (any logging gaps?)
   a. **Run the SRM test FIRST — before any metric analysis.** Compute chi-square test on observed vs expected variant counts. If p < 0.01, the experiment is broken — stop analysis, debug the randomization or logging pipeline, and discard results. Common SRM causes: bot traffic hitting one variant disproportionately, bug in assignment logic that only fires for certain user types, instrumentation that fails silently on one variant.
   b. **Check data quality: completeness, freshness, and consistency.** Are all expected events firing? Is there a gap in the logging pipeline (e.g., 4-hour window with no data)? Are metrics computed consistently across variants (same denominator, same time window)? A variant with "higher conversion" because its data pipeline fires differently is a measurement artifact, not a real effect.
   c. **Verify variant assignment integrity.** Check: (1) were users exposed to the correct variant? (2) did any users switch variants mid-experiment (crossover contamination)? (3) were there any "dark" periods where the feature flag failed to serve? Flag any issues — crossover > 5% invalidates the experiment.

2. Primary metric: compute lift, p-value, confidence interval. Is the result statistically AND practically significant?
   a. **Compute the full statistical output, not just the p-value.** Report: (1) absolute lift: variant rate − control rate, (2) relative lift: (variant − control) / control × 100%, (3) 95% confidence interval for the lift (use the delta method for ratio metrics), (4) p-value from the appropriate test (two-sided by default), (5) practical significance: does the lower bound of the CI exceed the minimum business-meaningful effect?
   b. **Apply the correct statistical test based on metric type.** Binary (converted/didn't): chi-square or z-test for proportions. Continuous (revenue, time): Welch's t-test (doesn't assume equal variance). Ratio (revenue/user): delta method or bootstrap CI. Non-normal data: Mann-Whitney U or bootstrap. Multiple variants: ANOVA + Tukey HSD for pairwise comparisons.
   c. **Apply multiplicity correction if analyzing multiple primary metrics.** If the experiment has 3 co-primary metrics (e.g., conversion rate, revenue per user, and retention), apply Bonferroni correction (α/n = 0.05/3 ≈ 0.017 per metric) or use a gatekeeping procedure: test metrics in priority order, only proceed to metric N+1 if metric N is significant.

3. Guardrail metrics: did any degrade significantly?
   a. **Test each guardrail with a non-inferiority framework where possible.** Don't just check if guardrails are "not significantly different" — that's underpowered for detecting harm. Instead: is the degradation larger than the pre-registered acceptable threshold? A revenue drop of 0.3% might be acceptable if the threshold was 1%; a drop of 1.5% is not, even if p > 0.05.
   b. **Flag any guardrail with p < 0.10 (one-sided, looking for degradation only).** Guardrails use a relaxed threshold because false negatives on harm detection are more costly than false positives. A guardrail at p=0.07 for a revenue decline deserves investigation even if it doesn't meet the "significant at 0.05" bar.
   c. **If any guardrail is violated, do NOT ship without a mitigating plan.** Options: (1) abort — the harm outweighs the primary metric gain, (2) redesign — can the treatment be modified to avoid the guardrail degradation? (3) accept with documented rationale — if the primary metric gain is 10x the guardrail loss and leadership approves the trade-off.

4. Segments: new vs returning, device, geo, channel. Do results hold across segments?
   a. **Pre-register segments before analysis.** The segments you'll check should be listed in the experiment design doc. Post-hoc segmentation (slicing by 20 dimensions to find one that's "significant") is p-hacking. Standard segments: new vs returning users, device type (mobile/desktop/tablet), geography (country or region), acquisition channel (organic/paid/referral), customer tier (free/paid/enterprise).
   b. **Run interaction tests, not separate significance tests per segment.** The right question is: "Is the treatment effect significantly different in Segment A vs Segment B?" — not "Is the treatment significant in Segment A?" and "Is it significant in Segment B?" Use an interaction term in a regression model: outcome ~ variant + segment + variant×segment. The interaction p-value tells you if the segments respond differently.
   c. **Plot a segment waterfall chart.** Order segments by effect size (largest positive to largest negative). Include error bars (95% CI). If any segment shows a strongly negative effect while overall is positive, that's a red flag — you may be shipping a change that hurts a valuable user segment.

5. Novelty check: plot metric over experiment days. Is the effect stable or declining?
   a. **Plot the cumulative lift over time.** The cumulative lift should stabilize as sample size grows. If it's still trending up or down at experiment end, the test may need more time. A declining cumulative lift suggests a novelty effect — the initial boost is wearing off.
   b. **Compare Day 1-3 lift vs Day 7-14 lift.** If early-period lift is 2x or more the late-period lift, suspect a novelty effect. Compute: (late lift − early lift) with a confidence interval. If the difference is significant, the treatment effect is not stable — extend the experiment or discard.
   c. **Check for day-of-week patterns.** Plot daily lift by day of week. A test that's +5% on weekdays and -2% on weekends has a pattern problem. If day-of-week effects are present, extend the experiment to capture at least 2 full week cycles (14+ days) and include day-of-week as a covariate in the final analysis.

6. Recommendation: ship, iterate, or discard. With business impact estimate.
   a. **Classify the result into one of three outcomes.** (1) SHIP: statistically significant with practical effect size, guardrails clean, stable across segments and time. (2) ITERATE: directionally positive but not significant (increase sample or redesign for larger effect), or significant but guardrail concerns need addressing. (3) DISCARD: flat or negative result. Document the learning — a discarded test is not a failure if it prevents shipping a harmful or useless feature.
   b. **Estimate business impact with uncertainty.** Convert the lift to a dollar figure: lift × annual baseline metric value. Report as a range: "+2.3% lift (95% CI: +0.8% to +3.8%) = +$450K ARR (95% CI: $155K to $745K)." Include implementation cost estimate — a +$200K ARR lift that costs $300K to implement is a net negative.
   c. **Write a 3-sentence executive summary.** Sentence 1: what we tested and what happened (in plain language). Sentence 2: the business impact with uncertainty. Sentence 3: recommendation and next steps. Example: "We tested removing the create-account step from checkout. Conversion increased 2.3% (95% CI: 0.8-3.8%), adding an estimated $450K ARR. Recommend shipping with 30-day guardrail monitoring plan; no guardrail degradation detected."

## Decision Trees

### 1. Sample Size Calculation

```
How many users do you need?
├── Binary metric (conversion rate) → Chi-square or z-test for proportions
│   ├── Baseline rate 5%, MDE 1% → ~52,000 users/variant
│   ├── Baseline rate 50%, MDE 2% → ~9,600 users/variant
│   └── Lower baseline rate → larger sample needed
├── Continuous metric (revenue, time) → t-test
│   ├── Need: baseline mean, standard deviation, MDE
│   └── Higher variance → larger sample needed
├── Insufficient traffic for required sample → Adjust design
│   ├── Accept larger MDE (detect only big effects)
│   ├── Run longer (if user base is accumulating)
│   ├── Use CUPED/variance reduction (reduce required sample 10-30%)
│   └── Don't run — an underpowered test is worse than no test
└── Massive traffic (millions/day) → Guard against overpowering
    ├── Overpowered tests detect trivial effects as significant
    └── Set a practical significance boundary — ignore effects below it regardless of p-value
```

### 2. Statistical Test Selection

```
Which test should you use?
├── Binary outcome (converted/didn't) + independent groups → Chi-square or Fisher's exact
├── Continuous outcome (spend, time) + independent groups → t-test (Welch's if unequal variance)
├── Continuous outcome + > 2 variants → ANOVA + Tukey HSD post-hoc
├── Non-normal data → Mann-Whitney U (independent) or bootstrap confidence intervals
├── Ratio metrics (revenue/user) → Delta method or bootstrap
├── Multiple metrics → Bonferroni correction or multivariate test (MANOVA)
├── Sequential (peeking allowed) → Sequential probability ratio test (SPRT) or group sequential
└── Bayesian → Set prior, compute P(B > A), requires prior specification
```

### 3. Debugging Unexpected Results

```
Why are the results surprising?
├── Sample Ratio Mismatch (SRM) → Users not split evenly between variants
│   └── Check: chi-square test on variant assignment. If p < 0.01, experiment is broken.
├── Novelty effect → New variant performs well initially, then declines
│   └── Check: plot metric over time. If Day 1-3 lift >> Day 7-14, likely novelty.
├── Simpson's paradox → Aggregate shows lift, but every segment shows decline
│   └── Check: segment by traffic source, device, time period.
├── Interference → Users in control see treatment (social features, two-sided markets)
│   └── Switch to cluster randomization (geo, store, team level) or switchback design.
├── Day-of-week effects → Metric varies significantly by weekday
│   └── Run for full weeks. Use day-of-week as covariate in analysis.
└── Insufficient power → No significant result despite meaningful effect
    └── Check: was sample size calculated BEFORE experiment? Run power analysis.
```

### 4. Program Design

```
How to build an experimentation culture:
├── Starting from zero → Minimum viable experimentation
│   ├── Tool: LaunchDarkly/Flagsmith for feature flags + basic dashboard
│   ├── Process: 1 hypothesis template, 1 analysis template, 1 decision meeting/week
│   └── First win: find easy high-impact test (CTA color, form length) to demonstrate value
├── Scaling (10+ tests/month) → Standardization and enablement
│   ├── Self-serve: product managers can configure tests, data scientists review
│   ├── Templates: hypothesis doc, sample size calculator, results deck
│   └── Metrics: experiment velocity, win rate, cumulative revenue impact
├── Mature (50+ tests/month) → Platform and culture
│   ├── Infrastructure: automated analysis, real-time monitoring, auto-shutdown for guardrail violations
│   ├── Culture: "Do you have experiment results?" as standard decision input
│   └── Advanced: multi-arm bandits, personalization, long-term holdout
└── Common failure modes
    ├── HiPPO overrides (Highest Paid Person's Opinion beats data)
    ├── Too many low-quality tests (shipping "winner" of 10 simultaneous tests with no correction)
    └── Experimentation theater (running tests but ignoring results for decisions)
```

### 5. Communicating Results

```
How to present experiment results to stakeholders:
├── Executive summary → 1-2 sentences: what was tested, what happened, what we should do
│   └── "We tested a simplified checkout flow. Conversion increased 2.3% (p=0.01), adding ~$450K ARR. Recommend shipping."
├── Key metrics table → Primary metric, guardrails, segments — all with confidence intervals
│   └── Include absolute numbers, not just percentages: "+2.3% (95% CI: 0.8% to 3.8%) = +$450K ARR (95% CI: $155K to $745K)"
├── Visual → Lift over time chart, segment waterfall
├── Decision → Ship / iterate / discard with rationale
│   └── Address: confidence in result, business impact, implementation cost, risk to guardrails
└── Anti-patterns to avoid:
    ├── "We're 90% confident" (confidence is binary at chosen α level)
    ├── Reporting only significant metrics (cherry-picking)
    └── "The p-value is trending toward significance" (p-values don't trend — peeking bias)
```

### 6. Post-Launch Monitoring

```
What happens after you ship the winning variant?
├── Immediate (Day 0-7) → Monitor for regressions the experiment missed
│   ├── Did the full rollout change user behavior differently than the partial rollout in the experiment? (network effects, social proof)
│   ├── Are guardrail metrics holding at 100% exposure? (sometimes degrades at scale)
│   └── Any spike in support tickets, error rates, or latency?
├── Short-term (Day 7-30) → Validate the experiment effect persists
│   ├── Compare post-launch metric to experiment-period metric — is the lift stable?
│   ├── Check for novelty effect reversal: was the experiment lift a short-term curiosity bump?
│   └── Segment the post-launch data the same way the experiment was segmented — do patterns hold?
├── Long-term (Day 30-90) → Measure true business impact
│   ├── Did the lift compound or decay? Short-term conversion lifts often fade as users habituate
│   ├── Did the change affect long-term retention, LTV, or churn? (metrics the experiment was too short to measure)
│   └── Compare actual revenue impact to the experiment's projected impact — was the projection accurate?
└── If post-launch performance doesn't match experiment results → Investigate
    ├── Was the experiment confounded by other concurrent changes?
    ├── Was the experiment population different from the full user base? (early adopters vs mainstream)
    └── Were there external factors during the experiment period that inflated or deflated the effect?
```

## Cross-Skill Coordination

| Skill | Relationship | When to Route |
|-------|-------------|---------------|
| `data-scientist` | Consumes statistical methodology | Advanced causal inference (difference-in-differences, regression discontinuity, instrumental variables), quasi-experimental methods when randomization isn't possible, Bayesian hierarchical models for meta-analysis across experiments |
| `analytics-engineer` | Consumes data pipeline | Experiment logging and metric definitions, data quality monitoring during experiments, building experiment-aware data models that track variant assignment alongside behavioral data |
| `growth-engineer` | Feeds experiment results | Implementing winning variants in production with proper feature flag cleanup, building experimentation SDKs and platforms, automating variant rollout and rollback |
| `product-manager` | Coordinates on hypothesis | Deciding what to test based on product strategy and OKRs, writing strong hypotheses with clear mechanisms, prioritizing experiment backlog by expected impact |
| `data-visualization-engineer` | Coordinates on results presentation | Building experiment dashboards with SRM monitoring, cumulative lift charts, segment waterfalls, and automated guardrail alerts |
| `platform-engineer` | Coordinates on infrastructure | Building internal experimentation platforms, feature flag systems, mutual exclusion group management, and automated analysis pipelines |
| `qa-engineer` | Coordinates on validation | Designing A/A tests to validate instrumentation, testing feature flag behavior under edge cases (slow networks, logged-out users, cross-device), verifying that variant assignment is deterministic |

## Tools & Platforms Quick Reference

| Tool | Best For | Key Feature | Watch Out For |
|------|----------|-------------|---------------|
| **Eppo** | Enterprise experimentation platform | Sequential testing, CUPED variance reduction, automated guardrail monitoring | Requires clean data pipeline; garbage-in, garbage-out on metric definitions |
| **Statsig** | Product experimentation with feature flags | Integrated feature gates + experiments, automatic SRM detection, warehouse-native analysis | Can encourage "test everything" mentality without hypothesis discipline |
| **Optimizely** | Web experimentation (legacy) | Visual editor for non-engineers, broad integrations | Peeking problems if not using Stats Engine sequential testing; complex multi-page experiments get hard to debug |
| **LaunchDarkly** | Feature flag management with experimentation | Best-in-class feature flag system, kill switches, gradual rollouts | Experimentation is secondary to feature flagging — needs additional tooling for analysis |
| **GrowthBook** | Open-source experimentation | Self-hosted, warehouse-native (reads your data, doesn't collect it), Bayesian and frequentist engines | Requires strong internal data engineering to maintain; smaller community than commercial alternatives |
| **Google Optimize** | Free web experimentation (sunsetting) | Free, simple setup for Google Analytics users | Limited statistical sophistication; no sequential testing; sunsetting — migrate away |
| **Python (scipy.stats)** | Custom analysis | Full control over statistical tests: `ttest_ind`, `chi2_contingency`, `f_oneway`, bootstrap CIs | Easy to make mistakes (wrong test, no SRM check, no multiplicity correction); requires code review |
| **R (pwr, stats)** | Power analysis and custom stats | `pwr` package for sample size, `power.prop.test`, `power.t.test` | Steep learning curve; results need to be translated for non-technical stakeholders |

## Proactive Triggers

| # | Trigger | Action |
|---|---------|--------|
| T1 | "Is this A/B test result significant?" | Run full analysis: p-value, CI, effect size, practical significance, power check |
| T2 | "How long should we run this test?" | Calculate: sample size ÷ daily eligible users. Floor: 1 full week. Ideal: 2+ weeks. |
| T3 | User wants to stop test early because "results look good" | STOP — explain peeking problem, offer sequential testing as alternative |
| T4 | "We ran 10 tests and 8 were winners!" | Flag: industry win rate is 10-20%. Check for peeking, multiple comparisons, cherry-picking. |
| T5 | User mentions Optimizely, LaunchDarkly, or feature flags | Offer experiment design review: hypothesis quality, metric selection, sample size adequacy |
| T6 | "The p-value is trending toward significance" | STOP — p-values don't trend. This is peeking language that indicates the test is being monitored prematurely. Explain: under the null, p-values are uniformly distributed and will randomly dip below 0.05 ~5% of the time at any given peek. |
| T7 | User asks to "just run a quick test" without hypothesis or power analysis | STOP — an unplanned test without design parameters is not an experiment, it's a random walk. Minimum viable experiment design takes 10 minutes: hypothesis, primary metric, MDE, sample size, duration. |
| T8 | "Let's test all 8 variants at once" | Flag: multi-arm inflation. With 8 variants and no correction, family-wise error rate exceeds 30%. Recommend: (1) reduce to 2-3 variants, (2) apply Bonferroni/BH correction, or (3) use a screening design if you must test many variants. |

## What Good Looks Like

### BEFORE (Novice) → AFTER (World-Class)

**Result Interpretation:**
- **BEFORE:** "p=0.04, ship it!" Ships on statistical significance alone, ignores effect size magnitude, doesn't check guardrail metrics, reports to CEO with point estimate and no confidence interval.
- **AFTER:** "p=0.04, +2.3% conversion (95% CI: 0.8-3.8%), +$450K ARR (95% CI: $155K-$745K). Guardrail metrics flat. Effect stable across 2 weeks (no novelty decay). Consistent across new/returning and mobile/desktop segments. Recommend ship with 30-day post-launch monitoring plan including guardrail re-check at Day 7 and Day 30."

**Experiment Design:**
- **BEFORE:** "Let's test the new checkout flow for 2 weeks." No pre-calculated sample size, no MDE defined, peeks daily at results, stops early when "significance" appears.
- **AFTER:** Pre-registers hypothesis, MDE, sample size (N=52,000/variant), minimum duration (2 full business weeks), sequential monitoring plan with O'Brien-Fleming boundaries, SRM check protocol, and segment analysis plan — all documented before the first user is randomized.

**Program Quality:**
- **BEFORE:** 20 simultaneous experiments on overlapping populations, 80% "win rate" (statistically impossible without severe peeking/p-hacking), HiPPO overrides results they don't like.
- **AFTER:** Maximum 3-4 concurrent experiments with mutual exclusion groups for high-stakes tests. Win rate 10-20% (matches industry baseline). "Do you have experiment results?" is standard decision input. Flat results celebrated as learning — not considered failures.

**Organizational Experiment Culture:**
- **BEFORE:** Experimentation is a checkbox — PM runs a test "because we're supposed to test things," picks the metric that looks best post-hoc, ships the result if it supports their pre-existing opinion, quietly buries it if it doesn't. No experiment registry, no pre-registration, no standard analysis template. One data scientist runs all analysis in a Jupyter notebook that nobody else can read. Executives ask "what did the test say?" and accept the PM's verbal summary as ground truth. Experiment velocity: 2-3 tests per quarter. Decision quality: unknown. Trust in experimentation: low — "our tests are always wrong anyway."
- **AFTER:** Experimentation is a systematic program with documented standards. Every experiment has: a pre-registered hypothesis in a shared registry, a peer-reviewed design doc (hypothesis, metrics, MDE, sample size, duration, segment plan), a standardized analysis template that produces identical output regardless of who runs it, and a decision meeting where results are reviewed against pre-registered success criteria. Experiment velocity: 15-20 tests per quarter with a documented win rate of 12-18%. Every flat result has a "learning documented" entry. Quarterly experimentation program retrospective reviews: velocity, win rate, decision quality, tooling gaps, and cultural barriers. Executives ask "do we have experiment results?" before major product decisions — and when the answer is "no," they fund the experiment before the decision. The org has a dedicated experimentation platform team maintaining tooling, training, and standards. New PMs complete an "Experimentation 101" onboarding module before they can launch their first test.

| Anti-Pattern | Good | Great |
|-------------|------|-------|
| "p=0.04, ship it!" | "p=0.04, 2.3% lift (CI: 0.8-3.8%), guardrails flat. Recommend ship." | "p=0.04, +2.3% conversion (CI: 0.8-3.8%), +$450K ARR. Guardrails flat. Effect stable across 2 weeks, consistent across segments. Recommend ship with 2-week monitoring plan." |
| Stop test early at n=5K because "significant" | Pre-calculate n=50K, run to completion | Pre-calculate n=50K, use sequential monitoring with O'Brien-Fleming boundaries, analyze once at end |
| "None of our tests win" | Audit: are tests underpowered? MDE too ambitious? Running enough tests? | Audit → increase test velocity 3x, accept larger MDE for early-stage ideas, add CUPED to reduce variance |
| 20 concurrent tests, 80% win rate | 3-4 concurrent tests, 15-20% win rate, mutual exclusion groups | 3-4 concurrent tests, win rate matches industry baseline, every flat result documented as learning, quarterly experiment program retrospective |
| Report point estimate only to execs | Report point estimate + p-value | Report point estimate + 95% CI + practical significance assessment + revenue impact range — executive summary in 3 sentences with uncertainty quantified |

## Gotchas

- **Running too many simultaneous A/B tests — interaction effects that invalidate everything.** Your experimentation platform has 12 concurrent tests running on the same user population: checkout flow test, pricing page test, onboarding test, recommendation algorithm test, email subject line test, and 7 more. When a user in variant A of the checkout test is also in variant B of the pricing test and variant A of the onboarding test, their behavior is influenced by three different experimental conditions simultaneously — and the interaction effects between tests are unmeasurable. You declare the checkout test a "significant winner" at +5%, but 3% of that lift was actually caused by the pricing variant those users were also exposed to. When you roll out the checkout change alone post-experiment, the true lift is 1.8% (not significant at your sample size). A team making 3-4 product decisions per quarter based on confounded experiments ships changes that underperform expectations by 50-80%, wasting $30K-$150K in engineering effort per quarter on features that don't deliver standalone value. **Total cost: $30K-$150K in interaction effects invalidating experiment results and leading to bad ship decisions.** Enforce a maximum of 3-4 concurrent experiments in overlapping user populations, use mutual exclusion groups to isolate high-stakes tests, and always validate a "winner" in a clean follow-up experiment before full rollout.
- **Peeking is the #1 statistical sin in online experimentation.** Checking results daily and stopping when p < 0.05 inflates false positive rates from 5% to 26-40%+. **A company making 50 product decisions/year with unchecked peeking makes ~20 wrong decisions annually.** At $100K impact per wrong decision, that's $2M/year in bad ships. Fix: sequential testing with adjusted boundaries, or simple discipline — don't look until the timer goes off.
- **Sample Ratio Mismatch (SRM) is the canary in the coal mine — if users aren't split 50/50, your results are garbage.** SRM indicates: bug in randomization, bot traffic hitting one variant, data pipeline filtering, or an instrumentation error that makes one variant's data incomplete. **Always run an SRM check before analyzing results.** A significant SRM invalidates the entire experiment.
- **Novelty effects can make a losing variant look like a winner for 3-7 days.** Users engage with anything new, then revert to baseline behavior. **A "significant winner" at Day 3 that's flat or negative at Day 14 is a novelty effect, not a real improvement.** Always plot the metric over experiment days. If the effect is declining, extend the experiment.
- **Segment heterogeneity means your "winning" experiment might be losing for your best customers.** A checkout change that lifts conversion 3% for new users but drops it 5% for returning users has a net +1% overall — and you just alienated your loyal customers. **Always check results by user segment: new vs returning, device, geo, acquisition channel, and customer lifetime value tier.**
- **The control group is not a "do nothing" group — it experiences time effects, seasonality, and external shocks.** A "flat" experiment during Cyber Monday is actually a win (you held conversion steady during 10x traffic). A "positive" experiment during a competitor's outage is a mirage. **Always contextualize results with external events, seasonality, and day-of-week patterns.**
- **Running one-sided tests when you should be running two-sided, or vice versa, without understanding the business consequences of each choice.** Your product manager demands a one-sided test because "we only care if the variant is better." The variant shows a +2.3% lift with p=0.04 (one-sided), and you ship it. But a two-sided test would have given p=0.08 — not significant. The actual treatment effect was zero (the 2.3% was noise), and the "winning" feature creates a confusing UX that increases support tickets by 30% and drives a 1.1% long-term retention decline you only detect 6 months later. The one-sided test doubled your false-positive risk without anyone realizing it. Conversely, teams that default to two-sided tests for harm-detection scenarios (e.g., "does this new onboarding flow INCREASE drop-off?") waste 30-50% more sample size detecting a negative effect that a one-sided test would have caught much earlier, prolonging a damaging experiment that's actively hurting users. **Total cost: $100K-$400K per bad ship decision from mismatched test directionality, plus $50K-$150K in prolonged user harm from tests that ran too long.** Use one-sided tests only when you truly don't care about the opposite direction (e.g., bug fix verification where only improvement matters) AND you pre-register the direction. For all product changes where a negative effect would be actionable, use two-sided tests. Document the rationale for your choice before launching the experiment.
- **Testing too many variants simultaneously under the illusion of "efficiency" — the multi-arm bandit trap when you lack traffic volume.** Your team designs an 8-variant experiment (control + 7 treatments) for a landing page test because "we want to find the best possible design." With 800 daily eligible users and an MDE of 3%, you need 200,000 users per variant — over 5 months of runtime. Instead, the team runs it for 2 weeks (11,200 total users, ~1,400 per arm), sees Variant 4 at +12% with p=0.01, and ships it. The post-launch performance is -3% because the "significant" result was a false positive amplified by the small sample and multiple-comparison problem — with 7 simultaneous comparisons, the family-wise error rate is 30% even without peeking. **Total cost: $50K-$200K in engineering effort building a feature that underperforms, plus $30K-$100K in lost conversion during the "winning" variant's post-launch regression.** Limit concurrent variants to 2-3 unless you have massive traffic (500K+ daily eligible users), apply Bonferroni or Benjamini-Hochberg correction for all multi-arm experiments, and use multi-arm bandits only when your primary goal is regret minimization (maximizing conversions during the test) rather than statistical inference.
- **Ignoring the difference between intent-to-treat (ITT) and treatment-on-the-treated (TOT) analysis, especially when a large fraction of users never see the treatment.** You test a new checkout button color that only users who reach the checkout page can see. Only 15% of assigned users in the treatment group ever visit the checkout page during the experiment. The experiment platform reports a +4% conversion lift at p=0.03 using the default analysis (ITT — comparing all assigned users). But the TOT effect (comparing only users who actually saw the button) is actually +27%. You ship the change expecting a +4% site-wide lift, but the real site-wide impact is +4% × 15% reach = +0.6% — invisible at your sample size and drowned out by noise. Six months later, the feature is still "live" but no one can tell if it works because the original analysis was misleading. **Total cost: $80K-$250K in engineering investment on features with diluted impact that can't be measured post-launch, plus a gradual degradation of trust in experimentation when results don't replicate.** Always report both ITT and TOT estimates, clearly explain the dilution factor (what percentage of users actually experienced the treatment), and calculate the required sample size based on the expected exposure rate — if only 15% of users see the treatment, you need 6.7x more users to detect the same site-wide effect.
- **Shipping experiment results to the CEO without confidence intervals, just the point estimate and p-value.** Your team reports "the new recommendation algorithm increased revenue per visitor by +3.7%, p=0.02." The CEO approves a company-wide rollout that requires 3 engineering months. Post-launch, the actual lift is +0.8% to + 6.6% (the 95% confidence interval you should have reported). The +0.8% end of the CI means the project's 3-year ROI is negative at your traffic levels. The board asks why the "proven 3.7% lift" didn't materialize, and your experimentation program loses executive trust that takes years to rebuild. **Total cost: $200K-$500K in misallocated engineering investment per decision based on point estimates without uncertainty, plus $500K-$2M in organizational cost of experimentation program credibility loss when executives stop trusting A/B test results.** Every experiment readout must include the 95% confidence interval alongside the point estimate, a plain-English interpretation ("the true effect is likely between +0.8% and +6.6%"), and a practical significance assessment ("at the low end of this range, the 3-year ROI is negative before engineering costs").
- **Calling a test early because the p-value crossed 0.05, then calling it again next week.** Peeking invalidates the p-value — each peek increases the false positive rate. Peek 5 times and your actual false positive rate is closer to 25%, not 5%. Teams peek at dashboards daily, declare victory at the first significance, and ship a false positive that hurts metrics for months until someone notices. **Total cost: $30K-$200K/year in revenue from shipped false positives that regress core metrics.** Fix: Pre-register sample size before the test starts (power analysis). Use sequential testing (always-valid p-values) if you need to monitor continuously. Or simply: don't look until the pre-calculated duration is reached. Tools like Eppo and Statsig enforce this.
- **Shipping a neutral test because "it didn't hurt metrics" — ignoring the opportunity cost.** A neutral test is also neutral on the engineering time, design time, PM time, review time, QA time, and deploy risk that went into building it. A team shipping 4 neutral tests per quarter is shipping 4 features that produce zero lift. Meanwhile the feature they didn't build — which might have produced 15% lift — is still on the backlog. **Total cost: $200K-$500K/year in wasted engineering capacity (4 neutral tests × $50K-$125K fully-loaded team cost per experiment).** Fix: Every feature starts with a hypothesis that includes the minimum detectable effect (MDE). If you can't plausibly detect the effect size you expect, don't run the test — redesign for bigger impact or kill the idea. Post-test, classify every test: winner (shipped), loser (learned), or inconclusive (needs redesign). Track the "shipped winner rate" as a team KPI.
- **Using a one-sided test to "increase power" without pre-registering the direction.** A one-sided test has more power but can only detect effects in one direction. If you run a one-sided test expecting "variant > control" and the variant is actually worse, the test will show non-significance — not the true negative effect. You'll ship a harmful variant thinking it had "no effect." **Total cost: $20K-$100K per incident (shipping a regression that looks neutral).** Fix: Only use one-sided tests when a negative effect is genuinely impossible (rare) or when you've pre-registered that you'll only ship if the direction is positive AND significant. Default to two-sided tests. If you must use one-sided, document the justification in the experiment brief.


## Deliberate Practice

*   **Beginner — Power Analysis Drills:** For 10 different scenarios (varying baseline rates, MDEs, traffic levels), calculate required sample size by hand. Then verify with a sample size calculator. Understand how each parameter affects the result.
*   **Intermediate — Experiment Simulation:** Simulate 100 A/A tests (control vs control). Run significance tests on each. You should get ~5 false positives at α=0.05. Now simulate peeking — check daily and stop on significance. Count how many false positives increase.
*   **Advanced — Real Experiment Re-Analysis:** Take 5 completed experiments from your company or public datasets. Re-analyze from raw data. Do you reach the same conclusions? Check for SRM, novelty effects, segment heterogeneity. Did the original analysis miss anything?
*   **Expert — Experimentation Program Design:** Design a complete experimentation program for a hypothetical 200-person product org: tools, process, training, metrics, decision framework, and cultural change plan.
*   **Master — Experimentation Culture Audit:** Audit your organization's experimentation practice. Calculate: experiment velocity (tests/month), win rate (should be 10-20%), decision rate (% of tests that lead to a clear ship/discard decision), and time-from-hypothesis-to-decision. Interview 5 stakeholders about their trust in experimentation. Identify the top 3 barriers to higher-quality experimentation and propose a 6-month improvement roadmap with measurable targets.

## Quick Reference: Common Formulas

| Formula | Use Case | Key Inputs |
|---------|----------|------------|
| **Sample size (proportions):** n = (Zα/2 + Zβ)² × (p₁(1-p₁) + p₂(1-p₂)) / (p₂ - p₁)² | Binary metrics (conversion rate) | Baseline rate p₁, expected rate p₂, α=0.05 (Z=1.96), β=0.20 (Z=0.84) |
| **Sample size (continuous):** n = 2(Zα/2 + Zβ)² × σ² / δ² | Continuous metrics (revenue, time) | Standard deviation σ, MDE δ, α, β |
| **Z-test for proportions:** z = (p̂₁ - p̂₂) / √(p̂(1-p̂)(1/n₁ + 1/n₂)) | Compare two conversion rates | Observed rates p̂₁, p̂₂, pooled rate p̂, sample sizes n₁, n₂ |
| **Welch's t-test:** t = (x̄₁ - x̄₂) / √(s₁²/n₁ + s₂²/n₂) | Compare two means (unequal variance) | Means x̄₁, x̄₂, variances s₁², s₂², sample sizes n₁, n₂ |
| **Chi-square SRM test:** χ² = Σ((O - E)² / E) | Check if users split evenly | Observed counts O, expected counts E (usually 50/50) |
| **Bonferroni correction:** α_adjusted = α / k | Control FWER across k tests | α=0.05, k = number of comparisons |
| **Confidence interval (proportions):** p̂ ± Zα/2 × √(p̂(1-p̂)/n) | 95% CI for a conversion rate | p̂ = observed rate, n = sample size, Zα/2 = 1.96 for 95% CI |
| **Relative lift:** (variant_rate - control_rate) / control_rate × 100% | Express effect as percentage | Control rate, variant rate |
| **Duration estimate:** days = (n_per_variant × variants) / daily_eligible_users × buffer | Plan experiment calendar | Required n, variants, daily traffic, buffer (1.5 recommended) |
| **Minimum detectable effect (proportions):** MDE = Zα/2 × √(p(1-p) × 2/n) | What effect size can this test detect? | Baseline rate p, sample n per variant, α |

## Verification

- [ ] Hypothesis written before experiment: "If we [change], then [metric] will [direction] because [reason]"
- [ ] Sample size calculated before experiment starts: target MDE, α=0.05, power=0.80, daily eligible users
- [ ] Experiment ran for pre-determined duration: no early stopping, minimum 1 full business week
- [ ] SRM check passed: chi-square test on variant assignment, p > 0.01
- [ ] Primary metric: lift, p-value, confidence interval reported — both statistical and practical significance
- [ ] Guardrail metrics checked: no significant degradation on key secondary metrics
- [ ] Segment analysis: results checked across new/returning, device, geo, and top customer segments
- [ ] Novelty effect check: metric plotted over experiment days, effect stable (not declining)
- [ ] Business impact estimated: lift converted to dollar range with 95% CI, implementation cost factored
- [ ] Executive summary written: 3 sentences — what was tested, business impact with uncertainty, recommendation
- [ ] Decision documented: ship/iterate/discard classification with rationale, learning captured for discarded tests
- [ ] Post-launch monitoring plan: guardrail re-check schedule (Day 7, Day 30), rollback criteria defined
- [ ] Experiment registry updated: hypothesis, design, results, and decision archived for future reference
- [ ] Peer review completed: at least one other data scientist or experienced experimenter has reviewed the analysis

## References

- **Sample Size Calculator**: See [references/sample-size.md](references/sample-size.md)
- **Statistical Test Selection Guide**: See [references/statistical-tests.md](references/statistical-tests.md)
- **Experiment Design Template**: See [references/experiment-design.md](references/experiment-design.md)
- **Results Communication Template**: See [references/results-template.md](references/results-template.md)
- **Anti-Patterns**: See [references/anti-patterns.md](references/anti-patterns.md)
- **Calibration**: See [references/calibration.md](references/calibration.md)
- **Production Checklist**: See [references/checklist.md](references/checklist.md)
- **Error Decoder**: See [references/error-decoder.md](references/error-decoder.md)
- **Footguns**: See [references/footguns.md](references/footguns.md)
- **Scale Depth**: See [references/scale-depth.md](references/scale-depth.md)
- **Sub-Skills**: See [references/sub-skills.md](references/sub-skills.md)
