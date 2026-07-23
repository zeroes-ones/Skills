# Core Workflow — Full Implementation

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
