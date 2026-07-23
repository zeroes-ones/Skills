# Sub-Skills

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
