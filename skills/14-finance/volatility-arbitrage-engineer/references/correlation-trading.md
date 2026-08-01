# Correlation Trading

## The Opportunity

Options on baskets, indices, and pairs embed assumptions about correlation. When implied correlation (from options prices) diverges from realized correlation (from actual price movements), correlation trades become possible.

## Correlation Defined

**Realized correlation:** The actual historical correlation between two assets' returns over a lookback period.

**Implied correlation:** The correlation implied by the relationship between index option prices and constituent option prices.

$$\rho_{implied} = \frac{\sigma^2_{index} - \sum_i w_i^2 \sigma_i^2}{2 \sum_{i < j} w_i w_j \sigma_i \sigma_j}$$

## Correlation Trade Types

### Type 1: Dispersion (Index vs Basket)

The most well-known correlation trade. Already covered in detail in `dispersion-trading-math.md`.

**Signal:** Implied correlation > Realized correlation → Short index vol / Long single-stock vol
**Signal:** Implied correlation < Realized correlation → Long index vol / Short single-stock vol

### Type 2: Pair Correlation Trading

Trade the correlation between two highly correlated underlyings:

```python
def pair_correlation_signal(ticker_a, ticker_b, lookback=60):
    """Detect divergence in correlation structure between two names."""

    # Realized correlation over lookback
    ret_a = get_returns(ticker_a, lookback)
    ret_b = get_returns(ticker_b, lookback)
    realized_corr = np.corrcoef(ret_a, ret_b)[0, 1]

    # Implied correlation from options
    atm_iv_a = get_atm_iv(ticker_a)
    atm_iv_b = get_atm_iv(ticker_b)

    # Normalized IV spread
    iv_spread = abs(atm_iv_a - atm_iv_b)
    historical_iv_spread_avg = get_avg_iv_spread(ticker_a, ticker_b, lookback=252)

    # If realized correlation is high but IV spread is wide:
    # Options imply they'll diverge, but historically they move together
    if realized_corr > 0.80 and iv_spread > 1.5 * historical_iv_spread_avg:
        return {
            "trade": "correlation_convergence",
            "action": f"Sell strangle on {ticker_a if atm_iv_a > atm_iv_b else ticker_b}, "
                      f"buy strangle on the other. IV spread should compress",
            "realized_corr": realized_corr,
            "iv_spread": iv_spread,
            "avg_spread": historical_iv_spread_avg,
        }

    return {"trade": "no_action"}
```

### Type 3: Sector Correlation Trading

Sectors have characteristic correlation structures:

| Sector | Typical Intra-Sector Correlation | Notes |
|--------|--------------------------------|-------|
| Financials (XLF) | 0.70-0.85 | High — macro-driven |
| Technology (XLK) | 0.50-0.70 | Moderate — idiosyncratic winners |
| Energy (XLE) | 0.60-0.80 | High — commodity-driven |
| Healthcare (XLV) | 0.30-0.50 | Low — drug-specific outcomes |
| Utilities (XLU) | 0.40-0.60 | Moderate — rate-sensitive |

When intra-sector implied correlation diverges from these norms:

```python
def sector_correlation_signal(sector_etf, constituents):
    """Trade implied vs historical intra-sector correlation."""

    implied_corr = compute_implied_correlation(sector_etf, constituents)
    historical_corr = get_avg_realized_correlation(constituents, lookback=252)

    z_score = (implied_corr - historical_corr) / get_std_correlation(constituents)

    if z_score > 2.0:
        return "implied_corr_too_high"  # Sector options pricing in excessive correlation
    elif z_score < -2.0:
        return "implied_corr_too_low"  # Sector options pricing in too little correlation

    return "neutral"
```

### Type 4: Correlation Swap (Institutional)

OTC derivative that exchanges realized correlation for a fixed strike correlation:

- Buyer of correlation: Pays fixed correlation, receives realized correlation
- Seller of correlation: Receives fixed correlation, pays realized correlation

Institutional only (ISDA). No retail equivalent, but dispersion trades are a proxy.

## Correlation During Stress

### The Correlation → 1.0 Problem

During market stress, all correlations converge toward 1.0. This is the single most important fact in correlation trading:

- In calm markets: average pairwise SPX correlation = 0.30-0.40
- During corrections (-10%): correlation rises to 0.50-0.60
- During crashes (-20%+): correlation rises to 0.70-0.90
- During panic (2008, 2020): correlation → 0.85-0.95

**Implication for dispersion:** Long dispersion trades (short index vol, long single-stock vol) are short correlation. They get crushed when correlation spikes. Always have a correlation stop: close the trade if realized correlation exceeds the 90th percentile of the 2-year lookback.

### Correlation Regime Detection

```python
def correlation_regime(market_returns, sector_returns, lookback=60):
    """Classify the current correlation regime."""

    avg_pairwise_corr = compute_avg_pairwise_correlation(market_returns)
    corr_trend = avg_pairwise_corr - compute_avg_pairwise_correlation(market_returns, lookback=252)

    if avg_pairwise_corr > 0.60:
        regime = "high_correlation"  # Diversification isn't working
        sizing_mult = 0.5
    elif avg_pairwise_corr < 0.30:
        regime = "low_correlation"  # Stock-picker's market
        sizing_mult = 1.0
    else:
        regime = "normal"
        sizing_mult = 0.8

    # If correlation is RISING (trend), reduce dispersion and pair trades
    if corr_trend > 0.05:
        sizing_mult *= 0.7

    return {"regime": regime, "sizing_multiplier": sizing_mult, "trend": corr_trend}
```

## Correlation Trade Sizing

Correlation trades are levered bets on a second-order relationship. Sizing must be conservative:

```python
MAX_CORRELATION_TRADE_SIZE = account_value * 0.05  # 5% per trade
MAX_TOTAL_CORRELATION_BOOK = account_value * 0.15  # 15% total
```

Correlation stops:
- Dispersion trade: Close if realized correlation > implied correlation + 0.15
- Pair trade: Close if IV spread widens beyond 3σ from historical
- Sector trade: Close if 3+ consecutive days of correlation divergence widening

## Summary

Correlation trading is the most mathematically elegant form of vol arb — it exploits the structural relationship between individual and aggregate volatility. But it's also the most fragile. Correlation assumptions break in stress, and correlation trades are short convexity (they make steady small profits and occasional large losses). Size small, monitor correlation levels daily, and exit fast when the correlation regime shifts.
