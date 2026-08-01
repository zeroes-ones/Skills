# Behavioral Bias in Swing Options Trading

> **Portability target:** Spec-level. Bias definitions are universal — detection rules are implementable in any trading journal.

## Why This Matters

The Trading project's 1,068-trade backtest surfaced behavioral patterns that destroy swing accounts. These are NOT strategy problems — they are decision-making failures that occur during live trading but never appear in backtests.

## The Five Killers

| Bias | Symptom | Swing-Specific Trigger | Fix |
|------|---------|----------------------|-----|
| Disposition Effect | Closing winners at 30% profit, holding losers to -100% because "it'll come back" | Seeing a 20% unrealized loss → rationalizing: "there's still 3 weeks to expiration" | **Mechanical exit at -50% max loss. No discretion.** The trade is wrong — time won't fix a bad entry. |
| Revenge Trading | Entering a new position within 15 minutes of a stop-out, usually 2× size | Stop just triggered → "I'll make it back on the next setup." Adrenaline, not analysis. | **30-minute mandatory gap after ANY stop-out.** Resume at 50% size. Second stop = day over. |
| Anchoring | "I bought at $1.50 so I won't sell below $1.50" — stock at $142 from entry price $155, option worth $0.40 | Entry price is a memory. Current price is reality. The market doesn't remember your fill. | **Ask: would I enter this trade NOW at current prices?** If no, exit. Entry price is sunk cost. |
| Overconfidence | "I've won 5 in a row — the system is working!" Sizing increases. Next trade: loser at 1.5× size erases 3 wins. | Win streak ≥ 4 → trader feels invincible → sizing creeps up → mean reversion in outcomes | **AFTER 3 consecutive wins: REDUCE size 25%.** Win streaks are luck + positive variance. They reverse. |
| Loss Aversion | Taking $200 profit at 30% max profit because "profit is profit" while holding $800 losers | The math: 4 wins at $200 + 1 loss at $800 = $0. 5 wins at $200 + 1 loss at $1,000 = break even → negative after commissions | **Minimum R:R 2:1. Never close a winner for less than 2× the risk you hold on losers.** 50% winners at 2:1 = +25% expectancy. |

## Detection Rules

### Programmatic Detection (For Trading Journals)

| Rule | Detection | Alert |
|------|-----------|-------|
| Disposition | Winners closed at < 40% of max profit AND losers closed at > 80% of max loss, across last 10 trades | "Disposition Effect Alert: Avg profit capture = X%, avg loss = Y%. Ratio < 0.5." |
| Revenge | Entry within 15 minutes of prior exit AND size > prior trade size | "REVENGE TRADE DETECTED. HALT. 30-min mandatory pause." |
| Anchoring | Entry price within 2% of prior exit price on same underlying within 24 hours | "Anchoring Alert: Re-entering same ticker at near-same price. Is this a new signal or attachment?" |
| Overconfidence | Win rate > 70% over 10+ trades AND average size increased > 20% | "Overconfidence Alert: High win rate + increasing size. Win streaks revert." |
| Loss Aversion | Avg win < 0.5× avg loss, last 10 trades | "Loss Aversion Alert: You're cutting winners early and holding losers. R:R is inverted." |

## The Pre-Trade Bias Check

Before entering any swing trade, answer these 3 questions:

1. **"Would I enter this trade if I had NO open positions?"** If the answer is "I need to recover from my last loss" — STOP. You're revenge trading.

2. **"Am I increasing size because of recent wins?"** If yes — REDUCE to standard size. Recent wins have zero predictive value.

3. **"If this trade goes to max loss, will I be okay?"** If the answer is "I'll be angry/frustrated/discouraged" — reduce size until max loss feels boring.

## The Hardest Truth

**"The problem isn't my strategy — it's my psychology."** This is usually wrong. Strategy and psychology interact: a good strategy with loose exits invites disposition effect. A poor strategy that produces streaks invites overconfidence.

The fix is mechanical rules, not willpower. **You cannot discipline your way out of a poorly-structured trading system.**
