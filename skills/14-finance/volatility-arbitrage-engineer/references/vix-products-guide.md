# VIX Products Guide

## The VIX Ecosystem

The CBOE Volatility Index (VIX) has spawned an entire ecosystem of tradeable products. Understanding what each instrument represents — and doesn't represent — is critical for vol arbitrage.

## VIX Cash (Spot) Index

**What it is:** A calculated index representing 30-day expected volatility of the S&P 500, derived from SPX option prices.

**Can you trade it?** NO. The VIX spot is not directly tradeable.

**What it's useful for:** Reference point. Regime detection. The "truth" that all VIX products converge toward (or diverge from).

**Calculation:** Weighted average of OTM SPX put and call prices across all strikes, interpolated to a constant 30-day maturity. Formula is public (CBOE white paper) but complex — 50+ options used in each calculation.

## VIX Futures

**What they are:** Exchange-traded futures on the VIX index. Cash-settled to a Special Opening Quotation (SOQ) of the VIX on expiration morning.

**Key characteristics:**
- Traded on CFE (CBOE Futures Exchange)
- Contract size: $1,000 × VIX (VIX at 20 = $20,000 notional)
- Minimum tick: 0.05 ($50 per contract)
- Monthly expirations + weekly expirations
- Trading hours: Nearly 24/5 (Sun 5pm – Fri 4:15pm CT)

**Term structure (contango vs backwardation):** VIX futures don't track VIX spot — they track expected VIX at expiration. This creates the futures curve that's in contango ~80% of the time.

```python
# VIX futures pricing
vix_future_price = vix_spot + expected_change_in_vix - convenience_yield

# In practice: futures are a bet on where VIX will be at expiration
# Not a bet on where VIX is now
```

**Who trades them:**
- Long: Hedgers buying crash protection, vol funds betting on spike
- Short: Vol sellers harvesting contango roll yield, yield enhancement

**Risk:** Contango roll yield bleeds longs. Backwardation roll yield bleeds shorts. VIX can spike 100%+ in days.

## VIX Options

**What they are:** Options on VIX futures (not on VIX spot). The underlying is the corresponding VIX future.

**Key characteristics:**
- Traded on CBOE
- European exercise (no early assignment)
- Cash-settled
- Underlying is the VIX future, not the VIX spot — this creates a "double derivative" structure

**Critical difference: VIX options vs equity options:**
- VIX is mean-reverting (equities are not)
- VIX has a hard floor (~9 historically) and theoretical ceiling
- VIX options have their own IV — "vol of vol" or "VVIX"
- VVIX typically trades 80-110 (VIX options IV is 80-110% of the VIX level)

**VVIX (VIX of VIX):** The implied volatility of VIX options. Key facts:
- VVIX > 100 is normal (vol of vol is high)
- VVIX spikes to 150-200+ during vol events
- VVIX < 80 is low and may signal complacency

## VIX ETNs and ETFs

**VIX ETNs (Exchange-Traded Notes):**
- Not funds — they're unsecured debt of the issuing bank
- Track VIX futures indices (usually a rolling basket of front and second-month futures)
- Carry credit risk of the issuer
- Examples: VXX (iPath), VIXY (ProShares), UVXY (1.5× leveraged, ProShares)

**VIX ETFs:**
- Actually hold VIX futures (unlike ETNs which are debt)
- Examples: VIXM (mid-term futures), SVOL (short VIX futures, ~0.2× leverage)

**The decay problem:** All long VIX products that roll futures decay in contango:
- VXX lost ~99.9% of its value since inception due to roll decay + reverse splits
- The average monthly roll cost in contango is 5-10%
- Annualized: 60-120% decay! (compensated by spikes, but timing must be perfect)

**Short VIX products (inverse):**
- SVXY (short VIX futures, 0.5× leverage, ProShares)
- SVIX (short VIX futures, 1×, but with active management to avoid blowup)
- These harvest the contango roll yield but can lose 90%+ in a vol spike

## Trading Strategies by Product

### VIX Futures Calendar Spread

```
Long VIX futures calendar: Buy Dec VIX future, sell Nov VIX future
→ Profit if VIX term structure steepens (back months rise relative to front)
→ Loss if VIX term structure flattens or inverts
```

### VIX Options: Straddle on VIX

```
Buy VIX call + put at same strike (on VIX future, not spot)
→ Profit if VIX moves more than the premium paid
→ VIX straddles are expensive (high VVIX). Need a BIG move
```

### VIX Options: Ratio Spread

```
Buy 1 VIX call at strike X, sell 2 VIX calls at strike X+10
→ Small credit. Profit if VIX moves to X+10 but not beyond
→ Loss if VIX surges through X+10 (short call goes deep ITM)
```

### Vol of Vol Relative Value

```
If VVIX is unusually LOW (< 80): Buy VIX straddles (vol of vol is cheap)
If VVIX is unusually HIGH (> 130): Sell VIX straddles (vol of vol is expensive)
```

## When Each Product Makes Sense

| Product | Best Use Case | Worst Use Case |
|---------|--------------|----------------|
| VIX Futures (long) | Short-term hedge against vol spike (days) | Long-term hold (roll decay kills returns) |
| VIX Futures (short) | Harvesting contango in calm markets | ANY vol spike event (tail risk is catastrophic) |
| VIX Options (long premium) | Vol of vol is cheap (VVIX < 80), expect near-term vol spike | Vol of vol is expensive (VVIX > 130) |
| VIX Options (short premium) | Vol of vol is expensive, calm market regime | Pre-FOMC, pre-elections, any event risk |
| VIX ETNs (long, e.g. VXX) | Short-term tactical hedge (hours to days max) | Multi-day hold. Roll decay is brutal |
| Inverse VIX (SVXY) | Calm bull market, harvesting roll yield | Any vol spike. Product can go to near-zero |

## The Golden Rule of VIX Products

**Never be long VIX products for more than a few days.** The roll decay is relentless. Unless you're (a) hedging a specific short-term event with a defined exit date, or (b) running a systematic short-VIX strategy with strict risk management, VIX products are wealth-destroying for buy-and-hold.

**Never be short VIX products without a kill switch.** The one vol spike you don't hedge or exit will cost more than years of roll yield harvesting. Every short-vol strategy must have:
1. Hard VIX level exit (e.g., VIX > 30: close 50%, VIX > 40: close all)
2. Hard drawdown exit (-15% on the position)
3. Non-negotiable execution of exits (no "waiting for it to come back")

## Summary

VIX products are powerful but dangerous. The key distinction is VIX spot vs VIX futures vs VIX options — three different instruments with three different pricing dynamics. Most retail traders lose money in VIX products because they don't understand contango decay (on the long side) or tail risk (on the short side). Trade them tactically, size them small, and exit fast.
