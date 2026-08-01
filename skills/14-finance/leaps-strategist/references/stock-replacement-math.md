# Stock Replacement with LEAPS — Deep Reference

> **Reading time:** 15 min | **Prerequisites:** options-strategist (long calls), quantitative-analyst (Greeks, rho)

## The Core Proposition

LEAPS (Long-term Equity Anticipation Securities) are options with expirations of 9 months to 3 years. A deep-in-the-money (DITM) LEAPS call can functionally replace 100 shares of stock at 25-40% of the capital cost, with near-identical upside participation, defined risk, and — critically — fundamentally different Greek behavior that must be understood before deployment.

## Why Replace Stock with LEAPS?

### Capital Efficiency

```
Stock: 100 shares of SPY @ $500 = $50,000 capital required
LEAPS: 1 SPY Jan 2027 400 Call (DITM) @ ~$115 = $11,500
Capital saved: $38,500 (77% reduction)
```

[COMPUTED] The capital saved can be deployed in risk-free assets (T-bills) earning ~5% = $1,925/year. This reduces the effective cost of the LEAPS position.

### Defined Risk

```
Stock max loss: $50,000 (if SPY → $0)
LEAPS max loss: $11,500 (premium paid)
```

[VERIFIED] The LEAPS defines maximum loss at the premium paid. Stock has unlimited downside to zero.

### Leverage Without Margin

```
LEAPS leverage: ~4.3x ($50,000 notional / $11,500 capital)
No margin interest. No maintenance requirements (beyond initial debit).
No margin calls.
```

## DITM Strike Selection

### The Delta-Moneyness Tradeoff

| Strike % of Spot | Approximate Delta | Capital Required | Extrinsic % | Time to Breakeven |
|-----------------|-------------------|-----------------|-------------|-------------------|
| 50% (S×0.50) | 0.95+ | ~51% of stock | < 1% | Near-immediate |
| 60% (S×0.60) | 0.92+ | ~42% of stock | < 1.5% | < 1 month |
| 70% (S×0.70) | 0.88+ | ~33% of stock | < 2% | ~2 months |
| 80% (S×0.80) | 0.82+ | ~26% of stock | < 3% | ~3 months |
| 85% (S×0.85) | 0.78 | ~22% of stock | ~4% | ~4 months |
| 90% (S×0.90) | 0.72 | ~18% of stock | ~6% | ~6 months |

[COMPUTED] Delta approximations for 18-month LEAPS, IV=20%, r=5%. Actual delta varies by IV and rates.

### The Sweet Spot: 0.80-0.85 Delta

[COMMON-PRACTICE] Most LEAPS stock replacement practitioners target **0.80-0.85 delta** at entry. This balances:
- Sufficient capital efficiency (75-80% savings vs. stock)
- Acceptable extrinsic premium (< 4%)
- Tracking error within 10-15% of stock moves
- Reasonable breakeven timeline

### Extrinsic Value: The Hidden Cost

[VERIFIED] Even a DITM LEAPS call carries some extrinsic (time) value. This is the "rent" you pay for the leverage and defined risk.

```
Extrinsic = option_price - max(0, S - K)
Extrinsic_pct = extrinsic / option_price
Annualized_extrinsic_cost = extrinsic_pct × (365 / DTE)
```

**Rule:** Annualized extrinsic cost must be < 2% for the LEAPS to beat buying stock on margin (where margin interest is 6-10%).

### Example Calculation

```
SPY @ $500, Jan 2027 400 Call (18 months, ~550 DTE)
Option price: $115.00
Intrinsic: $500 - $400 = $100
Extrinsic: $115 - $100 = $15.00
Extrinsic_pct: $15 / $115 = 13.0%
Annualized: 13.0% × (365/550) = 8.6%

Verdict: Too expensive. The annualized extrinsic cost (8.6%) exceeds margin rates (6-8%).
```

```
SPY @ $500, Jan 2027 450 Call (18 months)
Option price: $72.00
Intrinsic: $500 - $450 = $50
Extrinsic: $72 - $50 = $22.00
Extrinsic_pct: $22 / $72 = 30.6%
Annualized: 30.6% × (365/550) = 20.3%

Verdict: This is NOT a stock replacement. 30% extrinsic defeats the purpose.
```

```
SPY @ $500, Jan 2027 350 Call (18 months)
Option price: $161.00
Intrinsic: $500 - $350 = $150
Extrinsic: $161 - $150 = $11.00
Extrinsic_pct: $11 / $161 = 6.8%
Annualized: 6.8% × (365/550) = 4.5%

Verdict: Acceptable. ~4.5% annualized extrinsic cost. Capital saved: $50,000 - $16,100 = $33,900.
At 5% T-bill rate: $33,900 × 5% = $1,695/year. Net cost: ~$700/year for leverage + defined risk.
```

## LEAPS vs. Stock: Head-to-Head

| Feature | 100 Shares SPY | 1 LEAPS Call (80Δ) | Winner |
|---------|---------------|-------------------|--------|
| Capital required | $50,000 | ~$13,000 | LEAPS |
| Upside participation | 100% | ~85-90% | Stock |
| Max loss | $50,000 | $13,000 | LEAPS |
| Dividends | Yes (~1.3% yield) | No | Stock |
| Voting rights | Yes | No | Stock |
| Theta decay | None | -$2 to -$5/day | Stock |
| Margin interest | None (if cash) | None | Tie |
| Liquidity | Excellent (anytime) | Good (market hours) | Stock |
| Tax treatment | LTCG after 1 year | LTCG after 1 year (if held > 1yr) | Tie |
| Assignment risk | None | Yes (if DITM near expiration) | Stock |
| Can sell covered calls against | No (need 100 more shares) | Yes (PMCC — see leaps-diagnals) | LEAPS |
| Expiration | None | Must roll or exercise within 2-3 years | Stock |

## The Dividend Gap

[VERIFIED] LEAPS holders do NOT receive dividends. For SPY (~1.3% yield), this is a real cost:
```
Annual dividend loss on LEAPS vs. 100 shares: $50,000 × 1.3% = $650/year
```

This must be factored into the LEAPS cost calculation. Some traders partially offset this through PMCC (selling short-dated calls against the LEAPS to capture premium ≈ dividend yield).

## When LEAPS Stock Replacement Wins

| Scenario | Stock | LEAPS | Winner |
|----------|-------|-------|--------|
| 12-month bull view, limited capital | Capital-intensive | 75% less capital | **LEAPS** |
| Multi-decade buy-and-hold | No expiration, dividends compound | Must roll every 2-3 years, no dividends | **Stock** |
| Volatile stock, want defined risk | Full downside exposure | Defined max loss | **LEAPS** |
| High-dividend stock (>3% yield) | Captures dividends | Misses significant dividends | **Stock** |
| Writing covered calls | Need 100 shares (or LEAPS+PMCC) | PMCC works but is complex | **Depends** |
| Tax-loss harvesting | Sell shares, realize loss | Sell LEAPS, realize loss | **Tie** |

## Provenance

[VERIFIED] LEAPS defined by CBOE as equity options with expiration > 9 months. Available on ~2,500 stocks and ETFs.
[COMPUTED] Extrinsic value computed as option_price - max(0, S-K). Annualization: (extrinsic/option_price) × (365/DTE).
[COMMON-PRACTICE] DITM strike selection at 0.80-0.85 delta from practitioner guides (Natenberg, McMillan).
[BACKTEST-EVIDENCE] Trading project analysis confirms simpler directional strategies (long calls) with proper exits outperform complex multi-leg structures for directional trades. LEAPS are the simplest directional options expression.
[AS OF 2026-07]
