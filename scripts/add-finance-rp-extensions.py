#!/usr/bin/env python3
"""
Add domain-specific RESEARCH_PREREQUISITE extensions to finance/trading skills.
These go AFTER the universal RP section and add market-specific research steps.
"""
import os, sys, re

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Domain-specific RP extensions per skill
FINANCE_EXTENSIONS = {
    'algorithmic-trader': """
### Trading Domain Extension — Execute These ADDITIONAL Research Steps

| # | Research Step | Why It Matters | Where to Look |
|---|--------------|----------------|----------------|
| **RP-F1** | **Validate backtest integrity.** Check for look-ahead bias, survivorship bias, overfitting (parameters > data points), and walk-forward vs. in-sample performance divergence. | [OVERFITTING_RISK] A backtest with 95% win rate on 7 parameters over 100 trades is curve-fit noise. Walk-forward validation that drops from 95% to 52% exposes the illusion. Every backtest must survive out-of-sample testing. | Backtest engine logs, parameter count vs. trade count ratio |
| **RP-F2** | **Benchmark execution assumptions.** Verify slippage estimates (default: 0.05% for liquid, 0.5% for illiquid), commission schedules, and fill probability against real broker data. | [EXECUTION_GAP] A strategy that returns +18% in simulation with zero slippage returns +9% in production with real fills. The execution gap is real and quantifiable — ignore it at your capital's peril. | Broker fill reports, bid-ask spread history, TCA (Transaction Cost Analysis) |
| **RP-F3** | **Check exchange rules and circuit breakers.** Verify that strategy parameters (DTE, strike width, position size) comply with exchange limits, margin requirements, and circuit breaker thresholds. | [EXCHANGE_REJECTION] Strategies that violate exchange rules fail silently in simulation and catastrophically in production. A position too large for the market maker to fill = partial fill at worst price. | Exchange rulebooks, broker API limits, Reg T/portfolio margin rules |
| **RP-F4** | **Stress-test against historical tail events.** Run the strategy against March 2020, October 1987, August 2015 flash crash, and 2008 financial crisis data. Document max drawdown in each. | [TAIL_BLINDNESS] A strategy that never saw a crash in backtest WILL face one in production. Historical tail events are the cheapest stress tests available — use them. | Historical market data, VIX spike periods, flash crash dates |
| **RP-F5** | **Verify strategy capacity.** Compute estimated market impact at current position size. If AUM/strategy capacity > 50%, returns will degrade from slippage alone. | [CAPACITY_CEILING] A market-neutral strategy that works at $500K may break at $50M. Market impact is nonlinear — doubling size more than doubles impact. | Average daily volume (ADV), bid-ask spread as % of price, depth of book |
""",

    'options-risk-engineer': """
### Risk Domain Extension — Execute These ADDITIONAL Research Steps

| # | Research Step | Why It Matters | Where to Look |
|---|--------------|----------------|----------------|
| **RP-F1** | **Compute full portfolio VaR and CVaR.** Calculate 95% and 99% Value-at-Risk AND Conditional VaR (expected loss beyond VaR). Regime-adjust using current VIX level. | [VAR_ILLUSION] VaR tells you what happens on a bad day. CVaR tells you what happens on a CATASTROPHIC day. The difference is often 5×. A portfolio that passes VaR can fail CVaR. | Portfolio Greeks, VIX term structure, historical stress test data |
| **RP-F2** | **Map correlation matrix across all open positions.** Compute pairwise correlations. Identify clusters: are 3+ positions in the same sector/strategy type? If so, they are NOT diversified regardless of ticker. | [CORRELATION_COLLAPSE] In a crash, correlations converge to ~0.92 for short-premium strategies. Five iron condors on five different stocks = ONE position with 5× leverage. True diversification crosses the short/long boundary. | Pattern Recognition Engine §Correlation Collapse, position database |
| **RP-F3** | **Verify margin requirements under stress.** What happens to margin requirements if VIX doubles? If correlation collapses? If the portfolio takes a 3-sigma hit? | [MARGIN_CALL] Margin requirements expand precisely when capital is scarce. A strategy that uses 60% of margin today may use 180% during a crash — triggering forced liquidations at the worst possible price. | Broker margin formulas, SPAN/portfolio margin documentation, VIX-margin correlation data |
| **RP-F4** | **Check for pin risk and expiration concentration.** Are multiple positions expiring on the same date? Are any short strikes within 2% of current price on expiration day? | [PIN_CATASTROPHE] A short option $0.01 OTM at Friday close can gap $5 against you by Monday. The last $0.05 of premium is NEVER worth the gap risk. | Options chain, expiration calendar, position delta-at-expiration |
| **RP-F5** | **Compute the portfolio convexity profile.** Is the overall portfolio long gamma (profits accelerate on large moves) or short gamma (losses accelerate)? Short gamma portfolios MUST have stop-losses — unlimited loss is not theoretical. | [CONVEXITY_ASYM] Short gamma portfolios (iron condors, credit spreads, naked options) carry tail risk that standard deviation-based measures miss entirely. A 4-sigma move in a short-gamma portfolio is NOT a 1-in-10,000-year event — it happens every 5-10 years. | Greeks surface, strategy convexity table, historical drawdown data |
""",

    'portfolio-signal-manager': """
### Portfolio Domain Extension — Execute These ADDITIONAL Research Steps

| # | Research Step | Why It Matters | Where to Look |
|---|--------------|----------------|----------------|
| **RP-F1** | **Resolve all active signal conflicts.** For every pair of conflicting signals (e.g., technical says BUY, macro says SELL), document the resolution logic. Signal conflicts that go unresolved produce contradictory position changes. | [SIGNAL_CONFLICT] A portfolio with 3 bullish signals and 2 bearish signals on the same asset has a net signal of zero — not bullish. Unresolved conflicts cause whipsaw: buy on one signal, sell on the next, accumulate transaction costs. | Signal dashboard, conflict resolution matrix, priority hierarchy |
| **RP-F2** | **Check circuit breaker thresholds.** Verify: drawdown limit (default: 15% from peak), single-position loss limit (default: 5%), correlation-based concentration limit (default: 30% in any sector), and daily loss limit (default: 3%). | [DRAWDOWN_SPIRAL] Without hard circuit breakers, a 10% drawdown becomes 20% becomes 40%. Each recovery requires progressively larger gains: -10% needs +11%, -20% needs +25%, -40% needs +67%. | Circuit breaker configuration, account drawdown history, daily P&L reports |
| **RP-F3** | **Rebalance check: are current allocations within tolerance bands?** Compare target weights vs. actual weights. Positions that have drifted >20% from target need rebalancing evaluation (cost vs. drift risk). | [DRIFT_RISK] A 5% tactical allocation that grows to 15% through outperformance has become a 15% strategic bet without a decision. Rebalancing isn't about locking in profits — it's about maintaining intended risk exposure. | Position sizing sheet, allocation targets, tax-impact analysis |
| **RP-F4** | **Assess liquidity of all holdings.** For each position: what % of ADV does the position represent? If any position > 5% of ADV, exiting will move the market against you. | [LIQUIDITY_TRAP] A profitable position you can't exit without crashing the price is not a position — it's a hostage situation. Liquidity risk is the most underestimated portfolio risk. | ADV data, bid-ask spread history, depth of market |
| **RP-F5** | **Stress-test the portfolio against the last 3 regime shifts.** Apply the portfolio composition to: (a) the most recent correction (-10%), (b) the most recent bear market (-20%), (c) the most recent crash (-30%+). Document max portfolio drawdown in each. | [REGIME_FRAGILITY] A portfolio optimized for the current regime is fragile by definition. Regime-agnostic portfolios survive; regime-optimized portfolios get destroyed when the regime changes — which it always does. | Historical regime dates, strategy backtest data, composite portfolio P&L simulation |
""",

    'technical-signals-engineer': """
### Technical Domain Extension — Execute These ADDITIONAL Research Steps

| # | Research Step | Why It Matters | Where to Look |
|---|--------------|----------------|----------------|
| **RP-F1** | **Validate multi-timeframe confluence.** Check: weekly trend, daily trend, 4-hour momentum alignment. A daily buy signal against a weekly downtrend has a ~35% false signal rate vs. ~15% when aligned. | [TIMEFRAME_CONFLICT] Single-timeframe signals are noise. A golden cross on the 15-minute chart means nothing if the weekly is in a death cross. Multi-timeframe alignment is the cheapest signal quality filter. | Multi-timeframe dashboard, false signal database by timeframe combination |
| **RP-F2** | **Calculate the false signal rate for each indicator in current regime.** RSI oversold signals have ~40% false positive rate in downtrends vs. ~15% in uptrends. MACD crossovers generate ~60% more false signals in low-VIX environments. | [FALSE_SIGNAL_COST] Every false signal costs: spread + commission + opportunity cost of being in the wrong position. At $5/trade with 40% false signals on 100 signals/year, that's $200/year in false-signal commissions alone — 0.4% drag on a $50K account. | Backtest signal database, regime-specific performance metrics |
| **RP-F3** | **Quantify indicator lag.** Moving average crossovers lag price by MA_period/2 on average. A 50-day SMA crossover signal is ~25 days late. MACD (12/26/9) introduces ~9-13 periods of lag. | [LAG_PENALTY] Lag transforms "buy low" into "buy after the move already happened." The profit left on the table by indicator lag is often larger than the profit captured by the signal. | Indicator lag calculations, lead-lag analysis against price |
| **RP-F4** | **Detect the current regime before applying indicators.** Trend-following indicators (MACD, moving averages) fail in ranges. Mean-reversion indicators (RSI, Bollinger Bands) fail in trends. Applying the wrong indicator family to the current regime destroys alpha. | [REGIME_MISMATCH] The #1 misuse of technical analysis: applying trending indicators to a ranging market (whipsaw losses) or mean-reversion indicators in a trending market (fading a freight train). Regime detection FIRST, indicator selection SECOND. | Pattern Recognition Engine §Regime Detection, ADX readings, volatility regime classification |
| **RP-F5** | **Backtest each signal against out-of-sample data.** A signal that worked in 2020-2023 may fail in 2024-2026. Markets adapt. Walk-forward testing reveals signal decay. | [OVERFITTING] Technical indicators have parameters. Optimizing parameters on historical data without out-of-sample validation is curve-fitting. The optimal RSI period for 2020 is not the optimal period for 2025. | Walk-forward backtest framework, parameter stability analysis |
""",

    'quantitative-analyst': """
### Quantitative Domain Extension — Execute These ADDITIONAL Research Steps

| # | Research Step | Why It Matters | Where to Look |
|---|--------------|----------------|----------------|
| **RP-F1** | **Calibrate the pricing model.** Verify: risk-free rate (current Treasury yield for matching tenor), dividend yield (trailing + forward consensus), and implied borrow cost (hard-to-borrow fee schedule). Mispricing by 50bp on any input compounds across the position. | [GARBAGE_IN] The most elegant pricing model with wrong inputs produces garbage. A Black-Scholes price using the wrong risk-free rate is mathematically correct and financially wrong. | Treasury yield curve, dividend calendars, broker borrow fee schedules |
| **RP-F2** | **Construct the full volatility surface.** Plot IV by strike and expiration. Check for: skew (OTM puts vs. OTM calls), term structure (contango vs. backwardation), and smile/smirk asymmetry. | [FLAT_VOL_FALLACY] Treating volatility as a single number ignores the surface. The ATM IV might be 25% while the 25-delta put IV is 32% — that 7-point skew is where edge lives or dies. | Options chains across all strikes and expirations, vol surface visualization |
| **RP-F3** | **Compute position sizing via Kelly Criterion.** f* = (bp − q) / b. Cap at 25% Kelly for real execution. Regime-adjust: 25% Kelly in bull, 15% in correction, 10% in bear, 5% in crash. | [OVERBETTING] Full Kelly is optimal for log-utility in theory and ruinous in practice. Parameter uncertainty, non-normal returns, and gap risk make full Kelly a path to eventual blow-up. 25% Kelly is the practical maximum. | Kelly calculator, strategy win rate and win/loss ratio data |
| **RP-F4** | **Validate that the Greeks tell a coherent story.** Delta ≈ directional exposure. Gamma ≈ acceleration (how fast delta changes). Theta ≈ daily cost of holding. Vega ≈ IV sensitivity. A position with positive gamma, negative theta, and high vega is a long vol position — confirm this aligns with the strategy thesis. | [GREEKS_CONTRADICTION] A strategy that claims to be "directionally neutral" but has net delta of +0.30 on a $100K notional has $30K of directional exposure. The Greeks don't lie — they reveal what the strategy ACTUALLY does vs. what it CLAIMS to do. | Greeks calculator, position summary, strategy thesis document |
| **RP-F5** | **Check for early exercise and assignment risk.** American-style options can be exercised at any time. Check: dividends (calls exercised pre-ex-div), hard-to-borrow (puts exercised to capture borrow rebate), deep ITM (assignment probability rises with moneyness). | [EARLY_EXERCISE] Early assignment transforms a defined-risk spread into an undefined-risk short stock position overnight. A short call assigned on ex-div eve = you owe the dividend. | Dividend calendar, short interest data, ITM depth analysis |
""",

    'market-data-engineer': """
### Market Data Domain Extension — Execute These ADDITIONAL Research Steps

| # | Research Step | Why It Matters | Where to Look |
|---|--------------|----------------|----------------|
| **RP-F1** | **Validate data quality: check for missing ticks, duplicate bars, timestamp gaps, and price outliers.** A single bad tick (price = $0.01 for one millisecond) can corrupt an entire backtest. | [GARBAGE_IN_GARBAGE_OUT] Data quality issues are the silent killers of production trading systems. A strategy that "works" on dirty data works on fiction. Every data quality issue that reaches production is a future P&L loss waiting to happen. | Data quality dashboard, tick-level audit logs, outlier detection reports |
| **RP-F2** | **Handle corporate actions: splits, dividends, mergers, spin-offs, symbol changes.** A 2:1 stock split that isn't adjusted makes the stock look like it dropped 50% overnight — triggering every stop-loss and generating false signals. | [CORPORATE_ACTION_BOMB] Unadjusted corporate actions are the #1 source of backtest-contamination. A single unadjusted split can make a losing strategy look profitable or vice versa. | Corporate action calendar, adjustment factor database, exchange bulletins |
| **RP-F3** | **Assess survivorship bias.** Are backtest symbols still listed today? Stocks that went bankrupt, were delisted, or acquired are absent from current symbol lists — making historical returns look BETTER than reality. | [SURVIVORSHIP_BIAS] Using only currently-listed symbols adds 1-2% annually to backtest returns. A strategy that shows +12% on survivorship-biased data may be +10% (or worse) in reality. | Delisted securities database, historical index constituents, CRSP/Compustat |
| **RP-F4** | **Verify tick precision and timestamp granularity.** Options data at minute resolution hides 90%+ of actual trades. Sub-second timestamps matter for: fill probability estimation, slippage modeling, and signal latency measurement. | [RESOLUTION_BLINDNESS] A strategy that works on 1-minute bars may fail on tick data. The difference between the high of the minute and the actual trade price = hidden slippage. | Tick data archives, exchange timestamp specifications, fill reports |
| **RP-F5** | **Calculate data pipeline latency and reliability.** Measure: ingestion-to-availability latency (target: <100ms for real-time), uptime (target: 99.9%+), and data loss rate (target: <0.01%). Pipeline failure during market hours = blind trading. | [PIPELINE_BLINDNESS] A trading system without data is a car without headlights at night. Every minute of pipeline downtime during market hours is a minute of unmonitored risk. | Pipeline monitoring dashboard, latency histograms, incident reports |
""",

    'financial-security': """
### Financial Security Domain Extension — Execute These ADDITIONAL Research Steps

| # | Research Step | Why It Matters | Where to Look |
|---|--------------|----------------|----------------|
| **RP-F1** | **Map the fraud taxonomy for the transaction type.** Wire fraud, ACH fraud, check fraud, card-not-present, account takeover, synthetic identity — each has distinct patterns and detection signatures. | [PATTERN_BLINDNESS] Generic fraud detection catches ~40% of fraud. Pattern-specific detection catches ~85%. The 45% gap is the cost of treating all fraud as the same problem. | Fraud taxonomy database, industry fraud reports, regulatory alerts |
| **RP-F2** | **Check AML/KYC requirements for the jurisdiction and transaction size.** CTR threshold ($10,000), SAR triggers, PEP screening, sanctions list checks. Missing a SAR filing = personal criminal liability. | [COMPLIANCE_GAP] AML failures are not "compliance issues" — they are federal crimes. The cost of a missed SAR is measured in prison time, not dollars. | FinCEN regulations, OFAC SDN list, jurisdictional AML requirements |
| **RP-F3** | **Analyze transaction velocity and pattern anomalies.** Normal: 3 transactions/day, $200 avg. Suspicious: 15 transactions/day, $50 avg (structuring). Velocity × amount × deviation from baseline = anomaly score. | [VELOCITY_BLINDNESS] Single-transaction monitoring misses structuring. The aggregate pattern across time reveals what individual transactions hide. | Transaction monitoring system, velocity baselines, peer group comparisons |
| **RP-F4** | **Verify device fingerprinting and behavioral biometrics.** Is the device known? Is the typing pattern consistent with the account holder? Does the geolocation match the billing address? | [DEVICE_SPOOF] Stolen credentials + VPN + device emulator = perfect mimicry of the legitimate user. Device fingerprinting catches what credentials alone miss. | Device fingerprint database, behavioral biometric baselines, geolocation logs |
| **RP-F5** | **Stress-test fraud detection against adversarial adaptation.** Fraudsters adapt to detection rules in 2-4 weeks. A rule that caught 90% of fraud last month catches 70% this month and 40% next month. | [ADVERSARIAL_DECAY] Static rules decay. The half-life of a fraud detection rule is ~6 weeks. Without continuous adaptation, detection degrades from prevention to post-mortem. | Rule performance over time, adversarial pattern evolution, ML model drift metrics |
""",

    'fundamental-analyst': """
### Fundamental Analysis Domain Extension — Execute These ADDITIONAL Research Steps

| # | Research Step | Why It Matters | Where to Look |
|---|--------------|----------------|----------------|
| **RP-F1** | **Verify financial statement quality.** Check: revenue recognition policy (aggressive vs. conservative), one-time items as % of earnings (>10% = red flag), accounts receivable growth vs. revenue growth (AR growing faster = channel stuffing risk). | [ACCOUNTING_FICTION] GAAP earnings can be legally manipulated through revenue recognition, capitalization of expenses, and reserve manipulation. Reported earnings and economic earnings can diverge by 20%+. | 10-K, 10-Q, earnings call transcripts, auditor opinion letters |
| **RP-F2** | **Compute normalized (cycle-adjusted) earnings.** Use 5-10 year average margins to smooth cyclicality. A cyclical at peak earnings trading at 8× P/E is expensive, not cheap — normalized P/E may be 18×. | [CYCLICAL_TRAP] Buying cyclicals at peak earnings on low P/E is the classic value trap. Normalized earnings reveal the true valuation. | Historical margin data, sector cycle analysis, normalized P/E calculations |
| **RP-F3** | **Assess competitive moat durability.** Porter's Five Forces on the specific business: barriers to entry, supplier power, buyer power, substitution threat, competitive intensity. A wide moat deteriorating is more dangerous than no moat at all — it means the market is overpaying for a fading advantage. | [MOAT_MIRAGE] "Wide moat" is not a permanent certification. Moats erode: technological disruption, regulatory change, new entrants, changing consumer behavior. A moat assessment from 2020 may be obsolete in 2025. | Industry reports, competitor analysis, technology disruption timelines |
| **RP-F4** | **Reverse-engineer the DCF assumptions.** What growth rate and terminal value are priced in at current market price? If the implied growth rate exceeds GDP growth + inflation by 3%+, the market is pricing in dominance that may not materialize. | [DCF_ASSUMPTION_BLINDNESS] A DCF is only as good as its assumptions. The market price IS a DCF — reverse it to see what assumptions are embedded. If those assumptions are unreasonable, the price is unreasonable. | Reverse DCF model, GDP growth forecasts, inflation expectations |
| **RP-F5** | **Cross-check against the three most dangerous words in investing: "this time is different."** For every bullish thesis, find the historical analog where the same thesis was applied and failed. If no analog exists, the thesis is either genuinely novel (rare) or the historical search was insufficient (common). | [HISTORICAL_AMNESIA] Every bubble has been accompanied by a "this time is different" narrative. The four most expensive words in finance. Historical analogs are the cheapest reality check available. | Financial history databases, bubble case studies, "This Time Is Different" (Reinhart & Rogoff) |
""",

    'personal-finance': """
### Personal Finance Domain Extension — Execute These ADDITIONAL Research Steps

| # | Research Step | Why It Matters | Where to Look |
|---|--------------|----------------|----------------|
| **RP-F1** | **Verify current tax brackets, contribution limits, and deduction thresholds.** 401(k) limits, IRA limits, HSA limits, standard deduction, tax brackets — all indexed to inflation and change annually. | [TAX_STALENESS] Recommending last year's contribution limits costs real dollars. A $500 over-contribution triggers 6% excise tax annually until corrected. | IRS publications, tax code updates, contribution limit trackers |
| **RP-F2** | **Check current interest rate environment.** Mortgage rates, savings account APYs, CD rates, bond yields, Fed funds rate expectations. A "refinance now" recommendation at 6.5% mortgage rates may be terrible advice if rates are trending to 5.5%. | [RATE_CONTEXT] Personal finance advice is rate-dependent. "Pay off mortgage early" at 3% is mathematically suboptimal vs. investing. At 7%, it becomes a guaranteed 7% return. Same advice, different rates, opposite conclusions. | Fed funds futures, yield curve, mortgage rate indices, savings rate aggregators |
| **RP-F3** | **Calculate the specific dollar impact.** "Save more for retirement" is vague. "Increasing 401(k) contribution from 6% to 8% on a $85,000 salary adds $1,700/year, grows to $89,247 over 25 years at 7% — $25,500 in additional contributions generating $63,747 in gains" is actionable. | [DOLLAR_VAGUENESS] Personal finance without dollar math is fortune-cookie advice. Abstract guidance doesn't change behavior — concrete numbers do. | Compound interest calculators, salary data, retirement projections |
| **RP-F4** | **Identify behavioral failure modes.** The #1 reason financial plans fail is not market performance — it's behavioral deviation. Panic selling in drawdowns. Lifestyle inflation as income rises. Analysis paralysis leading to inaction. | [BEHAVIORAL_RISK] A perfectly optimized financial plan that the person won't follow is worth $0. The best plan is the one that gets executed. Address the behavioral failure mode before optimizing the financial model. | Behavioral finance literature, common financial mistakes databases |
| **RP-F5** | **Check for life-event alignment.** Is there a wedding, child, home purchase, career change, or medical event in the near term? Major life events override standard financial rules. A 6-month emergency fund recommendation becomes 12 months during a career transition. | [LIFE_EVENT_BLINDNESS] Financial planning that ignores life events is spreadsheet fiction. The mathematically optimal asset allocation is irrelevant if the person needs cash for a down payment in 18 months. | Life event checklist, time horizon analysis, liquidity requirement assessment |
""",

    'home-buying': """
### Home Buying Domain Extension — Execute These ADDITIONAL Research Steps

| # | Research Step | Why It Matters | Where to Look |
|---|--------------|----------------|----------------|
| **RP-F1** | **Check current mortgage rates, loan limits, and PMI thresholds.** Conforming loan limits, FHA limits, VA eligibility, PMI rates by LTV band. A 0.5% rate difference on a $400K loan = $42,000 over 30 years. | [RATE_LEVERAGE] Mortgage rates are the single largest cost driver in home buying. Every 1% rate increase reduces buying power by ~11%. Rate shopping across 3+ lenders saves $3,000-$5,000 in closing costs. | Mortgage rate aggregators, FHFA conforming limits, PMI rate schedules |
| **RP-F2** | **Analyze the local market: inventory, days on market, sale-to-list ratio, price trends.** A "buyer's market" with 6+ months inventory vs. a "seller's market" with 1-2 months require completely different negotiation strategies. | [MARKET_TYPE_MISMATCH] Offering 5% under list in a seller's market = you'll never get a house. Offering list price in a buyer's market = you're overpaying. Market type determines strategy. | MLS data, Redfin/Zillow market reports, local agent insights |
| **RP-F3** | **Calculate the true cost of ownership, not just PITI.** Property taxes (1-3% of value/year), insurance (0.5-1%), maintenance (1-2% of value/year), HOA fees, utilities, and opportunity cost of down payment. PITI is ~70% of true cost. | [HIDDEN_COST] A $2,500/month PITI becomes $3,800/month actual cost after taxes, insurance, maintenance, and HOA. The gap between PITI and true cost is where new homeowners get financially trapped. | Property tax records, insurance quotes, maintenance cost estimators |
| **RP-F4** | **Verify the rent-vs-buy breakeven.** Compute: (annual rent × rent inflation) vs. (annual ownership cost − equity buildup + transaction costs). In high-cost markets, renting and investing the difference often beats buying. | [OWNERSHIP_BIAS] The cultural pressure to buy ignores math. In markets where price-to-rent ratio > 20, renting + investing the down payment often outperforms buying over 10+ year horizons. | Rent-vs-buy calculators, price-to-rent ratio data, investment return assumptions |
| **RP-F5** | **Check for first-time homebuyer programs, grants, and tax incentives.** Down payment assistance (up to 5% of purchase price), mortgage credit certificates (20% of interest as tax credit), state-specific programs. Many programs go unused because buyers don't know they exist. | [PROGRAM_BLINDNESS] Thousands of dollars in grants and tax credits go unclaimed because the maze of programs is hard to navigate. A 30-minute search can find $5,000-$15,000 in assistance. | State housing finance agency websites, HUD programs, mortgage credit certificate programs |
""",
}

def already_has_extension(content):
    """Check if skill already has a domain-specific extension."""
    return bool(re.search(r'Domain Extension.*Execute These ADDITIONAL', content))

def add_extension(filepath, skill_name, dry_run=False):
    with open(filepath, 'r') as f:
        content = f.read()
    
    if already_has_extension(content):
        return 'skipped', 'already has domain extension'
    
    if skill_name not in FINANCE_EXTENSIONS:
        return 'skipped', 'no domain extension defined'
    
    extension = FINANCE_EXTENSIONS[skill_name]
    
    # Insert after the universal RP section's closing compliance line
    # Find the "Compliance:" line which is the end of universal RP
    compliance_marker = '> **Compliance:**'
    if compliance_marker not in content:
        return 'error', f'cannot find universal RP compliance marker in {skill_name}'
    
    # Find the line after the compliance block (next ## or blank line followed by ##)
    insert_marker = compliance_marker
    idx = content.index(insert_marker) + len(insert_marker)
    
    # Find the end of the compliance line
    end_of_line = content.index('\n', idx)
    
    if dry_run:
        return 'dry-run', f'would insert extension after line ~{content[:end_of_line].count(chr(10)) + 1}'
    
    new_content = content[:end_of_line + 1] + '\n' + extension + content[end_of_line + 1:]
    
    with open(filepath, 'w') as f:
        f.write(new_content)
    return 'added', 'domain extension inserted'


def main():
    dry_run = '--dry-run' in sys.argv
    
    skills_dir = os.path.join(REPO_ROOT, 'skills')
    stats = {'added': 0, 'skipped': 0, 'error': 0, 'dry-run': 0}
    
    target = None
    for i, arg in enumerate(sys.argv):
        if arg == '--skill' and i + 1 < len(sys.argv):
            target = sys.argv[i + 1]
    
    for skill_name in FINANCE_EXTENSIONS:
        if target and skill_name != target:
            continue
        
        # Find the skill file
        found = False
        for root, dirs, files in os.walk(skills_dir):
            if os.path.basename(root) == skill_name and 'SKILL.md' in files:
                filepath = os.path.join(root, 'SKILL.md')
                status, msg = add_extension(filepath, skill_name, dry_run=dry_run)
                stats[status] += 1
                print(f"  [{status.upper()}] {skill_name}: {msg}")
                found = True
                break
        
        if not found:
            print(f"  [MISSING] {skill_name}: SKILL.md not found")
            stats['error'] += 1
    
    print(f"\nSummary: {stats['added']} added, {stats['skipped']} skipped, {stats['error']} errors")
    if dry_run:
        print("DRY RUN — no files were modified.")

if __name__ == '__main__':
    main()
