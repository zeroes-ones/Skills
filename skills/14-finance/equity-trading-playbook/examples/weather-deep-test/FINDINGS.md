# FINDINGS — what the extra sleeves actually bought

This is the honest narrative. Every number is from the run captured in
`RESULTS.md`; nothing here is an estimate unless it is labelled `[ESTIMATED]` or
`[MODELED]`.

The short version: **the positivity frontier did move — to 100% of years at 6.3%
of capital at risk paying +0.48%/yr over cash, up from the predecessor's 0.8%
exposure at +0.03%/yr — but roughly two-thirds of that move comes from one modelled
sleeve, the six-sleeve book is only 2.37 independent bets, diversification halved
the drawdown without measurably improving Sharpe, and nothing clears the
pre-registered bar.**

---

## 1. The headline table

Primary window 2005-09-30 → 2026-10-14, 21.04 years, 5,292 sessions.
`[ESTIMATED]` dividends, 5 bps round trip.

| series | CAGR | maxDD | Sharpe (exc. cash) | pos. years | pos. Q | pos. M | losing years |
|---|---|---|---|---|---|---|---|
| **BOOK** | 8.68% | −28.59% | 0.58 | 85.0% (17/20) | 83.3% | 79.4% | 2008, 2018, 2022 |
| **BOOK-NOV** | 4.52% | **−8.08%** | 0.56 | 75.0% (15/20) | 76.2% | 66.3% | 2008, 2012, 2015, 2018, 2022 |
| **BOOK-VT** | 2.68% | **−3.47%** | 0.51 | **95.0% (19/20)** | 78.6% | 71.4% | 2015 |
| T trend | 4.39% | −7.31% | **0.65** | **90.0%** | 72.6% | 67.9% | 2015, 2022 |
| C carry (pair) | 1.12% | −22.32% | −0.09 | 65.0% | 76.2% | 63.1% | 2008, 2010, 2011, 2014, 2015, 2018, 2020 |
| V VRP `[MODELED]` | 10.01% | **−99.83%** | **0.74** | 75.0% | 83.3% | 90.1% | 2008, 2009, 2018, 2020, 2022 |
| H hedge | 1.29% | −14.08% | −0.12 | 65.0% | 51.2% | 49.6% | 2009, 2010, 2012, 2013, 2014, 2017, 2021 |
| X x-sec momentum | 11.01% | −29.97% | 0.55 | 75.0% | 72.6% | 59.5% | 2008, 2012, 2015, 2018, 2022 |
| B SPY buy & hold | **11.08%** | −55.35% | 0.55 | 85.0% | 73.8% | 65.5% | 2008, 2018, 2022 |
| CASH | 1.77% | −0.00% | n/a | 100% | 100% | 100% | none |

Price-only, for contrast: BOOK 7.53% / −28.90% / 0.50; SPY 9.10% / −56.47% / 0.46.
The dividend assumption is worth 0.7–2.2 pp of CAGR depending on the series (§5 of
`README.md`), and it is an assumption, not a measurement.

---

## 2. What the extra sleeves bought

### 2.1 They bought **drawdown** and **quarterly/monthly positivity**, not Sharpe

This is the most important result in the study and it is not the one hoped for.

Against plain SPY buy and hold, the six-sleeve book gives up **2.40 pp of CAGR**
(8.68% vs 11.08%) and buys:

| | SPY | BOOK | change |
|---|---|---|---|
| CAGR | 11.08% | 8.68% | −2.40 pp |
| max drawdown | −55.35% | −28.59% | **+26.8 pp better** |
| Sharpe | 0.55 | 0.58 | **+0.03 — within noise** |
| years positive | 85.0% | 85.0% | **no change** |
| quarters positive | 73.8% | 83.3% | **+9.5 pp** |
| months positive | 65.5% | 79.4% | **+13.9 pp** |
| worst 12-month return | −43.75% | −24.97% | **+18.8 pp better** |
| worst 36-month return | −39.15% | −5.50% | **+33.7 pp better** |

**The Sharpe barely moved.** Twenty-one years of six sleeves, thirty-one
instruments and a cross-asset universe produced a book whose risk-adjusted return
is statistically indistinguishable from owning the index. What it produced instead
is a book that is positive far more often at the quarterly and monthly horizon and
that never has a 36-month hole worse than −5.5%, because the trend sleeve and the
hedge cut the tails.

That is exactly what the identity `P(positive) ≈ Φ(Sharpe·√fraction)` predicts and
it is worth saying plainly: **if Sharpe is unchanged, positivity at long horizons
is bought only by removing downside, which costs return.** The book's 85% of years
is not better than SPY's 85% — it is the *same number* bought a different way (SPY:
3 losing years with a worst of −37.15%; BOOK: 3 losing years with a worst of
−19.69%). The book converts a −37% year into a −20% year; it does not convert a
losing year into a winning one.

### 2.2 They bought it through one high-Sharpe, un-investable sleeve

The book's improvement over BOOK-NOV (the same book without the modelled VRP
sleeve) is unambiguous:

| | BOOK-NOV | BOOK | change |
|---|---|---|---|
| CAGR | 4.52% | 8.68% | **+4.16 pp** |
| Sharpe | 0.56 | 0.58 | +0.02 |
| years positive | 75.0% | 85.0% | **+10 pp** |
| max drawdown | −8.08% | −28.59% | **−20.5 pp worse** |

So the modelled variance-risk-premium sleeve contributes **+4.2 pp of CAGR and +2
more positive years while tripling the drawdown**. It is not a diversifier: its
yearly correlation with the book is **+0.86**, the *highest* of any sleeve, and it
dominates the book's risk because it runs at 179% annualised vol while everything
else runs at 3–19%.

And it is un-investable as defined. Its Sharpe, **0.74, is the best of any sleeve in
the study**, and its monthly positivity is **90.1%**, the highest of any sleeve. Yet
it compounds to a **−99.83% drawdown** and its worst month is **−93.57%**, because
`units = capital / width` means a single session in which SPY gaps through both
strikes loses ~100% of the posted margin. **A Sharpe ratio cannot see ruin risk.**
This is the single most important caveat in the study.

BOOK-VT is the controlled experiment on sizing alone: the identical trade, scaled by
one uniform rule (`k = min(1, 4%/vol)` ⇒ `k_V = 0.0224`), gives **+2.68% CAGR,
−3.47% maxDD, 95% of years positive** — i.e. the V sleeve's *edge* is real and small
once you take only 2.2% of it, and its headline return is an artefact of leverage.

### 2.3 They bought nothing from the genuinely uncorrelated sleeves

Ranked by yearly correlation with the BOOK:

| sleeve | yearly corr with BOOK | its own Sharpe | verdict |
|---|---|---|---|
| H_b `[MODELED]` put overlay | **−0.671** | −0.76 | a real hedge, but it costs 5%/yr |
| H (blend) | −0.048 | −0.12 | near-zero correlation, negative Sharpe |
| CASH | +0.225 | n/a | |
| H_a (VIX rule) | +0.357 | +0.38 | the one hedger with a positive Sharpe |
| C carry | +0.629 | **−0.09** | correlated *and* unprofitable |
| T trend | +0.681 | +0.65 | |
| X x-sec momentum | +0.684 | +0.55 | |
| SPY buy & hold | +0.735 | +0.55 | |
| V VRP `[MODELED]` | +0.861 | +0.74 | |

**The sleeves that are genuinely uncorrelated with the book are the ones with no
return.** H_b is the only negative correlation in the table and it earns −1.30% CAGR
against 1.77% cash. The measured sleeves that earn anything (T, X, B) are all 0.68+
correlated with each other. This is the wall the study hit: on this universe, a
sleeve either correlates with the equity beta or it does not pay.

H_a is worth singling out: it is the only sleeve that is *both* meaningfully
decorrelated from the book (+0.357) *and* has a positive Sharpe (+0.38), and it
earns 3.83% CAGR with 85% of years positive for −13.58% maxDD. A rule triggered by
VIX rather than applied to VIX — deliberately not the trend-on-VIX sleeve the
predecessor found loses 86.9%/yr compounded.

### 2.4 The diversification is real but thin: **2.37 independent bets**

Mean pairwise **yearly** correlation across the book's five sleeves: **ρ̄ = +0.278**.

| group | n | ρ̄ | independent bets |
|---|---|---|---|
| the 5 sleeves of BOOK | 5 | +0.278 | **2.37** |
| T and X alone | 2 | **+0.722** | **1.16** |
| the 5 sleeves + SPY buy & hold | 6 | +0.295 | 2.42 |

Two things follow.

First, **T and X are the same bet** (1.16 independent bets, ρ = +0.72 yearly). The
cross-sectional momentum sleeve on a 31-instrument cross-asset universe is not a
new source of return — it is the trend sleeve wearing a different hat, because both
end up long the same risk-on assets whenever those assets are trending.

Second, the honest headline: **the widest realistic cross-asset universe this data
source will resolve produced 2.37 independent bets.** The predecessor's 14-name
equity basket produced **2.53**. Widening the universe from 14 equities to 31
cross-asset instruments did **not** increase the number of independent bets — it
slightly reduced it, because the cross-asset universe adds bonds and gold (which
correlate with each other and with equities in a crisis) rather than adding truly
independent risk. The predecessor's narrowing study is corroborated from the other
direction.

---

## 3. Where the positivity frontier moved to

The frontier is parameterised by λ, the fraction of capital at risk; the rest earns
cash. `[ESTIMATED]` dividends, 5 bps.

### 3.1 The comparison that matters

| | predecessor (SPY/TLT/GLD/EEM, 20y) | this study BOOK | this study BOOK-VT |
|---|---|---|---|
| λ for **100% positive years** | 0.008 | **0.063** | 0.144 |
| CAGR there | 1.80%* | **2.25%** | 1.91% |
| excess over cash | **+0.03%/yr** | **+0.48%/yr** | +0.14%/yr |
| λ for **100% positive quarters** | 0.001 | 0.003 | 0.012 |
| λ for **100% positive months** | ~0.000 | 0.001 | 0.002 |
| full-exposure CAGR | 4.67% | **8.68%** | 2.68% |
| full-exposure maxDD | −14.83% | −28.59% | **−3.47%** |
| losing years | 7 | **3** | 1 |

\* the predecessor's cash CAGR is not restated here; its reported excess over cash
at that λ was +0.03%/yr.

**The frontier moved materially: 0.8% → 6.3% of capital deployable at 100% of years
positive, and the reward for deploying it went from +0.03%/yr to +0.48%/yr over
cash.** That is roughly 8× the deployable capital and 16× the excess return — and,
critically, it breaks the predecessor's finding that "nothing reached 100% of years
at a positive return". It now does.

**But the honest attribution:** BOOK-NOV (without the modelled V sleeve) reaches only
λ = 0.025, +0.08%/yr over cash. So of the 0.8% → 6.3% movement, the part that
survives without the modelled sleeve is 0.8% → 2.5%. **About two-thirds of the
frontier advance is the `[MODELED]` variance-risk-premium sleeve**, whose P&L is
itself a function of one unmeasured assumption (§4).

### 3.2 Daily, weekly and biweekly still have NO endpoint

The predecessor found that no λ makes cash positive on every *day*, because the
T-bill yield itself went negative on 21 of 5,311 days. This study reproduces that
exactly: **the cash return was negative on 11 of 5,291 sessions (0.21%)** in this
window. The λ frontier is therefore reported for years, quarters and months only,
and the largest λ with 100% of *months* positive is 0.001 — a book that is 99.9%
cash. **There is no exposure level at which this, or any, book is never down on a
daily or weekly clock.** The identity `P(positive) ≈ Φ(Sharpe·√fraction)` is
brutal at short horizons and no sleeve construction escapes it.

### 3.3 The best point actually achieved

**BOOK, `[ESTIMATED]` dividends, 5 bps, λ = 0.553:**

| | |
|---|---|
| CAGR | **5.75%** |
| max drawdown | −16.45% |
| Sharpe (excess of cash) | 0.58 |
| years positive | **18/20 = 90.0%** |
| losing years | **2008 (−10.47%), 2018 (−5.44%)** |
| quarters positive | 86.90% |
| months positive | 81.35% |
| worst month | −6.20% (2018-10) |

For reference, the predecessor's *full-exposure* 4-sleeve book earned 4.67% CAGR
with −14.83% drawdown and 7 losing years. Here, at 55% exposure, the book earns
**5.75%** — more — with a comparable drawdown and **2 losing years instead of 7**.
That is a genuine, measurable improvement in weather-proofing, and it is the best
point on the trade-off the study can honestly claim.

---

## 4. What is `[MODELED]` and what that is worth

### 4.1 The VRP sleeve's sign depends on one unmeasured number

| skew steepness assumed on the short strike | V sleeve CAGR |
|---|---|
| 0.0 vol points | **−2.54%** |
| **1.5 vol points (the base case)** | **+10.01%** |
| 3.0 vol points | +15.50% |

**The sign of the sleeve flips inside the plausible range.** The predecessor
measured the variance risk premium as real — VIX above subsequent realised vol in
82.9% of windows, by +3.62 vol points, negative only in 2008 — and found the
harvested edge goes to zero at **+1.5 vol points of skew**. That break-even is
carried forward here as the base case, and the sensitivity above shows what it is
worth: the base case is not a measurement of realised skew, it is an assumption of
it, and everything the V sleeve contributes to this study rests on it.

Note also that the sleeve's daily mark never sees realised volatility: IV is taken
from VIX(t−3) and then held *fixed* for the life of each spread. So the model
contains no vol-of-vol P&L and cannot lose money from implied vol moving against it
inside a month — a real short-premium book can and does.

### 4.2 Everything modelled, listed

* **V (VRP)** — Black–Scholes pricing, a closed-form 16Δ strike solve, a 3-session
  VIX lag, a fixed intra-spread IV, no bid/offer, no early exercise, no pin risk, no
  dividend risk, cash rate floored at zero in the pricing function. **Settlement is
  the only thing anchored to reality: intrinsic against the real SPY path.**
* **H_b (put overlay)** — same model, priced at ATM + 3.0 vol points, 60 DTE, 5%
  OTM, with a declared premium budget of 5%/year spent at 1/12 a month. It is a cost
  model, not a hedge model: it does not roll strikes.
* **BOND10M** — `r = −7.5·Δy10 + y10/252` with **constant** modified duration. It
  exists only so the REDUCED book has a duration leg before 2002, and constant
  duration is wrong in exactly the period it is used for (the 1999–2002 long-bond
  rally), so the REDUCED book's dot-com coverage is the weakest number in the study.

`out/vrp_rolls.csv` carries every roll's exact inputs (signal date, S0, VIX(t−3),
IV, σ_short, σ_long, r, q, K1, K2, width, credit, credit/width) so the model can be
audited roll by roll. `handcheck.py` independently re-derives one roll from VIX and
SPY prices and lands within 8.0e-11 of the study's own numbers.

### 4.3 The measured sleeves are genuinely measured

T, C, X, B and the cash accrual are price arithmetic on real OHLCV, with one
`[ESTIMATED]` constant dividend yield added. `verify_sources.py` confirms the
inputs agree to the last cent with four sibling studies' independent pulls over
311,224 shared dates (0 price disagreements), and `handcheck.py` rebuilds the trend
sleeve for a sample month from raw prices and matches the engine's own compounding
to **5.2e-11**.

---

## 5. The regime grid: the structural DOWN-state problem is mostly, but not fully, fixed

Monthly book return by trend state (SPY vs SMA(200), read at the previous
month-end) × realised-vol tercile (trailing 20-session SPY vol, previous month-end).
`[ESTIMATED]` dividends, 5 bps. Terciles are an **in-sample** partition.

| trend | vol | months | BOOK mean monthly | BOOK-NOV | BOOK-VT |
|---|---|---|---|---|---|
| UP | LOW | 79 | +0.77% | +0.29% | +0.22% |
| UP | MID | 78 | +0.86% | +0.41% | +0.22% |
| UP | HIGH | 32 | +1.42% | +0.83% | +0.38% |
| DOWN | LOW | **0** | n/a | n/a | n/a |
| DOWN | MID | 5 | +0.28% | +0.81% | +0.21% |
| DOWN | HIGH | 48 | **−0.01%** | +0.12% | +0.10% |
| | | | **1/6 negative** | **0/6** | **0/6** |

The predecessor measured long-only trend as structurally negative in the DOWN state
— negative in **10 of 10 survivors at DOWN×MID** — because the rule can only go flat
*after* the price crosses and cannot go short. Here **DOWN×MID is positive
(+0.28%)** and the only negative cell is **DOWN×HIGH at −0.01%/month**, which is
flat rather than negative. The extra sleeves (the hedge H_a, and the VRP sleeve
whose best months are high-vol months) did absorb the DOWN-state bleed.

Two caveats must travel with this table:

* **DOWN×LOW has zero months.** The trend state and the volatility tercile are
  nearly collinear on this window — a genuine down-trend essentially never happens
  in a low-vol regime. The grid is really 5 cells pretending to be 6, and "0 of 6
  negative" should be read as "0 of 5 populated".
* **The −0.01% cell is not a victory.** DOWN×HIGH is where the book must earn its
  keep, and the book is flat there. The measured improvement over the predecessor is
  "not bleeding" rather than "making money in the storm".

Worst single month across the whole window (`[ESTIMATED]` dividends, 5 bps):
**BOOK −11.25% (2018-10), BOOK-NOV −3.28% (2022-06), BOOK-VT −0.95%.**
For the sleeves: V −93.57% (2018-10, `[MODELED]`), SPY −16.38% (2008-10),
X −14.69% (2022-06), C −7.22% (2008-11), H −2.99% (2010-07),
T −2.73% (2024-12).

---

## 6. The dot-com bear is still a loss

The main window cannot see 2000–2002 because GLD/QQQ/IEF et al. do not exist. The
**REDUCED** book (T 0.40 + X 0.15 + V 0.10 + H 0.10 + BOND10M 0.15 + CASH 0.10, on
the 9 instruments that have a print on 1998-12-22) covers **1998-12-22 → 2026-10-14,
27.81 years, 5 losing years: 2001, 2002, 2008, 2018, 2022.**

| year | REDUCED book | T | X | V `[MODELED]` | H_a | H_b | BOND10M | SPY |
|---|---|---|---|---|---|---|---|---|
| 2000 | +14.01% | −3.88% | +13.68% | +136.32% | +5.99% | +3.69% | +16.37% | −9.06% |
| **2001** | **−2.77%** | −4.11% | −9.81% | −40.95% | +3.40% | +3.80% | +5.10% | −11.31% |
| **2002** | **−9.83%** | −3.52% | −16.49% | −77.81% | +1.62% | +1.43% | +14.86% | −21.40% |

Read that table carefully, because it is the most sobering result in the study:

* **The trend sleeve lost money in 2001 and 2002 while flat.** "Flat below SMA(200)"
  is decided *after* the cross, so the sleeve is repeatedly whipsawn back in on
  false signals — −4.11% and −3.52% in years when the underlying fell 11% and 21%.
  Being long-only and flat-capable is not the same as being defensive.
* **The only thing that worked was the bond sleeve** — `[MODELED]` BOND10M at
  +5.10% and +14.86% — and it is the weakest number in the study (constant duration).
* **The modelled VRP sleeve was the largest loser** in both years (−40.95%, −77.81%).
* The hedges (H_a, H_b) each earned 1–6% and did their job.

**So the honest answer to "does the widest realistic cross-asset book survive the
dot-com bear?" is: no.** Over 27.81 years the REDUCED book is positive in 22 of 27
years (81.5%) with a 10.37% CAGR and −31.43% maxDD — good, and worse than SPY's
8.82%/-55.35% on drawdown but not on return — but the two years of the actual
equity bear that the window can see are both losses. The positivity record is built
over a period that contains 2008 but not 2000–2002.

---

## 7. Costs

`[ESTIMATED]` dividends; CAGR lost going from 0 to 20 bps round trip.

| sleeve | CAGR 0 bps | CAGR 5 bps | CAGR 20 bps | drag at 20 bps |
|---|---|---|---|---|
| T trend | 4.50% | 4.39% | 4.06% | **0.44 pp** |
| C carry | 1.14% | 1.12% | 1.05% | 0.09 pp |
| X x-sec momentum | 11.23% | 11.01% | 10.36% | **0.88 pp** |
| H_a hedge | 4.12% | 3.83% | 2.94% | **1.19 pp** |
| H_b put overlay | −1.30% | −1.30% | −1.31% | 0.01 pp |
| V VRP `[MODELED]` | 10.67% | 10.01% | 8.05% | **2.62 pp** |
| SPY buy & hold | 11.08% | 11.08% | 11.08% | 0.01 pp |

Two readings:

* **For the measured trend and cross-sectional sleeves, costs are not the binding
  constraint.** 20 bps round trip — a punitive assumption for monthly ETF trading —
  costs the trend programme 0.44 pp/yr. The predecessor's first trend study carried
  no costs at all; this closes that gap and the gap was small.
* **For the modelled option sleeves, costs dominate.** The VRP sleeve rolls 252
  times and is charged one round trip per roll; at 20 bps that is 2.62 pp/yr, and at
  5 bps it is 0.66 pp — a quarter of the sleeve's edge at the base skew assumption.
  Any real implementation would need to be far cheaper than a 20 bps round trip per
  monthly roll, or it would not be worth running.

Book-level costs are small and visible in the book table: BOOK 8.85% → 8.68% → 8.16%
across 0/5/20 bps.

---

## 8. The pre-registered success bar: nothing clears it

**Bar:** positive in ≥90% of years **AND** ≥75% of quarters **AND** Sharpe > 0.8
**AND** CAGR above cash.

| book | posY ≥ 90 | posQ ≥ 75 | Sharpe > 0.8 | CAGR > cash | verdict |
|---|---|---|---|---|---|
| BOOK div 5 bps | ✗ (85.0%) | ✓ (83.3%) | ✗ (0.58) | ✓ (8.68%) | **fail** |
| BOOK-NOV div 5 bps | ✗ (75.0%) | ✓ (76.2%) | ✗ (0.56) | ✓ (4.52%) | **fail** |
| BOOK-VT div 0 bps | **✓ (95.0%)** | ✓ (78.6%) | ✗ (0.54) | ✓ (2.74%) | **fail** |
| REDUCED div 5 bps | ✗ (81.5%) | ✓ (82.9%) | ✗ (0.64) | ✓ (10.37%) | **fail** |

**VERDICT: nothing clears the bar.** Not at any cost level, in either dividend
treatment, for any of the four books.

Three things are worth saying about *why*, because the shape of the failure is the
result:

1. **The binding constraint is Sharpe, always.** The positivity clauses are
   satisfiable and are satisfied (BOOK-VT at 95% of years and 78.6% of quarters;
   BOOK at 83.3% of quarters). The clause that fails in **every one of the 24
   verdict rows** is `Sharpe > 0.8`. The best Sharpe anywhere in the study is the
   `[MODELED]` VRP sleeve at **0.74** — and it loses 99.8% of its capital, so a
   Sharpe near 0.8 exists here only in configurations that are uninvestable.
   **Among sleeves a desk could actually hold, the best Sharpe is the trend
   sleeve's 0.65** — the simplest sleeve in the study. Twenty-one years of six
   sleeves over thirty-one cross-asset instruments cannot produce a survivable
   0.8 Sharpe.
2. **The positivity and return clauses fight each other exactly as the identity
   says.** The configuration with the best positivity (BOOK-VT, 95% of years) has
   the *lowest* Sharpe of the three books (0.51) because it is 36.6% cash. You can
   have the years or you can have the risk-adjusted return; you cannot have both
   without leverage, and leverage re-imports the drawdown.
3. **The bar was declared before the run and is not being moved.** 0.8 was chosen
   with the predecessor's 0.65 in hand and an expectation that a wider universe
   would lift it. It did not.

**Closest cell: BOOK-VT, dividend-adjusted, 0 bps — 95% of years, 78.6% of
quarters, CAGR 2.74% against 1.77% cash, Sharpe 0.54.** It fails one clause, and
fails it by 0.26.

---

## 9. What this study does NOT settle

Ordered by how much they matter.

1. **Whether the VRP sleeve's skew assumption is right.** Its sign flips inside the
   plausible range (§4.1). Settling it needs a paid options chain with real bid/ask
   at the 16Δ strike, not a VIX-derived Black–Scholes price. **This is the single
   largest open question**, because two-thirds of the frontier advance depends on it.
2. **Whether any of this survives after 2026-10-14.** Every number here is
   in-sample on one realisation of history. The predecessor's 7,380-configuration
   sweep found that only 10 of 1,620 clear a Bonferroni bar and that more iterations
   made results *monotonically worse*; nothing in this study is exempt.
3. **Shorting.** The inherited structural weakness — a long-only trend sleeve cannot
   make money in a down-trend, only stop losing — is diagnosed and only partly
   worked around. A genuine short leg (trend-following the downside, or an explicit
   short-equity sleeve with a defined risk budget) is the obvious untested lever,
   and 2001–2002 is the year that says so.
4. **Rebalancing cadence.** Everything here is monthly. Nothing is known about
   weekly, quarterly or band-based rebalancing, and the positivity identity is
   sensitive to the period fraction.
5. **Signal lookbacks.** SMA(200), 126 sessions and SMA(50) on VIX are each single
   declared values with no sensitivity range. Changing them would be a new
   pre-registration, and tuning them here would be the exact error the brief forbids.
6. **A hedge with an optimised cost budget.** H_b spends a declared 5%/year and
   earns −1.30%. It has the only negative yearly correlation with the book (−0.671)
   and is therefore the most promising thing to *improve* rather than replace — but
   it was not optimised, by design.
7. **Whether the 2.37-bets ceiling is a property of markets or of this sleeve set.**
   A market-neutral equity sleeve, a carry sleeve that is not a bond pair, or an
   explicit cross-asset short-volatility sleeve might add a third or fourth
   independent bet. Nothing here tests that.
8. **`BOND10M`.** The weakest input in the study is the one that carries the
   dot-com years. A real pre-2002 Treasury price series (or mutual-fund NAV series)
   would fix it and is not available from this source.

---

## 10. The one-line answer

**The frontier did move — 100% of years becomes reachable at 6.3% of capital at
risk earning +0.48%/yr over cash, versus 0.8% and +0.03%/yr before — and the best
honest point is 90% of years positive, 86.9% of quarters, 5.75% CAGR and −16.45%
drawdown at 55% exposure with only two losing years (2008, 2018). But the six-sleeve
cross-asset book is only 2.37 independent bets (barely fewer than a 14-name equity
basket's 2.53), its Sharpe (0.58) is indistinguishable from SPY's (0.55), about
two-thirds of the frontier advance comes from a modelled sleeve whose sign depends
on an unmeasured skew assumption, the best-Sharpe sleeve in the study loses 99.8%
of its capital, the dot-com bear is still a loss, and nothing clears the
pre-registered bar.**

The lever the brief identified — buy positivity with Sharpe, and Sharpe with
genuinely uncorrelated sleeves — is the right lever. This study's answer is that on
the widest universe the data source will resolve, **the uncorrelated sleeves do not
pay and the paying sleeves are not uncorrelated.**
