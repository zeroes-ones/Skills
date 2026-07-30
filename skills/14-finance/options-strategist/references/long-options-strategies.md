# Long Options Strategies

## Purpose
Comprehensive reference for LONG (debit) options strategies — the complement to the short-premium strategies (iron condors, credit spreads, CSPs) covered in other references. This file covers directional long positions (calls/puts), defined-risk debit spreads (bull call / bear put spreads), and volatility/event-driven long structures (straddles, strangles, backspreads). Every strategy here is net-long premium: you pay a debit, your risk is defined, and your edge comes from buying cheap insurance (low IV) or anticipating large directional moves.

> **Core principle:** BUY premium when IV is LOW (you're buying cheap insurance). SELL premium when IV is HIGH (you're selling expensive insurance). Never buy options with IV Rank > 50. Never sell options with IV Rank < 25. [COMMON-PRACTICE]

---

## A. Long Calls — Directional Bullish

### When to Use
- Strong bullish UOA (buying calls at ask, sweeps) + IV Rank < 30 (cheap premium) + clear catalyst (earnings, product launch, FDA approval)
- Conviction must be HIGH — outright calls have ~35-45% POP, so you need 2:1+ reward/risk to justify the low win rate

### Construction
- Strike: ATM or slightly OTM (0.50–0.70 delta for high conviction, 0.30–0.50 delta for lower conviction)
- DTE: 30–60 minimum (avoid theta bleed). 60–90 DTE optimal for swing trades
- Sizing: Max loss (total debit) ≤ 2% of portfolio

### Risk Profile
- **Max loss:** 100% of premium paid (defined risk)
- **POP:** Typically 35–45% [ESTIMATED ±5%]
- **Breakeven at expiration:** Strike + Premium Paid

### Profit Target
- **Minimum target:** +100% of debit (need 2:1 reward/risk to compensate for low POP)
- **Scale-out plan:** Close 50% at +100%, let 50% run with trailing stop at +50% from entry

### Stop-Loss
- **Hard stop:** -50% of premium. If the move isn't happening by -50%, the thesis is broken
- **Time stop:** If not at +30% profit by 21 DTE, close. Theta acceleration makes recovery unlikely

### UOA Integration
- UOA buying calls at ask ($1M+ notional) = confirmation → enter trade
- UOA selling calls = fade or skip → the smart money disagrees with your direction
- UOA neutral = rely on technicals and IV alone

### [VERIFIED] Mechanics
- Call delta ranges from 0 (far OTM) to 1.0 (deep ITM). ATM calls have ~0.50 delta at entry
- Gamma is highest ATM and accelerates in final 21 DTE — your delta changes fastest when you can least afford surprises
- Vega works FOR you: if IV rises after entry, the call gains value even without stock movement
- Theta works AGAINST you: every day the stock doesn't move, time decay erodes your premium
- [VERIFIED] A 30 DTE ATM call loses ~2% of its premium per day to theta in the final week. A 60 DTE call loses ~0.5%/day in weeks 4-6. Longer DTE = slower theta bleed.

---

## B. Long Puts — Directional Bearish

### When to Use
- Bearish UOA (put buying at ask > $1M notional) + IV Rank < 30 + technical breakdown (below 50-SMA, bearish MACD cross, breakdown from support)
- Catalyst: earnings disappointment expected, sector rotation, macro headwind

### Construction
- Strike: ATM or slightly OTM (0.50–0.70 delta high conviction, 0.30–0.50 delta lower)
- DTE: 30–60 minimum. Big drops happen fast but timing is hard — give yourself runway

### Risk Profile
- **Max loss:** 100% of premium paid (defined risk)
- **Breakeven at expiration:** Strike − Premium Paid

### Profit Target
- **Minimum target:** +150% of debit. Stocks drop faster than they rally (panic > greed), so the asymmetric payout must be larger
- **Scale-out:** Close 50% at +150%, let 50% run with trailing stop at +75%

### Stop-Loss
- -50% of premium. Stock rallies above your entry trigger level → thesis broken

### Special Consideration: Volatility Skew
- OTM puts are structurally more expensive than equidistant OTM calls (volatility skew/smile)
- [VERIFIED] For a typical large-cap stock, a 5% OTM put trades at IV ~2-4 points higher than a 5% OTM call
- This means put buyers pay a "crash premium" embedded in the skew — the IV Rank filter (< 30) is even MORE critical for puts than calls
- If IV Rank is 35-45 and you MUST express bearishness, use a bear put debit spread instead (sell the cheaper OTM put to offset the skew premium)

---

## C. Bull Call Debit Spreads — Defined Risk Bullish

### When to Use
- Moderate bullish UOA + IV Rank 30-50 + want defined risk cheaper than outright calls
- Lower cost than outright calls, higher POP, but capped upside

### Construction
- Buy lower-strike call (ATM or slightly ITM), Sell higher-strike OTM call
- Width: 5-10 points (1-3% of underlying price). Same expiration, same number of contracts
- Example: Buy $430 call, Sell $450 call on $420 stock → $20-wide spread

### P&L Metrics
| Metric | Formula |
|--------|---------|
| Max Profit | (Short Strike − Long Strike) − Debit Paid |
| Max Loss | Debit Paid |
| Breakeven | Long Strike + Debit Paid |
| POP | ~40-50% [ESTIMATED ±5%] |

### Profit Target
- **50% of max profit:** Scale out 50% of position. Remaining 50% of max requires doubling the gain — high marginal risk
- **75% of max profit:** Close remaining. The last 25% of max profit carries disproportionate gamma/time risk

### Stop-Loss
- 100% of debit (max loss accepted) OR underlying breaks technical support level (20-EMA or 50-SMA), whichever triggers first

### Key Advantage Over Credit Spreads
- Works better in LOW IV environments (Rank < 35). Credit spreads need elevated IV to collect worthwhile premium
- Vega is net long — rising IV helps your position (credit spreads are net short vega)

### [VERIFIED] Commission Note
- Two legs = $1.30 round-trip per spread at $0.65/contract. On a $10-wide spread with $4.00 debit: commission = 0.33% of max loss. On narrow ($2.50-wide) spreads, commission drag can exceed 1% — use $5+ wide minimum.

---

## D. Bear Put Debit Spreads — Defined Risk Bearish

### When to Use
- Bearish UOA + IV Rank 30-50 + want lower cost and higher POP than outright puts
- Mitigates the volatility skew problem: the sold OTM put offsets the inflated premium on the long put

### Construction
- Buy higher-strike put (ATM), Sell lower-strike OTM put
- Width: 5-10 points. Same expiration, same contracts

### P&L Metrics
| Metric | Formula |
|--------|---------|
| Max Profit | (Long Strike − Short Strike) − Debit Paid |
| Max Loss | Debit Paid |
| Breakeven | Long Strike − Debit Paid |

### Profit Target
- 50% scale out, 75% close remaining (same logic as bull call spreads)

### Stop-Loss
- 100% of debit OR underlying breaks above resistance (50-SMA, prior support-turned-resistance)

### Volatility Skew Advantage
- The short OTM put captures the elevated IV from put skew, partially offsetting the inflated cost of the long put
- [ESTIMATED ±10%] A bear put spread typically costs 10-15% less (as % of width) than an equivalent-distance bull call spread, all else equal, due to put skew providing richer premium on the short leg

---

## E. Long Straddle — Volatility/Event Play

### When to Use
- Earnings, FDA decision, binary event, major macro announcement + IV Rank < 40 (cheap enough to buy)
- Expectation: the stock will move significantly in EITHER direction, but direction is unknown
- **Critical filter:** The expected move (straddle price) must be SMALLER than the move you anticipate

### Construction
- Buy ATM call + ATM put, same expiration. Typically 5-10 DTE past the event date
- Example: Stock at $100, buy $100 call + $100 put. Total debit: $8.00. Breakevens: $108 and $92

### Risk Profile
- **Max loss:** Total premium paid (call + put) — 100% defined
- **POP:** ~30-35% [ESTIMATED ±5%]
- **Breakevens:** Strike ± Total Debit

### Profit Target
- **+100% minimum.** The breakeven is wide — need a BIG move. A straddle that returns +50% is a "win" but below target
- At +100%, close 50%. At +150%, close remaining. If the move is massive (+200%+), let a runner ride

### Stop-Loss
- -50% of total debit if no significant move by 2 days post-event
- The IV crush post-event is 60-80% of the pre-event volatility premium — after that, time decay dominates

### [VERIFIED] IV Crush Dynamics
- Post-earnings, IV typically drops 60-80% from pre-announcement levels
- [VERIFIED] For a stock with IV Rank 35 pre-earnings: the ATM straddle IV might be 45 (event-inflated). Post-earnings, IV reverts to ~20-25. The vega loss on a straddle is approximately: vega × IV drop × 100. With vega ~0.10 per leg: total loss ~$400-600 from IV crush alone, before any stock movement
- This is why IV Rank < 40 is critical: if IV Rank is already 60+, the post-event crush is even more devastating

### Common Mistakes
1. Buying straddles with IV Rank > 60 — IV crush destroys you even if the stock moves
2. Buying too close to expiration — no time for the move to develop; theta is brutal
3. Sizing too large — straddles have low POP; they're event plays, not portfolio cornerstones

---

## F. Long Strangle — Cheaper Volatility Play

### When to Use
- Same scenario as straddle (binary event, unknown direction) but want lower cost and are willing to accept wider breakevens
- Better when the expected move is large enough to justify the wider profit zone

### Construction
- Buy OTM call (0.25 delta) + OTM put (0.25 delta). Costs ~50-60% of an equivalent straddle
- Example: Stock at $100. Buy $105 call ($2.50) + $95 put ($2.50). Total debit: $5.00 (vs. $8.00 straddle)
- Breakevens: $110 upside, $90 downside (wider than straddle's $108/$92)

### Risk Profile
- **Max loss:** Total debit (lower than straddle, lower dollar risk)
- **POP:** ~25-35% [ESTIMATED ±5%] — lower than straddle due to wider breakevens
- **Breakevens:** Call Strike + Total Debit AND Put Strike − Total Debit

### Profit Target
- +150% minimum (lower cost = need higher % return to justify the lower POP)
- At +150%, close 50%. At +200%, close remaining

---

## G. Call/Put Backspreads — Leveraged Directional

### When to Use
- Strong directional conviction + IV is low to moderate (< 40) + expect a large, sustained move
- Higher confidence than a simple long call/put because you're financing the long legs

### Construction (Call Backspread — Bullish)
- Sell 1 ATM call, Buy 2 OTM calls (ratio 1:2). Net credit or small debit
- Example: Stock at $100. Sell 1 $100 call at $5.00, Buy 2 $110 calls at $1.50 each ($3.00 total). Net credit: $2.00
- If stock stays below $100: keep $2.00 credit. If stock rockets to $130: short call loses $30, long calls worth $40 ($20 × 2). Net: $40 − $30 + $2.00 = $12.00 profit

### Construction (Put Backspread — Bearish)
- Sell 1 ATM put, Buy 2 OTM puts (ratio 1:2). Net credit or small debit

### Risk Profile
- **If net credit:** Zero risk to upside (call backspread) or downside (put backspread). Risk is on the "wrong direction" between the strikes
- **If net debit:** Risk is the debit paid
- **Maximum risk zone:** Stock pins at the long strike at expiration — short leg is ITM, long legs expire worthless. This is the "valley of death"
- **Upside:** UNLIMITED on the long legs beyond the long strike

### [ESTIMATED ±15%] Backspread Performance
- Backspreads work best when IV is low (cheap to buy the OTM legs) and a large move is expected
- The "valley of death" at the long strike is the primary risk. The sold ATM option caps your gain between the strikes
- Optimal when you expect a 10%+ move — backspreads need a big move to overcome the drag of the short leg

---

## H. Long vs. Short Strategy Selection Matrix

### The Fundamental Decision: Buy or Sell Premium?

| Market Condition | IV Rank | Direction | LONG Strategy | SHORT Strategy |
|-----------------|---------|-----------|---------------|----------------|
| Bullish | < 30 | Up | Long Call, Bull Call Debit Spread | N/A (premium too cheap to sell) |
| Bullish | 30-50 | Up | Bull Call Debit Spread | Bull Put Credit Spread |
| Bullish | > 50 | Up | N/A (premium too expensive to buy) | Bull Put Credit Spread, Naked Put |
| Bearish | < 30 | Down | Long Put, Bear Put Debit Spread | N/A |
| Bearish | 30-50 | Down | Bear Put Debit Spread | Bear Call Credit Spread |
| Bearish | > 50 | Down | N/A | Bear Call Credit Spread, Naked Call |
| Neutral/Event | < 40 | Either | Long Straddle, Long Strangle | N/A |
| Neutral | > 50 | None | N/A | Iron Condor, Short Strangle |
| Neutral | 30-50 | None | Long Butterfly, Long Calendar | Short Butterfly, Short Calendar |
| Bullish (strong) | < 40 | Big Up | Call Backspread | N/A |
| Bearish (strong) | < 40 | Big Down | Put Backspread | N/A |

### Quick Decision Rule
1. **IV Rank < 30:** You are BUYING premium. Select from LONG column only.
2. **IV Rank 30-50:** Both viable. Debit spreads for higher conviction, credit spreads for moderate conviction.
3. **IV Rank > 50:** You are SELLING premium. Select from SHORT column only.
4. **IV Rank > 75:** Aggressive premium selling only. Never buy options here unless hedging a specific, imminent risk.

### The "Never" Rules
- **Never buy options (calls/puts/straddles) with IV Rank > 50** — you're overpaying for volatility that will mean-revert
- **Never sell options (credit spreads, iron condors, CSPs) with IV Rank < 25** — you're selling cheap insurance; one adverse move wipes out 10 trades of tiny premium
- **Never buy straddles/strangles into earnings with IV Rank > 40** — IV crush guarantees a loss unless the move is extraordinary
- **Never hold long options through expiration** — close by 21 DTE minimum. Theta acceleration in final 21 days is brutal on long premium positions

---

## Anti-Hallucination Section

### Knowledge Confidence Levels
- **[VERIFIED]:** Statements backed by public data, exchange rules, or widely published research. These are facts about options mechanics (delta ranges, expiration processes, IV crush magnitude).
- **[COMPUTED]:** Numbers derived from established formulas (breakeven = strike ± premium, max profit = width − debit). These are mathematically certain given the inputs.
- **[ESTIMATED ±X%]:** Approximations based on market microstructure knowledge and common practice. Actual values vary by underlying, market regime, and liquidity conditions.
- **[COMMON-PRACTICE]:** Widely accepted among options traders but not formally published. Rules of thumb with collective practitioner validation.

### What This File Does NOT Cover
- Options pricing models (Black-Scholes, binomial trees) — route to quantitative-analyst
- Greeks computation from first principles — route to quantitative-analyst
- Trade execution, order routing, or broker-specific mechanics
- Portfolio-level risk management or margin calculations
- Tax implications of options trading

### Knowledge Cutoff
The strategy descriptions and market behaviors in this file are based on principles that are timeless (volatility mean-reversion, theta decay, probability distributions), but specific market conditions, IV rank thresholds, and ticker-level behavior can shift with regime changes. Always validate current IV Rank, options liquidity (bid-ask spread, open interest), and event calendar before deploying any strategy.

### Never Guess
If asked for a strategy recommendation on a ticker not analyzed, or for a backtest not run, state: "I don't have data on that ticker/setup. I can describe the strategy framework, but I cannot validate its application to this specific case without running the analysis." Never fabricate price data, IV values, or trade outcomes.

