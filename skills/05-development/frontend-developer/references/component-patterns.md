# Component Patterns

> **Author:** Sandeep Kumar Penchala

Comprehensive patterns for building composable, performant, and maintainable UI components across React, Vue, and Svelte. These patterns derive from the frontend-developer skill's emphasis on clean architecture and separation of concerns.

## Component Composition Patterns

### 1. Render Props (React)

Pass a function as a child/render prop to share logic between components. Best when you need runtime flexibility but avoid when hooks can serve.

```tsx
// DataFetcher shares fetch state via render prop
interface FetchProps<T> {
  url: string;
  children: (state: { data: T | null; loading: boolean; error: Error | null }) => React.ReactNode;
}

function DataFetcher<T>({ url, children }: FetchProps<T>) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    fetch(url).then(r => r.json()).then(setData).catch(setError).finally(() => setLoading(false));
  }, [url]);

  return <>{children({ data, loading, error })}</>;
}
```

### 2. Higher-Order Components (HOCs)

Functions that take a component and return an enhanced one. Common for cross-cutting concerns like auth, logging, theming.

```tsx
function withAuth<P extends object>(Component: React.ComponentType<P>) {
  return function AuthenticatedComponent(props: P) {
    const { user, isLoading } = useAuth();
    if (isLoading) return <Spinner />;
    if (!user) return <Navigate to="/login" />;
    return <Component {...props} user={user} />;
  };
}

const ProtectedDashboard = withAuth(Dashboard);
```

### 3. Custom Hooks (React)

The primary composition mechanism in modern React. Extract stateful logic into reusable functions.

```tsx
function useDebounce<T>(value: T, delay: number): T {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);
  return debounced;
}

function useLocalStorage<T>(key: string, initial: T): [T, (v: T) => void] {
  const [stored, setStored] = useState<T>(() => {
    const item = window.localStorage.getItem(key);
    return item ? JSON.parse(item) : initial;
  });
  const setValue = (value: T) => { window.localStorage.setItem(key, JSON.stringify(value)); setStored(value); };
  return [stored, setValue];
}
```

### 4. Compound Components

Share implicit state between parent and children without prop drilling. Ideal for Select, Tabs, Accordion, and Menu components.

```tsx
const TabsContext = createContext<{ active: string; setActive: (id: string) => void } | null>(null);

function Tabs({ children, defaultTab }: { children: React.ReactNode; defaultTab: string }) {
  const [active, setActive] = useState(defaultTab);
  return <TabsContext.Provider value={{ active, setActive }}>{children}</TabsContext.Provider>;
}

Tabs.Tab = function Tab({ id, children }: { id: string; children: React.ReactNode }) {
  const ctx = useContext(TabsContext)!;
  return <button onClick={() => ctx.setActive(id)} className={ctx.active === id ? 'active' : ''}>{children}</button>;
};

Tabs.Panel = function Panel({ id, children }: { id: string; children: React.ReactNode }) {
  const ctx = useContext(TabsContext)!;
  return ctx.active === id ? <div>{children}</div> : null;
};
```

### 5. Vue Composables

Vue 3 composables are the equivalent of React hooks for reusing stateful logic.

```typescript
// composables/useFetch.ts
import { ref, watchEffect, type Ref } from 'vue';

export function useFetch<T>(url: Ref<string>) {
  const data = ref<T | null>(null);
  const loading = ref(true);
  const error = ref<Error | null>(null);

  watchEffect(async () => {
    loading.value = true;
    try {
      data.value = await fetch(url.value).then(r => r.json());
    } catch (e) {
      error.value = e as Error;
    } finally {
      loading.value = false;
    }
  });

  return { data, loading, error };
}
```

### 6. Svelte Stores

Svelte uses reactive stores for shared state. Derived stores automatically recalculate.

```typescript
// stores/cart.ts
import { writable, derived } from 'svelte/store';

export const cartItems = writable<CartItem[]>([]);
export const itemCount = derived(cartItems, $items => $items.length);
export const cartTotal = derived(cartItems, $items => $items.reduce((sum, i) => sum + i.price * i.qty, 0));
```

## State Management Decision Tree

```
Does state belong to a single component?
├── YES → useState (React) / ref (Vue) / local variable (Svelte)
└── NO → Is it shared by 2-3 sibling components?
    ├── YES → Lift state up / props
    └── NO → Is the update logic complex (multiple sub-values)?
        ├── YES → useReducer (React)
        └── NO → Do 4+ components across the tree need it?
            ├── YES → Is the app large with frequent updates?
            │   ├── YES → Zustand (lightweight), Redux Toolkit (full-featured)
            │   └── NO → Context API / provide-inject (Vue)
            └── NO → Is it server state (fetched from API)?
                ├── YES → React Query / TanStack Query / SWR
                └── NO → Reconsider — does it actually need global state?
```

| Library | Bundle Size | Boilerplate | Best For |
|---------|------------|-------------|----------|
| Context API | 0 KB | Low | Theme, locale, auth — low-frequency updates |
| Zustand | ~1 KB | Minimal | Medium apps, fast re-renders, no boilerplate |
| Jotai | ~2 KB | Minimal | Atomic state, fine-grained updates |
| Redux Toolkit | ~12 KB | Moderate | Large apps with complex state, DevTools, middleware |
| MobX | ~16 KB | Low | OOP-style state, automatic dependency tracking |

## Performance Patterns

### Memoization (React)

```tsx
// useMemo — cache expensive computations
const sorted = useMemo(() => items.sort((a, b) => a.name.localeCompare(b.name)), [items]);

// useCallback — stable function references for child memo
const handleClick = useCallback((id: string) => { dispatch({ type: 'SELECT', id }); }, [dispatch]);

// React.memo — skip re-render when props haven't changed
const ExpensiveList = React.memo(function ExpensiveList({ items }: { items: Item[] }) {
  return items.map(i => <ExpensiveItem key={i.id} item={i} />);
});
```

### Virtual Scrolling

For lists with 1000+ items, render only visible rows:

```tsx
import { useVirtualizer } from '@tanstack/react-virtual';

function VirtualList({ items }: { items: string[] }) {
  const parentRef = useRef<HTMLDivElement>(null);
  const virtualizer = useVirtualizer({ count: items.length, getScrollElement: () => parentRef.current, estimateSize: () => 40 });
  return (
    <div ref={parentRef} style={{ height: 600, overflow: 'auto' }}>
      <div style={{ height: virtualizer.getTotalSize() }}>
        {virtualizer.getVirtualItems().map(vi => (
          <div key={vi.key} style={{ position: 'absolute', top: 0, transform: `translateY(${vi.start}px)` }}>{items[vi.index]}</div>
        ))}
      </div>
    </div>
  );
}
```

### Lazy Loading & Code Splitting

```tsx
// Route-based splitting
const Dashboard = React.lazy(() => import('./pages/Dashboard'));
const Settings = React.lazy(() => import('./pages/Settings'));

// Component-based splitting
const HeavyChart = React.lazy(() => import('./HeavyChart'));

function App() {
  return (
    <Suspense fallback={<PageSkeleton />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
}
```

## Form Patterns

### Controlled vs Uncontrolled

| Approach | When to Use | Tradeoff |
|----------|-------------|----------|
| Controlled (`value` + `onChange`) | Real-time validation, dynamic fields, conditional logic | More code, re-renders on every keystroke |
| Uncontrolled (`ref` + `defaultValue`) | Simple forms, submit-only validation | Less code, harder to validate per-keystroke |

```tsx
// Controlled with React Hook Form + Zod
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';

const schema = z.object({
  email: z.string().email(),
  age: z.number().min(18, 'Must be 18+'),
});

function SignupForm() {
  const { register, handleSubmit, formState: { errors } } = useForm({ resolver: zodResolver(schema) });
  const onSubmit = (data: z.infer<typeof schema>) => console.log(data);
  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('email')} />
      {errors.email && <span>{errors.email.message}</span>}
      <input type="number" {...register('age', { valueAsNumber: true })} />
      {errors.age && <span>{errors.age.message}</span>}
      <button type="submit">Submit</button>
    </form>
  );
}
```

### Validation Library Comparison

| Library | Size | Schema-first | TypeScript | Async Validation |
|---------|------|-------------|------------|------------------|
| Zod | ~12 KB | Yes | First-class | Yes (`.refine`) |
| Yup | ~8 KB | Yes | Good | Yes |
| Joi | ~150 KB (server) | Yes | Partial | Yes |
| Valibot | ~1 KB | Yes | First-class | Yes |

## CSS Strategy Comparison

| Approach | Bundle Impact | DX | Theming | Critical CSS |
|----------|-------------|-----|---------|-------------|
| CSS Modules | None (static CSS) | Good — co-located styles | Manual variables | Manual extraction |
| Tailwind CSS | ~3 KB (purged) | Excellent — rapid prototyping | Config file | Utility-first inline = zero unused |
| styled-components | ~12 KB + runtime | Good — full JS power | ThemeProvider | Needs babel-plugin |
| Vanilla Extract | Zero runtime | Good — type-safe | Sprinkles/recipes | Built-in |

**Decision:** Use Tailwind for rapid iteration and consistent design systems. Use CSS Modules for projects where designers hand off precise CSS. Use Vanilla Extract for type-safe, zero-runtime approaches in large TypeScript codebases.

## Error Boundary Patterns

```tsx
class ErrorBoundary extends React.Component<{ fallback: React.ReactNode; children: React.ReactNode }, { hasError: boolean }> {
  state = { hasError: false };
  static getDerivedStateFromError() { return { hasError: true }; }
  componentDidCatch(error: Error, info: React.ErrorInfo) { console.error('Caught:', error, info); }
  render() { return this.state.hasError ? this.props.fallback : this.props.children; }
}

// Layered boundaries: per-feature → per-route → global
<ErrorBoundary fallback={<GlobalError />}>
  <ErrorBoundary fallback={<RouteError />}>
    <ErrorBoundary fallback={<WidgetError />}>
      <CriticalWidget />
    </ErrorBoundary>
  </ErrorBoundary>
</ErrorBoundary>
```

## Data Fetching Patterns

```tsx
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

// Query — with loading/error/empty states
function UserList() {
  const { data, isLoading, isError, error } = useQuery({
    queryKey: ['users'],
    queryFn: () => fetch('/api/users').then(r => r.json()),
    staleTime: 30_000,  // 30s before refetch
    retry: 2,
  });
  if (isLoading) return <Skeleton count={5} />;
  if (isError) return <ErrorDisplay message={error.message} />;
  if (!data.length) return <EmptyState />;
  return <UserTable users={data} />;
}

// Mutation — optimistic updates
function useUpdateUser() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (user: User) => fetch(`/api/users/${user.id}`, { method: 'PUT', body: JSON.stringify(user) }),
    onMutate: async (updated) => {
      await queryClient.cancelQueries({ queryKey: ['users'] });
      const previous = queryClient.getQueryData(['users']);
      queryClient.setQueryData(['users'], (old: User[]) => old.map(u => u.id === updated.id ? updated : u));
      return { previous };
    },
    onError: (_err, _user, context) => { queryClient.setQueryData(['users'], context?.previous); },
    onSettled: () => { queryClient.invalidateQueries({ queryKey: ['users'] }); },
  });
}
```

These patterns embody the frontend-developer skill's principle of architecture-first development: choose the right composition pattern for the problem, escalate state management only when necessary, and instrument performance from the start.
