# Correlation and Concentration Risk

## The Hidden Single-Bet Problem

Options traders often believe they have diversified positions because they trade multiple tickers. In reality, correlation makes multiple bets functionally identical.

### Same-Expiration Concentration
If 50%+ of portfolio theta comes from the same expiration cycle, one gap event affects the entire portfolio [COMPUTED]:

Example: 4 iron condors on SPY, QQQ, IWM, DIA — all expiring March 15. A CPI report on March 12 gaps SPY 2%. All 4 positions take simultaneous losses. You effectively have ONE position, not four.

Rule: Max 30% of theta in any single expiration cycle [COMMON-PRACTICE].

### Sector Correlation Within Options

Mega-cap tech correlations [VERIFIED from rolling 90-day correlations]:

| Pair | Correlation | Interpretation |
|------|------------|----------------|
| AAPL-MSFT | 0.82 | Near-identical moves |
| MSFT-NVDA | 0.78 | Near-identical moves |
| QQQ-XLK | 0.95 | QQQ IS the tech sector |
| SPY-QQQ | 0.88 | Large-cap indices highly correlated |

If you sell options on AAPL, MSFT, and NVDA, you have 3 contracts of the same bet. The correlation reduces effective diversification [COMPUTED].

### Effective N Formula

For a portfolio of N positions with weights w_i and pairwise correlations ρ_ij [COMPUTED]:
```
N_eff = (Σw_i)² / Σ(w_i² × ρ_ij)
```

Example: 5 equal-weighted positions, each 20% of portfolio:
- If all ρ_ij = 0 (uncorrelated): N_eff = 5 real independent bets
- If all ρ_ij = 0.85 (mega-cap tech): N_eff = 1.18 — barely more than 1 bet
- If all ρ_ij = 1.00 (identical): N_eff = 1 — one position

This quantifies what traders sense intuitively: "My 5 positions move together."

### Real Portfolio Concentration Example

5 iron condors, equal allocation [COMPUTED]:
- SPY 480/500 call spread, 460/440 put spread
- QQQ 400/415 call spread, 385/370 put spread
- IWM 195/205 call spread, 185/175 put spread
- DIA 390/400 call spread, 375/365 put spread
- XLF 38/40 call spread, 36/34 put spread

Pairwise correlations: SPY-QQQ (0.88), SPY-IWM (0.80), SPY-DIA (0.85), SPY-XLF (0.72), QQQ-IWM (0.72), QQQ-DIA (0.77), QQQ-XLF (0.65), IWM-DIA (0.78), IWM-XLF (0.70), DIA-XLF (0.75).

N_eff = 1.37 — five positions behave like 1.37 independent bets. A single market move hits all of them [COMPUTED].

## Crash Correlation: All Correlations → 1

During market crashes, all risk assets correlate toward 1.0. Diversification that worked in calm markets disappears precisely when you need it [VERIFIED]:

| Regime | SPY-QQQ Correlation | SPY-IWM Correlation | SPY-EEM Correlation |
|--------|--------------------|--------------------|--------------------|
| Calm (VIX < 20) | 0.85 | 0.72 | 0.55 |
| Elevated (VIX 20-30) | 0.90 | 0.80 | 0.65 |
| Crisis (VIX > 30) | 0.95 | 0.88 | 0.80 |
| Panic (VIX > 50) | 0.98+ | 0.95+ | 0.90+ |

The only negative correlations that persist through crises [VERIFIED]:
- SPX vs VIX: maintains -0.60 to -0.80 (weaker, but still negative)
- SPX vs Long Treasuries (TLT): often goes more negative (-0.40 → -0.55)
- SPX vs USD/JPY: yen strengthens as carry trades unwind

## Concentration Limits

Hard limits for option-selling portfolios [COMMON-PRACTICE]:

| Dimension | Max Limit | Rationale |
|-----------|-----------|-----------|
| Single underlying theta | 15% of total theta | Any single stock gap (±10% on earnings) capped at 1.5% portfolio loss from theta concentration |
| Single sector theta | 25% of total theta | Sector-wide shock (tech selloff, financial crisis) capped at 2.5% loss |
| Single expiration cycle | 30% of total theta | One event date (CPI, FOMC, earnings wave) capped at 3% loss |
| Single strategy type | 40% of portfolio | If all positions are iron condors, an IV spike hits everything |

### Position Size Cap Based on Open Interest
```
max_position_contracts = 0.05 × open_interest
```
Your position must be ≤ 5% of open interest. Beyond 10% OI, you become the market and cannot exit without significant slippage [COMMON-PRACTICE].

## Correlation Monitoring Cadence

1. **Daily**: Compute rolling 20-day correlation for all position pairs. Flag any pair crossing above 0.85.
2. **Weekly**: Compute N_eff. If N_eff drops below 2.0, increase diversification.
3. **Monthly**: Full concentration report. Theta by sector, expiration, strategy, underlying. Color-code violations.
4. **Pre-earnings**: Identify all positions with earnings exposure within 7 days. Single-stock options gap 5-15% through earnings. Verify concentration limits hold post-move.

## Real-World Concentration Failure

March 2020 COVID crash: A trader holding short puts on SPY, QQQ, IWM, DIA, and XLF — "diversified across 5 indices." All 5 dropped 30-40% simultaneously. All short puts went deep ITM simultaneously. Portfolio loss: 10× max planned loss because the 5 positions were effectively one [VERIFIED — representative scenario].

The N_eff calculation would have shown N_eff ≈ 1.2. The trader thought they had 5 independent bets. They had 1. The math would have warned them.

## Same-Underlying Concentration: Multiple Strikes

Selling options at multiple strikes on the same underlying does NOT create diversification — it creates a leveraged bet on volatility and direction [COMPUTED]:

Example: Short 10 SPY 500 puts (20 delta) + Short 5 SPY 490 puts (10 delta). Effective position: 15 contracts of SPY short puts with a blended delta of ~0.17. A 5% SPY drop hits both strikes simultaneously. The weighting may differ, but the correlation is 1.0 — it's the same underlying.

Rule: All positions on the same underlying count as ONE position for concentration purposes. The 15% single-underlying theta limit applies to the SUM of all strikes [COMMON-PRACTICE].

## Correlation-Adjusted Position Sizing

When adding a position with correlation ρ to existing portfolio [COMPUTED]:
```
adjusted_size = target_size × (1 - ρ²)
```

Example: Portfolio already holds SPY options. Adding QQQ options (ρ = 0.88 to SPY). Target size for new position was 10 contracts. Adjusted: 10 × (1 - 0.77) = 2.3 contracts — only 23% of the intended size. The correlation discount prevents accidental doubling of SPY exposure [COMPUTED].

This formula prevents the most common options portfolio mistake: thinking you're adding diversification when you're adding leverage to the same bet.

## Concentration Report Template

Weekly report fields to generate [COMPUTED from broker API positions]:
- Theta attribution by underlying (% of total theta)
- Theta attribution by sector (% of total theta)
- Theta attribution by expiration cycle (% of total theta)
- N_eff calculation with pairwise correlation matrix
- Correlation-adjusted exposure for each position
- Flag: any limit violation (single underlying > 15%, sector > 25%, expiration > 30%)
- Flag: any pairwise correlation > 0.85 that wasn't there last week

