# REST API Design Rules

## Resource Naming

### Collection Resources
```
✅ GET    /api/v1/users              # List users
✅ GET    /api/v1/users/{id}         # Get single user
✅ POST   /api/v1/users              # Create user
✅ PUT    /api/v1/users/{id}         # Replace user
✅ PATCH  /api/v1/users/{id}         # Partial update
✅ DELETE /api/v1/users/{id}         # Delete user
```

### Sub-resources
```
✅ GET    /api/v1/users/{id}/orders                    # User's orders
✅ GET    /api/v1/users/{id}/orders/{orderId}/items    # Order items
```

### Naming Conventions
- Use **kebab-case** for URL paths: `/user-profiles`, `/shipping-addresses`
- Use **camelCase** for JSON fields: `createdAt`, `shippingAddress`
- Use **plural nouns** for collections: `/users` not `/user`
- Use **nouns, not verbs**: `/users` not `/getUsers`
- No trailing slashes: `/users` not `/users/`

### HTTP Methods — Correct Usage
| Method | Idempotent | Safe | Purpose |
|--------|-----------|------|---------|
| GET    | ✅ | ✅ | Retrieve |
| POST   | ❌ | ❌ | Create |
| PUT    | ✅ | ❌ | Full replace |
| PATCH  | ❌ | ❌ | Partial update |
| DELETE | ✅ | ❌ | Remove |
| HEAD   | ✅ | ✅ | Metadata |
| OPTIONS| ✅ | ✅ | Capabilities |

## HTTP Status Codes

### Success (2xx)
- `200 OK` — Standard success
- `201 Created` — Resource created (return Location header)
- `202 Accepted` — Async processing started
- `204 No Content` — Success with no body (DELETE, PUT)

### Client Error (4xx)
- `400 Bad Request` — Malformed input, validation failure
- `401 Unauthorized` — Missing/invalid authentication
- `403 Forbidden` — Authenticated but not authorized
- `404 Not Found` — Resource doesn't exist
- `409 Conflict` — Resource state conflict (optimistic locking)
- `422 Unprocessable Entity` — Semantic validation failure
- `429 Too Many Requests` — Rate limit exceeded

### Server Error (5xx)
- `500 Internal Server Error` — Unexpected failure
- `502 Bad Gateway` — Upstream failure
- `503 Service Unavailable` — Maintenance/overload
- `504 Gateway Timeout` — Upstream timeout

## Response Format

### Success
```json
{
  "data": { "id": "usr_123", "name": "Jane Doe" }
}
```

### Collection
```json
{
  "data": [...],
  "pagination": {
    "cursor": "opaque_cursor_string",
    "hasMore": true,
    "total": 1243
  }
}
```

### Error
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable description",
    "details": [
      { "field": "email", "message": "Invalid email format" }
    ],
    "requestId": "req_abc123"
  }
}
```

## Versioning

- **URL path versioning** (preferred): `/api/v1/users`
- **Header versioning**: `Accept: application/vnd.api+json;version=1`
- Never use query params: `/users?version=1` ❌
- Deprecation: `Sunset` + `Deprecation` headers with migration docs link

## Pagination

- **Cursor-based** (preferred for scale): `?cursor=xxx&limit=50`
- **Offset-based** (acceptable for small datasets): `?offset=0&limit=50`
- **Page-based** (legacy): `?page=1&per_page=50`
- Max limit: 100 items per page

## Filtering, Sorting, Searching

```
GET /api/v1/users?status=active&role=admin          # Filtering
GET /api/v1/users?sort=-createdAt,+name             # Sorting (- for desc)
GET /api/v1/users?q=john                            # Full-text search
GET /api/v1/users?fields=id,name,email              # Sparse fieldsets
```

## Rate Limiting Headers

```
RateLimit-Limit: 1000
RateLimit-Remaining: 987
RateLimit-Reset: 1623456789
Retry-After: 60
```

## Authentication

- **Bearer token**: `Authorization: Bearer <jwt>`
- **API Key**: `X-API-Key: <key>` or `Authorization: ApiKey <key>`
- Always use HTTPS — never accept API keys over HTTP
