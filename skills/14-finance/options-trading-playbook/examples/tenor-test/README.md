# Tenor test — does tenor buy edge, or only change the clock?

**One structure, one view, nine DTE buckets, three indexes.**
Holding the structure and the view constant, how do expectancy net of cost, the
daily theta yield on risk, tail risk, positivity-by-horizon, sample adequacy and
model (skew) sensitivity change as the time to expiry at entry goes from one week
to a LEAPS?

**Every option number in this study is `[MODELED]`.** There are no historical
option quotes in these feeds. Read §4 before using any figure.

- Findings / narrative → [`FINDINGS.md`](FINDINGS.md)
- Every table verbatim from a real run → [`RESULTS.md`](RESULTS.md)
- Raw stdout of that run → `run-output.txt`
- Independent re-derivation → `handcheck.py` → `handcheck-output.txt`

---

## 1. Sources, pull date, and provenance

| Series | Source | Interval | Pulled | Rows | First | Last |
|---|---|---|---|---|---|---|
| `AMEX:SPY` | TradingView MCP `mcp__tradingview__mcp-tv-get-ohlcv` | `1D` | **2026-10-14** | 8 485 | 1993-01-29 | 2026-10-14 |
| `NASDAQ:QQQ` | same | `1D` | **2026-10-14** | 6 943 | 1999-03-10 | 2026-10-14 |
| `AMEX:IWM` | same | `1D` | **2026-10-14** | 6 635 | 2000-05-26 | 2026-10-14 |
| `TVC:VIX` | same | `1D` | **2026-10-14** | 9 283 | 1990-01-03 | 2026-10-14 |
| `TVC:US03M` | same | `1D` | **2026-10-14** | 18 197 | 1954-01-04 | 2026-10-14 |

These are the **same five 1D series the sibling studies already pulled**, carried
forward rather than re-pulled:

```
index-options-test   first pull            2026-10-14
      |
leg-count-test       carried, re-verified  2026-10-15
      |
tenor-test           carried, re-verified  2026-10-15   <- this study
```

`carry_data.py` does not trust the files: it re-reads the sibling header's own
`rows=` / `first=` / `last=` claims and refuses to carry a series whose header
disagrees with the body beneath it, records the SHA-256 of the body, and re-checks
the sibling's `_check_<SYM>_recent.csv` audit fixture session by session. That
fixture is an audit trail, **never a strategy input**.

`data/*.csv` provenance lines, verbatim from the carried SPY file:

```
source=TradingView MCP tool mcp__tradingview__mcp-tv-get-ohlcv
symbol=AMEX:SPY  interval=1D  fields=OHLCV
pulled=2026-10-14 (UTC date of the sibling pull)
CARRIED from ../index-options-test/data/SPY_1d.csv -- same tool, same pull date
carried_by=pull_data.py  carried=2026-10-15
VERIFIED before carry: the sibling header's own rows/first/last claims were re-checked against its body and matched
sha256(body of the carried file)=8c9fd9d9cc75fc7430e64df2a2b17218e73a6522bb0381fc7df7c4c32008a596
rows=8485  first=1993-01-29  last=2026-10-14
date is the exchange session date, rendered as the UTC calendar date of the bar timestamp
split-adjusted, regular session only
volume is as reported by the source, in shares (unadjusted for splits)
PRICE-ONLY series. No dividends or distributions. Not a total-return series.
carried_by=carry_data.py  carried=2026-10-15  from=...\leg-count-test\data\SPY_1d.csv
CARRIED, not re-pulled. These are the same 1D series pulled on 2026-10-14; a re-pull would return the same bars through a tool result.
VERIFIED at carry: the source header's own rows/first/last claims were re-checked against the body it sits above and matched.
sha256(body of the carried file)=8c9fd9d9cc75fc7430e64df2a2b17218e73a6522bb0381fc7df7c4c32008a596
```

Carry verified: **6 000 overlapping sessions against the fresh validation pull,
0 OHLC mismatches.**

The **common window** (identical construction to the sibling studies — the
intersection of the five series, starting at the first session on which every
index has a 200-session SMA) is:

```
2001-03-13 … 2026-10-14     6 436 sessions     25.59 years
306 complete months   102 complete quarters   24 complete years
```

## 2. How to re-run

```bash
cd skills/14-finance/options-trading-playbook/examples/tenor-test

export PYTHONIOENCODING=utf-8
py -3 carry_data.py     # re-carry + re-verify data/*.csv from the sibling study
py -3 study.py          # ~48 s.  Writes run-output.txt (stdout) AND RESULTS.md,
                        # and out/*.csv.  Deterministic: no RNG, no clock,
                        # no network.
py -3 handcheck.py      # ~3 s.  Independent re-derivation + by-hand checks.
```

`study.py` and `handcheck.py` are stdlib-only (no PyYAML, no numpy, no tiktoken).
`study.py` imports one thing outside itself: the sibling timeframe engine's
`bucket_key` from
`skills/14-finance/timeframe-performance-statistics/scripts/timeframe_stats.py`,
so the M/Q/Y buckets here cannot disagree with that engine's. `handcheck.py`
imports **nothing** from `study.py` and nothing from that engine either.

## 3. The pre-registered grid, and one arithmetic correction to the brief

The brief's own enumeration and its own cell count do not agree, so the count is
reconciled here rather than quietly matched to either number.

**Structures — the brief enumerates SEVEN, not six.** 1-leg: long call ~50Δ;
cash-secured put ~16Δ. 2-leg: short put spread ~16Δ/5-wide; bull call debit
spread ~50Δ/25Δ; covered call (stock + ~30Δ call). 4-leg: iron condor ~16Δ
shorts/5-wide wings; iron butterfly ATM short/5-wide wings. All **seven** are
run. The brief's `6 structures × 8 tenors = 48 cells` matches neither its own
list nor its own tenor set.

**Tenors — nine are measured, not eight.** The brief lists eight
(7, 14, 30, 45, 60, 90, 180, 365) and then, in the same paragraph, says
`>365 LEAPS as 730` and describes the 730-day cell's sample size
("~12 non-overlapping trades"). 730 is therefore a measured tenor.

```
7 structures × 9 tenors = 63 cells per index
   × 3 indexes (SPY, QQQ, IWM) = 189 sleeves
   × 3 variants               = 567 simulated sleeves
```

The run prints `CELLS ACTUALLY STATISTICISED (variant BASE): 63` and checks it
against the declared 7 × 9, so the reported grid size is asserted against the
grid that actually ran. **0DTE is not a measured tenor** and no 0DTE cell is
counted (§5).

### Bucket boundaries — `options-risk-engineer`'s exact partition

`0DTE (same session) · weeklies 1–7 · gamma shoulder 8–20 · monthlies 21–60 ·
quarterlies 60–120 · annuals 121–365 · LEAPS >365`

Two of the owning skill's labels **overlap**, and an assignment had to be chosen
*and declared before the first run*:

| Tenor DTE | Bucket used here | Note |
|---|---|---|
| 7 | weeklies | |
| 14 | gamma shoulder | |
| 30, 45 | monthlies | |
| **60** | **quarterlies** | 60 is inside both `monthlies 21–60` and `quarterlies 60–120`. Assigned to the **later** bucket, following the owning skill's rule to assign by the position's own gamma and never to round down to the gentler bucket. |
| 90 | quarterlies | |
| 180 | annuals | |
| **365** | **annuals** | `LEAPS >365` excludes 365. |
| 730 | LEAPS | |

Those two calls are the only judgement made about the buckets, and §9 of
`RESULTS.md` reports them back to the owning skill as a real ambiguity in its own
two tables (a 60-DTE position resolves to different hard deadlines — 21 DTE vs
45 DTE — and different roll windows under the two labels).

### Design, declared before the run

- **Entry programme:** sequential and **non-overlapping**. The first trade opens
  on the second session of the window (the first needs a prior session to be its
  signal), exits on the first session on or after `entry + tenor days`, and the
  next trade opens on the session **after** that expiry. The sleeve is always in
  the market.
- **Entry** at the session OPEN; **strikes solved from the SIGNAL close** (the
  prior session); **settlement at intrinsic against the real expiry CLOSE**.
- **No management.** No stop, no profit target, no roll, no partial close.
- **R** = the structure's own modelled **maximum loss** per contract, the exact
  piecewise-linear minimum over `{0, 3S} ∪ {strikes}`. All seven structures are
  bounded (the covered call's short call is covered by stock), so no stated-stop
  normalisation is used anywhere.
- **Cost (headline `LOW`)** = `($0.65 + $0.025 × 100)` per ticket per
  contract-leg, one ticket per leg → **$3.15 per leg** ($3.15 / $6.30 / $12.60
  per unit for 1 / 2 / 4 legs). The covered call also pays 5 bps round trip on
  its stock leg. `HIGH` doubles the spread widening; `RT_LOW` doubles every
  ticket (`cost-drag-per-leg-and-per-rung.md`'s round-trip convention). **A leg
  that expires has no closing ticket**, which is why one ticket per leg is the
  headline.
- **E is GROSS** (settlement P&L ÷ R, before cost) so that the brief's identity
  `E_net = E − c_R` holds exactly. `p`, `b`, `p*`, `b*` and `sd` are computed on
  the same gross series; `p_net` is reported beside them.
- **`n_available`** = trades **pooled** over SPY+QQQ+IWM (the sibling studies'
  convention); `n_per_index = n_available ÷ 3`. `n_req = 4(sd/|E|)²`.
- **Declared width `W`** for the `credit/width` column: `$5.00` for the four
  wing structures; for the cash-secured put the short strike `K` (the cash
  actually secured); for the covered call the underlying entry price (the
  notional); **no width at all** for the naked long call — its "credit" is a
  DEBIT and only its debit/notional is meaningful.
- **`theta/day/R`** = median credit (dollars) ÷ (tenor days × median R). The
  brief's derivation. A debit structure carries a negative credit and therefore a
  negative (costly) daily yield.
- **Skew variants:** `SKEW_SOLD_P15` (+1.5 vol points on sold legs) and
  `SKEW_SOLD_M15` (−1.5). Strikes are held fixed, so a difference between two
  variants is a pure pricing effect. **Both directions are reported** because the
  sibling studies established that this model cannot say which is right; this
  study does not contradict that.

## 4. Modelling limitations — the full list

### Inherited from the sibling studies (unchanged)

1. **No bid/ask in the quote.** A flat per-contract cost is charged, but the
   quote itself is a mid. A 4-leg structure is assumed to fill as one ticket:
   four legs' worth of legging risk is invisible here and every 4-leg `E_net` is
   optimistic relative to a real fill.
2. **No skew surface.** One vol prices every strike, so the sold leg is priced
   at the same vol as the wings. Test 5 sizes the direction-ambiguous part.
3. **No term structure.** One vol — the 3-session-lagged VIX, a ~30-day vol —
   prices **every tenor from 7 DTE to 730 DTE**. This is the single largest
   weakness of a study whose subject *is* tenor, and it is not repairable from
   these feeds. A real 730-DTE option has its own implied vol, its own skew and
   its own dividend assumptions.
4. **No early exercise, no assignment.** SPY/QQQ/IWM options are **American and
   physically settled**; every leg here is priced European and cash-settled. The
   annual probability of an exercise event is roughly proportional to the holding
   period, so a 730-DTE short call's real risk is understated by far more than a
   7-DTE one's.
5. **No pin risk.** The expiry session's close decides everything.
6. **No dividends.** The series is price-only, so every modelled call is too
   expensive and every modelled put too cheap, and the bias compounds with tenor
   (a 730-DTE modelled call omits ~2 years of dividends). The covered call's
   entire economics turn on dividends.
7. **No margin, no buying-power constraint, no liquidity limit, no partial
   fills, no tax.** A 730-DTE cell would in reality tie up margin for two years.
8. **Strikes are not rounded to exchange increments.** A real SPY chain is
   $1-wide; a solved strike may sit up to $0.50 off a listed one. At 0DTE the
   listing grid is the same size as the whole modelled move, so the rounding
   error is proportionally worse there than anywhere else.
9. **One contract per unit, integer, always fillable at the modelled mid.**

### New limitations this study creates

- **N1 — No intraday path.** The bars are daily. 0DTE P&L is decided by the
  intraday path, so **no multi-year 0DTE backtest is reported**. 0DTE is handled
  analytically, plus one clearly-labelled `[ILLUSTRATIVE]` computation that
  **cannot be extrapolated**. See §5.
- **N2 — Fixed dollar wing.** Every defined-risk structure uses a $5.00 wing at
  **every** tenor, but one standard deviation of the terminal distribution is
  `S·σ·√T`, which grows as `√T`. So the same $5 wing is **1.44 standard
  deviations at 7 DTE and 0.15 at 730 DTE** (at the window-median index price).
  Part of any apparent "tenor effect" on a 5-wide structure is therefore this
  convention rather than the tenor. The `W/(Sσ√T)` column is printed in every
  per-cell table so the drift is visible, and **Appendix A** re-runs two
  structures with the wing re-solved to hold 0.15σ at every trade — the only way
  to separate the tenor effect from the width convention.
- **N3 — The entry calendar differs by tenor.** The 7-DTE programme enters
  1 100 times per index and the 730-DTE programme 12 times, at different dates.
  A tenor difference is therefore a difference in holding period *and* in which
  dates were sampled.
- **N4 — One vol per tenor is the VIX, so the tenor comparison is a comparison
  at a fixed input vol**, not at the vol the market would actually charge. Every
  long-tenor cell is priced with a ~30-day vol, so it is cheap or rich relative
  to reality by an unknown sign.
- **N5 — The risk budget is 10 × R**, and for a 1-leg long option R *is* the
  debit, so the budget moves with the index and with √T across a window in which
  SPY went 43 → 770. The budget is re-set to the position in force each session
  (the sibling convention), which keeps the return series meaningful at both
  ends, but "10R" is 10 different dollar amounts on the first and last day.
- **N6 — The long-option cells are long the realised equity risk premium.** The
  model prices with the T-bill rate `r` while the *realised* path drifted at
  `r + ERP`. Any long-premium cell's `E` therefore contains the risk premium, and
  it **scales with tenor** because the premium accumulates over the holding
  period. The monotone rise of `E_net` for S1/S4/S5 into the LEAPS bucket is
  mostly this, not an edge in the options.
- **N7 — No vega P&L path.** Vol is a function of the lagged VIX close, so a
  position does experience some mark-to-market vol movement — but this is a
  3-session-lagged series, not a live surface, and the long-tenor cells' vega
  exposure is not measured.
- **N8 — One window, two crashes.** 25.59 years, 306 complete months, 24
  complete years. Enough to see a tail, not enough to grade every corner — which
  is exactly what Test 3 measures (16 of 63 cells are unmeasurable).
- **N9 — Seven structures, pre-registered, and no others.** Nothing here speaks
  to calendars, diagonals, ratios, jade lizards, or any 3-leg structure.

## 5. The 0DTE reasoning

**0DTE is deliberately NOT in the 63-cell grid.** The reason is specific: a 0DTE
position's P&L is decided by the **intraday path** — whether the strike was
touched at 11:00 or at 15:55, what the surface did between, whether the position
was stopped — and a daily open/high/low/close bar cannot see any of it. Reporting
a multi-year 0DTE backtest from these bars would be fabricating a result the data
cannot support.

What the study does instead:

1. **An analytic block (§12 of `RESULTS.md`)** derived from the same pricer.
   `Γ_ATM ∝ 1/√T`, so 30 DTE → 0.25 DTE multiplies ATM gamma by
   `√(30/0.25) = 10.954`; this study's pricer returns **10.959×** `[COMPUTED]`
   (an exact match, because the pricer *is* Black-Scholes). The same `1/√T`
   multiplies the **daily decay in dollars**, while the position's value falls by
   that same factor — so the decay **as a fraction of the premium** scales as
   `1/T`: **1.67% per day at 30 DTE against 200% per day at 0.25 DTE**, a 120×
   ratio `[COMPUTED]`.
2. **The cost-per-ticket arithmetic against a sub-$0.20 credit.** A 0DTE ticket
   costs the same as any other. At the headline LOW setting a 2-leg ticket is
   `2 × ($0.65 + $0.025 × 100) = $6.30`; on a **$0.05 credit that is 126% of the
   entire premium** (226% at HIGH prices), falling to 32% (56%) on a $0.20
   credit. Both readings are printed side by side — cost as a share of *premium*
   (what a high-frequency 0DTE seller pays) and cost as a share of *R* (what a
   risk-budget comparison pays). They answer different questions.
3. **One `[ILLUSTRATIVE]` held-to-settlement computation (`RESULTS.md` §13)**,
   in its own section, with its own caveat block, entering at the session open
   and settling at the session close. It is not a 0DTE result: no intraday stop,
   no intraday mark, no path. Both structures' gross `E` is negative, which is a
   statement about pricing a 0.25-day option off a 30-day VIX, not about 0DTE
   trading. The one number in it that would survive a real simulator is the
   cost arithmetic: a **5.5-cent-per-share credit against a $6.30 ticket is 114%
   of the premium**.
4. **The 0DTE share-of-volume figure is refused.** The widely quoted
   "0DTE = 59% of SPX volume" sits on a **marketing page with no as-of date**
   `[ESTIMATED — undated vendor marketing page]`. Per
   `trading-decision-data-catalogue` (`SKILL.md:163` and
   `references/options-positioning-data.md` §3.1), an undated market-share
   statistic is not a statistic, it can be neither right nor wrong, and it must
   **not be put in a chart** — with the reason stated when asked. **This study
   reports no 0DTE share-of-volume number at all, dated or not.**

## 6. What the verification found

### Determinism
Two full runs of `study.py`, `diff`ed: **stdout byte-identical, `RESULTS.md`
byte-identical.** No RNG, no clock, no network, no dict-iteration-order
dependence, LF output throughout.

### Independent re-derivation (`handcheck.py`)
`handcheck.py` imports **nothing** from `study.py`. It re-implements the window,
the implied-vol context, the tenor schedule, the strike solve (`0.5·erfc(−x/√2)`
instead of `0.5·(1+erf(x/√2))`; a 200-iteration bisection with a 1e-15 relative
stop instead of 80 iterations), the entry premium, the settlement, `R` (a direct
payoff scan rather than the kink-set argument), the cost, and the per-cell
statistics — then compares against `out/cells_summary.csv`.

**It re-derives all 63 BASE cells across 11 fields. Worst absolute gap, per
field, across all 63 cells:**

| field | worst absolute gap |
|---|---|
| `n_available` | 0.000000000000 |
| `p_gross` | 0.000000000000 |
| `b` | 0.000000000004 |
| `E_gross` | 0.000000000000 |
| `sd` | 0.000000000001 |
| `n_req` | 0.000000026619 |
| `c_R` | 0.000000000000 |
| `E_net` | 0.000000000000 |
| `theta_pd_R` | 0.000000000000 |
| `R_dollars_med` | 0.000000000006 |
| `credit_med` | 0.000000000006 |

**Every cell's maximum relative gap is 0.0000000000** at ten decimal places.
The residual is floating-point noise in a statistic (`n_req`) that is a squared
ratio of two nearly-equal numbers, not a definitional disagreement.

**The handcheck earned its keep twice, and both findings were bugs in the
STUDY, not in the checker:**

1. **A silently wrong strike bracket (a real bug in the study, inherited from
   the sibling studies' solver).** The sibling solvers bisect on
   `[0.20 S, 1.60 S]` with **no straddle check**. On a 730-DTE ticket priced at
   a 2008-style 80% vol, `σ√T ≈ 1.13` and the **25Δ call strike sits near
   8.4 × spot** — outside that bracket. Bisection then converged silently onto
   the bracket endpoint and returned a wrong strike with no warning. The
   handcheck raises instead, which is how it was found. `study.py`'s bracket is
   now `[0.02 S, 100 S]` with an explicit straddle assertion that raises.
   *This is why an independent re-derivation is worth the effort: the two files
   agreed on 61 of 63 cells while both were wrong.*
2. **A credit-accounting bug in the handcheck itself** (summing the underlying
   leg into the covered call's premium) — found and fixed by the gap table, and
   recorded in the file rather than removed.

### By-hand checks (`handcheck.py` §H1–H3)
- **H1** — one leg priced at **7, 90 and 730 DTE** from stated inputs
  (`S = K = 100, r = 4.25%, σ = 20%`), with `d1`, `d2` printed so the arithmetic
  can be repeated on a calculator; the normal CDF is validated against an
  independent **Simpson quadrature of the standard normal density** to ~1e-10;
  and put-call parity `C − P = S − Ke^{−rT}` is checked at all three tenors
  (agreement to 1e-9).
- **H2** — `theta-per-day per R` computed by hand for cell (S3, 30 DTE), with the
  arithmetic shown, matching `study.py` to 8 significant figures; plus the
  reciprocal reading ("the position collects 1R in 276 days at this rate, against
  a 30-day hold").
- **H3** — one **730-day** structure settled against the real path, leg by leg,
  with the real signal close, entry open, expiry close, `σ√T`, `r`, each strike,
  each intrinsic and each leg's P&L printed. Trade #1 of the S3/730 programme on
  SPY: signal 2001-03-13 close 120.02, entry 2001-03-14 open 117.05, expiry
  2003-03-14 close **84.13** — the short put spread finishes at exactly −1.000R,
  which is the fixed-dollar-wing point made concrete: a 5-wide wing on a $117
  index is 4.3% of notional and cannot survive 2001–2003.

## 7. Files

```
tenor-test/
├── carry_data.py          carry + re-verify data/*.csv from the sibling study
├── study.py               the study.  Deterministic, stdlib, LF.
├── handcheck.py           INDEPENDENT re-derivation + by-hand checks
├── data/                  SPY, QQQ, IWM, VIX, US03M 1D + audit fixtures
├── out/                   cells_summary.csv + test1..test8 + appendixA
├── logs/                  run-progress.txt, determinism pair (run1/run2, RESULTS1)
├── run-output.txt         raw stdout of the last full run
├── handcheck-output.txt   raw stdout of the independent check
├── RESULTS.md             every table, verbatim from that run
├── FINDINGS.md            the honest narrative
└── README.md              this file
```

`out/cells_summary.csv` is the machine-readable spine: one row per cell (63
rows) with all 53 per-cell statistics, including `n_available`, `n_req`,
`measurable`, `p_gross`, `p_net`, `b`, `E_gross`, `sd`, `c_R`, `E_net`,
`E_net_high`, `E_net_rt`, `c_R_star`, `credit_over_width`,
`credit_over_notional`, `R_dollars_med`, `credit_med`, `frac_at_max`,
`p05/p25/p50/p75`, `theta_pd_R`, `ann_R`, `ann_R_net`, `dd_R`, `worst_trade`,
`worst1`, `L_actual`, `L_expected`, `pos_M/Q/Y`, `inverted_MY`, and the entry
Greeks.
