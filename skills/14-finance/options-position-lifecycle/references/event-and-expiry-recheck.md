# Event and Expiry Recheck

Steps 6 and 7 of the health check, expanded. These are the two steps that get skipped when time is short, and they are the two with the highest ratio of avoided loss to effort: an event missed is an unplanned bet, and an instrument missed is a plan with no executor.

## Why events are a distinct step

A price chart shows what has happened. It does not show what is scheduled. Options positions are affected by scheduled events in ways that are invisible on a chart:

- An **earnings print** changes the entire volatility surface for the front expiry, and can move a position more in one session than a month of trend.
- A **dividend** can make an in-the-money short call economically irrational to hold for the counterparty, producing early assignment that has nothing to do with price direction.
- A **scheduled macro print** compresses or expands implied volatility across the whole index complex, whether or not the underlying moves.
- An **index rebalance** changes liquidity and flow in the affected names, often on a specific close.
- A **trading holiday or half-session** moves the expiry-day clock, which is the clock the whole 0–2 DTE protocol depends on.

The event check is not a forecast. It produces a decision boundary: before this event I will be in state X, and at this event I will do Y, for both outcomes.

## The event checklist

Run this for every position, every review. Each line resolves to a date or to `none`. An empty list is a valid result only if it was checked.

| Event | Where it comes from | Why it matters here |
|-------|--------------------|---------------------|
| Earnings | Your data source or the issuer's investor-relations calendar | The largest single-session volatility event for most single names |
| FOMC / rate decisions | The central bank's published calendar | Moves rate-sensitive names and the whole index complex |
| Scheduled macro releases (CPI, employment, GDP) | The statistical agency's release calendar | Intraday and overnight gap risk; affects IV |
| Ex-dividend dates | The exchange's published corporate-action data | The classic driver of early assignment on short calls |
| Index rebalance / reconstitution | The index provider's published schedule | Liquidity and flow changes, concentrated in a close |
| Quarterly expiration | The exchange's expiration calendar | Pin behaviour, liquidity, and pin-risk mechanics |
| Trading holidays and half-days | The exchange's session calendar | Moves the 15:45 decision deadline and the available exit window |
| Corporate actions (splits, mergers, special dividends) | The exchange's corporate-action notices | Change contract terms; a split-adjusted position is a different structure |

**Data-source discipline.** Event dates change. Record the source and the date you read it (`source:` with the calendar it came from), and re-check at each review rather than trusting a list written two weeks ago. A stale event list is worse than no event list, because it produces confidence in a boundary that no longer exists.

## Event decision template

For each event inside the window, state the action for **both** outcomes. An event with one planned branch is a bet, not a plan.

```text
event:            earnings, 2026-11-04, after the close
position state:   long call, 2 contracts, mark $3.10, debit $3.10
implied move:     about 6.5% from the at-the-money straddle  [ESTIMATED from the chain]
plan:
  if the implied move is below 5% at the print  -> hold the full position through
  if the implied move is 5% or above           -> reduce to 1 contract before the print
  either way, after the print:
    the level is restated at the post-earnings structure, and the improve-by date is
    re-checked against the remaining DTE
recheck at:       the session before the print, to read the implied move
```

The threshold (5% here) is a position-specific number. It should be calibrated to what the position can absorb, not to a general rule of thumb.

## Short calls and ex-dividend dates

This deserves its own section because it is the single most frequently missed event in a book of covered calls and spread structures, and because the mechanics are published rather than mysterious.

**The setup.** A short call that is in the money, or close to it, ahead of an ex-dividend date where the dividend exceeds the remaining extrinsic value of the call. The counterparty can exercise early to capture the dividend, taking the stock a day before the ex-date.

**The consequences.**

1. The short call position becomes a **stock position** (long or short, depending on the structure's other legs) at an unplanned moment.
2. The remaining structure is now **not the structure that was sized**: a spread with one leg assigned is a naked position, which is a step-2 failure.
3. The stock leg has its own **margin, dividend and capital** consequences, none of which were part of the original trade's arithmetic.
4. For a **cash-secured put** writer, the mirror image applies at the other end of the spectrum: the put can be assigned earlier than expected if it is deep in the money and the extrinsic is gone.

**Prevention and handling.**

| Timing | Action |
|--------|--------|
| 5+ sessions before the ex-date | Add the ex-date to the event list with an explicit plan for both outcomes |
| 1–3 sessions before | Read the remaining extrinsic against the dividend; if the dividend exceeds it, assignment is materially more likely |
| Decision point | Either close the short call (paying to remove the risk), roll it above the strike if a credit-or-flat roll exists, or accept assignment with a **written stock-leg plan** in place first |
| After assignment | Immediately write the contract for the stock leg: level, target, date, events. The stock is a new position and gets the same treatment as any other |

**Never** accept assignment without a plan for the resulting shares. The stock leg is usually larger, in capital terms, than the option it replaced — a $5-wide spread's assignment can consume multiples of the original position's risk budget.

## Expiry-day protocol (0–2 DTE)

Expiry is mechanics. The decision has to be made before the mechanics decide for you.

### The clock

| Time (ET) | State | What to do |
|-----------|-------|-----------|
| Session open | Assignment and pin probabilities are live | Read the underlying's open relative to the short strike |
| Mid-morning | Liquidity improving | The practical execution window for a discretionary close |
| 15:00 | Window narrowing | Confirm the closing orders are in place, on the right side, for the right quantity |
| **15:45** | **Decision deadline** | Any discretionary action on an expiring position is decided and sent here |
| After the close | Clearing-house processing | ITM options are exercised by exception unless instructed otherwise [VERIFIED] OCC expiration processing |

### Expiry checklist

```text
1. Structure: which legs expire today, and have the others already been closed?
2. Moneyness: where is each short strike relative to the underlying, and inside what
   plausible pin range?
3. Assignment: if a short leg is assigned, what does the resulting exposure look like,
   and is it inside the account's risk budget?
4. Dividend: does an ex-date fall between the trade date and the expiration settlement?
5. Liquidity: is there a market to close the position today, in the session in which
   the order can actually fill?
6. Orders: are the closing orders correct in side, quantity and session?
7. Brackets: are there resting orders that would OPEN a position after expiry? Cancel them.
8. Record: the resolution (expired / closed / assigned) and the lesson row.
```

Item 7 is a genuinely common incident: a GTC order sized for a structure that is about to expire becomes an instruction to open something new after the position is gone.

### Pin risk

"Pin" describes the case where the underlying finishes very near a short strike, so the option's expiry outcome is genuinely uncertain until settlement. The practical consequences:

- You may not know at 16:00 whether the leg is assigned.
- The resulting exposure can appear over a weekend, unhedged, with no session in which to manage it.
- The uncertainty is largest where the strike is closest to the price, exactly where the position's delta is largest.

**Handling.** Either close the position before the close (accepting the cost of removing the uncertainty), or explicitly accept the pin with a written plan for the weekend outcome. What is not acceptable is being surprised by it — a pin is visible in advance as a small distance between price and strike.

## Corporate actions

Splits, mergers, special dividends and symbol changes alter contract terms. Two practical rules:

1. **Check the exchange's corporate-action notices** for the underlying of every open position at each review in the 0–21 DTE zone, and monthly outside it. Contract multipliers and strike conventions change, and a position that was defined-risk can stop being so.
2. **Never assume the position survived a corporate action unchanged.** Re-read the actual contract terms from your broker's position record and tag the result `[BROKER-VERIFIED]`. This is exactly the class of fact where guessing produces a wrong answer with high confidence.

## Instruments (step 7): the boring step that prevents the incident

The final step asks a simple question: **does the machine that is supposed to execute the plan still exist, and is it pointing the right way?**

| Check | Failure if skipped |
|-------|-------------------|
| Take-profit order exists (or the position is documented as deliberately no-TP) | A winner is never booked because nothing was ever set to book it |
| The SL is a level plus an action, not only a resting order | The level is "managed" by an order that gaps straight through |
| Both are priced for the structure **as now held** | The bracket protects a position that no longer exists |
| The order session matches when the exit can actually fill | An RTH-only venue silently ignores an extended-hours plan |
| Quantities match the current unit count | A bracket sized for the original count reopens structure after a trim |
| No orphan orders remain from a closed or converted position | A stale order opens an unplanned position |

Two minutes of instrument checking per position is the cheapest insurance in this entire skill.

## Failure modes

| Failure mode | What goes wrong | Countermeasure |
|--------------|-----------------|----------------|
| Stale event list | A date moved; the plan is anchored to a boundary that no longer exists | Record the source and the read date; re-check at every review |
| One-branch event plans | Only the favourable outcome was planned; the other is improvised live | Every event gets an action for both outcomes |
| Dividend-blind short calls | Early assignment produces stock nobody planned for | Ex-date is a mandatory line for every short call |
| Pin as a surprise | The position is uncertain at expiry and the exposure appears over a weekend | Detect it in advance (small distance to the strike) and choose: close, or accept with a written plan |
| Half-day ignored | The 15:45 deadline is not where the calendar says it is | Check the exchange session calendar for the expiry week |
| Brackets left live after a close | A stale order opens a new position | Cancel and verify after every CLOSE or CONVERT |
| Corporate action assumed benign | Contract terms changed; a defined-risk structure no longer is | Read the actual position record; tag `[BROKER-VERIFIED]` |
| The instrument check deferred "to the next review" | The gap between the plan and the executor widens silently | Step 7 runs in the same review as steps 1–6, always |

## Provenance

- Expiration, exercise-by-exception and clearing behaviour are governed by the clearing house [VERIFIED] OCC expiration processing; the rules of the venue govern session times and closing-auction handling [VERIFIED] exchange rules as published by the venue's rulebook.
- The interaction between dividends and early exercise on in-the-money short calls is a published feature of American-style equity options and the standard rationale for early exercise; treat any specific dividend-versus-extrinsic comparison as a computation on live data, tagged with its source and timestamp.
- Session times, holiday calendars and half-day schedules change; read them from the exchange's published calendar for the specific expiry week rather than from memory or from a list embedded in a document.
- All worked numbers in this reference are `[COMPUTED]` from stated widths, credits and marks; implied-move figures are `[ESTIMATED]` from the option chain at the moment of reading and are market-implied, not forecasts.
- Past performance is not a guarantee, and an event calendar is a snapshot: it describes what is scheduled as of the moment you read it, not what will happen.
