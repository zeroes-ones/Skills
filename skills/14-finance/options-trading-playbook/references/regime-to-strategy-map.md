# Regime to Strategy Map

Which payoff corner pays in which market regime, and why. This file does **not**
define regimes. The definitions live elsewhere and are consumed by name:

- **Trend and range regimes** — `technical-signals-engineer` classifies with ADX
  (a trend-strength measure, not a direction) and the 50-period SMA slope, and
  names six states: strong uptrend, weak uptrend, ranging, volatile uptrend,
  volatile downtrend, volatile range.
- **Macro and cross-asset regimes** — `macro-strategist` supplies the central-bank
  reaction function, the global liquidity impulse, and the risk-on/risk-off frame.
- **Volatility regimes** — `quantitative-analyst` and the options sibling skills
  supply IV rank and the term-structure shape.
- **Book-level regime exposure** — `options-risk-engineer` supplies gamma exposure,
  vanna/charm and the correlation-collapse question.

Everything table-shaped below is the *strategy layer* sitting on top of those: given
the regime the other skills have named, which corner do we trade, and what does it
do to the payoff arithmetic.

---

## The map

| Regime (as named by the siblings) | Corner that pays | Structure family | Entry condition | Exit rule | Sizing consequence |
|---|---|---|---|---|---|
| **Trending** — strong uptrend / volatile uptrend, ADX > 25 with a positive slope | Long premium, directional | long call, long put, call or put debit spread | Trend confirmed by `technical-signals-engineer`, and implied vol not rich versus realised | 1R stop, 2.5R target, trail after 1.5R | `b = 2.5` → `p* = 28.6%`; long streaks possible, so risk per trade must be *small* (see streak file) |
| **Trending down** — weak uptrend failing, volatile downtrend | Long premium, bearish, or short-premium-with-a-far-wing | long put, put debit spread, put ratio | Down-break confirmed, term structure not inverted | same 1R/2.5R card | same as above; the corner is identical, only the instrument changes |
| **Range-bound** — ranging, ADX < 20, flat slope, ATR/close < 2% | Short premium | short put, credit spread, iron condor, butterfly | IV rank above the entry gate, and the range's edges identified | target 50% of credit, **stop at ≤ 1× credit** | `b = 0.5` → `p* = 66.7%`; short streaks, so a larger risk per trade is survivable — but only if the range holds |
| **High IV** — IV rank high, realised vol *below* implied | Short premium, defined risk | credit spread, iron condor, broken-wing butterfly | IV rank gate met **and** realised vol trailing implied | target 50% of credit, stop ≤ 1× credit; take the whole structure off before expiry week | the variance risk premium is the compensation; `b = 0.5` needs `p = 66.7%` |
| **Low IV** — IV rank low, realised vol *above* implied | Long premium, non-directional or directional | long straddle, long strangle, debit spread, calendar | IV rank below the entry gate and a catalyst identified | 1R stop, 2.5R target; calendars are managed by the front leg's decay | `b = 2.5` → `p* = 28.6%`; long streaks, small risk per trade |
| **Event-driven** — earnings, FDA decision, FOMC, index rebalance | Long premium through the event, *or* short premium after it | long straddle before; iron condor after the event's IV crush | event date known and IV not already at an extreme | pre-event: hard 1R stop, target inside the expected move; post-event: condor at 50%/1× | pre-event cards have wide `sd`; the `n_req` rises and the sample gets long |
| **Volatile range** — ADX < 20 with ATR/close > 3% | **Nothing.** No corner clears its own cost | — | — | stay flat | `[COMMON-PRACTICE]` `technical-signals-engineer` calls this regime "no edge in chaotic ranges"; the arithmetic agrees, because both the win rate and the payoff ratio are unstable inside it |

The "volatile range" row is the only entry in this table that recommends no trade.
It is there because a corner needs a *stable* `p` and `b` to have an expectancy at
all, and a chaotic range moves both.

---

## Deriving the two central claims

### Claim 1 — premium selling pays in low-realised-vol / high-IV-rank regimes

Short premium is compensation for taking the other side of a volatility risk
transfer. `[COMMON-PRACTICE]` The expected payoff is the **variance risk premium** —
implied variance minus subsequently realised variance — which is positive on
average and is not free. Nothing in this skill measures it; the point here is only
that the corner's `p` and `b` both depend on it.

The arithmetic makes the dependence explicit. A short-premium book has two inputs
that move with the regime:

- `p` — the win rate — falls when realised vol rises. More realised movement means
  more touches of the short strike, which means more stops.
- The realised `b` — the payoff ratio — is `avg_win / avg_loss`, and it is a
  *management* number, so it is stable **only if the exits are followed**. In a
  trending regime they are not: the stop is jumped, or an assignment replaces the
  stop, and the realised average loss becomes a gap loss several times the intended
  stop.

So in a trending regime the card's `b` is not the card's `b`. Take the
range-bound card (`b = 0.5`, `p = 0.66` gives `E = 0.33 − 0.34 = −0.01R`, i.e.
already below break-even) and let two trades a quarter gap through the stop at 4×
the intended loss instead of 1×:

```
50 trades in the quarter; 2 of them realise -4R instead of -1R.
avg_loss_R = (48 x 1.0 + 2 x 4.0) / 50 ... but only the losing trades enter b.
Suppose 18 losses, 2 of which gapped to -4R:
  avg_loss = (16 x 1.0 + 2 x 4.0) / 18 = 24.0 / 18 = 1.3333 R
  avg_win  = 0.5 R    (the target is unchanged; the winners are fine)
  b        = 0.5 / 1.3333 = 0.3750
  p        = 32/50 = 0.64
  E        = 0.64 x 0.375 - 0.36 = 0.240 - 0.360 = -0.1200 R     [COMPUTED]
  p*       = 1 / 1.375 = 0.7273                                 [COMPUTED]
```

Two gap losses a quarter take the card from "needs 66.7%" to "needs 72.7%" and from
a thin positive to `−0.12R`. **The regime did not change the strategy; it changed
`b`, and `b` is what the card depends on.** This is why
`references/streak-survival-by-corner.md` and `options-risk-engineer`'s gap analysis
belong in the same conversation.

### Claim 2 — long premium pays when implied is cheap relative to realised

A long-premium position pays when the underlying moves more than the implied
volatility it was bought at. The purchase price *is* the market's forecast of
future movement. Buying when implied is rich means paying above the forecast and
needing the forecast to be wrong in your favour.

The payoff arithmetic says why an entry gate matters more here than the structure
choice:

```
long premium, 1R stop, 2.5R target:  b = 2.5,  p* = 28.57%      [COMPUTED]
at p = 0.30 :  E = 0.30 x 3.5 - 1 = +0.0500 R                  [COMPUTED]
at p = 0.35 :  E = 0.35 x 3.5 - 1 = +0.2250 R                  [COMPUTED]
at p = 0.40 :  E = 0.40 x 3.5 - 1 = +0.4000 R                  [COMPUTED]
```

Five points of win rate is worth `0.175R` — and on this card the win rate is
essentially a function of entry price. The IV-rank gate is not a refinement; it is
the source of the edge. `[COMMON-PRACTICE]` Long-premium books that ignore the
entry gate are buying the market's forecast at the market's price and paying theta
for the privilege.

Note the asymmetry: the *shape* of the card (`b = 2.5`) is fixed by the exits and
is available for free. The `p` is not. **Set `b = 2.5` by rule, then use the IV-rank
gate to earn the `p`.**

---

## What each regime does to the other terms

| Regime | `p` | `b` (realised) | `sd` | `L` (streak) | `n_req` |
|---|---|---|---|---|---|
| Range-bound, stable | stable | stable at the managed value | low | short | low — the edge is visible sooner |
| Trending (against the premium seller) | falls | **falls** — gap losses widen the average loss | rises | rises | rises |
| High IV, realised below implied | rises | stable | low | short | low |
| Low IV, realised above implied | falls | stable | low | short | rises fast (small `E`) |
| Event-driven | bimodal | depends entirely on the exit discipline | **high** | rises | high |
| Volatile range | unstable | unstable | high | unstable | undefined — no stable corner |

`n_req = 4(sd/|E|)²` moves as the **square** of the sd-to-edge ratio. A regime that
doubles `sd` while halving `E` multiplies the required sample by sixteen. This is
why "trade the same card in every regime" produces a book whose evidence never
accumulates: the mixture has a larger `sd` and a smaller `E` than either
component.

---

## Failure modes

1. **Failure mode — the regime is classified after the trade.** Regime labelling is
   an entry condition, not a post-hoc explanation of a loss.
2. **Failure mode — the same card is run in every regime and pooled.** Pooling
   inflates `sd` and deflates `E`, so the pooled book is unmeasurable even when one
   component is genuinely positive.
3. **Failure mode — a trending regime is treated as a range merely because the
   premium seller is winning.** Short-premium books win more often in ranges; a
   run of wins in a trend is a warning, not a confirmation.
4. **Failure mode — the volatility regime is read from price instead of from
   implied.** The claim is about implied *relative to* realised; observing that price
   has been quiet says nothing about what implied is charging for the next move.
5. **Failure mode — one gap loss is excluded as an outlier.** The gap is the regime
   speaking. Excluding it removes exactly the observation the regime map exists to
   capture.
6. **Failure mode — an event regime is traded with a continuous-time card.** An
   earnings gap does not respect a stop placed 1R away. The `b` that gets realised
   is not the `b` on the card.
7. **Failure mode — the entry gate is applied as a rule with no measurement behind
   it.** A gate at "IV rank 50" is a hypothesis; the iteration protocol in
   `references/the-iteration-protocol.md` is how it becomes a number.
8. **Failure mode — regime correlation is ignored across positions.** Five
   short-premium structures in the same index are one position wearing five names.
   `options-risk-engineer` owns the correlation-collapse question; the strategy
   consequence is that `sd` for the *book* is not `sd / sqrt(5)`.
9. **Failure mode — a bull market is assumed to make premium selling safe.** A bull
   market raises the *win rate* of short puts and simultaneously raises the *gap*
   when it ends. Both sides of the card move at once.

---

## Reading the regime, then the card

The order is fixed:

1. Name the regime with the sibling that owns it (`technical-signals-engineer` for
   trend/range, `macro-strategist` for cross-asset and liquidity, the options
   siblings for vol rank and term structure).
2. Read the corner from the table above.
3. Set the exits from `references/stop-and-target-arithmetic.md`.
4. Run `scripts/payoff_check.py` on the resulting card.
5. If the verdict is not POSITIVE, do not trade the card. **The regime has not
   earned it a pass.**

See also: `references/payoff-corners-for-options.md`,
`references/streak-survival-by-corner.md`,
`references/the-iteration-protocol.md`.
