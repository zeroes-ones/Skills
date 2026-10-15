# How Many Trades to Know

```
n_req = 4 · (sd_R / |E|)²
years_at_current_pace = n_req / trades_per_year
```

This is the arithmetic of "is my edge real". It is a 2-sigma separation heuristic,
stated as such, and it is the single most deflating number the engine produces.
That is its job.

---

## 1. Where the formula comes from

You have `n` trades whose per-trade R-multiples have mean `E` and sample standard
deviation `sd_R`. The standard error of that mean is:

```
se_mean = sd_R / sqrt(n)
```

You want the mean to be **two standard errors from zero** — the conventional
`|t| >= 2` bar — so that noise alone would rarely produce a mean this large:

```
|E| >= 2 · sd_R / sqrt(n)
sqrt(n) >= 2 · sd_R / |E|
n >= 4 · (sd_R / |E|)²                      ∎
```

The `4` is the square of the `2`. A 3-sigma bar would use `9`, and a 1-sigma bar
would use `1`. The choice of `2` is a convention, disclosed in the output, and a
reader who wants a real power calculation instead of a heuristic should compute
one — this file says so explicitly rather than implying more rigour than there is.

---

## 2. What the number looks like on real shapes

`[COMPUTED]` — `n_req = 4·(sd_R/|E|)²`, assuming `sd_R ≈ 1.0`, which is close to
the case for a book losing approximately `1R` on losers:

| `E` (net, per trade) | `sd_R` | `n_req` | At 150 trades/year |
|---|---|---|---|
| +0.30R | 1.10 | 54 | 0.4 years |
| +0.20R | 1.10 | 121 | 0.8 years |
| +0.10R | 1.10 | 484 | 3.2 years |
| +0.05R | 1.10 | 1,936 | 12.9 years |
| +0.02R | 1.10 | 12,100 | 80.7 years |

`[VERIFIED]` — the shipped illustrative ledger, whose numbers are the engine's
rather than the table's: `E = 0.000941R`, `sd_R = 1.072301`, giving
`n_req (2-sigma) = 5199305.93` and `years_at_current_pace = 32882.67` at the
ledger's own pace of `158.12` trades a year. The engine prints those two figures
verbatim on every run of that file.

The last row is not hypothetical: it is the shipped illustrative ledger's pooled
`E = 0.000941R` with `sd_R = 1.072301`, and the engine prints
`n_req (2-sigma)  5199305.93` and `years_at_current_pace  32882.67` `[VERIFIED]`.

**Read the table as a warning about small edges, not as a target.** The distance
from `+0.10R` to `+0.02R` is a factor of 25 in required sample, and the distance
from `+0.02R` to `+0.0009R` is another factor of 430. Halving `E` quadruples
`n_req`; halving `sd_R` quarters it. Both directions matter, and only one of them
is under the trader's control.

---

## 3. The three ways to read `years_at_current_pace`

`trades_per_year` is computed from the ledger itself: `n` divided by the observed
close-date span in years. It is a measurement, not an assumption.

**Read 1 — under a year: a decision is available soon.** `n_req / pace < 1` means
the current book, if it keeps its `p`, `b` and dispersion, will be decidable within
a year. Keep trading and keep the rule stable.

**Read 2 — one to five years: the decision is expensive but possible.** The honest
move is usually to raise `|E|` rather than to wait. Cutting one losing cohort
raises the mean more cheaply than three more years of the same process.

**Read 3 — more than a decade: the number is a rejection.** A strategy whose edge
cannot be separated from zero inside a decade is not investable, whatever its
sign, because the trader will not keep the rule stable for a decade and the market
will not keep the same regime. This is the correct reading of `32,882.67`.

On the shipped trimmed book (after killing the two negative setup cohorts) the
engine prints `n_req = 146.53`, `years_at_current_pace = 2.17` `[VERIFIED]`. That
is read 2: possible, expensive, and worth doing because the alternative was a
negative book.

---

## 4. `sd_R` is the number nobody looks at, and it matters as much as `E`

`n_req` is quadratic in `sd_R`. A book with the same expectancy but half the
dispersion needs a quarter of the sample. Dispersion in R comes from three places:

* **Loss width variability.** If losses are all `−1R`, that term is small. If half
  the losses are `−1R` and half are `−2.5R`, the dispersion is large, and the book
  is not doing what it says it does.
* **Winner variability.** Wide, fat-tailed winners raise `sd_R` a lot while raising
  `E` only slightly. A single `+8R` winner is a large `sd_R` contribution and a
  modest `E` contribution.
* **Position-sizing variability.** If `risk` varies a lot trade to trade, `sd_R`
  reflects the sizing policy rather than the strategy. This is a reason to record
  risk per trade, not just P&L.

The engine prints `sd_R` on the pooled panel and per cohort, and it is the input
to `n_req` that a trader can actually reduce by tightening the payoff rule.

---

## 5. What `n_req` is not

1. **It is not a proof threshold.** Clearing it means the mean is two standard
   errors from zero, which is a conventional bar, not a demonstration. At the
   2-sigma bar, a book with no edge clears it about 5% of the time — before
   accounting for how many books were tried.
2. **It is not stable.** `n_req` is a function of the sample's `sd_R` and `E`.
   Both move as trades accumulate, so `n_req` moves too. A book that needs 400
   trades today can need 90 next month if two fat winners land.
3. **It is not a licence to trade more.** `n_req` is about how many *comparable*
   trades are needed. Trading more while changing the rule every month does not
   accumulate toward `n_req` at all — it produces several short samples, none of
   which is decididable.
4. **It is not the same as the confidence interval on `b`.** `n_req` bounds the
   *mean*, not the payoff ratio. A book can have a decididable mean and a `b` that
   is still uncertain.
5. **It does not include unrealised or unbooked trades.** A rolled position that
   has not closed is not in the sample, and the sample is therefore
   systematically short of the losses.

---

## 6. Failure modes

1. **Failure mode — quoting `E` without `n_req`.** A `+0.0009R` expectancy and a
   `+0.30R` expectancy print the same shape without the required sample beside
   them. The engine prints both on the same panel for this reason.
2. **Failure mode — treating `n_req` as a finish line.** It is a moving estimate.
   Recompute it every run; record it in the state log; watch it move.
3. **Failure mode — trading more while changing the rule.** The sample is only
   comparable if the process is. Rule churn resets the clock, and the clock is
   never announced as reset.
4. **Failure mode — ignoring `sd_R` while trying to fix `E`.** A book with a fat
   left tail has a large `sd_R` and a large `n_req`, and tightening the stop is
   often worth more than raising the win rate.
5. **Failure mode — deciding a strategy is dead because `n < n_req`.** The verdict
   is `INSUFFICIENT SAMPLE`, which means "not yet", not "no". The engine's wording
   is chosen carefully: a promising sign that is not yet a finding.
6. **Failure mode — using `n_req` on a cohort you already know is negative.** For
   a negative cohort with `n >= 30`, waiting for `n_req` to "confirm" is waiting to
   lose more money at a known-negative expectation. Sample size is for confirming
   positives, not for delaying negative verdicts.
7. **Failure mode — forgetting that `n_req` is per population.** The pooled
   `n_req` is not the cohort `n_req`; a book that pools to a positive number can
   have cohorts that individually need decades.

---

## 7. The decision procedure

```
1. Read E_net (net of cost, in R).
2. Read sd_R.
3. Compute n_req = 4*(sd_R/|E|)^2.
4. Compare n to n_req.
   n >= n_req  -> the sign is a finding. Size from R_max and continue.
   n <  n_req  -> compute years_at_current_pace.
                   < 1 year   -> keep trading, keep the rule stable.
                   1-5 years  -> change p, b or cost before waiting.
                   > 5 years  -> the edge is not separable from zero in a
                                 human horizon. Treat as a rejection.
5. Record n, n_req and the pace in the state log so the next run can see
   whether the required sample is falling (edge or dispersion improving) or
   rising (the book is drifting toward zero).
```

The most useful thing `n_req` does is not the verdict. It is the comparison across
runs: a `n_req` that falls month over month is a book getting more measurable, and
that is a real, reportable achievement even before the edge is proven.
