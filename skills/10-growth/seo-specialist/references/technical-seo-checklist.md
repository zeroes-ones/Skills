# Technical SEO Checklist

## Crawl & Index

### robots.txt
- [ ] Correctly configured — not blocking important resources
- [ ] Sitemap URL referenced
- [ ] No `Disallow: /` on production

### Sitemap
- [ ] XML sitemap exists at `/sitemap.xml`
- [ ] All canonical URLs included
- [ ] `lastmod` dates accurate
- [ ] No 4xx/5xx URLs in sitemap
- [ ] Sitemap submitted to Google Search Console

### Canonical Tags
- [ ] Every page has `<link rel="canonical">` pointing to canonical URL
- [ ] No canonical chains (A→B→C)
- [ ] Canonical matches actual URL or is intentional cross-domain

### Meta Tags
- [ ] Unique `<title>` per page (50-60 chars)
- [ ] Unique `<meta description>` per page (150-160 chars)
- [ ] `<meta robots>` not accidentally blocking indexing
- [ ] Open Graph tags for social sharing
- [ ] Twitter Card tags

## Technical Foundation

### URLs
- [ ] Clean, descriptive URLs (no query params for content pages)
- [ ] Hyphens, not underscores: `/blog/seo-guide` not `/blog/seo_guide`
- [ ] Consistent trailing slash policy (pick one, redirect the other)
- [ ] No URL parameters for tracking without canonical

### HTTPS
- [ ] TLS 1.2+ enforced
- [ ] HTTP→HTTPS redirect (301)
- [ ] No mixed content warnings
- [ ] HSTS header set with reasonable max-age

### Redirects
- [ ] All redirects are 301 (permanent) or 302 (temporary)
- [ ] No redirect chains (A→B→C)
- [ ] No redirect loops
- [ ] Broken redirects monitored

### Status Codes
- [ ] 200 for valid pages
- [ ] 301/302 for redirects
- [ ] 404 for not found (custom page helpful)
- [ ] 410 for permanently removed content
- [ ] No soft 404s (200 with "not found" content)

## Performance (Core Web Vitals)

### LCP (Largest Contentful Paint)
- [ ] Target: < 2.5 seconds
- [ ] Optimize hero images (lazy load, modern format, correct size)
- [ ] Preload critical resources (fonts, hero image)
- [ ] Minimize render-blocking resources

### INP (Interaction to Next Paint)
- [ ] Target: < 200ms
- [ ] Avoid long tasks (>50ms on main thread)
- [ ] Use web workers for heavy computation
- [ ] Debounce/throttle event handlers

### CLS (Cumulative Layout Shift)
- [ ] Target: < 0.1
- [ ] Set explicit dimensions on images, videos, embeds
- [ ] Reserve space for dynamic content (ads, banners)
- [ ] Avoid inserting content above existing content

## Structured Data

### Schema.org JSON-LD
- [ ] Organization schema on homepage
- [ ] Article/BlogPosting on blog posts
- [ ] Product schema on product pages (if e-commerce)
- [ ] BreadcrumbList on all pages
- [ ] FAQ schema on FAQ pages
- [ ] Validated in Rich Results Test

### Implementation
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Company Name",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "sameAs": [
    "https://twitter.com/company",
    "https://linkedin.com/company/company"
  ]
}
```

## Mobile SEO
- [ ] Responsive design — no separate mobile URLs
- [ ] Mobile-friendly test passes (Google Search Console)
- [ ] Tap targets > 48px
- [ ] Font size readable without zoom (≥16px)
- [ ] No horizontal scroll on mobile

## International SEO (if applicable)
- [ ] `hreflang` tags for language/region variants
- [ ] Proper locale in URL: `/en/`, `/en-us/`, `/es/`
- [ ] No automatic redirects based on IP
- [ ] geo-targeting in Search Console (if country-specific)

## Monitoring
- [ ] Google Search Console connected
- [ ] Core Web Vitals monitored (CrUX dashboard)
- [ ] 404 errors tracked
- [ ] Index coverage issues reviewed weekly
- [ ] Manual actions checked monthly
