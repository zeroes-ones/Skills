---
name: bizdev-manager
description: "Business development & strategic partnerships: partner identification & qualification, partnership models (reseller, OEM, marketplace, co-sell), deal structuring & term sheets, channel sales enablement, co-marketing agreements, API/integration partnerships, ISV ecosystem building, partner tier programs (Silver/Gold/Platinum), joint business planning, partner-sourced revenue tracking."
author: Sandeep Kumar Penchala
type: sales
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - bizdev-manager
  - business-development
  - partnerships
token_budget: 3900
output:
  type: "code"
  path_hint: "./"
chain:
  consumes_from:
    - business-strategist
    - legal-advisor
  feeds_into:
    - sales-engineer
    - product-manager
  alternatives:
    - partnerships-manager
---
# Business Development Manager (BizDev / Strategic Partnerships)

Own the partnership pipeline: identify partners that create market access, structure deals (reseller, OEM, marketplace, co-sell), negotiate term sheets, build channel enablement programs, and design partner tier programs that scale. BizDev is deal creation — partnerships-manager handles execution.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->

```
What are you trying to do?
├── Identify & qualify potential partners → Jump to "Decision Trees > Partner Qualification"
├── Design a partnership model (reseller, OEM, marketplace, co-sell) → Go to "Decision Trees > Partnership Model Selection"
├── Structure a deal & draft a term sheet → Jump to "Core Workflow > Phase 3"
├── Build channel sales enablement → Go to "Core Workflow > Phase 4"
├── Negotiate a co-marketing agreement → Jump to "Core Workflow > Phase 5"
├── Design partner tier programs (Silver/Gold/Platinum) → Go to "Decision Trees > Partner Tier Design"
├── Build an ISV / API integration partner ecosystem → Jump to "Core Workflow > Phase 2: Ecosystem Design"
├── Create a joint business plan with a key partner → Go to "Core Workflow > Phase 6"
└── Not sure where to start? → Start at "Core Workflow > Phase 1"
```

Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces.

- **Never sign a partnership without a joint business plan.** A handshake and a press release is not a partnership — it's PR. If both sides haven't committed to revenue targets, resource investments, and quarterly reviews, the partnership will underperform and die quietly.
- **Always structure partner economics so the partner makes more money selling your product than any alternative.** If a reseller makes 20% margin on your product and 40% on a competitor's, you're not their priority — you're their backup. Partner margin must be competitive within their portfolio.
- **Never give exclusivity without performance gates.** Exclusivity without minimum revenue commitments is a one-way bet. Structure as: "Exclusive for [territory/segment] provided partner achieves $X in year 1, $Y in year 2. Below threshold, exclusivity converts to non-exclusive."
- **Always involve legal-advisor before sending a term sheet.** A verbal agreement documented in an email can be legally binding. Term sheets should have a clear "Non-Binding except for [Confidentiality, Exclusivity Period, Governing Law]" header.
- **Admit what you don't know about a partner's business.** Before structuring a deal, interview 3 of their existing partners. Ask: "What works? What doesn't? What would you have negotiated differently?"

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->

- Building a partner program from scratch — defining which partner types, tiers, and economics make sense
- Evaluating a specific partnership opportunity — is this a real deal or a meeting that goes nowhere?
- Structuring a channel partnership — reseller agreement, referral agreement, or OEM deal
- Negotiating partnership terms — revenue share, exclusivity, performance commitments, termination clauses
- Designing a partner tier program (Silver/Gold/Platinum) with clear progression criteria and benefits
- Building an ISV or API integration partner ecosystem — who to recruit, how to structure, how to enable
- Creating a joint business plan with a strategic partner — shared goals, investments, GTM plan
- Resolving a channel conflict — direct sales competing with a partner for the same deal

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->

### Partnership Model Selection

```
                              ┌──────────────────────────────┐
                              │ START: Which partnership      │
                              │ model fits?                   │
                              └────────────┬─────────────────┘
                                           │
                         ┌─────────────────▼─────────────────┐
                         │ Does the partner want to sell to   │
                         │ their customers or integrate your  │
                         │ product into theirs?               │
                         └────┬──────────────────────────────┘
                              │
                    ┌─────────▼──────────┐
                    │ SELL to customers  │
                    │ (Channel Partner)  │
                    └────┬───────────────┘
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
┌─────────────────┐ ┌──────────┐ ┌──────────────┐
│ Referral        │ │ Reseller │ │ Distributor  │
│ Partner         │ │          │ │ /VAD         │
├─────────────────┤ ├──────────┤ ├──────────────┤
│ • 5-10% of      │ │ • 20-30% │ │ • 10-15%     │
│   deal value    │ │   margin │ │   margin on  │
│ • Partner       │ │ • Partner│ │   deals they │
│   introduces    │ │   sells  │ │   fulfill    │
│ • You sell      │ │   +      │ │ • Handles    │
│   + close       │ │   manages│ │   logistics  │
│ • Low investment│ │   cust   │ │   & procurement│
│ • High volume   │ │ • Med-High│ │ • High volume│
│                 │ │   investment│ │   low-touch  │
└─────────────────┘ └──────────┘ └──────────────┘
```

```
                    ┌─────────▼──────────┐
                    │ INTEGRATE into     │
                    │ their product      │
                    │ (Tech/ISV Partner) │
                    └────┬───────────────┘
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
┌─────────────────┐ ┌──────────┐ ┌──────────────┐
│ OEM             │ │Marketplace│ │ Co-Sell      │
│ Partner         │ │Partner   │ │ Partner      │
├─────────────────┤ ├──────────┤ ├──────────────┤
│ • Partner       │ │ • You list│ │ • Joint GTM  │
│   embeds your   │ │   product │ │ • Both teams │
│   product (white│ │   on their│ │   sell       │
│   label/branded)│ │   platform│ │ • Shared     │
│ • Revenue share │ │ • Rev     │ │   pipeline   │
│   per unit/seat │ │   share  │ │ • Customer   │
│ • You lose      │ │   15-30% │ │   owns       │
│   brand (OEM)   │ │ • Your   │ │   relationship│
│ • High investment│ │   brand  │ │              │
│   (build +      │ │   visible│ │              │
│    support)     │ │ • Low-Med│ │              │
│                 │ │   invest │ │              │
└─────────────────┘ └──────────┘ └──────────────┘
```
**Referral Partner:** Low commitment, high volume. Use for: SMB consultants, agencies, complementary SaaS. Easy to recruit, hard to get consistent deal flow. Commission only.

**Reseller:** Mid-to-high commitment. Partner sells, prices, and manages customer. Use for: regional VARs, MSPs, system integrators. Requires training + enablement. 20-30% margin.

**OEM:** Highest commitment. Partner embeds your technology. Use for: large ISVs embedding your capability. Requires dedicated engineering + support. Revenue per-seat or per-unit.

**Marketplace:** Growing fast (AWS, Azure, GCP, Salesforce, Shopify). List where your buyers already buy. 15-30% rev share. Your brand stays visible.

**Co-Sell:** Joint sales motion. Both companies' sales teams collaborate. Use when: complementary products sold to the same buyer. Account mapping required.

### Partner Qualification Scorecard

```
Score each potential partner 0-3 on the following:

S - Strategic Fit (0-3)
    3 = Partner's strategy directly depends on what we provide
    2 = Good complement, not core to their business
    1 = Nice-to-have for them
    0 = No strategic alignment → "Partnership theater"

I - Influence / Reach (0-3)
    3 = Partner has 500+ target customers we can't easily reach alone
    2 = 100-500 target customers in relevant segment
    1 = <100 customers, narrow reach
    0 = No customer overlap → Wrong partner

M - Momentum (0-3)
    3 = Partner actively growing, hiring, winning in their market
    2 = Stable, established business
    1 = Declining or stagnant
    0 = Distressed → You'll carry the partnership

C - Commitment (0-3)
    3 = Executive sponsor identified, resources allocated, timeline committed
    2 = Interest expressed but no resources committed
    1 = "We should explore this" with no follow-up
    0 = Only responding because you asked → Walk away

A - Ability to Execute (0-3)
    3 = Partner has technical capability and sales capacity to sell/deliver today
    2 = Capability exists but needs investment (training, integration)
    1 = Significant gaps — 6+ months to enable
    0 = Cannot execute → You'd be building their capability
```

**Go/No-Go Threshold:** Score <9 → Decline. Score 9-11 → Low priority, revisit in 6 months. Score 12-14 → Engage, structured pilot. Score 15 → Full investment, fast-track.

### Partner Tier Design (Silver/Gold/Platinum)

```
                              ┌──────────────────────────────┐
                              │ START: Design tier program    │
                              └────────────┬─────────────────┘
                                           │
                         ┌─────────────────▼─────────────────┐
                         │ What behavior do you want to       │
                         │ incentivize?                       │
                         └────┬──────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
    ┌─────────────────┐ ┌──────────┐ ┌──────────────────┐
    │ Revenue Volume  │ │Capability│ │ Customer Success │
    │                 │ │/Training │ │ / Retention      │
    ├─────────────────┤ ├──────────┤ ├──────────────────┤
    │ Tier Up:        │ │Tier Up:  │ │Tier Up:          │
    │ $X in sourced   │ │Certified │ │ NPS >50,         │
    │ revenue/year    │ │staff     │ │ renewal >90%     │
    │                 │ │          │ │                  │
    │ Example Tiers:  │ │Example:  │ │Example:          │
    │ Silver: $100K/yr│ │Silver: 2 │ │Silver: 1 case    │
    │ Gold:   $500K/yr│ │certified │ │ study + ref call │
    │ Platinum: $1M/yr│ │Gold: 5   │ │Gold: 3 studies,  │
    │                 │ │certified │ │ quarterly review  │
    └─────────────────┘ │Platinum: │ └──────────────────┘
                       │10 cert. +│
                       │trainer    │
                       └──────────┘
```
**Tier benefits should escalate meaningfully:** Silver: deal registration, basic portal access, standard margin. Gold: higher margin (+5%), MDF access, dedicated partner manager, joint marketing. Platinum: highest margin, MDF priority, executive sponsorship, roadmap input, co-development opportunities.

**Anti-pattern:** Tiers that exist on paper but don't change partner behavior. If 80% of partners are Gold within 90 days, your tier thresholds are too low.

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->

### Phase 1 (~30 min): Partner Discovery & Pipeline

Build a partner ICP: who serves your buyer before, during, or after they buy your product? Map the ecosystem: (1) Complementary SaaS — products your customers use alongside yours, (2) SI/VAR — system integrators and resellers in your target geographies/verticals, (3) ISV — software vendors who could embed your capability, (4) Platform marketplaces — where your buyers already transact, (5) Referral sources — consultants, agencies, advisors. Score each candidate using the SIMCA framework (Strategic fit, Influence, Momentum, Commitment, Ability). Create an outreach sequence: warm intro where possible, cold outreach with a value hypothesis ("Here's what our mutual customers tell us..."), discovery call, qualification scorecard, business case. Track partners in a CRM separate from customer CRM — partner pipeline needs its own stages and metrics.

### Phase 2 (~60 min): Ecosystem & Program Design

For API/ISV ecosystems: (1) Define the integration value proposition — what does the integration unlock for the end customer that neither product achieves alone? (2) Build the integration developer experience: API docs, SDKs, sandbox environment, certification test suite, (3) Define integration tiers — Basic (API key, shared data), Advanced (deep workflow integration, co-branded UX), Premium (OEM, embedded), (4) Set integration partner requirements: technical certification, joint support agreement, co-marketing commitment, (5) Build the partner portal: deal registration, deal tracking, training/certification, MDF requests, pipeline reporting, co-branded assets, (6) Set partner economics: referral fee (5-10%), reseller margin (20-30%), marketplace rev share (15-30%), OEM per-unit revenue share, (7) Define partner manager coverage model: Platinum = dedicated PAM, Gold = pooled PAM, Silver = self-serve + quarterly check-in.

### Phase 3 (~45 min): Deal Structuring & Term Sheet

Structure the economics: (1) Revenue model — commission on sourced deals, margin on resold deals, revenue share on marketplace, per-unit fee on OEM, (2) Payment terms — net-30 or net-45, minimum thresholds for payout, (3) Performance commitments — minimum revenue ($X/yr), minimum certifications completed, minimum customer satisfaction (NPS > X), (4) Exclusivity — if granted, bounded by territory + segment + time + performance gates, (5) Term & termination — initial term (1-3 years), auto-renewal, termination for convenience (90 days notice), termination for cause (30 days, material breach), (6) IP & data — who owns customer data? who owns integration code? who owns co-developed IP? (7) Non-compete — restricted to the specific product category, bounded by time (typically 12 months post-termination). Draft the term sheet with a prominent "NON-BINDING" header. Send to legal-advisor for review before sharing externally. The term sheet covers economics + key terms — the full agreement comes after alignment.

### Phase 4 (~45 min): Channel Sales Enablement

Enablement determines whether a partner deal actually closes. Components: (1) Partner onboarding — 30-60-90 day plan: week 1-2 product training, week 3-4 sales training, week 5-8 shadow deals, week 9-12 first independent deal, (2) Training & certification — product certification (required annually), sales certification (required quarterly), technical certification for integration partners, (3) Sales toolkit — partner pitch deck, battle cards, discovery questions, demo script, pricing guide, deal registration guide, (4) Deal registration — partner registers a deal, gets protected margin + opportunity lock for 60-90 days. Rules: deal must be net-new to your pipeline, partner must be actively engaged, registration expires if no activity in 30 days, (5) Joint selling — partner-sourced deals get assigned a partner manager or overlay SE. Partner brings the relationship, you bring the product expertise.

### Phase 5 (~30 min): Co-Marketing Agreements

Co-marketing terms: (1) Joint value proposition — one sentence that explains why the combined offering is better, (2) Marketing commitments — what each party will do: content (case study, whitepaper, webinar), events (booth share, co-hosted dinner), digital (blog swap, social amplification, email to each other's lists), (3) Brand usage — logo placement, co-branding guidelines, press release approval rights, (4) Budget — who pays for what. Typical: each party covers their own costs. For premium partners: MDF allocated from your budget, (5) Lead sharing — how are jointly generated leads handled? Which CRM do they go into? Who follows up first? Define in writing, (6) Performance review — quarterly review of co-marketing activities: leads generated, pipeline created, deals closed. Adjust mix based on data.

### Phase 6 (~45 min): Joint Business Planning

The JBP is the annual operating plan for a strategic partnership. Structure: (1) Relationship overview — why this partnership exists, strategic importance to both parties, (2) Shared goals — 3-5 measurable objectives: revenue target, new customer target, product milestones, (3) GTM plan — target accounts, joint value proposition, sales plays, marketing activities, (4) Investment commitments — what each party is investing: headcount, marketing dollars, engineering resources, executive time, (5) Governance — executive sponsor on each side, quarterly business review (QBR) cadence, escalation path, (6) Success metrics — sourced revenue, influenced revenue, joint customers, partner NPS, time-to-first-deal, (7) Risk register — what could derail this partnership and what's the mitigation. Review the JBP quarterly — update targets, assess performance, adjust investments. If a partnership consistently misses JBP targets for 2 consecutive quarters, it's time for a reset conversation or dissolution.

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
<!-- DEEP: 10+min -- these rules encode years of failed partnerships, channel conflicts, and deal structures that unraveled -->

- Qualify partners as rigorously as you qualify customers. A bad partner costs more than a bad customer — they consume SE hours, support resources, and management attention for zero revenue.
- Partner margin must be competitive within their portfolio. Interview partners: "What's your average margin across your top 5 vendor relationships?" Beat it or don't expect deal flow.
- Exclusivity is a performance-based privilege, not a signing bonus. "Exclusive for 12 months provided $X in revenue by month 12. Below threshold, converts to non-exclusive." Period.
- Deal registration conflicts are the #1 partner relationship killer. Define clear rules: first-to-register wins OR partner-of-record wins. Whatever your rule, enforce it consistently. Favoritism destroys trust.
- Partner onboarding must produce a deal within 90 days. Partners with no deal in 90 days rarely produce one in 180. Build a 90-day activation metric and intervene before the window closes.
- Joint business plans without quarterly review are fiction. A JBP that sits in a drawer for 11 months is worthless. QBRs with both executive sponsors present are the accountability mechanism.
- Co-selling requires account mapping. Before launching a co-sell motion, map both companies' target account lists. Overlap is the addressable co-sell market. Prioritize the overlap accounts.
- Never recruit a partner purely for logo prestige. A Fortune 500 logo on your partner page that produces $0 in revenue is dead weight. Partners are measured by revenue, not press releases.
- Channel conflict is inevitable — plan for it. Define rules of engagement: when does direct sales engage vs. partner? What happens when both are working the same account? Write it down before it happens.
- Partner NPS is a leading indicator of partner-sourced revenue. Survey partners quarterly. If partner NPS drops, partner-sourced pipeline drops 6 months later. Fix satisfaction issues early.

## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **Business Strategist** | Market entry strategy, partnership as GTM motion, partner economics | Market analysis, GTM plan, revenue targets, segment priorities |
| **Legal Advisor** | Term sheet, partnership agreement, IP terms, exclusivity clauses | Draft term sheet, deal structure, risk assessment, compliance requirements |
| **Sales Engineer** | Partner training, technical qualification, deal support | Partner enablement materials, technical certification requirements, demo environment |
| **Product Manager** | Integration roadmap, API requirements, OEM product gaps | Partner feedback on product gaps, integration requirements, co-development opportunities |
| **Marketing Manager** | Co-marketing agreements, partner positioning, joint content | Campaign briefs, co-branding guidelines, MDF budget allocation |
| **Partnerships Manager** | Handoff: deal structure → partner execution, onboarding, management | Signed partnership agreement, JBP, partner contact, deal structure details |
| **Customer Success Manager** | Partner-sourced customer health, retention of partner deals | Customer onboarding plan, health scores, renewal risk for partner-sourced customers |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Strategic partnership agreement signed | CEO Strategist, Product Manager, Partnerships Manager, Marketing Manager | Press release, internal announcement, partner onboarding kickoff |
| Partner misses JBP revenue target for 2 consecutive quarters | Business Strategist, VP Sales | Partnership reset conversation or dissolution decision |
| Channel conflict (direct sales + partner on same deal) | VP Sales, Partnerships Manager | Rules of engagement enforcement; deal-level resolution |
| Partner requests exclusivity | Legal Advisor, Business Strategist, CEO Strategist | Strategic decision with long-term implications |
| Partner ecosystem >50 partners without dedicated partner managers | VP Sales, Business Strategist | Partner experience degrading; hire or automate |

### Escalation Path

```
Channel conflict >$100K deal at risk → VP Sales + Partner VP. Resolution within 48 hours.
Strategic partner threatening termination → CEO Strategist + VP Product. Executive retention conversation.
Exclusivity request with >$1M commitment → CEO Strategist + Legal Advisor + Board awareness.
Partner program economics change (margin, tier structure) → VP Sales + Business Strategist + Finance.
```

### Cross-skills Integration

```bash
# Chain: business-strategist → bizdev-manager → partnerships-manager → sales-engineer
# Partnership GTM: Strategist identifies market entry via partners → BizDev structures deals → Partnerships Manager onboards → SE enables

# Chain: bizdev-manager → legal-advisor → partnerships-manager
# Deal structure: BizDev drafts term sheet → Legal reviews → Partnerships Manager executes

# Chain: bizdev-manager → product-manager
# ISV ecosystem: BizDev identifies integration partners → PM prioritizes integration roadmap
```

## What Good Looks Like
<!-- QUICK: 30s -- concrete success description -->

Partner pipeline scored with SIMCA framework — only 12+ scoring partners progress to deal structuring. Every partnership agreement has a signed JBP with revenue targets, investment commitments, and QBR cadence. Term sheets are clear, non-binding, and reviewed by legal before sharing. Partner tier program has meaningful thresholds — <25% of partners reach Platinum. Deal registration rules are published, enforced consistently, and trusted by partners. Partner onboarding achieves a deal within 90 days for >60% of new partners. Partner-sourced revenue tracked separately from direct revenue. Partner NPS measured quarterly and trending upward. Channel conflict resolution process documented and tested.

## Error Decoder
<!-- DEEP: 10+min -- each row is a real partnership that failed to deliver or a deal that nearly blew up -->

| Problem | Root Cause | Fix |
|---------|------------|-----|
| 50 partners signed, <5 producing revenue | Recruited partners for logo count, not revenue potential. No activation program or deal review cadence. | Apply SIMCA qualification retroactively. Partners scoring <9 → offboard. Partners scoring 9-11 → 90-day activation sprint. If no deal in 90 days, move to dormant. Focus partner manager time on top 20% of partners. |
| Reseller promises big pipeline but delivers zero | Partner has no real commitment — no executive sponsor, no dedicated sales resource, no integration investment | Require a Joint Business Plan before signing. JBP must name: dedicated resources, target accounts, revenue commitment for Y1. No JBP = no agreement. |
| Term sheet negotiated verbally, then legal kills the deal | Term sheet shared without legal review. Verbal handshake created expectations legal can't fulfill. | Term sheet template with "NON-BINDING" header. Legal reviews every term sheet before external sharing. No exceptions. |
| Channel conflict: partner and direct rep both claim the same deal | No rules of engagement defined. Ad-hoc resolution creates perception of favoritism. | Publish deal registration rules: first-to-register wins, partner-of-record wins, or deal split rules. Automate in CRM. Review disputes in a weekly partner ops meeting with documented outcomes. |
| Partner signs then goes silent — no onboarding completion | Onboarding is self-serve PDFs with no human accountability. Partner doesn't know where to start. | Build a 30-60-90 day onboarding plan with a named partner manager. Week 1: kickoff call. Week 2: product training. Week 4: first deal review. Week 12: activation check. Partners inactive after 30 days get an executive outreach. |
| ISV partner built integration but no customers using it | Integration exists technically but no joint GTM. Partner doesn't know how to sell it, you don't promote it. | Joint GTM is part of the integration agreement: co-marketing launch, sales enablement for both teams, customer-facing listing in integration marketplace, quarterly pipeline review. |

### Error Decoder

| Problem | Root Cause | Fix |
|---------|------------|-----|
| Prospect goes dark after great demo | No clear next step with owner and timeline | Every demo must end with a specific next step: "If you agree X by Friday, I'll have the PoC ready by next Wednesday." No open-ended "let me know when you're ready." |
| Technical win, commercial loss | Sold to engineering champion who has no budget authority | Always identify the economic buyer by the second meeting. MEDDIC: find the Champion AND Economic Buyer before writing a PoC. Engineers love your product; budget holders love ROI — speak both languages. |
| RFP response rejected on pricing | Didn't uncover budget range before responding | Always ask: "Have you allocated a budget range for this initiative?" before writing a single page. If they won't share a range, the RFP is a price-discovery exercise — bid your standard price, not your best price. |
| POC runs 3 months, no deal | No timeline boundaries or exit criteria set upfront | POC agreement must include: duration (max 30 days), success criteria (3 measurable metrics), and a kill switch ("if criteria not met by day 25, POC ends"). Long POCs kill pipeline velocity. |
| Champion leaves mid-cycle | Only cultivated one internal advocate | Multi-thread from day one. Minimum 3 relationships per account: champion (wants your solution), economic buyer (controls budget), technical evaluator (validates feasibility). If one leaves, you still have coverage. |
| Competitive deal lost on a feature you actually have | Prospect didn't know your product had that capability | Build a competitive battlecard for every RFP. Map every competitor feature claim to your equivalent or better. Train your team quarterly — competitive positioning decays as products evolve. |
| Sales engineer over-engineering the POC | SE builds a production system instead of a proof-of-concept | POC scope: "works with your data, demonstrates the core value, can be thrown away." No custom integrations, no production-grade setup. If prospect asks for production, it's not a POC — it's a paid engagement. |


## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
<!-- DEEP: 10+min -- each item references a standard born from a partnership that went sideways -->

- [ ] **[S1]** Partner qualification scorecard (SIMCA) applied to every partnership evaluation
- [ ] **[S2]** Partnership model selected with clear rationale — referral, reseller, OEM, marketplace, or co-sell
- [ ] **[S3]** Term sheet template reviewed by legal, with "NON-BINDING" header, before any external sharing
- [ ] **[S4]** Every strategic partnership has a signed Joint Business Plan with revenue targets and QBR cadence
- [ ] **[S5]** Partner economics are competitive — margin, rev share, or commission benchmarked against partner's portfolio
- [ ] **[S6]** Deal registration rules documented, published to all partners, and enforced consistently
- [ ] **[S7]** Partner tier program has meaningful thresholds — revenue, certifications, or customer success metrics
- [ ] **[S8]** Partner onboarding plan (30-60-90) with activation metric (first deal within 90 days)
- [ ] **[S9]** Partner-sourced revenue tracked separately from direct revenue in CRM
- [ ] **[S10]** QBR cadence established for Gold/Platinum partners — quarterly reviews with executive sponsors
- [ ] **[S11]** Channel conflict resolution process documented — rules of engagement published to direct sales + partners
- [ ] **[S12]** Co-marketing agreements include budget allocation, lead sharing rules, and performance review cadence
- [ ] **[S13]** Partner NPS measured quarterly — trend tracked against partner-sourced pipeline
- [ ] **[S14]** Partner ecosystem map maintained — who partners with whom, gaps in coverage, competitive overlaps
- [ ] **[S15]** Offboarding process for non-performing partners — dormant partners inactive >12 months removed from program

## Scale Depth
<!-- QUICK: 30s -- how this skill changes as the company grows -->

| Stage | Scope | Focus | Key Difference |
|-------|-------|-------|----------------|
| **Solo** | Founder-led partnerships, ad-hoc deals | Land first partners, validate channel | CEO does BD; handshake deals; no formal program |
| **Startup** | First BD hire builds repeatable process, partner pipeline | Establish partner motion, first integration partnerships | Dedicated BD person; structured outreach; first tech partnerships live |
| **Scale-up** | Partner program with tiers, incentives, co-marketing | Scale through partners, build ecosystem playbook | Formal partner tiers (Silver/Gold/Platinum); partner portal; MDF budget |
| **Enterprise** | Channel ecosystem, global alliances, strategic partnerships | Market expansion through partners, enterprise deals | Global partner org; SI/GSI relationships; OEM/reseller channels; partner-sourced > 30% of revenue |

## References

- **business-strategist** — for market analysis, GTM strategy, TAM/SAM/SOM, and segment prioritization
- **legal-advisor** — for term sheet review, agreement drafting, IP terms, compliance, and risk assessment
- **partnerships-manager** — for partner execution, onboarding, enablement, and ongoing relationship management
- **sales-engineer** — for partner technical enablement, demo support, and deal-level technical qualification
- **product-manager** — for integration roadmap, API requirements, and OEM product gaps
- **marketing-manager** — for co-marketing agreements, partner positioning, and MDF allocation
- **customer-success-manager** — for partner-sourced customer onboarding and retention
- _Crossing the Chasm_ by Geoffrey Moore — for ecosystem strategy in market creation and expansion
- _Partnering with the Frenemy_ by Sandy Jap — for navigating co-opetition and partner dynamics
