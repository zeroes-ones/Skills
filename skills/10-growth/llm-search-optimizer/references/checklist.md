# Production Checklist — LLM Search Optimizer

Expanded production checklist with per-platform verification steps.

## Pre-Launch Verification

- [ ] robots.txt: all AI crawler directives tested with `curl -H "User-Agent: GPTBot" https://example.com/robots.txt`
- [ ] llms.txt: accessible at root, returns 200, Content-Type text/plain or text/markdown
- [ ] llms-full.txt: if enabled, accessible and complete
- [ ] Schema.org: all entity markup validates via Schema Markup Validator
- [ ] sameAs links: all return HTTP 200 and point to correct entity pages
- [ ] @id URIs: consistent across all pages (no duplicate or conflicting entity IDs)
- [ ] Content: top 10 money pages restructured with answer-engine patterns

## Post-Launch Monitoring (30-Day Window)

- [ ] Day 1: Verify GSC AI Overviews tracking is collecting data
- [ ] Day 7: First citation baseline — which pages appear in AI Overviews?
- [ ] Day 14: Check AI crawler access logs — are GPTBot/CCBot hitting new pages?
- [ ] Day 21: Brand mention check — search brand on ChatGPT, Perplexity, Copilot
- [ ] Day 30: Full before/after comparison — AI citations, referral traffic, brand mentions

## Platform-Specific Verification

### Google AI Overviews
- [ ] GSC → Search Appearance → AI Overviews shows your pages
- [ ] Search "[your query]" on Google — do you appear in the AI Overview?

### ChatGPT
- [ ] Search "[your brand] + [topic]" on ChatGPT (with browsing enabled)
- [ ] Is your content cited or your brand mentioned?

### Perplexity
- [ ] Search "[your query]" on Perplexity
- [ ] Are your pages cited as sources?

### Bing Copilot
- [ ] Search "[your brand]" on Bing Copilot
- [ ] Are you recognized as an entity with knowledge panel data?
