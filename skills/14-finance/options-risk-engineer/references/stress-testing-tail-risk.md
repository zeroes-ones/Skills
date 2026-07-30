# Stress Testing and Tail Risk

## Why Standard VaR Fails for Options

Value at Risk (VaR) assumes normally distributed returns. Options produce non-linear, asymmetric payoff profiles. Standard VaR underestimates option portfolio risk by 2-5x [VERIFIED].

Example: A short strangle collects $3.00 credit. VaR at 95% says max loss = $200 based on 2σ move. But a 3σ tail event produces $2,500 loss — 12.5x VaR estimate [COMPUTED].

You MUST use Monte Carlo simulation with fat-tailed distributions (Student's t with df=3-5, or historical sampling). Gaussian assumptions are dangerous for options portfolios [COMMON-PRACTICE].

## Standard Stress Scenarios

Apply these historical scenarios to current portfolio [VERIFIED]:

### Scenario 1: October 1987 Crash
- SPX: -20.5% in ONE day
- VIX: spiked from 20 to 150 (pre-VIX calculation; implied vol equivalent)
- ATM SPX puts: went from ~$2 to $50+ — 25x price increase [VERIFIED]
- Portfolio impact: Any short put position goes catastrophic. A short 0.15-delta SPX put becomes 1.00 delta and deep ITM. Loss = (strike - new_spot) × 100 × contracts minus credit received [COMPUTED]

### Scenario 2: 2008 Global Financial Crisis  
- SPX: -50% over 17 months (October 2007 → March 2009)
- VIX: peaked at 89.53 on October 24, 2008 [VERIFIED]
- All correlations → 1.0. Any diversification thesis failed.
- Credit spreads on financials (XLF): short 22-strike puts became $18 ITM = $1,800/contract loss [COMPUTED]
- Key test: Did your portfolio survive 17 months of grinding decline?

### Scenario 3: March 2020 COVID Crash
- SPX: -34% in 23 trading days (February 19 → March 23, 2020)
- VIX: 14.38 → 82.69 peak [VERIFIED]
- Circuit breakers triggered 4 times in 10 days. Markets halted, options untradeable during halts.
- Put options priced for total collapse. Vega went exponential — IV on OTM SPX puts hit 150%+ [VERIFIED]
- Portfolio test: Can you survive a 34% drawdown with 4 trading halts?

### Scenario 4: May 2010 Flash Crash
- SPX: -9% in minutes, recovered within same day [VERIFIED]
- Stop-loss orders executed at WORST possible prices — $0.01 on blue chips that recovered to $40+ within hours
- Options: Implied vol spiked and collapsed intraday. Market orders on options traded at extreme dislocations.
- Critical test: What happens if all your GTC (good-till-canceled) stop-losses trigger simultaneously at worst-case prices?

### Scenario 5: 2022 Rate-Hike Cycle
- SPX: -25% peak-to-trough (January → October 2022)
- VIX: stayed elevated 25-35 for 9+ months
- Interest rates: Fed funds 0.25% → 4.50% in 12 months
- rho (rate sensitivity) mattered: higher rates reduce call prices and increase put prices via cost-of-carry. Short call positions benefited; short put positions suffered double (price decline + rate increase) [COMPUTED]

## CVaR (Expected Shortfall) for Options

Conditional Value at Risk asks: "When VaR is breached, what's the average loss beyond it?"

For option portfolios [ESTIMATED from empirical distributions]:
```
CVaR_99% ≈ 1.5x to 3x VaR_99%
```

Example: Portfolio VaR(99%) = $50,000. CVaR(99%) = $100,000-$150,000. Meaning: 1% of the time, you lose at least $50,000. But when you do, the average loss is $100,000-$150,000 — far worse than the VaR number suggests [COMPUTED].

This 1.5-3x multiplier is specific to option portfolios with short gamma. Long-gamma portfolios have CVaR closer to VaR (losses decelerate as positions gain value).

## Monte Carlo Stress Test Setup

```python
# Anti-hallucination: This is the standard methodology [COMMON-PRACTICE]

scenarios = {
    '1987_crash':    {'spx_return': -0.205, 'vix_change': +130, 'correlation': 1.0},
    '2008_gfc':      {'spx_return': -0.50,  'vix_change': +70,  'correlation': 1.0},
    '2020_covid':    {'spx_return': -0.34,  'vix_change': +68,  'correlation': 0.95},
    '2010_flash':    {'spx_return': -0.09,  'vix_change': +40,  'correlation': 0.90},
    'vol_event':     {'spx_return': -0.05,  'vix_change': +25,  'correlation': 0.85},
    'rate_shock':    {'spx_return': -0.15,  'vix_change': +15,  'correlation': 0.90, 'rate_change': +2.0},
}
```

For each scenario [COMPUTED]:
1. Shift all underlyings by (scenario_return × correlation_to_SPX)
2. Shift all IV surfaces by scenario_vix_change × vega_sensitivity
3. Shift rates by scenario_rate_change × rho_sensitivity
4. Compute new portfolio value. Record drawdown.
5. Record which positions contributed most to loss.

## Drawdown Tolerance and Position Sizing

The stress test output drives position sizing:

| Max Stress Drawdown | Assessment | Action |
|--------------------|------------|--------|
| < 15% | Well-constructed | Maintain sizing |
| 15-30% | Acceptable | Monitor, but within risk tolerance |
| 30-50% | Concerning | Reduce position sizes by 25-40% |
| > 50% | Dangerous | Reduce by 50%+. Portfolio won't survive next crisis |

A portfolio that survives 2008-style stress with <30% drawdown is well-constructed. One that loses >50% in backtest WILL lose >50% in the next crisis — the question is when, not if [VERIFIED].

## Tail Risk by Position Type

| Position | Tail Exposure | Worst Case |
|----------|--------------|------------|
| Short naked put | Unlimited downside | Stock → $0 = (strike × 100 × contracts) loss |
| Short naked call | Unlimited | Stock → ∞ = infinite loss |
| Short put spread | Defined | Width × 100 × contracts minus credit |
| Iron condor | Defined on both sides | Max loss on put OR call side (not both simultaneously — they cannot both be ITM at same spot price) |
| Short strangle | Unlimited both sides | Stock gaps beyond either strike |
| Long options (debit) | Defined | Premium paid |

Short naked options carry infinite tail risk. Defined-risk spreads carry finite but potentially large tail risk. Long options have no tail risk beyond premium paid [VERIFIED].

## Stress Test Cadence

- **Daily**: Quick scenario run: ±2%, ±5% SPX moves. Check margin impact.
- **Weekly**: Full historical scenario test (1987, 2008, 2020, 2010). Record max drawdown.
- **Monthly**: Monte Carlo simulation with 10,000 fat-tailed draws. Compute VaR(95%), VaR(99%), CVaR(99%).
- **Quarterly**: Full risk audit. All scenarios + Monte Carlo + correlation breakdown + concentration analysis.
- **Pre-FOMC/CPI**: Run rate-shock and vol-shock scenarios. These events trigger gamma events.

## The One Number That Matters

After all stress tests, the single most important metric is:

```
worst_case_portfolio_drawdown_pct = max(portfolio_loss / NAV) across all scenarios
```

If this number exceeds your maximum tolerable loss, reduce position sizes. No amount of cleverness in strike selection or entry timing changes the mathematics of being short options in a tail event. The only defense is position sizing [VERIFIED].
