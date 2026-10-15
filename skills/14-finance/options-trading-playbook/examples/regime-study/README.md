# Regime study — mean reversion and the volatility premium on real prices

A real-data study of three pre-registered long-only mean-reversion rule sets and a
short-volatility proxy, across four index ETFs (plus the VIX), over the full available
daily history. It answers, with numbers, which strategy makes money across years,
timeframes and market regimes — **including where each one loses**.

- `RESULTS.md` — every headline metric, the regime grid, per-year tables with losses,
  the vol-premium tables, the parameter-fishing before/after, and the all-weather verdict.
- `FINDINGS.md` — the honest narrative: what the proxy cannot tell you, what was not
  tested, and what would change the conclusions.
- `run.txt` — the complete captured stdout of one `study.py` run (every figure in
  `RESULTS.md` is pasted from this file).
- `hand-check.txt`, `source-check.txt` — the two verification runs.

---

## 1. Pull date

All price data was pulled **2026-10-14** (provenance header in each CSV carries the
exact UTC timestamp; e.g. `data/SPY_1d.csv` → `2026-10-14T23:23:41Z`).
Last bar in every series: **2026-10-14**.

---

## 2. Sources and why each is used

| Series | File | Source | Adjustment |
|---|---|---|---|
| SPY, QQQ, IWM, EEM | `data/<SYM>_1d.csv` | Yahoo Finance chart JSON API, full history | split-adjusted traded OHLC (`close_tr` = total-return close) |
| VIX | `data/VIX_1d.csv` | Yahoo Finance chart JSON API `^VIX` | unadjusted index level |
| SPY, QQQ, IWM, EEM | `data/<SYM>_1d_moomoo.csv` | moomoo vendor feed via local OpenD (127.0.0.1:11111) | forward-adjusted (qfq) |
| cross-check fixtures | `data/_tvcheck_VIX.csv`, `data/_tvcheck_SPY.csv` | `mcp__tradingview__mcp-tv-get-ohlcv`, copied verbatim | as served (split-adjusted) |

> **The two `_tvcheck_*.csv` fixtures are captured by hand, not downloaded.**
> `pull_data.py` cannot recreate them — they are the verbatim bars arrays from a
> `mcp__tradingview__mcp-tv-get-ohlcv` call, and that tool's result cannot be written to
> disk by a script. If you delete `data/` you must re-capture them before
> `verify_sources.py` can certify anything; the exact calls are recorded in the header
> comment of each fixture file, and `verify_sources.py` prints them and exits non-zero
> when they are missing.

**Why Yahoo is the primary series.** It carries the full history, which the study needs
because the point is regimes across decades:

| symbol | bars | first | last | study window (needs SMA200 + a 20-day slope) |
|---|---|---|---|---|
| SPY | 8,485 | 1993-01-29 | 2026-10-14 | 1993-12-13 → 2026-10-14 |
| QQQ | 6,943 | 1999-03-10 | 2026-10-14 | 2000-01-21 → 2026-10-14 |
| IWM | 6,635 | 2000-05-26 | 2026-10-14 | 2001-04-11 → 2026-10-14 |
| EEM | 5,914 | 2003-04-14 | 2026-10-14 | 2004-02-27 → 2026-10-14 |
| VIX | 9,266 | 1990-01-02 | 2026-10-14 | — |

**Two sources that were tried and did not serve this study:**

- **The moomoo VIX index.** `US.VIX` returns `ret=-1` on the local OpenD kline channel,
  and the hosted `mcp__moomoo__quote_history_kline` tool rejects the call on its
  `ktype`/`autype` enums regardless of whether they are passed as integers or strings.
  VIX therefore comes from Yahoo `^VIX` and is cross-checked against TradingView.
- **The moomoo feed as a primary equity source.** It serves only ~20 years (it starts
  2006-10-02) and contains repeated identical closes on some liquid-ETF sessions
  (SPY 2011-08-01/02/03 all read 105.0795 while the market moved ~2.5%). It is kept as
  an audit trail and compared on *returns*, not levels.

---

## 3. Commands — how to re-run

Everything is stdlib + the local OpenD channel. `python3` is not on PATH here; use `py -3`.

```bash
cd skills/14-finance/options-trading-playbook/examples/regime-study
export PYTHONIOENCODING=utf-8

# 1. pull (or refresh) the price data -> data/*.csv with provenance headers
py -3 pull_data.py
py -3 pull_data.py --check          # row count + date range per file, no download

# 2. prove the data is real and pick the source to trust
py -3 verify_sources.py             # exit 0 = primary series certified by TradingView

# 3. the study: full report to stdout, tables to out/
py -3 study.py > run.txt            # > run.txt is what makes RESULTS.md reproducible
py -3 study.py --no-tables          # stdout only
py -3 study.py --dump-trades M1:SPY:2018   # one strategy-year's trades, for hand-checking

# 4. hand-check the trade statistics with longhand arithmetic
py -3 verify_metrics.py             # exit 0 = hand arithmetic == study.py, on 13 quantities

# 5. rebuild RESULTS.md by slicing run.txt (so the report cannot drift from the run)
py -3 make_results.py
```

Determinism: `study.py` contains no randomness, no wall-clock reads and no
dict-order dependence. Three consecutive runs are **byte-identical** (`run.txt` is the captured output;
`diff` on two fresh runs and a `cmp` against `run.txt` are both clean).

---

## 4. Verification status

| Check | Result |
|---|---|
| Primary SPY vs TradingView `AMEX:SPY` (10 overlapping sessions) | worst \|diff\| **$0.0000** — exact |
| Primary VIX vs TradingView `TVC:VIX` (30 overlapping sessions) | worst \|diff\| **$0.0100** |
| Yahoo vs moomoo daily returns (4 ETFs, ~5,000 pairs each) | median diff **0.0000 pp**, p95 0.03 pp, worst 2.56 pp |
| Hand-computed `p, b, E, p*, b*, sd, n_req, L, t` vs `study.py` (M1/SPY/2018) | **13/13 agree to 1e-9** |
| Determinism (3 runs) | **byte-identical** |
| Output tables | `out/*.csv`, row counts as expected (grids 30 and 56) |

---

## 5. Layout

```
regime-study/
├── README.md                  this file
├── RESULTS.md                 the numbers (generated from run.txt)
├── FINDINGS.md                the honest narrative
├── run.txt                    full captured output of study.py
├── hand-check.txt             captured output of verify_metrics.py
├── source-check.txt           captured output of verify_sources.py
├── trade-dump-M1-SPY-2018.txt captured output of study.py --dump-trades
├── pull_data.py               downloads the CSVs
├── verify_sources.py          cross-checks the vendors
├── study.py                   indicators, rule engine, metrics, regimes, proxy, grids
├── verify_metrics.py          longhand hand-check of the statistics
├── make_results.py            slices run.txt into RESULTS.md
├── data/                      price CSVs with provenance headers
└── out/                       machine-readable result tables
```

`data/` is generated by `pull_data.py`; `out/` and `RESULTS.md` are generated by
`study.py` and `make_results.py`. Delete them and re-run the commands in §3 to rebuild.
