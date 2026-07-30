# Quality Scores — Piotroski, Altman, Beneish

## Piotroski F-Score (0-9)
Designed for value stocks (high book-to-market). Higher = better financial health.

**Profitability (0-4):**
1. Net Income > 0 (+1)
2. Operating Cash Flow > 0 (+1)
3. ROA increased vs prior year (+1)
4. OCF > Net Income (+1) — earnings quality check

**Leverage/Liquidity (0-3):**
5. Long-term Debt/Assets decreased (+1)
6. Current Ratio increased (+1)
7. No new share issuance (dilution ≤ 0%) (+1)

**Operating Efficiency (0-2):**
8. Gross Margin increased (+1)
9. Asset Turnover increased (+1)

**Interpretation:** 0-3 weak, 4-6 average, 7-9 high quality.
**Limitation:** ROA-based — asset-light companies score high even with high leverage.

## Altman Z-Score
Predicts bankruptcy within 2 years. ~72% accuracy.

Z = 1.2×WC/TA + 1.4×RE/TA + 3.3×EBIT/TA + 0.6×MVE/TL + 1.0×Sales/TA

- Z > 3.0: Safe zone (low bankruptcy probability)
- 1.8 < Z < 3.0: Gray zone (monitor carefully)
- Z < 1.8: Distress zone (high bankruptcy probability)

**For private companies (Z'-Score):** Replace MVE with Book Value of Equity. Thresholds: >2.9 safe, <1.23 distress.
**For non-manufacturing (Z''-Score):** Remove Sales/TA term. Thresholds: >2.6 safe, <1.1 distress.

## Beneish M-Score
Detects earnings manipulation. M > -2.22 suggests manipulation.

M = -4.84 + 0.92×DSRI + 0.528×GMI + 0.404×AQI + 0.892×SGI + 0.115×DEPI - 0.172×SGAI - 0.327×LVGI + 4.679×TATA

- DSRI: Days Sales in Receivables Index (↑ = revenue inflation via channel stuffing)
- GMI: Gross Margin Index (↓ = deteriorating margins, earnings pressure)
- AQI: Asset Quality Index (↑ = capitalization of expenses)
- SGI: Sales Growth Index (high growth companies more likely to manipulate)
- DEPI: Depreciation Index (↓ = extending asset lives to boost earnings)
- SGAI: SG&A Expense Index (↓ = cutting discretionary spending to hit targets)
- LVGI: Leverage Index (↑ = debt covenant pressure)
- TATA: Total Accruals to Total Assets (high accruals = low earnings quality)

M > -2.22: Likely manipulator. M > -1.78: High probability manipulation.

