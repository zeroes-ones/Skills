# Orchestra Platform — API Design Summary

## API Strategy

Orchestra exposes a hybrid API surface: **REST (OpenAPI 3.1)** for resource-oriented CRUD operations and **GraphQL** for flexible, consumer-driven catalog queries. Both are served through the Next.js BFF gateway at `api.orchestra.dev`.

## REST Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| `POST` | `/v1/catalog/services` | Register a new service in the catalog | JWT |
| `GET` | `/v1/catalog/services` | List services with filters (`?team=`, `?language=`, `?owner=`) | JWT |
| `GET` | `/v1/catalog/services/{id}` | Get a single service with full metadata | JWT |
| `PATCH` | `/v1/catalog/services/{id}` | Update service ownership or metadata | JWT |
| `DELETE` | `/v1/catalog/services/{id}` | Remove a service (soft-delete, 30-day grace) | JWT |
| `POST` | `/v1/templates/execute` | Trigger template execution (returns `202 Accepted`) | JWT |
| `GET` | `/v1/templates/{id}/status` | Poll template execution status | JWT |
| `GET` | `/v1/plugins` | List available plugins with compatibility info | JWT |
| `POST` | `/v1/plugins/{id}/install` | Install a plugin on the current organization | JWT (Admin) |
| `POST` | `/v1/auth/login` | Exchange credentials for JWT pair | None |
| `POST` | `/v1/auth/refresh` | Exchange refresh token for new JWT | Refresh Token |
| `POST` | `/v1/api-keys` | Create a service account API key | JWT (Admin) |

## GraphQL Queries

```graphql
type Query {
  serviceCatalog(filter: ServiceFilter, pagination: CursorInput): ServiceConnection!
  templateUsage(serviceId: ID!, range: DateRange): [TemplateExecution!]!
  pluginCompatibility(pluginId: ID!): CompatibilityMatrix!
}
```

GraphQL is used specifically for read-heavy, multi-entity queries where clients need to fetch service details, associated templates, active plugins, and team ownership in a single round-trip without over-fetching.

## Versioning Policy

All REST endpoints are URL-prefixed (`/v1/`). Breaking changes ship under a new major version (`/v2/`). Deprecated endpoints remain available for **6 months** after a deprecation notice, communicated via the `Sunset` HTTP header and the developer changelog.

## Pagination

Cursor-based pagination for all list endpoints. The response envelope:

```json
{
  "data": [...],
  "pagination": {
    "next_cursor": "eyJvZmZzZXQiOiAxMDB9",
    "has_more": true,
    "total": 1247
  }
}
```

Maximum page size is 100 items. Requests exceeding this receive a `400 Bad Request`.

## Rate Limiting

- **Default:** 1,000 requests per minute per API key / authenticated user
- **Template execution:** 60 executions per minute per organization (to prevent runaway costs)
- Rate-limited responses return `429 Too Many Requests` with a `Retry-After` header (seconds)
- Rate limit headers (`X-RateLimit-*`) included on every response

## Error Format

All errors follow [RFC 7807 Problem Details](https://datatracker.ietf.org/doc/html/rfc7807):

```json
{
  "type": "https://api.orchestra.dev/errors/validation-error",
  "title": "Validation Error",
  "status": 422,
  "detail": "The 'name' field is required for service creation.",
  "instance": "/v1/catalog/services",
  "errors": [
    {"field": "name", "message": "required"}
  ]
}
```

## Authentication

- **Human users:** JWT with RS256 signing. Access tokens expire in 15 minutes; refresh tokens last 7 days and are rotated on each use.
- **Service accounts:** Long-lived API keys (`orchestra_key_...` prefix), revocable via the admin dashboard.
- **CORS:** Whitelist of approved origins only (customer dashboard, CLI tool). Wildcard origins are rejected.
