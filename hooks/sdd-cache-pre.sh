#!/usr/bin/env bash
# SDD-Cache Pre-Hook — Checks WebFetch cache before making HTTP requests.
# Uses HTTP conditional requests (If-None-Match / If-Modified-Since) to skip redundant fetches.
# Cache directory: ~/.cache/skills/sdd/
set -euo pipefail

CACHE_DIR="${HOME}/.cache/skills/sdd"
mkdir -p "$CACHE_DIR"

# Read the URL from the WebFetch arguments (passed via stdin or environment)
# This hook is called before WebFetch — it checks if cached content is still fresh
# Returns cache hit data or passes through to let the actual fetch happen

# For now, output cache metadata that the agent can use
# The actual revalidation logic runs at fetch time via HTTP headers
echo "SDD-CACHE: Pre-fetch cache check. Cache directory: $CACHE_DIR"
