# Core Workflow — Full Implementation

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
