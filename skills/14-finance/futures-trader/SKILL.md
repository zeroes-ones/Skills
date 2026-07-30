---
name: futures-trader
description: >
  Use when trading futures contracts across any asset class — equity index futures (ES, NQ, YM, RTY),
  commodity futures (CL, GC, NG, ZC, ZW, ZS, CT, KC, HG), interest rate futures (ZB, ZN, ZF, ZT),
  or currency futures (6E, 6J, 6B, 6A). Handles futures-specific execution (Globex 23/5 sessions,
  GTC/IOC/FOK orders), SPAN margin calculation and cross-margining, contract roll mechanics
  (calendar spreads, roll yield, contango/backwardation), seasonal pattern analysis, COT report
  integration, inter-commodity and intra-commodity spread construction, futures options overlay,
  and delivery/expiration management. Do NOT use for equity stock trading (route to
  algorithmic-trader), ETF trading (route to technical-signals-engineer), cash forex (route to
  forex-trader), or physical commodity procurement (route to commodities-analyst).
license: MIT
tags:
  - futures-trader
  - futures-trading
  - cmegroup
  - span-margin
  - es-futures
  - commodity-futures
  - interest-rate-futures
  - cot-report
  - contract-roll
  - seasonality
author: Sandeep Kumar Penchala
type: finance
status: stable
version: 1.0.0
updated: 2026-07-30
token_budget: 5500
chain:
  type: symmetric
  consumes_from:
    - commodities-analyst
    - quantitative-analyst
    - market-data-engineer
    - options-risk-engineer
    - technical-signals-engineer
  feeds_into:
    - portfolio-signal-manager
    - algorithmic-trader
    - macro-strategist
  alternatives:
    - algorithmic-trader
    - forex-trader
---
# Futures Trader
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Trade futures contracts across all major asset classes with discipline specific to the futures market structure. Futures are NOT stocks — they have expiration, margin that expands near delivery, 23/5 trading on Globex, roll mechanics that create structural edge (or loss), and contract specifications that vary by exchange. This skill covers execution, margin, roll strategy, seasonal patterns, COT report analysis, spread construction, and futures options overlays across CME, CBOT, NYMEX, COMEX, ICE, and EUREX. Every position is sized against SPAN margin, rolled with explicit roll-date rules, and monitored for delivery risk. Futures leverage averages 10:1 to 20:1 [VERIFIED] — a 5% adverse move can wipe out 50-100% of initial margin. Risk management is not a feature; it is the product.

## <!-- DEEP: 5+min --> RESEARCH_PREREQUISITE — Execute Before Any Output

**This is a HARD GATE. Do not produce ANY output, trade recommendation, contract analysis, or execution plan without completing this research.**

Before you act, you MUST execute every applicable research step. Research-before-acting is the difference between professional trading and gambling:

| # | Research Step | Why It Matters | Where to Look |
|---|--------------|----------------|----------------|
| **RP1** | **Verify contract specifications are current.** Contract size, tick value, trading hours, margin requirements, delivery terms, and expiration calendar CHANGE by exchange announcement. CME revises margins weekly. A $6,000 ES margin from last month may be $12,000 today. | [STALE_RISK] Trading with stale contract specs causes wrong position sizing (e.g., ZB tick = $31.25, not $15.625 like ZN). Margin surprise = forced liquidation. Delivery terms change can put you into physical delivery unaware. | CME Group product pages, exchange memos, broker margin reports |
| **RP2** | **Audit the current portfolio for futures exposure.** Read existing positions across all accounts. Futures in one account interact with futures options in another through SPAN cross-margining. | [CONTEXT_VIOLATION] Entering a long ES in account A while holding short ES calls in account B creates synthetic exposure you didn't compute. SPAN cross-margining means separate accounts may still be linked. | Broker portfolio view, SPAN risk arrays, cross-margining reports |
| **RP3** | **Cross-reference claims against exchange sources.** Every contract spec, margin rate, and trading hour must be [VERIFIED] against exchange documentation. Never rely on training data for margin rates — they change weekly. | [HALLUCINATION_GUARD] CME margin rates updated weekly. A claim that "ES margin is $12,000" without [VERIFIED] against current CME clearing data is dangerous. Wrong margin = wrong position sizing. | cmegroup.com/clearing, ice.com, eurex.com, broker margin API |
| **RP4** | **Identify the contract's delivery/expiration mechanics.** Is this physically delivered or cash-settled? What are First Notice Day (FND) and Last Trading Day (LTD)? Which contracts have delivery windows vs single-day expiration? | [DELIVERY_SURPRISE] Physical delivery contracts (CL, GC, ZC, ZW) REQUIRE closing before FND unless you have a delivery facility. Cash-settled (ES, NQ) auto-settle. Confusing the two = catastrophic outcome. | CME contract specifications, broker delivery notices, exchange delivery calendars |
| **RP5** | **Quantify roll cost.** What is the spread between front-month and next-month? Is the market in contango (futures > spot) or backwardation (futures < spot)? What is the annualized roll yield (positive or negative)? | [ROLL_COST_BLINDNESS] A commodity ETF bleeding 12% annually to contango looks "flat" on a chart. The chart shows price, not roll cost. Over 12 months, roll cost can consume 50%+ of a position's value. | Futures term structure, broker roll analysis tools, CME settlement data |
| **RP6** | **Map seasonality windows.** Does this commodity have known seasonal patterns? What is the current position in the seasonal cycle (planting, growing, harvest, storage drawdown, demand peak)? | [SEASONALITY_SURPRISE] Buying natural gas in October after storage is full and before winter demand materializes is buying into a structural headwind. Seasonality is probabilistic, not deterministic — but ignoring it is willful blindness. | USDA WASDE reports, EIA storage data, commodity seasonality calendars |
| **RP7** | **Verify against SPAN margin requirements.** Compute SPAN margin for any new position. Check if cross-margining with existing positions reduces combined margin. Verify margin buffer > 40% unused. | [MARGIN_CALL_RISK] SPAN margin changes with volatility and time. A position at 50% margin utilization in low vol is at 90%+ when vol doubles. Futures brokers auto-liquidate within minutes of margin deficit. | SPAN risk arrays (CME FTP), broker margin API, portfolio margin calculator |
| **RP8** | **Declare explicit limitations.** What does this trade NOT protect against? What market conditions invalidate the thesis? What is the worst-case loss (including gap risk through stops)? | [SCOPE_HONESTY] "I'm buying ES futures because I'm bullish" is incomplete. "I'm buying ES futures, bullish based on [factor], thesis invalid if ES closes below [level]. Max loss = [amount] if gap through stop on [event]." That is professional. | Trade plan template, risk management rules |

**If you skip any of these research steps, you are not producing quality output — you are guessing with leverage.** Futures amplify mistakes at 10:1 to 20:1. A $5,000 error in stocks is a $50,000-$100,000 error in futures. The references, ground rules, and decision trees in this skill exist specifically to prevent guessing. Use them.

> **Compliance:** Research must be executed before any substantial output. For each step, document findings inline in your response using `[RESEARCHED]` marker: `[RESEARCHED: RP1 — ES contract specs verified against CME, margin = $13,200 as of [date].]`. Partial research = partial quality. Zero research = zero credibility.

### 🔄 Iterative Research Loop — Research at EVERY Decision Point, Not Just Entry

**The RP1-RP8 cycle above is NOT a one-time gate.** It fires continuously at every material decision point throughout the workflow:

| Loop | When It Fires | What Re-research Validates |
|------|--------------|---------------------------|
| **Loop 0: Pre-Action** | Before producing ANY trade recommendation, execution plan, or position analysis | Contract specs, portfolio audit, source verification, delivery mechanics, roll cost, seasonality, SPAN margin, limitations |
| **Loop 1: Mid-Action** | At roll decision, position adjustment, stop-loss trigger, margin buffer drop below 40%, or significant news event | Has vol changed SPAN margin? Has term structure flipped? Has a seasonal window opened/closed? Are delivery dates approaching? |
| **Loop 2: Pre-Exit** | Before trade entry, position exit, contract roll, or declaring completion | Is the execution plan complete? Are all contract specs verified? Is margin buffer sufficient? Is delivery risk zero? |
| **Loop 3: Post-Action** | After trade execution, roll completion, or exit | What was the realized roll cost vs estimated? Did the fill match expectation? What slippage was experienced? What learnings to apply? |

**Integration into Core Workflow:**

Every decision point in a skill's Core Workflow must be marked with:
```
[RESEARCH LOOP: Re-execute RP1-RP8 before proceeding to next phase]
```

This ensures the agent pauses to re-verify ALL research dimensions before making the next decision. Futures markets move 23 hours a day. Context from 2 PM is stale by 8 PM.

**Markers for output:** At each loop, the agent outputs: `[RESEARCHED: Loop N — RP1-RP8 re-verified. Key delta from previous loop: ...]`

> **Compliance:** Research must be executed before any substantial output AND re-executed at every decision point. For each research loop, document findings inline. Partial research = partial quality. Zero research = zero credibility. Stale research = dangerous confidence with 20:1 leverage.

### Futures Domain Extension — Execute These ADDITIONAL Research Steps

| # | Research Step | Why It Matters | Where to Look |
|---|--------------|----------------|----------------|
| **RP-F1** | **Identify First Notice Day and Last Trading Day.** For physical delivery contracts: FND is the REAL deadline — after FND, longs can be assigned delivery. LTD is the trading deadline. The gap between FND and LTD can be 5-10 days — during which you hold a position that can convert to physical delivery at any moment. | [DELIVERY_NIGHTMARE] A retail trader long 1 CL (1,000 barrels) past FND receives a delivery notice. They now owe $75,000 for 1,000 barrels of crude oil that MUST be taken at Cushing, OK. The broker liquidates at any price — typically a 5-15% loss from market. | CME delivery calendars, broker FND/LTD schedules, contract specifications |
| **RP-F2** | **Check the COT (Commitments of Traders) report structure.** What are commercial hedgers doing? What are large speculators doing? Are there extreme net-long or net-short positions that signal crowded trades? | [CROWDED_TRADE] When large speculators are record-long a commodity, the exit is crowded. A reversal catches everyone on the same side — amplifying the move 2-3× normal. The COT report is a contrarian indicator at extremes. | CFTC COT reports (weekly, released Fridays), cotbase.com, barchart.com/cot |
| **RP-F3** | **Verify roll date and roll methodology.** When does this position get rolled? What is the roll strategy (calendar spread at market, limit spread, ratio roll)? What is the current calendar spread cost? | [ROLL_LEAKAGE] Rolling with market orders on expiration day costs 2-3× more than rolling with limit calendar spreads 5-7 days before expiration. Roll cost compounds — 12 rolls/year × $50/contract extra slippage = $600/contract/year in unnecessary cost. | Futures term structure, roll analyzer, broker roll tools, historical calendar spread data |
| **RP-F4** | **Compute the contract's notional value.** Futures notional = contract multiplier × current price. ES at 5,500 × $50 = $275,000 per contract. CL at $75 × 1,000 = $75,000. ZB at 120-00 × $1,000 = $120,000. Position size MUST be normalized to account equity — 3 ES contracts on $100K = 8.25:1 notional leverage. | [LEVERAGE_ILLUSION] "I only put up $39,600 in margin for 3 ES" — but you control $825,000 in notional. A 2% ES decline (110 points) = $16,500 loss (16.5% of account). Margin is the deposit, not the risk. Notional is the risk. | Contract specs × current price, broker notional value calculation |

## Route the Request

<!-- QUICK: 30s — auto-route first, then intent-route -->

### Auto-Route (No User Input Required)

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*.py", "futures|es_|nq_|cl_|gc_|zb_|zn_|span_margin|cot_report|contract_roll|globex")` AND `file_contains("*.py", "CME|NYMEX|COMEX|CBOT|ICE|EUREX|delivery|FND|LTD")` | This is your skill. Jump to **Core Workflow** — Phase 0 (Contract Analysis). |
| A2 | `file_contains("*.py", "futures_option|ES.*option|CL.*option|fop|span.*risk_array")` AND NOT `file_contains("*.py", "contract_roll|delivery|FND|cot")` | Invoke **options-risk-engineer** for futures options risk. Then return here for execution. |
| A3 | `file_contains("*.py", "seasonal|contango|backwardation|roll_yield|supply_demand|crop|inventory")` AND NOT `file_contains("*.py", "margin|execution|order|broker")` | Invoke **commodities-analyst** for physical market analysis. Return here if trade execution is needed. |
| A4 | `file_contains("*.py", "forex|currency_pair|spot_fx|pip|carry_trade")` AND NOT `file_contains("*.py", "6E|6J|6B|currency_future|CME")` | Invoke **forex-trader** for spot FX. Currency futures (6E, 6J) are this skill's domain. |
| A5 | `file_contains("*futures*.py|*roll*.py|*cot*.py|*span*.py")` AND `file_contains("*.py", "alpaca|ibkr|schwab|robinhood")` | This is your skill. Jump to **Core Workflow** — Phase 3 (Execution). |

### Intent Route

```
What futures trading task?
├── Contract specification lookup → Phase 0
├── SPAN margin calculation → Phase 1
├── Contract roll strategy → Phase 2
├── Trade execution (order type, session, sizing) → Phase 3
├── COT report analysis → Phase 4
├── Seasonal pattern analysis → Phase 5
├── Spread construction (intra/inter-commodity) → Phase 6
├── Delivery/expiration management → Phase 7
├── Futures options overlay → Phase 8
└── Full trade lifecycle → Run Phases 0-8 sequentially

```

## Ground Rules — Read Before Anything Else

<!-- STANDARD: 3min -->

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to enter any futures position without computing notional value and normalizing to account equity. "Buy 2 ES" is dangerously incomplete. Report: "2 ES = $550,000 notional [COMPUTED] = X% of account. Margin required: $Y [VERIFIED]. Max adverse move before margin call: Z points." | Trigger: position_sizing without notional_value / account_equity ratio | STOP. "Position sizing incomplete. Compute: notional value [COMPUTED], % of equity, margin required [VERIFIED], and margin-call distance. Futures leverage amplifies mistakes at 10:1+. Never enter without full sizing analysis." |
| R2 | REFUSE to hold ANY physical-delivery futures contract past First Notice Day. Physical delivery = you receive (long) or deliver (short) the actual commodity. Most brokers auto-liquidate retail positions before FND at unfavorable prices. Get out before they do. | Trigger: position.expiration - current_date < days_to_FND AND contract.delivery_type == "PHYSICAL" | STOP. "Physical delivery contract {symbol} approaching FND ({date}). Close or roll IMMEDIATELY. Broker auto-liquidation typically occurs 1-3 days before FND at market — you lose control of exit price. Manual close NOW at your chosen price." |
| R3 | REFUSE to use equity-style position sizing for futures. "2% risk per trade" applied to futures requires computing the dollar risk per tick × stop distance in ticks. A 10-tick ES stop = $125 risk per contract ($12.50/tick). 3 contracts = $375 stop risk. | Trigger: position_sizing uses equity stop-loss logic without tick-value adjustment | STOP. "Futures position sizing requires tick-value awareness. Apply: risk_per_contract = tick_value × stop_distance_in_ticks. Max contracts = (account × risk_pct) / risk_per_contract. Equity sizing logic ignores contract multipliers." |
| R4 | REFUSE to roll futures contracts without computing the calendar spread cost. Rolling "at market" costs 1-3 ticks in spread slippage. Rolling with a limit calendar spread order saves 30-60% of roll cost. Over 12 rolls/year, this is significant. | Trigger: roll_action without calendar_spread_cost_computed | STOP. "Roll cost not computed. Determine: front-month bid/ask, next-month bid/ask, calendar spread mid, spread slippage estimate. Optimal roll: limit calendar spread order at mid + 1 tick. Market roll = guaranteed slippage." |
| R5 | REFUSE to compute SPAN margin without verifying current exchange scan ranges. SPAN risk arrays are updated weekly by CME Clearing. Using last month's scan range understates margin by 20-50% in high vol. | Trigger: span_margin_computation without verified_scan_range_date within 7 days | STOP. "SPAN scan range not current. CME updates SPAN risk arrays weekly. Verify current scan range for {symbol} at cmegroup.com/clearing. Margin error = forced liquidation at worst price." |

## Anti-Hallucination

<!-- STANDARD: 3min — EXTRA CRITICAL for futures -->

Futures contract specifications, margin rates, and delivery rules CHANGE. CME margin rates change weekly. Contract multipliers occasionally change (CME reduced ZB tick from $31.25 to $15.625 for micros). Delivery rules are amended by exchange notice. **Every contract-specific number must carry its provenance and verification date.**

### Provenance Tags (Mandatory on All Numerical Output)

| Tag | Meaning | When to Use | Example |
|-----|---------|-------------|---------|
| `[VERIFIED]` | Confirmed against current exchange documentation within 7 days | Contract specs, margin rates, trading hours, delivery terms | "ES margin = $13,200 [VERIFIED] against CME Clearing as of 2026-07-28" |
| `[COMPUTED]` | Calculated by this skill from verified inputs using known formulas | Notional value, SPAN margin from risk arrays, roll cost from term structure | "2 ES notional = $550,000 [COMPUTED]: 2 × $50 × 5500.00. Margin/equity = 26.4% on $100K account." |
| `[ESTIMATED]` | Calculated but with known uncertainty; always includes ±X% error bound | Slippage estimates, roll cost in volatile markets, COT-based sentiment | "Roll cost estimate: $35-55/contract [ESTIMATED ±20%] based on current calendar spread of 2.50-3.50 with 1-tick wide market." |
| `[BROKER-VERIFIED]` | Confirmed against broker API or account statement | Current margin requirement, position P&L, realized roll cost | "Account SPAN margin = $41,200 [BROKER-VERIFIED] via IBKR API at 14:31 ET. Buffer: 38% unused." |

### Safety Protocol Rules

| # | Rule | Mechanical Trigger | Penalty |
|---|------|-------------------|---------|
| S1 | **Admit uncertainty** — When data is stale (>5 min), when the model doesn't cover this scenario (binary events, delivery mechanics, physical settlement), when liquidity is insufficient for clean pricing — say so. "Cannot compute SPAN margin — current CME risk array not available. Use broker API or cmegroup.com/clearing." | Any output containing a price, contract spec, margin number, or trade recommendation without a [VERIFIED] or [BROKER-VERIFIED] provenance tag | BLOCK OUTPUT. $50K-$500K in forced liquidations from acting on "certain" numbers that were fabricated or stale |
| S2 | **Flag your knowledge cutoff** — Your training data has a cutoff date. SPAN scan ranges change weekly. CME adds/delists contracts. Broker futures API support evolves (Alpaca doesn't offer futures as of 2026-07). If you don't know the current state, pull live data or say so. | Output containing a position size, leverage ratio, or margin calculation without the [COMPUTED] derivation showing the formula and inputs | BLOCK OUTPUT. $10K-$200K in mispriced risk from stale assumptions about contract specs, margin rates, or broker capabilities |
| S3 | **Never guess security or broker capabilities** — Margin at IBKR is not margin at Schwab. Auto-liquidation policies differ. "Most brokers" is dangerous. If the broker's specific futures support is unverified, route user to broker-integration-futures.md or say "unverified." | Output claiming a broker supports a futures feature (API, order type, SPAN pull) without [BROKER-VERIFIED] | BLOCK OUTPUT. $25K-$1M in margin calls from assuming one broker's rules apply to another |
| S4 | **Never confuse contract sizes** — ES = $50 × index, MES = $5 × index. CL = 1,000 barrels. ZC = 5,000 bushels. Confusing these = 10× position size error. Always pull from contract-specifications.md or cross-verify exchange + broker. | Output with a tick value or notional that, if off by a factor of 10, changes position sizing by >20% | BLOCK AND CORRECT. $25K-$250K in oversized positions from contract spec errors |
| S5 | **Never ignore delivery terms** — Physical delivery (CL, GC, NG, ZC, ZW, ZS, CT, KC, HG) requires closing before FND. Cash-settled (ES, NQ, YM, RTY) auto-settle. Trading a physical-delivery contract without knowing FND is negligence. | Trade output for a physical-delivery contract without FND date [VERIFIED] and exit plan | BLOCK OUTPUT. $50K-$500K in auto-liquidation losses or accidental delivery obligations |

## Anti-Rationalization

<!-- DEEP: 10+min -->

| Rationalization | Reality |
|---|---|
| "ES is just like trading SPY but with better hours and more leverage. Same analysis applies." | ES is NOT SPY. ES has expiration and roll mechanics, different tax treatment (60/40 rule under Section 1256), no dividend adjustments, and trades in a different market microstructure (central limit order book on Globex vs fragmented equity markets). A SPY support level at $550 is ES support at 5,500 — but the liquidity profile, order book depth, and session behavior are completely different. **Cost: $10K-$100K in "same as SPY" trades that fail on futures-specific mechanics you didn't account for.** |
| "The contract is cash-settled so I don't need to worry about expiration. I can hold until the last day." | Cash-settled futures still have expiration effects. Liquidity migrates from expiring contract to next contract starting ~7 days before expiration. Holding until Last Trading Day means you're trading in a thinning book — wider spreads, less depth, more slippage. And many brokers auto-close cash-settled positions 1-2 days before LTD. **Cost: $500-$2,000 per contract in excess slippage on expiration week. Roll at 7-10 DTE, not on LTD.** |
| "I'll just put a stop-loss and go to sleep. The market will take care of it." | Stop orders in futures become market orders when triggered. A stop at 5,480 in ES becomes a market sell at whatever the next bid is. In a fast market, that might be 5,475 — or 5,450 if there's a flash crash. Stops protect against slow moves, not gap moves. And futures trade 23/5 — a stop triggered at 2 AM CT in illiquid conditions fills at much worse prices. **Cost: $2,500-$12,500 in stop-slippage per contract during gap moves. Stops are risk mitigation, not risk elimination.** |
| "The COT report shows commercials are net-long — they must know something. I'll follow the smart money." | Commercial hedgers are NOT speculating. They're hedging physical production/consumption. A grain elevator being short futures (offsetting long physical grain) looks "bearish" on COT but is actually neutral — they're hedged. COT data must be interpreted through the lens of who the participants are and what their commercial motive is. Following commercials blindly = trading based on misunderstood positioning. **Cost: $5K-$50K in copycat trades that misunderstand the commercial motive behind the positioning.** |
| "I'll just buy the micro contract (MES) — it's 1/10 the size so it's 1/10 the risk." | Micro contracts have 1/10 the notional but the SAME percentage risk. MES at $5/point vs ES at $50/point — a 100-point ES loss = $5,000 vs $500 on MES. Percentage-wise identical. The smaller size is better for position sizing granularity, not for reducing risk per unit of capital. A $100K account trading 20 MES ($275K notional) has the same leverage as 2 ES ($275K notional). **Cost: Death by a thousand cuts — small contract sizes mask the aggregate leverage. Track notional, not contract count.** |

## The Expert's Mindset

<!-- STANDARD: 3min -->

World-class futures trading is about understanding the machinery — contract specifications, margin mechanics, roll costs, delivery terms, and session behavior — and exploiting structural edges while avoiding structural traps. Futures are the most transparent market in the world (central limit order book, published volume/OI, COT data, exchange-regulated) and simultaneously the most dangerous (leverage, delivery, 23/5 trading, margin calls). The futures trader lives by two questions: "What is the notional exposure of this position relative to my account?" and "Exactly when and how does this contract expire?" If you cannot answer both definitively, you are not trading futures — you are gambling with leverage.

## Operating at Different Levels

<!-- STANDARD: 3min -->

| Level | Scope | Example |
|-------|-------|---------|
| **L1: Apprentice** | Trade single futures contract with basic technical analysis and stop-losses | "Buy 1 MES at 5,500 with stop at 5,480. Notional: $27,500. Risk: $100 (20 pts × $5). 0.5% of $20K account." |
| **L2: Practitioner** | Multi-contract with roll strategy, seasonal awareness, and SPAN margin monitoring | "Long 2 ES (Jun) at 5,520. Roll to Sep at 7 DTE using calendar spread limit. SPAN margin: $28,400 [VERIFIED]. COT shows specs net-long but not extreme. Seasonal: May historically bullish (60% win rate, avg +2.1%)." |
| **L3: Senior** | Multi-asset futures with inter-commodity spreads, COT-based positioning, and futures options overlay | "Long ES/short NQ spread (2:1 ratio) on tech underperformance thesis. Net delta: +$85K ES / -$42K NQ. Selling ES calls against long to reduce theta bleed. Monitoring COT extremes for reversal signal." |
| **L4: Staff** | Cross-asset macro futures portfolio with curve trades, volatility arbitrage, and market-making awareness | "Long ZB/short ZN steepener on curve-dislocation thesis. DV01-neutral. Adding long CL calendar spread on backwardation-to-contango transition. Portfolio SPAN margin: $185K on $500K equity (37% utilization)." |
| **L5: Transformative** | Design systematic futures trading framework with automated roll execution, SPAN optimization, and multi-broker routing | "Implementing automated calendar-spread roll engine at 7 DTE with TWAP execution. SPAN margin optimization through cross-margining with futures options. Broker-aware routing: ES to IBKR, CL to Tastytrade for optimal commissions." |

## When to Use

<!-- QUICK: 30s -->

- Executing trades in any CME Group futures contract (ES, NQ, YM, RTY, CL, GC, NG, ZB, ZN, ZF, ZT, 6E, 6J, 6B, ZC, ZW, ZS, CT, KC, HG, etc.)
- Computing SPAN margin requirements and cross-margining opportunities
- Planning and executing contract rolls with calendar spread analysis
- Analyzing CFTC Commitment of Traders (COT) reports for positioning insights
- Identifying seasonal patterns in commodity and financial futures
- Constructing inter-commodity and intra-commodity spreads
- Managing delivery risk — tracking FND, LTD, and physical vs cash settlement
- Overlaying futures options for yield enhancement or hedging
- Navigating Globex session behavior and liquidity patterns

## When NOT to Use

<!-- QUICK: 30s -->

- Trading individual stocks or ETFs — use **algorithmic-trader**
- Trading spot forex (EUR/USD, GBP/JPY) on retail platforms — use **forex-trader**
- Physical commodity procurement or hedging physical inventory — use **commodities-analyst**
- Corporate hedging under ASC 815 (hedge accounting) — use **accountant** + **commodities-analyst**
- Purely speculative crypto perpetual swaps (Binance, Bybit) — use **crypto-trader**
- Single-stock options or equity options strategies — use **options-strategist** + **options-risk-engineer**
- Fixed income portfolio management beyond futures overlay — use **fixed-income-analyst**

## Best Practices

<!-- STANDARD: 3min -->

1. Always compute notional value before entry — margin is the deposit, notional is the risk
2. Roll 7-10 days before expiration using calendar spread limit orders, never market orders
3. Exit physical-delivery contracts 3+ business days before First Notice Day — broker deadlines vary
4. Never let SPAN margin utilization exceed 60% — futures margin expands under volatility
5. Verify contract specifications against exchange website within 7 days of any trade
6. COT data is a contrarian indicator at extremes, not a trend-following signal
7. Trade during primary session hours (8:30 AM-3:15 PM CT for most CME products) — avoid settlement periods
8. Tick value, not point value, determines dollar P&L — memorize tick sizes for traded products
9. Futures are Section 1256 contracts — 60% long-term / 40% short-term capital gains regardless of holding period
10. Cross-margin futures with futures options when possible — SPAN recognizes offsetting positions
11. Never hold more than 3 contracts of any product without knowing the market depth at 3× your position
12. Reconcile broker margin report daily — SPAN margin changes, and you find out when the broker auto-liquidates

## Error Decoder

<!-- STANDARD: 3min -->

| Symptom | Root Cause | Fix |
|---------|------------|-----|
| Position auto-liquidated overnight | Broker has auto-liquidation rules for positions approaching FND (physical delivery). Liquidation happens 1-3 business days before FND at market price | Track FND for every physical-delivery contract. Close 5+ business days before FND. Set calendar alerts. Never assume "there's still time" — brokers are more conservative than exchange rules |
| Margin requirement doubled without trading | CME increased SPAN scan range on weekly recalculation. Typically happens after volatility spikes — margin follows vol with ~1-week lag. Combined with position moving against you = double margin call | Monitor CME clearing notices. Anticipate margin increases after VIX spikes 10+ points. Maintain 40%+ margin buffer to absorb weekly recalculation increases |
| Roll cost was 3× expected | Spread widened during roll execution — likely rolling on expiration day when liquidity migrates to next contract. The front-month book thins, calendar spread widens | Roll 7-10 days before expiration. Use calendar spread orders, not sequential outright trades. Monitor roll cost daily in the roll window and execute when spread is favorable |
| Stop-loss filled 20 ticks below trigger | Stop order became market order in a fast market. The 20-tick gap is the difference between your stop price and the next available bid during the flush. Stops are risk mitigation, not price guarantees | Use stop-limit orders with appropriate limit width (5-10 ticks beyond stop). Accept that gap moves through stops are unhedgeable — position size accordingly |
| Physical delivery notice received on long CL | Held long Crude Oil futures past First Notice Day. CME's delivery system assigned a delivery notice. Broker auto-liquidated at penalty pricing | Never hold physical-delivery contracts past FND. Cash-settled contracts (ES, NQ) — fine. Physical (CL, GC, NG, grains) — close 5+ days before FND |

## Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|---|---|---|
| ❌ **Using equity-style "2% risk per trade" without tick-value adjustment** | "2% of $50K = $1,000 risk. ES tick = $12.50. 8-tick stop = $100 risk per contract. So I can trade 10 contracts." WRONG. 10 ES = $2.75M notional on $50K account = 55:1 leverage. A 0.2% ES move = complete account wipeout | ✅ Compute: (1) notional per contract, (2) tick value × stop ticks = dollar risk per contract, (3) max contracts = (account × risk_pct) / dollar_risk_per_contract, (4) verify notional/equity < 5:1 for overnight positions |
| ❌ **Rolling by closing front-month and opening next-month as two separate orders** | Two outright orders pay the bid-ask spread TWICE — once to exit front-month (sell at bid), once to enter next-month (buy at ask). A 1-tick spread × 2 orders = 2 ticks cost. The calendar spread is 1-tick wide — half the cost | ✅ Use a calendar spread order: "Sell 1 ZCZ6 / Buy 1 ZCH7 at -3'2 limit." One order, one spread, one tick of cost. Every broker supports spread orders — use them |
| ❌ **Treating all futures contracts as having the same risk profile** | ES ($12.50/tick, $50/point, $275K notional at 5500) vs ZN ($15.625/tick, $1,000/point, ~$110K notional) vs CL ($10/tick, $1,000/point, $75,000 notional at $75). Each has different vol profiles, margin reqs, session liquidity, and event sensitivity | ✅ Build a contract profile database: multiplier, tick value, notional at current price, 20-day ATR in dollars, SPAN margin, roll date, delivery type, primary session hours. Size positions by dollar vol, not contract count |
| ❌ **Holding commodity futures through USDA/EIA/OPEC+ report releases** | WASDE (grains), EIA storage (energy), OPEC+ meeting (crude) — these events routinely move markets 3-5% in minutes. A stop-loss becomes irrelevant when the market gaps through it. Your $500 risk becomes $2,500 actual loss | ✅ Calendar all major report dates. Reduce position by 50% or exit 24h before. Re-enter after the report settles. The report is a binary event — you're gambling, not trading, if you hold through it |
| ❌ **Ignoring the futures curve structure when choosing which expiration to trade** | Buying the front-month in a steep contango market (e.g., VIX futures, natural gas in shoulder season) means paying a premium that decays as expiration approaches. The position needs the underlying to rise just to offset roll decay | ✅ Always check the term structure. In contango: prefer deferred months or spread trades (sell front/buy back). In backwardation: front-month long positions benefit from roll yield. The curve IS the trade — don't ignore it |

## State Log

<!-- STANDARD: 3min -->

| State Field | Type | Persists Across | Description |
|---|---|---|---|
| `positions.active` | [FuturesPosition] | Realtime | All open futures positions: contract, quantity, entry price, current price, unrealized P&L, FND, LTD |
| `positions.notional` | {symbol: notional} | Realtime | Notional value per contract = multiplier × current price. Aggregate notional across positions |
| `positions.leverage` | float | Realtime | Total notional / account equity. Alert if >5:1 for multi-contract or >3:1 overnight |
| `margin.span_current` | float | Daily | Current SPAN margin requirement [BROKER-VERIFIED] from broker API |
| `margin.span_utilization` | float | Realtime | Margin used / total margin available. Alert at 50%, danger at 70%, critical at 85% |
| `margin.span_scan_range` | {symbol: scan_range} | Weekly | Current SPAN scan range per product from exchange. Updated weekly |
| `margin.cross_margin_benefit` | float | Weekly | Dollar reduction in margin from cross-margining futures with futures options |
| `roll.calendar` | [RollEvent] | Session | Upcoming roll dates per position with target expiration and current calendar spread |
| `roll.cost_history` | [RollCost] | Archive | Historical roll costs per contract roll: estimated vs actual, slippage, timing |
| `delivery.fnd_calendar` | [FNDEvent] | Session | First Notice Day dates for all physical-delivery positions |
| `delivery.ltd_calendar` | [LTDEvent] | Session | Last Trading Day dates for all positions |
| `cot.positioning` | [COTSnapshot] | Weekly | Latest COT data: commercial net, large spec net, small spec net, open interest change |
| `cot.extreme_flag` | boolean | Weekly | True if any COT category is at 2+ year extreme (potential contrarian signal) |
| `seasonal.current_phase` | {commodity: phase} | Daily | Current position in seasonal cycle per traded commodity |
| `execution.session` | SessionType | Realtime | Current trading session: PRE-OPEN, OPEN, DAY, LUNCH, CLOSE, POST-CLOSE, OVERNIGHT |
| `execution.liquidity` | {contract: LiquidityScore} | Realtime | Bid-ask spread, market depth at 3 levels, current volume vs 20-day average |

## Core Workflow

<!-- STANDARD: 3min -->
All computation details in references/futures-trading-computations.md.

### Phase 0: Contract Specification Analysis (Full detail → references)
1. Pull contract specs (ticker, multiplier, tick_val, point_val, notional, delivery, FND/LTD, margin) from verified exchange sources.
   |-- Complete when: All [VERIFIED] fields populated with source + date. Notional & leverage [COMPUTED]. FND/LTD in calendar. Margin verified.

### Phase 1: SPAN Margin Analysis (Full detail → references)
1. Fetch SPAN margin from exchange. Check if broker adds surcharge (~10-20%). Analyze margin/notional ratio, scan array decomposition, concentration charge.
2. Stress-test worst-case scan loss against equity buffer (max 50% drawdown). Set account-level hard cap at 80% buying power.
   |-- Complete when: SPAN line items decomposed [VERIFIED]. Max loss vs equity computed [COMPUTED]. Position size hard cap set. Circuit breaker triggered if >80% BP consumed.

### Phase 2: Contract Roll Strategy (Full detail → references)
1. Check calendar: proximity to expiration, volume migration, open interest shift, spread width, backwardation/contango influence.
2. Execute roll via calendar spread or leg-by-leg. Manage roll cost (commission, slippage, spread P&L).
   |-- Complete when: Roll date selected. Method chosen + execution criteria. Cost computed [COMPUTED]. Roll alert logged with State Log.

### Phase 3: Execution and Order Management (Full detail → references)
1. Route order: DOM depth, spread check, aggressive/passive, iceberg/synthetic, stop placement logic, multi-contract splitting.
   |-- Complete when: Order type + routing method selected and justified. Slippage estimate [COMPUTED]. Pre-trade checklist satisfied.

### Phase 4: COT Analysis (Full detail → references)
1. Pull COT report (producer/merchant, managed money, other reportables). Build positioning index (z-score vs 52-week). Classify: extreme, crowded, neutral, contrarian.
   |-- Complete when: Positions extracted [VERIFIED]. z-score [COMPUTED]. Positioning classification assigned with actionable label.

### Phase 5: Seasonality Framework (Full detail → references)
1. Compute 5/10/15-year monthly averages, standard deviations, win rates. Classify as strong/weak/neutral. Combine with COT for weighted directional bias (60% COT / 40% seasonality).
   |-- Complete when: Monthly stats [COMPUTED] for all lookback periods. Classification assigned. COT/seasonality weight boundary check satisfied.

### Phase 6: Spread Trading (Full detail → references)
1. Identify spread opportunity: inter-commodity, intra-commodity calendar, crack/crush. Compute correlation, cointegration, mean-reversion half-life.
2. Size the spread: spread notional, SPAN margin offset, leg ratio.
   |-- Complete when: Spread type identified. Correlation/cointegration [COMPUTED]. SPAN offset verified [VERIFIED]. Risk-to-reward computed [COMPUTED].

### Phase 7: Delivery Management (Physical-Settled Only) (Full detail → references)
1. For physical delivery contracts: monitor FND/LND/LTD. NO physical delivery under any circumstance — exit or roll before FND.
   |-- Complete when: Calendar entries set (FND-5 as CLOSE deadline). Exit strategy written at position open. NO physical-settled positions within 5 days of FND.

### Phase 8: Options on Futures (Overlay) (Full detail → references)
1. Identify overlay opportunities: protective puts, covered calls, collars. Size to futures underlying. Verify expiration BEFORE FND.
   |-- Complete when: Overlay strategy defined. SPAN margin impact [COMPUTED]. Max profit/risk bounded. Expiration verified pre-FND.
## Decision Trees

<!-- STANDARD: 3min -->

### DT1: Should I Trade This Contract?
```
Leverage ≤ 5:1 overnight? → NO → Reduce size or day-trade only
  ↓ YES
SPAN margin utilization <60%? → NO → Add capital or reduce position
  ↓ YES
Physical delivery & FND >7 days? → NO → Exit before FND-5
  ↓ YES
Roll cost <3% annualized? → NO → Consider spread or deferred month
  ↓ YES
PROCEED ✓
```

### DT2: Roll Decision — Calendar Spread or Outright?
```
FND<10 or LTD<14? → NO → Hold current contract
  ↓ YES
Intend to maintain exposure? → NO → CLOSE: outright sell at limit
  ↓ YES
Calendar spread >0 (backwardation)? → NO → Roll cost >5% annualized? → NO → ROLL: accept cost
  ↓ YES                                              ↓ YES
ROLL favorable ✓                                RECONSIDER: position may have negative carry
```
## Gotchas

| Gotcha | Cost | Fix |
|--------|------|-----|
| Holding futures through FOMC/NFPs/CPI releases believing your stop will protect you — stops are NOT market orders, they're triggers that send market orders. On FOMC day, ES can gap 50 points (100 ticks) in 30 seconds. Your 8-tick stop becomes a 50-tick fill. "Risk management" fails catastrophically because the mechanism you relied on (stop = guaranteed exit) is flawed | $2,500-$15,000 per contract in excess loss vs expected stop. On 1 ES contract, expected $400 loss (8 pts × $50) becomes $2,500+ actual (50 pts × $50). On 3 contracts: $7,500+ loss. This is the #1 cause of blown-up futures accounts | Reduce position size by 50-75% 24h before known high-impact events. Replace stops with options-based protection (buy OTM puts/calls). Accept that event risk IS the risk — you either size for it or hedge it, but you can't stop-order your way out of it |
| Trading micro contracts (MES, MNQ, M2K) as "practice" then scaling to mini contracts (ES, NQ) thinking "it's the same, just bigger" — the psychological difference between $6.25/tick (M2K) and $50/tick (ES) is not linear. Watching a position move -$1,000 in 20 minutes (normal for 1 ES) triggers different decision-making than watching -$125 (same move in MES). Bad decisions multiply with contract size | $5,000-$50,000 in behavioral losses during the scaling process. The trader who is disciplined at $125 drawdowns becomes erratic at $1,000 drawdowns. Psychology doesn't scale linearly with contract size | Scale gradually: MES (1 month) → 2 MES (1 month) → 1 ES (2 months) → 2 ES (3 months). Track trade decisions per drawdown level. If you make impulsive decisions at any level, stay at that level for another month. The market will always be there — your capital won't be if you rush scaling |
| Using equity-style portfolio allocation ("I'll put 10% in gold futures, 10% in oil...") — 1 GC contract at $3,100/oz = $310,000 notional. 1 CL contract at $75 = $75,000 notional. On a $200,000 account, that's 192.5% notional allocation. "10% allocation" in futures means nothing because each contract has a different notional value | $20,000-$100,000 in blown-up positions from misunderstanding leverage. A "10% allocation" mentality applied to futures leads to 20:1+ leverage that triggers margin calls on routine 2% moves | Allocate by DOLLAR RISK, not by notional. "I want each trade to risk 1% of my account ($2,000 on $200K). If my ES stop is 8 points ($400 risk), I trade 5 contracts." OR: "I want my total notional under 3× account equity overnight. On $200K, that's $600K notional = 2 ES contracts." Both methods prevent leverage creep |
| Rolling futures positions without checking the roll cost first — the calendar spread between front-month and next-month can represent 10%+ annualized cost in steep contango markets (natural gas, VIX, some grain spreads). Rolling "blind" locks in this cost without evaluation | 5-20% annualized drag on returns. A strategy that makes 15% annually before roll costs might make only 5% after roll costs in a contango market. The roll IS the edge — or the leak | Always compute the annualized roll cost before committing to a position. Formula: (calendar spread / front-month price) × (365 / days between expirations). If >5% annualized, consider: (a) the deferred month instead, (b) a spread trade instead of outright, (c) whether the thesis can overcome this headwind |
| Assuming all "futures" trade 23/5 like ES — grain futures (ZC, ZS, ZW) trade 8:30 AM-1:20 PM CT (day session) + 7:00 PM-7:45 AM CT (overnight). Entering a grain position at 2:00 PM CT means you entered AFTER the close — your order sits until the overnight open at 7:00 PM, exposed to any gap | $500-$5,000 in overnight gap losses. Grain markets routinely gap on overnight weather forecasts, export sales announcements, and WASDE report releases at 11:00 AM CT | Know your contract's trading hours before placing an order. Check the CME product spec page for every contract you trade. Grain day-session close at 1:20 PM CT is 2 hours BEFORE the equity close — this catches equity traders every harvest season |

## Proactive Triggers

| # | Trigger Condition | Auto-Response |
|---|------------------|---------------|
| P1 | `margin_utilization > 0.60` | [ALERT] SPAN margin utilization at {value}%. Buffer narrowing. Reduce positions by {amount} or add {dollars} capital to return to 50% target |
| P2 | `days_to_fnd <= 10 AND position.contract.delivery_type == 'PHYSICAL'` | [URGENT] {symbol} FND in {days} days. Plan exit. Calendar spread to roll, or outright close. Broker auto-liquidation at FND-{broker_days} |
| P3 | `calendar_spread.roll_cost_annualized > 0.05` | [WARN] Roll cost for {symbol} is {pct}% annualized. Position must overcome this headwind. Consider deferred month or spread alternative |
| P4 | `cot.z_score[symbol].large_spec_net > 2.0 OR cot.z_score[symbol].commercial_net > 2.0` | [SIGNAL] COT extreme in {symbol}: {category} net position at {z_score}σ. Contrarian signal active. Reduce or reverse to align with commercial positioning |
| P5 | `session.phase IN ['OVERNIGHT', 'PRE-OPEN'] AND order.type == 'MARKET'` | [BLOCK] Market orders not permitted outside DAY (core) session. Use limit or marketable limit. Overnight gaps make market orders dangerous |
| P6 | `calendar_spread.bid_ask_ticks >= 3 AND order.type == 'MARKET'` | [BLOCK] Wide spread detected. Market order would cross 3+ ticks. Use limit order at midpoint or wait for DAY session |
| P7 | `futures_positions.count > 0 AND major_report_dates.next_24h` | [ALERT] USDA/EIA/OPEC+/FOMC report in <24h. Binary event risk. Reduce position by 50% or hedge with options |
| P8 | `leverage.overnight > 5.0` | [CRITICAL] Overnight leverage at {ratio}:1, exceeding 5:1 limit. Reduce before session close to avoid margin call on overnight gap |

## Cross-Skill Coordination

### Upstream (Data & Analysis Flow In)

| Upstream Skill | What You Receive | Trigger | Your Response |
|---|---|---|---|
| `quantitative-analyst` | Statistical models, volatility forecasts, correlation matrices, regime detection signals | **PUSH:** Regime change detected. **PUSH:** Vol forecast updated. **PULL:** requestModel when sizing requires regime context | Regime change → adjust position sizing, tighten stops, reduce leverage. Vol forecast → update SPAN margin estimates, review risk per contract |
| `market-data-engineer` | Real-time futures quotes, contract chain data, session status, data quality alerts | **PUSH:** Price update for held contracts. **PUSH:** Session change (OPEN/CLOSE/OVERNIGHT). **PULL:** requestChain when evaluating roll targets | Price update → recompute unrealized P&L, check stop proximity. Session change → adjust order types per session rules. Data degraded → halt new orders |
| `options-risk-engineer` | Portfolio Greeks, margin impact of options overlay, pin risk on short options on futures, gamma exposure profile | **PUSH:** Options position added/modified. **PUSH:** Pin risk alert (expiration week). **PULL:** requestMarginImpact when evaluating futures options overlay | Options added → recompute combined futures+options SPAN margin. Pin risk → close short futures options approaching expiration ITM |
| `technical-signals-engineer` | Entry/exit signals, trend strength, momentum readings, support/resistance levels, volume profile | **PUSH:** Entry signal generated. **PUSH:** Exit/stop-loss signal. **PUSH:** Trend reversal alert | Entry signal → validate against COT positioning, seasonality, roll cost. Exit signal → execute as limit or marketable limit per session rules. Reversal → tighten stops, do NOT add to position |
| `commodities-analyst` | Supply/demand balance, WASDE projections, EIA storage data, weather impact forecasts, physical market conditions | **PUSH:** Major report released (WASDE, EIA, acreage). **PUSH:** Supply disruption alert. **PUSH:** Seasonal phase transition | Report release → reduce position 50% or exit 24h before. Supply disruption → evaluate impact on contract month held. Seasonal transition → realign bias per seasonality calendar |

### Downstream (Execution & Portfolio Flow Out)

| Downstream Skill | What You Send | Trigger | Expected Response |
|---|---|---|---|
| `portfolio-signal-manager` | Futures positions: contract, quantity, notional, SPAN margin, leverage ratio, roll schedule, FND dates | **PUSH:** New futures position opened. **PUSH:** Position closed/rolled. **PUSH:** Delivery risk alert (FND approaching) | Portfolio manager integrates futures notional into total portfolio exposure. Flags if combined equity+futures leverage exceeds limits |
| `algorithmic-trader` | Execution instructions: contract, side, quantity, order type, limit price, session constraint, spread order flag | **PUSH:** Trade signal validated and ready for execution. **PUSH:** Roll order (calendar spread). **PUSH:** Emergency liquidation (margin call, delivery risk) | Order confirmation with fill price and slippage. Roll execution report with calendar spread fill. Emergency fill report |
| `macro-strategist` | Cross-asset futures exposure: equity index, rates, currencies, commodities — notional, direction, conviction | **PUSH:** Significant position change in any asset class. **PUSH:** COT extreme detected (contrarian macro signal). **PULL:** requestFuturesExposure when assessing total macro risk | Macro strategist evaluates cross-asset correlation, identifies overcrowded trades, flags conflicting positions across asset classes |

## Error Recovery

| Symptom | Root Cause | Fix | Lesson |
|---|---|---|---|
| Margin utilization jumped from 45% to 78% overnight without trading | SPAN scan range was increased by CME on Friday. Your positions didn't change but the exchange now considers them riskier. This happens every volatile week | Pull SPAN margin daily, not weekly. Maintain 50% utilization target so a 20% scan range increase doesn't trigger a margin call. If utilization >60%, reduce positions BEFORE the Friday SPAN update | SPAN is dynamic, not static. CME changes scan ranges weekly based on realized volatility. A quiet period lulls traders into maxing out margin. A vol spike + SPAN increase = margin call cascade |
| Rolled ES position perfectly on calendar spread but feel uneasy because you can't verify the fill was fair | Calendar spreads have wider quoted markets than outright futures. The "bid-ask" you see may be 1-2 ticks but the actual spread between real bids and offers could be wider. You may have paid more than necessary | Always check the implied spread: (front-month bid - next-month ask) vs (front-month ask - next-month bid). Your fill should be between these two values. Track roll slippage per roll to build a benchmark | Calendar spread "price" can be misleading. The true spread market has width that varies with volatility, time to expiration, and open interest migration |
| COT data shows commercials heavily short but the market keeps rallying — contrarian signal is "wrong" | COT is a medium-term signal (weeks to months), not a timing tool. Commercials can be short and right for months before the turn comes. The 3-day lag (report Friday, positions as of Tuesday) means you're trading stale data | NEVER use COT alone for entry timing. Combine: COT extreme + technical reversal pattern + seasonal shift. Wait for price confirmation before fading the crowded trade. The market can stay irrational longer than you can stay solvent | COT tells you WHO is positioned WHERE, not WHEN the turn happens. Contrarian signals without timing are just academic. Price must confirm before you commit capital |
| Thought you were trading "Corn" but ZC, ZCPA, ZC electronic, and ZC pit-traded are different instruments | Some commodities have parallel contracts: electronic (Globex), pit-traded (open outcry), and alternative delivery specifications. ZC electronic ≠ ZC pit, especially in the closing minutes when pit liquidity dries up | Always specify the exchange and trading venue. Most retail traders should ONLY trade Globex electronic contracts. Pit-traded contracts have different hours, different liquidity, and different last-trade times | Futures symbols are NOT unique without exchange + venue. CME Globex symbols are the standard for electronic trading |
| Placed a "market" order at 6:01 PM CT Sunday open and got filled 15 ticks from the last Friday close | Sunday opens gap. The first prints are often wide as the order book builds. Market orders in the first 60 seconds of the Sunday open are a donation to market makers | Use limit orders for ALL Sunday/Monday open entries. Wait 60 seconds for the order book to populate. The first minute of the week is the most expensive minute to use a market order | Sunday opens gap. Period. Market orders at the open = paying the maximum possible spread. Wait for the book to build or use limits |

## What Good Looks Like

A high-quality futures trade execution:

```
Account: $100,000. Trade: Long 1 ES at 5525.50.
Notional: $276,275. Leverage: 2.76:1. ✓
SPAN Margin: $13,200. Utilization: 13.2%. ✓ (well below 50%)
Delivery: Cash-settled. No FND risk. ✓
Session: DAY (core), 10:30 AM CT. Spread: 0.25 wide. ✓
Order: Limit at 5525.50. Filled at 5525.50. Zero slippage. ✓
Stop: 5517.50 (32 ticks, $400 risk = 0.4% of account). ✓
Roll plan: Calendar spread at LTD-10. Target: Sep→Dec roll. ✓
COT: No extreme positioning. No contrarian signal. ✓
Seasonality: May-Oct bearish. Counter-seasonal. Reduced conviction. ⚠
Sizing adjustment: 1 contract (not 2) due to counter-seasonal bias. ✓
```

The position is sized for the gap risk (overnight max 5:1 leverage), session-aware (limit order during high-liquidity window), delivery-safe (cash-settled), and roll-ready (plan in place). Every number is tagged [VERIFIED] or [COMPUTED]. No fabrications.

## Verification Guardrails

Before delivering work, verify:

- [ ] **All prices from live market data:** No training-data prices used. Every price tagged [VERIFIED] with source and timestamp
- [ ] **All computations tagged:** [COMPUTED] = calculated from verified inputs, [BROKER-VERIFIED] = confirmed via broker API, [VERIFIED] = confirmed via exchange or regulator source
- [ ] **All notional values computed and leverage checked:** Never trade by contract count alone — always surface the notional value in dollars
- [ ] **All FND/LTD dates confirmed from exchange calendar:** No physical-delivery position without exit plan before FND-5
- [ ] **All SPAN margin from exchange or broker:** Never estimate. SPAN changes weekly — stale margin numbers cause margin calls
- [ ] **All roll strategies use calendar spread orders:** Never two outright orders. Quote the calendar spread price
- [ ] **No fabricated contract specs:** Multiplier, tick size, tick value, trading hours all from exchange specification
- [ ] **Anti-hallucination provenance tags present:** Every factual claim tagged. No claim without source

If any checkbox fails, revise before delivering. If revision is impossible (no live data), inform the user of exactly what cannot be verified and why.

## Deliberate Practice

### Exercise 1: Contract Spec Drill (5 min)
Pick 3 futures contracts you don't trade. For each, find and verify: multiplier, tick size, tick value, delivery type, FND date, primary session hours. Compare CME product page vs broker platform vs a data vendor. Did all three agree?

### Exercise 2: Notional & Leverage Calculation (5 min)
Given an account size of $100,000, compute the notional value and leverage ratio for: 2 ES at 5525, 1 CL at $75, 3 ZC at $4.50/bu, 1 GC at $3,100. Which positions exceed the 5:1 overnight limit? Which are day-trade only?

### Exercise 3: Roll Cost Analysis (5 min)
For CL: front-month $75.00, next-month $75.80, 30 days between expirations. Compute the annualized roll cost for a long position. At what annualized cost would you consider NOT rolling and instead exiting?

### Exercise 4: COT Signal Detection (5 min)
Given: Corn commercials net long +350K (3yr mean: +50K, std: 120K), large specs net short -180K (3yr mean: -20K, std: 80K). Compute z-scores. What is the contrarian signal? Would you go long, short, or stay flat?

### Exercise 5: Session-Based Order Selection (5 min)
For each scenario, select the correct order type and session: (a) Entering long ES at 10:30 AM CT, (b) Exiting long CL at 3:05 AM CT, (c) Rolling ZC from Sep to Dec at 12:00 PM CT, (d) Emergency exit at 8:32 AM CT during NFP release.

## References
* [contract-specifications.md](references/contract-specifications.md) — Contract specs for all major futures: multiplier, tick size, tick value, delivery type, FND/LTD, trading hours, exchange
* [span-margin-calculator.md](references/span-margin-calculator.md) — SPAN margin computation: risk arrays, scan range, cross-margining rules, exchange minimums
* [roll-strategy-guide.md](references/roll-strategy-guide.md) — Roll execution: calendar spread orders, timing windows, cost analysis, broker-specific roll mechanics
* [cot-analysis-framework.md](references/cot-analysis-framework.md) — COT interpretation: categories, positioning extremes, z-score computation, contrarian signal detection
* [seasonality-calendar.md](references/seasonality-calendar.md) — Commodity seasonality tables: bullish/bearish windows per commodity, transition dates, historical reliability scores
* [delivery-management.md](references/delivery-management.md) — Physical delivery: FND/LTD calendars, broker auto-liquidation policies, delivery assignment mechanics
* [broker-integration-futures.md](references/broker-integration-futures.md) — Broker API specifics for futures: IBKR futures orders, Schwab futures, order types, SPAN pulls
* [tax-treatment.md](references/tax-treatment.md) — Section 1256 60/40 treatment, mark-to-market rules, wash sale inapplicability, Form 6781 filing requirements
* [error-recovery.md](references/error-recovery.md) — Futures-specific error patterns: margin call response, gap-through-stop recovery, delivery notice handling, roll error correction

