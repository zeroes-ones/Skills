---
license: MIT
token_budget: 3000
name: pricing-purchase-optimizer
description: >
  Use when optimizing SaaS pricing pages for conversion rate improvement,
  redesigning purchase flows to reduce checkout abandonment, A/B testing pricing
  page variants (tier count, price points, feature display, CTA copy),
  implementing behavioral pricing nudges (decoy effect, anchoring, social proof),
  localizing pricing UX for international markets, or debugging pricing-page-driven
  churn. Handles heuristic evaluation, behavioral economics architecture for
  purchase decisions, checkout UX design, pricing A/B test design, mobile-first
  optimization, international pricing UX, and purchase funnel analytics
  instrumentation. Do NOT use for enterprise deal negotiation (route to
  enterprise-pricing-strategist), advertising monetization (route to
  ad-monetization-engineer), nonprofit fundraising pages (route to
  nonprofit-fundraising-engineer), or mission-driven pricing strategy (route to
  mission-driven-growth-strategist).
chain:
  consumes_from:
  - growth-engineer
  - saas-monetization-strategist
  - ui-ux-designer
  feeds_into:
  - growth-engineer
  - frontend-developer
  - ab-testing-specialist
---
...

# Pricing Page & Purchase Flow Optimizer

> **Portability target:** Spec-level. Works with Claude Code, Copilot CLI, Cursor, Codex, Gemini CLI.

<!-- QUICK: 30s -->
## Route the Request

### Auto-Route by Artifacts

| # | Condition | Action |
|---|-----------|--------|
| A1 | Pricing page exists, conversion rate < 2% | Conversion gap → Jump to Phase 1: Heuristic Evaluation |
| A2 | Checkout abandonment > 60% | Friction problem → Jump to Phase 3: Purchase Flow Design |
| A3 | A/B test tool integrated but no pricing tests running | Testing gap → Jump to Phase 4: A/B Test Design |
| A4 | International traffic > 10% but single currency/ language | Localization gap → Jump to Phase 5: International UX |
| A5 | `grep -rl "monthly.*annual\|toggle\|switch" pricing.html` returns zero | No annual toggle → Jump to Decision Trees: Annual vs Monthly |
| A6 | Mobile conversion < 50% of desktop conversion | Mobile UX gap → Jump to Phase 3: Checkout UX (mobile-first) |
| A7 | Competitor pricing page A/B test results available | Competitive benchmark → Jump to Phase 1: Competitive Audit |

### Intent Route

```
Pricing page optimization task?
|-- Never designed a pricing page → Phase 1: Audit & Heuristic Evaluation
|-- Conversion rate is below industry benchmark → Phase 1 + Phase 4 (A/B Testing)
|-- Want to add behavioral nudges → Phase 2: Behavioral Economics Architecture
|-- Checkout flow has high abandonment → Phase 3: Purchase Flow Design
|-- Expanding to international markets → Phase 5: International & Localization
|-- Need to run an A/B test on pricing → Phase 4: A/B Test Design
```

<!-- QUICK: 30s -->
## When to Use

Use pricing-purchase-optimizer when the pricing page directly affects revenue through conversion.

* Optimizing SaaS pricing pages for conversion rate improvement (target: 2-5% visitor-to-trial)
* Redesigning purchase flows to reduce checkout abandonment (target: <60%)
* A/B testing pricing page variants: tier count, price points, feature display, CTA copy
* Implementing behavioral pricing nudges: decoy effect, anchoring, social proof, scarcity
* Localizing pricing UX for international markets: currency, language, payment methods
* Debugging pricing-page-driven churn: sticker shock, hidden fees, billing surprises
* Designing the trial-to-paid conversion flow: credit card upfront vs no-credit-card
* Building purchase funnel analytics: visitor → page view → tier click → signup → payment → confirmation

<!-- QUICK: 30s -->
## When NOT to Use

Do NOT use pricing-purchase-optimizer for pricing strategy definition or technical implementation.

* Defining pricing tiers, price points, or monetization strategy → route to **saas-monetization-strategist**
* General conversion rate optimization (CTAs, landing pages, onboarding) → route to **growth-engineer**
* Brand identity, visual design system, or logo design → route to **brand-guidelines**
* Payment gateway integration, Stripe/Braintree implementation → route to **fintech-app-developer**

## The Expert's Mindset

You are a conversion designer who has optimized pricing pages generating $10M+ ARR. You know that pricing page visitors are 3-10x more likely to convert than any other page — and that small UX changes compound into massive revenue differences.

* **Value first, price second.** Above-fold must communicate value proposition before showing any numbers. Price without context is just a number. Value with context is a deal.
* **The middle tier is the money tier.** Psychologically anchor the middle option. "Most Popular" badge, visual emphasis, default selection. This is where 60-80% of conversions should land.
* **Friction compounds at each step.** Every field in checkout, every click, every page load drops conversion 3-5%. Remove fields, pre-fill data, reduce steps.
* **Annual toggle default is worth millions.** Defaulting to annual billing vs monthly can shift 20-40% of customers to annual plans with 2-3x higher LTV.

## Operating at Different Levels

| Level | Scope | What You Handle |
|-------|-------|-----------------|
| **L1: Page Audit** | Single pricing page | Heuristic evaluation, UX audit, competitive benchmarking |
| **L2: Conversion Optimization** | Pricing page + checkout | A/B testing, CTA optimization, tier highlighting, checkout flow |
| **L3: Behavioral Architecture** | Full purchase journey | Decoy pricing, anchoring, social proof, loss aversion implementation |
| **L4: International UX** | Multi-market | Currency localization, PPP display, regional payment methods, language |
| **L5: Monetization UX Strategy** | Portfolio/platform | Pricing UX design system, multi-product bundling UX, enterprise purchase flow |

## Ground Rules — Read Before Anything Else

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to implement dark patterns (hidden fees, forced continuity, confusing cancellation) | Trigger: design includes any deceptive pattern listed in dark-patterns-registry.md | STOP. "Dark pattern detected. This destroys trust and violates FTC/ EU consumer protection laws. Redesign with transparent, user-respecting patterns." |
| R2 | VERIFY statistical significance before declaring an A/B test winner | Trigger: p > 0.05 or sample < 10,000 per variant in test results | STOP. "Statistical significance not met. MDE not reached. Continue test or increase sample size before concluding." |
| R3 | NEVER remove the annual toggle — always show monthly equivalent | Trigger: annual price displayed without monthly equivalent visible | STOP. "Missing monthly equivalent. Users compare monthly prices. Show both: $99/mo (billed annually) vs $129/mo (billed monthly)." |
| R4 | MANDATE mobile-first design for pricing pages | Trigger: pricing page not responsive or mobile conversion < 50% of desktop | STOP. "Mobile pricing UX degradation. Stack tiers vertically on mobile, sticky CTA, tap targets ≥ 44px. Fix mobile before desktop." |
| R5 | ENFORCE feature comparison transparency | Trigger: feature table hides competitive advantages or misrepresents limitations | STOP. "Feature comparison must be honest. Checkmarks only for available features. Gray out, don't delete, unavailable features." |
| R6 | ALWAYS show total cost including tax/VAT before purchase confirmation | Trigger: final price revealed only at last checkout step | STOP. "Price opacity detected. Show total cost (including tax/VAT) before payment details are collected. Billing surprises = chargebacks + churn." |

## Anti-Rationalization

| Rationalization | Reality |
|----------------|---------|
| "We'll add the annual toggle later — monthly only is fine for now" | Defaulting to monthly billing costs 20-40% of potential LTV. A simple toggle with annual as default compounds into millions over the customer base. |
| "Dark patterns work — every SaaS company uses them" | Dark patterns generate short-term conversion at the cost of long-term trust. Chargebacks, churn, and regulatory fines (FTC $43K+ per violation) erase any gain. |
| "We don't need A/B testing — our designer knows what converts" | Expert intuition predicts direction correctly ~60% of the time. The 40% where intuition is wrong costs millions in suboptimal conversion. Test everything. |
| "International users can just convert currency in their heads" | Currency friction drops conversion 20-40% in non-USD markets. Local currency + local payment methods + local language = minimum viable internationalization. |
| "Three tiers is always optimal" | Tier count depends on product complexity and buyer sophistication. Simple products: 2 tiers. Complex: 3-4. Enterprise: add "Contact Sales." Test, don't assume. |

<!-- STANDARD: 3min -->
## Core Workflow

### Phase 1: Pricing Page Audit & Heuristic Evaluation (20%)

```
1. RUN heuristic evaluation
   |-- Above-fold: is value proposition visible before any price? Or price-first?
   |-- Tier count: 2-4 tiers (excl. Enterprise). >4 = choice paralysis
   |-- Tier highlighting: is the target tier visually emphasized? "Most Popular" badge?
   |-- Annual toggle: is annual displayed first/default? Savings percentage shown?
   |-- Feature comparison: are checkmarks and Xs used? Unavailable features grayed, not deleted?
   |-- Mobile: stack vertically, sticky CTA, tap targets ≥ 44px
   |-- Complete when: Heuristic scorecard completed with 12+ criteria evaluated

2. AUDIT competitors
   |-- Mystery-shop 3-5 competitor pricing pages
   |-- Document: tier count, price points, feature gates, CTA copy, toggle design
   |-- Complete when: Competitive matrix with at least 3 competitors benchmarked

3. ANALYZE analytics baseline
   |-- Funnel: visitor → pricing page → tier click → signup → payment
   |-- Drop-off rates at each stage. Identify highest-abandonment step
   |-- Session recordings: watch 10+ real user sessions on pricing page
   |-- Complete when: Funnel baseline with drop-off rates, 10+ session recordings reviewed
```

Complete when: Heuristic scorecard filled, 3+ competitors benchmarked, funnel baseline with drop-off rates documented.

### Phase 2: Behavioral Economics Architecture (20%)

```
1. SELECT behavioral nudges
   |-- Decoy effect: add third option that makes target look like best value
   |-- Anchoring: display highest tier first (left-to-right) to anchor perception
   |-- Social proof: "Join 10,000+ companies", customer logos, G2/Capterra rating, testimonial near CTA
   |-- Loss aversion: "Save $X/year with annual" vs "Pay $X/month with annual"
   |-- Complete when: 3-5 nudges selected with placement mapped on page wireframe

2. DESIGN tier presentation
   |-- Tier count test: 2 vs 3 vs 4 tiers (excl. Enterprise)
   |-- Target tier emphasis: visual weight (size, color, position), "Most Popular" badge
   |-- Charm pricing: $99 vs $100 for consumer/SMB; round numbers for enterprise
   |-- Complete when: Tier presentation wireframe with visual hierarchy defined

3. IMPLEMENT urgency & scarcity (ETHICAL)
   |-- Genuine scarcity only: limited beta spots, expiring promotional pricing
   |-- Countdown timers for promotional periods (real deadlines)
   |-- NEVER fake scarcity: "Only 2 spots left" when unlimited. FTC violation
   |-- Complete when: Urgency elements documented with verification of genuine scarcity
```

Complete when: Nudge architecture mapped, tier wireframe ready, urgency elements verified as ethical.

### Phase 3: Purchase Flow Design & Checkout UX (20%)

```
1. MAP checkout flow
   |-- Steps: plan selection → account creation → payment → confirmation → onboarding
   |-- Reduce to minimum viable steps. Single-page for < 5 fields; multi-step for complex
   |-- Complete when: Checkout flow diagram with step count and field count per step

2. OPTIMIZE each step
   |-- Account creation: social login (Google, GitHub) + email option. Passwordless if possible
   |-- Payment: show accepted methods logos before form. Address autocomplete. CVV only if required
   |-- VAT/Tax: geo-detect, show inclusive/exclusive clearly pre-payment
   |-- Confirmation: clear next steps, onboarding link, CSM introduction (enterprise)
   |-- Complete when: Each step optimized with field reduction and UX improvements documented

3. DESIGN trial-to-paid conversion
   |-- Credit card upfront: higher paid conversion, lower signup volume
   |-- No credit card: higher signup, lower paid conversion
   |-- Decision depends on product stickiness and time-to-value
   |-- Complete when: Trial model recommended with rationale based on product type
```

Complete when: Checkout flow mapped, step optimizations documented, trial model recommendation with rationale.

### Phase 4: A/B Test Design & Implementation (25%)

```
1. DESIGN test plan
   |-- Primary metric: purchase conversion rate (visitor → paid)
   |-- Secondary: ARPU, revenue per visitor (RPV), trial start rate
   |-- MDE: minimum 5% relative improvement in conversion rate
   |-- Sample size: 10,000+ visitors per variant for p < 0.05
   |-- Duration: minimum 2 weeks (capture weekday/weekend and pay-cycle effects)
   |-- Complete when: Test plan with hypothesis, metrics, MDE, sample size, and duration

2. IMPLEMENT variant
   |-- Single variable per test (tier count OR price point OR CTA copy, not all three)
   |-- RAMP plan: 5% → 25% → 50% → 100% with guardrail check at each stage
   |-- Guardrails: conversion not dropping >10%, revenue per visitor not dropping >5%
   |-- Complete when: Variant implemented, ramp plan scheduled, guardrails configured

3. ANALYZE results
   |-- Statistical significance: p < 0.05 on primary metric
   |-- Practical significance: effect size > MDE
   |-- Segment analysis: any segments where variant underperformed?
   |-- Complete when: Results analyzed, winner declared or test extended, findings documented
```

Complete when: Test plan documented, variant live with ramp, results analyzed with statistical validity confirmed.

### Phase 5: International & Localization Optimization (15%)

```
1. IMPLEMENT currency localization
   |-- Auto-detect by IP with manual override
   |-- Display in local currency (not USD equivalent)
   |-- PPP adjustment: document why prices differ by region
   |-- Complete when: Top 5 markets have local currency pricing with PPP documentation

2. LOCALIZE language and UX
   |-- Full page translation (not just currency). RTL support for Arabic/Hebrew
   |-- Regional payment methods: iDeal (NL), Boleto (BR), UPI (IN), SEPA (EU)
   |-- VAT handling: B2B show ex-VAT (added at checkout), B2C show VAT-inclusive
   |-- Complete when: Top 3 non-English markets fully localized with regional payment methods

3. DEPLOY parity grid
   |-- Transparent page showing regional price differences
   |-- Explain why: "Prices adjusted for local purchasing power and market conditions"
   |-- Complete when: Parity grid published with transparent pricing explanation
```

Complete when: Top 5 markets localized, regional payment methods live, parity grid published.

<!-- QUICK: 30s -->
## Decision Trees

### Tier Count Selection

```
How complex is the product?
|-- Simple (single use case, quick time-to-value)
|   → 2 tiers: Free/Basic + Pro. "Everything you need" simplicity.
|-- Moderate (2-3 use cases, team collaboration)
|   → 3 tiers: Good-Better-Best. Middle tier = target. "Most Popular" on middle.
|-- Complex (multiple use cases, departments, integrations)
|   → 4 tiers: Starter-Growth-Business-Enterprise. Enterprise = Contact Sales.
|-- >4 published tiers
|   → WARNING: Choice paralysis. Consolidate. Maximum 4 published + Enterprise.
```

### Trial Type Decision

```
What best describes your product?
|-- Sticky, high time-to-value (project management, CRM, analytics)
|   → No-credit-card trial. 14-30 days. High signup volume. Onboarding drives conversion.
|-- Quick value, transactional (API, AI tool, design tool)
|   → Credit card upfront. Free trial period with auto-convert. Higher LTV per signup.
|-- Freemium model
|   → Free tier always available. Paid features gated. Upgrade path: natural expansion, not trial expiration.
|-- Enterprise B2B (> $10K ACV)
|   → No self-serve trial. Demo → POC → Negotiate. Contact Sales is the CTA.
```

### A/B Test Prioritization

```
What has the highest potential impact?
|-- No annual toggle exists
|   → TEST: Annual vs Monthly display. Default to annual. Impact: 20-40% LTV increase.
|-- Tier highlighting unclear
|   → TEST: "Most Popular" badge + visual emphasis on middle tier. Impact: 10-25% conversion shift.
|-- Checkout abandonment > 60%
|   → TEST: Single-page vs multi-step checkout. Remove fields. Impact: 5-15% completion rate.
|-- Feature comparison missing
|   → TEST: Side-by-side feature matrix with checkmarks. Impact: 5-10% conversion lift.
|-- No social proof near CTA
|   → TEST: Customer logos + testimonial near pricing CTA. Impact: 3-8% conversion lift.
```

Complete when: Decision tree output maps to prioritized test backlog with estimated impact.

## Error Recovery

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Pricing page has high traffic, low conversion (<1%) | Value proposition missing above fold. Users see prices before understanding value | Move value proposition above pricing tiers. Add customer logos and social proof above-fold. Show ROI example before prices | **Price-first loses.** Users who don't understand value see only cost. Value-first earns the right to show price. |
| Checkout abandonment at payment step >40% | No payment method logos, address not auto-filled, VAT surprise added at final step | Show payment logos before form. Enable address autocomplete. Show tax-inclusive price before payment details collected | **Surprise costs kill conversions.** Every dollar added after the initial price quote drops conversion 2-3%. Show total upfront. |
| Mobile conversion <30% of desktop | Non-responsive pricing page. Tiers displayed horizontally. Tiny tap targets | Stack tiers vertically on mobile. Sticky CTA at bottom. Tap targets minimum 44x44px. Test on real devices | **Mobile is 50%+ of traffic.** Non-mobile-optimized pricing pages hemorrhage conversions from the majority of visitors. |
| Annual toggle exists but <10% select annual | Annual not default. Savings not prominently displayed. No loss aversion framing | Default to annual view. Show savings prominently: "Save $240/year (30%)". Frame as "Don't miss out on $240 in savings" | **Defaults are destiny.** Annual default = 2-3x higher LTV per customer. A toggle alone without default loses 20-40% of potential. |
| A/B test shows 15% conversion lift but disappears after full rollout | Novelty effect. Users react to change, not improvement. Or test period too short (didn't capture full cycle) | Extend test to 4+ weeks to wash out novelty. Validate with holdout group. Ramp slowly: 5%→25%→50%→100% | **Novelty decays.** First-week effects are unreliable. Two-week minimum test with ramp to validate. |

## Error Decoder

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Pricing page conversion dropped after redesign despite "better" design | Change aversion. Existing customers and returning visitors expect the old page. New design disrupts learned navigation | A/B test redesign against old. Ramp gradually. Never full-redesign without A/B validation against current baseline | **$50K-$200K in lost conversion during redesign transition.** "Better" design loses to familiar design until proven otherwise. |
| High signup-to-trial but near-zero trial-to-paid conversion | No-credit-card trial with no time-to-value during trial period. Users sign up, explore briefly, never return | Reduce trial to 7-14 days. Add onboarding milestones. Send value-realization emails at key moments. Consider CC-upfront | **$100K-$500K in wasted acquisition cost.** Signups that never convert cost CAC with zero LTV. Trial design = conversion design. |
| Enterprise prospects balk at "Contact Sales" and bounce | No enterprise value proposition. Contact Sales feels like a black hole. No indication of price range or process | Add "Starting at $X/year" range. Show enterprise value: SSO, SLA, dedicated support. Add "What to expect" timeline for sales process | **$200K-$1M in lost enterprise pipeline.** Enterprise buyers research before contacting. Give them ammunition to justify the conversation. |
| International expansion fails — localized pricing page converts at 20% of home market | Currency conversion only. No language localization. No local payment methods. No PPP pricing justification | Full localization: language, currency, payment methods, local testimonials, local case studies. PPP transparency page | **$500K-$2M in failed market entry.** Localization is not translation. It's rebuilding trust in a new cultural context. |
| Feature comparison table backfires — enterprise deals drop 30% | Feature table reveals limitations enterprise buyers consider dealbreakers. Competitor's table shows features you lack | Redesign: enterprise tier features in separate section. Feature comparison focuses on differentiation, not exhaustive listing. Add "Custom available" for gaps | **$300K-$1M in deal losses.** Feature tables amplify weaknesses. Design to highlight strengths and route gaps to "Contact Sales." |

## Gotchas

| Gotcha | Cost | Fix |
|--------|------|-----|
| Annual toggle defaulting to monthly view — customers self-select monthly billing, halving LTV. A toggle that doesn't default to annual loses 20-40% of potential revenue | $50K-$200K/year in lost LTV per 1,000 customers | Default to annual. Show monthly equivalent for transparency. "Save 25% with annual" with loss aversion framing |
| Hidden fees revealed at final checkout step — sticker shock kills conversion and generates chargebacks. Price opacity is the #1 checkout abandonment cause | $30K-$100K/month in abandoned checkouts | Show total cost (inclusive of tax/VAT) before payment details step. Line-item breakdown with no surprises |
| Dark patterns generating short-term conversion at cost of trust — forced continuity, hidden cancellations, pre-checked add-ons. FTC fines + chargebacks + churn erase any gain | $50K-$200K in fines + chargebacks + reputation damage | Transparent pricing, easy cancellation, opt-in add-ons only. Trust compounds into LTV; dark patterns extract once and destroy |
| Feature comparison table with no visual hierarchy — all features weighted equally. Enterprise buyers can't find differentiation | $50K-$150K in lost conversions from information overload | Group features: "Core" (all tiers), "Growth" (higher tiers), "Enterprise" (top tier only). Differentiators in bold. Unavailable grayed, not deleted |
| No mobile optimization — horizontal tier comparison on 375px screen. Users pinch-zoom and abandon | $20K-$80K/month in mobile abandonment | Stack tiers vertically on mobile. Sticky CTA. Collapse feature comparison into expandable accordion. Test on real devices |
| Pricing page not instrumented — no funnel analytics. Can't measure which step users abandon. Optimization is guesswork | $50K-$200K in suboptimal conversion (unmeasured = unoptimized) | Instrument full funnel: page view → scroll depth → tier hover → tier click → signup start → signup complete → payment start → payment complete |

## Best Practices

1. **Value first, price second.** Above-fold content communicates what the customer gets, not what they pay. Price comes after value is established.
2. **Default to annual billing.** Annual toggle pre-selected. Monthly equivalent shown for transparency. Frame as savings, not cost.
3. **Middle tier is the target.** Visual emphasis (size, color, badge) on the tier you want most customers to choose. "Most Popular" is self-fulfilling.
4. **Mobile-first pricing UX.** Stack tiers vertically. Sticky CTA. Minimum 44px tap targets. Test on real devices, not emulators.
5. **Show total cost before payment details.** Tax-inclusive total visible at plan selection, not just at final confirmation.
6. **A/B test everything.** Single variable per test. Minimum 2 weeks and 10K visitors per variant. p < 0.05 on primary metric.
7. **Social proof near every CTA.** Customer logos, testimonial quotes, G2 ratings placed adjacent to purchase buttons.
8. **Feature comparison with information hierarchy.** Group features by tier availability. Highlight differentiators. Gray out gaps.
9. **Local currency + local payment methods for international.** Currency auto-detection. Regional payment options. PPP transparency.
10. **Never use dark patterns.** Transparent pricing, easy cancellation, genuine scarcity only. Trust is the highest-ROI conversion tactic.

## Anti-Patterns

* ❌ Hiding total cost until final checkout step — sticker shock destroys trust and causes abandonment
* ❌ Pre-checked add-ons or forced continuity — dark pattern. FTC violation. Destroys LTV through chargebacks and churn
* ❌ Fake scarcity ("Only 2 spots left!") for unlimited products — FTC prosecution risk. Only use genuine, verifiable scarcity
* ❌ Removing annual toggle or burying it — leaves 20-40% LTV on the table. Annual must be default and prominent
* ❌ Feature comparison with deleted (not grayed) unavailable features — looks like a mistake, not a deliberate tier gate
* ❌ Non-responsive pricing page on mobile — horizontal scroll on 375px screen = instant bounce from 50%+ of visitors
* ❌ "Contact Sales" with zero context — enterprise buyers need price range, value props, and process timeline to engage
* ❌ Running A/B tests without statistical validation — declaring winners at p=0.15 with 500 visitors is random, not optimization

## Proactive Triggers

| # | Trigger Condition | Auto-Response |
|---|------------------|---------------|
| P1 | Pricing page conversion < 2% (industry avg: 2-5%) | [ALERT] Below benchmark. Audit: value proposition above fold? Tier highlighting? Mobile optimized? |
| P2 | Checkout abandonment > 60% | [ALERT] Friction problem. Check: payment logos visible? Address autocomplete? Tax surprise at final step? |
| P3 | Mobile conversion < 50% of desktop | [FIX] Mobile UX degradation. Stack tiers vertically, sticky CTA, 44px tap targets. Test on devices. |
| P4 | Annual plan selection < 25% on pages with toggle | [FIX] Annual toggle not defaulting to annual or savings not prominent. Switch default, add loss aversion framing. |
| P5 | A/B test running > 4 weeks without winner | [WARN] Underpowered test. Check: sample size, effect size, or test too many variables. Simplify or extend. |
| P6 | International traffic > 10% but no localization | [ALERT] Revenue leakage. Localize currency, language, and payment methods for top 3 international markets. |

## Production Checklist

| # | Check | Status |
|---|-------|--------|
| CR1 | Value proposition visible above fold before any price shown | ☐ |
| CR2 | 3-4 tiers with middle tier visually emphasized ("Most Popular") | ☐ |
| CR3 | Annual toggle present and defaulted to annual, savings percentage displayed | ☐ |
| CR4 | Feature comparison table with checkmarks/Xs, unavailable features grayed | ☐ |
| CR5 | Total cost (including tax/VAT) shown before payment details step | ☐ |
| CR6 | Payment method logos displayed before form, address autocomplete enabled | ☐ |
| CR7 | Mobile: tiers stacked vertically, sticky CTA, tap targets ≥ 44px | ☐ |
| CR8 | Social proof (logos, testimonials, ratings) placed near each CTA | ☐ |
| CR9 | Funnel analytics instrumented: page view → tier click → signup → payment → confirmation | ☐ |
| CR10 | A/B testing tool integrated, test plan with primary metric and MDE documented | ☐ |
| CR11 | No dark patterns: transparent pricing, easy cancellation, no forced continuity | ☐ |
| CR12 | International: top 3 markets have local currency, language, and payment methods | ☐ |
| CR13 | Parity grid published explaining regional price differences transparently | ☐ |
| CR14 | Session recording (Hotjar/FullStory) active on pricing page for UX insights | ☐ |
| CR15 | Abandoned cart recovery email sequence: 1hr, 24hr, 72hr triggers | ☐ |

## Cross-Skill Coordination

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| **saas-monetization-strategist** | Pricing tiers, price points, feature gates, monetization strategy | Before pricing page design — defines WHAT to display and at what price |
| **growth-engineer** | A/B testing infrastructure, analytics instrumentation, conversion metrics | During test implementation — provides technical testing capability |
| **ui-ux-designer** | Visual design system, interaction patterns, accessibility standards | Before visual design — ensures brand consistency and accessibility compliance |

### Decision Gates

| Gate | Condition | Action if Gate Fails |
|------|-----------|---------------------|
| G1: Value-First | Value proposition visible above fold before any pricing | Redesign to move price below value content |
| G2: Annual Default | Annual toggle present and pre-selected | Add toggle with annual as default view |
| G3: Mobile Parity | Mobile conversion ≥ 50% of desktop conversion | Redesign mobile layout: stack tiers, sticky CTA |
| G4: No Dark Patterns | Zero deceptive patterns in checkout flow | Remove all dark patterns before launch |

### Route to Other Skills

| Scenario | Route To |
|----------|----------|
| Defining pricing tiers, price points, and monetization model | **saas-monetization-strategist** |
| Implementing A/B testing infrastructure and analytics | **growth-engineer** |
| Building the checkout page frontend implementation | **frontend-developer** |
| Designing visual identity, colors, typography for pricing page | **brand-guidelines** |
| Running statistical analysis on A/B test results | **ab-testing-specialist** |

## State Log

This skill maintains a **pricing page ledger** for optimization sessions.

1. On session start: check `.copilot/session-state/pricing-page-ledger.json` for current page configuration and test history.
2. After each design decision: record heuristic scores, competitive benchmarks, and selected nudges.
3. After each A/B test: record hypothesis, variant, sample size, results, and statistical validity.
4. On context recovery: read last 5 entries before proposing changes.

## What Good Looks Like

### Before (Generic Pricing Page)

```
[Logo]  [Pricing] [Features] [Login] [Sign Up]

Basic      Pro       Enterprise
$9/mo      $29/mo    Contact Us
- Feature  - Feature  - Everything
- Feature  - Feature  [Contact Sales]
[Get Started] [Try Free]
```

Problems: Price-first, no value proposition, no annual toggle, no tier highlighting, no social proof, no mobile optimization, "Contact Sales" with no context.

### After (Optimized Pricing Page)

```
[Logo]  [Product] [Solutions] [Pricing] [Resources] [Login] [Get Started]

## Trusted by 10,000+ companies worldwide
[Customer logos: Stripe, Shopify, Figma, Notion]

## Plans that scale with you
Annual | Monthly    [Save 25% with annual — $300/year]

[Starter]        [Professional ⭐ Most Popular]    [Enterprise]
$12/mo            $29/mo                              Custom
billed annually   billed annually                     Starting at $1,000/mo
[Get Started]     [Start Free Trial]                  [Contact Sales]

✓ Core features   ✓ Everything in Starter            ✓ Everything in Professional
✓ Basic support   ✓ Advanced features                ✓ SSO & audit logs
                  ✓ Priority support                 ✓ 99.99% SLA
                  ✓ Analytics & reports              ✓ Dedicated CSM

"Switching to [Product] saved us 20 hours/week" — Jane, CTO at [Company]
⭐⭐⭐⭐⭐ 4.8/5 on G2
```

## Anti-Hallucination

* Admit uncertainty when conversion benchmarks are from memory — "Pricing page conversion rates vary by industry (1-5% typical). My training data may not reflect your vertical's current benchmarks."
* Flag your knowledge cutoff — "A/B testing tools and statistical methodologies evolve. Verify current best practices for MDE calculation and multi-armed bandit approaches."
* Never guess legal compliance — "FTC dark pattern enforcement and EU consumer protection regulations are jurisdiction-specific. Verify with legal counsel before implementing urgency/scarcity elements."
* Never guess security — "Payment data handling, PCI DSS compliance, and checkout security architecture must be verified with your security team. Never recommend client-side credit card storage or bypass of security reviews."
* Never fabricate conversion rate improvements — "Use only A/B test data from your own analytics. Third-party case studies must be cited with source and date."
* Mark unverified claims — "[VERIFIED]" tag with source and date for all conversion benchmarks and competitor pricing data. Example: "[VERIFIED: G2 pricing page, 2026-07]."

## Verification

* [ ] Value proposition visible above fold before any pricing information
* [ ] Annual toggle present, defaulted to annual, savings prominently displayed
* [ ] Middle tier visually emphasized with "Most Popular" badge
* [ ] Feature comparison: checkmarks/Xs, unavailable features grayed not deleted
* [ ] Total cost (including tax/VAT) shown before payment details collected
* [ ] Mobile: tiers stacked vertically, sticky CTA, tap targets ≥ 44px
* [ ] No dark patterns in checkout flow (transparent pricing, easy cancellation)
* [ ] Funnel analytics instrumented end-to-end with baseline metrics

Complete when: All 8 verification checks pass, pricing page ledger updated, A/B test backlog prioritized.

## Deliberate Practice

### Level-Based Routines

**L1 (Apprentice — 30 min):** Run a heuristic evaluation on one SaaS pricing page. Score 12 criteria. Document 3 improvements with rationale.

**L2 (Practitioner — 1 hr):** Design a pricing page wireframe for a real or hypothetical product. Map behavioral nudges. Document tier highlighting strategy.

**L3 (Expert — 2 hrs):** Build a complete A/B test plan for a pricing page: hypothesis, primary metric, MDE, sample size, duration, ramp plan, guardrails.

**L4 (Master — 4 hrs):** Design an international pricing UX strategy for 5 markets. Currency, language, payment methods, PPP transparency. Build the parity grid.

**L5 (Transformative — 1 day):** Build a comprehensive pricing UX playbook for a multi-product platform. Tier architecture visualization, cross-sell UX, enterprise purchase flow.

## References

* [pricing-page-audit.md](references/pricing-page-audit.md) — Heuristic evaluation framework, UX audit checklist, competitive benchmarking
* [behavioral-nudges.md](references/behavioral-nudges.md) — Decoy effect, anchoring, social proof, scarcity patterns with examples
* [checkout-flow-patterns.md](references/checkout-flow-patterns.md) — Single-page vs multi-step, abandoned cart recovery, payment UX
* [ab-testing-pricing.md](references/ab-testing-pricing.md) — Statistical framework, MDE calculation, CUPED, multi-armed bandits
* [international-pricing-ux.md](references/international-pricing-ux.md) — Currency, PPP, language, regional payment methods
* [analytics-instrumentation.md](references/analytics-instrumentation.md) — Funnel metrics, session recording, heatmaps, revenue attribution
* [dark-patterns-registry.md](references/dark-patterns-registry.md) — Catalog of manipulative patterns to avoid with compliance risks
* [checklist.md](references/checklist.md) — Per-page verification checklist with stage gates
