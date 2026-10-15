# The Disposition Effect as a Math Error

The disposition effect is usually described as a behavioural bias: traders sell
winners too early and hold losers too long. That description is true and it is not
actionable. This file states the same phenomenon as an arithmetic condition, which
is.

```
b < (1 - p)/p          equivalently          b < b*
```

**A trader with a good win rate and a bad payoff is not unlucky. They are
structurally unprofitable, and the condition is one line of algebra.**

---

## 1. The condition, and what it looks like in a ledger

`[VERIFIED]` — `SETUP-CREDIT` in the shipped synthetic ledger, constructed to have
exactly this shape:

```
n        : 55
wins     : 34        losses : 21        p : 0.618182
avg_win  : 0.4924R
avg_loss : 0.9935R
b        : 0.495589
b*       : (1 - 0.618182)/0.618182 = 0.617647
E        : -0.074962R
E_net    : -0.104837R       (c_R = 0.029875R)
verdict  : KILL (E_net<=0 with n>=30)
```

The trader wins **61.8%** of their trades. The average winner returns `0.4924R`
while the average loser costs `0.9935R` — the winners are roughly **half the size
of the losers**. `b = 0.4956` against a required `0.6176`.

Nothing behavioural is needed to explain this. The two numbers that produce it are
`avg_win` and `avg_loss`, and both are results of where the exits were placed.

---

## 2. The mechanism, stated mechanically

The behavioural description maps onto two exit rules:

| Behaviour | Exit rule | Effect on the payoff |
|---|---|---|
| "I'll take the profit before it disappears" | Winner closed at a fraction of `1R` | Lowers `avg_win` → lowers `b` |
| "It'll come back; I don't want to realise the loss" | Loser held past its stop, or held to expiry | Raises `avg_loss` → lowers `b` |

Two independent mechanisms, both pushing `b` down, and both operating through the
**exit**, not the entry. That is why the fix is a payoff rule and not a filter.

The behavioural account also predicts the observable pattern: the win rate stays
**high**, because the winners that are closed early are still winners. The trader
is not bad at picking trades. The book's `p` is above `0.6`, which is a genuinely
good win rate, and the book is losing money. This is the signature.

---

## 3. Why the trader usually misdiagnoses it

The two plausible misdiagnoses are both wrong:

* **"My win rate is good, so I'm fine."** `p` alone decides nothing. At
  `p = 0.6182` the break-even payoff is `0.6176`; the trader has `0.4956`.
  The win rate is not the problem.
* **"I'm getting unlucky."** A run of losses at a real edge is a streak of length
  `L`, and `L` is short on a `0.62` win rate — about `4` losses in `55` trades by
  the closed form, less by simulation. `[ESTIMATED]` — `ln(55)/ln(1/0.3818) =
  4.01`. A book with a `62%` win rate does not lose through unlucky streaks; it
  loses through every single trade, at about `0.075R` each.

The third misdiagnosis — "the strategy stopped working" — is also wrong here,
because the pattern is stable. It is not a change; it is a structural property.

---

## 4. The fix, quantified

At `p = 0.618182`, `b_needed = (E_target + 1 − p)/p`:

| Target | `b` required | `p*` at that `b` |
|---|---|---|
| `E = +0.1R` | 0.7794 | 0.5620 |
| `E = +0.2R` | 0.9412 | 0.5152 |
| `E = +0.3R` | 1.1029 | 0.4755 |
| `E = +0.5R` | 1.4265 | 0.4121 |

`[COMPUTED]` — the middle row is `(0.2 + 1 − 0.618182)/0.618182 = 0.9412`.

**Fix 1 — raise `b` by holding to the target.** If the average winner goes from
`0.4924R` to about `1.0R` while the average loser stays near `0.9935R`, then
`b ≈ 1.0`. `[VERIFIED]` — running the engine on the `SETUP-CREDIT` cohort alone
(`grep 'SETUP-CREDIT'` out of the illustrative ledger, header and comments kept)
prints this ladder verbatim:

```
  b            E              E_net          note
  0.4956       -0.0755        -0.1051        ACTUAL b
  1.0000       0.2364         0.2067
  1.5000       0.5455         0.5158
  2.0000       0.8545         0.8249
  3.0000       1.4727         1.4431
```

From `−0.1051R` to `+0.2067R` per trade, by changing **one number in the order
ticket**: where the profit target sits. (The panel's `E` column is the closed form
`p·b − (1−p)`; the engine's true sample mean for this cohort is `−0.074962R`
against a closed form of `−0.075437R`, and the reconciliation row explains the gap
as `avg_loss = 0.9935R` rather than `1R`.)

**Fix 2 — raise `p` instead.** With `b` unchanged, the net break-even win rate is
`(1 + c_R/avg_loss)/(1 + b) = 0.688621` `[COMPUTED]`, using the engine's own
`c_R = 0.0297` for this cohort and `avg_loss = 0.9935R`. So `p` must rise from
`0.618182` to at least `0.6886` — a **+7.0 percentage point** move — to make the
cohort net positive at its current payoff.

Two fixes, one of which is a setting and the other a search. On a high-win-rate
book the setting is the answer, and there is usually no search available that
would find `+7.1pp` of win rate anyway — the trader is already winning `61.8%` of
their trades.

---

## 5. How to detect it before it costs a decade

1. **Compute `b*` on every report.** It is `(1−p)/p` and it takes one line. A
   report that shows `b` without `b*` is a report that cannot see this condition.
2. **Watch `avg_win` and `avg_loss` in R, not just their ratio.** Their ratio can
   look stable while both drift. `[COMPUTED]` — `avg_win = 0.4924R` against
   `avg_loss = 0.9935R` is a ratio of `0.4956`, and the two numbers themselves are
   the diagnosis.
3. **Compare the median winner's holding time to the median loser's.** The
   behavioural signature is a large asymmetry. This is not an output of the
   engine, because the engine reads `close_date` and not intraday timing — but the
   `open_date`/`close_date` pair gives holding periods, and a ledger where winners
   are held for three days and losers for thirty is the condition in another form.
4. **Look for the target.** A profit target set at half the stop distance produces
   `b < 0.5` by construction and cannot be profitable at any win rate below
   `66.7%`. If the target is defined as "half the risk", the condition is
   guaranteed.
5. **Look for the absence of a stop.** A book whose `avg_loss` exceeds `1R` has
   losers wider than planned, which is the second half of the mechanism.

---

## 6. Why it is so hard to fix, and what makes it possible

The reason is that closing a winner early is **immediately pleasant** and holding a
loser is **immediately comfortable**, while the arithmetic consequence is invisible
until a hundred trades have accumulated. The feedback loop runs the wrong way: the
behaviour is rewarded per trade and punished per year.

The three things that make the fix possible:

* **A number instead of a feeling.** "Raise `b` from 0.4956 to 0.9412" is a
  mechanical instruction. "Don't be so emotional" is not.
* **A rule applied at entry.** A target expressed as a multiple of the stop is set
  before the trade exists, so the decision is made once and not ninety times under
  pressure.
* **A measurement after thirty trades.** `p` and `b` are re-measured together. If
  `b` rose and `p` fell by more, the rule was too wide and is adjusted once — with
  evidence, not with a feeling.

---

## 7. Failure modes

1. **Failure mode — reading the wrong number.** A trader who checks the win rate
   will never see this condition. The report must show `b` and `b*` on the same
   line.
2. **Failure mode — a target set as a fraction of the stop.** A target at half the
   stop gives `b ≈ 0.5` and requires `p > 0.667`. It is the condition, installed at
   entry.
3. **Failure mode — a stop that is not enforced.** `avg_loss` above `1R` is the
   other half of the mechanism and it is silent in a P&L-only export.
4. **Failure mode — attributing it to luck.** At a `62%` win rate the routine
   streak is about four losses. A book that grinds down over a year is not
   streaking; it is losing slowly on every trade.
5. **Failure mode — fixing it with an entry filter.** Raising `p` from `0.6182` to
   `0.6887` is a seven-point move. The payoff is the binding constraint and it is
   the cheaper fix.
6. **Failure mode — widening the target without re-measuring `p`.** A farther
   target is reached less often. Measure both, together, after thirty trades.
7. **Failure mode — treating the condition as psychological and therefore
   unfixable.** It is `b < b*`. Both terms are numbers, and one of them is a
   setting.

---

## 8. The one-line statement

```
A high win rate with a payoff below (1-p)/p is not bad luck, a bad strategy,
or a psychological mystery. It is a book that sells its winners at half price
and pays full price for its losers, and the arithmetic says so exactly.
```

The engine prints the banner whenever this condition holds. `[VERIFIED]` — this is
the engine's literal output when it is run on the `SETUP-CREDIT` cohort of the
shipped illustrative ledger, reproduced by keeping the file's comments and header
and `grep`-ing out the 55 `SETUP-CREDIT` rows:

```
  *** b = 0.4956 is BELOW b* = 0.6176. This book is structurally
      unprofitable at its current win rate: it is winning
      trades and losing money. That is the disposition
      effect expressed as arithmetic, not psychology. ***
```

Note that the banner fires on the **payoff panel**, which is pooled. On the full
200-trade illustrative ledger the pooled `b = 0.962557` sits just above
`b* = 0.960784`, so no banner appears — the trap is visible there only in the
cohort table, where `SETUP-CREDIT` is killed at `E_net = −0.1048R`. That is worth
remembering: a pooled book can hide the disposition condition behind a book-level
`b` that happens to clear, which is one more reason never to report a pooled panel
without the cohort table beside it.
