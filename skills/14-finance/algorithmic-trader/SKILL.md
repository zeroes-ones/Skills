---
name: algorithmic-trader
description: "Algorithmic trading strategy development and execution: entry/exit/trim strategy design, backtesting engines (vectorized and event-driven), walk-forward optimization, position sizing (Kelly, risk-parity, fixed-fractional), risk management (VaR, CVaR, max drawdown limits, correlation matrices), broker API integration (Alpaca, Interactive Brokers, TD Ameritrade/Schwab), order execution algorithms (TWAP, VWAP, iceberg), and portfolio-level risk monitoring. Triggered by algorithmic trading, trading bot, backtest, position sizing, entry strategy, exit strategy, trim strategy, stop-loss, trailing stop, options flow, unusual options activity, UOA, broker API, Alpaca, Interactive Brokers, order execution, TWAP, VWAP, Kelly criterion, drawdown, risk management, Sharpe ratio."
author: Sandeep Kumar Penchala
type: finance
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - algorithmic-trader
token_budget: 4000
output:
  type: "code"
  path_hint: "./"
chain:
  consumes_from:
    - quantitative-analyst
    - market-data-engineer
    - system-architect
    - backend-developer
    - observability-engineer
  feeds_into:
    - backend-developer
    - frontend-developer
    - observability-engineer
  alternatives:
    - ml-ai-engineer
---
# Algorithmic Trader

Algorithmic trading strategy development and execution — from signal consumption through position
management to post-trade analysis. This skill is the bridge between quantitative research output
and live market execution. Covers entry/exit/trim strategy design for unusual-options-activity
(UOA) signals, multi-engine backtesting, walk-forward optimization, position sizing across
regimes, broker API integration, order execution algorithms, and portfolio-level risk monitoring.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->
```
What are you trying to do?
├── DESIGN a strategy
│   ├── Entry rules for UOA signals → Jump to "Decision Trees > Entry Strategy Selection"
│   ├── Exit / trim rules → Jump to "Decision Trees > Exit & Trim Strategy Selection"
│   └── Position sizing model → Jump to "Core Workflow > Phase 2 (Position Sizing)"
├── BACKTEST or validate
│   ├── Vectorized backtest (fast, approximate) → Jump to "Core Workflow > Phase 6 (Backtesting)"
│   ├── Event-driven backtest (accurate, realistic) → Jump to "Core Workflow > Phase 6 (Backtesting)"
│   └── Walk-forward optimization → Jump to "Best Practices > Walk-Forward Validation"
├── EXECUTE live
│   ├── Broker API integration (Alpaca, IB, Schwab) → Jump to "Core Workflow > Phase 3 (Entry Execution)"
│   ├── Order execution algo (TWAP, VWAP, iceberg) → Jump to "Decision Trees > Order Execution Algorithm"
│   └── Portfolio risk monitoring → Jump to "Core Workflow > Phase 5 (Risk Monitoring)"
├── Analyze a losing streak or drawdown → Jump to "Error Decoder"
├── Design UOA-specific strategy → Jump to "Decision Trees > Entry Strategy Selection"
├── Need quantitative signal generation → Invoke quantitative-analyst skill instead
├── Need ML-based signal detection → Invoke ml-ai-engineer skill as alternative
├── Need market data pipeline (options flow, tick storage) → Invoke `market-data-engineer` skill
├── Need trading system architecture (event bus, failover) → Invoke `system-architect` skill
├── Need order management system / broker API client → Invoke `backend-developer` skill
├── Need trading dashboards / Prometheus alerting → Invoke `observability-engineer` skill
└── Not sure? → Describe the trade or problem in plain language and I will route you
```
Do not read the entire skill. Follow the route above and read only the sections it points to.
## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces. Trading is a domain where overconfidence kills accounts — humility and risk management are non-negotiable.

- **Never trade without a stop-loss.** Every position must have a predefined exit price before entry. A trade without a stop-loss is not a strategy — it is gambling. Hard stops go in at order entry; mental stops are lies you tell yourself during drawdowns.
- **Backtest results are optimistic — always haircut by 30%.** Survivorship bias, look-ahead bias, and in-sample overfitting inflate backtest returns. Reduce Sharpe ratio, win rate, and CAGR by 30% for realistic forward expectations. If the strategy does not survive the haircut, it is not production-ready.
- **Never average down on UOA signals.** Adding to a losing position because "the signal was strong" is how accounts blow up. UOA signals have a shelf life — if price moves against you, the smart money already exited. Cut losers; let winners run. Never add to a position that is underwater.
- **Correlation is the silent portfolio killer.** Five UOA signals on five different tickers can all be the same trade if they are in the same sector. Position-level risk is an illusion without a correlation matrix. Max 30% portfolio exposure to any single sector or factor.
- **Admit what you do not know.** If you do not have option chain liquidity data, borrow costs, or real-time fills data, say so. Recommending a trade without understanding execution reality is malpractice. Ask for the information you need before sizing or entering.

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Designing entry, exit, and trim strategies for unusual options activity (UOA) signals
- Building backtesting engines: vectorized (pandas/numpy) for speed or event-driven for realism
- Running walk-forward optimization to validate strategy robustness across market regimes
- Implementing position sizing: Kelly criterion, fixed-fractional, volatility-adjusted, risk-parity
- Integrating with broker APIs: Alpaca (equity/options), Interactive Brokers (TWS/Client Portal), Schwab (trader API)
- Executing orders with minimal market impact: TWAP, VWAP, iceberg, implementation shortfall algorithms
- Building real-time risk dashboards: VaR, CVaR, beta exposure, correlation matrix, max drawdown monitors
- Conducting post-trade analysis: P&L attribution, slippage audit, signal decay analysis, regime detection
- Hardening a strategy for production: circuit breakers, duplicate order prevention, broker reconnect logic
## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->

### Entry Strategy Selection for UOA Signals

```
                         ┌──────────────────────────────────┐
                         │ START: UOA Signal Received from   │
                         │ quantitative-analyst pipeline     │
                         └───────────────┬──────────────────┘
                                         │
                       ┌─────────────────▼─────────────────┐
                       │ Signal fired during market hours    │
                       │ AND price is within 1% of VWAP?     │
                       └────┬──────────────────────────┬────┘
                            │ YES                      │ NO
                       ┌────▼────────────────┐   ┌─────▼────────────────────┐
                       │ MOMENTUM ENTRY      │   │ Price extended >2% from    │
                       │ Enter 50% now,      │   │ VWAP or signal at open?    │
                       │ wait for confirmation│   └────┬─────────────────┬────┘
                       │ for remaining 50%   │        │ YES             │ NO
                       └─────────────────────┘   ┌────▼──────────┐ ┌───▼──────────────┐
                                                  │ PULLBACK ENTRY│ │ Signal fired      │
                                                  │ Wait for price │ │ overnight/weekend?│
                                                  │ to touch VWAP  │ │ Gap risk >2%?     │
                                                  │ or 20-EMA.     │ └──┬───────────┬───┘
                                                  │ If it never     │    │YES        │NO
                                                  │ pulls back,     │ ┌──▼──────┐ ┌──▼──────────┐
                                                  │ pass on trade   │ │SPREAD    │ │MOMENTUM     │
                                                  └─────────────────┘ │ENTRY     │ │ENTRY on     │
                                                                      │Use options│ │open with    │
                                                                      │vertical   │ │reduced size │
                                                                      │spread to  │ │(25% of      │
                                                                      │define risk│ │normal)      │
                                                                      │and reduce │ └─────────────┘
                                                                      │capital req│
                                                                      └───────────┘
```

**When to choose Momentum Entry:** Signal fires mid-session, price has not already gapped, confirmation within same day or next day. Best for high-conviction signals with strong volume confirmation. **Risk:** Buying into strength can mean buying the top if signal was a bull trap.

**When to choose Pullback Entry:** Price is extended (RSI > 70 for calls, RSI < 30 for puts) when signal fires. Better risk/reward — entry at VWAP or 20-period EMA reduces slippage and improves fill quality. **Risk:** The move might not pull back; you miss the trade entirely.

**When to choose Spread Entry:** Gap risk exceeds 2% (overnight/weekend signals), account is capital-constrained, or underlying has wide bid-ask spreads. Vertical spreads define max loss and reduce buying power requirement by 60-80%. **Risk:** Capped upside; theta decay works against you on long spreads.

### Exit & Trim Strategy Selection

```
                         ┌──────────────────────────────────┐
                         │ START: Position is live.           │
                         │ When and how do you exit?          │
                         └───────────────┬──────────────────┘
                                         │
                       ┌─────────────────▼─────────────────┐
                       │ Has the position hit +20% gain      │
                       │ on equity?                          │
                       └────┬──────────────────────────┬────┘
                            │ YES                      │ NO
                       ┌────▼────────────────┐   ┌─────▼────────────────────┐
                       │ TIER 2 TRIM:         │   │ Has position been open      │
                       │ Sell 25% at +20%.    │   │ for >5 trading days         │
                       │ Move stop to         │   │ without moving in your      │
                       │ breakeven on         │   │ favor?                      │
                       │ remaining position.  │   └────┬─────────────────┬────┘
                       │ Then check:          │        │ YES             │ NO
                       │ ┌──────────────────┐ │   ┌────▼──────────┐ ┌───▼──────────────┐
                       │ │ Hit +40% or       │ │   │ TIME STOP:    │ │ Has the            │
                       │ │ RSI > 70 daily?   │ │   │ Exit 100%.     │ │ underlying signal   │
                       │ └──┬───────────┬───┘ │   │ Smart money    │ │ logic been          │
                       │    │YES        │NO   │   │ moves within   │ │ invalidated?        │
                       │ ┌──▼──────┐ ┌──▼────┐│   │ days. If price │ │ (e.g., data error,  │
                       │ │TIER 3   │ │HOLD   ││   │ is flat, you   │ │ P/C parity break    │
                       │ │TRIM:    │ │with   ││   │ are in the     │ │ was bogus?)         │
                       │ │Sell 25% │ │trailing││   │ wrong trade.   │ └──┬───────────┬─────┘
                       │ │at +40%  │ │stop    ││   └────────────────┘    │YES        │NO
                       │ │or RSI>70│ │(2x ATR)││                      ┌──▼──────────┐ ┌──▼──────────┐
                       │ │Let last │ └────────┘│                      │SIGNAL       │ │TRAILING STOP│
                       │ │25% run  │           │                      │INVALIDATION:│ │MANAGEMENT:  │
                       │ │to trail │           │                      │Exit 100%    │ │2x ATR trail │
                       │ └─────────┘           │                      │immediately. │ │from entry.  │
                       └───────────────────────┘                      │No hesitation│ │Raise stop   │
                                                                      │First loss   │ │as price     │
                                                                      │is best loss │ │moves up.    │
                                                                      └─────────────┘ └─────────────┘
```

**Tier 1 (Risk-Off Trim):** Sell 25% at +10%. Reduces position risk to breakeven on the remainder. This "free trade" psychology reduces emotional decision-making — you are now playing with the house's money.

**Tier 2 (Scaling Trim):** Sell 25% at +20%. Lock in meaningful profit, reduce exposure by half total. Move stop to breakeven.

**Tier 3 (Runner Trim):** Sell 25% at +40% or when daily RSI > 70 (overbought). Let the final 25% ride until the 2x ATR trailing stop is hit.

**Emergency Trim:** Sell 100% immediately if an unexpected news event invalidates the thesis. No partial exits, no "wait and see." First loss is the smallest loss.

### Order Execution Algorithm Selection

```
                         ┌──────────────────────────────────┐
                         │ START: Entry order needs to be    │
                         │ executed. Choose algorithm.       │
                         └───────────────┬──────────────────┘
                                         │
                       ┌─────────────────▼─────────────────┐
                       │ Order size > 1% of daily volume?    │
                       └────┬──────────────────────────┬────┘
                            │ YES                      │ NO
                       ┌────▼────────────────┐   ┌─────▼────────────────────┐
                       │ Need to minimize      │   │ Is the option spread       │
                       │ market impact.         │   │ >5% of mid-price?          │
                       │ ┌──────────────────┐  │   └────┬─────────────────┬────┘
                       │ │ Urgency?          │  │        │ YES             │ NO
                       │ └──┬───────────┬───┘  │   ┌────▼──────────┐ ┌───▼──────────┐
                       │    │HIGH       │LOW   │   │ICEBERG ORDER  │ │LIMIT ORDER   │
                       │ ┌──▼──────┐ ┌──▼────┐│   │Display only 10%│ │Place at mid   │
                       │ │VWAP     │ │TWAP   ││   │of size. Refresh│ │or slightly    │
                       │ │Minimize │ │Spread ││   │as filled.      │ │favorable.     │
                       │ │slippage │ │over   ││   │Avoid signaling │ │Walk the book  │
                       │ │vs VWAP  │ │time   ││   │large interest. │ │if needed.     │
                       │ │benchmark│ │window ││   └────────────────┘ └───────────────┘
                       │ └─────────┘ └───────┘│
                       └──────────────────────┘
```

**When to use VWAP:** High urgency, large size. Participates with volume — buys more when volume is high, less when it is low. Benchmark is the day's VWAP; a good VWAP algo finishes within 2 bps of the benchmark.

**When to use TWAP:** Lower urgency, can spread over 30-90 minutes. Splits order into equal time slices regardless of volume. Simpler than VWAP, slightly higher slippage in volatile names.

**When to use Iceberg:** Wide spreads (>5% of mid), illiquid options, or when you do not want to reveal full size. Displays only 10-20% of the order; refills the displayed quantity as it gets filled.
## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->

<!-- DEEP: 10+min -->
### Phase 1 (~10 min): Signal Reception & Validation

Consume output from the quantitative-analyst pipeline. Every signal must be validated before any capital is committed.

1. **Parse signal envelope**: Extract ticker, direction (CALL=long equity, PUT=short equity), timestamp, conviction score (0.0-1.0), and expected catalyst timeframe from the quantitative-analyst JSON payload.
2. **Liquidity gate**: Check that the underlying trades >500K shares/day and option open interest on the target strike is >1,000 contracts. Illiquid underlyings amplify slippage beyond model assumptions — reject signals on names with average daily volume under 100K.
3. **Correlation gate**: Compare the signal ticker against existing positions. If adding this position would push sector exposure above 30% of portfolio, reduce size or skip. UOA signals cluster — 5 signals in semiconductors is one bet, not five.
4. **News gate**: Scan for pending earnings (within 5 days), FDA decisions, merger votes, or regulatory rulings. Binary event risk trumps any UOA signal. Reduce position size by 50% or skip if an unmodelable event is imminent.
5. **Signal freshness check**: If the signal timestamp is >2 hours old during market hours (or >1 day for overnight signals), check whether the edge has decayed. Compare current price vs. signal price — if the move already happened, the trade is over.

```python
# Signal validation pseudocode
def validate_signal(signal: dict, portfolio: Portfolio, market_data: MarketData) -> SignalDecision:
    if signal['avg_daily_volume'] < 100_000:
        return SignalDecision.REJECT  # insufficient liquidity

    if signal['option_open_interest'] < 1_000:
        return SignalDecision.REJECT

    sector = get_sector(signal['ticker'])
    if portfolio.sector_exposure[sector] + signal['suggested_size'] > 0.30 * portfolio.nav:
        signal['adjusted_size'] = 0.30 * portfolio.nav - portfolio.sector_exposure[sector]
        if signal['adjusted_size'] <= 0:
            return SignalDecision.REJECT  # sector limit reached

    if days_to_earnings(signal['ticker']) <= 5:
        signal['adjusted_size'] *= 0.5

    signal_age_minutes = (datetime.utcnow() - signal['timestamp']).total_seconds() / 60
    if signal_age_minutes > 120:
        price_change = (market_data.last - signal['signal_price']) / signal['signal_price']
        if abs(price_change) > 0.02:  # >2% move already happened
            return SignalDecision.EXPIRED

    return SignalDecision.ACCEPT
```
<!-- DEEP: 10+min -->
### Phase 2 (~15 min): Position Sizing

Translate a validated signal into a concrete share/contract count. Position sizing is where risk management lives — get this wrong and no entry strategy saves you.

1. **Select sizing method**:
   - **Kelly Criterion**: f* = (bp - q) / b where b = win/loss ratio, p = win probability, q = 1-p. Use **half-Kelly** in practice — full Kelly assumes perfect knowledge of edge and can produce 50%+ drawdowns.
   - **Fixed-Fractional**: Risk 1-2% of account NAV per trade. For a $100K account risking 1.5%, max loss per trade = $1,500.
   - **Volatility-Adjusted**: Position size = (Account Risk $) / (ATR_20 * Multiplier). Larger positions in low-volatility names, smaller in high-vol.

2. **Calculate share quantity**:
   ```
   account_risk_dollars = portfolio.nav * risk_per_trade_pct
   stop_distance_pct = abs(entry_price - stop_loss_price) / entry_price
   position_value = account_risk_dollars / stop_distance_pct
   shares = floor(position_value / entry_price)
   ```

3. **Apply Kelly if win/loss data exists**:
   ```python
   def half_kelly_fraction(win_rate: float, avg_win: float, avg_loss: float) -> float:
       b = avg_win / abs(avg_loss)  # win/loss ratio
       p = win_rate
       q = 1 - p
       kelly_f = (b * p - q) / b
       return max(0.0, kelly_f * 0.5)  # half-Kelly, floor at 0

   # Example: 55% win rate, avg win +8%, avg loss -5%
   # b = 8/5 = 1.6, f* = (1.6*0.55 - 0.45)/1.6 = 0.26875
   # Half-Kelly = 13.4% of account... way too aggressive for multi-position portfolio
   # Cap half-Kelly at 5% max position size regardless of formula output
   ```

4. **Apply constraints**:
   - Max single position: 10% of NAV (absolute hard cap)
   - Max sector exposure: 30% of NAV
   - Max gross leverage: 2.0x (long + |short|)
   - Min position size: $2,000 (below this, commissions eat the edge)

5. **Size the trim targets**: Pre-compute exit tiers based on entry:
   ```
   tier_1_target = entry_price * 1.10   # +10% — risk-off trim (sell 25%)
   tier_2_target = entry_price * 1.20   # +20% — scaling trim (sell 25%)
   tier_3_target = entry_price * 1.40   # +40% — runner trim (sell 25%)
   stop_loss = entry_price - (2 * ATR)  # initial hard stop
   ```
<!-- DEEP: 10+min -->
### Phase 3 (~20 min): Entry Execution

Bridge the gap between model prices and real fills. Slippage, commissions, and timing determine whether a theoretically profitable strategy actually makes money.

1. **Choose order type based on urgency and spread**:
   - Tight spreads (<0.1% of price) and normal urgency → limit order at mid or 1 tick favorable
   - Wide spreads (>0.5%) or high urgency → marketable limit (limit at ask for buys, bid for sells)
   - Size >1% of ADV → TWAP/VWAP algorithm to avoid moving the market

2. **Estimate slippage before submitting**:
   ```
   # Realistic slippage model (from live trading data)
   if market_cap > 100e9:     slippage_pct = 0.02  # mega-cap: 2 bps
   elif market_cap > 10e9:    slippage_pct = 0.05  # large-cap: 5 bps
   elif market_cap > 2e9:     slippage_pct = 0.15  # mid-cap: 15 bps
   else:                       slippage_pct = 0.50  # small-cap: 50 bps

   # Options slippage is worse — multiply by 3-5x
   option_slippage_pct = slippage_pct * 4.0
   # For OTM options, add another 2-3%
   if option_moneyness < 0.95:  # OTM
       option_slippage_pct += 2.0
   ```

3. **Commission-aware sizing**:
   - Equity: ~$0 (commission-free at most brokers), but SEC fees apply (~$8/million sold)
   - Options: $0.65/contract typical. 100 contracts = $65 round trip. On a $5,000 position, that is 1.3% drag.
   - If estimated commissions > 1% of expected profit, reduce size or skip the trade.

4. **Broker API execution flow** (Alpaca example):
   ```python
   import alpaca_trade_api as tradeapi

   api = tradeapi.REST(api_key, secret_key, base_url, api_version='v2')

   # Place bracket order: entry + stop-loss + take-profit in one request
   api.submit_order(
       symbol='AAPL',
       qty=shares,
       side='buy',
       type='limit',
       limit_price=entry_price,
       time_in_force='day',
       order_class='bracket',
       stop_loss={'stop_price': stop_loss_price},
       take_profit={'limit_price': tier_1_target}
   )

   # For options through Alpaca (if enabled):
   # api.submit_order(
   #     symbol='AAPL250117C00200000',  # OSI format
   #     qty=10,
   #     side='buy',
   #     type='limit',
   #     limit_price=2.50,
   #     time_in_force='day'
   # )
   ```

5. **Duplicate order guard**:
   ```python
   # Idempotency via client_order_id
   order_id = f"{signal['id']}_{datetime.utcnow().strftime('%Y%m%d')}"
   existing = api.get_order_by_client_order_id(order_id)
   if existing and existing.status not in ('canceled', 'rejected'):
       return existing  # already submitted, do not duplicate
   api.submit_order(..., client_order_id=order_id)
   ```
<!-- DEEP: 10+min -->
### Phase 4 (~15 min): Position Management

A live position is not passive — it requires active monitoring and pre-programmed responses to price movement, time decay, and signal degradation.

1. **Trailing stop engine**:
   ```python
   def update_trailing_stop(position: Position, current_price: float, atr: float) -> float:
       # 2x ATR trailing stop from highest high since entry
       new_stop = current_price - (2.0 * atr)
       position.trailing_stop = max(position.trailing_stop, new_stop)
       # Stop never moves down — only up for longs, down for shorts
       return position.trailing_stop
   ```

2. **Trim execution logic**:
   ```python
   def check_trims(position: Position, current_price: float) -> list[Order]:
       orders = []
       remaining = position.remaining_shares

       if current_price >= position.tier_1_target and not position.tier_1_executed:
           sell_qty = int(position.original_shares * 0.25)
           orders.append(Order(side='sell', qty=sell_qty, type='limit', price=current_price))
           position.tier_1_executed = True
           # Move stop to breakeven after Tier 1
           position.trailing_stop = position.entry_price

       if current_price >= position.tier_2_target and not position.tier_2_executed:
           sell_qty = int(position.original_shares * 0.25)
           orders.append(Order(side='sell', qty=sell_qty, type='limit', price=current_price))
           position.tier_2_executed = True

       if current_price >= position.tier_3_target and not position.tier_3_executed:
           sell_qty = int(position.original_shares * 0.25)
           orders.append(Order(side='sell', qty=sell_qty, type='limit', price=current_price))
           position.tier_3_executed = True

       return orders
   ```

3. **Time stop monitor**: If `(datetime.utcnow() - position.entry_time).days >= 5` and the position P&L is between -2% and +5%, the signal has not worked. Exit at market. UOA signals that do not move within 5 trading days almost never become big winners.

4. **Earnings blackout**: If earnings are within 48 hours and position has profit >10%, exit 50%. If flat or losing, exit 100%. The UOA signal was not an earnings play unless explicitly tagged as such.

5. **Signal decay tracker**: Monitor whether the original UOA signal conditions still hold. If the unusual activity was a large call buyer and those calls are now being sold (delta hedging unwound), the smart money has exited — you should too.
<!-- DEEP: 10+min -->
### Phase 5 (~15 min): Exit Execution & Risk Monitoring

Systematic exits prevent emotional decisions. Every exit is pre-planned — the only decision at exit time is whether the pre-planned condition has been met.

1. **Exit trigger hierarchy** (checked in order every 1 minute):
   ```
   1. Emergency stop: News/event invalidating thesis → Exit 100% market order
   2. Hard stop-loss: price <= stop_loss → Exit 100% market order
   3. Trailing stop: price <= trailing_stop → Exit 100% market order
   4. Time stop: days_held >= 5 AND pnl_pct < 5% → Exit 100% market order
   5. Trim targets: price >= tier_N_target → Sell tier_N quantity
   6. Signal invalidation: original UOA flow reversed → Exit 100%
   ```

2. **Portfolio risk dashboard** (real-time calculations):
   ```python
   def portfolio_risk_metrics(positions: list[Position], prices: dict) -> dict:
       nav = sum(p.market_value for p in positions) + cash
       returns = daily_return_series(positions)

       # Value at Risk (95%, 1-day)
       var_95 = np.percentile(returns, 5)

       # Conditional VaR (expected loss beyond VaR)
       cvar_95 = returns[returns <= var_95].mean()

       # Max drawdown
       cumulative = (1 + returns).cumprod()
       running_max = cumulative.expanding().max()
       drawdown = (cumulative - running_max) / running_max
       max_dd = drawdown.min()

       # Beta to SPY
       spy_returns = get_spy_returns()
       beta = cov(returns, spy_returns) / var(spy_returns)

       # Correlation matrix
       returns_df = pd.DataFrame({p.ticker: p.daily_returns for p in positions})
       corr_matrix = returns_df.corr()

       # Net delta exposure
       net_delta = sum(p.delta_exposure for p in positions)

       return {
           'nav': nav, 'var_95': var_95, 'cvar_95': cvar_95,
           'max_drawdown': max_dd, 'beta': beta,
           'corr_matrix': corr_matrix, 'net_delta': net_delta
       }
   ```

3. **Hard circuit breaker**: If account drawdown exceeds 20% from peak NAV:
   - Liquidate all positions at market
   - Cancel all open orders
   - Set trading mode = HALTED
   - Require manual review before resuming
   - This is non-negotiable. No strategy, no conviction, no "but the signal was strong" overrides the circuit breaker.

4. **Black swan hedge monitor**: When VIX < 15, purchase OTM SPY puts (5% OTM, 30-45 DTE) for 1-2% of portfolio NAV as tail risk insurance. Cheap when volatility is low — do not wait for the storm to buy flood insurance.
<!-- DEEP: 10+min -->
### Phase 6 (~25 min): Backtesting & Post-Trade Analysis

Validate strategies before risking capital. Learn from every trade — winners and losers.

1. **Vectorized backtest** (fast, for strategy exploration):
   ```python
   def vectorized_backtest(signals: pd.DataFrame, prices: pd.DataFrame, atr: pd.Series) -> pd.DataFrame:
       # signals columns: date, ticker, signal, entry_price, conviction
       results = []

       for _, signal in signals.iterrows():
           entry_idx = prices.index.get_loc(signal['date'])
           future_prices = prices.iloc[entry_idx:entry_idx + 20]  # next 20 days

           entry = signal['entry_price']
           stop = entry - (2 * atr.iloc[entry_idx])
           tier_1 = entry * 1.10
           tier_2 = entry * 1.20

           for i, price in enumerate(future_prices):
               if price <= stop:
                   results.append({'pnl_pct': (stop - entry) / entry, 'exit_reason': 'stop_loss', 'days_held': i})
                   break
               elif price >= tier_2 and i > 0:
                   results.append({'pnl_pct': (tier_2 - entry) / entry, 'exit_reason': 'tier_2', 'days_held': i})
                   break
           else:
               # Time stop after 20 days
               results.append({'pnl_pct': (future_prices.iloc[-1] - entry) / entry, 'exit_reason': 'time_stop', 'days_held': 20})

       return pd.DataFrame(results)
   ```

2. **Walk-forward optimization** (the only backtest that matters):
   - Split data: 3 years in-sample → optimize parameters → 1 year out-of-sample → test
   - Slide forward 1 year, repeat. Five windows minimum.
   - If strategy parameters are unstable across windows (Sharpe swings >50%), the strategy is overfit.
   - Only trade strategies where out-of-sample Sharpe is within 20% of in-sample Sharpe.

3. **Backtest reality checks** (apply these or your results are fiction):
   - **Survivorship bias**: Backtest on point-in-time universes. Companies get acquired and delisted — if your backtest only uses today's tickers, it has survivorship bias.
   - **Look-ahead bias**: Do not use split-adjusted prices before the split date. Do not use earnings data before the announcement time.
   - **Slippage model**: Deduct 0.5% per trade for mid-cap equity, 2-3% for OTM options.
   - **Commission drag**: $0.65/contract × (buy + sell) = $1.30 round trip per contract.
   - **Regime test**: Run backtest separately on bull (2009-2020), bear (2008, 2020 Q1, 2022), and sideways (2015-2016) markets. A strategy that only works in bull markets will blow up.

4. **Post-trade P&L attribution**:
   ```python
   def attribution_report(closed_trades: list[Trade]) -> dict:
       df = pd.DataFrame([t.to_dict() for t in closed_trades])

       return {
           'total_trades': len(df),
           'win_rate': (df['pnl'] > 0).mean(),
           'avg_win': df[df['pnl'] > 0]['pnl_pct'].mean(),
           'avg_loss': df[df['pnl'] < 0]['pnl_pct'].mean(),
           'profit_factor': df[df['pnl'] > 0]['pnl'].sum() / abs(df[df['pnl'] < 0]['pnl'].sum()),
           'largest_winner': df['pnl_pct'].max(),
           'largest_loser': df['pnl_pct'].min(),
           'avg_hold_days': df['days_held'].mean(),
           'exit_by_reason': df.groupby('exit_reason')['pnl_pct'].agg(['count', 'mean']),
           'sector_pnl': df.groupby('sector')['pnl'].sum(),
           'signal_conviction_decay': df.groupby('conviction_bucket')['pnl_pct'].mean()
       }
   ```
## Best Practices
<!-- STANDARD: 3min -- rules extracted from production trading experience -->

- **Paper trade for 30 days minimum before live capital.** The gap between backtest and reality is always larger than you think. Paper trade with realistic fills (not mid-price) and actual slippage assumptions. If you cannot be profitable on paper, you will not be profitable with real money.
- **Half-Kelly is full Kelly in practice.** Full Kelly assumes you know your edge exactly — you do not. Half-Kelly preserves 75% of the growth rate with 50% of the drawdown risk. When in doubt, quarter-Kelly.
- **Size positions by risk, not conviction.** "High conviction" signals do not deserve larger positions. They deserve the same 1-2% risk per trade. Conviction is an emotion; position sizing is math. Let the math win.
- **Walk-forward validation is the only backtest that matters.** A single in-sample backtest with optimized parameters is curve-fitting, not strategy development. Minimum five walk-forward windows with stable parameters across windows before going live.
- **Monitor signal decay in real time.** UOA signals have a half-life measured in hours to days. If your signal-to-execution pipeline takes more than 5 minutes, you are trading stale information. Benchmark: time from signal generation to order submission should be under 60 seconds.
- **Treat commissions as a strategy input, not an afterthought.** On a $3,000 options position with $65 round-trip commissions, you need +2.2% just to break even. Factor commissions into position sizing — $2,000 minimum trade size for equity, $1,000 minimum for single-leg options.
- **Log everything — every fill, every rejection, every reconnect.** Trading bugs are discovered in logs, not in P&L. Structured JSON logs with correlation IDs from signal → validation → order → fill → position update → exit. If you cannot trace a losing trade end-to-end, you cannot fix what broke.
- **Run a "paper clone" of live strategies.** Mirror your live strategy in a paper account with the same signals, same sizing, same timing. Divergence between paper and live P&L reveals execution problems — slippage you did not model, fills you are not getting, latency you did not measure.
- **Never override the circuit breaker.** If max drawdown is 20% and you are at 19.5%, you are already past the point where you should have reduced size. The circuit breaker exists because you will be wrong about when to stop. Trust the breaker — it is smarter than you are during a losing streak.
- **Correlation matrix is a daily check, not an annual review.** UOA signals cluster. A massive call-buying day in tech can give you 10 "independent" signals that are all the same bet. Recompute sector and factor correlations daily. Max 30% in any correlated bucket, no exceptions.

## Anti-Patterns
<!-- STANDARD: 3min -- patterns that predictably fail -->

| Anti-Pattern | Why It Fails | Correct Approach |
|---|---|---|
| **Skipping the paper clone because the backtest was perfect** | Backtests assume idealized fills; real-world execution has slippage, latency, and partial fills that compound. Without a parallel paper account, you cannot distinguish strategy failure from execution failure. | Run a paper clone mirroring live signals identically. Monitor P&L divergence daily — >2% gap means the execution model is broken, not the strategy. Investigate before adding more capital. |
| **Doubling Kelly on high-conviction trades** | Conviction is emotional, not mathematical. Doubling Kelly inflates drawdown risk exponentially — a 3-sigma event causing 15% drawdown at half-Kelly becomes 45% drawdown at full Kelly. | Cap all positions at half-Kelly maximum. Size by risk-per-trade (1-2% of NAV), not by conviction level. The sizing formula is deterministic — encode it, test it, lock it. No manual overrides. |
| **Relaxing the stop-loss because the thesis is still intact** | Stops exist precisely because the thesis is wrong and you do not know it yet. Widening stops during a losing trade converts a small controlled loss into a large unplanned drawdown. | Set bracket orders at entry with fixed stop-loss (2x ATR). The stop never moves against the position. If the thesis is truly intact, re-enter at a better price after the stop triggers — never hold through it. |
| **Running the backtest once and calling it validated** | Single-period backtests optimize for noise, not signal. Parameters that work in a 2020-2021 bull market collapse in a 2022 rate-hiking cycle. One backtest = one data point, not proof. | Walk-forward validation with minimum 5 windows: train on 3 years, test on 6 months out-of-sample. Reject the strategy if out-of-sample Sharpe varies >50% across windows or any window produces negative returns. |
| **Treating all STRONG BUY signals from quant as equal-sized trades** | A $5M call sweep on a stock with $500K daily option volume is fundamentally different from the same sweep on a $200B mega-cap. Signal size relative to float and liquidity matters more than absolute premium. | Normalize signals by ADV and float. Filter: reject signals where premium < 2% of daily dollar volume. Size positions proportional to liquidity — a $5M signal on an illiquid name gets a smaller position than a $2M signal on a liquid name. |
| **Deploying live without testing broker API failure modes** | Broker APIs fail in production — timeouts, rate limits, partial fills, rejected orders. A rejected bracket order means the stop-loss never activates. A retried order can double-fill. Silent failures destroy accounts. | Test every failure mode before going live: API timeout, rate-limit response, duplicate submission rejection, partial fill handling. Verify the system logs every failure explicitly and never silences an error from the broker API. |
| **Ignoring correlation until the drawdown forces attention** | UOA signals cluster by sector and factor. Five "independent" tech call sweeps on the same day are one leveraged bet on tech. Daily correlation monitoring catches concentration before it becomes a blow-up — checking monthly means the damage is already done. | Compute sector and factor correlation matrix daily. Hard cap: 30% per correlated bucket, 50% per factor. If correlation spikes above threshold, reduce the newest positions first — they have the least edge decay. |
| **Assuming trailing stops protect profits without monitoring time-of-day effects** | In the first 30 minutes of market open, ATR is inflated by gap fills and opening auctions. A 2x ATR trailing stop set at 9:35 AM is 40% wider than the same stop at 10:30 AM, causing premature stop-outs. | Delay trailing stop activation for the first 30 minutes of trading. Use 15-minute ATR (not 1-minute) for stop calibration. Backtest stop placement by time-of-day to verify performance across the trading session. |

## Error Decoder
<!-- DEEP: 10+min -->

| Symptom | Root Cause | Fix | Lesson |
|---------|------------|-----|--------|
| Latency arbitrage strategy destroyed by colocated competitor's faster feed | Assumed 5ms advantage was sufficient; competitor used FPGA and microwave links for 100-microsecond advantage | Model competitor reaction latency as a probability distribution not a fixed value; add 50% margin to assumed latency advantage; optimize for worst-case not average-case latency | In latency arbitrage you aren't competing against the market — you're competing against whoever is colocated in the same data center with better hardware |
| Backtest showed Sharpe 2.5 but went bust live | Walk-forward validation never performed; backtest overfit to a single bull-market regime; parameters had no stability across sub-periods | Run walk-forward optimization: 3-year train windows sliding every 6 months, minimum 5 windows; reject strategy if out-of-sample Sharpe varies >50% across windows | A backtest that explains the past perfectly will fail the future predictably — complexity is the enemy of robustness |
| Live trading executed on stale data from previous market close | Market data feed lost connection; signal validation used last cached prices; system silently traded on 4-hour-old quotes | Implement data freshness gate: reject any signal older than 60 seconds during market hours; add heartbeat monitoring on data feed with automated halt if feed drops | A trading system without data staleness detection is a gambling system — validate every data point before trading on it |
| Risk limit breached by correlated positions across five different accounts | Risk limits enforced per-account but correlation computed across accounts; five accounts each at 90% capacity in the same sector | Implement cross-account correlation monitoring at the portfolio level; aggregate position exposure before checking limits; use a central risk engine that sees all accounts | Per-account risk limits that ignore cross-account correlation are theater — a fund can blow up one account at a time across five accounts with the same correlated bet |
| VWAP execution algorithm leaked 50bps of alpha vs. paper record | Backtest assumed perfect splits across the volume curve; real execution had order book imbalance and queue position effects not modeled | Model execution with expected queue position distribution and order book resilience; use implementation shortfall for sizing not VWAP for timing | Execution models that assume perfect market conditions will systematically overestimate fill quality — test with actual market impact not theoretical curves |

## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass before live trading. -->

- [ ] **[P1]** Signal validation pipeline passes all gates: liquidity >500K ADV, OI >1,000 contracts, no binary events within 5 days
- [ ] **[P2]** Position sizing model implemented: max 2% risk per trade, half-Kelly cap at 5% NAV, max 10% single position
- [ ] **[P3]** Bracket orders used: every entry order includes simultaneous stop-loss and take-profit (OCO/OCO)
- [ ] **[P4]** Duplicate order guard active: idempotency keys prevent double-submission on broker API retries
- [ ] **[P5]** Trailing stop engine running: 2x ATR, stop never moves against position, 30-min opening whipsaw delay
- [ ] **[P6]** Trim execution logic tested: Tier 1 (25% at +10%), Tier 2 (25% at +20%), Tier 3 (25% at +40%/RSI>70)
- [ ] **[P7]** Time stop enforced: exit 100% if position flat/negative after 5 trading days
- [ ] **[P8]** Circuit breaker at -20% account drawdown: liquidate all, cancel orders, halt trading, require manual review
- [ ] **[P9]** Correlation matrix computed daily: max 30% sector exposure, max 50% factor exposure
- [ ] **[P10]** Broker API reconnection logic with exponential backoff: 1s, 2s, 4s, 8s, 16s, max 5 retries before alerting
- [ ] **[P11]** Paper clone running in parallel with live: divergence monitoring triggers alert at >2% P&L gap
- [ ] **[P12]** Structured logging with correlation IDs: signal_id → order_id → fill_id → position_id, end-to-end traceable
- [ ] **[P13]** Walk-forward backtest completed: minimum 5 windows, out-of-sample Sharpe within 20% of in-sample
- [ ] **[P14]** Slippage model calibrated with live fill data: compare fill prices to mid-price at order time, track running average
- [ ] **[P15]** Earnings blackout window active: reduce 50% if earnings within 48 hours, exit 100% if flat/losing
- [ ] **[P16]** Black swan hedge active when VIX < 15: 1-2% NAV in OTM SPY puts, 30-45 DTE, 5% OTM
## Cross-Skill Coordination
<!-- QUICK: 30s -- real chains with upstream and downstream skills -->

### Consumes From

| Skill | What It Provides | How This Skill Uses It |
|-------|-----------------|----------------------|
| **quantitative-analyst** | UOA signal JSON: ticker, direction, conviction, expected timeframe, flow metrics (premium, volume, OI change, IV percentile) | Phase 1: Parses signal envelope, validates freshness. Entry decisions are downstream of quant signal quality — garbage signals produce garbage trades regardless of execution quality. Feed signal metadata back to quant-analyst for model improvement. |
| **market-data-engineer** | Clean options flow data, adjusted chains, corporate actions, real-time streaming via Kafka/Redpanda | Phase 1 Pre-flight: Validates that market data pipeline is healthy before consuming signals. **Decision gate:** Is data freshness < 60s? → proceed. Are corporate actions current? → proceed. Otherwise, halt and invoke `market-data-engineer`. **Artifact:** pipeline health check report. |
| **system-architect** | Trading system topology: event bus design, database schema for time-series data, API gateway patterns, failover architecture | Phase 3-5: Execution engine design — how signals flow from quant pipeline → order management → broker API. System-architect defines the reliability patterns (circuit breakers, retry policies, idempotency) that prevent duplicate orders and missed exits. |
| **backend-developer** | Order management system (OMS) API, idempotent order submission endpoints, position tracking service | Phase 3: Consumes order execution specs. **Decision gate:** Are idempotency keys implemented? → proceed. Is OMS circuit breaker tested? → proceed. **Artifact:** OMS integration test report. |
| **observability-engineer** | Prometheus metrics definitions, Grafana dashboard templates, alerting rule thresholds | Phase 5-6: Consumes trading-specific metric requirements. **Decision gate:** Are slippage alerts firing at >50 bps? → calibrate. **Artifact:** trading dashboard JSON + alert config YAML. |

### Feeds Into

| Skill | What It Produces | Coordination |
|-------|-----------------|-------------|
| **backend-developer** | Order management system (OMS), position tracker, broker API client, signal validation service | Phase 3: Provide order execution spec — bracket order logic, idempotency keys, broker-specific API calls for Alpaca/IB/Schwab. Backend-dev implements the execution engine; algorithmic-trader defines the trading logic (entry conditions, stop calculations, trim targets). |
| **frontend-developer** | Real-time P&L dashboard, position monitor, risk metrics UI, order entry interface | Phase 5: Provide dashboard requirements — VaR, CVaR, beta, correlation heatmap, drawdown chart. Frontend-dev builds the visualization; algorithmic-trader defines what metrics matter and at what refresh rate (1-second for positions, 1-minute for risk). |
| **observability-engineer** | Prometheus metrics, Grafana dashboards, alerting rules, log aggregation pipeline | Phase 5-6: Define trading-specific metrics: fill slippage (bps), signal-to-execution latency (ms), order rejection rate, position count, margin utilization. Observability-engineer builds the dashboards; algorithmic-trader defines alert thresholds (e.g., slippage >50 bps triggers investigation). |

### Alternatives

| Skill | When to Use Instead |
|-------|-------------------|
| **ml-ai-engineer** | When signals are ML-generated (LSTM price predictions, NLP on earnings calls, GNN on options flow networks) rather than rule-based UOA patterns. ML-engineer builds the signal model; algorithmic-trader still handles execution, but the entry logic must accommodate probabilistic (not binary) signals with confidence intervals. |

### Coordination Table

| Trigger | Notify | Why |
|---------|--------|-----|
| Signal pipeline delivers UOA alert | algorithmic-trader + backend-developer | Validate signal → size position → submit order within 60 seconds |
| Order rejected by broker API | backend-developer + algorithmic-trader | Check buying power, position limits, symbol tradability; retry or skip |
| Circuit breaker triggered (-20% drawdown) | algorithmic-trader + observability-engineer + security-engineer | Halt trading, investigate cause, review strategy before resuming |
| Slippage exceeds 2x model estimate | observability-engineer + algorithmic-trader | Recalibrate slippage model; may indicate strategy decay or market regime change |
| Portfolio correlation spikes above 0.7 | algorithmic-trader + quantitative-analyst | Reduce correlated positions; review whether UOA signals are truly independent |

### Integration Chain

```bash
# UOA signal → Strategy execution → Dashboard update
/quantitative-analyst && /algorithmic-trader && /frontend-developer

# Strategy design → Backend implementation → Production monitoring
/system-architect && /algorithmic-trader && /backend-developer && /observability-engineer

# ML signal generation → Trade execution with confidence intervals
/ml-ai-engineer && /algorithmic-trader
```

## Proactive Triggers
<!-- QUICK: 30s -- when to proactively notify stakeholders -->

| Trigger | Notify | Why |
|---------|--------|-----|
| Portfolio drawdown exceeds 10% intraday | algorithmic-trader + observability-engineer | Approaching circuit breaker territory; review open positions for correlated losses, prepare for potential partial liquidation before -20% breaker triggers |
| Signal-to-execution latency exceeds 60 seconds for 3+ consecutive signals | backend-developer + market-data-engineer | Stale signals being traded — pipeline bottleneck or data feed degradation; halt new entries until latency restored below threshold |
| Slippage exceeds 1.5x model estimate for 3 consecutive fills | observability-engineer + backend-developer | Execution quality degrading — possible market impact, liquidity drain, or broker routing change; recalibrate slippage model before next session |
| Paper clone P&L diverges >2% from live P&L over trailing 5 days | algorithmic-trader + backend-developer | Execution fidelity problem — live fills not matching modeled fills; investigate broker routing, market impact, or latency not captured in backtest |
| Correlation matrix shows >50% in single factor bucket | algorithmic-trader + quantitative-analyst | Concentration risk — multiple "independent" signals are the same directional bet; reduce newest correlated positions immediately |
| Broker API returns 3+ consecutive order rejections within 5 minutes | backend-developer + algorithmic-trader | Possible buying power issue, symbol restriction, or API authentication failure; halt all trading until root cause identified and resolved |
| Strategy win rate drops below 40% on 30-day rolling window | quantitative-analyst + algorithmic-trader | Strategy decay or market regime change; reduce position sizes by 50% until backtest confirms parameters are still valid in current regime |
| VIX spikes >30 while holding net-long Vega positions | algorithmic-trader + observability-engineer | Volatility regime change — Vega exposure may dominate Delta P&L; review all position Greeks, hedge ratios, and correlation assumptions immediately |

## What Good Looks Like

A production algorithmic trading system that executes this skill correctly has these observable characteristics:

- **Signal-to-execution latency under 60 seconds.** From the moment the quantitative-analyst pipeline emits a signal to the moment a bracket order is resting at the broker. Stale signals are worse than no signals — a UOA alert from 30 minutes ago is already priced in.

- **Every order is a bracket order.** No naked market orders. Every entry comes with a stop-loss and at least one take-profit target attached at submission time. The broker holds the OCO (one-cancels-other) bracket — if the connection drops, protection is still live at the exchange.

- **Position sizing is deterministic, not emotional.** The sizing formula produces the same share count for the same signal and account state every time. No "I have a good feeling about this one" adjustments. The Kelly/fixed-fractional formula is codified and unit-tested — regression tests verify that a $100K account with signal X always produces Y shares.

- **Drawdown never surprises you.** The max drawdown monitor updates in real time. At -10% from peak, it automatically reduces new position sizes by 50%. At -15%, it sends an alert. At -20%, it liquidates everything. These thresholds are hardcoded and cannot be overridden without a code change and deployment — no "override breaker" button exists.

- **You can trace any P&L dollar to its source signal.** Structured logs with correlation IDs mean that when a trade loses $500, you can query: which quant-analyst signal generated it, what was the conviction score, what entry strategy was used, what was the fill slippage, and which exit rule triggered. Every losing trade is a learning opportunity because every trade is fully instrumented.

- **The paper clone tracks within 2% of live.** If the paper account (same signals, same sizing, same timing, but fills at mid-price) diverges from live P&L by more than 2% over any rolling 20-trade window, an alert fires. Divergence means your slippage model is wrong or you are getting worse fills than expected — fix execution, not strategy.

- **No single sector or factor can destroy the account.** The correlation matrix runs daily before market open. If any sector exceeds 30% of NAV, the smallest position in that sector is reduced or closed. Diversification is enforced by code, not discipline — discipline fails under stress; code does not.

## Scale Depth
<!-- QUICK: 30s -- find your team size column -->

### Solo
- **What changes**: Single strategy, manual execution via broker UI. Learn market mechanics, prove a thesis. Execute trades manually; no automation; spreadsheet-based tracking.
- **What to skip**: Real-time risk monitoring (end-of-day is fine). Multi-strategy correlation. Automated execution. Colocation or low-latency infrastructure. Regulatory compliance frameworks.
- **Coordination**: Self-contained. Track P&L in a spreadsheet. Review weekly.
- **Cost**: Free — Alpaca paper trading API, Yahoo Finance data, Python.

### Small Team
- **What changes**: Automated trading bot, backtesting framework, paper trading. Build reliable automation, validate strategies. Code executes trades; backtesting catches bad strategies before real money.
- **What to skip**: Multi-strategy portfolio management. Real-time correlation monitoring. Full risk management system. Institutional-grade execution.
- **Coordination**: Weekly strategy review with trader. Backtest results shared before paper trading. Developer handles execution reliability.
- **Cost**: $500-$2K/month (broker API, cloud VM, basic market data).

### Medium Team
- **What changes**: Multi-strategy portfolio, risk management system, real-time monitoring. Diversify alpha, manage drawdowns. Portfolio-level risk controls; strategy correlation monitored; position sizing automated.
- **What to skip**: Market making. Colocation and FPGA execution. SEC/FINRA institutional compliance. Internal quantitative research platform.
- **Coordination**: Daily risk meeting. Bi-weekly strategy review. Integration with execution/OMS. Compliance oversight introduced.
- **Cost**: $5K-$30K/month (risk monitoring platform, multiple data feeds, cloud compute).

### Enterprise
- **What changes**: Market making, institutional execution, regulatory compliance. Scale AUM, minimize market impact. Colocation, smart order routing, SEC/FINRA compliance, institutional counterparties.
- **What's full production**: 24/7 operations team. Dedicated risk management team. Model governance framework. Annual external audits.
- **Coordination**: Daily risk meeting. Weekly strategy performance review. Monthly compliance review. Quarterly model audit.
- **Cost**: $50K-$500K+/month (colocation, data, compute, team, compliance).

### Transition Triggers

| From \u2192 To | Trigger | What to Change |
|-----------|---------|----------------|
| Solo \u2192 Small | Automated strategy profitable for 3+ months, AUM >$100K | Move from manual to automated execution; add basic backtesting; formalize entry/exit rules |
| Small \u2192 Medium | Multi-strategy, AUM >$2M, >10 signals/day | Add portfolio-level risk controls; implement real-time monitoring; hire dedicated operations |
| Medium \u2192 Enterprise | Institutional counterparties, regulatory requirements, AUM >$50M | Colocate; implement smart order routing; build compliance framework; hire risk and compliance team |

## References
<!-- QUICK: 30s -- links to deeper reading -->

- [Alpaca Trading API Docs](https://docs.alpaca.markets/) — REST API for equity and options trading, bracket orders, streaming data
- [Interactive Brokers API](https://www.interactivebrokers.com/api/) — TWS API and Client Portal API for institutional-grade execution
- [Schwab Trader API](https://developer.schwab.com/) — Retail trader API (TD Ameritrade successor) for equity and options
- [QuantConnect](https://www.quantconnect.com/) — Cloud-based algorithmic trading platform with LEAN engine, multi-asset backtesting
- [Backtrader](https://www.backtrader.com/) — Python event-driven backtesting framework with live trading support
- [Zipline-Reloaded](https://github.com/stefan-jansen/zipline-reloaded) — Maintained fork of Quantopian's Zipline backtesting engine
- [Kelly Criterion — Edward Thorp](https://www.eecs.harvard.edu/cs286r/courses/fall12/papers/Thorpe_KellyCriterion2007.pdf) — The mathematics of optimal bet sizing
- [Expected Shortfall (CVaR)](https://en.wikipedia.org/wiki/Expected_shortfall) — Basel III standard for tail risk measurement
- [Advances in Financial Machine Learning — Marcos Lopez de Prado](https://www.wiley.com/en-us/Advances+in+Financial+Machine+Learning-p-9781119482086) — Walk-forward validation, triple-barrier labeling, meta-labeling
- [Option Volatility and Pricing — Sheldon Natenberg](https://www.amazon.com/Option-Volatility-Pricing-Strategies-Techniques/dp/0071818774) — Options market making, volatility surface, risk management
- [Trading and Exchanges — Larry Harris](https://www.amazon.com/Trading-Exchanges-Market-Microstructure-Practitioners/dp/0195144708) — Market microstructure, order types, liquidity, transaction costs
- Internal: [references/backtest-pitfalls.md](references/) — Common backtesting mistakes and how to avoid them
- Internal: [references/broker-integration-guide.md](references/) — Step-by-step broker API setup with code examples

<!-- DEEP: Full broker-specific execution playbooks in references/ -->
<!-- DEEP: Walk-forward optimization framework with hyperparameter stability tests in references/ -->
<!-- EXPERT: Custom order execution algorithms (implementation shortfall, adaptive VWAP) in references/ -->
<!-- EXPERT: Options-specific risk: gamma scalping, vega hedging, pin risk management in references/ -->
