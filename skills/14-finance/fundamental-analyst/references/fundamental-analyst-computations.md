# Fundamental Analyst — Full Computation Reference

---

## Core Workflow

<!-- STANDARD: 3min -->

### Phase 1: Valuation — Determine Intrinsic Value Range

```

1. GATHER FINANCIAL DATA (3+ years)
   ├── Income Statement: Revenue, Gross Profit, Operating Income, Net Income, EPS (GAAP + Adjusted)
   ├── Balance Sheet: Total Assets, Total Liabilities, Debt (short + long), Equity, Working Capital
   ├── Cash Flow: Operating CF, Capex, FCF (= OCF - Capex), Share Buybacks, Dividends
   └── Footnotes: One-time items, segment breakdowns, related-party transactions, off-balance-sheet obligations

   Complete when: 3+ fiscal years of all 3 statements collected. One-time items identified and isolated.

2. BUILD DCF MODEL (3 scenarios)
   ├── Revenue Projection (5 years): based on historical CAGR, industry growth, market share
   ├── FCF Projection: Revenue × FCF margin (historical avg ± sensitivity)
   ├── Terminal Value: Gordon Growth Model (FCF_year5 × (1+g) / (WACC - g))
   │   └── g = risk-free rate (10Y Treasury) to risk-free + 2% (no higher)
   ├── WACC: CAPM → Rf + β × ERP + size premium + company-specific risk
   │   └── ERP default 5.0%, β from 5Y monthly regression against SPY
   └── DISCOUNT: FCF_t / (1+WACC)^t + TV / (1+WACC)^5

   SCENARIOS:
   ├── BEAR: Revenue growth -30% below base, FCF margin -200bps, WACC +100bps
   ├── BASE: Revenue growth = conservative estimate, FCF margin = 3Y avg, WACC = computed
   └── BULL: Revenue growth +30% above base, FCF margin +200bps, WACC -100bps

   Complete when: DCF range produced (bear/base/bull). All assumptions documented.

3. COMPARABLE COMPANY ANALYSIS
   ├── Select 5-8 comparable companies (industry, size, growth rate, margins)
   ├── Compute multiples: EV/EBITDA, PE (adjusted), PB, EV/Revenue, PEG, FCF Yield
   ├── Apply MEDIAN multiples (NOT mean — outliers skew mean)
   └── Range: 25th percentile to 75th percentile of implied values

4. GRAHAM NUMBER (value floor — for mature, profitable companies only)
   Graham Number = √(22.5 × EPS × BVPS)
   Valid only when: PE < 15, PB < 1.5. Do NOT use for growth companies or negative-earnings companies.

   Complete when: Valuation range triangulated from DCF + comparables + Graham floor.

```

### Phase 2: Financial Statement Analysis

```

1. PROFITABILITY ANALYSIS
   ├── Gross Margin trend (3-5 years): expanding = pricing power, contracting = competition
   ├── Operating Margin trend: expanding = operating leverage, contracting = cost pressure
   ├── Net Margin: check for one-time items distorting bottom line
   ├── ROE (DuPont): Net Margin × Asset Turnover × Equity Multiplier
   │   └── ROE rising from leverage alone (equity multiplier ↑) = WARNING
   ├── ROIC = NOPAT / Invested Capital: must exceed WACC for value creation
   └── FCF Yield = FCF / Market Cap: > 5% = cheap, > 8% = very cheap, > 10% = investigate why

2. FINANCIAL HEALTH ANALYSIS
   ├── Current Ratio: current assets / current liabilities > 1.5
   ├── Debt/Equity < 2.0 (ex-financials); Debt/EBITDA < 3.0
   ├── Interest Coverage: EBIT / Interest Expense > 3.0
   ├── FCF / Debt: ability to pay down debt from operations
   └── Altman Z-Score: > 3.0 safe, 1.8-3.0 gray, < 1.8 distress

3. EARNINGS QUALITY ANALYSIS
   ├── Accruals Ratio: (Net Income - FCF) / Total Assets — persistent negative = red flag
   ├── Revenue vs Receivables: receivables growing faster than revenue = channel stuffing
   ├── Depreciation / Capex ratio: < 1.0 = under-investing (consuming assets)
   └── Beneish M-Score: > -2.22 = potential manipulation

   Complete when: All ratios computed. Red flags documented with specific numbers.

```

### Phase 3: Quality Scoring

```

1. PIOTROSKI F-SCORE (0-9) — for value stocks (high B/M ratio)
   PROFITABILITY (0-4):
   ├── +1: Positive Net Income
   ├── +1: Positive Operating Cash Flow
   ├── +1: ROA increased vs prior year
   └── +1: OCF > Net Income (earnings quality)

   LEVERAGE/LIQUIDITY (0-3):
   ├── +1: Long-term Debt/Assets decreased vs prior year
   ├── +1: Current Ratio increased vs prior year
   └── +1: No new share issuance (dilution)

   OPERATING EFFICIENCY (0-2):
   ├── +1: Gross Margin increased vs prior year
   └── +1: Asset Turnover increased vs prior year

   SCORE: 0-3 = weak, 4-6 = average, 7-9 = high quality

2. ALTMAN Z-SCORE (bankruptcy risk within 2 years)
   Z = 1.2×WC/TA + 1.4×RE/TA + 3.3×EBIT/TA + 0.6×MVE/TL + 1.0×Sales/TA
   ├── Z > 3.0: Safe zone
   ├── 1.8 < Z < 3.0: Gray zone (monitor)
   └── Z < 1.8: Distress zone (high bankruptcy probability)

3. BENEISH M-SCORE (earnings manipulation)
   M = -4.84 + 0.92×DSRI + 0.528×GMI + 0.404×AQI + 0.892×SGI + 0.115×DEPI
       - 0.172×SGAI - 0.327×LVGI + 4.679×TATA
   ├── M > -2.22: Likely manipulator
   └── M < -2.22: Unlikely manipulator

4. TRIANGULATION RULE
   F-Score ≥ 7 AND Z-Score > 3.0 AND M-Score < -2.22 = HIGH QUALITY
   F-Score ≤ 3 OR Z-Score < 1.8 OR M-Score > -1.78 = HIGH RISK — do not buy regardless of valuation

   Complete when: All three scores computed. Quality label assigned.

```

### Phase 4: Fundamental Buy/Sell Signal Generation

```

1. VALUATION SIGNAL
   Compare current price to intrinsic value range:
   ├── Price < Bear Case: STRONG BUY (margin of safety even in worst scenario) — confidence 80
   ├── Price < Base Case: BUY (margin of safety in base scenario) — confidence 60
   ├── Price between Base and Bull: HOLD (fairly valued) — confidence 50
   ├── Price > Bull Case: OVERVALUED — confidence 40
   └── Price > 1.5x Bull Case: STRONG SELL — confidence 75

2. QUALITY SIGNAL
   Quality score modifies valuation signal:
   ├── High Quality: reinforce buy, dampen sell
   ├── Average Quality: neutral
   └── Low Quality: dampen buy (value trap risk), reinforce sell

3. DIVIDEND SIGNAL (for dividend-paying stocks)
   ├── Dividend Yield > 3% AND Payout Ratio < 60% AND 5Y Dividend Growth > 5% → DIVIDEND BUY
   ├── Payout Ratio > 80% → UNSUSTAINABLE — cut risk high
   ├── Dividend cut in past 3 years → DIVIDEND RISK — reduce confidence 20
   └── FCF < Dividend Payments → FINANCING DIVIDENDS WITH DEBT — red flag

4. MOMENTUM OVERLAY (business momentum, not price momentum)
   ├── Revenue Growth Accelerating (3Y CAGR > 5Y CAGR): +10 confidence
   ├── Margin Expanding (last year > 3Y avg): +10 confidence
   ├── Revenue Growth Decelerating: -10 confidence
   └── Margin Contracting: -10 confidence

5. FINAL SIGNAL OUTPUT
   {
     "ticker": "AAPL",
     "signal_type": "BUY",
     "confidence": 68,
     "valuation": {
       "method": "DCF + Comparables",
       "bear_case": 155,
       "base_case": 185,
       "bull_case": 220,
       "current_price": 170,
       "margin_of_safety": "8.8% below base case"
     },
     "quality": {
       "piotroski_f_score": 7,
       "altman_z_score": 5.2,
       "beneish_m_score": -2.8,
       "quality_label": "HIGH"
     },
     "key_ratios": {
       "pe_trailing": 28.5,
       "pe_forward": 24.1,
       "peg_ratio": 1.8,
       "ev_ebitda": 18.2,
       "fcf_yield": 0.041,
       "roe": 0.52,
       "debt_equity": 1.4
     },
     "red_flags": [],
     "earnings_date": "2026-10-27"
   }

   Complete when: Signal generated with all required fields.

```

### Phase 5: Multi-Stock Screening

```

1. SCREEN PARAMETERS (user-specified or defaults)
   ├── Market Cap: > $2B (avoid micro-cap manipulation)
   ├── Avg Volume: > $10M/day (liquidity)
   ├── FCF Yield: > 3% (positive cash generation)
   ├── Debt/Equity: < 2.0 (financial health)
   ├── ROIC > WACC (value creation)
   └── Piotroski F-Score: ≥ 5 (quality floor)

2. RANK METHODOLOGY
   Composite Score = normalized(FCF_Yield) + normalized(ROIC) + normalized(F_Score) - normalized(Debt_Equity)

3. OUTPUT
   Top 20 ranked by composite score with:
   ├── Composite Score, FCF Yield, ROIC, PE, EV/EBITDA, Debt/Equity, F-Score, Z-Score
   └── Sorted by composite score descending

   Complete when: Screen results ranked and output with all columns.

```


   Complete when: [VERIFIED] All positions sized within capital constraints.
   Complete when: [VERIFIED] Correlation matrix checked and N_effective > 3.
   Complete when: [VERIFIED] Circuit breakers armed and tested.
   Complete when: [VERIFIED] Broker connection in READY state.
   Complete when: [VERIFIED] No sector exceeds 25% exposure.
   Complete when: [VERIFIED] Stop-losses set for all open positions.
