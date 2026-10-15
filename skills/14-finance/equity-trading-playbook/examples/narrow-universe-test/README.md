# narrow-universe-test -- README

**The hypothesis under test.** The desk owner proposed restricting the traded
universe to a few index ETFs (SPY, QQQ, IWM), or to the S&P 100 / Nasdaq 100
constituents, and trading those as both stocks and options. Is a narrow, highly
liquid universe better or worse than a broad one?

The measured answer is in [`FINDINGS.md`](FINDINGS.md). Every number in that
document comes from the run captured in [`RESULTS.md`](RESULTS.md) and
[`run-output.txt`](run-output.txt).

---

## 1. Where the data came from, and when

| | |
|---|---|
| **Price source** | TradingView, via the MCP tool `mcp__tradingview__mcp-tv-get-ohlcv`, `interval=1D`, `format=columns` |
| **Price pull date** | **2026-10-14** (the final bar of that day was still forming at pull time) |
| **Quote source** | Schwab, via `mcp__schwab__get_quotes`, one snapshot of all 17 instruments |
| **Quote snapshot** | **2026-10-15T00:39Z** (= 2026-10-14 20:39 ET, ~40 min after the 16:00 ET close) |
| **Cash source** | `TVC:US03M` -- the 3-month US Treasury bill **yield index**, in percent per annum. **Not a price.** |
| **Reused series** | SPY, QQQ, IWM, TLT, GLD, EEM, VIX, US03M, BIL were already pulled by `../frontier-test` on the same day and are reused after a byte-level overlap check |

`data/*.csv` each carry a `# PROVENANCE:` header naming the exact source symbol,
the interval, the pull date, the number of payloads merged, and -- for price
series -- an explicit `PRICE-ONLY. No dividends or distributions. Not a
total-return series.` line.

### Which tickers resolved, and which did not

Six of the fourteen constituent tickers **did not resolve under the exchange
prefix given in the brief**. `AMEX:JPM`, `AMEX:JNJ`, `AMEX:WMT`, `AMEX:XOM`,
`AMEX:UNH`, `AMEX:V` and `AMEX:AVGO` were all refused by the source with
`symbol_error [invalid symbol]`; `NYSE:WMT` was refused too. The prefixes that
actually worked are recorded in `pull_ohlcv.py`'s `FILENAME_FOR_SYMBOL` and in
`pull-output.txt`. All fourteen tickers were obtained; **none was dropped for
resolution failure.**

Note that `WMT` resolves as `NASDAQ:WMT` because Walmart's listing moved.

---

## 2. The universe rule, declared before any run

Nothing in this study was chosen because it scored well. The following was fixed
before the first number was computed.

**The three-index universe.** `SPY, QQQ, IWM`. Exactly the tickers the brief
named. No substitutions, no additions.

**The cross-asset universe.** `SPY, TLT, GLD, EEM` -- the four trend sleeves of
the sibling `../weather-test`'s book **F**, taken unchanged so the two studies
are directly comparable.

**The constituent universe (S14).** The fourteen tickers the brief named,
verbatim:

```
AAPL  MSFT  NVDA  AMZN  GOOGL  META  TSLA  JPM  JNJ  WMT  XOM  UNH  V  AVGO
```

Every one resolved and every one has a bar on every date of the primary window.
**None was dropped.**

**The long-window subset (S10).** Declared rule: *every member of S14 whose first
available bar is on or before the long window's start date, 2005-09-02.* This is
a **listing-date** rule, not a performance screen. It yields:

```
AAPL  MSFT  NVDA  AMZN  GOOGL  JPM  JNJ  WMT  XOM  UNH
```

Excluded by listing date only: `META` (first bar 2012-05-18), `TSLA`
(2010-06-29), `V` (2008-03-19), `AVGO` (2009-08-06).

**The sleeve rule.** Long when the close is above its own 200-day simple moving
average; flat otherwise; the position may only change on a book date; equal
weights; rebalanced on the first session of each calendar month. Unchanged from
the sibling studies, and verified against them in `RESULTS.md` §11.

**The inverse-volatility rule.** Weight proportional to 1 / (trailing 60-day
sample standard deviation of the sleeve's own daily return), clamped to
[0.5x, 3.0x] equal weight, with the excess mass redistributed by water-filling.
The standard deviation is measured over the 60 book days **strictly before** the
rebalance date, so the weights set on the close of day *j-1* use only
information available at that close.

**The windows.**

| window | span | days | years | built from | contains 2008 |
|---|---|---|---|---|---|
| **W14** (primary) | 2013-03-07 .. 2026-10-14 | 3422 | 13.6 | intersection of the prices in S14 + NARROW3 + CROSS4 | no |
| **W10** (long) | 2005-09-02 .. 2026-10-14 | 5310 | 21.1 | intersection of the prices in S10 + NARROW3 + CROSS4 | **yes** |
| W3LONG | 2001-03-13 .. 2026-10-14 | 6436 | 25.6 | intersection of NARROW3 | yes |
| WSPY | 1993-11-11 .. 2026-10-14 | 8286 | 32.9 | SPY alone | yes |

Each window starts on the last date on which **every** sleeve's SMA-200 rule is
computable. W14 is short only because `META` did not list until 2012 -- that is
why W10 exists.

**The time split.** The 70th percentile of book days. Nothing is fitted, so the
split is a robustness check rather than a holdout in the machine-learning sense.

**The cost levels.** `0, 2, 4, 20, 50` basis points round trip, plus the two
measured/declared group-specific levels derived in `RESULTS.md` §7.

**The horizon buckets.** `D, W, 2W, M, Q, H, Y`, restricted to **complete**
periods only -- a period is complete when its whole calendar span lies inside
the window.

---

## 3. How to re-run

```bash
cd skills/14-finance/equity-trading-playbook/examples/narrow-universe-test
export PYTHONIOENCODING=utf-8

py -3 study.py            # ~20 s.  Writes out/*.csv and prints every table.
py -3 handcheck.py        # ~2 s.   Independent re-derivation; exits non-zero
                          #         if any gap exceeds 1e-6.
py -3 make-results.py     # rebuilds RESULTS.md from the two captured streams
```

`study.py` needs no network. It needs `data/*.csv` (committed) and the sibling
engine at `../../timeframe-performance-statistics/scripts/timeframe_stats.py`.

### Re-pulling the data from scratch

Repulling is a manual, two-step process because the MCP tool is not callable
from inside a script:

```bash
# 1. In the agent session, call mcp__tradingview__mcp-tv-get-ohlcv once per
#    symbol.  The host persists each large payload to
#    <session>/agents/<id>/tool-results/mcp__tradingview__mcp-tv-get-ohlcv-*.txt
#    The exact arguments used are recorded in README §4.
# 2. Turn those payloads into the CSVs:
py -3 pull_ohlcv.py --results "<tool-results dir>" --out data \
    --pull-date 2026-10-14
py -3 reuse_sibling_data.py      # re-verify and reuse the sibling series
```

`reuse_sibling_data.py` refuses to overwrite a local CSV that disagrees with the
sibling on any overlapping row, and prints the count of identical rows when it
does not.

### Determinism

`study.py` is stdlib-only, uses no randomness, and sorts every symbol list. Two
consecutive runs were diffed: **identical stdout, byte-identical `out/*.csv`**.
That check is reproducible:

```bash
py -3 study.py > /tmp/a.txt && py -3 study.py > /tmp/b.txt && diff /tmp/a.txt /tmp/b.txt
```

---

## 4. The exact pull calls

Every price series was requested as:

```
mcp__tradingview__mcp-tv-get-ohlcv(
    symbol=<see below>, interval="1D", count=8000,
    date_from=<see below>, date_to="2026-10-14", format="columns")
```

| series | source symbol | `date_from` | rows obtained | first bar |
|---|---|---|---|---|
| AAPL | `NASDAQ:AAPL` | *(none)* and `2004-01-01` | 8000 | 1994-12-30 |
| MSFT | `NASDAQ:MSFT` | `2010-01-01`, `2004-01-01` | 5732 | 2004-01-02 |
| NVDA | `NASDAQ:NVDA` | `2010-01-01`, `2004-01-01` | 5732 | 2004-01-02 |
| AMZN | `NASDAQ:AMZN` | `2010-01-01`, `2004-01-01` | 5732 | 2004-01-02 |
| GOOGL | `NASDAQ:GOOGL` | `2010-01-01`, `2004-01-01` | 5574 | 2004-08-19 |
| META | `NASDAQ:META` | `2010-01-01`, `2004-01-01` | 3622 | 2012-05-18 |
| TSLA | `NASDAQ:TSLA` | `2010-01-01`, `2004-01-01` | 4099 | 2010-06-29 |
| JPM | `NYSE:JPM` | `2010-01-01`, `2004-01-01` | 5732 | 2004-01-02 |
| JNJ | `NYSE:JNJ` | `2010-01-01`, `2004-01-01` | 5731 | 2004-01-02 |
| WMT | `NASDAQ:WMT` | `2010-01-01`, `2004-01-01` | 5732 | 2004-01-02 |
| XOM | `NYSE:XOM` | `2010-01-01`, `2004-01-01` | 5731 | 2004-01-02 |
| UNH | `NYSE:UNH` | `2010-01-01`, `2004-01-01` | 5732 | 2004-01-02 |
| V | `NYSE:V` | `2010-01-01`, `2004-01-01` | 4673 | 2008-03-19 |
| AVGO | `NASDAQ:AVGO` | `2010-01-01`, `2004-01-01` | 4324 | 2009-08-06 |

The `2004-01-01` requests were issued so that S10 (the "present for the whole
long window" basket) would be computable. Payloads were merged per symbol and
de-duplicated on the session date; any OHLC disagreement between two payloads of
the same symbol aborts the merge. None occurred: `pull-output.txt` reports the
collapsed duplicate counts.

SPY, QQQ, IWM, TLT, GLD, EEM, VIX, US03M and BIL were **not** re-pulled. They
were reused from `../frontier-test/data/` after `reuse_sibling_data.py` verified
them row-by-row: `reuse-verify-output.txt` reports **0 differing rows** across
all nine series and **71,938 overlapping rows**.

### The quote snapshot

One `mcp__schwab__get_quotes` call for all 17 symbols at one instant, transcribed
into `data/cost-quotes.csv`. The quote payload was small enough that the agent
host did not spill it to disk, so there is no file to re-parse -- the CSV header
says so in as many words. The transcription is **verified in the run**:
`study.py` §0.2 compares each quote's session high and low against the final
TradingView bar's high and low. **All 17 match to within $0.02**, which confirms
the snapshot describes the same session as the price data.

---

## 5. What the hand-check caught

`handcheck.py` is not decoration. Writing it found four real defects, all fixed
before the reported run, all listed here because a reader deserves to know what
the verification actually did:

1. **The cash series was shrinking the book calendar.** `TVC:US03M` is a yield
   index with no print on 483 of the primary window's trading days (14.1%).
   Intersecting the book's calendar on it silently deleted those days, and
   because cash accrues one day of quoted yield per *book* day, it under-accrued
   cash by ~14%. Cash CAGR read 1.602% instead of 1.871%. Every book's
   excess-over-cash was overstated. Fixed: the window is built from **price**
   instruments only; `cash_returns()` carries the last known rate forward.
2. **Buy-and-hold books were re-simulated through the trend path.** `W14_BH_SPY`
   and `W14_N3_BH` returned the *trend* book's numbers at every cost level. Fixed
   with an explicit `sim_kind` dispatch, and §7.1 now shows buy-and-hold books as
   having zero flips.
3. **The inverse-volatility cap was being violated.** A single clamp-and-
   renormalise let a name that had been capped at 3x equal weight drift back to
   4.42x. Fixed with water-filling; §4.2 now asserts the cap binds and prints
   how often. The bound is verified over the entire weight path, not one
   rebalance.
4. **The CSV writer did not quote fields containing commas.** Several weight
   descriptions contain a comma, so they shifted every following column by one
   -- which is exactly how `handcheck.py` noticed. Fixed with RFC-4180 quoting.

Two further bugs were found and fixed without the hand-check's help, both caught
by reading the output: a regime-cell table that reported degenerate cells
(a trend x vol grid has one cell with a single day in it, because SPY's trend
state and SPY's vol tercile are not independent), and a frontier section that
reported "100% positive years" for every book at zero exposure -- which is true
and useless, so the section now reports the *return* at which the 100% is bought.

---

## 6. Limitations -- what this study cannot tell you

Read this section before quoting any number in `FINDINGS.md`.

**Survivorship bias in every constituent result.** The fourteen names are
*today's* large caps. They are the companies that grew into the index, chosen
with hindsight. Their record is not what a fourteen-name draw from the index
would have produced. `RESULTS.md` §4.6 bounds this by removing the three
best-returning names -- but the remaining eleven are also survivors, so the bound
is partial. A clean control needs the index's *historical* membership, which this
data source does not expose. **No conclusion about a broad universe should rest
on the level of any basket return here; only the covariance and dispersion
statements are reasonably immune.**

**Equal weighting vs cap weighting.** Every basket here is equal-weighted while
the index is cap-weighted. Equal-weighting a cap-weighted index has its own
long-run return effect, and this study cannot separate that from the selection
effect.

**Price only, no dividends.** SPY's dividend yield alone is worth roughly 1-1.5%
a year over this window. Every equity CAGR below is therefore understated, and
understated *differently* per instrument (the constituents pay less than SPY did).
The comparisons between rules on the same instrument are unaffected; the
comparisons between instruments are not clean.

**The cash series is an upper bound, not a tradable return.** A yield index
ignores management fees, the bid/offer and roll of an actual T-bill portfolio,
and it credits the full quoted yield every business day. Treat every
"excess over cash" figure as slightly optimistic.

**Costs are estimated from a single closing snapshot.** One observation of a
noisy quantity, taken at the moment of the day when spreads are widest. Ten of
the seventeen quotes sit outside their own session's high/low range, meaning they
are stale or extended-hours. The study therefore reports both the measured
snapshot and a declared published-style alternative, and carries both forward.
It does **not** claim a precise cost.

**No option data.** The hypothesis mentions trading options on a narrow universe.
This study contains **no option quotes, no implied volatilities and no option
P&L**. It measures the *equity* universe question only. §6 of `RESULTS.md` is an
explicit proxy for dispersion, not a dispersion trade.

**One snapshot of one market regime.** 13.6 and 21.1 years of US equity, one
country, one currency.

**The regime grid is degenerate by construction.** SPY's realised-vol tercile and
SPY's trend state are strongly dependent: the calmest tercile contains exactly
**one** down-trend day in the whole window. A trend x vol grid therefore cannot be
populated evenly, and §5 counts negative cells only over cells with at least 60
days.

**Nothing is fitted, so nothing is optimised.** That is a virtue for honesty and
a limit on what can be concluded: the pre-registered rule is one rule, not the
best rule. A reader who would have chosen a different SMA window or a different
rebalance frequency is owed the observation that this study did not test that.

---

## 7. Files

| file | what it is |
|---|---|
| `study.py` | the study. stdlib only, deterministic, LF output. |
| `handcheck.py` | independent re-derivation. Does not import `study.py`. Exits non-zero on any gap > 1e-6. |
| `make-results.py` | builds `RESULTS.md` from the two captured streams. |
| `pull_ohlcv.py` | MCP payload on disk -> `data/*.csv`, with provenance headers. |
| `reuse_sibling_data.py` | verifies and reuses the sibling studies' series. |
| `data/*.csv` | every input series, provenance in the header. |
| `out/*.csv` | every machine-readable result table. |
| `run-output.txt` | complete captured stdout of `study.py`. |
| `handcheck-output.txt` | complete captured stdout of `handcheck.py`. |
| `pull-output.txt`, `reuse-output.txt`, `reuse-verify-output.txt` | the data lineage, verbatim. |
| `RESULTS.md` | all tables verbatim. |
| `FINDINGS.md` | the honest narrative. |
