# MCP Broker Integration — Full State Machine

## 8 States

```

DISCONNECTED → AUTHENTICATING → CONNECTED → SYNCING → READY → EXECUTING → RECONCILING → DISCONNECTED

```

## State Transitions

| From | To | Trigger |
|------|----|---------|
| DISCONNECTED | AUTHENTICATING | User initiates connection |
| AUTHENTICATING | CONNECTED | OAuth/API key validated |
| AUTHENTICATING | DISCONNECTED | Auth failed 3x |
| CONNECTED | SYNCING | WebSocket established |
| SYNCING | READY | Positions + orders + account synced |
| SYNCING | DISCONNECTED | Sync timeout >60s |
| READY | EXECUTING | Order submitted |
| EXECUTING | RECONCILING | Fill received |
| EXECUTING | READY | Order rejected (known reason) |
| RECONCILING | READY | Reconciliation complete |
| Any | DISCONNECTED | WebSocket disconnect, token expiry, rate limit |

## Error Handling Per Broker

| Broker | Auth Method | Rate Limit | Known Issues |
|--------|------------|------------|--------------|
| Alpaca | API Key + Secret | 200/min | Paper and live use different endpoints |
| IBKR | OAuth + Gateway | Varies | Gateway must be running locally |
| Schwab | OAuth | 120/min | Token refresh every 30 min |
| Robinhood | OAuth | 100/min | No official API; use with caution |
