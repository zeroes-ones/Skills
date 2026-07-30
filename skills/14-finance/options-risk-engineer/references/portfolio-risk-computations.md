# Portfolio Risk Computations — Detailed Reference

> Extracted from options-risk-engineer Core Workflow. Contains full computation examples, formulas, and rule tables. Referenced by the compact Core Workflow skeleton in SKILL.md.

## Phase 0: Portfolio Greek Snapshot — Full Detail

### Greek Aggregation

For each position, pull individual Greeks from quantitative-analyst output:

```json
{
  "position_id": "AAPL-250C-20260821",
  "ticker": "AAPL",
  "type": "LONG_CALL",
  "strike": 250,
  "expiration": "2026-08-21",
  "quantity": 5,
  "underlying_price": 248.50,
  "individual_greeks": {
    "delta": 0.48, "gamma": 0.032, "theta": -0.12,
    "vega": 0.28, "vanna": 0.008, "charm": -0.003
  }
}
```

**Portfolio-Level Aggregation:**

| Greek | Formula | Example Output |
|-------|---------|---------------|
| Net Delta | Σ(pos.delta × qty × multiplier × underlying_price) | +$47,520 — equivalent to 191 AAPL shares |
| Net Gamma | Σ(pos.gamma × qty × multiplier × underlying_price / 100) | +$1,260/1% move |
| Net Theta | Σ(pos.theta × qty × multiplier) | +$85/day (0.0085% of $1M NAV) |
| Net Vega | Σ(pos.vega × qty × multiplier) | +$3,200/1% IV change |
| Vanna | d(Delta)/d(IV) | +$420/%IV — delta increases in volatile markets |
| Charm | d(Delta)/d(Time) | -$180/day — delta decay from time passage |

**Theta/NAV assessment:** <0.005%/day = negligible | 0.01-0.03%/day = healthy | >0.05%/day = excessive short premium

**GEX Range:** Profile gamma at ±1%, ±2%, ±5% underlying moves to understand convexity.

### Greek Limit Enforcement

| Limit | Threshold | Consequence if Breached |
|-------|-----------|------------------------|
| Max Net Delta | ±50% of NAV | Portfolio is directional, not options-neutral |
| Max Net Gamma | ±5% of NAV per 1% move | Risk profile changes too rapidly |
| Max Net Vega | ±5% of NAV per 1-point IV | Vol moves dominate P&L |
| Min Net Theta | Positive preferred; negative > -0.02%/day needs justification | Paying for protection must be intentional |
| Max Vanna/Delta | Vanna > 2× daily theta | Rising vol increases directional exposure |

---

## Phase 1: Pin Risk & Assignment Detection — Full Detail

### Pin Risk Score (0-100)

```
Pin_Risk_Score = distance_component × dte_multiplier × position_factor
```

**Distance Component:**
- 0–0.25% from strike: 90
- 0.25–0.5%: 70
- 0.5–1.0%: 40
- 1.0–1.5%: 20
- >1.5%: 5

**DTE Multiplier:**
- DTE=0: 1.5 (expiration gamma spike)
- DTE=1: 1.3
- DTE=2: 1.1
- DTE=3–5: 1.0
- DTE>5: 0.7

**Position Factor:**
- Short naked call: 1.3 (unlimited risk)
- Short naked put: 1.1 (defined but large)
- Short vertical spread: 0.7 (defined risk)
- Short covered call: 0.4 (stock covers)

**Action Thresholds:**
- Score ≥ 60: CLOSE OR ROLL IMMEDIATELY
- Score 40–59: Close/roll at next opportunity
- Score 20–39: Set price alert at strike ±0.5%

### Assignment Risk Triggers (American-Style)

| Trigger | Rule | Assignment Probability |
|---------|------|----------------------|
| CALL: Ex-div + dividend > time premium by $0.10+ | Dividend arbitrage | 85%+ |
| CALL: Ex-div + dividend > time premium by $0.05–$0.10 | Marginal arbitrage | 60–85% |
| PUT: Deep ITM (>$2.00) + time premium < $0.05 | Capital efficiency exercise | 75% |
| ITM by >$2.00 + DTE < 3 | Near-expiration capture | 70%+ |
| Special situations (merger, tender) | Event-dependent | Flag, don't estimate |

### Pre-Close Rules

| Condition | Action |
|-----------|--------|
| Short call ITM >$0.50 AND ex-div within 3 days | CLOSE OR ROLL IMMEDIATELY |
| Short put ITM >$2.00 AND DTE < 3 | CLOSE OR ROLL |
| Pin Risk Score ≥ 60 | CLOSE at market |
| Pin Risk Score 40–59 AND DTE ≤ 2 | CLOSE with limit; market if unfilled in 5 min |
| Short ITM at 3:30 PM ET expiration day | CLOSE (physical delivery) or let expire (cash-settled) |

---

## Phase 2: Expiration Risk Management — Full Detail

### DTE-Based Action Rules

| DTE Range | Action Required | Rationale |
|-----------|----------------|-----------|
| >21 DTE | Normal monitoring | Gamma manageable, theta linear |
| 14–21 DTE | Begin expiration planning | Evaluate close/roll/expire |
| 7–14 DTE | Gamma acceleration zone | Gamma ~2× from 14 to 7 DTE |
| 3–7 DTE | Active management | Gamma 3–5× normal, pin risk active |
| 0–3 DTE | CRITICAL zone | Every hour matters, gamma → ∞ |
| 0 DTE | Expiration day protocol | Continuous monitoring |

### Physical vs Cash-Settled

**Physical Delivery (most equity options):**
- LONG CALL ITM → BUY 100 shares at strike (need cash)
- SHORT CALL ITM → SELL 100 shares at strike (unlimited risk if naked)
- LONG PUT ITM → SELL 100 shares at strike
- SHORT PUT ITM → BUY 100 shares at strike (need cash)

**Cash-Settled (SPX, NDX, RUT, VIX):**
- ITM → cash credit/debit = (settlement - strike) × multiplier
- No stock delivery, no weekend gap risk

**Friday Expiration Protocol:**
- ITM short options (physical): CLOSE by 3:00 PM ET Friday
- ITM long options (physical, insufficient capital): CLOSE by 3:30 PM ET
- Cash-settled index options: Safe to let expire
- No new same-day-expiring options after 2:00 PM ET

### 0DTE Rules

- Max notional: 2% of NAV per position
- Continuous monitoring (≤60 seconds)
- Hard stop: -50% of premium (directional) or -100% of credit (spreads)
- No 0DTE short naked — defined risk only

---

## Phase 3: Margin & Capital Efficiency — Full Detail

### Regime Detection

| Account Type | Margin Rules | Key Feature |
|-------------|-------------|-------------|
| Standard Reg T | 50% initial, 25% maintenance (equities) | Simple, rule-based |
| Portfolio Margin (≥$110K) | Theoretical stress test: ±15% indices, ±20% stocks | Portfolio-level, risk-based |
| Futures Options (SPAN) | 16 risk array scenarios per contract | Most capital-efficient |

### Reg T Margin by Strategy

| Strategy | Initial Margin |
|----------|---------------|
| Long Call/Put | 100% of premium |
| Short Naked Call | Premium + 20% underlying - OTM |
| Short Naked Put | Premium + 20% underlying - OTM |
| Covered Call | Stock margin + option premium |
| Vertical Spread (debit) | Debit paid |
| Vertical Spread (credit) | Width × 100 - credit received |
| Iron Condor | Max(put_spread_margin, call_spread_margin) |
| Short Straddle/Strangle | Naked call margin + naked put margin |

**Example — Short AAPL 250 Put (AAPL at $248.50):**
- Premium: $3.50 × 100 = $350
- 20% underlying: 20% × $24,850 = $4,970
- OTM: ($250 - $248.50) × 100 = $150
- Reg T Margin = $350 + $4,970 - $150 = **$5,170** (20.7% of notional)

### Portfolio Margin (PM)

PM margin = max loss across stress scenarios:
- Broad-based indices: ±15% price move
- Single stocks: ±20% price move

**PM vs Reg T:**
- Defined-risk strategies: PM ≈ Reg T
- Naked options: PM 40–60% LOWER
- Hedged portfolios: PM 50–70% LOWER
- Concentrated portfolios: PM can be HIGHER (penalizes concentration)

### Margin Call Distance

```
Margin_Call_Distance = (NAV - Maintenance_Margin) / NAV
>20%: Green | 10–20%: Yellow | 5–10%: Orange | <5%: Red — IMMEDIATE action
```

### Buying Power Reduction

```
BPR = margin_required / buying_power_total
<30%: Healthy | 30–50%: Cautious | 50–70%: Tight | >70%: DANGER
```

---

## Phase 4: Liquidity & Slippage — Full Detail

### Liquidity Scoring

| Component | Green | Yellow | Orange | Red |
|-----------|-------|--------|--------|-----|
| Bid-Ask Spread | <2% of mid | 2–5% | 5–10% | >10% |
| Open Interest | >10,000 | 1,000–10,000 | 100–1,000 | <100 |
| Position vs OI | <1% | 1–5% | 5–10% | >10% |

### Slippage Estimates

| Liquidity | Market Order | Limit Order |
|-----------|-------------|-------------|
| Liquid (spread <2%) | 0.5–1.5% | 0.2–0.8% (mid ± spread/4) |
| Moderate (2–5%) | 2–5% | May not fill at mid |
| Illiquid (>10%) | >20% round-trip | DO NOT TRADE |

### Position Sizing with Liquidity

```
Max_Position_Size = min(Kelly_vol_size, 5% × 20d_avg_dollar_vol, 5% × open_interest)
```

---

## Phase 5: Options as Hedging Instruments — Full Detail

### Hedge Selection by Risk Type

| Risk | Instrument | Cost (% NAV/year) |
|------|-----------|-------------------|
| Single-stock downside | Protective puts, collars | 8–20% |
| Portfolio-wide decline | Index puts (SPY, QQQ) | 3–8% |
| Tail risk (3σ+) | Deep OTM puts, VIX calls | 1–3% |
| Correlation breakdown | VIX futures, variance swaps | 2–5% |
| Vol expansion (short vega) | Long VIX calls, long straddles | 3–6% |

### Protective Put Cost Comparison (AAPL at $248.50, 60 DTE)

| Strategy | Cost | Protection | Annual Cost |
|----------|------|-----------|-------------|
| ATM Put (250 strike) | $850 (3.4%) | Full below $250 | ~20% |
| 5% OTM Put (236 strike) | $320 (1.3%) | Below $236 (5% deductible) | ~8% |
| Put Spread (250/220) | $570 (2.3%) | $250→$220 max; tail unhedged | ~14% |

**Hedge Cost Rule:**
- <2% annually: Sustainable
- 2–5%: Use selectively
- >5%: Prohibitive — cost exceeds expected return

### Delta Hedging

**When:** Net delta > ±50% NAV | Earnings on large position | Weekend before FOMC/election

**Frequency:**
- Daily: ~0.05%/rebalance (≥$500K portfolios)
- Weekly: ~0.02%/week ($100K–$500K)
- Threshold-based (delta drift >2% NAV): Most cost-effective

**Instruments:** Shares (cheapest) | Futures (capital-efficient) | Opposite options (introduces new Greeks)

---

## Phase 6: Correlation & Concentration — Full Detail

### Options-Specific Correlation

- Same underlying, multiple options → perfectly correlated
- Same expiration across tickers → gamma concentration event
- Sector correlation → triple exposure on sector moves
- Vol correlation → all vega moves together on VIX spikes

### Concentration Limits

| Type | Limit |
|------|-------|
| Single ticker (options notional + stock) | <10% NAV |
| Expiration week concentration | <30% of positions |
| Sector (equity + options notional) | <25% NAV |

### Crash Correlation

- Normal: SPY-QQQ r ≈ 0.85
- Crash: r → 0.95–1.0
- Every hedging analysis must include a correlation→1.0 scenario
- Crash VaR is 2–3× normal VaR

---

## Phase 7: Event Risk Assessment — Full Detail

### Event Types and Risk

| Event | Risk Mechanism | Action Threshold |
|-------|---------------|-----------------|
| Earnings (any ticker) | IV crush (vega) + gap (gamma) | >5% NAV → reduce 50% or hedge |
| FDA/Regulatory | Binary outcome; IV underprices | Any position >2% NAV → CLOSE |
| FOMC/Economic | Portfolio-wide delta+gamma | Cut delta 50%, close short gamma |
| Merger arbitrage | Deal-break binary risk | No short options through close dates |

### Event P&L Formula

```
Total Event P&L = delta_impact + gamma_impact + vega_impact + theta
- Delta impact: pos.delta × implied_move_dollars
- Gamma impact: gamma × (implied_move)² / 2
- Vega impact: vega × expected_IV_change (-30% to -50% of pre-event premium)
```

