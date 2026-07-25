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
| 7 | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| 8 | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |

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

### Scale Depth

| Depth | Time | Scope | Artifacts |
|-------|------|-------|-----------|
| **Quick Scan** | ~30s | Verify version, method signature, deprecation status for a known library | One-line citation |
| **Standard Engagement** | ~5-10min | Full DETECT→FETCH→IMPLEMENT→CITE cycle for unfamiliar API | Cited code with version |
| **Deep Dive** | ~30min+ | Major version migration, security-critical path, performance-sensitive integration | Full audit trail: release notes, source code verification, gap analysis |
| **Enterprise Audit** | Multi-session | Framework governance across org: dependency inventory, version consistency audit, citation coverage report, migration planning | Dependency provenance report, framework upgrade runbook |

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
**(STANDARD)**

<!-- COMPRESSED: Full 137 lines extracted to references/core-workflow.md -->

```
DETECT─────────────────────────────────────────────────────────
  │  Identify every framework/library touchpoint in the change
  │  surface: imports, method calls, config objects, type refs
  ▼
...
> 📎 **Full content (137 lines):** [references/core-workflow.md](references/core-workflow.md)

## Best Practices

1. **Citations are source code comments, not directory artifacts.** Every framework API call gets an inline citation: `// [Source: React Docs, v18.3, https://react.dev/reference/useDeferredValue]`. Citations live with the code they verify — not in a separate audit report that nobody reads after merge.

2. **Verify version BEFORE reading docs.** Run `npm list <pkg> --depth=0` (or `pip show`, `go list -m`) and check the result against the docs URL. A Next.js 13 codebase reading Next.js 14 docs will produce silently broken patterns. The mechanical trigger: never navigate to docs without confirming installed version first.

3. **Prefer source code over documentation when they disagree.** When `fetch('/api', { cache: 'no-store' })` behaves differently than docs describe, trust `node -e` behavior and cite the source code at the pinned commit. File a docs issue upstream — but ship based on reality, not documentation.

4. **Frame citations as searchable breadcrumbs.** Format every citation so `grep -r "Source:" src/` produces a complete audit trail of all framework touchpoints. A new team member can audit every external dependency in 30 seconds: `grep -rn "Source:" src/ | sort`.

5. **Treat LLM-generated framework code as Level 0 (untrusted) by default.** Every `import` suggested by an LLM triggers a compulsory verification against Level 1 docs. Never commit LLM code that calls a framework API you haven't personally verified. The cost: 30 seconds of doc lookup per import. The alternative: production incidents from hallucinated APIs.

6. **Continuous spec-code sync via CI.** Add a CI job that checks: (a) every `// [Source:` comment's version matches the installed version in the lockfile, (b) no deprecated methods are called per the framework's changelog, (c) citation URLs resolve (no 404s). Fail the build on mismatch. Living documentation rots without automation.

7. **Spec as the source of truth for implementation decisions.** When a team debate arises ("should we use `useMemo` or `useCallback`?"), the answer comes from the framework's official docs — not from the most senior engineer's preference. Cite the docs as the arbiter: "Per React docs v18.3, `useMemo` caches a computation result; `useCallback` caches a function definition."

8. **Version-pin documentation bookmarks.** Browser bookmarks, team wiki links, and README references to docs must include the version: `https://nextjs.org/docs/app` is ambiguous; `https://nextjs.org/docs/14.2/app` is precise. Bookmark rot is silent — the URL still works, but describes the wrong API.

9. **Generated code from spec must carry version provenance.** When generating code from OpenAPI specs, protobuf definitions, or database schemas, the generated file header must include: source file path, source version/tag, generation timestamp, and generator version. Without this, regenerated code is indistinguishable from manually-edited code.

10. **Run spec validation in CI for every PR.** Schema files (OpenAPI, protobuf, GraphQL, JSON Schema) must pass validation against their specification version: `openapi-generator validate`, `buf breaking`, `graphql-inspector validate`. A malformed schema that passes CI is an undocumented breaking change waiting to happen.
**(QUICK)**

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

## Decision Trees
**(QUICK)**

### Spec-First vs Code-First: When to Write the Spec

```
Starting a new feature
  │
  ├─ Is this feature touching multiple bounded contexts or services?
  │    └─ YES → Write the spec first (OpenAPI for API boundaries, Gherkin for behavior)
  │
  ├─ Is this feature implementing a well-understood pattern (CRUD, simple query)?
  │    └─ YES → Code-first is acceptable. Document with inline comments and a 1-paragraph ADR
  │
  ├─ Will this feature require compliance review (GDPR, SOC2, HIPAA)?
  │    └─ YES → Spec is MANDATORY. The spec IS the compliance artifact
  │
  └─ Is this feature for an external API consumed by third parties?
       └─ YES → Spec-first. Breaking changes to external APIs require versioning and migration plans
```

### Spec Evolution: When to Version vs Backward-Compatibly Extend

```
API change requested
  │
  ├─ Adding a new optional field?
  │    └─ Backward-compatible extension. No version bump. Add to spec, regenerate, ship
  │
  ├─ Adding a new required field?
  │    └─ MINOR version bump. Existing clients continue working. New clients must provide it
  │
  ├─ Changing field semantics (e.g., "id" from integer to UUID string)?
  │    └─ MAJOR version bump. This is a BREAKING CHANGE. Deprecate old endpoint, support both for migration window
  │
  ├─ Removing an endpoint or field?
  │    └─ Deprecation process: (1) Mark deprecated in spec, (2) Add deprecation header in responses, (3) Monitor usage for 2 release cycles, (4) Remove only when usage drops to zero
  │
  └─ Changing auth requirements (e.g., adding required scope)?
       └─ MAJOR. This denies access to previously authorized clients. Coordinate with all consumers before shipping
```

### Spec-Code Sync Failures: Decision Protocol

```
Spec and code disagree
  │
  ├─ Is the spec more recent than the code?
  │    └─ Code is stale → update code to match spec. The spec IS the source of truth
  │
  ├─ Is the code more recent than the spec?
  │    └─ Was the code change intentional?
  │         ├─ YES → The spec is stale. Update spec to match code, then validate spec is still correct
  │         └─ NO  → The code change was accidental or a workaround. Revert code to match spec, address root cause
  │
  ├─ Are spec AND code both recently updated but disagree?
  │    └─ Concurrent work — teams didn't coordinate. Hold an immediate sync: which is the intended behavior? Update the wrong one. Then fix the process gap (no spec review on PR? no CI spec validation?)
  │
  └─ Neither is recent — discrepancy has existed for months?
       └─ Audit both against actual runtime behavior. What does the system ACTUALLY do? That's the de facto spec. Document it formally, then decide what to change.
```

---

## Error Recovery
**(STANDARD)**

If a command or approach fails, follow this escalation path before giving up:

| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|---------------|-------------|
| Tool/command not found | Check installation: `which [tool]` or `[tool] --version`. Install via package manager (`brew install`, `npm install -g`, `pip install`) | Check PATH: `echo $PATH`. Verify the tool binary is in a PATH directory. Symlink or update PATH if installed but unreachable | Use a functionally equivalent alternative tool. If `rg` is unavailable, use `grep -r`. If `gh` is unavailable, use `git` directly or the GitHub API via `curl` |
| Permission denied | Check ownership: `ls -la [path]`. Fix with `chmod` or `sudo` if appropriate. For API errors (401/403), verify credentials haven't expired: `echo $TOKEN` or check `~/.netrc` | Refresh credentials: re-authenticate with the service. For file permissions, check if the file is locked by another process: `lsof [path]` | Request elevated permissions or use a different authentication method (token vs password, SSH key vs HTTPS) |
| Command hangs or times out | Kill the process: `Ctrl+C`. Re-run with a timeout: `timeout 30 [command]` or `gtimeout` on macOS. Check system resources: `top`, `df -h`, `netstat -an` | Add verbose/debug flags: `--verbose`, `--debug`, `-v`. Check logs: `tail -f [logfile]`. Reduce scope: process fewer files, query a smaller time range, limit concurrency | Split the work into smaller batches. Implement a retry loop with exponential backoff (1s, 2s, 4s, 8s). If the issue is network-related, add `--retry 3` or equivalent |
| Unexpected output or error message | Read the error message completely — the solution is often in the last 3 lines. Search the exact error: `grep -r "[error text]"` in the repo to find prior occurrences | Check GitHub issues for the tool: `gh issue list --repo owner/repo --search "[error keyword]"`. Check Stack Overflow | Simplify the approach. If the complex one-liner fails, break it into 3 sequential commands. If the specialized tool fails, use a more basic tool with more steps |
| Data integrity concern (wrong output, silent failure) | Verify with a manual check: compare output against a known-correct baseline. Add assertions: `[command] | grep -q "[expected]" && echo "OK" || echo "FAIL"` | Run the operation on a smaller subset first. Compare checksums: `shasum`, `md5`. Check for silent truncation: `wc -l` before and after | Abort and flag for human review. Do not proceed past data integrity failures — the cost of propagating bad data exceeds the cost of delay |

**Hard failure boundary:** If 3 different approaches all fail, STOP. Do not iterate infinitely. Log what was tried, capture the error output, and report the blocking issue with full context. Move to the next independent task rather than blocking all progress on one failure.

## Error Decoder

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Code compiles but API silently does nothing | Docs describe v3 API; package.json has v2 installed. `deprecatedExport()` exists but is a no-op | Pin versions exactly. Verify installed version (`npm list`) before reading docs. Never trust search engine snippets | Version mismatch between docs and installed package is the #1 source of silent failures. Always confirm the version you read matches the version you run |
| TypeScript types pass but runtime throws `TypeError: x is not a function` | LLM hallucinated an API that doesn't exist. The type assertion `as any` suppressed errors | Never accept LLM-generated framework calls without cross-referencing official docs. Every new `import` is a verification trigger | Framework APIs evolve faster than LLM training data. Hallucinated APIs are the most dangerous because they pass type checking |
| `npm ci` produces different lockfile than CI | `package.json` uses `^` ranges; different `npm` versions resolve differently. Docs describe behavior from a version neither env actually has | Pin all dependencies with exact versions. Add `--save-exact` to `.npmrc`. Add CI check: `npm list --depth=0` vs documented versions | Non-deterministic dependency resolution means non-deterministic behavior. Exact pinning is the only defense |
| CI passes locally, fails on GitHub Actions with identical environment | Different `node_modules` resolution order due to filesystem ordering differences. A transitive dep has a breaking change in a patch version | Use `npm ci` (not `npm install`) everywhere. Commit `package-lock.json`. Use `engines` field to pin Node/npm versions | "Works on my machine" in dependency management means your machine might resolve differently. Identical lockfiles are the only truth |
| Docs describe `async function` but code is synchronous in your version | Framework deprecated the sync API in a minor release. Docs were updated prematurely before the deprecation shipped | Cross-reference release notes for every version between your installed version and the doc version. Test with `node -e` one-liner | Docs can describe the FUTURE, not the PRESENT. Trust behavior over documentation when they disagree |
| Security vulnerability in transitive dep undetected for 6 months | Team used docs from framework v4 security guide, but v5 changed the CSP configuration API entirely. The old config silently became a no-op | Subscribe to framework security advisories. Run `npm audit` in CI with `--audit-level=high`. Re-verify security config after every major version bump | Security documentation for the wrong version is worse than no documentation — it creates a false sense of safety |

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

## Anti-Patterns

### Anti-Pattern: Trusting Search Engine Results for Documentation
**What it looks like:** Developer Googles "Next.js generateStaticParams," clicks the top result, and implements based on whatever version Google indexed — without checking the version selector on the docs page.
**Why it fails:** Google often indexes older or newer versions than what you have installed. The indexed v14 pattern silently fails in your v13 codebase because the API shape changed. No error — just empty results.
**Do this instead:** Never navigate to docs from a search engine. Always start from the framework's official site root, select your version, THEN search within that version's docs. Bookmark version-specific doc roots: `https://nextjs.org/docs/14.2`.

### Anti-Pattern: Community Solutions Without Official Verification
**What it looks like:** A Stack Overflow answer with 500+ upvotes recommends `app.use(multer().single('file'))` in Express. Developer copies it verbatim. Middleware silently corrupts request bodies.
**Why it fails:** Highly-upvoted answers are often for older versions where the API worked. Community solutions accumulate inertia — they stay upvoted long after they become wrong. The upvote count reflects past correctness, not current correctness.
**Do this instead:** Every Stack Overflow or blog-derived solution must be cross-referenced against the current version's official docs before commit. Add `// [Verified against X docs vY.Z]` as proof. If docs contradict the community answer, trust docs.

### Anti-Pattern: LLM-Generated Code Without Verification
**What it looks like:** Copilot/Claude generates `prisma.$transaction([prisma.$queryRaw`...`, ...])`. It compiles, types pass, code ships. Production silently fails because the API doesn't accept that argument shape.
**Why it fails:** LLMs are trained on a corpus that predates API changes. They confidently generate plausible-looking APIs that don't exist or have changed. The code often passes type checks because LLMs also generate type assertions.
**Do this instead:** Every LLM-generated framework call is Level 0 (untrusted) until verified against Level 1 docs. The trigger: any `import` of a new package or unfamiliar API in LLM output triggers compulsory doc verification. 30 seconds of doc lookup prevents production incidents.

### Anti-Pattern: Reading Docs for the Wrong Version
**What it looks like:** Team reads Next.js App Router docs at `nextjs.org/docs/app` showing v14.2 patterns. Their `package.json` has `"next": "^13.4.0"`. They use v14 async signatures that silently return empty in v13.4.
**Why it fails:** Docs sites default to "latest" — which may be newer than your installed version. `^` ranges in `package.json` make the actual resolved version opaque. The mismatch is silent — no error, just incorrect behavior.
**Do this instead:** Before reading any docs page: (1) Run `npm list <pkg>` to confirm installed version. (2) Check the docs URL for a version selector. (3) If docs have no version selector, cross-reference the page's "Last updated" date against the framework's release dates. (4) Pin exact versions in `package.json`.

### Anti-Pattern: No Citation Audit Trail
**What it looks like:** A 50,000-line codebase with zero comments about framework version provenance. Onboarding devs can't tell which version of React patterns are used. Deprecation warnings go unnoticed. Dependencies upgraded without auditing API surface changes.
**Why it fails:** Without citations, every dependency upgrade is a leap of faith. You can't `grep` for which code uses which version's API. Major version migrations require reading the entire codebase to find touchpoints.
**Do this instead:** `grep -rn "Source:" src/` must produce a complete, current audit trail of every framework touchpoint. Citations are the index to your dependency surface — without them, you're navigating blind.

### Anti-Pattern: Docs vs Behavior — Trusting Documentation Over Reality
**What it looks like:** Lodash v4 docs still list `_.pluck()` as available (it was removed in v4.0.0). Developer uses it, code runs without error (returns `undefined`), undercharges customers. Docs say it works; behavior says it doesn't.
**Why it fails:** Documentation is a lagging indicator. Removals, deprecations, and behavioral changes can ship in the package before docs are updated. When docs and behavior disagree, docs are wrong.
**Do this instead:** When docs describe an API but you're uncertain: verify with a REPL one-liner: `node -e "const _ = require('lodash'); console.log(typeof _.pluck)"`. If the result contradicts docs, trust the result and cite the source code at the pinned commit. File a docs issue upstream but ship based on behavior.

### Anti-Pattern: Cherry-Picking Documentation to Justify Pre-Existing Decisions
**What it looks like:** A developer wants to use `useReducer` over `useState` because they prefer the pattern. They find a React docs paragraph that says "useReducer is preferable for complex state logic" and cite it as justification — ignoring the preceding paragraph that says "useState is sufficient for simple cases."
**Why it fails:** Confirmation bias in documentation reading leads to over-engineered solutions. The docs are a balanced resource; quoting selectively turns them into a weapon for winning arguments rather than a tool for making good decisions.
**Do this instead:** When citing docs to support a decision, cite the FULL context — including any caveats, warnings, and alternatives mentioned on the same page. If the docs say "X is good for A but Y is better for B," you must establish that your case is A, not just quote the "X is good" part.

---

## Production Checklist
**(STANDARD)**

Before any framework-dependent code reaches production:

- [ ] Every third-party import has a `// [Source: ...]` citation comment with exact version
- [ ] The installed version (from lockfile) matches the version in ALL citations — run `scripts/verify-citations.sh` in CI
- [ ] No `^` or `~` ranges in production `package.json` dependencies — all pinned to exact versions
- [ ] CI step validates: `npm list --depth=0` output matches documented versions in README/citations
- [ ] Every method call's signature verified against official docs for that exact version
- [ ] Every configuration option confirmed in the official config schema reference
- [ ] Zero deprecated methods or options used (verified against framework changelog/release notes)
- [ ] All Stack Overflow, blog, or community-derived solutions cross-referenced against official docs
- [ ] Any unverifiable behavior flagged with `⚠️ UNVERIFIED` annotation and risk level (HIGH/MEDIUM/LOW)
- [ ] Migration guide consulted and cited for any major version bumps in the dependency tree
- [ ] CI pipeline warns or fails on version mismatches between lockfile and citation comments
- [ ] All citation URLs resolve (no 404s) — `grep -oP 'https?://[^)\s]+' src/ | sort -u | xargs -I{} curl -sI {} | grep "HTTP/2 404"` returns empty
- [ ] LLM-generated framework calls flagged and require manual Level 1 doc verification before merge
- [ ] Generated code from specs (OpenAPI, protobuf) includes source provenance header with version, timestamp, and generator version
- [ ] Spec files (OpenAPI, GraphQL schema, protobuf) pass validation in CI against their specification version

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

Before delivering work, verify: self-check against What Good Looks Like, no broken references, continuity with State Log, no fabricated APIs/versions/capabilities, Error Recovery paths exercised, cross-skill dependencies satisfied. If any fail, revise before delivering.## References

- [Source Hierarchy Guide](../references/source-hierarchy-guide.md) — Detailed source authority hierarchy with trust levels and escalation paths
- [Documentation Fetching Patterns](../references/doc-fetching-patterns.md) — Patterns for programmatic documentation retrieval (curl, gh CLI, web_fetch)
- [Citation Templates](../references/citation-templates.md) — Standardized citation formats for every major framework ecosystem
- [Version Pinning Strategies](../references/version-pinning-strategies.md) — How to pin and verify framework versions against documentation
- [Unverified Claim Detection](../references/unverified-claim-detection.md) — Patterns for identifying claims not backed by official sources
- [Stale Documentation Detection](../references/stale-documentation-detection.md) — Detecting when official docs are out of date with the actual API
- [Framework Migration Checklist](../references/framework-migration-checklist.md) — Source-driven approach to major version migrations
- [Source-Driven Code Review](../references/source-driven-code-review.md) — Code review checklist for source-driven development compliance
