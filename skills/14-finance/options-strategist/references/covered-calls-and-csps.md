# Covered Calls and Cash-Secured Puts (CSPs)

## Purpose
Operational guide to the Wheel Strategy — selling CSPs until assignment, then covered calls until shares are called away. Simple in structure, frequently misapplied in execution. These are the foundational income-generating options strategies.

---

## Cash-Secured Put (CSP) Mechanics

### Entry Parameters

| Parameter | Conservative | Moderate | Aggressive |
|-----------|-------------|----------|------------|
| Strike Delta | 0.15–0.20 | 0.20–0.30 | 0.30–0.40 |
| DTE | 30–45 | 21–35 | 7–14 |
| IV Rank Minimum | > 25 | > 20 | > 10 |
| Cash Reserve | Strike × 100 × Contracts | Same | Same |
| Max per Ticker | 5% of portfolio | 10% | 15% |

[VERIFIED] A single CSP at $50 strike requires $5,000 cash. On a $25,000 account, that's 20% — above all maximums. Size to limits, not premium targets.

### Strike Price Formula
```
Target Strike ≈ S × (1 - (z × σ × √(DTE/365)))
```
z-scores: 0.30 delta → 0.524, 0.20 delta → 0.842, 0.15 delta → 1.036.

Example: $100 stock, 30% IV, 30 DTE, 0.25 delta (z ≈ 0.674): Strike ≈ $94.20.

### Premium Targets
- 30–45 DTE: 1–2% of strike price per contract
- 21–30 DTE: 0.75–1.5% of strike price
- 7–14 DTE: 0.5–1% (higher annualized, elevated gamma risk)

### CSP Exit Rules

| Condition | Action |
|-----------|--------|
| Profit reaches 50% of max | Close early. Remaining 50% requires doubling gain with proportionally more risk. Redeploy capital. |
| Profit reaches 80% with > 14 DTE | Close. Remaining 20% isn't worth the theta left. |
| Stock drops to strike | Evaluate: still want to own? Let assign. Thesis broken? Close for loss. |
| Stock drops 5% below strike | Close immediately. Assignment means owning at 5% above market. |
| Stock drops 10%+ below strike in < 3 days | Close — crash, not a dip. Capital tie-up exceeds realistic premium recovery. |

---

## Covered Call Mechanics

### Entry Parameters (Post-CSP Assignment)

| Parameter | Conservative | Moderate | Aggressive |
|-----------|-------------|----------|------------|
| Strike Delta | 0.20–0.30 | 0.30–0.40 | 0.40–0.50 (ATM) |
| Strike vs Cost Basis | Above cost basis | At or above | At cost basis |
| DTE | 30–45 | 21–30 | 7–14 |
| Premium Target | 1–2% of cost basis | 1.5–3% | 3–5% |

### Critical Rule: Never Sell Below Cost Basis
Exception: if net proceeds (strike + premium) > cost basis, the round-trip is profitable. Example: Cost basis $100, sell $98 call for $3.00 → net = $101 → profitable despite below-cost strike. [COMMON-PRACTICE]

### Covered Call Exit and Roll Rules

| Condition | Action |
|-----------|--------|
| Stock ITM at expiration | Let assign — max profit achieved |
| Stock above strike, > 14 DTE | Roll up and out: buy back, sell higher strike further out for net credit ≥ $0.05 |
| Stock drops 5%+ below cost basis | Close call (buy back at profit). Wait for recovery before selling new call. |
| Profit on call reaches 80% | Close early. Sell new call at same or higher strike. |
| Ex-dividend near, call ITM | Close or roll past ex-div — high early assignment risk |

### Rolling Mechanics
```
Net Credit = New Call Premium - Cost to Buy Back Old Call
```
Roll only if net credit ≥ $0.05. Debit roll only if regret on old strike assignment exceeds debit cost.

---

## The Wheel Strategy Full Flow

```
1. Screen for fundamentally sound stocks → Rev growth > 0, EPS > 0, D/E < 1.5
2. Sell CSP at 0.20–0.30 delta, 30–45 DTE
   → Expires OTM: Keep premium, return to Step 2
   → Assigned: Own shares at (strike - premium received)
3. Sell covered call at or above cost basis, 0.20–0.30 delta, 30–45 DTE
   → Expires OTM: Keep premium + shares, repeat Step 3
   → Assigned: Sell shares. Total return = Σ(CSP + CC premiums) + (strike - cost basis)
   → Return to Step 1
```

### ROI Calculation
```
Annualized CSP = (Premium / Strike) × (365 / DTE)
Annualized CC  = (Premium / Cost Basis) × (365 / DTE)
Cycle Return   = (Total Premiums + Stock Gain) / (Capital × Days Held) × 365
```
Target 15–30% annualized in normal IV. Above 40% = unsustainable. Below 10% = underperforming buy-and-hold.

---

## When the Wheel Works vs Fails

| Works Best | Fails |
|-----------|-------|
| IV Rank 50+ (rich premium) | Strong bull market (capped upside > premium) |
| Sideways/range-bound market | Bear market/crash (assignment at inflated prices) |
| Slightly bullish | Earnings week (binary gap risk) |
| Strong fundamentals (want to own) | Low IV Rank < 20 (premium too thin) |
| Weekly options available | High-dividend near ex-date (early assignment) |
| Dividend-paying stocks | Value trap (stock cheap for a reason) |

---

## UOA Integration

| UOA Signal | Wheel Action |
|------------|-------------|
| Heavy put selling (bullish) | Confirms CSP entry |
| Heavy put buying (bearish) | AVOID CSP on this ticker |
| Call buying above ask (bullish) | CC: sell deeper OTM (0.10–0.15 delta) to avoid early assignment |
| Call selling (bearish) | CC: sell closer to ATM (0.35–0.40 delta) — upside is capped |
| Block trade > $500K | Extend DTE to 45–60 |

[INFERRED] Require 3+ UOA prints within 60 minutes before acting. The wheel is multi-week — single UOA prints are noise at this timeframe.

---

## Tax Considerations

| Scenario | Tax Treatment | Holding Period Impact |
|----------|--------------|----------------------|
| CSP expires OTM | Short-term capital gain | None |
| CSP assigned | Premium reduces cost basis | Holding period starts at assignment |
| Qualified CC (OTM, >30 DTE) | Standard | Does NOT reset share holding period |
| Unqualified CC (ITM or ≤30 DTE) | Standard | RESETS holding period — LT gains clock restarts |

[VERIFIED] Qualified CC = strike ≥ prior day's close AND > 30 DTE at entry. Consult IRS Pub 550 for deep-ITM exceptions.

---

## Risk Guardrails
- Max portfolio in wheel: 40% total
- Per-ticker: 10% max
- Sector diversification: ≤ 25% in any GICS sector
- Cash reserve: 10–15% minimum
- Post-assignment stop: sell shares if 10% below adjusted cost basis
- Max consecutive rolls: 2 per position
