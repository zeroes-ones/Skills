# weather-deep-test — the widest realistic cross-asset universe, one pre-registered run

**Status:** complete. Every number in `RESULTS.md` is the verbatim stdout of a real
run on the real data in `data/`. Nothing was typed by hand, and nothing was carried
over from a sibling study except the SPY price file, which was verified row-for-row
before it was used.

**Data pull date:** 2026-10-14 (UTC) for every series in `data/`.
**Primary window:** 2005-09-30 → 2026-10-14 = **21.04 years** (SPY's own session
calendar, 5,292 book days). Chosen to match the predecessor studies so the results
are comparable, not because of anything in the data.
**Reduced window:** 1998-12-22 → 2026-10-14 = **27.81 years**, so the 2000–2002
dot-com bear is inside at least one book.

---

## 1. What this study is for

The desk owner's goal is to **maximise the fraction of market conditions in which
the book is profitable**, honestly. The whole exercise rests on one identity:

```
P(positive period)  ~=  Phi( annual_Sharpe * sqrt(period_fraction) )
```

Positivity is therefore bought with **Sharpe**, and Sharpe is bought with **sleeves
that are genuinely uncorrelated**. This study builds the widest realistic
cross-asset universe the data source will resolve, pre-registers six sleeves and
three books over it, runs once, and reports what the measured positivity frontier
actually is — including every losing year, every negative regime cell, the worst
drawdown and the full cost drag.

The question it answers is **not** "how do I make more money". It is "how much of
the weather can this be made to survive, and at what price in return".

---

## 2. Pre-registration — declared before the first run

Everything below was fixed before `study.py` was executed for the first time. It is
also printed at the top of every run, and written to `out/preregistration.txt`.

### 2.1 The universe (screened on EXISTENCE only)

No sleeve, instrument, rule or weight was chosen by looking at a result. The only
screen applied is **existence**: does the data source resolve the symbol, and does
it have prints over the window. Which symbols resolved and which did not is
recorded in §4 and in `out/data_inventory.csv`.

The 31-instrument tradable universe:

| family | instruments |
|---|---|
| equity beta | SPY, QQQ, IWM, MDY, DIA |
| duration / credit | TLT, TLH, EDV, IEF, SHY, TIP, LQD, HYG, EMB |
| real assets | GLD, SLV, GDX, DBC |
| property | VNQ |
| international equity | EEM, EFA, EWJ, FXI, ILF, EWZ |
| dollar | UUP |
| sectors | XLE, XLU, XLK, XLP, XLV |

Plus, as **state variables only** (never traded): `VIX`, `US03M` (cash), `US10Y`
(used only by the modelled `BOND10M`), `US02Y`, `US30Y`, `DXY`, and `BIL` (used
only to demonstrate why a T-bill ETF's price is not cash — see §6).

### 2.2 The sleeves

| sleeve | rule |
|---|---|
| **T — trend programme** | every instrument in the universe; long when its own close > its own SMA(200) on the rebalance close, flat below; portfolio is **inverse-volatility** weighted (60-day trailing vol) over the instruments that exist at that date, renormalised to 1; **rebalanced monthly**; flat capital earns the cash rate |
| **C — carry / credit** | long `HYG`, short `IEF`, at inverse-vol weights summing to 1; the short leg's proceeds earn the cash rate; the long leg is credited its estimated dividend and the short leg **pays** it. **Live only when BOTH legs exist**; cash before that |
| **V — variance risk premium `[MODELED]`** | monthly short 30-DTE put spread on SPY; short strike at \|delta\| = 0.16 under IV = VIX(t−3); long strike 5% lower; short strike priced at ATM + 1.5 vol pt, long at ATM + 3.0 vol pt; daily Black–Scholes mark; **settled at intrinsic against the real SPY path**; return = P&L ÷ the spread **width** |
| **H — crisis hedge** | H = 0.5 × H_a + 0.5 × H_b, fixed. **H_a**: equal-risk long GLD/UUP when VIX(close) > SMA(50) of VIX, else flat (cash). **H_b `[MODELED]`**: always-on long 60-DTE 5%-OTM SPY put overlay with a premium budget of 5% of sleeve capital **per year**, spent at 1/12 a month |
| **X — cross-sectional momentum** | each month hold the top **N = 5** instruments by trailing 126-day (~6-month) return, equal-weight, rest cash. **Not tuned** |
| **B — baseline** | 100% `SPY` buy and hold |

Declared (not searched) variants reported but used in **no** book: `C_hyg` (long
HYG only), `V_s0` and `V_s3` (the VRP at 0 and 3.0 vol points of skew steepness),
`X8` (N = 8).

### 2.3 The books — fixed weights, never searched

| book | weights |
|---|---|
| **BOOK** | T 0.40 + X 0.15 + C 0.15 + V 0.10 + H 0.10 + CASH 0.10 |
| **BOOK-NOV** | T 0.45 + X 0.17 + C 0.17 + H 0.11 + CASH 0.10 (the same book without the modelled V sleeve) |
| **BOOK-VT** | the BOOK weights passed through **one** uniform, declared risk normalisation: every sleeve scaled by `k = min(1, 4% / its own annualised vol)`, released weight to CASH. Resolution: T 0.3954, X 0.0315, C 0.1053, V 0.0022, H 0.1000, CASH 0.3655 |
| **REDUCED** | T 0.40 + X 0.15 + V 0.10 + H 0.10 + BOND10M 0.15 + CASH 0.10, over the **existence-restricted** 9-instrument universe that has a print on 1998-12-22 (SPY, MDY, EWJ, DIA, XLE, XLU, XLK, XLP, XLV). CARRY is set to 0.00 because neither HYG nor IEF lists before 2002/2007 |

**Why BOOK-VT exists, stated plainly.** The sleeves are not naturally comparable in
risk: the trend sleeve runs at ~4% annualised vol and the `[MODELED]` VRP sleeve at
~179%. A fixed-weight sum of incomparable risks is unreadable, and the desk
principle quoted in the brief is itself *equal-risk, not optimised*. BOOK-VT applies
one uniform rule to every sleeve, never by inspection of a result. It was added
after the first run showed the V sleeve's variance drag dominating the book — that
is disclosed here and in `FINDINGS.md` §4 rather than hidden. **Scaling cannot
create edge; it can only change how much of the same edge you own.** The
pre-registered BOOK and BOOK-NOV are unchanged and are reported first everywhere.

### 2.4 Costs and the success bar

* Round-trip cost levels: **0, 5 and 20 bps**. One-way cost per unit notional
  traded is half the round trip: `cost_j = (round_trip/2)/10000 × one-way notional
  traded on day j`, charged **in the return**, never by shrinking a dollar value.
* **Success bar, declared before the run:** a book is "weather-proof enough" iff it
  is **positive in ≥90% of years AND ≥75% of quarters AND has Sharpe > 0.8 AND CAGR
  above cash**.

---

## 3. How the study is put together

```
study.py              the run.  Stdlib only.  Deterministic.  LF output.
handcheck.py          an INDEPENDENT re-derivation.  Imports nothing from study.py
                      and nothing from the sibling engine.
pull_ohlcv.py         MCP payload on disk -> data/*.csv, with provenance headers
reuse_sibling_data.py extends SPY back to 1993 from ../frontier-test, verifying the
                      overlap row-for-row first
verify_sources.py     cross-checks data/ against every sibling study's independent
                      pull of the same symbol
make-results.py       assembles RESULTS.md from the captured stdout
data/*.csv            the inputs, six-column OHLCV behind `# PROVENANCE:` headers
out/*.csv, *.txt      every intermediate the run writes, so nothing is un-auditable
logs/*.txt            raw stdout of each step
```

`study.py` **imports** `bucket_key`, `aggregate_bucket`, `sample_sd`,
`max_drawdown`, `lag1_autocorr` and `n_effective` from
`../../timeframe-performance-statistics/scripts/timeframe_stats.py` rather than
re-implementing them, and refuses to run if that engine is missing.

### Re-running

```bash
export PYTHONIOENCODING=utf-8
cd skills/14-finance/equity-trading-playbook/examples/weather-deep-test

py -3 verify_sources.py                       # data cross-check, ~1 s
py -3 study.py      > logs/run-output.txt     # the run, ~80 s
py -3 handcheck.py  > logs/handcheck-output.txt
py -3 make-results.py                         # -> RESULTS.md
```

To re-pull the data from scratch, re-issue the `get_ohlcv` calls listed in
`pull-output.txt` (one per symbol, `interval="1D"`, `count=8000`,
`format="columns"`), then:

```bash
py -3 pull_ohlcv.py --results <tool-results dirs> --out data --pull-date 2026-10-14
py -3 reuse_sibling_data.py --data data --sibling ../frontier-test/data --name SPY
```

Determinism: `study.py` was run twice and the two stdouts are byte-identical, and
all 36 artefacts in `out/` hash identically across runs.

---

## 4. Symbols: what resolved, what did not

**38 series resolved.** Three source symbols failed and were recorded, then
retried on the exchange code the source actually publishes them under:

| requested | result | resolution |
|---|---|---|
| `AMEX:SHY` | `error: invalid symbol` | resolved as **`NASDAQ:SHY`** |
| `AMEX:TLT` | `error: invalid symbol` | resolved as **`NASDAQ:TLT`** |
| `AMEX:EMB` | `error: invalid symbol` | resolved as **`NASDAQ:EMB`** |

Same funds, different exchange code. Nothing was substituted silently: the exchange
code actually used is in each file's provenance header, and `AMEX:TLH` — the one
Treasury ETF that *did* resolve on AMEX — is recorded as such.

Every other requested symbol resolved: `EFA`, `LQD`, `UUP`, `TIP`, `SLV`, `EWJ`,
`FXI`, `ILF`, `EWZ`, `GDX`, `XLE`, `XLU`, `XLK`, `XLP`, `XLV`, `MDY`, `DIA`, `SHY`,
`TLH`, `EDV`, `EMB`, `US10Y`, `US02Y`, `US30Y`, `DXY`.

**Duration and curve pairs, as requested.** Duration ladder resolved on real
prices: `SHY` (1–3y) → `IEF` (7–10y) → `TLH` (10–20y) → `TLT` (20+y) → `EDV`
(extended). A pure curve pair on prices does not exist as an ETF pair, so the curve
is carried as **yield indices** — `US02Y`, `US10Y`, `US30Y` — which are recorded as
**not tradable** and used only as state/inputs (`US10Y` also feeds the modelled
`BOND10M`). Yield indices have no print on 16–18% of book sessions; that gap is
counted in `out/data_inventory.csv` and carried forward rather than interpolated.

**Cross-check against the sibling studies.** `verify_sources.py` compares this
study's `data/` against four sibling studies' independent pulls of the same symbols
from the same tool on the same date:

```
TOTAL: 44 file pairs compared, 311224 shared dates, 311194 identical,
       0 price disagreements, 30 volume-only warnings
```

**Zero price disagreements over 311,224 shared dates.** The 30 volume-only
differences are all on the still-forming final bar except 19 on `EEM`, which are
source-side volume revisions on old rows; every price on those rows is identical.

**One deliberate reuse.** `SPY` since 1993 is 8,485 bars, one more than a single
8,000-bar `get_ohlcv` response can return (the cap truncates the *old* end, there is
no `has_more` to page back with). So `SPY` is the union of
`../frontier-test/data/SPY_1d.csv` (1993-01-29 → 1994-12-29) and this study's own
independent pull (1994-12-30 → 2026-10-14). `reuse_sibling_data.py` verified the
8,000-row overlap first: **7,999 identical rows and 1 last-bar volume-only
exception, 0 disagreements** before writing anything. The provenance header records
which rows came from where.

---

## 5. `[ESTIMATED]` dividends — the arithmetic, and how much of the result it is

`data/*.csv` are **price-only**. A price-only series understates total return by
roughly the dividend yield, so every result is reported **twice**: **price-only**
(as measured) and **dividend-adjusted `[ESTIMATED]`**.

**The assumption.** A **constant** annualised yield per instrument, credited at
`yield / 252` on every book session on which the instrument has a bar, proportional
to exposure (a flat sleeve earns no dividend). It is not a measured distribution
stream and it does not vary through time.

| instrument | %/yr | instrument | %/yr | instrument | %/yr |
|---|---|---|---|---|---|
| SPY | 1.80 | TLT | 3.00 | EEM | 2.30 |
| QQQ | 0.90 | TLH | 2.90 | EFA | 2.70 |
| IWM | 1.40 | EDV | 3.60 | EWJ | 1.60 |
| MDY | 1.60 | IEF | 2.60 | FXI | 2.20 |
| DIA | 1.90 | SHY | 1.90 | ILF | 4.30 |
| TIP | 2.80 | LQD | 3.40 | EWZ | 5.80 |
| HYG | 5.60 | EMB | 4.80 | XLE | 3.40 |
| XLU | 3.00 | XLK | 0.90 | XLP | 2.60 |
| XLV | 1.80 | VNQ | 3.80 | GDX | 1.20 |
| GLD / SLV / DBC / UUP / BIL | 0.00 | | | | |

Universe mean = **2.38%/yr**; SPY = **1.80%/yr**.

**The arithmetic, worked for SPY over the primary window.** The window is 21.04
years. A constant 1.80%/yr accrued daily compounds to `1.018^21.04 − 1 = +45.6%`
of cumulative return on top of the price-only path. Over 21.04 years that is an
addition of `(1+0.456)^(1/21.04) − 1 = +1.80%/yr` to CAGR, before the second-order
effect of compounding on the path — which is why the measured SPY gap is
**+1.98 pp** (price-only CAGR 9.10% → dividend-adjusted 11.08%) rather than exactly
1.80 pp.

**How much of the result is the dividend assumption:**

| series (5 bps) | price-only CAGR | `[ESTIMATED]` div CAGR | gap |
|---|---|---|---|
| SPY buy & hold | 9.10% | 11.08% | **+1.98 pp** |
| T trend | 2.88% | 4.39% | **+1.51 pp** |
| X x-sec momentum | 8.80% | 11.01% | **+2.21 pp** |
| BOOK | 7.53% | 8.68% | **+1.15 pp** |
| BOOK-NOV | 3.27% | 4.52% | **+1.25 pp** |
| BOOK-VT | 1.99% | 2.68% | **+0.69 pp** |
| REDUCED (27.81y) | 9.42% | 10.37% | **+0.95 pp** |

The honest reading: **between 0.7 and 2.2 percentage points of every CAGR in this
study is an assumption, not a measurement.** The dividend treatment moves the
positivity fractions too (BOOK: 85% of years either way, but 60.32% → 58.73% of
months, and BOOK-VT: 95% → 85% of years). Every table is therefore printed in both
treatments, and the success-bar verdict is reported for both.

---

## 6. The cash proxy — an upper bound, handled explicitly

`TVC:US03M` is a **3-month Treasury bill YIELD INDEX in percent per annum**, not a
fund. The accrual used everywhere is

```
r_cash[j] = (yield observed at the close of book session j-1 / 100) / 252
```

the previous-session rate, the same no-lookahead convention every sleeve uses for
its position.

**Three properties of this proxy, measured rather than assumed:**

1. **It is an upper bound.** A yield index is not a fund: it ignores the expense
   ratio, the bid/offer and the roll of a real T-bill portfolio, and it credits the
   full quoted yield on every business day. The measured mean rate over the window
   is `1.7634% p.a.` and cash compounds at `1.7750%/yr`.
2. **It carries forward.** `TVC:US03M` has no print on **14.00%** of the 5,291
   book sessions (741 sessions). The rate is carried forward from the last print,
   the longest gap is **2 sessions**, and the count, longest gap and rate range are
   all printed on every run and written to `out/cash_daily.csv`. This is the same
   ~14% gap a sibling study saw; it is handled rather than silently under-accrued.
3. **Cash itself was negative.** The rate goes slightly negative (minimum
   `−0.0406% p.a.`) and on **11 of 5,291 sessions (0.21%) the cash return itself was
   negative**. That matters for the frontier: it is why no book can have 100% of
   *daily* periods positive, exactly as the predecessor found.

**Why `BIL` is not used as cash.** A T-bill ETF distributes essentially all of its
yield, so its **price** is nearly flat while its holders earn the distribution.
Compounding BIL's price-only return over 2007-05-30 → 2026-10-14 gives
**−0.0045%/yr** — it measures the fee drag and the distribution, not cash. The study
computes this and prints it, rather than asserting it.

---

## 7. What is measured and what is modelled

| tag | meaning |
|---|---|
| **MEASURED** | price and `[ESTIMATED]` dividend returns of 31 listed instruments; the cash yield index |
| **`[MODELED]`** | **every option position**: the `V` sleeve, the `H_b` put overlay, and `BOND10M` |

Every `[MODELED]` number is tagged in its table header, in the CSVs, and in
`FINDINGS.md`. The VRP sleeve writes every roll's exact inputs and resulting
contract to `out/vrp_rolls.csv` (signal date, roll date, expiry, S0, VIX(t−3), IV,
σ_short, σ_long, r, q, K1, K2, width, credit, credit/width) so the model can be
audited roll by roll rather than trusted.

`BOND10M` exists only so the reduced long-window book has a duration leg before
IEF/TLT list in 2002: `r_j = −7.5 × Δy10 + y10(j−1)/252` with a **constant**
modified duration of 7.5. Convexity, roll-down and the maturity drift of a real bond
are all ignored, which is why every number from it is tagged.

---

## 8. Limitations — the full list

**Data**

1. `data/*.csv` are **price-only**. Dividends enter only through the `[ESTIMATED]`
   constant yields above; the `[ESTIMATED]` variant is an assumption, not a
   measurement. Between 0.7 and 2.2 pp of every CAGR is that assumption.
2. One source, one pull date (2026-10-14). No second vendor was consulted *by this
   study*; the sibling `regime-study` did cross-check SPY/QQQ/TLT/GLD against a
   second broker, and `verify_sources.py` reproduces this study's agreement with
   those files (0 price disagreements over 311,224 shared dates).
3. The final bar of every series is still forming and may change. Every comparison
   treats a last-bar difference as a warning, never a match.
4. Yield indices (`US03M`, `US02Y`, `US10Y`, `US30Y`) and `DXY` have no print on
   14–20% of book sessions. They are carried forward, never interpolated, and the
   gap counts are reported.
5. ETF price histories begin at each fund's listing, so the 21.04-year window
   cannot see 2000–2002. The REDUCED book covers 1998-12-22 onwards for that
   reason, at the cost of a 9-instrument trend universe.
6. Splits are adjusted; distributions are not.

**Method**

7. **Monthly rebalancing only.** Every rule reads its signal at a month end and
   holds it for the month. Nothing here says what a faster or slower cadence would
   do.
8. **Inverse-volatility weights are in-sample-free but the vol window is 60
   sessions**, and instruments without 60 sessions of history are simply absent
   from the normalisation. A real book would hold something in their place; here the
   freed weight goes to cash.
9. **No shorting anywhere except the `C` sleeve's IEF leg.** The predecessor showed
   long-only trend is structurally negative in the DOWN state precisely because it
   cannot go short. That limitation is inherited, not fixed.
10. **The regime terciles are an in-sample partition** of the whole window. The grid
    is a description of the weather, not a tradable signal, and the breakpoints are
    fixed ex post.
11. **Only one signal lookback per sleeve.** SMA(200) for T, 126 sessions for X,
    SMA(50) on VIX for H_a. No sensitivity range is reported for these; changing
    them would be a new pre-registration, and tuning them here would be exactly the
    error the brief forbids.
12. **`X`'s N = 5 is declared, not chosen.** `X8` is reported as a sensitivity, and
    the two are close (11.01% vs 10.75% CAGR) — which is itself evidence that N is
    not where the edge lives.

**Modelled sleeves — read these before trusting any V or H_b number**

13. **The VRP sleeve's P&L is almost entirely a function of one unmeasured
    assumption**: the skew premium applied to the short strike. At 0 vol points of
    assumed skew it returns **−2.54%/yr**; at 1.5 (the base case) **+10.01%/yr**; at
    3.0 **+15.50%/yr**. The sign of the sleeve flips inside that range. The
    predecessor's `+1.5 vol points` break-even is carried forward and re-reported
    here as a sensitivity, not as a fact.
14. **The VRP sleeve is uninvestable at full-width sizing.** Its daily mark can lose
    ~100% of the posted width in a single session when SPY gaps through both
    strikes, so at `units = capital / width` it compounds to a **−99.83%** drawdown
    while showing the *highest* Sharpe of any sleeve (0.74). This is the single most
    important modelling caveat in the study: **a Sharpe ratio cannot see ruin risk.**
    BOOK-VT exists to show the effect of sizing alone on the same trade.
15. **Realised volatility in the VRP model is taken from VIX(t−3)**, i.e. the model
    never sees the realised path except at settlement. It also prices with a
    **fixed** IV for the life of each spread, so the model contains no vol-of-vol
    P&L and no vol-mean-reversion effect inside a month.
16. **The option model has no bid/offer, no early exercise, no pin risk and no
    dividend risk**, and the cash rate is floored at zero inside the pricing
    function. `VRP_SPREAD_PCT`, `VRP_DTE` and `VRP_DELTA` are single declared values
    with no sensitivity range.
17. **The `H_b` overlay is a cost model, not a hedge model.** It buys 5%-OTM puts on
    a fixed premium budget and settles at intrinsic; it does not model rolling the
    strikes, and its 5%/year budget is a declared choice, not an optimum.
18. **`BOND10M` holds modified duration constant at 7.5.** This is wrong in exactly
    the periods it is used for (1999–2002, when the long bond rallied hard), so the
    REDUCED book's dot-com coverage is the weakest number in the study.

**Statistical**

19. **20 complete years** in the primary window and **27** in the reduced window.
    100% of years is `20/20` or `27/27` — a very coarse, very fragile statement, and
    the frontier λ is resolved to 0.001 only.
20. **No significance testing is presented and none should be inferred.** The
    predecessor's sweep found that of 1,620 configurations only 10 cleared a
    Bonferroni bar and 0 of 5,610 cleared it at the strictest level, and that more
    iterations made results monotonically *worse*. Nothing here is exempt from that.
21. **Every threshold in the success bar is arbitrary** (90% / 75% / 0.8). It was
    declared before the run so it could not be moved afterwards, not because 90% is
    a law of nature.
22. **Overfitting by selection is not eliminated here**, only declared away: the
    universe, the sleeves and the weights were fixed in advance and never searched,
    but they were chosen by a human who had already read four prior studies.
23. **`H_a` and the VRP model share VIX**, so their independence is partly
    structural rather than economic.

---

## 9. Where things are

| file | what |
|---|---|
| `RESULTS.md` | every table, verbatim from the run |
| `FINDINGS.md` | the honest narrative: what the extra sleeves bought, where the frontier moved, what is modelled, what remains untested |
| `out/preregistration.txt` | the pre-registration as the run printed it |
| `out/summary.csv` | one row per series × dividend treatment × cost level |
| `out/years.csv`, `out/corr_yearly.csv`, `out/corr_yearly_reduced.csv` | yearly returns and their correlation matrices |
| `out/horizon.csv`, `out/lambda_frontier.csv`, `out/regime.csv` | positivity by horizon, the λ frontier, the regime grid |
| `out/vrp_rolls.csv` | `[MODELED]` the VRP model's inputs and contracts, roll by roll |
| `out/cash_daily.csv`, `out/data_inventory.csv` | the cash accrual path; every series' span and gap count |
| `out/book_weights.csv`, `out/book_daily_*.csv`, `out/sleeve_daily_*.csv`, `out/sleeve_monthly_*.csv` | the full daily and monthly return streams behind every figure |
| `run-output.txt`, `handcheck-output.txt`, `source-check.txt`, `pull-output.txt`, `reuse-output.txt` | raw stdout of each step |

---

## 10. Verification summary

| check | result |
|---|---|
| determinism | `study.py` run twice — stdout **byte-identical**; all 36 `out/` artefacts hash identically |
| independent re-derivation | `handcheck.py`, 17 checks, imports nothing from `study.py` — **largest gap 1.9e-4**, and every non-zero gap is named and explained (see `handcheck-output.txt`); 14 of the 17 agree to better than 1e-9, 12 of them to ~1e-10 |
| source cross-check | 44 file pairs, 311,224 shared dates, **0 price disagreements** |
| correlation matrix | **symmetric, diagonal exactly 1.0**, asserted in the run and re-checked by hand |
| symbols that failed | `AMEX:SHY`, `AMEX:TLT`, `AMEX:EMB` — recorded, retried on `NASDAQ:`, provenance updated |
