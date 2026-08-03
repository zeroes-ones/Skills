---
name: real-estate-investor
description: >
  Rental property analysis, BRRRR modeling, mortgage optimization, house hacking, REIT vs direct comparison, 1031 basics, and landlord cashflow math.
license: MIT
author: Sandeep Kumar Penchala
type: personal-finance
status: stable
version: 1.0.0
updated: 2026-08-02
tags:
  - real-estate
  - rental
  - brrrr
  - 1031
  - mortgage
  - house-hacking
token_budget: 4500
chain:
  consumes_from:
    - personal-finance
    - tax-strategist
  feeds_into:
    - property-manager
    - commercial-real-estate-analyst
  alternatives: []
---
# Real Estate Investor
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Actionable real estate investing skill: underwriting rental deals (cap rate, cash-on-cash, IRR), BRRRR execution steps, mortgage underwriting and rate/points tradeoffs, house-hacking analysis, REIT vs direct property evaluation, 1031 exchange timing rules, and landlord reserves planning.
<!-- QUICK: 30s -->
## <!-- DEEP: 5+min --> RESEARCH_PREREQUISITE — Execute Before Any Output

**HARD GATE: run RP1-RP8 before any recommendation.**

| # | Research Step | Why | Where |
|---|---|---|---|
| RP1 | Verify market data | Local cap rates and rent comps change quickly | MLS, Zillow, CoStar, local MLS reports |
| RP2 | Inspect property docs | Lease terms, tax bills, inspection reports | Lease copies, inspection, title report |
| RP3 | Cross-check financing options | Rate sheet, ARM terms, points | Lender disclosures, Good Faith Estimate |
| RP4 | Identify failure modes | Vacancy, unexpected CapEx, tenant default | Historical vacancy, local eviction timelines |
| RP5 | Quantify impact | Cash-on-cash, IRR, tax benefit, depreciation | Pro forma spreadsheet, NPV analysis |
| RP6 | Map side effects | How purchase impacts personal taxes, mortgage covenants | Consult tax-strategist, lender docs |
| RP7 | Quality gates | Reserve levels, insurance, licensing | Local landlord regs, insurance binders |
| RP8 | Limitations | Not for primary residence counseling | This SKILL.md |

Document each research step with [RESEARCHED: RPn — ...].

## Iterative Research Loop

At every underwriting pivot, re-run RP1-RP8 and publish findings.

## Quickstart

1. Gather rent comps for subject: 3 nearest comparable units within 0.5 mile and same bedroom count.
2. Pull recent property tax bill, insurance quote, and HOA fees.
3. Build a 10-year pro forma with conservative rent growth 2%/yr, vacancy 7%, CapEx reserve 5% of rent, management fee 8–10%.

## Ground Rules

- Use conservative vacancy: 7% for single-family, 10%+ for small multi-family in soft markets.
- Maintain operating reserves: at least 6 months of mortgage + operating expenses.
- Avoid negative cashflow deals unless strategy is appreciation/BRRRR with clear exit.

## Decision Trees

DT1: Buy vs Pass
1. Is pro forma cash-on-cash return ≥6% after financing and reserves? Yes -> consider. No -> pass or renegotiate.
2. Is cap rate > market cap rate by 1.5%? Yes -> possible value-add. No -> market-priced.

DT2: Refinance timing
1. Rate environment below current note by ≥1.0% and refinance costs <6% of loan amount amortized <3 years -> refinance.
2. If ARM reset within 24 months and rates rising -> refinance to fixed.

## Core Workflow / Implementation

Phase 0 — Deal Intake

- Collect purchase price, expected rent, current leases, property tax, insurance quote, utilities split, HOA.
- Compute initial metrics: Gross Rent Multiplier (GRM), cap rate, cash-on-cash return.

[RESEARCH LOOP: Re-execute RP1-RP8 before proceeding to next phase]

<!-- DEEP: 10+min -->Phase 1 — Underwriting Metrics

Key formulas:
- Cap Rate = NOI / Purchase Price. Target: 4–6% in high-appreciation coastal markets; 7–10% in Sunbelt growth markets for buy-and-hold.
- Cash-on-Cash = (Pre-tax cash flow) / (Cash invested). Target: ≥6–8% for leveraged buys.
- Debt Service Coverage Ratio (DSCR) = NOI / Debt Service. Lenders require 1.2–1.35+ depending on product.
- IRR: project 10-year hold with exit cap rate assumptions (market cap ±1%).

Example: $300k purchase, rent $2,200/mo = $26,400 gross/year. Vacancy 7% -> effective rent $24,552. Operating expenses 35% -> NOI ≈ $15,958. Cap rate = 5.32%.

[RESEARCH LOOP: Re-execute RP1-RP8]

<!-- DEEP: 10+min -->Phase 2 — Financing & Mortgage Optimization

- Rate vs points: compute breakeven months = points / (monthly payment savings). If breakeven < expected hold period, buy points.
- ARM vs fixed: choose fixed if hold > 3–5 years or if expected rate volatility likely to exceed tolerance.
- Mortgage shopping: pull at least 3 lender quotes; compare APR, not just nominal rate.

[RESEARCH LOOP: Re-execute RP1-RP8]

<!-- DEEP: 10+min -->Phase 3 — BRRRR Execution

Steps: Buy (below market), Rehab (budget with 10–15% contingency), Rent (lease within 60 days), Refinance (cash-out to recoup basis at 75% LTV), Repeat.

Metrics: Aim for post-refi LTV that returns ≥70% of initial cash to recycle. Example: Buy $150k, rehab $50k, total $200k; post-rehab value $300k -> 75% LTV = $225k -> recoup $225k - existing mortgage (~$50k) ≈ $175k to recycle.

[RESEARCH LOOP: Re-execute RP1-RP8]

<!-- DEEP: 10+min -->Phase 4 — House Hacking Analysis

- Compare PITI for duplex/two-unit: owner-occupant FHA 3.5% down possible for duplex up to 4 units (certain restrictions). Calculate net housing cost: mortgage - rental income.
- Example: 2-unit purchase $400k, unit rents $1,400 & $1,600, mortgage = $2,500 -> net housing cost = $2,500 - $3,000 = -$500 (positive cashflow).

[RESEARCH LOOP: Re-execute RP1-RP8]

<!-- DEEP: 10+min -->Phase 5 — 1031 Exchange Basics

- Requirements: Like-kind exchange within 45-day ID period and 180-day close; use qualified intermediary; replacement property identification rules (3-property rule or 200% aggregate).
- Timing risk: lock in replacement options before sale; maintain contingency for financing timing.

[RESEARCH LOOP: Re-execute RP1-RP8]

## Error Decoder

| Symptom | Cause | Fix |
|---|---|---|
| Cash-flow negative after closing | Underestimated vacancy or CapEx | Re-run pro forma with higher vacancy and CapEx; renegotiate price or terms |
| Refinance denied | Overstated rents or incomplete documentation | Provide leases, updated appraisal, and audited P&L; reduce withdrawal expectation |

## Best Practices

- Maintain CapEx reserve at 5–10% of gross rents.
- Use professional property manager if >10 units or if owner lacks time; budget 8–10% management fee.
- Keep 6 months of P&I + OpEx as reserve before scaling.

## Production Checklist

- Rent comps validated (3 comps within .5 mile)
- Inspection report completed and material defects priced
- Lender pre-approval and pro forma stress-tested at 5% vacancy and 8% CapEx reserve

## Verification

- Deal passes: DSCR ≥1.25, Cash-on-Cash ≥6%, Reserve ≥6 months P&I + Opex.

## Cross-Skill Coordination

Consumes: personal-finance, tax-strategist. Feeds: property-manager, commercial-real-estate-analyst.

## What Good Looks Like

- Conservative 10-year pro forma with IRR ≥12% and leverage-managed risk.

## References

- IRS Pub 527, local MLS data, Fannie Mae investor rules, HUD guidelines for FHA multi-unit

## Scale Depth

- Solo: single rental underwriting and BRRRR model
- Small: portfolio building and property management coordination
- Medium: 50–250 unit portfolio with asset management
- Enterprise: route to commercial-real-estate-analyst

## Anti-Hallucination

[VERIFIED] Wash sale rules do not apply to real estate; 1031 exchange rules have strict timelines.
[COMMON-PRACTICE] 6 months reserve before scaling purchases.
[INFERRED] Target CoC 6–8% for leveraged buys in moderate markets.
[UNKNOWN] Local landlord-tenant statutes — confirm municipal rules before eviction planning.

<!-- DEEP: 10+min --> War Stories, Edge Cases & Advanced Strategies

- War story: An investor bought a 6-unit property assuming 7% vacancy. After a local economic shock, vacancy rose to 22% for 18 months. The investor's reserves covered P&I for only 9 months and they had to liquidate a unit at a 12% haircut—losing $48k on exit. Lesson: stress-test vacancy to 15–20% for single-market bets; keep 6–12 months P&I + OpEx in reserves.

- Failure narrative: An investor used a 1031 exchange but misidentified replacement property rules (identified 4 properties without using 200% rule); the QI rejected the claim and the client realized $220k taxable gain. Lesson: strictly follow 45/180-day rules and use qualified intermediaries with documented identification.

- Edge case: An owner-occupant house-hacker bought a duplex with FHA 3.5% down, then converted to short-term rentals; insurer canceled policy and rate soared. Lesson: review occupancy clauses and insurance endorsements before strategy changes.

- Advanced tactic: Use a blended financing stack (senior mortgage + mezzanine or preferred equity) for value-add projects to reduce stretched senior LTV while preserving returns to equity — model blended WACC and stress-tests for exit cap rate widening.

[RESEARCH LOOP: Re-execute RP1-RP8]

## Deeper Decision Tree — Acquisition to Exit

```
Acquire -> Underwrite
  |-- Market check: vacancy risk > threshold?
      |-- Yes -> Increase capex and reserves or pass
      |-- No -> Financing
          |-- Conventional vs portfolio lender vs hard money
              |-- Hold period < 3yrs -> consider bridge/hard money with refinance plan
              |-- Hold period > 5yrs -> prefer fixed rate long-term mortgage
Rehab -> Rent vs Flip
  |-- Rehab ROI > 20% after fees? -> Flip (sell within 6-12 months)
  |-- Rehab ROI 10–20% -> Rent & BRRRR if market favorable
Refinance -> Cash-out target met?
  |-- Yes -> Recycle cash and repeat
  |-- No -> Hold and stabilize
Exit -> Market cap rate widening scenario
  |-- Stress test exit IRR; if IRR < target -> extend hold or reduce leverage
```

[RESEARCH LOOP: Re-execute RP1-RP8]

## Error Decoder — Expanded (7 rows)

| Symptom | Cause | Fix |
|---|---|---|
| Underestimated CapEx ($15k surprise) | Incomplete inspection and no contingency | Always add 10–15% contingency to rehab; require inspection with licensed inspector and contractor bids |
| Refinance appraisal shortfall | Comparable sales stale or overoptimistic comp | Obtain second appraisal or provide additional comps and lease data to lender; reduce refinance expectation |
| HOA debt surprise at close | Seller failed to disclose special assessments ($8k–$25k range) | Include HOA estoppel in escrow conditions and demand seller pay or reduce price |
| ARM reset shock | ARM indexed to SOFR and resets +3.5% causing payment to jump $300/mo | Refinance to fixed if hold >24 months or set aside 12 months of payment volatility in reserves |
| Property management failure | 25% delinquency due to tenant screening lapse | Switch PM, tighten screening criteria, maintain vacancy/capex reserve |
| 1031 timing failure | Missed 45-day identification deadline | Consult QI and consider partial recognition; avoid by using flexible 200% rule with clear IDs |
| Insurance cancellation on occupancy change | Using short-term rental platform without endorsement | Secure short-term rental endorsement before switching strategy; consult insurer for proper product |

[RESEARCH LOOP: Re-execute RP1-RP8]

## Best Practices — Specific (10 items)

1. Use conservative vacancy assumptions: 7% for SFH, 10% for small multifamily, 15%+ for uncertain markets. Prefer scenario planning: baseline/ stress/black-swan.
2. Maintain OpEx reserves: 5–10% of gross rents for CapEx plus cash reserves = 6–12 months P&I + OpEx before acquiring additional properties.
3. Target minimum pre-tax Cash-on-Cash of 6% for leveraged buy-and-hold in moderate markets; 8–10% in opportunistic markets.
4. Require DSCR ≥1.25 for conservative financing; 1.2 for aggressive deals with strong exits.
5. For BRRRR, aim to recoup ≥70% of initial cash at refinance to sustain portfolio growth.
6. Use three lender quotes and compare APR and escrow/fees; never accept first offer without two competitive bids.
7. Budget 10–15% rehab contingency and cap timeline slippage by +30% in schedule planning.
8. Contract with professional property manager when >10 units or if owner time investment <5 hrs/week; cap management fee at 8–10% for single-family portfolios.
9. Use inflation-protected instruments (TIPS ladder) for reserve cash rather than low-yield checking accounts when horizon >12 months.
10. Keep separate legal entity per property or grouped by risk profile; consult CPA for 1031 transfer and depreciation schedule optimization.

[RESEARCH LOOP: Re-execute RP1-RP8]

## Production Checklist — Expanded (12 items)

| # | Check | Verify |
|---|---:|---|
| ☐ | Validated 3 comparable rents within 0.5 mile | Attach comps and time/date stamps |
| ☐ | Inspection report with contractor bids | Signed scope-of-work and cost estimates included |
| ☐ | Appraisal/market valuation obtained | Appraisal report in file |
| ☐ | Lender pre-approval or term sheet | APR, points, and fees documented |
| ☐ | Reserve fund ≥ 6 months P&I + OpEx funded | Bank statements verify reserve balance |
| ☐ | Insurance binder with correct occupancy endorsement | Policy shows landlord or STR endorsement as required |
| ☐ | Lease templates and eviction timeline reviewed | Local attorney sign-off for lease terms |
| ☐ | CapEx contingency (10–15%) included in budget | Contingency line item present in pro forma |
| ☐ | Management plan or PM contract in place | Contract signed or SOPs for self-managing documented |
| ☐ | Exit strategy defined (hold/refinance/sell) | Pro forma exit IRR and cap rate assumptions attached |
| ☐ | 1031 QI identified for exchange deals | Qualified intermediary agreement signed |
| ☐ | Tax-deferred depreciation schedule initiated | Depreciation schedule and cost segregation if applicable |
| ☐ | Environmental / title issues cleared | Phase I/II or title exception resolution included |

## References (8)

- IRS Publication 527 — Residential Rental Property
- Fannie Mae investor guides and lender overlays
- HUD/FHA guidance for multi-unit owner-occupants
- BiggerPockets rental property calculators and case studies
- CoStar/Zillow/MLS rent comp tools
- Book: "The Real Estate Game" by William J. Poorvu
- National Association of Realtors (NAR) investment reports
- FEMA flood map and local zoning ordinances for insurance and use restrictions

## Cross-Skill Coordination Additions

- To tax-strategist: send projected depreciation schedules, cost-segregation opportunities, and 1031 identification plan.
- To property-manager: hand off lease templates, rent roll, and maintenance budget forecasts.

## Scale Depth — Tools & Team Triggers

- Solo: Single-property underwriting using Excel + BiggerPockets calculators; <$300k property value; owner handles management.
- Small: 5–25 unit portfolio using Buildium/AppFolio + QuickBooks for bookkeeping; hire part-time PM at 8–10% fee.
- Medium: 50–250 units with asset manager, regional property managers, and centralized accounting; implement Yardi or MRI.
- Enterprise: >250 units — institutional asset management with acquisitions team, capital market access, and portfolio-level risk systems.

## Concrete Framework — BRRRR Math Example

- Buy $150k, rehab $50k, ARV = $300k. Target post-refi LTV 75% → Max loan = $225k. Payoff existing mortgage $40k → cash recovered ≈ $185k. If initial cash invested $60k, recycled cash fraction ≈ 308% allowing rapid scaling.

[RESEARCH LOOP: Re-execute RP1-RP8]

[VERIFIED] 1031 exchange strict timelines (45/180 days).
[COMMON-PRACTICE] Reserve 6 months P&I + OpEx before scaling.
[INFERRED] Target CoC 6–8% for leveraged buys in moderate markets.
[UNKNOWN] Local eviction timelines and COVID-era moratoria changes — verify current municipal guidance.

