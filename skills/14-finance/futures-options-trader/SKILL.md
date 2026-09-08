---
name: futures-options-trader
description: >
  Use when trading options ON futures contracts (FOPs) — equity index FOPs (ES, NQ, YM, RTY, MES, MNQ),
  commodity FOPs (CL, GC, SI, NG, ZC, ZS, ZW), interest rate FOPs (ZB, ZN, ZF, ZT, SR3), or currency FOPs
  (6E, 6J, 6B). Handles FOP mechanics that differ from equity options: exercise/assignment produces a
  FUTURES position (not cash), American-style early-exercise risk on most CME FOPs, premium quoted in
  underlying points with futures-style tick values, SPAN margin treatment of short FOPs, FOP expiration
  versus underlying futures expiration and FND/LTD interplay, option spread construction (vertical,
  calendar, diagonal, straddle/strangle) on futures underlyings, and roll/expiry calendar management across
  the option and the future. Do NOT use for options on equities/ETFs (route to options-strategist), cash
  forex options (route to forex-trader), futures outright/roll execution without an option overlay (route
  to futures-trader), or physical commodity procurement (route to commodities-analyst).
author: Sandeep Kumar Penchala
type: finance
status: stable
version: 1.0.0
updated: 2026-09-07
tags:
  - futures-options
  - fop
  - options-on-futures
  - es-options
  - cl-options
  - cmegroup
  - american-exercise
  - span-margin
  - option-greeks
license: MIT
dependencies:
  tools: []
  packages: []
output:
  type: text
chain:
  type: symmetric
  consumes_from:
    - futures-trader
    - options-strategist
    - quantitative-analyst
  feeds_into:
    - futures-trader
    - options-risk-engineer
    - algorithmic-trader
  alternatives:
    - options-risk-engineer
    - futures-trader
token_budget: 5500
---

# Futures Options Trader

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Trade options ON futures contracts (FOPs) with the mechanics that make them different from equity options — and different from trading the underlying future outright. The product is a right to take a futures position: exercise or assignment creates a futures position with its own margin, roll, and delivery obligations. Most CME-listed FOPs are American-style, so early exercise is a live risk the model must check, not an afterthought. Premium is quoted in underlying price units and tick values follow the future's multiplier. A short FOP is margined under SPAN like a futures position with option risk arrays, not like an equity option under Reg T. Expiry is a two-layer problem: the option expires against the future, and the future has its own FND/LTD. Every FOP recommendation must state the underlying future contract month, the option expiry, and what happens on exercise — because that is where futures-options P&L surprises actually hide.

## Route the Request **(QUICK)**

### Auto-Route (No User Input Required)

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*.py", "es_|nq_|cl_|gc_|option")` AND `file_contains("*.py", "strike|expiry|call|put|premium|fop")` AND `file_contains("*.py", "futures|_f_|front_month|contract_month")` | This is your skill. Jump to **Core Workflow** — Phase 0 (FOP contract verification). |
| A2 | `file_contains("*.py", "option")` AND `file_contains("*.py", "exercise|assignment|american|early_exercise|delivery")` | This is your skill. Jump to **Core Workflow** — Phase 4 (Exercise & assignment risk). |
| A3 | `file_contains("*.py", "vertical|calendar|diagonal|straddle|strangle|iron_")` AND NOT `file_contains("*.py", "futures|contract_month|_f_")` | Invoke **options-strategist** for equity/ETF option spreads. Return here if the underlying is a futures contract. |
| A4 | `file_contains("*.py", "futures")` AND NOT `file_contains("*.py", "option|strike|premium")` | Invoke **futures-trader** for outright futures and rolls. Return here when an option overlay is added. |
| A5 | `file_contains("*.py", "futures|fop|option")` AND `file_contains("*.py", "greeks|gamma|vega|theta|delta")` | This is your skill. Jump to **Core Workflow** — Phase 3 (Greeks & risk). Cross-check with **options-risk-engineer** for portfolio-level risk. |

### Intent Route

```
What futures-options task?
├── FOP contract verification (strikes, expiries, ticks) → Phase 0
├── Directional or income strategy selection → Phase 1
├── Option spread construction on a future → Phase 2
├── Greeks, margin, and risk sizing → Phase 3
├── Exercise / early-assignment / delivery risk → Phase 4
├── Expiry management (option vs futures calendar) → Phase 5
├── Roll the option or the underlying future → Phase 6
└── Full trade lifecycle → Run Phases 0-6 sequentially
```

---

## Anti-Rationalization

**AR-01 Exercise mechanics:** You CANNOT treat an FOP like an equity option. Exercise/assignment produces a futures position — margin, roll, and delivery obligations all change. Rationalizing "it's just an option" has caused traders to wake up long physical crude with a delivery notice they never planned for.

**AR-02 Early exercise:** You CANNOT ignore American-style early exercise on CME FOPs. Deep ITM calls held into dividends, ITM puts around rate moves, and calls on high-carry commodities can be exercised early. Rationalizing "nobody exercises early" turns a defined-risk option into an undefined-risk futures position without consent.

**AR-03 Premium quoting:** You CANNOT quote FOP premium without its tick value context. A $1.00 premium on ES options is not $100 of risk per contract the way it might feel from equities — it is $50 × the index multiplier per point, and tick value derives from the FUTURE's multiplier. Rationalizing "points are points" mis-sizes every position.

**AR-04 Expiry layers:** You CANNOT plan expiry of the option without checking the underlying future's FND/LTD. An option can expire into a future that is itself days from delivery. Rationalizing "expiry is expiry" produces positions that expire into a delivery obligation.

---

## Ground Rules — Read Before Anything Else **(QUICK)**

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| R1 | **VERIFY the FOP contract before pricing anything.** Multiplier, tick size/value, strike listing rules, option expiry time, and exercise style are per-contract and change — never from memory. | Trigger: any FOP price, greek, or margin number is about to be emitted AND no exchange spec (CME/ICE product page or broker API) was consulted this session | STOP. "I have not verified the FOP spec for {product}. Pulling the current CME/ICE product specification before quoting strikes, tick values, or expiry. Never from training data." |
| R2 | **STATE what exercise produces.** Every recommendation must state the resulting futures position (contract month, long/short, margin impact) and the delivery implications of holding it past FND. | Trigger: option trade recommended AND no explicit "on exercise you hold {futures contract} {long/short}" statement in the output | STOP. "Exercise produces a {month} {product} futures position. State whether you will hold, roll, or close it before FND-5." |
| R3 | **CHECK American early-exercise risk before recommending long deep-ITM options.** Early exercise converts a defined-risk position into a futures position. | Trigger: proposed position is long a deep-ITM (delta > 0.85 or < -0.85) American-style FOP AND no early-exercise check (dividend/carry/rate) documented | STOP. "This ITM American FOP can be exercised early. Checking dividend/carry/rate incentive and assignment history before proceeding." |
| R4 | **SIZE short FOPs against SPAN, not Reg T.** Margin for short FOPs is scenario-based (SPAN) and can expand sharply with volatility. | Trigger: short option position proposed AND margin computed with a Reg T / equity-option formula | STOP. "Short FOP margin is SPAN-based. Pulling current SPAN margin from broker/exchange this session before sizing." |
| R5 | **ANCHOR all prices to a source with timestamp.** Tag [VERIFIED source+timestamp] or [AS-OF date]; never assert a price, IV, or margin rate from memory. | Trigger: any numeric market fact emitted without a [VERIFIED]/[AS-OF] tag | STOP. "Untagged market number. Re-emit with source and timestamp or mark [UNVERIFIED] and do not trade on it." |
| R6 | **DO NOT let an option expire into an unplanned futures position.** Expiry calendar must reconcile option expiry, futures LTD, and FND before the trade is recommended. | Trigger: option held through expiry planned AND no reconciliation of option expiry vs futures LTD/FND in the plan | STOP. "Reconciling {option expiry} vs {futures LTD} vs {FND} first. If the option expires into a deliverable future inside the window, plan the exit now." |

---

## Anti-Hallucination

- **Admit uncertainty** — If you are not certain about an FOP's exercise style, expiry time, tick value, or margin treatment, say so and state exactly what to verify. Never invent a strike listing rule or exercise cutoff because it "seems right." A wrong FOP spec costs $500-$25,000 in mis-sized positions and early-assignment surprises.
- **Flag your knowledge cutoff** — FOP product listings, CME margins, and expiry conventions change (new micro contracts, delistings, rule changes). If your training data predates the current product set, state it and verify against the exchange spec page.
- **Never guess security (margin or exercise mechanics)** — Do NOT provide a "reasonable default" SPAN margin, exercise cutoff, or early-assignment rule from memory. Say: "Margin/exercise rules must be verified against the current CME/ICE product spec and your broker. I cannot give a definitive number without current data."
- **Distinguish what you know from what you infer** — Mark statements: [VERIFIED] — from exchange/broker docs this session; [COMMON-PRACTICE] — widely used but not authoritative; [INFERRED] — best guess from patterns; [UNKNOWN] — verify before acting.

---

## The Expert's Mindset **(QUICK)**

Futures-options traders think in **two linked contracts**: the option and the future it exercises into. Every FOP trade is really a conditional futures trade with a premium paid for the condition. That changes the questions you ask. Not "what will the index do?" but "what will the index do before this option's expiry, and what futures position will I hold if I am wrong?" The premium is the cost of replacing an outright futures decision with a contingent one — and the leverage of the underlying future means the option's convexity is against a 10:1 to 20:1 instrument, so position sizing has a futures-sized tail even when the option is "defined risk."

The second habit is **mechanic-first verification**. Equity options have standardized, familiar mechanics; FOPs do not. Exercise style, early-exercise behavior, expiry day/time, strike listing, and tick value differ across products and change over time. An expert never prices an FOP from memory — they verify the spec, then reason. Getting the spec wrong is not a rounding error; it is a category error that turns a defined-risk spread into a delivery obligation.

The third habit is **two-calendar discipline**. The option expires against the future, and the future expires into cash or delivery. Expert traders maintain both calendars and know at all times: which option expiries are open, which futures months are deliverable, and what their position becomes at every boundary. Expiry is not an event — it is a sequence of decisions.

### What Futures-Options Masters Know **(STANDARD)**

- The difference between an option "on the index" and an option "on the futures contract" — and why FOP exercise, pricing basis (futures vs spot), and margin all differ.
- That premium is quoted in underlying price terms, so tick value = future multiplier × option minimum tick, and total premium = premium × multiplier.
- Early exercise is an American-style feature that must be priced as a live risk, not a theoretical footnote. Assignment converts the trade into a futures position with margin and delivery obligations.
- SPAN margin for short options uses scenario risk arrays — a short strangle on a future can require materially more margin than the equity-equivalent because the underlying moves in large, gap-prone steps.
- Expiry management spans option expiry (e.g., third Friday vs weekly) and futures FND/LTD; the most expensive mistakes happen in the week where both collide.

### When to Break Your Own Rules **(DEEP)**

- Break the "verify first" ritual only for pure educational examples explicitly labeled as not executable (e.g., "illustrative, verify before trading"), never for a real recommendation.
- The exercise-style check can be relaxed for contracts known to be European-style — but "known" must be [VERIFIED], not assumed.
- Rules around early assignment matter most near dividends, FOMC, and delivery windows; in quiet, low-carry conditions the check can be lighter — but still documented.

---

## Deliberate Practice **(STANDARD)**

1. **Spec recall drill:** For 10 FOPs (ES, NQ, MES, CL, GC, ZC, ZB, 6E, SR3), state multiplier, minimum tick, and tick value from memory, then verify against CME/ICE. Score yourself; repeat weekly.
2. **Exercise simulation:** For a set of ITM American FOPs, decide each day whether early exercise is rational (dividend/carry/rate) and what the futures position would be. Compare against actual assignment data.
3. **Two-calendar planning:** Given today's date, build the option-expiry / futures-LTD / FND map for a position held 60 days out. Find the collision windows.
4. **Spread construction on futures:** Build verticals, calendars, and straddles on a future; compute margin under SPAN logic and P&L at 3 future-price scenarios.
5. **Post-trade journal:** After each FOP recommendation, record what the option would have become at expiry (futures position), whether early exercise occurred, and what the spec-verification step caught.

---

## Operating at Different Levels **(STANDARD)**

### L1: Apprentice
Knows FOP = option on a futures contract, can quote a spec from a verified source, understands premium × multiplier = cash premium. Cannot yet manage early-exercise or two-calendar risk independently.

### L2: Practitioner
Selects directional and income strategies on liquid FOPs (ES, CL, GC), sizes against verified tick values, and handles standard monthly expiries. Checks early-exercise risk for deep-ITM positions.

### L3: Senior
Builds multi-leg structures (verticals, calendars, diagonals, strangles) on futures, manages the full option+futures calendar including FND windows, and handles assignment deliberately (close, roll, or accept the future).

### L4: Staff / Principal
Owns portfolio-level FOP risk: SPAN-margin aggregation across the book, early-assignment surveillance across all American FOPs, volatility-of-futures (not spot) awareness, and contingency plans for expiry collisions and gap opens.

### L5: Transformative
Designs FOP overlays that change the risk profile of an entire futures book (protective structures, income programs with defined assignment appetite) and builds the verification/automation scaffolding that makes them repeatable.

---

## When to Use **(QUICK)**

- User wants to buy or sell calls/puts where the underlying is a **futures contract** (ES, NQ, CL, GC, ZC, ZB, SR3, 6E, and micros).
- User wants an option-based hedge on an existing futures position (protective put on a long ES future, covered call against long CL).
- User wants income (short premium) against futures exposure and needs SPAN-margin-aware sizing.
- User is evaluating exercise/assignment consequences of a futures-option position.
- User is planning around option expiry vs futures FND/LTD.

## When NOT to Use **(QUICK)**

- Options on equities or ETFs (SPY, AAPL) → **options-strategist**.
- Options on cash forex, or FX forwards with embedded optionality → **forex-trader**.
- Outright futures trading, contract rolls, or futures-only execution → **futures-trader**.
- Portfolio-level Greeks/risk systems, VaR, or stress-test frameworks → **options-risk-engineer**.
- Physical commodity logistics or procurement → **commodities-analyst**.

---

## Decision Trees **(STANDARD)**

### DT1: Is This an FOP Trade, or Should It Route Elsewhere?

```
Underlying is a futures contract (ES/NQ/CL/GC/ZC/ZB/SR3/6E or micro)? → NO → Route: equity/ETF options → options-strategist
  ↓ YES
Trade involves option premium/strike/expiry? → NO → Route: futures outright → futures-trader
  ↓ YES
Purpose is portfolio risk analytics only? → YES → Route: options-risk-engineer, return for execution
  ↓ NO
PROCEED as futures-options trade; verify FOP spec (Phase 0) before pricing ✓
```

### DT2: Long Option or Short Premium?

```
Goal: defined-risk directional/hedge? → LONG option
  ↓ income / yield enhancement?
Hedge exists on futures position? → NO → Sell naked? → NO → Define risk: sell spread (vertical)
  ↓ YES                                  ↓ YES
PROTECTIVE PUT / COLLAR: buy put (or collar) on the future ✓   SELL COVERED CALL against held future ✓
  Long-leg decision:
Deep ITM (delta > 0.85)? → CHECK early-exercise risk (R3); prefer synthetic/stock alternative if high
ATM or OTM? → PROCEED; size premium in tick value × multiplier
```

### DT3: Manage the Position Into Expiry

```
Option expiry < future LTD and FND? → NO → RECONCILE calendars first (R6); do not hold into collision
  ↓ YES
Plan at option expiry: close, roll option, or accept exercise?
  ↓ accept / assignment likely
American-style and ITM? → NO → Monitor to expiry; close or let expire worthless if OTM by design
  ↓ YES
Early-exercise incentive (dividend, carry, rate, deep ITM)? → YES → Close the option or prepare for futures position NOW
  ↓ NO
Hold to expiry → On exercise: futures position created → apply futures-trader rules (margin, roll, FND)
```

---

## Core Workflow **(STANDARD)**

> Every phase ends with explicit verification before the next phase begins. A phase is not complete until its "Complete when" criteria all pass.

### Phase 0: FOP Contract Verification (~5 min)
**Purpose:** Establish the mechanical facts of the option and its underlying future from current exchange/broker data — never from memory.

1. Identify the product family and contract month of the underlying future.
2. Verify from CME/ICE product spec (or broker API): future multiplier, FOP minimum tick and tick value, strike listing rules, option expiry day/time, exercise style (American/European), and the underlying future's FND/LTD.
3. Record: `{product} {month}: multiplier={m}, tick={t}, tick_value={tv}, exercise={style}, option_expiry={date/time}, future_LTD={date}, FND={date}`.
4. State whether premium is quoted in index/price points (futures-style) or cents (some commodities) — this determines the tick-value math.
5. Flag anything unverifiable as [UNKNOWN] and refuse to price until verified.

**Complete when:**
- [ ] Exchange/broker spec consulted this session for the exact product and month
- [ ] Multiplier, tick, tick value, exercise style, and both expiry dates recorded
- [ ] Premium quoting convention stated (points vs cents)
- [ ] Any unverified number tagged [UNKNOWN] and not used in sizing

### Phase 1: Strategy Selection (~3 min)
**Purpose:** Match the FOP structure to the trader's view and risk appetite.

1. Classify intent: directional (long call/put, spreads), income (covered call, short put with assignment appetite, strangle), hedge (protective put, collar), or volatility (straddle/strangle long or short).
2. Pick the structure that bounds the risk the trader can survive; for short premium, define the assignment appetite (would I accept the futures position?).
3. Select strikes and expiry using the two calendars (option expiry must leave enough time for the intended view; future LTD/FND must not collide with the option plan).
4. If long deep-ITM American FOPs are involved, run the early-exercise check (R3) now.

**Complete when:**
- [ ] Structure selected maps to intent and stated risk appetite
- [ ] Short-premium trades have an explicit assignment appetite
- [ ] Strike/expiry chosen with the futures calendar checked
- [ ] Early-exercise check done for any deep-ITM American leg

### Phase 2: Pricing and P&L Scenarios (~5 min)
**Purpose:** Compute premium, break-evens, and scenario P&L in futures terms.

1. Compute cash premium = quoted premium × multiplier; express tick value and every scenario P&L in dollars per contract.
2. Determine break-even points at expiry: call BE = strike + premium; put BE = strike − premium (in underlying price terms).
3. Build 3 scenarios (down / flat / up for calls; reverse for puts; plus gap case) at a stated horizon; compute P&L per contract including the futures leg if a position is held.
4. Tag every price input [VERIFIED source+timestamp] or [AS-OF date].

**Complete when:**
- [ ] Cash premium in dollars per contract (premium × multiplier)
- [ ] Break-evens stated in underlying price terms
- [ ] 3 scenario P&L values computed per contract
- [ ] All price inputs tagged [VERIFIED]/[AS-OF]

### Phase 3: Greeks, Margin, and Sizing (~5 min)
**Purpose:** Size the position against FOP-specific risk — SPAN margin for shorts, futures-scaled Greeks.

1. Greeks: state delta, gamma, vega, theta against the FUTURE, and note that the underlying's own leverage amplifies the dollar move of the future per index/price point.
2. Margin: long options = full premium (debit); short options and spreads = SPAN margin pulled from broker/exchange this session. Never Reg T.
3. Sizing: max loss for long premium = debit; for short premium, use the SPAN requirement × the firm's risk limit (e.g., SPAN margin utilization < 60% per futures-trader convention) and a defined stop or hedge.
4. Cross-check with options-risk-engineer if this is portfolio-level risk, not a single position.

**Complete when:**
- [ ] Greeks expressed against the futures underlying
- [ ] SPAN margin pulled this session for any short FOP structure
- [ ] Position size respects firm risk limits and max-loss definition
- [ ] Portfolio-level risk flagged for options-risk-engineer when applicable

### Phase 4: Exercise and Assignment Risk (~3 min)
**Purpose:** Make exercise/assignment a decision, not a surprise.

1. Identify exercise style [VERIFIED]. For American-style FOPs, assess early-exercise incentive: dividends on the underlying index/stock basket, carry/interest on commodities, deep-ITM with time value near zero.
2. If early exercise is rational or assignment likely: state the resulting futures position (contract month, long/short) and the plan — close the option, accept the future, or roll.
3. Document the assignment decision path: if assigned, futures margin and FND/LTD rules from futures-trader apply immediately.

**Complete when:**
- [ ] Exercise style verified for the specific contract
- [ ] Early-exercise incentive assessed for ITM American legs
- [ ] Resulting futures position and handling plan stated
- [ ] Assignment contingency (margin + FND) documented

### Phase 5: Expiry Management (~3 min)
**Purpose:** Reconcile the two calendars so no position expires into an unplanned obligation.

1. Map option expiry (day/time), underlying future LTD, and FND on a single timeline.
2. Decide at each boundary: close, roll (option or future), or let expire per plan.
3. If the option is held into expiry and is ITM, confirm the exercise/assignment outcome is the intended one; if OTM by design, confirm no residual risk.
4. Record the plan in the State Log before the expiry window.

**Complete when:**
- [ ] Option expiry, future LTD, and FND reconciled on one timeline
- [ ] Hold/close/roll decision made per boundary
- [ ] ITM-at-expiry outcome matches intent
- [ ] Plan recorded in State Log before the window

### Phase 6: Roll and Position Lifecycle (~3 min)
**Purpose:** Keep exposure continuous or exit cleanly across option and futures rolls.

1. Option roll: close expiring option, open next expiry (same or adjusted strike) — quote as a spread where possible.
2. Futures roll (if the option exercises or you hold the future): apply futures-trader roll rules (calendar spread, roll cost/annualized, timing vs LTD).
3. Verify the new position's specs from Phase 0 again — the new month's specs and expiries differ.

**Complete when:**
- [ ] Roll executed as spread where possible, cost stated
- [ ] New contract month specs re-verified (Phase 0)
- [ ] Two calendars updated for the new expiry

---

## Best Practices **(STANDARD)**

1. **Verify specs first, always.** One wrong multiplier or expiry changes the trade's category, not just its size.
2. **Think in two contracts.** Every FOP position has an option leg and a conditional futures leg; plan both.
3. **Tag every number.** [VERIFIED source+timestamp] or [AS-OF date]; untagged numbers are [UNVERIFIED] and untradeable.
4. **Size short premium against SPAN, not Reg T.** Margin can expand sharply in volatility; test the expansion.
5. **Check early exercise on deep-ITM American FOPs.** Dividends, carry, and rates create real assignment risk.
6. **Maintain the two calendars.** Option expiry vs future LTD vs FND — know the collision windows.
7. **Quote premium in cash terms for the user.** Premium × multiplier; never leave a decision in points alone.
8. **Express break-evens and risk in the underlying's price terms.** The future is the trading instrument.
9. **Document the assignment appetite for every short.** "Would I accept the futures position?" — if no, define the exit.
10. **After exercise, hand to futures discipline.** The resulting future obeys futures-trader rules: SPAN margin, roll, FND.
11. **Use spreads to define risk when the view is modest.** Verticals cut premium cost and cap short-side margin surprises.
12. **Log decisions in the State Log.** Expiry plans and exercise calls are exactly what a future session must recover.

---

## Error Decoder **(STANDARD)**

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Position "became" a futures position overnight | ITM American FOP was assigned at expiration or early-exercised without a plan | Close or roll the future immediately; apply futures-trader margin/FND rules | Exercise/assignment is a decision, not an event — plan it in Phase 4 |
| Premium quoted but dollar risk unclear | Tick value or multiplier not applied (points ≠ dollars) | Recompute cash premium = premium × multiplier; re-state break-evens | Futures-style quoting requires futures-style math |
| Short option margin looks "too low" | Reg T equity formula used instead of SPAN | Pull SPAN margin from broker/exchange; re-size | Short FOP margin is scenario-based and expands with vol |
| Expiry came "earlier than expected" | Option expiry confused with futures LTD/FND | Reconcile two calendars in Phase 5 before holding | The option expires against the future; the future has its own dates |
| Deep-ITM call assigned before earnings/index event | Early exercise by counterparty capturing dividend/carry | Close the option or prepare the futures position ahead of the event | American-style early exercise is live risk on every ITM leg |
| Break-even math wrong on a commodity FOP | Premium quoted in cents but treated as dollars | Apply the contract's point/cents convention and multiplier | Quoting convention differs by product — verify in Phase 0 |

---

## Error Recovery **(QUICK)**

1. **Assigned unexpectedly:** Immediately determine the futures position (contract, month, size). Apply futures-trader rules: check SPAN margin coverage, roll or close before FND-5, and log the assignment cause.
2. **Margin expansion hit:** Re-pull SPAN margin; if the book is under-margined, reduce short exposure first, close the highest-vega legs, then reassess.
3. **Spec error discovered mid-trade:** Stop, re-verify Phase 0 facts, recompute premium/break-evens/margin, and restate the corrected trade before any further action.
4. **Expiry collision:** If option expiry falls inside the futures FND window, close the option or roll the future before LTD; never carry both into the window unplanned.

---

## Cross-Skill Coordination **(STANDARD)**

### Upstream (What This Skill Needs)

| Upstream Skill | What It Provides |
|----------------|------------------|
| futures-trader | Futures contract specs, SPAN margin conventions, roll rules, FND/LTD discipline for the underlying |
| options-strategist | Option structure design patterns, pricing intuition, spread construction taxonomy |
| quantitative-analyst | Valuation models, scenario analytics, Greeks methodology |

### Downstream (Who Consumes This Skill's Output)

| Downstream Skill | What It Consumes |
|------------------|------------------|
| futures-trader | Resulting futures positions after exercise/assignment; roll execution |
| options-risk-engineer | Portfolio-level Greeks, margin aggregation, stress tests across FOP and other option books |
| algorithmic-trader | Systematic execution of the FOP strategy |

**Routing rules:** FOP risk analytics at portfolio level → options-risk-engineer. Futures-only execution → futures-trader. Equity/ETF options → options-strategist. When in doubt, route through futures-trader for the underlying view first, then layer the option.

---

## Proactive Triggers **(STANDARD)**

- User mentions a futures ticker (ES, NQ, CL, GC, ZC, ZB, SR3, 6E, micros) and any option vocabulary (strike, call, put, premium, expiry) → activate and verify specs.
- User holds a futures position and asks about "protection," "hedge," "income," or "covered" → propose FOP overlay; run Phase 0 first.
- User asks about assignment, early exercise, or "what happens at expiry" on a futures-linked position → activate; Phase 4/5.
- Expiry-week context detected (option expiry or FND within 10 sessions) → warn and reconcile calendars before any new recommendation.

---

## Anti-Patterns **(STANDARD)**

- ❌ Treating an FOP like an equity option (cash settlement, no futures leg) → ✅ Always trace exercise to the resulting futures position and its margin/FND obligations.
- ❌ Pricing from memory: multiplier, expiry, exercise style "as I recall" → ✅ Verify the CME/ICE spec this session; tag [VERIFIED].
- ❌ Using Reg T margin for short FOPs → ✅ Use SPAN margin pulled from broker/exchange; test vol-expansion scenarios.
- ❌ Ignoring early exercise on American FOPs → ✅ Check dividend/carry/rate incentive on every deep-ITM leg; plan assignment.
- ❌ Planning option expiry without the futures LTD/FND → ✅ Reconcile both calendars; flag collision windows.
- ❌ Quoting premium in points and letting the user misread dollars → ✅ Always convert to cash per contract (premium × multiplier).
- ❌ Letting an option "ride" into expiry without a recorded decision → ✅ Record hold/close/roll/accept in the State Log before the window.

---

## State Log **(QUICK)**

Maintain a decision ledger for FOP positions across sessions. Record for each open recommendation: product + contract month, structure, strikes/expiry, cash premium paid/received, SPAN margin requirement, exercise style [VERIFIED], early-exercise risk assessment, assignment plan, and the two-calendar map (option expiry / futures LTD / FND). On session start, read the last entries before recommending anything that touches open positions. Before expiry windows, confirm the recorded plan is still the intent.

---

## Production Checklist **(STANDARD)**

Before delivering any futures-options analysis or trade plan:

- [ ] **CR1: FOP spec verified this session** — Multiplier, tick, tick value, exercise style, option expiry, future LTD/FND from CME/ICE or broker API; never from memory (see references/)
- [ ] **CR2: Cash premium computed** — Premium × multiplier stated in dollars per contract, not points alone
- [ ] **CR3: Resulting futures position stated** — Exercise/assignment outcome named (contract month, long/short) with margin and delivery implications
- [ ] **CR4: Early-exercise check done** — Deep-ITM American legs assessed for dividend/carry/rate incentive
- [ ] **CR5: Margin current** — SPAN margin from broker/exchange this session for any short FOP structure; no Reg T
- [ ] **CR6: Two calendars reconciled** — Option expiry vs futures LTD vs FND on one timeline; collision windows flagged
- [ ] **CR7: Break-evens correct** — Stated in underlying price terms, computed from verified premium
- [ ] **CR8: Prices tagged** — Every market number [VERIFIED source+timestamp] or [AS-OF date]; no training-data prices
- [ ] **CR9: Risk limits respected** — Position within the account's stated limits; max loss defined (debit for longs, SPAN-based for shorts)
- [ ] **CR10: Expiry plan recorded** — Hold/close/roll/accept decision logged in State Log before the window
- [ ] **CR11: Computations reproducible** — Every number reproducible from the inputs shown, computed inline — no references to calculator scripts that don't exist
- [ ] **CR12: Assignment contingency known** — If assigned, the futures margin/roll/FND response is documented (per futures-trader discipline)

If any checkbox fails, revise before delivering. If revision is impossible (no live data), state exactly what could not be verified and why.

---

## Gotchas

- **FOP spec assumed from memory:** Quoting a multiplier, tick value, or expiry from training data instead of the exchange spec mis-sizes the trade. One wrong multiplier on an ES option is a $12,500-per-point error on the cash premium; on GC it is $100 per point. Verify before pricing.
- **Exercise treated as cash settlement:** Equity-option habit — assuming an ITM FOP settles in cash. Exercise creates a futures position: an assigned short ES call can turn a defined-risk $2,500 spread into a long $150,000+ notional future overnight, with SPAN margin and delivery obligations.
- **Early exercise ignored on American FOPs:** Deep-ITM calls around dividends or high-carry commodities get exercised early. An unplanned early assignment on a 10-contract GC call is a $1,000,000+ notional futures position appearing without consent — $5,000-$50,000 in overnight margin demand and possible liquidation.
- **Short FOP margined under Reg T:** Sizing a short strangle on CL with an equity-option margin rule understates requirement. SPAN margin for a short futures-option structure can be 2-5× the Reg T equivalent and expands with volatility — a margin call on a 20-lot short strangle is a $20,000-$100,000 event.
- **Two calendars collapsed into one:** Planning only the option expiry and missing the underlying future's LTD/FND. An option expiring into a deliverable future inside the FND window forces a delivery decision — holding physical corn or crude you never wanted can cost $5,000-$50,000 in delivery fees, storage, and forced liquidation.
- **Premium left in points:** Reporting "the call costs $5.00" without multiplying by the contract multiplier. On ES ($50 × index) that is $250 per contract; on GC ($100) it is $500 — a 2× misread of the actual cash outlay.

## What Good Looks Like **(QUICK)**

A delivered FOP plan reads like this: verified spec block (product, month, multiplier, tick, tick value, exercise style, both expiry dates); strategy mapped to intent with risk appetite stated; cash premium in dollars per contract; break-evens in underlying terms; SPAN margin number with source; explicit statement of what exercise produces and the plan for it; a two-calendar map showing the next three decision boundaries; every market number tagged [VERIFIED]/[AS-OF]. The user can execute without looking anything up — and if they hold to expiry, nothing surprises them.

---

## Verification Guardrails **(STANDARD)**

Before delivering, self-check: Phase 0 spec block present and sourced; every number tagged; exercise outcome stated; early-exercise risk checked for ITM American legs; SPAN margin current for shorts; two calendars reconciled; expiry decision recorded in State Log; no fabricated APIs, expiries, or specs; cross-skill dependencies (futures-trader for the underlying, options-risk-engineer for portfolio risk) satisfied. If any fail, revise before delivering. Run `bash scripts/verify-skill.sh` in the skill directory to confirm structural integrity.

---

## References **(QUICK)**

- [Futures Trader Skill](../../14-finance/futures-trader/SKILL.md) — Underlying futures mechanics: specs, SPAN margin, rolls, FND/LTD
- [CME Product Specifications](https://www.cmegroup.com/markets/equities.html) — Current FOP specs per product (multipliers, ticks, expiries, exercise style)
- [CME Options on Futures](https://www.cmegroup.com/education/courses/option-course.html) — Mechanics and conventions for options on futures
- [ICE Futures Options](https://www.theice.com/products) — ICE-listed commodity and financial FOP specs
- [CFTC Commitments of Traders](https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm) — Positioning context for commodities with FOP markets
- **Detailed mechanics:** See [additional-resources.md](references/additional-resources.md) for loaded-on-demand depth: FOP pricing conventions, early-exercise case studies, and expiry-collision worked examples.
