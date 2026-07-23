# Core Workflow — Full Implementation

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
