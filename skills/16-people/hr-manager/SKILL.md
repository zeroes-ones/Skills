---
name: hr-manager
description: Human resources management for startups — employee lifecycle management (hire-to-retire), leave of absence administration, benefits administration & broker management, workers' compensation, employee handbook development, compliance posters, I-9/E-Verify, unemployment claims, HR audits, and state-specific labor law compliance. Use when handling employee relations, benefits administration, leave management, HR compliance, or HR audits.
author: Sandeep Kumar Penchala
type: people
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - hr-manager
  - employee-lifecycle
  - benefits
  - leave-management
  - compliance
token_budget: 3200
output:
  type: "document"
  path_hint: "./"
---
# HR Manager

Human resources management covering employee lifecycle, benefits administration, leave management, compliance, and employee relations. This skill handles the operational side of HR — the systems, processes, and compliance requirements that keep a company running and out of trouble.

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->

- Managing employee lifecycles: onboarding (I-9, payroll setup, benefits enrollment), status changes (promotion, transfer, termination), and offboarding (COBRA, final paycheck)
- Administering benefits: health insurance, 401(k), commuter benefits, FSA/HSA — including open enrollment and broker management
- Handling leaves of absence: FMLA, state family leave (CA CFRA, NY PFL, WA PFML), short-term/long-term disability, parental leave, PTO — ensuring compliance with federal, state, and local laws
- Maintaining HR compliance: labor law posters, I-9/E-Verify, workers' compensation claims, unemployment claims, Form 5500 filing, ACA reporting
- Conducting HR audits: employee file completeness, policy review, wage and hour compliance, exemption classification
- Developing and maintaining the employee handbook that actually gets read — policies on harassment, leave, remote work, code of conduct, expense reimbursement

**Use `/people-ops` instead when:** You're designing strategic people programs — compensation philosophy, performance review cycles, leveling frameworks, career ladders, or engagement surveys. People-ops is strategic (how we grow and retain people); HR-manager is operational (the systems and compliance that keep the lights on).

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->

### Leave Type Determination

```
                      ┌──────────────────────────┐
                      │ START: Employee requests  │
                      │ time off for medical or   │
                      │ family reason             │
                      └───────────┬──────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Is the reason their own    │
                    │ serious health condition?  │
                    └────┬─────────────────┬────┘
                         │ YES             │ NO
                    ┌────▼──────────┐ ┌─────▼─────────────────────┐
                    │ Own illness?  │ │ Family member illness?     │
                    └────┬──────────┘ └─────┬─────────────────────┘
                         │                  │
                    ┌────▼──────────┐ ┌─────▼─────────────────────┐
                    │ FMLA (if     │ │ FMLA for family care      │
                    │ eligible) +  │ │ + state family leave if   │
                    │ STD if       │ │ applicable (CA PFL, NY    │
                    │ available.   │ │ PFL, WA PFML)             │
                    │ After STD    │ │ May run concurrently with │
                    │ runs out,    │ │ or separate from FMLA     │
                    │ LTD if       │ │ depending on state        │
                    │ enrolled.    │ │                            │
                    └──────────────┘ └────────────────────────────┘
                         │ NO (neither)
                    ┌────▼──────────────────────────────────────┐
                    │ Bonding / New child? → FMLA for bonding   │
                    │ (12 weeks, unpaid) + state paid leave if  │
                    │ applicable. Parental leave policy may     │
                    │ supplement.                                │
                    │ Military caregiver? → FMLA for military   │
                    │ caregiver leave (26 weeks) + USERRA       │
                    │ protections.                               │
                    │ Personal / Not covered by FMLA? → PTO,    │
                    │ unpaid leave per company policy, or state │
                    │ specific protected leave (e.g., sick/safe │
                    │ leave laws in CO, IL, OR, etc.)           │
                    └────────────────────────────────────────────┘
```

**FMLA eligibility:** 50+ employees within 75 miles AND employee has 12 months / 1,250 hours. If not eligible, check state-specific family/medical leave laws — several states have their own paid leave programs with no employer-size exemption.

### Exemption Classification

```
                     ┌──────────────────────────┐
                     │ START: Is the role       │
                     │ eligible for overtime?   │
                     └───────────┬──────────────┘
                                 │
                   ┌─────────────▼─────────────┐
                   │ Salary ≥ $684/week ($35,568/│
                   │ yr)? Plus duties test?     │
                   └────┬─────────────────┬────┘
                        │ YES             │ NO
                   ┌────▼──────────┐ ┌─────▼────────────────┐
                   │ Does the role  │ │ Non-exempt →         │
                   │ pass the       │ │ Eligible for         │
                   │ duties test?   │ │ overtime at 1.5x     │
                   │ (executive,    │ │ regular rate. Must   │
                   │ administrative,│ │ track all hours      │
                   │ professional,  │ │ worked — including    │
                   │ computer, or   │ │ after-hours emails,  │
                   │ outside sales) │ │ Slack, phone calls.  │
                   └────┬──────────┘ └──────────────────────┘
                        │ YES              │ NO
                   ┌────▼──────────┐       │
                   │ Exempt from   │       │
                   │ overtime. No  │       │
                   │ hourly track- │       │
                   │ ing needed.   │       │
                   └───────────────┘       │
                   ┌───────────────────────┘
                   │ NO
              ┌────▼──────────────────────────────┐
              │ Misclassification risk!            │
              │ If NOT exempt but treated as       │
              │ exempt: liability for back wages   │
              │ + liquidated damages + attorneys'  │
              │ fees. State tests may be stricter  │
              │ than federal (CA, NY, WA).         │
              └─────────────────────────────────────┘
```

**Key traps:** Computer professionals exemption requires specific job duties (software design/development, not IT support or QA). Outside sales requires the employee's primary duty to be making sales — not just being in the field. In California, the salary threshold is $66,560/yr — higher than federal.

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->

### Phase 1 (~15 min): New Hire Onboarding
**Steps:** 1) Collect completed I-9 with acceptable documents (List A or B+C) within 3 business days 2) Verify I-9 through E-Verify (if applicable, within 3 business days of hire) 3) Enter employee in payroll system with correct withholding (W-4, state withholding form) 4) Enroll in benefits (health, dental, vision, 401(k), commuter) — coordinate effective date with carrier 5) Add to HRIS with correct job title, department, manager, compensation, and start date 6) Provide employee handbook acknowledgment form 7) Schedule new hire orientation with IT (equipment), facilities (badge/desk), and team (intro meetings)
**What good looks like:** Day 1: employee can log into all systems, has a badge, a desk, a manager who knows they're coming, and has completed I-9, W-4, and benefits enrollment. Benefits effective date matches hire date.

### Phase 2 (~20 min): Leave of Absence Administration
**Steps:** 1) Determine leave type (FMLA, state leave, STD/LTD, personal, military) using the decision tree above 2) Provide employee with leave request form and medical certification (if applicable) 3) Notify employee of rights, responsibilities, and expected timeline under the applicable law/policy 4) Track leave dates, intermittent leave usage, and FMLA balance (12 weeks per 12-month rolling period) 5) Coordinate with payroll: unpaid leave, paid leave supplement, or contributions during leave (health insurance premiums) 6) Manage return-to-work: fitness-for-duty certification (if applicable), schedule coordination, accommodation review (ADA interactive process if needed)
**Time per leave case:** Simple leave (FMLA only) ~30 min setup + monthly tracking. Complex leave (overlapping FMLA + state leave + STD + accommodations) ~2 hours setup + weekly tracking.

### Phase 3 (~15 min): Benefits Administration
**Steps:** 1) Manage open enrollment: communicate changes, collect elections, process with carriers, reconcile payroll deductions 2) New hire enrollment: ensure elections submitted within eligibility window (typically 30 days) 3) COBRA administration: within 44 days of qualifying event, send election notice. Track election deadline (60 days from notice), payment deadline (45 days from election) 4) ACA compliance: offer minimum essential coverage to 95%+ of FTEs (50+ FTEs), distribute Form 1095-C by March 2 5) 401(k) compliance: non-discrimination testing, safe harbor contributions, Form 5500 annual filing (due July 31, extension available)
**Calendar:**
- **Monthly:** Payroll deduction reconciliation, new hire enrollments, benefit termination for leavers
- **Quarterly:** 401(k) contribution review, COBRA compliance check
- **Annually:** Open enrollment (Oct-Nov), ACA filing (Jan), Form 5500 (Jul), benefits renewal analysis (Jun-Sep)

### Phase 4 (~10 min): Employee Relations & Documentation
**Steps:** 1) Maintain employee files: I-9 in a separate I-9 binder (never in the personnel file), personnel file (hiring docs, performance reviews, disciplinary actions, signed acknowledgments), medical files (separate, confidential) 2) Document all employee relations issues: date, parties involved, description, investigation steps, outcome, action taken 3) Follow progressive discipline (verbal warning → written warning → PIP → termination) or document why immediate termination is warranted (theft, violence, severe misconduct) 4) Upon termination: final paycheck within legal timeframe (varies by state — some require same-day), COBRA notice, benefits termination, equipment return, system access revocation
**File retention:** I-9: 3 years from hire or 1 year from termination (whichever is later). Personnel records: 3+ years (state-specific). Medical records: 3+ years (ADA requires confidential storage).

### Phase 5 (~5 min): Compliance Monitoring
**Monthly:** Review new hire reporting (states require within 20 days), workers' compensation claims updates, unemployment claim responses (respond within 10 days typically), labor law poster compliance (posters must be current and visible in all locations). **Quarterly:** Exemption classification audit (any promotion/role change), I-9 self-audit (sample file review for completeness), OSHA 300 log posting (Feb 1-Apr 30, if required). **Annually:** Employee handbook review (update policies for new laws), ACA filing (by Jan 31/Feb 28/Mar 31), Form 5500, harassment prevention training (CA: AB 1825 every 2 years, others as required), pay equity audit.

## Best Practices
<!-- STANDARD: 3min -- rules extracted from HR experience -->

- **Never mix I-9s with personnel files.** I-9s must be in a separate binder available for DHS/ICE inspection on request. Mixing them means sensitive documents (medical, disciplinary) get exposed during an I-9 audit.
- **Document everything, especially when it's hard.** If a performance issue isn't documented, it didn't happen. Documentation should be factual, specific, and contemporaneous: "On 3/15, told the employee their report was 5 days late" not "employee has trouble meeting deadlines."
- **State laws always add complexity.** No state makes HR easier. When implementing any new policy, check: CA (most protective), NY, WA, OR, CO, MA, IL, NJ, MD, HI. These states have paid leave, paid sick leave, higher salary thresholds, and stricter documentation requirements.
- **COBRA deadlines are non-negotiable.** Missing the 44-day notice deadline means the employer may be liable for the employee's medical expenses during the gap period. Automate COBRA administration or use a third-party administrator.
- **Benefits during leave:** Employer must continue health insurance coverage during FMLA leave. The employee must continue paying their share. Track premium payments during unpaid leave — if they miss payment, you have a 30-day grace period before canceling.
- **ADA interactive process** is triggered whenever an employee with a disability requests accommodation — not just when they need leave. Have a standard accommodation request form and a documented process for engaging in the interactive dialogue.
- **PTO policies vary by state:** CA requires unlimited accrual (no use-it-or-lose-it). Some states require payout on termination (CA, IL, MA, ME, NE, etc.). Others allow forfeiture per policy. Know your state rules before drafting the policy.

## Scale Depth: Solo → Small → Medium → Enterprise

| Dimension | Solo (1) | Small (2-50) | Medium (50-500) | Enterprise (500+) |
|-----------|----------|-------------|-----------------|-------------------|
| **HR headcount** | Founder handles HR | 1 HR generalist | HR team (generalist + specialist) | HRBP model + COEs |
| **HRIS** | Spreadsheet | Gusto/Rippling/BambooHR | Rippling/BambooHR/Workday | Workday/SAP SuccessFactors |
| **Benefits** | Marketplace plan | PEO or broker-managed | Broker-managed + 401(k) provider | Self-funded + multiple carriers |
| **Compliance** | Basic state/federal | PEO covers most | In-house + employment counsel | In-house + team of counsel |
| **Leave management** | Manual tracking | HRIS-managed | HRIS + vendor (DMEC, Sedgwick) | Dedicated leave administration team |

### Error Decoder

| Problem | Root Cause | Fix |
|---------|------------|-----|
| Top performer quits unexpectedly | No retention risk signal detected | Implement pulse surveys with eNPS tracking. Flag any employee whose engagement score drops >20 points. Conduct stay interviews (not just exit interviews) — ask "what would make you leave?" before they decide. |
| Offer rejected at signing stage | Compensation not benchmarked, or process took too long | Benchmark every offer against market data (Radford/Pave). Time-to-offer should be < 5 business days from final interview. Equity offers need a clear narrative: "this refreshes every year, here's the projected value at IPO." |
| New hire underperforms after 90 days | No structured onboarding with milestones | 0-30-60-90 day plan with weekly check-ins. First week: systems access, team intros, small win. First 30 days: complete a defined project with measurable outcome. If no structure by day 30, the problem is the onboarding, not the hire. |
| Performance review results surprise the employee | Feedback only given during review cycles | Continuous feedback culture: written feedback within 48 hours of observing behavior. No surprises in formal reviews — every review item should have been discussed at least once before. Surprises in reviews are management failures. |
| Pay equity complaint or lawsuit | Compensation not audited for bias | Run annual pay equity audit by gender, race, and tenure. Adjust salaries to correct disparities — don't wait for a complaint. Publish compensation band ranges internally (transparency reduces bias). |
| DEI program has no measurable impact | Metrics measured for activity, not outcomes | Track: representation at each level, promotion rates by demographic, retention by demographic, pay equity by demographic. If promotion and retention rates are equal across groups but representation isn't, fix the pipeline. If they're not equal, fix the culture. |
| HRIS migration takes 3x longer than estimated | Data mapping not done before implementation | Start with a complete data audit before selecting the HRIS. Map every field from source → target. Test migration with a full data set in staging. Plan for 2x your optimistic timeline — HR data is always messier than expected. |


## Production Checklist
<!-- QUICK: 30s -- all must pass before an audit or new hire -->

- [ ] **[H1]** I-9s maintained in a separate binder from personnel files, completed within 3 business days
- [ ] **[H2]** E-Verify queries submitted within 3 business days of hire (if required in your state)
- [ ] **[H3]** Employee handbook reviewed and updated within the last 12 months
- [ ] **[H4]** All required labor law posters posted in all physical locations (federal + state + local)
- [ ] **[H5]** Annual harassment prevention training completed (state-specific cadence: CA every 2 years, NY annually)
- [ ] **[H6]** FMLA eligibility tracker maintained: 12-month rolling period, intermittent leave accounting
- [ ] **[H7]** COBRA administration current: all qualifying events have notices sent, election periods tracked
- [ ] **[H8]** Workers' compensation insurance policy in force for all employees in all states of operation
- [ ] **[H9]** ACA tracking active: FTE count confirmed, 1095-Cs distributed, 1094-C filed
- [ ] **[H10]** Form 5500 filed for 401(k) plan within deadline (July 31 with extension)
- [ ] **[H11]** Overtime-exempt classification reviewed and documented for every role
- [ ] **[H12]** Personnel files contain: offer letter, role changes, performance reviews, signed acknowledgments, discipline docs
- [ ] **[H13]** Benefits open enrollment completed, payroll deductions reconciled within 30 days
- [ ] **[H14]** Pay equity audit completed within last 12 months
- [ ] **[H15]** New hire reporting completed (state-specific deadlines, typically 20 days)

## Cross-Skill Integration
<!-- QUICK: 30s -- table of who to talk to when -->

| Step | Skill | What It Produces |
|------|-------|-----------------|
| **Before** | `recruiting` | Offer acceptance → triggers I-9, benefits enrollment, payroll setup in HR systems |
| **Before** | `people-ops` | Leveling framework, compensation bands → informs offer terms and role classification |
| **This** | `hr-manager` | Employee lifecycle compliance, benefits, leave management, file maintenance |
| **After** | `people-ops` | Consumes HR data (engagement scores, retention analysis) to design people programs |
| **After** | `fp-and-a-analyst` | Consumes headcount data, benefits cost trends, workers' comp claims for financial modeling |
| **After** | `legal-advisor` | Consumes documented policies and compliance records for legal review and litigation defense |
| **After** | `board-manager` | HR metrics (headcount, turnover, engagement) feed board reporting and compensation committee |

## What Good Looks Like

A compliant, well-run HR function has these characteristics:
- **Every new hire completes onboarding in under 2 hours** — I-9, payroll, benefits enrollment, handbook acknowledgment: all done before lunch on day one.
- **Leaves are managed without administrative drama** — the employee knows their rights, FMLA runs concurrently with state leave, COBRA notice goes out automatically. No missed deadlines, no liability.
- **An auditor could walk in tomorrow and find clean files** — I-9s are separate, personnel files are complete, medical files are locked. Every document is where it should be.
- **Benefits administration is invisible when it works** — open enrollment closes on time, payroll deductions match elections, COBRA is handled by a vendor or automated system. Nobody notices HR until something breaks.
- **Compliance calendar runs on autopilot** — ACA filing, Form 5500, labor law poster updates, harassment training — all scheduled and tracked. No last-minute scrambles before deadlines.
