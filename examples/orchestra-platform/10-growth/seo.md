# SEO Audit — July 2026

## Core Web Vitals

Measured via Google PageSpeed Insights and Chrome User Experience Report (CrUX) for `orchestra.dev`:

| Metric | Mobile | Desktop | Threshold (Good) |
|--------|--------|---------|-------------------|
| LCP (Largest Contentful Paint) | 1.8s | 0.9s | ≤ 2.5s |
| FID (First Input Delay) | 12ms | 8ms | ≤ 100ms |
| INP (Interaction to Next Paint) | 94ms | 62ms | ≤ 200ms |
| CLS (Cumulative Layout Shift) | 0.04 | 0.02 | ≤ 0.1 |
| TTFB (Time to First Byte) | 210ms | 85ms | ≤ 800ms |

All metrics pass Google's "Good" threshold. Improvements from June: TTFB reduced from 380ms to 210ms (mobile) by enabling CloudFront Origin Shield and moving the BFF to `us-east-1` (same region as CloudFront).

## Structured Data

Three schema.org types implemented via JSON-LD in Next.js `generateMetadata()`:

- **TechArticle** on blog posts: includes `headline`, `author`, `datePublished`, `dateModified`, `description`. Tested with Google Rich Results Test — eligible for "Article" rich result.
- **SoftwareApplication** on the homepage: includes `applicationCategory: "DeveloperApplication"`, `operatingSystem: "Web"`, `offers` (pricing tiers). Eligible for software app rich result.
- **BreadcrumbList** on all pages: dynamic generation from the App Router path segments. Validated and rendering in SERPs.

## Keyword Strategy

Primary keywords with monthly search volume (Ahrefs data, July 2026):

| Keyword | Volume | Difficulty | Current Rank | Target |
|---------|--------|------------|--------------|--------|
| "internal developer platform" | 8,200/mo | 42 | #14 | Top 5 |
| "platform engineering tool" | 5,400/mo | 38 | #22 | Top 10 |
| "Backstage alternative" | 3,100/mo | 35 | #7 | Top 3 |
| "developer portal software" | 2,800/mo | 40 | #31 | Top 10 |
| "build vs buy IDP" | 1,900/mo | 22 | #4 | #1 |
| "golden path template" | 1,200/mo | 12 | #2 | #1 |
| "plugin-driven platform" | 720/mo | 8 | #1 | Maintain #1 |

## Technical SEO Fixes

**Completed**: Canonical URLs on all pages (self-referencing, prevents duplicate content from query params). Dynamic `sitemap.xml` via Next.js `generateSitemaps()` — includes all static and ISR pages, 218 URLs indexed (Google Search Console, last 7 days). `robots.txt` allows all crawlers, points to sitemap. `hreflang` tags implemented for English (`en-US`) and German (`de-DE`) locales — verified in Google Search Console's International Targeting report, no errors.

**In Progress**: Image optimization — 12 blog post hero images over 500KB need conversion to WebP/AVIF with responsive `srcset`. Expected completion: July 25.

## Backlink Strategy

Current domain rating (Ahrefs DR): 27. Target: DR 40 by Q4 2026.

- **Guest posts**: 3 posts in pipeline — "The New Stack" (platform engineering deep dive, Aug), "DevOps.com" (CI/CD integration case study, Sep), "InfoQ" (plugin architecture, Oct).
- **Podcast appearances**: 4 recorded — "The Changelog" (aired June 15, #438), "Kubernetes Podcast" (airs Aug 1), "DevOps Chat" (scheduled Sep), "Screaming in the Cloud" (scheduled Oct).
- **HARO (Help a Reporter Out)**: Responding to 3–5 journalist queries/week related to platform engineering, DevOps, developer tools. 2 backlinks earned (TechCrunch mention, Forbes Technology Council roundup).
