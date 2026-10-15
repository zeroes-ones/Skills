# Stop and Target Arithmetic

The stop and the target are not two independent settings. They are the numerator
and the denominator of one number, `b`, and `b` alone determines the win rate the
card requires. This file derives every consequence of that fact and states the
rules that follow.

Notation: `1R` = the money lost when the stop fires. `tp` = target in R.
`sl` = stop in R. `b = tp / sl`. `E = p·b − (1−p)`. `p* = 1/(1+b)`.
`b* = (1−p)/p`. All arithmetic below is `[COMPUTED]`.

---

## The two identities

```
b  = tp / sl                [COMPUTED]
p* = 1 / (1 + b) = sl / (tp + sl)        [COMPUTED]
```

Substituting the second into the first gives the form that matters:

```
p* = sl / (tp + sl)                       [COMPUTED]
```

**The required win rate is the stop's share of the total range.** A trader who
risks 2 to make 1 needs to win 2/(2+1) = 66.7% of the time. A trader who risks 1
to make 2 needs 1/3 = 33.3%. There is nothing else in the formula — no volatility
input, no directional view, no market regime. Only the ratio.

| `tp` | `sl` | `b` | `p*` | `sl/(tp+sl)` check |
|---|---|---|---|---|
| 0.5 | 2.0 | 0.250 | 80.0% | 2.0/2.5 = 0.800 ✓ |
| 0.5 | 1.5 | 0.333 | 75.0% | 1.5/2.0 = 0.750 ✓ |
| 0.5 | 1.0 | 0.500 | 66.7% | 1.0/1.5 = 0.667 ✓ |
| 1.0 | 1.0 | 1.000 | 50.0% | 1.0/2.0 = 0.500 ✓ |
| 1.5 | 1.0 | 1.500 | 40.0% | 1.0/2.5 = 0.400 ✓ |
| 2.5 | 1.0 | 2.500 | 28.6% | 1.0/3.5 = 0.286 ✓ |
| 4.0 | 1.0 | 4.000 | 20.0% | 1.0/5.0 = 0.200 ✓ |

---

## Why the stop is the lever

`p* = sl/(tp+sl)` is increasing in `sl` and decreasing in `tp`. Both directions
work, but they are not equivalent in practice:

| Change | Effect on `p*` | Cost of making the change | Requires a forecast? |
|---|---|---|---|
| Tighten the stop (`sl` down) | `p*` **falls** | The stop is hit more often, so the win rate you measure afterwards changes | No |
| Raise the target (`tp` up) | `p*` **falls** | The target is reached less often — same caveat | No |
| Raise the win rate (`p` up) | `p*` unchanged; the **edge** rises | New entries, new signal, new data, new measurement | Yes |

Two of the three levers are free and available today. The third requires a
better prediction than the one being used now. **Set the exits first; only then
ask whether the win rate clears them.**

Now the size of each lever. From `E = p(b+1) − 1`:

```
dE/dp = b + 1        [COMPUTED]
dE/db = p            [COMPUTED]
```

At `b = 0.25, p = 0.80`: `dE/dp = 1.25`, `dE/db = 0.80`. One point of win rate
buys more than one point of payoff ratio. At `b = 2.5, p = 0.35`: `dE/dp = 3.5`,
`dE/db = 0.35` — one point of win rate is worth ten of payoff.

So the *derivative* says win rate is stronger. The *availability* says payoff is
the place to start. Both are true, and the order is: **payoff first, win rate
second**, because payoff is a decision and win rate is a discovery.

---

## The stop is a rules change, worked

Take the credit card from `references/break-even-payoff-for-credit-structures.md`
and move only the stop, holding the target and the win rate fixed.

At `p = 0.80`, target 50% of the credit:

| Stop | `b` | `E` (`[COMPUTED]`) | `sd` | `se_E` at n=250 | Verdict |
|---|---|---|---|---|---|
| 2.0× `C` | 0.250 | 0.80 × 0.25 − 0.20 = **0.0000 R** | 0.5000 | 0.0316 | MARGINAL |
| 1.5× `C` | 0.333 | 0.80 × 0.333 − 0.20 = **+0.0667 R** | 0.5333 | 0.0337 | POSITIVE |
| 1.0× `C` | 0.500 | 0.80 × 0.50 − 0.20 = **+0.2000 R** | 0.6000 | 0.0379 | POSITIVE |

All three verdicts above are the tool's own output for the three commands in the
"Worked checks" section at the bottom of this file, not a hand classification.

Read this table carefully, because it contains a trap. The expectancy rises as the
stop tightens — but only if the 80% win rate survives the tighter stop. It will
not: a 1×-credit stop is hit more often than a 2×-credit stop on the same trades.
The honest statement is:

> **The table shows what the card pays at each stop *if* the win rate holds. It
> does not show that the win rate holds. Re-measure `p` after the change — it is
> a new card.**

That is exactly what the iteration protocol in
`references/the-iteration-protocol.md` exists for: one change per cycle, then
measure, then decide.

---

## The stop and the risk unit are not always the same thing

This is the most common bookkeeping error in options, and it corrupts every
number downstream of it.

| Structure | Max loss (structure) | Typical stop | Is the stop = `1R`? |
|---|---|---|---|
| Long call / long put | the debit paid | none (debit is the loss) | Yes |
| Debit spread | the debit paid | none, or a fraction of it | Yes, if unstopped |
| Credit spread | `W − C` | often 1–2× the credit | **No** — the stop is far inside the max loss |
| Iron condor | `W − C` (one wing) | often 1–2× the credit | **No** |
| Calendar / diagonal | the debit plus term-structure decay | the debit | Approximately |

When the stop is inside the max loss, `R` must be defined as **the money lost at
the stop**, not the structural max loss. Otherwise the measured average loss in R
is not 1.0, and `b` — which is `avg_win_R / avg_loss_R` — is measured against the
wrong denominator.

`payoff_check.py` handles both readings and prints which one it used on the
`R BASIS` line:

- `--tp/--sl` mode: `1R` is the numeraire; `b = tp/sl` already carries the stop.
- `--credit/--width` mode: `1R` is the structural max loss `(W − C) × multiplier`;
  `b` is `tp_money / sl_money` and is scale-free, so the two readings agree on `b`
  even when they disagree on `R`.

The disagreement matters for exactly one term: `c_R = cost_per_trade / R_dollars`.
A larger `R` makes cost look smaller. Define `R` once, write it on the card, and
use it everywhere.

---

## Building a card backwards

The useful direction is backwards: pick the win rate you have actually measured,
then read off the payoff the card must have.

```
b_required = (1 + c_R - p) / p        from  p(b+1) - 1 - c_R = 0     [COMPUTED]
```

Worked at `c_R = 0.02R`:

| Measured `p` | Required `b` (`[COMPUTED]`) | Required `tp/sl` | Interpretation |
|---|---|---|---|
| 0.30 | (1.02 − 0.30)/0.30 = **2.400** | 2.4 : 1 | only the long-premium corner reaches this |
| 0.40 | (1.02 − 0.40)/0.40 = **1.550** | 1.55 : 1 | long premium, mid target |
| 0.50 | (1.02 − 0.50)/0.50 = **1.040** | ~1 : 1 | a genuine coin-flip card |
| 0.60 | (1.02 − 0.60)/0.60 = **0.700** | 0.7 : 1 | premium selling with a *tight* stop |
| 0.70 | (1.02 − 0.70)/0.70 = **0.457** | 0.46 : 1 | premium selling, target ≈ 0.5 × stop |
| 0.80 | (1.02 − 0.80)/0.80 = **0.275** | 0.28 : 1 | the 50%/2× credit corner, roughly |
| 0.90 | (1.02 − 0.90)/0.90 = **0.133** | 0.13 : 1 | needs a 7.5:1 loss-to-win ratio |

The last row is the honest ceiling on premium selling. A 90% win rate — high for a
measured retail book — still requires a stop only about one-seventh the size of the
target. **A high win rate does not license a wide stop. Nothing licenses a wide
stop except a correspondingly high win rate.**

---

## Failure modes

1. **Failure mode — the stop is set from a dollar amount rather than a ratio.** "I
   always risk $200" fixes `sl` in dollars and says nothing about `tp`, so it does
   not fix `b` at all.
2. **Failure mode — the target is set from a hope rather than an exit order.** A
   `tp` that no order implements is not a `tp`; it is a number in a document.
3. **Failure mode — the stop sits at the structural max loss while the card claims
   a tighter one.** The measured average loss then disagrees with `sl` in the
   formula, and `b` is wrong in a direction that flatters the card.
4. **Failure mode — the win rate is not re-measured after the stop moves.** The
   stop is the input that changes how often you lose. A new stop is a new card and
   needs a new cohort.
5. **Failure mode — `sl = 0` is entered as "no stop".** There is no `b` without a
   loss. `payoff_check.py` reports `b: n/a` with the reason rather than substituting
   a number.
6. **Failure mode — the target is counted as reached on trades that closed at
   expiry.** An open position that expires at 40% of the intended target was not a
   target hit, and counting it as one biases `p` upward.
7. **Failure mode — a 1:1 card is chosen because it "doesn't need much".** It needs
   `p > 50%` net of the spread, which is a real directional edge and not a default.
8. **Failure mode — a tighter stop is adopted without accounting for the extra
   commissions.** Each stop-out is a full closing ticket set. The tighter stop trades
   win rate for cost; both terms are in `E_net = E − c_R`.

---

## Worked checks

```bash
# the same structure at three stops, showing p* fall as the stop tightens
py -3 scripts/payoff_check.py --tp 0.5 --sl 2.0 --p 0.80    # p* = 80.00%, E =  0.0000 R
py -3 scripts/payoff_check.py --tp 0.5 --sl 1.5 --p 0.80    # p* = 75.00%, E = +0.0667 R
py -3 scripts/payoff_check.py --tp 0.5 --sl 1.0 --p 0.80    # p* = 66.67%, E = +0.2000 R

# the payoff needed to reach a measured win rate, given a cost
py -3 scripts/payoff_check.py --tp 2.5 --sl 1.0 --p 0.35 --cost-r 0.02   # E_net = 0.2050 R
```

See also: `references/break-even-payoff-for-credit-structures.md`,
`references/payoff-corners-for-options.md`,
`references/streak-survival-by-corner.md`.
