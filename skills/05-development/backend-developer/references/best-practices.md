# Best Practices

<!-- STANDARD: 3min -- rules extracted from production experience -->
- **API contract first**: Design the API before writing code. Share with consumers. Use OpenAPI.
- **Fail fast, fail loud**: Validate at boundaries. Invalid data should never reach business logic.
- **Idempotency for mutations**: Every POST/PUT/PATCH that affects state should be idempotent via idempotency keys.
- **Observability from day one**: Structured logging (JSON), request IDs on every log line, health checks.
- **Database per service** (if microservices): Never share databases across services. API is the contract.
- **Connection pooling**: Always pool database connections. Set statement timeout and idle-in-transaction timeout.
- **Migrate forward, rollback tested**: Every migration has a tested reversal. Expand-contract for zero-downtime schema changes.
