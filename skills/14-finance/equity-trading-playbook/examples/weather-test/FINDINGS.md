# FINDINGS — what un-optimised diversification bought, and what it did not

Study date / pull date **2026-10-14** (UTC). Book window **2005-09-02 ..
2026-10-14**, 5,311 trading days, 21.1 years. Every number below is copied from
`run-output.txt` (the complete stdout of `study.py`), and every table is in
[`RESULTS.md`](RESULTS.md). Two figures are arithmetic done *on* the printed
correlation matrix and the printed CAGR table; both say so in the line where they
appear. Nothing else here is hand-typed arithmetic.

---

## The answer in three sentences

**The diversification worked.** The sleeves in this book are genuinely close to
uncorrelated year to year — mean pairwise correlation **+0.016**, against the
**0.666-0.887** the sibling regime study found among *its* sleeves. That was the
design goal and it was met, decisively.

**The book still failed, and failed badly.** The pre-registered 5-sleeve book lost
money in **17 of 20 complete years**, had a worst year of **-25.27%**, and drew
down **-86.08%**. It is negative in **every** rolling 7-year and 10-year window.
There is no horizon over which this book is an all-weather anything.

**The reason is one sleeve, not the diversification.** Sleeve E — long the VIX
index when VIX is above its 50-day average — earned **-86.90% a year compounded**
on the days it was long, while the VIX index itself **rose 24.24%** over the
window. Its loss is structural, not noise, and it is present in all 17 losing
years. Correlation is necessary for a diversified book. It is not sufficient: a
sleeve that loses money loses money no matter what it is correlated with.

---

## 1. What diversification bought — the correlation matrix (§5 of RESULTS.md)

This was the key output, and it is the good news.

**The prior study's finding.** The sibling `equity-trading-playbook` regime study
measured six pairwise yearly correlations among its four sleeves (trend-200d,
trend-50/200, buy-and-hold, vol-targeted hold) and every one was **positive,
between 0.666 and 0.887**; mean 0.788, median 0.793. Its conclusion was that the
four rules were one bet — "long this instrument" — taken with three different
exits.

**This book, measured the same way** (Pearson, yearly returns, the 20 complete
years 2006-2025):

| | A | B | C | D | E | G |
|---|---|---|---|---|---|---|
| **A** equity trend | 1.000 | -0.314 | 0.047 | 0.110 | **-0.629** | 0.762 |
| **B** bond trend | -0.314 | 1.000 | -0.154 | -0.319 | 0.492 | -0.389 |
| **C** gold trend | 0.047 | -0.154 | 1.000 | 0.415 | 0.218 | 0.306 |
| **D** ex-US equity trend | 0.110 | -0.319 | 0.415 | 1.000 | -0.033 | 0.239 |
| **E** long volatility | -0.629 | 0.492 | 0.218 | -0.033 | 1.000 | -0.516 |
| **G** buy & hold SPY | 0.762 | -0.389 | 0.306 | 0.239 | -0.516 | 1.000 |

- All 15 pairs range **-0.629 to +0.762**.
- **Mean of the 15 printed values: +0.016.** (Averaged off the matrix printed in
  §5; the matrix itself is the run's.)
- The six trend-sleeve pairs among **A-D alone: -0.319 to +0.415**, mean
  **-0.036**, median **-0.054** — against the prior study's 0.666-0.887, mean
  0.788, median 0.793. (Means/medians of the printed pairs.)
- The vol sleeve is a real hedge in correlation terms, not a decoration:
  **corr(A,E) = -0.629** and **corr(E,G) = -0.516**. Equity trend and long
  volatility genuinely offset each other year to year.
- Two pairs are worth noting because they did *not* decorrelate:
  **corr(B,E) = +0.492** — a bond uptrend and a VIX uptrend are both "the market
  is frightened" trades, so the vol sleeve does **not** hedge the bond sleeve —
  and **corr(D,E) = -0.033**, so it does almost nothing for ex-US equity either.

**So yes: A-E are genuinely less correlated than the sleeves the prior study
tested, and by a lot.** The mean pair fell from +0.788 to -0.036, a swing of about
0.82. The *best* prior-study pair (0.666) was more correlated than the *worst*
trend pair here (0.415). On the specific design question — *can a book of
structurally different sleeves be built at all?* — this data answers an
unambiguous yes.

**And it did not matter, because of §2.**

---

## 2. What diversification did not buy — the book itself (§7, §8, §9)

The pre-registered book, A-E at 20% each, monthly rebalance, gross of costs:

| | CAGR | max drawdown | Sharpe | worst year | losing years | worst rolling 12m | worst rolling 36m |
|---|---|---|---|---|---|---|---|
| **BOOK_5** (pre-registered) | **-8.15%** | **-86.08%** | -0.276 | **2013, -25.27%** | **17 of 20** | -32.91% | -51.86% |
| **F** (4 trend sleeves, no vol) | +4.67% | -14.83% | 0.604 | 2022, -6.51% | 7 of 20 | -10.33% | -12.90% |
| **G** (buy & hold SPY) | +9.10% | -56.47% | 0.552 | 2008, -38.28% | 5 of 20 | -48.59% | -46.78% |

Sharpe convention: daily simple returns, full sample, Rf = 0, x sqrt(252). Losing
years count only the 20 complete calendar years 2006-2025; 2005 and 2026 are
partial and are reported separately in §4 and §8 of `RESULTS.md`.

**Is the book profitable in every year? No.** All 17 losing years, with the
sleeves that were negative in each (§8 — this is the full list, not a top ten):

| year | BOOK_5 | sleeves negative | per-sleeve return |
|---|---|---|---|
| **2013** | **-25.27%** | B, C, D, E | A +29.69% · B -3.07% · C -3.73% · D -19.47% · E -80.31% |
| 2021 | -21.16% | B, C, E | A +27.04% · B -5.07% · C -13.92% · D +0.14% · E -78.56% |
| 2017 | -18.57% | B, C, E | A +19.38% · B -3.05% · C -2.50% · D +32.99% · E -79.33% |
| **2015** | -16.78% | **A, B, C, D, E** | A -8.89% · B -5.28% · C -4.39% · D -4.26% · E -65.27% |
| 2024 | -16.59% | B, E | A +23.30% · B -12.45% · C +26.66% · D +2.11% · E -77.86% |
| 2014 | -14.02% | C, D, E | A +9.26% · B +15.54% · C -12.89% · D -6.20% · E -63.18% |
| 2022 | -13.68% | A, B, C, E | A -15.40% · B -2.63% · C -7.78% · D +0.00% · E -47.80% |
| 2012 | -13.41% | B, D, E | A +10.04% · B -10.87% · C +0.11% · D -1.55% · E -56.54% |
| 2023 | -12.57% | B, D, E | A +9.68% · B -13.82% · C +7.80% · D -15.80% · E -44.84% |
| 2019 | -11.76% | D, E | A +13.58% · B +10.63% · C +17.86% · D -5.25% · E -67.91% |
| 2006 | -6.37% | B, E | A +9.32% · B -0.30% · C +16.17% · D +9.66% · E -53.89% |
| **2018** | -4.79% | **A, B, C, D, E** | A -9.32% · B -3.41% · C -0.87% · D -7.28% · E -27.04% |
| 2009 | -3.92% | B, E | A +13.86% · B -15.74% · C +20.66% · D +46.08% · E -57.61% |
| 2010 | -3.71% | B, D, E | A +0.81% · B -1.45% · C +29.27% · D -1.53% · E -45.69% |
| 2016 | -2.45% | D, E | A +8.29% · B +5.35% · C +7.92% · D -2.04% · E -37.71% |
| 2011 | -1.54% | A, D, E | A -9.86% · B +19.89% · C +10.21% · D -10.11% · E -29.62% |
| 2008 | -0.72% | A, C, D, E | A -0.81% · B +17.45% · C -10.98% · D -16.92% · E -18.36% |

Three things are visible in that table and all three matter.

- **E is negative in all 17.** Not most — all. And E lost in **19 of the 20**
  complete years; its single positive year is 2020 (+7.60%).
- **Two years defeated the diversification outright: 2015 and 2018.** In both, all
  five sleeves lost. It is worth seeing that even a book this decorrelated has
  such years, and worth seeing how *mild* the trend sleeves were in them
  (2015: A -8.89%, B -5.28%, C -4.39%, D -4.26%; the book's -16.78% is E again).
- **A's best years carry the book.** 2013, when A made +29.69%, was the book's
  worst year, because E lost -80.31% beside it.

The rolling-window table, which is the honest version of "how often":

| window | windows tested | worst | mean | % positive |
|---|---|---|---|---|
| 1y | 5,060 | -32.91% | -7.55% | 22.9% |
| 2y | 4,808 | -42.39% | -15.18% | 15.6% |
| 3y | 4,556 | -51.86% | -22.43% | 7.8% |
| 5y | 4,052 | -60.47% | -36.56% | 2.6% |
| 7y | 3,548 | -71.89% | -49.31% | **0.0%** |
| 10y | 2,792 | -74.83% | -64.08% | **0.0%** |

Longer holding made this book strictly worse: the fraction of positive windows
falls monotonically with the horizon and reaches zero at seven years. A book with
a negative drift is not repaired by patience.

---

## 3. Why it failed — one sleeve, and it was structurally wrong (§3)

The per-sleeve table (§3), gross, on the book window:

| sleeve | CAGR | max dd | Sharpe | worst year | losing years | days long | annualised return on the days it was long |
|---|---|---|---|---|---|---|---|
| A equity trend | +6.48% | -20.96% | 0.611 | 2022, -15.40% | 6 | 77.8% | **+8.43%** |
| B bond trend | -0.60% | -39.26% | -0.003 | 2009, -15.74% | 13 | 47.1% | -1.28% |
| C gold trend | +8.25% | -33.52% | 0.599 | 2021, -13.92% | 8 | 68.2% | **+12.34%** |
| D ex-US equity trend | +2.64% | -42.66% | 0.241 | 2013, -19.47% | 11 | 62.1% | +4.30% |
| **E long volatility** | **-55.16%** | **-100.00%** | -0.312 | **2013, -80.31%** | **19** | 39.5% | **-86.90%** |
| G buy & hold SPY | +9.10% | -56.47% | 0.552 | 2008, -38.28% | 5 | 100% | — |

**The diagnosis.** Sleeve E is long the VIX index when the index is *above* its own
50-day average — that is, it buys **after** the spikes. And the VIX mean-reverts.
So the rule systematically buys near the top of a mean-reverting series, and it
earns **-86.90% a year compounded** over the 2,100 days it is long. Meanwhile the
VIX index **rose 24.24%** over the window (13.57 to 16.86). The loss is not the
level of volatility; it is the reversion.

The sibling engine's own yearly test says this is not sampling noise: E's mean
yearly P&L has **t_stat = -2.472**, beyond the engine's own ±2.0 noise band, and
its yearly series is *negatively* autocorrelated (lag-1 -0.339), so its `n_eff`
(44.5) is larger than the year count alone would demand — the evidence against E
is not thinner than it looks. Note the reverse case for C (gold): `n_eff` is only
**13.6** against 20 years, because its yearly series is positively autocorrelated
(+0.234), so its t_stat of 2.550 rests on fewer independent episodes than 20.

**First-order attribution of the book's -8.15% CAGR** (weights × each sleeve's own
CAGR, which is what the monthly-rebalance identity makes the book's monthly return
sum to):

| sleeve | weight | sleeve CAGR | contribution to the book |
|---|---|---|---|
| A | 0.20 | +6.48% | +1.30% |
| B | 0.20 | -0.60% | -0.12% |
| C | 0.20 | +8.25% | +1.65% |
| D | 0.20 | +2.64% | +0.53% |
| **E** | 0.20 | **-55.16%** | **-11.03%** |
| sum | | | **-7.68%** |
| actual book CAGR | | | **-8.15%** |

Residual **-0.48 pp**, which is the compounding asymmetry between a blend of
CAGRs and the actual monthly-blended, drifting book. The arithmetic is done off
the per-sleeve CAGR column printed in §3; the residual is printed rather than
smoothed away. **Take E out — a four-sleeve book at 20% each, the remaining 20%
left in cash — and the same decomposition is +3.35% instead of -7.68%**, which is
the whole story of this study in one line. (F's own realised CAGR, at 25% each
with no cash, is the +4.67% of §2.)

**This is the central lesson**: a +0.016 average correlation is worth nothing if
one component has a large negative expectation. Portfolio construction operates on
*covariance*; it does not fix *drift*.

---

## 4. The closest achievable standard the data actually supports (§9)

Since the pre-registered book supports no standard at all, the honest question is
what its closest neighbour supports.

**F — the same four trend sleeves at 25% each, no vol sleeve — is that neighbour**,
and it is not a fitted artefact: A-D at equal weights is the same design decision
as A-E at equal weights, minus the sleeve that does not work. (It is also the
portfolio the brief asked for as a comparison.)

| | 1y | 2y | 3y | 5y | 7y | 10y |
|---|---|---|---|---|---|---|
| **F** worst window | -10.33% | -12.80% | -12.90% | -4.45% | **+0.63%** | **+14.37%** |
| **F** % of windows positive | 66.5% | 77.6% | 83.6% | 95.5% | **100.0%** | **100.0%** |
| **G** (buy & hold) worst window | -48.59% | -51.61% | -46.78% | -17.40% | +9.65% | +44.27% |
| **G** % of windows positive | 80.7% | 85.6% | 83.8% | 89.1% | 100.0% | 100.0% |

**The standard the data supports, stated plainly:**

> **F is positive over every rolling 7-year window tested** — 3,548 windows, worst
> **+0.63%** — **with the worst drawdown bounded at −14.83%** and a worst single
> year of **−6.51%**.

Three things must be said about that sentence. Saying them is the difference
between a finding and a sales pitch.

1. **It is not "every year".** F lost in **7 of 20** complete years. If the
   requirement is literally "no losing year", this data supports **nothing** —
   not F, not G, not the pre-registered book, not any sleeve in either sibling
   study.
2. **The 3,548 windows are not 3,548 independent observations.** A 21.1-year
   sample contains about **two** non-overlapping 7-year windows; the 100% figure
   counts *overlapping* windows, which share almost all their years. The honest
   count of independent evidence behind "7 years is always positive" is **two**.
   The 5-year statement (95.5% positive, worst -4.45%) rests on about four.
3. **You pay for it in return.** F's CAGR is **+4.67%** against buy-and-hold's
   **+9.10%** — roughly half. The drawdown is **3.8x smaller** and the Sharpe is
   slightly better (0.604 vs 0.552), but this is not a way to beat buy-and-hold;
   it is a way to hold similar assets with a much smaller worst case.

For completeness: buy-and-hold SPY also reaches "positive in every 7-year window",
but its worst drawdown is **-56.47%** and its worst 12-month window **-48.59%**.
The **X** in "bounded at X%" is exactly what F buys: **X = 14.83% rather than
56.47%** — and it buys it for about half the return.

**The pre-registered book does not support even the 1-year version**: only 22.9% of
its rolling 1-year windows are positive. Book_5 has no defensible all-weather
claim at any horizon, and the number the owner should carry away is not its worst
year or its drawdown but the monotone collapse of the "windows positive" column
(23% → 16% → 8% → 3% → 0%).

---

## 5. The pre-registration comparison — reported honestly, including the inconvenient part (§11)

The brief asked for the fixed-weight result, and *separately* for what a
weight-optimised version would have produced, so the difference between a designed
book and a fitted one is visible. It is in §11. The result is not the one this
exercise is usually staged to produce, and it is reported as it came out.

**Fixed, pre-registered (the recommendation):** 20/20/20/20/20 → CAGR **-8.15%**,
max dd **-86.08%**, Sharpe **-0.276**, **17** losing years.

**Fitted, for comparison only** — every 5-vector in 10% steps summing to 100%
(1,001 books), objective = in-sample Sharpe on the first 70% of the window, gross
of costs:

| book | weights A/B/C/D/E | IS Sharpe | OOS Sharpe | Sharpe decay |
|---|---|---|---|---|
| FITTED BEST (IS-optimal) | 40/20/40/0/0 | 0.719 | **0.960** | **-0.241** |
| pre-registered equal weight | 20/20/20/20/20 | -0.204 | -0.445 | +0.241 |
| pre-registered F (no vol sleeve) | 25/25/25/25/0 | 0.569 | 0.737 | -0.169 |
| median-IS-Sharpe book | 30/20/0/40/10 | -0.126 | -0.196 | +0.070 |

**The fitted book did not decay. It improved.** 597 of the 1,001 books beat equal
weight in sample (60%), and **518 of those 597 (87%) also beat it out of sample**.
On this sample, weight fitting was *not* punished.

The reason is in the same section and it is not "fitting works":

- Books with **E = 0** (286 of them): mean in-sample Sharpe **+0.482**.
- Books with **E > 0** (715 of them): mean in-sample Sharpe **-0.173**.
- **Every one of the top 10** has E = 0 **and** D = 0.
- The best book that still holds E is 0/0/90/0/10 — in-sample Sharpe 0.165,
  out-of-sample 0.170.

So the grid did not discover a subtle reweighting. It discovered **"get out of the
volatility sleeve"**. And E's negative drift was *already statistically visible in
the first 70% of the sample* — that is exactly why removing it helped going
forward instead of hurting. Fitting "worked" here because the thing it was fitting
was a **structural** failure, not a run of bad luck.

Two conclusions, both uncomfortable, and both worth keeping:

- **A fitted weight vector that happens to be right is still a fitted weight
  vector.** It carries no information about the next sample. An owner who adopts
  40/20/40/0/0 has adopted a number chosen by looking at the answers.
- **A pre-registered weight vector over unvetted sleeves is no better.** Registering
  the *weights* protected nothing, because nothing was wrong with the weights. The
  pre-registration was at the wrong layer.

**What is recommended, and what is not.** The recommendation is the **fixed-weight
book** and its fixed-weight comparison **F**. The 40/20/40/0/0 vector appears
because the brief asked for it; it is labelled fitted everywhere it appears, is
written to `out/optimised_weights.csv` under a header saying it is not the
recommendation, and is used nowhere else in this study.

---

## 6. Costs (§10)

Both sibling studies charged no costs at all, which flatters every always-long
sleeve. This study turns them on: a round-trip rate of *c* bps means each side
costs *c*/2 bps of the notional traded, charged on every position flip and on each
monthly rebalance's one-way turnover.

| portfolio | CAGR @ 0 bps | CAGR @ 20 bps | CAGR drag |
|---|---|---|---|
| BOOK_5 | -8.15% | **-9.27%** | -111.5 bp |
| F | +4.67% | **+3.78%** | -89.3 bp |
| G (SPY buy & hold, one entry) | +9.10% | +9.10% | -0.5 bp |

**Costs are not why the book failed — it failed before costs.** But they are not
nothing either. The book flips positions **1,326 times** over 21.1 years — 12.6
flips per sleeve per year, plus monthly rebalance turnover of 0.32x book value per
year — and at 20 bps that costs **F**, the book that does work, **89 bp of CAGR**.
At 5 bps F loses 22 bp. A real book would also pay wider spreads than 20 bps on
ex-US equity and gold at times, so **F's +4.67% gross should be read as visibly
less than that, not as a forecast.**

One development note belongs in the open, because it is the kind of error that
flatters rather than damns. The first implementation charged costs by shrinking a
sleeve's *dollar value*. Because the weights are renormalised every day, that
changes the mix and leaves the level untouched — it produced a cost drag of
**0.4 bp** where the true drag is **111 bp**, a 280-fold understatement. It was
caught by stress-testing at an absurd rate (a 10,000 bps round trip still left the
book standing), and the cost is now charged against the **return**. The corrected
version is what is reported here, and `README.md` records it too.

---

## 7. What remains untested, and what a next study should attack

In rough order of how much each would change the answer:

1. **A tradable long-volatility sleeve, and a *held* one rather than a *trend-followed* one.**
   Sleeve E is a signal whose return is approximated by the VIX index level
   change: no futures, no ETN, no roll cost, no fee. A real long-vol position
   bleeds in contango, so E's already-catastrophic number is an **upper bound**
   and the true figure is worse. And the rule tested here is trend-following on
   VIX; the question "does a small structural long-vol allocation decorrelate a
   book" was **not tested**, because the brief fixed the rule and that rule is what
   failed.
2. **A sleeve-viability screen, applied out of sample.** The single most useful
   thing this study says is that a fixed-weight scheme inherits whatever is broken
   in its sleeves. The untested design is: pre-register the *screen* (each sleeve
   must show a positive edge with a statistic beyond a noise band on data
   *preceding* the book), then build the book. That is a different
   pre-registration and a better one.
3. **Sleeves of a genuinely different *shape*.** Four of the five sleeves here are
   the *same* rule on four instruments. The matrix shows they are nevertheless
   nearly uncorrelated — but "same rule, different asset" is a narrower design than
   it looks. Mean-reversion, carry, cross-asset relative value and held-long-vol
   are all absent; the sibling options study's mean-reversion sleeves were never
   combined into this book.
4. **A longer window.** The book needs all five series, so it starts in 2005 and
   misses 1993-2004 entirely — which excludes 2000-2002 and includes a one-way
   bull run. Sleeve A and sleeve G are shown on full history (32 complete years):
   A +6.49% CAGR, -28.13% max dd, 10 losing years; G +8.87%, -56.47%, 9 losing
   years. On that longer sample A's worst year is **2000 (-20.50%)**, not 2022 — a
   different regime with a different answer.
5. **Total-return series.** Every series is price-only. TLT's price ends *below*
   its 2002 start (multiple 0.9561 per the sibling study), because its coupons are
   excluded, so the bond sleeve is understated; SPY, GLD and EEM pay distributions
   too, so buy-and-hold G is understated most of all. A total-return version would
   *raise* G, *raise* B, and therefore raise the bar the book must clear — it
   would make the comparison harder, not easier.
6. **Parameter sensitivity.** SMA(200) and SMA(50) were fixed before the run, as
   they had to be. Nothing here shows 200 beats 150, or 50 beats 20; nothing rules
   it out either.
7. **Regime attribution.** The sibling study did that for its corner; this one
   reports years and drawdowns only.
8. **Intraday execution and higher-frequency data.** Signals are read on closes.

---

## 8. The design lesson

The prior study's conclusion was that its sleeves correlated too much to combine.
This study's sleeves do not: mean pairwise correlation **+0.016**, with
corr(A,E) = -0.629. So combining them should have worked — and it did not, because
one sleeve had a **-86.90% a year** conditional return while being, in correlation
terms, the most valuable sleeve in the book.

**Diversification is a statement about covariance. It says nothing about drift.**
A book can be perfectly diversified and still lose almost everything, and this one
did, losing 86% of its value at its worst point.

The order of operations this study argues for, from its own evidence:

1. **Vet the sleeves first.** Each one needs its own positive expectation, with a
   statistic that survives a noise band, measured on data that predates the book.
   A pre-registration over unvetted sleeves is a pre-registration over a lottery.
2. **Then check the correlations.** They are worth checking — this study shows a
   genuinely low-correlation book is achievable, and that the vol sleeve's -0.629
   against equity trend is real, not an artefact of the window.
3. **Only then fix the weights**, and never touch them again.

That is not the order this study followed, and the pre-registered book is the price
of it — reported in full, with the worst year, the worst drawdown, the losing-year
list and the rolling-window collapse all in the open, as asked.
