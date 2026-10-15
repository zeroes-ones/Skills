# Constraint Data and Calendars

Constraints are the datasets that **remove options rather than add information**. They are the most
valuable entries in this catalogue for exactly that reason: a signal offers a gain, a constraint
prevents a loss, and the loss is certain once it happens. This file collects them.

## §1 — The Exchange Calendar

**Source:** NYSE and Nasdaq published calendars for the equity session and the equity early closes;
each **venue's own options hours page** for the options early close, which is venue-specific.
`[VERIFIED — NYSE and Nasdaq published calendars; venue options hours pages]`.

| Property | Value |
|---|---|
| Equity regular close | **4:00pm ET** |
| Options regular close | **4:15pm ET** |
| Equity early close | **1:00pm ET** — on the day after Thanksgiving, **July 3** and **Dec 24** (and, in a year where July 4 falls on a weekend, on the exchange's own designated day — read the year's calendar rather than inferring it) `[VERIFIED — NYSE and Nasdaq published calendars]` |
| Options early close | **venue-specific** — **1:15pm ET** for eligible options on some venues, **13:00** at Cboe. **Check your venue's own calendar**; never carry one venue's early close to another |
| Holidays | published in advance, per year |

### 1.1 — Why this ranks third of twelve

**Every intraday statistic you own is distorted on those days.** Volume, range, realized volatility,
quote age, the half-life of an impact estimate, the effective spread — all of them are functions of
session length and liquidity, and a half day changes both. A statistic computed on a half day and
compared to a full day will read as a regime change in volatility that did not happen.

### 1.2 — The detection rule

Ask three questions of any intraday number:

1. **Which session is it from?** Pre-market, regular, after-hours, overnight. They are different
   markets with different participants.
2. **Was it an early close?** Check the calendar rather than the price action.
3. **Did a DST transition fall inside the comparison window?** A timezone shift moves one hour of
   activity from one bucket to another and looks like a liquidity change.

### 1.3 — The permanent record fields

| Field | Why |
|---|---|
| `session` | which of the four sessions the observation came from |
| `session_close_et` | 16:00, 16:15, 13:00 or 13:15 — the value is not always 16:00 |
| `is_early_close` | boolean, from the calendar, not inferred |
| `calendar_year_read` | the year of the calendar used, so a stale read is visible |

## §2 — Settlement: Get This Right

**Source:** SEC Release 34-96930; 12 CFR 220.2 and 220.4(c)(3)(i). `[VERIFIED — SEC Release 34-96930]`.

| Cycle | Value | Source |
|---|---|---|
| US equities | **T+1** since the 2024-05-28 compliance date | SEC Release 34-96930 |
| Listed options | **T+1** | SEC Release 34-96930 |
| **The Reg T payment / margin-call window** | the settlement cycle **+ 2 business days = 3 business days** from the trade | 12 CFR 220.2, 220.4(c)(3)(i) |

**A warning about stale sources.** You will encounter older pages still stating **T+2** for US
equities. That is stale. State **T+1** and cite the release `[VERIFIED — SEC Release 34-96930]`.

### 2.1 — The three clocks, kept apart

```
trade date  ──T+1──▶  settlement / delivery
trade date  ──+2 BD─▶ settlement ──▶ Reg T payment window closes (3 business days from trade)
```

1. **Settlement** is when cash and securities move.
2. **The Reg T payment window** is a *different* clock, measured from the trade, and it is the one a
   margin deficiency runs on. Do not use one as a proxy for the other.
3. **Both are business days in the market's calendar**, which is why §1 must be resolved first.

### 2.2 — How settlement data lies

1. **By being quoted as T+2.** Detection: cite the release, not the blog.
2. **By mixing the two clocks.** Detection: is the deadline measured from the trade or from
   settlement? State it.
3. **By ignoring holidays.** Detection: resolve the date on the calendar, then give the date, not a
   duration.

## §3 — Index Rebalance Dates

**Source:** S&P U.S. Indices Methodology; FTSE Russell reconstitution documentation.
`[VERIFIED — S&P U.S. Indices Methodology; FTSE Russell]`.

### 3.1 — S&P

| Property | Value |
|---|---|
| Share / IWF changes take effect | **after the close of the third Friday** of March, June, September and December |
| Reference date | the **Wednesday prior to the second Friday** |

### 3.2 — Russell

Russell reconstitution **was annual in June** and is **moving to semi-annual (June and December)
from 2026**. This is a recent change and worth calling out to anyone whose calendar was written
before it.

### 3.3 — How index dates lie

1. **The effective close is not the tradable close.** Rebalance activity concentrates in the closing
   auction, which is a different market from the continuous session.
2. **The reference date is not the effective date.** The reference date determines *what* changes;
   the effective date determines *when*. Trading the wrong one produces the wrong expectation about
   which side of the flow you are on.
3. **The announced list is not the completed list.** Additions and deletions can be announced and
   then amended.

## §4 — IPO Lock-Up Expiries: There Is No Primary Calendar

`[COMMON-PRACTICE]` — and this is stated as practice rather than as a rule because **no primary
calendar exists.**

| Property | Reality |
|---|---|
| Where the terms live | the **424B prospectus** on EDGAR, for that specific deal |
| Aggregator dates | frequently wrong |
| Structure | often **staggered tranches**, not a single date |
| Early release | often **triggered**, e.g. by a price condition or an earnings date |

### 4.1 — The detection rule

**Read the 424B prospectus for the deal you care about.** Do not use an aggregator's date as a fact.
If you must use one, label it `[COMMON-PRACTICE]` and say the primary source was not read.

### 4.2 — Why this entry exists at all

Because it is the most common **hallucinated calendar** in finance. A date that does not exist is
worse than an unknown date, because it will be used.

## §5 — Unverified Constraint Sources

Each of these was sought for this skill and **not confirmed against a primary source**. Retrieve
them from the publisher before relying on any specific value.

| Item | Status | What to do |
|---|---|---|
| **OCC** volume and open-interest statistics pages | not retrieved for this skill; **no OCC figure is stated anywhere in this skill** | retrieve the OCC page directly |
| **OPRA / CTA plan documents** (fee schedules, participant definitions) | not retrieved | read the plan documents from the plans' own sites before quoting a fee or a participant category |
| **S&P DJI methodology** behind a paywall or a 403 | not retrieved beyond the published effective-date convention | retrieve the current methodology document before depending on a specific rebalance detail |
| **MSCI** review effective dates | not retrieved | check MSCI's own index-review page |
| **Any IPO lock-up calendar** | **no primary calendar exists** | read the 424B prospectus for the deal |

## §6 — Ranked: Constraint Datasets

| Rank | Constraint | Kind | Cost | What it removes from the table |
|---|---|---|---|---|
| 1 | **The Reg SHO threshold list + the 13-settlement-day clock** | CONSTRAINT | free | the short position itself, if the close-out clock is running |
| 2 | **The exchange holiday and early-close calendar** | CONSTRAINT | free | the comparability of every intraday statistic you own |
| 3 | **Your broker's borrow availability** | CONSTRAINT | free to read | the short position, at the size the inventory cannot bear |
| 4 | **Settlement T+1 and the Reg T window** | CONSTRAINT | free | the assumption that cash arrives when you think it does |
| 5 | **Index rebalance effective dates** | CONSTRAINT | free | the assumption that the close is a tradable price on that date |
| 6 | **BLS / BEA release calendars** | CONSTRAINT | free | the assumption that a hold horizon contains no scheduled event |
| 7 | **IPO lock-up expiries** | CONSTRAINT-ish | free but laborious | nothing, unless you read the 424B — then it removes a supply surprise |

## §7 — Ten Failure Modes in Constraint Data

1. **An intraday statistic measured on a half day.** Detection: check `is_early_close` before
   comparing anything across sessions.
2. **A deadline given as a duration.** Detection: ask for the date and the calendar it was resolved
   on. A duration has no answer.
3. **Quoting T+2 for US equities.** Detection: cite SEC Release 34-96930 and state T+1.
4. **Confusing settlement with the Reg T payment window.** Detection: state which clock the deadline
   is measured from.
5. **Trading the index reference date instead of the effective date.** Detection: name both dates and
   say which one the position is positioned for.
6. **Using an aggregator's IPO lock-up date.** Detection: was the 424B prospectus read? If not, label
   it `[COMMON-PRACTICE]`.
7. **Assuming a single lock-up date where the deal has tranches.** Detection: count the tranches in
   the prospectus.
8. **Assuming a calendar read last year is current.** Detection: record `calendar_year_read`.
9. **A DST transition inside a comparison window.** Detection: compare like-for-like local times.
10. **Quoting an OCC, OPRA, CTA, S&P DJI or MSCI figure that was never retrieved.** Detection: this
    skill states none of them; if a draft contains one, it came from somewhere other than primary
    material.
11. **Carrying one venue's options early close to another.** Detection: the options early close is
    **venue-specific** (1:15pm ET for eligible options on some venues, **13:00** at Cboe). Read your
    venue's own hours page, and record `venue` beside `session_close_et` — a session close copied from
    another venue is an assumption wearing a fact's clothes.

**Source:** NYSE and Nasdaq published calendars for session times and early closes — including
**July 3**, and the exchange's own designated day in a year where July 4 falls on a weekend — and
each **venue's own options hours page** for the venue-specific options early close; SEC Release
34-96930 and 12 CFR 220.2 with 220.4(c)(3)(i) for T+1 and the Reg T payment window; the S&P U.S.
Indices Methodology and FTSE Russell reconstitution documentation for the rebalance effective and
reference dates and the move to semi-annual from 2026; 17 CFR 242.203 and 242.204(a) for the
threshold-security close-out clocks; and the 424B prospectus on EDGAR as the only primary source for
lock-up terms. The items in §5 are listed precisely because they were **not** retrieved; treat them
as open questions and check the publisher.
