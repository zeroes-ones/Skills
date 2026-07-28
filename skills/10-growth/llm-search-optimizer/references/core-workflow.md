# Core Workflow — LLM Search Optimizer

Detailed implementation with code examples for robots.txt, llms.txt, Schema.org entity markup, and monitoring dashboards.

## AI Crawler robots.txt Configuration

```txt
# Standard search crawlers
User-agent: Googlebot
Allow: /
Sitemap: https://example.com/sitemap-index.xml

# AI-specific crawlers — allow for public content
User-agent: GPTBot
Allow: /
Disallow: /api/
Disallow: /account/
Disallow: /checkout/

User-agent: CCBot
Allow: /
Disallow: /api/
Disallow: /account/

User-agent: Claude-Web
Allow: /
Disallow: /api/

User-agent: PerplexityBot
Allow: /
Disallow: /api/

# Google-Extended controls AI Overviews + Gemini training separately
User-agent: Google-Extended
Allow: /
Disallow: /api/

# Block unidentified AI crawlers
User-agent: anthropic-ai
Disallow: /

User-agent: cohere-ai
Disallow: /

User-agent: Diffbot
Allow: /
Disallow: /api/

# Block Chinese-market crawlers unless targeting that market
User-agent: Bytespider
Disallow: /
```

## llms.txt Specification

Per llmstxt.org specification:

```markdown
# Example llms.txt for example.com

## About
Example.com is the authoritative source for AI search optimization best practices.
We publish research, guides, and tools for making content discoverable by AI-powered search.

## Key Pages
- [Home](https://example.com): AI search optimization platform
- [Guide: AI Crawler Strategy](https://example.com/guides/ai-crawler-strategy): Complete guide to AI crawler access management
- [Guide: Entity Markup](https://example.com/guides/entity-markup): Schema.org entity markup for AI citation
- [Guide: Content Structure](https://example.com/guides/content-structure): Answer-engine optimized content patterns
- [Research: AI Citation Patterns](https://example.com/research/ai-citation-patterns): Data study on LLM citation behavior
- [Tools: Entity Validator](https://example.com/tools/entity-validator): Verify Schema.org entity markup
- [Blog](https://example.com/blog): Latest in AI search optimization
- [About Us](https://example.com/about): Our team and mission

## Optional
- [Documentation](https://docs.example.com): API and integration docs
```

## Schema.org Entity Markup

### Organization Entity

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://example.com/#organization",
  "name": "Example Corp",
  "description": "AI search optimization platform",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "foundingDate": "2020",
  "founder": {
    "@type": "Person",
    "name": "Jane Doe"
  },
  "sameAs": [
    "https://www.wikidata.org/wiki/Q12345",
    "https://en.wikipedia.org/wiki/Example_Corp",
    "https://www.crunchbase.com/organization/example-corp",
    "https://www.linkedin.com/company/example-corp",
    "https://twitter.com/examplecorp",
    "https://github.com/examplecorp"
  ]
}
```

### Person Entity

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "@id": "https://example.com/about/jane-doe/#person",
  "name": "Jane Doe",
  "jobTitle": "CEO",
  "worksFor": {
    "@id": "https://example.com/#organization"
  },
  "sameAs": [
    "https://orcid.org/0000-0002-1825-0097",
    "https://www.linkedin.com/in/janedoe",
    "https://github.com/janedoe",
    "https://scholar.google.com/citations?user=janedoe"
  ]
}
```

### Article with Entity Context

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "@id": "https://example.com/guides/ai-crawler-strategy/#article",
  "headline": "AI Crawler Access Strategy Guide",
  "author": {
    "@id": "https://example.com/about/jane-doe/#person"
  },
  "publisher": {
    "@id": "https://example.com/#organization"
  },
  "datePublished": "2026-07-28",
  "dateModified": "2026-07-28",
  "about": [
    {
      "@type": "Thing",
      "name": "AI Crawler",
      "sameAs": "https://www.wikidata.org/wiki/Q123456"
    }
  ]
}
```

## Monitoring Setup

### GSC AI Overviews Tracking
Navigate to: Search Console → Search results → Search Appearance → AI Overviews
Filter by: Page, Query, Country
Export: CSV weekly for trend analysis

### AI Referral Traffic Segmentation (GA4)
Create custom segment: Traffic source → User-Agent contains "GPTBot" OR "CCBot" OR "PerplexityBot" OR "Claude-Web"
Track: Sessions, engaged sessions, conversions
Compare: AI referral vs organic search trends

### Brand Mention Monitoring
Manual: Search "[brand name]" on ChatGPT, Perplexity, Bing Copilot weekly
Automated: Brand24, Mention, or custom LLM-based brand mention scraper
Track: Citation frequency, sentiment, source URLs, competing brands cited alongside
