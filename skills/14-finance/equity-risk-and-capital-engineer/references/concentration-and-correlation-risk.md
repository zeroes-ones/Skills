# Concentration and Correlation Risk

Concentration is not "one position is big". It is the joint condition of **size relative to the
book**, **size relative to the security's own market**, and **correlation with everything else the
book holds**. Two of those three can be benign while the third is fatal, and only one of them
appears in a portfolio screen.

## §1 — The Four Measures

| Measure | Formula | What it misses alone | Ceiling |
|---|---|---|---|
| **Weight in NAV** | `position_value / NAV` | Says nothing about whether the position can be exited | ≤ **10% NAV single name** — this is a **position-size rule**, and it is `portfolio-signal-manager`'s (the sizing owner). This skill applies it unchanged and adds no second single-name cap of its own |
| **Fraction of ADV** | `position_shares / 20-day ADV` | Says nothing about correlation | ≤ 20% of ADV (emergency ceiling); 10% is the plan |
| **Fraction of shares outstanding** | `position_shares / shares_outstanding` | Says nothing about the book | Monitor above 1%; a short above the 0.5%/10,000-share threshold engages the Reg SHO clock (`reg-sho-and-threshold-list.md`) |
| **Correlation-adjusted weight** | `Σ w_i × ρ_i,max` where `ρ_i,max` is the correlation to the largest position | Says nothing about the exit | ≤ **25% effectively-correlated exposure** — consistent with `portfolio-signal-manager`'s **25% per-sector** cap, which is the same constraint expressed by label rather than by measured correlation |

**One sizing owner, one set of numbers.** Single-name size is **10% of NAV** and sector /
correlated-cluster exposure is **25%**, both owned by `portfolio-signal-manager` and used here
verbatim. This file carries **no second single-name size ceiling**: the only thing it adds at a large
weight is the **exit test** below. A book that wants to exceed 10% in one name is making a sizing
argument to the sizing owner, not to this file — and a 15% figure is not a licence to do it.

**Source / method:** the first three are direct arithmetic on position and market data
[COMPUTED]. The correlation figure requires a return series; use the same window for every pair and
state the window, or the number is not comparable to anything.

## §2 — The Concentration That Matters Is the Exit-Weighted One [COMPUTED]

A position's weight understates its risk by exactly the amount it would cost to leave:

```
exit_weighted_concentration = Σ_i ( position_value_i / NAV × exit_cost_pct_i )
```

Worked on a $500,000 NAV book:

```
POSITION            VALUE      % NAV     exit_cost_pct   CONTRIBUTION
Small-cap A         $150,000    30.0%        3.21%          0.963%
Mega-cap B         $120,000    24.0%        0.10%          0.024%
Mid-cap C          $ 80,000    16.0%        0.80%          0.128%
Rest (12 names)    $150,000    30.0%        0.30%          0.090%
                                                       ──────────
exit_weighted_concentration (book)                       1.205%
```

The single small-cap name contributes **0.96 of the 1.21 percentage points** — 80% of the book's
exit-weighted concentration while holding 30% of its NAV. Mega-cap B holds almost as much NAV and
contributes 2% as much exit risk. **A NAV-weight screen calls those two positions similar. The
exit-weighted measure calls one of them a third of the book's problem.** Both figures are
[COMPUTED] from the stated inputs and the exit costs developed in
`liquidity-and-exit-cost-planning.md` §3.

**Rule of thumb that falls out of it:** if one position contributes more than half of the book's
exit-weighted concentration, that position *is* the book's exit risk, regardless of its NAV weight.

## §3 — Correlation: The Cluster Is the Position

Five different tickers in the same factor are not five positions. They are one position at five
times the size.

- **Cluster by economic driver, not by ticker or sector label.** Two "different sectors" that both
  sell into the same end market, or both depend on the same rate path, or both depend on the same
  single customer, behave as one name in a sell-off.
- **Correlations rise in a drawdown.** A cluster that measured 0.4 in an uptrend can behave as 0.9
  in a downturn. The stress correlation is the number to size against — not the measured one.
- **The stress test is correlation → 1.0.** Sum the positions in the cluster at full value and ask
  whether the result is a position the book would have been allowed to own. If not, the cluster is
  over-sized even though every *individual* position is inside its cap.
- **A cluster closes whole or not at all.** Closing one leg of five and keeping four converts a
  diversified cluster into a concentrated one at the exact moment capital is shortest.

## §4 — The Two Clocks of a Concentrated Position

A concentrated position has two deadlines, and they are not the same deadline:

1. **The exit clock** — the number of sessions required to leave at a stated participation rate,
   from §4 of `liquidity-and-exit-cost-planning.md`. This clock is running *now*; it is not started
   by a decision.
2. **The margin clock** — the price at which the position's contribution to the account's cushion
   disappears, from §3 of `margin-regimes-and-forced-liquidation.md`. For a maximally leveraged
   long account that is a 33.33% decline.

The dangerous case is the intersection: the margin clock fires while the exit clock is still
running. That is a forced sale into a thin book, and it is the mechanism behind most catastrophic
single-position losses. **The reserve floor in `capital-reserve-and-deployment.md` exists so that
the exit clock can finish before the margin clock fires.**

## §5 — Behaviour Across the Four Regimes

| Regime | Concentration behaves like | What changes | What the risk engineer does |
|---|---|---|---|
| **Bull market / uptrend** | A feature. The concentrated name is the reason the book is ahead; every screen shows it as the best decision made | Correlations fall, ADV rises, spreads tighten, exits look free, borrow looks easy. Every input to the exit model is at its most favourable | Do not resize the position upward because the model improved. Re-measure `exit_cost_pct` and *notice* that it improved, then leave the plan alone |
| **Correction / pullback** (−5% to −20%) | A warning. The name falls further than the index and the exit cost rises quietly | Spreads widen modestly, ADV falls, correlations begin to converge. Nothing has broken, and the exit plan has already degraded | Raise the re-measurement cadence; reduce at the margin only if `exit_cost_pct` has breached its cap; never add on the grounds that the name is "cheaper" |
| **Bear market / downturn** (−20% or more) | The problem. The position is now the largest risk in the book and the market for it is thin | Correlations near 1; the cluster behaves as one; margin requirements are computed on values that have already fallen (see §6 — the maintenance requirement shrinks but equity shrinks faster) | Cut by the forced-selling order, risk first; the sequence in `capital-reserve-and-deployment.md` §5 is a standing instruction, not an improvised one |
| **Crash / tail event** (a market collapse, a March-2020-style gap event) | The outcome. The position cannot be exited at any modelled cost | Every bid is optional; halts interrupt continuous trading; a stop order becomes a market order into no book | The only protection is what was done before: size, a reserve floor, and a position that a forced sale can afford to sell |

**All four regimes belong in the plan.** A plan written in an uptrend that has never been read in a
crash regime is not a plan; it is a description of the weather on the day it was written.

## §6 — The One Arithmetic That Surprises People [COMPUTED]

Maintenance margin is a percentage of **market value**, so it shrinks as the position falls. Equity
shrinks at 1:1. For a long position with debit `D`:

```
equity      = MV − D
requirement = 0.25 × MV
call        = MV − D < 0.25 × MV   →   MV < D / 0.75
```

At the maximum Reg T leverage `MV = 2D`, the call lands at `MV = 1.3333D` — a **33.33% decline**.
A 30%-of-NAV concentrated long in a leveraged account, therefore, is a position whose loss of the
position is triggered by a decline of approximately one third, which is inside the historical
range of a single bear market and well inside the range of a crash. The concentration cap and the
margin regime are the same conversation.

## §7 — Failure Modes

1. **Screening concentration by NAV weight alone.** The exit-weighted measure in §2 is the one that
   predicts the failure.
2. **Treating five correlated tickers as five positions.** The cluster is the position.
3. **Using an uptrend correlation to size a downturn cluster.** Measured correlation is the
   *optimistic* input.
4. **Closing one leg of a correlated cluster.** Converts diversification into concentration under
   pressure.
5. **Letting the position grow into concentration through appreciation.** The cap is on the position,
   not on the purchase.
6. **Adding to a concentrated name "because it is cheaper".** The exit cost rose while the price fell;
   the position got riskier, not better.
7. **Ignoring the fraction-of-shares-outstanding measure on the short side.** It engages the Reg SHO
   clock.
8. **Assuming the margin clock and the exit clock start together.** The exit clock is always running;
   the margin clock starts at the price in §6.
9. **Sizing the cluster at measured rather than stress correlation.** Use correlation → 1.0.
10. **Writing the plan in a bull market and never reading it in the other three regimes.**

## §8 — Verification

- [ ] The four concentration measures are computed and reported for the largest positions.
- [ ] `exit_weighted_concentration` is reported for the book, with the top contributor named.
- [ ] Every correlation cluster is listed with its members and its aggregate weight.
- [ ] Cluster sizing uses correlation → 1.0, not measured correlation.
- [ ] The two clocks of §4 are reported as dates or as session counts, not as adjectives.
- [ ] The plan has been re-read in the current regime, and the regime is named.
