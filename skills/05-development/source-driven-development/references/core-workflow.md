## Core Workflow

```
DETECT─────────────────────────────────────────────────────────
  │  Identify every framework/library touchpoint in the change
  │  surface: imports, method calls, config objects, type refs
  ▼
FETCH──────────────────────────────────────────────────────────
  │  Retrieve official documentation for the EXACT version
  │  in use. If version is unstated, fetch latest.
  ▼
IMPLEMENT──────────────────────────────────────────────────────
  │  Write code that exactly matches documented signatures,
  │  options, and return types. No creative interpretation.
  ▼
CITE───────────────────────────────────────────────────────────
     Annotate every framework call with its documentation source
```

### Phase 1: DETECT

Identify every framework touchpoint in the code being written or reviewed.

```python
# Mechanical detection — run these before committing:
# Find all third-party imports not in the standard library:
grep -rn "^import\|^from" --include="*.py" | grep -v "Source:"

# Find all require() calls in JS/TS:
grep -rn "require(" --include="*.{js,ts}" | grep -v "Source:"

# Find all Go external imports:
grep -rn '"github.com\|"go.' --include="*.go" | grep -v "Source:"
```

**Detection checklist:**
- [ ] Every `import` / `require` / `use` statement for third-party packages
- [ ] Every method call on a framework object
- [ ] Every configuration object passed to a framework constructor
- [ ] Every type annotation that references a framework type
- [ ] Every decorator / annotation provided by a framework
- [ ] Every middleware / plugin registration

### Phase 2: FETCH

Retrieve authoritative documentation for the detected framework touchpoints.

**Source fetching patterns:**

```bash
# Pattern A: Fetch official docs page via curl (when docs are static/SSR)
curl -sL "https://docs.example.com/api/v2/users/create" | head -200

# Pattern B: Fetch from GitHub source (last resort, Level 5)
gh api repos/owner/repo/contents/src/api/users.ts --jq '.content' | base64 -d | head -100

# Pattern C: Fetch caniuse data for browser APIs
curl -sL "https://api.caniuse.com/v2/feature/intersection-observer"

# Pattern D: Node.js version compatibility
curl -sL "https://node.green/#ES2023-array-find-from-last"

# Pattern E: Web standards reference
# Use web_fetch tool: web_fetch("https://developer.mozilla.org/en-US/docs/Web/API/fetch")
```

**Version pinning during fetch:**
```bash
# Always retrieve the version you're actually using:
npm list <package> --depth=0 2>/dev/null | grep <package>
pip show <package> 2>/dev/null | grep Version
go list -m <module> 2>/dev/null
```

### Phase 3: IMPLEMENT

Write code that EXACTLY matches the documented API. Copy-paste signatures from docs when possible.

```typescript
// ❌ UNCITED — no source, no version, no verification
import { useQuery } from '@tanstack/react-query';
const { data } = useQuery('todos', fetchTodos, { staleTime: 5000 });

// ✅ SOURCE-DRIVEN — cited, version-pinned, signature-verified
// [Source: TanStack Query Docs, Section: useQuery, URL: https://tanstack.com/query/v5/docs/reference/useQuery, Version: v5.59.0]
import { useQuery } from '@tanstack/react-query';
const { data } = useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
  staleTime: 5 * 1000, // documented default: 0ms; set for freshness control
});
```

```python
# ❌ UNCITED — no source, using positional args that changed in v2
from openai import OpenAI
client = OpenAI()
response = client.chat.completions.create("gpt-4", [{"role": "user", "content": "hi"}])

# ✅ SOURCE-DRIVEN — keyword args match v1.55.0 docs exactly
# [Source: OpenAI Python SDK, Section: chat.completions.create, URL: https://platform.openai.com/docs/api-reference/chat/create, Version: v1.55.0]
from openai import OpenAI
client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "hi"}],
)
```

### Phase 4: CITE

Use the standard citation format for every framework call:

```
[Source: {doc_name}, Section: {section}, URL: {url}, Version: {version}]
```

**Citation format by level:**

| Source Level | Citation Format | Example |
|---|---|---|
| Level 1 | `[Source: {Framework} Docs, Section: {section}, URL: {url}, Version: {v}]` | `[Source: React Docs, Section: useRef, URL: https://react.dev/reference/react/useRef, Version: v18.3.1]` |
| Level 2 | `[Source: {Project} Blog/Release Notes, Version: {v}, URL: {url}]` | `[Source: Next.js Blog, Version: v14.2.0, URL: https://nextjs.org/blog/next-14-2]` |
| Level 3 | `[Source: MDN, Section: {section}, URL: {url}]` | `[Source: MDN, Section: fetch(), URL: https://developer.mozilla.org/en-US/docs/Web/API/fetch]` |
| Level 4 | `[Source: caniuse/node.green, Feature: {name}, URL: {url}]` | `[Source: caniuse, Feature: css-grid, URL: https://caniuse.com/css-grid]` |
| Level 5 | `[Source: Source Code, File: {path}, Line: {line}, Commit: {sha}, Version: {tag}]` | `[Source: Source Code, File: src/router.ts, Line: 142, Commit: a1b2c3d, Version: v4.0.0]` |

**Unverified claim flagging:**
```
⚠️ UNVERIFIED: No official source found for {claim}.
  Assuming: {exact assumption being made}.
  Risk: {LOW|MEDIUM|HIGH|CRITICAL}.
  Recommended: {action to verify}.
```

---
