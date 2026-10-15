# index-options-test — SPY / QQQ / IWM, the underlying **and** options on it

A pre-registered, run-once study of whether restricting the universe to three
index ETFs and trading **both** the underlying and options on it can reach
"profitable in most conditions" — and what that costs.

- **Pull date: 2026-10-14** (the sibling studies' pull; re-validated this
  session against a fresh 2026-10-15 pull — see §3).
- **Run date: 2026-10-15.**
- **Window: 2001-03-13 … 2026-10-14** — 6 436 sessions, **24 complete calendar
  years (2002–2025)**, 102 complete quarters, 306 complete months.
- **Headline answer:** one book clears the pre-registered bar, and only one.
  See [`RESULTS.md`](RESULTS.md) and [`FINDINGS.md`](FINDINGS.md).

---

## 1. The question, and the predecessor result this study builds on

The desk owner has asked, repeatedly, for a book that is *profitable in most
conditions*. The sibling `../../equity-trading-playbook/examples/frontier-test`
answered it **for a cross-asset TREND book** and the answer was hard:

| horizon | largest λ with 100 % positive | CAGR there | cash CAGR | excess |
|---|---|---|---|---|
| year | 0.008 | 1.81 % | 1.78 % | **+0.03 %/yr** |
| quarter | 0.001 | 1.78 % | 1.78 % | +0.00 %/yr |
| month | 0.000 | 1.78 % | 1.78 % | +0.00 %/yr |

The frontier **ends at zero exposure** for that book. The sibling also measured
that the variance risk premium is real and is a high-frequency positivity
engine: VIX sat above the subsequently realised 21-day move in **82.9 %** of
windows, mean **+3.62** vol points, negative in exactly one year (**2008**).

**This study changes two things and only two:** the universe (three index ETFs
instead of a cross-asset book) and the instrument set (options on those ETFs
instead of the underlying alone). It does not contest the predecessor — §11 of
`RESULTS.md` reproduces the sibling's VRP arithmetic *exactly* (mean VRP
**+3.64** vs its +3.62; share positive **83.0 %** vs 82.9 %; 2008 mean VRP
**−2.33** vs its −2.33; 2020 fair-strike total **−7.3R** vs its −7.3R; worst
window **R = −3.98 starting 2020-02-20** vs its −3.98) and the correlation
finding it warned about. What changes is the **positivity frontier for years**,
and §5 below says by how much.

---

## 2. THE OPTIONS MODELLING PROBLEM — read this first

**Historical option quotes are not available from the sources used here.** Every
option price in this study is therefore computed, not observed. Every
options-derived number is labelled **`[MODELED]`** and never `[VERIFIED]`.

What IS real: the daily OHLC of `AMEX:SPY`, `NASDAQ:QQQ`, `AMEX:IWM`; the VIX
index level (`TVC:VIX`); and the 3-month T-bill yield index (`TVC:US03M`). Each
series sits in `data/*.csv` behind its own `# PROVENANCE:` header.

### The model, stated exactly

```
IV_leg  = VIX(t − 3 sessions) / 100
          × kappa(index, t − 3 sessions)
          × iv_stress
          × (30 / D)**alpha          # alpha = 0.0 in the primary run

kappa(index) = clip( RV60(index) / RV60(SPY), 0.60, 2.00 )
               both realised vols measured at t − 3 sessions

price = Black-Scholes, European, q = 0 (primary)
strike = solved so that the leg's |delta| hits the pre-registered target
settlement = intrinsic, against the REAL closing price of the expiry session
```

**Why the 3-day VIX lag.** A trade is entered at the *open* of the session after
the signal. Using that same session's VIX close would be information a trader
does not have. The headline run uses a **3-session lag** and §13 of `RESULTS.md`
re-runs with **no lag** so the size of the gift is visible. Measured: removing
the lag moves S2's CAGR from **+2.97 % to +2.94 %** and S3's from **+10.53 % to
+10.57 %** — i.e. the lag is worth **essentially nothing**, because a stale VIX
is as often lower than the current print as higher. Reported rather than hidden,
and the result is a genuine negative: the modelled edge is *not* a lookahead
artefact of the lag choice.

**Why `kappa`.** VIX is the **S&P 500** implied-vol index. QQQ and IWM do not run
at the S&P's vol. `kappa` is the mechanically-derived relative-vol multiplier
from the *lagged* 60-day realised-vol ratio, clipped to a stated band. It is not
a tuned parameter, and it is 1.0 for SPY by construction.

**On the brief's `sqrt(30/21)` factor.** Read as the term-structure rule
`IV(D) = VIX × (30/D)^alpha`, that factor is what the rule gives at a **21-day**
tenor (1.195×). This study's legs are **30 and 60 DTE**, so the same rule gives
**1.000×** and **0.707×**. Both settings are reported: the primary run uses
**alpha = 0.0 (flat term structure, one vol for both tenors)** and §13 reports
**alpha = 0.5**. The choice matters enormously for S4 — see §6.

### What the model cannot see

1. **No bid/ask spread in the quote.** A flat per-contract spread IS charged as
   a cost (§7), but the quote itself is a mid.
2. **No skew.** One implied vol prices every strike, so the *sold* leg is priced
   at the same vol as the wings. A real seller of an out-of-the-money option
   collects **less** than the flat-vol Black-Scholes value. §13c sizes this and
   it is the single largest bias in the study.
3. **No term structure in the primary run** (§13 runs the `sqrt(30/D)` variant).
4. **No early exercise and no assignment.** SPY/QQQ/IWM options are **American
   and physically settled**; they are priced here as **European**. For the
   spreads this is a genuine approximation: an American short put can be
   assigned early, and the model would never show it.
5. **No pin risk.** The expiry session's close decides everything.
6. **No dividends in the primary run.** The price series is price-only, so the
   modelled call is too expensive and the modelled put too cheap. §13b re-runs
   with published average yields held constant. The result is surprising and is
   reported as measured: it barely moves S1/S3, because moving to a
   dividend-aware price *also moves the delta-targeted strike*.
7. **No margin, no buying-power constraint, no liquidity limit, no partial
   fills, no legging risk, no tax.** One contract per sleeve, integer, always
   fillable at the modelled mid.
8. **No overlapping cycles.** The tenor is 30 calendar days **capped at the last
   session before the next monthly roll**, so a monthly programme never holds
   two structures at once. Measured tenors are 27–30 days and the pricing uses
   the **actual** calendar days, not a nominal 30/365.

**What this means for the reader.** A `[MODELED]` edge that survives a 1.5
vol-point skew haircut, a doubling of costs, and IV ±20 % is worth taking
seriously. One that does not survive them is a statement about the model.
§15 of `RESULTS.md` prints that matrix.

---

## 3. Data

**Primary source.** TradingView MCP tool `mcp__tradingview__mcp-tv-get-ohlcv`,
interval `1D`, `format="columns"`. Every series is **split-adjusted, regular
session only, and price-only — no dividends or distributions**. Every price
return in this study is therefore a price return.

**What was carried, and how it was verified.** The five long series already
existed in `../../equity-trading-playbook/examples/frontier-test/data/`, pulled
with the same tool on **2026-10-14**. `pull_data.py` carries them into `data/`
only after **re-checking the source header's own `rows`/`first`/`last` claims
against the body** and re-computing a SHA-256 of the body. It then **re-pulls**
the four series that matter (SPY, QQQ, IWM, VIX, `count=1500`, 2026-10-15) and
compares the overlapping sessions row for row:

| series | fresh rows | overlapping | byte-identical OHLC | mismatches |
|---|---|---|---|---|
| SPY | 1500 | 1500 | 1500 | 0 |
| QQQ | 1500 | 1500 | 1500 | 0 |
| IWM | 1500 | 1500 | 1500 | 0 |
| VIX | 1500 | 1500 | 1500 | 0 |

The fresh payloads are kept as `data/_check_<SYM>_recent.csv` (an audit trail,
**not** a strategy input). The full log is `logs/pull-output.txt`.

**Series inventory** (read back from the provenance blocks):

| series | source symbol | rows | first | last |
|---|---|---|---|---|
| SPY | `AMEX:SPY` | 8 485 | 1993-01-29 | 2026-10-14 |
| QQQ | `NASDAQ:QQQ` | 6 943 | 1999-03-10 | 2026-10-14 |
| IWM | `AMEX:IWM` | 6 635 | 2000-05-26 | 2026-10-14 |
| VIX | `TVC:VIX` | 9 283 | 1990-01-03 | 2026-10-14 |
| US03M | `TVC:US03M` | 18 197 | 1954-01-04 | 2026-10-14 |

**`TVC:US03M` is NOT a price series.** The `close` column is a
**percent-per-annum yield index**, not a tradable price, and nothing compounds
it as a price return. It is used only for the cash accrual
`r_cash[j] = yield(book date j−1)/100/252`, floored at zero, with the same
no-lookahead convention the sleeves use. It is an **upper bound** on cash: it
ignores fund fees, the bid/offer and the roll. Measured over this window, **20
of 6 436 sessions have a non-positive accrual**, so a cash-only plan is not
100 % positive even at zero exposure.

**The primary window** is the intersection of the SPY, QQQ, IWM and VIX
calendars, starting on the first session every SMA(200) is live — IWM is the
binding constraint. That is **2001-03-13**, which is why the window contains
both **2008** and **2020**.

---

## 4. The pre-registered strategies

Declared before the first run. Entries at the **next open** after a signal.

| id | what it is |
|---|---|
| **S1** | Trend on the underlying: long iff `close > SMA(200)`, flat below |
| **S2** | Systematic premium selling, defined risk: each month sell a 30-DTE put spread, **~16-delta short / $5 wide long**, hold to expiry, settle against the real path |
| **S3** | Buy-write / covered call: long the underlying, sell a **30-DTE ~30-delta call** each month |
| **S4** | Tail-hedged premium: S2 plus a long **~5 %-OTM 60-DTE put**, rolled monthly, the debit paid out of the same sleeve |
| **S5** | Trend + premium overlay: **0.75 × S1 book + 0.25 × S2 book**. The weight is FIXED and was not tuned |
| **S6** | Buy & hold — the control |

**Bounded by the pre-registration, not chosen:**

- Underlying rule `SMA(200)`; entry at the next open; exit at the next open.
- Risk unit `R`: **S1/S3/S6** `R = 2 × ATR(14)` at entry, per share (the
  siblings' measured unit). **S2** `R = width − gross credit`. **S4** `R = the
  structure's maximum loss` on a terminal-price grid.
- The premium sleeves' capital is a **fixed risk budget of 10 spread-widths**
  (`$5 000`), and their daily return is **dollar P&L ÷ that budget** — a fixed
  budget, not a compounding account, so a structure that is a persistent net
  cash outflow shows up as a persistent negative return instead of silently
  depleting an account.
- Costs: a **per-contract fee** and a **stated half-spread per share per side**,
  both charged at entry and (where there is an exit trade) at exit; plus a
  round-trip bps cost on the underlying.
- IV stress ±20 %; VIX lag 3 (variant 0); `alpha` 0 (variant 0.5); sold-leg skew
  haircut 0 (variants 1.5 and 3.0 vol points); dividends 0 (variant published).

### The pre-registered success bar

A book is **"all-weather enough"** if and only if it is

- **(a)** positive in **≥ 80 %** of complete **years**, and
- **(b)** positive in **≥ 70 %** of complete **quarters**, and
- **(c)** **CAGR above the cash rate** over the same window, and
- **(d)** max drawdown survivable — **reported, not thresholded after seeing
  the result**.

**Selection rule, declared up front:** the "best book" is the strategy with the
highest fraction of positive complete years; ties broken by CAGR.

---

## 5. How to re-run

`python3` is not on `PATH` on this machine; use `py -3` (Python 3.10.11).

```bash
cd skills/14-finance/options-trading-playbook/examples/index-options-test
export PYTHONIOENCODING=utf-8

# 1. build data/*.csv  (carry + verify + re-pull-check; needs the MCP payload dir)
py -3 pull_data.py \
    --results "$SESSION/agents/$AGENT/tool-results" \
    --sibling ../../equity-trading-playbook/examples/frontier-test/data \
    --out data --carry-date 2026-10-14 --check-date 2026-10-15 \
    | tee logs/pull-output.txt

# 2. the study  (deterministic, stdlib only, no network)
py -3 study.py > run-output.txt

# 3. the INDEPENDENT re-derivation  (does not import study.py)
py -3 handcheck.py > handcheck-output.txt     # expect HANDCHECK PASSED

# 4. rebuild RESULTS.md from the captured run
py -3 make-results.py
```

Steps 2–4 need **no network at all**. Only step 1 touches the session-local
copies of the MCP results, and only the MCP calls themselves need the network.

**Determinism** (verified, 2026-10-15): two consecutive runs produced **0
differing lines of stdout** and **0 differing bytes across all `out/*.csv`**.
There is no clock, no RNG and no set iteration in `study.py`.

---

## 6. Files

| file | what it is |
|---|---|
| `pull_data.py` | carries the five long series from the sibling study after verifying the source header against the body, re-pulls four series for validation, writes `data/*.csv` — **no network of its own** |
| `study.py` | the study: pre-registration echo, the Black-Scholes engine, the six strategies, the bar, the correlation, the positivity table, the λ frontier, the stress cells, the VRP reproduction, costs, IV/skew/dividend sensitivity, the SPY-only window. Deterministic, stdlib only, LF output |
| `handcheck.py` | an **independent** re-derivation from `data/*.csv`. Own CSV reader, own Black-Scholes, own delta solver, own implied-vol context, own month grid, own simulator, own statistics, own bucketing, own correlation, own VRP reproduction. **Does not import `study.py`** |
| `make-results.py` | renders `RESULTS.md` from `run-output.txt` and `out/*.csv`. Formats; never calculates |
| `data/*.csv` | the price/level series, each behind a `# PROVENANCE:` block |
| `data/_check_*_recent.csv` | this session's fresh validation pull — audit trail only |
| `out/*.csv` | every table the study produces (13 files) |
| `logs/pull-output.txt` | complete stdout of the data step |
| `run-output.txt` | complete stdout of `study.py` — the source of every number in `RESULTS.md` |
| `handcheck-output.txt` | complete stdout of `handcheck.py` |
| `RESULTS.md` | every table, pasted from the real run |
| `FINDINGS.md` | the honest narrative: what the carry stream added, where it breaks, what the model cannot see, what remains untested |

---

## 7. The cost model

`[MODELED]` — a cost assumption, not an observed quote.

| setting | fee / contract / side | half-spread / share / side | underlying round trip |
|---|---|---|---|
| **FREE** | $0.00 | $0.000 | 0 bps |
| **LOW** *(headline)* | $0.65 | $0.025 | 5 bps |
| **HIGH** | $0.65 | $0.050 | 20 bps |

One side of one leg costs `fee + half_spread × 100` dollars per contract. A
two-leg spread therefore pays **$6.30** at LOW to open (2 legs × $3.15) and
nothing to expire. A hedge leg pays one side at entry and one side at exit.
These are round numbers chosen for liquid index options; they are **not**
observed quotes, and §12 re-runs everything at all three settings.

---

## 8. Verification performed

```bash
py -3 study.py > run1.txt ; py -3 study.py > run2.txt
diff run1.txt run2.txt                       # 0 lines
diff -r out_snapshot out                     # 0 files differ
py -3 handcheck.py                           # HANDCHECK PASSED
```

| check | result |
|---|---|
| Determinism (two runs) | **0** differing stdout lines, **0** differing `out/*.csv` |
| Independent re-derivation, trade ledger | **918 / 918** S2 spreads matched on (index, expiry); worst credit gap **4.995×10⁻⁷** (the artefact's 6-decimal rounding); worst strike gap **4.996×10⁻⁷**; worst settlement gap **4.996×10⁻⁷** |
| Independent re-derivation, headline | S2 CAGR gap **0.000×10⁰**; maxDD **3.3×10⁻¹⁶**; Sharpe **5.6×10⁻¹⁷**; positive-year / -quarter / -month fractions **0.000×10⁰** |
| Independent re-derivation, correlation | all six gaps **0.000×10⁰** |
| Independent re-derivation, VRP | 2008 mean VRP −2.33; 2020 total −7.3R; worst window 2020-02-20, VIX 15.6, R_fair −3.98 — matching the sibling study exactly |
| **By hand**: one Black-Scholes price | S = 100, K = 95, T = 30/365, r = 4 %, σ = 20 % → **P = 0.5088781574**, every intermediate (`d1`, `d2`, `N(·)`, discount factors) printed in `handcheck-output.txt` §E |
| **By hand**: one month's spread settled against the real path | S2 SPY 2001-04-02 → 2001-04-30, K1 = 108.9730, K2 = 103.9730, real close 124.91, short intrinsic 0.000000, long intrinsic 0.000000, credit 0.606128, net **54.3128** vs the study's **54.312811**, gap **−1.1×10⁻⁵** (the 6-decimal artefact's rounding of the printed 54.3128); R = (5 − 0.606128) × 100 = **439.3872** vs the study's 439.387189 |
| Data provenance | 8 485 / 6 943 / 6 635 / 9 283 / 18 197 rows, every header claim re-checked against its body |
| Fresh-pull overlap | 6 000 overlapping rows across four symbols, **0** OHLC mismatches |

**What was NOT verified, and cannot be with these sources:** that the modelled
option prices resemble any price that ever existed. They are a construction from
VIX, not a quotation.

Do not modify a `SKILL.md` from this directory; the study is evidence, not a
skill.
