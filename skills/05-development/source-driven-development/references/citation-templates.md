# Citation Templates

## Universal Format

```
[Source: {doc_name}, Section: {section}, URL: {url}, Version: {version}]
```

## React Ecosystem

```tsx
// [Source: React Docs, Section: useCallback, URL: https://react.dev/reference/react/useCallback, Version: v18.3.1]
import { useCallback } from 'react';

// [Source: Next.js Docs, Section: generateStaticParams, URL: https://nextjs.org/docs/app/api-reference/functions/generate-static-params, Version: v14.2.0]
export async function generateStaticParams() { ... }
```

## Python Ecosystem

```python
# [Source: FastAPI Docs, Section: Path Parameters, URL: https://fastapi.tiangolo.com/tutorial/path-params/, Version: v0.115.0]
from fastapi import FastAPI

# [Source: SQLAlchemy Docs, Section: Declarative Mapping, URL: https://docs.sqlalchemy.org/en/20/orm/declarative_styles.html, Version: v2.0.35]
from sqlalchemy.orm import DeclarativeBase
```

## Node.js / Backend

```typescript
// [Source: Prisma Docs, Section: CRUD, URL: https://www.prisma.io/docs/orm/prisma-client/queries/crud, Version: v5.20.0]
const user = await prisma.user.findUnique({ where: { id: 1 } });

// [Source: Express Docs, Section: Routing, URL: https://expressjs.com/en/guide/routing.html, Version: v4.21.0]
app.get('/api/users', usersController.index);
```

## Go Ecosystem

```go
// [Source: Gin Docs, Section: Query Parameters, URL: https://gin-gonic.com/docs/examples/query-and-post-form/, Version: v1.9.1]
import "github.com/gin-gonic/gin"

// [Source: Go Standard Library, Section: net/http, URL: https://pkg.go.dev/net/http@go1.22.0, Version: go1.22.0]
import "net/http"
```

## Rust Ecosystem

```rust
// [Source: Tokio Docs, Section: Spawning, URL: https://docs.rs/tokio/1.40.0/tokio/task/fn.spawn.html, Version: 1.40.0]
use tokio::task;

// [Source: Serde Docs, Section: Derive, URL: https://serde.rs/derive.html, Version: 1.0.210]
use serde::{Serialize, Deserialize};
```

## Unverified Flag Template

```
⚠️ UNVERIFIED: No official source found for {claim}.
  Assuming: {exact assumption}.
  Risk: {LOW|MEDIUM|HIGH|CRITICAL}.
  Recommended: {action to verify}.
```

## Block Citation (Multiple Calls to Same API)

```python
# ═══════════════════════════════════════════════════════════════
# SOURCE: Stripe Python SDK Docs
# Version: v7.0.0 | API Version: 2024-04-10
# URL: https://docs.stripe.com/api
# Sections used: checkout/sessions/create, customers/create, payment_intents/confirm
# ═══════════════════════════════════════════════════════════════
```
