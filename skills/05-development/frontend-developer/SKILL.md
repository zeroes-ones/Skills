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
| Learning curve | Steep (RSC model) | Moderate | Gentle | Gentle | Moderate |
| Ecosystem maturity | Very high | High | Growing | High | High |
| Deployment complexity | Medium | Medium | Low | Low | Medium |

**When to pick Vue/Nuxt over React/Next.js:**
- Team has Vue experience and no React experience — framework familiarity beats framework hype
- Preference for convention over configuration (Nuxt auto-imports components, composables, and utilities)
- Simpler reactivity model: Vue's `ref()`/`reactive()` is more intuitive than React's immutable state + useEffect dance
- Single-file components (.vue) with scoped styles are preferred over JSX + separate CSS files

### Phase 1 (~15 min): Project Architecture & TypeScript Mastery

**Next.js App Router — the definitive project structure:**
```
src/
  app/
    (marketing)/          # Route group — no impact on URL
      page.tsx            # Server Component by default
      layout.tsx          # Shared layout for marketing routes
    (dashboard)/
      layout.tsx          # Auth-protected layout
      dashboard/
        page.tsx
        @analytics/       # Parallel route — renders alongside page
          page.tsx
    api/                  # Route handlers (API endpoints)
  components/
    ui/                   # Design system primitives: Button, Input, Card, Modal
    features/             # Feature-specific composed components
      checkout/
        CartSummary.tsx
        PaymentForm.tsx
    layout/               # Header, Footer, Sidebar, Navigation
  hooks/                  # Shared custom hooks
  lib/                    # Utilities, API client, type helpers
    db.ts                 # Database client (server-only)
    auth.ts               # Auth configuration
  types/                  # Shared TypeScript types
```

**Component classification — Server vs Client:**
| Component type | Where it runs | File marker | Capabilities | Restrictions |
|---------------|---------------|-------------|-------------|--------------|
| Server Component | Server only | No `'use client'` | async/await, DB queries, filesystem, secrets | No hooks, no event handlers, no browser APIs, no state |
| Client Component | Server (SSR) + Browser (hydrate) | `'use client'` | Hooks, state, effects, event handlers, browser APIs | Cannot import server-only modules directly |
| Shared Component | Depends on importer | Neither (re-exportable) | Renders children, passes props | Must work in both environments |

**Server Component composition rule — "Server is the shell, Client is the interactivity":**
```
ServerComponent (fetches data, renders layout)
  ├── ClientHeader ('use client' — has onClick, useState)
  │   └── ServerIcon (rendered as child prop — can be server component!)
  ├── StaticContent (server — just markup, no interactivity)
  └── ClientSearch ('use client' — input, state, debounce)
```
Key insight: Server Components can render Client Components as children. Client Components can accept Server Components as `children` props. This is how you compose them — the boundary is at the import, not the render tree.

**TypeScript patterns that prevent production bugs:**

```typescript
// 1. Discriminated unions for API states — impossible to access data in error state
type AsyncState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error };

// 2. Branded types — prevent mixing up IDs of different entities
type UserID = string & { readonly __brand: 'UserID' };
type OrderID = string & { readonly __brand: 'OrderID' };
function getUser(id: UserID) { /* ... */ }
getUser("123" as UserID); // OK
getUser("123");           // Type error — plain string not assignable to UserID

// 3. satisfies operator — validate shape without widening type
const config = {
  apiUrl: process.env.API_URL!,   // Type: string
  timeout: 3000,                   // Type: number
} satisfies Record<string, string | number>;
config.timeout.toFixed(2);        // OK — TypeScript knows it's number

// 4. Template literal types for route safety
type Route = `/app/${'dashboard' | 'settings' | 'profile'}/${string}`;
function navigate(route: Route) { /* ... */ }
navigate('/app/dashboard/analytics'); // OK
navigate('/app/unknown/page');        // Type error

// 5. const assertions for exhaustiveness
const STATUS = ['active', 'inactive', 'suspended'] as const;
type Status = typeof STATUS[number]; // 'active' | 'inactive' | 'suspended'
// Switch on Status — TypeScript ensures all cases handled
```

### Phase 2 (~30 min): State Management Taxonomy

The #1 mistake in React apps: treating all state the same. Different state categories need different tools.

```
State Category        Tool                          Persistence          Example
─────────────────────────────────────────────────────────────────────────────────
Server state          TanStack Query (v5)           Cache (stale TTL)    Products list, user profile, search results
Client global state   Zustand                       Session/localStorage Cart, theme, auth status (derived)
Form state            React Hook Form + Zod         Ephemeral            Login form, checkout flow, filters
URL state             useSearchParams + nuqs        URL (shareable)      Page number, sort order, search query
UI ephemeral          useState/useReducer           None (lost on nav)   Dropdown open, tooltip visible, hover
Navigation state      Next.js router                URL + history        Current route, params
```

**Server state with TanStack Query — the only correct pattern:**
```typescript
// NEVER: useEffect + useState for API calls
// ALWAYS: TanStack Query with staleTime and gcTime tuned per endpoint

const { data, isLoading, error } = useQuery({
  queryKey: ['products', { category, page }],  // Automatically refetches when deps change
  queryFn: () => fetchProducts({ category, page }),
  staleTime: 5 * 60 * 1000,  // 5min — data considered fresh, no refetch
  gcTime: 30 * 60 * 1000,    // 30min — keep in cache after unmount (garbage collection)
  placeholderData: keepPreviousData,  // Show previous page's data while loading next page
});

// Mutation with optimistic update — UI feels instant
const mutation = useMutation({
  mutationFn: updateTodo,
  onMutate: async (newTodo) => {
    await queryClient.cancelQueries({ queryKey: ['todos'] });
    const previous = queryClient.getQueryData(['todos']);
    queryClient.setQueryData(['todos'], (old) => /* optimistically update */);
    return { previous };  // Rollback context
  },
  onError: (err, newTodo, context) => {
    queryClient.setQueryData(['todos'], context.previous);  // Rollback on failure
    toast.error('Failed to update');
  },
  onSettled: () => queryClient.invalidateQueries({ queryKey: ['todos'] }),
});
```

**Client state with Zustand — when Context is not enough:**
Zustand over Context when: (a) state changes frequently (Context triggers re-renders of ALL consumers on every change), (b) state is complex with nested updates, (c) you need middleware (persist, devtools, immer).

```typescript
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface CartStore {
  items: CartItem[];
  addItem: (item: CartItem) => void;
  removeItem: (id: string) => void;
  total: () => number;  // Derived — computed, not stored
}

const useCart = create<CartStore>()(
  persist(
    (set, get) => ({
      items: [],
      addItem: (item) => set((s) => ({ items: [...s.items, item] })),
      removeItem: (id) => set((s) => ({ items: s.items.filter((i) => i.id !== id) })),
      total: () => get().items.reduce((sum, i) => sum + i.price * i.qty, 0),
    }),
    { name: 'cart-storage' }  // Persists to localStorage automatically
  )
);
```

**URL as state — the most underused pattern:**
For any state that should survive a page refresh or be shareable (filters, sort, search, pagination), use URL search params, not React state. Use `nuqs` (type-safe, Next.js-native URL state management):

```typescript
import { useQueryState } from 'nuqs';

// Instead of: const [page, setPage] = useState(1)
const [page, setPage] = useQueryState('page', { defaultValue: '1' });
// URL becomes: /products?page=3 — shareable, bookmarkable, SSR-compatible
```

### Phase 3 (~20 min): CSS Architecture at Scale
<!-- DEEP: 10+min -->

**The definitive CSS strategy for 2026:**

```
Approach           Use case                         Avoid when
────────────────────────────────────────────────────────────────────
Tailwind CSS       Application UI, design systems   Teams unfamiliar with utility-first (learning curve is real)
CSS Modules        Component-scoped styles           Need for shared design tokens (duplication risk)
Vanilla Extract    Type-safe CSS, design tokens      Build speed matters (adds compile step)
CSS-in-JS (runtime) NOT RECOMMENDED                  Runtime performance cost, SSR complexity, bundle bloat
```

**Tailwind CSS at scale — the patterns that work beyond 10,000 lines:**
1. **Design tokens in Tailwind config** — never hardcode colors/spacing in className:
   ```typescript
   // tailwind.config.ts
   theme: {
     extend: {
       colors: {
         brand: { 50: '...', 500: '...', 900: '...' },  // Generated from a single brand color
       },
       spacing: { 'page': '1.5rem', 'section': '3rem' },
     }
   }
   // In components: className="text-brand-500 p-page" — NOT className="text-[#3B82F6] p-6"
   ```
2. **Component extraction boundary**: Extract to a component when the same set of 3+ utility classes repeats across files. Do NOT create `@apply` abstractions for every repeated class — that defeats Tailwind's purpose.
3. **Responsive breakpoint strategy**: `sm: 640px` (tablet portrait), `md: 768px` (tablet landscape), `lg: 1024px` (desktop), `xl: 1280px` (wide). Mobile-first: base styles = mobile; override upward. Never desktop-first.
4. **Dark Mode**: Use `class` strategy (not `media`). Toggle `.dark` on `<html>`. Every color uses `dark:` variant. Semantic color naming helps here — `bg-surface dark:bg-surface-dark` is better than `bg-white dark:bg-gray-900`.

**CSS Modules — when Tailwind doesn't fit:**
Use CSS Modules for: complex animations that Tailwind can't express, component libraries distributed as npm packages (avoid forcing Tailwind on consumers), legacy codebases already on CSS Modules.

### Phase 4 (~15 min): Core Web Vitals — The Definitive Optimization Guide

**The three metrics that Google cares about — and that users feel:**

| Metric | Target | Measures | User impact |
|--------|--------|----------|-------------|
| LCP (Largest Contentful Paint) | < 2.5s (75th pctl) | When the largest content element becomes visible | "Is this page loading?" Perceived speed |
| INP (Interaction to Next Paint) | < 200ms (75th pctl) | Responsiveness to taps, clicks, key presses | "Is this page frozen?" Responsiveness |
| CLS (Cumulative Layout Shift) | < 0.1 (75th pctl) | Unexpected layout shifts during page load | "Why did that button move?" Visual stability |

**LCP optimization — attack in priority order:**

1. **Preload the LCP image** (usually the hero image). Add `<link rel="preload" as="image" href="hero.webp" fetchpriority="high">` in `<head>`. This tells the browser "load this NOW, not when the parser discovers it."
2. **Inline critical CSS for above-the-fold content.** Extract styles needed for the first viewport and inline them in `<style>` tags. Next.js can't do this natively — use `critters` or `critical` packages in post-processing. Target: < 14KB of inlined CSS (one TCP round trip).
3. **Font optimization**: Use `next/font` with `display: 'swap'` and `subset`. Self-host fonts — Google Fonts CDN adds 200-400ms DNS + connection + download. `next/font` downloads at build time and serves from your domain.
4. **Avoid lazy-loading the LCP image**. `loading="lazy"` on the hero image delays LCP by forcing the browser to finish layout before starting the image download. Use `fetchpriority="high"` instead.
5. **Minimize render-blocking JavaScript.** Any `<script>` without `async`/`defer` blocks HTML parsing and delays LCP. Use `next/script` with `strategy="lazyOnload"` for third-party scripts.

**INP optimization — the hardest metric to fix:**

INP measures the worst interaction delay on your page. Poor INP means users experience "jank" when clicking, typing, or scrolling.

1. **Break long tasks.** Any task > 50ms is a "long task" that blocks the main thread. Yield to the browser:
   ```typescript
   // Bad: synchronous processing of large array blocks main thread for 200ms
   items.forEach(processItem);

   // Good: yield every 50ms
   async function processInChunks(items: Item[]) {
     for (let i = 0; i < items.length; i++) {
       processItem(items[i]);
       if (i % 20 === 0) await scheduler.yield();  // Yield every 20 items (~50ms)
     }
   }
   ```
2. **Debounce input handlers.** Every keystroke firing a state update + re-render = jank. Debounce 150-300ms for search inputs; throttle 16ms (one frame) for scroll/resize handlers.
3. **Web Workers for heavy computation.** Move JSON parsing, data transformation, and search indexing off the main thread.
4. **Code splitting by interaction.** Load heavy libraries only when the user interacts with the feature that needs them — not on initial load.

**CLS prevention — the five causes and fixes:**

| Cause | Fix |
|-------|-----|
| Images without dimensions | Always set `width` and `height` on `<img>`. Next.js Image does this automatically. |
| Dynamically injected content | Reserve space with `min-height` or skeleton loader matching final content size. |
| Web fonts causing FOUT/FOIT | `font-display: swap` + `size-adjust` in `@font-face` to match fallback font metrics. |
| Ads/embeds without reserved space | Wrap in container with fixed aspect ratio. |
| Animations using top/left | Use `transform: translate()` — it doesn't trigger layout (only compositing). |

For the complete CWV optimization playbook, see `references/performance-cwv.md`.

### Phase 5 (~25 min): Accessibility — WCAG 2.2 AA Compliance

Accessibility is not optional. It's a legal requirement in most jurisdictions (ADA, Section 508, EAA) and affects 15-20% of users.

**The 80/20 rule of accessibility — these five practices catch 80% of issues:**

1. **Semantic HTML is your first and best tool.** `<button>` not `<div onclick>`. `<nav>` for navigation. `<main>` for primary content. `<form>` for forms. Browsers give you keyboard handling, focus management, and ARIA roles for free with semantic elements.
2. **Heading hierarchy without gaps.** h1 → h2 → h3, never h1 → h3 (skip). Screen reader users navigate by headings. Each page has exactly one h1. Headings form a table of contents — make it logical.
3. **Every interactive element is keyboard-reachable.** Tab to it, Enter/Space to activate, Escape to dismiss. Custom components (dropdowns, modals, tabs) must implement full keyboard interaction patterns from the WAI-ARIA Authoring Practices.
4. **Focus management on SPA navigation.** When a route changes, move focus to the new page's h1 or a skip-link target. Without this, screen reader users are "stuck" at the top of the page after navigation. Use `router.events` or Next.js `useRouter` to trigger `ref.current?.focus()`.
5. **Color contrast ≥ 4.5:1 for normal text, ≥ 3:1 for large text (≥18pt bold or ≥24pt regular).** Never convey information through color alone — add icons, text labels, or patterns. Test with a color blindness simulator.

**ARIA rules — "No ARIA is better than bad ARIA":**
```html
<!-- BAD: div impersonating a button, incomplete ARIA -->
<div role="button" onclick="...">Submit</div>

<!-- GOOD: just use a button -->
<button type="button" onclick="...">Submit</button>

<!-- GOOD: when HTML falls short, ARIA done right -->
<button aria-expanded="false" aria-controls="menu-panel" aria-haspopup="true">
  Menu
</button>
<div id="menu-panel" role="menu" hidden>
  <button role="menuitem">Option 1</button>
</div>
```

**Testing accessibility — tools and methodology:**
- Automated: `axe-core` via `@axe-core/react` (Catches 30-40% of issues — color contrast, missing labels, invalid ARIA)
- Manual keyboard test: Tab through every page. Can you reach everything? Is focus visible? Does Escape close modals?
- Screen reader: Test with VoiceOver (macOS/iOS) or NVDA (Windows). Can you navigate by heading? Are live regions announcing dynamic updates?
- CI integration: Run axe-core in Playwright E2E tests. Fail the build on violations above "minor" severity.

### Phase 6 (~25 min): Bundle Optimization

**Bundle size budget — hard limits:**
| Metric | Target | Red flag |
|--------|--------|----------|
| Initial JS per route (gzipped) | < 150KB | > 300KB |
| Total JS for full app (gzipped) | < 500KB | > 1MB |
| CSS per route (gzipped) | < 20KB | > 50KB |
| Lighthouse Performance score | ≥ 90 | < 70 |

**Code splitting patterns:**
1. **Route-based** (automatic in Next.js App Router): Each `page.tsx` is a split point. No additional work needed.
2. **Component-based**: `next/dynamic(() => import('./HeavyChart'), { loading: () => <Skeleton /> })`. Use for: heavy chart libraries (D3, ECharts), rich text editors (TipTap, Quill), video players, code editors (Monaco).
3. **Conditional**: Load only when a feature flag is true or user has a specific role. `{isAdmin && <AdminPanel />}` where AdminPanel is dynamically imported.
4. **Interaction-based**: Load on hover/focus and render on click. The `next/dynamic` `ssr: false` option prevents SSR of browser-only components.

**Tree shaking verification:**
Tree shaking is NOT automatic — it's fragile. ESM imports are tree-shakeable; CommonJS `require()` is not. Verify with `@next/bundle-analyzer`:
```bash
ANALYZE=true next build  # Opens bundle visualization
```
Look for: duplicated modules (same library in multiple chunks), large unused exports, moment.js locale bloat (use `date-fns` instead — 70% smaller and tree-shakeable).

For complete bundle optimization guide, see `references/bundle-optimization.md`.

### Phase 7 (~25 min): Error Handling & Resilience

**Error boundary strategy — layers of defense:**
```
Root Layout
  └── GlobalErrorBoundary     ← Catches everything; shows "Something went wrong" with retry
       ├── Route Segment
       │   └── error.tsx       ← Route-level; shows context-specific error UI
       │        └── Feature
       │            └── ErrorBoundary  ← Feature-level; graceful degradation
       │                 └── Component tree
       └── Suspense Boundary  ← Shows fallback during async rendering
```

```typescript
// Route-level error (Next.js App Router) — error.tsx
'use client';
export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error(error);  // Log to monitoring service
  }, [error]);

  return (
    <div role="alert">
      <h2>Something went wrong</h2>
      <button onClick={reset}>Try again</button>
    </div>
  );
}

// Component-level error boundary for critical sections
class FeatureErrorBoundary extends React.Component<Props, { hasError: boolean }> {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    captureException(error, { extra: { componentStack: info.componentStack } });
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback;  // Degraded but functional UI
    }
    return this.props.children;
  }
}
```

**Security headers that prevent XSS, clickjacking, and data injection:**
```
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
```

In Next.js, configure via `next.config.ts`:
```typescript
const cspHeader = `
  default-src 'self';
  script-src 'self' 'unsafe-eval' 'unsafe-inline';
  style-src 'self' 'unsafe-inline';
  img-src 'self' blob: data: https:;
  font-src 'self';
  connect-src 'self' https://*.sentry.io;
`.replace(/\n/g, '');

const nextConfig: NextConfig = {
  headers: async () => [{
    source: '/(.*)',
    headers: [{ key: 'Content-Security-Policy', value: cspHeader }],
  }],
};
```

### Phase 8 (~30 min): Testing Strategy

```
        /\
       /E2E\      10% — Critical user journeys (signup, checkout, core workflow)
      /------\
     /  Inte- \    25% — Feature integration, API mocking, complex user flows
    / gration  \
   /------------\
  /  Component   \ 35% — Rendering, user interactions, accessibility states
 /----------------\
/      Unit        \ 30% — Pure functions, utilities, hooks, type guards
/------------------\
```

**Component testing with React Testing Library — test behavior, not implementation:**
```typescript
// BAD: Testing implementation details
test('sets loading state', () => {
  const { result } = renderHook(() => useProducts());
  act(() => result.current.fetch());
  expect(result.current.isLoading).toBe(true);  // Implementation detail
});

// GOOD: Testing user-visible behavior
test('shows loading skeleton while fetching', async () => {
  server.use(http.get('/api/products', () => HttpResponse.json([], { status: 200 })));
  render(<ProductList />);
  expect(screen.getByRole('status')).toBeInTheDocument();  // Skeleton has role="status"
  await waitForElementToBeRemoved(() => screen.queryByRole('status'));
});
```

**E2E with Playwright — test the critical path, not every edge case:**
- Test: signup → onboarding → core action → logout (complete user lifecycle)
- Test: mobile viewport, keyboard-only navigation, screen reader path (axe-core integration)
- Anti-pattern: Don't test every form validation case in E2E — that's what component tests are for. E2E tests are slow and flaky; reserve them for revenue-critical paths.
- Use `page.route()` to mock API responses when testing error states (network failure, server error) — don't depend on real server errors.

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

## Scale Depth: Solo → Small → Medium → Enterprise

### Solo (1 person, 0-100 users)
- **What changes**: Frontend = Vite + React (or Next.js if SEO matters). No TypeScript (JS with JSDoc). CSS via Tailwind. State = React state + URL params. Deploy to Vercel/Netlify. No testing beyond manual. No CI. Lighthouse audit manually before launch.
- **What to skip**: TypeScript. Testing. CI/CD. Design system. State management libraries. SSR/SSG strategies. Bundle analysis. Core Web Vitals optimization (beyond basic).
- **Coordination**: You own frontend + backend. Build fast.

### Small Team (2-10 people, 100-10K users)
- **What changes**: TypeScript with strict mode. Component tests (Vitest + RTL). ESLint + Prettier. CI with lint + type-check + test. Lighthouse in CI (≥80). Image optimization (next/image or manual). Basic error boundaries. Semantic HTML. CSS via Tailwind with design tokens. Simple state management (TanStack Query + Zustand).
- **What to skip**: E2E tests (Playwright). Visual regression testing. Full design system. Performance budgets in CI. Bundle analysis. Server Components patterns (keep it simple).
- **Coordination**: PR review with another frontend dev. Design review with designer before implementation. API contract sync with backend.

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: Next.js App Router or Remix. E2E tests (Playwright) on critical flows. Lighthouse CI with performance budgets (≥90). Core Web Vitals monitoring (RUM). Bundle analysis in CI. Component library (Storybook). CSS architecture with CSS Modules or Tailwind. axe-core in CI with zero violations. Full error boundaries with logging (Sentry).
- **What to skip**: Micro-frontends. Advanced SSR patterns (streaming, partial hydration). Custom design system from scratch (use Radix/shadcn).
- **Coordination**: Weekly frontend guild. UI review with design team before release. Cross-team component sharing review.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Design system team with dedicated engineers. Micro-frontend architecture (if multi-team). Advanced SSR (streaming, ISR, PPR). Full RUM with Core Web Vitals analytics. Visual regression testing (Chromatic/Percy). A/B testing infrastructure. Feature flags. Internationalization (i18n with RTL). Accessibility program with audits. Performance budgets enforced in CI. Bundle size governance.
- **What's full production**: Frontend platform team. Design system as a product. Frontend observability (web vitals + errors + user behavior). Canary deployments with A/B. Multi-brand theming.
- **Coordination**: Frontend platform team weekly. Design system council monthly. Cross-team UI review. Quarterly accessibility audit.

### Transition Triggers
- **Solo → Small**: Second frontend developer. UI inconsistency across pages becomes visible.
- **Small → Medium**: 3+ frontend developers. Performance or accessibility becomes a user-reported issue. >10K users.
- **Medium → Enterprise**: 5+ frontend teams. Multi-brand or international. >100K users.

## What Good Looks Like

> Every page loads with a Lighthouse score of 95+, Core Web Vitals all green, and a JavaScript bundle under 150KB gzipped per route. The UI is fully keyboard-navigable, screen-reader-friendly, and WCAG 2.2 AA compliant. Components render correctly across loading, empty, error, and edge-case states — users never see a blank screen or an unhandled spinner. State lives where it belongs: server state in TanStack Query, URL state in search params, and form state in React Hook Form. Design tokens are the single source of truth — no hardcoded colors, no magic spacing values. Every interaction feels instant, deliberate, and polished from first paint to final interaction.

### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | ui-ux-designer | Design system, wireframes, mockups, interaction patterns |
| **This** | frontend-developer | React/Next.js/Vue implementation, state management, performance optimization, a11y compliance |
| **After** | code-reviewer | Reviews component architecture, state management choices, performance, accessibility |

Common chains:
- **Design to code**: ui-ux-designer → frontend-developer → code-reviewer — Designer defines look and feel, frontend builds it, reviewer validates quality
- **API to UI**: api-designer → frontend-developer → qa-engineer — API contract defines data shapes, frontend renders the experience, QA tests the integration

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->
| Sub-Skill | When to Use | Context |
|-----------|-------------|---------|
| `react-server-components` | Next.js App Router with RSC, streaming, and Suspense boundaries | Server Component patterns, Client Component boundaries, `use client` vs `use server` |
| `state-management` | Choosing between TanStack Query, Zustand, URL state, or React Hook Form | Server-state/Client-state/Form-state/URL-state taxonomy with selection criteria |
| `core-web-vitals` | LCP > 2.5s, INP > 200ms, CLS > 0.1 — or optimizing proactively | LCP (hero image preload, critical CSS inline), INP (long task breaking, input debouncing), CLS (dimensions, font loading) |
| `accessibility-audit` | WCAG 2.2 AA compliance: semantic HTML, keyboard, screen reader, focus | axe-core CI, manual VoiceOver/NVDA testing, focus management on SPA navigation |
| `bundle-optimization` | Bundle > 150KB gzipped initial JS per route | Dynamic imports, `next/dynamic`, tree shaking verification, Bundle Analyzer, code splitting |
| `css-architecture` | Scaling Tailwind beyond utility classes, design token integration | `tailwind.config.ts` tokens, component extraction rules, responsive strategy, dark mode |
| `component-testing` | Vitest + React Testing Library strategy, MSW for API mocking | Render → interact → assert pattern, loading/error/empty state coverage, accessibility assertions |
| `framework-migration` | Migrating from Pages Router → App Router, CRA → Vite, or Vue 2 → Vue 3 | Migration strategy, codemods, parallel-running strategy, incremental adoption patterns |

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
1. **Server-first data fetching:** Fetch data in Server Components whenever possible. Eliminate client-server waterfalls. Client components should receive data as props, not fetch it themselves — this cuts LCP by 300-800ms on average.
2. **TypeScript strict mode with discriminated unions:** Enable `strict: true` in tsconfig. Model async states as `{ status: 'loading' } | { status: 'success', data: T } | { status: 'error', error: E }` — never `data?: T, isLoading: boolean, error?: Error` which allows impossible states.
3. **Measure Web Vitals from real users (RUM), not just Lighthouse:** Lighthouse is lab data (simulated). Deploy RUM (Vercel Analytics, Web Vitals JS, Sentry) to get 75th percentile field data. Fix what real users experience, not what a simulation shows.
4. **Semantic HTML before ARIA:** Use `<button>`, `<nav>`, `<main>`, `<dialog>` instead of `<div role="button">`. ARIA adds roles/states but not behavior — you must implement keyboard interaction yourself. Native elements work out of the box.
5. **Image optimization is non-negotiable:** Use `next/image` or Nuxt Image with explicit width/height, WebP/AVIF formats, responsive sizes, and lazy loading. Preload LCP image with `fetchpriority="high"`. Unoptimized images are the #1 cause of poor LCP.
6. **CSS: design tokens in Tailwind config, never hardcoded values:** `tailwind.config.ts` defines colors, spacing, fonts, breakpoints. Components reference tokens, not arbitrary values. Changing a brand color should require one config edit.
7. **Error boundaries at route and feature level:** Wrap every route segment in an error boundary. Feature-level boundaries prevent one widget crash from taking down the entire page. Log to Sentry/Datadog with React component stack.
8. **Test behavior, not implementation:** Assert what the user sees (`screen.getByText('Order confirmed')`) not internal state (`expect(component.state.confirmed).toBe(true)`). Implementation tests break on refactor; behavior tests survive.
9. **Bundle budget: 150KB gzipped JS per route:** Use `@next/bundle-analyzer` or `vite-bundle-visualizer` on every PR. Flag any route exceeding budget. Heavy libraries (`moment.js`, `lodash` all) should be replaced or dynamically imported.
10. **CI must fail on regression:** TypeScript check, ESLint, Prettier, Vitest, Playwright smoke, Lighthouse CI, and axe-core must all pass before merge. A red CI that developers ignore is worse than no CI — it trains the team that failures are acceptable.

## Anti-Patterns
<!-- DEEP: 5min -- each anti-pattern includes machine-detectable patterns -->

| ❌ Anti-Pattern | ✅ Do This Instead | 🔍 Detect (grep / lint) | 🛡️ Auto-Prevent |
|-----------------|---------------------|--------------------------|-------------------|
| Managing server state with `useState + useEffect` — fetch on mount, manual cache invalidation, stale UI after every mutation | Use TanStack Query (or SWR) for all server state. It handles caching, background refetch, cache invalidation on mutation, retry logic, and optimistic updates out of the box. | `grep -rn "useState.*\[\].*useEffect\|useEffect.*fetch\|useEffect.*axios" --include="*.tsx" --include="*.jsx"` → finds fetch-in-effect patterns | eslint `no-restricted-syntax: [{selector: "CallExpression[callee.name='useEffect'][arguments.0.body.body]:has(CallExpression[callee.name='fetch'])", message: "Use TanStack Query for server state, not useState+useEffect."}]` |
| Using `<div role="button" onClick={handler}>` everywhere because "styling native buttons is hard" | Use `<button>` — it handles keyboard focus, Enter/Space activation, screen reader announcements, and form submission natively. | `grep -rn "role=[\"']button[\"']" --include="*.tsx" --include="*.jsx"` → finds divs masquerading as buttons | eslint `jsx-a11y/no-noninteractive-element-interactions: error` + `jsx-a11y/no-static-element-interactions: error` |
| Using array index as React `key` prop — `<li key={index}>` — causes corrupted component state on reorder | Always use a stable, unique identifier as the `key` prop (`item.id`, `item.slug`). Array index causes React to misidentify components on add/remove/reorder. | `grep -rn "key=\{[a-z]+\}" --include="*.tsx" --include="*.jsx"` → finds short variable names as keys (likely index) | eslint `react/jsx-key: error` + custom rule: `no-restricted-syntax: [{selector: "JSXAttribute[name.name='key'][value.expression.type='Identifier'][value.expression.name=/^(i\|idx\|index)$/]", message: "Use stable ID for key, not array index."}]` |
| Lighthouse, axe-core, and bundle analyzer exist in the project config but CI doesn't block on failures — "we'll fix the violations next sprint" | Every quality gate must be enforced in CI with hard blocks: TypeScript check, ESLint, Prettier, Vitest, Playwright smoke, Lighthouse CI (≥90), axe-core (zero violations), bundle budget (<150KB gzipped per route). | `grep -rn "lighthouse\|lighthouseci\|@lhci" .github/workflows/ -l` → returns empty if Lighthouse is installed but not in CI | CI: `@lhci/cli autorun --collect.url=$DEPLOY_URL --upload.target=temporary-public-storage` with `assert: { preset: 'lighthouse:recommended' }` — fails if score < 90 |
| Testing implementation details — `expect(component.state.confirmed).toBe(true)` — tests break on every internal refactor | Test behavior, not implementation: `expect(screen.getByText('Order confirmed')).toBeInTheDocument()`. Behavior tests survive refactors; implementation tests die on every change. | `grep -rn "\.state\.\|\.props\.\|component\.instance\|\.internal" --include="*.test.*" --include="*.spec.*"` → finds implementation-detail assertions | eslint `testing-library/no-node-access: error` + `testing-library/prefer-screen-queries: error` |
| Loading third-party scripts (analytics, chat widgets, ad trackers) synchronously in `<head>` — blocks first paint by 2+ seconds | Load all third-party scripts with `async` or `defer`. Use `next/script` with `strategy="lazyOnload"` for non-critical scripts. | `grep -rn "<script\b(?!.*\b(?:async\|defer)\b)" --include="*.html" --include="*.tsx" --include="*.jsx"` → finds scripts without async/defer | eslint `@next/next/no-sync-scripts: error` + pre-commit hook: block any `<script>` tag without `async\|defer\|type="module"` unless it's `next/script` |
| Blocking the entire page behind a single loading spinner — users stare at a white screen for 3 seconds | Use React Suspense boundaries at the component level, not the page level. Each data-dependent section shows its own skeleton. | `grep -rn "Suspense.*fallback" --include="*.tsx" --include="*.jsx" -c` → returns 0 if no Suspense boundaries exist | eslint `react/no-unstable-nested-components: error` — promotes component-level loading boundaries |

## Error Decoder
<!-- DEEP: 5min -- each entry includes a console-string matcher for automatic recovery loops -->

| 🖥️ Console Match (grep pattern) | Symptom | Root Cause | Fix | 🔄 Auto-Recovery Loop |
|---|---|---|---|---|
| `Uncaught TypeError:.*is undefined\|Cannot read properties of undefined` + `grep -rn "as \w+\|!" --include="*.tsx" --include="*.ts"` finds unsafe type casts | White screen of death — `data` was undefined from a 500 API response | API error state was not handled — component assumed `data` was always defined | Always handle all four states: loading, success, error, empty. Use discriminated unions: `{ status: 'loading' } \| { status: 'error', error: E } \| { status: 'success', data: T }`. Add error boundaries at route and feature level | 1. Find unsafe accesses: `grep -rn "\.data\." src/ --include="*.tsx" -B 2 \| grep -v "status\|loading\|error"` 2. Add discriminated union type 3. Add `<ErrorBoundary>` wrapper 4. Test: `curl -s http://localhost:3000/api/data \| jq .status` — simulate 500 |
| `Warning: Can't perform a React state update on an unmounted component` + `grep -rn "setInterval\|setTimeout" src/ --include="*.tsx" -A 3 \| grep -v "clearInterval\|clearTimeout"` | App crashed silently after navigation — 20 intervals running simultaneously calling `setState` on unmounted components | `useEffect` with `setInterval` had no cleanup function — stale closures persisted after unmount | Add cleanup: `useEffect(() => { const id = setInterval(fetch, 5000); return () => clearInterval(id); }, [])`. Enable React strict mode to detect unsafe effects | 1. Find effects without cleanup: `grep -rn "useEffect.*setInterval\|useEffect.*addEventListener" src/ -A 5 \| grep -v "return\|cleanup"` 2. Add cleanup function to every subscription 3. Enable `<React.StrictMode>` 4. Test: navigate rapidly between screens 20×, verify no console warnings |
| `Largest Contentful Paint.*[3-9]\.\d s\|LCP.*[4-9]\d{3} ms` + `grep -rn "import.*moment\|import.*lodash" --include="*.tsx" --include="*.ts"` finds heavy libraries in main bundle | App took 12 seconds on mobile 3G — users bounced | `moment.js` (525KB) and entire `lodash` (275KB) in main bundle — no tree-shaking | Replace `moment.js` with `date-fns` (tree-shakeable). Import only specific lodash functions. Add `@next/bundle-analyzer`. Set CI bundle budget: <150KB gzipped per route | 1. Run `npx @next/bundle-analyzer` → identify heaviest chunks 2. Replace moment with `npm install date-fns && find src/ -name '*.tsx' -exec sed -i '' 's/moment/date-fns/g' {} +` 3. Add CI: `@next/bundle-analyzer` with `maxSize: 150KB` 4. Verify: Lighthouse mobile score ≥ 90 |
| `Layout shift.*CLS.*0\.[2-9]\|Cumulative Layout Shift.*0\.[2-9]` + `grep -rn "<img\b(?!.*\bwidth\b)(?!.*\bheight\b)" --include="*.tsx" --include="*.jsx"` | Layout jumps — users tap wrong elements, bounce rate increased 27% | Images and ad slots rendered without explicit dimensions — layout engine reflows when content loads | Set explicit `width`/`height` on all images. Reserve space for dynamic content with `min-height`. Use `aspect-ratio` CSS. Add `font-display: optional` | 1. Find images without dimensions: `grep -rn "<img" src/ --include="*.tsx" \| grep -v "width\|height"` 2. Add `width={}` and `height={}` to every `<img>` 3. Add CI: Lighthouse CLS < 0.1 4. Test: `npx lighthouse --throttling.cpuSlowdownMultiplier=4` |
| `Firefox.*not.*working\|Safari.*broken\|works on Chrome but not` + `grep -rn "display:\s*grid\|gap:" src/ --include="*.css" -A 2 \| grep -v "@supports"` | Checkout button invisible on Firefox but perfect in Chrome | CSS Grid used without `@supports` fallback — Firefox had gap interaction bug with form elements | Add CSS feature queries: `@supports (grid-area: auto) { }`. Use Autoprefixer with `browserslist`. Test on Chrome, Firefox, Safari | 1. Find grid without fallback: `grep -rn "display:\s*grid" src/ -A 3 \| grep -v "@supports\|@media"` 2. Add `@supports` fallback 3. CI: Playwright E2E on Chromium + Firefox + WebKit 4. `browserslist: ['last 2 versions', '> 1%']` |
| `Warning: Each child in a list should have a unique "key" prop` + `grep -rn "\.map\(" src/ --include="*.tsx" -A 1 \| grep -v "key="` | List items flicker, form state lost on reorder | Array index used as key — React misidentifies components on add/remove/reorder | Always use stable unique ID as key (`item.id`, `item.slug`). Never use array index or random values | 1. Find keyless maps: `grep -rn "\.map\(" src/ --include="*.tsx" -A 3 \| grep -v "key="` 2. Add `key={item.id}` to every `.map()` 3. eslint: `react/jsx-key: error` 4. Test: reorder a list and verify all component state is preserved |
## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. Each has a mechanical validation command. -->

| ID | Checklist Item | Validation Command | Auto-Fix |
|----|---------------|-------------------|----------|
| **[S1]** | Framework documented with rationale (Next.js, Remix, Vite, Nuxt) | `grep -rn "\"next\"\|\"@remix-run\"\|\"vite\"\|\"nuxt\"" package.json` → must match | — |
| **[S2]** | TypeScript strict mode; zero `any` in domain types; discriminated unions for async states | `grep -rn "strict.*:.*true" tsconfig.json` → must match; `grep -rn ": any\b" src/ --include="*.ts" --include="*.tsx" -c` → must return 0 | CI: `tsc --noEmit` with `strict: true` fails on `any` |
| **[S3]** | State management follows taxonomy: TanStack Query for server, Zustand for client, React Hook Form + Zod for forms, URL for filters | `grep -rn "@tanstack/react-query\|useQuery\|zustand\|react-hook-form" src/ --include="*.tsx" -l` → must match > 0 files | `npm install @tanstack/react-query zustand react-hook-form zod` |
| **[S4]** | CSS: Tailwind with design tokens; no hardcoded colors; mobile-first; dark mode | `npx tailwindcss --check` → must pass; `grep -rn "#[0-9a-fA-F]{6}\|#[0-9a-fA-F]{3}" src/ --include="*.tsx"` → must return 0 | `npx @tailwindcss/upgrade` or eslint `tailwindcss/no-custom-classname: error` |
| **[S5]** | Core Web Vitals: LCP < 2.5s, INP < 200ms, CLS < 0.1 | `npx lighthouse http://localhost:3000 --only-categories=performance --throttling-method=simulate \| jq '.categories.performance.score'` → must be ≥ 0.9 | CI: `@lhci/cli autorun --assert.preset=lighthouse:recommended` |
| **[S6]** | Lighthouse ≥ 90 (Performance, Accessibility, Best Practices, SEO) mobile + desktop | `npx @lhci/cli collect --url=http://localhost:3000 && npx @lhci/cli assert --preset=lighthouse:recommended` → must return 0 | CI: `.github/workflows/lighthouse.yml` with `@lhci/cli` |
| **[S7]** | WCAG 2.2 AA: semantic HTML, heading hierarchy, keyboard nav, focus management, contrast ≥ 4.5:1 | `npx @axe-core/playwright --include="src/**/*.spec.ts"` → must return 0 violations | `npm install --save-dev @axe-core/playwright` + Playwright test fixture |
| **[S8]** | Images: next/image or Nuxt Image; WebP/AVIF; explicit width/height; LCP image `fetchpriority="high"` | `grep -rn "<img\b" src/ --include="*.tsx" \| grep -v "next/image\|NuxtImg\|width=\|height="` → must return 0 | — |
| **[S9]** | Bundle: initial JS < 150KB gzipped per route; dynamic imports for heavy libs; tree-shaking verified | `npx @next/bundle-analyzer` → each route chunk must be < 150KB gzipped | CI: `@next/bundle-analyzer` with `maxSize: 150KB` gate |
| **[S10]** | Error boundaries at route + feature level; graceful fallback UI; error logging (Sentry) | `grep -rn "ErrorBoundary\|error\.tsx\|error\.jsx" src/ --include="*.tsx" --include="*.jsx" -l` → must match > 0 files | `npx @sentry/nextjs --configure` or copy `templates/error-boundary.tsx` |
| **[S11]** | Security headers: CSP, X-Frame-Options, X-Content-Type-Options, HSTS, Referrer-Policy | `curl -sI https://localhost:3000 \| grep -iE "content-security-policy\|x-frame-options\|strict-transport-security"` → must return all headers | Copy `templates/security-headers.ts` into `next.config.js` |
| **[S12]** | Sitemap, robots.txt, canonical URLs, Open Graph meta tags | `curl -s https://localhost:3000/robots.txt \| head -1` → must return 200; `grep -rn "og:" src/ --include="*.tsx"` → must match | `npm install next-sitemap` |
| **[S13]** | Playwright E2E: critical flows + axe-core audit in CI; API mocking for error states | `npx playwright test --project=chromium` → must pass all; `grep -rn "@axe-core/playwright" e2e/` → must match | `npx playwright install` + copy `e2e/a11y-fixture.ts` |
| **[S14]** | CI: TS check → ESLint → Prettier → Vitest → Playwright → Lighthouse CI; fails on regression | `npx concurrently "tsc --noEmit" "eslint src/" "prettier --check src/" "vitest run" "playwright test"` → must return 0 | Copy `.github/workflows/ci-frontend.yml` template |

## Negative Constraints
<!-- DEEP: 5min -- hard-gate rules. Violating any of these is a production incident waiting to happen. -->

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|--------------------|--------------------|--------------------|
| NC1 | **REFUSE to ship a page with initial JS > 200KB gzipped** — mobile users on 3G pay 4+ seconds for every 100KB over budget. Barrel imports and un-tree-shaken libs are the #1 cause of bundle bloat. | `npx @next/bundle-analyzer` → any route chunk > 200KB gzipped | BLOCK merge. File a P1 ticket. Require dynamic import or library replacement before merge. |
| NC2 | **REFUSE to ship with Lighthouse Performance < 85** — a score below 85 means real users are experiencing slow loads. Every 1-second delay in load time reduces conversion by 7%. | `npx @lhci/cli assert --preset=lighthouse:recommended` → score < 0.85 | BLOCK merge. Run bundle analyzer, identify largest chunks, and fix before merging. |
| NC3 | **STOP using `<div onClick>` instead of `<button>`** — divs lack keyboard navigation, focus management, and screen reader announcements. This is an accessibility violation that excludes keyboard-only users. | `grep -rn "role=[\"']button[\"']" --include="*.tsx" --include="*.jsx" \| grep -c` → > 0 | BLOCK PR. eslint `jsx-a11y/no-noninteractive-element-interactions: error`. Replace all div-buttons with native `<button>`. |
| NC4 | **DETECT and BLOCK images without explicit dimensions** — images without `width`/`height` cause CLS (layout shift) when they load. CLS > 0.1 damages Core Web Vitals and SEO rankings. | `grep -rn "<img\b" src/ --include="*.tsx" \| grep -v "width=\|height=\|next/image\|NuxtImg" \| grep -c` → > 0 | BLOCK PR. Add `width`/`height` or migrate to `next/image`. Run Lighthouse to verify CLS < 0.1. |
| NC5 | **REFUSE to use `useState + useEffect` for server data** — this pattern creates stale UI, race conditions, and missing cache invalidation. It's the #1 cause of "I had to refresh the page" bugs. | `grep -rn "useEffect.*fetch\|useEffect.*axios" --include="*.tsx" \| grep -v "TanStack\|react-query\|useSWR" \| grep -c` → > 0 | BLOCK PR. Migrate to TanStack Query or SWR. The TanStack Query ESLint plugin can auto-detect and suggest fixes. |
| NC6 | **DETECT and BLOCK `key={index}` in list renders** — array index as key causes React to misidentify components on reorder, corrupting state and causing animation bugs. | `grep -rn "key=\{[a-z]\}" --include="*.tsx" \| grep -v "\.id\|\.slug\|\.uuid" \| grep -c` → > 0 | BLOCK PR. eslint `react/jsx-key: error`. Replace with stable unique ID from data. |
| NC7 | **STOP shipping without Error Boundaries** — unhandled React errors crash the entire component tree to a white screen. Every route needs a boundary with graceful fallback UI. | `grep -rn "ErrorBoundary\|error\.tsx" src/ --include="*.tsx" -l \| wc -l` → 0 | BLOCK PR. Add `<ErrorBoundary>` to every route. Add `error.tsx` (Next.js) or top-level boundary. |

## Calibration — How to Know Your Level
<!-- STANDARD: 3min — honest self-assessment rubric -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You can build a component but can't explain why INP is 350ms on a real Moto G4 — you blame "React being slow" | You can load a production page in Chrome DevTools, run a Performance trace, identify the specific function causing the longest task, and fix it — INP drops to < 200ms | Your app ships with LCP < 1.5s, CLS < 0.05, and INP < 100ms on a $150 Android device on throttled 3G — and these numbers are verified by CrUX field data, not lab tests |
| You handle loading, success, and error states with if/else chains that miss empty and partial-data states | You model every async data dependency as a discriminated union (`{ status: 'loading' } \| { status: 'success', data: T } \| { status: 'error', error: E }`) and TypeScript enforces that all branches are handled | You define the async state pattern for your org and the teams that adopt it see a 60% reduction in "cannot read property of undefined" production errors in the first quarter |
| You add `aria-label` to a div and consider the component "accessible" — Lighthouse says 100 but a screen reader user can't navigate past your carousel | You can navigate your entire app with only a keyboard, never touching a mouse, and complete every critical flow — including modals, dropdowns, and drag-and-drop interactions | Your app passes an external WCAG 2.2 AA audit by a certified accessibility specialist on first submission with fewer than 3 findings — and you've trained 3 other developers to do the same |

**The Litmus Test:** Build a page with: a server-rendered product grid (50 items with images), a filter sidebar (6 facet groups with counts), and an "add to cart" that updates a header badge — all on Next.js App Router. It must achieve LCP < 1.5s, CLS = 0, and INP < 100ms on a Moto G4 with Slow 3G throttling. If any Core Web Vital is above the threshold, you're not L3 yet.

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

## References
<!-- QUICK: 30s -- links to deeper reading -->
- [references/react-patterns.md](references/react-patterns.md) — Server Components, compound components, render props vs hooks, custom hooks
- [references/performance-cwv.md](references/performance-cwv.md) — Core Web Vitals optimization: LCP, INP, CLS techniques and measurement
- [references/bundle-optimization.md](references/bundle-optimization.md) — Dynamic imports, code splitting, tree shaking, bundle analysis
- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev/)
- [Vue.js Documentation](https://vuejs.org/guide/)
- [web.dev — Core Web Vitals](https://web.dev/vitals/)
- [WCAG 2.2 Guidelines](https://www.w3.org/TR/WCAG22/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [TanStack Query](https://tanstack.com/query/latest)
- [Testing Library Guiding Principles](https://testing-library.com/docs/guiding-principles/)
