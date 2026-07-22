---
name: fp-and-a-analyst
description: Financial planning & analysis for startups — 3-statement models, SaaS metrics, budgeting, variance analysis, scenario planning, fundraising modeling, board financials, unit economics, and headcount
  planning. Use when building financial models, preparing board decks, evaluating fundraising scenarios, or diagnosing SaaS metric health.
author: Sandeep Kumar Penchala
type: corporate-finance
status: stable
version: 1.0.0
updated: 2026-07-21
tags:
- fp-and-a
- financial-modeling
- saas-metrics
- budgeting
- fundraising
- corporate-finance
token_budget: 3420
output:
  type: spreadsheet
  path_hint: models/
chain:
  consumes_from:
  - accountant
  - business-intelligence-engineer
  - ceo-strategist
  - finops-engineer
  - hr-manager
  - investor-relations
  - product-strategist
  - recruiting
  - revops-manager
  - treasury-manager
  feeds_into:
  - accountant
  - board-manager
  - ceo-strategist
  - finops-engineer
  - investor-relations
  - revops-manager
  - treasury-manager
  - vp-engineering
---

# FP&A Analyst — The Startup Finance Engine

Financial planning and analysis for venture-backed startups. Build models that raise money, run companies, and survive downturns. Think like a startup CFO who's lived through a down round and a cash crunch — every number must be defensible.

## Ground Rules — Read Before Anything Else

These rules apply to **every** response this skill produces.

- **Never project without drivers.** Every revenue and cost line item must tie to a verifiable driver (headcount, customer count, usage volume). "Revenue grows 20% because it grew 20% last year" is not FP&A — it's guessing.
- **Model top-down AND bottom-up.** Top-down: TAM × penetration = revenue. Bottom-up: reps × quota × attainment = revenue. They must reconcile within 10%. If they don't, your assumptions are wrong.
- **Cash is the only truth.** GAAP profit is an opinion; cash is fact. Always model cash flow separately from P&L. A company can be "profitable" on GAAP basis and still run out of cash due to AR timing or prepaid expenses.
- **Show your work.** Every model cell must be traceable to its source assumption. If an investor or board member asks "where does this number come from?" and you can't answer in 5 seconds, the model fails.
- **Scenario ≠ wishful thinking.** Your "upside case" must be plausible under specific, named conditions (e.g., "conversion improves from 3% to 5% due to new onboarding flow"). Never model "everything goes perfectly."

## Route the Request
<!-- QUICK: 30s — pick your path, skip the rest -->

What are you trying to do?
├── Build a financial model
│   ├── From scratch (no existing model) → Jump to "Core Workflow > Phase 1: Model Architecture"
│   ├── Improve an existing model → Go to "Core Workflow > Phase 3: Model Audit"
│   └── For fundraising → Jump to "Decision Trees > Fundraising Model Type"
├── Analyze SaaS metrics
│   ├── Calculate your metrics → Go to "SaaS Metrics Formulas"
│   ├── Diagnose what's broken → Jump to "Decision Trees > SaaS Metric Diagnosis"
│   └── Benchmark against peers → Go to "Best Practices" benchmark table
├── Prepare board materials → Start at "Core Workflow > Phase 5: Board Financials"
├── Plan a budget → Jump to "Decision Trees > Budgeting Method Selection"
├── Run scenarios → Go to "Core Workflow > Phase 4: Scenario Planning"
├── Model headcount → Jump to "Core Workflow > Phase 2: Headcount & OpEx"
├── Model a fundraise → Go to "Fundraising Modeling"
├── Need actuals/closed books for your model? → Invoke `accountant` for GAAP financials and reconciliation
├── Need cash position or runway data? → Invoke `treasury-manager` for actual cash balances and debt covenants
├── Need investor materials packaged? → Invoke `investor-relations` for pitch deck and data room financials
├── Preparing for a board meeting? → Invoke `board-manager` for board package structure and governance requirements
├── Need engineering headcount planning? → Invoke `vp-engineering` for hiring plan and team structure input
└── Don't know where to start? → Run "Core Workflow > Phase 1: Model Architecture"

Do not read the entire skill. Follow the route above and read only the sections it points to.

## When to Use
<!-- QUICK: 30s — scan to decide if this skill fits -->

- Building a 3-statement financial model (P&L, balance sheet, cash flow) for a startup
- Creating a budget: zero-based, driver-based, or rolling forecast
- Running variance analysis: actuals vs budget vs forecast with root cause
- Preparing board deck financials: KPIs, burn, runway, revenue waterfall
- Calculating SaaS metrics: ARR/MRR, NRR/GRR, LTV/CAC, magic number, Rule of 40, burn multiple
- Modeling a fundraise: dilution, cap table, use of funds waterfall, cash runway
- Building unit economics: CAC by channel, LTV by cohort, payback period, gross margin by product line
- Scenario planning: best case, base case, downside case with sensitivity tables
- Headcount planning: department-level hiring plan tied to revenue milestones
- M&A financial modeling: accretion/dilution analysis, synergy sizing, purchase price allocation

### Cross-skills Integration

This skill in a typical workflow chain:

| Step | Skill | What it produces for this skill |
|------|-------|---------------------------------|
| **Before** | accountant | Actuals (P&L, balance sheet), month-end close data, revenue recognition treatment — the baseline for any forecast |
| **Before** | ceo-strategist | Fundraising thesis, growth targets, strategic priorities — what to model toward |
| **Before** | business-strategist | Market sizing, GTM strategy, pricing model — revenue driver assumptions |
| **This** | fp-and-a-analyst | 3-statement model, SaaS metrics dashboard, budget, scenario analysis, board financials, fundraise model |
| **After** | ceo-strategist | Consumes board financials and scenario analysis for strategic decisions |
| **After** | board-manager | Consumes board financials, KPI dashboard, runway analysis |
| **After** | investor-relations | Consumes fundraise model, cap table projections, use of funds |

Common chains:
- **Budgeting cycle**: accountant → fp-and-a-analyst → ceo-strategist — Actuals → budget → approval
- **Fundraising**: business-strategist → fp-and-a-analyst → investor-relations — Market sizing → fundraise model → investor deck
- **Board prep**: accountant → fp-and-a-analyst → board-manager — Month-end close → board financials → board packet

## Decision Trees
<!-- QUICK: 30s — follow the ASCII tree to your scenario -->

### Budgeting Method Selection

```
What's your stage?
├── Pre-revenue / < $1M ARR
│   └── Use: Zero-based budgeting. Justify every dollar. No "last year + 10%."
│       Model: Headcount × fully-loaded cost + vendor contracts + overhead.
├── $1M-$10M ARR (early growth)
│   └── Use: Driver-based budgeting. Revenue drivers → headcount → opex.
│       Model: ARR = f(sales headcount × quota × ramp); opex = f(headcount × cost/head).
├── $10M-$50M ARR (scaling)
│   └── Use: Rolling forecast (12-18 month). Update monthly with actuals.
│       Model: Departments own their budgets. Finance consolidates and challenges.
└── $50M+ ARR (enterprise)
    └── Use: Driver-based + department bottoms-up + rolling forecast.
        Model: FP&A system (Adaptive/Anaplan/Pigment), not spreadsheets.
```

### SaaS Metric Diagnosis

```
ARR growth < 30% YoY?
├── YES → Is NRR < 100%?
│   ├── YES → You have a leaky bucket. Fix retention before growth.
│   │         Root cause: churn > expansion. Check: onboarding, CS, product gaps.
│   └── NO  → Growth problem, not retention. Check: sales capacity, pipeline, conversion.
└── NO  → Burn multiple > 2x?
    ├── YES → You're burning too much per dollar of growth.
    │         Fix: cut burn or grow faster. Burn multiple = net burn / net new ARR.
    └── NO  → Rule of 40 < 40%?
        ├── YES → Growth + profitability below threshold. Investors will discount valuation.
        └── NO  → Healthy. Monitor Magic Number (> 0.8) and months to recover CAC (< 18).
```

**What good looks like:** A 3-statement model where changing any driver automatically updates P&L, balance sheet, and cash flow. Board financials show revenue waterfall, cohort retention curves, and scenario comparison on one page. SaaS metrics page passes investor scrutiny — every number is formula-traced to source data.

## Core Workflow
<!-- STANDARD: 3min -->

### Phase 1: Model Architecture (~45 min)
1. **Define model structure:** Time (monthly for 36-60 months), sections (assumptions → revenue → opex → P&L → balance sheet → cash flow → outputs).
2. **Set up assumptions tab:** All drivers in ONE place — pricing, headcount by department, salary by role, CAC by channel, churn rates, payment terms, tax rates. Color-code: blue = input, black = formula, green = linked from another sheet.
3. **Build revenue model:** Top-down (TAM × penetration) AND bottom-up (new customers × ARPU + existing × expansion). Must reconcile. Include seasonality adjustments if applicable.
4. **Build opex model:** Headcount-driven costs (salary + benefits + payroll tax = 1.25-1.35× base salary), non-HC costs (vendor contracts, rent, software — grow at 15% of HC growth).
5. **Build the three statements:** P&L → balance sheet (AR = revenue × DSO/30, AP = opex × DPO/30) → cash flow (indirect method: net income + non-cash adjustments + working capital changes). Check: ending cash = beginning cash + net cash flow. If it doesn't tie, fix working capital.

### Phase 2: Headcount & OpEx (~30 min)
1. **Department-level headcount:** Sales (AE + SDR, ratio 1:1 at early stage, 1:2 at scale), Engineering (1 PM : 5-8 engineers), G&A (1 finance per 50 employees, 1 HR per 75 employees).
2. **Fully-loaded cost per head:** Base salary × 1.08 (payroll tax) + benefits ($12K-18K/yr US) + equipment ($3K one-time) + software ($3K-6K/yr). RULE: never model salary alone.
3. **Revenue-linked hiring:** Sales hires = target ARR growth / (quota × ramp-adjusted attainment). E.g., $5M new ARR / ($500K quota × 70% attainment in year 1) = 14.3 → hire 15 AEs with staggered start dates.
4. **Ramp curves:** Month 1 = 0% of quota, Month 2 = 25%, Month 3 = 50%, Month 4 = 75%, Month 5+ = 100%. First-year productivity = ~60% of full quota.

### Phase 3: Model Audit (~20 min)
1. **Sanity checks:** ARR per employee (seed: $50K-100K, Series A: $150K-200K, growth: $200K-300K), gross margin (SaaS: 70-85%), opex as % of revenue, cash runway (months).
2. **Formula audit:** Trace every P&L line to its driver. Trace cash to P&L + balance sheet deltas. No hard-coded numbers outside assumptions tab.
3. **Sensitivity check:** Worst case: churn doubles AND sales attainment drops to 50% AND payment terms stretch 30 days. If the company survives 18 months, model is conservative enough.
4. **Peer comparison:** Run against public SaaS benchmarks (see Best Practices). If your model shows 95% gross margin when median is 78%, explain the difference.

### Phase 4: Scenario Planning (~25 min)
1. **Define scenarios:** Base case (most likely), upside (specific catalyst), downside (specific risk). Each scenario changes 3-5 key drivers, not everything.
2. **Build scenario selector:** Single dropdown that toggles all assumptions. Each scenario has its own assumptions column.
3. **Sensitivity tables:** Revenue vs. 2 key drivers (e.g., CAC and churn), cash out date vs. burn and growth rate. Use data tables, not manual iteration.
4. **Output comparison:** Side-by-side: ARR, gross margin, opex, EBITDA, cash balance, runway months, Rule of 40, burn multiple.

### Phase 5: Board Financials (~30 min)
<!-- DEEP: 10+min -->
1. **One-page dashboard:** Revenue (actual vs plan waterfall), ARR bridge (new + expansion - churn - contraction), headcount by department, cash + runway, top 3 KPIs vs target.
2. **Cohort view:** Revenue retention by cohort (monthly cohorts for first 24 months, quarterly after). Include logo retention alongside dollar retention.
3. **Burn analysis:** Gross burn (total cash out), net burn (cash out - cash in), runway (cash / net burn). Highlight date when cash runs out in each scenario.
4. **Ask slide:** If fundraising, include: amount raising, use of funds (% hiring, % marketing, % buffer), milestones achieved with this round, dilution at different valuations.

<!-- QUICK: 30s — key numbers that matter -->

## SaaS Metrics Formulas
<!-- QUICK: 30s — copy-paste calculator -->

| Metric | Formula | Good | Great | Red Flag |
|--------|---------|------|-------|----------|
| **ARR** | MRR × 12 (use actual MRR, not annualized run-rate of last month) | Growing | >100% YoY at <$10M | <30% YoY |
| **NRR** | (Starting ARR + Expansion - Churn - Contraction) / Starting ARR | >100% | >120% | <100% |
| **GRR** | (Starting ARR - Churn - Contraction) / Starting ARR | >85% | >90% | <80% |
| **LTV:CAC** | (ARPU × Gross Margin %) / (Monthly Churn × CAC) | >3x | >5x | <3x |
| **CAC Payback** | CAC / (ARPU × Gross Margin %) — in months | <18mo | <12mo | >24mo |
| **Magic Number** | (Current Q ARR - Prior Q ARR) × 4 / Prior Q S&M Spend | >0.8 | >1.0 | <0.5 |
| **Rule of 40** | Revenue Growth % + EBITDA Margin % | >40% | >60% | <25% |
| **Burn Multiple** | Net Burn / Net New ARR | <1.5x | <1.0x | >2.0x |
| **Gross Margin** | (Revenue - COGS) / Revenue | >70% | >80% | <65% |
| **ARR per Employee** | ARR / FTE Count | $150K+ | $200K+ | <$100K |

**DEEP: 10+min — War story:** A Series B startup reported "120% NRR" to their board for 6 quarters. When an acquirer did diligence, they found the company was including professional services revenue in expansion MRR. True NRR was 98%. Deal repriced from $200M to $80M. Lesson: audit your metric definitions against SaaS-industry-standard formulas. Never redefine a metric to look better.

## Fundraising Modeling
<!-- STANDARD: 3min -->

### Use of Funds Waterfall
Model exactly where the money goes over 24-36 months:

| Category | Typical % | Model As |
|----------|-----------|----------|
| Engineering / Product | 35-45% | Headcount × fully-loaded cost |
| Sales & Marketing | 30-40% | Headcount + ad spend + events |
| G&A | 10-15% | Headcount + professional services |
| Buffer / Contingency | 10-15% | 15% of total raise |

### Cap Table & Dilution

```
Round       Pre-Money    Raise     Post-Money   Dilution   New Investor
Seed         $8M          $2M       $10M         20%        Seed fund
Series A    $25M          $8M       $33M         24%        Tier-1 VC
Series B    $70M         $20M       $90M         22%        Growth fund
```

Founder dilution path from seed → Series B: (1 - 0.20) × (1 - 0.24) × (1 - 0.22) = 47.4% retained. Option pool expansion at each round adds 3-5% additional dilution.

**DEEP: 10+min — War story:** A founder modeled their Series A at $40M pre-money with $10M raise. Their revenue was $2M ARR — 20x multiple. They didn't model the "comp" scenario: what comparable companies actually raised at. VCs offered $20M pre-money. The model had no downside case, so the founder couldn't negotiate from data. They took the term sheet from a position of weakness. Always model: "what multiple do I need to justify my valuation to an investor who's seen 500 deals this year?"

## Best Practices
<!-- STANDARD: 3min -->

- **One source of truth for assumptions.** Every driver lives in exactly one cell on the assumptions tab. No exceptions. When you debate a number, you debate that one cell.
- **Model in months, not years, through at least month 36.** Annual models hide seasonality, hiring timing, and cash flow gaps. A company that's fine on an annual basis can miss payroll in month 9.
- **Gross margin by product line, not blended.** High-margin software revenue subsidizing low-margin services revenue creates a ticking time bomb. As the mix shifts, blended margin deteriorates — and you won't see it coming.
- **Cash flow statement from the balance sheet, not the P&L.** Indirect method: start with net income, add back non-cash items (D&A, SBC, bad debt), then adjust for working capital changes (ΔAR, ΔAP, Δprepaid, Δdeferred revenue). The balance sheet must balance every period.
- **AR = Revenue × DSO / Days.** If your SaaS company bills annually and DSO is 45, you have a collections problem. SaaS DSO should be < 30 for monthly billing, < 15 for annual upfront.
- **Deferred revenue is a liability, not revenue.** SaaS companies that bill annually show high cash but low GAAP revenue. Model the unwinding: deferred revenue balance / monthly revenue recognition = months of booked-but-unrecognized revenue.
- **SBC is a real expense.** Stock-based compensation reduces your ownership and will dilute you. Model it on the P&L (ASC 718) and show diluted share count. Investors will calculate EBITDA - SBC anyway.
- **Never model to a desired outcome.** If the model shows you run out of cash in 14 months, don't adjust assumptions until it shows 24. Present the real number and plan the bridge (raise sooner, cut burn, grow faster).
- **Version your models.** `Company_Model_v12_final_FINAL.xlsx` is not a system. Use: `YYYY-MM-DD_Model_v[#]_[change description].xlsx`. Archive old versions, don't overwrite.
- **Peer benchmark every quarter.** Pull public SaaS comps: gross margin, opex ratios, Rule of 40, ARR per FTE. If your model diverges >20% from median, write a footnote explaining why.

<!-- QUICK: 30s — key rule-of-thumb benchmarks -->

| Stage | ARR | Gross Margin | OpEx % Rev | Rule of 40 | Burn Multiple |
|-------|-----|-------------|-----------|------------|---------------|
| Seed | $0-3M | 65-75% | 150-250% | N/A (negative) | N/A |
| Series A | $3-8M | 70-78% | 100-150% | 20-40% | 1.5-2.5x |
| Series B | $8-25M | 72-80% | 80-110% | 35-55% | 1.0-1.8x |
| Series C | $25-100M | 73-82% | 60-90% | 45-70% | 0.5-1.2x |
| Pre-IPO | $100M+ | 75-85% | 50-75% | 50%+ | <0.8x |

## Cross-Skill Coordination

<!-- NEIGHBORS: Skills this FP&A analyst works with — the model is the central nervous system of the company -->

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `accountant` | Closed books, actuals by department, ARR schedule, cash flow statement | Monthly close — Day 5 draft, Day 10 final; every model refresh must reconcile to last closed period |
| `treasury-manager` | Actual cash position, 13-week cash flow, debt covenants, FX exposure | Weekly — update model cash forecast with actuals; monthly covenant compliance check |
| `ceo-strategist` | Fundraising strategy, board communication priorities, strategic initiatives for modeling | Pre-fundraising — build operating model; quarterly — board deck financial section |
| `recruiting` | Hiring plan with start dates, salary bands, equity guidelines | Monthly headcount forecast update; every hire changes the model burn rate |
| `revops-manager` | Pipeline data, quota attainment, ARR forecast by segment | Monthly revenue forecast sync; quarterly territory planning model |
| `product-strategist` | New product launch timeline, expected ARPU, adoption curve | Pre-launch — revenue scenario modeling; quarterly — actuals vs adoption assumptions |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `ceo-strategist` | Operating model, scenario analysis, board financials, valuation model | CEO presents to investors without current model = credibility loss |
| `board-manager` | Financial package: P&L forecast, cash runway, ARR bridge, headcount plan, burn multiple | Board governance requires financial visibility — stale data erodes board confidence |
| `investor-relations` | Quarterly earnings/update model, guidance ranges, KPI dashboard | Investors make allocation decisions on your guidance — errors = trust loss |
| `treasury-manager` | Cash forecast (annual + 13-week), fundraising timeline, expense run rate | Treasury manages daily cash based on your forecast — wrong = overdraft or missed opportunity |
| `department-heads` (via `engineering-manager`, `marketing-manager`, `sales-engineer`) | Department budget vs actual, hiring plan model, ROI analysis for spend requests | Business decisions stall without financial approval framework |

**Coordination cadence:**
- **Weekly:** Cash forecast update with treasury-manager; actuals check against model
- **Monthly:** Close reconciliation with accountant; budget vs actual variance report to department heads
- **Quarterly:** Re-forecast with all upstream inputs; board financial package; investor update draft
- **Pre-Fundraising:** Full operating model rebuild with CEO input; scenario analysis (bull/base/bear)
- **Annually:** Annual budget with bottoms-up department builds; compensation benchmarking; pricing model review

**Decision Gates & Handoff Artifacts:**
- **Model integrity gate:** Every model must reproduce last 12 months of actuals within 5% before it can be used for forecasting. Artifact: Model-vs-actuals reconciliation sheet with variance explanations.
- **Top-down/bottom-up reconciliation gate:** TAM-based revenue forecast must reconcile with bottoms-up (reps × quota × attainment) within 10%. Gap >10% = assumption error. Artifact: Reconciliation bridge document.
- **Scenario plausibility gate:** Every scenario must name the specific conditions under which it materializes (e.g., "conversion improves from 3% to 5% due to new onboarding flow"). "Everything goes perfectly" is not a scenario. Artifact: Scenario assumption document with named drivers.
- **Cash runway gate:** 13-week cash forecast must show runway ≥12 months in base case, ≥6 months in bear case. Shorter runway triggers fundraising preparation. Artifact: Cash runway tracker updated every Friday.
- **Board package gate:** Financial appendix must include: P&L forecast, cash runway, ARR bridge, headcount plan, burn multiple, and variance commentary. Package delivered 7 days before board meeting. Artifact: Board financial appendix with CEO-reviewed commentary.
- **Handoff to `ceo-strategist`:** Operating model with bull/base/bear scenarios; valuation model; strategic initiative ROI analysis. Artifact: CEO briefing deck with key assumptions highlighted.
- **Handoff to `board-manager`:** Board financial package with all required sections and variance analysis. Artifact: Board-ready financial appendix in board template format.
- **Handoff to `investor-relations`:** Investor-ready model with SaaS metrics dashboard, guidance ranges, and KPI definitions. Artifact: Fundraising model with methodology appendix.
- **Handoff to `treasury-manager`:** Cash forecast (annual + 13-week), fundraising timeline, expense run rate by department. Artifact: Cash forecast model with weekly granularity.

## Error Decoder
<!-- QUICK: 30s — exact error → root cause → fix -->
<!-- DEEP: 10+min — each error is a model failure that burned real cash -->

| Symptom | Root Cause | Fix | Lesson |
|---------|------------|-----|--------|
| Model doesn't balance (Assets ≠ Liabilities + Equity) | Working capital formula error or retained earnings not linked to P&L net income | Check: ΔRetained Earnings = Net Income (P&L) each period. Check: Cash = Prior Cash + Cash Flow Statement net change. Trace the plug line. | A broken model undermines every decision. Always verify retained earnings ties to net income. |
| ARR per employee outside $100K-$300K range | Headcount ramped too fast relative to revenue, or revenue overstated | Audit: sales headcount vs. quota attainment. Check ARR includes only recurring subscription revenue. At seed stage, $50K-80K is normal. | Headcount growth must track revenue. Never hire more than one quarter ahead of proven demand. |
| NRR > 120% consistently | Expansion includes non-recurring revenue, price increases double-counted, or churn understated | Recalculate: NRR = (starting cohort ARR + true expansion - true churn - downgrades) / starting cohort ARR. Exclude: one-time services, new product lines sold only to existing customers. | Metric inflation destroys credibility. Audit expansion revenue quarterly against industry-standard definitions. |
| Cash runs out while P&L shows profit | Deferred revenue timing mismatch — you spent the cash from annual prepays before earning the revenue | Model: monthly cash flow from balance sheet, not P&L. Add line: "cash collected but not yet earned" = Δ Deferred Revenue. This is the GAAP-vs-cash bridge. | Cash is fact, profit is opinion. Deferred revenue timing is the #1 GAAP-vs-cash trap. |
| Burn multiple spikes suddenly | Revenue growth slowed but burn stayed flat (hiring continued) | Freeze hiring until burn multiple < 2.0x. Model: what ARR growth is needed at current burn to get burn multiple < 1.5x? | Hiring freeze acts faster than growth acceleration. Act on burn multiple the quarter it spikes. |
| EBITDA looks great but bank account is shrinking | Working capital drain: AR growing faster than revenue, inventory build, prepaid expenses | Audit: DSO trend (rising = collection problem), DPO trend (falling = paying vendors faster), prepaid balance (lumpy annual software contracts). | Working capital can kill a profitable company. Track DSO and DPO as closely as revenue. |
| Fundraise dilution model shows 60%+ founder ownership after Series B | Assumed valuations too high relative to stage benchmarks | Check: pre-money / ARR multiple vs. market. Series A: 15-25x, Series B: 10-20x, Series C: 8-15x. Use median, not top-decile. | Unrealistic valuation assumptions mislead fundraising strategy. Always benchmark against actual market comps. |
| Forecast missed by 40% due to wrong growth assumption | Assumed 15% MoM growth based on best month, not 3-month average | Use trailing 3-month average for baseline growth rate. Model 3 scenarios: base, upside, downside — with probability weights. | A Series A company modeled 15% MoM growth because December was a record month. January-March averaged 3%. Missed forecast cost them a bridge round. |
| Budget variance not flagged until too late | No monthly variance review process — budget vs actual run only at quarter end | Implement monthly budget vs actual review within 5 business days of month-end. Flag any line >10% variance. Escalate >20% variances to CFO. | A marketing team spent 60% of annual budget in Q1 on a campaign that underperformed. By Q4, there was no budget left for critical demand gen. Monthly variance review would have caught this in February. |
| Board presentation with unreconciled numbers | Model was updated without reconciling to actuals — board saw forward projections that contradicted historical financials | Every board deck must reconcile model to actuals before presentation. Include a "model vs actuals" bridge page. Have finance team sign off on numbers. | A CEO presented $12M ARR to the board; accounting showed $9.8M. The CEO used gross ARR (including churned accounts not yet removed). Trust was damaged and the board asked for external audit. |
| Headcount model shows breakeven but company keeps burning | Fully loaded cost per employee understated by 30% (no benefits, payroll tax, equipment, or facilities cost included) | Build fully loaded cost per employee: salary + bonus + payroll tax (7.65% employer) + benefits ($12-20K/yr) + equipment ($5K/yr) + facilities ($15-30K/yr). Add 20% buffer. | A founder modeled breakeven at 50 people with $5K/mo per employee. Real cost was $8.5K/mo. At 50 people they were burning $175K/mo more than expected. |
| Unit economics show positive but company loses money on every customer | Contribution margin calculated incorrectly — allocated S&M and G&A as variable costs | Contribution margin = revenue - direct variable costs (COGS + customer support + payment processing). S&M and G&A are period costs, not COGS. Gross margin + contribution margin are different metrics. | A marketplace startup claimed 80% gross margin and positive unit economics. Their "COGS" excluded payment processing, customer support, and refunds. Real contribution margin was -15%. |

### Error Decoder

| Problem | Root Cause | Fix | Lesson |
|---------|------------|-----|--------|
| P&L doesn't tie to bank balance | Accrual accounting entries not reconciled | Run a monthly variance report: net income (accrual) vs cash flow from operations (cash). Every variance >5% needs a reconciling item identified. If accruals consistently drift from cash, review your revenue recognition and deferred revenue entries. | Accrual vs cash variance should be reviewed monthly. If >5%, find the reconciling item. |
| Board questions ARR calculation | SaaS metrics not defined with clear methodology | Document your SaaS metric calculation methodology: what counts as ARR (annualized recurring revenue, not one-time), how expansion/contraction/churn are attributed, and how multi-year contracts are counted. Publish this as a board appendix. | Publish your SaaS metric methodology as a board appendix. Standardize definitions. |
| Fundraising model doesn't match historicals | Model was built forward-only, not reconciled backwards | Every fundraising model must start by reproducing the last 12 months of actuals within 5%. If it can't explain the past, it can't predict the future. Reconcile model vs actuals before presenting to investors. | Every model must reproduce the last 12 months within 5%. If it can't explain the past, it can't predict the future. |
| Cash runway suddenly shorter than expected | 13-week cash flow not maintained | Update the 13-week cash flow forecast every Friday afternoon. If actual cash differs from forecast by >15% in any week, investigate the variance source. Key driver: AR timing vs actual collections — always track DSO. | Update 13-week cash forecast every Friday. Track DSO religiously. |
| Sales tax notice from a state you don't operate in | Economic nexus triggered by remote sales | Use a sales tax automation tool (TaxJar/Avalara). Monitor nexus thresholds in every state where you have customers. File in states where you have physical presence AND states where you cross economic nexus thresholds ($100K or 200 transactions). | Use automated sales tax tools. Monitor nexus thresholds in every state. |
| Audit reveals material weakness in revenue recognition | ASC 606 review not done at contract signing | Every contract must go through an ASC 606 checklist at signing: is it a license or a service? Are there performance obligations? Is revenue recognized over time or at a point in time? Involve accounting in the deal review process, not after the contract is signed. | ASC 606 review at contract signing, not after. Involve accounting early. |
| Cap table error discovered during fundraising | Stock ledger not maintained after every equity event | Update the cap table after every: funding round, option grant, option exercise, transfer, repurchase, and conversion. Use a platform (Carta/Pulley) — a spreadsheet cap table will have errors by the time you have >5 equity holders. | Use Carta/Pulley. Reconcile cap table monthly. Audit before fundraises. |


## Production Checklist
<!-- QUICK: 30s — all must pass before presenting to anyone -->

- [ ] **[S1]** Revenue model has both top-down AND bottom-up build — they reconcile within 10%
- [ ] **[S2]** Every cost line traces to a driver (headcount, customer count, usage) — no flat % growth assumptions
- [ ] **[S3]** Cash flow statement built from balance sheet (indirect method), not P&L — ending cash ties to balance sheet cash
- [ ] **[S4]** Headcount costs are fully loaded: salary × 1.25-1.35× for benefits + taxes + equipment + software
- [ ] **[S5]** SaaS metrics calculated using SaaS-industry-standard formulas — no custom definitions
- [ ] **[S6]** Three scenarios modeled: base, upside (specific catalyst), downside (specific risk) — not "everything +/- 10%"
- [ ] **[S7]** Fundraise model includes: use of funds waterfall, dilution path through next 2 rounds, option pool refresh
- [ ] **[S8]** Sensitivity tables on at least 2 key drivers (CAC + churn, or growth + burn)
- [ ] **[S9]** Board financials fit on one printed page: revenue waterfall, KPI dashboard, cash + runway, headcount
- [ ] **[S10]** Model is version-controlled with date in filename — not `_vFinal_FINAL`
- [ ] **[S11]** Peer benchmarks included: gross margin, opex ratios, ARR/FTE vs. public SaaS comps
- [ ] **[S12]** Deferred revenue modeled separately — cash collected ≠ GAAP revenue (ASC 606)
- [ ] **[S13]** Gross margin split by product line if multiple revenue streams exist
- [ ] **[S14]** Runway shown in months at current burn AND at 20% burn reduction scenario

## Scale Depth: Solo → Small → Medium → Enterprise

### Solo
Freelance/outsourced bookkeeper, spreadsheets or QuickBooks Simple Start. Focus on accurate transaction recording and tax compliance. Skip: intercompany eliminations, deferred tax accounting, complex consolidations. Coordination: external CPA handles tax filings; founder reviews P&L quarterly.

### Small Team
First in-house accountant, QuickBooks/Xero, month-end close process. Focus: reliable monthly financials, basic internal controls. Coordination: with FP&A for budget vs actuals, with operations for inventory/COGS tracking.

### Medium Team
Finance team (staff accountant, AP/AR, payroll), ERP migration (NetSuite/Intacct). Focus: scalable close process, audit readiness. Coordination: with FP&A on flux analysis, with legal on equity administration, with sales on revenue recognition.

### Enterprise
Controller + audit committee, SOX/internal controls, SEC reporting. Focus: public-company readiness, audit defense. Coordination: with investor relations on earnings prep, with legal on SEC filings, with tax on provision calculations.

### Transition Triggers
| From → To | Trigger |
|-----------|---------|
| Solo → Small | Month-end close taking >10 business days; investor requests reliable financials |
| Small → Medium | First external audit; >50 employees; multiple legal entities |
| Medium → Enterprise | IPO filing; SOX compliance requirement; global operations |

## What Good Looks Like

The financial model opens in Excel/Google Sheets. Changing the "Hiring Start Date" for sales from Jan to March shifts all downstream revenue, opex, and cash balances automatically. The board summary tab shows: ARR growth rate (30%+), NRR (110%+), gross margin (78%), burn multiple (1.2x), runway (21 months), Rule of 40 (45%) — each with a green/yellow/red indicator vs. benchmark. The fundraise tab shows dilution waterfall: founders 47%, employees 18%, Seed 20%, Series A 15% after Series B. No #REF! errors. No hard-coded numbers in formula cells. A new hire starting Monday can update actuals within 15 minutes.

## References
<!-- QUICK: 30s — deeper reading and templates -->

- **Templates:** `assets/three-statement-model-template.xlsx` — pre-built 3-statement model with SaaS revenue drivers and scenario selector
- **Templates:** `assets/saas-metrics-calculator.xlsx` — standalone SaaS metric calculator with cohort retention curves
- **References:** `references/saas-benchmarks-2026.md` — public SaaS comps by ARR range, updated quarterly
- **References:** `references/asc-606-saas-guide.md` — revenue recognition for SaaS: performance obligations, SSP, contract modifications
- **References:** `references/fundraising-model-guide.md` — dilution waterfalls, use of funds, cap table modeling
- **Books:** Financial Modeling (Simon Benninga), Venture Deals (Feld & Mendelson), SaaS Metrics 2.0 (David Skok)
- **Related skills:** `accountant` (actuals and month-end close), `treasury-manager` (cash management and banking), `ceo-strategist` (fundraising strategy), `business-strategist` (market sizing and GTM), `board-manager` (board meeting preparation)
