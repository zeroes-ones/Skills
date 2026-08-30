# State Management — Boundaries, Not Libraries

## The Boundary Model

State is not "pick a library" — it is "assign each piece of state to the right home":

| State type | Home | Why |
|------------|------|-----|
| Server state (API data, cache, mutations) | **React Query / TanStack Query** | Caching, refetch, optimistic updates, invalidation built in |
| Global client state (auth, settings, cart) | **Zustand** (light) or **Redux Toolkit** (large teams) | Cross-screen shared mutable state with selectors |
| Local UI state (form input, toggles) | **useState / useReducer** | Component-scoped; lifting it globally is premature |
| URL/navigation state | **React Navigation / Expo Router** | Route params are state; don't duplicate in stores |
| Server-synced offline state | **React Query + WatermelonDB/SQLite** | Persistence and sync, not in-memory stores |

## Selection Guide

- **Small/medium app, 1-3 devs** → Zustand + React Query. Minimal boilerplate, fast iteration.
- **Large app, many teams** → Redux Toolkit (RTK Query) for its DevTools, normalization, and team conventions.
- **Form-heavy** → react-hook-form for form state; keep server calls in React Query.
- **Offline-first** → WatermelonDB (lazy, reactive) or SQLite via `expo-sqlite`; sync engine in a library, never hand-rolled.

## Anti-Patterns

- **Everything in one store** — server cache in Redux duplicates React Query; you now maintain two sources of truth.
- **State in navigation** — passing whole objects as route params (they should be IDs + a query).
- **Context for everything** — Context re-renders all consumers; use it for low-frequency, low-volume state only.
- **No selectors** — components re-render on any store change; use selectors/memo to subscribe narrowly.

## Performance Note

Global store updates trigger re-renders across consumers. Keep store state normalized and selectors narrow; the scroll path (lists) should read the store as little as possible — prefer local/query state in list rows.
