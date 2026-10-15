# FINDINGS — does adding option legs buy edge, or only shape?

**Every number below is `[MODELED]`.** No historical option quotes exist in
`data/*.csv`.  The option prices are constructed from the real VIX with
Black-Scholes and settled against the real index closes.  Read
[`README.md`](README.md) §2 before using any figure here.

Source pull **2026-10-14**; carry and run **2026-10-15**; window
**2001-03-13 … 2026-10-14**, 6 436 sessions, 24 complete calendar years, 306
complete months.  12 pre-registered structures × 7 variants × 3 indexes =
**252 sleeves**, 11 016 trades.

---

## 0. The answer, in one paragraph

**Legs buy shape. They do not reliably buy edge.**  Holding the view fixed,
`E_net` is **not monotone in leg count on any of the three views** (Test 1), and
a 4-leg structure beat its 1-/2-leg comparator on `E_net` in **1 of the 4
comparisons that exist** (Test 7).  The extra legs bought three real things — a
balanced payoff (net delta 10.7 → −0.1), a smaller tail in a crash year (2008:
−1.3R → −0.3R), and a flatter positivity profile across horizons (the M>Y
inversion disappears at 4 legs) — and they cost three real things: a doubled
per-leg fee, a **larger** dependence on the skew the model cannot see, and, in
the iron-fly case, a **terminal max loss so small (1.17 % of notional) that it no
longer normalises anything**, because the mark-to-market swing exceeds it.
The one structure whose `E_net` survives every robustness cell in View A is the
**2-leg short strangle** — and it is undefined-risk on the call side, so its `R`
is a stated stop, not a structural maximum loss.  **No 4-leg structure survives
the conservative skew direction in any view.**

---

## 1. Test 1 — is `E_net` monotone in leg count?

`E_form` is the skill's identity `p·b − (1−p)`; `E_R` is the sample mean in `R`;
`c_R` is the mean cost ÷ `R`; `E_net = E_R − c_R`.  Ordered by leg count within
each view.

### View A — "the index stays inside ±1σ" (range)

| id | legs | contracts | `p` | `b` | `E_form` | `E_R` | `c_R` | **`E_net`** | `E$`/10k/mo | flag |
|---|---|---|---|---|---|---|---|---|---|---|
| A1 | 2 | 2 | 0.8976 | 0.181 | +0.0599 | +0.0321 | 0.0140 | **+0.0181** | +181 | |
| A4 | 2 | 2 | 0.8769 | 0.470 | +0.2893 | +0.2303 | 0.0258 | **+0.2045** | +2045 | **UNDEFINED call side** |
| A2 | 4 | 4 | 0.8573 | 0.353 | +0.1596 | +0.0915 | 0.0313 | **+0.0602** | +602 | |
| A3 | 4 | 4 | 0.4194 | 1.451 | +0.0279 | +0.0271 | 0.1387 | **−0.1116** | −1116 | |

**Order by leg count: +0.0181 → +0.2045 → +0.0602 → −0.1116.  NOT monotone.**
The best `E_net` in View A is a **2-leg** structure.  The two 4-leg structures
land on opposite sides of zero, and the iron fly is the worst structure in the
entire study.

### View B — "the index rises" (directional)

| id | legs | contracts | `p` | `b` | `E_form` | `E_R` | `c_R` | **`E_net`** | `E$`/10k/mo |
|---|---|---|---|---|---|---|---|---|---|
| B1 | 1 | 1 | 0.2298 | 1.464 | −0.4336 | −0.4271 | 0.0275 | **−0.4546** | −4546 |
| B2 | 2 | 2 | 0.4510 | 1.448 | +0.1040 | +0.0953 | 0.0428 | **+0.0525** | +525 |
| B4 | 2 | **3** | 0.4804 | 0.262 | −0.3939 | −0.2121 | 0.0263 | **−0.2384** | −2384 |
| B3 | 2 | 2 | 0.4946 | 0.963 | −0.0290 | −0.0005 | 0.0007 | **−0.0012** | −12 |

**Order by leg count: −0.4546 → +0.0525 → −0.2384 → −0.0012.  NOT monotone.**
The 1-leg long call is the worst structure in the study after A3: it pays the
full debit every month and wins 23 % of the time.  The 2-leg **debit spread**
is the only positive structure in the view.  The ratio backspread — the
**convexity** structure, the one with unbounded gain — is the second-worst,
because convexity is paid for every month that nothing happens.

### View C — "harvest premium, no directional view" (carry)

| id | legs | contracts | `p` | `b` | `E_form` | `E_R` | `c_R` | **`E_net`** | `E$`/10k/mo |
|---|---|---|---|---|---|---|---|---|---|
| C1 | 1 | 1 | 0.9031 | 0.220 | +0.1021 | +0.0027 | 0.0004 | **+0.0023** | +23 |
| C4 | 1 | 1 | 0.7625 | 0.602 | +0.2215 | +0.0085 | 0.0003 | **+0.0081** | +81 |
| C2 | 2 | 1 | 0.6841 | 0.880 | +0.2858 | +0.0118 | 0.0008 | **+0.0109** | +109 |
| C3 | 2 | 2 | 0.8976 | 0.181 | +0.0599 | +0.0321 | 0.0140 | **+0.0181** | +181 |

**NOT monotone** (1, 1, 2, 2 legs).  Note the two 1-leg structures differ by 3.5×
on `E_net` and by 14 pp on `p` — **which 1-leg structure you pick matters more
than the leg count**.

### The `E_form` vs `E_R` gap, reported rather than hidden

`E_form` and `E_R` disagree, sometimes by a lot (A4: +0.2893 vs +0.2303; B4:
−0.3939 vs −0.2121).  They agree exactly only when the average loss is `1R`,
and `R` here is the **structure's maximum loss**, which most losses do not reach.
Neither is wrong; they are different statements about the same trades.  `E_R` is
used for every headline because `E_net = E_R − c_R` is the money.

### The skill's break-even reading, for cross-reference

`references/payoff-corners-for-options.md` says the whole question is whether the
measured `p` clears `p* = 1/(1+b)`.  The study prints both, and they agree with
`E_R`'s sign in every case:

| id | `p` | `p*` | clears? | `E_R` |
|---|---|---|---|---|
| A1 / C3 | 0.8976 | 0.8469 | **+5.1 pp** | +0.0321 |
| A2 | 0.8573 | 0.7393 | **+11.8 pp** | +0.0915 |
| A3 | 0.4194 | 0.4080 | +1.1 pp | +0.0271 |
| A4 | 0.8769 | 0.6801 | **+19.7 pp** | +0.2303 |
| B1 | 0.2298 | 0.4058 | **−17.6 pp** | −0.4271 |
| B2 | 0.4510 | 0.4085 | +4.3 pp | +0.0953 |
| B3 | 0.4946 | 0.5093 | −1.5 pp | −0.0005 |
| B4 | 0.4804 | 0.7926 | **−31.2 pp** | −0.2121 |
| C1 | 0.9031 | 0.8194 | +8.4 pp | +0.0027 |
| C2 | 0.6841 | 0.5321 | **+15.2 pp** | +0.0118 |
| C4 | 0.7625 | 0.6243 | **+13.8 pp** | +0.0085 |

Read the `p*` column against the skill's own table: the measured `b` values here
(0.18–1.45 for the premium structures) sit **well below** the 2.5 the skill's
long-premium card assumes, because none of these structures is managed to a
target — they are **held to expiry**, so the "payoff ratio" is whatever the
terminal distribution hands over. `A1` and `C3` land on `b = 0.181`, `p* = 84.7 %`:
that is the skill's `b = 0.25, p* = 80 %` row moved a little by the actual
terminal distribution.  **A structure held to expiry does not have the `b` its
management card advertises.**  That is worth stating, because every "income"
structure in the study is being graded on a `b` nobody chose.

**Plain answer to Test 1: NO.  More legs did not buy edge net of cost, on any
view.**

---

## 2. Test 2 — cost drag by leg count

Cost scales **linearly in legs at fixed `R`**; what makes it bite is that **`R`
does not scale with legs**.

| id | legs | contracts | cost $/trade | `R$`med | `c_R` LOW | `c_R` HIGH | `c_R` round-trip | `c_R*` = `E_R` | **`c_R*` in $** |
|---|---|---|---|---|---|---|---|---|---|
| A1 | 2 | 2 | 6.30 | 454.35 | 0.0140 | 0.0251 | 0.0280 | 0.0321 | **+14.59** |
| A2 | 4 | 4 | 12.60 | 407.25 | 0.0313 | 0.0561 | 0.0625 | 0.0915 | **+37.26** |
| A3 | 4 | 4 | 12.60 | 139.38 | 0.1387 | 0.2488 | 0.2775 | 0.0271 | **+3.78** |
| A4 | 2 | 2 | 6.30 | 287.44 | 0.0258 | 0.0462 | 0.0515 | 0.2303 | **+66.20** |
| B2 | 2 | 2 | 6.30 | 171.95 | 0.0428 | 0.0768 | 0.0856 | 0.0953 | **+16.38** |
| C1 | 1 | 1 | 3.15 | 11 754 | 0.0004 | 0.0006 | 0.0007 | 0.0027 | **+31.17** |
| C2 | 2 | 1 | 9.34 | 12 271 | 0.0008 | 0.0026 | 0.0017 | 0.0118 | **+144.48** |
| C4 | 1 | 1 | 3.15 | 12 134 | 0.0003 | 0.0006 | 0.0007 | 0.0085 | **+102.67** |

`c_R*` = `E_R` is the per-trade cost, in `R` units, at which the gross edge is
exactly consumed.  The dollar column is `c_R* × R$`med` — the **break-even cost
per trade**.

### The leg count at which cost consumes the whole gross edge

| view | at LOW prices | at HIGH prices |
|---|---|---|
| **A** | **legs = 4 (A3)**, `c_R/E_R` = **5.120** | **legs = 4 (A3)**, `c_R/E_R` = **9.183** |
| **B** | **NONE** — B1, B3, B4 have `E_R ≤ 0`, so there is no gross edge for cost to consume | **NONE** |
| **C** | **NONE** at any leg count | **NONE** |

**This is the sharpest cost result in the study, and it is not the one the
brief's framing expects.**  Cost does **not** kill these structures.  At LOW
prices the 2-leg put spread keeps 56 % of its gross edge and the 4-leg condor
keeps 66 %; even at HIGH prices the 4-leg condor keeps 39 %.  The only structure
whose cost exceeds its edge is **A3, and only because A3's `R` is one third of
the others'** — a 5-wide iron fly on a $100–$700 index has a terminal max loss of
**1.17 % of notional**.  Cost is not the problem there either; the structure just
barely has any edge at all (`E_R = +0.0271 R`, i.e. +$3.78 per contract per
month on a $388 credit — **0.97 % of the credit**).

The structures that lose money in this study lose it **on the payoff**, not on
the fee.  **Cost and outcome are essentially uncorrelated in View B:** B3 has the
**smallest** `c_R` in the view (0.0007 — because its `R` is 97 % of notional) and
the best tail, while B2 has the **largest** (0.0428) and the best `E_net`, and
B1 sits in between on cost (0.0275) and last on outcome.  The same holds in View
C: C2's `c_R` (0.0008) is 2× C1's (0.0004) and C2's `E_net` is 4.8× C1's.

**Where cost does decide the answer:** the round-trip setting.  A2's `E_net`
goes from **+0.0602 → −0.0023** between LOW and round-trip prices, and A1's from
**+0.0181 → −0.0099**.  If you close these structures early rather than letting
them expire — which is what the popular management cards say to do — the extra
legs' cost is enough to flip the whole view negative.  That is the real
leg-count cost finding: it is not the fee level, it is **whether you pay one
ticket or two per leg**.

---

## 3. Test 3 — the model-risk test: does skew sensitivity rise with leg count?

Strikes are held **fixed**; only the pricing vol of the stated legs moves by 1.5
vol points.  `|dE|` is the largest change in `E_R` across the three skew
variants.

| id | legs | sold legs | distinct option strikes | `E_R` base | `dE` sold +1.5 | `dE` sold −1.5 | `dE` all +1.5 | `|dE|$`med | `|dE|/|E_R|` |
|---|---|---|---|---|---|---|---|---|---|---|
| **A3** | 4 | 2 | 4 | +0.0271 | **+1.3680** | −0.2924 | +0.0620 | **+190.68** | **50.48** |
| **A2** | 4 | 2 | 4 | +0.0915 | +0.1352 | −0.0857 | +0.0402 | **+55.06** | 1.478 |
| A4 | 2 | 2 | 2 | +0.2303 | +0.1222 | −0.0925 | +0.1222 | +35.13 | 0.531 |
| C3 / A1 | 2 | 1 | 2 | +0.0321 | +0.0477 | −0.0378 | +0.0172 | +21.67 | 1.486 |
| C4 | 1 | 1 | 1 | +0.0085 | +0.0017 | −0.0017 | +0.0017 | +20.83 | 0.203 |
| B2 | 2 | 1 | 2 | +0.0953 | +0.1187 | −0.0925 | −0.0218 | +20.40 | 1.246 |
| C2 | 2 | 1 | 1 | +0.0118 | +0.0015 | −0.0015 | +0.0015 | +18.66 | 0.129 |
| B3 | 2 | 1 | 2 | −0.0005 | +0.0015 | −0.0015 | −0.0000 | +17.98 | 2.916 |
| B4 | 2 | 1 | 2 | −0.2121 | +0.0399 | −0.0358 | −0.0238 | +16.36 | 0.188 |
| **B1** | 1 | **0** | 1 | −0.4271 | **+0.0000** | **+0.0000** | −0.0666 | +8.96 | 0.156 |
| C1 | 1 | 1 | 1 | +0.0027 | +0.0011 | −0.0010 | +0.0011 | +12.95 | 0.415 |
| A2 vs A1 | | | | | | | | **2.54×** | |

**The hypothesis held partially, and the way it failed is the interesting part.**

- Ordered by `|dE|` in `R`: A3 > A2 > A4 > B2 > B1 > C3/A1 > B4 > C4 > C2 > B3 > C1.
  `Pearson(|dE|_R, leg count) = 0.66`.
- Ordered by `|dE|` in **dollars**: A3 > A2 > A4 > C3/A1 > C4 > B2 > C2 > B3 > B4 > C1 > B1.
  `Pearson(|dE|_$, leg count) = 0.75`, `Pearson(|dE|_$, distinct strikes) = 0.75`.
- **`|dE|` is NOT monotone in leg count.**  12 structures, 11 rank positions, and
  a 2-leg structure (A4) sits third while two other 2-leg structures (B3, B4) sit
  ninth and tenth.  Both correlations are ~0.7, not 1.0.

**What IS true, and is stronger than the hypothesis:** the two **4-leg**
structures are the two most skew-sensitive on **every** measure — in `R` units
and in dollars — and they are the top two by a wide margin (A3: $190.68/trade;
A2: $55.06; the best 2-leg: $35.13).  So *the count of legs does not determine
skew sensitivity, but the two structures with the most legs have the most.*

**The direction of the bias is not resolvable by this model, so both are
reported.**  `references/cost-drag-per-leg-and-per-rung.md` and the sibling
study both take the conservative direction — a real seller of an OTM option
collects **less** than the flat-vol value — and `SKEW_SOLD_M15` implements it.
The opposite direction (`SKEW_SOLD_P15`) is defensible too, because a real 16Δ
put trades at a *higher* IV than ATM.  This study cannot say which is right.  It
can say how much the answer depends on it:

| id | legs | `E_net` base | `E_net` sold −1.5 | `E_net` sold +1.5 | `E_net` all +1.5 | **swing** |
|---|---|---|---|---|---|---|
| **A3** | 4 | −0.1116 | −0.3320 | **+1.1385** | −0.0582 | **1.4705** |
| **A2** | 4 | +0.0602 | **−0.0229** | +0.1914 | +0.0993 | 0.2143 |
| A1 / C3 | 2 | +0.0181 | **−0.0192** | +0.0651 | +0.0351 | 0.0843 |
| **A4** | 2 | **+0.2045** | **+0.1141** | +0.3240 | +0.3240 | 0.2099 |
| B2 | 2 | +0.0525 | **−0.0363** | +0.1664 | +0.0315 | 0.2027 |
| C2 | 2 | +0.0109 | +0.0094 | +0.0124 | +0.0124 | 0.0030 |
| C4 | 1 | +0.0081 | +0.0064 | +0.0098 | +0.0098 | 0.0034 |
| C1 | 1 | +0.0023 | +0.0013 | +0.0034 | +0.0034 | 0.0021 |
| B1 | 1 | −0.4546 | −0.4546 | −0.4546 | −0.5179 | 0.0633 |

**Read the `E_net` sold −1.5 column against the base column.**  Under the
conservative skew direction:

- **A1 and A2 both flip NEGATIVE**, and A2 (`−0.0229`) ends up **worse** than A1
  (`−0.0192`).  The condor's whole advantage over the put spread in View A lives
  **inside the skew assumption**.
- **A3 collapses** from −0.11 to −0.33, and under the opposite direction explodes
  to +1.14 — a 1.47`R` swing on a 1.5-vol-point move.  A3's answer is a statement
  about skew, not about a strategy.
- **A4 is the only View-A structure that stays strongly positive** (+0.1141).  It
  is also the only one whose sold strikes are the 16Δ wings of a strangle rather
  than a spread's short leg, so the haircut bites it least in `R` terms.

The same haircut moves the **drawdowns** too: A2's cumulative-P&L drawdown goes
from **−31.2 % to −58.4 %** of the budget, A3's from −402 % to −470 %, A1's from
−31.7 % to −32.0 %.  **The 4-leg condor's tail is more skew-dependent than the
2-leg spread's.**

---

## 4. Test 4 — did the extra legs buy tail protection?

All figures in `R` units, comparable across structures.  `ddBudget` is the worst
peak-to-trough of the cumulative P&L on a fixed 10`R` budget; `worstM`/`worstY`
are the SUM of returns inside the period.

| id | legs | worst 1 % of trades | worst single trade | `ddBudget` | worst month | worst year | 2008 GFC | 2020 COVID | 2022 bear |
|---|---|---|---|---|---|---|---|---|---|
| A1 | 2 | −1.015 | −1.015 | −3.17 | −1.02 | −2.77 | **−1.3** (−2.6) | +0.2 (−1.8) | −2.8 (−2.9) |
| A2 | 4 | −1.035 | −1.036 | **−3.12** | −1.03 | **−2.41** | **−0.3** (−2.4) | **+0.8** (−2.0) | **−2.4** (−2.6) |
| A3 | 4 | **−1.625** | **−1.766** | **−40.20** | −1.54 | **−10.78** | +0.6 (−3.5) | **−10.8** (−12.8) | −1.2 (−7.9) |
| A4 | 2 | **−2.475** | **−3.231** | −6.04 | **−2.09** | −1.23 | −0.1 (−6.0) | +0.5 (−5.6) | +0.5 (−2.3) |
| B1 | 1 | −1.096 | −1.146 | **−133.12** | −1.10 | −11.28 | −13.9 (−14.1) | −3.6 (−6.5) | −7.0 (−7.1) |
| B2 | 2 | −1.142 | −1.182 | −18.87 | −1.10 | −6.34 | −6.8 (−9.1) | +6.7 (−3.6) | −4.3 (−5.4) |
| B3 | 2 | **−0.132** | −0.192 | **−0.76** | −0.13 | −0.33 | −0.4 (−0.5) | 0.0 (−0.3) | −0.2 (−0.2) |
| B4 | 2 | −1.021 | −1.035 | −65.04 | −0.91 | −5.78 | −1.4 (−1.9) | −3.6 (−3.8) | −0.4 (−1.2) |
| C1 | 1 | −0.089 | −0.149 | −0.28 | −0.08 | −0.10 | −0.1 (−0.3) | 0.0 (−0.2) | −0.0 (−0.1) |
| C2 | 2 | −0.154 | −0.213 | −0.52 | −0.16 | −0.27 | −0.3 (−0.5) | +0.3 (−0.3) | −0.2 (−0.2) |
| C3 | 2 | −1.015 | −1.015 | −3.17 | −1.02 | −2.77 | −1.3 (−2.6) | +0.2 (−1.8) | −2.8 (−2.9) |
| C4 | 1 | −0.137 | −0.196 | −0.43 | −0.14 | −0.17 | −0.2 (−0.4) | +0.2 (−0.3) | −0.1 (−0.1) |

### Did the extra legs buy tail protection?  **Sometimes — and the leg placement matters more than the count.**

- **The 4-leg condor (A2) beat the 2-leg put spread (A1) on every tail measure,
  and on 2008 by a factor of 4** (−0.3R vs −1.3R).  This **reproduces the
  sibling's finding in direction**: adding legs to a premium structure repairs
  the crash year.  But the sibling's version repaired 2008 from −11.97 % to
  −5.63 % **at a cost of −2.72 pp CAGR**; here the condor cost **nothing** — its
  `tot_R` over the window is **+28.00R against A1's +9.82R**, i.e. the condor is
  *better on both axes*.  The difference is that the sibling's extra leg was a
  **paid hedge**; this study's extra legs are a **sold call side**, which
  collects premium instead of paying it.
- **But the other 4-leg structure is the worst tail in the study.**  A3's
  `ddBudget` is **−40.20R**, versus A1's −3.17R — a **13× worse** drawdown, and
  its 2020 is −10.8R while A2's is +0.8R.  **Two structures, both 4 legs, same
  view, opposite tails.**
- **The worst first-percentile in View A belongs to the 2-leg strangle (A4,
  −2.475R)** — because A4 is the only *undefined-loss* structure, and its `R` is
  a stated 1.5σ stop that a bigger move simply exceeds.  Its worst trade is
  −3.231R.  **Leg count and tail risk are not the same axis as definedness of
  risk.**
- **The 1-leg structures have the smallest tails in absolute `R`** (C1 −0.28R,
  C4 −0.43R) — but that is largely a statement that their `R` is 94–98 % of
  notional, so almost nothing is small relative to it.  See §6.
- **The deepest drawdown in the whole study is the 1-leg long call B1 at
  −133.12R.**  B1's problem is not its tail; it is its mean.

**So: the extra legs bought tail protection when the extra leg was placed on the
side that pays in the scenario being protected against, and bought nothing when
it was not.  "Leg count" is the wrong variable; "which side the leg is on" is the
right one.**

---

## 5. Test 5 — does leg count change the positivity inversion?

`law` is the normal null `Φ(Sharpe_annual × √(period in years))`.  A **positive
gap** (`law − observed`) is the signature of negative skew: the normal law says
the horizon should be positive more often than it is.

| id | legs | Sharpe | M | M_law | **M_gap** | Q | Q_law | Q_gap | Y | Y_law | **Y_gap** | M > Y? |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A1 | 2 | 0.43 | 88.6 % | 54.9 % | **−33.7** | 80.4 % | 58.4 % | −21.9 | 83.3 % | 66.7 % | **−16.8** | **INVERTED** |
| A4 | 2 | 1.00 | 86.6 % | 61.4 % | −25.2 | 86.3 % | 69.2 % | −17.1 | 91.7 % | 84.2 % | −7.5 | |
| A2 | 4 | 0.97 | 83.7 % | 61.0 % | −22.6 | 81.4 % | 68.6 % | −12.8 | **87.5 %** | 83.2 % | **−4.1** | |
| A3 | 4 | 0.08 | 44.8 % | 51.0 % | **+6.2** | 53.9 % | 51.7 % | −2.3 | 50.0 % | 53.3 % | **+3.3** | |
| B1 | 1 | −1.04 | 22.5 % | 38.2 % | +15.6 | 20.6 % | 30.1 % | +9.5 | 4.2 % | 14.7 % | +10.7 | **INVERTED** |
| B2 | 2 | 0.33 | 47.4 % | 53.9 % | +6.5 | 56.9 % | 56.6 % | −0.2 | 54.2 % | 63.1 % | +8.9 | |
| B3 | 2 | −0.04 | 53.6 % | 49.5 % | −4.1 | 57.8 % | 49.1 % | −8.7 | 58.3 % | 48.4 % | −10.1 | |
| B4 | 2 | −2.50 | 41.2 % | 23.5 % | −17.6 | 16.7 % | 10.6 % | −6.1 | 0.0 % | 0.6 % | +0.6 | **INVERTED** |
| C1 | 1 | 0.39 | 88.6 % | 54.4 % | −34.1 | 85.3 % | 57.6 % | −27.7 | 83.3 % | 65.1 % | −18.3 | **INVERTED** |
| C4 | 1 | 0.77 | 75.2 % | 58.8 % | −16.4 | 77.5 % | 65.0 % | −12.5 | 83.3 % | 77.7 % | −5.5 | |
| C2 | 2 | 0.86 | 69.9 % | 59.7 % | −10.2 | 79.4 % | 66.5 % | −12.9 | 83.3 % | 80.3 % | −3.0 | |
| C3 | 2 | 0.43 | 88.6 % | 54.9 % | −33.7 | 80.4 % | 58.4 % | −21.9 | 83.3 % | 66.7 % | −16.8 | **INVERTED** |

**The sibling's inversion replicates, and leg count changes it.**

| leg count | structures | inverted (M > Y) | mean Y gap |
|---|---|---|---|
| **1** | 3 | **2 of 3** | **−4.4 pp** |
| **2** | 7 | **3 of 7** | **−6.4 pp** |
| **4** | 2 | **0 of 2** | **−0.4 pp** |

- The sibling found premium selling at 89 % months but only 79 % years for SPY
  and 80 % quarters.  Here A1/C3 (the same 2-leg put spread) shows **88.6 % M /
  80.4 % Q / 83.3 % Y** — the same shape.
- **At 4 legs the inversion disappears** (0 of 2).  The condor shows **83.7 % M /
  81.4 % Q / 87.5 % Y** — monthly positivity *below* yearly.  That is the normal
  `Φ(Sharpe√period)` order, not the inverted one.
- **But read the mechanism honestly.**  The condor did not repair the inversion by
  becoming a better structure; it repaired it by **lowering monthly positivity**
  (83.7 % vs A1's 88.6 %) while raising yearly (87.5 % vs 83.3 %).  It traded
  frequency for horizon-consistency.  That is exactly what "shape, not edge"
  means, and the condor's `E_net` advantage over A1 (§3) is only 0.0421R and does
  not survive the skew haircut.
- **A3 is the exception that proves the rule.**  Its positivity is flat across
  horizons (44.8 / 53.9 / 50.0) with a **positive** M and Y gap — the fly's
  payoff is so small relative to `R` that its "wins" are noise, and its Sharpe is
  0.08.  A flat positivity profile bought by having no edge is not an
  achievement.

**Answer: yes, leg count changes the inversion — but from 1 leg to 2 legs it does
not, and the 4-leg improvement comes from giving up monthly win frequency, not
from gaining expected value.**

---

## 6. What the extra legs actually buy: the Greek shape

Mean position Greeks **at entry**, per one unit, in share-equivalents per 100
shares.

| id | legs | net delta | net gamma | net vega | net theta | `R`/notional |
|---|---|---|---|---|---|---|
| A1 | 2 | **+10.7** | −3.10 | −4.92 | +1.91 | 3.68 % |
| A2 | 4 | **−0.1** | **−6.13** | **−9.50** | **+3.51** | 3.34 % |
| A3 | 4 | −1.2 | −6.30 | −5.63 | +2.03 | **1.17 %** |
| A4 | 2 | −1.3 | **−8.09** | **−23.74** | **+9.25** | 2.51 % |
| B1 | 1 | **+31.0** | +5.86 | +17.05 | −6.30 | 1.16 % |
| B2 | 2 | +25.1 | +1.21 | +3.70 | −1.19 | 1.47 % |
| B3 | 2 | **+60.2** | +0.20 | +0.33 | +0.57 | **97.09 %** |
| B4 | 2 | +0.9 | +4.18 | +11.95 | −4.62 | 3.56 % |
| C1 | 1 | +15.5 | −3.91 | −11.65 | +4.74 | **93.91 %** |
| C2 | 2 | **+69.0** | −5.86 | −17.05 | +6.30 | **98.84 %** |
| C4 | 1 | +46.6 | −6.57 | −19.29 | +8.06 | **97.62 %** |

**This table is the answer to the question in the title.**

- **Going from the 2-leg put spread (A1) to the 4-leg condor (A2) does not double
  the edge; it doubles the gamma (−3.10 → −6.13) and the vega (−4.92 → −9.50)
  and sets the delta to zero (+10.7 → −0.1).**  The extra legs buy **balance**:
  the payoff stops leaning on where the index happens to be at entry.  That is
  real, it is why the condor's 2008 is −0.3R instead of −1.3R, and it is a
  *shape* purchase.  The `E_net` purchase is +0.0421R and, per §3, does not
  survive the conservative skew direction.
- **In View B, leg count changes the Greeks by a factor of 30 with almost no
  change in edge.**  1 leg (B1): delta +31.0, vega +17.05.  2 legs (B2, debit
  spread): delta +25.1, vega +3.70.  2 legs (B4, backspread): delta +0.9, vega
  +11.95.  Three different shapes; `E_net` of +0.0525, −0.4546 and −0.2384.
  The legs moved the shape far more than the value.
- **In View C, the "1-leg" comparator is the expensive one in capital terms.**
  C1, C2 and C4 all carry `R` ≈ 94–99 % of notional, while the 2-leg put spread
  C3 carries **3.68 %**.  The 2-leg structure is one where the 1-leg ones are
  capital-prohibitive.

---

## 7. Test 7 — the verdict

`edge_per_tail` = `E_net ÷ |mean R of the worst 1 % of trades|`, the
pre-registered selection metric.  `E$`/10k/mo = 10 000 × `E_net`, the dollars of
expectancy per $10 000 of capital committed per month (capital = `R`).

### View A — range

| id | legs | `E_net` | worst 1 % | `ddBudget` | **`edge_per_tail`** | `E$`/10k/mo | u@$25k | flag |
|---|---|---|---|---|---|---|---|---|
| A4 | 2 | +0.2045 | −2.475 | −6.04 | **0.0826** | +2045 | 86 | **UNDEFINED call side** |
| A2 | 4 | +0.0602 | −1.035 | **−3.12** | **0.0582** | +602 | 61 | |
| A1 | 2 | +0.0181 | −1.015 | −3.17 | 0.0178 | +181 | 55 | |
| A3 | 4 | −0.1116 | −1.625 | −40.20 | −0.0687 | −1116 | 179 | |

**Best by `edge_per_tail`: A4 — a 2-leg structure.**  Best by raw `E_net`: A4
again.  The 4-leg condor beats the 2-leg put spread on both, but loses to the
2-leg strangle on both.

### View B — directional

| id | legs | `E_net` | worst 1 % | `ddBudget` | **`edge_per_tail`** | `E$`/10k/mo | u@$25k |
|---|---|---|---|---|---|---|---|
| **B2** | 2 | **+0.0525** | −1.142 | −18.87 | **0.0459** | +525 | 145 |
| B3 | 2 | −0.0012 | −0.132 | −0.76 | −0.0091 | −12 | 2 |
| B4 | 2 | −0.2384 | −1.021 | −65.04 | −0.2335 | −2384 | 61 |
| B1 | 1 | −0.4546 | −1.096 | −133.12 | −0.4146 | −4546 | 185 |

**Best: B2, a 2-leg structure.**  Both rules agree.

### View C — carry

| id | legs | `E_net` | worst 1 % | `ddBudget` | **`edge_per_tail`** | `E$`/10k/mo | u@$25k |
|---|---|---|---|---|---|---|---|
| C2 | 2 | +0.0109 | −0.154 | −0.52 | **0.0709** | +109 | 2 |
| C4 | 1 | +0.0081 | −0.137 | −0.43 | 0.0591 | +81 | 2 |
| C1 | 1 | +0.0023 | −0.089 | −0.28 | 0.0256 | +23 | 2 |
| C3 | 2 | +0.0181 | −1.015 | −3.17 | 0.0178 | +181 | 55 |

**Best by `edge_per_tail`: C2 (2 legs).**  Best by raw `E_net`: C3 (2 legs).
**The two 1-leg comparators rank 3rd and 4th of 4.**

### Does any 4-leg structure beat its 1-/2-leg comparator on `E_net`?

Only two structures in the whole set have 4 legs, both in View A.  That gives
**four** comparisons:

| comparison | `ΔE_net` | result |
|---|---|---|
| A2 (4 legs) vs **A1** (2 legs, same short put side) | **+0.0421** | **4-LEG WINS** |
| A2 (4 legs) vs **A4** (2 legs, undefined risk) | −0.1443 | 4-leg LOSES |
| A3 (4 legs) vs **A1** | −0.1297 | 4-leg LOSES |
| A3 (4 legs) vs **A4** | −0.3162 | 4-leg LOSES |

**One win in four.**  And the one win is the one that does not survive the
conservative skew haircut (§3): under `SKEW_SOLD_M15`, A2 = −0.0229 and
A1 = −0.0192, so the 4-leg structure is **worse** than the 2-leg one.

### The conditions under which a complex structure IS the right answer

There are five, and they are specific:

1. **When the view cannot be expressed with fewer legs.**  "The index stays
   inside a range" needs a payoff that pays on **both** sides.  No 1-leg
   structure does that; A1 and A4 express one side and *hope* for the other.  A2
   is the minimum-leg expression of a genuine two-sided range view, and its
   measured net delta is **−0.1 against A1's +10.7** — the difference between
   having a view and having a view plus a directional bet you did not state.
2. **When capital, not risk, is the binding constraint.**  Today's `R$5yr` for
   one cash-secured put (C1) is **$37 194** and for one covered call (C2) is
   **$39 123**.  **A $25 000 account cannot open one contract of either.**  At
   $25 000 the 2-leg put spread (C3, `R$5yr` = $427 → 58 units) is the **only**
   structure in View C that the account can express at all.  The extra leg is
   not a refinement there; it is the reason the view is reachable.
3. **When the objective is explicitly tail protection in a crash.**  A2's 2008 is
   **−0.3R against A1's −1.3R**, and its `ddBudget` is the smallest in View A
   (−3.12R) — and here it **costs no `E_net` to buy it**, because the extra legs
   sell premium instead of buying it.  This is the *opposite* of the sibling
   study's paid hedge, which cost −2.72 pp of CAGR.
4. **When the mandate is delta-neutral at entry and the model risk is
   understood.**  Only A2 delivers `|net delta| < 2` shares among the range
   structures.  The price of that is the most skew-sensitive payoff in the view
   short of A3 (§3), and a drawdown that goes from −31 % to −58 % of budget under
   the conservative skew direction.  **Take the condor for the balance, not for
   the edge.**
5. **When you pay one ticket per leg.**  A2's `E_net` is **+0.0602** at LOW,
   **+0.0106** at HIGH, and **−0.0023** at round-trip prices.  A structure whose
   entire edge is inside the cost assumption is not a structure you can close
   early.

**And the conditions under which it is not:** when the extra legs are placed on
the *same* side as the view (A3 — the fly's 4 legs buy a 1.17 %-of-notional max
loss and a −40R drawdown, the worst tail in the study); when the extra leg only
adds convexity you cannot afford to hold (B4 — the backspread is the second-worst
structure in View B, because convexity is a monthly debit until the month it is
not); and when the extra legs merely re-express a one-sided view (A2 vs A1 — the
one 4-leg win that does not survive a skew haircut).

---

## 8. The capital finding, which the brief did not ask for and matters anyway

`R` is the structure's maximum loss, so **capital = `R`**, so `E_net` in `R` units
**is** the return on a risk budget — the structures are comparable in `R` provided
you can commit 10 of them.  They are **not** comparable in capital.

| id | legs | `R`/notional | `R$` median era | **`R$` last 5 years** | units at $25k (median era) | units at $25k **today** |
|---|---|---|---|---|---|---|
| A2 | 4 | **3.34 %** | 407 | **363** | 61 | **68** |
| A1 / C3 | 2 | 3.68 % | 454 | **427** | 55 | **58** |
| A3 | 4 | **1.17 %** | 139 | **43.6** | 179 | **572** |
| A4 | 2 | 2.51 % | 287 | 967 | 86 | 25 |
| C1 | 1 | **93.91 %** | 11 754 | **37 194** | 2 | **0** |
| C2 | 2 | **98.84 %** | 12 271 | **39 123** | 2 | **0** |
| C4 | 1 | **97.62 %** | 12 134 | **38 516** | 2 | **0** |
| B3 | 2 | **97.09 %** | 12 064 | 38 323 | 2 | **0** |

**The carry view's two 1-leg comparators cannot be traded at all in a $25 000
account today**, and neither can the risk reversal.  This is
`references/small-account-instrument-choice.md`'s point arriving as a measurement:
the **leg count you can actually trade is set by your capital, not by your view**.
It is also why `E$`/10k/mo must be read with `u@25k` beside it — an `E_net` you
cannot buy is not an option.

And the era warning cuts the other way for the long-premium structures: B1's
`R$med` is **$135** but its **`R$5yr` is $424** — three times the risk per
contract today than in a median year of the window.  A 25-year median understates
today's position size for every long-option structure and overstates it for every
short-put structure.

---

## 9. What this study cannot see, stated plainly

1. **No bid/ask, no legging risk, no partial fill.**  A 4-leg structure is
   assumed to fill as one ticket at the mid.  In reality the 4-leg structure has
   four legs' worth of legging risk and the 1-leg structure has none, and this
   study **cannot see that at all**.  Every 4-leg `E_net` here is optimistic
   relative to a real fill.
2. **No skew.**  §3 shows this matters more for the 4-leg structures than for any
   others.  The model cannot say which direction of the bias is right.
3. **No assignment.**  Every short-put structure here is European; a real
   American short put gets assigned.
4. **No dividends.**  Every modelled call is too expensive and every modelled put
   too cheap, and the bias compounds with the number of call legs.
5. **No margin model.**  A4's `R` is a stated ±1.5σ stop; a real broker margins a
   short strangle against the whole underlying.  Its `E$`/10k/mo of +2045 is
   therefore **not achievable**; the honest reading is "the only View-A structure
   whose edge survives the skew haircut, at a capital cost this study does not
   model".
6. **The window contains 24 complete calendar years and 306 complete months.**
   That is enough to see a tail, not enough to grade every corner.  The
   pre-registered `n_req = 4(sd/|E_R|)²` says how much evidence each structure's
   own edge needs, and against the **918 trades available per structure**:

   | structure | `n_req` | 918 available? |
   |---|---|---|
   | A3 iron fly | **17 266** | **no — 5 % of the requirement** |
   | B3 risk reversal | **13 197** | **no — 7 %** |
   | B2 debit spread | 646 | yes, with 1.4× headroom |
   | A1 / C3 put spread | 214 | yes |
   | C1 cash-secured put | 100 | yes |
   | C2 covered call | 62 | yes |
   | C4 short ATM put | 61 | yes |
   | A2 iron condor | 50 | yes |
   | B1 long call | 32 | yes |
   | A4 short strangle | 17 | yes |
   | B4 ratio backspread | 15 | yes |

   **A3 and B3 cannot be resolved by this window at all** — their `E_net` is
   indistinguishable from zero at two sigma, which is a further reason not to
   read A3's `c_R/E_R` of 5.12 as a measured verdict.  **B2's positive `E_net` is
   real but thinly evidenced** (1.4× headroom on a two-sigma test — i.e. about
   1.2 sigma of evidence, not two).  The premium-selling results in View A rest
   on the centre of the distribution and are the best-evidenced in the study;
   the View-B long-premium results rest on the tails and are the least.
7. **Twelve structures that were pre-registered, and no others.**  Nothing here
   says anything about a structure that was not on the list.  In particular the
   diagonal, the calendar, the jade lizard, the broken-wing butterfly and every
   3-leg structure are absent, because the brief asked for 1, 2 and 4 legs.

---

## 10. What would change the answer

- **A real skew surface.**  The two 4-leg structures are the two most
  skew-sensitive; a real surface could plausibly reverse A2's 0.0421R advantage
  over A1, and would very likely remove A3 entirely.
- **Real quotes.**  A 4-leg structure crossed at the bid/ask four times may not
  clear its own cost, and this study cannot price that.
- **A different leg placement, at the same leg count.**  A2 and A3 are both 4
  legs, both in View A, and their tails differ by 13×.  **Leg count is not the
  variable that matters.**  The variable that matters is which side of the payoff
  each leg lands on — and that is a design decision a trader makes, not a
  property of how many legs there are.

---

## 11. The one-sentence version

**Adding legs buys shape — balance, tails, a different Greek profile — and it
buying edge is the exception, not the rule: on three views it was not monotone
in leg count, it won one of four available 4-leg comparisons, and that one win
does not survive the skew the model cannot see.  Complex structures are the right
answer when the view itself needs both sides, when capital blocks the simple
version, or when the objective is explicitly a crash tail — and the number of
legs is not what decides it.**
