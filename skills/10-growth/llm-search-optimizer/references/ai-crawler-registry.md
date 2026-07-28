# AI Crawler Registry — LLM Search Optimizer

Maintained registry of known AI crawler user-agents, their documentation, and access patterns.

| Crawler | User-Agent Token | Platform | Purpose | robots.txt Directive |
|---------|-----------------|----------|---------|---------------------|
| GPTBot | GPTBot | OpenAI (ChatGPT) | Content ingestion for ChatGPT | `User-agent: GPTBot` |
| CCBot | CCBot | Common Crawl | Web corpus for AI training (used by multiple platforms) | `User-agent: CCBot` |
| Claude-Web | Claude-Web | Anthropic (Claude) | Content for Claude's web search | `User-agent: Claude-Web` |
| PerplexityBot | PerplexityBot | Perplexity | Content for Perplexity AI search | `User-agent: PerplexityBot` |
| Google-Extended | Google-Extended | Google (Gemini, AI Overviews) | Controls AI Overviews + Bard/Gemini training | `User-agent: Google-Extended` |
| anthropic-ai | anthropic-ai | Anthropic | Legacy AI crawler | `User-agent: anthropic-ai` |
| cohere-ai | cohere-ai | Cohere | AI model training | `User-agent: cohere-ai` |
| Diffbot | Diffbot | Diffbot | Knowledge graph construction | `User-agent: Diffbot` |
| Bytespider | Bytespider | ByteDance (TikTok/Douyin) | AI training for Chinese market | `User-agent: Bytespider` |
| Applebot-Extended | Applebot-Extended | Apple (Apple Intelligence) | AI feature training | `User-agent: Applebot-Extended` |
| OAI-SearchBot | OAI-SearchBot | OpenAI | ChatGPT search functionality | `User-agent: OAI-SearchBot` |

**Note:** This registry changes rapidly. Verify current User-Agent strings against official documentation before implementing.

**Audit command:**

```bash
# Extract AI crawler hits from access logs
grep -E 'GPTBot|CCBot|Claude-Web|PerplexityBot|Google-Extended|anthropic-ai|cohere-ai|Diffbot|Bytespider|Applebot-Extended|OAI-SearchBot' access.log | awk '{print $1, $NF}' | sort | uniq -c | sort -rn
```
