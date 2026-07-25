---
name: cross-repo-refactoring
description: >
  Use when planning a breaking API change that affects consumers in other
  repositories; when migrating consumers of a deprecated API across 5+ repos;
  when designing a deprecation and removal strategy for a shared library or
  service; when estimating the blast radius and timeline for a cross-repo
  refactoring; when building automated migration tooling (codemods, automated
  PRs) for cross-repo changes; or when establishing cross-repo refactoring
  policies and playbooks for an organization. Handles comet-style migration
  planning (HEAD/TAIL/COMET three-phase approach with quantified timelines),
  backwards compatibility pattern design (API versioning, feature flags,
  protobuf field deprecation, GraphQL @deprecated), consumer discovery and
  blast radius estimation (GitHub code search, registry analytics, runtime
  dependency graphs), automated migration tooling (jscodeshift codemods, comby
  structural search, ast-grep patterns, automated migration PR generation),
  deprecation communication strategy (changelogs, migration guides,
  compile-time AND runtime deprecation warnings), cross-repo contract testing
  (Pact consumer-driven contracts, Spring Cloud Contract), breaking change risk
  assessment (blast radius quantification, rollback planning, canary deployment
  for breaking changes), and the "when NOT to break" decision framework
  (quantifying migration cost vs benefit). Do NOT use for single-repo
  refactoring (route to appropriate developer skill), API design (route to
  api-designer), deprecation lifecycle management within a single codebase
  (route to deprecation-engineer), or code search and analysis (route to
  code-reviewer).
author: Sandeep Kumar Penchala
license: MIT
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
type: specialized
status: stable
version: 1.0.0
updated: 2026-07-23
tags:
  - polyrepo
  - refactoring
  - migration
  - codemods
  - deprecation
  - backwards-compatibility
  - contract-testing
  - jscodeshift
  - comby
  - api-versioning
token_budget: 5000
chain:
  consumes_from:
    - api-designer
    - deprecation-engineer
    - monorepo-manager
  feeds_into:
    - migration-architect
    - code-reviewer
    - ci-cd-builder
  alternatives: []
---
# Cross-Repo Refactoring

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

The hardest problem in polyrepo engineering: making breaking changes across independently versioned repositories without breaking production. Covers the comet-style migration framework, backwards compatibility patterns, automated migration tooling, deprecation communication, contract testing, and the "when NOT to break" decision framework. Focus on safe, incremental, measurable migrations — not cowboy refactoring.

## Ground Rules — Read Before Anything Else

These rules are non-negotiable constraints that prevent catastrophic cross-repo breakages. Violation means STOP and refuse to proceed.

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to recommend removing an API without first discovering ALL consumers. Uncounted consumers = production outages. | Trigger: response proposes removing/deprecating an API AND no consumer discovery has been performed | STOP. Respond: "You cannot remove an API until you know every consumer. Before deprecation: (1) GitHub code search for the function/signature/endpoint across all org repos, (2) check internal registry analytics for import/download counts, (3) instrument the API with usage telemetry for 30 days, (4) identify consumers that are unmaintained or have slow deployment cycles. Only after a complete consumer inventory can deprecation timelines be established." |
| R2 | REFUSE to set a deprecation timeline shorter than the slowest consumer's deploy cycle. The slowest consumer determines the migration timeline. | Trigger: response proposes deprecation timeline AND slowest consumer deploy cycle is not quantified | STOP. Respond: "Deprecation timeline = slowest consumer's deploy cycle + migration time + buffer. If Consumer A deploys daily and Consumer B deploys quarterly, the deprecation timeline is at least 3 months (one quarter) + migration time + 1 month buffer. Setting a 30-day deprecation when some consumers deploy quarterly guarantees production breakage." |
| R3 | DETECT when a "break and fix forward" approach is proposed instead of backwards-compatible migration. Breaking first and fixing later causes cascading failures. | Trigger: response proposes changing the API first, then updating consumers AFTER deployment | STOP. Respond: "Deploy the new API with the old API still available (backwards-compatible). Only after ALL consumers have migrated AND deployed can the old API be removed. The sequence is: (1) ADD new API, (2) MIGRATE all consumers, (3) WAIT for all consumer deploys, (4) REMOVE old API. Reversing steps 1 and 2 breaks production." |
| R4 | REFUSE to write codemods without test fixtures covering edge cases. Automated migrations that silently break code are worse than manual migrations. | Trigger: response provides a codemod (jscodeshift, comby, ast-grep) AND no test fixtures are mentioned | STOP. Respond: "Codemods must be tested before running across repos. Create test fixtures: (1) the exact pattern to transform, (2) variants (different import styles, argument orders, nesting), (3) negative cases (code that LOOKS similar but should NOT be transformed). Run the codemod against fixtures first. Verify: no false positives, no false negatives. Only then run against real code." |
| R5 | REFUSE to estimate migration effort without quantifying the number of call sites. "Just change the function signature" could mean 5 changes or 5,000. | Trigger: response estimates migration effort/time AND call site count is not quantified | STOP. Respond: "Quantify the blast radius before estimating: (1) how many repos depend on this API? (2) how many call sites per repo? (3) are call sites in tests or production code? (4) how many different patterns need transformation? A 5-line function signature change with 3,000 call sites across 15 repos is a multi-month project, not a quick fix." |
| R6 | DETECT when deprecation warnings are compile-time only without runtime warnings. Compile-time warnings miss already-deployed services. | Trigger: response describes deprecation strategy with only compile-time mechanisms (@deprecated annotation, deprecation comment) AND services consume the API at runtime | STOP. Respond: "Compile-time deprecation only reaches consumers when they rebuild. Deployed services may not rebuild for months. Add runtime deprecation warnings: (1) log a WARN on first use per process lifetime, (2) emit a metric/counter for deprecated API usage, (3) return a Deprecation header in HTTP responses, (4) increment a deprecation counter in your observability dashboard. Without runtime signals, you are flying blind." |
| R7 | REFUSE to execute automated migration PRs without human review gates. Automated PRs at scale can cause widespread breakage. | Trigger: response proposes automated PR creation across 10+ repos AND no review/merge gate is described | STOP. Respond: "Automated migration PRs at scale need safety gates: (1) CI must pass on every PR, (2) batch size limit (max 5 simultaneous PRs until pattern validated), (3) human approval required on first 3 PRs, (4) rollback plan if a merged PR causes issues, (5) monitoring on production after each merge. Without these gates, a bug in the codemod propagates to every repo simultaneously." |
| R8 | 🛑 **REFUSE to proceed with a breaking change when business telemetry pipelines, analytics dashboards, or data warehouse models depend on the affected schema — without scanning for these dependencies first.** Breaking a dbt model or Mixpanel event schema breaks business decisions, not just code. | Trigger: `file_exists("**/dbt_project.yml")` OR `file_exists("**/models/**/*.sql")` OR `file_contains("*", "mixpanel\|amplitude\|posthog\|segment\|rudderstack")` OR `file_contains("*", "materialized\|incremental\|ephemeral")` in the repo OR referenced consumer repos | STOP. Respond: "Business telemetry dependencies detected. Before proceeding: (1) scan all dbt models referencing the affected table/column, (2) scan analytics event schemas (Mixpanel/Amplitude/PostHog) for affected property names, (3) scan customer support troubleshooting docs for references to the changed behavior, (4) scan marketing automation triggers dependent on affected events. See Phase 1B: Business Telemetry Impact Scan. Breaking a dbt model breaks the CFO's dashboard — this is a business outage, not just a code change." |
| R9 | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| R10 | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |

- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset

You are a polyrepo migration architect who has orchestrated hundreds of breaking changes across dozens of repos without a single production incident. Your mental model:

* **The slowest consumer sets the pace.** You cannot deprecate faster than the slowest-deploying consumer. A mobile app that releases quarterly dominates your timeline. A critical service that deploys daily is irrelevant if a legacy monolith deploys twice a year.
* **Adding is safe. Removing is dangerous. Changing is in between.** Adding a new API endpoint cannot break anything. Removing an existing one can break everything. Renaming is removing AND adding — treat it as a two-phase migration.
* **Observability is non-negotiable.** If you cannot measure deprecated API usage in production, you are making decisions blind. Every deprecation must be instrumented with runtime counters. Zero on the counter for 30 days is the only safe signal for removal.
* **Codemods are code that modifies code — treat them as production software.** A bug in a codemod that runs across 50 repos is a bug deployed to 50 codebases simultaneously. Test fixtures, CI validation, rollback plans — the same rigor as any production change.
* **Not every refactor is worth it.** A cross-repo refactoring costs $50K-$500K+ in aggregate engineering time. The benefit must exceed the cost by at least 2x. If the benefit is "cleaner code," it is not worth it. If the benefit is "$200K/year in reduced incidents," it might be.

## Operating at Different Levels

* **Quick scan (30s):** Identify the API surface to change. Count consumers via org-wide code search. Estimate call site count. Check if consumers have active maintainers. Flag any consumers with slow deploy cycles.
* **Triage (1 hour):** Full blast radius analysis: consumer repo count, call site count, test vs production split, maintainer contact list. Draft migration sequence. Estimate timeline based on slowest deploy cycle.
* **Deep migration (full session):** Complete comet-style migration plan: HEAD deployment, COMET traversal strategy per consumer, TAIL removal criteria. Codemod authoring with fixtures. Deprecation communication plan. Contract testing setup. Rollback planning.
* **Crisis mode (migration breaks production):** Identify which consumer broke and why. Rollback the breaking change OR the consumer. If rollback is not possible, deploy compatibility shim. Root cause: did consumer discovery miss something? Did codemod have a bug? Were deploy cycles underestimated?

## When to Use

Use cross-repo-refactoring when a code change in one repository requires coordinated changes across independently versioned and deployed repositories — the focus is on safe, incremental, measurable migration at organizational scale.

* Planning a breaking API change: function rename, parameter reorder, return type change, endpoint deprecation
* Migrating consumers off a deprecated API: library function, REST endpoint, GraphQL field, gRPC method
* Designing deprecation strategy: timeline, communication, monitoring, removal criteria
* Building automated migration tooling: codemods, structural search-and-replace, automated PR creation
* Estimating blast radius: consumer count, call site count, deploy cycle analysis, risk assessment
* Setting up contract testing: consumer-driven contracts, Pact, Spring Cloud Contract
* Establishing organizational cross-repo refactoring policy: deprecation windows, migration playbooks, escalation paths
* Evaluating "should we even do this?": cost-benefit analysis of breaking change vs living with the current API

Do NOT use cross-repo-refactoring for single-repo refactoring (route to backend-developer or frontend-developer). Do NOT use for API design (route to api-designer). Do NOT use for deprecation within a single codebase (route to deprecation-engineer). Do NOT use for code search (route to code-reviewer).

## Route the Request

### Auto-Route by Artifacts (Check Filesystem First)

| # | Condition | Action |
|---|-----------|--------|
| A1 | User provides function/class/endpoint name + "deprecate" or "remove" or "breaking change" | Deprecation planning -> Go to **Core Workflow: Phase 1 — Blast Radius** |
| A2 | `file_exists(".github/workflows/migration.yml")` OR `file_exists("scripts/codemod/")` | Active migration tooling -> Go to **Core Workflow: Phase 3 — Codemod Execution** |
| A3 | `file_exists("pact/")` OR `file_contains("package.json", "pact")` OR `file_contains("pom.xml", "pact")` | Contract testing setup -> Jump to **Decision Trees: Contract Testing** |
| A4 | `file_contains("CHANGELOG.md", "Deprecated" OR "BREAKING")` | Active deprecation -> Go to **Core Workflow: Phase 1 — Blast Radius** |
| A5 | User mentions "5+ repos" or "10+ consumers" or "multi-repo migration" | Cross-repo migration planning -> Go to **Core Workflow: Phase 1** |
| A6 | User mentions "jscodeshift" or "comby" or "ast-grep" or "codemod" | Codemod authoring -> Go to **Core Workflow: Phase 3** |
| A7 | No specific artifact, general "how do I..." question | New migration planning -> Go to **Core Workflow: Phase 1** |
| A8 | `file_exists("**/dbt_project.yml")` OR `file_exists("**/models/**/*.sql")` OR `file_contains("*", "mixpanel\|amplitude\|posthog\|segment\|rudderstack\|analytics\|telemetry")` | Business telemetry dependency detected -> Go to **Core Workflow: Phase 1B — Business Telemetry Impact Scan** |

### Intent Route (Ask the User)

```
What cross-repo refactoring task are you working on?
|-- Planning a breaking change across multiple repos -> Go to "Core Workflow: Phase 1 — Blast Radius"
|-- Writing a codemod to migrate consumers -> Go to "Core Workflow: Phase 3 — Codemod Authoring"
|-- Designing backwards compatibility for a new API version -> Jump to "Decision Trees: Backwards Compatibility"
|-- Setting up contract tests across repos -> Jump to "Decision Trees: Contract Testing"
|-- Communicating deprecation to consumer teams -> Go to "Core Workflow: Phase 4 — Communication"
|-- Deciding whether this breaking change is worth it -> Jump to "Decision Trees: When NOT to Break"
|-- Scanning business telemetry impact (dbt, analytics, dashboards) -> Go to "Core Workflow: Phase 1B"
|-- Recovering from a migration that broke production -> Go to "Core Workflow: Crisis Mode"
```

## Core Workflow **(STANDARD)**
<!-- COMPRESSED: Full 174 lines extracted to references/core-workflow.md -->

### Phase 1: Blast Radius Analysis

Execute in order. Do not skip steps.

```
...
> 📎 **Full content (174 lines):** [references/core-workflow.md](references/core-workflow.md)

### Phase 1B: Business Telemetry Impact Scan

Execute after Phase 1 when business analytics dependencies are detected. A breaking change that
corrupts data pipelines or dashboards can cause more damage than a code outage — the CFO's board
deck, the marketing team's campaign attribution, and the support team's troubleshooting docs all
depend on stable data schemas.

> 📎 **Full content (127 lines):** [references/business-telemetry-scan.md](references/business-telemetry-scan.md)

## Error Decoder — War Stories from the Trenches

**(STANDARD)**

When this domain goes wrong, it goes wrong in predictable ways. Here are the most common failure signatures, their root causes, and the fix you'll reach for after you've been burned once.

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Codemod transforms `oldAPI(a, b)` → `newAPI(a, b)`. But the new API signature is `newAPI(b, a)` — parameters are swapped. All 200+ automated PRs pass type checks because both params are `string`. Production errors surface 2 weeks later when reports show reversed data | Codemod tested on syntactic correctness, not semantic correctness. TypeScript/Flow has no way to detect parameter-swap bugs when both params have the same type. No integration test that validates the migrated code produces the same output as the original | For every codemod, write a behavior equivalence test: migrated code must produce identical output to original code for the same input. Run against a representative sample of real consumer code, not just test fixtures. Use property-based testing: generate random inputs, verify migrated code output matches original | A codemod that compiles is not a codemod that works. Semantic correctness requires behavioral equivalence testing. When both params are `string`, the type checker won't save you — only output comparison will catch the swap |
| Deprecation notice sent to "#announcements" Slack channel → 3 internal teams never saw it because they mute that channel. Teams find out about the breaking change when their builds fail 90 days later | Communication channel assumption: "we posted it in the official channel" ≠ "everyone saw it." Teams filter out broadcast channels because they're too noisy. The teams that depend on your API the most are the ones most likely to have tuned out the noise | Multi-channel deprecation notification: (1) Slack/Discord announcement, (2) email to team leads of every known consumer, (3) runtime deprecation warning in the API response header, (4) GitHub issue tagged on consumer repos. Track acknowledgment: require a 👍 react or reply indicating the team saw and understood the timeline. Escalate to manager if no acknowledgment within 14 days | Communication ≠ receipt. A deprecation notice nobody saw is functionally identical to no deprecation notice. Multi-channel, track acknowledgment, escalate on silence. The teams you need to reach are the ones most likely to ignore the broadcast channel |
| "30-day deprecation window" announced → slowest internal consumer has a 90-day release cycle. Their next release is 2 months away. 30-day window means they'll ship exactly one release on the old API before being forced to emergency-patch the migration on a Friday | Deprecation timeline set by the deprecating team's velocity, not by the slowest consumer's velocity. "30 days is generous" — for a team that deploys daily. For a team with quarterly releases, 30 days is 1/3 of a release cycle. No consumer velocity assessment before setting the timeline | Measure consumer release cadence before setting deprecation timeline. Timeline = max(slowest_consumer_release_cycle × 2, 90 days). Never set a deprecation window shorter than the slowest consumer's release cycle — you're guaranteeing they can't migrate through their normal process. For external consumers: minimum 6 months for breaking changes | The deprecation clock doesn't tick at the same speed for everyone. Your daily-deploy team's "generous 30 days" is another team's "impossible deadline." The deprecation window is defined by the slowest consumer you're unwilling to break, not by the fastest team's velocity |
| Automated PR opened across 40 consumer repos with the codemod fix. 12 repos fail CI — the codemod doesn't handle TypeScript generics used in those repos. 12 PRs sit open for 3 weeks because the manual fix requires domain knowledge the migration team doesn't have | Codemod tested against 3 "representative" repos that all happened to use similar patterns. The 12 repos with complex TypeScript generics, higher-order functions, or decorators weren't in the test set. No CI pipeline to validate codemod output across all consumers before mass PR | Test codemod against ALL consumer repos — not a sample. Run in dry-run mode: `jscodeshift --dry --print` and validate the output compiles. For repos that fail: either fix the codemod to handle the pattern, or manually migrate and document the pattern. Only open automated PRs for repos where CI passes — manual follow-up for others | The codemod's test coverage is measured by the diversity of consumer code it handles, not by the number of repos tested. 3 repos with similar patterns give false confidence. Test against the full consumer graph — the repos with complex patterns are the ones most likely to break |
| Breaking change deployed, runtime deprecation counter shows 50,000 calls/day still using the old API 6 months after deprecation. Can't remove the old API because "that's real traffic." The old API is now permanent | Deprecation announced but not enforced. No consequences for ignoring the deprecation warning. Consumers learned that "deprecated" means "we suggest you migrate, but nothing bad happens if you don't." Old API has been in "deprecated" status for 18 months | Escalate deprecation: (1) Warning header for 3 months with timeline. (2) Rate limit old API: 10% throttle, increasing 10%/month. (3) Scheduled brownout: old API returns 503 for 5 minutes/week, increasing to 1 hour/day. (4) Hard cutoff at deadline. Communicate the escalation schedule at deprecation announcement so consumers know this is real | "Deprecated" without enforcement means "permanent." Consumers optimize for shipping features, not for migrating off your old API. If nothing breaks when they ignore the deprecation, they will ignore it forever. Brownouts are the most effective enforcement mechanism — a 5-minute weekly outage is annoying enough to motivate migration without being a production incident |
| Consumer-driven contract tests pass in CI → deploy → production errors: "Missing required field: customerId." CI used test fixtures that included `customerId`; real production data from this consumer never includes that field | Contract tests used simplified test data that doesn't reflect actual production traffic patterns. The consumer's CI tested against a mock that included optional fields as if they were always present. The provider's real data is sparser, structured differently, or uses different field names than the test fixtures | Contract tests must use production-derived fixtures — anonymized but structurally identical to real traffic. Sample 1,000 real requests, use them as contract test fixtures. Contracts test: (1) format compatibility (does the JSON parse?), (2) field presence (are required fields present?), (3) value ranges (are timestamps valid? are IDs within expected range?). Run contract tests against production data snapshots, not hand-crafted examples | Simplified test data tests your assumptions, not your contracts. Production data is messier, sparser, and weirder than any hand-crafted fixture. Contract tests with fake data pass while real data fails — the worst possible outcome because it creates false confidence |

## Best Practices

1. **Codemod first, manual second.** Automate 95% of migrations with jscodeshift, comby, or ast-grep. Manual work is error-prone and doesn't scale. Test codemods against 3+ real consumer repos with different code styles before deploying broadly.
2. **Use the Comet pattern for all breaking changes.** Add (new API) → Deprecate (old API with runtime warning) → Remove (old API after 30+ days of zero traffic). Each phase is independently deployable and reversible. Never remove the old API in the same release that adds the new one.
3. **Runtime deprecation counters are non-negotiable.** Every deprecated API must emit a counter metric. Without observability, you're flying blind — you'll either remove an API that still has callers or leave dead code indefinitely. Alert when counters drop to zero for 30 consecutive days.
4. **Consumer-driven contract tests prevent silent breakage.** For APIs with 5+ consumers, implement Pact or Spring Cloud Contract. The provider cannot deploy if any consumer contract fails. This catches breaking changes in CI, not in production.
5. **Progressive rollout with feature flags for behavioral changes.** Wrap new behavior behind a flag, enable for canary consumers first (1% → 10% → 50% → 100%), then remove the old code path after 30 days at 100%. This limits blast radius and enables instant rollback.
6. **Communication cadence scales with impact.** Announce deprecation at least 90 days before removal. Send reminders at 60d, 30d, 14d, 7d, and 1d before sunset. Direct-message consumer maintainers for high-traffic APIs. Include migration guides with before/after code examples.
7. **Consumer discovery must be exhaustive.** Search GitHub org-wide with multiple query variants (different import styles, aliases, dynamic invocations). A single missed call site equals a production outage. Cross-reference with runtime telemetry to confirm completeness.
8. **Every migration plan needs a per-consumer rollback.** If consumer A's migration fails, can they independently revert? Don't force all consumers to roll back because one failed. Feature flags and API versioning enable independent rollback per consumer.
9. **Timeline = slowest consumer deploy cycle × 3.** If a consumer deploys quarterly, your deprecation timeline must be at least 9 months. A consumer that hasn't even seen the deprecation warning before you break them is not a slow-migrator — it's a planning failure.
10. **Contract tests and schema compatibility checks in CI.** Run OpenAPI diff, GraphQL schema validation, or Protobuf backward-compatibility checks on every PR. A breaking schema change must fail CI before it reaches production. Pair with consumer contract verification in the same pipeline.

## Decision Trees **(QUICK)**

### Backwards Compatibility Patterns

```
How to introduce a breaking change without breaking consumers?
|-- Pattern 1: Add-Deprecate-Remove (Comet)
|   |-- Step 1: Add newFunction(args) alongside oldFunction(args)
|   |-- Step 2: Mark oldFunction as @Deprecated (compile-time + runtime warning)
|   |-- Step 3: Wait for all consumers to migrate (monitor with runtime counter)
|   |-- Step 4: Remove oldFunction once counter = 0 for 30 days
|   |-- Best for: function/class renames, parameter changes, return type changes
|   |-- Timeline: 4-12 months depending on consumer deploy cycles

|-- Pattern 2: API Versioning (URL path or header-based)
|   |-- Deploy /api/v2/new-endpoint alongside /api/v1/old-endpoint
|   |-- Consumers opt in to v2 by changing their request path or Accept header
|   |-- Deprecate v1 with Sunset header (HTTP date when v1 goes away)
|   |-- Remove v1 when telemetry shows zero traffic for 30 days
|   |-- Best for: REST APIs with many external consumers
|   |-- Timeline: 6-18 months (external consumers move slowly)

|-- Pattern 3: Feature Flags for API Changes
|   |-- Wrap new behavior behind feature flag: if (featureFlag('new-api')) { newBehavior() } else { oldBehavior() }
|   |-- Enable flag for specific consumers first (canary)
|   |-- Gradually increase: 1% -> 10% -> 50% -> 100%
|   |-- Remove old behavior code after 100% on new for 30 days
|   |-- Best for: behavioral changes where API surface stays the same
|   |-- Timeline: 2-8 weeks per flag rollout

|-- Pattern 4: Protocol Buffer Field Deprecation
|   |-- Add new field (never change field number or type of existing field)
|   |-- Mark old field with [deprecated = true]
|   |-- Reserve old field number after removal: reserved 5;
|   |-- Protobuf backwards compatibility: new servers read old messages, old servers read new messages
|   |-- Best for: gRPC services, protobuf-based message formats
|   |-- Timeline: 3-6 months per field deprecation

|-- Pattern 5: GraphQL @deprecated
|   |-- Add newField to schema alongside oldField
|   |-- Mark oldField: @deprecated(reason: "Use newField instead. Removal: 2026-12-31")
|   |-- GraphQL clients see deprecation in IDE and schema introspection
|   |-- Track oldField usage via resolver instrumentation
|   |-- Remove oldField when usage = 0 for 30 days
|   |-- Best for: GraphQL APIs
|   |-- Timeline: 2-6 months
```

### When NOT to Break

```
Is this cross-repo breaking change actually worth it?
|-- QUANTIFY THE COST:
|   |-- Consumer count: _____ repos
|   |-- Call site count: _____
|   |-- Migration time per consumer: _____ hours × _____ repos = _____ hours total
|   |-- Automated? Codemod possible? __% automatable (savings: _____ hours)
|   |-- Total engineering cost: _____ hours × $150/hr = $_____
|   |-- Opportunity cost: features NOT built during migration = $_____
|   |-- Risk cost: probability of production incident × impact per incident = $_____

|-- QUANTIFY THE BENEFIT:
|   |-- Performance improvement: $_____/year in reduced compute
|   |-- Incident reduction: $_____/year in fewer on-call pages
|   |-- Developer velocity: $_____/year in faster feature development
|   |-- Security improvement: $_____/year in reduced vulnerability surface
|   |-- Maintenance reduction: $_____/year in reduced code to maintain
|   |-- Total annual benefit: $_____

|-- DECISION GATE:
|   |-- If benefit / cost > 3: PROCEED (strong ROI)
|   |-- If benefit / cost 1.5-3: PROCEED with caution, strict timeline enforcement
|   |-- If benefit / cost 1-1.5: QUESTION — is there a cheaper way to achieve the benefit?
|   |-- If benefit / cost < 1: DO NOT BREAK — live with the current API

|-- RED FLAGS (any one = reconsider):
|   |-- 3+ unmaintained consumer repos (nobody to do the migration)
|   |-- External consumers outside your org (you cannot force them to migrate)
|   |-- Migration touches authentication/authorization code (high blast radius)
|   |-- Consumer deploy cycle > 3 months (timeline stretches beyond 1 year)
|   |-- Primary benefit is "cleaner code" (subjective, unquantifiable)
```

### Contract Testing Strategy

```
Should you implement consumer-driven contract tests across repos?
|-- WHEN CONTRACT TESTING IS WORTH IT:
|   |-- 5+ consumers of the same API
|   |-- Consumers are maintained by different teams
|   |-- Breaking changes have caused 2+ production incidents
|   |-- API changes at least quarterly

|-- PACT WORKFLOW (Consumer-Driven Contracts):
|   |-- Step 1: Consumer defines expectations in a Pact test:
|   |   |-- "When I call GET /api/users/123, I expect {id: 123, name: 'Alice'}"
|   |   |-- This generates a Pact contract file (JSON)
|   |-- Step 2: Consumer publishes contract to Pact Broker
|   |-- Step 3: Provider verifies all consumer contracts in CI:
|   |   |-- "Can I satisfy all consumer expectations with my current implementation?"
|   |   |-- If verification fails, provider CANNOT deploy — it would break consumers
|   |-- Step 4: Provider can see which consumers depend on which fields
|   |   |-- "Consumer A only uses id and name. Consumer B uses id and email."
|   |   |-- Provider knows: can I change the address field without breaking anyone?

|-- SPRING CLOUD CONTRACT (Provider-Driven):
|   |-- Provider defines contracts (Groovy DSL or YAML)
|   |-- Consumer-side: generated tests verify consumer code against contracts
|   |-- Best for: JVM ecosystem, provider-controlled API evolution

|-- LIGHTWEIGHT ALTERNATIVES:
|   |-- Schema registry + CI schema compatibility check (e.g., Avro, Protobuf)
|   |-- CI job that runs consumer test suites against provider staging
|   |-- Shared API client library with versioned releases
|   |-- OpenAPI spec validation in CI: does the new spec break consumers?
```

### Codemod Selection Guide

```
Which migration tool should you use for this cross-repo change?
|-- jscodeshift: JavaScript/TypeScript AST-level transforms
|   |-- Best when: complex transformations (reorder arguments, change call patterns, add/remove imports)
|   |-- Requires: Node.js, JS/TS codebase, familiarity with AST concepts (AST Explorer helps)
|   |-- Learning curve: medium (2-5 days to proficiency)
|   |-- Examples: renaming functions with argument reordering, converting callbacks to promises, updating import paths
|   |-- DO NOT use for: non-JS/TS codebases, simple find-replace, config file changes

|-- comby: Structural search-and-replace (regex-like but bracket-aware)
|   |-- Best when: patterns that are structural but don't need full AST awareness
|   |-- Requires: binary install, works on any language
|   |-- Learning curve: low (30 minutes to proficiency)
|   |-- Examples: function renames (same args), type renames, simple API migrations
|   |-- Limitations: cannot reorder arguments easily, limited type awareness
|   |-- DO NOT use for: complex refactors requiring type information, multi-file dependency changes

|-- ast-grep: AST-aware structural search (like comby + tree-sitter)
|   |-- Best when: need AST awareness but want simpler syntax than jscodeshift
|   |-- Requires: binary install, language-specific grammar (tree-sitter)
|   |-- Learning curve: low-medium (1-2 days to proficiency)
|   |-- Examples: cross-language migrations, config-as-code changes, YAML/JSON/TOML transformations
|   |-- Supports: 20+ languages via tree-sitter grammars

|-- semgrep: Pattern-based search with rule composition
|   |-- Best when: finding patterns to migrate (discovery phase), security-focused changes
|   |-- Requires: pip install semgrep, rule files in YAML
|   |-- Learning curve: low (1 day to proficiency)
|   |-- Examples: finding all uses of deprecated API across 50 repos, enforcing migration completion
|   |-- DO NOT use for: the actual migration (find only, no automatic fix in many cases)

|-- Custom Script (Python/Bash/sed): Regex-based
|   |-- ONLY as last resort when no other tool works
|   |-- Best when: config files, markdown, simple text patterns
|   |-- DANGER: regex cannot understand code structure. False positives and false negatives are guaranteed.
|   |-- ALWAYS: test fixtures + manual review of every change
```

### Escalation Patterns for Stuck Migrations

```
What to do when consumers are not migrating:
|-- Diagnose WHY the consumer is stuck:
|   |-- Technical blocker: dependency conflict, breaking test, incompatible version
|   |   |-- Action: pair with consumer team to resolve the technical issue. Extend timeline if needed.
|   |   |-- Signal: consumer tried to migrate, found a problem, stopped
|   |-- Resource constraint: team has higher-priority work, migration is not prioritized
|   |   |-- Action: escalate to engineering manager. Quantify the cost of NOT migrating (incident risk, maintenance burden).
|   |   |-- Signal: consumer acknowledged the need but hasn't allocated time
|   |-- Unmaintained repo: no active maintainer, repo is in "sustaining" mode
|   |   |-- Action A: migrate it yourself (2-5 days to understand codebase + migration time)
|   |   |-- Action B: accept breakage and prepare incident response plan
|   |   |-- Action C: extend deprecation indefinitely (last resort — creates tech debt)
|   |   |-- Signal: no commits in 6+ months, former maintainers have left the team
|   |-- Organizational blocker: team was reorged, ownership unclear, migration fell through cracks
|   |   |-- Action: escalate to director/VP level. Cross-team migrations need organizational support.
|   |   |-- Signal: "we thought Team B owned that" / "that team was disbanded"

|-- Escalation Ladder:
|   |-- Week 1-2 after announcement: direct message to consumer maintainers (friendly reminder)
|   |-- Week 3-4: second reminder, offer pair-programming session
|   |-- Week 5-6: escalate to engineering manager (EM) with quantified impact
|   |-- Week 7-8: EM escalates to director if still blocked
|   |-- Week 9+: director decision: extend timeline, force migration, or accept breakage risk

|-- When to ACCEPT that migration won't complete:
|   |-- Criteria: less than 5% of total call sites remain AND all remaining are in unmaintained repos
|   |-- Action: accept the risk. Remove old API. Monitor for 30 days post-removal.
|   |-- Pre-agreement: get VP-level signoff that the risk of breakage is acceptable
|   |-- DO NOT: silently accept that some consumers will break without organizational awareness

|-- When to EXTEND the timeline:
|   |-- Criteria: >10% of call sites remain after the original deadline
|   |-- Criteria: a critical-path consumer (monolith, payment system) has not migrated
|   |-- Action: communicate new timeline broadly. Explain WHY (not "we're slow" — specific blockers)
|   |-- DO NOT: extend indefinitely. Set a hard, non-negotiable new deadline.

## Error Recovery **(DEEP)**

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

| Scenario | Coordinate With | Why |
|----------|----------------|-----|
| Designing the new API that replaces the old one | api-designer | API design for HEAD, backwards compatibility patterns |
| Managing deprecation lifecycle within a single service | deprecation-engineer | @Deprecated annotations, runtime warnings, removal gates |
| Polyrepo architecture decisions affecting migration | monorepo-manager | Should you even be in polyrepo? Would monorepo simplify this? |
| CI/CD for automated migration PRs | ci-cd-builder | Automated PR CI, canary deployments for breaking changes |
| Cross-repo search and analysis for consumer discovery | code-reviewer | GitHub code search patterns, structural search with comby/ast-grep |
| Full repo migration (not just API change) | migration-architect | Framework migration, language version upgrades, architecture changes |
| Observability for deprecation tracking | observability-engineer | Deprecated API usage dashboards, runtime counter metrics, alerting |
| Security implications of deprecation | security-reviewer | Old API may have vulnerabilities — removal is also a security improvement |
| Breaking changes affecting downstream analytics | data-engineer, analytics-engineer | dbt models, data warehouse schemas, telemetry event definitions |
| Customer-facing API changes referenced in support docs | customer-support-engineer | Troubleshooting guides, runbooks, auto-remediation scripts referencing old behavior |

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `system-architect` | System context, integration points, architectural constraints | Before specialized implementation — understand the system it fits into |

## Proactive Triggers

| # | Trigger Condition | Auto-Response |
|---|------------------|---------------|
| P1 | Function marked @Deprecated but no runtime deprecation counter | [ALERT] Deprecation without observability is blind. Add a runtime counter to track usage before setting a removal date. |
| P2 | Deprecation announced with removal date < 90 days away AND consumers exist with quarterly deploy cycle | [ALERT] Timeline too aggressive. Consumers on quarterly deploy won't even see the deprecation before removal. Extend to 6+ months. |
| P3 | Migration plan lacks consumer contact list | [WARN] Who will do the migration in each consumer repo? Identify maintainers before setting timelines. |
| P4 | Codemod deployed to 5+ repos simultaneously without validation on first 2-3 | [WARN] Batch size too large. Validate on 2-3 repos first, then scale up. A codemod bug at scale is painful to undo. |
| P5 | Deprecated API removal date has passed but TAIL code still exists | [ALERT] Removal date was missed. Reassess: is there still usage? Extend or enforce removal. Indefinite deprecation creates confusion. |
| P6 | Breaking change in library/service that has public/external consumers | [ALERT] External consumers cannot be forced to migrate. API versioning (v1/v2) is the only safe path for public APIs. |
| P7 | Breaking change affects a database column or event property referenced in dbt models, analytics pipelines, or dashboards | [ALERT] 🔴 Breaking a column that feeds a dbt model = breaking the CFO's quarterly report. Scan: (1) `rg -r "column_name\|event_property" dbt_models/ analytics/ telemetry/` across ALL repos, (2) check Mixpanel/Amplitude/PostHog schema registry for the property, (3) check customer support docs for troubleshooting steps referencing this field. Cost of data corruption: $15K-$50K in remediation (per deprecation-engineer analysis). |

## State Log

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.
## What Good Looks Like

```
Ideal cross-repo migration (function rename, 12 consumer repos, 200 call sites):

Month 0: Comet Creation
  Library v2.5.0 ships with newFunction() alongside oldFunction()
  oldFunction() logs WARN + increments counter on every call
  CHANGELOG: "oldFunction() deprecated. Migrate to newFunction(). Removal: v3.0.0 (estimated Jan 2027)"
  Migration guide published with before/after examples

Month 1-2: Codemod + First Consumers
  Codemod transforms oldFunction() -> newFunction() (95% automated, 5% manual edge cases)
  PRs opened for top 5 consumer repos
  3 of 5 merged and deployed
  Dashboard: 40% of call sites migrated

Month 3-4: Remaining Consumers
  PRs opened for remaining 7 repos
  Monthly check-in with consumer teams
  Dashboard: 90% of call sites migrated
  2 repos unresponsive — escalated to engineering manager

Month 5: Cleanup
  Last consumer merges. Dashboard: 100% migrated.
  Runtime counter shows 0 oldFunction() calls for 30 consecutive days.

Month 6: Comet Removal
  Library v3.0.0 ships — oldFunction() removed
  Post-deploy monitoring: zero incidents
  Migration complete. Total cost: ~$75K. Benefit: $120K/year in reduced incidents + maintenance.
```

## Deliberate Practice

```
Phase 1: Consumer discovery
  Take a real function in your codebase. Search GitHub org-wide for all call sites.
  Classify: production vs test, critical vs non-critical, simple vs complex patterns.
  Goal: Understand how far a single function spreads across repos.

Phase 2: Write a simple codemod
  Create a function rename codemod with jscodeshift.
  Write 5 test fixtures (simple, nested, edge cases, negative, async).
  Run against a real repo, review the diff manually.
  Goal: Codemod authoring with confidence.

Phase 3: Design a deprecation timeline
  Pick a function you want to rename. Identify all consumers. Determine their deploy cycles.
  Create a deprecation timeline with specific dates: announcement, first migration, last migration, removal.
  Goal: Realistic timeline estimation.

Phase 4: Build a runtime deprecation counter
  Add a counter to an existing API. Emit it as a metric. Create a dashboard.
  Verify: you can see which consumers call which deprecated APIs in real time.
  Goal: Observability-driven deprecation.

Phase 5: Simulate a failed migration
  Change an API, update only SOME consumers. Observe what breaks.
  Practice rollback. Practice the emergency compatibility shim.
  Goal: Muscle memory for when things go wrong.

Phase 6: Full comet migration (capstone)
  Identify a real candidate. Write the plan. Present the cost-benefit analysis.
  If approved: execute Phases 1-3 (creation, traversal, removal).
  Goal: End-to-end migration experience.
```

## Anti-Patterns

* **A codemod that handles 95% of cases still leaves 5% as manual work — and 5% of 2,000 call sites is 100 manual changes.** Codemod authors consistently underestimate the manual tail. Each manual change requires: reading context, understanding the pattern, applying the fix, testing. At 10 minutes per manual change × 100 sites = 16+ hours of unplanned work. **Total cost: $15K-$50K in manual migration work for the tail end of a codemod that "handles almost everything."**

* **Deprecation warnings in logs that nobody reads are worse than no warnings at all.** If your runtime deprecation counter shows 500 calls/day but nobody has an alert on it, you have a false sense of safety. The counter must trigger a dashboard, which must trigger an alert, which must trigger a ticket. Otherwise you will remove the API while it still has active callers. **Total cost: $30K-$150K per production outage caused by removing a "deprecated but still used" API.**

* **"Just use the latest version" doesn't work for consumers with dependency conflicts.** Consumer A uses `your-lib@2.5` for the new API. But Consumer A also uses `other-lib@1.0` which depends on `your-lib@2.0`. Now Consumer A has a diamond dependency conflict and cannot upgrade until `other-lib` also upgrades. This chains indefinitely. **Total cost: $20K-$80K in blocked migration work across a dependency graph with 3+ levels of transitive dependencies.**

* **GraphQL deprecations are invisible if consumers don't update their schema introspection.** When you deprecate a GraphQL field, consumers see the deprecation in their IDE — IF they re-run introspection. Many teams run introspection once at project setup and never again. They will discover the deprecation when the field disappears, not when you announce it. **Total cost: $10K-$40K in emergency fixes when GraphQL consumers discover breaking changes at runtime, months after the deprecation announcement.**

* **Feature flags for API changes create a combinatorial testing matrix.** If you have 3 API changes behind 3 feature flags, you have 8 (2^3) possible states. Nobody tests all 8. When flag combination {newAuth: true, newPagination: false, newFormat: true} breaks, the root cause is a flag interaction that was never tested. **Total cost: $25K-$75K in debugging flag-interaction bugs across a service with 5+ simultaneously active API feature flags.**

* **Unmaintained consumer repos are deprecation black holes.** A repo with no active maintainers will never migrate. You have 3 options: (1) migrate it yourself (takes 2-5 days to understand unfamiliar codebase), (2) accept that this consumer will break and deal with the incident, (3) never remove the old API. All three options are expensive. **Total cost: $15K-$40K per unmaintained consumer repo, either in migration labor or production incident cost.**

* **Contract tests prevent regressions but don't prevent design mistakes.** If Consumer A's Pact test says "I expect field `address` to be a string," and you change `address` to an object (breaking change), the Pact test fails — good. But if Consumer A's Pact test was never written, you have no protection. Contract testing works only for the consumers who have actually written tests. **Total cost: $20K-$60K in undiscovered breaking changes for consumers without contract tests, discovered only after production deploy.**

* **Codemods that modify import paths can break barrel exports and tree shaking.** If a codemod changes `import { foo } from './old-module'` to `import { foo } from './new-module'`, but `./new-module` has different barrel re-exports, downstream consumers of the consumer may also break. Codemods operate on single repos — they cannot see transitive effects. **Total cost: $12K-$35K in cascading breakages when a codemod in Repo A causes import errors in Repo B that depends on Repo A.**

## Anti-Rationalization — No Excuses

| Rationalization | Reality |
|---|---|
| "We'll just grep and manually update all call sites" | Manual grep misses 10-25% of call sites (aliases, dynamic imports, reflection); each missed site is a production outage discovered by a user, not a test — cost is multiplied across all consumers |
| "We can deprecate the old API in one release cycle" | Consumer repos have deploy cycles from daily to quarterly; one cycle means the slowest consumer hasn't even seen the deprecation warning before you break them in production |
| "Codemods are overkill for a small refactor" | A "small" refactor of 50 call sites across 8 repos still takes 40+ hours manually; a 2-hour codemod script handles it with zero human error and comprehensive test coverage |
| "Breaking changes are fine if we communicate them clearly" | Communication doesn't prevent breakage; a breaking change taking down 3 consumer repos costs 15-30 engineering-hours in emergency response across teams that don't report to you |
| "We don't need contract tests; we'll manually verify" | Without contract tests, every consumer API change is Russian roulette — you discover breakage when consumers deploy to production, not when you make the change |

## Verification

After planning or executing a cross-repo refactoring, run this sequence. Do not proceed past a failure.

1. **Consumer inventory completeness:** `org:my-org <function-name>` GitHub search returns 0 additional call sites not in the migration plan. Re-run search with variants (different import styles, aliases).
2. **Codemod test fixtures:** All test fixtures pass: output matches expected, negative cases unchanged. Test against 3 real consumer repos — diffs are correct and complete.
3. **Blast radius documentation:** Consumer count, call site count, deploy cycle analysis, maintainer list all documented and current (within 1 week).
4. **Deprecation observability:** Runtime deprecation counter exists, dashboard shows per-consumer usage, alert fires if counter exceeds threshold.
5. **Timeline feasibility:** Deprecation removal date is at least (slowest deploy cycle × 3) days in the future. All consumer maintainers have acknowledged the timeline.
6. **Rollback plan:** Documented rollback procedure for every consumer. Contact list for emergency rollback coordination.
7. **Benefit exceeds cost:** Documented cost-benefit analysis with ratio > 1.5. Decision record with approval.

If any check fails: diagnose from verification item, provide specific actionable fix, restart verification from failed item.

## Verification Guardrails

Before delivering work, the agent must verify:

- [ ] **Self-check against What Good Looks Like:** All deliverables meet the quality bar defined above
- [ ] **No broken references:** All file paths, URLs, and skill references resolve correctly
- [ ] **Continuity with State Log:** No prior decisions contradicted without documented rationale
- [ ] **Anti-hallucination check:** No fabricated APIs, version numbers, or capabilities asserted
- [ ] **Error Recovery paths exercised:** Failure modes documented and recovery steps tested
- [ ] **Cross-skill dependencies satisfied:** All upstream skill outputs consumed as documented

If any checkbox fails, revise before delivering. When all pass, add to the state log.

## Production Checklist **(DEEP)**

- [ ] **[S1]** Consumer inventory is exhaustive: GitHub org-wide search with variants (import styles, aliases, dynamic invocations) returns zero additional call sites not in the migration plan. Cross-referenced with runtime telemetry.
- [ ] **[S2]** Codemod test fixtures cover: simple case, nested usage, edge cases (null, undefined, empty), negative cases (should NOT change), async/await variants. Tested against 3+ real consumer repos with manual diff review.
- [ ] **[S3]** Runtime deprecation counter exists and emits metrics. Dashboard shows per-consumer usage. Alert fires if counter exceeds threshold or drops to zero for 30 consecutive days.
- [ ] **[S4]** Deprecation timeline: removal date is at least (slowest consumer deploy cycle × 3) days in the future. All consumer maintainers have acknowledged the timeline in writing.
- [ ] **[S5]** Migration guide published with: before/after code examples for every affected pattern, common pitfalls and workarounds, timeline with specific dates, contact for migration support.
- [ ] **[S6]** Rollback plan per consumer: documented procedure for reverting the migration independently. Contact list for emergency rollback coordination. Tested in staging within the last 30 days.
- [ ] **[S7]** Contract tests pass: all consumer Pact/SCC contracts verified against the new provider version in CI. Zero contract failures. Schema compatibility check (OpenAPI diff, protobuf backward-compatibility) passes.
- [ ] **[S8]** Cost-benefit analysis documented: total engineering cost, opportunity cost, risk cost vs. performance improvement, incident reduction, velocity gain. Benefit/cost ratio > 1.5 with VP-level approval.
- [ ] **[S9]** Comet pattern phases tracked: ADD (new API deployed), DEPRECATE (old API with runtime warning), REMOVE (old API confirmed zero traffic for 30 days). Each phase independently deployed.
- [ ] **[S10]** Feature flags for behavioral changes: canary rollout path (1% → 10% → 50% → 100%) with monitoring gates at each step. Instant rollback via flag toggle.
- [ ] **[S11]** Dead code removal after deprecation: old API code, tests, documentation, and related configuration all removed. No commented-out code referencing the deprecated surface remains.
- [ ] **[S12]** Retrospective completed: what went smoothly, what surprised us, were migration tools adequate, was the timeline realistic. Lessons documented and fed back into the deprecation playbook.

## References

* [jscodeshift Documentation](https://github.com/facebook/jscodeshift) — JavaScript/TypeScript codemod toolkit
* [comby Documentation](https://comby.dev/) — Structural code search and replace
* [ast-grep Documentation](https://ast-grep.github.io/) — AST-based structural search
* [Pact Documentation](https://docs.pact.io/) — Consumer-driven contract testing
* [/references/comet-migration.md](references/comet-migration.md) — HEAD/TAIL/COMET three-phase framework with timelines
* [/references/backwards-compatibility.md](references/backwards-compatibility.md) — API versioning, feature flags, protobuf, GraphQL patterns
* [/references/consumer-discovery.md](references/consumer-discovery.md) — GitHub search, registry analytics, runtime dependency graphs
* [/references/migration-tooling.md](references/migration-tooling.md) — jscodeshift, comby, ast-grep, automated PR generation
* [/references/deprecation-communication.md](references/deprecation-communication.md) — Changelogs, migration guides, runtime warnings
* [/references/contract-testing.md](references/contract-testing.md) — Pact, Spring Cloud Contract, schema compatibility
* [/references/risk-assessment.md](references/risk-assessment.md) — Blast radius quantification, rollback planning
* [/references/when-not-to-break.md](references/when-not-to-break.md) — Cost-benefit analysis framework for breaking changes
