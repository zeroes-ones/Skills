# Skew and Term Structure Arbitrage

## The Two Dimensions of the Volatility Surface

Options are priced across two key dimensions:
1. **Strike (skew):** How IV varies across strikes at a fixed expiration
2. **Term (term structure):** How IV varies across expirations at a fixed strike

Arbitrage opportunities arise when these dimensions misprice relative to each other, historical norms, or across correlated underlyings.

## Skew Arbitrage

### What is Skew?

Skew is the difference between OTM put IV and OTM call IV. For equities, puts trade at a premium because investors buy downside protection:

$$Skew = IV_{OTM\_Put} - IV_{ATM}$$

Normal SPX skew: OTM puts (25-delta) trade 3-5 vol points above ATM. OTM calls trade 1-2 vol points below ATM.

### Skew Arbitrage: Risk Reversal

**When put skew is abnormally steep:** (puts expensive relative to calls)
- Buy OTM call (cheap)
- Sell OTM put (expensive)
- Net: zero or small credit, delta-positive position
- Profit from skew normalization

**When put skew is abnormally flat:** (puts cheap relative to calls)
- Sell OTM call (expensive relative to puts)
- Buy OTM put (cheap)
- Net: zero or small credit, delta-negative position

### Skew Arbitrage: Put Spread vs Call Spread

Compare the credit of equivalent-delta put spreads and call spreads:

```python
def skew_arb_signal(underlying, dte=30):
    """Compare put spread credit vs call spread credit at equivalent deltas."""

    # OTM put spread (e.g., 0.25 delta short, 0.15 delta long)
    put_spread_credit = get_spread_credit(underlying, 'put', 0.25, 0.15, dte)

    # OTM call spread (same deltas)
    call_spread_credit = get_spread_credit(underlying, 'call', 0.25, 0.15, dte)

    skew_ratio = put_spread_credit / call_spread_credit

    # Normal range: 1.3-2.0 (puts get paid more)
    if skew_ratio > 2.5:
        return "sell_put_spread"  # Puts abnormally expensive
    elif skew_ratio < 1.1:
        return "sell_call_spread"  # Calls abnormally expensive relative to puts
    else:
        return "neutral"
```

### Skew Arbitrage: Butterfly

A butterfly captures the skew premium when the wings are asymmetrically priced:

- Unbalanced butterfly: wider on the put side (where IV is higher), narrower on the call side
- This creates a put-skew-harvesting butterfly that's long skew

## Term Structure Arbitrage

### What is Term Structure?

The relationship between near-term IV and longer-term IV. For VIX:
- **Contango:** Front month < Back months (normal, ~80% of the time)
- **Backwardation:** Front month > Back months (stress signal, ~20% of the time)

### Term Structure Arbitrage: Calendar Spread

**When term structure is steep (contango):**
- Buy back-month option (relatively cheap)
- Sell front-month option (relatively expensive)
- Profit from: time decay on the short + term structure flattening

**When term structure is flat/inverted (backwardation):**
- Buy front-month option (relatively expensive but may be justified by imminent move)
- Sell back-month option
- Higher risk: backwardation often precedes large moves

### VIX Futures Term Structure Arbitrage

The VIX futures curve is the most actively traded vol term structure:

```python
def vix_term_structure_signal(vix_spot, futures_curve):
    """Signal based on VIX futures term structure."""

    front_month = futures_curve[0]["price"]
    second_month = futures_curve[1]["price"]

    # Contango percentage
    contango_pct = (second_month - front_month) / front_month

    # Historical average contango: ~3-6% per month
    if contango_pct > 0.10:  # >10% contango — unusually steep
        return {
            "trade": "short_vix_futures_calendar",
            "structure": "sell front month, buy second month",
            "edge": "Term structure mean reversion (steep → normal)",
            "contango_pct": contango_pct,
        }
    elif contango_pct < -0.05:  # Backwardation > 5%
        return {
            "trade": "close_all_short_vol",
            "reason": "Severe backwardation — elevated crash risk",
        }

    return {"trade": "no_action"}
```

### VIX Futures Roll Yield

In contango, rolling short VIX futures forward generates positive roll yield:

```
Roll yield = (Front month - Second month) / Front month × (365 / days_between_expirations)

Example: Front = 15, Second = 16, 30 days between
Roll yield = (15 - 16) / 15 × (365 / 30) = -24% annualized negative for long holders
                                                    +24% annualized for short holders
```

This is why shorting VIX futures in contango has historically been profitable — but why it's catastrophically dangerous in backwardation (when the roll yield flips).

## Cross-Underlying Skew Arbitrage

### Pair Skew Trade

When two correlated underlyings have divergent skew profiles:

```python
def pair_skew_signal(ticker_a, ticker_b, correlation=0.85):
    """Identify skew divergence between correlated underlyings."""

    skew_a = compute_skew_metric(ticker_a)  # e.g., 25-delta put IV / ATM IV
    skew_b = compute_skew_metric(ticker_b)

    skew_spread = skew_a - skew_b
    historical_spread = get_historical_skew_spread(ticker_a, ticker_b)

    z_score = (skew_spread - historical_spread.mean()) / historical_spread.std()

    if abs(z_score) > 2.0:
        # Skew divergence is statistically significant
        if skew_a > skew_b + 2 * historical_spread.std():
            return {
                "trade": "short_skew_A_long_skew_B",
                "A": ticker_a, "B": ticker_b,
                "action": f"Sell puts on {ticker_a} (expensive skew), buy puts on {ticker_b} (cheap skew)",
                "z_score": z_score,
            }

    return {"trade": "no_action"}
```

## Risk Management for Skew/Term Structure Trades

### Skew Trade Risks

1. **Crash risk (short skew):** Selling expensive puts because skew is high is exactly when you're most likely to need those puts. Never be net short puts during:
   - VIX > 25
   - Market below 200SMA
   - Fed decision days
   - Geopolitical events

2. **Correlation break (pair skew):** Pairs that normally move together can diverge sharply during sector rotations or idiosyncratic events.

### Term Structure Risks

1. **Backwardation acceleration:** Shorting front-month vol when backwardation is building is like shorting into a hurricane. The front month can spike 50-100% in days.
2. **Roll cost:** If you're long VIX futures, you pay roll yield in contango (~5-10% per month). This is a slow bleed that erodes profits.

### Position Sizing

```python
MAX_SKEW_TRADE_SIZE = account_value * 0.03  # 3% max per skew trade
MAX_TERM_STRUCTURE_SIZE = account_value * 0.05  # 5% max per term structure trade
MAX_TOTAL_VOL_ARB = account_value * 0.20  # 20% max total vol arb allocation
```

## Summary

Skew and term structure arbitrage are more sophisticated than simple VRP harvesting. They require understanding the vol surface in two dimensions and trading relative value (not absolute level). The edge is smaller but more consistent than VRP — skew mispricings are less persistent than the overall VRP but more frequent. These are quants' strategies — data-intensive, model-driven, and execution-sensitive.
