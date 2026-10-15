# FINDINGS -- is a narrow, highly liquid universe better or worse than a broad one?

Study date / pull date **2026-10-14**. Quote snapshot **2026-10-15T00:39Z**.
Primary window **W14 = 2013-03-07 .. 2026-10-14, 3,422 days, 13.6 years**.
Long window **W10 = 2005-09-02 .. 2026-10-14, 5,310 days, 21.1 years**, which is
the one that contains 2008.

Every number below is copied from [`run-output.txt`](run-output.txt) or from
[`RESULTS.md`](RESULTS.md). Where a figure is arithmetic done *on* two printed
numbers, the line says so. Nothing is hand-typed from memory.

---

## The answer in five sentences

**Narrowing the universe to SPY, QQQ and IWM destroys the diversification.**
Their mean pairwise correlation is **0.875 yearly / 0.838 daily**, and three
equally weighted names at that correlation are worth **1.12 independent bets** --
a rounding error away from one bet. Against the sibling regime study's
0.666-0.887 that the predecessor study called "one bet taken with three different
exits", three index ETFs *are* that same bet.

**It nevertheless improves the book's return and Sharpe, on both windows.** The
3-index trend book returned **9.858%/yr with a -19.72% drawdown and Sharpe 0.828**
on W14, against the cross-asset four-sleeve book's **3.727% / -14.83% / 0.556**.
On the 21-year window that contains 2008 the same ordering holds: **7.457% /
-23.50% / 0.646** against **4.674% / -14.83% / 0.604**.

**And it still fails to beat simply buying SPY.** Buy-and-hold SPY returned
**12.513%** on W14 (vs 9.858%) and **9.104%** on W10 (vs 7.457%), with the
drawdown that the trend rule exists to avoid (-34.10% vs -19.72%; -56.47% vs
-23.50%). So on return, the order is: **buy & hold the broad index > narrow
3-index trend book > cross-asset trend book**.

**A basket of large constituents diversifies materially better than the index** --
mean pairwise correlation **0.348 daily / 0.235 yearly**, **2.53 effective bets**
against 1.12 -- and, on this data, returns far more. That return figure is
survivorship-contaminated and must not be quoted as a result; the correlation
figure is not.

**Narrowing the universe moves the "never lose a year" frontier by 0.03
percentage points of annual excess return** once you measure on a window that
contains a real bear market. That is the direct answer to the question: the
frontier is set by the *rule* and the *cash sliver*, not by how many tickers the
rule is applied to.

---

## 1. The diversification cost of narrowing -- measured, not asserted

### 1.1 Three index ETFs are one bet

| | daily | yearly |
|---|---|---|
| SPY-QQQ | 0.850 | 0.917 |
| SPY-IWM | 0.884 | 0.892 |
| QQQ-IWM | 0.780 | 0.814 |
| **mean** | **0.838** | **0.875** |
| min / max | 0.780 / 0.884 | 0.814 / 0.917 |

(`RESULTS.md` §1.1. Daily pairs read on the full 6,634-6,942-day common calendar;
yearly pairs on 25-26 complete years.)

**This lands inside the predecessor's band, and that is the finding.** The sibling
regime study measured 0.666-0.887 among its four sleeves and concluded they were
one bet. Three index ETFs sit at the *top* of that band -- more correlated than
the most correlated pair the predecessor study found. Whatever decorrelation the
predecessor measured in the cross-asset book (mean pairwise **+0.016**) is
entirely absent here.

A cleaner single number: with equal weights and a correlation matrix of unit
variances, the number of independent bets is `1 / (w'Cw)`.

```
three index ETFs : 1.12 independent bets
fourteen names   : 2.53 independent bets
```

**So narrowing SPY/QQQ/IWM to trade "a diversified book of index ETFs" is not
diversification at all. The three-market cap of US equity is one asset wearing
three tickers.**

### 1.2 But the narrow book still out-returned the cross-asset book

| W14, gross of costs | CAGR | maxDD | Sharpe | % positive years |
|---|---|---|---|---|
| **N3_TREND** (SPY/QQQ/IWM, equal 1/3) | **9.858%** | -19.72% | **0.828** | 75% (9/12) |
| C4_TREND (SPY/TLT/GLD/EEM, equal 25%) | 3.727% | **-14.83%** | 0.556 | 67% (8/12) |
| BH_SPY (buy & hold SPY) | **12.513%** | -34.10% | 0.785 | 75% (9/12) |

(`RESULTS.md` §2.1, §2.2. Cash CAGR over W14: 1.871%.)

The narrow book beat the cross-asset book by **6.13 percentage points of CAGR**
and **0.272 of Sharpe**, at 1.33x the drawdown. It did **not** beat buy-and-hold
SPY on return: it gave up **2.65 pp** of CAGR to cut the drawdown from -34.10% to
-19.72%.

**This reproduces the predecessor finding that trend's product is drawdown
reduction, not return.** Buy-and-hold beat every trend rule on raw return on
SPY/QQQ/TLT/GLD; the trend book's contribution here is the same.

### 1.3 The same ordering on the 21-year window, which contains 2008

| W10, gross of costs | CAGR | maxDD | Sharpe | % positive years |
|---|---|---|---|---|
| **N3_TREND** | 7.457% | -23.50% | **0.646** | 75% (15/20) |
| C4_TREND | 4.674% | **-14.83%** | 0.604 | 65% (13/20) |
| BH_SPY | **9.104%** | -56.47% | 0.552 | 75% (15/20) |

(`RESULTS.md` §10.)

The long window keeps the ordering and adds one number the short window cannot:
the narrow trend book's **worst losing years** are 2008 **-10.5%**, 2011 -6.3%,
2015 -2.7%, 2018 -1.9%, 2022 **-14.8%** -- five losing years in twenty. Buy-and-hold
SPY lost **-38.3%** in 2008 alone. That is the whole case for the trend rule, and
it is a real case.

Note that the cross-asset book has **more** losing years than the narrow one on
both windows (7 vs 5 on W10; 4 vs 3 on W14). Bonds, gold and ex-US equity did not
rescue the equity sleeve; they diluted it.

### 1.4 The frontier: what the lambda scaling actually buys

`lambda` is the fraction held in the book; `1 - lambda` earns the cash series. A
flat trend sleeve earns nothing. `RESULTS.md` §3.2 finds the largest `lambda` at
which **every complete year** is positive.

| W14 | max lambda | exposure | CAGR there | excess over cash |
|---|---|---|---|---|
| N3_TREND | 0.021 | **2.10%** | 2.048% | **+0.178%** |
| C4_TREND | 0.008 | **0.80%** | 1.887% | +0.017% |
| SPY_TREND | 0.005 | 0.50% | 1.905% | +0.034% |
| BH_SPY | 0.097 | 9.70% | 2.986% | +1.115% |
| C14_EW_TREND | 0.154 | 15.40% | 4.399% | +2.528% |

**The predecessor's published frontier reproduces exactly.** The sibling claim was
"100% positive years needs **0.8% exposure** for **+0.03%/yr** over cash". The
cross-asset book here needs **0.8% exposure** and buys **+0.017%/yr**. Same
exposure to the digit, same order of magnitude on the return. That is an
independent confirmation of the predecessor number on a different dataset pull.

**And it is a near-vacuous promise.** Two percent of a book and 0.18% of annual
excess return is not a strategy; it is a cash account with a rounding error. The
honest reading is that **"never lose a year" is not purchasable at any exposure
that matters.** `RESULTS.md` §3.4 makes the trade-off explicit:

| required excess over cash | best % positive years | on book | exposure | CAGR there |
|---|---|---|---|---|
| 0.00% | 100.0% | N3_TREND | 0.021 | 2.048% |
| 0.25% | 100.0% | N3_BH | 0.075 | 2.818% |
| 1.00% | 100.0% | BH_SPY | 0.097 | 2.986% |
| 2.00% | 100.0% | C14_EW_BH | 0.084 | 4.013% |
| 3.00% | 91.7% | N3_BH | 0.266 | 5.175% |
| 5.00% | 91.7% | C14_EW_BH | 1.000 | 28.164% |

Each extra percent of annual return over cash costs roughly one losing year in
twelve. The `P(positive period) ≈ Φ(Sharpe·√period_fraction)` relation the
predecessor established is what generates that table, and it holds for the narrow
universe exactly as it did for the broad one.

**On the long window the frontier barely moves at all** (`RESULTS.md` §10.3):

```
from cross-asset to 3-index trend:
  W10 (contains 2008):  exposure 0.80% -> 0.90%  (+0.10 pp)
                        excess   0.025% -> 0.057% (+0.031 pp)
  W14 (no 2008)      :  exposure 0.80% -> 2.10%  (+1.30 pp)
                        excess   0.017% -> 0.178% (+0.161 pp)
```

**+0.031 percentage points of annual excess on the window with a bear market in
it.** That is the number. The W14 version of the same comparison gives +0.161 pp,
five times larger, on a window that happens to contain no 2008. A reader who
quoted the W14 figure without noting the window would be reporting a window
artefact. This is exactly why the study runs both.

---

## 2. Does a basket of constituents diversify better or worse than the index?

### 2.1 Better, materially

| | mean pairwise daily corr | mean pairwise yearly corr | effective bets |
|---|---|---|---|
| **three index ETFs** | **0.838** | **0.875** | **1.12** |
| **fourteen constituents** | **0.348** | **0.235** | **2.53** |

(`RESULTS.md` §1.1, §1.2. 91 constituent pairs; daily min 0.099, max 0.544; yearly
min **-0.470**, max 0.768 -- the yearly range spans zero, which the index trio's
never does.)

The constituents' correlation to the index itself is what you would expect from
members: mean daily correlation **0.581 to SPY**, **0.581 to QQQ**, **0.514 to
IWM**, with ranges from 0.386 to 0.757.

**This is the one part of the constituent result that is not contaminated.** A
correlation matrix of names against each other does not care that they were
selected by hindsight, because selection by hindsight does not raise the
correlation of the *residual* day-to-day noise. So: **on diversification, broad
genuinely beats narrow, by a factor of 2.26 in effective independent bets.**

### 2.2 The returns say the basket wins outright. Distrust them.

| W14, gross of costs | CAGR | maxDD | Sharpe | % positive years |
|---|---|---|---|---|
| N3_TREND (3 index ETFs, trend) | 9.858% | -19.72% | 0.828 | 75% (9/12) |
| C14_EW_TREND (14 names, trend) | **18.564%** | -25.58% | **1.357** | 83% (10/12) |
| C14_IV_TREND (14 names, inv-vol, trend) | 15.372% | -23.30% | 1.337 | 83% (10/12) |
| C14_EW_BH (14 names, buy & hold) | 28.164% | -32.38% | 1.352 | **92% (11/12)** |
| C14_IV_BH (14 names, inv-vol, rebalanced) | 24.795% | -28.87% | 1.316 | 83% (10/12) |

A **+8.71 pp CAGR** gap and a **+0.53 Sharpe** gap over the narrow book. The
one-year positivity is also higher (83-92% against 75%).

**Do not quote these.** The fourteen names are the large caps of 2026 picked in
2026. `RESULTS.md` §4.6 prints their compounded returns over the window:

```
NVDA   +69,273.0%      META    +2,480.8%      V         +875.5%
TSLA   +14,306.0%      AAPL    +2,130.2%      UNH       +635.4%
AVGO    +9,801.3%      MSFT    +1,796.6%      JPM       +562.2%
                       AMZN    +1,755.4%      WMT       +375.3%
                       GOOGL   +1,568.5%      JNJ       +226.6%
                                              XOM        +99.5%
```

NVDA alone compounded at roughly **62% a year for 13.6 years**. An equal-weighted
basket of that list cannot be evidence about a broad universe; it is evidence
about hindsight.

**The bias bound (`RESULTS.md` §4.6).** Removing the three best-returning names
(the declared, explicitly-labelled performance screen) leaves an eleven-name
basket. Comparing like with like -- trend book against trend book -- the
eleven-name basket returns **12.794% at Sharpe 1.126**, still **+2.936 pp** and
**+0.298 Sharpe** above the narrow book's 9.858% / 0.828. The full gap is
**8.706 pp**; the three removed names account for **5.770 pp** of it and the other
**2.936 pp** does not. So the selection effect is worth about **two-thirds of the
gap**, and the remaining third is unexplained by this bound -- but the remaining
eleven are also survivors, so the bound is partial, not clean.

Two confounds sit inside it and are stated rather than resolved:

- **Equal weighting vs cap weighting.** Every basket is equal-weighted; the index
  is cap-weighted. Equal-weighting a cap-weighted index has its own long-run
  return effect, and this study cannot separate it from selection.
- **No dividends.** SPY's yield is higher than most of the constituents', so SPY's
  price-only return here understates its total-return gap the most.

### 2.3 The Sharpe question, answered separately from the return question

The brief asks whether single-name dispersion raises achievable Sharpe above the
index's. **Yes, and for a reason that is not only survivorship:** 2.53 independent
bets against 1.12 mechanically lowers the variance of a book for a given level of
its members' volatility. That part is structural and would survive a bias-free
sample.

But the two books do not hold the same risk, so the raw Sharpe comparison is not
an apples-to-apples one:

```
14-name EW trend   13.23% annualised vol   Sharpe 1.357
3-index trend      12.29% annualised vol   Sharpe 0.828
buy & hold SPY     16.86% annualised vol   Sharpe 0.785
```

Roughly equal vol, a 0.53 Sharpe gap. Some of that gap is the extra independent
bets; some is a bull decade favouring higher-beta names. The study cannot
separate them with the data it has, and says so rather than picking the
flattering reading.

### 2.4 The regime cells -- and why the grid is degenerate

`RESULTS.md` §5 cross-tabulates trend state (SPY above/below its own SMA-200)
against the tercile of SPY's trailing 21-day realised volatility. TerCile edges
over W14: calm <= 10.88% < mid <= 15.74% < hot.

```
trend state  vol tercile   days
down         calm               1
down         hot              528
down         mid               30
up           calm            1137
up           hot              609
up           mid             1107
```

**Calm days are almost never down-trend days.** One day in the entire window is
`down/calm`. That is not a data defect; it is what volatility clustering looks
like -- a downtrend and a calm tape rarely coexist. It means a trend x vol grid
cannot be populated evenly, and this study counts negative cells only over cells
with at least 60 days.

**The count of negative cells, and it splits by universe width:**

| book | mean basis | compounded basis |
|---|---|---|
| N3_TREND | 1 of 4 (`up/calm`) | 1 of 4 (`up/calm`) |
| N3_BH, N3_REB | 1 of 4 (`up/calm`) | 1 of 4 (`up/calm`) |
| C4_TREND | 1 of 4 (`up/calm`) | 1 of 4 (`up/calm`) |
| BH_SPY, SPY_TREND | 1 of 4 (`up/calm`) | 1 of 4 (`up/calm`) |
| C14_EW_BH, C14_EW_REB, C14_EW_TREND | **0 of 4** | **0 of 4** |
| C14_IV_BH, C14_IV_TREND | **0 of 4** | **0 of 4** |

(`RESULTS.md` §5.3. Readable cells: `down/hot`, `up/calm`, `up/hot`, `up/mid`.)

**This is the cleanest breadth result in the study, and it must be read with
care in both directions.**

- **Every index construction** -- the narrow 3-index trend book, the cross-asset
  book, SPY's trend rule, and buy-and-hold SPY -- has **exactly one** losing
  readable regime cell, and it is the *same* cell every time: the
  low-volatility uptrend, `up/calm`. Narrowing to three tickers does not create
  it, and the predecessor's cross-asset book does not escape it either.
- **Every constituent-basket construction has zero** losing readable cells, on
  both the mean and the compounded basis.

So breadth *does* remove the one losing regime cell. **But the reason is not that
breadth makes a book safer.** The baskets carry *more* volatility than the index
books (13.2-19.9% against 11.5-16.9%), and they are survivor-selected. They clear
a mean-return test in a regime the index books fail because they are more
aggressive and better chosen, not because they are better hedged. **The honest
statement is: the `up/calm` drag is an index phenomenon, and this study cannot
tell how much of the baskets' escape from it is breadth and how much is
hindsight.**

---

## 3. The dispersion proxy -- and what it is not

**There are no constituent option quotes in this data set.** Implied dispersion
cannot be measured, a correlation swap cannot be priced, and no dispersion trade
is simulated. What follows is a **descriptive proxy**. It is not a P&L.

Three quantities, all on W14 (`RESULTS.md` §6):

```
mean SPY 21-day realised vol        : 15.38%
mean avg-constituent 21-day realised: 30.72%
mean ratio (index / constituents)   : 0.480
mean cross-sectional dispersion     : 25.73%   (annualised sd across the 14 one-day returns)
corr(ratio, cross-sectional dispersion) = 0.110 over 2929 days
```

**The ratio is what matters.** It runs around 0.48: the average constituent is
about twice as volatile as the index that contains it. When the ratio is *low*
(0.415 or below), the names are moving a lot but in offsetting directions -- the
index is quiet because its members cancel. When it is *high* (above 0.526), the
names are moving together and the index is as volatile as its members.

**Does that divergence predict anything?** Forward 21-day returns, bucketed by
ratio tercile (`RESULTS.md` §6.1):

| ratio tercile | n windows | SPY fwd 21d | EW basket fwd 21d | index - basket |
|---|---|---|---|---|
| low (<= 0.415) | 1119 | 0.30% | 1.42% | -1.12% |
| mid | 1135 | 0.87% | 2.14% | -1.27% |
| high (> 0.526) | 1137 | 2.08% | 3.10% | -1.02% |

Two honest readings, and both must be given:

1. **Higher index-relative volatility goes with higher forward returns for both.**
   2.08% forward over 21 days in the hot tercile against 0.30% in the calm one.
   Dispersion does not decay; it mean-reverts upward with the market.
2. **The basket beat the index in *every* tercile**, by 1.02-1.27 pp per 21 days.
   That is the survivorship bias showing up exactly where you would expect it, and
   it is a useful demonstration: **a proxy computed on a survivor-selected basket
   will show the selection as a "regime" effect.** Any dispersion study built on
   today's index membership would draw the same false conclusion.

**Stated plainly, so no reader can drift into the wrong reading: this section
measures the *shape* of index-vs-constituent divergence. It cannot harvest it. To
harvest dispersion you need options on the names and on the index, and this study
has none.** `RESULTS.md` §6.2 gives the yearly cross-sectional dispersion for
completeness: the sd across the 14 names' yearly returns ranges from **17.01%
(2018)** to **193.83% (2020)**, and the spread between best and worst name in a
year ranges from **59.4% (2018)** to **784.4% (2020)**. In 2018 nine of fourteen
names lost money; in 2019 none did.

---

## 4. Cost and liquidity -- measured, not assumed

The predecessor studies ran cost as a flat assumption (0 / 5 / 20 bp) and never
measured it. This one measures it: one Schwab NBBO snapshot for all 17
instruments at one instant, verified against the price data (§0.2 of
`RESULTS.md`: all 17 quotes' session high/low match the final bar's).

**Quoted spread, basis points of mid:**

| group | mean | median | min | max |
|---|---|---|---|---|
| index ETFs (n=3) | 1.439 | **1.043** | 0.692 | 2.583 |
| constituents (n=14) | 25.701 | **14.450** | 1.781 | 128.840 |

In dollars the median spread is $0.070 for an ETF and $0.440 for a constituent.
Adding a **declared** 1 bp/side of market impact (declared because it is not
observable here, and applied equally to both groups so it cannot tilt the answer):

```
MEASURED ROUND-TRIP COST       median basis   mean basis
  index ETF                       3.04 bp       3.44 bp
  constituent                    16.45 bp      27.70 bp
  DIFFERENTIAL                   13.41 bp      24.26 bp
```

**Three honest caveats, all of which cut the same way.** The snapshot is taken at
(and just after) the close, when spreads are widest. **Ten of the seventeen quotes
sit outside their own session's high/low range**, i.e. they are stale or
extended-hours, and those are flagged in `RESULTS.md` §7 rather than deleted --
deleting them would remove precisely the wide-quote tail a marketable order
actually faces. And 128.8 bp for JNJ is a bad print, not a liquidity fact.

So the study carries a second estimate forward, **declared** rather than
discovered: **2.0 bp round trip for an index ETF, 6.0 bp for a mega-cap
constituent, i.e. a 4.0 bp differential.** The truth is between 4 and 13 bp.
Which brings us to the actual question.

### 4.1 How much of the gap survives the cost differential?

`RESULTS.md` §7.3 runs both books at each group's own cost:

| cost scenario | N3 CAGR | C14 CAGR | N3 - C14 | C14 vs its own 2 bp run |
|---|---|---|---|---|
| both gross | 9.858% | 18.564% | -8.705 pp | 0.091 pp |
| both at 2.0 bp | 9.795% | 18.473% | -8.678 pp | 0.000 pp |
| **each at its own declared cost (ETF 2.0 / con 6.0)** | 9.795% | 18.292% | **-8.497 pp** | -0.181 pp |
| **each at its own measured cost (ETF 3.04 / con 16.45)** | 9.762% | 17.821% | **-8.059 pp** | -0.652 pp |
| each at its own measured-worst cost (ETF 3.44 / con 27.70) | 9.750% | 17.316% | **-7.566 pp** | -1.157 pp |
| both at 50 bp | 8.292% | 16.321% | -8.029 pp | -2.152 pp |

**The cost differential is worth at most 1.16 pp of CAGR on the broad book, and
the return gap between the two books is 7.6-8.7 pp. Costs do not decide this
question -- they are an order of magnitude too small.** Even at the measured-worst
cost the 14-name basket, survivorship and all, is 7.57 pp ahead.

The reason is turnover, and it is worth stating because it corrects an intuition:
**the trend rule trades rarely.**

| book | sleeves | flips/yr | round trips/yr/sleeve | rebalance turnover (whole window) |
|---|---|---|---|---|
| N3_TREND | 3 | 17.20 | 2.87 | 1.19 |
| C4_TREND | 4 | 34.69 | 4.34 | 1.54 |
| SPY_TREND | 1 | 5.66 | 2.83 | 0.00 |
| C14_EW_TREND | 14 | 107.39 | 3.84 | 3.80 |
| C14_IV_TREND | 14 | 107.39 | 3.84 | 21.45 |

Under three round trips per sleeve per year. Cost sensitivity at these turnover
levels is small: even a **50 bp** round trip -- 12x the measured ETF cost -- costs
the narrow book 1.57 pp and the broad book 2.24 pp of CAGR, and changes no
ordering anywhere in this study.

**One asymmetry does survive, and it is worth flagging.** The inverse-vol book's
rebalance turnover is **21.45** against the equal-weight book's **3.80** -- 5.6x --
because rebalancing *by inverse volatility* chases volatility changes while
rebalancing by *equal weight* mostly follows return drift. At a 50 bp round trip
that costs it **-2.829 pp** against the equal-weight book's **-2.242 pp**, only
1.26x more, because both books carry the same flip-driven cost and the flips
dominate. At the measured constituent cost of 16.45 bp the inverse-vol trend book
gives up **~0.94 pp** against the equal-weight trend book's **~0.74 pp**.
**If you narrow the universe to save on costs but weight by inverse volatility,
you give a meaningful part of the saving back -- but not most of it.**

---

## 5. The direct verdict

**Question as asked:** among everything tested, what achieves the highest fraction
of positive years at a CAGR above the cash rate?

**Answer: 100% -- achieved by every book tested, by holding almost none of it.**
At `lambda = 0` the book is entirely cash and every complete year is positive,
because cash was positive in every period of both windows. That is true and
useless. So the study re-asks the question the answer to which is interesting:
**at what exposure and what return does the 100% get bought?**

`RESULTS.md` §8, sorted by the CAGR at the full-positivity point:

| book | CAGR at λ=1 | Sharpe at λ=1 | max λ for 100% pos. yrs | exposure | CAGR there | excess over cash |
|---|---|---|---|---|---|---|
| **C14_EW_TREND** | 18.564% | 1.357 | 0.154 | **15.40%** | **4.399%** | **+2.528%** |
| C14_IV_BH | 24.795% | 1.316 | 0.099 | 9.90% | 4.091% | +2.221% |
| C14_IV_TREND | 15.372% | 1.337 | 0.165 | 16.50% | 4.074% | +2.204% |
| C14_EW_BH | 28.164% | 1.352 | 0.084 | 8.40% | 4.013% | +2.143% |
| BH_SPY | 12.513% | 0.785 | 0.097 | 9.70% | 2.986% | +1.115% |
| N3_BH | 13.387% | 0.766 | 0.075 | 7.50% | 2.818% | +0.947% |
| **N3_TREND** | 9.858% | 0.828 | 0.021 | **2.10%** | **2.048%** | **+0.178%** |
| SPY_TREND | 8.200% | 0.745 | 0.005 | 0.50% | 1.905% | +0.034% |
| **C4_TREND** | 3.727% | 0.556 | 0.008 | **0.80%** | 1.887% | **+0.017%** |

(cash CAGR over W14: 1.871%)

**The winner is the fourteen-name equal-weight trend book**: 100% of complete
years positive, at 15.40% exposure, earning **4.399%** -- **+2.528% a year over
cash**. **Its losing years at that `lambda`: none, of twelve** -- that is what
100% means. Held in full, that same book lived through **2018 -4.200%** and
**2022 -10.948%**.

**And the winner is the one result in this study that must not be believed.** It is
the most survivorship-contaminated construction on the list. The honest ranking
after discounting for that is:

1. **buy & hold SPY** -- 9.70% exposure buys 2.986% CAGR, +1.115% over cash. It is
   the *narrowest possible* universe: one ticker.
2. **N3_TREND** -- 2.10% exposure buys 2.048%, +0.178% over cash.
3. **C4_TREND** -- 0.80% exposure buys 1.887%, +0.017% over cash.

**So on the frontier, narrowing from the cross-asset four-sleeve book to the
three-index book moves you from 0.80% exposure and +0.017% to 2.10% exposure and
+0.178% -- and narrowing all the way to a single ETF moves you to 9.70% exposure
and +1.115%.** The narrowest universe is the best one, and it is the one with no
rule in it at all.

### 5.1 Does narrowing move the frontier, and by how much? The arithmetic.

```
W10 (21.1 years, contains 2008)
  cross-asset 4-sleeve : 0.80% exposure -> CAGR 1.806%  excess +0.025%
  3-index trend book   : 0.90% exposure -> CAGR 1.837%  excess +0.057%
  MOVE: +0.10 pp of exposure, +0.031 pp of annual excess
  ten-name basket      : 4.90% exposure -> CAGR 2.353%  excess +0.573%

W14 (13.6 years, no 2008)
  cross-asset 4-sleeve : 0.80% exposure -> CAGR 1.887%  excess +0.017%
  3-index trend book   : 2.10% exposure -> CAGR 2.048%  excess +0.178%
  MOVE: +1.30 pp of exposure, +0.161 pp of annual excess
```

**The two windows disagree by a factor of five.** The window that contains a real
bear market -- the one that can distinguish a rule from a lucky decade -- says
narrowing is worth **0.031 pp a year**. The window that does not says **0.161 pp**.

**The measured answer, stated for the record: narrowing the universe moves the
full-positivity frontier by ~0.03 percentage points of annual excess return. That
is not a result. The frontier is a property of the rule and the cash sliver, not
of the universe's width.**

---

## 6. Out-of-sample discipline: the 70/30 split

Nothing is fitted, so there is no parameter to overfit. The split is a robustness
check on whether a full-sample claim is one era's artefact.

```
in-sample  2013-03-07 .. 2022-09-08  (2395 days)
holdout    2022-09-09 .. 2026-10-14  (1027 days)
```

| book | IS CAGR | OOS CAGR | IS Sharpe | OOS Sharpe | IS %pos yrs | OOS %pos yrs |
|---|---|---|---|---|---|---|
| N3_TREND | 8.315% | 13.533% | 0.730 | 1.039 | 75% (6) | 100% (3) |
| C4_TREND | 2.220% | 7.313% | 0.389 | 0.851 | 75% (6) | 67% (2) |
| BH_SPY | 10.515% | 17.297% | 0.667 | 1.083 | 75% (6) | 100% (3) |
| N3_BH | 11.748% | 17.292% | 0.683 | 0.964 | 88% (7) | 100% (3) |
| C14_EW_TREND | 17.992% | 19.915% | 1.281 | 1.560 | 88% (7) | 100% (3) |
| C14_IV_TREND | 13.832% | 19.037% | 1.160 | 1.858 | 88% (7) | 100% (3) |

**What the split does establish:** the ordering is preserved in both halves. Every
book that beat a comparator in-sample also beat it out-of-sample, with **exactly
one exception across all eleven books measured against buy-and-hold SPY**:
`N3_BH` beat SPY in the first 70% (11.748% vs 10.515%) and did not in the last 30%
(17.292% vs 17.297%) -- by five thousandths of a percentage point, which is noise.
Nothing here is a first-half-only artefact.

**What the split does not establish, and this must be said loudly:** the holdout
is **1,027 days -- 4.1 years -- and contains only three complete calendar years**,
all of them a strong bull stretch for US equity. That is why almost every book
shows **100% positive years** out-of-sample. **The split is not a regime test.**
The regime test is the long window in §1.3 and §5.1, because it is the one with
2008 in it.

---

## 7. What the study could not do

Everything in this list is a real gap, not a hedge.

**No option data at all.** The hypothesis explicitly mentions trading options on a
narrow universe. This study contains no option quotes, no implied volatilities, no
option Greeks and no option P&L. Whatever is true about narrow-universe *options*
is untested here. §3 is a proxy for what a dispersion book would look at, and it
is labelled as a proxy in every place it appears.

**No historical index membership.** Everything about the constituent basket's
*return* is survivorship-contaminated (§2.2). The bias bound in §4.6 is partial
and says so. The study cannot produce a clean control for the selection effect
with this data source, and does not pretend the bound is one.

**Price-only data.** No dividends, no distributions. SPY's yield is worth roughly
1-1.5%/yr over this window; the constituents pay less. The *rule* comparisons
(same instrument, different rule) survive this; the *instrument* comparisons
(index vs basket, ETF vs stock) do not.

**Cost is one snapshot of a noisy quantity.** Ten of seventeen quotes are stale or
extended-hours. The measured differential (13.41 bp) and the declared alternative
(4.0 bp) bracket the truth; neither is the truth. Reported both, ranked with both.

**The cash series is a yield index, not a fund.** It ignores fees, bid/offer and
roll, and credits the full quoted yield every business day. Every "excess over
cash" figure in this document is therefore a slight overstatement.

**One country, one currency, one market regime.** 13.6 and 21.1 years of US
equity. 2008 is in the long window; 2000-2002 is not (the S10 constituents do not
all reach back that far), and the dot-com bear is the one regime where a
trend-following rule on a narrow index ETF universe is supposed to shine.

**The regime grid is degenerate by construction** (§2.4): one down-trend calm day
in the whole window. The regime-cell result is thin, and is reported with its cell
counts so a reader can see how thin.

**One pre-registered rule, not the best rule.** Nothing is fitted, which is the
honesty guarantee and also the limitation: this study cannot say what a different
SMA window, a different rebalance frequency or a volatility target would have
done.

**The frontier table's "100%" is trivially reachable** at zero exposure. Every
place it appears, the study states the return at which it is bought, because the
fraction alone is not information.

---

## 8. What the hand-check and the reproduction checks certify

Three things were verified rather than asserted, and a reader should know exactly
how much each is worth.

**`handcheck.py` re-derives every headline statistic from `data/*.csv` without
importing `study.py`.** Its final gap table lists **51** statistics: CAGR,
drawdown, Sharpe, day count, positivity by horizon, losing-year sets, six
pairwise correlations, four frontier lambdas, and the spread table.
**Every gap is below 1e-6.** The by-hand equal-weight basket return for
2022-06 agrees to **5.2e-16**; the by-hand one-year correlation of SPY and QQQ in
2024 agrees to **0.0e+00**.

**The simulator is the sibling studies' simulator, bit for bit.** Re-running the
weather-test's book F reproduces its published CAGR 4.6742%, maxDD -14.8291%,
Sharpe 0.6037, 5,311 days and 7 losing years with a gap of **0.000000** on every
one. More demanding: this study's SPY-trend book is compared **year by year**
against the weather-test's published per-year sleeve-A returns for the **17**
years where the two windows overlap -- **largest gap 0.0000**. A wrong SMA
convention or an off-by-one in the alignment would have shown up there.

**The frontier claim reproduces on a different pull.** The predecessor's "0.8%
exposure for +0.03%/yr over cash" comes back as **0.8% exposure** here.

**`study.py` is deterministic.** Two consecutive runs produced identical stdout
and byte-identical `out/*.csv`.

**What the certification is worth.** It certifies *arithmetic*. It does not
certify *interpretation*, and it certainly does not remove the survivorship bias,
the price-only data, or the absence of options. A study can be perfectly
reproducible and still be measuring the wrong thing.

---

## 9. The one-paragraph answer, for the desk owner

Narrowing to SPY/QQQ/IWM does not build a diversified equity book -- those three
tickers carry 0.875 yearly correlation and 1.12 independent bets, so they are one
asset, and a trend rule on them is one bet with three names. It does not beat
buying SPY outright on return on either window (9.858% against 12.513% on 13.6
years; 7.457% against 9.104% on 21.1 years), and what it buys in exchange is the
drawdown cut the trend rule always buys (-19.72% against -34.10%; -23.50% against
-56.47%). Broadening to a constituent basket does diversify better -- 2.53
effective bets, 0.235 yearly correlation -- and on this data returns far more, but
the return figure is contaminated by the fact that the fourteen names were chosen
in 2026 for being the winners and is not evidence about breadth. Costs are not the
tiebreaker: the measured round-trip differential is 13.4 bp and the declared one
is 4 bp, worth at most 1.16 pp of CAGR against a 7.6-8.7 pp return gap. And the
"never lose a year" frontier, which is what the desk owner's proposal is really
after, moves by **0.03 percentage points of annual excess** when you narrow, on
the only window tested that contains a real bear market. **The measured answer is
that narrowing the universe is close to irrelevant to the property being sought.
What sets that frontier is the rule and the cash sliver.**
