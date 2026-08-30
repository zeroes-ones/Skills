# Cache Strategy — Prefix Freezing, Hit-Rate Economics

## The Core Fact

Prompt caching matches the exact byte sequence from position 0. A stable prefix cached at the cached-read rate (1/10-1/25 of uncached input) is the **cheapest compression available** — it is reduction without information loss.

## Provider Mechanics (verify at research time)

| Provider | Mechanism | Min cacheable prefix | Cached read price |
|----------|-----------|---------------------|-------------------|
| Anthropic | Explicit `cache_control` blocks | 1,024 tokens | ~1/10 of input |
| OpenAI | Automatic; `cached_tokens` in usage | 1,024 tokens | 50% of input |
| Gemini | Implicit | 32,768 tokens | 25% of input |

## The Freeze Contract

1. Declare the stable prefix: L1 rules + L2 static specs + frozen tool schemas.
2. Order deterministically: priority tier → alphabetical within tier.
3. Enforce with a CI byte-diff gate: any change requires cache-freeze approval.
4. Bust deliberately when rules change: quantify the one-time uncached cycle, then re-freeze.

## Hit-Rate Economics (worked)

A 50K prefix, 500 requests/day, 22 days/month, uncached $7.50/M vs cached $0.30/M:

| State | $/day | $/month |
|-------|------:|--------:|
| Fully cached (100%) | $7.50 | $165 |
| Fully uncached (0%) | $187.50 | $4,125 |
| 50% hit rate | $97.50 | $2,145 |

**A single reordered comment is worth up to $3,960/month.**

## Interaction with Minification

Minification must NOT touch the prefix (Ground Rule R5). If you minify the prefix, you bust the cache. The optimizer's rule: **freeze first, then minify only the non-prefix content, and never reformat the frozen block.**

## Audit Protocol

1. Capture the assembled prompt for 10 consecutive requests.
2. Byte-diff the first N tokens (the intended static block) across all 10.
3. Identical → provider/config issue (check flags, min threshold).
4. Different → locate the churn (ordering, dynamic content, human edit) and fix + freeze.
