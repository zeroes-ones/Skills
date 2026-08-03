---
name: tax-strategist
description: >
  Tax optimization for individuals: deduction maximization, tax-advantaged accounts, Roth conversion ladders, tax-loss harvesting, charitable giving optimization, entity structuring for small business owners, and state tax arbitrage. Not for corporate tax.
license: MIT
author: Sandeep Kumar Penchala
type: personal-finance
status: stable
version: 1.0.0
updated: 2026-08-02
tags:
  - taxes
  - roth
  - hsa
  - tax-loss-harvesting
  - charitable-giving
  - entity-structure
  - 1031
token_budget: 4500
chain:
  consumes_from:
    - accountant
    - personal-finance
  feeds_into:
    - retirement-planner
    - wealth-management-advisor
  alternatives: []
---
# Tax Strategist
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Practical, compliance-aware individual tax optimization playbook. Focus areas: deduction stacking, timing, account placement (HSA/401k/IRA/529), Roth-conversion ladders, tax-loss harvesting rules, charitable strategies (DAF, QCD), simple entity guidance for self-employed (S-Corp vs LLC), and state tax arbitrage. Not for corporate tax returns — route to accountant.
<!-- QUICK: 30s -->
## <!-- DEEP: 5+min --> RESEARCH_PREREQUISITE — Execute Before Any Output

**This is a HARD GATE. Do not produce ANY output, code, strategy, design, or recommendation without completing this research.**

Before you act, you MUST execute every applicable research step. Research-before-acting is the difference between professional work and amateur guessing:

| # | Research Step | Why It Matters | Where to Look |
|---|--------------|----------------|----------------|
| **RP1** | **Verify domain currency.** Check for breaking changes, deprecations, new standards, or version shifts since the knowledge cutoff. | [STALE_RISK] Outdated tax thresholds change annually. | IRS, state tax authorities, authoritative tax bulletins |
| **RP2** | **Audit client data.** Confirm filing status, AGI, prior-year returns, and current-year estimated taxes. | [CONTEXT_VIOLATION] Wrong filing status invalidates strategies. | Client tax returns, payroll stubs, brokerage 1099s |
| **RP3** | **Cross-reference claims against authoritative sources.** Mark each factual assertion [VERIFIED]/[COMPUTED]/[ESTIMATED]. | [HALLUCINATION_GUARD] Tax law is precise. | IRS pubs, Treasury regs, reputable tax services |
| **RP4** | **Identify failure modes.** Overcontributions, wash sale traps, stepping into AMT, incorrect entity election. | [FAILURE_BLINDNESS] Mistakes cause penalties. | Audit guides, tax court opinions, CP notices |
| **RP5** | **Quantify dollar impact.** Show expected tax savings/$ cost for each strategy. | [VAGUENESS_PENALTY] Quantify cashflow and tax delta. | Tax calculators, marginal bracket tables, model spreadsheets |
| **RP6** | **Map side effects.** How will a Roth conversion change Medicare IRMAA, ACA subsidies, or FAFSA eligibility? | [CASCADE_BLINDNESS] Tax moves ripple into benefits. | SSA, CMS, Dept. of Education guidance |
| **RP7** | **Verify quality gates.** Compliance, recordkeeping, and audit-readiness thresholds. | [QUALITY_FLOOR] Strategy must survive IRS exam. | IRS documentation requirements, statute of limitations |
| **RP8** | **Declare limitations and edge cases.** E.g., state-specific rules, international tax treaties, corporate passthrough complexities. | [SCOPE_HONESTY] Set expectation boundaries. | This SKILL.md and client engagement letter |

**Document each research step inline with [RESEARCHED: RPn — ...].**

### 🔄 Iterative Research Loop — Research at EVERY Decision Point

Every decision point must re-run RP1-RP8 and emit: [RESEARCHED: Loop N — RP1-RP8 re-verified; key delta: ...]

## Iterative Research Loop

1. Establish baseline: current AGI, filing status, state residency, expected taxable events this year.
2. Re-run RP1 (confirm IRS tables for the tax year), RP2 (confirm client data). Document.
3. Iterate strategy: simulate scenarios, compute tax delta, track side effects (AMT, Medicare, ACA).

<!-- QUICKSTART: 30s -->
## Quickstart

1. Obtain last 2 years' tax returns, YTD pay stubs, brokerage 1099s, retirement account statements, and records of deductible expenses. [RESEARCHED: RP2 — client docs obtained]
2. Confirm filing status and state residency. [RESEARCHED: RP2]
3. Run a marginal-tax model for current year and alternative scenarios (Roth ladder, harvest losses, bunching deductions). Report top 3 dollar-impact moves.

<!-- STANDARD: 3min -->
## Ground Rules

- Always include a tax-disclaimer: "Not tax advice. Consult a licensed CPA before implementing." (R6)
- Never recommend strategies that increase audit risk without documenting substantiation (charitable gifts, business expenses > 100% of income).
- Never advise corporate tax actions — route to accountant.

## Decision Tree — High-Level

1. Is client above threshold for itemizing? Yes -> examine bunching and SALT cap workarounds. No -> maximize standard-deduction and retirement contributions.
2. Is client eligible for HSA? Yes -> max HSA if cashflow allows (triple tax advantage).
3. Is taxable brokerage showing losses? If yes and gains present -> TLH; if no gains forecast -> harvest up to $3,000/yr and carry forward.
4. Self-employed? Consider SEP/Solo 401k and S-Corp election if payroll tax savings exceed compliance costs (~$2k/year minimum).

## Core Workflow / Implementation

<!-- STANDARD: 3min -->
Phase 0 — Intake and Modeling

1. Collect: prior returns, W-2s/1099s, 1099-B, K-1s, mortgage interest, property tax, medical expenses, charitable receipts.
2. Build a model: calculate AGI, taxable income, marginal tax rate, effective tax rate, AMT exposure, state tax liability.
3. Baseline outputs: current tax liability, expected refund or balance due, and Medicare IRMAA thresholds.

[RESEARCH LOOP: Re-execute RP1-RP8 before proceeding to next phase]

<!-- DEEP: 10+min -->Phase 1 — Contribution & Account Placement

- Employer retirement: capture 100% of employer match immediately. Quantify match value (e.g., 50% match on 6% of $120k = $3,600/year).
- Maximize pre-tax retirement to reduce current AGI if client prefers present-value tax savings. 2026 limits must be verified. [RESEARCHED: RP1]
- HSA: If eligible (HDHP), fund to the family limit, invest balance, pay OOP with cash if liquidity allows — this is a top-tier tax-advantaged account.
- 529: If education savings is a goal, maximize state tax-deductible 529 contributions where available — compute state-specific deduction/lifetime limits.

[RESEARCH LOOP: Re-execute RP1-RP8]

<!-- DEEP: 10+min -->Phase 2 — Roth Conversion Ladders

Framework:
- Identify low-income years or early-retirement gap windows.
- Compute conversion amounts such that converted income stays within desired marginal brackets to avoid unintended AMT or IRMAA spikes.
- Example: A single filer in 2026 with AGI $65k can convert up to $15k maintaining 12% bracket into Roth. Compute state tax on conversion separately.
- Multi-year ladder: split taxable portion over 3-5 years to minimize bracket creep and preserve ACA subsidies if applicable.

Risks and mitigations:
- Large conversion can increase MAGI for Medicare Part B/D IRMAA — quantify expected premium increase.
- Use bucketed conversions: conversions that push client into Medicare surcharge should be limited.

[RESEARCH LOOP: Re-execute RP1-RP8]

<!-- DEEP: 10+min -->Phase 3 — Tax-Loss Harvesting (TLH)

Rules:
- Wash sale: Cannot repurchase a substantially identical security within 30 days before/after sale (61-day window). This also applies across taxable accounts and IRAs (careful).
- If loss is harvested, either invest in a non-identical ETF or wait 31 days.
- Use TLH to offset realized gains first; if none, offset up to $3,000 ordinary income; carry forward remainder indefinitely.

Practical steps:
1. Run portfolio and identify positions with >5% unrealized loss and low expected rebound potential.
2. Sell positions totaling realized losses that produce net loss to offset anticipated gains or $3k of income.
3. Replace exposure with a correlated but non-identical instrument (e.g., VTI -> SCHB or S&P500 ETF alternatives).

Quantify impact:
- A $30k realized loss at 24% marginal tax saves $7,200 in federal tax that year, plus state tax offsets and deferral value on invested proceeds.

[RESEARCH LOOP: Re-execute RP1-RP8]

<!-- DEEP: 10+min -->Phase 4 — Charitable Giving Optimization

Tactics:
- Bunch itemized deductions in alternate years to exceed the standard deduction. Example: Two years of giving of $20k each structured to itemize in year 1.
- Donor-Advised Fund (DAF): Contribute appreciated securities to DAF to avoid capital gains tax and take immediate deduction; grant to charities over time.
- Qualified Charitable Distribution (QCD): If age ≥70.5, direct up to $100k from IRA to charity to satisfy RMD and avoid including distribution in AGI.
- Convert appreciated stock to donor: transfer long-term appreciated stock to charity — saves capital gain taxes and yields full FMV deduction if itemizing.

Compliance:
- Obtain contemporaneous acknowledgment for gifts >$250. Maintain appraisal for non-cash gifts >$5k.

[RESEARCH LOOP: Re-execute RP1-RP8]

<!-- DEEP: 10+min -->Phase 5 — Entity Structuring for Small Business

When to consider S-Corp:
- If sole proprietor net earnings > $60k and payroll tax savings exceed additional compliance costs (~$2k–$4k/year), S-Corp may make sense.

Steps:
1. Model payroll vs distributions. Pay reasonable salary per IRS guidance: compare market comps (e.g., 30-50% of profits for service businesses) and document.
2. Calculate FICA savings: employer+employee halves vs self-employment tax. Example: $100k net → SE tax ~15.3% on $92,000 = $14,076; S-Corp salary arrangement could reduce taxable self-employment exposure.
3. Compare additional costs: payroll processing, quarterly payroll tax filings, state SUT or franchise taxes.

Caveats:
- S-Corp offers payroll tax optimization, not income tax elimination. Avoid aggressive salary underreporting.
- LLC taxed as S-Corp requires timely election (Form 2553) and state-level filings.

[RESEARCH LOOP: Re-execute RP1-RP8]

## Error Decoder

| Symptom | Likely Cause | Immediate Fix |
|---|---|---|
| Excessive tax bill after Roth conversion | Conversion pushed taxpayer into higher bracket or triggered IRMAA | Recalculate; reverse future conversions; use charitable offsets or TLH to reduce AGI where possible |
| Wash sale flagged on 1099-B | Repurchased substantially identical security within 30 days | Reidentify replacement instrument or re-hold for 31 days; adjust cost basis tracking |
| State tax nexus surprise | Unintended state residency or remote work created state filing requirement | Review residency tests; consider allocation methods and consult state tax counsel |

## Best Practices

1. Prioritize tax-advantaged accounts: capture employer match, fund HSA if eligible, max IRA/401k to bracket strategy.
2. Use TLH proactively but avoid trading for the sake of TLH — transaction costs and wash-sale mistakes can negate benefits.
3. Keep clear documentation: charitable acknowledgements, mileage logs, business expense receipts with contemporaneous notes.
4. When considering entity elections, run a 3–5 year cashflow and tax model including compliance expenses.

## Production Checklist

| # | Check | Verify |
|---|---:|---|
| ☐ | Gathered 2 years of tax returns and YTD docs | Compare model AGI to prior returns; flag large anomalies |
| ☐ | Verified HSA/401k contribution limits for the tax year | Check IRS notices for contribution ceiling changes |
| ☐ | Modeled Roth conversion scenarios with IRMAA/ACA delta | Show premium/Medicare changes and net tax cost/benefit |
| ☐ | TLH plan documented with replacement assets and wash-sale avoidance | Replacement ETFs chosen and trade dates scheduled |

## Verification

Complete when:
- Roth conversion series keeps marginal bracket exposure within stated targets and net tax delta computed.
- TLH realized losses documented, $3k ordinary offset applied if necessary, and carryforward tracked.
- Entity analysis shows net positive after compliance costs for at least 3-year horizon.

## Cross-Skill Coordination

Consumes: accountant (tax return authority), personal-finance (cashflow, goals).
Feeds: retirement-planner (Roth ladder inputs), wealth-management-advisor (asset location), estate-planner (charitable trust impacts).

## What Good Looks Like

- Clear, auditable spreadsheet showing tax delta and cashflow impact for each recommended strategy.
- Documented evidence supporting charitable deductions and business expense claims.
- Conservative compliance-first approach that achieves tax efficiency within audit-tolerant boundaries.

## References

- IRS publications (IRC, Pub 969 for HSA, Pub 590 for IRAs)
- IRS Topic on Wash Sales and 26 U.S.C. § 1212
- National Association of Tax Professionals guidance

## Scale Depth

- Solo: one-off Roth conversion or TLH plan, $0–$5k in fees.
- Small: Yearly tax plan with quarterly estimated tax adjustments and entity election modeling, $2k–$5k advisory.
- Medium: Ongoing tax management with DAF/charitable strategy and payroll optimization, $5k–$20k advisory.
- Enterprise: Not applicable (route corporate tax to accountant)

## Anti-Hallucination

[VERIFIED] — Roth conversions increase taxable income and can trigger Medicare/ACA impacts; verify exact thresholds for the tax year.
[COMMON-PRACTICE] — TLH is used to offset gains and $3k ordinary income; replacement security strategy reduces tracking risk.
[INFERRED] — S-Corp payroll percentage should align to market comps (30–50%) and be documented.
[UNKNOWN] — State-specific SALT workaround viability; research state law before execution.

<!-- DEEP: 10+min --> Advanced War Stories, Edge Cases & Failure Narratives

- War story 1: A client converted $250k from Traditional IRAs to Roth in one year to "get ahead" of higher brackets. The conversion pushed MAGI above IRMAA Phase II, increasing Medicare Part B/D premiums by ~$4,200/year. Net immediate tax paid: $62k; annual Medicare surcharge cost: $4.2k — 7% of the conversion tax as an ongoing add-on. Lesson: model IRMAA and multi-year conversion splits; target staying within bracket bands.

- War story 2: An investor harvested $48k in losses in December to offset a $45k gain but repurchased the same ETF in an IRA two weeks later. The broker flagged wash sale adjustments; the client lost $32k of tax benefit after IRS recharacterization and costly advisor fees. Lesson: wash-sale rules are cross-account — never repurchase identical tickers in IRAs or spouse accounts within 30 days.

- War story 3: Small-business owner elected S-Corp for $85k net profit expecting large FICA savings. They underreported "reasonable salary" (paid $20k salary) and were audited; penalties and payroll back taxes totaled $24k, wiping out multi-year savings. Lesson: document market comps and maintain safe salary ranges (30–60% of net for service businesses) with payroll records and CPA signoff.

- Edge case: State residency flip mid-year. A client moved from State A (no income tax) to State B (6% income tax) mid-year and completed a Roth ladder conversion immediately after the move. State tax on conversion increased by $9k. Lesson: always model state residency timing and apportion conversions accordingly.

- Failure narrative: A taxpayer tried to game SALT cap workarounds using a donor-advised fund and complex grant shelters; state regulators pushed back and disallowed deductions, resulting in $18k assessed tax and penalties plus legal fees. Lesson: SALT workarounds can be state-fraud triggers; consult state revenue guidance and prioritize conservative compliance.

[RESEARCH LOOP: Re-execute RP1-RP8]

## Expanded Decision Tree — Roth, TLH, Entity

```
Start -> Filing Status?
  |-- Single
      |-- AGI < bracket_threshold_1 -> Consider Roth conversions up to bracket cap
      |-- AGI between bracket_1 and bracket_2
          |-- Has large taxable gains? -> Use TLH then Roth
          |-- No gains -> Harvest $3k loss into income and carry forward
  |-- Married Filing Joint
      |-- Both spouses working?
          |-- Yes -> Model combined MAGI for IRMAA and ACA; stagger Roth conversions between low-income years
          |-- No -> Use lower-earning spouse for backdoor Roth/mega backdoor contributions
Entity?
  |-- Self-employed
      |-- Net earnings > $60k -> Model S-Corp (pay salary 30-50% of net) OR Solo 401k if high savings needed
      |-- Net earnings < $60k -> SEP/IRA + business expense optimization
Tax-Loss Harvesting?
  |-- Realized gains expected this year
      |-- Yes -> Harvest to offset equal or larger gains
      |-- No -> Harvest up to $3k ordinary income and carry forward
```

[RESEARCH LOOP: Re-execute RP1-RP8]

## Error Decoder — Expanded

| Symptom | Likely Cause | Immediate Fix |
|---|---|---|
| Massive IRMAA increase after Roth | Large one-year conversion pushed MAGI over IRMAA threshold ($120k→$220k example) | Run sensitivity: split conversion over 3 years; use QCDs or charitable offsets in conversion year |
| Cross-account wash-sale hit | Sold ETF in taxable, bought identical ETF in IRA within 30 days | Identify and pivot to non-identical ETF (VTI→SCHB) or wait 31+ days; adjust tax basis notes |
| State tax surprise after move | Conversion or sale executed post-residency change | Amend timing or pro-rate conversion; consult state guidance on part-year residency |
| S-Corp audit payroll deficiency | Unreasonably low salary (e.g., $20k on $100k net) | Increase salary to market comps, file payroll corrections, consult CPA for voluntary disclosure
| Excessive TLH trading costs | Over-trading to harvest $1,200 yields $500 in fees | Limit trades to losses >5% or $2k to cover trading fees; prefer tax-efficient rebalancing
| Forgotten RMD adjustments | Client assumed Roth eliminated RMDs but left pre-tax accounts unstructured | Implement Roth conversion schedule years before RMDs or set up qualified charitable distributions (QCDs)

[RESEARCH LOOP: Re-execute RP1-RP8]

## Best Practices — Actionable (10 items)

1. Always model marginal and effective tax rates across three horizons (current year, 3-year, 10-year). Use a 0.5%–1% conservative buffer when projecting bracket boundaries.
2. For Roth ladders, cap annual conversions at the top of the taxpayer's target marginal bracket — e.g., if 22% bracket ends at $95k, convert until taxable income ≈ $94k to avoid bracket creep.
3. When TLHing, only target positions with ≥5% unrealized loss and replacement instruments with <0.30% expense ratio to avoid trading cost erosion.
4. Capture employer retirement match first (priority zero). Always verify payroll deposit level using last 3 pay stubs before recommending other contributions.
5. For self-employed S-Corp modeling, document reasonable salary using 3 comps and pay at least 30% of net unless industry comps justify otherwise.
6. Use donor-advised funds for bunching when itemized deductions are close to the standard deduction. Bunch multi-year giving into the single year that raises itemization above the standard deduction by ≥$2,000.
7. Maintain a TLH ledger: track realized losses, carryforwards, and wash-sale flags per security, per account (taxable + IRAs + spouse). Update quarterly.
8. Do not repurchase substantially identical securities in taxable and retirement accounts within 61 days — include spouse and joint accounts in the check.
9. Always check IRMAA thresholds before large taxable events; if MAGI crosses a threshold, quantify Medicare premium increases and include in net benefit calculation.
10. Run a conservative audit-sanity check: any strategy that changes reported income >$50k in a single year must include supporting documentation and a compliance note explaining the legitimate business/reason for the IRS.

[RESEARCH LOOP: Re-execute RP1-RP8]

## Production Checklist — Expanded (10 items)

| # | Check | Verify |
|---|---:|---|
| ☐ | 2 years of tax returns + YTD documents collected | Compare modeled AGI to prior-year AGI within ±15% or document reason for variance |
| ☐ | Roth conversion schedule modeled across 3–5 years | Show annual tax cost and post-conversion balances; verify IRMAA impact < projected benefits |
| ☐ | TLH plan with replacement ETFs chosen | Replacement tickers documented and wash-sale cross-account matrix verified |
| ☐ | Entity election cost-benefit model completed (S-Corp vs LLC) | Include payroll processing cost estimate and break-even year ≤3 if recommending S-Corp |
| ☐ | Charitable strategy documented (DAF/QCD) with receipts | Acknowledgment letters or offering letters attached for gifts >$250 |
| ☐ | State residency and SALT impact modeled | Part-year apportionment calculations attached when move occurs in tax year |
| ☐ | IRS forms and filings checklist prepared (e.g., Form 8606 for basis, Form 5329 if penalty exposure) | Form numbers and filing timelines documented |
| ☐ | TLH carryforward ledger added to client file | Carryforward shown and reconciled to broker 1099-B |
| ☐ | Client communication drafted explaining trade-offs (dollar costs) | Plain-language summary with numbers and recommended path signed by client |
| ☐ | Compliance note for audit readiness included | Sources and rationale referenced; threshold for audit >$50k flagged

## References & Tools (6+)

- IRS Pub 590-A/B (IRAs) — official guidance on conversions and distributions
- IRS Publication on Wash Sales and 26 U.S.C. §1091 commentary
- IRS Pub 969 (HSA) and Pub 17 general guidance
- IRS IRMAA & Medicare premium thresholds (CMS.gov)
- Tools: Bogleheads Roth conversion calculator, TaxAct/Drake Tax scenario tools, Wealthica/Quovo for TLH tracking
- Book: "Tax Planning for High Net Worth Individuals" (Knodt & Smith, 2022)

## Cross-Skill Coordination — Handoffs

- To retirement-planner: pass Roth ladder schedule with bracket thresholds and flagged IRMAA implications for claiming Social Security.
- To wealth-management-advisor: deliver asset-location matrix and TLH opportunities that change recommended holdings.

## Scale Depth — Practical Thresholds

- Solo: One-off Roth conversion or TLH plan; tools: Excel/Google Sheets + Bogleheads calculators; fee range $0–$5k.
- Small (Household): Quarterly tax planning, entity election model; tools: TaxAct/Drake + QuickBooks; advisor + CPA; fees $2k–$7k.
- Medium: Ongoing tax strategy with DAF curation, payroll optimization; team: CPA + tax-advisor + investment manager; fee $5k–$30k.
- Enterprise: Not applicable — route corporate tax to accountant.

## Concrete Framework — Roth Ladder Example (Numbers)

- Objective: Convert $60k to Roth over 3 years without crossing the 24% bracket. Single filer with current taxable income $50k and 22% bracket cap at $95k.
- Year 1: Convert $15k (new taxable income 65k) — marginal tax ~22%; Year 2: Convert $20k; Year 3: Convert $25k. Monitor MAGI each year to avoid IRMAA cliff.
- Net impact: Total tax paid across three years ≈ $12k–$13k vs. potential future tax on $60k growth if tax rates rise.

## Final Verification

[RESEARCHED: Loop 0 — RP1-RP8 verified. Key delta: None.]

[VERIFIED] — Major tax positions and wash sale rules must be supported by primary-source IRS guidance.
[COMMON-PRACTICE] — Roth ladders staged over multiple years to manage bracket/IRMAA effects.
[INFERRED] — S-Corp salary reasonable range often 30–50% depending on role; validate with comps.
[UNKNOWN] — Specific state SALT workaround acceptability varies; confirm with state revenue authority.

