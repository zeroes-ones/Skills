---
title: Create User
description: Creates a new user in the system with the specified attributes.
sidebar_position: 1
---

# Create User

> Full API reference for the `POST /api/v1/users` endpoint. Creates a new user account and returns the created user object.

---

## Endpoint

```
POST /api/v1/users
```

| Property | Value |
|---|---|
| **Method** | `POST` |
| **URL** | `https://api.example.com/api/v1/users` |
| **Authentication** | Required (Bearer token) |
| **Rate Limit** | 100 requests per minute per token |
| **Idempotent** | No (each call creates a new resource) |

---

## Request Parameters

### Path Parameters

None.

### Query Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `include` | `string` | No | — | Comma-separated list of related resources to include. Supported: `roles`, `permissions`, `profile` |

### Headers

| Header | Type | Required | Description |
|---|---|---|---|
| `Authorization` | `string` | Yes | Bearer token. Format: `Bearer <token>` |
| `Content-Type` | `string` | Yes | Must be `application/json` |
| `Idempotency-Key` | `string` | No | UUID v4. Prevents duplicate user creation. Expires after 24 hours. |
| `Accept-Language` | `string` | No | Locale for error messages. Supported: `en`, `fr`, `zh-CN`. Default: `en` |

### Body

```json
{
  "email": "string (required) - User's email address. Must be unique. Max 255 chars.",
  "name": "string (required) - User's full name. Max 100 chars.",
  "password": "string (conditional) - Required if no SSO provider specified. Min 8 chars, must include uppercase, lowercase, number.",
  "role": "string (optional) - User role. Allowed: 'member', 'admin', 'viewer'. Default: 'member'.",
  "metadata": "object (optional) - Arbitrary key-value pairs. Max 10 keys, values max 500 chars each.",
  "sso_provider": "string (conditional) - SSO provider ID. Required if password omitted.",
  "tags": "array[string] (optional) - User tags. Max 5 tags, each max 50 chars."
}
```

#### Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| `email` | `string` | Yes | User's email address. Must be a valid email format. Unique across all users. Max 255 characters. |
| `name` | `string` | Yes | User's full display name. Max 100 characters. |
| `password` | `string` | Conditional | Required when `sso_provider` is not provided. Must include uppercase, lowercase, and a number. Min 8 characters. |
| `role` | `enum` | No | `member` (default), `admin`, or `viewer`. |
| `metadata` | `object` | No | Arbitrary key-value metadata. Keys are strings, values are strings. Max 10 keys, values max 500 chars. |
| `sso_provider` | `string` | Conditional | SSO provider identifier. Required when `password` is not provided. |
| `tags` | `array[string]` | No | List of tags for categorization. Max 5 tags, each max 50 characters. |

---

## Request Examples

### curl

```bash
curl -X POST https://api.example.com/api/v1/users \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..." \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: a1b2c3d4-e5f6-7890-abcd-ef1234567890" \
  -d '{
    "email": "jane.doe@example.com",
    "name": "Jane Doe",
    "password": "SecurePass123!",
    "role": "member",
    "tags": ["engineering", "api-users"]
  }'
```

### Python

```python
import requests

url = "https://api.example.com/api/v1/users"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIs...",
    "Content-Type": "application/json",
    "Idempotency-Key": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
}
payload = {
    "email": "jane.doe@example.com",
    "name": "Jane Doe",
    "password": "SecurePass123!",
    "role": "member",
    "tags": ["engineering", "api-users"],
}

response = requests.post(url, headers=headers, json=payload)
print(response.status_code)
print(response.json())
```

### JavaScript

```javascript
const response = await fetch('https://api.example.com/api/v1/users', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIs...',
    'Content-Type': 'application/json',
    'Idempotency-Key': 'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
  },
  body: JSON.stringify({
    email: 'jane.doe@example.com',
    name: 'Jane Doe',
    password: 'SecurePass123!',
    role: 'member',
    tags: ['engineering', 'api-users'],
  }),
});

const data = await response.json();
console.log(response.status, data);
```

### Go

```go
package main

import (
  "bytes"
  "encoding/json"
  "fmt"
  "net/http"
)

func main() {
  url := "https://api.example.com/api/v1/users"
  payload := map[string]interface{}{
    "email":    "jane.doe@example.com",
    "name":     "Jane Doe",
    "password": "SecurePass123!",
    "role":     "member",
    "tags":     []string{"engineering", "api-users"},
  }
  body, _ := json.Marshal(payload)

  req, _ := http.NewRequest("POST", url, bytes.NewBuffer(body))
  req.Header.Set("Authorization", "Bearer eyJhbGciOiJIUzI1NiIs...")
  req.Header.Set("Content-Type", "application/json")

  client := &http.Client{}
  resp, _ := client.Do(req)
  defer resp.Body.Close()

  var result map[string]interface{}
  json.NewDecoder(resp.Body).Decode(&result)
  fmt.Println(resp.StatusCode)
  fmt.Println(result)
}
```

---

## Response Schema

### Success (201 Created)

| Field | Type | Description |
|---|---|---|
| `id` | `string` | Unique user ID (ulid format: `user_01G5...`) |
| `email` | `string` | User's email address |
| `name` | `string` | User's full name |
| `role` | `string` | Assigned role: `member`, `admin`, or `viewer` |
| `status` | `string` | Account status: `active`, `pending`, `suspended` |
| `metadata` | `object` | User metadata (null if not set) |
| `tags` | `array[string]` | User tags |
| `created_at` | `string` (ISO 8601) | Timestamp of user creation |
| `updated_at` | `string` (ISO 8601) | Timestamp of last update |

### Response Examples

#### 201 Created — Success

```json
{
  "id": "user_01H2X3Y4Z5ABC6DEF7GH8IJ9K",
  "email": "jane.doe@example.com",
  "name": "Jane Doe",
  "role": "member",
  "status": "active",
  "metadata": null,
  "tags": ["engineering", "api-users"],
  "created_at": "2026-07-21T12:00:00Z",
  "updated_at": "2026-07-21T12:00:00Z"
}
```

#### 400 Bad Request — Validation Error

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "One or more fields failed validation.",
    "details": [
      {
        "field": "email",
        "code": "invalid_format",
        "message": "Must be a valid email address."
      },
      {
        "field": "password",
        "code": "too_short",
        "message": "Password must be at least 8 characters."
      }
    ],
    "request_id": "req_9X8Y7Z6W5V4U3T2S1R"
  }
}
```

#### 401 Unauthorized — Missing or Invalid Token

```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Authentication required. Provide a valid Bearer token in the Authorization header.",
    "request_id": "req_A1B2C3D4E5F6G7H8I9J0"
  }
}
```

#### 404 Not Found — Related Resource Not Found

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "The specified SSO provider 'provider-xyz' does not exist.",
    "request_id": "req_K1L2M3N4O5P6Q7R8S9T0"
  }
}
```

#### 409 Conflict — Duplicate Email

```json
{
  "error": {
    "code": "CONFLICT",
    "message": "A user with email 'jane.doe@example.com' already exists.",
    "request_id": "req_U1V2W3X4Y5Z6A7B8C9D0"
  }
}
```

#### 422 Unprocessable Entity — Idempotency Key Replay

```json
{
  "error": {
    "code": "IDEMPOTENCY_REPLAY",
    "message": "This request is a replay of a previously processed request. The original response is returned.",
    "previous_response": {
      "id": "user_01H2X3Y4Z5ABC6DEF7GH8IJ9K",
      "status": "active"
    },
    "request_id": "req_E1F2G3H4I5J6K7L8M9N0"
  }
}
```

#### 429 Too Many Requests — Rate Limited

```json
{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Rate limit exceeded. Please retry after the specified time.",
    "retry_after_seconds": 45
  },
  "request_id": "req_O1P2Q3R4S5T6U7V8W9X0"
}
```

#### 500 Internal Server Error

```json
{
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "An unexpected error occurred. Please try again later.",
    "request_id": "req_Y1Z2A3B4C5D6E7F8G9H0"
  }
}
```

---

## Error Codes

| HTTP Status | Code | Description |
|---|---|---|
| `400` | `VALIDATION_ERROR` | Request body failed validation. Check `details` array. |
| `400` | `INVALID_IDEMPOTENCY_KEY` | Idempotency-Key header is malformed or expired. |
| `401` | `UNAUTHORIZED` | Missing or invalid Authorization header. |
| `403` | `FORBIDDEN` | Token lacks permission to create users. |
| `404` | `NOT_FOUND` | Referenced resource (e.g., SSO provider) does not exist. |
| `409` | `CONFLICT` | Resource already exists (e.g., duplicate email). |
| `422` | `IDEMPOTENCY_REPLAY` | Duplicate request detected via Idempotency-Key. |
| `429` | `RATE_LIMITED` | Rate limit exceeded. Respect `retry_after_seconds`. |
| `500` | `INTERNAL_ERROR` | Server-side error. Retry with exponential backoff. |

---

## Rate Limiting

| Limit | Window | Scope |
|---|---|---|
| 100 requests | 1 minute | Per API token |
| 1000 requests | 1 hour | Per API token |
| 10000 requests | 1 day | Per organization |

**Headers returned on every response:**

| Header | Description |
|---|---|
| `X-RateLimit-Limit` | Maximum requests per window |
| `X-RateLimit-Remaining` | Requests remaining in current window |
| `X-RateLimit-Reset` | Unix timestamp when the window resets |

When rate limited (429), the response includes `retry_after_seconds` in the error body and a `Retry-After` header.

---

## See Also

- [List Users](./list-users) — `GET /api/v1/users`
- [Get User](./get-user) — `GET /api/v1/users/{id}`
- [Update User](./update-user) — `PATCH /api/v1/users/{id}`
- [Delete User](./delete-user) — `DELETE /api/v1/users/{id}`
- [Authentication Guide](../guides/authentication) — How to obtain and use API tokens
- [Rate Limiting Guide](../guides/rate-limiting) — Rate limit policies and best practices
- [Error Handling Guide](../guides/error-handling) — Standard error format and retry strategies
