# Best Practices

<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Spec-first, not code-first**: OpenAPI spec is the source of truth; generate server stubs and client SDKs from it.
- **Naming consistency**: camelCase for JSON properties, kebab-case for headers and query params, UPPER_SNAKE for enum values.
- **Use HTTP semantics correctly**: GET (safe, idempotent), PUT (idempotent replace), PATCH (partial update), POST (create), DELETE (idempotent).
- **Rate limiting headers**: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`, `Retry-After`.
- **HATEOAS links** where practical: include `_links` in responses for discoverability and self-documenting APIs.
- **SDK generation**: Use OpenAPI Generator or fern for multi-language SDKs; publish to package registries (npm, PyPI, Maven).
- **Contract testing**: Use Pact or Spring Cloud Contract to verify API compatibility between services.
