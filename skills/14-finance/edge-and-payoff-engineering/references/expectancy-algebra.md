# Expectancy Algebra

`E = p·b − (1−p)` is the whole subject. Everything else in this skill is a
consequence of it, and every number the engine prints can be derived from it on
paper. This file derives it, states its units honestly, and reconciles the two
forms in which it appears.

---

## 1. The two inputs

Let `p` be the win rate and `b` the payoff ratio.

```
p = wins / (wins + losses)
b = avg_win / avg_loss
```

**Break-even trades are excluded from `p`'s denominator.** A trade that closed at
exactly `0` P&L is counted in `n`, contributes `0` to expectancy, and is neither a
win nor a loss. The engine prints the break-even count separately on the
`decision mix` line, so a book with 60 break-even trades out of 100 cannot look
like a 100% win rate.

**`b` is a ratio, so it is unit-free** — which is exactly why both inputs must be
measured in a unit that does not itself carry position size. That unit is **R**.

---

## 2. Why R, and what R is

One R is **the planned risk on one trade**, fixed at entry, before the outcome is
known. For a defined-risk spread it is the max loss of the structure at entry.
For a stock with a stop it is `(entry − stop) × shares`.

An R-multiple is `r_i = pnl_i / risk_i`. In R units:

* a trade that lost exactly its planned risk is `−1R`;
* a trade that made twice its planned risk is `+2R`;
* a trade that lost more than planned is `−1.4R`, and that is itself a finding.

**In currency, `b` measures position size.** A trader who doubles the contract
count on their best setup doubles `avg_win` in currency while `avg_loss` moves by
whatever the stop distance happens to be, and `b` changes for a reason that has
nothing to do with the strategy. This is not a stylistic objection. It is the
difference between a statistic and an artefact, and it is why the engine refuses
to average two units together (see GR1 in the skill) and drops to CURRENCY MODE
with a printed reason rather than guessing.

---

## 3. The derivation

Over `N` trades with `W` wins and `L` losses:

```
sum of r_i  =  W · avg_win  −  L · avg_loss
mean r      =  (W · avg_win − L · avg_loss) / N
```

With `N = W + L` after excluding break-even trades:

```
mean r = (W/N)·avg_win − (L/N)·avg_loss
       = p·avg_win − (1−p)·avg_loss
       = avg_loss · ( p·(avg_win/avg_loss) − (1−p) )
       = avg_loss · ( p·b − (1−p) )
```

So:

```
mean r  =  avg_loss_R · E      where  E = p·b − (1−p)
```

**This identity is the reconciliation row in the engine's output.** When
`avg_loss_R = 1.000000` the two rows are identical and `E` is the per-trade mean
in R directly. When they differ, the difference *is* the average loss, and the
engine prints `E (closed form x avg_loss)` so the gap is visible rather than
argued about.

`[COMPUTED]` — on the hand-check fixture: `p = 0.6`, `b = 1.666667`,
`E = 0.6·1.666667 − 0.4 = 0.6`, `avg_loss_R = 1.0`, so `E × avg_loss = 0.6`, which
equals the engine's `expectancy E = 0.600000`. The two rows agree because the book
loses exactly what it plans to lose.

`[VERIFIED]` — on the shipped illustrative ledger: `E = 0.000941`,
`E (closed form) = 0.000904`, `E (closed form x avg_loss) = 0.000941`. The three
rows agree once the average loss (`1.040577R`) is applied, and the raw closed form
is `3.9%` lower than the true per-trade mean.

---

## 4. The four derived quantities

### Break-even win rate

```
p* = 1 / (1 + b)
```

The win rate at which `E = 0`. Solve `p·b − (1−p) = 0` for `p`:

```
p·b − 1 + p = 0
p(b + 1) = 1
p = 1/(1 + b)                     ∎
```

### Break-even payoff

```
b* = (1 − p) / p
```

The payoff at which `E = 0`. Solve `p·b − (1−p) = 0` for `b`:

```
p·b = 1 − p
b = (1 − p)/p                     ∎
```

`p*` and `b*` are the **same statement** in two coordinate systems. One is
convenient when you are changing entries (which move `p`); the other is convenient
when you are changing exits (which move `b`). This skill reports `b` against `b*`
because on a high-win-rate book `b` is the binding constraint, and because a
payoff rule is a mechanic you can set while a win rate is a selection problem you
must search for.

### Edge

```
edge = p − p*
```

A signed distance, in win-rate units, from the break-even line. It is redundant
with `E` — both are zero together — but it answers a different question: "how many
percentage points of win rate am I above the line?" `[COMPUTED]` — the hand-check
fixture's `edge = 0.6 − 0.375 = 0.225`.

### Kelly fraction

```
f* = (p·b − (1−p)) / b = E / b
```

The growth-optimal fraction of capital to risk, *given that `p` and `b` are
known*. On a real ledger they are estimates, so full Kelly is a bet on the
estimates. The engine prints half-Kelly beside it, and prints neither without `n`
on the same panel.

`[COMPUTED]` — hand-check fixture: `f* = 0.6 / 1.666667 = 0.360000`, half-Kelly
`0.180000`. At `$100,000` of capital and `1R = $100`, a 36% Kelly fraction implies
`360` contracts of a `$100`-risk unit; half-Kelly implies `180`. That is why Kelly
is printed next to the estimate quality and not on its own.

---

## 5. Worked hand-check, every field

The fixture is ten trades, `risk = 100` on every row, `pnl` in round numbers, and
R-multiples `+2 +2 +1 −1 +1 −1 +3 −1 −1 +1`.

| Field | Arithmetic | Value |
|---|---|---|
| `n` | ten rows | 10 |
| wins / losses / break-even | `+` rows / `−` rows / zero rows | 6 / 4 / 0 |
| `p` | `6 / (6+4)` | 0.600000 |
| `avg_win` | `(2+2+1+1+3+1) / 6 = 10/6` | 1.666667 |
| `avg_loss` | `(1+1+1+1) / 4 = 4/4` | 1.000000 |
| `b` | `1.666667 / 1.0` | 1.666667 |
| `E` | `(10 − 4) / 10` | 0.600000 |
| `E` (closed form) | `0.6·1.666667 − 0.4` | 0.600000 |
| `p*` | `1 / (1 + 1.666667)` | 0.375000 |
| `b*` | `0.4 / 0.6` | 0.666667 |
| `edge` | `0.6 − 0.375` | 0.225000 |
| `f*` / half | `0.6 / 1.666667` | 0.360000 / 0.180000 |
| `sd_R` | `sqrt(20.40 / 9)` | 1.505545 |
| `n_req` | `4·(1.505545/0.6)²` | 25.19 |
| `L` (formula) | `ln(10)/ln(2.5)` | 2.513 |
| `L` (simulated) | seeded, 20000 trials | 2.178 |

`[VERIFIED]` — every value in that table is what the engine prints, and
`scripts/verify-skill.sh` asserts it field by field against the fixture's own
header.

---

## 6. Degenerate samples, and what the algebra does with them

The algebra is defined on samples that a real ledger produces constantly. None of
these may crash, and none may be reported as if it were a normal result.

* **`n = 0`.** Every field is undefined. The engine prints a refusal, not a zero:
  "a strategy with no trades has no measured expectancy, positive or negative".
* **All wins.** `avg_loss = 0`, so `b = inf`. `p* = 0` and `E` is finite and
  positive. An infinite payoff ratio is a statement about the sample, not about
  the strategy: with no losing trades there is nothing that bounds the loss side.
* **All losses.** `avg_win = 0`, so `b = 0`, `p* = 1`, `b* = inf`, and Kelly is
  undefined (`E/b` with `b = 0`). `E` is finite and negative.
* **A single trade.** `sd_R` is undefined (`n − 1 = 0`), so `n_req` is undefined.
  `E` is the trade's own R-multiple and `b` is `inf` or `0`.
* **`sd_R = 0`.** Every trade identical. `E` is known exactly, so `n_req = 0`.
  The engine says so rather than printing `0` without explanation.
* **`E = 0` exactly.** No sample size separates zero from zero; `n_req` is
  undefined and the engine says why.
* **A cohort with `n = 1`.** `n < 30`, so the verdict is `INSUFFICIENT`, and `b`
  may be `inf`. No kill, no keep.

---

## 7. Three things the identity will not do for you

1. **It will not tell you whether the sample is big enough.** `E` has no `n` in
   it. A `+0.6R` expectancy on ten trades and on ten thousand trades print the
   same `E`; only `n_req` separates them. See
   `how-many-trades-to-know.md`.
2. **It will not survive a change of unit.** Compute the same ledger in currency
   and in R and you get two different `b`s. That is a defect in the currency
   computation, not a second opinion.
3. **It will not detect heterogeneity.** `E` pooled over a profitable setup and a
   fatal one is a mean of two processes, and it describes neither. See
   `cohort-attribution-and-the-kill-list.md`.

---

## 8. The one-line summary

```
E = p·b − (1−p)          in units of the average loss; equal to the per-trade
                          mean in R when the average loss is 1R
```

Print `p`, `b`, `E`, `E_net`, `n` and `n_req` on the same panel, in R units, with
cost subtracted, and the argument is over. Every other section of this skill is a
consequence of that sentence.
