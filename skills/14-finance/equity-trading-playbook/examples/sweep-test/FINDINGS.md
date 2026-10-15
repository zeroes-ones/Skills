# FINDINGS — what the sweep said, and what it refuses to say

This is the honest narrative. `RESULTS.md` holds every table verbatim from a real
run; this file holds the interpretation, the losses, and the list of things that
were **not** tested. Where a number is quoted here it comes from
`run-output.txt`.

---

## 1. The instruction, and why it is the wrong instruction

The desk owner's instruction was *"run as many iterations as you want to show
+ve numbers"*. The sweep executed it literally and then measured what it bought:

| over the 1,620 configurations of Grid P | result |
|---|---|
| configurations with a positive full-window CAGR | **1,599 (98.7%)** |
| configurations with a positive full-window Sharpe | **1,613 (99.6%)** |
| median configuration's Sharpe | 0.5129 |
| configurations that clear the Bonferroni bar for m = 1,620 | **10 (0.62%)** |
| configurations positive in **every** complete year | **0** |

The instruction works. It is also empty. A sweep this wide does not *find* a
positive result — it *manufactures* one, and the median member of the grid would
have been publishable under any conventional significance test (median `t` is
**2.343**, comfortably past the unadjusted 1.96). The rest of this file sizes that
effect instead of exploiting it.

---

## 2. What was fixed before the first number

| element | status |
|---|---|
| the signal (close vs SMA(N), long above / flat below) | **pre-registered** |
| N = 50, 100, 150, 200, 250 | **pre-registered** |
| the universe and every 2-, 3-, 4-instrument equal-weight subset of it | **pre-registered** |
| daily and monthly rebalance, one-session execution lag | **pre-registered** |
| the metric set (CAGR, maxDD, Sharpe, worst year, period positivity, regime cells) | **pre-registered** |
| the Bonferroni family (= every configuration in the grid) and alpha = 0.05 | **pre-registered** |
| the 70/30 time split and "rank by in-sample Sharpe, evaluate the top decile once" | **pre-registered** |
| the pre-registered default (SPY+QQQ+IWM+EEM, N=200, monthly) | **pre-registered** |
| the grids L and X (other universes, other windows) | **pre-registered** |

Nothing in §3–§8 was tuned, and no configuration was re-run after its result was
seen. The grid count printed in `SECTION 1` is asserted against the number of
records actually produced in `SECTION 1c` (`Grid P: declared 1620, run 1620 -> OK`),
and `handcheck.py` re-enumerates the grid independently by recursion.

One **implementation** defect in the regime series was found and fixed after the
first full run, without changing the regime *definition* (still SPY's trend state
against SPY's SMA(200), against SPY's realised-vol tercile). It is recorded in
§12; it changed the regime tables and nothing else. Every headline number, and
every out-of-sample number, is identical before and after.

---

## 3. What a grid this size produces by construction

Grid P, full window (2005-11-14 .. 2026-10-14, 5,261 sessions, 20.91 years):

| metric | best | p90 | median | p10 | worst |
|---|---|---|---|---|---|
| CAGR | 12.00% | 7.24% | 4.70% | 2.22% | −2.49% |
| Sharpe | 1.0060 | 0.7259 | 0.5129 | 0.2729 | −0.0892 |
| max drawdown | −10.22% | −14.78% | −20.90% | −31.78% | −68.25% |
| worst year | −3.63% | −7.08% | −11.63% | −18.58% | −48.30% |
| positive-year fraction | 90.00% | 80.00% | 70.00% | 55.00% | 30.00% |
| positive-quarter fraction | 74.70% | 66.27% | 57.83% | 49.40% | 26.51% |

**The p10 configuration is still up 2.22% a year.** In a grid where nine in ten
members are profitable and the tenth-percentile member is profitable too, a
green row is not evidence of anything. The only columns that carry information
are the tails — and the tail is where the losing configurations live
(CAGR −2.49%, Sharpe −0.0892, drawdown −68.25%, a −48.30% year). Those are the
configurations a report built from "the best of N" never shows you.

The in-sample half of the same table (first 70% of sessions) looks the same
shape with a slightly lower median (Sharpe 0.4626, CAGR 4.31%), which is the
point of §5.

---

## 4. The Bonferroni answer, and what the survivors have in common

```
m = 1,620 configurations           alpha = 0.05 two-sided
per-test alpha = 0.0000308642
critical |t|   = 4.1670            (the unadjusted 2-sigma mark is 1.9600)
```

| t across the grid | min | p10 | median | p90 | max |
|---|---|---|---|---|---|
| raw n | −0.4075 | 1.2468 | 2.3431 | 3.3162 | 4.5962 |

**10 of 1,620 configurations clear the bar.** With the stricter
autocorrelation-adjusted statistic the count is 17 — so the honest answer to
"how many are genuinely positive rather than positive by selection" is **ten,
at most, out of 1,620**, and that is under a null the test does not really
deserve (see below).

**The ten cluster, and that is the finding.** If ten survivors were a real
effect they would be spread across the universe. They are not:

| the ten survivors contain... | survivors | configs in the grid containing it |
|---|---|---|
| GLD | **10 of 10** | 640 of 1,620 |
| QQQ | 9 of 10 | 640 of 1,620 |
| SPY | 5 of 10 | 640 of 1,620 |
| TLT | 2 of 10 | 640 of 1,620 |
| IWM, EEM, EFA, VNQ | **0 of 10 each** | 640 of 1,620 each |

`N=150` supplies 6 of the 10; `N=50` and `N=100` supply none. If the ten had been
drawn at random from the grid, the chance that every one of them contained gold
would be about `(640/1620)^10 ≈ 9 × 10^-5`. They are not random. **The search
found "hold gold and the Nasdaq", which is a bet on two assets over one
particular window — not a rule that repeats.**

Two things make the count of ten *generous*, and both are worth stating because a
reader will otherwise read it as ten independent discoveries:

1. **The null is not interesting.** `t` here tests whether the mean daily return
   is zero. A long-or-flat sleeve on an asset that rose inherits that drift with
   no skill at all: **SPY is above its own SMA(200) on 77.9% of this window's
   sessions**, so a sleeve that follows it is long most of the time and picks up
   most of the market's rise. The Bonferroni correction makes the *family-wise*
   statement honest; it does not make the underlying null a test of skill.
2. **The sample-size correction cuts the other way.** Daily returns of these trend
   books are **negatively** autocorrelated at lag 1 (median `rho1 = −0.0446`), so
   `n_eff` is *larger* than the day count (it exceeds 5,260 for 1,569 of the 1,620
   configurations) and the adjusted count **rises** from 10 to **17** rather than
   falling. So the adjustment here is lenient, not conservative, and that is a
   property of the data rather than of the test. Neither number should be taken as
   settled. What *is* settled is that **99.4% of the grid cannot be distinguished
   from noise at the family-wise level.**

---

## 5. Out-of-sample: this split flatters the selection, and says so

Split: in-sample 2005-11-14 .. 2020-07-01, held out 2020-07-02 .. 2026-10-14.
Ranked by in-sample Sharpe, the top decile is 162 configurations, evaluated once.

| top-decile metric | median | q25 | q75 | p10 |
|---|---|---|---|---|
| Sharpe degradation (OOS − IS) | **+0.0642** | −0.0986 | +0.2035 | −0.2743 |
| CAGR degradation (OOS − IS) | **+1.01%** | −0.57% | +3.00% | −2.14% |

**The median top-decile configuration did BETTER out of sample.** Taken alone that
looks like the edge survived. It did not, and the reason is visible three lines
later in the same run:

| | in-sample | held out |
|---|---|---|
| all 1,620 configurations, median Sharpe | 0.4626 | 0.6185 |
| all 1,620 configurations, median CAGR | 4.31% | 5.94% |
| plain SPY trend sleeve (N=200 monthly), Sharpe / CAGR | 0.6800 / 7.76% | 0.8011 / 9.73% |

**Everything improved out of sample, including the whole grid and a single
instrument with no selection on it at all.** The held-out window is a rising
market; for a long-or-flat strategy that is the kinder half of the sample.
Degradation measured on this split is therefore a **lower bound** on how badly
the selection decays — the true decay would only show up in a holdout that
contained a bad decade.

So the honest test is not "did the Sharpe hold up" but **"did the search's
advantage over a no-search benchmark hold up"** — the sibling study's test:

**Test A — against the pre-registered default book.** Median retained fraction
of the in-sample Sharpe advantage: **−0.1782** (q25 −0.7846, q75 +0.3691);
62 of 162 keep a non-negative advantage. On CAGR the median retained fraction is
**−1.7616**; 66 of 162 keep a non-negative advantage.

**Test B — against the same book at the conventional parameter (N=200, monthly).**
Identical instruments, identical rebalance, so the only thing the search changed
is the moving-average length and the mode. This is the direct analogue of the
sibling's parameter-fishing test:

| | median retained | q25 | q75 | retained ≥ 0 | retained ≥ 0.5 |
|---|---|---|---|---|---|
| Sharpe | **+0.0692** | −1.3584 | +1.2841 | 71 of 137 | 57 of 137 |
| CAGR | **−0.2607** | −1.5736 | +1.1889 | 61 of 137 | — |

**A median of about 7% of the in-sample parameter advantage survives the
holdout, with an interquartile range that spans more than two units in both
directions.** That is the same order of magnitude as the 3% the sibling study
found for the best of its 30-combination grid, measured a different way on a grid
54 times larger. It extends that result; it does not contradict it.

The single best in-sample configuration makes the trap concrete:
`N150-monthly-SPY+QQQ+TLT+GLD`, in-sample Sharpe 0.9892, held out 0.9300 — and
against its own no-search reference it "retains 114.8%". But its advantage over
that reference was **0.0672 Sharpe in-sample**, i.e. it barely beat it to begin
with, and its full-window rank by `t` is **5th of 1,620 — it does not clear the
Bonferroni bar at all.** A report that led with "the search retains its edge"
would be leading with the one member of the top decile whose reference was
weakest.

---

## 6. The owner's real question: what is the maximum positivity?

Answered over **every** configuration, including the 1,610 that fail the bar.

### Years

| | result |
|---|---|
| highest fraction of positive complete years at a positive CAGR | **18 of 20 = 90.00%** |
| configuration | `N100-monthly-QQQ+TLT+GLD` |
| its CAGR / Sharpe / max drawdown | 6.79% / 0.8740 / −11.37% |
| its losing years | **2015 (−5.83%), 2022 (−7.77%)** |
| its worst year | **−7.77%** |
| does anything reach 100%? | **NO — 0 of 1,620** |

Relaxing the CAGR filter does not help: the maximum positive-year fraction over
all 1,620 configurations is also **18 of 20 (90.00%)**. Across **all 7,380
configurations of all three grids, not one is positive in every complete year.**

### Quarters and months

| period | best fraction | configuration | losing periods |
|---|---|---|---|
| quarters | **62 of 83 = 74.70%** | `N150-monthly-SPY+GLD` | 21 (listed in `RESULTS.md`) |
| months | **157 of 250 = 62.80%** | `N150-monthly-QQQ+IWM+GLD+EFA` | 93 (listed in `RESULTS.md`) |

**The plain answer.** The best achievable fraction of years any of these
thousands of real configurations reaches is **90%**, and it is reached by a
configuration selected by the same search that produced it. Nothing reaches
100%. As the measurement window shrinks the number falls — 75% of quarters, 63%
of months — which is what a strategy with a genuine but modest edge looks like,
and also what noise looks like.

The losing periods are not decoration, and they are concentrated in the two
episodes everyone remembers. The best **quarters** configuration
(`N150-monthly-SPY+GLD`) loses 21 of 83 quarters, its worst being **2022-Q2 at
−6.97%**, and its loss list includes **2008-Q2, 2008-Q3 and 2008-Q4**. The best
**months** configuration (`N150-monthly-QQQ+IWM+GLD+EFA`) loses 93 of 250 months
— its worst being **March 2026 at −7.24%** — and its loss list includes all three
months of **2008's fourth quarter** and **seven consecutive months of 2022
(April through October)**.

Two definitional notes, because they affect the counts:
- **A 0.00% period counts as not positive.** The rule is `return > 0`. Many of
  the losing months above read exactly 0.00% because the book was entirely flat
  for the whole month. That is a month the rule stood aside, not a month it lost
  money — but it is not a win either, and calling flat months wins would be the
  most flattering possible choice of convention.
- **The fractions are on COMPLETE periods only**, so a window that begins in the
  middle of a bad year is never credited with a good one.

There is no configuration in this sweep for which "always positive" is a
defensible description.

---

## 7. Regime coverage: what is structurally negative, and why

Regime = SPY trend state (close vs SPY's own SMA(200)) x SPY realised-vol
tercile (trailing 21 sessions, annualised, cut at **0.1046 / 0.1622** from this
window's own distribution). The label is measured *on* the session whose return
is attributed to it, so this is attribution, not prediction. All 5,261 window
sessions carry a label — the regime series is computed over the full history and
sliced, so the trailing-volatility window is always full.

Session counts per cell, over the 5,260 return days:

| | LOW | MID | HIGH |
|---|---|---|---|
| **UP** (above SMA200) | 1,752 | 1,635 | 711 |
| **DOWN** (below) | **2** | 117 | 1,043 |

That table is itself a finding, and it is more extreme than expected:
**SPY is above its own 200-day average on 4,098 of 5,260 sessions (77.9%)**, and
it is below that average *while realised volatility sits in the lowest tercile*
on **two sessions in 20.9 years**. Low-volatility regimes and downtrends barely
overlap, so `DOWN × LOW` is a null cell, not a result. A long-or-flat rule
therefore spends almost all of its offside time in high volatility — which is
exactly where its whipsaws are — and it inherits the market's drift on 78% of
sessions without any skill at all. That second fact is why the Bonferroni
survivor count in §4 is as large as ten.

The ten survivors' cells:

- **UP×LOW, UP×MID and UP×HIGH are positive in 10 of 10 survivors.** Being long
  in an uptrend is the entire edge, in every volatility tercile.
- **DOWN×MID is negative in 10 of 10.** It is the only universally negative cell
  with a usable sample.
- **DOWN×HIGH is negative in 8 of 10** — the two exceptions are
  `N150-monthly-SPY+GLD` and `N150-monthly-QQQ+TLT+GLD`, where gold carries that cell.
- UP×HIGH is not a losing cell anywhere. In several of the survivors it carries
  the **largest** mean of the six — high volatility above the average is where a
  trend rule earns, and the same volatility below the average is where it pays back.
- Negative-cell counts: 1 of 6 for the gold-led pair, 2 of 6 for the rest.

**So the structurally negative condition for a long-only trend approach is the
DOWN trend state, and specifically DOWN × MID.** The mechanism is structural, not
statistical: the rule is long-only, so its only defence in a downtrend is being
flat, and it can only become flat *after* price has already fallen through the
average. The sessions where price is whipsawing around the average — which is
what mid and high volatility in a downtrend look like — are the sessions the rule
gets caught in. It loses there because it cannot be short, and because there is
no cell for "trade nothing": when the rule is flat its return is exactly 0.0 and
that session is still counted as a flat entry in the cell.

---

## 8. Costs

Round-trip *c* bps charges *c*/2 bps per side on every sleeve flip and on each
monthly book reset's one-way turnover. The set re-run is **the surviving set from
§4 — all ten configurations that cleared the Bonferroni bar — plus the
pre-registered default as a reference row.** Every table line is in
`RESULTS.md` §8 and `out/costs.csv`.

| what | 20 bps round trip |
|---|---|
| the 5 **monthly**-rebalanced survivors | give up **0.23%–0.24%** of CAGR |
| the 5 **daily**-rebalanced survivors | give up **0.62%–0.88%** of CAGR |
| how many survivors go negative at 20 bps | **0 of 10** |
| grid-wide positive-CAGR count, 1,620 configs | 1,599 at 0 bps → 1,592 at 5 bps → **1,550 at 20 bps** |
| the default, as a reference row | 7.21% → 7.15% → **6.99%** |

Costs do not rescue or destroy anything here. A daily-rebalanced book pays on
every signal flip; a monthly one pays only at the month's reset, which is why the
daily survivors lose three to four times as much. Even so, all ten survivors stay
positive, and the grid-wide count barely moves — so **costs are not what
separates a survivor from a loser in this sweep**; the Bonferroni count is.
Note that a 20 bps round trip is *not* realistic for these instruments (SPY's
round trip is nearer 1 bp), so the 5 bps column is the one to read.

---

## 9. Robustness: other universes, other windows

| grid | universe | window | configs | critical \|t\| | clear the bar |
|---|---|---|---|---|---|
| **L** | SPY, QQQ, IWM, EEM | 2004-04-07 .. 2026-10-14 | 150 | 3.5879 | **1** (0.67%) |
| **P** | the 8 pre-registered | 2005-11-14 .. 2026-10-14 | 1,620 | 4.1670 | **10** (0.62%) |
| **X** | the 8 **+ IEF, HYG, DBC** | 2008-04-07 .. 2026-10-14 | 5,610 | 4.4420 | **0** (0%) |

The share of the grid that survives falls monotonically with grid size, from
0.67% to 0.62% to **zero**. That is the direct reproduction of the sibling
study's result — its wider grid also had **nothing** clear the bar — and it is
the answer to "would more iterations help?": **more iterations make it worse.**

Grid X also exposes an uncomfortable fact about "maximum positivity". Its best
configuration reaches **16 of 17 = 94.12%** of years — a *higher* number than
Grid P's 90% — but only because its window starts in April 2008, so its 17
complete years begin in **2009 and the worst year of the sample is not in them**.
The maximum-positivity number is a function of where the window starts at least
as much as of the rule. Quote it, and quote the window with it.

---

## 10. Does this contradict the sibling studies? No — it extends them

| study | its result | this sweep |
|---|---|---|
| `options-trading-playbook/.../regime-study` | best of a 30-combination grid beat its default by **+0.213R in-sample, +0.006R out-of-sample (3% retained)** | Test B: median retained parameter advantage **+6.9%**, IQR spanning ±1.3 |
| the same study, wider grid | **nothing** cleared the Bonferroni bar at m = 56 | Grid X: **nothing** cleared it at **m = 5,610** |
| the same study, main grid | m = 12, critical \|t\| = 2.865, one survivor | m = 1,620, critical \|t\| = 4.167, ten survivors, all holding gold |
| `equity-trading-playbook/.../weather-test` | four structurally different sleeves were **0.666–0.887** correlated — one bet, not several | the survivors here collapse onto **one asset** (GLD) and **one pair** (QQQ+GLD) |
| `equity-trading-playbook/.../regime-study` | no single rule set is profitable in every year or every regime, 1993–2026 | **zero of 7,380** configurations is positive in every year, 2004–2026 |

Same conclusion, on **86× the grid** (7,380 configurations against the options
study's 30 + 56 = 86), with four more instruments and a cross-asset book layer on
top. **More search produced fewer survivors, and the survivors that remain are
concentrated in one asset rather than spread across the universe.**

The one place this sweep is *weaker* than the sibling study is the window: 20.9
years from 2005, against the options study's 33 years from 1993. A 4-instrument
book cannot start before every member exists, and GLD did not list until November
2004. So this study adds breadth, not length, and it does not cover the 1990s at
all.

---

## 11. What this sweep cannot say

1. **Long-only, long-or-flat.** There is no short leg. A downtrend can only be
   avoided late, never profited from, so the DOWN regime cells are negative by
   construction rather than by measurement.
2. **Price-only series.** No distributions anywhere. TLT, IEF, HYG, VNQ and EEM
   are understated, and any always-long comparison most of all. A bond sleeve's
   true return is materially higher than what is measured here.
3. **The window is favourable and short.** Grid P is 20.9 years and starts in
   late 2005; Grid L is 22.5 years. Neither reaches the 1990s, because a
   4-instrument book needs every member to exist. Twenty complete years is a
   small sample for a "positive years" claim — the sibling engine's own `n_eff`
   says the yearly series carry less independent information than the count of
   years suggests.
4. **The holdout is kind.** See §5. A 2020-07 onward holdout for a long-or-flat
   equity strategy is close to the best case.
5. **One signal family.** The sweep varies N, the book and the rebalance mode.
   It does not vary the rule, so it says nothing about breakout, momentum
   ranking, carry, or mean reversion at other horizons.
6. **Mixed-N books were not run.** A book whose sleeves use different moving
   averages is `5^k x C(8,k)` for k = 2, 3, 4 — **700 + 7,000 + 43,750 = 51,450**
   more configurations, four times everything measured here. They were
   deliberately excluded, and they would only make the multiple-testing problem
   worse, so the exclusion is conservative.
7. **No position sizing, leverage, stops, or volatility targeting.** Every
   sleeve is 0 or 1. A risk overlay would change the drawdown column and the
   regime cells, and none is tested.
8. **The regime labels are SPY's.** "DOWN_rising" is an equity-trend statement
   applied to a book that contains gold and bonds.
9. **The last bar was still forming** at pull time and may revise.
10. **The `t` test is the wrong null for skill** (see §4). Nothing here is
    evidence for or against trend following as a *strategy*; what it measures is
    how much of a grid looks profitable, and how much of that survives being
    asked to repeat.

---

## 12. Verification status

| check | result |
|---|---|
| `study.py` determinism (two full runs of the FROZEN final code, all 7,380 configurations) | **byte-identical stdout** (546 lines, `diff` clean) and **byte-identical `out/*.csv`** — all 10 files matched by sha256 across both runs (runs L and M, ~115 s each) |
| independent re-derivation (`handcheck.py`, imports nothing from `study.py`) | worst gap **4.776e-07** across 6 check groups: 5 configurations × 5 full-window statistics, 4 configurations × 4 in-sample/held-out statistics, 3 max-positivity configurations × 3 statistics, the grid size, and the Bonferroni bar — the gap is the CSV's own 6-decimal rounding |
| by hand, one configuration, one year (`N200-monthly-SPY+QQQ+IWM+EEM`, 2015) | **−3.281575%** by hand from the equity curve (base = the prior session's close, printed), −3.281575% in the grid, gap **1.78e-15** |
| Bonferroni bar, recomputed by bisection instead of Acklam | m = 1,620 → **4.16699448** hand vs 4.16699400 in the file, gap 4.8e-07; cross-checks against published values for m = 1, 12, 30, 56 all agree to ≤ 3.7e-04 |
| the 70/30 split boundary, rebuilt independently (`handcheck.py CHECK 6`) | split index 3681; IS 2005-11-14..2020-07-01 (3,682 sessions), held out 2020-07-01..2026-10-14 (1,580, first a base day); IS and OOS **Sharpe, CAGR and positive-year fraction** all agree for 4 configurations, worst gap **4.3e-07** |
| declared grid size vs actually run | 1,620 / 150 / 5,610 declared, **1,620 / 150 / 5,610 run**, asserted in `SECTION 1c`; re-enumerated by recursion in `handcheck.py CHECK 0` |
| CSV vs the vendor, last six sessions of five series | worst \|diff\| **0.000000** over 30 bars (`source-check.txt`) |
| `make-results.py --check` | `RESULTS.md` is current against `run-output.txt` |

### What was NOT verified, and is therefore weakest

1. **The regime tercile boundaries.** Recomputed inside `study.py` from the
   window's own distribution; `handcheck.py` does not re-derive them, and the
   cell membership of any particular session was not checked by hand.
2. **The cost model.** A declared model, not an independent one. No spread data
   was pulled, so the 5 bps and 20 bps columns are scenarios, not measurements.
3. **The VIX-derived vol terciles** rest on the TVC:VIX index series, which is
   not tradable and is a 30-day constant-maturity index applied to a 21-session
   window.
4. **Grids L and X were not hand-checked.** Only Grid P configurations were
   re-derived independently. Their `out/grid_L.csv` and `out/grid_X.csv` come
   from the same code path, so a bug in the metrics would affect all three
   together — which is exactly why Grid P was the one re-derived.
5. **`n_eff` and `t_eff`.** Taken from the sibling engine and reported, not
   independently re-derived; the `rho1` values behind them were taken as given.

### Defects found and fixed during development

Recorded because a study that only reports its final state hides how much of the
final state was repair. Each of these was caught by re-reading the output against
the table it quotes, not by a test:

1. **The regime label series was computed over the window only.** The trend state
   and the trailing 21-session realised volatility were derived from the
   window-aligned SPY array, so the first ~199 sessions had no SMA(200) and were
   labelled DOWN, and the first 20 had no vol tercile at all. That mislabelled
   ~199 of 5,260 sessions and populated a spurious `DOWN × LOW` cell with 98
   sessions. Both series are now computed over the full history and sliced;
   `DOWN × LOW` collapsed to **2 sessions**, which is the honest count. The
   §7 table above is the corrected one — **an earlier version of this file
   quoted 98.**
2. **The narrative contradicted its own table.** The regime commentary asserted
   that "HIGH vol cells are the losers within an UP trend" while the table
   directly above it showed `UP × HIGH` positive in 10 of 10 survivors and
   carrying the *largest* mean in several. The claim is now the one the data
   supports: the DOWN trend state is the loser.
3. **Unmeasured numbers in the prose.** The text asserted the median
   configuration "is long roughly two thirds of the time". The measured figure is
   **77.9%** of sessions above SPY's SMA(200). The prose now quotes the
   measurement.
4. **The mixed-N grid size was wrong in three files.** `5^k x C(8,k)` for
   k = 2,3,4 is **700 + 7,000 + 43,750 = 51,450**, not "700 + 5,000 + 35,000".
5. **A drawdown row was printed worst-first** under a header labelled
   best → worst. Drawdowns are stored as negative fractions, so the largest
   value is the smallest fall; the row is now ordered correctly.
6. **`handcheck.py` had two bugs of its own, both found by its own gaps.** Its
   first version computed the moving average over the window instead of the full
   history (gap up to 1.3e-02 in Sharpe), and its second treated the
   daily-rebalanced book as a drifting-weight book (gap up to 1.1e-02 in CAGR).
   Both produced gaps of ~1e-2 that were far too large to be rounding, which is
   precisely why the independent implementation exists.
7. **`make-results.py` lost every section heading.** It labelled each buffered
   block with the *next* banner's title instead of the previous one, so
   `RESULTS.md` first rendered as one undifferentiated block of output with a
   single heading at the very end. The freshness gate passed the whole time — a
   hash gate proves the file matches the run, not that the file is readable. It is
   fixed, and `RESULTS.md` now carries 14 headings.
