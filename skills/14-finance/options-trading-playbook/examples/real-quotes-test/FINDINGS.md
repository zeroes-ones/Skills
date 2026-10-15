# FINDINGS — real-quotes-test

**The single largest gap in this body of trading research is now closed for the
window the data actually covers, and the answer moves the sign.**

Every option number produced before this study was `[MODELED]`: Black-Scholes at
a VIX-derived implied vol, because historical option quotes were believed
unavailable. They are available, and this run pulled **27 real option prices**
from Robinhood's expired-contract history. Everything below that comes from one
of those prices is labelled `[MEASURED]`; anything still derived from the VIX
proxy is labelled `[MODELED]`.

Read `README.md` §8 before quoting anything. The sample is small and I say so
throughout.

---

## 1. First: the data exists, but only from late 2017

The gating fact, established before any sample was designed:

- SPY expired expiries **resolve from 2017-09-15 onward**.
- **2017-08-18, 2017-07-21, 2017-06-16, 2017-03-17, 2016-01-15 and 2015-01-16
  all return an empty instrument list** — retested, not a fluke.

So the option universe starts in Q3-2017. **2008 is out of reach.** That kills
one of the six questions in the brief outright: the pre-2017 crisis skew cannot
be measured, and I will not substitute the model for it. I did not probe the
QQQ/IWM floors separately.

Two operational traps, both of which cost real calls:

1. **`expiration_dates` must be a single date.** A comma-separated list returns
   empty. Verified twice, on expiries I knew to be populated.
2. **The `strike_price` filter is flaky and a single empty result means
   nothing.** 2018-02-09 P260 appears in that expiry's own paginated listing,
   and a filtered query for it returned empty on the first attempt and the
   instrument on the second. About 45% of first-attempt filtered queries came
   back empty. Every contract was therefore retried, and the attempt count is
   recorded per contract. Related: the strike grid is not uniformly $1 — for
   2018-02-09 it steps by $2.50 below 245, so the target 242 genuinely does not
   exist and 242.5 was used instead, flagged in the CSV.

## 2. The measured skew is four to five times the assumption

**The assumption under test was 1.5 vol points.**

| quantity | `[MEASURED]` | the assumption |
|---|---|---|
| skew slope, median | **7.22 vol pts per 10% OTM** | 1.5 |
| skew slope, range (n=4) | 4.87 – 10.87 | 1.5 |
| put-call IV spread, median | **6.05 vol pts** | 1.5 |
| put-call IV spread, range (n=4) | 3.61 – 14.19 | 1.5 |

The comparable number to the sibling's 1.5 vol-point *haircut* is the put-call
IV **spread** (a level offset on the sold leg), and it is a median of **6.05**
vol points. The measured **slope** is **7.22** vol points per 10% OTM. Both are
several times the assumed 1.5, and the minimum observed spread (3.61) is still
2.4× the assumption.

The cleanest picture is the one complete ladder — **SPY 2020-03-02**, 46 DTE,
spot 309.09:

| strike | moneyness | real price | `[MEASURED]` IV |
|---|---|---|---|
| 300 put | −2.9% | 10.08 | **33.44%** |
| 291 put | −5.9% | 7.68 | 35.89% |
| 278 put | −10.1% | 5.04 | 38.98% |
| 263 put | −14.9% | 2.96 | 42.12% |
| 247 put | −20.1% | 1.62 | **45.43%** |
| 318 call | +2.9% | 5.02 | 19.25% |
| 328 call | +6.1% | 1.64 | 16.61% |
| 340 call | +10.0% | 0.36 | 15.79% |

A monotone rising put curve and a falling call curve, over an 11.99
vol-point put-call gap at matched moneyness. That is a real skew, and it is
nothing like flat.

The same shape appears on the other dates: SPY 2018-01-02 puts run 11.09% at
−2.9% OTM to 18.68% at −9.8%; SPY 2022-06-01 runs 26.43% to 30.28%. The
2020-01-02 put ladder runs 14.05% → 25.63%.

## 3. The old model was wrong in a structured way, and the direction matters

Repricing every real contract with the old method (Black-Scholes at
`VIX(t−3)/100 × kappa`, the sibling's exact model) against the real prices:

| statistic | price error | vol-point error | percentage error |
|---|---|---|---|
| min | −$3.25 | −21.62 | −99.9% |
| median | **−$0.14** | **−0.62** | −4.9% |
| max | +$3.71 | +11.77 | +772.6% |
| mean | +$0.11 | −1.31 | +103.3% |

The median is small; the tails are enormous; and the *shape* is the finding:

| moneyness | n | median error |
|---|---|---|
| 3–6% OTM | 19 | **+$0.53** (model too RICH) |
| 6–12% OTM | 5 | −$0.71 (model too CHEAP) |
| >12% OTM | 3 | **−$1.52** (model too CHEAP) |

A flat vol prices the near-money slightly high and the far wings badly low —
precisely the shape a missing skew produces. In the sibling's spread this means
the old study **over-credited the leg it sold and under-credited the wing it
bought**. On 2018-01-02 the model prices the 242.5 put (real $0.26) at
**$0.00** and the 285 call (real $0.02) at $0.17; on 2020-01-02 it prices the
275 put (real $0.16) at $0.00.

**Caveat that must travel with this:** the extreme percentage errors are
dominated by contracts quoted at the $0.01–$0.04 minimum tick, where a
one-tick difference is a 100% error. The SPY 2018-01-02 285 call printed
**$0.02** where even a flat 10.47% vol implies $0.17. A $0.02 print is a stale
or nominal last trade, not a market. Those contracts should be read as
**unmeasured**, not as evidence of a 7.48% IV.

## 4. The re-run: with the measured skew, the sign goes negative

The sibling's S2 sells a ~30-DTE ~16Δ put spread, $5 wide, monthly, to expiry.
I re-priced it using the **measured per-strike IV** interpolated in
log-moneyness across the measured ladder — **no VIX anywhere in that
calculation** — and settled against the real underlying closes.

| und | entry | K_short | K_wing | IV_short | IV_wing | credit | R |
|---|---|---|---|---|---|---|---|
| SPY | 2018-01-02 | 253 | 248 | 14.30% | 16.36% | $14.53 | +0.03 |
| SPY | 2020-01-02 | 305 | 300 | 17.10% | 18.46% | $27.72 | +0.06 |
| SPY | 2020-03-02 | 291 | 286 | 35.89% | 37.06% | $114.56 | **−0.83** |
| SPY | 2022-06-01 | 385 | 380 | 28.12% | 28.78% | $92.57 | +0.23 |
| QQQ | 2018-01-02 | 149 | 144 | 15.46% | 15.46% | $30.05 | +0.06 |

| statistic | value |
|---|---|
| n entries | 5 |
| p (win rate) | 0.8000 |
| b (mean win R) | 0.0949 |
| **E (mean R per entry)** | **−0.0908** |
| median R | 0.0587 |
| min R | −0.8340 |
| max R | 0.2272 |

**E_R = −0.0908. The sign is NEGATIVE.**

Compare:

| run | result |
|---|---|
| sibling, no skew haircut `[MODELED]` | CAGR +2.97%, 89% of months positive |
| sibling, +1.5 vol pts `[MODELED]` | CAGR **−0.87%** (sign flips) |
| sibling, +3.0 vol pts `[MODELED]` | CAGR −4.03% |
| **this re-run, measured IV `[MEASURED]`** | **E_R = −0.0908, negative** |

**It agrees with the sibling's flip direction and disagrees with its headline.**
The mechanism is exactly the one the sibling sized: the real spread credit is
small relative to the risk once the wing is priced at a realistic vol, and one
bad month (COVID, −0.83R) outweighs four good ones totalling +0.38R.

**Do not over-read this.** Five entries is not 306 months. This is not a CAGR,
it carries no usable confidence interval, and four of the five windows were
benign for a put seller. What it does establish is the **direction and the
mechanism**: with the skew measured rather than assumed, the modelled edge does
not survive, and the reason is the wing.

There is one honest counter-current to report: the *modelled* re-run at a 3.0
vol-point haircut was worse (−4.03%) than this measured run's E_R suggests per
month, because the measured IVs also raise the credit collected on the short
leg. A large part of the real skew is in the very leg being sold, not only in
the wing. The correct statement is that the flat-vol *model* was wrong on both
legs in opposite directions, and cancelling the two errors is not available to a
trader who must trade real prices.

## 5. Term structure: inverted at the one stress date measured

SPY 2020-03-02, two expiries, three common strikes — all `[MEASURED]`:

| type | strike | 18 DTE IV | 46 DTE IV |
|---|---|---|---|
| put | 300 | **40.67%** | **33.44%** |
| put | 278 | **49.18%** | **38.98%** |
| call | 328 | 18.58% | 16.61% |

A steeply **inverted** term structure, as expected in a crash, with the gap
widest in the far put (10.2 vol points at 278). This is 3 strikes on 1 date, so
it is a demonstration that the measurement works at two tenors, not a term
structure study.

## 6. Is the skew stable? No — and that is the answer

| date | underlying | slope (vol pts/10% OTM) | put-call spread |
|---|---|---|---|
| 2018-01-02 | SPY | 10.87 | 3.61 |
| 2020-01-02 | SPY | 8.91 | 5.78 |
| 2020-03-02 | SPY | 4.87 | **14.19** |
| 2022-06-01 | SPY | 5.54 | 6.32 |

The two measures move **in opposite directions** in stress. The put-call
**spread quadruples** (3.61 → 14.19) — the whole surface lifts and the put skew
deepens in absolute terms — while the *slope across the put ladder flattens*
(10.87 → 4.87), because in a high-vol regime the ladder's fixed moneyness steps
sit lower in a more uniformly elevated surface.

So **a single assumed number is indefensible**, and worse, a single assumed
*metric* is: whichever of the two you pick as "the skew", it moves by a factor
of 2–4 across four dates. The sibling's 1.5 vol points is below the minimum of
both ranges.

**Stress check:** only one stress date (2020-03-02) is measurable. 2008 is not
in the data. The claim "skew widens in stress" rests on **n = 1** and is
reported as such.

## 7. What remains unmeasured

1. **Any pre-2017 regime, including 2008.** The catalogue floor is 2017-09-15.
2. **A representative time series of skew.** 4 date-underlying panels, 27
   prices, one complete ladder. The quarterly design that would answer
   "stable or not" properly was declared and then cut for call budget; the cut
   is itemised in `README.md` §3.
3. **QQQ and IWM skew.** Both reduce to a single date with a 1-point ladder —
   too few puts to fit. Only SPY produced skew slopes.
4. **Half the declared contracts.**
   - **11** never resolved as instruments despite 2–6 attempts each
     (SPY 2018-02-09 P215/P228, SPY 2020-02-07 P260/C357,
     SPY 2022-07-08 C451, IWM 2018-02-09 C169, and the 5 unresolvable legs of
     the 2020-03-20 term panel).
   - **18** resolved but had **no non-interpolated bar** on the sample date
     (SPY 2018-02-09 P253/C277/C296, SPY 2020-02-07 P292,
     SPY 2022-07-08 P348/P328, and 12 QQQ/IWM legs).
5. **Liquidity.** Option bars carry no volume, so a print cannot be
   distinguished from a stale quote by any field in this data. This is the
   single biggest threat to the IVs: several $0.01–$0.04 prints drove the
   percentage-error tail.
6. **Anything requiring a mark rather than a print** — no bid/ask, no open
   interest, no spread cost measurement.
7. **American early exercise**, still modelled as European.
8. **The 46-DTE tenor** used for the stress date sits outside the declared
   30–45 DTE band, because the 39-DTE expiry (2020-04-10) could not be resolved
   at all.

## 8. Bottom line

- The historical option data **is** retrievable, and it is internally
  consistent: the historical bar close equals the official settled close
  **exactly** for all three live contracts cross-checked.
- **The real skew is 6.05 vol points of put-call spread (median) and 7.22 vol
  points per 10% OTM of slope — four to five times the 1.5 the previous study
  assumed.**
- **Re-priced on measured IVs, the premium-selling programme's mean R is
  negative (−0.0908, n=5).** The sign agrees with the sibling's own
  flip-direction finding and contradicts its modelled headline. It is a partial
  measured window, not a CAGR, and it is not statistically decisive — but it is
  measured, whereas +2.97% was not.
- **The old model's error is structured, not noise**: too rich near the money,
  far too cheap in the wings — the signature of a missing skew.
- **The skew is not stable**, and the two natural ways to quantify it move in
  opposite directions in stress, so no single assumed number is defensible.

Do not claim profitability from any of this. The programme's measured sign is
negative; the sample is 5 entries; the uncertainty is large and unquantified at
this size.
