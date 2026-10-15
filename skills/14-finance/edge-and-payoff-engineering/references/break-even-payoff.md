# Break-Even Payoff

```
b* = (1 − p) / p
```

This is the number that decides whether a trader is **structurally profitable**,
and it is the single most useful figure in the skill. It is not a target, not a
forecast and not an opinion. It is the payoff at which the expectancy of the
trader's own win rate is exactly zero.

---

## 1. What it says

If `b > b*`, the strategy makes money *before costs* at the observed win rate.
If `b < b*`, it loses money — **while winning most of its trades** if `p` is high.
There is no third case.

| Win rate `p` | `b*` | Read in plain language |
|---|---|---|
| 0.25 | 3.0000 | You must make three times what you lose |
| 0.33 | 2.0000 | Two to one |
| 0.40 | 1.5000 | Three to two |
| 0.50 | 1.0000 | Even money — break even at a coin flip |
| 0.55 | 0.8182 | You may lose more than you win |
| 0.60 | 0.6667 | Two-thirds of a win pays for a loss |
| 0.6182 | 0.6176 | The illustrative disposition cohort's line |
| 0.70 | 0.4286 | Less than half of a win pays for a loss |
| 0.80 | 0.2500 | You could lose four out of five |

`[COMPUTED]` — every row is `(1−p)/p`. The table is the reason `b` is never
compared to `1.0` unless `p` happens to be `0.5`.

---

## 2. Why `b*` and not `p*`

`p* = 1/(1+b)` and `b* = (1−p)/p` are the same line in two coordinate systems.
Which one you print depends on which lever you are about to pull.

* **`p*` is the right framing when the fix is entry selection.** "I need to win
  66.9% instead of 61.8%" is a statement about filtering trades, and it is honest
  about how hard that is.
* **`b*` is the right framing when the fix is the exit rule.** "I need my average
  win to be 0.62 of my average loss instead of 0.50" is a statement about where
  the target sits, and it is a setting you can change tomorrow.

This skill prints both, and leads with `b*` for one reason: **on a high-win-rate
book, `b` is almost always the binding constraint, and `b` is the only one of the
two that is a mechanic rather than a search.** A trader who is winning 62% of the
time and losing money has already solved the entry problem. They have an exit
problem, and it is expressed as a payoff ratio.

---

## 3. The disposition trap, as arithmetic

`[VERIFIED]` — `SETUP-CREDIT` in the shipped synthetic ledger:

```
n        : 55
p        : 0.618182      (34 wins, 21 losses)
avg_win  : 0.4924R
avg_loss : 0.9935R
b        : 0.495589
b*       : (1 - 0.618182)/0.618182 = 0.617647
E        : -0.074962R
E_net    : -0.104837R     (c_R = 0.029875R)
verdict  : KILL (E_net<=0 with n>=30)
```

This cohort wins **61.8%** of its trades and loses money on every one of them in
expectation. `b` is `0.4956` against a required `0.6176`. The average winner
returns half of what the average loser costs, and the arithmetic is unambiguous.

Why does that happen? Because a trade that is up is closed early — the profit is
pleasant and the risk of losing it is uncomfortable — while a trade that is down
is given room, because closing it converts a paper loss into a realised one. That
is the disposition effect in behavioural finance. In this skill it is a payoff
ratio below its own break-even line, and it is fixable by moving one number.

---

## 4. Fixing it: two levers, one of which is mechanical

`b_needed = (E_target + 1 − p)/p`

For `SETUP-CREDIT` at `p = 0.618182`:

| Target | `b_needed` | `p*` at that `b` |
|---|---|---|
| `E = +0.1R` | 0.7794 | 0.5620 |
| `E = +0.2R` | 0.9412 | 0.5152 |
| `E = +0.3R` | 1.1029 | 0.4755 |
| `E = +0.5R` | 1.4265 | 0.4121 |

`[COMPUTED]` — `b_needed = (0.2 + 1 − 0.618182)/0.618182 = 0.9412` for the middle
row.

**Fix 1 — raise `b` by holding to the target.** If winners are held to about `1R`
instead of banked at `0.49R`, `b` becomes `1.0/0.9935 = 1.0065` at the same `p`:

```
E     = 0.9935 x (0.618182 x 1.0065 - 0.381818) = +0.2388R
E_net = +0.2388 - 0.029875                        = +0.2090R
```

`[COMPUTED]` — this is a change to **where the profit target sits**. It is one
number in the order ticket, applied before entry, and it needs no market view.

**Fix 2 — raise `p` by filtering entries.** With `b` unchanged at `0.495589`,
the *net* break-even win rate is higher than `p*` because cost comes out first:

```
net break-even p = (1 + c_R/avg_loss) / (1 + b)
                 = (1 + 0.029875/0.993537) / 1.495589
                 = 0.688621
```

`[COMPUTED]` — with `c_R = 0.0297` (the engine's own figure for this cohort when
run alone) and `avg_loss = 0.9935R`, so `p` must rise from `0.618182` to at least
`0.688621`, a **+7.0 percentage point** move, before the cohort is net positive at
its current payoff. At `p = 0.70` the cohort earns `E_net = +0.016907R`; at
`p = 0.75`, `+0.091201R`.

**Which lever is correct?** Fix 1 moves the cohort from `−0.1048R` to `+0.2090R`
per trade by changing a rule at entry. Fix 2 needs seven points of win rate, which
is a search problem with no mechanical answer. On a high-`p`, low-`b` book, fix 1
is the answer, and on most negative traders' ledgers it is the *only* answer that
is available this week.

---

## 5. The `b` ladder, and what "enough payoff" looks like

The engine's panel 4b walks `b` up a ladder at the observed `p`. `[VERIFIED]` — on
the shipped illustrative ledger (`p = 0.510000`, `c_R = 0.029875`):

| `b` | `E` | `E_net` |
|---|---|---|
| 0.9626 (actual) | 0.000941 | −0.028935 |
| 1.0000 | 0.020000 | −0.009875 |
| 1.5000 | 0.275000 | 0.245125 |
| 2.0000 | 0.530000 | 0.500125 |
| 3.0000 | 1.040000 | 1.010125 |

Read the top row: the pooled book is **above** its `b*` of `0.960784` and still
loses money, because `c_R = 0.029875R` is larger than the gross `E` of
`+0.000941R`. That is the second failure shape — not a payoff below `b*`, but a
payoff barely above it with a cost the book cannot cover. The engine prints
`*** COST IS THE BINDING CONSTRAINT ***` for exactly this case.

---

## 6. Failure modes this number exposes

1. **Failure mode — a payoff driven by one outlier win.** `b` is a ratio of two
   means, and a single `+8R` trade can lift `avg_win` above `b*` on its own. The
   engine prints `wins` beside `b` so the size of that win's leverage is visible;
   the check is to remove the largest winner and see whether `b` still clears.
2. **Failure mode — measuring `b` in currency.** A larger position on the winners
   raises `b` without changing the strategy. This is why the skill refuses to
   compute `b` in currency unless there is no alternative, and says so when it
   must.
3. **Failure mode — `avg_loss` above `1R`.** If the average loss is `1.15R`, the
   book is not losing what it planned, `b` is understated as a ratio of *planned*
   risk, and every sizing number derived here needs rescaling. The engine prints
   `avg_loss` in the unit for this reason.
4. **Failure mode — a target so wide it is never reached.** Raising `b` by moving
   the target out lowers `p`. The two are not independent: `[ESTIMATED]` — holding
   a winner to `1R` instead of `0.5R` may cost a few points of win rate, and at
   `p = 0.50` with `b = 1.0` the expectancy is exactly `0.00R`. The honest way to
   test the change is to re-measure both `p` and `b` after thirty trades.
5. **Failure mode — `b*` computed on a `p` that no longer holds.** `b*` is a
   function of the current `p`. If the win rate moved from `0.62` to `0.55`, the
   break-even payoff moved from `0.6129` to `0.8182` and the old target is no
   longer sufficient. Recompute both together.
6. **Failure mode — treating `b*` as a performance target rather than a floor.**
   `b*` produces `E = 0`. A book trading exactly at `b*` is not "fine"; it is
   paying costs for nothing. Read `E_net` at the target, not `E`.

---

## 7. The rule of thumb worth memorising

```
b* = (1 - p)/p        and        b* = 1 when p = 0.5
```

Every point of win rate above `0.5` buys payoff tolerance: at `p = 0.6` you may
have `b = 0.667`, at `p = 0.7` you may have `b = 0.429`. Every point below `0.5`
costs more than a point of payoff: at `p = 0.4` you need `b = 1.5`, at `p = 0.3`
you need `b = 2.333`.

So the two questions are one question:

> "What is my win rate, and what payoff does that win rate *require*?"

Print `b` against `b*` on every report. Not against `1.0`. Not against a memory of
what a good payoff ratio is supposed to be. Against `b*`, computed from this
book's own `p`, on the same line.
