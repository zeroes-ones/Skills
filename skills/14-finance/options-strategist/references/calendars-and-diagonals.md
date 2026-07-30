# Calendars and Diagonals

## Purpose
Operational guide to calendar spreads (same strike, different expirations) and diagonal spreads (different strikes, different expirations). These are the primary term-structure strategies — profiting from the differential in time decay between near-month and far-month options, combined with vega exposure from the longer-dated leg.

---

## Calendar Spread Mechanics

### Standard Calendar (Horizontal Spread)
- **Construction:** Sell near-month option, buy far-month option at the SAME strike (same type — both calls or both puts)
- **Entry:** Typically a debit (far-month option costs more due to more time value)
- **Max Profit:** Achieved when the underlying closes EXACTLY at the strike price at near-month expiration, maximizing the value of the remaining far-month option
- **Max Loss:** Debit paid (capped)
- **Breakevens:** Two points — one below and one above the strike. Calculated dynamically based on volatility surface at near-month expiration.

### Key Greeks Profile

| Greek | Sign | Magnitude | Implication |
|-------|------|-----------|-------------|
| Theta | Positive (initially) | Near-month theta > far-month theta | Time decay on the short leg outpaces the long leg. Net theta-positive at entry. |
| Vega | Positive | Far-month vega > near-month vega | IV expansion helps. Calendars are vega-positive strategies. Best deployed in low IV. |
| Gamma | Negative (initially) | Near-month gamma > far-month gamma | Large moves hurt. Calendars want the underlying to stay near the strike. |
| Delta | Near zero at strike | ATM calendars are approximately delta-neutral | Profits come from time and volatility, not direction. |

[VERIFIED] The net theta of a calendar is positive at entry but turns negative if the underlying moves significantly away from the strike. The theta crossover point is approximately ±1 standard deviation from the strike — beyond that, the long leg's theta decay dominates because it has more absolute time value remaining.

---

## Strike Selection for Calendars

| Market Assumption | Strike Placement | Rationale |
|------------------|-----------------|-----------|
| Neutral (stock stays flat) | ATM (± 5 delta) | Maximum theta differential. ATM options have the highest absolute theta. |
| Slightly Bullish | OTM call calendar at 0.25–0.35 delta | Directional lean. If stock rises toward strike, calendar gains from delta AND theta. |
| Slightly Bearish | OTM put calendar at 0.25–0.35 delta | Directional lean. Stock drifting down toward strike benefits the position. |
| Trading range expected | ATM calendar at midpoint of expected range | Stock oscillating around the strike generates maximum theta profit. |

### Expiration Selection
```
Near-month DTE: 7–30 days (where theta decay is fastest)
Far-month DTE:  30–90 days (where theta decay is slowest relative to cost)
Optimal ratio:  Far-month DTE ≈ 2–3× near-month DTE
```

**Example:** Sell the 30-DTE option, buy the 60-DTE option (2:1 ratio). Sell the 14-DTE, buy the 45-DTE (~3:1 ratio). [COMMON-PRACTICE] Avoid ratios below 1.5:1 — the theta differential is too small to overcome bid-ask friction. Avoid ratios above 4:1 — the far-month cost is too high relative to near-month credit.

---

## Term Structure Exploitation

The options term structure (IV across expirations) is the primary edge for calendar spreads.

### Contango (Normal): Far-month IV > Near-month IV
- **Implication:** Calendars are expensive to enter (far-month option is priced at a premium to near-month)
- **Action:** Only enter calendars if the IV differential is modest (< 5 vol points between front and back month)
- **Alternative:** Consider reverse calendars (buy near, sell far) — but these are theta-negative and risky

### Backwardation: Near-month IV > Far-month IV
- **Implication:** Calendars are cheap to enter. Near-month options are expensive (sell rich), far-month are cheap (buy cheap). This is the ideal calendar entry environment.
- **Action:** Aggressively deploy calendars. The term structure edge is in your favor.
- **Common triggers for backwardation:** Earnings in the near month, binary events, sector rotation, pre-FOMC

[INFERRED] Backwardation in the term structure occurs approximately 15–20% of trading days for single-stock options and is most common in the 7–21 DTE front-month window. The edge from backwardation entry adds approximately 5–8% to the expected return of a calendar spread.

---

## Calendar Adjustment Rules

### Near-Month Expiration Approaches

| Scenario | Action |
|----------|--------|
| Stock near strike (± 0.5 SD) as expiration nears | Hold to expiration. Position is performing as designed. Near-month option expires worthless, far-month remains. |
| Stock at strike at near-month expiration | Maximum profit scenario. Close the entire position or sell the far-month leg separately. |
| Stock far from strike (> 1 SD) before near-month expiry | Roll the short leg: buy back the near-month option (likely worthless or cheap), sell the next-month option at the same strike for additional credit. |
| Stock has moved > 2 SD from strike | Close the position. The calendar thesis is broken. The long leg's vega is not compensating for directional loss. |
| Near-month expires ITM | Close or roll BEFORE expiration. Assignment on the short leg creates a naked short/long position in the underlying relative to the far-month long. |

### Rolling Mechanics
```
Initial: Short 30-DTE call + Long 60-DTE call at $100 strike
After 25 days: Short 5-DTE call (near worthless) + Long 35-DTE call
Action: Buy back 5-DTE call for $0.05, sell 35-DTE call for $1.20
Result: Short 35-DTE call + Long 35-DTE call → effectively a vertical spread at same expiration
        OR: sell 65-DTE call to maintain calendar structure (new short 65-DTE, original long now 35-DTE)
```

[COMMON-PRACTICE] Roll the short leg when the near-month option has lost 80–90% of its value. At that point, remaining theta is minimal and rolling captures fresh premium while maintaining the structure.

---

## Diagonal Spread Mechanics

### What Makes It Diagonal
A diagonal spread combines the calendar concept (different expirations) with the vertical concept (different strikes):

- **Long Call Diagonal:** Buy far-month OTM call, sell near-month further-OTM call. Bullish, vega-positive.
- **Short Call Diagonal:** Sell near-month call, buy far-month higher-strike call (PMCC — Poor Man's Covered Call). Slightly bullish to neutral, theta-positive.
- **Long Put Diagonal:** Buy far-month OTM put, sell near-month further-OTM put. Bearish, vega-positive.
- **Short Put Diagonal:** Sell near-month put, buy far-month lower-strike put. Slightly bearish to neutral.

### PMCC (Poor Man's Covered Call) — The Most Common Diagonal

| Parameter | Specification |
|-----------|--------------|
| Long Leg | Buy deep ITM call, 0.80–0.90 delta, 90–365 DTE (LEAPS preferred) |
| Short Leg | Sell OTM call, 0.20–0.30 delta, 14–45 DTE |
| Strike Relationship | Short strike MUST be above long strike (otherwise it's a calendar on a spread, not a PMCC) |
| Max Profit | (Short Strike − Long Strike) − Net Debit + Short Call Premiums (over multiple cycles) |
| Max Loss | Net Debit Paid (if short strike > long strike) |
| Capital Requirement | Net debit of the diagonal (typically 50–75% less than 100 shares) |

### Diagonal Strike Selection Rules
```
For PMCC: Long call strike ≤ 0.80 delta (deep ITM), Short call strike ≥ Long strike + 2–3 strike widths
```
[VERIFIED] The short call strike MUST be above the long call strike. If the short call goes ITM and is assigned, the long call must cover the assignment. If the short strike is below the long strike, assignment creates a net debit that is NOT covered by the long leg — this is a catastrophic structural error.

---

## Profit Sources for Calendars and Diagonals

| Profit Source | Calendar | Diagonal | Timing |
|--------------|----------|----------|--------|
| Theta decay on short leg | Primary | Primary | Continuous; accelerates in final 30 days |
| Vega expansion on long leg | Secondary | Secondary | Event-driven; benefits from IV spikes |
| Directional move toward long strike | Not applicable (same strike) | Secondary (diagonal only) | Continuous |
| Term structure normalization (backwardation → contango) | Bonus | Bonus | Post-event mean reversion |
| Multiple short-leg cycles (rolls) | Secondary | Primary (PMCC) | Each expiration cycle |

---

## Failure Modes

### 1. IV Crush on the Long Leg
Both legs lose value, but the long leg (far-month, higher vega) loses more. The calendar/diagonal turns from theta-positive to a net loser. **Prevention:** Enter calendars only when IV Rank < 30 OR in backwardation. Avoid entering before earnings (event vol collapses post-event).

### 2. Underlying Moves Far from Strike (Calendar)
A 3 SD move destroys a calendar. The near-month short expires worthless (small win), but the far-month long loses 60–80% of its value (big loss). **Prevention:** Set a stop-loss at 2× debit paid. If the calendar was entered for $1.50 debit, close at a $3.00 loss.

### 3. Near-Month Expires ITM Without Management (Calendar)
The short leg is assigned. You now have a naked short position against your long far-month option. The long option does NOT automatically cover short assignment. **Prevention:** Close or roll all calendars 2 days before near-month expiration.

### 4. PMCC Short Strike Below Long Strike (Diagonal)
Structural error — if the short call is assigned, the long call does not fully cover. You owe (short strike − long strike) × 100 × contracts in additional cash. **Prevention:** Verify at entry: short call strike > long call strike. This is non-negotiable.

### 5. Rolling the Short Leg for Debits (Diagonal/Calendar)
Each roll for a debit erodes the net credit base. After 3 debit rolls on a $1.50 credit position, you've paid $2.00+ in rolls for a position that was supposed to be an income strategy. **Prevention:** Hard rule — maximum 2 rolls total. If the position can't be rolled for credit on the third expiration, close it.

