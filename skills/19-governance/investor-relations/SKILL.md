---
name: investor-relations
description: Investor relations and fundraising operations for founders and CFOs. Covers investor CRM management, fundraising process, data room preparation, pitch deck creation, due diligence, cap table modeling, annual meetings, shareholder reporting, secondary transactions, and IR during crises. Use when raising capital, managing investor communications, or navigating down rounds and tender offers.
author: Sandeep Kumar Penchala
type: governance
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - investor-relations
  - fundraising
  - cap-table-management
  - pitch-deck
  - data-room
  - shareholder-reporting
  - secondary-transactions
token_budget: 3490
output:
  type: "document"
  path_hint: "./investor-relations/"
chain:
  consumes_from:
    - board-manager
    - ceo-strategist
    - fp-and-a-analyst
  feeds_into:
    - legal-advisor
    - ceo-strategist
---
# Investor Relations — The Fundraising Operating System

Investor relations and fundraising operations for founders, CEOs, and CFOs. Run efficient fundraises, manage investor communications at scale, handle due diligence, model dilution scenarios, and navigate the hardest IR moments — down rounds, tender offers, and crisis disclosures.

## Ground Rules — Read Before Anything Else

- **Never recommend a raise amount without runway math.** "Raise $10M" without knowing burn rate, revenue, and growth rate is malpractice. You need: monthly burn, cash on hand, projected revenue, hiring plan, and time to next milestone.
- **Investor updates are not optional.** If you miss a monthly update, investors assume bad news. Silence = crisis in IR. Send updates even when the news is terrible — especially when it's terrible.
- **The data room IS the diligence process.** A disorganized data room adds 2-4 weeks to a fundraise and signals operational weakness. A tight data room closes faster.
- **Term sheets are not commitments.** A signed term sheet can still blow up. Never stop talking to other investors until the wire hits. The "no-shop" period between term sheet and close is when deals die.
- **Cap table errors compound.** A 1% error at Seed becomes a 5% error at Series C. Audit your cap table quarterly with a lawyer. Use Carta or Pulley — spreadsheets kill companies.
- **Assume every investor email will leak.** Don't put anything in writing you wouldn't want a competitor, a journalist, or a future acquirer to see.

## Route the Request
<!-- QUICK: 30s — pick your path, skip the rest -->

What are you trying to do?
├── Start a fundraise → Jump to "Core Workflow > Phase 1: Fundraising Preparation"
├── Build a data room → Go to "Decision Trees > Data Room Checklist"
├── Create a pitch deck → Jump to "Core Workflow > Phase 2: Pitch Deck Construction"
├── Manage investor pipeline → Go to "Core Workflow > Phase 3: Pipeline Management"
├── Compare term sheets → Jump to "Decision Trees > Term Sheet Comparison Framework"
├── Prepare for investor due diligence → Go to "Core Workflow > Phase 4: Due Diligence"
├── Model cap table scenarios → Jump to "Decision Trees > Cap Table Scenario Modeling"
├── Send an investor update → Go to "Core Workflow > Phase 5: Investor Communications"
├── Run a secondary transaction → Jump to "Decision Trees > Secondary Transaction Types"
├── Handle a down round → Go to "Error Decoder" — last row, then "Crisis IR Playbook"
└── Don't know where to start? → Run "Core Workflow > Phase 1"

Do not read the entire skill. Follow the route above.

## When to Use
<!-- QUICK: 30s — scan the bullet list to decide if this skill fits -->
- Launching a fundraising process: strategy, materials, pipeline, close
- Building and managing a data room: what goes in, what stays out, how to organize
- Creating or refining a pitch deck: story arc, traction slides, market sizing, competitive positioning
- Managing the investor pipeline: CRM setup, tracking conversations, follow-up cadence
- Comparing term sheets: price, liquidation preference, participation, anti-dilution, board seats, protective provisions
- Running investor due diligence: tech DD, financial DD, customer references, background checks
- Modeling cap table scenarios: dilution, option pool expansion, liquidation waterfalls
- Sending monthly/quarterly investor updates: metrics that matter, good news/bad news format
- Preparing for annual shareholder meetings and proxy statements
- Coordinating secondary transactions: tender offers, direct secondaries, founder liquidity
- Managing IR during crises: down rounds, layoffs, product incidents, co-founder departures

<!-- STANDARD: 3min -->
### When NOT to Use This Skill
- You're pre-revenue and raising from friends & family (use `ceo-strategist` — this is institutional fundraising infrastructure)
- You need legal review of a term sheet (use `legal-advisor` — this skill helps you compare terms, not negotiate them)
- You're building the underlying financial model (use `fp-and-a-analyst` for the model; come here to package it for investors)

## Decision Trees
<!-- QUICK: 30s — follow the ASCII tree to your scenario -->

### Data Room Checklist — The 14 Folders Every Fundraise Needs
<!-- STANDARD: 3min -->

```
data-room/
├── 01-corporate-docs/
│   ├── Certificate of Incorporation (and amendments)
│   ├── Bylaws
│   ├── Board consents and minutes (last 2 years)
│   ├── Stockholder consents
│   └── Subsidiary org charts (with jurisdictional notes)
├── 02-cap-table/
│   ├── Pro forma cap table (fully diluted, with ESOP)
│   ├── 409A valuation report (current, within 12 months)
│   ├── Option grant history (date, strike price, vesting schedule)
│   └── Convertible instruments (SAFEs, notes, warrants — conversion terms and amounts)
├── 03-financials/
│   ├── Audited financials (last 2 years, if applicable)
│   ├── Unaudited interim financials (current year, monthly)
│   ├── Annual budget and quarterly forecasts
│   ├── Revenue by customer (anonymized, top 20 accounts)
│   ├── Cohort analysis (retention by cohort, logo and dollar-based)
│   └── Gross margin by product line
├── 04-product-tech/
│   ├── Architecture diagram (high-level, 1 page)
│   ├── Product roadmap (current + next 4 quarters)
│   ├── Tech debt assessment (with remediation plan)
│   ├── Security certifications (SOC 2, ISO 27001, pen test reports)
│   └── IP portfolio (patents filed/granted, trademarks, key licenses)
├── 05-gtm-sales/
│   ├── ICP and buyer persona documentation
│   ├── Pricing and packaging (current and planned)
│   ├── Sales playbook and comp plan
│   ├── Pipeline data (by stage, rep, vertical — last 4 quarters)
│   └── Win/loss analysis (last 20 deals)
├── 06-customer-reference/
│   ├── Referenceable customer list (name, contact, relationship notes)
│   ├── Case studies (3-5, with metrics)
│   └── NPS/CSAT data (rolling 12 months)
├── 07-market-competitive/
│   ├── TAM/SAM/SOM analysis (bottoms-up, with sources)
│   ├── Competitive landscape (with differentiation matrix)
│   └── Industry analyst reports (Gartner, Forrester — if available)
├── 08-people-culture/
│   ├── Org chart (current + planned 12 months)
│   ├── Headcount by department (with hiring plan)
│   ├── Employee NPS and engagement data
│   └── Key employee retention agreements
├── 09-legal-compliance/
│   ├── Material contracts (customer >$100K, vendor >$50K, partnership)
│   ├── Litigation summary (pending, threatened, settled — with counsel letter)
│   ├── Employment and IP assignment agreements (templates)
│   └── Regulatory filings and correspondence
├── 10-board-investor/
│   ├── Board meeting minutes (last 2 years)
│   ├── Investor update history (last 8 quarters)
│   └── Current investor contact list with ownership percentages
├── 11-fundraising/
│   ├── Pitch deck (current version, PDF)
│   ├── Financial model (Excel/Google Sheets, not PDF — they will model with it)
│   ├── Management bios and LinkedIn profiles
│   └── FAQ document (pre-empt the top 20 diligence questions)
├── 12-customer-contracts/
│   ├── Master Services Agreement (template)
│   └── Top 10 customer contracts (redacted for confidentiality, with counsel approval)
├── 13-vendor-partnerships/
│   └── Key vendor and partnership agreements
└── 14-tax-compliance/
    ├── Federal and state tax returns (last 2 years)
    ├── R&D tax credit documentation
    └── Sales tax compliance status by jurisdiction
```

**War story:** A Series B company sent their data room link to 40 investors. One folder — "06-customer-reference" — contained an Excel file with customer names, contact info, AND annual contract values, unredacted. An associate at a VC firm shared it with a competitor's CEO (their portfolio company). The competitor used the pricing data to undercut renewals. The startup lost 3 of their top 10 accounts within 6 months. Lesson: every document in the data room goes through counsel review before investor access. Revenue data is never customer-attributed in a data room.

### Term Sheet Comparison Framework
<!-- STANDARD: 3min -->

When comparing two term sheets, rank these 6 dimensions. Valuation is #4 on this list — not #1.

| Priority | Term | What to Look For | Red Flag |
|----------|------|-----------------|----------|
| 1 | **Liquidation Preference** | 1x non-participating is market. >1x or participating = red flag. | 2x participating preferred — investor gets paid twice before common sees a dollar |
| 2 | **Board Control** | Common + investor balance. Independent director breaks ties. | Investors control majority of board seats without an independent director |
| 3 | **Protective Provisions** | Standard: approve new financing, amend charter, sell company, change board size | Veto over budget, hiring, or customer contracts — investors are managing, not governing |
| 4 | **Valuation** | Higher = less dilution. But a clean $40M cap is better than a dirty $60M with 3x participating. | Valuation so high it makes the next round unwinnable (the "valuation trap") |
| 5 | **Option Pool** | 10-20% unallocated post-money. Pool should be pre-money (investor shares dilution). | Pool is post-money and too small — founders get diluted again at next round to refresh |
| 6 | **Anti-Dilution** | Weighted average (broad-based). | Full ratchet — if you raise a down round, investors get repriced. This destroys founder equity. |

**What good looks like:** A term sheet matrix where you can explain, in one sentence, why Term Sheet A is better than Term Sheet B despite the lower valuation. "Term Sheet A has a 1x non-participating liquidation preference and board balance, while Term Sheet B has 2x participating and investor board control — A leaves us with 3x more equity in a $100M exit."

### Cap Table Scenario Modeling
<!-- DEEP: 10+min -- cap table errors are irreversible -->

```
Model these 4 scenarios before every fundraise:

Scenario 1: Base Case (the round you're raising)
├── Pre-money: $[X]M | Raise: $[Y]M | Post-money: $[Z]M
├── Dilution: [%] per existing shareholder
└── New option pool: [%] of post-money (pre-money refresh vs. post-money)

Scenario 2: Down Round (30% below current valuation)
├── Full ratchet anti-dilution impact on founders vs. weighted average
├── Pay-to-play provisions: who gets washed out?
└── Liquidation preference stack: do common shareholders get anything in a fire sale?

Scenario 3: Exit Waterfall ($50M, $100M, $500M, $1B)
├── Liquidation preference payout order: Series B → Series A → Seed → Common
├── Participation cap: at what exit value does participating preferred convert to common?
└── Option holder payout: what do employees actually make at each exit threshold?

Scenario 4: Acquisition (stock vs. cash deal)
├── Cash: simple waterfall. Stock: what's the acquirer's stock worth? (and lockup period)
├── Earnout: how much is contingent? Who stays to earn it?
└── Retention packages: key employee retention carve-outs (don't come from common pool)
```

**War story:** A founder sold her company for $40M thinking she'd walk away with $8M (20% ownership). She got $0. Her Series B investors had 2x participating preferred with no cap. The $40M went: $15M to Series B liquidation preference + $15M participation + $8M to Series A preference + $2M to Seed preference = $40M. Common shareholders (founders + employees) received nothing. She had never modeled the liquidation waterfall. The acquirer's lawyers presented it at closing. Too late to negotiate.

## Core Workflow

### Phase 1 (~120 min): Fundraising Preparation
<!-- STANDARD: 3min -->
1. **Decide if you should raise** (15 min): 18+ months of runway? Growing 3x+ YoY? Category is investable? If any answer is "no," fix the business first. Raising without momentum = down round or no round at all.
2. **Set the raise parameters** (15 min): How much? For what? From whom? Raise enough for 24 months to the next value-inflection milestone. If your next milestone is $5M ARR and you're at $1M ARR growing 10% month-over-month, you need ~18 months → raise $X based on burn × 24.
3. **Build the target investor list** (30 min): 30-50 firms. Tiered: Tier 1 (top 10, your dream investors), Tier 2 (20 good fits), Tier 3 (20 backups). Research: who invested in adjacent companies? Who led rounds at your stage and sector in the last 12 months? Who has capacity? (Check fund size — a $1B fund doesn't lead $5M Seeds.)
4. **Prepare materials** (45 min): Pitch deck (see Phase 2), financial model, data room (see Decision Trees), management bios, reference customer list, FAQ doc.
5. **Warm introductions only** (15 min): Cold emails have a <1% response rate. Warm intros: 40-60%. Map your network → target investors. Ask existing investors, advisors, and portfolio company CEOs for introductions. One intro request per investor, with a blurb they can forward.

### Phase 2 (~90 min): Pitch Deck Construction
<!-- STANDARD: 3min -->
**The 12-slide narrative arc.** Every slide answers one question. No slide has >5 bullet points. No bullet point is >2 lines.

| Slide | Question It Answers | Content |
|-------|-------------------|---------|
| 1. Title | Who are you? | Company name, logo, tagline: "We do X for Y" — 8 words max |
| 2. Problem | Why does this matter? | The pain you solve. Use a customer quote, not a market stat. "I spend 4 hours a week manually reconciling..." beats "The TAM is $50B." |
| 3. Solution | How do you solve it? | Product screenshot or 30-second demo GIF. Show, don't tell. |
| 4. Why Now? | Why hasn't this been done? | Technology shift, regulatory change, behavioral change. "APIs didn't exist before 2023." "Remote work made this a top-3 pain." |
| 5. Market Size | How big can this get? | Bottoms-up TAM: how many customers × your ASP × penetration rate. Tops-down is backup. Show the beachhead and expansion. |
| 6. Traction | Is this working? | Revenue graph (MRR/ARR, month-by-month for 18+ months). Logo count. Key logos. Retention (logo and dollar-based net retention). |
| 7. Product | What have you built? | Current product, roadmap highlights, key metrics (DAU/MAU, engagement). Not a feature list — show what's defensible. |
| 8. Business Model | How do you make money? | Pricing model, ASP, sales motion (PLG vs. enterprise sales), CAC, LTV, payback period. Unit economics must be on this slide. |
| 9. Competition | Why will you win? | Competitive matrix: you vs. incumbents vs. startups across key dimensions. Your unfair advantage: data, network effects, switching costs, brand. |
| 10. Team | Why you? | Founders' photos, titles, 1-line bio (previous company, relevant achievement). Key hires. Why this team uniquely can solve this problem. |
| 11. Financials | What do the numbers look like? | 3-year revenue projection with assumptions. Headcount plan. Burn rate. Key metrics: gross margin, CAC payback, LTV/CAC. |
| 12. The Ask | What do you need? | "We're raising $X on a $Y pre-money valuation to achieve [milestone]." Use of funds: 50% engineering, 30% GTM, 20% G&A. |

**What good looks like:** A partner at a VC firm forwards your deck to another partner with the note "Take a look at this — interesting team and traction." You know you have it when you get partner-level meetings (not associate screens) within 1 week of intro.

### Phase 3 (~60 min setup + ongoing): Pipeline Management
<!-- STANDARD: 3min -->
1. **Set up investor CRM** (15 min): Use Affinity, Streak (Gmail), or a Notion/Airtable tracker. Fields: firm, contact name, role, intro source, date contacted, meeting date, stage (outreach → meeting 1 → partner meeting → term sheet → diligence → close), notes, next step.
2. **Run the process in batches** (ongoing): Week 1-2: Tier 1 outreach (10 firms). Week 3-4: Tier 1 meetings + Tier 2 outreach. Week 5-6: Partner meetings and term sheet conversations. Never have >15 active conversations at once — you'll lose track.
3. **Follow-up cadence** (ongoing): After meeting 1, send thank-you + any promised materials within 24 hours. If no response in 5 business days, follow up once. If still no response, move to "passive" and focus on active conversations. Silence is a pass.
4. **Signal management** (ongoing): When one Tier 1 investor shows strong interest ("We'd like to meet the full partnership"), use it as leverage: "We're in active conversations with [Firm A] and [Firm B] and expect term sheets in the next 2 weeks. We'd love to include you in the process."
5. **The close** (10 min post-term sheet): Signed term sheet → no-shop period (30-45 days) → legal diligence → definitive agreements → wire transfer. During no-shop: respond to all diligence requests within 24 hours. The #1 cause of blown-up deals: slow diligence response signals disorganization.

### Phase 4 (~90 min): Due Diligence
<!-- STANDARD: 3min -->
1. **Financial DD preparation** (30 min): Unaudited monthly financials for the current year. Customer-level revenue data (anonymized). Cohort retention analysis. Gross margin by product. All material contracts >$50K. Tax returns.
2. **Technical DD preparation** (30 min): Architecture overview (1-pager for non-technical investors). Tech debt register with severity and remediation plan. Security posture (SOC 2 report, penetration test results). IP ownership documentation (all code written by employees/contractors with IP assignment).
3. **Customer reference preparation** (15 min): Identify 5-8 referenceable customers. Pre-brief each: "A potential investor may call. Here's what they'll ask. Here's what we'd love you to emphasize." Never put a customer on a reference call without pre-briefing them.
4. **Background check readiness** (15 min): Every founder will be background checked. Disclose anything that will surface before it surfaces: prior lawsuits, bankruptcies, regulatory actions, academic credential discrepancies. Surprise in background check = deal killer.

**War story:** A founder didn't disclose a prior startup that had failed and been sued by its investors. The VC's background check found the lawsuit (public record). The VC pulled the term sheet — not because of the failure, but because the founder hid it. The failure was defensible. The concealment was not.

### Phase 5 (~30 min/month): Investor Communications
<!-- STANDARD: 3min -->

**Monthly Investor Update Template:**

```
Subject: [Company Name] — [Month Year] Update

TL;DR (3 bullets):
- [Win: e.g., Revenue grew 12% MoM to $[X]K MRR]
- [Win: e.g., Closed [Customer Name], our largest deal at $[Y]K ACV]
- [Concern: e.g., Sales hiring is behind plan — 2 of 3 open roles unfilled]

KPIs:
| Metric | This Month | Last Month | Plan | YoY |
|--------|-----------|------------|------|-----|
| MRR | $[X]K | $[Y]K | $[Z]K | +[%] |
| ARR | $[X]M | $[Y]M | $[Z]M | +[%] |
| Customers | [N] | [N-1] | [P] | +[%] |
| Gross Margin | [X]% | [Y]% | [Z]% | - |
| Net Revenue Retention | [X]% | [Y]% | - | - |
| Burn | $[X]K | $[Y]K | $[Z]K | - |
| Cash in Bank | $[X]M | $[Y]M | - | - |
| Runway (months) | [N] | [N-1] | - | - |
| Headcount | [N] | [N-1] | [P] | - |

Wins (3-5):
- [Specific win with metric]

Challenges (2-3):
- [Specific challenge, what you're doing about it]

Asks (1-3):
- [Specific intro, advice, or resource request]

Thank you to [investor name] for [specific help they provided this month].
```

**What good looks like:** Investors reply "Great update, keep it coming" or offer specific help on your asks. Investors who never reply within 3 months get moved to a "passive" distribution list.

## Best Practices
<!-- STANDARD: 3min — operational principles for IR -->

1. **Fundraise when you don't need the money**: The best time to raise is when you have 12+ months of runway and accelerating growth. The worst time is when you have 3 months of cash. Desperation is a negotiable term — and it always works against you.
2. **Your data room is your resume**: Organized, complete, counsel-reviewed. A messy data room adds 2-4 weeks to diligence and invites deeper scrutiny. Every missing document raises a question: "What are they hiding?"
3. **Pitch the problem, not the product**: Investors buy market insight, not features. "We built a better CRM" gets a pass. "The CRM market hasn't innovated for the 40% of sales teams that are field-based" gets a meeting.
4. **Traction is the only real currency**: Revenue growth rate, net revenue retention, CAC payback, and gross margin. Everything else is narrative. If your metrics are weak, your pitch won't save you.
5. **Term sheet comparison is about structure, not valuation**: A $50M clean cap is worth more than an $80M dirty cap. Liquidation preference, participation, board control, and anti-dilution determine your outcome, not the headline number.
6. **Investor updates: always on time, always honest**: Same day every month. Bad news goes in the subject line ("Challenging month — revenue miss, plan to recover"). Investors fund lines of trust before lines of code. Breach trust once on an update and they'll never trust your projections again.
7. **Never stop fundraising until the wire hits**: Between term sheet and close, 10-15% of deals blow up. Silent period means no active outreach, but maintain warm backup conversations. You need a Plan B investor who's met you 2-3 times and has done preliminary diligence.
8. **Cap table hygiene is a monthly practice**: Reconcile your cap table monthly. Every option grant, every exercise, every transfer. One error discovered during Series B diligence will delay your close by 2-4 weeks and cost $20K+ in legal fees to fix.
9. **Pitch deck design matters**: Good design signals attention to detail. Bad design signals sloppiness. Use one font family. One accent color. No clip art. No memes. Maximum 5 bullet points per slide. If a slide takes >30 seconds to understand, it's too complex.
10. **References make or break your round**: A single bad customer reference kills a deal faster than any diligence finding. Pre-select your references. Pre-brief them. Know what each reference will say. If a reference is lukewarm, they're not a reference — they're a liability.
11. **Secondary transactions require board approval and careful communication**: Tender offers and founder secondaries create winners and losers. Employees who can't sell watch colleagues cash out. Design secondaries so every employee gets at least some liquidity. Communicate the rationale transparently.

## Error Decoder
<!-- DEEP: 10+min -- IR failures that kill companies -->

| Problem | Root Cause | Fix |
|---------|------------|-----|
| Fundraise stalled — no term sheets after 30+ meetings | Weak traction metrics, unclear narrative, or wrong investor targeting. | Run a "no-term-sheet post-mortem": ask 3 friendly investors for honest feedback. Common answers: "Revenue too small for your valuation ask," "TAM not convincing," "Team doesn't have domain expertise." Fix the weakest link and re-approach in 3-6 months. |
| Term sheet pulled during no-shop | Material negative information surfaced in diligence that wasn't disclosed upfront. | Disclose all bad news before the term sheet: customer churn, key departures, pending litigation, revenue concentration. Surprise in diligence = pull. Pre-disclosed challenge = negotiated. |
| Data room requests overwhelm team (50+ follow-up items) | No data room structure before fundraise launch. | Build data room completely before first investor meeting. The "14-folders" checklist above. If an investor asks for something not in the room, it goes in the room for all future investors. |
| Investor update goes unanswered for 3+ months | Update is too long, too vague, or investor is disengaged. | Keep updates to 1 page. Lead with numbers, not narrative. If an investor never engages, move them to quarterly updates. Don't waste CEO time on disengaged investors. |
| Cap table error discovered during Series B diligence | Excel-based cap table with manual updates. No monthly reconciliation. | Migrate to Carta or Pulley. Reconcile monthly. Have outside counsel audit the cap table before every fundraise. Cost: $2K-$5K. Value: avoids $20K+ in legal fees and 2-4 weeks of delay. |
| Down round destroys founder equity | Anti-dilution provisions (full ratchet) + pay-to-play + option pool refresh combine to crush common. | Negotiate weighted-average anti-dilution. Model down-round scenarios before accepting terms. If facing a down round, negotiate: (1) recapitalization instead of priced round, (2) option pool refresh as part of the round, not after, (3) founder refresher grants for those who stay. |
| Customer reference call goes badly | Customer wasn't pre-briefed or was selected without verifying enthusiasm. | Only put forward customers who would rate you 9+/10. Ask directly: "Would you be willing to take a call and be fully candid about your experience?" If they hesitate, they're not a reference. |
| Pitch deck leaks to competitors | Sent to too many investors without watermarking or tracking. | Every deck has a unique watermark with the recipient firm name. Use Docsend or similar for view tracking. Never email the deck as an attachment — always a tracked link. |

### Crisis IR Playbook
<!-- DEEP: 10+min -->

- **Down round**: Communicate before it leaks. Frame as "recapitalization to extend runway to profitability, with strong insider participation." Lead with the plan, not the valuation. Existing investors must re-invest or signal confidence, or new investors won't touch it.
- **Layoffs**: Three communications, in order: (1) internal all-hands — laid-off employees hear from CEO first, (2) investor update within 24 hours with rationale, numbers, and path to breakeven, (3) public blog post if >20% of company. Never let investors learn about layoffs from TechCrunch.
- **Product incident/breach**: Customer communication first, investor update second, public disclosure third (if material). Investor update: "On [date], we experienced [incident]. Here's what happened, what we're doing, and the customer impact. We will provide a post-mortem within [timeframe]."

### Error Decoder

| Problem | Root Cause | Fix |
|---------|------------|-----|
| Board meeting is a status update, not a decision-making session | No decision-forward agenda or pre-reads | Every board agenda item must end with a specific ask: "approve budget," "approve option pool increase," "confirm strategy direction." Pre-reads sent 7 days before — no reading at the table. Meeting time is for discussion and decisions, not information dissemination. |
| Director conflicts not disclosed | No annual conflict-of-interest process | Implement an annual D&O questionnaire that explicitly asks about: board seats at other companies, investments in competitors, family relationships with suppliers, and other potential conflicts. Review with legal counsel before the first board meeting each year. |
| Investor-relations fire drill before funding round | No regular investor communication cadence | Send monthly investor updates: key metrics (revenue, burn, cash, headcount), milestones achieved, challenges, asks. Invest the time in quarterly one-on-ones with lead investors. If the only time you talk to investors is when you need money, you're not managing the relationship. |
| Down round devastates employee morale | No communication plan around the financing | Explain to employees what a down round means before they hear it on the news. Key messages: why the round happened (market conditions, not company failure), what it means for options (409A repricing, new grants), and the path to future value creation. Silence creates the worst possible narrative. |
| Shareholder lawsuit after acquisition | Fiduciary duties not followed during sale process | Document the full sale process: board minutes approving the process, fairness opinion, special committee (if conflict exists), market check, shareholder vote materials. Every step must demonstrate that the board fulfilled its Revlon duties. If no fairness opinion or market check, expect a lawsuit. |
| Cap table shows options that expired years ago | Option grants never tracked post-termination | Post-termination exercise periods vary (30-90 days standard, longer for early exercise). Track all option grants with expiration dates. Expired options should be returned to the pool. Uncancelled expired options create cap table noise and legal risk. |
| Annual shareholder meeting delayed past legal deadline | No calendar for corporate compliance events | Maintain a compliance calendar: annual meeting date, franchise tax deadlines, annual report filings, board election dates, option exercise windows. Set reminders 60 days before each deadline. Missing a filing deadline can result in fines or loss of good standing. |


## Production Checklist
<!-- QUICK: 30s — binary pass/fail items. All must pass. -->

- [ ] **[IR1]** Data room built with all 14 folders populated and counsel-reviewed before first investor contact
- [ ] **[IR2]** Pitch deck finalized: 12 slides, no slide >5 bullets, every slide answers one question
- [ ] **[IR3]** Financial model built with best/base/worst case scenarios, bottoms-up hiring plan, and 24-month projections
- [ ] **[IR4]** Target investor list: 30-50 firms, tiered, with warm intro path mapped for each
- [ ] **[IR5]** Investor CRM set up with pipeline stages and tracking fields (Affinity, Streak, or Airtable)
- [ ] **[IR6]** Reference customers identified (5-8), pre-briefed, and reference call logistics confirmed
- [ ] **[IR7]** Term sheet comparison matrix completed for any competing offers — structure ranked before valuation
- [ ] **[IR8]** Cap table modeled in 4 scenarios: base case, down round, exit waterfall ($50M/$100M/$500M/$1B), acquisition
- [ ] **[IR9]** Cap table reconciled and counsel-audited within 30 days of fundraise launch
- [ ] **[IR10]** Investor update template established and first monthly update sent (or schedule set)
- [ ] **[IR11]** Background check disclosures prepared: any litigation, regulatory actions, credential issues disclosed upfront
- [ ] **[IR12]** All material customer contracts (>$100K) collected and redacted for data room
- [ ] **[IR13]** Competitive differentiation matrix documented with specific evidence (win rates, customer quotes, product benchmarks)
- [ ] **[IR14]** Fundraising FAQ document created answering top 20 diligence questions before they're asked
- [ ] **[IR15]** No-shop period diligence response SLA established: all investor requests acknowledged within 4 hours, fulfilled within 24 hours

## Cross-Skill Integration
<!-- QUICK: 30s — table of who to talk to when -->

This skill in a typical IR and fundraising workflow chain:

| Step | Skill | What It Produces for This Skill |
|------|-------|--------------------------------|
| **Before** | `board-manager` | Board governance framework, investor communication cadence, fiduciary compliance → ensures IR aligns with board expectations |
| **Before** | `ceo-strategist` | Strategic vision, company narrative, fundraising amount and timing, organizational context → feeds the pitch deck story and raise parameters |
| **Before** | `fp-and-a-analyst` | Financial model (P&L, balance sheet, cash flow), cap table, dilution analysis, scenario modeling → provides the numbers behind every investor conversation |
| **This** | `investor-relations` | Data room, pitch deck, pipeline management, investor updates, due diligence coordination, term sheet comparison, secondary transaction management |
| **After** | `legal-advisor` | Consumes term sheet for legal review, definitive agreement drafting, and closing mechanics |
| **After** | `ceo-strategist` | Consumes fundraise outcomes to update strategic plan, org design, and board composition |

Common chains:
- **Full fundraise cycle**: `fp-and-a-analyst` → `investor-relations` → `legal-advisor` — Financial model → data room + deck + pipeline → term sheet negotiation and close
- **Quarterly IR cadence**: `board-manager` → `investor-relations` → `ceo-strategist` — Board deck and governance → investor update memo → strategic adjustments based on investor feedback
- **Down round navigation**: `ceo-strategist` → `investor-relations` → `board-manager` → `legal-advisor` — Crisis decision → investor communication → board approval → legal mechanics

```bash
# Example: Produce a fundraise-ready package from FP&A to IR
# 1. fp-and-a-analyst produces financial model and cap table
# 2. investor-relations structures data room, builds pitch deck, prepares pipeline
# 3. legal-advisor reviews term sheet and drafts definitive agreements
```

## What Good Looks Like

A fundraise that goes from first meeting to term sheet in 6 weeks, diligence to close in 4 weeks. The data room has zero follow-up requests because everything was there on day one. The pitch deck gets partner-level meetings within 1 week of warm intro. Investor updates go out on the 5th of every month — investors reply "great update" or offer specific help. Cap table is audited and reconciled. Term sheet comparison matrix is one page with the winner highlighted — the founder can explain why in one sentence. Down-round scenarios are modeled and stress-tested. Customer references are pre-briefed and enthusiastic. The wire hits on schedule. There is a Plan B investor in the wings throughout.

## References
<!-- QUICK: 30s — links to deeper reading -->

- `references/data-room-checklist-detailed.md` — Expanded 14-folder data room checklist with document descriptions and common red flags
- `references/term-sheet-anatomy.md` — Deep dive on every term sheet provision: liquidation preference math, anti-dilution formulas, protective provisions negotiation playbook
- `references/cap-table-waterfall-examples.md` — Worked examples of liquidation waterfalls at $10M, $50M, $100M, and $500M exit values
- `references/investor-pipeline-templates.md` — CRM setup guide for Affinity, Streak, Airtable, and Notion with pipeline stage definitions
- `references/due-diligence-response-playbook.md` — Common diligence requests organized by category with response templates
- `assets/pitch-deck-template.pptx` — 12-slide pitch deck template with layout, speaker notes, and design guide
- `assets/investor-update-template.md` — Monthly investor update template with KPI definitions and example updates
- `assets/data-room-index-template.xlsx` — Data room index with folder structure, document checklist, and status tracker
- `assets/term-sheet-comparison-matrix.xlsx` — Side-by-side term sheet comparison tool with weighted scoring
- Related skills: `ceo-strategist`, `board-manager`, `legal-advisor`, `fp-and-a-analyst`
- Books: Venture Deals (Feld & Mendelson), Secrets of Sand Hill Road (Kupor), The Art of Startup Fundraising (Cremades)
- Resources: NVCA model legal documents, YC Safe templates, Carta cap table benchmarks, PitchBook/NVCA Venture Monitor
