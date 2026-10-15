---
name: options-leg-management
description: >
  Use when an ALREADY-OPEN multi-leg position — iron condor, butterfly, vertical, calendar or
  diagonal — needs leg-level surgery: closing, rolling or converting individual legs or partial
  structures. Triggers: "close one leg", "roll the short up", "how do I close just one side of
  my condor", "turn my fly into a spread", "my short is going ITM into expiry", "one leg is deep ITM
  and the structure is unbalanced". Handles whole-unit scale-outs, fly-to-vertical downgrades,
  house-money long-only conversions, spread-to-long-only closes, short-leg pin guard, one-leg condor
  and calendar defense, unbalanced-legacy repair, and the no-naked-risk legging rules. It repairs ONE
  leg; the weeklies/monthlies/LEAPS close order is not its remit. Do NOT use to build a new structure
  (options-strategist), for the review router or the hold/trim/roll decision
  (options-position-lifecycle), per-trade sizing (trade-sizing-recovery), portfolio risk
  (options-risk-engineer), or execution (options-automation-engineer).
license: MIT
author: "Sandeep Kumar Penchala"
type: finance
status: experimental
version: "1.0.0"
updated: 2026-10-14
tags:
  - options
  - leg-management
  - legging
  - one-leg-surgery
  - legging-rules
  - rolling
  - butterflies
  - condor-defense
  - spreads
  - pin-risk
  - assignment
  - risk-reduction
  - scale-out
token_budget: 4000
chain:
  examples:
  - skills/14-finance/options-leg-management/examples/backtest
  consumes_from: [trade-sizing-recovery]
  feeds_into: [options-position-lifecycle]
---

# Options Leg Management — position surgery for multi-leg trades

> **Portability target:** spec-level. Broker command syntax and order-type names below
> illustrate a capability (native multi-leg / package orders), not a required venue. Every
> rule here is executable anywhere that supports a same-structure complex order at one
> net price.

<!-- QUICK: 30s --> (1) NEVER leg into naked risk: write the resulting leg list and
balance-check it before every order. (2) Same-structure changes go as ONE package order;
shorts-first sequencing only if the package is rejected. (3) Fly conversions: wing+short
TOGETHER → vertical; shorts+wing TOGETHER → long-only house money. (4) Pin guard at ≤ 2 DTE,
act by 15:45 ET on expiry day. (5) Any roll or leg op is a TRADE — full pre-action protocol,
ledger row FIRST.

<!-- STANDARD: 3min --> the five hard rules, the safe-conversion catalog and the decision
matrix are the whole skill. Read those three blocks and you can run a leg operation without
opening a single reference file.

<!-- DEEP: 10+min --> the conversion arithmetic in
`(references/leg-arithmetic-worked-examples.md)`, the assignment mechanics in
`(references/pin-risk-and-assignment-guard.md)`, and the failure-mode catalogue before you
manage a real assignment or a legacy unbalanced book.

## Route the Request

<!-- QUICK: 30s --> if a position is already open and the question is about a LEG, you are in the right place.

### Auto-route — fires without asking

| Signal in the request | Operation | Gate that must pass first |
|---|---|---|
| "close just the short leg" / "close one leg" | R1 pre-flight, then package it | resulting leg list is still defined-risk |
| "roll the short up" / "roll the fly up" | Financed roll-up (RU) | net debit ≤ realized proceeds AND new body above spot with room |
| "turn my fly into a spread / vertical" | Fly→vertical downgrade (VD) | wing + short closed as ONE package |
| "take the winner off" / "make it risk-free" | Long-only conversion (HM) | realized proceeds ≥ original debit + conversion cost |
| "my short is near the strike into expiry" | Pin guard (PG) | action by 15:45 ET on expiry day |
| "defend the tested side" / "my condor is broken" | Condor defense (CD) | close ONE side's two legs as a package |
| "roll the calendar out" | Calendar roll (CR) | DTE ≤ 5 AND net cost ≤ ~50% of current mark |
| "I got assigned" / "I woke up long stock" | Post-assignment triage | stock position re-banded as a NEW position |
| "my position is lopsided" / "I think I have naked shorts" | Unbalanced-legacy repair (UD) | risk defined in the FIRST order |
| "should I trim" / "take profit" | Rung scale-out (SC) | whole structure-units only |
| "should I do anything?" with a healthy structure | No-op review | no matrix row fires → HOLD and record it |

### Intent route — ask, do not assume

1. **The live leg list** — strikes, right, quantity with sign, expiry, average price per leg,
   and the structure's current mark. Leg surgery is designed against the leg list, never
   against a summary.
2. **Open structure-units.** Unit count decides whether a scale-out is legal at all.
3. **Realized cash to date.** Required by the house-money test.
4. **Events inside the remaining life** — earnings, ex-dividend, macro. These decide whether a
   roll is a roll or a new event bet.
5. **Does the venue execute same-structure complex orders at a single net price?** If not, the
   sequencing rules in `(references/package-order-execution.md)` become mandatory.

## Anti-Rationalization

**AR-01 [Naked risk]:** You CANNOT "temporarily" leave a naked short to get a better fill on a second ticket. Legging is not a plan; it is an unmanaged option position with a fill price.

**AR-02 [The winner]:** You CANNOT close the profitable leg of a ratio structure first because it is the one showing green. Removing the long wing from `+1 K1 / −2 K2 / +1 K3` leaves two naked short calls. The winning leg is often the one whose removal is most dangerous.

**AR-03 [The roll]:** You CANNOT treat a roll as bookkeeping. It closes one position and opens another at a new strike, expiry, delta and event window, so it needs the same pre-action protocol as any new trade.

**AR-04 [Defined risk]:** You CANNOT skip the stop line because the loss is capped. The cap is the size of the loss, not permission to take it.

**AR-05 [The pin]:** You CANNOT let an ITM short ride into expiry because "assignment at max value is the same money". Assignment creates a stock position with overnight gap risk and a new margin requirement — a different position, not a late payment.

**AR-06 [The average]:** You CANNOT add contracts to a losing structure to lower its breakeven. Size belongs to `trade-sizing-recovery`; this skill may change structure, never size.

**AR-07 [The untested roll]:** You CANNOT roll into a later expiry to dodge a loss without re-pricing the new position as a standalone trade.

## Ground Rules — Read Before Anything Else

<!-- QUICK: 30s --> these are the five hard rules plus three mechanical guards. No exceptions.
The cap on a defined-risk structure is the size of the loss, not permission to take it: a
**$505 loss** on a 5-wide debit spread is still `$505` gone `[COMPUTED]` from `95 / 100` strikes
and a `5.05` debit.

| # | Negative constraint | Mechanical Trigger | Violation Response |
|---|---|---|---|
| **R1** | **NO NAKED RISK, EVER.** No leg order may leave any remaining exposure undefined-risk. | Before submitting, write the resulting leg list and test it: for every short strike, count long contracts at a protective strike for the same right; `covering_longs >= short_contracts`, or the shape is a named defined-risk structure (vertical, fly, condor, calendar, collar). | STOP. Do not submit. Restate the leg list, name the uncovered short, and re-design so the short closes in the SAME package as the long it depended on. Report: "R1 VIOLATION — {n} uncovered short {call/put} contract(s); unlimited (call) / strike-to-zero (put) risk." |
| **R2** | **Package first.** Same-structure changes go as ONE multi-leg order at a single net price. | Order plan contains two or more tickets touching the SAME structure in one session, OR any ticket whose intermediate state is undefined-risk. | STOP the multi-ticket plan; re-draft as one complex order. If rejected, split in the only safe order: **short buy-backs FIRST, wing/closing sells SECOND**. Record the rejection (venue message + timestamp). |
| **R3** | **Whole units for scale-outs.** Partial rungs close whole structure-units, never fractionated legs. | A planned quantity is not a whole multiple of the unit ratio — e.g. 3 flies open and the plan says "sell 1 of the 2 short bodies". | STOP. Round to whole units (1 fly = long K1 + 2 short K2 + 1 long K3 as one package). A fractional leg yields a position that is neither the original nor the exit. |
| **R4** | **A leg operation is a trade.** Event check, session eligibility, falsification, ledger row FIRST. | Any order that changes the leg set (close, open, roll, convert). Exception: a fill inside an already-authorized TP/trim protocol follows the standing TP rules — but still gets a ledger line. | STOP if the pre-action checklist is incomplete. If you cannot state the resulting position's invalidation and one-line expectancy, you do not yet know what you are doing. |
| **R5** | **Expiry is a hard wall.** No unattended ITM/ATM short leg is carried into expiration. | DTE ≤ 2 AND any short strike within ~1% of spot or already ITM. Also: DTE = 0 and a short leg is still open after 15:45 ET. | STOP everything else and run the pin-guard ladder; act by **15:45 ET on expiry day**. American-style short calls additionally carry early-exercise/ex-dividend risk before expiry day. |
| **R6** | **Ledger row FIRST, one tag always.** Tags: `SC` scale-out · `RU` roll-up · `VD` vertical downgrade · `HM` house-money · `PG` pin guard · `CD` condor defense · `CR` calendar roll · `UD` unbalance repair. | An order touching a leg is about to be submitted and no tagged ledger row exists for it. | STOP. Create the row. An untagged leg operation is indistinguishable from an accident at review and cannot be scored against the counterfactual. |
| **R7** | **Monetize into the IV spike, not after the crush.** | IV percentile ≥ 80 AND the structure is net long premium (a debit, or a paid-for structure) AND DTE > 1. | WARN then act: convert, downgrade or scale out before the event. Holding long premium through a known event is paying full price for a ticket you tear up at the draw. |
| **R8** | **No adds to losers — and this skill never adds.** No operation of THIS skill's own may raise contract count on a structure below its entry basis. A *defined-risk restructure* is a different action, not an add: it is permitted only when it passes the five-clause written gate that `options-position-lifecycle` owns, with the size decision belonging to `trade-sizing-recovery`. | Proposed order raises `net_contract_count` while `current_mark < entry_basis`, AND no written gate worksheet has passed for that restructure. | STOP. Restructure at the same size, or close. If a restructure is genuinely wanted, route it to its owners and run the five-clause gate in writing first; adding contracts to lower a break-even stays forbidden here. The anti-martingale ladder lives in `trade-sizing-recovery`. |

## The Expert's Mindset

A multi-leg structure is a package, but its legs are live, separable, independently exercisable
instruments. That is a fact about the instrument, not a metaphor: an exchange will separate them
the moment you ask, and an assignment will separate them whether you ask or not. Everything
dangerous and everything valuable about position management lives inside that gap.

### What leg-management masters know that others do not

- **Where the naked state hides.** Closing a winning long wing, selling a spread's long leg, rolling one side of a condor, buying back two fly bodies — each looks conservative and each can leave uncovered short contracts. Masters judge an order by the state it leaves behind.
- **That the second-best fill beats the best fill.** A package filling `$0.15` `[ESTIMATED]` wide of mid is usually cheaper than two single-leg fills that each look better, because a lone far-wing fill routinely costs the structure's remaining edge in spread. `[COMMON-PRACTICE]`
- **That theta, gamma and assignment are one curve.** In the last week, a short's value collapses as its assignment probability rises. Those are the same fact.
- **That the counterfactual is the only scoreboard.** Every leg operation is measured against simply closing the whole structure at the same moment.
- **That doing nothing is a decision with a price tag.** Holding is often correct and is always an action, correct only under a stated condition, and logged so later review can score it.

### When to break your own rules

| Rule | The one narrow exception | Why it stays safe |
|---|---|---|
| R2 package-first | A venue with no complex-order support, on a wide-book far wing, where the package was rejected twice | Then split shorts-first; the intermediate state is a defined vertical or a fully closed short side, never a naked short |
| R3 whole units | An odd-lot legacy position whose ratio was never whole | Repair the ratio deliberately, never by selling one leg of a balanced pair |
| R5 act by 15:45 ET | A short deep OTM with < 1% assignment probability worth less than the commission to close | Only with the do-not-exercise economics evaluated and the assignment outcome pre-accepted in writing |
| R8 no adds | An **add** is never legal — but a *defined-risk restructure* is not an add, and one that passes the five-clause written gate is permitted. It is owned by `options-position-lifecycle` (the gate) and `trade-sizing-recovery` (the size); this skill routes to them rather than executing it | The gate prices the resulting structure's max loss in dollars, against the account's band, before the order exists — so nothing is added to lower a break-even, and this skill still changes structure, never size |

## Deliberate Practice

```text
   observe one leg op ──▶ write the resulting leg list ──▶ submit as ONE package
            ▲                        │                            │
            │                        ▼                            ▼
      re-score vs. the        note where the naked          log the fill and
      counterfactual          test would have fired         slippage vs. mid
            └──────────────┬─────────┴────────────────────────────┘
                           ▼
              monthly: keep only the tags that beat
              closing the whole structure
```

| Level | Routine | Volume |
|---|---|---|
| Novice | After every leg op, rewrite the resulting leg list by hand and re-run the R1 test; compare to the platform screen | 20 ops |
| Intermediate | Pre-commit the decision matrix: for each open structure, name the trigger that would fire and the operation it would fire | 20 structures |
| Advanced | Counterfactual study — for 30 closed structures, compute what closing the whole package would have returned at each moment a leg op was executed | 30 structures |
| Expert | Maintain the desk's own conversion playbook; retire any tag that fails to beat the counterfactual across two regimes | ongoing |

## Operating at Different Levels

| Level | Scope | What the practitioner does |
|---|---|---|
| **L1** | One open multi-leg position | Applies the R1 leg-list test, closes a spread-to-long-only, executes a pin guard at ≤ 2 DTE. Follows the catalog literally |
| **L2** | A book of 5–20 structures | Runs the decision matrix at every review; chooses between scale-out, downgrade and conversion; manages a roll ladder |
| **L3** | Book-level structure policy | Defines the conversion taxonomy and tag set, the roll cap per position, the pin-guard band, and which operations are pre-authorized |
| **L4** | Framework design | Designs the counterfactual measurement so every leg op is comparable to a package close; sets the evidence format and the sign discipline |
| **L5** | Industry practice | Contributes new defined-risk conversions others adopt; formalizes the separation of package economics from leg executability |

### Scale depth — what changes with position size

| Scale | What changes | Transition trigger |
|---|---|---|
| Single position (1–2 lots) | Every leg op is judgment; there is no sample to score | You have closed 20 structures and want to compare techniques |
| Small book (3–20 structures) | Tags become meaningful; the counterfactual study becomes possible | You can no longer hold the leg lists in your head |
| Medium book (20–100 structures) | Pin guard must be scheduled, not remembered; the matrix becomes a written checklist | Two structures approach expiry in the same week |
| Desk (100+ structures) | Expiry-week operations are calendarized; assignment handling is a standing procedure; leg ops are pre-authorized by rule | One expiry Friday has more than five short legs within 1% of spot |

**Default level for this skill:** L2 — an open position with a live question about a leg.

## When to Use

1. A structure is at or beyond its first profit target and money must come out **without breaking the structure** — the scale-out path.
2. A far wing has decayed to noise while the body is still live and you want a defined-risk shape with less theta drag — the vertical downgrade.
3. Realized proceeds already cover the original debit and you want a runner to stay alive at no net risk — the house-money conversion.
4. A short leg is within about 1% of spot with two days or fewer to expiry — the pin guard.
5. One side of an iron condor has been tested and the other has not — condor defense, closing the threatened side only.
6. A calendar's front leg is inside 5 DTE with the thesis intact — the calendar roll.
7. A position has arrived unbalanced (legacy ticket, partial fill, an old naked short) and must be made defined-risk before anything else happens.
8. An assignment occurred overnight and the resulting stock position must be folded back into a structure or closed.

## When NOT to Use

| Situation | Correct skill |
|---|---|
| Choosing which structure to open, or building a new advanced structure | `options-strategist`, `advanced-options-structures` |
| Building a structure deliberately across two or more complete tickets | `staged-structure-formation` — the owner's hand-installed desk skill, **outside the shipped library**, so it may not exist in your environment; where it is installed it owns staged formation, and this skill owns surgery on what is already open. If it is not installed: let `options-strategist` choose each structure, require every ticket to be ONE complete defined-risk package that would stand alone as a trade, log the sequence against one umbrella ledger with a row per ticket, and count heat once for the idea |
| Deciding what deserves attention today across the book, and the review cadence | `options-position-lifecycle` |
| Setting per-trade size, loss bands, or triaging a loser's size | `trade-sizing-recovery` |
| Portfolio-level Greeks, DTE calendar, capital floors, margin utilization | `options-risk-engineer` |
| Routing an order, building an execution algorithm, automating a roll | `options-automation-engineer` |
| Deciding whether the structure is a good idea at all | `quantitative-analyst`, `volatility-arbitrage-engineer` for pricing; this skill manages only what exists |

## Decision Trees

<!-- QUICK: 30s --> DT1 routes; DT3 is the fly decision; DT4 is the expiry-day decision.

### DT1 — Which operation applies right now (master router)

```text
                     ┌──────────────────────────────────┐
                     │ OPEN multi-leg position reviewed │
                     └────────────────┬─────────────────┘
                                      │
                     ▼ run the R1 leg-list test FIRST
                                      │
       ┌──────────────────────────────┼──────────────────────────────┐
       │                              │                              │
  risk is broken                profit is mature              nothing fired
       │                              │                              │
       ▼ repair first                 ▼ take it in whole units       ▼ do not touch
  ├── naked ratio present?      ├── ≥1.8× target ─▶ SC: close ½     └── log no-op review
  │    └─▶ buy the short(s)     ├── spot at body ─▶ CLOSE full value
  │         back, ONE package   └── ≥2× or event ─▶ HM conversion
  └── legacy imbalance? ─▶ UD        │
       │                             ▼ wing dead / IV ≥ 80 / DTE ≤ 7
       ▼ shorts within ~1% &              └── VD downgrade (wing + short, ONE package)
         DTE ≤ 2 ─▶ PG
         act by 15:45 ET on expiry day
```

### DT2 — Is a scale-out legal on this structure?

```text
   Want to take profit ──▶ count open STRUCTURE-UNITS
        ├── units == 1 ──▶ ▼ cannot scale out without fractionating legs
        │                   ├── close the WHOLE structure (one package), or
        │                   └── HOLD if no other trigger fired (no-op review)
        └── units >= 2 ──▶ ▼ close WHOLE units
                            ├── fly/call: ≥ 1.8× first target ─▶ close half the units
                            ├── spread: ≥ 50% of max value ───▶ close whole units
                            └── log tag SC + re-arm the TP rung on the remainder
```

### DT3 — Fly leg decision: downgrade, convert, or roll?

```text
   Fly open: +1 K1 / −2 K2 / +1 K3
        ├── far wing ≥ 30% of fly value AND DTE ≤ 7 ──▶ ▼ VD: ONE package
        │      { sell 1× K3 + buy 1× K2 } ──▶ leaves +1 K1 / −1 K2
        ├── ≥ 2× basis OR a known event ahead ───────▶ ▼ HM: ONE package
        │      { buy 2× K2 + sell 1× K3 } ──▶ keeps +1 K1 (long-only house money)
        ├── spot at the body, strong trend, DTE ≥ 5 ─▶ ▼ RU: close the fly and open the
        │      same fly at higher strikes in ONE package; net debit ≤ realized proceeds
        └── wing illiquid AND short already cheap ──▶ ▼ HM at the decay price;
               never single-leg the wing
```

### DT4 — Short leg into expiry: guard, close, or accept?

```text
   DTE ≤ 2 on a short leg
        ├── ITM or within ~1% of spot ──▶ ▼ PG: close the short leg(s) in a package with
        │      the long that defined them; re-establish the structure AFTER the close
        ├── 1–3% OTM ──────────────────▶ ▼ schedule the guard; re-check each session;
        │      do not wait for expiry morning
        └── deep OTM, < 1% assignment ─▶ ▼ evaluate do-not-exercise economics
               ├── value > commission ──▶ close it anyway
               └── value < commission AND assignment outcome pre-accepted ──▶ let it go
```

### DT5 — Condor defense: which side, and how much?

```text
   One side tested
        ├── that side's short is breached ──▶ ▼ CD: close that side's TWO legs as ONE
        │      package ──▶ leaves a defined vertical; optionally roll THAT side out
        ├── both sides breached (real range break, not a scare) ──▶ ▼ close the WHOLE
        │      condor as one package
        └── price merely touched the short ──▶ ▼ HOLD and re-check next session
               (a touch is not a break)
```

### Decision matrix — condition → action → priority

Run every row on every open structure at every review. Priorities: **Stop** beats everything else.

| Condition | Action | Priority |
|---|---|---|
| Structure ≥ 1.8× first target (fly/call) | Close half of the units; runner TP 2.5–3× | Profit-lock |
| Spot reaches the fly's max-profit strike | CLOSE (value ≈ full width); never hope past it | Profit-lock |
| Spot at the body, strong trend, DTE ≥ 5 | Financed roll-up or vertical downgrade | Extension |
| ≥ 2× and/or an event or IV crush ahead | House-money long-only conversion | Risk-zero |
| Far wing ≥ 30% of fly value, DTE ≤ 7 | Vertical downgrade (wing + short as ONE package) | Risk-reduce |
| IV percentile ≥ 80 on a DEBIT structure, DTE > 1 | Monetize the long legs early (downgrade or house-money) before the event | Risk-reduce |
| Underlying closes beyond invalidation | Close the WHOLE structure as one package — this is the stop | Stop |
| Shorts within ~1% of spot, DTE ≤ 2 | Pin guard: close the shorts (and restructure) by 15:45 ET | Stop |
| Short leg at or inside the money, DTE ≤ 2 | Pin guard on the ITM short first; assignment is a new position, not an exit | Stop |
| Position already unbalanced (legacy) | Define risk immediately: package the shorts into a spread | Repair |
| One leg ≥ 3× its basis with ≥ 2 units held | Balanced partial: close whole units only | Profit-lock |
| Long wing dead but the shorts are alive | Downgrade or close the short side; never leave the shorts bare | Risk-reduce |
| Both wings decayed to zero, only the bodies carry value | Close the whole structure as one package — a body-only ratio has no defined exit | Stop |
| An overnight assignment has landed | Triage the stock as a NEW position the same day | Repair |
| A roll cap for this position is exhausted | Close the structure; a third roll is an exit you are avoiding | Stop |
| No row fires | No-op review: HOLD, log the decision, set the re-check date | Hold |

## Core Workflow

| Phase | Time | Deliverable |
|---|---|---|
| **1. Intake the live state** | ~2 min | Strikes, right, signed quantity, expiry, average price per leg, current structure mark |
| **2. Trigger classification** | ~2 min | One decision-matrix row named, or an explicit "no trigger fired → no-op review" |
| **3. Pre-action protocol** | ~3 min | Event check · session eligibility · falsification · the resulting position's invalidation and one-line expectancy |
| **4. Design the resulting state** | ~3 min | The post-order leg list, written out, with the R1 test passed on paper |
| **5. Order construction** | ~2 min | ONE multi-leg order at a single net price; shorts-first sequencing only if rejected |
| **6. Ledger first** | ~1 min | Tagged ledger row created BEFORE submission, with basis, invalidation, target, expectancy |
| **7. Submit, log, re-arm** | ~2 min | Fill logged with slippage vs. mid; position record updated; TP rungs re-armed |
| **8. Review** | weekly | Leg-op outcome scored against the close-the-whole-structure counterfactual |

## Best Practices

1. **Write the resulting leg list before every order.** The single control that prevents naked-short accidents, and it takes twenty seconds.
2. **Close whole structure-units, never fractionated legs.** Three flies are three units; you may close one, never one of a pair of bodies.
3. **Package every same-structure change at one net price.** Far wings and cheap shorts are exactly where single-leg execution is worst.
4. **Sequence short buy-backs first only when the package is rejected.** The reverse order passes through a naked ratio state.
5. **Monetize a long wing into an IV spike rather than holding it into the crush.** Value from volatility is paid once.
6. **Treat the short leg near expiry as a new position, not an exit.** Small remaining value and high assignment probability are the same fact.
7. **Act on the pin guard by 15:45 ET on expiry day.** Liquidity exists before the close and the contrary-instruction cut-off is still ahead of you — but the window closes.
8. **Price the house-money conversion honestly.** Compute `2 × body_mid − 1 × wing_mid` before calling a runner free — in the worked example that is a **$45 cost** after decay `[COMPUTED]` against a **$475 debit** before it `[COMPUTED]`.
9. **Roll a credit structure credit-or-flat only, and cap the count.** Two is the desk's working cap; beyond that, close.
10. **Never roll both sides of a condor on the same scare.** A broken range is a different trade; a touched range is not a reason to pay two spreads of slippage.
11. **One tag per operation, one operation per row.** Tags are what make the counterfactual study possible.
12. **Pre-commit the trigger, then obey it.** A trigger invented at the moment of the move is usually a rationalization.
13. **Re-band the position the instant an assignment lands.** The stock leg has its own basis, capital charge and gap risk.
14. **Score every operation against closing the whole structure.** The only test that distinguishes a technique from a habit.

### Safe conversion catalog — the exact leg arithmetic

A bull fly is modelled as `+1× K1 (near) / −2× K2 (body) / +1× K3 (far)`. Sign discipline is
absolute: a package that closes `K3` and buys `K2` leaves `+1 K1 / −1 K2`, and no other ordering
leaves the same state.

| Conversion | Package legs (exact) | Resulting state | Use when |
|---|---|---|---|
| Fly → vertical (downgrade) | `{ sell 1× K3 + buy 1× K2 }` | `+1 K1 / −1 K2` — a debit call spread, defined risk, less theta drag | Far wing dead or illiquid, or IV-crush risk outweighs the tail's value |
| Fly → long-only (house money) | `{ buy 2× K2 + sell 1× K3 }`, keeping `+1 K1` | `+1 K1` only — risk is the premium already paid | ≥ 2×, or into an event date; bodies already decayed |
| Spread → long-only | Buy back the short leg, keep the long | `+1` long leg; risk = premium paid | The ONLY single-leg close that is always structurally safe |
| Financed roll-up (fly) | ONE package: close the current fly, open the same fly at higher strikes | Same shape, higher strikes | Net debit ≤ realized proceeds AND the new max-profit body sits above spot with room |
| Condor defense | Close the threatened side's two legs as ONE package | A defined vertical on the surviving side | One side tested; optionally roll THAT side to a later expiry |
| Calendar roll | Whole structure to a later expiry as ONE package | Same shape, later expiry | DTE ≤ 5, thesis intact, net cost ≤ ~50% of current mark |

**Worked arithmetic on a concrete strike set.** Inputs are illustrative and marked
`[ESTIMATED]`; every derived figure is `[COMPUTED]` from them.

Strike set: XYZ spot **$100.00** `[ESTIMATED]`, one expiry —
`+1× 95C @ $6.10` · `−2× 100C @ $3.05` · `+1× 105C @ $1.35` `[ESTIMATED]`.

- Fly net debit `= 6.10 − 2(3.05) + 1.35` = **`$1.35` per fly = `$135` debit** `[COMPUTED]`.
- Max **value** at expiry with spot at the body = width `$5.00` = **`$500` per fly** `[COMPUTED]`; against the `$135` `[COMPUTED]` basis, the max **profit** is `500 − 135` = **`$365` per fly** `[COMPUTED]`. Value is not profit.
- Scale-out trigger `= 1.8 × 135` = **`$243` profit per fly** `[COMPUTED]`.
- Fly→vertical package: sell `1× 105C` `+$135`, buy `1× 100C` `−$305` = **`$170` net debit per fly** `[COMPUTED]`;
  the resulting vertical's basis `= 135 + 170` = **`$305`** `[COMPUTED]`, its width `= (100 − 95) × 100` = **`$500`** `[COMPUTED]`,
  and its max profit `= 500 − 305` = **`$195` per unit** `[COMPUTED]`. The 105 wing is sold, so the surviving spread is `95 / 100`, never `95 / 105`.
- Fly→long-only while the bodies are still rich: buy `2× 100C` `−$610`, sell `1× 105C` `+$135` = **`$475` net debit per fly** `[COMPUTED]` — expensive, so wait for decay.
- Same conversion after decay (spot `$96`, DTE 3, bodies ≈ `$0.25`, wing ≈ `$0.05`) `[ESTIMATED]`: **`$45` net debit per unit** `[COMPUTED]`, against a retained `95C` worth ≈ **`$155`** `[ESTIMATED]` — the runner costs 29% of its own value `[COMPUTED]`.
- Spread→long-only (`+1× 95C / −1× 100C` — the short leg is the **100C**): buy back `1× 100C` at `$0.05` = **`$5` cost per spread** `[COMPUTED]`, leaving the long `95C` alone.
- **Free-runner test.** Total debit `3 × $135` = **`$405`** `[COMPUTED]`; close one unit at `$455` and a second at `$470` `[ESTIMATED]` = realized **`$925`** `[COMPUTED]`; convert the last unit at `$45` `[COMPUTED]`; net cash `925 − 405 − 45` = **`$475`** `[COMPUTED]` ≥ 0, so the surviving runner is free.
- **Counter-check.** After only one close two units are still open, so the conversion costs `units_remaining × 45` = `2 × 45` = **`$90`** `[COMPUTED]`, and `455 − 405 − 90` = **`−$40`** `[COMPUTED]` — the runner was NOT yet free, and acting there would have been an un-priced bet.

## Error Decoder

| Symptom | Root cause | Fix | Lesson |
|---|---|---|---|
| Position shows short contracts with no long legs; margin requirement jumped overnight | The winning long wing was closed alone "because it was the one working"; removing long K1 from `+1 K1 / −2 K2 / +1 K3` leaves two naked short calls | Buy back the uncovered shorts at once as one package, then re-design the whole exit as a single complex order | Evaluate an order by the state it leaves, never by the leg it touches |
| A "free" runner conversion turned out to be a `$475` `[COMPUTED]` debit per unit (`2 × 3.05 − 1.35 = 4.75` per share × 100) | The conversion was priced from the wing's screen price with the bodies assumed cheap; the bodies had not decayed | Re-price leg by leg from live quotes: `2 × body_mid − 1 × wing_mid`. If it is a debit, wait for decay or skip | House money is an arithmetic result, not a feeling |
| Rolled a tested credit spread "for credit" and risk became unbounded | The roll dropped the protecting long and opened a farther short — a one-leg-at-a-time roll | Close the resulting naked short; rebuild as a genuine credit vertical, or take the original loss | A roll that pays you is a roll that removed something — name it before taking the cash |
| Short call assigned over a weekend; account woke up short shares | An ITM short call was carried through the ex-dividend date without evaluating early-assignment economics | Treat the stock position as a new position the same day; document the assignment cost | Around ex-dividend, an American-style short call with less remaining extrinsic value than the dividend carries real early-assignment risk — on a calendar day, not only at expiry |
| The "downgraded vertical" loses on a move the fly would have won on | The downgrade ran as two single-leg tickets and the second leg filled at a basis-changing price | Recompute the vertical's basis from actual fills; if basis exceeds width, close it | Arithmetic is only true at the price it actually filled |
| Tried to scale out half of a one-unit fly; ended with one long and two shorts | R3 ignored — "half a fly" is three fractionated legs, not a structure | Package the mismatch back into whole units, or close the whole structure | Ratios are integer constraints; a unit is indivisible |

## Error Recovery

| Symptom | First action | If that fails | Last resort |
|---|---|---|---|
| Package order rejected by the venue | Re-price once toward the natural (widen by ~10% of the remaining edge) and resubmit as one package | Sequence shorts-first so every intermediate state passes R1; record the rejection | Do not trade that leg today; re-attempt next session at the same target |
| Cannot close a short leg at any price (no bid, halted, zero liquidity) | Post a limit that accepts residual risk; try a neighbouring strike or expiry as substitute protection | Buy underlying-equivalent protection so the exposure becomes a known position | Pre-accept the assignment in writing, with the resulting stock position sized and funded |
| Resulting leg list fails R1 after a fill | Buy back the uncovered shorts immediately as one package | If the market has moved, close the whole structure as one package | Escalate — an uncovered short is the one state this skill never tolerates overnight |
| Roll executed, but the new body no longer sits above spot | Re-evaluate as a fresh position against the event calendar; close if it fails | Convert to a vertical downgrade if the far wing still has value | Close the whole structure; a roll into a losing geometry is an exit you did not take |
| Assignment landed and the stock is unwanted | Evaluate the stock against the thesis and the capital plan the same day | Close the stock, or re-establish as a covered position at a size the plan allows | Hold and manage the stock only after re-banding it in the capital plan |

**Hard failure boundary:** if three different constructions of the same operation are all
rejected or all fail the R1 test, stop. The correct output is "close the whole structure as one
package" — a decision, not a defeat.

## Cross-Skill Coordination

| Upstream Skill | Artifact you need | What you do with it |
|---|---|---|
| `trade-sizing-recovery` | Authorized size, loss band, whether the mark is inside the band | Leg ops change structure, never size; if the fix needs more contracts, hand it back |
| `options-risk-engineer` | Portfolio Greeks, DTE calendar, capital floors, margin utilization | Decides whether a structure may be extended at all; this skill never rolls past a portfolio floor |
| `options-strategist` | Original thesis, invalidation line, profit-taking protocol | Surgery is legal only while the thesis is intact; a broken thesis is a close, not a conversion |
| `advanced-options-structures` | Roll caps and the structure's construction rules | Inherited: no legging, liquidity floors, ex-dividend awareness, buying-power discipline |
| `staged-structure-formation` — the owner's hand-installed desk skill, **outside the shipped library** | Whether the position was built across two or more complete tickets | Where it is installed, it tells you which legs are independent defined units versus one package. If it is not, read the answer off the fill record instead: separate tickets on separate timestamps are independent units — one umbrella ledger with a row per ticket, heat counted once for the idea, and each ticket treated as a full defined-risk trade rather than half of one |

| Downstream Skill | Deliverable | What they will do with it |
|---|---|---|
| `options-position-lifecycle` | Tagged ledger row, the resulting leg list, re-armed TP rungs | Runs the next review cycle against the new state |
| `options-risk-engineer` | Post-operation exposure change (Greeks, margin, DTE) | Re-scores portfolio risk and capital floors |
| `trade-performance-analyst` | The counterfactual comparison row | Attribution: which tags earn their keep and which to retire |
| `trade-sizing-recovery` | Realized proceeds and the surviving structure's new basis | Decides whether the remainder is a free runner or still carries risk |
| `trading-desk-sheets` | The state snapshot the workbook renders from | Renders account, positions and P&L tabs |

## Proactive Triggers

| # | Detectable pattern | Action |
|---|---|---|
| T1 | Any short leg within ~1% of spot and DTE ≤ 2 | Fire the pin guard; schedule the action before 15:45 ET on expiry day |
| T2 | Spot reaches the fly's maximum-profit strike | Close at full value; never wait for a better print above the body |
| T3 | Structure ≥ 1.8× first profit target | Scale out whole units; re-arm the TP rung on the remainder |
| T4 | A long leg's value ≥ 3× its own basis | Take profit in whole units, or convert the structure to long-only |
| T5 | IV percentile ≥ 80 and the structure is net long premium | Monetize the long legs before the event; do not hold into the crush |
| T6 | A far wing's value ≥ 30% of the structure's value with DTE ≤ 7 | Downgrade to a vertical with the wing + short as one package |
| T7 | Spot closes beyond the invalidation line | Close the whole structure as one package — this is a stop, not a conversion |
| T8 | An ex-dividend date falls inside the remaining life of a short call | Evaluate early-assignment economics; close or roll the short before the date |
| T9 | Unit count is odd or the ratio is non-integer | Flag as legacy imbalance; schedule a deliberate ratio repair (tag `UD`) |
| T10 | A calendar's front leg reaches DTE ≤ 5 with the thesis intact | Roll the whole structure to a later expiry as one package, net cost ≤ ~50% of current mark |

## Anti-Patterns

<!-- QUICK: 30s --> scan this table before designing any leg order.

| ❌ Forbidden | ✅ Instead |
|---|---|
| ❌ Closing "just the money leg" of a fly because it is green — removes a wing and leaves naked ratio shorts | ✅ Close a whole structure-unit as one package, or do nothing |
| ❌ Rolling a tested spread "for credit" into an undefined-risk shape | ✅ Close the resulting naked short; rebuild as a genuine credit vertical, or take the loss |
| ❌ Doubling contracts to "average" a losing structure — and equally, calling any add an "approved restructure" without the worksheet | ✅ Restructure at the same size, or close — adds to losers are out of scope here, and a restructure is only real once it is written on the owner's five-clause gate. That gate belongs to `options-position-lifecycle`, the size to `trade-sizing-recovery` |
| ❌ Eating a pin because "it will expire worthless" | ✅ Guard at ≤ 2 DTE and act by 15:45 ET on expiry day |
| ❌ Legging on a wide book when the far wing fills better inside the package | ✅ Submit the package first; widen once; sequence only on rejection |
| ❌ Selling the long leg of a spread while the short remains | ✅ Buy back the short and keep the long — spread-to-long-only is always structurally safe |
| ❌ Rolling both sides of a condor on the same scare | ✅ Close the threatened side's two legs as one package; roll only that side |
| ❌ Selling "half a fly" (one of two bodies) to take profit | ✅ Count structures in units; a unit is indivisible |
| ❌ Treating a roll as bookkeeping — no ledger row, no event check | ✅ Full pre-action protocol; ledger row first |
| ❌ Buying back a short with a market order on an illiquid wing name | ✅ Post a limit; if the package is rejected, sequence shorts-first with a limit |
| ❌ Holding a long wing into the event because it "still has value" | ✅ Monetize into the IV spike; value from volatility is paid once |
| ❌ Assuming the package filled at mid | ✅ Log the actual fill and re-derive the surviving basis from it |

## State Log

| Field | Type | Persists across | Purpose |
|---|---|---|---|
| `leg_op_ledger` | Array of rows | Cross-session | One row per op: `{tag, timestamp, structure_id, resulting_leg_list, entry_basis, invalidation, target, expectancy, fill, slippage_vs_mid, counterfactual}` |
| `resulting_leg_list` | Written artifact | Session | The post-order leg list with the R1 test result — written before submission, not after |
| `open_structure_units` | Integer per structure | Session | Gates whether a scale-out is legal at all |
| `pin_guard_queue` | Sorted list | Session | Short legs at DTE ≤ 2 or within ~1% of spot, each with its 15:45 ET deadline |
| `realized_proceeds` | Currency per structure | Cross-session | Cumulative realized cash — the numerator of the house-money test |
| `no_op_reviews` | Array | Cross-session | Structures reviewed with no trigger fired; doing nothing is a decision and needs a record |
| `technique_scorecard` | Tag → wins/losses vs. counterfactual | Cross-session | Retires a tag that cannot beat closing the whole structure |
| `assignment_events` | Array | Cross-session | Timestamp, leg, resulting stock position, disposition, cost |

**Anti-drift check:** before any leg operation, confirm the ledger leg list matches the
platform's position screen leg for leg, including sign and quantity. A drift is the first
symptom of an operation that was never fully executed, or of an untriaged assignment.

## Production Checklist

- [ ] **CR1 — Leg list written** before submission. Verify: present in the ledger row, not only in the message.
- [ ] **CR2 — R1 test passed.** Every remaining short has a covering long, or the shape is a named defined-risk structure. Verify: count per right at the resulting strikes.
- [ ] **CR3 — Trigger named.** One matrix row quoted verbatim, or an explicit no-op review.
- [ ] **CR4 — Event check done.** Earnings, ex-dividend and macro prints inside the remaining life listed with a decision each.
- [ ] **CR5 — Session eligibility stated** (regular vs. extended, and whether the leg type trades in it).
- [ ] **CR6 — Falsification recorded** in one sentence.
- [ ] **CR7 — Package constructed** as one complex order at a single net price, not two single-leg tickets.
- [ ] **CR8 — Rejection logged** (venue message + timestamp) before any sequencing fallback.
- [ ] **CR9 — Shorts-first sequencing** applied only after a rejection, with each intermediate state passing R1.
- [ ] **CR10 — Ledger row precedes the order,** carrying exactly one of the eight tags.
- [ ] **CR11 — Fill logged with slippage** vs. mid at drafting time, in the structure's own units.
- [ ] **CR12 — Basis re-derived from the fill,** not from the plan.
- [ ] **CR13 — TP rungs re-armed** on the remainder at explicit price levels.
- [ ] **CR14 — Size unchanged** — net contract count did not rise on a structure below its entry basis.
- [ ] **CR15 — Pin-guard queue updated** with any new short inside the ≤ 2 DTE / ~1% band.
- [ ] **CR16 — Counterfactual row opened** with the package close price at the operation's timestamp.
- [ ] **CR17 — Portfolio handoff** made to `options-risk-engineer` when the exposure change is material.
- [ ] **CR18 — Assignment triage closed** the same day, with the stock re-banded in the capital plan.

## What Good Looks Like

Good leg management looks boring and reads like arithmetic. The output names the live leg list,
names the trigger, writes the post-order leg list, states the resulting structure's worst case
in dollars, submits one package, and records a row a reviewer can score against a counterfactual
six weeks later. It never contains "I will close the other leg right after", and it never
converts a defined-risk structure into an undefined one as a side effect of taking a profit.
When the right action is to do nothing, the output says so, gives the condition under which that
remains true, and records the no-op review as a decision.

Signs of dysfunction: a leg operation described in prose with no resulting leg list; a profit
taken by selling one leg of a pair; a roll that cannot state its net cost or credit in dollars,
such as a **$170 debit** called "even" `[COMPUTED]`; a pin guard that starts after the close.

| ☐ | Completion criterion | Verification |
|---|---|---|
| ☐ | Complete when the resulting leg list is written out and every short in it has a covering long, or is a named defined-risk structure | Re-count shorts vs. covering longs per right at the RESULTING strikes |
| ☐ | Complete when exactly one decision-matrix row is named as the trigger, or the op is recorded as a no-op review | The ledger row quotes the matrix condition verbatim |
| ☐ | Complete when the operation is submitted as one multi-leg order at a single net price | The fill record shows a complex/package order type |
| ☐ | Complete when the resulting structure's worst case is stated in dollars per unit and in total | Multiply per-unit maximum loss by surviving units; label the figure `[COMPUTED]` with strike arithmetic |
| ☐ | Complete when the surviving basis is derived from the actual fill rather than the plan | Recompute basis from fill prices; a mismatch invalidates the planned target |
| ☐ | Complete when every event inside the remaining life is named with a decision attached | List earnings, ex-dividend and macro dates before expiry, each marked hold/close/roll |
| ☐ | Complete when any short inside the pin band has a scheduled action time before 15:45 ET on expiry day | The pin-guard queue carries a timestamped deadline per leg |
| ☐ | Complete when the net contract count did not increase on a structure below its entry basis | Compare pre- and post-operation counts against the entry basis |
| ☐ | Complete when a roll states its net cost or credit in dollars and the new body strike relative to spot | Roll row shows `net_cost_usd` and the new body strike vs. spot |
| ☐ | Complete when the close-the-whole-structure price at the operation's timestamp is recorded | The counterfactual field is populated |

## Verification Guardrails

- **Pre-generation.** Is the live leg list complete (strikes, right, signed quantity, expiry, average price)? Is any leg's state assumed rather than read from the position screen? Is the trigger named? Has the event calendar been checked inside the remaining life?
- **Post-generation.** Re-read the resulting leg list and re-run the R1 test on it. Confirm every dollar figure is labelled `[COMPUTED]` with its formula or `[ESTIMATED]` with its named input, and that no figure is presented as a measured result. Confirm the ledger row precedes the order in the narrative.
- **Continuity.** The ledger row must connect to the prior row for the same structure. A structure whose last operation is absent from the log has drifted.

## References

| File | What it covers |
|---|---|
| `(references/safe-conversion-catalog.md)` | The catalogue of defined-risk conversions with exact leg arithmetic and sign discipline |
| `(references/leg-arithmetic-worked-examples.md)` | Worked examples on a concrete strike set, all `[COMPUTED]` from stated `[ESTIMATED]` inputs |
| `(references/no-naked-risk-guardrails.md)` | Running the R1 test mechanically, per structure shape, and what to do when it fails |
| `(references/fly-rollup-and-downgrade-mechanics.md)` | Financed roll-ups and fly-to-vertical downgrades: gates, costs, and when they lose |
| `(references/house-money-conversion.md)` | The long-only conversion, the subtrahend, the free-runner test, and event-date usage |
| `(references/pin-risk-and-assignment-guard.md)` | Pin risk, early exercise, ex-dividend economics, the 15:45 ET deadline, the fallback ladder |
| `(references/condor-defense-playbook.md)` | Defending one side, the touched-versus-broken test, and why never to roll both sides |
| `(references/calendar-roll-windows.md)` | Calendar roll windows, cost caps, and the DTE boundary condition |
| `(references/unbalanced-legacy-repair.md)` | Repairing a structure that arrived with a non-integer ratio or an uncovered short |
| `(references/package-order-execution.md)` | Package vs. leg-by-leg execution, why lone far wings fill worse, and the sequencing rule |
| `(references/when-not-to-touch-a-leg.md)` | The no-op case: conditions under which every leg operation is the wrong action |

Meta-layer: setup classification before an operation is called a repair or an extension uses the
Pattern Recognition Engine at
`skills/14-finance/options-strategist/references/pattern-recognition-engine.md`.

## Gotchas

### Failure Modes

1. **What goes wrong — the invisible naked short.** Closing a long wing or a spread's long leg leaves uncovered shorts; it reads as profit-taking and behaves as an undefined-risk position.
2. **What goes wrong — the intermediate naked state.** A two-leg sequence in the wrong order is briefly naked. The window is short; a gap inside the window is not.
3. **What goes wrong — fractional legs.** Selling one of two bodies leaves a ratio structure that is neither the original nor an exit, and the original plan's rules no longer fit it.
4. **Worst case — the debit roll that prints as a credit.** Dropping the protective leg and opening a farther short can show a credit while the risk becomes unbounded.
5. **What goes wrong — the un-priced conversion.** Computing "house money" from the wing's screen price instead of `2 × body_mid − 1 × wing_mid` produces a runner that was paid for — a **$475 debit** misread as a free trade `[COMPUTED]`.
6. **Worst case — eating a pin.** An ITM short into expiry becomes a stock position with overnight gap risk. *Exit condition:* the guard fires at DTE ≤ 2, not on expiry morning.
7. **What goes wrong — early assignment around ex-dividend.** An American-style short call with less remaining extrinsic value than the dividend can be assigned days before expiry, when no guard was scheduled.
8. **Worst case — the illiquid wing stop-loss.** A stop on a far wing with no bid fills at whatever price exists, which can exceed the structure's remaining edge.
9. **What goes wrong — the both-sides condor roll.** Paying two sides of slippage on a scare doubles transaction cost and weakens the structure without a thesis.
10. **What goes wrong — basis drift.** The target computed from plan prices, not fill prices, sits at a level the position cannot reach.
11. **Known limitation — rolling past a portfolio floor.** A roll that extends DTE past the capital plan's floor. This skill cannot see portfolio constraints; the handoff is mandatory.
12. **Edge case — the untriaged assignment.** The stock position is held "temporarily" and never re-banded, so capital and risk sit outside the plan indefinitely.

### Known Limitations and Edge Cases

- **European-style, cash-settled products** exercise only at expiry and settle in cash. The pin guard's timing still applies to the settlement figure; the assignment-to-stock failure modes do not.
- **Index options** are typically cash-settled and may have a different last-trading day from the underlying's expiry. Verify the product's settlement and last-trade conventions.
- **Halts and corporate actions** can suspend the ability to close a leg at any price.
- **This skill cannot see the whole portfolio.** A leg operation that is locally safe can still be globally infeasible.
- **Approximation is unavoidable in the last hour of an expiry day.** Quotes on near-worthless short legs are indicative; the fill is what matters.
- **A technique that beats the counterfactual in one regime may lose in another.** Score across regimes, not once.

## Anti-Hallucination

This skill sits where an invented number becomes a real loss. A fabricated breakeven, a made-up
fill, or a hallucinated assignment rule will be acted on before it is checked.

- **Admit uncertainty — never fabricate.** If the live quote, the current leg list, or the ex-dividend date is missing, say so: "I need live marks on the bodies before I can price the conversion — quote both bodies and the far wing, then I will compute `2 × body_mid − 1 × wing_mid`." Never state a conversion cost you have not subtracted, and never state a worst case without the strike arithmetic that produces it.
- **Flag your knowledge cutoff.** Exercise procedures, contrary-instruction cut-offs, margin requirements and complex-order support are venue- and broker-specific and have changed over time. State it: "My knowledge of exchange and clearing exercise conventions is current as of the cutoff recorded in the ledger; verify the contrary-instruction cut-off and the assignment schedule against your broker's current documentation before relying on the 15:45 ET working deadline."
- **Never guess security, product or regulatory constraints.** Do not infer whether a product is American- or European-style, physically or cash-settled, whether a broker supports native complex orders, or what the margin regime requires. Say: "This requires verification against your broker's product specification and margin schedule, and against FINRA Rule 4210 for the margin regime. I cannot state it as fact."
- **Tag every number.** `[VERIFIED]` traced to a named public source · `[COMPUTED]` arithmetic from stated inputs with the formula shown · `[ESTIMATED]` an assumed input, named · `[BROKER-VERIFIED]` true for a specific broker's published behaviour, not universal · `[COMMON-PRACTICE]` desk convention without a vendor-independent source. An untagged number is treated as unverified and is not acted on.
- **What is genuinely true here.** It is `[VERIFIED]` against the OCC's standard options disclosure document and against US options exchange rules that a listed option is a separable instrument, that a multi-leg position is not one instrument to the exchange, that assignment converts an option into a position in the underlying, and that an American-style short call carries early-assignment risk around an ex-dividend date when the dividend exceeds the option's remaining extrinsic value. It is also `[VERIFIED]` that US options exchanges provide complex/package order types that execute at a single net price. Sources for these claims are named, not linked: the OCC's investor and clearing documentation, CBOE and other US options exchange rulebooks, and broker margin schedules. Where this skill cites a rule it is published by the exchange or the clearing corporation; where it cites a price, the data comes from the desk's own fill records — verified against them — not from Yahoo Finance, Bloomberg or any other market-data vendor.
- **Every threshold here is approximate and data-backed.** The 1.8× scale-out trigger, the ~1% pin band, the ≤ 2 DTE guard, the ≤ ~50% calendar-roll cost cap and the ≥ 30% dead-wing test are **data-backed desk thresholds derived from data** on this desk's own leg-op study — not exchange rules, and not a guarantee. They must be re-derived on your own book. Past performance of any tag does not predict its next result, and conversion arithmetic is approximate once quotes are stale.

### Regime coverage — how leg surgery changes

| Regime | What changes | Why |
|---|---|---|
| **Bull market / uptrend** | Wings get exercised; scale-outs trigger early and often. Prefer downgrades and rung scale-outs; the main risk is converting out of a winner too early | In a sustained uptrend the far wing becomes valuable and the tested side's short is the one at risk |
| **Correction / pullback** | The tested side flips. Condor defense moves to the side that was previously safe; long-premium structures gain and debit conversions get cheap | A few-percent pullback re-tests the side that had margin; the other side's wing was never priced for it |
| **Bear market / downturn / recession** | Short calls decay and wings die, so downgrades and house-money conversions get cheap and become the primary tool; long-only runners keep exposure without premium risk | A persistent drawdown makes the far call wing worthless while the body still carries value |
| **Crash / tail event / black swan (March 2020, the 2008 financial crisis, any market collapse)** | Every leg operation becomes a liquidity problem, not a structure problem: packages do not fill, wing bids vanish, margin requirements rise mid-position. Only a pre-committed action still works | A market collapse removes the counterparty for the leg you want to close, so the decision must have been made earlier |

Regime classification uses the Pattern Recognition Engine meta-layer cited above; its thresholds
and these are the same kind of evidence — derived from data, approximate in application, never a
guarantee.
