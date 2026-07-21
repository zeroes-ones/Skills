---
name: frontend-developer
description: React, Next.js, and Vue frontend development with TypeScript, Tailwind CSS, state management, routing, SSR/SSG patterns, Core Web Vitals optimization, accessibility (a11y), and testing. Trigger: frontend, React, Next.js, Vue, TypeScript, Tailwind, SSR, SSG, Core Web Vitals, accessibility.
author: Sandeep Kumar Penchala
---

# Frontend Developer

Build performant, accessible, and maintainable web applications using React (Next.js App Router) and Vue (Nuxt). This skill covers the complete frontend engineering practice: framework selection with trade-off analysis, component architecture with Server Components and composition patterns, state management taxonomy (server vs client vs form vs URL), CSS architecture at scale, Core Web Vitals optimization to measurable targets, WCAG 2.2 AA accessibility compliance, bundle optimization with tree shaking and code splitting, and comprehensive testing from unit to E2E.

## When to Use
- Choosing between Next.js, Vite React, Remix, Astro, or Nuxt for a new web project
- Implementing React Server Components (RSC) with Client Component boundaries and streaming
- Designing component architecture: compound components, render props vs hooks, Server Component composition
- Selecting and implementing state management: TanStack Query for server state, Zustand for client state, React Hook Form for forms
- Architecting CSS at scale: Tailwind utility-first patterns, CSS Modules, design tokens, responsive strategies
- Optimizing Core Web Vitals: LCP < 2.5s, INP < 200ms, CLS < 0.1 — measured via Real User Monitoring (RUM)
- Implementing WCAG 2.2 AA accessibility: semantic HTML, ARIA, keyboard navigation, focus management, screen reader testing
- Analyzing and optimizing bundle size: dynamic imports, tree shaking verification, code splitting strategies
- Setting up comprehensive testing: Vitest + React Testing Library (components), Playwright (E2E), axe-core (a11y)

## Core Workflow

### Phase 0: Framework Selection — Decision Tree

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

### Phase 1: Project Architecture & TypeScript Mastery

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

### Phase 2: State Management Taxonomy

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

### Phase 3: CSS Architecture at Scale

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

### Phase 4: Core Web Vitals — The Definitive Optimization Guide

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

### Phase 5: Accessibility — WCAG 2.2 AA Compliance

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

### Phase 6: Bundle Optimization

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

### Phase 7: Error Handling & Resilience

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

### Phase 8: Testing Strategy

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

Frontends consume APIs, render designs, and deliver user experiences — coordination with backend, design, and platform teams is continuous. Poor coordination manifests as mismatched contracts, broken UIs, and missed performance targets.

### Coordinate With

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **Backend Developer** | API contract creation/changes | OpenAPI spec review, field shape expectations, error response formats, pagination conventions |
| **Fullstack Developer** | Shared monorepo, Next.js/Remix features | Component APIs, server action signatures, shared type packages, middleware behavior |
| **Mobile Developer** | Cross-platform consistency | Design token alignment, navigation patterns, shared user flows, responsive breakpoint mapping |
| **UI/UX Designer** | Design handoff, feasibility review | Component complexity estimates, animation feasibility, responsive behavior, accessibility requirements |
| **QA Engineer** | E2E test scenarios, visual regression | Test IDs (data-testid), critical user paths, edge case states (loading, error, empty), accessibility test cases |
| **Observability Engineer** | Core Web Vitals, RUM setup | Custom metrics, performance budgets, trace context propagation, error boundary telemetry |
| **Security Reviewer** | CSP headers, XSS prevention, auth flows | Content-Security-Policy requirements, sanitization approach, token storage patterns, CSRF protection |
| **DevOps Engineer** | Build/deploy pipeline, CDN config | Static asset caching headers, environment variable needs, SSR server sizing, edge function limits |

### Communication Triggers

| Trigger | Notify | Why |
|---------|--------|-----|
| API contract breaking change needed | Backend, Fullstack, Mobile | Coordinate deprecation timeline; version API or migrate consumers |
| New third-party script/service added | Security Reviewer, Observability | CSP update, performance impact assessment, PII exposure review |
| Design system token change | UI/UX Designer, Mobile | Consistent visual language across platforms |
| Core Web Vitals regression detected | Observability, Backend (if API latency is cause) | Joint investigation — is it frontend bundle, API response, or rendering? |
| New route requiring SSR/SSG decision | Backend, DevOps | Deploy configuration, cache strategy, CDN rules |
| Bundle size spike (>20%) | All developers | Identify cause — unoptimized dependency, duplicate import, missing tree shaking |

### Escalation Path

```
API contract blocked? → Backend Developer lead → System Architect
Design feasibility dispute? → UI/UX Designer → Product Strategist
Performance SLO breach? → Observability Engineer → DevOps Engineer
Security vulnerability in dependency? → Security Reviewer → Security Engineer
Accessibility compliance gap? → QA Engineer → Compliance Officer
```

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

## Production Checklist

- [ ] Framework selection documented with rationale (Next.js App Router, Remix, Vite SPA, or Nuxt)
- [ ] TypeScript strict mode enabled; zero `any` in domain types; discriminated unions for async states
- [ ] State management follows taxonomy: TanStack Query for server state, Zustand for global client state, React Hook Form + Zod for forms, URL for shareable filters/pagination
- [ ] CSS architecture: Tailwind with design tokens in config; no hardcoded color values; mobile-first responsive; dark mode via class strategy
- [ ] Core Web Vitals: LCP < 2.5s (preloaded hero image, inlined critical CSS, self-hosted fonts); INP < 200ms (long tasks broken, inputs debounced); CLS < 0.1 (explicit dimensions, reserved spaces)
- [ ] Lighthouse score ≥ 90 in Performance, Accessibility, Best Practices, SEO on both mobile and desktop
- [ ] WCAG 2.2 AA: semantic HTML throughout; heading hierarchy without gaps; keyboard navigation verified; focus management on SPA navigation; color contrast ≥ 4.5:1; axe-core zero violations in CI
- [ ] Images: using next/image or Nuxt Image; WebP/AVIF with responsive sizes; explicit width/height; LCP image preloaded with fetchpriority="high"
- [ ] Bundle: initial JS < 150KB gzipped per route; heavy libraries dynamically imported; bundle analyzed for duplication; tree shaking verified
- [ ] Error boundaries at route and feature levels; graceful fallback UI; error logging to monitoring service (Sentry/Datadog)
- [ ] Security headers configured: CSP, X-Frame-Options, X-Content-Type-Options, HSTS, Referrer-Policy, Permissions-Policy
- [ ] Sitemap, robots.txt, canonical URLs, Open Graph meta tags configured
- [ ] Playwright E2E tests: critical user flows covered; axe-core accessibility audit in CI; API mocking for error states
- [ ] CI pipeline: TypeScript check → ESLint → Prettier → Vitest → Playwright → Lighthouse CI; fails on regression

## References
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
