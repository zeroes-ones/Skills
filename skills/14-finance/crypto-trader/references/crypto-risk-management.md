# Crypto Risk Management

## Volatility Calibration
| Asset | 30D Realized Vol (typical) | Stress Vol | Notes |
|-------|---------------------------|------------|-------|
| BTC | 40-60% annualized | 100%+ | Declining trend as market matures |
| ETH | 50-80% annualized | 120%+ | Higher beta to crypto cycle |
| SOL | 70-100% annualized | 150%+ | Higher growth beta |
| DeFi tokens | 80-150% annualized | 200%+ | Protocol-specific risk |
| Memecoins | 150-500%+ annualized | 1000%+ | Sentiment-driven |

## Crypto Correlation Matrix (Typical)
| Asset Pair | Normal Regime | Risk-On | Risk-Off |
|------------|--------------|---------|----------|
| BTC-ETH | 0.7-0.85 | 0.6-0.7 | 0.85-0.95 |
| BTC-S&P 500 | 0.2-0.4 | 0.3-0.5 | 0.5-0.7 |
| BTC-Gold | 0.0-0.2 | -0.1-0.1 | 0.1-0.3 |
| BTC-DXY | -0.2--0.4 | -0.1--0.3 | -0.4--0.6 |

## Tail Risk Scenarios
| Scenario | BTC Drawdown | Probability | Trigger |
|----------|-------------|-------------|---------|
| Major CEX failure | -30% to -50% | 2-5%/year | Exchange insolvency, regulatory action |
| Stablecoin systemic depeg | -20% to -40% | 1-3%/year | USDT or USDC loses peg during banking crisis |
| Regulatory crackdown | -20% to -60% | 5-10%/year | US/EU bans or severe restrictions |
| Protocol exploit (major) | -5% to -15% | 10-20%/year | Ethereum client bug, major bridge exploit |
| Global risk-off | -10% to -30% | 15-25%/year | Recession, financial crisis, war |

## Position Sizing Framework
```
Position Size = Account * Risk_Per_Trade / Stop_Loss_Distance
```
- Max risk per trade: 1-2% of account (standard), 0.5% (conservative for crypto)
- Crypto adjustment: Crypto vol = ~3x equity vol → position sizes should be ~1/3 of equity equivalents
- Exchange concentration: Max 20-30% of portfolio on any single CEX

## Provenance
[ESTIMATED] Vol figures and correlations are typical ranges; always verify with current data
[COMPUTED] Position sizing from Kelly Criterion adaptation
[AS OF 2026-01]

