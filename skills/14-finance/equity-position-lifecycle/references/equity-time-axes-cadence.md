# Equity Time Axes and Review Cadence

Options have one clock — DTE — and it expires the position whether or not anybody decides anything. Equities have four clocks, and **none of them ends the position**. Every one of them is a date, a window or a barrier that a holder can write down, miss, and be penalised for. What none of them does is force a decision.

That asymmetry is the whole design problem. The skill's job is to manufacture the deadlines the market will not.

**Portability target:** spec-level. The clocks are statutory or exchange-defined; the cadence is a desk convention and is labelled as such.

## The four axes

### Axis 1 — Settlement and payment (days)

| Item | The rule | Source |
|---|---|---|
| Settlement | **T+1** since 2024-05-28 | SEC Release 34-96930 |
| Reg T payment / margin call | standard settlement cycle **+ 2 business days = 3 business days** | 12 CFR 220.2, 220.4(c)(3)(i) |
| Margin call consequence | deficiency <= $1,000 → no action required; otherwise the firm must liquidate, and **no advance notice is required** | 12 CFR 220.4(d) |
| Intraday / day-trading margin | The **former "pattern day trader" regime was replaced in its entirety**: the four-day-trades-in-five-business-days count and the **$25,000 minimum equity** `[VERIFIED]` were superseded effective **2026-06-04** by **FINRA Regulatory Notice 26-10** (SEC-approved 2026-04-14/15, phased in to 2027-10-20), which sets intraday margin directly under **FINRA Rule 4210(d)(2)**. Verify with your broker: this changed in 2026. | FINRA Regulatory Notice 26-10; FINRA Rule 4210(d)(2) |

All four are [VERIFIED] against the citation in the source column. Note the shape of this axis: it is the only one of the four that can **force** an action, and it forces it on the firm's timetable, not yours. A T+1 settlement clock is short enough that a decision skipped on Friday is a decision taken by someone else on Monday.

**Historical note.** Until 2026-06-04 this axis carried a "pattern day trader" rule: four or more day trades in five business days, a $25,000 minimum equity `[VERIFIED]`, and a 90-day cash-available-basis restriction after a missed call — then at Rule 4210(f)(8). Regulatory Notice 26-10 replaced that framework in its entirety, so a broker page still publishing the old test is publishing a superseded requirement.

### Axis 2 — The tax holding period (barriers)

- Long-term means held **more than 1 year** [VERIFIED — IRC §1222].
- The holding period **begins the day after the buy trade date and ends on the sale trade date** [VERIFIED — IRS Pub 550].
- Therefore the earliest long-term sale is **buy date + 1 year + 1 day**.

The one-day offset is not trivia. A purchase on 12 June 2025 has its first long-term sale date on 13 June 2026, and a sale on 12 June 2026 is short-term — the anniversary date itself is still short. The trade-date convention is what makes this checkable rather than a memory exercise.

### Axis 3 — The tax windows (windows you must be inside or outside of)

| Window | The rule | Source |
|---|---|---|
| Wash sale | **61-day window: 30 days before through 30 days after** the loss sale; replacement shares inherit the old holding period | IRC §1091, §1223(3) |
| Qualified dividend | hold **>= 61 days during the 121-day period beginning 60 days before the ex-date** | IRC §1(h)(11), §246(c) |
| Ex-dividend | under T+1 the ex-date equals the record date for distributions under 25% of value; buy **before** the ex-date to receive | FINRA Rule 11140 (amended eff. 2024-05-28) |

All [VERIFIED] against the cited statute or rule. These are windows, not countdowns, and the difference matters: a countdown tells you when something happens, a window tells you what behaviour is legal during a period. A repurchase on day 29 after a loss sale is inside the window; on day 31 it is not.

### Axis 4 — The exchange and index calendar (fixed dates)

| Date | The rule | Source |
|---|---|---|
| S&P share/IWF changes | effective after the close of the **third Friday of March, June, September and December** | S&P U.S. Indices Methodology |
| Russell reconstitution | annual in June (effective after the close of the last Friday in June) — **moving to a SEMI-ANNUAL schedule (June and December) from 2026** | FTSE Russell reconstitution documentation |

Both [VERIFIED]. These matter for two reasons: index membership changes can move a position's liquidity, and the reconstitution sessions are among the highest-volume, most distorted prints of the quarter.

### Axis 5 — The insider's clock (for the reader who is the insider)

Short-swing profit from a purchase-and-sale **within less than six months** is recoverable by the issuer [VERIFIED — 15 U.S.C. §78p(b)]. The accompanying deadlines: Form 4 within 2 business days; Schedule 13D within 5 business days, amendments within 2 business days (eff. 2024-02-05); Form 13F within 45 days after quarter-end; Rule 10b5-1 cooling-off = the later of 90 days or 2 business days after the covering 10-Q/10-K, capped at 120 days for directors and officers and 30 days for everyone else (eff. 2023-02-27).

**Honest scope line.** If you are an ordinary retail holder, this entire axis is **not you**. It is listed so the reader can confirm that, not so the risk list can be padded.

## How the axes interact

The axes are not independent, and the interactions are where holders get hurt:

1. **Settlement can destroy a tax plan in three days.** A Reg T call outstanding on a position you intended to hold to the anniversary is a forced sale — the tax calendar is irrelevant, because the firm acts on its own timetable and need give no advance notice.
2. **The wash-sale window outlives the trade.** A harvested loss freezes the name for 61 days *in every account*, which means a rotation into the same name inside the window is not a rotation, it is a void harvest.
3. **The ex-date is a tax commitment, not a payday.** Buying for the dividend starts a 61-of-121 holding requirement; the ex-date is also a price event. The two facts are separate and both true.
4. **The long-term anniversary and the index calendar can collide.** A reconstitution session inside the five days before an anniversary gives a holder a liquidity reason and a tax reason to trade in the same week, and the two often point different ways.
5. **Hedging interacts with the holding-period rules.** Writing against a position is not a neutral act for the clock; the rule is owned by `equity-tax-lot-and-exit-management` and must be flagged before the hedge is written, never assumed.

## Review cadence by time-axis state

The cadence is a **desk convention** [ESTIMATED] — it is set by when each clock changes what is worth deciding, not by any measured statistic. What is not a convention is the escalation rule: any level breach pulls the review forward to now, on any state.

| State | Cadence | Required output of each review |
|---|---|---|
| No hot clock | **Weekly**, fixed day | Steps 1–8; a HOLD with a level and a date |
| Earnings inside 10 business days | **Daily** + written pre-earnings decision | The action for both outcomes, before the print |
| Ex-dividend inside 5 sessions | **Daily** | Buy / hold / avoid, plus the qualified-dividend window that follows |
| Index reconstitution inside 5 sessions | **Daily** | Whether membership change affects size or liquidity |
| Anniversary inside 5 sessions | **Daily** | The decision taken before the date, not after |
| Wash-sale window open | **Flag the name at every review** | No purchase in the name, any account, until it closes |
| Qualified-dividend window open and unmet | **Flag at every review** | The 61-day count; whether the action breaks the holding period |
| Margin, borrow or intraday-margin stress | **Intraday** | The forced action, inside the window the firm gave you |
| Winner above trim rung 1, no trim executed | Review before any new entry is discussed | The trim, or a written refusal |

## Escalation ladder

| Rung | Name | Trigger | What it authorises |
|---|---|---|---|
| 0 | WATCH | Ordinary state | Full review on the cadence; no action required |
| 1 | PREPARE | An event inside 10 business days | A written pre-event decision; no execution yet |
| 2 | ACT | Level breached, thesis broken, or an event inside 5 business days | The routed action, now |
| 3 | FORCE | Forced action live, or desk breaker on | CLOSE or reduce only; everything else is deferred |

The ladder only escalates. A position at rung 2 does not return to rung 0 because the market bounced; it returns when the level is re-established on a close and the event has passed, and the return is written down.

## Re-arm conditions

The date is the floor on attention; the level is the trigger. A review is re-armed early when:

- The close is beyond the invalidation level.
- A new event lands inside 10 business days (an unscheduled earnings date change, a merger announcement, a dividend declaration).
- Share count, lot set or basis changes without a decision by the holder.
- A margin, borrow or intraday-margin state appears.
- An anniversary moves inside 5 sessions.

## Failure modes of a cadence

1. **The cadence becomes the only trigger.** Monthly reviews of a position that broke on day 3. Countermeasure: the level trigger, armed separately from the date.
2. **The cadence is set once and never re-rated.** A weekly review of a position with no clock and no plan. Countermeasure: the state table is re-read at every review.
3. **The cadence is ignored during a drawdown, exactly when it matters.** Countermeasure: rung 3 is a forced-action rung, and forced actions are not subject to mood.
4. **The tax flag is raised and then treated as a reason to act.** The flag has no disposition; the router decides.
5. **Everything is escalated.** A book where every position is at rung 2 has no ladder at all. Countermeasure: rung 2 requires a breached level or an event inside 5 sessions, in writing.

**Past performance is not a guarantee of future results.** The cadence boundaries here are approximate operating bands, derived from when each clock changes a decision, not measured constants — re-check them against the position in front of you.
