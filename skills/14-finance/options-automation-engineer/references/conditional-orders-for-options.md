# Conditional Orders for Options

## The Challenge

Options conditional orders (OCO, bracket, trailing stops) are significantly more complex than equity equivalents because the "price" of an option is a function of 5+ variables (underlying, IV, time, rates, dividends), not just the underlying price. An OCO based solely on the option's price can trigger on IV changes, not directional movement.

## Order Types Matrix

| Order Type | What It Does | Best For | Limitation |
|-----------|-------------|----------|------------|
| **OCO (One Cancels Other)** | Two orders linked: fill one → cancel the other | Simultaneous profit target + stop loss | Only 2 legs. Both orders must be on the same side |
| **Bracket (OTO → OCO)** | Entry order triggers two exit orders (OCO pair) | Full trade lifecycle: enter, then auto-exit on target or stop | Entry must fill first |
| **Trailing Stop (underlying)** | Stop follows underlying price × offset | Momentum trades where you want to lock in gains | Trailing offset must account for option's gamma/delta |
| **Trailing Stop (option price)** | Stop follows option's own price | Single-leg directional trades | Option price jumps on IV spikes. Short vol positions can false-trigger |
| **Conditional on Underlying** | Trigger when underlying hits $X (not option price) | Spreads and multi-leg positions where underlying is the driver | Underlying-based trigger. Option fill at market may have slippage |
| **Contingent (If-Then)** | If order A fills → submit order B | Legging into spreads intentionally (rare) | Legging risk. If B doesn't fill, you're naked |

## OCO Construction for Options

### Standard OCO: Profit Target + Stop Loss

```
ENTRY: Buy 1 AAPL 200 Call at $5.00
  │
  ├─ PROFIT TARGET: Sell 1 AAPL 200 Call at $10.00 LIMIT (100% gain)
  └─ STOP LOSS: Sell 1 AAPL 200 Call at $2.50 STOP MARKET (50% loss)

  (Either fills → cancel the other)
```

**Caveat for OCO stops on options:**
- Stop market on options can have massive slippage during volatility events
- Stop limit can be missed entirely (gap through the limit)
- Recommendation: Stop market for liquid underlyings (SPY, QQQ, AAPL). Stop limit with 5-10% buffer for everything else.

### OCO for Credit Spreads

```
ENTRY: Sell 1 SPY 450/445 Bull Put Spread at $1.50 credit
  │
  ├─ PROFIT TARGET: Buy to close at $0.75 LIMIT (50% profit)
  └─ STOP LOSS: Buy to close at $3.00 STOP MARKET (2× credit loss)

  (Either fills → cancel the other)
```

### OCO Based on Underlying Price (not option price)

For spread positions, underlying-based triggers are more reliable than option-price triggers:

```
ENTRY: Sell 1 QQQ 380/375 Bull Put Spread at $1.20 credit
  │
  ├─ PROFIT TARGET: Buy to close spread at MARKET when QQQ ≥ $385 (target hit)
  └─ STOP LOSS: Buy to close spread at MARKET when QQQ ≤ $375.50 (breach of support)
```

**Why underlying-based triggers for spreads:**
- Option price on a spread is the net of 2 option prices, each with its own bid-ask
- Underlying price is unambiguous and directly tied to your thesis
- Avoids IV-driven false triggers on the option price

## Bracket Orders (OTO + OCO)

The full lifecycle: enter → auto-exit on target or stop.

```
BRACKET:
├─ ENTRY (OTO): Buy 1 SPY 450 Call at $4.50 LIMIT (one triggers other)
│  └─ IF FILLED → Submit OCO:
│     ├─ SELL: SPY 450 Call at $9.00 LIMIT (100% target)
│     └─ SELL: SPY 450 Call at $2.25 STOP MKT (50% stop)
```

**Bracket limitations for options:**
- Entry limit may not fill if the market moves quickly
- If entry partially fills, does OCO activate? (broker-specific — check)
- Some brokers don't support brackets on complex/spread orders

## Trailing Stops for Options

### Trailing by Underlying Price

```
ENTRY: Buy 1 IWM 210 Call at $3.00 with IWM at $208
TRAILING STOP: Sell call at MARKET when IWM drops $2.00 from highest point since entry

If IWM reaches $212 (highest), stop adjusts to $210
If IWM reaches $215 (highest), stop adjusts to $213
If IWM drops to $213, stop triggers
```

### Trailing Offset Calibration

The trailing offset must account for the option's delta and the underlying's normal volatility:

```
trailing_offset = (option_price_stop_pct / delta) + ATR_buffer

Example:
- Call delta = 0.40
- Want to stop out at 50% option loss ($1.50 on $3.00 entry)
- ATR(14) = $3.50 (1.7% of $208)
- trailing_offset = ($1.50 / 0.40) + ($3.50 × 0.5) = $3.75 + $1.75 = $5.50

Set trailing stop at $5.50 below IWM's high since entry
```

### Gamma Consideration

**Critical:** As DTE decreases and the option approaches the money, gamma increases. A small underlying move can cause a large delta shift, making the option price jump.

For DTE ≤ 14: reduce trailing offset by 25% (tighter stop) to account for gamma acceleration.
For DTE ≤ 7: reduce trailing offset by 40%.

## Conditional on IV (Volatility-Based Triggers)

```
CONDITION: If VIX > 30 while position is open
ACTION: Close 50% of all short-vol positions (credit spreads, iron condors, strangles)
```

```
CONDITION: If SPY IV Rank > 90
ACTION: Halt all new credit spread entries. Switch to debit spreads or wait
```

## Broker-Specific Support

| Feature | IBKR | TDA/Schwab | Tradier | tastytrade |
|---------|------|-----------|---------|------------|
| OCO orders | ✅ | ✅ | ✅ | ✅ |
| Bracket (OTO+OCO) | ✅ | ✅ | ✅ | ✅ |
| Trailing stop (underlying) | ✅ | ✅ | ✅ | ✅ |
| Trailing stop (option price) | ✅ | Limited | ❌ | ✅ |
| Conditional on underlying | ✅ | ✅ (Conditional orders) | ❌ | ✅ |
| Conditional on IV | ❌ (custom algo only) | ❌ | ❌ | ❌ |
| Complex OCO (spreads) | ✅ | Limited | ❌ | ✅ |
| Time-in-force customization | Full | Full | Limited | Full |

## Conditional Order Templates

### Template 1: Credit Spread Swing Entry with Auto-Exit

```yaml
strategy: bull_put_spread_swing
underlying: SPY
entry:
  order_type: limit
  action: sell_to_open
  legs:
    - strike: "{R1} P"   # nearest support
      action: sell
    - strike: "{R1 - width} P"
      action: buy
  dte_min: 30
  dte_max: 45
  limit: 0.30  # credit per spread

exit:
  profit_target:
    type: limit
    action: buy_to_close
    trigger: "mark <= 0.15"  # 50% of 0.30 credit
  stop_loss:
    type: stop_market
    action: buy_to_close
    trigger: "mark >= 0.60"  # 2× credit

  time_exit:
    type: limit
    action: buy_to_close
    trigger: "dte <= 14"
    limit: 0.05  # close for pennies if 50% target never hit
```

### Template 2: Debit Spread Momentum Entry with Trailing Stop

```yaml
strategy: call_debit_spread_momentum
underlying: {ticker}
entry:
  condition: "price > 20SMA AND RSI > 50 AND ADX > 25"
  order_type: limit
  action: buy_to_open
  legs:
    - strike: ATM
      action: buy
    - strike: "{ATM + width}"
      action: sell
  dte_min: 30
  dte_max: 45
  limit: "{mid - 0.05}"

exit:
  trailing_stop:
    type: stop_market
    trigger: "{underlying} drops {trailing_offset} from high"
  time_exit:
    dte: 14
    action: sell_to_close
```

## Failure Modes

| Failure | Cause | Prevention |
|---------|-------|------------|
| Stop limit never filled, position lost 3× stop | Underlying gapped through stop limit price | Use stop market for liquid underlyings. Wider limit buffer for others |
| OCO profit target triggered, stop still executed | Broker delay in cancel propagation | Use broker's native OCO. Do not simulate OCO with separate orders |
| Trailing stop triggered by false breakdown (1-min candle wick) | Short-term noise exceeding trailing offset | Apply FalseStopGuard: 4-layer confirmation before stop execution |
| Bracket entry filled, OCO never submitted | Broker rejects OCO on spread orders | Verify broker supports bracket on complex orders before entering |

## Summary

- **Use underlying-based triggers** for spread positions (not option-price-based)
- **Account for gamma in trailing stops** — tighten as DTE decreases
- **Always use native OCO, not simulated OCO** — propagation delays can cause double-fills
- **Test conditional orders in paper trading** before committing real capital
- **Volatility-based conditions** are critical but not supported natively — require external monitoring
