## Error Decoder

| Error Message | Root Cause | Fix | Lesson |
|--------------|------------|-----|--------|
| `UNKNOWN_TOPIC_OR_PARTITION` | Topic doesn't exist, auto-create disabled | Create topic in IaC before deploy: `kafka-topics --create --topic orders --partitions 12 --rf 3` | Disable auto-create in production. Pre-create in IaC. |
| `NOT_LEADER_FOR_PARTITION` | Producer connected to non-leader broker | Refresh metadata. If persistent, leader election failed — check broker health. | Handle transient metadata staleness in producers. |
| `RecordTooLargeException` | Payload > `max.message.bytes` (1MB default) | Move large data to S3, include URL. Increase limit only as last resort. | Kafka is not a file transfer system. |
| `DUPLICATE_KEY` in consumer DB | At-least-once without idempotency | `INSERT ON CONFLICT (idempotency_key) DO NOTHING RETURNING result` | Every at-least-once consumer needs idempotency. |
| `IncompatibleSchemaException` | Schema not registered or breaks compatibility | Register before producer deploy. BACKWARD compatibility. Test in CI. | Schema-first: register -> deploy producer -> deploy consumer. |
| Consumer stuck, not processing | Poisoned message retrying infinitely | Configure max retries (3) + DLQ. Reset offset past poison message if needed. | DLQ is day-zero infrastructure. |
