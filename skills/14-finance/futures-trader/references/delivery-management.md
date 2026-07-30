# Delivery Management

> Physical delivery: FND/LTD calendars, broker auto-liquidation policies, delivery assignment mechanics.

## Cash-Settled vs Physical Delivery

| Settlement Type | What Happens at Expiration | Examples | Risk |
|----------------|---------------------------|----------|------|
| Cash-Settled | Position marked to final settlement price. Cash credited/debited. No delivery. | ES, NQ, YM, RTY, VX | None. Auto-settles. |
| Physical Delivery | Long must take delivery. Short must make delivery. Actual commodity/security changes hands. | CL, NG, GC, ZC, ZS, ZW, ZB, 6E | HIGH if not managed. Brokers auto-liquidate. |

## Key Dates

### First Notice Day (FND)
The first day the exchange can assign delivery notices. LONG positions may receive a delivery notice starting on FND.

### Last Trading Day (LTD)
The final day the contract trades. After LTD, open positions enter the delivery process.

## Physical Delivery Contracts — Exit Timeline

```
FND - 14 days: NORMAL. No action required.
FND - 10 days: MONITOR. Plan exit strategy (roll or close).
FND - 7 days: ACT. Begin executing exit plan.
FND - 5 days: URGENT. Position must be closed or rolled within 3 trading days.
FND - 3 days: CRITICAL. Some brokers begin auto-liquidation. Close immediately.
FND - 1 day: DANGER. Position may be flagged. Broker likely liquidating.
FND: DELIVERY NOTICE RISK ACTIVE. Position should be ZERO.
PAST FND: BROKER AUTO-LIQUIDATION IN PROGRESS. You have lost control of exit.
```

## Broker Auto-Liquidation Policies

| Broker | Long Futures Liquidation | Short Futures Liquidation | Policy Source |
|--------|------------------------|--------------------------|---------------|
| Interactive Brokers | FND - 2 to 3 business days | FND - 1 to 2 business days | IBKR Futures Delivery Notice |
| Schwab (thinkorswim) | FND - 3 business days (margin call + liquidation) | FND - 3 business days | Schwab Futures Agreement |
| Alpaca | Futures not supported (2026-07) | N/A | N/A |
| Robinhood | Does not offer futures | N/A | N/A |

**These are guidelines, not guarantees.** Brokers may liquidate earlier during volatile markets or if margin is tight. NEVER rely on broker warnings as your risk management.

## What Happens If You DON'T Exit

### Long Physical Delivery Position at Expiration

1. Exchange assigns delivery notice to long position holder
2. Long must pay the full contract value (not just margin)
3. For CL (1,000 barrels at $75): $75,000 payment due
4. For GC (100 oz at $3,100): $310,000 payment due
5. Physical commodity is delivered to an approved warehouse/depository
6. Storage, insurance, and transportation are the long's responsibility

### What the Broker Does

Retail brokers DO NOT facilitate physical delivery. They will:
1. Send margin call for full contract value (if you haven't exited)
2. Auto-liquidate your position at market (you lose control of price)
3. Charge liquidation fees (typically $50-250 per contract)
4. Potentially restrict your account from trading futures

**You will never actually take delivery of 1,000 barrels of oil.** The broker will liquidate you first — at whatever price the market offers.

## Delivery Month Codes

| Month | Code | Month | Code |
|-------|------|-------|------|
| January | F | July | N |
| February | G | August | Q |
| March | H | September | U |
| April | J | October | V |
| May | K | November | X |
| June | M | December | Z |

## Section 1256 Tax Treatment

Futures (both cash-settled and physical delivery) are Section 1256 contracts:
- 60% taxed as long-term capital gains (max 20%)
- 40% taxed as short-term capital gains (ordinary income rate)
- Mark-to-market at year-end: unrealized gains/losses treated as realized on Dec 31
- Wash sale rules DO NOT apply to Section 1256 contracts
- Reported on Form 6781

## Delivery Management Checklist

- [ ] All physical-delivery contract FND dates in calendar
- [ ] All positions have exit plans before FND-7
- [ ] Roll strategies use calendar spread orders (not two outrights)
- [ ] Broker auto-liquidation dates confirmed for each broker
- [ ] Cash-seamled contracts marked (no delivery risk)
- [ ] FND within 5 days: position is ZERO
- [ ] No open positions in expiring contract after LTD

