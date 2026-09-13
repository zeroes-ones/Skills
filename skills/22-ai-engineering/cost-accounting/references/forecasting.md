# Forecasting

<!-- STANDARD: 3min -- unit economics to volume projections, bands and assumptions -->

## The rule

**Forecast from a measured unit, times realistic volume** (R6). Scaling multiplies cost; it does not
amortise it away. An extrapolation from an unmeasured baseline is a guess with decimal places.

## The formula

```text
period_cost = cost_per_unit × units_per_period × periods

where cost_per_unit is MEASURED (or tagged [ESTIMATED] with its assumption)
      units_per_period is the realistic volume, not the peak
      periods is the horizon
```

Four lines. The difficulty is not the arithmetic — it is that each input is a place to be
optimistic.

## The three inputs, and how each lies

### cost_per_unit

| Source | Quality |
|---|---|
| Measured median over ≥20 runs, same cohort | the only defensible basis |
| Measured mean | skewed by outliers; use the median |
| A single run | a sample of one |
| The cheapest observed run | a floor, presented as a typical value |
| A demo total | not a unit at all |

**Use the median, and state the p90 too.** The tail is where a forecast breaks: a workflow whose
median is $0.04 and p90 is $0.40 will blow through a budget built on the median alone.

### units_per_period

The input that is most often inflated, usually by the person who wants the project approved.

```text
Bad:  "we expect 10,000 users"            → users ≠ runs
Bad:  "peak capacity is 1,000/min"        → peak ≠ mean; and it is rarely sustained
Good: "240 users × 6 tasks/day × 21 days" → runs, derived from a workflow
```

**Derive it, do not assert it.** Units come from a user count times a per-user task frequency times
the period — so the assumptions are visible and each can be challenged separately.

### periods

Trivial, except that forecasts run for a year and prices do not. State the horizon and the
assumption about prices over it.

## The four scenarios

A single number is not a forecast; it is a hope with a decimal point.

| Scenario | cost_per_unit | units | Purpose |
|---|---|---|---|
| **Base** | measured median | derived realistic volume | the plan |
| **Worst** | p90 (tail) | volume ×1.5 | the number to survive |
| **Best** | p10 or a targeted improvement | volume ×0.8 | the number to aim at |
| **Stress** | p90 | volume ×1.5 **and** a price rise | what breaks the plan |

**The stress scenario is the one that matters in a budget conversation.** The question is never "what
if the plan holds" — it is "what if it doubles and the model gets dearer".

## Worked forecast

```text
Measured unit ([VERIFIED], 20 runs, <rev>):
  median cost/success       $0.0447
  p90 cost/success          $0.1180

Volume (derived, assumptions shown):
  240 users × 6 tasks/day × 21 working days      = 30,240 tasks/month
  success rate 76%                               → 22,982 successes/month

Base:   22,982 × $0.0447 = $1,027/month   → $12,324/year
Worst:  22,982 × $0.1180 = $2,712/month   → $32,544/year
Stress: $2,712 × 1.3 (price rise) = $3,526/month → $42,312/year
```

The spread — $12k to $42k — is the honest answer. Quoting only $12,324 is the failure mode.

## When the price is the uncertainty

For a long horizon, price is often a bigger unknown than volume:

| Price assumption | How to state it |
|---|---|
| Rates fixed for a contract term | cite the contract and the term |
| Rates follow list price | cite the page and the date; note prices generally move |
| A cheaper model is planned | state the model, the measured unit cost at its rate, and the *unmeasured* quality risk |
| Caching reduces cost | state the measured hit rate; a forecast on an assumed hit rate is an assumption |

**Never forecast a saving that has not been measured.** "Switching to model X will halve cost" is a
projection about a rate, not a measurement of an outcome — tag it `[ESTIMATED]` and say what would
confirm it.

## The break-even question

Often the useful output is not a total but a threshold:

```text
At what volume does this workflow stop being worth running?

revenue (or value) per success      $2.40
measured cost per success           $0.0447
gross margin per success            $2.3555

The workflow is worth running while cost_per_success < value_per_success.
The interesting number is the RATIO, not the total: a workflow at 2% of value
is fine at any volume; one at 90% is fragile to a price change.
```

**Report the ratio.** It survives volume changes, and it answers "is this still worth doing" without
a spreadsheet.

## Reporting shape

```text
Cost forecast — <workflow> — <horizon>

Unit cost basis: median $0.0447, p90 $0.1180  ([VERIFIED], 20 runs, <rev>, <price-date>)
Volume basis:    240 users × 6 tasks/day × 21 days = 30,240 tasks/month
                 success rate 76% → 22,982 successes/month    ([ESTIMATED] volume)

| Scenario | $/success | Volume | Monthly | Annual  |
|----------|-----------|--------|---------|---------|
| Base     | $0.0447   | 1.0×   | $1,027  | $12,324 |
| Best     | $0.0350   | 0.8×   | $  643  | $ 7,718 |
| Worst    | $0.1180   | 1.5×   | $4,068  | $48,815 |
| Stress   | $0.1534   | 1.5×   | $5,288  | $63,459 |

Assumptions: volume derived from usage assumptions above; prices held at the
<date> basis; caching hit rate unchanged; quality bar unchanged.
Confidence: unit cost is measured; volume is estimated; the price horizon is
the largest open risk.
```

The confidence line matters more than the table: it says which input a reader should challenge.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Unit from a single run | a sample of one, and usually a favourable one |
| Volume asserted, not derived | removes the assumptions a reviewer needs to challenge |
| One scenario | presents a hope as a plan; the first bad month discredits it |
| Median without the tail | the p90 is what breaks the budget |
| A saving assumed, not measured | a projection about a rate, presented as an outcome |
| Price horizon unstated | the largest risk is left invisible |
| No break-even ratio | cannot answer "is this still worth doing" as prices move |
| Forecast from a demo total | not a unit; not a forecast |

## Checklist

- [ ] The unit cost is measured, with its run count, revision and p90 (R6)
- [ ] Volume is derived from stated assumptions, not asserted (R6)
- [ ] At least base, worst and stress scenarios are reported
- [ ] The price horizon and its assumption are stated
- [ ] No unmeasured saving is included without an `[ESTIMATED]` tag and a confirmation path
- [ ] The break-even ratio (cost per success ÷ value per success) is reported
- [ ] The confidence of each input is stated, so a reviewer knows what to challenge
- [ ] The forecast is revisited when the measured unit or the price basis changes
