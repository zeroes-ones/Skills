# Cost drag and stop distance

Cost is a first-class term in the expectancy, and in equity it is a small one — small enough that it
is usually ignored, which is fine at a 5% stop and lethal at a 0.2% stop. This file derives the term,
shows what it depends on and what it does not, and works the break-even cost for the corners.

## 1. The term, derived

```
c_R          = round_trip_cost / R_dollars                  cost per trade, in R
round_trip   = notional * bps / 10000                        commission + fees + spread
R_dollars    = notional * stop_pct / 100                     planned risk in currency
stop_pct     = 100 * (entry - stop) / price                  stop distance, percent of price
```

Substituting and cancelling:

```
c_R = [ notional * bps/10000 ] / [ notional * stop_pct/100 ]

    = (bps/10000) * (100/stop_pct)

    = bps / (100 * stop_pct)
```

**The notional cancels.** `c_R` depends on the cost *rate* and the stop distance *as a fraction of
price*, and on nothing else:

- not on account size,
- not on share count,
- not on price,
- not on the instrument's liquidity, except insofar as liquidity sets the spread that goes into `bps`.

That is a surprisingly strong statement, and it is why a small account and a large account paying the
same cost rate have identical cost drag in R at the same stop distance.

## 2. The table

Cost drag in R, for a range of round-trip cost rates and stop distances.

| stop distance (% of price) | 1 bps | 5 bps | 10 bps | 25 bps |
|---|---|---|---|---|
| 5.0% | 0.002000R | 0.010000R | 0.020000R | 0.050000R |
| 3.0% | 0.003333R | 0.016667R | 0.033333R | 0.083333R |
| 2.0% | 0.005000R | 0.025000R | 0.050000R | 0.125000R |
| 1.0% | 0.010000R | 0.050000R | 0.100000R | 0.250000R |
| 0.5% | 0.020000R | 0.100000R | 0.200000R | 0.500000R |
| 0.2% | 0.050000R | 0.250000R | 0.500000R | 1.250000R |

Read it as a ratio against `E`. A `b = 2`, `p = 0.40` card has `E = +0.200000R`. At a 5.0% stop and
5 bps, `c_R = 0.010000R` consumes 5% of `E`. At a 0.5% stop and the same 5 bps, `c_R = 0.100000R`
consumes **50%** of `E`. At a 0.2% stop it consumes 125% and the card is a net loser.

## 3. The worked comparison the skill's checks ship

`examples/checks/04-cost-sensitive-tight-stop.md` runs one card twice, changing only `--stop-pct`:

```
b = 2.0, p = 0.45, E = +0.350000R, 5 bps round trip, sl = 1.0R

stop 0.10% of price : c_R = 5/(100*0.10)  = 0.500000R  -> E_net = -0.150000R  NEGATIVE
stop 1.00% of price : c_R = 5/(100*1.00)  = 0.050000R  -> E_net = +0.300000R  POSITIVE
stop 5.00% of price : c_R = 5/(100*5.00)  = 0.010000R  -> E_net = +0.340000R  POSITIVE
```

Same entries. Same win rate. Same assumed cost rate. **A fiftyfold difference in the cost term, and a
sign flip, from the stop distance alone.**

## 4. The break-even cost, derived

Set `E_net = E − c_R = 0`:

```
c_R* = E
```

The break-even cost **is** the expectancy. Two consequences follow immediately.

**Consequence 1 — the break-even stop distance.** Substituting `c_R = bps/(100*stop_pct)`:

```
bps / (100 * S*) = E       =>       S* = bps / (100 * E)
```

`S*` depends only on the cost rate and on `E` — never on the stop you chose. It is the **tightest
stop** at which the card still pays at that cost rate. Worked for each corner at 5 bps:

| Corner | `E` | `S* = 5/(100*E)` | Reading |
|---|---|---|---|
| `b = 3`, `p = 0.40` | +0.600000R | **0.083333%** | a trend corner tolerates a stop as tight as 0.083% of price |
| `b = 2`, `p = 0.45` | +0.350000R | **0.142857%** | 1.7x tighter than the trend corner's limit |
| `b = 2`, `p = 0.40` | +0.200000R | **0.250000%** | the break-even stop check 4 ships |
| `b = 0.75`, `p = 0.65` | +0.137500R | **0.363636%** | a thin corner tolerates the tightest stop of any positive card |
| `b = 1`, `p = 0.45` | −0.100000R | **none** | `E < 0`, so no stop distance breaks even |
| `b = 0.333333`, `p = 0.62` | −0.173333R | **none** | the disposition corner is already negative |

**The ordering is the strategic conclusion.** A larger `E` **lowers** `S*`, so a big-`E` corner keeps
paying *even when the stop is forced very tight*; a thin-`E` corner needs a wide stop to survive cost.
That is why a trend corner can be traded on a tight ATR stop and a mean-reversion corner cannot, and
the reason is arithmetic, not taste.

**Consequence 2 — cost shifts the mean, not the spread.**

```
net outcomes are (b - c_R) and (-1 - c_R)
sd_net^2 = p*(b - c_R - E_net)^2 + (1-p)*(-1 - c_R - E_net)^2
         = p*(b - E)^2 + (1-p)*(-1 - E)^2          because E_net = E - c_R
         = sd^2
```

`sd` is unchanged by cost. So a cost increase moves `E` down and leaves `sd` where it was, which
means `n_req = 4*(sd/|E|)^2` **rises** — the sample you need grows as the net edge shrinks. Cost does
not make the strategy noisier; it makes the signal smaller against the same noise. Check 4's wide-stop
run makes this visible: `n_req = 77.076` at `E_net = +0.340000R`.

## 5. What `bps` actually contains

`bps` is the **round trip** — entry and exit — as a fraction of the traded notional, times 10,000. It
is the sum of:

| Component | Typical scale | Notes |
|---|---|---|
| Commission | often `$0` for US listed equities at retail brokers; otherwise a per-share or per-trade fee | a per-share fee is *not* proportional to price, so it does not fit the bps model cleanly — convert it to bps at the position's notional before using this arithmetic |
| Regulatory and exchange fees on the sell side | small, on the order of a fraction of a basis point | schedule-dependent, not something this repository can state |
| **Bid-ask spread, paid twice** | usually the largest component | a 1-cent spread on a `$50` stock is 2 bps *per side*; on a `$5` stock the same 1 cent is 20 bps per side |
| **Slippage** | unbounded, and zero only in the model | a market order into a thin book pays more than the quoted spread; a stop order that gaps pays much more |

Two honesty notes:

1. **This file cannot give you a bps figure for your account.** Commission schedules, fee schedules
   and spreads are account-, venue- and instrument-specific and change. Compute your own from a
   statement and a few recorded fills, then put that number into `--cost-bps`.
2. **Slippage is not modelled by any part of this skill.** A `−1R` loss is `−1R` in the algebra and
   can be `−1.4R` in the account. If `payoff_check.py --from-log` reports a realised average loss
   materially worse than `−1.0R`, the difference *is* slippage and gap-through, and it belongs in the
   `cost` column rather than being ignored.

## 6. Why equity is cost-forgiving, and where that stops being true

Compared with the alternatives — options with wider relative spreads and per-contract fees, futures
with per-contract fees and roll cost, crypto with maker/taker tiers — a liquid US equity or ETF
round trip is cheap, often in the low single-digit basis points. At a swing-trade stop distance of
2–8% of price, `c_R` is `0.001–0.025R` against expectancies of `0.14–0.60R`. Cost is then a rounding
detail, and treating it as the main problem is a misdiagnosis.

It stops being a rounding detail exactly when the stop is forced tight:

| Situation | Typical `stop_pct` | `c_R` at 5 bps | Verdict on cost |
|---|---|---|---|
| Swing / position trade, 2–8% stop | 2.0–8.0% | 0.006–0.025R | negligible: under 15% of a thin `E` |
| Intraday, 0.5–1.5% stop | 0.5–1.5% | 0.033–0.100R | material: 17–70% of a `b = 0.75`, `p = 0.65` `E` |
| Scalp, under 0.3% stop | < 0.3% | > 0.167R | dominant: the cost term exceeds most equities' entire `E` |
| Illiquid small-cap, wide spread | any | any | the spread dominates at every stop distance |

**Derived strategic conclusion.** `c_R = bps/(100*stop_pct)` is a *hyperbola* in `stop_pct`. Doubling
the stop halves the cost drag; halving the stop doubles it. There is no regime in which a tight stop
is free. So:

> **A tight-stop equity strategy is a cost strategy. A wide-stop equity strategy is not.** If the
> card's stop sits below about 1% of price, `c_R` is one of the three terms in the expectancy and
> must be computed on every card. Above about 3%, it usually is not, and the interesting terms are
> `p` and `b`.

## 7. The five-step cost routine

```
1. Measure your own all-in round-trip bps from 20 recorded fills.
2. Convert the card's stop to a percent of price: stop_pct = 100*(entry-stop)/price.
3. c_R = bps / (100 * stop_pct).
4. E_net = E - c_R.     If E_net <= 0, the card is dead at this stop distance.
5. S* = bps / (100 * E).  If your intended stop is tighter than S*, the card is dead too.
```

Run it with `payoff_check.py --cost-bps <your bps> --stop-pct <the card's stop>`, and read the
`break-even cost` block, which prints `c_R*`, `E_net` and `S*` together.

## Cross-references

- The corners whose `E` sets `S*`: `payoff-corners-for-equities.md`
- Where the stop distance comes from: `stop-and-target-arithmetic.md`
- The shipped two-run check: `../examples/checks/04-cost-sensitive-tight-stop.md`
- Liquidity and exit-cost planning, which is not this skill's: `equity-risk-and-capital-engineer` →
  `references/liquidity-and-exit-cost-planning.md`
- The datasets you might buy to measure your own cost: `trading-decision-data-catalogue`
