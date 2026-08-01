# Scanner-to-Execution Pipeline

## Architecture Overview

```
[SCANNER] → [FILTER CHAIN] → [STRATEGY SELECTOR] → [SIZING ENGINE] → [ORDER BUILDER] → [EXECUTION] → [MONITOR] → [JOURNAL]
     │              │                │                    │                  │              │             │            │
  Scan all      Apply         Match setup       Calculate          Construct        Route        Track        Log
  underlyings   technical     to strategy       position           native           to broker    P&L in       trade
  for setups    + liquidity   template          size               spread order                  real-time    result
```

## Layer 1: Scanner

### What to Scan

```python
SCAN_CONFIG = {
    "underlyings": [],  # Populated from watchlist + liquid ETFs
    "min_option_volume": 1000,   # Daily option volume threshold
    "min_stock_price": 10.00,    # Avoid penny stocks
    "min_stock_volume": 500000,  # Daily stock volume
    "exclude_earnings_within_days": 5,  # Earnings blackout
    "exclude_underlyings": ["VIX", "UVXY", "SQQQ"]  # Leveraged/vol products
}
```

### Scanner Types

| Scanner | What It Finds | Input | Output |
|---------|--------------|-------|--------|
| **Pullback Scanner** | Stocks in uptrend, pulled back to MA on lower volume | 50SMA, 20SMA, volume | Tickers + pullback depth |
| **Gap Scanner** | Stocks gapped overnight, filling or continuing | Pre-market data, prior close | Tickers + gap % + gap direction |
| **IV Rank Scanner** | Stocks with high IV Rank for credit spreads | IV Rank data | Tickers + IV Rank + IV percentile |
| **Earnings Drift Scanner** | Stocks with post-earnings drift (PEAD) | Earnings data, price history | Tickers + surprise + drift direction |
| **Sector RS Scanner** | Sectors showing relative strength rotation | Sector ETF prices | Sectors + RS rank + momentum |
| **Support/Resistance Scanner** | Stocks approaching key S/R levels | Level data, price | Tickers + distance to S/R |

### Scanner Implementation Pattern

```python
def scan_pullbacks(universe, config):
    """Find pullback setups."""
    results = []
    for ticker in universe:
        # Get daily data
        df = get_daily_data(ticker, lookback=90)
        if df.empty:
            continue

        # Trend check: price > 50SMA, 20SMA > 50SMA
        if not (df['close'].iloc[-1] > df['50SMA'].iloc[-1] and
                df['20SMA'].iloc[-1] > df['50SMA'].iloc[-1]):
            continue

        # Pullback check: price near 20SMA, below recent high
        recent_high = df['high'].rolling(20).max().iloc[-1]
        pullback_pct = (recent_high - df['close'].iloc[-1]) / recent_high

        if not (0.01 < pullback_pct < 0.05):  # 1-5% pullback
            continue

        # Volume check: pullback on lower volume
        avg_vol = df['volume'].rolling(20).mean().iloc[-1]
        if df['volume'].iloc[-3:].mean() > avg_vol * 1.1:
            continue  # Too much volume on pullback

        results.append({
            "ticker": ticker,
            "pullback_pct": pullback_pct,
            "support_level": df['20SMA'].iloc[-1],
            "rsi": compute_rsi(df),
            "trend_duration": count_days_above_50sma(df),
        })

    return sorted(results, key=lambda x: x["pullback_pct"], reverse=True)
```

## Layer 2: Filter Chain

Apply filters sequentially. Each filter eliminates candidates. Order by computational cost (cheapest first).

```python
FILTER_CHAIN = [
    # 1. Liquidity filter (cheapest check)
    lambda r: get_option_oi(r["ticker"], dte=45) > 100,

    # 2. Spread filter
    lambda r: get_option_spread(r["ticker"], r["support_level"], dte=45) < 0.05,

    # 3. Earnings blackout
    lambda r: days_to_next_earnings(r["ticker"]) > 10,

    # 4. Correlation filter (vs existing positions)
    lambda r: compute_correlation(r["ticker"], existing_positions) < 0.8,

    # 5. Signal quality filter
    lambda r: r.get("trend_duration", 0) > 20,  # At least 20 days in trend
]
```

## Layer 3: Strategy Selector

Based on the setup, select the appropriate strategy template:

| Setup | Strategy | Structure | DTE |
|-------|----------|-----------|-----|
| Pullback to 20SMA in uptrend, RSI 40-50 | Bull Put Spread | Credit spread, 0.25-0.30Δ short | 30-45 |
| Pullback deeper (to 50SMA), RSI < 35 | ATM Debit Spread | Debit spread, ATM long | 45-60 |
| Sector RS rotation, strong sector | Sell put spread on sector ETF | Credit spread, 0.20-0.25Δ | 30-45 |
| Earnings drift confirmed (3+ days) | Debit spread in drift direction | Debit spread, ATM | 40-50 |
| IV Rank > 70, range-bound | Iron Condor | 0.15-0.20Δ wings | 30-45 |
| Gap fill pattern, > 1% gap, opening | Gap fade debit/credit spread | Direction opposite gap | 21-30 |

## Layer 4: Sizing Engine

```python
def calculate_position_size(account_value, strategy, setup_quality,
                            iv_rank, broad_market_regime):
    """Calculate position size in number of contracts."""

    # Base: 2% of account per trade
    base_risk = account_value * 0.02

    # Adjust for strategy risk profile
    strategy_risk_multipliers = {
        "bull_put_spread": 1.0,
        "bear_call_spread": 1.0,
        "iron_condor": 0.8,
        "debit_spread": 0.6,  # Debit spreads have lower win rates
        "calendar_spread": 0.7,
    }
    risk_mult = strategy_risk_multipliers.get(strategy, 1.0)

    # Volatility-adjusted sizing (Trading project formula)
    hv_percentile = get_hv_percentile()
    vol_mult = 1.5 - (hv_percentile / 100) * 1.1
    vol_mult = max(0.3, min(1.5, vol_mult))

    # Regime multiplier
    vix = get_vix()
    if vix < 15:
        regime_mult = 1.0  # Low vol, full size
    elif vix < 20:
        regime_mult = 0.9
    elif vix < 25:
        regime_mult = 0.7
    elif vix < 30:
        regime_mult = 0.5
    else:
        regime_mult = 0.3  # VIX > 30, reduce significantly

    # September/October seasonal adjustment
    from datetime import datetime
    if datetime.now().month in [9, 10]:
        regime_mult *= 0.5

    # Setup quality multiplier (0.5-1.0)
    quality_mult = max(0.5, min(1.0, setup_quality))

    # Final risk amount
    risk_per_trade = base_risk * risk_mult * vol_mult * regime_mult * quality_mult

    # Convert to contracts
    spread_width = get_spread_width(strategy)
    contracts = int(risk_per_trade / (spread_width * 100))

    return max(1, min(contracts, 50))  # 1-50 contract range
```

## Layer 5: Order Builder

```python
def build_native_spread_order(ticker, strategy, contracts, dte):
    """Build a broker-agnostic spread order representation."""

    strikes = get_option_strikes(ticker, strategy, dte)

    order = {
        "ticker": ticker,
        "action": strategy["action"],  # "sell_to_open" or "buy_to_open"
        "strategy_type": strategy["type"],
        "contracts": contracts,
        "dte": dte,
        "order_type": "limit",
        "limit_price": calculate_limit(strategy, strikes),
        "time_in_force": "day",
        "legs": [
            {
                "strike": strikes["short"],
                "option_type": strategy["option_type"],
                "action": "sell" if strategy["action"] == "sell_to_open" else "buy",
            },
            {
                "strike": strikes["long"],
                "option_type": strategy["option_type"],
                "action": "buy" if strategy["action"] == "sell_to_open" else "sell",
            },
        ]
    }

    return order
```

## Layer 6: Execution

See `multi-leg-execution.md` for exchange routing, order types, and fill quality monitoring.

## Layer 7: Monitor

```python
def monitor_position(position):
    """Monitor a position and trigger exit/roll actions."""

    checks = {
        "profit_target": check_profit_target(position),
        "stop_loss": check_stop_loss(position),
        "time_stop": check_time_stop(position),
        "thesis_invalidation": check_thesis(position),
        "roll_signal": check_roll_signal(position),
        "gamma_risk": check_gamma_zone(position),
    }

    return [action for action, triggered in checks.items() if triggered]
```

## Layer 8: Journal

Every execution, adjustment, and exit logged to a structured journal. See `circuit-breakers-and-safety.md` for audit trail requirements.

## Pipeline Configuration

```yaml
pipeline:
  name: "swing_credit_spreads"
  schedule: "market_open"  # or "continuous", "hourly", "eod"
  scanner:
    type: "pullback"
    universe: ["SPY", "QQQ", "IWM", "AAPL", "MSFT", "GOOGL", "AMZN", "META"]
    min_option_volume: 1000
  filters:
    min_oi: 100
    max_spread: 0.05
    earnings_blackout_days: 10
    max_correlation: 0.8
  strategy:
    type: "bull_put_spread"
    dte_min: 30
    dte_max: 45
    short_delta: 0.25
    width: 5  # points
  sizing:
    base_risk_pct: 0.02
    kelly_fraction: 0.5
    max_contracts: 20
  execution:
    order_type: "native_spread_limit"
    limit_offset: -0.05  # price improvement at mid
    max_attempts: 3
    retry_delay_seconds: 30
  monitoring:
    profit_target_pct: 0.50
    stop_loss_multiplier: 2.0
    time_stop_dte: 14
    gamma_zone_dte: 7
```

## Summary

The pipeline transforms scans from "what looks interesting" to "what can be systematically traded with defined risk, automated execution, and monitored exits." Each layer is independently testable and can be tuned via backtesting against the Trading project's data.
