# Cohort Attribution and the Kill List

A pooled `E_net` describes a portfolio of strategies, not a strategy. The shipped
illustrative ledger makes the point in one line:

```
POOLED   n=200  p=0.510000  b=0.962557  E_net=-0.028935   verdict NEGATIVE EDGE
SETUP-TREND   n=62  p=0.5000  b=1.5304  E_net=+0.2447     verdict KEEP
```

`[VERIFIED]` — both rows are the engine's actual output. The pooled mean describes
neither the good cohort nor the three others. Cohort attribution is not an
optimisation step; it is the minimum bar for knowing what you own.

---

## 1. Which cohort dimensions are worth the sample they cost

A cohort dimension consumes trades: splitting 200 trades into 12 month buckets
leaves about 14 per bucket, and 14 is below the 30-trade floor, so every verdict
becomes `INSUFFICIENT`. The engine groups on six dimensions, in rough order of
usefulness:

| Dimension | What it corresponds to | Verdict quality |
|---|---|---|
| `setup` | **A decision you make at entry and can stop making** | Best. Kill on this first |
| `side` | A structural decision (long/short, call/put, debit/credit) | Good, and often overlaps `setup` |
| `dte` bucket | Holding-period regime | Good, but correlates with `setup` |
| `iv_rank` bucket | Volatility regime at entry | Good, and the closest thing to a regime split a trade ledger can carry |
| `symbol` | Instrument | Useful for concentration and for spotting a single bad name |
| `month` | Time | Diagnostic only. Months are not decisions |

The rule: **kill on `setup`.** `setup` is the only dimension that maps to something
a trader is free to stop doing tomorrow. Killing a month is not a decision; killing
`SETUP-FADE` is.

---

## 2. The three verdicts, and why the floor is 30

```
n < 30                → INSUFFICIENT (n<30)      nothing is concluded
n >= 30 and E_net <= 0 → KILL (E_net<=0 with n>=30)
n >= 30 and E_net > 0  → KEEP
```

**Why 30.** It is a rule of thumb, not a theorem, and it is printed in the
engine's `SETTINGS` block so a reader can disagree with it. At `n = 30`, a win
rate near `0.5` has a standard error of about `0.091`; a two-sigma band on `p` is
therefore about `±0.18`. That is wide, and it is *supposed* to be wide: the verdict
is not "this cohort is proven", it is "this cohort has enough data that its sign
is worth acting on". Below 30 the sign of `E_net` is not even that.

**Why `E_net` and not `E`.** A cohort with a gross edge smaller than the cost of
trading it has no business being traded, and calling it `KEEP` on the gross number
is how a book fills up with slices that pay the broker and nobody else. The
`KEEP` verdict is a statement about net of cost.

**Why 30 does not override the multiple-testing bar.** These are different
questions. The floor asks "was this cohort big enough to look at"; the Bonferroni
bar asks "how many cohorts did I look at". A cohort can pass the floor and fail
the bar, and that is the normal case. See
`multiple-testing-in-cohort-mining.md`.

---

## 3. Reading the shipped illustrative cohort table

`[VERIFIED]` — the engine's actual panel 2, with the four constructed setups:

| Cohort | n | p | b | b\* | E | E_net | Verdict |
|---|---|---|---|---|---|---|---|
| `SETUP-TREND` | 62 | 0.5000 | 1.5304 | 1.0000 | +0.2746 | **+0.2447** | `KEEP` |
| `SETUP-FADE` | 60 | 0.4167 | 0.8974 | 1.4000 | −0.2229 | **−0.2527** | `KILL` |
| `SETUP-EVENT` | 23 | 0.5217 | 0.9678 | 0.9167 | +0.0285 | **−0.0013** | `INSUFFICIENT (n<30)` |
| `SETUP-CREDIT` | 55 | 0.6182 | 0.4956 | 0.6176 | −0.0750 | **−0.1048** | `KILL` |

Four lessons sit in that table:

1. **A high win rate is not a defence.** `SETUP-CREDIT` wins `61.8%` and is killed.
2. **A payoff below `b*` is fatal, and a payoff above `b*` is not sufficient.**
   `SETUP-EVENT` has `b = 0.9678 > b* = 0.9167` and still lands at
   `E_net = −0.0013R`, because cost is larger than its edge. Its `n` of 23 makes
   it `INSUFFICIENT` rather than `KILL`, but nothing about it is fundable.
3. **A negative cohort with a good payoff can exist.** `SETUP-FADE` has
   `b = 0.8974` against `b* = 1.4000`: at a `41.7%` win rate, a payoff of nearly
   `0.9` is nowhere near enough. Its fix is either a much wider target or a much
   higher win rate, and the table shows which is cheaper.
4. **The floor is doing work.** `SETUP-EVENT` has the second-highest `E_net` in
   the kill list's neighbourhood and is *not* killed, because 23 trades cannot
   decide anything. Calling it a `KILL` would be as wrong as calling it a `KEEP`.

---

## 4. Overlapping cohorts: count problems, not rows

The full kill list on that ledger has **10 rows**. It does not describe ten
problems.

```
iv_rank  IVR 25-50      n=54   E_net=-0.3071
setup    SETUP-FADE     n=60   E_net=-0.2527
symbol   SYN-B          n=40   E_net=-0.2193
side     short          n=105  E_net=-0.1054
setup    SETUP-CREDIT   n=55   E_net=-0.1048
symbol   SYN-D          n=40   E_net=-0.0991
dte      DTE 8-21       n=39   E_net=-0.0960
symbol   SYN-C          n=42   E_net=-0.0662
iv_rank  IVR 75-100     n=41   E_net=-0.0501
dte      DTE 46-90      n=57   E_net=-0.0285
```

`side=short` at `n = 105` is larger than any single setup cohort, and the overlap
explains why: it contains **58% of `SETUP-FADE` and 73% of `SETUP-CREDIT`**
`[COMPUTED]` — the two losing setups are overwhelmingly short-premium cohorts, so
`side=short` is largely those two cohorts wearing one label. `DTE 8-21` splits
along the same seam (42% of `FADE`, 0% of `CREDIT`), and `DTE 46-90` is the mirror
(0% of `FADE`, 58% of `CREDIT`), because the two setups were built with different
holding periods.

One row is **not** a duplicate. `IVR 25-50` has the worst `E_net` in the table at
`−0.3071` while overlapping only 22% of `FADE` and 31% of `CREDIT` `[COMPUTED]`.
It carries its own signal: a volatility-regime slice with an edge worse than either
setup it sits across.

**How to detect the overlap without a statistics package:** for each pair of killed
cohorts, count the trades in both. If the intersection is a large fraction of the
smaller cohort, the rows are one problem. The threshold is a judgement; the count
is not. Kill the row that corresponds to a decision — `setup` — and keep the
others as diagnostics, except where the overlap is small and the `E_net` is
materially worse, in which case you have found something new.

**Why this matters.** Treating ten overlapping rows as ten independent problems
produces a repair plan with ten items, eight of which are symptoms. A trader who
believes they have ten problems will change nothing.

---

## 5. Building cohorts that mean something

The cohort tag has to be decided **at entry**, not reconstructed afterwards.
A tag applied after the outcome is a label for how the trade went, and cohort
attribution on such a tag measures nothing at all. Concretely:

* **Tag the decision, not the result.** `credit-spread-30dte-trend-filter` is a
  decision. `bad-trade` is not.
* **Keep the number of tags small.** Three to five tags over a few hundred trades.
  Twelve tags on 80 trades are 6-trade cohorts and 6-trade cohorts are noise.
* **Keep the tags stable.** Re-tagging the history when a new taxonomy arrives
  destroys the time series. Add a tag and re-tag forward; do not rewrite the past.
* **Do not tag on the exit.** "Closed early" is an outcome, not a setup; if early
  closure is a real decision rule, it belongs in the payoff rule
  (`payoff-rule-engineering.md`), not in the cohort key.
* **Record `side`, `dte` and `iv_rank` at entry.** They are free to record and
  they are the closest thing a closed-trade ledger has to a regime split.

---

## 6. Failure modes of the kill list itself

1. **Failure mode — killing on a sample below the floor.** A 12-trade month with
   `E_net = −0.2R` looks decisive and is not. The floor is enforced in code, not
   by discipline, so the verdict is `INSUFFICIENT` whether or not it feels
   otherwise.
2. **Failure mode — counting overlapping rows as independent problems.** Covered
   above; it inflates the repair plan and de-motivates the trader.
3. **Failure mode — killing the cohort that is easiest to kill rather than the
   one that is largest.** The kill list is sorted by `E_net`, but the largest
   loss-making cohort by trade count is usually the bigger prize. Read `n × E_net`
   as well as `E_net`.
4. **Failure mode — killing everything and leaving no book.** If every cohort
   with `n >= 30` is negative, the problem is not any cohort; it is cost, or `b*`
   at the book level. Kill the book, not the slices.
5. **Failure mode — keeping a cohort because it is the one that is liked.** The
   `KEEP` verdict requires `n >= 30` **and** `E_net > 0`. A favourite setup with
   `E_net = −0.01R` is a `KILL`, and the smallness of the number is the whole
   reason it survives unnoticed.
6. **Failure mode — reading a `KEEP` as an endorsement.** `KEEP` means "this slice
   is not currently negative on 30 or more trades". It is not a claim of edge. The
   cohort still needs `n >= n_req` for its positive expectancy to be a finding.
7. **Failure mode — never re-running the screen.** A cohort killed in January can
   be positive in July after a rule change, and a cohort kept in January can be
   fatal after one. The screen is a routine, not a verdict for all time.

---

## 7. The one-page procedure

```
1. Export the ledger with a `setup` tag decided at entry, plus side/dte/iv_rank.
2. Run the engine. Read the pooled panel, then read the cohort table.
3. Take the KILL LIST as printed. For each row, note n and E_net.
4. Merge overlapping rows: same trades under two labels are one problem.
5. Rank the merged problems by n x |E_net| -- total damage, not rate.
6. Fix the top one with ONE rule change. Re-measure after 30 trades.
7. Re-run the screen on the next review date. It changes; that is the point.
```

The kill list is the cheapest lever in the skill. Stopping a slice costs nothing,
needs no market view, and can be done today. It cannot create edge — it can only
stop the bleeding from a slice that has none — and on most ledgers that is the
first several percentage points of improvement available.
