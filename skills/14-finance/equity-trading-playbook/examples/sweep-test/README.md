# sweep-test -- how many of a few thousand real configurations are actually positive?

**The question.** The instruction that produced this directory was *"run as many
iterations as you want to show +ve numbers"*. That instruction is satisfiable by
construction: enough configurations always contain green rows. So the question
this study answers is the one that instruction hides:

> Among hundreds of real configurations, how many are genuinely positive rather
> than positive by selection, and what is the maximum fraction of market
> conditions any of them is positive in?

**What this is not.** Nothing here is a strategy recommendation. The one
configuration printed as a strategy is the *pre-registered default* -- fixed
before the first number was produced -- and it is printed because it is the
benchmark, not because it won. The maximum-positivity configuration is named
because the owner asked for it, and it is named together with its losing years.

**Pull date / study date:** 2026-10-14 (UTC). Last bar in every series:
**2026-10-14**.

---

## 1. The design, declared before any result was looked at

Everything in this section is a constant in `study.py`, written above every
computation that reads it. The grid is counted, printed, and then asserted
against the number of configurations actually run (`SECTION 1c` of a run).

| element | declaration |
|---|---|
| signal | close vs an N-day simple moving average; **long when close > SMA(N), flat otherwise** |
| execution | the signal is read at a close and the position it implies is held from the **next** session. No look-ahead anywhere |
| N | 50, 100, 150, 200, 250 |
| universe (Grid P) | SPY, QQQ, IWM, EEM, TLT, GLD, EFA, VNQ -- one single-instrument trend sleeve each |
| cross-asset books | **every** 2-, 3- and 4-instrument subset of those sleeves, equal weight -- all 28 + 56 + 70 combinations, not a hand-picked few |
| rebalance | **daily** and **monthly** |
| declared size | (8 singles + 28 + 56 + 70 books) x 5 N x 2 modes = **1,620 configurations** |
| pre-registered default | SPY+QQQ+IWM+EEM at N=200, monthly -- chosen on instrument *coverage* (longest common history, widest breadth), not on performance; with a 4-instrument cap on a book it is the largest all-equity book the grid contains |
| second reference | SPY alone at N=200, monthly -- the textbook single-instrument rule |

Two further grids are declared in the same file, to test whether the
conclusions are an artifact of the universe or the window:

| grid | universe | window starts | declared size |
|---|---|---|---|
| **P** (primary) | the 8 instruments above | 2005-11-14 (the 250th bar of the last instrument to list) | **1,620** |
| **L** (long window) | SPY, QQQ, IWM, EEM | 2004-04-07 | **150** |
| **X** (extended universe) | the 8 above **+ IEF, HYG, DBC** | 2008-04-07 | **5,610** |

**Every configuration in a grid is evaluated on the same sessions.** The calendar
is the intersection of that grid's instruments' trading dates, sliced to start
after the longest moving average in the grid exists for every instrument, so no
configuration gets a head start and none is measured over a different window.

**Periods.** "Positive years" counts **complete calendar years only** -- a year,
quarter or month counts only if the evaluation window covers its entire calendar
span -- so the partial first and last periods can never be counted as wins.

**Metrics.**
- CAGR: compounded equity, calendar-time exponent (`365.25` days per year).
- Max drawdown: peak-to-trough of the **compounded** equity curve, quoted as a negative fraction.
- Sharpe: daily simple returns, full sample, **Rf = 0**, x `sqrt(252)`, sample sd (`ddof=1`).
- Worst year: minimum complete-calendar-year return.
- Losing regime cells: cells of the SPY trend-state x realised-vol-tercile grid (2 x 3, six cells) whose mean daily return is negative over at least 20 sessions.

**The significance test, stated once.** For each configuration,
`t = mean(daily return) / (sd / sqrt(n_days))`, i.e. annualised Sharpe x sqrt(years).
The family is **all m configurations of the grid counted together**;
`alpha = 0.05` two-sided; the **Bonferroni bar** is
`|t*| = Phi^-1(1 - alpha/(2m))`, computed by Acklam's inverse-CDF approximation.
A stricter variant re-runs the same bar on `t_eff`, which shrinks the sample size
by the measured lag-1 autocorrelation (`n_eff = n(1-rho)/(1+rho)`, taken from the
sibling engine). Both counts are reported.

**Out-of-sample split.** The first 70% of sessions are in-sample, the last 30%
are held out; the held-out data is touched once, on the in-sample ranking. The
top decile by in-sample Sharpe is evaluated on the holdout.

---

## 2. Data: what was pulled, from where, and when

Every series is **split-adjusted, regular-session, PRICE-ONLY** daily OHLCV with
a `# PROVENANCE:` header inside the CSV naming the source symbol, the pull date,
the page count and the row count. Price-only means no distributions anywhere:
TLT, IEF, HYG, VNQ and EEM are understated, and any always-long comparison is
understated most of all.

| stem | source symbol | first bar | last bar | bars | how it got here |
|---|---|---|---|---|---|
| SPY | `AMEX:SPY` | 1993-01-29 | 2026-10-14 | 8,485 | copied byte-identical from `../weather-test/data` |
| QQQ | `NASDAQ:QQQ` | 1999-03-10 | 2026-10-14 | 6,943 | **pulled for this study** |
| IWM | `AMEX:IWM` | 2000-05-26 | 2026-10-14 | 6,635 | **pulled for this study** |
| EEM | `AMEX:EEM` | 2003-04-11 | 2026-10-14 | 5,915 | copied byte-identical from `../weather-test/data` |
| TLT | `NASDAQ:TLT` | 2002-07-26 | 2026-10-14 | 6,094 | copied byte-identical from `../weather-test/data` |
| GLD | `AMEX:GLD` | 2004-11-18 | 2026-10-14 | 5,510 | copied byte-identical from `../weather-test/data` |
| EFA | `AMEX:EFA` | 2001-08-17 | 2026-10-14 | 6,326 | **pulled for this study** |
| VNQ | `AMEX:VNQ` | 2004-09-29 | 2026-10-14 | 5,546 | **pulled for this study** |
| IEF | `NASDAQ:IEF` | 2002-07-26 | 2026-10-14 | 6,094 | **pulled for this study** (Grid X only) |
| HYG | `AMEX:HYG` | 2007-04-11 | 2026-10-14 | 4,910 | **pulled for this study** (Grid X only) |
| DBC | `AMEX:DBC` | 2006-02-03 | 2026-10-14 | 5,206 | **pulled for this study** (Grid X only) |
| VIX | `TVC:VIX` | 1990-01-03 | 2026-10-14 | 9,283 | copied byte-identical from `../weather-test/data` |

The five copied series came from the **same vendor** as the seven pulled here
(`mcp__tradingview__mcp-tv-get-ohlcv`), pulled the same day, and were already
cross-checked against that vendor on overlapping sessions by the sibling studies
that first pulled them. Re-copying rather than re-pulling keeps one audit line
instead of five identical ones; the `copy_of=` line says exactly that.

### Exact calls

```
mcp__tradingview__mcp-tv-get-ohlcv(
    symbol   = "AMEX:EFA" | "AMEX:VNQ" | "AMEX:HYG" | "AMEX:DBC"
             | "NASDAQ:IEF" | "NASDAQ:QQQ" | "AMEX:IWM",
    interval = "1D",
    count    = 8000,        # the per-response column cap
    format   = "columns")   # the paging form, ~40% smaller than rows
```

Each of the seven came back in **one page** with `has_more=false`, so no paging
was needed and no page-merge conflict was possible. The agent host persists each
payload to
`<session>/agents/<id>/tool-results/mcp__tradingview__mcp-tv-get-ohlcv-*.txt`;
`pull_ohlcv.py` reads those already-on-disk bytes and makes no network call of
its own.

---

## 3. Reproduce

`python3` is not on `PATH` on this machine; use `py -3` (Python 3.10.11).
Everything is stdlib -- no PyYAML, no numpy. Steps 1-5 make no network call of
their own; step 0 (re-issuing the MCP calls) and step 3b (re-issuing one small
call per series for the spot-check) do.

```bash
cd skills/14-finance/equity-trading-playbook/examples/sweep-test
export PYTHONIOENCODING=utf-8

# 1. extract the already-pulled MCP payloads into data/*.csv, and copy the five
#    sibling series. No network.
py -3 pull_ohlcv.py \
    --results "$SESSION/agents/$AGENT/tool-results" \
    --out data --pull-date 2026-10-14 \
    --copy-from ../weather-test/data

# 2. the sweep: full report to stdout, tables to out/   (~2 min, all 7,380 configs)
py -3 study.py > run-output.txt
py -3 study.py P > run-output.txt          # primary grid only, ~60 s

# 3. an INDEPENDENT re-derivation that does not import study.py
py -3 handcheck.py > handcheck-output.txt

# 3b. spot-check the CSVs against a fresh vendor call (needs the network)
py -3 verify_sources.py > source-check.txt

# 4. rebuild RESULTS.md from the real run's stdout, and gate its freshness
py -3 make-results.py
py -3 make-results.py --check

# 5. determinism: two fresh runs must be byte-identical, and so must out/*.csv
py -3 study.py > /tmp/a.txt && py -3 study.py > /tmp/b.txt && diff /tmp/a.txt /tmp/b.txt
```

Step 0 (re-issuing the MCP calls) needs the network. Steps 1-6 read only what is
committed in this directory.

---

## 4. What reuses what

| reused | how |
|---|---|
| `skills/14-finance/timeframe-performance-statistics/scripts/timeframe_stats.py` | **imported**, not reimplemented: `sample_sd`, `median`, `lag1_autocorr`, `n_effective`, `bucket_key`. `study.py` fails loudly if the file moves rather than substituting its own formulae |
| `../weather-test/data/{SPY,TLT,GLD,EEM,VIX}_1d.csv` | copied byte-identical, with a `copy_of` provenance line added. **Not modified.** |
| `../options-trading-playbook/examples/regime-study` | the *result this sweep must extend, not contradict*: see `FINDINGS.md` section 4 |
| `../regime-study`, `../weather-test` | the regime-cell convention and the daily/monthly book construction |

No `SKILL.md` was modified and no other skill's files were touched. Files under
`../regime-study/data` and `../weather-test/data` were **read**, not written.

---

## 5. Execution model, stated once, because every number depends on it

- **No look-ahead.** The position held on session *t* is the signal read at the
  close of session *t-1*. The return earned on session *t* is
  `position_t x (close_t / close_{t-1} - 1)`.
- **Monthly mode.** The position may only change on the **first trading day of a
  calendar month**, where it is written from the previous session's signal and
  then carried forward. It is not re-read mid-month, because the book could not
  have acted on a mid-month signal.
- **Warm-up.** A sleeve is FLAT until its moving average exists. The window
  begins on the first session for which **every** instrument in the grid has its
  longest moving average, so day one is a real book rather than a book with a hole.
- **Daily-rebalanced book.** Each sleeve is 1/k of the book at every close, so
  the book return is exactly the mean of the sleeve returns.
- **Monthly-rebalanced book.** Each sleeve is reset to 1/k of the book on the
  first trading day of the month and drifts with its own return between resets.
- **Regime attribution is contemporaneous, not predictive.** The SPY trend state
  and vol tercile are measured *on* the session whose return is attributed to
  them, so the regime grid says "this is where the money was made", not "this is
  what you could have known". Both regime series are computed over the
  instrument's **full history** and then sliced to the window, so the trailing
  volatility window is full on the window's first session — every session in
  every grid therefore carries a regime label.
- **Costs are OFF** except in `SECTION 8`. A round-trip rate *c* bps charges
  *c*/2 bps per side of the traded notional, on every sleeve position flip and on
  each monthly book reset's one-way turnover, and is charged **against the
  return**, not against a sleeve value -- charging it against a value does
  nothing, because the weights are renormalised every day.

---

## 6. Layout

```
sweep-test/
├── README.md                this file -- the design, declared up front
├── RESULTS.md               every table, verbatim from run-output.txt (generated)
├── FINDINGS.md              the honest narrative, including what is not tested
├── run-output.txt           the complete raw stdout of study.py
├── handcheck-output.txt     the independent re-derivation, verbatim
├── source-check.txt         the vendor spot-check, verbatim
├── pull-output.txt          what the pull wrote
├── study.py                 the rule engine, the grids, the Bonferroni bar, the analysis
├── handcheck.py             independent: re-derives the headline numbers, imports nothing from study.py
├── verify_sources.py        last six sessions of five series vs a fresh vendor call
├── pull_ohlcv.py            MCP-payload-on-disk -> CSV with provenance; copies the sibling series
├── make-results.py          slices RESULTS.md out of run-output.txt; --check is the freshness gate
├── data/*_1d.csv            12 price series with provenance headers
└── out/*.csv                machine-readable tables (the full per-configuration grids)
```

## 7. Limits that bound every number

Stated here as well as in `FINDINGS.md` section 7, because they matter:

- **Long-only, long-or-flat.** There is no short leg; the only defence in a
  downtrend is standing aside, and that happens late.
- **Price-only series.** No distributions. Bond, credit, REIT and EM sleeves are
  understated.
- **A favourable window.** Grid P starts in late 2005. Grid L adds 2004-2005.
  Neither reaches the 1990s, because a 4-instrument book needs all four to exist.
- **A kind holdout.** The held-out 30% (2020-07 onward) is a rising market, so
  the measured out-of-sample degradation is a *lower* bound on how badly the
  selection decays.
- **One signal family.** The sweep varies N, the book and the rebalance mode. It
  does not vary the rule.
- **Mixed-N books are not tested.** A book whose sleeves use different moving
  averages is `5^k x C(8,k)` for k = 2, 3, 4 — 700 + 7,000 + 43,750 = **51,450**
  configurations, four times everything run here. It was deliberately not run: it
  would only make the multiple-testing problem worse, so leaving it out is the
  conservative choice.
- **The last bar was still forming** at pull time and may revise.
