# Footguns — War Stories from Production Marketplace Platform Builder

<!-- DEEP: 10+min -- war stories from production systems -->

| Footgun | What Happened | Root Cause | How to Prevent |
|---|---|---|---|
| "It works on my machine" | Works in dev, fails in production. Different Node version, OS, env vars, DB version. | No staging environment mirroring production. SQLite vs PostgreSQL differences. | Docker for identical environments. Test with production-like data. |
| The midnight deployment | Deployed at 11 PM, woke up to angry emails. Migration worked in staging with 100 rows, timed out with 10M rows in prod. | Migration untested at scale. No monitoring. No plan for large tables. | Test migrations at production scale. Batch process large tables. Never deploy then go offline. |
| The cascade failure | One service down cascaded to 20+ services. Entire system down in 30 seconds. | No circuit breakers. Services assumed dependencies always available. | Circuit breakers on all external deps. Graceful degradation. Chaos engineering. |
| The 3 AM alert nobody could fix | Alert at 3 AM. 2 hours debugging. Self-resolved by morning. Root cause never found. | Insufficient logging. No correlation IDs between services. | Structured logging with correlation IDs. Every error logs: what, when, where, who. |
| The "quick fix" that stayed 2 years | TODO: fix this properly with hacky workaround. Now critical infrastructure. | No tech debt tracking. TODOs invisible until they cause problems. | Every TODO references a ticket. Sprint TODO audit. If worth commenting, worth ticketing. |
