---
name: angel-investor
description: >
  Angel investing: sourcing dealflow, startup evaluation (TAM, traction, team), term sheet basics, cap table modeling, portfolio construction, follow-on strategy, and QSBS considerations.
license: MIT
author: Sandeep Kumar Penchala
type: personal-finance
status: stable
version: 1.0.0
updated: 2026-08-02
tags:
  - angel-investing
  - startups
  - cap-table
  - term-sheet
  - qsbs
token_budget: 4500
chain:
  consumes_from:
    - personal-finance
  feeds_into:
    - investor-relations
  alternatives: []
---
# Angel Investor
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Actionable angel investing skill: sourcing channels, evaluation frameworks (TAM, unit economics, retention, defensibility), cap table & dilution modeling, term sheet negotiation basics, portfolio construction (Power Law approach), follow-on reserve strategies, secondary sales, and QSBS tax planning. Not for VC fund management.
<!-- QUICK: 30s -->
## <!-- DEEP: 5+min --> RESEARCH_PREREQUISITE — Execute Before Any Output

**HARD GATE: RP1-RP8 before advising on deals.**

| # | Research Step | Why | Where |
|---|---|---|---|
| RP1 | Verify regulatory constraints | Accredited investor rules, securities laws differ | SEC rules, Reg D, state blue sky laws |
| RP2 | Audit startup docs | Cap table, incorporation, prior rounds | Company data room |
| RP3 | Cross-check market data | TAM, comparable exits | Pitch decks, industry reports |
| RP4 | Identify failure modes | Founder mismatch, pivot failure, dilution | Post-mortem analyses |
| RP5 | Quantify impact | Expected ownership after 3 rounds, time-to-exit scenarios | Cap table model, dilution schedule |
| RP6 | Map side effects | Tax treatment (QSBS), liquidity constraints | Tax-strategist input |
| RP7 | Quality gates | Legal docs, IP assignment, founder vesting | Counsel review |
| RP8 | Limitations | Not for institutional fund-level allocation | This SKILL.md |

Document research: [RESEARCHED: RPn — ...].

## Iterative Research Loop

Re-run RP1-RP8 at each tranche decision or term negotiation.

## Quickstart

1. Source: AngelList syndicates, local angel groups, accelerators, warm intros.
2. Evaluate quickly: TAM > $1B for potential unicorn, 3-5x revenue growth/year in early traction, churn <5% monthly for SaaS.
3. Run cap table dilution model for 3 future rounds to estimate ownership at exit.

## Ground Rules

- Expect 80% of deals to fail or return 0; rely on Power Law: one home run covers portfolio losses.
- Avoid over-concentration: target 20–40 deals for early-stage angels to diversify.
- Always run legal diligence: ensure entrepreneur has clear IP assignment and founder vesting schedule.

## Decision Tree

1. Is TAM large enough and defensibility plausible? If no → pass.
2. Does team show repeatable execution and relevant domain expertise? If no → pass.
3. Are unit economics favorable and capital-efficient? If no → negotiate improved terms or pass.

## Core Workflow / Implementation

Phase 0 — Deal Intake & Screening

- 5-minute screen: founder background, traction (revenue/MAU), runway, prior investor list, clear MVP and customer feedback.

[RESEARCH LOOP: Re-execute RP1-RP8 before proceeding to next phase]

<!-- DEEP: 10+min -->Phase 1 — Due Diligence Checklist

- Financial model: monthly burn, gross margin, CAC payback period, LTV/CAC ratio.
- Legal: incorporation jurisdiction, option pool size, existing convertible notes or SAFEs, vesting schedules.
- Product: defensibility, differentiation, tech/IP status.

[RESEARCH LOOP: Re-execute RP1-RP8]

<!-- DEEP: 10+min -->Phase 2 — Cap Table & Dilution Modeling

- Model three rounds: Seed (raise), Series A, Series B. Assume pre-money and raise sizes; apply dilution and option pool increases.
- Example: Invest $100k at $2M pre-money seed for 4.76% pre-option; post-seed ownership diluted by future rounds — model to ~1%–2% at exit depending on follow-ons.

[RESEARCH LOOP: Re-execute RP1-RP8]

<!-- DEEP: 10+min -->Phase 3 — Term Sheet Negotiation Basics

- Key terms: valuation, liquidation preference (1× non-participating standard), anti-dilution protection (avoid full ratchet), pro-rata rights, board seats, founder vesting, option pool expansion pre-money vs post-money.
- Negotiate pro-rata rights for follow-on allocations; reserve 20–40% of initial check for follow-on if you expect winners.

[RESEARCH LOOP: Re-execute RP1-RP8]

<!-- DEEP: 10+min -->Phase 4 — Portfolio Construction & Follow-on Strategy

- Power Law: aim for 1–3 home runs in portfolio. Target 20–40 initial investments; allocate reserve capital of 50% of total deployment for follow-ons into winners.
- Secondary sales: liquidity options depend on investor agreements; be prepared for long holds (7–10+ years).

[RESEARCH LOOP: Re-execute RP1-RP8]

## Tax Considerations (QSBS)

- QSBS Section 1202: Holding qualified small business stock >5 years may exclude up to $10M or 10× basis from gains if qualified. Company must be C-corp, meet active business tests. Coordinate with tax-strategist for structuring.

## Error Decoder

| Symptom | Cause | Fix |
|---|---|---|
| Unexpected dilution | Option pool expanded pre-money without investor consent | Re-negotiate or insist on option pool being carved out pre-money with transparent modeling |
| No quorum for board actions | Multiple investors with blocking rights | Use governance clause to clarify voting thresholds and escalate to mediation if needed |

## Best Practices

- Use standardized safe or convertible instruments for speed; only negotiate complex preferred terms for deals with unique risks or high conviction.
- Keep legal fees low via template documents, but engage counsel for departures from standard terms.

## Production Checklist

- Cap table modeled for 3 rounds
- Legal diligence completed (IP, incorporation, notes)
- QSBS eligibility checked for C-corp startups

## Verification

Complete when projected ownership at exit, expected return multiple per deal, and portfolio-level IRR targets are documented.

## Cross-Skill Coordination

Consumes: personal-finance. Feeds: investor-relations.

## What Good Looks Like

- Diversified angel portfolio, reserve for follow-ons, clear exit and tax plan for QSBS where applicable.

## References

- Y Combinator SAFE, NVCA model, IRS Section 1202 guidance

## Scale Depth

- Solo: individual angel investor model (20–40 deals)
- Small: syndicates and lead investing
- Medium: angel group operations with co-investment funds

## Anti-Hallucination

[VERIFIED] QSBS requires C-corp status and 5-year holding period to qualify for exclusion.
[COMMON-PRACTICE] Power Law governs early-stage returns — few wins dominate returns.
[INFERRED] Reserve 50% of deployment for follow-ons; exact amount depends on conviction.
[UNKNOWN] Specific state Blue Sky exemptions — verify local securities law before investing.

<!-- DEEP: 10+min --> Due Diligence Horror Stories & Advanced Negotiation

- Horror story: An angel invested $50k into an early-stage startup without verifying IP assignment. Post-investment, a prior founder's employer claimed ownership; legal defense costs exceeded $120k and the company pivoted to a non-commercial product. Lesson: require IP assignment agreements and counsel review before funding.

- Negotiation anecdote: Negotiating a 1× non-participating preference vs a 2× participating preference changed expected investor returns dramatically. In one deal, switching to 1× non-participating increased expected investor upside by an estimated 30% at exit assumptions — always model liquidation preference under multiple exit price scenarios.

- Edge case: Founders using complex cap table with multiple convertible instruments and side letters led to unexpected anti-dilution adjustments reducing seed investor ownership from 4.5% to 1.1% after Series A. Lesson: model post-money option pool and convertible cap scenarios comprehensively.

[RESEARCH LOOP: Re-execute RP1-RP8]

## Decision Tree — Screening to Term Sheet

```
Deal Intake -> Quick Screen (5 min)
  |-- Founder credible? (Yes/No)
  |-- Traction adequate? (Users/Revenue) -> if SaaS: 3x revenue growth year-over-year; churn <5% monthly
  |-- Capital efficient? -> runway >12 months with established milestones
Due Diligence -> Legal OK? -> IP assigned, incorporation clean
  |-- Yes -> Term Sheet negotiation
  |-- No -> Decline or conditional term sheet with fix-up
```

[RESEARCH LOOP: Re-execute RP1-RP8]

## Error Decoder — Expanded (8 rows)

| Symptom | Cause | Fix |
|---|---|---|
| IP ownership dispute | Founder failed to assign IP from prior employer or contractor | Require assignment and representations in purchase agreement; escrow if unresolved |
| Dilution from option pool expansion | Option pool created post-money without clarity | Negotiate pre-money pool creation or anti-dilution protection adjustments |
| Mispriced liquidation preference | Poor modeling under multiple exit scenarios | Model 1× non-participating vs 2× participating to show downside to common stock holders |
| SAFE cap mismatch | Ambiguous SAFE terms in later rounds | Reconcile SAFEs with cap table and add protective terms if investing large checks |
| Secondary sale blocked | No transfer provisions or right-of-first-refusal restrictions | Negotiate secondary sale windows or find secondary market buyers with company approval |
| Inadequate pro-rata funding | No reserve for follow-ons leads to dilution | Reserve 20–50% of original allocation for follow-ons in winners |
| Early founder departure | Key founder leaves early without vesting cliff | Ensure vesting cliff and acceleration provisions tied to performance

[RESEARCH LOOP: Re-execute RP1-RP8]

## Best Practices — Angel (10 items)

1. Build a portfolio of 20–40 investments for early-stage exposure reflecting Power Law: expect 70–90% failures, 5–15% moderate wins, 1–3 home runs.
2. Reserve 50% of deployment capital for follow-ons; allocate reserves proportionally to winners by conviction level.
3. Always require IP assignment, no outstanding claims, and clean cap table before funding.
4. Model cap table three rounds forward: seed, A, B with pre and post-money option pool assumptions.
5. Negotiate pro-rata rights and information rights as minimum for meaningful ownership maintenance.
6. Avoid investing more than 5% of net investable capital in a single early-stage deal unless lead-investor diligence justifies larger exposure.
7. Use standard documents (SAFE, NSAs, simple preferred) when possible; engage counsel for non-standard terms.
8. Track key traction metrics monthly (MRR, churn, CAC payback) and require monthly investor updates for >$500k rounds.
9. Consider QSBS planning at investment time: ensure C-corp qualification and track stock issuance dates for 5-year holding requirement.
10. Insist on vesting schedules with cliffs and double-trigger acceleration for founder departures.

[RESEARCH LOOP: Re-execute RP1-RP8]

## Production Checklist — Expanded (10 items)

| # | Check | Verify |
|---|---:|---|
| ☐ | Completed 5-minute screen with founder/traction | Founder CV and product demo attached |
| ☐ | Cap table modeled for 3 rounds | Spreadsheet with dilution scenarios attached |
| ☐ | IP assignment and incorporation docs verified | Counsel memo confirms clean status |
| ☐ | Term sheet drafted with liquidation preference and pro-rata rights | Term sheet PDF in file |
| ☐ | Reserve strategy defined (50% rule) | Capital allocation schedule attached |
| ☐ | QSBS eligibility assessed if C-corp | Counsel memo on 1202 compliance attached |
| ☐ | Legal diligence completed for material risks | Lawyer findings summarized |
| ☐ | Financial model with exit scenarios prepared | Returns under multiple exit valuations attached |
| ☐ | Investor update cadence established | Meeting schedule and KPIs listed |
| ☐ | Secondary sale policy reviewed with founders | Transfer rights and ROFR terms documented |

## References & Tools (7)

- YC SAFE docs and NVCA model term sheets
- IRS Section 1202 (QSBS) guidance and legal analyses
- "Venture Deals" by Brad Feld and Jason Mendelson for term sheet negotiation
- PitchBook and CB Insights for market comps and exits
- Tools: Carta/CapTable management, Google Sheets cap table models, LPA templates
- Counsel: Sample investment counsel checklist from experienced startup lawyers
- Book: "Angel" by Jason Calacanis for sourcing and syndicate tactics

## Cross-Skill Coordination Additions

- To tax-strategist: provide transaction structure for QSBS planning and anticipated holding schedules.
- To investor-relations: hand off communication templates and investor update cadence for syndicate management.

## Scale Depth — Deployment & Team

- Solo: Angel investor with 20–40 deals using Carta + Google Sheets; deployment <$500k/year.
- Small: Syndicate lead or platform investor coordinating 50–200 deals; team includes part-time counsel and analyst.
- Medium: Angel group with pooled capital and committed follow-on fund; team includes fund admin and legal.

## Concrete Framework — Cap Table Modeling Example

- Seed investment: $100k into $2M pre-money → ownership 4.76% pre-option. Model Series A: $5M pre-money with 20% option pool expansion premoney reduces founder and investors accordingly. Projected diluted ownership at exit often drops to ~1–2% depending on follow-on participation.

[RESEARCH LOOP: Re-execute RP1-RP8]

[VERIFIED] QSBS requires C-corp status and 5-year holding period for exclusion.
[COMMON-PRACTICE] Reserve 50% for follow-ons in early-stage portfolios.
[INFERRED] Cap table dilution modeling should always include pre-money option pool assumptions.
[UNKNOWN] State Blue Sky exemptions — verify with counsel before cross-state syndication.

