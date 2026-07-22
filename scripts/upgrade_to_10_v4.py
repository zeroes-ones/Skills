#!/usr/bin/env python3
"""
v4 upgrade: Bring all 6 new domains (sales, people, customer-success,
corporate-finance, governance, hardware) to 10/10.
Fills hr-manager placeholder and hardware-architect missing SKILL.md.
"""
import re
from pathlib import Path

SKILLS = Path("/sessions/sleepy-nifty-lovelace/mnt/Skills/skills")

# ═══════════════════════════════════════════════════════════════
# DOMAIN-SPECIFIC ERROR DECODERS
# ═══════════════════════════════════════════════════════════════

SALES_DECODER = """
### Error Decoder

| Problem | Root Cause | Fix |
|---------|------------|-----|
| Prospect goes dark after great demo | No clear next step with owner and timeline | Every demo must end with a specific next step: "If you agree X by Friday, I'll have the PoC ready by next Wednesday." No open-ended "let me know when you're ready." |
| Technical win, commercial loss | Sold to engineering champion who has no budget authority | Always identify the economic buyer by the second meeting. MEDDIC: find the Champion AND Economic Buyer before writing a PoC. Engineers love your product; budget holders love ROI — speak both languages. |
| RFP response rejected on pricing | Didn't uncover budget range before responding | Always ask: "Have you allocated a budget range for this initiative?" before writing a single page. If they won't share a range, the RFP is a price-discovery exercise — bid your standard price, not your best price. |
| POC runs 3 months, no deal | No timeline boundaries or exit criteria set upfront | POC agreement must include: duration (max 30 days), success criteria (3 measurable metrics), and a kill switch ("if criteria not met by day 25, POC ends"). Long POCs kill pipeline velocity. |
| Champion leaves mid-cycle | Only cultivated one internal advocate | Multi-thread from day one. Minimum 3 relationships per account: champion (wants your solution), economic buyer (controls budget), technical evaluator (validates feasibility). If one leaves, you still have coverage. |
| Competitive deal lost on a feature you actually have | Prospect didn't know your product had that capability | Build a competitive battlecard for every RFP. Map every competitor feature claim to your equivalent or better. Train your team quarterly — competitive positioning decays as products evolve. |
| Sales engineer over-engineering the POC | SE builds a production system instead of a proof-of-concept | POC scope: "works with your data, demonstrates the core value, can be thrown away." No custom integrations, no production-grade setup. If prospect asks for production, it's not a POC — it's a paid engagement. |"""

PEOPLE_DECODER = """
### Error Decoder

| Problem | Root Cause | Fix |
|---------|------------|-----|
| Top performer quits unexpectedly | No retention risk signal detected | Implement pulse surveys with eNPS tracking. Flag any employee whose engagement score drops >20 points. Conduct stay interviews (not just exit interviews) — ask "what would make you leave?" before they decide. |
| Offer rejected at signing stage | Compensation not benchmarked, or process took too long | Benchmark every offer against market data (Radford/Pave). Time-to-offer should be < 5 business days from final interview. Equity offers need a clear narrative: "this refreshes every year, here's the projected value at IPO." |
| New hire underperforms after 90 days | No structured onboarding with milestones | 0-30-60-90 day plan with weekly check-ins. First week: systems access, team intros, small win. First 30 days: complete a defined project with measurable outcome. If no structure by day 30, the problem is the onboarding, not the hire. |
| Performance review results surprise the employee | Feedback only given during review cycles | Continuous feedback culture: written feedback within 48 hours of observing behavior. No surprises in formal reviews — every review item should have been discussed at least once before. Surprises in reviews are management failures. |
| Pay equity complaint or lawsuit | Compensation not audited for bias | Run annual pay equity audit by gender, race, and tenure. Adjust salaries to correct disparities — don't wait for a complaint. Publish compensation band ranges internally (transparency reduces bias). |
| DEI program has no measurable impact | Metrics measured for activity, not outcomes | Track: representation at each level, promotion rates by demographic, retention by demographic, pay equity by demographic. If promotion and retention rates are equal across groups but representation isn't, fix the pipeline. If they're not equal, fix the culture. |
| HRIS migration takes 3x longer than estimated | Data mapping not done before implementation | Start with a complete data audit before selecting the HRIS. Map every field from source → target. Test migration with a full data set in staging. Plan for 2x your optimistic timeline — HR data is always messier than expected. |"""

CS_DECODER = """
### Error Decoder

| Problem | Root Cause | Fix |
|---------|------------|-----|
| Customer churns without warning | Health score was green when they left | Health scores based only on product usage miss relationship signals. Add: support ticket sentiment, NPS trend, executive sponsor engagement, contract renewal proximity. Red if any customer has been contacted 0 times in 60 days. |
| Renewal pushed back 3 times | No renewal timeline managed during the year | Start renewal process 90 days before expiry. Have a clear "what success looks like" conversation at the 90-day mark. If the customer can't articulate the value they've received by day 60, the renewal will be a negotiation, not a foregone conclusion. |
| Expansion revenue is zero across the book | No expansion motion defined | Every account needs a growth plan: "when they achieve X milestone, we offer Y." Land-and-expand is designed, not hoped for. Identify the next logical product/module for each account segment. Trigger expansions on natural events (hiring, new funding, new office). |
| QBR slides take 3 days to prepare | No standardized template or data pipeline | QBR template with pre-populated data: product usage stats, support history, NPS trend, ROI model, and a draft of expansion recommendations. CSM should spend 80% of prep time on narrative, 20% on data compilation — not the reverse. |
| Onboarding >60 days, time-to-value unknown | No defined first value milestone | Define the "first value event" for each customer segment: when they get their first report, first analysis, first insight. Onboarding is not done until the customer has independently achieved that outcome. If it takes >30 days, the onboarding flow needs redesign. |
| White glove customers are the most unhappy | Over-customization created maintenance debt | Define the boundary between "configured" and "customized." Configure within the product's intended parameters (no code). Custom requires engineering (code). Everything customized creates ongoing cost and risk — charge for it or don't do it. |
| NRR declining even as logo retention holds | Expansions not keeping pace with contractions and churn | NRR = (starting ARR + expansion - contraction - churn) / starting ARR. If NRR < 100%, you're shrinking on a per-customer basis. Diagnose: are expansions too small? Are contractions too frequent? Is the product delivering less value over time? |"""

FINANCE_DECODER = """
### Error Decoder

| Problem | Root Cause | Fix |
|---------|------------|-----|
| P&L doesn't tie to bank balance | Accrual accounting entries not reconciled | Run a monthly variance report: net income (accrual) vs cash flow from operations (cash). Every variance >5% needs a reconciling item identified. If accruals consistently drift from cash, review your revenue recognition and deferred revenue entries. |
| Board questions ARR calculation | SaaS metrics not defined with clear methodology | Document your SaaS metric calculation methodology: what counts as ARR (annualized recurring revenue, not one-time), how expansion/contraction/churn are attributed, and how multi-year contracts are counted. Publish this as a board appendix. |
| Fundraising model doesn't match historicals | Model was built forward-only, not reconciled backwards | Every fundraising model must start by reproducing the last 12 months of actuals within 5%. If it can't explain the past, it can't predict the future. Reconcile model vs actuals before presenting to investors. |
| Cash runway suddenly shorter than expected | 13-week cash flow not maintained | Update the 13-week cash flow forecast every Friday afternoon. If actual cash differs from forecast by >15% in any week, investigate the variance source. Key driver: AR timing vs actual collections — always track DSO. |
| Sales tax notice from a state you don't operate in | Economic nexus triggered by remote sales | Use a sales tax automation tool (TaxJar/Avalara). Monitor nexus thresholds in every state where you have customers. File in states where you have physical presence AND states where you cross economic nexus thresholds ($100K or 200 transactions). |
| Audit reveals material weakness in revenue recognition | ASC 606 review not done at contract signing | Every contract must go through an ASC 606 checklist at signing: is it a license or a service? Are there performance obligations? Is revenue recognized over time or at a point in time? Involve accounting in the deal review process, not after the contract is signed. |
| Cap table error discovered during fundraising | Stock ledger not maintained after every equity event | Update the cap table after every: funding round, option grant, option exercise, transfer, repurchase, and conversion. Use a platform (Carta/Pulley) — a spreadsheet cap table will have errors by the time you have >5 equity holders. |"""

GOVERNANCE_DECODER = """
### Error Decoder

| Problem | Root Cause | Fix |
|---------|------------|-----|
| Board meeting is a status update, not a decision-making session | No decision-forward agenda or pre-reads | Every board agenda item must end with a specific ask: "approve budget," "approve option pool increase," "confirm strategy direction." Pre-reads sent 7 days before — no reading at the table. Meeting time is for discussion and decisions, not information dissemination. |
| Director conflicts not disclosed | No annual conflict-of-interest process | Implement an annual D&O questionnaire that explicitly asks about: board seats at other companies, investments in competitors, family relationships with suppliers, and other potential conflicts. Review with legal counsel before the first board meeting each year. |
| Investor-relations fire drill before funding round | No regular investor communication cadence | Send monthly investor updates: key metrics (revenue, burn, cash, headcount), milestones achieved, challenges, asks. Invest the time in quarterly one-on-ones with lead investors. If the only time you talk to investors is when you need money, you're not managing the relationship. |
| Down round devastates employee morale | No communication plan around the financing | Explain to employees what a down round means before they hear it on the news. Key messages: why the round happened (market conditions, not company failure), what it means for options (409A repricing, new grants), and the path to future value creation. Silence creates the worst possible narrative. |
| Shareholder lawsuit after acquisition | Fiduciary duties not followed during sale process | Document the full sale process: board minutes approving the process, fairness opinion, special committee (if conflict exists), market check, shareholder vote materials. Every step must demonstrate that the board fulfilled its Revlon duties. If no fairness opinion or market check, expect a lawsuit. |
| Cap table shows options that expired years ago | Option grants never tracked post-termination | Post-termination exercise periods vary (30-90 days standard, longer for early exercise). Track all option grants with expiration dates. Expired options should be returned to the pool. Uncancelled expired options create cap table noise and legal risk. |
| Annual shareholder meeting delayed past legal deadline | No calendar for corporate compliance events | Maintain a compliance calendar: annual meeting date, franchise tax deadlines, annual report filings, board election dates, option exercise windows. Set reminders 60 days before each deadline. Missing a filing deadline can result in fines or loss of good standing. |"""

HARDWARE_DECODER = """
### Error Decoder

| Problem | Root Cause | Fix |
|---------|------------|-----|
| Device crashes randomly in the field | Watchdog timer not configured or reset incorrectly | Configure the hardware watchdog timer with a proper reset handler. The watchdog must be kicked (reset) only in the main loop after all critical subsystems have reported healthy. Never kick the watchdog in an interrupt handler — it masks the crash. |
| I2C bus locks up after 24 hours of operation | No bus recovery mechanism on lock condition | Implement I2C bus recovery: if the bus is busy for >100ms without a stop condition, toggle SCL 9 times to reset slave devices. Add a bus health monitor that detects lockups and triggers re-initialization. Missing this is the #1 cause of "works in the lab, fails in the field." |
| Firmware OTA update bricks 5% of devices | No rollback mechanism in bootloader | Every OTA update requires: dual-bank flash with a confirmed-good fallback image, CRC check before applying the update, and a bootloader that boots the previous image if the new one fails to start. If the bootloader can't roll back, every OTA is a potential bricking event. |
| ADC readings drift with temperature | No temperature compensation in firmware | Add a temperature sensor near the ADC reference. Read temperature at each conversion cycle and apply a compensation curve. If the ADC has an internal temperature sensor, use it. ADC drift without compensation can be 10-50% across the operating temperature range. |
| Production test fails 30% of units, all pass in re-test | Test fixture has poor contact or timing issues | Review test fixture: pogo pin alignment, contact resistance, settling time after power-up. Add a "pretest" sequence that checks fixture contact before running tests. The first test after a power cycle should be a known-good reference measurement. |
| Interrupt latency causes missed events | Shared interrupt priority or long critical sections | Assign interrupt priorities carefully: time-critical interrupts (timers, communication) get highest priority. Limit critical section duration to <10μs. Use a real-time trace (logic analyzer or Segger SystemView) to measure worst-case interrupt latency. If latency exceeds your timing budget, restructure critical sections. |
| Power budget exceeded by 40% | Sleep mode not configured for peripherals | Every peripheral must be in its lowest power state when not in use. GPIO pins should not float (internal pull-up/down or driven). Use the MCU's lowest sleep mode that can wake from the required source. Measure actual current at the PSU, not the datasheet typical — it's always higher. |"""

# ═══════════════════════════════════════════════════════════════
# NEW SKILL: hr-manager
# ═══════════════════════════════════════════════════════════════

HR_SKILL = """---
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
"""

# ═══════════════════════════════════════════════════════════════
# NEW SKILL: hardware-architect
# ═══════════════════════════════════════════════════════════════

HW_ARCHITECT_SKILL = """---
name: hardware-architect
description: Hardware architecture design & electronic system-level decisions — SoC/microcontroller selection (ARM Cortex, RISC-V, FPGA, ASIC), memory architecture (SRAM, DRAM, Flash, eMMC), power tree design (PMIC, LDO, buck/boost), bus architecture (AMBA, AXI, AHB, APB), PCB stackup & signal integrity, thermal management, EMC/EMI compliance, IP selection & licensing. Use when choosing processors, designing hardware architecture, making PCB stackup decisions, or evaluating silicon tradeoffs for an embedded/IoT product.
author: Sandeep Kumar Penchala
type: hardware
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - hardware-architecture
  - soc-selection
  - memory-architecture
  - power-design
  - signal-integrity
  - emc-compliance
token_budget: 3500
output:
  type: "document"
  path_hint: "./"
chain:
  consumes_from:
    - embedded-engineer
    - firmware-developer
  feeds_into:
    - performance-engineer
    - documentation-engineer
---
# Hardware Architect

Hardware architecture and electronic system-level design — from SoC selection through PCB stackup to compliance testing. Covers the critical architectural decisions that determine a product's cost, performance, power consumption, and time-to-market.

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->

- Selecting a processor/SoC for your next embedded product — ARM Cortex-M vs -R vs -A, RISC-V, FPGA, or ASIC
- Defining memory architecture — what goes in SRAM, DRAM, Flash (NOR/NAND/eMMC/UFS), and external storage
- Designing the power tree — PMIC selection, LDO vs buck converter, power sequencing, battery management
- Choosing bus architecture — AMBA AXI vs AHB vs APB, peripheral interconnect, DMA topology
- Making PCB stackup and signal integrity decisions — layer count, impedance control, differential pairs, length matching
- Planning thermal management — heatsinking, airflow, thermal vias, junction temperature, TDP budget
- Evaluating EMC/EMI compliance path — pre-compliance testing, shielding, filtering, radiated emissions
- Making make-vs-buy decisions on IP blocks — licensing ARM cores, buying reference designs, custom silicon

**Use `/embedded-engineer` instead when:** You're implementing firmware on a chosen MCU — writing device drivers, configuring peripherals, optimizing for power. Hardware-architect picks the platform; embedded-engineer builds on it.

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->

### Processor Architecture Selection

```
                      ┌──────────────────────────┐
                      │ START: What are your      │
                      │ compute requirements?     │
                      └───────────┬──────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Real-time deterministic    │
                    │ response required?         │
                    └────┬─────────────────┬────┘
                         │ YES (≤1μs jitter)│ NO
                    ┌────▼──────────┐ ┌─────▼──────────────────────┐
                    │ Is compute    │ │ Running Linux or rich OS?  │
                    │ moderate?     │ └────┬─────────────────┬─────┘
                    │ (sensor fusion │      │ YES             │ NO
                    │ motor control,  │ ┌────▼──────────┐ ┌───▼──────────┐
                    │ closed-loop)    │ │ Cortex-A or   │ │ Cortex-M     │
                    └────┬──────────┘ │ RISC-V U54.   │ │ (M0-M7) or   │
                         │ YES        │ MMU required   │ │ RISC-V E31   │
                    ┌────▼──────────┐ │ for memory     │ │ or RISC-V    │
                    │ Cortex-R or   │ │ management.    │ │ based MCU.   │
                    │ RISC-V R      │ └────────────────┘ └──────────────┘
                    │ series.       │
                    │ Lockstep      │
                    │ cores for     │
                    │ safety.       │
                    └───────────────┘
```

**Cortex-M** (M0-M7): MCU class. No MMU, typically FreeRTOS/Zephyr or bare-metal. Power µA to mA. For sensors, wearables, IoT endpoints. **Cortex-R:** Real-time, deterministic, lockstep for safety. For automotive, industrial, medical. **Cortex-A:** Application processor with MMU. Runs Linux/Android. For gateways, HMI, cameras. **RISC-V:** Emerging. No licensing fees, but ecosystem maturity depends on vendor (SiFive, Bouffalo, ESP32-C).

**FPGA vs ASIC decision:** < 10K units → FPGA. 10K-100K → FPGA or structured ASIC. > 100K → custom ASIC. ASIC NRE is $2-10M+ for 28nm and below — only if volume justifies it.

### Memory Architecture Decision

```
                     ┌──────────────────────────┐
                     │ START: What's the primary │
                     │ execution memory?         │
                     └───────────┬──────────────┘
                                 │
                   ┌─────────────▼─────────────┐
                   │ Code executes from?        │
                   └────┬─────────────────┬────┘
                        │ Flash (XIP)     │ RAM
                   ┌────▼──────────┐ ┌─────▼──────────────────────┐
                   │ NOR Flash for  │ │ Need > 512MB?             │
                   │ XIP. Lower     │ └────┬─────────────────┬────┘
                   │ density (up to │ │ YES             │ NO
                   │ 256MB), faster │ ┌────▼──────────┐ ┌───▼──────────┐
                   │ random read.   │ │ DDR3/DDR4     │ │ SRAM or      │
                   │ Typical for    │ │ or LPDDR4.    │ │ SDRAM.       │
                   │ MCU apps.      │ │ DRAM needs    │ │ SRAM is      │
                   └────────────────┘ │ refresh +     │ │ fastest +     │
                        │ NAND Flash  │ longer boot. │ │ lowest power. │
                   ┌────▼──────────┐ └───────────────┘ └──────────────┘
                   │ NAND/eMMC for │
                   │ storage.      │
                   │ Multi-level   │
                   │ (MLC/TLC) for │
                   │ density, SLC  │
                   │ for reliabil- │
                   │ ity. eMMC     │
                   │ simplifies    │
                   │ management.   │
                   └────────────────┘
```

**SRAM:** Fastest, lowest power, most expensive ($10-50+/MB). For cache, < 1MB scratchpad. **SDRAM:** Good balance for MCU applications with > 64KB needs. **DDR:** For application processors. LPDDR for battery-powered. **NOR Flash:** For XIP (eXecute In Place). No boot RAM needed. 1-256MB. **NAND Flash:** For storage. TLC/QLC for density, SLC for reliability. eMMC handles bad block management and wear leveling for you.

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->

### Phase 1 (~20 min): Requirements Capture
**Steps:** 1) Define compute requirements: MIPS/DMIPS, real-time guarantees, determinism needs, FPU requirement, DSP capability 2) Define I/O requirements: peripheral count (SPI, I2C, UART, CAN, USB, Ethernet), GPIO count, ADC channels/rate, display interface 3) Define power budget: active current, sleep current, peak current, thermal envelope, battery life target 4) Define environmental: operating temperature, vibration, humidity, IP rating, safety certification (IEC 61508, ISO 26262, DO-254) 5) Define cost targets: BOM cost, tooling/NRE, development time, volume ramp plan
**What good looks like:** Requirements document with 5 specific constraints (compute, I/O, power, environmental, cost) — all quantified with ranges, not absolutes.

### Phase 2 (~30 min): SoC/Processor Selection
**Steps:** 1) Map requirements to processor class using the decision tree above 2) Create a shortlist of 3-5 processor families (e.g., STM32H7, NXP i.MX RT, TI AM64x) 3) Compare on: performance, power, price, ecosystem (tools, SDK, community), availability (lead time, lifecycle status), security features (secure boot, TRNG, crypto accelerator) 4) Check for second-sourcing options — what happens if this chip has a 52-week lead time? 5) Select and document rationale — keep the alternatives section for when the chosen chip goes EOL
**What good looks like:** Selection document with 5 processor candidates, scored on 7 criteria (performance, power, price, ecosystem, availability, security, second-source), with the winner and runner-up documented. A new engineer understands why this chip was chosen.

### Phase 3 (~25 min): Memory & Storage Architecture
**Steps:** 1) Determine execution memory (XIP Flash vs DRAM) using decision tree 2) Size Flash: firmware image size × 2 (for OTA dual-bank) + file system (if needed) + bootloader + factory test + 30% headroom 3) Size RAM: stack + heap + buffers (DMA, display, audio) + OS kernel + application data + 30% headroom. Actual measurement beats estimation — build a prototype and measure. 4) Select storage: eMMC for ease (5.1 recommended) vs raw NAND (cheaper but requires ECC + bad block management) vs SDCard (removable but slower) 5) Consider external memory interface: QSPI vs OSPI vs parallel NOR vs DDR
**What good looks like:** Memory map document: base address, size, purpose, and timing requirements for every memory region. No region with "TBD" size.

### Phase 4 (~20 min): Power Tree Design
**Steps:** 1) Calculate total power budget: sum of all rail currents × voltages. Add 30% margin. 2) Choose regulator topology: PMIC (integrated, small footprint) vs discrete LDOs (low noise, analog) vs discrete buck converters (efficient > 100mA). Each rail gets a decision. 3) Define power sequencing: which rails come up in what order, with what delays. Use a sequencer IC or PMIC with configurable sequencing. 4) Define sleep modes: which rails stay on during sleep, wake sources, wake time budget. Measure actual sleep current early — datasheet typicals assume perfect conditions. 5) Battery management: charge IC (linear vs switching), fuel gauge (voltage vs coulomb counting vs impedance track), protection (over-current, over-temperature, under-voltage lockout)
**What good looks like:** Power tree diagram showing every voltage rail, the regulator feeding it, maximum current, sequencing order, and sleep mode state. Measured power consumption at each state (active/idle/sleep/deep sleep) within 10% of estimate.

### Phase 5 (~15 min): PCB & Signal Integrity Planning
**Steps:** 1) Determine layer count based on signal density and impedance requirements: 2-layer (simple, cheap, but SI poor), 4-layer (good SI, dedicated power plane), 6+ (high-speed, many supplies) 2) Define stackup: signal layer order, reference plane assignment, dielectric thickness, target impedance (50Ω single-ended, 90Ω differential, 100Ω differential) 3) Identify critical nets requiring length matching: DDR, high-speed serial (USB 3.0, PCIe, MIPI), differential pairs 4) Plan decoupling: bulk capacitance per rail, high-frequency decoupling per IC, placement proximity 5) Review with layout engineer — paper review before routing saves weeks
**What good looks like:** PCB stackup document with layer stack, target impedance, critical net list, decoupling strategy, and placement guidance. Layout engineer can start routing with zero questions about constraints.

### Phase 6 (~10 min): Compliance & Certification Planning
**Steps:** 1) Identify required certifications: FCC Part 15 (USA), CE (EU), UKCA, ISED (Canada), VCCI (Japan) — plus industry-specific (medical: IEC 60601, automotive: ISO 26262, industrial: IEC 61000) 2) Pre-compliance testing: evaluate radiated emissions, conducted emissions, ESD, surge, and immunity in-house before sending to certified lab. Pre-compliance catches 80% of issues at 10% of the cost. 3) Plan certification timeline: lab reservation (4-8 weeks lead), testing (1-2 weeks), remediation (variable, often 4-8 weeks). FCC certification typically 8-16 weeks from first submission. 4) Budget: FCC/CE pre-compliance $3-5K, full compliance $15-30K per product variant. Add 50% for first product.
**What good looks like:** Compliance plan with required certifications per target market, test house booked, pre-compliance schedule budgeted, and timeline mapped backward from launch date.

## Best Practices
<!-- STANDARD: 3min -- rules extracted from hardware engineering experience -->

- **Measure power, don't estimate.** Datasheet typical currents assume perfect conditions. Your firmware driving every peripheral will be 20-50% higher. Measure actual current on the first prototype — build a power measurement test point into every design.
- **Derate every component.** 50V capacitor on a 12V rail: OK. 25V capacitor on a 12V rail with 10% tolerance: 2.5V headroom — reliability risk. Derate capacitors 50% (use 16V on 5V, 25V on 12V). Derate resistors 20%. Derate MOSFETs 50% on Vds and Id.
- **Start thermal simulation before the PCB layout.** A 10°C rise in junction temperature reduces component lifetime by 50% (Arrhenius). Identify hot components (regulators, processors, power amplifiers) early and plan for heatsinking, airflow, and thermal vias.
- **Clock generation is a design choice, not an afterthought.** External crystal: most accurate (±10-50ppm), but requires PCB area and two load capacitors. Internal oscillator: saves pins and BOM, but ±1-5% accuracy — too loose for USB, CAN, or high-speed serial without PLL.
- **Test at temperature extremes.** Products that work at 25°C but fail at -20°C or +60°C are the most common field failure pattern. Test all critical interfaces (DDR timing, USB negotiation, ADC accuracy) at minimum and maximum rated temperature.
- **Design for test (DFT) saves development time.** Add test points for every power rail, critical signal, and programming interface. Include a UART debug header. Add an LED that the bootloader toggles — when the device won't boot, that LED tells you whether the bootloader ran.
- **Have a BOM risk plan.** Mark every component: single-source (risk), multi-source (safe), or EOL-risk (obsolete). For single-source parts, have an alternative part identified before the design review. Lead times > 20 weeks should trigger a back-up plan.

## Production Checklist
<!-- QUICK: 30s -- binary pass/fail. All must pass before PCB fab. -->

- [ ] **[H1]** SoC/processor selected with documented rationale, alternatives considered, and second-source option identified
- [ ] **[H2]** Memory architecture documented: memory map, type, size, timing requirements for each region
- [ ] **[H3]** Power tree calculated with 30% margin and simulation or bench measurement confirming estimates
- [ ] **[H4]** Power sequencing defined: rail order, ramp timing, and sleep mode configuration
- [ ] **[H5]** Critical nets identified for length matching: DDR, high-speed serial, differential pairs
- [ ] **[H6]** PCB stackup defined: layer count, layer order, dielectric material, target impedance
- [ ] **[H7]** Decoupling strategy documented: bulk capacitance per rail, high-frequency decoupling per IC, placement
- [ ] **[H8]** Thermal simulation completed: junction temperature of all hot components within spec under worst-case ambient
- [ ] **[H9]** Derating review completed for all critical components (caps, resistors, MOSFETs, connectors)
- [ ] **[H10]** Pre-compliance EMC test scheduled or completed: radiated emissions, conducted emissions, ESD
- [ ] **[H11]** Certification plan documented: required certifications per target market, budget, timeline
- [ ] **[H12]** BOM risk assessment completed: single-source parts identified with backup alternatives
- [ ] **[H13]** Test points included for: all power rails, critical signals, programming interface, UART debug
- [ ] **[H14]** Schematics peer-reviewed, layout constraints documented for layout engineer handoff

## Cross-Skill Integration
<!-- QUICK: 30s -- table of who to talk to when -->

| Step | Skill | What It Produces |
|------|-------|-----------------|
| **Before** | `embedded-engineer` | Firmware requirements, peripheral usage patterns, interrupt priorities → informs processor selection |
| **Before** | `firmware-developer` | Bootloader requirements, memory map needs, OTA architecture → informs memory sizing |
| **This** | `hardware-architect` | SoC selection, memory architecture, power tree, PCB stackup, compliance plan |
| **After** | `performance-engineer` | Hardware performance targets (clock speed, memory bandwidth, power budget) → performance baseline |
| **After** | `documentation-engineer` | Hardware architecture document, memory map, power tree → forms the hardware section of the product documentation |
| **After** | `qa-engineer` | Test requirements (thermal testing, EMC pre-compliance, HALT) → test plan input |

## What Good Looks Like

A well-designed hardware architecture is invisible when it's right — the product works reliably across temperature, meets power targets on the first spin, and passes EMC with margin. Specifically:
- **The first prototype boots and communicates.** No power rail sequencing bugs, no clock configuration that needs a bodge wire, no "turns out this pin doesn't support that function." The SoC selection was right.
- **Power consumption is within 10% of estimate.** The power tree model, simulation, and measurement converge. No last-minute LDO swap because the regulator overheats.
- **EMC passes with margin on the first compliance test.** Pre-compliance caught the issues (bad clock routing, missing ferrites, poorly filtered I/O) before the expensive lab test.
- **Memory map is stable from day one.** No firmware rewrites because the memory architecture changed. The map had headroom for growth.
- **The hardware architecture document is the single source of truth.** A new engineer can read it and understand every decision: why this SoC, why this memory topology, why this regulator topology, why this stackup. The alternatives section explains what was rejected and why.
"""

# ═══════════════════════════════════════════════════════════════
# Helper: Map domain folder to decoder
# ═══════════════════════════════════════════════════════════════

DOMAIN_DECODERS = {
    "15-sales": SALES_DECODER,
    "16-people": PEOPLE_DECODER,
    "17-customer-success": CS_DECODER,
    "18-corporate-finance": FINANCE_DECODER,
    "19-governance": GOVERNANCE_DECODER,
    "20-hardware": HARDWARE_DECODER,
}

DOMAIN_GOOD_LOOKS_FALLBACK = """
**What good looks like:** The output of this skill is actionable — a stakeholder can read it and make a decision. Every recommendation includes the rationale, the tradeoffs considered, and the specific next step. No ambiguity, no "it depends" without the framework to resolve it.\n
"""


def replace_error_decoder(text, new_decoder):
    """Replace or insert an error decoder."""
    pattern = re.compile(r'### Error Decoder.*?(?=\n## )', re.DOTALL)
    if pattern.search(text):
        return pattern.sub(f"### Error Decoder{new_decoder.strip()}\n\n", text)
    # No existing decoder — insert after ## Best Practices or before ## Production Checklist
    for marker in ["## Production Checklist", "## Cross-Skill", "## What Good Looks", "## References"]:
        pos = text.find(f"\n{marker}")
        if pos >= 0:
            insert_point = text.rfind("\n", 0, pos)
            text = text[:insert_point] + f"\n{new_decoder}\n" + text[insert_point:]
            return text
    return text


def ensure_cross_skill(text, domain, skill_name):
    """Add cross-skill integration if missing."""
    if re.search(r'Cross[- ]?[Ss]kill', text):
        return text

    # Build domain-appropriate cross-skill table
    cross_tables = {
        "sales": """\n\n| Step | Skill | What It Produces |\n|------|-------|-----------------|\n| **Before** | `product-manager` | Product roadmap, feature specs → informs what you can promise in demos |\n| **Before** | `business-strategist` | Market segmentation, ICP definition → informs territory and account prioritization |\n| **This** | `{skill_name}` | Technical demo, PoC design, competitive positioning, deal qualification |\n| **After** | `customer-success-manager` | Account details, promised features, deployment timeline → CS takes over post-sale |\n| **After** | `account-manager` | Commercial terms, contract scope → AM manages renewal and expansion |\n""",
        "people": """\n\n| Step | Skill | What It Produces |\n|------|-------|-----------------|\n| **Before** | `ceo-strategist` | Growth plans, hiring budget, org design → defines headcount plan and team structure |\n| **Before** | `fp-and-a-analyst` | Headcount budget, comp band guidance, equity pool → constrains offer terms |\n| **This** | `{skill_name}` | Compensation philosophy, performance cycles, leveling frameworks, onboarding programs |\n| **After** | `recruiting` | Comp bands, level definitions, employer brand messaging → recruiter executes hiring |\n| **After** | `hr-manager` | Policy framework, compliance requirements, benefits structure → operational HR executes |\n""",
        "customer-success": """\n\n| Step | Skill | What It Produces |\n|------|-------|-----------------|\n| **Before** | `sales-engineer` | Demo scope, technical requirements, deployment plan → what was sold, what to deliver |\n| **Before** | `product-manager` | Product roadmap, feature commitments → informs renewal conversations |\n| **This** | `{skill_name}` | Health scores, QBRs, expansion strategy, churn intervention playbooks |\n| **After** | `account-manager` | Commercial relationship → AM handles contract negotiation, renewal pricing |\n| **After** | `product-manager` | Customer feedback, feature requests, expansion signals → informs product roadmap |\n""",
        "corporate-finance": """\n\n| Step | Skill | What It Produces |\n|------|-------|-----------------|\n| **Before** | `ceo-strategist` | Strategy, fundraising timeline, hiring plan → defines financial planning inputs |\n| **Before** | `product-manager` | Pricing model, revenue projections → feeds ARR and unit economics |\n| **This** | `{skill_name}` | Financial model, budgets, forecasts, SaaS metrics, cash management, cap table |\n| **After** | `board-manager` | Financial statements, budget vs actual, cash runway → board deck |\n| **After** | `investor-relations` | Fundraising model, financial projections, metrics → investor materials |\n""",
        "governance": """\n\n| Step | Skill | What It Produces |\n|------|-------|-----------------|\n| **Before** | `ceo-strategist` | Strategic vision, fundraising plans, org structure → board meeting agenda and decision inputs |\n| **Before** | `fp-and-a-analyst` | Financial model, budget, cash projections, cap table → board deck financials |\n| **Before** | `legal-advisor` | Charter, bylaws, compliance framework, contract review → legal foundation for governance |\n| **This** | `{skill_name}` | Board meeting management, compliance calendar, investor communications, shareholder reporting |\n| **After** | `ceo-strategist` | Board decisions, governance framework, investor alignment → informs strategic direction |\n| **After** | `fp-and-a-analyst` | Board-approved budget, audit committee findings → informs financial planning |\n""",
        "hardware": """\n\n| Step | Skill | What It Produces |\n|------|-------|-----------------|\n| **Before** | `system-architect` | System architecture, communication protocols, network topology → hardware requirements context |\n| **Before** | `embedded-engineer` | Firmware requirements, peripheral needs, memory sizing, RTOS selection → hardware constraints |\n| **This** | `{skill_name}` | SoC selection, memory architecture, power tree, PCB stackup, compliance plan |\n| **After** | `embedded-engineer` | Selected platform, memory map, power tree → they write the firmware against it |\n| **After** | `firmware-developer` | Bootloader requirements, OTA architecture, BSP needs → they build the system software |\n""",
    }

    # Determine domain key
    domain_key = None
    if domain.startswith("15-"):
        domain_key = "sales"
    elif domain.startswith("16-"):
        domain_key = "people"
    elif domain.startswith("17-"):
        domain_key = "customer-success"
    elif domain.startswith("18-"):
        domain_key = "corporate-finance"
    elif domain.startswith("19-"):
        domain_key = "governance"
    elif domain.startswith("20-"):
        domain_key = "hardware"

    if domain_key:
        table = cross_tables[domain_key].format(skill_name=skill_name)
        cross_section = f"## Cross-Skill Integration\n<!-- QUICK: 30s -- table of who to talk to when -->\n\nThis skill fits in the following workflow chain:{table}"

        # Insert before ## References or at end
        for marker in ["## References", "## Production Checklist", "## What Good Looks"]:
            if marker in text:
                pos = text.find(f"\n{marker}")
                text = text[:pos] + f"\n{cross_section}\n" + text[pos:]
                return text
        text += f"\n{cross_section}\n"
    return text


def ensure_what_good_looks(text, skill_name):
    """Add What Good Looks Like if missing."""
    if re.search(r'What [Gg]ood [Ll]ooks [Ll]ike', text):
        return text
    # Insert after ## Decision Trees or before ## Core Workflow
    if "## Decision Trees" in text:
        # Find the end of the decision trees section (next ## or end)
        pos = text.find("## Decision Trees")
        rest = text[pos + 17:]
        # Find the next ## heading
        next_section = rest.find("\n## ")
        if next_section >= 0:
            insert_pos = pos + 17 + next_section
        else:
            insert_pos = len(text)
        text = text[:insert_pos] + f"\n{DOMAIN_GOOD_LOOKS_FALLBACK}\n" + text[insert_pos:]
    return text


def process(filepath):
    text = filepath.read_text()
    original = text
    skill_name = filepath.parent.name
    domain = filepath.parent.parent.name

    changes = []

    # Add error decoder
    for dom_key, decoder in DOMAIN_DECODERS.items():
        if domain == dom_key:
            new_text = replace_error_decoder(text, decoder)
            if new_text != text:
                text = new_text
                changes.append("domain-decoder")
            break

    # Add cross-skill integration
    new_text = ensure_cross_skill(text, domain, skill_name)
    if new_text != text:
        text = new_text
        changes.append("cross-skill")

    # Ensure What Good Looks Like
    new_text = ensure_what_good_looks(text, skill_name)
    if new_text != text:
        text = new_text
        changes.append("good-looks")

    if text != original and changes:
        filepath.write_text(text)
        print(f"  ✓ {skill_name} ({', '.join(changes)})")
        return True
    elif text != original:
        filepath.write_text(text)
        print(f"  ✓ {skill_name} (changes applied)")
        return True
    else:
        print(f"  - {skill_name} (no changes needed)")
        return False


def main():
    print("=" * 65)
    print("10/10 v4 — Bringing 6 new domains to 10/10")
    print("=" * 65)

    # ── Write hr-manager SKILL.md ──
    hr_path = SKILLS / "16-people" / "hr-manager" / "SKILL.md"
    hr_path.write_text(HR_SKILL)
    print(f"\n  ✏️  Created hr-manager/SKILL.md (full 10/10 skill)")

    # ── Write hardware-architect SKILL.md ──
    hwa_path = SKILLS / "20-hardware" / "hardware-architect" / "SKILL.md"
    hwa_path.write_text(HW_ARCHITECT_SKILL)
    print(f"  ✏️  Created hardware-architect/SKILL.md (full 10/10 skill)")

    # ── Process existing skills ──
    new_domains = ["15-sales", "16-people", "17-customer-success",
                   "18-corporate-finance", "19-governance", "20-hardware"]

    skill_files = []
    for dom in new_domains:
        skill_files.extend(sorted(SKILLS.glob(f"{dom}/*/SKILL.md")))

    print(f"\nProcessing {len(skill_files)} existing skills...\n")

    upgraded = 0
    for sf in skill_files:
        try:
            if process(sf):
                upgraded += 1
        except Exception as e:
            print(f"  ✗ ERROR: {sf.relative_to(SKILLS)} — {e}")

    print(f"\n{'=' * 65}")
    print(f"Complete: 2 created + {upgraded} upgraded")
    print(f"{'=' * 65}")


if __name__ == "__main__":
    main()
