# Error Recovery — Futures-Specific

> Futures-specific error patterns: margin call response, gap-through-stop recovery, delivery notice handling, roll error correction.

## Error Pattern 1: Margin Call

### Symptom
- Broker notification: "Margin deficiency in account."
- Equity fell below maintenance margin requirement.
- Position may be at risk of auto-liquidation.

### Root Cause
- Position moved against you more than the maintenance margin buffer
- OR: SPAN margin requirement increased (exchange raised scan range)
- OR: You added a position without sufficient excess margin

### Immediate Response

```
1. DO NOT PANIC-SELL. Evaluate:
   ├── Is this a normal volatility move or a structural break?
   ├── What is the margin shortfall in dollars and as % of account?
   └── How much time does the broker give? (Usually same day)

2. OPTIONS TO MEET CALL:
   ├── Deposit additional capital (wire transfer, instant if linked bank)
   ├── Reduce position size (sell partial position)
   ├── Hedge with options (buy puts if long, buy calls if short)
   │   → This may reduce SPAN margin by creating offsetting risk
   └── Do nothing → broker auto-liquidates (WORST option — lose control of exit)

3. AFTER CALL IS MET:
   ├── Compute: margin utilization should be ≤50% going forward
   ├── The margin call is a POSITION SIZING FAILURE — learn from it
   └── Adjust: increase margin buffer from 50% to 60% minimum
```

### Prevention
- Track margin utilization daily (not weekly)
- Maintain 50% margin buffer minimum
- Reduce positions before known volatility events (FOMC, NFP, CPI)
- Monitor SPAN scan range changes (CME updates weekly)
- Cross-margin positions reduce combined requirement — use it

## Error Pattern 2: Gap Through Stop

### Symptom
- Stop order was at 5517.50
- Market gapped from 5520.00 to 5490.00 (no trades in between)
- Order filled at 5490.00 — NOT at 5517.50
- Actual loss: 35.50 points instead of expected 8.00 points

### Root Cause
- Stops are TRIGGERS that send MARKET orders
- In a gap, the market order fills at the next available price, not the stop price
- Gaps are common: FOMC, NFP, CPI, earnings, geopolitical events, weekend opens

### Response

```
1. ACCEPT THE FILL. It happened. Fighting it wastes mental capital.

2. EVALUATE: Is this a trade-level problem or a risk-management problem?
   ├── Trade-level: Bad entry, wrong direction → Stop-loss did its job
   └── Risk mgmt: Correct direction, gap caused excessive loss → Position was too large

3. QUANTIFY THE GAP:
   Actual Loss - Expected Loss = Gap Premium
   Example: $1,775 actual - $400 expected = $1,375 gap premium
   This is the COST of holding through a binary event.

4. DECISION:
   ├── Re-enter immediately? Only if thesis is intact and gap is retraced
   ├── Wait for stabilization? Usually the right call
   └── Abandon? If gap broke the thesis (e.g., dovish FOMC vs your rate-hike thesis)
```

### Prevention (The Only Real Fix)
- Stops DON'T protect against gaps. Nothing does.
- Reduce position 50-75% before known binary events
- Use LONG OPTIONS for gap protection (buy puts/OTM calls)
- Accept that some events create unavoidable risk — size for the gap, not the stop
- Overnight positions: expect gaps. Size for 2-3× normal adverse move.

## Error Pattern 3: Delivery Notice Received

### Symptom
- Broker notification: "Delivery notice assigned on long [contract]."
- You held a physical-delivery futures position past First Notice Day.
- You may be obligated to take delivery of the physical commodity.

### Root Cause
- Automated position management failure
- Did not track FND calendar
- Assumed broker would auto-liquidate (they may, but timing varies)

### Immediate Response

```
1. DO NOT IGNORE. This does not go away on its own.

2. CONTACT BROKER IMMEDIATELY:
   ├── Phone is faster than email or chat
   ├── Ask: "Can this delivery notice be offset?"
   └── Most brokers can offset delivery notices by creating an offsetting position
       that nets to zero for delivery purposes

3. IF DELIVERY CANNOT BE OFFSET:
   ├── You must buy/sell the offsetting futures position yourself
   ├── You will have TWO positions for a brief period (the delivery + the offset)
   ├── The broker will net them for settlement
   └── There WILL be fees: delivery assignment fee + liquidation fee

4. AFTER RESOLVED:
   ├── Review FND calendar for ALL open positions
   ├── Set calendar alerts: FND-14, FND-10, FND-7, FND-5, FND-3
   └── Implement hard rule: NO physical-delivery positions past FND-7
```

### Prevention (Essential)
- Calendar ALL physical-delivery contracts at entry
- FND-14 alert: Plan exit
- FND-7 alert: Execute exit
- FND-3 alert: Position must be ZERO
- Never hold physical-delivery contracts into FND period

## Error Pattern 4: Roll Execution Error

### Symptom
- Attempted roll as two separate orders
- First leg filled, second leg did not fill
- Now you have either: NO position (sold front-month, didn't buy next) or DOUBLE position (bought front-month, didn't sell next)

### Root Cause
- Used two outright orders instead of a calendar spread order
- Market moved between order executions
- One leg filled at limit, other leg moved past limit

### Response

```
1. ASSESS CURRENT POSITION:
   ├── FLAT (sold front, didn't buy next) → You're out. Re-enter if thesis intact.
   ├── LONG 2× (bought next without selling front) → Reduce immediately to 1×
   └── SHORT 1× + LONG 1× = accidental spread → Net out if not intentional

2. IF FLAT AND WANT TO RE-ENTER:
   ├── Use limit order (not market)
   ├── Accept the missed fill as the cost of using the wrong order type
   └── Don't chase — wait for a pullback to re-enter

3. IF ACCIDENTALLY DOUBLED:
   ├── Sell the extra immediately — you didn't plan for 2× risk
   ├── Evaluate: did you just want to be 1× or did you accidentally double?
   └── If doubled, your risk is 2× planned. Cut to planned size NOW.
```

### Prevention
- ALWAYS use calendar spread orders for rolls
- This error is 100% preventable by using the correct order type
- If your broker cannot do spread orders, switch brokers

## Error Pattern 5: Trading the Wrong Contract Month

### Symptom
- Thought you were trading the front-month (Sep expiry)
- Actually traded the deferred month (Dec expiry)
- Position behaves differently from expectation (different liquidity, different price)

### Root Cause
- Contract month code confusion
- Did not verify the contract symbol and expiration before placing order
- Auto-filled contract selector chose wrong month

### Response

```
1. IF IMMEDIATELY DISCOVERED (same session):
   ├── Close the wrong contract
   └── Open the correct contract
   ├── Cost: bid-ask spread × 2 (wrong contract exit + correct contract entry)
   └── Accept this as a cheap lesson

2. IF DISCOVERED AFTER POSITION MOVES:
   ├── Evaluate: is the deferred-month position profitable or at a loss?
   ├── If profitable: close at profit, switch to correct month
   ├── If at loss: close immediately, don't let it run — you didn't plan this trade
   └── The deferred month may have different fundamentals (e.g., new crop vs old crop)

3. GRAINS WARNING:
   ├── Old-crop (front-month) vs new-crop (deferred) are DIFFERENT markets
   ├── Example: Jul Corn (old crop, tight supply) vs Dec Corn (new crop, uncertain)
   ├── The spread between them IS the trade thesis itself
   └── Being in the wrong month = accidentally trading a spread
```

### Prevention
- ALWAYS verify: symbol + month code + year before confirming order
- Never rely on auto-complete or auto-select for contract months
- Double-check the contract specification page for the exact symbol

