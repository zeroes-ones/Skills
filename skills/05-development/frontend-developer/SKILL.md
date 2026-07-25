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

## Anti-Rationalization — No Excuses

| Rationalization | Reality |
|---|---:|
| "I'll add accessibility after we ship — it's just aria-labels, how hard can it be?" | Retrofitting WCAG 2.2 AA onto a finished UI costs 3-5× more than building accessibly from the start. Every `<div onClick>` you ship today is a lawsuit risk and a rebuild tomorrow. Accessibility is not a feature — it's the floor. |
| "It works fine on my MacBook Pro — users have fast internet too." | Your median user is on a 3-year-old Android phone with 4GB RAM on spotty 4G. Desktop Chrome DevTools lie. Your 100 Lighthouse score on desktop means nothing when mobile users get 12-second loads and bounce. |
| "useState + useEffect for data fetching is simpler — TanStack Query is overkill for this." | This pattern causes stale data, race conditions on rapid re-renders, and duplicate network requests. One `useEffect` fetching bug in production costs hours of debugging. Server state belongs in a dedicated cache — every time you skip it, you're writing bugs you'll fix later. |
| "I'll optimize performance after we launch — premature optimization is the root of all evil." | Performance is architecture, not polish. A page with 3-second LCP loses 32% of users before it even renders. You can't bolt Core Web Vitals onto a finished app — you'll be rewriting components, not tweaking CSS. |
| "Security checks on the client are fine — nobody's going to hack our little app." | The client is attacker-controlled territory. Every auth gate, role check, and input sanitizer you put in client-side JS can be deleted with devtools in 3 seconds. Client-side security is a UX convenience, never a boundary. Your "nobody would bother" threshold is wrong — bots scan indiscriminately. |

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

These rules are non-negotiable constraints that detect frontend mistakes before they are given. Violation means STOP and refuse to proceed.

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE `useState` + `useEffect` for server data fetching | Trigger: User proposes or code uses `useState` paired with `useEffect` to fetch, cache, or synchronize server state | STOP. Respond: "This pattern causes stale data, race conditions on rapid re-renders, and unnecessary network requests. Use TanStack Query (React), SWR, or RTK Query — server state belongs in a dedicated cache with automatic invalidation, not in component-local `useState`/`useEffect`." |
| R2 | REFUSE building without design specs, API contract, or browser matrix | Trigger: User requests a component or feature without providing at least one of: design specifications, API response shape, or target browser/device matrix | STOP. Respond: "I need the design specifications, API contract (endpoints and response shapes), or target browser matrix before building. Building without these guarantees rework. Provide what you have — even a rough sketch — and I'll proceed." |
| R3 | DETECT missing WCAG 2.2 AA coverage in generated markup | Trigger: Generated HTML/JSX uses `<div onClick>` for buttons, omits `aria-label` on icon-only controls, lacks focus management in modals/dropdowns, or uses color-only indicators without text alternatives | STOP. Respond: "This component fails WCAG 2.2 AA: [specific violation]. Required: semantic HTML (`<button>` not `<div>`), keyboard reachability (Tab/Enter/Escape), focus trap in modals, `aria-label` on icon-only controls, and 4.5:1 color contrast. Fix these before proceeding — accessibility is not a separate task." |
| R4 | REFUSE performance optimization without measurement | Trigger: User proposes code splitting, virtualization, memoization, or caching optimizations without linking to a Lighthouse CI report or Core Web Vitals measurement (LCP/INP/CLS) showing the failing metric | STOP. Respond: "Optimize from measurements, not intuition. Run Lighthouse CI (target: LCP < 2.5s, INP < 200ms, CLS < 0.1) and identify the specific failing metric. Show me the bottleneck, and I'll address it surgically instead of guessing." |
| R5 | REFUSE shipping without real-device verification plan | Trigger: User asks to finalize or ship UI work citing only Chrome DevTools device emulation as testing evidence | STOP. Respond: "Chrome DevTools device mode is not a real device — it does not replicate touch event behavior, Safari rendering quirks, iOS viewport resizing, or low-memory constraints. Testing must cover: (1) physical low-end Android, (2) physical Safari iOS, (3) keyboard-only navigation, (4) screen reader pass (VoiceOver + NVDA). Confirm your testing plan before we ship." |
| R6 | DETECT security-sensitive logic placed client-side | Trigger: Generated code places authentication gate decisions, authorization role checks, input sanitization as sole defense, or secret keys/tokens in client-side JavaScript | STOP. Respond: "This logic is client-side but must execute server-side: [specific code location]. The client is attacker-controlled territory — any check there is a UX convenience, not a security boundary. Move auth decisions, validation authority, and secrets to the backend." |
| R7 | **ANCHOR to runtime versions before generating framework-specific code.** Never generate React/Next.js/Vue/Nuxt/Svelte API calls from training data alone — your training data may be stale and framework APIs change between major versions. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed framework versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {framework}@{version}. Anchoring all API calls to v{version}. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff. See `scripts/references/source-of-truth-anchoring.md` for the full anti-hallucination pattern." |
| **R8** | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |


- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
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

### Solo Developer
- Next.js or Vite SPA with minimal dependencies — optimize for iteration speed
- Tailwind CSS for styling, shadcn/ui or Radix for accessible component primitives
- TanStack Query for server state, Zustand for ephemeral client state
- Deploy to Vercel/Netlify with preview deployments per branch
- Lighthouse CI in GitHub Actions for perf regression detection
- Manual accessibility audit before each deploy

### Small Team (2-5)
- Shared component library in monorepo (`packages/ui`) with Storybook
- Design tokens as source of truth, consumed by Tailwind config and Figma
- Vitest + React Testing Library + Playwright for E2E, axe-core in CI
- Bundle analysis in CI with budget enforcement; visual regression testing (Chromatic/Percy)
- Real User Monitoring (RUM) with web-vitals.js sending to analytics
- Feature flags for phased rollout; error boundaries with Sentry integration

### Medium Team (5-20)
- Multi-app monorepo with Turborepo/Nx; shared packages for types, UI, config
- Design system with strict API contracts, semantic versioning, and migration guides
- Module federation or micro-frontend architecture for independent team deployment
- Automated accessibility CI gate (axe-core + pa11y) blocking merges on violations
- Performance lab: scheduled Lighthouse runs from multiple geographies and device profiles
- Incident runbooks for frontend-specific failures (CDN issues, JS errors by route)

### Enterprise (20+)
- Platform team maintaining internal framework, design system, and build toolchain
- Server-driven UI for native-like dynamic experiences without app store updates
- SLO-driven frontend reliability: p95 LCP < 2.5s, p95 error rate < 0.1%, tracked per route
- Canary deployments with automatic rollback based on error rate and Core Web Vitals
- Accessibility compliance automation (WCAG 2.2 AA) with legal audit trail
- Federated module ownership: each team owns their route bundle end-to-end

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

## Decision Trees **(QUICK)**

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

## Core Workflow **(STANDARD)**

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


## Best Practices

1. **Co-locate data fetching with the component that needs it.** In Next.js App Router, fetch data in Server Components using `async`/`await` directly — no `useEffect` waterfalls. For Client Components, use TanStack Query with `staleTime` and `gcTime` tuned to your data's freshness profile. Never fetch in a parent and drill through 4 layers of props — it couples unrelated components and causes unnecessary re-renders.

2. **Treat the Server/Client Component boundary as an explicit architectural decision.** Mark the boundary with `'use client'` only at leaf interactive nodes, not at page roots. Server Components handle data fetching and pass serializable props down; Client Components handle interactivity, state, and browser APIs. Pushing the boundary too high loses streaming and code-splitting benefits; pushing it too low forces awkward prop-drilling patterns.

3. **Set a bundle size budget and enforce it in CI.** Baseline: 200KB JS (gzipped) initial, 100KB CSS. Use `@next/bundle-analyzer` or `source-map-explorer` in CI with `lighthouse-ci` assertions. Every PR that increases the budget must either justify the trade-off or optimize. Bundle creep is invisible until your LCP crosses 2.5s and conversions drop.

4. **Use semantic HTML as the foundation of accessibility.** `<button>` for actions, `<nav>` for navigation, `<main>` for primary content — before reaching for ARIA. A single `<div onclick>` where a `<button>` belongs breaks keyboard navigation, screen readers, and form behavior. WCAG 2.2 AA compliance starts with correct element choice, not `role` attributes patching bad markup.

5. **Choose state management by data category, not by habit.** Server state (API responses) → TanStack Query or SWR with cache invalidation. Form state → React Hook Form with Zod validation. Client-only ephemeral state (theme, sidebar open) → Zustand or React Context + `useReducer`. URL state (filters, pagination) → `useSearchParams`. Mixing server state into Redux or Zustand creates cache synchronization bugs and duplicated fetching logic.

6. **Implement error boundaries at every route and major feature section.** A single uncaught exception crashes the entire React tree into a white screen. Wrap each route in an `<ErrorBoundary fallback={...}>` and log boundary errors to your observability platform. Test boundaries by deliberately throwing in lower components — the fallback UI should render, not the Next.js error overlay.

7. **Optimize images as a build-time concern, not runtime.** Use Next.js `<Image>` with explicit `width`/`height` to prevent Cumulative Layout Shift (CLS). Set `sizes` attribute for responsive `srcSet` generation. Convert to WebP/AVIF at build time. Lazy-load below-fold images with `loading="lazy"`. The Largest Contentful Paint (LCP) element must never be lazy-loaded — preload it with `priority`.

8. **Instrument Core Web Vitals in production with Real User Monitoring (RUM).** Lab data (Lighthouse) shows potential; field data (CrUX, web-vitals.js) shows reality. Send LCP, INP, and CLS to your analytics platform grouped by device type, connection speed, and geography. A p75 LCP of 1.5s from a MacBook Pro means nothing if your mobile users on 4G have a p75 of 4.8s.

9. **Use CSS containment and `content-visibility` for long lists.** For lists beyond ~50 items, `content-visibility: auto` tells the browser to skip rendering off-screen items entirely, reducing layout and paint work by 80%+. Combine with `contain: layout style paint` on list item wrappers. Test with Chrome DevTools Rendering panel to verify off-screen items show as "skipped."

10. **Hydration is a performance budget, not a free operation.** Every kilobyte of JS shipped to the client must be parsed, compiled, and executed before the page is interactive. Server Components ship zero JS. Client Components ship their bundle. Interactive islands (Astro) ship only the interactive parts. For every new dependency, ask: "Does this need to be on the client, or can it run at build time or on the server?"


## Error Recovery **(STANDARD)**

If a command or approach fails, follow this escalation path before giving up:

| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|---------------|-------------|
| Tool/command not found | Check installation: `which [tool]` or `[tool] --version`. Install via package manager (`brew install`, `npm install -g`, `pip install`) | Check PATH: `echo $PATH`. Verify the tool binary is in a PATH directory. Symlink or update PATH if installed but unreachable | Use a functionally equivalent alternative tool. If `rg` is unavailable, use `grep -r`. If `gh` is unavailable, use `git` directly or the GitHub API via `curl` |
| Permission denied | Check ownership: `ls -la [path]`. Fix with `chmod` or `sudo` if appropriate. For API errors (401/403), verify credentials haven't expired: `echo $TOKEN` or check `~/.netrc` | Refresh credentials: re-authenticate with the service. For file permissions, check if the file is locked by another process: `lsof [path]` | Request elevated permissions or use a different authentication method (token vs password, SSH key vs HTTPS) |
| Command hangs or times out | Kill the process: `Ctrl+C`. Re-run with a timeout: `timeout 30 [command]` or `gtimeout` on macOS. Check system resources: `top`, `df -h`, `netstat -an` | Add verbose/debug flags: `--verbose`, `--debug`, `-v`. Check logs: `tail -f [logfile]`. Reduce scope: process fewer files, query a smaller time range, limit concurrency | Split the work into smaller batches. Implement a retry loop with exponential backoff (1s, 2s, 4s, 8s). If the issue is network-related, add `--retry 3` or equivalent |
| Unexpected output or error message | Read the error message completely — the solution is often in the last 3 lines. Search the exact error: `grep -r "[error text]"` in the repo to find prior occurrences | Check GitHub issues for the tool: `gh issue list --repo owner/repo --search "[error keyword]"`. Check Stack Overflow | Simplify the approach. If the complex one-liner fails, break it into 3 sequential commands. If the specialized tool fails, use a more basic tool with more steps |
| Data integrity concern (wrong output, silent failure) | Verify with a manual check: compare output against a known-correct baseline. Add assertions: `[command] | grep -q "[expected]" && echo "OK" || echo "FAIL"` | Run the operation on a smaller subset first. Compare checksums: `shasum`, `md5`. Check for silent truncation: `wc -l` before and after | Abort and flag for human review. Do not proceed past data integrity failures — the cost of propagating bad data exceeds the cost of delay |

**Hard failure boundary:** If 3 different approaches all fail, STOP. Do not iterate infinitely. Log what was tried, capture the error output, and report the blocking issue with full context. Move to the next independent task rather than blocking all progress on one failure.

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


## State Log

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.

### How the State Log Works
<!-- AGENT: Read this before starting work, update after each phase -->

1. **On session start:** Check `.copilot/session-state/decision-ledger.json` for any prior decisions relevant to this domain. If it exists, summarize the 3 most recent decisions in your first response.
2. **After each major decision:** Append to the ledger:
   ```json
   {
     "timestamp": "ISO-8601",
     "skill": "frontend-developer",
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

## Production Checklist **(STANDARD)**

Before any production deployment, verify ALL of:

1. `npm run build` — zero build errors, no TypeScript errors, bundle within budget (<200KB JS initial gzipped)
2. `npm test` — all unit + integration tests pass, no snapshot regressions without review
3. `npm run lint` — zero ESLint errors, zero accessibility rule violations (eslint-plugin-jsx-a11y)
4. Lighthouse CI: Performance ≥ 90, Accessibility ≥ 95, Best Practices ≥ 90, SEO ≥ 90
5. Core Web Vitals lab check: LCP < 2.5s, INP < 200ms, CLS < 0.1 — all green
6. Manual keyboard audit: tab through all interactive elements — logical order, visible focus rings, no traps
7. Screen reader test: VoiceOver (macOS) or NVDA (Windows) — all content announced, forms labeled, live regions update
8. Responsive test at 320px, 768px, 1024px, 1440px — no horizontal scroll, no overlapping, text readable
9. Error boundaries tested: inject throw in child component, verify fallback UI renders, error logged
10. Loading states verified: Suspense boundaries render skeletons, not blank screens, during data fetch and lazy load
11. Network throttling: test critical flows at "Slow 3G" — app degrades gracefully, no white screens
12. Memory leak check: navigate routes 50×, `performance.memory.usedJSHeapSize` stable, no upward trend
13. Bundle analysis: `@next/bundle-analyzer` shows no duplicate dependencies, no unintended large imports
14. Environment variables: `NEXT_PUBLIC_` prefix only on intentional client-exposed values — secrets never bundled

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

## Anti-Patterns

### 1. No Bundle Size Budget
**What it looks like:** JavaScript bundles grow incrementally — an extra dependency here, an un-tree-shaken import there — until the homepage loads 2MB of JS. At 3G speeds, that's a 6-second Time to Interactive. Every second beyond 3s drops conversion rates ~2-4%.
**Cost:** $20,000-$100,000/year in lost conversions.
**Fix:** Set a bundle size budget (200KB JS initial, 100KB CSS). Enforce in CI with `bundlesize` or `lighthouse-ci`. Code-split routes and lazy-load below-fold components with `next/dynamic` or `React.lazy`.

### 2. Missing Error Boundaries
**What it looks like:** A single uncaught exception in a React component tree crashes the entire page to a white screen. 10K daily users at 1% crash rate = 100 users/day encountering a dead page.
**Cost:** $10,000-$50,000 in user churn, support tickets, and trust erosion.
**Fix:** Wrap every route and major feature section in an error boundary with a fallback UI. Log boundary errors to your observability platform (Sentry, Datadog RUM). Test by deliberately throwing in child components.

### 3. useEffect Double Invocation in Development
**What it looks like:** `useEffect` with empty deps `[]` runs twice in React 18 Strict Mode during development. Code that isn't idempotent (e.g., incrementing a counter, subscribing without cleanup) produces subtle bugs that only surface in production.
**Fix:** Design effects to be idempotent. Return cleanup functions. Use `AbortController` for fetch cancellation. Don't rely on effect running exactly once.

### 4. JSON Serialization Loss in Next.js Data Fetching
**What it looks like:** `getServerSideProps` and Server Components serialize everything with `JSON.stringify`. `Date` objects become strings, `undefined` becomes absent (not null), and `BigInt` throws. The client receives silently corrupted data.
**Fix:** Return only JSON-safe primitives. Convert dates to ISO strings explicitly. Use `superjson` or `next-superjson-plugin` for preserving types across the serialization boundary.

### 5. Dynamic Tailwind Class Construction
**What it looks like:** `bg-${color}-500` where `color` is dynamic — Tailwind's JIT compiler scans source code for complete class strings. Dynamic construction produces no CSS unless safelisted.
**Fix:** Use full class names: `color === 'red' ? 'bg-red-500' : 'bg-blue-500'`. Or safelist known values. Or use the `style` prop for truly dynamic values.

### 6. LCP Element Shift During Load
**What it looks like:** An initial hero image is the LCP candidate at 500ms, but a dynamically injected paragraph at 800ms becomes the new LCP. The measurement captures the slower element, masking the real user experience.
**Fix:** Measure after full hydration. Preload the LCP image with `<link rel="preload">` or Next.js `priority`. Avoid injecting content above the fold after initial render.

### 7. Synchronous localStorage Blocking Main Thread
**What it looks like:** `localStorage.getItem()` is synchronous and blocks the main thread. On slow disks, a single call takes 10-50ms. Multiple calls during initial render compound into visible jank.
**Fix:** Use `IndexedDB` (async) for large or frequent reads. Keep a memory cache for hot paths. Use `localStorage` only for small, infrequent reads during non-critical paths.

### 8. Form Autofill Bypasses onChange Validation
**What it looks like:** Browsers autofill form fields but don't fire `onChange` events consistently. Validation that relies solely on `onChange` misses autofilled fields, showing "required field" errors on pre-filled forms.
**Fix:** Listen to `onBlur` in addition to `onChange`. Use the `onInvalid` capture phase for native validation. Run validation on submit as the final gate. React Hook Form handles this correctly by default with `mode: 'onBlur'`.

### 9. Unstable React Keys Causing DOM Thrashing
**What it looks like:** `key={Math.random()}` or `key={index}` on sortable/filterable lists. React unmounts and remounts components unnecessarily, losing input focus, scroll position, and CSS transition state.
**Fix:** Use stable, unique identifiers from your data (database IDs, UUIDs). `crypto.randomUUID()` at data creation time, not at render time. Index is acceptable only for static, never-reordered lists.

### 10. No Offline or Slow-Network State Handling
**What it looks like:** App assumes always-on connectivity. Infinite spinners, silent crashes, and lost form data on flaky connections. Users in emerging markets abandon the app.
**Cost:** $15,000-$50,000/year in churn from mobile users on unreliable connections.
**Fix:** Implement optimistic UI updates with rollback on mutation failure. Queue offline mutations with service workers or IndexedDB. Display explicit offline indicators. Test every flow at "Slow 3G" and "Offline" in Chrome DevTools.

### 11. Memory Leaks from Uncleaned Subscriptions
**What it looks like:** Components subscribe to WebSockets, stores, or `resize` events on mount but never clean up. After 30-40 route navigations, the tab consumes 2GB+ and crashes. Mobile users crash within minutes.
**Cost:** $10,000-$40,000 in churn, negative reviews, and emergency debugging sprints.
**Fix:** Always return cleanup functions from `useEffect`. Use React DevTools Profiler to find mounted-but-never-unmounted instances. Monitor `performance.memory.usedJSHeapSize` in e2e tests. Wrap async operations in `AbortController`.

### 12. CSS-in-JS Runtime Overhead on Animations
**What it looks like:** styled-components or Emotion with dynamic props on components re-rendering at 60fps. Runtime computes and injects `<style>` tags every frame, triggering style recalculation and dropping below 30fps.
**Cost:** $5,000-$25,000 in performance sprints, reduced engagement, and eventual migration to zero-runtime CSS.
**Fix:** Use zero-runtime CSS (Tailwind, vanilla-extract, CSS Modules) for animation-heavy components. Reserve runtime CSS-in-JS for static styles. Profile with React DevTools "Highlight updates."

## Error Decoder — War Stories from the Trenches

**(STANDARD)**

When frontend apps go wrong, they go wrong in predictable ways. Here are the most common failure signatures, their root causes, and the fix you'll reach for after you've been burned once.

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| React component re-renders infinitely — browser tab freezes within seconds | `useEffect` dependency array includes an object/array created inline on every render. Reference identity changes every render cycle: `useEffect(() => {...}, [{ id: 1 }])` — each render creates a new object literal | Use primitive values in dependency arrays: `useEffect(() => {...}, [obj.id, obj.name])` not `useEffect(() => {...}, [obj])`. Wrap stable objects in `useMemo`. Use `useRef` for values that shouldn't trigger re-renders | Objects in dependency arrays are compared by reference, not value. Every render creates a new reference → infinite loop. This is the #1 performance bug in every React codebase |
| `useEffect` captures stale state — callback references a variable that was current 3 renders ago | Closure captures the value at the time `useEffect` was scheduled, not when it executes. If the effect depends on state that changes between schedule and execution, it operates on phantom data | Use the functional updater form: `setCount(prev => prev + 1)` instead of `setCount(count + 1)`. Use `useRef` for mutable values that effects need to read without depending on. Add exhaustive-deps lint rule | Closures capture values by reference for objects, by value for primitives. `useEffect` closures are frozen at creation time — the stale closure problem is a fundamental consequence of how JavaScript closures work |
| Server-rendered HTML doesn't match client render — React throws hydration mismatch error, page flashes and re-renders | Server renders different output than client. Common causes: `Date.now()` returns different values, `typeof window !== 'undefined'` branches differently, or data fetched during SSR differs from client-side data | Guard all browser-only code with `useEffect` (which only runs on client). Use `suppressHydrationWarning` only for intentional mismatches like timestamps. Fetch data via `getServerSideProps` and pass as props — don't fetch again on client | Hydration is a reconciliation, not a replacement. React expects the DOM to be identical. Any mismatch forces a full client re-render that defeats the purpose of SSR |
| Bundle contains entire library — importing `lodash` adds 72KB, but only `_.get` is used. Lighthouse flags excessive JavaScript | Default imports pull in the entire module. `import _ from 'lodash'` imports all 300+ functions. Tree-shaking can't eliminate because CommonJS modules have side effects | Use named imports: `import get from 'lodash/get'`. Configure `moduleResolution: 'bundler'` in tsconfig. Use `bundle-analyzer` to visualize what's in your bundle. Set bundle size budgets in CI | Tree-shaking is not magic — it can only eliminate dead code in ES modules without side effects. One default import from a CommonJS package adds 72KB to every page load |
| CSS specificity war — adding `!important` to fix one style breaks three other components. Nobody can predict which style wins | Component styles compete in a global namespace. A deeply nested selector in one component overrides a simple class in another. `!important` escalates the war — the next developer needs `!important` to override your `!important` | Use CSS Modules (`*.module.css`) or CSS-in-JS for component-scoped styles. Use design tokens for shared values. Never use `!important` except to override third-party styles. Set `selector-max-specificity` lint rule to `"0,4,0"` | Global CSS is shared mutable state. Every style rule you write can be overridden by any other file in the codebase. Component-scoped styles eliminate the specificity arms race |
| Async `useEffect` sets state after component unmounts — `Warning: Can't perform a React state update on an unmounted component` | `useEffect` fires an async fetch, user navigates away before it resolves, `setData()` is called on an unmounted component. Memory leak: the promise holds a reference to the component's closure | Use `AbortController`: `const controller = new AbortController(); fetch(url, { signal: controller.signal }); return () => controller.abort()`. Or use a `mounted` ref: `if (!isMountedRef.current) return` before `setData()`. Prefer React Query/TanStack Query which handles this automatically | Every async operation in a component is a potential memory leak. The component lifecycle and the promise lifecycle are independent — navigation can destroy the component while the promise is still in-flight |

## Verification

- [ ] Run `npm run build` — zero build errors, bundle size within budget (< 20% increase)
- [ ] Run `npm test` — all tests pass, no snapshot regressions without review
- [ ] Run `npm run lint` — zero ESLint errors, zero TypeScript errors
- [ ] Run Lighthouse: Performance > 90, Accessibility > 95, Best Practices > 90
- [ ] Manual: tab through every interactive element — focus order is logical, focus rings visible
- [ ] Manual: test at 320px, 768px, 1024px, and 1440px widths — no horizontal scroll, no overlapping content

## Verification Guardrails

Before delivering work, the agent must verify:

- [ ] **Self-check against What Good Looks Like:** All deliverables meet the quality bar defined above
- [ ] **No broken references:** All file paths, URLs, and skill references resolve correctly
- [ ] **Continuity with State Log:** No prior decisions contradicted without documented rationale
- [ ] **Anti-hallucination check:** No fabricated APIs, version numbers, or capabilities asserted
- [ ] **Error Recovery paths exercised:** Failure modes documented and recovery steps tested
- [ ] **Cross-skill dependencies satisfied:** All upstream skill outputs consumed as documented

If any checkbox fails, revise before delivering. When all pass, add to the state log.

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

