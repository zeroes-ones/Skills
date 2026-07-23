# Best Practices

<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Type safety end-to-end**: Use Zod schemas shared between frontend and backend. tRPC or typed fetch for compile-time guarantees.
- **Server-first data fetching**: Fetch on server when possible (RSC, SSR loaders). Eliminates client-server waterfalls and improves LCP.
- **Progressive enhancement**: Core functionality works without JavaScript. Forms submit natively; JavaScript enhances with client-side validation and optimistic UI.
- **Single source of truth**: Shared validation, shared types, shared constants. DRY across the stack.
- **Graceful degradation**: External service failures shouldn't crash the app. Show cached/stale data, fallback UI, retry buttons.
- **Security mindset**: Validate on both client (UX) and server (security). Never trust client input. Sanitize user-generated content. CSP headers, CSRF tokens.
