# R units versus currency

**R units are not a convenience. They are the only unit in which `p` and `b` mean what the algebra
says they mean.** Currency P&L mixes two skills — choosing an entry and choosing a size — into one
number, and the mixture is not separable from the number itself. This file proves that with two
trades and one added trade, derives the general condition under which the two units agree, and states
what to do about it.

## 1. Definitions

```
R_i         = the PLANNED risk of trade i, in currency (1R for that trade)
r_i         = pnl_i / R_i                    the R-multiple of trade i
p           = wins / (wins + losses)         the win rate is unit-free, always
b_R         = mean(r | win) / |mean(r | loss)|
b_currency  = mean(pnl | win) / |mean(pnl | loss)|
E_R         = mean(r_i)                      the realised expectancy, in R
E_currency  = mean(pnl_i)                    the realised expectancy, in currency
```

`p` is the same in both views: a win is a win whatever it paid. **Only `b` changes**, and `b` is what
`p*` and `E` are computed from. So a contaminated `b` contaminates everything downstream of it.

## 2. The two-trade proof

Two closed trades. Both are entirely invented numbers.

| Trade | planned risk `R_i` | outcome | R-multiple `r_i` |
|---|---|---|---|
| T1 | `$500` | `+$1,000` | `+2.0R` |
| T2 | `$2,000` | `−$2,000` | `−1.0R` |

**Currency view.**

```
mean win      = $1,000      mean loss = $2,000
b_currency    = 1,000 / 2,000 = 0.500000
p             = 1/2 = 0.500000
E$_ratio      = 0.5*0.5 - 0.5 = -0.250000
realised mean = ($1,000 - $2,000)/2 = -$500.00 per trade
```

**R view.**

```
mean win (R)  = 2.0         mean loss (R) = 1.0
b_R           = 2.0 / 1.0  = 2.000000
p             = 1/2        = 0.500000
E_R_ratio     = 0.5*2.0 - 0.5 = +0.500000
realised mean = (2.0 - 1.0)/2 = +0.500000R
```

Same two trades. The currency statistic says `b = 0.5`, `E = −0.250000`, a losing card. The R
statistic says `b = 2.0`, `E = +0.500000R`, a winning one. The account lost `$1,000` on the pair.

**Neither statistic is "wrong" at computing what it computes.** They disagree because T1's risk was
four times smaller than T2's, so the winner's `+2R` is a small number of dollars and the loser's
`−1R` is a large one. The currency ratio is measuring `mean(r * R | win) / |mean(r * R | loss)|`,
which is not `b`. It is `b` times a ratio of average position sizes, and that ratio is sizing.

## 3. A single added trade that flips the whole reading

Start with five trades, all risking `$200`:

| Trade | `R_i` | outcome | currency | `r_i` |
|---|---|---|---|---|
| T1 | `$200` | `+$160` | | `+0.8R` |
| T2 | `$200` | `−$200` | | `−1.0R` |
| T3 | `$200` | `−$200` | | `−1.0R` |
| T4 | `$200` | `−$200` | | `−1.0R` |
| T5 | `$200` | `+$160` | | `+0.8R` |

```
Currency: mean win = $160, mean loss = $200 -> b_$ = 0.800000
          p = 2/5 = 0.400000      E$_ratio = 0.4*0.8 - 0.6  = -0.280000
R:        mean win = 0.8R, mean loss = 1.0R -> b_R = 0.800000
          p = 0.400000            E_R_ratio = 0.4*0.8 - 0.6 = -0.280000
```

The two views **agree**, and the reason is the rule rather than luck: every trade risked the same
`$200`, so the size ratio is 1.0 and it cancels.

Now add **one** trade — a mediocre winner at `+1.0R`, taken at ten times the risk:

| Trade | `R_i` | outcome | `r_i` |
|---|---|---|---|
| T6 | `$2,000` | `+$2,000` | `+1.0R` |

```
Currency: mean win = ($160 + $160 + $2,000)/3 = $773.333333
          mean loss = $200
          b_$ = 773.333333 / 200 = 3.866667
          p = 3/6 = 0.500000
          E$_ratio = 0.5*3.866667 - 0.5 = +1.433333        <-- POSITIVE, and spectacular
R:        mean win (R) = (0.8 + 0.8 + 1.0)/3 = 0.866667
          mean loss (R) = 1.0
          b_R = 0.866667
          p = 0.500000
          E_R_ratio = 0.5*0.866667 - 0.5 = -0.066667       <-- still NEGATIVE
realised mean R = (0.8 + 0.8 + 1.0 - 1 - 1 - 1)/6 = -0.066667R
```

**One added trade, whose R-multiple was only `+1.0R` — an ordinary, unremarkable winner — moved the
currency payoff ratio from 0.800000 to 3.866667 and the currency expectancy from `−0.280000` to
`+1.433333`, while the R expectancy stayed negative at `−0.066667R`.**

No entry improved. No rule changed. The trade was not even a large R-multiple. It was a large
*notional*. The currency statistic recorded the size and called it edge.

## 4. When the two units agree, derived

Let the wins be indexed `w` and the losses `l`, with `n_w` and `n_l` counts:

```
b_currency = [ (1/n_w) * sum_{w} r_i * R_i ] / [ (1/n_l) * sum_{l} |r_i| * R_i ]
```

Write `avg_R|win = (1/n_w) * sum_w R_i` and `avg_R|loss = (1/n_l) * sum_l R_i`. Then

```
b_currency = b_R  *  [ avg(r*R | win) / (avg(r|win) * avg_R|win) ]
                  *  [ (avg(|r| | loss) * avg_R|loss) / avg(|r|*R | loss) ]
                  *  [ avg_R|win / avg_R|loss ]
```

The three bracketed factors are each equal to 1 exactly when risk is constant within the group (the
first two) and equal across groups (the third). So:

> **`b_currency = b_R` if and only if every trade risked the same amount, OR risk is uncorrelated with
> the R-multiple within both the winner group and the loser group AND the average risk of winners
> equals the average risk of losers.**

Every real book violates at least one of those conditions. A book that sizes by conviction violates
all three. **Therefore: convert to R before computing `p` and `b`, every time, with no exceptions.**

## 5. How to define `R_i` so the conversion is honest

`R_i` must be the **planned** risk at entry: the distance from entry to the initial stop, multiplied
by the share count actually held.

| Rule | Why |
|---|---|
| Use the **initial** stop, not the current one | A stop moved to break-even after the fact changes `R_i` retroactively and makes every loser look smaller. Use the risk you accepted when you entered |
| Multiply by **shares actually held**, including any partial fills | The risk you took is the risk you took |
| Record it **before** the outcome is known | A `risk` column filled in afterwards is a `risk` column shaped by the result, which is the contamination being removed |
| If a trade is added to or trimmed mid-flight, record the risk at **entry** and treat the addition as a separate trade | Otherwise the R-multiple of the composite is not a multiple of anything |
| Do **not** substitute average risk, a fixed notional, or "% of account" for a missing `R_i` | Any of those reintroduces the contamination. If `R_i` is missing, the trade is unusable and `payoff_check.py --from-log` reports CURRENCY MODE rather than inventing a denominator |

## 6. What the ledger tool does with this

`payoff_check.py --from-log` prints, for every `setup` cohort, both views side by side:

```
setup                    n wins     p      b_R      b_$   E$_ratio  E_R_ratio    c_R   E_net(R)
sizing-slip              3    1  0.3333   1.0000  10.0000   +2.6667    -0.3333  0.01000    -0.3433
```

and then flags the row:

```
sizing-slip: currency b = 10.0000 against R b = 1.0000 -- a gap of 9.0000.
             The gap IS the sizing, not the strategy.
sizing-slip: CONTAMINATED: currency ratio view +2.6667 against R ratio view
             -0.3333 -- opposite signs
```

`E_R_ratio` and `E$_ratio` are the same statistic (`p*b − (1−p)`, in units of the average loss); the
only difference is the unit `b` was measured in. `E_net(R)` is the realised mean R-multiple minus
`c_R`, which is the truth. **Read `E_net(R)` and the flag. Treat `b_$` as a diagnostic, never as a
payoff ratio.**

## 7. The one case where currency is the right unit

Currency is correct for exactly one question: **what happened to the account.** `net P&L` in currency,
reconciled against the broker's statement, is the check that no trade is missing and no fee is
undeclared. Everything else — every `b`, every `p*`, every `n_req`, every verdict — is computed in R.
The two questions are different questions and they must not share a column in a report.

## 8. The failure mode this prevents, stated once

A trader sizes up on high-conviction trades. Over a year, the high-conviction trades have a slightly
*better* win rate and a slightly *worse* average R-multiple — ordinary, and not evidence of skill
either way. The currency payoff ratio rises, because the sized-up winners are large in dollars. The
trader concludes the conviction sizing "works", raises size further, and the R expectancy — the only
one they actually earn — is unchanged. `r-units-versus-currency` is the check that catches this, and
it catches it before the size increase rather than after.

## Cross-references

- The corners the R view produces: `payoff-corners-for-equities.md`
- Why the ratio form can disagree with the sample mean: `break-even-payoff-and-the-disposition-trap.md`
- The measured walkthrough that uses this: `from-negative-to-positive-walkthrough.md`
- Cohort attribution and the kill list, which is a sibling skill's job: `edge-and-payoff-engineering`
- What the R statistic still cannot promise: `what-this-cannot-promise.md`
