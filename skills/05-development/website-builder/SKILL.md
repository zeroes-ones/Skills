---
name: website-builder
description: >-
  Use when building or migrating websites — static, e-commerce, SaaS landing pages, portfolios,
  or web apps. Handles SSG selection (Astro/Next.js/Hugo/11ty), low-code evaluation, $0-5/mo
  cost-optimized deployment, Core Web Vitals, SEO-first architecture, and maintenance planning.
  Do NOT use for backend API development, native mobile apps, or enterprise microservices —
  route to backend-developer, mobile-developer, or system-architect.
category: 05-development
tier: 2
author: Sandeep Kumar Penchala
license: MIT
type: development
status: stable
version: 1.0.0
updated: 2026-07-24
tags:
  - web
  - static-site
  - seo
  - performance
  - e-commerce
  - landing-page
  - portfolio
  - saas
  - jamstack
  - core-web-vitals
token_budget: 5000
chain:
  feeds_into:
    - seo-specialist
    - frontend-developer
    - fullstack-developer
    - performance-engineer
    - ui-ux-designer
    - qa-engineer
    - content-strategist
    - accessibility-testing
    - ci-cd-builder
    - devops-engineer
  consumes_from:
    - product-strategist
    - ui-ux-designer
    - content-strategist
    - api-designer
    - backend-developer
    - brand-guidelines
    - domain-modeling
    - ux-researcher
    - security-reviewer
---

# Website Builder
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

End-to-end website building from concept to production — covering static site generators, low-code platforms, full custom builds, and everything in between. This skill provides a decision framework for choosing the right stack based on requirements, budget, technical capability, and long-term maintenance capacity. Every recommendation includes cost transparency, performance budgets, SEO foundations, and accessibility baselines.

## Route the Request

<!-- QUICK: 30s — auto-route first, then intent-route -->

### Auto-Route (No User Input Required)

Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_exists("astro.config.*" \|\| "hugo.toml" \|\| ".eleventy.js" \|\| "eleventy.config.*")` | SSG project detected. Jump to **Decision Trees** — SSG Selection, then **Core Workflow > Phase 6 (Performance)**. |
| A2 | `file_contains("package.json", "\"next\"" \|\| "\"remix\"" \|\| "\"sveltekit\"")` | Full-stack framework detected. Jump to **Core Workflow > Phase 1 (Stack Selection)** to validate the choice against requirements. |
| A3 | `file_contains("*", "shopify" \|\| "woocommerce" \|\| "medusa" \|\| "stripe.*checkout")` | E-commerce detected. Jump to **Decision Trees** — E-commerce Platform, then **Cost Matrix** for pricing validation. |
| A4 | `file_exists("webflow" \|\| "framer" \|\| "bubble")` | Low-code site detected. Jump to **Ground Rules** — Rule about platform ignorance, then **Cost Matrix**. |
| A5 | `file_contains("*", "lighthouse" \|\| "core.*web.*vitals" \|\| "LCP" \|\| "CLS" \|\| "FID" \|\| "INP")` AND `file_contains("*", "fail\|poor\|needs.*improvement")` | Performance problem detected. Jump to **Error Recovery** — Core Web Vitals. |
| A6 | `file_contains("*", "sitemap" \|\| "robots.txt" \|\| "structured.*data" \|\| "json-ld")` AND `file_contains("*", "missing\|not.*found\|broken")` | SEO issue detected. Jump to **Core Workflow > Phase 5 (SEO Foundation)**. |
| A7 | No framework or platform detected (`!file_exists("package.json\|composer.json\|Gemfile\|requirements.txt")` AND no SSG configs) | Greenfield project. Jump to **Intent Route** below. |

### Intent Route (Ask the User)

If no auto-route matched, use this intent tree:

```
What are you trying to build?
├── Static marketing site / landing page → Start at "Decision Trees" — SSG Selection, then Core Workflow Phase 0
├── E-commerce store → Jump to "Decision Trees" — E-commerce Platform, then Cost Matrix
├── SaaS web application → Go to "Decision Trees" — Stack Selection, then Core Workflow Phase 1
├── Blog or content site → Start at "Decision Trees" — SSG Selection (Astro/11ty path)
├── Portfolio / personal site → Jump to "Cost Matrix" — pick Astro + Cloudflare or Framer row
├── Non-developer needs to build → Direct to "Decision Trees" — Low-Code Platform, then Core Workflow Phase 2
├── Existing site needs SEO overhaul → Invoke seo-specialist skill instead
├── Existing site needs performance optimization → Invoke performance-engineer skill instead
├── Existing site needs accessibility remediation → Invoke accessibility-auditor skill instead
├── Need UI/UX design first → Invoke ui-ux-designer skill instead
├── Need backend API for the site → Invoke backend-developer skill instead
├── Need content strategy for the site → Invoke content-strategist skill instead
└── Don't know where to start? → Answer discovery questions below and I'll route you

Discovery Questions (when user has no idea what to build):
1. "What's the primary goal? (sell products / generate leads / share content / showcase work / build a tool)"
2. "Who will update the content? (you — comfortable with code? / marketing team — need a dashboard? / clients — need drag-and-drop?)"
3. "What's your monthly hosting budget? ($0 / $5 / $20 / $50 / $200+)"
4. "How urgent is launch? (this week / this month / this quarter)"
5. "Any must-have third-party integrations? (Stripe, HubSpot, Salesforce, email provider, analytics)"
```

## Ground Rules — Read Before Anything Else

These rules are non-negotiable constraints that detect website building mistakes before they happen. Violation means STOP and refuse to proceed.

| # | Negative Constraint | Mechanical Trigger | Violation Example | Violation Response |
|---|-------------------|-------------------|-------------------|-------------------|
| R1 | **Never assume hosting budget** — always present $0, $5, $20, $50/mo tiers | Trigger: recommending a single hosting option without cost alternatives, or recommending Vercel Pro ($20/mo) when Cloudflare Pages ($0) also meets requirements | "Let's deploy on Vercel Pro." — without mentioning the free tier alternatives that handle the same static site | STOP. Respond: "Hosting recommendation at [recommendation]. Present at least 3 budget tiers: $0 (Cloudflare Pages/GitHub Pages), $5-20 (Netlify/Vercel Hobby), $20-50 (Vercel Pro/Netlify Pro). The user's budget may differ from your assumption. Always show the cost ladder." |
| R2 | **Mobile-first by default** — every site must pass Core Web Vitals on mobile | Trigger: recommending a design or stack that produces LCP > 2.5s on 4G mobile, or using desktop-only viewport testing | "The hero section uses a 5MB background video." — works on desktop WiFi, fails catastrophically on mobile 4G (LCP > 8s) | STOP. Respond: "Mobile performance degradation at [component]. Serve a poster image with `<video>` lazy-loading instead. Every page must pass LCP < 2.5s, INP < 200ms, CLS < 0.1 on a Moto G4 with 4G throttling. Desktop-only testing is not acceptable." |
| R3 | **SEO from line one** — semantic HTML, meta tags, structured data, sitemap must be in scaffolding | Trigger: scaffolded project has no `<title>`, `<meta name="description">`, Open Graph tags, or sitemap generation configured | "We'll add SEO after the site is built." — site deploys without a single meta tag; Google indexes blank titles for 3 months until someone notices | STOP. Respond: "Missing SEO foundation at [project]. Every scaffold must include: `<title>` + `<meta description>` in layout, Open Graph + Twitter Card tags, structured data (Article/Product/Organization JSON-LD), auto-generated sitemap.xml, and robots.txt. SEO retrofits cost 3-6 months of lost organic traffic." |
| R4 | **Never hardcode pricing info** — warn that pricing changes; always add "as of [current year]" | Trigger: writing fixed dollar amounts for any third-party service without a temporal qualifier | "Netlify Pro is $19/mo." — Netlify changes pricing, the statement is wrong next year, user acts on stale data | STOP. Respond: "Pricing cited without temporal qualifier. Append 'as of 2026' to every dollar figure for third-party services. Add: '⚠️ Pricing changes over time — verify current rates before committing.' Platforms change pricing, discontinue tiers, and get acquired. Stale pricing is worse than no pricing." |
| R5 | **Security baseline** — HTTPS enforced, server-side form validation, no API keys in client code, CSP headers | Trigger: any HTTP URL, `onSubmit` with only client-side validation, API key in `.js`/`.tsx` file not in `.env`, missing `Content-Security-Policy` header | Form validation is `required` attribute only — bypassed with `curl -X POST` containing malicious payload | STOP. Respond: "Security gap at [location]. (a) All production URLs must enforce HTTPS with redirect. (b) Form validation must run server-side — client validation is UX, not security. (c) API keys go in environment variables only — never in client code. (d) Set CSP header: `default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'`. A single missed CSP header is an XSS vector." |
| R6 | **Accessibility minimum AA** — WCAG 2.2 AA compliance, keyboard navigation, screen reader testing | Trigger: interactive element without `aria-label` or visible text, color-only information distinction, `tabindex` > 0, missing `alt` on content images | "The error state shows a red border with no text explanation." — color-blind users (8% of males) cannot perceive the error | STOP. Respond: "WCAG 2.2 failure at [element]. Accessibility checklist: (a) All interactive elements have accessible names. (b) Color contrast ≥ 4.5:1 for normal text, 3:1 for large text. (c) Every screen is navigable by keyboard (Tab/Shift+Tab, Enter to activate, Esc to close). (d) Error states use text + icon, not color alone. Test with axe DevTools and voiceover/TalkBack." |
| R7 | **Performance budget** — LCP < 2.5s, INP < 200ms, CLS < 0.1, pages < 200KB uncompressed | Trigger: recommending a dependency or asset that pushes any page over 200KB uncompressed, or recommending render-blocking resources without deferral | "Let's add a 150KB jQuery + 200KB Bootstrap CSS + 300KB carousel library." — page is 650KB before a single line of content loads | STOP. Respond: "Performance budget exceeded at [asset]. Every page must ship < 200KB uncompressed. Current page: [X]KB. Remove unnecessary libraries — modern JS (`querySelector`, `fetch`, `classList`) replaces jQuery. Use utility CSS (Tailwind) instead of component libraries. Defer non-critical JS with `type="module"` or `async`. Audit with Lighthouse CI in CI/CD." |
| R8 | **Admit platform ignorance** — if a platform (Webflow/Framer/Bubble/Shopify) has changed its pricing or features since training cutoff, say so | Trigger: making definitive claims about third-party platform pricing, features, or availability without qualification | "Framer costs $5/mo for a basic site." — Framer changed pricing tiers after training cutoff, statement is wrong | STOP. Respond: "⚠️ Platform pricing verification required. My knowledge of [platform] pricing may be outdated (training cutoff: early 2025). Current claims: [claims]. Action: Verify at [platform's pricing page URL] before committing. Platform features and pricing change frequently — always check the source." |
| R9 | **Always provide cost comparison table** — for any recommended stack, show monthly cost breakdown | Trigger: recommending a stack without itemizing costs (hosting, CMS, domain, email, CDN, analytics, stock assets) | "Use Next.js with Vercel and Sanity." — user signs up, discovers $20/mo Vercel + $15/mo Sanity + $12/yr domain + $6/mo email = surprise $41/mo | STOP. Respond: "Incomplete cost disclosure at [recommendation]. Provide a line-item cost breakdown: Hosting ($X/mo), CMS ($X/mo), Domain ($10-15/yr → ~$1/mo), Email ($0-6/mo), Analytics ($0-9/mo), CDN ($0 on most platforms), Stock assets ($0-50/mo). Total: $X/mo. Surprise costs erode trust. State the full number upfront." |
| R10 | **Never recommend deprecated hosts or platforms** — flag if a recommended platform has been acquired, shut down, or entered maintenance mode | Trigger: recommending Heroku free tier (discontinued 2022), Gatsby (largely abandoned since Netlify acquisition, development stalled), or any platform known defunct | "Use Gatsby Cloud for hosting." — Gatsby Cloud was discontinued in 2023; Gatsby itself has minimal maintenance activity since 2023 | STOP. Respond: "⚠️ Platform status concern at [recommendation]. [Platform] may be deprecated, acquired, or in maintenance mode. Verify: check the platform's GitHub repo for recent commits, their blog for acquisition news, and community forums for migration discussions. Prefer actively maintained alternatives: Gatsby → Astro/Next.js, Heroku free → Render/Fly.io, Surge → Cloudflare Pages." |


- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset

### The Mental Model Shift

Competent web developers build sites that look good on their MacBook Pro with gigabit WiFi. Masters build sites that **load in under 2.5 seconds on a $150 Android phone with 3G connectivity, render correctly at 320px width, score 100 on Lighthouse, and cost $0/month to host indefinitely.** The shift: your Retina display is not representative. The median web user browses on a mid-range mobile device with variable connectivity. Design for constraints first — enhance for abundance.

### Cognitive Biases That Kill Websites

| Bias | How It Manifests | Antidote |
|-------|------------------|----------|
| **Stack familiarity bias** | Choosing Next.js for a 3-page brochure site because "I know React" — adding 80KB of JS for zero dynamic functionality | Match the stack to the requirements, not your resume. A 3-page site needs 0KB of JS. Astro ships 0KB by default. |
| **Shiny object syndrome** | Adopting the newest framework (SolidStart, Qwik, Analog) for a production client site — zero ecosystem, no Stack Overflow answers | Bet on boring technology for production. If a framework is < 2 years old and < 10K GitHub stars, it's for side projects, not client sites. |
| **Over-engineering the CMS** | Building a custom headless CMS + GraphQL API for a blog that one person updates quarterly — 80 hours of engineering for a markdown folder | Content update frequency drives CMS complexity. Quarterly updates = markdown. Daily updates by 5+ people = headless CMS. Match investment to usage. |
| **Desktop-first design** | Designing at 1440px and "adapting" to mobile — mobile feels like a cramped afterthought | Design at 320px first. If it works on a tiny screen, it works everywhere. Mobile-first CSS (min-width breakpoints) enforces this mechanically. |

### What Website Masters Know That Others Don't

- **The cheapest hosting is no hosting.** A static site deployed to Cloudflare Pages or GitHub Pages costs $0/month forever. No servers to patch, no databases to backup, no runtime to monitor. If your site doesn't need server-side logic, don't pay for server-side infrastructure.
- **JavaScript is a progressive enhancement, not a requirement.** Your site must be functional and readable with JavaScript disabled. Semantic HTML handles navigation, forms, and content. JavaScript adds interactivity (animations, filtering, dynamic loading) but must never be the sole mechanism for core functionality.
- **SEO is a compounding investment.** A site with perfect SEO shipped today starts earning organic traffic in 3-6 months. A site with "SEO later" loses 6+ months of compounding traffic growth. Every month you delay SEO is a month of traffic you'll never get back.
- **Platform risk is real and often invisible.** Webflow, Shopify, Squarespace — they can change pricing, remove features, or get acquired. Your content and code should be extractable. Static site generators produce plain HTML/Markdown — portable to any host. Proprietary platforms produce locked-in data. The portability difference is existential.
- **The performance-poverty line divides the web.** Sites that load in < 2s on a budget device have global reach. Sites that require a flagship phone and fiber connection only serve the top 20% of users by income. Every 100KB of JS you ship excludes more of the world.

### When to Break Your Own Rules

- **Use a heavy framework when the dynamic features justify it.** If your marketing site has a real-time dashboard, user auth, and database-driven content, Next.js or Remix is appropriate. Don't use Astro just because "static is always better."
- **Use a low-code platform when the alternative is no website at all.** A non-technical founder with no budget for developers should use Webflow or Framer rather than waiting months to hire. A launched site > no site.

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Building a new website from scratch — static site, landing page, portfolio, blog, e-commerce storefront, or SaaS marketing site
- Migrating an existing website from a proprietary platform (Wix, Squarespace, WordPress) to a modern, portable stack
- Choosing between static site generators (Astro, Hugo, 11ty, Next.js, Remix) based on build speed, JS footprint, and content update frequency
- Evaluating low-code platforms (Webflow, Framer, Bubble) for non-developer content editors or rapid prototyping
- Optimizing Core Web Vitals and implementing SEO-first architecture for existing or new sites
- Setting up cost-optimized hosting and deployment pipelines ($0-50/mo range)
- Designing content architecture, CMS integration, and editorial workflows for teams
- Don't use for backend API development or full-stack web apps with complex server-side logic — invoke backend-developer or fullstack-developer

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

## Gotchas — Dollar-Quantified Website Footguns

- **"I'll just use WordPress" → $3,200/mo in security cleanup.** WordPress powers 43% of the web — and 90% of hacked CMS sites are WordPress. Plugin zero-days (e.g., the 2024 LiteSpeed Cache vulnerability affecting 5M+ sites) mean automated scanners find and exploit unpatched WP sites within 48 hours. A hacked site requires: malware removal ($500-2,000 one-time), SEO penalty recovery (backlink cleanup, Google reconsideration request — $1,000-3,000), and incident response ($500-1,500). Monthly cost of a WAF + malware scanning service: $50-300. **Fix: If you must use WordPress, use managed hosting (Kinsta, WP Engine, $30+/mo) with auto-updates and a WAF. Better: use a static site — no database to hack, no plugins to exploit, no PHP runtime to patch.**

- **Forgetting image optimization → $800/mo in bandwidth overages.** A single 5MB hero image served to 1M monthly visitors = 5TB of unnecessary transfer. Cloudflare Pages gives you unlimited bandwidth, but Vercel Pro caps at 1TB ($55/100GB overage), Netlify Pro at 400GB ($55/100GB overage), AWS S3 at $0.09/GB (5TB = $450). At 1M pageviews with 3 unoptimized images (total 15MB per pageview), bandwidth overages can hit $2,400 on Vercel, $2,200 on Netlify, or $1,350 on AWS — monthly. **Fix: Use responsive images (srcset + WebP/AVIF). Serve at display size (never larger than 2x viewport width). Automate with framework image components (@astrojs/image, next/image, Hugo image processing). A hero image should be < 100KB, not 5MB.**

- **"Vercel free tier is enough" → $500 surprise bill.** Vercel's free tier includes 100GB bandwidth and 1000 serverless function executions per day. A bot crawling 100K pages in 24 hours with SSR triggers 100K function invocations — 100x the daily limit. Overage is $0.60 per 1M function executions. At 100K/day for a month: 3M extra executions = $1.80 — seems small. But bandwidth is the real killer: 100K pages at 500KB each = 50GB/day = 1.5TB/month. Vercel overage: $55/100GB × 14 extra blocks = $770. **Fix: Set Vercel Spend Management limits on day one. Add rate limiting (Vercel WAF or Cloudflare in front). For content-heavy sites, use ISR/SSG instead of SSR — serve cached pages instead of rendering per-request.**

- **No CSP headers → $15,000+ in XSS-caused data breach recovery.** Content Security Policy headers block inline scripts (`script-src 'self'`) and restrict where scripts can load from. Without CSP, any unescaped user input (comment, search query, form field) is a potential XSS vector. An XSS attack that steals user sessions or payment data triggers: forensic investigation ($2,000-5,000), customer notification ($1,000-3,000 in legal + email costs), regulatory fines (GDPR: up to 4% of annual revenue; CCPA: $2,500 per violation), and reputation damage ($5,000-10,000 in lost business). **Fix: Set `Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'`. Test with CSP Evaluator (Google). Never use `'unsafe-inline'` for script-src. Use nonces or hashes for legitimate inline scripts.**

- **Hardcoding API keys in client JS → $50,000+ in API abuse.** Searching `site:github.com STRIPE_SECRET_KEY` finds thousands of exposed keys — and that's just Stripe. An exposed Stripe secret key lets attackers: issue refunds, create charges (fraud), access customer data. An exposed AWS key lets attackers: spin up crypto mining instances ($20,000+ in a weekend), exfiltrate data from S3 buckets, delete infrastructure. API providers may hold you liable for abuse charges. **Fix: Secrets go in environment variables ONLY. Client-side code never touches API secrets. Use serverless functions or API routes as a proxy. Rotate all keys exposed in git history (git-filter-repo to purge, then regenerate). Enable API key restrictions (IP allowlists, usage limits) on every provider.**

- **"I don't need HTTPS for my blog" → 30% organic traffic loss.** Google uses HTTPS as a ranking signal since 2014. Chrome and Safari show "Not Secure" warnings for HTTP sites with form fields — and increasingly for all HTTP pages. A site losing 30% of its organic traffic due to an avoidable security warning is losing that traffic permanently — every month. For a site earning $5,000/mo from organic traffic, that's $1,500/mo in lost revenue. Over 12 months: $18,000. **Fix: Let's Encrypt is free, automated, and supported by every recommended host. Enable "Always use HTTPS" (Cloudflare), "Force HTTPS" (Netlify), or equivalent. Add HSTS header: `Strict-Transport-Security: max-age=31536000; includeSubDomains`.**

- **Skipping sitemap.xml → 60% of pages never indexed.** Search engines discover pages via sitemaps for deep content and via internal links for shallow content. Without a sitemap, orphan pages (pages with no internal links pointing to them) are invisible to search engines. A blog with 100 posts where only 10 are linked from the homepage: 90 posts may never appear in search results. At an average of 500 organic visits/post/month, that's 45,000 lost visits/month. At a 2% conversion rate, that's 900 lost conversions/month. **Fix: Generate sitemap.xml on every build (framework plugins handle this automatically). Update `<lastmod>` dates when content changes. Submit to Google Search Console and Bing Webmaster Tools. Verify all pages return 200 (not 404, not redirects, not blocked by robots.txt).**

- **Using jQuery in 2025 → 87KB wasted download for no benefit.** jQuery (87KB gzipped) provides abstractions for APIs that modern browsers implement natively: `document.querySelector()` replaces `$()`, `fetch()` replaces `$.ajax()`, `element.classList` replaces `addClass()`/`removeClass()`, `element.dataset` replaces `$.data()`. The entire jQuery API surface has native browser equivalents in ES2020+. At 1M monthly pageviews, that's 87GB of unnecessary transfer = $7.83 on AWS S3, $4.35 on CloudFront — every month. More importantly: 87KB at 4G speeds (~10 Mbps) adds 70ms of download time. **Fix: Use vanilla JavaScript. If you must have a DOM library, Alpine.js (15KB) or Petite-Vue (5.8KB) provide reactivity without jQuery's bulk.**

- **No staging environment → $2,500 in revenue lost during a 4-hour outage.** Deploying directly to production without a staging/preview environment means every deploy is a gamble. A bad deploy (broken build, DB migration failure, API incompatibility) takes production offline. At $625/hr in revenue (typical for a small SaaS at ~$15K MRR), a 4-hour outage costs $2,500 in direct revenue plus $1,000-5,000 in emergency engineering time. **Fix: Deploy to staging first (Netlify Branch Deploys, Vercel Preview Deployments, Cloudflare Pages preview branches). Run smoke tests: homepage loads, login works, checkout completes, API responds. Promote to production only after verification. Keep previous production deploy as an instant rollback target.**

- **Not setting cache headers → 3x hosting cost from unnecessary requests.** Without `Cache-Control` headers, every page visit triggers a full server render (or at minimum, re-downloads static assets). A CDN without cache headers passes every request to origin — defeating the purpose of the CDN. For a site on Vercel Pro with 500K monthly pageviews, proper caching cuts origin requests from 500K to 50K (90% reduction). At 1M serverless function executions/month included: the difference between staying within limits vs. paying overages. **Fix: Set `Cache-Control: public, max-age=31536000, immutable` for hashed assets (`/assets/main.a1b2c3d4.js`). Set `Cache-Control: public, max-age=0, must-revalidate` or `stale-while-revalidate` for HTML. Use CDN-specific headers: `CDN-Cache-Control` (Cloudflare), `Surrogate-Control` (Fastly).**

- **"We'll add a cookie consent banner later" → $10,000+ GDPR fine.** GDPR (EU) and ePrivacy Directive require explicit consent before setting non-essential cookies — including Google Analytics, Facebook Pixel, Hotjar, and any advertising trackers. A site serving EU visitors with Google Analytics and no consent banner is in violation from day one. GDPR fines: up to €20 million or 4% of global annual revenue (whichever is higher). CCPA fines: $2,500 per unintentional violation, $7,500 per intentional. **Fix: If using privacy-first analytics (Plausible/Umami), no consent banner is needed — they don't use cookies. If using Google Analytics, add a consent management platform (CookieYes free, Osano, OneTrust). Block all tracking scripts until consent is given.**

- **Ignoring mobile Core Web Vitals → 20% lower conversion rate.** Google's page experience update means sites failing Core Web Vitals on mobile rank lower. A site ranking #3 (good CWV) vs #5 (poor CWV) sees a 20% difference in click-through rate (position #3: ~10% CTR; position #5: ~6% CTR). For 100K monthly searches at those positions: 10,000 visits vs 6,000 visits. At 2% conversion and $50 avg order value: $10,000/mo vs $6,000/mo — $4,000/mo difference from Core Web Vitals alone. **Fix: Test every page on mobile with PageSpeed Insights. Optimize LCP element (usually hero image). Minify and defer non-critical JS. Use a CDN. The fixes are mechanical — the revenue impact is compounding.**

## Anti-Rationalization Table — No Excuses

| The Temptation | Why It Feels Right | The Devastating Reality | Prevention |
|---------------|-------------------|------------------------|------------|
| **"WordPress is fine, everyone uses it"** | Most popular CMS (43% of web), massive plugin ecosystem, every developer knows it | Also the most hacked — 90% of CMS breaches target WordPress. The plugin ecosystem IS the attack surface. A single abandoned plugin with 10K installs is an exploit vector for 10K sites. The average hacked WP site has 20+ plugins — each one a potential entry point | Use static site generators for content sites — no database, no PHP runtime, no plugins. If WP is unavoidable, use managed hosting (Kinsta/WP Engine) with auto-updates, WAF, and zero-plugin policy. Maximum 5 well-maintained plugins |
| **"I'll add SEO later"** | Focus on building the product first. SEO is just meta tags — can add in an afternoon | SEO is a 3-6 month compounding investment. "Later" = 6 months of zero organic traffic while competitors build domain authority. Retroactive SEO requires: content audit, URL restructuring (breaking backlinks), meta tag backfill, and re-indexing. Each month delayed is 30 days of traffic you'll never recover — search rankings are temporal | Semantic HTML + `<title>` + `<meta description>` from template scaffolding. Structured data (JSON-LD) on first deploy. Sitemap generation in CI/CD. These are 30-minute additions to any scaffold — there is no "later" cost savings |
| **"Mobile optimization can wait until after launch"** | Desktop testing is faster. Mobile is "just smaller." Chrome DevTools responsive mode is good enough | 60%+ of global web traffic is mobile. Google exclusively uses mobile-first indexing as of 2023. A desktop-only site is literally invisible to Google. Beyond indexing: mobile users abandon sites that take >3 seconds to load at a 53% rate. A non-responsive site is non-functional for the majority of users | Design at 320px first (Tailwind mobile-first breakpoints enforce this). Test on a real $150 Android phone — DevTools emulation misses touch targets, font rendering, and real network latency. Every page must pass Core Web Vitals on mobile with 4G throttling |
| **"One more plugin instead of custom code"** | Faster implementation. "Why write 200 lines of CSS when there's a plugin?" The ecosystem exists so I don't have to code | WordPress sites average 20+ plugins. Each plugin is: a security surface, a performance cost (its own CSS/JS bundle), a compatibility risk (conflicts with other plugins/themes/WP versions), and an abandonment risk (maintainer stops updating → security vulnerability). A 100-line custom CSS solution is safer than a 10,000-line plugin with 3 dependencies | Write custom code for specific features. Use libraries (Alpine.js, Swiper.js) not monolithic plugins. Every dependency added to a project must justify itself: "What problem does this solve that 20 lines of vanilla code wouldn't?" |
| **"The free tier will be enough for now"** | Zero upfront cost. Quick to launch. "We'll upgrade when we hit the limits" | Free tiers have hidden cliffs: Vercel free limits commercial use to non-commercial/hobby projects (per ToS); Netlify free caps at 100GB bandwidth; Cloudflare Pages limits 1 concurrent build. The moment you exceed a limit — midnight bandwidth spike from a viral post, bot crawl triggering function overages — you face a choice: emergency upgrade (downtime during migration) or service degradation (your site is down/slow). "We'll upgrade when we need to" = "We'll deal with an outage first" | Budget $5-20/mo from day one. This covers: a domain ($1/mo), a hobby-tier hosting plan, and an analytics tool. Free tiers are for prototyping — a site that generates revenue or represents your brand deserves a paid plan |
| **"I don't need analytics — I'll just check occasionally"** | One less tool to set up. "Traffic doesn't matter yet" — we're pre-launch. Analytics can wait until there's something to measure | You cannot improve what you don't measure. Without analytics: you don't know which content performs, which pages have 90% bounce rates, which referrers send traffic, or whether your SEO is working. Six months post-launch, you have zero data to inform decisions. Marketing spend is blind. Content strategy is guesswork. | Install Plausible or Umami (privacy-first, 5-minute setup, $0-9/mo). It's 1 script tag. There is no legitimate reason to skip this — the cost is near-zero and the data compounds in value every month |
| **"I'll build my own e-commerce — Stripe is enough"** | Full control. No monthly platform fees. "Stripe Checkout handles payments — what else do I need?" | E-commerce is not just payments. You need: inventory management, tax calculation (VAT, GST, state-by-state US sales tax — Stripe Tax costs extra), shipping label generation, abandoned cart recovery, customer accounts/order history, and fraud detection. Building these from scratch takes 200-400 hours. Maintaining them as tax laws change is ongoing. Shopify/Medusa have solved these problems with teams of engineers | For 1-10 products, Gumroad/Lemon Squeezy. For 10-100 products, Shopify. For developer-controlled e-commerce with custom flows, Medusa (open-source). Only build from scratch if your e-commerce requirements are genuinely novel — and you have the team to maintain tax/shipping/fraud logic indefinitely |
| **"I can set up my own server — $5 VPS is cheaper than any platform"** | Lowest raw cost. Full control. "A $5/mo DigitalOcean droplet can handle 100K visits" — technically true for static files | A VPS requires: OS patching (monthly), web server config (nginx/Apache), SSL renewal automation, DDoS protection, monitoring, backups, and security hardening. These are "free" if your time has zero value. At a developer rate of $100/hr and 2 hours/month of maintenance, that $5 VPS costs $205/month. A managed platform at $20/mo is cheaper the moment you value your time above $10/hr | Use managed platforms for all but the most specialized use cases. Cloudflare Pages ($0), Vercel ($20), Netlify ($19) handle patching, SSL, CDN, DDoS, and monitoring. Spend your time building the site, not administering a server. VPS is for custom backend services that cannot run on serverless — not for hosting a marketing site |

## Error Recovery — Explicit Step-by-Step

### Build Fails with "Out of Memory"

**Symptoms:** Build process crashes with `JavaScript heap out of memory`, `FATAL ERROR: Ineffective mark-compacts`, or the build hangs indefinitely.

**Step-by-step recovery:**
1. **Increase Node memory limit:** `NODE_OPTIONS="--max-old-space-size=4096" npm run build` (default is 512MB-2GB depending on Node version).
2. **Check for circular imports:** Circular dependencies cause bundlers to loop. Run `npx madge --circular src/` to detect circular imports. Break circles with dependency injection, event emitters, or lazy imports.
3. **Reduce parallel builds:** Astro/Next.js/Vite parallelize page builds. If each page loads a heavy library (e.g., a markdown parser that loads 20MB of grammars), 16 parallel builds = 320MB memory spike. Limit concurrency: Astro (`--concurrency 4`), Next.js (set `experimental.cpus: 4` in config), Hugo (single-threaded by default).
4. **Profile the build:** `node --inspect-brk node_modules/.bin/astro build` → open Chrome DevTools → Memory tab → take heap snapshot. Identify the largest memory consumers.
5. **Split the build:** For large sites (10K+ pages), split into multiple builds by section (blog vs docs vs marketing) and combine output directories.

### Deploy Succeeds but Site Shows Blank Page

**Symptoms:** Deployment completes successfully, but the site at the production URL shows a completely white/blank page.

**Step-by-step recovery:**
1. **Check browser console (F12 → Console):** JS errors are the most common cause. Look for `Uncaught TypeError`, `Cannot read properties of undefined`, `Failed to load module`. If you see `404` for a JS/CSS file, the asset path is wrong.
2. **Check the page source (View Source, not DevTools Elements):** If the HTML is empty (`<body></body>`), the build didn't generate content. Check the build output directory — is `index.html` populated?
3. **Verify asset paths are relative, not absolute:** Absolute paths (`/assets/main.js`) resolve from the root domain. If your site is deployed to `https://user.github.io/repo/`, `/assets/main.js` resolves to `https://user.github.io/assets/main.js` (wrong). Use relative paths (`./assets/main.js`) or a `<base href="/repo/">` tag.
4. **Check for CORS errors on CDN assets:** If CSS/JS is served from a different domain (e.g., `cdn.example.com`), check the response headers for `Access-Control-Allow-Origin`.
5. **Disable service worker:** If you ship a service worker, clear it (DevTools → Application → Service Workers → Unregister) and hard reload. A broken service worker caching an empty response delivers a white page forever.

### Core Web Vitals Fail LCP Threshold

**Symptoms:** Lighthouse/PageSpeed Insights reports LCP > 4s (red). The largest content element takes too long to render.

**Step-by-step recovery:**
1. **Identify the LCP element:** Lighthouse report → "Largest Contentful Paint element" (typically hero image, hero heading, or hero background video). This is the bottleneck.
2. **If LCP is an image:** Preload it — `<link rel="preload" as="image" href="/hero.webp" fetchpriority="high">`. Convert to WebP/AVIF. Serve at display size (1x or 2x viewport — never full resolution). Use responsive `srcset` to avoid serving a 2000px image to a 375px phone.
3. **If LCP is text (heading):** Ensure the font is self-hosted and preloaded: `<link rel="preload" as="font" href="/fonts/inter.woff2" crossorigin>`. Set `font-display: swap` to show fallback text immediately. Subset fonts to only used characters (Latin subset typically 20-30KB vs 200KB full font).
4. **Inline critical CSS:** Above-the-fold styles go in a `<style>` tag in `<head>`. Eliminates the render-blocking CSS round-trip.
5. **Defer non-critical JS:** All `<script>` tags below the fold get `type="module"` (auto-deferred) or `defer`. Analytics, chat widgets, and social embeds load after the `load` event.
6. **Check server response time (TTFB):** If TTFB > 600ms, the issue is server-side. Use CDN edge caching, upgrade hosting, or move to SSG (pre-built HTML — TTFB < 50ms).

### SSL Certificate Not Issuing

**Symptoms:** Site shows "Your connection is not private" / `NET::ERR_CERT_AUTHORITY_INVALID`. Let's Encrypt fails to issue a certificate.

**Step-by-step recovery:**
1. **Verify DNS records:** `dig A example.com` + `dig AAAA example.com` must return the host's IP addresses. `dig CNAME www.example.com` must point to the host. DNS must be fully propagated (up to 48 hours, but typically < 30 minutes).
2. **Check CAA record:** `dig CAA example.com` — if a CAA record exists, it must include `letsencrypt.org`. Example: `example.com. CAA 0 issue "letsencrypt.org"`. If CAA only authorizes another CA, Let's Encrypt cannot issue.
3. **Verify the domain is pointed to the correct host:** If you changed hosting providers, the domain might still point to the old host's IPs. Cert issuance happens on the current host — old DNS records prevent completion.
4. **Try DNS validation instead of HTTP:** Most platforms allow switching validation method. DNS validation (`_acme-challenge` TXT record) is more reliable — no dependency on HTTP server being reachable.
5. **Wait and retry:** Let's Encrypt rate limits: 5 duplicate certificates per domain per week. If you've tried and failed multiple times, wait 1 hour and retry. Most platforms auto-retry on a backoff schedule.

### "Deploy Successful" but Site Shows Old Version

**Symptoms:** CI/CD reports success, but the live site still shows yesterday's content/design.

**Step-by-step recovery:**
1. **Clear CDN cache:** Cloudflare → Caching → Purge Everything. Vercel → Redeploy without cache. Netlify → Deploys → Clear cache and deploy site.
2. **Check cache headers:** If `Cache-Control: max-age=86400` (24 hours) is set on HTML, browsers cache the old version for a full day. Change to `max-age=0, must-revalidate` or `stale-while-revalidate` for HTML pages.
3. **Hard reload:** `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows) forces the browser to re-download all assets. This bypasses browser cache but not CDN cache.
4. **Check for service worker caching:** A service worker with `cache-first` strategy will serve the old version forever. Unregister the SW (DevTools → Application → Service Workers), hard reload, and fix the SW strategy to `network-first` for HTML.
5. **Verify the correct build deployed:** Some platforms deploy the latest build, not necessarily the branch you pushed. Check the deployment log for the commit SHA — does it match your latest push? If you pushed to `main` but the platform deploys from `production` branch, the deploy is stale.

### Form Submissions Not Delivering

**Symptoms:** Users submit forms, but emails/captures never arrive. No errors visible to the user.

**Step-by-step recovery:**
1. **Test the form endpoint directly:** `curl -X POST https://example.com/api/contact -d "name=Test&email=test@example.com&message=test"`. Check the HTTP response. 200 with a success message? The form handler works. 500/403/404? Check server logs.
2. **Check spam filtering:** Form submissions from @example.com or @test.com might be caught by spam filters. Test with a real email address. Add `Reply-To` header matching the submitter's email to avoid DMARC rejection (your server sending "from" the user's email domain without authorization = spam).
3. **Netlify Forms:** Verify `data-netlify="true"` attribute on the form, `netlify` attribute on `<form>`, and that the form is in the deployed HTML (not injected by JS after page load). Netlify's build bot parses static HTML forms at deploy time.
4. **Serverless function:** Check function logs (Vercel → Functions, Netlify → Functions, Cloudflare Workers → Logs). Common issues: missing environment variables, exceeded timeout (10s default on Vercel/Netlify), exceeded memory (default 1024MB).
5. **Email deliverability:** If using a transactional email service (Resend, SendGrid, Postmark), check their dashboard for bounces, spam reports, or rate limiting. Verify SPF, DKIM, and DMARC records for your sending domain.

## Verification Guardrails — Binary Deployment Checklist

Before ANY production deployment, every checkbox must be `[x]`. These are PASS/FAIL — no partial credit.

- [ ] **All images have `width` and `height` attributes** to prevent Cumulative Layout Shift (CLS). Browsers reserve space before images load. Without dimensions, text jumps when images appear. Test: open DevTools Performance tab → record a page load → check "Experience" track for layout shifts.
- [ ] **`aria-label` on all interactive elements without visible text.** Icon buttons (menu, search, close, social media), SVGs, and form controls that lack visible labels MUST have accessible names. Test: Chrome DevTools → Accessibility tab → inspect each interactive element → verify "Name" is populated.
- [ ] **Color contrast ratio ≥ 4.5:1 for normal text, ≥ 3:1 for large text (≥ 18pt or ≥ 14pt bold).** Test: WebAIM Contrast Checker or Chrome DevTools → inspect element → click color swatch → see contrast ratio. Every text color + background color pair must pass.
- [ ] **`Cache-Control` headers set for all static assets.** JS, CSS, fonts, and images must return `Cache-Control: public, max-age=31536000, immutable`. HTML must return `Cache-Control: public, max-age=0, must-revalidate` or `stale-while-revalidate`. Test: `curl -I https://example.com/main.js | grep Cache-Control`.
- [ ] **`robots.txt` does not block search engines.** The most common launch mistake: `User-agent: * \n Disallow: /` left from development. Verify: `curl https://example.com/robots.txt` must show `Allow: /` (or no `Disallow: /` line). Test individual pages: Google Search Console → URL Inspection → "Crawl allowed? Yes."
- [ ] **`sitemap.xml` generated, accessible, and submitted to Google Search Console and Bing Webmaster Tools.** Verify: `curl https://example.com/sitemap.xml` returns 200 with XML content. All listed URLs must return 200. No 404s, no redirect chains, no blocked URLs in the sitemap.
- [ ] **Open Graph + Twitter Card meta tags on every page.** Verify with: `opengraph.xyz` (paste URL) or `curl https://example.com | grep 'og:'`. Every page must have: `og:title`, `og:description`, `og:image`, `og:url`, `twitter:card`, `twitter:title`, `twitter:description`, `twitter:image`.
- [ ] **404 page exists and returns actual HTTP 404 status code.** A "soft 404" — a page that says "Not Found" but returns HTTP 200 — wastes crawl budget and confuses search engines. Test: `curl -I https://example.com/nonexistent-path` → must return `HTTP/2 404`.
- [ ] **Form submissions have server-side validation (not just client-side).** Client-side `required` and `pattern` attributes are UX, not security. Bypass: `curl -X POST https://example.com/api/contact -d "email=not-an-email"` → must return 400 with validation error, not 200 with "thanks for submitting."
- [ ] **CSP headers block inline scripts** (`Content-Security-Policy: script-src 'self'` or with nonce/hash). No `'unsafe-inline'` for `script-src`. Test: `curl -I https://example.com | grep Content-Security-Policy`. Also verify with CSP Evaluator (Google).
- [ ] **No console errors on any page.** Test: Chrome DevTools Console → navigate to every page → filter to "Errors" level → must show 0 errors. Red console errors = broken functionality for some subset of users. Warnings are acceptable; errors are not.
- [ ] **Site works without JavaScript** (progressive enhancement). Test: Chrome DevTools → Settings → Debugger → "Disable JavaScript" → reload page. Core content must be readable. Navigation must work (links, not JS router). Forms must submit (action attribute, not fetch API). If JS is required for basic content display, the site fails this guardrail.
- [ ] **Custom domain with HTTPS enforced** (HTTP → 301 → HTTPS). Test: `curl -I http://example.com` → must return `301` with `Location: https://example.com`. `curl -I https://example.com` → must return `200` with valid SSL certificate.
- [ ] **Privacy policy page exists and cookie consent is implemented** if using any tracking (Google Analytics, Facebook Pixel, Hotjar, advertising). Privacy-first analytics (Plausible, Umami) don't require cookie consent. Google Analytics does. Verify: visit site in incognito window → cookie consent banner appears → GA script is NOT loaded until user accepts.

## Sub-Skills — When to Use Specialized References

| Sub-Skill | When to Use | See Reference |
|-----------|-------------|---------------|
| **seo-audit** | Existing site needs search engine optimization overhaul — technical SEO, content optimization, backlink strategy | Invoke **seo-specialist** skill |
| **performance-audit** | Existing site fails Core Web Vitals — LCP, INP, CLS optimization, bundle analysis | Invoke **performance-engineer** skill |

## Cross-Skill Coordination

| Upstream Skill | What You Receive | When to Involve |
|----------------|-----------------|-----------------|
| **product-strategist** | Target audience, value proposition, competitive differentiation, feature priorities | Before stack selection — audience and use case drive technology choices |
| **ui-ux-designer** | Design system (typography scale, color tokens, spacing), wireframes, interaction patterns, platform-specific design conventions | Before Phase 3 (Design System) — design tokens translate directly to Tailwind config |
| **content-strategist** | Content hierarchy, information architecture, tone guidelines, messaging framework, editorial calendar | Before Phase 4 (Content Architecture) — content structure drives CMS selection and markdown layout |
| **api-designer** | OpenAPI 3.1 spec for backend services, API authentication scheme, rate limiting strategy | Before Phase 2 (Scaffolding) — API contract determines whether SSR/SSG can be used |
| **brand-guidelines** | Logo system, color palette with accessibility validation, typography, iconography, motion design | Before Phase 3 (Design System) — brand tokens become CSS custom properties |
| **ux-researcher** | User personas, journey maps, usability findings, competitive UX analysis | Before Phase 0 (Discovery) — user research drives content priorities and navigation |

| Downstream Skill | What You Provide | Impact of Delay |
|-----------------|-----------------|-----------------|
| **seo-specialist** | Site structure, URL hierarchy, content inventory, sitemap | SEO can't optimize without site architecture and content |
| **frontend-developer** | Stack decision (framework, rendering strategy), component architecture, design tokens | Frontend implementation blocked without stack and design system |
| **fullstack-developer** | Hosting platform, deployment pipeline, CMS choice, API integration points | Backend integration can't start without knowing deployment target and CMS |
| **performance-engineer** | Build configuration, caching strategy, CDN setup, image pipeline | Performance optimization requires deployed site with real traffic patterns |
| **qa-engineer** | Deployed staging environment, test user accounts, form endpoints, checkout flow | QA can't test without a running staging environment |
| **accessibility-testing** | Component inventory, interaction patterns, color tokens | Accessibility audit requires implemented UI components |
| **ci-cd-builder** | Framework build command, environment variables, deploy target, branch strategy | CI/CD can't be configured without knowing the build toolchain |

### Communication Triggers

| Trigger | Notify | Why |
|---------|--------|-----|
| Hosting platform changes pricing or features | Product Strategist, DevOps Engineer | Budget impact; may require migration |
| CMS selected dictates content workflow | Content Strategist | Content team needs training on new CMS |
| Core Web Vitals fail before launch | Performance Engineer, QA Engineer | Launch must be delayed until metrics pass |
| Third-party integration requirement surfaced (Stripe, HubSpot) | Backend Developer, Fullstack Developer | API integration may need backend work |
| Accessibility audit reveals WCAG violations | UI/UX Designer, Content Strategist | Design or content changes needed for compliance |
| SEO audit reveals missing structured data or broken URLs | SEO Specialist, Content Strategist | Content and markup fixes needed |

## Proactive Triggers
<!-- QUICK: 30s -- conditions that auto-activate this skill -->
| Trigger | Action | Rationale |
|---------|--------|-----------|
| User says "build me a website" or "create a landing page" | Start at Decision Trees → SSG Selection | Most requests are site-type-specific; match stack to type first |
| Existing site fails Lighthouse audit (Performance < 50, Accessibility < 80) | Invoke performance-engineer, then return here for stack migration if needed | Performance failure may indicate wrong stack, not just bad code |
| User asks "Webflow vs custom" or "should I use a website builder" | Jump to Core Workflow → Phase 0 (Discovery) | Platform-vs-custom is the most expensive decision; get it right upfront |
| Content team complains about update workflow | Jump to Core Workflow → Phase 4 (Content Architecture) | Pain point signals CMS mismatch; investigate markdown vs headless CMS |
| Monthly hosting bill exceeds $100 without clear justification | Jump to Cost Matrix → audit hosting choices | Static sites should cost < $5/mo; dynamic sites $20-100/mo |
| "We need a website by next week" | Start at Decision Trees → Time-Constrained Builds | Short timeline changes stack selection dramatically |

## Operating at Different Levels

| Level | Website Output Characteristics | Stack Evolution |
|-------|-------------------------------|-----------------|
| **Solo (1 person, $0-5/mo)** | Static site, markdown content, no database, no user accounts. Deployed to Cloudflare Pages or GitHub Pages. Zero maintenance. | Astro/Hugo/11ty + Git-based CMS. Plausible self-hosted analytics. Upptime for monitoring. Domain from Cloudflare Registrar. |
| **Small (2-5 people, $20-100/mo)** | Hybrid site — mostly static with a few dynamic pages (blog comments, newsletter signup, contact form). Headless CMS for non-dev editors. | Astro/Next.js hybrid + Decap CMS/Tina CMS. Vercel/Netlify Pro hosting. Sanity free tier. Resend for transactional email. Sentry free tier for error tracking. |
| **Medium (5-20 people, $100-500/mo)** | Full web app — user auth, database, API, payments, real-time features. Multi-environment (dev → staging → production). Feature flags. | Next.js/Remix + Supabase/PlanetScale. Vercel Pro/Enterprise. Headless CMS (Sanity paid). Stripe for payments. Sentry Team. Better Uptime. CI/CD with GitHub Actions. |
| **Enterprise (20+ people, $500-5,000+/mo)** | Multi-tenant SaaS, global CDN, multi-region deployment, SOC 2 compliance, SSO, audit logging, custom analytics pipeline, dedicated support. | Next.js/Remix on AWS (ECS/EKS or Amplify). Enterprise CMS (Contentful/Contentstack). Auth0/Okta for SSO. DataDog/New Relic for observability. LaunchDarkly for feature flags. Incident response on-call rotation. |

## Best Practices

1. **Prefer static over dynamic.** Every dynamic feature (SSR, serverless functions, real-time) adds cost, complexity, and failure modes. Question every requirement for dynamic behavior: "Can this be static?" A contact form can be a serverless function; it doesn't require a full SSR framework.

2. **Ship zero JavaScript by default.** Astro's "islands architecture" means JS is opt-in per component. A blog post, landing page, or documentation page ships 0KB of JS. When JS is needed (interactive search, carousel, modal), load it only for that component. The performance baseline should be "no JS required."

3. **Cache aggressively, invalidate surgically.** Hashed assets (`main.a1b2c3d4.js`) are immutable — cache forever. HTML pages change — cache for 0 seconds but serve stale while revalidating (`stale-while-revalidate`). Never cache forever without hash-based cache busting.

4. **Monitor Core Web Vitals in production, not just in Lighthouse.** Lighthouse is a lab test (simulated device, consistent conditions). Real users are on slow networks with low-end devices. Use the `web-vitals` library to collect real-user metrics (RUM) and report them to your analytics. A lab score of 95 can be a real-user score of 60.

5. **Use a CDN even for small sites.** CDNs (Cloudflare, Fastly, BunnyCDN) serve content from edge locations near the user — reducing latency from 200ms (US server → Europe visitor) to 20ms (Europe edge → Europe visitor). Cloudflare's free plan includes CDN, DDoS protection, and SSL. There is zero reason to not use a CDN.

6. **Automate image optimization at build time.** Never manually resize images for the web. Every SSG framework has built-in image processing: `@astrojs/image`, `next/image`, Hugo image processing, 11ty Image plugin. These generate responsive `srcset` attributes, convert to WebP/AVIF, and set dimensions automatically. Manual image work is wasted time and inevitably inconsistent.

7. **Version control everything except secrets.** Code, content (markdown), configuration, and design tokens go in git. Secrets (API keys, database URLs, tokens) go in environment variables. `.env` is in `.gitignore`. `.env.example` documents required variables without containing real values. A new developer should be able to clone the repo, read `.env.example`, and be fully operational in 10 minutes.

8. **Test on real devices, not just DevTools responsive mode.** Chrome DevTools emulation is for layout testing, not performance or tactile testing. Test on a low-end Android phone (Moto G series, $150-200) for performance. Test on an iPhone SE for Safari-specific bugs. Borrow devices if you don't own them. The bugs you find are the bugs your users experience.

9. **Set up CI/CD before writing features.** A deploy pipeline that builds, lints, audits accessibility, and deploys on every push to main means you can ship features continuously. Without CI/CD, each deploy is a manual, error-prone process that accumulates risk. Set up GitHub Actions (or equivalent) in Phase 2 — before any real features are built.

10. **Plan for content updates from day one.** "How does the content get updated?" is as important as "what stack should I use?" If the answer is "the original developer edits the code," the site becomes stale 6 months after they move on. Choose a CMS strategy (markdown + git, headless CMS, low-code platform) that matches the content editor's technical capability — not the developer's.


## State Log

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.

### How the State Log Works
<!-- AGENT: Read this before starting work, update after each phase -->

1. **On session start:** Check `.copilot/session-state/decision-ledger.json` for any prior decisions relevant to this domain. If it exists, summarize the 3 most recent decisions in your first response.
2. **After each major decision:** Append to the ledger:
   ```json
   {
     "timestamp": "ISO-8601",
     "skill": "website-builder",
     "phase": "Phase 3: Implementation",
     "decision": "What was decided",
     "rationale": "Why this choice over alternatives",
     "constraints": ["constraint-1", "constraint-2"],
     "alternatives_considered": ["alt-1", "alt-2"],
     "reversible": true
   }
   ```
3. **Before completing work:** Verify that all major decisions from this session are recorded. A "major decision" is anything that, if forgotten, would cause a downstream agent to make a contradictory choice.
4. **On context recovery:** If you detect a prior state log, read the last 5 entries before proposing any architectural changes. Cite the prior decisions you're building on.

### State Log Schema

| Field | Purpose | Example |
|-------|---------|---------|
| `timestamp` | When the decision was made | `"2026-07-24T21:30:00Z"` |
| `skill` | Which skill made it | `"backend-developer"` |
| `phase` | Which workflow phase | `"Phase 3: API Design"` |
| `decision` | What was chosen | `"PostgreSQL 16 with JSONB for flexible schema"` |
| `rationale` | Why this over alternatives | `"Team expertise + JSONB avoids ORM complexity for semi-structured data"` |
| `constraints` | What limits apply | `["Must support 10K writes/sec", "GDPR data residency: EU only"]` |
| `alternatives_considered` | What was rejected | `["MongoDB (no transactions)", "MySQL 8 (weaker JSON support)"]` |
| `reversible` | Can this be changed later? | `true` (migration possible) or `false` (irreversible choice) |

### Anti-Drift Check
<!-- AGENT: Run this check at the start of each new phase -->

Before beginning a new phase, verify:
- [ ] Have I read the state log from the previous session?
- [ ] Do any prior decisions constrain what I'm about to do?
- [ ] Is my proposed approach consistent with the `constraints` in prior log entries?
- [ ] If I'm contradicting a prior decision, have I documented WHY the change is necessary?

## Deliberate Practice
<!-- QUICK: 30s -- exercises to build website-builder mastery -->

| Exercise | Skill Targeted | Success Criteria | Time Investment |
|----------|---------------|------------------|-----------------|
| **Rebuild a client site from scratch in a different SSG** | Stack evaluation, migration planning | Site matches original feature-for-feature AND Lighthouse scores improve by 10+ points | 4-8 hours per platform |
| **Optimize a 50/100 Lighthouse site to 95+** | Core Web Vitals, performance debugging | All four Lighthouse categories (Performance, Accessibility, SEO, Best Practices) score 95+ on mobile | 2-4 hours per site |
| **Recreate a Webflow site as a static site using Astro** | Platform migration, content architecture | Visual parity maintained, content extractable as markdown, hosting cost reduced by 90%+ | 6-10 hours |
| **Build a 3-page marketing site in under 2 hours** | Rapid prototyping, SSG proficiency | Lighthouse 95+, mobile-first, deployed to production, $0/month hosting | 2 hours |
| **Audit a site's JavaScript and remove everything non-essential** | Progressive enhancement discipline | Site remains fully functional with JS disabled; bundle size reduced by 50%+ | 2-3 hours |
| **Implement structured data for all page types (Article, Product, FAQ, Breadcrumb)** | SEO architecture | Google Rich Results Test validates all structured data; no errors or warnings | 1-2 hours |
| **Set up CI/CD for a static site with Lighthouse budget in GitHub Actions** | DevOps for websites | Build fails if Lighthouse Performance < 90 or Accessibility < 95; deploys on passing | 1-2 hours |
| **Migrate a site from one host to another in under 4 hours** | Platform portability, domain configuration | Zero downtime, SSL intact, all redirects preserved, DNS propagation handled | 4 hours |

## Production Checklist — Pre-Launch Verification

- [ ] **P1. Lighthouse Performance ≥ 90 on mobile** (simulated 4G, Moto G4). Target: 95+. Check at PageSpeed Insights.
- [ ] **P2. Lighthouse Accessibility = 100.** Every point below 100 is a fixable issue. axe DevTools catches what Lighthouse misses.
- [ ] **P3. Lighthouse SEO = 100.** Meta descriptions, structured data, valid robots.txt, sitemap generation, canonical URLs, mobile-friendly.
- [ ] **P4. Lighthouse Best Practices = 100.** HTTPS, correct image aspect ratios, no deprecated APIs, no known vulnerabilities in JS libraries.
- [ ] **P5. Custom domain configured with HTTPS redirect.** `http://example.com` → 301 → `https://example.com`. `http://www.example.com` → 301 → `https://example.com` (or vice versa — pick one canonical domain).
- [ ] **P6. SSL certificate valid with auto-renewal.** Check SSL Labs (ssllabs.com/ssltest) for grade A+. Verify Let's Encrypt auto-renewal is active.
- [ ] **P7. `<title>` and `<meta name="description">` on every page.** No duplicates. Descriptions 120-155 characters. Titles 50-60 characters. Check with Screaming Frog or `curl` + grep.
- [ ] **P8. Open Graph + Twitter Card tags verified** on all sharable pages. Test with `opengraph.xyz` or Twitter Card Validator. Images must be 1200×630px minimum.
- [ ] **P9. Structured data (JSON-LD) validated.** Test with Google Rich Results Test and Schema.org Validator. Fix all errors and warnings.
- [ ] **P10. `robots.txt` verified** — not blocking search engines. Sitemap URL included in robots.txt.
- [ ] **P11. `sitemap.xml` verified** — all URLs return 200, no 404s, no redirect chains, no `noindex` pages in sitemap.
- [ ] **P12. 404 page functional** — returns HTTP 404, provides navigation (search bar, popular pages, home link), matches site design.
- [ ] **P13. Forms functional** — test every form (contact, newsletter, checkout, search). Server-side validation working. Confirmation email received. Spam protection (honeypot field or CAPTCHA).
- [ ] **P14. `Cache-Control` headers correct** — hashed assets: immutable + long max-age. HTML: short max-age with stale-while-revalidate. Verify with `curl -I`.
- [ ] **P15. CSP header deployed** — no `unsafe-inline` for `script-src`. Test with CSP Evaluator. Monitor for reports (report-uri or report-to).
- [ ] **P16. Analytics receiving data** — Plausible/Umami/GA4 shows real-time visitors. Verify pageview events fire. Verify no PII in analytics data (GDPR compliance).
- [ ] **P17. Error tracking configured** — Sentry or equivalent receives JS errors from production. Verify a test error appears in the dashboard.
- [ ] **P18. Environment variables verified** — all required variables set in production environment. No development values (`localhost`, test API keys) leaked to production.
- [ ] **P19. Rate limiting enabled** — Vercel WAF, Cloudflare Rate Limiting, or equivalent. Prevent bot crawls from triggering serverless function overages.
- [ ] **P20. Backup and rollback plan tested** — can you revert to the previous deploy in under 5 minutes? Test it. Previous deploy must remain accessible as a rollback target.

## What Good Looks Like

> The site loads in under 1.5 seconds on a $150 Android phone with 4G connectivity. Every page scores 95+ on Lighthouse mobile (Performance, Accessibility, SEO, Best Practices). The homepage is under 150KB total (HTML + CSS + JS + images + fonts). Meta tags, structured data, and sitemaps were part of the initial scaffold — not retrofitted. The monthly hosting bill is under $20 and clearly understood by the site owner. Content editors update blog posts through a visual CMS without touching git. Forms validate server-side, deliver emails reliably, and have never been exploited. The site has never had a security breach, never failed a Core Web Vitals threshold, and never shown a blank page to a visitor. When the platform changes pricing, the site can migrate to an alternative in under 4 hours because the content is stored as markdown in git. This is what a 10/10 website build looks like.

## References

- **Content Architecture Patterns**: Content modeling (collections, taxonomies, relationships), multilingual strategies, CMS migration paths, markdown-to-headless-CMS workflow. See Astro content collections, Hugo taxonomies, and 11ty data cascade docs.
- **Static Site Starter Templates**: Scaffolding for Astro (content collections, View Transitions), Hugo (modules, pipes), 11ty (data cascade, pagination), and Next.js (App Router, static exports). See framework docs for deployment config.
- **E-commerce Platform Comparison**: Shopify vs Medusa vs Saleor vs custom — checkout optimization, product page patterns, payment gateway integration, headless commerce API design.
- **SaaS Landing Page Patterns**: Waitlist pages, pricing tables, interactive demos, ROI calculators, social proof sections, and conversion rate optimization. See [landingfolio.com](https://landingfolio.com) for inspiration.
- **Web App Deployment Architecture**: Auth (Auth0, Clerk, Supabase), database (PlanetScale, Neon, Turso), API routes, real-time (WebSocket, Server-Sent Events), edge functions.
- **Low-Code Platforms**: Webflow (designer interface, CMS, interactions), Framer (React-based, animations), Bubble (no-code web apps). Know the migration path before committing.
- **Maintenance Guide**: Dependency upgrade cadences, security patch workflows, content audit automation, hosting migration runbooks, domain renewal checklists.
- **Core Web Vitals**: [web.dev/vitals](https://web.dev/vitals/), Lighthouse CI, `web-vitals` library, CrUX dashboard, PageSpeed Insights API.
- **Structured Data**: [schema.org](https://schema.org/), Google Rich Results Test, JSON-LD generation patterns, breadcrumb/FAQ/Article/Product schemas.
- **CDN & Hosting**: Cloudflare Pages, Vercel, Netlify, GitHub Pages, BunnyCDN — free tiers, limits, custom domain setup, SSL automation.
