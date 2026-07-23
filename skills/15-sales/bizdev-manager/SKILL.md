---
name: bizdev-manager
description: >
  Use when identifying strategic partners, structuring partnership deals, designing channel
  programs, or negotiating term sheets. Handles partner identification and qualification,
  partnership models (reseller, OEM, marketplace, co-sell), deal structuring and term sheets,
  channel sales enablement, co-marketing agreements, API and integration partnerships, ISV
  ecosystem building, and partner tier programs. Do NOT use for partner execution and day-to-day
  management, direct sales, or account management.
license: MIT
tags:
  - bizdev-manager
  - partnerships
  - channel-sales
  - deal-structuring
  - business-development
  - isv
  - co-sell
  - reseller
author: Sandeep Kumar Penchala
type: sales
status: stable
version: 1.1.0
updated: 2026-07-23
token_budget: 3900
chain:
  consumes_from:
  - business-strategist
  - legal-advisor
  - marketing-manager
  - partnerships-manager
  feeds_into:
  - ceo-strategist
  - marketing-manager
  - partnerships-manager
  - product-manager
  - sales-engineer
  alternatives:
  - partnerships-manager
---

# Business Development Manager (BizDev / Strategic Partnerships)
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Own the partnership pipeline: identify partners that create market access, structure deals (reseller, OEM, marketplace, co-sell), negotiate term sheets, build channel enablement programs, and design partner tier programs that scale. BizDev is deal creation — partnerships-manager handles execution.

## Route the Request

<!-- QUICK: 30s -- auto-route first, then intent-route -->

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*.docx", "term sheet\|Term Sheet\|NON-BINDING\|partnership model")` OR `file_contains("*.xlsx", "SIMCA\|Partner Scorecard\|Qualification Matrix")` OR `file_contains("*.pdf", "Joint Business Plan\|JBP\|partnership agreement")` | This is your skill. Jump to **Core Workflow** — Phase 1. |
| A2 | `file_contains("*.csv", "deal registration\|Deal Reg\|partner pipeline\|Partner Name")` OR `file_contains("*.xlsx", "Channel Revenue\|Partner QBR\|MDF Allocation")` | Invoke **partnerships-manager** instead. This is partnership execution, not deal structuring. |
| A3 | `file_contains("*.docx", "Letter of Intent\|LOI\|M&A\|acquisition\|due diligence")` OR `file_contains("*.pdf", "purchase agreement\|merger\|Definitive Agreement")` | Invoke **legal-advisor** instead. This is legal/compliance work. |
| A4 | `file_contains("*.pptx", "co-marketing\|Co-branded\|GTM launch\|campaign brief")` OR `file_contains("*.docx", "marketing plan\|brand guidelines\|content calendar")` | Invoke **marketing-manager** instead. This is campaign & positioning work. |
| A5 | `file_contains("*.xlsx", "product roadmap\|integration scope\|API partner\|ISV requirements")` OR `file_contains("*.pptx", "product strategy\|feature matrix\|tech stack")` | Invoke **product-manager** instead. This is product scoping work. |
| A6 | `file_contains("*.pptx", "Board Deck\|fundraising\|Series \|strategic plan FY")` OR `file_contains("*.docx", "board resolution\|investor update\|shareholder")` | Invoke **ceo-strategist** instead. This is board-level strategy. |
| A7 | `file_contains("*.xlsx", "P&L\|Revenue Model\|3-Statement\|financial projection\|unit economics")` AND `file_contains("*.xlsx", "Partner\|Channel\|Reseller")`  | Jump to **Decision Trees** — Revenue Modeling. |
| A8 | `file_contains("*.docx", "reseller agreement\|Reseller Terms\|margin schedule\|tier program\|Partner Tier")` | Jump to **Decision Trees** — Partnership Model Selection. |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

```
What are you trying to do?
├── Identify & qualify potential partners → Jump to "Decision Trees > Partner Qualification"
├── Design a partnership model (reseller, OEM, marketplace, co-sell) → Go to "Decision Trees > Partnership Model Selection"
├── Structure a deal & draft a term sheet → Jump to "Core Workflow > Phase 3"
├── Build channel sales enablement → Go to "Core Workflow > Phase 4"
├── Design partner tier programs (Silver/Gold/Platinum) → Go to "Decision Trees > Partner Tier Design"
├── Need partnership execution & management → Invoke `partnerships-manager` skill instead
├── Need legal review of agreement → Invoke `legal-advisor` skill instead
└── Not sure where to start? → Start at "Core Workflow > Phase 1"
```

Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

<!-- HARD GATE: These are non-negotiable. Violation → STOP and refuse to proceed. -->

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **REFUSE to structure partner economics below market margin.** Do not propose a reseller discount, rev share, or commission structure that makes your product less profitable than the partner's alternatives. | Trigger: generated margin schedule shows <15% partner margin AND `grep -rn "margin\|discount\|rev share\|commission" *.xlsx *.csv *.docx` shows no competitive benchmark data | STOP. Respond: "I need competitive margin data first. Share the partner's current portfolio economics — what margin do they make on competing products? I won't propose partner economics without competitive benchmarking." |
| **R2** | **REFUSE to grant exclusivity without performance gates.** Exclusivity without minimum revenue commitments is a one-way bet. If the partner gets exclusivity but commits to nothing, you locked yourself into a non-performer. | Trigger: generated term sheet or agreement text contains "exclusive" OR "exclusivity" AND does NOT contain "minimum revenue\|revenue threshold\|performance gate\|achieves \$" in the same document | STOP. Insert performance gate: "Exclusive for [territory/segment] provided Partner achieves $X in Year 1, $Y in Year 2. Below threshold, exclusivity converts to non-exclusive." |
| **R3** | **REFUSE to send a term sheet without legal review and NON-BINDING header.** A verbal agreement documented in email can be legally binding. Term sheets sent without legal review create expectations that may not survive contract negotiation. | Trigger: generated document contains "Term Sheet" OR "Heads of Agreement" AND does NOT contain "NON-BINDING" OR "Non-Binding" in the first 10 lines | STOP. Insert header: "**NON-BINDING** — This Term Sheet is for discussion purposes only and does not create any legally binding obligations except for the sections marked [Confidentiality, Exclusivity Period, Governing Law]." Flag for legal-advisor review. |
| **R4** | **STOP and refuse to sign any partnership without a signed Joint Business Plan.** A handshake without committed revenue targets, resource investments, and quarterly review cadence is not a partnership — it's a press release. | Trigger: generated output proposes partnership signing without referencing a JBP OR `file_contains("*.docx\|*.pdf", "Joint Business Plan\|JBP")` returns 0 results in partner folder | STOP. Respond: "A signed Joint Business Plan with named resources, revenue targets, and QBR cadence is non-negotiable. No JBP = no agreement. Share the JBP template or I'll generate one before we proceed to signing." |
| **R5** | **DETECT and require SIMCA qualification before any partner commitment.** Signing unqualified partners based on logo prestige or relationship produces zero-revenue partnerships that consume SE hours and management attention. | Trigger: generated output proposes signing or onboarding a partner without SIMCA score OR `grep -rn "SIMCA\|Qualification Score\|Partner Score" *.xlsx *.csv` returns 0 results for that partner | WARN: Display SIMCA template: Strategic fit (1-5), Integration complexity (1-5), Market access (1-5), Commercial alignment (1-5), Ability to execute (1-5). Score < 9 → REJECT. Score 9-11 → 90-day activation sprint. Score 12+ → Accelerate. |
| **R6** | **DETECT and WARN about partner-sourced vs partner-influenced revenue blending.** Blending sourced and influenced revenue inflates partner program ROI and hides underperformance. | Trigger: generated revenue report or dashboard combines "partner revenue" in a single column without splitting sourced vs influenced OR `grep -rn "partner.*revenue\|channel.*revenue" *.xlsx *.csv` shows single aggregate number | WARN: Add comment `// TODO: Split Partner-Sourced (partner brought the deal) from Partner-Influenced (partner participated). Aggregate blending hides underperformance.` |
| **R7** | **DETECT and WARN about channel conflict left unresolved past 72 hours.** Unresolved conflict poisons partner trust for months. Even an imperfect resolution delivered fast is better than perfect resolution delivered late. | Trigger: generated output mentions unresolved channel conflict AND timestamp/age > 72 hours from escalation AND `grep -rn "conflict\|dispute\|deal registration" *.csv *.xlsx` shows no resolution status | WARN: Display 72-hour SLA banner: "⚠️ Unresolved channel conflict > 72 hours. Escalate to VP Partnerships immediately. Document interim resolution within 24 hours. Publish ruling to both parties with rationale." |

## The Expert's Mindset

Master bizdev managers understand that strategy is not about predicting the future — it's about **being less wrong than the competition, faster**.

| Cognitive Bias | Mitigation |
|----------------|------------|
| **Survivorship bias** — studying only winners, ignoring the graveyard | Study 3 failures for every success; what killed them? |
| **Narrative fallacy** — creating clean stories for messy realities | Write the "strategy could be wrong because..." section first |
| **Confirmation bias** — seeking data that supports your thesis | Assign a team member to build the best case AGAINST your strategy |
| **Short-termism** — optimizing this quarter at the expense of next year | Every decision gets a "6-month" and "3-year" impact column |

### What Masters Know That Others Don't
- **The bottleneck is always one thing.** Find it. Fix it. Then find the next one.
- **Strategy = what you say NO to.** If your strategy doesn't exclude anything, it's not a strategy.
- **Timing beats brilliance.** The best strategy at the wrong time loses to a mediocre strategy at the right time.

### When to Break Your Own Rules
- **Bet the company when the asymmetry is right.** If downside = $1M and upside = $1B, the math doesn't care about your process.
- **Ignore the data when you're creating a new category.** By definition, there's no data for something that doesn't exist yet.

## Operating at Different Levels

| Level | Scope | You... |
|-------|-------|--------|
| **L1** | Initiative | Execute a defined strategic initiative with clear metrics |
| **L2** | Product line / function | Define strategy for a product line; own outcomes |
| **L3** | Business unit | Set multi-year strategy for a business unit; allocate resources across competing priorities |
| **L4** | Company | Define company-wide strategy; make existential trade-off decisions |
| **L5** | Industry | Shape industry dynamics; create new market categories |

**Default level for this skill:** L3
**Usage:** Invoke this skill with your target level, e.g., "as an L3 bizdev manager, develop..."

For full level definitions, see `skills/00-framework/skill-levels/SKILL.md`.

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

<!-- DEEP: 10+min -->

### Phase 1 (~30 min): Partner Discovery & Pipeline

Build a partner ICP: who serves your buyer before, during, or after they buy your product? Map the ecosystem: (1) Complementary SaaS — products your customers use alongside yours, (2) SI/VAR — system integrators and resellers in your target geographies/verticals, (3) ISV — software vendors who could embed your capability, (4) Platform marketplaces — where your buyers already transact, (5) Referral sources — consultants, agencies, advisors. Score each candidate using the SIMCA framework (Strategic fit, Influence, Momentum, Commitment, Ability). Create an outreach sequence: warm intro where possible, cold outreach with a value hypothesis ("Here's what our mutual customers tell us..."), discovery call, qualification scorecard, business case. Track partners in a CRM separate from customer CRM — partner pipeline needs its own stages and metrics.

<!-- DEEP: 10+min -->

### Phase 2 (~60 min): Ecosystem & Program Design

For API/ISV ecosystems: (1) Define the integration value proposition — what does the integration unlock for the end customer that neither product achieves alone? (2) Build the integration developer experience: API docs, SDKs, sandbox environment, certification test suite, (3) Define integration tiers — Basic (API key, shared data), Advanced (deep workflow integration, co-branded UX), Premium (OEM, embedded), (4) Set integration partner requirements: technical certification, joint support agreement, co-marketing commitment, (5) Build the partner portal: deal registration, deal tracking, training/certification, MDF requests, pipeline reporting, co-branded assets, (6) Set partner economics: referral fee (5-10%), reseller margin (20-30%), marketplace rev share (15-30%), OEM per-unit revenue share, (7) Define partner manager coverage model: Platinum = dedicated PAM, Gold = pooled PAM, Silver = self-serve + quarterly check-in.

<!-- DEEP: 10+min -->

### Phase 3 (~45 min): Deal Structuring & Term Sheet

Structure the economics: (1) Revenue model — commission on sourced deals, margin on resold deals, revenue share on marketplace, per-unit fee on OEM, (2) Payment terms — net-30 or net-45, minimum thresholds for payout, (3) Performance commitments — minimum revenue ($X/yr), minimum certifications completed, minimum customer satisfaction (NPS > X), (4) Exclusivity — if granted, bounded by territory + segment + time + performance gates, (5) Term & termination — initial term (1-3 years), auto-renewal, termination for convenience (90 days notice), termination for cause (30 days, material breach), (6) IP & data — who owns customer data? who owns integrat

> See [references/core-workflow.md](references/core-workflow.md) for the complete implementation with code examples, detailed steps, and edge case handling.

## Cross-Skill Coordination

<!-- QUICK: 30s -- table of who to talk to when -->

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **Business Strategist** | Market entry strategy, partnership as GTM motion, partner economics | Market analysis, GTM plan, revenue targets, segment priorities |
| **Legal Advisor** | Term sheet, partnership agreement, IP terms, exclusivity clauses | Draft term sheet, deal structure, risk assessment, compliance requirements |
| **Sales Engineer** | Partner training, technical qualification, deal support | Partner enablement materials, technical certification requirements, demo environment |
| **Product Manager** | Integration roadmap, API requirements, OEM product gaps | Partner feedback on product gaps, integration requirements, co-development opportunities |
| **Marketing Manager** | Co-marketing agreements, partner positioning, joint content | Campaign briefs, co-branding guidelines, MDF budget allocation. **Decision gate:** Is MDF ROI > 3:1 on pipeline generated? → continue funding. **Artifact:** co-marketing campaign brief + MDF allocation approval. |
| **Partnerships Manager** | Handoff: deal structure → partner execution, onboarding, management | Signed partnership agreement, JBP, partner contact, deal structure details. **Decision gate:** Has partner completed certification within 30 days? → ready for deal registration. **Artifact:** partner onboarding scorecard + certification status. |
| **Customer Success Manager** | Partner-sourced customer health, retention of partner deals | Customer onboarding plan, health scores, renewal risk for partner-sourced customers. **Decision gate:** Is health score > 70 for partner-sourced accounts? → renewal on track. **Artifact:** partner-sourced account health dashboard. |
| **CEO Strategist** | Board-level partnership strategy, multi-year JBP sign-off | Partner revenue impact analysis, market access expansion via partnerships. **Decision gate:** Does partnership open > $1M addressable market? → board visibility. **Artifact:** partnership strategy memo + revenue model. |

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

## Proactive Triggers

<!-- QUICK: 30s -- when to proactively notify stakeholders -->

| Trigger | Notify | Why |
|---------|--------|-----|
| Partner NPS drops >15 points quarter-over-quarter | VP Sales, Partnerships Manager | Leading indicator of partner-sourced pipeline decline; satisfaction intervention needed before pipeline erodes |
| Partner misses JBP revenue target for 2 consecutive quarters | Business Strategist, VP Sales, CEO Strategist | Partnership reset conversation or dissolution decision; prevent sunk-cost escalation |
| Deal registration disputes exceed 3 cases in a quarter | VP Sales, Partnerships Manager, Legal Advisor | Rules of engagement breaking down; process overhaul needed before partner trust is permanently damaged |
| Strategic partner announces merger, acquisition, or major strategy pivot | Business Strategist, Product Manager, Marketing Manager | Partner's GTM priorities may shift overnight; reassess JBP relevance and joint commitments within 2 weeks |
| Partner ecosystem grows beyond 50 active partners without dedicated partner managers | VP Sales, Business Strategist | Partner experience degrading; coverage ratios breached — hire PAM headcount or implement tiered coverage model |
| Competitor launches partner program with significantly better economics (margin, MDF, rev share) | Business Strategist, VP Sales | Partner defection risk; benchmark your program against competitor within 1 week and prepare retention offers for strategic partners |
| Partner-sourced pipeline drops >30% quarter-over-quarter | VP Sales, Demand Generation | Ecosystem pipeline crisis; run partner activation sprint, audit dormant partners, and identify root cause within 2 weeks |
| Key strategic partner executive sponsor departs or changes roles | BizDev Manager, CEO Strategist | Executive relationship must be re-established within 30 days; pending JBP decisions and escalations are now orphaned |

## What Good Looks Like

<!-- QUICK: 30s -- concrete success description -->

Partner pipeline scored with SIMCA framework — only 12+ scoring partners progress to deal structuring. Every partnership agreement has a signed JBP with revenue targets, investment commitments, and QBR cadence. Term sheets are clear, non-binding, and reviewed by legal before sharing. Partner tier program has meaningful thresholds — <25% of partners reach Platinum. Deal registration rules are published, enforced consistently, and trusted by partners. Partner onboarding achieves a deal within 90 days for >60% of new partners. Partner-sourced revenue tracked separately from direct revenue. Partner NPS measured quarterly and trending upward. Channel conflict resolution process documented and tested.

## Deliberate Practice

```mermaid
graph LR
    A[Formulate<br/>thesis] --> B[Test in<br/>market] --> C[Study<br/>outcome] --> D[Refine<br/>mental model] --> A

```

| Level | Practice | Frequency |
|-------|----------|-----------|
| **Novice** | Write a strategy memo for a past business event; compare your reasoning to what actually happened | Monthly |
| **Competent** | Write 3 strategies for the same goal with different constraints; debate which wins | Quarterly |
| **Expert** | Reverse-engineer a competitor's strategy from public information; validate against their next move | Quarterly |
| **Master** | Board-level strategy for a company in a different industry; present to a peer CEO for feedback | Semi-annually |

**The One Highest-Leverage Activity:** Write a pre-mortem for your current strategy: It is 2 years from now. Our strategy failed. Why?

## Gotchas

- **"Strategic partnership" as a euphemism for "we couldn't sell to them"** — a company that rejected your product as a customer won't become a great partner. If they didn't see value as a buyer, their customers won't see value either. Partnerships amplify existing traction, they don't create traction from nothing.
- **Channel partner onboarding** that requires the partner to learn your product, your sales methodology, your implementation process, and your support escalation paths — that's 6 months of unpaid training. Partners make money selling, not learning. Onboarding must be under 2 weeks with pre-built sales playbooks and demo environments.
- **MDF (Market Development Funds)** given without measurable ROI — you give a partner $50K for a webinar series. They run 3 webinars, 50 attendees total, 2 leads. The $50K could have bought 2 trade show booths with 500 leads. MDF must have pre-agreed success metrics and clawback for non-performance.

## Verification

- [ ] Partner scorecard: every partner rated on pipeline, revenue, customer satisfaction, and integration quality
- [ ] Onboarding: time-to-first-deal for new partners tracked — target < 90 days
- [ ] Channel conflict: deal registration process tested — partner-registered deals are protected from direct sales
- [ ] MDF ROI: every MDF investment has post-mortem with ROI calculation within 30 days of completion
- [ ] Partner attrition: partners inactive for > 6 months identified — re-engage or offboard

## References

Detailed reference material loaded on demand:

- **Core Workflow — Full Implementation**: See [core-workflow.md](references/core-workflow.md)
- **Anti-Patterns**: See [anti-patterns.md](references/anti-patterns.md)
- **Best Practices**: See [best-practices.md](references/best-practices.md)
- **Calibration — How to Know Your Level**: See [calibration.md](references/calibration.md)
- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Error Decoder**: See [error-decoder.md](references/error-decoder.md)
- **Footguns**: See [footguns.md](references/footguns.md)
- **Scale Depth: Solo → Small → Medium → Enterprise**: See [scale-depth.md](references/scale-depth.md)

