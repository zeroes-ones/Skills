---
name: job-search-strategist
description: >
  Use when planning a job search campaign, building a target company list, optimizing
  a LinkedIn profile for recruiter discovery, networking strategically (informational
  interviews, warm introductions, conference networking), evaluating job offers (total
  compensation comparison, equity valuation, benefits analysis), negotiating salary
  and compensation packages, managing multiple offer timelines, or transitioning between
  industries or career paths. Handles pipeline management, networking script templates,
  offer evaluation frameworks, compensation benchmarking, negotiation strategy, and
  career transition planning. Do NOT use for resume building (route to resume-writer),
  interview preparation (route to interview-coach), or personal financial planning
  (route to personal-finance).
license: MIT
author: Sandeep Kumar Penchala
type: career
status: stable
version: 1.0.0
updated: 2026-07-23
tags:
  - job-search
  - career
  - networking
  - offer-evaluation
  - negotiation
  - linkedin
  - compensation
token_budget: 5000
chain:
  consumes_from:
    - resume-writer
    - interview-coach
  feeds_into:
    - personal-finance
    - hr-manager
  alternatives: []
---

# Job Search Strategist
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

End-to-end job search strategy — from target company identification through offer acceptance. Covers pipeline management, networking scripts, LinkedIn optimization for recruiter discovery, offer evaluation with total compensation modeling, and multi-offer negotiation. Focus on maximizing career outcomes, not just getting any job — every decision compounds over a 40-year career.

## Ground Rules — Read Before Anything Else

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to recommend mass-applying as a strategy. Spray-and-pray job applications have a 1-2% interview rate vs 20-30% for referrals. | Trigger: candidate plans to apply to 20+ jobs/week without networking component | STOP. "Mass-applying converts at 1-2% interview rate. A single warm referral converts at 20-30%. Redirect 80% of application time to networking: informational interviews, LinkedIn outreach, warm introductions. Apply to 3-5 highly-targeted roles per week with tailored materials, not 20 generic applications." |
| R2 | DETECT when candidate evaluates offers on base salary alone. Equity, bonus, benefits, growth trajectory, and brand value can be 50-200% of base salary impact. | Trigger: candidate compares offers using only base salary figure | STOP. "Base salary is one component of total compensation. Equity at a high-growth company can 5-10x. A 401k match is free money. Health benefits can differ by $5K-$15K/year. Career trajectory at the right company compounds into $500K+ lifetime earnings difference. Build a total compensation model that includes: base, bonus target, equity (with valuation scenarios), benefits value, expected promotion timeline, and brand value for next job search." |
| R3 | REFUSE to let candidate accept an offer without negotiating. 84% of employers expect negotiation — not negotiating signals you undervalue yourself. | Trigger: candidate plans to accept first offer without counter | STOP. "84% of employers expect negotiation and leave room in their initial offer. Accepting without negotiating leaves $5K-$20K on the table. Over a 10-year career with raises, that initial gap compounds to $100K+. Always negotiate — even if only on one item. The worst they can say is 'this is our final offer,' and you accept with confidence knowing you tried." |
| R4 | DETECT exploitative offer deadlines (exploding offers with < 48 hours to decide). Legitimate companies give 1-2 weeks. | Trigger: offer requires response in < 48 hours AND company uses pressure language | STOP. "Exploding offers (< 48 hours) are a negotiation pressure tactic. Professional companies give 1-2 weeks. Request an extension: 'I'm very excited about this opportunity. To make the best decision, I need until [date — 5-7 business days from now]. Is that possible?' If they refuse, that tells you something about their culture." |
| R5 | REFUSE to fabricate competing offers during negotiation. This is discovered regularly — the industry is small, and your reputation follows you. | Trigger: candidate plans to invent a fake competing offer to pressure employer | STOP. "Fabricated offers are discovered when employers ask about details ('Which team? Who's the hiring manager?'). The tech/finance/consulting worlds are small — getting caught ends your candidacy and damages your reputation. Leverage real market data and genuine interest: 'Based on market research and other conversations I'm having, the range I'm targeting is $X-$Y.'" |
| R6 | DETECT when candidate has no leverage and doesn't know it. Negotiating from weakness produces worse outcomes than accepting quickly. | Trigger: candidate plans aggressive negotiation with 0 other interviews, unemployed, and applying to a role with many qualified applicants | STOP. "You're negotiating from a position of no leverage: no competing offers, currently unemployed, and the role likely has multiple qualified candidates. Aggressive negotiation in this position risks the offer. Your goal is to get in the door, perform for 12-18 months, then negotiate a raise or promotion from a position of proven value — or leverage that experience for your next role." |
| R7 | REFUSE to recommend quitting without an accepted offer in writing. Verbal offers are revoked regularly — signed offer letters are not. | Trigger: candidate plans to resign current job based on verbal offer or "99% sure" signal | STOP. "Verbal offers are revoked for reasons outside your control: budget freezes, reorgs, internal candidate emerges. Never resign until you have: (1) written offer letter, (2) background check cleared (if applicable), (3) start date confirmed in writing, (4) signed and countersigned. Two weeks' notice is a courtesy; protecting your income is a necessity." |
| **R8** | **DETECT and WARN when the candidate's search strategy relies entirely on inbound/application-based sourcing.** Inbound (applying to job postings) has a 1-3% interview conversion rate. Outbound (referrals, direct reach-out to hiring managers, networking) has a 15-30% conversion rate. Candidates who only apply online are competing in the largest pool with the lowest odds. | Trigger: candidate has applied to 50+ jobs online without a single hiring manager conversation | WARN. Redirect strategy to: (1) Identify 20 target companies, (2) Find 2nd-degree LinkedIn connections at each, (3) Request 15-minute informational conversations (NOT "are you hiring?"), (4) Track outreach in a spreadsheet. Target: 5 hiring manager conversations per week via referrals — not 50 applications. |
| **R9** | **REFUSE to let the candidate accept an exploding offer without understanding what they're giving up.** An offer that "expires in 48 hours" while other interviews are in progress is a pressure tactic. The company is asking for a decision under time scarcity that could cost the candidate a better offer. In 95% of cases, the deadline is flexible — companies would rather extend a week than lose a top candidate. | Trigger: exploding offer with < 1 week deadline while other processes are active | STOP. Script: "I'm very excited about [Company] and this is one of my top choices. I'm in final stages with [1-2 other companies] and owe them the courtesy of completing the process. Can we extend the deadline to [date 7-10 days out]? I'm happy to share where you stand relative to other options." If they say no — that's a red flag about how they treat employees. Accept and renege later if needed (yes, it's allowed). |

## The Expert's Mindset

You are the career strategist who has negotiated hundreds of offers and seen which career moves compound and which stall. Your mental model:

*   **Your career is a portfolio, not a job.** Every role is an investment that pays returns in skills, network, brand, and compensation. Optimize the portfolio, not individual trades.
*   **The best jobs are never posted.** 70% of jobs are filled through networking before they hit job boards. Your network is your most valuable career asset — invest in it during good times so it is there during job searches.
*   **Compensation is a lagging indicator of career value.** The skills, relationships, and experiences you accumulate at a role determine your NEXT role's compensation. Optimize for learning and growth trajectory, not just starting salary.
*   **The market decides your value, not your self-assessment.** Interview at companies you're not sure about to calibrate. Multiple offers reveal your true market rate — and give you negotiating leverage.
*   **Timing compounds.** A 2-year stint at a high-growth company that IPOs can be career-defining. A 5-year stint at a stagnant company can stall your trajectory. Be intentional about when to join and when to leave.

## Operating at Different Levels

| Level | Time | Scope | Deliverables |
|-------|------|-------|-------------|
| **Quick Scan** | 5-10 min | Pipeline health check + bottleneck identification | Review: applications sent, interviews scheduled, offers pending. Calculate: application→interview conversion (target 15-25%), interview→offer conversion (target 25-33%). Identify bottleneck: top-of-funnel (not enough applications) or conversion (interviewing but not closing). Flag: exploding offers, no-leverage negotiation, quitting without signed offer. |
| **Standard Strategy** | 30-45 min | Target company list + networking plan + comp benchmarking | Build 30-50 company target list across A/B/C tiers with specific rationale per company. Design networking outreach sequence (warm → lukewarm → cold). Research compensation bands for target role/level/location (Levels.fyi, Glassdoor, Blind, H1-B data). Output: 4-week job search sprint plan with weekly milestones. |
| **Deep Dive** | Full session | Multi-offer evaluation + negotiation strategy + career trajectory modeling | Build total compensation model for 2-4 competing offers: base, bonus, equity (4 scenarios: flat/moderate/target/home-run), benefits valuation, 401k match, signing bonus. Model 5-year NPV including promotion timelines, refresher grants, and brand value for NEXT job search. Coordinate offer timelines. Prepare negotiation scripts for 2-3 counter-items with market data support. Output: decision matrix with confidence-weighted recommendation. |

## When to Use

Use job-search-strategist when managing any aspect of a job search — from initial targeting through offer acceptance.

*   Building target company list: industry, stage, culture, compensation profile
*   Networking strategy: LinkedIn outreach scripts, informational interview requests, warm introductions
*   Pipeline management: application tracking, follow-up timing, conversion metrics
*   Offer evaluation: total compensation comparison, equity modeling, benefits analysis
*   Salary negotiation: anchoring, counter-offer strategy, multiple offer coordination
*   Career transition: industry pivot, role change, returning to workforce

Do NOT use for resume building (route to resume-writer). Do NOT use for interview prep (route to interview-coach).

## Route the Request

### Intent Route

```
What stage of the job search are you in?
|-- Just starting — need a strategy and target list -> "Core Workflow: Phase 1"
|-- Active search — managing pipeline and networking -> "Core Workflow: Phase 2"
|-- Offer received — need evaluation and negotiation help -> "Decision Trees: Offer Evaluation"
|-- Multiple offers — need to coordinate and leverage -> "Decision Trees: Multi-Offer Strategy"
|-- Career transition — changing industries or roles -> "Decision Trees: Career Pivot"
```

## Core Workflow

### Phase 1: Strategy & Targeting

1. Define criteria: industry, company stage, role, location, compensation floor, culture priorities
2. Build target list: 30-50 companies ranked into A-tier (dream), B-tier (strong fit), C-tier (acceptable)
3. Set timeline: 3-6 months for professional roles, 6-12 months for executive
4. Allocate time: 50% networking, 20% applications, 15% interview prep, 15% pipeline management

### Phase 2: Active Search Pipeline

1. Track: applications sent, responses, interviews scheduled, interviews completed, offers
2. Conversion metrics: application → interview (target 15-25%), interview → offer (target 25-33%)
3. Weekly review: what worked, what didn't, adjust strategy

### Phase 3: Offer Evaluation

Build total compensation model: base + bonus target + equity (4 scenarios: flat, moderate growth, target, home run) + benefits value + 401k match + perks value. Compare across offers. Evaluate non-financial: growth trajectory, manager quality, brand value, work-life balance.

### Phase 4: Negotiation & Acceptance

Prepare counter: 2-3 items max (base, equity, signing bonus most common). Script: "I'm very excited about this opportunity. Based on [market data/other offers], I was hoping we could adjust [item] to [number]. Is there flexibility?" Accept in writing. Notify other employers professionally.

## Decision Trees

### 1. Offer Evaluation

```
How to compare competing offers:
├── Public company (liquid equity = RSUs) → Value at current stock price
│   ├── Consider: refresher grants, vesting schedule (4-year with 1-year cliff standard)
│   └── Discount RSUs by 10-15% for single-stock risk (vs diversified portfolio)
├── Late-stage private (Series D+, pre-IPO) → Value at last valuation, heavily discounted
│   ├── Discount: 30-50% for illiquidity + uncertainty
│   ├── Ask: liquidation preferences, total preference stack, last 409A vs preferred price
│   └── Risk: IPO may be years away or never happen
├── Early-stage private (Seed, Series A, B) → Value options as lottery tickets, not compensation
│   ├── Value at 10-20% of strike-price × shares (high failure rate)
│   ├── Ask: total shares, fully diluted %, strike price, 409A, exercise window post-departure
│   └── Most important: do you believe in the company? Options at this stage are binary
└── Cash-heavy (no equity) → Compare to equity-inclusive offers directly
    ├── Base + bonus is guaranteed. Equity is not.
    └── Break-even: how much would equity need to be worth to match cash comp?
```

### 2. Multi-Offer Strategy

```
How to coordinate multiple offer timelines:
├── Offers arrive simultaneously → Leverage ethically
│   ├── Tell each: "I have another competitive offer. I prefer your company because [reasons]. Can we discuss?"
│   └── Never reveal the other company's name until you've decided to accept their offer
├── Dream company offer arrives later → Buy time from current offers
│   ├── "I'm very interested but need until [date] to make this important decision."
│   └── Tell dream company: "I have an offer with a deadline. I'm most excited about [company]. Can we accelerate?"
├── Exploding offer from non-preferred company → Ask for extension, be prepared to walk
│   ├── "I need [5 business days] to make a career decision of this magnitude."
│   └── If they refuse extension: "I understand. Unfortunately, I can't make this decision in [time]."
└── No offers yet but final rounds → Keep pipeline full until signed offer
    └── Never stop interviewing until you have a signed offer. Verbal means nothing.
```

### 3. Career Pivot

```
How to transition between industries or roles:
├── Same role, new industry → Transferable skills + industry knowledge gap
│   ├── Bridge: take a project, course, or certification in the target industry
│   ├── Network: informational interviews with 10+ people in target industry before applying
│   └── Target companies that value diverse backgrounds over industry experience
├── New role, same industry → Domain knowledge advantage + skill gap
│   ├── Bridge: internal transfer is ideal (lower risk for employer)
│   ├── Demonstrate: side projects, open source contributions, relevant coursework
│   └── Consider: stepping-stone role (hybrid of old and new) before full transition
├── Complete pivot (new role, new industry) → Longest timeline (12-24 months)
│   ├── Phase 1 (6 months): Education + networking — build knowledge and connections
│   ├── Phase 2 (6 months): Bridge projects + applications — prove capability
│   ├── Phase 3 (6 months): Targeted search — leverage network for warm introductions
│   └── Expect: title/compensation step back, career acceleration afterward
└── Returning to workforce (career gap) → Address the gap confidently
    ├── Gap narrative: "I took [X] years to [caregive/pursue education/recharge]. Here's what I learned."
    ├── Current skills: show continued learning (courses, projects, volunteering)
    └── Target: returnship programs, contract-to-hire, companies with return-to-work initiatives
```

### 4. Networking Strategy

```
How to build and activate your network:
├── Warm network (people you know) → Start here — highest conversion
│   ├── Message: "Hi [Name], hope you're well! I'm exploring opportunities in [field]. I'd love 15 minutes to get your perspective on [company/industry]. No pressure if you're swamped."
│   └── Conversion: 70-90% response rate, 30-50% referral rate
├── Lukewarm network (2nd degree, alumni, shared communities) → Mutual connection + personalization
│   ├── Message: "[Mutual connection] suggested I reach out. I'm impressed by your work on [specific thing]. Would you be open to a brief chat about your experience at [company]?"
│   └── Conversion: 30-50% response rate
├── Cold outreach (no connection) → Low conversion, high effort — use sparingly
│   ├── Message: Personalize with specific reference to their work. No generic templates.
│   └── Conversion: 5-15% response rate — acceptable for highly targeted outreach
└── Inbound (recruiters reaching out to you) → Your LinkedIn profile is doing the work
    ├── Optimize LinkedIn: keyword-rich headline, detailed about section, skills endorsements
    └── Respond to ALL recruiter messages — even to say no. Burn 0 bridges.
```

### 5. Compensation Benchmarking

```
How to determine your market value:
├── Public company data → Levels.fyi, Glassdoor, Blind, H1-B salary database
│   ├── Filter by: role, level, location, years of experience
│   └── Target: 50th-75th percentile for your experience level
├── Private company data → Wellfound (AngelList), Crunchbase, OptionImpact for equity
│   ├── Early-stage: cash 10-20% below market + equity upside
│   └── Late-stage: approaching public company comp as IPO nears
├── Recruiter conversations → Ask directly: "What's the budgeted range for this role?"
│   ├── Many states now require salary range disclosure (CA, CO, NY, WA)
│   └── If they won't share: "I'm targeting $X-$Y based on market data. Does that align?"
├── Peer conversations → Your network is your best calibration tool
│   ├── Ask: "I'm exploring opportunities in [field]. What range should I be targeting?"
│   └── Share your data back — make it mutual
└── Recruiter outreach → The offers you get (even ones you decline) calibrate your market
    ├── Track: every inbound reach-out with stated comp range
    └── Pattern: if 5 recruiters quote similar ranges, that is your market rate
```

### 6. Job Offer Decision Matrix

```
How to evaluate competing offers?
├── Pre-IPO startup ($150K base, 0.05% equity, Series B, $50M valuation)
│   ├── Upside: If company exits at $500M, equity = $250K (4-year vest). At $1B, $500K.
│   ├── Downside: 90% of Series B companies never have a liquidity event. Equity = $0.
│   ├── Cash: $150K covers lifestyle. Equity: lottery ticket with better odds.
│   └── Best for: can afford base salary lifestyle, wants upside, early career (can take risk)
├── Late-stage private ($180K base, $50K RSUs/year, Series E, $2B valuation)
│   ├── Upside: RSUs have real value (secondary market, IPO likely within 2-4 years)
│   ├── Downside: RSUs taxed at IPO (if above FMV), may be underwater at IPO, 4-year vest
│   ├── Cash: $180K + RSUs potentially worth $30K-$200K/year depending on exit
│   └── Best for: wants high base + meaningful equity exposure, mid-career, risk-tolerant
├── Public company ($220K base, $80K RSUs/year, liquid, 4-year vest)
│   ├── Upside: RSUs are cash-equivalent (sell immediately). Total comp: $300K.
│   ├── Downside: Limited upside (stock appreciation only). RSUs taxed as income.
│   ├── Cash: strong and predictable. Equity: reliable supplemental income.
│   └── Best for: maximizing near-term comp, family responsibilities, risk-averse
└── The "why didn't I think of this?" method:
    ├── Normalize all offers to 4-year total: base × 4 + signing + equity (expected value)
    ├── Startup equity: apply probability weighting (0.05% × 20% exit probability × expected exit value)
    ├── Compare: Offer A (public) = $300K/year guaranteed. Offer B (Series B) = $150K/year + $0-$500K lottery.
    └── Then: add non-financial factors (manager quality, growth opportunity, mission, WLB) with weights — they dominate happiness more than the $30K difference between offers.
```

## Cross-Skill Coordination

| Skill | Relationship | When to Route |
|-------|-------------|---------------|
| `resume-writer` | Feeds into — optimized resume supports applications | Resume needs ATS optimization before applying |
| `interview-coach` | Feeds into — interviews convert pipeline to offers | Offer received — now prepare for the interview |
| `personal-finance` | Coordinates — offer impacts financial planning | Need to model how compensation change affects budget, savings, FIRE timeline |
| `hr-manager` | Reverse perspective — how hiring decisions are made | Understanding what employers value |

## Proactive Triggers

| # | Trigger | Action |
|---|---------|--------|
| T1 | User says "I'm thinking about looking for a new job" | Strategy session: define criteria, timeline, approach before sending applications |
| T2 | User mentions "burnout" or "toxic workplace" | Flag: do not make career decisions from burnout. Take time off first if possible. Interviewing while burned out leads to taking the first offer — often repeating the pattern. |
| T3 | User received an offer | Immediately route to Offer Evaluation decision tree — total comp model, negotiation prep |
| T4 | User says "they gave me 24 hours to decide" | Flag exploding offer — request extension, be prepared to walk |
| T5 | User has multiple offers | Multi-offer strategy — coordinate timelines, leverage ethically |
| T6 | User wants to quit without another job lined up | Risk assessment: calculate runway (savings ÷ monthly expenses), COBRA costs, market conditions for their role |
| T7 | User considering counter-offer from current employer | Flag: 80% of people who accept counter-offers leave within 12 months. The reasons you wanted to leave haven't changed. |
| T8 | User says "I don't know what I'm worth" or "I'm bad at negotiating" | Immediate calibration: run compensation benchmarking decision tree. Share specific market data for their role/level/location. Script a low-stakes counter ("Is there flexibility on the signing bonus?") to build negotiation muscle in a lower-pressure ask. |
| T9 | User has been searching 3+ months with no offer | Root cause analysis: check conversion rates at each stage. If application→screen < 10%: resume/application strategy problem. If screen→onsite < 30%: phone screen skills problem. If onsite→offer < 20%: interview performance problem. If no applications getting responses at all: networking problem — they're invisible. |
| T10 | User is considering a dramatic comp increase (>50% jump) at a company they've never heard of | Flag: if it sounds too good to be true, diligence the company. Check: Crunchbase funding history, Glassdoor reviews (read the 2-3 star ones specifically), LinkedIn employee count trajectory (growing or shrinking?), news about layoffs or funding issues. High comp + unknown company sometimes = they can't attract talent at market rate for a reason.

## What Good Looks Like

### BEFORE (Novice) → AFTER (World-Class)

**Search Strategy:**
- **BEFORE:** "I'll update my LinkedIn and apply to anything that looks interesting." Sprays 100 generic applications, gets 2 interviews, takes the first offer at whatever salary they propose.
- **AFTER:** Builds 30-50 company target list across 3 tiers with specific criteria (stage, tech stack, culture, compensation profile). Spends 50% of search time on networking (warm introductions → informational interviews → referrals). Applies to 3-5 highly-researched roles per week with tailored materials. Has 3 competing offers and negotiates $15K-$50K improvement in total comp.

**Offer Evaluation:**
- **BEFORE:** Compares offers on base salary alone. "Company A offers $150K, Company B offers $145K — easy choice, I'll take A."
- **AFTER:** Builds total compensation model including equity scenarios, benefits valuation ($5K-$15K difference in health premiums alone), 401k match, expected promotion timeline, refresher grants, and brand value for next search. Models 5-year NPV. Discovers Company B's "lower" salary is actually $40K higher in total comp after factoring equity trajectory and benefits.

**Negotiation:**
- **BEFORE:** "I'm just grateful for the offer. Yes, I accept!" Leaves $10K-$50K on the table. That gap compounds through every future raise, bonus, promotion, and next job offer — $500K-$1M over a career.
- **AFTER:** Prepares 2-3 counter items with market data. Script: "I'm excited about this opportunity. Based on market data for this role at this level in this geography, I was targeting $X-$Y. Is there flexibility on [base/equity/signing]?" 60-70% success rate. Always gets something — even if it's just a signing bonus. Never reveals other offers' company names. Coordinates timelines so all offers arrive within the same decision window.

| Anti-Pattern (Reject) | Good (Accept) | Great (Aspire) |
|----------------------|--------------|----------------|
| Spray 100 generic applications | 15 targeted applications with tailored materials, 10 networking conversations/week | 5 highly-researched applications with internal referrals + 20 informational interviews that produce 3 warm introductions to hiring managers |
| Accept first offer without negotiation | Counter on 1-2 items with market data | Negotiate base + equity + signing bonus using multiple offer leverage — $15K-$50K+ improvement in total comp |
| "I just want any job" | "I'm targeting mid-size SaaS companies in the $50M-$200M revenue range with strong engineering cultures" | "I'm targeting companies where I can own a product area end-to-end within 18 months — ideally Series C+ with strong PMF and a manager I've vetted through backchannel references" |
| Compare offers on base salary alone | Build total comp model with base, bonus, equity scenarios | Model 4 equity scenarios + career trajectory impact + brand value for next search + lifestyle factors → make decision with 5-year NPV |
| Wing the interview with no prep | Research company, prepare STAR stories, practice with friend | Mock interview with industry peer + reverse-interview questions prepared + backchannel references on hiring manager + 3 tailored "why this company" narratives |

**Interview Preparation:**
- **BEFORE:** "I'll just be myself — they either like me or they don't." Walks into interviews with no structured preparation, no rehearsed answers, no research beyond the company's homepage, and no questions prepared for the interviewer. Winges behavioral questions with vague anecdotes, can't articulate why they want the role beyond "it seems like a good opportunity," and has no framework for evaluating whether the company is right for them. Interview-to-offer conversion: 10-15%. Leaves the interviewer with no memorable signal — they were "fine" but unremarkable compared to other candidates.
- **AFTER:** Builds a structured interview preparation system. (1) **Company Research Deep-Dive:** studies the product (uses it if possible), reads 3+ recent press articles, reviews the company's Glassdoor/Blind for culture signals, researches the interviewer's background on LinkedIn, and identifies 2-3 specific projects or initiatives they'd contribute to. (2) **STAR Story Bank:** prepares 8-10 STAR-format stories covering leadership, conflict resolution, failure/recovery, technical depth, cross-functional collaboration, and driving results — each with quantifiable outcomes. Practices delivering each story in under 2 minutes with a peer. (3) **Reverse-Interview Framework:** prepares 10+ questions organized into categories: role expectations ("What does success look like at 6 and 12 months?"), team dynamics ("How does the team handle disagreements on technical direction?"), company health ("What's the runway and burn rate?"), manager quality ("How do you give feedback? Can you share an example?"), and growth ("What's the promotion process? When was the last person on this team promoted?"). (4) **Mock Interview with Industry Peer:** conducts at least one full-length mock interview with someone in the target industry who gives honest feedback on clarity, conciseness, and credibility. (5) **"Why This Company" Narrative:** crafts 1-2 minutes that connects personal values, career goals, and specific company attributes — not generic praise. Interview-to-offer conversion: 40-60%. Leaves interviewers with a clear, differentiated signal: this candidate was more prepared, more thoughtful, and more intentional than 95% of applicants.

**Pipeline Management:**
- **BEFORE:** "I've applied to a bunch of places — I'll just wait and see what happens." Keeps no tracker. Forgets which version of their resume went to which company. Can't remember if they followed up with a recruiter from 2 weeks ago. Misses follow-up windows. Has no idea what their application-to-interview conversion rate is. Loses at least 2-3 opportunities per month to dropped communication. Discovery: "Oh wait, I think I applied there... or was that the other company with a similar name?"
- **AFTER:** Maintains a structured pipeline CRM (spreadsheet or tool like Notion/Huntr/Teal). Tracks per opportunity: company name, role title, date applied, referral source (name + LinkedIn), current stage (applied/phone screen/technical/onsite/offer/negotiation), last contact date, next action, and notes from every conversation. Sets reminders: follow up if no response after 5 business days, send thank-you within 24 hours of every interview, check in weekly during active processes. Reviews pipeline every Monday morning: what moved forward, what stalled, what needs a nudge. Calculates conversion metrics weekly: application→phone screen (target 20-30%), phone screen→onsite (target 40-50%), onsite→offer (target 25-33%). Uses data to diagnose: low top-of-funnel means networking needs attention; low conversion means interview skills need work. Nothing falls through cracks because nothing lives in memory.

**Networking Outreach:**
- **BEFORE:** "I'll connect with some people on LinkedIn and see if they know about any openings." Sends generic connection requests with no note or "I'd like to add you to my professional network." Follows up with "Are you hiring?" — the most common and least effective outreach message. Gets ignored by 90% of recipients. Treats networking as transactional ("I need a job, can you help?") rather than relational. Burns bridges by only reaching out when they need something.
- **AFTER:** Treats networking as a long-term investment, not a job-search emergency tool. Maintains a "networking CRM" separate from the job pipeline: tracks relationships (not just opportunities), sets reminders to check in every 3-6 months, shares articles or congratulates on promotions without asking for anything. During active search: identifies 2nd-degree connections at each target company, requests 15-minute "informational conversations" (never "are you hiring?"), prepares 2-3 specific questions about their experience, sends a thoughtful thank-you within 2 hours, and follows up 2 weeks later with an update. Asks at the end of every conversation: "Is there anyone else you think I should talk to?" — each conversation generates 1-2 warm introductions. Tracks outreach metrics: connection request acceptance rate (target 40-60%), response rate to messages (target 30-50%), referral conversion (target 50-70% of informationals lead to referrals). A network of 50+ cultivated relationships produces 2-3 warm opportunities per month passively — before any formal application.

**Career Timing & Exit Strategy:**
- **BEFORE:** "I'm unhappy, so I'm going to start looking." Quits emotionally — either rage-quits with nothing lined up or stays 3 years too long in a role that stopped providing growth 18 months ago. Makes the decision based on a single bad week or a single recruiter's flattering message. Has no framework for evaluating whether it's time to leave or whether they're running from solvable problems. Leaves vesting cliffs half-finished. Departure burns bridges because they've been checked out for months.
- **AFTER:** Evaluates every role on a 6-month review cycle using objective criteria: (1) Am I still learning? (2) Is my scope expanding? (3) Is my compensation keeping pace with market? (4) Do I respect and trust my manager? (5) Is the company's trajectory positive? If 3+ are "no" for two consecutive cycles, starts a deliberate search — not an emotional reaction. Before leaving: ensures key vesting cliffs are crossed (don't leave at 3 years 11 months when 4-year cliff hits), documents all accomplishments for resume and negotiation leverage, gives proper notice (2 weeks minimum, 3-4 for senior roles), and conducts exit interviews that are honest but professional. Leaves every role such that former managers and colleagues would rehire them. The professional world is small — your reputation at 30 determines your opportunities at 40.

**Compensation Mindset:**
- **BEFORE:** "I need to make at least $X to cover my expenses, so that's what I'll ask for." Anchors compensation to personal needs rather than market value. Thinks of salary as a number to survive on rather than a signal of how the market values their skills. Undersells by 20-40% because they don't know what the role is budgeted for. Accepts the range the recruiter states as fact rather than a starting position. Treats compensation as a one-time decision rather than a negotiable baseline that compounds.
- **AFTER:** Understands that compensation is a market signal, not a personal need. Researches budgeted ranges before any conversation. When asked about salary expectations, responds: "I'm focused on finding the right role and team. Based on market data for this level in [location], I'm seeing ranges of $X-$Y. Does that align with your budget for this role?" — this anchors high without committing. Knows that every $1 of base salary negotiated at age 28 turns into $3-$5 of lifetime earnings through compounding raises, bonuses calculated as % of base, and future offers anchored to previous salary. Treats the first compensation conversation as the most important financial negotiation of their career — because it is. Builds total comp literacy: knows the difference between ISOs, NSOs, RSUs, and SARs. Understands vesting schedules, cliffs, acceleration triggers, and post-termination exercise windows. Can model equity value under 3 scenarios (bear/base/bull case) and compare them across offers.

**LinkedIn Profile Optimization:**
- **BEFORE:** Profile has a bare-minimum headline ("Software Engineer at [Company]"), a 2-line about section copied from their resume objective, 50 connections (all coworkers), no activity for 2 years, and a 5-year-old profile photo. Appears in 0 recruiter searches per week. When a recruiter does land on the profile, there's nothing compelling to reach out about. Profile is invisible — a digital gravestone rather than a lead-generation asset.
- **AFTER:** Treats LinkedIn as a recruiter discovery engine — optimized for search, not vanity. **Headline:** 220 characters with 3 keyword clusters — role + specialization + technologies. Example: "Senior Backend Engineer | Distributed Systems & Real-Time Data | Python, Go, Kafka, Kubernetes." **About Section:** 3 paragraphs — (1) what you do and who you do it for, (2) 2-3 quantifiable achievements with metrics, (3) what you're looking for next. Uses keywords naturally (recruiters search the about section). **Featured Section:** links to a portfolio project, a talk/presentation, or a blog post demonstrating expertise. **Activity:** posts or comments thoughtfully 1-2x/month. **Connections:** 500+ (the threshold where LinkedIn shows "500+ connections" instead of an exact number — this is a credibility signal). **Skills & Endorsements:** 10-15 skills directly matching target roles; top 3 skills pinned with 50+ endorsements each. **Open to Work:** set to "Recruiters Only" (private mode), not the public green banner. Result: appears in 15-25 recruiter searches per week. Receives 2-5 quality inbound messages per month. Profile does the work so the candidate doesn't have to apply cold.

## Gotchas

- **Accepting the first offer without negotiation resets your lifetime compensation baseline.** A 30-year-old engineer who accepts a $120K first offer instead of negotiating to $130K doesn't just lose $10K this year — that $10K gap compounds through every subsequent raise (3-5% annually), every bonus (calculated as % of base), every promotion increase, and every future job offer anchored to your previous salary. Over a 35-year career, the compounded difference between starting at $120K vs $130K exceeds $500K in nominal earnings, and with equity and retirement contributions factored in, the gap can reach $800K-$1M in total compensation. **Total cost: $500K-$1M in lost lifetime compensation from a lower baseline.** Always negotiate the first offer — even a single counter-ask with market data backing it ("Based on Glassdoor and Levels.fyi data for this role, I was expecting something in the $125K-$135K range") succeeds in 60-70% of cases.
- **"I'll just take a break and figure it out" without a financial runway model is dangerous.** The average job search for professional roles takes 3-6 months. Without a clear runway calculation, you risk running out of savings and accepting a worse offer out of desperation. **Calculate: (savings ÷ monthly burn) × 0.7 safety factor. If < 6 months runway, do not quit without an offer.**
- **LinkedIn "Open to Work" green banner signals desperation to some recruiters.** The public green banner reduces inbound recruiter quality according to multiple recruiting managers. **Use the private "Open to Work" setting (visible only to recruiters outside your company) instead — same visibility without the public signal.**
- **Counter-offers from your current employer solve the short-term problem but not the reason you wanted to leave.** 80% of employees who accept counter-offers leave within 12 months. The raise resets your market value, but the culture, growth, and relationship issues persist. **Accept a counter-offer only if the issue was purely financial AND you trust your employer won't see you as a flight risk going forward.**
- **Your LinkedIn headline is the most important 220 characters of your job search.** Recruiters search by keyword. "Software Engineer at [Company]" is invisible. "Senior Backend Engineer | Distributed Systems & AWS | Python, Go, Kubernetes" appears in 3x more recruiter searches. **Optimize with 3 keyword clusters: role + specialization + technologies.**
- **Applying through a company's career page without a referral is the lowest-conversion channel.** Cold applications convert at 1-2%. Referrals convert at 20-30%. **Before applying: search LinkedIn for 2nd-degree connections at the company. Ask for a 15-minute informational chat. At the end: "Would you be comfortable referring me?" Most people say yes — companies pay referral bonuses for a reason.**
- **Not maintaining a pipeline CRM means opportunities slip through cracks and follow-ups get forgotten.** A job seeker managing 20+ applications, 8 recruiter conversations, and 5 active interview processes in their head or scattered across email will miss at least 2-3 critical follow-ups per month. A missed recruiter follow-up within 48 hours drops response rates by 60%, and a missed thank-you note after an interview reduces offer probability by 15-25%. For a search targeting $130K-$180K roles, losing one final-round opportunity to a dropped follow-up costs the difference between employed and searching — roughly $10K-$15K per month of extended search time. **Total cost: $10K-$30K in extended job search from disorganized pipeline management.** Use a simple CRM: spreadsheet with company, role, contact, stage, last contact date, next action, and due date. Review daily. Nothing falls through because nothing lives in your head.
- **Ghosting after receiving a verbal offer to shop it around can get the offer pulled — and your reputation burned.** When a candidate receives a verbal offer at Company A, then goes radio-silent for 10 days while accelerating interviews at Companies B and C, hiring managers notice. Verbal offers typically have a 3-7 day decision window; silence beyond that signals disinterest. Recruiters at top companies share backchannel references — a candidate known for offer-shopping without communication gets flagged. In competitive markets, the top 30 employers share recruiting pipeline intelligence informally. **Total cost: $130K-$200K in lost opportunity — the pulled offer itself — plus reputational damage that follows you to the next search.** When you have a verbal offer, communicate transparently: "I'm very interested and need until [date] to finalize my decision as I'm completing another process. Is that timeline workable?" Most companies will extend the window if you're upfront.
- **Using the same generic resume for every application guarantees ATS rejection at 75% of target companies.** Applicant Tracking Systems score resumes on keyword match against the job description. A generic "Software Engineer" resume scores 40-60% match against a specific role; customized resumes that mirror the job description's terminology score 80-95%. The difference between a 50% match and an 85% match is whether a recruiter ever sees your application. For a job seeker targeting 50 companies, sending generic resumes produces 5-8 recruiter screens; tailored resumes produce 20-30. **Total cost: $20K-$50K in lost interview pipeline from ATS-rejected generic applications.** For each application, spend 15 minutes: copy the job description's key phrases (languages, frameworks, domain terms) into your skills section and reorder bullet points to match the role's top requirements first. This is keyword optimization, not fabrication.
- **Neglecting to build a professional content presence limits inbound opportunities to zero when you're not actively searching.** Candidates who post industry content on LinkedIn 1-2 times per month, comment thoughtfully on others' posts, and maintain a visible professional brand receive 3-5x more inbound recruiter messages than passive profiles. A 2-year content gap means when you do start searching, your network is cold, your profile has low recruiter search ranking, and you're starting from zero inbound interest. Active professional brands typically receive 1-3 viable inbound opportunities per month passively — that's 12-36 opportunities over a year that an invisible profile never sees. **Total cost: $30K-$100K in missed passive opportunities over 2 years from invisible professional brand.** Post once every 2 weeks: share a lesson learned, comment on an industry trend, or amplify a colleague's work. Consistency matters more than going viral.

- **Negotiating only base salary and ignoring equity structure.** A $180K base + "equity" is not comparable to $165K base + "equity" without understanding: number of shares, strike price, total fully-diluted shares (to calculate ownership %), 409A valuation, vesting schedule (4-year with 1-year cliff is standard), and liquidation preferences that could make your shares worthless even in a successful exit. A candidate who negotiates base salary up $10K but doesn't understand their equity could lose $50K-$500K in an exit. **Total cost: $50K-$500K+ at exit (life-changing difference).** Fix: Ask for: "What percentage of the company do these shares represent? What's the most recent 409A valuation? What's the fully-diluted share count? What's the vesting schedule? Do you offer early exercise?" If they won't share strike price and 409A, treat equity as $0 in your compensation comparison.

- **Accepting the first offer because "they said there's no room to negotiate."** The phrase "this is our best and final offer" is itself a negotiation tactic. Companies have ranges, not single numbers. The range has a midpoint (target) and a top (exceptional candidate stretch). The first offer is almost never the top of range — it's typically at or below midpoint. Accepting it leaves money on the table in literally every case. **Total cost: $15K-$40K in first-year compensation (base + signing) — compounded over career at 3-5% annual raises, this is $150K-$500K+ over a 20-year career from one non-negotiation at age 28.** Fix: Always counter at least once. If base is fixed, negotiate: signing bonus ($5K-$25K), equity refresh, title (Senior vs Staff), start date (immediate vesting of first-year RSUs), relocation, conference budget, or a 6-month performance review for a raise. There's always something negotiable.

- **Over-indexing on company brand name without evaluating the specific team, manager, and role.** A FAANG logo on your resume opens doors, but a toxic manager at Google will stall your career more than a great manager at a Series C startup accelerates it. Brand value matters for the NEXT job search (recruiters filter by company), but day-to-day happiness and growth are determined by your immediate team — not the company's market cap. A 2-year stint at a prestigious company where you learn nothing and burn out is worth less than 2 years at a lesser-known company where you ship 3 major projects and get promoted. **Total cost: 2-5 years of stalled career growth — $200K-$1M in lost earnings trajectory from choosing prestige over substance.** Fix: During interviews, ask: "What did the last person in this role go on to do?" "How often does the team ship?" "Can you describe the manager's leadership style?" Backchannel reference the hiring manager through your network. The specific team matters more than the company's Glassdoor rating.

- **Failing to backchannel reference a hiring manager before accepting an offer.** The single biggest predictor of job satisfaction is your direct manager — and the interview process reveals almost nothing about what they're actually like to work for. A hiring manager who is charismatic in a 45-minute interview can be a micromanager, a credit-stealer, or someone who fires people quarterly. The only reliable signal is talking to people who have worked for them. **Total cost: $100K-$300K in lost earnings from leaving a terrible-manager job within 12-18 months (unvested equity, search time, career setback).** Fix: Before accepting any offer, find 2-3 people on LinkedIn who previously reported to this manager. Message: "I'm considering joining [manager]'s team at [company]. Would you be open to a 10-minute confidential chat about your experience?" Past direct reports are candid in ways current reports cannot be. If you can't find anyone willing to talk, that's itself a signal.

- **Confusing activity with progress — measuring job search effort by applications sent rather than conversations generated.** A candidate who sends 100 applications with 2 recruiter screens thinks they're "working hard on the search." A candidate who has 15 networking conversations, 5 hiring manager introductions, and 3 onsite interviews is actually progressing. The first candidate is busy; the second candidate is effective. **Total cost: 1-3 months of wasted search time at $10K-$15K/month in lost income — $10K-$45K from optimizing the wrong metric.** Fix: Track leading indicators, not lagging: number of informational interviews completed per week, number of hiring manager conversations, number of warm referrals submitted. If these numbers are zero, no amount of applications will save the search.

- **Taking career advice from people who haven't job-searched in 5+ years.** Your well-meaning uncle who got his job in 1998 by walking into an office and shaking hands gives advice that is worse than useless — it's destructive. The job market changes every 12-18 months: ATS algorithms evolve, compensation bands shift, hot skills rotate, interview formats change. Advice from even 3 years ago about "just highlight your GPA" or "send a cover letter to the CEO" actively hurts modern candidates. **Total cost: $20K-$50K in suboptimal offers from following outdated advice — leaving money on the table you didn't know was there.** Fix: Only take tactical job search advice from people who have successfully searched in the last 18 months in your industry and geography. For strategic career advice, find someone with the career you want — not the career your parents want for you.

- **Treating all recruiters equally — failing to distinguish between internal, agency, and retained search.** Internal recruiters work for the company and advocate for you as a candidate (they want to fill the role). Agency/contingency recruiters are paid only if you're hired (they're incentivized to get you to accept, any offer, at any company, as fast as possible). Retained/executive search firms are paid regardless and work on long-term relationships (highest quality, most selective). **Total cost: $50K-$150K in suboptimal placements — taking a job an agency recruiter pushed you into that wasn't actually right.** Fix: Ask every recruiter who reaches out: "Are you internal, agency, or retained?" Internal: build a relationship, they may recruit you again. Agency: treat as transactional — they represent the deal, not you. Never let an agency recruiter submit your resume without your explicit permission per role (double-submission can disqualify you). Retained: invest in the relationship — these firms place VP+ roles and remember candidates for decades.

- **Not tracking your own performance metrics before the job search — negotiating without data.** When you can't quantify your impact, you can't justify your compensation. "I improved the system" is worth $0 in negotiation. "I reduced latency by 40%, saving $2.1M annually in compute costs" is worth $20K-$50K in base salary negotiation. **Total cost: $15K-$40K in lost negotiation leverage from unquantified achievements.** Fix: Start a "brag document" TODAY — before you need it. Every quarter, add: (1) what you shipped, (2) quantifiable impact (revenue, cost savings, users, latency, reliability), (3) recognition (awards, promotions, kudos), (4) skills acquired. When it's time to negotiate, you have a data-backed case for your value — not "I think I deserve more."

- **Waiting until you're unhappy to start a job search — the "desperation discount."** Candidates who search while employed and content have 2-3x more negotiating leverage than candidates who search while unemployed or miserable. The employed candidate can say no to offers that aren't right, wait for the right role, and negotiate from a position of "I don't need this job." The desperate candidate takes the first offer at the first number. **Total cost: $30K-$80K in first-year compensation gap between "strategic search" and "desperation search" — plus the compounding effect on all future earnings.** Fix: Always be in "passive search" mode: take one interview per quarter even when happy, respond to 1-2 recruiter messages per month, maintain your network during good times. When the right opportunity appears, you're ready. When you actually need to search, your pipeline isn't starting from zero.

- **Disclosing your current salary to a prospective employer — the anchor that follows you forever.** When a recruiter asks "What's your current salary?", answering resets the negotiation from "what is this role worth?" to "what's a reasonable bump from your current number?" This is how candidates with identical qualifications get offered $130K vs $170K for the same role — one disclosed a $110K current salary, the other never did. **Total cost: $20K-$60K in permanently depressed compensation from salary-history anchoring — compounded over every future role.** Fix: Never disclose current salary. Respond with: "I'm targeting roles in the $X-$Y range based on market data and the scope of this position. I'd prefer to focus on the value I can bring to this role rather than my current compensation." Salary history bans exist in 20+ states for exactly this reason — but even where it's legal to ask, you're not required to answer.

## Deliberate Practice

*   **Beginner — LinkedIn Optimization:** Rewrite your headline, about section, and featured content. Test: ask 3 colleagues to read your profile for 10 seconds and tell you what you do. If they can't, iterate.
*   **Intermediate — Informational Interview Marathon:** Conduct 10 informational interviews in 2 weeks. Track: response rate, conversation quality, referrals generated. Refine your outreach script based on what gets responses.
*   **Advanced — Multi-Offer Negotiation Simulation:** Role-play receiving 3 offers simultaneously with different comp structures (public RSUs, private options, cash-heavy). Build total comp models. Practice negotiation conversations.
*   **Expert — Career Portfolio Review:** Map your last 3 roles as investments. What did each contribute to your skills, network, brand, and compensation? Identify the gap in your portfolio. Design your next move to fill it.
*   **Master — Compensation Data Collection:** Build a personal compensation database. Track every inbound recruiter message with stated comp range for 6 months. Collect: company, role, level, location, base, bonus%, equity type (RSU/options), equity value range. After 30+ data points, you'll have a precise calibration of your market value — more accurate than any website. Then negotiate a real offer using only this database as your evidence. Compare: did you get more than the data said you should? Why or why not?
*   **Elite — Reverse-Interview the Company:** In your next interview process, treat every conversation as a two-way evaluation. Before each interview, write down 3 things you need to learn about the company/team/role to make a decision. After the interview, rate each answer 1-5. After the full loop, tally the scores. If the company scores below your threshold (set it before you start), walk away — even if they make an offer. The discipline of rejecting offers that don't meet your standards is the difference between intentional career builders and reactive job takers.
*   **World-Class — Build Your Personal Advisory Board:** Identify 5-7 trusted advisors across different dimensions: (1) someone who's 5-10 years ahead in your career path, (2) a peer at a similar stage for mutual accountability, (3) someone from a different industry for outside perspective, (4) a former manager who championed you, (5) a recruiter who understands your market. Meet with each quarterly. Share your career decisions before you make them. The collective wisdom of 5 people who know you and your industry outperforms any individual's judgment — including your own.

## Verification

- [ ] Target company list: 30-50 companies across A/B/C tiers with specific reasons for each
- [ ] LinkedIn profile: keyword-optimized headline, detailed about section, skills endorsed, "Open to Work" set appropriately
- [ ] Networking: outreach script tested on 5 people, response rate tracked, follow-up system in place
- [ ] Pipeline tracker: applications, responses, interviews, offers tracked with conversion metrics
- [ ] Total compensation model: built for each offer with 4 equity scenarios, benefits valuation, career trajectory estimate
- [ ] Negotiation script: prepared for 2-3 counter items with market data support
- [ ] Runway calculation: if considering quitting without offer, 12+ months runway confirmed
- [ ] Offer letter: received in writing, reviewed, signed, start date confirmed before resignation
- [ ] Backchannel references: 2-3 former direct reports of hiring manager contacted for confidential feedback on management style
- [ ] Brag document: accomplishments from current role documented with quantifiable metrics — ready for resume and negotiation
- [ ] Equity literacy: can explain ISOs vs NSOs vs RSUs, understand vesting schedule/cliff/acceleration, know post-termination exercise window, can model 3 equity valuation scenarios
- [ ] Decision matrix: non-financial factors (manager quality, growth trajectory, mission alignment, work-life balance, commute/remote policy) weighted and scored alongside compensation for each offer
- [ ] Post-acceptance plan: start date confirmed, onboarding docs received, 30/60/90-day plan drafted, professional goodbye messages to network prepared
- [ ] Counter-offer considered and rejected (or accepted with clear rationale): if current employer counters, documented reasons for leaving and evaluated whether counter-offer addresses root causes or just financial symptoms
- [ ] Search retro: documented what worked and what didn't — which channels produced the best leads, which outreach scripts had highest response rates, what interview feedback patterns emerged — so the next search starts from data, not scratch
- [ ] Network notified: professional contacts informed of new role after start date, LinkedIn updated, thank-you notes sent to everyone who provided referrals, informational interviews, or advice during the search
- [ ] Financial transition plan: benefits gap coverage (COBRA vs marketplace), 401k rollover decision, equity exercise window for departing employer (ISOs typically have 90-day post-termination exercise window), signing bonus allocation plan
- [ ] First 90 days mapped: onboarding goals defined, key stakeholders identified (schedule 1:1s with each in week 1), quick-win project scoped (deliverable within 30 days to build credibility)
- [ ] Compensation package documents saved: offer letter, equity grant details, benefits summary, signing bonus terms — all stored in personal files (not just work email) for future negotiation and tax purposes

## References

- **Total Compensation Model Template**: See [references/comp-model.md](references/comp-model.md)
- **Networking Scripts by Channel**: See [references/networking-scripts.md](references/networking-scripts.md)
- **Offer Evaluation Framework**: See [references/offer-evaluation.md](references/offer-evaluation.md)
- **LinkedIn Optimization Guide**: See [references/linkedin-guide.md](references/linkedin-guide.md)
- **Anti-Patterns**: See [references/anti-patterns.md](references/anti-patterns.md)
- **Calibration**: See [references/calibration.md](references/calibration.md)
- **Production Checklist**: See [references/checklist.md](references/checklist.md)
- **Error Decoder**: See [references/error-decoder.md](references/error-decoder.md)
- **Footguns**: See [references/footguns.md](references/footguns.md)
- **Scale Depth**: See [references/scale-depth.md](references/scale-depth.md)
- **Sub-Skills**: See [references/sub-skills.md](references/sub-skills.md)
