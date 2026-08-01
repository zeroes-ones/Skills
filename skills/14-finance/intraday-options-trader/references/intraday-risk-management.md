# Intraday Options Risk Management — Deep Reference

> **Reading time:** 10 min | **Prerequisites:** options-risk-engineer (standard risk management), intraday-options-trader

## The Intraday Risk Difference

[VERIFIED] Intraday options risk differs fundamentally from multi-day risk in three ways:
1. **Gamma dominates.** Vega and theta are secondary. A 0.5% stock move can move an ATM 0DTE option 30-50%.
2. **No overnight recovery.** There is no "the market might bounce tomorrow." The option expires TODAY.
3. **Reaction time is compressed.** You have seconds, not days, to respond to adverse moves.

## Position Sizing Framework

### The Intraday Risk Budget

```
Daily risk budget = account_value × daily_risk_pct
Daily risk_pct: 1-2% for experienced traders, 0.5% for beginners

Per-trade risk allocation:
- Single-leg directional: 25% of daily risk budget
- Multi-leg spread: 30% of daily risk budget
- Gamma scalp: 15% of daily risk budget (frequent trading → smaller size)
- 0DTE butterfly: 10% of daily risk budget (highest gamma risk)

Max simultaneous positions: 2 (limit cognitive load for monitoring)
```

### Volatility-Adjusted Sizing

[BACKTEST-EVIDENCE] From the Trading project:

```
Volatility-adjusted size multiplier = 1.5 - (hv%/100 × 1.1) clipped [0.3, 1.5]

SPY HV% = 15: multiplier = 1.5 - (15/100 × 1.1) = 1.335 → size = normal × 1.335
SPY HV% = 40: multiplier = 1.5 - (40/100 × 1.1) = 1.060 → size = normal × 1.06
SPY HV% = 100: multiplier = 1.5 - (100/100 × 1.1) = 0.400 → size = normal × 0.40
SPY HV% = 120: multiplier = clip to 0.3 → size = normal × 0.30

Low vol → larger positions (calmer market, less noise)
High vol → smaller positions (larger swings, tighter risk)
```

### Gamma-Adjusted Sizing

[COMPUTED] For near-expiration options, gamma risk replaces vol risk as the primary sizing constraint:

```
Gamma-adjusted max contracts = normal_max_contracts × (0.001 / current_gamma)

Example:
Normal max = 5 contracts at gamma = 0.001
0DTE ATM gamma = 0.005 → max contracts = 5 × (0.001/0.005) = 1 contract
```

## Circuit Breakers (HARD GATES)

### Daily Loss Limit

```
If daily P&L < -daily_risk_budget: STOP ALL TRADING. No exceptions.

This is a HARD circuit breaker. Do not trade around it. Do not "make it back."
The market will be there tomorrow. Capital won't be if you blow through this.
```

### Consecutive Loss Limit

```
If 2 consecutive trades are full losses (hit max loss):
  → STOP FOR 30 MINUTES. Step away. Review what went wrong.
  → Resume at 50% of normal size for next trade.

If 3 consecutive trades are full losses:
  → STOP FOR THE DAY. Three consecutive max-loss trades is not random noise.
  → Something is wrong with your read, the market, or your execution.
```

### VIX Spike Halt

```
If VIX spikes >20% intraday from the day's open:
  → Close 50% of all open positions at market (use limit, not market orders)
  → Halve position sizes for remaining positions
  → No new entries for 30 minutes

If VIX spikes >50% intraday:
  → Close ALL positions. FLAT. No exceptions.
  → Stay flat for the rest of the day
```

### De-POG (Destruction of Profit Opportunity Gate)

```
If a position is profitable but:
  - Delta has moved beyond planned range (±30% from entry delta)
  - OR gamma has doubled from entry gamma
  - OR IV has spiked >20% against the position

→ CLOSE the position. A winning trade turning into a loser because you "let it ride"
   in a high-gamma/intraday environment is one of the most common failure patterns.
```

## The FalseStopGuard

[BACKTEST-EVIDENCE] From Trading project analysis: premature exits on noise are as costly as holding losers too long. The FalseStopGuard prevents exiting on noise:

```
DO NOT EXIT on a pullback unless:

For LONG positions:
  1. Price breaks below the previous 3-bar low AND
  2. Volume on the break bar > 120% of 5-bar trailing average AND
  3. OR a single bar wick > 2× the average bar range → treat as reversal

For SHORT positions:
  1. Price breaks above the previous 3-bar high AND
  2. Volume on the break bar > 120% of 5-bar trailing average AND
  3. OR a single bar wick > 2× the average bar range → treat as reversal
```

## Time-Based Risk Management

### Maximum Hold Times

| Strategy Type | Max Hold Time | Reason |
|--------------|---------------|--------|
| ORB options | 2 hours or target hit | ORB setups resolve within 90-120 min typically |
| Momentum options | 1 hour or target/stop hit | Momentum fades. If it hasn't hit target in 1 hour, the move is exhausted |
| 0DTE butterfly | 3:00 PM ET MAX | Gamma explosion after 3 PM. Close everything by 2:45 PM to be safe |
| Gamma scalp | Varies. Close all by 2:30 PM | Gamma becomes unhedgeable in the final 90 minutes |
| Post-news scalp | 30 minutes max | News impact fades within 30 min. Any edge after that is noise |

### Time-of-Day Risk Adjustments

```
9:35-10:30 AM: Normal risk. Best trading window.
10:30-11:30 AM: Reduce position size by 25%. Directional clarity fades.
11:30-1:30 PM: Reduce position size by 50%. Lunch lull. False breakouts common.
1:30-3:00 PM: Normal risk. Afternoon push window.
3:00-4:00 PM: CLOSE ONLY. No new entries. Gamma explosion.
```

## Pre-Trade Checklist (Intraday)

Before ANY intraday options trade:

- [ ] DTE ≥ 7? If less, reduce size per gamma-adjusted sizing
- [ ] Spread < 5% of option price? If not, skip
- [ ] Daily loss limit NOT hit? If hit, stop
- [ ] Consecutive loss limit NOT hit? If 2 losses, 30-min pause
- [ ] VIX stable? If >20% spike, halve positions. >50% spike, flat
- [ ] Within allowed trading window? (9:35 AM-3:00 PM)
- [ ] Exit plan written: target, stop, time stop
- [ ] Position size calculated per volatility-adjusted + gamma-adjusted formula
- [ ] P&L impact if stopped out < daily risk budget per-trade allocation

## Post-Trade Review (Same Day)

```
1. Journal: Entry time, exit time, strategy, P&L, max favorable/adverse excursion
2. Attribute: Was P&L skill, luck, or noise?
   - If target hit quickly (<30 min): likely luck/timing, not repeatable skill
   - If target hit after multiple pullbacks that held FalseStopGuard: skill
   - If stopped on noise (FalseStopGuard would have saved): fix the guard
3. Bias check:
   - After a win: was I overconfident? Did I size up unwisely?
   - After a loss: am I revenge-trading? Did I size up to "make it back"?
   - After flat: am I bored-trading? Entering without setup?
```

## Common Mistakes

| ❌ Mistake | ✅ Correct |
|-----------|-----------|
| Sizing based on account % without gamma adjustment | Gamma-adjusted sizing for DTE ≤ 7. Gamma exposure is the risk, not notional |
| "I'll just give it 15 more minutes" | Time stops are as important as price stops. If the setup hasn't resolved in expected time, exit |
| Revenge trading after a stop-out | 30-min mandatory pause after 2 losses. Day stop after 3 |
| Trading through the lunch lull at full size | Reduce size 50% 11:30-1:30 PM. Patterns are less reliable |
| "VIX is spiking, this is great for my long straddle" | VIX spike → spreads widen → you can't exit at fair price even if you're right. Close before the spike |

## Provenance

[VERIFIED] Circuit breaker design principles from risk management best practices (Taleb, Spitznagel).
[COMPUTED] Gamma-adjusted sizing formula. Gamma exposure scales with 1/√(DTE). Intraday gamma explosion well-documented in options literature.
[BACKTEST-EVIDENCE] Volatility-adjusted sizing formula, FalseStopGuard mechanics, and gamma tightening rule from Trading project backtest data.
[COMMON-PRACTICE] Time-of-day risk adjustments from professional day trading literature.
[AS OF 2026-07]
