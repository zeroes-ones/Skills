# Overfitting by Iteration

The iteration protocol in `references/the-iteration-protocol.md` is safe only if it
is followed exactly. This file derives what happens when it is not — specifically,
what a search over `m` cycles does to the evidence, and why the stop rule at five
cycles is arithmetic rather than discipline.

Every number is `[COMPUTED]` from the formulas shown. Two of the tables come from
closed-form results in order statistics; the formula is printed beside each value
so it can be checked rather than trusted.

---

## Overfitting is not parameter fitting. It is selection.

The intuition most traders hold is that overfitting means an over-complex model.
That is not the risk here. The risk here is simpler and worse:

> **Running `m` cycles and keeping the best one selects a survivor of `m` random
> draws. The kept result is not an estimate of the edge; it is the maximum of `m`
> estimates, and a maximum is biased upward by construction.**

No model complexity is required. A trader who tests five stop levels on the same
card and keeps the best one has run a five-draw selection. The arithmetic below
sizes that bias.

---

## Table 1 — the family-wise error rate

If each cycle is tested at a nominal `α` and the cycles were independent, the
probability that **at least one** cycle shows a false positive is

```
FWER = 1 - (1 - alpha)^m                                 [COMPUTED]
```

At `α = 0.05`:

| Cycles `m` | `FWER` | Interpretation |
|---|---|---|
| 1 | **0.0500** | the nominal level you thought you were testing at |
| 2 | **0.0975** | roughly one in ten |
| 3 | **0.1426** | one in seven |
| 5 | **0.2262** | more than one in five |
| 10 | **0.4013** | more than one in three |
| 20 | **0.6415** | nearly two in three |
| 50 | **0.9231** | almost certain |

**Five cycles at a nominal 5% is a 22.6% chance of at least one false positive.**
A trader who runs five cycles and finds one that looks good has found, with
probability 0.226, nothing at all. The protocol's stop rule at five cycles is placed
where the false-positive rate crosses the level at which the search is more likely
than not to have manufactured its own result.

### The honest caveat about independence

`1 − (1−α)^m` assumes independent cycles. **They are not independent**: consecutive
cycles trade the same market, often the same instruments, over adjacent time
windows. Correlated tests produce an FWER *below* the independence figure, not
above it.

The iteration protocol therefore uses **Bonferroni**, `α/m`, which is valid without
assuming independence:

```
alpha_adjusted = 0.05 / m                                [COMPUTED]
```

Bonferroni is conservative — it over-corrects for genuinely independent tests — and
the over-correction is the right direction to be wrong in when the alternative is
believing a searched result. Report both numbers rather than only the flattering one.

---

## Table 2 — what the selection overstates the edge by

Let each cycle's measured expectancy `Ê` be an unbiased estimate of the true `E`
with standard error `se_E`. Keep the best of `m`. The expected maximum of `m`
independent standard normal draws is

```
E[max_m] = m * ∫ x * phi(x) * Phi(x)^(m-1) dx            [COMPUTED]
```

with `phi` and `Phi` the standard normal density and distribution. At `m = 2` this
reduces to the known closed form `1/sqrt(pi) = 0.5642`, which is one check that the
integral is being evaluated correctly.

| Cycles `m` | `E[max_m]` | Overstatement at `se_E = 0.0443R` | Overstatement as a share of a `+0.2250R` true edge |
|---|---|---|---|
| 1 | **0.0000** | 0.0000R | 0.0% |
| 2 | **0.5642** | 0.0250R | 11.1% |
| 3 | **0.8463** | 0.0375R | 16.7% |
| 5 | **1.1630** | 0.0515R | 22.9% |
| 10 | **1.5388** | 0.0682R | 30.3% |
| 20 | **1.8675** | 0.0827R | 36.8% |
| 50 | **2.2491** | 0.0996R | 44.3% |

`se_E = 0.0443R` is the standard error of the `b = 0.5, p = 0.68` card at 250
trades — a thin, plausible card.

Read the table from a negative-expectancy starting point, which is the realistic
one. **A strategy with a true `E` of exactly zero, tested over 10 cycles and kept
at its best, reports `+0.0682R`.** That is a positive expectancy, printed by an
honest calculator, from a strategy with no edge. It is not a measurement error and
it is not a bug; it is what "keep the best of ten" means.

Worse: `+0.0682R` is larger than `se_E`, so a naive test would call it **POSITIVE**.
The selection manufactured a statistically significant result out of nothing.

---

## The three ways iteration overfits

### 1. Cycling the parameter space

Change the stop, change it back, change it differently. Each variation is a draw.
The stop levels are not independent of each other, so the effective `m` is smaller
than the count — which makes the problem *less* visible, not smaller.

**Prevention:** the protocol's one-change-per-cycle rule caps `m` at the number of
genuinely distinct hypotheses. If two cycles differ only in the stop's magnitude,
they are one hypothesis with a range, not two hypotheses.

### 2. Cycling the measurement window

Measure at 60 trades, then at 90, then at 120, and stop when the number looks good.
Each look is a test, and the looks are nested — trade 121 contains trades 1–120.

This is the mechanism behind the most familiar trading failure: a book that looks
positive for three months and reverts. The reading at month three was a draw from a
distribution whose mean was zero, and the trader read the draw as the mean.

**Prevention:** `n_req` is fixed before the cycle starts. If the cycle reaches
`n_req` and the result is not enough, the answer is a different card, not more looks.

### 3. Cycling the corner label

Re-tag the same trades under a new `setup` name and treat the new tag as a fresh
cohort. This does not reset `m`; it destroys the record that would have shown what
`m` is.

**Prevention:** the `setup` tag is a cohort key, not a description. A cohort's tag
changes only when the card's exits or entry condition genuinely change — and then it
is a new cohort with `m` starting at 1, not a re-labelling of the old one.

---

## The five-cycle arithmetic

Put the two tables together. After 5 cycles:

- The probability that at least one showed a false positive is **0.2262**.
- The best kept result is overstated by **1.1630 × se_E = 0.0515R**.
- The Bonferroni bar the surviving cycle must clear is **z = 2.576**, i.e.
  `|E_net| ≥ 2.576 × se_E = 0.1141R` at `se_E = 0.0443R`.

The `b = 0.5, p = 0.68` card's true edge is `+0.0200R` `[COMPUTED]`. Its Bonferroni
bar after 5 cycles is `0.1141R` — **5.7 times the edge it actually has.** The card
cannot pass, and it cannot pass *because it was searched for*. This is the arithmetic
reason the five-cycle stop rule exists: past five cycles, the bar a real edge must
clear has grown larger than the edges this skill's corners produce.

---

## What is not overfitting

Not every repeated action is a search. Distinguish carefully:

| Activity | Is it a test? | Why |
|---|---|---|
| Trading the same pre-registered card for a second cycle | Yes, `m` increments | It is a second measurement |
| Executing a trade at the card's rules | No | An observation, not a hypothesis test |
| Tightening a stop after a documented loss per a pre-written rule | No | The rule was fixed before the loss |
| Tightening a stop because the last four cycles with the wide stop lost | **Yes** | The last four cycles are the sample that motivated the change |
| Rotating to a different payoff corner after 5 failed cycles | **Yes — and it resets `m` to 1** | A new corner is a new hypothesis |
| Rotating and then returning to the old corner 2 cycles later | Yes, `m` continues | The old corner's record is part of the same search |

The last row is the subtle one. Going back to a corner already failed is not a fresh
start; it is a continuation of the same search with the old evidence in hand.

---

## Failure modes

1. **Failure mode — the count of cycles is never written down.** Without `m` the
   Bonferroni bar stays at 1.96. The single most common way this fails is not a
   wrong calculation; it is no calculation.
2. **Failure mode — the correction is applied to the *reported* p-value rather than
   to the decision threshold.** Both work arithmetically, but reporting an uncorrected
   significance level beside a corrected decision invites the reader to see a pass
   that did not happen. Publish the threshold.
3. **Failure mode — the search is hidden inside a "systematic" process.** Renaming
   parameter sweeps as "optimisation" does not remove them from `m`.
4. **Failure mode — a single lucky cycle is treated as the end of the search.** One
   cycle is one draw. Its expectation, if the true edge is zero, is not zero — it is
   `se_E` scaled by whatever the draw happened to be.
5. **Failure mode — negative cycles are excluded as "not representative".** Every
   excluded cycle is a draw removed from the denominator of `m`, and the surviving
   result is a maximum over fewer draws — the arithmetic is unchanged, only the
   correction is lost.
6. **Failure mode — the holdout is used more than once.** A second use makes it part
   of the fit. Three holdout checks over three cycles are three tests, not one.
7. **Failure mode — a searched card is traded at full size.** The size band belongs
   to `trade-sizing-recovery`, and it is computed from a `p` and `b` that the search
   has already inflated. Sizing on a selected estimate compounds the overstatement.
8. **Failure mode — "I only changed the stop" is used to argue the cycles are one
   hypothesis.** The stop *is* the parameter. Changing it five times is five
   hypotheses over one parameter, which is exactly the case Bonferroni covers.
9. **Failure mode — the five-cycle rule is extended "one more time" because the last
   cycle was close.** The cycle that was close was the fifth draw. The sixth draw is
   the sixth draw, and the bar rises.
10. **Failure mode — the overstatement table is read as a guarantee.** `E[max_m] × se_E`
    is an expectation. The realised overstatement is a random variable with its own
    spread, and the realised value exceeds the expectation about half the time.

---

## Worked check

```bash
# the un-searched bar, at se_E = 0.0443 R (b = 0.5, p = 0.68, n = 250)
py -3 scripts/payoff_check.py --tp 0.5 --sl 1.0 --p 0.68

# a card that clears the un-searched bar comfortably, for contrast
py -3 scripts/payoff_check.py --tp 2.5 --sl 1.0 --p 0.35 --cost-r 0.02
```

The first card's true edge is `+0.0200R`; the Bonferroni bar after 5 cycles is
`0.1141R`. The second card's edge is `+0.2250R` gross — larger than the
5-cycle bar and larger than the 50-cycle bar (`0.1458R`). **An edge large enough to
survive a search is a different thing from an edge large enough to pass once.**

See also: `references/the-iteration-protocol.md`,
`references/what-this-cannot-promise.md`,
`references/from-negative-to-positive-walkthrough.md`.
