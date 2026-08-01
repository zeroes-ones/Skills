# Circuit Breakers and Safety Systems

## The Case for Circuit Breakers

Automated options trading without circuit breakers is a time bomb. Options have asymmetric risk profiles, and an automation system that keeps trading through a broken strategy can compound losses faster than a human could. Circuit breakers are the stop-loss on the automation system itself.

## Circuit Breaker Hierarchy

```
LEVEL 1: Position-level circuit breakers
  └─ (applied to each individual position)
      │
LEVEL 2: Strategy-level circuit breakers
  └─ (applied per strategy type: credit spreads, debit spreads, etc.)
      │
LEVEL 3: Account-level circuit breakers
  └─ (applied to the entire automation system)
      │
LEVEL 4: Market-level circuit breakers
  └─ (triggered by external market conditions)
```

## Level 1: Position Circuit Breakers

### Individual Position Limits

```python
POSITION_BREAKERS = {
    "max_loss_per_position": 200,       # Hard dollar cap per position
    "max_drawdown_from_high": 0.50,     # 50% from position's peak value
    "max_holding_days": 60,             # Time-based stop
    "max_contracts_per_position": 50,   # Absolute contract cap
    "max_notional_per_position": 50000, # Max underlying notional
}
```

### Position Breaker Logic

```python
def check_position_breakers(position):
    """Check all position-level circuit breakers. Return list of triggered breakers."""
    triggered = []

    # Dollar loss cap
    if position.unrealized_pnl < -POSITION_BREAKERS["max_loss_per_position"]:
        triggered.append({
            "breaker": "max_loss_per_position",
            "action": "close_position",
            "reason": f"Loss ${abs(position.unrealized_pnl):.0f} exceeds ${POSITION_BREAKERS['max_loss_per_position']} cap"
        })

    # Drawdown from high
    if position.drawdown_from_high > POSITION_BREAKERS["max_drawdown_from_high"]:
        triggered.append({
            "breaker": "max_drawdown_from_high",
            "action": "close_position",
            "reason": f"Drawdown {position.drawdown_from_high:.1%} from position high"
        })

    # Max holding days
    if position.days_held > POSITION_BREAKERS["max_holding_days"]:
        triggered.append({
            "breaker": "max_holding_days",
            "action": "close_position",
            "reason": f"Held {position.days_held} days, exceeding {POSITION_BREAKERS['max_holding_days']} max"
        })

    # Gamma risk at low DTE
    if position.dte <= 7 and position.structure in ["credit_spread", "iron_condor"]:
        if position.delta > 0.40:
            triggered.append({
                "breaker": "gamma_zone",
                "action": "close_position",
                "reason": f"High gamma risk: DTE={position.dte}, delta={position.delta}"
            })

    return triggered
```

## Level 2: Strategy Circuit Breakers

### Strategy-Specific Limits

```python
STRATEGY_BREAKERS = {
    "credit_spreads": {
        "max_consecutive_losses": 5,
        "max_daily_loss": 500,
        "max_weekly_loss": 1500,
        "max_open_positions": 10,
        "min_credit_received": 0.10,   # Reject trades below this credit
    },
    "iron_condors": {
        "max_consecutive_losses": 4,
        "max_daily_loss": 400,
        "max_weekly_loss": 1200,
        "max_open_positions": 5,        # Fewer — more complex
        "min_credit_received": 1.00,
    },
    "debit_spreads": {
        "max_consecutive_losses": 3,    # Lower tolerance — lower win rates
        "max_daily_loss": 300,
        "max_weekly_loss": 900,
        "max_open_positions": 8,
        "max_debit_per_trade": 3.00,
    },
}
```

### Strategy Breaker Logic

```python
def check_strategy_breakers(strategy_id, strategy_type):
    """Check strategy-level breakers."""
    breaker = STRATEGY_BREAKERS.get(strategy_type, {})
    strategy_state = get_strategy_state(strategy_id)
    triggered = []

    # Consecutive losses
    if strategy_state["consecutive_losses"] >= breaker.get("max_consecutive_losses", 5):
        triggered.append({
            "breaker": "max_consecutive_losses",
            "action": "pause_strategy",
            "duration_hours": 24,
            "reason": f"{strategy_state['consecutive_losses']} consecutive losses"
        })

    # Daily loss
    if strategy_state["daily_pnl"] < -breaker.get("max_daily_loss", 500):
        triggered.append({
            "breaker": "max_daily_loss",
            "action": "pause_strategy_today",
            "reason": f"Daily loss ${abs(strategy_state['daily_pnl']):.0f} exceeds limit"
        })

    # Max open positions
    if strategy_state["open_positions"] >= breaker.get("max_open_positions", 10):
        triggered.append({
            "breaker": "max_open_positions",
            "action": "block_new_entries",
            "reason": f"{strategy_state['open_positions']} open, max {breaker['max_open_positions']}"
        })

    return triggered
```

## Level 3: Account Circuit Breakers

**These are the kill switches. They must be HARD stops — no overrides, no "this time is different."**

```python
ACCOUNT_BREAKERS = {
    "max_daily_loss": 2000,          # HARD daily loss limit
    "max_weekly_loss": 5000,         # HARD weekly loss limit
    "max_monthly_loss": 15000,       # HARD monthly loss limit
    "max_drawdown_from_high": 0.20,  # Account drawdown from peak
    "max_drawdown_review": 0.10,     # Review but don't kill
    "max_drawdown_reduce": 0.20,     # Close 50% of positions
    "max_drawdown_kill": 0.30,       # Close ALL positions. Stop automation.
    "max_consecutive_losing_days": 5,
    "max_correlation": 0.80,         # Max portfolio correlation
    "min_buying_power": 0.30,        # Don't use more than 70% of buying power
}
```

### Account Breaker Logic

```python
def check_account_breakers(account_state):
    """Check account-level circuit breakers. These are HARD KILL SWITCHES."""
    triggered = []

    # Drawdown circuit breakers (cascading severity)
    dd = account_state["drawdown_from_high"]

    if dd >= ACCOUNT_BREAKERS["max_drawdown_kill"]:
        triggered.append({
            "breaker": "max_drawdown_kill",
            "action": "liquidate_all_and_stop",
            "severity": "CRITICAL",
            "reason": f"Account drawdown {dd:.1%} reached kill threshold ({ACCOUNT_BREAKERS['max_drawdown_kill']:.0%})"
        })
    elif dd >= ACCOUNT_BREAKERS["max_drawdown_reduce"]:
        triggered.append({
            "breaker": "max_drawdown_reduce",
            "action": "close_50pct_positions",
            "severity": "HIGH",
            "reason": f"Account drawdown {dd:.1%} — reducing exposure"
        })
    elif dd >= ACCOUNT_BREAKERS["max_drawdown_review"]:
        triggered.append({
            "breaker": "max_drawdown_review",
            "action": "pause_new_entries",
            "severity": "MEDIUM",
            "reason": f"Account drawdown {dd:.1%} — review threshold"
        })

    # Daily loss limit
    if account_state["daily_pnl"] < -ACCOUNT_BREAKERS["max_daily_loss"]:
        triggered.append({
            "breaker": "max_daily_loss",
            "action": "close_all_and_pause",
            "severity": "CRITICAL",
            "reason": f"Daily loss ${abs(account_state['daily_pnl']):.0f}"
        })

    # Weekly loss limit
    if account_state["weekly_pnl"] < -ACCOUNT_BREAKERS["max_weekly_loss"]:
        triggered.append({
            "breaker": "max_weekly_loss",
            "action": "close_all_and_pause_week",
            "severity": "CRITICAL",
            "reason": f"Weekly loss ${abs(account_state['weekly_pnl']):.0f}"
        })

    # Consecutive losing days
    if account_state["consecutive_losing_days"] >= ACCOUNT_BREAKERS["max_consecutive_losing_days"]:
        triggered.append({
            "breaker": "max_consecutive_losing_days",
            "action": "pause_new_entries_3days",
            "severity": "HIGH",
            "reason": f"{account_state['consecutive_losing_days']} consecutive losing days"
        })

    return triggered
```

## Level 4: Market Circuit Breakers

```python
MARKET_BREAKERS = {
    "vix_spike": {"threshold": 30, "action": "halve_position_sizes"},
    "vix_crash": {"threshold": 40, "action": "close_short_vol_positions"},
    "vix_emergency": {"threshold": 50, "action": "close_all_positions"},
    "spy_below_200sma": {"action": "no_long_entries"},
    "spy_below_200sma_5pct": {"action": "close_all_long_positions"},
    "rate_hike_day": {"action": "no_new_entries"},
    "market_wide_circuit_breaker": {"action": "pause_all_automation"},
}

def check_market_breakers(market_data):
    """Check market-level conditions."""
    triggered = []

    vix = market_data["vix"]
    spy = market_data["spy"]

    # VIX-based breakers
    if vix > 50:
        triggered.append({
            "breaker": "vix_emergency",
            "action": "close_all_positions",
            "severity": "CRITICAL",
            "reason": f"VIX at {vix} — emergency conditions"
        })
    elif vix > 40:
        triggered.append({
            "breaker": "vix_crash",
            "action": "close_short_vol_positions",
            "severity": "HIGH",
            "reason": f"VIX at {vix} — closing short vol"
        })
    elif vix > 30:
        triggered.append({
            "breaker": "vix_spike",
            "action": "halve_position_sizes",
            "severity": "MEDIUM",
            "reason": f"VIX at {vix} — reducing exposure"
        })

    # SPY trend breakers
    if spy < market_data["spy_200sma"]:
        triggered.append({
            "breaker": "spy_below_200sma",
            "action": "no_long_entries",
            "severity": "MEDIUM",
            "reason": f"SPY ${spy:.0f} below 200SMA ${market_data['spy_200sma']:.0f}"
        })

    return triggered
```

## Circuit Breaker Action Matrix

| Breaker | Action | Scope | Duration | Recovery Condition |
|---------|--------|-------|----------|-------------------|
| Position max loss | Close position | Single position | Permanent for this setup | New setup signal |
| Position drawdown | Close position | Single position | Permanent for this position | New setup signal |
| Strategy consecutive losses | Pause strategy | Strategy only | 24 hours | Manual review or auto after timeout |
| Strategy daily loss | Pause strategy (today) | Strategy only | End of day | Next trading day |
| Account daily loss | Close all, pause | Full account | Today | Next trading day |
| Account drawdown -10% | Pause new entries | Full account | Until dd < 5% | Review and approve |
| Account drawdown -20% | Close 50%, pause | Full account | 1 week minimum | Review + manual restart |
| Account drawdown -30% | LIQUIDATE ALL. STOP. | Full account | Indefinite | Manual restart ONLY |
| VIX > 30 | Halve position sizes | Full account | Until VIX < 25 | VIX drops below 25 |
| VIX > 40 | Close short vol | Full account | Until VIX < 35 | VIX stabilizes |
| SPY < 200SMA | No long entries | Full account | Until SPY > 200SMA | SPY reclaims 200SMA |
| Market circuit breaker (NYSE) | Pause all | Full account | 30 min after resume | Market reopens |

## Implementation Pattern

```python
def safety_gate(order_intent):
    """THE GATE. Every order must pass through here before execution."""

    # 1. Check market breakers first (cheapest)
    market_breakers = check_market_breakers(get_market_data())
    if any(b["severity"] == "CRITICAL" for b in market_breakers):
        log_breaker_event(market_breakers)
        raise CircuitBreakerTriggered("Market-level CRITICAL breaker active")

    # 2. Check account breakers
    account_breakers = check_account_breakers(get_account_state())
    critical_account = [b for b in account_breakers if b["severity"] == "CRITICAL"]
    if critical_account:
        log_breaker_event(account_breakers)
        execute_breaker_actions(critical_account)
        raise CircuitBreakerTriggered("Account-level CRITICAL breaker active")

    # 3. Check strategy breakers
    strategy_breakers = check_strategy_breakers(
        order_intent.strategy_id, order_intent.strategy_type
    )
    if strategy_breakers:
        log_breaker_event(strategy_breakers)
        execute_breaker_actions(strategy_breakers)
        return {"status": "blocked", "reason": strategy_breakers}

    # 4. Apply market-level sizing adjustments
    sizing_adjustments = compute_sizing_adjustments(market_breakers, account_breakers)
    adjusted_order = apply_sizing(order_intent, sizing_adjustments)

    # 5. Log the gate passage
    log_audit("safety_gate_passed", {
        "order": adjusted_order,
        "market_breakers": market_breakers,
        "account_breakers": account_breakers,
    })

    return {"status": "approved", "order": adjusted_order}
```

## Audit Trail Requirements

Every breaker trigger must be logged with:

```python
breaker_event = {
    "timestamp": "ISO8601",
    "breaker_level": "position|strategy|account|market",
    "breaker_name": "max_daily_loss",
    "severity": "MEDIUM|HIGH|CRITICAL",
    "action": "close_all_and_pause",
    "reason": "Daily loss $2,450 exceeds $2,000 limit",
    "account_state_snapshot": {
        "daily_pnl": -2450.00,
        "drawdown": -0.08,
        "open_positions": 7,
        "buying_power_used": 0.55,
    },
    "market_state_snapshot": {
        "vix": 22.5,
        "spy": 478.50,
    },
}
```

## Recovery Protocol

After a circuit breaker triggers:

1. **Document the event.** What triggered it? What was the state?
2. **Do NOT immediately restart.** Wait for the cooling-off period.
3. **Review the strategy.** Was the breaker a false positive or a genuine problem signal?
4. **Adjust parameters if needed.** If breakers keep triggering, the strategy or sizing is wrong.
5. **Restart with reduced size.** After a drawdown breaker, start at 50% of normal size for 1 week.
6. **Escalate if repeated.** If the same breaker triggers 3× in a month, retire the strategy.

## Summary

Circuit breakers are not suggestions. They are hard stops that prevent automation from turning a bad day into a catastrophic one. The automation system must treat breaker violations as non-negotiable — no override, no exception, no "just one more trade."

**The automation that ignores its own circuit breakers is worse than no automation at all.**
