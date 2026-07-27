#!/usr/bin/env bash
# SDD-Cache Post-Hook — Stores WebFetch responses with cache validators.
# Extracts ETag and Last-Modified headers from responses for future revalidation.
set -euo pipefail

CACHE_DIR="${HOME}/.cache/skills/sdd"
mkdir -p "$CACHE_DIR"

# Store cache metadata for the fetched URL
# The agent calling this hook should pass: URL, ETag, Last-Modified via environment or stdin
URL="${1:-}"
ETAG="${2:-}"
LAST_MODIFIED="${3:-}"

if [[ -z "$URL" ]]; then
  echo "SDD-CACHE: No URL provided for caching"
  exit 0
fi

CACHE_KEY=$(echo -n "$URL" | sha256sum | cut -d' ' -f1)
CACHE_FILE="$CACHE_DIR/$CACHE_KEY.json"

# Store validators
jq -n \
  --arg url "$URL" \
  --arg etag "$ETAG" \
  --arg last_modified "$LAST_MODIFIED" \
  --arg cached_at "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  '{url: $url, etag: $etag, last_modified: $last_modified, cached_at: $cached_at}' \
  > "$CACHE_FILE" 2>/dev/null || {
  echo "SDD-CACHE: Failed to store cache metadata (jq may not be installed)"
  exit 0
}

echo "SDD-CACHE: Stored cache entry for $URL → $CACHE_FILE"
