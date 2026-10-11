# Expectancy Math for Retail Options

## Core formulas

```
E (in R)   = p·W − (1−p)·L                     # R = max loss of the position
E ($)      = E(R) × R$
R-multiple = (exit − entry) / (max loss)      # for debits: gain / debit paid
Kelly f*   = edge / odds                       # edge = p·b − (1−p), odds b = W/L
Half-Kelly = f*/2                             # the practical cap for uncertain p
```

## Base-rate anchors (use these, don't invent 70%)

| Setup | Typical honest p | Typical W | Typical L (with bands) |
|---|---|---|---|
| Momentum fly, rungs at 1.8–2.5× | 0.40–0.50 | +1.0 to +1.5 R | −0.8 to −1.0 R |
| Directional single, TP at 1.8× | 0.35–0.45 | +0.8 R | −1.0 R |
| Long-dated LEAP, liquid name | 0.50–0.60 | +0.7 R | −0.8 R |
| Premium-selling defined spreads | 0.60–0.70 | +0.5 R | −1.0 to −1.5 R |

If your assumption needs p > 0.60 or W > 2R to show positive E, the trade is probably not real — you're fitting numbers to desire.

## Streak arithmetic (why size, not skill, decides survival)

Probability of k consecutive losses at p(win)=0.45:

| Streak | Probability | Drawdown at 1.5%/trade | Drawdown at 10%/trade |
|---|---|---|---|
| 3 | ~17% | −4.5% | −27% |
| 5 | ~5% | −7.2% | −41% |
| 8 | ~0.8% | −11.4% | −57% |
| 10 | ~0.25% | −14.0% | −65% |

At 10% sizing, a 1-in-400 streak costs two-thirds of the account and needs +185% to recover. At 1.5%, even a brutal streak is a normal drawdown. **Real streaks are far more common than these baseline numbers** because signals correlate — count correlated positions as one bet.

## Half-Kelly sanity check (worked)

p = 0.45, W = +1.2R, L = −1.0R ⇒ b = 1.2, edge = 0.45×1.2 − 0.55 = −0.01 → **negative E; do not trade this configuration**. Raise W (better rungs) or raise p (better gates) first; sizing never fixes negative E.
