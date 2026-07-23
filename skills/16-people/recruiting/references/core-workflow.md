# Core Workflow — Full Implementation

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
