# Multi-Leg Execution Optimization

## The Problem

Multi-leg options orders (spreads, condors, butterflies) face unique execution challenges that single-leg orders don't: legging risk, exchange routing decisions, native vs. synthetic spread orders, and fill quality degradation with leg count.

## Exchange-Native Spread Orders

### Complex Order Book (COB)

Modern options exchanges (CBOE, ISE, PHLX, BOX, MIAX, BATS) support **complex order books** that allow multi-leg orders to execute as a unit.

**Advantages of COB:**
- **No legging risk:** All legs fill simultaneously or none fill. Guaranteed spread limit.
- **Price improvement:** COB auctions can discover prices between the individual-leg markets.
- **Fee caps:** Most exchanges cap the per-leg fee on complex orders (e.g., $1.50 total vs. $3.00 for 2 single-leg executions).
- **Priority:** Complex orders have dedicated market makers competing for the flow.

**Disadvantages:**
- **Lower fill probability:** Fewer contra-side participants in the COB.
- **Wider markets:** COB spread can be wider than sum of individual-leg spreads when liquidity is thin.
- **Not universal:** Some brokers route to single-leg only by default.

### When to Use Each

| Scenario | Route | Reason |
|----------|-------|--------|
| 2-leg spread, liquid underlyings | COB (native spread) | Fill quality, fee savings, no legging risk |
| 3-4 leg spread (condor, butterfly) | COB (native) | Legging risk compounds quadratically with leg count |
| Illiquid underlying, first-quoted leg | COB is unreliable; may need single-leg with caution | COB depth insufficient |
| Market order needed (rare!) | COB only. Never market-order single legs for a spread | Market single-leg = unbounded adverse selection on one side |
| Very large size (>100 contracts) | Start COB, monitor. Break to single-leg if no fill | Size may exceed COB depth |
| Index options (SPX, NDX) | COB default. Native support is excellent | SPX COB is deep and liquid |

### Legging Risk Quantification

**Legging risk** = probability that one or more legs fill before the remaining legs, leaving you with unhedged directional exposure.

For a 2-leg spread at mid-price:
- **Liquidity > 100 on both legs:** legging probability < 2%
- **Liquidity 50-100:** legging probability 5-10%
- **Liquidity < 50:** legging probability > 15%

Legging risk compounds with leg count:
- 3-leg position: ~3-4× 2-leg risk
- 4-leg position: ~6-8× 2-leg risk

**Never leg into a spread intentionally unless** you have identified an edge in the execution sequence (e.g., one leg is systematically mispriced vs the other). "Legging in to get a better price" is a common rationalization for gambling.

## Order Types for Multi-Leg

### Limit Orders (Default)

**Native spread limit:** "Buy SPY 450/455 call spread at $2.50 limit" → exchanges as a single unit. The spread fills if the net can be bought at ≤ $2.50.

**Single-leg limits (avoid):** "Buy 450 call at $8.00, sell 455 call at $5.50" → If the bid jumps after buying the 450 call, you're left with a naked position until you chase the 455 call at a higher price.

### Market Orders (Use Sparingly)

**Native spread market:** Accepts the best available spread price. Use ONLY for:
- Highly liquid underlyings (SPY, QQQ, IWM, AAPL)
- Urgent exits (circuit breaker triggered, must exit NOW)
- Position sizes < 10 contracts

**Never market-order individual legs** to create a spread position. This is how small losses become catastrophic.

### Midpoint Peg (Ideal for Swings)

**Midpoint pegged orders:** Continuously reprice to the midpoint of the spread market.

Best for:
- Swing entries where execution time is flexible (waiting hours is acceptable)
- Liquid underlyings where the mid is tightly quoted
- Avoiding the bid-ask crossing cost

### Stop Orders for Spreads

**Stop market on spread price:** When the net spread mark drops to X, trigger market order to close.

**Stop limit on spread price:** When net spread mark drops to X, place limit order at Y to close.

Caveats:
- Spread stops trigger on the **midpoint** of the spread, which can gap on wide markets
- During high-vol events, the spread price can jump through your stop limit without filling
- Always use at least a 10% buffer between stop trigger and limit price during high-vol periods

## Broker-Specific Routing

### Interactive Brokers (IBKR)

- **COB native support:** Excellent. Routes to ALL major options exchanges.
- **SmartRouting:** Automatically chooses between COB and legging based on fill probability.
- **Adaptive algo:** Midpoint peg with urgency parameter. Best for swing entries.
- **TWS settings:** Configure "Smart" routing for complex orders. Prefer "SMART" exchange.
- **API:** `ib_insync` → `order.LmtPrice`, `order.SmartRoutingParams`. Set `outsideRTH=True` for spread orders.

### TD Ameritrade / Schwab

- **Complex order support:** Good on thinkorswim. API support is limited.
- **thinkorswim:** Native spread orders with "NR" prefix. Use for manual execution.
- **API:** No native complex order support. Must be simulated by rapid sequential legs (risky).

### Alpaca

- **Options support:** Options trading available. **Complex order support is limited.**
- **Current state:** Single-leg options only via API. Spread execution requires multiple orders.
- **Recommendation:** Not suitable for automated multi-leg options trading until complex orders are supported.

### Tradier

- **Complex order support:** Native multileg endpoint. Good for spread trading.
- **API:** `POST /v1/accounts/{id}/orders/multileg`. Supports up to 4 legs.
- **Limitations:** Only 4 legs max. Limited exchange routing options.

### tastytrade (via API)

- **Complex order support:** Native. Built for multi-leg options.
- **API:** `POST /accounts/{id}/orders/dry-run` for preview. Dedicated complex order endpoint.
- **Advantage:** Schema designed for options first. Good institutional routing.

## Fill Quality Metrics

### What Good Looks Like

| Metric | Excellent | Acceptable | Unacceptable |
|--------|-----------|------------|--------------|
| Fill vs Mid (2-leg) | < 1% worse | 1-3% worse | > 3% worse |
| Fill vs Mid (4-leg) | < 2% worse | 2-5% worse | > 5% worse |
| Fill time (liquid) | < 30 seconds | 30s-2min | > 2 min |
| Partial fill rate | 0% | < 5% | > 5% |
| Slippage during vol events | < 5% | 5-15% | > 15% |

### Monitoring Fill Quality

```python
def assess_fill_quality(fill_price, bid, ask, legs, order_type):
    mid = (bid + ask) / 2
    fill_vs_mid = abs(fill_price - mid) / mid
    leg_multiplier = 1 + (legs - 2) * 0.5 if legs > 2 else 1
    adjusted_threshold = leg_multiplier * 0.02
    return {
        "fill_price": fill_price,
        "mid": mid,
        "fill_vs_mid_pct": fill_vs_mid * 100,
        "quality": "good" if fill_vs_mid < adjusted_threshold else (
                   "acceptable" if fill_vs_mid < adjusted_threshold * 2 else "poor"),
    }
```

## Execution Timing

### Best Times to Execute

- **9:35-10:30 AM ET:** Highest liquidity, narrowest spreads. Best for entries.
- **2:00-3:30 PM ET:** Second liquidity peak. Good for entries. Avoid exits (gamma risk).
- **11:00 AM-1:30 PM ET:** Lunch lull. Wider spreads. Avoid entries unless patient.
- **3:30-4:00 PM ET:** Gamma explosion zone. Exit existing positions. No new entries.

### Days to Execute

- **Tuesday-Thursday:** Best. Monday often has weekend gap adjustments. Friday has pre-weekend positioning.
- **Monthly OPEX (3rd Friday):** Massive volume. Execution is easy but pricing can be erratic near close.
- **Day before/after holidays:** Low volume. Wider spreads. Avoid.

### Execution in High Vol (VIX > 25)

- Double expected fill time
- Expect 2-3× wider effective spreads
- Reduce position size by 30% to account for exit slippage
- Always use native spread orders — legging risk is amplified in volatile markets

## Execution Error Handling

| Error | Meaning | Action |
|-------|---------|--------|
| "Order rejected: complex order not supported" | Broker/exchange doesn't support COB for this spread | Switch to manual legging WITH CAUTION |
| "No liquidity at this price level" | COB depth insufficient at your limit | Adjust limit to within 5% of mid. If still no fill, reconsider the trade |
| "Partial fill: 3 of 4 legs filled" | Legging occurred despite complex order | One leg's market moved. Close remaining leg or complete the spread at new price |
| "Order rejected: outside trading hours" | Trying to trade after close | Queue for next open. Check `outsideRTH` setting |
| "Margin requirement exceeds available" | Spread not recognized as defined risk by broker | Verify spread type. Some brokers treat diagonals/calendars as naked positions |

## Summary

- **Always use native spread orders** (COB) for 2+ leg positions
- **Set limits at mid or slightly better** — be patient for fills
- **Monitor fill quality** across all executions
- **Avoid legging into spreads** unless you've identified a specific execution edge
- **Account for leg count in fill expectations** — more legs = higher cost
- **Time your executions** to the 9:35-10:30 AM and 2:00-3:30 PM liquidity windows
