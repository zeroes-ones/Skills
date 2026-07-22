# MVP Growth Experiments

> **Audience:** 1-3 person startups (pre-PMF to 1K users) running growth experiments on zero budget.  
> **Principle:** You don't need a platform. You need analytics + feature flags + a spreadsheet.

---

## The MVP Growth Stack (Total: $0-20/mo)

| Component | Free Option | What It Does | When to Upgrade |
|-----------|-------------|-------------|-----------------|
| Analytics | PostHog (self-hosted, free) or Plausible ($9/mo) | Event tracking, funnel analysis, cohorts | >1M events/mo or need warehouse sync |
| Feature flags | JSON file in your codebase or DB config table | Toggle features, run 50/50 splits | >5 active flags, need % rollouts, or non-engineer toggling |
| A/B test analysis | Google Sheets + manual t-test | Calculate significance, lift, confidence | >2 experiments/month (automation saves time) |
| Session recording | PostHog (included, free up to 5K recordings) | See where users click, rage-click, get stuck | >5K recordings/mo |
| User surveys | Google Forms (free) or Tally (free) | Qualitative data for hypothesis generation | Need in-app triggers or NPS tracking |

**Total monthly cost at MVP: $0-20.** Growth tooling only becomes worth paying for when manual analysis takes more time than the tool costs.

---

## MVP Experiment Framework (No Platform Required)

### Step 1: Instrumentation (1 day)

```javascript
// The ONLY analytics event you need at MVP
analytics.track(eventName, {
  // Standard properties on every event
  userId: user.id,
  plan: user.plan,           // free | pro | enterprise
  signupDate: user.createdAt, 
  // Event-specific properties
  ...eventProperties
});

// Critical events to track (start with these 7):
// 1. user_signed_up       → acquisition
// 2. user_activated        → reached "aha moment"
// 3. user_invited_teammate → viral behavior
// 4. project_created       → core action
// 5. feature_X_used        → adoption of key feature
// 6. subscription_started  → monetization
// 7. user_churned          → cancellation
```

### Step 2: Feature Flags Without a Platform (30 minutes)

```javascript
// Option A: JSON config (simplest)
// flags.json — checked into the repo
{
  "onboarding_v2": {
    "enabled": true,
    "rollout": 0.5,        // 50% of users
    "excludePlans": []      // exclude enterprise
  }
}

// Usage in code:
function getUserVariant(featureName) {
  const flag = flags[featureName];
  if (!flag.enabled) return 'control';
  // Deterministic assignment: same user always gets same variant
  const hash = simpleHash(user.id + featureName);
  return (hash % 100) < (flag.rollout * 100) ? 'treatment' : 'control';
}
function simpleHash(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = ((hash << 5) - hash + str.charCodeAt(i)) | 0;
  }
  return Math.abs(hash);
}

// Option B: Database config (allows runtime changes without deploy)
// flags table: id | name | enabled | rollout | created_at | updated_at
// Query on every request (cache in memory, refresh every 60s)
```

### Step 3: A/B Test Analysis in Google Sheets (15 minutes setup)

```
Template columns:
A: Date of experiment start
B: Variant (control / treatment)
C: Total users in variant
D: Converted users (met success criteria)
E: Conversion rate (=D/C)
F: Lift vs control (=(treatment_rate - control_rate) / control_rate)
G: Sample size needed (for 80% power, 5% alpha, MDE=10%)
   Formula: =ROUND((NORM.S.INV(0.975)+NORM.S.INV(0.8))^2 * 
           (C5*(1-C5)+$C$4*(1-$C$4)) / (0.1*$C$4)^2, 0)
H: Is significant? Manual: check if actual n > required n

Quick significance check (no spreadsheet):
1. Calculate z-score: z = (p2-p1) / sqrt(p_pool*(1-p_pool)*(1/n1+1/n2))
2. If |z| > 1.96 → significant at 95% confidence
3. p-value ≈ 2 * (1 - NORM.S.DIST(|z|, TRUE))
```

### Step 4: Minimum Sample Size Table

| Baseline Rate | MDE (Min Detectable Effect) | Sample Size Per Variant |
|--------------|----------------------------|------------------------|
| 5% | 20% relative (1pp absolute) | 7,253 |
| 10% | 20% relative (2pp absolute) | 3,538 |
| 10% | 10% relative (1pp absolute) | 14,739 |
| 20% | 20% relative (4pp absolute) | 1,564 |
| 20% | 10% relative (2pp absolute) | 6,472 |
| 50% | 10% relative (5pp absolute) | 1,570 |

**Rule of thumb:** If you don't have >1,000 users/week reaching the conversion point, you can only detect large effects (>20% relative lift). Don't A/B test. Do qualitative research instead.

---

## When to Run Experiments vs. Just Ship It

| Situation | Action | Why |
|-----------|--------|-----|
| <100 users total | Ship based on intuition + user interviews | No statistical power. Your sample is 5 conversations, not 500 data points. |
| 100-1K users, clear hypothesis from 5+ user complaints | Build the fix. No A/B test needed. | If 5 users independently complain about the same thing, it's real. Fix it and measure before/after. |
| 1K-10K users, 2 viable approaches to the same problem | A/B test. 50/50 split. | You have enough users to detect a 10-20% lift. |
| 1K+ users, shipping a risky change (new pricing, new onboarding, new core UX) | A/B test with kill switch. Start at 5% rollout. | Risk mitigation, not optimization. If it breaks, only 5% of users see it. |
| Any size, fixing a bug | Just fix it. Ship. | Don't A/B test bug fixes. |

---

## MVP Experiment Prioritization (ICE Framework)

Score each experiment 1-10 on:

- **I**mpact: If it works, how much will it move the metric? (revenue, activation, retention)
- **C**onfidence: How sure are you it will work? (data, user research, competitor evidence)
- **E**ase: How easy is it to implement? (hours, not weeks)

```
ICE Score = (Impact + Confidence + Ease) / 3

Example prioritization:
1. Add social proof to pricing page          I:8 C:7 E:9 → 8.0  ← DO FIRST
2. Redesign onboarding flow                   I:9 C:5 E:4 → 6.0
3. Add "invite team" after first project      I:7 C:6 E:8 → 7.0  ← DO SECOND
4. Personalized email onboarding sequence     I:6 C:5 E:5 → 5.3
5. A/B test annual vs monthly default         I:8 C:8 E:3 → 6.3

Rule: Only run experiments with ICE ≥ 7. Below 7 = not worth the distraction at MVP.
```

---

## Cost Comparison: DIY vs. Tools vs. Team

| Stage | Approach | Monthly Cost | Experiments/Month | When Appropriate |
|-------|----------|-------------|-------------------|-----------------|
| **DIY** | JSON flags + PostHog + Google Sheets | $0-20 | 1-2 | 1-3 devs, <1K users |
| **Lightweight tooling** | GrowthBook (self-hosted, free) or Flagsmith (free) | $0-50 | 2-4 | 3-10 devs, 1K-50K users |
| **Growth platform** | LaunchDarkly + Amplitude + Statsig | $300-800/mo | 4-10 | 10+ devs, 50K+ users |
| **Growth team** | 1 growth engineer ($120K/yr) + tools | $11K/mo | 8-20 | 20+ devs, 100K+ users, proven PMF |

**The jump from DIY to tools should happen when:** you've run 5+ manual experiments and the analysis overhead is >2 hours per experiment. At that point, GrowthBook ($0 self-hosted) or Statsig (free tier up to 10K MTUs) pays for itself in engineering time.

---

## Common MVP Growth Mistakes (And Fixes)

| Mistake | Fix |
|---------|-----|
| "Let's A/B test our landing page headline" with 200 visitors/week | You'll need 3-6 months to reach significance. Ship your best guess. Move on. |
| Running 5 experiments simultaneously on the same user population | Interaction effects make results uninterpretable. Run 1-2 at a time, non-overlapping. |
| Peeking at results daily and stopping when p < 0.05 | This inflates false positive rate to ~30%. Pre-register: "I'll check after 2 weeks." |
| Optimizing for clicks that don't lead to revenue | Track through to the metric that matters: revenue, retention, or activation — not vanity metrics. |
| No "holdout" — shipping every winning experiment without measuring cumulative impact | 10 experiments at +2% each ≠ 20% lift (diminishing returns). Run a quarterly holdout check. |
| A/B testing without a hypothesis: "Let's see what happens if we change the button color" | Every experiment needs: "We believe [change] will cause [metric] to improve by [X%] because [user insight]." |

---

## The Only 3 Experiments That Matter at MVP

1. **Activation experiment**: What gets users to the "aha moment" faster? (onboarding flow, setup wizard, template library)
2. **Conversion experiment**: What makes free users pay? (pricing page, trial length, feature gating, social proof)
3. **Retention experiment**: What brings users back? (email/push cadence, weekly digest, collaboration features)

**Don't optimize acquisition until activation and retention work.** Pouring water into a leaky bucket is the #1 startup growth mistake. If activation is <30%, fix onboarding. If D30 retention is <20%, fix the core product. Only then spend on acquisition.
