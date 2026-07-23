---
name: customer-success-manager
description: >
  Use when designing customer health score models, preparing QBRs, predicting and preventing
  churn, optimizing time-to-first-value, identifying expansion opportunities, or running
  voice-of-customer programs. Handles the full post-sale customer lifecycle from onboarding
  through advocacy with health scoring, churn intervention playbooks, adoption monitoring,
  NRR/GRR tracking, and customer journey mapping. Do NOT use for commercial renewal
  negotiations, new business development, support ticket triage, or product roadmap
  decisions.
license: MIT
tags:
  - customer-success-manager
  - churn-prevention
  - health-scoring
  - qbr
  - customer-onboarding
author: Sandeep Kumar Penchala
type: customer-success
status: stable
version: 1.1.0
updated: 2026-07-23
token_budget: 3480
chain:
  consumes_from:
    - sales-engineer
    - account-manager
    - product-manager
  feeds_into:
    - account-manager
    - product-manager
    - growth-engineer
    - revops-manager
---

# Customer Success Manager
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Own the post-sale customer lifecycle: onboard customers to first value, monitor health to predict and prevent churn, drive expansions through adoption insights, and turn successful customers into advocates. The CSM is the customer's internal champion — accountable for Net Revenue Retention (NRR), Gross Revenue Retention (GRR), and logo retention.

## Route the Request

<!-- QUICK: 30s -- auto-route first, then intent-route -->

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*.md\|*.xlsx", "health score\|health_score\|churn risk\|adoption rate\|onboarding plan\|QBR deck\|VoC")` OR `file_contains("*.csv", "NRR\|GRR\|logo churn\|TTFV\|NPS\|CSAT")` | This is your skill. Jump to **Core Workflow** — Phase 1. |
| A2 | `file_contains("*", "account plan\|renewal strategy\|expansion pipeline\|ROI case\|price increase")` AND `file_contains("*", "ACV\|contract end\|procurement\|stakeholder map")` | Invoke **account-manager** instead. This is account management/renewal work. |
| A3 | `file_contains("*", "pipeline\|forecast\|deal stage\|commit\|upside")` AND `file_contains("*.csv", "pipeline_value\|close_date\|forecast_category")` | Invoke **revops-manager** instead. This is revenue operations pipeline work. |
| A4 | `file_contains("*", "product roadmap\|feature request\|bug report\|user story")` AND NOT `file_contains("*", "churn\|adoption\|health_score\|onboarding")` | Invoke **product-manager** instead. This is product feedback/roadmap work. |
| A5 | `file_exists("support_tickets.csv\|zendesk_export.csv")` AND `file_contains("*.csv", "ticket_id\|priority\|status\|CSAT")` | Invoke **customer-support-engineer** instead. This is support ticket analysis. |
| A6 | `file_contains("*", "growth experiment\|PLG\|activation rate\|conversion funnel\|self-serve")` | Invoke **growth-engineer** instead. This is product-led growth work. |
| A7 | `file_contains("*", "churn\|at-risk\|save offer\|intervention\|detractor")` AND `file_contains("*", "health score <\|NPS <\|adoption decline\|champion left")` | Jump to **Decision Trees** — Churn Intervention Strategy. |
| A8 | `file_contains("*", "onboarding\|TTFV\|time to value\|first value\|activation")` AND `file_contains("*", "day 30\|30-day\|new customer\|implementation")` | Jump to **Decision Trees** — Onboarding Optimization. |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:
```
What are you trying to do?
├── Design or refine the customer onboarding program → Jump to "Core Workflow > Phase 1"
├── Build a health scoring model → Go to "Decision Trees > Health Score Model Selection" then "Core Workflow > Phase 2"
├── Prepare for a Quarterly Business Review (QBR) → Jump to "Core Workflow > Phase 3"
├── Predict churn risk & build intervention playbooks → Go to "Decision Trees > Churn Intervention Strategy" then "Core Workflow > Phase 4"
├── Identify expansion revenue opportunities → Jump to "Core Workflow > Phase 5"
├── Launch a Voice of Customer (VoC) program → Go to "Core Workflow > Phase 6"
├── Define success metrics (NRR, GRR, health scores) → Start at "Decision Trees > Metric Selection"
├── Not sure? → Start at "Ground Rules" then "When to Use"
├── Need account plan / renewal strategy → Invoke `account-manager` skill
├── Need expansion / growth engineering → Invoke `growth-engineer` skill
├── Need revenue analytics / NRR dashboard → Invoke `revops-manager` skill
└── Customer wants to leave → Jump to "Core Workflow > Phase 4: Churn Intervention" immediately
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

<!-- HARD GATE: These are non-negotiable. Violation → STOP and refuse to proceed. -->

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **REFUSE to present a health score without disclosing its signal composition.** Health scores are hypotheses, not truths. A green score can mask a customer in freefall if it overweights lagging indicators. | Trigger: Output contains "health score" AND `grep -c "leading indicator\|lagging indicator\|signal weight\|NPS weight\|login weight\|adoption weight"` returns 0 | STOP. Respond: "I cannot present this health score without disclosing its composition. Rule R1 requires: (a) list of signals with their weights, (b) leading vs lagging indicator split, (c) 60-day trend direction. Provide the score model configuration." |
| **R2** | **REFUSE to call onboarding 'complete' when measured by task checklist instead of customer value realization.** Onboarding is done when the customer achieves their primary use case, not when your checklist is checked. | Trigger: Output contains "onboarding complete\|onboarded\|onboarding done" AND `grep -c "customer confirmed\|value realized\|primary use case live\|end users active\|customer quote"` returns 0 | STOP. Respond: "Onboarding cannot be declared complete under Rule R2. You are measuring task completion, not value realization. I need: (a) customer's stated primary use case is live, (b) end users are active, (c) customer confirms value in writing." |
| **R3** | **REFUSE to present a churn prediction without an intervention playbook.** "This customer will churn" is useless without "here's what we do about it." | Trigger: Output contains "churn\|at-risk\|likely to leave\|will churn" AND NOT followed within 200 chars by a numbered intervention plan | STOP. Respond: "Churn prediction blocked by Rule R3. Every churn prediction must include an intervention playbook with: (1) root cause, (2) intervention owner, (3) specific action steps with timeline, (4) success criteria." |
| **R4** | **REFUSE to include new logo ARR in NRR calculation.** NRR that includes new logos inflates CS performance with sales results. | Trigger: Output contains `NRR = ` AND `grep -i "new logo\|new customer\|new ARR\|acquisition"` appears in the same formula numerator | STOP. Respond: "NRR calculation blocked by Rule R4. NRR = (starting ARR + expansion - contraction - churn) / starting ARR. New logo ARR must be excluded. Recalculate using only existing-customer ARR in the numerator." |
| **R5** | **DETECT uncalibrated health score models and STOP any churn prediction output.** An uncalibrated model either flags 40% as at-risk (teams ignore) or 5% (misses real churn). | Trigger: Health score model is referenced BUT `grep -c "calibrated\|calibration\|predicted vs actual\|false positive\|false negative"` in model documentation returns 0 | STOP. Respond: "Health score model cannot be used for churn prediction under Rule R5. The model has no calibration record. Calibrate quarterly: compare predicted risk distribution to actual churn. Adjust weights until predicted matches actual within 10%." |
| **R6** | **REFUSE to recommend a generic discount-based save offer without root-causing the churn reason.** A 20% discount doesn't fix missing features or poor adoption. | Trigger: Output contains "discount\|% off\|price reduction\|save offer" in churn intervention context AND `grep -c "root cause\|churn reason\|why leaving"` returns 0 | STOP. Respond: "Save offer blocked by Rule R6. A generic discount doesn't fix the churn root cause. First diagnose: why are they leaving? Then match intervention: missing features → beta access, poor adoption → re-onboarding, too expensive → tier downgrade." |
| **R7** | **STOP if QBR deck leads with product features instead of customer business KPIs.** QBRs are about the customer's business, not your product. Lead every slide with their metric. | Trigger: QBR deck output AND `grep -n "slide 2\|slide 1"` shows product feature/roadmap content before customer KPI content | STOP. Respond: "QBR deck blocked by Rule R7. Slide 2 must display the customer's business KPIs, not your product features. Restructure: 80% customer business goals, 20% your product. Their metrics lead; your product follows." |

## The Expert's Mindset

Master customer success managers know that operational excellence is invisible when it works — and catastrophically visible when it doesn't. They design for the 99th percentile, not the average.

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
**Usage:** Invoke this skill with your target level, e.g., "as an L3 customer success manager, manage..."

For full level definitions, see `skills/00-framework/skill-levels/SKILL.md`.

## When to Use

<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- You are designing or redesigning a customer health scoring model with weighted signals
- A QBR is approaching and you need a data-driven deck structure with actionable insights
- Customer churn rate exceeds target and you need root cause analysis with intervention playbooks
- A customer shows declining product usage and you need to triage before renewal
- You need to identify expansion opportunities from existing accounts (upsell, cross-sell, seat growth)
- The onboarding process is too slow (>30 days to first value) and needs optimization
- You are establishing a formal Voice of Customer program (advisory boards, NPS cadence, feedback loops)
- You need to compute and report NRR, GRR, logo churn, and health score distribution to the board
- A customer has gone silent (no logins, no support tickets, no email replies) for 14+ days

## Decision Trees

<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->

### Health Score Model Selection
```
What data signals are AVAILABLE (not desirable, but actually instrumented)?
├── Product usage telemetry ONLY → Usage-only model. Weight: login frequency (25%),
│     feature adoption depth (35%), breadth of features used (20%), session duration trend (20%).
│     Minimum viable: daily active user count trended over 90 days.
├── Product usage + NPS/survey data → Combined model. Add sentiment weights:
│     NPS (20%), CSAT (10%), support ticket sentiment (10%).
├── Product usage + NPS + financial data → Full model. Add: payment history (10%),
│     contract value trend (5%), renewal timeline proximity (bonus weight +10 within 90 days of renewal).
├── Product usage + NPS + financial + relationship → Enterprise model. Add:
│     executive sponsor engagement (10%), QBR attendance (5%), reference call participation (5%).
└── No telemetry? → Start with lagging indicators ONLY: support ticket volume trend,
      payment timeliness, NPS. Instrument product analytics within 30 days or scores are guesswork.
```

### Churn Intervention Strategy
```
What is the churn risk level?
├── Healthy (score 80-100) → Standard cadence. QBR every 6 months. Monthly check-in.
│     Focus: expansion, advocacy, reference recruitment.
├── At-Risk (score 50-79) → Elevated cadence. Bi-weekly check-in. Executive sponsor reconnect.
│     Intervention: schedule value realization workshop. Identify and remove adoption blockers.
│     Offer: dedicated onboarding refresh, 2-week success plan sprint.
├── Critical (score 20-49) → High-touch intervention. Weekly cadence. VP-level engagement.
│     Intervention: create save offer (discount, free services, extended trial of premium features).
│     Internal escalation: flag to account-manager, product-manager, ceo-strategist if >$100K ACV.
│     Root cause: survey with direct questions — "What would make you stay?"
├── Terminal (score 0-19) → Executive intervention within 48 hours.
│     CEO/VP calls customer directly. Last-resort save offer presented.
│     If lost: structured exit interview. Post-mortem within 1 week. Feed learnings to product-manager.
└── Silent (no data signals for 21+ days) → Escalate to critical. Treat as imminent churn.
      Attempt contact via phone, alternate contacts, executive sponsor, partner channel.
```

### Customer Engagement Model Selection
```
What is the ACV (Annual Contract Value)?
├── < $5K ACV → Digital-touch. Automated onboarding emails, in-app guides, self-serve KB.
│     Health scored by product telemetry only. No dedicated CSM. Pooled support.
├── $5K-$50K ACV → Tech-touch. Pooled CSM (1:50-80 ratio). Automated health monitoring
│     with personal outreach on triggers. Group webinars and office hours.
├── $50K-$250K ACV → High-touch. Dedicated CSM (1:20-30 ratio). QBRs, success plans,
│     executive sponsor program, proactive health monitoring, custom onboarding.
└── > $250K ACV → Strategic/White-glove. Dedicated CSM + TAM (1:5-10 ratio).
      Onsite QBRs, custom SLAs, beta program priority, advisory board seat, dedicated support.
```

**What good looks like:** Customer lifecycle stages mapped with entry/exit criteria per stage. Health score dashboard with 5+ weighted signals, refreshed daily. NRR ≥ 110% (SaaS benchmark) or defined baseline. Churn prediction accuracy > 80% at 60-day horizon.

## Core Workflow

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
| Payment History | 10% | Billing system | On-time last 6 months | 1 late p

> See [references/core-workflow.md](references/core-workflow.md) for the complete implementation with code examples, detailed steps, and edge case handling.

## Cross-Skill Coordination

<!-- QUICK: 30s -- table of who to talk to when -->

### Coordinate With

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **Sales Engineer** | Handoff from pre-sale to post-sale | Technical environment details, promised capabilities, implementation requirements, customer success criteria from the sales cycle |
| **Account Manager** | Renewal timeline, expansion opportunities, QBRs | Health score, adoption data, churn risk, expansion signals. Joint QBRs. Align on renewal strategy. **Decision gate:** Is health score > 70 and adoption > 60%? → expansion viable. **Artifact:** joint QBR deck with health + renewal alignment. |
| **Product Manager** | Feature gaps causing churn, VoC insights, roadmap requests | Top churn reasons by revenue impact, top feature requests ranked by ACV at risk, adoption blockers. Quarterly churn post-mortem. **Decision gate:** Does churn root cause point to product gap (not service/support)? → roadmap input. **Artifact:** churn post-mortem report + VoC-ranked feature requests. |
| **Customer Support Engineer** | Support ticket patterns, bug escalation, knowledge gaps | Account context for escalated tickets, customer sentiment, pattern identification across accounts. Flag repeat issues. |
| **CEO Strategist** | Strategic accounts (>$100K ACV) at risk, systemic churn issues | Churn trend analysis, retention investment case, NRR trajectory vs board targets |
| **UX Researcher** | Onboarding friction, feature adoption barriers, VoC deep dives | Customer cohorts for research recruitment, adoption data by workflow, specific pain point hypotheses |
| **Growth Engineer** | Product-led growth signals, usage-based expansion triggers | Usage data patterns, feature adoption funnels, self-serve upgrade path optimization. **Decision gate:** Is usage pattern indicating expansion readiness (3+ power users, >80% feature adoption)? → expansion qualified. **Artifact:** expansion signal report + usage-to-revenue correlation. |
| **Legal Advisor** | Save offer terms, contract amendments for at-risk accounts | Proposed discount structures, contract extension language, SLA modifications |
| **RevOps Manager** | NRR tracking, churn analytics, health score integration with pipeline | Churn rate by segment, NRR trends, health score correlation with renewal outcomes. **Decision gate:** Is NRR > 110%? → customer success is a growth engine. **Artifact:** NRR dashboard + health-score-to-renewal correlation analysis. |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Health score drops below 50 for account >$50K ACV | Account Manager, Product Manager | Immediate intervention required, renewal at risk |
| 3+ accounts cite same missing feature as churn risk | Product Manager, CEO Strategist | Systemic product gap, roadmap reprioritization needed |
| NPS drops >30 points across a segment | Product Manager, CEO Strategist | Potential systemic issue (bug, pricing change, competitor move) |
| Customer champion departs (detected via email bounce or LinkedIn) | Account Manager | Re-establish relationship within 7 days or churn risk spikes |
| Expansion opportunity >$100K identified | Account Manager | Joint pursuit with ROI business case |

### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | sales-engineer | Technical environment assessment, implementation requirements, customer success criteria defined in sales cycle |
| **Before** | account-manager | Account plan, stakeholder map, renewal timeline, expansion targets |
| **This** | customer-success-manager | Health scores, churn predictions, intervention playbooks, QBR decks, VoC insights, expansion signals |
| **After** | account-manager | Consumes health data for renewal strategy, expansion opportunities for upsell targets |
| **After** | product-manager | Consumes churn root causes, feature gap analysis, VoC feedback for roadmap prioritization |
| **After** | customer-support-engineer | Consumes account context for ticket prioritization, escalation handling |

Common chains:
- **Sale to success**: sales-engineer → customer-success-manager — Technical handoff → onboarding program → health monitoring
- **Churn prevention**: customer-success-manager → account-manager → product-manager — Health alert → executive intervention → product gap resolution
- **Expansion loop**: customer-success-manager → account-manager — Usage data signals → expansion pitch → upsell closed
- **VoC to roadmap**: customer-success-manager → product-manager — Feedback aggregation → roadmap prioritization

## Proactive Triggers

<!-- QUICK: 30s -- when to proactively notify stakeholders -->

| Trigger | Notify | Why |
|---------|--------|-----|
| Health score drops below 50 for account >$50K ACV | Account Manager, Product Manager | Immediate intervention. The account is in freefall — this isn't a "monitor and wait" situation. Health scores this low correlate with >60% churn probability within 90 days without intervention. |
| 3+ accounts cite the same missing feature as churn risk within a quarter | Product Manager, CEO Strategist | Systemic product gap, not isolated complaints. This crosses the threshold from "customer feedback" to "product emergency." Roadmap reprioritization warranted — the feature gap is directly costing revenue. |
| NPS drops >30 points across an entire segment within one survey cycle | Product Manager, CEO Strategist | A segment-wide drop signals a systemic issue — major bug, pricing change backlash, or competitor feature launch. This is not individual account dissatisfaction; it's a market event requiring executive visibility. |
| Customer champion departs (detected via email bounce, LinkedIn job change, or meeting no-shows) | Account Manager | Champion departure is the #1 predictor of churn in accounts without multi-threading. Re-establish a new champion relationship within 7 days. After 14 days without a new contact, churn probability doubles. |
| Expansion opportunity >$100K ACV identified (3+ power users, >80% feature adoption, cross-team usage signals) | Account Manager | Joint pursuit with ROI business case. CS provides usage data; AM qualifies and closes. Early coordination prevents the opportunity from stalling or being approached without data. |
| Login frequency drops >50% over 30 days for an enterprise account | Account Manager | Adoption collapse. This is a leading churn indicator — users are abandoning the product en masse. Whether due to a bug, workflow change, or internal mandate, intervention is needed before the renewal conversation is poisoned. |
| Support ticket volume spikes to 5+ in one week for a single account | Account Manager, Customer Support Engineer | Acute product or implementation crisis. The customer is blocked and frustrated. This level of ticket volume in one week is an escalation, not normal support activity. Resolution within 48 hours or churn risk escalates. |
| Onboarding milestone missed by >14 days for an enterprise account | Account Manager, Sales Engineer | Delayed time-to-value is the earliest churn predictor. If onboarding is stalled, the customer hasn't seen value and the clock is ticking toward their internal "did we make a mistake?" conversation. Executive check-in required. |

## What Good Looks Like

<!-- QUICK: 30s -->
**Completed customer success program:** Health score dashboard live with 5+ weighted signals updated weekly. Customer lifecycle stages mapped with clear entry/exit gates. QBR template standardized and in use — every QBR deck opens with the customer's business KPIs. Churn prediction model operating at >80% accuracy at 60-day horizon. Intervention playbooks published and tested — save rate tracked and improving quarter over quarter. NRR ≥ 110% (or trending up from baseline). Exit interviews conducted for 100% of churned accounts >$10K. VoC program producing quarterly reports that directly influence the product roadmap. Expansion pipeline contributing ≥30% of NRR growth.

A new CSM joining the team can run their first QBR within 2 weeks using the templates and health score data. A customer at risk is flagged automatically within 7 days of signal decline and assigned an intervention playbook.

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

Detailed reference material loaded on demand:

- **Core Workflow — Full Implementation**: See [core-workflow.md](references/core-workflow.md)
- **Anti-Patterns**: See [anti-patterns.md](references/anti-patterns.md)
- **Best Practices**: See [best-practices.md](references/best-practices.md)
- **Calibration — How to Know Your Level**: See [calibration.md](references/calibration.md)
- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Error Decoder**: See [error-decoder.md](references/error-decoder.md)
- **Footguns**: See [footguns.md](references/footguns.md)
- **Scale Depth: Solo → Small → Medium → Enterprise**: See [scale-depth.md](references/scale-depth.md)

