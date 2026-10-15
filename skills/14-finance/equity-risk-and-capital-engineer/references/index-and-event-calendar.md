# Index and Event Calendar

Index events are the equity market's scheduled flow. They do not force the holder to act, and that is
exactly why they are dangerous: the holder's exit plan can be scheduled on the one day of the quarter
when the name is being bought or sold in size by everyone else, and nobody has to tell them.

A holder who cannot say which of the dates in this file affects their positions is holding an
unhedged calendar position.

## §1 — S&P Index Events

| Event | Rule | Source |
|---|---|---|
| Share / investable-weight-factor changes | effective **after the close of the third Friday** of **March, June, September and December** | S&P U.S. Indices Methodology |
| Reference date for those changes | the **Wednesday prior to the second Friday** of the same month | S&P U.S. Indices Methodology |
| S&P 1500 constituent changes | announced **5:15 p.m. ET**, with **at least three business days'** notice | S&P U.S. Indices Methodology |
| S&P Total Market Index reconstitution | after the close of the **third Friday in September** | S&P U.S. Indices Methodology |

**What this means for a holder.** The share/IWF change is a *quantity* change in every index-tracking
portfolio, so it produces volume at the effective close — the third Friday. The three-business-day
announcement window for S&P 1500 constituent changes means an add or a delete is knowable in advance,
which is information for anyone planning an exit into that day: **the flow is two-sided, and it is
larger than the average day.**

2026 dates implied by the rule (all three are third Fridays; weekdays verified on the calendar):

```
2026-03-20 (Fri)   2026-06-19 (Fri)   2026-09-18 (Fri)   2026-12-18 (Fri)
```

## §2 — Russell Reconstitution: A Recent Change That Must Be Stated as One

This is the year's largest scheduled liquidity event, and **it changed**.

| Item | Rule | Source |
|---|---|---|
| Historic cadence | annual, in **June**, effective after the close of the **last Friday in June** | FTSE Russell reconstitution documentation |
| **Change** | **moving to a SEMI-ANNUAL reconstitution (June and December) FROM 2026** | FTSE Russell reconstitution documentation |
| Rank day — **June event** | the **last trading day of April** — **2026-04-30** | FTSE Russell reconstitution documentation |
| Rank day — **December event** | the **last business day of October** — **2026-10-30** (the last trading day of October 2026) | FTSE Russell reconstitution documentation |
| First December event | effective **after the close on 2026-12-11** | FTSE Russell reconstitution documentation |
| Preliminary lists for the December event | **2026-11-13**, with updates on **2026-11-20**, **2026-11-27**, **2026-12-04** | FTSE Russell reconstitution documentation |

**Each event has its own rank day, and they are not the same day.** April is the rank day for the
**June** event; the **December** event's rank day is the **last business day of October**
(**2026-10-30**). Treating the April rank day as applying to both is wrong, and it is wrong in the
direction that matters: it puts the December reconstitution's membership determination five months
before the event actually happens.

**Say the word "change" out loud.** Every mental model of "Russell happens in June" that a reader
carries is now incomplete, and the second event does not exist in older documentation. The rank-day
mechanic is unchanged in kind — a rank day precedes its own event — but there are now **two rank days
and two events a year** (April → June, October → December) instead of one, so a name has **two
scheduled windows a year** in which it can be added to or deleted from the indexes rather than one.

### §2.1 — Why this is a liquidity fact and not trivia

The reconstitution's effective close is the single largest liquidity event of the year in many small
and mid-cap names. For a concentrated holder:

- The **effective date is the best liquidity of the quarter** and simultaneously the **worst price
  discovery of the quarter**. A seller gets size without impact and pays a re-rating for it. That
  trade-off has to be a *decision*, made in advance — not something noticed on the day.
- Names **added** to an index are bought by every tracker; names **deleted** are sold. A concentrated
  holder on the wrong side of a deletion faces the exit clock and the index flow meeting in the same
  session.
- The **preliminary and update-list dates** (2026-11-13 through 2026-12-04 above) are the window in
  which the direction of the flow becomes knowable. That is when an exit plan is either scheduled or
  abandoned.

## §3 — Triple and Quad Witching

The **third Friday of March, June, September and December** is the quarterly expiration of
index futures and index options, the session commonly called triple or quad witching.

**Tag: [COMMON-PRACTICE].** No primary source for this convention was retrieved during the research
for this skill, and **this file will not assert one.** What can be said without a source is
operational and useful: the session historically concentrates volume and can produce an unusual close
as positions expire. Treat it as a day on which fills are *different*, verify the session's behaviour
against the venue's own data before relying on it, and do not build a rule on it.

**This is the honest form of the statement.** Where the research did not produce a primary source, the
text says so and does not dress convention up as rule.

## §4 — IPO Lock-Up Expiry

| Item | Value | Tag |
|---|---|---|
| Typical lock-up length | about **180 days** after the offering — **contractual**, set by the underwriting agreement, and it varies | [COMMON-PRACTICE] |
| The only rule-fixed 180 days | FINRA Rule 5110(e)(1): a **180-day** restriction applying to securities received as **underwriting compensation** | [VERIFIED — FINRA Rule 5110(e)(1)] |

**Read the two rows as different things.** The 180-day lock-up everyone quotes is a contract term,
not a rule: some deals are 90 days, some are 180, some have staggered releases, and some have early
release triggers tied to the price. The rule-fixed 180 days in Rule 5110(e)(1) is narrow — it covers
underwriting compensation, not the general lock-up.

**Why a holder cares.** A lock-up expiry is a scheduled increase in **supply** in a name. For a
concentrated holder in a post-IPO small cap, the expiry date is a known future shift in the ADV and
spread inputs to the exit-cost model, and therefore a known future deterioration in
`exit_cost_pct` — see `liquidity-and-exit-cost-planning.md` §5. **The exit cost should be re-measured
on the expiry date, not remembered from before it.**

## §5 — Tax-Loss Selling Season

November and December historically bring concentrated selling in names with unrealised losses, as
holders realise losses before the tax year ends.

**Tag: [COMMON-PRACTICE].** No primary source is cited, because the behaviour is a tax-incentive
consequence rather than a rule. Two consequences that are worth planning around:

- **Spread and volume patterns change seasonally**, so the exit model's inputs move for a reason
  unrelated to the security.
- **The wash-sale window (61 days, ±30) reaches across the year boundary.** A loss realised in
  December and a repurchase in January can be a disallowed loss — the window, not the calendar year,
  is the operative rule. See `equity-time-axis-calendar.md` §1.

## §6 — A Year at a Glance

| When | What | Certainty |
|---|---|---|
| Last trading day of April (2026-04-30) | Russell rank day — **June event** | [VERIFIED — FTSE Russell] |
| Last business day of October (2026-10-30) | Russell rank day — **December event** | [VERIFIED — FTSE Russell] |
| Third Friday of March / June / September / December | S&P share/IWF effective close; quarterly futures and options expiration | [VERIFIED — S&P U.S. Indices Methodology] / [COMMON-PRACTICE] for the witching convention |
| Wednesday before the second Friday of those months | S&P reference date | [VERIFIED — S&P U.S. Indices Methodology] |
| Last Friday of June | Russell reconstitution effective close | [VERIFIED — FTSE Russell] |
| Third Friday of September | S&P Total Market reconstitution | [VERIFIED — S&P U.S. Indices Methodology] |
| 2026-11-13, -11-20, -11-27, 2026-12-04 | Russell December preliminary and update lists | [VERIFIED — FTSE Russell] |
| **2026-12-11** | **First December Russell reconstitution effective close (the new semi-annual event)** | [VERIFIED — FTSE Russell] |
| November–December | Tax-loss-selling concentration | [COMMON-PRACTICE] |
| Per name | Lock-up expiry, tender deadlines, redemption and expiry dates | Per-filing; see `corporate-action-and-halt-playbook.md` |

## §7 — Failure Modes

1. **Not knowing the index membership of a held name.** The largest scheduled flow in that name is
   then invisible.
2. **Planning a large exit on an index effective date without deciding whether the flow helps or
   hurts.** The date is knowable; the answer requires a decision.
3. **Using a pre-2026 model of Russell.** The reconstitution is semi-annual from 2026; a June-only
   calendar is now wrong.
4. **Asserting a source for triple witching.** None was retrieved; the text must say so.
5. **Treating ~180 days as a rule for lock-ups.** It is contractual except for the narrow
   Rule 5110(e)(1) case.
6. **Ignoring a lock-up expiry in the exit-cost model.** Supply rises; the exit cost moves.
7. **Using one rank day for both Russell events.** April's rank day belongs to the **June** event;
   the **December** event's rank day is the **last business day of October**. Using the April date for
   both puts the December membership determination months before the event.
8. **Reading a seasonal pattern as a rule.** November–December behaviour is an incentive consequence,
   not a regulation.
9. **Scheduling a wash-sale-sensitive repurchase by calendar year rather than by the 61-day window.**
10. **Treating a calendar as knowledge rather than as data with a read date.** Every row above carries
    a source and can change.

## §8 — Verification

- [ ] Every held name's index membership is recorded, with the source and the read date.
- [ ] Every effective date that touches a position is on the position's calendar as a date.
- [ ] The Russell semi-annual change from 2026 is stated explicitly wherever the reconstitution is
      discussed.
- [ ] Every Russell date names **which event** it belongs to (June or December) and that event's own
      **rank day** — April for June, the last business day of October for December.
- [ ] Triple witching is labelled [COMMON-PRACTICE], and no source is invented for it.
- [ ] Lock-up dates in held names trace to a filing or to the underwriting agreement, not to the
      ~180-day convention.
- [ ] The exit-cost re-measurement has been scheduled for every known event date in §6.
