# Payoff Corners for Options

Every options strategy lands in one of a small number of **payoff corners**. A
corner is defined by two numbers and nothing else: the payoff ratio `b` (average
win ÷ average loss, in R) and the win rate `p`. Everything a trader believes
about a strategy — "income", "convexity", "theta" — is downstream of those two.
This file maps the corners, derives each one's break-even win rate from its own
management rules, and states which corners are structurally hard.

Throughout: `1R` is the money lost per trade when the stop fires. `E = p·b − (1−p)`
is the expectancy per trade in R. `p* = 1/(1+b)` is the break-even win rate.
`b* = (1−p)/p` is the break-even payoff. Every number below is `[COMPUTED]` from
that algebra; none is a market statistic, and none is a forecast.

---

## The map

| Corner | Structures that express it | Typical `b` under mechanical management | `p*` at that `b` | What has to be true |
|---|---|---|---|---|
| **Short premium, wide management** | short put / credit spread, target 50% of credit, stop 2× credit | 0.25 | **80.0%** | win rate ≥ 80% |
| Short premium, wide management, tighter stop | same, stop at 1× credit | 0.50 | **66.7%** | win rate ≥ 67% |
| Short premium, wide management, mid stop | same, stop at 1.5× credit | 0.333 | **75.0%** | win rate ≥ 75% |
| Short premium, defined-risk condor | iron condor, target 50% of credit, stop at 2× credit | 0.25 | **80.0%** | win rate ≥ 80%, plus no trending regime |
| Long premium, directional | long call / long put / debit spread, 1R stop, 2.5R target | 2.50 | **28.6%** | win rate ≥ 29% and a directional catalyst |
| Long premium, symmetric | same, 1R stop, 1R target | 1.00 | **50.0%** | win rate ≥ 50% — a coin flip you do not have |
| Long premium, cheap-implied | same with an IV-rank gate | 2.50 | **28.6%** | realised vol > implied vol |
| Calendar / diagonal | term-structure expression, 1R stop, 1.5R target | 1.50 | **40.0%** | front-month IV > back-month IV, and the underlying stays put |
| Ratio / backspread | long premium with positive convexity, 1R stop, 4R target | 4.00 | **20.0%** | win rate ≥ 20% and a tail move |
| Collar / covered call | premium against stock, capped upside | 0.20–0.40 | **71–83%** | win rate ≥ 71–83%, and stock you wanted anyway |

The last row is why covered calls feel so good and pay so little: capping the
upside while keeping the downside *is* a `b ≈ 0.3` corner, and a `b = 0.3` corner
needs a `p ≈ 0.77`.

---

## Deriving the credit row, step by step

This is the arithmetic the skill is built on. Take a credit spread with credit
`C`, managed the way the retail options literature most often prescribes.

```
target  = 50% of the credit  = 0.5 C
stop    = 2 x the credit     = 2.0 C
b       = win / loss         = 0.5 C / 2.0 C = 0.25        [COMPUTED]
p*      = 1 / (1 + b)        = 1 / 1.25 = 0.80             [COMPUTED]
b*      = (1 - p) / p        = 0.20 / 0.80 = 0.25          [COMPUTED]
```

Note that `b*` and `p*` are the *same statement*. At `p = 0.80` and `b = 0.25`:

```
E = 0.80 x 0.25 - 0.20 = 0.20 - 0.20 = 0.0000 R            [COMPUTED]
```

**Exactly break-even.** Not approximately — identically. The popular management
rule puts a premium-selling book on the knife edge, and any cost, any slippage,
and any win rate below 80% moves it to the losing side. This is the arithmetic
answer to "why do I keep losing on credit spreads": the card as written needs an
80% win rate, and the trader has not measured theirs.

Now tighten the stop and watch `p*` fall:

```
stop = 1.0 C :  b = 0.5 C / 1.0 C = 0.50  ->  p* = 1/1.50 = 0.667   [COMPUTED]
stop = 1.5 C :  b = 0.5 C / 1.5 C = 0.333 ->  p* = 1/1.333 = 0.750   [COMPUTED]
stop = 2.0 C :  b = 0.5 C / 2.0 C = 0.25  ->  p* = 1/1.25  = 0.800   [COMPUTED]
```

The stop is a **rules change**, available today, with no forecasting. Moving it
from 2× to 1× the credit moves the required win rate from 80% to 67% — thirteen
percentage points of required skill, bought with one instruction.

---

## Deriving the long-premium rows

Long premium inverts the problem. The loss is normally the debit paid (1R) and
the win is whatever the move delivers.

```
1R stop, 2.5R target : b = 2.5 -> p* = 1/3.5  = 0.2857      [COMPUTED]
   at p = 0.35       : E = 0.35 x 3.5 - 1 = 1.225 - 1 = +0.225 R   [COMPUTED]
1R stop, 1R target   : b = 1.0 -> p* = 1/2.0  = 0.5000      [COMPUTED]
   at p = 0.50       : E = 0.50 x 2 - 1 = 0.0000 R          [COMPUTED]
1R stop, 4R target   : b = 4.0 -> p* = 1/5.0  = 0.2000      [COMPUTED]
```

The middle row is the trap. A 1:1 long-premium card is a coin flip at
break-even, and the options market does not hand out coin flips — it charges
theta for the privilege of holding one. A 1:1 structure with a positive edge
requires `p > 0.50`, and a directional signal that wins more than half the time
after the spread is a hard asset to hold.

The 2.5R row is the one with room: `p* = 28.6%`, and at `p = 0.35` the expectancy
is `+0.225R`. This is why long premium is not "worse than premium selling" — it is
a *different corner* with a different required input.

---

## Which lever to fix first

Differentiating `E = p·b − (1−p) = p(b+1) − 1`:

```
dE/dp = b + 1        [COMPUTED]
dE/db = p            [COMPUTED]
ratio = (dE/dp) / (dE/db) = (b + 1) / p              [COMPUTED]
```

At the credit corner's `b = 0.25`, `p = 0.80`: `(1.25)/0.80 = 1.5625`. One
percentage point of win rate is worth 1.56 percentage points of payoff ratio.
At the long-premium corner's `b = 2.5`, `p = 0.35`: `3.5/0.35 = 10`. One point of
win rate is worth **ten** points of payoff.

So the win rate looks like the stronger lever. But it is not the lever to reach
for first, and the reason is operational rather than mathematical:

- **`b` is a rules change.** Setting the stop at 1× the credit instead of 2× is
  an instruction you can write on a card and follow tomorrow.
- **`p` is a signal.** Raising it means finding better entries — new information,
  new data, new work, and a measurement problem to prove it moved.

**Fix the payoff first.** It is the lever you can actually pull, it is free, and
it moves `p*` immediately. Only after the corner's payoff has been set to the best
available value does a win-rate question become the right question.

---

## Where the corners fail

1. **Failure mode — the high-p/low-b corner fails on regime, not on win rate.**
   A `b = 0.25, p = 0.82` book can be genuinely positive in a range-bound market
   and catastrophically negative in a trending one, because the losses arrive
   together. The win rate is honest and the corner still dies.
2. **Failure mode — the low-p/high-b corner fails on sample size.** At
   `p = 0.35, b = 2.5`, `n_req = 4(sd/|E|)² = 220.20` trades to see the edge at
   two sigma `[COMPUTED]`. At 250 trades a year that is 0.88 years of *pure*
   evidence — and only if the corner is traded exclusively.
3. **Failure mode — a corner is measured on too few trades to grade.** A book of
   30 trades from either corner has a win-rate standard error of roughly
   `sqrt(p(1-p)/30)`: about `0.045` at `p = 0.80` and `0.087` at `p = 0.35`
   `[COMPUTED]`. Neither resolves the question the trader is asking.
4. **Failure mode — the corner is stated with a loss that is not the stop.** A
   credit spread's structural max loss and its stop are different numbers. If `R`
   is the max loss while the stop sits at 2× the credit, then the realised
   average loss in R is not 1 and every result below it is wrong.
5. **Failure mode — the corner is chosen because it feels safe.** Short premium
   feels safe because it wins often. That is a description of the corner, not a
   reason to trade it.
6. **Failure mode — the corner is switched before it is graded.** Two corners
   traded alternately produce a mixture; a mixture is not a corner, and the
   break-even rate of a mixture is not the break-even rate of either component.

---

## Using this file

Read the map as a set of tradeable corners with published prices. Then run
`scripts/payoff_check.py` on the specific card — with the stop and target you
will actually use, not the ones in the marketing — and see which side of `p*`
your measured win rate sits on. The file tells you what the corner costs. Only
your own log can tell you whether you can afford it.

See also: `references/break-even-payoff-for-credit-structures.md`,
`references/stop-and-target-arithmetic.md`, `references/streak-survival-by-corner.md`.
