# Position Sizing Methods — Formulas & When to Use

## Method A: Volatility-Adjusted 1/N (Default)

```

Base_Position = Available_Capital / N_Selected_Signals
Vol_Weight[i] = Median_Vol_All / Asset_Vol[i]  // capped at 3.0 max penalty
Adjusted_Position[i] = Base_Position × Vol_Weight[i]
Capped: min(Adjusted_Position, Portfolio_Value × 0.10, $25,000)

```

**When to use:** Always. This is the default. It works with no trade history required.
**When NOT to use:** When you have 50+ trades history AND win_rate > 0.45 → use Kelly instead.

## Method B: Kelly Criterion

```

f* = (b × p - q) / b
where:
  b = avg_win_dollars / avg_loss_dollars (reward-to-risk ratio)
  p = win_rate (historical)
  q = 1 - p (loss_rate)

Half-Kelly: f = f* / 2
Position = Portfolio_Value × f

```

**Requirements:** >50 historical trades for this ticker+strategy. p > 0.45.
**Warning:** Full Kelly is too aggressive. Always use half-Kelly.

## Method C: Risk-Parity

```

Risk_Budget[i] = Target_Portfolio_Risk / N_Selected
Position[i] = Risk_Budget[i] / Asset_Vol[i]

```

**When to use:** Portfolio-level rebalancing where equal risk contribution is the goal.
**Warning:** Risk-parity can over-allocate to low-vol assets. Cap individual position at 10%.

## Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Using full Kelly | Over-bets by 2x; drawdowns 2x expected | Always use half-Kelly |
| Equal weight without vol adjustment | High-vol stocks dominate risk contribution | Apply volatility adjustment |
| Ignoring correlation in sizing | 5 "different" positions = 1 effective bet | Check pairwise correlations |
| No position cap | Single position can exceed 10% | Hard cap at 10% of portfolio |
