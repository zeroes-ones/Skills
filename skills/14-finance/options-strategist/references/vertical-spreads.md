# Vertical Spreads

## Purpose
Definitive reference for the four vertical spread structures — the workhorse defined-risk directional strategies. Each decomposed into construction, P&L metrics, IV context, and UOA-informed deployment.

---

## The Four Vertical Spreads

### 1. Bull Call Spread (Debit)
- **Construction:** Buy lower-strike call, sell higher-strike call (same expiration)
- **Max Profit:** (Short Strike − Long Strike) − Debit. $100/$105 at $2.50 → $2.50 ($250)
- **Max Loss:** Debit Paid ($250)
- **Breakeven:** Long Strike + Debit = $102.50
- **POP:** ~1 − Delta(Short). At 0.30 delta short → ~70%
- **Vega:** Net long. Best when IV Rank < 30
- **Ideal DTE:** 45–60

### 2. Bull Put Spread (Credit)
- **Construction:** Sell higher-strike put, buy lower-strike put
- **Max Profit:** Credit. $95/$90 at $1.50 → $150
- **Max Loss:** (Short − Long) − Credit = $3.50 ($350)
- **Breakeven:** Short Strike − Credit = $93.50
- **POP:** ~1 − Delta(Short). At 0.25 delta → ~75%
- **Vega:** Net short (IV crush helps). Best when IV Rank > 30
- **Ideal DTE:** 30–45

### 3. Bear Call Spread (Credit)
- **Construction:** Sell lower-strike call, buy higher-strike call
- **Max Profit:** Credit. $105/$110 at $1.50 → $150
- **Max Loss:** (Long − Short) − Credit = $3.50 ($350)
- **Breakeven:** Short Strike + Credit = $106.50
- **POP:** ~1 − Delta(Short). At 0.25 delta → ~75%
- **Vega:** Net short. Best when IV Rank > 30
- **Ideal DTE:** 30–45

### 4. Bear Put Spread (Debit)
- **Construction:** Buy higher-strike put, sell lower-strike put
- **Max Profit:** (Long − Short) − Debit. $100/$95 at $2.00 → $3.00 ($300)
- **Max Loss:** Debit Paid ($200)
- **Breakeven:** Long Strike − Debit = $98.00
- **POP:** ~Delta(Long). At 0.40 delta → ~40%
- **Vega:** Net long. Best when IV Rank < 30
- **Ideal DTE:** 45–60

[VERIFIED] Subtract $0.05–$0.10 per leg for realistic execution P&L after bid-ask friction.

---

## Debit vs Credit: When to Use Each

| Factor | Debit (Buy Premium) | Credit (Sell Premium) |
|--------|--------------------|-----------------------|
| IV Rank | < 30 (cheap options) | > 30 (expensive options) |
| IV Trend | Rising (vega helps) | Falling (IV crush helps) |
| POP | 40–60% | 65–80% |
| Reward/Risk | 1:1 to 3:1 | 1:3 to 1:2 |
| Theta | Works against you | Works for you |
| Adjustment | Harder (must overcome debit) | Easier (can roll for credit) |

[COMMON-PRACTICE] When IV Rank > 50, always choose credit over debit for the same direction. Selling a bull put spread captures directional AND volatility edge.

---

## Strike Width Selection

| Underlying Price | Optimal Width | Notes |
|-----------------|---------------|-------|
| < $25 | $2.50 | Commission drag at $1 widths |
| $25–$100 | $5.00 | Retail sweet spot |
| $100–$500 | $10.00 | Fewer contracts = lower commissions |
| $500–$1,000 | $25.00 | Liquidity is primary concern |
| > $1,000 | $50.00 | Commission negligible |

**Width = 1–3% of underlying price** is the rule of thumb. For $100 stock: $1–$3 wide.

### Commission Efficiency Example
On $100 stock with $0.65/contract: $1-wide needs 10 contracts for $1K risk → $13.00 commission (1.3%). $5-wide needs 2 contracts → $2.60 (0.26%). On 100 trades/year, $1-wide costs $1,040 more in friction. [COMMON-PRACTICE]

---

## UOA-Driven Vertical Spread Selection

| UOA Signal | IV Rank | Strategy | Strike Construction |
|-----------|---------|----------|---------------------|
| Call sweeps, OI > 2× | < 25 | Bull Call Spread (debit) | Long at UOA strike; short at next resistance |
| Call sweeps, OI > 2× | 25–50 | Bull Put Spread (credit) | Short at support or 0.25 delta; long at 0.10 delta |
| Call sweeps, OI > 2× | > 50 | Bull Put Spread (aggressive) | Short at 0.30–0.35 delta |
| Put sweeps, OI > 2× | < 25 | Bear Put Spread (debit) | Long at UOA strike; short at next support |
| Put sweeps, OI > 2× | 25–50 | Bear Call Spread (credit) | Short at resistance or 0.25 delta; long at 0.10 delta |
| Put sweeps, OI > 2× | > 50 | Bear Call Spread (aggressive) | Short at 0.30–0.35 delta |
| Multi-leg UOA | Any | Mirror structure | Use identical UOA strikes; scale contracts |
| Block > $500K | Any | Extend DTE to 60–90 | Institutional timeframe |

[INFERRED] Volume > OI increase = opening activity (signal). Volume < OI increase = closing (noise). Act only on opening activity.

---

## Profit Targets and Stop-Losses

### Debit Spreads
| Trigger | Action |
|---------|--------|
| 50% of max profit | Close. Remaining 50% requires doubling gain. |
| 100% of debit | Stop-loss (max loss). Do NOT average down. |
| 21 DTE, not at 30%+ profit | Close. Theta accelerates — recovery unlikely. |

### Credit Spreads
| Trigger | Action |
|---------|--------|
| 50% of max credit | Close. Redeploy capital. [COMMON-PRACTICE] |
| 2× credit received | Stop-loss. Collected $1.50 → close at $3.00. |
| 21 DTE | Close. Gamma risk dominates in final 3 weeks. |
| Short strike tested | Close regardless of P&L. Probability edge violated. |

---

## Position Sizing
```
Max Contracts = (Portfolio × 0.02) / Max Loss Per Contract
```
$50K portfolio, $5-wide at $1.50 credit (max loss $350): 2 contracts ($700 risk = 1.4%).

---

## Adjustment Hierarchy for Credit Spreads

1. **Do nothing** — position in profit zone, short strike not threatened
2. **Roll untested side closer** — collect additional credit, reduce max loss
3. **Roll entire position** — same strikes, next expiration, for net credit ≥ $0.05
4. **Close** — thesis broken or adjustment requires more capital than original max loss

**Golden Rule:** Never adjust if adjustment requires > original max loss capital. [VERIFIED]

---

## Pin Risk Warning

Short $50 put, stock closes at $50.01 (OTM by $0.01). After-hours gap to $45. Monday: assigned short stock at $50, long $45 wing expired worthless. Supposed max loss: $500. Actual loss: $500+ and growing.

**Prevention:** Close all credit spreads by 3:30 PM ET on expiration day if within 2% of short strike. The final $0.05 of premium is NEVER worth the gap risk.

