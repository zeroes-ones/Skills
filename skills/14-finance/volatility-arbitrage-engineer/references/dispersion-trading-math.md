# Dispersion Trading Mathematics

## Core Concept

Dispersion trading exploits the gap between index implied volatility and the weighted average implied volatility of its constituents. The trade: **long index options, short a basket of single-stock options** (or vice versa).

## The Fundamental Relationship

The variance of a portfolio equals the weighted sum of individual variances adjusted for correlations:

$$\sigma^2_{index} = \sum_{i} w_i^2 \sigma_i^2 + 2 \sum_{i < j} w_i w_j \sigma_i \sigma_j \rho_{ij}$$

Or equivalently, in terms of the portfolio variance vs individual variances:

$$\sigma^2_{index} = \sum_i w_i^2 \sigma_i^2 + \sum_{i \neq j} w_i w_j \sigma_i \sigma_j \rho_{ij}$$

The key insight: **Index implied volatility should always be LOWER than the weighted average of constituent implied volatilities** because diversification reduces risk. When index IV is HIGHER than the weighted constituent IV, a dispersion trade is potentially profitable.

## The Dispersion Signal

```python
def compute_dispersion_signal(index_ticker, constituents, index_iv, constituent_ivs, weights):
    """Compute the dispersion signal — the gap between index IV and weighted constituent IV."""

    # Weighted average constituent IV
    weighted_avg_iv = sum(w * iv for w, iv in zip(weights, constituent_ivs))

    # The dispersion premium
    dispersion_premium = index_iv - weighted_avg_iv

    # Theoretical relationship: index IV should be ~70-85% of weighted constituent IV
    # due to diversification (correlation < 1.0)
    implied_correlation = (index_iv**2 - sum(w**2 * iv**2 for w, iv in zip(weights, constituent_ivs))) / \
                          (2 * sum(w[i] * w[j] * constituent_ivs[i] * constituent_ivs[j]
                                   for i in range(len(constituents))
                                   for j in range(i+1, len(constituents))))

    return {
        "weighted_avg_constituent_iv": weighted_avg_iv,
        "index_iv": index_iv,
        "dispersion_premium": dispersion_premium,
        "premium_pct": dispersion_premium / weighted_avg_iv,
        "implied_correlation": implied_correlation,
        "signal": "long_dispersion" if dispersion_premium > 0.02 else (
                  "short_dispersion" if dispersion_premium < -0.02 else "neutral"),
    }
```

## Trade Construction

### Long Dispersion Trade (Index IV > Weighted Constituent IV)

**When:** Index options are expensive relative to single-stock options. Implied correlation is HIGHER than historical.

**Structure:**
- **Sell** index straddle/strangle (short index vol — expensive)
- **Buy** straddles/strangles on the basket of constituents (long single-stock vol — cheap)

This profits when:
1. Realized correlation is LOWER than implied (diversification benefits appear in reality)
2. Single-stock realized vol exceeds their implied vol (cheap options pay off)

### Short Dispersion Trade (Index IV < Weighted Constituent IV)

**When:** Single-stock options are expensive relative to index options. Implied correlation is LOWER than historical (e.g., pre-earnings season).

**Structure:**
- **Buy** index straddle/strangle (long index vol — cheap)
- **Sell** straddles/strangles on the basket of constituents (short single-stock vol — expensive)

This profits when:
1. Realized correlation is HIGHER than implied (stocks move together more than priced)
2. Single-stock realized vol is LOWER than their implied vol (expensive options expire worthless)

## Practical Implementation

### Constituent Selection

Not all index constituents are tradeable. Selection criteria:
- **Min option volume:** 1000+ contracts daily
- **Min market cap:** Typically top 20-50 by weight
- **Sector diversification:** Avoid over-concentration
- **Earnings exclusion:** Remove any constituent with earnings in the trade window

### Weighting

Replicate the index weight approximately, but normalize:
```python
selected_weights = [w / sum(selected_weights) for w in selected_weights]
```

### Vega Neutrality

The trade should be vega-neutral at inception:
```python
index_vega_per_contract = compute_vega(index_option)
constituent_vegas = [compute_vega(opt) for opt in constituent_options]

# Scale index position
total_constituent_vega = sum(constituent_vegas)
index_contracts = total_constituent_vega / index_vega_per_contract
```

### Delta Hedging

Both legs should be delta-hedged daily (or more frequently for larger positions):
- Index leg: Hedge with index futures or ETF
- Single-stock legs: Hedge individually with stock

## Risk Management

### Correlation Risk

The #1 risk. If correlation spikes unexpectedly on a long dispersion trade:
- Index IV rises (costs you on the short)
- Single-stock options may not move enough to compensate
- Stop loss: close trade if implied correlation exceeds historical 90th percentile

### Gap Risk

Single-stock gaps (earnings, M&A, regulatory) are the #2 risk:
- A gap on ONE constituent of the short basket can wipe out gains from 20+
- Always check earnings calendar
- Exclude M&A targets, regulatory-sensitive stocks

### Liquidity Risk

Dispersion trades are large — often 20+ options positions:
- Execution cost compounds
- Rolling/hedging costs are significant
- Minimum account size: $250K+ for meaningful dispersion trading

### Sizing

```python
max_dispersion_allocation = account_value * 0.15  # 15% max
max_single_stock_short_vega = account_value * 0.005  # 0.5% per name
```

## Dispersion Trade Examples

### Example 1: SPX Dispersion (Long)

**Setup:** SPX IV = 18.5%. Weighted top-20 constituent IV = 15.2%.
**Signal:** Dispersion premium = +3.3% (index vol expensive).
**Action:** Short SPX straddle. Long straddles on 20 constituents.
**Result:** Realized correlation = 0.35 vs implied 0.55. Single-stock realized vol averaged 17.8% vs 15.2% implied. Profit: +$12K on $3M notional.

### Example 2: Pre-Earnings Dispersion (Short)

**Setup:** Earnings season approaching. Implied correlation = 0.25 (artificially low due to pre-earnings IV in single names).
**Signal:** Index vol cheap relative to single-stock.
**Action:** Long SPX strangle. Short single-stock strangles (ex-earnings).
**Result:** Earnings season produces correlated moves. Implied correlation converges to 0.40. Profit: +$8K on $2.5M notional.

## When NOT to Trade Dispersion

- **VIX < 12:** Vol premiums are too thin to cover execution costs
- **VIX > 35:** Correlation assumptions break down. Everything correlates to 0.80+ in a crash
- **Earnings season peak week:** Single-stock vol structure is distorted
- **Fed days:** Binary macro events override dispersion dynamics
- **Account < $250K:** Execution costs exceed potential edge

## Summary

Dispersion trading is one of the few "pure" volatility arbitrage strategies remaining in liquid markets. The edge comes from the structural relationship between index vol and single-stock vol — it's mathematical, not directional. But the edge is small (1-3% of notional annually) and execution costs can easily consume it. This is an institutional strategy that requires scale, sophisticated execution, and rigorous risk management.
