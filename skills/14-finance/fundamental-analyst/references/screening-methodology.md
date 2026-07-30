# Multi-Factor Screening Methodology

## Stock Screen Design Principles
1. Survival bias-free: include delisted stocks in historical validation
2. Sector-neutral: compare within sectors, not across
3. Liquidity floor: market cap > $2B, avg volume > $10M/day
4. Data staleness: financial data must be < 90 days old (post most recent 10-Q/10-K)
5. Look-ahead bias: screen on data available AT THE TIME, not hindsight

## Composite Score Construction
Composite = w1×FCF_Yield_rank + w2×ROIC_rank + w3×F_Score_rank + w4×(-Debt_Equity_rank) + w5×Momentum_rank

Default weights (equal): w1=w2=w3=w4=w5=0.2
Value tilt: w1=0.3, w2=0.2, w3=0.2, w4=0.2, w5=0.1
Quality tilt: w1=0.15, w2=0.25, w3=0.3, w4=0.2, w5=0.1

## Sector-Specific Adjustments
- Financials: replace Debt/Equity with Tier 1 Capital Ratio, use P/B instead of EV/EBITDA
- REITs: use P/FFO instead of P/E, Debt/EBITDA instead of Debt/Equity
- Tech: emphasize FCF yield and ROIC, de-emphasize P/B (asset-light)
- Energy: use EV/EBITDA on mid-cycle earnings, not trailing
- Biotech: separate pre-revenue (burn rate + catalyst timeline) from profitable

## Performance Attribution
After running screen, decompose performance:
1. How much came from factor exposure vs. stock selection?
2. Which factor contributed most? (FCF yield? F-Score? Momentum?)
3. Is the factor premium stable across market regimes?

## Rebalancing Schedule
- Quarterly rebalance: standard (aligns with earnings releases)
- Monthly: more trading costs, marginal improvement
- Annual: stale — factor decay at 6+ months
