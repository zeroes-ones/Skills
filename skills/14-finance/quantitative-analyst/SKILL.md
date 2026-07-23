---
name: quantitative-analyst
description: Quantitative finance for options markets — pricing models (Black-Scholes, Binomial, Monte Carlo), Greeks computation (Delta, Gamma, Theta, Vega, Rho), implied volatility surface construction, unusual options activity (UOA) detection, volatility smile/skew analysis, put-call parity validation, and trade signal generation from options flow anomalies. Triggered by options pricing, Greeks, UOA, unusual options activity, implied volatility, IV surface, volatility skew, Black-Scholes, binomial tree, Monte Carlo simulation, options flow, options signal, put-call parity, volatility smile, trade signal, options strategy.
author: Sandeep Kumar Penchala
type: finance
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - quantitative-analyst
  - options
  - uoa
  - greeks
  - volatility
token_budget: 4000
output:
  type: "code"
  path_hint: "./"
chain:
  consumes_from:
    - market-data-engineer
    - data-scientist
    - ml-ai-engineer
  feeds_into:
    - algorithmic-trader
    - data-scientist
    - ml-ai-engineer
  alternatives:
    - ml-ai-engineer
---
# Quantitative Analyst

Options market intelligence through quantitative rigor. Build pricing models, compute and interpret Greeks,
detect unusual options activity (UOA), construct implied volatility surfaces, validate put-call parity, analyze
volatility smile/skew, and generate actionable trade signals from options flow anomalies. This skill translates
raw options market data into structured, confidence-calibrated trade signals ready for algorithmic consumption.

## Route the Request
<!-- QUICK: 30s -- auto-route first, then intent-route -->

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*.py", "BlackScholes\|black_scholes\|bsm_price\|implied_volatility")` OR `file_contains("*.py", "scipy.stats.norm\|monte_carlo.*option\|heston\|binomial")` OR `file_contains("*.R", "BlackScholes\|Garch\|rugarch")` | This is your skill. Jump to **Core Workflow** — Phase 1. |
| A2 | `file_contains("*.py", "kafka\|KafkaProducer\|polygon\|alpaca.*trade\|websocket")` OR `file_contains("*.sql", "CREATE TABLE.*ticks\|CREATE TABLE.*options_flow")` | Invoke **market-data-engineer** instead. This is data pipeline work. |
| A3 | `file_contains("*.py", "backtrader\|zipline\|vectorbt\|alpaca.*trade\|order.*submit")` OR `file_contains("*.py", "Strategy.*next\|stop_loss\|take_profit\|bracket")` | Invoke **algorithmic-trader** instead. This is execution and order placement. |
| A4 | `file_contains("*.py", "sklearn\|tensorflow\|torch\|xgboost\|RandomForest\|GradientBoosting")` AND `file_contains("*.py", "predict\|classify\|signal")` | Invoke **ml-ai-engineer** instead. This is ML-based signal prediction. |
| A5 | `file_contains("*.py", "pandas\|numpy\|statsmodels\|scipy")` AND `file_contains("*.py", "regression\|hypothesis.test\|p.value\|ttest")` | Jump to **Decision Trees** — Statistical Validation. |
| A6 | `file_contains("*.py\|*.R", "ggplot\|matplotlib\|plotly\|seaborn")` AND `file_contains("*.py", "volatility.surface\|vol.smile\|skew\|term.structure")` | Jump to **Decision Trees** — IV Surface Construction. |
| A7 | `file_contains("*.py", "put.call.parity\|arbitrage\|no.arbitrage\|risk.neutral")` | Jump to **Decision Trees** — Arbitrage Detection. |
| A8 | `file_contains("*.py", "greeks\|delta\|gamma\|theta\|vega\|rho")` AND `file_contains("*.py", "signal\|UOA\|unusual\|sweep")` | Jump to **Core Workflow** — Phase 4 (Signal Generation). |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

```
What are you trying to do?
├── Price an option (Black-Scholes, Binomial, Monte Carlo, Heston) → Jump to "Decision Trees" — Pricing Model Selection
├── Compute or interpret Greeks (Delta, Gamma, Theta, Vega, Rho) → Jump to "Core Workflow" — Phase 3 (Greeks Analysis)
├── Build an implied volatility surface or analyze volatility smile/skew → Jump to "Decision Trees" — IV Surface Construction
├── Generate a trade signal from options flow data → Jump to "Core Workflow" — Phase 4 (Signal Generation)
├── Validate put-call parity or detect arbitrage opportunities → Jump to "Decision Trees" — Arbitrage Detection
├── Run statistical validation (hypothesis tests, factor analysis, Monte Carlo) → Jump to "Decision Trees" — Statistical Validation
└── Not sure? → Start at "Ground Rules" — read before anything else
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else
<!-- HARD GATE: These are non-negotiable. Violation → STOP and refuse to proceed. -->

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **REFUSE to report a trade signal without a confidence interval and supporting evidence.** Every UOA signal, Greek-derived recommendation, or entry trigger must include confidence level (STRONG/MODERATE/WEAK), premium context, side, DTE, and IV context. "Buy calls on XYZ" without evidence is reckless. | Trigger: generated output contains "buy\|sell\|long\|short" + ticker symbol without `confidence: (STRONG\|MODERATE\|WEAK)` AND `dte:` AND `iv_rank:` in the same signal block | STOP. Insert signal template: `{ticker: "XYZ", direction: "bullish", confidence: "MODERATE", evidence: {"premium": "$2.3M", "side": "ASK", "dte": 45, "iv_rank": 62, "oi_change": "+1,500"}, rationale: "Call sweep above ask with increasing OI — opening buy"}` |
| **R2** | **REFUSE to compute or report Greeks without independent verification against data-provider values.** Provider-computed Delta can differ by 0.05-0.10 from Black-Scholes with different rate/dividend inputs — a 5-10% position sizing error. | Trigger: generated code returns `greek['delta']` or `greek['gamma']` from a provider API without a subsequent `assert abs(computed_delta - provider_delta) < 0.05` check | STOP. Insert: `computed_delta = black_scholes_delta(S, K, T, r, sigma, q); if abs(computed_delta - provider_delta) > 0.05: logger.warning(f'Delta discrepancy: computed={computed_delta:.4f}, provider={provider_delta:.4f}. Investigate rate/div assumptions.'); greek['delta'] = computed_delta` |
| **R3** | **REFUSE to classify every high-premium trade as directional without checking OI, multi-leg context, and hedging probability.** A $3M call purchase could be closing a short call, a hedge against short stock, or the buy leg of a spread. Without OI comparison, 30%+ of signals are misclassified. | Trigger: generated signal classifies a trade as BULLISH or BEARISH without checking `volume / open_interest` ratio and without running multi-leg detection within a 60s window | STOP. Insert: `oi_ratio = trade.volume / trade.open_interest; if oi_ratio < 0.5: signal.classification = 'POTENTIAL_CLOSING'; signal.confidence = downgrade(signal.confidence); logger.info(f'Trade {trade.id}: OI ratio {oi_ratio:.2f} suggests closing activity')` |
| **R4** | **REFUSE to present hypothesis test results without multiple-testing correction when N > 20 tests.** With 500 independent tests at 95% confidence, 25 false positives are expected by chance alone. Without Bonferroni or Benjamini-Hochberg, you are trading noise. | Trigger: generated output reports p < 0.05 as "significant" or "edge discovered" AND `grep -c "p.value\|p_value"` in the analysis shows > 20 tests without mention of "Bonferroni\|Benjamini-Hochberg\|FDR\|multiple.testing" | STOP. Apply: `from statsmodels.stats.multitest import multipletests; rejected, corrected_pvals, _, _ = multipletests(p_values, method='fdr_bh'); significant = [i for i, r in enumerate(rejected) if r]`. Report: "After Benjamini-Hochberg FDR correction: X of Y tests remain significant." |
| **R5** | **STOP and ASK when signal context is missing.** Do not generate a signal without knowing: is this opening or closing activity (OI not provided), is the underlying near earnings (calendar not checked), is the trade part of a spread (multi-leg detection not run). | Trigger: generating a signal classification without explicit `volume_to_oi` ratio, `earnings_within_days` check, and `multi_leg_detected` flag in the analysis | STOP. Ask: "Has OI been compared to volume? Are there earnings within the position's DTE window? Has multi-leg detection been run within a 60-second window? I need these before classifying direction." |
| **R6** | **DETECT and WARN about survivorship-biased datasets.** Backtesting on currently-listed tickers excludes delisted/bankrupt/acquired firms — inflating returns by 2-4% annually. | Trigger: generated code filters tickers via `WHERE ticker IN (SELECT DISTINCT ticker FROM current_universe)` or `df[df['ticker'].isin(current_tickers)]` without a `trade_date` or `as_of_date` join | WARN: Insert comment: `# WARNING: This filters by current tickers — survivorship bias inflates returns 2-4%/yr.` Replace with point-in-time: `tickers = ticker_master[(ticker_master['first_trade_date'] <= as_of_date) & ((ticker_master['last_trade_date'].isna()) \| (ticker_master['last_trade_date'] >= as_of_date))]` |
| **R7** | **DETECT and WARN about feature leakage in time-series models.** Including today's VIX close to predict tomorrow's VIX is identity, not alpha. Any R² > 0.7 on financial time series is a bug until proven otherwise. | Trigger: generated model training code joins features on `df['date']` or `pd.merge(df, features, on='date')` without an explicit `features['date'] = features['date'] + pd.Timedelta(days=1)` lag shift OR reports R² > 0.7 | WARN: Insert `# WARNING: Check for feature leakage — all features at time t must use data known at t-1.` Add: `features = features.shift(1)  # Lag features by 1 period`. Add: `assert model.r2_score < 0.7, f'R² {model.r2_score:.3f} suspiciously high — check for future leakage'` |


## The Expert's Mindset

Masters of quantitative analyst don't just build — they build **the right thing, at the right time, with the right trade-offs**. They think in systems, not tasks.

| Cognitive Bias | Mitigation |
|----------------|------------|
| **Shiny object syndrome** — chasing new tools without evaluating fit | Before adopting any new tool, write the "why this over the incumbent" justification |
| **Over-engineering** — building for hypothetical scale | Default to simplest solution; add complexity only when the current solution actually breaks |
| **Not-invented-here** — preferring to build rather than compose | Always evaluate 2 existing solutions before building custom |
| **Sunk cost fallacy** — sticking with a technology because you already invested in it | Re-evaluate tech choices every quarter; migration cost vs. staying cost |

### What Masters Know That Others Don't
- The **failure modes** of every component in their stack — not just the happy path
- When **not** to use their favorite tool (every tool has a misuse zone)
- That **data/model quality decays over time** — monitoring is not optional, it's foundational

### When to Break Your Own Rules
- **Move fast on reversible decisions.** Data format? Hard to change. Dashboard layout? Easy. Know the difference.
- **Skip the abstraction until the third use case.** Two is coincidence, three is a pattern.
## Operating at Different Levels

| Level | Scope | You... |
|-------|-------|--------|
| **L1** | Single component/module | Implement a well-defined piece following established patterns |
| **L2** | Feature or service | Design and build a complete feature; make tech choices within team conventions |
| **L3** | System or product area | Define architecture for a product area; set team tech standards; mentor L1-L2 |
| **L4** | Multiple systems / platform | Define org-wide architecture patterns; make build-vs-buy decisions; influence industry practice |
| **L5** | Industry / ecosystem | Create new architectural patterns adopted across the industry; redefine what's possible |

**Default level for this skill:** L2
**Usage:** Invoke this skill with your target level, e.g., "as an L3 quantitative analyst, design..."

For full level definitions, see `skills/00-framework/skill-levels/SKILL.md`.

## When to Use
<!-- QUICK: 30s — scan the bullet list to decide if this skill fits -->
- You are screening for unusual options activity on mid-cap companies with $1M+ premium thresholds
- You need to compute and interpret Greeks (Delta, Gamma, Theta, Vega, Rho) for individual options or portfolios
- You are pricing options using Black-Scholes, Binomial trees, or Monte Carlo simulation
- You need to filter UOA by condition codes (sweep, split, block, floor) and classify trade intent
- You are constructing an implied volatility surface and analyzing smile/skew/term structure
- You need to generate structured trade signals (STRONG BUY, BUY, WEAK BUY, NEUTRAL, SELL) from options flow
- You are validating put-call parity or detecting arbitrage opportunities in options chains
- You need to assess IV rank/percentile to determine whether options are cheap or expensive
- You are filtering out noise — bad prints, dividend-affected chains, 0DTE gambler flow, pre-earnings hedging
- You need to distinguish multi-leg strategies (spreads, straddles, strangles, butterflies) from single-leg trades

## Decision Trees
<!-- QUICK: 30s — follow the ASCII tree to your scenario -->

### UOA Signal Classification: Trade Type Identification
```
                        ┌──────────────────────────────────┐
                        │ START: Incoming options trade     │
                        │ (strike, premium, volume, side)   │
                        └──────────────┬───────────────────┘
                                       │
                         ┌─────────────▼────────────────────┐
                         │ Premium ≥ $1M OR volume > 10x    │
                         │ average daily volume at strike?  │
                         └──┬──────────────────────┬────────┘
                            │ NO                   │ YES
                      ┌─────▼──────┐     ┌─────────▼──────────────┐
                      │ IGNORE     │     │ Check condition code:   │
                      │ (sub-threshold)│  │ ISO / Exchange code?   │
                      └────────────┘     └──┬──────────┬──────────┘
                                           │           │
                              ┌────────────▼──┐  ┌─────▼──────────────┐
                              │ ISO (Intermarket│  │ Exchange-specific  │
                              │ Sweep Order)    │  │ (CBOE, PHLX, etc.) │
                              └───────┬─────────┘  └──────┬─────────────┘
                                      │                   │
                              ┌───────▼──────────┐  ┌─────▼──────────────┐
                              │ SWEEP detected:  │  │ Check trade size   │
                              │ single large order│  │ vs conditions:     │
                              │ split across      │  │                    │
                              │ exchanges to fill │  │ ├─ Single large    │
                              │ → BULLISH/BEARISH │  │ │  print → BLOCK   │
                              │   (aggressive)    │  │ ├─ Floor-executed  │
                              └───────────────────┘  │ │  → FLOOR TRADE   │
                                                     │ └─ Multi-exchange  │
                                                     │    fills same sec  │
                                                     │    → SWEEP (soft)  │
                                                     └────────────────────┘
```

**Sweep**: Aggressive institutional order routed across exchanges to fill immediately. High conviction signal — someone wants in NOW.
**Block**: Single large print (>500 contracts typically) negotiated off-screen or printed late. May be pre-arranged, signal reliability medium.
**Split**: Single order executed in multiple smaller trades on same exchange (vs Sweep = across exchanges). Lower urgency.
**Floor Trade**: Executed on exchange floor (less common today). Usually hedges or institutional repositioning. Low signal for retail.

### Options Strategy Selection from UOA Signal
```
                        ┌────────────────────────────────────┐
                        │ START: Validated UOA signal         │
                        │ (premium, side, strike, DTE, IV)    │
                        └──────────────┬─────────────────────┘
                                       │
                          ┌────────────▼──────────────────┐
                          │ What is the trade SIDE?        │
                          └──┬──────────────────┬─────────┘
                             │ ASK (bought)     │ BID (sold)
                    ┌────────▼────────┐  ┌──────▼─────────────────┐
                    │ Option type?     │  │ Option type?           │
                    └──┬──────────┬────┘  └──┬──────────┬──────────┘
                       │CALLS     │PUTS      │CALLS     │PUTS
                 ┌─────▼──────┐ ┌─▼────────┐┌─▼─────────┐┌─▼──────────┐
                 │ ATM/OTM?    │ │ ATM/OTM? ││ ATM/OTM?  ││ ATM/OTM?   │
                 └──┬──────┬───┘ └┬──────┬──┘└┬──────┬───┘└┬──────┬────┘
                    │ATM   │OTM   │ATM   │OTM  │ATM   │OTM  │ATM   │OTM
              ┌─────▼──┐ ┌─▼────┐┌─▼──┐ ┌─▼────┐┌─▼──┐ ┌─▼──┐ ┌─▼──┐ ┌─▼──┐
              │DTE?    │ │DTE?  ││DTE?│ │DTE?  ││ANY │ │ANY │ │ANY │ │ANY │
              └──┬──┬──┘ └┬──┬──┘└┬─┬─┘ └┬──┬──┘│DTE │ │DTE │ │DTE │ │DTE │
                 │  │     │  │    │ │    │  │   └────┘ └────┘ └────┘ └────┘
           ┌─────▼┐┌▼───┐│┌─▼──┐│┌─▼──┐│┌─▼──┐
           │30-90││7-30│││30-90│││7-30│││30-90││7-30││
           │ DTE ││DTE │││DTE │││DTE │││DTE │││DTE ││
           └──┬──┘└─┬──┘└──┬──┘└──┬──┘└──┬──┘└──┬──┘
              │     │     │     │     │     │     │
      ┌───────▼──┐ ┌▼────▼─┐ ┌▼───▼─┐ ┌▼───▼─┐ ┌▼───────▼──┐ ┌▼───────▼──┐
      │Long Call │ │Bullish│ │OTM    │ │0DTE   │ │Covered    │ │Cash-Secured│
      │(directional│ │Debit  │ │Call   │ │Lottery│ │Call Write │ │Put Write   │
      │bet)       │ │Spread │ │Sweep  │ │Call   │ │(bearish/  │ │(bullish/   │
      │STRONG BUY │ │BUY    │ │STRONG │ │IGNORE │ │neutral)   │ │neutral)    │
      │           │ │       │ │BUY    │ │(gamblers)│ │SELL signal│ │BUY signal  │
      └───────────┘ └───────┘ └───────┘ └───────┘ └───────────┘ └────────────┘
```
**Key DTE thresholds**: <7 DTE = lottery/gambler flow (ignore unless extraordinary premium); 7-14 DTE = tactical but high Theta risk; 14-30 DTE = short-term conviction; 30-90 DTE = institutional sweet spot; >90 DTE = strategic positioning.

### Pricing Model Selection
```
                        ┌──────────────────────────────┐
                        │ START: Which pricing model?    │
                        └────────────┬─────────────────┘
                                     │
                       ┌─────────────▼──────────────────┐
                       │ Option type?                    │
                       └──┬───────────────┬──────────────┘
                          │European       │American
                 ┌────────▼───────┐  ┌────▼────────────────────┐
                 │ Underlying pays │  │ Early exercise possible? │
                 │ dividends?      │  └──┬──────────────────┬────┘
                 └──┬──────────┬───┘     │YES (dividends)   │NO
                    │YES       │NO   ┌───▼──────────┐  ┌───▼──────────────┐
            ┌───────▼──┐  ┌───▼────┐│Binomial Tree │  │Black-Scholes +   │
            │Black-Scholes│ │Black- ││(CRR model)   │  │discrete dividend │
            │w/ dividend │ │Scholes││50-200 steps  │  │adjustment (Merton)│
            │yield (q)   │ │(plain)││for accuracy  │  │                   │
            └────────────┘ └───────┘└──────────────┘  └───────────────────┘

                 ┌─────────────────────────────────────┐
                 │ Need path-dependent pricing?         │
                 │ (barrier, Asian, lookback, cliquet)? │
                 └──┬──────────────────────────┬───────┘
                    │YES                        │NO
            ┌───────▼──────────┐    ┌───────────▼──────────────┐
            │ Monte Carlo      │    │ Analytical (BS/Binomial)  │
            │ Simulation       │    │ or numerical PDE (Crank-  │
            │ 100K+ paths for  │    │ Nicolson finite difference│
            │ convergence      │    │ for American w/ dividends │
            └──────────────────┘    └──────────────────────────┘
```
**Black-Scholes formula (European, no dividends):**
C = S₀·N(d₁) − K·e^(−rT)·N(d₂)
P = K·e^(−rT)·N(−d₂) − S₀·N(−d₁)
where d₁ = [ln(S₀/K) + (r + σ²/2)T] / (σ√T), d₂ = d₁ − σ√T

### Volatility Skew & Sentiment Interpretation
```
                        ┌────────────────────────────────────┐
                        │ START: Analyze IV skew pattern      │
                        └──────────────┬─────────────────────┘
                                       │
                         ┌─────────────▼────────────────────┐
                         │ OTM Put IV vs OTM Call IV         │
                         │ (25-delta skew comparison)        │
                         └──┬──────────────────┬─────────────┘
                            │                  │
                  ┌─────────▼──────┐  ┌────────▼──────────────┐
                  │ Put IV > Call IV│  │ Call IV > Put IV      │
                  │ (normal skew)   │  │ (reverse skew)        │
                  └──┬──────────────┘  └──┬────────────────────┘
                     │                    │
           ┌─────────▼──────────┐  ┌─────▼────────────────────┐
           │ Skew widening?     │  │ Commodity/VIX-related     │
           │ (put IV rising     │  │ upside fear (short        │
           │  relative to calls) │  │ squeeze risk, supply      │
           └──┬──────────┬──────┘  │ disruption)               │
              │YES       │NO       └───────────────────────────┘
     ┌────────▼──┐  ┌───▼────────┐
     │ FEAR/CRISIS│  │ Normal     │
     │ signal:    │  │ market:    │
     │ elevated   │  │ puts cost  │
     │ hedging    │  │ more than  │
     │ demand     │  │ calls due  │
     │ → Bearish  │  │ to crash   │
     │   caution  │  │ insurance  │
     └────────────┘  │ premium    │
                     └────────────┘
```
**Skew metrics:** 25-delta risk reversal = IV(25Δ call) − IV(25Δ put). Negative = normal skew (puts richer). Widening negative skew = growing fear. Butterfly spread IV = [IV(25Δ call) + IV(25Δ put)]/2 − IV(ATM) measures smile convexity; elevated butterfly = tail-risk pricing.

## Core Workflow
<!-- STANDARD: 5min overview — skim the phases, read your target phase in detail -->

<!-- DEEP: 10+min -->
### Phase 1: Data Validation (5-10 min)
<!-- DEEP: Full validation protocol — read before processing any options data -->
**Goal**: Reject bad data before it contaminates signal generation.

**Steps:**
1. **Stale quote check**: Reject any quote where (now − quote_timestamp) > 60 seconds. Options markets move fast; stale quotes produce phantom signals.
2. **Bad print filter**: Reject trades with condition codes indicating: cancelled (C), corrected (CT), late (L), out-of-sequence (O). Accept only: regular (blank/@), ISO, sweep-eligible.
3. **Dividend-adjusted chain validation**: Cross-reference ex-dividend dates within option expiration. Calls on stocks going ex-div within DTE will have adjusted strikes. Flag and exclude from UOA unless dividend adjustment is explicitly modeled.
4. **Earnings blackout**: Flag all trades within 2 calendar days of the underlying's next earnings date. Pre-earnings options activity is predominantly hedging, not directional bets.
5. **Bid-ask spread sanity**: Reject options where (ask − bid) / mid > 25% (illiquid strikes produce noise). For mid-caps, threshold may relax to 35%.
6. **Volume-to-OI sanity**: If volume > 5× open interest AND premium < $100K, possible data error — flag for manual review.

**Output**: Cleaned options trade log with `is_valid`, `rejection_reason` columns.

<!-- DEEP: 10+min -->
### Phase 2: UOA Detection (10-20 min)
<!-- DEEP: Full UOA pipeline — this is the core differentiator -->
**Goal**: Identify unusual options activity meeting premium, volume, and condition thresholds.

**Steps:**
1. **Premium threshold filter**: Single trade premium ≥ $1,000,000 OR cumulative premium in strike/expiry within 5-min window ≥ $1,000,000.
2. **OI comparison**: Compute `volume / open_interest` ratio at the trade's strike+expiry. Ratio > 1.0 = new position opening (high conviction). Ratio < 0.3 = likely closing (fade signal). Ratio 0.3-1.0 = indeterminate.
3. **Average volume comparison**: Compute 20-day rolling average volume at this strike. Flag if today's volume > 10× average.
4. **Condition code classification** (see Decision Tree 1 above): ISO → SWEEP; exchange single large print → BLOCK; floor execution → FLOOR; multi-exchange same-second fills → SWEEP.
5. **Side determination**: Compare trade price to contemporaneous bid/ask midpoint. Price ≥ ask → ASK-side (bought, aggressive). Price ≤ bid → BID-side (sold, aggressive). Bid < price < ask → mid (passive/negotiated, ambiguous).
6. **Multi-leg detection**: Within a 60-second window for the same underlying, detect: same strike, opposite type → straddle; adjacent strikes, same type → vertical spread; non-adjacent strikes, same type, same side → strangle; three strikes with ratio → butterfly/condor.
7. **Sector/ETF context**: Cross-reference the underlying with its sector ETF performance. Sector tailwind (+2% on week) amplifies bullish call signals; sector headwind dampens them.

**Python pseudocode for UOA detection:**
```python
def detect_uoa(trades: pd.DataFrame, quotes: pd.DataFrame,
               oi: pd.DataFrame, min_premium: float = 1_000_000,
               oi_ratio_threshold: float = 1.0,
               avg_vol_multiple: float = 10.0) -> pd.DataFrame:
    """
    Detect unusual options activity from cleaned trade data.
    Returns DataFrame with UOA flags and signal metadata.
    """
    signals = []

    for (ticker, strike, expiry), group in trades.groupby(['ticker','strike','expiry']):
        # Premium aggregation within 5-min rolling window
        group = group.sort_values('timestamp')
        group['premium_5min'] = (group['premium']
            .rolling('5min', on='timestamp').sum())

        # Filter: $1M+ premium
        uoa = group[group['premium_5min'] >= min_premium]

        for _, trade in uoa.iterrows():
            # OI comparison
            current_oi = oi.loc[
                (oi.ticker == ticker) &
                (oi.strike == strike) &
                (oi.expiry == expiry), 'open_interest'
            ].values
            oi_ratio = trade['volume'] / current_oi[0] if len(current_oi) > 0 and current_oi[0] > 0 else float('inf')

            # Side determination
            bid, ask = get_contemporaneous_quote(quotes, trade)
            mid = (bid + ask) / 2
            if trade['price'] >= ask * 0.995:        # near or at ask
                side = 'ASK'
                intent = 'BULLISH' if trade['option_type'] == 'CALL' else 'BEARISH'
            elif trade['price'] <= bid * 1.005:       # near or at bid
                side = 'BID'
                intent = 'BEARISH' if trade['option_type'] == 'CALL' else 'BULLISH'
            else:
                side = 'MID'
                intent = 'NEUTRAL'

            # OI-based position assessment
            if oi_ratio > 1.0:
                position_type = 'OPENING'  # new position
            elif oi_ratio < 0.3:
                position_type = 'CLOSING'  # likely closing
            else:
                position_type = 'INDETERMINATE'

            # Build signal record
            signals.append({
                'ticker': ticker,
                'timestamp': trade['timestamp'],
                'strike': strike,
                'expiry': expiry,
                'dte': (expiry - trade['timestamp'].date()).days,
                'option_type': trade['option_type'],
                'premium': trade['premium_5min'],
                'volume': trade['volume'],
                'oi_ratio': round(oi_ratio, 2),
                'side': side,
                'intent': intent,
                'position_type': position_type,
                'condition_code': trade['condition_code'],
                'trade_classification': classify_trade_type(trade)
            })

    return pd.DataFrame(signals)
```

**Output**: `uoa_signals` DataFrame with one row per detected unusual trade.

<!-- DEEP: 10+min -->
### Phase 3: Greeks Analysis (10-15 min)
<!-- DEEP: Full Greeks computation and interpretation -->
**Goal**: Compute and validate Greeks for UOA-flagged strikes; assess IV context.

**Steps:**
1. **IV computation**: For each flagged strike, invert Black-Scholes to solve for implied volatility using the trade price. Use Newton-Raphson with initial guess σ₀ = 0.30, tolerance 1e-6, max 100 iterations. If NR fails to converge, fall back to bisection method on [0.001, 5.0].
2. **Greeks computation** (standard Black-Scholes partial derivatives):
   - **Delta (Δ)**: Δ_call = N(d₁), Δ_put = N(d₁) − 1. Interpretation: probability of expiring ITM (roughly). ATM ≈ 0.50; deep ITM → ±1.0; deep OTM → 0.
   - **Gamma (Γ)**: Γ = N'(d₁) / (S₀·σ·√T). Interpretation: rate of Delta change per $1 move in underlying. Highest ATM near expiry — explosive gamma squeezes possible. Normalize as dollar gamma: Γ_$ = Γ × S₀² × 0.01 for position sizing.
   - **Theta (Θ)**: Θ_call = −[S₀·N'(d₁)·σ] / (2√T) − r·K·e^(−rT)·N(d₂). Interpretation: daily time decay. Accelerates dramatically in final 30 days. A 7-DTE ATM option loses ~2-3% per day to Theta.
   - **Vega (ν)**: ν = S₀·√T·N'(d₁) / 100. Interpretation: dollar change per 1% IV change. High Vega = vulnerable to IV crush (post-earnings). Vega peaks ATM at ~60 DTE.
   - **Rho (ρ)**: ρ_call = K·T·e^(−rT)·N(d₂) / 100. Interpretation: sensitivity to risk-free rate. Least important Greek for short-dated options; matters for LEAPS.
3. **IV Rank & Percentile**: Compute 52-week IV range for the underlying. IV Rank = (current IV − 52wk min IV) / (52wk max IV − 52wk min IV). IV Percentile = percentile rank of current IV in 52-week distribution. IV Rank > 70 = options expensive (sell premium, fade buy signals). IV Rank < 30 = options cheap (buy premium, amplify buy signals).
4. **IV Skew analysis**: Compute 25-delta risk reversal (25Δ call IV − 25Δ put IV). Widening negative skew = growing downside fear. Compare current skew to 20-day average.
5. **Term structure**: Compare 30-day ATM IV to 90-day ATM IV. Normal contango (back-month IV > front-month IV) = no event premium. Backwardation (front-month IV > back-month IV) = event-driven premium (earnings, binary event, FOMC). Forward ratio = IV(30d) / IV(90d) > 1.15 flags event risk.
6. **Greeks validation**: Cross-check computed Greeks against data provider values (if available). Flag discrepancies > 5% for Delta, > 10% for Gamma/Theta/Vega — indicates different pricing model assumptions (rates, dividends, or wrong underlying price).

**Output**: `greeks_analysis` DataFrame with IV, all five Greeks, IV rank/percentile, skew metrics, and term structure for every UOA-flagged strike.

<!-- DEEP: 10+min -->
### Phase 4: Signal Generation (5-10 min)
<!-- DEEP: Full signal classification logic -->
**Goal**: Classify each UOA detection into a trade signal with confidence level.

**Signal Classification Matrix:**

| Signal | Premium | Side | Option | DTE Range | Moneyness | IV Rank | Position | Sector | Confidence |
|--------|---------|------|--------|-----------|-----------|---------|----------|--------|------------|
| **STRONG BUY** | ≥$5M | ASK | CALL | 30-90 | ATM/OTM | >70 | OPENING | Tailwind | HIGH |
| **BUY** | $1M-$5M | ASK | CALL | 14-90 | ATM/OTM | >50 | OPENING | Neutral+ | MEDIUM |
| **WEAK BUY** | ≥$1M | ASK | CALL | 7-14 | ATM | Any | OPENING | Any | LOW |
| **NEUTRAL** | ≥$1M | MID | Any | Any | Any | Any | INDETERMINATE | Any | NONE |
| **SELL/PUT BUY** | ≥$1M | ASK | PUT | 14-90 | ATM/OTM | >50 | OPENING | Headwind | MEDIUM |
| **FADE** | ≥$1M | BID | CALL | Any | ATM | <30 | CLOSING | Any | LOW |
| **IGNORE** | Any | Any | Any | <7 | Deep OTM | Any | Any | Any | NONE |

**Entry strategy logic:**
1. **Confirmation stacking**: UOA signal + technical breakout (price > 20-day high) + sector tailwind = upgrade confidence one level.
2. **Fade rules**: Deep OTM (<0.20 delta) options with <7 DTE and premium > $1M = lottery flow, NOT smart money. Flag as IGNORE regardless of premium.
3. **Earnings filter**: Any signal with DTE < 5 trading days before earnings = downgrade one confidence level. Pre-earnings flow is hedging, not directional.
4. **OI confirmation gate**: OPENING positions = full signal strength. CLOSING positions = invert signal (closing calls = bearish). INDETERMINATE = downgrade one level.
5. **Size-to-float check**: Premium / market_cap > 0.1% on mid-caps ($2B-$10B) = extraordinary. For mega-caps (>$200B), threshold relaxes to premium > $10M.

**Entry trigger output format:**
```json
{
  "signal_id": "UOA-2026-07-21-XYZ",
  "ticker": "XYZ",
  "timestamp": "2026-07-21T14:32:00Z",
  "signal": "STRONG_BUY",
  "confidence": "HIGH",
  "entry_trigger": {
    "type": "BREAKOUT_CONFIRMATION",
    "condition": "price > 20-day high AND volume > 1.5x avg",
    "entry_price": "market_on_breakout",
    "stop_loss": "strike * 0.85 OR -15% from entry",
    "take_profit": "strike * 1.30 OR +25% from entry"
  },
  "greeks_snapshot": {
    "delta": 0.62, "gamma": 0.041, "theta": -0.085,
    "vega": 0.23, "iv_rank": 78, "dte": 45
  },
  "evidence": [
    "$5.2M ask-side OTM calls, 45 DTE, IV rank 78",
    "OI ratio 2.3 → new positions opening",
    "Sweep execution across 3 exchanges",
    "Sector ETF +2.8% this week (tailwind)",
    "No earnings within 10 days"
  ],
  "risks": [
    "Mid-cap liquidity: wide spreads on exit",
    "IV rank 78 → options expensive, IV crush possible on sector rotation",
    "Position size: $5.2M on $4B market cap = 0.13% (significant)"
  ]
}
```

**Output**: `trade_signals.json` — one structured signal per UOA detection, ready for algorithmic-trader consumption.

<!-- DEEP: 10+min -->
### Phase 5: Signal Delivery (2-5 min)
**Goal**: Package signals for downstream consumption by algorithmic-trader skill.

**Steps:**
1. **Deduplication**: Merge signals within same ticker/strike/expiry within 15-minute window. Keep highest-premium instance.
2. **Ranking**: Sort by `confidence` (HIGH > MEDIUM > LOW) then by `premium` descending.
3. **Delivery format**: Output as structured JSON (schema above) — the algorithmic-trader skill consumes this exact format.
4. **Summary statistics**: Report total signals, STRONG BUY count, BUY count, aggregate premium, top-5 tickers by premium, sector distribution.
5. **Risk warnings**: Attach global risk context — VIX level, macro event calendar (FOMC, CPI), sector rotation signals.

**Output**: `signal_batch_YYYY-MM-DD.json` ready for handoff.

## Best Practices
<!-- STANDARD: 3min — rules extracted from production options trading experience -->
- **Always validate before you analyze** — Stale quotes, bad prints, and dividend-adjusted chains produce phantom UOA signals. Run Phase 1 data validation on every batch. A bad-print call sweep on a dead strike looks identical to a real signal.
- **Premium alone isn't enough — OI comparison is essential** — A $2M call purchase that's actually closing an existing position is bearish, not bullish. Without OI comparison, you're trading the wrong side 30%+ of the time.
- **Side (ASK vs BID) determines intent, not just direction** — An ask-side fill means the trader crossed the spread to get in. A bid-side fill means they hit the bid to get out (or sell). Mid-market fills on negotiated trades are ambiguous — flag, don't classify.
- **Time decay is the silent killer — Theta must be part of every signal** — A bullish signal on 5-DTE options is fundamentally different from the same signal on 60-DTE options. At 5 DTE, Theta burns 3-5% of premium per day. The move needs to happen NOW or the trade loses to decay.
- **IV rank tells you if you're overpaying** — Buying options at IV rank > 80 means you're paying top-dollar for premium. The signal may be directionally correct but the entry price is terrible. Factor IV rank into position sizing (smaller when IV rank is high).
- **Earnings create noise, not signal** — 60-70% of unusual options activity in the 3 days before earnings is hedging or volatility arbitrage, not directional bets. Always check the earnings calendar. If a signal falls within 2 days of earnings, downgrade it.
- **Multi-leg detection separates smart money from gamblers** — A $3M call purchase could be: (a) naked directional bet, (b) leg of a bull call spread (buying ATM, selling OTM), (c) closing leg of a short call. Multi-leg detection via time-clustered strikes at same ticker is the only way to know.
- **Sector context amplifies or dampens signals** — A bullish call sweep on a stock whose sector ETF is down 3% on the week is fighting the tape. Sector tailwind (+2%+) upgrades signal confidence; sector headwind (−2%+) downgrades it.
- **Position sizing scales with conviction, not premium size** — A $10M block trade by an institution repositioning is less directional than a $1.5M sweep executed aggressively across exchanges. Signal classification (STRONG/BUY/WEAK) should drive position sizing, not raw premium.
- **Backtest your signal filters before trading them live** — Run your UOA detection pipeline on 6 months of historical data. Measure: (a) win rate by signal strength, (b) average return by DTE bucket, (c) false positive rate around earnings. If STRONG BUY signals don't outperform BUY signals historically, your classification is broken.

## Anti-Patterns
<!-- DEEP: 5min -- each anti-pattern includes machine-detectable patterns -->

| ❌ Anti-Pattern | ✅ Do This Instead | 🔍 Detect (grep / lint) | 🛡️ Auto-Prevent |
|-----------------|---------------------|--------------------------|-------------------|
| Classifying every $1M+ premium trade as directional without OI comparison or multi-leg detection | Compare trade volume to open interest. Flag trades where volume/OI < 0.5 as potential closing activity. Run multi-leg detection within 60-second windows to identify spreads, straddles, and combos before classifying direction. | `grep -rn "classified\|BUY\|SELL\|bullish\|bearish" src/signals/ --include="*.py" -B 10 \| grep -v "volume.*oi\|open_interest\|multi.leg\|spread"` → finds signal classification without OI context | `pytest tests/test_oi_gating.py` — inject trade where vol/OI < 0.5, assert classification is POTENTIAL_CLOSING not BULLISH/BEARISH |
| Using IV rank without flagging earnings-contaminated 52-week max/min | Compute IV rank from non-earnings periods only. Flag when 52-week IV max or min coincide with earnings dates (±1 day). Report both raw IV rank and earnings-excluded IV rank — use the latter for position sizing. | `grep -rn "iv_rank\|iv_percentile" src/ --include="*.py" \| grep -v "earnings\|ex.div\|adjusted\|clean"` → finds IV rank without earnings adjustment | `pytest tests/test_iv_rank_earnings.py` — feed IV history with earnings spike, assert raw rank differs from clean rank and warning is emitted |
| Running 500 hypothesis tests and reporting every p < 0.05 as a discovered edge | Apply Bonferroni correction (α/n) or Benjamini-Hochberg FDR. Pre-register hypotheses before testing. Split data: 70% exploration for hypothesis generation, 30% confirmation for validation. Only confirmed signals graduate to production. | `grep -rn "p.value\|p_value.*<\s*0\.05" src/analysis/ --include="*.py" \| grep -v "bonferroni\|fdr\|corrected\|multipletests"` → finds uncorrected significance claims | `pytest tests/test_multiple_testing.py` — run 100 random tests, assert that Bonferroni-corrected p-values are used, not raw |
| Computing Greeks exclusively from provider-supplied values without independent Black-Scholes verification | Compute Greeks independently using Black-Scholes inversion with your own rate and dividend inputs. Cross-check against provider values. If Delta differs by >0.05, investigate which model input differs and flag for manual review. | `grep -rn "greeks\|delta\|gamma" src/ --include="*.py" \| grep -v "compute\|verify\|cross.check\|black.scholes\|bsm"` → finds direct use of provider Greeks without verification | `pytest tests/test_greeks_verification.py` — compute Greeks independently, assert `abs(computed_delta - provider_delta) < 0.05` |
| Validating signal performance over a single bull-market period (2020-2021) | Validate across at least three distinct market regimes: bull (2019-2021), bear (2022), and sideways/high-vol (2018 Q4, 2020 Q1). Reject signals that underperform in any regime — a real edge works across conditions. | `grep -rn "sharpe\|backtest.*result" backtest/ --include="*.py" \| grep -v "regime\|bear\|sideways\|vol"` → finds single-regime backtest results | `pytest tests/test_multi_regime.py` — runs strategy on 3 regimes, fails if any regime has negative returns or Sharpe < 0.5 |
| Flagging every high-premium trade as unusual without checking the ticker's historical distribution | Compute z-score of premium relative to the ticker's trailing 90-day distribution. Flag as UOA when z-score > 3.0. Use market-cap-appropriate thresholds: large-cap (z > 2.5), mid-cap (z > 3.0), small-cap (z > 3.5). | `grep -rn "premium.*>\|>\s*[\$]*[0-9].*premium" src/signals/ --include="*.py" \| grep -v "z.score\|zscore\|percentile\|distribution"` → finds absolute premium thresholds without normalization | `pytest tests/test_zscore_thresholds.py` — a $2M trade on SPY (normal) vs same trade on $500M small-cap (unusual) — assert different classifications |
| Feature leakage in time-series models: today's VIX close as a predictor of tomorrow's VIX (R² = 0.94) | Every feature must be time-stamped and lagged explicitly. Use point-in-time joins: features at time t can only use data known at time t-1. Implement `check_future_leakage()` function. Treat R² > 0.7 on financial data as a bug until proven otherwise. | `grep -rn "merge\|join" src/features/ --include="*.py" -A 3 \| grep -v "shift\|lag\|time.delta\|Timedelta"` → finds feature joins without explicit time lag | `pytest tests/test_feature_leakage.py` — train model with unlagged features, assert R² is suspiciously high; re-train with lagged features, assert R² drops significantly |
| Backtesting on the full universe of currently-listed tickers (survivorship bias) | Use a point-in-time ticker master with delisting history. For each backtest date, include all tickers tradable on that date. Account for delisting returns (often -100%) in P&L. A stock that goes to zero is part of the strategy's real return. | `grep -rn "ticker.*isin\|isin.*current\|WHERE.*ticker.*IN.*SELECT" src/backtest/ --include="*.py" \| grep -v "ticker_master\|trade_date\|as_of_date"` → finds universe filtering without point-in-time logic | `pytest tests/test_survivorship.py` — backtest on currently-listed vs full PIT universe, assert returns differ by > 2% annually (the bias is real) |

## Error Decoder
<!-- DEEP: 5min -- each entry includes a console-string matcher for automatic recovery loops -->

| 🖥️ Console Match (grep pattern) | Symptom | Root Cause | Fix | 🔄 Auto-Recovery Loop |
|---|---|---|---|---|
| `ValueError: x0 is infeasible\|RuntimeError: root finding did not converge` + `grep -rn "implied_volatility\|iv.*newton\|brentq\|fsolve" src/` finds IV solver | Black-Scholes implied volatility inversion failed to converge — returned NaN, downstream signal generation crashed | Newton-Raphson or Brent's method hit iteration limit because: (a) option is deep ITM/OTM with almost no time value, (b) bid-ask spread is wider than the model's tolerance, (c) market price violates no-arbitrage bounds. | Add convergence guards: max 100 iterations, fallback to bisection method, return `None` with diagnostic info instead of crashing. Log ticker, strike, expiry, market price, and bid-ask for failed convergences. | 1. Find IV solvers: `grep -rn "implied_vol\|brentq\|newton" src/ --include="*.py"` 2. Add fallback: `try: iv = newton(lambda s: bs_price(S, K, T, r, s) - market_price, x0=0.3, maxiter=100) except RuntimeError: iv = bisect(lambda s: bs_price(S, K, T, r, s) - market_price, 0.001, 5.0)` 3. Log failures: `if iv is None: logger.warning(f'IV solve failed: {ticker} K={K} T={T:.2f} price={market_price} bid={bid} ask={ask}')` 4. Test: feed intentionally bad prices, verify graceful None return |
| `ConvergenceWarning: Maximum Likelihood optimization failed to converge` + `grep -rn "GARCH\|fit\|ARCH\|EGARCH" src/ --include="*.py"` | GARCH/EGARCH model fitting failed — volatility forecast returned NaN, position sizing used wrong risk estimate | Poor initial parameter guesses for high-vol regimes. The optimizer hit parameter bounds (omega < 0, alpha + beta > 1). Default `scipy.optimize.minimize` settings too tight for financial data. | Relax convergence tolerance: `options={'ftol': 1e-5, 'maxiter': 2000}`. Scale returns (multiply by 100). Try multiple starting values (grid search for omega, alpha, beta). Fall back to EWMA if GARCH doesn't converge. | 1. Check for NaN: `assert not np.isnan(forecast.variance).any(), f'{np.isnan(forecast.variance).sum()} NaN values'` 2. Relax params: `model.fit(update_freq=0, disp='off', options={'maxiter': 2000, 'ftol': 1e-5})` 3. Grid search starting vals: `for omega in [0.01, 0.05, 0.1]: for alpha in [0.05, 0.1, 0.2]: try: res = model.fit(start_params=[omega, alpha, 1-alpha-omega])` 4. Fallback: `except: forecast = returns.ewm(span=20).std() * np.sqrt(252)` |
| `UserWarning: invalid value encountered\|RuntimeWarning: overflow` + `grep -rn "np.exp\|math.exp\|log\(" src/ -B 2 \| grep "dividend\|rate\|sigma"` | Black-Scholes d1/d2 calculation returned inf or NaN — strike adjustment or dividend yield caused overflow in `exp(-q*T)` | For deep ITM options with large T or high dividend yield, the `np.exp(-q * T)` term underflows to 0 or `np.exp(r * T)` overflows. The `log(S/K)` term can also blow up for extreme moneyness. | Clamp inputs before BS calculation: `S = max(S, 1e-6)`, `K = max(K, 1e-6)`, `T = max(T, 1e-6)`, `sigma = max(sigma, 1e-4)`. Use `np.log1p` for small inputs. Add warnings when inputs are extreme. | 1. Add input validation: `if S <= 0 or K <= 0 or T <= 0 or sigma <= 0: return {'price': np.nan, 'error': f'Invalid BS input: S={S}, K={K}, T={T}, sigma={sigma}'}` 2. Clamp: `S, K, T, sigma = max(S, 1e-6), max(K, 1e-6), max(T, 1/525600), max(sigma, 1e-4)` 3. Test extreme values: `bs_price(S=1e-10, K=1e10, T=10, r=0.5, sigma=5.0)` — must return gracefully |
| `AssertionError: put-call parity\|ValueError: Parity violation` + `grep -rn "put.call.parity\|pcp\|parity_check" src/` finds parity check failure | Put-call parity violation detected — C + PV(K) ≠ P + S. 500+ violations per day in options chain data. Either data is stale, dividend not adjusted, or rates wrong. | Data vendor's bid-ask quotes for calls and puts are not synchronized (different timestamps). Dividend yield assumption differs from actual. Interest rate proxy (LIBOR→SOFR) not updated. | Filter to only synchronous quotes (same `quote_timestamp` for call and put at same strike/expiry). Use implied forward from put-call parity instead of hardcoded rate. Flag violations > 5% of spot for manual review. | 1. Synchronize quotes: `merged = calls.merge(puts, on=['quote_timestamp', 'strike', 'expiration'], suffixes=('_call', '_put'))` 2. Compute parity: `parity_diff = (merged['call_bid'] + merged['strike'] * np.exp(-r * T)) - (merged['put_ask'] + merged['underlying_mid'])` 3. Threshold: `violations = merged[abs(parity_diff) > 0.05 * merged['underlying_mid']]` 4. Alert: `if len(violations) > 100: send_alert(f'{len(violations)} put-call parity violations')` |
| `LinAlgError: Singular matrix\|np.linalg.LinAlgError` + `grep -rn "np.linalg.inv\|np.linalg.solve\|cov" src/` finds matrix inversion | Covariance matrix for portfolio optimization or factor model is singular (not invertible) — more assets than time periods, or highly collinear assets | N assets > T time periods → covariance matrix rank-deficient. Or two assets have correlation = 0.999 (e.g., GOOGL and GOOG before merger complete). Standard `np.linalg.inv` fails. | Use pseudoinverse: `np.linalg.pinv(cov_matrix)`. Or regularize: add small diagonal term (`cov + 1e-6 * np.eye(n)`). Or use shrinkage estimator (Ledoit-Wolf): `from sklearn.covariance import LedoitWolf; cov = LedoitWolf().fit(returns).covariance_`. | 1. Detect: `if np.linalg.matrix_rank(cov) < cov.shape[0]: logger.warning(f'Cov matrix rank {np.linalg.matrix_rank(cov)} < {cov.shape[0]} assets — singular')` 2. Fix: `from sklearn.covariance import LedoitWolf; cov = LedoitWolf().fit(returns).covariance_` 3. Or pseudoinverse: `inv_cov = np.linalg.pinv(cov)` 4. Test: `pytest tests/test_covariance.py` — feed N=100 assets with T=50 periods, assert no LinAlgError |
| `KeyError: 'iv_rank'\|TypeError: unsupported operand` + `grep -rn "iv_rank\|iv_percentile" src/ -B 3 \| grep -v "earnings\|ex.div\|non.earnings"` | IV rank shows 50 but option is actually at 90th percentile — IV rank computed using 52-week range that includes an earnings volatility spike | The 52-week IV max was during an earnings event. Current IV is 60, max (earnings) is 120 → IV rank = 50. Excluding earnings, max IV is 70 → true IV rank = 85. Trading at IV rank 50 when true rank is 85 means buying overpriced options. | Compute IV rank from non-earnings periods only. Flag when 52-week IV max or min coincide with earnings dates (±1 day). Report both raw IV rank and earnings-excluded IV rank. Use the latter for position sizing. | 1. Detect earnings contamination: `earnings_dates = fetch_earnings_calendar(ticker); iv_max_date = iv_series.idxmax(); if abs((iv_max_date - earnings_dates).days).min() <= 1: logger.warning(f'{ticker}: IV max at {iv_max_date} coincides with earnings')` 2. Compute clean IV rank: `clean_iv = iv_series[~iv_series.index.isin(earnings_adjacent_dates)]; iv_rank_clean = (current_iv - clean_iv.min()) / (clean_iv.max() - clean_iv.min())` 3. Report both: `{iv_rank_raw: 0.50, iv_rank_clean: 0.85, warning: 'earnings_contaminated'}` |
## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. Each has a mechanical validation command. -->
<!-- Run: `bash scripts/checklist-quant.sh` for automated pass/fail on all items. -->

| ID | Checklist Item | Validation Command | Auto-Fix |
|----|---------------|-------------------|----------|
| **[S1]** | Options chain data validated: stale quotes rejected (>60s old), bad condition codes filtered, bid-ask spread sanity checked | `python3 -c "from validation.chain_validator import validate; r = validate(chain); assert r.passed, f'Chain validation failed: {r.failures}'"` → exit 0 | `pytest tests/test_chain_validation.py` — inject stale quotes, bad codes, wide spreads, assert rejection |
| **[S2]** | Greeks computed independently via Black-Scholes inversion — cross-checked against provider values (Delta diff < 0.05) | `python3 -c "from pricing.greeks import verify; d = verify(chain); assert max(abs(d['delta_diff'])) < 0.05, f'Max Delta diff: {max(abs(d[\"delta_diff\"])):.4f}'"` → exit 0 | `pytest tests/test_greeks_verification.py` — compute Greeks independently, compare to provider, assert within tolerance |
| **[S3]** | IV Rank computed from non-earnings periods only — earnings-contaminated 52-week range flagged | `python3 -c "from vol.iv_rank import compute_clean; ivr = compute_clean(iv_history, earnings_calendar); assert not ivr.empty, 'IV rank computation returned empty'"` → exit 0 | Script: `python3 scripts/compute_iv_rank.py --ticker SPY --exclude-earnings` |
| **[S4]** | Multiple-testing correction applied: Bonferroni or Benjamini-Hochberg FDR on all hypothesis test batches > 20 tests | `grep -rn "multipletests\|bonferroni\|fdr_bh\|benjamini" src/ --include="*.py"` → must match in every file that contains `p_value` or `pvalue` | `pytest tests/test_multiple_testing.py` — runs 100 random tests, asserts corrected p-values differ from raw |
| **[S5]** | OI comparison executed: volume/OI ratio computed per strike+expiry; opening vs closing classified | `python3 -c "from signals.oi_analyzer import classify; c = classify(trade, oi_history); assert c.activity in ('OPENING', 'CLOSING', 'UNKNOWN'), f'Unknown classification: {c.activity}'"` → exit 0 | `pytest tests/test_oi_classification.py` — test known opening and closing trades, assert correct classification |
| **[S6]** | Multi-leg detection run within 60s windows — spreads, straddles, combos identified before directional classification | `python3 -c "from signals.multi_leg import detect; legs = detect(trades, window_seconds=60); assert len(legs) > 0 or len(trades) == 0, 'Multi-leg detection returned empty for non-empty trades'"` → exit 0 | `pytest tests/test_multi_leg.py` — inject straddle and spread trades, assert correct multi-leg grouping |
| **[S7]** | Side determination completed: trade price vs contemporaneous bid/ask; ASK/BID/MID assigned with timestamp | `python3 -c "from signals.side_classifier import classify_side; s = classify_side(trade, quote); assert s.side in ('ASK', 'BID', 'MID'), f'Unknown side: {s.side}'"` → exit 0 | `pytest tests/test_side_classification.py` — test trades at bid, ask, and mid, assert correct classification |
| **[S8]** | Signal classification applied per matrix; confidence levels (STRONG/MODERATE/WEAK) assigned with evidence | `python3 -c "from signals.classifier import SignalClassifier; signals = SignalClassifier().classify(trades); assert all(s.confidence in ('STRONG','MODERATE','WEAK') for s in signals)"` → exit 0 | `pytest tests/test_signal_classification.py` — full end-to-end, assert every signal has confidence and evidence |
| **[S9]** | Z-score premium normalization: premium relative to ticker's trailing 90-day distribution; different thresholds per market-cap tier | `python3 -c "from signals.zscore import compute_zscores; z = compute_zscores(trades, lookback_days=90); assert all(z.threshold_applied), 'Missing z-score thresholds'"` → exit 0 | `pytest tests/test_zscore.py` — feed known distributions, assert z > 3 triggers UOA flag |
| **[S10]** | Earnings calendar loaded; all signals within 2 days of earnings downgraded one confidence level | `python3 -c "from signals.earnings_filter import apply_blackout; s = apply_blackout(signals, earnings_cal, days=2); assert all(sig.confidence_before >= sig.confidence_after for sig in s if sig.near_earnings)"` → exit 0 | `pytest tests/test_earnings_filter.py` — inject signals near earnings, assert confidence downgraded |
| **[S11]** | Survivorship-bias-free dataset: ticker master includes delisted/bankrupt tickers with `first_trade_date` and `last_trade_date` | `python3 -c "from data.ticker_master import check_survivorship; r = check_survivorship(); assert r.distinct_per_year_variance < 0.1, f'Ticker count varies {r.distinct_per_year_variance:.1%} per year — survivorship bias suspected'"` → exit 0 | Script: `python3 scripts/backfill_delisted_tickers.py --source=CRSP` |
| **[S12]** | Walk-forward validation: minimum 3 distinct market regimes, out-of-sample Sharpe within 20% of in-sample | `python3 -c "from validation.walk_forward import validate; r = validate(strategy, min_regimes=3); assert r.sharpe_stability < 0.2, f'Sharpe varies {r.sharpe_stability:.1%} across regimes'"` → exit 0 | `pytest tests/test_walk_forward.py` — validates across bull, bear, sideways regimes |

## Footguns
<!-- DEEP: 10+min — war stories from quantitative research and signal generation -->

| Footgun | What Happened | Root Cause | How to Prevent |
|---------|---------------|------------|----------------|
| A volatility arbitrage model "predicted" VIX with R²=0.94 — because the training data included the VIX settlement value as a feature, leaking the target into the input | A quant researcher at a $1.2B fund built a VIX prediction model using 47 features including "VIX close." The model appeared to predict next-day VIX with near-perfect accuracy for 3 months of paper trading. When deployed live, it lost $800K in the first week. The researcher had accidentally included `vix_close_today` in the feature set by joining on the wrong date index — the model was learning that "today's VIX close" equals "today's VIX close," discovering identity, not alpha. | The feature engineering notebook joined the feature table on `trade_date` instead of `trade_date - 1`. Pandas' merge defaults to inner join without warning. The model's R² of 0.94 should have been the first red flag — no financial time series is that predictable. | **Every feature must be time-stamped and lagged explicitly.** Use point-in-time joins: features at time t can only use data known at time t-1. Implement a `check_future_leakage()` function that tests whether any feature correlates with future returns at lag 0. Treat R² > 0.7 on financial data as a bug until proven otherwise — extraordinary performance means extraordinary data leakage. |
| UOA signal "STRONG BUY" fired 47 times — but 24 were on tickers where the same institution was selling stock in block trades while buying calls as a hedge | A quant analyst at a proprietary trading desk built an unusual options activity detector. It flagged $3M+ in OTM call buying as "STRONG BUY." For 6 weeks, the desk bought calls on these signals and lost money on 18 of 24 trades. Post-mortem: 14 of the losing trades were on tickers where the same fund was executing a block sale of the underlying stock and buying OTM calls as a delta hedge — the options flow was bearish, not bullish, in context. | The signal classified option flow in isolation. It didn't cross-reference with equity block trade data (dark pool prints, Form 4 filings, 13F filings). A $5M call purchase means opposite things when accompanied by a $50M stock sale vs a standalone bet. | **Options flow is never bullish or bearish in isolation.** Cross-reference every large option trade against: (1) same-day block trades in the underlying (FINRA TRF data), (2) the institution's recent 13F filings for their existing position, (3) whether the trade is delta-neutral vs directional based on concurrent activity. A call purchase hedging a short stock position is bearish flow — classifying it as bullish is a career-limiting mistake. |
| A quant promo presentation showed "Sharpe 2.1 on out-of-sample data" — the "out-of-sample" period was selected from 20 candidate windows, choosing the one with the best result | A junior quant presented a momentum strategy to the PM with a Sharpe of 2.1 on "out-of-sample" data from 2019–2020. The PM allocated $50M. After 6 months of live trading at Sharpe -0.4, a peer reviewed the research code and discovered the quant had tested 20 different out-of-sample windows and presented the best one. The quant genuinely believed this was valid because "each window was out of sample." | The researcher confused "out of sample" with "unbiased." Testing 20 windows and selecting the best is 20 independent hypothesis tests — a form of p-hacking applied to time windows. With 20 attempts, the probability of finding at least one window with Sharpe > 1.5 purely by chance is over 40%. | **Pre-register your out-of-sample window before running any test.** The window must be fixed before you see any results. Use the most recent N months as the single out-of-sample period — never cherry-pick. Report the strategy's performance in ALL candidate windows, including the worst one. If a strategy's returns are fragile to the window choice, it's not a strategy — it's overfitting wearing a lab coat. |
| The VIX was 14, IV Rank was 22nd percentile — the model said "sell premium," but it was March 9, 2020, and COVID was about to send VIX to 82 | A volatility selling strategy at a $300M options fund had a rule: "Sell straddles when IV Rank < 30." On March 9, 2020, VIX was at 14 and IV Rank was 22 — the model fired "SELL VOL." The PM overrode it because headlines were screaming. If executed, the position would have lost $12M as VIX hit 82 the following week. The model's entire training set (2017–2019) had zero pandemic events. | The model had no tail-risk awareness. IV Rank measures where current IV sits relative to its own history — it doesn't know about events that haven't happened yet. A 22nd-percentile IV before a pandemic is not "cheap" — it's "about to become historically expensive." | **Every volatility signal must include a forward-looking catalyst check.** Query an economic calendar and news sentiment feed before generating signals. If there's a Fed meeting, election, or emerging macro crisis within the position's DTE window, downgrade the signal. IV Rank tells you where IV has been — it says nothing about where it's going. The worst vol-selling losses happen when the model says "IV is low" and reality says "for good reason." |
| Published research showed 87% win rate on UOA trade signals — but the signal database had survivorship bias: it only included tickers still trading today, excluding the 34% that went bankrupt or were delisted | A quant research team at a sell-side desk published internal research claiming an 87% directional accuracy for $5M+ unusual options flow. Traders who followed the signals for 8 months got 51% accuracy — coin-flip territory. The audit revealed the backtest dataset excluded 1,200+ tickers that had been delisted since 2010. The excluded tickers had the worst returns — every delisted company had "bullish" option flow before bankruptcy because insiders were buying puts and selling calls, creating synthetic bearish flow that the classifier mislabeled. | The vendor dataset (CBOE LiveVol) defaults to excluding delisted symbols. The research team never checked the denominator — they assumed the database contained "all options trades" when it contained "all options trades for currently listed stocks." | **Always request survivorship-bias-free datasets and verify.** Count distinct tickers per year in your data — if the count decreases monotonically as you go back in time, you have survivorship bias. Buy a delisted securities database (CRSP for US equities provides this). Run your entire analysis pipeline on a dataset that includes delisted tickers. If your signal accuracy drops, the drop IS the bias — your real alpha is that smaller number. |

## Calibration — How to Know Your Level
<!-- STANDARD: 3min — honest self-assessment -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You report a backtest Sharpe of 2.5 and think "this strategy is ready for production" instead of "where is the data leak?" | You've had at least one strategy that backtested beautifully and failed live — and you can explain exactly which assumption broke and why you missed it | A quant brings you a backtest with Sharpe 3.0 and you find the look-ahead bias, survivorship bias, or multiple-testing error within 15 minutes of code review — and you're right 90% of the time |
| You classify an options trade as "bullish" or "bearish" based solely on call vs put and ask vs bid | You cross-reference every large option trade against the underlying's block trade activity, the institution's existing position, and concurrent multi-leg activity before assigning direction | You've built a flow classification system that correctly identifies synthetic positions (e.g., risk reversal = bullish, collar = hedged) and your directional accuracy on $5M+ trades is above 65% over a 500-trade sample |
| You generate signals with confidence labels like "HIGH" but can't quantify what "high" means in terms of historical win rate | Your confidence levels are calibrated: "HIGH" = historical win rate 65-75%, "MEDIUM" = 55-65%, and you recalibrate monthly based on rolling performance | Your signals have been running in production for 2+ years and the realized win rate per confidence bucket is within 3% of the stated range — and the algorithmic trader who executes them hasn't overridden a confidence level in 12 months |

**The Litmus Test:** Take your last 100 generated signals. Can you compute the Brier score (mean squared error between predicted confidence and actual binary outcome)? If your HIGH-confidence signals have a historical win rate of 60% but you label them "80% confident," your calibration is broken. A properly calibrated quant can state "this signal has a 62% probability of being correct" and the long-run frequency will be 62% ± 3%. If you can't produce that number, you're not L3.

## Cross-Skill Coordination
<!-- STANDARD: 3min — how this skill chains with others in the finance domain and beyond -->

### Coordinate With

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **Market Data Engineer** | Raw options chain data needed (quotes, trades, greeks, OI); data freshness issues; new data sources | Required data fields: strike, expiry, bid, ask, last, volume, OI, condition codes, Greeks (if provider-computed), underlying price, dividends calendar, earnings calendar. SLA: data freshness < 60 seconds for UOA detection. |
| **Algorithmic Trader** | Delivering structured trade signals for execution; entry trigger refinement | Signal JSON per Phase 5 schema. Entry trigger conditions, stop-loss/take-profit levels, position sizing guidance. Feedback loop: which signals executed, fills achieved, P&L outcomes. |
| **Data Scientist** | Statistical validation of signal performance; backtesting UOA signal efficacy; calibration of confidence levels | Historical signal dataset for backtesting. Request: win-rate analysis by signal strength, DTE bucket performance, false-positive rate around events. Receive: calibrated confidence thresholds, feature importance for signal classification. |
| **ML/AI Engineer** | Advanced signal classification (ML-based instead of rules-based); pattern recognition in options flow; anomaly detection models | Feature-engineered UOA dataset. Alternative to rules-based signal matrix when enough labeled data exists. ML model for trade classification (sweep vs block vs noise), sentiment scoring from options flow, predictive signal fusion. |
| **Data Scientist** | Statistical validation of signal performance; backtesting UOA signal efficacy; calibration of confidence levels | Historical signal dataset for backtesting. **Decision gate:** Is win-rate > 50% on 30-day rolling window? → signals are production-grade. Request: win-rate analysis by signal strength, DTE bucket performance, false-positive rate around events. **Artifact:** calibrated confidence thresholds + feature importance report. |
| **ML/AI Engineer** | ML-based signal classification; pattern recognition in options flow; anomaly detection models | Feature-engineered UOA dataset. **Decision gate:** Does labeled dataset have > 10K examples? → ML approach viable. Alternative to rules-based signal matrix. **Artifact:** trained model + classification accuracy report. |
| **Business Strategist** | Macro context for sector rotation signals; strategic positioning guidance | Sector-level UOA summaries (net call/put premium by sector, week-over-week changes). Strategic questions: "Which sectors are seeing unusual accumulation via options?" |
| **Compliance Officer** | Regulatory review of signal generation methodology; audit trail | Full signal generation pipeline documentation. Trade rationale for every signal. Model risk management documentation if ML-based classification is used. |

### Communication Triggers

| Trigger | Notify | Why |
|---------|--------|-----|
| Market data pipeline stale (>5 min no updates) | Market Data Engineer | UOA detection degrades rapidly with stale data; signals become unreliable |
| STRONG BUY signal generated (≥$5M, high confidence) | Algorithmic Trader | High-priority signal requiring immediate evaluation for execution |
| Signal batch complete for the day | Algorithmic Trader, Data Scientist | Batch handoff for execution + backtest incorporation |
| IV Rank > 95 across multiple names in same sector | Algorithmic Trader, Business Strategist | Potential sector-wide volatility event or regime change |
| Put-call parity violation detected (genuine arb) | Algorithmic Trader | Time-sensitive arbitrage opportunity (rare, but high-value) |
| Signal win-rate drops below 50% on 30-day rolling window | Data Scientist, Algorithmic Trader | Signal degradation — may need recalibration or model retraining |

### Escalation Path
```
Signal with >5% of float in notional? → Algorithmic Trader → Business Strategist (market impact concern)
Model performance degrading (win rate < 45%)? → Data Scientist → ML/AI Engineer (recalibration)
Data pipeline failure blocking UOA? → Market Data Engineer → DevOps Engineer
Regulatory inquiry about signal methodology? → Compliance Officer → Legal Advisor
Sector-wide anomaly (10+ STRONG BUY in single sector)? → Business Strategist → CEO Strategist
```

### Skill Chain Commands
```bash
# Full options flow pipeline: data → analysis → execution
/market-data-engineer && /quantitative-analyst && /algorithmic-trader

# UOA signal backtesting loop
/quantitative-analyst && /data-scientist && /quantitative-analyst

# ML-enhanced signal classification (alternative to rules-based)
/market-data-engineer && /quantitative-analyst && /ml-ai-engineer && /algorithmic-trader

# Market data engineer provides clean options chains.
# Quantitative analyst detects UOA, computes Greeks, generates signals.
# Algorithmic trader consumes signals for execution decisions.
```

## Proactive Triggers
<!-- QUICK: 30s -- when to proactively notify stakeholders -->

| Trigger | Notify | Why |
|---------|--------|-----|
| STRONG BUY signal generated with premium >$5M and OI ratio >2x | algorithmic-trader | Highest-priority signal requiring immediate evaluation; Theta decay starts at signal generation — every minute of delay reduces the edge |
| IV Rank exceeds 95 across 5+ names in same sector | algorithmic-trader + business-strategist | Potential sector-wide volatility event or regime change; review all open positions in affected sector for Vega exposure and correlation |
| Signal win-rate drops below 50% on 30-day rolling window | data-scientist + algorithmic-trader | Signal degradation detected — may indicate regime change, data quality issue, or model drift; recalibrate classification thresholds before next trading session |
| Put-call parity violation exceeds 5% of spot on active options chain | algorithmic-trader + market-data-engineer | Genuine arbitrage opportunity or data corruption — verify data quality with market-data-engineer first; evaluate arb execution only if data is confirmed clean |
| Earnings calendar shows 3+ portfolio holdings reporting within 48 hours | algorithmic-trader | Elevated event risk concentrated in the portfolio — downgrade all signals on affected tickers, reduce position sizes 50%, tighten stop distances |
| Market data pipeline reports >5 minutes of stale quotes during trading session | market-data-engineer + algorithmic-trader | UOA detection degraded — all signals generated during the gap window are unreliable; flag and downgrade affected signals, pause new signal generation until feed recovers |
| Sector ETF performance diverges >3% from signal direction in same week | algorithmic-trader + business-strategist | Signal is fighting macro tape — downgrade confidence on all counter-trend signals in the sector; sector headwind is a stronger signal than individual option flow |
| Computed Greeks diverge >10% from provider values on 3+ tickers simultaneously | market-data-engineer | Possible data feed corruption, incorrect dividend assumptions, or rate curve mismatch; halt signal generation until root cause identified — trading on wrong Greeks is worse than not trading |

## What Good Looks Like
<!-- STANDARD: 2min — the bar for production-quality quantitative analysis -->

A 10/10 quantitative analyst output reads like a professional options flow desk report. Here's what distinguishes excellent from adequate:

**Excellent signal delivery:**
> "**STRONG BUY — XYZ Corp ($4.2B mid-cap)** | Confidence: HIGH | DTE: 45 days
> **Signal**: $5.2M ask-side OTM calls at $55 strike (spot: $48.50, delta: 0.31). Sweep execution across CBOE, PHLX, and NASDAQ within 3 seconds. OI ratio 2.3x → new positions opening, not closing. IV rank 78 (elevated but justified by sector momentum).
> **Context**: Sector ETF (XLY) +2.8% this week. No earnings for 47 days. Short interest 8.2% of float — potential squeeze fuel.
> **Entry**: On breakout above $50 (20-day high) with volume > 1.5x average. Stop: $42.25 (-15%). Target: $65 (+30%).
> **Risks**: Mid-cap liquidity (avg spread $0.18). IV crush risk if sector rotates. Position size 0.13% of market cap — significant but not alarming."

**Adequate (but not excellent) signal delivery:**
> "XYZ had big call buying today. $5M in premium. Probably bullish. Consider buying calls."

The difference: **specificity, context, confidence calibration, entry/exit precision, and risk acknowledgment**. An excellent signal never says "probably" — it says "HIGH confidence with these specific evidence points and these specific risks."

Key quality markers:
- Every number has context (IV rank 78 means expensive, but we explain WHY it might be justified)
- Entry triggers are falsifiable (breakout above $50, not "buy on strength")
- Risks are named, not hand-waved ("IV crush risk" with specific catalyst)
- Position sizing awareness (premium relative to market cap, not just absolute dollars)
- Exit plan exists before entry (stop-loss and take-profit at signal generation time)

## Deliberate Practice

```mermaid
graph LR
    A[Build] --> B[Measure<br/>failure modes] --> C[Study<br/>post-mortems] --> D[Re-build<br/>with constraints] --> A
```

| Level | Practice | Frequency |
|-------|----------|-----------|
| **Novice** | Rebuild an existing system from scratch, then compare your design with the original | Monthly |
| **Competent** | Add a new constraint (10x data, zero downtime, etc.) to a familiar design and re-architect | Quarterly |
| **Expert** | Design the same system under 3 conflicting constraint sets; write a decision record for each | Quarterly |
| **Master** | Teach a junior to design a system; your role is to ask questions, not give answers | Monthly |

**The One Highest-Leverage Activity:** Every quarter, take a system you built 6+ months ago and redesign it from scratch with what you know now. Write down what changed and why.

## References
<!-- QUICK: 30s — links to deeper reading and canonical sources -->
- **Options Pricing Models**: [Black-Scholes Reference](references/black-scholes.md), [Binomial Tree Methods](references/binomial-tree.md), [Monte Carlo Simulation for Options](references/monte-carlo.md)
- **Greeks**: [Greeks Field Manual](references/greeks-reference.md) — formulas, interpretations, position Greeks, portfolio hedging
- **UOA Detection**: [UOA Algorithm Specification](references/uoa-detection.md) — full pseudocode, condition codes dictionary, exchange code mappings
- **Volatility Analysis**: [IV Surface Construction](references/iv-surface.md), [Skew & Term Structure Guide](references/volatility-analysis.md)
- **Signal Generation**: [Signal Classification Matrix](references/signal-classification.md), [Entry Strategy Rules](references/entry-strategies.md)
- Hull, John C. — *Options, Futures, and Other Derivatives* (the canonical textbook; 11th edition)
- Natenberg, Sheldon — *Option Volatility and Pricing* (practitioner's bible on Greeks, volatility, and trading strategy)
- Sinclair, Euan — *Volatility Trading* (practical volatility surface and options market making)
- Haug, Espen Gaarder — *The Complete Guide to Option Pricing Formulas* (exhaustive formula reference)
- https://www.cboe.com/ — CBOE options data, VIX methodology, condition code definitions
- https://www.optionseducation.org/ — OIC (Options Industry Council) educational resources

## Scale Depth
<!-- QUICK: 30s — find your team size column -->

### Solo (1 person, personal account)
- **What changes**: You are the quant, the data engineer, and the trader. Use free options data (Yahoo Finance delayed quotes, Polygon.io free tier). Focus on UOA on 5-10 mid-cap names you know well. Rules-based signals only (no ML). Manual entry from signals — no automated execution. Excel + Python scripts. Greeks from free calculators (no real-time surface).
- **What to skip**: Real-time scanning (end-of-day is fine). Multi-leg detection (manual spotting). Full IV surface construction. Automated execution. ML-based classification. Institutional-grade data feeds.
- **Coordination**: Self-contained. Track signals in a spreadsheet. Review weekly.
- **Cost**: Free — Yahoo Finance, Python (scipy, numpy, pandas), Polygon.io free tier (5 API calls/min).

### Small Team (2-10 people, small fund/prop trading)
- **What changes**: Real-time options data feed (OPRA via broker API or paid provider like ORATS, CBOE DataShop). Automated UOA scanner running intraday. Greeks computed in real-time (Black-Scholes inversion on every tick). Rules-based signals with basic backtesting. Signal delivery via Slack/email to trader. IV surface built daily. Multi-leg detection via time-clustering. Sector ETF context from free market data APIs.
- **What to skip**: ML-based signal classification. Real-time IV surface (daily rebuild is fine). Full portfolio Greeks integration. Automated execution (manual review still). Tick-level data storage. Custom pricing models beyond Black-Scholes.
- **Coordination**: Morning signal review. Weekly backtest review with trader feedback loop. Coordinate with data provider for feed reliability.
- **Cost**: $500-$3,000/month (OPRA data feed, small cloud VM for scanner, basic market data APIs).

### Medium Team (10-50 people, mid-size fund)
- **What changes**: Full institutional data feed (Bloomberg/Reuters/OPRA direct). Real-time UOA scanner with tick-level processing. ML-based signal classification alongside rules-based (ensemble approach). Real-time IV surface with arbitrage-free interpolation (SVI/SSVI parameterization). Automated execution of STRONG BUY signals (human override for BUY/WEAK). Portfolio-level Greeks and risk. Historical tick database for backtesting. Automated multi-leg detection with strategy recognition.
- **What to skip**: Custom exchange connectivity (use broker API). Full HFT infrastructure (not needed for mid-frequency options flow). Market making models. Exotic options pricing (focus on vanilla US equity options).
- **Coordination**: Daily signal review meeting. Bi-weekly model performance review with data scientist. Integration with execution/OMS. Compliance review of signal methodology.
- **Cost**: $10K-$50K/month (Bloomberg terminal, OPRA direct feed, cloud compute for scanning + ML, execution platform).

### Enterprise (50+ people, large fund/bank trading desk)
- **What changes**: Colocated OPRA feed processing. FPGA-accelerated UOA detection (microsecond latency). Deep learning signal classification with attention mechanisms on order flow. Real-time, arbitrage-free IV surface across all strikes/expiries. Full integration with OMS/EMS for automated execution with smart order routing. Real-time portfolio Greeks with scenario analysis (SPX -5%, VIX +10, etc.). Tick data warehouse with petabyte scale. Quantitative research platform for signal alpha research. Counterparty flow analysis. Multi-asset options (equity, index, ETF, futures options).
- **What's full production**: 24/7 operations team. Model risk management framework. Regulatory capital calculations integrated with options positions. Cross-asset risk management. Dedicated quant research team. Annual model audits.
- **Coordination**: Daily risk meeting. Weekly quant research review. Monthly model governance committee. Quarterly regulatory review.
- **Cost**: $200K-$1M+/month (colocation, data, compute, team, compliance, execution).

### Transition Triggers
| From → To | Trigger | What to Change |
|-----------|---------|----------------|
| Solo → Small | >$50K AUM or 10+ signals/week requiring real-time response | Add real-time data feed; automate UOA scanner; start Greeks computation |
| Small → Medium | 50+ signals/day, AUM >$5M, need automated execution | Add ML classification; build real-time IV surface; integrate with OMS |
| Medium → Enterprise | Multi-asset options, regulatory requirements, >$100M AUM | Colocate; add FPGA/DL pipeline; build quant research platform; hire risk team |
