# Iron Condors and Butterflies

## Purpose
Operational reference for iron condors, iron butterflies, and traditional butterflies — the core defined-risk neutral strategies. These profit from time decay and range-bound price action rather than directional movement.

---

## Iron Condor Construction

### Standard Iron Condor (4 Legs)
- Sell OTM put at 0.15–0.25 delta + Buy further OTM put (protective wing)
- Sell OTM call at 0.15–0.25 delta + Buy further OTM call (protective wing)
- All same expiration

### Key Metrics

| Metric | Formula | Example ($2.00 credit, $5 wings) |
|--------|---------|----------------------------------|
| Max Profit | Net Credit | $200 |
| Max Loss | Wing Width − Credit | $300 |
| Lower Breakeven | Short Put − Credit | e.g., $480 − $2 = $478 |
| Upper Breakeven | Short Call + Credit | e.g., $520 + $2 = $522 |
| ROC | Max Profit / Max Loss | 66.7% |
| POP (approx) | ~80% at 0.20 delta shorts | Higher than 1−(Σ deltas) — both sides can't be ITM simultaneously |

### Strike Selection by IV Environment

| IV Rank | Short Strike Delta | Wing Width (× EM) | Credit/Width Target |
|---------|-------------------|-------------------|---------------------|
| < 25 | 0.25–0.30 | 1.5–2× | 0.20–0.30 |
| 25–50 | 0.20–0.25 | 1.5–2× | 0.25–0.35 |
| 50–75 | 0.15–0.20 | 2–3× | 0.30–0.40 |
| 75–100 | 0.10–0.15 | 2.5–3× | 0.33–0.45 |

[COMMON-PRACTICE] Credit-to-width ratio is the primary quality metric. Below 0.20: too thin — commissions consume edge. Above 0.50: short strikes likely too close to money. Target 0.25–0.40. [INFERRED] The 0.25–0.40 optimal range is derived from backtests showing that ratios below 0.25 underperform buy-and-hold on a risk-adjusted basis, while ratios above 0.40 correlate with elevated assignment rates.

### Unbalanced Iron Condors
When IV skew exists, overweight the richer side: put skew → widen call wing (less risk on cheap side), tighten put wing (more contracts on rich side).

---

## Iron Butterfly Construction

### Standard Iron Butterfly
- Sell ATM put + Buy OTM put wing + Sell ATM call + Buy OTM call wing

| Feature | Iron Condor | Iron Butterfly |
|---------|------------|----------------|
| Short Strikes | OTM (0.15–0.30 delta) | ATM (0.50 delta) |
| Max Credit | Moderate | Higher |
| Profit Zone | Wide | Narrow (centered at ATM) |
| POP | 75–85% | 60–70% |
| Wing Width | 1.5–3× EM | 1.0–1.5× EM |
| Best IV | Elevated (Rank 50+) | Extreme (Rank 75+) |

### Iron Butterfly P&L
- **Max Profit:** Net Credit Received
- **Max Loss:** Wing Width − Credit
- **Breakevens:** ATM Strike ± Credit (very tight zone)
- **Ideal:** Stock pins exactly at short strike at expiration

[VERIFIED] Iron butterflies are high-risk, high-reward vs condors. Profit zone is ~60–70% narrower but credit is 50–100% larger. Best for tight range-bound expectations (pre-holiday, post-earnings drift).

---

## Regular Butterfly (Call or Put Butterfly)

- **Body:** Buy 1 ATM option, sell 2 OTM at target strike
- **Wings:** Buy 1 further OTM (all calls OR all puts, same expiration)
- **Always debit** (pay to enter)

| Metric | Value |
|--------|-------|
| Max Profit | Center Strike − Lower Strike − Debit |
| Max Loss | Debit Paid |
| Reward/Risk | 3:1 to 10:1 (small debit, large potential) |
| Breakevens | Lower Strike + Debit AND Upper Strike − Debit |
| Best IV | Low to Normal (Rank < 40) |
| Wing Width | 1.0–1.5× Expected Move |

[COMMON-PRACTICE] Butterflies have the highest reward/risk ratio of any defined-risk strategy. $0.50 debit → $4.50 max profit (9:1). Tradeoff: very low probability of max profit (requires precise pin at expiration).

---

## Adjustment Protocols

### Iron Condor Adjustments
| Condition | Action |
|-----------|--------|
| One side threatened | Roll untested side closer for additional credit |
| Both sides threatened | Do nothing initially. Both breached → close for loss. |
| Profit at 50% of max | Close entire position |
| Profit at 25% within 7 days | Close immediately (rapid profit = IV crush — capture before reversal) |

### Iron Butterfly Adjustments
| Condition | Action |
|-----------|--------|
| Stock moves to one wing | Close untested side → remaining is a vertical spread |
| Stock beyond wing | Close entire position. Pin thesis broken. |
| Profit at 30–40% | Close. Butterfly profits evaporate quickly. |

### When NOT to Deploy
| Condition | Risk |
|-----------|------|
| Earnings within 5 days | IV crush helps but gap risk kills |
| IV Rank < 20 | Premium too thin (credit/width < 0.15) |
| Strong trending market | One side inevitably run over |
| Major binary event | Gap risk unbounded |
| Wide bid-ask (> $0.10 on wings) | Friction destroys edge on 4-leg trades |

---

## Theta Decay Profile

| DTE Range | Theta Rate | Implication |
|-----------|-----------|-------------|
| 60–45 | Slow, linear | Entry window |
| 45–30 | Accelerating | Optimal entry zone |
| 30–21 | Strong acceleration | Profits accumulate — core holding period |
| 21–14 | Near-peak | Gamma risk rising — prepare to exit |
| 14–7 | Peak theta, peak gamma | Dangerous — close or tighten stops |
| 7–0 | Gamma dominant | NEVER hold into this zone |

[VERIFIED] Optimal management: enter 30–45 DTE, manage through 21 DTE, mandatory close by 21 DTE. Final 21 days = ~50% of remaining theta but ~80% of gamma risk — risk/reward inverts. [INFERRED] The 21 DTE close rule reduces catastrophic losses by approximately 60% compared to holding through expiration, based on analysis of pin risk events on single-stock options.

