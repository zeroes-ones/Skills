# Futures Trading — Full Computation Reference

Extracted from Core Workflow Phases 0-8 for progressive disclosure. Loaded on demand when the model needs implementation-level detail.

## Core Workflow

<!-- STANDARD: 3min -->

### Phase 0: Contract Specification Analysis

```
1. PULL CONTRACT SPECIFICATIONS FROM VERIFIED SOURCES

   For each contract under consideration, populate:

   {
     "contract": "ES",
     "exchange": "CME",
     "multiplier": 50,
     "tick_size": 0.25,
     "tick_value": 12.50,  // $50 × 0.25 = $12.50
     "point_value": 50,     // $50 per full point
     "current_price": 5525.50 [VERIFIED via market-data-engineer],
     "notional_value": 276275,  // [COMPUTED] = 5525.50 × $50
     "delivery_type": "CASH_SETTLED",
     "first_notice_day": null,  // N/A for cash-settled
     "last_trading_day": "2026-09-18",
     "trading_hours": "SUN 5PM-FRI 4PM CT (break 3:15-3:30 PM)",
     "primary_session": "8:30 AM-3:15 PM CT",
     "span_margin": 13200 [VERIFIED via CME Clearing 2026-07-28],
     "margin_per_notional_pct": 4.78,  // [COMPUTED] 13200/276275
     "daily_volume": 1500000 [VERIFIED],
     "roll_date_target": "2026-09-08"  // 10 days before LTD
   }

2. NOTIONAL AND LEVERAGE CALCULATION

   For position_size contracts:
   Total Notional = position_size × multiplier × current_price
   Leverage Ratio = Total Notional / Account Equity

   Leverage Limits:
   ├── Day trade (intraday): max 10:1
   ├── Overnight position: max 5:1
   ├── Multi-contract portfolio: max 5:1 aggregate
   └── Single position: max 3:1 overnight

   Example [COMPUTED]:
   Account: $100,000. ES at 5525.50. 1 contract.
   Notional: $276,275. Leverage: 2.76:1. ✓ Acceptable overnight.
   3 contracts: $828,825 notional. Leverage: 8.29:1. ✗ EXCEEDS overnight limit.

3. DELIVERY RISK ASSESSMENT

   ├── CASH_SETTLED → No delivery risk. Auto-settles at final settlement. ✓
   ├── PHYSICAL with FND > 10 days away → Monitor. Roll/close before FND. ⚠
   ├── PHYSICAL with FND < 10 days away → URGENT: Plan exit within 5 days. ⚠⚠
   └── PHYSICAL with FND < 5 days away → CRITICAL: Close immediately. Broker may auto-liquidate. ⛔

   Complete when: Contract specs verified [VERIFIED with date]. Notional and leverage computed [COMPUTED].
   Delivery type identified with FND/LTD in calendar. Margin verified against exchange.

```

### Phase 1: SPAN Margin Analysis

```
1. RETRIEVE SPAN RISK ARRAYS

   Source: CME Clearing FTP (ftp.cmegroup.com/pub/span) or broker API
   SPAN risk arrays contain 16 scenarios per contract [VERIFIED]:
   - 6 price change scenarios: ±1/3, ±2/3, ±3/3 of scan range
   - 6 price + volatility scenarios: same price moves, ±vol shift
   - 4 extreme move scenarios: ±extreme, ±(extreme × 0.35)

2. COMPUTE SINGLE-CONTRACT SPAN MARGIN

   SPAN Margin = max(futures_scan_risk, short_option_minimum)
   For outright futures position:
   margin_per_contract = scan_risk × contract_multiplier × number_of_contracts

   Example [COMPUTED]:
   ES scan range = 240 points (current CME value)
   SPAN margin for 1 ES = 240 × $50 = $12,000
   (Plus any additional exchange/broker minimums)

3. CROSS-MARGINING OPPORTUNITY

   If holding futures + futures options in same product:
   ├── Long ES futures + Short ES calls → Reduced margin (delta offset)
   ├── Short ES futures + Short ES puts → Reduced margin (delta offset)
   └── Uncorrelated positions → No cross-margin benefit

   Cross-margining typically reduces combined margin by 20-60% vs
   computing each position independently [VERIFIED].

4. MARGIN BUFFER CALCULATION

   Margin Utilization = Total SPAN Margin / Net Liquidation Value
   Safety thresholds:
   ├── 0-40%: HEALTHY — significant buffer
   ├── 40-60%: NORMAL — monitor daily
   ├── 60-75%: ELEVATED — reduce or add capital; vol expansion = margin call risk
   └── >75%: DANGER — immediate position reduction required

   Complete when: SPAN margin computed [COMPUTED] or [BROKER-VERIFIED]. Cross-margining assessed.
   Margin utilization calculated with buffer threshold alert.

```

### Phase 2: Contract Roll Strategy

```
1. DETERMINE ROLL WINDOW

   Optimal roll: 7-10 calendar days before Last Trading Day
   Rationale: Liquidity begins migrating from front-month to next-month ~14 DTE.
   By 7 DTE, next-month volume exceeds front-month. By 3 DTE, front-month is illiquid.

2. ANALYZE CALENDAR SPREAD

   Calendar Spread = Front-Month Price - Next-Month Price

   ├── Calendar Spread > 0 → BACKWARDATION
   │   Front-month premium. Long positions: favorable roll (sell high, buy low).
   │   Short positions: unfavorable roll (buy high, sell low).
   │
   └── Calendar Spread < 0 → CONTANGO
       Front-month discount. Long positions: unfavorable roll (sell low, buy high).
       Short positions: favorable roll (buy low, sell high).

   Annualized Roll Yield = (Calendar Spread / Front-Month Price) × (365 / Days Between Expirations)

   Example [COMPUTED]:
   CL: Front-month $75.00, Next-month $75.80
   Calendar spread = -$0.80 (contango)
   Days between expirations = 30
   Annualized roll cost for longs = (0.80/75.00) × (365/30) = 13.0%
   → Long CL pays 13% annually in roll costs. Must overcome this just to break even.

3. EXECUTE THE ROLL

   Method: Calendar spread order (NOT two outright orders)

   Order: "Sell 2 ESU6 / Buy 2 ESZ6 at +3.75 limit"
   ├── This is ONE order that executes as a spread
   ├── Pay ONE bid-ask spread, not two
   ├── Slippage: typically 0.5-1 tick in ES calendar spreads
   └── Time: execute during primary session (8:30 AM-3:15 PM CT)

   Anti-pattern: "Close 2 ESU6 at market, then Buy 2 ESZ6 at market"
   → Pay bid-ask twice. Slippage: 2-4 ticks. Cost: 2-4× the calendar spread method.

   Complete when: Roll window identified. Calendar spread analyzed with annualized cost/benefit [COMPUTED].
   Roll order constructed as calendar spread with limit price. Roll date recorded.

```


### Phase 3: Execution and Order Management

```
1. SESSION-BASED EXECUTION STRATEGY

   | Session | Time (CT) | Liquidity | Spread | Best Orders |
   |---------|-----------|-----------|--------|-------------|
   | PRE-OPEN | 8:00-8:30 AM | LOW | WIDE (3-10 ticks) | AVOID. Wide spreads, thin book |
   | OPEN | 8:30-9:00 AM | EXTREME | NORMAL (1-2 ticks) | LIMIT only. Volatility spikes |
   | DAY (core) | 9:00 AM-3:00 PM | HIGH | TIGHT (1 tick) | LIMIT or MARKETABLE LIMIT |
   | CLOSE | 3:00-3:15 PM | HIGH | TIGHT | LIMIT. Settlement approaching |
   | POST-CLOSE | 3:15-3:30 PM | MEDIUM | WIDENING | AVOID for new entries |
   | OVERNIGHT | 5:00 PM-8:00 AM | LOW-MEDIUM | WIDER (1-3 ticks) | LIMIT only. News events = gap risk |

2. ORDER TYPE SELECTION

   ├── LIMIT → Primary order type. Specifies max pay (buy) or min receive (sell).
   │   Best during: DAY (core) session. Always use for: calendar spreads.
   │   Risk: non-execution if market moves away.
   │
   ├── MARKETABLE LIMIT → Limit at current ask (buy) or bid (sell). Near-immediate fill.
   │   Best during: OPEN or high-vol periods when you must get in.
   │   Risk: partial fill if limit price moves through rapidly.
   │
   ├── MARKET → Immediate fill at best available price.
   │   Best during: DAY (core) with high liquidity. Use ONLY for exits when price is moving FAST.
   │   Risk: slippage in fast markets. ES: 1-2 tick typical, 5-10 tick possible on events.
   │   ⛔ NEVER use market orders for calendar spreads — price is undefined.
   │
   └── STOP → Triggers market order when stop price is hit.
       Best during: DAY (core). Risk management only — not for entries.
       Risk: GAP through = orders fill at much worse price than stop level.
       ⛔ NEVER use stops during OVERNIGHT — gaps are common.

3. POSITION SIZING FROM TICK VALUE

   Formula: contracts = floor(risk_dollars / (stop_ticks × tick_value))

   Example [COMPUTED]:
   Account: $100,000, Risk: 1% = $1,000
   Trade: Long ES at 5525.50, Stop: 5517.50 (8 points = 32 ticks)
   Risk per contract: 32 × $12.50 = $400
   Max contracts: floor($1,000 / $400) = 2 contracts
   Total notional: 2 × $276,275 = $552,550
   Leverage: 5.53:1 — exceeds overnight limit. Day trade only.
   [ALERT] If intended as overnight, reduce to 1 contract: $276,275 notional, 2.76:1 ✓

   Complete when: Session identified with liquidity profile. Order type selected with rationale.
   Position size computed from tick-value risk math [COMPUTED]. Leverage checked against limits.

```

### Phase 4: Commitment of Traders (COT) Analysis

```
1. RETRIEVE COT DATA (released Fridays, positions as of Tuesday)

   Source: CFTC website (cftc.gov) or broker data feeds
   Weekly release: Legacy report (futures-only) and Disaggregated report

2. CLASSIFY TRADER POSITIONS

   Disaggregated Categories:
   ├── Producer/Merchant (Commercial Hedgers) — the "smart money"
   ├── Swap Dealers — hedging OTC swap exposure
   ├── Managed Money (Large Speculators) — trend followers, momentum
   ├── Other Reportables — non-commercial, non-managed-money
   └── Nonreportable (Small Speculators) — retail, typically wrong at extremes

3. DETECT POSITIONING EXTREMES

   Net Position = Long Contracts - Short Contracts

   For each category, compute z-score vs 3-year rolling window:
   z-score > 2.0 → 2+ standard deviation extreme

   Extreme interpretation (contrarian signals):
   ├── Commercials NET LONG at multi-year high → Bullish. Producers expect higher prices.
   ├── Commercials NET SHORT at multi-year high → Bearish. Producers hedging aggressively.
   ├── Large Specs NET LONG at multi-year high → Bearish. Trend followers all-in, no buyers left.
   └── Large Specs NET SHORT at multi-year high → Bullish. Crowded short, squeeze potential.

   Example [COMPUTED]:
   Corn (ZC): Commercials net long +350K (2.8σ above mean)
   Large specs net short -180K (2.1σ extreme)
   → Contrarian BULLISH. Producers are buying. Specs are all short — squeeze fuel.

4. INCORPORATE COT INTO POSITIONING

   ├── COT supportive + Technical bullish → Full size
   ├── COT supportive + Technical bearish → Half size, tight stop
   ├── COT contrary + Technical bullish → Half size, monitor for COT reversal
   ├── COT contrary + Technical bearish → No position or short-biased
   └── COT at extreme + approaching seasonal shift → MAX conviction contrarian

   Complete when: Latest COT data retrieved [VERIFIED with date]. Positioning extremes flagged.
   COT signal classified (supportive/neutral/contrary) and incorporated into sizing.
   Extreme alert set if any category >2σ from mean.

```

### Phase 5: Seasonality Framework

```
1. IDENTIFY SEASONAL PHASE

   Commodities have reliable seasonal patterns driven by:
   ├── Planting/growing/harvest cycles (grains, softs)
   ├── Heating/cooling demand (natural gas, heating oil)
   ├── Driving season (gasoline, crude oil)
   ├── Tax-year positioning (equity index rolls)
   └── Pre-harvest weather premium (grains: May-July)

2. SEASONALITY SCORECARD

   | Commodity | Bullish Window | Bearish Window | Driver |
   |-----------|---------------|----------------|--------|
   | Corn (ZC) | Mar-Jun (planting weather) | Jul-Sep (harvest pressure) | Growing cycle |
   | Soybeans (ZS) | Feb-May (SA weather) | Jun-Aug (US growing) | NH/SH rotation |
   | Natural Gas (NG) | Sep-Nov (storage build) | Mar-May (shoulder) | Heating demand |
   | Crude Oil (CL) | Jun-Aug (driving) | Sep-Nov (refinery maint) | Demand cycles |
   | ES (S&P) | Nov-Apr (Santa Claus) | May-Oct (Sell in May) | Tax/calendar effects |
   | Gold (GC) | Dec-Feb (jewelry demand) | Jun-Aug (doldrums) | Seasonal demand |

3. INCORPORATE SEASONALITY

   ├── Season bullish + Technical bullish + COT supportive → GREEN LIGHT. Full size.
   ├── Season bullish + Technical bearish → AMBER. Wait for confirmation.
   ├── Season bearish + Technical bullish → AMBER. Counter-seasonal = reduced conviction.
   ├── Season bearish + Technical bearish + COT contrary → RED LIGHT. Stay flat.
   └── Seasonal transition approaching (within 2 weeks) → Adjust bias proactively.

   ⚠ WARNING: Seasonality is tendency, not guarantee. 2022 natural gas defied 30-year seasonal
   patterns. Always size for the possibility that this year breaks the pattern.

   Complete when: Seasonal phase identified per commodity [VERIFIED]. Seasonality bias scored.
   Position alignment with seasonal tendency assessed. Transition dates flagged.

```

### Phase 6: Spread Trading

```
1. SPREAD TYPE SELECTION

   ├── INTRAMARKET (Calendar) Spread: Same commodity, different expirations
   │   Trade the curve shape. Direction: shape (contango/backwardation),
   │   not outright direction. Example: Buy ZCZ6 / Sell ZCH7 if you expect
   │   backwardation to steepen.
   │
   ├── INTERMARKET Spread: Related commodities
   │   Trade the relationship between connected markets.
   │   Example: Buy ZW (wheat) / Sell ZC (corn) — wheat-corn spread.
   │   Example: Buy CL / Sell RB — crack spread (crude → gasoline).
   │
   └── INTER-EXCHANGE Spread: Same commodity, different exchanges
       Arbitrage between venues. Example: WTI (NYMEX) vs Brent (ICE).
       Requires accounts at both exchanges. Advanced. Avoid as primary strategy.

2. SPREAD EXECUTION EXCLUSIVELY VIA SPREAD ORDER

   ⛔ NEVER execute spread as two outright orders. Penalty: double the bid-ask cost.
   ✅ ALWAYS use broker's spread order type: one order, simultaneous fill.
   Spread execution guarantees that:
   ├── Both legs fill at the same time (no leg risk)
   ├── Both legs fill at the spread price (no slippage from moving market)
   └── Margin is SPAN-based, typically 50-80% lower than two outright positions

3. SPREAD PRICING CONVENTIONS

   Calendar spread quoted as: (front-month price) - (back-month price)
   ├── Positive spread = backwardation. "Buy the spread" = buy front, sell back.
   ├── Negative spread = contango. "Sell the spread" = sell front, buy back.

   Intermarket spread quoted as: (long leg price) - (short leg price)
   ├── Wheat-Corn spread: Buy ZW / Sell ZC. Quoted in cents/bu.

4. SPREAD MARGIN ADVANTAGE

   SPAN computes spread margin as the maximum loss across scenarios where
   both legs move but offset each other. Risk reduction is structural.

   Example [COMPUTED]:
   Outright 1 ES long: $12,000 SPAN margin
   Outright 1 ES short: $12,000 SPAN margin
   Both outright: $24,000 total
   Calendar spread (long ESU6, short ESZ6): ~$2,400 SPAN margin
   → Spread margin is 90% lower. Same notional, 10% of the margin.
   [VERIFIED] This is why commercial hedgers trade spreads, not outrights.

   Complete when: Spread type selected with rationale. Spread order constructed.
   Margin advantage quantified [COMPUTED]. Leg risk eliminated via spread order type.

```

### Phase 7: Delivery Management (Physical-Settled Only)

```
1. FIRST NOTICE DAY (FND) MONITORING

   For physical-settled contracts (ZS, ZC, ZW, CL, NG, GC, SI, HG, etc.):
   Not cash-settled (ES, NQ, YM, RTY, VX — no FND concern).

   FND Calendar:
   ├── FND > 10 days → Normal. No action required.
   ├── FND 5-10 days → ACTION REQUIRED: Roll or close within 3 trading days.
   ├── FND 1-5 days → URGENT: Exit within 1 trading day or risk broker auto-liquidation.
   ├── FND TODAY → CRITICAL: Position may already be flagged. Close immediately.
   └── FND PAST → POSITION VIOLATION. Broker may assign delivery obligation. ⛔

2. BROKER DELIVERY POLICIES (varies by broker)

   ├── IBKR: Auto-liquidates long futures positions 2-3 days before FND.
   │   Auto-liquidates short positions 1-2 days before FND. No negotiation.
   ├── Schwab (thinkorswim): Sends margin call and liquidation notice at FND-3.
   ├── Alpaca: Futures not yet supported as of 2026-07-28 [VERIFIED].
   └── Robinhood: Does not support futures.

   ⛔ NEVER assume your broker will warn you. Different brokers, different timelines.
   It is YOUR responsibility to know FND and exit before auto-liquidation.

3. LONG POSITION DELIVERY RISK

   If you're LONG a physical-delivery futures contract at expiration:
   ├── You MUST take delivery of the physical commodity
   ├── For CL: 1,000 barrels of crude oil delivered to Cushing, OK
   ├── For ZC: 5,000 bushels of corn delivered to a CBOT-approved warehouse
   ├── For GC: 100 troy ounces of gold delivered to an approved depository
   └── Brokers DO NOT facilitate physical delivery for retail accounts

   → The broker WILL auto-liquidate your position. You lose control of exit price.

   Complete when: FND/LTD dates confirmed [VERIFIED]. Delivery calendar populated.
   All physical-delivery positions have exit plans before broker auto-liquidation threshold.

```

### Phase 8: Options on Futures (Overlay)

```
1. FUTURES OPTIONS SPECIFICS

   ├── Underlying: One futures contract (not shares). 1 option = right to 1 futures contract.
   ├── Exercise → Futures position, NOT shares. Call exercise = long futures. Put exercise = short futures.
   ├── Expiration: Usually the Friday before the underlying futures' FND.
   │   Some expire INTO the underlying futures contract (they become the futures).
   │   Some expire INTO CASH (settle to the futures settlement price, cash difference).
   │   MUST verify settlement type for each product [VERIFIED].
   └── SPAN margin applies, NOT Reg T. Short options margin is SPAN-based, not fixed percentage.

2. COVERED CALL ON FUTURES

   Long 1 ES futures @ 5525.50 + Short 1 ES 5600 call for $45.00 premium

   SPAN Margin: May be lower than outright futures because the short call
   offsets some of the downside risk on the long futures.

   Max Profit: (5600 - 5525.50) × $50 + $2,250 premium = $5,975
   Happens at: ES ≥ 5600 at expiration

   [COMPUTED] Return on margin: $5,975 / $12,000 = 49.8% (annualized: varies by DTE)

3. PROTECTIVE PUT ON FUTURES

   Long 1 ES futures @ 5525.50 + Long 1 ES 5450 put for $35.00 cost
   Max Loss: (5525.50 - 5450) × $50 + $1,750 put cost = $5,525
   → Absolute floor on loss. Position cannot lose more than $5,525 regardless
   of how far ES drops. This is insurance, not free — the put premium is the cost.

4. CREDIT SPREADS ON FUTURES (advanced)

   Vertical spreads, iron condors, butterflies on futures options use SPAN margin.
   Typically far lower capital requirement than equity option equivalents because
   SPAN models the actual risk of the spread rather than using fixed formulas.

   Complete when: Option settlement type verified [VERIFIED]. SPAN impact computed [COMPUTED].
   Strategy defined with max profit/risk. Exercise/conversion mechanics understood.

```

