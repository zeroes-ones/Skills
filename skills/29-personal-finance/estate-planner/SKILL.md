---
name: estate-planner
description: >
  Estate planning: wills, revocable living trusts, irrevocable trusts, powers of attorney, beneficiary audits, gifting strategies, and probate avoidance frameworks.
license: MIT
author: Sandeep Kumar Penchala
type: personal-finance
status: stable
version: 1.0.0
updated: 2026-08-02
tags:
  - estate-planning
  - trusts
  - wills
  - probate
  - gifting
  - beneficiary
token_budget: 4500
chain:
  consumes_from:
    - tax-strategist
    - retirement-planner
    - insurance-strategist
  feeds_into:
    - wealth-management-advisor
  alternatives: []
---
# Estate Planner
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Estate planning skill for individuals and families: will frameworks, revocable and irrevocable trusts (ILIT/CRUT/GRAT), powers of attorney, healthcare directives, beneficiary designation audits, lifetime gifting strategies, and probate avoidance. Not for corporate succession.
<!-- QUICK: 30s -->
## <!-- DEEP: 5+min --> RESEARCH_PREREQUISITE — Execute Before Any Output

**HARD GATE: RP1-RP8 required.**

| # | Research Step | Why | Where |
|---|---|---|---|
| RP1 | Verify state law differences | Trust & probate laws vary by state | State statutes, bar association guidance |
| RP2 | Audit client documents | Existing will, beneficiary designations, titling of assets | Estate documents, account records |
| RP3 | Cross-check tax implications | Gift tax, estate tax exemption amounts, portability rules | IRS, state revenue sites |
| RP4 | Identify failure modes | Broken beneficiary designations, missing POA, unintended intestacy | Case studies, court rulings |
| RP5 | Quantify impact | Estate tax exposure, probate fees, timeline delays | Estate tax calculator, probate costs estimates |
| RP6 | Map side effects | Trust may affect Medicaid eligibility, income tax | Medicaid rules, tax-strategist input |
| RP7 | Quality gates | Document execution formalities (witnesses/notary) | State notary/witness requirements |
| RP8 | Declare limitations | Not a substitute for licensed estate attorney for complex trusts | This SKILL.md |

Document research findings inline with [RESEARCHED: RPn — ...].

## Iterative Research Loop

Re-run RP1-RP8 before any change to beneficiaries, transfers, or trust funding.

## Quickstart

1. Collect existing wills, trust documents, beneficiary forms, deeds, life insurance policies, and retirement account statements.
2. Verify primary and contingent beneficiaries on all accounts; ensure they align with estate documents.
3. Create a short checklist: execute POA, healthcare directive, and update beneficiaries.

## Ground Rules

- Beneficiary designations trump wills for payable-on-death accounts and retirement accounts; always check and sync.
- Never assume joint tenancy achieves intended estate planning goals — it can unintentionally disinherit others and create gift tax exposure.
- For significant estates, involve an estate attorney for irrevocable trust and GST/estate tax planning.

## Decision Tree

1. Is estate <$12.92M (2026 hypothetical)? → Simple will + beneficiary audits + POD accounts. If > exemption or state estate tax: consider ILITs, GRATs, and advanced planning.
2. Are there minor children? → Establish guardianship clauses and trusts to manage assets until specified ages.
3. Are there special needs beneficiaries? → Special needs trust to preserve public benefits.

## Core Workflow / Implementation

Phase 0 — Intake & Risk Assessment

- Inventory assets by title, beneficiary, and liquidity. Calculate projected probate exposure and estate tax liability under current law.

[RESEARCH LOOP: Re-execute RP1-RP8 before proceeding to next phase]

<!-- DEEP: 10+min -->Phase 1 — Will & Simple Trusts

- Draft or update a will to name executor, beneficiaries, guardians for minors, and burial instructions.
- Use pour-over revocable trust when privacy and probate avoidance are priorities: fund trust by retitling assets (bank accounts, deeds, brokerage) into the trust's name.

[RESEARCH LOOP: Re-execute RP1-RP8]

<!-- DEEP: 10+min -->Phase 2 — Irrevocable Trusts & Gifting

- ILIT for life insurance to remove policy proceeds from taxable estate: transfer via Crummey powers and annual exclusion gifting ($18,000 per donee in 2024; verify current year in RP1).
- GRAT for transferring appreciation: fund GRAT with appreciating assets expecting low-interest environment where GRAT outperforms 1-month AFR + spread.

[RESEARCH LOOP: Re-execute RP1-RP8]

<!-- DEEP: 10+min -->Phase 3 — Durable POA & Healthcare Directive

- Durable POA: grants agent power over finances; check for springing vs immediate and state-specific statutory language.
- Healthcare directive: specify preferences for life-sustaining treatment and appoint health agent. Ensure HIPAA release language is included to allow information flow.

[RESEARCH LOOP: Re-execute RP1-RP8]

<!-- DEEP: 10+min -->Phase 4 — Beneficiary Audits & Titling

- Verify beneficiary forms on retirement accounts, life insurance, and TOD/POD assets.
- Retitle assets to reflect trust funding plan. Example: change deed to "John Doe Revocable Trust dated [date]" to avoid probate for real estate.

[RESEARCH LOOP: Re-execute RP1-RP8]

## Error Decoder

| Symptom | Cause | Fix |
|---|---|---|
| Assets still in probate despite trust | Trust not funded; deeds not retitled | Execute deed transfers; confirm title company recorded deed |
| Unexpected estate tax bill | Portability not elected or gifts misreported | File portability election or amend returns where possible; consult estate tax counsel |

## Best Practices

- Annual beneficiary review, especially after divorce, birth, death, or move.
- Keep a centralized estate inventory accessible to executor and attorney.
- Use trust funding checklist to ensure assets are properly titled to trust.

## Production Checklist

- Will + POA + Healthcare directive executed per state formalities.
- Retirement beneficiaries aligned with estate documents.
- Deeds retitled for real estate intended to avoid probate.

## Verification

- Test: Simulate transfer — confirm account POD/TOD triggers, trust ownership of deed shows in county recorder.

## Cross-Skill Coordination

Consumes: tax-strategist, retirement-planner, insurance-strategist. Feeds: wealth-management-advisor.

## What Good Looks Like

- A funded revocable trust for probate avoidance, clear beneficiary designations, and a documented plan for estate tax minimization where needed.

## References

- Uniform Probate Code guidance, IRS gift/estate tax publications, local bar association estate planning guides

## Scale Depth

- Solo: Will + POA + beneficiary audit
- Small: Funded revocable trust + guardianship directives
- Medium: ILIT/GRAT setup and gifting program
- Enterprise: Not applicable

## Anti-Hallucination

[VERIFIED] Beneficiary forms override wills for account transfers.
[COMMON-PRACTICE] Fund revocable trust via retitling to avoid probate.
[INFERRED] GRATs perform best with assets expected to outpace the Section 7520 rate.
[UNKNOWN] State-specific homestead protections — verify local law before advising.

<!-- DEEP: 10+min --> Real Examples, Failures & Edge Cases

- Client story: A divorced parent failed to update beneficiary designations after divorce; retirement account paid ex-spouse due to primary beneficiary still listed — estate had to litigate and counsel fees exceeded $45k. Lesson: enforce beneficiary audit at major life events (divorce, marriage, birth).

- Failure mode: Trust not funded. A revocable trust was executed but real estate deed remained in individual name; upon death the estate entered probate causing 9 months delay and $18k in probate-related expenses. Lesson: create a trust-funding checklist and confirm recording of deeds.

- Edge case: Special needs beneficiary inherited cash directly, disqualifying them from Medicaid benefits and costing the family ~$300k/year in lost support. Lesson: use special needs trust with proper trustee and ABLE accounts for supplemental support.

[RESEARCH LOOP: Re-execute RP1-RP8]

## Deepened Decision Tree — Guardians, Trusts, and Gifting

```
Start -> Estate Size?
  |-- <$12.92M
      |-- Minor children?
          |-- Yes -> Appoint guardians + testamentary trust for minors (ages to distribute: 25/30 rule)
          |-- No -> Simple will + beneficiary audit
  |-- > Exemption threshold or state estate tax
      |-- Yes -> Consider ILIT, GRAT, family limited partnership, and portability election
Special Needs?
  |-- Yes -> Create Special Needs Trust (SNT) + ABLE account; coordinate with Medicaid rules
Gifting desires?
  |-- Annual exclusion gifting feasible ($18k per donee example) -> Implement Crummey notices for ILIT and document gifts
  |-- High-net worth philanthropic goals -> Consider CRUT/CRAT/DAF strategies and projected income streams
```

[RESEARCH LOOP: Re-execute RP1-RP8]

## Error Decoder — Expanded (7 rows)

| Symptom | Cause | Fix |
|---|---|---|
| Beneficiary mismatch on IRA | Outdated beneficiary form supersedes will | Immediately update beneficiary designations and confirm via custodian letter |
| Trust not funded | Failure to retitle assets (deeds, accounts) | Execute retitling; verify recording of deed and custodian acknowledgments |
| Gift tax misfiling | Gifts exceeded annual exclusion and no Form 709 filed | File Form 709; consult estate counsel for penalty mitigation if late |
| ILIT Crummey notice failure | Failure to send proper notices invalidates gift treatment | Reconstruct notices, document, and consult counsel about remedial options |
| Guardian ambiguity | Vague language in will causing court to decide | Amend will to name primary and alternate guardians with detailed care plan |
| Special needs disinheritance | Direct inheritance affecting benefits | Establish SNT and transfer assets into trust; coordinate with benefits counselor |
| Real property stuck in probate | Deed titled in decedent's name, no transfer-on-death | Execute corrective retitling and use probate avoidance strategies going forward |

[RESEARCH LOOP: Re-execute RP1-RP8]

## Best Practices — Specific (10 items)

1. Perform beneficiary audit annually and within 30 days of any major life event; require custodian confirmation letter.
2. For minor children, set trust distribution ages not younger than 25 and include staggered distributions to enforce responsible use.
3. Use pour-over wills to capture stray assets with clear funding instructions; follow up with retitling within 90 days of execution.
4. For life insurance used in estate planning, consider ILITs funded via annual exclusion gifts; document Crummey notices and trustee records.
5. Keep a centralized digital vault with encrypted copies of key documents and executor access; rotate keys every 3 years.
6. Coordinate gifting strategy with tax-strategist to use annual exclusion ($18k per person example) and lifetime exemption planning.
7. Use professional trustee for complex family dynamics and special needs situations; quantify trustee fees vs family management cost-benefit.
8. Draft HIPAA-compliant release clauses in healthcare directives to avoid information blocking for agents.
9. Map asset-by-asset titling and beneficiary list to avoid surprises — create a table and verify 1:1 alignment between will/trust and account beneficiaries.
10. Engage local estate counsel for state-specific homestead, elective share laws, and to execute county recorder tasks for deeds.

[RESEARCH LOOP: Re-execute RP1-RP8]

## Production Checklist — Expanded (10 items)

| # | Check | Verify |
|---|---:|---|
| ☐ | Will, POA, Healthcare directive executed per state formalities | Notarized and witnessed per state requirement |
| ☐ | Beneficiary forms updated and signed | Custodian confirmation letters present |
| ☐ | Trust funded: deeds retitled and accounts transferred | Recorded deed or custodian transfer receipts attached |
| ☐ | Guardianship clauses documented for minors | Primary and alternate named with clear instructions |
| ☐ | ILIT/GRAT documents prepared if estate tax planning required | Trustee and funding plan documented |
| ☐ | Special needs trust created if needed | Trustee chosen with care coordination plan |
| ☐ | HIPAA and FERPA release language included where needed | Language present in healthcare directive |
| ☐ | Probate avoidance checklist completed | POD/TOD, beneficiary alignment, and title review complete |
| ☐ | Client has emergency contact and executor contact info stored | Contact list saved in secure vault |
| ☐ | Annual review schedule set (calendar) | Next review date within 12 months |

## References & Tools (7)

- Uniform Probate Code and state-specific probate statutes
- IRS gift and estate tax publications (Form 709 instructions)
- ABA estate planning resources and local bar association templates
- Nolo guides: "Estate Planning Basics" and "Special Needs Trusts"
- Tools: LegalZoom for simple documents (use with caution), Trust & Will, county recorder online portals
- Book: "Plan Your Estate" — Denis Clifford (Nolo)
- State bar estate planning clinics for localized guidance

## Cross-Skill Coordination Additions

- To tax-strategist: share projected estate tax exposure and gifting schedule to align lifetime exemption utilization.
- To wealth-management-advisor: coordinate investment funding of trusts and liquidity planning for estate tax liabilities.

## Scale Depth — Roles, Tools & Thresholds

- Solo: Will + POA + beneficiary audit using templates + local notary; estate <$1M.
- Small: Funded revocable trust and retitling with CPA; estate $1M–$5M; use local estate attorney for retitling.
- Medium: ILIT/GRAT setup and active gifting program with trustee and tax counsel; estate $5M–$50M; team: estate attorney + CPA + trustee.
- Enterprise: Multi-jurisdictional planning and family office coordination — team required (lawyers, tax counsel, trust company).

## Concrete Framework — Gift/ILIT Scheduling (Numbers)

- Annual exclusion gifting: $18k per donee (2024 example). For a married couple with 3 children: annual exclusion contribution = $18k × 2 × 3 = $108k/year tax-free gift into trusts.
- GRAT example: Fund GRAT with $1M expected to appreciate at 6% while Section 7520 rate = 2.5%; expected remainder to beneficiaries may transfer tax-efficiently if returns exceed rate.

[RESEARCH LOOP: Re-execute RP1-RP8]

[VERIFIED] Beneficiary forms override wills for transfers.
[COMMON-PRACTICE] Fund revocable trust by retitling assets.
[INFERRED] GRATs work best when funding rapidly appreciating assets and low Section 7520 rates.
[UNKNOWN] State-specific homestead protections vary widely — consult local counsel.

