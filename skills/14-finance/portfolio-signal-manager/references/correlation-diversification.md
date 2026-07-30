# Correlation & Diversification — Beyond GICS

## Economic Driver Taxonomy (Replaces GICS for Risk)

| Economic Driver | GICS Sectors Included | Example Stocks |
|----------------|----------------------|----------------|
| Cloud/Enterprise | Tech, Comm Svc, Consumer Disc | MSFT, AMZN, GOOGL |
| Consumer Discretionary | Consumer Disc, Comm Svc | AAPL, TSLA, NKE |
| Rates-Sensitive | Financials, Real Estate, Utilities | JPM, PLD, DUK |
| Commodity-Exposed | Energy, Materials, Industrials | XOM, FCX, CAT |
| Healthcare | Health Care | JNJ, UNH, PFE |
| Defensive | Consumer Staples, Utilities | PG, WMT, KO |

## When to Use Economic Drivers

- Correlation within the same economic driver averages 0.65 in normal markets
- Correlation across different economic drivers averages 0.30
- During crises: ALL drivers can go to 0.80+ correlation
- True diversification requires at least 4 different economic drivers

## ETF Overlap Check

```

Overlap = (Holdings_A ∩ Holdings_B by weight) / min(Total_Holdings_A, Total_Holdings_B)
If Overlap > 0.90: REJECT — these are effectively the same ETF
If Overlap > 0.70: WARN — significant duplication

```

Examples:
- SPY vs VOO: 99.5% overlap → Same position
- QQQ vs XLK: 65% overlap → Significant duplication
- SPY vs BND: <1% overlap → True diversification

