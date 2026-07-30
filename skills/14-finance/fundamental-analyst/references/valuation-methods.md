# Valuation Methods — Complete Reference

## Discounted Cash Flow (DCF)

### Formula
Enterprise Value = Σ(FCF_t / (1+WACC)^t) + Terminal Value / (1+WACC)^n

### Steps
1. Project revenue for 5-7 years (conservative growth rate based on industry + market share)
2. Project FCF = EBIT(1-tax) + D&A - Capex - ΔWorking Capital
3. Terminal Value = FCF_n × (1+g) / (WACC - g) where g ≤ risk-free rate + 1%
4. Discount all cash flows to present using WACC
5. Subtract net debt, add cash → Equity Value
6. Equity Value / Shares Outstanding = Fair Value per Share

### WACC Calculation
WACC = (E/V × Re) + (D/V × Rd × (1-t))
- Re = Rf + β × ERP + Size Premium + Company-Specific Risk
- ERP default: 5.0% (Damodaran annual survey)
- β from 5-year monthly regression against S&P 500
- Size premium: 0-6% based on market cap decile

### Critical Checks
- Terminal Value < 70% of total EV. If not, extend forecast or use exit multiple.
- FCF margin should not exceed sustainable industry maximums
- Capex should exceed D&A in terminal year (maintenance capex)

## Comparable Company Analysis
- Select 5-8 peers by: industry, size (±50% market cap), growth rate, margins, geography
- Multiples: EV/EBITDA, EV/Revenue, P/E (adjusted), P/B, P/FCF, PEG
- Use MEDIAN not mean. Report both; flag >20% divergence.
- Apply 25th-75th percentile range to implied valuations

## Graham Number
√(22.5 × EPS × BVPS) — for defensive value investors
Constraints: P/E < 15, P/B < 1.5, Current Ratio > 2.0
Not applicable to: growth companies, financials, negative earnings

## Sector-Specific Methods
- Banks/Financials: P/B + ROE, Dividend Discount Model, Excess Returns Model
- REITs: P/FFO, P/AFFO, NAV (cap rate based)
- SaaS: EV/Revenue with growth-adjusted multiple (Rule of 40)
- Biotech (pre-revenue): rNPV with probability of success per trial phase
- Energy/Cyclicals: Mid-cycle normalized earnings, EV/EBITDA, P/NAV
