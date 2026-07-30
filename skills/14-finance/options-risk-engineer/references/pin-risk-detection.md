# Pin Risk Detection

## What is Pin Risk?

Pin risk occurs when you are short an option whose strike is near the current stock price near expiration. At 4:00 PM ET on expiration day, you don't know whether you'll be assigned. But if assigned, you wake up Monday with a stock position that may have gapped significantly over the weekend — with no ability to hedge.

The critical window: Friday 4:00 PM ET (options stop trading) → Monday 9:30 AM ET (stock re-opens). That is 65.5 hours of market risk with zero ability to manage positions.

## Detection Algorithm

```
if (abs(strike - spot) / spot < 0.005 AND DTE <= 3 AND position is short):
    PIN_RISK = True
```

Thresholds [COMMON-PRACTICE]:
- 0.5% of spot price = pin risk zone. SPY at $500 → any short strike between $497.50 and $502.50 is pinned.
- DTE ≤ 3: pin risk is highest on expiration day but meaningful 1-3 days out.
- Only short positions matter: long holders control exercise decision; short holders do not.

## Broker Auto-Exercise / Auto-Close Behaviors

| Broker | Behavior | Timing |
|--------|----------|--------|
| Robinhood | Auto-closes any option ITM by $0.01+ at 3:00 PM ET on expiration day if account cannot support exercise/assignment [VERIFIED] | 3:00 PM ET |
| TD Ameritrade / Thinkorswim | Auto-exercises all long options $0.01+ ITM at expiration. Auto-assignment on short options follows OCC exercise notices [VERIFIED] | 4:00 PM ET cutoff, OCC processes by 5:30 PM |
| Interactive Brokers | Allows you to manage positions through close but will liquidate at 3:45 PM ET if margin is insufficient to hold resulting stock position [VERIFIED] | 3:45 PM ET liquidation check |
| TastyTrade | Same as TDA (same clearing firm). Auto-exercise $0.01+ ITM [VERIFIED] | 4:00 PM ET cutoff |
| E*TRADE | Risk desk reviews accounts 2:00-3:30 PM ET. May close positions without notice if assignment would create margin deficiency [VERIFIED] | 2:00-3:30 PM ET |

Key insight: You do NOT control whether you get assigned on a short option near expiration. The long holder decides. If the option is $0.01 ITM at 4:00 PM ET, the OCC auto-exercises it unless the long holder explicitly submits a contrary exercise instruction [VERIFIED].

## Assignment Probability by Moneyness

These are empirical estimates based on observed market behavior [INFERRED]:

| Moneyness | Assignment Probability | Reasoning |
|-----------|----------------------|-----------|
| ATM ($0.00-$0.10 ITM) | ~90% | Auto-exercise catches most. Only deep OTM holders who forget to submit contrary instructions escape |
| Slightly ITM ($0.10-$0.50) | ~70% | Some holders close early rather than take assignment. But auto-exercise still triggers for most |
| Moderately ITM ($0.50-$1.00) | ~50% | More holders close positions before expiration. Assignment less certain but still material |
| Deep ITM ($1.00+) | ~30% | Most holders close or roll before expiration. But anyone holding through expiration gets auto-exercised |
| OTM | 0% | No auto-exercise. Short holder safe from assignment |

## Dividend Assignment Risk

Short calls carry additional early-assignment risk around ex-dividend dates [COMMON-PRACTICE]:

```
if (call_strike - stock_price < dividend AND ex_div_date < expiration AND ex_div_date - today <= 1):
    assignment_risk = 0.85
```

Mechanics: The call holder can exercise early to capture the dividend. They pay strike price, receive stock + dividend. This is rational when the dividend exceeds the remaining time value of the call. Assignment occurs the day BEFORE ex-dividend date (you must own shares on ex-div date to receive dividend) [VERIFIED].

Example: AAPL at $185, strike $190 call, dividend $1.00. Stock at $191 = call $1.00 ITM. Dividend $1.00 > remaining time value ~$0.15. Holder exercises, you deliver shares at $190, lose the $1.00 dividend you would have received holding shares plus the $1.00 ITM value = $2.00/share × 100 shares/contract = $200 per contract [COMPUTED].

## Pre-Close Action Plan

### Thursday Before Expiration Friday
- Scan all short positions with DTE ≤ 2
- Flag any strike within 0.5% of current price
- Decision matrix:

| Scenario | Action | Cost Estimate |
|----------|--------|---------------|
| Short option ATM (within 0.5%), DTE=1 | Close it. Cost: ~$0.03-0.05 × 100 × contracts | $3-5/contract |
| Short option 0.5-1% OTM, DTE=1 | Close or roll. Cost: ~$0.01-0.03 | $1-3/contract |
| Short option >1% OTM, DTE=1 | Monitor. Assignment risk <10% | Minimal |
| Short option ITM by >1%, DTE=1 | Close NOW. Assignment near certain | ITM amount × 100 × contracts |

Cost-benefit: Closing a $0.03 pin-risk option costs $3/contract. If assigned and stock gaps $2.00 over weekend, loss = $200/contract. The $3 insurance is worth 66:1 expected value [COMPUTED].

### Expiration Friday Timeline
1. **12:00 PM ET**: Review all expiring positions. Pin-risk scan.
2. **2:00 PM ET**: Call broker risk desk if questions. They are reviewing accounts now.
3. **2:45 PM ET**: Final decision deadline. Robinhood closes at 3:00 PM, IBKR at 3:45 PM. Don't wait.
4. **3:00 PM ET**: All closing orders must be executed. Markets thin out, spreads widen.
5. **4:00 PM ET**: Options stop trading. Whatever you hold determines your weekend risk.
6. **5:30 PM ET**: OCC processes exercise/assignment. You cannot change anything after 4:00 PM.
7. **Saturday AM**: Broker notifies you of assignments.
8. **Monday 9:30 AM ET**: Stock opens. You discover whether the gap was in your favor.

## Weekend Gap Risk Quantification

| Asset | Typical Weekend Gap (±1σ) | Worst Weekend Gap (5-year) |
|-------|---------------------------|----------------------------|
| SPY | ±0.5% | -4.1% (Mar 2020 COVID) [VERIFIED] |
| QQQ | ±1.0% | -5.8% (Mar 2020) [VERIFIED] |
| AAPL | ±1.2% | -12.9% (Mar 2020) [VERIFIED] |
| TSLA | ±2.5% | -21.3% [VERIFIED] |
| GME | ±5.0%+ | N/A — unreliable estimate |

Gap risk on 10 contracts of TSLA pinned at $250 strike:
- 1σ weekend gap: ±$6.25 × 1000 shares = ±$6,250
- Worst case: $52.50 × 1000 shares = -$52,500

Cost to close pin-risk position: ~$30. Maximum weekend loss: $52,500. The math is unambiguous [COMPUTED].

## Pin Risk by Strategy Type

| Strategy | Pin Risk Level | Mitigation |
|----------|---------------|------------|
| Short naked put | HIGH | Close by Thursday. One assignment = 100 shares/contract |
| Short naked call | HIGH | Close by Thursday. Short stock assignment on Monday |
| Short put spread | MODERATE | Max loss is defined by spread width, but assignment on short leg creates stock position that gaps against long leg protection |
| Short call spread | MODERATE | Same mechanics as put spread — assignment creates interim stock position |
| Iron condor | MODERATE-HIGH | Pin risk on ONE side only (both can't be ITM simultaneously). But assignment on one side + weekend gap = stock position outside spread protection |
| Short strangle | HIGH | Naked on both sides. Pin risk applies to whichever side is near-the-money |
| Long options | NONE | You control exercise. No assignment risk |
| Cash-settled (SPX, NDX) | NONE | No delivery. Cash settlement eliminates pin risk entirely [VERIFIED] |

Key insight: Cash-settled index options (SPX, NDX, RUT) have ZERO pin risk. This is the single biggest advantage of trading SPX over SPY for premium-selling strategies [VERIFIED].

## Avoiding Pin Risk Entirely

The simplest risk management rule in options [COMMON-PRACTICE]:

**Close or roll ALL short options with DTE ≤ 7 regardless of moneyness.**

Cost of rolling early: ~$0.05-0.10 slippage per contract × 52 weeks. On a 10-contract weekly position, that's $260-520/year. Cost of ONE pin-risk assignment that gaps against you: potentially $2,000-20,000.

This is insurance with a ~10:1 to 100:1 expected value. You cannot afford NOT to manage pin risk [COMPUTED].


