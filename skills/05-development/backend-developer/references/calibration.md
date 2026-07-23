# Calibration — How to Know Your Level

<!-- STANDARD: 3min — honest self-assessment rubric -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You can build an endpoint but don't know what happens when 10,000 users hit it simultaneously | You load-test your endpoints before deployment and can name the bottleneck (DB query, serialization, connection pool) from the flame graph | You design a system architecture and 6 months later, it handles 10× the original traffic with no major rewrites |
| You use `try/catch` but don't differentiate between retryable errors (network timeout) and non-retryable errors (validation failure) | You implement circuit breakers, retry with exponential backoff + jitter, and graceful degradation for every external dependency | You can look at a production incident and identify whether the fix needs to be in the code, the infrastructure, or the architecture — and you're right |
| You copy-paste error handling patterns without understanding why one endpoint returns 400 vs 409 vs 422 | You have a consistent error response format with unique error codes that the frontend team can programmatically handle | You define org-wide error handling standards and the teams that adopt them see 40% fewer P1 incidents |

**The Litmus Test:** Can you write a production service from scratch — routing, middleware, error handling, connection pooling, health checks, graceful shutdown — using only the standard library and a database driver? If you need a framework to get started, you're not L3 yet.
