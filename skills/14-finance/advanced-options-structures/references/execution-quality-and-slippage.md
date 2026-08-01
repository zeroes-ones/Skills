# Execution Quality & Slippage for Advanced Multi-Leg Structures

> **Portability target:** Spec-level. Execution concepts are universal — adapt to any broker's order routing.

## The Multi-Leg Spread Problem

A 2-leg spread has 1 bid-ask crossing. A 6-leg Christmas tree has 6 bid-ask crossings. The spread cost is multiplicative, not additive — and mid-price modeling systematically understates it.

## Spread Cost by Leg Count

| Leg Count | Typical Structure | Mid-to-Fill Cost | Notes |
|-----------|------------------|-----------------|-------|
| 1 | Single option | 1-3% | Baseline spread cost |
| 2 | Vertical spread | 2-5% | Exchange-native spread orders hide 1 crossing |
| 3 | Butterfly, zebra | 3-8% | 3 crossings — real cost 3× single-leg |
| 4 | Iron condor, double diagonal | 4-10% | Can be 10%+ if any leg is illiquid |
| 5+ | Christmas tree, iron albatross | 6-15% | Each additional leg widens the total spread |

**Rule of thumb:** Each leg beyond 2 adds ~2% to total spread cost. A 5-leg structure at mid-price showing +8% profit likely has +2% to -3% at real fills.

## Modeling: Mid vs. Real Fills

```python
# WRONG — what most traders do:
pnl_at_entry = sum(mid_price[leg] * contracts * multiplier for leg in legs)
# This shows +3% profit. It's fantasy.

# CORRECT — what professional traders do:
pnl_at_entry = sum(
    (ask_price[leg] if leg.side == 'buy' else bid_price[leg])
    * contracts * multiplier
    for leg in legs
)
# This shows -2% loss. This is reality.
```

**R6 from the skill:** If the trade doesn't work at bid/ask, it doesn't work. Period.

## Exchange-Native Spread Orders: The Only Way

| Execution Method | Fill Quality | Legging Risk | Recommendation |
|-----------------|-------------|-------------|----------------|
| Exchange-native spread | Best — exchange guarantees all-or-none | Zero — all legs fill together or none | **Required for all multi-leg structures** |
| Leegged manually, one at a time | Potentially better on individual legs | EXTREME — market can move between legs | **DO NOT DO THIS (R1)** |
| Smart router (broker aggregates) | Good — broker attempts to fill as package | Low — broker manages execution | Acceptable for liquid 2-3 leg spreads |

## Liquidity Requirements by Structure

| Structure Type | Minimum OI per Leg | Minimum Volume per Leg | Max Spread per Leg |
|---------------|-------------------|----------------------|-------------------|
| Standard vertical, calendar | 100 | 20 | 10% |
| Butterfly, iron condor | 300 | 50 | 8% |
| Double diagonal, zebra | 500 | 50 | 6% |
| Christmas tree, seagull | 500 | 100 | 5% |
| Box spread | 1,000+ (SPX only) | 200+ | 2% |

Structures with 5+ legs: Even one illiquid strike makes the entire position unexitable. The exit is only as good as the worst leg.

## Broker Execution Comparison for Multi-Leg

| Broker | Multi-Leg Native Support | Fill Quality | Maximum Legs |
|--------|------------------------|-------------|-------------|
| IBKR | Full exchange-native spread support | Best | 8 legs in TWS, unlimited via API |
| tastyworks | Built for spreads — native multi-leg entry | Good | 4 legs |
| TDA thinkorswim | Good spread support | Good | 4 legs standard, more via custom |
| Tradier | API supports multi-leg | Varies | 4 legs |
| Robinhood | Basic multi-leg (Level 2 only) | Poor | 2 legs max for options |

## Dollar Impact Example

Christmas tree spread (6 legs), 10 contracts:

| Model | Per-Contract | 10 Contracts |
|-------|-------------|-------------|
| Mid-price model | +$350 profit | +$3,500 |
| Bid/ask realistic fill | +$50 profit | +$500 |
| Illiquid leg (1 strike with OI = 80) | -$200 loss | -$2,000 |

**The difference between "profitable strategy" and "losing strategy" is execution quality.** Don't model mid-prices. Don't trade illiquid strikes. Don't leg in.
