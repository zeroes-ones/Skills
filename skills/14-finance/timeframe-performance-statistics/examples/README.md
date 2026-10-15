# Examples — the Runnable Calculator

**Every file in this directory is synthetic. None of it is a result.**

The two logs shipped here were invented by the skill author so that the engine has something
deterministic to run on and so that a reader can verify the arithmetic by hand. They contain
**no market information**. They are not backtests, not historical data, not a strategy, not a
finding, and they must never be quoted as anything about any instrument, market or period.
Every output in `run-output.txt` carries the word SYNTHETIC because the engine echoes the
log's own `# PROVENANCE:` lines into its output.

| File | What it is |
|---|---|
| `logs/hand-check-synthetic.csv` | Six invented trades over two months, with the full expected arithmetic written into the file's header. Paper-checkable. `[ILLUSTRATIVE]` |
| `logs/illustrative-year-synthetic.csv` | 120 invented trades over ~14 months, four invented symbols, generated at a **fixed seed**. `[ILLUSTRATIVE]` |
| `logs/generate_synthetic.py` | The seeded generator. Stdlib only. Byte-identical reruns. |
| `run-output.txt` | The engine's **actual stdout** on both logs, captured by redirecting the commands shown in the file. Not written by hand. |

---

## 1. The engine

```
scripts/timeframe_stats.py        deterministic, stdlib-only, Python 3, no network
```

```bash
py -3 scripts/timeframe_stats.py --csv examples/logs/illustrative-year-synthetic.csv
py -3 scripts/timeframe_stats.py --bucket M,Q --capital 250000 examples/logs/<your-log>.csv
py -3 scripts/timeframe_stats.py --json examples/logs/<your-log>.csv
py -3 scripts/timeframe_stats.py --periods examples/logs/<your-log>.csv
py -3 scripts/timeframe_stats.py --csv-out periods.csv examples/logs/<your-log>.csv
```

| Flag | Effect |
|---|---|
| `--capital N` | Adds return-based rows on a starting equity of N, with a printed fiction warning |
| `--bucket B` | One or more of `D,W,2W,M,Q,H,Y`, comma-separated. Default: all seven |
| `--json` | Machine-readable output; carries the reason for every `n/a` |
| `--csv` | Appends the per-period series as CSV blocks, one per bucket |
| `--csv-out FILE` | Writes the per-period series for all buckets to one file with a `bucket` column |
| `--periods` | Prints the per-period series as an aligned human table |
| `--quiet` | Suppresses the transposed summary table |
| `--version` | Prints the engine version |

Exit codes: `0` ran; `2` the input could not be read or parsed (the message names the line).

---

## 2. Input schema

```
trade_id,open_date,close_date,pnl,risk,symbol
```

| Column | Required | Meaning |
|---|---|---|
| `trade_id` | recommended | Any unique label. Used only for deterministic sorting within a day |
| `open_date` | optional | ISO `YYYY-MM-DD`. The date the position was opened. Not used for bucketing |
| `close_date` | **required** | ISO `YYYY-MM-DD`. **This is the bucketing key** |
| `pnl` | **required** | Realised P&L in currency for that closed trade. Negative allowed, zero allowed |
| `risk` | optional | The planned per-trade risk unit, so R-multiples can be derived downstream |
| `symbol` | optional | Instrument label. Carried through, not grouped |

**Comment lines.** Any line beginning with `#` is ignored as data. A line beginning
`# PROVENANCE:` is **echoed verbatim into the engine's own output**. Use it:

```
# PROVENANCE: exported from <broker> trade blotter 2026-10-01, realised P&L net of commission and fees.
# PROVENANCE: covers account <name>, closed trades only, 2023-01-01 .. 2026-09-30.
# PROVENANCE: partial exits are one row per closing fill.
```

If a log declares no provenance the engine prints `declared : NONE` and warns. **A run without
a provenance block should not be quoted.**

**Accepted `pnl` formats.** `1234.5`, `1,234.50`, `$1,234.50`, `(1,234.50)` for a negative,
and a leading minus. Anything else fails with the line number rather than being skipped.

**Empty periods do not exist.** Periods are created where trades exist. A month with no closed
trades is not a zero-P&L month; it is absent. That is a real limitation — see
`references/what-the-engine-cannot-tell-you.md`.

---

## 3. Exporting a real trade ledger to this CSV

One row per **closed trade**. One row per full close of a position.

```
trade_id,open_date,close_date,pnl,risk,symbol
T-0001,2025-03-04,2025-03-18,412.55,300,AAPL
T-0002,2025-03-11,2025-03-21,-300.00,300,AAPL
T-0003,2025-03-19,2025-04-02,0.00,250,MSFT
```

| Field | Where it comes from | The rule to apply |
|---|---|---|
| `trade_id` | your blotter's execution or ticket id | Make it unique. If your broker does not give one, use `SYMBOL-YYYYMMDD-seq` |
| `open_date` | the **trade date of the opening fill**, not the order date | Multi-fill entries: use the first fill's date, and say so in the provenance block |
| `close_date` | the **trade date of the closing fill** | Multi-fill exits: use the *last* fill's date, because that is when the position closed. This is what makes the trade an entry in the bucket that contains its full life |
| `pnl` | realised P&L for that closed trade, **including** commission, exchange fees, financing and borrow costs, **or** explicitly excluding them | Whichever you choose, write it in a `# PROVENANCE:` line. The engine cannot tell, and every statistic is either gross or net according to this one decision |
| `risk` | the **planned** per-trade risk at entry, in the same currency as `pnl` | For a defined-risk options spread, that is the max loss of the structure at entry. For a stock with a stop, that is (entry − stop) × shares. For an undefined-risk position there may be no honest answer — leave it blank rather than inventing one |
| `symbol` | the underlying ticker or a class label | See "one population per run" below |

**The mapping the desk's ledger needs.**

| Ledger concept | This CSV |
|---|---|
| Opening execution (one or more fills) | `open_date` — first fill's trade date |
| Closing execution (one or more fills) | `close_date` — last fill's trade date |
| Realised P&L for the closed position | `pnl` — one number, net or gross per your provenance line |
| Planned risk at entry | `risk` — one number |
| Instrument | `symbol` |
| **Unrealised P&L** | **not exported.** The engine reads closed trades only |
| **Open positions** | **not exported** |
| **Deposits, withdrawals, dividends, interest, fees charged to cash** | **not exported.** These are cashflows, not trade P&L; including them corrupts the cumulative series |
| **A partial exit with the position still open** | **not exported yet.** It becomes one row when the position finally closes — and say in the provenance block that multi-trim positions are recorded as a single row, because it changes `n_trades` |

**Six checks before the first run.**

1. `n_trades` in the engine's output equals your row count minus the header.
2. The printed close-date span matches your expectation to the day.
3. `gross_profit − gross_loss` equals your broker's realised P&L for the same window, to the
   currency — if it does not, `pnl` is net of something you did not declare, or rows are missing.
4. No trade has `close_date < open_date`.
5. Every `pnl` is in the same currency. A multi-currency book needs conversion first, at a rate
   you state.
6. The provenance block names the source, the window, the fee treatment and the partial-exit
   convention.

**One population per run.** If the log mixes an equity book and a short-premium options book,
run the engine once per population. Pooling raises `trades_per_period` and destroys the meaning
of the pooled `payoff_ratio`, because the two classes have different break-even win rates. The
engine cannot detect this; `n_trades` will look perfectly healthy. See
`references/per-instrument-interpretation.md`.

---

## 4. How to read each output field

Full walkthrough with live values: `references/reading-the-engine-output.md`.

### Coverage

| Field | Meaning | What to check |
|---|---|---|
| `n_periods` | Number of periods in this bucket | Fewer than 12 fails the verdict gate |
| `n_trades` | Trades in the bucket | **Must equal the log's row count in every bucket** |
| `trades_per_period` | `n_trades / n_periods` | Below 5 fails the verdict gate |
| `periods_per_year` | `365.25 / nominal_length` | A calendar fact, not a licence to annualise |
| `first_period`, `last_period` | Span covered | Watch for a stub first or last period |

### Trade totals (pooled — identical in every bucket by construction)

| Field | Meaning |
|---|---|
| `gross_profit` | Sum of positive `pnl` |
| `gross_loss` | Sum of negative `pnl`, reported as a **positive magnitude** |
| `net_pnl` | `gross_profit − gross_loss` |
| `wins`, `losses`, `breakeven_trades` | Counts of `pnl > 0`, `pnl < 0`, `pnl == 0` |
| `win_rate` | `wins / (wins + losses)`. **Break-even trades are excluded from the denominator** |
| `avg_win`, `avg_loss` | `gross_profit / wins`, `gross_loss / losses` |
| `payoff_ratio` | `avg_win / avg_loss` |
| `expectancy_per_trade` | `net_pnl / n_trades` |
| `profit_factor` | `gross_profit / gross_loss`; prints `inf` when there are no losses |

### Beat losses

| Field | Meaning |
|---|---|
| `break_even_win_rate` | `1 / (1 + payoff_ratio)`. The win rate this book needs to break even at its own average sizes |
| `edge` | `win_rate − break_even_win_rate` |
| `se_win_rate` | `sqrt(p(1−p)/N)` with `p = win_rate` and `N = wins + losses` |
| `2 × se_win_rate` | The threshold `edge` must exceed for the win rate to be distinguishable from break-even |
| `edge > 2 × se?` | `PASS` / `FAIL`. The engine's own verdict on the win-rate test |
| `periods_positive_edge` | How many individual periods had a computable positive edge |

**This whole group is bucketing-invariant.** Every trade is in every bucket, so these numbers
are the same in all seven columns. Changing the review timeframe cannot move them.

### Across periods — the group that answers the timeframe question

| Field | Meaning |
|---|---|
| `mean_period_pnl`, `median_period_pnl` | Location. A mean far above the median says a few periods carry the series |
| `sd_period_pnl` | Sample standard deviation, `n − 1`. `n/a` for a single period |
| `t_stat` | `mean / (sd / sqrt(n_periods))`. Read it with `n_eff` |
| `period_sharpe` | `mean / sd` at this bucket's frequency. Note `t_stat = period_sharpe × sqrt(n_periods)` |
| `cumulative_pnl` | Running sum of the period series. Must equal `net_pnl` |
| `max_drawdown` | Peak-to-trough fall of the cumulative series, **negative**. Running equity starts at zero, and zero is the initial peak |
| `lag1_autocorrelation` | Lag-1 correlation of the period P&L series. `n/a` below 3 periods |
| `n_eff` | `n_periods × (1−ρ)/(1+ρ)`. `n/a` when `ρ` is unavailable or `|ρ| ≥ 0.999` |
| `n_eff_capped` | `n_eff` limited to the trade count, because `ρ < 0` can inflate the raw formula past what exists |

### Verdict inputs

| Field | Meaning |
|---|---|
| `verdict eligible` | `yes` only when `n_periods ≥ 12` **and** `trades_per_period ≥ 5` **and** `t_stat` is computable |
| `noise flag` | `NOT DISTINGUISHABLE FROM NOISE` when `|t_stat| < 2`; `t_stat not computable` when it is `n/a` |

### The verdict

```
VERDICT: <BUCKET>   ranked by descending |t_stat| among the buckets that pass both gates
        INSUFFICIENT DATA   when none passes, with the failing constraint named per bucket
```

The verdict line also prints `n_periods` **and** `n_eff`, and the dependence caveat is printed
unconditionally: nested buckets are not independent tests, so a bucket t-statistic is a
**stability indicator**, not a significance test. See
`references/dependence-and-autocorrelation.md`.

---

## 5. How to use this on the real ledger

**Run it monthly. Keep the output. Compare across months.**

The engine answers a question about a *sample*, so a single run is one observation. The value
comes from repetition with a fixed procedure:

1. **Fix the cadence first, from the holding period.** Compute the mean of
   `close_date − open_date` over the closed trades in the log, then apply the quarter-to-half
   rule in `references/cadence-versus-holding-period.md`. An options book with a 2–30 DTE
   holding period lands on weekly-to-monthly; a stock book with a 6–18 month holding period
   lands on monthly-to-quarterly. **Write the chosen bucket into your review template before
   looking at any P&L**, so the bucket is not chosen after seeing the answer.
2. **On the first of each month, export the full ledger to the CSV** and overwrite
   `# PROVENANCE:` with the export date, account and fee treatment.
3. **Run the engine with `--csv` and save the whole stdout** as
   `reviews/YYYY-MM-timeframe-stats.txt`. Also save `--json` — it is the machine-readable
   archive and it carries the reason for every `n/a`.
4. **Record four numbers in a one-row log** (a spreadsheet is fine), one row per month:

   | Column | Where it comes from |
   |---|---|
   | `as_of` | the month |
   | `n_trades`, `n_periods` | coverage group, for the review bucket |
   | `t_stat` | across-periods group, for the review bucket |
   | `n_eff` | across-periods group — carries the dependence disclosure forward |
   | `win_rate`, `break_even_win_rate`, `edge` | beat-losses group (identical for every bucket) |
   | `edge_test` | `PASS` / `FAIL` |
   | `verdict_bucket` | the bucket the verdict named |

5. **Read the month-over-month changes, not the levels.**

   - **`t_stat` moving while `n_trades` barely moves** means the *composition* of the sample
     changed, not the sample size. A t-statistic that jumps because one large loss fell out of
     the trailing window is not a change in the edge.
   - **`t_stat` rising steadily with `n_eff` rising alongside it** is the shape you want: the
     claim is strengthening because the sample is.
   - **`edge` drifting while `break_even_win_rate` is flat** means the win rate moved.
     **`edge` drifting while `win_rate` is flat** means `payoff_ratio` moved, which usually
     means one trade did. Check `avg_win` and `avg_loss` before believing it.
   - **`edge_test` flipping from `FAIL` to `PASS`** requires either a real change or a bigger
     sample. Confirm which by looking at `n_trades`: if the count is roughly the same and the
     test flipped, the flip is one or two trades and should not be announced.
   - **`verdict_bucket` changing between months** is usually a gate crossing, not a regime
     change: `trades_per_period` drifts as you trade more or less, and a bucket can pass in one
     month and fail in the next. Check which constraint moved before interpreting the change.

6. **Do not re-chase the bucket.** If the verdict names `M` this month and `2W` next month,
   the finding is "the book's turnover sits near the gate boundary", not "the right timeframe
   is `2W` now". The review cadence stays where step 1 put it.

7. **Once a quarter, do the checks the engine cannot do** — see
   `references/what-the-engine-cannot-tell-you.md`. In particular reconcile `n_trades` against
   the broker's blotter (unlogged trades and collapsed partial exits are invisible to the
   engine), confirm the fee treatment has not changed, and confirm whether any account or
   instrument class leaked into the log.

8. **Keep a run you do not like.** The archive's value is that it contains the months before
   the drawdown. Deleting a bad run is the fastest way to turn a statistics trail into a
   highlight reel.

---

## 6. Reproducing everything in this directory

```bash
# regenerate the illustrative log (byte-identical: fixed seed 20260414)
py -3 examples/logs/generate_synthetic.py

# the two commands whose output is captured verbatim in run-output.txt
py -3 scripts/timeframe_stats.py --csv examples/logs/hand-check-synthetic.csv
py -3 scripts/timeframe_stats.py --csv examples/logs/illustrative-year-synthetic.csv

# the self-verifying gate: structure, provenance, the hand-check arithmetic, determinism
bash scripts/verify-skill.sh
```

`verify-skill.sh` asserts the hand-check fixture's documented expected values against the
engine's live output, and asserts that two consecutive runs of the engine on the same log are
byte-identical.

---

## 7. The blunt statement, restated because it matters

**Nothing in this directory is a result.**

- `hand-check-synthetic.csv` and `illustrative-year-synthetic.csv` are **invented**. Their
  `pnl` figures are invented currency, not dollars earned by anyone.
- They describe **no instrument, no market, no period and no strategy**. The symbols
  `SYN-A`..`SYN-D` exist so that nobody can mistake them for tickers.
- The numbers in `run-output.txt` are the engine's honest arithmetic **on invented data**. They
  demonstrate what the engine does; they demonstrate nothing about trading.
- Every `[COMPUTED]` figure quoted in the skill's `SKILL.md` and `references/` is either pasted
  from `run-output.txt` or is arithmetic on a figure that is, and is labelled as such.
- `[ESTIMATED]` figures are assumptions with their derivation shown. `[ILLUSTRATIVE]` marks
  synthetic data. `[VERIFIED]` marks a statement checked against a named source.

A calculator you can run yourself is worth more than one you have to trust. That is the entire
point of shipping the code, the logs and this file together.
