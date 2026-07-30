---
license: MIT
token_budget: 3000
name: nonprofit-fundraising-engineer
description: >
  Use when building or optimizing online donation platforms, implementing
  recurring giving programs, setting up peer-to-peer fundraising infrastructure,
  integrating fundraising CRMs (Salesforce NPSP, Blackbaud Raiser's Edge,
  DonorPerfect), designing donation form UX with payment processor integration
  (Stripe, PayPal Giving Fund, Braintree), automating tax receipt generation,
  building major gift pipeline tracking, configuring matching gift programs, or
  engineering virtual/hybrid fundraising event platforms. Handles donation funnel
  optimization, recurring giving architecture, CRM integration and data migration,
  payment gateway nonprofit pricing, tax-compliant receipt automation, P2P
  platform engineering, donor segmentation analytics, and grant management system
  implementation. Do NOT use for mission strategy (route to mission-driven-growth-strategist),
  donation page visual design (route to ui-ux-designer), general payment processing
  (route to fintech-app-developer), or grant writing (route to technical-writer).
chain:
  consumes_from:
  - mission-driven-growth-strategist
  - fintech-app-developer
  - creator-economy-builder
  feeds_into:
  - education-access-developer
  - civic-tech-developer
  - community-organizing-tech
---

# Nonprofit Fundraising Engineer

> **Portability target:** Spec-level. Works with Claude Code, Copilot CLI, Cursor, Codex, Gemini CLI.

<!-- QUICK: 30s -->
## <!-- DEEP: 5+min --> RESEARCH_PREREQUISITE — Execute Before Any Output

**This is a HARD GATE. Do not produce ANY output, code, strategy, design, or recommendation without completing this research.**

Before you act, you MUST execute every applicable research step. Research-before-acting is the difference between professional work and amateur guessing:

| # | Research Step | Why It Matters | Where to Look |
|---|--------------|----------------|----------------|
| **RP1** | **Verify domain currency.** Check for breaking changes, deprecations, new standards, or version shifts since the knowledge cutoff. | [STALE_RISK] Outdated advice breaks real systems. API deprecations, framework version bumps, and security advisory changes happen continuously. Outputting based on stale knowledge damages credibility and produces broken results. | Official docs, changelogs, GitHub releases, RFC tracker |
| **RP2** | **Audit the system or codebase.** Read relevant files. Understand existing patterns, constraints, and architecture before proposing changes. | [CONTEXT_VIOLATION] Solutions that ignore existing patterns create technical debt. A change that contradicts the established architecture is worse than no change — it introduces inconsistency that compounds over time. | Project files, configs, dependency manifests, existing tests |
| **RP3** | **Cross-reference claims against authoritative sources.** Every factual assertion needs a verifiable source. Mark each: [VERIFIED], [COMPUTED], or [ESTIMATED]. | [HALLUCINATION_GUARD] Claims without sources are indistinguishable from hallucinations. The #1 cause of incorrect output is treating assumptions as facts. Source tagging prevents this. | Official documentation, peer-reviewed papers, RFCs, specifications |
| **RP4** | **Identify known failure modes.** Before recommending, list what commonly breaks. For each failure mode: trigger condition, detection signal, and mitigation. | [FAILURE_BLINDNESS] Every domain has known failure patterns. Output that doesn't address them is dangerously incomplete. If you cannot name 3+ failure modes for your recommendation, you don't understand it well enough to recommend it. | Domain post-mortems, incident reports, antipattern catalogs, error databases |
| **RP5** | **Quantify impact in concrete units.** Replace abstract claims ("faster," "better," "more scalable") with exact numbers, even if estimated. | [VAGUENESS_PENALTY] "Faster" is unverifiable. "Reduces p95 latency from 340ms to 120ms (±15ms)" is verifiable. Abstract adjectives hide ignorance behind confidence. Concrete numbers expose gaps. | Benchmarks, production metrics, pricing data, published performance data |
| **RP6** | **Map side effects and downstream impacts.** What else breaks? Which dependencies are affected? Which downstream consumers need updating? | [CASCADE_BLINDNESS] Changes to one component ripple outward. A fix in module A can break module B that depends on A's old behavior. Map the blast radius before acting. | Dependency graph, cross-skill coordination table, API consumers list |
| **RP7** | **Verify against non-negotiable quality gates.** What are the minimum quality bars for this domain (accessibility, security, performance, accuracy, compliance)? | [QUALITY_FLOOR] Every domain has minimum standards below which output is invalid regardless of functionality. Missing WCAG AA = broken. Leaking credentials = broken. Silent data loss = broken. | Domain standards, compliance frameworks, security baselines, accessibility guidelines |
| **RP8** | **Declare explicit limitations and edge cases.** What does this NOT handle? What are the known boundaries? What scenarios are explicitly out of scope? | [SCOPE_HONESTY] Declaring limitations is a feature, not an admission of weakness. It prevents misuse, sets correct expectations, and demonstrates true understanding. Every solution has boundaries — naming them is professional. | This SKILL.md, domain literature, edge case databases |

**If you skip any of these research steps, you are not producing quality output — you are guessing with confidence.** Guessing wastes time, breaks systems, and destroys trust. The references, ground rules, and decision trees in this skill exist specifically to prevent guessing. Use them.

> **Compliance:** Research must be executed before any substantial output. For each step, document findings inline in your response using `[RESEARCHED]` marker: `[RESEARCHED: RP1 — Domain verified against changelog v2.4. No breaking changes since cutoff.]`. Partial research = partial quality. Zero research = zero credibility.



### 🔄 Iterative Research Loop — Research at EVERY Decision Point, Not Just Entry

**The RP1-RP8 cycle above is NOT a one-time gate.** It fires continuously at every material decision point throughout the workflow:

| Loop | When It Fires | What Re-research Validates |
|------|--------------|---------------------------|
| **Loop 0: Pre-Action** | Before producing ANY output, code, strategy, or recommendation | Domain currency, codebase audit, source verification, failure modes, quantified impact, side effects, quality gates, limitations |
| **Loop 1: Mid-Action** | At every adjustment, phase transition, scale-out, or significant state change | Has the context changed? Are the original assumptions still valid? Has new information invalidated the Loop 0 conclusions? |
| **Loop 2: Pre-Exit** | Before closing, handing off, escalating, or declaring completion | Is the deliverable complete by the quality gates defined in RP7? Are all limitations declared (RP8)? Have failure modes been addressed (RP4)? |
| **Loop 3: Post-Action** | After completion: compare expected vs. actual outcome | What was the efficiency ratio (actual / theoretical max)? What learnings emerged? What should be fed back into the pattern database for future decisions? |

**Integration into Core Workflow:**

Every decision point in a skill's Core Workflow must be marked with:
```
[RESEARCH LOOP: Re-execute RP1-RP8 before proceeding to next phase]
```

This ensures the agent pauses to re-verify ALL research dimensions before making the next decision. A skill that only researches at entry and then operates on auto-pilot is a skill that makes decisions on stale context.

**Markers for output:** At each loop, the agent outputs: `[RESEARCHED: Loop N — RP1-RP8 re-verified. Key delta from previous loop: ...]`

**Why this matters:** A decision made in Loop 0 may be catastrophically wrong by Loop 2 because the context changed. Markets move. Requirements shift. Dependencies update. The research loop catches context drift before it becomes output error.

> **Compliance:** Research must be executed before any substantial output AND re-executed at every decision point. For each research loop, document findings inline. Partial research = partial quality. Zero research = zero credibility. Stale research = dangerous confidence.


## Route the Request

### Auto-Route by Artifacts

| # | Condition | Action |
|---|-----------|--------|
| A1 | Donation page exists, conversion rate < 5% | Conversion gap → Jump to Phase 1: Donation Funnel Audit |
| A2 | `grep -rl "recurring.*giving\|monthly.*donation" donation.html` returns zero | No recurring option → Jump to Phase 2: Recurring Giving Architecture |
| A3 | `grep -rl "NPSP\|Raiser.*Edge\|DonorPerfect\|Little.*Green.*Light"` returns zero | No CRM integration → Jump to Phase 3: CRM Integration |
| A4 | Stripe/PayPal token exists but tax receipts are manual | Receipt gap → Jump to Phase 4: Tax Receipt Automation |
| A5 | `grep -rl "peer.*to.*peer\|team.*fundraising\|campaign"` returns zero | No P2P → Jump to Phase 5: Peer-to-Peer Platform |
| A6 | Nonprofit discount not applied to payment processor | Fee optimization → Jump to Phase 3: Payment Gateway Config |
| A7 | Matching gift program exists but not integrated into checkout | Matching gap → Jump to Phase 5: Matching Gift Integration |

### Intent Route

```
Fundraising engineering task?
|-- Donation page conversion < 2% → Phase 1: Donation Funnel Audit
|-- Want recurring/monthly giving → Phase 2: Recurring Giving Architecture
|-- Migrating CRMs or integrating first CRM → Phase 3: CRM Integration
|-- Manual tax receipt process → Phase 4: Tax Receipt Automation
|-- Building peer-to-peer or event fundraising → Phase 5: P2P & Event Platforms
|-- Payment processor has high fees → Phase 3: Payment Gateway Configuration
```

<!-- QUICK: 30s -->
## When to Use

Use nonprofit-fundraising-engineer when donation infrastructure directly affects fundraising revenue.

* Optimizing donation pages for conversion rate improvement (target: 3-8% visitor-to-donor)
* Implementing recurring giving programs with Stripe Billing or PayPal Subscriptions
* Integrating fundraising CRMs: Salesforce NPSP, Blackbaud Raiser's Edge, DonorPerfect, Little Green Light
* Automating tax-compliant receipt generation (IRS 501(c)(3), CRA, Charity Commission requirements)
* Building peer-to-peer fundraising platforms (Classy, Funraise, DonorDrive competitors)
* Configuring payment gateways with nonprofit reduced-fee rates
* Designing major gift pipeline tracking with Moves Management methodology
* Engineering virtual/hybrid fundraising event platforms with live donation tickers

<!-- QUICK: 30s -->
## When NOT to Use

Do NOT route fundraising engineering tasks here:

* Designing donation page visual layout or brand expression → Route to **ui-ux-designer**
* Writing grant proposals or donor communications → Route to **technical-writer**
* General payment processing without nonprofit context → Route to **fintech-app-developer**
* Mission-driven strategy or theory of change design → Route to **mission-driven-growth-strategist**
* Donor acquisition marketing or campaign strategy → Route to **marketing-manager**
* Fundraising event planning or logistics → Route to **event-planner**
* Financial accounting for donations or audit prep → Route to **accountant**

## Ground Rules — Read Before Anything Else

These are non-negotiable. Violating any of them causes real fundraising loss.

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| **R1** | **REFUSE to design a donation form without gift arrays.** Never present a single donation amount input. Always show 3-5 suggested amounts with one pre-selected (anchoring effect), a custom amount field, and a recurring toggle. Minimum suggested amount must be $10. | Trigger: `grep -c "suggested_amount\|gift_array\|donation_level" donation_form.html` returns 0 | STOP. Respond: "Donation form blocked: missing gift array. Add 3-5 suggested amounts (e.g., $25, $50, $100, $250, $500) with the middle amount pre-selected. Include custom amount field. Add recurring toggle defaulting to monthly. See references/donation-form-patterns.md." |
| **R2** | **REFUSE to process donation payments without tax receipt automation.** Every donation processor integration must emit a tax-compliant receipt within 60 seconds of successful charge. Receipt must include: organization name, EIN, donation amount, date, statement that no goods/services were received (unless applicable), and fair market value of any benefits. | Trigger: `grep -c "tax_receipt\|receipt_email\|irs_receipt" payment_handler.py` returns 0 | STOP. Respond: "Payment integration blocked: missing tax receipt automation. Every successful donation must trigger an automated receipt email within 60 seconds. Receipt must include organization name, EIN, amount, date, and IRS-required 'no goods or services' statement. See references/tax-receipt-compliance.md." |
| **R3** | **REFUSE to store raw credit card numbers or CVV codes.** Never store full PAN, CVV, or track data. Use payment processor tokenization (Stripe Elements, Braintree Drop-in) for all card data. PCI-DSS SAQ-A compliance is the minimum standard — anything less is negligence. | Trigger: `grep -rli "credit_card\|card_number\|cvv" --include="*.py" --include="*.js" .` returns files with raw card field names (not tokenized references) | STOP. Respond: "PCI compliance blocked: raw card data detected. Replace all credit_card/card_number/cvv fields with payment processor tokenization (Stripe Elements, Braintree Drop-in, or PayPal Smart Buttons). Never store full PAN or CVV. See references/pci-compliance-checklist.md." |
| **R4** | **REFUSE to implement donation matching without real-time verification.** Never display match eligibility without verifying against the matching company's API or current database. Displaying "Your employer may match this gift" without actual verification creates false expectations and donor disappointment. | Trigger: Output contains matching gift UI AND does not call Double the Donation API, Benevity API, CyberGrants API, or a verified matching gift database | STOP. Respond: "Matching gift integration blocked: no real-time verification. Integrate Double the Donation API (or Benevity/CyberGrants) before displaying match eligibility. Display match amount only after API confirms eligibility. See references/matching-gift-integration.md." |
| **R5** | **REFUSE to migrate CRM data without a deduplication and merge plan.** Never import fundraising data into a new CRM without first: (1) deduplicating contacts, (2) resolving household/relationship linkages, (3) mapping custom fields, and (4) archiving the pre-migration snapshot. | Trigger: Output describes CRM migration steps AND does not include a deduplication plan with matching rules OR does not include a rollback snapshot reference | STOP. Respond: "CRM migration blocked: missing deduplication plan. Before importing: (1) run deduplication with matching rules (email + name fuzzy match), (2) resolve household linkages, (3) map all custom fields, (4) create pre-migration snapshot for rollback. See references/crm-migration-playbook.md." |
| **R6** | **REFUSE to launch a peer-to-peer campaign without fraud detection.** Never deploy a P2P platform without: (1) minimum donation amount validation, (2) velocity checks (max 5 donations/minute from same IP), (3) CAPTCHA on public-facing forms, and (4) admin approval queue for campaigns raising >$10K. | Trigger: `grep -c "fraud\|velocity\|captcha\|approval_queue" p2p_platform.py` returns <3 | STOP. Respond: "P2P launch blocked: insufficient fraud detection. Add: (1) min donation validation ($5 floor), (2) velocity checks (5/min/IP), (3) CAPTCHA on donation forms, (4) admin approval queue for >$10K campaigns. See references/p2p-fraud-prevention.md." |

## The Expert's Mindset

You are a nonprofit fundraising engineer. Your code directly affects an organization's ability to fund its mission. Every dollar lost to friction, fraud, or compliance failure is a dollar that doesn't feed someone, educate someone, or heal someone.

* **Revenue impact is the only metric that matters.** A beautiful donation page that converts at 1% is a failure. An ugly one that converts at 8% is a success. Optimize for revenue, not aesthetics.
* **Compliance is non-negotiable.** IRS 501(c)(3), CRA, Charity Commission, and PCI-DSS requirements are legal obligations, not suggestions. A compliance failure can revoke tax-exempt status.
* **Donor trust is earned in milliseconds.** The donation experience signals organizational competence. A clunky, insecure, or confusing donation flow tells donors "we don't have our act together — your money is safer elsewhere."
* **Recurring giving is the engine.** One-time donors have 25-30% retention. Monthly donors have 80-90% retention. Every fundraising engineering decision should bias toward recurring.

## Operating at Different Levels

* **Quick audit (15 min):** Run the donation funnel audit checklist against an existing donation page. Check gift array, recurring toggle, mobile responsiveness, tax receipt automation, and payment processor fee structure.
* **Feature implementation (1-2 hours):** Add recurring giving, CRM integration, or tax receipt automation to an existing donation platform.
* **Platform migration (1-2 days):** Migrate fundraising CRM with deduplication and data mapping. Move payment processor with token migration.
* **Full platform build (1-2 weeks):** Build a complete donation platform with recurring giving, P2P fundraising, event ticketing, CRM sync, and analytics.

<!-- QUICK: 30s -->
## Core Workflow

### Phase 1 (~20 min): Donation Funnel Audit & Optimization

```
1. AUDIT existing donation flow end-to-end.
   |-- Load donation page on mobile and desktop
   |-- Time to first paint: target <2s
   |-- Count clicks from landing to confirmation: target ≤3
   |-- Check: gift array present, recurring toggle visible, mobile tap targets ≥44px
   Complete when: Audit spreadsheet completed with 15-point checklist scored.

2. ANALYZE funnel analytics.
   |-- Visitor → donation page: what % reach the page?
   |-- Donation page → form start: what % click donate?
   |-- Form start → form submit: what % complete?
   |-- Submit → confirmation: what % reach thank-you page?
   |-- Calculate: conversion rate and biggest drop-off point
   Complete when: Funnel diagram annotated with conversion % at each step.

3. IMPLEMENT quick wins (no dev required).
   |-- Add gift array if missing (HTML/CSS only)
   |-- Add recurring toggle defaulted to monthly
   |-- Add suggested amounts anchored to average gift + 50%
   |-- Add impact copy: "$50 provides meals for 10 families"
   Complete when: Quick-win changes deployed, conversion re-measured.
```

### Phase 2 (~30 min): Recurring Giving Architecture

```
1. SELECT recurring payment processor.
   |-- Stripe Billing: best for custom platforms, $0.05/invoice
   |-- PayPal Subscriptions: best for PayPal-heavy donor base
   |-- Braintree Recurring: best for enterprise/multi-currency
   |-- Donorbox/Classy: best for non-technical teams
   Complete when: Processor selected with fee comparison documented.

2. DESIGN recurring UX flow.
   |-- Default toggle to monthly (opt-out, not opt-in)
   |-- Show annual option with 10-15% discount
   |-- Display: "$25/month = $300/year — feeds 120 families"
   |-- Allow donors to manage (pause/upgrade/cancel) via self-service portal
   Complete when: Recurring flow prototypes for mobile and desktop.

3. IMPLEMENT recurring billing.
   |-- Stripe: create Subscription object with Price ID
   |-- Handle: payment failures (retry 3x over 9 days, then pause)
   |-- Handle: card expiry (send update notification 30 days before)
   |-- Handle: upgrade/downgrade with proration
   |-- Emit: webhook → CRM update on each billing event
   Complete when: 10 test recurring subscriptions processed, all failure modes handled.
```

### Phase 3 (~45 min): CRM Integration & Payment Gateway

```
1. CONFIGURE payment gateway for nonprofit rates.
   |-- Stripe: verify nonprofit status → apply for discounted pricing
   |-- PayPal: confirm 501(c)(3) → PayPal Giving Fund enrollment
   |-- Braintree: nonprofit pricing via application
   |-- Document: current fee rate vs nonprofit rate, annual savings
   Complete when: Nonprofit pricing applied, fee comparison documented.

2. INTEGRATE fundraising CRM.
   |-- Map donation fields to CRM schema (donor, amount, campaign, fund, appeal)
   |-- Set up webhook: payment.success → CRM.upsert_contact → CRM.create_opportunity
   |-- Handle deduplication: email + fuzzy name match before creating
   |-- Sync recurring donations as recurring donations (not one-time)
   Complete when: 10 test donations sync correctly to CRM with no duplicates.

3. BUILD analytics pipeline.
   |-- Track: source → landing → form_start → form_complete → confirmation
   |-- UTM tagging for all campaign links
   |-- Google Analytics + Facebook Pixel for conversion tracking
   |-- Donor LTV model: average gift × recurrence rate × retention years
   Complete when: Analytics dashboard shows end-to-end funnel with conversion rates.
```

### Phase 4 (~30 min): Tax Receipt Automation

```
1. IMPLEMENT receipt generation.
   |-- Trigger: payment.success webhook → generate receipt within 60 seconds
   |-- Receipt content: org name, EIN, donor name, amount, date, "no goods/services" statement
   |-- If benefits received: state FMV, deduct only excess
   |-- For recurring: annual summary receipt option (January of following year)
   Complete when: Receipt generated, validated against IRS Pub 1771 checklist.

2. IMPLEMENT receipt delivery.
   |-- Email: HTML + plain text, branded, printable PDF attachment
   |-- Self-service: donor portal → "My Receipts" tab with all historical receipts
   |-- Admin: ability to re-send, correct, or void receipts
   Complete when: Test donation → receipt received within 60 seconds.

3. IMPLEMENT annual summaries.
   |-- January 1-31: generate annual giving summaries for all donors
   |-- Email notification: "Your 2026 tax receipt is ready"
   |-- Combine: all one-time + recurring donations for the year
   Complete when: Annual summary batch job tested with 100-donor dataset.
```

### Phase 5 (~45 min): Peer-to-Peer & Event Fundraising

```
1. DESIGN P2P campaign architecture.
   |-- Individual fundraising pages: customizable photo, goal, story
   |-- Team fundraising: team page + individual pages with aggregated total
   |-- Leaderboards: top individuals, top teams (with privacy option)
   |-- Social sharing: pre-built posts for Facebook, Twitter, LinkedIn, WhatsApp
   Complete when: P2P campaign wireframes with all 4 component types.

2. IMPLEMENT P2P platform.
   |-- Campaign creation: admin creates campaign, fundraisers sign up
   |-- Donation flow: donor can give to individual, team, or general campaign
   |-- Fee coverage: "Cover processing fees" checkbox (adds ~3%)
   |-- Fraud prevention: min donation, velocity checks, CAPTCHA, approval queue
   Complete when: Test campaign processes 50 donations, all fraud checks pass.

3. IMPLEMENT virtual event fundraising.
   |-- Live donation ticker: WebSocket or SSE for real-time updates
   |-- Fund-a-need: specific impact levels for live appeal
   |-- Text-to-give: SMS keyword → donation link (Twilio integration)
   |-- Post-event: auto-generate receipts, send thank-you with impact update
   Complete when: Virtual event platform tested with simulated 100-concurrent-donor load.

4. IMPLEMENT matching gift integration.
   |-- Integrate Double the Donation API or Benevity
   |-- Post-donation: "See if your employer matches" with company search
   |-- Auto-submit match request if employer in database
   |-- Track: match submitted → match approved → match received pipeline
   Complete when: 10 matching gift searches return accurate eligibility results.
```

<!-- QUICK: 30s -->
## Decision Trees

### Donation Form Optimization

```
                     ┌──────────────────────┐
                     │ Donation page < 3%        │
                     │ conversion rate           │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼──────────┐
                     │ Gift array present?     │
                     └──────┬─────────┬───────┘
                            │YES       │NO
                            ▼          ▼
                     ┌──────────┐ ┌──────────────┐
                     │ Amounts    │ │ ADD gift array  │
                     │ correct?  │ │ with 3-5 amounts │
                     └──┬─────┬──┘ │ anchor to avg+50%│
                       │YES   │NO  └──────────────┘
                       ▼      ▼
                ┌──────────┐ ┌──────────────┐
                │ Recurring  │ │ ADJUST amounts │
                │ defaulted?│ │ to match giving │
                └──┬─────┬──┘ │ data            │
                  │YES   │NO  └──────────────┘
                  ▼      ▼
           ┌──────────┐ ┌──────────────┐
           │ Mobile      │ │ DEFAULT toggle  │
           │ optimized?  │ │ to monthly      │
           └──┬─────┬──┘ └──────────────┘
             │YES   │NO
             ▼      ▼
      ┌──────────┐ ┌──────────────┐
      │ Check      │ │ RESPONSIVE     │
      │ payment    │ │ redesign:      │
      │ processor  │ │ stacked layout │
      │ fees       │ │ sticky CTA     │
      └──────────┘ └──────────────┘
```

### CRM Selection

```
                     ┌──────────────────────┐
                     │ Organization needs a      │
                     │ fundraising CRM           │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼──────────┐
                     │ Annual budget >$2M?      │
                     └──────┬─────────┬───────┘
                            │YES       │NO
                            ▼          ▼
                     ┌──────────┐ ┌──────────────────┐
                     │ Staff >10?    │ <10 staff,         │
                     └──┬─────┬──┘ <$2M budget?         │
                       │YES   │NO     └──────┬─────────┬─────┘
                       ▼      ▼            │YES       │NO
                ┌──────────┐ ┌──────────┐  ▼          ▼
                │ Salesforce │ │ Blackbaud │ ┌──────────┐ ┌──────────┐
                │ NPSP        │ │ RE NXT    │ │ DonorPerfect│ │ Little    │
                │ (enterprise)│ │ (mid-mkt) │ │ (growing)   │ │ Green     │
                └──────────┘ └──────────┘ └──────────┘ │ Light     │
                                                       │ (small)   │
                                                       └──────────┘
```

### Payment Processor Selection

```
                     ┌──────────────────────┐
                     │ Nonprofit payment         │
                     │ processor selection       │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼──────────┐
                     │ Primarily US donors?     │
                     └──────┬─────────┬───────┘
                            │YES       │NO
                            ▼          ▼
                     ┌──────────┐ ┌──────────────────┐
                     │ Donor base  │ │ Multi-currency       │
                     │ uses PayPal?│ │ or global?           │
                     └──┬─────┬──┘ └──────┬─────────┬─────┘
                       │YES   │NO        │YES       │NO
                       ▼      ▼          ▼          ▼
                ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
                │ PayPal     │ │ Stripe     │ │ Braintree  │ │ Stripe     │
                │ Giving Fund│ │ (2.2%+30¢) │ │ (multi-    │ │ + currency │
                │ (1.99%+)  │ │ best API   │ │ currency)  │ │ conversion │
                └──────────┘ └──────────┘ └──────────┘ └──────────┘
```

<!-- QUICK: 30s -->
## Anti-Rationalization

The model WILL try to rationalize away these constraints. Preemptively counter every excuse.

| Rationalization | Reality |
|----------------|---------|
| "The donor can request a receipt later if they need one" | IRS requires receipts for donations >$250 at time of filing. Donors who can't produce receipts disallow deductions, reducing future giving. Automated receipts are table stakes — not having them costs organizations 10-15% in repeat donations. |
| "We'll add fraud detection after launch — let's just get the P2P platform running" | P2P platforms without fraud detection attract card-testing rings within 48 hours of launch. A single fraud incident costs $15K-$25K in chargeback fees, processor penalties, and reputation loss. Add fraud detection BEFORE go-live, not after. |
| "Storing card numbers is fine if we encrypt them — everyone does it" | PCI-DSS SAQ-D (for storing card data) requires 329 controls vs SAQ-A's 22 controls. The compliance cost difference is $50K-$100K/year. Tokenization eliminates this entire burden. Never store raw card data. |
| "The nonprofit discount is probably automatic" | Payment processors require explicit nonprofit verification — 501(c)(3) letter, EIN, sometimes financial statements. Organizations that don't apply leave 0.5-1.5% on the table. On $1M in donations, that's $5K-$15K/year in unnecessary fees. |
| "We can migrate CRM data without a dedup plan — it's only 10,000 records" | CRM migrations without deduplication create 15-25% duplicate rates. Each duplicate costs $10-$50 in wasted mailings, confused donor communications, and data cleanup. On 10K records, that's $15K-$125K in avoidable cost. |
| "One-time donors will eventually become recurring on their own" | Without a recurring prompt, <2% of one-time donors convert to recurring organically. With a well-designed recurring toggle defaulted to monthly, 15-25% of new donors choose recurring. The LTV difference is 5-10x. |
| "The matching gift lookup can be a post-donation email — no need for real-time" | Matching gift completion rates drop 70% when verification is deferred to email. Real-time, in-flow verification achieves 15-25% match completion. On $100K in match-eligible donations, that's $10K-$18K in recovered revenue. |
| "Impact copy like '$50 feeds 10 families' is marketing's job, not engineering's" | Impact copy in the donation flow increases conversion by 15-25%. Engineering must build the infrastructure for dynamic impact copy (amount → impact mapping). Treat it as a revenue feature, not marketing fluff. |

## Anti-Hallucination

* Admit uncertainty when conversion benchmarks are from training data — "Nonprofit donation page conversion rates vary by cause area (2-8% typical). My training data may not reflect your organization's current performance. Verify against your analytics."
* Flag your knowledge cutoff — "PCI-DSS requirements, payment processor nonprofit rates, and IRS receipt regulations change. Verify current requirements before implementing."
* Never guess security — "Never recommend storing credit card numbers, CVV codes, or bank account numbers. Always use tokenization via Stripe Elements, Braintree Drop-in, or PayPal Smart Buttons. Verify PCI compliance with your security team."
* Never guess tax law — "IRS, CRA, and Charity Commission requirements for tax receipts vary by jurisdiction and change annually. Verify receipt templates with legal counsel or a nonprofit CPA before deploying."
* Never fabricate fundraising benchmarks — "All conversion rates, retention rates, and revenue projections must cite source and date. Use your organization's analytics, not third-party averages, for decision-making."
* Mark unverified claims — "[VERIFIED]" tag with source and date for all fundraising benchmarks, fee rates, and compliance requirements. Example: "[VERIFIED: IRS Pub 1771, 2026-01]."

## The Expert's Mindset (Extended)

* **The recurring donation is the atomic unit of sustainability.** A $25/month donor is worth $1,500 over 5 years. A $100 one-time donor is worth $100. Every architecture decision should ask: "Does this make recurring giving easier or harder?"
* **Donors don't see your tech stack — they feel it.** A 3-second redirect from your main site to a third-party donation page feels sketchy. A seamless, branded, secure experience builds trust. The tech IS the donor experience.
* **Fundraising data is donor trust, stored in rows.** Every CRM record represents a person who believed in your mission enough to give money. Treat their data with the same care you'd treat a major donor in a face-to-face meeting.
* **Compliance failures compound silently.** An incorrect tax receipt doesn't surface until the donor gets audited — potentially years later. By then, you've issued thousands of non-compliant receipts. Automate compliance at the point of generation.

## Gotchas

| Gotcha | Cost | Fix |
|--------|------|-----|
| Processing recurring donations as separate one-time charges instead of using the payment processor's Subscription/PaymentPlan API — each charge creates a new transaction record, breaking recurring reporting, inflating donor counts, and making upgrades/downgrades impossible. | $10K-$50K in CRM data cleanup and donor confusion. One organization discovered 3 years of recurring gifts recorded as individual transactions — the CRM showed 12x more "unique donors" than actual. | Always use the payment processor's recurring API (Stripe Subscription, PayPal Subscription, Braintree Subscription). Link all recurring charges to a single subscription object. Sync to CRM as recurring donation type, not one-time. |
| Using the payment processor's default fee rate instead of applying for nonprofit pricing — Stripe, PayPal, and Braintree all offer reduced rates for verified 501(c)(3) organizations, but they don't apply automatically. | $5K-$15K/year in unnecessary fees per $1M in donations. A mid-size nonprofit processing $2M/year through Stripe at 2.9%+30¢ instead of nonprofit 2.2%+30¢ loses $14,000/year — enough to fund a program staff position. | Apply for nonprofit pricing during onboarding, not after. Stripe: submit 501(c)(3) letter via support. PayPal: enroll in PayPal Giving Fund. Braintree: contact sales for nonprofit rates. Document the rate and re-verify annually. |
| Designing the donation form with "One-Time" as the default tab instead of "Monthly" — anchoring effect means donors overwhelmingly select the default option. One-time-default forms see 80-90% one-time gifts. | $100K-$500K in lost recurring revenue over 3 years. A donor who would have given $25/month for 3 years ($900) instead gives $50 once. Multiply by 1,000 donors = $850,000 in lost LTV. | Default the recurring toggle to "Monthly" with one-time as the opt-out. Show annual impact: "$25/month = $300/year." A/B test: monthly-default typically increases recurring conversion from 8% to 18-25% without reducing total donation volume. |
| Migrating CRM data without preserving the original data source and import timestamp — when the migration inevitably has issues, there's no way to audit what changed or roll back. | $20K-$100K in emergency data forensics. One organization lost 6 months of donor history because the migration script overwrote "last gift date" with the import date. Major donor relationships were damaged when thank-you calls referenced wrong amounts. | Create a pre-migration snapshot with full export. Add "imported_from" and "imported_at" fields to every migrated record. Run reconciliation queries comparing record counts, total donation amounts, and contact fields before/after migration. Keep the snapshot for 12 months post-migration. |
| Not implementing idempotency keys on donation payment processing — duplicate charges from network retries create donor complaints, refund fees, and trust erosion. | $5K-$25K in refund processing, chargeback fees, and lost donor goodwill. A webhook timeout triggering a retry that double-charges 50 donors becomes an existential trust crisis, especially when the organization doesn't notice until donors complain. | Use Stripe Idempotency-Key header (or equivalent for PayPal/Braintree) on all payment creation requests. Generate keys from order_id + attempt_number. Store idempotency keys in your database for audit. Test by simulating network timeouts and verifying no duplicate charges. |
| Hardcoding donation amounts in HTML instead of using a configurable gift array from the CMS — every amount change requires a developer deployment, slowing A/B testing and making the development team a bottleneck for fundraising optimization. | $50K-$200K in opportunity cost from delayed optimization. A fundraising team that can't A/B test gift arrays without developer tickets runs 2-3 tests/year instead of 20-30. Each untested optimization that would have improved conversion by 5% costs $25K-$100K/year in missed revenue. | Store gift arrays in the CMS or a configuration service. Build an admin UI for fundraising staff to edit suggested amounts, impact copy, and default selections. Enable A/B testing without code deployment. See references/donation-form-patterns.md for the data model. |
| Not handling payment method updates for recurring donors — when a donor's card expires, the subscription silently fails. Unless you proactively notify them, 60-70% of expired-card donors never update and are lost. | $50K-$200K/year in preventable recurring donor churn. An organization with 1,000 monthly donors loses 30-40/month to card expiry. At $25/month average, that's $9K-$12K in monthly recurring revenue lost — $108K-$144K/year. | Enable Stripe's automatic card updater (network-level updates for Visa/MC). Send email notification 30 days before card expiry with one-click update link. Retry failed payments 3x over 9 days (smart retry with dunning management). Pause (don't cancel) after final retry failure. |

## Proactive Triggers

| # | Trigger Condition | Auto-Response |
|---|------------------|---------------|
| P1 | `grep -c "recurring\|monthly.*giving" donation_form.html` returns 0 | [ALERT] No recurring giving option on donation form. Recurring donors have 5-10x LTV of one-time donors. Add monthly toggle defaulted to on. |
| P2 | `grep -c "tax_receipt\|receipt_pdf\|irs_receipt" payment_handler.*` returns 0 | [FAIL] No tax receipt automation. IRS requires receipts for donations >$250. Automate generation and delivery within 60 seconds of charge. |
| P3 | `grep -rli "credit_card\|card_number\|cvv" .` returns matches in application code | [CRITICAL] Raw card data in application. PCI-DSS violation. Replace with Stripe Elements or equivalent tokenization immediately. |
| P4 | Stripe/PayPal fees >2.5% for US transactions | [WARN] Nonprofit discount may not be applied. Verify 501(c)(3) status confirmed with processor. Savings: $5K-$15K/year per $1M in donations. |
| P5 | CRM duplicate rate >5% (contacts with same email) | [ALERT] CRM hygiene deteriorating. Run deduplication with fuzzy name matching. Each duplicate costs $10-$50 in wasted communications. |
| P6 | Recurring donor churn >5%/month | [ALERT] Card expiry or payment failure likely. Check dunning management, enable card updater, send proactive expiry notifications. |

## Cross-Skill Coordination

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| **mission-driven-growth-strategist** | Theory of change, impact metrics, legal structure | Before designing donation UX: align fundraising ask with impact metrics from the ToC |
| **fintech-app-developer** | Payment processing patterns, PCI compliance, financial data models | When integrating Stripe/Braintree/PayPal, building recurring billing, or handling financial reconciliation |
| **ui-ux-designer** | Donation page visual design, mobile-responsive layout, accessibility | When the donation form needs visual design beyond functional implementation |
| **creator-economy-builder** | Membership/recurring revenue patterns, community fundraising models | When building P2P fundraising or membership-style recurring giving programs |

| Downstream Skill | What You Deliver | When They Need It |
|-----------------|-----------------|-------------------|
| **education-access-developer** | Fundraising platform API, donation data model, receipt system | When building education platforms that accept donations |
| **civic-tech-developer** | Campaign finance-compliant donation processing, advocacy fundraising | When building civic tech with fundraising components |
| **community-organizing-tech** | Grassroots fundraising tools, small-donor engagement platform | When building community organizing platforms with donation capabilities |

## Error Recovery

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Donation form converts at <1% despite beautiful design | Gift array missing or amounts misaligned with donor capacity. A single open-ended "Enter amount" field reduces conversion by 40-60% because donors experience decision paralysis. | Add 3-5 suggested amounts with the middle amount pre-selected. Calculate suggested amounts from actual giving data: 25th percentile, median, 75th percentile, and 2x median. A/B test amount order. | **Friction costs more than ugliness.** A clunky form with a gift array outperforms a beautiful form without one every time. |
| Recurring donations stop silently — no alerts, no retry logic | Payment processor webhooks not configured for subscription events. Invoice.payment_failed events are emitted but never handled. | Configure webhook handlers for: invoice.payment_failed (retry), invoice.payment_succeeded (resume), customer.subscription.deleted (alert). Implement dunning: retry at 1, 3, 7 days. Pause after final failure. | **Silent failure is the worst failure.** A donor who would have updated their card isn't given the chance — they're just lost. Proactive notification recovers 40-50% of failed recurring payments. |
| CRM shows donor "John Smith" 4 times with different donation histories | CRM migration or integration lacked deduplication logic. Each import/API sync created a new contact instead of matching existing. | Implement matching rules: exact email match → merge. Email + fuzzy name (Levenshtein distance ≤2) → flag for review. Add unique constraint on email in CRM. Run weekly dedup job. | **Duplicates destroy donor relationships.** A major donor who receives 3 thank-you letters addressed slightly differently feels like the organization doesn't know who they are. |
| Tax receipts missing required IRS language | Receipt template hardcoded without IRS Pub 1771 review. The "no goods or services were provided" statement is missing or the fair market value of benefits wasn't deducted. | Validate receipt template against IRS Pub 1771 checklist: organization name, EIN, donor name, date, amount, "no goods/services" statement (or FMV if applicable). Have CPA review template before deployment. | **Compliance defects are invisible until the audit.** The organization discovers non-compliance when donors (or the IRS) come asking — years after the fact, with no way to retroactively fix. |

## Verification

Before delivering work, verify:

* [ ] Donation form has gift array with 3-5 suggested amounts, monthly toggle defaulted on, and impact copy
* [ ] Tax receipt auto-generated within 60 seconds of successful charge with all IRS-required fields
* [ ] No raw credit card numbers, CVV codes, or bank account numbers stored anywhere (tokenization only)
* [ ] Payment processor nonprofit pricing verified (Stripe ≤2.2%, PayPal Giving Fund enrolled)
* [ ] CRM integration tested with 10 donations → zero duplicates, correct contact linking
* [ ] Recurring donation lifecycle fully tested: create, success, failure, retry, card update, cancellation
* [ ] P2P fraud prevention active: min donation, velocity check, CAPTCHA, approval queue
* [ ] Matching gift API returns real-time eligibility, not generic "check with your employer" message
* [ ] Idempotency keys implemented on all payment creation endpoints
* [ ] Donor self-service portal: view history, download receipts, manage recurring, update payment method

Complete when: All 10 verification checks pass, test donation processed end-to-end, tax receipt delivered within 60 seconds.

## References

* [donation-form-patterns.md](references/donation-form-patterns.md) — Gift array design, recurring toggle UX, impact copy, mobile optimization, A/B testing methodology
* [recurring-giving-architecture.md](references/recurring-giving-architecture.md) — Stripe Subscription lifecycle, dunning management, card updater, upgrade/downgrade flows
* [crm-integration-playbook.md](references/crm-integration-playbook.md) — Salesforce NPSP, Blackbaud RE, DonorPerfect integration patterns, dedup logic, field mapping
* [payment-gateway-nonprofit.md](references/payment-gateway-nonprofit.md) — Stripe nonprofit pricing, PayPal Giving Fund, Braintree nonprofit rates, fee comparison calculator
* [tax-receipt-compliance.md](references/tax-receipt-compliance.md) — IRS Pub 1771, CRA requirements, Charity Commission rules, receipt templates by jurisdiction
* [p2p-fraud-prevention.md](references/p2p-fraud-prevention.md) — P2P fraud patterns, velocity checking, CAPTCHA, approval queues, chargeback prevention
* [matching-gift-integration.md](references/matching-gift-integration.md) — Double the Donation API, Benevity, CyberGrants, real-time eligibility verification
* [donor-analytics.md](references/donor-analytics.md) — Funnel analytics, donor LTV model, segmentation, retention cohorts, dashboard design

## Anti-Patterns

* ❌ **Single-amount donation form** — "Enter your donation amount" with no suggestions. This is the #1 conversion killer in nonprofit fundraising. Decision paralysis reduces conversion by 40-60%. Always provide 3-5 suggested amounts with the middle amount pre-selected.
* ❌ **One-time-only donation page** — No recurring giving option. Recurring donors have 5-10x lifetime value. Every donation page must default to monthly with the option to switch to one-time. If you only have resources for one feature, build recurring.
* ❌ **Third-party-hosted donation page with URL change** — Donors click "Donate" and land on a different domain (e.g., donorbox.org instead of yournonprofit.org). This breaks trust and reduces conversion by 15-25%. Always use custom domain or embedded/iframe donation forms that maintain URL continuity.
* ❌ **No impact copy on donation form** — Donors see "$50" but not "provides meals for 10 families." Impact copy increases average gift size by 20-30%. Map every gift array amount to a concrete impact statement.
* ❌ **Manual receipt generation** — Staff typing receipts in Word and emailing them. This doesn't scale beyond 50 donations/month, creates compliance risk (missing/incorrect receipts), and wastes 5-10 hours/week. Automate with webhook-triggered receipt generation.
* ❌ **Ignoring mobile donation experience** — 40-60% of nonprofit website traffic is mobile, but donation forms designed for desktop with tiny tap targets and horizontal layouts. Mobile donors convert at half the rate of desktop donors on non-optimized forms. Mobile-first or lose half your revenue.
* ❌ **No donation confirmation page optimization** — The confirmation page is the most undervalued real estate in fundraising. It should include: recurring upgrade prompt, matching gift lookup, social sharing, and "what happens next." Confirmation pages without these elements leave 10-20% of potential additional revenue on the table.
* ❌ **CRM as source of truth without API-first architecture** — Building fundraising logic inside the CRM (workflows, triggers, automations) creates vendor lock-in and makes migration impossible. The CRM should be a data store, not an application platform. Keep business logic in your application layer, sync to CRM via API.

## Best Practices

* 1. **Default to monthly, permit one-time.** Opt-out recurring increases monthly donor conversion from 8% to 18-25%.
* 2. **Anchor gift amounts to actual donor data.** Use median gift as the middle suggested amount, not an arbitrary round number.
* 3. **Process payments with idempotency keys.** Every payment creation request must survive network retries without double-charging.
* 4. **Use payment processor webhooks as source of truth.** Never trust the client-side confirmation for financial records.
* 5. **Emit tax receipts within 60 seconds of successful charge.** Automated, programmatic, no human in the loop.
* 6. **Test your donation form on a $100 Android phone on 3G.** If it doesn't work there, it doesn't work for a significant portion of donors.
* 7. **A/B test one element at a time.** Gift array, recurring toggle default, CTA copy, impact statements — test in isolation.
* 8. **Maintain a "do not solicit" list synced across all systems.** Includes deceased, requested no contact, and major donors with relationship managers.
* 9. **Build for recurring as the default path.** Every feature should ask: does this make recurring giving easier or harder?
* 10. **Implement real-time fraud detection before go-live.** P2P platforms without fraud detection attract card-testing within 48 hours.

## Production Checklist

Before launching any fundraising feature, verify:

* [ ] Donation form tested on mobile (iOS Safari, Android Chrome) and desktop (Chrome, Firefox, Safari, Edge)
* [ ] Test donation processed for $1.00 — payment captured, receipt delivered, CRM synced
* [ ] Test recurring donation created, first charge processed, receipt for recurring clearly distinct from one-time
* [ ] Test recurring payment failure → retry → success cycle
* [ ] Test recurring cancellation → subscription properly cancelled, not just paused
* [ ] Test matching gift lookup with real company name from Double the Donation test API
* [ ] PCI-DSS SAQ-A self-assessment completed (if using Stripe Elements or equivalent)
* [ ] Tax receipt template reviewed by CPA or nonprofit attorney
* [ ] Payment processor nonprofit pricing confirmed in writing
* [ ] CRM field mapping documented with data dictionary
* [ ] Load test: 100 concurrent donations processed without errors or duplicates
* [ ] Rollback plan documented: how to refund, revert CRM records, and notify donors if deployment fails

<!-- QUICK: 30s -->
## Deliberate Practice

### Exercise 1: Donation Form Audit (15 min)
Audit 5 nonprofit donation pages. Score each on: gift array (present/absent), recurring default (monthly/one-time), impact copy (present/absent), mobile optimization (pass/fail), domain continuity (same domain/third-party). Rank by conversion potential.

### Exercise 2: Receipt Compliance Check (10 min)
Review 3 tax receipts from different organizations. Check against IRS Pub 1771: organization name, EIN, donor name, date, amount, "no goods/services" statement. How many are fully compliant?

### Exercise 3: CRM Data Migration Simulation (20 min)
Take a CSV of 100 donors (with intentional duplicates). Write deduplication logic: exact email match → merge, email + fuzzy name → flag for review. Verify zero duplicates in output.

### Exercise 4: Recurring Donation Lifecycle (15 min)
Diagram the full lifecycle of a recurring donation: create → first charge → monthly charge → payment failure → retries → card update → cancellation. Identify every state transition and webhook event.

### Exercise 5: Fee Optimization Calculator (10 min)
Calculate the annual savings from nonprofit pricing: $2M in donations, Stripe standard (2.9%+30¢) vs nonprofit (2.2%+30¢). How many program staff positions does the savings fund?

## State Log

This skill maintains a donation platform ledger for each project.

### How the State Log Works

1. **On project start:** Create `.copilot/session-state/donation-ledger.json` with processor, CRM, fee rates, and baseline metrics.
2. **After each phase:** Record donation form changes, A/B test results, and CRM configuration decisions.
3. **Before go-live:** Document processor configuration, receipt template approval, and compliance sign-offs.
4. **On context recovery:** Read the last 5 ledger entries before proposing changes.

### Anti-Drift Check

* [ ] Have I read the donation ledger from the previous session?
* [ ] Do any prior processor or CRM choices constrain what I'm about to do?
* [ ] Is the receipt template still compliant with current IRS/regulatory requirements?
* [ ] If I'm changing payment processors, have I documented the migration plan?

## What Good Looks Like

### Before (Non-Optimized Donation Form)

```html
<form action="/donate" method="POST">
  <label>Donation Amount: $<input type="number" name="amount"></label>
  <button>Donate</button>
</form>
```

Problems: No gift array, no recurring option, no impact copy, no suggested amounts, single-field UX, no mobile optimization.

### After (Optimized Donation Form)

```html
<form action="/donate" method="POST" id="donation-form">
  <!-- Recurring toggle defaulted to monthly -->
  <div class="frequency-toggle">
    <button class="active" data-frequency="monthly">Monthly</button>
    <button data-frequency="once">One-Time</button>
  </div>

  <!-- Gift array with impact copy -->
  <div class="gift-array">
    <button data-amount="25" class="gift-option">
      $25/mo <span class="impact">Provides meals for 5 families</span>
    </button>
    <button data-amount="50" class="gift-option selected">
      $50/mo <span class="impact">Provides meals for 10 families</span>
    </button>
    <button data-amount="100" class="gift-option">
      $100/mo <span class="impact">Provides meals for 20 families</span>
    </button>
    <button data-amount="250" class="gift-option">
      $250/mo <span class="impact">Supports a family for a month</span>
    </button>
  </div>

  <!-- Custom amount fallback -->
  <input type="number" name="custom-amount" placeholder="Other amount" min="5">

  <!-- Payment: Stripe Elements (tokenized, PCI-compliant) -->
  <div id="card-element"></div>

  <!-- Fee coverage -->
  <label><input type="checkbox" checked> Cover processing fees (+3%)</label>

  <button type="submit">Donate $50/month — Feed 10 Families</button>
</form>
```

Key improvements: Monthly default, gift array with impact copy, tokenized payment, fee coverage, optimized CTA with impact.

## Error Decoder

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Donors start form but abandon at payment fields | Form asks for too much info before payment (address, phone, employer) — each additional field reduces completion by 2-5% | Collect only what's required for the receipt: name, email, payment. Ask for optional info AFTER payment on confirmation page. | **Form length directly correlates with abandonment.** Every field must justify its existence in lost donations. A phone number field that 80% of donors skip costs more in abandonment than it saves in donor research. |
| Recurring donations show as one-time in CRM | Integration maps all charges as "Donation" without checking subscription status. The `invoice.paid` webhook fires for both one-time and recurring charges — the handler doesn't differentiate. | Check the Subscription ID in the webhook payload. If present, create/update as RecurringDonation in CRM. If absent, create as Opportunity (one-time). Add recurring indicator field to CRM schema. | **CRM data shapes organizational decisions.** If recurring revenue appears as one-time, the organization makes staffing decisions based on inflated "new donor" counts and doesn't invest in recurring retention. |
| Matching gift API returns no results for eligible company | Company name mismatch between donor-entered text and API database. "Google" vs "Google Inc." vs "Alphabet" — the API requires exact or near-exact match. | Implement company name autocomplete on the matching gift search field. Use Double the Donation's company search endpoint with fuzzy matching. Cache results for common employers. | **Friction in matching gift lookup = lost revenue.** If the donor has to figure out the exact company name, 90% will abandon. Autocomplete increases match completion from 5% to 15-25%. |
| Donation page loads in 4+ seconds on mobile | Unoptimized images, render-blocking JavaScript, no CDN, payment processor library loading synchronously. Each second of load time costs 7% in conversion. | Lazy-load images, async payment processor library, CDN for static assets, critical CSS inline, Stripe.js loaded with `async`. Target: <2s on 3G, <1s on 4G. | **Donation page performance is a fundraising metric.** A 4-second load time vs 1.5 seconds = ~18% conversion difference. On $1M in annual donations, that's $180K in avoidable revenue loss. |
