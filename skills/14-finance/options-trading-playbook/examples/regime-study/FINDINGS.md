# FINDINGS — what the data said, and what it cannot say

This is the honest narrative for the regime study. `RESULTS.md` holds the numbers;
this file holds the interpretation, the limits, and the list of things that were **not**
tested. Where a number is quoted here it comes from `run.txt`.

---

## 1. What was fixed in advance, and what was searched

The discipline of this study is the point, so it is worth stating precisely:

| element | status |
|---|---|
| M1, M2, M3 rule definitions (entry, exit, stop, filters) | **pre-registered** — not modified after seeing results |
| stop distance (2 × ATR(14)), entry (next open), long-only, single position | **pre-registered** |
| metric set (`p, b, E, p*, b*, sd, n_req, L, CAGR, maxDD, Sharpe`) | **pre-registered** |
| RSI thresholds and holding periods | searched **only** in Task 5, and reported as a demonstration of the danger |
| the vol-premium payoff definition | pre-registered, run as specified, and then supplemented (see §4) |

Nothing in §2–§4 of `RESULTS.md` was tuned. The three strategies were coded once and run
once; the results above are the first output, including the negative ones (M3 on EEM at
E_R = −0.016R, M3 in LOW vol at −11.2R pooled, 66 negative regime cells, and losing years
in all 12 cells).

Two things I added **after** seeing the pre-registered output, both clearly labelled in
`RESULTS.md` as additions rather than substitutions:

1. **`E_R` alongside the pre-registered `E` formula.** The pre-registered
   `E = p·b − (1−p)` measures expectancy in units of the *average loss*, not in R. For
   M3 the losses are always exactly −1R so the two coincide; for M1/M2 they do not, and
   the formula overstates. Reporting both is not a change to the rule, it is a
   disclosure that the metric needed it. The identity is `E = E_R / |avg_loss|`.
2. **The fair-strike short-vol variant.** The pre-registered payoff — collect the
   1-sigma move, pay the realised absolute move — is structurally biased positive. I ran
   it exactly as specified, then added the corrected series to find the honest answer.
   See §2.2.

---

## 2. The volatility proxy: exactly what it is, and what it cannot tell you

### 2.1 What was computed

No options implied-volatility history is available in this environment, so the study
builds a stand-in and states it plainly:

- **Collected premium** = `VIX / √252 × √21` in vol points — the 21-day move implied by
  the VIX level on the entry day.
- **Paid** = the realised absolute 21-day move of SPY, in percent.
- **R** = (collected − paid) / (2 × collected), so the risk unit is twice the collected
  premium and the maximum gain is +0.5R.
- A second, unbiased series replaces the collected premium with the *fair straddle value*,
  `0.798 ×` implied, because E|Z| = √(2/π) ≈ 0.798 for a standard normal.
- A third measure, the classic variance risk premium, is `VIX − forward 21-day realised
  vol`, which has no absolute-value artifact at all.

### 2.2 The pre-registered payoff is biased, and that matters

As specified, the proxy reports **p = 0.833, E_R = +0.1934R, +1637R total, and zero
losing years in 34 years**. That is not evidence that selling volatility is free money.
Collecting the 1-sigma move while paying the realised absolute move guarantees a positive
mean payoff, because the expected absolute value of a normal is 0.798, not 1. Roughly a
fifth of the apparent edge is that artifact.

Removing it (fair strike) leaves **E_R = +0.1158R, +980R total, and one losing year: 2020
at −7.3R**. So the honest reading is:

- **The premium is real, not imagined.** Mean VRP is **+3.62 vol points** and VIX
  exceeded the vol that followed in **82.9%** of 21-day windows. VRP is negative in
  exactly one calendar year of 34: **2008 (−2.33 vol points)**.
- **It is not free.** The worst single window — entered **2020-02-20**, VIX 15.6, implied
  21-day move 4.49%, realised **32.10%** — is **R = −3.98** on a stake whose maximum gain
  is +0.5R. One window gave back about eight typical wins. That is the whole
  "selling premium is picking up pennies" story in a single line of the table.

### 2.3 What this proxy cannot tell you — the list that matters

These are not footnotes; they are the reasons a reader should not lift the +0.1158R
number and use it as an expected P&L for a real short-premium book.

1. **VIX is the wrong instrument, by construction.** It is a 30-day constant-maturity
   implied-vol index on the **S&P 500**. It is not the IV of SPY, not the IV of any
   option anyone would actually sell, and the study applies it to a **21-day** horizon
   against VIX's 30-day tenor. Both the underlying and the tenor are mismatched.
2. **A realised move is not an option's P&L.** A short straddle's settlement is
   `premium − |S_T − K|`, so the payoff direction is captured — but the proxy has no
   **theta, gamma, vega, rho, skew, term structure, bid-ask spread, assignment,
   early exercise, margin, or roll**. A real short-premium position is path-dependent:
   it can be stopped out or margined out before expiry, which the proxy cannot represent
   and which is exactly how real short-vol books die.
3. **The proxy assumes the option is held to expiry and settles cleanly.** It cannot
   show a position that was closed early, rolled, or assigned.
4. **The fair-strike correction is an approximation.** `0.798 × implied` is the ATM
   straddle value under a lognormal, zero-skew, zero-rate model. Real index skew makes
   puts dearer than calls, so the true fair value differs, and an actual seller picks a
   strike, which changes everything.
5. **No transaction costs.** Options spreads are wide; the proxy pays none. See §3.1.
6. **Overlapping windows.** Every session is an entry, so consecutive "trades" share 20
   of their 21 days. This does not bias the mean but it badly overstates the effective
   sample size and therefore the apparent significance. The non-overlapping
   every-21st-session subset (n = 404, p = 0.854, total +79.4R) agrees on the sign and
   magnitude, which is reassuring but is not a significance test.
7. **The regime labels come from SPY.** Regime classification for the vol study uses
   SPY's trend state and vol tercile, which is defensible for an SPX-based premium but
   means "DOWN_rising" is an equity-trend statement, not a vol-regime statement.

**Bottom line on the options corner:** this study can tell you the *sign and shape* of
the risk premium — positive on average, concentrated in calm and grinding-up markets,
punctured by crisis onsets with a fat left tail — and cannot price a tradeable structure.
It is evidence about the premium, not a backtest of an option position.

---

## 3. Limitations of the mean-reversion study

### 3.1 Costs are set to ZERO — and that is material for the weaker cells

Every expectancy in `RESULTS.md` is gross. The data lets us size the omission instead of
just flagging it — these figures are produced by `study.py` §8 and are in `out/cost_sensitivity.csv`. 1R is a measured quantity (median 2 × ATR(14) ÷ entry price), so a
round trip costing `c` basis points of price costs `c / 100 ÷ (1R as % of price)` in R:

| cell | measured 1R | gross E_R | cost in R at 5 bps round trip | as % of the edge | round trip that wipes out the edge |
|---|---|---|---|---|---|
| M1 / SPY | 2.16% of price | +0.1711 | 0.0232 | 14% | **36.9 bps** |
| M1 / IWM | 3.09% of price | +0.0816 | 0.0162 | 20% | **25.2 bps** |
| M1 / EEM | 2.87% of price | +0.0033 | 0.0174 | **527%** | **1.0 bps** |

Read the last row carefully. A 5 bps round trip costs **5.3 times** M1/EEM's entire
apparent edge — the cell does not merely weaken after costs, it goes decisively negative,
and it is already negative at a **1.0 bps** round trip, which is below the spread on the instrument.
M1/IWM needs a round trip under 25 bps to stay positive. Only M1/SPY has real room:
36.9 bps of round-trip cost before the edge is gone, against a realistic SPY round trip
of about 1 bp (a one-cent spread on a ~$770 price is 0.13 bps each way plus slippage).

So the honest ranking after costs is: **M1/SPY survives comfortably, M1/IWM survives
narrowly, and everything with a thin edge — M1/EEM above all — does not survive at all.**
The zero-cost assumption is not a rounding error for the weak cells; it is the difference
between a positive and a negative result.

### 3.2 Fill assumptions are optimistic

- **Stops fill exactly at the stop price.** Every stopped-out trade is booked at exactly
  −1.000R. In reality an index ETF can gap through a stop overnight. The measured share
  of exits that are stops is **14–21% for M1, 28–35% for M2 and 46–61% for M3** — so this
  matters most for the dip-buying rule, which is also the rule with the widest spread of
  outcomes. For M1/SPY (42 stop exits out of 281 trades), if a third of them gap through
  by 0.3R the expectancy falls by 0.0149R, about 9% of the edge; if half gap through by
  0.5R it falls by 0.0374R, about 22%. Those are illustrations of the direction and
  rough size of the bias, not measured slippage.
- **Signal exits fill at the close** of the day the condition is true, with no slippage.
- **Entries fill at the next open**, with no gap slippage beyond the open itself.

All three assumptions push the same way: the reported results are **optimistic**.

### 3.3 Sizing drives every CAGR, drawdown and Sharpe figure

The equity curve risks a flat **1% of equity per trade**, one position at a time, no
pyramiding. That single choice sets CAGR, max drawdown and Sharpe. Total R and the
trade-level statistics (`p, b, E, p*, b*, sd, n_req`) are sizing-independent and are the
robust part of the report.

Time-in-market is reported with the headline table for exactly this reason: M1/SPY is in
the market **8.8%** of sessions and M3/EEM **24.8%**. The 0.0–1.4% CAGR versus
buy-and-hold's 7.0–10.8% is mostly **idle capital**, not a missing edge, and comparing
the two CAGR figures without that context would be misleading in either direction.

### 3.4 Dividend treatment

The traded series is **split-adjusted price**, not total return. That is the right series
for signals and stops, but it understates the return of anything held. The measured
dividend drag over each window was SPY 2.0%, QQQ 0.7%, IWM 1.4%, EEM 2.1% per year, and
because the rules hold only 6–25% of the time the drag the *strategies* miss is small
(≈0.1–0.5%/yr). The buy-and-hold benchmark is reported both ways, so that comparison is
not overstated.

### 3.5 The regime definitions are arbitrary

Regimes are defined as `close` vs `SMA(200)` crossed with the 20-day sign of `SMA(200)`,
and vol terciles from trailing 20-day realised vol cut **per instrument**. All four
choices are conventional and none is privileged. Different windows (say 100-day,
or 60-day vol) would move trades between cells and change the cell counts. The *direction*
of the finding is stable — `UP_rising` carries the profit, `DOWN_falling` loses for
everything — but individual cell numbers should not be treated as precise.

Because the tercile cuts are per instrument, a `HIGH` vol day for IWM is not the same
absolute vol as a `HIGH` vol day for SPY. Comparisons across instruments in the vol
dimension are therefore relative, not absolute.

### 3.6 Data quality, and how far the deep history is corroborated

- The **primary series is certified** against an independent vendor where they overlap:
  Yahoo SPY matches TradingView `AMEX:SPY` **exactly ($0.0000)** on 10 sessions, and
  Yahoo VIX matches TradingView `TVC:VIX` within **$0.01** on 30 sessions. That is real
  verification, but it covers only the **most recent few weeks**.
- The **deep history (1993–2026 for SPY) is not corroborated by a second vendor.** The
  only other feed available, moomoo, retains ~20 years and folds dividends in on its own
  schedule, so its levels are not comparable; on daily *returns* it agrees at the median
  (0.0000 pp difference) but diverges by **up to 2.6 pp** on ~1% of sessions. Inspection
  shows moomoo **repeating identical closes** on liquid-ETF sessions (SPY 2011-08-01/02/03
  all read 105.0795 while the market moved ~2.5%), which is a feed defect.
- **Yahoo is not clean either**: 20–62 "stale" bars (consecutive identical closes) per
  series, clustered in the early, thin years. They were detected and reported
  (`source-check.txt`) but **not repaired**. A handful of the 1990s sessions in the
  per-year tables may rest on stale bars.
- **Two sources failed outright and are reported as failures**: the moomoo feed has no
  VIX index (`US.VIX` returns `ret=-1`), and the hosted
  `mcp__moomoo__quote_history_kline` tool rejects the call on its `ktype`/`autype` enums
  whether they are passed as integers or strings.

### 3.7 Instrument selection

Four large US-listed index ETFs plus VIX. There is no single-stock, sector, small-cap
(outside IWM), commodity, bond, or non-US-ex-EM evidence here. Mean reversion is widely
reported to behave very differently in single names and in illiquid instruments, and
nothing in this study speaks to that. The four ETFs were chosen ex ante as broad index
proxies rather than screened on performance, so there is no survivorship filter inside
the set — but the *set itself* is a selection.

### 3.8 The main study has its own multiple-comparisons problem

3 rule sets × 4 instruments is 12 tests. Correcting for that search (Bonferroni,
|t| > 2.865 for m = 12) leaves **exactly one cell standing: M1 on SPY at t = 4.79**. The
next best, M3 on SPY at t = 2.73, fails — despite having the *largest* per-trade
expectancy in the whole table (+0.371R). That contrast is the study's most useful
caution: a big expectancy on a small sample with a wide spread is not a finding.

The one survivor then has to justify itself, and it does: positive in **26 of 31 years
(84%)**, in both halves of the sample (+0.193R then +0.154R), and in **all four decades**
(+0.198, +0.187, +0.136, +0.181). That is the behaviour of an effect, not of a fitted
number — and it is the direct counter-example to the fished parameters of Task 5.

### 3.9 Strategy-family caveats that are easy to miss

- **Only long signals were tested.** These rules are all "buy the dip in an uptrend".
  There is no short leg, so in a sustained bear market (2008, 2022) the rules simply do
  not trade much — M1/SPY took only 2 trades in 2022. The apparent "safety" of these
  rules in crashes is mostly **inactivity**, not skill.
- **Overlapping signals are discarded.** After a trade exits, the next scan resumes at
  the following day; a second signal during a held position is ignored (no pyramiding).
  This is a choice, and a different one changes trade counts.
- **Open trades at the data end are excluded** (their outcome is unknown). The count of
  such trades is reported as `n_open` in the headline table — it is 0 or 1 in every cell,
  so this is immaterial here.
- **`n_req = 4·(sd/|E|)²` is a rule-of-thumb for ~2σ**, not an exact power calculation,
  and `L ≈ ln(N)/ln(1/(1−p))` is an expected longest-run approximation. Both are reported
  with the observed longest run alongside so the approximation can be judged.

---

## 4. Deviations from the brief, and why

Stated plainly because a reader should know where the study departed from its
instructions.

1. **Bulk price data came from the moomoo SDK over local OpenD and from the Yahoo
   chart API, not from the MCP tools directly.** The brief named the MCP OHLCV tools.
   Two constraints made that impractical for bulk history: the brief also required
   "never print raw bar dumps into your context — write to CSV via a script", which is
   impossible when the only access path is a tool whose result lands in context; and the
   moomoo MCP kline tool rejects the calls (documented above). The MCP tools were used
   for their intended role — **verification** — with TradingView responses captured
   verbatim as fixtures (`data/_tvcheck_*.csv`) and compared by script. The result is
   that the primary series is certified against the designated tool where they overlap.
2. **Yahoo is the primary equity source rather than the moomoo vendor feed.** Moomoo
   retains only ~20 years, which would have excluded the 2000–02 bear market, and it
   contains the repeated-close defect described in §3.6. Both are kept, so the choice is
   auditable.
3. **`E_R` was added alongside the pre-registered `E` formula** (§1).
4. **The fair-strike short-vol variant was added** after running the pre-registered
   payoff as specified (§2.2). The pre-registered version is reported in full and is not
   replaced.
5. **The multiple-comparison and robustness analysis (§7, §7b of `RESULTS.md`) was added**
   because the main study has the same 12-test problem the Task 5 demonstration is about.
   Leaving it out would have been the dishonest choice.
6. **Extra files were created** beyond the four named outputs: `pull_data.py`,
   `verify_sources.py`, `verify_metrics.py`, `make_results.py`, `run.txt`,
   `hand-check.txt`, `source-check.txt`, `trade-dump-M1-SPY-2018.txt`, and `out/*.csv`.
   All are additive. **No `SKILL.md` was modified** and no other skill's files were
   touched.

---

## 5. What I did not test

Listing this explicitly, because absence of evidence here is not evidence of absence.

- **Options at all.** No option prices, greeks, IV surfaces, term structure, skew,
  strikes, expiries, assignment, margin, or early exercise. The "volatility corner" of
  this brief is answered with a vol-index proxy, not with options.
- **Intraday anything.** Daily bars only. No opening-range, no intraday stops, no
  overnight-gap handling, no time-of-day effects. Since stops are checked against the
  daily low and exits are at the close, intraday sequencing (did the low come before the
  close?) is assumed, not observed.
- **Costs, taxes, financing, borrow.** Zero across the board.
- **Position sizing search.** 1% fixed risk was assumed, not optimised. Since the
  reported CAGRs depend entirely on it, there is no claim about the *best* sizing.
- **Portfolio combination.** Each rule runs alone on each instrument. No capital
  allocation across the 12 cells, no correlation analysis between them, no combined
  equity curve.
- **Shorting, leverage, or hedging.** Long-only, unlevered.
- **Parameter robustness surfaces.** Task 5 searched two grids on M1 only. M2 and M3 were
  not searched at all — deliberately, since searching them would have re-opened the
  fishing problem — so their sensitivity to thresholds is unmeasured.
- **The 1990–1993 VIX history** is in `data/VIX_1d.csv` but the vol study starts with SPY
  at 1993, so 3 years of available vol data are unused.
- **Statistical inference proper.** No confidence intervals, no bootstrap, no
  block-bootstrap for autocorrelated trade returns, no formal test of the regime
  differences. The `t` statistics are naive iid-mean t-tests and are optimistic where
  trades cluster.

---

## 6. What would change the conclusions

In rough order of how much it would move the answer:

1. **Adding realistic costs.** At 5 bps round trip, M1/EEM's edge is wiped out more than
   five times over (it needs a round trip under 1.0 bps to stay positive) and M1/IWM
   loses 20% of an already-thin edge (breakeven at 25.2 bps). The one survivor, M1/SPY,
   keeps 86% of its edge at 5 bps and survives up to 36.9 bps. The *ranking* of cells
   changes materially with costs, even though M1/SPY's survival does not.
2. **Modelling gap-through on stops.** The stop share of exits is 14–21% for M1, 28–35%
   for M2 and 46–61% for M3, all booked at exactly −1R. For M1/SPY, a third of the 42
   stop exits gaping through by 0.3R removes 9% of the edge, and half of them gaping by
   0.5R removes 22%. M3, where most exits are stops, is the most exposed to this.
3. **Replacing the vol proxy with real option data.** A real short-vol backtest with
   strikes, expiries, skew, spreads and margin rules would very likely show a *worse*
   left tail than −3.98R per unit, because the proxy cannot be margined out at the worst
   moment and real positions can.
4. **Testing single names and less liquid instruments.** Where mean reversion is
   strongest in the literature is also where the costs modelled in (1) bite hardest. The
   interaction is the real question and it is untested here.
5. **A proper out-of-sample protocol on the main study too.** The 12 cells were
   pre-registered but not split into in-sample/held-out halves the way Task 5 was. The
   decade and half-sample splits in §7b are a partial substitute, not a substitute.
6. **More data, or different regimes.** A single 33-year US sample, dominated by a long
   bull market, cannot distinguish "mean reversion in an uptrend works" from "buying dips
   in a decades-long uptrend worked". Japan 1990–2010, or any long sideways market, would
   be the natural falsification and is absent from this study.

---

## 7. The one-paragraph summary

The data supports exactly one of the things this study went looking for. Mean reversion
in an uptrend is real on large-cap US indices — M1 on SPY clears the multiple-comparison
bar, holds in all four decades, and wins in 26 of 31 years — but it is worth about
+0.17R per trade *before* costs, is in the market under 9% of the time, and does not
exist in the emerging-market ETF where the same code produces a t-statistic of 0.07.
Nothing here is profitable in every year or every regime; 66 regime cells lose money and
every one of the 12 strategy × instrument pairs has losing years. The volatility premium
is genuinely positive on average — VIX beat subsequent realised vol in 83% of windows —
and it is genuinely not free, with a single 2020 window costing −3.98R against a maximum
gain of +0.5R. And parameter fishing on this same data would have handed the desk a
"winner" whose in-sample advantage over the honest default was +0.213R and whose
out-of-sample advantage was +0.006R. The honest answer to "which strategy makes money
across years, timeframes and market regimes" is: one of them, barely, before costs, in
one instrument, and not in every regime or year — and the number you get by searching
until the backtest turns green is a fitted number, not an edge.
