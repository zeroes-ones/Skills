# weather-test — does a genuinely diversified, un-optimised book survive every year?

A pre-registered, run-once test of the one question the two sibling regime
studies left open: **can sleeves that are genuinely uncorrelated be combined, at
fixed weights nobody tuned, into a book that makes money in every year and never
draws down badly?**

- **Pull date / study date:** 2026-10-14 (UTC).
- **Book window:** 2005-09-02 .. 2026-10-14 — 5,311 trading days, 21.1 years.
- **Headline answer:** diversification worked; the book did not. See
  [`FINDINGS.md`](FINDINGS.md). Every table is in
  [`RESULTS.md`](RESULTS.md), sliced out of `run-output.txt` by
  `make-results.py`.

## The two studies this builds on, and what it adds

| study | what it established |
|---|---|
| `skills/14-finance/equity-trading-playbook/examples/regime-study` | no single rule set is profitable in every year or every regime, on real daily data 1993-2026 |
| `skills/14-finance/options-trading-playbook/examples/regime-study` | the mean-reversion / vol-premium corner, including the corrected variance-risk-premium finding |
| **this study** | the sleeves those studies tested were **0.666-0.887** correlated year to year — one bet, not several — so they could not be combined. **This** study tests sleeves chosen to be structurally different, at **pre-registered fixed weights**, and reports the worst year and worst drawdown. |

## The pre-registered book (fixed before the first number was produced)

Equal-risk, **20% each**, rebalanced monthly, on a single book. These weights
were not searched, tuned, or adjusted at any point. The only place a weight is
optimised anywhere in this directory is §11 of `RESULTS.md`, which is explicitly
labelled as the fitted comparison **and is not the recommendation**.

| id | sleeve | instrument | rule |
|---|---|---|---|
| A | equity trend | `AMEX:SPY` | long when close > SMA(200), else flat |
| B | bond trend | `NASDAQ:TLT` | long when close > SMA(200), else flat |
| C | gold trend | `AMEX:GLD` | long when close > SMA(200), else flat |
| D | ex-US equity trend | `AMEX:EEM` | long when close > SMA(200), else flat |
| E | long volatility | `TVC:VIX` | long when VIX > SMA(50), else flat |

Comparisons, same construction: **F** = the four trend sleeves A-D at 25% each,
no vol sleeve. **G** = 100% buy-and-hold SPY.

### Sleeve E is a signal, not a tradable instrument — read this first

The VIX index cannot be bought. Sleeve E's return is the day-over-day change in
the **VIX index level** while the rule is long. No VIX futures, no futures-based
ETN, no roll cost, no fee, no borrow is modelled anywhere in this study. A real
long-volatility position is a futures position, and futures bleed on roll in
contango — a cost this proxy does not carry. **Every number from sleeve E is an
upper bound on the signal, not a return anybody could have earned.** It is
reported anyway because "does a crisis sleeve decorrelate the book" is worth
answering even when the tradable form is unavailable. Drop E and the book is
portfolio F, whose row is in every table.

## What was pulled

| instrument | source symbol | interval | first bar | last bar | bars in file | pages merged | source of the file |
|---|---|---|---|---|---|---|---|
| SPY | `AMEX:SPY` | 1D | 1993-01-29 | 2026-10-14 | 8,485 | 3 | copied byte-identical from the sibling regime study |
| TLT | `NASDAQ:TLT` | 1D | 2002-07-26 | 2026-10-14 | 6,094 | 1 | copied byte-identical from the sibling regime study |
| GLD | `AMEX:GLD` | 1D | 2004-11-18 | 2026-10-14 | 5,510 | 1 | copied byte-identical from the sibling regime study |
| EEM | `AMEX:EEM` | 1D | 2003-04-11 | 2026-10-14 | 5,915 | 1 | **pulled for this study** |
| VIX | `TVC:VIX` | 1D | 1990-01-03 | 2026-10-14 | 9,283 | 2 | **pulled for this study** |

**Price-only, all five. No dividends, no distributions.** SPY, TLT, GLD and EEM
all pay distributions that these series exclude. The sibling study measured
**TLT's price multiple over its own window at 0.9561** — the fund's *price* ends
*below* where it started, because the coupons that produced its actual return are
not in a price series. So any always-long bond exposure is understated here, and
the always-long comparison sleeve G is understated most of all. Every CSV carries
a `# PROVENANCE:` header naming the source, the pull date, the interval, the page
count and the row count, so a CSV can never be separated from where it came from.

### Exact calls

Primary source — TradingView MCP, one call per page:

```
mcp__tradingview__mcp-tv-get-ohlcv(
    symbol    = "AMEX:EEM" | "TVC:VIX",
    interval  = "1D",
    count     = 8000,             # the per-response column cap
    format    = "columns",        # ~40% smaller than row form, and the paging form
    date_from = "2003-01-01" | "1990-01-01",
    date_to   = "2026-10-14")     # then date_to = <next_date_to> until has_more=false
```

VIX needed two calls (the response holds at most 8,000 bars as columns; the VIX
window is 9,283 bars). EEM came back in one call with `has_more=false`. The three
ETF series were **not** re-pulled: they were copied byte-identical from
`../regime-study/data/` and an extra `# PROVENANCE: copy_of=...` line was added.

The agent host persists a large tool result to
`<session>/agents/<id>/tool-results/*.txt` (whole file = one JSON payload).
`pull_ohlcv.py` reads those already-on-disk bytes and turns them into CSV — it
makes no network call of its own, and it groups pages by the payload's own
`symbol` field and refuses to merge two pages that disagree on a shared date.

## Reproduce

`py -3` is the interpreter on this machine (`python3` is not on `PATH`); the
scripts are stdlib-only and were run under Python 3.10.11.

```bash
cd skills/14-finance/equity-trading-playbook/examples/weather-test
export PYTHONIOENCODING=utf-8

# 1. extract the already-pulled MCP payloads into data/*.csv   (no network)
#    Only EEM and VIX: SPY/TLT/GLD are copied from the sibling study.
py -3 pull_ohlcv.py \
    --results "$SESSION/agents/$AGENT/tool-results" \
    --out data --pull-date 2026-10-14 --only VIX,EEM

# 2. the analysis (deterministic; reads only data/*.csv). ~19 s.
py -3 study.py > run-output.txt

# 3. independent verification of the book arithmetic
py -3 handcheck.py --year 2013 > handcheck-output.txt

# 4. rebuild RESULTS.md from the real run's stdout
py -3 make-results.py
py -3 make-results.py --check        # freshness gate
```

Step 0 (re-issuing the MCP calls) needs the network. Steps 1-4 read only what is
committed in this directory. `study.py --no-grid` skips the 1001-book
optimisation sweep and finishes in ~5 s.

## Files

| file | what it is |
|---|---|
| `data/SPY_1d.csv`, `TLT_1d.csv`, `GLD_1d.csv` | copied byte-identical from the sibling regime study, with a `copy_of` provenance line added |
| `data/EEM_1d.csv`, `VIX_1d.csv` | pulled for this study, with full provenance headers |
| `pull_ohlcv.py` | MCP-payload-on-disk → CSV, with provenance; merges pages, de-duplicates, refuses conflicts |
| `study.py` | the analysis: pre-registered sleeves, the book, per-sleeve and portfolio metrics, the correlation matrix, rolling-window standards, costs, and the labelled optimisation comparison |
| `handcheck.py` | an **independent** re-derivation that does not import `study.py` |
| `make-results.py` | slices `RESULTS.md` out of `run-output.txt`; `--check` is the freshness gate |
| `run-output.txt` | the **complete raw stdout** of `study.py` — the source of every figure in `RESULTS.md` |
| `handcheck-output.txt` | the verification evidence, verbatim |
| `pull-output.txt` | what the pull wrote |
| `RESULTS.md` | every table (generated; do not hand-edit) |
| `FINDINGS.md` | the honest narrative: what diversification bought, what it did not, and what is untested |
| `out/*.csv` | machine-readable versions of the reported tables, plus `book_daily.csv` (the book's daily weights, sleeve returns and equity) and `sleeve_monthly.csv` |

## Execution model — stated once, because every number depends on it

- **No look-ahead.** The signal is read at the close of a book date and the
  position it implies is held from the next book date. Concretely, the return
  earned on day *t* is `pos(close of previous book date) x (close[t]/close[previous book date] - 1)`.
- **A position may only change on a book date.** The equity instruments and the
  VIX index do not share an identical calendar: the CBOE trades on Good Friday
  when NYSE does not, and VIX carries 22 date stamps inside this window that the
  equity instruments do not have. A date an instrument has no bar for contributes
  a return of exactly 0.0 and carries the previous position; a bar of its own
  that falls *between* two book dates may not change the position, because the
  book could not have acted on it. Its price move is still counted in full — the
  next book date measures the return from that bar's close.
- **Warm-up.** A sleeve is FLAT until its moving average exists. The book
  therefore starts on the first date on which **every** sleeve's rule is
  computable (gold's SMA(200) on 2005-09-02 is the binding one), so that day one
  is a real five-sleeve book rather than a book with a hole in it.
- **Monthly rebalance** to the pre-registered weights. Between rebalances each
  sleeve holds its own dollars and the weights drift; at the first day of a new
  calendar month each sleeve is reset to its target share of the book. This makes
  the book's monthly return exactly `0.20*rA + 0.20*rB + 0.20*rC + 0.20*rD + 0.20*rE`
  when measured from the sleeve monthly returns — an identity, and the by-hand
  check in `handcheck.py` is built on it.
- **Costs are OFF** except in §10, where they are turned on at 5 and 20 bps round
  trip. A round-trip rate *c* bps means each side costs *c*/2 bps of the notional
  traded: charged on every position flip, and on each monthly rebalance's one-way
  turnover. The cost is charged against the **return**, not against a sleeve's
  value — charging it against a value does nothing, because the weights are
  renormalised every day and a haircut on one sleeve changes the mix while
  leaving the level alone. (That mistake was made during development, produced a
  cost drag of 0.4 bps where the true drag is 111 bps, and is recorded here
  because a bug that flatters costs is exactly the kind that survives a review.)
- **Sharpe convention:** daily simple returns, full sample, Rf = 0, x sqrt(252).
- **Max drawdown (headline):** compounded peak-to-trough of the equity curve, as
  a negative fraction — the same definition and code shape the sibling regime
  study used, so the two studies' drawdown columns compare directly.
- **Max drawdown (additive):** the sibling engine's `max_drawdown()` on the daily
  return series — peak-to-trough of the cumulated returns. Quoted for the book
  once, to show the two measures are different quantities.
- **Rolling windows** are trailing **trading-day** windows (252 days = "1y"),
  measured on the compounded equity curve, over every window ending on a book day.

## Which parts of the toolchain this reuses rather than reimplements

`study.py` **imports** the sibling engine

```
skills/14-finance/timeframe-performance-statistics/scripts/timeframe_stats.py
```

and calls its `bucket_key()`, `aggregate_bucket()`, `sample_sd()`,
`max_drawdown()`, `lag1_autocorr()` and `n_effective()`, and its
`T_STAT_NOISE_BAND` verdict threshold. If that file moves, `study.py` fails loudly
instead of substituting its own formulae.

## Verified before publishing

| check | result |
|---|---|
| CSV row counts match the source | 8,485 / 6,094 / 5,510 / 5,915 / 9,283 — all equal to the bar counts returned |
| CSV integrity | no duplicate dates, strictly monotonic, **no weekend dates**, no OHLC-invariant violations, across all 35,287 bars |
| Calendar alignment | 4 equity series carry every one of the 5,311 book dates; VIX has 22 extra date stamps, handled explicitly, not silently dropped |
| `study.py` determinism | run twice → **byte-identical stdout**, byte-identical `out/*.csv` (10 files hashed), identical `data/` hashes |
| `handcheck.py` determinism | run twice → byte-identical stdout |
| Independent re-derivation of the book | worst day-by-day equity difference **5.0e-11** over 5,311 days, from an implementation that does not import `study.py` |
| By-hand one-year book return, 2013 | **-25.2651%** by hand from the sleeve monthly returns and the 0.20 weights; `study.py` says **-25.2651%**; gap 4.7e-07 (the CSV's own 10-decimal rounding) |
| Correlation matrix | symmetric (all 15 pairs agree both ways, worst gap 0.0), unit diagonal exact |
| One sleeve-year from prices, no reuse | sleeve A 2013 = **+29.6889%** recomputed straight from `data/SPY_1d.csv`; `out/sleeve_yearly.csv` says +29.6889% |
| `make-results.py` freshness | `--check` reports `RESULTS.md` current |

## Known limits of this study

Stated here as well as in `FINDINGS.md` and §12 of `RESULTS.md`, because they
bound every number above:

- **Sleeve E is not tradable** (see above). Its numbers are an upper bound.
- **Price-only.** No distributions anywhere; the bond sleeve and buy-and-hold are
  understated.
- **Long only, no leverage, no shorts.** The book can stand aside; it cannot go
  short a downtrend.
- **One parameter set.** SMA(200) and SMA(50) were fixed before the run. This
  study does not show that 200 beats 150, and does not rule it out.
- **One window, and a favourable one.** The book needs all five series, so it
  starts in 2005 and therefore misses 1993-2004 entirely. Sleeve A and sleeve G
  are additionally shown on full history for that reason. The window is dominated
  by the post-2009 bull market, which flatters every long-only sleeve and the
  always-long comparison most.
- **Five sleeves, four of them the same rule on different instruments.** §5
  measures how much that actually diversifies; that measurement is the answer to
  "is this four bets or one".
- **No costs** outside §10, and the §11 grid is run gross.
- **Thin evidence for the year-level statements.** 20 complete years, and the
  engine's `n_eff` says the yearly series carry less independent information than
  20 suggests (gold's is 13.6). The rolling-window table in §9 is the honest
  version of "how often".
- **The last bar was still forming** at pull time and may revise.

## Scope

Only this directory was created. No `SKILL.md` was modified, and no other
skill's files were touched. `../regime-study/data/*.csv` were read (copied) but
not modified.
