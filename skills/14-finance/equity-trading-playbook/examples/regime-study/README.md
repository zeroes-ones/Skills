# regime-study — the trend/momentum corner, on real daily prices

A pre-registered, run-once study of four long-only strategies on four
instruments, over the full daily history the data source would give us.

- **Study date / pull date:** 2026-10-14 (UTC).
- **What it answers:** does any single trend/momentum rule set make money across
  years, timeframes and market regimes — and where does it lose?
- **Headline answer:** no. See [`RESULTS.md`](RESULTS.md) and
  [`FINDINGS.md`](FINDINGS.md).

## What was pulled

| instrument | source symbol | interval | first bar | last bar | bars in file | pages merged |
|---|---|---|---|---|---|---|
| SPY | `AMEX:SPY` | 1D | 1993-01-29 | 2026-10-14 | 8,485 | 3 |
| QQQ | `NASDAQ:QQQ` | 1D | 1999-03-10 | 2026-10-14 | 6,943 | 1 |
| TLT | `NASDAQ:TLT` | 1D | 2002-07-26 | 2026-10-14 | 6,094 | 1 |
| GLD | `AMEX:GLD` | 1D | 2004-11-18 | 2026-10-14 | 5,510 | 1 |

All are **split-adjusted, regular session only**, as the source reports them.
Volume is as reported and is *not* split-adjusted. Each CSV carries a
`# PROVENANCE:` header naming the source, the pull date, the interval, the page
count and the row count, so a CSV can never be separated from where it came from.

> **Source correction, recorded rather than hidden.** The brief named
> `AMEX:TLT`. That symbol does not exist: the tool returned
> `symbol_error [invalid symbol]`. A symbol search resolved TLT to
> **`NASDAQ:TLT`**, and the pull succeeded there. The failed call and the
> resolution are both real and are reported here rather than quietly worked
> around.

### Exact calls

Primary source — TradingView MCP, one call per page:

```
mcp__tradingview__mcp-tv-get-ohlcv(
    symbol   = "AMEX:SPY" | "NASDAQ:QQQ" | "NASDAQ:TLT" | "AMEX:GLD",
    interval = "1D",
    count    = 8000,             # the per-response column cap
    format   = "columns",        # ~40% smaller than row form, and the paging form
    date_from= "1993-01-01" ... "2004-01-01",
    date_to  = "2026-10-14")     # then date_to = <next_date_to> until has_more=false
```

SPY needed three calls (the response holds at most 8,000 bars as columns; SPY has
8,485). The other three came back in one call each with `has_more=false`.

The agent host persists a large tool result to
`<session>/agents/<id>/tool-results/*.txt` (whole file = one JSON payload) and
also appends the raw result to `<session>/agents/<id>/wire.jsonl`. `pull_ohlcv.py`
reads those already-on-disk bytes and turns them into CSV — it makes no network
call of its own.

Cross-check source — Robinhood MCP:

```
mcp__robinhood__get_equity_historicals(
    symbols    = ["SPY", "QQQ", "TLT", "GLD"],
    start_time = "2026-09-01T00:00:00Z",
    interval   = "day")
```

## Reproduce

`py -3` is the interpreter on this machine (`python3` is not on `PATH`); the
scripts are stdlib-only and were run under Python 3.10.11.

```bash
cd skills/14-finance/equity-trading-playbook/examples/regime-study
export PYTHONIOENCODING=utf-8

# 1. extract the already-pulled MCP payloads into data/*.csv   (no network)
py -3 pull_ohlcv.py \
    --results "$SESSION/agents/$AGENT/tool-results" \
    --wire    "$SESSION/agents/$AGENT/wire.jsonl" \
    --out data --pull-date 2026-10-14

# 2. the analysis (deterministic; reads only data/*.csv)
py -3 study.py > run-output.txt

# 3. independent cross-check of the price series against a second feed
py -3 verify_robinhood.py --wire "$SESSION/agents/$AGENT/wire.jsonl" \
                          --pull-date 2026-10-14 > crosscheck-output.txt

# 4. hand-verify the trade-level arithmetic for four strategy-years
py -3 handcheck.py SPY S1 1994   >  handcheck-output.txt
py -3 handcheck.py SPY S1 2000   >> handcheck-output.txt
py -3 handcheck.py SPY S1 2007   >> handcheck-output.txt
py -3 handcheck.py QQQ S1 2000   >> handcheck-output.txt

# 5. rebuild the table portion of RESULTS.md from run-output.txt
py -3 make-results.py
```

Steps 2–5 need **no network at all** — they read the committed CSVs. Only step 1
touches the session-local copies of the MCP results, and only step 0 (re-issuing
the MCP calls) needs the network.

## Files

| file | what it is |
|---|---|
| `data/SPY_1d.csv`, `QQQ_1d.csv`, `TLT_1d.csv`, `GLD_1d.csv` | the pulled history, `date,open,high,low,close,volume`, with `# PROVENANCE:` headers |
| `data/crosscheck-robinhood.csv` | the Robinhood window used for the cross-check; **not** an input to any strategy |
| `study.py` | the analysis: strategies, headline metrics, R-unit statistics, regimes, year and timeframe attribution, complementarity |
| `pull_ohlcv.py` | MCP-payload-on-disk → CSV, with provenance |
| `verify_robinhood.py` | TradingView vs Robinhood close-by-close comparison |
| `handcheck.py` | re-derives p, b, E, p\*, b\* for one strategy-year by hand and diffs against `per-year.csv` |
| `make-results.py` | slices the tables out of `run-output.txt` into `RESULTS.md` |
| `run-output.txt` | the **complete raw stdout** of `study.py` — the source of every figure in `RESULTS.md` |
| `RESULTS.md` | the tables (generated from `run-output.txt`; do not hand-edit) |
| `FINDINGS.md` | the honest narrative: what works, where it fails, and what was not tested |
| `crosscheck-output.txt`, `handcheck-output.txt`, `pull-output.txt` | the verify-before-finishing evidence, verbatim |
| `headline.csv`, `rstats.csv`, `per-year.csv`, `regime.csv`, `buckets.csv`, `complementarity.csv` | machine-readable versions of the reported tables |
| `tradelogs/<INST>_<STRAT>.csv` | the simulated round-trips for S1/S2, in the input format of the sibling timeframe engine |
| `engine-output/<INST>_<STRAT>.txt` / `.json` | the sibling engine's own full report and JSON on those trade logs |

## Which parts of the toolchain this reuses rather than reimplements

`study.py` **imports** the sibling engine

```
skills/14-finance/timeframe-performance-statistics/scripts/timeframe_stats.py
```

and calls its `bucket_key()`, `aggregate_bucket()`, `sample_sd()`, `median()`,
`max_drawdown()`, `lag1_autocorr()`, `n_effective()` and `profit_factor()`, and
imports its verdict thresholds `MIN_PERIODS_FOR_VERDICT=12`,
`MIN_TRADES_PER_PERIOD_FOR_VERDICT=5`, `T_STAT_NOISE_BAND=2.0`. If that file
moves, `study.py` fails loudly instead of substituting its own formulae.

It also **runs** that engine as a subprocess on the real trade logs, and the
engine's own pooled win-rate / break-even / edge test and its verdict are quoted
in §4 of `RESULTS.md`. Those full engine reports are in `engine-output/`.

## Verified before publishing

| check | result |
|---|---|
| CSV row counts match the source | 8,485 / 6,943 / 6,094 / 5,510 — all equal to the bar counts returned; SPY's 3 pages contain 8,490 raw bars, of which 5 were a duplicate test call, leaving 8,485 unique sessions |
| CSV integrity | no duplicate dates, strictly monotonic, **no weekend dates**, no OHLC-invariant violations |
| `study.py` determinism | run twice → **byte-identical stdout** and byte-identical CSV artefacts (22 files hashed) |
| `make-results.py` idempotence | `--check` reports RESULTS.md current |
| Cross-check vs Robinhood | 120 overlapping closes across 4 instruments, **worst disagreement 0.00 bp** |
| Hand-check of p, b, E, p\*, b\* | 4 strategy-years (SPY S1 1994, 2000, 2007; QQQ S1 2000) — **all match `per-year.csv` to 6 dp** |

## Known limits of this study

Stated here as well as in `FINDINGS.md`, because they bound every number above:

- **No costs.** No commission, spread, slippage, or borrow. This flatters every
  strategy, and flatters the two trend rules most, since they trade 83–248 times
  where buy & hold trades once.
- **No dividends or fund distributions.** SPY, QQQ and especially **TLT** pay
  distributions that this price-only series excludes. TLT's price multiple over
  the window is **0.9561** — the fund's price is *below* where it started — so
  TLT's buy & hold figure is a price return, not a total return. Excluding
  coupons penalises the always-long rules (S3, S4) more than the trend rules,
  and makes TLT's row not comparable with the other three.
- **Four instruments, long only.** No shorts, no options, no futures, no
  intraday bars, no portfolio-level capital sharing.
- **No parameter sensitivity.** Nothing here establishes that 200 days beats 150,
  and nothing here rules it out. That question was deliberately not asked.
- **The last bar was still forming at pull time** and may revise.
- **The cross-check covers recent history only.** The pre-2004 TradingView bars
  have no second source in this study.

## Scope

Only this directory was created. No `SKILL.md` was modified, and no other
skill's files were touched.
