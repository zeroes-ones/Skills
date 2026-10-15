# What the Engine Cannot Tell You

The engine prints this panel on every run, unconditionally. It is not a disclaimer
appended for form. Each item below is a question a trader will actually ask, and
for each one the honest answer is somewhere else.

---

## 1. It cannot tell you *why* a cohort is negative

It can tell you that `SETUP-FADE` returns `E_net = −0.252740R` over 60 trades
`[VERIFIED]`. It cannot tell you whether that is because the entries are early,
the target is too far, the setup only works in a volatility regime the sample
happened to miss, or the market changed in March.

**What to do instead.** Form the hypothesis from the numbers the engine does give
you, and test it on the next thirty trades:

* `p` low and `b` fine → the entries are the problem. Look at what the losers had
  in common at entry.
* `p` fine and `b` low → the exits are the problem. See
  `disposition-effect-as-a-math-error.md`.
* `b` above `b*` but `E_net` negative → cost. See `cost-drag-in-r-units.md`.
* `sd_R` far above `E` → a few large outcomes are dominating. Look at the tail.

---

## 2. It cannot see a position that has not closed

The engine reads closed trades. A position that is open, a roll that has not been
booked as a close, an assignment that has not been recorded, or a partial exit
still in progress is **invisible**.

**Consequences.** The report systematically under-counts losses that are still
unrealised, and it under-counts `n`. `[ESTIMATED]` — a book with a dozen open
positions carrying unrealised losses will report an `E_net` and a payoff ratio that
do not describe the account's actual state, and no arithmetic inside this engine
can detect it.

**What to do instead.** Reconcile the closed-trade count against the broker's own
closed-position count for the same window. If they differ, the ledger is missing
rows, and the reconciliation is the only check that reveals it.

---

## 3. It cannot detect a regime change

`b*`, `E`, `L` and `n_req` are properties of the **sample you handed it**. A
strategy that stopped working last month is summarised as it worked for the whole
period, and the summary will look fine.

In market terms:

* In a **bull market / uptrend**, `p` tends to rise and `b` tends to fall. `E` can
  fall while the equity curve rises, and the engine will report the falling `E` as
  a fact with no explanation attached.
* In a **correction / pullback**, `p` falls and `b` rises — stops are hit at full
  width while targets are reached less often. `L` grows. The cohort table usually
  shows one setup carrying the damage.
* In a **bear market / downturn / drawdown**, `p` falls hard and tail losses widen,
  so `avg_loss` moves above `1R` and every R in the report shrinks in real terms.
* In a **crash / tail event** (`2008` financial crisis, `march 2020`, a market
  collapse), the sample's `sd_R` is set by events that happened outside the sample's
  own regime, and `n_req` computed on the calm period permanently understates the
  required sample.

**What to do instead.** Keep the review cadence short enough that a change shows up
in a cohort before it shows up in the account. Split the ledger by date and run the
engine on the last 30 and the previous 30 separately. Compare `p` and `b`; a
difference larger than two standard errors is the first evidence of a change, not
proof of one.

---

## 4. It cannot tell a routine losing streak from a broken edge — but it gives you the number that does

The engine prints `L` twice: the closed-form estimate `ln(N)/ln(1/(1−p))` and a
seeded simulation of the same quantity. A losing streak **of length `L` is
expected**. That is the whole point of printing it.

What the engine cannot do is look at the streak currently happening and classify it.
That requires re-measuring `p` and `b` on recent trades and comparing them to the
prior sample with their standard errors — which is arithmetic outside the engine,
described in `streak-survival-and-risk-per-trade.md`.

---

## 5. It has no idea whether your `risk` column is honest

Every R in the report is `pnl / risk`. If `risk` was not enforced at entry — if the
stop was wider than planned, if the position was added to, if the structure was
undefined-risk — then every R is a ratio against a number that was never true.

**The tell is `avg_loss` in R.** `[VERIFIED]` — the engine prints it on the pooled
panel. If it is materially above `1.00`, either the stops were not where the ledger
says they were, or the `risk` column records an intention rather than a plan.

**What to do instead.** Set `risk` from the structure's honest max loss at entry and
declare in a `# PROVENANCE:` line how it was derived. If no honest answer exists for
a position — an undefined-risk structure with no stop — leave the field blank, and
the engine will drop the run to CURRENCY MODE and say so rather than average two
different units together.

---

## 6. It computes no risk-adjusted return metric, and that is deliberate

There is no Sharpe, no Sortino, no Calmar, no annualised return and no maximum
drawdown anywhere in this engine's output. Those are `trade-performance-analyst`'s
definitions, and this engine does not redefine them.

**Why it matters here.** Sharpe ratios and annualised returns are computed against a
time series and a frequency. A ledger's `trade_id` order is a sequence of decisions,
not a clock, and annualising a two-month sample produces a number that looks like a
result and is not one. If a report needs a Sharpe, it needs a period series and a
declared risk-free rate, and that is a different engine with a different contract.

---

## 7. It cannot tell you what to do next with an open position

This skill measures closed trades and derives one risk-per-trade ceiling. It does
not decide whether to close, roll, trim, or convert an open structure — that is the
decide-what-to-do-next router owned by `options-position-lifecycle` and
`equity-position-lifecycle`. Nor does it place a derived `R_max` into a sizing band
or a recovery ladder — that is `trade-sizing-recovery`, `portfolio-signal-manager`
and `algorithmic-trader`.

**What it does contribute.** The `b*` and `b_needed` figures that say whether the
structure's payoff can be profitable at the book's win rate, and the kill list that
says which slices should not be opened again. Those are inputs to a decision, not
the decision.

---

## 8. It cannot tell you whether the sample is a fair sample

A ledger of closed trades is a **selected** sample. Positions that are still open
are missing (§2). Trades the trader chose not to take are missing by definition.
Trades that were closed early because they were uncomfortable are present, while
trades that would have been closed early but were not are shaped differently.

**What to do instead.** State the selection in the provenance line. A ledger that
covers "all closed trades on account X from 2025-01-01 to 2026-09-30, one row per
final close, multi-trim positions recorded as a single row" is a sample with a
stated selection rule. A ledger with no such line is a sample of unknown shape, and
`n_req` computed on an unknown sample is a number about that sample only.

---

## 9. It cannot see correlation between positions

`R_max` is a per-trade ceiling derived from a per-trade streak model. Three
simultaneous positions in the same theme, each sized at `R_max`, is one bet at
`3 × R_max`, and the streak model does not know it.

**What to do instead.** Portfolio construction and correlation belong elsewhere.
The honest statement this skill can make is that its `R_max` assumes the trades are
independent draws from a distribution with win rate `p`, and that assumption is
false exactly when it matters most.

---

## 10. It does not know your capital, your tolerance, or your horizon

The engine defaults `--capital` to `100,000` and `D_tolerance` to `20%` of it. Both
are printed in the `SETTINGS` block on every run precisely so that the assumption
is visible. `R_max` in dollars, `years_at_current_pace`, and every currency figure
are all meaningless against a default that does not match the real account.

**What to do instead.** Pass `--capital` and `--dd-tolerance` on every run, and
record both in the state log. A quoted `R_max` without the capital it belongs to is
not a number; it is a fraction in search of a denominator.

---

## 11. It is a measurement instrument, not a strategy

The engine answers "what does this ledger say". It does not answer "what should I
trade", "is this a good setup", or "will this work next quarter". Every positive
verdict it can print is a statement about a **past sample**, and the only forward-
looking claim anywhere in this skill is the derivation of a risk ceiling from a
streak distribution.

If a request needs live prices, live Greeks, a forward-looking return estimate, or
a strategy recommendation, this engine cannot supply it and must not appear to. The
right response is to say so and route to the skill that can.

---

## 12. The honesty statement, restated

The shipped ledgers are **SYNTHETIC**. `examples/logs/hand-check-synthetic.csv` is
ten invented trades with `risk = 100` on each, built so the arithmetic can be
checked on paper. `examples/logs/illustrative-cohorts-synthetic.csv` is 200 invented
trades generated at a fixed seed, with four constructed cohorts chosen so the
`KEEP` / `KILL` / `INSUFFICIENT` verdicts all appear.

No number in this skill is a claim that any real strategy is profitable. The pooled
verdict on the larger fixture is `NEGATIVE EDGE`, which is a statement about four
invented cohorts and nothing else. The engine is real; the data is not; and the
distinction is carried in the filenames, the file headers, the `# PROVENANCE:`
lines that the engine echoes into its own output, and every number quoted from it.
