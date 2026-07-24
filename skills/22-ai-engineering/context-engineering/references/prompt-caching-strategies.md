# Prompt Caching Strategies

## Overview

Provider-specific strategies for maximizing prompt cache hit rates. Prompt caching can reduce input token costs by 80-90% when configured correctly.

## Anthropic (Claude) Prompt Caching

**Mechanism:** Cache breakpoints mark a prefix. Anthropic caches everything up to the last breakpoint. Minimum cacheable prefix: 1024 tokens (Claude 3.5 Sonnet) or 2048 tokens (Claude 3 Opus).

**Strategy:**
```
[STATIC PREFIX — CACHED]
  ├── System prompt (unchanging instructions)
  ├── Level 1: Rules files (deterministic order, alphabetically sorted)
  ├── Level 2: Specs (deterministic order, alphabetically sorted)
  └── [CACHE BREAKPOINT]

[DYNAMIC SUFFIX — NOT CACHED]
  ├── Level 3: Source files (may change between requests)
  ├── Level 4: Error output (varies)
  └── Level 5: Conversation history (grows each turn)
```

**Key rules:**
1. Cache breakpoint must be at a token boundary, not mid-token
2. Static prefix must be byte-for-byte identical between requests
3. Sort all static content alphabetically (or any deterministic order)
4. Minimum 1024 tokens for Sonnet cache blocks; split into multiple blocks if needed
5. Cache TTL: 5 minutes (reset on each hit)

## OpenAI Automatic Caching

**Mechanism:** OpenAI automatically caches prefixes > 1024 tokens. No explicit breakpoints needed. Cache hit is automatic when prefix matches.

**Strategy:**
1. Keep system message + static instructions as the first message(s)
2. Avoid prepending dynamic content (timestamps, request IDs) before static content
3. Cache TTL: 5-10 minutes (varies by load)
4. 50% discount on cached input tokens for GPT-4o

## Google (Gemini) Context Caching

**Mechanism:** Explicit context cache creation via API. Cache persists for a configurable TTL (up to several hours). Multiple requests can share one cache.

**Strategy:**
1. Create a named cache with all static content (L1 + L2)
2. Set TTL based on expected session duration (default: 1 hour)
3. Reference cache ID in each request
4. Update cache when rules or specs change
5. Monitor `cachedContentTokenCount` in response metadata

## Deterministic Ordering Protocol

The #1 cause of cache misses: non-deterministic file ordering. Fix:

```python
def deterministic_sort(files: List[FileMetadata]) -> List[FileMetadata]:
    """Sort files for cache-friendly prefix stability."""
    return sorted(files, key=lambda f: (
        f.priority_tier,  # 'A' < 'B' < 'C' (but these go in suffix)
        f.path.lower()     # Alphabetical for stability
    ))

# For the cacheable prefix (L1 + L2):
static_prefix = deterministic_sort(level1_files + level2_files)

# For the non-cacheable suffix (L3 + L4 + L5):
dynamic_suffix = deterministic_sort(level3_files + level4_files)
```

## Cache Performance Monitoring

Track these metrics per session:
- **Cache hit rate:** `hits / (hits + misses)` — target > 60%
- **Cache efficiency:** `cached_tokens / total_input_tokens` — target > 40%
- **Prefix stability:** bytes changed in first N tokens between requests — target < 5%
- **Cost savings:** `(uncached_cost - actual_cost) / uncached_cost` — target > 30%

## Provider Comparison

| Feature | Anthropic | OpenAI | Google |
|---------|-----------|--------|--------|
| Cache control | Explicit breakpoints | Automatic | Named caches |
| Min cache size | 1024 tokens | 1024 tokens | 32K tokens |
| Cache TTL | 5 min (sliding) | 5-10 min | Configurable (hours) |
| Cost discount | 90% | 50% | 75% |
| Multi-request sharing | No (per-request) | No (per-request) | Yes (named cache) |
| Best for | Long conversations | Quick sessions | Batch processing |
