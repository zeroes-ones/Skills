# FINDINGS — what the data said

Study date 2026-10-14. Four long-only rules, four instruments, full daily history
(23–34 years each). Every number below is from the run recorded in
[`run-output.txt`](run-output.txt); the tables are in [`RESULTS.md`](RESULTS.md).

Four rules were fixed before the first number was produced, and no parameter was
searched, swept or tuned. Where a result is bad it is reported as bad.

---

## 1. What works

**Trend-following reduces drawdown. That is its product, and it is real.**

On every instrument the 200-day rule cut the worst loss a holder would have had
to sit through — by roughly half on SPY, and by a fifth to a third elsewhere:

| instrument | S1 max drawdown | buy & hold max drawdown | S1 total return | buy & hold total return |
|---|---|---|---|---|
| SPY | **−28.60%** | −56.47% | 712.24% | 1651.56% |
| QQQ | **−65.75%** | −82.98% | 427.87% | 1327.56% |
| GLD | **−33.86%** | −45.56% | 435.91% | 747.21% |
| TLT | **−36.75%** | −55.06% | −7.99% | −4.39% |

On SPY the risk-adjusted numbers actually favour the trend rule: S1's Sharpe is
**0.584** against buy & hold's **0.551**, even though buy & hold returned more
than twice as much. Cutting the exposure during the bad stretches bought more
than it cost, in Sharpe terms.

**Volatility targeting is the best risk-adjusted line in the book for three of
four instruments**, and it is the only rule with the fewest losing years:

| instrument | S4 Sharpe | buy & hold Sharpe | S4 max drawdown | buy & hold max drawdown |
|---|---|---|---|---|
| GLD | 0.616 | 0.627 | −58.57% | −45.56% |
| QQQ | **0.614** | 0.493 | **−47.23%** | −82.98% |
| SPY | **0.559** | 0.551 | **−45.03%** | −56.47% |
| TLT | **0.377** | 0.058 | −48.81% | −55.06% |

S4 also produced the fewest losing instrument-years of any rule: **30 of 110**
(27%), against 44 of 110 (40%) for both trend rules and 37 of 110 (34%) for buy
& hold.

**The trade-level edge of the trend rules is real where the sample is big
enough.** The sibling engine's own pooled test (win rate against break-even win
rate, two standard errors) **PASSes for six of the eight trend rules** — both
S1 and S2 on SPY, QQQ and GLD. And the required sample sizes are plausible:
`n_req` is 28–65 trades against 83–248 actual trades.

## 2. Where it fails

**Buy & hold beats both trend rules on raw return on all four instruments.** No
exceptions. If the question is "which made the most money", trend-following lost
that question here.

**Trend-following failed outright on long Treasuries.** Over 24.2 years on TLT:

- S1: **−7.99%** total, CAGR **−0.34%**, Sharpe **0.018**
- S2: **+3.43%** total, CAGR **+0.14%**, Sharpe **0.058**

The sibling engine's edge test **FAILs** for both on TLT, and S1's
`n_req` is **25,706 trades against 121 actual trades**. A 200-day price trend on
a mean-reverting, carry-driven instrument bought nothing — and the sample cannot
even establish that it bought nothing precisely, only that it bought nothing
measurable.

**Every rule has losing years, and there is no instrument where any rule is
clean.**

| strategy | losing instrument-years | worst year | worst year |
|---|---|---|---|
| S1 | 44 / 110 (40%) | −43.08% | QQQ 2000 |
| S2 | 44 / 110 (40%) | −20.82% | SPY 2000 |
| S3 | 37 / 110 (34%) | −41.94% | QQQ 2008 |
| S4 | 30 / 110 (27%) | −34.40% | GLD 2013 |

S1 lost money in **16 of 25 years on TLT**; S3 lost in **14 of 25**. Trend
followers do not get to describe TLT as a diversifier on this evidence.

**The regime grid shows where each corner fails, and it is not where the story
says.** Using state known at the *previous* close (no hindsight), the 2×3 grid of
trend × volatility tercile gives, for SPY:

- S1 is **negative in `below|vol-mid` (−0.21% annualised contribution)** and
  makes essentially nothing in `below|vol-low` (+0.02%). Its whole return comes
  from the three `above` cells (2.17%, 2.35%, 2.53%).
- S3 is negative in the same `below|vol-mid` cell (−0.29%) — **trend and hold
  lose in the same regime**, which is the first hint of §5.
- QQQ S1 has **3 of 6 cells negative**; TLT S1 has **4 of 6**.

Only three strategy-instrument pairs have **no** negative regime cell at all
(QQQ S3, QQQ S4, SPY S4). And QQQ S3 has *zero* negative regime cells while
still losing money in **6 separate years** — the grid and the calendar disagree,
which is exactly why both were run.

## 3. The sample-size caveat, stated plainly

`n_req = 4·(sd/|E|)²` is the number of trades needed before an edge of size `E`
is two standard deviations from zero. It is not decoration; it is the difference
between a result and a rumour.

| rule | n_trades | n_req | verdict |
|---|---|---|---|
| SPY S1 | 114 | 29.3 | adequate |
| SPY S2 | 248 | 63.2 | adequate |
| QQQ S1 | 92 | 28.1 | adequate |
| QQQ S2 | 178 | 65.4 | adequate |
| GLD S1 | 83 | 51.6 | adequate |
| GLD S2 | 137 | 46.6 | adequate |
| **TLT S1** | **121** | **25,706** | **unmeasurable** |
| **TLT S2** | **136** | **3,039** | **unmeasurable** |

Two of the eight rules cannot support any claim at all. Their `E` values
(+0.0308 and +0.0558 average-loss units) are positive, and reporting them as
"profitable" would be the single most misleading thing this study could do. They
are noise with a sign.

The formula for the expected longest losing streak holds up as a rough guide but
is **not a ceiling**:

| rule | L_pred | L_actual | ratio |
|---|---|---|---|
| SPY S2 | 12.82 | **15** | 0.85 |
| SPY S1 | 11.68 | 10 | 1.17 |
| TLT S1 | 19.64 | 15 | 1.31 |
| GLD S1 | 13.62 | 8 | 1.70 |

The realised worst run exceeded the prediction on SPY S2. Plan for the streak the
formula names and do not treat it as a bound
(full table in [`handcheck-output.txt`](handcheck-output.txt)).

## 4. Which review timeframe can be trusted — and the honest answer is
   "the question is mostly not answerable"

The sibling engine's own verdict rule ranks buckets by |t| **only among buckets
with n_periods ≥ 12 and trades_per_period ≥ 5**. Applied here:

- **Y is the most trustworthy bucket, and it is the only one that qualifies
  anywhere — only for S2.** It wins because it is the one bucket big enough to
  contain ≥5 trades per period for a book that trades a few times a year. It is
  not that yearly P&L carries more information than daily P&L; the engine's own
  dependence caveat says the opposite, since Y literally contains every smaller
  bucket.
- **Even then, it barely qualifies.** For SPY S2 and TLT S2 the engine's verdict
  is the literal string **"NOT DISTINGUISHABLE FROM NOISE"** (|t| = 1.872 and
  0.367). Only GLD S2 (|t| = 2.344) and QQQ S2 (2.055) clear the ±2 band.
- **S1 fails both gates on every instrument**, so the engine returns
  `INSUFFICIENT DATA` and names the constraint rather than picking a bucket
  anyway.
- **S3 and S4 have no trades**, so `trades_per_period` is 0 and no bucket can
  ever qualify. The verdict machinery simply does not apply to a single
  continuous position — and bucketing one position does not manufacture
  independent observations.

The engine's own words are the conclusion: *more periods will not fix this; more
independent trades will.* Moving the review timeframe cannot create trades that
did not happen. **This study's timeframe analysis is therefore a negative
result: it identifies the one bucket that is not disqualifying, and shows that
the rule-set-to-rule-set comparison is not statistically supportable at any of
these frequencies for S1, S3 or S4.**

## 5. The all-weather answer

**No. "Profitable every time in every market condition" is not achievable with
any single one of these four rule sets, on this data.**

- No strategy has a single instrument on which every year was positive.
- The fewest losing instrument-years any strategy manages is **30 of 110** (S4).
- Every strategy except QQQ S3/S4 and SPY S4 has at least one regime cell with a
  negative annualised contribution.
- Worst single years: **−43.08%** (S1, QQQ 2000), **−41.94%** (S3, QQQ 2008),
  **−34.40%** (S4, GLD 2013), **−20.82%** (S2, SPY 2000).

This is a statement about the evidence, not a theorem. It is what four
instruments × 23–34 years of daily bars can show — and it is enough to reject
the claim as stated.

## 6. Complementarity: they lose in the SAME years

**All six pairwise correlations of yearly returns are positive, and they sit
between 0.666 and 0.887.** The pooled matrix:

| | S1 | S2 | S3 | S4 |
|---|---|---|---|---|
| **S1** | 1.000 | 0.887 | 0.800 | 0.780 |
| **S2** | 0.887 | 1.000 | 0.666 | 0.808 |
| **S3** | 0.800 | 0.666 | 1.000 | 0.786 |
| **S4** | 0.780 | 0.808 | 0.786 | 1.000 |

Over the 34 pooled years, S1 and S3 **both lost in 7**, and disagreed in only
**one year each way** — S1 lost alone in 2004, S3 lost alone in 2008. S1, S2 and
S3 all lost together in **5** years.

The three trend/hold rules are not three bets. They are one bet — long this
instrument — taken with three different exits. S2 does dodge some years that S1
and S3 lose (its faster 50-day exit leaves earlier), which is why S2's worst year
is milder while its *count* of losing years is higher. That is a real but small
asymmetry, not diversification.

**S4 is not the exception it looks like.** It is correlated with S1 at 0.780 and
with S3 at 0.786. Volatility scaling changes the *size* of the same long
position, not its direction. S4 is a position-sizing policy applied to the S3
bet, not a second bet.

So the honest route to an all-weather **book** is not a better long-only equity
rule. On this evidence it has to be sleeves whose losing years do not coincide —
a short or defensive sleeve, or an instrument whose bad years fall elsewhere.
**This study did not test one**, and it cannot conclude that one exists.

## 7. Corrections made before publishing

Recorded because a study that hides its own corrections is not trustworthy:

1. **S4 leverage accounting was wrong on the first pass.** The first
   implementation modelled the position as levering the *entire* equity
   (`w × close/open − 1`) instead of only the target exposure
   (`w × (close/open − 1)`, with the remainder in cash). The pre-registered rule
   is "position sized so that trailing vol targets 15%", which is the second
   form. The bug produced absurd compounding (S4 total return 2.4e18% on SPY) and
   was corrected **before any conclusion was drawn**, not to improve a result.
   After the fix, S4's numbers are ordinary: SPY +1616.42% at −45.03% drawdown.
   The realised leverage is now reported explicitly in §2 of `RESULTS.md` because
   it drives the comparison with S3.
2. **The TLT symbol in the brief was wrong.** `AMEX:TLT` returned
   `symbol_error [invalid symbol]`; TLT resolved to `NASDAQ:TLT`. The failed call
   is recorded in `README.md` rather than quietly replaced.
3. **The hand-check's first algebraic identity was wrong.** It asserted
   `E = (sum(wins) − sum(loss))/decided`. That is false: with
   `b = avg_win/avg_loss`, `E = p·b − (1−p)` equals the raw-R expectancy
   `p·avg_win − (1−p)·avg_loss` **divided by the average loss**. The hand-check
   now prints the correct identity, and §3 of `RESULTS.md` states that E is in
   *average-loss units*, not raw R. The pre-registered formula itself was applied
   correctly throughout.

Nothing else was changed. No parameter value was altered at any point.

## 8. What I did NOT test

Stated so the boundary of the claim is visible:

- **No transaction costs.** No commission, spread, slippage or borrow. This
  flatters every rule and flatters the trend rules most, since they trade 83–248
  times where buy & hold trades once. A 200-day rule that trades ~3 times a year
  needs only a few basis points per round trip to lose its already-thin edge.
- **No dividends or fund distributions.** The series is price-only. **TLT's
  price multiple over the window is 0.9561 — the fund's price is below where it
  started**, so TLT's rows are price returns, not total returns; long-bond
  coupons (~3–4%/yr) are excluded and would move TLT's numbers more than any
  other instrument's. This bias is *not* neutral: it penalises the always-long
  rules (S3, S4) more than it penalises the trend rules, because they forgo more
  distributions. **The TLT comparisons in this study should not be read as
  total-return comparisons.**
- **No parameter sensitivity.** Nothing here shows 200 days beats 150, and
  nothing here rules it out. That question was deliberately not asked.
- **No portfolio.** Each instrument is traded alone: no capital sharing, no
  correlation-aware sizing, no cross-instrument risk budget. §6 is therefore
  about the *rules*, not about any portfolio that could be built from them.
- **No shorts, options, futures, or intraday bars.** A long-only book was the
  registration.
- **Only four instruments**, all US-listed ETFs, all from one data feed.
- **The last bar was still forming at pull time** and may revise.
- **The pre-2004 history has no second source.** The Robinhood cross-check agrees
  to 0.00 bp, but only over a 30-session window in 2026 — the 1993–2004 TradingView
  bars are unverified against any second feed.

## 9. The one-paragraph version

Trend-following on these four instruments is a **risk-reduction** technique, not
a return technique: it cut the worst drawdown on every equity instrument roughly
in half and beat buy & hold on Sharpe on SPY, but it lost on raw return
everywhere and it failed completely on long Treasuries. Volatility targeting had
the best risk-adjusted line on three of four instruments and the fewest losing
years, but it does that by levering with no cap. **Every rule lost money in 27–40%
of the instrument-years available, no rule was clean on any instrument, and the
three trend/hold rules are one bet, not three.** The timeframe machinery cannot
rescue the comparison: only the yearly bucket ever qualifies, only for S2, and on
two of four instruments its t-statistic is not distinguishable from noise. If the
owner wants an all-weather outcome, the data points away from a better single
rule and toward sleeves with non-coincident losing years — which this study did
not test.
