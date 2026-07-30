# Behavioral Bias Detection

## Disposition Effect
**Definition**: Tendency to sell winners too early and hold losers too long.

### Detection Algorithm
1. Compute holding period for each closed trade
2. Separate by: winner (P&L > 0) vs loser (P&L ≤ 0)
3. Compare: mean_hold_winner vs mean_hold_loser
4. Disposition effect PRESENT if mean_hold_loser > mean_hold_winner * 1.5

### Confounding Factors
- Mechanical profit targets: winners automatically closed → NOT disposition
- Stop losses: losers automatically closed → masks disposition
- Filter: only compare DISCRETIONARY exits

## Revenge Trading
**Definition**: Increasing position size or trade frequency after losses.

### Detection Algorithm
1. Identify losing trades
2. Measure: time to next trade entry after a loss
3. Measure: position size of next trade vs baseline average
4. Revenge trading PRESENT if:
   - Post-loss time_to_entry < 0.5 * baseline_time_between_trades AND
   - Post-loss position_size > 1.3 * baseline_position_size

### Additional Signals
- Increased frequency: multiple trades in same session after a loss
- Asset switching: trading different instrument than usual (chasing)
- Conviction abandonment: ignoring system rules after losses

## Loss Shyness (Under-Trading After Losses)
**Definition**: Reducing position size or avoiding trades after losses, leading to missed recovery opportunities.

### Detection Algorithm
1. Compare position sizes after wins vs after losses
2. Loss shyness PRESENT if post-loss position_size < 0.7 * baseline

## Anchoring
**Definition**: Fixating on entry price or recent high as reference point.

### Detection Algorithm
- Check if stop-loss levels cluster at round numbers rather than technical levels
- Check if take-profit targets are near entry price (breakeven bias)
- Compare partial exit behavior: exiting at breakeven = anchoring

## Overconfidence
**Definition**: Taking larger positions after winning streaks.

### Detection Algorithm
1. Track position size after win streaks (3+ consecutive wins)
2. Overconfidence PRESENT if post-streak_size > 1.5 * baseline AND post-streak win rate declines

## Provenance
[VERIFIED] Behavioral bias definitions from Kahneman & Tversky (prospect theory), Odean (disposition effect 1998)
[AS OF 2026-01]

