# Break-Even Payoff for Credit Structures

This file is the credit-spread version of the pay-off question, worked as a
table so that a trader can look up their own card instead of re-deriving it. Every
number is `[COMPUTED]` from two formulas and nothing else:

```
p* = 1 / (1 + b)              break-even win rate, given the payoff ratio
b  = (TP money) / (SL money)  the payoff ratio, from the management rules
```

The `b` column below is derived from the **management rules**, because that is what
determines it. A credit spread's structure sets the maximum possible win and
maximum possible loss, but the *realised* `b` comes from where the exit orders sit.

---

## The table

Targets are stated as a fraction of the credit `C`; stops as a multiple of `C`.
`1R` is the money lost when the stop fires.

| Target | Stop | `b` (`[COMPUTED]`) | `p*` (`[COMPUTED]`) | `b*` at `p = 0.80` | Verdict on the card |
|---|---|---|---|---|---|
| 100% of `C` | 1× `C` | 1.000 | **50.0%** | 0.250 | Needs a coin flip; rare in practice because assignment risk eats the win |
| 75% of `C` | 1× `C` | 0.750 | **57.1%** | 0.250 | Achievable only with a measured win rate ≥ 57% |
| 50% of `C` | 1× `C` | 0.500 | **66.7%** | 0.250 | The most defensible retail card |
| 50% of `C` | 1.5× `C` | 0.333 | **75.0%** | 0.250 | Needs 75%; the extra stop width costs 8 points of win rate |
| 50% of `C` | 2× `C` | 0.250 | **80.0%** | 0.250 | **Exactly break-even at `p = 0.80`** |
| 50% of `C` | 3× `C` | 0.167 | **85.7%** | 0.250 | Needs 86% — outside the range most measured retail books report |
| 25% of `C` | 2× `C` | 0.125 | **88.9%** | 0.250 | Needs 89%; a 2-point win-rate error is fatal |
| 25% of `C` | 1× `C` | 0.250 | **80.0%** | 0.250 | Taking less profit without tightening the stop changes nothing |

Read the last two rows together. **Cutting the target in half while leaving the
stop where it is does not improve the card.** Moving from "50%/1×" to "25%/1×"
takes `b` from 0.50 to 0.25 and `p*` from 66.7% to 80.0%: the trader has given up
half the win to keep the same loss. The only lever that helps the credit corner is
the **stop**.

---

## The identity at `p = 0.80`

At any win rate, `b* = (1−p)/p`. At `p = 0.80`:

```
b* = (1 - 0.80) / 0.80 = 0.20 / 0.80 = 0.2500          [COMPUTED]
b  = 0.5 C / 2 C                        = 0.2500         [COMPUTED]
E  = 0.80 x 0.25 - 0.20                 = 0.0000 R       [COMPUTED]
```

The two numbers coincide. That coincidence is the entire explanation for the
observed retail experience of premium selling: a well-known card sits on its own
break-even point, so the *average* trader running it earns nothing before costs
and loses after them. It is not a bad strategy in the sense of being incoherent —
it is a strategy with no margin for error.

Verify it yourself:

```bash
py -3 scripts/payoff_check.py --tp 0.5 --sl 2.0 --p 0.80     # E = 0.0000, MARGINAL
py -3 scripts/payoff_check.py --tp 0.5 --sl 2.0 --p 0.70     # E = -0.1250, NEGATIVE
```

---

## Why the stop, and not the target

`p*` is a function of `b` alone, and `b` is the ratio of the two exits. Widening
the stop widens the denominator and drives `b` down. Tightening it does the
reverse. So the question is not "how much profit should I take" but "**how much
loss am I willing to take relative to the profit I am taking**".

The derived rule for premium selling:

> **The stop must be tighter relative to the credit than the target is.**
> Cutting at ≤ 1× the credit received, with a target at 50% of the credit,
> gives `b ≥ 0.5` and `p* ≤ 66.7%`. Cutting at 2× the credit with the same
> target gives `b = 0.25` and `p* = 80.0%`.

This is arithmetic, not preference. A trader who wants to sell premium and keep a
2×-credit stop has to bring an 80% win rate and prove it. A trader who wants a
67% requirement can have it by moving the stop — provided they accept that a
1×-credit stop will be hit more often, so the win rate they measure after the
change *will* differ from the one before it. **The trade-off is real and it moves
in both directions.** What the arithmetic removes is the illusion that there is a
card with a wide stop and a low requirement.

---

## The cost term on top

The table above is gross. Add `c_R = cost_per_trade / R_dollars` and the required
win rate rises again. Solve `p(b+1) − 1 − c_R = 0`:

```
p*_net = (1 + c_R) / (1 + b)                            [COMPUTED]
```

At `b = 0.25`:

| `c_R` | `p*_net` (`[COMPUTED]`) | Change from the gross 80.0% |
|---|---|---|
| 0.000 | 80.00% | — |
| 0.010 | 80.80% | +0.80 pp |
| 0.026 | 82.08% | +2.08 pp |
| 0.052 | 84.16% | +4.16 pp |
| 0.100 | 88.00% | +8.00 pp |

A four-leg structure at `$0.65` per contract per ticket pays `$5.20` round trip.
On a `$400` max-loss condor that is `c_R = 0.0130R` and the requirement rises to
`80.00% → 81.04%` `[COMPUTED]`. On a `$100` structure the same fee is
`c_R = 0.052R` and the requirement is `84.16%`. **The smaller the structure, the
higher the win rate you must bring to pay the same commission.** Cost does not
shrink with size; `R` does.

---

## Failure modes

1. **Failure mode — `b` is computed from the structure's max profit and max loss
   rather than from the exits.** A credit spread's max win is the credit and its
   max loss is the width minus the credit, but a 50%-of-credit target does not
   realise the max win. Computing `b = C/(W−C)` describes a card nobody trades and
   understates `p*` badly.
2. **Failure mode — the win rate is asserted from memory.** `p = 0.80` is a
   *measurement*, not a belief. With 40 trades the standard error at `p = 0.80` is
   `sqrt(0.8·0.2/40) = 0.063` `[COMPUTED]`; a 40-trade record cannot distinguish
   74% from 86%, and the whole band around 80% decides the card.
3. **Failure mode — the stop is described as "2× the credit" while the order sits
   at the structural max loss.** The two are different prices. If the realised
   average loss in R is 1.0 while the card says 2.0, the measured `b` will silently
   disagree with the intended one.
4. **Failure mode — a mid-flight stop change is counted as one cohort.** Trades
   taken before and after the stop moved belong to different `b` values. Pooling
   them measures neither.
5. **Failure mode — the target is treated as a certainty.** A 50%-of-credit target
   is only reached on the winners. Trades closed at 30%, at expiry, or by
   assignment are not the card.
6. **Failure mode — cost is left out of a small-structure comparison.** A trader
   comparing a `$100` condor to a `$400` condor on gross expectancy has compared
   the wrong numbers.
7. **Failure mode — the win rate is compared to 50% instead of to `p*`.** For a
   `b = 0.25` card, 50% is thirty points below break-even. "I win more than half"
   is not evidence of anything here.

---

## Worked check

```bash
py -3 scripts/payoff_check.py --credit 1.00 --width 5.00 \
    --tp-money 50 --sl-money 200 --p 0.80
```

Expected shape: `b = 0.2500`, `b* = 0.2500`, `p* = 80.00%`, `E = 0.0000R`,
`sd = 0.5000R`, `L = 4`, `R_max = 3.33%`, verdict `MARGINAL`. The full captured
output is `examples/checks/03-break-even-credit-50-2x-at-80pct.md`.

See also: `references/stop-and-target-arithmetic.md`,
`references/payoff-corners-for-options.md`,
`references/cost-drag-per-leg-and-per-rung.md`.
