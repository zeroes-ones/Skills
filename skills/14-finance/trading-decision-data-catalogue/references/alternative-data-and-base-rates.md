# Alternative Data and Base Rates

Alternative data is the class where **the seller's incentive and the buyer's evidence are the same
document.** That is not an accusation of fraud; it is a statement about degrees of freedom. This file
is about the two things that make an alt-data panel worth its price: a holdout the seller did not
choose, and a base rate written before the results were seen.

## §1 — The Categories, and What Each Can Actually Support

| Category | Typical form | What it can support | What it cannot |
|---|---|---|---|
| **Card / transaction panels** | aggregated spend by merchant or brand | a revenue-direction nowcast, with coverage and panel-drift caveats | a margin or an earnings claim |
| **Web and app traffic** | sessions, installs, engagement | a demand-direction nowcast | revenue per user, or a profitability claim |
| **Geolocation** | foot-traffic counts | a store-level activity nowcast | in-store conversion or basket size |
| **Email and receipt parsing** | anonymised e-receipts | a basket-composition read | universe representativeness |
| **Job postings** | counts by role and geography | a hiring-direction read, which is a lagging indicator | a headcount level |
| **Satellite / imagery** | parking-lot, storage, construction | a physical-activity read | anything about willingness to pay |
| **Shipping and port data** | container and vessel counts | a goods-flow read | a services read |
| **Sentiment and text** | see [text-and-language-data.md](text-and-language-data.md) | an aggregated tone measure | a causal claim |

**Every row shares one property: the panel measures a *sample*, and the target is a *population*.**
The gap between them is where alt data fails, and it fails silently, because the sample is all the
vendor has.

## §2 — The Seller's-Holdout Problem

The chain of decisions a panel vendor makes before you see a backtest:

1. **Universe** — which names are in the sample, chosen after seeing which ones worked.
2. **Period** — which years are shown, chosen after seeing where the strategy performed.
3. **Metric** — Sharpe, hit rate, information coefficient, chosen after seeing which is flattering.
4. **Rebalance rule** — the strategy's turnover, chosen after seeing the transaction-cost impact.
5. **The exclusion list** — names quietly dropped for data-quality reasons, which are often the names
   that hurt.

**Each of those is a degree of freedom, and all five lean the same way**, because the seller's
revenue depends on the backtest looking good. This is not dishonesty; it is selection pressure.

### 2.1 — The three-step test

```
1. Pick YOUR OWN holdout period, before reading the seller's material.
2. Ask for a point-in-time sample of that period, with the vendor's own data dictionary.
   → if the vendor cannot supply a point-in-time sample, the panel is NOT testable
3. Re-run on your period. Compare to the base rate, not to zero.
```

**If the seller's period cannot be replaced because the vendor will not supply other periods, the
panel is inadmissible as evidence.** That is the whole test, and it costs nothing to run.

### 2.2 — The one question that disqualifies a panel fastest

*"What was the panel's coverage of this name in this period, and how did that coverage change?"*

A panel whose coverage changes over the backtest period can produce a strategy out of coverage alone,
because a growing panel looks like a growing signal.

## §3 — Base Rates: Define Before Looking

A base rate is **how often the event happens in the population, unconditionally.** It is the only
comparison that makes a hit rate meaningful.

### 3.1 — Why 50% is the wrong benchmark

A hit rate of 62% against a coin flip looks like an edge. Against a base rate of 65% — which is what
you get if the event is simply "the stock went up" in an uptrend — it is a worse-than-random signal
wearing a good number.

### 3.2 — Four base rates to fix before any signal test

| Base rate | Definition | Why it is needed |
|---|---|---|
| **Unconditional** | how often the event happens over the full sample | the floor any signal must beat |
| **Conditional on the regime** | how often it happens within each of the four regimes | the number that matters when the regime changes |
| **Conditional on liquidity and size** | how often it happens within the tradable universe actually under test | small-cap rates are not large-cap rates |
| **Conditional on the horizon** | how often it happens within the holding period | a 10-day rate and a 250-day rate are different quantities |

### 3.3 — The pre-commitment rule

**Write the base rate down, with a timestamp, before loading the signal's output.** The order is the
entire difference between a test and a description, and no amount of later honesty repairs it. If the
document shows results first, re-run it.

## §4 — Sample Size, Stated as Arithmetic

The arithmetic below is `[COMPUTED]` on stated hypothetical inputs. It exists to make the precision
claim checkable, not to assert a market fact.

**Rule of thumb used here:** a rough standard error for a hit rate is `sqrt(p(1−p)/n)`, and a
"±2 standard errors" band is `2 × sqrt(p(1−p)/n)`.

| Stated hit rate | Sample size `n` | ±2 SE band `[COMPUTED]` | Verdict against a 55% base rate |
|---|---|---|---|
| 60% | 100 | `2 × sqrt(0.60 × 0.40 / 100) = 2 × 0.0490 = ±9.80pp` | indistinguishable from the base rate |
| 60% | 400 | `2 × sqrt(0.60 × 0.40 / 400) = ±4.90pp` | still overlapping |
| 60% | 1,000 | `2 × sqrt(0.60 × 0.40 / 1,000) = ±3.10pp` | marginal |
| 60% | 2,500 | `2 × sqrt(0.60 × 0.40 / 2,500) = ±1.96pp` | distinguishable |

**The implication:** a signal tested on 100 observations cannot support a claim of a 5-percentage-
point edge, and most vendor demonstrations are in that range. **A backtest is not a sample because it
is long; it is a sample because it has independent observations, and overlapping trades are not
independent.**

## §5 — Ranked: Alt-Data Categories for a Trading Decision

| Rank | Category | Verdict |
|---|---|---|
| 1 | **Job postings** | free or cheap, verifiable against the company's own careers page, lagging but honest about being lagging |
| 2 | **Shipping and port data** | free sources exist (see [free-and-underused-sources.md](free-and-underused-sources.md)), physical, hard to fake |
| 3 | **Web and app traffic** | useful as a *direction* nowcast with an explicit coverage caveat |
| 4 | **Card panels** | useful, expensive, and the panel-drift problem is chronic |
| 5 | **Geolocation** | useful for a narrow set of physical retailers; poor coverage elsewhere |
| 6 | **Email and receipt parsing** | interesting, small universes, representativeness unknown |
| 7 | **Satellite imagery** | expensive, high skill floor, and the interpretive step is where the errors are |
| 8 | **A panel sold with the vendor's backtest as its evidence** | **inadmissible until re-run on a period you chose** |

## §6 — Ten Failure Modes in Alt Data and Base Rates

1. **The seller's holdout treated as independent verification.** Detection: whose period is it?
2. **A base rate written after the results.** Detection: check the document order.
3. **A hit rate compared to 50% instead of the base rate.** Detection: is the base rate printed next
   to the hit rate? If not, the comparison was to a coin.
4. **Overlapping observations counted as independent.** Detection: divide the number of trades by the
   overlap factor before computing a standard error.
5. **Panel coverage changing across the backtest period.** Detection: ask for coverage by name by
   period.
6. **Panel drift mistaken for a change in the world.** Detection: compare the panel's own
   composition change against the signal's change.
7. **Small-capillarity assumed to hold in large caps.** Detection: state the universe explicitly.
8. **An unconditional base rate applied in a downturn.** Detection: recompute within the current
   regime.
9. **A vendor metric chosen after the fact.** Detection: ask what the metric was before the test.
10. **A panel's own data dictionary never read.** Detection: was the vendor's data dictionary
    requested? A panel without a dictionary cannot be audited.

**Source:** the panel-category table describes the general form of each category as sold in the
market and asserts no coverage statistic for any vendor; the arithmetic in §4 is `[COMPUTED]` from
the stated formula on the stated hypothetical inputs; the base-rate definitions are standard
statistical constructs. **No commercial alternative-data panel is named or priced as verified in this
skill** — read the vendor's own methodology document and data dictionary before use.
