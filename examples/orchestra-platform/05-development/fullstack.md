# Full-Stack Integration

## Backend-for-Frontend (BFF) Pattern

Next.js 14 serves as the BFF layer between the React frontend and the Go microservices backend. Instead of calling Go services directly from the browser, the frontend calls Next.js API routes under `/api/`, which handle session validation, data aggregation, and proxy to the appropriate Go service. This avoids exposing internal service URLs to the client and allows the BFF to transform responses (e.g., flattening nested JSON, enriching with feature flags) before sending to the UI.

## API Route Design

All BFF API routes live in `src/app/api/` using Next.js Route Handlers. Example: `GET /api/catalog/services` authenticates the session cookie, calls `catalog-service.internal:8080/v1/services?org_id=X`, merges the response with plugin metadata from `plugin-service`, and returns a single JSON payload. Error responses from Go services are normalized to a consistent `{ error: { code, message, details } }` format.

## Server-Side Rendering

Catalog pages use Next.js SSR for SEO and initial load performance. The `generateMetadata()` function produces dynamic `<title>` and `<meta>` tags per service. Page components fetch data in `async` server components, passing dehydrated state to the client via React Query's `HydrationBoundary`. The Template Detail page is statically generated at build time for the top 200 most-used public templates (ISR with 1-hour revalidation).

## Shared Types via tRPC / OpenAPI

Go services expose OpenAPI 3.1 specs at `/openapi.json`. A CI job uses `openapi-typescript` to generate TypeScript types into `packages/api-types/`, shared by both the Next.js BFF and the React frontend. This eliminates type drift — renaming a Go struct field immediately fails TypeScript compilation in the frontend until the generated types are updated.

## Real-Time Communication

Template execution status uses Server-Sent Events (SSE) rather than WebSockets for unidirectional server-to-client updates. The BFF exposes `GET /api/templates/executions/:id/stream` which proxies SSE from the Go execution service. The client uses the EventSource API with automatic reconnection (3-second backoff). For bidirectional communication (future terminal-in-browser feature), a WebSocket endpoint is planned at `wss://api.orchestra.dev/ws` using the Go gorilla/websocket library behind the ALB with a 60-second idle timeout.

## Authentication Flow

NextAuth.js v5 handles OAuth 2.0 with Auth0 as the identity provider. The session JWT is stored in an httpOnly, Secure, SameSite=Lax cookie. BFF API routes read the session server-side via `auth()`. For service-to-service calls, the BFF attaches a short-lived internal JWT (5-minute expiry, signed with a shared HMAC key) in the `X-Internal-Auth` header.
