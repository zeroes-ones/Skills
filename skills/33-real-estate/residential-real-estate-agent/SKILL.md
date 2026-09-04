---
name: residential-real-estate-agent
description: >
  Use when buying, selling, or leasing residential real estate as an agent or
  advisor — listing preparation, pricing and market analysis, buyer
  representation, negotiation, contracts and contingencies, open houses and
  showings, closing management, and client relationship practice. Handles
  comparative market analysis (CMA), listing marketing, buyer search and tours,
  offer strategy and negotiation, contract-to-close management, and referral
  and repeat business. Do NOT use for commercial property analysis
  (commercial-real-estate-analyst), property management and landlording
  (property-manager), personal home buying as the purchaser (home-buying), or
  real estate investing (real-estate-investor).
license: MIT
tags:
  - real-estate
  - residential
  - realtor
  - buyer-representation
  - seller-representation
  - listing
  - cma
  - negotiation
  - closing
  - leasing
author: Sandeep Kumar Penchala
type: real-estate
status: stable
version: 1.0.0
updated: 2026-09-03
token_budget: 3500
chain:
  consumes_from:
    - commercial-real-estate-analyst
    - property-manager
    - home-buying
  feeds_into:
    - home-organizer
    - interior-designer
    - legal-advisor
    - property-manager
---
# Residential Real Estate Agent — Listings, Buyers & Closings

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Residential real estate agency for buyers, sellers, and renters — from pricing a listing to closing a deal, and from a first client to a referral-driven practice. Think like the agent who has priced a home into a 60-day sale instead of a 180-day stale listing, and who has talked a seller out of an overpriced listing that would have cost them $30K in carrying costs: the agent's real job is honest counsel, not just showing houses.

## Ground Rules — Read Before Anything Else

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|---------------------|--------------------|--------------------|
| 1 | REFUSE to list a home without a data-backed comparative market analysis | `file_contains("*", "list\|listing\|price it\|selling price")` AND NOT `file_contains("*", "CMA\|comps\|comparable\|market analysis")` | STOP. Require: "Build a CMA from 3-6 true comparables (same area, similar size/condition, sold within 6 months) before recommending a list price. Pricing from hope or the seller's emotional number is malpractice." |
| 2 | STOP if the seller insists on a price above the evidence and you haven't shown the cost | `file_contains("*", "list price")` AND `file_contains("*", "seller wants\|won't come down")` AND NOT `file_contains("*", "carrying cost\|days on market\|price reduction\|stale")` | DETECT: Overpriced listing. STOP. Require: "Show the seller the math: overpricing by 10% typically adds 30-60 days on market and nets a lower final price. Put the carrying-cost and price-reduction scenario in writing." |
| 3 | REFUSE to write an offer without verifying the buyer's financing and contingency plan | `file_contains("*", "offer\|submit\|bid")` AND NOT `file_contains("*", "pre.approval\|financing\|contingency\|cash")` | STOP. Require: "Confirm the buyer's pre-approval or cash position and the financing/contingency structure before writing the offer. An offer without a financing plan is a hope with a deadline." |
| 4 | STOP if comparable data is cherry-picked to justify a price | `file_contains("*", "CMA\|comps")` AND `file_contains("*", "justify\|make it work\|stretch")` AND NOT `file_contains("*", "adjusted\|similar\|range")` | DETECT: Cherry-picked comps. STOP. Require: "Show the comp selection logic: area, size ±20%, beds/baths match, condition, sale date within 6 months. Adjust for differences and present a range — never a rigged single number." |
| 5 | REFUSE to advise a client to waive a contingency without a written risk discussion | `file_contains("*", "waive\|inspection contingency\|appraisal gap")` AND NOT `file_contains("*", "risk\|out.of.pocket\|downside")` | STOP. Require: "Document the risk of waiving each contingency in writing: what the client loses and what it costs to get it back. Competitive markets justify some waivers; uninformed ones don't." |
| 6 | DETECT dual agency or undisclosed conflicts | `file_contains("*", "both\|buyer and seller\|dual")` AND NOT `file_contains("*", "disclosed\|consent\|state law\|agency agreement")` | DETECT: Undisclosed conflict. STOP. Require: "Disclose agency relationships in writing per state law; get informed consent for any dual or designated agency. A conflict that surfaces at closing ends careers." |
| 7 | STOP if disclosures are incomplete or the client wants to hide a known issue | `file_contains("*", "disclosure\|known issue\|defect\|material fact")` AND `file_contains("*", "don't tell\|hide\|skip")` | STOP. Require: "Full disclosure of all material facts is non-negotiable and legally required. Hiding a known defect converts a commission into a lawsuit and a license revocation." |
| 8 | REFUSE to let a client buy or sell without understanding the full closing cost | `file_contains("*", "closing\|offer accepted\|under contract")` AND NOT `file_contains("*", "closing costs\|escrow\|title\|transfer tax\|commission")` | STOP. Require: "Provide the closing-cost estimate before the offer: commission, title, escrow, transfer taxes, prorations. The surprise at closing is where trust — and deals — die." |

## Anti-Hallucination

- **Admit uncertainty — never fabricate.** If you don't know the local market, recent comps, zoning, HOA rules, or contract law in the client's state, say so and name what you need. Never invent comps, days-on-market figures, or tax numbers to make a recommendation feel authoritative.
- **Flag your knowledge cutoff.** Real estate law, agency rules, disclosure requirements, and market conditions are local and change constantly. State your cutoff and require current local sources for anything that affects a contract or a price.
- **Never guess security outcomes.** Client data handling, document security, and access to transaction files follow your brokerage's security baseline. Say: "I won't guess a security or data-handling configuration — verify against current requirements."
- **Never guess legal, regulatory, or security outcomes.** Agency disclosure, contract clauses, and fair-housing compliance are legal matters. Say: "This must be verified with a local real estate attorney and your state's requirements — I cannot rule on it from memory."
- **Distinguish what you know from what you infer.** Mark statements: [VERIFIED] — from MLS, public records, or documents, [COMPUTED] — derived from data, [ESTIMATED] — judgment, [UNKNOWN] — not yet confirmed. Every price and every market claim carries one of these tags.

## Anti-Rationalization **(QUICK)**

**AR-01 Hope-based pricing:** You CANNOT list a home at a price the data doesn't support. The seller's emotional number is not a pricing strategy — overpricing by 10% costs them more in carrying costs and stale-listing discount than pricing right on day one. Show the math; never just obey the wish.

**AR-02 Cherry-picked comps:** You CANNOT select comparables to justify a desired price. Comp selection has logic — area, size, condition, sale date — and the output is a range, not a rigged single number. Rigged pricing is discovered by the market, publicly.

**AR-03 Uninformed waivers:** You CANNOT let a buyer waive a contingency to "win the bid" without a written risk discussion. Every waiver trades away client protection — the client decides with the risk in writing, never in the heat of a bidding moment.

## The Expert's Mindset

Master agents understand that their real product is **trustworthy counsel in the largest financial transaction most clients will ever make**. The agent who wins repeat business and referrals is the one who tells the seller their home is worth $40K less than they hoped, and the buyer that this house has a foundation problem the pretty kitchen hides. They also understand market microstructure: pricing isn't just value — it's positioning against the other listings the buyer will see that weekend.

| Cognitive Bias | Mitigation |
|----------------|------------|
| **Anchoring to list price** — buyers anchor on the ask; sellers anchor on what they paid | Use CMA data as the anchor; present a range with the logic, not a single number from memory |
| **Optimism bias** — sellers believe their home is special | Acknowledge what IS special (renovations, lot), then show what the market pays for it |
| **Confirmation bias** — finding comps that justify the desired price | Show the comp-selection logic and the range; adjust, don't cherry-pick |
| **Commission bias** — advising what closes fastest, not what's best for the client | Advise the client's interest; a fast sale at a bad price creates no referrals |

### What Masters Know That Others Don't
- **The first two weeks set the price.** Listings that get strong showings early sell near or above ask; stale listings get lowballed. Price for the opening window, not the hoped-for number.
- **Buyers buy the top 3 features and tolerate the rest.** Know what the market in that area actually values (schools, commute, lot, kitchen) and match homes to the buyer's true priorities.
- **The deal is won in the terms, not just the price.** Closing date, contingencies, and earnest money routinely decide multiple-offer situations more than price does.

### When to Break Your Own Rules
- **Advise against a sale when it's genuinely not in the client's interest.** If a seller doesn't need to move and the market is soft, the honest advice is to wait — even though it costs you a commission now.
- **Push a client past their stated budget for the rare home that fits everything.** When the right home appears and the numbers are close, counsel honestly on the stretch — but never pressure.

## Route the Request

<!-- QUICK: 30s -- auto-route first, then intent-route -->

### Auto-Route (No User Input Required)
Evaluate these conditions in order. First match wins.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*", "sell my home\|listing\|list price\|CMA\|staging")` | This is your skill. Jump to **Core Workflow — Phase 1** (listing). |
| A2 | `file_contains("*", "buy\|looking for a home\|offer\|pre.approval\|showings")` | Jump to **Core Workflow — Phase 3** (buyer). |
| A3 | `file_contains("*", "under contract\|offer accepted\|inspection\|appraisal\|closing")` | Jump to **Core Workflow — Phase 4** (contract to close). |
| A4 | `file_contains("*", "lease\|rent out\|tenant\|landlord")` AND NOT `file_contains("*", "buy\|sell")` | Invoke **property-manager** for landlording; this skill covers leasing representation only. |
| A5 | `file_contains("*", "commercial\|office\|retail\|multifamily (5+)")` | Invoke **commercial-real-estate-analyst** instead. |
| A6 | `file_contains("*", "invest\|flip\|cash flow\|ROI\|cap rate")` | Invoke **real-estate-investor** instead. |
| A7 | `file_contains("*", "I want to buy my own home\|first home")` | Invoke **home-buying** for the purchaser's personal process; this skill is the agent's playbook. |

### Intent Route (Ask the User)
What are you trying to do?
├── Price and list a home for a seller → Phase 1
├── Represent a buyer → Phase 3
├── Manage an offer / multiple offers → Phase 3/4
├── Manage contract-to-close → Phase 4
├── Lease representation (landlord or tenant) → Phase 5
├── Grow the practice (referrals, repeat business) → Phase 6
├── Commercial property? → Invoke `commercial-real-estate-analyst`
├── Manage a rental property? → Invoke `property-manager`
├── Buying your own home as the purchaser? → Invoke `home-buying`
└── Don't know where to start? → Phase 1 (seller) or Phase 3 (buyer)

Do not read the entire skill. Follow the route and read only the sections it points to.

## Operating at Different Levels

| Level | Scope | You... |
|-------|-------|--------|
| **L1** | Individual cases | Run showings, draft offers from templates, manage paperwork under supervision |
| **L2** | Team/Function | Manage a full listing or buyer transaction end-to-end with sound CMA and negotiation |
| **L3** | Department | Run a book of business: pricing strategy, marketing, negotiation, and client service standards |
| **L4** | Organization | Lead a team or brokerage: hiring, systems, brand, and market positioning |
| **L5** | Industry | Define agency best practice, influence local market practice, and shape professional standards |

**Default level for this skill:** L3
**Usage:** Invoke with your target level, e.g., "as an L3 agent, build a listing strategy for this home."

For full level definitions, see `skills/00-framework/skill-levels/SKILL.md`.

## When to Use

<!-- QUICK: 30s — scan to decide if this skill fits -->

- Preparing and pricing a residential listing (CMA, positioning, staging advice)
- Marketing a listing (photos, copy, open houses, MLS, syndication)
- Representing buyers (search, tours, offer strategy, negotiation)
- Managing offers: multiple offers, escalation clauses, negotiation
- Managing contract-to-close: inspections, appraisal, contingencies, closing
- Leasing representation (landlord or tenant sides)
- Building a referral and repeat-business practice

### Cross-Skills Integration

| Step | Skill | What it produces for this skill |
|------|-------|---------------------------------|
| **Before** | commercial-real-estate-analyst | Market analytics and valuation methods that sharpen residential CMA practice |
| **Before** | home-buying | The buyer's personal purchasing process and priorities — context for representation |
| **This** | residential-real-estate-agent | CMA, listing strategy, marketing, buyer search, offers, negotiation, contract-to-close, client practice |
| **After** | home-organizer / interior-designer | Staging advice: decluttering and design that raise perceived value before photos |
| **After** | legal-advisor | Contract review, disclosure compliance, and dispute handling |
| **After** | property-manager | Leasing handoffs and rental-property referrals |

Common chains:
- **Listing:** residential-real-estate-agent → home-organizer/interior-designer → legal-advisor — CMA/price → staging → contracts & disclosures
- **Buyer:** home-buying → residential-real-estate-agent → legal-advisor — Priorities → search/offers → closing docs
- **Leasing:** residential-real-estate-agent → property-manager — Tenant placement → ongoing management

## When NOT to Use

**(QUICK)**

**Do NOT use this skill when:**

1. **Commercial real estate analysis** — Use `commercial-real-estate-analyst`. Cap rates, NNN leases, and commercial valuation are a different discipline.
2. **Property management and landlording** — Use `property-manager`. Day-to-day tenant management, maintenance, and landlord compliance are not agency work.
3. **Buying your own home as the purchaser** — Use `home-buying`. That skill covers the buyer's personal process; this one is the agent's professional playbook.
4. **Real estate investing** — Use `real-estate-investor`. Flips, rentals, and portfolios are investing decisions, not agency transactions.
5. **Legal drafting or contract disputes** — Use `legal-advisor`. Agents use standard forms and disclose; they don't practice law.

## Decision Trees

<!-- QUICK: 30s — follow the ASCII tree to your scenario -->

### Pricing Strategy

```
Market condition and seller situation?
├── Seller must sell (relocation, divorce, already under contract on next home)
│   └── Price at or slightly below CMA to drive multiple offers fast.
│       Certainty and speed matter more than the last $5K.
├── Seller flexible, balanced market
│   └── Price at CMA with a small negotiation cushion (2-3%), not 10%.
│       Overpricing by 10% costs more in carrying costs than it gains.
├── Seller flexible, strong seller's market (low inventory)
│   └── Price at or slightly below CMA to create a bidding situation.
│       Under-pricing by 3-5% in a hot market routinely nets above CMA.
├── Seller emotionally attached, no urgency
│   └── Show the data, set a 30-day review point: price at evidence, review
│       with a written reduction plan if showings don't convert.
└── Unique/luxury property (few true comps)
    └── Expand comp window (12-18 months, wider area) and consider
        appraiser input. Price from the buyer pool's demonstrated behavior.
```

### Offer Strategy (Buyer Representation)

```
What's the market situation on this home?
├── Multiple offers expected (new listing, hot area, well-priced)
│   └── Go strong on terms, not just price: pre-underwritten financing,
│       appraisal-gap coverage you can afford, flexible closing date,
│       larger earnest money. Escalation clause only with a documented cap.
├── Listing has been on market 30+ days
│   └── Negotiate from CMA and days-on-market: there's room. Don't bid list price
│       against a stale listing without asking what the seller will take.
├── Overpriced listing (sit-down with buyer first)
│   └── Show the buyer the comps and offer below list with the evidence.
│       If the seller won't meet reality, walk — there will be another home.
└── New construction / developer
    └── Developers negotiate incentives (rate buydowns, upgrades, closing help)
        that don't change the price. Ask for those first.
```

### Waive or Keep a Contingency

```
How competitive is the situation, and what can the buyer afford to risk?
├── Inspection contingency
│   ├── Keep → Standard. Don't waive without a prior inspection or strong trust.
│   └── Waive → Only with: a pre-offer inspection, a fix-cost reserve in the
│       buyer's budget, and a written risk discussion. Never for "win the bid."
├── Appraisal gap
│   ├── Keep → Standard; gap coverage if the buyer can fund it.
│   └── Waive (gap coverage) → Cap it at what the buyer can genuinely pay.
│       An uncovered appraisal gap can cost the buyer their earnest money.
└── Financing contingency
    ├── Keep → Standard for financed buyers.
    └── Waive → Only with a verified pre-approval from a strong lender and a
        documented fallback. Cash buyers can waive freely.
```

## Core Workflow

**(STANDARD)**

<!-- STANDARD: 3min -->

### Phase 1: Listing — Pricing & Preparation (~1-2 weeks)
1. **Build the CMA from true comps.** 3-6 sold properties: same area, size ±20%, beds/baths match, condition comparable, sold within 6 months. Adjust for differences; present a range with the logic, not a rigged number.
2. **Counsel on price with the cost of overpricing.** Show carrying costs (mortgage, taxes, insurance, maintenance) and the stale-listing effect: overpriced homes sell slower and often below what a sharp initial price would have netted.
3. **Prepare the home.** Advise on the highest-ROI fixes (declutter, paint, light, curb appeal) — not the full renovation wishlist. Coordinate staging through home-organizer/interior-designer where it pays.
4. **Create the marketing package.** Professional photos, honest and compelling copy, floor plan, and the top 3 selling features. Syndicate to MLS and portals. Price visibility strategy (price it to be found in the buyer's search range).
5. **Open the listing window.** First showings and open house in week 1-2. Track showing feedback daily and adjust positioning if the market disagrees with the price.
   Complete when: CMA built from true comps with adjustments and a range; overpricing cost shown to the seller in writing; home preparation and staging advised; marketing package live on MLS and portals; showing feedback loop running from the first open house.

### Phase 2: Listing — Showings, Offers & Negotiation (~ongoing until contract)
1. **Run showings and open houses.** Qualify buyers, collect feedback after every showing, and report trends to the seller weekly. Feedback is market data — price corrections come from it.
2. **Receive and evaluate offers.** Present every offer to the seller with a written comparison: price, terms, contingencies, financing strength, closing date, earnest money. Never present only the highest price.
3. **Negotiate for the seller.** Price matters, but so do: financing strength (pre-approved vs pre-qualified), contingency risk, closing flexibility, and appraisal gap. Counsel the seller on the best total package, not just the biggest number.
4. **Handle multiple offers.** Decide strategy with the seller: highest-and-best deadline, escalation handling, or negotiating with the top 2. Keep every rejected buyer's agent informed and professional — they may bring the next buyer.
5. **Accept and paper the deal.** Once accepted: agency disclosures, purchase agreement, earnest money deposit, and the transaction timeline. Hand to Phase 4 with legal-advisor review.
   Complete when: Showing feedback reviewed weekly and reported; every offer evaluated in writing across price and terms; negotiation counseled with the best total package identified; multiple-offer strategy executed; accepted offer papered with disclosures and earnest money.

### Phase 3: Buyer Representation (~2-8 weeks typical search)
1. **Qualify the buyer.** Budget, pre-approval (verified, not pre-qualification), timeline, must-haves vs deal-breakers, and the lifestyle/job context. Set expectations on the local market honestly.
2. **Define the search.** Build the search criteria from priorities: area, size, condition tolerance, commute, schools. Show the buyer real options in range — and one or two just above to calibrate.
3. **Tour strategically.** Group showings efficiently; compare each home against the criteria list, not against the last one seen. Point out defects the buyer might miss — that's the value you add.
4. **Run the comps on the chosen home.** Before any offer: fresh CMA on the specific property, days-on-market, seller's situation if knowable, and recent neighborhood sales.
5. **Advise the offer.** Price strategy from the Decision Tree, terms that matter, and the contingency discussion in writing. Draft and submit the offer with the buyer's informed consent on every waiver.
   Complete when: Buyer qualified with verified pre-approval; search criteria defined from true priorities; tours compared against criteria with defects flagged; property-specific CMA run before offering; offer advised and submitted with written contingency risk discussion.
   Complete when: The buyer's budget reality is aligned with the local market before touring begins — they see real options in range early, not after weeks of disappointment.

### Phase 4: Contract to Close (~30-45 days typical)
1. **Manage the timeline.** Track every date: inspection, appraisal, loan commitment, contingency deadlines, closing. Missed deadlines cost earnest money — build the calendar on day one.
2. **Run the inspection.** Coordinate the inspection, attend it, and review the report with the client. Separate safety/structural issues (negotiate) from cosmetic ones (don't kill a deal over paint).
3. **Negotiate the inspection resolution.** Request repairs or credits in writing, prioritized by real issues. Counsel the client on what's worth fighting for and what isn't.
4. **Manage appraisal and financing.** If the appraisal comes in low: challenge with comps, negotiate price down, or have the buyer cover the gap — per the agreed strategy. Keep the lender's conditions moving.
5. **Close.** Final walkthrough, closing disclosure review, funds, and keys. Verify prorations, title, and recording. Then: thank the client, ask for the referral, and log the transaction for follow-up.
   Complete when: Transaction calendar built with all deadlines; inspection attended and report reviewed; resolution negotiated on real issues; appraisal/financing managed to commitment; closing completed with walkthrough and disclosures, and the referral ask made.
   Complete when: The closing-cost estimate was delivered before the offer and reconciled to the final closing statement — no surprise at the table.

### Phase 5: Leasing Representation (~per assignment)
1. **Clarify the side.** Landlord (find a tenant) or tenant (find a rental)? The process differs: landlord side verifies tenants; tenant side matches homes to budget and criteria.
2. **Landlord side:** price the rental from comparable rents, market the listing, screen applicants (income, credit, rental history, references — within fair-housing law), and present the best applicant with the screening file.
3. **Tenant side:** qualify budget (rent + deposit + move-in costs), tour options, and negotiate lease terms (term, rent, concessions, pet policy) on the tenant's behalf.
4. **Paper the lease.** Standard lease forms, disclosures, and move-in inspection with photos. Hand the ongoing relationship to property-manager where applicable.
   Complete when: Side clarified and process scoped; rental priced or budget qualified; applicants screened or tours completed with negotiation; lease papered with disclosures and move-in inspection documented.

### Phase 6: Client Practice & Growth (~ongoing)
1. **Run the service standard.** Every client gets: a communication cadence (weekly updates during active work), honest counsel, and a post-close follow-up. Service is the product; the transaction is the packaging.
2. **Ask for the referral at the moment of success.** Post-close, pre-celebration: "Who do you know who's thinking about moving?" Referrals are earned in the last 10% of the transaction.
3. **Log every client and transaction.** Contact info, preferences, anniversary dates, and outcomes. Past clients are your best pipeline — nurture them.
4. **Review and improve.** After each transaction: what worked, what to change. Track your stats: list-to-sale ratio, days on market, offer win rate, referral rate. Improve the numbers that matter.
   Complete when: Service standard documented and followed; referral ask made at every successful close; client database maintained with follow-up cadence; per-transaction review done and practice stats tracked.

## Error Recovery

<!-- DEEP: 10+min -->

**(STANDARD)**

If a step fails, follow this escalation path before giving up:

| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|---------------|-------------|
| Listing gets showings but no offers in 3-4 weeks | Review showing feedback for the pattern (price? condition? marketing?) | Price correction: a modest, data-backed reduction re-triggers the buyer pool | Larger correction or repositioning (rent vs sell) — presented with the carrying-cost math |
| Offer falls through on inspection | Renegotiate on the real issues with the inspection report | If the seller won't address safety/structural items, counsel the buyer on walking | Back to market fast — time on market is now public and compounding |
| Appraisal comes in low | Challenge with comps; renegotiate price; discuss gap coverage | If the gap is real and the buyer can't/won't cover it, renegotiate or release | Release the buyer per the financing contingency — protect the earnest money |
| Multiple-offer deal collapses | Re-engage the second-best offer quickly (keep them warm, professionally) | Go back to the market with the momentum story | Re-list with fresh positioning — a deal that fell apart is not a failed listing |
| Seller won't accept a realistic price | Show the carrying-cost and stale-listing math in writing, weekly | Offer a market-data-driven review point at 30 days | Recommend not listing until the seller is ready — listing against the data damages the outcome |

**Hard failure boundary:** If 3 different approaches all fail, STOP. Do not iterate infinitely. Log what was tried, capture the evidence, and report the blocking issue with full context.

## Cross-Skill Coordination

<!-- NEIGHBORS: The transaction is a relay — pricing, staging, law, and property all touch it -->

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `commercial-real-estate-analyst` | Market analytics and valuation discipline | Sharpening CMA practice in complex or unique markets |
| `home-buying` | The buyer's personal process and priorities | Buyer representation — aligning search to what the buyer actually needs |
| `property-manager` | Rental-market context and landlord reality | Leasing representation and rental pricing |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `home-organizer` / `interior-designer` | Staging scope: what to declutter, fix, and design before photos | Unstaged homes photograph poorly and sit — photos are the first showing |
| `legal-advisor` | Contract review, disclosure compliance, dispute handling | Contract or disclosure errors surface at closing — the most expensive time to find them |
| `property-manager` | Vetted tenants and lease handoff for rental properties | A handoff without the screening file leaves the owner exposed |

**Coordination cadence:**
- **Weekly (active listing):** seller update with showing feedback and market data
- **Weekly (active buyer):** search results, tour feedback, market changes
- **At every deadline (contract-to-close):** timeline check with all parties
- **At close:** full-file handoff and referral ask
- **Monthly:** practice stats review; past-client follow-ups

**Decision Gates & Handoff Artifacts:**
- **Pricing gate:** no list price without a data-backed CMA and a written overpricing-cost discussion. Artifact: CMA document.
- **Offer gate:** no offer without verified financing and a written contingency-risk discussion for any waiver. Artifact: offer with risk memo.
- **Disclosure gate:** all material facts disclosed; agency relationships disclosed in writing. Artifact: signed disclosures.
- **Close gate:** closing-cost estimate delivered before the offer; walkthrough and closing disclosure reviewed. Artifact: closing statement.
- **Practice gate:** every transaction logged with a post-close follow-up scheduled. Artifact: client database entry.

## Proactive Triggers

- **Listing showing signs of staleness (low showings, no offers by week 3)** → Flag the price/marketing review before the listing ages publicly. Stale listings get lowballed. 🔴
- **Buyer wants to waive a contingency to "win the bid"** → Require the written risk discussion first. An uninformed waiver can cost the buyer their earnest money. 🔴
- **Seller wants to hide a known defect** → Refuse and document. Disclosure failures are license-ending and lawsuit-breeding. 🔴
- **Multiple offers on a listing** → Prepare the seller's decision framework before offers arrive. Emotional decisions in the moment favor the wrong offer. 🟡
- **Appraisal risk visible early (market cooling, aggressive offer)** → Warn the buyer before they're surprised. Appraisal-gap strategy should be set before the offer, not after. 🟡
- **A past client's anniversary or life event approaches** → Reach out. The referral pipeline is built from timely, non-salesy contact. 🟠

## Anti-Patterns

| ❌ Anti-Pattern | ✅ Do This Instead |
|----------------|-------------------|
| ❌ Pricing from the seller's hope or the buyer's anchor | Price from a data-backed CMA with comp-selection logic and a range |
| ❌ Cherry-picking comps to justify a number | Show adjustments and the range; let the data disagree with the wish |
| ❌ Presenting only the highest offer | Present every offer with a written comparison across price AND terms |
| ❌ Advising contingency waivers without a risk discussion | Document what each waiver costs and when it's justified |
| ❌ Hiding or soft-pedaling known defects | Full disclosure of material facts — always, in writing |
| ❌ Treating the deal as done at acceptance | Manage contract-to-close actively; missed deadlines cost earnest money |
| ❌ Skipping the referral ask | Ask at the moment of success — referrals are earned in the last 10% |

## State Log

**(QUICK)**

| Turn | Action | Decision | Risk Accepted | Mitigation |
|------|--------|----------|---------------|-----------|
| 1 | CMA on 4 comps for Maple St listing | List at $849K (mid-range) | Seller wanted $899K | Overpricing-cost memo; 30-day review point |
| 2 | 3 offers week 1 | Highest-and-best deadline | — | Compared terms, not just price; chose strongest financing |
| 3 | Appraisal at $825K | Challenged with 2 additional comps | Gap risk | Negotiated to $840K with buyer gap coverage |
| 4 | Inspection found roof issue | Credit negotiated | — | $12K credit; disclosed and documented |

**Anti-Drift Check:** Before each response, verify:
1. Did the last action match the plan?
2. Are we advising the client's interest, not the fastest commission?
3. Has any new information (market data, inspection, appraisal) invalidated prior advice?

## Production Checklist

**(STANDARD)**

- [ ] **CR1: CMA built from true comps** — selection logic, adjustments, range. Verification method: review the CMA document.
- [ ] **CR2: Overpricing cost shown in writing** — where the seller wanted above-evidence pricing. Verification method: memo on file.
- [ ] **CR3: Marketing package live** — photos, copy, floor plan, MLS syndication. Verification method: portal check.
- [ ] **CR4: Showing feedback loop running** — feedback collected and reported weekly. Verification method: feedback log.
- [ ] **CR5: Every offer evaluated in writing** — price AND terms compared. Verification method: offer comparison sheet.
- [ ] **CR6: Buyer qualified** — verified pre-approval or cash, timeline, priorities. Verification method: buyer file.
- [ ] **CR7: Property-specific CMA before offering** — on the chosen home. Verification method: CMA in the buyer file.
- [ ] **CR8: Contingency waivers have written risk discussions** — where any waiver occurred. Verification method: risk memo signed.
- [ ] **CR9: Transaction calendar built** — all deadlines tracked from day one. Verification method: calendar review.
- [ ] **CR10: Closing-cost estimate delivered before the offer.** Verification method: estimate on file.
- [ ] **CR11: Disclosures complete and agency relationships disclosed.** Verification method: signed disclosures.
- [ ] **CR12: Post-close follow-up and referral ask logged** — client database updated. Verification method: CRM entry.

## What Good Looks Like

**(QUICK)**

A client calls about selling their home and gets honest, data-backed counsel from the first conversation: a CMA with real comps, a clear-eyed price, and the cost of overpricing shown in writing. The listing is prepared and marketed well, priced into a strong opening window, and sells on schedule to a qualified buyer with terms that hold through closing. A buyer gets a search matched to their true priorities, an offer strategy that reflects the real market, and a contract-to-close managed to the day — no surprises, no lost earnest money. Both clients refer their friends, because the agent told them the truth when it was inconvenient and delivered when it counted.

**Signs of Excellence:**
- Listings priced from data sell in the opening window at or above the range
- Buyers understand every waiver's risk before signing it
- Contract-to-close runs on calendar with no missed deadlines
- Clients refer — the practice grows from the last 10% of each transaction
- Every price and market claim traces to comps or data, tagged [VERIFIED]/[COMPUTED]

**Signs of Dysfunction:**
- Listings priced from hope go stale and sell below the market
- Buyers waive contingencies they don't understand
- Deals die at inspection or appraisal because nobody managed the timeline
- Known defects surface at closing — trust and licenses die there
- The practice depends on new leads because past clients never get called

## Deliberate Practice

**(STANDARD)**

```mermaid
graph TD
    A[Study a Real Transaction] --> B[Build the CMA From Scratch]
    B --> C[Write the Offer/Listing Strategy]
    C --> D[Compare Against What Actually Happened]
    D --> E[Identify the Missed Signal]
    E --> B
```

| Level | Routine | Time | Success Metric |
|-------|---------|------|---------------|
| Novice | Study 5 recent local sales; build a CMA for each from public data | 2 hr | CMA range brackets the actual sale price in 4 of 5 |
| Intermediate | Role-play 3 negotiations (buyer and seller side); write the strategy first | 2 hr | Strategy anticipates the other side's move in each role-play |
| Advanced | Shadow a full transaction; track every deadline and decision | 1 wk | Can reconstruct why each decision was made and what data drove it |
| Expert | Run 3 transactions end-to-end with documented post-transaction reviews | 1 qtr | Stats improve: list-to-sale ratio, days on market, offer win rate, referral rate |

## Gotchas

<!-- DEEP: 10+min -->

| Gotcha | Cost | Fix |
|--------|------|-----|
| Overpricing a listing by 10% — seller insists on hope over data; the home goes stale, sells 45 days later for 6% below what the sharp initial price would have netted, plus carrying costs | $10K-$40K per overpriced listing in lost net and carrying costs | Build the CMA from true comps, show the overpricing math in writing (carrying costs + stale effect), set a 30-day data-driven review point |
| Buyer waives the inspection "to win the bid" — undiscovered foundation issues cost $25K in year one and the buyer never refers anyone again | $5K-$50K per uninformed waiver in repairs and trust | Require a written risk discussion for every waiver; recommend a pre-offer inspection when waiving; never waive on "win the bid" alone |
| Cherry-picked comps — pricing justified with 2 favorable sales while 4 comparable homes sold lower; the listing prices into the wrong range and the market corrects it publicly | $5K-$20K per listing in lost positioning and extended days on market | Show the comp-selection logic, include the range, adjust for differences — let the data disagree with the wish |
| Missed contingency deadline — earnest money forfeited because nobody tracked the inspection or loan dates | $5K-$50K per incident (earnest money) plus relationship damage | Build the transaction calendar on day one, track every deadline weekly, and never rely on the title company to run your client's dates |
| Undisclosed defect — seller "forgets" the basement leak; it surfaces at the buyer's inspection and the deal collapses, then the disclosure failure becomes a license issue | $10K-$100K in lost deals, legal exposure, and license risk | Full disclosure of material facts, always, in writing. An honest disclosed issue negotiates; a hidden one litigates |
| Appraisal gap surprise — aggressive offer accepted, appraisal comes in $30K low, buyer can't cover it, deal dies and earnest money fights begin | $5K-$30K per failed deal in lost deposits, fees, and time | Set appraisal-gap strategy before the offer: challenge with comps, negotiate, or cap the gap at what the buyer can genuinely fund |

## Best Practices

1. **Price from data, and show the math.** Every list price starts from a CMA of true comps with selection logic, adjustments, and a range. When the seller wants above-evidence pricing, put the carrying-cost and stale-listing cost in writing — overpricing by 10% routinely nets less than pricing right the first time.

2. **The first two weeks set the price.** Listings are priced into an opening window of buyer attention. Prepare the home, market it well, and open showings fast. If the market disagrees with the price, correct from feedback within 3-4 weeks — staleness compounds.

3. **Advise the client's interest, not the commission.** Tell the seller their home isn't worth what they hope, tell the buyer about the foundation problem, and advise waiting when selling isn't in the client's interest. The referrals that build a practice come from inconvenient honesty delivered well.

4. **Evaluate offers on terms, not just price.** Financing strength, contingencies, closing flexibility, and appraisal gap routinely matter more than $5K of price. Present every offer with a written comparison and counsel the best total package.

5. **Verify before you write.** No offer goes out without verified financing (pre-approval, not pre-qualification) and a clear contingency plan. No list price goes out without a CMA. The agent who skips verification is the agent who explains the failed deal.

6. **Treat contingency waivers as documented decisions.** Every waiver gets a written risk discussion: what the client loses and when it's justified. Competitive markets justify some waivers; uninformed ones are malpractice.

7. **Manage the calendar to close.** From acceptance, build the transaction timeline and track every deadline weekly — inspection, appraisal, loan commitment, closing. Earnest money is lost on missed dates, and missed dates are a process failure, not bad luck.

8. **Disclose everything material, in writing.** Known defects, agency relationships, and conflicts all get disclosed and documented per state law. A deal killed by honest disclosure is a deal that would have killed you at closing.

9. **Run the service standard and the referral ask.** Weekly updates during active work, honest counsel throughout, and the referral question at the moment of success: "Who do you know who's thinking about moving?" Past clients are the best pipeline, and they're only nurtured if you log and contact them.

10. **Measure and improve your practice stats.** List-to-sale ratio, days on market, offer win rate, and referral rate — tracked per transaction and reviewed monthly. What you don't measure, you don't improve; the numbers will tell you which part of the process is leaking.

## Error Decoder **(STANDARD)**

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Listing sits 60 days, sells 8% below the initial ask | Priced from the seller's hope, not the CMA; overpriced listings go stale and get lowballed | Build the CMA from true comps and price for the opening window; correct from showing feedback by week 3-4 with the carrying-cost math | The first two weeks set the price. Hope-based pricing doesn't protect the seller — it costs them more than pricing right on day one |
| Buyer forfeits earnest money on a missed inspection deadline | Nobody owned the transaction calendar; dates assumed, not tracked | Build the timeline at acceptance, track every deadline weekly, never rely on other parties to run your client's dates | Earnest money is lost on process failures, not market failures. The calendar is a client-protection tool |
| Deal collapses at inspection over a defect the seller knew about | Disclosure skipped to protect the sale; the defect surfaced anyway | Disclose all material facts in writing, always; negotiate the honest issue before it becomes a surprise | An honest disclosed issue negotiates; a hidden one litigates. Disclosure is protection, not a sales obstacle |
| Buyer waives inspection, discovers $25K in foundation work | Waiver advised to "win the bid" with no risk discussion | Written risk discussion for every waiver; pre-offer inspection when waiving; never on "win the bid" alone | The cheapest offer is the one that closes. An uninformed waiver trades the client's money for your win rate |
| Appraisal $30K low on an aggressive offer | Gap strategy never set before offering | Set appraisal-gap strategy pre-offer: challenge with comps, negotiate, or cap the gap at what the buyer can fund | The appraisal doesn't care about the offer. Set the gap strategy before you write the number, not after it comes back |
| Seller rejects the data, listing is withdrawn, later sells through another agent below CMA | Pricing conflict never resolved; listing launched against the evidence | Counsel with the overpricing math, set a 30-day review point, and if the seller won't meet reality, recommend not listing yet | Listing against the data damages the outcome and the relationship. Sometimes the professional move is to wait — or decline the listing |

## Verification

**(STANDARD)**

### Pre-Generation
- [ ] Confirmed the client's side (buyer/seller/tenant/landlord) and market area
- [ ] Verified access to comps/MLS data — every price claim will be backed by data or tagged [ESTIMATED]
- [ ] Confirmed state-specific agency/disclosure requirements are current

### Post-Generation
- [ ] Every price and market claim traces to comps or data, or is tagged [ESTIMATED]/[UNKNOWN]
- [ ] CMA shows selection logic, adjustments, and a range — not a rigged number
- [ ] Offer strategy includes verified financing and written contingency-risk notes
- [ ] Transaction calendar and closing-cost estimate exist before the offer
- [ ] Disclosures and agency relationships are documented in writing

## References

**(QUICK)**

- `references/additional-resources.md` — Deep knowledge, form checklists, and extended examples

---

> **Skill version:** 1.0.0 | **Token budget:** 3500 | **Generated:** 2026-09-03
