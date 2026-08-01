# Monitoring & Observability for Options Automation

> **Portability target:** Spec-level. Metric definitions are universal — adapt monitoring stack to any infrastructure (Prometheus, Datadog, CloudWatch, custom).

## The Rule

**If your automated options system doesn't have monitoring, it doesn't exist.** You cannot manage what you cannot measure. An automated system that trades silently is more dangerous than a manual trader with no plan.

## Core SLIs (Service Level Indicators)

| SLI | Definition | Target | Alert Threshold |
|-----|-----------|--------|-----------------|
| Scanner Freshness | `now() - last_scan_completion_time` | < 30 seconds | > 120 seconds — data is stale |
| Order Latency | `fill_time - order_submit_time` | < 500ms | > 2 seconds — market has moved |
| Fill Rate | `filled_orders / (filled + cancelled + rejected)` | > 85% | < 70% — routing/sizing problem |
| Circuit Breaker Status | `breakers_active / total_breakers` | 0 (none tripped) | > 0 — system partially or fully halted |
| API Health | `successful_api_calls / total_api_calls` | > 99% | < 95% — broker connectivity degrading |
| Position Drift | `actual_position_delta - target_position_delta` | < $500 delta | > $2,000 delta — positions unmanaged |

## Dashboard: What to Watch

Every automated options system needs one dashboard with these panels:

1. **System Status:** Green/Yellow/Red. Green = all systems nominal, trades flowing. Yellow = warning (stale data, elevated latency, partial fill rate below target). Red = circuit breaker tripped OR API disconnected > 60 seconds.

2. **Active Positions:** Current positions with unrealized P&L, Greeks summary, days to expiration, adjustment count. Auto-sort by P&L % (worst first).

3. **Today's Activity:** Orders placed, filled, cancelled, rejected. P&L realized today. Commissions paid. Circuit breaker events (if any).

4. **Execution Quality:** Fill-to-mid spread (avg today, 5-day avg, 30-day avg). Time-to-fill distribution. Slippage by strategy.

5. **Risk Gauges:** Notional exposure % of account. Net delta. Net theta. Vega exposure. Correlation (are all positions moving together?).

## Alert Rules

| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Data Stale | Scanner freshness > 120s | CRITICAL | Halt new orders. Reconnect. Resume only after 60s of fresh data. |
| High Fill Slippage | Avg fill-to-mid > 5% across 10+ orders today | WARNING | Check broker routing. May indicate market-wide spread widening or routing degradation. |
| API Disconnect | Last successful API call > 60s | CRITICAL | Emergency reconnect. After 120s → trigger circuit breaker. |
| Max Daily Loss | Realized loss today ≥ max_daily_loss | CRITICAL | Trigger circuit breaker. Close all positions. System offline until manual review. |
| Position Drift | Delta drift > $2,000 | WARNING | Reconcile positions against broker. May indicate missed fill or partial execution. |
| Roll Limit | Any trade at 2 rolls and approaching DTE threshold | INFO | Pre-warning: trade will be closed at next threshold if unable to roll profitably. |
| VIX Spike | VIX > +20% intraday | WARNING | Halve all sizes. Suspend new premium-selling entries. |

## Logging Level Guidelines

| Level | What to Log | Retention |
|-------|------------|-----------|
| ERROR | Circuit breaker trips, API failures, order rejections, state machine illegal transitions, data corruption | 90 days |
| WARNING | Partial fills, elevated slippage (> 3% fill-to-mid), roll limit approaching, stale data < 120s | 30 days |
| INFO | State transitions, order submissions/fills/cancellations, strategy signals, scanner completions | 14 days |
| DEBUG | Scanner detail (every ticker, every filter result), API request/response bodies, Greek calculations | 3 days |

## Healthcheck Endpoint

Every automated system must expose a healthcheck:

```python
@app.get("/health")
def healthcheck():
    return {
        "status": "healthy" if all_checks_pass() else "degraded",
        "checks": {
            "broker_api": broker_api.ping(),
            "market_data": market_data_stream.is_connected(),
            "circuit_breakers": circuit_breaker.status(),
            "scanner_freshness": scanner.seconds_since_last_scan(),
            "open_orders": len(order_manager.get_open_orders()),
        },
        "uptime_seconds": time.time() - start_time,
    }
```

## The Overnight Check

Before leaving the system unattended:

- [ ] Dashboard: all panels green
- [ ] Healthcheck: status = "healthy"
- [ ] No open orders older than 5 minutes (stuck order detection)
- [ ] All positions have defined exit triggers
- [ ] Circuit breakers: all armed, zero tripped
- [ ] Enough buying power for tomorrow's expected entries
- [ ] Alert notifications: test alert sent and received
