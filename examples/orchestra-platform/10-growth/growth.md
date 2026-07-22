# Orchestra Platform — Growth Engineering

**Owner:** Growth Team | **Date:** 2026-07-21 | **Cycle:** Q3 2026

## Homepage Hero Experiment

**Hypothesis:** An outcome-focused headline will outperform a feature-focused headline on signup conversion.

| Arm | Headline | n | Rate | Δ |
|---|---|---|---|---|
| Control | "Service Catalog, Templates, Plugins" | 2,400 | 3.2% | — |
| Variant | "Ship services in 15 minutes, not 15 days" | 2,400 | 3.6% | +12% |

**p = 0.01** — statistically significant. Variant shipped to 100%.

## Onboarding Optimization

**Problem:** New teams took 3.2 days on average to deploy their first service (time-to-value).

**Interventions:**
1. **Pre-built demo environment** — skip "set up your first service" wizard; users land in a live sandbox
2. **Guided template selection** — 3 lightweight questions → one recommended template (removed paradox of choice from 40+ templates)
3. **In-app activation checklist** — 5 steps: create service → configure → deploy → invite teammate → view dashboard. Completion rate: **78%**

**Result:** Time-to-value reduced from 3.2 days → **1.8 days** (44% improvement).

## Referral Program

**Mechanism:** "Refer a team — both get 1 month free on any paid plan."

| Metric | Month 1 |
|---|---|
| Referrals sent | 23 |
| Referrals converted | 16 (70%) |
| CAC on referrals | $0 |

## Activation Metric

**Definition:** First template execution = activated user. Orchestra activation rate: **85%**. Industry benchmark for developer tools: 40–60%.

## Viral Coefficient

**k = 0.3** — each user invites approximately 0.3 new users via team invite. This is healthy but not viral; it supplements, but does not replace, content marketing and outbound sales.

## Engineering Principle

> **Growth hacks that damage user trust are net negative.** Every experiment must have a kill criterion defined before launch. If an experiment drives signups but increases churn, it fails — no exceptions.
