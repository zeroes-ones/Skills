# Portfolio-Level Circuit Breakers

## Breaker Catalog

| Breaker | Threshold | Action | Reset |
|---------|-----------|--------|-------|
| Rejected Order Surge | >5 in 60 seconds | HALT all orders | Manual after investigation |
| Stop-Loss Cascade | >3 stops hit in 1 session | HALT new positions. Tighten all stops. | Manual + strategy review |
| P&L Shock | >$5,000 unrealized swing in <5 min | PAUSE new orders. Check news feed. | Auto after 15 min calm |
| Margin Call | Any margin call | IMMEDIATE reduction. Sell weakest 50%. | Manual + margin review |
| API Error Rate | >10% of requests fail | HALT. Connection check. | Manual after connectivity restored |
| Price Gap on Position | >3 ATR gap at open | Close position at market. | Manual post-mortem |
| Consecutive Losing Days | 5 days with negative P&L | Reduce size 50%. Review strategy. | Strategy review complete |

## Testing Protocol

Test each breaker:
1. Simulate trigger condition in paper trading
2. Verify breaker fires
3. Verify action executed correctly
4. Verify reset procedure works
5. Document test results
