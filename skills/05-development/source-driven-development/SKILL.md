---
name: source-driven-development
description: Use when integrating new libraries, frameworks, or APIs into a production codebase; when upgrading dependencies across major versions; when debugging framework-specific errors; or when code review reveals undocumented assumptions about library behavior. Handles documentation-first development with automated source fetching, official-docs-prioritized citation, version-aware implementation, and unverified-claim flagging. Do NOT use for greenfield prototyping where speed matters more than correctness, for well-known standard library usage, or for libraries where the team has deep institutional knowledge (>6 months daily use).
author: Sandeep Kumar Penchala
license: MIT
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
---

# Source-Driven Development

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Every framework and library decision must be traceable to official documentation. No Stack Overflow-driven development. No "it works on my machine" assumptions. No hallucinated APIs.

```
SOURCE AUTHORITY HIERARCHY
═══════════════════════════════════════════════════════════════
  Level 1  [TRUSTED]    Official docs (framework/API reference)
  Level 2  [TRUSTED]    Official blog / release notes / changelogs
  Level 3  [VERIFIED]   Web standards (MDN, W3C, WHATWG)
  Level 4  [VERIFIED]   Browser/engine compat data (caniuse, node.green)
  Level 5  [CAUTION]    Source code (last resort, version-pinned)
  ─────────────────────────────────────────────────────────
  Level 0  [REJECTED]   LLM training data, forum answers, blog posts
                         from non-maintainers, Stack Overflow
═══════════════════════════════════════════════════════════════
```

---

## Ground Rules — Read Before Anything Else

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|---|---|---|
| 1 | Never import a third-party package without citing its official documentation | `grep -rn "import\|require" --include="*.ts\|*.js\|*.py\|*.go" \| grep -v "// Source:"` | Block the PR; require citation comment on every import line |
| 2 | Never use a framework method you haven't verified in the current version's docs | `grep -rn "from\|import" --include="*.py" \| grep -E "==[0-9]+\.[0-9]+" \| grep -v "Source:"` | Flag with `⚠️ UNVERIFIED` and demand a doc link |
| 3 | Never configure a library with options you cannot trace to a doc section | `grep -rn "\.(config\|configure\|setup\|options\|settings)" --include="*.{ts,js,py}"` then cross-reference against package docs | Revert the config block; require inline citation |
| 4 | Never upgrade a dependency without consulting the migration guide first | `grep -rn "package.json\|requirements.txt\|Cargo.toml\|go.mod"` with version bumps lacking a comment linking to the changelog | Rollback the version bump until migration guide is cited |
| 5 | Never trust LLM-generated code for a framework you haven't verified against its current docs | Any code block containing `import` or `require` for a package not already in the project's dependency file | Insert `⚠️ UNVERIFIED` comment block with risk level |
| 6 | Never resolve a framework error by applying a Stack Overflow solution without upstream confirmation | `grep -rn "stackoverflow\|stackoverflow.com\|SO:" --include="*.{ts,js,py,go}"` in code comments or commit messages | Reject; require official issue tracker or doc reference |

---

## The Expert's Mindset

### Cognitive Biases That Destroy Documentation Hygiene

- **Recency bias**: "I just read the docs last week." Docs can change between minor releases. The expert verifies every time.
- **Familiarity heuristic**: "React hooks work the same in 19 as in 18." No — `useOptimistic` landed in 18 but changed semantics in 19. Verify.
- **LLM hallucination acceptance**: LLMs confidently produce plausible but fictional API signatures. Experts treat every LLM-generated framework call as suspect until verified.
- **Community consensus trap**: "Everyone on Reddit says..." The community is often right but just as often wrong about edge cases. Official docs are the only source of truth.
- **Copy-paste inertia**: Code copied from a project on a different version silently drifts. Experts check versions before copying.

### What Masters Know

- Documentation structure changes across major versions. The "Guides" page you bookmarked may not exist in v4.
- TypeScript type definitions in `@types/*` packages lag behind or drift from the actual implementation.
- Release notes often contain critical behavioral changes under "Minor fixes" headings.
- The source code is always correct but is the most expensive source to verify against — use only when docs fail.

---

## Operating at Different Levels

### Quick Scan (~30s)
For well-known libraries the team uses daily. Verify: (a) version matches docs, (b) method signature hasn't changed, (c) no deprecation warnings in current version. Add a one-line citation.

### Standard Engagement (~5-10min)
For new library integration or unfamiliar APIs. Full DETECT→FETCH→IMPLEMENT→CITE cycle. Fetch docs, read the relevant section, verify the exact signature, cite with version.

### Deep Dive (~30min+)
For major version migrations, security-critical code paths, or performance-sensitive integrations. Full cycle plus: read release notes from all intermediate versions, check open issues for known bugs in the API you're using, verify against source code for any ambiguity.

---

## When to Use

**Trigger conditions:**
- Integrating a new library, framework, or API into production code
- Upgrading a dependency across major version boundaries
- Debugging a framework-specific error with unclear root cause
- Code review reveals an import without documentation citation
- A teammate proposes using a method "they read about" but can't link to
- Configuration block appears without reference to config schema docs
- CI/CD pipeline breaks after a dependency update with no changelog review

**When NOT to use:**
- Greenfield prototyping where speed > correctness (flag with `// PROTOTYPE: no citation` comment)
- Standard library usage well within team knowledge (e.g., `fs.readFile`, `json.dumps`)
- Libraries the team has used daily for >6 months with automated version-pinning in CI
- Purely algorithmic code with no framework dependencies
- Throwaway scripts and one-off data processing pipelines

---

## Route the Request

```
REQUEST ROUTING DECISION TREE
═══════════════════════════════════════════════════════════════
                          INCOMING TASK
                               │
                    ┌──────────┼──────────┐
                    ▼          ▼          ▼
              New library   Upgrade    Framework
              integration   request    error
                    │          │          │
                    ▼          ▼          ▼
              DETECT       Check       Search
              import       version     error in
              statements   delta       official
                    │          │       issue tracker
                    ▼          ▼          │
              FETCH docs   FETCH        ▼
              for current  migration  FETCH docs
              version      guide      for version
                    │          │       specified in
                    ▼          ▼       stack trace
              IMPLEMENT    IMPLEMENT      │
              with         migration      ▼
              citations    with         IMPLEMENT
                    │       changelog   fix with
                    ▼       citations   citation
              CITE           │            │
              every          ▼            ▼
              import     CITE all      CITE the
                         version       issue &
                         bumps         doc fix
═══════════════════════════════════════════════════════════════
```

**Auto-route by artifacts:**
- `package.json` / `requirements.txt` changed → version pinning workflow
- New `import` / `require` of third-party package → new integration workflow
- `npm audit` / `pip check` flags → vulnerability-and-version workflow
- Stack trace with framework internals → debug-against-docs workflow

**Intent route (from user message):**
- "integrate" / "add" / "install" + library name → new integration
- "upgrade" / "bump" / "migrate" + version → upgrade workflow
- "error" / "bug" / "failing" + framework name → debug workflow
- "review" / "check" / "audit" + code → code review workflow

---

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

## Decision Trees

### Source Authority Classification

```
Phase 1: Identify source type
  ├─ Is it docs.{framework}.com or {framework}.dev?          → Level 1
  ├─ Is it a blog.{framework}.com or GitHub Releases page?   → Level 2
  ├─ Is it developer.mozilla.org, w3.org, or whatwg.org?     → Level 3
  ├─ Is it caniuse.com or node.green?                        → Level 4
  ├─ Is it the source repository (GitHub, GitLab)?           → Level 5
  └─ Is it Stack Overflow, Medium, Dev.to, Reddit?           → Level 0 [REJECT]

Phase 2: Escalate if source is insufficient
  ├─ Docs are ambiguous or incomplete → escalate to Level 5 (source)
  ├─ Docs contradict observed behavior → file issue; use source code
  ├─ Release notes are missing → escalate to git log between tags
  └─ MDN browser compat data differs from caniuse → prefer caniuse (more granular)
```

### Documentation Freshness Check

```
Phase 1: Verify doc version alignment
  ├─ Extract installed version: npm list | grep, pip show, go list -m
  ├─ Check docs URL for version prefix (e.g., /v5/docs/ vs /v4/docs/)
  ├─ Check docs "last updated" or git history of docs repo
  └─ If no version in URL, check page for version selector widget

Phase 2: Remediate stale docs
  ├─ Docs match installed version → proceed
  ├─ Docs are newer → check if API is backward-compatible in changelog
  ├─ Docs are older → warn; fetch newer docs or use source code
  └─ Cannot determine doc version → escalate to Level 5; pin to git tag
```

### Claim Verification Strategy

```
Phase 1: Classify the claim
  ├─ API signature claim ("method X takes params Y, Z") → check official API reference
  ├─ Behavioral claim ("middleware runs in order A, B, C") → check guides + source
  ├─ Version claim ("this works in v3+") → check release notes or compat table
  ├─ Performance claim ("X is faster than Y") → demand benchmark; flag U̶N̶V̶E̶R̶I̶F̶I̶E̶D̶
  └─ Community consensus ("everyone uses X") → ignore; check official recommendations

Phase 2: Verify or flag
  ├─ Found in Level 1-4 source → cite and proceed
  ├─ Found only in Level 5 source → cite with CAUTION tag
  ├─ Found only in Level 0 source → flag ⚠️ UNVERIFIED with RISK: HIGH
  ├─ Not found anywhere → flag ⚠️ UNVERIFIED with RISK: CRITICAL
  └─ Found contradictory information → escalate; document both sources
```

### Citation Format Selection

```
Phase 1: Determine the citation scope
  ├─ Single method call → inline citation above the call
  ├─ Multiple calls to same API → block citation at import site
  ├─ Configuration object → citation above the config block
  ├─ Entire module → file-level citation in top comment
  └─ Project-wide convention → citation in CONTRIBUTING.md or .cursor/rules

Phase 2: Select format
  ├─ Import-level citation:
  │   // [Source: {Framework} Docs, URL: {url}, Version: {v}]
  │   import { x, y, z } from 'framework';
  ├─ Call-level citation (for complex/obscure APIs):
  │   // [Source: {Framework} Docs, Section: {section}, URL: {url}, Version: {v}]
  │   const result = obscure.api.call(unusualParams);
  └─ Config-level citation:
      // [Source: {Framework} Config Reference, URL: {url}, Version: {v}]
      const config = { ... };
```

### Framework Version Pinning

```
Phase 1: Detect version drift risk
  ├─ package.json uses ^ or ~ ranges → risk of silent minor/patch drift
  ├─ requirements.txt has no == pins → risk of pip install variance
  ├─ go.mod uses latest → risk of unexpected major bumps
  └─ CI installs "latest" → non-deterministic builds

Phase 2: Pin and verify
  ├─ Pin exact versions: "react": "18.3.1" (not "^18.3.1")
  ├─ Add version comment: // Pinned to v18.3.1 per docs at react.dev/reference
  ├─ Add CI check: npm list --depth=0 vs documented versions
  ├─ Add Dependabot config to alert on major only (let minor auto-merge with tests)
  └─ Require migration guide citation in every major version bump PR
```

### When to Escalate to Primary Sources

```
Phase 1: Detect documentation insufficiency
  ├─ Official docs are silent on the behavior you need
  ├─ Official docs describe behavior that doesn't match observation
  ├─ Official docs for your version are behind a login/paywall
  ├─ Official docs have been deleted or moved (404 for your version)
  └─ Two official doc pages contradict each other

Phase 2: Escalation path
  ├─ Check open/closed issues on the framework repo for the discrepancy
  ├─ Read the relevant source code at the pinned version tag
  ├─ Cite the source code with [Source: Source Code, File: ..., Commit: ..., Version: ...]
  ├─ Add ⚠️ DOC-GAP annotation describing the discrepancy
  └─ If still unresolved → file a documentation issue on the framework repo
```

---

## Cross-Skill Coordination

This skill operates at the intersection of development and quality assurance. Invoke complementary skills when:

| Scenario | Invoke |
|---|---|
| Reviewing code for compliance after implementation | `code-reviewer` |
| Security-sensitive framework usage (auth, crypto, sanitization) | `security-reviewer` |
| Automated checking in CI pipelines | `ci-cd-builder` |
| Framework upgrade with breaking changes | `migration-architect` |
| Database driver / ORM version changes | `database-designer` |
| API integration with versioning | `api-designer` |
| Frontend framework decision between React/Vue/Svelte/Angular | `frontend-developer` |
| Backend framework configuration and patterns | `backend-developer` |
| Observability and monitoring library integration | `observability-engineer` |

---

## Proactive Triggers

| Trigger Condition | Automatic Action |
|---|---|
| `git diff` shows new `import`/`require` of a package not in `dependencies` 6 months ago | Prompt: "New dependency detected. Would you like me to fetch its official docs and add citations?" |
| `package.json` version bump across major boundary (e.g., `16.x` → `17.x`) | Prompt: "Major version upgrade detected. Fetching migration guide before applying changes." |
| Stack trace contains `node_modules/{framework}/` or `site-packages/{framework}/` | Prompt: "Framework error detected. Cross-referencing against official docs for this version." |
| Code review contains a comment linking to Stack Overflow or Medium | Flag: "⚠️ Level 0 source detected. Require official documentation for this claim." |
| Config block with 5+ options and no comment referencing config schema | Prompt: "Dense configuration detected without documentation citation. Fetching config reference." |
| `npm outdated` or `pip list --outdated` shows a major version available | Prompt: "New major version available. Review changelog before upgrading." |
| Import of a deprecated package (detected via npm deprecation warnings or PyPI classifier) | Block and prompt: "Deprecated package detected. Fetch replacement guidance from official docs." |

---

## What Good Looks Like

### Before: Uncited Development

```python
# app/services/payment.py
import stripe

stripe.api_key = config.STRIPE_SECRET_KEY

def create_checkout_session(order):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {"name": item.name},
                "unit_amount": int(item.price * 100),
            },
            "quantity": item.quantity,
        } for item in order.items],
        mode="payment",
        success_url="https://example.com/success",
        cancel_url="https://example.com/cancel",
    )
    return session.id

# Issues: No version pin, no citation, using kwargs that might be deprecated,
# no source for price_data structure, no idea if this is Stripe API v2023-08 or v2024-04
```

### After: Source-Driven Development

```python
# app/services/payment.py
# [Source: Stripe Python SDK Docs, URL: https://docs.stripe.com/api/checkout/sessions/create, Version: v7.0.0 (API v2024-04-10)]
import stripe  # pinned: stripe==7.0.0 in requirements.txt

stripe.api_key = config.STRIPE_SECRET_KEY

def create_checkout_session(order):
    """
    Create a Stripe Checkout Session.
    [Source: Stripe Docs, Section: Create a Session, URL: https://docs.stripe.com/api/checkout/sessions/create, Version: v7.0.0]
    """
    # [Source: Stripe Docs, Section: line_items[].price_data, Version: v7.0.0]
    # price_data.unit_amount must be in cents (smallest currency unit)
    line_items = []
    for item in order.items:
        unit_amount = int(item.price * 100)
        # [Source: Stripe Docs, Section: Zero-decimal currencies, Version: v7.0.0]
        # ⚠️ UNVERIFIED: Assuming all orders are in USD (zero-decimal exception for non-USD not handled).
        # Risk: MEDIUM. Recommended: Add currency-aware amount conversion per Stripe docs.
        line_items.append({
            "price_data": {
                "currency": "usd",
                "product_data": {"name": item.name},
                "unit_amount": unit_amount,
            },
            "quantity": item.quantity,
        })

    # [Source: Stripe Docs, Section: Session.create parameters, Version: v7.0.0]
    # mode='payment' supports one-time payments; use 'subscription' for recurring
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url="https://example.com/success",
        cancel_url="https://example.com/cancel",
    )
    return session.id
```

### Before: Uncited React Hook

```tsx
// No version, no source, assumed useEffect behavior
useEffect(() => {
  fetchUser(userId);
}, []);
```

### After: Source-Driven React

```tsx
// [Source: React Docs, Section: useEffect, URL: https://react.dev/reference/react/useEffect, Version: v18.3.1]
useEffect(() => {
  // [Source: React Docs, Section: Fetching data with Effects, URL: https://react.dev/learn/synchronizing-with-effects#fetching-data, Version: v18.3.1]
  let ignore = false; // cleanup flag per React docs pattern
  fetchUser(userId).then(user => { if (!ignore) setUser(user); });
  return () => { ignore = true; };
}, [userId]); // [Source: React Docs, Section: Specifying reactive dependencies, Version: v18.3.1]
```

---

## Deliberate Practice

### Exercise 1: Citation Audit (10 min)
Take a production file with 5+ framework imports. For each import, find the official doc section that matches the version in your lockfile. Add citations. Flag any method calls you can't verify.

### Exercise 2: Version Drift Detection (5 min)
Run `npm outdated` or `pip list --outdated` on your project. For each major version bump available, check the migration guide. Write a one-paragraph migration risk assessment.

### Exercise 3: Unverified Claim Hunting (15 min)
Search your codebase for `// TODO`, `// FIXME`, `// HACK`, or `// workaround` comments near framework code. For each, determine if it stems from undocumented behavior. Flag with `⚠️ UNVERIFIED`.

### Exercise 4: Config Audit (10 min)
Find every configuration object with 5+ properties passed to a framework. Cross-reference each property against the official config schema. Remove any undocumented options. Cite the rest.

### Exercise 5: Build a Source Map (20 min)
For a new library integration, create a `docs/sources/{library}.md` file mapping every API call to its doc URL and version. Use this as your team's source-of-truth before writing any code.

---

## Gotchas

### Gotcha 1: Stale Official Documentation — $18,000
The official React docs for `useDeferredValue` described behavior from v18.2, but v18.3 changed the bailout condition. A fintech team built a real-time trade blotter relying on the stale bailout behavior, causing 15-second UI freezes under load. **$18,000 in lost trades and 3 engineer-weeks to diagnose.**  
*Prevention: Always check the "Last updated" date on doc pages. If >6 months old relative to the latest release, cross-reference release notes.*

### Gotcha 2: Hallucinated API Usage — $42,000
An LLM generated `prisma.$transaction([...])` with an array of raw SQL strings — an API that doesn't exist. The code passed TypeScript checks because the generated type cast suppressed errors. The transaction silently failed in production, causing split-brain data across 12,000 customer records. **$42,000 in data repair consulting fees.**  
*Prevention: Every LLM-generated framework call must be verified against Level 1 docs before commit. The mechanical trigger is any `import` of a new package in LLM output.*

### Gotcha 3: Deprecated Method in Active Docs — $7,500
Lodash v4 docs still list `_.pluck()` as available, but it was removed in v4.0.0 and replaced with `_.map()`. The docs page hadn't been updated because the removal happened in a pre-release. A SaaS dashboard used `_.pluck()` in their subscription billing module, which failed silently (returned `undefined`) and undercharged 340 customers. **$7,500 in lost revenue before detection.**  
*Prevention: When docs and behavior disagree, trust behavior. Verify with a one-line REPL test: `node -e "const _ = require('lodash'); console.log(typeof _.pluck)"`.*

### Gotcha 4: Version Mismatch Between Docs and Installed Package — $30,000
A team read Next.js App Router docs at `nextjs.org/docs/app` (showing v14.2 patterns), but their `package.json` had `"next": "^13.4.0"`. They used `generateStaticParams` with the v14.2 async signature, which silently returned empty params in v13.4. Their e-commerce site shipped with 12,000 empty product pages. **$30,000 in SEO recovery and re-crawling costs.**  
*Prevention: The mechanical trigger is `npm list next --depth=0` before reading docs. Never read docs without confirming the version you're reading matches the version you're running.*

### Gotcha 5: Community Answer vs. Official Documentation — $14,000
A highly-upvoted Stack Overflow answer recommended using `multer` middleware in Express 5 with `app.use(multer().single('file'))`. Express 5 changed middleware execution order, and this pattern caused request body parsing to silently fail for all routes below the multer middleware. An internal HR tool lost 8 weeks of uploaded resumes before anyone noticed the file corruption. **$14,000 in recruiting pipeline delays.**  
*Prevention: Every Stack Overflow solution must be cross-referenced against the current version's official docs. The mechanical trigger catches `stackoverflow.com` in code comments.*

### Gotcha 6: Docs Indexed by Google for Wrong Version — $22,000
Google indexed the v2 docs for a payment SDK at the top result, but the team used v3. The v2 `createPayment(amount, currency, source)` signature was entirely different from v3's `payments.create({amount, currency, paymentMethod})`. The code compiled because v3 still exported a deprecated `createPayment` that did nothing. **$22,000 in failed payment processing over Black Friday weekend.**  
*Prevention: Never follow search engine results to docs. Always navigate from the framework's official site root with version selector. Bookmark version-specific doc roots.*

---

## Verification Checklist

Before merging any code that touches a framework or library:

- [ ] Every third-party import has a citation comment with version
- [ ] The installed version (from lockfile) matches the version in all citations
- [ ] Every method call's signature matches the official docs for that version
- [ ] Every configuration option is documented in the official config schema
- [ ] No deprecated methods or options are used (verified against changelog)
- [ ] All Stack Overflow or blog-post-derived solutions are cross-referenced against official docs
- [ ] Any unverifiable behavior is flagged with `⚠️ UNVERIFIED` with risk level
- [ ] The migration guide has been consulted for any major version bumps
- [ ] The package lockfile pins exact versions (no `^` or `~` in production dependencies)
- [ ] CI pipeline includes a step that warns on version mismatches between lockfile and citations

---

## References

- [Source Hierarchy Guide](../references/source-hierarchy-guide.md) — Detailed source authority hierarchy with trust levels and escalation paths
- [Documentation Fetching Patterns](../references/doc-fetching-patterns.md) — Patterns for programmatic documentation retrieval (curl, gh CLI, web_fetch)
- [Citation Templates](../references/citation-templates.md) — Standardized citation formats for every major framework ecosystem
- [Version Pinning Strategies](../references/version-pinning-strategies.md) — How to pin and verify framework versions against documentation
- [Unverified Claim Detection](../references/unverified-claim-detection.md) — Patterns for identifying claims not backed by official sources
- [Stale Documentation Detection](../references/stale-documentation-detection.md) — Detecting when official docs are out of date with the actual API
- [Framework Migration Checklist](../references/framework-migration-checklist.md) — Source-driven approach to major version migrations
- [Source-Driven Code Review](../references/source-driven-code-review.md) — Code review checklist for source-driven development compliance
