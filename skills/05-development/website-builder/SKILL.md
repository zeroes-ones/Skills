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

## Anti-Hallucination
<!-- STANDARD: 3min -->

* Admit uncertainty. If you cannot determine the correct approach, ask — do not guess.
* Flag your knowledge cutoff. If this project uses tools or patterns you have not seen, state your assumptions.
* Never guess security. If work touches auth, payments, or PII, route to security-reviewer.
* [VERIFIED] before any production guidance: Verify assumptions. Verify compatibility. Verify correctness.

## Route the Request
<!-- STANDARD: 3min -->

<!-- QUICK: 30s — auto-route first, then intent-route -->

#

## Auto-Route (No User Input Required)
<!-- STANDARD: 3min -->

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

#

## Intent Route (Ask the User)
<!-- STANDARD: 3min -->

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
<!-- STANDARD: 3min -->

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
| **R11** | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| **R12** | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |

- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.

## The Expert's Mindset
<!-- STANDARD: 3min -->

#

## The Mental Model Shift
<!-- STANDARD: 3min -->

Competent web developers build sites that look good on their MacBook Pro with gigabit WiFi. Masters build sites that **load in under 2.5 seconds on a $150 Android phone with 3G connectivity, render correctly at 320px width, score 100 on Lighthouse, and cost $0/month to host indefinitely.** The shift: your Retina display is not representative. The median web user browses on a mid-range mobile device with variable connectivity. Design for constraints first — enhance for abundance.

#

## Cognitive Biases That Kill Websites
<!-- STANDARD: 3min -->

| Bias | How It Manifests | Antidote |
|-------|------------------|----------|
| **Stack familiarity bias** | Choosing Next.js for a 3-page brochure site because "I know React" — adding 80KB of JS for zero dynamic functionality | Match the stack to the requirements, not your resume. A 3-page site needs 0KB of JS. Astro ships 0KB by default. |
| **Shiny object syndrome** | Adopting the newest framework (SolidStart, Qwik, Analog) for a production client site — zero ecosystem, no Stack Overflow answers | Bet on boring technology for production. If a framework is < 2 years old and < 10K GitHub stars, it's for side projects, not client sites. |
| **Over-engineering the CMS** | Building a custom headless CMS + GraphQL API for a blog that one person updates quarterly — 80 hours of engineering for a markdown folder | Content update frequency drives CMS complexity. Quarterly updates = markdown. Daily updates by 5+ people = headless CMS. Match investment to usage. |
| **Desktop-first design** | Designing at 1440px and "adapting" to mobile — mobile feels like a cramped afterthought | Design at 320px first. If it works on a tiny screen, it works everywhere. Mobile-first CSS (min-width breakpoints) enforces this mechanically. |

#

## What Website Masters Know That Others Don't
<!-- STANDARD: 3min -->

- **The cheapest hosting is no hosting.** A static site deployed to Cloudflare Pages or GitHub Pages costs $0/month forever. No servers to patch, no databases to backup, no runtime to monitor. If your site doesn't need server-side logic, don't pay for server-side infrastructure.
- **JavaScript is a progressive enhancement, not a requirement.** Your site must be functional and readable with JavaScript disabled. Semantic HTML handles navigation, forms, and content. JavaScript adds interactivity (animations, filtering, dynamic loading) but must never be the sole mechanism for core functionality.
- **SEO is a compounding investment.** A site with perfect SEO shipped today starts earning organic traffic in 3-6 months. A site with "SEO later" loses 6+ months of compounding traffic growth. Every month you delay SEO is a month of traffic you'll never get back.
- **Platform risk is real and often invisible.** Webflow, Shopify, Squarespace — they can change pricing, remove features, or get acquired. Your content and code should be extractable. Static site generators produce plain HTML/Markdown — portable to any host. Proprietary platforms produce locked-in data. The portability difference is existential.
- **The performance-poverty line divides the web.** Sites that load in < 2s on a budget device have global reach. Sites that require a flagship phone and fiber connection only serve the top 20% of users by income. Every 100KB of JS you ship excludes more of the world.

#

## When to Break Your Own Rules
<!-- STANDARD: 3min -->

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
<!-- STANDARD: 3min -->

### Decision Tree 1: Rendering Strategy

        ┌── INPUT: Website content & traffic profile
        │
   ┌────┴────┐
   │         │
   ▼         ▼
Content    Content
changes    changes
rarely     frequently
(<daily)?  or is user-
   │       specific?
   │          │
   ▼     ┌────┴────┐
STATIC   │         │
SITE     ▼         ▼
GENERA-  Real-time  SEO is
TOR (SSG) dashboard  critical?
Build at   or highly    │
deploy,    interactive?┌────┴────┐
serve      │         │
static     ▼         ▼
HTML     SINGLE    YES       NO
from     PAGE APP   │         │
CDN      (SPA)      ▼         ▼
         Client-   SERVER-   SPA
         side      SIDE      with
         rendered  RENDERING prerender
                   (SSR) or  or
                   Incremental CSR-only
                   Static
                   Regen (ISR)

### Decision Tree 2: CMS Selection

        ┌── INPUT: Content management needs
        │
   ┌────┴────┐
   │         │
   ▼         ▼
Non-tech   Developers
content     are the
editors?    only editors?
   │         │
   ▼         ▼
HEADLESS   GIT-BASED
CMS        CMS
(Strapi,   (markdown
Sanity,    files +
Contentful) git workflow)
   │         │
   ▼         ▼
Need       Need
WYSIWYG +  versioning
media      and PR
library?   workflows?
   │         │
   ▼         ▼
Sanity     Contentful
or         or custom
Strapi     MDX setup

### Decision Tree 3: Hosting Platform

        ┌── INPUT: Site complexity & traffic
        │
   ┌────┴────┐
   │         │
   ▼         ▼
Static     Needs
site?      backend
   │       (API, DB,
   │       server
   ▼       functions)?
CLOUDFLARE    │
PAGES or  ┌────┴────┐
Netlify    │         │
(CDN-      ▼         ▼
native,   Serverless Custom
free      functions  runtime
tier)     only?      needed?
             │         │
        ┌────┴────┐    ▼
        │         │  RAILWAY,
        ▼         ▼  FLY.IO,
      Vercel    Netlify or
      (Next.js  AWS ECS
      native)   Functions  (Docker/
                (AWS Lambda container)
                backend)

Detailed reference material

> 📎 Full content extracted to [references/decision-trees.md](references/decision-trees.md) — 158 lines of detailed guidance, patterns, and code examples.

## Core Workflow
<!-- STANDARD: 3min -->

Before writing a single line of code or choosing a platform, answer five questions. The answers dete...

> 📎 See [references/core-workflow.md](references/core-workflow.md) for complete guidance (398 lines).
## Cost Matrix — Full Transparency
<!-- STANDARD: 3min -->

Detailed reference material

> 📎 Full content extracted to [references/cost-matrix---full-transparency.md](references/cost-matrix---full-transparency.md) — 54 lines of detailed guidance, patterns, and code examples.

## Gotchas — Dollar-Quantified Website Footguns
<!-- STANDARD: 3min -->

- **"I'll just use WordPress" → $3,200/mo in security cleanup.** WordPress power...

> 📎 Full content extracted to [references/gotchas---dollar-quantified-website-footguns.md](references/gotchas---dollar-quantified-website-footguns.md) — 25 lines of detailed guidance, patterns, and code examples.

## Error Recovery — Explicit Step-by-Step
<!-- STANDARD: 3min -->

**Symptoms:** Build process crashes with `JavaScript heap out of memory`, `FATAL...

> 📎 Full content extracted to [references/error-recovery---explicit-step-by-step.md](references/error-recovery---explicit-step-by-step.md) — 68 lines of detailed guidance, patterns, and code examples.

## Error Recovery
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

| Symptom | Root Cause | Fix |
|---------|-----------|-----|
| Site loads blank page after deployment | Build output path mismatch — framework outputs to `/dist` but CDN serves from `/build` | Verify build output directory matches CDN config. Run `npm run build && ls dist/` or `ls .next/`. Check `_redirects` or `vercel.json` for correct output |
| Form submissions silently fail with 0 emails received | Server-side validation missing or email service not configured; client-side validation passed but server rejected | Check server logs for form endpoint. Verify email service API key and sender domain. Add monitoring: alert if 0 submissions in 24 hours. Always validate server-side |
| Lighthouse SEO score drops from 100 to 60 after relaunch | Missing meta tags, broken canonical URLs, or robots.txt blocking all crawlers post-migration | Audit: `curl -I https://site.com | grep -i robot`, check `<meta name="robots">` is NOT `noindex`, verify `sitemap.xml` is accessible and submitted to Search Console |
| Images load as broken on production but work locally | Relative paths that break with base URL change, or CDN misconfigured to block referrer | Use absolute URLs or `import` for assets. Check CDN CORS headers. Verify `assetPrefix` in framework config matches production domain |
| Mobile menu doesn't open — JS error in console | Third-party script loaded synchronously blocks menu JS execution | Load third-party scripts with `async` or `defer`. Use Partytown for heavy scripts. Check browser console for render-blocking errors |
| Fonts flash invisible for 3 seconds then appear | `font-display: block` (default) hides text during font load; on slow 3G this means invisible text for seconds | Set `font-display: swap` on all `@font-face` declarations. Preload critical fonts: `<link rel="preload" as="font" crossorigin>` |

## Gotchas
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

| Gotcha | Cost | Fix |
|--------|------|-----|
| Building a custom CMS when a static site generator would suffice — over-engineering maintenance burden | $50K-$200K in unnecessary development and maintenance costs; 80% of website needs are content display, not dynamic logic | Use Astro/Hugo/11ty for content sites. Only add a CMS or backend when user-generated content, auth, or real-time features are requirements |
| Choosing a platform without checking the exit strategy — site trapped in proprietary ecosystem | $20K-$100K in migration costs when platform raises prices or discontinues features; content locked in proprietary database format | Store content as markdown in git. Use standard frameworks (Astro, Next.js, Hugo, 11ty). Test: can you migrate to an alternative host in <4 hours? |
| Ignoring Core Web Vitals until after launch — 53% of mobile visitors abandon sites taking >3 seconds | $50K-$500K in lost conversions; each 100ms delay in LCP reduces conversion rate by ~1%. Google uses CWV as ranking signal | Target: LCP <2.5s, FID <100ms, CLS <0.1. Set performance budgets before writing code. Test on real Moto G4 with 4G throttling, not MacBook Pro |
| Not implementing form submission monitoring — 3 weeks of silent failures before noticing | $10K-$50K in lost leads/sales; broken contact form = 0 leads for weeks with no alert | Monitor form submissions: alert if 0 in 24 hours for a form that normally gets 5+/day. Send confirmation emails. Test form weekly with edge case inputs |
| Deploying without CSP headers — first XSS vulnerability compromises entire site | $50K-$500K in breach costs; XSS via a third-party script or user content can exfiltrate all user data | Set Content-Security-Policy without `unsafe-inline` or `unsafe-eval`. Add HSTS, X-Frame-Options, X-Content-Type-Options. Test with Mozilla Observatory |
| Not compressing or optimizing images — 5MB hero image on homepage | $20K-$80K in lost SEO traffic; Largest Contentful Paint blocked by unoptimized image drops search rankings | Use `<img>` with `srcset` and `sizes`. Convert to WebP/AVIF with `<picture>`. Lazy load below-fold images. Target: hero image <100KB, all images <200KB |
| Using `target="_blank"` without `rel="noopener noreferrer"` — security vulnerability | $10K-$50K in phishing risk; opened page can redirect original page to phishing site via `window.opener.location` | Always use `rel="noopener noreferrer"` with `target="_blank"`. ESLint rule: `react/jsx-no-target-blank`. This is a known security anti-pattern |

## Verification Guardrails — Binary Deployment Checklist
<!-- STANDARD: 3min -->

Before ANY production deployment, every checkbox must be `[x]`. These are PASS/F...

> 📎 Full content extracted to [references/verification-guardrails---binary-deployment-checklist.md](references/verification-guardrails---binary-deployment-checklist.md) — 18 lines of detailed guidance, patterns, and code examples.

## Sub-Skills — When to Use Specialized References
<!-- STANDARD: 3min -->

| Sub-Skill | When to Use | See Reference |

> 📎 Full content extracted to [references/sub-skills---when-to-use-specialized-references.md](references/sub-skills---when-to-use-specialized-references.md) — 6 lines of detailed guidance, patterns, and code examples.

## Cross-Skill Coordination
<!-- STANDARD: 3min -->

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

#

## Communication Triggers
<!-- STANDARD: 3min -->

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
<!-- STANDARD: 3min -->

| Level | Website Output Characteristics | Stack Evolution |
|-------|-------------------------------|-----------------|
| **Solo (1 person, $0-5/mo)** | Static site, markdown content, no database, no user accounts. Deployed to Cloudflare Pages or GitHub Pages. Zero maintenance. | Astro/Hugo/11ty + Git-based CMS. Plausible self-hosted analytics. Upptime for monitoring. Domain from Cloudflare Registrar. |
| **Small (2-5 people, $20-100/mo)** | Hybrid site — mostly static with a few dynamic pages (blog comments, newsletter signup, contact form). Headless CMS for non-dev editors. | Astro/Next.js hybrid + Decap CMS/Tina CMS. Vercel/Netlify Pro hosting. Sanity free tier. Resend for transactional email. Sentry free tier for error tracking. |
| **Medium (5-20 people, $100-500/mo)** | Full web app — user auth, database, API, payments, real-time features. Multi-environment (dev → staging → production). Feature flags. | Next.js/Remix + Supabase/PlanetScale. Vercel Pro/Enterprise. Headless CMS (Sanity paid). Stripe for payments. Sentry Team. Better Uptime. CI/CD with GitHub Actions. |
| **Enterprise (20+ people, $500-5,000+/mo)** | Multi-tenant SaaS, global CDN, multi-region deployment, SOC 2 compliance, SSO, audit logging, custom analytics pipeline, dedicated support. | Next.js/Remix on AWS (ECS/EKS or Amplify). Enterprise CMS (Contentful/Contentstack). Auth0/Okta for SSO. DataDog/New Relic for observability. LaunchDarkly for feature flags. Incident response on-call rotation. |

## Best Practices
<!-- STANDARD: 3min -->

1. **Prefer static over dynamic.** Every dynamic feature (SSR, serverless functi...

> 📎 Full content extracted to [references/best-practices.md](references/best-practices.md) — 21 lines of detailed guidance, patterns, and code examples.

## State Log
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.

#

## How the State Log Works
<!-- STANDARD: 3min -->
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

#

## State Log Schema
<!-- STANDARD: 3min -->

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

#

## Anti-Drift Check
<!-- STANDARD: 3min -->
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

## Error Decoder — War Stories from the Trenches
<!-- STANDARD: 3min -->

**(STANDARD)**

When website builds go wrong, they go wrong in predictable ways. Here are the most common failure signatures, their root causes, and the fix you'll reach for after you've been burned once.

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| 404 on page refresh — user navigates to `/about`, hits refresh, gets "404 Not Found" from the server | SPA client-side routing handles navigation via History API, but the server doesn't know about `/about` — it only serves `index.html`. A direct request to any route other than `/` hits the server, which has no file at that path | Configure server to serve `index.html` for all routes (SPA fallback). For Netlify: `_redirects` with `/* /index.html 200`. For Vercel: `rewrites` in `vercel.json`. For Apache: `FallbackResource /index.html`. For Nginx: `try_files $uri /index.html` | Client-side routing creates URLs that only exist in the browser's memory. The server has never heard of `/about` — it needs a catch-all rule to delegate routing to the client |
| Lighthouse Performance drops from 98 to 45 after adding Google Analytics — LCP goes from 1.2s to 4.8s | Third-party scripts load synchronously and block the main thread. `gtag.js` downloads, parses, and executes before the browser can finish painting the page. The script is render-blocking because it's loaded via a regular `<script>` tag | Load analytics with `async` or `defer`: `<script async src="https://www.googletagmanager.com/gtag/js">`. Use Partytown to run third-party scripts in a Web Worker off the main thread. Set a performance budget in Lighthouse CI that fails the build if any third-party script exceeds 50ms blocking time | Third-party scripts are performance kryptonite. A single synchronous `<script>` tag can add 3+ seconds to page load. Every script must be `async`, `defer`, or offloaded to a worker |
| Image loads, text shifts down 200px — user taps the wrong link because the page jumped. Cumulative Layout Shift (CLS) is 0.45 | `<img>` lacks explicit `width` and `height` attributes. The browser doesn't know the image dimensions until it downloads the file. Text content renders first, then images push everything down as they load in | Always set `width` and `height` on every `<img>` tag, paired with `aspect-ratio` in CSS or `style="aspect-ratio: 16/9"`. Modern browsers reserve the space before the image loads. Use `loading="lazy"` for below-fold images | The browser renders HTML top-to-bottom without knowing future element sizes. An image without dimensions takes 0px of space until it loads — then claims its real size and shifts everything below it. Two attributes prevent the shift |
| `window is not defined` during SSR — Next.js/Astro build fails with obscure error, production deploy is blocked | Server-side code references browser-only globals (`window`, `document`, `localStorage`, `navigator`). Node.js has no DOM — these don't exist. The code may be in a component that the bundler includes in the server bundle | Guard browser API access: `if (typeof window !== 'undefined') { ... }`. Use `useEffect` for browser-only code (runs only on client). For Next.js, use `'use client'` directive. For Astro, use `<script>` or `client:load` directive. Use `import.meta.env.SSR` to detect server context | Node.js and browsers share JavaScript syntax but not runtime APIs. Every reference to `window` or `document` is a potential SSR crash. The build succeeds locally because the bundler doesn't evaluate runtime code |
| CDN serves stale HTML for days after deploy — users see old content, purge button didn't help, business-critical update invisible | HTML is cached at the CDN edge with a long `max-age`. The new deploy uploads fresh HTML to origin, but the CDN already cached the old version. Cache invalidation is eventually consistent — purge requests take minutes to propagate globally | Set short cache TTL for HTML: `Cache-Control: public, max-age=0, must-revalidate`. Long-cache static assets by content hash: `app.a1b2c3d4.js`. Use CDN purge API on deploy: `curl -X POST "https://api.cloudflare.com/.../purge_cache"`. Add cache-busting query params for emergency purges | HTML is the entry point — cache it aggressively and you lose the ability to update your site. Cache-bust hashes on static assets let you cache them forever while HTML stays fresh. The trade-off: one cached HTML file = your entire deployment pipeline is invisible |
| Form submissions work locally, silently fail in production — 50+ leads lost before anyone notices. No error, no bounce, just an empty inbox | Server-side form handler (API route or serverless function) crashes on input it didn't expect: empty field, emoji in name, plus-sign in email. The client-side `fetch` resolves (the request was sent) but the server returns 500. No client-side error handling checks the response | Check `response.ok` after every form fetch: `if (!response.ok) throw new Error(...)`. Add server-side validation with clear error messages. Set up form submission monitoring: log every submission, alert if submissions stop. Test with edge-case inputs: emoji, SQL fragments, 1000-character names | Client-side `fetch` doesn't throw on HTTP errors — it throws on network errors. A 500 response is a "successful" fetch. You must explicitly check `response.ok` or `response.status` on every form submission |
| CSS `font-display: block` causes invisible text for 3 seconds on slow connections — users bounce before reading a single word | Web font hasn't loaded yet. `font-display: block` tells the browser to hide text (invisible fallback) for up to 3 seconds while the font downloads. On 3G, the font takes 4+ seconds — text is invisible the entire time | Use `font-display: swap` — the browser shows fallback text immediately, then swaps to the web font when loaded. Preload critical fonts: `<link rel="preload" as="font" crossorigin>`. Subset fonts to Latin-only if targeting English-speaking audiences | The browser's font loading strategy determines whether users see your content in 0ms or 3000ms. `font-display: swap` guarantees content is readable immediately. Invisible text for 3 seconds is a worse UX than using a system font |

## Verification
<!-- STANDARD: 3min -->

| # | Complete when... | Verify |
|---|-----------------|--------|
| ☐ | Complete when Lighthouse Performance ≥ 90 on mobile (simulated 4G, Moto G4) for every page | Run Lighthouse CI on PR; build fails if Performance < 90 or Accessibility < 95 |
| ☐ | Complete when All `<img>` tags have explicit `width` and `height` attributes paired with `aspect-ratio` in CSS | `grep -r "<img" src/ | grep -v "width="` returns zero results; CLS < 0.1 verified |
| ☐ | Complete when Third-party scripts loaded with `async`, `defer`, or Partytown — zero render-blocking scripts | Lighthouse report shows zero render-blocking resources; blocking time < 50ms per script |
| ☐ | Complete when HTML cache TTL set short (`max-age=0, must-revalidate`); static assets cached by content hash | `curl -I https://site.com | grep Cache-Control` confirms short TTL for HTML; assets use hash filenames |
| ☐ | Complete when Form submissions check `response.ok` on every fetch; server-side validation catches edge cases (emoji, SQL fragments, 1000-character names) | Test form with all edge-case inputs; submission monitoring alerts on zero-submission periods |
| ☐ | Complete when `font-display: swap` on all `@font-face` declarations; critical fonts preloaded with `<link rel="preload" as="font" crossorigin>` | Lighthouse FCP < 1.8s; no invisible text period during font loading on Slow 3G |
| ☐ | Complete when Structured data (JSON-LD) validated for all page types: Article, Product, FAQ, Breadcrumb | Google Rich Results Test returns zero errors or warnings for every page template |
| ☐ | Complete when SPA fallback configured: server returns `index.html` for all routes; no 404 on page refresh for client-side routes | `curl -I https://site.com/about` returns 200, not 404; Netlify `_redirects` or Vercel `rewrites` configured |
| ☐ | Complete when CSP headers set without `unsafe-inline` or `unsafe-eval`; security headers (HSTS, X-Frame-Options, X-Content-Type-Options) present | `curl -I https://site.com | grep -E "Content-Security|Strict-Transport|X-Frame|X-Content"` confirms all headers |
| ☐ | Complete when Site migratable in <4 hours: content stored as markdown in git, no proprietary lock-in, DNS and SSL documented | Migration runbook tested: clone repo → install deps → build → deploy to alternate host in <4 hours |

## Production Checklist — Pre-Launch Verification
<!-- STANDARD: 3min -->

- [ ] **P1. Lighthouse Performance ≥ 90 on mobile** (simulated 4G, Moto G4). Tar...

> 📎 Full content extracted to [references/production-checklist---pre-launch-verification.md](references/production-checklist---pre-launch-verification.md) — 22 lines of detailed guidance, patterns, and code examples.

## What Good Looks Like
<!-- STANDARD: 3min -->

> The site loads in under 1.5 seconds on a $150 Android phone with 4G connectivity. Every page scores 95+ on Lighthouse mobile (Performance, Accessibility, SEO, Best Practices). The homepage is under 150KB total (HTML + CSS + JS + images + fonts). Meta tags, structured data, and sitemaps were part of the initial scaffold — not retrofitted. The monthly hosting bill is under $20 and clearly understood by the site owner. Content editors update blog posts through a visual CMS without touching git. Forms validate server-side, deliver emails reliably, and have never been exploited. The site has never had a security breach, never failed a Core Web Vitals threshold, and never shown a blank page to a visitor. When the platform changes pricing, the site can migrate to an alternative in under 4 hours because the content is stored as markdown in git. This is what a 10/10 website build looks like.

## References
<!-- STANDARD: 3min -->

Detailed reference material loaded on demand:

- **Anti-Rationalization**: See [anti-rationalization.md](references/anti-rationalization.md)
- **Best Practices**: See [best-practices.md](references/best-practices.md)
- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Deliberate Practice**: See [deliberate-practice.md](references/deliberate-practice.md)
- **Error Recovery**: See [error-recovery.md](references/error-recovery.md)
- **Gotchas**: See [gotchas.md](references/gotchas.md)
- **State Log**: See [state-log.md](references/state-log.md)
- **Sub-Skills**: See [sub-skills.md](references/sub-skills.md)
- **Verification Guardrails**: See [verification-guardrails.md](references/verification-guardrails.md)
- **What Good Looks Like**: See [what-good-looks-like.md](references/what-good-looks-like.md)

#

## External Resources
<!-- STANDARD: 3min -->

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
