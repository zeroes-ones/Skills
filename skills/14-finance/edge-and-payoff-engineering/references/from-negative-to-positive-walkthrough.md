# From Negative to Positive — The Worked Walkthrough

This is the whole skill executed on one book in five steps. Every number below is
the engine's actual output on the shipped synthetic ledger, and every command is
given so the walkthrough can be reproduced.

> **The ledger is SYNTHETIC and ILLUSTRATIVE.** Nothing here is a claim that any
> strategy, setup or market behaves in any way. The purpose is to show the
> *procedure* on a book whose cohort structure is known by construction.

---

## Step 0 — the starting position

```bash
py -3 scripts/edge_engine.py --csv examples/logs/illustrative-cohorts-synthetic.csv
```

`[VERIFIED]` — the engine's pooled panel:

```
trades (n)                         200
decision mix                       102 wins / 98 losses / 0 break-even
win rate p = wins/(wins+losses)    0.510000
avg win (in unit)                  1.001614
avg loss (in unit)                 1.040577
payoff ratio b                     0.962557
expectancy E                       0.000941
cost drag c_R                      0.029875
net expectancy E_net               -0.028935
break-even payoff b*               0.960784
sd_R                               1.072301
n_req (2-sigma)                    5199305.93
years_at_current_pace              32882.67
VERDICT: NEGATIVE EDGE
```

Three things are already decided by those eleven lines:

* The book loses `0.028935R` per trade net of cost. **It is negative.**
* `b = 0.962557` is *above* `b* = 0.960784`, so this is **not** a payoff problem at
  the pooled level. The engine says so explicitly.
* `n_req` is `5,199,305.93` trades. **Do not try to prove this book.** Change it.

---

## Step 1 — name the binding constraint

`[VERIFIED]` — the engine's payoff panel on the same run:

```
  b = 0.9626 is at or above b* = 0.9608, so the payoff is not the
  binding constraint.
  *** COST IS THE BINDING CONSTRAINT: gross E = 0.0009 is
      smaller than c_R = 0.0299, so the book pays more to
      trade than it earns before costs. It does not have
      an edge; it has a rounding error and a bill. ***
```

So at the pooled level the answer is **cost**. But a pooled book is not a strategy,
and the pooled answer is about a blend. Before cutting cost, ask whether the blend
is hiding something.

---

## Step 2 — separate the cohorts and take the kill list

`[VERIFIED]` — the engine's cohort table, filtered to the four constructed setups
(the run prints 35 cohorts across six dimensions; these are the `setup` rows):

| Cohort | n | p | b | b\* | E | E_net | Verdict |
|---|---|---|---|---|---|---|---|
| `SETUP-TREND` | 62 | 0.5000 | 1.5304 | 1.0000 | +0.2746 | **+0.2447** | `KEEP` |
| `SETUP-FADE` | 60 | 0.4167 | 0.8974 | 1.4000 | −0.2229 | **−0.2527** | `KILL` |
| `SETUP-EVENT` | 23 | 0.5217 | 0.9678 | 0.9167 | +0.0285 | **−0.0013** | `INSUFFICIENT (n<30)` |
| `SETUP-CREDIT` | 55 | 0.6182 | 0.4956 | 0.6176 | −0.0750 | **−0.1048** | `KILL` |

The pooled `−0.028935R` describes none of these four. Two are killed, one is
undecidable, and one is clearly positive.

**Two distinct problems, not one:**

* `SETUP-FADE` is a **win-rate problem**: `p = 0.4167` against a break-even payoff
  of `1.4000`. It does not win often enough to matter how much it makes when it
  wins.
* `SETUP-CREDIT` is a **payoff problem**: `p = 0.6182` — a good win rate — against
  `b = 0.4956` when `b* = 0.6176`. It wins most trades and loses money. This is
  the disposition trap.

And `SETUP-EVENT` is neither: `b = 0.9678` clears its `b* = 0.9167`, and its
`E_net = −0.0013R` is negative because **cost is larger than its edge**. Its `n` of
23 makes it undecidable rather than killed.

---

## Step 3 — fix the disposition cohort with the right lever

`SETUP-CREDIT`: `p = 0.618182`, `b = 0.495589`, `b* = 0.617647`,
`E = −0.074962R`, `E_net = −0.104837R`.

Reproduce the cohort on its own:

```bash
grep '^#'      examples/logs/illustrative-cohorts-synthetic.csv >  /tmp/credit.csv
grep -v '^#'   examples/logs/illustrative-cohorts-synthetic.csv | head -1 >> /tmp/credit.csv
grep -v '^#'   examples/logs/illustrative-cohorts-synthetic.csv \
  | grep 'SETUP-CREDIT'                                   >> /tmp/credit.csv
py -3 scripts/edge_engine.py /tmp/credit.csv
```

`[VERIFIED]` — the engine's payoff panel for that cohort:

```
Observed p = 0.6182, observed b = 0.4956, b* = 0.6176, c_R = 0.0297

  E target     b needed       p* at that b   b net of cost
  +0.20R       0.9412         0.5152         0.9892
  +0.30R       1.1029         0.4755         1.1509
  +0.50R       1.4265         0.4121         1.4745

  b            E              E_net          note
  0.4956       -0.0755        -0.1051        ACTUAL b
  1.0000       0.2364         0.2067
  1.5000       0.5455         0.5158
  2.0000       0.8545         0.8249
  3.0000       1.4727         1.4431

  *** b = 0.4956 is BELOW b* = 0.6176. This book is structurally
      unprofitable at its current win rate: it is winning
      trades and losing money. That is the disposition
      effect expressed as arithmetic, not psychology. ***
```

**Fix A — raise `b` by holding to the target.** `b_needed = (E_target + 1 − p)/p`.
For `E = +0.2R`, `b` must go from `0.4956` to `0.9412` `[COMPUTED]`. If winners are
held to about `1R` instead of banked at `0.49R`, the ladder's `b = 1.0000` row
applies: `E_net` goes from `−0.1051R` to `+0.2067R` per trade.

**Fix B — raise `p` by filtering entries.** With `b` fixed, the net break-even win
rate is `(1 + c_R/avg_loss)/(1 + b) = 0.688621` `[COMPUTED]` (the engine's own
`c_R = 0.0297` for this cohort). That is a
**+7.0 percentage point** move — from `0.6182` to `0.6886` — before the cohort is
net positive at its current payoff.

**Fix A wins, and it is not close.** Fix A is a setting applied at entry. Fix B is
a search over entry filters with a seven-point target and no mechanical path to it.
On a high-win-rate, low-payoff book, the payoff is the binding constraint and the
payoff rule is the fix.

---

## Step 4 — fix the win-rate cohort

`SETUP-FADE`: `p = 0.416667`, `b = 0.897394`, `b* = 1.400000`,
`E = −0.222864R`, `E_net = −0.252740R`.

`[COMPUTED]` — two candidate fixes, at the cohort's own average loss
(`1.0642R`) and its own cost drag (`c_R = 0.0288R`), using
`E = avg_loss × (p·b − (1−p))`:

| Fix | New value | `E` | `E_net` |
|---|---|---|---|
| Raise `b` to 1.50 (a 1.5-to-1 payoff) | `b = 1.50` | `+0.0443R` | `+0.0156R` |
| Raise `b` to 1.60 | `b = 1.60` | `+0.0887R` | `+0.0599R` |
| Raise `p` to 0.48 | `p = 0.48` | `−0.0950R` | `−0.1238R` |
| Raise `p` to 0.50 | `p = 0.50` | `−0.0546R` | `−0.0834R` |

Both levers, computed before anything is changed. Raising the win rate from
`0.4167` to `0.50` — a **+8.3 point** move — is still not enough: `E_net` stays
negative at `−0.0834R`. Raising the payoff to `1.6` turns it positive.

**Read the difference from Step 3.** On `SETUP-CREDIT` the payoff fix is worth
`+0.21R` and the win-rate fix is unrealistic. On `SETUP-FADE` the payoff fix is
worth `+0.06R` and the win-rate fix does not work at all. Two cohorts, two
different binding constraints, and only one thing distinguishes them: their `p`.

```
p > 0.55  ->  b is usually the binding constraint, and b is a setting
p < 0.45  ->  p is often the binding constraint, and p is a search
```

That single line is the most useful thing a trader can take from this walkthrough.

---

## Step 5 — check the whole book after the kills

Reproduce by deleting the two negative setup cohorts and re-running:

```bash
grep '^#'  examples/logs/illustrative-cohorts-synthetic.csv >  /tmp/trimmed.csv
grep -v '^#'  examples/logs/illustrative-cohorts-synthetic.csv | head -1 >> /tmp/trimmed.csv
grep -v '^#'  examples/logs/illustrative-cohorts-synthetic.csv \
  | tail -n +2 | grep -v -E 'SETUP-FADE|SETUP-CREDIT'   >> /tmp/trimmed.csv
py -3 scripts/edge_engine.py /tmp/trimmed.csv
```

`[VERIFIED]` — the engine's pooled panel on the trimmed book:

```
trades (n)                         85
decision mix                       43 wins / 42 losses / 0 break-even
win rate p = wins/(wins+losses)    0.505882
payoff ratio b                     1.370477
expectancy E                       0.208034
cost drag c_R                      0.030790
net expectancy E_net               0.177244
break-even payoff b*               0.976744
sd_R                               1.259131
n_req (2-sigma)                    146.53
years_at_current_pace              2.17
expectancy E                       0.208034   = mean of the per-trade values
E (closed form)                    0.199182   = p*b-(1-p); equal to E when avg loss = 1 unit
E (closed form x avg_loss)         0.208034   = that closed form x avg_loss: the same number as E
R_max (survival-derived risk/trade) 0.023493 of capital = 2,349.30
VERDICT: INSUFFICIENT SAMPLE (< n_req trades)
```

**Read the second verdict honestly.** `E_net` went from **−0.028935R** to
**+0.177244R**, and the verdict moved from `NEGATIVE EDGE` to
`INSUFFICIENT SAMPLE (< n_req trades)`. That is not the same as proof. 85 trades is
still short of the 147 that the remaining book's dispersion demands, and two years
and two months at its own pace of `67.64` trades a year would settle it.

Killing the two losing cohorts did not prove an edge. It produced a book that is
**worth continuing to measure**, which is the most a ledger can do.

Note too that `c_R` rose slightly, from `0.029875R` to `0.030790R` `[VERIFIED]`,
because the mean planned risk of the remaining 85 trades is slightly lower than
that of the full 200. Cost drag is a ratio, and it moves when the composition of
the book moves.

---

## Step 6 — size the fixed book from the streak

`[VERIFIED]` — the trimmed run's derivation:

```
expected longest losing streak L   6.302   = ln(N)/ln(1/(1-p)), N = 85
  same L, simulated                5.675   (20000 seeded trials)
R_max (survival-derived risk/trade) 0.023493 of capital = 2,349.30
  derivation                       D_tolerance 20,000.00 / (L 5.675 x safety 1.50)
```

At `p = 0.5059`, a **six-loss run is routine**. A trader risking `5%` per trade
would be down about `30%` on that run — past the stated `20%` tolerance — and would
then be trading recovery rather than edge. The derivation says `2.35%`, and it says
so with `D_tolerance`, `L` and `safety` all printed.

---

## The five steps, compressed

```
1. Run the engine. Read E_net, then b vs b*, then n_req vs n, then c_R.
2. Read the cohort table. One pooled number cannot describe a portfolio.
3. For each killed cohort, ask which of p or b is binding:
      p > 0.55 -> the payoff rule is the fix, and it is a setting.
      p < 0.45 -> the win rate is the fix, and it is a search.
4. Change ONE rule. Re-measure after 30 trades.
5. Size the surviving book from R_max = D_tolerance / (L x safety).
```

## What this walkthrough deliberately does not claim

* It does **not** claim the illustrative book can be made profitable in reality.
  The cohorts are constructed; the numbers are produced by a generator at a fixed
  seed; the file says SYNTHETIC in its name, its header, its provenance lines and
  every output it produces.
* It does **not** claim that killing two cohorts generalises. The point is the
  procedure: measure the binding constraint per cohort, change one thing, re-measure.
* It does **not** claim `+0.177244R` is an edge. The engine's verdict for that
  book is `INSUFFICIENT SAMPLE (< n_req trades)`, and that is the honest reading —
  85 trades against a required 147.
* It does **not** quote a typical win rate, a typical payoff, or a typical cost for
  any real strategy, because none was measured here.
