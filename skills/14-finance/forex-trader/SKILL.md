---
name: forex-trader
description: >
  Use when trading spot foreign exchange, FX forwards, or managing currency exposure
  across major, minor, and exotic pairs. Handles pip-value computation per pair,
  carry trade analysis (interest rate differentials, swap points, forward points),
  central bank policy anticipation (FOMC, ECB, BOJ, BOE, RBA, RBNZ, BOC, SNB),
  correlation-based pair selection, technical analysis adapted to 24/5 FX market
  structure, session-based liquidity profiling (Asia, London, NY, overlap),
  risk management for leveraged FX (50:1–500:1 depending on jurisdiction),
  and currency futures hedging (6E, 6J, 6B, 6A vs spot equivalents).
  Do NOT use for currency futures execution (route to futures-trader),
  cryptocurrency trading (route to crypto-trader), or macro-only analysis
  without trade execution (route to macro-strategist).
license: MIT
tags:
  - forex-trader
  - fx-trading
  - spot-forex
  - currency-pairs
  - carry-trade
  - central-banks
  - pip-calculation
author: Sandeep Kumar Penchala
type: finance
status: stable
version: 1.0.0
updated: 2026-07-30
token_budget: 5000
chain:
  type: symmetric
  consumes_from:
    - quantitative-analyst
    - market-data-engineer
    - macro-strategist
    - technical-signals-engineer
  feeds_into:
    - portfolio-signal-manager
    - algorithmic-trader
    - futures-trader
  alternatives:
    - futures-trader
    - crypto-trader
---

# Forex Trader
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Trade spot foreign exchange with discipline specific to the decentralized, 24/5 OTC market structure. Forex is NOT equities and NOT futures — it has no central exchange, variable spreads depending on session, rollover/swap that credits or debits daily, and leverage that reaches 500:1 in unregulated jurisdictions. A 0.2% adverse move at 100:1 leverage = 20% account loss. This skill covers spot FX execution, carry trade mechanics, central bank policy trading, correlation-based pair selection, session liquidity profiling, and risk management for leveraged currency positions. Every trade is sized against pip value × stop distance, every carry trade evaluated against interest rate differential sustainability, and every position monitored for central bank event risk.

## Route the Request
### Auto-Route

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*.py", "forex|fx_|spot_|currency_pair|pip|carry_trade|rollover|swap_point")` AND `file_contains("*.py", "EUR/USD|GBP/USD|USD/JPY|central_bank|interest_rate")` | This is your skill. Jump to **Core Workflow**. |
| A2 | `file_contains("*.py", "6E|6J|6B|6A|currency_future|CME.*currency")` AND NOT `file_contains("*.py", "spot|carry|swap|pip")` | Invoke **futures-trader** for currency futures. Return here if spot FX overlay is needed. |
| A3 | `file_contains("*.py", "bond|yield_curve|duration|treasury|sovereign_debt")` AND `file_contains("*.py", "currency|forex|fx")` | Invoke **fixed-income-analyst** for yield differential analysis. Return here for FX execution. |

## Ground Rules

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to compute position size in "lots" without converting to dollar risk via pip value | Trigger: position size output contains "lot", "mini", or "micro" without pip_value × stop_pips = dollar_risk [COMPUTED] | STOP. "Position in lots is ambiguous. Compute: pip_value × stop_pips × lots = dollar_risk. Verify against account risk %." |
| R2 | REFUSE to recommend carry trade without computing: (a) annualized carry return, (b) adverse move that wipes out 1 year of carry, (c) central bank meeting dates in the carry period | Trigger: carry trade recommendation missing any of (a) annualized_rate [COMPUTED], (b) adverse_move_breakeven [COMPUTED], (c) next central bank meeting dates [VERIFIED] | STOP. "Carry trade without break-even analysis is yield-chasing, not trading. A 2% carry that loses 15% on a policy surprise is a negative-EV trade." |
| R3 | DETECT and CORRECT "standard lot" assumptions — a standard lot is 100K units on most pairs but 100K yen is NOT 100K dollars. EUR/USD lot = €100K = ~$110K notional. USD/JPY lot = $100K notional. These are fundamentally different exposures | Trigger: "1 standard lot of [pair]" without computing notional in account currency | STOP. "Standard lots have different notional values across pairs. Compute notional in account currency before sizing." |
| R4 | REFUSE to ignore session liquidity when selecting entry/exit times | Trigger: order recommendation at time T where T falls in lowest-liquidity session for that pair | FLAG. "EUR/USD at 10 PM GMT (Asia session) has 3-5× wider spreads than London/NY overlap. Reschedule or widen stops." |
| R5 | NEVER quote a fixed spread for spot FX — spreads are variable, widen during news, and differ by broker | Trigger: output containing fixed spread value (e.g., "EUR/USD spread is 0.8 pips") without timestamp and session qualifier | STOP. "FX spreads are variable. Quote: 'EUR/USD spread: 0.3-0.8 pips during London/NY overlap, 1.5-3.0 pips during Asia, 5-20 pips during news events [ESTIMATED].'" |

## Verification
<!-- STANDARD: 3min -->

1. **[Pip Value Calculation]** — Verify position sizing shows pip value computation: `pip_value × stop_pips × lots = dollar_risk [COMPUTED]`.
2. **[Carry Trade Break-Even]** — Verify carry trade recommendations include annualized carry return, adverse move that wipes out 1 year of carry, and next central bank meeting dates.
3. **[Session Context]** — Verify entry/exit time includes session liquidity context (overlap vs single-session, expected spread range).

**Pass criteria:** All checks pass before delivering output.

## Anti-Hallucination

### Provenance Tags

| Tag | Meaning | Example |
|-----|---------|---------|
| `[VERIFIED]` | Confirmed against broker feed or central bank source within 24h | "ECB rate = 3.75% [VERIFIED] as of 2026-07-30" |
| `[COMPUTED]` | Calculated from verified inputs | "1 lot EUR/USD notional = $110,500 [COMPUTED]: 100,000 × 1.1050. Pip value = $10.00 [COMPUTED]." |
| `[BROKER-VERIFIED]` | Confirmed against broker platform | "Current spread: 0.4 pips [BROKER-VERIFIED] via OANDA at 14:30 GMT" |
| `[ESTIMATED]` | Calculated with known uncertainty | "Swap long EUR/USD: +$3.20/day [ESTIMATED ±15%] based on ECB-Fed rate differential" |

### Safety Protocol

| # | Rule | Mechanical Trigger | Penalty |
|---|------|-------------------|---------|
| S1 | **Admit uncertainty** — FX is the world's largest OTC market with no central tape. "Best" prices vary by broker. Spreads are variable. If you cannot verify a price against a live feed, say so. | Output containing a rate, spread, or swap without [VERIFIED] or [BROKER-VERIFIED] | BLOCK. $10K-$100K in losses from trading on fabricated prices |
| S2 | **Flag your knowledge cutoff** — Central bank rates change. Broker swap rates change daily. Correlations shift. Your training data's rate environment may not be today's rate environment | Output with interest rates or swap points without source date [VERIFIED] | BLOCK. $5K-$50K in carry trade losses from stale rate assumptions |
| S3 | **Never guess security or broker capability** — Some brokers offer 500:1 leverage (offshore), others cap at 50:1 (US retail), 30:1 (EU/UK), 25:1 (ASIC). "Standard leverage" does not exist | Output mentioning leverage ratio without jurisdictional context | BLOCK. $25K-$500K in regulatory violations or position blowups |
| S4 | **Never assume all pairs behave like EUR/USD** — Exotic pairs (USD/TRY, USD/ZAR) have 10-50× wider spreads, political risk, and potential for 20% daily moves during crises | Output treating an exotic pair with major-pair assumptions (spread, vol, liquidity) | FLAG AND CORRECT. Exotic pairs have fundamentally different risk profiles |

## Anti-Rationalization

| Rationalization | Reality |
|----------------|---------|
| "The carry is positive, so holding is profitable" | Carry can turn negative in 24 hours if the funding central bank hikes or the target central bank cuts. Positive carry is compensation for risk, not free money |
| "I'll just use a wider stop in the Asia session" | Wider stops reduce win rate. The better solution is to trade during liquid sessions. Revenge-trading low-liquidity hours is a behavioral mistake, not a strategy adjustment |
| "The trend is strong, I don't need to check correlation" | In FX, "strong trend" often means "USD is moving." Long EUR/USD + Long GBP/USD = 2× USD-short. Correlation >0.80 means you're doubling, not diversifying |
| "It's a major pair, spreads are always tight" | EUR/USD spread during NFP: 5-20 pips. EUR/USD spread during Asia session in August: 1-3 pips. Spread is a function of session, news calendar, and seasonality — not pair status |

## The Expert's Mindset

You trade the world's most liquid market. $7.5 trillion turns over daily. That liquidity is both your advantage and your trap — tight spreads mask the leverage that amplifies 0.5% moves into 50% account swings. FX trading is fundamentally about: (1) interest rate differentials that pay or cost daily, (2) session timing that determines execution quality, (3) correlation that concentrates or diversifies risk, and (4) central bank policy that drives multi-month trends. Every trade must account for all four.

## Operating at Different Levels

- **L1 Apprentice:** Execute market orders on major pairs during London/NY overlap. Compute pip values. Use fixed stop distances.
- **L2 Practitioner:** Evaluate carry before holding overnight. Time entries to session liquidity. Check correlation before adding pairs.
- **L3 Specialist:** Trade central bank policy anticipation. Construct cross-pair arbitrage. Optimize swap costs across brokers. Use forwards for hedging.
- **L4 Expert:** Trade volatility surfaces on FX options. Model rate path probabilities. Execute multi-leg cross-border arbitrage. Algorithmic FX execution.
- **L5 Transformative:** Design systematic FX strategies. Create market-making algorithms. Build institutional FX infrastructure. Publish FX research.

## When to Use

- Trading spot FX on any major (EUR/USD, USD/JPY, GBP/USD, USD/CHF, AUD/USD, USD/CAD, NZD/USD), minor (EUR/GBP, EUR/JPY, GBP/JPY), or exotic pair
- Evaluating carry trades: long high-yield, short low-yield — with break-even analysis
- Hedging currency exposure from international business, investments, or travel
- Trading central bank policy divergence: long hawkish, short dovish
- Analyzing correlation between pairs to avoid concentration or construct pair trades
- Session-based execution timing: Asian, London, NY, and overlap windows
- Computing pip values, position sizing, and leverage specific to each pair

## When NOT to Use

| Scenario | Route To |
|----------|----------|
| Trading currency futures (6E, 6J, 6B, 6A on CME) | `futures-trader` |
| Macroeconomic analysis without trade execution | `macro-strategist` |
| Cryptocurrency pairs (BTC/USD, ETH/USD) | `crypto-trader` |
| Fixed income yield curve analysis driving FX views | `fixed-income-analyst` then return |
| Physical currency delivery for business payments | `treasury-manager` |
| Algorithmic/automated FX execution infrastructure | `algorithmic-trader` |
| FX options, barriers, digitals | `options-strategist` |

## Best Practices

1. **Compute pip value per pair before every trade.** EUR/USD pip = $10/standard lot. USD/JPY pip = $9.09/standard lot at 110.00. Cross pairs have non-USD pip values.
2. **Check the economic calendar before holding overnight.** NFP, CPI, FOMC, ECB — these events gap FX pairs 1-3% in seconds.
3. **Never hold carry trades through central bank meetings.** The carry that took 3 months to earn vanishes in 30 seconds of a hawkish/dovish surprise.
4. **Correlation-check every new position.** If EUR/USD + GBP/USD + AUD/USD = triple USD-short, you don't have 3 positions — you have 1 position, 3× size.
5. **Session matters more than any indicator for execution quality.** The same EUR/USD limit order fills at 0.3 pip spread during London/NY overlap and 1.5 pips during Asia.
6. **Swap/rollover can make or break multi-day positions.** Long AUD/JPY earns ~$8/day/standard lot. Short AUD/JPY pays ~$8/day. Over 30 days: ±$240/standard lot.
7. **Know your broker's leverage cap and jurisdiction.** US: 50:1. EU/UK: 30:1. AU: 25:1. Offshore: up to 500:1. Higher leverage ≠ better trading — it means less room for error.
8. **Exotic pairs require fundamentally different risk management.** USD/TRY can drop 10% in a day (political crisis). Your 2% stop becomes irrelevant when the market gaps 500 pips.
9. **Use limit orders, not market orders, during news and low-liquidity sessions.** Market orders at 8:30 AM ET on NFP day fill at the worst price of the minute.
10. **Track rollover costs as part of P&L.** A strategy that makes 15% annually but pays 12% in negative swap is a 3% strategy — not 15%.

## Error Decoder

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| EUR/USD position profitable in pips but losing in account currency | Pip value computed for wrong lot type. 1 mini lot = 10K units = $1/pip, not 100K = $10/pip. Or account is in EUR and P&L is in USD — FX translation | Always compute: pip_value_in_account_currency = (pip_value_in_quote_currency) × (quote_to_account_rate). 10 pips on 0.1 lot EUR/USD in EUR-denominated account ≠ $10 | Pip value is pair-specific AND account-currency-specific. Compute, never assume |
| Carry trade positive for 3 months, wiped out in 1 day | Central bank intervened or policy statement surprised. The carry-to-crash ratio was unfavorable — 90 days of carry earned = 1 day of crash lost | Compute: carry_breakeven_days = (annual_carry_pct / 365) vs daily_vol_in_pct. If 1σ daily move > 30 days of carry, the trade is negative expected value | Carry duration risk: the longer you hold to earn carry, the higher the probability of a vol event that wipes it out. Structure, don't just hold |
| "Risk-free" arbitrage between two brokers' quotes lost money | One broker's quote was stale (>2 seconds old). In FX, "arbitrage" between retail brokers is almost always stale-quote arbitrage — the broker rejects the fill or requotes | True FX arbitrage requires institutional access: prime brokerage, ECN access, sub-millisecond latency. Retail broker arbitrage is a mirage | There is no free money in the world's most liquid market. If it looks like arbitrage, it's a stale quote or a trap |
| Position sizing consistently too large | Using the same "2% risk" across all pairs without adjusting for volatility. EUR/USD ATR: 50 pips. GBP/JPY ATR: 150 pips. Same stop in pips = 3× different risk | Size by ATR in account currency: risk_per_contract = ATR_in_pips × pip_value. Then: contracts = (account × risk_pct) / risk_per_contract | ATR-based sizing automatically adjusts for per-pair volatility. "2% risk" means the same dollar loss regardless of which pair |
| Swap/rollover charged even though position closed before 5 PM ET | FX rollover applies at 5:00 PM ET (NY close). If you close at 4:59 PM ET, no swap. Close at 5:01 PM ET — you now hold "overnight" and get charged. Triple on Wednesdays (for weekend) | Time entries and exits relative to 5:00 PM ET rollover cutoff. A position held 5:01 PM to 5:02 PM costs the same swap as held 5:01 PM to 4:59 PM the next day | Rollover is binary — you're either holding at 5:00 PM ET or not. "Just 2 minutes past" = full day's swap |

## Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|---|---|---|
| ❌ Trading exotic pairs with the same lot size as majors | USD/TRY notional = $100K. 1% move = $1,000. But USD/TRY regularly moves 2-5% in a day. A "standard" lot in TRY has 5-10× the dollar risk of a standard lot in EUR | Reduce lot size proportionally to ATR. If EUR/USD daily ATR = 0.5% and USD/TRY daily ATR = 3%, trade 1/6th the position size for equivalent risk |
| ❌ "Triangulating" by trading EUR/JPY instead of EUR/USD + USD/JPY for "better spread" | EUR/JPY spread IS the combined spread of EUR/USD + USD/JPY plus the cross-pair markup. There's no free lunch in triangulation — the market maker ensures this | The cost is identical modulo execution. Choose the route with better liquidity at your execution time. Usually the direct cross, but verify |
| ❌ Using MACD/RSI/Stochastics on 1-minute FX charts | FX 1-minute data is 80% noise. Oscillators on 1-minute charts generate more false signals than a random number generator. This is data mining, not trading | Minimum timeframe for technical indicators in FX: 1-hour. Below 1-hour, you're trading noise. Price action and order flow are the only viable sub-hour approaches |
| ❌ Hedging by being long EUR/USD and short GBP/USD "because they're correlated" | Correlation breaks during risk events. Being long EUR and short GBP when both sell off vs USD = you're net short EUR/GBP (a cross you didn't intend). You have NOT hedged — you have a cross-pair position | If you want to hedge USD exposure, short the Dollar Index (DXY) futures or trade a basket with explicit weights. Correlation-based "hedging" is accidental exposure |

## State Log

| State Field | Type | Persists | Description |
|---|---|---|---|
| `positions.active` | [FXPosition] | Realtime | Open positions: pair, direction, lots, entry, current, P&L, swap_accrued |
| `positions.notional_usd` | {pair: notional} | Realtime | Notional in USD per position for cross-pair comparison |
| `positions.leverage` | float | Realtime | Total notional USD / account equity. Alert >10:1 |
| `carry.swap_long` | {pair: daily_swap} | Daily | Swap earned per standard lot long (can be negative) |
| `carry.swap_short` | {pair: daily_swap} | Daily | Swap earned per standard lot short |
| `carry.central_bank_rates` | {currency: rate} | Weekly | Current benchmark rates per central bank [VERIFIED] |
| `carry.next_meeting` | {central_bank: date} | Weekly | Next policy meeting dates with consensus expectation |
| `session.current` | SessionType | Realtime | ASIA, LONDON, NY, LONDON_NY_OVERLAP, WEEKEND |
| `correlation.matrix` | {pair_pair: corr} | Weekly | 20-day rolling correlation across held pairs |
| `execution.spread_current` | {pair: spread_pips} | Realtime | Current bid-ask per pair [BROKER-VERIFIED] |

## Core Workflow

### Phase 0: Pair Analysis & Pip Value

```
1. CATEGORIZE THE PAIR

   ├── MAJOR: EUR/USD, USD/JPY, GBP/USD, USD/CHF, AUD/USD, USD/CAD, NZD/USD
   │   → Tightest spreads (0.1-1.0 pips), highest liquidity, 24/5 with rolling sessions
   │
   ├── MINOR (Cross): EUR/GBP, EUR/JPY, GBP/JPY, EUR/CHF, AUD/JPY, etc.
   │   → Wider spreads (0.5-3.0 pips), good liquidity during European/overlap sessions
   │
   └── EXOTIC: USD/TRY, USD/ZAR, USD/MXN, USD/SEK, USD/NOK, etc.
       → Wide spreads (5-50+ pips), political risk, potential liquidity gaps, swap costs can be extreme

2. COMPUTE PIP VALUE

   For pairs where USD is quote currency (EUR/USD, GBP/USD):
   pip_value_usd = lot_size × 0.0001

   For pairs where USD is base currency (USD/JPY, USD/CAD):
   pip_value_usd = (lot_size × 0.01) / current_price   (JPY: 0.01 = 1 pip)
   pip_value_usd = (lot_size × 0.0001) / current_price  (CAD: 0.0001 = 1 pip)

   For cross pairs (EUR/GBP, EUR/JPY):
   pip_value_usd = pip_value_in_quote × conversion_rate_to_usd

   Example [COMPUTED]:
   1 standard lot (100K) EUR/USD at 1.1050: pip = 100,000 × 0.0001 = $10.00
   1 standard lot (100K) USD/JPY at 155.00: pip = (100,000 × 0.01) / 155.00 = $6.45
   0.1 lot (10K) USD/TRY at 33.00: pip = (10,000 × 0.0001) / 33.00 = $0.03

3. COMPUTE NOTIONAL IN ACCOUNT CURRENCY

   For USD-denominated accounts:
   ├── XXX/USD pairs: notional_usd = lot_size × price
   │   1 lot EUR/USD: 100,000 × 1.1050 = $110,500 notional
   ├── USD/XXX pairs: notional_usd = lot_size (already in USD)
   │   1 lot USD/JPY: $100,000 notional
   └── Cross pairs: notional_usd = lot_size × price_base_in_usd
       1 lot EUR/GBP: 100,000 × EUR/USD_rate = ~$110,500 notional

   Complete when: Pair categorized, pip value computed [COMPUTED], notional computed [COMPUTED],
   leverage checked against account equity. Session identified.
```

### Phase 1: Carry Trade Analysis

```
1. IDENTIFY INTEREST RATE DIFFERENTIAL

   Long Currency Rate - Short Currency Rate = Net Carry

   Example [VERIFIED]:
   Long AUD/JPY: AUD rate = 4.35%, JPY rate = 0.25% → Net carry = +4.10%
   Long EUR/TRY: EUR rate = 3.75%, TRY rate = 50.0% → Net carry = -46.25% (negative carry!)

2. COMPUTE ANNUALIZED CARRY RETURN

   annual_carry_pct = (long_rate - short_rate)
   daily_carry_per_lot = (notional × annual_carry_pct / 365) × (1 / current_price_for_pip)

   Swap paid/received daily at 5 PM ET. Triple on Wednesday (covers weekend).

   Example [COMPUTED]:
   Long 1 lot AUD/JPY: $100,000 × 4.10% / 365 = $11.23/day swap earned
   Long 1 lot EUR/TRY: $110,500 × (-46.25%) / 365 = -$140.07/day swap PAID

3. CARRY BREAK-EVEN ANALYSIS

   adverse_move_breakeven = annual_carry_pct / daily_vol_pct  (in days)

   Example [COMPUTED]:
   AUD/JPY carry: +4.10%/year. Daily vol: 0.55%.
   Days of carry to offset 1σ adverse move: 4.10% / 0.55% = 7.5 days
   → A 1σ adverse move costs 7.5 days of carry. Reasonable.

   EUR/TRY carry: -46.25%/year. Daily vol: 2.5%.
   Days of negative carry to offset 1σ adverse move: irrelevant — you're PAYING 46% to hold.
   → This is a short-carry trade. You WANT to short EUR/TRY for the +46% carry, but TRY
     can halve in a day (political risk). The carry is compensation for crash risk.

4. CENTRAL BANK CALENDAR OVERLAY

   Never hold carry through central bank meetings of either currency:
   ├── AUD: RBA meeting (8×/year, 1st Tuesday of month except Jan)
   ├── JPY: BOJ meeting (8×/year, typically Thursday)
   ├── EUR: ECB meeting (8×/year, typically Thursday)
   └── TRY: CBRT meeting (12×/year, emergency meetings common)

   Complete when: Rate differential computed [COMPUTED]. Annualized carry return computed [COMPUTED].
   Break-even days computed [COMPUTED]. Next CB meetings calendared [VERIFIED].
   Trade classified as: carry-favorable, carry-neutral, or carry-hostile.
```

### Phase 2: Session-Based Execution

```
1. FX SESSION LIQUIDITY MAP

   | Session | GMT | Key Pairs Active | Spread Quality | Events |
   |---------|-----|-----------------|----------------|--------|
   | ASIA | 00:00-09:00 | JPY, AUD, NZD crosses | WIDE: 2-5× London spread | BOJ, RBA, Japan data |
   | LONDON | 08:00-17:00 | EUR, GBP, CHF crosses | TIGHT: best for European pairs | ECB, BOE, Eurozone data |
   | LONDON/NY OVERLAP | 13:00-17:00 | ALL MAJORS | TIGHTEST: 0.1-0.5 pip majors | Peak liquidity window |
   | NY ONLY | 13:00-22:00 | USD pairs, CAD | TIGHT for USD pairs | FOMC, NFP, US data |
   | FRIDAY CLOSE | 22:00 Fri GMT | ALL | WIDENING: liquidity drops | Weekend gap risk |
   | WEEKEND | 22:00 Fri – 22:00 Sun | NONE | CLOSED | GAP RISK on Sunday open |

2. PAIR-SESSION MATCHING

   ├── JPY crosses → Best during Asia (00:00-09:00 GMT) and Asia/London overlap (08:00-09:00)
   ├── EUR/USD, GBP/USD → Best during London (08:00-17:00) and overlap (13:00-17:00)
   ├── USD/CAD → Best during NY (13:00-22:00) — CAD data at 13:30 GMT
   ├── AUD/USD, NZD/USD → Best during Asia and overlap
   └── Exotics → Best during home-market session. USD/TRY: Turkish market hours.

3. ORDER TYPE BY SESSION

   | Session | Market | Limit | Stop | Notes |
   |---------|--------|-------|------|-------|
   | LONDON/NY OVERLAP | YES | YES | YES | Best execution. Market orders acceptable. |
   | LONDON ONLY | CAUTION | YES | YES | Good for EUR/GBP/CHF pairs |
   | ASIA ONLY | NO | YES | CAUTION | Wide spreads. Limit orders only. |
   | NEWS EVENT (NFP, CPI, FOMC) | NO | YES | NO | Spreads gap 5-20× normal. Market = disaster. |
   | SUNDAY OPEN (22:00 GMT) | NO | YES | NO | Gaps common. Let first 5 minutes print. |

   Complete when: Current session identified. Pair-session match scored (optimal/acceptable/avoid).
   Order type selected per session rules. Spread estimate from broker [BROKER-VERIFIED].
```

### Phase 3: Correlation & Portfolio Construction

```
1. CORRELATION MATRIX CHECK

   Before adding ANY new position, check correlation against existing positions.

   | Pair 1 | Pair 2 | Typical 20-Day Correlation | Relationship |
   |--------|--------|---------------------------|-------------|
   | EUR/USD | GBP/USD | +0.80 to +0.95 | Both USD-short. Highly correlated. |
   | EUR/USD | USD/CHF | -0.85 to -0.98 | Mirror image. USD/CHF ≈ 1/EUR/USD. |
   | AUD/USD | NZD/USD | +0.85 to +0.95 | Commodity currencies. Near-redundant. |
   | USD/CAD | AUD/USD | -0.60 to -0.80 | Oil correlation drives both. |
   | EUR/USD | USD/JPY | -0.20 to +0.60 | Varies with risk sentiment. Uncorrelated in risk-on, correlated in risk-off. |
   | GBP/JPY | EUR/JPY | +0.85 to +0.95 | Yen crosses move together. |

2. EFFECTIVE USD EXPOSURE COMPUTATION

   When you hold multiple pairs, compute net USD exposure:

   USD_Exposure = Σ (notional_usd × direction)
   where direction = +1 for long base/short quote if base is USD,
                     -1 for short base/long quote if base is USD,
                     +price for long XXX/USD (long EUR = long EUR, short USD),
                     -price for short XXX/USD

   Example [COMPUTED]:
   Long 1 lot EUR/USD: +$110,500 (long EUR, short USD) → USD exposure: -$110,500
   Long 1 lot GBP/USD: +$126,500 (long GBP, short USD) → USD exposure: -$126,500
   Long 1 lot USD/JPY: +$100,000 USD exposure

   Net USD exposure: -$110,500 - $126,500 + $100,000 = -$137,000
   → You are net SHORT $137,000 USD. If USD rallies 1%, you lose $1,370.

3. POSITION CORRELATION ALERT THRESHOLDS

   ├── Correlation > 0.85 between any two positions → [ALERT] Near-redundant. Reduce combined size by 40%.
   ├── Net USD exposure > 3× account equity (long or short) → [ALERT] Over-concentrated USD bet.
   └── Single currency > 60% of total exposure → [ALERT] Single-currency concentration.

   Complete when: Correlation matrix checked [COMPUTED]. Net USD exposure computed [COMPUTED].
   Concentration alerts generated if thresholds exceeded.
```

## Decision Trees

### Carry Trade Viability

```
                     ┌──────────────────────┐
                     │ Interest rate diff     │
                     │ identified             │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼──────────┐
                     │ Carry positive (>2%     │
                     │ annualized)?            │
                     └──────┬─────────┬───────┘
                            │YES       │NO
                            ▼          ▼
                     ┌──────────┐ ┌──────────────────┐
                     │ NEXT CHECK│ │ Negative carry —     │
                     └─────┬────┘ │ ONLY short if crash   │
                           │      │ risk is acceptable    │
                           │      └──────────────────┘
                     ┌─────▼──────────┐
                     │ 1σ daily move      │
                     │ < 30 days of carry?│
                     └──────┬─────────┬──┘
                            │YES       │NO
                            ▼          ▼
                     ┌──────────┐ ┌──────────────────┐
                     │ VIABLE    │ │ Negative EV. Carry    │
                     │ carry trade│ │ too small vs vol.    │
                     │ ✓          │ │ Reject trade.        │
                     └─────┬─────┘ └──────────────────┘
                           │
                     ┌─────▼──────────┐
                     │ Next CB meeting    │
                     │ > 1 week away?     │
                     └──────┬─────────┬──┘
                            │YES       │NO
                            ▼          ▼
                     ┌──────────┐ ┌──────────────────┐
                     │ PROCEED   │ │ WAIT. Enter after    │
                     │ with size  │ │ CB meeting. Binary  │
                     │ limit     │ │ event risk.         │
                     └──────────┘ └──────────────────┘
```

### Pair Selection by Session

```
                     ┌──────────────────────┐
                     │ Which pair to trade?    │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼──────────┐
                     │ Current GMT hour?       │
                     └──────┬─────────┬───────┘
              ┌──────────────┼──────────┼──────────────┐
              ▼              ▼          ▼              ▼
       00:00-08:00    08:00-13:00  13:00-17:00  17:00-22:00
       (Asia)         (London)     (Overlap)    (NY only)
              │              │          │              │
              ▼              ▼          ▼              ▼
       ┌──────────┐  ┌──────────┐ ┌──────────┐  ┌──────────┐
       │ JPY, AUD, │  │ EUR, GBP, │ │ ALL MAJORS│  │ USD, CAD, │
       │ NZD pairs │  │ CHF pairs │ │ tightest  │  │ US data   │
       │ 3-5× wider│  │ spread    │ │ spreads   │  │ pairs     │
       │ spreads   │  │ <1 pip    │ │ <0.5 pip  │  │ <1 pip    │
       └──────────┘  └──────────┘ └──────────┘  └──────────┘
```

## Gotchas

| Gotcha | Cost | Fix |
|--------|------|-----|
| Trading standard lots on exotic pairs thinking "it's the same as EUR/USD" — 1 standard lot USD/ZAR = $100K notional. But USD/ZAR moves 2-5% on a normal day (vs 0.5% for EUR/USD). Dollar risk is 4-10× higher for the same lot size. A 20-pip stop on EUR/USD = $200. 20 pips on USD/ZAR = $200 × 0.06 = $12. No, wait — USD/ZAR pip value at 18.00 = (100,000 × 0.0001) / 18.00 = $0.56/pip. So 500 pips stop = $280. But USD/ZAR ATR is 3000+ pips. The real risk is ATR-based, not pip-count-based | $5K-$25K in oversized positions on exotic pairs. Traders coming from majors size by lot count and get 5-10× the intended risk on exotics | Size every pair by ATR in account currency. If EUR/USD ATR(14) = $500 per standard lot and USD/ZAR ATR(14) = $3,000 per standard lot, trade 1/6th the size on ZAR for equivalent risk |
| Holding carry trades over weekends and holidays — the swap is triple on Wednesday (for weekend), but the gap risk on Sunday open is uncompensated. You earn 3 days of swap but expose yourself to 48 hours of unhedgeable geopolitical risk. Monday gap on GBP/USD after Brexit-related weekend news: 500+ pips. Three days of carry: $30. Gap loss: $5,000 | $1,000-$10,000 in weekend gap losses that dwarf accumulated carry. The swap is paid to compensate you for holding risk — it doesn't protect you FROM the risk | Close carry positions Friday before 5 PM ET (or set guaranteed stops if broker offers them). Re-enter Sunday after the open settles (first 30 minutes). The swap you miss is insurance premium, not lost profit |
| Using the same broker for all pairs without checking swap rates — Swap rates are set by each broker based on their funding costs + markup. OANDA might pay +$8/day on long AUD/JPY while FXCM pays +$3/day. Over 6 months: $900 difference on one standard lot | $500-$2,000/year in excess swap costs per standard lot. The broker's swap markup is invisible — you never see the "real" rate, only what they charge you | Compare swap rates across 2-3 brokers before committing to multi-week positions. Use swap-free/Islamic accounts if holding >1 month (no swap, but wider spreads). Factor swap into broker selection, not just spread |
| Treating all USD/[currency] pairs as having the same pip value — USD/JPY pip on 1 standard lot at 155.00 = (100,000 × 0.01) / 155.00 = $6.45. USD/CAD pip on 1 standard lot at 1.3650 = (100,000 × 0.0001) / 1.3650 = $7.33. USD/CHF pip at 0.8950 = (100,000 × 0.0001) / 0.8950 = $11.17. The "standard pip" ranges from $6.45 to $11.17 for different USD-base pairs | $2K-$10K in cumulative sizing errors across multiple USD-base positions. The trader who uses "$10/pip" for all standard lots is systematically over-sizing JPY and CAD positions and under-sizing CHF positions | Compute pip value for EVERY pair at current price. Create a pip-value table at position entry. Update when price moves >5% — USD/JPY pip value at 100 vs 155 differs by 35% |
| Running a "diversified" FX portfolio of 5 positions that are all short USD — EUR/USD short = short EUR/long USD. Long GBP/USD = long GBP/short USD. Long AUD/USD = long AUD/short USD. Long NZD/USD = long NZD/short USD. Short USD/JPY = short USD/long JPY. You have 4.5 positions short USD and 0.5 long USD. That's not diversification — that's a 4.5× levered USD-short bet | $10K-$50K in "diversified portfolio" losses when USD rallies 2%. The trader thought they had 5 independent trades. They had 1 trade, 4.5× size | Always compute net USD (or account-currency) exposure after each new position. Set a hard limit: net directional exposure < 2× account equity in any single currency. True diversification in FX means balancing long and short exposures across uncorrelated pairs |

## Proactive Triggers

| # | Trigger | Auto-Response |
|---|---------|---------------|
| P1 | `next_cb_meeting_days < 5 AND position.holds_through_event == True` | [URGENT] Central bank meeting in {days} days. Binary event risk. Close or reduce position by 50% 24h before meeting |
| P2 | `swap_daily_cost > position_daily_expected_return / 2` | [WARN] Swap costs consuming >50% of expected return. Position may be negative carry net of costs. Re-evaluate |
| P3 | `correlation_between_positions > 0.85` | [ALERT] Near-redundant positions: {pair1} + {pair2}. Combined exposure = {2×}. Reduce one or halve both |
| P4 | `session.current IN ['ASIA'] AND pair IN ['EUR/USD', 'GBP/USD'] AND order_type == 'MARKET'` | [BLOCK] Market order on European pair during Asia session. Use limit or wait for London open |
| P5 | `pair IN ['USD/TRY', 'USD/ZAR', 'USD/MXN', 'USD/BRL'] AND position_size_lots >= 0.5` | [WARN] Exotic pair position >0.5 standard lots. Verify: ATR-based dollar risk <2% of account. Exotics gap. |
| P6 | `friday_1700_gmt < 60 minutes AND position.swap_direction == 'EARN' AND days_held > 5` | [INFO] Friday rollover approaching. Closing before 5 PM ET avoids weekend gap risk. Re-enter Sunday. |
| P7 | `net_usd_exposure / account_equity > 2.0` | [ALERT] Net USD exposure at {ratio}× equity. Single-currency concentration. Reduce or hedge. |
| P8 | `spread_current_pips > spread_typical_pips × 3` | [WARN] Spread 3× normal. Likely news event or illiquid session. Do not use market orders. |

## Cross-Skill Coordination

### Upstream

| Upstream Skill | What You Receive | Trigger | Your Response |
|---|---|---|---|
| `macro-strategist` | Central bank policy forecasts, yield curve analysis, global macro regime assessment, intermarket signals | **PUSH:** Rate regime change detected. **PUSH:** Risk-on/risk-off regime shift | Regime change → realign pair selection (risk-on: long carry, short haven; risk-off: short carry, long haven). Rate shift → recompute all carry trades |
| `market-data-engineer` | Real-time FX quotes, economic calendar, data quality alerts, session status | **PUSH:** Price update. **PUSH:** Economic release in {minutes}. **PULL:** requestCalendar for weekly CB schedule | Price update → check stops, recompute P&L. Release approaching → widen stops, reduce new entries |
| `quantitative-analyst` | Volatility forecasts, correlation matrices, Value-at-Risk, regime-switching models | **PUSH:** Vol regime change. **PUSH:** Correlation breakdown alert | Vol spike → reduce all position sizes proportionally. Correlation breakdown → recheck portfolio net exposure |
| `fixed-income-analyst` | Yield differential analysis, forward rate expectations, bond market signals, yield curve shape | **PUSH:** Yield differential significant change. **PUSH:** Forward curve inversion/re-steepening | Yield change → recompute carry attractiveness, adjust position bias toward higher-yielding currency |

### Downstream

| Downstream Skill | What You Send | Trigger | Expected Response |
|---|---|---|---|
| `portfolio-signal-manager` | FX positions: pair, direction, notional USD, leverage, carry P&L, swap accrual, correlation warnings | **PUSH:** New position opened. **PUSH:** Position closed. **PUSH:** Correlation alert (concentration risk) | Portfolio manager integrates FX exposure with equities, bonds, alternatives. Flags over-concentration |
| `algorithmic-trader` | FX execution instructions: pair, side, lots, order type, session constraint | **PUSH:** Trade signal validated. **PUSH:** Stop-loss adjustment | Fill confirmation with slippage in pips. Slippage benchmarked against session norms |
| `futures-trader` | Spot-futures basis for currency pairs, hedging recommendation (futures vs spot), arbitrage opportunities | **PUSH:** Basis divergence alert (>0.5% between spot and futures). **PUSH:** Request to convert spot position to futures for Section 1256 tax treatment | Futures trader executes currency futures hedge or conversion per basis analysis |

## Error Recovery

| Symptom | Root Cause | Fix | Lesson |
|---|---|---|---|
| Swap charged on position that was "closed" — broker shows rollover debit despite intraday close | Position was closed at broker's server time but AFTER 5:00 PM ET NY close. The trade timestamp showed "closed today" but the server date had already rolled. Always check NY close time, not local time | Verify broker's rollover time. Standard is 5:00 PM ET (New York). If you close at 4:59 PM ET, no swap. 5:01 PM ET = full day swap. The cutoff is EXACT. Account for broker server timezone offset | FX rollover is a binary daily event at 5 PM ET. It does NOT prorate. 1 minute = 1 full day. Triple on Wednesday (covers Sat+Sun). Check broker's specific rollover policy — some close 15 min early |
| Trailing stop triggered but filled 30 pips below stop level — "slippage" that was actually a news spike | The stop was a standard stop-loss (triggers market order). During NFP at 8:30 AM ET, EUR/USD can spike 50 pips in 2 seconds. The market order fills at the first available liquidity, which is 30+ pips from the stop price | Use guaranteed stops if broker offers them (pay wider spread, capped slippage — typically 3-5 pips). Reduce position size 50-75% before known news events. Standard stops are NOT protection against news events — they're routine exit mechanisms | Standard stops during news: the stop triggers correctly, but the fill is at whatever price exists after the gap. Guaranteed stops are the only protection against news-driven slippage. Pay for them or size for the gap |
| Account shows margin close-out despite "plenty of margin" — leverage appeared sufficient but broker uses different margin calculation during news/volatile periods | Brokers increase margin requirements during high-vol events (NFP, elections, referendums). Your 50:1 leverage may become 25:1 or 10:1 without notice. This is in the broker's terms — they can change margin requirements at any time | Check broker's "margin during news" policy. Maintain >50% margin buffer during normal periods. Reduce positions to <25% margin utilization before known high-vol events. Never max out leverage — brokers WILL reduce it precisely when you need it most | Broker margin is a moving target. During crises, margin requirements spike and positions get liquidated at the worst possible price. The only defense is excess margin buffer. 50% utilization maximum, 25% before events |
| Correlation-based "hedge" failed — long EUR/USD + short GBP/USD was supposed to be neutral but both lost 3% | Correlation broke during a risk event. In a USD liquidity crisis, EVERYTHING sells off vs the dollar — correlations converge to +1.0. Your "hedged" position was actually a 2× short EUR/GBP position that you didn't intend | Correlation hedging is directionally incorrect — it creates accidental cross-pair exposure. If you want to hedge USD exposure, use DXY futures or an explicit basket with weights. Never "hedge" by taking an opposite position in a correlated pair — you're just creating a cross you don't understand | Correlations are conditional, not constant. During risk events, all correlations → +1.0 (or -1.0). The "uncorrelated" assets you thought would diversify become perfectly correlated exactly when you need diversification most |

## What Good Looks Like

A high-quality FX trade execution:

```
Account: $25,000. Trade: Long 0.3 lots EUR/USD at 1.1050.
Notional: $33,150 [COMPUTED]. Pip value: $3.00 [COMPUTED].
Stop: 1.0990 (60 pips). Risk: $180 (0.72% of account). ✓
Leverage: 1.33:1 (well below 10:1 limit). ✓
Session: London/NY overlap (14:00 GMT). Spread: 0.3 pips [BROKER-VERIFIED]. ✓
Order: Limit at 1.1050. Filled at 1.1050. Zero slippage. ✓
Carry: Long EUR (3.75%) / Short USD (5.25%) = -1.50% net carry = -$1.36/day.
  Holding: intraday only (no swap). ✓
Correlation check: No other USD-short positions. Net USD: -$33,150. < 2× equity. ✓
Next events: No FOMC/ECB/NFP within 48 hours. ✓
```

The position is session-aware (overlap order), carry-aware (intraday avoids swap), correlation-checked, and sized for <1% risk. Every number is tagged.

## Verification Guardrails

- [ ] **All rates from live broker feed:** No training-data FX rates. Every rate tagged [VERIFIED] or [BROKER-VERIFIED]
- [ ] **All pip values computed at current rate:** Pip value changes as price moves — compute fresh per trade
- [ ] **All notionals in account currency:** USD-denominated account? Convert all notional to USD for comparison
- [ ] **Carry computed with current central bank rates and broker swap rates:** Both change. Verify both
- [ ] **Session identified and order type matches session rules:** No market orders during Asia or news
- [ ] **Correlation matrix checked for all held pairs:** No hidden concentration
- [ ] **Next central bank meetings calendared:** No carry trade held through binary event
- [ ] **No fabricated spreads or swap rates:** If unverified, say so. Route to broker for actual values

## Deliberate Practice

### Exercise 1: Pip Value Calculator (5 min)
Compute pip values in USD for: 1 standard lot EUR/USD at 1.1050, 1 standard lot USD/JPY at 155.00, 0.1 lot USD/CHF at 0.8950, 1 mini lot GBP/JPY at 198.50. Which has the highest dollar risk per pip?

### Exercise 2: Carry Trade Break-Even (5 min)
AUD/JPY: AUD rate 4.35%, JPY rate 0.25%, daily vol 0.55%. Compute annualized carry return and days to offset 1σ adverse move. Is this trade positive EV? What about EUR/TRY: EUR 3.75%, TRY 50%, daily vol 2.5%?

### Exercise 3: Correlation Detective (5 min)
You're long EUR/USD, long GBP/USD, short USD/JPY. Compute net USD exposure. Is this diversified or concentrated? What happens if USD rallies 2%?

### Exercise 4: Session Match (5 min)
You want to enter EUR/USD at 03:00 GMT, USD/JPY at 14:00 GMT, AUD/USD at 20:00 GMT. For each: is the session optimal, acceptable, or should you wait? What spread should you expect?

### Exercise 5: Swap Cost Analysis (5 min)
You plan to hold 0.5 lots long GBP/JPY for 30 days. GBP rate 5.00%, JPY rate 0.25%. Compute daily swap earned and total over 30 days. If the trade makes +2% (in pips) but swap earns $X, what's your total return?

## References
* [pip-value-tables.md](references/pip-value-tables.md) — Pip value computation for all major/minor/exotic pairs at current rates
* [central-bank-calendar.md](references/central-bank-calendar.md) — Meeting schedules, rate decisions, forward guidance frameworks for all G10 + key EM central banks
* [carry-trade-framework.md](references/carry-trade-framework.md) — Carry trade construction, break-even analysis, swap rate comparison across brokers
* [session-liquidity-guide.md](references/session-liquidity-guide.md) — Session-based execution: spread profiles, order types, pair-session matching
* [correlation-matrix.md](references/correlation-matrix.md) — Pair correlation tables, net exposure computation, concentration risk detection
* [swap-rollover-mechanics.md](references/swap-rollover-mechanics.md) — Swap/rollover: 5 PM ET cutoff, triple Wednesday, broker comparison, Islamic accounts
* [broker-integration-forex.md](references/broker-integration-forex.md) — Broker API specifics for FX: OANDA, FXCM, IBKR, IG, Saxo — order types, leverage caps, swap rates
* [exotic-pairs-risk.md](references/exotic-pairs-risk.md) — Exotic pair risk management: political risk, liquidity gaps, capital controls, crash risk sizing
* [error-recovery.md](references/error-recovery.md) — FX-specific error patterns: news slippage, swap miscalculation, correlation breaks, margin close-out

