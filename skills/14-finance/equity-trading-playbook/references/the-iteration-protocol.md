# The iteration protocol

Moving a negative-expectancy equity book to positive is not a search problem, it is a **testing**
problem. The difference is that a search terminates when a number looks good, and a test terminates
when a pre-registered prediction survives a pre-registered sample. This file is the protocol, in the
same shape as the sibling options playbook's, so the two speak one language.

## Why a protocol rather than a loop

The failure mode is not "the trader did not iterate". Traders iterate constantly. The failure mode is
that each cycle is measured against the last cycle's *result*, on a sample too small to distinguish
the change from noise, with the change chosen after the result was seen. That is not iteration, it is
serial curve-fitting, and it converges to a strategy that fits the past.

Seven rules prevent it. Each is mechanical. Each has a trigger.

## Rule 1 — Pre-register the hypothesis, naming the lever and the direction

Before the cycle begins, write:

```
CYCLE n
  card          : <the setup tag, the SC-id from strategy-cards.md>
  lever         : p | b | cost        (EXACTLY ONE)
  change        : <the specific rules change>
  predicted     : E_net moves from <X>R to <Y>R, direction <up|down>
  falsifier     : the measurement that would show this wrong
  n_required    : <n_req from payoff_check.py, rounded up>
  window        : <the calendar window this cycle will use>
```

**Why the lever must be named.** `E = p*b − (1−p)` has three inputs. A cycle that changes two of them
at once cannot attribute the result, and a cycle that changes all three is a new strategy wearing the
old one's name.

**Why the direction must be predicted.** A prediction whose direction is not stated cannot be
falsified, because any result can be read as "roughly what I expected". "E_net should rise by at
least 0.10R" is a prediction. "E_net should improve" is not.

## Rule 2 — Change exactly one thing per cycle

| Lever | What a change to it looks like | What it costs |
|---|---|---|
| `p` | a different entry rule, a regime filter, a confirmation signal, a higher-timeframe agreement | **requires a new signal**, so it requires research before it requires measurement |
| `b` | a different target distance, a different stop distance, a trailing exit, removing a cap on the winner | **a rules change you can make today**, at the cost of moving `p` in the opposite direction |
| `cost` | a different instrument, a limit order instead of a market order, a wider stop, fewer trades in the same notional | **usually available today**, and it is the only lever that improves without any market view |

Note the asymmetry in the middle column. `dE/db = p` and `dE/dp = b + 1`; a payoff change is available
immediately while a win-rate change requires a signal you may not have. **A book that is negative
should try the `b` and `cost` levers before the `p` lever**, because those two are rules and the third
is research.

## Rule 3 — A cycle is `n_req` trades. Do not measure earlier

```
n_req = 4 * (sd / |E_net|)^2          from payoff_check.py
```

`n_req` is the sample at which the mean reaches two standard errors. Measuring before it produces a
result that is *indistinguishable from noise by construction*, and reading that result is how a
working change gets reverted.

Worked, from the shipped checks:

| Card | `E_net` | `sd` | `n_req` | At 250 trades/year |
|---|---|---|---|---|
| `b = 3`, `p = 0.40` | +0.590000R | 1.959592 | **43** | 0.17 years |
| `b = 2`, `p = 0.40` | +0.200000R | 1.469694 | **216** | 0.86 years |
| `b = 0.75`, `p = 0.65` | +0.127500R | 0.834697 | **171** | 0.69 years |

**The thin corner needs 4.0x the sample of the fat one to say the same thing.** That is not a reason
to avoid the thin corner; it is a reason to know which corner you are testing and to write the number
down before you start.

(The three rows above use `E_net` with `c_R = 0.01` for the second and third, and `c_R = 0` for the
first — copy the number from your own run rather than from this table.)

**If `n_req` is `n/a` because `E_net <= 0`:** that is a result, not a measurement problem. A negative
expectancy does not become positive with more trades. Go to Rule 6.

## Rule 4 — Holdout by time: fit on the first 70%, check on the last 30%

```
|---------------------------- fit window 70% ---------------------------|-- holdout 30% --|
```

- Sort by `close_date`, not by trade id or by row order.
- The split is by **time**, not randomly. Random splits leak regime information across the boundary
  and make every strategy look better than it is.
- **Never re-fit on the holdout.** If a change is suggested by holdout behaviour, it is a *new*
  hypothesis requiring a *new* holdout window — a later one, that does not exist yet.
- Report the holdout figure even when it is bad, and especially when it is bad.
- **`p`, `b` and `c_R` reported on the fit window must be labelled as such.** A number measured
  in-sample is a description; only the out-of-sample figure is a test.

**Why 70/30 and not 50/50.** The fit window has to be large enough to contain `n_req` trades, or the
"fit" is not a fit. If a book has fewer than `n_req/0.7` trades in total, it has no holdout at all —
and the honest statement is "this book is too small to iterate on", not a 90/10 split.

## Rule 5 — Count your cycles; the bar tightens with the count

Each cycle is a comparison, and each comparison is a chance for a false positive. With `m` cycles and
a per-comparison two-sided 5% level, the family-wise error rate is `1 − 0.95^m`, which reaches 40% by
`m = 10`; the Bonferroni correction divides the per-comparison level by `m`:

```
alpha_i = 0.05 / m          two-sided
```

And for a win-rate comparison at `alpha_i`, the required sample grows. The standard-error form for a
proportion is `se = sqrt(p(1−p)/n)`, so the sample needed for a decision at level `alpha_i` goes as
`1/alpha_i` — i.e. **a book that has run `m` cycles needs roughly `m` times the trades per cycle to
keep the same power.**

**Print the adjusted bar in the cycle log, every cycle:**

| cycles `m` | `alpha_i = 0.05/m` | Rough multiple of `n_req` to keep the same power |
|---|---|---|
| 1 | 0.050000 | 1.0x |
| 2 | 0.025000 | 2.0x |
| 3 | 0.016667 | 3.0x |
| 5 | 0.010000 | 5.0x |
| 10 | 0.005000 | 10.0x |
| 20 | 0.002500 | 20.0x |

**This is the arithmetic reason a "successful" long iteration history is suspicious.** Twenty cycles
of small-sample tuning have an adjusted bar 20x tighter than the first cycle's, and a book that never
tightened it has been selecting noise for twenty rounds.

## Rule 6 — The stop rule: five cycles with `E_net <= 0` means the corner is wrong

```
if cycles_run >= 5 and E_net <= 0 on every cycle:
    STOP.
    ROTATE TO A DIFFERENT PAYOFF CORNER.
    Do not tune the parameters. Do not add a filter. Do not change the timeframe.
```

**Why rotation and not tuning.** Five cycles with `E_net <= 0` is evidence about the *corner*, not
about its parameters. If the corner is `b = 0.333333`, the problem is that `p* = 0.75` and no filter
changes `p*`. If the corner is `b = 1`, the problem is that `p* = 0.50` and the book is not beating a
coin flip. The repairs are the ones in
`break-even-payoff-and-the-disposition-trap.md`: widen the target, tighten the stop, or remove the
cap. Each of those **changes the corner**, which is what rotation means.

Tuning inside a corner that has failed five times is the definition of the loop that never terminates.

**The corollary:** rotation is not free and it is not unlimited. Every rotation resets the cycle count
*and* adds to the total `m` used in Rule 5, because every rotation is a comparison against the
previous configuration. Five rotations is not five fresh starts; it is a search across five corners.

## Rule 7 — Log every cycle with a `setup` tag

The log row for each trade carries the `setup` tag, so cohort attribution can be computed by
`payoff_check.py --from-log` and by `edge-and-payoff-engineering`. The cycle log is separate and
carries:

```
cycle | date_start | date_end | setup | lever | change | predicted | n_trades | n_required
p_fit | b_fit | E_fit | p_holdout | b_holdout | E_holdout | c_R | E_net | verdict | cycles_m | alpha_i
```

**Why the tag matters more than the cycle log.** A trade without a `setup` tag cannot be attributed,
and a book with no attribution cannot build a kill list — it can only report a pooled number, which
is the number that hides one cohort paying `+0.590000R` and another bleeding `−0.260000R`. The
shipped synthetic ledger in `../examples/logs/equity-book-synthetic.csv` demonstrates exactly that:
four cohorts, pooled `E_net = +0.066613R`, and two cohorts of opposite sign inside it.

## The protocol, as a checklist

- [ ] Cycle count `m` incremented and written down before the cycle starts.
- [ ] Lever named: one of `p`, `b`, `cost`.
- [ ] Change stated as a rule, not an intention.
- [ ] Predicted direction and magnitude of `E_net`, written before the cycle.
- [ ] `n_required` copied from `payoff_check.py`, rounded up to a whole number of trades.
- [ ] Fit window and holdout window dated, before the cycle.
- [ ] `alpha_i = 0.05/m` computed and written into the cycle log.
- [ ] The proposed card checked with `payoff_check.py` *before* the cycle, so `b`, `E`, `p*` and
      `c_R` are known rather than discovered.
- [ ] Holdout figure reported, whatever it says.
- [ ] **Complete when** the holdout `E_net` is recorded with its sign, its sample size, and the
      adjusted alpha it was judged against.

## What the protocol cannot do

It cannot make a negative corner positive, and it cannot tell you that a positive corner will persist.
It can only prevent one specific failure: **concluding from a sample that could not have supported the
conclusion.** See `overfitting-by-iteration.md` for the ways the protocol itself is defeated, and
`what-this-cannot-promise.md` for the limits that no protocol removes.

## Cross-references

- The corners that rotation moves between: `payoff-corners-for-equities.md`
- The repairs that count as rotation: `break-even-payoff-and-the-disposition-trap.md`
- How the protocol gets defeated: `overfitting-by-iteration.md`
- A worked run of the protocol: `from-negative-to-positive-walkthrough.md`
- Cohort attribution and the kill list: `edge-and-payoff-engineering`
- Review timeframe for the cycle's own statistics: `timeframe-performance-statistics`
