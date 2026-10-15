# Per-Instrument Interpretation

**Portability target:** spec-level. Every statement below is about the *shape* of a trade
population, not about any product, venue or contract specification. Contract multipliers,
tick sizes, margin schedules and expiration mechanics belong to other skills and are not
restated here.

## Why instrument class changes the answer

Three properties of an instrument class decide which bucket can carry a statistical claim:

1. **Holding period** — sets the cadence by the quarter-to-half rule and sets how many trades
   per period a bucket will have.
2. **Payoff shape** — sets `break_even_win_rate`. A class that wins small and often needs a
   high win rate; a class that loses small and often needs a low one.
3. **Trade population size per year** — sets `n_periods` at a given bucket. This is the
   binding constraint for almost every real book.

The engine reads none of this. It reads `pnl` and dates. Which bucket is *usable* is
arithmetic; which bucket is *meaningful* is the class question this file answers.

## Short-premium options books (credit spreads, condors, cash-secured puts, covered calls)

| Property | Typical shape |
|---|---|
| Holding period | days to a few weeks; a 21-DTE spread often resolves in 7–14 days |
| Payoff shape | high win rate, small average win, occasional full-loss or worse event |
| `break_even_win_rate` | high — often 60–75%. A book winning 65% with a 0.45 payoff ratio is *below* break-even |
| Trades per year | high; hundreds to thousands for an active book |

**What timeframes mean here.**

- `W` is usually the natural review unit, matching a 7–14 day resolved life.
- `D` will almost always fail `trades_per_period` even for a busy book, because a book with
  200 trades over 250 sessions has 0.8 trades per day.
- `M` typically passes both gates and will usually be named by the verdict — and that is
  exactly why a short-premium book's monthly view is where the danger hides: **the loss is
  concentrated.** A book whose months are +300, +250, +280, −1,900 has a positive mean and a
  catastrophic distribution shape. `sd_period_pnl` catches that; `win_rate` does not.
- The tail is the whole story. Read `avg_loss`, `payoff_ratio` and the largest single loss
  from the `--csv`/`--periods` output, not the headline win rate.

**Specific trap.** A short-premium book's win rate *rises* as the book takes more risk
(selling closer to the money), which raises `win_rate` and lowers `payoff_ratio` roughly in
step, leaving `edge` flat while the tail grows. **A win-rate review of a short-premium book
can show improvement while the book is getting more dangerous.** The engine prints
`payoff_ratio` and `break_even_win_rate` on adjacent rows so the two move together in the
report.

## Long-premium options books (debit spreads, long calls/puts, LEAPS)

| Property | Typical shape |
|---|---|
| Holding period | weeks to two years |
| Payoff shape | low win rate, large average win when it works |
| `break_even_win_rate` | low — 30–40% is normal |
| Trades per year | low for a concentrated book |

**What timeframes mean here.**

- A long-premium book with 20 trades a year has **no usable bucket finer than quarterly**, and
  at quarterly it has 4 periods. That is the honest statement.
- Because `break_even_win_rate` is low, a 35% win rate can be a real edge. **Never apply a
  habit of "above 50% is good" to this class** — the engine's pooled `break_even_win_rate`
  is the comparison, whatever it says.
- `max_drawdown` here is often the book's dominant risk, and the coarsest bucket will hide it.
  Review the finest bucket with a defensible `trades_per_period` for drawdown even when the
  verdict names a coarser one.

## Equity books (6–18 month holds)

| Property | Typical shape |
|---|---|
| Holding period | 180–540 days |
| Payoff shape | mixed; often near 1.0 payoff, win rate near 50% |
| Trades per year | 5–50 for a concentrated book |
| Cadence (quarter-to-half rule) | monthly to quarterly |

**What timeframes mean here.** A 20-position book turning over once a year produces ~20
trades a year. At `M` that is 1.67 trades per period — under the gate. At `Q` that is 5 trades
per period but only 4 periods. **The gate's two numbers cannot both be satisfied by a
low-turnover equity book, and saying so is the correct output.** Options:

- Treat the yearly review as a *description* and stop asking it to be a test.
- Extend the window (5–10 years of history) until `M` has 60+ periods.
- Do not pool unrelated accounts to inflate the count.

**Consistency check with `equity-position-lifecycle`.** That skill's cadence table sets the
*ordinary-state monitoring* cadence at **weekly on a fixed day**, tightening to daily as
earnings, ex-dividend, index reconstitution, the long-term anniversary or margin stress come
into range. That is position monitoring, not performance review, and the two are compatible:
monitoring is weekly so a level breach is noticed; the *statistics* review is monthly to
quarterly because a 6–18 month holding period does not generate 12 independent monthly
outcomes. If a report conflates the two, one cadence will look wrong; they are different
questions. See [cadence-versus-holding-period.md](cadence-versus-holding-period.md).

## Futures and intraday books

| Property | Typical shape |
|---|---|
| Holding period | hours to days |
| Payoff shape | near-symmetric, high trade counts |
| Trades per year | hundreds to thousands |

**What timeframes mean here.**

- This is the one class where `D` can pass `trades_per_period >= 5`. A book taking 3–10 trades
  a session genuinely has a daily series.
- `periods_per_year = 365.25` for `D`, but the *trading* year is ~252 sessions. **The engine's
  periods-per-year figure is a calendar count and should not be used to annualise a futures
  book's session-based returns.** The engine does not annualise anything; this is a warning
  about what not to do with the printed number.
- Rolling contracts create a subtle break: a continuous series mixes contracts, and a
  position-roll's cost lands in whichever period it happened. If rolls are material, state
  whether their cost is inside `pnl`.

## Crypto books (24/7 markets)

| Property | Typical shape |
|---|---|
| Holding period | hours to months |
| Payoff shape | wide, fat-tailed |
| Trades per year | wide range |

**What timeframes mean here.** Because crypto trades every calendar day, `D` is a genuine
period and `W` is a genuine seven-day period — there is no weekend gap to create artificial
zero-day periods. Two consequences:

- A crypto book can produce `D` periods with real per-period statistics, unlike an equity
  book whose non-session days never appear (periods only exist where trades exist — the engine
  creates no empty periods).
- **A fine bucket on a 24/7 market produces more periods per year than the same bucket on an
  equity market**, so `n_periods >= 12` is reached sooner and the gate is easier. That does not
  make the statistic better; it makes the calendar denser.
- The fat tail interacts hard with `payoff_ratio`. Recompute with the largest win and loss
  removed, as [win-rate-versus-break-even.md](win-rate-versus-break-even.md) prescribes.

## Mixed books, multiple accounts, multiple strategies

**The rule: one bucket series, one population.** If a log contains an equity book and an
options book, the pooled `win_rate`, `payoff_ratio` and `break_even_win_rate` describe a
population that does not exist, and the period P&L series blends two different return shapes
into a distribution neither of them has.

Two acceptable approaches:

1. **Run the engine once per population.** Filter the CSV by `symbol` (or by an account
   column you add) and run each separately. Then compare the *verdicts*, not the period
   counts.
2. **Run pooled only for the reconciled total**, and label it as a total. A pooled run answers
   "did the desk make money"; it does not answer "is the equity book's edge real".

**Do not** pool to reach `trades_per_period >= 5`. Raising the count by mixing populations
raises the count and destroys the meaning at the same time.

## The class-to-bucket quick table

| Class | Expected usable bucket | Usually fails because | Watch out for |
|---|---|---|---|
| Short-premium options | `W` (review), `M` (verdict) | `D` on trades/period | High win rate masking a growing tail |
| Long-premium options | `M`–`Q`, often none | Low trade count | Applying a 50% win-rate habit to a low break-even |
| Equity (6–18 month) | `M`–`Q`, often none | Low trade count | Conflating monitoring cadence with review cadence |
| Futures / intraday | `D`–`W` | Nothing, usually | Annualising a session-based series with calendar periods-per-year |
| Crypto | `W`–`M`; `D` is genuine | Fat tails in `payoff_ratio` | Assuming the equity market's session calendar |
| Mixed / multi-account | none — split first | Blended population | Pooling to raise the trade count |

## Failure modes around instrument class

1. **Failure mode: one bucket series, two populations.** Countermeasure: split by `symbol` or
   account and run each.
2. **Failure mode: a win-rate habit imported from another class.** A 55% win rate judged
   against a fixed 50% instead of the class's own `break_even_win_rate`. Countermeasure: read
   the printed break-even rate.
3. **Failure mode: an equity book's session days treated as calendar days.** Countermeasure:
   the engine creates periods only where trades exist, so an equity `D` series is a
   session series wearing a calendar name — say so.
4. **Failure mode: contract rolls and financing treated as P&L.** Countermeasure: state what
   `pnl` includes in the log's `# PROVENANCE:` block.
5. **Failure mode: the class's tail not visible at the chosen bucket.** A short-premium book's
   one catastrophic month inside a quarterly bucket. Countermeasure: compute drawdown at the
   finest defensible bucket.
6. **Failure mode: a low-turnover book's annual review presented as a test.** Countermeasure:
   label it a description.
7. **Failure mode: pooling to reach the gate.** Countermeasure: read the gate as a finding
   about the book's turnover, not as an obstacle to be worked around.
