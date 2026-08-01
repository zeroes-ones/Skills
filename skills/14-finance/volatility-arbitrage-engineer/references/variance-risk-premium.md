# Variance Risk Premium (VRP) Harvesting

## What is the Variance Risk Premium?

The VRP is the difference between implied variance (what options price in) and realized variance (what actually happens):

$$VRP = IV^2 - RV^2$$

Or expressed as a premium ratio:

$$VRP_{ratio} = \frac{IV}{RV}$$

Historically, **SPX implied volatility exceeds realized volatility by 3-5 volatility points on average** [VERIFIED]. This is the "insurance premium" investors pay to protect against downside risk. Systematically selling this premium is the variance risk premium strategy.

## The VIX-VRP Relationship

The VRP is NOT constant. It varies with:
- **VIX level:** VRP is highest when VIX > 25 (fear premium)
- **Term structure:** VRP is largest in the front month (highest fear)
- **Market regime:** VRP expands during drawdowns, contracts during bull markets
- **Event risk:** VRP spikes pre-FOMC, pre-elections, pre-earnings season

## VRP Harvesting Strategies

### Strategy 1: Short SPX Straddles (Simple but Risky)

```python
def short_spx_straddle_signal(vix, iv_rank, vrp):
    """Signal for short SPX straddle based on VRP."""

    # Only sell when premium is rich
    if vrp < 3.0:  # VRP too thin
        return {"action": "no_trade", "reason": f"VRP {vrp:.1f} below minimum 3.0"}

    # Size based on VRP richness
    if vrp > 6.0:
        size_mult = 0.5  # Extreme premium = extreme risk. Size DOWN
    elif vrp > 4.5:
        size_mult = 0.75  # Good premium, moderate size
    else:
        size_mult = 1.0   # Standard premium

    # Exit the trade early (don't hold through large moves)
    return {
        "action": "sell_straddle",
        "dte": 30,
        "size_multiplier": size_mult,
        "profit_target": 0.50,  # Close at 50% of credit
        "stop_loss": 2.0,       # 2× credit stop
    }
```

**Caveat:** Short straddles have UNLIMITED risk on the call side. This is NOT a set-and-forget strategy. Delta hedging is essential.

### Strategy 2: Short Strangles (Defined Risk Proxy)

More practical than straddles — the wings limit catastrophic risk:

```python
def short_strangle_vrp(underlying_price, iv, expected_move):
    """Strangle with 0.10-0.15 delta wings."""

    # Place wings outside 1.5× expected move
    em = underlying_price * iv * sqrt(30/365)  # 30-day expected move

    call_strike = underlying_price + 1.5 * em
    put_strike = underlying_price - 1.5 * em

    # Only trade if credit > 1.5% of underlying
    credit = estimate_strangle_credit(underlying_price, call_strike, put_strike)
    min_credit = underlying_price * 0.015

    if credit < min_credit:
        return {"action": "no_trade", "reason": "Credit too small for risk"}

    return {
        "action": "sell_strangle",
        "call_strike": call_strike,
        "put_strike": put_strike,
        "credit": credit,
    }
```

### Strategy 3: Ratio Put Spreads (Bullish VRP with Downside Protection)

For harvesting VRP with a bullish bias:

- Sell 2 ATM puts
- Buy 1 OTM put (further OTM)
- Net credit. Bullish. If the stock goes up, keep the credit. If it drops moderately, the long put caps losses. If it crashes, the 2:1 ratio hurts but is defined.

### Strategy 4: Variance Swaps (Institutional Only)

Variance swaps are the purest VRP instrument — direct exchange of realized vs implied variance. However:
- Institutional only (ISDA required)
- Minimum notional typically $1M+
- Counterparty risk
- No daily mark-to-market liquidity

For retail: VIX futures and options are the closest proxies.

## VRP Calendar Effects

| Period | VRP Characteristic | Strategy Adjustment |
|--------|-------------------|---------------------|
| Pre-FOMC (3 days before) | VRP expands 20-30% | Increase size by 20%. Close before the announcement |
| Post-FOMC (day after) | VRP collapses | Wait 1 day for IV to settle. Then re-enter |
| Pre-OPEX (3 days before) | VRP compressed (pin risk priced out) | Reduce size by 30% |
| Monthly OPEX day | VRP minimal (front month expiring) | Trade next month only |
| Earnings season peak week | VRP distorted per-name | Avoid systematic VRP. Trade dispersion instead |
| August / December | VRP thin (low volume, holidays) | Reduce size by 50% |
| VIX > 30 | VRP large but dangerous | Reduce size by 50%. Tight stops |
| VIX > 40 | VRP extreme, gap risk extreme | No new entries. Close existing |

## VRP Performance Characteristics

Historical SPX VRP strategy (short 30-delta strangles, 30 DTE, managed at 50% profit):

| Period | Annualized Return | Max Drawdown | Sharpe | Win Rate |
|--------|------------------|--------------|--------|----------|
| 2010-2019 (bull) | +12-15% | -25% | 1.0-1.2 | 75-80% |
| 2020 (COVID) | -30 to -50% | -50%+ | -1.5 | 40-50% |
| 2021 (recovery) | +18-22% | -15% | 1.5-1.8 | 80-85% |
| 2022 (bear) | -10 to -15% | -30% | -0.5 | 55-60% |

**Key insight:** VRP harvesting has positive expectancy over the long run but experiences severe tail events (2020 COVID). Position sizing and correlation awareness are critical.

## Implementation Notes

### Capital Efficiency

Short strangles on portfolio margin:
- SPX strangle (30 DTE, 10-delta wings): ~$8K-12K margin per strangle
- SPY strangle (same specs): ~$2K-3K margin per strangle
- 10 SPY strangles = 1 SPX strangle approximately (capital efficiency favors SPX for larger accounts)

### Delta Hedging Frequency

- Daily delta hedging is sufficient for most accounts
- Intraday hedging adds cost without proportional risk reduction at < $1M notional
- Hedge to delta-neutral at market close. Let intraday deltas float within ±0.15

### When to STOP Harvesting VRP

- **VIX > 35 for 3+ consecutive days:** Systemic vol event. Close all short vol.
- **Drawdown > -15% on the VRP book:** Reduce by 50%.
- **Drawdown > -25% on the VRP book:** Close everything. Wait 1 month.
- **VIX term structure in backwardation for > 5 days:** Near-term risk is severe. Exit.

## Summary

VRP harvesting is the most persistent edge in options markets — investors systematically overpay for downside protection. But it's not free money: the premium exists BECAUSE of tail risk. A VRP strategy that works for 3 years can lose 50% in 3 weeks. Sizing, correlation control, and volatility-based exit rules are the difference between harvesting VRP and being harvested by it.
