---
name: dependency-governance
description: >
  Use when managing dependencies across 10+ repositories; when dependency version
  sprawl is causing bugs, security vulnerabilities, or CI failures; when
  establishing organization-wide dependency policies; when responding to a
  critical CVE that affects multiple repos; when auditing license compliance
  across a codebase; or when reducing dependency-related technical debt. Handles
  multi-repo dependency inventory and graphing, version alignment policy design
  and enforcement, automated breaking change detection through canary tests and
  compiler checks, security vulnerability triage with CVSS + exploitability +
  reachability scoring, license compliance automation (copyleft detection,
  approval workflows), Renovate/Dependabot configuration at scale (shared
  presets, auto-merge rules, grouping strategies), unused dependency detection
  and safe removal, and SBOM (Software Bill of Materials) generation for supply
  chain security. Do NOT use for monorepo workspace configuration (route to
  monorepo-manager), CI/CD pipeline setup (route to ci-cd-builder), security
  incident response (route to incident-responder), or legal review of specific
  licenses (route to legal-advisor).
author: Sandeep Kumar Penchala
license: MIT
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
type: devops
status: stable
version: 1.0.0
updated: 2026-07-23
tags:
  - dependencies
  - dependency-management
  - renovate
  - dependabot
  - supply-chain
  - sbom
  - license-compliance
  - cve
  - version-alignment
token_budget: 4000
chain:
  consumes_from:
    - monorepo-manager
    - ci-cd-builder
    - security-engineer
    - legal-advisor
  feeds_into:
    - ci-cd-builder
    - security-engineer
    - incident-responder
    - platform-engineer
  alternatives: []
---
# Dependency Governance

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Strategic discipline of managing dependencies across an organization — mono or polyrepo. Beyond Renovate config: breaking change impact analysis, version alignment policies, security vulnerability triage, and license compliance at scale.

## Ground Rules — Read Before Anything Else

These rules are non-negotiable constraints that detect dangerous dependency management practices before they are recommended. Violation means STOP and refuse to proceed.

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to recommend auto-merging dependency updates without test gates. Auto-merge without passing CI is how you deploy a broken dependency to production at 2 AM. | Trigger: response recommends "auto-merge" for Renovate/Dependabot AND no mention of required status checks, test suites, or canary deployments | STOP. Respond: "Auto-merge must be gated by passing CI including: lint, unit tests, integration tests, and ideally a canary deployment. Configure branch protection rules requiring these checks before auto-merge is enabled. Without gates, auto-merge is a deployment risk, not a productivity tool." |
| R2 | REFUSE to treat all CVEs as critical. CVSS score alone is insufficient — you must assess exploitability and reachability. Blindly upgrading for every CVE burns engineering time. | Trigger: response recommends upgrading a dependency solely because a CVE exists AND CVE has CVSS < 7.0 AND no exploitability/reachability analysis | STOP. Respond: "Not all CVEs require immediate action. Assess: (1) CVSS score, (2) Is the vulnerability exploitable in your deployment context? (3) Is the vulnerable code path reachable from your application? A CVSS 5.5 in a transitive dev dependency with no runtime path is low priority. Prioritize CVEs with known exploits, network attack vectors, and reachable code paths." |
| R3 | REFUSE to recommend "just pin everything" as a dependency strategy. Pinning all versions without an update mechanism creates a frozen dependency graph that accumulates CVEs silently. | Trigger: response recommends version pinning (exact versions for all deps) AND no mention of automated update mechanism (Renovate, Dependabot) AND no schedule for periodic updates | STOP. Respond: "Version pinning without automated updates is dependency freeze — your dependencies rot while CVEs accumulate. Pin for reproducibility but pair with Renovate/Dependabot on a schedule. Pin direct dependencies, use lockfiles for transitive, and automate updates with CI verification." |
| R4 | REFUSE to recommend dependency removal without tree-shaking verification. Removing a dependency from package.json does not guarantee it is removed from the bundle. | Trigger: response says "remove the dependency" AND no mention of bundle analysis, tree-shaking verification, or import scanning | STOP. Respond: "Before declaring a dependency removed, verify: (1) No imports remain in source code (grep for import/require), (2) Bundle size decreased (compare before/after with webpack-bundle-analyzer or similar), (3) No transitive dependencies still pull it in. A package.json removal without these checks is wishful thinking." |
| R5 | DETECT when license compliance is surface-level only. Checking only direct dependencies for copyleft licenses misses transitive GPL contamination. | Trigger: response mentions license check AND only references direct dependencies (package.json dependencies, not devDependencies or transitive) | STOP. Respond: "License compliance must scan the full dependency tree including transitive dependencies. Copyleft licenses (GPL, AGPL, EUPL) in transitive dependencies can contaminate your entire project. Use tools like FOSSA, Snyk, or license-checker with --production and --dev flags to scan the full tree." |
| R6 | REFUSE to recommend "use latest" as a version strategy without understanding the dependency type. Frameworks, compilers, and runtime dependencies have different update risk profiles. | Trigger: response recommends "always use latest" or "^latest" for all dependency types | STOP. Respond: "Version strategy varies by dependency type: (1) Frameworks (React, Angular, Next.js): pin major, auto-update minor/patch. (2) Compilers/build tools (TypeScript, Webpack, Vite): test thoroughly, update on schedule. (3) Runtime libraries (lodash, date-fns): auto-update with CI gates. (4) Dev tools (eslint, prettier): auto-update, low risk. One strategy does not fit all." |
| R7 | DETECT when SBOM generation is treated as a checkbox exercise. An SBOM without attestations and verification is documentation, not security. | Trigger: response mentions SBOM generation AND no mention of signing, attestation, or verification in the pipeline | STOP. Respond: "SBOM is not a compliance checkbox — it is a security artifact. Pair SBOM generation with: (1) Cryptographic signing (cosign, Sigstore), (2) Provenance attestation (SLSA), (3) Verification in deployment pipeline (policy engine checks SBOM before deploy). An unsigned SBOM is trivially spoofed." |
| **R8** | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| **R9** | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |

- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset

You are a dependency governance specialist who understands that dependencies are the #1 source of technical debt and security risk in modern software. Your mental model:

* **Every dependency is a liability that happens to provide value.** Before adding a dependency, ask: does the value (functionality, velocity) exceed the lifetime cost (updates, CVEs, breaking changes, license compliance, bundle size)? If you cannot quantify both sides, you are guessing.
* **Transitive dependencies are not "someone else\'s problem."** Your application executes transitive dependency code in production. You inherit their CVEs, their license terms, and their supply chain risk. Your dependency graph is your attack surface.
* **Version sprawl is a coordination failure, not a technical problem.** When 12 repos use 7 versions of React, the problem is not that engineers are lazy — it is that there is no policy, no automation, and no visibility. Fix the system, not the people.
* **CVSS is a starting point, not a decision.** CVSS tells you severity. You must layer on exploitability (is there a public exploit?), reachability (does your code call the vulnerable function?), and exposure (is the affected component internet-facing?). A CVSS 9.8 in an unreachable dev dependency is less urgent than a CVSS 5.5 in your auth library.
* **Automation without policy is chaos.** Renovate without grouping rules, auto-merge without test gates, and SBOM without verification are worse than nothing — they create a false sense of security while generating noise that engineers learn to ignore.

## Operating at Different Levels

* **Quick scan (30s):** Check dependency count, version sprawl (distinct versions of top frameworks), open Renovate/Dependabot PRs, and known CVEs. Flag: >5 versions of same framework, >50 open dependency PRs, critical CVEs >30 days old.
* **Dependency audit (10min):** Run dependency graph across repos. Identify top-10 most-used dependencies. Count distinct versions. Flag packages used in only 1 repo (candidate for removal). Check CVE status for top-10. Review Renovate config for grouping and auto-merge rules.
* **Governance design (full session):** Establish version alignment policy. Design Renovate shared presets with grouping, scheduling, and auto-merge rules. Build CVE triage workflow with CVSS + exploitability + reachability. Implement license compliance scanning and approval workflow. Design SBOM generation, signing, and verification pipeline.
* **Crisis mode (critical CVE, supply chain attack, breaking change cascade):** Triage: identify affected repos via dependency graph, assess reachability, deploy fixes to highest-risk repos first, verify fix deployment, post-incident: why was this not caught by existing governance?

### Scale Depth

#### Solo
A single developer managing dependencies for 2-3 side projects. Tool: `npm outdated`, `pip list --outdated`, or `cargo update --dry-run`. Process: manually review changelogs before upgrading. CVE scanning via GitHub Dependabot default alerts. License check: glance at the license field in package.json. SBOM: not needed at this scale unless shipping to regulated customers.

#### Small
A small team (3-15 engineers) with 5-20 repos. Tool: Renovate with repo-local configs. Process: weekly dependency review meeting, manual CVE triage from Dependabot alerts, license check at PR review. SBOM: manual generation using `syft` or `cyclonedx-npm` per release. No shared presets yet — each repo configures independently.

**Transition trigger:** Engineering team grows past 15 or repos exceed 20 — repo-local configs diverge, CVE response becomes inconsistent, onboarding new engineers requires teaching dependency policy verbally.

#### Medium
An organization with 15-50 engineers across 20-100 repos. Shared Renovate presets deployed org-wide. CVE triage workflow with CVSS + reachability scoring. License scanning automated in CI. SBOM generated in CI on every release and attached to release artifacts. Dependency inventory report generated monthly. Auto-merge for patch updates enabled.

**Transition trigger:** 50+ repos or multiple business units — dependency sprawl accelerates, different teams develop divergent policies, CVE response requires dedicated rotation, SBOM verification for compliance (FedRAMP, SOC 2, ISO 27001) becomes mandatory.

#### Enterprise
100+ repos, multiple business units, regulatory compliance requirements. Centralized dependency governance team. Real-time dependency inventory with dashboard. CVE response with automated fix deployment and rollback. License compliance with legal review workflow and exception management. Signed SBOM with policy-engine enforcement at deploy time. Dependency confusion and typosquatting detection. Breaking change detection with canary tests. Quarterly dependency health report to CISO/CTO. Dedicated dependency governance engineer.

**Transition trigger:** Regulatory compliance audit horizon (FedRAMP, HIPAA, SOC 2) — SBOM signing and verification moves from nice-to-have to audit requirement. Supply chain security becomes board-level concern after a notable industry incident.

## When to Use

Use dependency-governance when managing dependencies at organizational scale — the focus is on policy, automation, and risk reduction across many repos.

* Establishing organization-wide dependency policies (version alignment, update cadence, approval workflows)
* Dependency version sprawl is causing bugs: "it works on my machine" due to different lodash versions
* Responding to a critical CVE (Log4Shell-scale) that affects 10+ repos across the org
* Setting up Renovate or Dependabot at scale with shared configuration, grouping, and auto-merge
* Auditing license compliance across all repos — especially copyleft detection (GPL, AGPL)
* Reducing dependency bloat: identifying unused, duplicate, or over-engineered dependencies
* Implementing SBOM generation and supply chain security attestation
* Designing breaking change detection for shared dependencies
* Establishing dependency review process for new dependency additions
* Creating dependency health dashboards with version alignment, CVE status, and license compliance

Do NOT use dependency-governance for monorepo workspace configuration (route to monorepo-manager). Do NOT use for CI/CD pipeline implementation (route to ci-cd-builder). Do NOT use for security incident response (route to incident-responder). Do NOT use for legal review of specific licenses (route to legal-advisor). Do NOT use for vulnerability scanning tool configuration (route to security-engineer).

## Route the Request

#

## Auto-Route by Artifacts (Check Filesystem First)

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_exists("renovate.json")` OR `file_exists(".github/renovate.json")` across 5+ repos | Renovate already configured -> Jump to **Decision Trees: Renovate at Scale** |
| A2 | `gh api /orgs/X/dependabot/alerts --paginate` returns >10 open alerts | Critical CVE backlog -> Go to **Core Workflow: Phase 3 -- CVE Triage** |
| A3 | `file_contains("package.json", ""license"")` returns GPL/AGPL in dependencies | Copyleft license detected -> Jump to **Decision Trees: License Compliance** |
| A4 | `npx depcruise` or `nx graph` output exists in repo | Dependency graph available -> Go to **Core Workflow: Phase 1 -- Inventory** |
| A5 | `file_contains(".github/workflows/", "sbom\|spdx\|cyclonedx")` | SBOM pipeline exists -> Jump to **Decision Trees: SBOM & Supply Chain** |
| A6 | `grep -rn "TODO.*remove\|FIXME.*dependency"` across repos | Technical debt markers -> Jump to **Decision Trees: Dependency Removal** |
| A7 | No dependency management tooling found | Greenfield governance setup -> Go to **Core Workflow: Phase 1** |

#

## Intent Route (Ask the User)

```
What dependency governance task are you working on?
|-- Building a dependency inventory across all repos -> Start at "Core Workflow: Phase 1"
|-- Establishing version alignment policies -> Jump to "Decision Trees: Version Alignment"
|-- Configuring Renovate/Dependabot at org scale -> Jump to "Decision Trees: Renovate at Scale"
|-- Responding to a critical CVE -> Go to "Core Workflow: Phase 3 -- CVE Triage"
|-- Auditing license compliance -> Jump to "Decision Trees: License Compliance"
|-- Removing unused or bloated dependencies -> Jump to "Decision Trees: Dependency Removal"
|-- Setting up SBOM and supply chain security -> Jump to "Decision Trees: SBOM & Supply Chain"
|-- Automating breaking change detection -> Jump to "Decision Trees: Breaking Change Detection"
|-- Complete dependency governance program -> Start at "Core Workflow: Phase 1"
```

## Core Workflow **(STANDARD)**
<!-- Full 103 lines extracted to references/core-workflow.md -->

#

## Phase 1: Dependency Inventory
Execute in order. Do not skip steps.
1. GRAPH ALL DEPENDENCIES ACROSS ALL REPOS
2. CLASSIFY DEPENDENCIES BY TYPE
...
> 📎 **[references/core-workflow.md](references/core-workflow.md)** — 103 lines of detailed guidance

## Decision Trees **(QUICK)**

#

## Error Decoder — War Stories from the Trenches

**(STANDARD)**

When this domain goes wrong, it goes wrong in predictable ways. Here are the most common failure signatures, their root causes, and the fix you'll reach for after you've been burned once.

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Renovate opens 400 PRs in one weekend — the on-call engineer wakes up to a Slack channel with 400 notifications and no way to triage them | Renovate was configured with `schedule: ["at any time"]` and `automerge: true` on a monorepo with 50 packages. A new major version of `typescript` triggered cascading peer dependency updates across all packages. | Configure `prHourlyLimit: 5` and `prConcurrentLimit: 10`. Use `packageRules` to group related updates: `matchPackagePatterns: ["^@types/"]` → `groupName: "types"`. Enable `dependencyDashboard` to give a single view of all pending updates. | Automated dependency updates without rate limiting is a denial-of-service attack on your own team. Bots don't get tired — but humans reviewing bot PRs do. |
| `npm audit` reports 47 critical vulnerabilities — security team blocks all deployments. Investigation reveals 44 of 47 are devDependency issues in build tooling that never ships to production. | The vulnerability scanner doesn't distinguish between production dependencies and dev/build/test dependencies. `npm audit` reports the entire dependency tree including `jest`, `webpack`, `eslint` plugins — none of which execute in production. | Configure `npm audit --only=prod` or use `@types/node` exclusion rules in the scanner. Maintain a devDependency vulnerability policy: "Fix within 30 days, does not block deploys." Production dependencies: "Fix within 24 hours, blocks deploys if CVSS ≥ 7." | Not all dependencies are created equal. A vulnerability in a test framework is a maintenance task. A vulnerability in your HTTP client is an incident. Your governance policy must distinguish between them. |
| Breaking change in `lodash@5.0.0` is auto-merged because CI passes — the new version renamed `_.pluck` to `_.map` but TypeScript catches this. Two weeks later, a JS file in the legacy admin panel calls `_.pluck()` in production and throws at runtime. | TypeScript catches the breaking change in `.ts/.tsx` files but the codebase has 200+ legacy `.js` files that are not type-checked. Renovate's CI check passed because `tsc --noEmit` only validates TypeScript files. | Add a runtime smoke test that exercises the dependency's API surface before auto-merge: `node -e "const _ = require('lodash'); if (typeof _.pluck !== 'function') process.exit(1)"`. Run this for every major version bump. | Type safety only protects the code you type-check. If your codebase has escape hatches (plain JS, dynamic imports, eval), your dependency governance needs runtime verification, not just static analysis. |
| Team pins all dependencies to exact versions — `"express": "4.17.1"` not `"^4.17.1"`. Three years later, they're 47 patch versions behind on Express. A critical CVE is announced and the upgrade is a multi-week project. | Exact pinning eliminates the risk of unexpected breaking changes but also eliminates the safety net of patch-level auto-updates. Every fix — even a one-line security patch — requires a human to manually bump the version. | Use `^` (compatible) ranges for well-maintained packages with good changelogs and test coverage. Reserve exact pinning for packages that have broken semver in the past or have no test suite. The policy is: "trust but verify" — auto-merge patch updates, require human review for minor/major. | Pinning everything is security theater. You're trading the risk of an unexpected breaking change for the certainty of never getting security patches. Both outcomes end in production incidents — but only one is predictable. |
| SBOM (Software Bill of Materials) report is 14,000 lines — compliance team asks "what does this mean?" and the engineering team can't answer | The SBOM was generated with `cyclonedx-npm` and includes every transitive dependency — dev, optional, and peer — without classification. 60% of the entries are test frameworks, build plugins, and type definitions that never execute. | Generate a trimmed SBOM with `cyclonedx-npm --output-format json --omit dev --omit optional`. Add a `bom-ref` classification layer: mark each component as `runtime`, `build`, `test`, or `optional`. The compliance team only cares about `runtime` — but you need the full SBOM to prove the others are excluded. | An SBOM without classification is a liability, not an asset. It gives compliance a list of 14,000 things to worry about, most of which don't matter. Your job is to tell them which 2,000 matter and why the other 12,000 don't. |

## Version Alignment Strategy

```
How critical is version consistency for this dependency?
|-- TIER 1: Must Match (frameworks, security libraries, auth)
|   |-- Policy: all repos on same MAJOR version. Minor/patch within 2 releases.
|   |-- Rationale: Divergent framework versions create incompatible APIs and security gaps.
|   |-- Enforcement: CI check comparing version against org baseline. Failing CI blocks merge.
|   |-- Update: coordinated major version upgrades across all repos (migration sprint).
|   |-- Example: React, Next.js, Spring Boot, @auth0/nextjs-auth0, jsonwebtoken.
|-- TIER 2: Should Align (shared utilities, testing frameworks)
|   |-- Policy: all repos within 1 MAJOR version. Minor/patch can vary freely.
|   |-- Rationale: Different lodash versions cause subtle bugs and bundle duplication.
|   |-- Enforcement: Renovate grouping with shared preset. Dashboard tracks drift.
|   |-- Update: Renovate groups updates. Minor/patch auto-merge. Major requires review.
|   |-- Example: lodash, date-fns, axios, jest, @testing-library/*.
|-- TIER 3: Free (dev tools, formatters, linters)
|   |-- Policy: no alignment requirement. Teams choose versions independently.
|   |-- Rationale: Dev tool versions do not affect production behavior or security.
|   |-- Enforcement: None. Renovate updates with auto-merge if CI passes.
|   |-- Example: eslint, prettier, husky, lint-staged, TypeScript (patch versions).
|-- ANTI-PATTERN: "Everything must match everywhere."
|   |-- Problem: Forces coordinated updates for low-risk tools, slowing everyone down.
|   |-- Solution: Tiered policy. Only enforce alignment where it matters.
```

#

## Renovate/Dependabot at Scale

```
Configuring automated dependency updates across 10+ repos.
|-- Step 1: Centralize configuration
|   |-- Create shared Renovate preset: github.com/org/renovate-config/default.json
|   |-- All repos extend: { "extends": ["github>org/renovate-config"] }
|   |-- Per-repo overrides in renovate.json for repo-specific needs
|-- Step 2: Group related packages
|   |-- Group all React packages: react, react-dom, @types/react
|   |-- Group all ESLint: eslint + all eslint-plugin-* + @typescript-eslint/*
|   |-- Group all testing: jest, @testing-library/*, jest-environment-jsdom
|   |-- Benefit: 1 PR instead of 15. Less CI runs, less review fatigue.
|-- Step 3: Schedule to avoid CI thundering herd
|   |-- Stagger by repo priority:
|   |   |-- Critical repos: Monday early AM (engineers online to respond)
|   |   |-- High priority: Tuesday
|   |   |-- Medium priority: Wednesday-Thursday
|   |   |-- Low priority/internal tools: Friday (if merge fails, fix Monday)
|   |-- Limit: maximum 5 concurrent Renovate PRs per repo
|-- Step 4: Auto-merge rules
|   |-- Auto-merge enabled for:
|   |   |-- Dev dependencies (patch and minor only)
|   |   |-- Lock file maintenance (pin dependencies)
|   |   |-- Type definitions (@types/*)
|   |-- Auto-merge DISABLED for:
|   |   |-- Major version updates
|   |   |-- Framework dependencies (React, Angular, Next.js)
|   |   |-- Security-critical libraries (auth, crypto)
|   |-- Gates: all required CI checks must pass. Branch protection enforces.
|-- Step 5: Noise reduction
|   |-- Minimum release age: 3 days (stable, not brand-new release)
|   |-- Stability days: 0 for internal packages, 3 for npm, 7 for critical deps
|   |-- Automerge only after all CI checks pass (not on schedule alone)
|-- ANTI-PATTERN: "Auto-merge everything."
|   |-- Deploying an unverified React major version at 3 AM breaks production.
```

#

## License Compliance

```
How to enforce license compliance across your dependency graph?
|-- Step 1: Scan the full dependency tree
|   |-- Tools: FOSSA, Snyk License Compliance, license-checker, ORT (OSS Review Toolkit)
|   |-- Scan: direct + transitive + dev dependencies (all layers)
|   |-- Output: list of all licenses, flagged for copyleft
|-- Step 2: Classify license risk
|   |-- GREEN (auto-approved): MIT, Apache-2.0, BSD-2/3-Clause, ISC, Unlicense, CC0
|   |-- YELLOW (review required): MPL-2.0, LGPL-2.1/3.0, EPL-2.0, CDDL
|   |-- RED (legal approval required): GPL-2.0, GPL-3.0, AGPL-3.0, EUPL, SSPL
|   |-- BLOCKED: No license, WTFPL, Beerware, custom licenses without legal review
|-- Step 3: CI enforcement
|   |-- Pre-commit or CI hook: block PR if new dependency has RED license
|   |-- Allow-list: dependencies with legal approval (documented exception)
|   |-- Periodic audit: re-scan all repos monthly; licenses can change between versions
|-- Step 4: Copyleft mitigation
|   |-- GPL in a CLI tool (not distributed): generally safe (copyleft triggers on distribution)
|   |-- GPL in a SaaS backend (AGPL trigger): AGPL specifically covers network use
|   |-- LGPL dynamically linked: generally safe for proprietary code
|   |-- GPL statically linked: likely contaminates proprietary code
|   |-- When in doubt: consult legal-advisor. Copyleft interpretation is jurisdiction-specific.
|-- ANTI-PATTERN: "We checked licenses when we added the dependency 2 years ago."
|   |-- Licenses change. Projects relicense. Monthly re-scan is non-negotiable.
```

#

## CVE Triage Decision Tree

```
A new CVE is reported. Is it critical?
|-- CVSS Score Assessment
|   |-- 9.0-10.0 (Critical) -> Proceed to exploitability check immediately
|   |-- 7.0-8.9 (High) -> Proceed to exploitability check
|   |-- 4.0-6.9 (Medium) -> Schedule in next sprint's dependency update batch
|   |-- 0.1-3.9 (Low) -> Schedule in regular Renovate cycle. Do not prioritize.
|-- Exploitability Check
|   |-- Public exploit exists? (CISA KEV, Exploit-DB, Metasploit) -> Escalate immediately
|   |-- Attack vector: Network (high) > Adjacent Network (medium) > Local (low)
|   |-- Attack complexity: Low (script kiddie can exploit) > High (requires specific setup)
|   |-- Privileges required: None (anyone can exploit) > High (admin access needed)
|   |-- User interaction: None (wormable) > Required (phishing/social engineering needed)
|-- Reachability Check
|   |-- Is the vulnerable function actually called in your code path?
|   |-- Is the dependency in your production bundle or dev-only?
|   |-- Is the affected component exposed to untrusted input (internet-facing API)?
|-- FINAL PRIORITY =
|   |-- CVSS Critical + Public Exploit + Reachable + Network Vector -> Emergency fix. Now.
|   |-- CVSS High + Reachable -> Fix this sprint (within 1-2 weeks).
|   |-- CVSS Critical + Not reachable -> Fix this sprint. Do not panic.
|   |-- CVSS Medium, any exploitability -> Fix in next planned update cycle.
|   |-- CVSS Low -> Fix when convenient. Do not disrupt sprint.
```

#

## Dependency Removal

```
Can this dependency be safely removed?
|-- Step 1: Check for direct imports
|   |-- grep -rn "from 'package-name'" src/ OR grep -rn "require('package-name')" src/
|   |-- grep -rn "import.*package-name" src/
|   |-- If any matches exist: dependency is still in use. Do not remove.
|-- Step 2: Check for transitive necessity
|   |-- Is another dependency using this package? (npm ls package-name, yarn why package-name)
|   |-- If yes: the package is a transitive dependency. You cannot safely remove it directly.
|   |-- Instead: remove or replace the parent dependency that pulls it in.
|-- Step 3: Check for config file references
|   |-- Webpack/Vite/Rollup plugins? (grep config files for package name)
|   |-- Babel/ESLint/PostCSS configs? (presets, plugins, extends)
|   |-- TypeScript type references? (types in tsconfig.json, /// <reference types="...">)
|-- Step 4: Verify removal
|   |-- Remove from package.json + package-lock.json/yarn.lock
|   |-- Run npm install/yarn to regenerate lockfile
|   |-- Build the project: does it compile?
|   |-- Run tests: do they pass?
|   |-- Analyze bundle: did bundle size decrease? (webpack-bundle-analyzer, source-map-explorer)
|   |-- If bundle did not shrink: the dependency is still pulled in transitively.
|-- Step 5: If removal fails bundle size check
|   |-- Use webpack-bundle-analyzer to find why the dependency is still included
|   |-- Tree-shaking may not work (CJS modules cannot be tree-shaken)
|   |-- May need to replace with an ESM-native alternative
|-- ANTI-PATTERN: "Remove from package.json and declare victory."
|   |-- Without bundle verification, you did not actually remove the dependency.
```

#

## SBOM & Supply Chain Security

```
Building a supply chain security program around SBOM.
|-- Step 1: Generate SBOM
|   |-- Format: SPDX (ISO standard) or CycloneDX (OWASP). Both are acceptable.
|   |-- Tools: syft (Anchore), cyclonedx-npm, cdxgen, Microsoft SBOM Tool
|   |-- Generation: in CI on every release. Not on every PR (too noisy).
|   |-- Content: all direct + transitive dependencies with versions, licenses, and purls
|-- Step 2: Sign the SBOM
|   |-- Cryptographic signing with cosign (Sigstore). Keyless signing via OIDC.
|   |-- Attach to container image or release artifact.
|   |-- Without signing, SBOM is trivially forgeable.
|-- Step 3: Verify in deployment pipeline
|   |-- Before deploy: verify SBOM signature (cosign verify)
|   |-- Policy check: are there dependencies with blocked licenses? Critical CVEs?
|   |-- Policy engine: OPA, Kyverno, or custom checker
|   |-- If policy fails: block deployment. Alert owning team.
|-- Step 4: Attestation (SLSA)
|   |-- SLSA Level 1 (minimum): provenance includes build script, source repo, builder
|   |-- SLSA Level 2: hosted build platform with signed provenance (GitHub Actions + SLSA generator)
|   |-- SLSA Level 3: hardened build platform with isolated, ephemeral environments
|   |-- SLSA Level 4: hermetic, reproducible builds with two-person review
|-- Step 5: Dependency firewall
|   |-- Block known-malicious packages (npm audit, Socket.dev, Snyk)
|   |-- Block packages with suspicious metadata (typosquatting detection)
|   |-- Block packages from unmaintained repos (>1 year since last commit)
|-- ANTI-PATTERN: "We generate SBOM, we are secure."
|   |-- An unsigned, unverified SBOM is documentation, not security. It proves nothing.
```

## Best Practices

1. **Pin all direct dependencies to exact versions, not ranges.** `^1.2.3` or `~1.2.3` allows silent upgrades that break reproducibility. Use exact versions (`1.2.3`) with lockfiles (`package-lock.json`, `Cargo.lock`, `poetry.lock`) committed to the repo. Ranges are for libraries; pinned versions are for applications.

2. **Group Renovate/Dependabot PRs by ecosystem and update type.** Default Renovate creates one PR per dependency — a 500-dependency project gets 20-50 PRs/week. Configure groups: `renovate.json` with `"groupName": "all minor and patch"` for non-breaking updates, separate groups for framework majors. Auto-merge patch updates that pass CI.

3. **Define a tiered version alignment policy.** Tier-1 frameworks (React, Spring, Django) within 1 MAJOR version across 95% of repos. Tier-2 utilities (lodash, Guava) within 1 MINOR. Tier-3 dev tools: latest stable. Any repo out of alignment needs a documented exception and upgrade plan.

4. **Triage CVEs by reachability, not just CVSS score.** A CVSS 9.8 in a transitive dev dependency that never executes in production is lower priority than a CVSS 6.5 in your auth library. Use `npm audit --production`, `cargo audit`, or OWASP Dependency-Check with reachability analysis to prioritize.

5. **Generate and sign an SBOM on every release.** Use CycloneDX or SPDX format. Cryptographically sign with cosign or in-toto. Verify SBOM at deploy time — a policy engine must block deployments without a valid, signed SBOM. Unsigned SBOM is documentation, not security.

6. **Scan licenses at CI gate, not pre-launch review.** Discovering a GPL transitive dependency after 3 months of integration means ripping it out and rewriting. Block PRs that introduce unapproved licenses (GPL, AGPL) unless a documented exception exists. Rescan monthly — projects relicense.

7. **Automate dependency freshness checks.** A dependency not updated in 12 months is a security risk. Use Renovate's `stabilityDays` and `minimumReleaseAge` to avoid brand-new releases, but flag dependencies > 6 months behind upstream. Weekly stale-dependency report to engineering leads.

8. **Protect against dependency confusion and typosquatting.** Configure package managers to resolve private registries first (`npm config set registry`, `.npmrc` with scoped registries). Use Socket.dev or Snyk to detect suspicious package metadata. Block packages from unmaintained repos (>1 year since last commit).

9. **Test framework major upgrades in staging before auto-merging.** React 17→18 passing unit tests does not catch CSS breakage, deprecated API behavioral changes, or ecosystem plugin incompatibility. Auto-merge patches; manual review + staging verification for majors. Never auto-merge framework majors.

10. **Scan the full transitive dependency tree, not just direct deps.** A CVE 4 levels deep is just as exploitable. Tools that only scan `package.json` miss 60-80% of the dependency tree. Use `npm ls --all`, `cargo tree`, or dedicated SCA tools that traverse the full graph.

## Error Recovery **(STANDARD)**

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
| Monorepo workspace dependency management | monorepo-manager | Workspace hoisting, shared node_modules, nx affected |
| CI/CD integration for dependency scanning | ci-cd-builder | Pipeline stages for CVE scan, license check, SBOM generation |
| Security incident from dependency CVE | incident-responder | Incident response workflow, blast radius assessment, fix deployment |
| Legal review of specific license terms | legal-advisor | GPL interpretation, copyleft analysis, license exception decisions |
| Vulnerability scanning tooling | security-engineer | Snyk, Trivy, OSV-Scanner configuration, SAST integration |
| Polyrepo dependency version alignment | polyrepo-strategy | Cross-repo Renovate config, breaking change propagation, shared presets |
| Platform dependency standards | platform-engineer | Golden path dependencies, approved dependency catalog, scaffolding defaults |
| Build optimization from dependency pruning | performance-engineer | Bundle size analysis, tree-shaking verification, dead code elimination |
| Package registry infrastructure | devops-engineer | Internal npm/PyPI/Maven registry, artifact storage, access control |

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `cloud-architect` | Infrastructure design, networking, IAM, cost model | Before provisioning infrastructure or designing deployment pipelines |
| `ci-cd-builder` | Pipeline design, build optimization, deployment strategies | Before designing CI/CD workflows |

## Proactive Triggers

| # | Trigger Condition | Auto-Response |
|---|------------------|---------------|
| P1 | Same framework appears at >5 different versions across repos | [ALERT] Critical version sprawl: [framework] has [N] versions across [M] repos. Establish tier-1 alignment policy. Create coordinated upgrade plan. |
| P2 | Critical CVE (CVSS >= 9.0) unfixed for >48 hours | [ALERT] Emergency: CVE [ID] affecting [package] in [N] repos remains unfixed after 48h. Escalate to security leadership. Override change control. |
| P3 | Renovate/Dependabot PR count >50 open across org | [WARN] Dependency update backlog. Review auto-merge rules. Consider grouping strategy to reduce PR noise. Engineers may be ignoring updates. |
| P4 | GPL/AGPL license detected in new dependency without legal approval | [BLOCK] Copyleft license [license] in [package] requires legal review before merge. Add to allow-list only with documented approval. |
| P5 | Dependency count >1500 in a single project | [INFO] Dependency bloat: [project] has [N] dependencies. Industry median for similar projects: [M]. Audit for unused, duplicate, and unnecessary dependencies. |
| P6 | SBOM generated but not signed or verified | [WARN] Unsigned SBOM: [repo] generates SBOM without cryptographic signing or deployment verification. Add cosign signing and policy enforcement. |
| P7 | Dependency added with no maintainer activity >12 months | [WARN] Abandoned dependency: [package] has not been maintained in [N] months. Evaluate alternatives or plan to fork/vendor if critical. |
| P8 | Breaking change detected in shared dependency affecting >3 repos | [ALERT] Breaking change cascade: [package] v[X] breaks [N] repos. Coordinate migration across affected teams. Establish deprecation window. |

## State Log

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.

#

## How the State Log Works
<!-- AGENT: Read this before starting work, update after each phase -->

1. **On session start:** Check `.copilot/session-state/decision-ledger.json` for any prior decisions relevant to this domain. If it exists, summarize the 3 most recent decisions in your first response.
2. **After each major decision:** Append to the ledger:
   ```json
   {
     "timestamp": "ISO-8601",
     "skill": "dependency-governance",
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

#

## State Log Schema

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

#

## Anti-Drift Check
<!-- AGENT: Run this check at the start of each new phase -->

Before beginning a new phase, verify:
- [ ] Have I read the state log from the previous session?
- [ ] Do any prior decisions constrain what I'm about to do?
- [ ] Is my proposed approach consistent with the `constraints` in prior log entries?
- [ ] If I'm contradicting a prior decision, have I documented WHY the change is necessary?

## Production Checklist **(STANDARD)**

- [ ] **[DG-01]** Dependency inventory script runs across all repos, outputting full transitive tree (not just direct deps), with version counts for each unique package
- [ ] **[DG-02]** Tier-1 frameworks within 1 MAJOR version across 95%+ of repos; any outlier has a documented exception and upgrade plan with target date
- [ ] **[DG-03]** Shared Renovate/Dependabot presets deployed to 100% of repos with grouping rules (minor/patch grouped, framework majors separate), scheduling, and auto-merge rules
- [ ] **[DG-04]** Auto-merge enabled for patch updates that pass CI; disabled for framework major versions; auto-merge success rate above 60%
- [ ] **[DG-05]** Critical CVEs triaged with reachability analysis within 24h, fixed within 72h; High CVEs fixed within 14 days; no CVE older than 30 days without triage
- [ ] **[DG-06]** Full transitive dependency tree scanned for CVEs; scanner configured to traverse all levels, not just direct dependencies
- [ ] **[DG-07]** License compliance gate active in CI: PRs blocked if they introduce unapproved licenses (GPL, AGPL, SSPL); exceptions documented in a license exception registry
- [ ] **[DG-08]** Monthly license re-scan configured; any project that re-licensed is flagged within 5 business days; copyleft contamination detected before merging
- [ ] **[DG-09]** SBOM generated in CycloneDX or SPDX format on every release; cryptographically signed with cosign or in-toto; verified at deploy time by policy engine
- [ ] **[DG-10]** Dependency confusion protection enabled: private registries configured first in resolution order; scoped packages pinned to private registry; typosquatting detection active
- [ ] **[DG-11]** New dependency approval workflow: PR adding a new dependency must include justification, bundle size impact, and license verification; reviewer gate before merge
- [ ] **[DG-12]** Dependency freshness dashboard: red flag for packages >6 months behind upstream, >1 year since last commit (unmaintained), or with deprecated notices
- [ ] **[DG-13]** Breaking change detection: canary tests or compiler-based detection run against framework MAJOR upgrades before auto-merge; results posted to PR as comment
- [ ] **[DG-14]** Quarterly dependency health report automated: version alignment trend, CVE SLA compliance, license violation count, removal candidates (unused/duplicate), and dependency bloat trend

## What Good Looks Like

```mermaid
graph TD
    A[50-Repo Organization] --> B[Dependency Inventory: 15,000 packages across all repos]
    B --> C[Tiered Version Alignment: 95% repos on same React MAJOR]
    C --> D[Shared Renovate Presets: grouping, scheduling, auto-merge]
    D --> E[CVE Pipeline: Scan -> Triage -> Fix within SLA]
    E --> F[License Compliance: Zero unapproved GPL in production]
    F --> G[SBOM: generated on release, signed, verified before deploy]
    G --> H[Quarterly Dependency Health Report: sprawl trend, CVE SLA, removal candidates]
```

A well-governed dependency ecosystem has these characteristics:
- **Version sprawl is managed.** Top-10 frameworks are within 1 MAJOR version across all repos. Teams are not surprised by framework differences.
- **Renovate PRs are acted on, not ignored.** <20 open dependency PRs org-wide. Auto-merge handles 60%+ of updates. Engineers spend <1 hour/week on dependency updates.
- **CVEs are triaged, not panicked over.** Critical CVEs fixed within 24h. High CVEs within 7 days. Medium/low in regular cycles. No CVE email fire drills.
- **License compliance is automated.** Zero unapproved copyleft licenses in production. New dependency PRs are blocked at CI if license is flagged. Monthly audit confirms.
- **SBOM is a security artifact.** Generated on every release. Cryptographically signed. Verified at deploy time. Policy engine blocks non-compliant deployments.

## Deliberate Practice

```
Exercise 1: VERSION SPRAWL AUDIT (1 hour)
|-- For an organization you know (or a hypothetical 20-repo org):
|-- Choose a framework (React, Angular, Django, Spring Boot)
|-- Research: what versions would realistically exist across 20 repos built over 3 years?
|-- Calculate: how many distinct MAJOR versions? How many MINOR? What is the security gap?
|-- Design: a version alignment policy that reduces sprawl without forcing everyone to the latest.
|-- Extra credit: what would it cost to upgrade the oldest repo to the current version?

Exercise 2: CVE TRIAGE SIMULATION (45 min)
|-- CVE-2024-XXXX: CVSS 9.8, network attack vector, low complexity, no privileges required.
|-- The vulnerability is in a transitive dependency of a logging library used only in dev.
|-- Question: Is this critical for your production deployment? Why or why not?
|-- Compare: same CVE, but in your authentication library, directly handling user tokens.
|-- What changes? Why does reachability matter more than CVSS score?

Exercise 3: RENOVATE CONFIG DESIGN (1 hour)
|-- Design a shared Renovate preset for a 30-repo org with React, Node.js, and Python projects.
|-- Specify: grouping rules, scheduling, auto-merge rules, and noise reduction settings.
|-- Edge case: 3 repos are critical infrastructure. How does their config differ from internal tools?
|-- Anti-pattern check: Would your config create a "Renovate firehose" of PRs? How do you prevent it?

Exercise 4: LICENSE COMPLIANCE SCENARIO (30 min)
|-- A new dependency (left-pad equivalent) is proposed. It is MIT-licensed but depends on a GPL-3.0 package.
|-- Question: Does the GPL transitive dependency contaminate your project? Why or why not?
|-- Research: GPL linking — static vs dynamic. SaaS loophole. AGPL difference.
|-- Recommendation: would you approve this dependency? Under what conditions?
```

## Anti-Rationalization — No Excuses

| Rationalization | Reality |
|---|---|
| "We'll pin everything and update once a year — it's more stable." | When Log4Shell hits and you have 18 months of unpulled updates across 50 repos, you're doing 200+ emergency upgrades simultaneously. Every one is a potential breaking change under duress. $150K-$500K in emergency remediation. |
| "Renovate/Dependabot handles it — just enable and forget." | Default Renovate creates one PR per dependency. A 500-dependency project = 20-50 PRs/week. Engineers develop notification fatigue and start blindly closing them. Within 3 months: 200+ open dependency PRs and a culture of ignoring updates. $80K-$200K/year. |
| "It's a dev dependency — it doesn't affect production, so it doesn't matter." | Dev tools run in CI/CD pipelines with full repo access, secret access, and deployment credentials. Compromised dev dependency = full supply chain compromise. $30K-$100K per incident in credential rotation, incident response, and potential data exposure. |
| "We'll review licenses during the legal review phase before launch." | Discovering a GPL transitive dependency after 3 months of integration means ripping it out and rewriting that functionality. $20K-$50K in rework. License scanning must be a CI gate, not a pre-launch checkbox. |
| "Internal packages can't be compromised — they're behind our firewall." | Dependency confusion and typosquatting attacks target internal package names. If your CI resolves `company-utils` from a public registry before your private one, the attacker's package runs with full CI privileges. $15K-$40K per incident. |

## Anti-Patterns

### Anti-Pattern: Pin everything and never update
**What it looks like:** A dependency graph frozen for 6-18 months. Engineers say "if it works, don't touch it." Lockfiles committed but never regenerated.
**Why it fails:** When a critical CVE hits, you must update 200 packages at once — every one is a potential breaking change. The emergency remediation effort across 50 repos costs $150K-$500K when Log4Shell-level CVEs hit and you have 18 months of unpulled updates.
**Do this instead:** Establish a regular update cadence (monthly for patches, quarterly for minors). Use Renovate with grouping and auto-merge for patches. Freeze only with a documented exception and sunset date.

### Anti-Pattern: Default Renovate without configuration
**What it looks like:** Renovate installed with default config, creating one PR per dependency. 20-50 PRs per week in a 500-dependency project. Engineers learn to close bot PRs on sight. Within 3 months: 200+ open dependency PRs.
**Why it fails:** $80K-$200K per year in wasted CI minutes, review cycles, and accumulated security debt. The exact opposite of what Renovate is supposed to achieve — it trains teams to ignore dependency updates entirely.
**Do this instead:** Configure grouping rules: all minor/patch updates in one PR group per ecosystem. Framework majors in separate, well-labeled PRs. Set `automerge: true` for patches that pass CI. Add `stabilityDays: 3` to avoid brand-new releases.

### Anti-Pattern: Auto-merging framework major versions
**What it looks like:** React 17→18, Spring Boot 2→3, or Django 4→5 auto-merged because CI passes. "The tests are green" used as justification.
**Why it fails:** Unit tests don't catch CSS breakage, deprecated API behavioral changes, ecosystem plugin incompatibility, or runtime performance regressions. A broken production checkout flow costs hours of debugging, rollback, and team trust in automation. $25K-$75K per incident.
**Do this instead:** Auto-merge patches only. Framework majors require manual review + staging environment verification for at least 24 hours. Post results of canary tests as PR comment. Never auto-merge framework majors.

### Anti-Pattern: Treating every Dependabot alert as P0
**What it looks like:** Every Dependabot alert triggers an incident response. Medium-severity CVEs in transitive dev dependencies that never execute in production get the same urgency as critical CVEs in auth libraries.
**Why it fails:** 10 such alerts per week across 30 repos = 320 engineering hours/month wasted. $200K-$500K per year in misallocated CVE response. Teams burn out and stop taking alerts seriously.
**Do this instead:** Triage by reachability: can this code path actually be invoked in production? If no, downgrade to P3 with a documented analysis. Reserve P0 for CVEs in production-reachable code with known exploitability (CISA KEV catalog).

### Anti-Pattern: Declaring CVE fixed after merging the Dependabot PR
**What it looks like:** Dependabot PR merged, alert closed, team moves on. But the same dependency is pinned separately in a Dockerfile, CI config, or monorepo root package.json that wasn't updated.
**Why it fails:** The CVE persists in production despite being "fixed." Discovering a "fixed" CVE is still exploitable 3 months later destroys security credibility. $50K-$150K per incident in response, disclosure, and remediation.
**Do this instead:** After merging a CVE fix, verify across all lockfiles, Dockerfiles, and configuration files that the vulnerable version is absent. Run `npm ls [package]` or `cargo tree | grep [crate]` across the full build graph. Automate this verification in CI.

### Anti-Pattern: Scanning only direct dependencies for CVEs
**What it looks like:** CVE scanner configured to check `package.json` or `requirements.txt` only. Transitive tree ignored because "we don't directly depend on that."
**Why it fails:** A CVE 4 levels deep is just as exploitable. Tools scanning only the top level miss 60-80% of the dependency tree. $100K-$300K in undetected risk exposure.
**Do this instead:** Always scan the full transitive tree. Use `npm audit --all`, `cargo audit` (traverses full graph), or dedicated SCA tools (Snyk, Black Duck) that build the complete dependency graph. Configure CI to fail on critical/high CVEs in any transitive dependency.

### Anti-Pattern: "It was MIT when we added it" — ignoring license changes
**What it looks like:** License checked once at dependency addition time. No periodic re-scan. Packages sit in the dependency tree for years with no license verification.
**Why it fails:** Projects relicense. A package that was MIT 2 years ago may be GPL today. Or it may have added a GPL dependency transitively. GPL contamination discovered during due diligence (fundraising, acquisition) can block or devalue the deal. $250K-$2M in legal exposure and remediation.
**Do this instead:** Monthly automated license re-scan of the full dependency tree. Configure CI to block PRs introducing unapproved licenses. Maintain a license exception registry with documented rationale for each exception, reviewed quarterly.

### Anti-Pattern: Ignoring devDependencies in license scans
**What it looks like:** License scanner configured with `--production` flag, skipping devDependencies. Justification: "devDependencies aren't shipped to production."
**Why it fails:** DevDependencies execute during builds with full repo and credential access. A GPL build tool that injects GPL code into your output is a contamination risk. $75K-$250K in legal remediation. "It was only a dev dependency" is not a universal defense against copyleft claims.
**Do this instead:** Scan devDependencies too. Use separate license policy tiers: production = strict (no copyleft), dev = cautious (copyleft allowed only with documented review that it doesn't inject code into build output).

## Verification

After designing a dependency governance program, run this sequence. Do not proceed past a failure.

1. **Dependency inventory check:** All repos have their full dependency tree (direct + transitive) documented. Top-20 most-used packages identified with version counts. If inventory is incomplete, governance policies will miss repos.
2. **Version alignment check:** Tier-1 frameworks are within 1 MAJOR version across 95%+ of repos. Any repo out of alignment has a documented exception and upgrade plan. If >10% of repos are out of alignment, the policy is aspirational, not enforced.
3. **Renovate health check:** <20 open dependency PRs org-wide. Auto-merge handles 60%+ of eligible updates. No PR older than 14 days without review. If PR backlog exists, review grouping and auto-merge rules.
4. **CVE SLA check:** Critical CVEs fixed within 24h (or documented exception with reachability analysis). High CVEs fixed within 7 days. No CVE older than 30 days without triage. If SLAs are not met, the CVE response process is broken.
5. **License compliance check:** Zero unapproved copyleft licenses in production. Monthly re-scan confirms no new violations. CI blocks PRs that add flagged licenses. If violations exist, fix before proceeding.
6. **SBOM integrity check:** SBOM generated on every release. Cryptographically signed. Verified at deploy time. If any step is missing, SBOM is incomplete.
7. **Dependency firewall check:** Known-malicious packages are blocked. Packages from unmaintained repos trigger review. Typosquatting detection is active. If not, supply chain attack surface is open.

If any check fails: diagnose from checklist, provide specific actionable fix, restart verification from failed item.

## Verification Guardrails

Before delivering work, verify: self-check against What Good Looks Like, no broken references, continuity with State Log, no fabricated APIs/versions/capabilities, Error Recovery paths exercised, cross-skill dependencies satisfied. If any fail, revise before delivering.

## References

* [Renovate Documentation: Shareable Config Presets](https://docs.renovatebot.com/config-presets/) — Centralized configuration across repos
* [GitHub: Dependabot Alerts & Security Updates](https://docs.github.com/en/code-security/dependabot) — Automated vulnerability detection and remediation
* [NIST National Vulnerability Database (NVD)](https://nvd.nist.gov/) — CVSS scoring and CVE database
* [CISA Known Exploited Vulnerabilities Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) — CVEs with active exploitation
* [Open Source Security Foundation (OpenSSF) Scorecard](https://securityscorecards.dev/) — Automated security health assessment for open source projects
* [SPDX Specification](https://spdx.dev/specifications/) — ISO-standard SBOM format
* [/references/dependency-inventory.md](references/dependency-inventory.md) — Multi-repo dependency graphing and analysis framework
* [/references/version-alignment.md](references/version-alignment.md) — Tiered version policy design and enforcement
* [/references/breaking-change-detection.md](references/breaking-change-detection.md) — Automated canary tests and compiler-based detection
* [/references/vulnerability-triage.md](references/vulnerability-triage.md) — CVSS + exploitability + reachability scoring methodology
* [/references/license-compliance.md](references/license-compliance.md) — Copyleft detection, approval workflows, exception management
* [/references/renovate-at-scale.md](references/renovate-at-scale.md) — Shared presets, auto-merge rules, grouping, scheduling
* [/references/dependency-removal.md](references/dependency-removal.md) — Safe removal with tree-shaking and bundle verification
* [/references/sbom-supply-chain.md](references/sbom-supply-chain.md) — SBOM generation, signing, attestation, and verification
