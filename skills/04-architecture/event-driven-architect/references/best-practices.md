## Best Practices

1. **One event type per topic/queue** — Mixing forces filtering, breaks ordering.
2. **Partition by business key** — `order_id` ensures ordering. RabbitMQ: consistent hash exchange.
3. **Idempotency key = business key + version** — `order-12345-placed-v1`. Never timestamp alone.
4. **Events are immutable** — Publish correction event (`OrderCorrected`), never modify original.
5. **Keep events < 1MB** — Large payloads in S3/GCS with URL reference.
6. **Consumer groups for scaling** — 1 consumer per partition max (Kafka). Competing consumers (RabbitMQ).
7. **Monitor consumer lag** — Kafka: `consumer-groups --describe`. Lag >1000 or >30s = incident.
8. **Test schema evolution in CI** — Consumer v1 reads producer v2, consumer v2 reads producer v1.
9. **Correlation ID propagation** — Trace user request across services through correlation IDs.
10. **Time-bound consistency** — Define p95 staleness. <200ms = users won't notice. >5s = they will.
