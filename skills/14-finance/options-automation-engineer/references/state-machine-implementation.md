# State Machine Implementation for Options Automation

> **Portability target:** Spec-level. State machines are universal — implement in any language. Code examples in Python/pseudocode.

## The State Machine: Every Options Trade Has a Lifecycle

```
[IDLE] → [SCANNING] → [SIGNAL] → [SIZING] → [ENTRY] → [MONITORING]
                                                         ├── [ADJUST] → [MONITORING]
                                                         ├── [ROLL] → [MONITORING]
                                                         └── [EXIT] → [JOURNAL] → [IDLE]

[ANY STATE] → [CIRCUIT_BREAKER] → [EMERGENCY_EXIT] → [IDLE]
```

## State Definitions

| State | Description | Entry Condition | Exit Condition |
|-------|------------|----------------|---------------|
| IDLE | No active trades. System ready. | On startup or after EXIT + JOURNAL | Scanner timer fires |
| SCANNING | Running scanner pipeline against universe | Timer or manual trigger | Strategy match found |
| SIGNAL | Signal generated, awaiting entry | Scanner returns match | Entry order placed or signal expired |
| SIZING | Computing position size | Signal confirmed | Size output returned |
| ENTRY | Order submitted, awaiting fill | Sizing output accepted | Fill confirmed or order cancelled |
| MONITORING | Active position, tracking Greeks and P&L | Fill confirmed | Profit target, stop, time stop, or adjustment trigger |
| ADJUST | Executing adjustment order | Adjustment trigger fires | Adjustment fill confirmed |
| ROLL | Executing roll order | Roll trigger fires (DTE threshold, ITM gate) | Roll fill confirmed |
| EXIT | Closing position | Profit target, stop, time stop, or manual | All legs closed |
| JOURNAL | Logging trade details | EXIT completed | Journal entry saved |
| CIRCUIT_BREAKER | System halt — emergency | Max daily loss, max drawdown, VIX spike, or API disconnect | Manual override or cooldown expired |

## Implementation Pattern

```python
class OptionTradeStateMachine:
    """Manages the lifecycle of a single options trade."""

    VALID_TRANSITIONS = {
        'IDLE': ['SCANNING'],
        'SCANNING': ['SIGNAL', 'IDLE'],
        'SIGNAL': ['SIZING', 'IDLE'],  # IDLE if signal expires
        'SIZING': ['ENTRY', 'IDLE'],    # IDLE if sizing rejects
        'ENTRY': ['MONITORING', 'IDLE'], # IDLE if order cancelled/rejected
        'MONITORING': ['ADJUST', 'ROLL', 'EXIT', 'CIRCUIT_BREAKER'],
        'ADJUST': ['MONITORING', 'EXIT'], # EXIT if adjustment fails
        'ROLL': ['MONITORING', 'EXIT'],   # EXIT if roll rejected
        'EXIT': ['JOURNAL'],
        'JOURNAL': ['IDLE'],
        'CIRCUIT_BREAKER': ['IDLE'],  # IDLE only after cooldown + manual review
    }

    def transition(self, to_state: str, reason: str):
        if to_state not in self.VALID_TRANSITIONS[self.current_state]:
            raise IllegalTransitionError(
                f"Cannot transition {self.current_state} → {to_state}. "
                f"Valid: {self.VALID_TRANSITIONS[self.current_state]}"
            )
        self.log_transition(self.current_state, to_state, reason)
        self.current_state = to_state
```

## Critical Rules

### R1: Circuit Breaker Has Priority

The CIRCUIT_BREAKER state must be reachable from ANY state. Implementation:

```python
# In every state's update loop:
if self.circuit_breaker.check():
    self.transition('CIRCUIT_BREAKER', self.circuit_breaker.reason)
    self.halt_all_execution()
    return
```

### R2: Maximum 2 Consecutive Rolls

```python
def roll_decision(self) -> bool:
    if self.roll_count >= 2:
        self.transition('EXIT', 'Maximum rolls reached (2). Closing position.')
        return False
    if self.roll_credit < 0.05:
        self.transition('EXIT', f'Roll credit ${self.roll_credit:.2f} < $0.05 minimum.')
        return False
    self.roll_count += 1
    return True
```

### R3: Never Transition While Order Is Unconfirmed

```python
if self.has_pending_order():
    raise IllegalTransitionError("Cannot transition state with unconfirmed order.")
```

## State Persistence

Every state transition must be persisted. Recovery from crash:

```python
def recover_from_crash(self):
    last_state = database.get_last_state(self.trade_id)
    last_order = database.get_last_order(self.trade_id)

    if last_order and last_order.status in ('pending', 'working'):
        # Order may have filled during outage — reconcile before continuing
        self.reconcile_order(last_order)
    else:
        self.current_state = last_state
```

## Audit Trail Requirements

Every transition logs: timestamp, from_state, to_state, reason, trade_id, portfolio_value, and a unique transition_id. This is non-negotiable. Without an audit trail, you cannot debug, cannot optimize, and cannot prove you weren't trading recklessly.

```json
{
  "transition_id": "uuid",
  "trade_id": "uuid",
  "timestamp": "ISO8601",
  "from_state": "MONITORING",
  "to_state": "EXIT",
  "reason": "Profit target hit: 50% of max profit",
  "portfolio_value": 125432.50,
  "trigger": "profit_target_50pct"
}
```
