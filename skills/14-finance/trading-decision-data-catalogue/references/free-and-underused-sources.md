# Free and Under-Used Sources

Everything in this file is **free**, and most of it is under-used, which is the point. A trader who has
not exhausted this list has no business buying a data subscription: the free material answers a large
share of the questions people pay for, and it answers them with a named publisher attached.

**Two rules before the list.** (1) **Free is not unbiased** — the SEC's fails-to-deliver file is free
and carries an explicit non-meaning. (2) **Read the publisher's own page for the schedule**, because
third-party summaries of regulatory datasets are routinely wrong about the lag.

## §1 — The List

| # | Source | What it gives you | Publisher's own cadence and lag |
|---|---|---|---|
| 1 | **EDGAR full-text search** | search across filing text, including forms predating structured data | continuous; EDGAR accepts **6:00am–10:00pm ET** `[VERIFIED — SEC Accessing EDGAR Data]` |
| 2 | **`data.sec.gov` APIs** | structured submissions, company facts, financial statements | continuous; same acceptance window; rate limit **10 requests/second**; a declared **User-Agent** is required `[VERIFIED — SEC Accessing EDGAR Data]` |
| 3 | **EDGAR daily index files** | every filing accepted that day, by form type | daily; **corrections are not backfilled** into prior daily indexes `[VERIFIED — SEC Accessing EDGAR Data]` |
| 4 | **EDGAR full and quarterly index files** | the rebuildable indexes | **rebuilt weekly, early Saturday** `[VERIFIED — SEC Accessing EDGAR Data]` |
| 5 | **FINRA Rule 4560 equity short interest** | the only real short-**position** number in public data | semi-monthly; settlement on the 15th or the last settlement business day; reported by **6pm ET the 2nd business day**; **published the 7th business day after settlement**; **Revision Flag overwrites history**; 5 rolling years `[VERIFIED — FINRA Rule 4560]` |
| 6 | **Nasdaq Reg SHO threshold list** | the daily threshold-security list | daily; **one list is not the universe** — only the exchange with the primary listing publishes a name `[VERIFIED — SEC]` |
| 7 | **SEC fails-to-deliver** | settlement-failure data | **twice a month**, history from **2004Q1** `[VERIFIED — SEC]` |
| 8 | **Cboe `VIX_History.csv`** | the VIX series | free; **from 1990** `[VERIFIED — Cboe]` |
| 9 | **Cboe `VVIX_History.csv`** | the volatility-of-volatility series | free; **from 2006** `[VERIFIED — Cboe]` |
| 10 | **Cboe `SKEW_History.csv`** | the tail-risk skew series | free `[VERIFIED — Cboe]` |
| 11 | **Cboe daily market statistics** | put/call **disaggregated by index, ETF, equity and VIX** | free, daily `[VERIFIED — Cboe]` |
| 12 | **FRED** | thousands of economic series | daily; **the restated series only** `[VERIFIED — FRED/ALFRED]` |
| 13 | **ALFRED** | the same series **as published on each vintage date** | per vintage; the only defence against look-ahead bias in macro backtests `[VERIFIED — FRED/ALFRED]` |
| 14 | **Fed H.4.1** | the Federal Reserve balance sheet | weekly; **as of Wednesday, released Thursdays generally 4:30pm ET**, shifted to the next business day on holidays `[VERIFIED — Federal Reserve]` |
| 15 | **SLOOS** | the Senior Loan Officer Opinion Survey on credit conditions | quarterly, timed to the Jan/Feb, Apr/May, Aug and Oct/Nov FOMC meetings `[VERIFIED — Federal Reserve]` |
| 16 | **CFTC Public Reporting Environment** | the Commitments of Traders archive and the reportable-trader detail behind it | weekly; COT is **as of the preceding Tuesday and published Friday 3:30pm ET**; historical data is **never updated** `[VERIFIED — CFTC]` |
| 17 | **Treasury Fiscal Data** | federal receipts, outlays, debt and the Daily Treasury Statement family | per dataset; check each dataset's own cadence |
| 18 | **TreasuryDirect auction results** | auction dates, sizes, results and awards | per auction |
| 19 | **BLS and BEA ICS release calendars** | the scheduled macro releases, in a machine-readable calendar | annual, published in advance — the cheap way to avoid an unplanned event |
| 20 | **openFDA** | FDA adverse-event, recall, device and label data | per dataset; a genuine alternative dataset with a named publisher |
| 21 | **ClinicalTrials.gov** | trial registrations, status changes and results postings | continuous; the primary record for the trial-timeline question |
| 22 | **EIA Open Data** | energy production, storage, consumption and prices | weekly to monthly, per series |
| 23 | **Federal Register API** | every rule, notice and **exemptive order**, with effective dates | daily; **this is the tool that tells you whether a dataset legally exists yet** |

## §2 — The Two Entries That Answer the Most Questions

### 2.1 — The Federal Register API

The most under-used source in the whole list, because it answers a question no market data feed can:
**does this dataset legally exist?**

- Form SHO / Rule 13f-2 monthly manager short positions: **exempt until Jan 2, 2028**
  `[VERIFIED — SEC exemptive order, FR 2025-22158]`.
- Rule 10c-1a securities-lending reporting: **exempt until Sept 28, 2028**, with FINRA public
  dissemination exempt until **March 29, 2029** `[VERIFIED — SEC exemptive order, FR 2025-22158]`.

**The method:** search the API for the implementing release, read its effective date and any relief.
A press release announcing an adopted rule is not evidence that the data exists.

### 2.2 — ALFRED

FRED is the most-used free macro source and the most dangerous one to backtest on, because it serves
the **restated** series. ALFRED serves the series **as published on each vintage date**
`[VERIFIED — FRED/ALFRED]`. One audit settles it: pick a decision date in your backtest, pull the
ALFRED vintage for that date, and compare it to the FRED value. If they differ, every number derived
from that series is wrong by the difference.

## §3 — Ranked: Free Sources by Decision Value

| Rank | Source | Why it ranks here |
|---|---|---|
| 1 | **FINRA Rule 4560 short interest** | the only real short-position number; nothing paid replaces it |
| 2 | **Nasdaq threshold list** | a constraint that can delete the trade; free |
| 3 | **Exchange holiday and early-close calendars** | without it no intraday statistic is comparable |
| 4 | **CFTC Public Reporting Environment** | free, weekly, immutable history, with the trader-count caveats |
| 5 | **Fed H.4.1** | free, weekly, short lag, structural |
| 6 | **ALFRED vintages** | changes backtests rather than trades, and therefore changes everything downstream |
| 7 | **EDGAR (search, APIs, indexes)** | the primary text and filing corpus, regulator-timestamped |
| 8 | **Federal Register API** | tells you whether a dataset exists |
| 9 | **Cboe daily market statistics + three index CSVs** | free, dated, long history from 1990 / 2006 |
| 10 | **SEC fails-to-deliver** | free and twice-monthly, meaningful **only** with the threshold list |
| 11 | **BLS / BEA ICS calendars** | schedules the events that dominate the tape |
| 12 | **Treasury Fiscal Data / auction results** | free funding and supply picture |
| 13 | **openFDA, ClinicalTrials.gov, EIA** | genuine alternative datasets with named publishers, and no panel-drift problem |
| 14 | **FRED alone** | useful for reading, **not admissible in a backtest** without vintages |

## §4 — Six Things People Pay For That This List Already Answers

1. **"Where can I see short interest?"** FINRA Rule 4560, free, with the revision flag.
2. **"How do I know if a name is a threshold security?"** the exchange's own daily list, free — and
   remember one list is not the universe.
3. **"What is the VIX history?"** Cboe's own CSV, free, from 1990.
4. **"Where is the options positioning data?"** Cboe's free daily market statistics, disaggregated,
   plus end-of-day open interest.
5. **"How do I get macro data without look-ahead?"** ALFRED vintages, free.
6. **"Does the monthly short reporting exist yet?"** the Federal Register API, free, in one query.

## §5 — Ten Failure Modes Even With Free Data

1. **Treating free as unbiased.** Detection: does the dataset's publisher state a non-meaning? FTD
   does `[VERIFIED — SEC]`.
2. **Reading a frequency and inferring a lag.** Detection: read the publisher's own schedule.
3. **Re-reading the archive instead of crawling forward.** Detection: EDGAR does not backfill
   corrections `[VERIFIED — SEC Accessing EDGAR Data]`.
4. **Ignoring the revision flag on short interest.** Detection: is there a field for it? `[VERIFIED —
   FINRA Rule 4560]`.
5. **Reading the threshold list as an accusation.** Detection: quote the SEC's scope statement.
6. **Assuming one threshold list is the universe.** Detection: name the exchange that published it.
7. **Using FRED in a backtest.** Detection: is there a vintage identifier per observation?
8. **Assuming an auction result is a tradable price.** Detection: state the fill assumption and venue.
9. **Treating the free daily short-sale volume as short interest.** Detection: if the number is daily,
   it is a flow `[VERIFIED — FINRA dataset documentation]`.
10. **Citing a dataset whose implementing release is under relief.** Detection: one Federal Register
    API query.

**Source:** each row of §1 states its publisher and was read from that publisher's own
documentation — FINRA for Rule 4560 and the daily short-sale-volume dataset; the SEC for EDGAR access
rules, the fails-to-deliver file, the Reg SHO investor page and the threshold-list scope statement;
the SEC exemptive order at FR 2025-22158 for the Form SHO and Rule 10c-1a dates; Cboe for the three
index history CSVs and the daily market statistics; the Federal Reserve for H.4.1 and SLOOS; FRED and
ALFRED for the restated-versus-vintage distinction; the CFTC for the Commitments of Traders schedule
and its trader-count caveats; the U.S. Treasury for Fiscal Data and TreasuryDirect auction results;
BLS and BEA for the ICS calendars; and openFDA, ClinicalTrials.gov and EIA Open Data as named public
datasets. No price is stated for any of them because all are free.
