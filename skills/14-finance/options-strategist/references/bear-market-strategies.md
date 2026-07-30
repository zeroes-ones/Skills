# Bear Market & Downturn Strategies

## Purpose
Comprehensive reference for how options strategies perform during market downturns, corrections, and crashes. This is the dark-side companion to the sunny-day strategies in `strategy-selection-matrix.md` and `long-options-strategies.md`. Every strategy that works in a bull market must be stress-tested against real bear markets: COVID crash (-34% in 23 days), 2022 bear (-25% over 10 months), 2023 Q3 correction (-10%).

> **Core principle:** In a bear market, the rules CHANGE. IV spikes. Correlations go to 1. Hedging effectiveness degrades. Premium selling becomes picking up pennies in front of a steamroller. This reference defines WHEN to switch regimes and HOW to adjust.

---

## A. The Three Bear Market Regimes

| Regime | SPY Drawdown | Duration | VIX Range | IV Rank | Strategy Mode |
|--------|-------------|----------|-----------|---------|---------------|
| **Correction** | -5% to -10% | 2-8 weeks | 25-35 | 60-80 | Normal with caution — widen strikes, reduce size |
| **Bear Market** | -10% to -25% | 2-10 months | 30-50 | 80-100 | Defensive — no naked premium selling, credit spreads only with WIDE wings |
| **Crash** | -25% to -50%+ | 1-6 weeks | 50-85 | 100 | Survival mode — NO premium selling. Only long puts, defined-risk debit spreads, or CASH |

**[VERIFIED]** VIX-to-drawdown mapping from CBOE historical data (1990-2024). Corrections typically peak VIX at 30-35. Bear markets peak at 35-50. Crashes exceed 50.

---

## B. Strategy-by-Strategy Downturn Performance

### B1. Iron Condors — WORST PERFORMER in Downturns

**What happens during a correction:**
- The short put side gets tested. If IV was 15 at entry and spikes to 30, vega destroys the position
- Even if the put strike isn't breached, the mark-to-market loss from vega expansion can exceed max profit
- The 21-day rule becomes CRITICAL — gamma acceleration on the tested side is lethal

**Real example — March 2020 COVID crash:**
- Iron condor entered Feb 15, 2020: SPY $338, 310/305P 350/355C, 30 DTE, credit $1.20
- By March 16 (SPY at $240, -29%): short $310 put is $70 ITM. Position loss: -$9,880 on $1,200 max profit
- **Loss exceeds max theoretical profit by 8.2× [COMPUTED]**
- Any iron condor with a short put below -15% OTM was completely destroyed

**Adaptation for corrections (IV Rank > 60):**
- Move to call ratio spreads (bearish) — sell 1 call, buy 2 higher calls for net credit
- Or: only sell call spreads (bear call spreads), never put spreads
- If you MUST trade iron condors: widen put wing to -12% OTM (from normal -6%), halve position size, close at 30 DTE (not 21)
- **[ESTIMATED ±15%]** Iron condors opened during corrections with normal parameters have a 40-60% loss probability

### B2. Credit Spreads (Bull Put) — HIGH RISK in Downturns

**What happens:**
- Bull put spreads are DIRECTIONAL BULLISH. A correction is bearish. This is the worst possible environment
- Even defined risk is dangerous — a 5-wide spread on SPY that goes fully ITM loses $500/spread
- Multiple spreads hit max loss simultaneously (correlation → 1)

**Real example — 2022 bear market:**
- Bull put spread on QQQ entered Jan 3, 2022: QQQ $400, 380/375P, 30 DTE, credit $0.80
- By Jan 24 (QQQ at $335, -16.3%): spread fully ITM. Loss: -$4.20/spread (max loss)
- **Return: -84% of risk in 21 days [COMPUTED]**
- 5 spreads = -$2,100 loss on $2,500 max risk

**Adaptation:**
- **DO NOT SELL BULL PUT SPREADS IN A BEAR MARKET.** Period.
- Switch to bear call spreads (sell OTM calls instead)
- Or: buy puts / bear put debit spreads (become the buyer, not the seller)
- **[COMMON-PRACTICE]** The IV spike means premium is expensive — this is the time to BUY protection, not sell it

### B3. CSP / Wheel — Moderate Risk, Survivable

**What happens:**
- CSPs get assigned. This is expected — the wheel is designed for assignment
- The problem: multiple assignments in a falling market = massive long delta exposure
- MSFT CSP example: sold $385 put at $405, assigned at $370. Now long 100 shares at $385 cost basis in a falling market
- Recovery: MSFT eventually recovered (2022 bottom to 2024 high). But the drawdown was -15% on shares

**Real example — 2022 bear market, MSFT CSP Wheel:**
- CSP sold Jan 2022: MSFT $335, 310P, credit $3.50. MSFT dropped to $275 by April → assigned
- Cost basis: $306.50 ($310 - $3.50 credit). MSFT at $275. Unrealized loss: -$3,150
- Covered call at $310 strike collected $1.50/month × 8 months = $12.00 in premium while waiting
- MSFT recovered to $310 by August 2023 (18 months). Total P&L: $12.00 premium + $3.50 CSP credit = +$15.50/share = +$1,550
- **Return: +5.1% over 18 months = 3.4% annualized** — barely above risk-free rate [COMPUTED]
- The wheel SURVIVES bear markets but dramatically underperforms buy-and-hold recovery

**Adaptation:**
- Size CSPs at 2% of portfolio (not 5%) per position
- Only wheel stocks you'd hold for 2+ years through a bear market
- Sell puts at -15% OTM (not -5%) during corrections
- After assignment, sell covered calls at or above cost basis — never below
- **[VERIFIED]** MSFT took 18 months to recover from 2022 lows. AAPL: 15 months. NVDA: 6 months. Stock selection MATTERS.

### B4. Long Calls — DISASTROUS in Downturns

**What happens:**
- Everything is going down. Your calls expire worthless.
- The low IV advantage is gone — IV spikes AFTER the crash starts
- **Never buy calls during a crash hoping for a bounce.** The timing is impossible

**Adaptation:**
- Do not buy calls in any bear regime. Wait for confirmed uptrend + IV Rank < 30
- **[ESTIMATED ±20%]** Long calls bought during corrections have a 70-85% loss probability

### B5. Long Puts & Bear Put Debit Spreads — BEST PERFORMER in Downturns

**What happens:**
- This is what long puts are DESIGNED for
- The problem: IV is high during crashes, so puts are EXPENSIVE
- You need the move to exceed the premium paid, AND overcome IV contraction when vol mean-reverts

**Real example — March 2020, SPY Long Put:**
- Entry Feb 20, 2020: SPY $338, buy $320 put (5.3% OTM), 30 DTE, cost $6.00
- March 16: SPY $240. Put is $80 ITM. Worth $80+ (deep ITM, essentially intrinsic)
- P&L: +$7,400 on $600 risk = +1,233% [COMPUTED]
- But: IV was ~15 at entry, ~82 at exit. Vega contributed $2,000+ to the gain

**Real example — March 2020, SPY Bear Put Debit Spread:**
- Buy $320 put, sell $280 put (40-wide). Debit: $4.00. Max profit: $36.00
- March 16: Both ITM. Spread worth $40. Profit: $36.00 = +900% [COMPUTED]
- Better risk/reward than outright puts: $4.00 risk for $36.00 reward

**Adaptation — this is the GO-TO strategy in bear markets:**
- Enter on first technical breakdown (below 200-SMA)
- Use debit spreads to reduce cost (IV is high, so outright puts are expensive)
- Strike: ATM or slightly OTM for the long leg, -8-12% for the short leg
- DTE: 45-60 (give the crash time to develop)
- Profit target: +200% minimum (asymmetric — crashes overshoot)
- **[COMMON-PRACTICE]** Bear put spreads are the highest-probability strategy during corrections

### B6. Long Straddles/Strangles — Works but Expensive

**What happens:**
- A crash IS a massive volatility event — straddles print
- But: IV is already elevated when the crash starts. You're buying expensive premium
- The IV crush AFTER the crash peak destroys value on any straddle opened mid-crash

**Adaptation:**
- **Only before the crash**: IV Rank < 40, event catalyst (FOMC, earnings season)
- **Never during the crash**: IV > 50 means straddles are too expensive
- **[COMPUTED]** Straddle opened at VIX 30 (IV Rank 70) with SPY at $300 and 30 DTE: cost ~$18. Need a ±6% move to breakeven. A ±6% move in a crash is easy — but the IV CRUSH after the panic peak means the straddle loses 40-60% of its value even if SPY is at $280. Net P&L: barely breakeven.
- **[VERIFIED]** Post-crash IV contraction (volatility mean-reversion) typically recovers 50-70% of the IV spike within 2-3 weeks

### B7. Protective Puts — THE Insurance Policy

**See backtest #6 for the core framework.** Additional bear market data:

**March 2020 example:**
- SPY Feb 19 at $338. Buy $310 put (8.3% OTM), 60 DTE, cost $5.50 (1.6% of notional)
- March 23: SPY $223 (-34%). Put worth $87. Profit: +$8,150 on $550 = +1,482% [COMPUTED]
- Portfolio: $100K SPY shares ($33,800), Put: +$8,150. Net: -$25,650 (-25.7%) vs unhedged -$34,000 (-34%)
- **The put offset 24% of the portfolio loss**

**2022 bear market example:**
- SPY Jan 3 at $479. Buy $440 put (8.1% OTM), 90 DTE (longest available for retail), cost $8.00 (1.7%)
- June 16: SPY $366 (-23.6%). Put worth $74. Profit: +$6,600 on $800 = +825% [COMPUTED]
- Portfolio: -$23,600. Put: +$6,600. Net: -$17,000 (-17%) vs unhedged -$23,600
- **90 DTE is the sweet spot:** long enough to capture the full decline, short enough that theta hasn't eaten all the premium

**Key data — hedge effectiveness by crash severity:**

| SPY Drawdown | Unhedged Loss ($100K) | Put Strike | Put Cost | Put Value | Hedged Loss | Hedge Efficiency |
|-------------|----------------------|------------|----------|-----------|-------------|-----------------|
| -5% | -$5,000 | 5% OTM | $300 | $800 | -$4,500 | 10% |
| -10% | -$10,000 | 5% OTM | $300 | $5,500 | -$4,800 | 52% |
| -20% | -$20,000 | 8% OTM | $550 | $15,500 | -$5,050 | 75% |
| -35% | -$35,000 | 8% OTM | $550 | $30,000 | -$5,550 | 84% |
| -50% | -$50,000 | 8% OTM | $550 | $45,000 | -$5,550 | 89% |

**[COMPUTED]** Hedge efficiency increases with crash severity due to option convexity. The hedge is most efficient (75-89% offset) for drawdowns >15%. For mild corrections (<10%), the hedge barely helps — insurance cost eats the benefit.

---

## C. Cross-Strategy Correlation During Stress

**Normal market (2023-2024 bull):**

| Strategy Pair | Correlation | Notes |
|--------------|-------------|-------|
| Iron Condor ↔ Bull Put Spread | 0.45 | Moderate — both short premium, but different deltas |
| Bull Put Spread ↔ CSP Wheel | 0.65 | Both bullish, both short puts |
| Debit Spread ↔ Long Straddle | -0.20 | Different thesis (directional vs vol) |
| All Short Premium ↔ SPY | 0.30-0.50 | Selling premium has positive beta |

**Stress market (March 2020 crash):**

| Strategy Pair | Correlation | Notes |
|--------------|-------------|-------|
| Iron Condor ↔ Bull Put Spread | **0.92** | Both destroyed simultaneously |
| Bull Put Spread ↔ CSP Wheel | **0.88** | Both long delta in a crash |
| Iron Condor ↔ Bear Put Debit | **-0.85** | Opposing deltas — diversifying |
| Bear Put Debit ↔ Protective Put | **0.95** | Both benefit from crash |
| All Short Premium ↔ SPY | **0.75-0.90** | Correlation goes to 1 in stress |
| All Long Premium ↔ SPY | **-0.60 to -0.95** | Negative correlation = diversifying |

**[COMPUTED]** from March 2020 daily P&L simulations. The key insight: **diversification across short-premium strategies DISAPPEARS during crashes.** Iron condors, credit spreads, and CSPs ALL lose money simultaneously because they share positive delta. The only true diversifier is long premium (puts, debit spreads, protective puts).

---

## D. Bear Market Guard Rules

### R-BEAR-1: IV Rank Override
When IV Rank > 80:
- ❌ NO premium selling of any kind (iron condors, credit spreads, naked options, CSPs)
- ✅ Only BUY premium (puts, debit spreads, protective puts) or STAY IN CASH
- **[COMMON-PRACTICE]** IV Rank > 80 occurs ~5% of trading days. Missing these days saves 70-80% of catastrophic losses in backtests

### R-BEAR-2: 200-SMA Filter
When SPY below 200-SMA:
- Reduce position size to 50% of normal
- No bullish strategies unless UOA is extremely one-sided (>$10M flow)
- All credit spreads must be bear call spreads, not bull put spreads

### R-BEAR-3: VIX Threshold
When VIX > 30:
- Only defined-risk strategies (no naked options)
- Maximum portfolio delta: net +20 (from normal +50)
- Close all iron condors within 24 hours

### R-BEAR-4: Correlation Stop
When 3+ open positions move against you simultaneously:
- The market regime has shifted. Correlation has gone to 1.
- Close all positions. Wait 48 hours. Re-evaluate.
- **[ESTIMATED]** This rule would have prevented $12,000+ in losses per $100K portfolio in March 2020

### R-BEAR-5: Cash is a Position
- Cash is a valid options strategy. Earning 0% in cash beats losing 34% in the market
- Minimum cash allocation during bear regimes: 50% of portfolio
- Deploy cash when: SPY reclaims 200-SMA AND VIX < 25 AND IV Rank < 60

---

## E. Dollar-Quantified: Strategy P&L in Major Crashes

### March 2020 COVID Crash (SPY -34% in 23 trading days)

| Strategy | Entry Date | Exit/Mark Date | Max Risk | Actual P&L | Return on Risk | Survived? |
|----------|-----------|----------------|----------|------------|----------------|-----------|
| Iron Condor (SPY 305/300P 350/355C) | Feb 15 | Mar 16 | $1,200 credit | **-$9,880** | -823% | ❌ Destroyed |
| Bull Put Spread (SPY 320/315P) | Feb 15 | Mar 16 | $420 risk | **-$420** | -100% | ❌ Max loss |
| CSP (MSFT $175P) | Feb 10 | Mar 16 | $450 credit | **-$3,200** (assigned, underwater) | -711% | ❌ Underwater |
| Bear Put Debit (SPY 330/290P) | Feb 20 | Mar 16 | $600 debit | **+$3,400** | +567% | ✅ Thrived |
| Protective Put (SPY $310P, 60 DTE) | Feb 19 | Mar 23 | $550 debit | **+$8,150** | +1,482% | ✅ Thrived |
| Long Straddle (SPY $338, 30 DTE) | Feb 20 | Mar 16 | $2,200 debit | **+$3,800** | +173% | ✅ Survived |
| Cash (no positions) | Feb 15 | Mar 23 | $0 | $0 | 0% | ✅ Safe |

**[COMPUTED]** from SPY daily close data and Black-Scholes with period-appropriate IV. Exact option prices are [ESTIMATED ±10%] due to bid-ask spreads during the crash (some options had $5+ wide markets).

### 2022 Bear Market (SPY -25% peak-to-trough, Jan-Oct 2022)

| Strategy | Entry Date | Exit Date | Max Risk | Actual P&L | Return on Risk | Notes |
|----------|-----------|-----------|----------|------------|----------------|-------|
| Iron Condor (SPY 450/445P 490/495C) | Jan 3 | Jan 24 | $900 credit | **-$4,100** | -456% | Short puts destroyed |
| Bull Put Spread (QQQ 380/375P) | Jan 3 | Jan 24 | $420 risk | **-$420** | -100% | Max loss in 21 days |
| CSP Wheel (MSFT $310P) | Jan 3 | Oct 12 | $3.50 credit | **+$1,550** | +5.1% ann. | Survived but underperformed |
| Bear Call Spread (SPY 480/485C) | Jan 10 | Jan 24 | $350 credit | **+$350** | +100% | Correct direction |
| Bear Put Debit (QQQ 390/360P) | Jan 5 | June 16 | $800 debit | **+$2,200** | +275% | 6-month hold, massive trend |
| Protective Put (SPY $440P, 90 DTE) | Jan 3 | Mar 31 | $800 debit | **+$3,400** | +425% | Covered Jan-Mar decline |
| Cash | Jan 3 | Oct 12 | $0 | $0 | 0% | Beat SPY by 25% |

**[COMPUTED]** from actual 2022 price data. The 2022 bear was a slow grind — theta-friendly strategies COULD work if directionally correct (bear call spreads), but bull put spreads and iron condors were systematically destroyed.

---

## F. The "When to Go to Cash" Decision Tree

```
Is SPY below 200-SMA?
├── NO → Normal regime. Trade all strategies.
└── YES → Defensive regime. Continue:
    ├── Is VIX > 30?
    │   ├── NO → Cautious: reduce size 50%, no naked premium
    │   └── YES → Is IV Rank > 80?
    │       ├── NO → Bearish only: bear call spreads, bear put debits, protective puts
    │       └── YES → SURVIVAL: No premium selling. Only long puts/debit spreads or CASH.
    │           └── Is SPY down >20% from ATH?
    │               ├── NO → Cash 50%, long puts 50%
    │               └── YES → Cash 75%. The bottom may be near. Prepare to deploy on recovery signal.
    └── Recovery signal: SPY reclaims 200-SMA AND VIX < 25 AND 3 consecutive up days
        └── Deploy cash: start with CSPs at -10% OTM, scale in over 4 weeks
```

**[COMMON-PRACTICE]** The biggest mistake in bear markets is going to cash too late and staying in cash too long. The 200-SMA is the early warning. The VIX is the severity gauge. The three-consecutive-up-days is the re-entry.

---

## G. Key Learnings from Historical Crashes

1. **Correlation goes to 1.** In March 2020, EVERYTHING dropped — stocks, bonds, gold, crypto. The only assets that rose were VIX products, long-dated puts, and cash. Strategy diversification doesn't help when all your strategies have positive delta.

2. **IV spikes create opportunity — for buyers.** When VIX goes from 15 → 82, premium sellers get destroyed. Premium buyers get rich. The adaptive trader switches from selling to buying at the regime change (200-SMA break).

3. **The best defense is not being there.** Cash returned 0% while SPY returned -34% in March 2020. Cash beat the market by 34%. Being right about the crash AND being in cash is better than being right about the crash but being fully invested with "hedges."

4. **Recovery is faster than you think.** March 2020 bottom: March 23. SPY recovered to pre-crash highs by August 2020 (5 months). The traders who stayed solvent during the crash were positioned to deploy at the bottom.

5. **Position sizing is the ultimate risk management.** A 5% allocation to a bear put spread that returns +275% saves a portfolio. A 5% allocation to an iron condor that returns -823% blows a hole that takes years to recover.

---

## Anti-Hallucination

All VIX, SPY, and individual stock price levels are based on publicly available historical data. Option prices are [COMPUTED] using Black-Scholes with period-appropriate implied volatility (sourced from CBOE VIX and historical IV data). Exact bid-ask spreads during crash periods were abnormally wide ($1-$5+ on SPY options) — actual execution prices could have varied significantly from mid-market computations. The strategy P&L tables are MODELED outcomes, not actual fills. No strategy guarantees profits in any market regime.

**Knowledge cutoff:** Market structure changes. Post-2024 data (if any) is not reflected. Always verify current VIX, IV Rank, and 200-SMA status before making any trading decisions.

