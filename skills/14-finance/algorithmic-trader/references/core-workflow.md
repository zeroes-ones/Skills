# Core Workflow — Full Implementation

<!-- QUICK: 30s -- scan phase titles to understand the process -->

<!-- DEEP: 10+min -->
### Phase 1 (~10 min): Signal Reception & Validation

Consume output from the quantitative-analyst pipeline. Every signal must be validated before any capital is committed.

1. **Parse signal envelope**: Extract ticker, direction (CALL=long equity, PUT=short equity), timestamp, conviction score (0.0-1.0), and expected catalyst timeframe from the quantitative-analyst JSON payload.
2. **Liquidity gate**: Check that the underlying trades >500K shares/day and option open interest on the target strike is >1,000 contracts. Illiquid underlyings amplify slippage beyond model assumptions — reject signals on names with average daily volume under 100K.
3. **Correlation gate**: Compare the signal ticker against existing positions. If adding this position would push sector exposure above 30% of portfolio, reduce size or skip. UOA signals cluster — 5 signals in semiconductors is one bet, not five.
4. **News gate**: Scan for pending earnings (within 5 days), FDA decisions, merger votes, or regulatory rulings. Binary event risk trumps any UOA signal. Reduce position size by 50% or skip if an unmodelable event is imminent.
5. **Macro event gate**: Check economic calendar for high-impact releases within 24 hours — FOMC rate decisions, CPI, PPI, NFP, GDP advance, PMI flash, jobless claims. During macro events, intraday volatility expands 2-4x normal and stop-losses get hunted en masse. If a red-flag event (FOMC, CPI, NFP) is within 24 hours: reduce position size by 50% AND widen stop-loss by 1.5x. If within 2 hours: skip the trade entirely — the signal edge is noise against macro volatility.
6. **Signal freshness check**: If the signal timestamp is >2 hours old during market hours (or >1 day for overnight signals), check whether the edge has decayed. Compare current price vs. signal price — if the move already happened, the trade is over.

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

    hours_to_macro = hours_to_next_macro_event()
    if hours_to_macro <= 2 and is_red_flag_event():
        return SignalDecision.REJECT  # macro event imminent, edge is noise
    elif hours_to_macro <= 24 and is_high_impact_event():
        signal['adjusted_size'] *= 0.5
        signal['stop_multiplier'] = 1.5  # widen stops for macro vol

    signal_age_minutes = (datetime.utcnow() - signal['timestamp']).total_seconds() / 60
    if signal_age_minutes > 120:
        price_change = (market_data.last - signal['signal_price']) / signal['signal_price']
        if abs(price_change) > 0.02:  # >2% move already happened
            return SignalDecision.EXPIRED

    return SignalDecision.ACCEPT

```

Complete when: All 6 gates return PASS or adjusted parameters: identity verified (symbol/strategy/confidence match), entry within 1.5 ATR of VWAP, liquidity confirmed (cap >$2B, spread <0.15%), no binary earnings within 5 days (or size halved), no red-flag macro event within 2 hours (or rejected), and signal freshness validated (age <2 hours or move precheck passed). Any rejected signal has a documented rejection reason.

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

5. **Set liquidity-grab-aware stop-loss**: Market makers actively hunt obvious stop levels — 2x ATR from entry is the most common, most hunted level. The stop must survive liquidity sweeps, not just reflect volatility.

   ```python
   def compute_stop_loss(
       entry_price: float,
       atr: float,
       swing_low: float,           # nearest swing low below entry
       round_number_step: float,   # 0.50 for stocks > $20, else 0.10
       vix: float,                 # current VIX
       vwap_band_low: float,       # VWAP - 2σ (lower band)
       macro_stop_mult: float = 1.0  # from macro gate, 1.5x during CPI/NFP/FOMC
   ) -> tuple[float, dict]:
       # --- LAYER 1: Regime-adjusted ATR multiplier ---
       if vix > 30:
           atr_mult = 2.5          # wide during volatility spikes
       elif vix > 20:
           atr_mult = 2.2
       else:
           atr_mult = 2.0

       atr_mult *= macro_stop_mult  # widen during macro events

       raw_stop = entry_price - (atr_mult * atr)

       # --- LAYER 2: Swing-low buffer ---
       # Never place stop AT a swing low — market makers push through
       # swing lows knowing stops cluster there. Go BELOW the swing low.
       if (swing_low - raw_stop) < (0.3 * atr):
           raw_stop = swing_low - (0.3 * atr)

       # --- LAYER 3: Round-number avoidance ---
       # Stops cluster at round numbers ($X.00, $X.50). Use asymmetric offset.
       nearest_round = round(raw_stop / round_number_step) * round_number_step
       if abs(raw_stop - nearest_round) < (round_number_step * 0.3):
           raw_stop = nearest_round - (round_number_step * 0.378)

       # --- LAYER 4: VWAP band floor ---
       # Stops within normal noise range get swept. Push below VWAP band.
       if raw_stop > vwap_band_low:
           raw_stop = vwap_band_low - (0.1 * atr)

       # --- LAYER 5: Stop-distance safety check ---
       stop_atr_distance = (entry_price - raw_stop) / atr
       warnings = []
       if stop_atr_distance < 1.5:
           warnings.append('STOP_TOO_TIGHT: <1.5x ATR — high grab probability')
       if abs(raw_stop % round_number_step) < 0.02:
           warnings.append('ROUND_NUMBER: stop at obvious level')

       # --- LAYER 6: Audit trail ---
       audit = {
           'atr_multiplier': atr_mult,
           'swing_low': swing_low,
           'final_stop': round(raw_stop, 2),
           'stop_pct': round((entry_price - raw_stop) / entry_price * 100, 2),
           'stop_atr_distance': round(stop_atr_distance, 2),
           'warnings': warnings
       }

       return raw_stop, audit
   ```

   **Layer rationale**: L1 adjusts for market regime (wide during fear), L2 avoids the #1 source of false stop-outs (swing low sweeps), L3 camouflages from order-book clustering, L4 ensures stops aren't in normal noise range, L5 catches configuration errors, L6 creates an audit trail for post-trade review.

6. **Size the trim targets**: Pre-compute exit tiers based on entry:

   ```
   tier_1_target = entry_price * 1.10   # +10% — risk-off trim (sell 25%)
   tier_2_target = entry_price * 1.20   # +20% — scaling trim (sell 25%)
   tier_3_target = entry_price * 1.40   # +40% — runner trim (sell 25%)
   initial_stop_loss, stop_audit = compute_stop_loss(
       entry_price, atr, swing_low, round_number_step, vix,
       vwap_band_low, macro_stop_mult
   )
   ```

Complete when: Share quantity calculated from selected sizing method (Kelly/fixed-fractional/vol-adjusted). All portfolio constraints applied (max position 10%, sector 30%, gross leverage 2.0x). Trim targets T1/T2/T3 pre-computed. Stop-loss computed through all 6 liquidity-grab layers (regime multiplier, swing-low buffer, round-number avoidance, VWAP floor, safety check, audit trail). Stop audit dict logged with no STOP_TOO_TIGHT warnings.

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

Complete when: Order type selected based on spread and urgency. Slippage estimate computed. Commission drag verified <1% of expected profit. Broker API order submitted with bracket (stop-loss + take-profit). Idempotency key (client_order_id) registered. Duplicate order guard confirmed — no double-submission.

<!-- DEEP: 10+min -->
### Phase 4 (~15 min): Position Management

A live position is not passive — it requires active monitoring and pre-programmed responses to price movement, time decay, and signal degradation.

1. **Trailing stop engine with grab protection**:

   ```python
   def update_trailing_stop(
       position: Position,
       current_price: float,
       atr: float,
       vix: float,
       bars_1m: list[Bar]  # last 20 1-minute bars for volume context
   ) -> float:
       # Regime-adjusted ATR multiplier (same as initial stop logic)
       if vix > 30:
           atr_mult = 2.5
       elif vix > 20:
           atr_mult = 2.2
       else:
           atr_mult = 2.0

       new_stop = current_price - (atr_mult * atr)

       # --- GRAB GUARD: Don't adjust stop on a wick ---
       # If the current candle is a wick (low << close), the current_price
       # may be a temporary sweep — don't ratchet the stop up from a wick low
       if len(bars_1m) >= 1:
           last_bar = bars_1m[-1]
           body_low = min(last_bar.open, last_bar.close)
           wick_ratio = (body_low - last_bar.low) / atr if atr > 0 else 0
           if wick_ratio > 0.5:  # >0.5 ATR wick — this is a grab, not a move
               # Use the body low instead of the wick low
               new_stop = body_low - (atr_mult * atr)

       # Stop only moves up for longs (down for shorts). Never reverse.
       position.trailing_stop = max(position.trailing_stop, new_stop)
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

Complete when: Trailing stop engine is active with VIX-adjusted multiplier and wick-filter guard, updating every 30 seconds. Trim execution logic is armed (T1/T2/T3 targets monitored). Time stop monitor is tracking days-held. Earnings blackout rules are active (48-hour pre-earnings check). Signal decay tracker is polling original UOA conditions. Liquidity grab detector is armed for every stop-trigger candle.

<!-- DEEP: 10+min -->
### Phase 5 (~15 min): Exit Execution & Risk Monitoring

Systematic exits prevent emotional decisions. Every exit is pre-planned — the only decision at exit time is whether the pre-planned condition has been met.

1. **Exit trigger hierarchy** (checked in order every 30 seconds):

   ```
   1. Emergency stop: News/event invalidating thesis → Exit 100% market order
   2. Hard stop-loss: price <= stop_loss → Run grab-detector BEFORE exiting
   3. Trailing stop: price <= trailing_stop → Run grab-detector BEFORE exiting
   4. Time stop: days_held >= 5 AND pnl_pct < 5% → Exit 100% market order
   5. Trim targets: price >= tier_N_target → Sell tier_N quantity
   6. Signal invalidation: original UOA flow reversed → Exit 100%
   ```

2. **Liquidity grab detector** — runs BEFORE executing a stop-loss exit. A stop trigger is NOT automatically an exit. The detector applies 5 confirmation layers to distinguish a real breakdown from a liquidity sweep:

   ```python
   def is_liquidity_grab(
       trigger_price: float,      # the stop level that was breached
       stop_type: str,            # 'hard_stop' or 'trailing_stop'
       bars_1m: list[Bar],        # last 30 1-minute bars
       bars_5m: list[Bar],        # last 12 5-minute bars
       avg_volume_20d: float,     # 20-day average volume
       premarket: bool = False,
       postmarket: bool = False,
       seconds_since_open: int = 0
   ) -> tuple[bool, str, str]:
       """
       Returns (is_grab, action, reason)
       action: 'EXIT' | 'HOLD' | 'WIDEN_AND_HOLD'
       """

       if len(bars_1m) < 5:
           return (False, 'EXIT', 'insufficient data to evaluate')

       last_bar = bars_1m[-1]
       prior_bars = bars_1m[-5:-1]  # 4 prior bars for context
       bar_low = last_bar.low
       bar_close = last_bar.close
       bar_volume = last_bar.volume if hasattr(last_bar, 'volume') else avg_volume_20d
       bar_body_low = min(last_bar.open, last_bar.close)

       # --- CHECK 1: Wick vs. body violation ---
       # If the low is a wick (low << close) but the body is ABOVE the stop,
       # this is a classic liquidity grab — a momentary sweep that reversed.
       # A real breakdown closes through the stop, not just ticks through it.
       if bar_body_low > trigger_price and bar_low <= trigger_price:
           wick_depth = (trigger_price - bar_low) / (bar_body_low - bar_low) if bar_body_low != bar_low else 0
           if wick_depth < 0.5:  # stop was only wick-violated, not body-violated
               return (True, 'HOLD', f'wick-only violation: body={bar_body_low:.2f} > stop={trigger_price:.2f} (wick depth {wick_depth:.1%})')

       # --- CHECK 2: Close-below confirmation ---
       # Even if the body violated the stop, require the bar to CLOSE below stop.
       # Intra-bar spikes that reverse before close are false signals.
       if bar_close > trigger_price:
           # Bar went through stop but closed above it — recovery already happened
           avg_body = sum(abs(b.open - b.close) for b in prior_bars) / max(len(prior_bars), 1)
           if bar_close - trigger_price > avg_body * 0.5:  # closed convincingly above
               return (True, 'HOLD', f'recovery close: close={bar_close:.2f} > stop={trigger_price:.2f}')

       # --- CHECK 3: Volume confirmation ---
       # A real breakdown comes with conviction. A low-volume sweep is noise.
       # Require the trigger bar to have at least 70% of average volume.
       volume_ratio = bar_volume / avg_volume_20d if avg_volume_20d > 0 else 1.0
       if volume_ratio < 0.7:
           # Low-volume stop trigger — likely a grab during a quiet period
           # Widen stop by 0.3 ATR but DON'T exit yet
           return (True, 'WIDEN_AND_HOLD', f'low-volume trigger: vol ratio={volume_ratio:.2f} (<0.7 threshold)')

       # --- CHECK 4: Time-of-day gating ---
       # First 30 minutes have massive noise. Last 30 minutes have positioning games.
       # Stops triggered during these windows are disproportionately false.
       if seconds_since_open < 1800:  # first 30 min
           # Widen by 0.5 ATR during opening noise window
           return (True, 'WIDEN_AND_HOLD', f'opening noise window: {seconds_since_open}s since open')

       if premarket or postmarket:
           # Thin liquidity outside regular hours = easy to engineer a stop sweep
           return (True, 'WIDEN_AND_HOLD', f'extended hours trigger: pre={premarket}, post={postmarket}')

       if seconds_since_open > 20700:  # last 30 min of regular session (6.5h = 23400s)
           return (True, 'WIDEN_AND_HOLD', f'closing positioning window: {seconds_since_open}s since open')

       # --- CHECK 5: Multi-timeframe confirmation ---
       # A 1-min tick below the stop means nothing if the 5-min bar is still above.
       # Require confirmation on the higher timeframe.
       if len(bars_5m) >= 1:
           last_5m = bars_5m[-1]
           if last_5m.low > trigger_price:
               # 1-min triggered but 5-min is clean — grab
               return (True, 'HOLD', f'1-min violation only: 5-min low={last_5m.low:.2f} > stop={trigger_price:.2f}')

       # --- ALL CHECKS PASSED: REAL BREAKDOWN ---
       return (False, 'EXIT', f'confirmed breakdown: volume ratio={volume_ratio:.2f}, close={bar_close:.2f}')

   ```

   **Detector rationale**: The 5 checks form a progressive sieve. A stop must fail ALL 5 defenses to execute:
   - Check 1 (Wick): Catches 60-70% of false triggers — the most common grab pattern
   - Check 2 (Close): Catches intra-bar reversal grabs — price goes through, then back
   - Check 3 (Volume): Filters low-conviction moves during quiet periods
   - Check 4 (Time): Blocks noise windows where stop hunting is concentrated
   - Check 5 (MTF): Ensures the breakdown shows on multiple timeframes, not just a 1-min tick

3. **Stop execution after grab check**:

   ```python
   def execute_stop_exit(position: Position, trigger_price: float, stop_type: str, context: dict) -> Order | None:
       is_grab, action, reason = is_liquidity_grab(
           trigger_price, stop_type,
           context['bars_1m'], context['bars_5m'],
           context['avg_volume_20d'],
           context.get('premarket', False),
           context.get('postmarket', False),
           context.get('seconds_since_open', 0)
       )

       log_event(position.id, stop_type, trigger_price, is_grab, action, reason)

       if action == 'HOLD':
           return None  # do nothing — it was a grab

       if action == 'WIDEN_AND_HOLD':
           # Widen the stop by 0.3 ATR and continue monitoring
           position.hard_stop -= (0.3 * position.atr_at_entry)
           position.trailing_stop -= (0.3 * position.atr_at_entry)
           position.grab_widen_count += 1
           if position.grab_widen_count >= 3:
               # After 3 widens, the thesis is broken — exit
               return Order(side='sell', qty=position.remaining_shares, type='market')
           return None

       # action == 'EXIT': confirmed breakdown
       return Order(side='sell', qty=position.remaining_shares, type='market')
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

Complete when: Exit trigger hierarchy is armed (6 levels checked every 30 seconds). Liquidity grab detector is live — all 5 confirmation layers (wick, close, volume, time-of-day, multi-timeframe) evaluating every stop trigger before execution. HOLD/WIDEN_AND_HOLD/EXIT actions logged per trigger. Portfolio risk dashboard is computing VaR/CVaR/max-drawdown/beta/correlation/net-delta in real time. Hard circuit breaker is set at 20% drawdown. Black swan hedge is evaluated and purchased if VIX < 15.

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

Complete when: Vectorized backtest produced with entry/exit logic across full date range. Walk-forward validation completed (5+ windows, out-of-sample Sharpe within 20% of in-sample). All reality checks applied (survivorship bias, look-ahead bias, slippage model, commission drag, regime test). Post-trade P&L attribution report generated with win rate, profit factor, exit reason breakdown, and sector PnL.
