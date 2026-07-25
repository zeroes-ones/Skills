## Cost Matrix — Full Transparency

<!-- SIGNATURE FEATURE: always present this table when recommending a stack -->

### Primary Stack Cost Comparison

| Stack | Hosting | CMS | Monthly Cost | Setup Time | Maintenance | Best For |
|-------|---------|-----|-------------|------------|-------------|----------|
| **Astro + Cloudflare Pages** | $0 (CF Pages) | Git-based (free) | **$0-5/mo** | 2-4 hours | Very low | Blog, portfolio, docs, landing pages, marketing sites |
| **Hugo + GitHub Pages** | $0 (GH Pages) | Git-based (free) | **$0/mo** | 1-3 hours | Very low | Static content, 1000+ page documentation, JAMstack blogs |
| **11ty + Netlify** | $0-19/mo (Netlify) | Decap CMS (free) | **$0-19/mo** | 3-6 hours | Low | JAMstack sites with non-dev editors, high-performance blogs |
| **Next.js + Vercel (static)** | $0-20/mo (Vercel) | Git-based (free) | **$0-20/mo** | 8-16 hours | Low-medium | Static marketing sites needing occasional SSR, hybrid sites |
| **Next.js + Vercel (dynamic)** | $20/mo (Vercel Pro as of 2026) | Sanity/Strapi ($0-99/mo) | **$20-99/mo** | 16-40 hours | Medium | SaaS apps, e-commerce with custom checkout, dynamic content |
| **Astro + Decap CMS + Netlify** | $0-19/mo (Netlify) | Decap CMS (free) | **$0-19/mo** | 4-8 hours | Low | Client-handoff sites where client needs visual editor |
| **Shopify** | Included ($29+ as of 2026) | Built-in | **$29-299/mo** | 4-8 hours | Very low | E-commerce — non-technical store owners, 10-100+ products |
| **Webflow** | Included ($14+ as of 2026) | Built-in | **$14-39/mo** | 8-20 hours | Low | Design-heavy marketing sites, agency client handoff |
| **Framer** | Included ($5+ as of 2026) | Built-in | **$5-30/mo** | 4-12 hours | Very low | Portfolio sites, landing pages, rapid prototyping |
| **WordPress + Kinsta** | $30/mo (Kinsta as of 2026) | Built-in | **$30-100/mo** | 8-24 hours | Medium | Client-handoff when client demands WordPress, existing WP migrations |
| **Full custom (Next.js + AWS)** | $20-200/mo (AWS) | Custom headless ($0-99/mo) | **$20-300/mo** | 40-160 hours | High | Enterprise SaaS, marketplaces, multi-tenant apps, high-traffic custom solutions |
| **Medusa (OSS) + Self-hosted** | $20-50/mo (VPS/ Railway) | Built-in headless (free) | **$20-50/mo** | 16-40 hours | Medium | Developer-controlled e-commerce, multi-vendor, complex product models |

⚠️ **All prices "as of 2026" — verify current rates before committing.** Platforms change pricing, discontinue plans, and get acquired. The cost structure above is directionally accurate but may have shifted. Check each platform's pricing page for current rates.

### Hidden Costs — The Real Monthly Bill

These costs apply to every stack, regardless of technology choice:

| Hidden Cost | Typical Range | Frequency | Notes |
|-------------|--------------|-----------|-------|
| **Domain name** | $10-15/yr → **~$1.25/mo** | Annual | Use Cloudflare Registrar (at-cost, no markup). Avoid GoDaddy (upsells, renewal hikes). Enable auto-renew. |
| **Email hosting** | $0-6/mo | Monthly | $0: Cloudflare Email Routing (forward-only). $1-3: Zoho Mail. $6: Google Workspace/ Microsoft 365 (per user). |
| **Stock photos** | $0-50/mo | Monthly | $0: Unsplash, Pexels, Pixabay (free, attribution-free). $15/mo: Envato Elements. $50/mo: custom photography. |
| **SSL certificate** | **$0** | Annual | Let's Encrypt is free, auto-renewed on all recommended platforms. Never pay for SSL. |
| **CDN** | **$0** | Monthly | Included on Cloudflare Pages, Vercel, Netlify, GitHub Pages. Self-hosted: Cloudflare Free plan (unlimited bandwidth). |
| **Analytics** | $0-9/mo | Monthly | $0: Plausible/Umami self-hosted. $9/mo: Plausible/Umami cloud. $0: Google Analytics 4 (requires cookie consent). |
| **Form handling** | $0-20/mo | Monthly | $0: Netlify Forms (100 submissions/mo free), Cloudflare Workers. $20/mo: Typeform, Jotform. Custom endpoint: minimal serverless cost. |
| **Uptime monitoring** | $0-24/mo | Monthly | $0: Upptime (GitHub Actions, self-hosted). $24/mo: Better Uptime (as of 2026). |
| **Error tracking** | $0-26/mo | Monthly | $0: Sentry free tier (5K errors/mo). $26/mo: Sentry Team. |

**Realistic total monthly cost for a static marketing site:** Domain ($1.25) + Email ($0-6) + Analytics ($0) + Monitoring ($0) = **$1.25-7.25/mo**. Everything else is included in the $0 hosting plan.

**Realistic total monthly cost for a SaaS/e-commerce site:** Domain ($1.25) + Email ($6) + Analytics ($9) + Monitoring ($24) + Error tracking ($26) + Hosting ($20-99) + CMS ($0-99) = **$60-255/mo** (excluding platform transaction fees).

### Transaction Fee Quick Reference (e-commerce)

| Platform | Transaction Fee | Monthly Fee | Best For |
|----------|----------------|-------------|----------|
| Stripe | 2.9% + $0.30 | $0 | Custom storefronts, SaaS billing |
| Shopify Payments | 2.9% + $0.30 | $29+/mo | Shopify stores using native payment |
| Shopify (third-party gateway) | 2.0% additional | $29+/mo | Penalty for not using Shopify Payments |
| Gumroad (free plan) | 10% flat | $0 | Digital products, < $100/mo revenue |
| Gumroad (paid) | 3.5% + $0.30 | $10/mo | Digital products, > $100/mo revenue |
| Lemon Squeezy | $0.50 flat | $0 | Digital products, low transaction values |
| PayPal | 3.49% + $0.49 | $0 | International transactions, buyer trust |
