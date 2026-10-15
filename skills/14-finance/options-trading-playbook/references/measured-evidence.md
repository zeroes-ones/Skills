# Measured Evidence — What Four Studies Actually Found

This file exists so the numbers do not stay inside the study output. Four studies were run under
`examples/`; each has a `README.md` (model, inputs and *stated limitations*), a `FINDINGS.md`
(the narrative) and a `RESULTS.md` (every table verbatim). This reference records **what each study
measured, with the number and the path it came from**, so a decision can be made against it instead of
against a memory of it.

**Every figure here is a study result, not a market fact.** Each one carries a tag:

| tag | means |
|---|---|
| `[MODELED]` | simulated. The option prices in `leg-count-test`, `tenor-test` and `index-options-test` are built from the **real VIX** with Black-Scholes and settled against **real index closes**. There are no historical option quotes anywhere in these studies. |
| `[COMPUTED]` | arithmetic or an identity from the algebra, shown inline. |
| `[ESTIMATED]` | a desk choice or an uncertain input. |

**No figure in this file is a profit claim, and none of them should be read as one.** Several are
explicitly *negative* results — including the two most useful ones (legs and tenor buy shape, not edge).
Where a modelled result clears a bar only under one cost or skew assumption, that is stated beside the
number.

---

## 1. Legs buy shape, not edge — `examples/leg-count-test/`

`[MODELED]` Window 2001-03-13 … 2026-10-14; 6 436 sessions; 24 complete years; 306 complete months.
12 pre-registered structures × 7 variants × 3 indexes = **252 sleeves, 11 016 trades**.

- **`E_net` is not monotone in leg count on any of the three views.** Ordered by legs, the measured
  `E_net` is `+0.0181 → +0.2045 → +0.0602 → −0.1116` for the range view; `−0.4546 → +0.0525 → −0.2384 →
  −0.0012` for the directional view; `+0.0023 → +0.0081 → +0.0109 → +0.0181` for the carry view. Adding
  legs does not add edge in any of the three. `[MODELED]`
- **A 4-leg structure beat its 1-/2-leg comparator in 1 of the 4 comparisons that exist.** The one win
  is the condor (A2, 4 legs, `+0.0602`) against the put spread (A1, 2 legs, `+0.0181`) — a margin of
  **+0.0421R**. `[MODELED]`
- **That single win flips negative under the conservative skew direction.** With the sold leg priced
  1.5 vol points lower (`SKEW_SOLD_M15` — the direction both this library and the sibling study take,
  because a real seller of an OTM option collects less than the flat-vol value), **A2 = −0.0229** and
  **A1 = −0.0192**: the 4-leg structure becomes *worse* than the 2-leg one it beat. The condor's whole
  advantage over the put spread lives inside the skew assumption. `[MODELED]`
- **Skew sensitivity rises with the number of strikes touched.** `Pearson(|ΔE| in dollars, leg count)
  = 0.75` and `Pearson(|ΔE| in dollars, distinct option strikes) = 0.75` (`0.66` in `R` units). The two
  4-leg structures are the two most skew-sensitive on every measure (`$190.68` and `$55.06` per trade
  against `$35.13` for the best 2-leg), and the swing on the iron fly is **1.47R on a 1.5-vol-point
  move**. The count of legs does not *determine* skew sensitivity, but the structures with the most legs
  have the most. `[MODELED]`
- **No 4-leg structure survives the conservative skew direction in any view.** `[MODELED]`

The honest summary: legs buy a balanced payoff (net delta 10.7 → −0.1), a smaller crash-year tail
(2008: −1.3R → −0.3R) and a flatter positivity profile across horizons — and they cost a doubled
per-leg fee, more skew dependence, and (on the iron fly) a terminal max loss so small that it no longer
normalises anything.

## 2. Tenor buys a clock, not edge — `examples/tenor-test/`

`[MODELED]` Same window and carry as above. **7 structures × 9 tenors = 63 cells per index × 3 indexes =
189 sleeves × 3 variants = 567 simulated sleeves.** The grid is pre-registered and asserted at run time.
**0DTE is not one of the 63.**

- **`E_net` is not monotone in tenor for 6 of the 7 structures.** The single monotone structure is the
  covered call, and it is monotone because it is long the realised equity risk premium — a property of
  the holding window, not of the option. `[MODELED]`
- **The only interior `E_net` peaks are at 180 DTE — for both real premium sellers.** Short put spread
  `+0.1277` at 180 DTE (vs `+0.0172` at 7 and `+0.0964` at 730); iron condor `+0.1979` at 180 DTE (vs
  `+0.0403` at 7 and `−0.0910` at 730). Every other structure peaks at an endpoint (7 or 730 DTE), i.e.
  at a boundary of the grid. `[MODELED]`
- **`theta-per-day ÷ R` is exactly `−1/D` for fully-debit structures.** The long call and the debit
  spread print `−1/7, −1/14, −1/30 … −1/730` to the printed precision: a position that spends its whole
  `R` on premium bleeds `1/D` of its own maximum loss every calendar day. **This is an identity, not a
  measurement** — their credit *is* `−1 × R`. The measured ratio is `104.3×` between 7 and 730 DTE for
  those two, and `6.8×` (cash-secured put) to `33.8×` (iron condor) for the others: short tenor is paid
  more per calendar day in every structure, and that is the whole of the "tenor edge". `[COMPUTED]`
  for the identity; `[MODELED]` for the ratios.
- **Skew dependence rises 3–4× with tenor.** Mean `max|ΔE|` by bucket: weeklies `0.133` → gamma
  shoulder `0.133` → monthlies `0.229` → quarterlies `0.511` → annuals `0.416` → LEAPS `0.439` `R`
  units. Under the conservative direction the premium-selling edge at the long end is wiped out: the
  short put spread's `E_net` runs `−0.0020` (7 DTE) … `+0.0257` (180) … `−0.0642` (730), and the condor
  reaches `−0.3346` at 730 DTE. `[MODELED]`
- **16 of 63 cells are unmeasurable** (an `E` indistinguishable from zero at two sigma), and **4 of the
  7 LEAPS cells** — 57% of that column is not a result. Per structure the measurable tenor count is
  S1 4/9, S2 6/9, S3 8/9, S4 9/9, S5 9/9, S6 8/9, S7 3/9. Unmeasurable cells are printed and flagged,
  never used as a verdict. `[MODELED]`
- **Long tenor did NOT buy crash protection.** In the 2008 window the iron condor earned `+1.06R` at
  7 DTE against `−1.04R` at 730 DTE; in the 2020 window it earned `+3.75R` at 7 DTE against
  `−0.62R` at 730 DTE, and the iron butterfly `+16.74R` against `−0.60R`. **7 DTE beat the long tenors in
  both crises**, because a short-dated spread re-written through a crash keeps re-marking to the new
  level while a long-dated one sits through it. The long bucket buys a shallower drawdown and a cheaper
  ticket per unit of `R`; it does not buy the tail. `[MODELED]`

**Note on the owning skill's own labels.** This study found that `monthlies 21–60` and
`quarterlies 60–120` overlapped at exactly 60 DTE, with two roll windows (21–30 vs 60–75) and two hard
deadlines (21 vs 45 DTE). That ambiguity has since been fixed in `options-risk-engineer`
(`dte-close-roll-calendar.md` §2): monthlies are **21–59**, quarterlies **60–120**, and 60 DTE resolves
to quarterlies. This study assigns 60 → quarterlies, which now matches.

## 3. Cost — `examples/leg-count-test/`, `examples/tenor-test/`, `examples/index-options-test/`

- **Cost scales linearly in legs at fixed `R`; `R` does not scale with legs.** One-leg cost
  `$3.15`/trade, two-leg `$6.30`, four-leg `$12.60` at the LOW schedule (a round trip = two tickets per
  leg, which doubles each figure). At the same ticket convention, **a 4-leg structure costs 4× a 1-leg
  and 2× a 2-leg** — so the leg-count cost premium is roughly **2–4×** against a low-leg-count
  structure, and it is the linear-in-legs term, not the fee level, that carries it. `[MODELED]`
- **`c_R` consumes the edge exactly where `R` is small.** The iron fly's `c_R/E_R` is `5.120` at LOW
  and `9.183` at HIGH, and the reason is that its `R` is one third of the others': a 5-wide iron fly has
  a terminal max loss of **1.17% of notional**. It is the only structure in the study whose cost exceeds
  its edge. No leg count destroys the others. `[MODELED]`
- **Round-trip vs one-ticket-per-leg is what decides the range view.** Between LOW and round-trip
  prices, **A2 goes `+0.0602 → −0.0023`** and A1 `+0.0181 → −0.0099`. If you close the structure early
  instead of letting it expire — which is what the popular management cards say to do — the extra legs'
  cost is enough to flip the whole view negative. **The leg-count cost finding is not the fee level; it
  is whether you pay one ticket or two per leg.** `[MODELED]`
- **Cost and outcome are essentially uncorrelated in the directional view.** The structures that lose
  money lose it on the payoff, not on the fee: the structure with the smallest `c_R` in that view is not
  the best, and the one with the largest is not the worst. `[MODELED]`
- **The buy-write clears its pre-registered bar only at zero cost.** `examples/index-options-test/`:
  the three-index buy-write is positive in **83% of years / 80% of quarters at FREE costs** (+4.54%
  CAGR), **79% / 79% at LOW**, and **75% / 78% at HIGH**. `[MODELED]`
  The premium-selling stream alone shows the same shape more harshly: its CAGR drag is **−1.56 pp at
  LOW and −2.79 pp at HIGH**, because its premium is `$0.49` per share against a `$4.51` risk unit, so a
  `$6.30` two-leg round trip is **1.40% of `R` per trade** and there are twelve trades a year. **A
  premium-selling result that clears the bar only at zero cost is not a result you can run.** `[MODELED]`

## 4. The variance risk premium is real — harvesting it is modelled and fragile

`examples/regime-study/` and `examples/index-options-test/`

**The VRP itself is measured on real prices, not modelled:**

- VIX exceeded the realised 21-day move that followed in **82.9%** of windows, with a mean VRP of
  **+3.62 vol points**. It was negative in **exactly one calendar year of 34: 2008 (−2.33 vol points)**.
  `examples/regime-study/FINDINGS.md` `[COMPUTED]` on real VIX and real index closes.
- The index-options study reproduced this on an independently pulled series with independently written
  code: mean **+3.64**, share **83.0%**, 2008 **−2.33** — sign, size and the named year all match.
  `examples/index-options-test/FINDINGS.md` §4.4 `[COMPUTED]`.
- The same study names the worst window: starting 2020-02-20 with VIX at 15.6, the realised move was
  32.10% and the fair strike was `−3.98R`. `[COMPUTED]`

**Harvesting it is where the modelling starts, and where it becomes fragile.** `[MODELED]`

- The modelled premium-selling stream returns **+2.97% CAGR** with **89% of months** positive and
  **79% of years** (max drawdown `−26.75%`, Sharpe 0.18 against cash). It misses the pre-registered 80%
  year bar by a single year of 24. `examples/index-options-test/` `[MODELED]`
- **The skew assumption is the single most likely reason it would not survive contact with real
  quotes.** Sold strikes priced **1.5 vol points lower** move the stream from **+2.97% to −0.87%**, its
  drawdown from `−26.75%` to **`−45.72%`**, and its positive years from 79% to 67%. `[MODELED]`
- The modelled buy-write returns **+10.53% CAGR**, positive in **83% of years / 75% of quarters / 70% of
  months**, max drawdown `−28.74%`. It survives 1.5 vol points and fails at 3.0. `[MODELED]`

**Read this section as: the premium is real, the harvest is a model.** The measured part is the gap
between implied and subsequently realised vol. Every "and therefore you earn X" figure above is
`[MODELED]`, and the model has one implied vol for every strike — i.e. **no skew at all**, which is
precisely the assumption the sensitivity table breaks under.

## 5. 0DTE cannot be backtested from daily bars — `examples/tenor-test/`

**This is a refusal, not a result.** 0DTE is not one of the study's 63 cells: a daily bar carries no
intraday path, and 0DTE P&L *is* the path. What can be stated are the analytic facts and the
study's own labelling rules. `[COMPUTED]` unless marked otherwise.

- **`Γ ∝ 1/√T`.** The study's own pricer returns **10.959×** for the 30 DTE → 0.25 DTE gamma ratio
  against the derived **10.954×** (`√(30/0.25) = √120`) — the ladder the sibling risk skill publishes,
  reproduced exactly. `[COMPUTED]`
- **`theta-per-day ÷ R` is `1/D` for a fully-debit structure** — the identity from §2 above, which reads
  `3.33%` of `R` per calendar day at 30 DTE and `14.29%` at 7 DTE. `[COMPUTED]`
- **Decay as a fraction of the *premium* scales as `1/T`, not `1/√T`.** The same `1/√T` multiplies the
  daily decay in dollars and the position's value at once, so the ratio runs **1.67% per day at 30 DTE
  against 200% per day at 0.25 DTE — a 120× ratio**. Note the denominator: this is decay÷*premium*,
  which is a different quantity from decay÷`R` in the bullet above, and the two must not be mixed.
  `[COMPUTED]`
- **A ticket costs the same against a near-zero credit, so `c_R` is worst at 0DTE.** At the headline LOW
  setting a two-leg ticket is `2 × ($0.65 + $0.025 × 100) = $6.30`; against a **$0.05** credit that is
  **126% of the entire premium** (226% at HIGH), falling to **32% (56%)** against a $0.20 credit. Cost
  as a share of *premium* and cost as a share of *`R`* answer different questions and both are printed.
  `[MODELED]`
- **The widely quoted "0DTE = 59% of SPX volume" figure must not be charted.** It sits on a vendor
  marketing page with **no as-of date**. The study refuses to report any 0DTE share-of-volume number,
  dated or not, and cites `trading-decision-data-catalogue` (`SKILL.md`, and
  `references/options-positioning-data.md` §3.1) for the rule: an undated market-share statistic is not
  a statistic. `[ESTIMATED — undated vendor marketing page]`
- The one 0DTE section in the study output is labelled `[ILLUSTRATIVE]`, enters at the session open,
  settles at the close, and **cannot be extrapolated**: no intraday stop, no intraday mark, no path, and
  its own 0.25-DTE credit is an artefact of flat-vol pricing. Nothing in it may be scaled or annualised.

## 6. What these numbers are not

1. **Not market data.** The three option studies have no historical quotes. Their prices are
   Black-Scholes on the real VIX, settled on real index closes. Every option figure here is `[MODELED]`.
2. **Not profitability evidence.** `index-options-test` documents one modelled book clearing a
   pre-registered bar and failing it at LOW costs; `leg-count-test` and `tenor-test` report no
   profitability claim at all, and their headline findings are *negative* (legs and tenor buy shape, not
   edge).
3. **Not survivorship-free or window-free.** 24–34 complete years is enough to see a tail and not enough
   to settle anything; the 730-DTE cells have as few as 36 trades.
4. **Limitations are stated in each study's own `README.md`**, not only here — read
   `examples/leg-count-test/README.md`, `examples/tenor-test/README.md`,
   `examples/index-options-test/README.md` and `examples/regime-study/README.md` before acting on any
   number, and `FINDINGS.md` for the study's own statement of what it refuses to conclude.
5. **This skill's own arithmetic is elsewhere.** `references/cost-drag-per-leg-and-per-rung.md`,
   `references/payoff-corners-for-options.md` and `references/what-this-cannot-promise.md` hold the
   identities and their guards; this file holds *results*, and a result is only as good as the model
   that produced it.
