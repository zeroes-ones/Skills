# index-options-test — FINDINGS

The honest narrative. Every number is in [`RESULTS.md`](RESULTS.md); the model
and its limitations are in [`README.md`](README.md).

**Window:** 2001-03-13 … 2026-10-14. 6 436 sessions, **24 complete years
(2002–2025)**, 102 quarters, 306 months. Cash CAGR **+1.80 %**.
**Every option number below is `[MODELED]`.**

---

## 1. The short version

1. **One book clears the pre-registered bar, and only one.** The three-index
   **buy-write (S3)** — long SPY/QQQ/IWM in equal sleeves, selling a 30-DTE
   ~30-delta call each month — is positive in **83 % of years**, **75 % of
   quarters** and **70 % of months**, with CAGR **+10.53 %** against cash
   **+1.80 %** and max drawdown **−28.74 %**. It clears (a), (b) and (c); (d) is
   reported, not thresholded.

2. **The premium-selling stream alone (S2) does not clear it — but by one year.**
   S2 is positive in **79 % of years** and **79 % of quarters** with CAGR
   **+2.97 %**. It misses the 80 % year threshold by a single year out of 24,
   and **it only clears at zero costs** (FREE: 83 %/80 %, +4.54 %; LOW: 79 %/79 %;
   HIGH: 75 %/78 %).

3. **The options carry stream does raise positivity, and this is the one place
   this study moves the predecessor's frontier.** For a book made only of these
   three index ETFs, the largest exposure at which **100 % of years** are
   positive is **λ = 0.0773**, earning **+2.50 %** CAGR versus cash **+1.80 %** —
   **+0.70 %/yr** of excess. The sibling cross-asset trend book's frontier ended
   at **λ = 0.008 → +0.03 %/yr**. Same arithmetic, ~10× the exposure and ~23× the
   excess return. **For quarters and months nothing changes:** λ = 0.0008 and
   0.0000, i.e. you must still hold essentially no risk to be positive every
   quarter, and literally none to be positive every month.

4. **The tail hedge does not work, and it fails in an interesting way.** The
   pre-registered S4 loses **−14.84 % a year** with a **−98 %** drawdown. Two
   structural reasons, both measured: the hedge costs **4.66×** the premium it is
   supposed to be funded from, and in **584 of 915 months (64 %)** the
   "5 %-OTM tail put" strikes **above** the spread's short strike.

5. **The whole edge is a bet on three modelled inputs.** S2 clears at FREE costs
   and fails at LOW; it fails at IV × 0.8 and clears at IV × 1.2; it dies
   completely at **1.5 vol points** of sold-leg skew. That matrix is §15 of
   `RESULTS.md`.

---

## 2. What the carry stream added

### 2.1 S2: a high-hit-rate, low-return stream

| | S1 trend | **S2 premium** | S3 buy-write | S5 blend | S6 buy&hold |
|---|---|---|---|---|---|
| CAGR | +7.07 % | **+2.97 %** | +10.53 % | +6.16 % | +9.23 % |
| maxDD | −21.83 % | **−26.75 %** | −28.74 % | −18.84 % | −56.30 % |
| Sharpe (Rf = cash) | 0.47 | **0.18** | 0.75 | 0.46 | 0.44 |
| positive years | 18/24 (75 %) | **19/24 (79 %)** | 20/24 (83 %) | 17/24 (71 %) | 19/24 (79 %) |
| positive quarters | 54/102 (53 %) | **81/102 (79 %)** | 77/102 (75 %) | 60/102 (59 %) | 70/102 (69 %) |
| positive months | 159/306 (52 %) | **271/306 (89 %)** | 214/306 (70 %) | 194/306 (63 %) | 190/306 (62 %) |
| worst year | 2022 −14.49 % | 2022 −22.22 % | 2008 −16.95 % | 2022 −16.33 % | 2008 −38.04 % |

Trade level, pooled over the three index sleeves:

| | n | p | b | E | E_R | sd | p* | b* | n_req | L expected | L actual |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S2 | 918 | 0.8976 | 0.181 | 0.0599 | **+0.0321** | 0.235 | 0.8469 | 0.1141 | 214.1 | 2.99 | **2** |
| S3 | 918 | 0.6950 | 0.951 | 0.3556 | **+0.4533** | 1.377 | 0.5127 | 0.4389 | 36.9 | 5.75 | 6 |

**What that says.** S2 wins **89.8 % of months**. Its expectancy is
**+0.0321 R** per trade — real, positive, and *small*: 3.2 % of the risk unit.
It has never lost three months in a row in 24 years (longest actual streak
**2**, against a 2.99 expected by the naive formula, and `n_req = 214` says it
would take **214 trades** — nearly 18 years — to establish that mean at 2σ).

**That is the trade.** The carry stream buys *frequency*, not *return*: it turns
a 52 % monthly hit rate (S1) into an 89.8 % one, and pays for it with a CAGR of
+2.97 % against the trend sleeve's +7.07 % and buy-and-hold's +9.23 %. It also
carries a **worse** drawdown than the trend sleeve (−26.75 % vs −21.83 %) — the
losses are rare and large, which is exactly what a short-gamma profile looks
like.

### 2.2 The blend (S5) and the honest note about the blend weight

S5 = 0.75 × S1 + 0.25 × S2 (weight fixed before the run, not tuned). It lands at
CAGR **+6.16 %**, maxDD **−18.84 %** — the best drawdown of the six — and
**71 %** positive years. It does **not** clear the bar. Note what happened: the
blend improved the drawdown but *lowered* the fraction of positive years
relative to S2 alone (79 % → 71 %), because it re-introduced the trend sleeve's
monthly noise. **The 0.25 weight is a genuine degree of freedom that this study
deliberately did not explore**; a reader should not read S5's numbers as the
best a blend can do.

---

## 3. The frontier: the one number that moved

`RESULTS.md` §8, for S3, on this window:

| horizon | largest λ with 100 % positive | CAGR there | cash CAGR | excess |
|---|---|---|---|---|
| **year** | **0.0773** | +2.50 % | +1.80 % | **+0.70 %/yr** |
| quarter | 0.0008 | +1.80 % | +1.80 % | +0.01 %/yr |
| month | 0.0000 | +1.80 % | +1.80 % | +0.00 %/yr |

The sibling cross-asset **trend** book measured **λ = 0.008 → +0.03 %/yr** for
years, 0.001 for quarters, 0.000 for months.

**So the answer to the owner's question is split, and it must be reported split:**

- **"Profitable in every year"** is materially cheaper with an
  index-ETF buy-write book than with a cross-asset trend book: you may hold
  **7.7 %** of the book instead of **0.8 %**, and be paid **+0.70 %/yr** instead
  of +0.03 %. The carry stream does not *fix* the problem — you still cannot hold
  the book — but it moves the price by a factor of twenty.
- **"Profitable in every quarter or month"** is unchanged. λ ≈ 0. That part of
  the predecessor's finding is confirmed, not softened.

**Positivity by horizon**, complete periods only, strict (`> 0`):

| book | D | W | 2W | M | Q | H | Y |
|---|---|---|---|---|---|---|---|
| **S3** | 59.6 % | 64.1 % | 67.1 % | 69.9 % | 75.5 % | 78.0 % | **83.3 %** |
| S2 | 65.9 % | 70.4 % | 72.2 % | **88.6 %** | 79.4 % | 78.0 % | 79.2 % |
| S6 buy&hold | 54.1 % | 56.6 % | 59.0 % | 62.1 % | 68.6 % | 74.0 % | 79.2 % |
| S1 trend | 45.5 % | 46.3 % | 49.0 % | 52.0 % | 52.9 % | 64.0 % | 75.0 % |
| *cash* | 99.7 % | 99.9 % | 99.9 % | 100 % | 100 % | 100 % | 100 % |

Note the shape. S2 is the **best monthly** book (88.6 %) and the **worst annual**
of the three (79.2 %) — the opposite of S3, whose monthly hit rate is 69.9 % but
whose annual is 83.3 %. There is no single book that is best at every horizon.

---

## 4. Where it breaks

### 4.1 The hedge does not repair the hole. It cannot be funded.

`RESULTS.md` §9–§10. The pre-registered S4 — S2 plus one long 5 %-OTM 60-DTE
put per spread, rolled monthly — is a **net-debit** strategy:

- the tail put costs **4.66× the spread credit** (median 3.65×, min 0.34×,
  max 24.92×);
- the structure's mean monthly cash flow is **−$214.27 per spread**, i.e.
  **−5.27 % of the sleeve's risk budget per month**;
- and, structurally, in **584 of 915 months (64 %)** the 5 %-OTM put strikes
  **above** the spread's short strike (mean offset **−1.08 %** of spot). When
  that happens the structure is not a credit spread plus a tail hedge at all —
  it is a **net long put** whose maximum loss is the net debit.

The reason is arithmetic, not luck: a **16-delta 30-DTE put on SPY is usually
further out than 5 %**, and a $5-wide 30-DTE spread collects about **11 % of its
width** in premium. **A 16-delta/$5-wide/30-DTE spread cannot buy a 5 %-OTM
60-DTE put.** "Paid for by the premium" is false by a factor of about four.

### 4.2 What the hedge *does* do, when you size it to the premium

`S4c` — a disclosed variant, not the pre-registration: the long put's quantity
is set so its debit **equals** the credit (fractional contracts; a stated
simplification). Measured:

| | S2 | S4 (literal) | **S4c (credit-funded)** |
|---|---|---|---|
| CAGR | +2.97 % | −14.84 % | **+0.25 %** |
| maxDD | −26.75 % | −98.45 % | −25.56 % |
| positive years | 79 % | 12 % | 75 % |
| E_R | +0.0321 | −0.1865 | +0.0050 |
| 2008 window, option sleeves | **−11.97 %** | +9.59 % | **−5.63 %** |
| 2020 window, option sleeves | −1.09 % | **−36.24 %** | **+0.07 %** |

**Answer:** an *affordable* hedge **halves the 2008 damage** (−11.97 % →
−5.63 % of the risk budget) and **turns 2020 positive** (−1.09 % → +0.07 %), and
it costs **2.72 percentage points of CAGR** — nearly the whole edge — plus
4 points of positive years. The literal S4 does the opposite of what it looks
like it does in 2020: it pays **−36.24 %** because its hedge's *cost* dominates a
year without a sustained crash, while in 2008 it earns **+9.59 %**.

So: **the hedge repairs the tail and destroys the carry.** Both readings are in
`RESULTS.md`; neither is a recommendation.

### 4.3 The stress cells, in full

| window | S1 | S2 | S3 | S4 | S5 | S6 |
|---|---|---|---|---|---|---|
| **2008 GFC** window total | −9.21 % | −11.97 % | −19.01 % | +9.59 % | −9.74 % | −43.82 % |
| 2008 maxDD | −9.21 % | −21.36 % | −28.08 % | −16.95 % | −12.24 % | −52.89 % |
| option P&L, 2008 (3 sleeves, $) | — | **−1 796** | — | **+1 954** | — | — |
| S2 worst 2008 trade | — | **−1.015 R**, entering **2008-09-02** | — | — | — | — |
| **2020 COVID** window total | +20.08 % | −1.09 % | +23.42 % | −36.24 % | +14.68 % | +30.45 % |
| 2020 maxDD | −18.48 % | −15.87 % | −20.13 % | −69.26 % | −17.59 % | −33.41 % |
| option P&L, 2020 (3 sleeves, $) | — | **+95** | — | **−3 402** | — | — |
| S2 worst 2020 trade | — | **−1.015 R**, entering **2020-02-03** | — | — | — | — |

**Two things worth saying plainly.**

**The premium seller's breaks are small and bounded.** The worst S2 trade in
either crisis is **−1.015 R** — the defined-risk structure did its job. Five of
36 trades in 2020 and 12 of 45 in 2008 lost money; the 2008 window cost
**−11.97 %** of the risk budget, which is **less than a quarter** of what
buy-and-hold lost in the same window (−43.82 % window, −52.89 % drawdown). The
$5-wide, 16-delta, 30-DTE put spread is a *far* OTM structure on a $244–770
index ETF and 2008/2020 simply did not reach it often.

**This is a caution, not a comfort.** The measured break is small *because the
structure is small*, and because the 21–30 day tenor rolled through both crises
rather than sitting through them. It says nothing about what happens if the
short strike is hit — the model would show a −1.0 R month, but it would also
show that the *real* instrument can be **assigned early** (these are American
options), which this model cannot represent.

### 4.4 The VRP is real here too, and reproduces the sibling exactly

`RESULTS.md` §11, same arithmetic as
`../../options-trading-playbook/examples/regime-study`:

| | this study | sibling's published finding |
|---|---|---|
| mean VRP, full history | **+3.64** vol pts | +3.62 |
| share of windows VIX > forward 21-day realised vol | **83.0 %** | 82.9 % |
| 2008 mean VRP | **−2.33** vol pts | −2.33 (the only negative year) |
| 2020 fair-strike total | **−7.3 R** | −7.3R (the only losing year) |
| worst window | **2020-02-20**, VIX 15.6, realised \|move\| 32.10 %, **R_fair = −3.98** | −3.98 starting 2020-02-20, VIX 15.6, realised 32.1 % |

**Sign, size and the two named years all match.** The predecessor's VRP result
is confirmed on an independently pulled series with independently written code
(`handcheck.py` reproduces it too, in `handcheck-output.txt` §D). This is the
part of the study that is *not* a model: the gap between implied and subsequently
realised vol is measured on real prices, and it is not in dispute.

---

## 5. What it costs, and the assumptions the answer depends on

The verdict matrix (`RESULTS.md` §15), read straight from the sensitivity
tables:

| assumption | S2 | S3 |
|---|---|---|
| costs **FREE** | **CLEARS** (+4.54 %, 83 %/80 %) | CLEARS |
| costs **LOW** (headline) | fails (+2.97 %, **79 %**/79 %) | CLEARS |
| costs **HIGH** | fails (+1.74 %, 75 %/78 %) | CLEARS |
| IV × 0.8 | fails (−1.46 %, 67 %, maxDD −47.28 %) | fails (−39.25 % maxDD) |
| IV × 1.0 | fails | **CLEARS** |
| IV × 1.2 | **CLEARS** (+6.96 %, 88 %/87 %) | CLEARS |
| term structure `sqrt(30/D)` | fails | CLEARS |
| **no VIX lag** | fails (+2.94 %) | CLEARS |
| dividends at published averages | fails (+3.23 %) | CLEARS |
| **sold leg −1.5 vol pts (skew)** | fails (−0.87 %, 67 %, maxDD **−45.72 %**) | **CLEARS** (+10.11 %) |
| **sold leg −3.0 vol pts (skew)** | fails (−4.03 %, 54 %) | **fails** (+9.65 %, 79 %) |

Three readings:

**Costs.** S2's CAGR drag is **−1.56 pp at LOW** and **−2.79 pp at HIGH**; S3's
is **−0.06 pp and −0.10 pp**. The reason is arithmetic: S2's premium is
**$0.49 per share** on a structure whose risk unit is **$4.51**, so a $6.30
round-trip on two legs is **1.40 % of R per trade**, and there are twelve trades
a year. S3's single-leg roll costs **$3.15 against a ~$4.50 credit** — which
sounds worse, but S3's *returns* are dominated by the long underlying, so the
same dollar cost is a fifth of the percentage drag. **A premium-selling edge that
clears the bar only at zero cost is not an edge you can run.**

**Skew — the big one.** One implied vol prices every strike in this model, so the
sold leg is priced at the same vol as the wings. A 30-delta 30-DTE call has
roughly **$24 of vega per vol point per contract** at a $244 spot; 1.5 vol points
is **$36 per contract per month**, which on a single covered-call sleeve is about
**1.8 percentage points of annual return — the same order as the entire edge.**
Measured: **S2 goes from +2.97 % to −0.87 %**, its drawdown from −26.75 % to
**−45.72 %**, and its positive years from 79 % to 67 %. **S3 survives 1.5 vol
points (+10.11 %) and dies at 3.0 (+9.65 %, 79 %).** Since real index-option skew
at the 30-delta strike is real and one-directional, **the honest reading is that
this is the single most likely reason the S2 result would not survive contact
with actual quotes.**

**IV level.** S2 swings from −1.46 % at IV × 0.8 to +6.96 % at IV × 1.2. The
sign of the whole result is set by an input the model cannot verify. That is the
most important sentence in this document.

**A genuine negative result: dividends.** The price series carries no dividends,
so the modelled call is too expensive — which should *flatter* S3 and, in the
opposite direction, *hurt* S2 (whose long wing is a bought put). Re-running with
published average yields held constant over 25 years moves **S3 by −0.08 pp** and
**S2 by +0.26 pp**. The reason is that moving to a dividend-aware price **also
moves the delta-targeted strike**: the same-delta call is written at a lower
strike and its price barely changes. **The missing-dividend bias is therefore NOT
the explanation for either result** — which is not what one would guess, and is
worth recording.

---

## 6. The three indices are nearly one bet

Measured on this window, 24 complete years (yearly) and 6 435 daily pairs:

| pair | yearly corr | daily corr | R² yearly |
|---|---|---|---|
| SPY / QQQ | **0.917** | 0.884 | 0.841 |
| SPY / IWM | **0.895** | 0.887 | 0.801 |
| QQQ / IWM | **0.840** | 0.793 | 0.705 |

Mean pairwise yearly correlation **0.884**. The brief predicted 0.85–0.95 and the
measurement lands inside it.

**A three-index book of SPY/QQQ/IWM is not three bets.** It is one broad-market
bet taken at three slightly different tilts — a mega-cap-growth tilt (QQQ) and a
small-cap tilt (IWM) wrapped around the market (SPY). Adding QQQ and IWM to SPY
buys almost no diversification; it buys a slightly different beta. Every
diversification claim in `RESULTS.md` should be read with this in mind: S3's
"three sleeves" are one bet, and S2's "three premium streams" are one short-vol
position taken three times.

---

## 7. The longest window, for comparison

`RESULTS.md` §14. SPY only, 1993-11-11 … 2026-10-14 (8 285 sessions, **32
complete years**, cash CAGR +2.52 %) — this window contains the whole dot-com
bear as well as 2008:

| | S1 | S2 | S3 | S4 | S5 | S6 |
|---|---|---|---|---|---|---|
| CAGR | +6.86 % | +2.82 % | +10.12 % | −14.46 % | +5.97 % | +8.91 % |
| maxDD | −28.15 % | −32.57 % | −23.72 % | −99.44 % | −23.33 % | −56.47 % |
| positive years | 66 % | **81 %** | 81 % | 19 % | 69 % | 72 % |
| positive quarters | 60 % | 81 % | 76 % | 27 % | 66 % | 71 % |
| positive months | 53 % | **91 %** | 70 % | 30 % | 66 % | 63 % |

The pattern holds over 32 years and through the dot-com crash: the premium stream
keeps its hit rate (**81 % of years, 91 % of months**) and keeps its thin return
(+2.82 % vs cash +2.52 % — a **+0.30 pp** excess, thinner than on the three-index
window), with a **−32.57 %** drawdown. The buy-write keeps its CAGR and its
positive years. **The S1/S2/S3 shape is stable across two windows that share
almost nothing except 2008 and 2020 — that is the strongest single piece of
evidence in this study.**

---

## 8. What the model cannot see — the reader's checklist

Full list in [`README.md`](README.md) §2. In order of how much they could move
the answer:

1. **Skew.** One vol prices every strike. §5 above measures the effect at 1.5 and
   3.0 vol points; it is larger than the edge.
2. **No observed quotes at all.** No bid/ask in the price, no liquidity limit, no
   partial fill, no legging risk, always fillable at the modelled mid.
3. **European pricing of American, physically settled contracts.** No early
   exercise, no assignment, no pin risk.
4. **No term structure** in the primary run. S4's viability **flips sign**
   between `alpha = 0` (−14.84 %) and `alpha = 0.5` (**+15.91 %**, 100 % positive
   years). The model has no data to choose between them.
5. **The IV *level*.** S2 goes from −1.46 % to +6.96 % across IV × 0.8 … × 1.2.
6. **Dividends** (measured: small here — see §5).
7. **The sleeve's risk budget.** Both premium sleeves report *dollar P&L on a
   fixed risk budget of 10 spread-widths*. Changing that constant rescales the
   premium stream inside S5 but does not change S2's or S3's own sign pattern.
8. **Margin, buying power, tax, and the practical cost of rolling 3 legs a month
   for 25 years.**

**One more, and it is a real one:** the premium sleeves were simulated as
**always one spread per index per month**, in all 306 months, including the
months when VIX was at 60 and the credit was fat. That is a fixed rule, not a
vol-timed one, which is what the pre-registration demanded — but it means this
study **cannot say** whether timing the premium (sell more when VIX is high)
would help. See §9.

---

## 9. What remains untested

- **Parameter sensitivity is untested by design.** SMA(200), the 16-delta short,
  the $5 width, the 30-DTE tenor, the 30-delta call, the 5 %/60-DTE hedge, the
  0.25 blend weight and the 10× risk budget were all fixed before the run.
  Nothing here shows any of them is optimal, or rules out a better choice.
- **The width is a genuinely ambiguous pre-registration.** A literal **$5** is
  **2.92 % of spot on SPY** but **7.35 % on QQQ** and **5.63 % on IWM** on
  average, and in 2001 it was **12.8 % of QQQ's spot**. The resulting long wing
  is at **−0.063 delta on SPY's first trade but −0.005 on IWM's** — a nearly
  worthless wing. A width normalised to a percentage of spot is a different
  study, and it is not this one.
- **Premium timing is untested.** The carry stream runs unconditionally every
  month. A vol-conditional version (sell only when VIX is above its median) is
  the obvious next experiment and could move both S2 and the S5 blend.
- **Strike selection by delta is untested** against selection by fixed
  percentage OTM.
- **The hedge was tested at exactly one shape** (5 % OTM, 60 DTE, linear). A
  put-spread hedge, a ratio hedge, a VIX-call hedge, or a *conditional* hedge
  (only when VIX is low) are all absent. Given §4.1's finding — the hedge cannot
  be funded by a 16-delta spread — the interesting question is a *wider* spread
  whose credit could fund a real tail, and that is a different pre-registration.
- **The short side is untested.** λ ≤ 1 only; no shorting, no leverage, no
  funding.
- **"Every period" is a statement about a finite sample:** 24 years, 102
  quarters, 306 months. **83 % of years positive is a statement about 24
  periods.** It is not a guarantee and it is not out-of-sample.
- **No walk-forward, no train/test split.** The parameters were fixed by
  judgement, not fitted, but the *stories* in this document were written after
  the numbers arrived, and a reader should treat them as such.

---

## 10. The answer, stated once

**Can a SPY/QQQ/IWM book that trades both the underlying and options on it be
"profitable in most conditions"?**

- **In most years: yes, at 83 % — with the buy-write, and it costs −28.74 % of
  drawdown to get there.** For a book with *options only*, the year-fraction tops
  out at 79 %. And you still cannot hold the book: **7.7 %** exposure is the most
  that keeps every year positive, earning **+0.70 %/yr** over cash.
- **In most quarters: barely.** 75 % at best (S3), 79 % from the premium stream
  alone but with a 79 % year record. The 100 %-positive-quarter frontier is
  **λ = 0.0008**.
- **In most months: yes for the premium stream (88.6 %), no for anything that
  earns a return.** S2's 89.8 % monthly hit rate is the best number in the study
  and it comes with a +2.97 % CAGR.
- **In every month: no, and not close.** λ = 0.0000.

**And the cost of the answer is that it is not robust.** The one book that clears
the bar stops clearing when the sold leg loses **3 vol points** to skew. The
premium stream never clears once you charge a real spread or take **1.5 vol
points** of skew. Nothing here would justify a position; the study's value is
that it says exactly which assumptions the answer rests on.
