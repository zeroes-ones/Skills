# Scale Depth: Solo → Small → Medium → Enterprise

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
