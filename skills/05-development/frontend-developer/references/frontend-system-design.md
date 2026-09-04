# Frontend System Design — Thinking at the UI-Scale Level

> Original explainer for interview prep and learning. [research-source: title-only]

## What it is

Frontend system design is the discipline of designing a *frontend application* the way backend system design designs a service: requirements → scale (users/screens/data) → architecture → data flow → performance → failure. It covers the whole client: **app architecture, state management, data fetching, routing, rendering strategy, performance, accessibility, and how the client talks to the backend.** Interviewers use it to test senior frontend thinking beyond "build a component."

## The framework (mirror backend design, adapted to the client)

1. **Clarify requirements** — what screens/features; who uses it (DAU, devices, regions); read-heavy vs write; realtime needs; offline needs.
2. **Set the constraints that matter** — bundle size budget, first-load target (LCP), target devices (low-end mobile?), data volume per screen.
3. **Choose the app architecture** — framework + structure:
   - **Rendering strategy:** SPA vs SSR vs SSG vs islands/streaming. Decision drivers: SEO, first-load speed, interactivity, data freshness, cost. (A content site → SSR/SSG; a dashboard → SPA with route-level code-splitting.)
   - **Module/feature structure** — feature-first folders, shared UI kit, clear boundaries (the frontend version of modular monolith).
4. **Design state management** — the big fork:
   - **Server state** (data from APIs): caching layer (TanStack Query/SWR) — cache keys, staleness, invalidation, optimistic updates, refetch on focus.
   - **Client state** (UI): local/context/URL; a global store only when genuinely shared.
   - **URL as state** — filters, pagination, tabs belong in the URL (shareable, back-button-safe).
5. **Design data flow** — how screens fetch: query per screen, prefetch on route hover, cache in memory/IndexedDB, offline queue for writes. Include the **contract with the backend** (pagination, error shapes — see api-design docs).
6. **Performance budget & strategy** — code-splitting per route, image/font strategy, virtualization for long lists, memoization only where it pays, Web Vitals targets.
7. **Failure & edge states** — loading/empty/error/offline for every view; retries; partial data; "the API is down" UX.
8. **Accessibility & i18n as design inputs**, not afterthoughts.

## The interview-specific decision table

| Situation | Default choice |
|---|---|
| SEO + fast first paint + public content | SSR/SSG (Next.js-style), stream where possible |
| App-like dashboard behind login | SPA + route-level code splitting |
| Realtime data (chat, collab) | SPA + WebSocket/subscription layer (see websockets-realtime.md) |
| Low-end devices / regions | Ship less JS; SSR/static where possible; image CDN |
| Data freshness + offline | SWR/TanStack caching + service worker (see PWA notes in frontend-developer) |

## Frontend "scale" is different from backend scale

Frontend scale = **bundle size × device capability × state complexity**, not request QPS. A "scaling" frontend problem usually means: the bundle is huge, the state graph is tangled, or every screen re-fetches. The senior moves are architectural: split routes, centralize server state, push state to the URL, virtualize, and keep the data contract explicit.

## Common failure modes & answers

- **State explosion** → classify state (server/client/URL); each class gets its mechanism; never duplicate server state in a global store.
- **Bundle creep** → code-split by route, dynamic-import heavy libs, audit dependencies.
- **N+1 / waterfall fetches** → parallelize, prefetch, colocate queries with components, batch endpoints.
- **Slow interactions on low-end devices** → reduce main-thread work, virtualize lists, avoid layout thrash.
- **Offline = broken** → service worker + offline cache + write queue with sync on reconnect.

## Interview answer skeleton

"I'd scope requirements and constraints first — users, devices, first-load budget. Then choose the rendering and app architecture (SSR/SSG for content, SPA with code splitting for app-like views), split state into server (cached queries), client, and URL, and design every view's loading/error/empty/offline states. I set Web Vitals budgets, code-split routes, virtualize long lists, and treat accessibility and i18n as design inputs. The backend contract — pagination, errors, realtime — is decided up front."

## Anti-patterns

- ❌ Jumping to a framework without requirements (SSR when SEO doesn't matter, SPA when it does).
- ❌ Dumping all server data into a global store (re-render storms, stale duplication).
- ❌ One giant bundle / no route splitting.
- ❌ Only designing the happy path — no loading/error/offline states.
- ❌ Ignoring the target device: desktop-only assumptions on a low-end-mobile product.

## Deliberate-practice drills

1. **Design drill:** 30 minutes on "design the web client for a realtime collaborative dashboard" using the 8-step framework.
2. **State drill:** for an e-commerce checkout, classify every piece of state into server/client/URL and pick its mechanism.
3. **Performance drill:** given a 4 MB bundle and 3s LCP, propose the split plan and budget with targets.
4. **Edge drill:** design loading/error/empty/offline for a search results view, including retry and stale-while-revalidate.
5. **Interview drill:** "SPA or SSR for our product?" — answer with the decision drivers, not a preference.

## References
- `frontend-developer` SKILL.md — implementation, Core Web Vitals, CSS architecture at scale
- See also: system-design-101.md, api-design-best-practices.md (this repo)
- `ui-ux-designer` + `accessibility-*` skills — design/UX and WCAG inputs
