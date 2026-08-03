---
name: property-manager
description: "Use when operating small to mid-size residential properties: tenant screening, lease design, maintenance systems, vendor management, rent optimization, and legal compliance. Handles checklists, SOPs, and reporting templates. Do NOT use for commercial property management or hotel operations."
license: MIT
author: Sandeep Kumar Penchala
type: real-estate
status: stable
version: 1.0.0
updated: 2026-08-02
tags: [property-management, tenant-screening, leases, maintenance, vendor-management, rent-pricing, compliance]
token_budget: 4000
chain:
  consumes_from: [real-estate-investor]
  feeds_into: []
  alternatives: [third-party-pm, real-estate-operator]
---

# Property Manager
Portability target: run as operational SOP and integrate with PM software

<!-- QUICK: 30s -->
Operationalize residential property management: screening, leases, maintenance, vendor workflows, pricing, compliance, and reporting with actionable checklists and templates.

## RESEARCH_PREREQUISITE (hard gate)
| RP# | Requirement |
|-----|-------------|
| RP1 | Owner authorization and property documentation (title, insurance, contact). |
| RP2 | Tenant data privacy consent for screening processes. |
| RP3 | Local legal/regulatory context for eviction and habitability. |
| RP4 | Existing lease templates and historic rent rolls. |
| RP5 | Vendor contact list and insurance/license verification. |
| RP6 | Emergency contact and access to property (keys/lockbox). |
| RP7 | Financial reporting cadence and accounting access. |
| RP8 | Exclusions: commercial regulations, hotel licensure, HOA master policies unless in scope. |

## Iterative Research Loop
| Loop | Goal | Inputs | Output |
|------|------|--------|--------|
| Loop 0 | Intake property & owner goals | Property details, owner objectives | Asset brief & KPI targets |
| Loop 1 | Tenant operations | Applications, screening results | Approved tenant profile & move-in checklist |
| Loop 2 | Maintenance & vendors | Work order history | Preventive maintenance schedule & vendor SLAs |
| Loop 3 | Financial ops | Rent roll, expenses | P&L template and cash flow dashboard |

## Quickstart (30s)
1. Confirm owner authorization and property address.  
2. Run a 3-point safety check: active hazards, locks, smoke detectors.  
3. Output: Move-in readiness checklist and tenant screening template link.

<!-- STANDARD: 3min -->
## Ground Rules
- Mechanical triggers:
  - If habitability failure or health hazard identified: prioritize immediate remediation and notify owner.
  - If a tenant reports domestic violence: follow local victim-support protocols and confidentiality rules.
- Negative constraints:
  - Do NOT offer legal advice; refer to local counsel for eviction timelines and notices.
  - Do NOT manage commercial leases or hospitality operations.

## Decision Tree (detailed)
Start
|-- Safety/habitability issue? -- Yes -> Emergency repair + owner notify
|                     |-- Is it life/health-threatening? -> Call emergency services, document, and notify owner immediately
|                     |-- Non-emergency but habitability failure -> Temporary remediation + schedule permanent fix within 72 hours
|
|-- No -> Vacancy or Occupied State
    |-- Occupied -> Maintenance request? -> Emergency? -> Yes -> On-call vendor + owner spend threshold check
                              -> No -> Schedule routine work order, provide ETA to tenant
    |
    |-- Vacancy -> Market comp check
         |-- High demand (avg vacancy < 20 days) -> List at market median, 5% upgrade for premium features
         |-- Low demand (avg vacancy > 30 days) -> Price aggressively (median -5%) and invest in cost-effective staging
         |-- Applicant pool -> Screen -> If <3 applicants -> widen ad channels and offer small concession (1 week free / free cleaning)

Notes:
- At each decision node, log owner approvals when spend exceeds pre-agreed thresholds.
- Always run Fair Housing screening rules and maintain consistent criteria across applicants.

## Core Workflow
STANDARD: Tenant Screening
1. Application intake form (ID, income, landlord refs)
2. Credit & background check (consistent criteria, comply with fair housing)
3. Income verification: 2.5x rent guideline or guarantor path
4. Landlord reference: confirm payment, notice, damages

STANDARD: Lease Drafting & Move-in
- Lease essentials: parties, term, rent, security deposit, maintenance responsibilities, pet policy, rent escalation, entry rights, lead paint & disclosures
- Move-in checklist: photos, meter readings, keys, emergency contacts

<!-- DEEP: 10+min -->
DEEP: Maintenance & Vendor Management — war stories and edge cases
- War story: deferred HVAC maintenance in a 12-unit building led to a complete system failure in January; emergency replacement cost $45,000 and 30 days of tenant relocations versus a $1,200 annual preventive contract. Lesson: preventive maintenance is cost-effective; keep capital reserve for HVAC replacement.
- Edge case: single-vendor monopolies in small markets — one vendor failure caused service disruption for 2 weeks. Mitigation: keep at least two vetted vendors per trade (plumbing, HVAC, electrical).
- Contract design: include SLAs (response within 4 hours for emergency, 48 hours for non-emergency), penalties for missed response times, and trial period with performance review after 90 days.
- Escalation protocol: define emergency spend thresholds (e.g., manager can sign up to $500; owner approval required for $500–$5,000; >$5,000 requires owner sign-off) and automate notifications.

<!-- DEEP: 10+min -->
DEEP: Pricing & Turnover — numeric failure narratives
- Failure story: listed a renovated 2-bed unit at +15% above market expecting premium tenants; it remained vacant for 72 days. Cost of vacancy (lost rent $3,600 + $500 marketing) exceeded potential premium. Fix: re-price at market median - set rapid re-listing incentives after 21 days.
- Turnover cost framework: average turnover cost per unit (cleaning, painting, repairs, marketing) = $1,200–$3,500 depending on market. Use conservative $2,000 baseline when budgeting and compare against renewal incentive costs (e.g., 1 month free = rent * 1 month). Calculate ROI on retention incentives.
- Pricing rule: use three comps, adjust for days-on-market (DOM). If DOM > 30, reduce price by 3–5% and add a small concession. Track elasticity by comparing price change vs application rate over 14 days.

<!-- DEEP: 10+min -->
DEEP: Legal & Compliance — risk narratives
- Case study: failure to refund security deposit within statutory timeframe resulted in tenant suing and a $7,500 judgment plus attorney fees. Fix: implement deposit accounting and automated reminders aligned to local law. Keep a checklist per state jurisdiction for deposit timelines and allowable deductions.
- Fair Housing risk: a manager posted a listing that discriminated by family status inadvertently. Action: take down ad, retrain staff, and document remediation. Maintain advertising templates vetted against HUD guidance (42 U.S.C. 3601-3619).
- Edge case: HOA rules conflict with lease terms. Mitigation: consult HOA covenants during lease drafting and include owner/HOA clauses.

<!-- DEEP: 10+min -->
DEEP: Maintenance Vendor Financial Controls
- Financial failure: vendor invoice duplication and weak PO controls led to $12,000 in overpayments over a year. Implement 3-way matching (PO, work order, invoice), monthly vendor reconciliations, and limit changes to PO > $1,000 through owner approval.
- War story: a 'cheap' vendor saved on invoices but created higher long-term rework costs. Implement quality audits and require at least two references and photo evidence of work completed before payment.

## Error Decoder
| Error Message / Pitfall | Root Cause | Fix | Lesson |
|-------------------------|------------|-----|--------|
| "Tenant left without notice, deposit dispute" | Move-in/out condition report missing or insufficient | Use robust photo timestamped report and signed checklist; require tenant sign-off | Document, quantify, and communicate to reduce disputes |
| "Vendor underperformed" | No SLA or trial period; loose vendor vetting | Terminate vendor, run performance review, re-bid the trade, and enroll new SLAs | Test vendors before scaling assignments; quality beats lowest price |
| "Unclear rent pricing" | Lack of recent comps or seasonality data | Run comp analysis and update pricing cadence quarterly; track DOM and application rates | Market data reduces vacancy-days and churn |
| "Security deposit litigation" | Missing accounting or incorrect deductions | Implement deposit ledger, timestamped move-in/out photos, and clear deduction policy | Follow local statutes precisely; automated reminders help compliance |
| "Repeated emergency spend" | No preventive maintenance or poor vendor SLAs | Institute preventive schedule and vendor SLAs; track emergency spend monthly against capex reserves | Preventive maintenance reduces emergency costs dramatically |
| "High turnover costs" | Poor tenant-screening or no renewal incentives | Improve screening quality, offer targeted renewal incentives, and track retention metrics | Retaining tenants is often cheaper than re-leasing |
| "Regulatory ad takedown" | Listing language inadvertently discriminatory | Use vetted ad templates, train staff on HUD guidelines, and audit listings weekly | Proactive compliance avoids fines and reputational harm |

## Best Practices
1. Standardize screening criteria and document every decision for fair housing defense; keep audit logs for 3 years.
2. Maintain digital photo move-in/out records with timestamps and tenant sign-off; store in secure cloud.
3. Keep at least two vetted vendors per trade with SLAs and trial periods for new vendors.
4. Automate rent collection, apply consistent late-fee policy, and reconcile monthly to a P&L per unit.
5. Offer renewal incentives when retention ROI beats turnover cost (calculate per-unit baseline).
6. Set tenant service SLAs: emergency response 4 hours, routine response 48 hours, with owner escalation rules.
7. Budget preventive maintenance at 1–2% of property value annually and create a 10-year CapEx reserve schedule.
8. Track turnover cost per unit (baseline $2,000) and use that to price renewal incentives and marketing spend.
9. Use standardized listing templates vetted for Fair Housing compliance and run weekly audits.
10. Implement 3-way invoice matching (PO, work order, invoice) to reduce overpayments and fraud.

## Production Checklist
- [ ] Owner authorization and property details on file
- [ ] Local jurisdiction landlord-tenant rules loaded for reference
- [ ] Current lease template reviewed for local disclosures and HOA clauses
- [ ] Tenant screening SOP implemented with documented criteria
- [ ] Move-in/out photo report template in use and signed by tenant
- [ ] Vendor roster verified for insurance/licenses and SLAs
- [ ] Preventive maintenance schedule created and assigned
- [ ] Emergency on-call vendor roster and authorization thresholds documented
- [ ] Monthly P&L template configured and owner reporting cadence set
- [ ] Turnover cost model (baseline per-unit) built and validated
- [ ] Security deposit ledger established for each unit
- [ ] Ad templates created and vetted for Fair Housing compliance
- [ ] 30-day tenant satisfaction survey template ready
- [ ] Quarterly vendor performance review calendar set

## Verification
- Tenant screening: all new tenants have completed credit/background checks and signed leases.
- Move-in: photo report stored and deposit allocation documented.
- Financial: monthly P&L reconciled and owner receives a summary.
- Maintenance: preventive tasks logged for the quarter.

## Cross-Skill Coordination
| Skill | When to call | Inputs | Outputs |
|-------|--------------|--------|---------|
| real-estate-investor | For capital improvements and ROI analysis | CapEx requests, reserve levels | Approve/decline improvements and funding plan |
| accountant | End-of-month reconciliation | Rent roll, expenses | Tax-ready P&L and schedule for deductions |
| tenant-lawyer | Complex eviction or legal dispute | Notice history, communications | Legal notice drafting and court representation |

## What Good Looks Like
- Vacancy days < 30 for typical markets.
- Tenant satisfaction score above local average (surveyed after 30 days).
- Turnover spend within planned CapEx per unit/year.
- Timely owner reporting with reconciling statements.

## References
- U.S. Department of Housing and Urban Development (HUD). Fair Housing Act (42 U.S.C. 3601–3619) and guidance documents.
- Local landlord-tenant statutes (state-level) — always consult the jurisdiction's official code.
- Buildium (property management software), AppFolio, and RentRedi — vendor selection guides and industry comparisons.
- National Apartment Association (NAA) operations guides and benchmarking reports.
- Nolo Press: state-specific landlord-tenant legal guides for compliance templates.
- Institute of Real Estate Management (IREM) best-practice guides on maintenance and capital planning.

## Scale Depth
Solo (1–5 units):
- Tools: Google Sheets, QuickBooks for small landlords, simple PM apps (SimplifyEm).
- Team: single operator; owner-managed.
- Trigger to scale: >5 properties or need for hands-free rent collection and maintenance coordination.

Small (6–50 units):
- Tools: Buildium, RentRedi, AppFolio (entry-level), digital lease signing, automated payments.
- Team: 1 property manager + part-time maintenance coordinator; 1 bookkeeper.
- Output: automated rent collection, monthly owner statements, basic preventive maintenance program.
- Trigger: sustained vacancy rate > market average or >50 units.

Medium (50–250 units):
- Tools: AppFolio/Buildium enterprise modules, vendor portal, work order tracking (Maintenance Connection), tenant portal.
- Team: Operations manager, maintenance team (2–6), leasing agent(s), accountant.
- Output: SLA-managed maintenance, vendor contracts, monthly KPIs (vacancy, NOI, turnover cost).
- Trigger: need for in-house maintenance or consistent multi-market operations.

Enterprise (250+ units/portfolio):
- Tools: Enterprise property management platform, integrated accounting (Yardi), procurement workflows, BI dashboards.
- Team: Director of Operations, procurement, regional managers, in-house maintenance, compliance/legal.
- Output: portfolio-level analytics, centralized procurement, capital planning, formal vendor procurement.
- Trigger: multi-market scaling, institutional investor requirements, regulatory complexity.

## Concrete Frameworks
Pricing & Vacancy Sensitivity Framework
- Baseline: compute market median rent from 3 comps. Rule: if DOM <= 20, price at median; if DOM 21–30, price median -2%; if DOM >30, price median -5% + concession.
- Turnover Cost Benchmark: conservative baseline $2,000 per turnover (cleaning, painting, minor repairs, marketing). Use local data to calibrate.
- Renewal ROI rule: if retention incentive cost < 50% of turnover cost, offer incentive (e.g., $500 credit vs $2,000 turnover baseline).

Maintenance Financial Rule-of-Thumbs
- Preventive maintenance budget: 1–2% of property value annually (or $300–$500/unit/year for small portfolios).
- CapEx reserve: forecast major items (roof, HVAC) on 10-year replacement schedule and fund monthly to meet projected costs.

## Anti-Hallucination
- [VERIFIED] Fair Housing and security deposit rules exist and are jurisdiction-specific.
- [COMMON-PRACTICE] 2.5x income screening and photo move-in reports are widely used industry practices.
- [INFERRED] Turnover cost baselines vary widely; $2,000 is a conservative aggregate estimate.
- [UNKNOWN] Exact local statutory timelines for eviction and deposit return — always consult local counsel.
