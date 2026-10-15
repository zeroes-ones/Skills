# The Iteration Protocol

How a negative-expectancy options book becomes a positive one — as a protocol, not
as advice. This is the same protocol
`references/from-negative-to-positive-walkthrough.md` walks through
case by case, and the same shape `edge-and-payoff-engineering` uses on a realised
ledger, so a cycle can be read by either skill without translation.

The protocol exists for one reason: **to stop self-deception.** It is not designed
to find an edge. It is designed to make the absence of one visible before more
capital is spent on it.

---

## The seven steps

### 1. Pre-register the hypothesis

Before the cycle, write down:

- **Which lever** you are changing: `p` (win rate), `b` (payoff), or `c_R` (cost).
- **The direction you predict** the change moves it.
- **The number you expect** afterwards.

One sentence, dated, written before the first trade of the cycle. Example:

> Cycle 3, 2026-11-02. Lever: `b`. Change: credit-spread stop from 2× the credit to
> 1× the credit, target unchanged at 50%. Prediction: realised `b` rises from
> ≈0.25 toward ≈0.50 and the measured win rate falls from ≈0.78 toward ≈0.68.
> Predicted `E`: from `−0.031R` to between `−0.02R` and `+0.02R`.

**Mechanical trigger for skipping this step:** you cannot state which of `p`, `b`,
or `c_R` the change targets. If the change could plausibly move two of them, it is
not one change; see step 2.

### 2. Change ONE thing per cycle

Two changes and you learn nothing. If the stop moves *and* the entry filter
tightens, a rise in `E` cannot be attributed. Worse, the two changes may work
against each other: a tighter stop lowers `p`, a better entry filter raises it, and
the sum is uninterpretable.

The three levers, with what each one actually is:

| Lever | What changing it means | Available today? | Requires a forecast? |
|---|---|---|---|
| `b` | Change a stop or a target price on the card | Yes | No |
| `c_R` | Change leg count, rung count, or structure size | Yes | No |
| `p` | Change the entry condition, filter, or instrument | Yes, but it is a research project | Yes |

Two of the three are free. Start there.

### 3. A cycle is `n_req` trades — do not measure earlier

`n_req = 4(sd/|E|)²` is the number of trades at which the edge is roughly two
standard errors from zero. Measure at `n_req`, not at a round number and not when
the book feels good.

The failure this rule prevents is **peeking**. A book that is measured every week
will show a positive stretch in any quarter of its existence; the trader reads the
stretch as evidence, sizes up, and re-measures after the next losing run. The
arithmetic in `references/overfitting-by-iteration.md` shows exactly how expensive
that habit is.

If the cycle would take longer than you are willing to trade it, that is a finding:
**the edge is too thin to grade, and that is a reason to change the card, not the
sample rule.**

### 4. Hold out by time — 70 / 30

Fit on the first 70% of the cycle's trades. Check on the last 30%. Never re-fit on
the holdout.

```
cycle trades:  |---------------- fit 70% ----------------|---- holdout 30% ----|
```

Concretely: if `n_req` is 40, the first 28 trades define the parameters and the
last 12 test them. If the holdout's expectancy and the fit's expectancy disagree in
sign, the fit did not generalise, and the cycle is a failure regardless of the
pooled number.

Time holds out better than random splits for a trading book, because the market
regime in the second half is not the regime in the first. A random split leaks the
future into the past.

### 5. Count the cycles and raise the bar (Bonferroni)

Every cycle is a test. `m` tests at a nominal 5% level have an expected number of
false positives of `0.05m`. To hold the family-wide error rate at 5%, test each
cycle at

```
alpha_adjusted = 0.05 / m            two-sided                    [COMPUTED]
```

In standard-error terms, the threshold on `|E_net| / se_E`:

| Cycles `m` | `alpha_adjusted` | Two-sided z threshold | Required `\|E_net\|` at `se_E = 0.0443R` |
|---|---|---|---|
| 1 | 0.0500 | 1.960 | 0.0868R |
| 2 | 0.0250 | 2.241 | 0.0993R |
| 3 | 0.0167 | 2.394 | 0.1061R |
| 5 | 0.0100 | 2.576 | 0.1141R |
| 10 | 0.0050 | 2.807 | 0.1244R |
| 20 | 0.0025 | 3.023 | 0.1339R |

The last column is the whole point: **by the twentieth cycle, the same measured
edge that would have passed on cycle one no longer passes.** Fishing has a price,
and the price is paid in evidence. A trader who tests twenty variations of a card
and keeps the best one has selected a survivor of twenty coin-flipping processes,
not discovered an edge.

`payoff_check.py`'s `n_req` uses the plain 2σ convention (a factor of 4 on
`(sd/|E|)²`). This table is the *stricter* bar a multi-cycle search has to clear.
Report both.

### 6. The stop rule: five cycles, then rotate

**After five cycles with `E_net ≤ 0`, the strategy is wrong. Rotate to a different
payoff corner. Do not tune the parameters.**

This is the rule the whole protocol exists to enforce, and it is the one most often
violated. Tuning a card that has no edge is not iteration; it is a search over
parameter space for a shape that looks good in the sample. The expected outcome of
that search is a card that performs at its *sample* level and not at its *true*
level — which, for a card with no true level, is `E = 0` minus the cost.

"Rotate to a different payoff corner" means changing which of `p` and `b` you are
trying to trade — moving from the `b = 0.25` credit corner to the `b = 2.5`
long-premium corner, or from premium selling to a term-structure card. It does not
mean finding a better strike on the same card.

### 7. Log every cycle — and tag the `setup`

The log is what makes the protocol checkable and what makes a kill list possible.
The `setup` column is not documentation; it is the key that lets any of these
questions be answered later:

- Which cohort produced this cycle's result?
- Which cohort is still alive, and which was killed and why?
- How many cycles has this cohort had, and therefore what is the Bonferroni bar?

`payoff_check.py --from-log` reads the same schema as
`edge-and-payoff-engineering`'s engine, so a cycle logged once can be graded by
either. The synthetic fixture at
`examples/logs/synthetic-options-log.csv` is a worked example of the schema.

---

## The loop as a diagram

```
   pre-register  ──►  change ONE lever  ──►  trade n_req trades
        ▲                                            │
        │                                            ▼
        │                         fit on 70% / hold out 30%
        │                                            │
        │                                            ▼
        │                      compute realised p, b, E_net  (--from-log)
        │                                            │
        │                                            ▼
        │                             ┌──────────────┴──────────────┐
        │                             │                             │
        │                    E_net > 0 and                  E_net <= 0  OR
        │                    clears alpha_adjusted          cycles == 5
        │                             │                             │
        │                             ▼                             ▼
        │                     keep the card,                ROTATE to a different
        │                     raise size within             payoff corner.
        │                     trade-sizing-recovery's       Do NOT tune parameters.
        │                     bands                                     │
        │                             │                             │
        │                             └──────────────┬──────────────┘
        │                                            │
        └──────────── increment m, log the cycle ◄────┘
```

---

## What the protocol does NOT do

- It does not tell you which corner will work. The corner map
  (`references/payoff-corners-for-options.md`) prices the corners; the market
  decides which one pays this year.
- It does not make a thin edge tradeable. If `n_req` is 4,896 trades
  (`[COMPUTED]` for `b = 0.5, p = 0.68`), no protocol shortens it. The correct
  response is a different card, not a shorter measurement window.
- It does not guarantee a positive result. It guarantees that the *evidence* for a
  result is honest. See `references/what-this-cannot-promise.md`.
- It does not own sizing. `trade-sizing-recovery` owns the bands; this protocol
  only tells you whether the card has earned a place in them.

---

## Failure modes

1. **Failure mode — the hypothesis is written after the cycle.** A pre-registration
   that appears in the log with the same timestamp as the result is not a
   hypothesis; it is a description of a known outcome, and it removes the only
   protection the protocol offers.
2. **Failure mode — two levers moved at once.** The most common version is changing
   the stop and the entry filter in the same cycle. It always produces an
   uninterpretable result.
3. **Failure mode — the cycle is measured early because the book is winning.** A
   hot week is not evidence. The `n_req` rule is the defence, and it will always
   feel too slow during a winning run — which is exactly when it is load-bearing.
4. **Failure mode — the holdout is re-fitted.** Once the holdout has informed a
   parameter choice it is not a holdout. It is part of the fit, and the 70/30 split
   has become 100/0.
5. **Failure mode — the cycle count `m` is not incremented.** Without `m` the
   Bonferroni bar stays at 1.96 and a searched card passes a test designed for a
   single pre-registered hypothesis.
6. **Failure mode — the five-cycle stop rule is treated as advice.** It is the one
   step whose purpose is to end a search. A sixth cycle on the same corner is the
   failure mode the protocol was written to prevent.
7. **Failure mode — the cycle is logged without a `setup` tag.** The cohort becomes
   unattributable, so the kill list cannot be built and the next cycle repeats the
   same work.
8. **Failure mode — a different strike on the same card is called "a different
   corner".** Rotation means a different payoff, not a different price.
9. **Failure mode — the cost lever is skipped because it is boring.** `c_R` is the
   cheapest lever to pull and the one most often left unexamined. Run it first; it
   costs a commission schedule and an afternoon.
10. **Failure mode — the protocol is applied to a single card and then abandoned
    after one cycle.** One cycle is one measurement. The protocol is designed to be
    run repeatedly, with the bar tightening each time.

---

## Worked check

```bash
# the realised record for one cycle, by cohort, with the sample the edge would need
py -3 scripts/payoff_check.py --from-log examples/logs/synthetic-options-log.csv

# the same, restricted to the corner under test, beside the proposed card
py -3 scripts/payoff_check.py --from-log examples/logs/synthetic-options-log.csv \
    --setup debit-spread-2.5R --tp 2.5 --sl 1.0 --p 0.35
```

See also: `references/overfitting-by-iteration.md`,
`references/from-negative-to-positive-walkthrough.md`,
`references/strategy-cards.md`, `references/what-this-cannot-promise.md`.
