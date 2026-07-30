# Error Recovery — Fixed Income

## Error 1: Duration Type Confusion (Macaulay → Modified → DV01)

**Pattern:** Trader says "Bond has 8.2 year duration, hedge with 82 contracts of ZN." But 8.2 is Macaulay. At 5% YTM, modified = 7.81. DV01 = $781 per $100K. ZN DV01 = $79. Hedge = 781/79 = 9.9 contracts, not 82.

**Immediate:** Recompute with correct duration type. DV01 is always in dollars, never years.

**Prevention:** Build a function: `DV01(price, macaulay, ytm, freq, notional)` → dollar DV01. Never manually convert. Automate.

## Error 2: CTD Switch During Hedge Holding Period

**Pattern:** Portfolio hedged with ZN futures. Yields rally below 6% → CTD switches from high-coupon to low-coupon bond. Futures DV01 changes 12%. Hedge ratio was 565 contracts, should be 500.

**Immediate:** Check CME daily bulletin for current CTD and CF. Recompute futures DV01. Adjust position.

**Prevention:** Monitor CTD weekly. Set alert for yield level where CTD might switch (near 6% ± 50bp). Pre-compute hedge ratio for both potential CTDs.

## Error 3: Special Repo Bleeding Short Carry

**Pattern:** Flattener trade: short 10yr on-the-run. Bond goes 200bp special → borrow cost = GC - 200bp. Daily carry goes from -$50 to -$250. Trader thought carry was manageable; actual is 5× worse.

**Immediate:** Check specific CUSIP repo rate. If special > 100bp, find off-the-run alternative with similar duration that's NOT on special.

**Prevention:** Pre-trade: check repo market for the specific bond. Special spreads > 50bp → find alternative. Off-the-runs almost never go special.

## Error 4: Credit P&L Attribution Confusion

**Pattern:** "My corporate bond position made +$50K this month — the credit call was right!" Decompose: rates rallied 50bp → +$65K from duration. Spreads widened +15bp → -$15K from credit. Net +$50K, but credit call was WRONG. Next month rates don't rally → -$15K loss.

**Immediate:** Decompose P&L: ΔP = (-Duration × ΔTreasury) + (-Spread_Duration × ΔSpread). Always attribute to rate and spread separately.

**Prevention:** Track rate P&L and spread P&L as separate P&L lines. If you can't separate them, you don't know which bet made you money.

## Error 5: TIPS Liquidity Premium Spikes During Risk-Off

**Pattern:** TIPS position bought at breakeven 2.20%. Market sell-off: nominals rally (yields drop 50bp), TIPS rally less (yields drop 30bp). Breakeven WIDENS to 2.40%. Trader expected breakeven to hold steady. Loss: 20bp × duration ≈ -1.6%.

**Root Cause:** TIPS liquidity premium spiked from -30bp to -50bp during sell-off. The breakeven move was entirely liquidity, not inflation expectations.

**Immediate:** Decompose breakeven change: ΔBE = ΔInflation_Expectation + ΔInflation_Risk_Premium - ΔTIPS_Liquidity_Premium. A 20bp BE widening with 0bp inflation expectation change = pure liquidity.

**Prevention:** Never hold TIPS unhedged through risk-off events. The liquidity premium spike is predictable. Hedge TIPS with nominal shorts (duration-weighted) or accept the liquidity beta.

