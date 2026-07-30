# Attribution Methodology

## Benchmark Selection Framework
| Strategy Type | Primary Benchmark | Secondary Benchmark |
|--------------|------------------|---------------------|
| US Large Cap Equity | S&P 500 (SPX) | Russell 1000 |
| US Small Cap | Russell 2000 | S&P 600 |
| International Equity | MSCI EAFE or ACWI ex-US | FTSE All-World ex-US |
| Global Equity | MSCI ACWI | FTSE All-World |
| US Aggregate Bond | Bloomberg US Aggregate | ICE BofA US Broad Market |
| High Yield | ICE BofA US HY | Bloomberg US HY |
| Multi-Asset | 60/40 (60% SPX, 40% AGG) | Risk-parity index |
| Hedge Fund | HFRX Global Hedge Fund | HFRI Fund Weighted Composite |
| Crypto | BTC | Bloomberg Galaxy Crypto Index |

## Jensen's Alpha
```
R_portfolio - Rf = α + β * (R_benchmark - Rf) + ε
```
- α (alpha) = risk-adjusted excess return
- β (beta) = market sensitivity
- R² = % of return variation explained by market
- Statistically significant α requires t-statistic > 2 (|α| / SE(α) > 2)

## Fama-French 5-Factor Model
```
R - Rf = α + β1*Mkt + β2*SMB + β3*HML + β4*RMW + β5*CMA + ε
```
| Factor | Name | Construction |
|--------|------|-------------|
| Mkt | Market | Rm - Rf |
| SMB | Small Minus Big | Small-cap returns - Large-cap returns |
| HML | High Minus Low | Value returns - Growth returns |
| RMW | Robust Minus Weak | High-profitability - Low-profitability |
| CMA | Conservative Minus Aggressive | Low-investment - High-investment firms |

Plus Momentum (Carhart 4-factor):
- MOM (Winners Minus Losers): Past 12-month winners - losers

## Sector/Asset Class Attribution
```
Total Excess Return = Σ (w_portfolio,i - w_benchmark,i) * R_benchmark,i + Σ w_portfolio,i * (R_portfolio,i - R_benchmark,i)
```
- Allocation effect: overweight/underweight vs benchmark
- Selection effect: stock/sector selection skill within allocation
- Interaction effect: residual

## Provenance
[VERIFIED] Factor models from Fama-French (1993, 2015), Carhart (1997); attribution from Brinson et al. (1986)
[AS OF 2026-01]

