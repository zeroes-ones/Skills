# Circuit Breaker Design

## State Machine

```

CLOSED (normal operation)
   │
   ├── Success: stay CLOSED
   └── Failure: increment failure_count
       └── failure_count >= threshold → OPEN

OPEN (requests blocked)
   │
   └── After timeout (5 min) → HALF_OPEN

HALF_OPEN (testing)
   │
   ├── Heartbeat succeeds → CLOSED (reset failure_count)
   └── Heartbeat fails → OPEN (reset timeout)

```

## Threshold Configuration

| Dependency Type | Failure Threshold | Open Duration | Half-Open Test |
|----------------|-------------------|---------------|----------------|
| Critical (pipeline cannot proceed) | 3 failures in 60s | 2 minutes | Heartbeat request with 10s timeout |
| Important (can degrade) | 5 failures in 120s | 5 minutes | Heartbeat + 1 real request |
| Optional (nice-to-have) | 10 failures in 300s | 15 minutes | Single heartbeat |

## Failure Definition

| Failure Mode | Counts As |
|-------------|-----------|
| Timeout (no response within deadline) | 1 failure |
| Malformed response (schema validation fails) | 1 failure |
| Error response (skill returns error) | 1 failure |
| Partial response (incomplete data) | 0.5 failure (2 partials = 1 full failure) |

## Monitoring Integration

```

Alert when:
├── Any circuit breaker transitions CLOSED → OPEN: "Circuit open for {skill}"
├── Circuit stays OPEN > 15 minutes: "Extended outage for {skill}"
├── Circuit opens 3+ times in 24 hours: "Flapping circuit: {skill}"
└── Multiple circuits open simultaneously (>3): "Systemic communication failure"

```
