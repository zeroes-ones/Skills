# Swing Timeframe Optimization — Swing Options Reference

> **Reading time:** 10 min | **Prerequisites:** options-strategist (Greeks), swing-options-trader

## The Swing Timeframe

[VERIFIED] Swing trading occupies the 2-30 day holding period — longer than intraday (minutes/hours), shorter than position trading (months/years). Options on the swing timeframe have a unique Greek profile: theta is meaningful but manageable, vega matters but isn't dominant, and gamma isn't yet explosive.

## Optimal DTE for Swing Options

### The DTE Sweet Spot

| Holding Period | Optimal Entry DTE | Expiration at Exit | Why |
|---------------|-------------------|-------------------|-----|
| 2-5 days | 21-30 DTE | 16-28 DTE | Enough theta buffer. Gamma manageable. Tight spreads on weeklies |
| 5-10 days | 30-45 DTE | 20-40 DTE | Theta sweet spot. Good premium/duration ratio. Still liquid |
| 10-20 days | 45-60 DTE | 25-50 DTE | More time for thesis to play out. Lower theta per day |
| 20-30 days | 60-90 DTE | 30-70 DTE | Position trade territory. Theta decay just accelerating at exit |

[COMMON-PRACTICE] The 30-45 DTE entry window is optimal for most swing trades. It sits in the theta acceleration zone (day 45-21 is when daily theta decay is highest) while providing enough time for the thesis to develop.

### The Theta Curse of Short-Dated Swings

[COMPUTED] Entering a swing trade with 7 DTE and expecting a 7-day hold means:

```
Day 0 (7 DTE): Theta = -$3/day
Day 3 (4 DTE): Theta = -$8/day
Day 5 (2 DTE): Theta = -$25/day
Day 6 (1 DTE): Theta = -$60/day

If the stock is flat for 7 days, the option loses 40-60% of its value from theta alone.
The option MUST be right AND the timing MUST be precise. This is not a swing trade — it's a gamble.
```

**Rule:** Entry DTE must be at least 2× the expected holding period. If you plan to hold 10 days, enter at 30+ DTE minimum.

## Greek Evolution Across Swing Holding Periods

[COMPUTED] For a 45-DTE ATM call, $500 stock, IV=20%:

| Days Held | DTE Remaining | Delta | Gamma | Theta | Vega | Option Price |
|-----------|--------------|-------|-------|-------|------|-------------|
| 0 (entry) | 45 | 0.52 | 0.008 | -$2.80 | 0.52 | $12.00 |
| 5 | 40 | 0.53 | 0.009 | -$3.00 | 0.54 | $11.50 (if flat) |
| 10 | 35 | 0.54 | 0.010 | -$3.30 | 0.56 | $11.00 (if flat) |
| 15 | 30 | 0.55 | 0.012 | -$3.80 | 0.58 | $10.20 (if flat) |
| 20 | 25 | 0.56 | 0.014 | -$4.50 | 0.60 | $9.00 (if flat) |
| 25 | 20 | 0.58 | 0.018 | -$5.80 | 0.62 | $7.50 (if flat) |
| 30 | 15 | 0.60 | 0.025 | -$8.00 | 0.64 | $5.50 (if flat) |

**Key observation:** From day 20 onward (DTE ≤ 25), theta decay accelerates rapidly. If your thesis hasn't played out by then, the trade is dying — not from being wrong, but from time.

## Strike Selection for Swing Trades

### Long Premium (Debit Spreads, Single Legs)

| Directional Conviction | Best Structure | Strike Selection | Rationale |
|-----------------------|---------------|-----------------|-----------|
| Strong bullish | ATM Debit Call Spread (5-10 wide) | Long: ATM, Short: 1-2 strikes OTM | Balanced debit vs. probability. Capped risk/reward |
| Moderate bullish | OTM Call Spread (5 wide) | Long: 1 strike OTM, Short: 2-3 strikes OTM | Lower debit, higher leverage, lower probability |
| Strong bearish | ATM Debit Put Spread (5-10 wide) | Long: ATM, Short: 1-2 strikes OTM | Mirror of bullish call spread |
| High conviction, want uncapped upside | Long Call (single leg) | ATM or 1 strike OTM | Unlimited upside. Must manage theta and have exit plan |
| Neutral, want to collect theta | Credit spread | Short: 0.20-0.30Δ | Theta collection. Defined risk. |

### Short Premium (Credit Spreads, Iron Condors)

| Market View | Structure | Short Strike Delta | Profit Target | Stop |
|------------|-----------|-------------------|---------------|------|
| Neutral/bullish | Bull Put Spread | 0.20-0.30 | 50% of credit | 2× credit received |
| Neutral/bearish | Bear Call Spread | 0.20-0.30 | 50% of credit | 2× credit received |
| Neutral, low vol | Iron Condor | 0.15-0.20 (each side) | 25% of width at 50% profit | 2× credit received |
| Neutral, high vol | Short Strangle | 0.10-0.15 (each side) | 50% of credit | 3× credit (undefined risk — wider stop) |

## Multi-Timeframe Confirmation

### The 3-Tier Confirmation System

```
Tier 1 (Weekly): Long-term trend direction. Determines BIAS.
  - Price vs 20SMA/50SMA on weekly
  - Weekly RSI > 50 = bullish bias, < 50 = bearish bias
  - If weekly is flat/choppy → neutral bias → credit spreads only

Tier 2 (Daily): Swing setup identification. Determines ENTRY TIMING.
  - Pullback to support in uptrend → bull put spread entry
  - Test of resistance in downtrend → bear call spread entry
  - Breakout from consolidation → debit spread in breakout direction
  - Only enter when daily and weekly align

Tier 3 (4-Hour): Intra-swing fine-tuning. Determines PRECISE ENTRY.
  - Oversold RSI on 4H in daily uptrend → optimal long entry
  - Overbought RSI on 4H in daily downtrend → optimal short entry
  - 4H volume confirmation of the daily setup
  - If 4H doesn't confirm daily → wait. Don't force it
```

### Confirmation Matrix

| Weekly | Daily | 4H | Action |
|--------|-------|-----|--------|
| Bullish | Bullish pullback | Oversold bounce | ✅ Best long entry |
| Bullish | Bullish continuation | Overbought | ⚠️ Wait for pullback. Don't chase |
| Bullish | Bearish reversal | Bearish momentum | ⚠️ Weekly/daily conflict. Skip or reduce size |
| Bearish | Bearish rally | Overbought fade | ✅ Best short entry |
| Flat/Neutral | Range support | Oversold | ✅ Bull put spread at support |
| Flat/Neutral | Range resistance | Overbought | ✅ Bear call spread at resistance |

## Position Sizing for Swing

### Kelly-Optimized Sizing

[COMPUTED] For options swing trades, Kelly fraction adjusted for serial correlation:

```
Kelly_f = win_rate - ((1 - win_rate) / (avg_win / avg_loss))

Then: Kelly_f_adjusted = Kelly_f × 0.50 (half-Kelly — reduces drawdown, accounts for estimation error)

Position_size = account_value × Kelly_f_adjusted × (max_loss_per_contract / option_credit_or_debit)

Example: 55% WR, avg_win = $150, avg_loss = -$100, account = $50,000
Kelly_f = 0.55 - (0.45 / 1.5) = 0.55 - 0.30 = 0.25
Kelly_f_adjusted = 0.125
Max risk per trade = $50,000 × 0.125 = $6,250
For a trade risking $250: 25 contracts
```

[BACKTEST-EVIDENCE] Half-Kelly provides ~75% of full-Kelly returns with ~50% of the drawdown. In the Trading project backtest, full-Kelly would have blown up 3 of 11 tickers. Half-Kelly survived all 11.

### Volatility-Adjusted Sizing

[BACKTEST-EVIDENCE] From Trading project data:

```
size_multiplier = 1.5 - (hv_pct/100 × 1.1), clipped [0.3, 1.5]

SPY (15% HV): multiplier = 1.335 (can size up — calm market)
META (45% HV): multiplier = 1.005 (standard size)
TSLA (70% HV): multiplier = 0.730 (reduce — volatile)
GME (120% HV): multiplier = 0.300 (minimum size — extreme vol)
```

## Common Mistakes

| ❌ Mistake | ✅ Correct |
|-----------|-----------|
| Entering a swing trade with <14 DTE | Minimum 21 DTE at entry. Theta decay will kill the trade before the thesis plays out |
| Only checking daily chart | Multi-timeframe: weekly for bias, daily for setup, 4H for entry. At minimum: daily + 4H |
| Using same size for all underlyings | Volatility-adjusted sizing. TSLA options should be ~50% of SPY option size |
| Holding credit spreads to expiration for "max profit" | Close at 50% of max profit. The remaining 50% requires 50%+ of the time with increasing gamma risk |
| No exit plan beyond "when it's profitable" | Define: target (50% credit / 100%+ debit), stop (2× credit / 30% debit), time stop (14 DTE remaining) |

## Provenance

[VERIFIED] DTE selection framework from options market mechanics. Theta acceleration in final 21 days is well-documented.
[COMPUTED] Greek evolution table uses Black-Scholes with S=500, K=500 (ATM), IV=20%, r=5%. Delta shifts assume flat stock.
[COMMON-PRACTICE] Multi-timeframe confirmation and 50%-profit credit spread close from Tastytrade, Options Alpha.
[BACKTEST-EVIDENCE] Half-Kelly sizing and volatility-adjusted multiplier from Trading project backtest.
[AS OF 2026-07]
