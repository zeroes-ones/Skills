# Examples — the payoff checker, its fixtures, and the strategy cards

**Every number in this directory is either the tool's own stdout or arithmetic shown inline.**

Nothing here is a backtest, a track record, a forecast or advice. The ledger in `logs/` is
**SYNTHETIC** throughout: invented trades, invented symbols (all prefixed `X` so they cannot be
mistaken for tickers), invented currency, invented dates. It carries **no market information** and
must never be quoted as evidence about any instrument, market or period. `payoff_check.py` echoes the
log's own `# PROVENANCE:` lines into its output so the label cannot be detached from the numbers.

| File | What it is |
|---|---|
| `checks/01-trend-breakout-positive.md` | A POSITIVE card: `b = 3`, `p = 0.40`, `E = +0.60R`. [ILLUSTRATIVE] |
| `checks/02-one-to-one-negative.md` | The 1:1 corner at 45%: `E = −0.10R`, NEGATIVE. [ILLUSTRATIVE] |
| `checks/03-disposition-trap-high-win-rate.md` | The disposition profile: **`p* = 0.75`** at a 62% win rate. NEGATIVE. [ILLUSTRATIVE] |
| `checks/04-cost-sensitive-tight-stop.md` | Same card twice, 0.10% stop vs 5.0% stop: **NEGATIVE vs POSITIVE** from one flag. [ILLUSTRATIVE] |
| `checks/05-marginal-mean-reversion.md` | `b = 0.75`, `p = 0.65`: `+0.1375R`, MARGINAL, `n_req = 147.405`. [ILLUSTRATIVE] |
| `checks/06-atr-sizing-and-ledger.md` | ATR stop → share count, and the `--from-log` cohort table. [ILLUSTRATIVE] + SYNTHETIC ledger |
| `strategy-cards.md` | Seven payoff specs (six cards plus the anti-card SC-0) with entry, exits, regime filter, size rule and kill criteria |
| `logs/equity-book-synthetic.csv` | 62 invented trades over four setups, with the full expected cohort arithmetic in its header. **SYNTHETIC** |

The check files are *documents*: each one states the command, the hand arithmetic computed
independently of the tool, and then the tool's **verbatim** stdout. If the tool's output ever
diverges from the hand arithmetic in those files, `scripts/verify-skill.sh` fails.

---

## 1. The engine

```
skills/14-finance/equity-trading-playbook/scripts/payoff_check.py
```

Deterministic, stdlib-only, Python 3, no network, no third-party imports, LF output.

```bash
# a card
py -3 scripts/payoff_check.py --tp 3.0 --sl 1.0 --p 0.40

# a card with cost derived from a cost rate and a stop distance
py -3 scripts/payoff_check.py --tp 2.0 --sl 1.0 --p 0.45 --cost-bps 5 --stop-pct 1.0

# an ATR stop, turned into a share count
py -3 scripts/payoff_check.py --tp 3.0 --sl 1.0 --p 0.40 \
    --atr 2.0 --atr-value 5.00 --price 50.00 --capital 100000 --cost-bps 5

# a ledger, per setup cohort
py -3 scripts/payoff_check.py --from-log examples/logs/equity-book-synthetic.csv

# one cohort only, and the cohort table as CSV
py -3 scripts/payoff_check.py --from-log examples/logs/equity-book-synthetic.csv --setup sizing-slip
py -3 scripts/payoff_check.py --from-log examples/logs/equity-book-synthetic.csv --csv-out cohorts.csv

# a proposed card measured against a ledger in the same run
py -3 scripts/payoff_check.py --tp 3.0 --sl 1.0 --p 0.40 \
    --from-log examples/logs/equity-book-synthetic.csv
```

The flag names are shared with the sibling `options-trading-playbook`'s `payoff_check.py`
(`--tp --sl --p --cost-r --n --d-tol --safety --trades-per-year --from-log --setup --json
--csv-out --version`), so the two engines speak one language, and both read the same ledger schema
by column name.

| Flag | Default | Effect |
|---|---|---|
| `--tp F` | required for a card | profit target in R |
| `--sl F` | `1.0` | stop distance in R. `0` is refused: a 0R stop is not a stop |
| `--p F` | required for a card | expected win rate, `0..1`. Outside that range is refused |
| `--cost-r F` | `0` | round-trip cost in R units, stated directly |
| `--cost-bps F` | — | round-trip commission+spread in bps of notional; with `--stop-pct` this **derives** `c_R = bps/(100*stop_pct)` |
| `--stop-pct F` | `5.0` | stop distance as a percent of price |
| `--n INT` | `250` | trades in the evaluation window, for `L` |
| `--d-tol F` | `20` | drawdown tolerated, percent of equity, for `R_max` |
| `--safety F` | `1.5` | streak-survival safety multiple |
| `--trades-per-year F` | `250` | pacing, for `years_at_pace` |
| `--atr F` | — | stop distance in ATR multiples (enables the sizing block) |
| `--atr-value F` | — | the ATR itself, currency per share. Requires `--atr` |
| `--price F` | — | share price, to express the ATR stop as a percent |
| `--capital F` | — | account equity, for risk dollars and share count |
| `--from-log FILE` | — | read a closed-trade ledger and report per-`setup` cohorts |
| `--setup TAG` | — | restrict `--from-log` to one cohort tag; the pooled row then describes only that cohort |
| `--csv-out FILE` | — | write the cohort table as CSV, one row per setup |
| `--json` | off | machine-readable output, for the verifier |
| `--quiet` | off | suppress the sensitivity block |
| `--version` | — | print the engine version |

Exit codes: `0` ran, whatever the verdict says; `2` the input could not be read or parsed, or a
required flag is missing. A NEGATIVE verdict is a successful run, not an error.

---

## 2. Input schema for `--from-log`

The **sibling ledger schema**, read by column name so a log written for `edge-and-payoff-engineering`
or `timeframe-performance-statistics` needs no alteration:

```
trade_id,open_date,close_date,pnl,risk,cost,setup,symbol
```

| Column | Required | Meaning |
|---|---|---|
| `pnl` | **yes** | realised P&L of one CLOSED trade, in currency, **gross** of `cost`. May be negative or zero |
| `risk` | for R mode | planned per-trade risk in the same currency (1R). Absent or non-positive anywhere → CURRENCY MODE, and every R-unit field is reported `n/a` |
| `cost` | for a net view | commission + fees + spread for that trade. Absent → `0`, and a zero-cost warning fires |
| `setup` | for cohorts | the cohort key. Absent → one cohort named `(none)` |
| `symbol` | optional | informational only; not used in any statistic |
| `trade_id`, `open_date`, `close_date` | optional | informational. A `close_date` is not used for bucketing here — that convention belongs to `timeframe-performance-statistics` |
| `#` lines | — | comments. A line containing `PROVENANCE:` is echoed into the output |

**Two views are printed for every cohort, and that is the point.** The R view (`b_R`) divides each
trade's P&L by that trade's own risk. The currency view (`b_$`) divides average winning dollars by
average losing dollars. They agree only when every trade risked the same amount, or when risk is
uncorrelated with the outcome in both groups. When they disagree in sign the row is flagged
`CONTAMINATED`, because the disagreement is **sizing**, not edge.

---

## 3. The synthetic ledger

`logs/equity-book-synthetic.csv` — 62 invented trades, four invented setups, six invented symbols
(`XAAA`…`XFFF`), invented currency. Its header carries the complete expected arithmetic for every
cohort, so the file is checkable on paper without running anything.

| Setup | n | `p` | `b_R` | `E` (mean R) | `c_R` | `E_net` | Shape |
|---|---|---|---|---|---|---|---|
| `trend-breakout` | 15 | 0.400000 | 3.000000 | +0.600000R | 0.010000 | **+0.590000R** | profitable |
| `range-meanrev` | 20 | 0.650000 | 0.750000 | +0.137500R | 0.010000 | **+0.127500R** | thin |
| `disposition-quick-tp` | 24 | 0.625000 | 0.333333 | −0.250000R | 0.010000 | **−0.260000R** | negative at a 62.5% win rate |
| `sizing-slip` | 3 | 0.333333 | 1.000000 | −0.333333R | 0.010000 | **−0.343333R** | **contaminated** |
| pooled book | 62 | 0.564516 | 0.887755 | +0.076613R | 0.010000 | +0.066613R | pooling hides the spread |

The `sizing-slip` cohort is the contamination demonstration: three trades risking `200 / 200 / 2000`,
realising `−1.0R`, `−1.0R`, `+1.0R`. The currency payoff ratio is `2000/200 = 10.000000` and the R
payoff ratio is `1.0/1.0 = 1.000000`. Same trades, opposite signs on the expectancy ratio view.

**This ledger is not a result.** It was built by hand from the design in its header. It is a fixture
for the tool, a paper-checkable exercise for a reader, and nothing else.

---

## 4. What the shipped numbers are, and are not

- **The card numbers are the tool's real output.** Every block quoted in `checks/` was produced by
  redirecting the command shown directly above it. They were not written by hand, and
  `scripts/verify-skill.sh` re-runs the tool and asserts they have not drifted.
- **The card numbers are `[ILLUSTRATIVE]`.** `p` is an *assumed* win rate in every one of them.
  `p = 0.40` on the trend card is not a measured hit rate and not a claim.
- **The ledger numbers are `[ILLUSTRATIVE]` and the ledger is `SYNTHETIC`.** Four cohorts were
  designed with round numbers so a reader can verify the arithmetic in their head. A designed
  fixture cannot support a conclusion about anything.
- **No performance claim exists anywhere in this directory.** A POSITIVE verdict says an *assumed*
  `p` and `b` produce a positive expectancy on paper. Whether that `p` is achievable on any
  instrument, in any regime, by any person, is outside this tool entirely.
- **The cost rate in check 4 is an assumption too.** 5 bps round trip is a plausible retail
  all-in figure for a liquid US equity; it is not a schedule. Your broker's schedule is not
  something this repository can know.
