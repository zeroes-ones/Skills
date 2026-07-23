# Scale Depth: Solo → Small → Medium → Enterprise

### Solo (1 person, 0-100 users)
- **What changes**: API = simple REST endpoints in your framework (FastAPI, Express). No OpenAPI spec (generate from code). No versioning. No pagination. No rate limiting. Auth = a simple API key or session cookie.
- **What to skip**: OpenAPI spec-first. GraphQL. gRPC. API versioning. Rate limiting. SDK generation. Pagination. Idempotency keys.
- **Coordination**: You own client + server. Change API whenever needed.

### Small Team (2-10 people, 100-10K users)
- **What changes**: OpenAPI 3.1 spec (code-first or spec-first). REST with proper HTTP semantics. Cursor-based pagination for large lists. Basic rate limiting (100 req/min per user). JWT authentication. Error responses follow RFC 7807. Health check endpoint. Interactive docs (Swagger UI).
- **What to skip**: GraphQL (REST is fine). gRPC (unless internal service-to-service). API versioning (<100 consumers). SDK generation (consumers read OpenAPI). Idempotency keys (add when payments involved).
- **Coordination**: API design review in eng sync. OpenAPI spec in shared repo. Breaking changes communicated in Slack.

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: Spec-first OpenAPI with code generation. API versioning (URL path). GraphQL for complex client needs. gRPC for internal service-to-service. Tiered rate limiting with headers. Idempotency keys for all mutating endpoints. SDK generation (TypeScript, Python, Go). API changelog + deprecation policy (6 months). API gateway for routing + auth.
- **What to skip**: gRPC-web (unless need streaming in browser). Full HATEOAS. Multiple API gateway layers.
- **Coordination**: API design RFC process. Monthly API review. Deprecation calendar published. SDK release coordination with consumers.

### Enterprise (50+ people, 1M+ users)
- **What changes**: API platform team. Multi-protocol (REST + GraphQL + gRPC + WebSocket). API gateway with developer portal. API analytics (usage, latency, errors per consumer). Rate limiting with dynamic quotas. API versioning with automated migration tooling. SDKs for 5+ languages with CI/CD. API style guide. API linting in CI (Spectral). Contract testing (Pact). API product management.
- **What's full production**: API platform as a product. Developer portal with onboarding. API analytics dashboard. Automated breaking change detection. API consumer communication pipeline.
- **Coordination**: API platform team weekly. API design review board bi-weekly. Consumer office hours monthly. Breaking change notification pipeline.

### Transition Triggers
- **Solo → Small**: Second consumer of your API (frontend team or external). Need documented contract.
- **Small → Medium**: >100 API consumers or external developers. First breaking change requires versioning.
- **Medium → Enterprise**: >1000 API consumers. Multi-product API surface. Developer portal needed.
