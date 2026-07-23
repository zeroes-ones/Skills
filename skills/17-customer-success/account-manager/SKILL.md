---
name: account-manager
description: >
  Use when planning account strategies, executing renewals, expanding revenue within existing
  accounts, building ROI business cases, or preparing for contract negotiations. Handles
  commercial relationship management post-sale with stakeholder mapping, renewal strategy
  and price justification, land-and-expand selling, executive sponsor programs, account tier
  management, multi-threading, retention campaigns, and renewal forecasting. Do NOT use for
  new logo acquisition, customer onboarding and adoption, product roadmap prioritization,
  or support ticket management.
license: MIT
tags:
  - account-manager
  - renewal-management
  - expansion-selling
  - contract-negotiation
  - stakeholder-mapping
author: Sandeep Kumar Penchala
type: customer-success
status: stable
version: 1.1.0
updated: 2026-07-23
token_budget: 3520
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
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

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

> See [references/core-workflow.md](references/core-workflow.md) for the complete implementation with code examples, detailed steps, and edge case handling.

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

## What Good Looks Like

<!-- QUICK: 30s -->
**Completed account management program:** Every account >$50K ACV has a living account plan with stakeholder map updated quarterly. No account has a single point of contact failure. Renewal pipeline managed on a 120-day cycle with commit stages objectively defined. Forecast accuracy within 10% of actual. Every price increase backed by a value justification document. Expansion pipeline sourced from product usage data, not guesswork — expansion contributes ≥30% of NRR growth. Executive sponsor program active with quarterly engagement tracked and reported. ROI business cases use customer-specific data with labeled assumptions. Competitive displacement losses have post-mortems completed within 2 weeks.

A new AM joining the team can take over an existing account within 1 week — the account plan, value log, and stakeholder map tell them everything they need to know. A renewal can be forecasted 90 days out with >80% accuracy by an AM who has never met the customer, based on health score, adoption data, and relationship audit.

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

## Gotchas

- **QBR (Quarterly Business Review) as a product demo** — you spend 45 minutes showing features they already have, 10 minutes on new features, and 5 minutes on "any questions?" The customer learned nothing about the VALUE they got. QBR should be: "Here's what you achieved with our product this quarter (with data), here's what you could achieve next quarter, what's blocking you?"
- **Renewal conversation that starts 30 days before renewal date** — the customer has been silently unhappy for 11 months, built a business case for a competitor, and secured budget. Your "let's talk renewal" arrives as they're signing with the competitor. Renewal is a continuous conversation starting day 1, not a Q4 event.
- **"Our NPS is 65!"** — but you only surveyed customers who renewed (churned customers weren't asked). And the CEO of a 500-seat account gave a 9, while 12 end-users gave 4s. NPS weighted by revenue AND stratified by role (decision-maker vs end-user) tells the real story.
- **Expansion revenue from "land and expand"** — you landed with a $20K team deal and plan to expand to $200K enterprise in year 2. But the team that adopted your product LEFT the company. Your internal champion is gone, and the new team lead uses a competitor. Land-and-expand requires multi-threaded relationships from day 1.


## Verification

- [ ] Health score: every account has a health score (green/yellow/red) updated monthly
- [ ] QBR cadence: every strategic account had QBR within last 120 days
- [ ] Renewal pipeline: all renewals in the next 90 days have active engagement within last 30 days
- [ ] NPS: response rate ≥ 40%, results segmented by revenue tier and user role
- [ ] Expansion: at least 2 contacts per strategic account, decision-maker engaged within last quarter


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

