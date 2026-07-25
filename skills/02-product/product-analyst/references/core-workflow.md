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
