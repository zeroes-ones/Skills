# Decision Trees for growth-engineer

<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### Experiment Design: A/B vs Multivariate vs Sequential vs Bayesian
```
                     ┌──────────────────────────────┐
                     │ START: Experiment type?        │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Testing >3 variables            │
                    │ simultaneously AND need         │
                    │ interaction effects?            │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────┐    ┌──────────▼──────────┐
                    │ Multivariate│    │ Need early stopping  │
                    │ Test (MVT) │    │ for clear winners?   │
                    │ Requires 4x │    └──┬──────────────┬────┘
                    │ traffic of  │       │YES          │NO
                    │ A/B         │  ┌────▼────┐ ┌──────▼─────────┐
                    └─────────────┘  │Sequential│ │Standard A/B    │
                                     │or Bayesian│ │Frequentist:   │
                                     │A/B — stop │ │Fixed horizon, │
                                     │at interim │ │MDE pre-defined│
                                     │looks      │ │p-value < 0.05 │
                                     └──────────┘ └────────────────┘
```
**When to choose Multivariate:** Testing layout, headline, CTA, and image simultaneously — needs 4× traffic of A/B per variant, interaction effects matter.
**When to choose Sequential/Bayesian:** Early stopping allowed, continuous monitoring, faster decision when effect is large — use Eppo, Statsig, or custom Bayesian framework.
**When to choose Standard A/B:** Simple change, fixed duration, pre-registered analysis — most common, lowest complexity, p-value < 0.05 at planned horizon.

### Activation: Aha Moment Diagnosis
```
                     ┌──────────────────────────────┐
                     │ START: Activation rate low     │
                     │ (< 30% of signups activated)? │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Users dropping before first    │
                    │ key action (e.g., first        │
                    │ transaction, first playlist)?  │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────────┐    ┌──────▼──────────┐
                    │Onboarding     │    │ Users activate   │
                    │Friction:      │    │ but don't return │
                    │Simplify flow, │    │ (Day 7 retention │
                    │progressive    │    │ < 20%)?          │
                    │disclosure,    │    └──┬──────────┬────┘
                    │tooltips       │       │YES      │NO
                    └───────────────┘  ┌────▼────┐ ┌─▼──────────┐
                                       │Habit    │ │Value prop  │
                                       │formation│ │mismatch —  │
                                       │— email, │ │targeting or│
                                       │push,    │ │acquisition │
                                       │in-app   │ │channel     │
                                       │nudges   │ │problem     │
                                       └─────────┘ └────────────┘
```
**When to optimize onboarding:** Metric: time-to-aha moment > target. Simplify initial flow, remove optional steps, progressive disclosure, contextual tooltips.
**When to build habits:** Users activate once but churn — add email/push notifications, streaks, in-app nudges, re-engagement triggers.
**When to fix acquisition:** Users don't even reach aha moment — wrong audience, misleading ads, or value proposition mismatch.

### CRO: Funnel Leak Diagnosis
```
                     ┌──────────────────────────────┐
                     │ START: Which funnel stage      │
                     │ to optimize?                   │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ >60% drop between landing      │
                    │ page visit → signup?           │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────────┐    ┌──────▼──────────┐
                    │Top-of-funnel  │    │ >50% drop between │
                    │CRO:          │    │ signup → aha?     │
                    │Headline,hero,│    └──┬──────────┬────┘
                    │CTA,social    │       │YES       │NO
                    │proof,above-  │  ┌────▼────┐ ┌──▼──────────┐
                    │fold tweaks   │  │Activation│ │Monetization │
                    └──────────────┘  │CRO:     │ │CRO:         │
                                      │onboarding│ │pricing page,│
                                      │flow,     │ │trial length,│
                                      │TTV reduce│ │payment flow │
                                      └──────────┘ └─────────────┘
```
**When to optimize top-of-funnel:** >60% drop LP → signup — A/B test headline, hero image, CTA copy, social proof placement, form fields reduction.
**When to optimize activation:** >50% drop signup → aha — simplify onboarding, add guided tours, reduce TTV, trigger contextual help.
**When to optimize monetization:** Low conversion free→paid — test pricing page layout, trial length, payment options, upgrade prompts.

### Viral Loop Design
```
                     ┌──────────────────────────────┐
                     │ START: What type of viral      │
                     │ mechanism to build?            │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Product inherently improves    │
                    │ with more users (network       │
                    │ effect, collaboration)?        │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────────┐    ┌──────▼──────────┐
                    │Inherent      │    │ Users motivated   │
                    │Virality:     │    │ by reward (credit,│
                    │Invite        │    │ storage, cash)?   │
                    │collaborators │    └──┬──────────┬────┘
                    │vs invite     │       │YES       │NO
                    │strangers     │  ┌────▼────┐ ┌──▼──────────┐
                    └──────────────┘  │Incentivized│ │Content     │
                                      │Referral   │ │Virality:   │
                                      │(Dropbox   │ │Shareable   │
                                      │model —    │ │outputs,    │
                                      │two-sided  │ │public      │
                                      │reward)    │ │results     │
                                      └───────────┘ └────────────┘
```
**When to build inherent virality:** Slack, Figma, Notion — collaboration drives adoption. Build invite-to-workspace, shared links, guest access.
**When to build incentivized referral:** Dropbox, Uber model — two-sided reward (give $10/get $10), clear trigger post-aha moment, fraud detection.
**When to build content virality:** Spotify Wrapped, Strava — create shareable outputs from product usage; public by default with privacy controls.

### Experiment Ramp Decision
```
                     ┌──────────────────────────────┐
                     │ START: How to ramp an          │
                     │ experiment?                    │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ High-risk change (payment,      │
                    │ auth, core experience)?         │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────────┐    ┌──────▼──────────┐
                    │Phased rollout │    │ User-facing UI   │
                    │1% → 5% → 25% │    │ change?          │
                    │→ 50% with    │    └──┬──────────┬────┘
                    │monitoring     │       │YES       │NO
                    │gates per stage│  ┌────▼────┐ ┌──▼──────────┐
                    └───────────────┘  │Instant   │ │Shadow       │
                                       │50/50 A/B │ │deployment:  │
                                       │with kill │ │log both     │
                                       │switch    │ │variants,    │
                                       │ready     │ │compare      │
                                       └──────────┘ │analytically │
                                                    └─────────────┘
```
**When to do phased rollout:** High-risk — payment flow, auth, core UX. Start at 1%, monitor revenue/errors, gate at each stage, auto-rollback on anomaly.
**When to launch 50/50 A/B:** Standard UI/UX change with kill switch — quick statistical read, lower operational overhead than phased.
**When to shadow deploy:** Backend algorithm change, ML model update — log predictions from new model, compare offline, no user impact until validated.
