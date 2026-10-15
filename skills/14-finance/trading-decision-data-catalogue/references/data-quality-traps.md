# Data Quality Traps

This is the full traps table. **Each trap is a documented failure mode of the dataset, not a mistake
of the trader** — the trader's own failures are listed in ## Core Workflow of SKILL.md under Failure
Modes. A trap is something the data does to you; a failure mode is something you do to yourself.

## §1 — The Twenty Traps

| # | Trap | How it bites | How to detect it |
|---|---|---|---|
| 1 | **Intraday "open interest"** | The intraday column is yesterday's. A position sized on "OI is rising into the close" is sized on a stale figure | Venues sell a separate end-of-day snapshot *and* a 3:45pm ET snapshot with OI as an **optional** field `[VERIFIED — exchange market-data product documentation]`. If the field were intraday, the EOD product would not exist. Check the field's as-of date, not the read time |
| 2 | **Vendor disagreement on OI or IV** | Two feeds differ for the same contract at the same instant and one is silently chosen, so a hidden assumption enters the model | Diff both feeds on **one fixed timestamp** and record both values with read times. A silent choice is a hidden assumption |
| 3 | **Short-sale volume versus short interest** | Daily short-sale volume is read as shorting pressure and substituted for the position number | Daily short-sale volume is **off-exchange (TRF/ADF/ORF) only**, not consolidated, and FINRA states it **does not equate** to bi-monthly short interest `[VERIFIED — FINRA dataset documentation]`. If the number is daily, it is not short interest |
| 4 | **Fails-to-deliver as naked shorting** | FTD counts are used to argue manipulation, so the thesis is wrong about both the mechanism and the timeline | The SEC states a fail "may result from either a short or a long sale" and that naked short selling "is not necessarily a violation" `[VERIFIED — SEC Reg SHO investor page]`. A fail is a settlement event. *That page is authoritative for these two propositions and **stale on settlement** — it still teaches **T+2** for US equities, so take settlement from SEC Release 34-96930 (`constraint-data-and-calendars.md` §2), never from it* |
| 5 | **The 13F 45-day lag and the "delta" trap** | A quarter-over-quarter change is traded as if four months fresher than it is, and as if the file were the whole book | Due within **45 days after quarter-end** `[VERIFIED — 17 CFR 240.13f-1]`; **long-only, no shorts**, and confidential-treatment requests now file on EDGAR so positions can be absent `[VERIFIED — SEC 13F FAQ]` |
| 6 | **Duplicate and managed 13F filings** | The same book is filed by several entities and the aggregate "position" is double- or triple-counted | **Aggregate by CIK family, not manager name.** Look for identical holdings rows in one quarter; the ticker↔CIK mapping files are explicitly "not guaranteed for accuracy" and cumulative `[VERIFIED — SEC]` |
| 7 | **COT Tuesday-as-of published Friday** | Positioning is read as current when it is three days old at publication and older when read | **Data as of the close of the preceding Tuesday; published Friday 3:30pm ET**; the CFTC states processing takes three days `[VERIFIED — CFTC]`. Historical COT is **never updated** once published |
| 8 | **Point-in-time versus restated** | A macro backtest uses revised history nobody had at the time, so the strategy is fitted to revisions | FRED serves only the **restated** series; without **ALFRED vintages** every macro backtest is look-ahead biased `[VERIFIED — FRED/ALFRED]`. Every macro series needs a vintage identifier |
| 9 | **Survivorship in any historical file** | The delisted names — the losers — are missing, so results are flattered everywhere and the bias is invisible | Count delisted names in the file. A "historical" universe with **zero** delistings is not historical |
| 10 | **Look-ahead in a revised "history"** | A vendor ships a "history" restated after the fact; the strategy is tuned on numbers that post-date the trades | Ask when each row was *first published*, not what value it now holds. If the vendor cannot answer, the file is restated |
| 11 | **Adjusted versus unadjusted prices; splits, spin-offs, symbol changes** | A 2:1 split reads as a −50% daily return; a spin-off's parent return is wrong; a symbol change fragments the series silently | **Rebuild one known spin-off by hand** and compare it to the vendor's series. Once per vendor, and any systematic defect shows up immediately |
| 12 | **The closing print is not a tradable price** | A backtest fills at the official close, which is an auction result, not a price obtainable in the size being simulated | State the fill assumption and the venue. A market-on-close fill is not the printed close, and the printed close is not a bid |
| 13 | **Stale quotes in illiquid options** | A paper fill is taken at the mid of a quote hours old, and the position is marked at a price that never traded | Check the quote **age** before the quote, especially on early-close days — **1:00pm ET** for equities, and options early **by venue** (a venue's options may close at **13:00** where another closes eligible options at 1:15pm). Check your venue's calendar. A stale quote is not a price |
| 14 | **ATS / dark prints lack identity and direction** | A "dark pool accumulation" feed is read as institutional buying when the print carries no counterparty identity and no direction | ATS prints have no identity and no direction in the public tape. Treat any feed assigning a direction as attributing something the data does not contain |
| 15 | **The GEX sign assumption** | A dealer-gamma conclusion is drawn from an inferred figure whose sign convention the vendor chose; flipping it flips the trade | **GEX / dealer gamma by strike is inferred from open interest, never observed.** No exchange publishes it `[COMMON-PRACTICE — vendor product documentation]` |
| 16 | **UOA that is one leg of a spread, a hedge or a roll** | A large single-leg print is read as directional conviction; it was one leg of a structure the screen cannot see | Use open-close volume by **participant capacity** where it is sold (Cboe DataShop) to see *who* traded `[VERIFIED — Cboe DataShop]`. Otherwise label it unclassified flow |
| 17 | **Timezone, DST and half-day effects** | An intraday statistic is compared across a DST shift, or measured on an early-close day, and reads as a regime change in volume or volatility | Equities close **4:00pm ET**, options **4:15pm ET**; **equity** early close **1:00pm ET** on the day after Thanksgiving, **July 3** and **Dec 24** `[VERIFIED — NYSE and Nasdaq published calendars]`. The **options** early close is **venue-specific** (1:15pm ET for eligible options on some venues; **13:00** at Cboe) — check your venue's calendar |
| 18 | **EDGAR post-acceptance corrections not in prior indexes** | A correction to a filing is missed because the daily index was already read and will never be updated | EDGAR accepts **6:00am–10:00pm ET**; filings after **5:30pm ET** (**10:00pm ET** for Forms 3/4/5) disseminate the **next business day**; corrections and deletions are **not backfilled** into prior indexes (full/quarterly indexes rebuild weekly, early Saturday) `[VERIFIED — SEC Accessing EDGAR Data]` |
| 19 | **COT category migration on a Form 40 update** | A trader changes category and the whole historical series shifts; the "positioning change" is an accounting reclassification | The CFTC suppresses category counts with fewer than **4** traders and drops a contract when reportable large traders fall below **20**; spread legs double-count `[VERIFIED — CFTC]`. Check the reportable-trader count before reading a change as positioning |
| 20 | **Vendor alt-data backtests whose holdout the seller chose** | A panel is bought on the strength of a backtest over the period, universe and metric the seller selected | Hold out a period **you** pick, point-in-time, before paying. If the seller's period cannot be replaced, the panel is inadmissible as evidence |

## §2 — Two More That Are Usually Missed

- **A dataset that is free is not therefore unbiased.** SEC fails-to-deliver is free, twice monthly,
  and has a stated non-meaning `[VERIFIED — SEC]`. Free datasets are the most-read ones, which is
  exactly why their documented non-meaning matters more, not less.
- **A dataset with a short lag is not therefore accurate.** Daily short-sale volume arrives daily and
  is not a short-position number at all. **Fresh and relevant are independent properties**, and a
  catalogue that conflates them ranks the wrong thing first.

## §3 — The Traps Grouped by Kind

The grouping matters because the *response* differs by kind.

### 3.1 — STATE traps: the number is stale or partial

Traps 1, 2, 3, 4, 6, 9, 11, 12, 13, 14, 17, 18.

**Response:** state the as-of date and the coverage; never present a subset as the whole. For each of
these the fix is a **field in the record**, not a judgement call: `as_of`, `coverage`, `venue`,
`quote_age`, `is_early_close`, `snapshot_read_timestamp`.

### 3.2 — SIGNAL traps: the number does not measure what it claims

Traps 5, 7, 10, 15, 16, 19, 20.

**Response:** name the assumption, name the seller's incentive, and require a base rate written before
the results. For trap 15 the assumption is a sign; for trap 16 it is a missing leg; for trap 20 it is a
choice of period.

### 3.3 — CONSTRAINT traps: the number binds and is misread as commentary

Traps 4 (partly), 17 (partly), 18 (partly).

**Response:** resolve to a date on a named calendar, and **do not let a constraint carry a view**. The
SEC's own scope statement on the threshold list — that appearance "should not be interpreted as
connoting anything negative about the particular issuer" `[VERIFIED — SEC]` — is the model for how to
phrase every constraint.

## §4 — The Trap Detection Kit

Five mechanical checks that catch most of the list. Each is cheap and each is a standing habit.

1. **The as-of check.** For every STATE figure, is there an `as_of` field distinct from the read
   timestamp? **Catches 1, 3, 7, 9, 12.**
2. **The two-source check.** For every load-bearing number, were two sources compared on a single
   fixed timestamp? **Catches 2, 11, 13.**
3. **The coverage check.** For every dataset with a universe, is the coverage stated and did it
   change over the period? **Catches 6, 9, 10, 14, 20.**
4. **The assumption check.** For every inferred quantity, is the assumption written next to the
   number? **Catches 15, 16, 19.**
5. **The session check.** For every intraday statistic, is the session and its close time recorded?
   **Catches 17, and part of 12 and 13.**

**Running these five on every dataset is the difference between a catalogue and a pile.** None of
them requires a subscription, and all five can be part of a review checklist.

## §5 — Ten Failure Modes That Produce These Traps

1. **Frequency recorded and lag omitted.** Detection: grep the record for a lag field.
2. **A single source treated as verification.** Detection: count sources per load-bearing figure.
3. **An inferred figure stored in a column named like an observed one.** Detection: read the column
   names; `gex` beside `oi` implies they are the same kind of thing, and they are not.
4. **A subset presented as a universe.** Detection: does the record state coverage?
5. **A vendor methodology never requested.** Detection: was the data dictionary asked for, and was it
   read?
6. **A historical file accepted without a delisting count.** Detection: count them.
7. **A revision flag ignored.** Detection: does the record have a field for it?
8. **An index file assumed current after a correction.** Detection: EDGAR does not backfill
   `[VERIFIED — SEC Accessing EDGAR Data]`.
9. **A half day compared to a full day.** Detection: check `is_early_close`.
10. **A holdout accepted without asking who chose it.** Detection: ask the question out loud before
    paying.

**Source:** the publishers named inline in the table — the SEC (Reg SHO investor page, 13F FAQ,
Accessing EDGAR Data, the ticker↔CIK mapping caveat), FINRA (Rule 4560, the daily short-sale-volume
dataset documentation), the CFTC (Commitments of Traders documentation), the Federal Reserve
(H.4.1), FRED/ALFRED, Cboe (DataShop), NYSE and Nasdaq (calendars, for the equity session and the
equity early close — **July 3, the day after Thanksgiving and Dec 24**), each **venue's own options
hours page** for the venue-specific options early close, exchange market-data product
documentation, and vendor product documentation tagged `[COMMON-PRACTICE]`. Each trap above is
attributed to a named source or explicitly labelled as a convention; none is asserted from memory.
Two of those sources come with a scope limit: the **Reg SHO investor page** is authoritative for the
fail's stated non-meaning and is **stale on settlement** (it still teaches T+2 — take settlement from
SEC Release 34-96930), and the **exchange calendars give the equity close only**; the options early
close is the venue's.
