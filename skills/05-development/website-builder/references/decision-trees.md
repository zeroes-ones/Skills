## Decision Trees

<!-- QUICK: 30s — follow the ASCII tree to your scenario -->

### SSG Selection

```
                         ┌──────────────────────────────────┐
                         │ START: What type of site?         │
                         └────────────────┬─────────────────┘
                                          │
                    ┌─────────────────────▼─────────────────────┐
                    │ Is this a content site (blog, docs,       │
                    │ portfolio, marketing pages)?              │
                    └──┬──────────────────────────────────┬─────┘
                       │ YES                              │ NO
                       ▼                                  ▼
            ┌──────────────────┐              ┌──────────────────────────┐
            │ Does the site    │              │ Is this e-commerce?       │
            │ need a CMS for   │              └──┬───────────────────┬───┘
            │ non-devs?        │                 │ YES               │ NO
            └──┬───────────┬───┘                 ▼                   ▼
               │ YES       │ NO         ┌──────────────┐   ┌──────────────────┐
               ▼           ▼            │ Next.js +    │   │ Is this a SaaS    │
        ┌──────────┐ ┌──────────┐       │ Shopify/     │   │ web app with      │
        │ Astro +  │ │ Astro or │       │ Medusa or    │   │ auth, dashboard,  │
        │ Decap CMS│ │ 11ty +   │       │ Shopify      │   │ real-time data?   │
        │ or Tina  │ │ Markdown │       │ (Go to       │   └──┬───────────┬───┘
        │ CMS      │ │          │       │ E-commerce   │      │ YES       │ NO
        └──────────┘ └──────────┘       │ Tree)        │      ▼           ▼
                                        └──────────────┘ ┌──────────┐ ┌──────────┐
                                                         │ Next.js  │ │ Astro    │
                                                         │ or Remix │ │ or Hugo  │
                                                         │ (SSR/SSG)│ │ (static) │
                                                         └──────────┘ └──────────┘
```
**When Astro + Markdown:** Blog, portfolio, documentation. Content changes infrequently. Developer edits markdown, pushes to git, site rebuilds automatically. Zero CMS cost, zero maintenance.

**When Astro + CMS (Decap/Tina):** Marketing site where non-technical team updates content weekly. Git-based CMS (Decap) stores content in repo — no database. Tina CMS provides visual editing. Both free, open-source.

**When 11ty (Eleventy):** Performance-obsessed content sites. 11ty produces zero-client-JS output by default. Faster builds than Astro for large sites (1000+ pages). Excellent for blogs with complex taxonomies.

**When Hugo:** Fastest build times (1ms per page). Best for 5000+ page documentation sites. Go-based — single binary, no Node dependency. Limited plugin ecosystem compared to Astro/11ty.

### Hosting Selection

```
                         ┌──────────────────────────────────┐
                         │ START: Monthly hosting budget?    │
                         └────────────────┬─────────────────┘
                                          │
              ┌───────────────────────────▼───────────────────────────┐
              │ $0/month?                                             │
              └──┬────────────────────────────────────────────────┬───┘
                 │ YES                                            │ NO
                 ▼                                                ▼
      ┌──────────────────────┐                    ┌──────────────────────────┐
      │ Static site?          │                    │ $5-20/month?             │
      └──┬───────────────┬───┘                    └──┬───────────────────┬───┘
         │ YES           │ NO                       │ YES               │ NO
         ▼               ▼                          ▼                   ▼
  ┌──────────────┐ ┌──────────────┐        ┌──────────────┐   ┌──────────────────┐
  │ Cloudflare   │ │ Render       │        │ Need server-  │   │ $20-50/month?    │
  │ Pages or     │ │ Free Tier    │        │ side rendering│   └──┬───────────┬───┘
  │ GitHub Pages │ │ (Node/Python │        │ or functions? │      │ YES       │ NO
  │              │ │ backends)    │        └──┬────────┬───┘      ▼           ▼
  └──────────────┘ └──────────────┘           │ YES    │ NO  ┌──────────┐ ┌──────────┐
                                              ▼        ▼     │ Vercel   │ │ $50+/mo  │
                                       ┌──────────┐ ┌──────┐ │ Pro or   │ │ → AWS    │
                                       │ Vercel   │ │Netlify││ Netlify  │ │ Amplify  │
                                       │ Hobby or │ │Free/  ││ Pro      │ │ or self- │
                                       │ Netlify  │ │Starter││          │ │ hosted   │
                                       │ Starter  │ │       ││          │ │ VPS      │
                                       └──────────┘ └──────┘└──────────┘ └──────────┘
```
**When Cloudflare Pages:** Best free tier in the industry — unlimited bandwidth, unlimited requests, 1 build at a time, 500 builds/month. Global edge network (330+ cities). Automatic HTTP/3 and Brotli compression. The gold standard for $0 hosting.

**When GitHub Pages:** Simple, reliable, free. Deploy from any branch with GitHub Actions. No build plugins — pre-build your site and push the output directory. Bandwidth limit: 100GB/month (soft cap — GitHub rarely enforces for personal sites).

**When Vercel/Netlify:** Need serverless functions, form handling, split testing, or analytics. Vercel free tier: 100GB bandwidth, 1000 serverless function executions/day. Netlify free tier: 100GB bandwidth, 300 build minutes/month.

### CMS vs Custom Content Management

```
                         ┌──────────────────────────────────┐
                         │ START: Who updates the content?   │
                         └────────────────┬─────────────────┘
                                          │
              ┌───────────────────────────▼───────────────────────────┐
              │ Is the content editor a developer?                    │
              └──┬────────────────────────────────────────────────┬───┘
                 │ YES                                            │ NO
                 ▼                                                ▼
      ┌──────────────────────┐                    ┌──────────────────────────┐
      │ Content changes       │                    │ Marketing team or client? │
      │ < weekly?             │                    └──┬───────────────────┬───┘
      └──┬───────────────┬───┘                       │ YES               │ NO
         │ YES           │ NO                        ▼                   ▼
         ▼               ▼                    ┌──────────────┐   ┌──────────────────┐
  ┌──────────────┐ ┌──────────────┐           │ Need visual   │   │ Clients who      │
  │ Markdown +   │ │ Git-based    │           │ drag-and-drop │   │ demand full      │
  │ Git. No CMS  │ │ CMS (Decap)  │           │ editing?      │   │ design control?  │
  │ needed.      │ │ — stores in  │           └──┬────────┬───┘   └──┬───────────┬───┘
  │              │ │ repo, no DB  │              │ YES    │ NO       │ YES       │ NO
  └──────────────┘ └──────────────┘              ▼        ▼          ▼           ▼
                                           ┌──────────┐ ┌──────┐ ┌──────────┐ ┌──────┐
                                           │ Webflow  │ │Head- │ │ Webflow  │ │Word- │
                                           │ or Framer│ │less  │ │ or Framer│ │Press │
                                           │          │ │CMS   │ │          │ │+ page│
                                           │          │ │(Sanity│ │          │ │builder│
                                           │          │ │Strapi)│ │          │ │      │
                                           └──────────┘ └──────┘ └──────────┘ └──────┘
```
**When Git-based (Decap CMS/Tina CMS):** Sweet spot — non-developer editors who are comfortable with a web UI but don't need drag-and-drop. Content stored as markdown in git. PR-based workflow with previews. $0/month, fully portable.

**When Headless CMS (Sanity/Strapi):** Structured content with relationships (product catalogs, multi-author publications). API-first. Sanity free tier is generous (unlimited users on free plan). Strapi is self-hosted (free) or cloud ($29+/mo).

**When Webflow/Framer:** Design-driven teams that need pixel-perfect visual control. Non-technical editors who need drag-and-drop. Lock-in risk: content not easily exportable. Framer is more affordable ($5-30/mo as of 2026); Webflow scales higher ($14-39/mo as of 2026).

### E-commerce Platform

```
                         ┌──────────────────────────────────┐
                         │ START: How many products?         │
                         └────────────────┬─────────────────┘
                                          │
              ┌───────────────────────────▼───────────────────────────┐
              │ 1-10 products?                                        │
              └──┬────────────────────────────────────────────────┬───┘
                 │ YES                                            │ NO
                 ▼                                                ▼
      ┌──────────────────────┐                    ┌──────────────────────────┐
      │ Digital products     │                    │ 10-100 products?          │
      │ only? (ebooks,       │                    └──┬───────────────────┬───┘
      │ courses, software)   │                       │ YES               │ NO
      └──┬───────────────┬───┘                       ▼                   ▼
         │ YES           │ NO                 ┌──────────────┐   ┌──────────────────┐
         ▼               ▼                    │ Need full     │   │ 100+ products or  │
  ┌──────────────┐ ┌──────────────┐           │ e-commerce    │   │ enterprise?       │
  │ Gumroad or   │ │ Shopify      │           │ platform?     │   └──┬───────────┬───┘
  │ Lemon Squeezy│ │ Starter or   │           └──┬────────┬───┘      │ YES       │ NO
  │ (10% fee or  │ │ Next.js +    │              │ YES    │ NO       ▼           ▼
  │ flat $0.50)  │ │ Stripe       │              ▼        ▼     ┌──────────┐ ┌──────────┐
  └──────────────┘ └──────────────┘       ┌──────────┐ ┌──────┐│ Shopify  │ │ Big      │
                                          │ Shopify  │ │Medusa││ Plus or  │ │ Commerce │
                                          │ (standard│ │(open ││ Big      │ │ Enterprise│
                                          │ plan)    │ │source││ Commerce │ │          │
                                          │          │ │+ self││          │ │          │
                                          │          │ │host) ││          │ │          │
                                          └──────────┘ └──────┘└──────────┘ └──────────┘
```
**When Gumroad/Lemon Squeezy:** 1-3 digital products. No storefront to build — just a payment link. Gumroad takes 10% (free plan) or $10/mo + 3.5%. Lemon Squeezy: $0.50 flat fee per sale as of 2026. Best for creators, indie hackers, course sellers.

**When Shopify:** Standard e-commerce with inventory, shipping, tax calculation. $29-299/mo as of 2026. Huge app ecosystem. 0% transaction fee if using Shopify Payments. Best for non-technical store owners.

**When Medusa (open-source):** Developer-controlled e-commerce with custom checkout flows, multi-currency, multi-vendor. Self-hosted (free software), but you handle hosting ($20-50/mo). Best for developers who need full customization.

**When Next.js + Stripe:** Custom storefront with Stripe Checkout. No monthly platform fee — Stripe takes 2.9% + $0.30 per transaction. Best for developers building a unique shopping experience with full design control.
