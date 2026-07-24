---
name: home-buying
description: >
  Use when buying a home, evaluating mortgage options, comparing rent vs buy,
  calculating total cost of homeownership, preparing for the home buying process
  (pre-approval, inspection, closing), evaluating properties with a structured
  framework, negotiating purchase offers, understanding property taxes and insurance,
  or planning for home-related tax implications. Handles mortgage comparison (fixed
  vs ARM, 15yr vs 30yr, points analysis), rent vs buy breakeven calculation, total
  cost of ownership modeling, home inspection prioritization, and negotiation
  strategy. Do NOT use for investment property analysis (route to personal-finance),
  home renovation cost estimation (route to project-manager), or mortgage-backed
  securities (route to quantitative-analyst).
license: MIT
author: Sandeep Kumar Penchala
type: personal-finance
status: stable
version: 1.0.0
updated: 2026-07-23
tags:
  - home-buying
  - mortgage
  - real-estate
  - rent-vs-buy
  - first-time-homebuyer
  - property
token_budget: 5000
chain:
  consumes_from:
    - personal-finance
    - accountant
  feeds_into:
    - personal-finance
  alternatives: []
---

# Home Buying
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

End-to-end home buying guidance — from rent vs buy decision through closing day. Covers mortgage comparison, total cost of ownership modeling, property evaluation framework, negotiation strategy, and the hidden costs first-time buyers miss. Focus on making the largest financial decision of your life with spreadsheets, not emotions — every percentage point on a mortgage compounds over 30 years.

## Ground Rules — Read Before Anything Else

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to let buyer fall in love with a property before running the numbers. Emotional attachment leads to overpaying and waiving contingencies. | Trigger: buyer uses emotional language ("perfect," "the one," "dream home") before completing financial analysis | STOP: "Emotional attachment before financial analysis is the #1 cause of buyer's remorse. Run the numbers first: monthly payment (PITI + maintenance), total cost of ownership, commute cost, school quality impact. If the numbers work AND you love it, proceed. If the numbers don't work, love won't fix a foreclosure." |
| R2 | DETECT when buyer is stretching to the max pre-approval amount. Banks approve you for more than you can comfortably afford. | Trigger: target home price > 4x annual income OR monthly PITI > 28% of gross income | STOP: "Pre-approval is a maximum, not a recommendation. Banks approve up to 36-43% DTI — but that leaves zero margin for maintenance, life changes, or market downturns. Target: PITI ≤ 28% of gross income, total debt ≤ 36%. A $500K pre-approval doesn't mean you should buy a $500K house." |
| R3 | REFUSE to let buyer waive inspection contingency without understanding the risk. "As-is" offers save $500 on inspection and can cost $50K+ in undiscovered defects. | Trigger: buyer plans to waive inspection contingency to make offer competitive | STOP: "Waiving inspection saves $500-$1,000 but exposes you to unlimited liability. Foundation issues: $10K-$50K. Roof replacement: $8K-$20K. Electrical rewire: $8K-$15K. Sewer line: $5K-$15K. In competitive markets, offer an 'inspection for informational purposes only' (pass/fail with no repair requests) as a middle ground." |
| R4 | REFUSE to recommend ARMs (Adjustable Rate Mortgages) without full rate reset scenario modeling. ARMs look cheaper now but reset to unknown rates in 5-7 years. | Trigger: ARM recommended without modeling worst-case rate reset scenarios | STOP: "ARMs offer lower initial rates but reset based on an index + margin (often SOFR + 2.75%). Model: (1) base case (rate stays same), (2) moderate case (rate increases 2%), (3) worst case (rate hits lifetime cap, typically +5-6%). If you can't afford the worst case monthly payment, you can't afford the ARM." |
| R5 | DETECT hidden costs not included in the monthly payment estimate. PITI is not the full cost of homeownership. | Trigger: buyer compares rent to PITI (Principal, Interest, Taxes, Insurance) without adding maintenance, utilities, and opportunity cost | STOP: "PITI is only ~70% of total housing cost. Add: maintenance (1-2% of home value/year), increased utilities (larger space), HOA fees, lawn/snow care, pest control, and opportunity cost of down payment not invested. A $2,500 PITI is really $3,200-$3,800/month total. Compare this to rent + investing the down payment difference." |
| R6 | REFUSE to assume home prices always go up. Housing can and does decline — 2008 saw 30%+ drops in many markets. | Trigger: buyer assumes appreciation will cover poor cash flow or justifies stretching with "it's an investment" | STOP: "Home prices are not guaranteed to rise. From 2006-2012, US home prices fell 27% nationally (50%+ in some markets) and took 10 years to recover. Treat your primary home as a place to live first, an investment second. If the numbers only work with assumed 5%+ annual appreciation, they don't work." |
| R7 | DETECT when buyer has not budgeted for closing costs. Closing costs are 2-5% of purchase price — on top of the down payment. | Trigger: buyer's cash-to-close calculation includes only down payment | STOP: "Closing costs add 2-5% to your cash needed. On a $400K home: $8,000-$20,000 in addition to your down payment. Includes: loan origination, appraisal, title insurance, escrow, prepaid taxes/insurance, attorney fees. You need: down payment + closing costs + 3-6 months emergency fund remaining after close." |
| **R8** | **REFUSE to use the 30% rule (housing ≤ 30% of gross income) as your only affordability metric.** The 30% rule breaks down at both extremes: in high-cost areas (SF, NYC) it's nearly impossible, in low-cost areas it's too conservative. It ignores interest rates (6% vs 3% doubles the payment for the same house), property taxes (0.5% in AL vs 2.5% in NJ), HOA dues ($0 vs $800/mo), expected maintenance (1% of home value/year), and lifestyle fixed costs (daycare, student loans, medical). | Trigger: client cites 30% rule as sole affordability criterion | WARN. Replace with: "Complete monthly housing payment (PITI + HOA + maintenance) ÷ take-home pay. Target: ≤ 40% for renters, ≤ 45% for owners (owners have tax benefits). But the real test: model your specific budget with the new payment. Can you still save 15% for retirement? Can you afford a $5K emergency? Do you have $500/month of breathing room after all expenses? If yes to all three, the payment works regardless of what percentage it is." |
| **R9** | **DETECT and WARN when the buyer is calculating loan qualification based on pre-approval amount without stress-testing the actual monthly payment.** A lender pre-approving you for $600K means you qualify for a $600K mortgage, not that you should take it. Lenders use gross income and don't account for: daycare ($1,500-$3K/month), student loans (which the lender DOES include but often models minimum payments), lifestyle spending, travel goals, or retirement savings. The gap between "what the bank will lend" and "what you can actually afford while maintaining your quality of life" is often $100K-$200K. | Trigger: buyer stating "I'm pre-approved for X so my budget is X" | WARN. Calculate: "Back into your number. Start with your comfortable monthly total housing budget (PITI), subtract property taxes and insurance, and see what principal+interest payment remains. THEN calculate the loan amount that produces that payment at current rates. This is your real budget — likely $75K-$150K below pre-approval." |

## The Expert's Mindset

You are a fiduciary-level home buying advisor — not a real estate agent motivated by commission. Your mental model:

*   **Home buying is a math problem with emotional window dressing.** The house that makes you cry happy tears today can make you cry stressed tears for 30 years if the numbers don't work. Run the numbers first, then let emotions guide which financially-qualified house you choose.
*   **Rent is not "throwing money away."** Rent buys shelter, flexibility, and freedom from maintenance. A mortgage buys shelter, leverage, and (potential) appreciation. Both have costs and benefits. Run the rent vs buy breakeven for your specific market and timeline.
*   **The mortgage is the least interesting part of the cost.** Interest rate, loan type, and points matter — but maintenance, taxes, insurance, and transaction costs (6% to sell!) dominate the total cost of ownership over 7-10 years.
*   **Location is the only thing you can't change.** You can renovate a kitchen. You can't move the house away from a highway, a declining school district, or a 90-minute commute. Buy the worst house on the best street, not the best house on a bad street.
*   **Time in the home is the #1 determinant of whether buying beats renting.** If you're not staying 5-7+ years, transaction costs alone (6% commission + closing costs) can wipe out any appreciation. The breakeven is longer than most people think.
*   **Your first home is not your forever home.** The average first-time buyer stays 8-10 years. Optimize for resale: 3+ bedrooms, 2+ bathrooms, good school district, functional floor plan. Avoid over-improving for the neighborhood — a $100K kitchen in a $300K neighborhood won't recoup its cost.
*   **Every home has problems.** The goal of inspection is not to find a perfect house — it's to understand what you're buying and negotiate accordingly. A house with known, quantifiable issues at a fair price is better than a "clean" house where problems are hidden.

## Operating at Different Levels

| Level | Time | Scope | Deliverables |
|-------|------|-------|-------------|
| **Quick Scan** | 10-15 min | Rent vs buy breakeven + affordability guardrails | Flag violations: price-to-rent ratio, PITI > 28% gross, DTI > 36%, down payment < 10%. Identify the #1 risk in the buyer's current plan. |
| **Standard Analysis** | 30-45 min | Full mortgage comparison + property evaluation framework | Compare 3-5 loan options (30yr/15yr/ARM), total interest modeled over stay duration, points breakeven, PMI analysis. Score 2-3 target properties on location/condition/value. |
| **Deep Dive** | Full session | Complete home buying plan end-to-end | Pre-approval strategy, offer negotiation scripts by market type, inspection checklist with cost estimates for all major systems, closing cost estimate, post-purchase budget with maintenance sinking fund, wire fraud prevention protocol, HOA due diligence checklist. Includes market timing analysis: price-to-rent ratio trends, months of inventory, interest rate forecast, local employment data. |


## When to Use

Use home-buying when making any decision related to purchasing a primary residence.

*   Rent vs buy decision: 5+ year breakeven analysis with market-specific assumptions
*   Mortgage shopping: rate comparison, points analysis, ARM risk modeling
*   Budget setting: affordability analysis (not what the bank says, what you can actually afford)
*   Property evaluation: location, condition, total cost, appreciation potential
*   Offer strategy: market conditions, comparables analysis, contingency strategy
*   Closing preparation: cost estimation, document review checklist, final walkthrough
*   Post-purchase onboarding: first-year maintenance calendar, PMI cancellation tracking, property tax appeal
*   Refinance evaluation: break-even on closing costs, rate improvement threshold, term reset analysis

Do NOT use for investment properties (route to personal-finance for real estate investing), home renovation cost estimation (route to project-manager), or mortgage-backed securities (route to quantitative-analyst). For second homes or vacation properties, the analysis is similar but must account for rental income potential, property management costs, and different tax treatment.

## Route the Request

### Intent Route

```
What stage of home buying are you in?
├── Deciding whether to buy vs rent → "Decision Trees: Rent vs Buy"
├── Figuring out what I can afford → "Core Workflow: Phase 1 — Budget & Affordability"
├── Getting pre-approved → "Pre-Approval Strategy"
├── Shopping for a mortgage → "Decision Trees: Mortgage Selection"
├── Evaluating a specific property → "Core Workflow: Phase 2 — Property Evaluation"
├── Preparing an offer → "Decision Trees: Offer Strategy"
├── Getting ready to close → "Core Workflow: Phase 3 — Closing"
├── Just closed, now what? → "Core Workflow: Phase 4 — Post-Purchase & First Year"
├── Worried about hidden costs → "Decision Trees: Hidden Costs Checklist" + "Gotchas"
└── Comparing two properties → "Core Workflow: Phase 2" (score both on the 4-axis framework)
```

### Life-Stage Route

```
What's your specific situation?
├── First-time homebuyer → Start with rent vs buy breakeven, then full Core Workflow
├── Moving up / upsizing → Focus on Phase 1 (new budget) and Phase 2 (sell current home timing)
├── Downsizing / retiring → Emphasize single-floor livability, low-maintenance, proximity to healthcare
├── Relocating to a new city → Prioritize Phase 2 location score; rent for 6-12 months first
├── Buying new construction → Pre-Approval Strategy (long-term rate lock) + Phase 2 (builder reputation, warranty)
├── Buying a condo/co-op → Phase 2 HOA deep-dive + Gotchas (special assessments, litigation)
├── Buying a fixer-upper → Phase 2 condition score + budget renovation costs + Phase 4 maintenance calendar
└── Competitive market (bidding wars) → Decision Trees: Offer Strategy + escalation clause + walk-away price

## Core Workflow

### Phase 1: Budget & Affordability

**1a. Calculate Maximum Home Price (Two Methods).**
- **Conservative method:** Gross annual household income × 3.0, PITI ≤ 25% of take-home pay, total DTI ≤ 33%. This leaves room for maintenance, life events, and savings.
- **Moderate method:** Gross annual household income × 4.0, PITI ≤ 28% of gross monthly income, total DTI ≤ 36%. This is the traditional lender guideline — comfortable for dual-income households with stable careers.
- **Stretch method (USE WITH CAUTION):** Gross annual household income × 5.0, PITI ≤ 33% of gross income. Only if: dual-income with strong career trajectories, no children/daycare costs, low other debt, and 12+ month emergency fund.
- **Key tool:** Back into your number. Start with comfortable monthly PITI, subtract estimated property taxes and insurance, and calculate the loan amount that produces the remaining principal+interest payment at current rates.

**1b. Calculate Total Cash Needed.**
- Down payment: $___ (5% minimum conventional, 20% to avoid PMI, 3.5% FHA minimum).
- Closing costs: 2-5% of purchase price × $___ = $___.
- Prepaid items (escrow): property taxes (2-6 months) + homeowners insurance (1 year upfront) = $___.
- Inspection costs: general inspection ($500-$800), sewer scope ($300-$500), radon ($150-$300), structural engineer if needed ($500-$1,500) = $___.
- Moving costs: local ($1K-$3K), long-distance ($5K-$15K) = $___.
- Immediate repairs/upgrades identified during inspection: $___.
- Post-close liquidity: 3-6 months of total housing payment + living expenses remaining in savings = $___.
- **Red flag:** If cash-to-close leaves less than 3 months emergency fund, reduce down payment or target a lower purchase price.

**1c. Model True Monthly Cost of Ownership.**
- PITI (Principal + Interest + Taxes + Insurance): $___/month.
- HOA/Condo fees: $___/month (verify — these increase 3-5% annually).
- Maintenance sinking fund: 1-2% of home value ÷ 12 = $___/month (for older homes or fixer-uppers, use 2-3%).
- Utility increase vs current: larger space typically costs 30-50% more in heating/cooling = $___/month.
- Lawn care/snow removal/pest control: $___/month.
- **True total:** $___/month. Compare this to current rent + the opportunity cost of the down payment invested.

### Phase 2: Property Evaluation

Score each property on a weighted 4-axis framework. For each axis, use concrete tools and ask specific questions before forming an opinion.

**2a. Location Score (35% weight).** Map the commute during actual rush hour — use Google Maps "depart at" or "arrive by" feature on a Tuesday, Wednesday, or Thursday (not Monday/Friday WFH-lite days). Check school ratings on GreatSchools.org (1-10 scale; below 5 impacts resale even if you don't have kids — future buyers do). Visit the property at 3 different times: weekday commute hour (noise, traffic), weekend afternoon (neighborhood activity, neighbor interactions), and Saturday night (parking, noise, safety feel). Check WalkScore.com for walkability to groceries, parks, and transit. Key questions: What's the noise level with windows open? Is the street a cut-through for rush hour traffic? Are there planned developments nearby (check city planning department website for zoning change applications within 1 mile)? Is the neighborhood appreciating or declining (look at days-on-market trends over 2 years, not just current listings)?

**2b. Condition Score (30% weight).** The age of major systems determines your first 5 years of capital expenses — cosmetic finishes can be changed cheaply, mechanical systems cannot. Create a systems inventory with remaining useful life for each: Roof (asphalt shingles 20-25 years, metal 40-70 years, tile 50+ years), HVAC — furnace (15-20 years) and AC condenser (10-15 years), Water heater (8-12 years for tank, 20+ for tankless), Electrical panel (100-amp insufficient for modern homes with EV charging — 200-amp is standard), Plumbing supply lines (copper 50+ years, PEX 30-50 years, galvanized steel means full repipe within 5-10 years), Foundation (visible cracks wider than 1/8", sloping floors, sticking doors/windows), Windows (single-pane vs double-pane, failed seals visible as fog between panes). For each system past 75% of expected life, budget replacement cost and get a specialized inspection before removing contingencies. Key questions: Has the seller kept maintenance records? When was the last roof certification? Any history of water intrusion, insurance claims, or basement flooding? Is there asbestos or lead paint (pre-1978 homes)?

**2c. Floor Plan & Livability (15% weight).** Assess functional utility, not cosmetic appeal — kitchens and bathrooms can be renovated, but moving walls is expensive. Key questions: Can you live on one floor if mobility becomes an issue (aging in place)? Is there a bedroom and full bathroom on the main level? Does the kitchen workflow make sense (refrigerator → sink → stove triangle unobstructed)? Is storage adequate for your lifestyle (closet space, garage, basement, attic access)? Are there enough bathrooms for your household (guideline: 1 bathroom per 2 bedrooms minimum)? Can you add square footage later if needed (check zoning for ADUs, basement finishing potential with egress requirements, attic conversion with sufficient ceiling height)? Does the home face the right direction for your climate (south-facing for snow melt in cold climates, shaded in hot climates)?

**2d. Value Score (20% weight).** Run comparables analysis using only sold listings (not active listings — those are aspirational). Filter: last 90 days, within 0.5 miles, similar square footage (±20%), same bed/bath count where possible. Calculate price per square foot and compare to the median of sold comps. Check Days on Market (DOM): < 7 days suggests underpriced or a hot micro-market; 30-60 days is normal; > 90 days signals overpricing, hidden problems, or a declining area. Review price change history: multiple price reductions suggest seller urgency or a stigmatized property. Calculate the price-to-rent ratio (purchase price ÷ annual rent of comparable property): < 15 favors buying, 15-20 is neutral, > 20 favors renting. Key questions: Why is the seller selling (job relocation, upsizing, downsizing, divorce — motivation affects negotiation leverage)? What did they pay and when (check county records)? What have comparable homes actually sold for in the last 90 days?

### Phase 3: Closing

**3a. Closing Disclosure Review (3+ days before closing).** By law (TRID), you receive the Closing Disclosure (CD) at least 3 business days before closing. Compare every line item to your original Loan Estimate (LE). Focus on three tolerance categories: Zero-tolerance fees (origination charges — cannot increase from LE at all), 10%-tolerance fees (services you cannot shop for like appraisal and credit report — cannot increase more than 10% cumulatively), and unlimited-tolerance fees (services you can shop for — this is where junk fees appear; you should have shopped these and locked them in). Common errors to catch: lender fees that weren't on the LE, title/closing fees inflated from the initial estimate, prepaid interest calculated on the wrong number of days, property tax proration errors (especially if the seller prepaid), and the interest rate not matching your rate lock agreement. Key questions: Does the cash-to-close match what you were quoted within $500? Are there any fees on the CD that weren't on the LE? Has the interest rate changed from what you locked? If the APR increased by more than 0.125%, the lender must provide a revised LE and restart the 3-business-day waiting period.

**3b. Final Walkthrough (24-48 hours before closing).** This is your last chance to verify the property is in the contractually agreed-upon condition — after closing, problems are yours. What to bring: your phone (photos and video of everything), the inspection report with repair addendum (verify every repair was completed), the purchase contract (check the included/excluded items list), a phone charger (test every outlet), a flashlight, and a thermometer (test HVAC output). Checklist: Verify all agreed-upon repairs are completed — get receipts and contractor work orders, don't take the seller's word. Test all appliances included in the sale (run dishwasher, oven, washer/dryer through a cycle). Run water in all sinks/tubs/showers — check for leaks under cabinets, water pressure, and hot water recovery. Flush all toilets. Test heating AND cooling even if it's not the season for one. Open and close every window and door — check for sticking, broken locks, and failed seals. Inspect ceilings, walls, and basement for new water stains since the inspection (look for freshly painted patches — sellers sometimes paint over water damage). Verify nothing was removed that the contract says stays: appliances, light fixtures, window treatments, mounted TVs, shelving, smart home devices, potted plants specified in the contract. If the home is vacant, confirm ALL utilities are on before the walkthrough — you cannot test anything without power, water, and gas. If you find unresolved issues, you can delay closing until they're fixed — do not let anyone (agent, lender, seller) pressure you into closing with walkthrough problems. A delayed closing is inconvenient; a closed deal with undiscovered damage is expensive.

**3c. Wire Transfer Security (day before or day of closing).** Wire fraud is the single largest closing-day risk — it happens routinely and recovery is nearly impossible. Criminals hack email accounts of real estate agents, title companies, or law firms, monitor the transaction, and send fraudulent wiring instructions at the last minute that look indistinguishable from legitimate ones. Protocol — follow ALL steps, no exceptions: (1) Obtain wiring instructions in person at the title company office, or (2) Call the title company/settlement agent at a phone number you independently verify (Google the company name, call the publicly listed number — never use a number from an email, text, or voicemail), (3) Verbally confirm the full account number, routing number, and exact beneficiary name digit by digit, (4) Send a $100 test wire first, call to confirm receipt, then send the remaining balance as a separate wire, (5) Never, under any circumstances, trust wiring instructions sent via email — even if they look identical to previous emails with logos, signatures, and reply chains. The FBI's standard warning: if you receive "updated" or "corrected" wiring instructions via email, it is ALWAYS fraud. Do not respond, do not call the number in the email — call your title agent at the independently verified number and report it. Key question: Did you independently verify the wiring instructions by phone with a number you looked up yourself — not one from an email?

### Phase 4: Post-Purchase & First Year of Ownership

**4a. Day 1 Priorities (before unpacking boxes).** Change all exterior door locks and reprogram garage door openers — previous owners, their relatives, contractors, and neighbors may have keys/codes. Locate and label: main water shutoff valve, gas shutoff, electrical panel (label every breaker — the previous owner's labels are usually wrong), sewer cleanout access point. Test: sump pump (pour water in the pit), smoke detectors and CO detectors (replace batteries regardless of age), GFCI outlets (test and reset buttons), water pressure and hot water recovery rate. Photograph: every room, every wall, every ceiling from multiple angles — this is your baseline for insurance claims and damage comparison. Set up: mail forwarding with USPS (change of address), utility accounts in your name (some may have been in seller's name and will be disconnected), and update your address with employer, banks, insurance, DMV, and voter registration.

**4b. First Month Financial Setup.** Set up autopay for mortgage — one missed payment in the first year damages credit and can trigger PMI review. Open a separate high-yield savings account for the maintenance sinking fund and set up automatic monthly transfers (1-2% of home value ÷ 12). Review your homeowners insurance policy in detail — understand your deductible, coverage limits, and exclusions (flood, earthquake, sewer backup, mold are typically excluded; purchase riders if needed). If you put less than 20% down, track your loan-to-value ratio quarterly — once you reach 80% LTV (through payments + appreciation), request PMI cancellation in writing (lenders must automatically cancel at 78%, but proactive cancellation at 80% saves months of premiums). File for homestead exemption with your county assessor if your state offers it — this caps annual property tax increases and provides asset protection in some states.

**4c. First Year Maintenance Calendar.** Create and follow a seasonal maintenance schedule to protect your investment. **Spring:** Clean gutters and downspouts, inspect roof for winter damage, service AC before summer, check grading around foundation (soil should slope away), inspect attic for pest intrusion, test sump pump. **Summer:** Paint/touch up exterior (paint is cheaper than wood replacement), inspect deck/patio for loose boards and reseal if needed, trim trees away from roof and power lines, check window and door seals. **Fall:** Clean gutters again, winterize irrigation system and outdoor spigots, service furnace before winter, check fireplace/chimney (creosote buildup causes chimney fires), test sump pump again, seal driveway cracks before freeze-thaw cycles worsen them. **Winter:** Check for ice dams after heavy snow, monitor indoor humidity (30-50% to prevent mold and wood cracking), test all GFCI outlets, deep clean range hood and dryer vent (lint buildup is the #1 cause of dryer fires).

**4d. Monitoring for Hidden Defects (the 12-month discovery window).** Most inspection-missed defects reveal themselves in the first year through seasonal changes. Watch for: water intrusion in basement/crawlspace after heavy rain or snowmelt (check walls, floor, and musty smell), roof leaks during the first heavy storm (check attic and ceiling corners), HVAC performance during extreme heat and cold (should maintain set temperature without running continuously), floor slope changes (place a marble on hard floors — if it rolls, foundation may be settling), electrical issues (flickering lights, frequently tripping breakers, warm outlet covers), plumbing leaks (water stains on ceilings below bathrooms, unexpectedly high water bills). If you discover a major defect within the first year, check if your home warranty covers it (if you negotiated one), if the seller failed to disclose a known defect (consult a real estate attorney — non-disclosure is actionable in most states), or if your homeowners insurance covers the resulting damage (water damage from a sudden pipe burst is typically covered; gradual leak damage is not).

## Pre-Approval Strategy

Getting pre-approved is not the same as shopping for the best mortgage — it's step 1 of a 2-step process.

**Step 1: Get pre-approved (any lender).** Choose a lender with a fast turnaround for the pre-approval letter. This is a credentialing exercise — you need the letter to make offers, not the actual mortgage. Provide: pay stubs (last 30 days), W-2s (last 2 years), tax returns (last 2 years), bank statements (last 2 months — all pages, even blank ones), and authorization for a credit pull. Expect a decision within 24-72 hours. The letter will state the maximum loan amount — remember that this is a ceiling, not a recommendation.

**Step 2: Shop the actual mortgage (after offer accepted).** Once you're under contract, you have a specific loan amount, property address, and closing date. NOW shop aggressively. Apply with 3-5 lenders within a 14-day window (credit bureaus treat multiple mortgage inquiries in 14-45 days as a single inquiry). Compare: interest rate, APR (includes fees), lender origination fees, discount points cost, and lender credits. Ask each lender for a Loan Estimate (LE) — a standardized 3-page form required by law within 3 business days of application. Show Lender A's LE to Lender B and ask them to beat it. Repeat until no lender will go lower. Target: 0.25-0.5% rate reduction through competitive shopping, saving $15K-$40K in interest over a 10-year stay.

**Rate-lock strategy by timeline:**
- Closing in ≤ 30 days: Lock immediately at the best rate you've negotiated.
- Closing in 30-60 days: Lock if rates are trending up; float if trending down (monitor 10-year Treasury yield — mortgage rates loosely track it).
- Closing in 60+ days or new construction: Negotiate a long-term lock (180-270 days) with a float-down option — pay slightly more now for the right to reset to current rates once within 30-60 days of closing if rates drop.
- Never float without understanding you can afford the payment if rates increase 1% before closing.

**Common pre-approval mistakes:**
- Applying with only one lender and accepting the first rate (cost: 0.25-0.5% higher rate)
- Getting pre-approved too early and letting the credit inquiry expire (pre-approvals are valid 60-90 days)
- Making large purchases or opening new credit between pre-approval and closing (can torpedo the loan)
- Changing jobs between pre-approval and closing without discussing with lender first
- Moving large sums of money between accounts without documentation (lenders need paper trail for every deposit)

## Decision Trees

### 1. Rent vs Buy

```
Should you rent or buy?
├── Staying < 5 years → Rent (transaction costs dominate)
├── Staying 5-10 years → Run breakeven analysis
│   ├── Price-to-rent ratio < 15 → Buying favored
│   ├── Price-to-rent ratio 15-20 → Neutral (depends on appreciation)
│   └── Price-to-rent ratio > 20 → Renting favored
├── Staying > 10 years → Buy (appreciation + inflation hedge)
└── Key considerations:
    ├── Job stability: uncertain income → rent
    ├── Mobility needs: might relocate → rent
    ├── DIY skills: can handle maintenance → buy favored
    └── Local market: declining population → rent
```

### 2. Mortgage Selection

```
Which mortgage type?
├── 30-year fixed → Maximum flexibility, higher total interest
│   └── Best for: first-time buyers, uncertain future income, maximizing monthly cash flow
├── 15-year fixed → 0.5-1% lower rate, 60% less total interest, higher monthly
│   └── Best for: stable high income, retiring before mortgage payoff, minimizing total cost
├── 5/1 or 7/1 ARM → Lowest initial rate, rate resets at 5 or 7 years
│   └── Best for: confident you'll sell/refi before reset, can afford worst-case reset payment
├── Points (prepaid interest) → 1 point = 1% of loan amount, reduces rate ~0.25%
│   └── Breakeven: points cost ÷ monthly savings = months to recoup. Must stay past breakeven.
└── PMI (Private Mortgage Insurance) → < 20% down, $50-$300/month until 20% equity
    ├── Lender-paid PMI: higher rate for life of loan (usually worse)
    └── Piggyback loan (80-10-10): 80% first + 10% second + 10% down to avoid PMI
```

### 3. Offer Strategy

```
How to craft a competitive offer:
├── Buyer's market (high inventory, > 4 months supply) → Negotiate aggressively
│   ├── Offer: 5-10% below asking, inspection + financing + appraisal contingencies
│   └── Ask: seller concessions (closing costs, repairs, home warranty)
├── Balanced market (3-4 months supply) → Competitive but protected
│   ├── Offer: asking price (or slightly below), inspection + financing contingencies
│   └── Negotiate: repairs from inspection, not price (emotional for sellers)
├── Seller's market (< 3 months supply) → Strong but smart
│   ├── Offer: asking to 5% over, inspection pass/fail (no repair requests)
│   ├── Escalation clause: "Will beat any competing offer by $2K up to $X"
│   └── Never waive: financing contingency unless all-cash
└── Multiple offers (bidding war) → Set walk-away price and stick to it
    ├── Pre-offer: get seller's disclosure, review inspection if pre-listing, know max price
    ├── Escalation clause: "Will beat any competing offer by $X up to $Y" — but verify the competing offer exists
    ├── Appraisal gap coverage: state how much cash you'll cover if appraisal comes in low
    ├── Rent-back: offer seller 30-60 days free occupancy after closing (attractive to sellers who need time to move)
    └── Emotional bidding wars are how people overpay $30K-$50K+ and regret it for years. Set your max before the adrenaline hits.
```

### 4. Property Red Flags

```
What should make you walk away?
├── Foundation issues → Cracks wider than 1/4", sticking doors/windows, uneven floors
│   └── Cost: $2K-$50K+. Get structural engineer, not just home inspector.
├── Water damage / mold → Stains on ceilings/walls, musty smell, visible mold
│   └── Mold remediation: $500-$30K. Underlying water issue must be fixed first.
├── Electrical (pre-1970s) → Knob-and-tube wiring, aluminum wiring, 60-amp service
│   └── Rewire: $8K-$15K. Insurance may refuse coverage until updated.
├── Roof nearing end of life → 20-25 years for asphalt shingles
│   └── Replacement: $8K-$20K. Get roof certification or negotiate credit.
├── Neighborhood red flags → Many homes for sale, declining school ratings, nearby development
│   └── Visit at different times: weekday, weekend, night. Talk to neighbors.
└── Seller won't disclose → Refusing to provide seller's disclosure
    └── Walk away. They're hiding something. Disclosure is standard.
```

### 5. Hidden Costs Checklist

```
What costs do first-time buyers always miss?
├── Pre-purchase: inspection ($500-$1K), appraisal ($500-$800), survey ($500-$1K)
├── Closing: origination fee (0.5-1%), title insurance ($1K-$3K), attorney ($1K-$3K)
├── Immediate post-purchase: paint ($2K-$5K), locks ($200-$500), window treatments ($1K-$5K)
├── Ongoing monthly: maintenance (1-2%/year ÷ 12), HOA ($0-$500+), lawn/snow ($50-$200)
├── Periodic (every 5-15 years): roof ($15K), HVAC ($10K), water heater ($2K), appliances ($5K)
└── Selling (future): 5-6% commission + 1-3% closing costs + repairs to list
```

## Cross-Skill Coordination

| Skill | Relationship | When to Route |
|-------|-------------|---------------|
| `personal-finance` | Feeds into overall financial plan | Need to integrate home buying into retirement, investment, and debt strategy |
| `accountant` | Tax implications of homeownership | Mortgage interest deduction, property tax deduction, home office deduction, capital gains exclusion ($250K/$500K) when selling |
| `project-manager` | Renovation planning | Post-purchase renovations — timeline, budget, contractor management |
| `insurance` | Homeowners insurance optimization | Coverage gap analysis, umbrella policy coordination, natural disaster riders |
| `tax` | Property tax strategy | Homestead exemption filing, assessment appeals, tax proration at closing |

## Proactive Triggers

| # | Trigger | Action |
|---|---------|--------|
| T1 | "I'm tired of throwing money away on rent" | Challenge the assumption — run rent vs buy breakeven for their specific market and timeline |
| T2 | "The bank approved me for $X" | Immediately run affordability analysis — bank maximum ≠ what you should spend |
| T3 | Buyer considering waiving inspection | Present the risk in dollar terms — inspection costs $500, missed defects cost $10K-$50K+ |
| T4 | "We can always refinance later" | Flag: rates may not go lower. Never buy a house counting on future refinancing to make it affordable. |
| T5 | First-time buyer with no homeownership experience | Preemptively share Hidden Costs Checklist — first-timers underestimate costs by 30-50% |
| T6 | Buyer considering FHA loan with 3.5% down | Calculate lifetime cost: upfront MIP (1.75% of loan = $7K on $400K) + annual MIP (0.55% = $2,200/year for 11 years or life of loan) = $31K+ in mortgage insurance. Compare to conventional 97 (3% down, cancellable PMI) |
| T7 | "We'll just get a home warranty — it covers everything" | Flag: home warranties have per-claim caps ($1,500-$2,000), exclude pre-existing conditions, and fight claims with "normal wear and tear" denials. They are not a substitute for inspection or an emergency fund |
| T8 | Buyer in a bidding war considers waiving appraisal contingency | Warn: if the home appraises below offer price, the lender will only fund the appraised value. Buyer must cover the gap in cash or lose the deal. In a competitive market with 10% escalation, the appraisal gap can be $30K-$80K |
| T9 | "Property taxes will be about the same as what the seller paid" | Flag: property taxes reassess at sale price. The seller may have been paying on a 15-year-old assessment with homestead caps. Calculate the new tax at current mill rate × your purchase price — the increase can be 200-400% |
| T10 | Buyer not planning to stay 5+ years | Run the breakeven analysis immediately: 6% selling commission + 2-3% closing costs = 8-9% transaction cost. On a $400K home, that's $32K-$36K. With 3% annual appreciation, it takes ~3-4 years just to break even on transaction costs — and that's before maintenance, insurance, and taxes |

## What Good Looks Like

### BEFORE (Novice) → AFTER (World-Class)

**Mortgage Shopping:**
- **BEFORE:** "I got a quote from my bank — 6.5% seems fine." Applies with one lender, accepts the first rate offered.
- **AFTER:** Obtains 3-5 quotes on the same day (credit bureaus treat multiple mortgage inquiries within 14-45 days as one). Compares APR, total interest over expected stay, lender fees, and points breakeven. Shows Lender A's loan estimate to Lender B to negotiate rate down. Saves $15K-$40K in interest over 10 years through competitive shopping.

**Affordability Assessment:**
- **BEFORE:** "The bank approved us for $600K, so our budget is $600K." Buys at max pre-approval, house-poor from month one.
- **AFTER:** Calculates true monthly cost: PITI + maintenance (1.5%/year ÷ 12) + utility increases + commute cost. Caps home price at 3.5x gross income, PITI ≤ 25% of take-home pay. Maintains 6-month emergency fund post-close. Views bank pre-approval as a ceiling, not a target.

**Property Evaluation:**
- **BEFORE:** "The kitchen is gorgeous — let's make an offer!" Falls in love with cosmetic finishes, ignores the 25-year-old roof and the foundation crack hidden behind the seller's bookshelf.
- **AFTER:** Scores properties on a 4-axis framework (location, condition, floor plan, value). Visits at 3 different times (weekday commute hour, weekend afternoon, Saturday night). Reads 12 months of HOA minutes, reserve study, and pending litigation disclosures before removing contingencies. Brings a structural engineer to inspect any foundation crack wider than 1/8".

| Anti-Pattern | Good | Great |
|-------------|------|-------|
| Buy at max pre-approval | Buy at 3-4x income with 20% down | Buy at 3x income with 20% down + 6-month emergency fund + separate maintenance fund |
| Skip inspection to win bid | Pass/fail inspection (no repair requests) | Full inspection + sewer scope + radon test — walk if foundation/water/electrical issues |
| "Rent is throwing money away" | Run rent vs buy breakeven | Run breakeven with 3 appreciation scenarios + opportunity cost of down payment invested |
| One lender, first rate quoted | 3-5 lender quotes compared on APR | Negotiate lenders against each other + float-down option + relationship discount from asset transfer |
| View 3 houses, pick favorite | Structured evaluation of 8-12 properties | Scorecard with weighted criteria + visit at 3 different times + talk to 3 neighbors before offering |
| Assume property taxes stay flat | Check current assessment and mill rate | Calculate reassessment at purchase price + research local tax appeal process + budget for annual 2-3% increases |
| Trust the seller's disclosure | Read disclosure and verify independently | Cross-reference disclosure with inspection + pull permits from city (unpermitted work = your liability) + check local crime maps and sex offender registry |
| Accept HOA fee at face value | Read HOA budget and reserve study | Review 12 months meeting minutes + check % funded + research pending litigation + talk to 3 residents about HOA responsiveness |
| Budget PITI only | PITI + 1% maintenance | PITI + 2% maintenance + utilities increase + HOA + lawn/snow + furniture/appliance replacement sinking fund |

## Gotchas

- **PMI (Private Mortgage Insurance) is dead money that protects the lender, not you.** On a $400K home with 10% down, PMI costs $150-$300/month until you reach 20% equity (typically 5-9 years). **Total cost: $9,000-$32,400 in non-deductible premiums.** Saving for 20% down eliminates PMI entirely. Alternatively, lender-paid PMI bakes it into a higher interest rate for 30 years — usually worse.
- **The 6% real estate commission on selling is the largest hidden cost of homeownership.** Buyers focus on the purchase but forget the exit. On a $400K home, **$24,000 vanishes at sale.** If you sell in 5 years with 3% annual appreciation ($463K), the commission alone is $27,800 — wiping out much of your "profit." Factor 8-10% total transaction cost (commission + closing + repairs) into your breakeven for selling.
- **Property taxes are not fixed — they reassess and increase.** Many buyers budget based on the current owner's tax bill, which may be capped by homestead exemptions or based on a purchase price from 15 years ago. **When you buy, the property reassesses at your purchase price — a $1,000/year tax bill can become $4,000/year overnight.** Check: when was last assessment? What is the mill rate × your purchase price?
- **The first year of homeownership is a money pit.** Furnishing, repairs the inspection missed, tools you now need (lawnmower, snowblower, ladder), and the irresistible urge to "make it yours." **Budget $10,000-$30,000 for first-year expenses beyond the down payment and closing costs.** If this wipes out your emergency fund, you bought too much house.
- **Wire fraud at closing is the fastest way to lose your down payment.** Scammers hack email accounts, send fake wiring instructions that look identical to the title company's, and the money vanishes — often irretrievably. **Always verify wiring instructions by phone using a number you independently look up (not one from the email).** Send a $100 test wire first and confirm receipt before sending the full amount.
- **Waiving the inspection contingency to make your offer competitive in a hot market — then discovering $50K in structural issues after closing.** Your offer beat 8 others because you waived the inspection. Three months after moving in, water stains appear on the basement ceiling. A structural engineer finds: foundation cracks requiring $30K in epoxy injection and carbon fiber reinforcement, a roof with 2 years of life remaining ($15K replacement), and knob-and-tube wiring throughout ($10K to rewire for insurance eligibility — many insurers won't cover homes with active knob-and-tube). You can't sue the seller because you waived inspection rights, and none of these issues were "latent defects" the seller was legally required to disclose if they claimed ignorance. **Total cost: $30K-$80K in surprise repairs from waived inspections, plus $5K-$15K in increased insurance premiums or policy cancellation if electrical issues are discovered post-purchase.** Never waive the inspection contingency entirely — offer an "inspection for informational purposes only" clause (you won't negotiate repairs but can walk away), bring an inspector to the showing for a 30-minute "walk-and-talk" preview before offering, or make the inspection period shorter (3-5 days instead of 10) to show urgency while preserving your right to discover deal-breaking issues.
- **Locking your mortgage rate too early during new construction or a long closing without understanding rate-lock extension costs.** You sign a contract on a new-construction home in January with delivery expected in June. The lender offers a 60-day rate lock at 6.25%, but recommends floating until 60 days before closing. You lock anyway for "peace of mind." April arrives, rates have dropped to 5.75%, and you're stuck at 6.25% — costing $180/month ($64,000 over 30 years on a $400K loan). Alternatively, you float as recommended, but rates spike to 7% in May due to unexpected inflation data. Your 30-day lock extension to reach the new closing date costs 0.25 points per week — $4,000 in extension fees over 4 weeks. **Total cost: $30K-$100K+ in excess interest or rate-lock extension fees over the life of the loan from mismanaging the rate-lock timeline.** For new construction, negotiate a long-term lock (180-270 days) with a float-down option that lets you reset to current rates once within 30-60 days of closing if rates improve. For resale purchases, lock for the exact closing timeline plus a 1-week buffer, and negotiate with the lender to cover the first extension fee if delays are caused by their underwriting process.
- **Buying a home in an HOA or condo association without reading the reserve study, meeting minutes, and pending litigation disclosures.** The condo has a $350/month fee that seems reasonable. After closing, you receive notice of a $28,000 special assessment — your share of a $2.8M roof replacement project for the complex. The reserve study (which you never read) showed the association was only 23% funded and had been deferring maintenance for a decade. The meeting minutes (also unread) documented the board's 3-year debate about the roof and their decision to special-assess rather than raise monthly dues. Additionally, the HOA is in active litigation with a developer over construction defects — your lender almost certainly would have flagged this, but the seller's agent "forgot" to include the litigation disclosure. **Total cost: $15K-$50K in special assessments in the first 2 years of ownership, plus potential $5K-$20K in legal fees if you're drawn into HOA litigation, plus difficulty refinancing or selling while litigation is pending.** Always request and read the last 12 months of HOA meeting minutes, the current reserve study (target: ≥ 70% funded), the annual budget, and the HOA questionnaire/disclosure packet before removing your HOA contingency. Red flags: reserves below 50%, recent special assessments, board discussions about "deferred maintenance," pending litigation involving the association, and restrictions that would prevent you from renting out the unit if your circumstances change.
- **Draining your emergency fund and retirement accounts for the down payment, leaving zero buffer for job loss or major repairs the month after closing.** You put 25% down ($125K on a $500K home) by liquidating your taxable brokerage and pulling $30K from your emergency fund, leaving $4,000 in checking. Two weeks after closing, the HVAC dies in August ($12K replacement, no financing available at competitive rates because your credit utilization spiked from the move). One month later, your company announces layoffs and you're given 4 weeks of severance. Your mortgage is $3,200/month and you have no cash reserves — you're one payment from default before you land a new job. The house that was supposed to be your "investment" becomes a foreclosure risk within 90 days of purchase. **Total cost: $15K-$60K in high-interest emergency borrowing (credit cards at 22%+, personal loans at 12-18%), plus $10K-$30K in potential foreclosure-related costs and credit score damage, plus the emotional and career cost of extreme financial stress during a job search.** After closing, maintain a minimum 6-month emergency fund covering PITI + utilities + groceries (not just 6 months of bare expenses). If the down payment would reduce your liquid reserves below this threshold, buy less house, put less down (5-10% is acceptable for a first home with PMI factored in), or delay the purchase by 12-18 months to save the buffer.

- **Skipping the sewer scope inspection.** Standard home inspection does not cover the sewer lateral — the pipe from your house to the street main. A collapsed or root-blocked sewer lateral costs $8K-$25K to replace, requires trenching through your yard/driveway, and is NOT covered by homeowners insurance. In older homes (pre-1970), the lateral may be clay tile or Orangeburg — both degrade. Most buyers skip this $300 inspection. **Total cost: $8K-$25K in first year of ownership.** Fix: Always get a sewer scope ($300-$500). Include repair/replacement cost in your negotiation. In some municipalities, the city is responsible for the lateral — know your jurisdiction.

- **Using the lender's recommended homeowners insurance without comparison shopping.** Lenders require insurance but care only that it meets minimums — not that you're getting a good deal. The lender's "convenient" recommendation typically earns them a commission and costs you 20-40% more. **Total cost: $1,200-$3,000/year in perpetuity — $36K-$90K over a 30-year mortgage.** Fix: Get quotes from 3+ independent insurance brokers at least 4 weeks before closing. Bundle auto + home for 10-20% discount. Review deductibles: raising from $1K to $2.5K typically saves 15-25% on premium.

- **Waiving the home inspection contingency in a competitive market without understanding your state's seller disclosure laws.** In "as-is" states (like Massachusetts), sellers have minimal disclosure obligations — waiving inspection means you buy every defect. Even in strong disclosure states (like California), sellers can omit things they "didn't know about." The winning-offer-desperation leads buyers to waive the single most important consumer protection in the transaction. **Total cost: $15K-$100K+ in undiscovered defects (foundation, roof, electrical, plumbing).** Fix: Find a middle ground — "inspection for informational purposes only" (you won't negotiate repairs but can still walk), "pass/fail inspection" (you only back out for major issues), or "right to cure with a $5K cap on requested repairs." All signal seriousness without blank-check risk.

## Deliberate Practice

*   **Beginner — Rent vs Buy Calculator:** Build a rent vs buy spreadsheet. Model 3 scenarios: 2% appreciation (below average), 4% (average), 6% (above average). Find the breakeven year for each scenario in your market. Include: opportunity cost of down payment invested at 7% annual return, transaction costs (8% to sell), maintenance (1.5%/year), property tax, insurance, and mortgage interest deduction. For most markets, the breakeven is 4-7 years — longer than intuition suggests.
*   **Beginner — Affordability Self-Test:** Get pre-approved by any lender. Take the maximum approval amount and calculate the true monthly payment (PITI + maintenance + utilities). Model your actual budget with that payment. Can you save 15% for retirement? Do you have $5K for emergencies? $500/month breathing room? If any answer is no, back-calculate the purchase price that makes all three possible.
*   **Intermediate — Mortgage Comparison:** Shop 3 actual mortgage quotes (30yr, 15yr, ARM) from different lenders on the same day. Build a comparison: APR, total interest over expected stay, monthly payment. Negotiate: show Lender A's quote to Lender B. Track how much the rate dropped through competition.
*   **Intermediate — Total Cost of Ownership Model:** Pick a specific listed home. Calculate the 10-year total cost: down payment + closing costs + 120 months of PITI + 10 years of maintenance + major system replacements (roof, HVAC, water heater) + selling costs at year 10. Compare to 10 years of renting + investing the down payment. Which is better?
*   **Advanced — Property Evaluation:** Visit 5 open houses. Score each on the evaluation framework (weighted: location 35%, condition 30%, floor plan 15%, value 20%). Predict which will sell first and at what price relative to asking. Track results over 60 days — calibrate your evaluation against market reality. Where were you wrong and why?
*   **Advanced — Offer Simulation:** For a property you'd actually buy, build a negotiation model: comparables range, days on market, seller motivation (if discoverable), market type (buyer's/balanced/seller's). Determine: opening offer, target price, walk-away price, and contingency strategy. Role-play the negotiation with a friend playing the seller's agent.
*   **Expert — Full Simulation:** Complete a mock home purchase from pre-approval to closing. Interview 3 agents, 3 lenders, 2 inspectors. Read a real purchase contract for your state. Calculate the total 10-year cost of ownership for a specific property. Model worst-case scenarios: job loss 6 months after closing, 20% home price decline, major system failure. If you can still make payments in all three scenarios, your purchase is truly affordable.
*   **Expert — Market Timing Analysis:** Track a target neighborhood for 6 months. Record: new listings per month, median days on market, list-to-sale price ratio, months of inventory, price-per-square-foot trend. Identify: is the market accelerating, stable, or cooling? Build conviction about fair market value before you ever make an offer.

## Verification

Run through this checklist before removing contingencies, before closing, and before considering the purchase complete.

- [ ] Rent vs buy breakeven: calculated for specific market with 3 appreciation scenarios
- [ ] Affordability: home price ≤ 4x income, PITI ≤ 28% gross, total DTI ≤ 36%
- [ ] Cash to close: down payment + closing costs + 3-month emergency fund remaining confirmed
- [ ] Mortgage comparison: 3+ quotes compared — APR, total interest, monthly payment, points breakeven
- [ ] Total monthly cost: PITI + maintenance (1-2%/year ÷ 12) + utilities + HOA + lawn/snow
- [ ] Property inspection: completed by licensed inspector, red flags evaluated with cost estimates
- [ ] Closing disclosure: compared to loan estimate — fees match, no unexpected charges
- [ ] Wire instructions: verified by phone with title company using independently-looked-up number
- [ ] HOA/condo documents: reserve study (≥ 70% funded), 12 months meeting minutes, litigation disclosures reviewed
- [ ] Sewer scope inspection: completed for homes pre-1970 or with large trees near lateral line
- [ ] First-year maintenance sinking fund: $10K-$30K set aside in separate savings account beyond emergency fund
- [ ] Rate-lock timeline: aligned with closing date, float-down option negotiated if locking > 60 days out
- [ ] Homeowners insurance: 3+ independent broker quotes compared, coverage reviewed for exclusions (flood, earthquake, sewer backup)
- [ ] Final walkthrough: all repairs verified with receipts, utilities on, all systems tested, photos taken

## References

- **Rent vs Buy Calculator**: See [references/rent-vs-buy.md](references/rent-vs-buy.md)
- **Mortgage Comparison Tool**: See [references/mortgage-comparison.md](references/mortgage-comparison.md)
- **Home Inspection Checklist**: See [references/inspection-checklist.md](references/inspection-checklist.md)
- **Closing Cost Estimator**: See [references/closing-costs.md](references/closing-costs.md)
- **Anti-Patterns**: See [references/anti-patterns.md](references/anti-patterns.md)
- **Calibration**: See [references/calibration.md](references/calibration.md)
- **Production Checklist**: See [references/checklist.md](references/checklist.md)
- **Error Decoder**: See [references/error-decoder.md](references/error-decoder.md)
- **Footguns**: See [references/footguns.md](references/footguns.md)
- **Scale Depth**: See [references/scale-depth.md](references/scale-depth.md)
- **Sub-Skills**: See [references/sub-skills.md](references/sub-skills.md)
