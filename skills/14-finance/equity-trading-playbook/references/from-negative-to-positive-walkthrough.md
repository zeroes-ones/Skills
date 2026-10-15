# From negative to positive — a worked walkthrough

This is the protocol of `the-iteration-protocol.md` run end to end on one book. Every number is
either a `[COMPUTED]` figure from `payoff_check.py` or a hand derivation shown inline. **Nothing here
is a case study of a real account and nothing here is a promise.** The book is an invented,
representative shape: a retail equity trader with a high win rate and a negative expectancy, which is
the most common negative book there is.

The point of the walkthrough is the *order of operations*: which lever is tried first, why, and what a
cycle looks like when it is measured instead of felt.

## Cycle 0 — the book as it stands

The book, from a ledger with `setup`, `risk`, `cost` and `pnl` columns:

| Setup | n | wins | losses | `p` | avg win R | avg loss R | `b_R` | `c_R` |
|---|---|---|---|---|---|---|---|---|
| `disposition-quick-tp` | 24 | 15 | 9 | 0.625000 | +0.50 | −1.50 | 0.333333 | 0.010000 |

This is exactly the `disposition-quick-tp` cohort of the shipped synthetic ledger
(`../examples/logs/equity-book-synthetic.csv`), and its arithmetic is checkable in that file's header:

```
b_R        = 0.50 / 1.50                     = 0.333333
p*         = 1/(1+0.333333)                  = 0.750000
E (mean R) = (15*0.50 - 9*1.50)/24 = (7.5 - 13.5)/24 = -0.250000R
E (closed) = 0.625*0.333333 - 0.375          = -0.166667
c_R        = 72/7200                         = 0.010000
E_net      = -0.250000 - 0.010000            = -0.260000R
```

**Note the two expectancies.** `-0.250000R` is the realised mean R-multiple — the truth. `-0.166667`
is the closed form `p*b − (1−p)`, which is only the expectancy when the average loss is exactly 1R.
Here the average loss is 1.5R, and `1.5 * (-0.166667) = -0.250000`. **The closed form understates the
damage by a factor of the average loss magnitude.** Both figures must be reported; the mean is the one
to act on.

Run `py -3 scripts/payoff_check.py --from-log examples/logs/equity-book-synthetic.csv` and the
`disposition-quick-tp` row prints `E_net = -0.2600`. That is the starting point.

## Cycle 1 — rotate the payoff corner (lever: `b`)

**Pre-registered before the cycle:**

```
CYCLE 1
  lever      : b
  change     : target 0.50R -> 1.00R, stop unchanged at 1.50R
  predicted  : E_net rises from -0.260000R toward +0.033333R at the SAME p
  falsifier  : realised p falls below 0.600000, i.e. more than a 2.5-point loss of hit rate
  n_required : recomputed AFTER the change, from the new corner
  window     : 2026-04-01 .. the next n_required trades
```

**Why `b` first and not `p`.** From `payoff-corners-for-equities.md`, `dE/db = p` and `dE/dp = b + 1`.
A payoff change is a rules change available today; a win-rate change is a research programme measured
over `n_req` trades. **Try the lever you can pull today before the lever that requires a signal.**

**The new corner, computed:**

```
b      = 1.00 / 1.50                        = 0.666667
p*     = 1/(1+0.666667)                     = 0.600000        (was 0.750000)
E      = 0.625*0.666667 - 0.375 = 0.416667 - 0.375 = +0.041667  at the OLD p
       -- but p will fall, because fewer trades reach 1.0R than reached 0.5R
```

That last line is the whole risk of the cycle, and the falsifier names it. Run the card:

```
py -3 scripts/payoff_check.py --tp 1.0 --sl 1.5 --p 0.62
```

**Three scenarios, each computed:**

| Realised `p` | `b` | `E` | `c_R` at a 1.5R stop* | `E_net` | verdict |
|---|---|---|---|---|---|
| 0.62 (no `p` loss) | 0.666667 | `0.62*0.666667 − 0.38 = +0.033333` | 0.010000 | **+0.023333R** | MARGINAL |
| 0.60 (a 2-point loss) | 0.666667 | `0.60*0.666667 − 0.40 = 0.000000` | 0.010000 | **−0.010000R** | NEGATIVE |
| 0.55 (a 7-point loss) | 0.666667 | `0.55*0.666667 − 0.45 = −0.083333` | 0.010000 | **−0.093333R** | NEGATIVE |

\* the stop *distance* is unchanged at 1.5R, and `c_R = bps/(100*stop_pct)` depends on the stop in
**price** terms. If the R-distance is unchanged, the price distance is unchanged, so `c_R` is
unchanged. That is a real property worth noticing: `c_R` does not care about `b`.

**The cycle's margin is 2 percentage points of win rate.** A wider target that costs 2.5 points of hit
rate turns the cycle from `+0.023333R` to `−0.010000R`. This is why the falsifier was written down
*before* the cycle: without it, a 2-point `p` loss would be read as "the change did not work" and the
next cycle would change something else, and the ledger would never identify which change did what.

**Cycle 1 verdict: MARGINAL, and the margin is thin.** Not a failure — a real improvement from a
`−0.260000R` corner to a corner whose sign depends on a 2-point measurement.

## Cycle 2 — take the same corner and tighten the stop (lever: `b`, again)

Tightening the stop is a second change to `b`, and the protocol permits a repeat of the same lever,
one at a time.

```
CYCLE 2
  lever      : b
  change     : target 1.00R, stop 1.50R -> 1.00R
  predicted  : E_net rises to +0.240000R at the SAME p
  falsifier  : realised p falls below 0.50, or c_R rises above 0.05R
```

```
b      = 1.00 / 1.00                       = 1.000000
p*     = 1/(1+1.000000)                    = 0.500000
E      = 0.62*1.000000 - 0.38              = +0.240000R   at the old p
```

And the new risk, which the falsifier names: **the stop is 50% tighter in price terms, so `c_R` rises
by 50% for an unchanged bps.** Worked at 5 bps and a stop that was 3.0% of price and is now 2.0%:

| stop distance | `c_R = 5/(100*stop_pct)` | `E_net` at `E = +0.240000R` |
|---|---|---|
| 3.0% (before) | 0.016667R | +0.223333R |
| 2.0% (after) | 0.025000R | **+0.215000R** |
| 1.0% | 0.050000R | +0.190000R |
| 0.5% | 0.100000R | +0.140000R |

Cost drag doubles as the stop halves — and the card still pays comfortably, because `E` is large
relative to a 5 bps round trip. **This is the difference between a cost-sensitive and a
cost-insensitive card**, and the break-even stop shows it: `S* = bps/(100*E) = 5/(100*0.24) =
0.208333%` of price. Any stop wider than about 0.21% keeps this card positive.

**Cycle 2 is the cycle that matters, and it is the one the `p` lever could not have produced.**
`m = 2`, so the adjusted bar is `alpha_i = 0.05/2 = 0.025000` and the cycle needs roughly **2x**
`n_req` to keep the same power. `n_req` for the new corner:

```
sd  = sqrt(0.62*(1.0 - 0.24)^2 + 0.38*(-1 - 0.24)^2)
    = sqrt(0.62*0.5776 + 0.38*1.5376) = sqrt(0.358112 + 0.584288)
    = sqrt(0.942400) = 0.970773
n_req = 4*(0.970773/0.215000)^2 = 4*(4.515223)^2 = 4*20.387 = 81.549
```

**Cycle 2 verdict: candidate POSITIVE, `n_required = 82` trades, adjusted bar `0.025000`, requiring
about 2x for the same power because `m = 2`.**

## The cost lever, in the same book

The book's `c_R` is 0.010000 because every trade's stop was several percent of price. Suppose a
variant of the book ran the same corner on a 0.50% stop instead:

```
c_R = 5/(100*0.50) = 0.100000R
E_net = 0.240000 - 0.100000 = +0.140000R     (from +0.240000R)
```

The cost lever alone moved `E_net` by `−0.100000R` — larger than either of Cycles 1 and 2's
improvements. **That is the case for measuring `c_R` before optimising anything else.** An instrument
with a 5x wider spread, or a stop 5x tighter, dominates every entry-improvement the book could make.

## What the walkthrough demonstrates, in order

1. **The starting point was a corner, not a discipline problem.** `b = 0.333333` implies `p* = 0.75`.
   No psychological fix changes `p*`.
2. **The first lever was `b`, because it is available today.** `dE/db = p` is a coefficient you can
   change by editing an exit rule.
3. **Each cycle changed one thing, and the falsifier named the thing most likely to move the wrong
   way** — the `p` loss from a wider target in Cycle 1, the `c_R` rise from a tighter stop in Cycle 2.
4. **`m` was counted, and the adjusted bar was computed and printed.** Two cycles tighten it from
   `0.050000` to `0.025000`.
5. **`n_required` was recomputed after each change**, because `n_req = 4*(sd/E_net)^2` depends on
   `E_net`, which changed.
6. **The cost lever was evaluated before the entry lever was touched**, because it was larger.
7. **The result was stated as a candidate, never as a profit.** Cycle 2 is a card with a positive
   `E_net` on an *assumed* `p`. Whether `p = 0.62` survives the wider target and the tighter stop is
   exactly what the 82 trades are for.

## What the walkthrough does not show

- **It does not show a profitable trader.** It shows arithmetic moving in the right direction on an
  invented book.
- **It does not show that `p = 0.62` is achievable** on the new corner, on any instrument, in any
  regime, by anyone.
- **It does not show an out-of-sample result.** There is no holdout here at all: every figure is a
  projection from an assumed `p`, and the projection is what the cycles will test.
- **It does not model gap risk, halt risk, or a stop that fails to fill.** A `−1R` loss that becomes
  `−2R` invalidates the `sd`, `n_req` and `R_max` figures used above.
- **It does not produce a single dollar of P&L.** Every figure is in R.

## The same walkthrough as a one-page log

| cycle | lever | change | predicted `E_net` | `n_required` | `m` | `alpha_i` | verdict |
|---|---|---|---|---|---|---|---|
| 0 | — | the book as it stands | — | — | 0 | — | NEGATIVE, `−0.260000R` |
| 1 | `b` | target 0.50R → 1.00R | +0.033333R at unchanged `p` | recompute after | 1 | 0.050000 | MARGINAL, `+0.023333R` |
| 2 | `b` | stop 1.50R → 1.00R | +0.240000R at unchanged `p` | 82 | 2 | 0.025000 | POSITIVE candidate, `+0.215000R` |
| 3 | `cost` | (evaluate before any further entry work) | `c_R` moves `E_net` by up to 0.100000R | — | 3 | 0.016667 | evaluate first |

Row 3 is deliberately unfinished, because the walkthrough's own conclusion is that the cost lever
belongs earlier in the sequence than a third payoff tweak.

## Cross-references

- The protocol this runs: `the-iteration-protocol.md`
- The corner repairs used in Cycles 1 and 2: `break-even-payoff-and-the-disposition-trap.md`
- The cost term that dominated: `cost-drag-and-stop-distance.md`
- The unit the whole walkthrough is in: `r-units-versus-currency.md`
- Cohort attribution for the book's `setup` tags: `edge-and-payoff-engineering`
- What none of this guarantees: `what-this-cannot-promise.md`
