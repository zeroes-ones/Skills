---
name: equity-tax-lot-and-exit-management
description: >
  Use when a holder of shares asks "which lots should I sell", "how do I trim half a position
  across lots", "should I harvest a loss", how the "wash sale" window works, "should I wait for
  long-term capital gains", about "year-end tax selling", "average cost vs specific lots", or
  "dividend capture". Handles lot-level selection on a sale — which lots, in what order, when
  the trim is only half a position — plus loss harvesting, wash-sale-safe re-entry,
  holding-period completion, the qualified-dividend window, and the after-tax comparison that
  decides between them. Whether and how much to trim is equity-position-lifecycle's call. Do NOT
  use to decide whether to act at all (equity-position-lifecycle), for margin, borrow,
  concentration or liquidity (equity-risk-and-capital-engineer), for position sizing
  (portfolio-signal-manager, algorithmic-trader), or to choose the security itself
  (fundamental-analyst, technical-signals-engineer). Computes and orders lots; it is not tax
  advice.
license: MIT
author: "Sandeep Kumar Penchala"
type: finance
status: experimental
version: "1.0.0"
updated: 2026-10-14
tags:
  - tax-lots
  - specific-identification
  - wash-sale
  - loss-harvesting
  - holding-period
  - long-term-capital-gain
  - qualified-dividend
  - ex-dividend
  - after-tax-pnl
  - year-end-tax-selling
  - partial-scale-out
  - equity-exit
token_budget: 4000
chain:
  examples:
  - skills/14-finance/equity-tax-lot-and-exit-management/examples/backtest
  consumes_from: []
  feeds_into: [equity-position-lifecycle]
---

# Equity Tax Lot and Exit Management — after-tax surgery on a share position

> **Portability target:** spec-level. Broker order-ticket fields, lot-relief menus and
> cut-off times below illustrate a **capability** (per-lot identification on a sale), not a
> required venue. Every rule here is executable anywhere that lets you choose which tax
> lots a sell order consumes and lets you record that choice before the order is sent.

> **This skill is not tax advice.** It computes, orders and documents. Confirm every rule
> quoted here against the current text of the Internal Revenue Code, the current IRS
> Publication 550, and your broker's published lot-relief procedure before relying on it.

<!-- QUICK: 30s --> (1) A position is not one decision, it is N lots — name the lots before
you name the order. (2) The objective function is AFTER-tax P&L, never gross. (3) Loss sales
live inside a **61-day box** (30 before → 30 after) that looks BOTH ways. (4) The earliest
long-term sale is **buy date + 1 year + 1 day**. (5) Tax changes WHEN you sell a position you
were selling anyway; it never turns a sell into a hold.

<!-- STANDARD: 3min --> the nine hard rules, the four lot-ordering objectives, and the
holding-period completion formula are the whole skill. Everything else is date arithmetic.

<!-- DEEP: 10+min --> the identification mechanics in
`(references/specific-identification-mechanics.md)`, the wash-sale algebra in
`(references/wash-sale-window-playbook.md)`, and the dividend clocks in
`(references/qualified-dividend-window.md)` and `(references/ex-dividend-under-t-plus-one.md)`
before a real harvest or a year-end programme.

## Route the Request

<!-- QUICK: 30s --> if a position is already open and the question is about WHICH shares to
sell, WHEN to sell them, or what the sale costs AFTER tax, you are in the right place.

### Auto-route — fires without asking

| Signal in the request | Operation | Gate that must pass first |
|---|---|---|
| "which lots should I sell" / "should I sell the old ones" | Lot-selection ladder (LS) | the lot table is read from the broker, not reconstructed from memory |
| "harvest a loss" / "tax-loss sell" | Harvest design (HL) | no purchase of the same or a substantially identical security inside the 61-day box |
| "how does the wash sale rule work" / "did I trip it" | Wash-sale box audit (WB) | every purchase of the same or a similar security listed for 30 days either side |
| "should I wait for long-term capital gains" | Holding-period completion (HP) | the buy trade date and the intended sale trade date are both known to the day |
| "year-end tax selling" / "what do I sell in December" | Year-end harvest calendar (YE) | the re-entry date is chosen at the same time as the sale date |
| "average cost or specific lots" | Lot-relief method audit (LR) | the broker's current default and election mechanics are confirmed in writing |
| "dividend capture" / "buy before the ex-date" | Dividend-clock check (DC) | the 61-of-121 window and the T+1 last-day-to-buy are both computed |
| "partial sell" / "take a third off" | Partial scale-out (PS) | the sale is sized in whole lots, or the split is identified lot by lot |
| "I shorted it and got a dividend bill" | Short-side cost triage (SC) | the short's open days are counted against the 46-day deductibility test |
| "just sell some" with no lot question | No-op review | nothing fired → HOLD the lot decision and record it |

### Intent route — ask, do not assume

1. **The live lot table** — acquisition date, quantity still open, basis per share, and any basis adjustment already applied. Lot work is designed against the lot table, never against an average cost, a total share count, or a memory of the buy.
2. **The broker's default lot-relief method** and what it takes to override it for one order. This single fact changes the answer, and it is broker-specific.
3. **The objective** — harvest, fund, reduce concentration, finish a thesis exit, or complete a holding period. The objective picks the lot, not the other way round.
4. **Realized gain/loss for the year so far**, by character. A harvest is worth something only against a real offset or a real carry-forward.
5. **Every purchase of the same or a similar security in the last 30 days**, including other accounts and retirement accounts. The wash-sale window looks backwards too.
6. **The marginal rate pair** — short-term and long-term, surtax included — or an explicit "I do not know, use a placeholder".
7. **The intended re-entry**, if any. The re-entry date is part of the harvest design, not a later decision.

## Anti-Rationalization

**AR-01 [The default]:** You CANNOT let the broker's default lot-relief method decide your tax bill by omission. A default is a choice made by someone who was not thinking about your taxes, at a price you never measured.

**AR-02 [The rate]:** You CANNOT hold a broken thesis "for the long-term rate". The rate differential is worth a few percent of cushion; a broken thesis is worth the whole position. Tax changes WHEN you sell; it never changes WHETHER the position deserves to exist.

**AR-03 [The loss]:** You CANNOT bank a loss and then re-buy the same name "because it is cheaper now". Re-buying inside the box does not delete the loss — it defers it into the replacement shares' basis, which is worse than useless if you never sell those.

**AR-04 [The substitute]:** You CANNOT call a replacement "different" because the ticker differs. Substantially identical is a facts-and-circumstances test, and you do not get to pick the facts. Verify, or stay out.

**AR-05 [The calendar]:** You CANNOT assume December 31 is the harvest deadline when you also intend to be back in the position in January. The two dates are one decision.

**AR-06 [The capture]:** You CANNOT treat a dividend as free money collected by owning a stock for one day. The price drops by roughly the dividend, and the window is about two months long if you want the favourable rate.

**AR-07 [The average]:** You CANNOT reason about a position from its average cost when the account holds lots with bases 3× apart. The average is a display convenience, not a lot.

**AR-08 [The alibi]:** You CANNOT keep a losing lot because "selling it now would trip the wash sale". Not buying is free. The rule never forces you to hold anything.

## Ground Rules — Read Before Anything Else

| # | Negative constraint | Mechanical Trigger | Violation Response |
|---|---|---|---|
| **R1** | **The broker's default is not a decision.** No sale may consume lots unless the intended selection was identified and confirmed at or before the sale. | A sell order is about to be sent and no written lot instruction exists for it, OR the ticket shows no lot-relief field and none was requested. | STOP. Write the lot instruction, or state in one line "default relief accepted: {method}" as a deliberate choice. An unstated default is an unpriced cost. |
| **R2** | **The 61-day wash-sale box looks BOTH ways** — 30 days before through 30 days after the loss sale. | Any loss sale is planned or executed AND a purchase of the same or a substantially identical security exists in the prior 30 days or may occur in the next 30. | STOP the harvest. Move the sale outside the box, or stay out of the security until day 31. Never assume the loss survived; recompute the allowed share. |
| **R3** | **Identification is a documented act, not an intention.** The exact requirement and your broker's cut-off must be verified. | A specific-lot sale is planned and the broker's deadline for the instruction, or the confirmation format, has not been read. | STOP. Read the broker's published procedure first. If it cannot be confirmed, the sale is a default-relief sale and must be labelled that way. `[BROKER-VERIFIED]` |
| **R4** | **After-tax is the objective function.** Every lot comparison is stated in after-tax proceeds. | Two candidate lots are compared and the comparison shows gross P&L, or a rate, but not after-tax dollars. | STOP. Restate both as after-tax dollars with the rate pair shown. A gross comparison between lots of different character is not a comparison. |
| **R5** | **Tax never converts a sell into a hold.** It may change the ORDER and the DATE; it may not be the reason the position exists. | The only stated reason for holding is a rate, a date or a window, with no thesis, valuation or risk statement. | STOP. Write the non-tax reason this position is held. If there is none, the tax question is moot — sell. |
| **R6** | **No substitute without a substantial-identity check.** | A harvest names a replacement ticker and the entry says "similar sector" or "close enough" with no analysis. | STOP. Ask the facts-and-circumstances question and record the answer, or stay out 31 days. A wrong call converts a real loss into a deferred one. |
| **R7** | **A dividend has two clocks, not one.** Ex-date ownership and the qualified-dividend holding window are different tests. | A dividend-motivated purchase is planned and only the ex-date has been considered. | STOP. Compute the last day to buy under T+1 and the 61-of-121 window. If the second cannot pass, the dividend is ordinary income and the trade changes character. |
| **R8** | **The short side's dividend cost has its own clock.** A payment in lieu is deductible only if the short stayed open at least 46 days — over one year for an extraordinary dividend. | A short is closed at a profit before 46 days and the payment in lieu was assumed deductible. | STOP. Recompute the after-tax result with the payment disallowed before calling the trade a win. `[VERIFIED — IRC §263(h); IRS Pub 550]` |
| **R9** | **Ledger row FIRST, one tag always.** Tags: `LS` lot selection · `HL` harvest · `WB` wash-sale audit · `HP` holding-period completion · `YE` year-end · `LR` lot-relief audit · `DC` dividend clock · `PS` partial scale-out · `SC` short-side cost. | A sale or purchase is about to be submitted and no tagged row exists for it, carrying the lot instruction and the 61-day window. | STOP. Create the row. An untagged lot decision cannot be scored later and cannot be defended to anyone. |

**Hard boundary.** This skill does not give tax advice and does not file anything. It computes lot-level after-tax outcomes, orders the lots, and writes the evidence down. Rates and brackets are inputs supplied by the reader — never assumed silently, never invented. `[COMMON-PRACTICE]`

## The Expert's Mindset

A share position looks like one thing on a screen. It is not. It is a stack of separately acquired, separately dated, separately priced parcels, and the tax law treats each one differently. The screen averages them because averaging is cheap; the tax code does not average them, and the gap between the average view and the lot view is where every real decision lives.

### What lot-management masters know that others do not

- **That the position's average cost is a fiction the broker maintains for convenience.** Two lots bought four months apart at 3× different bases are not one asset.
- **That the date is worth more than the rate.** Moving a sale across a holding-period boundary changes the character of the whole gain; the rate differential itself is worth only a few percent of cushion. Dates are the lever; rates are the payoff.
- **That a loss is an asset with an expiry and a contamination radius.** It is worth something only against a real offset, and a purchase you made eleven days ago in a different account can spoil it.
- **That the objective function is after-tax dollars, and that the residual position's embedded tax liability travels with it.** Selling the loss lot and keeping the low-basis lot swaps realized tax for deferred tax.
- **That doing nothing is a legitimate lot decision.** Not buying the replacement is free and is always available. The wash-sale rule constrains purchases, never holds.

### When to break your own rules

| Rule | The one narrow exception | Why it stays safe |
|---|---|---|
| R2 wash-sale box | An **unrelated but economically similar** security — a broad sector fund instead of a single name, or a competitor — where the identity question has been asked and answered in writing | This is one of the few places where a substitute is genuinely legitimate rather than an evasion, because the test is substantial identity, not economic exposure. It is still a judgement call: verify, and do not stretch it |
| R5 tax never converts a hold to a sell | A position whose thesis is intact and whose only defect is a *date* — a lot nine days short of long-term with an unchanged risk outlook | The exception is narrow by construction: it requires the non-tax reason to be written down first. If it cannot be written, R5's stop fires |
| R1 identify your lots | A position whose lots are identical in basis and acquisition date, in an account where lot relief does not apply | There is nothing to choose. State that in one line and move on |

## Deliberate Practice

```text
   read the LOT table ──▶ name the objective ──▶ write the lot instruction
            ▲                     │                        │
      re-score after-tax    check the 61-day box     confirm with the broker
      vs. the FIFO baseline  both ways, every        BEFORE the order is sent
            └────────────┬───── account ─────────┬───────────┘
                         ▼                        ▼
              monthly: which lot-ordering      ledger row per sale,
              rule beat the FIFO default?      one tag, after-tax delta
```

| Level | Routine | Volume |
|---|---|---|
| Novice | For every position, write the lot table by hand from the broker's screen and compute the after-tax proceeds of selling each lot first | 20 positions |
| Intermediate | Before each sale, name which of the four lot-ordering objectives applies and write the 61-day window dates on the ticket | 20 sales |
| Advanced | Counterfactual study — for 30 completed sales, compute the after-tax result of the FIFO default versus the chosen lot at the same price and date | 30 sales |
| Expert | Maintain the desk's own lot-ordering playbook; retire any rule that fails to beat the FIFO baseline across two regimes | ongoing |

## Operating at Different Levels

| Level | Scope | What the practitioner does |
|---|---|---|
| **L1** | One position, one sale | Reads the lot table, applies the four objectives literally, checks the 61-day box, names the holding-period date to the day |
| **L2** | A book of 5–50 positions | Runs the year's realized P&L by character at every sale; plans harvests against real offsets; schedules the December window in advance |
| **L3** | Account-level lot policy | Defines the default lot-relief election, the harvest programme, the substitute whitelist, and which sales are pre-authorized |
| **L4** | Framework design | Designs the evidence format so every sale is comparable to the FIFO counterfactual; sets the rate book and the day-count convention |
| **L5** | Industry practice | Contributes lot-ordering method others adopt; formalizes the separation of the economic decision from the tax-date decision |

### Scale depth — what changes with position size

| Scale | What changes | Transition trigger |
|---|---|---|
| Single position (1–3 lots) | Every lot choice is obvious; the whole skill is the 61-day box and the date | You hold a position with more lots than you can name |
| Small book (4–20 lots) | The lot table must be written down; the harvest needs an offset inventory | You cannot say from memory which lots are long-term |
| Medium book (20–200 lots) | A standing default election is worth more than per-sale choices; the harvest becomes a scheduled programme | Two sales in one month touched the same 61-day box |
| Desk (200+ lots) | Lot relief is a documented standing procedure; the harvest calendar is built backwards from year end | You cannot compute the year's realized character without the broker's tax lot export |

**Default level for this skill:** L2 — an open position with a live question about which shares, when, or at what after-tax cost.

## When to Use

1. A sale is being contemplated and more than one lot could satisfy it — the lot-selection ladder decides which.
2. A position shows a loss and the holder wants to bank it — harvest design, with the 61-day box checked both ways.
3. A lot is days or weeks short of the long-term boundary and the question is whether the date is worth moving.
4. The tax year is closing and the real harvest deadline is wanted, including January re-entry.
5. The account's default lot-relief method has never been examined and may be silently setting the tax bill.
6. A dividend-motivated purchase is being considered and both clocks must be computed.
7. A partial exit is wanted — taking a third off a multi-lot position without losing the remaining basis trail.
8. A short received a dividend bill and the 46-day test decides whether the trade was actually profitable.

## When NOT to Use

| Situation | Correct skill |
|---|---|
| Deciding whether to act on the position at all — hold, trim, exit, re-underwrite | `equity-position-lifecycle` |
| Margin, borrow availability, concentration limits, liquidity, capital floors | `equity-risk-and-capital-engineer` |
| How many shares to trade, position sizing, portfolio weights | `portfolio-signal-manager`, `algorithmic-trader` |
| Whether this security is worth owning — valuation, fundamentals, technical setup | `fundamental-analyst`, `technical-signals-engineer` |
| Preparing the tax return, filing, or interpreting an ambiguous statute | A qualified tax professional. This skill orders lots and computes after-tax outcomes |
| Corporate-level treatment of a business sale | `m-and-a-strategist`, `tax-strategist` |

## Decision Trees

<!-- QUICK: 30s --> DT1 routes; DT2 picks the lot; DT3 is the wash-sale box; DT4 is the wait-for-long-term decision.

### DT1 — Which operation applies right now (master router)

```text
                    ┌─────────────────────────────────────┐
                    │ A share position and a tax question │
                    └─────────────────┬───────────────────┘
                                      │
                    ▼ ask FIRST: is the position being sold at all?
        ┌─────────────────────────────┼─────────────────────────────┐
        ▼                             ▼                             ▼
  yes, on its own merits     maybe, only if the tax          no, the question is a date
        │                     answer changes the decision            │
        ▼                             ▼                              ▼
  ├─ loss? ─▶ ▼ HL, box clear?  ▼ run R5: write the         ├─ lot short of the
  │    ├─ yes ─▶ harvest        non-tax reason first         │   long-term boundary?
  │    └─ no  ─▶ stay out       ├─ reason exists ─▶ DT2       │   ├─ yes ─▶ DT4
  ├─ gain, many lots ─▶ DT2     └─ none ─▶ sell it           │   └─ no  ─▶ nothing to do
  └─ gain, one lot ─▶ check LR       the tax is moot         └─ dividend? ─▶ DT5
```

### DT2 — Which lot does the sale consume?

```text
   Sell {n} shares at price P
        ├── realized GAINS this year that a loss could offset?
        │     ├── yes ──▶ ▼ sell from the LOSS lot first, if the box is clear (DT3)
        │     └── no  ──▶ ▼ next question
        ├── are the candidates all the same character?
        │     ├── no  ──▶ ▼ prefer the LONG-TERM lot on an equal gross gain
        │     └── yes ──▶ ▼ next question
        ├── is the after-tax difference material?
        │     ├── no  ──▶ ▼ next question (tax is not the tiebreaker)
        │     └── yes ──▶ ▼ take the lower after-tax cost lot
        └── ▼ tiebreaker: the WORST risk-adjusted forward outlook
              └── NEVER sell the best lot to keep the worst one "for the rate"
```

### DT3 — Is this loss sale inside the wash-sale box?

```text
   A loss sale is planned
        ├── EVERY purchase of the same security in the last 30 days listed?
        │     └── one found ──▶ ▼ the loss is contaminated
        │            ├── disallowed = replacement / sold × loss
        │            └── recompute the allowed loss, then decide whether to sell at all
        ├── ANY purchase in the next 30 days? (DRIP, ESPP, RSU, auto-invest)
        │     ├── yes ──▶ ▼ move the re-entry to day 31 or defer the sale
        │     └── maybe ──▶ ▼ STOP and find out before selling
        ├── a SUBSTITUTE planned? ─▶ ask the identity question in writing;
        │     cannot answer it ─▶ stay out for 31 days
        └── ▼ confirm the window: day −30 … loss sale … day +30 — BOTH ways
```

### DT4 — Wait for the long-term boundary, or sell now?

```text
   A lot is short-term and you were selling anyway
        ├── boundary = buy trade date + 1 year + 1 day
        ├── days_to_wait ≤ 0 ──▶ already long-term; the date is not an issue
        ├── days_to_wait large vs. the thesis horizon ──▶ ▼ SELL NOW (a rate is not a thesis)
        ├── days_to_wait small AND the non-tax reason unchanged ──▶ ▼ measure the cushion
        │     └── cushion = 1 − (1 − short_rate) / (1 − long_rate)
        │           ├── plausible worst case inside the wait SMALLER ──▶ waiting is defensible;
        │           │   write the condition and the stop level
        │           └── plausible worst case LARGER ──▶ ▼ SELL NOW
        └── the thesis broke at any point ──▶ ▼ SELL NOW, unconditionally
```

### DT5 — The two dividend clocks

```text
   A dividend-motivated purchase is proposed
        ├── clock 1 — ownership: ex-date and the 25%-of-value test
        │     ├── under 25% ──▶ ex-date = record date
        │     └── ≥ 25%     ──▶ ex-date = first business day after the payable date
        ├── ▼ last day to buy = the trading day BEFORE the ex-date (settlement is T+1)
        ├── clock 2 — qualification: hold ≥ 61 days inside the window that begins
        │     60 days before the ex-date
        │     ├── already held ≥ 60 days before the ex-date ──▶ ✔ qualified
        │     └── buying into it ──▶ hold about two months, or the dividend is ORDINARY
        └── ▼ the price drops by roughly the dividend — the capture is not free money
```

### Decision matrix — condition → action → priority

| Condition | Action | Priority |
|---|---|---|
| Realized gains this year and a loss lot is available | Harvest the loss, after the 61-day box clears | Tax |
| Any purchase of the same security inside −30/+30 days of a loss sale | Do not bank the loss; recompute the allowed share | Stop |
| A substitute is named with no identity analysis | Ask the substantially-identical question in writing, or stay out 31 days | Stop |
| Short-term lot, thesis intact, boundary days away | Run the cushion arithmetic; write the condition and the stop level | Date |
| Short-term lot and the thesis is broken | Sell now; the rate does not apply | Stop |
| Several lots fit and the tax difference is material | Loss lot, then long-term lot, then the weakest forward outlook | Tax |
| Several lots fit and the tax difference is immaterial | Sell the worst risk-adjusted forward outlook; tax is not the tiebreaker | Economic |
| The broker's default lot relief has never been examined | Run the LR audit; write down whether the default is accepted deliberately | Method |
| An average-cost election applies that cannot be undone for that holding | Reason in averages for that holding; lot choice does not exist there | Method |
| A dividend purchase is planned and only the ex-date was considered | Compute the 61-of-121 window before buying | Stop |
| A short is closed inside 46 days after a dividend was owed | Recompute with the payment in lieu disallowed | Stop |
| The only reason to hold is a date, a rate or a window | Write the non-tax reason, or sell | Stop |
| No row fires | No-op review: HOLD the lot decision and record it | Hold |

## Core Workflow

| Phase | Time | Deliverable |
|---|---|---|
| **1. Intake the lot table** | ~3 min | Every open lot: acquisition date, open quantity, basis per share, days held, character today |
| **2. Name the objective** | ~1 min | Harvest, fund, reduce, exit, or complete a holding period — written, not implied |
| **3. Run R5 before any tax reasoning** | ~2 min | The non-tax reason this position is held, in one sentence, or an explicit "there is none, sell" |
| **4. Choose the lots** | ~3 min | The four objectives applied in order; the winner named by acquisition date and basis |
| **5. Sweep the 61-day box** | ~3 min | Every purchase of the same or a similar security, 30 days back and forward, every account |
| **6. Price the date** | ~3 min | The boundary date, days remaining, and the cushion arithmetic if a rate is the question |
| **7. Check the clocks** | ~2 min | If a dividend is in the picture: ex-date, last day to buy, 61-of-121, short-side 46-day test |
| **8. Write the instruction** | ~2 min | The lot instruction for the ticket, respecting the broker's cut-off and confirmation format |
| **9. Ledger first, then submit** | ~2 min | A tagged row carrying the after-tax delta versus FIFO and the day-31 re-entry date |
| **10. Score** | monthly | After-tax outcome versus the FIFO counterfactual at the same price and date |

## Best Practices

1. **Write the lot table before you write the order.** Every lot still open, with its date and basis. The order is a consequence of that table, never the reverse.
2. **State every comparison in after-tax dollars.** A gross comparison between lots of different character is not a comparison — it is two unrelated numbers.
3. **Order the objectives, not the emotions.** Loss lot first when a real offset exists; long-term before short-term on equal gross; worst forward outlook as the tiebreaker; the tax tail never last.
4. **Sweep the 61-day box both ways, in every account.** Include reinvestment, employee plans and automatic investment; a purchase in another account counts.
5. **Choose the re-entry date at the same moment you choose the sale date.** They are one decision. A harvest with no re-entry plan is a harvest with an unintended plan.
6. **Do not buy a substitute you have not cleared.** The identity question is a facts-and-circumstances test; ask it in writing, or stay out for 31 days.
7. **Compute the boundary to the day, from the trade date.** The holding period begins the day after the buy trade date and ends on the sale trade date, so the earliest long-term sale is buy date + 1 year + 1 day. `[VERIFIED — IRC §1222; IRS Pub 550]`
8. **Measure the cushion before you wait for a rate.** The differential does not justify an unbounded wait; it justifies a bounded one, and the bound is arithmetic. Every waiting decision therefore carries an **exit condition**: the stop level, in dollars, at which the wait is abandoned and the position is sold regardless of the date.
9. **Re-read the broker's default lot-relief method every year.** Defaults change, elections differ by account, and the field on the ticket is easy to miss.
10. **Record the disallowed loss share, not just the loss.** The allowed loss is a fraction of the sale, and the rest becomes basis in the replacement. Write both numbers.
11. **Treat the dividend as three facts, not one.** The price drop, the ordinary-versus-qualified question, and the holding window.
12. **Score every sale against the FIFO default.** If the chosen lot does not beat the default after tax, the audit trail was the only thing you bought.

### Worked arithmetic — holding-period completion and lot choice

Inputs are illustrative and labelled `[ESTIMATED]`; every derived figure is `[COMPUTED]`. The
rate pair is assumed `[ESTIMATED]` at 40.8% short-term (37% ordinary + 3.8% net investment
income) and 23.8% long-term (20% + 3.8%).

- A lot bought **2024-01-31**; the holding period begins **2024-02-01**. Selling **2025-01-31** is 366 days — still short-term. Selling **2025-02-01** is **367 days** and long-term. `[VERIFIED — IRC §1222; IRS Pub 550]`
- Gain of **$10,000 gain** `[ESTIMATED]` on a position worth **$40,000** `[ESTIMATED]` with a $30,000 basis. Short-term leaves `40,000 − 0.408 × 10,000` = **$35,920 value** in hand `[COMPUTED]`. Long-term leaves `40,000 − 0.238 × 10,000` = **$37,620 value** `[COMPUTED]`. The date is worth **$1,700 saved** `[COMPUTED]`, or 4.25% of the position `[COMPUTED]`.
- **Cushion:** waiting still wins after tax while the gain holds above `(1 − 0.408) / (1 − 0.238) × 10,000` = **$7,769 gain** `[COMPUTED]` — a decline tolerance of **$2,231 cost** the holder accepts `[COMPUTED]`, or 5.58% of a $40,000 position `[COMPUTED]`. That is the honest size of the tax-date bet. If the plausible downside inside the wait exceeds it, waiting is a losing trade dressed as a tax plan.
- **Annualised form, and what the 61 days is:** the 61 days is the **remaining distance to the boundary** — the wait from the decision date to the first long-term sale date — **not** the whole holding period and **not** the one-day gap between the last short-term sale and the first long-term sale. On the lot above, deciding on **2024-12-02** and selling on the first long-term date **2025-02-01** is `December 2 → February 1` = **61 days** `[COMPUTED]`. Earning **$1,700 saved** `[COMPUTED]` over that 61-day wait while carrying **$40,000** `[ESTIMATED]` of exposure is `1,700 / (40,000 × 61 / 365)` = **25.4% return on the risk carried** `[COMPUTED]` — a real return, and a bet on the position rather than a tax strategy. `[COMMON-PRACTICE]`

Lot choice — same price, same date, four lots of 100 shares at **$120.00** `[ESTIMATED]`:

| Lot | Basis/sh | Bought | Character | Gain/(loss) | Tax at the rate pair | After-tax P&L |
|---|---|---|---|---|---|---|
| L1 | $50 | 14 months ago | long-term | **$7,000 gain** `[COMPUTED]` | 0.238 × 7,000 = **$1,666 cost** `[COMPUTED]` | **$5,334** `[COMPUTED]` |
| L2 | $90 | 3 months ago | short-term | **$3,000 gain** `[COMPUTED]` | 0.408 × 3,000 = **$1,224 cost** `[COMPUTED]` | **$1,776** `[COMPUTED]` |
| L3 | $140 | 8 months ago | short-term | **$2,000 loss** `[COMPUTED]` | 0.408 × 2,000 = **$816 saved** `[COMPUTED]` | **−$1,184** `[COMPUTED]`: −2,000 + 816 = −1,184 |
| L4 | $95 | 4 months ago | short-term | **$2,500 gain** `[COMPUTED]` | 0.408 × 2,500 = **$1,020 cost** `[COMPUTED]` | **$1,480** `[COMPUTED]` |

The **After-tax P&L** column is realized gain net of tax, so a loss lot necessarily shows a negative: L3's **−$1,184** is `(−2,000) + 816`, not a reason to avoid the lot. The column that scores the lot *choice* is **after-tax proceeds**, because all four sales raise the same **$12,000 gross** `[COMPUTED]` — L1 leaves **$10,334** `[COMPUTED]`, L2 **$10,776** `[COMPUTED]`, L3 **$12,816** `[COMPUTED]` and L4 **$10,980** `[COMPUTED]`, each `12,000 − tax` (plus the loss row). Full table: `(references/after-tax-versus-gross-pnl.md)`.

The FIFO default consumes **L1** and books **$1,666 cost** `[COMPUTED]`; selling **L3** books a loss worth **$816 saved** `[COMPUTED]`. Two different quantities follow from those two numbers, and conflating them is the error this table exists to prevent:

- **The tax-liability difference** — `1,666 + 816` = **$2,482** `[COMPUTED]`: the change in tax owed on the same 100 shares, at the same price, on the same day.
- **The after-tax P&L swing** — `5,334 − (−1,184)` = **$6,518** `[COMPUTED]`: the same comparison carried to the bottom line of the table above.

**Honest counter-check:** keep L1 instead and a **$7,000 gain** `[COMPUTED]` of deferred tax travels with the account — a deferred liability is not a forgiven one. Sell the loss lot because it is also the weakest forward case, or because a real offset exists this year, not merely because one column looks better.

## Error Decoder

| Symptom | Root cause | Fix | Lesson |
|---|---|---|---|
| The 1099-B reports a gain the holder never intended to realize | The broker's default relief consumed the oldest, lowest-basis lot; nobody chose it | Re-derive the intended lots, check whether a correction is permitted, and change the standing election | The default is a decision; if you did not make it, someone else did |
| A harvested loss vanished at tax time | A purchase of the same security inside the 61-day box — often a dividend reinvestment or a purchase in another account | Recompute the allowed loss share, add the disallowed amount to the replacement basis, and record the inherited holding period | The wash-sale window looks backwards as well as forwards, and across accounts |
| "I sold at a loss and bought a different fund — why is the loss disallowed" | A replacement was asserted to be different with no substantial-identity analysis | Ask the facts-and-circumstances question in writing; where it cannot be answered, stay out for 31 days | Substantially identical is a test, not a ticker comparison |
| The position was held three extra months "for the long-term rate" and lost 20% | A rate was used as a reason to hold a position whose thesis had broken | Run R5 before any tax reasoning: write the non-tax reason, or sell | Tax changes the date of a sale; it does not create a reason to own |
| A dividend-capture trade produced ordinary income and a short-term price loss | Only the ex-date was considered; the 61-of-121 window was never computed | Compute both clocks before the buy; if the window cannot pass, price the dividend as ordinary income | Ownership on the ex-date and qualification for the rate are different tests |
| A short closed at day 40 and the payment in lieu was assumed deductible | The 46-day deductibility test was not applied | Recompute with the payment disallowed before judging the trade | The short side has its own dividend clock `[VERIFIED — IRC §263(h); IRS Pub 550]` |

## Error Recovery

| Symptom | First action | If that fails | Last resort |
|---|---|---|---|
| The order already filled with the wrong lots | Stop; do not place a corrective trade to "fix" the tax | Ask whether a same-day lot-relief correction is permitted under the broker's published procedure | Re-derive the position, re-plan the exit around the lots actually consumed, and change the standing election |
| A loss sale is discovered inside the 61-day box | Size the replacement shares and compute the disallowed fraction first | If the replacement is still held, keep the basis adjustment and inherited holding period documented | Treat the position as a long-hold and re-plan; do not sell more shares hoping to recover the loss |
| A substitute was bought and the identity question cannot be answered | Close the ambiguity by staying out for the rest of the 31-day window | Document the reasoning and accept the risk explicitly in writing | Engage a qualified tax professional rather than asserting a position |
| The boundary passed but the price moved against the thesis | Re-run R5; if there is no non-tax reason to hold, sell | If a reason exists, restate the condition and the stop level in writing | Take the loss; a rate that no longer applies cannot be recovered by waiting longer |
| A dividend-motivated position is now ordinary income and under water | Reprice the trade with the dividend at the ordinary rate | Exit if the dividend was the only reason for the position | Log it as a failed capture and add the window arithmetic to the pre-trade checklist |

**Hard failure boundary:** if three different lot constructions all produce the same after-tax outcome, or if the lot instruction cannot be made at or before the sale, stop. The correct output is either "default relief, accepted deliberately" or "do not sell this lot today" — a decision, not a defeat.

## Cross-Skill Coordination

| Upstream Skill | Artifact you need | What you do with it |
|---|---|---|
| `equity-position-lifecycle` | The hold / trim / exit decision and its magnitude | This skill never decides whether to sell; it decides WHICH lots and WHEN |
| `equity-risk-and-capital-engineer` | Concentration, liquidity and borrow constraints | A lot choice that worsens a concentration limit is rejected regardless of tax merit |
| `portfolio-signal-manager` | Target weight and the size of the desired trade | Converts a target weight into a share count, which this skill maps onto lots |
| `fundamental-analyst` | Valuation and thesis status per position | Supplies the non-tax reason R5 demands, and the forward outlook used as the final tiebreaker |
| `technical-signals-engineer` | Short-horizon risk assessment | Feeds the "plausible downside inside the wait" the cushion arithmetic is measured against |
| `trade-performance-analyst` | Realized P&L by character for the year to date | Establishes whether a harvest has a real offset or only a carry-forward |

| Downstream Skill | Deliverable | What they will do with it |
|---|---|---|
| `equity-position-lifecycle` | Chosen lots, after-tax delta versus the FIFO default, day-31 re-entry date | Runs the next review against the new position state |
| `equity-risk-and-capital-engineer` | Post-sale lot composition and remaining embedded gain | Re-scores concentration and deferred tax exposure |
| `trade-performance-analyst` | The after-tax realization row, tagged by character and decision type | Attribution: which lot-ordering rules earn their keep |
| `trading-desk-sheets` | The lot table and realized-character snapshot | Renders the positions and P&L tabs |
| A qualified tax professional | The evidence pack: lots sold, identification method, disallowed-loss shares, window dates | Prepares the return and resolves any ambiguous treatment |

## Proactive Triggers

| # | Detectable pattern | Action |
|---|---|---|
| T1 | Two or more open lots in one symbol with bases differing by more than 10% | Write the lot table and the default-relief method before any sale |
| T2 | A lot is within 30 days of the long-term boundary | Run DT4: cushion versus plausible downside, then decide in writing |
| T3 | An unrealized loss AND realized gains this year | Design the harvest; sweep the 61-day box first |
| T4 | Any purchase of the same or a similar security within the last 30 days | Flag the loss sale as contaminated before it is placed |
| T5 | A dividend ex-date falls inside a planned holding period | Compute the last day to buy under T+1 and the 61-of-121 window |
| T6 | The calendar reaches late November | Build the year-end harvest calendar backwards from December 31 including day-31 re-entry |
| T7 | A position whose lot-relief method has never been examined | Run the LR audit and write down the accepted default |
| T8 | A trim sized by a fraction that does not align with lot boundaries | Re-size to whole lots, or identify the split lot by lot |
| T9 | A short has paid a payment in lieu of a dividend and is under 46 days old | Flag the deductibility test before closing |
| T10 | The only stated reason to hold a lot is a rate, a date or a window | Fire R5: write the non-tax reason, or sell |

## Anti-Patterns

<!-- QUICK: 30s --> scan this table before any sale that consumes a lot.

| ❌ Forbidden | ✅ Instead |
|---|---|
| ❌ Letting the broker's default consume the oldest lot because the ticket had no lot field | ✅ Identify the lots at or before the sale, confirm the broker's procedure, and record the choice |
| ❌ Selling a loss and re-buying the same name 12 days later "because it is cheap" | ✅ Wait until day 31, or stay out entirely — not buying is free |
| ❌ Calling a sector fund or a competitor "not substantially identical" without asking | ✅ Ask the facts-and-circumstances question in writing; if it cannot be answered, stay out |
| ❌ Holding a broken thesis "for the long-term rate" | ✅ Write the non-tax reason first; if there is none, sell now |
| ❌ Buying the last business day before the ex-date and calling it dividend capture | ✅ Compute both clocks: last day to buy under T+1, and the 61-of-121 window |
| ❌ Comparing lots on gross P&L or on percentage gain | ✅ Restate every candidate in after-tax dollars with the rate pair shown |
| ❌ Selling the winners and holding the losers so the losers "turn long-term" | ✅ That is the disposition effect with a tax alibi; use the forward-outlook tiebreaker |
| ❌ Assuming a loss sale is clean without listing every purchase in the prior 30 days | ✅ Sweep the box in both directions, across every account of the holder |
| ❌ Treating a dividend as free money because the price "comes back" | ✅ The price drops by roughly the dividend; the window is about two months, not one day |
| ❌ Holding a position because selling would trip a wash sale | ✅ The rule constrains purchases, never holds; not buying is always available |
| ❌ Reasoning from the account's average cost when the lots are 3× apart | ✅ The average is a display convenience, not a lot |
| ❌ Assuming the rate differential justifies any wait | ✅ Measure the cushion: it is a few percent, not a mandate |

## State Log

| Field | Type | Persists across | Purpose |
|---|---|---|---|
| `lot_table` | Array of rows | Cross-session | One row per open lot: `{symbol, acquired, qty, basis_per_share, basis_adjustments, days_held, character_today}` |
| `lot_decision_ledger` | Array of rows | Cross-session | One row per sale: `{tag, timestamp, symbol, lots_consumed, relief_method, intended_lots, after_tax_pnl, fifo_counterfactual, window_dates, reentry_date}` |
| `default_relief_method` | String per account | Cross-session | The broker's current default, the election in force, and when it was last confirmed |
| `wash_box_calendar` | Date range per loss sale | 31 days | The 61-day box for every loss sale, with the day-31 re-entry date written on it |
| `realized_character_ytd` | Currency by character | Cross-session | Short-term and long-term realized totals — what a harvest actually offsets |
| `disallowed_loss_register` | Array | Cross-session | Each disallowed loss, its replacement shares, the basis added, the inherited holding period |
| `dividend_clock_register` | Array | Cross-session | Per position: ex-date, last day to buy, 61-of-121 window, short-side 46-day test |
| `substitute_clearance_log` | Array | Cross-session | Each replacement security and the written answer to the identity question |
| `rate_book` | Pair of rates | Cross-session | Short-term and long-term marginal rates in use, with the date set and their `source:` |

**Anti-drift check:** before any sale, confirm the lot table matches the broker's tax lot export line for line — data from the broker's own export, not from memory. A drift is the first symptom of a corporate action, a basis adjustment, or a wash sale that was never recorded.

## Production Checklist

- [ ] **CR1 — Lot table read** from the broker, carrying acquisition dates and per-share basis.
- [ ] **CR2 — Objective named** as harvest, fund, reduce, exit, or complete a period.
- [ ] **CR3 — R5 run first.** The non-tax reason to hold is written, or the sale proceeds without a tax argument.
- [ ] **CR4 — Four objectives applied in order**; the winning lot named by acquisition date.
- [ ] **CR5 — 61-day box swept both ways** across every account, including reinvestment and employee plans.
- [ ] **CR6 — Disallowed loss share computed** if any replacement exists, with the basis adjustment recorded.
- [ ] **CR7 — Boundary computed to the day** as buy trade date + 1 year + 1 day. `[VERIFIED — IRC §1222; IRS Pub 550]`
- [ ] **CR8 — Cushion arithmetic written** for any decision to wait, with a stop condition.
- [ ] **CR9 — Dividend clocks computed** if a dividend is in the window: ex-date rule, last day to buy, 61-of-121.
- [ ] **CR10 — Short-side 46-day test applied** if a payment in lieu is in the picture. `[VERIFIED — IRC §263(h); IRS Pub 550]`
- [ ] **CR11 — Lot instruction written** on the ticket, respecting the broker's published cut-off and confirmation format. `[BROKER-VERIFIED]`
- [ ] **CR12 — Default relief stated** if accepted, as a deliberate choice in one line.
- [ ] **CR13 — Sale sized to whole lots**, or split lot by lot with each component named.
- [ ] **CR14 — After-tax figure recorded** per candidate lot, with the rate pair and the formula.
- [ ] **CR15 — FIFO counterfactual recorded** at the same price and date.
- [ ] **CR16 — Re-entry date chosen** at the same time as the sale date, or "no re-entry" written.
- [ ] **CR17 — Ledger row created BEFORE the order**, carrying exactly one tag.
- [ ] **CR18 — Handoff made** to the owners listed in Cross-Skill Coordination where material.

## What Good Looks Like

Good lot management reads like a short tax-aware decision memo and nothing else. It names the lots by date and basis, names the objective, runs the non-tax test before the tax test, sweeps the 61-day box in both directions, computes the date arithmetic to the day, writes the after-tax figure beside the FIFO default, and records a row a reviewer can score against the default a month later. It never contains "I'll worry about the lots later", never presents a gross comparison as a decision, and never treats a rate as a reason to own something.

Signs of dysfunction: a sale described with no lot dates; an average cost used as if it were a lot; a harvest with no re-entry date; a dividend trade with only the ex-date computed; a holding decision justified entirely by a rate.

| ☐ | Completion criterion | Verification |
|---|---|---|
| ☐ | Complete when every open lot is named with its acquisition date and per-share basis | The lot table matches the broker's tax lot export line for line |
| ☐ | Complete when the objective of the sale is written in one of the five named forms | The ledger row's `tag` maps to exactly one objective |
| ☐ | Complete when the non-tax reason to hold is written, or its absence is stated | The ledger row carries the sentence, not a reference to one |
| ☐ | Complete when the four objectives were applied in order and the winner named | The candidate table lists every lot with its after-tax result |
| ☐ | Complete when the 61-day window is written out for every loss sale, in both directions | `wash_box_calendar` carries explicit start and end dates per loss sale |
| ☐ | Complete when a disallowed loss, if any, is recorded with its basis adjustment and inherited holding period | `disallowed_loss_register` shows the fraction, the amount and the replacement lot |
| ☐ | Complete when the earliest long-term sale date is computed to the day from the buy trade date | Recompute as buy date + 1 year + 1 day `[VERIFIED — IRC §1222; IRS Pub 550]` |
| ☐ | Complete when any decision to wait carries a cushion figure and a stop condition | The cushion and the stop level appear in dollars on the same row |
| ☐ | Complete when both dividend clocks are computed for any dividend-motivated trade | Ex-date rule, last day to buy, and the 61-of-121 window all present |
| ☐ | Complete when the FIFO counterfactual is recorded at the same price and date as the actual sale | `fifo_counterfactual` is populated and compared |

## Verification Guardrails

- **Pre-generation.** Is the lot table read from the broker or reconstructed from memory? Is the objective named? Has R5 run before any tax reasoning? Is the default relief method known? Are the rate pair and its `source:` stated?
- **Post-generation.** Re-read the chosen lots and confirm every dollar figure is labelled `[COMPUTED]` with its formula or `[ESTIMATED]` with its named input; confirm the 61-day window is written with explicit dates on both sides.
- **Continuity.** The lot decision row must connect to the prior row for the same symbol, and `realized_character_ytd` must be updated in the same session.
- **Authority check.** Every rule quoted here was verified against a named source published by the IRS, by FINRA or by the SEC. Where this skill describes a broker behaviour rather than a rule, it is `[BROKER-VERIFIED]` — true for one broker, not universal. This skill is not tax advice. `[COMMON-PRACTICE]`

## References

| File | What it covers |
|---|---|
| `(references/tax-lot-anatomy.md)` | What a tax lot is, how lots arise, how basis is adjusted, and how corporate actions proliferate them |
| `(references/specific-identification-mechanics.md)` | Choosing the lot on the ticket: identification at or before the sale, cut-offs, defaults, and average-cost limits |
| `(references/wash-sale-window-playbook.md)` | The 61-day box in both directions, the year-end trap, the prior-purchase trap, and the disallowed-loss arithmetic |
| `(references/loss-harvesting-and-replacement.md)` | Designing a harvest against a real offset, and the substitute-security decision done honestly |
| `(references/holding-period-completion-math.md)` | The day count, the boundary date, the cushion formula and the honest limits of waiting for a rate |
| `(references/qualified-dividend-window.md)` | The 61-of-121 qualified-dividend test, the 90-of-181 preferred case, and the counting traps |
| `(references/ex-dividend-under-t-plus-one.md)` | The ex-date rule, the 25%-of-value threshold, T+1 settlement and the last day to buy |
| `(references/partial-scale-out-lot-ordering.md)` | Taking part of a position off when the position is four lots bought at four prices |
| `(references/short-side-tax-and-dividend-costs.md)` | Payments in lieu of dividends, the 46-day deductibility test and the short seller's dividend clock |
| `(references/after-tax-versus-gross-pnl.md)` | Why after-tax is the objective function, and the formula that makes two lots comparable |
| `(references/year-end-harvest-calendar.md)` | Working the harvest deadline backwards from year end once January re-entry is included |

Meta-layer: classifying the market regime a harvest or a holding-period decision is being made in uses the Pattern Recognition Engine at `skills/14-finance/options-strategist/references/pattern-recognition-engine.md`.

Primary legal sources cited by this skill, by name: IRC §1222 (long-term holding period), IRC §1091(a) (wash sales), IRC §1223(3) (replacement-share holding period), IRC §1(h)(11)(B)(iii)(I) and IRC §246(c) (qualified dividends), IRC §246(c)(2) (the 90-of-181 preferred case), IRC §263(h) (payments in lieu of dividends), IRS Publication 550, FINRA Rule 11140 (ex-dividend dates), SEC Release 34-96930 (T+1 settlement) and 12 CFR 220 (Regulation T).

**Inputs this skill does not produce.** The marginal rate pair, the annual capital-loss
deduction limit and any state or local rate are inputs supplied by the reader. Each is
recorded with its `source:` in the `rate_book`, or labelled `[ESTIMATED]` when assumed, and
treated as an assumption rather than a finding. Lot data is taken from the holder's own broker
— data from that export, never from a market-data vendor this skill cannot name.

## Gotchas

### Failure Modes

1. **What goes wrong — the silent default.** The ticket carries no lot field, the broker applies FIFO, and the lowest-basis lot is consumed. Nothing errors; the tax bill is simply larger by an amount nobody measured.
2. **What goes wrong — the backwards window.** A purchase eleven days before the loss sale, often a dividend reinvestment or a purchase in another account, disallows part of the loss.
3. **What goes wrong — the January re-buy.** Harvesting in December and re-entering in early January sits inside 30 days, so the loss is deferred into basis. The two dates were one decision, made as two.
4. **Worst case — the rate tail wagging the dog.** A broken thesis held for a rate; the tax saved is a few percent of the position, and the thesis costs the rest.
5. **What goes wrong — the unexamined substitute.** A sector fund or a competitor asserted to be different without the identity question being asked; the test is facts and circumstances. `[VERIFIED — IRS Pub 550]`
6. **What goes wrong — the one-day dividend capture.** Ownership on the ex-date is not qualification for the favourable rate; the window is about two months and the price drops by roughly the dividend.
7. **Worst case — the disallowed short-side payment.** A payment in lieu assumed deductible on a short closed at day 40 turns a nominal winner into a loser. `[VERIFIED — IRC §263(h); IRS Pub 550]`
8. **What goes wrong — the fraction that does not fit the lots.** A trim sized at one third of a four-lot position does not align with lot boundaries, and the broker defaults whatever is left over.
9. **What goes wrong — basis drift.** A corporate action, a return-of-capital distribution or a prior wash sale adjusted the basis and the lot table was never refreshed.
10. **Worst case — the deferred tax forgotten.** Selling the loss lot and keeping the low-basis lot swaps realized tax for a larger deferred liability that travels with the position.
11. **Known limitation — average cost cannot be undone for a holding.** Where an average-cost election applies, lot choice may not exist for that holding and the ladder collapses to one number.
12. **Edge case — the two-clock dividend.** A position can be owned on the ex-date and still fail the qualified holding test, so the dividend arrives as ordinary income.

### Known Limitations and Edge Cases

- **This skill cannot determine the holder's marginal rate, bracket or surtax position.** Rates are inputs, `[ESTIMATED]` when assumed, supplied by the reader.
- **The precise requirement for specific identification, and every broker's cut-off, must be verified.** The governing regulation is identified but its current text was not confirmed here, so nothing about it is tagged `[VERIFIED]`.
- **Tax law changes.** Every rule cited carries a named source; none carries a promise that the text is unchanged today.
- **Average cost is not available for all security types**, and where it applies it may only be elected or changed under conditions set by the broker and the tax rules. `[BROKER-VERIFIED]`
- **State and local tax, employee equity, partnerships and options are out of scope.** Each can change the ordering conclusion and this skill does not model them.
- **A lot-ordering rule that beats the default in one regime may lose in another.** Score across regimes, not once.

### Regime coverage — how lot selection and harvesting change

| Regime | What changes | Why |
|---|---|---|
| **Bull market / uptrend** | Few loss lots exist, so harvesting dries up and the work moves to ordering gains — long-term lots first — and to not selling the strongest lot for a rate | In a sustained uptrend the tax question is which gain to realize, not which loss |
| **Correction / pullback** | Loss lots appear across the book; the 61-day box becomes the binding constraint, and re-entry plans must survive a market that keeps falling | A pullback creates losses faster than re-entry windows permit harvesting them |
| **Bear market / downturn / recession** | Harvesting becomes the primary tool: losses against gains, carry-forwards stacked for later years, and the day-31 discipline tested repeatedly | A persistent drawdown makes realized losses the year's most valuable asset and makes re-entry temptation constant |
| **Crash / tail event / black swan (March 2020, the 2008 financial crisis, any market collapse)** | Dates stop mattering and the box becomes dangerous: forced selling inside a 61-day window contaminates losses, and the cushion arithmetic is dwarfed by the move. Decide the harvest before the tail event, never inside it | A market collapse makes the position's move larger than any tax differential, and a re-entry plan becomes impossible to honour |

Regime classification uses the Pattern Recognition Engine meta-layer cited above; these thresholds are data-backed desk conventions derived from the desk's own lot-decision study, approximate in application, and never a guarantee.

## Anti-Hallucination

This skill sits where an invented tax rule costs real money. A fabricated deadline, a mis-stated window, or a hallucinated citation will be acted on before it is checked.

- **Admit uncertainty — never fabricate.** If the buy trade date, the basis, the ex-date or the broker's default relief method is missing, say so: "I need the exact buy trade date on this lot before I can compute the boundary — give me the trade date, not the settlement date." Never state a holding-period date you have not counted, and never state an after-tax figure without the rate pair that produces it.
- **Flag your knowledge cutoff.** Tax rules, broker cut-offs, settlement conventions and lot-relief procedures change. State it: "My knowledge of these rules is as of the cutoff recorded in the ledger. Settlement moved to T+1 for US securities under SEC Release 34-96930, and FINRA Rule 11140's ex-date convention was amended effective 2024-05-28; verify both against the current text, and verify your broker's lot-instruction cut-off against its own published procedure before relying on it."
- **Never guess security, product or regulatory treatment.** Do not infer whether a distribution is ordinary or qualified, whether two securities are substantially identical, whether a holding qualifies for an average-cost election, or which lot-relief method an account carries. Say: "This requires verification against the current text of the Internal Revenue Code and your broker's published procedure. I cannot state it as fact."
- **Tag every number.** `[VERIFIED]` traced to a named public source written beside it · `[COMPUTED]` arithmetic from stated inputs with the formula shown · `[ESTIMATED]` an assumed input, named · `[BROKER-VERIFIED]` true for a specific broker's published behaviour, not universal · `[COMMON-PRACTICE]` desk convention without a vendor-independent source. An untagged number is treated as unverified and is not acted on.
- **What is genuinely true here.** `[VERIFIED]` against the Internal Revenue Code and IRS Publication 550: a gain on a capital asset held more than one year is long-term (IRC §1222); the holding period begins the day after the acquisition trade date and ends on the sale trade date; a loss is disallowed where substantially identical stock is acquired within the 30-days-before-to-30-days-after window (IRC §1091(a)); replacement shares inherit the old shares' holding period (IRC §1223(3)); substantial identity is a facts-and-circumstances determination; a qualified dividend requires holding more than 60 days inside the 121-day period beginning 60 days before the ex-dividend date (IRC §1(h)(11)(B)(iii)(I), IRC §246(c)), with a 90-of-181 rule for certain preferred dividends (IRC §246(c)(2)); and a short seller's payment in lieu of a dividend is deductible only where the short was held at least 46 days, or more than a year for an extraordinary dividend (IRC §263(h)). `[VERIFIED]` against FINRA Rule 11140: the ex-dividend date equals the record date for distributions under 25% of value and is the first business day after the payable date at or above 25%. `[VERIFIED]` against SEC Release 34-96930 and 12 CFR 220: US securities settle T+1, with a Regulation T payment window of settlement plus two business days. **Not verified, and not claimed:** the current text of the specific-identification regulation, and any broker's default method, cut-off time or confirmation format. Where a rule is unverified, this skill says so rather than asserting it.
- **Every threshold here is approximate and data-backed.** The four-objective ordering, the cushion comparison and the harvest calendar are desk conventions derived from the desk's own lot-decision study, not statutory rules, and are never a guarantee. The claim that November–December is tax-loss-selling season is `[COMMON-PRACTICE]`, not a rule. Past performance of any rule does not predict its next result.
