---
name: mock-data-sync
description: >
  Use when backend API schemas change (Pydantic, database columns) and mobile
  test fixtures must stay in sync; when TypeScript types drift from mock
  factories; when setting up CI pipelines to catch mock-data drift
  automatically; or when configuring OpenAPI generator for automated type
  generation. Handles backend schema change propagation to mock factories,
  mobile type-to-fixture validation with tsc, OpenAPI generator configuration
  for automated type generation, and CI validation pipeline setup for
  mock-data sync checks. Do NOT use for general API design, database schema
  design, or end-to-end test authoring outside the mock-fixture context.
author: Sandeep Kumar Penchala
license: MIT
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
chain:
  consumes_from:
  - backend-developer
  - api-designer
  feeds_into:
  - mobile-developer
  - qa-engineer
  - ci-cd-builder
---

# Mock-Data Sync

> **Portability target:** Spec-level (runs on Claude Code, Copilot CLI, Cursor,
> OpenClaw, Gemini CLI). No vendor-specific frontmatter fields.

Keep mobile test fixtures in sync with backend API schemas and TypeScript types
in a monorepo. When a database column changes, the Pydantic schema shifts, the
mobile `lib/types.ts` is updated — and mock factories must follow automatically.
This skill enforces that chain.

## Anti-Rationalization — No Excuses

| Rationalization | Reality |
|---|---|
| "The mock factory compiled last week — it must still be valid." | TypeScript types change with every backend PR. A field renamed from `user_name` to `display_name` compiles silently in the mock factory (the old field just becomes an extra property). The mock still passes tsc but returns data the UI never renders — tests pass against a ghost schema. |
| "I'll update the mocks when the tests break." | Mocks that compile but produce wrong-shaped data are the most dangerous. Tests continue passing with stale field names because `as ForumPost` assertions suppress structural mismatches. The breakage surfaces in production, not in CI. |
| "This is just a one-line schema change — no need to run validate:mocks." | A single `VARCHAR(255)` → `TEXT` migration adds a new required field to the Pydantic response schema. The mock factory is now missing a required property. tsc catches it immediately with `pnpm validate:mocks` — but only if you run it. Skipping validation for "trivial" changes is how drift accumulates. |
| "The OpenAPI generator will fix this automatically when we wire it up." | The generator produces types, not mock data. Automating type generation eliminates manual sync of `lib/types.ts` but does nothing for mock factories — you still need `validate-mocks.ts` to catch factory drift. Postponing mock hygiene until the generator is live means living with broken fixtures indefinitely. |
| "The mock returns all required fields — the extra ones from the old schema don't hurt anything." | Extra fields in mock objects mask real problems. When a test asserts `expect(user.old_field).toBe("value")` and `old_field` was removed from the type 3 sprints ago, the test is testing dead code. Worse, new engineers copy the stale mock pattern and perpetuate the drift. |

Every mock factory must produce objects that satisfy the current TypeScript type. No stale fields. No missing required properties. No "close enough" mock data.

## Architecture & File Locations

```

backend/schemas/*.py ──(manual sync)──▶ mobile/lib/types.ts
                                               │
                                               ▼
                              __fixtures__/api-mocks.ts ← Factory per type
                                               │
                                               ▼
                              scripts/validate-mocks.ts  ← Typed assignments
                                               │
                                               ▼
                              tsc --noEmit → PASS (types match) or FAIL (drift)

```

| File | Purpose |
|------|---------|
| `__tests__/__fixtures__/api-mocks.ts` | Single source of truth for test data — factory per type |
| `scripts/validate-mocks.ts` | Assigns every factory result to typed vars, catches drift |
| `tsconfig.validate-mocks.json` | Dedicated tsconfig for `scripts/` + `__fixtures__/` |
| `jest.config.js` | Excludes `__fixtures__/` from test discovery |
| `package.json` | Script: `validate:mocks` runs the type-check |

## Ground Rules — Read Before Anything Else

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|---|---|---|
| 1 | Never add a backend schema field without updating the corresponding mock factory | `grep -rn "class.*Schema\|: Mapped\[" backend/app/schemas/ --include="*.py"` reveals new/changed fields; cross-reference against `__tests__/__fixtures__/api-mocks.ts` for matching factory coverage | Block the PR; require the mock factory update in the same commit as the schema change |
| 2 | Never let `pnpm validate:mocks` fail silently — treat every tsc error as a blocking issue | CI job `validate:mocks` exits non-zero; pre-push hook runs `pnpm validate:mocks` when `backend/app/schemas/**` or `mobile/lib/types.ts` change | Reject the push/PR; the type error message identifies the exact field mismatch — fix before proceeding |
| 3 | Never inline mock data in tests — always import from `api-mocks.ts` | `grep -rn ": {[^}]*id:" --include="*.test.ts" --include="*.test.tsx" mobile/` finds inline object literals with test data | Flag with `⚠️ INLINE-MOCK`; replace with factory import. Inline mocks cannot be validated by `validate-mocks.ts` |
| 4 | Never use `as` type assertion to suppress mock factory type errors | `grep -rn "} as [A-Z]" __tests__/__fixtures__/api-mocks.ts` finds `as Type` casts that bypass type checking | Remove the assertion; fix the factory to match the actual type. Using `as` on mock output is a code smell — it means the factory produces wrong-shaped data |
| 5 | Never modify `lib/types.ts` without running `pnpm validate:mocks` in the same changeset | `git diff --name-only` contains `mobile/lib/types.ts` but not `__tests__/__fixtures__/api-mocks.ts` | Block; the type change is unvalidated against mock factories. Run `pnpm validate:mocks` and fix any drift in the same commit |
| 6 | Never commit a mock factory that lacks defaults for all required fields | `grep -rn "export function createMock" __tests__/__fixtures__/api-mocks.ts` and trace each factory return object against its corresponding `lib/types.ts` interface | Mark the factory with `⚠️ INCOMPLETE-MOCK: missing required field [fieldName]`. A factory with missing required fields will cause runtime undefined errors in tests that do not provide overrides |
| 7 | Never bypass the `DeepPartial<Type>` override pattern — all factory signatures must accept `overrides: DeepPartial<Type> = {}` | `grep -A1 "export function createMock" __tests__/__fixtures__/api-mocks.ts | grep -v "DeepPartial"` finds factories without the override parameter | Add the `DeepPartial<Type>` parameter. Factories without overrides force every test to post-modify mock objects, which breaks the single-source-of-truth contract |
| 8 | **RUN `pnpm validate:mocks` before every push.** The pre-push hook exists to catch drift, but the developer must configure it. Until then, manual validation is the only guardrail. | Trigger: `git push` is attempted; `git diff --cached --name-only` intersects with `backend/app/schemas/**`, `mobile/lib/types.ts`, or `__tests__/__fixtures__/**` | STOP. Respond: "Staged changes include schema, type, or mock files. Running `pnpm validate:mocks` before push. If validation fails, fix the drift before pushing." |

## Anti-Hallucination Guardrails

- **Admit uncertainty — never fabricate.** If you are not certain about a type
  definition, schema field, or OpenAPI generator behavior, say so explicitly:
  "I am not certain this field exists in the current schema. Verify against
  `backend/app/schemas/`."

- **Flag your knowledge cutoff.** If your knowledge predates the latest framework
  or tool version, state your cutoff date and recommend verifying against current
  documentation.

- **Never guess security.** Do not provide authentication tokens, API keys, or
  security-sensitive configurations without explicit user instruction. Say:
  "Security configurations must be verified against current best practices."

- **Distinguish certainty levels.** Mark statements as:
  [VERIFIED] — from official docs or schema files,
  [COMMON-PRACTICE] — widely used but not authoritative,
  [INFERRED] — best guess based on patterns,
  [UNKNOWN] — unsure and needs verification.


## The Expert's Mindset

### Cognitive Biases That Destroy Mock-Data Hygiene

- **Compilation bias**: "It compiles, so it must be correct." Mock factories can compile while producing objects with missing, extra, or wrong-type fields — especially with `as Type` assertions. Compilation is necessary but insufficient. Only `pnpm validate:mocks` (which assigns factory output to explicitly typed variables) catches structural drift.
- **Familiarity heuristic**: "I know this API shape — I do not need to check the type." Backend schemas evolve weekly. The `User` type you memorized 2 sprints ago may now require `preferences` where it did not before. The expert checks the type definition before touching the factory.
- **Test-passing trap**: "The tests pass, so the mocks are fine." Tests passing with stale mocks is a false negative. If the mock has an extra field that the test asserts on but the actual type no longer includes it, the assertion tests dead code. New fields not exercised by old tests mask missing data.
- **Copy-paste inertia**: "I will copy this factory pattern for the new endpoint." Copying a factory that itself has drift propagates the error. Experts always verify the source factory against its type before using it as a template.
- **OpenAPI optimism**: "The generator will catch everything once we set it up." An OpenAPI generator produces types, not test data. Without `validate-mocks.ts` running in CI, generated types and hand-maintained mocks will drift independently. The generator is a type source, not a mock validator.

### What Masters Know

- Structural validation (`pnpm validate:mocks`) catches missing/extra fields; runtime validation catches wrong data values. You need both.
- `DeepPartial<Type>` is the correct override pattern because it ensures overrides are structurally compatible with the target type — unlike `Partial<Type>` which allows `undefined` in required fields.
- The validate-mocks.ts file must assign every factory result to a **typed variable** (not `any`, not `unknown`). If the variable is `any`, tsc will not catch drift.
- Mock factories should produce **realistic** data, not placeholder strings. `uid("post")` is fine for IDs; `"Test Post"` for titles is not — use `faker` or domain-appropriate defaults.
- A single `as Type` assertion in a mock factory is a time bomb. Every subsequent test that imports that factory inherits the silent type mismatch.

---

## Operating at Different Levels

### Scale Depth

| Depth | Time | Scope | Artifacts |
|-------|------|-------|-----------|
| **Quick Scan** | ~30s | Run `pnpm validate:mocks`, read the first type error, fix the mismatched field | One corrected factory field |
| **Standard Engagement** | ~5-10min | Full DETECT→VALIDATE→SYNC→VERIFY cycle: check which schemas changed, update types, update factories, run validation | Updated api-mocks.ts, passing validate:mocks, commit with all 3 files |
| **Deep Dive** | ~30min+ | New endpoint integration: design factory defaults, add to validate-mocks.ts, wire up CI pre-push hook, verify all existing tests still pass | New factory + validate-mocks entry + CI config + test audit |
| **Enterprise Audit** | Multi-session | Full mock-sync health check: audit all factories against types, measure CI coverage, configure OpenAPI generator, eliminate all `as` assertions | Mock health report, OpenAPI pipeline config, factory coverage matrix |

### Quick Scan (~30s)
For known schema changes where the scope is clear (e.g., "added `bio` field to User"). Run `pnpm validate:mocks`, read the error, add the missing field to the factory, re-run validation. Commit the factory change alongside the schema change.

### Standard Engagement (~5-10min)
For new endpoints or multi-field schema changes. Trace the change from backend schema → mobile type → mock factory → validate-mocks.ts. Update all touchpoints, run validation, verify tests pass, commit atomically.

### Deep Dive (~30min+)
For new API surface areas (new resource, new endpoint family). Design factory defaults that exercise edge cases (empty arrays, null optional fields, boundary values). Add comprehensive validate-mocks.ts coverage. Configure CI pre-push hook if not present. Audit existing tests for inline mocks that should migrate to factories.

---
## When to Use

**Trigger conditions:**
- A backend Pydantic schema gains, loses, or renames a field
- `mobile/lib/types.ts` is modified in any way
- A new API endpoint is added that returns typed data
- CI pipeline reports `pnpm validate:mocks` failure
- A test is flaky due to mock data that does not match the real response shape
- Code review reveals inline mock data in test files
- A mock factory contains `as Type` assertions
- Setting up or repairing the pre-push validation hook
- Configuring the OpenAPI generator pipeline for type generation

**When NOT to use:**
- Writing the backend schema itself (use `backend-developer` or `api-designer`)
- Designing the database schema (use `database-designer`)
- Writing end-to-end tests (use `qa-engineer`)
- General TypeScript type definitions unrelated to API responses
- Fixing test logic errors that are not mock-data-shape related

---

## Route the Request

| Trigger | Route to Workflow |
|---|---|
| `backend/app/schemas/*.py` changed | Schema Change → Validate workflow |
| `mobile/lib/types.ts` changed | Type Change → Validate workflow |
| CI `validate:mocks` fails | Drift Repair workflow (decode error → fix → recommit) |
| New route/endpoint added | New Factory workflow (type → factory → validate → commit) |
| `openapitools.json` modified | Generator Config workflow |

---

## Core Workflow
**(STANDARD)**

1. **DETECT** — Identify what changed: backend schema, mobile types, or CI failure. Determine scope.
2. **TRACE** — Follow the dependency chain: `schemas/{resource}.py` → `lib/types.ts` → `api-mocks.ts` → `validate-mocks.ts`. Identify every touchpoint.
3. **UPDATE** — Update types.ts, then factory (add/remove/rename fields, never `as Type` to suppress), then validate-mocks.ts typed assignment.
4. **VALIDATE** — Run `pnpm validate:mocks`. Expect zero tsc errors. Read exact mismatch, fix, re-run.
5. **TEST** — Run `npx jest`. Verify all tests pass with updated mocks. Failing tests relied on stale shapes — update assertions.
6. **COMMIT** — Atomically: schema + types + factory + validate in ONE commit. Message: "sync: update User factory after adding preferences field (backend schema v2.3)".
7. **VERIFY** — CI passes (validate:mocks + jest), no drift, done.

## Best Practices

1. **Every `lib/types.ts` type gets a factory.** No type should exist without a `createMock*()` function.

2. **Factories are the single source of truth for test data.** Tests import `createMockUser()`, never inline `{ id: "u1", ... }`.

3. **Use `DeepPartial<Type>` for overrides, never `Partial<Type>`.** `Partial` makes required fields optional, allowing `undefined` where the type expects a value. `DeepPartial` handles nested objects correctly.

4. **Override only what the test cares about.**

```typescript

// ✅ CORRECT
const lockedPost = createMockForumPost({ is_locked: true });
// ❌ WRONG — over-specifying defaults
const post = createMockForumPost({ id: "p1", category_id: "c1", title: "Test", is_locked: true, /* ...15 more */ });

```

5. **Naming convention is strict:** `createMockThing(overrides?)` for single objects, `createMockThingArray(n, overrides?)` for arrays. Never: `mockThing()`, `fakeThing()`.

6. **validate-mocks.ts uses typed assignments, not `as` or `any`:**

```typescript

const _checkUser: User = createMockUser();  // ✅ type catches drift
const _checkUser: any = createMockUser();   // ❌ erases validation

```

7. **Commit schema, types, and mocks atomically** — same commit. Split commits create windows where CI is red.

8. **Run `pnpm validate:mocks` as a pre-push hook.** 2 seconds locally vs. 5-15 minute round-trip through CI.

9. **Mock defaults should be realistic enough to catch domain bugs:**

```typescript

// ✅ REALISTIC: email: "user@example.com", verification_tier: "verified", created_at: new Date().toISOString()
// ❌ PLACEHOLDER: email: "a@a.com", verification_tier: "???", created_at: "2020-01-01"

```

10. **Isolate `as Type` to the bottom of each factory.** Goal is `satisfies Type`, not `as Type`.

## Validation Pipeline

### Local (pre-push hook)
The pre-push hook (`scripts/pre-push-check.sh`) automatically runs mock-sync validation when staged changes touch:
- `backend/app/schemas/**`
- `mobile/lib/types.ts`

### CI
The `mobile-test` job runs `validate:mocks` after Jest tests. Failure blocks the PR from merging.

### Manual

```bash

cd mobile && pnpm validate:mocks
# or
cd mobile && npx tsc --project tsconfig.validate-mocks.json --noEmit

```

## Adding a New Mock Factory

1. Define the factory in `__tests__/__fixtures__/api-mocks.ts`:

```typescript

export function createMockNewThing(overrides: DeepPartial<NewThing> = {}): NewThing {
  return { /* defaults */ ...overrides } as NewThing;
}

```

2. Add type-check in `scripts/validate-mocks.ts`:

```typescript

import { createMockNewThing } from "../__tests__/__fixtures__/api-mocks";
import type { NewThing } from "@/lib/types";
const _checkNewThing: NewThing = createMockNewThing();
void _checkNewThing; // suppress unused warning

```

3. Add both to the `void [...]` array at the bottom.

4. Run `pnpm validate:mocks` to confirm.

## Backend Schema Change Checklist

When adding/removing/renaming a field in a Pydantic schema:

1. [ ] Update `backend/app/schemas/{resource}.py`
2. [ ] Update `mobile/lib/types.ts` with matching field
3. [ ] Update `createMock*()` in `__tests__/__fixtures__/api-mocks.ts`
4. [ ] Run `pnpm validate:mocks` — should pass
5. [ ] Run `npx jest` — all tests should still pass
6. [ ] Commit all three files together

## Decision Trees
**(QUICK)**

### Schema Change → Validate

```

Field ADDED (required) → Add to types.ts + factory default → validate:mocks
Field ADDED (optional) → Add to types.ts as field? → factory default → validate:mocks
Field REMOVED            → Remove from types.ts + factory → validate:mocks catches stale refs
Field RENAMED            → Rename in both → tsc flags all old-name references

```

### Mock Failure → Fix

```

"Property X missing but required"   → Add X to factory default
"Property X does not exist on type" → Intentional removal: remove from factory.
                                      Accidental: restore to types.ts.
"Type X not assignable to type Y"   → Type changed; update factory default to match
"Cannot find module"                → Check tsconfig.validate-mocks.json paths

```

### New Endpoint → Add Factory

```

Type exists? → YES: Create factory. NO: Add type to types.ts first.
Create factory: createMockThing() for single, createMockThingArray(n) for lists
Add to validate-mocks.ts: const _checkNew: NewType = createMockNewType()
Run validate:mocks → Fix mismatches (never use `as` to suppress)

```

### OpenAPI Generator Pipeline

```

Spec stable?  → YES: Generate types, validate mocks against generated types.
                NO: Keep manual sync until spec stabilizes.
Spec complete? → YES: Full generation. NO: Partial for documented endpoints only.

```

## OpenAPI Generator (Future)

`openapitools.json` is configured with TypeScript/Python/Swift/Kotlin generators targeting `specs/api-spec.yaml`. When wired up:

```

specs/api-spec.yaml  ──openapi-generator──▶  mobile/lib/types.ts (auto-generated)
                                                   │
                                                   ▼
                                       __tests__/__fixtures__/api-mocks.ts
                                                   │
                                                   ▼
                                      scripts/validate-mocks.ts (catches drift)

```

Until then, manual sync between Pydantic schemas and `lib/types.ts` is required.

## Error Recovery
**(STANDARD)**

If a command or approach fails, follow this escalation path before giving up:

| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|---------------|-------------|
| `pnpm validate:mocks` fails | Read the type error — it tells you exactly which field is mismatched | Check if the schema changed intentionally (new required field) vs accidentally | Update the mock factory to match the current type shape |
| `tsc` cannot find types | Verify `tsconfig.validate-mocks.json` includes the right paths | Check that `@/lib/types` path alias resolves correctly | Run `npx tsc --project tsconfig.json --noEmit` to check the full project |
| OpenAPI generator produces wrong types | Regenerate with `openapi-generator-cli generate` | Check `openapitools.json` configuration | Manually sync types until generator is fixed |
| CI validation fails on PR | Check CI logs for the specific type error | Reproduce locally with `pnpm validate:mocks` | Fix and push a new commit |
| Factory update causes cascading test failures | Audit which tests broke — are they testing the right thing? | Update test assertions to match the new shape if the schema change was intentional | If the schema change was accidental, revert it rather than fixing downstream |
| `DeepPartial<Type>` not resolving | Verify the `DeepPartial` utility type is imported correctly | Check that the type `Type` is exported from `lib/types.ts` | Use `Partial<Type>` as temporary fallback with a `// FIXME: DeepPartial` comment |

**Hard failure boundary:** If 3 different approaches all fail, STOP. Do not iterate infinitely. Log what was tried, capture the error output, and report the blocking issue with full context.

## Error Decoder

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| `Property X is missing in type Y but required` | A required field was added to the type but the factory does not provide it | Add a sensible default for X in the factory return object | Required fields added to types must immediately be reflected in factories — this is the most common drift pattern |
| `Property X does not exist on type Y` | Factory includes a field that was removed from the type or never existed | Remove the field from the factory. If the field was intentionally removed from the schema, this is correct behavior | Stale fields in mocks are dangerous because tests can pass against deleted fields |
| `Type string is not assignable to type "A" | "B"` | A field changed from a broad type to a union of string literals | Update the factory default to one of the valid union members | Union types require factories to pick a valid default — random strings will cause type errors |
| `Type number is not assignable to type string` | A field type changed (e.g., ID from number to UUID string) | Update the factory default to match the new type | Type changes require factory updates AND test assertion updates — tests comparing against old types will fail |
| `Cannot find module @/lib/types` | tsconfig path alias is misconfigured or the file was moved | Check `tsconfig.validate-mocks.json` paths section; verify `lib/types.ts` exists | Path aliases in validate-mocks.tsconfig must match the main tsconfig exactly |
| `Object literal may only specify known properties` | Factory includes a field not in the type (spelling error or removed field) | Compare the field name against the type definition — it is either misspelled or removed | tsc excess property checking is a safety net — never use `as Type` to suppress it |
| `createMock* is not a function` | Factory was not exported or the import path is wrong | Check the export in api-mocks.ts and the import in validate-mocks.ts | validate-mocks.ts imports are the canary — if they fail, test files will too |

## Cross-Skill Coordination

This skill operates at the intersection of backend schema design, mobile development, and CI quality gates. Invoke complementary skills when:

| Scenario | Invoke |
|---|---|
| Reviewing mock factory code for correctness | `code-reviewer` |
| Setting up CI validation pipeline | `ci-cd-builder` |
| Major schema migration with breaking changes | `backend-developer` |
| Mobile type definition changes | `mobile-developer` |
| API contract design that affects mock shapes | `api-designer` |
| Debugging test failures caused by mock data | `qa-engineer` |
| Automating type generation from specs | `devops-engineer` |

---

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `backend-developer` | Backend Pydantic schemas, database column definitions, API response shapes | When a new endpoint is added or an existing schema field changes type/required status |
| `api-designer` | API contracts, response schemas, versioning strategy | Before generating OpenAPI types from specs |
| `domain-modeling` | Domain entity definitions, relationship mappings | When new domain objects need mock factories |

## Proactive Triggers

| Trigger Condition | Automatic Action |
|---|---|
| `git diff` shows changes to `backend/app/schemas/*.py` without corresponding changes to `__tests__/__fixtures__/api-mocks.ts` | Prompt: "Backend schema changed but mock factory was not updated. Run `pnpm validate:mocks` to check for drift." |
| `git diff` shows changes to `mobile/lib/types.ts` without changes to `api-mocks.ts` | Prompt: "Type definitions changed. Verifying mock factories are still compatible with `pnpm validate:mocks`." |
| CI `validate:mocks` job fails on a PR | Block merge; display the exact type error and the file:line of the mismatch |
| New `createMock*` function added without corresponding entry in `validate-mocks.ts` | Prompt: "New factory detected. Add a typed assignment in `validate-mocks.ts` to ensure it is validated." |
| `as Type` assertion found in `api-mocks.ts` outside of the standard return pattern | Flag: "Unexpected type assertion in factory. Factory may be producing wrong-shaped data." |
| `openapitools.json` modified but `lib/types.ts` not regenerated | Prompt: "Generator config changed. Run `openapi-generator-cli generate` to regenerate types, then run `validate:mocks`." |
| Test file contains inline object literals with `id`, `email`, or known API field names | Suggest: "Inline mock data detected. Replace with `createMock*()` import from api-mocks.ts." |

---

## State Log

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every mock factory addition, type validation decision, and schema sync strategy choice must be recorded so subsequent agents (or future sessions) can recover context without replaying the entire conversation. Log decisions in `files/state-log.md` within the session context.

## What Good Looks Like

### Before: Stale Factory → After: Synced Factory

```typescript

// ❌ BEFORE — preferences missing, avatar_url removed 2 sprints ago
export function createMockUser(o: DeepPartial<User> = {}): User {
  return { id: uid("user"), email: "test@test.com", display_name: "Test User",
    verification_tier: "unverified",
    avatar_url: "https://example.com/avatar.png", ...o } as User;
}

// ✅ AFTER — all fields present, defaults match system
export function createMockUser(o: DeepPartial<User> = {}): User {
  return { id: uid("user"), email: "user@example.com", display_name: "Test User",
    verification_tier: "unverified", preferences: createMockUserPreferences(),
    created_at: new Date().toISOString(), ...o } as User;
}
// validate-mocks.ts: const _checkUser: User = createMockUser();  ← catches drift

```

### Before: Inline Mock → After: Factory Import

```typescript

// ❌ BEFORE — field removed from type, test silently passes
const user = { id: "u1", email: "test@test.com", avatar_url: "/old.png" };

// ✅ AFTER — factory validated by CI, override only what matters
const user = createMockUser({ verification_tier: "unverified" });

```

---

## Deliberate Practice

| Exercise | Time | What You Do |
|---|---|---|
| **Audit a factory** | 10 min | Cross-reference each factory in `api-mocks.ts` against `lib/types.ts`. Flag: missing required fields, extra fields not in type, wrong types, unregistered factories. |
| **Simulate schema change** | 15 min | Add `tags: string[]` to `ForumPost` schema. Walk the full 6-step checklist: update schema → types → factory → validate:mocks → jest → commit. Measure cycle time. |
| **Eliminate inline mocks** | 20 min | Search tests for inline object literals. Replace with factory calls. Track how many tests break — they relied on stale shapes. |
| **Build validate-mocks from scratch** | 30 min | Create tsconfig.validate-mocks.json, write validate-mocks.ts, add script to package.json, configure pre-push hook, verify pipeline catches intentionally introduced drift. |
| **OpenAPI generator integration** | 20 min | Configure openapitools.json for TypeScript generation. Compare generated types against manual types.ts. Document discrepancies. |

---

## Anti-Patterns

| Anti-Pattern | Why It Fails | Do This Instead |
|---|---|---|
| **The `as Type` escape hatch** — `return { id: "1" } as User` with 6 missing fields | Destroys all type safety; every downstream consumer inherits the lie; production crashes on `user.preferences.theme` | Fill every required field; `as Type` only at the very end of the return object, never as a shortcut |
| **Copy-paste factory** — copy `createMockForumPost()`, rename to `createMockPodcast()`, keep old fields | Transfers stale structure; `category_id` instead of `genre`, `is_locked` instead of `is_explicit` | Read the target type; write each field explicitly; use existing factory only for style reference |
| **Inline mocks diverge** — each test has `{ id: "u1", ... }` with different shapes | No single update point; every test drifts independently; validate-mocks can't see inline mocks | Every test imports from `api-mocks.ts`; one factory update fixes all tests |
| **Factory defaults ≠ system defaults** — `verification_tier: "verified"` when new users default to `"unverified"` | Tests pass against wrong state; critical flows never exercised with correct default | Factory defaults = system defaults; tests needing different state override explicitly |
| **Factory per test case** — `createMockLockedPost()`, `createMockDeletedPost()`, etc. bloat to 5000 lines | Type gains a field → every variant factory must be updated; some are missed | One factory per type; variants via overrides: `createMockForumPost({ is_locked: true })` |
| **Skipping validate:mocks** — "just a refactor, no new fields" | Refactors change type STRUCTURE; "by eye" misses structural incompatibilities tsc catches instantly | Run `pnpm validate:mocks` after EVERY types.ts change (2 seconds) |
| **Committing types without mocks** — "factory in follow-up PR" that never happens | Deferred mocks become permanent inline mocks; 6 months later, 15 tests have diverging shapes | Mock factory IS part of the type PR; CI enforces: types.ts diff → api-mocks.ts must also be in diff |

---

## Gotchas

| Gotcha | Cost | Fix |
|--------|------|-----|
| Mock factory compiles with `as Type` but is missing required fields — production crashes when a new screen accesses the missing field | $5K-$50K in production incident (rollback, RCA, hotfix, downtime) | Remove `as Type`; run `validate:mocks` in CI; typed assignments catch missing fields |
| Stale field persists in factory 6 months after removal — 12 tests assert on dead data, masking a silently broken feature | $10K-$30K in misdirected debugging (days wasted chasing phantom bugs) | Run `validate:mocks` which catches excess properties |
| Inline mock uses `amount: 100` (int) but API returns `"100.00"` (string) — 2 sprints of features built on wrong assumption | $15K-$40K in rework (features must be re-validated and partially rewritten) | Use factory imports; factories get type-checked by validate-mocks.ts |
| Backend adds required field Friday, mock deferred to Monday — weekend CI passes, 3 PRs merge with stale factory | $8K-$20K in Monday remediation (revert/patch 3 PRs, add CI, half-day lost) | Never defer mock updates; atomic commits prevent split-state windows |
| `createMockUserArray(5)` returns 5 identical objects (same ID) — dedup tests pass trivially, production bug surfaces with real unique IDs | $3K-$15K in escaped defect (support handles duplicate complaints, pattern rewrite needed) | `Array.from({ length: n }, (_, i) => createMockUser({ id: uid(\`user-\${i}\`) }))` |
| OpenAPI generator idle 3 months — 47 type mismatches surface, blocking all work for 2 days | $12K-$25K in integration debt (full-team type reconciliation, 47 factories audited) | Run generator on every spec change or remove config until ready |
| Factory overrides break after field rename: `role` → `user_role` — override silently becomes extra property, factory returns object with no role | $5K-$20K in silent test breakage (admin features appear broken in tests, team chases phantom bug) | Add override validation test: `expect(createMockUser({ user_role: "admin" }).user_role).toBe("admin")` |

## Verification Checklist

Before merging any code that touches mock data or validation:

- [ ] `pnpm validate:mocks` exits 0 with no tsc errors — **Complete when** tsc reports zero type errors across all typed assignments
- [ ] Every factory in `api-mocks.ts` has a corresponding typed assignment in `validate-mocks.ts` — **Complete when** `grep "createMock" api-mocks.ts | wc -l` equals the factory count in validate-mocks.ts
- [ ] No `as Type` assertions exist except the single return-statement cast in each factory — **Complete when** `grep -c " as " api-mocks.ts` returns ≤ factory count
- [ ] All factory defaults are realistic and match system defaults — **Complete when** manual review confirms each default value matches production defaults
- [ ] Factory override parameters use `DeepPartial<Type>` — **Complete when** `grep "Partial<" api-mocks.ts` returns zero matches (all use DeepPartial)
- [ ] Schema changes, type changes, and factory changes are in the same commit — **Complete when** `git diff --name-only HEAD~1` includes all three file categories
- [ ] Jest test suite passes (`npx jest` exits 0) — **Complete when** all test suites report green with no failures
- [ ] No inline mock data in test files — **Complete when** `grep -rn ": {[^}]*id:" --include="*.test.*"` returns empty
- [ ] Pre-push hook is configured and not bypassed with `--no-verify` — **Complete when** `.git/hooks/pre-push` exists and references validate:mocks
- [ ] CI pipeline includes `validate:mocks` step — **Complete when** CI workflow YAML contains `pnpm validate:mocks` in the jobs list
- [ ] State log is updated with any intentional deviations or deferred work — **Complete when** `files/state-log.md` contains an entry for the current session

---

## Verification Guardrails

Before delivering work, verify: all mock factories match current TypeScript types (`pnpm validate:mocks` passes), no broken references to non-existent types, the CI validation workflow is correctly configured, new factories follow naming conventions (`createMock*`, `createMock*Array`), all backend schema change checklist items are completed, and cross-skill dependencies (backend schemas → types → mocks) are satisfied. If any check fails, revise before delivering.

## References

- [Reference Index](references/README.md) — Consolidated index of all reference materials for mock-data synchronization workflows
