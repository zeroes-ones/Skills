# SDD-Cache: Source-Driven Development Caching

Cache layer for `source-driven-development` skill WebFetch calls. Uses HTTP conditional revalidation to skip redundant fetches without sacrificing freshness guarantees.

## How It Works

1. **Pre-hook** (`sdd-cache-pre.sh`): Before WebFetch, checks if URL has a cached version with valid ETag/Last-Modified. If so, the fetch uses `If-None-Match` / `If-Modified-Since` headers.
2. **Post-hook** (`sdd-cache-post.sh`): After WebFetch, stores ETag and Last-Modified from the response for future revalidation.

## Cache Location

`~/.cache/skills/sdd/` — one JSON file per URL (keyed by SHA-256 of URL).

## Cache Entry Format

```json
{
  "url": "https://example.com/docs/api",
  "etag": "\"abc123\"",
  "last_modified": "Wed, 21 Oct 2025 07:28:00 GMT",
  "cached_at": "2026-07-27T13:00:00Z"
}
```

## Freshness Guarantees

- **HTTP 304 (Not Modified)** → Use cached content (server confirms freshness)
- **HTTP 200 (OK)** → Replace cache with new content + validators
- **No validators** → Cache for session only, no cross-session persistence
- **Cache older than 24h** → Revalidate even if validators exist (stale-while-revalidate)
