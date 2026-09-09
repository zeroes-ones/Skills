---
name: services-engagement-pricing
description: >
  Use when pricing client-facing software engagements for freelancers, agencies, or
  consultancies — choosing between hourly, fixed-bid, time-and-materials, retainer, and
  value-based models; converting an effort estimate into a quote range with buffer; building
  rate cards from salary/overhead/profit; applying engagement-category multipliers (C2C, B2C,
  B2B, B2G); or drafting SOW-ready pricing with assumptions and change control. Handles
  billable-hours math, effective-rate checks, not-to-exceed caps, milestone billing, and
  re-quote triggers. Do NOT use for product pricing strategy (enterprise-pricing-strategist),
  for producing the underlying effort estimate (software-project-estimator), or for running a
  sales pipeline (revops-manager).
license: MIT
tags:
- pricing
- rate-card
- fixed-bid
- time-and-materials
- retainer
- value-based
- freelancer
- agency
- consulting
- sow
- quote
author: Sandeep Kumar Penchala
type: sales
status: stable
version: 1.0.0
updated: 2026-09-09
token_budget: 4000
chain:
  examples:
  - skills/15-sales/services-engagement-pricing/examples/backtest
  consumes_from:
  - software-project-estimator
  - software-maintenance-support-estimator
  - consulting-effort-estimator
  feeds_into:
  - software-project-estimator
  - software-maintenance-support-estimator
  - consulting-effort-estimator
---
# Services Engagement Pricing
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Price a client-facing software engagement from an effort estimate: choose the pricing model,
build or check the rate card, apply engagement-category and market multipliers, add an explicit
buffer, and produce SOW-ready pricing with assumptions and change control. Used by freelancers,
agencies, and consultancies selling **project work** — not product pricing.

## <!-- DEEP: 5+min --> RESEARCH_PREREQUISITE — Execute Before Any Output

**This is a HARD GATE. Do not quote a price before completing this research.**

| # | Research Step | Why It Matters | Where to Look |
|---|--------------|----------------|----------------|
| **RP1** | **Get the real effort estimate** (low/base/high from software-project-estimator) with its assumptions register. | [CONTEXT_VIOLATION] Pricing without an estimate is a guess with a dollar sign. | software-project-estimator output |
| **RP2** | **Know your costs.** Salary target, overhead %, profit target, realistic billable hours, or firm multiplier. | [STALE_RISK] Rates decay with inflation and your costs; a 2-year-old rate card is a loss-maker. | Your books, accountant, market rate data |
| **RP3** | **Classify the engagement category** (C2C/B2C/B2B/B2G) and the buyer's procurement reality. | [MISPOSITION] Category drives 2–4× pricing differences; misclassifying leaves money on the table or loses the deal. | Buyer persona, procurement rules, RFP |
| **RP4** | **Tag every figure [VERIFIED]/[COMPUTED]/[ESTIMATED]** (rates, multipliers, buffer). | [HALLUCINATION_GUARD] A confident wrong price is worse than an honest range. | This skill's references, docs/estimation-research.md |
| **RP5** | **List what a fixed price must cover** and what it must NOT (change control boundary). | [FAILURE_BLINDNESS] Fixed-bid risk is scope risk; the clause list is the product. | SOW templates, past disputes |
| **RP6** | **Map downstream consumers** — the quote feeds the SOW, the invoice schedule, and (if ongoing) the maintenance estimate. | [CASCADE_BLINDNESS] A bad price poisons delivery, finance, and the support quote that references it. | Cross-skill coordination table |

### 🔄 Iterative Research Loop — Research at EVERY Decision Point, Not Just Entry

Re-check costs/category/competition at each fork (model choice, rate level, buffer size)
before committing the number.

## Anti-Hallucination

- Never quote from a single point estimate; use the low/base/high and price the **base** with
  an explicit buffer.
- Never invent "market rate" — name the source (survey, your actuals, 3 real comparables) or
  mark it [ESTIMATED] with a wide band.
- Every line of the SOW pricing must trace to an estimate line or a stated pricing rule.
- If you cannot compute your own break-even rate, you are not ready to quote fixed price.

## Route the Request

### Auto-Route (No User Input Required)

- "What should I charge for <project>?" → this skill (effort estimate first, then model + rates).
- "Should I do fixed or T&M for this client?" → Decision Tree 1.
- "How do I set my hourly/day rate?" → Decision Tree 2 + Phase 2.
- "How much retainer should I ask for?" → Decision Tree 3.

### Intent Route (Ask the User)

If unclear, ask up to 3 questions: (1) do you have the effort estimate (low/base/high)?
(2) engagement category: individual (C2C/B2C), business (B2B), or government (B2G)?
(3) who carries the risk you prefer — fixed = you, T&M = client?

## Ground Rules — Read Before Anything Else

1. **Price from costs up, then sanity-check against the market** — never from the market alone.
2. **Billable hours are ~1,200–1,400/yr for a solo operator** (60–70% utilization), never 2,080.
3. **Fixed price = your risk; T&M = the client's risk.** Charge accordingly (buffer on fixed,
   caps on T&M). Never quote fixed from a single-point estimate.
4. **Retainer is a premium, not a discount** — you are selling guaranteed availability.
5. **Always show the buffer and assumptions**; SOW money without assumptions is a dispute
   waiting to happen.
6. **Category multiplier reality:** B2B generally prices 2–4× B2C-equivalent work; B2G adds
   compliance cost and slower payment terms.
7. **Re-quote at ~15–20% scope change**; below that, absorb with visible notes only if you
   documented the boundary.

## The Expert's Mindset

### What Masters Know That Others Don't

- Effective rate ≠ billed rate: unbilled calls, proposal time, admin, travel and slow-paying
  invoices routinely add 15–40% on top of billed hours. Price the *effective* number.
- Multiplier pricing is how firms survive overhead: billing rate ≈ direct pay × overhead factor
  (2.0–3.7×) × profit markup (1.10–1.25).
- Risk transfer is a pricing decision: every model choice moves money between you and the
  client; pricing is negotiating who eats the uncertainty.
- The best quotes are built like estimates: decomposed, ranged, and auditable. Clients pay for
  the feeling that you know your numbers.

### When to Break Your Own Rules

- Early-career: hourly/day-rate builds the actuals you need before you can quote fixed safely
  (≈10–20 similar projects).
- High-demand, provable-outcome work: value-based pricing can beat any cost-plus number — but
  only with inbound demand and measurable results.

## Operating at Different Levels

| Level | Mode | Model | Signature move |
|---|---|---|---|
| L1 Apprentice | New freelancer | Hourly/day rate | Track actuals to enable fixed bids later |
| L2 Practitioner | Freelancer | Hourly + fixed for simple scopes | Buffer on fixed (15–20%) |
| L3 Senior | Agency/consultancy | Fixed/T&M/retainer mix | Risk split by model; milestone billing |
| L4 Lead | Firm | Cost-plus multiplier + value levers | Overhead-factor rate card, category tiers |
| L5 Transformative | Strategic partner | Value/outcome-based | Priced on results, with guardrails |

## When to Use

| Use this skill | Instead use |
|---|---|
| Client-facing project price / quote / SOW | `enterprise-pricing-strategist` (product price) |
| Converting an effort estimate to money | `revops-manager` (pipeline) / `sales-engineer` (demo) |
| Retainer or support price | `software-maintenance-support-estimator` |
| Estimating effort first | `software-project-estimator` |
| Deciding payment terms legally | `legal-advisor` / SOW counsel |

## Decision Trees

### Decision Tree 1: Choose the pricing model by scope + risk appetite

| Situation | Model | Guardrails |
|---|---|---|
| Clear deliverable, defined end, you know the work | Fixed-bid | Buffer 15–25%; assumptions + change control |
| Evolving/unknown scope (R&D, discovery, post-launch) | T&M | Not-to-exceed cap, low/high ranges, burn reports |
| Ongoing access/availability need | Retainer | Price as premium; hours bucket or deliverables |
| Measurable outcome + strong positioning | Value-based | Define the metric and the floor before agreeing |
| New relationship, unknown delivery cost | Hourly/day | Track actuals; move up as data accumulates |
| Big project, client wants budget ceiling | Hybrid | Fixed for scoped slice + T&M for iteration |

### Decision Tree 2: Build/check your rate

| Input | Rule of thumb |
|---|---|
| Target income (salary you aim to earn) | Start here (not current draw) |
| Overhead | 25–40% of labor; rule of thirds (⅓ comp / ⅓ overhead / ⅓ tax+margin) |
| Profit target | 15–25% above costs (solo); multiplier firms 1.10–1.25 on loaded cost |
| Billable load | 1,200–1,400 hrs/yr solo; ~220 billable days |
| Formula | (salary + overhead + profit) ÷ billable hours → then compare to market |
| Firm shortcut | direct pay × 2.0–3.7 overhead factor × profit markup |

### Decision Tree 3: Engagement-category multiplier

| Category | Typical pricing | Adjustments |
|---|---|---|
| C2C (individual ↔ individual) | Lowest per-unit | Small scopes; simple terms |
| B2C (you → consumer) | 1× base | Volume-sensitive; fixed simple scopes |
| B2B (you → business) | 2–4× base | Procurement rigor, structured SOW, slower pay |
| B2G (you → government) | 3–5× base effort cost | Compliance, reporting, long cycles, payment lag |

## Core Workflow

### Phase 1 (~10 min): Collect Inputs

1. Pull the effort estimate (low/base/high + assumptions) from `software-project-estimator`.
2. Confirm the engagement category (Tree 3) and buyer procurement reality.
   - **Complete when:** effort range and category are both named in writing.

### Phase 2 (~15 min): Rate Card

3. Compute break-even rate from your costs (Tree 2), mark [COMPUTED].
4. Cross-check against 3 real comparables or a named market source; record the spread.
   - **Complete when:** you have a [COMPUTED] break-even rate and a named market check, and you
     can state the utilization assumption behind it.

### Phase 3 (~10 min): Price the Engagement

5. Choose the model (Tree 1) and apply its rule: fixed → base + 15–25% buffer; T&M → rate ×
   low/high range with cap; retainer → monthly premium with hours/deliverables bucket;
   value → outcome metric + floor.
6. Apply the category multiplier (Tree 3) when pricing to market.
   - **Complete when:** quote range and model-specific numbers are computed with visible basis.

### Phase 4 (~10 min): Milestones & Terms

7. Set milestone billing aligned to deliverables (e.g., 30/30/30/10 or phase gates).
8. Add payment terms (net-30/45, deposit %), late-payment line, and expense pass-through.
   - **Complete when:** billing schedule and payment terms are explicit.

### Phase 5 (~10 min): SOW Pricing & Change Control

9. Write the price section: scope boundary, price, buffer, assumptions register, out-of-scope
   list, and the 15–20% re-quote trigger.
10. Hand the SOW-ready pricing to legal/procurement or the client; if the engagement includes
    ongoing support, send the build figure to `software-maintenance-support-estimator`.
    - **Complete when:** SOW pricing block is complete and handoff targets are named.

## Best Practices

- Sell a range with a named base ("base $48K, range $44–56K depending on assumptions A–C").
- Never discount the rate; discount the scope. Scope cuts protect the economics.
- Invoice on milestones you can prove (demo, sign-off, deploy) — cash flow is pricing too.
- Raise rates for new clients at least yearly; keep a rate log with win/loss reasons.

## Error Decoder

| Symptom | Root cause | Fix |
|---|---|---|
| Fixed jobs always blow up | No buffer / no change control | Buffer 15–25%; re-quote at scope trigger |
| You're the cheapest and busiest | Market-anchored pricing, no cost floor | Price from costs; raise; lose some deals |
| Cash flow gaps mid-project | Milestones misaligned to spend | Deposit + milestone billing aligned to costs |
| Client ghosts after proposal | Quote without options/assumptions | Offer 2–3 scope/price options |
| Retainer feels like a discount | Priced as bulk hours | Price availability premium + bucket |

## Error Recovery

1. Identify which pricing assumption broke (scope, rate, category, terms).
2. If scope crossed the trigger → re-quote the delta (never silently absorb).
3. If a job is running loss-making → stop, re-scope with the client, and document the lesson in
   the rate log.
4. If a quote was declined → record why (price? terms? trust?) and feed the signal back into
   rate/multiplier calibration.

## Cross-Skill Coordination

### Decision Gates & Artifacts

| Artifact | Consumed by | Trigger |
|---|---|---|
| Effort estimate (L/B/H) | this skill | from software-project-estimator |
| Rate card + multiplier basis | SOW, legal-advisor, accountant | Quote time |
| Build price | software-maintenance-support-estimator | Support quote requested |
| Win/loss data | revops-manager | Pipeline review |

### Communication Triggers — When to Proactively Notify

- Effort estimate changes ≥ 15%: re-quote immediately, notify the client in writing.
- Payment terms slip beyond agreed net: notify finance/accountant for collections.
- Category was misjudged (discovered B2G procurement rules late): stop and re-price before
  signing.

### Escalation Path

If you cannot determine your own cost basis or the legal terms are material, escalate to
`accountant` (cost basis) or `legal-advisor` (SOW) with the quote draft — never sign
unreviewed SOW money.

### Route to Other Skills

Effort input → `software-project-estimator` · legal terms → `legal-advisor` · cost basis →
`accountant` · support/retainer → `software-maintenance-support-estimator` · product pricing →
`enterprise-pricing-strategist`.

## Proactive Triggers

| Trigger | Action | Why |
|---|---|---|
| Scope change ≥ 10–15% | Prepare re-quote before it hits 20% | The trigger loses meaning if you wait |
| New fiscal year / inflation | Rebuild rate card from current costs | Old rates are a hidden discount |
| First enterprise (B2B) deal | Move to structured SOW + category multiplier | B2B ≠ B2C pricing |
| Client asks "what if we add support" | Route to maintenance estimator now | Price support while the build is fresh |

## State Log

Per quote: estimate sha/version, category, model, break-even rate [COMPUTED], market check
source, base price, buffer %, multiplier applied, milestones, payment terms, assumptions
register, SOW status, outcome (won/lost + why).

## Production Checklist

- [ ] Effort estimate attached (range, not point)
- [ ] Break-even rate computed from current costs [COMPUTED]
- [ ] Market check named (comparables or source)
- [ ] Model chosen with reason (risk split stated)
- [ ] Buffer visible (fixed) or cap + burn report (T&M)
- [ ] Category multiplier applied correctly
- [ ] Milestone billing + payment terms explicit
- [ ] SOW price block: boundary, assumptions, out-of-scope, re-quote trigger
- [ ] Complete when the quote draft is saved with date, basis tags, and outcome status
- [ ] Complete when a stranger could recompute the price from the inputs in < 10 minutes

## What Good Looks Like

A one-page SOW price block a procurement officer can act on: scope boundary in one sentence,
base price and range, a visible buffer, milestones with payment terms, an assumptions register,
and a change-control clause — every number traceable to an estimate line or a pricing rule, and
the support-quote path already started if the client will need it.

## Deliberate Practice

- Price the same fake project as C2C, B2C, B2B, and B2G to internalize the multiplier effect.
- Keep a quote log for 6 months: record estimate, quoted price, buffer, and outcome; compute
  your real effective rate quarterly.
- Rebuild a rate card from scratch monthly for one quarter to automate the cost check.

## Anti-Patterns

- Anchoring to the client's budget and reverse-engineering.
- Quoting fixed price from a point estimate with no buffer.
- Pricing from a 3-year-old rate card.
- Discounting the rate instead of the scope.
- Hiding assumptions until after signature.

## Gotchas

- **Effective rate trap:** add 15–40% for unbilled time before judging a "great" hourly rate —
  a "$200/hr" client can be **$4,000–$15,000/yr** cheaper than the sticker implies.
- **B2B ≠ B2C:** same work, 2–4× pricing — mispricing a B2B deal as B2C costs **$10,000–$60,000**
  per engagement.
- **Retainer premium:** guaranteed availability costs you capacity; charging discount retainer
  hours is a **$6,000–$24,000/yr** hidden subsidy.
- **Fixed-price math:** base + 15–25% buffer + assumptions is the floor of a sane fixed quote;
  below that you are subsidizing the client by **$5,000–$20,000** of your own margin.
- **No rate-card refresh:** a 2-year-old rate card under-charges by 10–20% — worth
  **$500–$5,000** per project before you notice.

## When NOT to Use

- Product pricing / SaaS plans → `enterprise-pricing-strategist`, `saas-monetization-strategist`.
- The effort number itself → `software-project-estimator` first.
- Post-launch retainer/SLA pricing → `software-maintenance-support-estimator`.
- Deal pipeline / CRM → `revops-manager`; product demos → `sales-engineer`.
- A quote without a cost basis is not a quote — go build the rate card before pricing.

## Anti-Rationalization

| Rationalization | Rebuttal |
|---|---|
| "Client gave a budget; price to it" | Price from costs, then sanity-check market; anchoring to the budget is how you go negative. |
| "Add the buffer later if scope grows" | A fixed price without a buffer is a **$5,000–$20,000** risk you already accepted. |
| "B2C and B2B are the same work" | Category is 2–4× pricing; mispricing B2B as B2C leaves **$10,000–$60,000** on the table per deal. |
| "Just bill hourly, simpler" | Hourly caps upside and rewards slowness; keep it only while you collect actuals. |

## Ground-Rules Enforcement Matrix

| Rule | Mechanical Trigger | Violation Response |
|---|---|---|
| Cost-based pricing | Quote with no [COMPUTED] break-even rate | Recompute rate before final price |
| Model fits risk | Model chosen without naming who carries risk | State risk split explicitly |
| Buffer visible | Fixed quote with no buffer line | Add buffer or switch model |
| Category applied | No category/multiplier stated | State category + multiplier |
| Assumptions written | SOW price without assumptions | Add register before output |

## Guardrails (repeat before final output)

- Admit uncertainty: no actuals → wider band and a flag, not a confident number.
- Flag your knowledge cutoff: market rate data ages; re-check before quoting.
- Never guess security: compliance-heavy scope (B2G, regulated) quotes a compliance/legal
  review line — do not improvise liability numbers.

## Cross-Skill Upstream Inputs

| Upstream Skill | Input artifact |
|---|---|
| software-project-estimator | effort low/base/high + assumptions |
| software-maintenance-support-estimator | support actuals (rate calibration) |
| sales-engineer (on a team) | buyer/procurement context |

- [`references/patterns-catalog.md`](references/patterns-catalog.md) — backing tables for this
  skill (rate math, models, multipliers, dollar context).

<!-- QUICK: 30s --> <!-- model decision tree first -->
<!-- QUICK: 30s --> <!-- compute break-even rate before any price -->
<!-- QUICK: 30s --> <!-- buffer on fixed, caps on T&M -->

## Verification

| Check | Complete when |
|---|---|
| Cost basis | Break-even rate is [COMPUTED] from salary/overhead/profit/billable-hours |
| Market check | A named source or 3 comparables appear in the quote notes |
| Model fit | The chosen model matches the scope/risk situation in Tree 1 |
| Buffer/caps | Fixed quotes show buffer; T&M quotes show cap or range |
| Category | Engagement category and multiplier are stated |
| Terms | Milestones + payment terms written |
| Change control | 15–20% re-quote trigger and out-of-scope list present |
| Traceable | Price recomputable from estimate + rules in < 10 minutes |

## Verification Guardrails

- No effort estimate attached → do not produce a final price; return a price range with wide
  band and flag the missing input.
- Break-even rate absent → refuse fixed price; offer T&M/hourly only.
- Assumptions register missing → the quote is not SOW-ready; rewrite before output.

## Failure Modes

- **Cost-blind pricing** — trigger: quoting without a computed break-even rate; impact:
  **$5,000–$20,000** per fixed deal subsidized by you.
- **Fixed-price risk transfer** — trigger: buffer skipped on fixed quotes; impact: overrun
  absorbed (typical 30–40%); mitigation: 15–25% buffer + assumptions.
- **Category mispricing** — trigger: B2B priced like B2C; impact: **$10,000–$60,000** per deal
  left behind; mitigation: category multiplier check.
- **Effective-rate blindness** — trigger: judging "great" hourly without unbilled time; impact:
  **15–40%** of income invisible; mitigation: effective-rate calc per client.

## References

- `docs/estimation-research.md` — rate math (1,200–1,400 billable hrs), overhead 25–40%,
  multiplier 2.0–3.7×, B2B ≈ 2–4× B2C, buffer and re-quote norms.
- Xero / HoneyBook / Plutio / Toggl consulting-pricing guides; Deltek consulting pricing
  models; Catalant "Pricing to Win"; Glencoyne hourly-billing guide; ClientCasa
  per-client-profitability; Small Business Chron / Architekwiki billing-rate multipliers.
