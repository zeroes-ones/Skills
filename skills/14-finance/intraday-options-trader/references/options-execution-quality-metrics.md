# Options Execution Quality Metrics

> **Portability target:** Spec-level. Vendor-agnostic metric definitions — implement in any execution framework.

## Why This Matters

For intraday options trading, execution quality IS the edge. If your fill is 5% worse than mid and your edge is 6%, you're making 1% — and after commissions, you're negative. Every intraday trader must measure and optimize execution.

## Core Metrics

| Metric | Formula | Intraday Target | Failing Threshold |
|--------|---------|----------------|------------------|
| Fill-to-Mid Spread | `(fill_price - mid_price) / mid_price` | < 2% for options | > 5% — edge consumed |
| Slippage | `execution_price - signal_price` | < $0.05/contract | > $0.15/contract |
| Fill Rate | `filled_orders / total_orders` | > 90% | < 70% — broker/routing problem |
| Time-to-Fill | `fill_timestamp - order_timestamp` | < 500ms | > 2s — price has moved |
| Price Improvement | `mid - fill` (for buys), `fill - mid` (for sells) | > $0.02 | Negative consistently — routing issue |
| Spread Capture | `(fill - bid) / (ask - bid)` for sells | > 45% | < 30% — always hitting bid |

## Dollar Impact

A single intraday options trader making 20 trades/day at 10 contracts each:

| Fill Quality | Per-Trade Cost | Daily Cost | Monthly Cost |
|-------------|---------------|-----------|-------------|
| Excellent (< 1% slippage) | $5 | $100 | $2,100 |
| Good (1-2% slippage) | $15 | $300 | $6,300 |
| Average (2-4% slippage) | $30 | $600 | $12,600 |
| Poor (4-8% slippage) | $60 | $1,200 | $25,200 |

**$25,200/year difference between poor and excellent execution.** That's more than most traders' annual P&L.

## Execution Routing

| Route Type | Latency | Fill Quality | Cost | Best For |
|-----------|---------|-------------|------|----------|
| DMA (Directed Market Access) | < 50ms | Best — hits exchange directly | Commission + exchange fees | Gamma scalping, ORB, momentum |
| Smart Router | 50-200ms | Good — routes to best exchange | Commission only | Most intraday trades |
| PFOF (Payment for Order Flow) | 100-500ms | Worst — internalized, delayed | Free | **Do not use for intraday options** |

## Measuring Your Execution

### Daily Review Checklist

- [ ] Record fill price vs. mid for every trade
- [ ] Compute fill-to-mid spread for each trade
- [ ] Flag trades where spread > 5% — these are execution failures, not trading failures
- [ ] Track time-to-fill — if consistently > 1s, check broker/routing
- [ ] Compute weekly average fill quality — should be improving or stable, never degrading

### Red Flags

- Fill-to-mid consistently > 5% → Wrong broker for intraday. Switch to DMA or at minimum a non-PFOF smart router.
- Time-to-fill > 2s consistently → Latency issue. Check internet connection, broker API, or routing configuration.
- Fill rate < 70% → Your limit prices are too aggressive or your broker's routing is rejecting.
- Negative price improvement on every trade → You're hitting bids/offers. Use limit orders inside the spread.

## Broker-Specific Notes

| Broker | Intraday Suitability | Notes |
|--------|---------------------|-------|
| IBKR Pro (DMA) | Excellent | Sub-50ms fills, exchange-native routing, no PFOF. Required for gamma scalping |
| tastyworks | Good | Smart router, reasonable fills, spread-friendly for multi-leg |
| TDA thinkorswim | Good | Good order routing, education-focused, fills acceptable for non-scalping |
| Tradier | Decent | API-first, suitable for automation, fills vary by underlying |
| Robinhood | Poor | PFOF routing, 100-300ms latency, wide spreads on options. Not suitable for intraday |
| Webull | Poor | PFOF routing, similar to Robinhood. Not suitable for intraday options |
