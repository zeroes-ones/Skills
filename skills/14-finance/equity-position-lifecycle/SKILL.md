---
name: equity-position-lifecycle
description: >
  Use when you already OWN the shares: "my stock is down 20%", "should I average down", "should
  I sell before earnings", "should I trim, and how much", "cut it or hold", "it's up 40%, take
  profit?", "should I rotate into something better", "do I hold for long-term capital gains".
  Handles the ordered review of an open position, the cadence keyed to the four equity clocks
  instead of DTE, the action router, trigger precedence, and the hold-and-revisit deadline. It
  owns ORDER, CADENCE and PRECEDENCE: whether and how much to trim is decided here, and the lot
  question is not. Do NOT use it to choose the stock (fundamental-analyst,
  technical-signals-engineer, macro-strategist), to pick WHICH lots to sell, or for harvests or
  holding-period timing (equity-tax-lot-and-exit-management), for the margin, borrow or
  liquidity ASSESSMENT (equity-risk-and-capital-engineer), for size (portfolio-signal-manager,
  algorithmic-trader), or a hedge structure (options-strategist, advanced-options-structures).
license: MIT
author: "Sandeep Kumar Penchala"
type: finance
status: active
version: "1.0.0"
updated: 2026-10-14
tags:
  - equity
  - position-management
  - exit-ordering
  - review-cadence
  - hold-or-sell
  - average-down
  - pyramid
  - trim
  - cut
  - rotate
  - hedge
  - tax-lots
  - wash-sale
  - long-term-capital-gains
  - trigger-precedence
token_budget: 4000
chain:
  examples:
  - skills/14-finance/equity-position-lifecycle/examples/backtest
  consumes_from: [equity-tax-lot-and-exit-management, equity-risk-and-capital-engineer, portfolio-signal-manager, trading-decision-data-catalogue, equity-trading-playbook]
  feeds_into: [equity-trading-playbook]
---

# Equity Position Lifecycle

> **Portability target:** spec-level; broker examples are illustrative. Every action here is a decision plus the numbers that decision needs — never a broker-specific command sequence.

<!-- QUICK: 30s -->
The whole skill is one loop: check in a fixed order, route to exactly one action, write the date you will revisit it. If you read nothing else, read the Action Router (DT2) and the Trigger Precedence (DT3).

This skill owns **three things and only three things** for a position that is already open: **DECISIONS**, **ORDER**, and **SCHEDULE**. What it refuses to let happen is a position that is held, unexamined and undeclared — the state in which every avoidable equity loss is born.

---

## Route the Request

### Auto-Route (no user input needed)

| Detected condition | Route |
|--------------------|-------|
| A named open position and no written exit contract | Freeze the name — no adds, no new risk in it — then write the contract |
| "Should I hold / trim / cut / average down / rotate this?" | Action Router (DT2) → Trigger Precedence (DT3) |
| "How often should I look at this?" | Review Cadence by time-axis state |
| A margin call, borrow recall or intraday-margin restriction is live | Precedence rung 1: forced action, and it outranks every opinion below it |
| The close is through the written invalidation level | Precedence rung 2: CUT or CLOSE. Tax is not a counter-argument |
| A loss was realized in this name inside 30 days | Flag the name: the wash-sale window is open — no purchases in it until it closes |
| A winner sits above trim rung 1 with no trim executed | TRIM review before any new entry is discussed |

### Intent Route (ask only when the auto-route does not fire)

1. Is the position open, or still planned? Planned → choose the stock elsewhere (`fundamental-analyst`, `technical-signals-engineer`); this skill starts at the fill.
2. Do you want the **decision** or the **numbers**? Numbers → `equity-tax-lot-and-exit-management` (lots, harvests, holding periods), `equity-risk-and-capital-engineer` (margin, borrow, concentration, liquidity, events), `portfolio-signal-manager` (size).
3. What is the written invalidation level, and when was it last checked? No level → Phase 1 step 2 fails; fix that before anything else is discussed.

---

## Anti-Rationalization

**AR-01 "It's only down on paper":** You CANNOT treat an unrealized loss as unreal. The mark is the price at which the position closes today. *Say instead:* "What is the level, and is the thesis intact at it?"

**AR-02 "I'll average down and fix the basis":** You CANNOT average down as a reflex. The only form of it that is legal here is the five-clause gate in `(references/average-down-honest-form.md)`, and equities have no defined-risk restructure to fall back on. *Say instead:* "Run the gate; if a clause fails, the answer is CUT."

**AR-03 "I'll hold it until it's long-term":** You CANNOT use a tax anniversary as a thesis. The long-term rate changes the *tax* on a sale you had already decided to make; it never turns a sale into a hold. *Say instead:* "Decide the economics first, then choose the date."

**AR-04 "A stock has no expiry, so I can wait":** You CANNOT let the absence of a clock be the plan. Nothing expires an equity position, which is exactly why the deadline has to be manufactured. *Say instead:* "Write the improve-by date and the level today."

**AR-05 "The dividend is free money":** You CANNOT collect a dividend without committing to the holding-period window that makes it qualified, and the ex-date is a price event as well as a cash event. *Say instead:* "Do I want the 61-of-121 commitment, not just the cash?"

**AR-06 "I'll sell the winner and keep the loser":** You CANNOT choose dispositions by which one feels worse. That concentrates the book in its weakest ideas and is a tax tail wagging an economic dog. *Say instead:* "Rank by thesis state, not by the sign of the P&L."

**AR-07 "Just this once":** You CANNOT grant a one-off exception without a written reason, a bounded worst case and a grading date. The exception path is closed to anything less than all three.

**AR-08 "A percentage stop is close enough to a level":** You CANNOT substitute a percentage of entry for a price level. The percentage moves every time the basis moves — exactly the failure the level exists to prevent.

**AR-09 "I'll grade it later":** You CANNOT leave an action ungraded. Until it is graded the position stays flagged unmanaged, and the precedence table cannot be tuned from outcomes nobody wrote down.

---

## Ground Rules

Read these before anything else in this skill. They are mechanical, not aspirational: each has a trigger that can be detected and a response that can be enforced.

| # | Rule | Mechanical Trigger | Violation Response |
|---|------|--------------------|--------------------|
| R1 | The review runs in fixed order 1→8 and stops early | Any review of an open equity position | Restart at step 1. A review that opens at P&L is not a review |
| R2 | Steps 1–3 are gates: any FAIL escalates the position to ACT | FAIL on forced action, thesis/level, or position identity | Write the ACT disposition before any other position is discussed |
| R3 | Every open position carries a written exit contract (level, target, date, events) | Position opened, inherited, gifted or found undocumented | Position frozen: no adds, no new risk in that name, until the contract exists |
| R4 | One action per review, chosen by the router's priority order | Two or more actions qualify | Higher rung wins; the loser is recorded as a standing queued action |
| R5 | HOLD requires a level, a target and a date | Any HOLD on a losing or stalled position | The HOLD is invalid; apply the next action down the router |
| R6 | A cut triggers on a breached level or a broken thesis — never on a P&L percentage | The position is a loser | If no level is on file the position is unmanaged: write the level now, then re-run the review |
| R7 | The wash-sale window freezes trading in the name | A loss was realized in this name within 30 days, forward or backward | No repurchase in the name, in any account, until the window closes |
| R8 | Tax is decided after the economic decision, never instead of it | Two actions differ only by tax | Take the better economic action; apply tax to its *timing*, not to its existence |
| R9 | Any action above HOLD recomputes the position and its band state | ADD, AVERAGE DOWN, TRIM, HEDGE | Incomplete record → the position counts as unmanaged at the next book review |

---

## Anti-Hallucination

- **Admit uncertainty** — if the mark, the share count, the lot set, the cost basis or the account's margin state is not in front of you, say so and fetch it. Never route an action off a guessed number.
- **Flag your knowledge cutoff** — marks, borrow rates, margin schedules, index membership and dividend dates decay within a session. State the timestamp and source of every figure, and re-pull it before acting.
- **Never guess security** — if an action touches order authority, account permissions, or *which shares sit in which lot*, stop and confirm. A trim against the wrong lot, or a hedge written against shares you no longer own, is worse than no action.
- **[VERIFIED]** — every rule attributed to a regulator or exchange names its source (IRC, SEC, FINRA, exchange rules) written next to the tag. Broker-set numbers are `[BROKER-VERIFIED]`; seasonal or behavioural claims are `[COMMON-PRACTICE]`; computed numbers are `[COMPUTED]` with their formula. Past performance is not a guarantee; these are operating bands, approximate by construction, not predictions.
- **Honest scope line** — Form 4, Schedule 13D/13G, Form 13F, §16(b) short-swing and Rule 144 all bind **insiders, affiliates and institutional managers**. If you are an ordinary retail holder, those are **not you**, and this skill does not inflate its risk list by pretending otherwise. They apply only if you are the insider, the affiliate or the 13F filer — in which case that compliance work belongs to counsel, not to a position-review skill.

---

## The Expert's Mindset

A position is not an opinion, it is a commitment with a clock attached. For an equity holder the first question is never "am I up or down" — it is "is the reason I own this still true, and what is forcing me to decide". P&L is an output; the level, the calendar and the account's margin state are inputs. Reviewing the output before the inputs is exactly how a −15% position becomes a −45% position: nothing changed except that nobody looked at the level.

The second habit is arithmetic over narrative, and the third is that the decision set is small and ordered. Every action this skill routes carries a number that must exist before the action is taken — the blended basis, the break-even, the band state after the change, the tax and cost friction of moving, the days left on the anniversary. And when two actions qualify, the router already knows which one wins, because the priority was written down before the loss rather than during it.

### The Four Equity Clocks: Why This Skill Exists

For options, the clock does the work: DTE expires the position whether or not anybody decides anything. **Equities have no such clock.** A stock never expires, never settles to zero because Tuesday arrived, and never sends the margin desk to fetch the decision. So the equity failure mode is the opposite of the options one: **never being forced, therefore never deciding.** This skill's job is to manufacture the deadlines the market will not.

That is not a metaphor. An equity position really does sit on four separate clocks, and every one of them is a date you can write down, check, and be late for.

| Clock | The rule | Source | Analogue of DTE |
|---|---|---|---|
| Settlement | **T+1** since 2024-05-28 | SEC Release 34-96930 | countdown to a forced action |
| Reg T payment / margin call | standard settlement cycle **+ 2 business days = 3 business days** | 12 CFR 220.2, 220.4(c)(3)(i) | countdown |
| Tax holding period | long-term = held **more than 1 year**; the holding period **begins the day AFTER the buy trade date and ends ON the sale trade date** → earliest long-term sale = buy date + 1 year + 1 day | IRC §1222, IRS Pub 550 | barrier you must be past |
| Wash sale | **61-day window: 30 days before through 30 days after** the loss sale; replacement shares inherit the old holding period | IRC §1091, §1223(3) | window you must be inside/outside |
| Qualified dividend | hold **>= 61 days during the 121-day period beginning 60 days before the ex-date** | IRC §1(h)(11), §246(c) | window you must be inside |
| Ex-dividend | under T+1 the ex-date equals the record date for distributions <25% of value; buy **before** the ex-date to receive | FINRA Rule 11140 (amended eff. 2024-05-28) | countdown to a barrier |
| Margin call consequence | deficiency <= $1,000 → no action required; otherwise the firm must liquidate; **no advance notice required** | 12 CFR 220.4(d) | forced action |
| Intraday / day-trading margin | The **former "pattern day trader" regime was replaced in its entirety**: the four-day-trades-in-five-business-days count and the **$25,000 minimum equity** `[VERIFIED]` were superseded effective **2026-06-04** by **FINRA Regulatory Notice 26-10** (SEC-approved 2026-04-14/15, phased in to 2027-10-20), which sets intraday margin directly under **FINRA Rule 4210(d)(2)**. **Verify with your broker: this changed in 2026** — many broker pages still publish the superseded rule. | FINRA Regulatory Notice 26-10; FINRA Rule 4210(d)(2) | barrier + rolling look-back |
| Index calendar | S&P share/IWF changes effective after the close of the **third Friday of March/June/September/December** | S&P U.S. Indices Methodology | fixed calendar date |
| Russell | annual in June (effective after the close of the last Friday in June) — **moving to a SEMI-ANNUAL schedule (June and December) from 2026** | FTSE Russell reconstitution documentation | fixed calendar date |
| Short-swing (insiders only) | profit from a purchase-and-sale **within less than six months** is recoverable by the issuer | 15 U.S.C. §78p(b) | the insider's true DTE |

**Historical note on the day-trading clock.** A reader who finds an older broker page will see a different rule. Until 2026-06-04 the day-trading margin regime sat in what was then **FINRA Rule 4210(f)(8)**: four or more day trades in five business days designated a "pattern day trader" and required **$25,000** `[VERIFIED]` of minimum equity, and a missed call restricted the account to cash-available basis for 90 days. That framework was **superseded** by Regulatory Notice 26-10 — current Rule 4210(f)(8) is "Special Initial and Maintenance Margin Requirements" and the rule text carries no "pattern day" definition, with intraday margin now under (d)(2). A page still quoting the four-in-five / **$25,000** `[VERIFIED]` test is quoting a replaced requirement, so **verify with your broker before relying on either the old or the new figure**.

The compliance deadlines that accompany the insider row, for the reader who *is* the insider: Form 4 within 2 business days; Schedule 13D within 5 business days with amendments within 2 business days (eff. 2024-02-05); Form 13F within 45 days after quarter-end; Rule 10b5-1 cooling-off = the later of 90 days or 2 business days after the covering 10-Q/10-K, capped at 120 days for directors and officers and 30 days for everyone else (eff. 2023-02-27). Each is [VERIFIED] against the statute or release named in the source column above.

### What Equity Position Managers Know That Others Don't

- **The level, not the P&L, is the trigger.** A position can be down 30% with an intact thesis and up 40% with a broken one. Rank by thesis state first, then by money.
- **Average down usually cannot be sized.** The honest form requires the position to have been *undersized* to begin with. On a position already at or near its per-idea band, the arithmetic forbids it and no amount of conviction changes the arithmetic.
- **Rotation is a real action, not a cop-out.** Opportunity cost is the largest silent cost in a buy-and-hold book, and unlike a loss it never appears on a statement.
- **The tax tail is small; the position is large.** Waiting 20 sessions to reach the long-term rate risks roughly $2,789 of one-sigma price move to save about $510 in tax on a typical $33,000 position [COMPUTED]. That is a bet on the market dressed as a bet on the tax code.

### When to Break Your Own Rules

<!-- DEEP: 10+min -->
Breaking a rule is allowed only with all three of: a written reason, a bounded worst case, and a date by which the exception is graded. Without all three it is not an exception, it is drift.

- **Forced corporate action.** A merger, cash-and-stock election or spin-off delivers shares or cash you did not choose. That is a new position: new contract, router runs again.
- **Event-driven holds.** A pre-earnings hold is a bet on the event. It must be sized as one and must state the post-event action for both outcomes before the print.
- **Circuit-breaker days.** When the desk breaker is on, "I said I would hold" is not a defence. The breaker exists precisely to override locally reasonable holds during a correlated unwind.

---

## Deliberate Practice

<!-- STANDARD: 3min -->
The loop is only as good as the grading step. Practise the review *and* the grade on a closed position before doing it live.

| Level | Routine | Time | Success Metric |
|-------|---------|------|----------------|
| Novice | 8 steps in order on one position; never look at P&L first | per position, 2 min | zero reviews that start at P&L |
| Intermediate | Apply the router priority; write the contract (level, target, date, events) | per review, 5 min | 100% of open positions carry a dated contract |
| Advanced | Run the book on the time-axis cadence; arbitrate clock conflicts explicitly | daily/weekly, 20 min | zero unresolved clock conflicts; zero overdue reviews |
| Expert | Tune cadence by regime; audit which clock won each conflict and whether it was right | weekly + monthly, 60 min | precedence table refined from graded outcomes, not opinion |

---

## Operating at Different Levels

### L1: Apprentice
- **Scope:** One position, one decision, one action from the router.
- **Craft:** Applies the eight steps and the priority order mechanically; can state the invalidation level, the days to the anniversary and the next review date in one sentence.

### L2: Practitioner
- **Scope:** A handful of positions across sectors and holding periods.
- **Craft:** Runs the router unaided, writes exit contracts, escalates correctly under a breach, and knows which lot a trim is about to touch.

### L3: Senior
- **Scope:** The whole book's review schedule; conflict arbitration across clocks.
- **Craft:** Sets the cadence, owns the precedence resolution, and reads liquidity, the event calendar and the tax calendar as inputs rather than footnotes.

### L4: Staff / Principal
- **Scope:** Design of the review system — cadence, records, grading, band definitions, breaker conditions.
- **Craft:** Defines what "in plan" means per holding period, owns when a position is frozen, and can show which clock won each historical conflict.

### L5: Transformative
- **Scope:** The culture and tooling that make the loop survive a bad week.
- **Craft:** Codifies the cadence and the gates so the operator's worst day cannot skip them, and prunes rules that do not earn their keep.

---

## When to Use

**Use this skill when:**

1. **You already own the shares and the next move is undecided** — you need one action, chosen in a fixed order, not a menu of market opinions.
2. **The position is underwater** — you need the average-down gate, the cut rule, or a dated hold, and you need to know which one applies.
3. **An event is coming** — earnings, an ex-dividend date, an index reconstitution, an FOMC meeting — and the pre-event decision must be written before the event.
4. **A tax date is in reach** — the one-year anniversary, a wash-sale window, a qualified-dividend window — and you need to know whether it changes the action or only its timing.
5. **A winner has run past its plan** — you need the trim ladder and a rule for the remainder.
6. **The review schedule itself is the problem** — positions drift between annual glances and daily obsession.

---

## When NOT to Use

**Do NOT use this skill when:**

1. **You need to choose the stock.** Which name, at what valuation, on what technical structure, in what macro regime belongs to `fundamental-analyst`, `technical-signals-engineer` and `macro-strategist`. This skill starts when the shares are already in the account.
2. **You need a number, not a decision.** Which lots to sell, how much loss to harvest, when a holding period starts, how a wash sale is measured, what a corporate action does to basis — all `equity-tax-lot-and-exit-management`.
3. **The problem is the account, not the position.** Margin, borrow and recall, concentration, capital floors and the event calendar belong to `equity-risk-and-capital-engineer`, and so does the liquidity *assessment* — this skill only screens whether an intended exit can fill at size and whether the name belongs in the write-off set. It does not price depth, spread or borrow: that is step 7 of Phase 1 and CR8, a routing check, not an assessment.
4. **You need a size.** How many shares, what fraction of the book, which band — `portfolio-signal-manager` and `algorithmic-trader`.
5. **You want a hedge structure.** Which option, strike or expiry is `options-strategist`; non-standard structures are `advanced-options-structures`. This skill decides *whether* to hedge, not *with what*.
6. **The position does not exist yet.** Entry decisions are not lifecycle decisions. Running this skill on a hypothetical holding produces confidently-worded nonsense.

---

## Decision Trees

<!-- QUICK: 30s — DT2 is the router. When two actions qualify, the higher rung wins; DT3 is the precedence order that settles it when the clocks disagree. -->

### DT1: Is this still the position I bought? (the eight-step gate)

```text
Review due, or a level breached
├─ 1. Forced action live? (margin call, borrow recall, intraday-margin restriction, halt/delisting)
│      YES → ACT NOW, precedence rung 1: CLOSE or reduce only  ·  NO → step 2
├─ 2. Is the written invalidation level intact on the close?
│      NO → ACT: CUT, or CLOSE if the reason to own the name is gone  ·  YES → step 3
├─ 3. Is it still the position the contract describes?
│      NO (share count, unknown lots, unplanned corporate action, forgotten overlay)
│         → ACT: freeze the name and rebuild the contract before anything else
│      YES → step 4
├─ 4. Event clock: anything inside the next 10 business days?
│      earnings | ex-dividend | reconstitution | FOMC → PREPARE the pre-event decision
│      nothing → step 5
├─ 5. Tax clock: anniversary in reach, or a window open?
│      YES → FLAG it, carry it to rung 4 of the precedence table  ·  NO → step 6
├─ 6. Plan rung: at a trim rung, or through the written level?
│      rung hit → TRIM whole shares on the ladder
│      level broken → back to step 2; the level triggers, not the percentage
│      inside the band → step 7
├─ 7. Exit liquid at size, and position inside its per-idea band?
│      thin → WRITE-OFF candidate: stop paying attention, not money
│      over band → any ADD or AVERAGE DOWN is arithmetically barred
│      else → step 8
└─ 8. Are the level, the target and the review date all written?
       NO → write them now; an undocumented HOLD is not a decision
       YES → HOLD with a revisit date and the level that re-arms it early
```

### DT2: Which action wins when several qualify?

```text
Two or more actions qualify — which one? (stop at the first YES)
▼
1. FORCED ACTION, or a DESK CIRCUIT BREAKER active?
   YES → CLOSE or reduce only; everything below is deferred  ·  NO ↓
2. LEVEL BREACHED, or THESIS BROKEN?
   YES → CUT; CLOSE if there is no reason to own the name; tax is not an argument  ·  NO ↓
3. CAPITAL NEEDED ELSEWHERE, or a computed better idea? YES → ROTATE: exit here first, then
   size the new idea through portfolio-signal-manager — a CUT plus a sized ADD, never two
   positions held "temporarily"  ·  NO ↓
4. THESIS INTACT, TAX CLOCK ARGUES AGAINST REALIZING, a defined structure exists?
   YES → HEDGE — whether, not what; the structure belongs to options-strategist  ·  NO ↓
5. TRIM RUNG HIT, level intact? YES → TRIM whole shares on the ladder; the lot choice is
   equity-tax-lot-and-exit-management's call — name the interaction, do not pick the lot  ·  NO ↓
6. WINNER ABOVE RUNG 1, fresh level test, thesis re-underwritten in writing?
   YES → ADD / PYRAMID, if the enlarged position stays inside the per-idea band  ·  NO ↓
7. LOSER BELOW ENTRY, level intact, five-clause average-down gate passes?
   YES → AVERAGE DOWN in the honest form: references/average-down-honest-form.md
   NO  → CUT. A failed gate is an answer, not a delay
8. NOTHING TRIGGERED → HOLD with a date, a target and a level; tighten the invalidation
```

### DT3: Which clock binds — the tax clock, the event clock, the risk clock, or the level?

```text
Two clocks disagree. Which binds? (resolve top-down, stop at the first YES)
├─ Forced action live? (margin call, borrow recall, intraday-margin restriction, halt/delisting)
│      YES → the RISK CLOCK wins, and the firm need give no advance notice
│            [VERIFIED] — 12 CFR 220.4(d). Stop.
├─ Written invalidation level breached on the close?
│      YES → the LEVEL wins. The level is the position; tax changes nothing here. Stop.
├─ Event inside 5 business days? (earnings, ex-dividend, reconstitution)
│      YES → the EVENT CLOCK wins the decision date: decide before the boundary,
│            execute at or before it, never after on a story. Stop.
├─ Tax date in reach? (anniversary inside 5 sessions, wash-sale window open,
│   qualified-dividend window unmet)
│      YES → the TAX CLOCK wins only over a DISCRETIONARY plan action, and only by
│            changing WHEN a sale you were already making happens. It never turns a
│            sale into a hold. Stop.
└─ Then the PLAN RUNG decides: at rung → TRIM; below rung → HOLD to the written date,
   at the written level. Nothing else is a reason to act.
```

### DT4: HOLD, HOLD-WITH-DEADLINE, or CUT?

```text
Position is a loser. Hold it on a plan, or cut it?
├─ Is the thesis still true at the level?
│      NO → CUT. There is no hold on a broken thesis.
├─ Can you name the target price, the level that must hold, and the improve-by date?
│      NO → that is hope, not a plan → CUT
├─ Does the five-clause average-down gate pass? (thesis re-underwritten to the LOWER price;
│   blended basis computed; position still inside the band; written invalidation for the
│   enlarged position; add count under the maximum)
│      YES → AVERAGE DOWN, in the honest form, once
├─ Is the capital needed elsewhere, or is there a computed better idea net of tax and costs?
│      YES → ROTATE
└─ HOLD-WITH-DEADLINE granted:
       write all four fields: invalidation level, target, improve-by date, event calendar
       re-arm the clock at the level, not only at the date
       at the improve-by date: at plan, or cut. No renegotiation.
```

---

## Core Workflow

<!-- QUICK: 30s — Phase 1 gates on steps 1–3. A FAIL there escalates the position *before* the P&L is read; that ordering is the whole protocol. -->

### Phase 1: The ordered health check (~3 min per position)

Work the eight steps **in order**; do not skip ahead to step 6 because step 6 is the interesting one. Steps 1–3 are gates — a FAIL ends the check and escalates the position to ACT. Full criteria and a worked transcript: `(references/position-health-check-protocol.md)`.

1. **Forced action.** Is a margin call, borrow recall, intraday-margin restriction, halt or delisting live? This rung outranks opinion and is not negotiable.
2. **Thesis.** Is the invalidation level intact on the close? Name the level and mark pass/fail against it — not against the entry price.
3. **Position identity.** Share count, lot set, basis, any option overlay, any pending corporate action (split, merger, spin-off, special distribution). An equity position mutates silently; this is where mutation is caught.
4. **Event clock.** Earnings, ex-dividend, index reconstitution, FOMC, scheduled data — to a date, not "soon".
5. **Tax clock.** Days to the long-term anniversary; is a wash-sale window open; is a qualified-dividend holding window unmet.
6. **Plan rung.** Position against its band — rung hit, inside band, or band breach.
7. **Liquidity and concentration (screening only).** Can the intended exit fill at size, and is the position inside its per-idea band after the change you are contemplating? This is a screen, not an assessment: where the answer turns on depth, spread or borrow, that analysis belongs to `equity-risk-and-capital-engineer` — record the screen result and route it there.
8. **Instruments and records.** Level, target, date and event list all written; any resting orders match the position you now hold.

### Phase 2: Route to exactly one action (~1 min)

Apply DT2's priority order, then check it against DT3's precedence. Record the winner and the queue of losers. If the winner changes the basis or the band state, compute that now — an uncomputed action is not yet a decision. The numbers come from the owners named in `(references/action-router-decision-matrix.md)`; this skill never supplies them.

### Phase 3: Execute and instrument (~5 min)

Do the action, then do the boring part: recompute the blended basis and the band state, rewrite the exit contract, and note what the position now is. Every action above HOLD writes its expected outcome in one sentence and the date it will be graded. That is what makes the next review a judgement rather than a feeling.

### Phase 4: Schedule the next look (~2 min)

Set the next review from the cadence table below — and re-arm it at the level. The date is the floor; the level is the trigger. Any level breach pulls the review forward to now, on any cadence state.

### Review Cadence by Time-Axis State

| Time-axis state | Cadence | What each review must produce |
|---|---|---|
| No hot clock (the ordinary state) | **Weekly**, on a fixed day | Steps 1–8; a HOLD with a level and a date |
| Earnings inside **10 business days** | **Daily** + a written pre-earnings decision | The pre-earnings action for both outcomes, written before the print |
| Ex-dividend inside **5 sessions** | **Daily** | Whether you are buying, holding or avoiding the ex-date, and the qualified-dividend window that follows it |
| Index reconstitution inside **5 sessions** (S&P third Friday of Mar/Jun/Sep/Dec; Russell June, plus December from 2026) | **Daily** | Whether membership change affects size or liquidity |
| Within **5 sessions of the long-term anniversary** | **Daily** | The decision taken *before* the anniversary, not the day after |
| Inside a **wash-sale window** (30 days before through 30 days after a loss sale) | **Flag the name at every review** | No purchase in the name, in any account, until the window closes |
| A **qualified-dividend window** open and unmet | **Flag at every review** | The 61-day count and whether the action would break the holding period |
| **Margin, borrow or intraday-margin stress** live | **Intraday** | The forced action, executed inside the window the firm gave you |
| Winner above **trim rung 1** with no trim executed | Review before any new entry is discussed | The trim, or a written reason it is refused |

Full cadence rules and the re-arm conditions: `(references/equity-time-axes-cadence.md)`.

### Phase 5: Revisit and grade (~10 min, at the revisit date)

If the position was granted HOLD-WITH-DEADLINE, the improve-by date is a decision date, not a discussion: at plan, or cut. Grade the action against what was expected, write the one-line lesson, and update the precedence table if a clock lost. Then, and only then, consider re-entry — through the re-entry gate, never through nostalgia.

---

## Best Practices

1. **Check the level before the P&L.** The first three steps are structural. A review that opens with "we're down 18%" has already lost the plot.
2. **Treat steps 1–3 as gates, not as scores.** One FAIL ends the review and produces a disposition. Partial compliance with an invalidation is not a thing.
3. **Write the invalidation level at entry, as a price.** A stock has no expiry to stop you out, so the level is the only stop the position will ever have — and it must exist before the position does. A price level is a desk convention [COMMON-PRACTICE], not a published rule — but it is the convention that makes every other clause here enforceable.
4. **One action per review.** Two actions qualify → the router's priority wins, the other becomes queued. Doing both is how a trim becomes a new position.
5. **Decide before the event, not after.** The earnings, ex-date and reconstitution decisions are all cheaper written before the print than rationalised after it.
6. **Never let the tax tail wag the position.** Compute the tax difference in dollars, compare it to one standard deviation of the position over the waiting period, and let the larger number win.
7. **Trim in whole shares, in thirds, on a ladder.** A fractional trim is a rounding decision pretending to be a strategy.
8. **Name the lot interaction before you trim.** Whole shares and a ladder are one thing; *which* lot they come from changes the tax and the wash-sale outcome, and that call belongs to `equity-tax-lot-and-exit-management`.
9. **Refuse the average-down default.** The gate is five clauses, not five feelings. A failed gate is an answer: CUT, not a delay.
10. **Make rotation first-class.** Every held position competes against the best idea you could buy with the same money today. If the answer is "nothing", that is fine — but the question is asked on the cadence, not once at purchase.
11. **Manufacture the deadline.** No clock will ever end an equity position. Write the improve-by date, the level and the target, and treat the date as binding.
12. **Grade every action, including the winners.** An ungraded action teaches nothing, and the precedence table can only be tuned from graded outcomes.

---

## Error Decoder

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| A position "suddenly" collapses from −15% to −45% | Reviews only happened when the position made the news; the level broke quietly in between | Move the trigger to the level; the cadence is the floor, not the trigger | A stock has no alarm clock. Someone has to set one |
| The loser is the largest position in the book and the winners were sold | Dispositions were chosen by the sign of the P&L instead of by the level | Re-run DT2 on the loss side; HOLD requires a level that holds and a date | Selling winners to keep losers concentrates the book in its weakest ideas |
| A "cheap" add triples the loss | The add reacted to the price instead of re-underwriting the thesis at the lower price | Apply all five clauses; if any fails, CUT | Averaging down converts a small loss into a large one in exactly the cases where the thesis broke |
| A repurchase inside 30 days voids a harvested loss | The wash-sale window was not flagged on the name, or the repurchase happened in another account | Flag the name for 61 days at every review; no purchases in the name, anywhere | The window is a property of the security, not of the account |
| A dividend is taxed at the full ordinary rate | The position was bought for the dividend without the 61-day holding inside the 121-day window | Size the ex-date as a two-month commitment, not a payday | The ex-date is a price event and a holding-period commitment at once |
| Every position is a HOLD and nothing has been sold in a year | The router was applied to conviction instead of to the level and the date | Force one full pass of DT2 across the book; count the positions with no date | A book with no exits is not patient, it is unmanaged |

---

## Error Recovery

| Symptom | First Action | If That Fails | Last Resort |
|---------|--------------|---------------|------------|
| The stock gapped through the invalidation level overnight | Do not chase the opening print; queue the exit for the first 30 minutes of regular hours | Use a limit at a level you can defend, and accept a partial fill | Accept the fill and re-underwrite what remains; never average down a gapped loss |
| A margin call arrived with no notice | Fund it, or reduce, inside the window the firm gave you — the firm need give no advance notice and may liquidate without one | Reduce the position yourself at a level you choose rather than at the firm's | Accept the firm's liquidation; then rebuild the account's floors before trading again |
| No executable exit (thin name, wide spread, no depth) | Reclassify as a WRITE-OFF candidate; stop monitoring it weekly | Leave a resting order at a level you would genuinely accept | Hold it out of the attention set; the attention you saved is the recovery |
| The improve-by date arrived and the position is not at plan | Cut, per the contract. Do not renegotiate the date | If liquidity blocks the cut, write off and remove it from the attention set | Cooldown the name; re-entry requires a new thesis through the re-entry gate |
| Two clocks disagree and both are "house rules" | Apply the precedence order: forced action → level → event → tax → plan rung | Ask which owner supplies the number (tax vs sizing vs calendar) and follow that owner | Apply the more conservative action and record the conflict for the review |

**Hard failure boundary:** after three failed attempts to resolve the same conflict on the same position, escalate to the human owner of the book. Do not loop, and do not reframe the problem to avoid the escalation.

---

## Cross-Skill Coordination

### Upstream (what this skill needs)

| Upstream Skill | Artifact Needed | What You'll Use It For |
|----------------|-----------------|------------------------|
| `equity-tax-lot-and-exit-management` | Lot selection, cost basis, harvest candidates, wash-sale windows, holding-period arithmetic | Every tax clause of the router — never invented here |
| `equity-risk-and-capital-engineer` | Margin and borrow state, concentration, liquidity, the event calendar | The forced-action gate in step 1 and the precedence table's rung 1 |
| `portfolio-signal-manager` | Per-idea bands, sector caps, capital available, correlation | Whether an ADD or AVERAGE DOWN is arithmetically possible at all |
| `algorithmic-trader` | The pyramid gate for adding to confirmed winners | The ADD preconditions, so the add is not a hunch |
| `technical-signals-engineer` | The level, the trend state, the behaviour at the level | The invalidation level, and the fresh level test an ADD requires |

### Downstream (what this skill produces)

| Downstream Skill | Deliverable | What They'll Do With It |
|------------------|-------------|-------------------------|
| `equity-risk-and-capital-engineer` | Position dispositions, planned exits, band states, freezes | Recompute concentration, margin and liquidity against the planned book |
| `trade-performance-analyst` | Graded action records: action, expectation, outcome, lesson | Attribute expectancy by action type and by which clock won |
| `portfolio-signal-manager` | Standing queued actions, frozen names, capital released by rotations | Re-weight the book and respect freezes and cooldowns |
| `equity-tax-lot-and-exit-management` | Lot intentions, realized-loss events, approaching anniversary dates | Plan which lots a pending trim will actually touch |

---

## Proactive Triggers

- **The close is beyond a written invalidation level** → escalate one rung immediately and re-run Phase 1 from step 1. 🔴
- **A margin call, borrow recall or intraday-margin restriction is live** → announce the forced window before discussing anything else. 🔴
- **Earnings is inside 10 business days** → demand the written pre-earnings decision now. 🟡
- **An ex-dividend date is inside 5 sessions** → surface the two-month qualified-dividend commitment. 🟠
- **The long-term anniversary is inside 5 sessions** → force the decision before the date, not after. 🟠
- **A loss was realized in this name inside 30 days** → flag the wash-sale window and freeze the name. 🔴
- **A position has no written exit contract** → freeze the name and write the contract. 🔴
- **An ADD or AVERAGE DOWN would push the position past its per-idea band** → block it and record the refusal. 🔴
- **An improve-by date is within two sessions** → surface the pending decision before it becomes a post-hoc rationalisation. 🟠
- **A name is proposed for re-entry inside its cooldown** → name the cooldown and block it. 🟠

---

## Anti-Patterns

| ❌ Anti-Pattern | ✅ Do This Instead |
|----------------|-------------------|
| ❌ Checking the P&L before the level | ✅ Steps 1–3 first: forced action, level, position identity. Money is step 6 |
| ❌ "It's only down on paper, it'll come back" | ✅ The mark is the price you can transact at today; treat it as real and apply the router |
| ❌ Averaging down a broken thesis because "it's cheaper" | ✅ Five-clause gate or CUT. A failed clause is an answer, not a delay |
| ❌ Holding a loser purely to reach the long-term rate | ✅ Decide the economics first; tax changes *when* you sell, never *whether* |
| ❌ Treating the ex-date as free money on a long or a short | ✅ Treat it as a two-month qualified-dividend commitment and a price event at once |
| ❌ Assuming a hedge leaves the tax clock untouched | ✅ Flag the interaction and route the rule to the tax skill before writing the hedge |
| ❌ Never rotating because "it might come back" | ✅ Ask the rotation question on the cadence, with the friction computed in dollars |
| ❌ Writing a stop as a percentage of entry | ✅ Write a price level, versioned; a percentage moves every time the basis moves |
| ❌ Treating the insider deadlines as part of a retail holder's risk list | ✅ State plainly that Form 4, 13D/13G, 13F, §16(b) and Rule 144 are not you |

---

## State Log

| Turn | Action | Decision | Risk Accepted | Mitigation |
|------|--------|----------|---------------|-----------|
| 1 | Ran Phase 1 on a 4-month-old position, down 15%, earnings in 6 sessions, invalidation level not on file | Step 2 FAIL (no level) → position is unmanaged; froze new risk and wrote the level | The position is unhedged while the contract is rebuilt | Level written and versioned before the earnings decision; no add permitted until it exists |
| 2 | Ran step 4: earnings inside 10 business days | PREPARE. Pre-earnings decision written for both outcomes, before the print | Gap risk through the event on both sides | Decision written on the date, executed at the event boundary |
| 3 | Ran the average-down gate on the same position | Gate FAILED clause 3: the position was already 16% of a $250,000 account against a 10% per-idea band [COMPUTED] | The position stays at full size into a decided event | Router fell through to HOLD-WITH-DEADLINE with an improve-by date and a level trigger |

**Anti-Drift Check.** Before each response on this position: (1) did the last action match the plan in the contract; (2) is the next review still the earliest of the date floor and the level trigger; (3) has anything arrived since — a new event, a corporate action, a margin change, a tax date — that invalidates the disposition?

---

## Production Checklist

- [ ] **CR1: The eight steps ran in order** — **Complete when** steps 1–8 are each marked pass/fail in the review record.
- [ ] **CR2: The invalidation level is a price** — **Complete when** the level is a price or a named condition, never an adjective or a percentage of entry.
- [ ] **CR3: The forced-action gate is checked** — **Complete when** margin, borrow, intraday-margin (day-trading) and halt state are each recorded as clear or live.
- [ ] **CR4: Position identity verified** — **Complete when** share count, lot set, basis and any corporate action are checked against what the contract describes.
- [ ] **CR5: The event clock is dated** — **Complete when** earnings, ex-dividend, reconstitution and macro events are each listed with a date or explicitly absent.
- [ ] **CR6: The tax clock is dated** — **Complete when** days to the anniversary, wash-sale window state and qualified-dividend window state are written down.
- [ ] **CR7: P&L mapped to a band** — **Complete when** the position is labelled rung hit / inside band / band breach.
- [ ] **CR8: Liquidity screened for the intended exit** — **Complete when** the exit is screened against the intended size and either the screen passes or the position is reclassified as a write-off candidate; any depth, spread or borrow analysis behind the screen is routed to `equity-risk-and-capital-engineer`.
- [ ] **CR9: Band state recomputed after the action** — **Complete when** any ADD, AVERAGE DOWN or TRIM shows the resulting per-idea percentage with its arithmetic.
- [ ] **CR10: Exactly one action chosen** — **Complete when** the winner is recorded and the losers are queued, not executed.
- [ ] **CR11: The precedence order was applied** — **Complete when** the winning clock is named and any lower clock that lost is recorded as a queue entry.
- [ ] **CR12: Numbers produced by their owners** — **Complete when** every number in the record cites `equity-tax-lot-and-exit-management`, `equity-risk-and-capital-engineer` or `portfolio-signal-manager`.
- [ ] **CR13: Next review dated, and the level trigger armed** — **Complete when** both the date (from the cadence table) and the level are written.
- [ ] **CR14: Expected outcome recorded and graded** — **Complete when** the action carries one sentence of expectation plus a grading date, and the grade is written at that date.

---

## What Good Looks Like

A well-run equity book sounds like a shift log, not a market commentary. Every held position has a contract: a level that must hold, a target, a date, an event list and a tax-calendar note. Reviews happen on a cadence that tightens automatically as clocks come into range, and a single close beyond a level pulls the review forward without anyone deciding to be disciplined. When clocks disagree the arbitration is written down and the winner named. Losses exit at the level they were planned for, winners are trimmed in whole shares at rungs, adds happen only above rung 1 with the thesis re-underwritten, and dead names are written off and forgotten. Nothing in the log reads as hope.

**Signs of Excellence:** every action traces to a router rung and a number somebody else owns; every held position has a date and a level, and every date is met; the rotation question is asked on the cadence with the friction in dollars, and "nothing better" is an accepted answer with a date; the precedence table has been amended from graded outcomes.

**Signs of Dysfunction:** the first number mentioned in a review is a P&L percentage; the invalidation level moves down every time the price does; the phrase "let's see how the quarter goes" appears in a decision record; adds cluster on the positions with the strongest narrative and the worst arithmetic.

---

## Verification Guardrails

### Pre-Generation

- [ ] The position and its contract are identified (never route an action against a guessed holding, lot set or share count).
- [ ] The mark, the share count and the cost basis have a stated timestamp and source.
- [ ] The owner of every number used is known: tax from `equity-tax-lot-and-exit-management`, account and events from `equity-risk-and-capital-engineer`, size from `portfolio-signal-manager`.

### Post-Generation

- [ ] Exactly one action was chosen, and its priority rung is stated.
- [ ] The winning clock is named whenever two clocks disagreed.
- [ ] The next review date and the level trigger are both written.

### Failure Modes

**Failure modes and known limitations — what goes wrong with equity position management, and the countermeasure for each:**

1. **Failure mode: the position is never forced, so it is never decided.** Nothing expires an equity position. Countermeasure: the improve-by date and the level, both written, both binding.
2. **Failure mode: the review degrades into a P&L glance.** Step 6 crowds out steps 1–3. Countermeasure: the gates are pass/fail and are written before step 6 is read.
3. **Failure mode: the level quietly moves.** A stop is restated lower each month until it is meaningless. Countermeasure: the level is versioned; a change needs a written reason and a new grading date.
4. **Failure mode: averaging down a broken thesis.** Worst case: the add converts a small loss into a large one in exactly the cases where the thesis broke. Countermeasure: the five-clause gate, a maximum add count, and CUT as the default on any failed clause.
5. **Failure mode: the tax tail wags the position.** A sale is delayed past the point where the thesis broke, for a rate difference worth a fraction of one standard deviation of the position. Countermeasure: compute both in dollars and compare before deciding.
6. **Failure mode: the wash sale is violated by accident.** A repurchase in another account, or an automatic reinvestment, voids a harvested loss. Countermeasure: flag the name for the full 61-day window and freeze purchases in it everywhere.
7. **Failure mode: the dividend is bought without the commitment.** The 61-day holding inside the 121-day window is missed and the dividend is taxed as ordinary income. Countermeasure: size the ex-date as a two-month commitment before the buy.
8. **Failure mode: liquidity evaporates exactly when the exit is needed.** The intended exit cannot fill at the planned level and the position is carried into the event. Countermeasure: check exit depth every review; pre-classify thin names as write-off candidates rather than pretending they are tradeable.
9. **Failure mode: the forced action arrives unannounced.** A margin call or borrow recall is satisfied by the firm's liquidation at a price nobody chose. Countermeasure: check the account's floors every review and treat the firm's right to act without notice as a fact.
10. **Failure mode: the event decision is made after the event.** The earnings or ex-date action is rationalised in hindsight on the gap. Countermeasure: the event decision has a written date that precedes the event.
11. **Failure mode: rotation is never considered.** The book drifts into "what I own" rather than "what I would buy". Countermeasure: ask the rotation question on the cadence with the friction computed.
12. **Failure mode: grading is skipped.** Without graded outcomes the precedence table drifts back to folklore and the same conflict is arbitrated differently next quarter. Countermeasure: an ungraded action keeps the position flagged unmanaged.

**Exit conditions / stop-loss rules:**

- Stop-loss: a **price level**, written at entry and versioned — never a percentage of entry, never widened without a written reason and a new grading date.
- Exit condition: the thesis is invalidated (level broken, or the reason for owning the name withdrawn).
- Exit condition: a forced action — margin call, borrow recall, intraday-margin restriction, halt or delisting.
- Exit condition: the improve-by date arrives and the position is not at plan.
- Exit plan: scale out in whole shares on a ladder; never add to a losing position outside the written average-down gate.

### Regime Table

| Regime | What it looks like | What changes here |
|--------|--------------------|-------------------|
| **Bull market / uptrend** | Broad advance, shallow dips, vol drifting lower, breadth healthy | Winners reach rungs quickly: trim on schedule and resist selling a compounding name for the tax rate. Adds are most defensible and rotation is easiest because cash is not scarce. The failure mode is greed, not damage |
| **Correction / pullback** | A decline of roughly 5–10% inside an uptrend; vol ticks up | Most "level breaches" here are noise — require a close, not a wick. Shorten the cadence by one step, stop adding to losers, and refuse average-down proposals unless the gate passes on arithmetic, which it usually will not |
| **Bear market / drawdown / recession** | A sustained decline of roughly 20% or more, rallies sold, rising realised vol | Concentration becomes acute, margin requirements bite and correlations rise. Cut thresholds tighten, adds are barred, and defensiveness is expected rather than clever. Every position is re-underwritten and the tax clock loses to the level every time |
| **Crash / tail event / March 2020-style dislocation** | Correlation goes to one, liquidity evaporates, gaps replace prices, the market collapse is a session not a year | Circuit-breaker territory. Positions are closed or reduced, never averaged into. The only reliable defence is size already taken at entry and a level already written. A black-swan day is not the day to discover that a name has no contract |

A regime change is a **state to re-check**, not a background constant: the same position correctly held in an uptrend can be a mistake in a drawdown with no change to the position at all.

### Data Sources and Provenance

The **structure of the decision** — fixed order, gates, priority order, precedence — is durable engineering. The **numbers** are not: marks, spreads, borrow rates, margin schedules, dividend dates and index membership decay within a session. So the operating bands here are **derived from data** — published statutes and regulations, exchange rules, observed liquidity and graded outcomes from the review record — not asserted from opinion.

- `source:` IRC §1222 — the definition of long-term and short-term capital gain and loss; the origin of the one-year-plus-one-day anniversary rule. [VERIFIED] — IRC §1222, with IRS Publication 550 for the trade-date convention.
- `source:` IRC §1091 and §1223(3) — the wash-sale rule: the 61-day window and the inheritance of holding period by replacement shares. [VERIFIED] — IRC §1091, §1223(3).
- `source:` 12 CFR 220.2 and 220.4 — the Reg T payment window of settlement plus two business days, the $1,000 deficiency threshold, and the firm's authority to liquidate without advance notice. [VERIFIED] — 12 CFR 220.4(c)(3)(i), 220.4(d).
- `source:` FINRA Regulatory Notice 26-10 and FINRA Rule 4210(d)(2) — the intraday (day-trading) margin framework that **replaced the former "pattern day trader" regime in its entirety** effective 2026-06-04 (SEC approval 2026-04-14/15; phase-in to 2027-10-20), retiring the four-day-trades-in-five-business-days count and the $25,000 minimum equity. [VERIFIED] — FINRA Regulatory Notice 26-10; FINRA Rule 4210(d)(2); verify the current requirement with the firm.
- `source:` FINRA Rule 11140 (amended effective 2024-05-28) — the ex-dividend date convention that makes the ex-date equal the record date for distributions under 25% of value. [VERIFIED] — FINRA Rule 11140.
- `source:` SEC Release 34-96930 — the shortening of the standard settlement cycle to T+1, effective 2024-05-28. [VERIFIED] — SEC Release 34-96930.
- `source:` S&P U.S. Indices Methodology — share and IWF changes effective after the close of the third Friday of March, June, September and December. [VERIFIED] — S&P U.S. Indices Methodology.
- `source:` FTSE Russell reconstitution documentation — the annual June reconstitution effective after the close of the last Friday in June, moving to June and December semi-annually from 2026. [VERIFIED] — FTSE Russell reconstitution documentation.
- `data from:` broker margin schedules — read your own firm's house maintenance requirements and tag the result `[BROKER-VERIFIED]`, because house percentages, borrow recall notice and liquidation timing differ by firm. [BROKER-VERIFIED] — read the schedule your firm actually applies.
- `verified against:` exchange rules for trading calendars, half-sessions and corporate-action processing whenever a date or a share count is ambiguous. [VERIFIED] — exchange rules.
- `published by:` your own review record — the only source that can say which clock won a past conflict and whether it was right [COMPUTED] from graded actions, not recollection.
- Cross-reference, in this library, the **Pattern Recognition Engine** meta-layer at `skills/14-finance/options-strategist/references/pattern-recognition-engine.md`. It names the pattern being held; if an action changes the pattern, re-name it before the next review. (Repo-relative path; nothing here depends on it being installed in your project.)
- [ESTIMATED] Cadence boundaries (weekly, 10 business days, 5 sessions) and the friction band used in the rotation arithmetic are pragmatic operating bands, derived from when event and tax dates materially change a decision. Past performance is not a guarantee; thresholds here are approximate and must be re-checked against the position in front of you.

### Dollar-Quantified Worked Figures (format demonstration)

**Format demonstrations on stated inputs, not observations.** Every figure is reproducible by hand from the inputs in its own line.

- **The tax tail, in dollars.** A $3,000 gain [COMPUTED]: 500 sh × ($66.00 − $60.00) = 500 × $6.00 = 3,000. The rate pair is an **assumption the reader substitutes, not a measurement**: 40.8% short-term and 23.8% long-term [ESTIMATED], being the 37% and 20% statutory rates plus the 3.8% net investment income tax. Short-term: **$1,224** [COMPUTED]: 3,000 × 0.408. Long-term: **$714** [COMPUTED]: 3,000 × 0.238. The rate difference is **$510** [COMPUTED]: 3,000 × (0.408 − 0.238) = 510. The statutory rates are [VERIFIED] — IRC §1(h) and §1411 — but the 40.8% / 23.8% pair is an assumption; substitute your own bracket and the arithmetic still holds.
- **What waiting 20 sessions for the anniversary risks.** A $33,000 position [COMPUTED]: 500 sh × $66.00 = 33,000. At 30% annualized volatility a one-sigma daily move is **$624** [COMPUTED]: 33,000 × 0.30 ÷ √252 = 623.7. Over 20 sessions one sigma is **$2,789** [COMPUTED]: 623.7 × √20 = 2,789. The $510 tax saving is **18%** of one standard deviation of the wait [COMPUTED]: 510 ÷ 2,789 = 18.3%. That is the whole argument for "tax never justifies a worse economic position", in two numbers.
- **The margin line is a number, not a feeling.** A $60,000 position with a $32,000 debit carries $28,000 of equity; at a 30% house maintenance requirement the requirement is **$18,000** [COMPUTED]: 60,000 × 0.30 = 18,000 [BROKER-VERIFIED] — read your own firm's house percentage, which is not a regulatory constant. A deficiency of **$940** requires no action; a deficiency of **$1,060** does [VERIFIED] — 12 CFR 220.4(d).
- **Rotation friction, in dollars.** A $39,900 position [COMPUTED]: 700 sh × $57.00 = 39,900. Rotating means realizing a $4,000 gain at 23.8% = **$952** [COMPUTED]: 4,000 × 0.238, plus round-trip commission and spread of roughly 0.3% of the position = **$120** [ESTIMATED]: 39,900 × 0.003, an operating band for a liquid large-cap name, not a measured cost. Total friction **$1,072** [COMPUTED]: 952 + 120 = 1,072, which is **2.7%** of the position [COMPUTED]: 1,072 ÷ 39,900 = 2.69%. The new idea must beat the old one by that much in year one before the rotation is level.
- **What an average-down actually buys.** Original 500 sh at $80.00 = $40,000 [COMPUTED]: 500 × 80 = 40,000. Add 250 sh at $64.00 = $16,000 [COMPUTED]: 250 × 64 = 16,000. Blended basis **$74.67** [COMPUTED]: (40,000 + 16,000) ÷ 750 = 74.67. Recovery needed falls from **25.0%** to **16.7%** [COMPUTED]: (80.00 ÷ 64.00) − 1 = 25.0%; (74.67 ÷ 64.00) − 1 = 16.7%. The cost is **50% more shares** and **40% more capital committed** [COMPUTED]: 250 ÷ 500 = 50%; 16,000 ÷ 40,000 = 40%. Eight points of recovery, bought with four-tenths more money, on a thesis not yet re-underwritten.
- **The band usually forbids it anyway.** A $40,000 position on a $250,000 account is **16%** of the book [COMPUTED]: 40,000 ÷ 250,000 = 16.0%, against a per-idea band of 10% = $25,000 [VERIFIED] — the 10%-per-position cap published in this library's `portfolio-signal-manager`. The position is already **$15,000 over** the band [COMPUTED]: 40,000 − 25,000 = 15,000, so clause 3 of the average-down gate fails before the size is even discussed.
- **The cost of an undisciplined hold.** A 15% decline on a $30,000 position is a **$4,500 loss** [COMPUTED]: 30,000 × 0.15 = 4,500. If the thesis is broken and the position runs to −40%, that is **$12,000** [COMPUTED]: 30,000 × 0.40 = 12,000 — an additional **$7,500** [COMPUTED]: 12,000 − 4,500 = 7,500, paid to the story told while the level was breaking.

---

## References

| Reference | Covers | Use When |
|-----------|--------|----------|
| [position-health-check-protocol.md](references/position-health-check-protocol.md) | The eight-step ordered check, pass/fail criteria, stop-early rule, worked transcript | Every review, before any action is considered |
| [equity-time-axes-cadence.md](references/equity-time-axes-cadence.md) | The four clocks in full, cadence by time-axis state, how clocks interact, re-arm rules | Setting the next review date, or deciding which clock is live |
| [action-router-decision-matrix.md](references/action-router-decision-matrix.md) | Trigger, precondition, forbidden variant and numbers-owner for all eight actions, plus the priority order | Choosing the action |
| [trigger-precedence.md](references/trigger-precedence.md) | The precedence order, worked conflicts, and why tax never beats a breached level | When two clocks disagree |
| [add-and-pyramid-gate.md](references/add-and-pyramid-gate.md) | The five ADD preconditions, blended basis arithmetic, band recheck, the add-count cap | Only on a winner already above rung 1 |
| [average-down-honest-form.md](references/average-down-honest-form.md) | The five-clause gate, worked arithmetic, rejection examples, audit trail | When someone proposes averaging down |
| [trim-and-scale-out-ladder.md](references/trim-and-scale-out-ladder.md) | Whole-share rule, thirds ladder, the lot interaction, the remainder's rule | Booking profit at a rung |
| [cut-and-rotation-decision.md](references/cut-and-rotation-decision.md) | Level-based cut, gap rules, write-off classification, rotation arithmetic net of tax and costs | Any level breach, and the rotation question |
| [hedging-an-equity-position.md](references/hedging-an-equity-position.md) | Decide *whether* to hedge, cost arithmetic, contract granularity, the tax interaction flag | Thesis intact, tax clock argues against realizing |
| [hold-and-revisit-protocol.md](references/hold-and-revisit-protocol.md) | The deadline contract, the improve-by date, no-renegotiation, cooldown and the re-entry gate | Keeping a loser alive on a plan |
| [close-versus-hold.md](references/close-versus-hold.md) | When CLOSE beats every other action, the capital-needed case, and the difference from CUT | The reason to own the name is gone |

Meta-layer: `skills/14-finance/options-strategist/references/pattern-recognition-engine.md` — the pattern taxonomy this skill assumes still describes the position after every action.

---

## Gotchas

- **A stock has no expiry, so the exit plan is the only clock.** Everything else in an equity position is a date somebody wrote down. If nobody wrote one, the position has no clock at all.
- **The tax rate is a percentage; the position is the whole number.** A $510 tax saving against $2,789 of one-sigma price risk over a 20-session wait is a bet on the market wearing a tax costume [COMPUTED]: 510 ÷ 2,789 = 18.3%.
- **The wash-sale window is a property of the security, not the account.** A repurchase in a different account, or an automatic reinvestment, still counts — which is why the flag sits on the *name* for 61 days.
- **$1,000 is the margin line that decides whether you get warned or liquidated.** A deficiency of $940 requires no action; $1,060 does, and the firm need give no advance notice [VERIFIED] — 12 CFR 220.4(d). Size the account so it never sits near the line.
- **A covered call is not a free hedge.** It caps the position, changes the tax picture and needs 100 shares per contract, so a 300-share position can only be one-third hedged. Flag the tax interaction before writing it.
- **Rotation friction is smaller than it feels and larger than it looks.** A 2.7% round-trip friction on a $39,900 position is $1,072 [COMPUTED]: 952 + 120. That is the bar a new idea must clear in year one — not a reason never to rotate.
- **The improve-by date is not negotiable.** If it moves once it will move every time, and the HOLD becomes a permanent, undated position with a story attached.
- **The one-year rule has a day in it, and the day is not the buy date.** The holding period begins the day *after* the buy trade date and ends *on* the sale trade date, so the earliest long-term sale is the buy date plus one year plus one day [VERIFIED] — IRC §1222, IRS Pub 550.
