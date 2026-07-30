# Global Liquidity Measurement

## G4 Central Bank Balance Sheet Aggregation
```
G4 Total = Fed + ECB + BOJ + PBoC (in USD terms)
```
| Central Bank | Peak (USD) | Current Trend | Key Assets |
|-------------|-----------|---------------|------------|
| Fed | ~$9T (Apr 2022) | QT: -$95B/month | Treasuries, MBS |
| ECB | ~€8.8T (2022) | QT: PEPP reinvestment ended | Bonds, TLTROs |
| BOJ | ~¥760T (2024) | Still expanding | JGBs, ETFs |
| PBoC | ~¥40T | Easing via RRR/MLF | Loans to banks (not QE) |

## Liquidity Impulse Calculation
```
3-month change annualized = (Current - 3mo_ago) / 3mo_ago * 4 * 100
```
Positive = liquidity tailwind for risk assets
Negative = liquidity headwind

## Financial Conditions Indices
| Index | Provider | Components | Interpretation |
|-------|----------|-----------|----------------|
| GS FCI | Goldman Sachs | Rates, credit, equity, dollar | >100 = tightening |
| Chicago Fed NFCI | Fed | Money market, debt, equity, banking | >0 = tighter than avg |
| Bloomberg FCI | Bloomberg | Money market, bond, equity | Proprietary scale |

## Real Rate Decomposition
```
Real Rate = Nominal Yield - Inflation Expectations
```
- **TIPS-based**: 10Y Nominal - 10Y TIPS = breakeven inflation
- **Inflation swap-based**: 5Y5Y forward inflation swap
- **Policy real rate**: Fed Funds - Core PCE YoY

## Global Capital Flow Tracking
| Data Source | Frequency | Coverage | Lag |
|------------|-----------|----------|-----|
| TIC Data (US Treasury) | Monthly | Foreign flows into US | ~6 weeks |
| EPFR | Weekly | Fund flows by asset class/region | 3 days |
| IIF | Monthly | EM portfolio flows | 3-4 weeks |
| Central bank reserve data | Quarterly | FX reserve composition | ~3 months |

## Provenance
[VERIFIED] Balance sheet data from Fed, ECB, BOJ, PBoC websites; FCI methodology from provider docs
[AS OF 2026-01 — VERIFY LATEST BALANCE SHEETS]

