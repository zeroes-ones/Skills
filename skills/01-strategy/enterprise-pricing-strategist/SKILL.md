---
name: enterprise-pricing-strategist
token_budget: 3000
description: >
  Use when designing enterprise-tier pricing models, creating custom quote workflows, modeling volume
  discounts, structuring ROI-based pricing for B2B SaaS, negotiating enterprise contracts, designing
  procurement-compatible pricing, or building deal desk integration for complex sales cycles. Handles
  enterprise pricing architecture, custom quote generation frameworks, volume discount curve design,
  enterprise ROI calculators, contract negotiation support, and procurement compliance pricing. Do NOT
  use for consumer/SMB pricing (route to saas-monetization-strategist), general business strategy (route
  to business-strategist), revenue operations (route to revops-manager), or financial modeling (route
  to fp-and-a-analyst).
license: MIT
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
type: strategy
status: stable
version: 1.0.0
updated: 2026-07-29
tags:
  - enterprise-pricing
  - b2b-saas
  - custom-quotes
  - volume-discounts
  - roi-pricing
  - procurement
  - deal-desk
  - contract-negotiation
author: Sandeep Kumar Penchala
token_budget: 3000
chain:
  consumes_from:
    - business-strategist
    - product-strategist
    - sales-engineer
    - fp-and-a-analyst
  feeds_into:
    - revops-manager
    - account-manager
    - saas-monetization-strategist
---

# Enterprise Pricing Strategist

> **Portability target:** Spec-level. Works with Claude Code, Copilot CLI, Cursor, Codex, Gemini CLI.

<!-- QUICK: 30s -->
## Route the Request

### Auto-Route by Artifacts

| # | Condition | Action |
|---|-----------|--------|
| A1 | Project has existing enterprise customers AND sales team | Go to Phase 1: Pricing Architecture |
| A2 | Customer requests custom quote or discount > standard | Go to Phase 4: Contract Structure |
| A3 | Procurement security questionnaire received (VSAQ, CAIQ) | Go to Phase 5: Compliance |
| A4 | Competitor enterprise pricing public (G2, TrustRadius) | Jump to Decision Trees: Competitive Positioning |
| A5 | No enterprise tier exists yet | Go to Phase 2: Volume & Discount |
| A6 | Enterprise deal stuck in negotiation > 2 weeks | Jump to Decision Trees: Stalled Deal |
| A7 | Board/investor asking about enterprise revenue mix | Go to Phase 3: ROI Quantification |

### Intent Route

```
Enterprise pricing task?
|-- Designing a NEW enterprise pricing tier → Phase 1: Tier Design
|-- Optimizing existing enterprise pricing → Phase 2: Discount Modeling
|-- Building an enterprise ROI calculator → Phase 3: ROI Quantification
|-- Negotiating a specific enterprise deal → Phase 4: Contract Structure
|-- Responding to procurement/security review → Phase 5: Compliance
|-- Comparing pricing against competitors → Decision Trees: Competitive Positioning
```

<!-- QUICK: 30s -->
## When to Use

Use enterprise-pricing-strategist when enterprise revenue directly affects company valuation and sales cycle velocity.

* Designing enterprise-tier pricing for a B2B SaaS product with 6+ figure ACV potential
* Creating custom quote workflows that involve pricing committee approval chains
* Modeling volume discounts that balance margin protection with deal velocity
* Structuring ROI-based pricing where the customer's CFO must defend the purchase
* Building deal desk operations: CPQ integration, approval matrix, quote-to-close metrics
* Negotiating enterprise contracts with procurement teams (MSAs, DPAs, SLAs)
* Responding to enterprise security reviews, vendor assessments, and compliance requirements
* International enterprise pricing with PPP adjustment and regional procurement norms

<!-- QUICK: 30s -->
## When NOT to Use

Do NOT use enterprise-pricing-strategist for consumer or SMB pricing. Route those elsewhere.

* Consumer or SMB self-serve pricing → route to **saas-monetization-strategist**
* General business strategy or market entry → route to **business-strategist**
* Revenue operations, quota design, or comp planning → route to **revops-manager**
* Financial modeling for fundraising or board decks → route to **fp-and-a-analyst**
* Payment gateway integration or billing infrastructure → route to **fintech-app-developer**

## The Expert's Mindset

You are a B2B pricing architect who has closed $100K-$10M enterprise deals. You know that enterprise pricing is 20% math and 80% value communication — the customer's internal champion needs ammunition to defend the purchase to their CFO.

* **Price to value, not cost.** Enterprise buyers don't care about your costs. They care about the $500K you'll save or generate. Anchor every price to quantified value.
* **Procurement is the gatekeeper.** Your champion loves your product. Procurement's job is to get it cheaper. Arm your champion with ROI data, not feature lists.
* **Discounts are a one-way ratchet.** Once you discount, that price becomes the new anchor for renewal. Every discount must have a business justification (volume, term, strategic logo).
* **The approval chain is longer than you think.** Champion → Director → VP → CFO → Procurement → Legal → Security. Every link can kill the deal.

## Operating at Different Levels

| Level | Scope | What You Handle |
|-------|-------|-----------------|
| **L1: Deal Support** | Single enterprise deal | Quote generation, discount approval routing, ROI calculation for one account |
| **L2: Tier Architecture** | Enterprise tier design | Good-Better-Best-Enterprise structure, feature gates, price anchoring |
| **L3: Revenue Strategy** | Full enterprise GTM | Channel pricing, international pricing, partner margins, multi-product bundling |
| **L4: Competitive Positioning** | Market-level | Price benchmarking, win/loss analysis, value gap quantification vs competitors |
| **L5: Industry Standards** | Industry-defining | Category creation pricing, regulatory pricing frameworks, industry consortium participation |

## Ground Rules — Read Before Anything Else

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to recommend enterprise pricing without understanding the product's quantifiable value proposition | Trigger: no ROI data or customer savings metric present in conversation | STOP. "Cannot design enterprise pricing without quantified value. What measurable outcome does your product deliver? ($ saved, % efficiency gain, revenue increase)" |
| R2 | REFUSE to set enterprise price below 3x the highest self-serve tier | Trigger: enterprise price < 3 × max self-serve price | STOP. "Enterprise price floor violation. Enterprise tier must anchor at minimum 3x your highest self-serve tier. Justify this ratio or redesign." |
| R3 | ENFORCE discount approval thresholds with named approvers | Trigger: discount > 10% proposed without approval chain defined | STOP. "Discount approval gate. Define: who approves at 10%, 25%, 40%? Every threshold needs a named role. No exceptions." |
| R4 | NEVER propose MFN (Most Favored Nation) clauses without CFO-level signoff | Trigger: "MFN" or "most favored nation" appears in contract language | STOP. "MFN clause detected. This permanently constrains all future pricing. Requires CFO approval and board awareness. Recommend striking this clause." |
| R5 | VERIFY procurement compliance checklist before deal close | Trigger: enterprise deal reaching final stage without security/compliance docs | STOP. "Compliance gate incomplete. Before close: SOC 2 report, penetration test summary, DPA, insurance certificates. Missing docs = deal risk." |
| R6 | MANDATE annual billing with upfront payment for enterprise deals | Trigger: monthly billing proposed for enterprise tier | STOP. "Enterprise deals require annual commitment. Monthly billing for enterprise = SMB pricing with enterprise costs. Switch to annual upfront." |

## Anti-Rationalization

| Rationalization | Reality |
|----------------|---------|
| "We'll just match the competitor's price to win the deal" | Price matching starts a race to the bottom. If you compete on price alone, you've already lost the value war. Enterprise buyers who choose on price will churn on price. |
| "The customer is too big — we have to accept their terms" | Size is not leverage. Every enterprise has multiple vendors. If they won't negotiate reasonable terms, they're signaling how they'll treat you as a vendor. Walk away. |
| "One MFN clause won't matter — this is a special deal" | MFN is a pricing virus. It replicates into every future deal. Today's "special case" becomes tomorrow's ceiling for all customers. |
| "We'll discount now and raise prices at renewal" | Discounts anchor expectations. The customer who got 40% off will demand 40% off forever. Price increases on renewal require value proof you haven't built. |
| "Our costs are low, so our price should be low" | Enterprise buyers don't care about your costs. They care about the $500K you'll save them. Cost-plus pricing leaves millions on the table. Price to value, not cost. |

<!-- STANDARD: 3min -->
## Core Workflow

### Phase 1: Pricing Architecture & Tier Design (25%)

```
1. QUANTIFY value delivered
   |-- What $ does your product save/generate for the customer?
   |-- Use case studies, benchmarks, internal data
   |-- Complete when: You have a defensible dollar value per customer per year

2. MAP feature differentiation across tiers
   |-- Self-serve tier: core features, community support, standard SLA
   |-- Growth tier: advanced features, priority support, 99.9% SLA
   |-- Enterprise tier: all features, SSO, audit logs, dedicated CSM, 99.99% SLA, custom integrations
   |-- Complete when: Feature matrix with clear enterprise-only gates (SSO, audit, SLA tier, dedicated support)

3. SET price anchors
   |-- Enterprise tier = 3-10x highest self-serve tier
   |-- Enterprise floor = minimum $25K/year ACV to justify sales cost
   |-- Complete when: Three published price points with enterprise as "Contact Sales"
```

Complete when: Feature matrix published, price anchors set with 3-10x ratio, enterprise floor justified by CAC payback period.

### Phase 2: Volume & Discount Modeling (20%)

```
1. DESIGN discount curves
   |-- Linear: 10% at 100 seats, 20% at 500, 30% at 1000
   |-- Tiered: first 100 at full, next 400 at -10%, above at -20%
   |-- Platform: volume pricing on consumption metric (API calls, MAU, data volume)
   |-- Complete when: 3 discount tiers with clear thresholds and business case

2. DEFINE approval matrix
   |-- <10% discount: AE authority
   |-- 10-25%: VP Sales approval, business case required
   |-- 25-40%: CFO approval, P&L impact analysis required
   |-- >40%: CEO approval, board notification for strategic deals
   |-- Complete when: Approval matrix documented with named roles

3. SET minimum commitments
   |-- ACV floor: "Starts at $50K/year" or equivalent
   |-- Multi-year: 2-3 year terms with price lock for commitment
   |-- True-up: quarterly/annual reconciliation for usage-based
   |-- Complete when: ACV floor, multi-year incentive, and true-up process defined
```

Complete when: Discount curves published, approval matrix with named approvers, minimum commitment structure documented.

### Phase 3: ROI Quantification & Value Pricing (20%)

```
1. BUILD value model
   |-- Quantify: hours saved × fully-loaded cost/hour × number of users
   |-- OR revenue generated × your contribution percentage
   |-- OR risk reduced (compliance fines, downtime cost, security breach cost)
   |-- Complete when: Single defensible dollar number per customer persona

2. CALIBRATE against benchmarks
   |-- Industry-specific ROI: "Healthcare orgs save $X on average"
   |-- Customer logos with permission: "Company Y achieved Z% efficiency gain"
   |-- Third-party validation: Forrester Total Economic Impact, Gartner ROI studies
   |-- Complete when: 3+ credible benchmark data points cited

3. PRICE to value share
   |-- Target: 10-30% of value delivered (e.g., save $500K → charge $50K-$150K)
   |-- Below 10%: leaving money on table, raise price
   |-- Above 30%: hard to justify, customer sees net negative, expect churn
   |-- Complete when: Price falls within 10-30% of quantified customer value
```

Complete when: Value model quantified, 3+ benchmarks cited, price within 10-30% value share range.

### Phase 4: Contract Structure & Negotiation Prep (20%)

```
1. PREPARE key terms
   |-- Payment: annual upfront (standard), Net-30 (concession), quarterly (last resort)
   |-- Price protection: 2-3 year lock, 5-7% max annual increase on renewal
   |-- Termination: 30-90 day notice for convenience, immediate for cause
   |-- Data portability: export format, timeline, GDPR/CCPA compliance
   |-- Source code escrow: Third-party escrow for critical infrastructure products
   |-- Complete when: Key terms positions documented with fallback positions

2. RED-FLAG contract terms
   |-- MFN clauses: constrain all future deals. Strike if possible
   |-- Unlimited liability: cap liability at fees paid (12-24 months)
   |-- IP assignment: never assign IP; license it
   |-- Non-compete: limit scope to direct competitive products
   |-- Complete when: Red-flag list reviewed against proposed contract

3. PREPARE negotiation playbook
   |-- Champion's deck: ROI summary, internal selling points, competitor comparison
   |-- Concession plan: what you'll give (payment terms, training credits) vs hold (price, IP, liability)
   |-- BATNA: best alternative if deal fails. Never negotiate without one
   |-- Complete when: Champion deck, concession plan, and BATNA documented
```

Complete when: Key terms defined, red flags identified, negotiation playbook ready with BATNA.

### Phase 5: Procurement Compliance & Deal Desk (15%)

```
1. COMPILE security & compliance package
   |-- Required: SOC 2 Type II report, penetration test summary, DPA
   |-- Recommended: ISO 27001 certification, SIG Lite questionnaire, CAIQ
   |-- Insurance: cyber liability ($2M-$10M), E&O, general liability
   |-- Complete when: Compliance package assembled, gaps identified with remediation timeline

2. DESIGN deal desk workflow
   |-- CPQ integration: Salesforce CPQ or equivalent
   |-- Quote stages: discovery → config → pricing committee → approval → proposal → negotiate → close
   |-- SLAs: 24hr standard quote, 4hr strategic, 1hr must-win (deal desk, not approval)
   |-- Complete when: Deal desk workflow mapped with stage SLAs

3. SETUP supplier diversity & ESG compliance
   |-- Supplier diversity certification if applicable (WBENC, NMSDC)
   |-- ESG questionnaire: many enterprises require sustainability data
   |-- Complete when: Diversity cert status confirmed, ESG questionnaire prepared
```

Complete when: Compliance package ready, deal desk workflow active, supplier requirements addressed.

<!-- QUICK: 30s -->
## Decision Trees

### Tier Structure Decision

```
What's the enterprise buyer's primary need?
|-- Security & compliance (SSO, audit logs, SOC 2)
|   → Enterprise tier gates: SSO, audit logs, custom DPA, dedicated security contact
|-- Scale & performance (99.99% SLA, dedicated infra)
|   → Enterprise tier gates: 99.99% SLA with credits, dedicated tenant, priority support
|-- Customization & integration (API access, custom workflows)
|   → Enterprise tier gates: API access tier, custom integrations, solution architect
|-- Support & training (dedicated CSM, onboarding, SLAs)
|   → Enterprise tier gates: named CSM, 4hr response SLA, onboarding program
|-- All of the above
|   → Full enterprise package: combine all gates, price accordingly (top of value range)
```

### Discount Approval Path

```
Discount requested: [X]%
|-- X ≤ 10%
|   → AE authority. Document reason. No additional approvals.
|-- 10 < X ≤ 25%
|   → VP Sales approval. Business case: deal size, strategic value, competitive pressure.
|-- 25 < X ≤ 40%
|   → CFO approval. P&L analysis: margin impact, volume commitment, multi-year value.
|-- X > 40%
|   → CEO approval + board notification for deals >$500K ACV. Strategic rationale required.
```

### Contract Type Selection

```
Enterprise deal structure?
|-- Standard procurement (MSA + Order Form)
|   → Most common. MSA governs all terms, Order Form specifies products, pricing, term.
|-- Pilot/POC → Enterprise
|   → Pilot agreement with success criteria → auto-convert to enterprise if met. Lock pricing.
|-- Multi-product platform deal
|   → Master agreement + individual product schedules. Bundle discount for multi-product.
|-- Reseller/Channel deal
|   → Channel partner agreement + end-customer order form. Partner margin 15-30%.
|-- International deal
|   → Local entity contract (preferred) OR international MSA with local law addendum.
```

Complete when: Decision tree output maps to actionable next step with named owner and SLA.

## Error Recovery

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Deal stuck in procurement for 30+ days | Missing compliance docs: no SOC 2, no pen test | Pre-build compliance package before first enterprise deal. SOC 2 Type II takes 6-12 months | **Compliance before demand.** Procurement won't move without the package. Build it during beta, not after the first enterprise inquiry. |
| Enterprise customer churns after year 1 | Price-to-value gap: they paid but didn't realize the value | Implement QBR (quarterly business review) showing quantified value delivered. Renewal conversation starts day 1 | **Value communication is continuous.** The champion who bought needs ongoing ammunition to defend the renewal. |
| Competitor undercuts by 50% and wins | Your pricing was cost-based, theirs was value-based with aggressive anchor | Shift to value-based pricing. If competitor can undercut by 50%, you either have no value differentiation or your price is too high relative to value | **Cost-plus pricing loses to value-based.** The customer buys outcomes, not your costs. |
| Discount spiral: every deal demands 40%+ | No approval gates. AEs learned "every deal gets 40% off" | Implement approval matrix with hard gates. Track "discount given vs quota attainment" and coach outliers | **Discounts are a learned behavior.** Without gates, 40% becomes the new list price. Set the norm early. |
| International deal fails at legal review | No local entity. Couldn't contract in local currency/law | Set up international contracting infrastructure before entering markets: local entity OR international MSA with local counsel review | **International = legal complexity.** Budget 3-6 months lead time for new geo legal readiness. |
| Procurement demands MFN, you agree | Now every future deal references this MFN. All deals must match | Strike MFN clauses. If unavoidable, scope to: same product, same term length, same volume, same geo, within 12-month window | **MFN is a pricing virus.** It replicates into every future deal. Resist at all costs. |

## Error Decoder

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Enterprise pipeline full but close rate <5% | No ROI quantification. Champion can't defend the price internally | Build ROI calculator, train champions on internal selling. Price without value proof = indefinite procurement purgatory | **$500K-$2M in lost pipeline value.** Champions sell internally; arm them with CFO-ready numbers. |
| Discount approval taking 2+ weeks per deal | No approval matrix. Every deal escalates to CEO individually | Define thresholds with named approvers. 24hr SLA per stage. Deals stuck >48hr auto-escalate | **$100K-$500K in deal slippage.** Slow approvals kill deal momentum. Speed signals confidence. |
| Enterprise customers demanding SMB pricing | Your public pricing page shows SMB prices next to enterprise CTA | Remove enterprise from comparison table. Enterprise = "Contact Sales" with no price anchor visible. SMB pricing anchors enterprise down | **$200K-$1M/year in underpriced deals.** Price anchoring works both ways. Hide enterprise price. |
| New enterprise customer costs more to serve than revenue | No ACV floor. Signed a $10K "enterprise" deal that demands enterprise support | Set $25K-$50K ACV minimum. Below floor → point to self-serve with premium support add-on | **$50K-$200K per bad-fit deal in support costs + churn.** Not every company is an enterprise customer. |
| Win/loss analysis shows "price" as #1 loss reason | You haven't quantified value. "Price" is what prospects say when they don't see value | Shift from feature-sheet selling to ROI presentation. If you can't quantify value, you can't defend price | **$500K-$3M in avoidable losses.** "Too expensive" means "I don't see enough value." Fix the value story. |

## Gotchas

| Gotcha | Cost | Fix |
|--------|------|-----|
| Publishing enterprise pricing on your website anchors negotiations at that number. Every deal starts at the published price and discounts downward. "Contact Sales" for enterprise removes the anchor | $100K-$500K/year in lost ACV per enterprise deal | Enterprise tier = "Contact Sales." No price on website. Discovery call reveals budget before quoting |
| MFN (Most Favored Nation) clauses in enterprise contracts: one customer demands "best pricing we give anyone." If you agree, every future deal is constrained. Future investors/acquiring companies flag this | $500K-$2M in deal flexibility destroyed | Strike MFN in all contracts. If unavoidable, scope to: exact product, exact volume tier, 12-month window, same geo |
| Not verifying procurement compliance requirements before the deal reaches legal review. Missing SOC 2 or DPA adds 4-8 weeks to close. Deals die in procurement purgatory | $200K-$500K per delayed/dead deal | Pre-build compliance package. Maintain current SOC 2, pen test, DPA, insurance certs. Proactive > reactive |
| Pricing too low for enterprise — leaving millions on the table. First enterprise deals often underprice (excitement to close). That low price becomes the renewal anchor | $100K-$1M/year/account in underpricing | Enterprise minimum = 3x highest self-serve tier. Defend with value quantification. Raise prices annually (5-7% cap) |
| No price protection for multi-year deals — customer locked in at Year 1 price for 3 years while your costs rise 10-15%/year. Margin compression destroys deal economics | $100K-$300K in margin erosion per deal | Multi-year deals: price lock with 5-7% annual escalator built in. "Year 1: $100K, Year 2: $107K, Year 3: $114K" |
| Discounting to close the deal, then AE leaves. New AE inherits low-price account they can't raise. Customer expects perpetual discount | $200K-$500K in perpetually discounted revenue | Every discount: documented business justification. Discount tied to volume/term commitment, not AE relationship |

## Best Practices

1. **Start value-first, price-second.** Lead every enterprise conversation with quantified value. Price is what they pay; value is why they pay it.
2. **Build the compliance package before the first enterprise inquiry.** SOC 2 Type II takes 6-12 months. Start during beta.
3. **"Contact Sales" for enterprise tier.** Never publish enterprise pricing. Discovery reveals budget; you anchor from value, not a web page number.
4. **Every discount has a documented business case.** Volume commitment, multi-year term, strategic logo, competitive displacement. Never "the AE wanted to close."
5. **Annual upfront billing for all enterprise deals.** Monthly billing for enterprise = SMB economics with enterprise costs. Annual commit aligns incentives.
6. **QBRs (Quarterly Business Reviews) from day one.** Show value delivered every quarter. Renewal is not an event; it's a continuous conversation.
7. **Price-to-value ratio at 10-30%.** Below 10%: you're underpricing. Above 30%: customer questions net value. Stay in the zone.
8. **Multi-year deals with built-in escalators.** Lock commitment with 5-7% annual increase. Protects against cost inflation and sets renewal expectations.
9. **Deal desk SLAs are non-negotiable.** 24hr for standard quotes. Speed signals operational maturity to procurement teams.
10. **Never sign MFN clauses without C-suite approval.** One MFN contaminates your entire deal book. This is a board-level risk decision.

## Anti-Patterns

* ❌ Publishing enterprise pricing next to SMB pricing on your website — anchors enterprise buyers at SMB price points
* ❌ Offering enterprise features (SSO, audit logs) in mid-tier to "sweeten the deal" — removes the primary upgrade driver
* ❌ Negotiating price before value is established — you're arguing about cost, not outcomes. Value first, price second
* ❌ Discounting without tying to volume or term commitment — you give margin, they give nothing. Asymmetric concessions destroy margin
* ❌ Signing MFN clauses — permanently constrains all future pricing. This is the single most expensive contract term you can accept
* ❌ Skipping legal review of international contracts — local law defaults can override your MSA. Always local counsel review
* ❌ Treating every deal the same — a $500K strategic deal ≠ a $50K volume deal. Different approval paths, different concessions
* ❌ No QBR process — enterprise customers who don't see value churn at renewal. Value communication is the renewal strategy

## Proactive Triggers

| # | Trigger Condition | Auto-Response |
|---|------------------|---------------|
| P1 | Enterprise deal in pipeline > 60 days without close | [ALERT] Stalled deal. Check: missing compliance docs? No ROI deck? Champion left company? Escalate. |
| P2 | Discount > 25% on 2+ consecutive deals | [ALERT] Discount spiral. Audit: are AEs anchoring at list price? Or has discount become the new list? |
| P3 | Enterprise churn rate > 10% annually | [ALERT] Value delivery gap. Audit QBR cadence, customer health scores, and value realization metrics. |
| P4 | Win/loss analysis shows "price" as top-2 loss reason for 3+ months | [ALERT] Value communication failure. Price is what prospects say when they don't see value. Rebuild ROI narrative. |
| P5 | No enterprise deal > $100K ACV closed in 6+ months | [ALERT] Enterprise motion not working. Check: wrong ICP? No compliance package? Sales team can't sell value? |
| P6 | Average discount rate increasing month-over-month for 3+ months | [ALERT] Pricing discipline eroding. Tighten approval gates. Coach AEs on value selling. |

## Production Checklist

| # | Check | Status |
|---|-------|--------|
| CR1 | Enterprise tier defined with clear feature gates (SSO, audit, SLA, support) | ☐ |
| CR2 | Price anchors set: enterprise floor ≥ 3x highest self-serve tier | ☐ |
| CR3 | Discount approval matrix documented with named approvers per threshold | ☐ |
| CR4 | ROI calculator built with industry benchmarks and customer-specific inputs | ☐ |
| CR5 | Compliance package ready: SOC 2, pen test summary, DPA, insurance certs | ☐ |
| CR6 | Deal desk workflow mapped with stage SLAs and CPQ integration | ☐ |
| CR7 | Contract playbook: key terms, fallback positions, red-flag list | ☐ |
| CR8 | QBR template and cadence defined for all enterprise accounts | ☐ |
| CR9 | International pricing strategy: currencies, PPP, local entities/counsel | ☐ |
| CR10 | Win/loss analysis process in place with "price" decomposition | ☐ |
| CR11 | Supplier diversity certification status reviewed (WBENC, NMSDC) | ☐ |
| CR12 | Multi-year contract template with built-in escalators (5-7%) | ☐ |
| CR13 | ACV floor enforced: no enterprise deal below $25K-$50K/year | ☐ |
| CR14 | No MFN clauses in any active contracts (or CFO-approved exceptions only) | ☐ |
| CR15 | Enterprise pricing reviewed quarterly against competitor benchmarks | ☐ |

## Cross-Skill Coordination

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| **business-strategist** | Market sizing, competitive landscape, business model design | Before pricing architecture — validates enterprise segment is viable |
| **product-strategist** | Feature roadmap, product differentiation, value proposition | During tier design — defines what features gate enterprise tier |
| **sales-engineer** | Technical validation, POC architecture, integration complexity | During deal support — validates technical feasibility of enterprise commitments |
| **fp-and-a-analyst** | Margin analysis, P&L modeling, revenue forecasting | During discount approval — validates financial impact of proposed pricing |

### Decision Gates

| Gate | Condition | Action if Gate Fails |
|------|-----------|---------------------|
| G1: Enterprise Readiness | SOC 2 Type II report active and current | Halt enterprise sales until compliance package complete |
| G2: Value Quantified | ROI model with 3+ customer case studies or benchmarks | Do not publish enterprise pricing until value is defensible |
| G3: CAC Payback < 12 months | Enterprise CAC < 12 months of ACV | Restructure enterprise GTM: reduce sales cycles or raise price |
| G4: No MFN Contamination | Zero active MFN clauses (or CFO-approved only) | Remediate existing MFNs before new pricing architecture |

### Route to Other Skills

| Scenario | Route To |
|----------|----------|
| Designing the sales compensation plan for enterprise AEs | **revops-manager** |
| Building the enterprise onboarding and CSM program | **account-manager** |
| Creating the enterprise marketing and demand gen strategy | **demand-generation** |
| Designing the self-serve-to-enterprise upgrade path | **saas-monetization-strategist** |
| International tax, entity setup, and transfer pricing | **fp-and-a-analyst** |

## State Log

This skill maintains a **deal ledger** for enterprise pricing sessions.

1. On session start: check `.copilot/session-state/enterprise-deal-ledger.json` for active deals and pricing decisions.
2. After each pricing architecture decision: record tier structure, price points, approval thresholds.
3. Before completing work: verify all contract terms documented in the ledger.
4. On context recovery: read last 5 deal entries before proposing pricing changes.

## What Good Looks Like

### Before (Novice Enterprise Pricing)

```markdown
# Enterprise Plan
- All features included
- Priority support
- Custom pricing
- Contact sales
```

Problems: No feature differentiation, no value quantification, no approval process, no compliance awareness. This is a feature list, not a pricing strategy.

### After (Professional Enterprise Pricing)

```markdown
# Enterprise Plan — Starting at $75K/year
- Everything in Growth, plus: SSO/SAML, audit logs, 99.99% SLA
- Dedicated CSM with quarterly business reviews
- Custom integrations and API access
- SOC 2 Type II, ISO 27001, DPA included
- Annual upfront billing, 5% annual escalator
- Custom volume pricing for 500+ seats
- 24hr support SLA, named escalation contact
```

## Anti-Hallucination

* Admit uncertainty when pricing benchmarks are from memory — "My knowledge of competitor enterprise pricing may be stale. Verify against current G2/TrustRadius listings."
* Flag your knowledge cutoff — "Enterprise pricing norms shift with macro conditions. My training data may not reflect current market rates."
* Never guess security compliance requirements — "Compliance requirements are jurisdiction-specific. Verify with legal counsel before finalizing."
* Never fabricate customer logos or ROI data — "Use only verifiable, published case studies or customer-approved references."
* Mark unverified claims — "[VERIFIED]" tag with source and date for all pricing benchmarks and ROI data points. Example: "[VERIFIED: G2 Enterprise Grid, 2026-07]".

## Verification

* [ ] Enterprise tier feature gates are non-negotiable and not available in lower tiers
* [ ] Discount approval matrix has named roles at each threshold
* [ ] ROI model is defensible by customer's CFO using third-party benchmarks
* [ ] Compliance package (SOC 2, pen test, DPA) is current and accessible
* [ ] Deal desk SLAs are documented and enforced
* [ ] No MFN clauses in any active contract (or CFO-approved with scope limitations)
* [ ] ACV floor enforced — zero enterprise deals below minimum
* [ ] Multi-year contracts include built-in escalators (5-7% annual)

Complete when: All 8 verification checks pass, deal ledger updated, compliance package verified current.

## Deliberate Practice

### Level-Based Routines

**L1 (Apprentice — 30 min):** Take one existing enterprise deal. Apply the discount approval matrix. Was the right approval path followed? Document gaps.

**L2 (Practitioner — 1 hr):** Design the enterprise tier for a real or hypothetical B2B SaaS product. Build the feature matrix. Set price anchors. Identify compliance gaps.

**L3 (Expert — 2 hrs):** Build a full negotiation playbook for an upcoming enterprise deal. Champion's deck, concession plan, BATNA, red-flag review.

**L4 (Master — 4 hrs):** Competitive pricing analysis. Mystery-shop 3 competitors' enterprise pricing. Build a value gap analysis showing where your pricing wins/loses.

**L5 (Transformative — 1 day):** Design an enterprise pricing category standard. Publish thought leadership. Define pricing benchmarks for an industry vertical.

## References

* [pricing-architecture.md](references/pricing-architecture.md) — Tier design patterns, per-seat vs usage-based comparison, anchor pricing with worked examples
* [volume-discount-models.md](references/volume-discount-models.md) — Linear, tiered, and consumption discount curves with Excel-ready formulas
* [roi-calculators.md](references/roi-calculators.md) — Value quantification methodology, ROI calculator design, benchmark data sources
* [contract-negotiation.md](references/contract-negotiation.md) — Enterprise contract playbook, term-by-term negotiation guide, red flags
* [procurement-compliance.md](references/procurement-compliance.md) — Security review checklist, DPA requirements, insurance standards
* [deal-desk-operations.md](references/deal-desk-operations.md) — CPQ workflow, approval matrix design, quote-to-close metrics
* [gotchas.md](references/gotchas.md) — Extended failure patterns: 15 enterprise pricing disasters with case studies
* [checklist.md](references/checklist.md) — Per-deal verification checklist with stage gates
