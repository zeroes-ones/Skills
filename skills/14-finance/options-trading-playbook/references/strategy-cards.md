# Strategy Cards

A strategy card is the smallest complete statement of a tradeable hypothesis. It
fits on an index card because it contains seven fields and a prediction. This file
specifies the schema, works three cards end to end against `payoff_check.py`, and
states what makes a card *testable* rather than merely *stated*.

The cards themselves are in `examples/strategy-cards.md`. This file is the schema
and the reasoning behind it.

---

## The card schema

| Field | What it must contain | Why it is required |
|---|---|---|
| **Corner** | which payoff corner, in `(b, p)` terms | the corner determines `p*` before any trade is taken |
| **Structure** | the specific options structure, named | structure selection is `options-strategist`'s; the card must hand it a target |
| **Regime filter** | the state in which the card is legal, named by the sibling that classifies it | a card without an entry condition is being traded in every regime at once |
| **Entry condition** | the testable trigger, with a number | "when IV looks high" is not testable; "IV rank ≥ 50" is |
| **TP** | target in R or in money, with the exit order that implements it | a target no order implements is a description, not a rule |
| **SL** | stop in R or in money, with the exit order that implements it | the stop is the denominator of `b`; without it there is no `b` |
| **Size rule** | how many contracts, derived from `R_max` and the size bands | size belongs to `trade-sizing-recovery`; the card must point at the number |
| **Prediction** | the `p` and `b` you expect, and the `E_net` that follows | this is what the cycle measures against |
| **Kill criteria** | the condition that retires the card, with a count | a card without a kill criterion cannot be killed |

The **prediction** and the **kill criteria** are what separate a card from a wish.
A card with no prediction cannot be checked; a card with no kill criterion is
traded forever because nothing was ever specified that would stop it.

---

## Every card is a corner, and every corner has a price

The card does not choose the corner. The **exits** choose the corner, and the corner
sets the required win rate:

```
b  = TP / SL                    from the two exit levels
p* = 1 / (1 + b)                the win rate the card requires
```

So a card's `TP` and `SL` fields are not two independent preferences. They are one
decision with two numbers in it. Writing them down is what makes the card checkable;
`references/stop-and-target-arithmetic.md` derives the consequences.

| Card shape | `TP` | `SL` | `b` | `p*` |
|---|---|---|---|---|
| The popular credit card | 0.5 × credit | 2 × credit | 0.25 | **80.0%** |
| The defensible credit card | 0.5 × credit | 1 × credit | 0.50 | **66.7%** |
| The directional debit card | 2.5R | 1R | 2.50 | **28.6%** |
| The coin-flip card | 1R | 1R | 1.00 | **50.0%** |

Three of those four are live retail cards. Only one of them has a required win rate
that a measured retail book is likely to clear.

---

## Three worked cards

### Card A — directional debit spread, low-IV regime

| Field | Value |
|---|---|
| Corner | long premium, `b = 2.5` → `p* = 28.57%` |
| Structure | 2-leg call or put debit spread (structure selection → `options-strategist`) |
| Regime filter | trend regime per `technical-signals-engineer`; IV rank below the low-IV gate |
| Entry condition | trend confirmed **and** IV rank ≤ 30 |
| TP | 2.5R, implemented as a resting limit on the spread |
| SL | 1R, implemented as a resting stop-limit |
| Size rule | `R_max` from `references/streak-survival-by-corner.md`, then the size bands in `trade-sizing-recovery` |
| Prediction | `p ≈ 0.35`, `b = 2.5`, `E = +0.2250R` gross |
| Kill criteria | after 5 cycles with `E_net ≤ 0`, retire the card |

**Check it:**

```bash
py -3 scripts/payoff_check.py --tp 2.5 --sl 1.0 --p 0.35 --cost-r 0.02
```

Tool output: `b = 2.5000`, `p* = 28.57%`, `E_net = 0.2050R`, `n_req = 220.20`,
`L = 13`, `R_max = 1.03%`, verdict `POSITIVE`. Captured in full at
`examples/checks/01-positive-long-premium-2.5R.md`.

Note what the card's `p = 0.35` requires: the *entry condition* is where that win
rate comes from. The trend filter and the IV-rank gate are the mechanism, and they
are what the cycle tests.

### Card B — the popular credit card, priced as written

| Field | Value |
|---|---|
| Corner | short premium, target 0.5 × credit, stop 2 × credit → `b = 0.25`, `p* = 80.0%` |
| Structure | 4-leg iron condor (structure selection → `options-strategist`) |
| Regime filter | ranging regime per `technical-signals-engineer`; IV rank above the high-IV gate |
| Entry condition | IV rank ≥ 50 **and** realised vol below implied |
| TP | 50% of the credit |
| SL | 2 × the credit |
| Size rule | `R_max` at the card's `p` |
| Prediction | `p ≈ 0.78` — the win rate a condor book commonly reports |
| Kill criteria | retire on `E_net ≤ 0` after 5 cycles |

**Check it:**

```bash
py -3 scripts/payoff_check.py --tp 0.5 --sl 2.0 --p 0.78
```

At `p = 0.78`: `E = 0.78 × 0.25 − 0.22 = 0.195 − 0.220 = −0.0250R` `[COMPUTED]`.
The card **is a losing card at the win rate it predicts**. Making it work requires
either `p ≥ 0.80` (which is exactly break-even, `E = 0.0000R`) or a different `SL`.
The repair is in the `SL` field:

```bash
py -3 scripts/payoff_check.py --tp 0.5 --sl 1.0 --p 0.78
```

`b = 0.50`, `p* = 66.67%`, `E = 0.78 × 0.5 − 0.22 = +0.1700R` `[COMPUTED]`. The
card is positive at the *same* predicted win rate, with one number changed in one
field.

### Card C — the thin-edge card, and why it is retired before it is traded

| Field | Value |
|---|---|
| Corner | short premium, target 0.5 × credit, stop 1 × credit → `b = 0.50` |
| Prediction | `p ≈ 0.68` |
| Kill criteria | retire if `n_req` exceeds the trades the account can complete in one year |

**Check it:**

```bash
py -3 scripts/payoff_check.py --tp 0.5 --sl 1.0 --p 0.68
```

Tool output: `E = +0.0200R`, `se_E = 0.0443R`, `n_req = 4896.00`, `years_at_pace =
19.58`, verdict `MARGINAL`. Captured at `examples/checks/05-marginal-two-point-edge.md`.

The card is not negative and it is not wrong. It is **ungradeable inside a lifetime
of trading at a retail pace**. The kill criterion catches it at the desk rather than
after nineteen years.

---

## What makes a card testable

Four tests, in order. A card that fails any of them is not ready to trade.

1. **The `TP` and `SL` produce a `b`.** Two numbers, one ratio. If either field says
   "discretionary", there is no `b` and no `p*`.
2. **The `p` is a prediction, not a memory.** "Around 70%" is a memory. `p = 0.70`
   with the cycle count that produced it is a prediction.
3. **The entry condition has a number and a source.** "IV rank ≥ 50" is testable;
   "IV rank as classified by `technical-signals-engineer`" gives the source. Both are
   needed — a threshold with no classifier cannot be reproduced.
4. **The kill criterion is reachable.** "Retire if it loses money" is not reachable
   as written; "retire after 5 cycles with `E_net ≤ 0`" is a count and a measure.

---

## Failure modes

1. **Failure mode — the card has a `TP` and no `SL`.** Without a loss there is no
   `b`, no `p*`, and nothing for `payoff_check.py` to compute. The tool reports
   `b: n/a` with the reason rather than guessing.
2. **Failure mode — the card's `p` was chosen to make the card pass.** Running the
   checker backwards from a desired verdict is the selection problem in
   `references/overfitting-by-iteration.md`, performed on paper instead of in trades.
3. **Failure mode — the entry condition is descriptive.** "Sell premium when IV is
   high" cannot be reproduced by a second person or by the same person next month.
4. **Failure mode — the kill criterion is a feeling.** A card retires on a count and
   a measure, or it does not retire.
5. **Failure mode — the card is written after the position is opened.** The card is
   an entry artifact. A card written at exit is a rationalisation and cannot be
   tested.
6. **Failure mode — the regime filter is omitted because "it works in all regimes".**
   No corner in `references/regime-to-strategy-map.md` works in all regimes, and a
   card that claims to cannot be attributed when it fails.
7. **Failure mode — the size rule is left blank.** Size is where `R_max` becomes real.
   A card without a size rule delegates the decision to the moment of maximum
   emotional pressure — which is `trade-sizing-recovery`'s entire subject.
8. **Failure mode — two cards share a `setup` tag.** The cohorts merge and neither
   can be graded. The tag is the cohort key.
9. **Failure mode — the card's prediction is a single number with no interval.** Five
   points of win rate is worth `0.175R` on the `b = 2.5` card `[COMPUTED]`; a card
   whose prediction has no width cannot be honestly compared to a result.

---

## Worked check

```bash
# Card A as written, then Card B as written and repaired
py -3 scripts/payoff_check.py --tp 2.5 --sl 1.0 --p 0.35 --cost-r 0.02
py -3 scripts/payoff_check.py --tp 0.5 --sl 2.0 --p 0.78
py -3 scripts/payoff_check.py --tp 0.5 --sl 1.0 --p 0.78
```

See also: `references/payoff-corners-for-options.md`,
`references/stop-and-target-arithmetic.md`,
`references/the-iteration-protocol.md`,
`references/from-negative-to-positive-walkthrough.md`.
