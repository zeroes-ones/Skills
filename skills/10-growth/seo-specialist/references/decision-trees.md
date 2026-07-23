# SEO Decision Trees

<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### Traffic Decline Diagnosis
```
                     ┌──────────────────────────────┐
                     │ START: Organic traffic drop    │
                     │ >20% week-over-week            │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Drop is sudden (1-3 days)      │
                    │ vs gradual (weeks)?            │
                    └────┬──────────────────────┬───┘
                         │ Sudden               │ Gradual
                    ┌────▼──────────┐    ┌──────▼──────────┐
                    │ Check GSC     │    │ Check GSC for   │
                    │ Manual Actions│    │ declining avg   │
                    │ → Penalty?    │    │ position across │
                    └──┬────────┬───┘    │ keywords        │
                       │YES     │NO      └──┬──────────┬────┘
                  ┌────▼───┐ ┌─▼────────┐   │YES       │NO
                  │File    │ │Server 5xx │ ┌─▼──────┐ ┌─▼──────────┐
                  │recon-  │ │or robots │ │Algorithm│ │Competitor  │
                  │sideration│ │.txt      │ │Update:  │ │Gained:     │
                  │request │ │blocking? │ │Content  │ │Analyze     │
                  │and fix │ │Fix issue │ │refresh +│ │SERP overlap│
                  │cause   │ └──────────┘ │E-E-A-T  │ │+ gap       │
                  └────────┘              │improve  │ │analysis    │
                                          └─────────┘ └────────────┘
```
**When to suspect manual action:** Sudden drop with GSC notification — check manual actions report, fix violation, submit reconsideration request.
**When to suspect technical issue:** Sudden drop, no GSC penalty — check server logs (5xx), robots.txt, noindex tags, sitemap accessibility.
**When to suspect algorithm update:** Gradual decline, positions slipping across terms — align with known Google updates (Semrush Sensor, MozCast), improve content E-E-A-T.
**When to suspect competitor gain:** Your positions unchanged but traffic down — competitor took SERP features (featured snippet, PAA, image pack) eating your CTR.

### International SEO: ccTLD vs Subdirectory vs Subdomain
```
                     ┌──────────────────────────────┐
                     │ START: Multi-language/region   │
                     │ site architecture?             │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Have local team + budget for   │
                    │ separate domains AND need      │
                    │ geo-targeting signal?          │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────┐    ┌──────────▼──────────┐
                    │ ccTLD     │    │ Want to consolidate │
                    │ (example. │    │ domain authority?   │
                    │ de,       │    └──┬──────────────┬────┘
                    │ example.  │       │YES          │NO
                    │ fr)       │  ┌────▼────┐ ┌──────▼─────────┐
                    │ Strongest │  │Subdirect-│ │Subdomain       │
                    │ geo-signal│  │ory:      │ │(de.example.com)│
                    │ Cost: $$  │  │example   │ │Moderate geo    │
                    │ per domain│  │.com/de/  │ │signal, easier  │
                    └───────────┘  │Weak geo  │ │ops separation  │
                                   │signal,   │ └────────────────┘
                                   │best for  │
                                   │SEO auth  │
                                   └──────────┘
```
**When to choose ccTLD:** Dedicated country presence, local team, local hosting, and budget for separate domains — strongest geo-targeting signal to Google.
**When to choose Subdirectory:** Want to consolidate domain authority (backlinks count toward main domain) — weaker geo-signal but best for unified SEO.
**When to choose Subdomain:** Separate tech stacks per market (different CMS, server), moderate geo-signal via GSC geo-targeting, easier operational split.

### JavaScript Rendering Strategy
```
                     ┌──────────────────────────────┐
                     │ START: JS-heavy site — how     │
                     │ to handle indexing?            │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Site is primarily SPA (React,   │
                    │ Vue, Angular) with CSR?         │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────────┐    ┌──────▼──────────┐
                    │ Viable to     │    │ Partial JS —     │
                    │ migrate to    │    │ key content in   │
                    │ SSR/SSG       │    │ HTML but some    │
                    │ (Next.js,     │    │ dynamic?         │
                    │ Nuxt.js)?     │    └──┬──────────┬────┘
                    └──┬────────┬───┘       │YES       │NO
                       │YES     │NO     ┌────▼────┐ ┌──▼──────────┐
                  ┌────▼───┐ ┌─▼──────┐│Hybrid:  │ │Full SSR/SSG │
                  │Migrate │ │Dynamic ││SSR for  │ │recommended  │
                  │to Next │ │Render  ││critical │ │for all SEO- │
                  │.js/Nuxt│ │(Prerender││pages, CSR│ │sensitive    │
                  │or Remix│ │io,     ││for app  │ │content      │
                  │(SSR/SSG│ │Puppeteer││features │ └─────────────┘
                  │preferred)│ │Service)│└─────────┘
                  └────────┘ └────────┘
```
**When to migrate to SSR/SSG:** Primary choice for SEO-dependent sites — Next.js (React), Nuxt (Vue), Remix, SvelteKit. Full control, best Core Web Vitals.
**When to use Dynamic Rendering:** Can't migrate from SPA (legacy, team constraints) — Prerender.io or Puppeteer service serves static HTML to bots only.
**When to use Hybrid:** Most of site is app-like but marketing/blog pages need SEO — SSR for public-facing pages, CSR for logged-in features.

### Crawl Budget Optimization
```
                     ┌──────────────────────────────┐
                     │ START: Crawl budget wasted?    │
                     │ (GSC: discovered-not-indexed)  │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Faceted navigation generating  │
                    │ >10K low-value URLs (filters,  │
                    │ sort variants, pagination)?    │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────────┐    ┌──────▼──────────┐
                    │Block in      │    │ Thin/duplicate   │
                    │robots.txt or │    │ content pages    │
                    │canonicalize  │    │ (<300 words,     │
                    │+ noindex     │    │ >50% duplicate)? │
                    │parameterized │    └──┬──────────┬────┘
                    │URLs          │       │YES       │NO
                    └──────────────┘  ┌────▼────┐ ┌──▼──────────┐
                                      │Consolidate│ │Slow server  │
                                      │or improve│ │response?    │
                                      │content to│ │Optimize TTFB│
                                      │>500 words│ │<200ms,       │
                                      │unique    │ │upgrade infra│
                                      └──────────┘ └────────────┘
```
**When to block + canonicalize:** Facets/filters/sort producing 10K+ low-value URLs — disallow in robots.txt, canonical to root, noindex parameter URLs.
**When to consolidate thin content:** Pages <300 words, >50% duplicate — merge into comprehensive resources, 301 redirect, or improve to 500+ unique words.
**When to optimize server:** Crawl delay from slow TTFB — optimize to <200ms, reduce page size, upgrade hosting, enable caching.

### Link Building: Strategy Selection
```
                     ┌──────────────────────────────┐
                     │ START: Which link building     │
                     │ strategy to prioritize?        │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Have high-quality, unique data │
                    │ or research (original surveys, │
                    │ industry benchmarks)?          │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────────┐    ┌──────▼──────────┐
                    │Digital PR +  │    │ Have existing    │
                    │Data Journalism│    │ broken pages    │
                    │Pitch original│    │ with backlinks   │
                    │research to   │    │ pointing to them?│
                    │journalists   │    └──┬──────────┬────┘
                    └──────────────┘       │YES       │NO
                                      ┌────▼────┐ ┌──▼──────────┐
                                      │Broken   │ │Expert roundup│
                                      │Link      │ │or guest post │
                                      │Building: │ │on relevant   │
                                      │find broke│ │sites with    │
                                      │links →   │ │high DR +     │
                                      │offer your│ │traffic       │
                                      │resource  │ └──────────────┘
                                      └──────────┘
```
**When to use Digital PR:** Unique data/research that journalists want — original surveys, industry reports, data studies. Highest ROI but requires data capabilities.
**When to use Broken Link Building:** Find dead pages with backlinks in your niche using Ahrefs/Semrush — reach out with your relevant replacement resource.
**When to use Expert/Guest Posting:** No unique data — contribute expert insights to authoritative sites in your niche; focus on quality over quantity.
