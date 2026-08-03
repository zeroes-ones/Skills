---
name: wealth-management-advisor
description: >
  Holistic wealth management: multi-goal optimization, asset location, concentrated position management, family office primitives, and philanthropy strategy for high-net-worth individuals.
license: MIT
author: Sandeep Kumar Penchala
type: personal-finance
status: stable
version: 1.0.0
updated: 2026-08-02
tags:
  - wealth-management
  - asset-location
  - concentrated-positions
  - family-office
  - philanthropy
token_budget: 4500
chain:
  consumes_from:
    - tax-strategist
    - retirement-planner
    - estate-planner
    - personal-finance
  feeds_into:
    - family-office
  alternatives: []
---
# Wealth Management Advisor
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Comprehensive wealth management for high-net-worth (HNW) individuals and families: multi-goal optimization, asset location rules, withdrawal optimization, concentrated position remediation (exchange funds, collars), alternative investments, and philanthropic planning. Not for institutional asset management.
<!-- QUICK: 30s -->
## <!-- DEEP: 5+min --> RESEARCH_PREREQUISITE — Execute Before Any Output

**HARD GATE: RP1-RP8 mandatory.**

| # | Research Step | Why | Where |
|---|---|---|---|
| RP1 | Verify regulatory boundaries | Securities rules and private placement limits | SEC, FINRA, private placement memos |
| RP2 | Audit client constraints | Liquidity needs, risk tolerances, KYC/AML flags | Client onboarding docs |
| RP3 | Cross-reference fees and performance | Net-of-fee expectations | Manager LPA, fund docs |
| RP4 | Identify failure modes | Concentration failure, liquidity crunch | Historical HNW case studies |
| RP5 | Quantify impact | Tax drag, opportunity cost, carry fees | Scenario modeling |
| RP6 | Map side effects | Estate tax, family governance issues | Estate-planner input |
| RP7 | Quality gates | Fiduciary standard, conflict disclosure | Fiduciary policies |
| RP8 | Declare limitations | Not for institutional asset management | This SKILL.md |

Document results with [RESEARCHED: RPn — ...].

## Iterative Research Loop

Re-run RP1-RP8 at every portfolio adjustment or alternative investment allocation.

## Quickstart

1. Run multi-goal optimizer: list goals (retirement, education, liquidity, philanthropy) with target dollar amounts and timelines.
2. Compute after-tax returns by account type and move tax-inefficient assets to tax-deferred accounts where possible.
3. For concentrated stock positions, compute exchange fund or partial sale with hedging alternatives and model tax-cost basis.

## Ground Rules

- Asset location trumps tactical asset allocation when tax optimization matters — place tax-inefficient assets (taxable bonds, REITs) into tax-deferred accounts when feasible.
- For HNW, maintain liquidity reserves: 1–3 years of planned liquidity depending on private investments and income stability.
- Avoid overleveraging liquid portfolios to fund illiquid alternative investments unless explicit risk controls exist.

## Decision Tree

1. Is client > $5M liquid net worth? Family office primitives apply: governance, multi-gen planning, private market access.
2. Does client hold concentrated equity >20% of investable assets? If yes: evaluate exchange funds, collars, and structured sales over multiple years to manage tax.
3. Are alternative allocations >10%? If yes: due diligence checklist for manager selection and liquidity projections.

## Core Workflow / Implementation

Phase 0 — Onboarding & Goal Definition

- Collect full financial picture and define goals with horizon and probability of success target.
- Build consolidated balance sheet and cashflow model for planning horizon.

[RESEARCH LOOP: Re-execute RP1-RP8 before proceeding to next phase]

<!-- DEEP: 10+min -->Phase 1 — Asset Location & Tax-Efficiency

- Tax-efficiency ranking: Taxable accounts: equities (low turnover) > tax-exempt muni bonds > REITs/bond funds (hold in tax-deferred). Place index funds with low turnover in taxable when possible.
- Compute tax drag difference: e.g., a 1% higher expense ratio or 1% higher tax drag on $5M = $50k/year loss.

[RESEARCH LOOP: Re-execute RP1-RP8]

<!-- DEEP: 10+min -->Phase 2 — Concentrated Position Management

Options:
- Exchange fund: swap concentrated appreciated stock into diversified pooled vehicle, defer capital gains, but accept lock-up and fees.
- Collar: sell covered calls and buy puts to limit downside while funding cost via premium income.
- Structured sale: use forward sale or prepaid forward with tax deferral, requires counsel.

Quantify: Sell 20% of a $10M concentrated position over 5 years in 4 equal tranches to stay within long-term capital gains brackets and use tax-loss harvesting in opportunistic years.

[RESEARCH LOOP: Re-execute RP1-RP8]

<!-- DEEP: 10+min -->Phase 3 — Multi-Goal Optimization

- Use goal-based buckets: safe (liquidity + near-term), growth (retirement), strategic (private equity), philanthropic.
- Optimize with utility functions: assign higher utility to capital preservation for near-term goals and higher risk budget for long-term goals.

[RESEARCH LOOP: Re-execute RP1-RP8]

<!-- DEEP: 10+min -->Phase 4 — Family Office Primitives (HNW)

- Governance: investment committee, family council, succession plan.
- Reporting cadence: monthly P&L, quarterly performance vs. benchmarks, annual tax aggregation.
- Vaulted documents: centralized legal, tax, and estate docs with controlled access.

[RESEARCH LOOP: Re-execute RP1-RP8]

## Error Decoder

| Symptom | Cause | Fix |
|---|---|---|
| Liquidity crunch after private drawdown | Overcommit to private investments with quarterly NAV uncertainty | Enforce reserve rules; set private commitment cap at 20% of investable assets |
| Concentrated tax bill | Lump-sum disposition of appreciated position | Implement staged sales, charitable contribution, or donor-advised fund to offset gains |

## Best Practices

- Stress-test portfolio for a 25% instantaneous drawdown and 3-year slow recovery; ensure liquidity to avoid fire sales.
- Formalize documented investment policy statement with tax-aware rules and rebalancing bands.
- Negotiate manager fee breaks at scale and monitor net-of-fee performance.

## Production Checklist

- Consolidated balance sheet with liquidity schedule
- IPS signed and risk budget approved
- Concentration remediation plan with tax modeling

## Verification

Complete when multi-goal optimizer shows ≥90% probability of meeting core goal (retirement) and liquidity plan covers next 24 months of commitments.

## Cross-Skill Coordination

Consumes: tax-strategist, retirement-planner, estate-planner. Feeds: family-office.

## What Good Looks Like

- Clear tax-aware asset location, staged plan for concentrated positions, documented governance for multi-gen wealth transfer.

## References

- CFA Institute guidance on portfolio construction, IRS rules for QSBS, public market fee studies

## Scale Depth

- Solo: HNW plan under $5M
- Small: Family office primitives for $5M–$50M
- Medium: Single-family office operations with private markets
- Enterprise: Institutional work — not applicable

## Anti-Hallucination

[VERIFIED] Asset location materially affects after-tax returns.
[COMMON-PRACTICE] Exchange funds used to diversify concentrated equity positions.
[INFERRED] HNW clients require 1–3 years liquidity buffer depending on commitments.
[UNKNOWN] Specific private fund LP terms — review LPA before committing.

<!-- DEEP: 10+min --> HNW Case Studies & Advanced Tactics

- Case study: A client with $8M investable assets held a concentrated tech position representing 45% of investable assets. Over 18 months, the position lost 65% after regulatory shocks. The client's net worth fell to $4.8M, triggering margin calls on some derivative hedges. Recovery required staged liquidation and use of exchange fund to diversify while deferring gains. Lesson: cap concentrated position to 20% and plan staged remediation with reserve capital of 12–24 months of liquidity.

- Advanced strategy: Use tax-aware swapping into single-stock ETFs (where available) or structured collars to preserve pre-tax basis while limiting downside for positions >20% of portfolio — ensure options counterparty risk and costs are modeled.

- Failure narrative: A family office overcommitted 60% to private equity illiquid allocations and faced a 30% NAV markdown during a credit contraction; forced secondary sales at 40% discounts. Lesson: maintain 1–3 years of liquidity for known commitments and cap private commitments to 25–35% of investable assets.

[RESEARCH LOOP: Re-execute RP1-RP8]

## Expanded Decision Tree — Concentration & Alternatives

```
Start -> Liquid Net Worth?
  |-- < $5M -> Standard HNW playbook: asset location + tax efficiency
  |-- >= $5M -> Family office primitives
Concentrated stock >20%?
  |-- Yes -> Evaluate: (1) exchange fund, (2) staged sale over 3–5 years, (3) collar/option strategy
      |-- Exchange fund considered -> check lockup, fees, and liquidity terms; prefer if investor horizon >7 years
Alternatives allocation >10%?
  |-- Yes -> Rigorous due diligence: LPA, GP track record, liquidity schedules, fee cliffs
```

[RESEARCH LOOP: Re-execute RP1-RP8]

## Error Decoder — Expanded (7 rows)

| Symptom | Cause | Fix |
|---|---|---|
| Concentration collapse | Lack of diversification; macro/regulatory shock | Implement staged de-risking: 20% sale/year + hedging; use DAF to offset gains when selling |
| Liquidity mismatch | Overcommit to private funds without reserve | Enforce private allocation cap and maintain 24 months of liquid runway |
| Fee erosion | High active manager fees vs benchmark | Negotiate fee breakpoints and test net-of-fee performance annually |
| Estate tax surprise | Poor integration with estate planner | Run pro-forma estate tax simulation and implement ILIT/GRAT where applicable |
| Governance failure | No replacement or succession plan for family office leadership | Establish investment committee charter and succession plan
| Manager operational risk | Failed operational controls at manager (valuation errors) | Increase operational due diligence and request audited statements
| QSBS misclassification | Company fails active business test | Consult tax counsel before structuring; avoid relying on QSBS without legal confirmation |

[RESEARCH LOOP: Re-execute RP1-RP8]

## Best Practices — HNW (10 items)

1. Cap concentrated position at 20% of investable assets; implement staged remediation plan when above threshold.
2. Maintain 12–24 months of liquidity for operational and commitment needs depending on private market exposure.
3. Use tax-aware asset location: tax-inefficient vehicles (REITs, taxable bonds) in tax-deferred accounts when possible.
4. Negotiate manager fee breaks at $5M+ commitment levels and track net-of-fee performance quarterly.
5. Keep private commitments to ≤30% of investable assets for single-family offices to avoid liquidity crises.
6. Implement an IPS with rebalancing bands (e.g., ±5% for equities) and tax-aware rebalancing triggers.
7. Reserve 30–50% of deployment capital for follow-ons in early-stage portfolios to capture winners.
8. Use exchange funds for large concentrated positions >$2M if liquidity and lockup are acceptable.
9. Build family governance documents and a continuity plan for generational handoffs when AUM >$10M.
10. Conduct annual stress tests (25% drawdown, 3-year slow recovery) and ensure no forced sale scenarios exist for private allocations.

[RESEARCH LOOP: Re-execute RP1-RP8]

## Production Checklist — Expanded (10 items)

| # | Check | Verify |
|---|---:|---|
| ☐ | Consolidated balance sheet with investable assets and liquidity schedule | Aggregation tool (e.g., Addepar) or manual ledger updated within 30 days |
| ☐ | IPS signed with tax-aware asset location rules | Documented rebalancing bands and tax triggers |
| ☐ | Concentration remediation plan if >20% | Timeline and tax modeling attached |
| ☐ | Private commitment cap policy in place | Signed variance approval if exceeded |
| ☐ | Manager due diligence checklists completed | References, audited statements, operational review attached |
| ☐ | Family governance documents created | Investment committee charter and family council notes attached |
| ☐ | Liquidity reserve funding verified (12–24 months) | Bank statements or lines-of-credit validated |
| ☐ | Philanthropy plan aligned with tax strategy (DAF/CRT) | DAF paperwork or trust documents attached |
| ☐ | QSBS and alternative-tax planning verified with counsel | Counsel memo on QSBS eligibility attached |
| ☐ | Annual performance review process scheduled | Performance calendar and review templates in place |

## References & Tools (8)

- Addepar or Tamarac for consolidated reporting
- "The Outsiders" (Byr) for capital allocation case studies (apply with caution)
- CFA Institute readings on asset location and tax-aware investing
- IRS Section 1202 (QSBS) guidance and Treasury regs
- PitchBook/Preqin for private market benchmarking
- Book: "Family Wealth" by James E. Hughes for governance
- Tools: eMoney/Wealthfront for planning, BlackRock Aladdin for institutional risk (enterprise)
- Sample LPAs and NVCA term sheets for negotiation templates

## Cross-Skill Coordination Additions

- To tax-strategist: pass concentrated-position sale timelines and QSBS eligibility checks.
- To estate-planner: align philanthropic planned giving with estate and ILIT strategies.

## Scale Depth — Teams & Thresholds

- Solo: HNW plan under $5M using Vanguard/Schwab tools; single advisor.
- Small: Family office primitives $5M–$50M; team: advisor + CPA + tax counsel; tools: Addepar, eMoney.
- Medium: Single-family office $50M–$500M; team includes CIO, tax counsel, investment ops, legal.
- Enterprise: Multi-family office or institutional operations; heavy-duty platforms (Aladdin), in-house legal and compliance.

## Concrete Framework — Concentration Remediation (Numbers)

- If a position >20%: implement 4-year staged sale plan: Year 1: 30% sale, Year 2: 25%, Year 3: 25%, Year 4: 20%; use DAF to donate a portion at favorable tax times and collars to hedge while retaining some upside.

[RESEARCH LOOP: Re-execute RP1-RP8]

[VERIFIED] Asset location materially affects after-tax returns.
[COMMON-PRACTICE] Exchange funds and collars are used for concentrated positions.
[INFERRED] Maintain 12–24 months liquidity for private commitments.
[UNKNOWN] Specific private fund terms vary by GP and LPA; review each LPA.

