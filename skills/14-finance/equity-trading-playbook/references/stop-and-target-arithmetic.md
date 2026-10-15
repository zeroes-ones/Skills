# Stop and target arithmetic

`b = tp / sl`. A payoff ratio is two distances divided, and in equity both distances are chosen by
the trader. This file works the mechanics of choosing them: what an ATR stop is, why a
percentage-from-entry stop makes `b` instrument-dependent, how a trailing exit destroys a fixed `b`,
and the three ways a stop distance is measured that quietly disagree with each other.

## 1. The three stop units, and why they are not the same number

| Unit | Definition | What it is good for | What it hides |
|---|---|---|---|
| **Percent of price** | `sl_pct = (entry − stop)/entry * 100` | cost arithmetic, because `c_R = bps/(100*sl_pct)` | volatility: 2% is tight on one instrument and loose on another |
| **ATR multiple** | `sl = k * ATR` | volatility normalisation; comparable across instruments | gaps: an ATR stop is a distance, not a guarantee of a fill |
| **R dollars** | `R = shares * (entry − stop)` | position sizing and the whole payoff algebra | nothing — it is the unit the algebra is written in |

The conversion between the first two is the one that matters:

```
sl_pct = 100 * k * ATR / price
```

Worked: `k = 2.0`, `ATR = $5.00`, `price = $50.00` gives `sl_pct = 100*2.0*5.00/50.00 = 20.0%`.
Worked the other way: `k = 1.5`, `ATR = $0.80`, `price = $40.00` gives `sl_pct = 3.0%`.

**This conversion is the hinge of the whole skill.** `b` is unit-free, so the payoff corner does not
care which unit you used. But `c_R = bps/(100*sl_pct)` **is** unit-dependent, because it depends on
the stop distance as a fraction of price. Two cards with identical `b` and identical cost rates have
different `c_R` if their stop *percentages* differ — and ATR-normalising a stop across instruments
with different volatilities guarantees that they will.

## 2. Choosing `sl` and `tp` from structure, then checking `b`

The order that works: pick the stop from the structure the entry invalidates, then pick the target
from the structure the move can reach, then **compute `b` and read `p*` from it.** Not the other way
round.

```
1. entry        : where the rules fire
2. stop         : the level that proves the entry WRONG
                  (the far side of the base, the pullback low, the failed-break extreme)
3. risk per share = entry - stop  (or stop - entry, for a short)
4. target       : the nearest level the move can plausibly reach
                  (range width, measured move, prior swing high, 2-3 ATR)
5. b            = (target - entry) / (entry - stop)
6. p*           = 1 / (1 + b)          <-- read this BEFORE taking the trade
7. E            = p*b - (1-p)          <-- at your measured p, not a hoped-for one
```

Step 6 is the step that gets skipped, and skipping it is the mechanism by which SC-0 in
`strategy-cards.md` comes into existence. There is nothing to compute after the trade is on: `p*`
was fixed at the moment the stop and the target were placed.

## 3. Worked structure examples

All entries and levels below are invented prices, used only to work the arithmetic.

**A pullback in a trend.** Entry `$50.00`, pullback low `$47.50`, first resistance `$60.00`.

```
risk per share = 50.00 - 48.00 (a shade under the low) = $2.00      -> 4.0% of price
reward/share   = 60.00 - 50.00                        = $10.00
b = 10.00/2.00 = 5.00      p* = 1/(1+5.00) = 0.166667
at p = 0.40: E = 0.40*5.00 - 0.60 = +1.400000R
```

**The same entry with a nearer target.** Resistance at `$54.00` instead:

```
reward/share = 54.00 - 50.00 = $4.00       b = 4.00/2.00 = 2.00
p* = 1/3 = 0.333333                        E at 0.40 = +0.200000R
```

The entry did not change. The target halved, and `E` fell by `1.200000R` per trade.

**The same entry with a wider stop.** Stop moved to `$45.00` (10% of price) to "avoid being shaken
out":

```
risk/share = $5.00      reward/share = $10.00      b = 2.00
```

Same `b` as the near-target case — and a **much larger `R` per share**, which means fewer shares for
the same dollar risk, which means the same R expectancy. Widening the stop while holding the target
fixed lowers `b`; widening the stop *and* the target proportionally leaves `b` alone and changes only
the instrument's volatility exposure. Nothing about the stop distance alone changes `E`.

**A tight stop on a low-volatility name.** Entry `$40.00`, stop `$39.20` (2.0% of price), target
`$42.40` (6.0%):

```
b = 6.0/2.0 = 3.00     p* = 0.250000     E at p = 0.40 = +0.600000R
c_R at 5 bps = 5/(100*2.0) = 0.025000R   -> E_net = +0.575000R
```

**A tight stop inflates `b` — and inflates `c_R` by the same factor.** Hold the target fixed at 6% of
price and tighten the stop from 2.0% to 0.4%: entry `$40.00`, target `$42.40` throughout.

```
stop 2.0% of price ($39.20): b = 6.0/2.0 = 3.00   c_R at 5 bps = 5/(100*2.0) = 0.025000R
stop 0.4% of price ($39.84): b = 6.0/0.4 = 15.00  c_R at 5 bps = 5/(100*0.4) = 0.125000R
```

The second card looks **five times better on `b`** (`p*` falls from 0.250000 to 0.062500) and **five
times worse on cost** — and neither number is the truth, because a 6% target on a 0.4% stop is
reached far less often, so the realised `p` collapses. **A tighter stop does not create a better
corner; it slides the same corner along the `p`/`b` trade-off.** Which way the net moves is measured
over `n_req` trades, never assumed from the `b` figure.

## 4. Trailing exits and the `b` that is not there

A trailing stop or a "let it run" exit does not have a `b`. It has a *distribution* of R-multiples,
and the useful summary of that distribution is the **sample mean R** and the **realised average
win / average loss ratio**, not the intended one.

Three consequences:

1. **The closed form `E = p*b − (1−p)` is only valid when the average loss is 1R.** With a trailing
   exit the average loss is usually slightly worse than 1R (slippage through the stop) and the
   average win is a distribution, not a number. Compute the sample mean of `pnl/risk`. It is the
   truth, and `payoff_check.py --from-log` prints it.
2. **`b` computed from a trailing book is a description, not a decision variable.** You cannot change
   it by choice, only by changing the exit rule. That is fine — but it means the exit rule *is* the
   decision variable, and it should be written down.
3. **A trailing exit raises `b` and lowers `p` at the same time.** The two move in opposite
   directions in `E = p*b − (1−p)`, and which dominates is empirical. `stop-and-target-arithmetic`
   cannot answer it; `the-iteration-protocol.md` can, over `n_req` trades.

## 5. The four stop-placement mistakes that are arithmetic mistakes

1. **A stop placed for comfort rather than for invalidation.** The question is "what price proves
   this entry wrong", not "what price can I tolerate". A comfort stop is usually too far, which
   lowers `b`, and it is usually placed without reference to structure, which lowers `p`. Both
   levers move the wrong way at once.
2. **A target placed at a round number rather than at a level the market has already respected.**
   This lowers the realised `p` at a fixed `b` — the target is not reached as often — without
   changing anything else.
3. **A stop measured from the wrong reference.** An ATR stop measured from the entry closes and an
   ATR stop measured from the setup's extreme are different numbers, sometimes by more than the stop
   itself. State which one the card uses; two people reading "1 ATR" will otherwise place different
   orders.
4. **A stop whose distance is not converted before comparing cards.** `b = 3` on a 0.4% stop and
   `b = 3` on a 12% stop are the same corner and completely different trades in every other respect:
   different `c_R`, different `R_max` in shares, different gap risk. Compare `b` first, then compare
   `sl_pct`, then compare `c_R`.

## 6. The check that takes ten seconds

For any proposed trade, before entry:

```
b  = reward / risk                      (in currency per share, or in R - same number)
p* = 1 / (1 + b)
```

If `p*` is above the best win rate you have ever measured on this setup over at least `n_req`
trades, the trade is a donation. That is the whole checklist. Everything else in this file exists to
make the two inputs to it well defined.

## Cross-references

- The corners these distances produce: `payoff-corners-for-equities.md`
- Why `p*` decides everything: `break-even-payoff-and-the-disposition-trap.md`
- How the stop distance drives cost: `cost-drag-and-stop-distance.md`
- Which stop a regime permits: `regime-to-strategy-map.md`
- Which indicator a card may use for the stop, and who owns its definition:
  `technical-signals-engineer` (`references/indicator-formulas.md`, `references/regime-detection.md`)
