# Payoff-Rule Engineering

The payoff rule is the **primary control**. It is set before entry, it is
mechanical, it needs no market view, and it is the only one of the four levers
that can be changed today without searching for anything.

This file is about the stop and the target as *settings* rather than as
*forecasts*. It does not tell you where a stop should go for a given instrument,
because that is a market-structure question belonging to the strategy skills. It
tells you what payoff the stop and target pair must **produce**, given your win
rate, for the book to be profitable.

---

## 1. The rule in one line

```
b = avg_win / avg_loss     must exceed     b* = (1 - p)/p
```

The stop width sets the denominator. The target sets the numerator. Together they
set `b`, and `b` is what the book actually has. Nothing about the trader's opinion
of the trade enters the arithmetic.

---

## 2. Why the payoff rule beats an entry filter

Both raise `E`. They differ in cost:

| Lever | What it requires | How long it takes | What it costs |
|---|---|---|---|
| Raise `b` (target/stop setting) | One decision rule, applied mechanically at entry | Zero trades — it applies to the next one | Some win rate: a wider target is reached less often |
| Raise `p` (entry filtering) | A search for a filter that improves selection, validated on a fresh sample | Dozens to hundreds of trades per candidate filter | The filtered-out trades may have contained the winners |
| Cut cost | A commission schedule, a contract count, a wider strike, less frequent trading | Immediate | Nothing, except less trading |

`[COMPUTED]` — on the shipped illustrative book (`p = 0.510000`), lever `(b)` at
`+0.25` is worth `+0.25 × 0.510000 = +0.1275R` per trade, and lever `(a)` at
`+5pp` of win rate is worth `+0.05 × (0.962557 + 1) = +0.0981R`. The engine prints
both, ranked, on every run. On that book the payoff lever is the larger of the two
and it costs no trades to try.

**The comparison is not close on high-win-rate books.** At `p = 0.6182` the payoff
lever is worth `+0.25 × 0.6182 = +0.1546R` per `+0.25` of `b`, while five points of
win rate are worth `+0.05 × 1.4956 = +0.0748R`. The payoff lever is twice as
effective, and it is a setting rather than a search.

---

## 3. Setting the pair from the required payoff

Work backwards from the target expectancy. Given `p` and a target `E_target`:

```
b_needed = (E_target + 1 - p) / p
```

Then choose stop and target so that the realised ratio lands at or above
`b_needed`. Two consequences:

* **The stop width is not free to be arbitrary.** If the stop must sit at `$2.00`
  and `b_needed = 1.5`, the target must sit at `$3.00`. If the structure cannot
  reach `$3.00` inside the holding period, the trade does not have the payoff the
  book needs, and no amount of conviction changes that.
* **Adding cost raises `b_needed`.** The *net* requirement includes `c_R`:

```
b_needed_net = (E_target + c_R + 1 - p) / p
```

`[VERIFIED]` — on the shipped illustrative ledger at `p = 0.510000` and
`c_R = 0.029875`, reaching `E = +0.20R` requires `b = 1.3529` gross and `1.4115`
net of cost. The engine prints both columns side by side (`b needed` and
`b net of cost`) so the cost of cost is visible in the payoff it demands.

---

## 4. The stop: what it does to `avg_loss`

A stop is a promise about the denominator. If the average loss is `1.00R`, the
promise is being kept. If it is `1.15R`, the book is losing more than it planned,
and every R figure in the report is optimistic — including the payoff ratio, which
uses the *realised* `avg_loss` but is then used for sizing that assumes `1R`.

Three checks:

1. **`avg_loss` in R.** The engine prints it. Above about `1.15R`, either the
   stops are not where the ledger says they are, or the `risk` column is not the
   planned risk. Both need fixing before any sizing decision.
2. **The distribution, not just the mean.** If half the losses are `−1.0R` and
   half are `−2.5R`, the mean may still be near `1.5R` while the fat tail is doing
   the damage. The engine's `sd_R` is the proxy; a large `sd_R` beside a modest
   `E` means the outliers are setting the required sample.
3. **Gaps and assignments.** A stop does not guarantee a fill at the stop. Where
   the structure can be assigned or gapped through, the honest denominator is
   larger than the stop width, and the payoff rule must be set with that in mind.

`[ILLUSTRATIVE]` — a `$2.00` stop on a structure that can gap to a `$4.00` loss
has an effective average loss of more than `2 × 1R`; the required target roughly
doubles. This is why undefined-risk structures have no honest `risk` column, and
why the engine drops to CURRENCY MODE rather than invent one.

---

## 5. The target: what it does to `avg_win` and to `p`

A target is a promise about the numerator, and it is not free. Moving the target
out:

* raises `avg_win`, which raises `b`;
* lowers `p`, because a farther target is reached less often.

The two effects partially cancel, and which one wins is a property of the trade's
distribution, which nobody knows in advance. `[ESTIMATED]` — take a specific,
testable assumption: if a target moved from `0.5R` to `1.0R` is reached by only
half of the trades that reached `0.5R`, then `b` roughly doubles while `p` falls by
that fraction. At `p = 0.6182` and `b = 0.4956`, moving to `b = 1.0065` **with `p`
unchanged** is worth `+0.2388R` per trade; at `p = 0.50` with `b = 1.0` the
expectancy is exactly `0.00R`. The honest way to test a target change is to
**re-measure both `p` and `b`** after thirty trades, not to assume `p` holds.

**The rule that makes this actionable:** express the target as a multiple of the
stop, not as a price. "Take profit at `2 × risk`" survives a change in volatility;
"take profit at `$3.50`" does not.

---

## 6. The payoff ladder as a diagnostic

The engine's panel 4b prints `E` and `E_net` at a ladder of `b`, at the observed
`p`. `[VERIFIED]` — the shipped illustrative ledger:

| `b` | `E` | `E_net` | Reading |
|---|---|---|---|
| 0.9626 (actual) | 0.000941 | −0.028935 | Above `b*`, below cost. The book pays to trade |
| 1.0000 | 0.020000 | −0.009875 | Still under water |
| 1.5000 | 0.275000 | 0.245125 | A real edge, if `p` holds at a `1.5` payoff |
| 2.0000 | 0.530000 | 0.500125 | — |
| 3.0000 | 1.040000 | 1.010125 | — |

The diagnostic question is always the same: **is the required `b` reachable
without losing the `p`?** A `b` of `3.0` at `p = 0.51` is a trend-following book
and it will not have a `51%` win rate. A `b` of `1.5` at `p = 0.62` is a
credit-spread book and it will not have a `62%` win rate either. The ladder does
not answer that question; it makes the question precise enough to answer from the
strategy's own structure.

---

## 7. Failure modes

1. **Failure mode — a stop that is not actually where the ledger says.** The
   `risk` column records the plan; the fills record the truth. A book whose
   `avg_loss` is `1.2R` has a payoff ratio computed against a denominator that
   never existed.
2. **Failure mode — a target chosen for comfort rather than for `b_needed`.**
   Banking at `0.5R` produces `b ≈ 0.5` and, at any win rate below `67%`, a
   negative expectancy. That is the disposition trap, and the target is its cause.
3. **Failure mode — widening the target without re-measuring `p`.** The payoff
   rises and the win rate falls. Only the product matters, and the product is
   measured, not assumed.
4. **Failure mode — a payoff manufactured by one outlier.** `[COMPUTED]` — twenty
   winners that are otherwise `+1R` each, `avg_loss = 1R`, give `b = 1.00`; add
   one `+8R` winner to the same set and `avg_win` becomes `(8 + 19)/20 = 1.35R`, so
   `b` moves from `1.00` to `1.35` on the strength of a single trade. Remove the
   largest winner and re-check whether `b` still clears `b*`.
5. **Failure mode — an undefined-risk position given a fabricated `risk`.** If no
   honest max loss exists at entry, there is no honest R. Inventing one makes every
   statistic downstream a fiction.
6. **Failure mode — the same stop width on structures of different volatility.**
   A fixed dollar stop on a `20%`-IV name and a `60%`-IV name produces two
   different effective `b` profiles, and the cohort table will show it as a
   mystery difference between two setups.
7. **Failure mode — the payoff rule as a prediction.** A target is a setting, not
   a forecast. A trader who believes the target will be reached is making a
   directional call and has stopped using the payoff rule as a control.

---

## 8. The rule to write on the ticket

```
Before entry:
  stop   = the structure's honest max loss at entry      -> denominator
  target = stop x b_needed, where b_needed = (E_target + c_R + 1 - p)/p
  size   = R_max / stop_distance                         -> from streak survival
After 30 trades:
  re-measure p and b together, never one of them alone
```

The payoff rule is the only one of the four levers that is a mechanic rather than
a search. That is why this skill leads with it, and why the engine's panel 4 is
titled "the actionable table".
