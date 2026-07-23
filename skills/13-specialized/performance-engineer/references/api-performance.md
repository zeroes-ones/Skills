# API Performance

### Connection Pooling

- **Pool sizing formula**: `connections = (core_count × 2) + effective_spindle_count` (traditional) or for SSDs: `connections ≈ core_count × 2 ÷ (expected_active_queries_per_connection)`
- **Connection timeout configuration**: Set `connect_timeout` (fail fast if DB is down), `idle_in_transaction_session_timeout` (release stuck connections), `statement_timeout` (kill runaway queries).
- **Idle connection management**: Tune `idle_timeout` (close unused connections), `max_lifetime` (periodically rotate connections to avoid stale ones), use connection health checks (`SELECT 1`).

### Query Optimization

- **N+1 queries**: One request triggers 1 query for a list + N queries per item. Example: fetching 100 blog posts then querying author for each. Fix: eager loading (`JOIN ... IN`), DataLoader pattern (batch + cache).
- **DataLoader**: Batching + memoization per request. Combines N individual lookups into one batched query. Standard in GraphQL ecosystems.
- **Eager loading**: Use `SELECT * FROM posts JOIN authors ON posts.author_id = authors.id` instead of N+1 individual queries.

### Response Caching

- **ETag**: Content-based hash. Client sends `If-None-Match`, server responds `304 Not Modified` if unchanged. Great for API responses that change infrequently.
- **Last-Modified**: Timestamp-based. Client sends `If-Modified-Since`. Coarser than ETag but simpler.
- **Cache-Control**:
  - `public, max-age=60, s-maxage=300` — browser caches 60s, CDN caches 300s
  - `private` — do not cache in shared caches (CDN/proxies) — for user-specific data
  - `no-cache` — revalidate with origin on every use
  - `stale-while-revalidate=86400` — serve stale data for 24h while revalidating in background
- **CDN-edge caching**: For read-heavy APIs, cache at the CDN edge. Invalidate on write (surrogate-key based purge). Reduces origin load by 60-90%.

### Compression

- **gzip**: Universal support, ~70% reduction on text. Default baseline.
- **Brotli**: 15-20% better than gzip for text, supported by all modern browsers. Use at CDN or origin (dynamic Brotli is CPU-intensive; Brotli + static caching is best).
- **zstd**: Better ratios than Brotli, faster decompression. Growing browser support. Best for static assets served via CDN.
- **When to compress**: At CDN edge for static assets (compress once, cache forever). At application level for dynamic API responses (Brotli for JSON, negotiate with `Accept-Encoding`).
- **What NOT to compress**: Already-compressed formats (JPEG, PNG, WebP, AVIF, video, audio) — waste of CPU with no benefit.

### Pagination

- **Cursor-based**: `?cursor=eyJsYXN0X2lkIjogMTAwMH0=` (base64-encoded opaque token). Stable even if data is inserted/deleted. Required for real-time or high-churn data. Preferred for APIs.
- **Offset-based**: `?offset=20&limit=10`. Simple but unstable — inserting rows before the current page shifts offset. Acceptable for static/admin UIs with small datasets (<10K rows).
- **Keyset pagination**: `WHERE id > last_seen_id ORDER BY id LIMIT 10`. Faster than offset, no skip overhead. Works only with sortable, unique columns.
