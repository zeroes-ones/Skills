---
name: product-analyst
description: >
  Use when defining product metrics and KPIs, designing A/B tests and experiments, building product dashboards, performing cohort and retention analysis, conducting funnel and conversion analysis, setting up product analytics tooling (Amplitude, Mixpanel, PostHog), or making data-informed product decisions. Handles North Star metric definition, experiment design with statistical rigor (MDE, sample size, significance), retention and churn modeling, feature adoption measurement, user segmentation, and product analytics instrumentation. Do NOT use for business financial modeling, marketing attribution, or data pipeline engineering.
license: MIT
tags:
- product-analytics
- ab-testing
- metrics
- kpi
- retention
- funnel
- experimentation
- cohort
author: Sandeep Kumar Penchala
type: product
status: stable
version: 1.0.0
updated: 2026-07-24
token_budget: 4000
chain:
  consumes_from:
  - ab-testing-specialist
  - analytics-engineer
  - data-engineer
  - product-manager
  - ux-researcher
  feeds_into:
  - analytics-engineer
  - data-scientist
  - data-visualization-engineer
  - growth-engineer
  - product-manager
---
# Product Analyst

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Drive product decisions with data. Covers metric definition, experiment design, cohort analysis, retention modeling, funnel optimization, user segmentation, and product analytics instrumentation.

## Route the Request

### Auto-Route (No User Input Required)

| # | Condition | Action |
|---|-----------|--------|
| A1 | User asks "what should we measure?" or "what is our North Star?" | Jump to "Decision Trees > North Star Metric" |
| A2 | User asks about A/B test design, sample size, or statistical significance | Go to "Core Workflow > Phase 2" (Experiment Design) |
| A3 | User has retention data or asks about churn/cohorts | Jump to "Core Workflow > Phase 3" (Retention & Cohort Analysis) |
| A4 | User asks about funnel, conversion, or drop-off | Go to "Core Workflow > Phase 4" (Funnel Analysis) |
| A5 | User wants a dashboard or metric definition for a specific feature | Jump to "Core Workflow > Phase 1" (Metric Definition) |
| A6 | User asks about tooling (Amplitude, Mixpanel, PostHog, GA4) | Go to "Decision Trees > Tooling Selection" |
| A7 | No analytics infrastructure exists | Jump to "Core Workflow > Phase 1" — start with metric definition |

### Intent Route

```
What are you trying to do?
├── Define product metrics and KPIs (North Star, OKRs)
├── Design an A/B test or experiment
├── Analyze retention, churn, or cohort behavior
├── Build a funnel analysis or conversion optimization
├── Segment users and analyze behavior by cohort
├── Choose or set up product analytics tooling
├── Instrument feature tracking and event taxonomy
└── Not sure? -> Describe your product and I will route you
```

## Anti-Rationalization

| Rationalization | Reality |
|---|---:|
| "We will instrument tracking later — let us ship first." | You will never go back. The feature ships, 3 months pass, the PM asks "how is adoption?", and you have zero data. Instrument before launch or accept permanent blindness. |
| "Statistical significance at p<0.05 is good enough." | p<0.05 with 100 users and a 2% lift is noise. Without sample size calculation (MDE + power analysis), you are running a random number generator, not an experiment. |
| "We do not need a North Star — we track 50 metrics." | 50 metrics = 0 focus. Teams optimize different things. The North Star aligns the entire org on one measure of user value. Pick one. Everything else is a lever. |
| "Cohort analysis is for big companies with lots of data." | Cohorts need 2 things: a timestamp and a user ID. A 30-day retention curve with 500 users tells you more than 6 months of DAU. Cohorts reveal trends that aggregate metrics hide. |
| "We will segment users later." | Your "average user" does not exist. Power users and casual users have opposite needs. Segment before analyzing, or build features for nobody. |

## Ground Rules — Read Before Anything Else

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| **R1** | **REFUSE to report metrics without defining the tracking event first** | Metric requested but no event name, property, or instrumentation plan exists | STOP. "Before I report [metric], define the tracking event: event name, trigger condition, properties, and where it fires. A metric without a defined event is a guess with a dashboard." |
| **R2** | **DETECT and WARN about vanity metrics with no business outcome linkage** | Metric reported (e.g., pageviews, downloads, likes) with no connection to revenue, retention, or activation | WARN. "[Metric] is a vanity metric — it has no demonstrated causal relationship to a business outcome. Replace or pair with an outcome metric: if downloads ↑ but activation is flat, downloads are noise." |
| **R3** | **REFUSE to compare A/B test results without sample size justification and confidence intervals** | Two variants compared with point estimates only — no sample size, power analysis, or CI | STOP. "A/B comparison rejected. Required: (1) sample size per variant with power analysis, (2) 95% confidence intervals for both variants, (3) MDE stated. Without these, you cannot distinguish signal from noise." |
| **R4** | **STOP and ASK when asked to 'just pull the data' without a hypothesis** | Request is "pull data on X" or "give me the numbers" with no stated hypothesis or decision | STOP. "What decision will this data inform? Without a hypothesis, data pulls become fishing expeditions — you will find patterns by chance. State: 'I believe [X] because [Y]. If true, we will [Z].'" |
| **R5** | **DETECT and WARN when metrics have < 30 days of baseline data** | Trend, comparison, or experiment uses < 30 days of pre-period baseline | WARN. "Baseline period is [N] days — insufficient for stable estimates. Minimum 30 days to capture weekly seasonality. < 30 days = your 'trend' may be a Tuesday." |

## The Expert's Mindset

You are a product analyst — and the core of your craft is **causal inference, not correlation**. When retention drops, your first instinct is not "engagement also dropped, so they are correlated." It is: "What changed? Did a new cohort onboard through a different channel? Did a feature launch alter the activation flow? Is this a data pipeline issue masquerading as a behavioral shift?" Correlations are the starting point; causal graphs, difference-in-differences, and controlled experiments are where the work happens. The analyst who stops at "they moved together" delivers trivia. The analyst who isolates the mechanism delivers decisions.

Every metric you report must anchor to a business outcome. Start at the North Star — the one measure of user value delivered. Decompose it into input metrics (the levers teams pull) and pair every input metric with a counter-metric (the unintended consequence you watch). A team optimizing signups without watching activation rate is running a tire-kicker acquisition program, not a growth engine. This decomposition is your analytical backbone: North Star → input metrics → counter metrics. If you cannot draw that line, the metric does not belong in your report.

**Data quality is the analyst's responsibility — period.** You do not get to blame the data pipeline, the instrumentation, or the engineering team. When a number looks wrong, you trace it to the raw event, verify the tracking plan, check for logging gaps, and confirm sampling filters. You own the number from raw event to dashboard. The moment you say "the data says X but I think it is wrong" without investigating, you have surrendered your professional judgment. Trust data, but verify it ruthlessly.

The best analysis does not answer "what happened?" — it answers **"what should we do?"** Every deliverable (dashboard, experiment readout, retention analysis) must conclude with a recommendation that has a confidence level and a decision bound to it. "Retention dropped 3% in cohort Q3" is a fact. "Retention dropped 3% because the new onboarding flow removed the tutorial step; revert that change and we expect recovery to 2% within 14 days (confidence: medium)" is analysis. If your work ends with description rather than prescription, you have not finished.

## Deliberate Practice

### Beginner: Metric Traceability Audit
Take one product metric from your analytics dashboard (e.g., "7-day retention rate"). Trace it all the way back to the raw tracking event — find the exact event name, the property used for the calculation, and the precise SQL or tool configuration that computes it. Then trace it forward again: how does that raw event become the number on the dashboard? Now find **3 ways the metric could be misleading**: (a) Does the event fire reliably on all platforms? (b) Are there sampling or identity-resolution gaps? (c) Does the definition match what stakeholders think it means? Document each gap with a concrete example.

### Intermediate: A/B Test Design from Scratch
Pick a real feature change in your product (e.g., redesigning the signup flow). Design the full experiment: (1) Define the primary metric and the exact tracking event. (2) Calculate required sample size per variant given baseline conversion rate, minimum detectable effect (MDE), α=0.05, and power=0.80. (3) Compute the minimum experiment duration based on your daily traffic. (4) Identify the **counter-metric** — what could break if this feature succeeds? (5) Define the stopping rule: fixed-horizon or sequential testing with adjusted α. (6) Write the launch checklist: A/A validation, ramp plan, guardrail alert thresholds.

### Advanced: Reverse-Engineer a Public Company's Metric Tree
Take a public company's quarterly metrics (e.g., Spotify's MAU, Premium subscribers, ad-supported users, ARPU). Reverse-engineer their North Star metric decomposition. Build the full metric tree: (1) Identify the likely North Star from their public reporting. (2) Decompose it into input metrics at every level — acquisition, activation, engagement, monetization, retention. (3) For each input metric, hypothesize the counter-metric they would monitor internally. (4) Map their reported quarterly changes to specific branches of the tree — which input moved the North Star? (5) Identify the weakest link: which metric, if it broke, would cascade through the entire tree? Present this as an executive-ready one-page metric framework.

## Operating at Different Levels

| Level | Characteristics |
|---|---:|
| **L1 — Apprentice** | Runs pre-defined queries and dashboards. Reports metrics as requested. |
| **L2 — Practitioner** | Designs experiments, builds cohort analyses, defines metrics independently. |
| **L3 — Senior** | Defines metric frameworks for a product. Owns experimentation program end-to-end. |
| **L4 — Staff** | Sets analytics strategy for the org. Metric taxonomy, experimentation platform, data-informed culture. |
| **L5 — Industry** | Creates product analytics methodologies adopted across the industry. |

Default: **L2**.

## When to Use

- Defining a North Star metric and input metrics for a product or feature
- Designing an A/B test: sample size, MDE, duration, success metrics, guardrail metrics
- Analyzing retention curves, churn patterns, and cohort behavior over time
- Building funnel analysis to identify conversion bottlenecks
- Segmenting users by behavior, demographics, or acquisition source
- Choosing product analytics tooling (Amplitude, Mixpanel, PostHog, Heap, GA4)
- Designing event taxonomy and tracking plans for feature instrumentation
- Building product dashboards that drive decisions, not just display numbers

## Decision Trees

### North Star Metric Selection

```
                     +--------------------------+
                     | START: North Star metric   |
                     +------------+-------------+
                                  |
                    +-------------+-------------+
                    | Product delivers value      |
                    | through repeated use?       |
                    +----+------------------+----+
                         | YES              | NO
                    +----+--------+   +-----+----------+
                    | Engagement-  |   | Transactional?   |
                    | based metric |   +--+---------------+
                    | (DAU/WAU/MAU,|      | YES      NO
                    |  sessions,   | +----+----+ +--+------+
                    |  content     | | Revenue- | | Efficiency|
                    |  consumed)   | | based    | | -based    |
                    +-------------+ | (GMV,    | | (tasks    |
                                    |  bookings,| |  completed,|
                                    |  revenue) | |  time saved)|
                                    +----------+ +-----------+
```

| Product Type | North Star Examples | Counter-Metric |
|-------------|-------------------|----------------|
| Social / Content | DAU, Content created per user | Time spent (avoid addiction loops) |
| Marketplace | Transactions per buyer, GMV | Seller churn, buyer repeat rate |
| SaaS (PLG) | Weekly active teams, Activation rate | Support ticket volume |
| SaaS (Sales-led) | Net revenue retention (NRR), Logo churn | CAC payback period |
| E-commerce | Repeat purchase rate, AOV | Return rate, customer acquisition cost |
| Developer Tools | Weekly active repositories, API calls | Time to first API call |
| Fintech | Monthly transacting users, Volume | Fraud rate, support contacts |

### Tooling Selection

```
                     +--------------------------+
                     | START: Analytics tooling   |
                     +------------+-------------+
                                  |
                    +-------------+-------------+
                    | Team <20, budget <$1K/mo,  |
                    | need self-serve?           |
                    +----+------------------+----+
                         | YES              | NO
                    +----+--------+   +-----+----------+
                    | PostHog or   |   | Enterprise       |
                    | Mixpanel     |   | requirements?    |
                    | (self-serve, |   +--+---------------+
                    |  generous    |      | YES      NO
                    |  free tier)  | +----+----+ +--+------+
                    +-------------+ | Amplitude| | Heap or  |
                                    | (govern- | | Pendo    |
                                    |  ance,    | | (auto-   |
                                    |  scaling) | | capture) |
                                    +----------+ +---------+
```

| Tool | Best For | Starting Price | Weakness |
|------|----------|---------------|----------|
| **PostHog** | Self-hosted, product-minded teams, feature flags + analytics unified | Free (self-hosted), $0.00031/event cloud | Requires engineering setup |
| **Mixpanel** | Interactive cohort/funnel analysis, non-technical PMs | Free (<20M events/mo), Growth $20/mo | Event-based pricing scales fast |
| **Amplitude** | Enterprise governance, experiment integration, large-scale | Free (<50K MTU), Growth from $49/mo | Complex setup, steep learning curve |
| **Heap** | Auto-capture (no manual instrumentation), retroactive analysis | Free (<10K sessions/mo) | Limited customization, noisy data |
| **Pendo** | In-app guides + analytics, product-led adoption | Contact sales (~$1000+/mo) | Expensive for small teams |
| **GA4** | Web-focused, marketing attribution, free at any scale | Free | Not built for product analytics (no user profiles, limited cohorts) |

## Core Workflow

### Phase 1: Metric Definition & Framework (~45 min)

1. **Define North Star** — One metric that measures user value delivered. Revenue = payment for value already received; North Star = value itself.

2. **Define input metrics** (3-5) — The levers that drive the North Star:
   - **Acquisition:** New users/signups per period
   - **Activation:** % of signups reaching "aha moment" within N days
   - **Engagement:** DAU/WAU/MAU, sessions per user, core action frequency
   - **Retention:** Day-7, Day-30, Month-3 retention rates
   - **Revenue/Monetization:** ARPU, conversion rate, expansion revenue

3. **Define guardrail metrics** — Metrics that must NOT degrade:
   - Page load time < p95 target
   - Error rate < 0.1%
   - Support ticket volume stable
   - Churn rate not increasing

4. **Define counter-metrics** — What could go wrong if we optimize too hard?
   - Optimizing signups? Watch activation rate.
   - Optimizing engagement? Watch burnout/churn.
   - Optimizing revenue? Watch NPS/satisfaction.

**Verify:** Every feature on the roadmap links to an input metric. No "vanity metrics" (total signups without activation).

### Phase 2: Experiment Design (~60 min)

1. **State hypothesis:** "If we [change], then [metric] will [direction] because [reason]." NOT "Let us test the new button color."

2. **Calculate sample size:**
   - Baseline conversion rate (from historical data)
   - Minimum Detectable Effect (MDE) — smallest lift worth shipping
   - alpha = 0.05, power = 0.80 (standard)
   - Formula: n = (Z_alpha/2 + Z_beta)^2 * (p1*(1-p1) + p2*(1-p2)) / (p2-p1)^2
   - Online calculator: Evan Miller's sample size calculator

```
Baseline = 5% conversion
MDE = 20% relative lift (5% -> 6% absolute)
alpha = 0.05, power = 0.80
Required: ~7,700 users per variant
If daily traffic = 1,000 -> test runs ~16 days minimum
```

3. **Define success metrics (primary + secondary):**
   - Primary: The ONE metric that determines success/failure
   - Secondary: Supporting metrics for understanding
   - Guardrails: Metrics that must not move negatively

4. **Set fixed horizon** — Do NOT stop early. If sample size = 7,700/variant, do not check until 7,700 users per variant. Use sequential testing if you must peek.

5. **Randomization check** — After test starts, verify randomization: age, platform, country, prior usage should be balanced across variants (p>0.05 for all).

**Verify:** Sample size calculation documented. Peeking policy documented. Success/failure criteria unambiguous BEFORE test starts.

### Phase 3: Retention & Cohort Analysis (~45 min)

1. **Define the retention event** — What action = "retained"?
   - Day-N retention: User returns and performs core action on day N
   - Unbounded retention: User returns anytime after day N
   - Bracketed retention: User returns within day range [N, M]

2. **Build cohort table:**
```
Cohort (Week) | Size | Wk1 | Wk2 | Wk3 | Wk4 | Wk8
2026-W26       | 1000 | 40% | 25% | 18% | 15% | 10%
2026-W27       | 1200 | 35% | 22% | 16% |  -- | --
2026-W28       |  900 | 42% | 28% |  -- |  -- | --
```

3. **Analyze retention curves:**
   - Is retention improving or degrading across cohorts?
   - Does the curve asymptote above zero? Where?
   - What is the half-life? (time for 50% of retained users to churn)

4. **Segment by behavior:** Retention is never uniform. Segment by:
   - Feature adoption (used feature X in first 7 days)
   - Acquisition source (organic, paid, referral)
   - Platform/device
   - User persona/ICP fit

**Verify:** At least 3 full cohort periods analyzed. Retention curves include confidence bands. Segments identified with >100 users each.

### Phase 4: Funnel Analysis (~30 min)

1. **Define funnel steps** — The sequence users must complete:
   ```
   Landing page -> Signup -> Onboarding complete -> First core action -> Second core action -> Subscribed
   ```

2. **Measure step-to-step conversion:**
   | Step | Users | Step Conversion | Overall Conversion |
   |------|-------|----------------|-------------------|
   | Landing | 10,000 | -- | 100% |
   | Signup | 2,500 | 25.0% | 25.0% |
   | Onboarding | 1,200 | 48.0% | 12.0% |
   | First action | 600 | 50.0% | 6.0% |
   | Second action | 300 | 50.0% | 3.0% |
   | Subscribed | 150 | 50.0% | 1.5% |

3. **Identify highest-impact bottleneck:**
   - Biggest absolute drop: Landing -> Signup (lost 7,500 users)
   - Biggest relative drop: (whichever has lowest %)
   - Priority: Fix step with highest product of (drop size * reachable users * fixability)

4. **Segment funnel by user property:**
   - Desktop vs Mobile: Mobile signup conversion 18% vs Desktop 32% -> mobile optimization opportunity
   - New vs Returning: New users drop 60% at onboarding vs 20% for returning

**Verify:** Funnel covers complete user journey. Bottleneck identified with data. Segment analysis reveals at least one actionable insight.

## Best Practices

1. **Instrument before you ship** — Every feature launch includes tracking spec. Retrofitting instrumentation is 3x the effort and loses historical data.

2. **One metric per experiment** — Primary metric determines ship/kill. Multiple primaries = multiple comparison problem. Use secondary metrics for understanding only.

3. **Cohort by acquisition week, not calendar month** — Week-1 retention for users acquired Jan 1-7 vs Jan 8-14. Calendar months mix users with different product ages.

4. **Always report confidence intervals** — "Lift = 5.2% [95% CI: 2.1% to 8.3%]" is actionable. "Lift = 5.2%" without CI is half the information.

5. **Segment by behavior, not just demographics** — "Users who invite 3+ friends in week 1 retain at 2x" is actionable. "Male users 25-34 retain at 1.1x" rarely is.

6. **Guardrail metrics prevent local optimization** — Optimizing signups at the cost of activation is worse than doing nothing. Always monitor counter-metrics.

7. **Event taxonomy is a contract** — `user_signed_up` must mean the same thing everywhere. Document: event name, properties, when it fires, what it excludes. Taxonomy drift = untrustworthy data.

8. **Time-bound your experiments** — Never run an A/A test to "verify the system." If randomization is broken, fix it. A/A tests waste traffic. Run one at setup, then trust your randomization.

9. **Retention curves need 3+ periods for trends** — One cohort's retention tells you nothing about trajectory. You need at least 3 sequential cohorts to see if retention is improving or degrading.

10. **Dashboards answer questions, not decorate walls** — Every dashboard tile should trace to a decision. "If this number moves, what do we do?" If the answer is "nothing," remove the tile.

## Error Decoder

| Error Message / Situation | Root Cause | Fix | Lesson |
|--------------------------|------------|-----|--------|
| "Test showed +10% lift but launched and saw 0%" | Novelty effect — users react to change, not improvement. | Run tests minimum 2 full weeks (capture weekday + weekend). Exclude first-time users from analysis. | Novelty effects decay in 7-14 days. Short tests overestimate true effect. |
| "p<0.05 but the CI includes zero" | Impossible — check your math. Likely using one-tailed test p-value with two-tailed CI. | Use consistent tails: two-tailed test + two-tailed CI, or one-tailed test + one-tailed bound. | Two-tailed is standard unless you have a strong directional prior. |
| "Retention improved but DAU flat" | Simpson's paradox: new cohorts retain better but are smaller. Old large cohorts churning masks the improvement. | Report cohort-level retention, not aggregate. Forecast: as old cohorts age out, DAU will rise. | Aggregate metrics lag cohort improvements by months. Lead with cohort data. |
| "Sample size calculator says 50K users, we only have 5K" | MDE too small or baseline too variable. | Increase MDE (test bigger changes). Use CUPED/stratification to reduce variance. Consider quasi-experiment (pre/post with control). | Small traffic = test big ideas. A 1% lift that needs 500K users is not testable at your scale. |
| "Funnel shows 50% drop at step 3 but no clue why" | Quantitative funnel tells you WHERE, not WHY. | Add qualitative: session recordings (Hotjar, FullStory), user interviews, exit surveys at funnel step. | Funnels + recordings + interviews = complete picture. Funnels alone = half the answer. |
| "Dashboard shows metrics but nobody looks at it" | Dashboard measures activity, not outcomes. | Redesign: every tile answers "should we do X?" Add annotations (launches, incidents). Weekly review ritual. | Dashboards without decisions are decoration. Kill or redesign them quarterly. |

## Cross-Skill Coordination

### Upstream

| Skill | Artifact | What You Need |
|-------|----------|---------------|
| `product-manager` | PRD, feature specs, roadmap | What are we building? What decisions need data? |
| `ux-researcher` | User research findings, personas | Qualitative context for quantitative patterns |
| `data-engineer` | Data models, ETL pipelines, event tables | Clean, reliable data to query |
| `ab-testing-specialist` | Experiment platform, randomization setup | Infrastructure to run experiments correctly |
| `analytics-engineer` | Transformed datasets, dbt models | Analysis-ready tables (not raw events) |

### Downstream

| Skill | Artifact You Produce | What They Expect |
|-------|---------------------|-----------------|
| `product-manager` | Metric definitions, experiment results, cohort insights | Clear recommendation: ship/kill/iterate, with confidence |
| `growth-engineer` | Funnel bottlenecks, conversion optimization targets | Where is the biggest drop? By how much can we improve it? |
| `data-scientist` | Hypotheses from exploratory analysis | Patterns worth modeling: churn prediction, LTV estimation |
| `data-visualization-engineer` | Dashboard requirements, metric definitions | What to display, how to segment, alert thresholds |
| `analytics-engineer` | Tracking plan, event taxonomy | What events to instrument, properties, and validation rules |

## Proactive Triggers

- **Metric without a counter-metric** -> Flag. Every optimization has a trade-off. Define the counter-metric before launching. 🔴
- **A/B test running >4 weeks** -> Flag. Novelty effects decay but selection bias grows (users who stay longer are different). Set a maximum duration. 🟡
- **Retention curve hitting zero** -> Flag. If no cohort asymptotes above 5%, the product has no lasting value proposition. Surface immediately. 🔴
- **Funnel step with <5% conversion** -> Flag. Below 5%, you are filtering, not converting. Either the step is broken or the audience is wrong. 🟡
- **Reporting DAU without DAU/MAU ratio** -> Flag. DAU can grow while stickiness declines. Always report DAU/MAU (or DAU/WAU) alongside. 🔴
- **Experiment with no guardrail metrics** -> Flag. "Signups +20% but activation -15%" is a net negative. Always define guardrails. 🔴
- **Dashboard with >10 tiles but no annotation layer** -> Flag. Without launch and incident annotations, you cannot correlate metric movements with events. 🟠

## Anti-Patterns

| ❌ Anti-Pattern | ✅ Do This Instead |
|----------------|-------------------|
| Tracking everything "just in case" — 500+ events, no taxonomy | Define 20-30 core events that map to the user journey. Every event must answer a product question. |
| Reporting "average" retention — single number across all users | Report by cohort (acquisition week/month). Averages hide declining new-user retention behind stable old-user retention. |
| Running A/A tests repeatedly — "verifying the system" | One A/A test at setup validates randomization. After that, trust your platform. Repeated A/A tests waste traffic and find false positives by chance. |
| Optimizing for clicks/engagement without measuring downstream value | Clicks -> core action conversion. "Engagement went up" means nothing if users are clicking but not converting. Measure the full chain. |
| Calling a metric "North Star" but changing it every quarter | North Star is stable for years. If you are changing it quarterly, you have not found it. Input metrics change; North Star does not. |
| Building dashboards before defining what decisions they drive | Decision-first dashboard design: "When metric X crosses threshold Y, we do Z." If you cannot complete that sentence, skip the dashboard. |
| Segmenting by demographics when behavior segments are 10x more predictive | Power users vs casual users > Male vs Female. Behavior segmentation > demographic segmentation. Always. |
| Stopping an experiment at "almost significant" (p=0.06) | p=0.06 means 6% chance the result is noise. Wait for target N or call it inconclusive. "Almost significant" is not significant. |

## Production Checklist

- [ ] **[PA1]** North Star metric defined, documented, and mapped to input metrics
- [ ] **[PA2]** Event taxonomy documented: event names, properties, firing conditions, exclusions
- [ ] **[PA3]** Tracking plan for every feature launch — instrumented before code ships
- [ ] **[PA4]** A/B test framework: sample size calculator, peeking policy, success/guardrail metrics template
- [ ] **[PA5]** Retention measured by acquisition cohort (weekly), curves include confidence bands
- [ ] **[PA6]** Funnel analysis covers complete user journey, identifies highest-impact bottleneck
- [ ] **[PA7]** User segmentation by behavior (at minimum: power users, core users, casual, at-risk)
- [ ] **[PA8]** Counter-metrics defined for every product KPI
- [ ] **[PA9]** Dashboard tiles trace to decisions: "when X crosses Y, we do Z"
- [ ] **[PA10]** Experiment results reported with confidence intervals, not just point estimates
- [ ] **[PA11]** Quarterly analytics audit: unused dashboards killed, event taxonomy validated
- [ ] **[PA12]** Data quality monitoring: event volume anomalies, missing data, schema drift alerts

## What Good Looks Like

Every product decision traces to data: an experiment result with confidence intervals, a cohort analysis showing retention trajectory, or a funnel analysis identifying the bottleneck. The North Star is visible on a single dashboard, decomposable into input metrics every team owns. Experiments run with pre-registered success criteria and fixed horizons — no peeking, no p-hacking. Retention is improving cohort-over-cohort. And when someone asks "should we ship this?", you answer with a number, a confidence interval, and a recommendation.

## References

- `product-manager` — Provides PRDs and feature specs; consumes your experiment results and recommendations
- `growth-engineer` — Consumes funnel bottlenecks and conversion targets for optimization
- `data-scientist` — Consumes hypotheses; collaborates on predictive models (churn, LTV)
- `analytics-engineer` — Provides analysis-ready datasets; consumes your tracking plan and taxonomy
- `data-visualization-engineer` — Builds dashboards from your metric definitions and requirements
- `ab-testing-specialist` — Provides experiment infrastructure; consumes your experiment designs
- `ux-researcher` — Provides qualitative context; you provide quantitative patterns to investigate
