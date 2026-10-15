# Trigger Precedence: What Wins When the Clocks Disagree

The four equity clocks are described in `equity-time-axes-cadence.md`. This file is about the collisions: an earnings date three days away, an anniversary twenty days away, a margin call this morning, and a level that broke on Friday's close. Four clocks, four different answers, one position.

**The precedence order is the whole content of this file.** It is fixed, it is resolved top-down, and it stops at the first rung that fires.

## The precedence order

| Rung | Wins | Because |
|---|---|---|
| 1 | **Risk / forced action** | The firm acts on its own timetable, and need give no advance notice [VERIFIED — 12 CFR 220.4(d)]. The decision is already made; only the executor is undecided |
| 2 | **Breached invalidation level** | The level is the position. Everything else is about the position's price, tax or timing |
| 3 | **Event clock** | It wins the *decision date*, not the outcome: the decision must be written before the boundary |
| 4 | **Tax clock** | It wins only over a **discretionary plan action**, and only by changing *when* a sale you were already making happens |
| 5 | **Plan rung** | The default when nothing above fires: at rung → TRIM; below rung → HOLD to the written date |

Two rules make this table usable:

- **Tax never justifies a worse economic position.** It changes *when* you sell a position you were selling anyway; it never turns a sell into a hold.
- **A higher rung does not delete a lower one.** The lower clock is recorded as a queued entry, so a later review can see what it wanted.

## Rung 1 — Risk and forced action

Fires on any of:

- A margin call outstanding. Above a $1,000 deficiency the firm must liquidate [VERIFIED — 12 CFR 220.4(d)], and the Reg T payment window is the standard settlement cycle plus two business days, which under T+1 is three business days [VERIFIED — 12 CFR 220.2, 220.4(c)(3)(i)].
- A borrow recall on a short position.
- An intraday (day-trading) margin restriction: the former "pattern day trader" designation — four or more day trades in five business days and a $25,000 minimum equity `[VERIFIED]` — was **superseded effective 2026-06-04** by FINRA Regulatory Notice 26-10 (SEC-approved 2026-04-14/15, phased in to 2027-10-20), and intraday margin is now set under FINRA Rule 4210(d)(2) [VERIFIED — FINRA Regulatory Notice 26-10; FINRA Rule 4210(d)(2)]. Verify the current requirement with the broker, because many pages still publish the old test.
- A halt, a delisting notice, or a desk circuit breaker.

**What it does:** authorises CLOSE or reduce only. It does not authorise a hedge, an add, a rotation, or an average down. It also does not consult the tax calendar — a forced liquidation happens on the firm's clock, and the holder's opinion about a rate difference is not an input.

## Rung 2 — The breached level

A close beyond the written invalidation level, or a thesis whose reason has been withdrawn.

**What it does:** authorises CUT, or CLOSE if there is no reason to own the name at all.

**What it does not do:** it does not negotiate. Specifically, three arguments that do not survive this rung:

1. *"It's only down on paper."* The mark is today's exit price.
2. *"It's cheaper now — I'll add."* That is rung 7, and rung 7 sits below this one. A breached level disqualifies the average-down gate at clause 1.
3. *"I'll wait for the long-term rate."* The tax clock is rung 4 and this is rung 2.

## Rung 3 — The event clock

Fires when earnings, an ex-dividend date or an index reconstitution is inside 5 business days — or, at the softer PREPARE rung, inside 10.

**What it does:** wins the *decision date*. The pre-event action for both outcomes is written before the boundary and executed at or before it. It does not dictate **which** action; it dictates **when the choice has to exist**.

**Why this is not merely procedural:** an event is a discontinuous repricing. After it, the information that would have made the decision obvious is free to everyone, and the price has already moved. A decision made after the gap is a decision made by the gap.

## Rung 4 — The tax clock

Fires when a tax date is in reach:

- The long-term anniversary inside 5 sessions. Remember the arithmetic: the holding period begins the day after the buy trade date and ends on the sale trade date, so the earliest long-term sale is buy date + 1 year + 1 day [VERIFIED — IRC §1222, IRS Pub 550].
- A wash-sale window open: 30 days before through 30 days after the loss sale, with replacement shares inheriting the old holding period [VERIFIED — IRC §1091, §1223(3)].
- A qualified-dividend window open and unmet: 61 days inside the 121-day period beginning 60 days before the ex-date [VERIFIED — IRC §1(h)(11), §246(c)].

**What it does:** re-times a **discretionary** action. If the disposition is TRIM or CLOSE and the economics do not care about a fortnight, the tax clock may move the execution inside the window, or outside it, or to just after an anniversary.

**What it never does:** it never creates a hold, never overrides rung 2, never overrides rung 1, and never converts a losing position into a plan.

## Rung 5 — The plan rung

The default. At a rung → TRIM on the ladder. Below a rung, inside band, level intact → HOLD to the written date at the written level. Nothing else in this table is a reason to act, which is the point: most reviews should end here.

## Worked conflicts

**Conflict A — the tax clock against the level.**

A position is 20 sessions short of the anniversary. The level breaks on Friday's close. The holder wants to wait 20 sessions for the long-term rate.

Resolution: rung 2 beats rung 4. CUT. And the arithmetic agrees, which is worth showing:

- The gain at stake: $3,000 [COMPUTED]: 500 sh × ($66.00 − $60.00) = 500 × $6.00 = 3,000.
- Short-term at 40.8% versus long-term at 23.8%: **$510** of rate difference [COMPUTED]: 3,000 × (0.408 − 0.238) = 510. The 40.8% / 23.8% pair is an assumption the reader substitutes [ESTIMATED]; the statutory rates behind it are [VERIFIED] — IRC §1(h) and §1411.
- The risk of the wait: a $33,000 position [COMPUTED]: 500 × 66.00 = 33,000; at 30% annualized volatility, one sigma over 20 sessions is **$2,789** [COMPUTED]: (33,000 × 0.30 ÷ √252) × √20 = 623.7 × 4.472 = 2,789.
- The tax saving is **18%** of one standard deviation [COMPUTED]: 510 ÷ 2,789 = 18.3%.

The clock that has a level in it wins, and the arithmetic says the tax argument was never the bigger number.

**Conflict B — the event clock against the tax clock.**

Earnings in 3 sessions; the anniversary in 6. Holding through the print to reach the anniversary is a bet on the event, not a tax decision.

Resolution: rung 3 wins the decision date. Decide now, for both outcomes. If the decision is "sell", the tax clock can then move the *execution* to just after the anniversary **only if** the position's economics do not depend on the event — which, with earnings in three sessions, they almost certainly do.

**Conflict C — the risk clock against everything.**

A Reg T call outstanding, a level broken, earnings tomorrow, an anniversary in nine sessions.

Resolution: rung 1. Reduce or close, inside the window the firm gave you. The other three clocks are queued in writing so the next review can see what they wanted.

**Conflict D — two tax clocks at once.**

A harvested loss two weeks ago and a repurchase idea in the same name, with the anniversary 40 sessions away.

Resolution: the wash-sale window is a **freeze**, not a preference. No purchase in the name, in any account, until day 61 closes. The anniversary is not relevant because the position you would be adding to is inside a window that voids the harvest.

## Failure modes of precedence

1. **Precedence applied from the bottom.** The tax rung is reached first because it is the one with a date the holder likes.
2. **The tax rung used as a veto.** "I can't sell because of tax" applied to a rung-1 forced action, where it has no standing.
3. **The event rung used to delay.** "I'll decide after earnings" repeated through three consecutive quarters is a series of post-hoc decisions, not one decision.
4. **The queued clocks discarded.** A rung-4 clock that lost is invisible unless it is written down.
5. **Precedence confused with consensus.** The table does not average clocks; it ranks them. Averaging a tax date with an event date produces a decision neither clock supports.
6. **The plan rung used when a higher rung fired.** A rung-5 HOLD chosen on a position whose level broke two sessions ago.

## Recording a conflict

Every resolved conflict produces one line in the review record:

```text
conflict:      tax(anniversary in 6 sessions) vs level(breached on the close)
rung_that_won: 2 — breached invalidation level
rung_queued:   4 — tax anniversary, re-checked after the cut
why:           the level is the position; the rate difference is 18% of one sigma of the wait
grade_on:      the next review date
```

The last field matters most. A precedence table that is never graded is folklore; one amended from graded outcomes is a process. Past performance is not a guarantee, and a resolved conflict is evidence about a decision, not a forecast about the price.
