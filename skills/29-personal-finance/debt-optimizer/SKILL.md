---
name: debt-optimizer
description: >
  Debt optimization: avalanche vs snowball, refinancing models, student loan strategies (PSLF, IDR), mortgage paydown vs invest analysis, and HELOC/margin considerations.
license: MIT
author: Sandeep Kumar Penchala
type: personal-finance
status: stable
version: 1.0.0
updated: 2026-08-02
tags:
  - debt
  - refinancing
  - student-loans
  - mortgage
  - credit-score
token_budget: 4500
chain:
  consumes_from:
    - personal-finance
  feeds_into:
    - tax-strategist
    - real-estate-investor
  alternatives: []
---
# Debt Optimizer
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Focused debt management skill: model avalanche vs snowball, refinance timing, student loan optimization (PSLF, SAVE), mortgage payoff vs invest analysis, credit optimization, HELOC and margin loan hazard analysis. Not for corporate debt strategy.
<!-- QUICK: 30s -->
## <!-- DEEP: 5+min --> RESEARCH_PREREQUISITE — Execute Before Any Output

**HARD GATE: RP1-RP8 required.**

| # | Research Step | Why | Where |
|---|---|---|---|
| RP1 | Verify interest rate environment | Refinance decisions depend on current yields | Freddie Mac, Fed, lender rate sheets |
| RP2 | Audit debt inventory | List balance, APR, term, secured/unsecured | Client statements |
| RP3 | Cross-check care programs | PSLF rules and IDR latest changes | ED/servicer guidance |
| RP4 | Identify failure modes | Refinance traps, prepayment penalties, variable-rate shock | Note docs, ARM caps |
| RP5 | Quantify impact | Interest saved by refinancing, opportunity cost of early payoff | NPV and IRR models |
| RP6 | Map side effects | Prepaying mortgage vs investment tax consequences | Tax-strategist input |
| RP7 | Quality gates | Ensure no loan covenants or tax events stop strategies | Loan docs, tax regs |
| RP8 | Limitations | Not for corporate treasury-level leverage | This SKILL.md |

Document research with [RESEARCHED: RPn — ...].

## Iterative Research Loop

At every refinance or consolidation decision, re-run RP1-RP8 and record deltas.

## Quickstart

1. Inventory all debts: balance, interest, minimum payment, due dates, secured status.
2. Compute weighted average interest rate and prioritize >8% as emergency targets for avalanche.
3. For student loans, determine federal vs private and explore PSLF/IDR eligibility and savings.

## Ground Rules

- Avalanche is mathematically optimal (highest APR first) — provide snowball as behavioral alternative with explicit cost tradeoff.
- Do not refinance federal student loans into private loans if PSLF, IDR forgiveness, or special forbearances are available.
- Avoid using retirement assets (401k loans except as last resort) to pay consumer debt because of lost compounding and tax penalties.

## Decision Tree

1. Is there >8% unsecured debt? → Prioritize avalanche and consider balance transfer at 0% if fee <3% and paydown can be completed before promo expires.
2. Is mortgage rate > current market rate by ≥1% and expected hold >3 years? → Refinance if closing costs amortize within expected hold period.
3. Student loan: federal -> assess PSLF/IDR; private -> refinance to lower rate if no PSLF path.

## Core Workflow / Implementation

Phase 0 — Intake & Baseline

- Compile balances and compute current amortization schedules and total interest remaining.
- Compute monthly cashflow freed by refinancing or paydown scenarios.

[RESEARCH LOOP: Re-execute RP1-RP8 before proceeding to next phase]

<!-- DEEP: 10+min -->Phase 1 — Avalanche vs Snowball

- Avalanche model: simulate paying min on all loans and extra on highest APR. Compute total interest saved and months shortened.
- Snowball model: extra payments on smallest balance first; compute psychological benefit score and cost in interest.

Example: $12k @22% credit card vs $25k @4% student loan. Avalanche directs extra to 22% which saves thousands over snowball.

[RESEARCH LOOP: Re-execute RP1-RP8]

<!-- DEEP: 10+min -->Phase 2 — Refinancing & Consolidation

- For mortgage refinance: compute APR/points tradeoff, breakeven months, and closing cost amortization: breakeven months = points / (monthly_savings).
- For credit cards: consider 0% balance transfer offers with fee = 3% and term 12–18 months; compare interest saved vs fee and ability to pay.

[RESEARCH LOOP: Re-execute RP1-RP8]

<!-- DEEP: 10+min -->Phase 3 — Student Loan Optimization

- PSLF path: track qualifying payments, employer certification, and schedule consolidation only if it preserves PSLF eligibility.
- IDR/SAVE: model payments as % discretionary income; simulate forgiveness horizon and tax exposure on any forgiven amount (as per law). Use income-driven plan if payments < standard repayment and forgiveness horizon acceptable.

[RESEARCH LOOP: Re-execute RP1-RP8]

<!-- DEEP: 10+min -->Phase 4 — Mortgage Paydown vs Invest

- Compare guaranteed return of paying mortgage (APR) vs expected after-tax net return of investing (assume 6–7% after inflation long-term). Use NPV and risk-adjusted comparison.
- If mortgage rate <4% and investor can earn >6% net, investing often wins; for rates >6–7%, paying down mortgage is often optimal.

[RESEARCH LOOP: Re-execute RP1-RP8]

## Error Decoder

| Symptom | Cause | Fix |
|---|---|---|
| Refinanced into longer term accidentally | Chasing lower monthly payment but adding years | Recalculate total interest; if unacceptable, refinance again or make principal prepayments |
| Lost PSLF credit after consolidation | Consolidation with wrong servicer or private consolidation | Re-examine paperwork; seek special remedy via servicer escalation and document employer certification |

## Best Practices

- Keep a 3-6 month emergency fund before aggressive debt paydown to avoid re-borrowing at higher rates.
- Use amortization transparency: provide a schedule for every scenario and show interest saved vs time.
- Consider balance-transfer as bridge, not cure: only if disciplined paydown is possible.

## Production Checklist

- All debts inventoried and validated
- Refinance breakeven < expected hold period
- PSLF/IDR eligibility verified with employer certification if pursued

## Verification

Complete when net present value of chosen strategy is positive vs alternatives and client liquidity/behavioral constraints are satisfied.

## Cross-Skill Coordination

Consumes: personal-finance. Feeds: tax-strategist, real-estate-investor.

## What Good Looks Like

- Clear amortization schedules, documented refinancing rationale, and an actionable payment plan with dates and amounts.

## References

- Federal Student Aid PSLF guidance, Freddie Mac quarterly rates, CFPB consumer debt guides

## Scale Depth

- Solo: individual debt plan
- Small: household-level refinancing and student-loan navigation
- Medium: multiple household consolidation and portfolio refinancing

## Anti-Hallucination

[VERIFIED] Avalanche saves more interest than snowball (mathematically). [COMMON-PRACTICE] Snowball used for behavioral wins. [INFERRED] Break-even months for points darken with shorter expected hold period. [UNKNOWN] Future legislative forgiveness programs — check current law.

<!-- DEEP: 10+min --> Complex Scenarios, Real Examples & Pitfalls

- Example: Borrower refinanced into a 30-year mortgage at a lower rate but extended term from 15 to 30 years; monthly payment fell by $400 but total interest increased by $120k over loan life. Lesson: analyze total interest and breakeven period, not just monthly cashflow.

- Student loan trap: Borrower consolidated federal loans into private refinance to get a 3% rate, losing PSLF eligibility. Ten years later, employer public service layoffs would have qualified them for forgiveness; lost benefit >$120k. Lesson: preserve federal loan status until PSLF/IDR pathway conclusively exhausted.

- HELOC misuse: Homeowner used HELOC to bridge cashflow for variable income; interest rate reset caused payments to double and foreclosure risk when market rates rose. Lesson: only use HELOCs for high-ROI short-term needs and cap draw at 50% of emergency fund.

[RESEARCH LOOP: Re-execute RP1-RP8]

## Expanded Decision Tree — Refinance, Paydown, Consolidate

```
Debt Inventory -> Prioritize
  |-- Any debt APR > 8%? -> Emergency: avalanche focus, consider balance transfer with fee <3%
  |-- Mortgage rate > market by ≥1%? -> Refinance if breakeven months < expected hold
  |-- Student loans federal? -> Evaluate PSLF/IDR; do NOT refinance to private unless PSLF impossible
  |-- HELOC question? -> Only if short-term ROI > HELOC APR + 2% buffer
```

[RESEARCH LOOP: Re-execute RP1-RP8]

## Error Decoder — Expanded (7 rows)

| Symptom | Cause | Fix |
|---|---|---|
| Refinance increases total interest | Chose longer term to lower payment | Recalculate total interest; if unacceptable, refinance again or accelerate principal payments
| Lost PSLF credit after private consolidation | Consolidated federal into private loans | Can't return—re-evaluate relief options; avoid private refinance until PSLF path closed
| Balance transfer fee larger than savings | 3% fee on $10k transfers may cost $300 vs interest saved of $200 | Only transfer if projected interest saved > fee + buffer
| Variable-rate shock (ARM/HELOC) | Index + margin spikes cause payment shock | Refinance to fixed or set aside 12–24 months of payment reserves
| Credit score hit after mass inquiries | Rapid rate-shopping and new credit | Use rate quotes (soft pull) when possible; stagger applications
| Improper tax treatment of forgiven debt | IDR forgiveness expectations change | Model tax treatment; recent law may exclude certain IDR forgiven amounts—consult current law
| Margin loan liquidation | Using margin for investments without guardrails | Implement stop-loss and pre-funded cash buffer; avoid margin if illiquid

[RESEARCH LOOP: Re-execute RP1-RP8]

## Best Practices — Concrete (10 items)

1. Prioritize paying off any unsecured debt >8% APR before investing in taxable accounts.
2. Keep emergency fund 3–6 months before aggressive payoff; with variable income favor 6–12 months.
3. Compute refinance breakeven months = closing_costs / monthly_savings; require breakeven < expected hold period (default 36 months).
4. For balance transfers, only accept if fee <3% and paydown plan clears balance before promo end.
5. Preserve federal student loan status unless PSLF/IDR path impossible; consult servicer before consolidating.
6. Use NPV analysis on mortgage paydown vs invest with conservative expected after-tax return (6% nominal) and personal discount rate.
7. Avoid using retirement accounts for consumer debt; net cost includes lost compounding and tax penalties.
8. When using HELOC/ARM, cap exposure such that potential payment rise of +3% does not increase debt service >30% of net income.
9. Maintain credit utilization <30% for scoring health; target <10% for best rate access.
10. Re-run debt plan annually and after any rate environment change or major income event.

[RESEARCH LOOP: Re-execute RP1-RP8]

## Production Checklist — Expanded (10 items)

| # | Check | Verify |
|---|---:|---|
| ☐ | Complete inventory of all debts with APR, term, secured status | Statements attached for each liability |
| ☐ | Weighted average interest rate computed | Calculation and summary included |
| ☐ | Avalanche vs Snowball NPV comparison produced | Show total interest saved and time to payoff |
| ☐ | Refinance breakeven calculation for mortgages | Breakeven months documented and compared to hold horizon |
| ☐ | PSLF/IDR eligibility checked with employer certs | Employer certification forms or correspondence attached |
| ☐ | HELOC/ARM risk stress test completed | Payment sensitivity to +200/300 bps increase modeled |
| ☐ | Credit impact forecast included | Expected score changes and timeline for recovery modeled |
| ☐ | Debt payoff schedule with dates and amounts created | Amortization tables attached |
| ☐ | Behavioral plan (snowball triggers) documented if used | Psychological milestones and small-win schedule present |
| ☐ | Client acceptance and signatures on plan | Written confirmation saved in client file |

## References (6)

- CFPB guides on mortgages and balance transfers
- Federal Student Aid PSLF and IDR program pages
- Freddie Mac Primary Mortgage Market Survey for current rate context
- CFPB debt collection and consumer protections
- Book: "Your Money or Your Life" (Vicki Robin) for behavioral context
- Tools: Bankrate refinance calculator, StudentAid.gov PSLF Help Tool

## Cross-Skill Coordination Additions

- To tax-strategist: pass large debt forgiveness projections and tax implications for IDR/PSLF cases.
- To real-estate-investor: coordinate when mortgage paydown vs reinvestment into properties is being considered.

[RESEARCH LOOP: Re-execute RP1-RP8]

[VERIFIED] Avalanche saves more interest than snowball mathematically.
[COMMON-PRACTICE] Snowball used for behavioral wins at known cost.
[INFERRED] HELOC risk increases significantly when rates rise >300 bps.
[UNKNOWN] Future student loan legislative changes — verify current laws.

