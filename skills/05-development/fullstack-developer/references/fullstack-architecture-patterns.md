---
name: fullstack-architecture-patterns
description: Deep reference on monorepo patterns, tRPC, BFF, Next.js server actions and RSC, Remix loaders/actions, real-time patterns, and file upload architectures for fullstack applications.
author: Sandeep Kumar Penchala
---

# Fullstack Architecture Patterns

A definitive reference for architecting fullstack TypeScript applications. Covers monorepo organization, end-to-end type safety, backend-for-frontend patterns, framework-specific fullstack patterns (Next.js, Remix), real-time communication, and file upload architectures.

---

## 1. Monorepo Patterns

### 1.1 Turborepo (Recommended for Most Teams)

```
my-app/
├── turbo.json              # Pipeline & cache configuration
├── pnpm-workspace.yaml     # Workspace definition
├── package.json             # Root scripts (turbo run ...)
├── apps/
│   ├── web/                 # Next.js frontend (port 3000)
│   ├── api/                 # Express/Fastify backend (port 4000)
│   ├── admin/               # Separate admin SPA
│   └── mobile/              # Expo React Native
├── packages/
│   ├── shared/              # Types, Zod schemas, constants, utilities
│   │   ├── src/
│   │   │   ├── types/       # Domain types shared across apps
│   │   │   ├── schemas/     # Zod validation schemas
│   │   │   ├── constants/   # Enums, error codes, config keys
│   │   │   └── utils/       # Date formatting, slug generation
│   │   └── package.json
│   ├── ui/                  # Shared React components (Storybook)
│   ├── config-eslint/       # Shared ESLint config
│   ├── config-ts/           # Shared TypeScript config
│   └── database/            # Prisma/Drizzle schema & migrations
└── tooling/
    └── scripts/             # Code generation, deployment helpers
```

**`turbo.json` critical configuration:**
```json
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": ["**/.env.*local"],
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": [".next/**", "dist/**", ".expo/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "lint": {
      "dependsOn": ["^build"]
    },
    "typecheck": {
      "dependsOn": ["^build"]
    },
    "test": {
      "dependsOn": ["build"],
      "inputs": ["src/**/*.tsx", "src/**/*.ts", "test/**/*.ts"]
    },
    "db:migrate": {
      "cache": false
    },
    "db:generate": {
      "cache": false
    }
  }
}
```

Key principles:
- **`^build`** means "run build in dependencies first, then this package."
- Packages reference each other via `workspace:*` protocol in `package.json`.
- `@repo/shared`, `@repo/ui`, `@repo/database` are importable from any app.
- CI caches `node_modules/.cache/turbo` for dramatic speed improvements.

### 1.2 Nx (Enterprise Scale)

Nx suits teams needing:
- Affected-command detection (`nx affected:test --base=main` — only test what changed)
- Strict dependency boundaries via module tags (enforce that `shared` cannot import from `web`)
- Project graph visualization for dependency auditing

**Nx boundary rules (`project.json`):**
```json
{
  "tags": ["scope:shared"],
  "implicitDependencies": []
}
```

**ESLint rule enforcing boundaries:**
```js
// .eslintrc.js with @nx/enforce-module-boundaries
'@nx/enforce-module-boundaries': ['error', {
  'allow': [],
  'depConstraints': [
    { 'sourceTag': 'scope:shared', 'onlyDependOnLibsWithTags': ['scope:shared'] },
    { 'sourceTag': 'scope:web', 'onlyDependOnLibsWithTags': ['scope:shared', 'scope:ui'] },
    { 'sourceTag': 'scope:api', 'onlyDependOnLibsWithTags': ['scope:shared', 'scope:database'] }
  ]
}]
```

### 1.3 Shared Types Strategy

**Layer 1: Domain types** — pure TypeScript, no runtime impact:
```typescript
// packages/shared/src/types/user.ts
export interface User {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'editor' | 'viewer';
  createdAt: Date;
}

export interface CreateUserInput {
  email: string;
  name: string;
  password: string;
}

export type UserResponse = Omit<User, 'passwordHash'>;
```

**Layer 2: Zod schemas** — runtime validation derived from types:
```typescript
// packages/shared/src/schemas/user.ts
import { z } from 'zod';

export const CreateUserSchema = z.object({
  email: z.string().email().max(255),
  name: z.string().min(1).max(100),
  password: z.string().min(8).max(128)
    .regex(/[A-Z]/, 'Must contain uppercase')
    .regex(/[a-z]/, 'Must contain lowercase')
    .regex(/[0-9]/, 'Must contain number'),
});

export type CreateUserInput = z.infer<typeof CreateUserSchema>;
// Type is automatically inferred — single source of truth!
```

**Layer 3: API contract** — what crosses the wire:
```typescript
// packages/shared/src/api/users.ts
export interface UserAPI {
  'GET /api/users': {
    query: { page?: number; limit?: number; search?: string };
    response: { data: UserResponse[]; total: number; page: number };
  };
  'POST /api/users': {
    body: CreateUserInput;
    response: { data: UserResponse };
  };
  'GET /api/users/:id': {
    params: { id: string };
    response: { data: UserResponse };
  };
}
```

---

## 2. tRPC — End-to-End Type Safety

tRPC eliminates the API contract drift possible with REST + OpenAPI by letting you import server types directly into the client.

### 2.1 Architecture

```
┌─────────────────────────────────────────────────┐
│  Monorepo: packages/shared (types & schemas)     │
└──────────┬──────────────────────┬────────────────┘
           │ import { router }    │ import { inferRouterOutputs }
           ▼                      ▼
┌──────────────────┐   ┌──────────────────────┐
│  Server (tRPC)   │   │  Client (React)       │
│  appRouter.ts    │   │  const { data } =     │
│                  │   │    trpc.user.getById  │
│  publicProcedure │   │    .useQuery({ id })  │
│    .input(schema)│   │  // data is fully     │
│    .query(...)   │   │  // typed!             │
└──────────────────┘   └──────────────────────┘
```

### 2.2 Router Definition

```typescript
// apps/api/src/trpc/router.ts
import { initTRPC, TRPCError } from '@trpc/server';
import { z } from 'zod';
import { CreateUserSchema } from '@repo/shared/schemas';

const t = initTRPC.context<{ userId?: string }>().create();

// Middleware: authentication
const isAuthed = t.middleware(({ ctx, next }) => {
  if (!ctx.userId) throw new TRPCError({ code: 'UNAUTHORIZED' });
  return next({ ctx: { userId: ctx.userId } });
});

// Reusable procedures
export const publicProcedure = t.procedure;
export const protectedProcedure = t.procedure.use(isAuthed);

// Router
export const appRouter = t.router({
  user: t.router({
    list: publicProcedure
      .input(z.object({ page: z.number().default(1), limit: z.number().max(100).default(20) }))
      .query(async ({ input, ctx }) => {
        const users = await db.user.findMany({
          skip: (input.page - 1) * input.limit,
          take: input.limit,
        });
        return { data: users, total: await db.user.count() };
      }),

    create: protectedProcedure
      .input(CreateUserSchema)
      .mutation(async ({ input }) => {
        const exists = await db.user.findUnique({ where: { email: input.email } });
        if (exists) throw new TRPCError({ code: 'CONFLICT', message: 'Email taken' });
        return db.user.create({ data: input });
      }),

    getById: publicProcedure
      .input(z.object({ id: z.string().uuid() }))
      .query(async ({ input }) => {
        const user = await db.user.findUnique({ where: { id: input.id } });
        if (!user) throw new TRPCError({ code: 'NOT_FOUND' });
        return user;
      }),
  }),
});

export type AppRouter = typeof appRouter;
```

### 2.3 Client Usage

```typescript
// apps/web/src/lib/trpc.ts
import { createTRPCReact } from '@trpc/react-query';
import type { AppRouter } from '@repo/api';
export const trpc = createTRPCReact<AppRouter>();

// apps/web/src/pages/users.tsx
import { trpc } from '@/lib/trpc';

function UsersPage() {
  const [page, setPage] = useState(1);

  // Fully typed query — data, error, isLoading all inferred
  const { data, isLoading, error } = trpc.user.list.useQuery({ page, limit: 20 });

  const createMutation = trpc.user.create.useMutation({
    onSuccess: () => {
      // Invalidate the list query to refetch
      trpcUtils.user.list.invalidate();
    },
  });

  if (isLoading) return <Skeleton />;
  if (error) return <ErrorBanner message={error.message} />;

  return (
    <div>
      {data?.data.map(user => (
        <UserCard key={user.id} user={user} />
      ))}
      <Pagination page={page} total={data?.total ?? 0} onChange={setPage} />
    </div>
  );
}
```

### 2.4 When NOT to Use tRPC
- Public APIs consumed by third parties (use REST + OpenAPI)
- Non-TypeScript clients (mobile apps, external services)
- Server-to-server communication without shared codebase (use gRPC)
- Very large payloads or streaming responses (use native fetch/streams)

---

## 3. BFF (Backend-for-Frontend) Pattern

### 3.1 Concept

Instead of one general-purpose API, each frontend gets a dedicated backend that shapes data specifically for its needs.

```
┌──────────┐  ┌──────────┐  ┌──────────┐
│  Web App  │  │  Mobile  │  │  TV App  │
└─────┬─────┘  └─────┬─────┘  └─────┬─────┘
      │              │              │
┌─────▼─────┐  ┌─────▼─────┐  ┌─────▼─────┐
│ BFF-Web   │  │ BFF-Mobile│  │ BFF-TV    │
│ (Next.js  │  │ (Express) │  │ (Fastify) │
│  API rt)  │  │           │  │           │
└─────┬─────┘  └─────┬─────┘  └─────┬─────┘
      │              │              │
      └──────────────┼──────────────┘
                     │
              ┌──────▼──────┐
              │  Domain API │
              │  (gRPC/REST)│
              └──────┬──────┘
                     │
              ┌──────▼──────┐
              │  Database   │
              └─────────────┘
```

### 3.2 BFF Responsibilities
- **Aggregation**: Combine data from multiple downstream services into a single response.
- **Transformation**: Reshape data for the specific frontend (camelCase for JS, different field subsets).
- **Protocol translation**: Downstream gRPC → frontend REST/GraphQL.
- **Authentication**: Validate tokens, inject user context into downstream calls.
- **Caching**: Cache composed responses with frontend-appropriate TTLs.
- **Error normalization**: Map downstream errors to frontend-friendly error formats.

### 3.3 BFF Anti-Patterns
- **Duplicated logic across BFFs**: Move shared logic to the domain API layer.
- **BFF becomes a monolith**: Each BFF should be thin (< 500 LOC). Heavy logic goes downstream.
- **Bypassing the BFF**: Frontend should never directly call the domain API (security, consistency risks).

---

## 4. Next.js Fullstack Patterns

### 4.1 Server Components (RSC) — Default Pattern

```typescript
// app/dashboard/page.tsx — Server Component (async, no 'use client')
import { db } from '@/lib/db';
import { auth } from '@/lib/auth';

export default async function DashboardPage() {
  const session = await auth(); // Reads cookie — server-only
  if (!session) redirect('/login');

  // Direct database query — no API layer needed
  const stats = await db.$queryRaw<DashboardStats[]>`
    SELECT
      COUNT(*) FILTER (WHERE status = 'active') as active_users,
      COUNT(*) FILTER (WHERE created_at > now() - interval '7 days') as new_users
    FROM users WHERE org_id = ${session.orgId}
  `;

  const recentOrders = await db.order.findMany({
    where: { orgId: session.orgId },
    orderBy: { createdAt: 'desc' },
    take: 10,
    include: { customer: { select: { name: true } } },
  });

  return (
    <div>
      <StatsCards stats={stats[0]} />
      <Suspense fallback={<OrdersSkeleton />}>
        <RecentOrders orders={recentOrders} />
      </Suspense>
    </div>
  );
}
```

**When to use Server Components:**
- Data fetching (no `useEffect` waterfalls)
- Access to backend resources (DB, filesystem, internal services)
- Large dependencies that shouldn't ship to the client
- SEO-critical content

### 4.2 Server Actions — Mutations Without API Routes

```typescript
// app/actions/order.ts — Server Action file
'use server';

import { revalidatePath } from 'next/cache';
import { z } from 'zod';
import { auth } from '@/lib/auth';
import { db } from '@/lib/db';

const CreateOrderSchema = z.object({
  productId: z.string().uuid(),
  quantity: z.number().int().min(1).max(100),
});

export async function createOrder(formData: FormData) {
  const session = await auth();
  if (!session) throw new Error('Unauthorized');

  const parsed = CreateOrderSchema.safeParse({
    productId: formData.get('productId'),
    quantity: Number(formData.get('quantity')),
  });

  if (!parsed.success) {
    return { error: parsed.error.flatten().fieldErrors };
  }

  await db.order.create({
    data: {
      ...parsed.data,
      userId: session.user.id,
    },
  });

  revalidatePath('/orders'); // Invalidate cache for this path
  return { success: true };
}

// app/checkout/page.tsx — Client Component using Server Action
'use client';
import { createOrder } from '@/app/actions/order';
import { useFormState } from 'react-dom';

export function CheckoutForm() {
  const [state, formAction] = useFormState(createOrder, null);

  return (
    <form action={formAction}>
      <input name="productId" type="hidden" value={product.id} />
      <input name="quantity" type="number" defaultValue={1} />
      {state?.error?.quantity && <p className="text-red-500">{state.error.quantity}</p>}
      <button type="submit">Place Order</button>
    </form>
  );
}
```

**Server Actions best practices:**
- Always validate input with Zod — Server Actions receive `FormData`, not typed objects.
- Use `revalidatePath` or `revalidateTag` to refresh cached data after mutation.
- Throw errors for unexpected failures; return error objects for validation failures.
- Keep actions small and focused; extract business logic to service layer functions.

### 4.3 API Routes vs Dedicated Backend

| Criterion | Next.js API Routes | Dedicated Backend (Express/Fastify) |
|-----------|-------------------|--------------------------------------|
| **Complexity** | Low — single deploy, same repo | Medium — separate deploy, service discovery |
| **Performance** | Serverless cold starts possible | Always warm, predictable latency |
| **Long-running tasks** | Limited by serverless timeout (Vercel: 10s hobby, 60s pro) | Unlimited |
| **WebSocket** | Not supported in API routes | Full WebSocket support |
| **Database connections** | Connection pooling tricky in serverless | Standard connection pooling |
| **Team scaling** | Fullstack devs own everything | Frontend/backend specialization |
| **Best for** | Early-stage, B2C SaaS, content sites | Complex domains, high-scale, enterprise |

**Hybrid pattern:** Use Next.js API routes for BFF (aggregation, auth) + dedicated backend for heavy compute and domain logic.

---

## 5. Remix Fullstack Patterns

### 5.1 Loaders (Data Fetching)

```typescript
// app/routes/dashboard.tsx
import { json, type LoaderFunctionArgs } from '@remix-run/node';
import { useLoaderData } from '@remix-run/react';
import { requireAuth } from '~/session.server';
import { db } from '~/db.server';

export async function loader({ request }: LoaderFunctionArgs) {
  const user = await requireAuth(request);

  // Parallel data fetching
  const [stats, recentOrders] = await Promise.all([
    db.getDashboardStats(user.orgId),
    db.order.findMany({
      where: { orgId: user.orgId },
      orderBy: { createdAt: 'desc' },
      take: 10,
    }),
  ]);

  return json({ stats, recentOrders, user });
}

export default function Dashboard() {
  const { stats, recentOrders, user } = useLoaderData<typeof loader>();
  // Fully typed — useLoaderData infers from the loader return type!
  return (/* ... */);
}
```

### 5.2 Actions (Mutations with Progressive Enhancement)

```typescript
// app/routes/orders.new.tsx
import { type ActionFunctionArgs, redirect } from '@remix-run/node';
import { Form, useActionData } from '@remix-run/react';

export async function action({ request }: ActionFunctionArgs) {
  const formData = await request.formData();
  const productId = formData.get('productId');
  const quantity = Number(formData.get('quantity'));

  const errors = validate({ productId, quantity });
  if (errors) return json({ errors }, { status: 400 });

  await db.order.create({ data: { productId, quantity } });
  return redirect('/orders'); // PRG pattern built-in
}

export default function NewOrder() {
  const actionData = useActionData<typeof action>();

  return (
    <Form method="post">
      {/* Works without JavaScript! Progressive enhancement. */}
      <input name="productId" required />
      <input name="quantity" type="number" required />
      {actionData?.errors?.quantity && <em>{actionData.errors.quantity}</em>}
      <button type="submit">Create Order</button>
    </Form>
  );
}
```

### 5.3 Progressive Enhancement Philosophy
- Forms work with full-page reloads (no JS required).
- `useFetcher` for in-page mutations without navigation.
- `useRevalidator` to refresh data after mutations.
- Optimistic UI with `useFetcher().state === 'submitting'` and `useFetcher().formData`.

---

## 6. Real-Time Patterns

### 6.1 WebSocket (Persistent Bidirectional)

**Server (Node.js with `ws`):**
```typescript
// apps/api/src/ws.ts
import { WebSocketServer } from 'ws';
import { verifyToken } from './auth';

const wss = new WebSocketServer({ port: 8080 });

// Connection registry: userId → Set<WebSocket>
const connections = new Map<string, Set<WebSocket>>();

wss.on('connection', async (ws, req) => {
  const token = new URL(req.url!, 'http://localhost').searchParams.get('token');
  const user = await verifyToken(token);
  if (!user) { ws.close(4001, 'Unauthorized'); return; }

  // Register connection
  if (!connections.has(user.id)) connections.set(user.id, new Set());
  connections.get(user.id)!.add(ws);

  ws.on('message', (data) => {
    const message = JSON.parse(data.toString());
    if (message.type === 'ping') ws.send(JSON.stringify({ type: 'pong' }));
  });

  ws.on('close', () => {
    connections.get(user.id)?.delete(ws);
    if (connections.get(user.id)?.size === 0) connections.delete(user.id);
  });
});

// Utility to broadcast to a user
export function sendToUser(userId: string, event: string, payload: unknown) {
  const userSockets = connections.get(userId);
  if (!userSockets) return;
  const message = JSON.stringify({ event, payload, timestamp: Date.now() });
  for (const ws of userSockets) ws.send(message);
}
```

**Client (React hook):**
```typescript
// apps/web/src/hooks/useWebSocket.ts
import { useEffect, useRef, useCallback } from 'react';

export function useWebSocket(token: string) {
  const wsRef = useRef<WebSocket | null>(null);
  const handlersRef = useRef<Map<string, Set<(payload: unknown) => void>>>(new Map());

  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:8080?token=${token}`);
    wsRef.current = ws;

    ws.onmessage = (event) => {
      const { event: eventName, payload } = JSON.parse(event.data);
      handlersRef.current.get(eventName)?.forEach(handler => handler(payload));
    };

    // Heartbeat every 30s
    const heartbeat = setInterval(() => {
      if (ws.readyState === WebSocket.OPEN) ws.send(JSON.stringify({ type: 'ping' }));
    }, 30_000);

    // Reconnect with exponential backoff
    ws.onclose = () => { /* reconnect logic */ };

    return () => { clearInterval(heartbeat); ws.close(); };
  }, [token]);

  const subscribe = useCallback((event: string, handler: (payload: unknown) => void) => {
    if (!handlersRef.current.has(event)) handlersRef.current.set(event, new Set());
    handlersRef.current.get(event)!.add(handler);
    return () => { handlersRef.current.get(event)?.delete(handler); };
  }, []);

  return { subscribe };
}
```

### 6.2 Server-Sent Events (SSE) — Server → Client Push

**When to use over WebSocket:** Unidirectional data (notifications, live feeds, progress updates). Simpler, works through most proxies, auto-reconnect built-in.

```typescript
// app/api/events/route.ts (Next.js — stream response)
export async function GET(request: Request) {
  const session = await auth();
  if (!session) return new Response('Unauthorized', { status: 401 });

  const stream = new ReadableStream({
    start(controller) {
      const encoder = new TextEncoder();

      // Send initial connection event
      controller.enqueue(encoder.encode('event: connected\ndata: {}\n\n'));

      // Subscribe to user events
      const unsubscribe = eventBus.subscribe(`user:${session.user.id}`, (event) => {
        controller.enqueue(
          encoder.encode(`event: ${event.type}\ndata: ${JSON.stringify(event.data)}\n\n`)
        );
      });

      // Cleanup on connection close
      request.signal.addEventListener('abort', unsubscribe);
    },
  });

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    },
  });
}
```

**Client consumption:**
```typescript
const eventSource = new EventSource('/api/events');
eventSource.addEventListener('order-shipped', (e) => {
  const order = JSON.parse(e.data);
  showToast(`Order #${order.id} shipped!`);
});
```

### 6.3 Polling — Simplest, Most Compatible

```typescript
// TanStack Query with refetchInterval
const { data } = useQuery({
  queryKey: ['notifications'],
  queryFn: () => fetch('/api/notifications').then(r => r.json()),
  refetchInterval: 15_000, // Poll every 15 seconds
});

// Smart polling: pause when tab is inactive, adjust on error
const { data } = useQuery({
  queryKey: ['status'],
  queryFn: fetchJobStatus,
  refetchInterval: (query) => {
    if (query.state.data?.status === 'completed') return false; // Stop polling
    if (query.state.error) return 30_000; // Slow down on error
    return 5_000; // Normal interval
  },
  refetchIntervalInBackground: false, // Pause when tab inactive
});
```

**Polling vs WebSocket vs SSE decision tree:**
```
Need bidirectional communication?
├── Yes → WebSocket
└── No → Need ultra-low latency?
    ├── Yes → WebSocket
    └── No → Browser compatibility critical?
        ├── Yes → Polling (with TanStack Query)
        └── No → SSE
```

---

## 7. File Upload Patterns

### 7.1 Multipart Form Upload (Simple — < 10MB)

**Server (Next.js API Route):**
```typescript
// app/api/upload/route.ts
export async function POST(request: Request) {
  const session = await auth();
  if (!session) return Response.json({ error: 'Unauthorized' }, { status: 401 });

  const formData = await request.formData();
  const file = formData.get('file') as File;

  if (!file) return Response.json({ error: 'No file' }, { status: 400 });
  if (file.size > 10 * 1024 * 1024) {
    return Response.json({ error: 'File too large (max 10MB)' }, { status: 413 });
  }

  const allowedTypes = ['image/jpeg', 'image/png', 'image/webp', 'application/pdf'];
  if (!allowedTypes.includes(file.type)) {
    return Response.json({ error: 'Invalid file type' }, { status: 415 });
  }

  // Sanitize filename — remove path separators, non-alphanumeric
  const safeName = file.name.replace(/[^a-zA-Z0-9._-]/g, '_');
  const key = `uploads/${session.user.id}/${Date.now()}-${safeName}`;

  // Upload to S3
  const buffer = Buffer.from(await file.arrayBuffer());
  await s3.putObject({
    Bucket: process.env.S3_BUCKET!,
    Key: key,
    Body: buffer,
    ContentType: file.type,
    ServerSideEncryption: 'AES256',
  });

  const url = `https://${process.env.S3_BUCKET}.s3.amazonaws.com/${key}`;
  return Response.json({ url, key });
}
```

### 7.2 Presigned URL Upload (Large Files — > 10MB)

**Why:** Bypasses your server entirely. File goes directly client → S3. Your server only generates a temporary signed URL.

```typescript
// Server: Generate presigned URL
// app/api/upload/presigned/route.ts
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3';
import { getSignedUrl } from '@aws-sdk/s3-request-presigner';

export async function POST(request: Request) {
  const session = await auth();
  const { fileName, fileType, fileSize } = await request.json();

  const key = `uploads/${session.user.id}/${crypto.randomUUID()}-${fileName}`;

  const command = new PutObjectCommand({
    Bucket: process.env.S3_BUCKET,
    Key: key,
    ContentType: fileType,
    ContentLength: fileSize,
    ServerSideEncryption: 'AES256',
  });

  const presignedUrl = await getSignedUrl(s3Client, command, { expiresIn: 300 }); // 5 min

  return Response.json({ presignedUrl, key, publicUrl: getPublicUrl(key) });
}

// Client: Upload directly to S3
async function uploadFile(file: File) {
  // 1. Get presigned URL
  const { presignedUrl, key, publicUrl } = await fetch('/api/upload/presigned', {
    method: 'POST',
    body: JSON.stringify({ fileName: file.name, fileType: file.type, fileSize: file.size }),
  }).then(r => r.json());

  // 2. Upload directly to S3
  await fetch(presignedUrl, {
    method: 'PUT',
    body: file,
    headers: { 'Content-Type': file.type },
  });

  // 3. Notify server of completion
  await fetch('/api/upload/complete', {
    method: 'POST',
    body: JSON.stringify({ key }),
  });

  return publicUrl;
}
```

### 7.3 TUS Protocol (Resumable Uploads)

For very large files (> 100MB) or unreliable connections. TUS allows pausing, resuming, and parallel chunk uploads.

**Server (tus-node-server):**
```typescript
// apps/api/src/tus-server.ts
import { Server } from '@tus/server';
import { S3Store } from '@tus/s3-store';
import express from 'express';

const tusServer = new Server({
  path: '/uploads',
  datastore: new S3Store({
    s3ClientConfig: {
      bucket: process.env.S3_BUCKET,
      region: process.env.AWS_REGION,
      credentials: { /* ... */ },
    },
    partSize: 8 * 1024 * 1024, // 8MB chunks
  }),
  respectForwardedHeaders: true,
  maxSize: 5 * 1024 * 1024 * 1024, // 5GB
});

const app = express();
app.use('/uploads', tusServer.handle.bind(tusServer));
app.listen(4000);
```

**Client (tus-js-client):**
```typescript
import * as tus from 'tus-js-client';

function uploadWithResume(file: File, onProgress: (pct: number) => void) {
  return new Promise<string>((resolve, reject) => {
    const upload = new tus.Upload(file, {
      endpoint: 'https://api.example.com/uploads',
      metadata: { filename: file.name, filetype: file.type },
      headers: { Authorization: `Bearer ${token}` },
      chunkSize: 8 * 1024 * 1024, // 8MB
      onProgress(bytesUploaded, bytesTotal) {
        onProgress(Math.round((bytesUploaded / bytesTotal) * 100));
      },
      onError(error) { reject(error); },
      onSuccess() { resolve(upload.url!); },
    });

    // Check for previous uploads to resume
    upload.findPreviousUploads().then((previousUploads) => {
      if (previousUploads.length > 0) {
        upload.resumeFromPreviousUpload(previousUploads[0]);
      }
      upload.start();
    });
  });
}
```

### 7.4 Upload Pattern Decision Matrix

| Pattern | Max Size | Resumable | Server Load | Complexity |
|---------|----------|-----------|-------------|------------|
| Multipart | < 10MB | No | High (proxies data) | Low |
| Presigned URL | < 5GB | No | Low (URL generation only) | Medium |
| TUS Protocol | Unlimited | Yes | Low (S3 store) | High |
| Chunked Upload | < 100MB | Manual | Medium (assembles chunks) | Medium |

---

## References
- [Turborepo Documentation](https://turbo.build/repo/docs)
- [tRPC Documentation](https://trpc.io/docs)
- [Next.js Server Components](https://nextjs.org/docs/app/building-your-application/rendering/server-components)
- [Remix Data Flow](https://remix.run/docs/en/main/guides/data-loading)
- [TUS Protocol](https://tus.io/protocols/resumable-upload)
- [S3 Presigned URLs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/presigned-url-upload-object.html)
