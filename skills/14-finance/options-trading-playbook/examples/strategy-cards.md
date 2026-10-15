# Strategy Cards

Concrete, testable cards. Each one is a complete hypothesis: a payoff corner, a
structure family, a regime filter, a numeric entry condition, an implemented target
and stop, a size rule, a prediction, and a kill criterion.

The schema and the reasoning behind each field are in
`../references/strategy-cards.md`. This file is the cards themselves.

**Every card is a hypothesis, not a recommendation.** No card here is asserted to be
profitable, and none has been validated on real data. The `verdict` on each card is
`payoff_check.py`'s output for the card's own stated inputs — an arithmetic result,
not a market result.

---

## How to read a card

| Field | Meaning |
|---|---|
| **Corner** | Which payoff corner, in `(b, p)` terms. The corner sets `p*`. |
| **Structure** | The options structure family. Construction is `options-strategist`'s job. |
| **Regime** | The market state in which the card is legal, named by the sibling that classifies it. |
| **Entry** | The numeric trigger. No adjectives. |
| **TP / SL** | The two exits, in R or in money, and the order type that implements each. |
| **Size** | Where the contract count comes from. Bands are `trade-sizing-recovery`'s. |
| **Prediction** | The `p` and `b` expected, and the `E_net` that follows. This is what a cycle grades. |
| **Kill** | The count and measure that retire the card. |
| **Check** | The `payoff_check.py` invocation and its real verdict. |

---

## Card 1 — `debit-2.5R-dir`

Directional debit spread in a trend regime, bought when implied is cheap.

| Field | Value |
|---|---|
| **Corner** | long premium: `b = 2.50`, `p* = 28.57%` |
| **Structure** | 2-leg call debit spread (bullish) / put debit spread (bearish) → `options-strategist` |
| **Regime** | trend regime per `technical-signals-engineer` (ADX > 25 with a signed slope) |
| **Entry** | trend confirmed **and** IV rank ≤ 30 |
| **TP** | 2.5R — a resting limit sell on the spread |
| **SL** | 1R — a resting stop-limit buy-to-close |
| **Size** | `R_max` from `../references/streak-survival-by-corner.md`, then the bands in `trade-sizing-recovery` |
| **Prediction** | `p ≈ 0.35`, `b = 2.50`, `E = +0.2250R` gross, `E_net = +0.2050R` at `c_R = 0.02R` |
| **Kill** | retire after 5 cycles with `E_net ≤ 0` |

**Check:**

```bash
py -3 scripts/payoff_check.py --tp 2.5 --sl 1.0 --p 0.35 --cost-r 0.02
```

Tool verdict: **POSITIVE** — `b = 2.5000`, `p* = 28.57%`, `E_net = 0.2050R`,
`n_req = 220.20`, `L = 13`, `R_max = 1.03%`. Full output:
`checks/01-positive-long-premium-2.5R.md`.

**Why the entry condition matters more than the structure.** At `b = 2.5`, five
points of win rate is worth `0.175R` `[COMPUTED]`: `p = 0.30` gives `E = +0.0500R`,
`p = 0.40` gives `E = +0.4000R`. The IV-rank gate is the source of `p`; without it
the card is buying the market's forecast at the market's price.

**Its weakness.** `L = 13` — a 13-loss streak is expected in 250 trades, so
`R_max = 1.03%` of equity per trade. This is the corner that needs the *smallest*
size, and it is the corner that feels the most exciting to trade.

---

## Card 2 — `credit-50-2x`

The popular credit card, priced exactly as written.

| Field | Value |
|---|---|
| **Corner** | short premium: `b = 0.25`, `p* = 80.00%` |
| **Structure** | 4-leg iron condor → `options-strategist` |
| **Regime** | ranging regime per `technical-signals-engineer` (ADX < 20, flat slope, ATR/close < 2%) |
| **Entry** | IV rank ≥ 50 **and** realised vol trailing implied |
| **TP** | 50% of the credit |
| **SL** | 2 × the credit |
| **Size** | `R_max` at the card's `p` |
| **Prediction** | `p ≈ 0.775`, `b = 0.25`, `E = −0.03125R` gross |
| **Kill** | retire after 5 cycles with `E_net ≤ 0` |

**Check:**

```bash
py -3 scripts/payoff_check.py --tp 0.5 --sl 2.0 --p 0.775
```

Tool verdict: **MARGINAL** — `b = 0.2500`, `p* = 80.00%`, `E = −0.03125R`.

**This card is negative at the win rate it predicts.** At `p = 0.80` exactly:

```bash
py -3 scripts/payoff_check.py --tp 0.5 --sl 2.0 --p 0.80
```

`E = 0.0000R`, `b* = 0.2500 = b`, `p* = 80.00% = p`. **Exactly break-even**, which is
why the popular card produces a flat-to-negative book. Full output:
`checks/03-break-even-credit-50-2x-at-80pct.md`.

**Do not repair this card by changing the target.** From 50%-of-credit/2×-credit to
25%-of-credit/2×-credit, `b` falls from 0.25 to 0.125 and `p*` rises from 80% to
88.9% — a worse card. The only lever that helps is the stop. See Card 3.

---

## Card 3 — `credit-50-1x`

The same corner, repaired with one number: the stop.

| Field | Value |
|---|---|
| **Corner** | short premium: `b = 0.50`, `p* = 66.67%` |
| **Structure** | 2-leg credit spread, or a 4-leg condor with a tighter stop → `options-strategist` |
| **Regime** | ranging regime, same as Card 2 |
| **Entry** | IV rank ≥ 50 **and** realised vol trailing implied |
| **TP** | 50% of the credit |
| **SL** | **1 × the credit** (the only change from Card 2) |
| **Size** | `R_max` at the card's `p` |
| **Prediction** | `p ≈ 0.70` — **lower than Card 2's**, because a tighter stop fires more often |
| **Kill** | retire after 5 cycles with `E_net ≤ 0` |

**Check, at Card 2's win rate first — to show the arithmetic, then the honest case:**

```bash
py -3 scripts/payoff_check.py --tp 0.5 --sl 2.0 --p 0.775   # the card as Card 2
py -3 scripts/payoff_check.py --tp 0.5 --sl 1.0 --p 0.775   # same p, tighter stop
py -3 scripts/payoff_check.py --tp 0.5 --sl 1.0 --p 0.70    # the honest p for this stop
```

| Command | `b` | `p*` | `E` | Verdict |
|---|---|---|---|---|
| `--sl 2.0 --p 0.775` | 0.250 | 80.00% | −0.03125R | MARGINAL (negative) |
| `--sl 1.0 --p 0.775` | 0.500 | 66.67% | +0.16250R | POSITIVE |
| `--sl 1.0 --p 0.70` | 0.500 | 66.67% | +0.05000R | POSITIVE |

**Read the caveat in row 2.** The `+0.16250R` is what the card pays *if* the 0.775
win rate survives a stop that is twice as tight. It will not:
`../references/the-iteration-protocol.md` calls this out as the exact reason a stop
change is a *new* card needing a *new* cohort tag and a *new* measurement. Row 3 is
the conservative version.

**Its weakness.** Row 3's `E = +0.05R` needs `n_req = 756` trades to grade at 2σ
`[COMPUTED]` — about three years at a retail pace. The card is real and the evidence
is expensive.

---

## Card 4 — `long-premium-cheap-implied`

Long premium, non-directional, bought only when implied is cheap.

| Field | Value |
|---|---|
| **Corner** | long premium: `b = 1.50`, `p* = 40.00%` |
| **Structure** | long straddle / long strangle, or a calendar → `options-strategist`, `advanced-options-structures` |
| **Regime** | low-IV regime; IV rank ≤ 25 |
| **Entry** | IV rank ≤ 25 **and** a dated catalyst identified (earnings, FOMC, FDA) |
| **TP** | 1.5R — resting limit on the structure |
| **SL** | 1R — resting stop on the structure |
| **Size** | `R_max` at the card's `p` |
| **Prediction** | `p ≈ 0.45`, `b = 1.50`, `E = 0.45 × 1.5 − 0.55 = +0.1250R` |
| **Kill** | retire after 5 cycles with `E_net ≤ 0` |

**Check:**

```bash
py -3 scripts/payoff_check.py --tp 1.5 --sl 1.0 --p 0.45 --cost-r 0.03
```

`b = 1.5000`, `p* = 40.00%`, `E = +0.1250R`, `E_net = +0.0950R`,
`se_E = 0.0787R`, `f* = 8.33%`. Tool verdict: **POSITIVE** — but note the margin:
`0.0950` vs `0.0787` is a narrow pass at 250 trades.

**Why the catalyst is part of the entry, not a hope.** A non-directional card pays
when realised exceeds implied. The catalyst is the mechanism by which that happens.
Without one, the card needs `p > 40%` from a market that is charging less than it
expects to move — the wrong way round. Note the `1.5R` target, not `2.5R`: a
straddle's exit is a movement target and it is reached less often than a directional
move. Setting `b` lower is the honest response.

---

## Card 5 — `symmetric-1R-1R` — the card that should not be traded

Included because it is the most common card in retail options, and the arithmetic
retires it.

| Field | Value |
|---|---|
| **Corner** | `b = 1.00`, `p* = 50.00%` |
| **Structure** | any 1:1 card |
| **Entry** | — |
| **TP / SL** | 1R / 1R |
| **Prediction** | `p` must exceed 0.50 net of cost |
| **Kill** | immediate — the corner requires an edge that a 1:1 payoff does not supply |

**Check:**

```bash
py -3 scripts/payoff_check.py --tp 1.0 --sl 1.0 --p 0.50
py -3 scripts/payoff_check.py --tp 1.0 --sl 1.0 --p 0.50 --cost-r 0.02
```

At `p = 0.50`: `E = 0.0000R`, `f* = 0.00%`, verdict **MARGINAL**. Add `c_R = 0.02R`
and `E_net = −0.0200R`: the sign is negative but the verdict is still **MARGINAL**
(`|−0.0200| < se_E = 0.0632`). **A 1:1 card is a below-zero card at a coin-flip win
rate**, because it pays a cost to hold a payoff with no compensation for it — and the
verdict band is wide enough that a decade of trading it would not settle the question.

**Note `f* = 0`.** Kelly says the optimal fraction is zero. No risk per trade makes a
zero-expectancy card profitable; sizing is a survival tool, not an edge.

---

## Card 6 — `micro-account-dir` — the card that is wrong for its size, not its math

Directional debit spread on a structure small enough that the ticket count dominates.

| Field | Value |
|---|---|
| **Corner** | long premium: `b = 2.50`, `p* = 28.57%` — **identical to Card 1** |
| **Structure** | 4-leg, or a narrow 2-leg spread on a small max loss |
| **Entry** | same as Card 1 |
| **R (`max loss`)** | **$15.00** |
| **Fee** | $0.65 per contract per ticket |
| **Prediction** | `p ≈ 0.35`, `b = 2.50`, `E = +0.2250R` gross |
| **Kill** | retire — the fee exceeds the edge |

**Check:**

```bash
py -3 scripts/payoff_check.py --tp 2.5 --sl 1.0 --p 0.35 \
    --fee-per-contract 0.65 --legs 4 --r-dollars 15
```

Tool verdict: **NEGATIVE**. `cost_per_trade = 0.65 × 4 × 2 = $5.20`,
`c_R = 5.20/15.00 = 0.3467R`, `E_net = 0.2250 − 0.3467 = −0.1217R`. The tool states
it plainly: *cost is not a rounding term here; it is the whole result.* Full output:
`checks/06-cost-turns-positive-into-negative.md`.

**The lesson is not "trade bigger".** On a `$500` max-loss structure the same fee is
`c_R = 0.0104R` and the card is POSITIVE at `+0.2146R`. The lesson is that **the fee
is set by the structure and `R` is set by the market, so structure size is a strategy
input, not an execution detail.** See
`../references/small-account-instrument-choice.md`.

---

## Card 7 — `rung-scaleout` — the card that pays a second opening fee

An exit-management rule, priced.

| Field | Value |
|---|---|
| **Structure** | 4-leg |
| **Fee** | $0.65 per contract per ticket |
| **Rule** | close in thirds (3 rungs) |
| **Fee per rung** | `4 × 0.65 = $2.60` |
| **Derived threshold** | `3 × 4 × 0.65 = $7.80` per spread — below this the rule is fee-negative |
| **Kill** | replace the 3-rung scale-out with a single close unless the remaining structure is worth more than $7.80 |

**Check:**

```bash
py -3 scripts/payoff_check.py --scaling-check --legs 4 \
    --fee-per-contract 0.65 --rung-split 3 --position-value 5.00
py -3 scripts/payoff_check.py --scaling-check --legs 4 \
    --fee-per-contract 0.65 --rung-split 3 --position-value 12.00
```

At a `$5.00` mark: **FEE-NEGATIVE** — each rung banks `$1.67` and pays `$2.60`. The
extra fee across the three rungs is `$5.20`, **exactly the round-trip fee of opening
the structure.** At a `$12.00` mark the split is fee-positive. Full output:
`checks/04-fee-negative-rung-scaling.md`.

---

## Cross-reference

| Card | Corner | `b` | `p*` | Prediction `p` | Verdict | Check file |
|---|---|---|---|---|---|---|
| 1 `debit-2.5R-dir` | long premium | 2.50 | 28.57% | 0.35 | POSITIVE | `checks/01-...md` |
| 2 `credit-50-2x` | short premium | 0.25 | 80.00% | 0.775 | MARGINAL (negative `E`) | `checks/03-...md` |
| 3 `credit-50-1x` | short premium | 0.50 | 66.67% | 0.70 | POSITIVE | `checks/05-...md` (same corner, thin edge) |
| 4 `long-premium-cheap-implied` | long premium | 1.50 | 40.00% | 0.45 | run it | — |
| 5 `symmetric-1R-1R` | symmetric | 1.00 | 50.00% | 0.50 | MARGINAL; sign negative with cost | — |
| 6 `micro-account-dir` | long premium | 2.50 | 28.57% | 0.35 | NEGATIVE | `checks/06-...md` |
| 7 `rung-scaleout` | — (exit rule) | — | — | — | FEE-NEGATIVE at `$5.00` | `checks/04-...md` |

**Two of these seven cards are the same corner with different verdicts** (1 and 6),
and the difference is entirely `R`: `$500` versus `$15`. **Two of them are the same
corner with different verdicts by `b`** (2 and 3), and the difference is entirely the
stop. Neither difference required a forecast.

---

## What is missing from these cards

- **None has been traded.** Every verdict is arithmetic on a stated prediction.
- **No `p` here is measured.** Each is a hypothesis for a cycle to grade.
- **No size is given in contracts.** `R_max` is a cap; the count is
  `trade-sizing-recovery`'s number.
- **No structure is specified to the strike.** That is `options-strategist`'s work,
  handed a payoff profile by these cards.
- **No card has a correlation allowance.** Five of these at once is one position;
  `options-risk-engineer` owns that question.
