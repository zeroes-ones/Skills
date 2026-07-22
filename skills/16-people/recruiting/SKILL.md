---
name: recruiting
description: "Technical & executive recruiting: job description writing (outcomes-based), sourcing (Boolean, GitHub, LinkedIn Recruiter, referrals), structured interview design (rubric scoring, panel calibration), offer construction & negotiation (equity: ISO/NSO/RSU, 409A, cliff vs graded vesting), closing strategies, recruiting metrics, employer branding, diversity sourcing. Use when hiring technical or executive roles, building a recruiting function, or optimizing hiring throughput."
author: Sandeep Kumar Penchala
type: people
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - recruiting
  - talent-acquisition
  - technical-hiring
  - executive-recruiting
token_budget: 3500
output:
  type: "markdown"
  path_hint: "./"
chain:
  consumes_from:
    - ceo-strategist
    - hr-manager
  feeds_into:
    - people-ops
    - hr-manager
---

# Technical & Executive Recruiting

End-to-end hiring system for technical and executive roles. From job description through close — every stage is measured, every decision is structured, every candidate interaction is intentional.

## Route the Request
<!-- QUICK: 30s — pick your path, skip the rest -->

What are you trying to do?
├── Write a job description → Start at "Phase 1: Role Definition & JD Writing"
├── Source candidates for a hard-to-fill role → Jump to "Sourcing Strategy & Boolean Search"
├── Design a structured interview loop → Go to "Phase 2: Interview Loop Design"
├── Build an offer / negotiate comp → Jump to "Phase 4: Offer Construction & Negotiation"
├── Close a candidate who has competing offers → Go to "Closing Strategies" under Best Practices
├── Set up recruiting metrics/dashboard → Jump to "Phase 5: Metrics & Optimization"
├── Fix diversity pipeline → Go to "Diversity Sourcing" under Best Practices
└── Don't know where to start? → Start at "Phase 1: Role Definition & JD Writing"

**Do not read the entire skill.** Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces.

- **Never write a JD without outcomes.** A JD that lists "5+ years of React" is a filtering tool, not an attraction tool. Describe what the person will accomplish in their first 6 months. "You'll own the migration from REST to GraphQL, reducing API response times from 400ms to <100ms p95" — that's a hiring magnet.
- **Never make an offer without a band.** Every offer must be benchmarked against market data (Pave/Radford/OptionImpact for equity, Levels.fyi/Carta for cash). No number leaves this skill without a percentile anchor: "This offer is at 65th percentile for Series B companies in the Bay Area."
- **Never present equity without explaining it.** ISO/NSO/RSU, strike price vs 409A vs preferred price, cliff vs graded vesting, early exercise + 83(b), post-termination exercise window. If the candidate doesn't understand what they're getting, the offer isn't complete.
- **Never skip the closing plan.** The offer letter is the *beginning* of closing, not the end. Every candidate with competing offers needs a written closing strategy before the offer goes out.
- **Admit what you don't know.** If you don't have current market comp data for a geo/role/stage combination, say so and tell the recruiter where to find it.

## When to Use
<!-- QUICK: 30s — scan the bullet list to decide if this skill fits -->

- Hiring a technical role (engineer, data scientist, PM, designer) where structured interviewing is critical
- Building an executive search for VP/C-suite roles requiring backchannel references and board alignment
- Redesigning an interview loop because your offer acceptance rate is below 70% or quality-of-hire feedback at 6 months is poor
- Writing job descriptions that attract passive candidates, not filter active applicants
- Constructing an offer with equity components (ISO, NSO, RSU) and negotiating against competing offers
- Setting up recruiting metrics: time-to-fill, offer acceptance rate, source-of-hire, quality-of-hire
- Improving diversity pipeline when underrepresented candidate throughput is below 30% at top-of-funnel
- Choosing or migrating an ATS (Greenhouse, Lever, Ashby) and designing the workflow
- Running a recruiting sprint for a critical hire (target: offer accepted within 21 days)

## Decision Trees

### Sourcing Channel Selection
<!-- QUICK: 30s — where to find this candidate type -->

```
                     ┌──────────────────────────────┐
                     │ START: Which sourcing channel?  │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Role is highly specialized       │
                    │ (staff+ engineer, exec, niche)?   │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────────┐    ┌──────▼──────────────────┐
                    │ Outbound       │    │ Is the role early-career │
                    │ sourcing       │    │ or high-volume (SDR,     │
                    │ required.      │    │ support, junior eng)?    │
                    │ Use: LinkedIn  │    └──┬──────────────────┬────┘
                    │ Recruiter +    │       │YES               │NO
                    │ GitHub +       │  ┌────▼──────────┐ ┌────▼──────────┐
                    │ employee refs  │  │ Inbound +     │ │ Mixed: inbound │
                    │ + boolean      │  │ university    │ │ + outbound.    │
                    │ search         │  │ recruiting +  │ │ LinkedIn +     │
                    └────────────────┘  │ job boards    │ │ well-written JD│
                                        │ (LinkedIn,    │ │ + employee refs│
                                        │ Indeed,       │ └────────────────┘
                                        │ Handshake)    │
                                        └───────────────┘
```
**When outbound sourcing is mandatory:** Staff+ engineers, executives, niche roles (e.g., Rust kernel engineer, quant researcher). Inbound alone won't fill these — you must map the market and reach out directly.
**When inbound works:** Junior/mid-level roles with clear JD, strong employer brand, and compensation in market range. Expect 200-500 inbound applicants for a mid-level engineering role in a known company.

### Interview Loop Design: Deep vs Broad
```
                     ┌──────────────────────────────┐
                     │ START: Interview loop design?   │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Role requires one primary skill  │
                    │ deeply (e.g., backend eng =      │
                    │ system design + coding)?         │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────────┐    ┌──────▼──────────────────┐
                    │ 4-5 rounds:   │    │ Role spans multiple      │
                    │ 2 coding,     │    │ domains (e.g., EM =      │
                    │ 1 system      │    │ people mgmt + tech +     │
                    │ design, 1     │    │ product + execution)?    │
                    │ behavioral,   │    └──┬──────────────────┬────┘
                    │ 1 values.     │       │YES               │NO
                    │ ~4 hours total│  ┌────▼──────────┐ ┌────▼──────────┐
                    └────────────────┘ │6 rounds:      │ │3-4 rounds:    │
                                       │2 behavioral   │ │1 combo screen │
                                       │(IC+manager),  │ │+ 2 domain +   │
                                       │1 technical,   │ │1 values.      │
                                       │1 system,      │ │Add take-home  │
                                       │1 cross-func,  │ │if portfolio   │
                                       │1 values/exec  │ │review needed. │
                                       │presentation.  │ └───────────────┘
                                       │~6 hours total │
                                       └───────────────┘
```
**When deep loop:** Individual contributor roles where one skill dominates. Fewer rounds, higher signal per round. Each interviewer owns one dimension.
**When broad loop:** Cross-functional roles (EM, PM, TPM, exec). More rounds covering distinct dimensions. Panel debrief required to synthesize signals.

### Offer Approval Authority
```
                     ┌──────────────────────────────┐
                     │ START: Offer above band?        │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Offer is within band AND         │
                    │ within 2% of median?             │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────────┐    ┌──────▼──────────────────┐
                    │ Hiring        │    │ Is it >10% above band    │
                    │ manager       │    │ OR >90th percentile      │
                    │ approves.     │    │ total comp?              │
                    │ (no escalation│    └──┬──────────────────┬────┘
                    │ needed)       │       │YES               │NO (2-10% above)
                    └───────────────┘  ┌────▼──────────┐ ┌────▼──────────┐
                                       │VP People +    │ │Head of People │
                                       │CEO/COO        │ │+ Hiring Mgr   │
                                       │approval       │ │approval.      │
                                       │required.      │ │Document       │
                                       │Business case  │ │compelling     │
                                       │required: why  │ │reason.        │
                                       │this candidate │ └───────────────┘
                                       │at this price  │
                                       └───────────────┘
```
**Within band (<2% above median):** Auto-approved. Speed matters — every day of approval delay increases drop-off risk by 3-5%.
**Slightly above band (2-10%):** HM + Head of People approve. Document: competing offers, specialized skill scarcity, time-to-fill cost if role remains open.
**Significantly above band (>10%):** VP People + CEO/COO. Requires business case with ROI justification (e.g., "This hire unblocks $2M ARR pipeline").

## Core Workflow
<!-- QUICK: 30s — scan phase titles to understand the process -->

### Phase 1 (~60 min): Role Definition & JD Writing
<!-- STANDARD: 3min -->

1. **Outcome Mapping** — For each role, define 3 outcomes the hire must achieve in months 1-3, 4-6, and 7-12. Example: "Month 1-3: Ship auth service rewrite reducing login latency from 800ms to <200ms p95. Month 4-6: Design and implement rate-limiting layer handling 50K RPS."
2. **JD Structure** — Title + One-sentence mission + 6-month outcomes (3 bullets) + Why this company/team now + Nice-to-have (NOT requirements — only 3 "must-have" hard skills max) + Comp range (transparent by law in CA/CO/NY/WA). No laundry list of "5+ years X, 3+ years Y."
3. **Comp Band** — Benchmark against Pave/Radford/Levels.fyi for the role, stage, and geo. Define: base range, equity range (with 409A context), target bonus %. Document the percentile anchor.
4. **Scorecard** — Define 4-6 attributes weighted by importance. Each attribute has 3 behavioral indicators (what "great" looks like). Example: "System Design (25%): Designs for 10x scale, clear trade-off articulation, appropriate tech selection."
5. **Verify:** Share JD with 2 team members in the target role. Ask: "Would you apply to this?" If either says no, rewrite.

### Phase 2 (~45 min): Interview Loop Design
<!-- STANDARD: 3min -->

1. **Loop Architecture** — Map attributes from scorecard → interview rounds. Each round tests 1-2 attributes max. No attribute tested by only one interviewer unless it's low-weight.
2. **Interviewer Selection** — Panel of 4-6 interviewers. Each trained on rubric + bias awareness. At least one interviewer from an underrepresented group. No single interviewer should see >60% of candidates (avoid bottleneck).
3. **Rubric Design** — Each attribute scored 1-4: 1=Strong No, 2=No (with reservations), 3=Yes (with reservations), 4=Strong Yes. No 3-point scales (forces false neutrality). Each score anchored to behavioral examples.
4. **Calibration Session** — Before first interview: all panelists review same mock interview recording. Score independently. Discuss variance >1 point. Repeat until scores converge within 0.5 points.
5. **Candidate Experience** — Send prep email 48 hours before: who they'll meet, what each round covers, what to prepare. No surprise rounds. 15-minute buffer between rounds. Same-day debrief scheduling for fast turnaround.

<!-- DEEP: 10+min — War story -->
> **War Story:** A Series B startup's eng loop had 7 rounds over 3 weeks with different interviewers each week. Offer acceptance was 45%. Root cause: candidates accepted elsewhere before loop finished. Fix: Compressed to 4 rounds in 2 days, added a dedicated recruiting coordinator for scheduling, and gave candidates a timeline commitment in the first screen. Acceptance jumped to 78% in 2 months.

### Phase 3 (~90 min): Candidate Sourcing & Outreach
<!-- STANDARD: 3min -->

1. **Sourcing Mix** — For every role, split effort: 40% outbound (LinkedIn Recruiter, GitHub search, Boolean), 30% inbound (JD + careers page), 20% employee referrals (pay $3K-10K depending on role), 10% events/communities.
2. **Boolean Search Strings** — Build reusable search templates by role family:
   - Backend eng: `("staff engineer" OR "principal engineer") AND (Go OR Rust OR Kotlin) AND (Kubernetes OR AWS) AND NOT (intern OR junior OR "new grad") site:linkedin.com/in`
   - ML Engineer: `("machine learning" OR "ML engineer") AND (PyTorch OR TensorFlow) AND (deployed OR production) site:github.com`
3. **GitHub Candidate Search** — Search by: language + stars + recent activity. Contributions to relevant OSS projects. Profile README quality. Avoid: only judging commit count (deep contributors may commit infrequently).
4. **Outreach Message** — Subject: "[Company] — [Role] (saw your work on [specific thing])" Body: One sentence about what they built (proves you researched), one sentence about what they'd build here, comp range, ask for 15 minutes. No "we're revolutionizing..." No "fast-paced environment."

### Phase 4 (~45 min): Offer Construction & Negotiation
<!-- STANDARD: 3min -->

1. **Offer Components** — Base salary ($) + Equity (options/RSUs) + Sign-on (if needed) + Benefits summary + Start date flexibility + Relocation (if applicable).
2. **Equity Deep-Dive** —
   - **ISO** (Incentive Stock Options): Pre-exit startup. Tax-advantaged but $100K exercise limit/year. Candidate must understand AMT implications.
   - **NSO** (Non-Qualified Stock Options): Advisors, contractors, or when ISOs aren't available. Ordinary income tax on spread at exercise.
   - **RSU** (Restricted Stock Units): Public companies or late-stage private. Taxed as income at vest. No purchase needed.
   - **409A valuation:** Strike price for options. If 409A is $2.00 and preferred price is $10.00, the spread per share is $8.00. Candidates care about preferred price relative to strike.
   - **Cliff vs graded:** Standard = 1-year cliff (25% vests), then monthly/quarterly for 3 years. Graded only (no cliff) = trust signal but uncommon.
3. **Offer Letter Structure** — Company letterhead → Role + Start date + Manager → Compensation table (cash + equity + total target) → Equity details (grant size, strike price, vesting schedule, post-termination exercise window) → Benefits summary (1-pager attached) → At-will employment statement → Expiration: 5 business days standard, 3 for competitive situations.
4. **Competing Offer Handling** — Ask: "What matters most to you — cash, equity upside, scope, manager quality, team, mission?" Address top 2. Don't match cash if equity is their driver. Don't break bands for one candidate (creates internal equity problems). Use sign-on bonus as one-time bridge, not base salary inflation.
5. **Closing Call** — Hiring manager calls candidate within 2 hours of offer sent. Says: "We built this offer for you. Here's why each number is what it is. Here's what your first 90 days look like. I'm excited to work with you." No email-only offers.

<!-- DEEP: 10+min — Offer negotiation failure pattern -->
> **Failure Pattern:** Candidate asked for $20K more base. Recruiter said "I'll check" — took 4 days. Candidate accepted competing offer during the wait. Fix: Pre-wire approvals for up to 5% flex above band. Recruiter can say "We can do $10K more now, plus $10K guaranteed bonus at 6 months based on these milestones." Close within 24 hours.

### Phase 5 (~30 min): Recruiting Metrics & Dashboard
<!-- STANDARD: 3min -->

1. **Top-of-Funnel Metrics** — Pipeline volume by source, source-to-screen conversion %, demographic breakdown at each stage.
2. **Throughput Metrics** — Time-to-fill (from JD approval to signed offer), time-in-stage (each stage duration), interviewer utilization (no one doing >4 interviews/week).
3. **Quality Metrics** — Offer acceptance rate (target >80%), quality-of-hire score at 6 months (hiring manager rating 1-5), 12-month retention of new hires, regrettable attrition of hires in first 18 months.
4. **Dashboard Cadence** — Weekly: pipeline health + stuck candidates (>5 days in any stage). Monthly: source effectiveness + acceptance rate trend. Quarterly: quality-of-hire + diversity ratios.

### Phase 6 (~20 min): Employer Branding & Candidate Experience
<!-- STANDARD: 3min -->

1. **Careers Page Audit** — Does it answer: Who will I work with? What will I build? How do you make decisions? What's the comp philosophy? Show team photos (real, not stock). Link to engineering blog posts. Show GitHub org.
2. **Candidate NPS** — Survey every candidate (hired and rejected) post-process: "How likely are you to recommend our interview process to a friend? (0-10)" Target >8 for hires, >6 for final-round rejects.
3. **Rejection Experience** — Rejected after phone screen: personalized email from recruiter. Rejected after onsite: phone call from recruiter + hiring manager within 48 hours of decision. Offer specific feedback if candidate requests it. Rejected candidates are future applicants, referral sources, and customers.

## Best Practices
<!-- STANDARD: 3min — rules extracted from production recruiting experience -->

1. **Outcomes over requirements in JDs.** "5+ years React" → qualified candidate self-selects out because they have 4. "Ship a real-time collaborative editor handling 200 concurrent editors" → qualified candidate thinks "I've done that" and applies. Outcomes attract builders; requirements attract checkbox-fillers.
2. **Panel calibration before every new role.** Without calibration, one interviewer's "Strong Yes" is another's "No with reservations." Run a mock interview with all panelists. Score independently. Discuss until variance <0.5 points. Re-calibrate every 6 months.
3. **No offer without a closing strategy.** Before the offer letter goes out, write: (a) Top 2 things candidate cares about, (b) What competing offers they have, (c) Who will call them and when, (d) What flex you have (cash, equity, scope, title, start date), (e) Your BATNA if they decline.
4. **Employee referrals are 3x more likely to be hired and stay 2x longer.** Pay referral bonuses within 30 days of start (not after 90 days). Publicly celebrate referrals in team channels. Track referral-source quality-of-hire separately.
5. **Diversity sourcing is pipeline engineering, not charity.** Rooney Rule: at least 2 underrepresented candidates interviewed for every role. Blind resume review: strip names + schools before HM review. Source from: /dev/color, Black Girls Code alumni, Lesbians Who Tech, AfroTech, Tapia Conference job boards, HBCU career centers.
6. **Speed is a competitive advantage.** Top candidates are off the market in 10 days. If your loop takes 3+ weeks, you are hiring from the pool of people rejected by faster-moving companies. Target: 14 days from first contact to offer.
7. **Never ghost a candidate.** If someone took time to interview with you, they get a decision — yes or no — within 48 hours of their last interview. Ghosting burns your employer brand. Rejected candidates talk about their experience on Blind/Glassdoor.
8. **Comp bands must be internally equitable.** Two people in the same role, same level, same location, with equivalent performance should have comp within 10% of each other. If a new hire comes in 25% above existing team members, you have a retention time bomb. Fix existing team comp before making above-band offers.
9. **Post-termination exercise window (PTEW) is a dealbreaker for senior hires.** Standard 90-day PTEW means a 4-year employee has 90 days to buy options they spent 4 years earning. Extended PTEW (1-5 years, or 10 years like Quora/Amplitude) is a competitive advantage. If your default is 90 days, expect senior candidates to negotiate this.
10. **Hiring manager does the closing call, not the recruiter.** Candidates join for the manager and the team. The recruiter builds the bridge; the hiring manager seals the deal.

## Token-Efficient Workflow

```
# Step 1: Generate JD with outcomes
python3 scripts/generate_jd.py --role "Staff Backend Engineer" --outcomes outcomes.yaml --output markdown

# Step 2: Score a candidate against scorecard
python3 scripts/score_candidate.py --candidate-id 42 --scorecard role_scorecard.yaml --output json
# Returns: {"overall":3.7,"attributes":[{"name":"System Design","score":4,"weight":0.25},...]}

# Step 3: Generate offer comp
python3 scripts/build_offer.py --role "Staff Engineer" --level L6 --geo "SF Bay Area" \\
  --percentile 65 --equity-type ISO --stage "Series B" --output json
# Returns: {"base":215000,"equity_grant":"50,000 options","strike_price":3.50,...}

# Step 4: Weekly pipeline health
python3 scripts/pipeline_health.py --ats greenhouse --output json
# Returns: {"open_roles":12,"candidates_in_process":87,"stuck_candidates":5,...}
```

## Cross-Skill Coordination
<!-- QUICK: 30s — table of who to talk to when -->

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **CEO Strategist** | Executive hiring, headcount approval, comp above band, hiring plan for new initiatives | Role criticality, budget impact, executive candidate profiles, offer terms needing CEO sign-off |
| **HR Manager** | Headcount planning, comp band design, diversity targets, hiring process changes, recruiting tool procurement | Quarterly hiring plan, band compliance, source-of-hire ratios, pipeline diversity, offer acceptance trends |
| **People Ops** | Onboarding handoff for signed candidates, comp philosophy alignment, employer branding content, referral program administration | Signed offer details, start date, pre-boarding materials, referral payouts, candidate experience survey results |
| **Legal Advisor** | Offer letter templates, equity grant documentation, immigration/visa sponsorship, employment law compliance | Offer letter language, equity plan documents, visa transfer requirements, non-compete enforceability by state |

### Cross-Skill Integration Chains
<!-- STANDARD: 3min — actual command sequences these skills execute together -->

**Chain 1: Strategic hire request → Signed offer**
```
ceo-strategist (headcount approval + role criticality)
  → recruiting (JD writing + sourcing + interview loop)
    → hr-manager (comp band validation)
      → legal-advisor (offer letter review + equity docs)
        → recruiting (closing call + signed offer)
          → people-ops (onboarding handoff)
```

**Chain 2: Pipeline health review → Process optimization**
```
recruiting (pipeline_health.py → stuck candidates + conversion rates)
  → hr-manager (workforce plan reconciliation)
    → ceo-strategist (reprioritize headcount if critical roles blocked)
```

**Chain 3: Diversity sourcing audit → Pipeline improvement**
```
recruiting (demographic funnel report by stage)
  → hr-manager (DEI target assessment)
    → people-ops (employer brand content refresh)
      → recruiting (updated sourcing strategy + new channels)
```

**Chain 4: Offer negotiation deadlock → Resolution**
```
recruiting (competing offer analysis + candidate priorities)
  → hr-manager (comp exception review + internal equity impact)
    → ceo-strategist (above-band approval if required)
      → recruiting (revised offer within 24 hours)
```

### Escalation Path

| Situation | Escalate To | Rationale |
|-----------|------------|-----------|
| Offer requires >10% above band | VP People + CEO/COO | Budget impact; creates internal equity precedent |
| Role unfilled for >60 days with qualified pipeline | HR Manager + Hiring Manager | Process or comp issue; root cause investigation needed |
| Offer acceptance rate drops below 60% for 2+ quarters | HR Manager + Head of People | Systemic issue; comp, process, or brand problem |
| Candidate reports discriminatory interview behavior | HR Manager + Legal Advisor | Legal and brand risk; immediate investigation required |
| Hiring manager consistently overrides panel feedback | HR Manager | Process integrity; panel trust erodes without enforcement |

## Scale Depth

### Solo (1-10 employees)
Founder does all recruiting. No ATS — Lever free tier or Google Sheets pipeline. Outbound sourcing via personal network + LinkedIn. Interview loop: 2-3 rounds (founder screen + technical + values). Comp: mostly equity (0.5-2%), cash below market. Close tactic: mission + ownership. **Overkill:** Greenhouse, dedicated recruiter, exec search firm, formal scorecards, comp bands.

### Small (10-50 employees)
First dedicated recruiter (or founder still leading). ATS: Greenhouse or Ashby. Structured loop: 4-5 rounds with rubrics. Comp: 25-50th percentile cash + meaningful equity. One scorecard per role family. Referral program launched. Basic metrics: time-to-fill, source, acceptance rate. **Overkill:** recruiting ops specialist, employer brand agency, 6+ round loops.

### Medium (50-200 employees)
Recruiting team of 2-5 (1 recruiter per 20-30 hires/year). Sourcing function separate from coordination. Full Greenhouse/Lever implementation. Diversity sourcing targets + reporting. Comp bands formalized at 50th-75th percentile. Dedicated exec recruiter for VP+. Candidate NPS tracked. Greenhouse reports automated to hiring managers. **Overkill:** campus recruiting team (unless high-volume), RPO, global mobility function.

### Enterprise (200+ employees)
Recruiting team of 10+. Specialized: university, exec, technical, G&A, international. Greenhouse/Workday + CRM (Gemini/Entelo). Employer brand team. DEI analytics with demographic funnel reporting at every stage. Comp at 75th+ percentile or above. Relocation + immigration function. Candidate experience surveys with quarterly review. Agency management program. **When to scale:** >30 hires/quarter, >2 geographies, or exec roles requiring retained search.

## Error Decoder

| Problem | Root Cause | Fix |
|---------|------------|-----|
| Offer acceptance rate <60% | Comp below market, slow process, or weak closing strategy | Benchmark comp against Pave/Levels.fyi for stage + geo. Compress loop to <14 days. Pre-wire approval flex. HM calls within 2 hours of offer. |
| Candidates dropping out after onsite | Long decision time or ghosting | Decide within 24 hours of debrief. If yes, HM calls immediately. If no, recruiter calls within 48 hours with feedback. Never leave candidates in limbo. |
| Low-quality inbound applicants | JD lists requirements, not outcomes | Rewrite JD: 3 outcomes for first 6 months. Remove "years of experience" requirements. Add comp range. Add "Why this role exists now" section. |
| Interviewers disagree on scores by >1.5 points | No calibration or vague rubric | Run calibration session before first interview. Each score must have 3 behavioral anchors. Recalibrate monthly until variance <0.5 points. |
| New hire fails within 6 months | Hired for skills, not for attributes that predict success in your environment | Audit scorecard: does it include adaptability, collaboration style, and decision-making approach? Add values-based behavioral round. Reference checks with specific scenario questions. |
| Referral program produces few hires | Bonus too low, payout too slow, or no internal promotion | Raise bonus to $3K-10K based on role. Pay within 30 days of start. Feature referral stories in company meetings. Send quarterly "What we're hiring" digest to all employees. |

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

- [ ] **[R1]** Job description written with 3 measurable 6-month outcomes (not requirements checklist)
- [ ] **[R2]** Comp band benchmarked against Pave/Radford/Levels.fyi for role + stage + geo with percentile anchor documented
- [ ] **[R3]** Scorecard defined: 4-6 weighted attributes with 3 behavioral indicators each. Scoring rubric 1-4 with anchors
- [ ] **[R4]** Interview panel of 4-6 trained interviewers, at least one from underrepresented group
- [ ] **[R5]** Panel calibration session completed: all scores within 0.5 points on mock candidate
- [ ] **[R6]** Candidate prep email template includes: schedule, who they'll meet, what each round covers, what to prepare
- [ ] **[R7]** Boolean search strings built and tested for role. GitHub + LinkedIn searches active
- [ ] **[R8]** Employee referral program active with bonus amounts defined and payout within 30 days of start
- [ ] **[R9]** Offer letter template includes: comp table, equity details (grant size, strike price, vesting, PTEW), benefits summary
- [ ] **[R10]** Closing strategy written before any offer goes out: candidate priorities, competing offers, flex levers, BATNA
- [ ] **[R11]** Offer decision communicated within 24 hours of final debrief (yes or no)
- [ ] **[R12]** ATS configured: stages, templates, scorecards, automated candidate communications
- [ ] **[R13]** Recruiting dashboard live: weekly pipeline health + monthly source effectiveness + quarterly quality-of-hire
- [ ] **[R14]** Candidate NPS survey sent to all interviewed candidates; score tracked quarterly
- [ ] **[R15]** Rooney Rule compliance: at least 2 underrepresented candidates interviewed per role before offer

## What Good Looks Like

A hiring manager can open the ATS and see: pipeline health (candidates per stage, no one stuck >5 days), scorecard completion rate 100%, offer acceptance rate >80%, time-to-fill <30 days for IC roles and <60 days for exec roles. Candidates receive prep emails 48 hours before interviews and decisions within 24 hours of their last round. Every rejected candidate gets a human phone call. The careers page shows real team photos, links to engineering blogs, and lists comp ranges. At 6 months, hiring managers rate new hires >4/5 on quality-of-hire score.

## References
<!-- QUICK: 30s — links to deeper reading and files -->

- [Pave — Real-time compensation benchmarking](https://www.pave.com/)
- [Levels.fyi — Tech compensation data](https://www.levels.fyi/)
- [OptionImpact — Equity benchmarking for startups](https://www.optionimpact.com/)
- [Carta — Equity management and 409A valuations](https://carta.com/)
- [Greenhouse — Structured hiring ATS](https://www.greenhouse.com/)
- [Ashby — All-in-one recruiting platform](https://www.ashbyhq.com/)
- [Lever — Talent acquisition suite](https://www.lever.co/)
- [Gem — Recruiting CRM and sourcing](https://www.gem.com/)
- [references/offer-letter-template.md](./references/offer-letter-template.md) — Complete offer letter template with equity language
- [references/interview-scorecard-template.md](./references/interview-scorecard-template.md) — Scorecard template with rubric anchors
- [references/job-description-template.md](./references/job-description-template.md) — Outcome-based JD template with examples
- [references/boolean-search-library.md](./references/boolean-search-library.md) — Boolean search strings by role family
- [assets/closing-strategy-canvas.md](./assets/closing-strategy-canvas.md) — One-page canvas for pre-offer closing plan
- [assets/sourcing-channel-effectiveness-tracker.csv](./assets/sourcing-channel-effectiveness-tracker.csv) — Tracker for source-of-hire data
