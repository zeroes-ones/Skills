# Multiple Testing in Cohort Mining

The engine screens cohorts on six dimensions. That is not one test; it is many,
run against the same ledger. This file is the arithmetic of why that matters, in
one page, plus a precise statement of what the correction cannot fix.

---

## 1. The problem, stated numerically

At a two-sided `alpha = 0.05`, a single test has a 5% chance of clearing the bar
when nothing is there. Run `m` independent tests and the probability that **at
least one** clears the bar by chance is:

```
family-wise false-positive rate = 1 - (1 - alpha)^m
```

| `m` tests | chance of at least one false positive |
|---|---|
| 1 | 5.0% |
| 3 | 14.3% |
| 5 | 22.6% |
| 10 | 40.1% |
| 20 | 64.2% |
| 35 | 83.4% |
| 50 | 92.3% |

`[COMPUTED]` — `1 − 0.95^35 = 0.8340`. The engine prints this figure next to the
cohort count on every run, using the run's own `m`.

So on the shipped illustrative ledger, which tests **35** cohorts, a naive
`|t| > 1.96` screen finds something about **83.4%** of the time whether or not an
edge exists anywhere in the book. That is what the engine's panel 3 means by
"screening is a multiple-testing problem".

---

## 2. The correction the engine applies

Bonferroni: to hold the family-wise error rate at `alpha` across `m` tests, test
each at `alpha/m`. For a two-sided test, the bar on `|t|` is the standard normal
critical value at tail `alpha/(2m)`:

```
alpha_adjusted = 0.05 / m
z_bar          = Phi^-1(1 - alpha_adjusted/2)
```

`[VERIFIED]` — on the shipped illustrative ledger the engine prints:

```
cohorts tested (m)            : 35
family-wise alpha             : 0.0500
Bonferroni-adjusted alpha     : 0.00142857
adjusted two-sided |t| bar z  : 3.1888
cohorts clearing ADJUSTED bar : 1 of 35
cohorts clearing a naive 1.96 : 2 of 35
```

Two cohorts clear the naive bar. **One** clears the adjusted bar of `3.1888`. The
gap between those two counts is the entire value of the correction, and the engine
prints both so the gap is visible rather than described.

The inverse normal CDF is implemented inside `scripts/edge_engine.py` (Acklam's
rational approximation, relative error below `1.15e-9`) so that the bar is
computed rather than looked up, and so the engine keeps its stdlib-only property.

---

## 3. What the correction cannot fix

`[VERIFIED]` — the single cohort that clears the adjusted bar on the shipped
ledger:

```
cohorts clearing the ADJUSTED bar, with their n:
  month    2026-08        n=2    t=-61.637
```

A two-trade month, both losses, produces `|t| = 61.637`. The number is
arithmetically correct: with two identical observations the sample standard
deviation is non-zero but tiny relative to the mean, so the t-statistic explodes.
It clears a bar of `3.1888` comfortably and it is **evidentially worthless**.

**Bonferroni answers "how many slices did I test?". It does not answer "was this
slice big enough to test?".** Those are different questions, and a correction for
the first cannot substitute for a floor on the second. That is exactly why the
engine:

1. prints the `n` of every cohort that clears the bar, beside its `t`;
2. forces the verdict `INSUFFICIENT (n<30)` on any cohort below the floor,
   regardless of how spectacular its `t` is; and
3. prints the sentence "READ n NEXT TO t" in the middle of the panel, because this
   is the single most misread output the engine produces.

---

## 4. A second, quieter problem: the tests are not independent

Bonferroni assumes the `m` tests are independent, or at least that this is a
conservative approximation. **They are not independent here.**

`side=short` contains 58% of `SETUP-FADE` and 73% of `SETUP-CREDIT`
`[COMPUTED]`. `DTE 8-21` is 42% `FADE`; `DTE 46-90` is 58% `CREDIT`. A cohort
screen over overlapping slices re-uses the same trades, so the effective number of
independent tests is smaller than `m` and Bonferroni is, in that specific sense,
*conservative* — it over-corrects. It is conservative in the direction that makes
false positives rarer and true finds harder to see, which is the safer direction
for a screen whose purpose is to prevent acting on noise.

The practical consequence is the opposite of the usual one: **when cohorts
overlap, do not read a failure to clear the bar as evidence that the cohorts are
fine.** It may only mean the correction was applied too many times to too few
independent observations. Reduce the cohort set to dimensions that are genuinely
distinct — `setup` and `iv_rank`, say — and re-run.

---

## 5. What to do instead of nothing

The correction is not a reason to stop looking. It is a reason to look *once*,
properly.

* **Pre-register the screen.** Decide which cohort dimensions will be screened and
  what `E_net` and `n` will trigger a `KILL` **before** looking at the table. A
  screen designed after seeing the data is a screen fitted to the data, and the
  fitted version will always find something.
* **Keep `m` small.** Three to five cohort dimensions on a few hundred trades.
  Every added dimension multiplies `m`, raises the bar, and consumes sample.
* **Read the adjusted count as the headline, not the naive count.** The engine
  prints both in that order for a reason.
* **Use the kill list, not the winner list.** Bonferroni protects against
  *believing* a positive slice. It is not needed to decide that a large negative
  slice with `n ≥ 30` should stop being traded — that decision is about avoiding a
  known loss, not about believing a discovery.
* **Report `m` in the state log.** A run with 35 cohorts and a run with 5 are not
  the same evidence, and the `m` is what makes them distinguishable later.

---

## 6. Failure modes

1. **Failure mode — screening many cohorts and reporting only the survivor.** The
   classic multiple-testing failure. `m` must be reported with the result; a
   survivor quoted without its `m` is not a finding, it is a selection.
2. **Failure mode — treating the naive `1.96` bar as the bar.** At `m = 35` that
   bar produces at least one false positive 83.4% of the time.
3. **Failure mode — treating the adjusted bar as sufficient.** A two-trade cohort
   clears it. Read `n`.
4. **Failure mode — adding cohort dimensions until something clears.** Each added
   dimension raises `m` and, past a point, the search itself becomes the error.
5. **Failure mode — ignoring overlap and over-correcting.** Bonferroni on
   overlapping slices hides real effects. Reduce the dimension set before
   concluding there is nothing.
6. **Failure mode — mining months.** A month is not a decision a trader can stop
   making. Fourteen month cohorts add fourteen to `m` and change nothing that can
   be acted on except the total.
7. **Failure mode — re-running the screen until a different cohort wins.** That is
   multiple testing across *runs*, which Bonferroni inside a run cannot see. The
   state log exists to make this visible.

---

## 7. The five-line summary

```
m = cohorts tested
alpha_adjusted = 0.05 / m
z_bar = Phi^-1(1 - alpha_adjusted/2)
report: m, z_bar, count clearing z_bar, and the n of every clearer
remember: the correction bounds the NUMBER of tests, not the SIZE of a cohort
```

The shipped illustrative ledger's numbers, verbatim: `m = 35`, `z_bar = 3.1888`,
`1 of 35` clearing against `2 of 35` at a naive `1.96`, and the single clearer is
a two-trade month. That panel is the whole lesson compressed into four lines, and
it is printed on every run whether or not anyone reads it.
