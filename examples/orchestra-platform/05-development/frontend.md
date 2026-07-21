# Frontend Architecture

## Technology Stack

React 18.3 with TypeScript 5.5 in strict mode. Next.js 14 using the App Router — all routes under `src/app/` with `layout.tsx` for shared shell (sidebar nav, top bar, breadcrumbs). Zustand 4.5 for client-side state (auth session, UI preferences, selected organization). TanStack React Query 5 for all server state (caching, refetching, optimistic updates). Tailwind CSS 3.4 with design tokens mapped to a custom theme in `tailwind.config.ts`. shadcn/ui as the component primitives (Button, Input, Dialog, DropdownMenu) extended with Orchestra-specific components.

## Component Architecture — Atomic Design

**Atoms**: Button, Input, Label, Badge, Icon, Spinner, Avatar, Toggle, Tooltip — pure presentational, no business logic.

**Molecules**: SearchBar (Input + Icon + debounce), StatusBadge (Badge + health status logic), ServiceCard (Badge + Avatar + text), FilterGroup (multiple Toggle + label), FormField (Label + Input + error message).

**Organisms**: ServiceTable (Table + StatusBadge + RowActions), TemplateWizard (Stepper + FormField + FilePreview), PluginCatalog (SearchBar + FilterGroup + ServiceCard grid), AdminMetrics (Chart + MetricCard rows).

**Templates**: CatalogLayout (SidebarFilter + ServiceTable), WizardLayout (Stepper container + step transitions), DashboardLayout (Metrics row + Activity feed + Charts grid).

**Pages**: `/catalog` (search, filter, detail panel), `/templates/create` (5-step wizard), `/plugins/configure/:id` (plugin config form), `/admin` (dashboard + team management), `/settings` (org profile, billing, members).

## Key Pages and States

**Catalog Page**: Loading state shows 12 skeleton cards pulsing. Empty state ("No services match your filters — try adjusting criteria" with illustration). Error state (retry button, error details collapsed behind "Show details"). Normal state: faceted search with `useDeferredValue` for responsive 60fps filtering. URL search params persist filter state for shareable links.

**Template Wizard**: Each step validates independently. Back button preserves form state. Browser back button triggers a "Leave page?" confirmation dialog. On success, redirects to the new service detail page. On failure, shows step-specific error with retry.

**Admin Dashboard**: All metric cards load independently (React Suspense boundaries). Charts lazy-load below the fold. Time range selector (24h, 7d, 30d) updates all panels via React Query key invalidation.
