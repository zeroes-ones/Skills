---
name: account-manager
description: "Account Manager: own the commercial relationship post-sale — account planning with stakeholder mapping, renewal management (timeline, negotiation, price justification), expansion selling (land-and-expand, upsell, cross-sell), executive sponsor programs, ROI documentation, account tier management, multi-threading, retention campaigns, renewal forecasting, and contract negotiation (MSA, SLA, security addenda). Use for account planning, renewal strategy, expansion deals, ROI business cases, negotiation prep. [KEYWORDS: account management, AM, renewal, expansion, upsell, cross-sell, contract negotiation, stakeholder mapping, account planning, executive sponsor]"
author: Sandeep Kumar Penchala
type: customer-success
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - account-manager
  - renewal-management
  - expansion-selling
  - contract-negotiation
  - stakeholder-mapping
token_budget: 3520
output:
  type: "document"
  path_hint: "./"
chain:
  consumes_from:
    - sales-engineer
    - customer-success-manager
    - customer-support-engineer
  feeds_into:
    - customer-success-manager
    - revops-manager
    - product-manager
---
# Account Manager

Own the commercial relationship: retain and expand revenue within existing accounts. Unlike the sales engineer (who wins new logos) and the CSM (who drives adoption and health), the Account Manager owns the renewal, the expansion, and the commercial negotiation. Your KPIs: Gross Revenue Retention (GRR), Net Revenue Retention (NRR) from expansion, renewal rate, and average contract value growth.

## Route the Request
<!-- QUICK: 30s -- auto-route first, then intent-route -->

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*.md\|*.docx", "account plan\|renewal strategy\|expansion pipeline\|stakeholder map\|QBR")` OR `file_contains("*.csv\|*.xlsx", "ACV\|NRR\|renewal date\|contract end\|procurement contact")` | This is your skill. Jump to **Core Workflow** — Phase 1. |
| A2 | `file_contains("*.pdf\|*.docx", "MSA\|SLA\|security addendum\|DPA\|terms of service")` | Invoke **legal-advisor** instead. This is contract review work — scoping legal terms, not account management. |
| A3 | `file_contains("*.csv", "ticket_id\|CSAT\|support_tier\|resolution_time")` AND `file_contains("*", "backlog\|SLA breach\|escalation")` | Invoke **customer-support-engineer** instead. This is support ticket pattern analysis. |
| A4 | `file_exists("salesforce_export.csv\|hubspot_export.csv\|crm_export.csv")` AND `file_contains("*.csv", "pipeline_stage\|deal_amount\|forecast_category")` | Invoke **revops-manager** instead. This is revenue operations pipeline work. |
| A5 | `file_contains("*", "product roadmap\|feature request\|user story\|sprint")` AND NOT `file_contains("*", "renewal\|expansion\|account plan")` | Invoke **product-manager** instead. This is product roadmap work. |
| A6 | `file_contains("*.csv\|*.xlsx", "health_score\|adoption_rate\|login_frequency\|NPS\|TTFV")` AND `file_contains("*", "churn\|onboarding\|QBR deck")` | Invoke **customer-success-manager** instead. This is CS health/engagement work. |
| A7 | `file_contains("*", "competitive\|displacement\|competitor_price\|switching cost\|win-loss")` | Jump to **Decision Trees** — Competitive Defense. |
| A8 | `file_contains("*", "multi-year\|annual escalator\|volume discount\|SLA tier\|price increase")` | Jump to **Decision Trees** — Renewal Strategy. |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:
```
What are you trying to do?
├── Build an account plan for a specific customer → Jump to "Core Workflow > Phase 1"
├── Prepare for a renewal negotiation → Go to "Decision Trees > Renewal Strategy" then "Core Workflow > Phase 2"
├── Identify and pursue an expansion opportunity → Jump to "Decision Trees > Expansion Strategy" then "Core Workflow > Phase 3"
├── Set up an executive sponsor program → Go to "Core Workflow > Phase 4"
├── Build an ROI business case → Jump to "Core Workflow > Phase 5"
├── Handle a competitive displacement threat → Go to "Decision Trees > Competitive Defense" then "Core Workflow > Phase 2"
├── Negotiate contract terms (MSA, SLA, security) → Jump to "Core Workflow > Phase 2" then "Cross-Skill Coordination" with legal-advisor
├── Structure a multi-year deal with price increases → Go to "Decision Trees > Renewal Strategy > Multi-Year"
├── Forecast renewals for the quarter → Start at "Core Workflow > Phase 2: Renewal Forecasting"
├── Need technical handoff / demo context → Invoke `sales-engineer` skill
├── Need customer support ticket patterns → Invoke `customer-support-engineer` skill
├── Need revenue analytics / NRR tracking → Invoke `revops-manager` skill
├── Need product roadmap for expansion → Invoke `product-manager` skill
└── Not sure? → Start at "Ground Rules" then "When to Use"
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else
<!-- HARD GATE: These are non-negotiable. Violation → STOP and refuse to proceed. -->

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **REFUSE to write a renewal proposal that leads with price before value.** Price-first renewals become commodity transactions. The customer answers "did we deliver what we promised?" before pricing is discussed. | Trigger: `grep -i "price\|discount\|rate increase"` present in renewal draft AND `grep -ic "value delivered\|ROI\|outcome\|saved\|reduced\|improved"` returns 0 | STOP. Respond: "I cannot draft a renewal proposal that opens with price. First, let me compile the value delivered over the contract term. Show me the account's value log, adoption data, and documented wins." |
| **R2** | **REFUSE to mark a deal as Commit without verified procurement engagement.** Gut-feel commit creates 30%+ forecast misses. | Trigger: Deal marked "Commit" AND `grep -ic "procurement\|purchasing\|buying center"` in contact map returns 0 | STOP. Respond: "This deal cannot be marked Commit. Rule R2: no procurement contact is documented. Please provide: procurement contact name, engagement date, and their stated process timeline." |
| **R3** | **REFUSE to draft a seat/module expansion pitch when current adoption is below 70%.** Expansion without adoption is a money grab. | Trigger: Output contains "expansion\|upsell\|add seats\|additional licenses" AND `grep -i "adoption rate\|usage\|active users"` shows <70% OR no data present | STOP. Respond: "Expansion is blocked by Rule R3. Current adoption data is missing or below 70%. Provide the adoption dashboard showing >70% active usage across the current seat base before I can build an expansion case." |
| **R4** | **REFUSE to justify a price increase with 'market rates' or 'our costs went up.'** Price increases must be justified by incremental value delivered, not cost-push. | Trigger: `grep -i "market rate\|industry standard\|cost increased\|inflation\|our costs"` in price increase justification section | STOP. Respond: "Price increase justification blocked by Rule R4. Replace market-rate/cost arguments with customer-specific incremental value: new features adopted, new use cases enabled, additional ROI generated since last renewal." |
| **R5** | **DETECT single-threaded accounts and STOP any renewal/expansion work until multi-threading is addressed.** One champion = one resignation away from churn. | Trigger: `grep -c "contact\|stakeholder\|relationship owner"` in account stakeholder map < 3 | STOP. Respond: "This account is single-threaded (Rule R5). < 3 active contacts detected. Before proceeding with renewal/expansion, multi-threading is required: identify economic buyer, executive sponsor, and power users. Escalate within 14 days." |
| **R6** | **REFUSE to produce an ROI business case using industry-average numbers without customer-specific data.** Finance teams reject generic assumptions instantly. | Trigger: `grep -i "industry average\|typical\|estimated\s+\$\|assumed"` in ROI model AND `grep -c "customer-provided\|source: customer\|confirmed by"` returns 0 | STOP. Respond: "ROI case blocked by Rule R6. All numbers must trace to customer-provided data or labeled adjustable assumptions. Replace industry averages with customer-specific metrics, or label every assumption with an adjustable cell reference." |
| **R7** | **STOP and flag if asserting facts about a customer's org structure without CRM verification.** Making claims about reorgs, new hires, or budget without source data. | Trigger: Output contains "VP of\|C-suite\|new hire\|recently promoted\|budget approved" AND `grep -ic "CRM\|verified\|confirmed with\|last updated"` returns 0 | STOP. Respond: "I cannot assert this about the customer's org without verification (Rule R7). I need: the CRM record showing this information, the last contact date confirming it, or I will flag this as unverified and request validation." |


## The Expert's Mindset

Master account managers know that operational excellence is invisible when it works — and catastrophically visible when it doesn't. They design for the 99th percentile, not the average.

| Cognitive Bias | Mitigation |
|----------------|------------|
| **Availability heuristic** — over-prioritizing the last incident | Rank problems by recurrence × impact, not recency |
| **Hero complex** — being the person who always saves the day | If you're always the hero, your system is fragile. Automate your heroism. |
| **Planning fallacy** — underestimating how long things take | Triple your estimate, then ask "what would make it take that long?" — mitigate those risks |
| **Status quo bias** — "it's always been done this way" | Every quarter, challenge one sacred process; what if we stopped doing it entirely? |

### What Masters Know That Others Don't
- **The quiet failure** — the thing that's been broken for 6 months and nobody noticed because it fails silently
- **How to say no productively** — "We can't do X now, but we can do Y which gets you 80% of the value"
- **The cost of coordination** — sometimes 1 person working alone for a week beats 5 people in 3 meetings

### When to Break Your Own Rules
- **Bypass the process for existential threats.** If the site is down, fix it first; process comes after.
- **Over-communicate during ambiguity.** When the path is unclear, silence is worse than wrong information.
## Operating at Different Levels

| Level | Scope | You... |
|-------|-------|--------|
| **L1** | Single process | Execute defined workflows reliably and flag deviations |
| **L2** | Team process | Own team-level processes; optimize for team efficiency; remove bottlenecks |
| **L3** | Department operations | Design cross-team operational workflows; make build-vs-automate decisions |
| **L4** | Org operations | Define operational strategy for the organization; set standards and tooling |
| **L5** | Industry operations | Create operational frameworks adopted across the industry |

**Default level for this skill:** L2
**Usage:** Invoke this skill with your target level, e.g., "as an L3 account manager, manage..."

For full level definitions, see `skills/00-framework/skill-levels/SKILL.md`.

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- A customer renewal is 120 days out and you need a structured renewal strategy with timeline and negotiation plan
- An existing account shows expansion potential — new department, new use case, seat growth, or module cross-sell
- You need to build an account plan with stakeholder map, org chart, political landscape, and whitespace analysis
- A competitor is actively trying to displace your product and you need a defense strategy
- You are preparing a price increase for renewal and need the business case to justify it
- A multi-year contract negotiation requires structuring — annual escalators, volume discounts, SLA tiers
- You need to launch or refresh an executive sponsor program for your top 20 accounts
- The quarterly renewal forecast needs to be built with objective commit categories and risk assessment
- A customer asks for MSA amendments, custom SLA terms, or security addenda and you need to scope the ask
- You are transitioning from a land-and-expand motion to a broader enterprise deployment

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->

### Renewal Strategy Selection
```
When is the renewal date?
├── > 180 days out → Early stage. Focus: value delivery tracking, executive alignment.
│     Action: start value log. Document every win, metric improvement, and success story.
│     Identify renewal risk factors now (champion stability, budget cycle, competitor presence).
├── 90-180 days out → Preparation. Focus: stakeholder validation, ROI documentation, pricing strategy.
│     Action: present draft ROI analysis to champion. Confirm budget allocation for next year.
│     Begin multi-threading into procurement, legal, and executive sponsor.
├── 30-90 days out → Active negotiation. Focus: proposal delivery, objection handling, terms.
│     Action: formal proposal sent. Weekly check-ins. Legal review initiated if terms changing.
└── < 30 days out → Critical. Focus: close, escalation if stalled.
      Action: executive-to-executive call. Final offer. Escalate to VP/CRO if blocked.

What is the account health? (from customer-success-manager)
├── Healthy (score 80-100) → Standard renewal + expansion pitch. Multi-year with escalator.
│     Price increase: 5-8% justified by new value delivered. Target: multi-year lock.
├── At-Risk (score 50-79) → Flat renewal or modest increase (0-3%). Focus on value reinforcement.
│     Do not pitch expansion. Stabilize first.
├── Critical (score 20-49) → Flat renewal or small concession. Executive engagement required.
│     Save offer prepared. Do not push multi-year unless customer requests it.
└── Terminal (score 0-19) → Last resort save. CEO involvement. Concession-heavy offer.
      Accept that you may lose the account. Plan for structured offboarding.

Multi-year deal structure?
├── 1-year → Standard terms. 5-8% increase. Annual negotiation. Good for at-risk accounts.
├── 2-year → 3-5% annual escalator. 5-10% discount vs 2 single-year deals. Good for stable accounts.
├── 3-year → 2-4% annual escalator. 10-15% discount vs 3 single-year deals. Lock-in for strategic accounts.
│     Requires: mutual exit clauses, SLA guarantees, price protection against product sunset.
└── 5+ year → Rare in SaaS. Only for deeply embedded, on-premise hybrid deployments.
      Requires: business review clauses, technology refresh provisions, inflation adjustment caps.
```

### Expansion Strategy Selection
```
What type of expansion?
├── Seat growth within existing department → Land-and-expand.
│     Trigger: license utilization >85% for 2+ months.
│     Pitch: volume discount tier. "Moving from 50 to 75 seats reduces per-seat cost by 15%."
│     Required: current user adoption >80%, NPS >30, no active support escalations.
├── New department / business unit → Cross-department expansion.
│     Trigger: inbound inquiry from new team, or you identify adjacent use case.
│     Approach: new stakeholder discovery. Treat as mini new-logo sale within existing account.
│     Required: executive sponsor introduction to new department head. ROI case for their use case.
├── Module / product upsell → Feature expansion.
│     Trigger: power users hitting paywall on premium features, customer requests capability.
│     Pitch: "Based on your team's usage of [related feature], [premium module] would save [X] hours/week."
│     Required: adoption data proving they've mastered the core product first.
├── Cross-sell adjacent product → Portfolio expansion.
│     Trigger: customer's use case naturally extends to second product (identified via multi-product analysis).
│     Pitch: bundle discount. "Customers using both products see 40% higher ROI than single-product."
│     Required: product-manager validation that integration is production-grade, not roadmap-only.
└── Usage-based growth → Consumption expansion.
      Trigger: API calls or data volume exceeding 80% of plan limit for 2 consecutive months.
      Pitch: automatic upgrade path with overage protection. "Your growth is exceeding your plan — here's the right tier."
      Required: proactive — reach out BEFORE they hit the limit and get throttled.
```

### Competitive Defense Strategy
```
Which competitor is threatening?
├── Lower-price competitor → Defend on value, not price.
│     Quantify: total cost of ownership (migration cost, retraining, lost productivity during switch).
│     Show: your product's differentiated capabilities they'd lose. "Yes, competitor X is 30% cheaper,
│     but they lack [specific feature] which your team uses daily — migrating would cost $Y in lost productivity."
├── Feature-parity competitor → Defend on relationship, integration depth, and roadmap.
│     Show: your product's integration with their stack (SSO, data pipeline, existing workflows).
│     Commit: roadmap item they need, with named quarter. "Feature Z is on our Q3 roadmap — here's the beta access."
├── Incumbent / legacy competitor → Defend on innovation velocity and modern architecture.
│     Show: release cadence comparison, API-first design, ecosystem integrations.
│     Position: "You're comparing a 2024 platform to a 2012 platform. Here's what you'd give up."
└── Internal build threat → Defend on TCO and time-to-value.
      Show: cost to build + maintain + evolve vs your annual subscription.
      "Building this internally would require 3 engineers × 9 months = $450K, plus $150K/year maintenance.
      Our platform costs $120K/year and you get it today."
```

**What good looks like:** Account plan with 10+ named stakeholders mapped. Renewal forecast with commit/upside/pipeline categories and objective criteria per stage. Every expansion pitch grounded in adoption data. ROI document with customer-specific metrics and ROI > 300% over 3 years.

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->

<!-- DEEP: 10+min -->

### Phase 1 (~40 min): Account Planning
<!-- STANDARD: 3min -->
Build a comprehensive account plan for each strategic account. **Account Plan Structure:**
1. **Account Summary** — Industry, size, ACV, contract end date, products owned, health score
2. **Stakeholder Map** — Org chart with:
   - Economic Buyer (budget authority) — name, title, relationship strength (1-5), last contact
   - Champion (product advocate) — name, title, relationship strength, influence score
   - Executive Sponsor (your internal exec mapped to their exec) — paired relationship
   - Influencers (3-5 power users) — names, departments, usage patterns
   - Detractors (known blockers) — name, concern, mitigation strategy
   - Procurement/Legal contacts — names, known preferences (standard terms, redline tendencies)
3. **Political Landscape** — Recent reorgs, leadership changes, M&A activity, budget cycle timing, strategic initiatives your product supports
4. **Whitespace Analysis** — What don't they own? Map all products/modules to departments. Identify: departments with no adoption, products not owned, use cases not addressed
5. **Relationship Health** — At least 3 active relationships. No single point of failure. Last contact dates for all named contacts. Executive sponsor interaction log.
6. **Risk Register** — Champion departure risk, budget cut risk, competitor presence, M&A risk, regulatory change risk. Each with probability (H/M/L) and mitigation.
7. **Growth Plan** — Expansion targets (seats, modules, products, departments), timeline, revenue potential, required proof points
<!-- DEEP: 10+min -->
**War story:** An AM lost a $500K account because the champion — their only contact — left for a competitor. The new VP arrived, had a pre-existing relationship with a competitor's sales team, and switched within 60 days. The AM had never met anyone else at the account in 3 years. Fix: minimum multi-threading standard — 3 named contacts with relationship score ≥3, each contacted within the last 30 days. Run a "single-point-of-failure audit" on every account >$50K ACV quarterly. Any account with only 1 active contact is automatically flagged as at-risk.

<!-- DEEP: 10+min -->

### Phase 2 (~35 min): Renewal Management
<!-- STANDARD: 3min -->
**Renewal Timeline (120-day cycle):**
- **Day 120-90:** Internal prep. Review account plan, health score, adoption data, support history. Compile value log. Draft ROI analysis. Identify risks. Set pricing strategy.
- **Day 90-60:** Value delivery review with customer. Present ROI analysis to champion. Socialize value delivered. Identify gaps. Align on next year's objectives.
- **Day 60-30:** Formal proposal. Send renewal proposal with pricing, terms, and value justification. Address objections. Begin legal/procurement engagement if terms changing.
- **Day 30-0:** Close. Executive-to-executive call if needed. Final negotiation. Contract signed.

**Pricing Strategy by Scenario:**

| Scenario | Price Change | Justification | Risk |
|----------|-------------|---------------|------|
| Strong adoption + NPS >50 + multi-product | +8-12% | New features adopted, usage growth >30%, multi-product expansion | Low |
| Good adoption + NPS 20-50 + stable usage | +5-8% | Standard annual increase, modest new value delivered | Low-Med |
| Flat adoption + NPS 0-20 + no expansion | 0-3% | Value maintenance, inflation adjustment | Medium |
| Declining adoption + NPS <0 + at-risk | 0% or concession | Stabilization priority, save offer if needed | High |
| Competitive threat active | Competitive pricing | Match or slightly undercut with value differentiation | Critical |

**Price Increase Justification Formula:** "Since your last renewal, you've adopted [X new features], expanded usage by [Y%], and achieved [Z specific business outcome]. The [N]% increase reflects the additional value delivered and ongoing investment in [relevant roadmap area]."
<!-- DEEP: 10+min -->
**War story:** An AM secured a 3-year deal with 7% annual escalators. In year 2, the customer's budget was cut 20% company-wide. The AM had no mutual exit clause — the customer was locked in at a price they couldn't afford, breeding resentment that poisoned the relationship for 3 years. Fix: multi-year deals should include annual business review clauses with mutual opt-out if either party's circumstances change materially. Lock-in creates hostages, not customers.

<!-- DEEP: 10+min -->

### Phase 3 (~30 min): Expansion Selling
<!-- STANDARD: 3min -->
**Land-and-Expand Playbook:**
1. **Qualify:** License utilization >85% for 2+ months. Adoption rate >80%. NPS >30. No open SEV1/SEV2 support tickets. Health score >70.
2. **Identify trigger:** Customer mentions "we're rolling out to [new team]," job postings in relevant departments, inbound license requests from new users, usage bump above plan limits.
3. **Build business case:** "Adding 25 seats at tier 2 pricing reduces your per-seat cost by 15% while enabling [new department/Rollout] to achieve [their objective]."
4. **Pitch to champion first:** Socialize the expansion logic with your champion before involving procurement. Get their endorsement. Have them present to the economic buyer.
5. **Close:** Simple amendment to existing MSA. No new procurement cycle if within same legal entity. Target: close within 30 days of pitch.

**Module Upsell Playbook:**
1. **Identify power users:** Who's hitting paywalls on premium features? Run feature-flag telemetry report monthly.
2. **Quantify current behavior:** "Your team has attempted to use [premium feature] 47 times this month. Each time, they hit the paywall. Here's what they're trying to accomplish and how the premium module enables it."
3. **Demo with their data:** Never demo with sample data. Show the premium module working with their actual workflows.
4. **ROI case:** "Power users save 5 hours/week with [premium feature]. At 10 power users × $75/hour × 50 weeks = $187,500 annual productivity gain vs $24,000 module cost. 7.8x ROI."
<!-- DEEP: 10+min -->
**Cross-sell by correlation:** Analyze your multi-product customer base. Which product pairs have the highest co-adoption? Customers who buy Product A + Product B have 40% higher NPS and 25% lower churn than single-product customers. Build your cross-sell pitch around this data: "Customers like you who added [Product B] saw [specific outcome improvement]. Based on your [use case], here's the projected impact."

<!-- DEEP: 10+min -->

### Phase 4 (~20 min): Executive Sponsor Program
<!-- STANDARD: 3min -->
Pair each strategic account (>$100K ACV) with an internal executive sponsor (VP or above). **Executive Sponsor Charter:**
- **Cadence:** Quarterly 30-minute call with customer's executive counterpart. Not a sales call — a peer relationship call.
- **Agenda:** Industry trends (50%), customer's strategic initiatives (30%), product roadmap alignment (20%). No pricing, no support issues, no tactical product questions.
- **Accountability:** Sponsor is accountable for the relationship health, not the renewal (that's the AM's job). Sponsor opens doors; AM closes deals.
- **Selection:** Match by industry, functional area, or personal connection. The VP of Engineering sponsors engineering leaders. The CTO sponsors CTOs. Never pair a marketing VP with a CFO — peer relationship requires peer relevance.
- **Handoff protocol:** AM briefs sponsor 48h before call with: account summary, current health score, top 3 opportunities, top 3 risks, customer's personal interests (conference they spoke at, recent promotion, company news).

**Executive Sponsor Scorecard (quarterly):** Number of executive interactions, relationship strength score (1-5, rated by sponsor), customer satisfaction with program, renewals with sponsor involvement vs without (track differential).
<!-- DEEP: 10+min -->
**War story:** An executive sponsor program failed at scale because sponsors were assigned but never briefed. A CRO showed up to a quarterly call and asked "so, what do you do?" to a customer they'd supposedly been sponsoring for 6 months. The customer's CEO was insulted and the account went to competitor within 90 days. Fix: sponsor assignment includes mandatory 30-minute onboarding with the AM. No sponsor call happens without a written brief delivered 48h in advance. Track sponsor engagement; reassign after 2 missed quarters.

<!-- DEEP: 10+min -->

### Phase 5 (~25 min): ROI Documentation & Business Case Construction
<!-- STANDARD: 3min -->
**ROI Business Case Template:**
1. **Executive Summary** — 3-sentence summary: investment, return, payback period
2. **Current State Costs** — What are they spending today (people, tools, time) to solve this problem without your product? Quantify: hours/week × fully loaded cost/hour × 50 weeks. "Your team spends 120 hours/month on manual reporting. At $75/hour fully loaded, that's $108,000/year in labor cost alone."
3. **Your Solution Investment** — Annual subscription + implementation + training + ongoing admin. "Total first-year investment: $85,000. Annual recurring: $72,000."
4. **Quantified Benefits** — Hard savings (reduced headcount, eliminated tools, reduced errors), soft savings (faster time-to-decision, improved employee satisfaction), revenue impact (faster time-to-market, increased conversion). Each with source: "Based on your team's current reporting cycle (per our discovery call with [Name] on [Date])..."
5. **ROI Calculation** — Total 3-year benefits / Total 3-year costs. Target: ROI > 300% over 3 years. Payback period < 12 months.
6. **Risk-Adjusted ROI** — Apply confidence discount: High confidence = 90%, Medium = 70%, Low = 50%. Present both optimistic and conservative scenarios.
7. **Appendix** — Data sources, assumptions, customer quotes that support the analysis
<!-- DEEP: 10+min -->
**War story:** An AM built a flawless ROI model showing 500% return. The customer's CFO rejected it. Why? The AM used "industry average" salary data ($150K/engineer) instead of the customer's actual fully loaded cost ($220K/engineer including benefits, office, equipment). The CFO spotted the discrepancy immediately and distrusted the entire analysis. Fix: every number in the ROI model must trace to one of: (a) data the customer provided directly, (b) data from the customer's public financial filings, or (c) explicitly stated assumptions with the source. "We assumed $75/hour based on [Role] median salary from [Bureau of Labor Statistics / Glassdoor / your team's input]. Please adjust if your actual cost differs."

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Start renewal conversations at 120 days, not 30.** Early renewal discussions are about value delivered. Late renewal discussions are about price — and price-only conversations are races to the bottom.
- **Document every customer win in a shared value log.** Every time the customer achieves something with your product — faster report, fewer errors, new capability — log it with date, metric, and customer quote. This is your renewal justification file. Without it, you're negotiating from memory.
- **The economic buyer and the champion are rarely the same person.** The champion loves your product. The economic buyer signs the check. Map both. Maintain relationships with both. If you only know the champion, you don't know if budget exists for renewal.
- **Never present a price increase without first presenting the value increase that justifies it.** The sequence is fixed: (1) Here's what you achieved with our product, (2) Here's what's new since your last renewal, (3) Here's the renewed investment. If step 1 and 2 are weak, skip step 3 until they're strong.
- **Multi-thread at least 3 contacts per account, contacted within 30 days.** Relationship depth, not just breadth. A contact you emailed once 6 months ago doesn't count. Track relationship health: green = responded in last 30 days, yellow = 30-60 days, red = >60 days or never responded.
- **Expansion pitches must cite the customer's own usage data.** "Based on your team's adoption data, 87% of your licensed users are active weekly. Your power users in the engineering org have attempted to access [premium feature] 47 times this month." Generic expansion pitches ("you should buy more") lose to data-driven ones every time.
- **Forecast using commit categories with objective criteria, not gut feel.** Commit = procurement contact confirmed + budget verified + timeline agreed. Upside = verbal yes but no procurement engagement. Pipeline = positive signals only. Never mix them.
- **Competitive displacement defense must include migration cost quantification.** The cheapest competitor wins on price alone. You win on: "switching will cost you $X in migration, $Y in retraining, and $Z in lost productivity during the 6-month transition." Most customers underestimate switching costs by 3-5x — quantify it for them.
- **Executive sponsor relationships must be peer-to-peer.** A VP-level sponsor paired with a Director-level customer contact creates an awkward power dynamic. Match levels intentionally. VP to VP. C-level to C-level.
- **Every account plan includes a "who could kill this deal" section.** Identify the one person (not your champion) who could veto the renewal — the new CFO cutting costs, the incoming VP with a competitor relationship, the procurement lead who hates your standard terms. Document your mitigation strategy for each.

## Anti-Patterns
<!-- DEEP: 5min -- each anti-pattern includes machine-detectable patterns -->

| ❌ Anti-Pattern | ✅ Do This Instead | 🔍 Detect (grep / lint) | 🛡️ Auto-Prevent |
|-----------------|---------------------|--------------------------|-------------------|
| Waiting until the last 30 days to start renewal conversations | Start renewal cycle at 120 days: Phase 1 (120-90) internal prep, Phase 2 (90-60) value review with champion, Phase 3 (60-30) proposal, Phase 4 (30-0) close and procurement | `grep -i "renewal\|contract end" renewal_tracker.csv \| awk -F',' '{if ($2 < date + 30) print}'` → flag any renewal <30 days without documented value log | Auto-check: before any renewal proposal is generated, validate `days_until_renewal >= 90` AND `value_log_entries > 0`. Block if either fails. |
| Leading expansion pitches with product features instead of customer business problems | Identify the customer's unsolved problem your expansion solves. Lead with: "Your EMEA team is still on spreadsheets — here's what rolling out licenses would unlock." | `grep -c "feature\|module\|capability\|product\s+can"` in expansion pitch > `grep -c "your\s+team\|your\s+business\|your\s+problem\|you\s+need"` → self-serving pitch detected | Auto-rewrite: require the first paragraph to contain a customer problem statement. Validate `grep -c "your (team\|business\|problem\|need)"` > 0 before output. |
| Using industry-average ROI numbers instead of customer-specific data | Every number traces to customer-provided data or a labeled adjustable assumption: "Your actual cost may differ — adjust cell B12." | `grep -i "industry average\|typical\|estimated at\|assumed\|\$\d+[KM]/year"` in ROI section → generic assumption detected | Auto-flag: wrap any number without `source: customer` or `adjustable: cell_ref` in `[UNVERIFIED]` bracket before output. |
| Building relationship only with the champion, ignoring the economic buyer | Map both roles from day one. Schedule quarterly touchpoints with economic buyer focused on business outcomes, not product features. | `grep -c "economic buyer\|CFO\|VP Finance\|procurement\|budget owner"` in stakeholder map == 0 → single-role relationship | Auto-check: require `stakeholder_map.roles` includes "economic_buyer" with `last_contact < 90 days` before any Deal Desk output. |
| Discounting to defend against competitors without quantifying switching costs | Quantify migration costs first: data migration $X, retraining $Y, lost productivity $Z. Present total cost of switching before any discount. | `grep -i "discount\|price match\|competitive rate"` in defense strategy AND `grep -ci "switching cost\|migration\|retraining\|reimplementation"` == 0 | Auto-block: require `switching_cost_calc` section with 3+ quantified line items before any discount proposal appears in output. |
| Allowing single-threaded accounts to persist without escalation | Flag accounts with only 1 active contact. Escalate within 14 days. Target: ≥3 active contacts per account >$50K ACV. | `grep -c "contact\|responded\|last_touch\|active"` in account stakeholder map < 3 → single-threaded | Auto-flag: insert `[SINGLE-THREADED ACCOUNT — ESCALATE WITHIN 14 DAYS]` banner at top of any output for accounts failing the 3-contact check. |
| Forecasting renewals on gut feel without objective commit criteria | Enforce: (1) procurement contact engaged, (2) budget confirmed, (3) timeline agreed, (4) legal review complete. Missing 2+ = Upside, not Commit. | `grep "Commit" forecast.csv \| awk -F',' '{if ($4 != "yes") print "R2: no procurement"; if ($5 != "yes") print "R3: no budget"}'` → missing criteria | Auto-demote: any deal in forecast with `commit_criteria_met < 3` is automatically classified as `Upside` in output tables. |
| Treating QBRs as product roadmap presentations | Restructure: 80% customer business goals, 20% your product. Pre-read sent 48h before. Confirm economic buyer attends. | `grep -ci "feature\|roadmap\|product update\|new release\|demo"` in QBR deck > `grep -ci "your KPI\|your metric\|you achieved\|your goal\|business outcome"` → one-way pitch | Auto-rewrite: require slide 2 to display customer KPIs. Validate `QBR_deck.slides[1].content` contains customer business metric before deck is finalized. |

## Error Decoder
<!-- DEEP: 5min -- each entry includes a console-string matcher for automatic recovery loops -->

| 🖥️ Console Match (grep pattern) | Symptom | Root Cause | Fix | 🔄 Auto-Recovery Loop |
|---|---|---|---|---|
| `grep -c "procurement\|purchasing" stakeholder_map.csv` returns 0 | Customer agrees to renew verbally but procurement stalls for 60+ days | No relationship with procurement. AM assumed champion controls the process — they don't. | Introduce yourself to procurement contact at 120-day mark. Build procurement into the timeline as a named milestone with owner. | **Loop 1:** (1) Detect: `grep "procurement_engaged" renewal_tracker.csv \| grep "no"` → stall risk. (2) Auto-insert: procurement outreach email template into renewal plan. (3) Require: update `procurement_contact` field before deal moves to Commit. (4) Retry gate: `grep -c "procurement_engaged: yes"` must be >0. |
| `grep -ci "feature\|module\|capability" expansion_pitch.md` > `grep -ci "your problem\|your need\|your team"` | Expansion pitch rejected despite high adoption | Pitch was based on YOUR expansion target, not the customer's business need. | Reframe: identify an unsolved customer problem your expansion solves. Lead with the problem, not the product. | **Loop 2:** (1) Detect: expansion_pitch.md has more product-mentions than customer-problem mentions. (2) Auto-rewrite: insert customer problem statement as paragraph 1. (3) Validate: `grep -ci "your (problem\|need\|team\|pain)"` > 0. (4) Regenerate and retest. |
| `grep "multi_year" contract.csv \| grep -v "exit clause\|off-ramp\|mutual review"` | Multi-year deal signed but customer is unhappy in year 2 | The deal locked them in without corresponding value commitments. They feel trapped. | Add mutual business review clauses (quarterly) with defined success criteria and customer off-ramp if value isn't delivered. | **Loop 3:** (1) Detect: multi-year contract without exit/mutual review clause. (2) Auto-flag: insert `[MISSING: MUTUAL REVIEW CLAUSE]` in contract template. (3) Inject: quarterly business review clause with success criteria. (4) Validate: `grep -c "mutual review\|exit clause\|off-ramp"` > 0 before contract is final. |
| `grep -i "industry average\|typical\|assumed\|\$\d+[KM]" roi_model.xlsx \| wc -l` > 3 | ROI case rejected by finance team | Numbers used industry averages instead of customer-specific data. Finance teams spot generic numbers immediately. | Every number must trace to a customer-provided data point or a labeled adjustable assumption. | **Loop 4:** (1) Detect: >3 generic/industry-average numbers in ROI model. (2) Auto-annotate: wrap each in `[UNVERIFIED — replace with customer data or label as adjustable]`. (3) Inject: adjustable cell reference comment. (4) Validate: `grep -c "customer-provided\|adjustable:"` must equal total assumption count. |
| `grep "Commit" forecast.csv \| awk -F',' '{sum+=$3} END {print sum}'` > `grep "actual" forecast.csv \| awk -F',' '{print $2}'` by >30% | Renewal forecast missed by >30% | Commit category was inflated — deals marked without procurement engagement, budget verification, or timeline confirmation. | Enforce: (1) procurement engaged, (2) budget confirmed, (3) timeline agreed, (4) legal review complete. Missing 2+ = Upside. | **Loop 5:** (1) Detect: commit_total / actual_renewed > 1.3. (2) Auto-demote: all deals with `commit_criteria_met < 3` reclassified to Upside. (3) Regenerate forecast with demoted deals. (4) Validate: `grep "Commit" forecast.csv \| awk -F',' '{if ($4+$5+$6+$7 < 3) print "ERROR"}'` must be empty. |
| `grep -c "switching_cost\|migration_cost\|retraining\|reimplementation" competitive_response.md` == 0 | Discount offered before switching costs quantified | AM panic-discounts to defend against competitor, ignoring that switching costs are the real barrier. | Quantify migration costs before any discount: $X data migration, $Y retraining, $Z lost productivity. | **Loop 6:** (1) Detect: competitive response contains discount language but zero switching-cost references. (2) Auto-inject: switching cost calculator section with 3+ line items. (3) Require: switching cost total displayed before any discount number. (4) Validate: `grep -c "switching cost\|migration\|retraining"` > 0. |
| `grep "last_contact" stakeholder_map.csv \| awk -F',' '{if ($2 > 30) print}' \| wc -l` > 0 | Account goes silent — no contact activity in 30+ days | Relationship has decayed. Champion may have left, budget may have shifted, or competitor has engaged without your knowledge. | Trigger re-engagement sequence: value-add email → executive sponsor outreach → direct phone call within 7 days. | **Loop 7:** (1) Detect: any stakeholder with `last_contact > 30 days`. (2) Auto-generate: 3-step re-engagement plan with templates. (3) Escalate: if no response in 7 days, flag to CEO strategist. (4) Validate: `grep -c "last_contact: <30"` stakeholder_map.csv must equal total contacts. |


## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. Each has a mechanical validation command. -->

| ID | Checklist Item | Validation Command | Auto-Fix |
|----|---------------|-------------------|----------|
| **[AM1]** | Account plans built for all accounts >$50K ACV with stakeholder map (10+ named contacts) | `grep -c "ACV" account_plan_index.csv \| awk '{if ($1 > 0) print "PASS"}'` then `grep -c "contact" account_plans/*.md \| awk -F: '{if ($2 < 10) print "FAIL: " $1}'` → must have 0 failures | Generate account plan template for each account missing one. Auto-populate stakeholder map skeleton with role placeholders. |
| **[AM2]** | Multi-threading audit complete — every account >$50K has ≥3 active contacts (responded within 30 days) | `grep "last_contact" stakeholder_map.csv \| awk -F',' '{if ($2 > 30) count++} END {if (count == 0) print "PASS"; else print "FAIL: " count " stale contacts"}'` → must be PASS | Auto-flag stale contacts. Generate re-engagement email templates. Schedule follow-up reminders. |
| **[AM3]** | Single-point-of-failure accounts identified and flagged | `grep -c "active_contact" account_plans/*.md \| awk -F: '{if ($2 < 2) print "FAIL: " $1}'` → must be empty | Auto-insert `[ESCALATE: SINGLE-THREADED — 14 DAY DEADLINE]` banner in account plan. Generate executive sponsor pairing request. |
| **[AM4]** | Value log maintained per account — every customer win documented with date, metric, and customer quote | `grep -c "date\|metric\|quote" value_logs/*.md \| awk -F: '{if ($2 < 1) print "MISSING: " $1}'` → must be empty | Generate value log template. Prompt for recent wins. Auto-schedule monthly value log review reminder. |
| **[AM5]** | Renewal timeline initiated at 120-day mark with standardized 4-phase process | `grep "days_until_renewal" renewal_tracker.csv \| awk -F',' '{if ($2 <= 90 && $3 == "not_started") print "LATE: " $1}'` → must be empty | Auto-create renewal kickoff task. Generate 120-day countdown timeline. Notify AM if within 90-day window with no activity. |
| **[AM6]** | Price increase justification links to customer-specific value delivered, not market rates | `grep -i "market rate\|inflation\|our costs" price_increase/*.md` → must return nothing | Block price increase justification containing market-rate language. Auto-prompt for value log to populate justification with customer-specific ROI data. |
| **[AM7]** | Renewal forecast maintained with commit/upside/pipeline categories and objective criteria | `grep "Commit" forecast.csv \| awk -F',' '{if ($4+$5+$6+$7 < 3) print "DEMOTE: " $1 " has only " $4+$5+$6+$7 " criteria"}'` → must be empty | Auto-demote deals with <3 commit criteria to Upside. Regenerate forecast with corrected categories. |
| **[AM8]** | Expansion pipeline scored and reviewed monthly with adoption qualification | `grep "expansion" pipeline.csv \| awk -F',' '{if ($4 < 80 \|\| $5 < 30 \|\| $6 > 0) print "UNQUALIFIED: " $1}'` → must be empty | Auto-flag unqualified expansion opportunities. Block expansion pitch generation until adoption >80%, NPS >30, no open escalations. |
| **[AM9]** | ROI business case template standardized with traceable numbers | `grep -ci "industry average\|typical\|assumed" roi_cases/*.md` → must return 0 | Auto-wrap unverifiable numbers in `[UNVERIFIED]`. Require customer data source or labeled adjustable cell for every assumption. |
| **[AM10]** | Competitive displacement defense playbook ready with migration cost calculator | `file_exists("competitive_defense/*/migration_cost_calc.xlsx")` → must return true for all top-10 accounts | Generate migration cost calculator template. Auto-populate with estimated data migration, retraining, and productivity loss line items. |
| **[AM11]** | Executive sponsor program active with quarterly engagement tracking | `grep "sponsor_last_contact" exec_sponsor/*.csv \| awk -F',' '{if ($2 > 90) print "STALE: " $1}'` → must be empty | Auto-generate sponsor briefing document. Schedule quarterly sponsor-customer touchpoint. Flag stale pairings for re-assignment. |
| **[AM12]** | Multi-year deal template includes annual business review and mutual exit clauses | `grep -c "business review\|mutual exit\|off-ramp" contract_templates/multi_year.md` → must be >= 3 | Auto-inject quarterly business review clause, mutual exit criteria, and technology refresh provision into multi-year templates. |
| **[AM13]** | Procurement path mapped per account — contact, timeline, terms acceptability known | `grep -c "procurement_contact\|standard_terms\|security_review" account_plans/*.md \| awk -F: '{if ($2 < 3) print "INCOMPLETE: " $1}'` → must be empty | Auto-generate procurement path questionnaire. Prompt for contact name, standard terms acceptability, security review timeline. |
| **[AM14]** | Quarterly account tier review completed with engagement cadence per segment | `file_contains("account_tiers/*.md", "Strategic\|Enterprise\|Commercial\|SMB")` AND `date -r account_tiers/last_review < date -d "-90 days"` → must be PASS | Auto-classify accounts by ACV thresholds. Generate tier review summary. Schedule next quarterly review. Set engagement cadence per tier. |

## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->

### Coordinate With

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **Sales Engineer** | Account handoff post-sale, expansion opportunity requiring technical scoping | Technical environment, promised capabilities, integration requirements. For expansion: scoping new use cases, security review support. |
| **Customer Success Manager** | Health score insights, adoption data, QBR alignment, churn risk detection | Request: health score report, adoption dashboard, support ticket summary, VoC feedback. Share: renewal timeline, pricing strategy, stakeholder changes. **Decision gate:** Is health score > 70? → renewal on track. **Artifact:** account health report + joint QBR deck. |
| **Customer Support Engineer** | Support ticket patterns affecting renewal, unresolved escalations, customer satisfaction signals | Request: ticket history summary, resolution trends, open issues. Share: renewal context — don't push expansion if support issues are unresolved. **Decision gate:** Are open tickets < 5 and none older than 30 days? → expansion viable. **Artifact:** support health summary + ticket trend report. |
| **Legal Advisor** | Contract negotiation (MSA amendments, SLA changes, security addenda, multi-year terms) | Redline requests, customer's proposed language, business rationale for terms. Ask: risk assessment, fallback positions, non-negotiable provisions. |
| **CEO Strategist** | Strategic account (>$500K ACV) at risk, multi-year deal >$1M, competitive displacement at key account | Revenue impact analysis, strategic importance of account, options with tradeoffs. Escalate when standard interventions have failed. |
| **Product Manager** | Feature gaps blocking expansion, competitive feature parity threats, roadmap commitments for customer retention | Specific customer requirements, revenue at risk, competitive intelligence. Request: roadmap confirmation for customer-facing commitments. **Decision gate:** Does feature gap affect > 3 accounts? → roadmap escalation. **Artifact:** feature gap impact analysis + customer commitment tracker. |
| **Business Strategist** | Pricing strategy for new segments, competitive positioning, market rate benchmarks | Share: win/loss data, competitive pricing intel, customer willingness-to-pay signals. Ask: market pricing analysis, competitive landscape update. |
| **RevOps Manager** | Renewal forecasting, NRR tracking, pipeline analytics, account tier modeling | Renewal pipeline data, expansion pipeline, account tier classification. **Decision gate:** Is renewal forecast accuracy > 80% at 90-day horizon? → forecast reliable. **Artifact:** renewal forecast report + NRR dashboard. |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Renewal at risk (customer signals intent to not renew) | Customer Success Manager, CEO Strategist (if >$100K ACV) | Immediate intervention. Health re-evaluation. Save strategy activated. |
| Competitor formally engaged (RFP, POC, trial with competitor) | Product Manager, CEO Strategist | Competitive defense. Feature gap analysis. Executive relationship activation. |
| Champion departs (detected) | Customer Success Manager | Re-establish relationship within 7 days. Multi-threading emergency. |
| Procurement demands non-standard terms (uncapped liability, custom SLA) | Legal Advisor | Contract review. Risk assessment. Negotiation strategy. |
| Expansion closed >$100K | Customer Success Manager | Onboarding trigger. Success plan updated. Health score recalibrated for larger deployment. |
| Customer requests feature that's on roadmap for next quarter | Product Manager | Beta program enrollment. Roadmap commitment confirmation. Customer NDA if needed. |

### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | sales-engineer | Technical handoff document, implementation requirements, customer expectations set during sales cycle |
| **Before** | customer-success-manager | Health scores, adoption data, churn risk assessment, QBR outputs, VoC insights |
| **This** | account-manager | Account plans, renewal strategy, expansion pipeline, ROI business cases, executive sponsor program, negotiated contracts |
| **After** | customer-success-manager | Consumes renewal outcome for health score recalibration, expansion wins trigger onboarding/success plan updates |
| **After** | legal-advisor | Consumes contract negotiation requests, redline review, risk assessment for non-standard terms |
| **After** | ceo-strategist | Consumes strategic account status, revenue at risk, multi-year deal structures for board reporting |

Common chains:
- **Sale to renewal**: sales-engineer → account-manager → customer-success-manager — Technical handoff → account plan → health monitoring and adoption
- **Expansion loop**: customer-success-manager → account-manager — Usage signals → expansion qualification → upsell/cross-sell close
- **Renewal defense**: account-manager → product-manager → legal-advisor — Competitive threat detected → feature gap commitment → contract terms review
- **Strategic negotiation**: account-manager → legal-advisor → ceo-strategist — Non-standard terms requested → risk assessment → executive approval

## Proactive Triggers
<!-- QUICK: 30s -- when to proactively notify stakeholders -->

| Trigger | Notify | Why |
|---------|--------|-----|
| Champion departs (detected via email bounce, LinkedIn job change, or non-response >30 days) | Customer Success Manager | Single point of contact failure. Re-establish relationship with a new champion within 7 days. If no new contact is made, renewal probability drops below 30%. |
| Competitor formally engaged (RFP issued, POC underway, trial with competitor detected) | Product Manager, CEO Strategist (if >$100K ACV) | Competitive defense activation. Feature gap analysis required. Executive relationship must be activated immediately — peer-to-peer sponsor outreach within 48 hours. |
| Procurement demands non-standard terms (uncapped liability, custom SLA, IP indemnity, data residency addenda) | Legal Advisor | Non-standard terms can delay or kill deals. Legal review, risk assessment, and negotiation strategy needed before committing to any position. |
| Multi-year renewal approaching 120-day mark for account >$250K ACV | Customer Success Manager, RevOps Manager, CEO Strategist | Strategic renewal cycle initiation. Value documentation review. Executive alignment on pricing strategy. Multi-year deals require longer preparation and executive sponsorship. |
| Customer's usage of premium/paid-addon features spikes 3x month-over-month | Customer Success Manager | Expansion signal — the customer is outgrowing their current tier. Engagement before they hit a usage ceiling prevents frustration and positions expansion naturally. |
| Account health score drops >20 points within 30 days | Customer Success Manager, CEO Strategist (if >$100K ACV) | Rapid health deterioration signals an acute issue — product failure, support crisis, or internal customer decision to evaluate alternatives. Intervention required within 48 hours. |
| Customer contact goes silent for 45+ days (no email response, missed meetings, no support activity) | Customer Success Manager | Disengagement is a leading churn indicator. The customer has likely deprioritized your product or is evaluating alternatives. Re-engagement before the relationship fully atrophies. |
| Expansion closed >$100K ACV | Customer Success Manager, Sales Engineer | Onboarding trigger for expanded deployment. Success plan update. Health score recalibrated. The larger deployment requires coordinated handoff to ensure value is delivered against the expanded scope. |

## Scale Depth: Solo → Small → Medium → Enterprise
<!-- DEEP: 10+min -- how this skill changes as the company grows -->

### Solo
Founder handles renewals and upsells personally. Keep customers, don't churn. No dedicated AM; relationship is founder-to-buyer; ad-hoc check-ins. Focus on keeping early customers happy and learning which expansion motions work.

### Small Team
First AM hire manages all accounts, builds playbooks. Systematize retention, identify expansion. Dedicated AM; QBR cadence starts; renewal process defined. Account management moves from reactive to proactive with structured renewal cadence.

### Medium Team
Named account model, tiered coverage, expansion targets. Grow accounts strategically, protect revenue base. Strategic vs. Commercial tiers; account plans; whitespace analysis; NRR tracked. AM team has capacity for account planning and proactive expansion while maintaining retention.

### Enterprise
Global account management, key account programs, executive sponsorship. Enterprise land-and-expand, multi-year deals. Global AM team; executive sponsor program; multi-product expansion; $1M+ account plans. Executive relationships are systematically maintained, not left to chance.

### Transition Triggers
- **Solo → Small Team:** Customer count exceeds 20 accounts or ACV base exceeds $1M ARR requiring dedicated retention focus.
- **Small Team → Medium Team:** Accounts exceed 50 requiring account tiering and named AM model.
- **Medium Team → Enterprise:** Multi-product, multi-region accounts require global AM coordination and executive sponsor programs.


## What Good Looks Like
<!-- QUICK: 30s -->
**Completed account management program:** Every account >$50K ACV has a living account plan with stakeholder map updated quarterly. No account has a single point of contact failure. Renewal pipeline managed on a 120-day cycle with commit stages objectively defined. Forecast accuracy within 10% of actual. Every price increase backed by a value justification document. Expansion pipeline sourced from product usage data, not guesswork — expansion contributes ≥30% of NRR growth. Executive sponsor program active with quarterly engagement tracked and reported. ROI business cases use customer-specific data with labeled assumptions. Competitive displacement losses have post-mortems completed within 2 weeks.

A new AM joining the team can take over an existing account within 1 week — the account plan, value log, and stakeholder map tell them everything they need to know. A renewal can be forecasted 90 days out with >80% accuracy by an AM who has never met the customer, based on health score, adoption data, and relationship audit.


## Footguns
<!-- DEEP: 10+min — war stories from account management -->

| Footgun | What Happened | Root Cause | How to Prevent |
|---------|---------------|------------|----------------|
| Managed a $450K ARR account through a single champion for 3 years — the champion left for a competitor, and within 90 days the account churned because nobody else in the 800-person customer organization knew the AM's name | The AM had a great relationship with the VP of Engineering. Monthly check-in calls, quarterly dinners, Christmas gifts. The VP championed the product internally — convinced their CTO, pushed through procurement, defended the renewal. When the VP left for a competitor, the AM called their mobile. No answer. Called again. "I can't help you — I'm at [competitor] now." The AM had zero relationships with the VP's boss, their peers, their direct reports, or procurement. The new VP arrived, found a vendor with no internal advocates, and ran an RFP. The account churned. $450K ARR gone. | The AM built a single-threaded relationship and confused "the champion loves us" with "the account is healthy." A single-threaded account is one resignation away from churn. The AM had no trigger for "what if this person leaves?" and no multi-threading program in their account plan. | **Every account >$50K ACV must have minimum 4 active relationships documented in CRM with last contact dates: champion, executive sponsor, 1 power user, and 1 procurement/finance contact.** Multi-threading health check monthly: if any account has only 1 active contact (responded within 30 days), it's flagged as "single point of failure" and the AM has 14 days to establish a second relationship or escalate. Set LinkedIn alerts on all champions — if they change jobs, you get notified within 24 hours. The account plan must include "who succeeds the champion?" — name the person, start the relationship now. |
| Sent a renewal quote with a 15% price increase justifying "market rates and increased product investment" — the customer's procurement team ran an RFP, found a competitor at 20% less, and moved the entire 300-seat deployment | The AM's renewal strategy was: "We delivered value, so we're raising prices." The renewal letter said: "Due to market conditions and our continued investment in the platform, your renewal price will increase by 15% to $172,500/year." The customer's procurement team: "Show us the value you delivered that justifies 15% more." The AM sent a generic product release notes PDF. Procurement ran an RFP. A competitor offered the same core functionality at $115,000/year. The customer moved. Total revenue loss: $150K/year × 3-year expected lifetime = $450K. | The price increase was justified by the seller's costs ("we invested more"), not the buyer's value ("you achieved X"). "Market rates" is not a justification — it's an invitation to run an RFP. The AM didn't quantify the customer's ROI from the product before asking for more money. | **Every price increase must be preceded by a value delivery document sent at least 60 days before the renewal quote.** The document must answer: "Here's what we promised, here's what we delivered — with YOUR data." Example: "In 2023, your team processed 47,000 support tickets through our platform. Average resolution time dropped from 14 hours to 3.2 hours. Your VP of Support estimated this saved $680K in headcount costs. Your renewal is $172,500 — a 15% increase reflecting the 4 new modules you adopted and your 22% seat growth. Your ROI on the platform was 5.1× in 2023." If you can't produce that paragraph with customer-specific numbers, don't raise the price. |
| Forecast a $320K renewal as "Commit — 95% confidence" because the champion said "we're good, just send the paperwork" — the champion hadn't told their VP, procurement wasn't engaged, budget hadn't been allocated, and the renewal slipped 2 quarters with a 10% discount to close | The AM had a verbal commitment from their champion: "Budget is approved, we're renewing. Send the contract." The AM marked it "Commit" in the forecast. CEO presented the renewal pipeline to the board: "$2.1M in Commit, 95% confidence." The champion was sincere — they believed the renewal was a done deal. But they hadn't initiated the procurement process. When the contract landed in procurement, the response was: "This isn't in Q2 budget. We can look at it in Q3." The deal slipped 2 quarters. To close in Q3, the AM had to offer a 10% discount because the customer's "leverage" had increased. Revenue recognized in Q3 instead of Q1, and $32K lower. | The AM confused "champion commitment" with "procurement commitment." A verbal yes from a champion is "Upside," not "Commit." Commit requires: (a) procurement contact confirmed and engaged, (b) budget verified (not "champion says it's there" — "procurement confirmed PO number"), (c) legal/security review complete or not required, (d) no blockers identified. | **Use objective commit criteria, not relationship sentiment.** Commit (90%+): procurement contact confirmed AND budget verified (PO number or written confirmation) AND all approvals identified AND no outstanding legal/security items. Upside (50–89%): champion committed verbally AND no blockers identified AND procurement path known. Pipeline (<50%): early stage, budget not verified, procurement not engaged. Review every deal marked "Commit" weekly: "Has procurement acknowledged the renewal? Show me the email." If the answer is "the champion said..." — downgrade to Upside. A forecast surprise is always better than a forecast miss. |
| Pitched a $120K module upsell to a customer whose core product adoption was at 40% and NPS was 12 — the customer canceled the upsell meeting, escalated to their VP, and the VP demanded a "value audit" of the core product before the renewal | The AM identified a $120K expansion opportunity: a new analytics module that would "transform how the customer uses our platform." The customer's adoption of the core product: 40% of licensed seats active in the last 30 days. NPS: 12. Three open support tickets, one >45 days old. The AM pitched the upsell anyway — "this will solve your analytics gaps." The customer's response: "We're not even getting value from what we already bought. Why would we buy more?" The conversation escalated to the VP of Operations, who demanded a comprehensive value audit. The renewal, previously on track, was now contested. | The AM chased expansion revenue without checking adoption health. Expansion that precedes value realization is value extraction — the customer experiences it as "they're trying to sell me more of something I'm not sure I want." The AM didn't check the CS health score before pitching expansion. | **Gate all expansion conversations on adoption health.** Before pitching expansion, verify: (a) core product adoption >60% (active seats/licensed seats), (b) NPS >30 or health score >70, (c) zero open escalations older than 14 days. If any gate fails, the expansion conversation becomes a value-recovery conversation: "Before we talk about the analytics module, let's make sure you're getting full value from what you have. Can we schedule a 30-minute optimization session to get your adoption above 80%?" Expansion follows adoption — always in that order. |
| Offered a 30% discount to save a $180K account that was threatening to churn — the customer took the discount, stayed for 6 months, churned anyway, and the discounted rate became the new anchor for 3 other accounts the customer referred to | A $180K account threatened to churn — "Competitor X is 40% cheaper." Without a save agreement or success criteria, the AM offered a 30% discount: "We value your partnership and want to make this work." The customer accepted. No terms attached. Six months later, they churned — the competitor was actually better for their use case. Worse: the procurement contact mentioned the discounted rate to a peer at a conference. Within 3 months, 3 other accounts were asking "why are we paying full price when [Customer X] got a 30% discount?" Total revenue impact: $180K (churned account) + $135K (price concessions to 3 referenced accounts) = $315K. | The save offer had no conditions. A discount without a save agreement is a gift — the customer has no incentive to change behavior or commit to renewal. The AM prioritized retention of THIS quarter's revenue over long-term pricing integrity. B2B pricing is a network — enterprise customers talk to each other. | **Every save offer must include a save agreement with mutual commitments.** Template: "We're offering a 30% discount for the next 12 months. In return, we ask for: (a) monthly executive check-ins to track value metrics, (b) a case study or reference upon achieving agreed-upon outcomes, (c) a commitment to a 2-year renewal at standard pricing if the value metrics are met, (d) our pricing terms remain confidential under NDA." The save agreement must have a named executive sponsor on the customer side. If the customer won't commit to the save agreement, the discount won't save them — it only delays churn and sets a precedent. |

## Calibration — How to Know Your Level
<!-- STANDARD: 3min — honest self-assessment rubric -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You can run a standard renewal to close but can't build a stakeholder map, don't know who the economic buyer is vs. the champion, and have never documented who actually signs the contract at any of your accounts | You manage a $3M book of business at >95% GRR and >115% NRR; every account >$50K has a live account plan with 4+ named contacts updated quarterly; renewal forecast accuracy is within 10% at 90-day horizon | The champion at your $1M account resigns — within 72 hours you have a new executive sponsor relationship established through an introduction from the departing champion, the renewal closes on time at a 7% price increase, and the customer's new VP tells their team "the AM is the reason we didn't skip a beat during the transition" |
| You lead renewal conversations with price — "here's your renewal quote" — and can't answer when the customer says "remind me what value you delivered this year?" | You lead every renewal with a value review that the customer agrees with BEFORE you discuss pricing — "Your team resolved 47K tickets this year, average time dropped 72%, your VP estimates $680K saved. Your renewal is $172,500. Is that value story accurate?" | You take over a $500K account that's been flat for 3 years with no expansion — within 12 months you've identified 3 whitespace opportunities through stakeholder discovery, expanded ACV to $820K, and the customer references you to 2 other divisions |
| You forecast renewals based on "the champion said we're good" and have a forecast accuracy below 60% at 30-day horizon | You forecast renewals with objective commit criteria — procurement confirmed, budget verified, legal review complete — and your 90-day forecast accuracy is >85% for 4 consecutive quarters | A VP of Sales asks you to build the account management function from scratch at a company with $15M ARR and 80 accounts — within 6 months you've designed the account tiering model, hired and trained 4 AMs, implemented the renewal forecasting system, and NRR is trending from 105% to 118% |

**The Litmus Test:** Can you take over an at-risk account you've never touched — review the account plan, health score, adoption data, and support history — and tell me within 30 minutes whether it's savable, what the save play is, and what the probability of retention is at 90 days? If you'd need to "schedule a call with the champion first," you're not L3.

## References

## Deliberate Practice

```mermaid
graph LR
    A[Execute<br/>process] --> B[Measure<br/>friction] --> C[Identify<br/>bottleneck] --> D[Re-design<br/>process] --> A
```

| Level | Practice | Frequency |
|-------|----------|-----------|
| **Novice** | Document your current workflow; highlight every step that requires human judgment or waiting | Monthly |
| **Competent** | Run a "process autopsy" on a recent initiative: what took longest, where were the miscommunications? | Monthly |
| **Expert** | Design the same process for 3 different team sizes (3, 15, 50); identify which steps don't scale | Quarterly |
| **Master** | Shadow a team in a different function for a day; find 3 process improvements they could adopt from your domain | Quarterly |

**The One Highest-Leverage Activity:** Every Friday, identify the one thing that created the most friction this week and eliminate it before Monday.

## References
<!-- QUICK: 30s -- links to deeper reading -->
- **references/account-plan-templates.md** — Full account plan templates by tier (Strategic, Enterprise, Commercial, SMB), stakeholder mapping worksheets, whitespace analysis frameworks
- **references/renewal-playbooks.md** — Step-by-step renewal scripts by scenario (healthy renewal, at-risk save, competitive defense, multi-year negotiation), price increase justification templates, procurement navigation guide
- **references/expansion-selling-guide.md** — Land-and-expand methodology, module upsell qualification criteria, cross-sell correlation analysis, usage-based growth triggers and playbooks
- **references/roi-business-case-builder.md** — ROI model spreadsheet template, customer data collection questionnaire, CFO-facing presentation format, common objection handling
- **references/executive-sponsor-program.md** — Sponsor matching methodology, briefing template, quarterly scorecard, escalation protocols
- **references/contract-negotiation-guide.md** — MSA redline playbook (common clauses, fallback positions), SLA tier structure, security addenda templates, multi-year deal provisions
- _The Challenger Customer_ by Brent Adamson, Matthew Dixon, et al. — stakeholder mapping and multi-threading methodology
- _Negotiating the Impossible_ by Deepak Malhotra — frameworks for complex multi-stakeholder negotiations
- _Mastering the Complex Sale_ by Jeff Thull — value-based selling and ROI justification for enterprise deals
