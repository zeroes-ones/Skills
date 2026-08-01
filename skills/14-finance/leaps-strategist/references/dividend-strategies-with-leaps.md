# Dividend Strategies with LEAPS — Deep Reference

> **Reading time:** 10 min | **Prerequisites:** options-strategist (covered calls), leaps-strategist (stock replacement, PMCC)

## The Dividend Gap Problem

[VERIFIED] Options holders do NOT receive dividends. When you replace 100 shares with a LEAPS call, you lose all dividend payments over the holding period. For a 2-year LEAPS on a 2% yielding stock, that's ~4% of notional value lost to missed dividends.

This reference covers how to quantify, mitigate, and in some cases profit from the dividend-options relationship.

## Quantifying the Dividend Cost

```
Annual dividend cost of LEAPS vs. shares = stock_price × dividend_yield × 100

Example: SPY @ $500, yield 1.3%
  Annual dividend lost: $500 × 1.3% × 100 = $650/year
  18-month LEAPS hold: ~$975 in missed dividends
```

### Incorporating Dividends into LEAPS Cost-Benefit

```
LEAPS total cost of ownership = premium_paid + missed_dividends - interest_on_saved_capital

SPY LEAPS 400 Call (18-month), $500 stock, $13,000 premium:
  Missed dividends: ~$975
  Interest earned on saved capital ($37,000 at 5%): +$2,775
  Net benefit vs. stock: $2,775 - $975 = +$1,800

SPY LEAPS 450 Call (18-month), $500 stock, $7,500 premium:
  Missed dividends: ~$975
  Interest earned on saved capital ($42,500 at 5%): +$3,188
  Net benefit vs. stock: $3,188 - $975 = +$2,213
```

[COMPUTED] For high-dividend stocks (>4% yield), the dividend gap can eliminate the LEAPS advantage. For low-yield growth stocks, the capital efficiency benefit dominates.

## Strategy 1: PMCC for Dividend Offset

The PMCC can partially offset dividend loss through premium collection:

```
PMCC on SPY, 12 monthly cycles:
  Monthly premium collected: ~1.2% of LEAPS cost = $156/month
  Annual premium: ~$1,872
  Annual missed dividends: ~$650

  Net: $1,872 - $650 = +$1,222/year from premium (beyond dividend offset)
```

[COMMON-PRACTICE] Targeting monthly premium ≥ 1.2% of LEAPS cost fully offsets the dividend gap on a 1.3% yielding underlying. For higher-yield stocks, target higher monthly premium or accept the net cost.

## Strategy 2: LEAPS on Low-Dividend / No-Dividend Stocks

The LEAPS dividend gap is minimal or zero for:
- Growth stocks with no dividend (AMZN, GOOGL, META, TSLA)
- Low-dividend tech (AAPL ~0.5%, NVDA ~0.03%)
- ETFs with below-market yields

For these underlyings, the LEAPS stock replacement math is cleaner — no dividend adjustment needed.

## Strategy 3: Synthetic Dividend Capture

### The Ex-Dividend LEAPS Roll

[COMMON-PRACTICE] Some traders attempt to capture dividends synthetically:

```
1. Buy LEAPS call before ex-dividend date
2. Stock pays dividend → stock drops by dividend amount
3. LEAPS call drops by (delta × dividend amount) ≈ slightly less than dividend
4. Net: You don't capture the dividend, and the LEAPS call loses some value
```

**Reality:** This does NOT work. The option market prices in expected dividends. The call price already reflects the present value of expected dividends over the option's life.

### What Does Work: Pre-Ex-Div Short Call Closing

[VERIFIED] If you have a PMCC with a short call that is ITM before ex-dividend:
```
1. Close (buy back) the short call before the ex-dividend date
2. Short call holders exercise ITM calls before ex-div to capture the dividend
3. Avoid assignment by closing the short call
4. Re-sell a new short call after the ex-dividend date (at a lower strike, since stock dropped)
```

This prevents forced exercise of your LEAPS (which would lose remaining time premium).

## Strategy 4: LEAPS Puts on High-Dividend Stocks

[COMPUTED] High-dividend stocks have elevated put premiums because:
1. Stock price is expected to decline by the dividend amount on ex-div dates
2. Put options price this in — puts are more expensive relative to calls
3. This creates a put-call parity imbalance

For a high-dividend stock (5% yield):
```
Put-Call Parity with dividends: C + K×e^(-rT) = P + S - PV(dividends)

For S=$100, K=$100, T=1yr, r=5%, div=$5:
  C + $95.12 = P + $100 - $4.88
  C + $95.12 = P + $95.12
  C = P

Without dividends: C + $95.12 = P + $100
  C = P + $4.88 (calls more expensive than puts)

With 5% dividend: C = P (puts are equally expensive as calls due to dividend pricing)
```

**Implication:** On high-dividend stocks, puts are relatively expensive → selling LEAPS puts (cash-secured) can be more attractive than buying LEAPS calls.

## Strategy 5: LEAPS on Dividend Aristocrats — The Covered LEAPS Put

```
Instead of: Buy 100 shares of KO ($6,000) + wait for dividends
Alternative: Sell 1 LEAPS Put (DITM, Δ=-0.80, DTE 540) on KO

Result:
- Receive LEAPS put premium (benefits from elevated put pricing on high-div stocks)
- If KO stays above strike: keep premium. No dividends received, but premium compensates
- If KO drops below strike: assigned shares at the strike (which you wanted anyway)
- The put premium is partially funded by the dividend expectation priced into puts
```

[COMMON-PRACTICE] For dividend stocks you want to own, selling DITM LEAPS puts can be more capital-efficient than buying shares directly AND collecting dividends — because the put premium already prices in expected dividends.

## Dividend Risk: The Short Call Assignment Trap

[VERIFIED] Short call holders have the right (not obligation) to exercise before ex-dividend. Rational call holders exercise ITM calls the day before ex-dividend if:
```
dividend > (strike - stock_price) + remaining_time_value
```

For PMCC traders, this means:

| Short Call Status | Ex-Div Date Within DTE? | Risk | Action |
|-------------------|------------------------|------|--------|
| OTM (>2% OTM) | Yes | Very low | Monitor. Roll if delta increases |
| ATM (±2%) | Yes | Moderate | Close short call before ex-div. Re-enter after |
| ITM | Yes | **HIGH** | Close short call immediately. Assignment is near-certain |

### The CCL LEAPS Dividend Example

[BACKTEST-EVIDENCE] From the Trading project: CCL ($28 strike call, Aug 21 expiry). CCL does not currently pay a dividend (suspended since 2020), so dividend risk is zero. But if CCL reinstates its dividend, the $28 call (currently at the money) becomes an assignment target.

## Common Mistakes

| ❌ Mistake | ✅ Correct |
|-----------|-----------|
| Ignoring dividends in LEAPS cost-benefit ("dividends are small") | Over 2 years, 2% yield = 4% of notional. On $50K that's $2,000 — significant relative to LEAPS extrinsic cost |
| Assuming you can capture dividends through LEAPS timing | Option prices fully reflect expected dividends. There is no arbitrage |
| Forgetting to check dividend calendar for PMCC short calls | Check ex-div dates before every short call sale. If ex-div within DTE and short call could go ITM → pick a higher strike or shorter DTE |
| Buying LEAPS calls on 5%+ yielding stocks → massive dividend gap | For high-yield stocks (VZ, T, MO), LEAPS stock replacement is usually -EV due to dividend loss. Use the stock or sell LEAPS puts instead |
| Not factoring dividend impact on early exercise probability | ITM LEAPS calls on high-dividend stocks have elevated early exercise risk. The dividend can trigger exercise even with significant time premium remaining |

## Dividend-Adjusted LEAPS Decision Matrix

| Dividend Yield | LEAPS Call (Stock Replacement) | LEAPS Put (Sell) | PMCC | LEAPS Collar |
|---------------|-------------------------------|-------------------|------|-------------|
| 0% (AMZN, GOOGL) | ✅ Best case | Neutral | ✅ Good | ⚠️ No dividend to offset collar cost |
| 0-1.5% (AAPL, NVDA, SPY) | ✅ Good (dividend gap < 3% over 2 yr) | Slightly favorable puts | ✅ Premium offsets dividend gap | ✅ Good |
| 1.5-3% (MSFT, JPM) | ⚠️ Borderline (gap = 3-6% over 2 yr) | ✅ Favorable puts | ⚠️ PMCC premium must exceed dividend gap | ✅ Collar more attractive |
| 3-5% (KO, VZ, T) | ❌ Poor (gap = 6-10% over 2 yr) | ✅ Best case — sell puts | ❌ PMCC unlikely to overcome gap | ✅ Best — collar financed by high div |
| 5%+ (MO, BTI) | ❌ Never | ✅ Sell puts or buy stock | ❌ Don't bother | ✅ Excellent |

## Provenance

[VERIFIED] Options holders do not receive dividends per OCC rules. Put-call parity with dividends: C + K×e^(-rT) = P + S - PV(D).
[VERIFIED] ITM call exercise before ex-dividend is rational when dividend > remaining time value. This is a well-documented phenomenon (Kalay & Subrahmanyam, 2020).
[COMPUTED] Dividend-adjusted PCP calculations. Actual premiums vary with IV and rate environment.
[COMMON-PRACTICE] PMCC premium offset strategy from Options Alpha and Tastytrade research.
[BACKTEST-EVIDENCE] CCL example from Trading project trade ledger. CCL suspended dividends in 2020.
[AS OF 2026-07]
