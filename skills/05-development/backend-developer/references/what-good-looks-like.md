# What Good Looks Like — Full Quality Standard

Every endpoint is contract-first, validated at the boundary, and fully documented. Authentication is airtight — JWTs validated, RBAC enforced, secrets never leaked. The database hums with connection pooling, indexed queries, and targeted caching that keeps p95 latency under 200ms. Async tasks are idempotent, retried with exponential backoff, and monitored via dead-letter queues. Structured logs carry correlation IDs from ingress to response, and health checks report green before users notice anything wrong. The service ships with confidence — migrations are backward-compatible, rollback plans are tested, and load tests pass at 2× peak QPS.

> This is the full aspirational quality standard. The compressed version in SKILL.md is optimized for model token budgets.
