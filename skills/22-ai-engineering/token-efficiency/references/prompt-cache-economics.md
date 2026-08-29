# Prompt Cache Economics — Prefix Stability and Provider Rules

> `[VERIFIED 2026-08-29]` against provider documentation. Caching is the highest-ROI token lever because it is *reduction without information loss*: you send the same bytes, but pay 1/10-1/25 of the price.

## The Core Rule: Byte-Stable Prefix

Prompt caching matches the **exact byte sequence from position 0**. Any change — a reordered line, an added comment, a timestamp, a different file order — invalidates the cache for the entire prefix.

```
cache hit ⇔ bytes[0..N) identical to the previous request
```

## Provider Rules at a Glance

| Provider | Mechanism | Min cacheable prefix | Cached read price | Notes |
|----------|-----------|---------------------|-------------------|-------|
| Anthropic | Explicit `cache_control` blocks | 1,024 tokens | ~1/10 of input | Cache persists 5 min; explicit breakpoints |
| OpenAI | Automatic + `cached_tokens` in usage | 1,024 tokens | 50% of input | No control needed; measure `usage.prompt_tokens_details.cached_tokens` |
| Gemini | Implicit | 32,768 tokens | 25% of input | Automatic; below 32K prefix caching never engages |

## Prefix-Stability Audit (Decision Tree 2 in SKILL.md)

1. Capture the assembled prompt for 10 consecutive real requests.
2. Byte-diff the first N tokens (the intended static block) across all 10.
3. If identical → provider/config issue: check cache flags, check min-prefix threshold.
4. If different → locate the churn:
   - **File ordering varies** → sort deterministically: priority tier, then alphabetical within tier.
   - **Dynamic content in the prefix** (timestamps, request IDs, dates) → move it *after* the static block. The cache covers the prefix; the dynamic tail is paid at full rate but is usually small.
   - **A human reordered/reformatted** → enforce cache-freeze approval; add a CI byte-diff gate on the prefix artifact.
5. Measure hit rate over the next 50 requests; target ≥ 60%, goal 90%+ for stable workloads.

## Cost Model: What One Prefix Byte Costs

A 50K-token prefix on Claude Sonnet 4, 500 requests/day, 22 days/month:

| State | Cost/day | Cost/month |
|-------|---------:|-----------:|
| Fully cached (hit rate 100%) | $7.50 | $165 |
| Fully uncached (hit rate 0%) | $187.50 | $4,125 |
| 50% hit rate | $97.50 | $2,145 |

**A single reordered comment is worth up to $3,960/month** — the difference between rows 1 and 2. This is the #1 measured token-efficiency failure in production systems.

## Cache-Prefix Freeze Protocol

1. Declare the prefix artifact (L1 rules + L2 static specs + frozen tool schemas) as versioned, byte-stable content.
2. Add a CI gate: byte-diff of the committed prefix against the previous release; any change requires approval.
3. Approve changes explicitly: "cache-freeze approval" with the one-time cost of the bust quantified.
4. When a rule genuinely changes, bust deliberately: measure the one-time uncached cycle, then re-freeze.

## Interaction with Compression

Compression and caching are substitutes — **stabilize first, compress second**. If content is repeated across requests, caching it (stable, lossless, cheap) beats compressing it (lossy, risky, and it still costs something). Only compress what cannot be stabilized: unique per-request content, long conversation tails, and one-off dumps.
