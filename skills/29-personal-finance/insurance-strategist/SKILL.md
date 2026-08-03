---
name: insurance-strategist
description: >
  Insurance strategy: life insurance needs analysis, disability coverage, umbrella sizing, long-term care evaluation, and health plan optimization (HDHP+HSA vs PPO).
license: MIT
author: Sandeep Kumar Penchala
type: personal-finance
status: stable
version: 1.0.0
updated: 2026-08-02
tags:
  - insurance
  - life-insurance
  - disability
  - ltc
  - umbrella
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
# Insurance Strategist
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Evidence-driven insurance strategy: term life needs (DIME), disability insurance design (own-occupation vs any-occupation), umbrella sizing, LTC evaluation, health plan optimization (HDHP+HSA modeling), and insurer financial strength evaluation (AM Best, S&P).
<!-- QUICK: 30s -->
## <!-- DEEP: 5+min --> RESEARCH_PREREQUISITE — Execute Before Any Output

**HARD GATE: run RP1-RP8.**

| # | Research Step | Why | Where |
|---|---|---|---|
| RP1 | Verify product specs | Policy definitions (own-occupation vs any-occupation) vary | Policy contracts, insurer manuals |
| RP2 | Audit client exposure | Income, dependents, liabilities, assets | Client profile, mortgage docs |
| RP3 | Cross-reference cost data | Rates vary by age/health/class | Carrier rate sheets, broker quotes |
| RP4 | Identify failure modes | Claim denials, contestability, lapse | Policy clauses, AG office records |
| RP5 | Quantify impact | Replacement ratio, indemnity vs premium | Spreadsheet modeling |
| RP6 | Map side effects | LTC benefits impact Medicaid eligibility | State Medicaid rules |
| RP7 | Quality gates | Replace with evidence of insurer ratings & non-guaranteed elements | AM Best, S&P reports |
| RP8 | Limitations | Not for commercial insurance program design | This SKILL.md |

Document research with [RESEARCHED: RPn — ...].

## Iterative Research Loop

Re-run RP1-RP8 before recommending a policy or changing coverage.

## Quickstart

1. DIME needs analysis for term life: Debt, Income replacement (12–15x if young with dependents), Mortgage, Education costs.
2. Collect current policies, beneficiary designations, and insurer ratings.
3. For disability: target own-occupation until at least 2–3 years into career; replace 60% of earned income as a baseline.

## Ground Rules

- Prefer term life for pure death benefit needs; avoid whole life as primary investment vehicle.
- Disability own-occupation preferred for specialized professions; otherwise use any-occupation as fallback with own-occ for early-career protection.
- Umbrella: minimum coverage = net worth rounded up to nearest $1M; for HNW, consider $5M+ layers via excess policies.

## Decision Tree

1. Are dependents present? If yes, term life sized at 12–15x income + mortgage + college costs. If estate liquidity concern exists, consider ILIT or permanent policy for estate tax planning.
2. Is client at high-risk occupation? If yes, prioritize own-occupation disability.
3. Does client face LTC risk? If self-insure capacity < expected LTC PV, model LTC policy with inflation protection.

## Core Workflow / Implementation

Phase 0 — Intake & Exposure Modeling

- Gather income history, employer benefits, current coverage, and health status.
- Compute replacement needs and run DIME model with present value of future obligations adjusted for inflation.

[RESEARCH LOOP: Re-execute RP1-RP8 before proceeding to next phase]

<!-- DEEP: 10+min -->Phase 1 — Life Insurance Design (DIME)

- Debt: outstanding mortgage and other debts.
- Income: multiply net annual income by replacement factor (12–15x for young families).
- Mortgage: include remaining principal and expected home expenses until child reaches self-sufficiency.
- Education: estimate tuition PV at current costs inflated to future years.

Example: $120k net income × 12 = $1.44M replacement + $300k mortgage + $200k education = $1.94M → round to $2M term policy.

[RESEARCH LOOP: Re-execute RP1-RP8]

<!-- DEEP: 10+min -->Phase 2 — Disability Insurance

- Evaluate employer coverage: short-term disability (STD) and long-term disability (LTD) replacement rates.
- Personal policy: aim for 60% of income (net of other sources), cost typically 1–3% of income depending on occupation/health.
- Own-occupation vs any-occupation: own-occupation preserves future earnings for specialists and is more expensive but recommended for high human-capital careers (surgeons, partners, rainmakers).

[RESEARCH LOOP: Re-execute RP1-RP8]

<!-- DEEP: 10+min -->Phase 3 — Long-Term Care & Hybrid Models

- LTC decision: compute expected PV of LTC needs and compare to premium stream. Example: median nursing home private-pay ~$120k/year; 3-year PV at 3% real ≈ $330k.
- Hybrid life/LTC policies shift mortality/longevity risk but can be expensive; consider if client desires legacy floors and wishes to avoid stand-alone LTC premiums.

[RESEARCH LOOP: Re-execute RP1-RP8]

<!-- DEEP: 10+min -->Phase 4 — Health Insurance Optimization

- HDHP + HSA vs PPO: model annual expected medical spend. If expected OOP < deductible + HSA contribution and client can fund HSA, HDHP+HSA wins due to triple tax advantage.
- Example: single under 45 with expected OOP $1,500/year: HDHP + $3,850 HSA (2024 limits variable) invested with long-term horizon is efficient.

[RESEARCH LOOP: Re-execute RP1-RP8]

## Error Decoder

| Symptom | Cause | Fix |
|---|---|---|
| Claim denial on disability | Material misrepresentation or pre-existing condition | Appeal with medical records, broker escalation; maintain thorough documentation |
| Policy lapse due to non-payment | Premium increases or missed premium | Reinstate per policy grace period or find replacement coverage if not eligible |

## Best Practices

- Annual policy inventory: track policy issue dates, riders, and contestability periods.
- Use term life + investment strategy for most clients; reserve whole life only for specific estate tax or irrevocable needs with counsel.
- Shop underwriting classes and consider medical exam timing aligned with life events (e.g., before aviational employment).

## Production Checklist

- DIME calculation completed and policy recommended
- Disability gap documented and own-occupation recommendation made where appropriate
- Umbrella coverage sized to net worth and documented with insurer A- ratings

## Verification

- Verify quotes and bind policies; confirm riders, exclusions, and contestability windows.

## Cross-Skill Coordination

Consumes: personal-finance, tax-strategist. Feeds: estate-planner, wealth-management-advisor.

## What Good Looks Like

- Documented insurance plan that covers immediate liquidity needs, income replacement, catastrophic LTC risk, and excess liability with rated carriers.

## References

- AM Best, NAIC consumer guides, CMS for Medicare basics

## Scale Depth

- Solo: term life + disability recommendation
- Small: family-level insurance program and umbrella layering
- Medium: integrated LTC and hybrid product evaluation with estate trust coordination

## Anti-Hallucination

[VERIFIED] Own-occupation disability policies are superior for specialists.
[COMMON-PRACTICE] Term life is the most cost-effective death benefit for most families.
[INFERRED] LTC expected costs often exceed $100k/year in many markets.
[UNKNOWN] Exact HSA contribution limits for current year — verify via IRS.

<!-- DEEP: 10+min --> Claim Denials, Rider Pitfalls & Real Examples

- Claim denial story: A surgeon's own-occupation disability policy was denied because the insurer defined "own occupation" narrower than claimed (focused on surgical subspecialty). After appeal and legal fees ($22k+), settled for 40% of expected benefits. Lesson: define 'own-occupation' precisely in policy language and get insurer confirmation in writing.

- Rider surprise: A life insurance policy with accelerated death benefit for chronic illness excluded certain cognitive decline definitions; family faced $80k unexpected LTC costs despite believing they had coverage. Lesson: read rider fine print and run scenarios against insurer definitions.

- LTC underwriting edge: Buying LTC later in life (>75) can be 3–5× more expensive; early purchase at 60–65 often reduces lifetime premium. Model expected PV of premiums vs self-insure threshold.

[RESEARCH LOOP: Re-execute RP1-RP8]

## Expanded Decision Tree — Life, Disability, LTC, Umbrella

```
Coverage Need -> Dependents present?
  |-- Yes -> DIME calculation for life insurance (target 12–15x income + mortgage + education)
  |-- No -> Minimal term or self-insure for small obligations
Disability -> High human-capital role?
  |-- Yes -> Own-occupation LTD up to 60% income replacement, eliminate offsets where possible
  |-- No -> Any-occupation acceptable with careful definition
LTC -> Self-insure capacity vs expected PV of LTC
  |-- If PV > self-insure capacity -> purchase LTC or hybrid life/LTC
Umbrella -> Net worth rounded to nearest $1M; consider $5M layers for HNW
```

[RESEARCH LOOP: Re-execute RP1-RP8]

## Error Decoder — Expanded (6 rows)

| Symptom | Cause | Fix |
|---|---|---|
| Disability claim denied | Material misrepresentation or narrow 'own-occupation' clause | Appeal with medical documentation; engage broker/legal counsel; seek retroactive benefits if evidence supports claim |
| Underinsurance after life event | Policy not updated after mortgage/job change | Recalculate DIME annually and update coverage within 30 days of major change |
| LTC premium surprise | Bought LTC late or selected inflation protection too expensive | Consider hybrid products earlier or self-insure with escalating reserve plan |
| Umbrella coverage gap | Underestimated liability exposures (e.g., rental property) | Increase umbrella to at least net worth or purchase excess layers; include rental endorsements |
| Health plan mis-scenario | Choosing PPO over HDHP when annual OOP < deductible | Run 3-year expected OOP comparison and include HSA investment opportunity cost |
| Policy lapse | Underpriced premium increases or missed payments | Use annual premium review and lock-in guaranteed level-premium products when appropriate |

[RESEARCH LOOP: Re-execute RP1-RP8]

## Best Practices — Specific (10 items)

1. Re-run DIME every 12 months or after income changes >10%; round policy size to nearest $100k for term quotes.
2. For disability, aim for 60% replacement net of other benefits; cap benefit duration at least to age 65 if career-dependent.
3. For LTC, consider purchase when client age 55–65 if expected PV of LTC > 4% of investable assets.
4. Keep umbrella coverage ≥ net worth rounded up to next $1M; for HNW use $5M+ layers with A-rated carriers.
5. Prefer term life for active income replacement; only use permanent life for explicit estate tax strategies documented with estate counsel.
6. Shop underwriting classes; encourage medical exam and favorable class timing before major life changes (ex: before surgery or new job hazard exposure).
7. For HDHP+HSA, only recommend if client can fund HSA fully and expected OOP < deductible + HSA contribution; otherwise model PPO total cost.
8. Review insurer financial strength annually; replace policies only after underwriting windows and cost-benefit analysis.
9. For group employer benefits, confirm portability and portability cost before relying on group LTD for long-term retirement planning.
10. Document all policy riders and have a 3-tier escalation plan for claim denials (broker -> insurer internal appeals -> external counsel).

[RESEARCH LOOP: Re-execute RP1-RP8]

## Production Checklist — Expanded (10 items)

| # | Check | Verify |
|---|---:|---|
| ☐ | DIME calculation present with supporting numbers | DIME spreadsheet attached |
| ☐ | Disability gap quantified with employer benefits factored | LTD/STD documents on file |
| ☐ | Quote comparisons from ≥3 carriers for major policies | Rate sheets and class assumptions attached |
| ☐ | Umbrella coverage sized and insurer A-rated | AM Best rating attached |
| ☐ | LTC analysis completed with PV calculation | Premiums vs self-insure PV table attached |
| ☐ | HDHP vs PPO cost model run for 3 years | OOP and HSA investment benefit calculated |
| ☐ | Policy riders reviewed and documented | Rider text and exclusions summarized |
| ☐ | Renewal calendar created with premium review triggers | Calendar invite set for 60 days before renewal |
| ☐ | Beneficiaries on insurance policies verified | Beneficiary forms on file match estate plan |
| ☐ | Claim escalation plan documented | Broker contact, insurer appeals steps, counsel contact included |

## References & Tools (6)

- AM Best insurer ratings and reports
- NAIC market conduct resources and consumer complaint indices
- CMS Medicare & Medicaid guidance for LTC implications
- NAIC Long-Term Care Insurance Model Regulation
- Book: "The New Health Insurance Solution" (Gruber) for health-plan evaluation
- Tools: Policygenius, LIMRA insurance market data, HSA contribution calculators

## Cross-Skill Coordination Additions

- To estate-planner: ensure ILIT structure when life insurance proceeds intended to bypass estate taxation.
- To tax-strategist: synchronize HSA + LTC + accelerated death benefits with tax planning calendars.

## Scale Depth — Tools & Triggers

- Solo: Basic term life + disability recommendation with online quoting tools (Policygenius), personal CPA for tax sync; net worth <$1M.
- Small: Family-level program with broker + CPA + estate counsel; net worth $1M–$10M; use broker portals for multi-carrier quotes.
- Medium: Integrated LTC + hybrid policies with trust coordination and trustee governance; net worth $10M–$100M; team includes insurance broker, trust counsel, and financial planner.

## Concrete Framework — DIME with Numbers

- Example DIME for a 35-year-old earning $150k gross: Debt = $300k mortgage; Income replacement = 12× net income ($120k net × 12 = $1.44M); Mortgage = $300k; Education reserve = $200k → Total insurance need ≈ $1.94M → Recommend $2M term (20-30 year).

[RESEARCH LOOP: Re-execute RP1-RP8]

[VERIFIED] Own-occupation policies protect specialists more than any-occupation.
[COMMON-PRACTICE] Term life is cost-effective for income replacement.
[INFERRED] Buy LTC earlier to economize premiums; costs escalate with age.
[UNKNOWN] Current year's HSA limits — verify via IRS publications.

