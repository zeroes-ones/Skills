---
name: retirement-planner
description: >
  Retirement planning: withdrawal sequencing, 401k/IRA optimization, Social Security claiming strategies, pension vs annuity evaluation, and sequence-of-returns risk mitigation.
license: MIT
author: Sandeep Kumar Penchala
type: personal-finance
status: stable
version: 1.0.0
updated: 2026-08-02
tags:
  - retirement
  - social-security
  - ira
  - 401k
  - sequence-of-returns
  - pension
token_budget: 4500
chain:
  consumes_from:
    - personal-finance
    - tax-strategist
  feeds_into:
    - estate-planner
    - wealth-management-advisor
  alternatives: []
---
# Retirement Planner
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Comprehensive retirement planning skill: FIRE math (4% rule with guardrails), VPW/Variable Percentage Withdrawal, tax-aware account sequencing, Social Security optimization using actuarial breakeven analysis, pension lump-sum vs annuity modeling, healthcare cost projections, and Monte Carlo stress tests for sequence-of-returns risk. Not for corporate retirement plan administration.
<!-- QUICK: 30s -->
## <!-- DEEP: 5+min --> RESEARCH_PREREQUISITE — Execute Before Any Output

**This is a HARD GATE. Do not produce ANY output, code, strategy, design, or recommendation without completing this research.**

| # | Research Step | Why It Matters | Where to Look |
|---|--------------|----------------|----------------|
| RP1 | Verify domain currency | Benefit formulas and actuarial tables change; Social Security rules update | SSA tables, official actuarial sources |
| RP2 | Audit client data | Retirement ages, pension terms, healthcare eligibility, existing balances | Statements, pension docs, Medicare guidance |
| RP3 | Cross-reference claims | All rate assumptions must be cited | Morningstar, Treasury yield curves |
| RP4 | Identify failure modes | Running out of money, early retirement funding gaps | Sequence-of-returns literature |
| RP5 | Quantify impact | Show dollar outcomes and probabilities | Monte Carlo, deterministic scenarios |
| RP6 | Map side effects | Roth conversions impact Medicare/ACA benefits | SSA, CMS docs |
| RP7 | Quality gates | Fiduciary thresholds and stress-test criteria | Firm policies, regulatory guidance |
| RP8 | Declare limitations | Not for complex corporate pensions or ERISA plan administration | This SKILL.md |

Document each result with [RESEARCHED: RPn — ...].

### Iterative Research Loop

At each decision (claim SS age, run Roth ladder, pick withdrawal method), re-run RP1-RP8 and emit [RESEARCHED: Loop N — ...].

## Quickstart

1. Gather balances (401k, IRA, Roth, taxable), projected retirement age, expected Social Security earliest/primary/late claiming amounts (SSA statement), pension paperwork.
2. Run three scenarios: conservative (4% real withdrawal, 2% inflation), baseline (3.5% real), optimistic (5% real). Include tax drag and required minimum distributions.
3. Provide recommended claiming age and withdrawal sequence with dollar-by-dollar example from ages 62–95.

## Ground Rules

- Never assume a guaranteed return >3% real for planning; model multiple return regimes.
- Do not recommend a single static withdrawal rate without stress-testing against a 30-year horizon.
- Prioritize minimax longevity — preserve a 90% success probability in Monte Carlo for baseline plan.

## Decision Tree

1. Can client tolerate 25% drawdown? If no and retirement <10 years, shift to more conservative asset mix or delay retirement.
2. Is pension present? Compute actuarial lump-sum vs annuity NPV at client discount rate and mortality assumptions.
3. Social Security claiming: compute breakeven ages between claiming at 62, FRA, and 70; adjust for health and spousal options.

## Core Workflow / Implementation

Phase 0 — Intake & Baseline Modeling

- Collect balances, expected retirement age, planned lifestyle spending (inflation-adjusted), expected pensions, and health insurance assumptions.
- Baseline: compute replacement ratio (target gross spending/last salary), safe withdrawal rate using multiple scenarios.

[RESEARCH LOOP: Re-execute RP1-RP8 before proceeding to next phase]

<!-- DEEP: 10+min -->Phase 1 — Asset Allocation & Glidepath

- Use age-based starting allocation: equity % = 110 - age as starting rule; adjust by risk capacity and time to retirement.
- Design bond ladder for the first 10 years of withdrawals to reduce sequence-of-returns risk: target ladder = annual withdrawal × 10 years. Use TIPS/Cash for immediate needs.

[RESEARCH LOOP: Re-execute RP1-RP8]

<!-- DEEP: 10+min -->Phase 2 — Withdrawal Sequencing

Priority sequence examples:
- Traditional-first: taxable → tax-deferred → Roth (if trying to minimize taxable income early to reduce RMDs later).
- Roth-first: Roth → taxable → tax-deferred (if seeking to reduce taxable income near Social Security claiming or Medicare thresholds).
- Bucket approach: Short-term (3–7 years cash/T-bills), Medium (7–15 years bonds), Long-term (stocks).

Provide concrete example: $1M portfolio, annual spending $40k (4%), taxable savings $200k, pre-tax IRAs $600k, Roth $200k: recommend taxable to preserve flexibility, Roth conversions in low-tax years.

[RESEARCH LOOP: Re-execute RP1-RP8]

<!-- DEEP: 10+min -->Phase 3 — Social Security Claiming

- Compute primary insurance amount (PIA) and benefit at age 62, FRA, 70; compute breakeven ages and survivor impacts.
- Example: If FRA benefit $30k/year, claiming at 62 reduces to ~$22.5k (25% reduction), at 70 increases ~32% vs FRA. Breakeven often near age 78–82 depending on discount rate.
- Consider spousal strategies, restricted application nuances (where applicable), and divorced spouse entitlements.

[RESEARCH LOOP: Re-execute RP1-RP8]

<!-- DEEP: 10+min -->Phase 4 — Pension Lump-Sum vs Annuity

- Compute present value of annuity using safe discount rate (e.g., Treasury strip + spread) and longevity assumptions.
- Compare lump-sum invested by client with conservative drawdown plan. Include fees, inflation adjustments, and insurer credit risk.
- Rule of thumb: take lump sum if you can invest at a long-term real return > annuity implied rate and you have bequest preference.

[RESEARCH LOOP: Re-execute RP1-RP8]

<!-- DEEP: 10+min -->Phase 5 — Healthcare & Long-Term Care Modeling

- Project Medicare premiums and supplemental Medigap or Medicare Advantage costs; compute IRMAA triggers based on MAGI.
- Model LTC probabilities by age cohort and estimate expected annual LTC cost (US median private-pay nursing home ~$120k/year in many markets). Recommend insurance purchase if expected cost > self-insurance capacity and premium is <4% of assets annually.

[RESEARCH LOOP: Re-execute RP1-RP8]

## Error Decoder

| Symptom | Cause | Fix |
|---|---|---|
| Portfolio depletion in simulation | Too high withdrawal rate or poor sequence | Reduce withdrawal by 0.5–1%, delay retirement 2–3 years, or adopt dynamic withdrawal (VPW) |
| Unexpected tax spike at 72 | RMDs kick in and cause higher AGI | Model RMDs earlier with Roth conversions to smooth taxable income |

## Best Practices

- Use glidepath and buckets to manage sequence-of-returns risk.
- Favor flexibility: maintain a taxable buffer to avoid forced selling in down markets.
- Use Roth ladders opportunistically in low-income years to reduce lifetime tax drag.

## Production Checklist

- Client balance data collected and validated.
- Three scenario projections (conservative/base/optimistic) with Monte Carlo probabilities.
- Social Security breakeven table and recommended claiming age with rationale.

## Verification

Complete when: plan satisfies >90% success probability on baseline Monte Carlo or client accepts risk tradeoffs documented.

## Cross-Skill Coordination

Consumes: personal-finance, tax-strategist. Feeds: estate-planner, wealth-management-advisor.

## What Good Looks Like

- Clear age-by-age cashflow plan, Social Security claiming recommendation, Roth conversion schedule if applicable, and a bond ladder to cover first 10 years of withdrawals.

## References

- Social Security Administration calculators and PIA rules
- Bengen/Trinity studies on safe withdrawal rates

## Scale Depth

- Solo: Retirement readiness check and claiming recommendation
- Small: Full retirement income plan with Roth ladder and healthcare model
- Medium: Ongoing advice with pension/annuity negotiation and taxable restructuring
- Enterprise: Not applicable

## Anti-Hallucination

[VERIFIED] Social Security benefits depend on PIA and claiming age per SSA rules.
[COMMON-PRACTICE] Use of a 10-year bond ladder to mitigate sequence-of-returns risk.
[INFERRED] Roth conversion sizing should avoid IRMAA cliffs where possible.
[UNKNOWN] Future legislative changes to Social Security or Medicare premiums beyond 2026.

<!-- DEEP: 10+min --> Advanced Case Studies & Failure Modes

- Case study: A client attempted FIRE at 58 with a $1.2M portfolio and 4% rule assumptions. A 2000–2002-style sequence-of-returns (−40% first 3 years) dropped portfolio to $720k. Switching to VPW reduced withdrawals to 2.6% and forced lifestyle cuts. Loss: projected 30-year spending reduced by ~$18k/year. Lesson: test extreme negative-return scenarios and maintain a 2–5 year bond ladder to cover withdrawals.

- Failure mode: Ignoring Medicare IRMAA when doing Roth conversions. A married couple converted $120k in one year, pushing their MAGI into IRMAA surcharges; cumulative Medicare premium increase exceeded tax savings that year. Mitigation: spread conversions, use QCDs, or convert in years with lower MAGI.

- Edge case: Pension survivor benefit overlooked. A client took lump-sum pension instead of 60% joint-and-survivor annuity. After the spouse's early death, the surviving spouse lost ~$35k/yr in guaranteed income. Lesson: model survivor scenarios with longevity and health assumptions.

[RESEARCH LOOP: Re-execute RP1-RP8]

## Expanded Decision Tree — Withdrawal & Claiming

```
Retirement Plan Start -> Primary Goal?
  |-- Maximize Income
      |-- Pension available?
          |-- Yes -> Compute lump-sum vs annuity NPV
              |-- Lump-sum if investable return > annuity implied rate + risk premium
              |-- Annuity if desire inflation-protected guaranteed stream or spouse survivor need
          |-- No -> Sequence of withdrawals
              |-- Sequence choice -> Tax-aware: (Taxable → Traditional → Roth) OR Flexibility-first: (Roth → Taxable → Traditional)
  |-- Minimize Longevity Risk
      |-- Use annuitization for portion (20–40%) + bucket strategy for rest
Social Security Claiming -> Health & Life Expectancy?
  |-- Good health & family history longevity >85 -> defer to 70
  |-- Poor health or caregiving needs -> claim early (62–FRA) with conservative withdrawal offsets
```

[RESEARCH LOOP: Re-execute RP1-RP8]

## Error Decoder — Expanded (6 rows)

| Symptom | Cause | Fix |
|---|---|---|
| Early portfolio depletion | Withdrawal rate > sustainable for given sequence-of-returns | Reduce withdrawals by 0.5–1%, rebalance to conservative mix, delay retirement if possible |
| IRMAA surprise after Roth | Massive conversion/spike in MAGI | Model in advance; split conversions; use QCDs to reduce MAGI |
| Pension undervaluation | Discount rate assumption too high | Recompute PV with conservative Treasury + spread; include inflation adjustments |
| RMD tax shock at 73 | Failure to model RMDs into cashflow | Implement Roth conversions earlier to reduce RMD base |
| Healthcare black swan | Early chronic illness raising costs beyond model | Re-run LTC model; consider LTC insurance or hybrid product |
| Incorrect Social Security spousal claim | Misinterpretation of ex-spouse/ survivor rules | Re-evaluate using SSA tools and consult estate planner for survivor sequences |

[RESEARCH LOOP: Re-execute RP1-RP8]

## Best Practices — Concrete (10 items)

1. Target bond-cash ladder covering 7–10 years of planned withdrawals (e.g., for $50k annual spending, ladder = $350k–$500k in short-duration bonds/TIPS).
2. Use three-scenario Monte Carlo: conservative (2% real), baseline (4% real), optimistic (6% real). Demand ≥90% success on baseline to recommend standard plan.
3. For Social Security, run breakeven and probability-weighted outcomes; if breakeven > expected survival age by >5 years, prefer deferral.
4. Limit initial safe withdrawal rate to 4% or VPW equivalent; reduce to 3.25–3.5% for early retirements (<60) to preserve longevity.
5. Schedule Roth conversions to avoid bumping MAGI across IRMAA or ACA cliffs; model state tax impact separately.
6. Rebalance with tax-efficient methods: use new contributions and harvest losses before selling appreciating taxable lots.
7. Maintain a taxable buffer of 12–24 months of spending for retirees to avoid forced sales in down markets.
8. Update retirement plans annually and after major events (marriage, death, home sale, job change) — use a checklist and automated reminders.
9. Use annuitization only for a defined floor (20–40% of necessary income) to balance longevity risk and liquidity.
10. For clients with pensions, run both lump-sum investable scenario and annuity NPV; choose lump-sum only if net after-tax expected return > annuity rate and client can tolerate investment risk.

[RESEARCH LOOP: Re-execute RP1-RP8]

## Production Checklist — Expanded (10 items)

| # | Check | Verify |
|---|---:|---|
| ☐ | All account balances updated and verified | Statements within 30 days present for all accounts |
| ☐ | Monte Carlo runs completed (3 scenarios) | Baseline success probability documented ≥ target (default 90%) |
| ☐ | Social Security PIA and claim ages modeled | Breakeven ages computed and documented |
| ☐ | Roth conversion schedule (if any) created | Annual tax cost and post-conversion balances attached |
| ☐ | Bond ladder plan for years 1–10 created | Securities chosen and ladder dates scheduled |
| ☐ | Healthcare cost projections included | IRMAA and Medicare supplemental costs estimated by age 65/70 |
| ☐ | Annuity vs lump-sum analysis completed | Present value and credit risk notes included |
| ☐ | LTC analysis performed if client risk > self-insurance capacity | Premium vs expected PV compared, threshold trigger set |
| ☐ | Withdrawal policy/IPS documented and signed | ISR triggers and dynamic withdrawal rules stated |
| ☐ | Client acceptance documented | Client signature or written confirmation on plan decisions |

## References & Tools (6+)

- "The 4% Rule and Safe Withdrawal," William Bengen and Trinity study papers
- Social Security Administration calculators and PIA rules
- Morningstar Retirement Manager and Vanguard Retirement Income Model
- CMS IRMAA and Medicare premium tables (CMS.gov)
- Tools: FIRECalc, cFIREsim, Vanguard retirement income tools

## Cross-Skill Coordination Additions

- To tax-strategist: send Roth conversion schedule with projected MAGI by year and IRMAA modeling details.
- To estate-planner: confirm how pension survivor elections interact with estate liquidity planning.

## Scale Depth — Tools & Triggers

- Solo: retirement readiness check using Excel + FIRECalc; <$500k investable assets; single-advisor engagement.
- Small: full retirement income plan with Monte Carlo (Vanguard/Morningstar tools); $500k–$3M assets; team: planner + CPA.
- Medium: Ongoing plan with pension negotiation and healthcare/LTC modeling; $3M–$50M; team: planner + investment PM + actuary + CPA.
- Enterprise: large institution or corporate plan — route to specialized retirement consultants.

## Concrete Framework — VPW Example

- Variable Percentage Withdrawal (VPW): For a $1M portfolio at retirement, VPW table suggests initial withdrawal ~4.2% (adjusted each year by portfolio value and remaining life expectancy). For a 30-year horizon, compute table and apply 3–5% guardrails.

## Final Verification

[RESEARCHED: Loop 0 — RP1-RP8 verified. Key delta: None.]

[VERIFIED] Social Security PIA rules per SSA.
[COMMON-PRACTICE] Use of 10-year bond ladder for sequence-of-returns mitigation.
[INFERRED] VPW reduces depletion risk compared to static 4% in adverse markets.
[UNKNOWN] Future Medicare premium rules beyond current CMS tables.

