# Macro and Liquidity Data

Macro data is the class where **the lag is the whole story**. Every series here is published on a
schedule the publisher documents, and every one of them is misread by someone who assumed the value
they can see today is the value that existed then. Two of the datasets below are included because
they are free and structural; the rest are included because they move decisions.

## §1 — The Dataset Table

| Dataset | Publisher | Frequency | **Lag** | Kind |
|---|---|---|---|---|
| **H.4.1** — balance sheet | Federal Reserve | weekly | **as of Wednesday, released Thursdays generally 4:30pm ET**; shifted to the next business day on holidays `[VERIFIED — Federal Reserve]` | STATE |
| **SLOOS** — Senior Loan Officer Opinion Survey | Federal Reserve | quarterly | timed to the Jan/Feb, Apr/May, Aug and Oct/Nov FOMC meetings `[VERIFIED — Federal Reserve]` | STATE |
| **Commitments of Traders** | CFTC | weekly | **data as of the close of the preceding Tuesday; published Friday 3:30pm ET**; the CFTC states processing takes three days; historical data is **never updated** `[VERIFIED — CFTC]` | SIGNAL |
| **GDPNow** | Federal Reserve Bank of Atlanta | roughly weekly, as inputs arrive | updates on the model's own schedule | SIGNAL (nowcast) |
| **FRED** | Federal Reserve Bank of St. Louis | daily | the **restated** series only | STATE |
| **ALFRED** | Federal Reserve Bank of St. Louis | per vintage | the series **as published on each vintage date** `[VERIFIED — FRED/ALFRED]` | STATE (point-in-time) |
| **Treasury auction results** | U.S. Treasury / TreasuryDirect | per auction | published with each auction result | STATE |
| **Treasury Fiscal Data** | U.S. Treasury | daily to monthly, per dataset | per dataset | STATE |
| **BLS / BEA release calendars (ICS)** | BLS / BEA | annual, with updates | published in advance | CONSTRAINT |

## §2 — The CFTC Commitments of Traders, in Full

**Source:** the CFTC's own Cot reports page. `[VERIFIED — CFTC]`.

### 2.1 — The three-day processing lag

The CFTC states it takes **three days to process** the data, which is why the report is **as of the
close of the preceding Tuesday** and is **published Friday at 3:30pm ET**. Two consequences:

1. **The figure is three days old when it is published** and older by the time you read it. A
   "this week's positioning" sentence is a sentence about Tuesday.
2. **Historical COT is never updated once published.** There is no revision process to check. What
   you see for a past date is what was printed, which makes COT unusually clean for backtesting —
   and unusually immutable for anyone who wanted a correction.

### 2.2 — The three ways it silently disappears or double-counts

| Property | Value | Why it matters |
|---|---|---|
| A contract is dropped | when reportable large traders fall below **20** | the series simply ends, and a naive time series reads that as a data outage |
| A category count is suppressed | when fewer than **4** traders are in it | the category looks empty rather than small |
| Spread legs **double-count** | a spread position appears on both sides | gross positioning overstates net exposure |

### 2.3 — Category migration

When a trader updates its **Form 40** and changes category, **the whole historical series shifts.**
A "positioning change" in the data can be an accounting reclassification by one participant.

**Detection rule:** before reading any COT change as positioning, check the **reportable-trader
count** for that market and category. If it moved, the change may be definitional.

## §3 — H.4.1 and SLOOS: The Reserve Backdrop

**Source:** Federal Reserve release schedules. `[VERIFIED — Federal Reserve]`.

- **H.4.1 is weekly, as of Wednesday, released Thursdays generally 4:30pm ET**, shifted to the next
  business day on holidays. It is the reserve-supply backdrop against which every liquidity argument
  is made.
- **SLOOS is quarterly**, timed to the **Jan/Feb, Apr/May, Aug and Oct/Nov FOMC meetings**. It is the
  survey evidence on credit conditions, and because it is quarterly it is a **regime input**, never a
  timing input.

**How they lie:** by being slow and authoritative at the same time. A reader who treats H.4.1 as a
daily liquidity gauge will find it stale three days in four. A reader who treats SLOOS as a
monthly series will find it absent two months in three.

## §4 — GDPNow and the Honesty of Its Own Published Accuracy

**Source:** the Atlanta Fed's own published accuracy statistics. `[VERIFIED — Atlanta Fed]`.

The Atlanta Fed publishes its own error statistics for final GDPNow forecasts over 2011:Q3–2025:Q2:

| Metric | Value |
|---|---|
| Mean absolute error of the final GDPNow forecast | **0.77 percentage points** |
| Root mean squared error | **1.17 percentage points** |

**And the publisher's own conclusion:** the Atlanta Fed itself says this **"does not give compelling
evidence that the model is more accurate than professional forecasters."**

This is the rare case of a dataset whose **producer has published the honest bound on its own
usefulness**, which makes it the best available teaching example for how to read a nowcast:

1. **Use it as a distribution input, not a point estimate.** A forecast with a 0.77pp mean absolute
   error is a forecast with a ±0.77pp average miss, published by its own author.
2. **Do not put it on a chart as a line without its error band.** The band is published; use it.
3. **Do not claim superiority over consensus.** The publisher does not.

## §5 — FRED, ALFRED, and Look-Ahead Bias

**Source:** FRED and ALFRED. `[VERIFIED — FRED/ALFRED]`.

**FRED gives only the restated series.** ALFRED gives the series **as published on each vintage
date**. The difference matters more than it looks:

```
A backtest reads CPI for 2021-03 from FRED today.
FRED returns the value as restated.
If that value was revised after 2021-03, the backtest used a number
that did not exist on the decision date.
        → every macro backtest without ALFRED vintages is LOOK-AHEAD BIASED.
```

### 5.1 — The rule

**Every macro series in a backtest carries a vintage identifier.** Not the series name — the vintage.
A backtest without them is not conservative or optimistic; it is measuring the wrong quantity.

### 5.2 — The cheap audit

Pick one macro series, one decision date in your backtest, and one revision you know happened. Pull
the ALFRED vintage for that decision date and compare it to the FRED value. If they differ, every
backtest number derived from that series is wrong by the difference.

## §6 — Treasury Data and the Release Calendars

- **Treasury Fiscal Data** (the U.S. Treasury's own API) and **TreasuryDirect auction results** are
  free STATE datasets for the funding and supply picture. Read each dataset's own as-of cadence; they
  differ.
- **BLS and BEA publish ICS release calendars**, free, in advance. These are **CONSTRAINT** data: they
  schedule the events that dominate the tape. A position carried into a release the trader did not
  know about is a position with unplanned event risk.

## §7 — Ranked: Macro Datasets for a Trading Decision

| Rank | Dataset | Kind | Verdict |
|---|---|---|---|
| 1 | **H.4.1** | STATE | weekly, short lag, free, structural — the best single liquidity input `[VERIFIED — Federal Reserve]` |
| 2 | **CFTC Commitments of Traders** | SIGNAL | free, weekly, immutable history, with the trader-count and double-count caveats `[VERIFIED — CFTC]` |
| 3 | **ALFRED vintages** | STATE | ranks here rather than lower because it *changes a backtest*, and a wrong backtest changes everything downstream `[VERIFIED — FRED/ALFRED]` |
| 4 | **BLS / BEA ICS calendars** | CONSTRAINT | free, in advance, and the cheapest way to avoid an unplanned event |
| 5 | **SLOOS** | STATE | quarterly; a regime input only `[VERIFIED — Federal Reserve]` |
| 6 | **GDPNow** | SIGNAL | with its own 0.77pp MAE and 1.17pp RMSE published, and the publisher's own caveat `[VERIFIED — Atlanta Fed]` |
| 7 | **Treasury Fiscal Data / auction results** | STATE | free; check each dataset's own cadence |
| 8 | **FRED alone, without vintages** | STATE (biased) | **not admissible in a backtest.** Listed so it can be recognised and replaced |

## §8 — Ten Failure Modes in Macro Data

1. **Reading COT as current positioning.** Detection: state the Tuesday as-of and the Friday 3:30pm ET
   publication in the same sentence. If you cannot, you have not read the schedule.
2. **Using FRED in a backtest without vintages.** Detection: grep the backtest for a vintage
   identifier. Its absence is the defect.
3. **Treating a COT series end as a data outage.** Detection: check whether reportable large traders
   fell below **20** `[VERIFIED — CFTC]`.
4. **Reading a COT change as positioning when a trader changed category.** Detection: check the
   reportable-trader count across the boundary.
5. **Double-counting spread legs.** Detection: compare gross against net category totals.
6. **Treating H.4.1 as a daily series.** Detection: the release is weekly and as of Wednesday.
7. **Treating SLOOS as a monthly series.** Detection: it is quarterly, timed to four FOMC meetings.
8. **Presenting GDPNow without its error band.** Detection: the publisher supplies MAE and RMSE; use
   them or do not chart it.
9. **Comparing GDPNow to consensus as if it were proven better.** Detection: the publisher says the
   opposite `[VERIFIED — Atlanta Fed]`.
10. **Carrying a position through a scheduled release the plan did not name.** Detection: check the
    BLS/BEA ICS calendars against every position's hold horizon.

**Source:** the Federal Reserve's H.4.1 release schedule and its SLOOS description page; the CFTC's
Commitments of Traders documentation for the Tuesday as-of, the Friday 3:30pm ET publication, the
three-day processing statement, the 20-reportable-trader contract threshold, the 4-trader category
suppression and the spread double-count; the Atlanta Fed's published GDPNow accuracy statistics
(2011:Q3–2025:Q2) and its own comparative statement; FRED and ALFRED documentation for the restated
versus vintage distinction; the U.S. Treasury's Fiscal Data and TreasuryDirect auction-results
pages; and the BLS and BEA ICS release calendars. Re-read each before a live decision depends on it.
