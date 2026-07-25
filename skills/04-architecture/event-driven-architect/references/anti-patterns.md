## Anti-Patterns

| ❌ Anti-Pattern | ✅ Do This Instead |
|----------------|-------------------|
| Publishing CDC as business events: `{"table":"users","op":"UPDATE","data":{...}}` | Publish domain events: `UserEmailChanged {user_id, old_email, new_email}`. CDC is for replication. |
| Events as commands: `PlaceOrder` (imperative) | Events are past-tense facts: `OrderPlaced`. If rejectable, it's a command. |
| Single mega-topic for all events | One topic per event type or bounded context. |
| Sync HTTP in event handler without circuit breaker | Publish event, let next handler consume. If sync is unavoidable: circuit breaker + 5s timeout. |
| Infinite retry without DLQ | Max 3 retries + exponential backoff -> DLQ -> alert. |
| Event sourcing without snapshots | Snapshot every N events (e.g., 1000). Cold start: 2s instead of 45 min. |
| Same schema for internal + external events | External events get separate, stable, documented schemas. |
| Hard-deleting events from event store for GDPR | Crypto-shred: encrypt PII with per-user key, delete the key. History preserved, PII unrecoverable. |
