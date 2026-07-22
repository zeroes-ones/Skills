---
name: ceo-strategist
description: CEO field manual covering vision, fundraising, board management, competitive strategy, org design, OKRs, crisis management, executive hiring, M&A, metrics dashboards, and personal effectiveness.
  Use when making company-defining decisions, raising capital, designing organizations, navigating crises, or scaling from seed to enterprise.
author: Sandeep Kumar Penchala
type: strategy
status: stable
version: 1.0.0
updated: 2026-07-21
tags:
- ceo-strategist
chain:
  consumes_from:
  - accountant
  - bizdev-manager
  - board-manager
  - business-strategist
  - cto-advisor
  - fp-and-a-analyst
  - hr-manager
  - investor-relations
  - legal-advisor
  - product-strategist
  - treasury-manager
  - vp-engineering
  feeds_into:
  - board-manager
  - fp-and-a-analyst
  - hr-manager
  - investor-relations
  - treasury-manager
  - vp-engineering
token_budget: 3285
output:
  type: code
  path_hint: ./
---
# CEO Strategist — The Operator's Field Manual

Executive-level strategy for company formation, fundraising, organizational design, and governance. Think like a founder/CEO making resource-constrained decisions under uncertainty.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces. Violating any of them produces bad advice.

- **Never invent numbers.** If you don't have actual revenue, burn rate, headcount, or market data for the user's company, ask for it or state your assumptions explicitly with a range. "A typical Series A SaaS company might have..." is fine. "Your company should raise $5M" is not — you don't know.
- **Never present a guess as fact.** Use phrases like "typical range is...", "many companies at this stage...", "one approach is...". Never say "the right answer is..." without evidence.
- **Always suggest validation.** Every strategic recommendation should include: "Verify this against [specific data source or person]." For example: "Verify pricing against what competitors actually charge, not what they list on their website."
- **Context trumps frameworks.** Frameworks (Porter, SWOT, etc.) are tools, not answers. If the user's specific situation contradicts a framework, the framework is wrong, not the user.
- **Admit what you don't know.** If a question requires data you don't have access to (current market conditions, specific competitor financials, regulatory changes from last week), say so and tell the user where to find it.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->

What are you trying to do?
├── Raise capital
│   ├── Should I raise VC? → Jump to "Decision Trees > Fundraising: Should You Raise VC?"
│   └── How much to raise? → Go to "Fundraising Cost by Round"
├── Design the organization
│   ├── Team structure by size → Jump to "Decision Trees > Organization Design by Team Size"
│   └── Hiring plan → Go to "Core Workflow > Phase 3: Organization and Talent"
├── Set strategy & vision → Start at "Core Workflow > Phase 1: Strategic Alignment and Vision"
├── Manage the board → Go to "Core Workflow > Phase 4: Governance and Reporting"
├── Navigate a crisis → Jump to "Core Workflow > Phase 5: Execution Cadence and Crisis Readiness"
├── Evaluate M&A → Go to "Sub-Skills" (mergers-and-acquisitions, buy-side-diligence)
├── Plan equity & cap table → Jump to "Equity & Cap Table"
├── Compete effectively → Go to "Core Workflow > Phase 1" + "Cross-Skill Coordination"
├── Need business model design or GTM strategy? → `business-strategist`
├── Need product strategy or roadmap planning? → `product-strategist`
├── Need technology strategy or build-vs-buy analysis? → `cto-advisor`
├── Need board governance or investor updates? → `board-manager`
└── Don't know where to start? → Run "Core Workflow > Phase 1: Strategic Alignment and Vision"

Do not read the entire skill. Follow the route above and read only the sections it points to.

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Fundraising strategy: when to raise, how much, from whom
- Organizational design: team structure by stage and size
- Equity and cap table planning: founder splits, employee option pools, dilution modeling
- Board governance: composition, meeting cadence, fiduciary duties
- Business model validation and pivoting decisions
- M&A evaluation: buy-side and sell-side strategy
- Company-building through MVP → Growth → Scale phases


### Cross-skills Integration

This skill in a typical workflow chain:

| Step | Skill | What it produces for this skill |
|------|-------|---------------------------------|
| **Before** | business-strategist | Financial model, GTM strategy, market sizing — informs fundraising and resource allocation decisions |
| **This** | ceo-strategist | Strategic vision, fundraising plan, org design, board governance framework, crisis playbook |
| **After** | product-strategist | Consumes strategic vision and resource allocation to set product direction and OKRs |

Common chains:
- **Vision to execution**: ceo-strategist → product-strategist → cto-advisor — Company vision → product strategy → technology roadmap
- **Fundraising**: business-strategist → ceo-strategist → legal-advisor — Financial model → investor narrative → term sheet review
- **Org design**: ceo-strategist → cto-advisor → project-manager — Org structure → engineering org design → team planning
- **M&A**: ceo-strategist → legal-advisor → business-strategist — Acquisition thesis → due diligence → integration model

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->
When this skill is invoked, drill into these specialized areas as needed:

| Sub-Skill | When to Use | Reference |
|-----------|-------------|-----------|
| `fundraising-strategy` | Raising any round (pre-seed → Series C+) | This file — Fundraising sections |
| `board-management` | Board meetings, governance, investor relations | This file — Equity & Cap Table section |
| `org-design` | Hiring first 10, scaling to 100, 500+ | This file — Organization Design section |
| `competitive-strategy` | Market entry, pivot, defending competitors | `references/` (see business-strategist) |
| `crisis-management` | PR crisis, security breach, down round, co-founder conflict | This file — Anti-Patterns section |
| `m-and-a-strategy` | Acquiring or being acquired | `references/` (create as needed) |
| `vision-to-execution` | Translating 5-year vision to quarterly OKRs | This file — MVP-to-Scale section |

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### Fundraising: Should You Raise VC?

```
Are you solving a venture-scale problem? (TAM > $1B?)
├── NO → Don't raise VC. Bootstrap, angel, or revenue finance.
│         VC requires 10x+ return. $50M exit = failure for VC.
└── YES → Can you grow 3x+ year-over-year?
    ├── NO → Don't raise VC. Growth equity or strategic investors.
    └── YES → Is the market timing right? (category is hot?)
        ├── NO → Wait. Raise when you have momentum.
        └── YES → Raise. But only what you need for 18-24 months.
```


**What good looks like:** An investor or new hire reads the strategy document and can explain the company's core thesis, target market, and 12-month priorities in under 60 seconds. Cap table is clean with 18-month runway across 3 funding scenarios. Every key role has a named owner and the next 2 hires are budgeted. Board meeting produces decisions, not debate.
### When NOT to Raise VC
- [ ] TAM < $1B (VCs need massive outcomes to return their fund)
- [ ] You want to run a lifestyle business ($1-5M ARR, profitable)
- [ ] You can reach profitability within 12 months on existing cash
- [ ] You're in a niche market that won't grow beyond $50M
- [ ] You value full control over company direction
- [ ] Your growth rate is <20% YoY (VCs want 3x+)

### Organization Design by Team Size

| Team Size | Structure | Management Layers | Key Hire | Monthly Burn (US) |
|-----------|----------|-------------------|----------|-------------------|
| **1-5** (MVP) | Everyone does everything. No managers. | 0 | Founding engineer | $40K-80K |
| **5-15** (Seed) | 1-2 functional leads. CEO still product. | 0-1 | First sales hire | $80K-150K |
| **15-30** (Series A) | Functional teams: eng, product, GTM. | 1-2 | VP Engineering or Head of Sales | $200K-400K |
| **30-80** (Series B) | Departments with directors. CEO delegates. | 2-3 | CFO/COO | $500K-1.2M |
| **80-200** (Series C+) | VPs with directors under them. COO runs ops. | 3-4 | CPO, CRO | $1.5M-4M |

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~20 min): Strategic Alignment and Vision
1. Articulate the 3-year vision: what does success look like? What must be true for the company to win?
2. Translate vision into annual strategic pillars (3-5 max). Each pillar must have a measurable outcome.
3. Derive quarterly OKRs: 3-5 objectives with 3-5 key results each. KRs must be outcome-based, not activity-based.
4. Socialize with leadership team. Pressure-test assumptions. Identify the "one thing" that would kill the plan.
5. Document in a strategy memo (2 pages max). Circulate to board and entire company.

### Phase 2 (~15 min): Resourcing and Capital Allocation
1. Map strategic pillars to required resources: headcount, budget, time, executive attention.
2. Identify the binding constraint: is it engineering capacity, sales pipeline, capital, or market timing?
3. Run a "zero-based" exercise: if starting from scratch, would you allocate resources the same way? Cut what wouldn't survive.
4. Determine funding needs: runway in months, burn rate, hiring plan, contingency buffer (20% minimum).
5. Build a financial model with best/base/worst case scenarios. Stress-test against losing your top customer or key hire.

### Phase 3 (~20 min): Organization and Talent
1. Design the org chart for the next 12 months, not today. What roles will you need at the next funding milestone?
2. Identify the top 3 hires that will unlock the next phase. Write job descriptions with success criteria.
3. Evaluate current team: who has outgrown their role? Who needs support? Is there a single point of failure?
4. Define compensation philosophy: salary bands by role/level, equity refresh policy, performance review cadence.
5. Plan for culture scaling: what values are non-negotiable? How will you preserve them as you double headcount?

### Phase 4 (~15 min): Governance and Reporting
1. Set board meeting cadence (quarterly minimum, monthly during crises). Define board packet contents.
2. Establish a company-wide metric dashboard: revenue, burn, runway, CAC, LTV, churn, NPS, headcount.
3. Define decision rights: which decisions require CEO approval vs. VP discretion? Document in a RACI matrix.
4. Create an escalation framework: what constitutes a "CEO must know immediately" event vs. weekly update?
5. Schedule skip-level 1:1s with key ICs quarterly. Information bottlenecks kill companies.

### Phase 5 (~25 min): Execution Cadence and Crisis Readiness
1. Establish operating rhythm: weekly leadership standup (30 min), monthly business review (2 hrs), quarterly offsite (full day).
2. Run a pre-mortem: "It's 12 months from now, we failed. What happened?" — then build mitigations into the plan.
3. Define crisis triggers: down round, co-founder departure, major customer loss, security breach, regulatory action.
4. For each crisis trigger, pre-designate a response owner, communication template, and first 24-hour action plan.
5. Review quarterly: what got done vs. committed? What did we learn? What changes for next quarter?

## MVP-to-Scale Progression

| Phase | Fundraising | Valuation Driver | Monthly Cost |
|-------|------------|-----------------|--------------|
| **Pre-Seed** ($500K-2M) | Angel/accelerator | Team quality, market size | $30K-60K/mo |
| **Seed** ($2-5M) | Seed funds, angels | Early traction, PMF signals | $80K-150K/mo |
| **Series A** ($8-20M) | Tier 1/2 VCs | Revenue growth rate, retention | $200K-400K/mo |
| **Series B** ($20-50M) | Growth funds | Efficient growth, unit economics | $500K-1M/mo |
| **Series C+** ($50M+) | Late-stage, PE | Path to profitability, market leadership | $1.5M+/mo |

## Fundraising Cost by Round

| Round | Typical Raise | Dilution | Legal Cost | Time to Close |
|-------|-------------|----------|-----------|---------------|
| Pre-Seed (SAFE) | $500K-2M | 10-20% (cap dependent) | $5K-15K | 4-8 weeks |
| Seed (Priced) | $2-5M | 15-25% | $30K-60K | 8-12 weeks |
| Series A | $8-20M | 18-25% | $60K-120K | 12-16 weeks |
| Series B | $20-50M | 15-20% | $100K-200K | 12-16 weeks |
| Series C | $50M+ | 10-15% | $200K-400K | 12-20 weeks |

**Fundraising math:** A successful fundraise takes 3-6 months full-time for CEO. At $200K/year opportunity cost, a 4-month raise costs $67K in lost CEO time PLUS legal costs.

## Equity & Cap Table

### Option Pool Sizing
| Stage | Pool Size | Notes |
|-------|-----------|-------|
| Pre-Seed | 10-15% | Larger pool = less dilution at next round |
| Seed | 10-15% | Refresh pool before priced round |
| Series A | 15-20% | VCs will require this; refresh pre-money |
| Series B+ | 10-15% | Ongoing refresh for key hires |

### Employee Equity by Role (Seed/Series A)
| Role | Equity Range |
|------|-------------|
| CTO (co-founder) | 10-30% (4-year vest, 1-year cliff) |
| VP Engineering (#1-5 hire) | 1-3% |
| Senior Engineer (#5-20) | 0.2-0.5% |
| Engineer (#20+) | 0.05-0.2% |
| VP Sales | 0.5-2% |
| Head of Product | 0.5-1.5% |

## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->
The CEO sits at the center of all strategic decisions. Coordination failures here cascade into every function — product builds the wrong thing, engineering builds it wrong, sales sells to the wrong market.

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `business-strategist` | Financial model, GTM strategy, market sizing (TAM/SAM/SOM), unit economics, pricing model | During fundraising preparation; before board meetings; during annual strategic planning |
| `cto-advisor` | Technology strategy memo, build-vs-buy analysis, engineering capacity assessment, technical debt report | Before major build-vs-buy decisions; during engineering org restructuring |
| `product-strategist` | Product vision, PMF assessment, OKR draft, competitive analysis, roadmap scenario | Before quarterly OKR planning; during pivot evaluation |
| `fp-and-a-analyst` | Cash runway projections, burn rate analysis, revenue forecast, scenario models | Before fundraising; monthly finance review; during budget allocation |
| `board-manager` | Board deck feedback, investor sentiment signals, governance recommendations, prep notes | Before quarterly board meetings; during governance restructuring |
| `legal-advisor` | Term sheet analysis, IP strategy, regulatory exposure assessment, co-founder agreement review | Before fundraising close; during M&A evaluation; when regulatory threat emerges |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `board-manager` | Strategic vision, financial summary, KPI dashboard, capital allocation plan, risk register | Board meets without context — wasted meetings, eroded investor confidence |
| `investor-relations` | Fundraising narrative, cap table, growth metrics, milestone roadmap, use-of-funds plan | Investors receive incomplete story — fundraising round delayed or undersubscribed |
| `vp-engineering` | Org design parameters, hiring budget, strategic priorities, technical investment thesis | Engineering builds without strategic context — misaligned architecture and resourcing |
| `hr-manager` | Culture vision, org chart, compensation philosophy, diversity targets, leadership gaps | Hiring and retention policies disconnect from company direction — talent churn |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Fundraising round opening | `cto-advisor`, `business-strategist`, `legal-advisor`, `fp-and-a-analyst` | Due diligence prep, data room, financial modeling, term sheet negotiation |
| Pivot decision | `cto-advisor`, `product-strategist`, `board-manager` | Architecture replanning, roadmap overhaul, investor communication |
| Co-founder departure/conflict | `legal-advisor`, `board-manager`, `hr-manager` | Equity implications, leadership gap, team morale, retention risk |
| Cash running below 6 months runway | `fp-and-a-analyst`, `board-manager`, `cto-advisor` | Emergency fundraising, cost cutting, hiring freeze decisions |
| Major customer loss (>10% revenue) | `product-strategist`, `board-manager` | Churn analysis, product gaps, competitive threat response |
| Acquisition offer received | `legal-advisor`, `board-manager`, `cto-advisor`, `fp-and-a-analyst` | Due diligence, valuation, integration feasibility, cap table analysis |
| Regulatory/legal threat | `legal-advisor`, `board-manager` | Risk assessment, PR strategy, operational changes, board communication |
| Key hire (VP-level) accepted/rejected | `vp-engineering`, `hr-manager`, `board-manager` | Org chart changes, onboarding plan, backup strategy |

### Escalation Path

```
Board level (existential risk: runway < 3mo, lawsuit, co-founder exit, acquisition offer)
  └── CEO handles directly. No delegation. Board convened within 48 hours.

Executive level (strategic: pivot, fundraising, major customer loss)
  └── `ceo-strategist` + relevant C-level (`cto-advisor`, `fp-and-a-analyst`). Decision within 1 week. Board informed.

Functional level (tactical: org change, process issue, vendor decision)
  └── Functional lead handles. `ceo-strategist` informed via weekly sync. No escalation needed.
```

## Best Practices
<!-- STANDARD: 3min -- operational principles for the CEO role -->
- **Strategy before execution**: Spend 20% of your time on strategy. Without it, you optimize the wrong thing. Annual offsite for long-range planning; quarterly reviews to adjust.
- **Cash is oxygen**: Never let runway drop below 6 months without raising the alarm. Model conservatively — assume revenue takes 2x longer and costs 1.5x more than projected.
- **Hire for the company you're building, not the one you have**: Seed-stage needs generalists who thrive in chaos. Growth-stage needs specialists who build process. Don't hire a VP of Sales when you haven't figured out how to sell yourself.
- **Founder vesting is non-negotiable**: 4-year vesting with 1-year cliff for ALL founders. Without it, a departing co-founder walks away with equity they didn't earn, dooming future fundraising.
- **Board seats are permanent decisions**: Every board member shapes strategy, hires/fires the CEO, and influences the next round. Choose investors who add value beyond capital — network, domain expertise, operator experience.
- **Culture compounds**: The values you tolerate in employee #5 become the culture at employee #50. Fire toxic A-players fast — the cost of keeping them (attrition, morale, reputational damage) exceeds their output.
- **Default to transparency**: Share board decks with the entire company (redact only compensation and legal). Informed employees make better decisions. Surprises breed distrust.
- **The CEO's job changes every 12 months**: What made you effective at 5 people (doing everything) makes you a bottleneck at 50. Deliberately hand off functions as the company scales — product, then engineering, then sales, then operations.
- **Your calendar is your strategy**: If 80% of your time is internal meetings, nobody is focused on customers, recruiting, or fundraising. Audit your calendar monthly — cut or delegate anything that doesn't require the CEO.
- **Pre-mortem every major decision**: Before a big hire, fundraising round, or pivot, ask "If this fails, what was the root cause?" Design mitigations before you start, not after you're committed.
- **Founder conflict kills more startups than competition**: Address co-founder tension early. Use a coach or facilitator. Have a pre-agreed decision framework for impasses: who decides what, and what happens if you still disagree?

## Scale Depth: Solo → Small → Medium → Enterprise

### Solo (1 person, 0-100 users)
- **What changes**: You are the CEO, CFO, and COO. Fundraising = friends & family or bootstrapping. Org design = just you + maybe a co-founder. Board = informal advisory chats.
- **What to skip**: Venture capital entirely. Cap table software. Formal board meetings. 409A valuations. Org charts.
- **Coordination**: None needed. Talk to customers directly.

### Small Team (2-10 people, 100-10K users)
- **What changes**: Pre-seed/Seed fundraising begins. Simple cap table on Carta/Pulley. Board of 3 (2 founders + 1 lead investor). First hires — generalists who wear multiple hats. 409A for option pricing.
- **What to skip**: Series A prep. Independent board members. Executive hires (stay functional leads). Complex option structures.
- **Coordination**: Weekly all-hands (30 min). Monthly board updates (1-pager). Bi-weekly 1:1s with each report.

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: Series A/B fundraising ($5M-$30M). Independent board member. First exec hires (VP Eng at 25+, VP Sales at 30+). Department structure emerges. Employee option pool at 15-20%. Performance review cycles.
- **What to skip**: Series C prep at <$10M ARR. Multi-class share structures. Full C-suite (CFO/COO can wait).
- **Coordination**: Quarterly board meetings with full deck. Monthly leadership offsite. Bi-weekly department leads sync.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Series C+ ($30M+). Professional board (5-7 members, majority independent). Full C-suite. Audit committee. Compensation committee. SOX readiness at IPO path. Multi-class shares for founder control. Secondary sales for employee liquidity.
- **What's full production**: Quarterly board with formal packages. Annual shareholder meeting. 409A every 12 months. D&O insurance. Investor relations function.
- **Coordination**: Formal board calendar. Quarterly earnings-style updates. Annual strategy offsite.

### Transition Triggers
- **Solo → Small**: You have paying customers and cannot build + sell + support alone anymore. Revenue > $50K ARR.
- **Small → Medium**: You're hiring specialists (not just generalists). Burn rate requires institutional capital. Revenue > $2M ARR.
- **Medium → Enterprise**: Board demands independent governance. IPO/liquidity event within 24 months. Revenue > $20M ARR.


### War Story 1 — The Bridge Round That Cost the Company
**Symptom:** CEO of a growing SaaS company started Series A fundraising with 4 months of runway. Term sheets took 10 weeks to materialize. By week 9, payroll was at risk. The only offer came at a 40% discount to the last round with cram-down terms.
**Root cause:** The CEO waited for "the right metrics" to improve before starting the raise. By the time metrics were ready, runway was critical. Investors sensed desperation and lowballed.
**Fix:** Instituted a board policy: CEO must begin next fundraise when runway hits 10 months, regardless of metric perfection. Second round: started with 11 months runway, closed 3 term sheets in 6 weeks at much better terms.
**Lesson:** Fundraising leverage is 80% timing, 20% metrics. A B+ round with 10 months runway beats an A round with 4 months runway. Start fundraising before you need to — the best time to raise is when you don't need the money.

### War Story 2 — The Org Chart That Almost Killed Velocity
**Symptom:** CEO of a 45-person company reorganized from functional teams (frontend, backend, design) to stream-aligned teams (checkout, search, account management). For 2 months, velocity dropped 60%. Death-spiral talk began.
**Root cause:** The reorganization was announced Monday, effective Monday. No transition plan, no interim team leads, no clear ownership of in-flight work. Engineers spent 3 weeks figuring out who owned what.
**Fix:** Implemented a phased org transition model: announce 2 weeks early, appoint interim leads before the reorg, create a dependency register for in-flight work, run a 2-week "stabilization sprint" before new feature work began.
**Lesson:** Org redesigns are architecture changes, and architecture changes take time. Plan for a 6-week dip in velocity. Over-communicate during it. The dip is temporary; the wrong org structure is permanent.

### War Story 3 — The Co-Founder We Didn't Fire Soon Enough
**Symptom:** A CTO co-founder stopped being productive 12 months in but retained 25% equity. The company couldn't raise Series A because investors flagged the cap table as "toxic." The only fix was buying back shares at a painful valuation.
**Root cause:** No vesting schedule on the founder agreement. The co-founder had walked with unvested-but-issued shares. The remaining founders spent 6 months and $80K in legal fees negotiating a buyback.
**Fix:** Every subsequent founder agreement included: 4-year vesting with 1-year cliff, double-trigger acceleration, IP assignment tied to vesting, and a bad-actor buyback clause at fair market value or $0.
**Lesson:** Founder agreements without vesting are not agreements — they're lawsuits waiting to happen. A $5K lawyer session pre-incorporation saves $80K+ and untold relationship damage. Vesting is not optional.


### Error Decoder
<!-- DEEP: 10+min -->

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Market timing wrong | Product launched too early (no demand) or too late (crowded) | Run demand validation with 10+ paid pre-orders before building; use Wardley Map to time your entry | Timing risk is invisible from inside the building. Validate demand with money (pre-orders), not words (surveys). Wardley Maps show market evolution — use them before committing. |
| Team can't execute | Key hires missing, wrong incentives, no clear owner | Hire for the next 6 months' problems, not the last 6 months'; DRI model with written OKRs | Hiring for yesterday fixes nothing. One clear owner per initiative eliminates the diffusion of responsibility that kills execution. |
| Runway < 12 months | Burn rate exceeds plan, revenue slower than projected | Cut burn to 18-month runway immediately; model best/worst/realistic case scenarios | Cash is the CEO's only non-negotiable. 18 months of runway buys leverage in fundraising; 4 months buys desperation terms. Fundraise before you need to. |
| Investor pass | Pitch doesn't articulate defensible moat | Lead with TAM → problem → traction → team → ask. Your demo is not your pitch. | Investors are buying a monopoly thesis in a growing market. If you cannot explain your moat in one sentence, your pitch is incomplete. |
| Board misalignment | Founder/board disagree on strategy | Pre-board one-on-ones before every board meeting. Surface disagreement in the room, not after. | Board meetings are for decisions, not surprises. Alignment is built in prep calls, not broken in the boardroom. |
| Scaling prematurely | Growing team/features before PMF | Sean Ellis test: < 40% "very disappointed" if product disappeared → do not scale | Growth before PMF multiplies problems, not revenue. The Sean Ellis test costs nothing but saves millions. |
| Co-founder conflict | Roles, equity, or vision disagreement | Written founder agreement with vesting, roles, decision rights, and exit terms | Handshakes are not contracts. A written founder agreement is the most important legal document you will sign — it protects the relationship, not just the company. |


## What Good Looks Like

> You've just completed the CEO strategy exercise. Your cap table is clean, dilution is modeled through Series B, and your 409A is current. You can articulate your vision in one sentence that makes investors lean forward, not check their phones. Your fundraising pipeline has 30+ warm-intro targets ranked by thesis fit, and your data room answers every question before it's asked. The org chart doesn't just solve today's problems — it's designed for the company you'll be in 18 months. Your co-founders have signed agreements covering vesting, IP, decision rights, and the hard conversation you hope you never have.


## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
- [ ] **[S1]**  Cap table modeled with dilution at each round (use Carta/Pulley)
- [ ] **[S2]**  18-24 month runway modeled with hiring plan and burn rate
- [ ] **[S3]**  Board composition planned with independent director identified
- [ ] **[S4]**  Employee option pool sized correctly for hiring plan
- [ ] **[S5]**  Fundraising materials: pitch deck, financial model, data room
- [ ] **[S6]**  Investor pipeline: 30+ target investors per round
- [ ] **[S7]**  Org chart designed for next 2 phases (MVP → Growth → Scale)
- [ ] **[S8]**  Key person risk mitigated: no single employee is irreplaceable
- [ ] **[S9]**  Founder agreement signed: vesting, IP assignment, decision rights
- [ ] **[S10]**  409A valuation completed for option pricing

## References
<!-- QUICK: 30s -- links to deeper reading -->
- Related: `cto-advisor`, `business-strategist`, `product-manager`
- Books: Venture Deals (Feld & Mendelson), The Hard Thing About Hard Things (Horowitz), High Growth Handbook (Gil)
