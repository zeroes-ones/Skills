# FINDINGS — where "profitable every time" ends, measured

This is the narrative. Every number below is read off `RESULTS.md`, which is
rendered from `out/*.csv` of the run captured in `run-output.txt`. The commands
are in `README.md`.

---

## 1. The frontier exists, and it ends at essentially zero

The owner asked for every-period profitability. The honest, constructive form of
that request is the mixing line

```
r(λ) = λ · r_risky + (1 − λ) · r_cash
```

and the answer is where that line stops delivering 100 % positivity. For the
primary book (R4: equity, bond, gold and ex-US-equity trend, 25 % each,
2005-09-02 … 2026-10-14, 20 complete years):

| horizon | periods | largest λ with 100 % positive | CAGR there | cash CAGR | excess |
|---|---|---|---|---|---|
| year | 20 | **0.008** | 1.81 % | 1.78 % | **+0.03 %/yr** |
| half-year | 41 | 0.004 | 1.79 % | 1.78 % | +0.01 %/yr |
| quarter | 84 | **0.001** | 1.78 % | 1.78 % | **+0.00 %/yr** |
| month | 252 | **0.000** | 1.78 % | 1.78 % | **+0.00 %/yr** |
| week | 1101 | *n/a* | — | — | not even cash clears it |
| 2 weeks | 551 | *n/a* | — | — | not even cash clears it |
| day | 5311 | *n/a* | — | — | not even cash clears it |

Read the middle column against the last: **to be positive in every month of this
window you must hold no risky exposure at all**, and to be positive in every year
you may hold 0.8 % of the book, which earns three basis points a year over cash.
The `λ = 0` column *is* the cash rate — the identity check in `RESULTS.md`
section 2 shows a gap of exactly 0.000000000000 between the independently
computed cash CAGR and the `λ = 0` CAGR, for all five books.

So the one-sentence conclusion the data supports:

> **"Profitable every time" and "meaningful return" do not coexist in these
> books: the frontier's endpoint sits at 0.8 % exposure and 3 basis points of
> annual excess over cash, and every month with no losing period requires holding
> no risky asset at all — the only way to make the trade-off is to give up the
> return, and the exchange rate is measured here at 1 %.**

---

## 2. The one place the frontier does not end at zero: cash itself fails daily

The day / week / 2-week endpoints are `n/a`, and the reason is worth stating
plainly: **the cash proxy is not positive every day either.** In R4's window,
21 of 5311 days have a non-positive cash accrual —

* 8 days on which the 3-month T-bill yield printed exactly **0.00 %**;
* 11 days on which it printed **negative**, from −0.0025 % to **−0.0406 %**
  (2015-09-18 … 2015-10-14 and 2020-03-25 … 2020-03-30);
* the remainder where the index had no prior print.

US Treasury bill yields really did print zero in 2011–2015 and negative in
September 2015 and March 2020. This is not a defect of the cash proxy; it is what
the market did. Under a strict reading of "profitable", a cash-only plan fails
its own target on 21 days out of 5311 — so the *floor* of the frontier is not
100 % at daily resolution. It is 99.6 %.

The loose reading (a flat period is not a loss) does not rescue it either,
because those 11 days are strictly negative: 99.8 %, not 100 %.

**Practical consequence.** If the owner's standard is "no losing day, ever", the
goal is unattainable for any portfolio including cash. If the standard is "no
losing day, ever, except that a flat day counts as fine", it is still
unattainable. The only way to reach 100 % of positive *days* in this data is to
accept a rate that rounds to zero and hope it never goes negative — which is
exactly the thing the 2015 and 2020 prints show cannot be relied on.

---

## 3. The trade-off curve, and what each positive year costs

For R4, at the efficient point of each plateau — the largest λ that still holds
that many positive years (`RESULTS.md` §6b):

| years > 0 | max λ there | CAGR | excess vs cash | years lost |
|---|---|---|---|---|
| 100 % | 0.008 | 1.81 % | +0.03 % | none |
| 95 % | 0.165 | 2.30 % | +0.52 % | 1 (2015) |
| 90 % | 0.234 | 2.51 % | +0.73 % | 2 |
| 85 % | 0.282 | 2.66 % | +0.88 % | 3 |
| 80 % | 0.297 | 2.70 % | +0.92 % | 4 |
| 75 % | 0.343 | **2.84 %** | **+1.06 %** | 5 |
| 70 % | 0.610 | 3.62 % | +1.84 % | 6 |
| 65 % (the whole book) | 1.000 | **4.67 %** | +2.89 % | 7 |

The price is **not uniform**. Going from 70 % to 75 % of years costs 78 bp of
CAGR; 75 % to 95 % costs 54 bp for four times as many years; and the last five
points — 95 % to 100 % — cost 49 bp and buy exactly one calendar year (2015).
The expensive zone is the middle of the curve, where several years flip at once.
The cheap-looking zone next to cash is a trap: λ = 0.05 and λ = 0.165 both
deliver 95 % of years, but at 1.94 % and 2.30 %, so most of the de-risking in
that band gives away return for nothing. Only the top of each plateau is worth
holding.

**The best achievable yearly positivity above cash, at each threshold:**

| minimum excess over cash | best years > 0 | λ range (plateau) | CAGR at top of plateau | the losing years, in full |
|---|---|---|---|---|
| any positive excess | 100 % (20 of 20) | 0.000 … 0.008 | 1.81 % | none |
| **+1 %/yr** | **75 % (15 of 20)** | 0.324 … 0.343 | **2.84 %** | 2012, 2013, 2015, 2018, 2022 |
| +2 %/yr | 65 % (13 of 20) | 0.669 … 1.000 | 4.67 % | 2008, 2012, 2013, 2015, 2018, 2022, 2023 |
| +3 %/yr | **unattainable** | — | — | — |

At the whole book (λ = 1) R4 earns **4.67 % CAGR with a −14.83 % max drawdown**
and loses in **7 of 20 years**: 2008, 2012, 2013, 2015, 2018, 2022, 2023. That is
the price of the return: five years bought back at +1 %/yr of excess, seven more
at full exposure.

Widening the long window to 26 years (R2L: SPY + Nasdaq-100 trend) makes the
point harder:

| minimum excess | best years > 0 | λ | CAGR | losing years |
|---|---|---|---|---|
| +1 %/yr | 80.8 % (21 of 26) | 0.219 | 3.10 % | 2002, 2008, 2011, 2015, 2022 |
| +2 %/yr | 69.2 % (18 of 26) | 0.554 | 4.67 % | 2000, 2001, 2002, 2008, 2011, 2015, 2018, 2022 |
| +3 %/yr | 65.4 % (17 of 26) | 1.000 | 6.47 % | 2000, 2001, 2002, 2005, 2008, 2011, 2015, 2018, 2022 |

At full exposure that book loses **9 of 26 years** with a **−42.87 % max
drawdown**, and it loses in all three dot-com years (2000 −21.13 %, 2001
−7.44 %, 2002 −7.17 %).

---

## 4. What costs, and what does not

Costs do **not** change the frontier's answer, and they very much do change the
return at the risky end. At a 20 bps round trip:

| book | CAGR @ λ=1, 0 bps | CAGR @ λ=1, 20 bps | shift | %Y>0 | max λ with 100 % years |
|---|---|---|---|---|---|
| R4 | 4.67 % | 3.78 % | −0.89 pp | 65 % → 65 % | 0.008 → 0.007 |
| R9 | 3.22 % | 2.29 % | −0.92 pp | 68.4 % → 63.2 % | 0.009 → 0.007 |
| R10 | 2.70 % | 1.79 % | −0.90 pp | 70.6 % → 64.7 % | 0.010 → 0.008 |
| R2L | 6.47 % | 5.75 % | −0.72 pp | 65.4 % → 65.4 % | 0.005 → 0.004 |
| R1L | 6.65 % | 5.93 % | −0.72 pp | 65.6 % → 65.6 % | 0.005 → 0.004 |

The endpoint moves by one thousandth of exposure — it was never a return claim to
begin with. The return claim moves by ~0.9 pp a year, and for the two extended
books a full year flips from positive to negative. **Costs attack the return, not
the positivity.** That is why a cost-reduction campaign cannot buy back the seven
losing years, and why the frontier's end is not a fee problem.

---

## 5. Why the frontier is not linear — and how thin its end is

Two mechanisms, both measured (`RESULTS.md` §10):

**The first 5 % of risk is the expensive part.** Going from pure cash to 95 %
cash takes R4's daily positivity from 99.6 % to 66.2 % — a collapse. The reason
is scale: at λ = 0.05 the risky term contributes 0.05 × the book's daily swing
(standard deviation 0.51 %) while cash contributes 0.95 × a daily accrual of
0.0070 %. The ratio is **3.6**, so the *sign* of the day's return is decided by
the risky sliver, not by the cash. There is no "small" amount of risk that leaves
every day positive; the very first increment of exposure destroys daily
positivity, and everything after it is a slow grind.

**Flat days are a separate, real effect.** A trend book that is out of the market
returns *exactly* zero. Under the strict reading a flat day is not a profitable
day, so the book's own daily positivity understates its in-market win rate: R2L
is flat 22.6 % of days (43.0 % positive → 65.6 % non-negative), R1L 25.5 %
(40.6 % → 66.1 %), R4 only 4.7 %. This does not move the monthly, quarterly or
yearly endpoints — a 0.8 % cash sliver already makes any flat month positive —
but it does explain why the daily column of the frontier looks harsher than the
book's trading record suggests. One year in the whole study is exactly flat:
R1L's 2001 returns 0.000000 at λ = 1, which is why R1L's table shows 65.6 % of
years positive at λ = 1 and 68.8 % at λ = 0.999 — 0.1 % of cash buys back three
percentage points of positivity by turning a flat year positive.

**The end of the frontier is decided by one year and one basis point.** For R4,
2015 is the binding year. At λ = 0.008 it returns **+0.0038 %**; at λ = 0.009 it
returns **−0.0017 %**. The entire difference between "positive in every year" and
"not positive in every year" is **0.0056 percentage points** of one year's return.
The endpoint is real, and it is also a knife edge — 2015 was the year the trend
book was run over repeatedly in a directionless market while bills yielded
nothing, so cash had no cushion to absorb the loss.

---

## 6. What was verified, and what the first attempt got wrong

* **Determinism.** Two consecutive runs: 0 differing lines of stdout, 0 differing
  bytes across all 59 `out/*.csv`.
* **Independent re-derivation.** `handcheck.py` rebuilds the frontier from
  `data/*.csv` with its own reader, SMA, alignment, simulator, cash accrual,
  bucket keys and CAGR, importing neither `study.py` nor the engine.
  Max absolute gap over 21 λ × 7 buckets × 2 books: **4.9×10⁻⁷**, which is the
  6-decimal rounding of the written CSVs. The cash identity held at exactly
  **0**, and the endpoint bisection agreed **exactly** at 0.008.
* **Reproduction of prior work.** This study's simulator reproduces the
  weather-test's published four-sleeve book to **6×10⁻⁸** on CAGR and **1.6×10⁻⁷**
  on max drawdown, with the same window and the same losing-year count. The
  sleeve rule and simulator are genuinely the same ones, not a lookalike.
* **The reuse of sibling data was verified, not assumed.** 8000 overlapping SPY
  rows: 7999 identical, the one difference being the still-forming final bar's
  volume. 8000 overlapping VIX rows: all identical. Fresh pulls of TLT, GLD, QQQ
  and EEM were likewise compared and agree except the final bar's volume.
* **A real error was caught by the hand-check.** The first worked example
  computed the book's daily return as a *fixed* 25 % blend of the sleeve returns.
  The comparison against the study's own daily trail disagreed by ~1×10⁻⁴,
  because the book's weights drift between monthly rebalances. The example was
  changed to print the weights actually held and now agrees to 4×10⁻⁹. The
  disagreement was small and it was found, not smoothed over.

---

## 7. What remains untested, and what would change the answer

1. **Total return.** Every series here is price-only. Bonds, credit and gold are
   understated, so the risky book's return — and therefore the bar the frontier
   has to clear — is understated. A total-return version would *raise* the return
   available at the risky end; it would not move the endpoint much, because the
   endpoint is a statement about loss years, not about average return. Worth
   doing properly before any conclusion is acted on.
2. **Sleeve shape.** All five books are the same SMA(200) rule on different
   assets. Mean-reversion, carry, cross-asset relative value and held long
   volatility are absent. The weather-test's own finding was that a
   well-diversified book could still lose 87 % a year because one sleeve had
   negative drift; the mirror risk here is that a *different* sleeve shape has
   fewer loss years and therefore shifts the endpoint. Nothing in this study
   shows it cannot. This is the single most valuable untested extension.
3. **A vetting screen before book construction.** The weather-test argues for
   pre-registering a per-sleeve edge screen on data preceding the book. That
   would change the book, and therefore the frontier. It was not done here.
4. **Leverage and the short side.** λ ≤ 1 only. Nothing here constrains λ > 1,
   which would push the frontier down and to the right.
5. **A real cash instrument, with fees.** The proxy is an upper bound at 0 bp.
   A 15 bp expense ratio would lower every row of the `λ`-low end and make the
   endpoint's excess smaller — possibly negative. `study.py` accepts
   `CASH_FEE_BPS` for exactly this, and the headline run used 0.
6. **Parameter sensitivity.** SMA(200) was fixed before the run, as it had to be.
   Nothing here shows 200 beats 150, or rules it out.
7. **Sample size.** 20 complete years for R4, 32 for R1L. "100 % of years
   positive" is a statement about 20 or 32 periods. It is not a guarantee and it
   is not an out-of-sample claim. The engine's own `n_effective` is reported
   next to every bucket in `RESULTS.md` §12 for precisely this reason.
8. **The practical cost of the recommendation.** Holding 0.8 % of a four-sleeve
   book for the sake of being positive in every year is not a strategy anyone
   would run — the position is smaller than the noise in any account, and the
   rebalancing alone would cost more than the excess. That is the point: the
   frontier's endpoint is not advice, it is the *price*, and the price is that
   the answer to the owner's question is "yes, but only by not investing".

---

## 8. The short version

1. The frontier is real, measurable, and reported at all seven horizons.
2. It ends at **λ = 0.008 (0.8 % exposure, +0.03 %/yr over cash) for years**,
   **λ = 0.001 (+0.00 %/yr) for quarters**, and **λ = 0 for months**.
3. At daily, weekly and biweekly resolution it does not end anywhere, because
   **cash itself was not positive on 21 of 5311 days**.
4. The return cost of each additional positive year is **not uniform**: ~49 bp for
   the last five points of yearly positivity, ~54 bp for the four points before
   that, ~78 bp for one point in the middle.
5. Costs (~0.9 pp/yr at 20 bps) attack the return, not the endpoint.
6. The endpoint is decided by **one year (2015) and 0.0056 percentage points** of
   return.
7. What would change the answer is a sleeve with fewer loss years, or a book that
   is positive in the flat, directionless years — not lower fees, not a better
   cash instrument, and not more diversification of the same rule.
