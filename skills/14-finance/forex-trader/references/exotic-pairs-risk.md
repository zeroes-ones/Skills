# Exotic Pairs Risk Management

## What Makes a Pair "Exotic"?

| Characteristic | Major | Minor | Exotic |
|---------------|-------|-------|--------|
| Daily volume | $100B+ | $10-100B | <$10B |
| Typical spread (best session) | <1 pip | 1-5 pips | 5-50+ pips |
| Liquidity gaps during news | Rare (<5 pips) | Occasional (5-20 pips) | Common (50-200+ pips) |
| Central bank intervention risk | Very low | Low | High (TRY, BRL, INR, IDR) |
| Capital controls risk | Zero | Zero | Significant (CNY, TRY, MYR) |
| Counterparty fills at quoted price | >99.9% | >99% | 90-95% (requotes common) |
| Swap costs | ~1-2% annualized | ~2-5% annualized | 5-50%+ annualized |

## Exotic Pair Specific Risks

### USD/TRY (Turkish Lira)
- **Capital controls:** Turkey has imposed restrictions on shorting TRY. Some brokers restrict TRY pairs.
- **Political risk:** Central bank governors can be fired for not cutting rates. Monetary policy is not independent.
- **Daily vol:** 1-3% ADR. 10%+ moves on political events.
- **Swap:** -40% to -50% annualized for long USD/TRY. This is NOT a misprint.
- **Trading rule:** Only trade with catalyst (election, crisis, extreme mispricing). Never just "trend follow" — the carry will eat you alive.

### USD/ZAR (South African Rand)
- **Commodity sensitivity:** ZAR moves with gold, platinum, and EM risk sentiment. Not just SA fundamentals.
- **Liquidity:** Decent during London hours. Thin during Asia and late NY.
- **ADR:** 1.0-2.0%. 3,000+ pips ATR (but pip value is tiny: ~$0.54/pip per standard lot at 18.50).
- **Political:** ANC politics, Eskom load-shedding, fiscal deficits. Each crisis can gap 2-5%.
- **Trading rule:** Size by ATR, not pips. A 500-pip stop on ZAR is tiny — that's only ~$270 per lot.

### USD/MXN (Mexican Peso)
- **US-Mexico spread:** MXN is sensitive to the rate differential with the Fed. Banxico often lags/mirrors Fed.
- **Liquidity:** Very liquid during NY hours. One of the most liquid EM currencies.
- **ADR:** 0.8-1.5%. Pip value is tiny (~$0.59/pip at 17.00). Standard lots are manageable.
- **Political:** US election risk, NAFTA/USMCA renegotiation, AMLO/Sheinbaum policy shifts.
- **Trading rule:** Trade during NY hours. MXN is a "mini-major" — not truly exotic in liquidity terms.

### USD/BRL (Brazilian Real)
- **Onshore vs offshore:** The offshore BRL (NDF) market is different from onshore. Spot BRL is restricted; most brokers offer NDFs or CFDs.
- **Capital controls:** Brazil restricts foreign exchange. Spot BRL may not be available at all brokers.
- **ADR:** 0.8-1.5%. Political drama drives sharp moves (Lula, Bolsonaro, fiscal fears).
- **Trading rule:** Verify it's deliverable BRL, not just CFD. Check swap costs — BRL rates are 10-14%, so carry is significant.

### USD/INR (Indian Rupee)
- **Intervention:** RBI actively manages INR. The pair is NOT free-floating. Expect sudden reversals near policy levels.
- **Liquidity:** INR is traded as NDF offshore. Spot INR requires onshore presence for most brokers.
- **ADR:** 0.2-0.5% — actively suppressed by RBI intervention. Low vol, but sudden breaks happen.
- **Trading rule:** INR is a managed currency. Breakout trading works poorly. Range trading within RBI's implicit band is the only viable approach.

## Exotic Pair Position Sizing

### The ATR Method
```
risk_per_lot = ATR(14) × pip_value × lot_size
max_lots = (account_equity × risk_percent) / risk_per_lot
```

Example: USD/ZAR at 18.50, ATR(14) = 3500 pips, pip value = $0.54, account = $50K, risk = 1%
```
risk_per_lot = 3500 × 0.54 = $1,890
max_lots = ($50,000 × 0.01) / $1,890 = 0.26 lots
```
→ Even though the pip value seems tiny, the ATR is so large that proper sizing means fractional lots.

### Exotic Pair Checklist

Before entry, verify ALL of:
- [ ] Broker offers this pair (not all do for TRY, BRL, INR)
- [ ] Broker allows the direction (some restrict short TRY)
- [ ] Swap rate verified from broker (not assumed from interest rates)
- [ ] Position sized by ATR, not by lot count
- [ ] Stop-loss gapped: assume -30% fill on market stops during news
- [ ] Only limit orders for entry (market = requote/slippage risk)
- [ ] No position held through local elections or central bank decisions
- [ ] Account can withstand a 5% overnight gap without margin call

## The 5% Overnight Gap Test

For ANY exotic pair position, compute:
```
gap_loss = notional × 0.05 × (1 if correct direction else -1)
margin_after_gap = equity - gap_loss
```

If `margin_after_gap < margin_requirement`, the position is oversized. Reduce.

