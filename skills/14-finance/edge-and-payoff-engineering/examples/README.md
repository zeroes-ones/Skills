# Examples — the Runnable Expectancy Engine

**Every file in this directory is synthetic. None of it is a result.**

The two ledgers shipped here were invented by the skill author so that the engine
has something deterministic to run on and so that a reader can verify the algebra
by hand. They contain **no market information**. They are not backtests, not
historical data, not a strategy, not a finding, and they must never be quoted as
anything about any instrument, market or period. Nothing in this directory
demonstrates that any strategy is profitable — the illustrative ledger is
deliberately mostly unprofitable, and the hand-check ledger is ten invented rows.

Every output in `run-output.txt` carries the word SYNTHETIC because the engine
echoes each log's own `# PROVENANCE:` lines into its own output.

| File | What it is |
|---|---|
| `logs/hand-check-synthetic.csv` | **10** invented trades, `risk=100` on every row, with the full expected arithmetic written into the file's header. Paper-checkable. `[ILLUSTRATIVE]` |
| `logs/illustrative-cohorts-synthetic.csv` | **200** invented trades over ~16 months, 4 constructed setup cohorts, a non-zero `cost` column, generated at a **fixed seed**. `[ILLUSTRATIVE]` |
| `logs/generate_synthetic.py` | The seeded generator. Stdlib only. Byte-identical reruns. |
| `run-output.txt` | The engine's **actual stdout** on both ledgers, captured by redirecting the two commands shown in the file. Not written by hand. |

---

## 1. The engine

```
scripts/edge_engine.py        deterministic, stdlib-only, Python 3, no network
```

```bash
py -3 scripts/edge_engine.py --csv examples/logs/illustrative-cohorts-synthetic.csv
py -3 scripts/edge_engine.py --capital 250000 --dd-tolerance 40000 log.csv
py -3 scripts/edge_engine.py --json examples/logs/hand-check-synthetic.csv
py -3 scripts/edge_engine.py --cohort-csv cohorts.csv log.csv
```

| Flag | Effect |
|---|---|
| `--capital N` | Account equity, used to translate R into dollars. Default 100,000 |
| `--dd-tolerance N` | Currency the account can lose before the method is abandoned. Default: **20% of `--capital`** |
| `--safety F` | Streak-survival safety multiple. Default **1.5** |
| `--json` | Machine-readable output; carries every field plus the reason for each `n/a` |
| `--csv` | Appends the cohort table as a CSV block |
| `--cohort-csv FILE` | Writes the cohort table to one file |
| `--quiet` | Suppresses the panels (leaves provenance, units, cost, settings) |
| `--version` | Prints the engine version |

Exit codes: `0` ran; `2` the input could not be read or parsed (the message names
the line).

---

## 2. Input schema

```
trade_id,open_date,close_date,pnl[,risk][,cost][,setup][,symbol][,dte][,iv_rank][,side]
```

| Column | Required | Meaning |
|---|---|---|
| `trade_id` | recommended | Any unique label. Used only for deterministic sorting within a close date |
| `open_date` | optional | ISO `YYYY-MM-DD`. Not used by any calculation here |
| `close_date` | **required** | ISO `YYYY-MM-DD`. **The bucketing key** — a trade belongs to the bucket containing its close date, never its open date |
| `pnl` | **required** | Realised P&L for that closed trade. Negative allowed, zero allowed |
| `risk` | **strongly recommended** | The **planned** per-trade risk at entry, same currency as `pnl`. Its presence switches the engine into R MODE |
| `cost` | **strongly recommended** | Commission + exchange/regulatory fees + **half the bid-ask spread** for that trade |
| `setup` | **strongly recommended** | Your own setup tag. **This is the field that makes cohort attribution possible** |
| `symbol` | optional | Instrument label. Grouped as a cohort |
| `dte` | optional | Days to expiration at entry. Bucketed into 0-7 / 8-21 / 22-45 / 46-90 / 91+ |
| `iv_rank` | optional | 0-100 (or 0-1, both accepted). Bucketed into 0-25 / 25-50 / 50-75 / 75-100 |
| `side` | optional | `long` / `short`, `call` / `put` — whatever you actually decide at entry |

**Comment lines.** Any line beginning with `#` is ignored as data. A line
beginning `# PROVENANCE:` is **echoed verbatim into the engine's own output**.
Use it — an output with no provenance line should not be quoted:

```
# PROVENANCE: exported from <broker> trade blotter 2026-10-01, realised P&L net of commission and fees.
# PROVENANCE: covers account <name>, closed trades only, 2025-01-01 .. 2026-09-30.
# PROVENANCE: `risk` is the structure's max loss at entry, not the margin requirement.
```

If a ledger declares no provenance the engine prints `declared : NONE` and warns.

**Accepted numbers.** `1234.5`, `1,234.50`, `$1,234.50`, `(1,234.50)` for a
negative, a leading minus. Anything else fails with the line number rather than
being silently skipped.

**Zero-P&L rows.** A `pnl` of exactly `0` is a break-even trade: counted in `n`,
contributing `0` to expectancy, and **excluded** from the win-rate denominator
(`p = wins / (wins + losses)`). This matches `timeframe-performance-statistics`.

---

## 3. Exporting a real trade ledger to this CSV

One row per **closed trade**.

```
trade_id,open_date,close_date,pnl,risk,cost,setup,symbol,dte,iv_rank,side
T-0001,2026-03-04,2026-03-18,412.55,300,6.40,bull-call-spread,AAPL,14,38,long
T-0002,2026-03-11,2026-03-21,-300.00,300,6.40,bull-call-spread,AAPL,10,41,long
T-0003,2026-03-19,2026-04-02,0.00,250,5.10,iron-condor,MSFT,31,22,short
```

| Field | Where it comes from | The rule to apply |
|---|---|---|
| `trade_id` | your blotter's ticket or order id | Make it unique. If your broker gives none, use `SYMBOL-YYYYMMDD-seq` |
| `open_date` | the **trade date of the opening fill** | Multi-fill entries: the first fill's date, and say so in the provenance block |
| `close_date` | the **trade date of the closing fill** | Multi-fill exits: the *last* fill's date, because that is when the position closed. **The engine uses this for every bucket.** |
| `pnl` | realised P&L for the closed position, **including** or **excluding** cost — your choice, but declare it | The engine cannot tell. If it includes cost AND you also fill `cost`, you will subtract cost twice. The clean choice: `pnl` = gross realised P&L, `cost` = the total round-trip cost |
| `risk` | the **planned** per-trade risk at entry, in the same currency as `pnl` | For a defined-risk spread that is the max loss of the structure at entry. For a stock with a stop, `(entry − stop) × shares`. For an undefined-risk position there may be no honest answer — leave it blank rather than inventing one (and the engine will drop the whole run to CURRENCY MODE if any row is blank, and say so) |
| `cost` | commission + exchange fees + regulatory fees + **half the spread** paid on the way in and out | If you cannot compute your half-spread, say so in the provenance block. Do **not** put `0` and move on: a zero cost column makes every result flattering and the engine prints a warning saying exactly that |
| `setup` | **your own tag**, decided at entry, not after the fact | This is the highest-value field in the schema. Without it there is no cohort attribution and a fatal slice hides inside the pooled mean |
| `symbol` | underlying ticker | Grouped. See "one population per run" below |
| `dte`, `iv_rank`, `side` | values **at entry**, not at exit | Never back-fill these from the outcome |

**The mapping a desk ledger needs.**

| Ledger concept | This CSV |
|---|---|
| Opening execution (one or more fills) | `open_date` — first fill's trade date |
| Closing execution (one or more fills) | `close_date` — last fill's trade date |
| Realised P&L for the closed position | `pnl` — one number |
| Planned risk at entry | `risk` — one number |
| Commissions + fees + half-spread | `cost` — one number |
| **Unrealised P&L** | **not exported.** Closed trades only |
| **Open positions** | **not exported** |
| **Rungs/trims of a still-open position** | **not exported yet.** One row when the position finally closes, and say in the provenance block that multi-trim positions are a single row — it changes `n` |

**Five checks before the first run.**

1. Every row has a `close_date` and a `pnl`.
2. `risk` is positive on **every** row, or you are in CURRENCY MODE (the engine
   says which, at the top of its output, and why).
3. `cost` is filled and is **not** zero-only.
4. `setup` is filled and has fewer than ~10 distinct values. Twelve setups on 80
   trades are 6-trade cohorts and the cohort table becomes noise.
5. The provenance block names the source, the account, the window, and whether
   `pnl` is gross or net.

---

## 4. How to read each panel

### Panel 1 — the pooled panel

The whole answer in one block: `n`, `p`, `b`, `E`, `p*`, `b*`, `edge`, Kelly,
`sd_R`, `n_req`, `years_at_current_pace`, `L`, `R_max`, `c_R`, `E_net`, verdict.

* **`E (closed form x avg_loss)` reconciles the two expectancies.** `E` is the
  sample mean of the per-trade R-multiples; `p·b − (1−p)` is the textbook form.
  They are the same number multiplied by the average loss. When `avg_loss = 1R`
  the two rows are identical. When they are not, you are reading a book that does
  not lose exactly what it planned to lose — which is itself the finding.
* **Read `E_net`, not `E`.** `E_net = E − c_R`. On a `cost`-less ledger they are
  equal and the engine prints the zero-cost warning in capitals.
* **`n_req` is not a suggestion.** It is `4·(sd_R/|E|)²`, the sample at which the
  mean is two standard errors from zero. If `n < n_req`, the verdict is
  `INSUFFICIENT SAMPLE (< n_req trades)` **regardless of how good `E` looks**.
* **`years_at_current_pace = n_req / trades_per_year`.** This is the row that
  ends arguments. A book with a real but tiny edge and a wide dispersion can
  need more years than the trader has.
* **`L` is printed twice on purpose** — the closed form `ln(N)/ln(1/(1−p))` and a
  seeded simulation of the same quantity. They are estimates of an expectation,
  not a forecast. A losing streak of length `L` is **routine**. A streak
  materially longer than `L×1.5` is the first real evidence something changed.

### Panel 2 — cohort attribution and the kill list

Cohorts are grouped by `setup`, `symbol`, `dte` bucket, `iv_rank` bucket, `side`
and month, and sorted by `E_net`.

| Verdict | Rule |
|---|---|
| `INSUFFICIENT (n<30)` | `n < 30`, whatever the sign. Nothing is concluded |
| `KILL (E_net<=0 with n>=30)` | `n >= 30` **and** `E_net <= 0` |
| `KEEP` | `n >= 30` **and** `E_net > 0` |

The **KILL LIST** is the actionable output: the slices with enough data to say
they lose money. Stopping a slice is the cheapest lever in the skill. A `KILL`
means "you have no evidence this slice works today" — not "this can never work".

### Panel 3 — the multiple-testing guard

`m` cohorts were tested, so the two-sided bar is Bonferroni-adjusted to
`0.05/m`, and the count that clears it is printed alongside the count that clears
a naive `1.96`. The panel also lists **which** cohorts clear, with their `n`,
because the number to read next to `t` is always `n`: on the shipped illustrative
ledger the single cohort that clears the adjusted bar is a 2-trade month with a
`t` of −61.6. Bonferroni answers "how many slices did I test?"; it does not
answer "was this slice big enough to test?".

### Panel 4 — the payoff-engineering panel

`(4a)` inverts the expectancy identity: at the observed `p`, what payoff reaches
`E = +0.2R`, `+0.3R`, `+0.5R`, and what does that payoff need to be once cost is
paid. `(4b)` walks `b` up a ladder and shows the resulting `E`. This is the panel
that converts "make more money" into "raise `b` from X to Y".

### Panel 5 — lever sensitivity

The same book with `(a)` +5pp on `p`, `(b)` +0.25 on `b`, `(c)` −25% on cost,
`(d)` +50% on `n`, ranked by effect on `E_net`. `(d)` is always zero by
construction and the engine says so: more trades of the same process change the
evidence, not the expectancy.

### Panel 6 — what the engine cannot tell you

Printed unconditionally. It cannot tell you *why* a cohort is negative, cannot
see an open position, cannot detect a regime change, and has no idea whether your
`risk` column was ever enforced at entry.

---

## 5. The hand-check ledger, verified on paper

`logs/hand-check-synthetic.csv` — ten trades, `risk = 100`, R-multiples
`+2 +2 +1 −1 +1 −1 +3 −1 −1 +1`. The file header carries every expected value;
`scripts/verify-skill.sh` asserts the engine reproduces them.

```
n = 10    wins/losses/break-even = 6/4/0    p = 6/10 = 0.600000
avg_win  = (2+2+1+1+3+1)/6 = 10/6 = 1.666667
avg_loss = 4/4 = 1.000000                   b = 1.666667
E        = (10-4)/10 = 0.600000             (closed form 0.6*1.666667-0.4 = 0.600000)
p*       = 1/(1+1.666667) = 0.375000        b* = 0.4/0.6 = 0.666667
edge     = 0.6 - 0.375 = 0.225000           f* = 0.6/1.666667 = 0.360000 (half 0.180000)
sd_R     = sqrt(20.40/9) = 1.505545         (sum of squared deviations = 20.40)
n_req    = 4*(1.505545/0.6)^2 = 25.19       years_at_pace = 25.19/57.98 = 0.43
L        = ln(10)/ln(2.5) = 2.513           (simulated 2.178 over 20000 trials)
R_max    = (0.20)/(2.17825*1.5) = 0.061211 of capital = $6,121.12
```

`E_net = +0.60R` and yet the verdict is **`INSUFFICIENT SAMPLE (< n_req trades)`**,
because 10 trades is less than the 25 the dispersion requires. That is the whole
skill in one line: a positive expectancy is not the same thing as a demonstrated
one.

---

## 6. The illustrative ledger's constructed structure

`logs/illustrative-cohorts-synthetic.csv` was built so the four cohort verdicts
all appear. The engine's actual output:

| Cohort | n | p | b | b\* | E | E_net | Verdict |
|---|---|---|---|---|---|---|---|
| `SETUP-TREND` | 62 | 0.5000 | 1.5304 | 1.0000 | +0.2746 | **+0.2447** | `KEEP` |
| `SETUP-FADE` | 60 | 0.4167 | 0.8974 | 1.4000 | −0.2229 | **−0.2527** | `KILL` |
| `SETUP-EVENT` | 23 | 0.5217 | 0.9678 | 0.9167 | +0.0285 | **−0.0013** | `INSUFFICIENT (n<30)` |
| `SETUP-CREDIT` | 55 | 0.6182 | 0.4956 | 0.6176 | −0.0750 | **−0.1048** | `KILL` |
| **POOLED** | 200 | 0.5100 | 0.9626 | 0.9608 | +0.0009 | **−0.0289** | `NEGATIVE EDGE` |

`SETUP-CREDIT` is the disposition-effect trap: it wins **61.8%** of its trades
and still loses money, because its payoff is **0.4956** against a break-even
payoff of **0.6176**. That is a maths error, not bad luck.

The pooled verdict is `NEGATIVE EDGE`, and `n_req` is **5,199,305.93 trades** —
32,882.67 years at the ledger's own pace of 158.12 trades a year. That is what a
`+0.0009R` gross expectancy with `sd_R = 1.0723` costs to prove. Do not attempt
to prove it; change `p`, `b` or cost instead.

---

## 7. Worked walkthrough — how to go from negative to positive

This is the part that turns the engine into a decision. Reproduce it with the
commands shown.

### Step 1 — name the binding constraint

```
Observed p = 0.5100, observed b = 0.9626, b* = 0.9608, c_R = 0.0299
*** COST IS THE BINDING CONSTRAINT: gross E = 0.0009 is
    smaller than c_R = 0.0299, so the book pays more to
    trade than it earns before costs. ***
```

At the **pooled** level the payoff clears `b*`, but by `0.0009R` — less than the
`0.0299R` the book pays per trade. Nothing at the pooled level is worth fixing
until the cohorts are separated.

### Step 2 — separate the cohorts, take the kill list

The kill list from panel 2, with `n ≥ 30` and `E_net ≤ 0`:

```
iv_rank  IVR 25-50      n=54   p=0.3889 b=0.8805 E_net=-0.3071
setup    SETUP-FADE     n=60   p=0.4167 b=0.8974 E_net=-0.2527
symbol   SYN-B          n=40   p=0.4000 b=1.0392 E_net=-0.2193
side     short          n=105  p=0.5048 b=0.8360 E_net=-0.1054
setup    SETUP-CREDIT   n=55   p=0.6182 b=0.4956 E_net=-0.1048
...
```

Note that `side=short` (`n=105`) and the `iv_rank`/`symbol` cohorts overlap the
two setup cohorts — the same losing trades wearing four different labels. Kill
the **setup** slices first; the others are symptoms of them.

### Step 3 — fix the trap cohort with the right lever

`SETUP-CREDIT`: `p = 0.6182`, `b = 0.4956`, `b* = (1−p)/p = 0.6176`, `E = −0.0750`,
`E_net = −0.1048`. Two possible fixes. Both are arithmetic, so both can be
checked before anything is changed.

**Fix 1 — raise `b` (hold to the target).** `b_needed = (E_target + 1 − p)/p`. To
reach `E = +0.2R`, `b` must go from `0.4956` to `0.9412`. Holding winners to
about `1R` instead of banking `0.49R` gives `b = 1.0065` at the same `p`:

```
b 0.9412 -> E=+0.198700   E_net=+0.168825
hold to 1R (b=1.0065)     E=+0.238844   E_net=+0.208969
```

**Fix 2 — raise `p` (filter entries).** With `b` unchanged at `0.4956`,
`p* = 1/(1+b) = 0.6686`, and the **net** break-even is higher still, because the
cost has to come out first:

```
p needed to be net positive at b=0.4956: 0.688739 (now 0.618182, +7.1pp)
at p=0.70: E=+0.046607   E_net=+0.016732
at p=0.75: E=+0.120901   E_net=+0.091026
```

**Which one is the fix?** Fix 1 moves the cohort from `−0.1048R` to `+0.2090R`
per trade by changing an **entry rule** you control: where the profit target sits.
Fix 2 needs **+7.1 percentage points** of win rate — a selection problem with no
mechanical answer, and `+13.2pp` to reach `p = 0.75`. On a high-win-rate,
low-payoff book the payoff is the binding constraint. That is the disposition
effect, and this is why fixing it is the highest-return change available to most
negative traders.

### Step 4 — check the whole book after the kills

Reproduce by deleting the two negative setup cohorts and re-running:

```bash
grep '^#'      examples/logs/illustrative-cohorts-synthetic.csv >  /tmp/trimmed.csv
grep -v '^#'   examples/logs/illustrative-cohorts-synthetic.csv | head -1 >> /tmp/trimmed.csv
grep -v '^#'   examples/logs/illustrative-cohorts-synthetic.csv \
  | tail -n +2 | grep -v -E 'SETUP-FADE|SETUP-CREDIT'      >> /tmp/trimmed.csv
py -3 scripts/edge_engine.py /tmp/trimmed.csv
```

The engine's actual output on that trimmed book:

```
trades (n)                         85
win rate p = wins/(wins+losses)    0.505882
payoff ratio b                     1.370477
expectancy E                       0.208034
cost drag c_R                      0.030790
net expectancy E_net               0.177244   <-- THE NUMBER TO ACT ON
break-even payoff b*               0.976744
sd_R                               1.259131
n_req (2-sigma)                    146.53
years_at_current_pace              2.17
R_max (survival-derived risk/trade) 0.023493 of capital = 2,349.30
VERDICT: INSUFFICIENT SAMPLE (< n_req trades)
```

`E_net` goes from **−0.0289R** to **+0.1772R**, and the verdict moves from
`NEGATIVE EDGE` to `INSUFFICIENT SAMPLE (< n_req trades)`. Read the second verdict
honestly: **85 trades is still short of the 147 the remaining book's dispersion
requires.** Two years and two months of trading at its own pace would settle it.
Killing the losing slices did not prove an edge; it produced a book that is
worth continuing to measure, which is the most a ledger can do.

### Step 5 — pick the risk per trade from the streak, not from a feeling

Before sizing up, use the derived number. On the trimmed book
`L = 5.675` (simulated) and `D_tolerance = $20,000`, so

```
R_max = 20,000 / (5.675 × 1.5) = $2,349.30 = 2.35% of a $100,000 account
```

A six-loss run is **routine** at `p = 0.5059`. A book sized at 5% per trade would
be down 30% on that run — past its own stated tolerance — and would then be
trading recovery instead of edge. That is the entire argument for deriving risk
per trade from the streak rather than accepting a number that "feels right".

---

## 8. What is deliberately not shipped

* **No real ledger.** A real one carries a real edge or the lack of it, and the
  skill author has no business asserting either.
* **No performance claim.** Not one number in this directory is a claim that any
  strategy works. The illustrative ledger's pooled verdict is `NEGATIVE EDGE`.
* **No broker, no market data, no backtest.** There is no vendor dependency in
  the engine at all: `scripts/edge_engine.py` imports `argparse`, `csv`, `json`,
  `math`, `os`, `random`, `re`, `sys` and `datetime`, and nothing else.
