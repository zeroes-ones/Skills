# Streak Survival and Risk Per Trade

```
L      = ln(N) / ln(1/(1-p))                          expected longest losing streak
R_max  = D_tolerance / (L × safety)                   largest survivable risk per trade
safety = 1.5                                          a named, printed default
```

This is the **only defensible way to pick risk per trade**, and it is a derivation
rather than a house number. The engine exposes `D_tolerance` and `safety` as CLI
inputs (`--dd-tolerance`, `--safety`) and prints both in its `SETTINGS` block, so a
quoted `R_max` can never be separated from the assumptions behind it.

This skill derives the number. The **bands, ladders and recovery schedules** that
might sit around it belong to `trade-sizing-recovery`, `portfolio-signal-manager`
and `algorithmic-trader`. One number, derived, is what this file delivers.

---

## 1. The streak, and why it decides everything

A losing streak is not bad luck. It is the predictable consequence of a win rate,
and its length is computable before it happens.

For `N` independent trades at win rate `p`, the expected longest run of losses is
approximately:

```
L = ln(N) / ln(1/(1-p))
```

**This is an approximation, and the engine says so.** It is the standard asymptotic
estimate for the longest run in `N` Bernoulli trials, and it is biased **low**
because it ignores the tendency of losses to cluster. The engine therefore prints
it beside a seeded simulation of the same quantity, computed over the run's own
`N` and `p`, so the two can be compared:

`[VERIFIED]` — the engine's actual output:

| Ledger | `N` | `p` | `L` formula | `L` simulated |
|---|---|---|---|---|
| hand-check fixture | 10 | 0.600000 | 2.513 | 2.178 |
| illustrative (pooled) | 200 | 0.510000 | 7.427 | 6.810 |
| illustrative (trimmed) | 85 | 0.505882 | 6.302 | 5.675 |

The simulation lands below the closed form on all three, which is the right order
of magnitude for the approximation and the right direction for a small sample. The
important reading is not the difference; it is that a **six- to seven-trade losing
streak is routine** on a book that wins about half its trades.

The simulation is deterministic: the RNG is seeded from a fixed constant plus `N`,
so two runs on the same ledger agree byte for byte. That is why the number is
quotable at all.

---

## 2. The survival derivation

Given:

* `D_tolerance` — the currency the account can lose before the method is
  abandoned. The engine's default is **20% of capital**, which is a stated
  convention, not a recommendation.
* `L` — the expected longest losing streak.
* `safety` — a multiple applied to `L` to leave room for the approximation's
  understatement and for clustering. Default **1.5**.

Then the largest risk per trade that survives a run of `L × safety` losses is:

```
R_max = D_tolerance / (L × safety)
```

`[COMPUTED]` — the hand-check fixture, `capital = $100,000`, `D_tolerance =
$20,000`, `L = 2.17825`, `safety = 1.5`:

```
R_max = 20,000 / (2.17825 × 1.5) = 20,000 / 3.267375 = $6,121.12
as a fraction of capital: 0.061211, i.e. 6.12%
```

`[VERIFIED]` — the engine prints exactly `R_max (survival-derived risk/trade)
0.061211 of capital = 6,121.12` for that fixture, with the derivation shown on the
next line.

`[VERIFIED]` — the illustrative ledger, whose `L` is much longer because its win
rate is lower: `R_max = 0.019580 of capital = $1,958.03`, derived from
`D_tolerance 20,000.00 / (L 6.810 × safety 1.50)`.

**Read the two numbers together.** Same account, same tolerance, same safety
multiple — and the survivable risk per trade differs by a factor of three, purely
because the win rate differs. Risk per trade is a **property of the book's win
rate**, not of the trader's appetite.

---

## 3. Why `safety = 1.5` and not `1.0`

`L` is an *expectation*, not a bound. Roughly half of all samples contain a longer
streak than `L`. A trader who sizes at `D_tolerance / L` is sizing for the median
outcome of the streak distribution, which means an approximately even chance of
breaching their own tolerance.

`safety = 1.5` buys room in three directions at once:

1. **The approximation's bias.** The closed form understates the streak.
2. **Clustering.** Real loss sequences are not independent; bad regimes produce
   runs longer than an independent model predicts.
3. **The gap between `−1R` and reality.** A streak of `L` losses costs `L × 1R`
   only if every loss is exactly `1R`. `[ESTIMATED]` — if the book's average loss
   is `1.15R`, the effective streak cost is `1.15×` larger and `R_max` should be
   divided by that factor.

`1.5` is a disclosed default, not a universal truth. A reader who wants `2.0` can
pass `--safety 2.0` and the output will show it. What is not acceptable is an
undeclared safety margin, because the whole point of the derivation is that every
input is visible.

---

## 4. `D_tolerance` is the number the trader must actually choose

The engine defaults `D_tolerance` to `0.20 × capital` for arithmetic convenience
and prints the figure it used. The real choice is the trader's, and it is a
different kind of decision from everything else in this skill:

* **It is a method-abandonment threshold, not a stop.** "If the account falls this
  far, I stop trading this method and re-derive." It is a policy, and it must be
  written down before it is needed.
* **It must be a number the trader can actually honour.** A tolerance the trader
  will not act on is not a tolerance; it is a hope.
* **It interacts with `L`, not with conviction.** A trader who cannot accept a six
  loss run at a given size has chosen a size that is too large, whatever the
  derivation says.

`[ILLUSTRATIVE]` — a `$25,000` account with a stated tolerance of `$5,000` (20%),
a `p` of about `0.51` and an `L` of about `6.8` yields `R_max = 5,000/(6.8 × 1.5) =
$490`, about `1.96%` of the account per trade. Those inputs are invented to make
the arithmetic legible; the point is that the output is a **derived** number, and
that a trader who wanted `5%` per trade on the same account would be taking a
tolerance of about `51%` — which nobody would write down on purpose.

---

## 5. What `R_max` is not

1. **It is not a target.** It is a ceiling. Risking less is always permitted —
   it just slows the accumulation of evidence.
2. **It is not a Kelly fraction.** Kelly maximises growth given `p` and `b`; the
   survival derivation minimises the chance of breaching an abandonment threshold.
   They answer different questions and can disagree. Take the smaller.
3. **It is not a portfolio constraint.** Correlation across positions is invisible
   to a per-trade number. Three positions each at `R_max` in the same theme is one
   position at `3 × R_max`. Portfolio construction belongs elsewhere.
4. **It is not a licence to size up after a winning streak.** The streak
   distribution's parameters have not changed; only the bankroll has. See
   `how-many-trades-to-know.md` for what actually changes with more trades.
5. **It is not a substitute for `n >= n_req`.** A well-sized bet on an unmeasured
   edge is still a bet on an unmeasured edge.

---

## 6. The losing streak, and the "strategy stopped working" question

The most valuable use of `L` is diagnostic. When losses accumulate, there are two
hypotheses:

* **H1 — routine.** The streak is within `L × safety` and the book is behaving as
  its own win rate predicts.
* **H2 — changed.** The streak is material and the win rate or the payoff has
  moved.

The engine's decision tree (DT4) makes the test mechanical:

```
streak <= L x safety   -> ROUTINE. Keep sizing at R_max. Keep measuring.
streak >  L x safety   -> re-measure p and b on the last 30 closed trades:
                           b > b* and p within 2 se of the prior p  -> likely routine
                           b <= b* or p below 2 se of the prior p   -> the edge moved
```

`[ESTIMATED]` — at `p = 0.51` and `n = 30`, the standard error of the win rate is
`sqrt(0.51 × 0.49 / 30) ≈ 0.091`, so a two-sigma band is about `±0.18`. Three
trades of win-rate change inside that band are not evidence, which is exactly why
the comparison is made against the standard error and not against the previous
month's point estimate.

---

## 7. Failure modes

1. **Failure mode — sizing from a percentage that feels nice.** A number with no
   derivation cannot be checked, and it will be raised the moment it binds.
2. **Failure mode — using the closed-form `L` without the simulation beside it.**
   The closed form is biased low; a trader who sizes on it is under-provisioned by
   an unknown amount.
3. **Failure mode — forgetting the `safety` multiple.** `D_tolerance / L` sizes for
   the median streak, which means a coin-flip chance of breaching tolerance.
4. **Failure mode — an undeclared `D_tolerance`.** The engine prints the default it
   used; a report that omits it has hidden an assumption.
5. **Failure mode — treating `R_max` as a target.** It is a ceiling derived from
   survival, not an ambition.
6. **Failure mode — ignoring `avg_loss` above `1R`.** A streak of `L` trades costs
   `L × avg_loss_R`, not `L × 1R`. Divide `R_max` by the observed average loss in R.
7. **Failure mode — scaling up after a winning streak.** The edge is unchanged;
   only the variance grew. Sizing changes must come from `D_tolerance`, `L` or
   capital — not from how the last month felt.
8. **Failure mode — treating a routine streak as a broken edge.** Changing the
   method mid-streak guarantees that the sample never becomes decidable.
9. **Failure mode — treating a broken edge as a routine streak.** Re-measure `p`
   and `b` on the last 30 trades; do not assume the parameters are stationary
   forever.

---

## 8. The one-page procedure

```
1. p          = the book's win rate, from the engine.
2. L          = the engine's SIMULATED longest-losing-streak figure.
3. D_tolerance= a currency figure the trader has written down and will honour.
4. safety     = 1.5 by default, printed, changeable.
5. R_max      = D_tolerance / (L x safety)          -> the ceiling
6. avg_loss_R = the engine's avg_loss in R
   if avg_loss_R > 1: divide R_max by avg_loss_R
7. Size every trade at or below R_max, and write R_max into the state log.
8. On every losing streak, compare its length to L x safety before changing
   anything.
```

The single sentence worth remembering: **a losing streak of length `L` is what
your own win rate predicts, so it is not evidence about the strategy until it
exceeds `L × safety`.**
