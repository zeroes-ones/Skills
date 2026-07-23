# Best Practices

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
