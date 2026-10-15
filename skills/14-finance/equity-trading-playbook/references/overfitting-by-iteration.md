# Overfitting by iteration

The iteration protocol in `the-iteration-protocol.md` is designed to prevent one failure: concluding
from a sample that could not support the conclusion. This file is the counter-file. It lists the eight
ways the protocol is defeated *while being followed*, each with the mechanism, a worked number where
one exists, and the countermeasure.

None of these is a discipline problem. Every one is a statistical one, and every one has an arithmetic
tell.

## 1. Selection across corners

**Mechanism.** Five payoff corners are tried and the best one is reported. The reported corner is not
a hypothesis that survived a test; it is the maximum of five draws.

**The arithmetic tell.** Under a null where all five corners have `E = 0`, the chance that at least one
shows a positive expectancy at a nominal 5% level is `1 − 0.95^5 = 22.6%`. At ten corners it is
`1 − 0.95^10 = 40.1%`. The five-corner search has a 22.6% chance of producing a winner from nothing.

**Countermeasure.** Count the corners tried as `m` in `alpha_i = 0.05/m` in Rule 5 of the protocol,
*before* naming the winner. A book that tried five corners and reports one has an adjusted bar of
`0.01`, and the reported corner must clear it on a sample sized for it.

## 2. Selection across windows

**Mechanism.** The strategy is evaluated over several calendar windows — the last 3 months, the last
6, the last 12, the last 24 — and the window that shows the best `E_net` is quoted.

**The arithmetic tell.** The windows are **nested**, not independent: the 12-month window literally
contains the 6-month one. A nested family is one draw read at several resolutions, and quoting the
best resolution is quoting the peak of a noisy series. `timeframe-performance-statistics` owns this
specific failure at the review level; the tell there is that the pooled `win_rate`, `payoff_ratio`
and `edge` are **identical** across every bucket, because the trades are the same trades.

**Countermeasure.** Fix the window before the cycle, from the intended trade cadence, and write it
down. Report the whole window series, not the best one.

## 3. Re-fitting on the holdout

**Mechanism.** The holdout is checked, the result is disappointing, a filter is added and the holdout
is re-checked. The second holdout figure is quoted.

**The arithmetic tell.** The second figure is in-sample, whatever it is called. Once the holdout has
informed a change, it is part of the fitting set and carries no out-of-sample information.

**Countermeasure.** A change suggested by the holdout is a **new** hypothesis requiring a **new**
holdout window — a later one, that does not exist yet. The honest statement is "this change cannot be
tested until I have another 30% of trades". That statement costs time, and it is the price of the
holdout being worth anything.

## 4. The sample that is too small by construction

**Mechanism.** A cycle is declared successful after 20 trades because `E_net` is positive.

**The arithmetic tell.** `n_req = 4*(sd/|E_net|)^2` is the sample at which the mean reaches two
standard errors. From the shipped checks:

| card | `n_req` | what 20 trades can say |
|---|---|---|
| `b = 3`, `p = 0.40` | 42.667 | less than half the required sample; the sign of `E_net` is a coin flip |
| `b = 2`, `p = 0.40` | 216.000 | about 9% of the required sample |
| `b = 0.75`, `p = 0.65` (with cost) | 171.434 | about 12% |
| `b = 1`, `p = 0.45` | n/a (`E < 0`) | nothing: more trades carry the mean further from break-even |

**Countermeasure.** `n_required` is copied from the tool into the cycle log *before* the cycle, and a
cycle that has not reached it is reported as **IN PROGRESS**, never as a result.

## 5. Cycle-count amnesia

**Mechanism.** The cycle log is not kept, or `m` is reset every time the card is renamed. Fifteen
cycles are reported as three.

**The arithmetic tell.** `alpha_i = 0.05/m`. At `m = 3` the bar is 0.016667; at `m = 15` it is
0.003333, five times tighter. A book that resets its count has been evaluating its fifteenth
comparison at its first comparison's threshold for fourteen rounds.

**Countermeasure.** `m` is a monotone counter on the *book*, not on the card. Renaming the setup tag
does not reset it. Adding a rotation does not reset it — a rotation is a comparison.

## 6. Pooling cohorts to reach the sample

**Mechanism.** The setup tag is dropped, or several setups are pooled, so the run reaches `n_required`
faster.

**The arithmetic tell.** Pooling hides sign structure rather than revealing it. The shipped synthetic
ledger is the demonstration: four cohorts, of which `trend-breakout` has `E_net = +0.590000R` and
`disposition-quick-tp` has `E_net = −0.260000R`. Pooled, the book reports `E_net = +0.066613R` — a
number that describes **no cohort in the book** and is MARGINAL by the tool's own band.

**Countermeasure.** One population per run, ever. If a cohort is too small to test, the honest
finding is "this cohort is too small to test", and it is a finding about the *book*, not about the
corner.

## 7. The `b` improvement that came from a `p` loss

**Mechanism.** The target is widened, `b` rises from 1.0 to 2.0, and the cycle is declared a success
on the `b` figure alone. The realised `p` falls at the same time, because fewer trades reach a farther
target, and the net effect is unmeasured.

**The arithmetic tell.** `E = p*b − (1−p)` has both terms moving. Worked: at `p = 0.45`, `b = 1.0`
gives `E = −0.100000R`; at `p = 0.35`, `b = 2.0` gives `E = 0.70 − 0.65 = +0.050000R`; at `p = 0.30`,
`b = 2.0` gives `E = 0.60 − 0.70 = −0.100000R`. **The same change to `b` is worth `+0.150000R` or
`0.000000R` depending on how much `p` moved with it** — and the width of the target is exactly what
determines that.

**Countermeasure.** A payoff change is measured with **both** `p` and `b` reported, and the cycle's
prediction is stated in `E_net`, not in `b`. The prediction "`E_net` should rise" forces the `p` term
into the ledger.

## 8. Cost that appears only after the sample

**Mechanism.** The cycle is evaluated on gross `pnl`, and the fee and slippage reconciliation happens
later — usually at tax time, by which point the conclusion has been acted on.

**The arithmetic tell.** Cost shifts the mean and leaves `sd` where it was, so `n_req` **rises** as
cost rises and the net edge shrinks. A card at `b = 0.75`, `p = 0.65` has `n_req = 147.405` at zero
cost and `171.434` at `c_R = 0.01` — a 16% larger sample requirement from a cost term of one
hundredth of an R. And at a 0.10% stop distance the same 5 bps is `c_R = 0.500000R`, which turns a
`+0.350000R` card into a `−0.150000R` card.

**Countermeasure.** The ledger's `cost` column is populated before the cycle, and the cycle is
evaluated on `E_net`. The break-even cost `c_R* = E` is printed by the tool and is the ceiling on
cost above which the corner is dead regardless of `p` and `b`.

## The eight, in one table

| # | Failure | Arithmetic tell | Countermeasure |
|---|---|---|---|
| 1 | Selection across corners | `1 − 0.95^m` reaches 22.6% at `m = 5` | count tried corners into `alpha_i = 0.05/m` |
| 2 | Selection across nested windows | pooled statistics are identical in every bucket | fix the window before the cycle |
| 3 | Re-fitting on the holdout | the second figure is in-sample by construction | a new hypothesis needs a new, later window |
| 4 | Sample too small by construction | `n_req` printed and ignored | log `n_required`; report IN PROGRESS |
| 5 | Cycle-count amnesia | `alpha_i` was computed against a reset `m` | `m` counts the book, not the card |
| 6 | Pooling cohorts to reach the sample | pooled `+0.066613R` against cohorts at `+0.590000R` and `−0.260000R` | one population per run |
| 7 | `b` gain measured without the `p` loss | `E_net` moving the wrong way while `b` rises | predict in `E_net`, report `p` and `b` together |
| 8 | Cost arriving after the conclusion | `n_req` rises from 147.405 to 171.434 at `c_R = 0.01` | populate `cost`, evaluate on `E_net`, read `c_R*` |

## The test that catches most of them in one move

**Recompute the whole cycle with the largest single win and the largest single loss removed.**

If `E_net` changes sign, the cycle's conclusion rested on two trades. If it does not, the conclusion
is at least not a two-trade artefact — which is a weaker claim than "the change worked", and a much
stronger one than the cycle's original headline.

Do it every cycle. It takes one command and one minute.

## What none of this fixes

Overfitting is not the same failure as a **wrong regime**, an **unexecutable rule**, or a **broken
stop**. A perfectly clean, protocol-following, out-of-sample-validated cycle can still describe a
corner that will not exist next quarter. That limit is permanent and is written down in
`what-this-cannot-promise.md`.

## Cross-references

- The protocol these eight defeat: `the-iteration-protocol.md`
- The corners the search moves across: `payoff-corners-for-equities.md`
- The nested-window problem at the review level: `timeframe-performance-statistics`
- Cohort attribution and the kill list: `edge-and-payoff-engineering`
- The permanent limits: `what-this-cannot-promise.md`
