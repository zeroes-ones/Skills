# Error Recovery — Forex

## Error 1: News Slippage (Stop Triggered, Filled Far From Stop Price)

**Pattern:** Trader places standard stop-loss at 1.1020 on long EUR/USD. NFP release at 8:30 AM ET causes instant 50-pip spike. Stop triggers at 1.1020 but fills at 1.0970 — 50 pips worse.

**Root Cause:** Standard stop-losses become market orders on trigger. During news, the market gaps THROUGH the stop price. The first available liquidity is at whatever price exists after the gap, not at the stop price.

**Immediate Actions:**
1. Accept the fill. Do NOT try to "get back in" to recover — revenge trading after a bad fill is the #1 account killer.
2. Log the slippage: stop level, fill level, time, event, spread at time of fill.
3. Compute the excess loss: `(fill - stop) × pip_value × lots = unplanned loss`

**Prevention:**
- Use guaranteed stops for news-sensitive positions (pay the premium — wider spread or per-lot fee)
- Reduce position size by 50-75% before scheduled news
- Widen stops by 2× normal before news (the spread alone can trigger tight stops)
- Know the economic calendar: never be surprised by NFP, FOMC, CPI

## Error 2: Swap Miscalculation (Expected +$X, Received -$Y)

**Pattern:** Trader enters long NZD/JPY expecting +$12/day carry. After 2 weeks, account shows $0 credited. Broker swap table shows long NZD/JPY = -$3/day.

**Root Cause:** Swap rates are broker-specific and change daily. Your calculation used the central bank rate differential (RBNZ 4.25% - BoJ 0.25% = 4.00%), but the broker's tom-next rate + markup made it negative. Additionally, some brokers have swap tiers — if your position exceeds a certain size, they use a different rate.

**Immediate Actions:**
1. Check broker's CURRENT swap rate (not 2 weeks ago, not the central bank rate).
2. Verify swap direction: long = earn or long = pay? It varies by broker.
3. If swap is negative: close the position or accept the cost if the directional move outweighs it.

**Prevention:**
- Verify swap from broker API BEFORE entry, not after
- Compare 2-3 brokers' swap rates for multi-week holds
- Build a swap-rate tracker: `[broker, pair, direction, swap_rate, timestamp]`
- For carries >30 days, use brokers with competitive swap (IBKR, Saxo)

## Error 3: Correlation Break ("Hedged" Both Lose)

**Pattern:** Trader is long EUR/USD and short GBP/USD, expecting them to neutralize. EUR/USD drops 2% AND GBP/USD drops 2.5%. The "hedged" position loses 4.5%.

**Root Cause:** Correlation is NOT stable. In a USD liquidity crisis, ALL pairs become correlated at +1.0 (everything sells off against USD). The "hedge" was actually a 2× EUR/GBP short that the trader didn't intend.

**Immediate Actions:**
1. Close BOTH positions. The hedge thesis has failed.
2. Compute accidental cross exposure: `EUR/GBP = EUR/USD / GBP/USD` — track actual cross-pair P&L.
3. Do NOT add more positions to "fix it."

**Prevention:**
- Never "hedge" with correlated pairs. Use the actual asset you want to hedge (DXY futures, EUR futures, or explicit pair).
- Compute net USD exposure after every trade. If it exceeds 2× equity, reduce.
- Track 20-day rolling correlations weekly. If key correlations shift (EUR/USD + USD/CHF drops below -0.80), reassess all positions.

## Error 4: Margin Close-Out During News ("Margin Was Fine Yesterday")

**Pattern:** Trader has positions using 45% margin at 50:1 leverage. NFP day — broker sends notice that leverage is now 25:1. Margin used jumps to 90% and triggers automatic liquidation.

**Root Cause:** Brokers can change margin requirements without notice, especially during high-volatility events. Your 50:1 leverage was "normal conditions" only. The broker's terms explicitly allow margin changes at their discretion.

**Immediate Actions:**
1. Do NOT fight the liquidation. The broker's risk system has already acted.
2. After the event, request a breakdown: which positions were closed, at what prices, and what margin rule triggered it.
3. If the broker changed margin with zero notice and you had a reasonable buffer, consider switching brokers.

**Prevention:**
- Never exceed 50% margin utilization. 45% leaves room for a margin increase.
- Before NFP, FOMC, or elections: reduce to <25% margin.
- Check broker's "margin during news" policy BEFORE volatile events.
- Maintain emergency cash in the account (uninvested) = 20-30% of equity.

## Error 5: Wrong Pair Traded (EUR/USD vs EUR/USD.m vs EUR/USD.pro)

**Pattern:** Trader places order on EUR/USD (standard account, 1.0 pip spread). But they meant to trade on EUR/USD.pro (raw spread, 0.1 pip + commission). The wider spread costs them $90 more on 1 lot.

**Root Cause:** Many brokers offer multiple tiers of the same pair: standard (spread-only, wider), pro/raw/ECN (commission + tight spread), mini (fractional lots only). The trader selected the wrong account type or instrument code.

**Immediate Actions:**
1. Check which instrument was traded: account type, spread at time of entry, commission charged.
2. If this was the broker's default and you didn't have access to the pro tier, request upgrade.
3. Log the cost difference: `(actual_spread - intended_spread) × pip_value × lots`

**Prevention:**
- Create a broker instrument map: `[broker, account_type, pair, instrument_code, typical_spread, commission]`
- Verify the instrument code matches the intended tier before every order
- For OANDA: Core (spread-only) vs Core+commission (raw spread). Check which you're on.
- For IG: Standard vs DMA. DMA requires professional status or $500K+ portfolio.

