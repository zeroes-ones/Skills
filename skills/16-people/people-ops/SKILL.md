---
name: people-ops
description: "People operations & employee experience: onboarding program design (0-30-60-90 day plans), compensation philosophy & band design (market percentiles, geo-differentials), performance review cycles (360 feedback, calibration sessions, 9-box grid), leveling frameworks & career ladders (IC vs management track), employee engagement surveys (eNPS, pulse checks), retention risk analysis, internal mobility programs, offboarding & exit interviews, HR compliance (I-9, EEO, FLSA classification, state-specific labor laws), HRIS implementation (Rippling/BambooHR/Workday). Use when designing people programs, running performance cycles, building compensation bands, or implementing HR systems."
author: Sandeep Kumar Penchala
type: people
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - people-ops
  - employee-experience
  - compensation
  - performance-management
  - onboarding
token_budget: 3500
output:
  type: "markdown"
  path_hint: "./"
chain:
  consumes_from:
    - hr-manager
    - recruiting
    - legal-advisor
  feeds_into:
    - hr-manager
    - recruiting
    - engineering-manager
---

# People Operations & Employee Experience

Operational backbone for scaling a company through people programs. From onboarding through offboarding — every program is measurable, every process is documented, every decision is anchored in philosophy before policy.

## Route the Request
<!-- QUICK: 30s — pick your path, skip the rest -->

What are you trying to do?
├── Design an onboarding program → Start at "Phase 1: Onboarding Program Design"
├── Build compensation bands → Jump to "Phase 2: Compensation Philosophy & Band Design"
├── Run a performance review cycle → Go to "Phase 3: Performance Review Cycles"
├── Create career ladders / leveling → Jump to "Phase 4: Leveling Frameworks & Career Ladders"
├── Run an engagement survey → Go to "Phase 5: Employee Engagement & Retention"
├── Handle an offboarding / exit → Jump to "Phase 6: Offboarding & Compliance"
├── Choose or implement an HRIS → Go to "HRIS Implementation" under Best Practices
├── Need compliance / legal review of policy → Invoke `legal-advisor` skill
├── Need performance management cycle → Invoke `hr-manager` skill
├── Need engineering team onboarding → Invoke `engineering-manager` skill
└── Don't know where to start? → Start at "Phase 1: Onboarding Program Design"

**Do not read the entire skill.** Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces.

- **Never design a program without measurement.** Every people program — onboarding, performance reviews, engagement surveys — must have a defined success metric before it launches. "We'll know it's working" is not a metric. "New hire productivity rating at 90 days ≥4/5" is a metric.
- **Never set comp without a philosophy.** A comp band without a stated philosophy (e.g., "We target 65th percentile for cash and 75th for total comp at Series C") is a band that will drift into chaos. Write the philosophy first; bands follow.
- **Never run a performance cycle without calibration.** Uncalibrated reviews mean the best-reviewed employees are those with the most lenient managers, not the best performers. Calibration sessions are mandatory, not optional.
- **Never treat compliance as paperwork.** I-9 errors, missed FLSA reclassifications, and state labor law violations are not administrative annoyances — they're legal liabilities. Every compliance item has a deadline and an owner.
- **Admit what you don't know.** State labor laws change. If you don't have current NY/CA/WA/CO-specific requirements, say so and direct to the state DOL website.

## When to Use
<!-- QUICK: 30s — scan the bullet list to decide if this skill fits -->

- Designing a new-hire onboarding program with 0-30-60-90 day milestones, buddy assignments, and manager check-in cadence
- Building or revising compensation bands with market data, geo-differentials, and equity refresh guidelines
- Running a performance review cycle: 360 feedback collection, calibration sessions, 9-box talent mapping, comp adjustments
- Creating a leveling framework with career ladders for IC and management tracks, including promotion criteria and terminal levels
- Deploying an employee engagement survey (eNPS, pulse) and building action plans from results
- Conducting retention risk analysis on high-performers and designing retention interventions
- Setting up internal mobility programs: job boards, rotation programs, transfer policies
- Managing offboarding: exit interviews, knowledge transfer, system access revocation, COBRA, final pay compliance
- Implementing or migrating an HRIS (Rippling, BambooHR, Workday) with data migration and workflow configuration

## Decision Trees

### Performance Review Cadence
<!-- QUICK: 30s -->

```
                     ┌──────────────────────────────┐
                     │ START: Performance review       │
                     │ cadence?                       │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Company growing fast (>30%      │
                    │ headcount YoY) OR roles          │
                    │ changing rapidly?                │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────────┐    ┌──────▼──────────────────┐
                    │ Semi-annual   │    │ Is compensation tightly   │
                    │ reviews +     │    │ coupled to performance    │
                    │ quarterly     │    │ (bonus, equity refreshes  │
                    │ check-ins.    │    │ tied to rating)?          │
                    │ Cycle: Jan +  │    └──┬──────────────────┬────┘
                    │ July reviews, │       │YES               │NO
                    │ April + Oct   │  ┌────▼──────────┐ ┌────▼──────────┐
                    │ check-ins     │  │ Annual formal  │ │ Continuous    │
                    └───────────────┘  │ review +       │ │ feedback +    │
                                       │ mid-year       │ │ annual        │
                                       │ check-in.      │ │ summary.      │
                                       │ Cycle: Jan     │ │ Lightweight,  │
                                       │ review, July   │ │ no ratings.   │
                                       │ check-in       │ │ Culture of    │
                                       └────────────────┘ │ coaching.     │
                                                          └───────────────┘
```
**When semi-annual:** Rapid growth, role fluidity, frequent reorgs — people need formal feedback twice/year to calibrate expectations as the company changes. Cost: 2-3 weeks of manager time per cycle.
**When annual + mid-year:** Stable organization, clear roles, comp tied to reviews — one deep review/year for comp decisions, one light check-in for course correction.
**When continuous feedback:** Mature coaching culture, comp decoupled from ratings — avoid rating-induced gaming. Requires high manager capability.

### Compensation Philosophy: Percentile Anchor Decision
```
                     ┌──────────────────────────────┐
                     │ START: What comp percentile?    │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Cash-constrained startup         │
                    │ (<$5M raised, pre-revenue)?      │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────────┐    ┌──────▼──────────────────┐
                    │ 25-40th       │    │ Competing for talent     │
                    │ percentile    │    │ with FAANG or well-funded │
                    │ cash.         │    │ unicorns?                │
                    │ Compensate    │    └──┬──────────────────┬────┘
                    │ with equity   │       │YES               │NO
                    │ (0.5-3%) +    │  ┌────▼──────────┐ ┌────▼──────────┐
                    │ mission.      │  │ 65-85th       │ │ 50-65th       │
                    │ Target: early │  │ percentile    │ │ percentile    │
                    │ believers,    │  │ total comp.    │ │ total comp.   │
                    │ not mercenaries│ │ Must be in top│ │ Competitive   │
                    └───────────────┘  │ quartile for  │ │ but not       │
                                       │ at least 2 of │ │ premium.      │
                                       │ 3: cash,      │ │ Good for      │
                                       │ equity, scope │ │ stable growth │
                                       └───────────────┘ │ companies.    │
                                                          └───────────────┘
```
**25-40th percentile:** Pre-seed/Seed. Compensate with equity and autonomy. Accept that you'll lose candidates optimizing for cash. The ones who join are in it for the mission.
**65-85th percentile:** Growth stage competing with big tech. Expensive but necessary for critical roles. Apply selectively: staff+ engineers, execs, specialized roles — not every role needs to be at this tier.
**50-65th percentile:** Default for most Series A-C companies. Competitive enough to close, sustainable enough to maintain margins.

### 9-Box Talent Grid — Action Matrix
```
                     ┌──────────────────────────────┐
                     │ START: Where does employee      │
                     │ land on 9-box?                 │
                     └────────────┬─────────────────┘
                                  │
            Potential (Y-axis: Low / Medium / High)
            Performance (X-axis: Low / Medium / High)

    HIGH POTENTIAL    │  1A: "Rough Diamond"   │  2A: "High Potential"   │  3A: "Star"
                      │  Coach up performance. │  Growth assignments.    │  Promote now. Retain
                      │  Tight feedback, clear │  Stretch projects,      │  aggressively. Comp
                      │  PIP if no improvement │  mentorship. Protect    │  at top of band.
                      │  in 2 cycles.          │  from burnout.          │  Succession candidate.
                      │────────────────────────│─────────────────────────│────────────────────────
    MED POTENTIAL     │  1B: "Risk"            │  2B: "Core Performer"   │  3B: "High Performer"
                      │  Performance PIP.      │  Keep engaged. Growth   │  Reward & recognize.
                      │  Assess fit. Consider  │  assignments within     │  Equity refreshers.
                      │  exit if no change in  │  comfort zone. Don't    │  Keep challenged.
                      │  1 cycle.              │  overlook — they're     │  Succession depth.
                      │                        │  your steady state.     │
                      │────────────────────────│─────────────────────────│────────────────────────
    LOW POTENTIAL     │  1C: "Mismatch"        │  2C: "Solid/Plateaued"  │  3C: "Expert"
                      │  Exit. Don't delay.    │  Value in role. Don't   │  Deep expertise.
                      │  Cost of keeping >     │  push for promotion —   │  Keep as IC anchor.
                      │  cost of replacing.    │  they're content.       │  Recognition without
                      │  Severance + dignity.  │  Risk: key person       │  promotion pressure.
                      │                        │  dependency if niche.   │
                      └────────────────────────┴─────────────────────────┴────────────────────────
```
**Decision principle:** Box 1C = exit within 30 days. Box 3A = promote within 6 months or lose them. Box 2B = your largest population; invest in engagement, not promotion pressure. Box 3C = celebrate — not everyone needs to be on a management track.

## Core Workflow
<!-- QUICK: 30s — scan phase titles to understand the process -->

### Phase 1 (~60 min): Onboarding Program Design
<!-- STANDARD: 3min -->

1. **Pre-boarding (offer signed to day 0)** — Send welcome email within 24 hours: manager intro, day-1 logistics, laptop shipped, accounts pre-provisioned (email, Slack, GitHub, HRIS). Assign buddy from different team. Share team org chart + reading list.
2. **Week 1: Orientation & Context** — Day 1: IT setup (2 hrs max), manager 1:1 (role expectations + 30-day goals), team lunch. Days 2-5: Product deep-dives, customer shadowing, codebase walkthrough. End of week 1: "What's one thing that's different than you expected?" check-in.
3. **Day 30: First Milestone Check** — Manager + new hire review 30-day goals. New hire ships at least one thing to production (engineers), completes first customer call (sales), publishes first doc (PM). Buddy check-in: "Anything you're hesitant to ask your manager?"
4. **Day 60: Deepening Integration** — New hire owns a small project end-to-end. Manager reviews contribution quality. Peer feedback collected from 2-3 teammates. Adjust role expectations based on observed strengths.
5. **Day 90: Full Ramp Assessment** — Formal review: manager rates productivity (1-5), cultural contribution, autonomy. Decision: confirmed (meets bar), extended ramp (needs 30 more days), or not a fit (exit). Buddy graduates. New hire completes onboarding NPS survey.

<!-- DEEP: 10+min — Onboarding failure pattern -->
> **War Story:** A 50-person startup had no structured onboarding. New engineers got a laptop and a "figure it out" Slack message. 90-day voluntary attrition was 22%. Root cause: new hires felt unwelcome and unproductive. Fix: Implemented 30-60-90 day plan with assigned buddy, pre-provisioned dev environments, and weekly manager 1:1s for first month. 90-day attrition dropped to 5% within 2 quarters. Cost of fix: ~10 hours of manager time per new hire. Cost of not fixing: $50K+ per lost hire (recruiting + ramp + lost productivity).

### Phase 2 (~45 min): Compensation Philosophy & Band Design
<!-- STANDARD: 3min -->

1. **Philosophy Statement** — Write in 3 sentences: (a) What percentile we target and why (cash + equity + total), (b) How we handle geo-differentials (national, tiered, or location-agnostic), (c) Our refresh philosophy (when, how much, performance-linked or tenure-linked).
2. **Market Data** — Pull Pave/Radford/Levels.fyi data for your stage, industry, and locations. For each level: 25th, 50th, 75th percentile for base + equity + bonus. Update quarterly — comp data >6 months old is stale.
3. **Band Construction** — For each level: min (80% of midpoint), midpoint (target percentile), max (120% of midpoint). Bands should overlap ~20% with adjacent levels to allow for tenured individual contributors above new managers.
4. **Geo-Differential Model** — Choose one: (a) National pay + location adjustment (most common), (b) Tier-based: Tier 1 (SF/NYC = 100%), Tier 2 (LA/Seattle/Boston = 90-95%), Tier 3 (rest of US = 80-85%), (c) Location-agnostic (same pay everywhere — Buffer, GitLab model). Document rationale.
5. **Equity Refresh Program** — Annual refresh grants starting year 2. Refresh size: 25-50% of new-hire grant for same level, adjusted by performance (Exceeds = 1.5x, Meets = 1.0x, Below = 0.5x or 0). Refresh vesting starts immediately (not another cliff). Avoid the "4-year retention cliff" where equity runs out and employees walk.

### Phase 3 (~45 min): Performance Review Cycles
<!-- STANDARD: 3min -->

1. **Self-Review** — Employee writes: accomplishments vs goals, strengths leveraged, areas for growth, career aspirations. Template limits: 500 words max. Due 1 week before manager review.
2. **Manager Review** — Manager rates on: performance (what was delivered), behaviors (how it was delivered), values alignment. Rating scale: Does Not Meet / Meets / Exceeds / Exceptional. Write narratives, not just scores. Address: "What should this person start/stop/continue?"
3. **360 Feedback (optional for mid-level, required for senior+)** — 3-5 peers, 1-2 cross-functional partners, 1-2 direct reports (if manager). Anonymous unless employee opts in. Questions: strengths, growth areas, one thing they should do differently. Manager synthesizes themes, not raw quotes.
4. **Calibration Session** — All managers in a function meet. Review distribution: typically 5-10% Exceptional, 15-20% Exceeds, 60-70% Meets, 5-10% Does Not Meet. Force-rank only if distribution is skewed (e.g., 40% Exceeds — indicates leniency, not performance). Calibrate by asking: "Who would you fight to keep? Who would you accept resigning?"
5. **Review Delivery** — Manager delivers review in person (or video). Start with appreciation. Deliver rating clearly — no hedging. Discuss comp implications transparently. Co-create development plan for next cycle. Document in HRIS within 48 hours.

### Phase 4 (~40 min): Leveling Frameworks & Career Ladders
<!-- STANDARD: 3min -->

1. **Dual-Track System** — IC track and Management track, parallel levels. IC levels: Associate → Engineer → Senior → Staff → Senior Staff → Principal → Distinguished. Management: Manager → Senior Manager → Director → Senior Director → VP → SVP → C-level. Tracks are bridges, not one-way streets — managers can return to IC.
2. **Level Definitions** — Each level defined by: scope (team/org/company impact), autonomy (needs direction / self-directed / directs others / directs strategy), craft depth (learning / proficient / expert / defines industry practice), and leadership (mentors individuals / leads teams / leads org / leads company).
3. **Promotion Criteria** — Promote when someone is already operating at the next level for 6+ months, not when you hope they'll grow into it. Evidence: project outcomes at next-level scope, peer feedback confirming next-level behaviors, manager narrative. No promotion based on tenure or "it's their turn."
4. **Terminal Levels** — Define which levels are "terminal" (acceptable to stay indefinitely with good performance). Typically: Senior Engineer (IC), Senior Manager (Mgmt). Beyond these requires sustained impact at that scope; not everyone wants or needs to get to Staff/Director.

<!-- DEEP: 10+min — Leveling failure mode -->
> **Failure Pattern:** A 200-person company promoted based on manager advocacy alone — no written criteria, no calibration. Result: title inflation (40% "Senior" engineers, 15% "Staff" when only 3 actually operated at that level), internal inequity (two people at same title with 2x comp difference), and external credibility loss (candidates from other companies declined because "Senior" at this company meant mid-level elsewhere). Fix: Written level definitions with behavioral anchors, promotion packets reviewed by cross-functional panel, calibration across all functions quarterly.

### Phase 5 (~35 min): Employee Engagement & Retention
<!-- STANDARD: 3min -->

1. **eNPS Survey (quarterly)** — Single question: "How likely are you to recommend [Company] as a great place to work? (0-10)." Promoters (9-10), Passives (7-8), Detractors (0-6). Target: eNPS >30. Below 0 = crisis.
2. **Pulse Surveys (monthly, 5 questions max)** — Rotate themes: belonging, manager quality, growth opportunities, workload sustainability, confidence in leadership. Use a 1-5 Likert scale. Track trends, not point-in-time scores.
3. **Retention Risk Scoring** — Score every employee quarterly on: comp competitiveness (are they in bottom quartile of band?), time since last promotion (>18 months?), manager quality (low eNPS for their team?), external market heat (is their role in high demand?), flight risk signals (LinkedIn activity increase, PTO pattern changes). High-risk employees get proactive retention conversation within 2 weeks.
4. **Stay Interviews** — 30-minute conversation with high-performers (top 20%) every 6 months. Ask: "What would make you leave? What keeps you here? What would make this your last job?" Act on feedback within 30 days or explain why not.

### Phase 6 (~30 min): Offboarding & Compliance
<!-- STANDARD: 3min -->

1. **Exit Interview** — Conducted by People Ops (not the employee's manager) within the employee's last week. Structured questions: reason for leaving (pull vs push factors), manager effectiveness (1-5), would they return?, what would they change?, who else is at risk of leaving? Anonymize themes for leadership; share raw data only with CPO.
2. **Knowledge Transfer** — Document: active projects + status, key contacts for each, access credentials handoff, recurring responsibilities. 2-week transition plan for voluntary departures, immediate for involuntary.
3. **System Offboarding Checklist** — Revoke access within 4 hours of departure: email, Slack, GitHub, HRIS, AWS, all SaaS tools. Forward email to manager. Transfer document ownership. Remove from all distribution lists.
4. **Compliance Requirements** — Final paycheck: CA = immediate on termination day, most states = next regular payday. COBRA notification within 14 days. I-9 retention: 3 years after hire or 1 year after termination, whichever is later. Unemployment claim response within state deadline (typically 7-10 days). FLSA exemption audit: confirm exempt/non-exempt classification is still correct (salary threshold updates regularly).

## Best Practices
<!-- STANDARD: 3min — rules extracted from production people ops experience -->

1. **Onboarding buddies are not optional.** A new hire with a buddy reaches full productivity 2x faster and rates onboarding 1.5 points higher. Buddy must be from a different team (cross-functional context), trained (1-hour session on what to do/not do), and recognized (small bonus or public thank-you).
2. **Comp bands live in a shared document, not in your head.** Transparency is a spectrum: publish bands internally (Buffer model: everyone can see everyone's salary) or keep them manager-visible only. Either way, they must be WRITTEN DOWN. Verbal comp philosophy doesn't survive a single departure.
3. **Calibration sessions are about the distribution, not the individual.** A manager arguing "but my report is exceptional!" for 50% of their team has a calibration problem, not exceptional reports. The session fixes the standard, not the person.
4. **Performance ratings without comp impact are theatre.** If ratings don't affect bonus, equity refresh, or base adjustment, don't bother with ratings. Use narrative-only feedback. Ratings exist to differentiate compensation — if you won't differentiate, don't rate.
5. **Geo-differential models must survive one senior hire in a low-cost city.** If your NYC-based VP moves to Boise and you cut their pay, they leave. If you don't cut their pay, your geo model is broken. Decide up front: do you adjust comp on relocation? If not, your model is location-agnostic — embrace it fully.
6. **Employee surveys without visible action destroy trust.** If you ask "How's your workload?" for 3 quarters and the score stays at 2.8/5 with no change, employees stop responding. Publicize survey results within 2 weeks. Commit to 1-2 action items. Report back on progress next cycle.
7. **Exit interview themes are a lagging indicator.** By the time someone is in an exit interview, they've been considering leaving for 3-6 months. The real signal is in stay interviews, pulse surveys, and manager 1:1s. Fix exit interview themes by addressing them while people are still employed.
8. **HRIS implementation fails when you replicate bad processes.** Don't automate a broken performance review form in Workday. Fix the process first, then implement the system. HRIS migration is a process redesign project that happens to involve software.
9. **I-9 compliance errors are the most common and most preventable HR liability.** Penalties: $250-$2,700 per form. Most common errors: Section 1 not completed by day 1, Section 2 not completed within 3 business days, acceptable documents not examined in person (remote I-9 requires authorized representative). E-Verify if required by state or federal contracts.
10. **Internal mobility is the cheapest and fastest source of hire.** Internal candidates ramp 50% faster, have 30% higher retention at 12 months, and cost $0 in recruiting fees. Require: 12 months in current role before transfer eligibility, manager notification before application (not permission — notification), transparent internal job board.

## Token-Efficient Workflow

```
# Step 1: Generate comp band
python3 scripts/build_comp_band.py --level L5 --geo "SF Bay Area" --stage "Series B" \\
  --percentile 65 --output json
# Returns: {"level":"L5","base":{"min":185000,"mid":215000,"max":258000},...}

# Step 2: Onboarding checklist for new hire start date
python3 scripts/onboarding_checklist.py --employee-id 42 --start-date 2026-08-01 \\
  --hris rippling --output markdown
# Returns: 0-30-60-90 day task list with owners

# Step 3: Performance calibration distribution check
python3 scripts/calibration_audit.py --cycle 2026H1 --department engineering --output json
# Returns: {"ratings_distribution":{...},"skew_detected":true,"affected_managers":["alice","bob"]}

# Step 4: Retention risk scan
python3 scripts/retention_risk.py --high-performers-only --output json
# Returns: [{"employee":"jane","risk_score":78,"reasons":["18mo_since_promo","bottom_quartile_comp"]},...]
```

## Cross-Skill Coordination
<!-- QUICK: 30s — table of who to talk to when -->

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **Recruiting** | New hire starts, onboarding feedback loops, comp band misalignment with market | Signed offer details, candidate experience feedback from new hires, comp bands that are losing candidates. **Decision gate:** Is offer acceptance rate > 60%? → comp bands competitive. **Artifact:** offer acceptance rate dashboard + candidate experience NPS. |
| **HR Manager** | Performance cycles, PIP status, retention risks, org design changes, compliance program rollouts | Cycle timelines, calibration results, high-risk retention flags, FLSA audit findings. **Decision gate:** Are calibration sessions completed before comp decisions? → fair process. **Artifact:** calibration session summary + promotion approval list. |
| **Legal Advisor** | Offer letter updates, employment law changes, compliance audit findings, offboarding terminations | Policy language review, state law change alerts, I-9 audit results, separation agreement templates |
| **CEO Strategist** | Comp philosophy approval, workforce planning input, engagement survey results, culture program ROI | Annual comp review packet, eNPS trends, retention analytics, program budget requests |
| **Finance (Corporate Finance)** | Comp band cost modeling, headcount budget vs actual, benefits cost projections | Band impact analysis, headcount reconciliation, benefits renewal data |
| **Engineering Manager** | Team-level onboarding, performance review participation, retention risks, leveling decisions | Team structure context, skill gap analysis, promotion readiness assessments. **Decision gate:** Is manager-to-IC ratio within target range? → team scalable. **Artifact:** team health dashboard + promotion pipeline. |

### Cross-Skill Integration Chains
<!-- STANDARD: 3min — actual command sequences these skills execute together -->

**Chain 1: New hire signed → Fully ramped employee**
```
recruiting (signed offer + start date)
  → people-ops (pre-boarding: laptop + accounts + buddy assignment)
    → people-ops (30-60-90 day onboarding program)
      → hr-manager (productivity assessment at 90 days)
        → ceo-strategist (workforce capacity update)
```

**Chain 2: Performance cycle execution → Comp adjustments**
```
people-ops (review cycle launch + calibration sessions)
  → hr-manager (talent review + PIP decisions + promotion approvals)
    → people-ops (comp adjustments within bands + equity refreshers)
      → ceo-strategist (budget impact summary)
```

**Chain 3: Retention risk detected → Intervention deployed**
```
people-ops (retention_risk.py scan → high-risk employees flagged)
  → hr-manager (retention conversation strategy + comp flex approval)
    → ceo-strategist (above-band exception if needed for critical talent)
      → people-ops (retention offer delivered within 2 weeks)
```

**Chain 4: Compliance audit → Corrective action**
```
people-ops (I-9/FLSA self-audit findings)
  → legal-advisor (compliance gap assessment + correction guidance)
    → hr-manager (policy update + manager retraining)
      → people-ops (process fix implemented + re-audit scheduled)
```

**Chain 5: Engagement survey results → Culture program**
```
people-ops (eNPS survey + thematic analysis)
  → hr-manager (action plan development + manager coaching priorities)
    → ceo-strategist (culture investment decisions)
      → people-ops (program rollout + progress tracking)
```

### Escalation Path

| Situation | Escalate To | Rationale |
|-----------|------------|-----------|
| Comp bands causing >15% offer declines due to market | HR Manager + CEO Strategist | Philosophy vs market misalignment; strategic decision required |
| eNPS drops below 0 for 2 consecutive quarters | HR Manager + CEO Strategist | Cultural crisis; leadership intervention required |
| FLSA exemption audit reveals misclassified employees | Legal Advisor + HR Manager | Legal liability with back-pay exposure; immediate correction required |
| Calibration reveals systemic bias (e.g., underrepresented groups rated lower across all managers) | HR Manager + Legal Advisor | Potential discrimination pattern; external audit may be needed |
| HRIS data migration reveals data integrity issues (missing I-9s, incorrect comp) | HR Manager + Legal Advisor | Compliance risk; may require self-audit and correction filings |

## Scale Depth

### Solo (1-10 employees)
No dedicated People Ops. Founder handles HR. Onboarding: laptop + 3 coffee meetings + 1 doc listing team members. No formal review cycles — continuous feedback. Comp: founder decides per person, no bands. Compliance: Gusto/Zenefits handles payroll, I-9, benefits. **Overkill:** HRIS, formal leveling, engagement surveys (just ask), 360 reviews.

### Small (10-50 employees)
First People Ops hire (part-time or combined with Office Manager/EA role). HRIS: Rippling or BambooHR. Onboarding: documented checklist with buddy program. Performance: lightweight annual reviews, no ratings. Comp: informal bands (manager discretion within ranges). Compliance: payroll provider + periodic legal review. **Overkill:** calibration sessions, 9-box, geo-differential calculators, full Workday.

### Medium (50-200 employees)
Dedicated People Ops team (2-4). HRIS: Rippling/BambooHR/Workday depending on complexity. Full programs: semi-annual reviews with calibration, formal comp bands with geo-differentials, engagement surveys (quarterly eNPS), career ladders published. Onboarding: 0-30-60-90 day program with dedicated onboarding specialist. Compliance: internal audit quarterly. **Overkill:** Workday (unless >200), dedicated internal mobility team, 360 feedback for all levels.

### Enterprise (200+ employees)
Dedicated People Ops team (5+). HRIS: Workday. Specialized: total rewards, people analytics, L&D, DEI, internal mobility. Full programs: continuous performance management, talent reviews, succession planning, workforce analytics. Compliance: dedicated employment counsel + external audit annually. Global mobility function for international employees. **When to scale:** Compliance complexity from new states/countries, >200 employees needing structured career development, or board-level people metrics requirements.

## Error Decoder

| Problem | Root Cause | Fix |
|---------|------------|-----|
| Onboarding NPS <30 | No structure, no buddy, no 30-day check-in | Implement buddy program. Ship laptop + accounts before day 1. Manager 30/60/90 day check-ins with written goals. Measure NPS at day 90. |
| Performance ratings inflated (40%+ "Exceeds") | No calibration; "leniency bias" where managers rate to avoid difficult conversations | Implement calibration sessions. Force distribution targets (5-10% Exceptional). Train managers on giving honest feedback. Review ratings by manager — flag outliers. |
| High-performers leaving for 15-20% raises elsewhere | Comp bands stale or below market. No equity refresh program. | Re-benchmark against Pave/Levels.fyi quarterly. Implement annual equity refreshers. Proactive retention conversations for top 20% with comp adjustments. |
| Engagement survey participation <50% | Employees don't trust anonymity or don't believe action will be taken | Use third-party survey tool with anonymity guarantee (CultureAmp, Lattice). Share results transparently within 2 weeks. Commit to specific action items and report progress. |
| I-9 audit reveals missing/incorrect forms | No I-9 process owner, forms completed by hiring managers without training | Assign I-9 ownership to People Ops. E-Verify within 3 business days of hire. Quarterly self-audit on random sample of 10% of I-9s. Use electronic I-9 system (Equifax, LawLogix). |
| Career ladder exists but no one uses it for promotions | Ladder is aspirational, not operational. No measurable criteria per level. | Add behavioral anchors to each level (e.g., "Staff Engineer: Led architecture for system serving 1M+ users"). Require promotion packets with evidence against level criteria. Review by cross-functional panel. |

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
<!-- QUICK: 30s — binary pass/fail items. All must pass. -->

- [ ] **[P1]** Onboarding program documented: 0-30-60-90 day milestones, buddy assignment, manager check-in cadence
- [ ] **[P2]** Compensation philosophy written and approved: percentile targets, geo-differential model, equity refresh policy
- [ ] **[P3]** Comp bands built for all levels with min/mid/max, benchmarked against market data <6 months old
- [ ] **[P4]** Performance review cycle defined: cadence, rating scale, self-review + manager review + calibration process
- [ ] **[P5]** Calibration sessions scheduled for every review cycle with distribution targets and manager training
- [ ] **[P6]** Leveling framework published: IC and management tracks, level definitions with behavioral anchors, promotion criteria
- [ ] **[P7]** Engagement survey cadence set (eNPS quarterly, pulse monthly) with results-sharing commitment (<2 weeks)
- [ ] **[P8]** Retention risk scoring model active: comp, promotion recency, manager quality, market heat for top 20%
- [ ] **[P9]** Internal mobility policy documented: eligibility (12 months in role), notification process, internal job board
- [ ] **[P10]** Offboarding checklist documented: exit interview, knowledge transfer, system access revocation (4-hour SLA)
- [ ] **[P11]** I-9 compliance: process owner assigned, E-Verify within 3 days of hire, quarterly self-audit
- [ ] **[P12]** FLSA classification audit completed: all employees correctly classified exempt/non-exempt with current salary thresholds
- [ ] **[P13]** HRIS configured with all workflows: onboarding, offboarding, performance, comp changes, time-off
- [ ] **[P14]** State-specific labor law compliance verified: CA (final paycheck timing, meal breaks, PTO payout), NY (wage theft prevention), CO (pay transparency in JDs), WA (salary threshold)
- [ ] **[P15]** COBRA administration process documented: notification within 14 days, carrier enrollment window tracked

## What Good Looks Like

A new hire receives a shipped laptop, fully-provisioned accounts, and a welcome email before day 1. Their buddy reaches out within the first week. At 90 days, their manager rates their productivity at 4+/5 and the new hire rates onboarding NPS >8. Comp bands are visible to managers, updated quarterly against market data, and every employee's comp falls within their band. Performance reviews happen on schedule with calibration distributions within targets. eNPS stays above 30. No high-performer leaves because of comp or lack of growth — they're identified and retained proactively. Offboarding is smooth: knowledge transferred, access revoked within hours, exit interview completed, final pay compliant.

## References
<!-- QUICK: 30s — links to deeper reading and files -->

- [Pave — Real-time compensation benchmarking](https://www.pave.com/)
- [Levels.fyi — Tech compensation data](https://www.levels.fyi/)
- [Rippling — HRIS for small/medium companies](https://www.rippling.com/)
- [BambooHR — HRIS for SMB](https://www.bamboohr.com/)
- [Workday — Enterprise HRIS](https://www.workday.com/)
- [Culture Amp — Employee engagement platform](https://www.cultureamp.com/)
- [Lattice — Performance management platform](https://lattice.com/)
- [USCIS I-9 Central](https://www.uscis.gov/i-9-central)
- [DOL FLSA Overtime Rules](https://www.dol.gov/agencies/whd/overtime)
- [references/onboarding-checklist-template.md](./references/onboarding-checklist-template.md) — 0-30-60-90 day task checklist with owner assignments
- [references/comp-philosophy-template.md](./references/comp-philosophy-template.md) — Compensation philosophy statement template with example
- [references/performance-review-template.md](./references/performance-review-template.md) — Manager review template with rating anchors and narrative prompts
- [references/career-ladder-template.md](./references/career-ladder-template.md) — IC + management track level definitions with behavioral anchors
- [references/exit-interview-template.md](./references/exit-interview-template.md) — Structured exit interview questionnaire
- [assets/9-box-placement-canvas.md](./assets/9-box-placement-canvas.md) — Talent review calibration canvas with action matrix
- [assets/offboarding-checklist.csv](./assets/offboarding-checklist.csv) — Offboarding task tracker with SLA timelines
