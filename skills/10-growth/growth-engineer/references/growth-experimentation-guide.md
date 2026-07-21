---
name: growth-experimentation-guide
description: A/B testing infrastructure, growth loops, activation frameworks, feature flagging patterns, and experimentation culture.
author: Sandeep Kumar Penchala
---

# Growth Experimentation Guide

Build a culture of rigorous experimentation. Covers A/B testing infrastructure, statistical
methods, growth loop design, activation frameworks, and feature flagging for safe,
measured product growth.

## 1. A/B Testing Infrastructure

### 1.1 Architecture

```
┌──────────┐     ┌──────────────┐     ┌──────────────────┐
│ User      │────▶│ Assignment    │────▶│ Variant A or B   │
│ Request   │     │ Service       │     │ (via feature flag)│
└──────────┘     └──────┬───────┘     └────────┬─────────┘
                        │                      │
                   ┌────▼──────┐          ┌────▼──────────┐
                   │ Event Log  │◀─────────│ Instrumentation│
                   │ (analytics)│          │ (events, props)│
                   └────┬──────┘          └───────────────┘
                        │
                   ┌────▼──────┐
                   │ Metrics    │
                   │ Pipeline   │
                   └────┬──────┘
                        │
                   ┌────▼──────┐
                   │ Analysis   │
                   │ Engine     │
                   └───────────┘
```

### 1.2 Randomization

**Hashing for consistent assignment:**
```python
import hashlib

def get_variant(user_id: str, experiment_id: str, variants: list[str]) -> str:
    """Deterministic variant assignment based on user_id + experiment."""
    seed = f"{experiment_id}:{user_id}"
    hash_val = int(hashlib.md5(seed.encode()).hexdigest(), 16)
    return variants[hash_val % len(variants)]
```

**Properties of good assignment:**
- Deterministic: same user always gets same variant (within experiment)
- Uniform: each variant gets ~equal traffic (with large N)
- Independent across experiments: exp A assignment doesn't predict exp B
- Sticky: user keeps same variant for experiment duration

### 1.3 Sample Ratio Mismatch (SRM) Detection

SRM = the observed traffic split significantly differs from expected. This is a **fatal**
validity threat — if SRM exists, the experiment is invalidated regardless of results.

**Detection:**
```python
from scipy.stats import chi2_contingency

# Expected: 50/50 split with 10,000 users
expected = [5000, 5000]
observed = [5100, 4900]  # actual assignments

chi2, p_value, _, _ = chi2_contingency([observed, expected])
# If p_value < 0.01 → SRM detected → investigate immediately
```

**Common SRM causes:**
- Bug in assignment code (hash collision, modulo error)
- Bot traffic not filtered (bot always gets same variant)
- Variant-specific crashes cause differential drop-off
- Data pipeline filters one variant's events
- Ramp-up: one variant deployed before the other

**Rule:** Run SRM check daily for every active experiment. P-value < 0.01 → pause and investigate.

### 1.4 Statistical Framework: Frequentist vs Bayesian

**Frequentist (NHST — Null Hypothesis Significance Testing):**
```
H₀: variants are identical (no effect)
H₁: variants differ

Compute p-value: probability of observing data (or more extreme) if H₀ is true
If p < 0.05 → reject H₀ → "statistically significant"
```

**Limitations:**
- Can't say "probability that B is better" — only "probability of data given H₀"
- Peeking inflates false positive rate (if you check daily and stop when significant, actual FPR is 20–40% not 5%)
- p-value doesn't tell you effect size or practical significance
- Requires pre-declared sample size

**Bayesian:**
```
Start with prior belief about effect → update with data → posterior distribution

Output: "There's a 92% probability that B is better than A, with expected lift of 2.3% (±1.1%)"
```

**Advantages:**
- Intuitive output: probability that B beats A
- Can peek safely: posterior updates naturally with more data
- Incorporates prior knowledge (previous experiments, domain expertise)
- Directly estimates effect size with credible intervals

**Recommendation:** Use Bayesian for most product experiments. Use frequentist when regulatory or academic requirements demand it.

### 1.5 Minimum Detectable Effect (MDE)

The smallest effect you care about detecting. Drives sample size requirements.

```python
import statsmodels.stats.api as sms

# Frequentist sample size calculation
effect_size = 0.02     # 2% relative improvement
alpha = 0.05           # significance level
power = 0.80           # 80% chance of detecting true effect

sample_size = sms.NormalIndPower().solve_power(
    effect_size=effect_size,
    alpha=alpha,
    power=power,
    ratio=1.0           # 50/50 split
)
# → ~15,700 per variant
```

**MDE calibration by metric:**
| Metric               | Typical MDE | Why                                   |
|----------------------|-------------|---------------------------------------|
| Conversion rate       | 1–2% relative| Small changes matter at scale        |
| Revenue per user      | 0.5–1%      | Requires large N; use CUPED           |
| Click-through rate    | 2–5%        | High variance, need larger MDE        |
| Retention (D30)       | 3–5%        | Long measurement window, small effects hard to detect |
| Time on page          | 3–5%        | High variance metric                  |

### 1.6 Variance Reduction with CUPED

Controlled-experiment Using Pre-Experiment Data: adjust metrics by pre-experiment behavior
to reduce variance by 30–50%.

```python
# CUPED-adjusted metric
def cuped_adjust(Y_exp, Y_pre, X_exp, X_pre):
    """Adjust experiment metric by pre-experiment covariate."""
    theta = np.cov(Y_pre, X_pre)[0][1] / np.var(X_pre)
    Y_adjusted = Y_exp - theta * (X_exp - np.mean(X_pre))
    return Y_adjusted

# Usage:
# Y: conversion rate during experiment
# X: conversion rate in 2 weeks before experiment
# Result: same expected value, 30-50% lower variance → smaller sample needed
```

**Good pre-experiment covariates:**
- Same metric in pre-period (e.g., pre-experiment conversion rate)
- Related stable metrics (e.g., pre-period login frequency for retention experiments)
- User tenure, total historical spend

### 1.7 Multiple Testing Correction

If you test 20 metrics per experiment, you'll get ~1 false positive by chance (at α=0.05).

**Corrections:**
- **Bonferroni**: divide α by number of tests (α_adjusted = 0.05/20 = 0.0025). Conservative.
- **Benjamini-Hochberg**: control False Discovery Rate. Less conservative, preferred for exploration.
- **Pre-register primary metric**: the ONE metric that decides ship/kill. Others are directional only.

```
Always: 1 primary metric → go/no-go decision
        3–5 secondary metrics → supporting evidence, directional
        Guardrail metrics → must NOT degrade (latency, crash rate, support tickets)
```

## 2. Growth Loops

### 2.1 Loop Types

**Viral Loop:**
```
User discovers product → Uses product → Shares/invites → New user discovers → ...
```
Metrics: viral coefficient (K-factor = invites_sent × conversion_rate), cycle time
Goal: K-factor > 1 for exponential growth

**Content Loop:**
```
Company creates content → Content ranks/gets shared → New users discover → Users engage/conver
```
Metrics: organic traffic growth, content-to-signup rate, content ROI
Goal: compounding traffic from SEO and social

**Paid Acquisition Loop:**
```
Spend $X on ads → Acquire users for $CPA → Users generate $LTV → Reinvest profit → ...
```
Metrics: LTV:CAC ratio, payback period, marginal CPA
Goal: LTV:CAC > 3:1, payback < 12 months

**Sales-Led Loop:**
```
Outbound → Demo → Close → Revenue → Hire more sales reps → More outbound → ...
```
Metrics: pipeline generated per rep, win rate, average deal size, ramp time
Goal: predictable pipeline, CAC payback < 18 months

**Product-Led Loop:**
```
Free product → Usage hits limit/aha moment → Upgrade to paid → Usage expands → ...
```
Metrics: free-to-paid conversion, activation rate, expansion revenue
Goal: self-serve revenue > 40% of total

### 2.2 Loop Measurement

For each loop, track:

| Metric                | What It Tells You                                    |
|-----------------------|------------------------------------------------------|
| Input rate            | How fast users enter the loop                        |
| Conversion rate       | What % move to the next step                         |
| Cycle time            | How long one full loop takes                         |
| Output rate           | How many users emerge from the loop                  |
| Loop efficiency       | Output / Input (ideally >1, self-sustaining)         |
| Compounding rate      | MoM growth in loop output                            |

## 3. Activation Frameworks

### 3.1 AARRR Pirate Metrics

```
Acquisition  — Where do users come from?
Activation   — Do they have a great first experience?
Retention    — Do they come back?
Revenue      — How do you make money?
Referral     — Do they tell others?
```

### 3.2 Habit-Forming Loop (Hook Model)

```
TRIGGER (external: notification, email; internal: boredom, need)
   │
   ▼
ACTION (simplest behavior in anticipation of reward)
   │
   ▼
VARIABLE REWARD (tribe: social validation; hunt: material/info; self: mastery)
   │
   ▼
INVESTMENT (user puts in effort → increases likelihood of next loop: data, followers, content)
   │
   └──→ back to TRIGGER
```

### 3.3 Activation Metric Design

The activation metric should be the earliest user action that predicts long-term retention.

**Finding your activation metric:**
1. List candidate actions: completed profile, invited teammate, created first project, used feature X
2. For each action, compare D30 retention: users who did action vs didn't
3. Pick the action with the largest retention differential
4. This becomes your North Star activation metric

**Example:** Slack found that teams who sent 2,000 messages reached the "sticky" threshold.

## 4. Feature Flagging

### 4.1 Flag Types

| Type              | Use Case                          | Lifetime    | Example                            |
|-------------------|-----------------------------------|-------------|------------------------------------|
| Release flag      | Decouple deploy from release      | Days        | New feature hidden until ready     |
| Experiment flag   | A/B test                          | 2–4 weeks   | "50% see old checkout, 50% see new"|
| Ops flag          | Kill switch for risky code        | Permanent   | Disable ML recommendation if broken |
| Permission flag   | Entitlement-based access          | Long-term   | "Premium users see advanced reports"|
| Migration flag    | Gradual rollout of infra changes  | Weeks       | "10% traffic to new DB cluster"    |

### 4.2 LaunchDarkly Patterns

**Targeting rules (priority order):**
1. User whitelist (internal testers, beta users)
2. User segment (country, plan type, device)
3. Percentage rollout (random hash assignment)
4. Default rule (on/off for everyone else)

**Kill switch design:**
```javascript
// ALWAYS wrap new features in a flag
if (await ldClient.variation("new-checkout-flow", user, false)) {
    renderNewCheckout();
} else {
    renderOldCheckout();  // battle-tested fallback
}
```

**Gradual rollout:**
```
Phase 1: Internal team (0.1%)         — 1 day: smoke test
Phase 2: Beta users (1%)              — 2 days: early feedback
Phase 3: 10% of all users             — 3 days: monitor metrics
Phase 4: 25%                          — 3 days: verify at scale
Phase 5: 50%                          — 3 days
Phase 6: 100%                         — Clean up flag after 1 week
```

### 4.3 Flag Hygiene

- **Flag debt is real**: every flag is tech debt. Plan removal in the same sprint as rollout.
- **Naming convention**: `{team}.{feature}.{purpose}` e.g., `growth.checkout.redesign-v2`
- **Flag lifecycle**: `adding → ready → active → removing → removed`
- **Stale flag detection**: flag not evaluated in 30 days → alert team → remove within 14 days
- **Never nest flags**: complexity explodes. `if (flagA && !flagB || flagC)` is untestable.

## 5. Experimentation Culture

### 5.1 Experiment Cadence

| Org Maturity | Weekly Experiments | Win Rate | Key Challenge                |
|--------------|--------------------|----------|------------------------------|
| Starting     | 0–2               | 10–20%   | Building infrastructure       |
| Emerging     | 3–5               | 20–30%   | Generating good hypotheses    |
| Scaling      | 10–20             | 30–40%   | Avoiding interference         |
| Mature       | 50+               | 40–50%   | Prioritization and velocity   |

### 5.2 Hypothesis Template

```
We believe that [change]
will cause [impact on metric]
for [target user segment]
because [reasoning/evidence].

We'll know this is true when we see [quantitative signal]
with [statistical confidence level].

Experiment: [name]
Owner: [name]
Duration: [X] days
Primary metric: [name]
Guardrail metrics: [name, name]
```

### 5.3 Results Template

```markdown
# Experiment Results: [Name]

## Summary
[One sentence: did it work? Expected lift vs actual]

## Results
| Metric        | Control | Treatment | Lift      | P-value / Prob |
|---------------|---------|-----------|-----------|----------------|
| Primary       | 12.3%   | 12.8%     | +4.1%     | 94% prob B>A   |
| Guardrail 1   | 1.2s    | 1.3s      | +8.3%     | 89% prob worse |
| Guardrail 2   | 0.5%    | 0.48%     | -4.0%     | Not sig        |

## Decision
[SHIP / KILL / ITERATE / MORE DATA NEEDED]

## Learnings
- [Qualitative insight from user behavior]
- [Surprising result worth investigating further]
- [What we'd do differently next time]
```

## References

- Trustworthy Online Controlled Experiments (Kohavi, Tang, Xu): https://experimentguide.com/
- CUPED: https://dl.acm.org/doi/10.1145/2433396.2433413
- Statistical Methods in Online A/B Testing (Georgi Georgiev): https://www.abtestingstats.com/
- LaunchDarkly: https://docs.launchdarkly.com/
- Growth Loops (Reforge): https://www.reforge.com/blog/growth-loops
- Hooked (Nir Eyal): https://www.nirandfar.com/hooked/
