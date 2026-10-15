# Win Rate versus Break-Even

**Portability target:** spec-level. Two arithmetic quantities and a sample-size question.

## The two numbers

```
payoff_ratio          = avg_win / avg_loss
                        avg_win  = gross_profit / wins
                        avg_loss = gross_loss  / losses     (a POSITIVE magnitude)

break_even_win_rate   = 1 / (1 + payoff_ratio)

win_rate              = wins / (wins + losses)              (break-even trades EXCLUDED)
edge                  = win_rate − break_even_win_rate

se_win_rate           = sqrt( p(1−p) / N )                  where p = win_rate, N = wins + losses
```

`edge > 0` means the book wins more often than it needs to in order to pay for its own
losses, at the average sizes it actually achieved. `edge > 2 × se_win_rate` means the win
rate is distinguishable from its own break-even at roughly the 95% level.

**These are two different claims and the engine reports them separately.** A book can have a
positive edge it cannot prove. That is the normal case, and it is the case for the shipped
illustrative log.

## Why break-even depends on the payoff ratio, not on a fixed 50%

The formula's shape is worth internalising, because the intuition "I win more than half the
time, therefore I am profitable" is wrong in both directions:

| `payoff_ratio` | `break_even_win_rate` | Reading |
|---|---|---|
| 0.50 | 66.67% | Win twice as often? Still need two wins for every loss |
| 0.75 | 57.14% | A short-premium book's typical shape |
| 1.00 | 50.00% | Symmetric: half is exactly break-even |
| 1.05 | 48.78% | Slightly better than even money per win |
| 2.00 | 33.33% | A trend book: most trades lose small, one wins big |
| 3.00 | 25.00% | A long-premium book's typical shape |

Two books with the same win rate have different break-evens and therefore different futures.
A 55% win rate is a healthy edge at a payoff of 1.05 and a losing business at a payoff of
0.60. **`win_rate` alone is not a performance statistic.** The engine prints `payoff_ratio`
and `break_even_win_rate` immediately next to it so the three cannot be read apart.

## The shipped illustrative log, quoted from engine output

Data: `examples/logs/illustrative-year-synthetic.csv` — **synthetic, illustrative, generated
at fixed seed 20260414, carries no market information.** Values pasted from
`examples/run-output.txt`:

```
wins = 66   losses = 54   breakeven_trades = 0   decided = 120
gross_profit = 7,851.87      gross_loss = 6,143.48
avg_win      = 118.97        avg_loss   = 113.77
payoff_ratio = 1.045703

win_rate            = 0.550000   (55.00%)
break_even_win_rate = 0.488829   (48.88%)           1 / (1 + 1.045703)
edge                = 0.061171   ( 6.12%)
se_win_rate         = 0.045415   ( 4.54%)
2 × se_win_rate     = 0.090830   ( 9.08%)
edge / (2 × se)     = 0.6735                         ->  engine prints edge_test = FAIL
```

Read that as the honest description of a marginal book: it wins 55% of decided trades, it
needs 48.88%, so it is 6.12 percentage points above its own break-even, and 6.12 points is
**not** enough separation from 0 to call it proven at 120 trades. It needs about 265 trades
for a two-sigma result and about 519 for 80% power — the arithmetic is in
[significance-and-sample-size.md](significance-and-sample-size.md). [COMPUTED]

## The bucketing-invariance, which surprises people

The engine prints the beat-losses test once per bucket, and every row is **identical**. That
is not a bug and not redundancy: it is a proof.

- Every trade falls in exactly one period of every bucket.
- Pooling "all trades in the bucket" therefore pools *all trades*, whatever the bucket.
- `win_rate`, `payoff_ratio`, `break_even_win_rate` and `edge` are properties of the trade
  set, not of the calendar.

**Consequence: choosing a different review timeframe cannot move this test at all.** Reviewing
weekly instead of monthly changes `t_stat`, `n_eff` and `max_drawdown`. It changes nothing
about whether the win rate beats its break-even. If someone reports that "the weekly view
shows a better edge than the monthly view", they have made an error — the trade set is the
same, and the only thing that changed is the calendar.

## Break-even trades: reported, and excluded from the denominator

A trade whose `pnl` is exactly zero is counted, reported as `breakeven_trades`, and **kept out
of the win-rate denominator**:

```
win_rate = wins / (wins + losses)        NOT wins / n_trades
```

The reason: a scratch trade is neither evidence for nor against the strategy's win rate. It
consumed a decision but produced no outcome in the direction the statistic measures. Including
it would drag the win rate toward zero as scratch volume rose, which would make a book that
flattens more positions look worse than one that refuses to.

The cost of that choice, stated plainly: a book with many scratch trades has a win rate
computed from a smaller sample than its trade count suggests, and its `se_win_rate` uses
`N = wins + losses`, not `n_trades`. The engine prints `breakeven_trades` on its own row so
this is always visible. On the shipped log it is 0; on the hand-check fixture it is 1, and the
engine reports `win_rate = 0.600000` from 5 decided trades rather than `3/6 = 0.500000` from
6. Both numbers are defensible; only one is the reported statistic, and the choice is printed.
[COMPUTED]

## When the break-even rate cannot be computed

`break_even_win_rate` is `n/a` whenever `payoff_ratio` is `n/a`, which happens when:

- the bucket has **no losing trades** (`avg_loss` undefined) — every daily period on the
  shipped log, since each holds one trade;
- the bucket has **no winning trades** (`avg_win` undefined).

That is why the engine reports `n/a` in the `edge` row for `D`, `W` and `2W`-heavy periods and
a real number for `M`, `Q`, `H`, `Y`. **A bucket whose periods are individually one-sided
cannot state an edge**, even though its *pooled* edge across all its trades can be stated. The
engine reports both, and the pooled figures are the ones used for the beat-losses test.

## Why the payoff ratio is fragile

`payoff_ratio` is a ratio of two averages, and averages move when one observation moves. Two
failure shapes matter here:

**1. One outlier win.** A single 8R winner in a 120-trade book can lift `avg_win` by several
percent and therefore *lower* `break_even_win_rate`, making the edge look better without the
strategy having changed. The generator for the shipped log deliberately includes a tail of
outsized **losses** (roughly 1.8–2.4R at a 3% rate, 6% in the stress window), which raises
`avg_loss` and makes the demonstrated edge *harder*, not easier. That is the honest direction
to fail in.

**2. One outlier loss.** The opposite: a single −2.4R loss raises `avg_loss`, lowers
`payoff_ratio`, raises `break_even_win_rate` and can turn a positive edge negative. On a book
whose `edge` is within a few points of zero — the shipped log's edge is 6.12 points — a single
tail trade can flip the sign of the headline number.

**The countermeasure, in order:** (a) recompute with the single largest win and the single
largest loss removed, and report both figures; (b) express P&L in R-multiples where the `risk`
column exists, so a 2R loss means the same thing in every trade; (c) never quote `edge` without
`payoff_ratio`, `avg_win` and `avg_loss` next to it, which is how the engine already lays it
out.

## Fees: the number that is not in the log

`pnl` is whatever the ledger says it is. If the ledger's `pnl` excludes commissions, exchange
fees, financing, borrow costs and the spread paid to enter and exit, then **every timeframe
flatters the strategy by the same amount** and the edge is overstated in every bucket.

`trade-performance-analyst` owns the fees-and-slippage guidance (its SKILL.md prescribes
modelling commission + half-spread + market impact + funding/borrow, and showing gross and net
returns). What belongs here is the timeframe consequence: **fees are per trade, so they hit the
fine buckets hardest in relative terms and the coarse buckets not at all.** A book whose edge
is 6.12 points gross may be negative net, and the fact that the weekly and monthly views agree
does not help — they agree because they are the same gross numbers.

Test: take a plausible round-trip cost per trade, subtract it from each `pnl`, and re-run. If
the edge flips sign, the review timeframe was never the problem.

## Failure modes around the win-rate test

1. **Failure mode: win rate quoted alone.** "I win 55%" is not a performance statement without
   the payoff ratio. Countermeasure: always print the pair, plus `break_even_win_rate`.
2. **Failure mode: a positive edge presented as a proven edge.** 6.12 points is a description;
   `FAIL` on `edge > 2 × se` is the test. Countermeasure: quote the engine's `edge_test`.
3. **Failure mode: zero-P&L trades inflating or deflating the denominator silently.**
   Countermeasure: report `breakeven_trades` and the denominator used.
4. **Failure mode: payoff ratio driven by one trade.** Countermeasure: recompute with the
   outlier removed and report both.
5. **Failure mode: a timeframe credited with an edge change it cannot cause.** Countermeasure:
   note the bucketing-invariance explicitly.
6. **Failure mode: scratch trades treated as wins.** A "cut at breakeven" is not a win.
   Countermeasure: `pnl > 0` is the only win test, and the engine enforces exactly that.
7. **Failure mode: R-multiple edge compared to percentage edge.** A 6.12-point edge in
   percentage terms and a 0.06R edge in risk terms are different units. Countermeasure: state
   the unit.
8. **Failure mode: fees omitted so every bucket agrees on a gross edge.** Countermeasure:
   state whether `pnl` is gross or net, in the log's own provenance block, before running.
