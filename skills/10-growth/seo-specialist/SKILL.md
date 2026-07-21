---
name: seo-specialist
description: Technical SEO audits, structured data (JSON-LD), Core Web Vitals optimization, crawl budget management, E-E-A-T content strategy, international SEO, JavaScript SEO, link building, schema markup, algorithm update response, rank tracking. Triggered by SEO audit, structured data, Core Web Vitals, crawl budget, hreflang, JSON-LD, schema markup, organic traffic, ranking drop, JavaScript SEO.
author: Sandeep Kumar Penchala
---

# SEO Specialist

Expert field manual for technical SEO strategy, audit execution, and search visibility optimization.
Covers the full lifecycle: crawl budget management, structured data deployment, Core Web Vitals
remediation, content SEO (E-E-A-T, topic clusters, semantic search), international SEO (hreflang,
localization), JavaScript SEO (SSR/SSG, dynamic rendering), link building strategy, rank tracking,
and algorithm update response.

## When to Use

- Launching a new domain or executing a site migration — pre-launch SEO audit and post-launch verification
- Organic traffic decline: root cause diagnosis — manual actions, algorithm update, technical regression, competitor moves
- Implementing structured data (JSON-LD): Article, Product, FAQ, HowTo, LocalBusiness, Organization, BreadcrumbList, Sitelinks Searchbox
- Core Web Vitals below thresholds: LCP > 2.5s, INP > 200ms, CLS > 0.1 — with per-metric optimization playbooks
- Crawl budget wasted on low-value URLs (facets, pagination, query params, duplicate content)
- Multi-language/multi-region site: hreflang architecture, ccTLD vs subdirectory vs subdomain decision
- JavaScript-heavy site: SSR/SSG strategy, dynamic rendering, hydration impact on indexing
- Competitor outranking on high-intent keywords — content gap analysis and SERP feature targeting
- Building a link acquisition strategy: digital PR, broken link building, HARO, link reclamation
- Setting up SEO monitoring: GSC API dashboards, rank tracking, algorithm update alerts

## Core Workflow

### Phase 1: Technical SEO Audit & Crawl Optimization

1. **Crawl Budget Management** — Define what percentage of crawl budget reaches valuable pages:
   ```
   Crawl Budget Formula:
   Crawl Rate Limit (Googlebot requests/sec from Search Console) ×
   Crawl Demand (URL popularity + freshness signals) =
   Effective crawl budget

   Budget Killers (wasting crawl capacity):
   ❌ Faceted navigation: /?color=red&size=large&sort=price — exponential URL space
   ❌ Session IDs in URL: /product?sessionid=abc123
   ❌ Infinite scroll without History API pushState
   ❌ Poorly configured pagination: ?page=1 through ?page=5000
   ❌ Duplicate content with different URL slugs
   ❌ Staging/dev environments accidentally open to crawlers

   Budget Reclamation Strategy:
   1. robots.txt: Disallow: /*?sort=*, Disallow: /*?filter=*, Disallow: /search/*
   2. Canonical tags on faceted pages → point to clean URL
   3. noindex + nofollow on thin/utility pages (login, cart, account settings)
   4. Redirect chains: audit all redirects → flatten to single 301 hop
   5. Remove stale URLs from sitemaps (404, redirected, noindex)
   ```

2. **XML Sitemaps — Production Patterns**:
   ```xml
   <!-- Sitemap index for sites > 50K URLs — split by content type -->
   <?xml version="1.0" encoding="UTF-8"?>
   <sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
     <sitemap><loc>https://example.com/sitemap-products.xml</loc><lastmod>2026-07-15</lastmod></sitemap>
     <sitemap><loc>https://example.com/sitemap-articles.xml</loc><lastmod>2026-07-15</lastmod></sitemap>
     <sitemap><loc>https://example.com/sitemap-categories.xml</loc><lastmod>2026-07-15</lastmod></sitemap>
   </sitemapindex>
   ```

   **Sitemap Rules**:
   - Only canonical URLs. No URLs with `noindex`. No redirects. No 404s.
   - `<lastmod>` must reflect actual content changes (don't set to today's date for all URLs)
   - `<priority>` is largely ignored by Google — invest time in `<lastmod>` and URL selection instead
   - For news: separate Google News sitemap with `news:news` namespace — URLs published in last 48 hours
   - For video: video sitemap or `VideoObject` schema — use schema for richer results
   - Compress with gzip: `sitemap.xml.gz` — submit compressed URL to GSC

3. **robots.txt Precision**:
   ```
   # Pattern: allow crawling, block only problematic paths
   User-agent: *
   Allow: /
   Disallow: /api/
   Disallow: /*?sort=
   Disallow: /*?filter=
   Disallow: /*?color=
   Disallow: /search
   Disallow: /checkout
   Disallow: /account
   Sitemap: https://example.com/sitemap-index.xml

   User-agent: Googlebot-News
   Allow: /

   User-agent: GPTBot
   Disallow: /
   ```

   **Common Mistakes**:
   - `Disallow: /` on staging (correct) but accidentally deployed to production
   - Using `Noindex` in robots.txt (robots.txt doesn't support this — use meta tag or HTTP header)
   - Blocking CSS/JS: Google needs to render your pages — don't block `/assets/` or `/static/`

4. **Canonical Tags Strategy**:
   ```html
   <!-- Self-referencing canonical (defensive — ALWAYS include) -->
   <link rel="canonical" href="https://example.com/products/blue-widget" />

   <!-- Decision matrix for cross-domain canonicals -->
   <!-- Syndicated content → canonical to original source -->
   <!-- Parameterized URLs → canonical to clean URL -->
   <!-- HTTP → canonical to HTTPS -->
   <!-- Trailing slash → pick one convention and canonical to it -->
   ```

### Phase 2: Core Web Vitals for SEO

1. **LCP (Largest Contentful Paint) < 2.5s** — Measures when the largest visible content element renders:

   **Optimization Playbook** (ordered by impact):
   ```
   1. Image optimization (LCP is usually a hero image):
      - Use <img> not CSS background-image for LCP element
      - Preload: <link rel="preload" as="image" fetchpriority="high" href="hero.webp">
      - Responsive: srcset + sizes for different viewports
      - Format: WebP (lossy) or AVIF (smaller but slower decode) — serve both via <picture>
      - CDN: Serve from edge, not origin — reduces TTFB for far-away users

   2. Eliminate render-blocking chains:
      - Inline critical CSS (<14KB): <style>/* above-fold styles */</style>
      - Defer non-critical CSS: <link rel="preload" as="style" onload="this.rel='stylesheet'">
      - defer or async on all non-critical JS
      - lazyload below-fold images: loading="lazy"

   3. Reduce server response time (TTFB):
      - CDN edge caching for static content
      - DB query optimization for dynamic pages
      - Server-side caching (Redis, Varnish) for API responses
      - Use HTTP/3 for connection multiplexing
   ```

2. **INP (Interaction to Next Paint) < 200ms** — Measures responsiveness to user interactions:

   **Optimization Playbook**:
   ```
   1. Break up long tasks (< 50ms each):
      - Yield to main thread: setTimeout(fn, 0) or requestIdleCallback
      - isInputPending() API for yielding during long loops

   2. Reduce JavaScript execution:
      - Code splitting: load only what's needed per page
      - Tree shaking: eliminate dead code
      - Avoid large inline scripts (>1KB) — they block parsing
      - Audit third-party scripts: analytics, chatbots, ads → load async with timeout

   3. Optimize event handlers:
      - Debounce scroll/resize handlers (250ms)
      - Move non-UI work to Web Workers: data processing, filtering
      - Use CSS animations (GPU-accelerated) instead of JS animations
   ```

3. **CLS (Cumulative Layout Shift) < 0.1** — Measures visual stability:

   **Optimization Playbook**:
   ```
   1. Reserve space for dynamic content:
      - Images: explicit width and height OR aspect-ratio CSS
      - Ad slots: min-height with placeholder or skeleton
      - Embeds: iframe with defined dimensions
      - Fonts: font-display: swap + size-adjust to match fallback font metrics

   2. Avoid inserting content above existing content:
      - Banners/newsletters: push down existing content, don't overlay
      - Infinite scroll: use History API pushState + graceful loading
      - Dynamic injected ads: reserve space BEFORE ad loads

   3. Handle font loading with size-adjust to prevent layout shifts.

   4. CLS Debugging in PageSpeed Insights:
      - "Avoid large layout shifts" diagnostic → shift score per element
      - Elements with highest cumulative CLS score → fix top 3
   ```

4. **How CWV Impacts Rankings**:
   ```
   Direct: All three thresholds (LCP, INP, CLS) are page experience ranking signals.
   Indirect: Slow pages → higher bounce rate → lower engagement signals → lower rankings.
   Tipping point: Pages passing ALL thresholds get a ranking boost over pages that don't.
   Not a tiebreaker: Excellent CWV won't outrank highly relevant content from a slow site.
   ```

### Phase 3: Content SEO & E-E-A-T

1. **E-E-A-T Framework** (Experience, Expertise, Authoritativeness, Trustworthiness):

   | Signal | Implementation | Verification |
   |---|---|---|
   | **Experience** | Author bios with real credentials, first-hand product use, original photography | Does the author demonstrate actual use of the product/topic? |
   | **Expertise** | Detailed author pages, credentials, citations, peer-reviewed sources | Does the content show deep knowledge beyond surface-level summaries? |
   | **Authoritativeness** | Backlinks from .edu/.gov, Wikipedia citations, industry recognition, awards | Are recognized authorities linking to this content? |
   | **Trustworthiness** | HTTPS, clear contact info, privacy policy, terms, refund policy, real business address | Would a user feel safe sharing payment info? |

   **YMYL (Your Money Your Life)** — Medical, financial, legal, news content faces higher E-E-A-T scrutiny.

2. **Topic Clusters & Pillar Pages**:
   ```
   Architecture:
   Pillar Page (comprehensive guide: "Complete Guide to Home Brewing")
   ├── Cluster Page 1: "Best Home Brewing Equipment for Beginners"
   ├── Cluster Page 2: "How to Sanitize Brewing Equipment"
   ├── Cluster Page 3: "5 Common Home Brewing Mistakes (and How to Avoid Them)"
   └── Cluster Page 4: "Home Brewing vs Craft Beer: Cost Comparison"

   Internal linking: Every cluster page links back to pillar page with descriptive anchor.
   Pillar page links to each cluster page. No orphan pages.
   ```

3. **Content Gap Analysis**:
   ```
   1. List your top 20 target keywords + top 3 competitors
   2. For each keyword: which competitor ranks in top 10 that you don't?
   3. For missing keywords: what type of content ranks? (guide, listicle, tool, comparison)
   4. Build a content brief: target keyword, search intent, SERP features present,
      content type needed, estimated word count (analyze top 3 ranking pages)
   5. Prioritize: high search volume × low competition score × high business relevance
   ```

4. **Semantic Search Optimization** (entities, not just keywords):
   ```
   Keyword: "best coffee maker"
   Google understands related entities: "drip coffee," "espresso machine," "French press,"
   "grind size," "brew temperature," "SCA certification"

   Optimize for entities:
   - Use Schema.org types (Product, Review, HowTo)
   - Link to authoritative sources (Wikipedia, manufacturer pages) for entity confirmation
   - Cover semantically related subtopics: cleaning, durability, warranty, price range
   - Answer "People Also Ask" questions in H2s with concise answers below
   ```

### Phase 4: Schema Markup (JSON-LD)

1. **Schema Decision Matrix** — Which schema per page type:

   | Page Type | Schema.org Type | Rich Result |
   |---|---|---|
   | Homepage | `Organization` + `WebSite` + `SitelinksSearchBox` | Site name, sitelinks, search box |
   | Blog post | `Article` + `BreadcrumbList` + `Person (author)` | Top stories, rich snippet |
   | Product | `Product` + `Offer` + `AggregateRating` + `Review` | Product rich result with price, availability, stars |
   | FAQ page | `FAQPage` with nested `Question`/`Answer` | FAQ accordion in SERP |
   | How-to guide | `HowTo` with `HowToStep` and `HowToSupply` | Step-by-step rich result |
   | Local business | `LocalBusiness` subtype (Restaurant, Dentist, etc.) | Knowledge panel, Local Pack |
   | Recipe | `Recipe` + `NutritionInformation` + `VideoObject` | Recipe rich result |
   | Event | `Event` + `Place` + `Offer` | Event rich result |
   | Video | `VideoObject` + `Clip` | Video rich result |
   | Job posting | `JobPosting` | Google Jobs |
   | Course | `Course` + `EducationalOccupationalProgram` | Course rich result |

2. **JSON-LD Patterns**:

   ```html
   <!-- Organization (homepage) -->
   <script type="application/ld+json">
   {
     "@context": "https://schema.org",
     "@type": "Organization",
     "name": "Acme Corp",
     "url": "https://www.acme.com",
     "logo": "https://www.acme.com/logo.png",
     "sameAs": [
       "https://twitter.com/acme",
       "https://linkedin.com/company/acme",
       "https://github.com/acme"
     ],
     "contactPoint": {
       "@type": "ContactPoint",
       "telephone": "+1-555-0123",
       "contactType": "customer service"
     }
   }
   </script>
   ```

   ```html
   <!-- FAQPage — high CTR uplift when eligible -->
   <script type="application/ld+json">
   {
     "@context": "https://schema.org",
     "@type": "FAQPage",
     "mainEntity": [{
       "@type": "Question",
       "name": "How long does shipping take?",
       "acceptedAnswer": {
         "@type": "Answer",
         "text": "Standard shipping takes 3-5 business days. Express shipping takes 1-2 business days."
       }
     }, {
       "@type": "Question",
       "name": "What is your return policy?",
       "acceptedAnswer": {
         "@type": "Answer",
         "text": "Returns are accepted within 30 days of purchase. Items must be unused and in original packaging."
       }
     }]
   }
   </script>
   ```

   ```html
   <!-- BreadcrumbList (every page deeper than homepage) -->
   <script type="application/ld+json">
   {
     "@context": "https://schema.org",
     "@type": "BreadcrumbList",
     "itemListElement": [
       {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.acme.com"},
       {"@type": "ListItem", "position": 2, "name": "Products", "item": "https://www.acme.com/products"},
       {"@type": "ListItem", "position": 3, "name": "Blue Widget"}
     ]
   }
   </script>
   ```

3. **Schema Validation Pipeline**:
   ```
   1. Development:   JSON-LD Playground (syntax + basic structure)
   2. Staging:       Google Rich Results Test (URL or code snippet)
   3. Pre-production: Schema Markup Validator (schema.org official)
   4. Production:    GSC Enhancements report → Errors & Warnings → Fix → Validate Fix
   5. Monitoring:    GSC API → alert on new schema errors within 24 hours
   ```

4. **Rich Results Monitoring**:
   ```
   GSC → Performance → Search Appearance
   Track: Impressions, clicks, CTR, position for each rich result type.
   Compare: CTR with rich result vs without → quantify schema ROI.

   Common issues:
   - Schema deployed but no rich results → check eligibility (not all schemas show rich results)
   - Errors in GSC → fix within 1 week (Google may drop rich results after prolonged errors)
   - Schema on page but not in GSC → check canonical is correct, page is indexed
   ```

### Phase 5: International SEO

1. **Domain Strategy Decision**:

   | Strategy | SEO Signal | Cost/Complexity | When to Use |
   |---|---|---|---|
   | **ccTLD** (example.de) | Strongest geo signal | High (separate domains, backlinks per domain) | Large market, dedicated local team, strong local brand |
   | **Subdirectory** (example.com/de/) | Moderate (consolidates domain authority) | Low (single domain, shared infrastructure) | Default for most companies — simplest to maintain |
   | **Subdomain** (de.example.com) | Weak (treated as separate site) | Medium | Rarely recommended — splits domain authority |
   | **gTLD + geo params** | Very weak | Low | Don't rely on URL params for geo-targeting |

   **Recommendation**: Subdirectory (example.com/de/) for 90% of cases. ccTLD only when you have a dedicated local team, local hosting, and the market size justifies the overhead.

2. **Hreflang Implementation**:
   ```xml
   <!-- Hreflang via XML sitemaps (RECOMMENDED for 10+ locales) -->
   <url>
     <loc>https://example.com/products/blue-widget</loc>
     <xhtml:link rel="alternate" hreflang="en-us" href="https://example.com/products/blue-widget"/>
     <xhtml:link rel="alternate" hreflang="en-gb" href="https://example.com/gb/products/blue-widget"/>
     <xhtml:link rel="alternate" hreflang="de-de" href="https://example.com/de/produkte/blauer-widget"/>
     <xhtml:link rel="alternate" hreflang="x-default" href="https://example.com/products/blue-widget"/>
   </url>
   ```

   **Hreflang Rules**:
   - Bidirectional: If EN-US page says "DE-DE version is at /de/", the DE-DE page must say "EN-US version is at /"
   - `x-default`: Fallback for unmatched languages — usually the English/international version
   - Self-referencing: Every page must include hreflang for itself
   - Language codes: ISO 639-1 (`en`, `de`, `fr`). Region: ISO 3166-1 Alpha 2 (`us`, `gb`, `de`)
   - Validation: GSC → International Targeting → Hreflang report → zero errors

3. **Localized Keyword Research**:
   ```
   Process:
   1. Native speaker researches keywords in target language
   2. Use local Google domain (google.de, google.fr) or local keyword tool
   3. Map local keywords to local URLs — translation + localization
   4. Localize meta titles and descriptions independently per language
   ```

### Phase 6: JavaScript SEO

1. **Rendering Strategy Decision Tree**:
   ```
   Is SEO a primary traffic channel (>30% of traffic)?
   ├── YES → Is content highly dynamic (real-time data)?
   │   ├── YES → SSR (Next.js, Nuxt) with ISR (Incremental Static Regeneration)
   │   │         Example: e-commerce with live inventory
   │   └── NO → SSG (Static Site Generation) — Gatsby, Astro, Hugo
   │             Example: blog, documentation, marketing site
   └── NO → CSR (Client-Side Rendering) is acceptable
             Example: web app behind login, internal tool
   ```

2. **SSR/SSG Best Practices**:
   ```
   ✅ Server-render critical content (title, meta, H1, body text)
   ✅ Page source (View Source) should contain full rendered content
   ✅ Use framework Link components for internal navigation — not SPA router
   ✅ Metadata in <head> rendered server-side (title, meta description, canonical, hreflang)
   ✅ Semantic HTML: <nav>, <article>, <section>, <h1>-<h6> hierarchy
   ❌ Client-side data fetching for above-the-fold content
   ❌ window or document references in SSR code (causes hydration mismatch)
   ```

3. **Dynamic Rendering** (legacy approach, SSR/SSG preferred):
   ```
   When: You have a SPA that can't be migrated to SSR and SEO is critical.

   Architecture:
   User-Agent: Googlebot → Rendertron/Puppeteer → Pre-rendered HTML
   User-Agent: Chrome (normal user) → SPA as normal

   Caveats:
   - Google considers this cloaking unless content is identical
   - Adds infrastructure complexity (rendering service, cache invalidation)
   - Prefer SSR/SSG. Dynamic rendering is a bridge, not a destination.
   ```

4. **Infinite Scroll SEO**:
   ```html
   <!-- Replace with: paginated series + History API -->
   <!-- Each "page" of infinite scroll should have a unique URL -->

   <!-- Correct pattern: -->
   <link rel="next" href="https://example.com/blog?page=2">
   <link rel="prev" href="https://example.com/blog">

   <!-- OR: consolidated approach — all products on a single page -->
   <link rel="canonical" href="https://example.com/category/all-products">

   <!-- JavaScript: pushState on scroll → Google can follow links -->
   window.history.pushState({page: 2}, '', '?page=2');
   ```

5. **Hydration Considerations**:
   ```
   Problem: SSR sends HTML → client-side JS hydrates → layout shift during hydration
   Solution:
   - Suppress hydration warnings: suppressHydrationWarning on dynamic content
   - Progressive hydration: hydrate critical components first, lazy parts later
   - Static rendering: skip hydration entirely for static content (Astro islands architecture)
   ```

### Phase 7: Link Building Strategy

1. **Link Acquisition Methods** (white-hat, sustainable):

   | Method | Effort | Impact | When to Use |
   |---|---|---|---|
   | **Digital PR** | High | High | Data studies, original research, surveys |
   | **Broken link building** | Medium | Medium | Find dead links on relevant blogs → offer your content as replacement |
   | **HARO / Qwoted** | Low | Medium-High | Respond to journalist queries → get quoted + linked |
   | **Guest posting** | Medium | Medium | Write for reputable industry publications |
   | **Link reclamation** | Low | Low-Medium | Reclaim unlinked brand mentions, fix broken backlinks |
   | **Resource page links** | Medium | Medium | Find "best resources" pages in niche → suggest your resource |

2. **Broken Link Building Process**:
   ```
   1. Identify relevant sites (Ahrefs/SEMrush → competitor backlinks)
   2. Find broken outbound links: check-links tool or Screaming Frog
   3. Create or identify your content that matches the dead resource
   4. Email: "I noticed [URL] links to [dead resource]. I've published [your resource]
      that covers the same topic in more depth. Would it be useful as a replacement?"
   5. Track: spreadsheet of all outreach → response rate benchmark: 5-15%
   ```

3. **Link Reclamation**:
   ```
   Unlinked brand mentions:
   1. Set up Google Alerts + Mention.com for brand name
   2. Find pages mentioning your brand without a link
   3. Email requesting a link to a relevant page

   Broken backlinks (links to your site that return 404):
   1. Ahrefs/SEMrush → Backlinks report → filter 404
   2. Fix: 301 redirect to relevant page OR restore the content
   3. Priority: high-authority domains → fix immediately
   ```

4. **Link Quality Assessment**:
   ```
   ✅ Good links: .edu, .gov, industry publications, high-traffic blogs, editorial links
   ⚠️ Questionable: link exchanges, paid links (must be nofollow/sponsored), article directories
   ❌ Toxic: PBNs (Private Blog Networks), comment spam, forum profile links, link farms

   Spam score factors: domain-wide outbound links, thin content, irrelevant niche
   Disavow: Use ONLY when you have a manual action or clear toxic link attack.
             Google is good at ignoring low-quality links. Disavow can hurt if misused.
   ```

### Phase 8: SEO Monitoring & Alerting

1. **GSC API Integration for Dashboards**:
   ```python
   from googleapiclient.discovery import build
   from google.oauth2 import service_account

   service = build('searchconsole', 'v1', credentials=creds)
   request = {
       'startDate': '2026-07-01',
       'endDate': '2026-07-31',
       'dimensions': ['query', 'page', 'device', 'country'],
       'rowLimit': 25000,
       'aggregationType': 'auto'
   }
   response = service.searchanalytics().query(
       siteUrl='https://example.com', body=request
   ).execute()
   ```

2. **Rank Tracking Architecture**:
   ```
   Tier 1 (Top 50 keywords): Daily tracking — API (SEMrush/AccuRanker)
   Tier 2 (50-500 keywords): Weekly tracking
   Tier 3 (500+ keywords): Bi-weekly or monthly via GSC average position

   Track: Position, SERP feature presence, competitor positions
   Store: Time-series database for trend analysis
   Alert: Position drop ≥ 3 spots on tier 1 keywords within 24 hours
   ```

3. **Competitor SERP Analysis**:
   ```
   Monthly cadence:
   1. For top 20 keywords: who moved up? who moved down?
   2. New entrants: who started ranking in the past 30 days?
   3. SERP feature changes: new featured snippet owner? New video carousel?
   4. Content changes: did top-ranking pages change their content/title/schema?
   ```

4. **Algorithm Update Response Plan**:
   ```
   Detection:
   - Monitor industry chatter (Search Engine Roundtable, WebmasterWorld, X/Twitter)
   - Check Semrush Sensor / MozCast / Algoroo for volatility spikes
   - Cross-reference with your own traffic changes

   Triage (within 24 hours of detected drop):
   ├── GSC Manual Actions → Fix and submit reconsideration request
   ├── Technical issue (noindex, robots.txt, server errors) → Fix immediately
   ├── Content quality → E-E-A-T audit of affected pages vs ranking pages
   ├── Link penalty → Backlink audit for toxic links (disavow only if manual action)
   └── Core update → Content improvement: depth, authority, user satisfaction signals

   Recovery timeline:
   - Technical fix: days to 2 weeks
   - Content improvement: 2-4 weeks (Google needs to re-crawl and re-evaluate)
   - Core update recovery: next core update cycle (3-6 months)
   ```

## Best Practices

- **Indexability is job #1** — You can't rank what Google can't index. Sitemaps, robots.txt, HTTP status codes, and canonicals are the foundation.
- **Renderability matters** — Google renders JavaScript. If content depends on JS, verify it's in the rendered HTML (GSC URL Inspection → View Crawled Page).
- **E-E-A-T is not optional for YMYL** — Medical, financial, legal content without demonstrated expertise will not rank.
- **Schema validates → Schema monitors** — Validate at deployment, monitor in GSC weekly. Schema errors can compound.
- **Core Web Vitals are cumulative** — Fix the worst-performing page first. One 10-second page drags down your entire origin's CrUX score.
- **Hreflang must be bidirectional** — EN→DE requires DE→EN. Broken hreflang is worse than no hreflang.
- **Link building is about relevance, not volume** — 5 links from authoritative industry publications > 500 directory links.
- **Algorithm updates happen every 3-6 months** — Don't panic-react. Wait for the update to finish rolling out (usually 2 weeks), then analyze.

## Cross-Skill Coordination

SEO touches content, engineering, marketing, and design. Rankings degrade when any of these operate in isolation.

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **Content Strategist** | Content planning, keyword strategy | Keyword targets, content gaps, SERP intent analysis |
| **Frontend Developer** | Core Web Vitals, structured data, rendering | CWVs scores, JS rendering audit, `<head>` markup requirements |
| **Backend Developer** | Sitemaps, redirects, URL structure, canonicals | Dynamic sitemap spec, redirect map, server-side rendering decisions |
| **Growth Engineer** | A/B testing SEO-safe parameters, landing pages | Canonical URL rules, noindex on test pages, traffic impact of experiments |
| **UX Designer** | Navigation, IA, mobile UX | Crawl depth analysis, mobile usability issues, internal linking structure |
| **System Architect** | CDN, page speed, SSR vs CSR | LCP/INP targets, caching strategy, rendering architecture impact on crawl budget |
| **Marketing/Demand Gen** | Campaign landing pages, paid search | Keyword cannibalization risks, landing page SEO requirements |
| **Data/Analytics** | GA4, Search Console, rank tracking | Event tracking for SEO metrics, GSC data integration, attribution modeling |
| **Technical Writer** | Documentation site, blog platform | Docs site crawlability, content hierarchy, schema markup for docs |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Site redesign or URL structure change | Content Strategist, Frontend Dev, Marketing | Redirect planning, content migration, traffic preservation |
| Core Web Vitals regression below threshold | Frontend Dev, System Architect, Project Manager | Performance blocks indexing; needs immediate fix |
| New JavaScript framework adoption (SPA → CSR) | System Architect, Frontend Dev, Content Strategist | JS rendering breaks crawlability; needs SSR/hydration review |
| Organic traffic drop >20% week-over-week | Marketing, Content Strategist, Growth Engineer | Algorithm update or technical regression; triage immediately |
| New subdomain or international site launch | System Architect, Content Strategist, Backend Dev | Domain authority split, hreflang, geo-targeting |
| Structured data errors in GSC | Frontend Dev, Backend Dev | Rich results eligibility lost; fix within 48 hours |
| Crawl budget exhaustion (log analysis shows) | System Architect, Backend Dev | Pages not indexed; prune or optimize crawl efficiency |

### Escalation Path

| Situation | Escalate To | Rationale |
|-----------|------------|-----------|
| Manual action (penalty) in GSC | **Legal Advisor** + VP Engineering | Legal risk if algorithmic; needs formal response plan |
| Competitor outranking on primary keyword after algorithm update | **Content Strategist** + Growth Engineer | Content quality + technical gap analysis required |
| Site migration (domain change) with traffic at risk | **CTO Advisor** + Project Manager | Cross-team coordination; executive visibility needed |
| SEO recommendations blocked by engineering for >2 sprints | **CTO Advisor** or VP Product | SEO debt compounds; needs prioritization authority |
| Paid and organic cannibalizing >30% overlap | **Marketing Lead** + Growth Engineer | Budget waste; needs channel alignment |

## Production Checklist

### Technical Foundation
- [ ] XML sitemap(s) valid, compressed, submitted to GSC — only canonical, indexable URLs
- [ ] robots.txt configured — blocks staging/dev, allows crawling, doesn't block CSS/JS
- [ ] All indexable pages have unique `<title>` (50-60 chars) and meta description (150-160 chars)
- [ ] Canonical tags: self-referencing, absolute URLs, consistent trailing slash policy
- [ ] Redirects: all single-hop 301s, no redirect chains, no redirect loops
- [ ] HTTPS everywhere — HSTS header with `max-age=31536000; includeSubDomains; preload`
- [ ] 404 pages return actual 404 status code (not soft 404), with helpful navigation

### Structured Data
- [ ] JSON-LD schema deployed on homepage: Organization + WebSite + SitelinksSearchBox
- [ ] Article schema on all blog posts with author Person entity
- [ ] Product schema on product pages with Offer, price, availability
- [ ] BreadcrumbList schema on all pages deeper than homepage
- [ ] FAQ/HowTo schema on eligible pages
- [ ] Zero errors in GSC Enhancements report
- [ ] Schema validated: Rich Results Test → Schema Markup Validator → GSC

### Core Web Vitals
- [ ] LCP < 2.5s (75th percentile) — CrUX + Lighthouse lab data confirmed
- [ ] INP < 200ms (75th percentile) — interaction responsiveness verified
- [ ] CLS < 0.1 (75th percentile) — visual stability confirmed
- [ ] Images optimized: WebP/AVIF, srcset, preloaded LCP, explicit dimensions
- [ ] Critical CSS inlined, non-critical CSS deferred, JS deferred/async
- [ ] No interstitials or intrusive popups per Google guidelines

### Content & International
- [ ] E-E-A-T signals present: author bios, credentials, contact info, trust signals
- [ ] Topic clusters: pillar pages + linked cluster content with descriptive anchors
- [ ] Content gap analysis complete for top 20 target keywords
- [ ] Hreflang: bidirectional, self-referencing, x-default, zero GSC errors (if multi-language)
- [ ] Localized keyword research per locale (not translated English keywords)

### JavaScript SEO
- [ ] Critical content rendered server-side (SSR/SSG) — visible in View Source
- [ ] Meta tags (title, description, canonical, hreflang) in server-rendered HTML
- [ ] Internal navigation uses `<a href>` or framework Link components
- [ ] Infinite scroll implements History API pushState or pagination with rel=next/prev

### Monitoring
- [ ] GSC integrated: manual weekly check + API dashboard for daily metrics
- [ ] Rank tracking: top 50 keywords daily, 50-500 weekly
- [ ] Core Web Vitals dashboard: CrUX data + lab data trended over time
- [ ] Algorithm update monitoring: volatility alerts (SERP tracking tool)
- [ ] Backlink monitoring: new links detected, toxic links flagged, broken backlinks tracked
- [ ] SEO on-call: 24-hour response SLA for >20% traffic drop or manual action

## When NOT to Use This Skill (Overkill)

- **Pre-launch startup with 0 users** — `<title>`, sitemap, robots.txt. Ship and iterate.
- **Internal tools / admin dashboards behind auth** — Focus on UX, not search engines.
- **Single Page App with <10 pages** — Manual review + GSC. Don't over-engineer.
- **API-only service with no public pages** — SEO is irrelevant.
- **Ranking #1 for all target keywords** — Shift to CRO (conversion rate optimization).

## References

- [Google Search Central — SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)
- [Schema.org — Full Hierarchy](https://schema.org/docs/full.html)
- [web.dev — Core Web Vitals](https://web.dev/vitals/)
- [Google Search Central — Crawl Budget Management](https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget)
- [Google Search Central — JavaScript SEO Basics](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics)
- [Google Rich Results Test](https://search.google.com/test/rich-results)
- [Schema Markup Validator](https://validator.schema.org/)
- [Ahrefs — Link Building Guide](https://ahrefs.com/blog/link-building/)
- [Search Engine Roundtable (algorithm updates)](https://www.seroundtable.com/)
- [Google Search Central Blog](https://developers.google.com/search/blog)
