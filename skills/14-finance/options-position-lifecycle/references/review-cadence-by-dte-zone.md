# Review Cadence by DTE Zone

The cadence is how often a position is *examined*, which is different from how often it is *acted on*. Most reviews end in HOLD. The cadence exists so that the reviews that end in an action happen near the moment the action became correct, rather than a week later.

## The base table

| DTE zone | Minimum cadence | What the cadence is protecting against |
|----------|-----------------|----------------------------------------|
| > 45 DTE | Weekly | Slow thesis decay, event drift, and the assumption that "there is time" |
| 21–45 DTE | Twice a week | The working zone: level tests, trims, and rolls are all cheap here |
| 8–21 DTE | Daily | Theta acceleration and the last window in which a repair can complete |
| 3–7 DTE | Daily, plus an intraday gamma watch | Gamma: delta can move faster than the plan assumed |
| 0–2 DTE | Expiry protocol: decide by 15:45 ET on expiry day | Assignment, pin, and the closing auction |
| LEAPS (> 365 DTE) | Monthly, plus every planned roll window | Rho, dividends, and thesis drift over quarters |

**The cadence is a floor, not a schedule.** It says how long a position may go unexamined; it does not say that a position must wait for its slot. Two things pull a review forward immediately:

1. **A level breach** — on the stated measurement, at any DTE, in any zone.
2. **A changed structural fact** — an assignment, a leg that moved, a margin change, an announced event that was not on the calendar.

Everything below in this reference is detail on top of the floor.

## Why the zones are where they are

The boundaries are **derived from when the decision materially changes**, not from a round-number aesthetic.

- **45 days.** The conventional line between "position management" and "position babysitting" for premium-selling strategies. Above it, gamma is small relative to a daily move and a roll is nearly free in theta terms; below it, the clock starts to matter every week.
- **21 days.** The point at which a repair needing a level test can still plausibly complete before expiry for a typical 1–2 week test. Cross it without a repair plan and the plan is mostly gone.
- **8 days.** The last zone in which a level test of even a few sessions fits. Below it you are no longer trading the thesis, you are trading the expiry.
- **3 days.** Gamma becomes the dominant risk for near-the-money short strikes. An intraday look is no longer paranoia; it is the difference between choosing your exit and being handed one.
- **2 days / 0 days.** The expiry protocol, below.
- **365 days.** A LEAPS is a different instrument: it prices rho and dividends more than theta, and a monthly rhythm matches the speed at which its thesis actually changes.

[ESTIMATED] These are operating bands, not measured constants. They come from the structure of option decay and event risk, and they should be re-calibrated per family if your own record shows a different failure pattern — for example, if your cuts cluster at 5 DTE, your 8–21 zone cadence was too slow.

## Expiry protocol (0–2 DTE)

The last two sessions are governed by mechanics, not by thesis.

**The clock.**

| Time (ET) | What matters |
|-----------|--------------|
| Session open | Pin and assignment probabilities are live; the underlying's open matters more than its trend |
| Late morning | Liquidity improves in most names; this is the practical execution window for a discretionary close |
| 15:00 | The window starts closing; some venues handle closing-auction orders differently |
| **15:45** | **Decision deadline.** Any discretionary action on an expiring position is decided here, not at 16:00 |
| After the close | Expiration is processed by the clearing house; ITM options are exercised by exception unless instructed otherwise [VERIFIED] OCC expiration processing |

**The decision deadline is the point of the protocol.** After 15:45 the decision has effectively been made by the market. A plan that says "we'll see how it closes" is a plan to accept whatever assignment or expiration produces.

**Expiry-day checklist.**

1. Is the short strike ITM or within a plausible pin range? If yes, assignment risk is live.
2. Is there a dividend on the underlying before the ex-date? Assignment on short calls is dividend-driven far more often than it is price-driven.
3. Does the assignment produce exposure the plan was never sized for (stock, a bigger delta, a margin call)?
4. Are the closing orders in place with enough time to fill, on the correct side, for the correct quantity?
5. Is the multi-leg structure meant to expire whole, or is one leg at risk of early assignment and the other not?

**Same-session rule for 0DTE.** A 0DTE position is decided and executed in the same session. There is no overnight plan for a contract that does not survive the close, and there is no "gap risk" to accept because there is no gap. What replaces it is an *intraday* stop: a level on the underlying plus a rule about what happens when it is touched.

## Gamma watch (3–7 DTE)

Near the money, an at-the-money option's gamma at a few days to expiry is a multiple of what it was at 45 days; the exact multiple depends on the moneyness and the volatility, but the direction is unambiguous and it is the reason this zone gets daily attention.

**What to watch.**

- **Delta speed.** How much the position's delta changes for a 1% move in the underlying. If the position was sized for a delta that no longer describes it, the size is a fiction.
- **Distance to the short strike** in both absolute and standard-deviation terms.
- **Realised volatility versus the implied volatility you sold.** If realised has been above implied for several sessions, the short-premium position is being paid less than the risk it is carrying.
- **Whether the plan still fits the clock.** At 5 DTE, a plan requiring a level *test* is usually already dead.

**Rule.** In this zone, pay no new extrinsic to extend a position that has not earned it. Extending at 4 DTE is buying expensive time with a story; if the position deserves more time it should have been rolled at 21 DTE.

## Daily zone (8–21 DTE)

The zone where most repairs happen and most trims are booked.

- **Review daily**, preferably at the same time each session so that comparisons are meaningful.
- **Prefer whole-unit trims** here: liquidity in the structure is usually good enough to close whole units without paying a leg-by-leg penalty.
- **Repairs must be initiated here**: the level test needs to fit inside the zone.
- **Roll decisions**: this is where the question "is the remaining premium worth the remaining risk" gets a clean answer, because both sides are still meaningful.

## Working zone (21–45 DTE)

- **Twice a week.** Monday and Thursday, or any two stable points; stability matters more than which days.
- **The structural zone.** Rolls are affordable, trims are cheap, and a level test can complete.
- **Where the exit contract gets maintained.** If a position is going to be held through this zone without a contract, that is the moment to write it, not in the 0–2 zone.

## Long-dated zone (> 45 DTE)

- **Weekly minimum.** The failure mode here is drift: a position opened for a reason that quietly stopped being true two months ago.
- **Monthly deep review**: full re-underwrite, including whether the capital is better used elsewhere.
- **Event checks tighten as expiry approaches.** A quarterly earnings print at 60 DTE matters less than one at 10 DTE, but it still belongs on the list.

## LEAPS (> 365 DTE)

- **Monthly rhythm**, plus **every planned roll window**. LEAPS management is calendar-driven by design: you roll at pre-planned points rather than in reaction to price.
- **Dividends and rho** are the primary variables, not theta. A dividend change on a PMCC's underlying is a bigger event than a 2% move in the stock.
- **The re-underwrite cadence is monthly**, and it must answer one question: does the long-dated thesis still justify the capital, given what has happened to the underlying and to rates?
- **Do not apply short-dated cadence to LEAPS.** Daily attention on a two-year position produces forced action, which is the main way long-dated positions get ruined.

## Re-arm rules (the part that makes the cadence safe)

The cadence floor is only safe if something else can fire between slots. Define the triggers once per position:

| Re-arm trigger | Effect |
|----------------|--------|
| Closing price beyond the invalidation level | Immediate review; escalate one rung |
| The structure's max loss changes (new leg, assignment, ratio slip) | Immediate review of step 2 |
| A new event appears inside the window | Move to PREPARE at the time of discovery |
| Margin requirement rises materially | Immediate review with `options-risk-engineer` |
| The position reaches a take-profit rung | Immediate TRIM review, do not wait for the slot |
| Two consecutive reviews with no state change | Force a full re-underwrite (attention budget check) |

**Write the re-arm level in the same line as the cadence.** A cadence without a trigger is a timetable for being late.

## Session and calendar details that break naive cadences

- **Extended hours are not a reviewable market.** If the exit can only fill in RTH, then a plan built on a pre-market print is built on a market you cannot trade.
- **Half-sessions and holidays** move the expiry-day clock. A "Friday expiry" decision deadline is not always Friday.
- **Early closes** compress the 15:45 window; the practical decision deadline on a half-day is earlier by the amount of the shortened session.
- **Quarterly expiration** changes liquidity and pin behaviour for index-heavy names; treat it as an event, not as a background condition.

## Cadence anti-patterns

| ❌ Anti-pattern | ✅ Do instead |
|----------------|--------------|
| "I'll check it when the alert fires" | Keep the cadence floor *and* the alert; the alert cannot see events or structure |
| Moving the whole book to daily because one position is hot | Cadence is per position and per zone; a hot position does not make the others time-sensitive |
| Reviewing more often as positions lose, less often as they win | Cadence follows the clock; trims are the exception, and they fire on rungs |
| A weekly review that is really a P&L glance | The review runs the seven steps; a glance is not a review |
| Ignoring the LEAPS because "it has time" | Monthly, and at every planned roll window |

## Measuring whether the cadence is right

Two simple diagnostics, both from your own record:

1. **Action latency** — the number of sessions between the moment a level broke and the moment the position was acted on. If this number is consistently above one session, the cadence (or the re-arm triggers) is too slow.
2. **Forced actions** — the share of actions taken in the 0–2 DTE zone. A healthy book resolves most positions before expiry; if most decisions are made in the last two sessions, the earlier zones are being wasted.

Neither number needs to be precise to be useful. Both are visible in the review record this skill's example format describes.
