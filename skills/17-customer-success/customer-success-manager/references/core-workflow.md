# Core Workflow — Full Implementation

<!-- QUICK: 30s -- scan phase titles to understand the process -->

<!-- DEEP: 10+min -->

### Phase 1 (~45 min): Customer Onboarding Design
<!-- STANDARD: 3min -->
Design the onboarding program from signature to first value. Map the customer journey: **Pre-boarding** (contract signed → kickoff call: define success criteria, identify stakeholders, align on timeline), **Technical Onboarding** (integration/implementation: SSO, data import, API setup), **Product Onboarding** (user training, workflow configuration, admin setup), **Value Realization** (customer achieves "aha moment" — the first measurable outcome that proves the product works for their use case).

Define TTFV target by segment: SMB = 7 days, Mid-Market = 14 days, Enterprise = 30 days. Track onboarding completion rate and TTFV by cohort. Build an onboarding scorecard: % tasks complete, days to first value, CSAT at 30/60/90 days.
<!-- DEEP: 10+min -->
**War story:** A $200K enterprise deal churned at month 4 despite "successful" technical onboarding. Root cause: the technical team completed integration in 10 days, but the business users — who were the actual buyers — never logged in. The CS team measured "integration complete" as onboarding done but never verified end-user adoption. Fix: onboarding is not complete until 80% of named users have logged in and completed at least one core workflow. Add "business user activation" as a required gate before closing the onboarding phase.

<!-- DEEP: 10+min -->

### Phase 2 (~30 min): Health Scoring Model Construction
<!-- STANDARD: 3min -->
Build a weighted health score (0-100) from 5-8 signal categories. Each signal gets a normalized sub-score (0-100), then weighted. **Core signals:**

| Signal | Weight | Data Source | Healthy | Warning | Critical |
|--------|--------|-------------|---------|---------|----------|
| Product Usage (DAU/WAU/MAU) | 25% | Product analytics | >80% of licensed seats active | 50-80% | <50% |
| Feature Adoption Depth | 20% | Product analytics | >5 core features used weekly | 2-4 features | <2 features |
| Login Recency | 15% | Auth logs | Last login <7 days | 7-14 days | >14 days |
| NPS / CSAT | 15% | Survey tool | NPS >50, CSAT >4.0 | NPS 0-50 | NPS <0, CSAT <3.0 |
| Support Ticket Health | 10% | Support desk | <2 tickets/month, avg resolution <24h | 2-5 tickets/month | >5 tickets/month or unresolved >72h |
| Payment History | 10% | Billing system | On-time last 6 months | 1 late payment | 2+ late payments |
| Relationship Strength | 5% | CRM | Executive sponsor engaged, QBR attended | Sponsor changed in 6 months | No sponsor identified |

Score = Σ (signal_score × weight). Recalculate weekly. Set thresholds: Green ≥80, Yellow 60-79, Orange 40-59, Red <40. Review thresholds quarterly against actual churn data for calibration.
<!-- DEEP: 10+min -->
**War story:** A CS team used NPS as 40% of health score weight. A "promoter" (NPS 9) churned 3 weeks later. Investigation: the NPS respondent was the original champion who'd left the company 2 weeks before the survey — the new decision-maker inherited the contract and had no relationship. Fix: always verify that survey respondents still match the account's current decision-maker. Add executive-sponsor-change as an automatic -20 point penalty to health score regardless of other signals.

<!-- DEEP: 10+min -->

### Phase 3 (~40 min): QBR Preparation & Execution
<!-- STANDARD: 3min -->
**QBR Deck Structure (12 slides, 45 min presentation):**
1. **Executive Summary** — 3 bullet outcomes from last QBR, status of each
2. **Success Metrics Review** — Customer's business KPIs, not your product metrics. "Time to close month-end reduced from 5 days to 2 days."
3. **Product Adoption Dashboard** — Feature usage trends, user growth, depth of adoption. Show the ROI: "87% of your licensed users are active weekly."
4. **Value Delivered This Quarter** — Specific use cases solved, problems eliminated, wins enabled
5. **Support & Incident Review** — Tickets filed, resolution times, root causes addressed. "We resolved 12 tickets, average time 4.2 hours, 3 bugs fixed in your environment."
6. **Product Roadmap Alignment** — 2-3 items from your roadmap that map to their stated priorities
7. **Upcoming Risks & Mitigations** — Be proactive about: contract renewal, changing requirements, market shifts
8. **Expansion Opportunities** — New departments, use cases, or modules they'd benefit from (grounded in data)
9. **Success Plan for Next Quarter** — Joint objectives with owners and dates on both sides
10. **Customer Feedback & Requests** — Their top feature requests, status of each
11. **Executive Ask** — What you need from them: reference call, case study, beta participation
12. **Next Steps & Timeline** — Commitments with dates from both parties

Pre-QBR checklist: run health score report, compile support ticket summary, check payment status, confirm attendees (must include economic buyer), prepare 3 customer-specific value stories.
<!-- DEEP: 10+min -->
**War story:** A CSM delivered a QBR showing 98% uptime, 50+ features shipped, and glowing adoption metrics. The customer's VP didn't renew. Why? The QBR never connected product usage to the customer's actual business goal: "reduce customer onboarding time by 40%." The VP saw zero progress on their metric and concluded the product didn't deliver. Fix: every QBR must open with the customer's stated business objectives from the prior QBR and close with measurable progress against them. The product metrics are evidence, not the story.

<!-- DEEP: 10+min -->

### Phase 4 (~25 min): Churn Prediction & Intervention
<!-- STANDARD: 3min -->
**Churn Prediction Model:** Identify leading indicators that precede churn by 60-90 days. Top predictors: declining login frequency (3+ consecutive weeks of decline), reduced feature usage breadth (stopped using 2+ core features), support ticket spike (>3x normal volume in 30 days), key champion change (departure detected), missed payment, competitor search activity, declining NPS (drop >20 points in 6 months).

**Intervention Playbooks:**
- **Product Adoption Decline:** Schedule "value realization workshop" — 60 min session with power users + decision-maker. Re-demo the core workflow they stopped using. Identify friction. Assign a 14-day success plan sprint.
- **Champion Departure:** Immediate outreach to executive sponsor. Schedule re-onboarding for new champion within 7 days. Offer to present product value to new stakeholder directly.
- **Competitive Threat:** Research competitor's claimed advantage. Build comparison document with verifiable data. Offer extended trial of your differentiating features. Engage product team for roadmap commitment if there's a genuine gap.
- **Silent Customer (21+ days):** Phone call, not email. Loop in sales AE who closed the deal. Check company news for acquisition, layoff, or leadership change.
<!-- DEEP: 10+min -->
**Save Offer Framework:** Tier save offers based on ACV. <$25K: 1-month free, extended onboarding. $25K-$100K: 10-20% discount for multi-year commitment, premium feature unlock. >$100K: custom pricing package, dedicated support for 90 days, executive sponsor alignment. Never offer discount without a commitment (contract extension, case study, reference). Track save rate by offer type to optimize over time.

<!-- DEEP: 10+min -->

### Phase 5 (~20 min): Expansion Revenue Identification
<!-- STANDARD: 3min -->
Identify expansion within existing accounts using product signals: **Seat expansion** — license utilization >85% for 2+ consecutive months triggers upsell conversation. **Module upsell** — power user accessing premium features (tracked via feature flag pings) triggers premium tier conversation. **Usage-based growth** — API call volume or data storage exceeding 80% of plan limit for 2 consecutive months. **Cross-sell adjacent products** — account uses Product A, their use case maps to Product B (identified via correlation analysis of multi-product customers).

**Expansion pipeline:** Score each account on expansion propensity (1-5) using: license utilization %, feature exploration behavior, department count, contract age (>12 months = higher propensity). Review expansion pipeline weekly with account-manager. Target: 30% of NRR growth from expansion, not just retention.
<!-- DEEP: 10+min -->
**War story:** A CS team identified a customer at 95% seat utilization and pitched a 20-seat expansion. The customer declined. Six months later, the customer churned. Post-mortem: the customer didn't need more seats — they needed to optimize existing workflows so they could use fewer seats more effectively. The CSM's expansion pitch felt like a money grab. Fix: expansion recommendations must be grounded in the customer's stated goals. "Based on your goal to roll out to the EMEA team, you'll need 15 additional seats. Here's the business case showing expected productivity gain."

<!-- DEEP: 10+min -->

### Phase 6 (~20 min): Voice of Customer Programs
<!-- STANDARD: 3min -->
Build systematic feedback collection: **NPS surveys** — quarterly, transactional (post-support, post-onboarding milestone), relationship (semi-annual). Target >30% response rate; below that, scores are unreliable. **Customer Advisory Board (CAB)** — 8-12 strategic customers, meet quarterly, 90-minute sessions. Agenda: 50% roadmap feedback, 30% industry trends discussion, 20% relationship building. **Beta program** — recruit 5-10 customers per feature beta. Criteria: high health score, relevant use case, willingness to provide feedback within 14 days. **Win/loss analysis** — interview churned customers within 30 days. Questions: "What problem were you solving?", "Why did you choose our competitor?", "What would have made you stay?"

**Feedback loop closure:** Every quarter, publish to product-manager: top 5 feature requests (ranked by revenue at risk), top 3 churn reasons (with representative quotes), top 3 expansion signals. Track: % of product roadmap items originating from VoC, time from feedback received to roadmap response.
<!-- DEEP: 10+min -->
**War story:** A CS team ran NPS quarterly and consistently scored 60+. Leadership celebrated. But the survey only went to the champion (who picked the product). When they surveyed end users separately, NPS was -10. The champion was happy; the people using the product every day were frustrated. Fix: survey at least 2 personas per account — champion/buyer AND end user. Segment NPS by persona. A champion-only NPS is dangerously inflated.
