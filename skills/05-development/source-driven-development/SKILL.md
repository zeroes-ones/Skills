---
name: source-driven-development
description: Use when integrating new libraries, frameworks, or APIs into a production
  codebase; when upgrading dependencies across major versions; when debugging framework-specific
  errors; or when code review reveals undocumented assumptions about library behavior.
  Handles documentation-first development with automated source fetching, official-docs-prioritized
  citation, version-aware implementation, and unverified-claim flagging. Do NOT use
  for greenfield prototyping where speed matters more than correctness, for well-known
  standard library usage, or for libraries where the team has deep institutional knowledge
  (>6 months daily use).
author: Sandeep Kumar Penchala
license: MIT
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
chain:
  consumes_from:
  - backend-developer
  feeds_into:
  - code-reviewer
  - qa-engineer
---
# Source-Driven Development

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

## Anti-Rationalization — No Excuses

| Rationalization | Reality |
|---|---:|
| "I've used React for 5 years — I know the APIs. Checking docs for every import is a waste of time." | React hooks changed semantics between v18 and v19. Express middleware patterns shifted in v5. The API you memorized in 2022 may be deprecated, have different edge-case behavior, or not exist at all. Familiarity is the #1 source of framework bugs — you're coding against a version in your head, not the version in your `package.json`. |
| "The LLM knows the latest version — it was trained recently." | LLMs confidently hallucinate API signatures that never existed, mixing methods from different major versions into plausible-but-wrong code. Your model doesn't know your project's exact dependency versions. Every LLM-generated framework call is a guess until verified against the current docs. |
| "Everyone on Stack Overflow says this is the fix — 500 upvotes can't be wrong." | Stack Overflow answers are version-frozen at the moment of posting. The accepted answer for React 16 patterns may be actively harmful in React 19. Community consensus is often right about common cases and catastrophically wrong about edge cases. Official docs and issue trackers are the only sources of truth. |
| "I'll check the docs if something breaks — let's not slow down for citation comments." | When something breaks 6 months later during a dependency upgrade, the engineer debugging it has no idea which version you verified against, which doc section you referenced, or whether you checked at all. A one-line `// Source:` comment takes 5 seconds to write and saves hours of forensic archaeology. |
| "This config block is identical to my last project — I can copy-paste without re-reading the docs." | Configuration schemas change between major versions. Options get renamed, defaults shift, and deprecated settings silently break. Copy-paste from a project on a different version is code you haven't verified. The 2 minutes you save is the 2 hours someone else spends debugging a config that "should work." |

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

- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
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
<!-- COMPRESSED: Full 137 lines extracted to references/core-workflow.md -->

```
DETECT─────────────────────────────────────────────────────────
  │  Identify every framework/library touchpoint in the change
  │  surface: imports, method calls, config objects, type refs
  ▼
...
> 📎 **Full content (137 lines):** [references/core-workflow.md](references/core-workflow.md)

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

## Error Recovery

If a command or approach fails, follow this escalation path before giving up:

| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|---------------|-------------|
| Tool/command not found | Check installation: `which [tool]` or `[tool] --version`. Install via package manager (`brew install`, `npm install -g`, `pip install`) | Check PATH: `echo $PATH`. Verify the tool binary is in a PATH directory. Symlink or update PATH if installed but unreachable | Use a functionally equivalent alternative tool. If `rg` is unavailable, use `grep -r`. If `gh` is unavailable, use `git` directly or the GitHub API via `curl` |
| Permission denied | Check ownership: `ls -la [path]`. Fix with `chmod` or `sudo` if appropriate. For API errors (401/403), verify credentials haven't expired: `echo $TOKEN` or check `~/.netrc` | Refresh credentials: re-authenticate with the service. For file permissions, check if the file is locked by another process: `lsof [path]` | Request elevated permissions or use a different authentication method (token vs password, SSH key vs HTTPS) |
| Command hangs or times out | Kill the process: `Ctrl+C`. Re-run with a timeout: `timeout 30 [command]` or `gtimeout` on macOS. Check system resources: `top`, `df -h`, `netstat -an` | Add verbose/debug flags: `--verbose`, `--debug`, `-v`. Check logs: `tail -f [logfile]`. Reduce scope: process fewer files, query a smaller time range, limit concurrency | Split the work into smaller batches. Implement a retry loop with exponential backoff (1s, 2s, 4s, 8s). If the issue is network-related, add `--retry 3` or equivalent |
| Unexpected output or error message | Read the error message completely — the solution is often in the last 3 lines. Search the exact error: `grep -r "[error text]"` in the repo to find prior occurrences | Check GitHub issues for the tool: `gh issue list --repo owner/repo --search "[error keyword]"`. Check Stack Overflow | Simplify the approach. If the complex one-liner fails, break it into 3 sequential commands. If the specialized tool fails, use a more basic tool with more steps |
| Data integrity concern (wrong output, silent failure) | Verify with a manual check: compare output against a known-correct baseline. Add assertions: `[command] | grep -q "[expected]" && echo "OK" || echo "FAIL"` | Run the operation on a smaller subset first. Compare checksums: `shasum`, `md5`. Check for silent truncation: `wc -l` before and after | Abort and flag for human review. Do not proceed past data integrity failures — the cost of propagating bad data exceeds the cost of delay |

**Hard failure boundary:** If 3 different approaches all fail, STOP. Do not iterate infinitely. Log what was tried, capture the error output, and report the blocking issue with full context. Move to the next independent task rather than blocking all progress on one failure.

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

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `system-architect` | Architecture decisions, technology constraints, system boundaries | Before implementing features that cross system boundaries |
| `api-designer` | API contracts, versioning strategy, rate limiting, error handling | Before building API-consuming code |

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

## State Log

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.

### How the State Log Works
<!-- AGENT: Read this before starting work, update after each phase -->

1. **On session start:** Check `.copilot/session-state/decision-ledger.json` for any prior decisions relevant to this domain. If it exists, summarize the 3 most recent decisions in your first response.
2. **After each major decision:** Append to the ledger:
   ```json
   {
     "timestamp": "ISO-8601",
     "skill": "source-driven-development",
     "phase": "Phase 3: Implementation",
     "decision": "What was decided",
     "rationale": "Why this choice over alternatives",
     "constraints": ["constraint-1", "constraint-2"],
     "alternatives_considered": ["alt-1", "alt-2"],
     "reversible": true
   }
   ```
3. **Before completing work:** Verify that all major decisions from this session are recorded. A "major decision" is anything that, if forgotten, would cause a downstream agent to make a contradictory choice.
4. **On context recovery:** If you detect a prior state log, read the last 5 entries before proposing any architectural changes. Cite the prior decisions you're building on.

### State Log Schema

| Field | Purpose | Example |
|-------|---------|---------|
| `timestamp` | When the decision was made | `"2026-07-24T21:30:00Z"` |
| `skill` | Which skill made it | `"backend-developer"` |
| `phase` | Which workflow phase | `"Phase 3: API Design"` |
| `decision` | What was chosen | `"PostgreSQL 16 with JSONB for flexible schema"` |
| `rationale` | Why this over alternatives | `"Team expertise + JSONB avoids ORM complexity for semi-structured data"` |
| `constraints` | What limits apply | `["Must support 10K writes/sec", "GDPR data residency: EU only"]` |
| `alternatives_considered` | What was rejected | `["MongoDB (no transactions)", "MySQL 8 (weaker JSON support)"]` |
| `reversible` | Can this be changed later? | `true` (migration possible) or `false` (irreversible choice) |

### Anti-Drift Check
<!-- AGENT: Run this check at the start of each new phase -->

Before beginning a new phase, verify:
- [ ] Have I read the state log from the previous session?
- [ ] Do any prior decisions constrain what I'm about to do?
- [ ] Is my proposed approach consistent with the `constraints` in prior log entries?
- [ ] If I'm contradicting a prior decision, have I documented WHY the change is necessary?

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

## Verification Guardrails

Before delivering work, the agent must verify:

- [ ] **Self-check against What Good Looks Like:** All deliverables meet the quality bar defined above
- [ ] **No broken references:** All file paths, URLs, and skill references resolve correctly
- [ ] **Continuity with State Log:** No prior decisions contradicted without documented rationale
- [ ] **Anti-hallucination check:** No fabricated APIs, version numbers, or capabilities asserted
- [ ] **Error Recovery paths exercised:** Failure modes documented and recovery steps tested
- [ ] **Cross-skill dependencies satisfied:** All upstream skill outputs consumed as documented

If any checkbox fails, revise before delivering. When all pass, add to the state log.

## References

- [Source Hierarchy Guide](../references/source-hierarchy-guide.md) — Detailed source authority hierarchy with trust levels and escalation paths
- [Documentation Fetching Patterns](../references/doc-fetching-patterns.md) — Patterns for programmatic documentation retrieval (curl, gh CLI, web_fetch)
- [Citation Templates](../references/citation-templates.md) — Standardized citation formats for every major framework ecosystem
- [Version Pinning Strategies](../references/version-pinning-strategies.md) — How to pin and verify framework versions against documentation
- [Unverified Claim Detection](../references/unverified-claim-detection.md) — Patterns for identifying claims not backed by official sources
- [Stale Documentation Detection](../references/stale-documentation-detection.md) — Detecting when official docs are out of date with the actual API
- [Framework Migration Checklist](../references/framework-migration-checklist.md) — Source-driven approach to major version migrations
- [Source-Driven Code Review](../references/source-driven-code-review.md) — Code review checklist for source-driven development compliance
