# Volatility Regime Detection

## Why Regime Matters

All volatility strategies are regime-dependent. Shorting vol in a low-vol regime is steady income. Shorting vol in a high-vol regime is catastrophe. Buying vol in a low-vol regime is slow bleed from theta. Buying vol in a high-vol regime may have already missed the spike.

**The #1 edge in volatility trading is knowing which regime you're in.**

## The Three Volatility Regimes

### Regime 1: Low Vol / Complacency

| Metric | Threshold |
|--------|-----------|
| VIX | < 15 |
| VIX percentile (1-year) | < 25th |
| VIX term structure | Steep contango (> 5% front to second) |
| Realized vol (SPX 20-day) | < 10% annualized |
| VVIX | < 80 |

**What works:** Selling premium, harvesting VRP, harvesting contango roll yield
**What doesn't:** Buying premium (theta bleed), long vol strategies (no movement to monetize)
**Risk:** Black swan event. Puts are cheap — buy tail hedges
**Sizing:** Full size on short-vol strategies but MUST have crash hedges in place

### Regime 2: Normal Vol

| Metric | Threshold |
|--------|-----------|
| VIX | 15-22 |
| VIX percentile (1-year) | 25th-75th |
| VIX term structure | Mild contango (1-5%) |
| Realized vol (SPX 20-day) | 10-18% annualized |
| VVIX | 80-110 |

**What works:** Everything (if sized correctly). Credit spreads, iron condors, strangles, calendar spreads
**What doesn't:** Nothing is structurally broken, but nothing is on sale either
**Risk:** Standard. Use normal position sizing
**Sizing:** Standard allocation. Normal Kelly sizing

### Regime 3: High Vol / Stress

| Metric | Threshold |
|--------|-----------|
| VIX | > 25 |
| VIX percentile (1-year) | > 75th |
| VIX term structure | Flat or backwardation |
| Realized vol (SPX 20-day) | > 25% annualized |
| VVIX | > 120 |

**What works:** Buying premium (expensive but may be justified), defined-risk credit spreads (wide wings), long vol strategies
**What doesn't:** Short naked vol. Short strangles. Anything with undefined risk
**Risk:** Further vol expansion, gap moves, correlation → 1.0
**Sizing:** 0-50% of normal size. Close existing short vol immediately

## Regime Detection Algorithm

```python
def detect_vol_regime(vix_spot, vix_futures, spy_realized_vol, vvix):
    """Multi-factor volatility regime classification."""

    # VIX percentile (1-year lookback)
    vix_percentile = compute_percentile(vix_spot, lookback=252)

    # Term structure signal
    front_month = vix_futures[0]
    second_month = vix_futures[1]
    term_structure_pct = (second_month - front_month) / front_month

    # Score each factor
    score = 0

    # VIX level (0-3)
    if vix_spot < 15: score += 0
    elif vix_spot < 22: score += 1
    else: score += 2

    # VIX percentile (0-3)
    if vix_percentile < 25: score += 0
    elif vix_percentile < 75: score += 1
    else: score += 2

    # Term structure (0-3)
    if term_structure_pct > 0.05: score += 0  # Steep contango
    elif term_structure_pct > -0.02: score += 1  # Mild/flat
    else: score += 2  # Backwardation

    # Realized vol (0-2)
    if spy_realized_vol < 0.12: score += 0
    elif spy_realized_vol < 0.25: score += 1
    else: score += 2

    # VVIX (0-2)
    if vvix < 80: score += 0
    elif vvix < 120: score += 1
    else: score += 2

    # Classify
    if score <= 3:
        regime = "low_vol"
        sizing_mult = 1.0
    elif score <= 7:
        regime = "normal"
        sizing_mult = 0.8
    else:
        regime = "high_vol"
        sizing_mult = 0.4

    return {
        "regime": regime,
        "score": score,
        "sizing_multiplier": sizing_mult,
        "components": {
            "vix_level": vix_spot,
            "vix_percentile": vix_percentile,
            "term_structure": term_structure_pct,
            "realized_vol": spy_realized_vol,
            "vvix": vvix,
        }
    }
```

## Regime Transition Detection

Regime transitions are where money is made and lost:

### Low → Normal Transition
- VIX rises to 15-18 from < 13
- Term structure flattens slightly
- **Action:** Begin reducing short-vol positions. Don't panic — just trim.

### Normal → High Transition (THE DANGER ZONE)
- VIX rises above 22 rapidly (3+ point move in 1-2 days)
- Term structure inverts (backwardation)
- VVIX spikes above 120
- **Action:** CLOSE ALL SHORT VOL IMMEDIATELY. Do not wait. Do not hope. Do not "give it another day."

### High → Normal Transition
- VIX drops below 22 for 5+ consecutive days
- Term structure returns to contango
- VVIX drops below 110
- **Action:** Begin scaling into short-vol strategies at 25% size. Ramp to 50% after 2 weeks, full size after 1 month of normal regime.

### Normal → Low Transition
- VIX drops below 15 for 10+ consecutive days
- **Action:** Full size on short-vol strategies. But BUY TAIL HEDGES. Cheap puts are the insurance premium you pay for harvesting vol in complacency.

## Regime-Based Strategy Matrix

| Strategy | Low Vol | Normal | High Vol |
|----------|---------|--------|----------|
| Short strangles/straddles | ✅ Full | ⚠️ Half | ❌ CLOSED |
| Credit spreads (0.25Δ) | ✅ | ✅ | ⚠️ Wide wings only |
| Iron condors | ✅ | ✅ | ⚠️ Wider, fewer |
| Calendar spreads | ⚠️ Limited | ✅ | ✅ Best use |
| Debit spreads | ❌ | ⚠️ | ✅ Buy when expensive |
| Long straddles/strangles | ❌ | ⚠️ | ✅ Vol may keep expanding |
| VRP harvesting | ✅ | ✅ | ❌ CLOSED |
| Dispersion (short) | ✅ | ⚠️ | ❌ |
| Dispersion (long) | ❌ | ❌ | ⚠️ Risky but edge exists |
| VIX futures (long) | ❌ | ❌ | ⚠️ Short-term only |
| VIX futures (short) | ✅ | ⚠️ | ❌ NEVER |

## The Single Most Important Rule

**When the VIX term structure inverts (backwardation), close every short-vol position within 24 hours. No exceptions.**

Backwardation means the market is pricing higher uncertainty NOW than in the future. This is the single most reliable signal of near-term stress. Every major vol event (2008, 2011, 2015 Aug, 2018 Feb, 2020 Mar) was preceded by or coincided with VIX term structure inversion.

## Summary

Volatility regime detection is not academic — it's the difference between a profitable vol arb operation and a blow-up. The metrics are simple (VIX, VIX percentile, term structure, realized vol, VVIX). The challenge is acting on them without hesitation when regime transitions occur. Build regime detection into your automation, not your intuition.
