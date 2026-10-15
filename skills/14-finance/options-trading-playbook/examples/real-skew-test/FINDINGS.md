# FINDINGS — real-skew-test

**The skew assumption is settled: it was wrong by a factor of five, and the
large sample now says so with a confidence interval. The premium-selling
conclusion is NOT settled, and the larger sample says the previous alarming
answer was an artefact of n=5.**

Read `README.md` §9 before quoting anything. Everything below that comes from a
real SPY option print is labelled `[MEASURED]`; anything from the VIX proxy is
labelled `[MODELED]`.

---

## 1. Headline: the skew number, with its uncertainty

The assumption under test — the one the entire existing premium-selling result
was built on — is **1.5 vol points per 10% OTM**.

| quantity | `[MEASURED]` | vs 1.5 |
|---|---|---|
| **skew slope, median** | **8.19 vol pts per 10% OTM** | **5.5×** |
| skew slope, 95% bootstrap CI | **7.00 to 9.01** | the CI's lower end is **4.7×** |
| skew slope, quartiles | 6.95 to 9.02 | |
| skew slope, range (n=15) | 6.02 to 11.12 | the **minimum** is 4.0× |
| skew slope, mean ± SE | 8.12 ± 0.36 | |
| ladders above +1.5 | **15 of 15** | |
| **put-call IV spread, median** | **5.51 vol pts** | **3.7×** |
| put-call spread, 95% bootstrap CI | 4.72 to 7.73 | lower end is **3.1×** |
| put-call spread, range (n=18) | 2.88 to 14.41 | the **minimum** is 1.9× |

**This is the answer, and it is decisive for the skew question.** The measured
skew is five times the assumption, on 15 independently drawn ladders, and the
*lower* end of the 95% confidence interval is still 4.7× the assumption. The
first pass's 7.22 (n=4) is inside this interval; the two studies agree.

**The single cleanest ladder** is SPY 2020-03-02, 46 DTE, spot 309.09 — a
complete 4-put/2-call panel, and the only complete ladder this study shares with
pass one:

| strike | moneyness | real price | `[MEASURED]` IV | delta |
|---|---|---|---|---|
| 263 put | −14.9% | 2.96 | **42.12%** | −0.122 |
| 278 put | −10.1% | 5.04 | **38.98%** | −0.198 |
| 291 put | −5.9% | 7.68 | **35.89%** | −0.290 |
| 300 put | −2.9% | 10.08 | **33.44%** | −0.372 |
| 318 call | +2.9% | 5.02 | 19.25% | 0.362 |
| 328 call | +6.1% | 1.64 | 16.61% | 0.172 |

A monotone rising put curve and a falling call curve, over a **14.19 vol-point**
put-call gap at matched moneyness. Same numbers as pass one, reproduced
independently. That 2020-03-02 panel is the study's strongest single result.

**One honest caveat that travels with the number.** This is the skew of the
strikes that **traded**, and the sample has **no true at-the-money measurement** —
every put ladder starts at 3% OTM by design, so any d=0 figure is an
extrapolation. The **slope** is unaffected by that; the **level** is.

## 2. What the large sample changes, and what it does not

| quantity | first pass | this run | verdict |
|---|---|---|---|
| skew slope, median | 7.22 (n=4) | **8.19 (n=15)** | **replicates** |
| put-call IV spread, median | 6.05 (n=4) | **5.51 (n=18)** | **replicates** |
| premium re-run `E_R` | **−0.0908** (n=5) | **+0.0067 gross / −0.0082 net** (n=20) | **does NOT replicate** |

The skew findings replicate. The premium-selling finding does not, and the
reason is worth stating plainly: **pass one's −0.0908 was one COVID loss in five
entries.** With 20 entries the same programme — priced the same way, from real
prints — has a mean R indistinguishable from zero. This run contains **two**
full −1.00 max losses (2020-02-24, whose expiry closed at 248.19 against a 303
short strike; and 2022-04-01, 411.34 against 426) and still lands at zero,
because four of the twenty entries cleared more than +0.20.

So: the first pass's *direction* was an artefact of sample size, and reporting it
as a finding ("the sign flips negative") was over-claiming. This run corrects
that. See §5.

## 3. The measurement path, and the five traps that cost calls

The call path is `get_option_chains` → `get_option_instruments` →
`get_option_historicals`, with `state="expired"` to reach the expired catalogue.
**Total MCP calls: 201** (`logs/mcp-call-log.tsv`).

Five traps, four inherited and one new:

1. **`expiration_dates` must be a SINGLE date.** A list returns empty.
2. **The `strike_price` filter is flaky.** 22 of 122 declared rows (18%) needed
   more than one call; the mean is **1.34 calls per contract**. Every contract
   got up to 4 attempts at the exact strike, then an ordered neighbour probe. The
   per-contract attempt counts are in `logs/instrument-ids.tsv`. **A single empty
   result is not evidence of absence.**
3. **The strike grid is not uniformly $1.** 8 of 120 ladder contracts needed a
   substitution, flagged in the CSV.
4. **Good Friday.** SPY 2020-03-02 + 39 days = 2020-04-10, which is Good Friday:
   the market was closed, so the expiry does not exist and all six resolution
   calls came back empty. The declared override moves that ladder to
   **2020-04-17 (46 DTE, outside the band)**, the nearest expiry with a full set
   of prints. The in-band substitute 2020-04-09 exists but printed on only 1 of
   6 strikes.
5. **NEW, and it would have corrupted the whole study: an `end_time` equal to the
   sample date truncates that session's own bar.** The first three dates were
   pulled with `end_time = sample_date T23:59:59Z` and silently reported the
   *previous* session's print. Extending the window by a few days made the sample
   date's bar appear — verified on SPY 2018-11-09 P283, which reads **1.80 on
   2018-09-28** with the short window and **1.57 on 2018-10-01** with the
   corrected one. All three dates were re-pulled. The correct window is
   `[sample_date − 8d, sample_date + 3d]`. A one-line window error would have
   introduced a uniform one-session lag into the entire measurement.

**And one discovery about the data's shape that constrains what can be asked of
it.** Sessions before a contract's first trade *in the window* come back
`interpolated: true` at $0.01. A strike showing only interpolated bars therefore
had **no trade at all** — it is genuinely unmeasured, not a flaky query. The
consequence is severe: **40 of the 122 declared rows have no usable print**, and
the far-OTM strikes are the ones that vanish (14 of them never resolved as an
instrument at all).

The funnel, in full:

| stage | count |
|---|---|
| declared (120 ladder + 2 parity) | 122 |
| resolved as an instrument | 108 |
| returned a **non-interpolated** bar | 82 |
| passed the **$0.10** print floor | 81 |
| passed the IV band [2%, 150%] | 81 |
| usable date panels | **20 of 20** |
| **ladders with ≥2 put prints (the slope sample)** | **15** |

Exclusions: **40** no print; **1** below the $0.10 floor (a $0.06 call).
Flags: **6** flat bars (`open == high == low == close` — one print is the whole
session) and **6** bars with an impossible `low` of $0.01 while the close is
above $1. **No monotonicity violation was detected on either side** under a
2.0-vol-point slack.

## 4. Is the skew stable? Yes for the slope, no for the spread

| era | n | median slope / 10% OTM | median put-call spread |
|---|---|---|---|
| 2017–2019 calm | 4 | 7.93 | 4.93 |
| COVID Feb–Apr 2020 | 2 | 7.69 | **9.19** |
| late 2020–2021 | 3 | 9.05 | 5.29 |
| 2022 drawdown | 2 | 7.52 | 4.95 |
| 2023–2026 | 4 | 7.59 | 5.49 |

**The slope is remarkably stable** — 7.52 to 9.05 across nine years and two
crises, a spread of 1.5 vol points. **The level offset is not**: the put-call
spread nearly **doubles** in the COVID window (4.93 → 9.19).

| group | n | median slope | median put-call spread |
|---|---|---|---|
| stress (COVID + 2022) | 4 slopes / 5 spreads | **7.69** | **8.88** |
| rest | 11 slopes / 13 spreads | **8.19** | **5.27** |

So: **in stress the whole surface lifts and the put-call gap widens by ~3.6 vol
points, while the slope across the put ladder does not steepen** — it slightly
*flattens*. That is the same opposition the first pass found, now on 5 stress
dates rather than 1.

**This is a direct answer to the brief's era question, and it kills the idea of
one global "skew" number.** Whichever of the two natural metrics you pick, the
other one moves independently, and in stress they move in opposite directions.

**2008 is not reachable.** The expired-contract catalogue starts ~2017-09-15;
2017-08-18 and every earlier expiry tested return an empty instrument list. The
pre-2017 crisis skew therefore **cannot be measured**, and the model was **not**
substituted for it anywhere in this study.

## 5. The re-run: on real prices, the premium-selling edge is not measurable

Sibling programme S2: each period, sell a ~16-delta put spread, short leg near
6% OTM, wing $5 lower, hold to expiry, settle at intrinsic. **Both legs priced
from the MEASURED put ladder**, interpolated in log-moneyness. No VIX anywhere.

| | gross of costs | after LOW costs |
|---|---|---|
| n entries | 20 | 20 |
| p (win rate) | 0.8500 | 0.8500 |
| b (mean win R) | 0.1745 | 0.1572 |
| **E (mean R per entry)** | **+0.0067** | **−0.0082** |
| median R | 0.1308 | 0.1149 |
| min / max R | −1.0000 / +0.5907 | −1.0000 / +0.5595 |
| bootstrap 95% CI for mean R | **−0.1843 to +0.1706** | |

**The 95% CI spans zero.** The point estimate is a hair above zero gross of
costs and a hair *below* zero after realistic costs.

**So the verdict on the premium-selling edge is: NOT MEASURABLE AT THIS SAMPLE
SIZE.** Not positive, not negative — indistinguishable from zero, with an
interval wide enough to contain both the sibling's +2.97% CAGR flavour and a
meaningful loss. What the run *does* establish:

1. **The modelled +2.97% CAGR is not reproduced.** Over 20 measured entries the
   mean is ~0, with two full max losses and a high win rate. That is a
   *different shape* from "89.8% of months positive, +2.97% CAGR".
2. **The first pass's −0.0908 does not survive.** It was one COVID loss in five
   entries. On 20 entries, priced identically, the answer is zero.
3. **The mechanism the sibling blamed is not the mechanism.** See §6.

**The two full losses are instructive and they bracket the risk:** 2020-02-24
(spot 322.42, short the 303 put) settled at **248.19** on 2020-04-03 — deep
through both strikes; and 2022-04-01 (spot 452.92, short 426) settled at
**411.34** on 2022-05-06. The single biggest winner was 2020-04-01 (+0.59) —
the same crisis, from the other side, because the short 231 put expired 61
points out of the money on the 292.44 recovery.

## 6. The most important structural finding: the skew barely moves the spread

The sibling's own conclusion was: *"the honest reading is that this is the single
most likely reason the S2 result would not survive contact with actual quotes."*
The measurement does not support that.

| variant | mean R | sign |
|---|---|---|
| **A. both legs from the MEASURED ladder** `[MEASURED]` | **+0.0067** | ~0 |
| **D. both legs at flat VIX (the sibling's model)** `[MODELED]` | **+0.0129** | ~0 |
| E. measured, minus **1.5** vol pts on the **sold leg only** | −0.0949 | negative |
| F. measured, minus **3.0** vol pts on the **sold leg only** | −0.1704 | negative |
| B. sold leg at zero vol, wing measured | −0.4045 | negative |
| G. sold leg at zero vol, wing at flat VIX | −0.3425 | negative |
| H. sold leg at flat VIX, wing at zero vol | −0.4405 | negative |
| C. both legs at zero vol (pure intrinsic credit) | −0.1436 | negative |

**A vs D differ by only −0.0062 R per entry.** Pricing BOTH legs off the real
ladder instead of the flat VIX model moves the mean by six thousandths of the
risk unit. The flat model was wrong — §7 shows it was wrong in a structured way
— but it was wrong **on both legs, in opposite directions, and the two errors
very nearly cancel inside a $5-wide spread.**

**The dramatic sign flip the sibling produced comes from variant E/F, not from
the real skew.** A haircut applied *only* to the sold leg leaves the wing
untouched, so it double-counts: the seller is charged the skew twice — once on
the leg being shorted, and again by leaving the bought wing at the measured
(higher) vol. Variants E and F are therefore **an upper bound on how much skew
can hurt this structure, not a realistic treatment of it.**

This is exactly the asymmetry the brief flagged, now measured: **the first pass
was right that the flat model was wrong on both legs, and right that a
haircut applied only to the sold leg overstates the damage.** The corollary is
new and it is the important one: **for a defined-risk spread, "there is a big
skew" does not imply "the modelled credit is overstated."** The credit is
overstated near the money and understated in the wing, and those two errors are
of similar size on a $5 width.

## 7. The old model was wrong in a structured way, and where

Repricing all 81 measured contracts with the sibling's exact flat-vol method
(`VIX(t−3)/100`, kappa = 1 for SPY) against the real prints:

| statistic | price error | vol-point error | percentage error |
|---|---|---|---|
| min | −$3.67 | −16.25 | −100.0% |
| median | **+$0.01** | +0.05 | +0.3% |
| max | **+$10.62** | +21.81 | +819.7% |
| mean | +$0.69 | +0.18 | +40.5% |

The median is *tiny* — that is itself the finding — but the tails are enormous,
and the shape is systematic:

| moneyness | n | median price error |
|---|---|---|
| 3–6% OTM | 62 | **+$0.72** (model too **RICH**) |
| 6–12% OTM | 13 | −$0.88 (model too **CHEAP**) |
| >12% OTM | 6 | −$0.46 (model too **CHEAP**) |

| tenor | n | median price error |
|---|---|---|
| 35–39 DTE | 75 | +$0.10 |
| 45–49 DTE | 6 | **−$2.42** (the 46-DTE override ladder) |

A flat vol is too rich near the money and too cheap in the wings — the signature
of a missing skew — and that structure, not the magnitude, is what cancels in a
$5-wide spread.

**The caveat that must travel with the percentage column.** The extreme
percentage errors are dominated by contracts quoted at or near the $0.01
minimum tick, where a one-tick difference is a 100% error, and by the one print
this study actually excluded for it (a **$0.06** call on 2017-10-02). Several
$0.10–$0.25 prints in the sample sit at 10–25 ticks and carry the same problem in
milder form. **The price-error distribution is reliable in dollars; the
percentage column is not a market-level statement.**

## 8. The data-quality threat that dominates everything, stated plainly

**Option bars from this source are LAST-TRADE PRINTS, not marks.** There is no
volume, no bid, no ask and no open interest, so a print cannot be distinguished
from a stale quote by any field in the data. Three measured consequences:

**(a) The call side is systematically stale-low, and it inflates the put-call
spread.** The measured 3%-OTM put IV against VIX(t−3) is mostly within ±1 vol
point — for 2018-04-02, 2022-04-01, 2023-04-03, 2023-10-02 and 2024-04-01 the
two agree to within 1 point. But the measured **call** IVs are frequently
implausible: 6.43% for the 2017-10-02 260 call and 8.13% for the 2018-10-01 300
call, against VIX of 9.87% and 12.89%. Those are prints, not markets. **A stale
call print makes the put-call spread larger**, so the median 5.51 is more likely
an over-estimate than an under-estimate. The put **slope** is far less exposed to
this, because the put side is the liquid side and the strikes are nearer the
money.

**(b) Six of 81 contracts are flat bars** — the session's entire information
content is a single print — and **six more carry an impossible low of $0.01**
while closing above $1. Only the close is used.

**(c) Put-call parity fails by 3.2 and 3.4 vol points** on the two ITM puts that
were resolved by mistake alongside the calls at the same strike and expiry
(SPY 2020-05-08, 254 and 261). For European options those IVs must be equal. Two
causes, both stated rather than buried: SPY options are **American**, so a
deep-ITM put carries an early-exercise premium that a European Black-Scholes
pricing cannot see; and an ITM price is dominated by intrinsic, so its implied
vol is numerically ill-conditioned. **This is a real, quantified inconsistency in
the measurement, and it is the honest bound on the study's precision.**

**The good news, and it is not small: the price series is the vendor's own.**
Four live contracts were checked against `get_option_quotes` and the historical
bar close for 2026-10-13 equals the **official settled close** for that session
**exactly** in all four cases (11.35 / 5.34 / 13.50 / 33.72). And the vendor's
live IVs independently confirm the put skew: on the live SPY 2027-01-15 expiry
the 750 put prints **16.56%** and the 700 put **21.00%**, against the 800 call's
**11.99%** — roughly 6.8 vol points per 10% OTM, the same order as the historical
ladders measured here.

## 9. Verification

- **Determinism.** `study.py` and `handcheck.py` were each run twice and `diff`ed;
  both pairs are **byte-identical**. The bootstrap uses a fixed-seed LCG
  implemented inside `study.py`.
- **Independent hand-check.** `handcheck.py` shares no code with `study.py` — an
  Abramowitz & Stegun 7.1.26 `erf` instead of `math.erf`, a bracket-expansion
  bisection, and OLS through the normal equations. It prints every
  Black-Scholes intermediate for five real prices.
  - implied vol, 5 contracts: largest gap **0.0042 vol points**
  - one ladder's slope (2020-03-02): gap **0.0024 vol points**
  - one settled spread (2020-03-02, 291/286): R agrees to **6 decimals**
    (`−0.833957` both ways; the 0.0040 printed is `study.py`'s 2-decimal table
    rounding)
  - **The hand-check found a real bug — in itself.** Its interpolation array was
    built in ascending-strike order, where `d = −ln(K/S)` is *descending*, and it
    silently returned a plausible but wrong wing vol (37.376% instead of
    37.060%). That is precisely why the two files are run side by side: a
    plausibility check on the final R would not have caught it.
- **Live cross-check.** 4 of 4 exact matches against the official settled close.

## 10. What remains unmeasured, and what would change the sign

1. **Any pre-2017 regime, including 2008.** Catalogue floor ~2017-09-15. No
   substitute was used.
2. **The true at-the-money vol, and the extreme wings.** The ladder starts at 3%
   OTM; the far wings are where the prints die.
3. **Liquidity, real spread cost, and fills.** No volume/bid/ask exists in this
   data. The LOW cost setting ($0.65/contract/side + $0.025/share/side) is an
   assumption, not a measurement, and it is worth ~0.008 R per entry here — i.e.
   of the same order as the whole measured mean.
4. **A representative time series.** 20 dates, 15 fittable ladders. Quarterly
   resolution over nine years would be ~36 ladders; the flaky filter makes that
   ~500 resolution calls, which is affordable and is the obvious next step.
5. **QQQ and IWM.** Declared secondary, not pulled. On pass one's evidence they
   produce no fittable ladder.

**What would change the sign of the premium-selling verdict.** The mean R is
+0.0067 ± 0.09. The sample is dominated by benign periods for a put seller (15 of
20 entries won, most by decay). One thing would move it decisively: **more
measured entries, deliberately including more stress dates.** A programme whose
measured mean sits at zero with a high hit rate and two max losses has negative
tail risk that 20 entries cannot size. **Do not claim profitability from this.**
The honest measured statement is that the premium-selling edge is **indistinguishable
from zero at n=20**, that the modelled +2.97% CAGR is not reproduced, and that
the skew — five times larger than assumed — is **not** the reason.

## 11. Bottom line

- **The skew assumption was wrong by a factor of five.** `[MEASURED]` median
  **8.19 vol points per 10% OTM**, n=15, 95% CI **7.00 to 9.01**; the put-call
  spread is a median **5.51** vol points, n=18, CI 4.72 to 7.73. Fifteen of
  fifteen ladders exceed 1.5. The first pass's 7.22 sits inside this interval.
- **The premium-selling verdict is NOT MEASURABLE.** `[MEASURED]`, n=20:
  `E_R = +0.0067` gross / `−0.0082` net, CI **−0.184 to +0.171**, spanning zero.
  The modelled +2.97% CAGR is not reproduced and the first pass's −0.0908 does
  not survive.
- **The skew is not what breaks the spread.** Pricing both legs off the real
  ladder versus a flat VIX moves the mean R by **−0.0062** — the flat model was
  wrong on both legs in opposite directions and the errors cancel on a $5 width.
  The dramatic flips come only from the *unrealistic* treatment of haircutting
  the sold leg alone.
- **The slope is stable (7.52–9.05 across nine years); the level is not**
  (put-call spread 4.93 → 9.19 in COVID). One assumed number is indefensible;
  so is one assumed *metric*.
- **The binding constraint is that prints are not marks**, and 40 of 122
  declared contracts have no print at all. That, not the analysis, is what limits
  this study.
