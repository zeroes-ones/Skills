# Global Rates Linkages

## FX-Hedged Yield Computation

Comparing bond yields across currencies requires FX-hedging to isolate the pure yield pick-up.

### Formula
```
Hedged Yield = Foreign Bond Yield + (Foreign Short Rate - Domestic Short Rate)
```

The FX forward points embed the short-rate differential. Buying a foreign bond and selling the FX forward locks in the rate differential.

### Example: US Investor Buying German Bund
```
10yr Bund yield: 2.50%
EUR 3-month rate: 3.50%
USD 3-month rate: 5.25%

Hedged Yield = 2.50% + (3.50% - 5.25%) = 2.50% - 1.75% = 0.75%
```

The Bund yields 2.50% but after hedging EUR back to USD, the net return is 0.75% — less than the 4.00% available on US 10yr Treasuries. The Bund is NOT attractive on a hedged basis.

### Why This Works
```
1. Buy €100 of Bund → earn 2.50% in EUR
2. Sell €100 forward (hedge principal back to USD) → you receive USD at the forward rate
3. The forward rate embeds: F = S × (1 + r_USD) / (1 + r_EUR) — covered interest parity
4. Your total USD return = Bund yield + (EUR rate - USD rate) = hedged yield
```

## Cross-Currency Basis

In practice, FX forwards don't perfectly follow covered interest parity — there's a "cross-currency basis."

```
Cross-Currency Basis = Actual FX Forward Points - CIP-Implied Forward Points
```

A negative basis means USD is in demand — it costs MORE to borrow USD through FX swaps than CIP suggests. This has been persistent since 2008 (post-GFC) and reflects structural demand for USD funding.

### Basis Impact on Hedged Yields
```
True Hedged Yield = Foreign Yield + (Foreign Rate - Domestic Rate) + Basis_Adjustment
```

| Basis | Impact | Signal |
|-------|--------|--------|
| EUR/USD basis -20bp | EUR-based investor earns +20bp hedging USD bonds | USD funding premium |
| JPY/USD basis -40bp | JPY-based investor earns +40bp hedging USD bonds | Strong USD demand from Japan |
| GBP/USD basis -10bp | GBP-based investor earns +10bp | Mild USD demand |

## Global FI Relative Value Matrix

| Country | 10yr Yield | Short Rate | FX-Hedged Yield (USD) | US 10yr | Pick-Up | Decision |
|---------|-----------|------------|----------------------|---------|---------|----------|
| US | 4.00% | 5.25% | 4.00% (base) | 4.00% | — | Baseline |
| Germany | 2.50% | 3.50% | 0.75% | 4.00% | -3.25% | ❌ Negative pick-up |
| UK | 4.25% | 5.00% | 4.50% | 4.00% | +0.50% | ⚠️ Small pick-up vs higher vol |
| Japan | 0.75% | 0.25% | 5.75% | 4.00% | +1.75% | ✓ Attractive but JGB low liquidity |
| Australia | 4.50% | 4.35% | 3.60% | 4.00% | -0.40% | ❌ Slight negative |
| Canada | 3.75% | 4.75% | 3.25% | 4.00% | -0.75% | ❌ Negative pick-up |
| Italy | 4.25% | 3.50% | 2.50% | 4.00% | -1.50% | ❌ Sovereign risk + negative carry |

**Formula for each row:** Hedged = Local_Yield + (Local_Short_Rate - 5.25%). Pick-Up = Hedged - 4.00%.

## Central Bank Divergence Trades

When two central banks are on different policy paths, the rate differential changes → the FX forward points change → hedged yields change.

| Scenario | Trade |
|----------|-------|
| ECB cutting, Fed on hold → EUR short rates falling relative to USD | Long EUR bonds hedged to USD becomes MORE attractive (hedging cost drops) |
| BoJ hiking, Fed cutting → JPY short rates rising relative to USD | Japanese investors unwind USD bond positions (hedging pick-up shrinks) |
| BoE cutting faster than ECB → GBP hedged costs dropping | UK bonds attractive to EUR-based investors on hedged basis |

## Duration Matching Across Currencies

When building a global FI portfolio:
1. Compute DV01 in PORTFOLIO BASE CURRENCY for each position (DV01 × FX rate)
2. Sum cross-currency DV01s — this is the portfolio's total rate sensitivity
3. Hedge residual FX exposure if duration view is separate from currency view
4. Monitor cross-currency basis — basis moves change hedged yields by 10-30bp

