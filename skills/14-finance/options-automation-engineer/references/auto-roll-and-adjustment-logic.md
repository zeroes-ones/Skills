# Auto-Roll and Adjustment Logic

## The Roll Decision Framework

Rolling options positions is mechanically simple (close existing, open new) but strategically complex. The decision to roll must account for: credit received, DTE of the new position, capital efficiency, and the distinction between "rolling to extend" and "rolling to avoid taking a loss."

## Ground Rules for Rolling

**GR-R1: IF roll credit < $0.05/contract → DO NOT ROLL. Close or let expire.** [COMMON-PRACTICE] Below $0.05, the credit doesn't justify the transaction costs or the extended capital commitment.

**GR-R2: IF rolling an ITM credit spread → MAX 1 ROLL. After that, take assignment or close.** [VERIFIED] Rolling ITM spreads is "rolling down a hole." Each roll extends capital commitment without changing the fundamental problem — the strike was wrong.

**GR-R3: IF rolling for credit AND original credit received → IF net credit < 80% of original → REJECT.** Rolling for a fraction of the original credit is just loss-avoidance behavior.

**GR-R4: IF total rolls on one position > 2 → HARD STOP. Close the position.** [BACKTEST-EVIDENCE] Positions rolled 3+ times have -40% worse cumulative P&L than positions closed cleanly on the first roll.

**GR-R5: IF DTE remaining ≤ 7 AND OTM credit spread → DO NOT ROLL. Close.** Gamma risk in the final week makes rolling into unknown territory.

## Roll Types by Strategy

### Credit Spread Roll Matrix

| Situation | Action | Parameters |
|-----------|--------|------------|
| OTM, 21 DTE, credit > $0.05 | Roll to 42-45 DTE, same strikes | Stay ahead of theta acceleration |
| OTM, 21 DTE, credit < $0.05 | Close. 50% target should have hit by now | If credit too small, it's not worth the capital |
| OTM, 14 DTE, < 50% profit | Roll to 30 DTE, same strikes | Time is running out on theta |
| OTM, 14 DTE, > 50% profit | Close. Take the win | Never let a winner become a roller |
| ATM, 14 DTE | Roll to 30 DTE, adjust strikes if directional view changed | ATM means the credit is eroding fast |
| ITM, 14 DTE | Close or take assignment. Do NOT roll unless credit > original × 0.80 | ITM roll credit is usually small; not worth the risk |
| ITM, 7 DTE | Take assignment or close. NEVER roll | Gamma explosion zone |

### Diagonal / Calendar Roll Matrix

| Situation | Action | Parameters |
|-----------|--------|------------|
| Short leg ATM, OTM long leg, 7 DTE on short | Roll short leg to 30 DTE, same or adjusted strike | Short leg time decay extracted; redeploy |
| Short leg ITM, long leg OTM, 7 DTE on short | Close entire position OR roll short + adjust long strike | The spread is broken. Don't chase |
| Both legs OTM, short leg close to 0 value | Roll short leg early to capture next cycle | If short is at $0.05, close it. Free up capital for next cycle |
| Short leg ATM, long leg substantial value remaining, 3 DTE | Roll short to next month. Protect long leg value | Gamma risk on short leg is acute. Roll NOW |

### PMCC (Poor Man's Covered Call) Roll Logic

```
Every cycle (30-45 days on the short leg):
├─ Short leg OTM at expiration → NEW short leg at strike > LEAPS strike, 30-45 DTE
├─ Short leg ATM at 7 DTE → ROLL NOW to next cycle. Do not wait for expiration
├─ Short leg ITM at 7 DTE →
│  ├─ Roll up and out if credit > $0.00 AND new strike > LEAPS strike
│  └─ If roll credit negative OR new strike < LEAPS strike → Close entire position
└─ LEAPS DTE < 180 → STOP PMCC. Close or convert to stock replacement only
```

## State Machine for Trade Lifecycle

```
[IDEA] → [SCREEN] → [CONFIRM] → [SIZE] → [ENTER] → [MONITOR] →
  ├─ [WIN] → [EXIT] → [JOURNAL]
  ├─ [LOSS] → [EXIT] → [JOURNAL]
  ├─ [ROLL] → [ENTER] (new position)
  ├─ [ADJUST] → [MONITOR] (modified existing)
  └─ [TIME STOP] → [EXIT] → [JOURNAL]

State transitions:
- SCREEN → CONFIRM: All research prerequisites met
- CONFIRM → SIZE: Risk check passed, sizing calculated
- SIZE → ENTER: Order filled. Log entry
- ENTER → MONITOR: Position tracked in real-time
- MONITOR → WIN/LOSS/ROLL/ADJUST/TIME STOP: Based on position state
```

## Adjustment Patterns

### Iron Condor Adjustment

**When one side is tested (delta > 0.30 on one wing):**

Option A: **Roll the untested side closer.** Collect more credit. Widens profit zone on the tested side.
- If 10-15 DTE: roll untested wing to 0.10-0.15Δ
- If 5-10 DTE: roll untested wing to collect 30-40% of original credit
- NEVER both roll AND widen the tested side. Pick one adjustment.

Option B: **Convert to iron butterfly.** Close the untested side. Accept reduced profit but defined risk.
- Best when: < 10 DTE, tested wing is only 1-2% ITM
- NOT best when: tested wing is deep ITM (close the position)

Option C: **Close the position.** Accept the loss.
- Best when: tested wing is > 2% ITM, DTE < 10, roll credit insufficient
- HARD RULE: maximum loss on any iron condor is 2× credit received

### Butterfly Adjustment

Butterflies are pin-seeking structures. Adjustments are usually destructive.

**If the underlying moves 1 strike away from center:**
1. Close the position. The probability of a return to the center is low relative to the remaining credit.
2. Do NOT add another butterfly at the new level. This is doubling down on a pin that's moving away from you.

**If the underlying stays range-bound but theta is running out:**
1. If DTE < 7 and still near center: let it ride. Gamma can bring it home.
2. If DTE < 3 and 1 strike away: close. Pin probability drops to < 20%.

## Automated Roll Rules (Production)

```python
def should_roll_credit_spread(position: dict) -> dict:
    """Determine if a credit spread should be rolled."""
    dte = position["dte"]
    is_otm = position["mark"] > 0 and position["mark"] < position["width"]
    profit_pct = position["credit"] - position["mark"]  # simplified
    is_itm = position["underlying_price"] > position["short_strike"]  # calls

    decision = {"action": "hold", "reason": "No roll criteria met"}

    # Short circuit: ITM with ≤7 DTE
    if is_itm and dte <= 7:
        return {"action": "close", "reason": "ITM at 7 DTE — gamma risk critical"}

    # OTM credit spread at DTE roll threshold
    if is_otm and dte <= 21:
        roll_credit = estimate_roll_credit(position)
        if roll_credit >= 0.05:
            return {"action": "roll", "reason": f"Roll credit ${roll_credit:.2f} at {dte}DTE",
                    "roll_credit": roll_credit, "target_dte": 42}
        else:
            return {"action": "close", "reason": f"Roll credit ${roll_credit:.2f} too small"}

    # Profit target check
    if profit_pct >= 0.50 * position["credit"]:
        return {"action": "close", "reason": f"50% profit target reached"}

    return decision


def estimate_roll_credit(position: dict) -> float:
    """Estimate credit from rolling to 42 DTE same strikes."""
    # Real implementation would query option chain
    target_dte = 42
    current_short = get_option_price(
        position["underlying"], position["short_strike"],
        position["expiration"], position["option_type"]
    )
    new_short = get_option_price(
        position["underlying"], position["short_strike"],
        target_dte, position["option_type"]
    )
    new_long = get_option_price(
        position["underlying"], position["long_strike"],
        target_dte, position["option_type"]
    )
    close_cost = current_short  # buy to close existing short
    open_credit = new_short - new_long  # sell to open new spread
    return open_credit - close_cost
```

## Roll Tracking

Every roll must be logged:

```python
roll_log = {
    "position_id": "uuid",
    "roll_number": 1,  # 1st roll, 2nd roll, etc.
    "original_credit": 1.20,
    "roll_credit": 0.15,
    "cumulative_credit": 1.35,
    "roll_dte_entered": 21,
    "new_dte": 42,
    "reason": "DTE threshold reached, still OTM",
    "timestamp": "2026-07-16T10:30:00Z"
}
```

**Flag: cancel-task** if total_rolls > 2 for any position. HARD STOP.
