## Core Workflow

### Phase 0 (~20 min): Discovery — Audience, Budget, Content, Updates

Before writing a single line of code or choosing a platform, answer five questions. The answers determine the entire stack.

**1. Audience:** Who visits the site? Technical (devs, engineers) → minimal JS, max speed. General consumer (shopping, reading) → mobile-first, SEO-critical. Enterprise (procurement, compliance) → accessibility, security, PDF generation.

**2. Budget:** Monthly hosting budget in one of four tiers: $0 (static site, no server), $5-20 (JAMstack with serverless), $20-100 (full CMS or e-commerce platform), $100+ (custom SaaS, high traffic). Multiply the budget by 12 to get the annual commitment.

**3. Content type:** Static text/images (blog, portfolio → SSG). Products with inventory (e-commerce → Shopify/Medusa). User-generated content (forums, reviews → dynamic app). Real-time data (dashboards → SSR framework).

**4. Update frequency:** Quarterly or less (markdown + git is fine). Weekly (Git-based CMS like Decap/Tina). Daily by non-technical team (headless CMS or Webflow). Hourly by automation (headless CMS with webhooks).

**5. Technical owner:** Is there a developer on staff who will maintain this? Yes → custom stack is viable. No → use a managed platform (Webflow, Shopify, Squarespace). A site without a maintainer becomes a security liability within 12 months.

**Discovery output:** One-page document with all five answers. Stack selection follows directly from this document — no guessing.

### Phase 1 (~30 min): Stack Selection — Decision Matrix

Map discovery answers to stack recommendations using this matrix:

| Requirement | Best Stack | Why |
|-------------|-----------|-----|
| Static content, $0 budget, dev maintainer | Astro + Cloudflare Pages | Zero JS by default, global CDN, unlimited free bandwidth |
| Static content, non-dev editor, $0-20/mo | Astro + Decap CMS + Netlify | Git-based CMS, visual preview, free tier handles moderate traffic |
| Blog/news, high volume (1000+ posts) | Hugo + GitHub Pages | Fastest build times (1ms/page), single binary, no Node dependency |
| E-commerce, 10-100 products, non-dev owner | Shopify ($29/mo as of 2026) | Managed checkout, inventory, shipping, 24/7 support, huge app ecosystem |
| E-commerce, 100+ products, developer team | Medusa (self-hosted) + Next.js storefront | Full customization, multi-currency, no platform lock-in, open-source |
| SaaS app, auth, dashboard, database | Next.js + Vercel + Supabase | SSR/SSG hybrid, serverless functions, free Postgres tier |
| Marketing site, design-heavy, non-dev team | Webflow ($14-39/mo as of 2026) | Visual designer, CMS built in, hosting included, client-handoff friendly |
| Landing page, rapid launch, solo founder | Framer ($5-30/mo as of 2026) | Design → publish in hours, animations built in, no code required |
| Portfolio, photographer/designer, $0 budget | Astro + Cloudflare Pages | Image optimization built in, zero hosting cost, excellent Lighthouse scores |
| Documentation site, open-source project | Starlight (Astro) or VitePress | Markdown-native, search built in, versioned docs, full i18n support |
| Client-handoff site, agency | WordPress + Kinsta ($30/mo as of 2026) | Client knows WordPress, managed hosting with auto-updates, WAF included |

### Phase 2 (~15-60 min): Scaffolding — Project Setup

**Astro (recommended for most content sites):**
```bash
npm create astro@latest           # Choose: Empty project, TypeScript strict, no SSR adapter yet
cd my-site
npx astro add tailwind            # Add Tailwind CSS integration
npm install @astrojs/sitemap      # Sitemap generation
npm install @astrojs/partytown    # Offload third-party scripts to web worker
```

**Next.js (for SaaS/dynamic sites):**
```bash
npx create-next-app@latest my-app --typescript --tailwind --eslint --app --src-dir
cd my-app
npm install next-sitemap           # Sitemap generation (postbuild)
```

**Hugo (for documentation/large content sites):**
```bash
hugo new site my-docs
cd my-docs
git init
git submodule add https://github.com/adityatelange/hugo-PaperMod themes/PaperMod
echo "theme = 'PaperMod'" >> hugo.toml
```

**11ty (Eleventy):**
```bash
mkdir my-blog && cd my-blog
npm init -y
npm install @11ty/eleventy
echo 'module.exports = function(eleventyConfig) { return { dir: { input: "src", output: "_site" } }; };' > .eleventy.js
mkdir src && echo '# Hello' > src/index.md
```

**Scaffolding checklist (all stacks):**
- [ ] `.gitignore` includes `node_modules`, `.env`, build output directories
- [ ] `.env.example` committed (`.env` in `.gitignore`)
- [ ] `README.md` with setup instructions
- [ ] Build scripts: `dev`, `build`, `preview`
- [ ] Linting configured (ESLint/Prettier)

### Phase 3 (~2-8 hours): Design System — Visual Foundation

Use Tailwind CSS as the default recommendation. It enforces consistency, prevents CSS bloat (purges unused styles), and is the most portable design system across frameworks.

**Typography scale (Tailwind config):**
```js
// tailwind.config.js
theme: {
  fontSize: {
    'xs': ['0.75rem', { lineHeight: '1rem' }],
    'sm': ['0.875rem', { lineHeight: '1.25rem' }],
    'base': ['1rem', { lineHeight: '1.5rem' }],
    'lg': ['1.125rem', { lineHeight: '1.75rem' }],
    'xl': ['1.25rem', { lineHeight: '1.75rem' }],
    '2xl': ['1.5rem', { lineHeight: '2rem' }],
    '3xl': ['1.875rem', { lineHeight: '2.25rem' }],
    '4xl': ['2.25rem', { lineHeight: '2.5rem' }],
    '5xl': ['3rem', { lineHeight: '1.1' }],
  }
}
```

**Color system:** Define 3-5 semantic color tokens. Never use raw hex values in components.
- `primary` — brand color, used for CTAs, links, accent elements
- `neutral` — text, backgrounds, borders (grayscale)
- `success`, `warning`, `danger` — semantic feedback colors
- All colors must pass WCAG 2.2 AA contrast ratios (4.5:1 normal text, 3:1 large text)

**Spacing scale:** Use Tailwind's default 4px grid (0.25rem increments). Never use arbitrary pixel values. Consistency in spacing is more visible than consistency in typography.

**Component inventory** (build these first):
- Button (3 variants: primary, secondary, ghost; 3 sizes: sm, md, lg)
- Input (text, email, textarea, select; error, disabled, focus states)
- Card (image + title + description + CTA)
- Navigation (mobile hamburger → desktop horizontal)
- Footer (links, social, copyright)
- Hero section (headline, subheadline, CTA, image/video)

### Phase 4 (~2-8 hours): Content Architecture

**Markdown structure (for SSGs):**
```
src/content/
├── blog/
│   ├── 2024-01-hello-world.md
│   ├── 2024-02-second-post.md
│   └── _drafts/
│       └── upcoming-post.md
├── pages/
│   ├── about.md
│   ├── contact.md
│   └── pricing.md
└── data/
    ├── navigation.yml       # Site navigation structure
    ├── authors.yml          # Multi-author blog metadata
    └── testimonials.yml     # Reusable testimonial data
```

**Frontmatter standard (YAML in markdown):**
```yaml
---
title: "How to Build a $0 Website in 2026"
description: "Complete guide to building and hosting a production website for free using Astro and Cloudflare Pages."
publishDate: 2026-07-24
author: jane-doe
tags: [astro, cloudflare, web-development]
featuredImage: ./images/astro-cloudflare.png
draft: false
---
```

**Content modeling (for headless CMS):**
- Blog: title, slug, body, excerpt, author (reference), publishDate, tags (array), featuredImage
- Product: name, slug, description, price, images (array), category (reference), inventory, variants (array of {size, color, stock})
- Page: title, slug, sections (array of flexible content blocks — hero, features, testimonials, CTA, FAQ)

**Content update workflow:**
- Developer pushes content → Git triggers build → site deploys (CI/CD)
- Editor saves in CMS → CMS triggers webhook → site rebuilds → deploys
- Schedule content: use draft status + future `publishDate` → build process filters out unpublished content


### Phase 5 (~2-4 hours): SEO Foundation

SEO is not a post-launch activity — it is scaffolding. Every page must ship with complete SEO metadata from day one.

**Layout-level SEO (applied to every page):**
```html
<!-- In <head> of base layout -->
<title>{pageTitle} | {siteName}</title>
<meta name="description" content="{pageDescription}" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<link rel="canonical" href="{canonicalUrl}" />
<meta name="robots" content="index, follow" />

<!-- Open Graph (Facebook, LinkedIn, Slack, Discord) -->
<meta property="og:title" content="{ogTitle}" />
<meta property="og:description" content="{ogDescription}" />
<meta property="og:image" content="{ogImageUrl}" />
<meta property="og:url" content="{canonicalUrl}" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="{siteName}" />

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{twitterTitle}" />
<meta name="twitter:description" content="{twitterDescription}" />
<meta name="twitter:image" content="{twitterImage}" />

<!-- Structured Data (JSON-LD) -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "{siteName}",
  "url": "{siteUrl}",
  "description": "{siteDescription}"
}
</script>
```

**Per-page structured data (choose based on content type):**
- Blog post: `@type: Article` or `@type: BlogPosting` — include author, datePublished, dateModified, image, publisher
- Product: `@type: Product` — include name, description, image, offers (price, currency, availability), aggregateRating
- Organization: `@type: Organization` — include name, url, logo, sameAs (social profiles), contactPoint
- FAQ page: `@type: FAQPage` with `mainEntity` array of `@type: Question` / `@type: Answer` pairs
- Local business: `@type: LocalBusiness` — include address, geo, openingHours, telephone

**Sitemap generation:**
- Every framework has a sitemap plugin: `@astrojs/sitemap`, `next-sitemap`, Hugo's built-in `[sitemap]`
- Sitemap must include `<lastmod>` dates for content freshness signals
- Exclude: 404 page, thank-you pages, admin pages, draft content
- Submit sitemap URL to Google Search Console and Bing Webmaster Tools on launch day

**robots.txt (minimal, permissive):**
```
User-agent: *
Allow: /
Sitemap: https://example.com/sitemap-index.xml
```
Common mistake: `Disallow: /` during development and forgetting to remove it. Check robots.txt on launch day.

**URL design rules:**
- Lowercase, hyphens between words (`/how-to-build-website`, not `/HowToBuildWebsite` or `/how_to_build_website`)
- No trailing slashes (choose one style, redirect the other)
- Short, descriptive slugs (3-5 words max)
- No dates in URLs for evergreen content (or use `/blog/2024/01/slug` if you must)
- 301 redirect all old URLs to new URLs — never break a URL that has backlinks

### Phase 6 (~3-6 hours): Performance Optimization

The goal: Lighthouse score of 95-100 on mobile, LCP < 2.5s on 4G, zero render-blocking resources.

**Image optimization pipeline:**
- **Format:** Serve WebP (92% browser support) with AVIF fallback (88% support as of 2026). Never serve uncompressed PNG/JPEG.
- **Responsive images:** Use `<img srcset>` or `<picture>` with at least 3 breakpoints (320w, 768w, 1280w).
- **Lazy loading:** `loading="lazy"` on all below-the-fold images. `fetchpriority="high"` on LCP image (hero).
- **Dimensions:** Always include `width` and `height` attributes to prevent CLS (layout shift).
- **Automation:** Astro's `@astrojs/image`, Next.js `next/image`, or a build-time sharp/imagemagick pipeline. Never manually resize images.
- **Budget:** Hero image < 100KB. Thumbnails < 20KB. Full-width images < 200KB. Total image weight per page < 500KB.

**Font loading strategy:**
- Self-host fonts (no Google Fonts CDN) — eliminates external DNS lookup and connection negotiation
- Use `font-display: swap` to show fallback text immediately while custom font loads
- Subset fonts to only used characters (Latin, numbers, punctuation) — reduces font files from 200KB to 30KB
- Preload critical font files: `<link rel="preload" href="/fonts/inter-var.woff2" as="font" crossorigin>`

**CSS optimization:**
- Tailwind with JIT mode: only ships CSS classes that are actually used. Production build typically 3-10KB (gzipped).
- Inline critical CSS (above-the-fold styles) in `<head>` — eliminates render-blocking CSS for first paint
- Defer non-critical CSS with `media="print" onload="this.media='all'"` pattern
- Remove unused CSS: Tailwind purge, PurgeCSS, or manual audit with Chrome DevTools Coverage panel

**JavaScript optimization:**
- Zero JS for static content pages — Astro ships 0KB by default. You don't need JavaScript for a blog post or landing page.
- `type="module"` for modern JS — automatically deferred, no need for `async`/`defer`
- Dynamic `import()` for below-the-fold interactivity (modals, search, filters)
- Offload third-party scripts (analytics, chat widgets, ads) to a web worker using Partytown
- Audit bundle with `webpack-bundle-analyzer`, `rollup-plugin-visualizer`, or Lighthouse's "Reduce JavaScript" audit

**Edge caching (platform-specific):**
- Cloudflare Pages: automatic — all assets cached at edge (330+ cities). HTML: `max-age=0, must-revalidate`. Hashed assets: `max-age=31536000, immutable`.
- Vercel: add `stale-while-revalidate` for HTML. Static assets auto-cached at edge.
- Netlify: `Cache-Control` headers in `netlify.toml` or `_headers` file.
- Self-hosted: Nginx `expires` directive or CDN (Cloudflare, Fastly, BunnyCDN).

### Phase 7 (~2-4 hours): Accessibility — WCAG 2.2 AA

Accessibility is not optional — it is a legal requirement (ADA, Section 508, EN 301 549) and a moral obligation. 15% of the global population has a disability.

**Automated audit (first pass, catches 30-40% of issues):**
- Run `axe DevTools` (browser extension) or `@axe-core/cli` in CI: `npx @axe-core/cli https://example.com`
- Run Lighthouse accessibility audit (scores 0-100; target: 100)
- Integrate `eslint-plugin-jsx-a11y` for React, `eslint-plugin-vuejs-accessibility` for Vue

**Manual audit (catches the remaining 60-70%):**
- **Keyboard navigation:** Tab through every page. Can you reach every link, button, and form control? Is there a visible focus ring? Does the tab order match the visual order?
- **Screen reader:** Test with VoiceOver (Mac, free), NVDA (Windows, free), or TalkBack (Android, free). Can you complete every task without seeing the screen?
- **Zoom test:** Zoom to 200%. Does content reflow without horizontal scrolling? Do all interactive elements remain visible and usable?
- **Motion sensitivity:** Respect `prefers-reduced-motion` media query. Disable all animations and transitions when set.

**Critical ARIA patterns:**
```html
<!-- Hamburger menu button -->
<button aria-expanded="false" aria-controls="mobile-menu" aria-label="Open menu">
  <span class="sr-only">Menu</span>
  <svg>...</svg>
</button>

<!-- Screen-reader-only text (Tailwind) -->
<span class="sr-only">Skip to main content</span>

<!-- Navigation landmark -->
<nav aria-label="Primary navigation">...</nav>
<nav aria-label="Breadcrumb">...</nav>

<!-- Form error association -->
<label for="email">Email address</label>
<input id="email" aria-describedby="email-error" aria-invalid="true" />
<span id="email-error" role="alert">Please enter a valid email address.</span>
```

**Color contrast requirements:**
- Normal text (< 18pt or < 14pt bold): 4.5:1 minimum
- Large text (≥ 18pt or ≥ 14pt bold): 3:1 minimum
- UI components (buttons, inputs, icons): 3:1 minimum against adjacent colors
- Test with WebAIM Contrast Checker or Chrome DevTools color picker (shows contrast ratio)

### Phase 8 (~1-3 hours): Analytics & Monitoring

**Privacy-first analytics (GDPR-compliant without cookie banners):**
| Tool | Cost (as of 2026) | Privacy Model | Best For |
|------|------------------|----------------|----------|
| Plausible | $0 (self-hosted) / $9/mo (cloud) | No cookies, no personal data, open-source | General website analytics |
| Umami | $0 (self-hosted) / $9/mo (cloud) | No cookies, no personal data, open-source | General website analytics |
| Fathom | $14/mo | No cookies, anonymized, GDPR-compliant | Simpler alternative to Plausible |
| Google Analytics 4 | $0 | Cookies, personal data (requires consent banner) | Enterprise, advanced segmentation |

**Recommendation:** Plausible or Umami (self-hosted on Railway/Render for $0-5/mo). 30-second setup script. No cookie consent banner needed. Covers 95% of what most sites need: pageviews, bounce rate, visit duration, referrers, top pages, UTM campaign tracking.

**Core Web Vitals monitoring:**
- **Lighthouse CI:** Run in CI/CD on every deploy. Set budget assertions: Performance ≥ 90, Accessibility = 100, SEO = 100.
- **Web Vitals library:** Install `web-vitals` npm package. Report LCP, INP (Interaction to Next Paint, replacing FID in 2024), CLS, and TTFB to your analytics.
- **CrUX (Chrome User Experience Report):** Free real-user data from Chrome — available in PageSpeed Insights, Search Console, and BigQuery.
- **Synthetic monitoring:** Set up SpeedCurve, Calibre, or Checkly for scheduled Lighthouse runs from multiple geographic regions ($20-50/mo as of 2026).

**Error and uptime monitoring:**
- **Uptime:** Upptime (free, open-source, GitHub Actions-based) or Better Uptime ($24/mo as of 2026). Pings your site every 5 minutes, alerts on Slack/email.
- **Error tracking:** Sentry (free tier: 5K errors/month) for JS errors. Log errors from edge functions/serverless to a centralized dashboard.
- **404 monitoring:** Check Google Search Console → Coverage report for 404 errors. Redirect broken URLs or restore missing content.

### Phase 9 (~1-3 hours): Deployment — CI/CD & Launch

**Pre-launch checklist (complete before first production deploy):**
- [ ] Custom domain purchased and verified (Namecheap, Cloudflare Registrar, Porkbun — all ~$10-15/yr)
- [ ] DNS configured: `CNAME` record pointing to host, `CAA` record allowing Let's Encrypt (if needed)
- [ ] SSL certificate active (Let's Encrypt — free, auto-renewing on all recommended platforms)
- [ ] HTTPS redirect enforced: all HTTP requests → 301 → HTTPS
- [ ] WWW decision made and enforced: `example.com` → `www.example.com` (or vice versa) via 301 redirect
- [ ] Build succeeds in CI/CD: all pages render, no broken links, no console errors
- [ ] `.env` variables configured in hosting dashboard (not committed to repo)
- [ ] Cache headers verified: `Cache-Control` headers correct for HTML vs static assets
- [ ] Sitemap accessible at `/sitemap-index.xml` or `/sitemap.xml`
- [ ] robots.txt accessible and not blocking search engines

**CI/CD pipeline (GitHub Actions example for Astro + Cloudflare Pages):**
```yaml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm ci
      - run: npm run build
      - run: npx astro check          # Type checking
      - run: npx @axe-core/cli _site/ # Accessibility audit
      - run: npx wrangler pages deploy _site/ --project-name=my-site
```

**Post-launch actions (day of launch):**
1. Submit sitemap to Google Search Console and Bing Webmaster Tools
2. Request indexing for homepage and key pages (Search Console → URL Inspection → Request Indexing)
3. Verify Google Analytics/Plausible is receiving data
4. Test Core Web Vitals in PageSpeed Insights (mobile + desktop)
5. Set up Google Search Console email alerts (coverage issues, manual actions)
6. Share on social media with proper Open Graph tags (use `opengraph.xyz` to verify)

### Phase 10 (~ongoing): Maintenance — Content, Dependencies, Security

**Weekly (5-15 min):**
- Check analytics: traffic trends, top pages, bounce rate anomalies
- Check Search Console: new coverage issues, manual actions, security issues
- Publish content according to editorial calendar

**Monthly (15-30 min):**
- `npm outdated` → review and update dependencies (patch versions: auto-merge; minor: review changelog; major: plan migration)
- Run Lighthouse audit on top 5 pages (traffic-weighted)
- Check 404 errors in Search Console → redirect or restore
- Review form submissions for spam patterns → add honeypot/CAPTCHA if needed

**Quarterly (1-2 hours):**
- Full accessibility audit (axe DevTools + manual keyboard + screen reader)
- Review all third-party scripts (analytics, chat, ads) — remove any that are unused or slow
- Check hosting bill — verify no unexpected charges (serverless function overages, bandwidth spikes)
- Test all forms (contact, newsletter, checkout) — form backends can silently break
- Review content for accuracy (pricing, dates, team members, product info)

**Annually (2-4 hours):**
- Major version upgrades (Astro 4→5, Next.js 14→15, Node.js 20→22)
- Domain renewal (enable auto-renew, verify contact email is active)
- SSL certificate renewal verification (Let's Encrypt auto-renews, but verify it's working)
- Full content audit: archive outdated posts, update evergreen content, refresh screenshots
- Platform pricing review: has your hosting/CMS changed pricing? Are there cheaper alternatives?
