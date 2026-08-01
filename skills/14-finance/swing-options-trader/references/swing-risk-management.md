# Swing Options Risk Management — Deep Reference

> **Reading time:** 10 min | **Prerequisites:** options-risk-engineer, swing-options-trader

## The Swing Risk Difference

Swing options trades (2-30 day holds) face a unique risk profile:
1. **Overnight/weekend gap risk** — The market moves while you can't react
2. **Theta decay** — Cost of carrying options across days
3. **IV regime shifts** — Volatility environment can change mid-swing
4. **Correlation decay** — Diversification that works in normal times fails in crashes
5. **Earnings risk** — Binary events within swing holding periods

## Kelly-Optimized Position Sizing

### Standard Kelly for Options

[COMPUTED] The Kelly Criterion adapted for options swing trading:

```
Kelly fraction = win_rate - ((1 - win_rate) / (avg_win / avg_loss))

Where:
  win_rate = historical win rate for this strategy/underlying
  avg_win = average winning trade profit (in dollars)
  avg_loss = average losing trade loss (in dollars, absolute value)

Constraints:
  - Use trailing 20-trade stats, not all-time
  - If < 20 trades: use conservative estimates (40% WR, avg_win/avg_loss = 1.5)
  - Apply half-Kelly: Kelly_f_adjusted = Kelly_f × 0.50
  - Max risk per trade = account_value × min(Kelly_f_adjusted, 0.05)
```

### Half-Kelly: Why Half?

[BACKTEST-EVIDENCE] Full Kelly maximizes long-term growth rate but produces extreme drawdowns. In the Trading project backtest:
- Full Kelly: would have blown up 3 of 11 tickers (drawdown > 80%)
- Half Kelly: survived all 11 tickers (max drawdown -57%, SPY)
- Quarter Kelly: gentler ride, ~65% of half-Kelly returns

**Half-Kelly is the default for swing options.** Quarter-Kelly for accounts < $25,000 or strategies with < 30 trades of history.

## Volatility-Adjusted Sizing

[BACKTEST-EVIDENCE] Position sizes must shrink as volatility increases:

```
vol_multiplier = 1.5 - (hv_pct / 100 × 1.1)
vol_multiplier = max(0.3, min(1.5, vol_multiplier))

Example:
HV = 15% → multiplier = 1.335 (above standard — calm market)
HV = 30% → multiplier = 1.170 (slightly above standard)
HV = 50% → multiplier = 0.950 (slightly below standard)
HV = 80% → multiplier = 0.620 (reduced — turbulent)
HV = 120% → multiplier = 0.300 (minimum — extreme volatility)
```

### Combined Sizing Formula

```
final_risk_per_trade = base_kelly_risk × vol_multiplier × regime_multiplier

regime_multiplier:
  SPY > 50SMA + VIX < 20:  1.00 (full)
  SPY > 50SMA + VIX 20-25: 0.75
  SPY < 50SMA + VIX < 20:  0.75 (bearish but calm)
  SPY < 50SMA + VIX 20-25: 0.50
  SPY < 50SMA + VIX > 25:  0.25
  SPY < 50SMA + VIX > 30:  0.00 (do not trade)
```

## Swing Exit Rules

### The 4-Exit System

Every swing trade must have all four exits defined at entry:

| Exit Type | Trigger | Action |
|-----------|---------|--------|
| **Profit Target** | Specific price or % of max profit | Close full position |
| **Stop Loss** | Specific loss amount or % of debit/credit | Close full position |
| **Time Stop** | DTE threshold or calendar date | Close regardless of P&L |
| **Thesis Invalidation** | Technical or fundamental reason the trade no longer makes sense | Close immediately |

### Profit Targets by Strategy

| Strategy | Profit Target | Rationale |
|----------|-------------|-----------|
| Credit Spread (Bull Put / Bear Call) | 50% of credit received | Remaining 50% takes disproportionately longer and carries increasing gamma risk |
| Iron Condor | 25% of wing width at 50% of max profit | 4-leg structures decay slower. Take profits earlier |
| Debit Spread (Call/Put) | 80-100% of max profit | Debit trades have theta working against you. Let winners run but take profits near max |
| Long Call/Put (single leg) | 100%+ of premium (2:1 minimum RR) | [BACKTEST-EVIDENCE] 2:1 asymmetric exit ratio is the #1 profit lever |
| Calendar/Diagonal | 25-50% of debit paid | These are theta-positive. Take profits when the short leg decays |

### Stop Losses by Strategy

| Strategy | Stop Loss | Rationale |
|----------|----------|-----------|
| Credit Spread | 2× credit received | 2:1 risk/reward with 50% target. Breakeven at 33% WR |
| Iron Condor | 2× credit received or 1.5× wing width (whichever is tighter) | 4 legs = more can go wrong in a fast move |
| Debit Spread | 50% of debit paid | Debit = max loss already. 50% stop preserves capital for re-entry |
| Long Call/Put | 40% of premium (tighter than 50% due to theta decay) | Time works against you. Tighter stops needed |
| Calendar/Diagonal | 50% of debit paid | Theta is your friend, but IV moves can hurt |

### Time Stops

| DTE at Entry | Time Stop | Why |
|-------------|----------|-----|
| 21-30 DTE | Exit at 14 DTE remaining | Gamma starts accelerating. Theta benefit diminishing |
| 30-45 DTE | Exit at 21 DTE remaining | Capture the best theta decay, avoid gamma acceleration |
| 45-60 DTE | Exit at 30 DTE remaining | Give more time. Still exit before acceleration zone |
| 60-90 DTE | Exit at 45 DTE remaining | Position trade territory. Exit if thesis hasn't played out by halfway |

[COMMON-PRACTICE] The 21-DTE time stop is the most common: exit all short premium positions by 21 DTE to avoid gamma risk.

## Weekend Gap Risk

[VERIFIED] Weekend gaps are 2-3× larger than typical overnight gaps because 2.5 days of news accumulate. For swing traders:

```
Weekend gap risk management:
1. Reduce position size by 25-50% before weekends
2. If holding through weekend: tighten stops on Friday close
3. Check economic calendar: any weekend events (G7, OPEC, elections)?
4. Monday morning: check futures before open. Gap plan:
   - Gap < 1%: Normal management
   - Gap 1-3%: Assess against positions. Adjust if needed
   - Gap > 3%: Emergency mode. Close endangered positions at open
```

## Correlation Decay in Crashes

[VERIFIED] Diversification works in normal markets but fails in crashes. Correlations converge to 1 during market stress. For swing options:

```
Normal market: 5 positions across 5 uncorrelated sectors → diversification benefit
Crash (-5%+ day): ALL 5 positions move together → correlation → 1

What to do:
1. Assume crash correlation = 0.7-0.9 for all equity positions
2. Size the portfolio for the correlated scenario, not the independent scenario
3. True diversification for options: long/short across assets, not just different longs
4. VIX futures/options as a crash hedge (negative correlation to SPY in crashes)
```

## Position Correlation Matrix

Before adding a new swing position, check correlation with existing positions:

```
New position correlation check:
1. Compute correlation of new underlying with each existing position's underlying
2. If any correlation > 0.70 → combined position size = sum × 0.75 (correlation penalty)
3. If > 0.90 → the positions are effectively the same bet. Pick the better one

Total portfolio beta check:
  Sum of (position_size × delta × beta_to_SPY) across all positions
  If portfolio delta > 2× account delta capacity → reduce
```

## Drawdown Management

[BACKTEST-EVIDENCE] From Trading project: max drawdown is extreme even for winning strategies (SPY -57%, META -49%, QQQ -92%):

```
Drawdown circuit breakers:
- -10% from portfolio high: Review all positions. Tighten stops. No new entries
- -20% from portfolio high: Close 50% of positions. Pause new entries for 1 week
- -30% from portfolio high: Close all positions. Pause new entries for 2 weeks. Review strategy
- -40% from portfolio high: FULL STOP. 1-month trading halt. Complete strategy review

These are PORTFOLIO-LEVEL circuit breakers, not position-level.
```

## Common Mistakes

| ❌ Mistake | ✅ Correct |
|-----------|-----------|
| Letting credit spreads run to expiration for "the last 10 cents" | Close at 50% of credit. The last 50% takes 50%+ of the time with increasing gamma risk |
| "I have 5 diversified swing positions — I'm safe" | In a crash, all 5 will move together. Size for the correlated scenario |
| Sizing based on notional instead of risk | Options notional is misleading. A $5 credit on a $5-wide spread has $500 risk, not $5 risk |
| "Kelly says 15% of account — let's do it" | Never bet >5% of account on a single swing trade regardless of what Kelly says. Half-Kelly with a 5% cap |
| Ignoring correlation between option positions and stock portfolio | If you have a stock portfolio AND options swing positions, the combined beta must be managed |

## Provenance

[VERIFIED] Kelly Criterion from Kelly (1956). Half-Kelly adaptation from Thorp (1997) "The Kelly Criterion in Blackjack, Sports Betting, and the Stock Market."
[VERIFIED] Correlation convergence in crashes from Longin & Solnik (2001) and subsequent research.
[COMPUTED] Volatility-adjusted multiplier formula and combined sizing formula.
[BACKTEST-EVIDENCE] Max drawdown statistics, half-Kelly survival rates, asymmetric exit ratio from Trading project backtest.
[COMMON-PRACTICE] 50% credit close rule, 21-DTE time stop from professional option selling methodology (Tastytrade, Options Alpha).
[AS OF 2026-07]
