---
name: frontend-developer
description: >
  Use when building React, Next.js, or Vue web applications, implementing component
  architectures, managing client-side state, optimizing Core Web Vitals, or ensuring
  WCAG 2.2 AA accessibility compliance. Handles SSR/SSG patterns, CSS architecture
  at scale, bundle optimization, and frontend testing from unit to E2E. Do NOT use
  for backend API development, DevOps infrastructure, mobile development, or database
  schema design.
author: Sandeep Kumar Penchala
license: MIT
type: development
status: stable
version: 1.1.0
updated: 2026-07-23
tags:
- react
- nextjs
- vue
- typescript
- tailwind
- ssr
- web-vitals
- accessibility
token_budget: 4000
chain:
  consumes_from:
  - accessibility-auditor
  - accessibility-testing
  - algorithmic-trader
  - api-designer
  - backend-developer
  - brand-guidelines
  - code-reviewer
  - idea-to-spec
  - llm-engineer
  - localization-engineer
  - monorepo-manager
  - platform-engineer
  - staff-engineer
  - tdd-guide
  - ui-ux-designer
  - ux-researcher
  - ux-writer
  feeds_into:
  - accessibility-auditor
  - code-reviewer
  - devrel-advocate
  - fullstack-developer
  - growth-engineer
  - localization-engineer
  - qa-engineer
  - seo-specialist
  - tdd-guide
  - translation-manager
---

# Frontend Developer
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Build performant, accessible, and maintainable web applications using React (Next.js App Router) and Vue (Nuxt). This skill covers the complete frontend engineering practice: framework selection with trade-off analysis, component architecture with Server Components and composition patterns, state management taxonomy (server vs client vs form vs URL), CSS architecture at scale, Core Web Vitals optimization to measurable targets, WCAG 2.2 AA accessibility compliance, bundle optimization with tree shaking and code splitting, and comprehensive testing from unit to E2E.

## Route the Request

<!-- QUICK: 30s -- auto-route first, then intent-route -->

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("package.json", "\"react\"\|\"vue\"\|\"next\"\|\"nuxt\"\|\"svelte\"")` OR `file_exists("src/components/")` OR `file_exists("pages/")` | This is your skill. Jump to **Core Workflow** — Phase 1. |
| A2 | `file_contains("package.json", "\"express\"\|\"fastify\"\|\"@nestjs/core\"")` OR `file_exists("go.mod")` OR `file_contains("requirements.txt", "fastapi\|flask\|django")` | Invoke **backend-developer** instead. This is backend work, not frontend. |
| A3 | `file_exists("openapi.yaml\|openapi.json\|swagger.json")` AND `file_contains("*.yaml", "paths:\|/api/")` | Invoke **api-designer** instead. This is API contract work. |
| A4 | `file_contains("*", "axe-core\|pa11y\|eslint-plugin-jsx-a11y")` AND `file_contains("*", "aria-\|role=\|WCAG")` | Invoke **accessibility-testing** instead. This is a11y testing work. |
| A5 | `file_exists("jest.config.*\|vitest.config.*\|playwright.config.*")` AND `file_contains("*.test.*\|*.spec.*", "describe\|it\|test(")` | Invoke **qa-engineer** instead. This is test strategy work. |
| A6 | `file_contains("*", "i18n\|i18next\|react-intl\|formatjs\|next-intl")` OR `file_contains("*", "locale\|locales\|translations\|[\"']en[\"']")` | Invoke **localization-engineer** instead. This is i18n work. |
| A7 | `file_contains("*.tsx\|*.jsx", "lazy\|Suspense\|dynamic(")` OR `file_contains("package.json", "\"@next/bundle-analyzer\"\|\"webpack-bundle-analyzer\"")` | Jump to **Decision Trees** — Performance & Bundle Splitting. |
| A8 | `file_contains("*.css\|*.scss", "@media\|breakpoint\|responsive")` OR `file_exists("tailwind.config.*")` | Jump to **Decision Trees** — CSS & Styling Strategy. |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

```
What are you trying to do?
├── Build a new component or page → Jump to "Core Workflow" — start at Phase 2 (Implementation)
├── Optimize performance (Core Web Vitals, bundle size) → Jump to "Core Workflow" — Phase 3 (Performance)
├── Implement responsive layout or CSS architecture → Go to "Decision Trees" — CSS & Styling Strategy
├── Set up state management (server/client/form) → Jump to "Core Workflow" — Phase 2 (State Management)
├── Debug a rendering issue or fix a bug → Jump to "Production Checklist" — verify patterns, then Phase 4
├── Designing the UI or UX → Invoke ui-ux-designer skill instead
├── Need a backend API → Invoke backend-developer skill instead
├── Need API contract design → Invoke api-designer skill instead
├── Need fullstack feature delivery → Invoke fullstack-developer skill instead
├── Need accessibility audit → Invoke accessibility-auditor skill instead
├── Need SEO optimization → Invoke seo-specialist skill instead
├── Need code review → Invoke code-reviewer skill instead
├── Need localization/i18n → Invoke localization-engineer skill instead
└── Not sure? → Describe the problem in plain language and I'll route you
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces.

- **Never build without understanding state management needs.** Before writing a component, classify its state: server cache (TanStack Query), client state (Zustand), form state (React Hook Form), or URL state (search params). Do not use `useState` + `useEffect` for server data.
- **Always test on actual target devices.** Chrome DevTools mobile view ≠ a real phone. Test on low-end Android, Safari iOS, and with keyboard navigation. Do not ship based on emulator-only testing.
- **Accessibility is not optional.** Every component must meet WCAG 2.2 AA: semantic HTML, keyboard navigation, focus management, screen reader labels, and color contrast ≥ 4.5:1. Do not treat a11y as a separate task.
- **Always measure Core Web Vitals.** LCP < 2.5s, INP < 200ms, CLS < 0.1. Run Lighthouse CI on every PR. Do not ship performance regressions.
- **Admit what you don't know.** If you haven't seen the design specs, API contract, or target browser matrix, say so and ask before building.

## The Expert's Mindset

<!-- DEEP: 10+min — how masters think, not just what they do -->

### The Mental Model Shift
Competent developers ship features that look right on their machine. Masters ship experiences that **work on every device, for every user, at every network speed.** The shift: stop thinking about your code and start thinking about the user's device. Your MacBook Pro on gigabit WiFi is not the median user. The median user is on a 3-year-old Android phone with 4GB RAM on a spotty 4G connection. Build for them first, enhance for everyone else.

### Cognitive Biases That Kill Frontend Experiences
| Bias | How It Manifests | Antidote |
|-------|------------------|----------|
| **Shiny framework syndrome** | Rewriting in the newest framework before measuring if the current one is the bottleneck | Framework migrations cost 3-6 months. A new framework must be 2× better, not just newer. |
| **Premature component splitting** | Extracting every UI element into a reusable component before the pattern repeats 3 times | Don't abstract until you see the same pattern in 3 different places. One occurrence is an implementation; two is a coincidence; three is a pattern. |
| **Lighthouse blindness** | Shipping with 100 Lighthouse scores on desktop while mobile users experience 12-second loads | Test on emulated Moto G4 with 4G throttling. Desktop Lighthouse scores are vanity; mobile scores are reality. |

### What Frontend Masters Know That Others Don't
- **Paint cycles are your budget.** Every style change that triggers layout → paint → composite costs 16ms on a 60fps device. Style changes that trigger layout (width, height, top, left) are 10× more expensive than opacity or transform. Use the Performance tab, not guesswork.
- **Accessibility is UX, not compliance.** A screen reader user is a user. Keyboard-only navigation is how power users operate. Semantic HTML is free performance — a `<button>` comes with focus, role, and keyboard handling that takes 50 lines to replicate on a `<div>`.
- **Every refactor must remove dead code — not just reorganize it.** When you refactor a component or module, actively delete unused CSS, dead `import` statements, unreachable code branches, and legacy polyfills. A refactor's diff should be net-negative in lines. Dead imports still execute — they're not free.
- **Bundle size is a product metric.** Every 100KB of JavaScript costs 1 second on a median mobile device. Your imports are a tax your users pay. Tree-shake aggressively. Lazy-load everything below the fold.

### When to Break Your Own Rules
- **Skip SSR for internal dashboards.** Server-side rendering adds complexity. If your users are 50 employees on office WiFi, a client-side SPA is faster to build and perfectly adequate.
- **Use a `<div>` when semantics don't help.** Not every container needs to be `<section>`, `<article>`, or `<aside>`. Semantic HTML matters for landmarks and interactive elements. For purely visual grouping, a `<div>` is fine.

## Operating at Different Levels

The same frontend task produces fundamentally different output depending on the practitioner's level. Invoke this skill with your target level to calibrate depth and scope.

| Level | Frontend Output Characteristics |
|---|---|
| **L1 — Apprentice** | Step-by-step component implementation with explanations. Safe defaults, accessibility basics covered. "Here's the component, here's why we use flexbox here." |
| **L2 — Practitioner** | Production-ready component with all states (loading, empty, error, edge cases), tests, and accessibility. Independent delivery. |
| **L3 — Senior** | Component architecture design with trade-off analysis. State management strategy. Performance and bundle-size optimization. Decision rationale included. |
| **L4 — Staff** | Design system patterns, shared component library standards, SSR/SSG strategy for the org. "This is how all our apps should handle routing/data fetching/state." |
| **L5 — Principal** | Novel frontend patterns or tools adopted across the industry. Framework-level contributions. "Here's a new rendering strategy for this class of interaction." |

**Usage**: Say "as an L3 frontend developer, architect the component tree for..." or "give me an L2 implementation of this form" to calibrate. Default: **L2** (production-ready, independent execution).

## When to Use

<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Choosing between Next.js, Vite React, Remix, Astro, or Nuxt for a new web project
- Implementing React Server Components (RSC) with Client Component boundaries and streaming
- Designing component architecture: compound components, render props vs hooks, Server Component composition
- Selecting and implementing state management: TanStack Query for server state, Zustand for client state, React Hook Form for forms
- Architecting CSS at scale: Tailwind utility-first patterns, CSS Modules, design tokens, responsive strategies
- Optimizing Core Web Vitals: LCP < 2.5s, INP < 200ms, CLS < 0.1 — measured via Real User Monitoring (RUM)
- Implementing WCAG 2.2 AA accessibility: semantic HTML, ARIA, keyboard navigation, focus management, screen reader testing
- Analyzing and optimizing bundle size: dynamic imports, tree shaking verification, code splitting strategies
- Setting up comprehensive testing: Vitest + React Testing Library (components), Playwright (E2E), axe-core (a11y)

## Decision Trees

<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### Rendering Strategy
```
                     ┌──────────────────────────┐
                     │ START: SSR, SSG, or ISR? │
                     └───────────┬──────────────┘
                                 │
              ┌──────────────────▼──────────────────┐
              │ Does content change per user or     │
              │ per request?                        │
              └────┬────────────────────┬───────────┘
                   │ YES                │ NO
                   ▼                    ▼
        ┌──────────────────┐  ┌──────────────────────┐
        │ SSR (dynamic).   │  │ How often does       │
        │ Render on each   │  │ content change?      │
        │ request. Use for │  └──┬───────────────┬───┘
        │ dashboards, auth │     │ < 1/day       │ > 1/day
        │ pages, real-time │     ▼               ▼
        │ data.            │ ┌────────┐    ┌───────────┐
        └──────────────────┘ │ SSG    │    │ ISR       │
                             │ Build  │    │ Revalidate│
                             │ time   │    │ every N   │
                             │ only   │    │ seconds   │
                             └────────┘    └───────────┘
```
**When to choose SSR:** Content is per-user (dashboards, settings) or real-time (live scores, stock prices). SEO is critical and content changes by request.  
**When to choose SSG:** Content changes < once per deploy (blog posts, docs, marketing pages). Maximum cache hit ratio desired. Build time < 5 minutes.

### State Management Selection
```
                     ┌──────────────────────────┐
                     │ START: State type?       │
                     └───────────┬──────────────┘
                                 │
              ┌──────────────────▼──────────────────┐
              │ Does the state come from the        │
              │ server (API/DB)?                    │
              └────┬────────────────────┬───────────┘
                   │ YES                │ NO
                   ▼                    ▼
        ┌──────────────────┐  ┌──────────────────────┐
        │ TanStack Query / │  │ Shared across        │
        │ SWR. Caching,    │  │ unrelated components?│
        │ refetch, mutate. │  └──┬───────────────┬───┘
        └──────────────────┘     │ YES           │ NO
                                 ▼               ▼
                          ┌────────────┐  ┌──────────────┐
                          │ Zustand /  │  │ useState /   │
                          │ Jotai      │  │ useReducer   │
                          │ (global)   │  │ (local)      │
                          └────────────┘  └──────────────┘
```
**When TanStack Query:** Data originates from API. Needs caching, background refetch, optimistic updates. Pagination/infinite scroll required.  
**When Zustand:** Client-only global state (theme, auth status, UI preferences). Cross-component shared state not tied to server. Avoids prop drilling across > 3 levels.

### CSS Architecture
```
                     ┌──────────────────────────┐
                     │ START: CSS approach?     │
                     └───────────┬──────────────┘
                                 │
              ┌──────────────────▼──────────────────┐
              │ Team size > 5 + design system       │
              │ with tokens?                        │
              └────┬────────────────────┬───────────┘
                   │ YES                │ NO
                   ▼                    ▼
        ┌──────────────────┐  ┌──────────────────────┐
        │ Tailwind with    │  │ Solo dev or rapid    │
        │ design tokens in │  │ prototyping?         │
        │ config. Utility- │  └──┬───────────────┬───┘
        │ first, component │     │ YES           │ NO
        │ extraction at    │     ▼               ▼
        │ > 5 repetitions. │ ┌────────┐    ┌───────────┐
        └──────────────────┘ │Tailwind│    │ CSS       │
                             │utility │    │Modules or │
                             │classes │    │styled-    │
                             │        │    │components │
                             └────────┘    └───────────┘
```
**When Tailwind + tokens:** Team with design system. Design tokens (colors, spacing, typography) defined once. Rapid iteration with constraints.  
**When CSS Modules:** Scoped styles per component. No utility-class learning curve. Complex pseudo-selectors or animations that don't map well to utilities.

### Component Testing Strategy
```
                     ┌───────────────────────────┐
                     │ START: How to test this   │
                     │ component?                │
                     └───────────┬───────────────┘
                                 │
              ┌──────────────────▼──────────────────┐
              │ Does component handle user          │
              │ interaction + async data?           │
              └────┬────────────────────┬───────────┘
                   │ YES                │ NO
                   ▼                    ▼
        ┌──────────────────┐  ┌──────────────────────┐
        │ React Testing    │  │ Pure render (no      │
        │ Library + MSW.   │  │ state, no async)?   │
        │ Test: render →   │  └──┬───────────────┬───┘
        │ interact → wait  │     │ YES           │ NO
        │ for async →      │     ▼               ▼
        │ assert UI.       │ ┌────────┐    ┌───────────┐
        └──────────────────┘ │Vitest  │    │ Playwright│
                             │snapshot│    │ E2E for   │
                             │or      │    │ critical  │
                             │render  │    │ user flow │
                             │assert  │    └───────────┘
                             └────────┘
```
**When Testing Library + MSW:** Component fetches data, handles form submission, or manages async state. Need to test loading → success → error states.  
**When snapshot test:** Presentational component with stable output. No dynamic data. Quick regression detector. Avoid for large component trees.

## Core Workflow

<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 0 (~15 min): Framework Selection — Decision Tree

Choosing the wrong framework costs months of migration. Start here:

```
Is SEO critical OR do you need server-side rendering?
├── YES → Is content highly dynamic (per-user, real-time)?
│   ├── YES → Next.js App Router (SSR + Streaming + ISR)
│   │        Best for: dashboards, e-commerce, social feeds, multi-tenant apps
│   │        Tradeoff: server costs, cold start latency on serverless, RSC learning curve
│   ├── NO  → Astro (mostly static, islands of interactivity)
│   │        Best for: marketing sites, documentation, blogs, content sites
│   │        Tradeoff: limited dynamic server capabilities, not for app-like experiences
│   └── MIXED → Next.js App Router with PPR (Partial Prerendering)
│              Static shell + dynamic holes. Best of both worlds; experimental as of Next.js 15.
│
└── NO → Is it a highly interactive SPA (very little static content)?
    ├── YES → Vite + React Router (pure SPA)
    │        Best for: internal tools, admin panels, apps behind auth walls
    │        Tradeoff: no SSR, poor SEO, larger initial JS bundle, "white flash" on load
    │
    └── MIXED → Remix (React Router v7)
               Best for: forms-heavy apps, progressive enhancement philosophy
               Tradeoff: smaller ecosystem than Next.js, less mature RSC support
```


**What good looks like:** Storybook runs with every component rendering in light mode, dark mode, and all interactive states (hover, focus, active, disabled, loading, error). Lighthouse score ≥ 95 across Performance, Accessibility, Best Practices, and SEO. No console errors in production. The bundle ships under 200KB gzipped for initial load, and every page has a measured Core Web Vitals score from lab data before merge.

**Framework comparison — hard numbers:**

| Criterion | Next.js App Router | Remix/React Router v7 | Astro | Vite SPA | Nuxt (Vue) |
|-----------|-------------------|----------------------|-------|----------|------------|
| Initial JS (KB, gzipped) | 85-120 (RSC) | 70-100 | 5-30 (islands) | 150-250 | 70-110 |
| LCP potential (static) | < 1.0s | < 1.0s | < 0.5s | 1.5-3.0s | < 1.0s |
| Build speed (100 pages) | 45-90s | 30-60s | 15-30s | 5-15s | 30-60s |
| Learning curve | Steep (RSC model) | Moderate | Gentle | Gentle |

> See [references/core-workflow.md](references/core-workflow.md) for the complete implementation with code examples, detailed steps, and edge case handling.

## Cross-Skill Coordination

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `api-designer` | OpenAPI 3.1 spec, type-safe SDK, error response formats, pagination conventions | Before building any API-consuming component; ensures contract alignment |
| `ui-ux-designer` | Design system, wireframes, mockups, interaction patterns, responsive breakpoints | Before implementing any UI component; design-to-code handoff |
| `backend-developer` | API implementation, type definitions, validation schemas, auth token patterns | Before integrating with backend APIs; ensures data shapes match |
| `ux-researcher` | User personas, accessibility requirements, behavior flows, usability test results | Before making UX decisions that impact diverse user groups |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `fullstack-developer` | Component APIs, server action signatures, shared type packages, middleware behavior | Fullstack can't wire frontend to backend without component contracts |
| `qa-engineer` | Test IDs (data-testid), critical user paths, edge case states (loading/error/empty), accessibility test cases | QA can't author E2E tests without UI implementation |
| `accessibility-auditor` | WCAG 2.2 AA implementation, semantic HTML, ARIA labels, keyboard navigation, focus management | Auditor can only report issues without source to verify fixes |
| `seo-specialist` | SSR/SSG strategy, meta tags, structured data, hreflang implementation, Core Web Vitals | SEO recommendations can't be implemented without frontend capability |

### Communication Triggers

| Trigger | Notify | Why |
|---|---|---|
| API contract breaking change needed | Backend, Fullstack, Mobile | Coordinate deprecation timeline; version API or migrate consumers |
| Design system token change | UI/UX Designer, Mobile | Consistent visual language across platforms |
| Core Web Vitals regression detected | Observability, Backend (if API latency is cause) | Joint investigation — is it frontend bundle, API response, or rendering? |
| Bundle size spike (>20%) | All developers | Identify cause — unoptimized dependency, duplicate import, missing tree shaking |
| New third-party script/service added | Security Reviewer, Observability | CSP update, performance impact assessment, PII exposure review |

### Escalation Path

```
API contract blocked? → Backend Developer lead → System Architect
Design feasibility dispute? → UI/UX Designer → Product Strategist
Performance SLO breach? → Observability Engineer → DevOps Engineer
Security vulnerability in dependency? → Security Reviewer → Security Engineer
Accessibility compliance gap? → QA Engineer → Compliance Officer
```

## Proactive Triggers

| Trigger | Action | Why |
|---------|--------|-----|
| Lighthouse Performance score drops below 90 on a PR that "just added a new library for date formatting" | Run bundle analyzer (`@next/bundle-analyzer`) on the PR: identify the new dependency's contribution. If >50KB gzipped, find a lighter tree-shakeable alternative or dynamically import. Flag the PR — bundle budgets must be enforced in CI | Unvetted dependencies accumulate silently. One "small utility library" at 80KB gzipped can push your LCP from green to red on mobile 3G. Each dependency is a permanent tax on every user's first load |
| User reports "blank white screen" after navigating between routes — no error visible in console | Check if error boundaries exist at the route AND feature level. If not, wrap every route segment in a React error boundary with a graceful fallback UI. Log the component stack to Sentry/Datadog. Test by intentionally throwing in a child component | A single unhandled error in one widget should never take down the entire page. Error boundaries contain blast radius; without them, any component crash = white screen of death for the whole SPA |
| Design review catches a hardcoded color (`#3B82F6`) in a component — the design system defines this as `primary-500` | Replace all hardcoded values with design tokens from `tailwind.config.ts`. Add a grep-based CI check (or ESLint rule) to reject hex/rgb/rgba values in component files. Run a one-time audit of the entire codebase for hardcoded values | Hardcoded values mean a brand color change requires find-and-replace across 200 files instead of one config edit. Design tokens are the single source of truth — diverging from them guarantees visual inconsistency |
| Bundle analysis reveals `moment.js` (72KB gzipped) in the main chunk — used for a single `format()` call | Replace with `date-fns` (import only the `format` function, ~3KB) or `Intl.DateTimeFormat` (native, zero bytes). Add a CI allowlist/blocklist for known-heavy dependencies. Audit all existing imports for bundle bloat | `moment.js` is a known bundle killer — it imports all locales and is not tree-shakeable. Tree-shakeable alternatives let you pay only for what you use. One moment import can double your route's JS budget |
| TypeScript component props defined as `{ data?: T, isLoading: boolean, error?: Error }` — TypeScript allows `{ isLoading: false, error: null, data: undefined }` | Refactor to a discriminated union: `{ status: 'loading' } \| { status: 'success', data: T } \| { status: 'error', error: E }`. TypeScript's exhaustiveness checking then guarantees every render path handles all states | Impossible states make impossible bugs. A discriminated union guarantees exactly one valid state at compile time. The original type allows the "impossible" state where loading is done, there's no error, but there's also no data — and that's exactly where rendering crashes |
| `useEffect` with `setInterval` but no cleanup function — component mounts/unmounts on each navigation, accumulating duplicate intervals | Add a cleanup function: `useEffect(() => { const id = setInterval(poll, 5000); return () => clearInterval(id); }, [])`. Use a `useRef` to track mounted state. Enable React strict mode in development to double-invoke effects | Every subscription (`setInterval`, `addEventListener`, `WebSocket`) in an effect needs cleanup. Memory leaks in SPAs are invisible until the app crashes after 20+ navigations. Strict mode surfaces missing cleanups in dev |
| Lighthouse Accessibility score drops below 95 — new component uses `<div onClick={handler}>` instead of a native interactive element | Replace with `<button onClick={handler}>` or `<a href={url}>`. Native elements handle keyboard focus, Enter/Space activation, screen reader announcements, and form submission out of the box. Add axe-core to CI with a zero-violation policy | `<div onClick>` is invisible to screen readers and impossible to reach via keyboard alone. Semantic HTML before ARIA — native elements provide behavior that ARIA roles only describe (you'd need 6+ additional handlers to replicate `<button>` behavior) |
| "Why is this product page loading 2.3MB?" — all product images are original-resolution 4000x3000 PNGs served at full size, scaled down via CSS | Implement `next/image` or Nuxt Image with: automatic WebP/AVIF conversion, responsive `sizes` attribute, lazy loading below the fold, and explicit width/height to prevent CLS. Preload the LCP (hero) image with `fetchpriority="high"`. Audit all `<img>` tags | Unoptimized images are the #1 cause of poor LCP scores. A 2MB hero image displayed at 400px wide is 95% wasted bytes. Image optimization tooling is free in modern frameworks — not using it costs real users 2-5 seconds on every page load |

## What Good Looks Like

> Every page loads with a Lighthouse score of 95+, Core Web Vitals all green, and a JavaScript bundle under 150KB gzipped per route.

> See [references/what-good-looks-like.md](references/what-good-looks-like.md) for the full quality standard.


### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | ui-ux-designer | Design system, wireframes, mockups, interaction patterns |
| **This** | frontend-developer | React/Next.js/Vue implementation, state management, performance optimization, a11y compliance |
| **After** | code-reviewer | Reviews component architecture, state management choices, performance, accessibility |

Common chains:
- **Design to code**: ui-ux-designer → frontend-developer → code-reviewer — Designer defines look and feel, frontend builds it, reviewer validates quality
- **API to UI**: api-designer → frontend-developer → qa-engineer — API contract defines data shapes, frontend renders the experience, QA tests the integration

## Deliberate Practice

<!-- DEEP: 10+min — how to improve, not just what to do -->

### The Frontend Improvement Loop
1. **Audit the real user experience** — Open Chrome DevTools → Performance tab → record a critical user flow on a throttled Moto G4. Find the longest task.
2. **Profile the bottleneck** — Is it a large bundle? Expensive re-render? Layout thrashing? Unoptimized image?
3. **Fix one thing** — Target the single biggest regression. Re-audit. Did Core Web Vitals improve?
4. **Repeat every sprint** — Frontend performance is a garden, not a monument. It degrades with every feature.

### Practice Routines
| Skill Level | Practice | Frequency | Expected Result |
|-------------|----------|-----------|-----------------|
| Novice → Competent | Rebuild a UI from Dribbble/UIFry using only HTML/CSS — no JS, no framework. Must work at 320px and 1920px | Weekly | Internalizes layout algorithms, responsive patterns, and CSS capabilities without framework crutches |
| Competent → Expert | Audit a popular website's accessibility: navigate it with keyboard only, then with VoiceOver. Document every failure | Monthly | Develops a11y intuition — can spot focus trap, missing label, color-only indicator from a screenshot |
| Expert → Master | Contribute a bug fix to React, Next.js, or a major component library. Read the source of a framework you use daily | Quarterly | Understands the framework's internals — makes better design decisions because they know what happens under the hood |

### The One Thing
**Rebuild a component you built 6 months ago without looking at the original code.** Compare: is the new version simpler? More accessible? Smaller bundle impact? If it's not better, you haven't grown. If it's worse (over-engineered), you've learned the wrong lessons. Your own code, given 6 months of distance, is the best mirror of your growth.

## Gotchas

- **`useEffect` with empty deps `[]`** runs once on mount. But React 18 Strict Mode in development runs it twice to catch side effects. Your production code must tolerate double invocation.
- **Next.js `getServerSideProps`** serializes everything with `JSON.stringify` internally. `Date` objects become strings, `undefined` becomes absent (not null), and `BigInt` throws. Return only JSON-safe primitives.
- **Tailwind's JIT compiler** scans your source for class strings. Dynamic class construction like `bg-${color}-500` will NOT generate CSS unless you safelist it or use full class names.
- **Core Web Vitals LCP** element changes during page load. The initial hero image may be the LCP candidate at 500ms, but a dynamically injected paragraph at 800ms becomes the new LCP. Measure after full hydration.
- **`localStorage` is synchronous and blocking**. On slow disks, a `localStorage.getItem()` call can block the main thread for 10-50ms. Use `IndexedDB` or memory cache for hot paths.
- **Form autofill by browsers** doesn't fire `onChange` events in all cases. If your validation relies on `onChange`, it will miss autofilled fields. Listen to `onBlur` or use the `onInvalid` capture phase.
- **React `key` prop on list items** must be stable across re-renders. Using `Math.random()` or `index` with sortable lists causes DOM thrashing and lost input focus.


## References

Detailed reference material loaded on demand:

- **Core Workflow — Full Implementation**: See [core-workflow.md](references/core-workflow.md)
- **Anti-Patterns**: See [anti-patterns.md](references/anti-patterns.md)
- **Best Practices**: See [best-practices.md](references/best-practices.md)
- **Calibration — How to Know Your Level**: See [calibration.md](references/calibration.md)
- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Error Decoder**: See [error-decoder.md](references/error-decoder.md)
- **Negative Constraints**: See [negative-constraints.md](references/negative-constraints.md)
- **Scale Depth: Solo → Small → Medium → Enterprise**: See [scale-depth.md](references/scale-depth.md)
- **Sub-Skills**: See [sub-skills.md](references/sub-skills.md)

