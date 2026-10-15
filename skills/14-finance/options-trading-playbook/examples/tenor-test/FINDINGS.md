# FINDINGS — does tenor buy edge, or only change the clock?

**Every number below is `[MODELED]`.** No historical option quotes exist in
`data/*.csv`. Option prices are constructed from the real VIX with Black-Scholes
and settled against the real index closes. Read [`README.md`](README.md) §4
before using any figure here.

Sources pulled **2026-10-14**; carried and run **2026-10-15**; window
**2001-03-13 … 2026-10-14**, 6 436 sessions, 25.59 years, 306 complete months,
24 complete years. **7 structures × 9 tenors = 63 cells per index × 3 indexes =
189 sleeves × 3 variants = 567 simulated sleeves.**

The grid is pre-registered in `README.md` §3 and asserted at run time
(`CELLS ACTUALLY STATISTICISED (variant BASE): 63 … matches: YES`).
**0DTE is not one of the 63** — it cannot be backtested from daily bars.

---

## 0. The answer, in one paragraph

**Tenor does not buy edge. It buys a different clock, a different tail, and a
different bill.** Holding structure and view fixed, `E_net` is **not monotone in
tenor for 6 of the 7 structures**; the one that *is* monotone (the covered call,
`INCREASING 8 up 0 flat`) is monotone because it is long the **realised equity
risk premium**, which accumulates over the holding period — a property of the
window, not of the option (limitation N6). The only two structures whose `E_net`
peaks **interior** are the two that actually sell premium — the short put spread
and the iron condor, **both at 180 DTE** — and that peak survives an independent
scale control (Appendix A). Per unit of risk, **short tenor is paid 6.8× to 104×
more per calendar day than long tenor** (Test 2), and that is the whole of the
"tenor edge": theta does not compound, it decays as `1/√day`. What the long
tenors buy is a **shallower drawdown** and a **cheaper ticket per unit of R**;
what they cost is **3–4× more skew dependence**, a **shrinking sample** (16 of 63
cells unmeasurable, 4 of 7 in the LEAPS bucket), and — under a **fixed dollar
wing** — a payoff whose structural maximum loss fires **more** often, not less.

---

## 1. Test 1 — is anything monotone in tenor?

`E` is gross (settlement P&L ÷ R); `c_R` is the headline LOW cost ÷ R;
`E_net = E − c_R`; `cr/W` is the premium per share as a fraction of the declared
width; `theta/day/R` is the credit ÷ tenor days ÷ R; `ann_R_net` is the
annualised return on 1R continuously committed.

### The whole grid in one view — `E_net` by structure × DTE

| id | 7 | 14 | 30 | 45 | 60 | 90 | 180 | 365 | 730 | monotone? |
|---|---|---|---|---|---|---|---|---|---|---|
| **S1** long call ~50Δ | −0.1321 | −0.1337 | −0.1027 | −0.0594 | −0.0899 | −0.0156 | +0.1461 | +0.3392 | **+1.0714** | NOT (3 sign changes) |
| **S2** cash-secured put ~16Δ | +0.0007 | +0.0012 | +0.0019 | +0.0014 | +0.0051 | +0.0043 | +0.0075 | +0.0172 | **+0.0206** | NOT (4) |
| **S3** short put spread 16Δ/5-wide | +0.0172 | +0.0247 | +0.0394 | +0.0311 | +0.0652 | +0.0516 | **+0.1277** | +0.1133 | +0.0964 | NOT (5) |
| **S4** bull call debit spread | −0.0194 | +0.0277 | +0.1497 | +0.1916 | +0.1765 | +0.3071 | +0.4625 | +0.6404 | **+1.1173** | NOT (2) |
| **S5** covered call | +0.0033 | +0.0066 | +0.0143 | +0.0173 | +0.0251 | +0.0335 | +0.0630 | +0.1147 | **+0.2104** | **INCREASING** |
| **S6** iron condor 16Δ/5-wide | +0.0403 | +0.0650 | +0.1052 | +0.0873 | +0.1463 | +0.1300 | **+0.1979** | +0.1391 | **−0.0910** | NOT (5) |
| **S7** iron butterfly ATM/5-wide | **+0.0878** | +0.0701 | −0.0039 | −0.1169 | −0.0571 | −0.2733 | −0.4395 | −0.4260 | −0.4801 | NOT (4) |

**Six of seven are not monotone.** Nothing here supports "more tenor, more edge".

Where the peak sits, and where the daily yield peaks:

| id | peak `E_net` DTE | where | peak `theta/day/R` DTE |
|---|---|---|---|
| S1 long call | 730 | endpoint | 730 |
| S2 cash-secured put | 730 | endpoint | 7 |
| **S3 short put spread** | **180** | **INTERIOR** | 7 |
| S4 debit spread | 730 | endpoint | 730 |
| S5 covered call | 730 | endpoint | 7 |
| **S6 iron condor** | **180** | **INTERIOR** | 7 |
| S7 iron butterfly | 7 | endpoint | 7 |

**The two interior peaks are both at 180 DTE and both belong to the premium
sellers.** The endpoint peaks belong to the structures long the risk premium
(S1, S4, S5) or long the cash-secured carry (S2) — for those, the 730-DTE number
must be read as *"two years of equity risk premium, harvested once per two
years"*, not as a tenor effect. S4's `E_net` of +1.1173R at 730 DTE on 36 trades
is the clearest case: it is a levered claim on a 25-year up-market, and it is
marked **UNMEASURABLE-adjacent** by sample size for S1 and S2 (4 and 6 of 9
tenors measurable).

### The same grid at HIGH cost and round-trip cost

| id | 7 | 30 | 90 | 180 | 365 | 730 |
|---|---|---|---|---|---|---|
| HIGH: S3 | +0.0064 | +0.0282 | +0.0401 | +0.1158 | +0.1010 | +0.0835 |
| HIGH: S6 | +0.0170 | +0.0803 | +0.1039 | +0.1709 | +0.1114 | **−0.1197** |
| RT: S3 | +0.0036 | +0.0253 | +0.0371 | +0.1127 | +0.0979 | +0.0801 |
| RT: S6 | +0.0109 | +0.0738 | +0.0971 | +0.1639 | +0.1042 | **−0.1272** |
| RT: S4 | **−0.1071** | +0.1073 | +0.2819 | +0.4441 | +0.6262 | +1.1060 |

The premium-selling cells survive a doubling of cost, but **the 730-DTE condor
goes from −0.0910 to −0.1197 at HIGH and −0.1272 at round-trip**: its long-tenor
gross edge is already negative, and cost deepens it.

---

## 2. Test 2 — the risk-efficiency curve, and the cleanest result here

`theta/day/R` = median credit ÷ (tenor days × median R) — the fraction of the
risk budget earned or paid per calendar day.

| `theta/day/R` | 7 | 14 | 30 | 45 | 60 | 90 | 180 | 365 | 730 | @7 ÷ @730 |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | −0.14286 | −0.07143 | −0.03333 | −0.02222 | −0.01667 | −0.01111 | −0.00556 | −0.00274 | −0.00137 | **104.3×** |
| S2 | +0.00034 | +0.00025 | +0.00017 | +0.00014 | +0.00013 | +0.00010 | +0.00008 | +0.00006 | +0.00005 | **6.8×** |
| S3 | +0.00838 | +0.00582 | +0.00362 | +0.00268 | +0.00231 | +0.00171 | +0.00101 | +0.00059 | +0.00037 | **22.9×** |
| S4 | −0.14286 | −0.07143 | −0.03333 | −0.02222 | −0.01667 | −0.01111 | −0.00556 | −0.00274 | −0.00137 | **104.3×** |
| S5 | +0.00076 | +0.00053 | +0.00036 | +0.00030 | +0.00025 | +0.00020 | +0.00015 | +0.00009 | +0.00007 | **10.9×** |
| S6 | +0.01928 | +0.01281 | +0.00782 | +0.00586 | +0.00478 | +0.00341 | +0.00199 | +0.00105 | +0.00057 | **33.8×** |
| S7 | +0.15122 | +0.12126 | +0.09275 | +0.07850 | +0.07037 | +0.05715 | +0.04455 | +0.02595 | +0.01206 | **12.5×** |

**"Short tenor is better paid per day" is confirmed, decisively, for every
structure in the grid** — and for two of them it is not a measurement but an
identity:

> **A fully-debit structure's `theta/day/R` is exactly `−1/D`.** S1 and S4 show
> −1/7, −1/14, −1/30 … −1/730, to the printed precision. Their credit *is*
> −1 × their `R`, so the ratio is the reciprocal of the day count and nothing
> else. **A position that spends its whole `R` on premium bleeds `1/D` of its own
> maximum loss every calendar day, and only the tenor decides how big that is.**
> `[COMPUTED]`

For the five credit structures the decay is monotone decreasing, from 6.8× (S2)
to 33.8× (S6).

### The mechanism, and the half of the hypothesis that fails

`theta/day/R × √DTE` is **not flat** — it falls for the width-defined structures
(S3: 0.0222 → 0.0099; S6: 0.0510 → 0.0155). The daily yield therefore decays
**faster than `1/√T`**, which is exactly what a **fixed dollar wing** does: the
wing is a shrinking fraction of `σ√T`, so the credit does not keep up with `√T`.
The printed `W/(Sσ√T)` column shows the drift: **1.44σ at 7 DTE against 0.15σ at
730 DTE** for every 5-wide structure.

**The second half of the hypothesis — that `E_net` peaks at an interior tenor —
holds for exactly two of seven structures, and both peaks are at 180 DTE.** So
the peak is *not* a general property of tenor. It appears where a genuine
volatility-risk-premium carry meets a fixed ticket and a fixed wing, and it
survives the control: with the wing re-solved to hold 0.15σ at every trade,
**both peaks stay at 180 DTE** (S3 +0.1323, S6 +0.1787).

---

## 3. Test 3 — sample adequacy, or: which of these cells is a result?

`n_req = 4(sd/|E|)²` is what a two-sigma verdict on the cell's own mean needs.
`n_available` is what 25.59 years produced.

| DTE | trades / index | `n_available` pooled | bucket |
|---|---|---|---|
| 7 | 1 100 | 3 300 | weeklies |
| 14 | 603 | 1 809 | gamma shoulder |
| 30 | 294 | 882 | monthlies |
| 45 | 199 | 597 | monthlies |
| 60 | 148 | 444 | quarterlies |
| 90 | 102 | 306 | quarterlies |
| 180 | 51 | 153 | annuals |
| 365 | 25 | 75 | annuals |
| **730** | **12** | **36** | **LEAPS** |

**A 730-day tenor over a 25.59-year window yields 12 non-overlapping trades per
index — 36 pooled.** That is the entire sample behind every LEAPS cell.

| bucket | unmeasurable cells | cells | share |
|---|---|---|---|
| weeklies | 0 | 7 | 0% |
| gamma shoulder | 0 | 7 | 0% |
| monthlies | 3 | 14 | 21% |
| quarterlies | 4 | 14 | 29% |
| annuals | 5 | 14 | 36% |
| **LEAPS** | **4** | **7** | **57%** |

**16 of 63 cells (25%) have an `E` indistinguishable from zero at two sigma.**
None are in the first two buckets; **more than half of the LEAPS column is not a
result.** Measurable tenors per structure: S1 **4 of 9**, S2 6, S3 8, S4 9, S5 9,
S6 8, **S7 3 of 9**.

The starkest shortfalls: 90-DTE S1 needs `n_req = 76 077` against 306 available
(**0.4%** of the requirement); 730-DTE S7 needs **11 785** against 36 (0.3%);
365-DTE S7 needs **5 657** against 75 (1.3%); 45-DTE S2 needs 756 against 597;
730-DTE S3 needs 65 against 36; 730-DTE S6 needs **648** against 36. Cells that
comfortably clear: 180-DTE S3 (`n_req` 11 against 153), 180-DTE S6 (10 against
153), every S4 and S5 tenor, and the whole S3 column except 730.

**These cells are printed and flagged, and never used as a verdict.**

---

## 4. Test 4 — cost by tenor, and the brief's expectation contradicted

| `c_R` (LOW) | 7 | 14 | 30 | 45 | 60 | 90 | 180 | 365 | 730 | shape |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | 0.0276 | 0.0193 | 0.0132 | 0.0107 | 0.0095 | 0.0078 | 0.0057 | 0.0044 | 0.0034 | **falls 8.1×** |
| S2 | 0.0003 | 0.0004 | 0.0004 | 0.0004 | 0.0004 | 0.0004 | 0.0004 | 0.0004 | 0.0006 | ~flat |
| **S3** | 0.0136 | 0.0138 | 0.0141 | 0.0142 | 0.0144 | 0.0145 | 0.0150 | 0.0155 | **0.0163** | **rises** |
| S4 | 0.0877 | 0.0616 | 0.0425 | 0.0345 | 0.0305 | 0.0252 | 0.0184 | 0.0142 | 0.0112 | **falls 7.8×** |
| S5 | 0.0008 | 0.0008 | 0.0008 | 0.0008 | 0.0009 | 0.0009 | 0.0009 | 0.0009 | 0.0009 | ~flat |
| **S6** | 0.0294 | 0.0303 | 0.0314 | 0.0320 | 0.0324 | 0.0329 | 0.0340 | 0.0349 | **0.0363** | **rises** |
| **S7** | 0.0778 | 0.1036 | 0.1438 | 0.1701 | 0.1939 | 0.2145 | 0.2743 | 0.3353 | **0.3806** | **rises 4.9×** |

Cost in **dollars** is flat in tenor by construction ($3.15 / $6.30 / $9.3 /
$12.60 per unit), so every movement in `c_R` is `R` moving:

| `R` $ (median) | 7 | 30 | 90 | 180 | 365 | 730 |
|---|---|---|---|---|---|---|
| S1 | 135.99 | 274.76 | 457.35 | 668.40 | 769.64 | 1 112.65 |
| S3 | 472.29 | 451.00 | 433.34 | 423.37 | 411.58 | 394.43 |
| S4 | 84.23 | 171.04 | 282.58 | 410.95 | 476.46 | 681.64 |
| S6 | 440.55 | 405.02 | 382.47 | 368.15 | 361.07 | 352.33 |
| S7 | 242.89 | 132.19 | 81.39 | 55.43 | 47.74 | 51.02 |

The grid splits in two, and the split is **not** the one the brief anticipated:

- **The four 5-wide structures (S3, S4, S6, S7).** The brief's mechanism —
  *credit/width and `R` move in opposite directions as tenor extends* — is
  **confirmed**: S3's credit/width rises **0.055 → 0.211** while its `R` falls
  $472 → $394; S6's rises **0.119 → 0.295** while its `R` falls $441 → $352. The
  brief's implied conclusion — *therefore `c_R` falls* — is **contradicted**:
  `R = width − credit`, and credit grows faster than the width-bound `R` shrinks,
  so **`c_R` rises with tenor** for S3, S6 and S7. The mechanism is the
  fixed-dollar wing: at 7 DTE a $5 wing is 1.44σ and sits far out in the tail
  where the density is low; at 730 DTE it is 0.15σ and sits near the money where
  the density is high, so the same $5 captures far more premium per dollar of
  width. **The brief's mechanism and its conclusion are not the same statement,
  and the data separates them.**
- **The structures whose `R` is not a wing and does scale with the index and with
  √T (S1, S4 — `R` = the debit; S2, S5 — `R` = the cash secured / the notional).**
  Here `c_R` **falls** with tenor, by 8.1× (S1: 0.0276 → 0.0034) and 7.8× (S4:
  0.0877 → 0.0112), because the ticket is a constant $3.15–$6.30 while `R` grows.

### Where cost consumes the gross edge at LOW prices

| cell | `c_R` | `E` | verdict |
|---|---|---|---|
| **S4 @ 7 DTE** | 0.0877 | +0.0683 | **cost 1.28× the gross edge** |
| S1 @ 90 DTE | 0.0078 | −0.0078 | `E` already ≤ 0 |
| S7 @ 30 DTE | 0.1438 | +0.1399 | cost 1.03× the edge |
| S7 @ 45, 60, 180, 365, 730 | 0.1701 → 0.3806 | +0.0531 → −0.0995 | 1.42× – 3.82× |
| **S2, S3, S5, S6** | — | — | **never**, at any tenor, LOW, HIGH or round-trip |

At **HIGH** cost the first tenor where cost exceeds the gross edge is: S4 **7**,
S7 **14**, S1 **90**, S6 **730**; and S2, S3, S5 **never**. Round trip is the
same list.

**The sharpest cost finding is the opposite of the one the brief frames.** The
structure whose cost destroys its edge outright is **not** a 4-leg structure at
long tenor — it is the **2-leg debit spread at 7 DTE**, where a $6.30 ticket
meets an `$84` `R`. And the structures that keep their edge at every cost setting
and every tenor are S2, S3, S5 and S6. The iron butterfly is the other failure:
its `R` is so small ($132 at 30 DTE, $51 at 730 DTE) that its ticket is 14%–38%
of `R` and exceeds its gross edge from 30 DTE onward.

Break-even cost `c_R* = E` in dollars, against the actual ticket: **S3 @ 180 DTE
`c_R*` = $60.39 against $6.30 (9.6× headroom); S6 @ 180 DTE `c_R*` = $85.39
against $12.60 (6.8× headroom)**. Both structures have their best `E_net` at
exactly the tenor where their cost headroom is largest.

---

## 5. Test 5 — skew sensitivity by tenor: longer tenor is MORE assumption-dependent

`dE` is the change in gross `E` when the SOLD legs are re-priced ±1.5 vol points
with strikes held fixed. Both directions are reported because the sibling studies
established that the model cannot say which is right.

### The band of model ambiguity — `E_net`(SOLD +1.5) − `E_net`(SOLD −1.5)

| id | 7 | 30 | 90 | 180 | 365 | 730 |
|---|---|---|---|---|---|---|
| S1 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| S2 | 0.0010 | 0.0023 | 0.0041 | 0.0061 | 0.0093 | 0.0144 |
| S3 | 0.0414 | 0.0919 | 0.1650 | 0.2637 | 0.3601 | **0.4826** |
| S4 | 0.1848 | 0.2241 | 0.2661 | 0.3006 | 0.3501 | 0.5041 |
| S5 | 0.0014 | 0.0031 | 0.0055 | 0.0080 | 0.0122 | 0.0190 |
| S6 | 0.0969 | 0.2404 | 0.5142 | **2.0116** | 1.9397 | 1.7418 |
| S7 | 0.7846 | 1.6301 | **4.1734** | 1.0415 | 1.4211 | 0.9810 |

Mean `max|dE|` by bucket: **weeklies 0.133 → gamma shoulder 0.133 → monthlies
0.229 → quarterlies 0.511 → annuals 0.416 → LEAPS 0.439** `R` units.

**Yes: longer tenor is more assumption-dependent — 3–4× between the weeklies and
the quarterly/annual/LEAPS buckets — and the ambiguity band widens monotonically
in tenor for S2, S3, S4 and S5.** The relationship is **not** clean cell by cell:
S6 and S7 are non-monotone (their worst skew cells sit at 90 and 180 DTE), which
is why the pooled Pearson of `|dE|` against DTE is only 0.02–0.29. Reported, not
smoothed.

### And under the conservative direction the premium edge largely disappears

`E_net` with SOLD −1.5 vol points:

| id | 7 | 30 | 90 | 180 | 365 | 730 |
|---|---|---|---|---|---|---|
| **S3** | −0.0020 | −0.0013 | −0.0168 | +0.0257 | **−0.0176** | **−0.0642** |
| **S6** | −0.0021 | +0.0132 | −0.0219 | −0.0176 | **−0.1235** | **−0.3346** |
| S4 | −0.1003 | +0.0520 | +0.1915 | +0.3320 | +0.4905 | +0.9050 |
| S5 | +0.0026 | +0.0128 | +0.0308 | +0.0590 | +0.1087 | +0.2012 |
| S7 | −0.0833 | −0.2856 | −0.5474 | −0.6864 | −0.8369 | **−1.0469** |

**This is the most important caveat in the study.** Under the conservative skew
direction — the one `cost-drag-per-leg-and-per-rung.md` and the sibling studies
both take — **the short put spread goes negative at 7, 30, 90, 365 and 730 DTE**
(positive only at 60 and 180), and **the condor goes negative at 7, 90, 180, 365
and 730**. In `R` terms **the long tenor is the most fragile**: S6 loses 0.335R of
`E_net` at 730 DTE against 0.002R at 7 DTE; S3 loses 0.064R against 0.002R.

The drawdowns move differently by tenor, and the split is informative:

| `dd(R)` change, BASE → SOLD −1.5 | 7 | 30 | 90 | 180 | 365 | 730 |
|---|---|---|---|---|---|---|
| S3 | −2.65 | −0.36 | −0.69 | +0.02 | −0.02 | −0.13 |
| S4 | **−58.19** | −3.23 | −1.80 | −0.66 | +0.07 | +0.14 |
| S6 | −6.28 | −1.98 | −0.91 | −0.93 | −1.94 | −1.65 |
| S7 | **−79.87** | −46.68 | −20.96 | −10.21 | −7.61 | **+2.09** |

**Skew changes the TAIL most at short tenor** (where the wing is a large fraction
of `R` and the position is repeatedly re-written) and **changes the MEAN most at
long tenor** (where the credit is a large fraction of `R` and each trade is held
for years). The two effects point in opposite directions, which is precisely why
`E_net` peaks in between.

---

## 6. Test 6 — the tail by tenor

**Read the "worst trade" column carefully.** For every defined-risk structure it
is the **structural maximum loss, exactly −1.000R at every tenor**, because a
7-DTE move and a 730-DTE move both eventually cross a 5-wide wing. It is a
statement about the structure, not about the tenor. The columns that move are
**`% at −1R`**, the percentiles, the drawdown, and the period sums.

| `% of trades at −1R` | 7 | 14 | 30 | 45 | 60 | 90 | 180 | 365 | 730 |
|---|---|---|---|---|---|---|---|---|---|
| S3 short put spread | 1.5% | 2.4% | 2.9% | 4.4% | 3.6% | 5.2% | 3.9% | 6.7% | **11.1%** |
| S6 iron condor | 2.7% | 3.9% | 4.2% | 6.4% | 4.3% | 6.5% | 6.5% | 13.3% | **30.6%** |
| S7 iron butterfly | 20.6% | 28.8% | 41.0% | 51.6% | 52.9% | 64.1% | 73.9% | 82.7% | **97.2%** |

**The structural tail fires MORE often as tenor extends, not less** — because the
fixed $5 wing becomes a smaller fraction of `σ√T`, so a smaller terminal move
crosses it. **This is the fixed-wing convention (N2) speaking, and it is the
single most misleading column in the study if read as a tenor effect.** It is
printed here in full so it cannot be read silently: **on a fixed dollar wing,
"longer tenor" is "closer wing in distribution units", and therefore "maximum
loss realised more often".**

What does *not* follow from the convention is the drawdown, which improves and
then gives the improvement back:

| `dd` (R) | 7 | 14 | 30 | 45 | 60 | 90 | 180 | 365 | 730 |
|---|---|---|---|---|---|---|---|---|---|
| S3 | −4.03 | −4.61 | −2.59 | −3.41 | −1.63 | −2.02 | **−1.23** | −1.25 | −1.36 |
| S6 | −5.01 | −5.13 | −2.56 | −2.96 | −1.65 | −2.69 | **−1.31** | −1.44 | **−2.56** |
| S7 | −25.16 | −30.10 | −38.75 | −33.96 | −21.13 | −35.55 | −25.21 | −13.32 | −14.65 |

And the ordinary bad periods improve monotonically:

| | 7 | 30 | 90 | 180 | 365 | 730 |
|---|---|---|---|---|---|---|
| S3 worst MONTH (R) | −0.150 | −0.094 | −0.081 | −0.040 | −0.048 | **−0.036** |
| S6 worst MONTH (R) | −0.172 | −0.118 | −0.091 | −0.052 | −0.048 | **−0.049** |
| S3 worst YEAR (R) | −0.359 (2022) | −0.151 (2008) | −0.164 (2008) | −0.087 (2002) | −0.056 (2008) | −0.090 (2008) |
| S6 worst YEAR (R) | −0.388 (2022) | −0.085 (2008) | −0.145 (2008) | −0.074 (2002) | −0.049 (2002) | −0.091 (2008) |

### The crashes, in `R`, over the pre-registered windows

| structure | window | 7 | 30 | 90 | 180 | 365 | 730 |
|---|---|---|---|---|---|---|---|
| **S3** short put spread | 2008 GFC | −1.05 | −1.25 | −1.87 | −0.78 | −0.84 | −1.00 |
| **S3** | 2020 COVID | **+2.03** | +0.77 | +0.30 | +0.38 | −0.04 | +0.04 |
| **S3** | 2022 bear | **−3.59** | −0.71 | −0.45 | +0.02 | −0.02 | −0.02 |
| **S6** iron condor | 2008 GFC | **+1.06** | −0.42 | −1.79 | −0.69 | −0.78 | −1.04 |
| **S6** | 2020 COVID | **+3.75** | +1.27 | +0.46 | −0.03 | +0.05 | −0.62 |
| **S6** | 2022 bear | **−3.88** | +1.00 | +0.15 | +0.37 | +0.32 | +0.18 |
| **S7** iron butterfly | 2020 COVID | **+16.74** | −6.16 | −3.17 | −2.27 | −2.77 | −0.60 |

**Answer: going longer in tenor is NOT a cheaper way to buy the protection the
sibling's paid hedge bought.** The sibling's paid hedge repaired 2008 from
−11.97% to −5.63% at a cost of −2.72 pp CAGR. Here:

- **2008 is NOT repaired by tenor for either premium seller.** S3 goes −1.05R
  (7 DTE) → −1.00R (730 DTE) — a wash, and *worse* than the 180-DTE −0.78R. S6
  goes **+1.06R (7 DTE) → −1.04R (730 DTE)**: the short tenor was *better* in
  2008, because a 7-DTE put spread repeatedly re-written through a crash keeps
  collecting crash vol, while a 730-DTE spread is one position that simply sits
  through it. S6's worst 2008 cell is 45 DTE (−2.60R).
- **2020 is not repaired either**: S6 +3.75R (7 DTE) → −0.62R (730 DTE); S7
  +16.74R (7 DTE) → −0.60R (730 DTE). Both premium sellers were *better* short.
- **2022 IS repaired, strongly**: S3 −3.59R (7 DTE) → −0.02R (730 DTE); S6
  −3.88R (7 DTE) → **+0.18R** (730 DTE). The long tenor turned the worst year of
  the grid into a small gain — and it did so by missing the repeated re-write,
  not by hedging.
- **What long tenor reliably bought is the ordinary bad month and year**, not the
  crash: S6's worst month improves 3.5× and its worst year 8× between 7 DTE and
  365 DTE. The 730-DTE cells give some of that back (S6 `dd` −2.56R at 730
  against −1.44R at 365).

**So the tail answer is genuinely two-sided: tenor buys a shallower ordinary
drawdown up to about 180–365 DTE; it does NOT buy crash protection, and past
365 DTE it starts giving the drawdown back.** The mechanism is that a long tenor
holds ONE position through the regime while a short tenor re-underwrites into it.

---

## 7. Test 7 — positivity by tenor and horizon: tenor partially repairs the inversion

`law` is `Φ(Sharpe_annual × √(period))`. The sibling found premium selling at
89% of months against 79% of years — the **inverted** order.

### S3, short put spread

| DTE | M | M_law | M_gap | Q | Y | Y_law | Y_gap | M > Y? |
|---|---|---|---|---|---|---|---|---|
| 7 | 72.2% | 56.4% | −0.158 | 67.6% | 62.5% | 71.1% | +0.086 | **INVERTED** |
| 30 | 75.5% | 56.0% | −0.195 | 74.5% | 75.0% | 70.0% | −0.050 | **INVERTED** |
| 45 | 73.5% | 53.6% | −0.199 | 73.5% | 70.8% | 62.4% | −0.084 | **INVERTED** |
| 60 | 74.8% | 56.4% | −0.184 | 81.4% | 83.3% | 71.2% | −0.122 | |
| 90 | 68.6% | 53.9% | −0.148 | 74.5% | 79.2% | 63.1% | −0.160 | |
| 180 | 69.6% | 56.7% | −0.129 | 76.5% | 87.5% | 71.9% | −0.156 | |
| 365 | 63.7% | 53.1% | −0.106 | 71.6% | 75.0% | 60.7% | −0.143 | |
| 730 | 57.5% | 51.5% | −0.061 | 59.8% | 79.2% | 55.0% | −0.241 | |

### The inversion counted by bucket

| bucket | inverted cells | cells | mean M | mean Y | mean M − Y |
|---|---|---|---|---|---|
| weeklies | 4 | 7 | 62.3% | 64.9% | −2.6 pp |
| gamma shoulder | 2 | 7 | 65.3% | 69.6% | −4.3 pp |
| monthlies | 3 | 14 | 63.2% | 70.8% | −7.6 pp |
| quarterlies | 3 | 14 | 62.5% | 69.9% | −7.4 pp |
| annuals | 2 | 14 | 58.5% | 67.6% | −9.1 pp |
| **LEAPS** | **1** | **7** | **51.3%** | **63.7%** | **−12.4 pp** |

**Yes — tenor changes the inversion, and the direction of the change is
repair.** Mean monthly-minus-yearly positivity runs from **−2.6 pp at the
weeklies to −12.4 pp at LEAPS**: the ordinary `Φ(Sharpe√period)` order is
increasingly restored as tenor extends. The mechanism is the same one the sibling
found at 4 legs: **the longer tenor lowers MONTHLY positivity** (62.3% → 51.3%)
**rather than raising yearly** (64.9% → 63.7%, essentially flat). It trades
monthly win frequency for horizon consistency — a **shape** purchase, not an edge
purchase, since `E_net` at 730 DTE is *below* its 180-DTE peak for both S3 and S6.

The mean yearly gaps tell the same story: weeklies −0.0116, gamma shoulder
−0.0505, monthlies −0.0761, quarterlies −0.0703, annuals −0.0636, LEAPS −0.0692.

**One honest qualification:** the inversion is *not* monotone in tenor cell by
cell. S7 is inverted at 60, 90, 180, 365 and 730 DTE — the *opposite* of repair —
because its `E` is negative and its positivity profile collapses at both ends
(M 34.3%, Y 25.0% at 730). A bucket-level mean hides that, so it is stated rather
than averaged away.

---

## 8. Test 8 — the verdict, per structure

`edge_per_tail = E_net ÷ |mean of the worst 1% of trades|`. Both rules are shown
because they can disagree.

| id | best DTE by edge/tail | edge/tail | `E_net` | `dd` (R) | best DTE by `E_net` | `ann_R_net` | measurable tenors |
|---|---|---|---|---|---|---|---|
| S1 long call | 730 | +1.0714 | +1.0714 | −3.37 | 730 | +1.507 | 4 of 9 |
| S2 cash-secured put | 365 | +0.0764 | +0.0172 | −0.34 | 730 | +0.050 | 6 of 9 |
| **S3 short put spread** | **180** | **+0.1277** | +0.1277 | **−1.23** | 180 | +0.763 | 8 of 9 |
| S4 bull call debit spread | 730 | +1.1173 | +1.1173 | −2.04 | 730 | +1.572 | 9 of 9 |
| S5 covered call | 730 | +0.4787 | +0.2104 | −0.61 | 730 | +0.296 | 9 of 9 |
| **S6 iron condor** | **180** | **+0.1979** | +0.1979 | −1.31 | 180 | +1.183 | 8 of 9 |
| S7 iron butterfly | 7 | +0.0878 | +0.0878 | **−25.16** | 7 | +11.326 | 3 of 9 |

For the two premium sellers **both rules agree on the same interior tenor (180
DTE)** — the only agreement of its kind in the grid. Restricting to measurable
cells changes nothing: the verdicts are identical.

### When a LONG tenor (LEAPS) is the right answer — precisely

1. **When `R`, not the view, is the binding constraint.** A 730-DTE 50Δ call's
   `R` is **10.4% of the underlying notional**, against **94.9%** for the covered
   call at the same tenor — a **9.1×** notional-efficiency gain. That is the
   capital-efficiency claim the owning skill makes, and it is confirmed.
2. **When the cost floor is the obstacle.** A $3.15 ticket against an $1 112.65
   `R` is **0.34% of `R`**; against a $135.99 `R` at 7 DTE it is **2.76%**, and
   for the 2-leg version (S4) it is **8.77%** — enough to consume a positive gross
   edge (S4 @ 7 DTE: gross +0.0683, cost 0.0877). **If an account can only afford
   a few tickets, the long tenor is where the fee stops mattering.**
3. **When `rho` exposure is wanted.** A 730-DTE 50Δ call carries large positive
   rho, priced off the real `TVC:US03M` yield — the one axis where this study's
   own inputs genuinely favour the long tenor.
4. **When the objective is horizon consistency, not expectancy.** LEAPS has the
   least-inverted positivity profile of any bucket (mean M − Y = −12.4 pp) and
   the flattest worst month (S6: −0.049R).
5. **When the regime is a slow trend, not a crash.** S6's 2022 goes −3.88R at
   7 DTE to +0.18R at 730 DTE, and S3's −3.59R to −0.02R.

### When a very SHORT tenor is the right answer — precisely

1. **When the tail is being re-underwritten monthly.** S3's 2020 is **+2.03R at
   7 DTE against −0.04R at 365**, and S6's is **+3.75R against +0.05R**; S6's
   2008 is **+1.06R at 7 DTE against −1.04R at 730**. A re-written short tenor
   collects the crash vol; a held long tenor absorbs the crash.
2. **When `ann_R` is the objective.** Every structure's `ann_R_net` is highest at
   the short end: S7 **+11.326** at 7 DTE against −0.675 at 730; S6 +5.201
   against −0.128; S3 +2.212 against +0.136; S4 +5.160 at **30** DTE against
   +1.572 at 730. The annualised return on a continuously committed 1R sleeve is
   a short-tenor phenomenon.
3. **When the ordinary bad month matters more than the tail.** S6's worst month
   is −0.172R at 7 DTE and −0.049R at 730 — this one favours the LONG tenor, and
   it is listed here only to show the two rules genuinely conflict.
4. **When the assignment surface is a cost you want to bound.** A 7-DTE short put
   either expires or is assigned within the week; a 730-DTE short leg carries two
   years of American early-exercise exposure. **This study cannot price that
   difference at all** (limitation 4), and the ignorance cuts against long tenor.

### Two negative results worth naming

- **The iron butterfly (S7) is the study's failure case at every tenor but 7.**
  Its `E_net` is negative from 30 DTE onward, its drawdown is −21R to −39R at
  every tenor, its ticket is 8%–38% of `R`, its credit is 51%–90% of its width,
  its maximum loss is realised in **97.2%** of 730-DTE trades, and under the
  conservative skew direction it is negative **everywhere** (−0.083R at 7 DTE to
  −1.047R at 730 DTE). **A 5-wide iron fly at long tenor is not a strategy; it is
  a bet that the index closes within 0.65% of its strike two years from now.**
- **The 730-DTE condor (S6) is the second.** `E_net` −0.0910 at LOW, −0.1197 at
  HIGH, −0.1272 round trip, −0.3346 under the conservative skew direction, 30.6%
  of trades at maximum loss, and `n_req` 648 against 36 available.

---

## 9. Test 9 — reconciliation with `options-risk-engineer`

The owning skill's partition is used verbatim. What this study can say about its
prescriptions:

| claim in the owning skill | verdict | why |
|---|---|---|
| 0DTE: close by 14:45 ET, hard stop 15:00 ET | **CANNOT TEST** | daily bars have no intraday path |
| weeklies: close at 50% of max profit or 3 DTE | **CANNOT TEST** | no profit target exists in this design; every trade runs to expiry |
| weeklies: "theta is large but no longer compensates the gamma you accept" | **SUPPORTS (direction)** | `theta/day/R` is highest at 7 DTE by 6.8×–104× in every structure |
| gamma shoulder 8–20: "hold; add no new credit" | **CANNOT TEST** | a hold/no-add instruction is a portfolio rule, not a payoff |
| monthlies 21–60: "the open and scale zone" | **PARTIALLY SUPPORTS** | 30 and 45 DTE are among the best-evidenced cells in the grid for the premium sellers, and the interior `E_net` peak sits just above them at 180 DTE; but for the other five structures the peak is elsewhere |
| quarterlies 60–120: "vega is the only live Greek of size" | **SUPPORTS (direction)** | entry vega relative to `R` is largest in this band for the credit structures — but no vega P&L path is simulated, so this is a statement about entry Greeks only |
| quarterlies: "this bucket has no other owner" | **NO EVIDENCE EITHER WAY** | an ownership convention is not a measurable claim |
| annuals 121–365: "manage by delta and vega, not theta" | **SUPPORTS (direction)** | `theta/day/R` at 180–365 DTE is 15–100× below the weeklies band |
| LEAPS >365: "capital-efficient stock substitute" | **SUPPORTS** | S1's `R` is 10.4% of notional against S5's 94.9% — a 9.1× notional-efficiency gain; but only 4 of S1's 9 tenors are measurable |
| `Γ_ATM ∝ 1/√T`; the 45→22.5→11.25→5.6→2.8 ladder | **SUPPORTS (exactly)** | this study's own pricer returns 10.959× for 30→0.25 DTE against the derived 10.954× |
| **roll windows and hard deadlines as forcing dates** | **CANNOT TEST** | the study never rolls, never closes early, and never observes broker margin or assignment |

### The one thing this study adds to that calendar

**The owning skill's own labels overlap at 60 DTE** (`monthlies 21–60` and
`quarterlies 60–120`) and abut at 365. A position at exactly 60 DTE therefore
resolves to **two different buckets under the skill's own two tables**, and those
two buckets carry **different hard deadlines (21 DTE vs 45 DTE)** and **different
roll windows (21–30 vs 60–75)**. A 60-DTE position is simultaneously "monthlies,
hard deadline 21 DTE" and "quarterlies, hard deadline 45 DTE". This study assigns
60 → quarterlies (declared in README §3) and reports the ambiguity rather than
resolving it, because resolving it is the owning skill's call.

### Claims that remain untested evidence

Every roll window (T−7→T−5, 14–21, 21–30, 60–75, 120–150, 120–90); every hard
deadline (T−0 15:00, 7, 21, 45, 90, 60); the 0DTE 14:45/15:00 clock; the
expiry-week T−5…T+1 rungs; the two-rolls-per-cycle cap; the credit-or-flat roll
rule (owned by `options-position-lifecycle`); and **every assignment,
ex-dividend and pin-risk consequence of holding an American short option**,
because this model is European, cash-settled and dividend-free. The long-tenor
cells are where that ignorance is most expensive: a 730-DTE short call carries two
years of ex-dividend exercise exposure that the model never sees.

---

## 10. What the study cannot see — the short version

Full list in `README.md` §4. The five that matter most for a *tenor* conclusion:

1. **No term structure.** One ~30-day VIX prices 7 DTE and 730 DTE alike. Every
   long-tenor cell is priced at a vol the market would not charge it, by an
   unknown sign. **This is the largest weakness of the whole study and it is not
   repairable from these feeds.**
2. **No skew surface** — and a skew surface is itself a function of tenor.
   Test 5 sizes the direction-ambiguous part (±1.5 vol points); it cannot size
   the tenor-dependent part. Under the conservative direction the premium-selling
   edge largely disappears at long tenor.
3. **The fixed $5 wing (N2).** Appendix A's control keeps both interior peaks at
   180 DTE, so the *peak* is not an artefact of the width — but every **magnitude**
   in the 5-wide rows is partly the convention, and the `% at −1R` column
   (Test 6) is entirely the convention.
4. **The long-option cells are long the realised equity risk premium (N6).** The
   monotone rise of `E_net` for S1/S4/S5 into the LEAPS bucket is mostly two
   years of risk premium per trade, not an options edge. The right comparison is
   buy-and-hold equity over the same window, and this study does not make it.
5. **One window, two crashes, 24 complete years.** Enough to see a tail; 16 of 63
   cells still fail their own two-sigma requirement.

---

## 11. The one-sentence version

**Tenor buys a clock, not an edge: it is monotone in nothing, it pays 6.8×–104×
less per day at 730 DTE than at 7 DTE, it raises skew dependence 3–4×, it shrinks
the sample to 36 trades, it partially repairs the positivity inversion by trading
monthly win frequency for horizon consistency, and it does not buy crash
protection — and the one place it genuinely peaks is the interior, at 180 DTE, for
the two structures that actually sell premium, where the drawdown is a quarter to
a third of its short-tenor size and the ticket still has 6.8–9.6× of headroom.**
