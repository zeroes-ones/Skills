# API Design Best Practices — Contracts That Age Well

> Original explainer for interview prep and learning. [research-source: title-only]

## What "good API design" means

An API is a contract between your system and everyone who depends on it. Good design minimizes **surprise**: predictable naming, consistent errors, explicit semantics, and safe evolution. The cost of getting it wrong is paid by every consumer forever — which is why design review matters more than code review for APIs.

## Design principles (the durable ones)

1. **Resources over actions.** Model nouns with standard verbs (`POST /orders`, `GET /orders/{id}`), not RPC-style verbs (`/createOrder`). Exceptions exist (search, actions) — use sub-resources or explicit action endpoints sparingly.
2. **Consistent naming & casing** (`snake_case` or `camelCase` — pick one and never mix; plural nouns; kebab URL segments).
3. **Idempotency where it matters** — `PUT`/`DELETE` are idempotent by contract; `POST` needs an `Idempotency-Key` for anything that can be retried (payments!). See idempotency.md in this repo.
4. **Explicit, structured errors.** Not just a status code: `{ error: { code, message, details, request_id } }` with a machine-readable `code` and human `message`. Never leak stack traces or SQL.
5. **Pagination from day one** — cursor/keyset pagination over page-number for large, changing datasets (avoids the "rows shifted between pages" problem). Return `next_cursor`.
6. **Versioning strategy decided up front** — URL `/v1/` is the pragmatic default; see versioning-cost-analysis.md in this repo.
7. **Documentation as contract** — OpenAPI 3.1 as the source of truth; examples per field; generated client/server where possible.
8. **Rate limiting & quotas with clear headers** — `X-RateLimit-Remaining`, `Retry-After`; clients should never discover limits by 429 surprise.
9. **Backward-compatible by default** — additive-only changes (new optional fields, new endpoints); breaking changes go through versioning + deprecation.
10. **Secure by design** — authz on every endpoint, least-privilege scopes, no sensitive data in URLs/logs (see secure-api-design SKILL.md).

## Status codes — use the right ones (a cheat sheet)

| Range | Use | Common specifics |
|---|---|---|
| 2xx | Success | 200 OK, 201 Created (+Location), 202 Accepted (async), 204 No Content |
| 4xx | Client error | 400 bad request, 401 unauthenticated, 403 forbidden, 404 not found, 409 conflict, 422 validation, 429 rate limited |
| 5xx | Server error | 500 internal, 502/503/504 gateway/service/timeout — retryable vs not |

Rules: never return 200 for an error payload; never return 500 for a client mistake; **409** for state conflicts, **422** for semantic validation.

## REST vs GraphQL vs gRPC (the honest comparison)

| Aspect | REST | GraphQL | gRPC |
|---|---|---|---|
| Best for | Public/web APIs, CRUD | Client-driven UIs, over-fetching pain | Internal service-to-service, streaming, low latency |
| Contract | OpenAPI | Schema + resolvers | Proto IDL |
| Over-fetching | Possible | Solved (query exactly) | N/A (typed methods) |
| Caching/HTTP | Native | Harder (single endpoint) | N/A (HTTP/2) |
| Versioning | URL/header | Schema evolution | Proto compatibility rules |
| Complexity | Low | Medium (client libs, N+1) | High (codegen, tooling) |

Don't be dogmatic — many systems are REST outward + gRPC internally (the common, sensible split).

## Interview answer skeleton

"I design APIs as resource-oriented contracts with consistent naming, structured errors (code + message + request_id), pagination from day one, and explicit idempotency for retryable operations. I version from the start and keep changes additive; breaking changes go through a documented deprecation. The contract is OpenAPI and reviewed like a product decision, because every consumer pays for surprises forever."

## Anti-patterns

- ❌ Returning `200 OK` with an error in the body — clients can't branch correctly.
- ❌ Endpoints that leak internal implementation (`/getUserDataFromDb`).
- ❌ No pagination until "we'll add it later" — adding it later is a breaking change.
- ❌ Inconsistent error shapes across endpoints.
- ❌ `POST` for everything "to keep it simple" — you lose idempotency semantics and caching.

## Deliberate-practice drills

1. **Design drill:** design the REST API for an orders resource: endpoints, status codes, error schema, pagination, idempotency.
2. **Error drill:** write the error contract for 8 failure cases (not found, conflict, validation, rate limit, auth, upstream timeout) with codes + messages.
3. **Evolution drill:** take a v1 endpoint and plan an additive change and a breaking change with deprecation.
4. **Comparison drill:** for a chat product, decide REST vs GraphQL vs gRPC for public client vs internal services.
5. **Review drill:** red-team an API design you find — list 5 surprises a consumer would hit.

## References
- See also: idempotency.md, versioning-cost-analysis.md, rpc-and-grpc.md (this repo)
- `api-designer` SKILL.md — OpenAPI, lifecycle, error modeling
- `secure-api-design` SKILL.md — authz, rate limiting, OWASP API Top 10
