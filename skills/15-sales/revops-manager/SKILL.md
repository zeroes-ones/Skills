---
<!-- DEEP: 10+min -->

<!-- DEEP: 10+min -->

<!-- DEEP: 10+min -->

<!-- DEEP: 10+min -->

<!-- DEEP: 10+min -->

<!-- DEEP: 10+min -->

name: revops-manager
description: Revenue Operations leadership — pipeline analytics with funnel stage conversion rates, velocity metrics, pipeline coverage ratios, cohort analysis, and forecasting models CRM strategy for HubSpot/Salesforce
  architecture including custom objects for health-tech (patient accounts, provider accounts, pharma partners), automation rules, and data hygiene territory planning with account segmentation (geographic,
  therapeutic area, HCP vs patient), territory assignment logic, capacity planning, and quota setting attribution modeling with first-touch, last-touch, multi-touch, and custom weighting for health-tech
  buying cycles covering marketing-sourced vs sales-sourced pipeline compensation design including commission structures, SPIFF programs, accelerator tiers, clawback policies, and plan modeling and rollouts
  tech stack integration with CRM to marketing automation to customer success platform to billing, data flow mapping, and integration health monitoring revenue forecasting across weekly, monthly, and quarterly
  cadences with pipeline inspection, commit vs best-case methodology, risk flagging, and forecast accuracy tracking deal desk operations covering quoting process, discount approval workflows, contract review
  routing, and non-standard terms escalation revenue analytics including ARR and MRR tracking, NRR and GRR, LTV:CAC by segment, logo vs expansion split, and churn and contraction analysis sales process
  optimization with stage definition, exit criteria, deal inspection, and win/loss analysis integration. Use when designing revenue operations strategy, building forecasting models, optimizing CRM architecture,
  designing compensation plans, or standing up a deal desk function.
author: Sandeep Kumar Penchala
type: sales
status: stable
version: 1.0.0
updated: 2026-07-21
tags:
- revops
- revenue-operations
- pipeline-analytics
- crm-strategy
- attribution-modeling
- compensation-design
- forecasting
- sales-operations
token_budget: 4000
output:
  type: code
  path_hint: ./
chain:
  consumes_from:
  - account-manager
  - analytics-engineer
  - business-intelligence-engineer
  - customer-success-manager
  - demand-generation
  - fp-and-a-analyst
  - growth-engineer
  - marketing-manager
  - sales-engineer
  feeds_into:
  - fp-and-a-analyst
  - growth-engineer
  - marketing-manager
  - sales-engineer
---
# RevOps Manager (Revenue Operations)

Own the revenue engine end-to-end: architect the CRM, design the forecasting model, build the territory plan, model compensation, run the deal desk, and connect every system in the tech stack so revenue moves predictably from pipeline to cash.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->

```
What are you trying to do?
|-- Build a forecasting model -> Jump to "Core Workflow > Phase 1: Forecasting Cadence"
|-- Design compensation plans -> Go to "Decision Trees > Compensation Architecture"
|-- Optimize pipeline analytics -> Jump to "Core Workflow > Phase 2: Pipeline Analytics"
|-- Configure CRM architecture -> Go to "Decision Trees > CRM Object Design"
|-- Set up territory assignments -> Jump to "Core Workflow > Phase 3: Territory Planning"
|-- Implement attribution modeling -> Go to "Decision Trees > Attribution Model Selection"
|-- Stand up a deal desk -> Jump to "Core Workflow > Phase 5: Deal Desk Operations"
|-- Map tech stack integrations -> Go to "Decision Trees > Integration Health"
|-- Run revenue analytics (ARR/NRR/LTV) -> Jump to "Core Workflow > Phase 4: Revenue Analytics"
|-- Diagnose a forecast miss -> Go to "Error Decoder"
|-- Audit CRM data hygiene -> Jump to "Best Practices > Data Quality"
|-- Need demand gen campaign performance data -> Invoke `demand-generation` skill
|-- Need sales cycle / demo conversion data -> Invoke `sales-engineer` skill
|-- Need financial model / budget projections -> Invoke `fp-and-a-analyst` skill
|-- Need growth experiments / CRO data -> Invoke `growth-engineer` skill
```

## Ground Rules — Read Before Anything Else
<!-- STANDARD: 3min -->

These rules apply to *every* response this skill produces.

- **Never forecast revenue you cannot inspect.** Every commit number in the forecast must trace back to a specific deal, a specific stage, and a specific rep. Pipeline-as-forecast is not forecasting -- it is hope.
- **Always model comp plans in a spreadsheet with 3 scenarios before presenting to leadership.** Run the plan against last year's actuals. If a rep earning 120 percent of quota costs more than 2x their base, the plan is broken -- fix the accelerators.
- **Never build a custom CRM object without defining de-duplication rules, required fields, and the integration touchpoints first.** Custom objects without governance become garbage repositories within 90 days.
- **Always lag 2 quarters when measuring attribution.** Health-tech buying cycles run 6-18 months. Attribution models run on 90-day windows will misattribute 40-60 percent of pipeline -- you will cut programs that are actually working.
- **Never approve a non-standard discount without a written business case from the AE that includes: strategic value, precedent risk, and competitive context.** Discounts without documentation teach the field that everything is negotiable -- and they will test every boundary.

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->

- The CFO asks for a bottoms-up revenue forecast by segment, by quarter, with commit vs best-case splits
- The CRO wants territory redesign -- geographic realignment, therapeutic area specialization, or capacity rebalancing
- The board asks for pipeline coverage ratios, velocity metrics, and cohort conversion trends for the QBR
- Sales leadership is designing next year's compensation plan and needs SPIFFs, accelerators, and clawback modeling
- A new acquisition means CRM instance consolidation -- object mapping, data migration, and automation migration
- Attribution is being debated -- marketing claims 70 percent sourced, sales claims 80 percent self-sourced
- Deal velocity is slowing at a specific funnel stage -- need to diagnose with stage-by-stage conversion analytics
- A deal desk needs to be formalized -- quoting rules, discount approval matrix, contract review routing
- The tech stack has grown organically -- CRM, MAP, CSP, billing -- and no one knows the full data flow
- ARR growth is strong but NRR is soft -- need expansion vs logo retention analysis

## Decision Trees
<!-- DEEP: 5-10min -- structured decisions with trade-offs, not a flat list -->

### Compensation Architecture

```
What is the primary revenue motion?
|-- High-velocity transactional (less than $25K ACV, under 30-day cycle)
|   |-- OTE split: 50/50 base/variable
|   |-- Commission: flat rate per deal, paid monthly
|   |-- Accelerators: over 100% quota -> 1.5x rate, over 120% -> 2x rate
|   |-- Clawback: 90-day window for churned logos
|
|-- Mid-market ($25K-$100K ACV, 30-90 day cycle)
|   |-- OTE split: 60/40 base/variable
|   |-- Commission: tiered rate by deal size (under $50K: 8%, $50K-$100K: 10%)
|   |-- Accelerators: over 100% -> 1.5x, over 120% -> 2x, over 150% -> 2.5x
|   |-- SPIFFs: $1K per new logo in a named target account list
|   |-- Clawback: 6-month window if logo churns within 3 months
|
|-- Enterprise (over $100K ACV, 90-180+ day cycle)
    |-- OTE split: 70/30 base/variable
    |-- Commission: percentage of ACV with ramps (5% on first $250K, 7% beyond)
    |-- Accelerators: over 100% -> 1.3x, over 120% -> 1.8x, over 150% -> 2.5x, over 200% -> 3x
    |-- Multi-year deals: full year-1 commission at signing, 50% year-2 at renewal trigger
    |-- SPIFFs: $5K bonus for deals over $500K with C-suite involvement
    |-- Clawback: 12-month window, pro-rated monthly
```

### CRM Object Design

```
What is the core entity being managed?
|-- Healthcare Provider (HCP) Account
|   |-- Custom objects: Credentialing Record, Formulary Access, Payer Contract
|   |-- Required fields: NPI number, specialty, prescribing volume tier, therapeutic area
|   |-- De-dupe: NPI number + practice address as unique key
|   |-- Automation: auto-route to territory owner based on practice ZIP + therapeutic area
|
|-- Patient Account (DTC model)
|   |-- Custom objects: Enrollment Record, Treatment Journey, Insurance Verification
|   |-- Required fields: patient ID (de-identified), condition, enrollment date, payer
|   |-- De-dupe: patient ID + condition + date of birth year
|   |-- Automation: auto-flag for CS handoff at treatment milestone completion
|
|-- Pharma Partner Account
    |-- Custom objects: Co-Pay Program, Hub Services Agreement, Data Sharing Schedule
    |-- Required fields: partner company name, contract type, agreement end date, MSL contact
    |-- De-dupe: company name + agreement type
    |-- Automation: auto-notify 90 days before contract expiration
```

### Attribution Model Selection

```
What question are you answering?
|-- "Which channel first brought this account in?"
|   |-- First-Touch Attribution -- use for brand awareness campaign ROI, TAM expansion programs
|
|-- "Which touchpoint closed the deal?"
|   |-- Last-Touch Attribution -- use for bottom-of-funnel conversion optimization, SDR comp attribution
|
|-- "How do all touchpoints contribute across the journey?"
|   |-- Linear Multi-Touch -- equal weight to every touch, use as baseline sanity check
|   |-- Time-Decay -- weight increases closer to close, use for 60-90 day sales cycles
|   |-- U-Shaped -- 40% first touch, 40% lead conversion, 20% distributed, use for ABM programs
|   |-- W-Shaped -- 30% first touch, 30% lead conversion, 30% opportunity creation, 10% distributed
|       |-- **Recommended for health-tech**: accounts for long buying cycles with multiple key milestones
|
|-- "What is the custom weighting for our unique buying cycle?"
    |-- Custom Weighted -- define milestones (initial inquiry, demo, clinical evaluation, procurement, close)
        |-- Health-tech model: 15% first touch, 10% demo, 25% clinical evaluation, 20% procurement, 30% close
        |-- Rationale: clinical evaluation is the highest-friction gate in health-tech; procurement weight reflects legal/compliance review lift
```

### Integration Health Check

```
Which integration is suspect?
|-- CRM <-> Marketing Automation (HubSpot <-> Marketo / Salesforce <-> Pardot)
|   |-- Sync check: lead-to-contact conversion rate under 90% -> investigate field mapping
|   |-- Latency check: campaign membership sync over 5 minutes -> batch vs real-time config
|   |-- Hygiene check: bounced emails in CRM over 2% -> re-engagement or purge needed
|
|-- CRM <-> Customer Success (Salesforce <-> Gainsight / HubSpot <-> Vitally)
|   |-- Sync check: account health score not updating within 24 hours -> API throttle or field mapping
|   |-- Handoff check: new closed-won opportunities not creating CS playbooks -> workflow trigger gap
|   |-- NRR feed: expansion/renewal data flowing back to CRM opportunity records within 48 hours
|
|-- CRM <-> Billing (Salesforce <-> Zuora / HubSpot <-> Stripe)
    |-- Sync check: closed-won opp to subscription creation under 1 hour -> provisioning delay risk
    |-- ARR truth check: CRM ARR vs billing system ARR within 2% variance -> reconciliation gap
    |-- Churn feed: cancelled subscriptions updating CRM within 24 hours -> forecast accuracy impact
```

## Core Workflow
<!-- DEEP: 15-30min -- full end-to-end workflow -->

<!-- DEEP: 10+min -->

### Phase 1: Revenue Forecasting Cadence

**Weekly Pulse**
1. Pull current pipeline by rep, stage, and close date from CRM
2. Flag deals stuck in stage over 2x average stage duration -- schedule AE inspection
3. Identify deals pulled in or pushed out since last week -- log reason codes (timing, budget, competition, scope)
4. Update commit file: deals the AE says "will close this quarter" with over 80% confidence
5. Compare commit total to quota gap -- surface coverage risk immediately

**Monthly Forecast Roll-Up**
1. Aggregate weekly pulses into monthly view with commit + best-case totals
2. Calculate weighted pipeline: each deal x stage probability x AE confidence adjustment
3. Run cohort analysis: compare this month's forecast shape (stage distribution, age distribution) to prior months that converted
4. Flag: deals with over 3 push-outs ("slipping sand") -- escalate to CRO
5. Publish forecast accuracy score: last month's commit vs actual, best-case vs actual

**Quarterly Forecast Package (for Board/CEO)**
1. Bottoms-up: roll up monthly forecasts, adjusted for seasonal patterns (Q4 in health-tech = strong close, Q1 = slow start)
2. Tops-down: market TAM x penetration rate x expansion rate as sanity check
3. Risk adjustment: apply historical slippage rate by segment (enterprise typically 15-20% slippage, SMB 5-10%)
4. Scenario modeling: base case, upside (+15%), downside (-20%) with trigger assumptions
5. Pipeline coverage check: 3x coverage at start of quarter minimum; under 2.5x -> demand gen acceleration needed

<!-- DEEP: 10+min -->

### Phase 2: Pipeline Analytics

**Funnel Conversion Dashboard**
1. Define stages: Inquiry -> MQL -> SQL -> Demo -> Negotiation -> Closed-Won
2. Calculate conversion rates: stage N -> stage N+1 as percentage
3. Calculate stage velocity: average days in each stage
4. Segment by: geo, therapeutic area, deal size band, AE tenure, lead source
5. Identify bottleneck stage: where both conversion rate AND velocity are below benchmark

**Pipeline Coverage Ratios**
1. Calculate: total open pipeline / quota for the period
2. Segment coverage: early-stage (over 90 days out) vs late-stage (under 30 days out)
3. Waterfall analysis: how much pipeline must be created vs already exists
4. Cohort trend: coverage ratio trend over last 6 quarters -- is it improving or degrading?

**Cohort Analysis**
1. Group opportunities by creation quarter
2. Track: how many convert, average deal size, average cycle length, win rate
3. Compare cohorts: Q1-2026 vs Q1-2025 -- is time-to-close increasing? Win rate declining?
4. Surface leading indicators: cohorts with over 30% of deals in "stalled" status after 6 months

<!-- DEEP: 10+min -->

### Phase 3: Territory Planning

**Account Segmentation**
1. Tier accounts: Strategic (top 50), Enterprise (next 200), Mid-Market (next 500), SMB (remainder)
2. Segmentation criteria: current revenue + TAM potential + therapeutic area alignment
3. Assign ownership: named account reps (Strategic), pod-based (Enterprise), pooled (Mid-Market), inbound (SMB)
4. Validate: no account assigned to over 1 rep; no rep with over 30 named accounts

**Territory Assignment Logic**
1. Geographic: ZIP-based routing for field reps with territory boundaries defined by travel radius
2. Therapeutic area: specialty-based routing -- oncology vs cardiology vs rare disease
3. HCP vs Patient: separate motions -- HCP sales (prescriber education) vs DTC (patient enrollment)
4. Capacity check: each rep's territory TAM / quota target -> if over 5x, territory needs splitting
5. Vacancy planning: unassigned territories covered by float pool or adjacent rep with temporary 1.2x accelerators

**Quota Setting**
1. Tops-down: company revenue target / number of reps = average quota
2. Bottoms-up: territory TAM x expected penetration x average deal size = territory-level quota
3. Adjust for: rep tenure (ramp quota for first 2 quarters), territory maturity (new vs established), seasonal factors
4. Fairness check: quota distribution -- under 20% variance between same-tier territories

<!-- DEEP: 10+min -->

### Phase 4: Revenue Analytics

**ARR/MRR Tracking**
1. New logo ARR: sum of ACV from new customers this period
2. Expansion ARR: upsell + cross-sell from existing customers
3. Contraction: downgrades and partial churn
4. Churn ARR: full logo losses
5. Net New ARR = New + Expansion - Contraction - Churn

**NRR/GRR Calculation**
1. GRR (Gross Revenue Retention): (Starting ARR - Churn ARR - Contraction ARR) / Starting ARR -> target over 90%
2. NRR (Net Revenue Retention): (Starting ARR - Churn - Contraction + Expansion) / Starting ARR -> target over 110%
3. Segment NRR: enterprise vs SMB -- if SMB NRR under 90% with over 110% enterprise NRR, SMB GTM needs restructuring
4. Logo retention rate: logos retained / starting logos -> target over 85%

**LTV:CAC by Segment**
1. LTV = average ARR per customer x gross margin / churn rate
2. CAC = total sales + marketing spend / new logos acquired
3. Target: LTV:CAC over 3:1 for enterprise, over 5:1 for SMB (lower CAC per logo)
4. Payback period: CAC / monthly gross margin per customer -> target under 18 months

**Churn & Contraction Analysis**
1. Churn by reason code: price, product gap, competitor, bankrupt/acquired, no decision-maker
2. Churn by cohort: which acquisition cohort churns most? (indicates sales qualification or onboarding issues)
3. Contraction tracking: logo stays but ARR drops -- typically early warning of eventual full churn
4. Save rate: what percentage of at-risk accounts are saved by CS intervention -- measure CS effectiveness

<!-- DEEP: 10+min -->

### Phase 5: Deal Desk Operations

**Quoting Process**
1. AE submits quote request with: products, quantities, discount request, term length
2. Deal desk validates: products in price book, discount within AE authority level, terms standard
3. For non-standard discounts: AE attaches business case (strategic value, precedent risk, competitive context)
4. Approval routing: AE authority (under 15% off list) -> Sales Manager (under 25%) -> VP Sales (under 35%) -> CRO (under 50%) -> CEO (over 50%)
5. SLA: standard quotes approved within 4 hours, non-standard within 24 hours

**Contract Review Routing**
1. Standard contract (pre-approved terms): auto-generated from template, no legal review
2. Non-standard terms requested (SLA changes, liability caps, IP clauses, data residency): route to Legal
3. Security review required (prospect sends security questionnaire): route to Security Engineer
4. Procurement terms (payment terms, PO requirements, vendor registration): route to Finance
5. SLA: standard contracts same-day, legal review within 3 business days, security review within 5 business days

**Non-Standard Terms Escalation**
1. AE logs non-standard term request with justification
2. Deal desk triages: does request align with any existing precedent? If yes, apply precedent pricing and approve at appropriate level
3. If no precedent: CRO + CFO review for revenue recognition and margin impact; Legal review for contractual risk
4. Decision documented in deal record with rationale -- builds precedent library for future requests
5. Track: non-standard deal volume, discount depth, and win rate -- if over 20% of deals are non-standard, price book is wrong

<!-- DEEP: 10+min -->

### Phase 6: Sales Process Optimization

**Stage Definition & Exit Criteria**
1. Each stage has: definition, required activities, exit criteria, and maximum dwell time
2. Example -- Demo stage: demo completed, technical decision-maker present, MEDDIC score updated, exit: next step scheduled within 5 days
3. Stage enforcement: cannot advance without required fields populated in CRM
4. Stale opportunity rules: over 2x average dwell time -> auto-flag for manager inspection, over 3x -> auto-move to "stalled" with re-engagement playbook

**Deal Inspection Cadence**
1. Weekly 1:1: AE and manager inspect top 5 deals -- stage, next step, risk, MEDDIC score
2. Bi-weekly pipeline review: manager and director inspect all deals over $50K -- commit confidence, competitive presence, multi-threading status
3. Monthly forecast call: CRO reviews all commit deals with VPs -- challenge every deal not advanced in 2 weeks

**Win/Loss Analysis Integration**
1. Within 48 hours of deal outcome: AE completes win/loss form (why won/lost, competitor, decision criteria)
2. Monthly aggregation: win/loss patterns by competitor, by stage lost, by AE, by segment
3. Quarterly deep dive: external win/loss interview firm conducts 10-15 interviews for unbiased analysis
4. Feedback loop: win/loss insights -> product roadmap (product gaps), marketing (positioning adjustments), sales enablement (battle cards)

## Best Practices
<!-- STANDARD: 3min -->

- **Run forecast accuracy retro every quarter.** Compare commit vs actual by rep, by segment, by geo. Reps with under 70% accuracy need coaching on deal inspection. Reps with over 95% accuracy are sandbagging -- their quota is too low.
- **CRM data hygiene is a revenue function, not an IT function.** Appoint a data steward with weekly audit cadence. Track: duplicate rate, empty required fields, stale opportunities (over 90 days no activity), and contact decay (bounced emails, left-company rates).
- **Model comp plans in a live spreadsheet that leadership can play with.** Variables (OTE ratio, accelerator tiers, SPIFF amounts, clawback windows) should be adjustable with real-time cost impact. This prevents "can we just add a SPIFF?" from becoming an untested experiment.
- **Never let attribution become a marketing-vs-sales debate.** Present all models side-by-side with the same pipeline data. The W-shaped model is typically the most balanced starting point for health-tech. Agree on the model before measuring -- changing the model mid-year invalidates all trend analysis.
- **Treat the deal desk as a revenue accelerator, not a revenue blocker.** Publish approval SLAs and track compliance monthly. If average approval time exceeds SLA, add deal desk headcount or increase AE discount authority.
- **Revenue analytics dashboards must have a single source of truth.** Reconcile CRM ARR vs billing ARR monthly. Any gap over 2% triggers an immediate root cause analysis. Dual sources of ARR truth will erode board and investor confidence within 2 quarters.

## Anti-Patterns
<!-- STANDARD: 3min -- patterns that predictably fail -->

| Anti-Pattern | Why It Fails | Correct Approach |
|---|---|---|
| Accepting forecast commits without deal-level inspection | Reps over-commit to look good; forecast accuracy drops below 70%. Board presentations become fiction | Implement mandatory deal inspection on all commit deals. Every commit number must trace to a specific deal with a named rep, verified stage, and validated close date. Run forecast accuracy retro quarterly |
| Treating pipeline coverage ratio as meaningful without auditing pipeline quality | 4x coverage of unqualified leads creates false confidence. Reps work bad deals instead of hunting, and the quarter misses despite "healthy" coverage | Gate pipeline entry with BANT/MEDDIC qualification. Purge deals with no activity in 30 days. Coverage ratio only matters when the pipeline is real — audit quality before citing coverage |
| Reporting NRR as a single aggregate number without segmenting by customer cohort | A 115% NRR can hide 85% logo retention if a few large accounts are expanding. Concentration risk is invisible in the aggregate | Segment NRR by customer size decile, by segment, and by cohort. If top 10% of customers drive over 50% of expansion, flag concentration risk. Report NRR and logo retention side by side |
| Modeling new comp plans without running them against prior year actuals | Accelerators that look reasonable in a spreadsheet produce 30%+ cost overruns when applied to real deal distribution | Always back-test comp plans against prior year actuals before launch. Cap accelerators at 3x quota. If over 40% of reps would have exceeded 120% under the new plan, re-benchmark |
| Blaming CRM adoption on rep training instead of workflow design | If the CRM is a data-entry burden that doesn't help reps sell, no amount of training will fix adoption. Reps build shadow spreadsheets | Shadow top reps for a week. Remove all fields not used in pipeline meetings. Automate data capture from email/calendar. CRM must be a selling tool, not a reporting tool |
| Allowing the attribution debate to become a marketing-vs-sales political fight | Changing models mid-year invalidates all trend analysis. Teams argue about methodology instead of acting on pipeline data | Agree on one attribution model, lock it for 12 months. Present all models side-by-side for internal learning, but plan against the locked model. The CRO arbitrates if there's a dispute |
| Letting the deal desk become a bottleneck with no SLA tracking | Deals stall in approval, AEs lose momentum, and revenue velocity drops. Nobody knows how bad it is because nobody measures it | Publish approval SLAs: standard deals <4 hours, non-standard <24 hours. Track compliance monthly. If SLA is breached, either increase AE discount authority or add deal desk headcount |
| Running territory planning as an annual exercise with no quarterly validation | Territories calcify. High-growth accounts outgrow their segment, new logos go unassigned, and coverage gaps widen silently | Validate territory assignments quarterly. Check: no unassigned strategic accounts, no rep with >30 named accounts, territory variance <20% for same-tier reps. Adjust boundaries before the quarter starts |

## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **Sales Engineer** | Demo-to-close conversion rate declining, technical win rate trending down, PoC success criteria not aligning with close outcomes | Pipeline analytics by stage, win/loss patterns, demo environment stability impact on close rates. **Decision gate:** Is technical win rate > 40%? → sales process healthy. **Artifact:** technical win/loss analysis by deal stage. |
| **Marketing Manager** | Attribution debate, campaign ROI measurement, lead scoring model design, ABM program measurement | Attribution model outputs by campaign, pipeline sourced vs influenced splits, conversion rates by lead source. **Decision gate:** Is attribution model locked for 12 months? → report consistently. **Artifact:** attribution model documentation + quarterly report. |
| **Customer Success Manager** | NRR declining, churn rate increasing, expansion pipeline not materializing, handoff friction from sales to CS | Account health scores, churn reason codes, expansion opportunity identification, onboarding completion rates |
| **FP&A Analyst** | Building annual operating plan, quota setting, comp plan cost modeling, board reporting package | Revenue forecast data, pipeline coverage ratios, comp plan cost projections, ARR bridge analysis. **Decision gate:** Is forecast accuracy > 80% for 2+ months? → board deck ready. **Artifact:** quarterly board package with forecast accuracy metrics. |
| **CEO Strategist** | Quarterly board deck preparation, annual planning, strategic initiative ROI analysis, M&A integration planning | Forecast accuracy data, NRR/GRR trends, LTV:CAC by segment, pipeline coverage trends, territory performance |
| **Business Strategist** | Market entry modeling, new product line revenue projections, pricing strategy impact analysis, competitive displacement tracking | TAM analysis inputs, win/loss data by competitor, pricing elasticity data from deal desk, segment profitability |
| **BizDev Manager** | Channel partnership revenue tracking, co-sell pipeline attribution, partner-sourced vs partner-influenced measurement | Partner pipeline data, channel commission structures, co-sell deal registration tracking |
| **Demand Generation** | Pipeline coverage gaps, lead quality trends, conversion rate drops at MQL-to-SQL, campaign budget allocation | Conversion rates by channel and campaign, pipeline coverage waterfall, lead scoring effectiveness. **Decision gate:** Is pipeline coverage > 3x for next quarter? → demand gen pacing healthy. **Artifact:** pipeline coverage waterfall report. |
| **Analytics Engineer** | Data pipeline for attribution, CRM data quality, dashboard refreshes | Event taxonomy, data freshness requirements, attribution data model. **Decision gate:** Is CRM-to-billing ARR variance < 2%? → single source of truth. **Artifact:** data quality dashboard + pipeline health report. |
| **Growth Engineer** | CRO experiment impact on pipeline, A/B test results affecting conversion rates, PLG signals | Experiment results, conversion rate changes, PLG funnel data. **Decision gate:** Did experiment produce statistically significant pipeline lift? → scale. **Artifact:** experiment results with pipeline impact analysis. |

### Communication Triggers -- When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Forecast accuracy drops below 80% for 2 consecutive months | CEO Strategist + CRO | Board credibility at risk; root cause analysis required within 1 week |
| NRR drops below 100% for any quarter | CEO Strategist + Customer Success Manager + CFO | Company is shrinking on a same-customer basis; retention strategy emergency |
| Pipeline coverage falls below 2.5x | Demand Generation + Marketing Manager + CRO | Insufficient pipeline to hit plan; demand gen acceleration needed |
| Deal velocity increases over 30% at any stage without process change | Sales Engineer + Sales Leadership | Possible stage skipping or qualification shortcuts -- quality risk |
| Non-standard deals exceed 25% of quarterly volume | CEO Strategist + FP&A Analyst + Legal Advisor | Pricing discipline breakdown; discounting culture forming |
| CRM <-> billing ARR variance exceeds 2% | FP&A Analyst + CFO | Dual source of truth emerging; investor reporting integrity at risk |
| Rep ramp time exceeds 6 months (enterprise) or 3 months (SMB) | VP Sales + People Ops | Hiring profile or onboarding process mismatch; cost of delayed productivity |

### Escalation Path

```
Forecast miss over 15% of quarterly target -> CEO Strategist + CFO + CRO
NRR under 95% for 2 consecutive quarters -> CEO Strategist + Customer Success Manager + CFO
Pipeline coverage under 2x -> Demand Generation + Marketing Manager + CRO
Non-standard deal over 50% discount -> CRO + CFO + CEO Strategist
CRM hygiene score under 70% -> VP Sales + CRO (halt all automation until data quality restored)
Attribution model dispute between marketing and sales -> CEO Strategist (arbitrate model selection, lock for 12 months)
```

### Cross-Skills Integration

```bash
# Chain: fp-and-a-analyst -> revops-manager -> ceo-strategist
# Board reporting: fp-and-a-analyst provides financial model -> revops-manager layers pipeline + NRR + forecast data -> ceo-strategist presents board narrative

# Chain: marketing-manager -> revops-manager -> sales-engineer
# Campaign attribution: marketing-manager defines campaign structure -> revops-manager applies attribution model -> sales-engineer adjusts demo approach based on source performance

# Chain: customer-success-manager -> revops-manager -> business-strategist
# NRR optimization: customer-success-manager identifies churn patterns -> revops-manager quantifies revenue impact and segments by cohort -> business-strategist adjusts market positioning

# Chain: bizdev-manager -> revops-manager -> fp-and-a-analyst
# Partner economics: bizdev-manager defines partner program -> revops-manager models commission impact and pipeline attribution -> fp-and-a-analyst validates unit economics
```

## Proactive Triggers
<!-- QUICK: 30s -- when to proactively notify stakeholders -->

| Trigger | Notify | Why |
|---------|--------|-----|
| Forecast accuracy drops below 80% for 2 consecutive months | CEO Strategist, CRO, CFO | Board credibility at risk; root cause analysis required within 1 week. Commit inspection discipline has broken down |
| NRR drops below 100% for any quarter | CEO Strategist, Customer Success Manager, CFO | Company is shrinking on a same-customer basis; retention strategy emergency. Segment immediately by cohort to identify where churn is concentrated |
| Pipeline coverage falls below 2.5x for the current quarter | Demand Generation, Marketing Manager, CRO | Insufficient pipeline to hit plan; demand gen acceleration needed. Run pipeline gap analysis by segment and geo within 48 hours |
| CRM-to-billing ARR variance exceeds 2% in monthly reconciliation | FP&A Analyst, CFO | Dual source of truth emerging; investor and board reporting integrity at risk. Root cause must be identified and resolved before month-end close |
| Non-standard deals exceed 25% of quarterly deal volume | CEO Strategist, FP&A Analyst, Legal Advisor, CRO | Pricing discipline breakdown; discounting culture forming. Audit non-standard deal log for patterns and tighten approval criteria |
| Rep ramp time exceeds 6 months (enterprise) or 3 months (SMB) for 2+ consecutive hires | VP Sales, People Ops | Hiring profile or onboarding process mismatch; cost of delayed productivity compounds. Audit recent hires for common failure patterns |
| Deal desk average approval time exceeds SLA for 2 consecutive months | CRO, VP Sales | Revenue velocity bottleneck; deals stalling in approval. Either increase AE discount authority or add deal desk headcount |
| Win/loss analysis reveals same competitor winning with same objection across 5+ deals in a quarter | Product Manager, Marketing Manager, Sales Engineer | Systemic competitive vulnerability; product gap or positioning weakness being exploited. Battle card refresh and roadmap escalation |

## Scale Depth: Solo → Small → Medium → Enterprise
<!-- DEEP: 10+min -- how this skill changes as the company grows -->

### Solo
Spreadsheet + basic CRM, manual reporting. Track deals, survive. Founder updates a pipe spreadsheet; no automation; gut-feel forecasting. The entire revenue operation lives in one person's head — the first priority is getting data into a CRM.

### Small Team
First RevOps hire, CRM administration, basic dashboards. Clean data, reliable reporting. CRM is source of truth; dashboards for leadership; sales process defined. Forecasting moves from gut-feel to data-informed with basic pipeline stage tracking.

### Medium Team
Dedicated RevOps team, full tech stack, forecasting. Optimize the revenue engine. HubSpot/Salesforce mastery; territory design; comp plans; attribution. The revenue engine has dedicated analytics, systems, and strategy resources running as a coordinated team.

### Enterprise
RevOps platform org (systems, analytics, enablement, strategy). Revenue as a science. Multi-product, multi-geo; AI forecasting; revenue platform architecture. RevOps is an independent function reporting to the CRO with mature processes and predictive capabilities.

### Transition Triggers
- **Solo → Small Team:** Revenue exceeds $5M ARR or forecasting with spreadsheets creates >15% error consistently.
- **Small Team → Medium Team:** Revenue exceeds $20M ARR or sales headcount exceeds 30 reps requiring dedicated systems and analytics resources.
- **Medium Team → Enterprise:** Multi-product or multi-geo revenue operations require a platform team with specialized roles.


## What Good Looks Like
<!-- STANDARD: 3min -->

- **Forecast accuracy**: 90%+ within 5% of commit; 85%+ within 10% of best-case on a 90-day rolling average
- **Pipeline coverage**: 3x-4x at all times, measured weekly; early-stage pipeline over 60% of total
- **NRR**: over 110% for enterprise, over 100% for SMB; GRR over 90% across all segments
- **Deal desk SLA**: 95%+ of standard deals approved within 4 hours; 90%+ of non-standard within 24 hours
- **CRM data hygiene**: duplicate rate under 1%, required field completion over 98%, stale opportunities purged weekly
- **Comp plan adoption**: under 5% of reps on guarantee; rep satisfaction survey over 4.0/5.0 on comp fairness

## Error Decoder
<!-- DEEP: 10+min -- each row is a real revops failure that misled the business or blew up the forecast -->

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Forecast consistently 20%+ above actuals | Reps over-committing; no inspection discipline; stage probabilities inflated | Implement mandatory deal inspection on all commit deals; adjust stage probabilities using 12-month actual conversion data | Forecast accuracy above 80% requires deal inspection discipline, not hope. A commit number that can't be traced to a specific deal with a specific rep is not a forecast — it's a wish. |
| Pipeline coverage is 4x but win rate is declining | Coverage is inflated by unqualified leads; reps working bad deals instead of hunting | Tighten MQL-to-SQL criteria; implement BANT/MEDDIC gating before pipeline entry; purge deals with no activity in 30 days | Coverage ratio is meaningless if the pipeline is full of bad deals. 4x coverage of unqualified leads is worse than 2x coverage of real opportunities — the first creates false confidence, the second drives real action. |
| NRR is 115% but logo retention is 85% | Expansion in a few large accounts masking broad-based logo churn; concentration risk | Segment NRR by customer size decile; if top 10% of customers drive over 50% of expansion, diversify base | A headline NRR of 115% can hide a logo churn crisis. The aggregate number masks concentration risk — a few big accounts expanding can paint a rosy picture while the base erodes underneath. |
| Comp plan costs exceed budget by 30% | Accelerator tiers too generous; quota attainment distribution skewed high | Model plan against last year actuals before launch; cap accelerators at 3x; re-benchmark quotas if over 40% of reps above 120% | Always model new comp plans against prior year actuals before launch. Accelerators that look reasonable in the boardroom can produce 30% cost overruns when applied to real deal distribution. |
| CRM adoption is low -- reps work from spreadsheets | CRM is a data-entry burden, not a workflow tool; fields do not match how reps sell | Shadow top reps for a week; remove all fields not used in pipeline meetings; automate data capture from email/calendar | CRM adoption is a workflow problem, not a training problem. If your CRM is a data-entry burden that doesn't help reps sell, they will build their own spreadsheets — and your data quality dies with every local file. |
| Attribution models produce wildly different results | Different time windows, different touch definitions, different pipeline filters | Standardize: agree on touch definition, attribution window (24 months for health-tech), pipeline inclusion criteria before running models | Attribution without methodology agreement is a political weapon, not a decision tool. Lock the model for 12 months — changing it mid-year invalidates every trend line and erodes trust in the data. |
| Deal desk is the bottleneck -- deals stall in approval | Approval routing too rigid; AE authority too low; deal desk understaffed | Increase AE discount authority to 20%; auto-approve deals within precedent range; add deal desk headcount if queue over 24 hours | The deal desk should accelerate revenue, not slow it down. If approval wait times exceed SLA, the fix is either more deal desk headcount or broader AE authority — not faster finger-pointing. |

## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
<!-- DEEP: 10+min -- each checklist item references a standard born from production failure -->

- [ ] **[RO1]** Weekly forecast pulse published by Monday 10 AM -- commit vs best-case, coverage ratio, deals flagged for inspection
- [ ] **[RO2]** Monthly ARR bridge completed within 5 business days of month-end -- new, expansion, contraction, churn reconciled to billing system
- [ ] **[RO3]** Quarterly forecast accuracy retro completed within 2 weeks of quarter-end -- commit accuracy, best-case accuracy, by-rep variance
- [ ] **[RO4]** Pipeline coverage dashboard refreshed weekly -- over 3x coverage at all times; early-stage over 60% of total pipeline
- [ ] **[RO5]** NRR and GRR calculated monthly by segment -- enterprise, mid-market, SMB tracked independently
- [ ] **[RO6]** CRM data hygiene audit run weekly -- duplicate rate, required field completion, stale opportunity purge executed
- [ ] **[RO7]** Deal desk SLA report published monthly -- standard approval under 4 hours: over 95%; non-standard under 24 hours: over 90%
- [ ] **[RO8]** Comp plan modeled against prior year actuals before launch -- cost variance vs budget under 10%
- [ ] **[RO9]** Territory assignment validated quarterly -- no unassigned strategic accounts; no rep with over 30 named accounts
- [ ] **[RO10]** Attribution model results published quarterly -- all models side-by-side; W-shaped model used for planning decisions
- [ ] **[RO11]** Tech stack integration health check run weekly -- CRM-MAP sync under 5 min latency; CRM-billing ARR variance under 2%
- [ ] **[RO12]** Win/loss analysis aggregated monthly -- patterns by competitor, stage, and segment reported to product and marketing
- [ ] **[RO13]** Non-standard deal log reviewed monthly -- volume trending under 20% of total deals; discount depth within policy
- [ ] **[RO14]** Quota fairness analysis completed within 30 days of plan launch -- territory variance under 20% for same-tier reps


## References
<!-- STANDARD: 3min -->

- `references/crm-architecture-guide.md` -- Custom object design patterns, automation rule frameworks, data hygiene standards
- `references/forecasting-models.md` -- Forecasting methodology, statistical models, accuracy measurement framework
- `references/comp-plan-templates.md` -- Commission plan templates by GTM motion, SPIFF program designs, clawback policy language
- `references/attribution-models.md` -- Attribution methodology deep dive, multi-touch model configurations, measurement framework
- `references/tech-stack-integration.md` -- Integration architecture patterns, data flow diagrams, health monitoring runbooks
- `references/deal-desk-playbook.md` -- Discount approval matrix templates, contract review routing, non-standard terms escalation framework
