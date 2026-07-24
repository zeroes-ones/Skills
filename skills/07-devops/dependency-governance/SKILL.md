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

### Auto-Route by Artifacts (Check Filesystem First)

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_exists("renovate.json")` OR `file_exists(".github/renovate.json")` across 5+ repos | Renovate already configured -> Jump to **Decision Trees: Renovate at Scale** |
| A2 | `gh api /orgs/X/dependabot/alerts --paginate` returns >10 open alerts | Critical CVE backlog -> Go to **Core Workflow: Phase 3 -- CVE Triage** |
| A3 | `file_contains("package.json", ""license"")` returns GPL/AGPL in dependencies | Copyleft license detected -> Jump to **Decision Trees: License Compliance** |
| A4 | `npx depcruise` or `nx graph` output exists in repo | Dependency graph available -> Go to **Core Workflow: Phase 1 -- Inventory** |
| A5 | `file_contains(".github/workflows/", "sbom\|spdx\|cyclonedx")` | SBOM pipeline exists -> Jump to **Decision Trees: SBOM & Supply Chain** |
| A6 | `grep -rn "TODO.*remove\|FIXME.*dependency"` across repos | Technical debt markers -> Jump to **Decision Trees: Dependency Removal** |
| A7 | No dependency management tooling found | Greenfield governance setup -> Go to **Core Workflow: Phase 1** |

### Intent Route (Ask the User)

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

## Core Workflow

### Phase 1: Dependency Inventory

Execute in order. Do not skip steps.

```
1. GRAPH ALL DEPENDENCIES ACROSS ALL REPOS
   |-- For each repo, extract direct + transitive dependencies
   |-- Tools: npx depcruise (JS), pipdeptree (Python), mvn dependency:tree (Java), cargo tree (Rust)
   |-- Output: dependency graph with repo -> package -> version mapping
   |-- Flag duplicates: same package at different versions across repos

2. CLASSIFY DEPENDENCIES BY TYPE
   |-- Frameworks: React, Angular, Next.js, Spring Boot (slow to upgrade, high impact)
   |-- Runtime libraries: lodash, date-fns, axios (frequent updates, moderate risk)
   |-- Build tools: TypeScript, Webpack, Vite, Babel (dev-only, moderate risk)
   |-- Dev tools: ESLint, Prettier, Jest (low risk, safe to auto-update)
   |-- Transitive-only: dependencies not directly imported (harder to track, hidden risk)

3. IDENTIFY VERSION SPRAWL
   |-- For top-20 most-used packages: count distinct versions across all repos
   |-- Sprawl thresholds:
   |   |-- 1 version: aligned (ideal)
   |   |-- 2-3 versions: moderate sprawl (acceptable if major version differences)
   |   |-- 4-7 versions: significant sprawl (coordination problem)
   |   |-- 8+ versions: critical sprawl (security and compatibility risk)
   |-- Prioritize alignment for frameworks and security-critical libraries

4. CALCULATE DEPENDENCY HEALTH SCORE
   |-- Per repo: % dependencies on latest major, % with known CVEs, dependency count vs. industry benchmark
   |-- Per org: % repos aligned on framework versions, average CVE age, orphan dependency count
   |-- Baseline: establish current state before governance changes
```

### Phase 2: Establish Governance Policies

```
1. VERSION ALIGNMENT POLICY
   |-- Tier 1 (Must Match): Frameworks (React, Angular, Next.js), security libraries (auth, crypto)
   |   |-- Policy: all repos on same MAJOR version. Minor/patch can vary within 2 releases.
   |   |-- Enforcement: CI check that compares version against org baseline
   |-- Tier 2 (Should Align): Shared utilities (lodash, date-fns), testing frameworks
   |   |-- Policy: all repos within 1 MAJOR version of each other
   |   |-- Enforcement: Renovate grouping with shared preset
   |-- Tier 3 (Free): Dev tools, formatters, linters
   |   |-- Policy: no alignment requirement beyond "reasonably current"
   |   |-- Enforcement: Renovate auto-update with auto-merge if CI passes

2. UPDATE CADENCE POLICY
   |-- Security patches (CVE fix): auto-merge within 24h if CI passes
   |-- Patch updates (1.2.3 -> 1.2.4): auto-merge weekly if CI passes
   |-- Minor updates (1.2.x -> 1.3.0): grouped PR every 2 weeks, manual review for frameworks
   |-- Major updates (1.x -> 2.0): manual review, migration plan required, coordinated across repos

3. NEW DEPENDENCY REVIEW PROCESS
   |-- Before adding: justify why existing deps cannot meet the need
   |-- Check: bundle size impact (<10KB gzipped ideal, >50KB needs justification)
   |-- Check: license compatibility (no GPL/AGPL without legal approval)
   |-- Check: maintenance health (recent commits, responsive maintainers, not abandoned)
   |-- Check: is there a smaller, well-maintained alternative?

4. RENOVATE/DEPENDABOT SHARED CONFIGURATION
   |-- Centralized preset in .github repo (or shared npm package)
   |-- All repos extend the shared preset (extend: ["github>org/renovate-config"])
   |-- Grouping strategy: group related packages (all React packages, all ESLint plugins)
   |-- Schedule: staggered by repo priority (critical repos on Monday, others Tuesday-Thursday)
   |-- Auto-merge: enabled for dev tools (patch/minor only) with required CI checks
```

### Phase 3: CVE Triage & Response

```
1. CVE DETECTION
   |-- Automated scanning: Dependabot, Snyk, Trivy, or OSV-Scanner in CI
   |-- Schedule: scan on every PR + daily scheduled scan for all repos
   |-- Alert routing: critical CVEs -> Slack/email to owning team + security team

2. CVE TRIAGE (Not All CVEs Are Critical)
   |-- Step 1: CVSS Score
   |   |-- Critical (9.0-10.0): requires immediate attention
   |   |-- High (7.0-8.9): address within 7 days
   |   |-- Medium (4.0-6.9): address within 30 days
   |   |-- Low (0.1-3.9): address in next planned update cycle
   |-- Step 2: Exploitability
   |   |-- Is there a public exploit? (check CISA KEV, Exploit-DB, GitHub Security Advisories)
   |   |-- Attack vector: Network (high risk) vs Local (lower risk) vs Physical (low risk)
   |   |-- Attack complexity: Low (easy to exploit) vs High (requires specific conditions)
   |-- Step 3: Reachability
   |   |-- Is the vulnerable function/method actually called by your application?
   |   |-- Is the vulnerable dependency in your runtime bundle or only in dev?
   |   |-- Tools: dependency-cruiser with reachability analysis, Snyk Reachability
   |-- Final Priority = CVSS adjusted by exploitability and reachability

3. CVE RESPONSE WORKFLOW
   |-- Critical + exploitable + reachable: Fix immediately. Override normal change control.
   |-- Critical + not exploitable or not reachable: Fix in next sprint.
   |-- High + exploitable + reachable: Fix within 7 days.
   |-- All others: Schedule in Renovate update cycle. Do not create emergency PRs.
   |-- Track CVE age: escalate any critical CVE unfixed >48h to security leadership.
```


## Decision Trees

### Version Alignment Strategy

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

### Renovate/Dependabot at Scale

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

### License Compliance

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

### CVE Triage Decision Tree

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

### Dependency Removal

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

### SBOM & Supply Chain Security

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


## Gotchas

### Version Management Gotchas

* **"We will pin everything and never update."** A dependency graph frozen for 6 months is a security incident waiting to happen. When a critical CVE hits, you must update 200 packages at once — every one is a potential breaking change. **Total cost: $150,000-$500,000 in emergency remediation effort** when Log4Shell-level CVE hits and you have 18 months of unpulled updates across 50 repos.

* **"Renovate will handle it" without configuration.** Default Renovate creates one PR per dependency. For a medium-sized project with 500 dependencies, that is 20-50 PRs per week. Engineers learn to ignore them. Within 3 months, you have 200+ open dependency PRs and a culture of "just close the bot PRs." **Total cost: $80,000-$200,000 per year in wasted CI minutes, review cycles, and the security debt of ignored updates** — the exact opposite of what Renovate is supposed to achieve.

* **Auto-merging a React major version update because "the tests pass."** Unit tests do not catch subtle runtime behavior changes, deprecated API removals, or CSS breakage. A React 17->18 auto-merge that passes CI but breaks the production checkout flow costs hours of debugging, a rollback, and team trust in automation. **Total cost: $25,000-$75,000 per incident** in debugging, rollback, and lost engineering trust. Auto-merge framework majors only after a manual review + staging verification.

### CVE Response Gotchas

* **Treating every Dependabot alert as a P0 incident.** A medium-severity CVE in a transitive dev dependency that is not reachable from production code consumes 4-8 engineering hours if treated as critical. At 10 such alerts per week across 30 repos, that is 320 engineering hours/month. **Total cost: $200,000-$500,000 per year in wasted CVE response** — triage is not optional, it is the difference between security engineering and security theater.

* **"We fixed the vulnerability — closed the Dependabot PR."** Merging the Dependabot PR updates the lockfile. But if you also have the dependency pinned in a Dockerfile, a CI config, or a monorepo root package.json that was not updated, the CVE persists in production. **Total cost: $50,000-$150,000 per incident** — discovering a "fixed" CVE is still exploitable in production, 3 months after you declared it resolved, destroys security credibility.

* **Checking only direct dependencies for CVEs.** A CVE in a transitive dependency 4 levels deep is just as exploitable as one in a direct dependency — your application executes that code. Tools that only scan package.json miss 60-80% of the dependency tree. **Total cost: $100,000-$300,000 in undetected risk exposure** — every CVE scanner is only as good as its depth. Always scan the full tree.

### License & Compliance Gotchas

* **"It was MIT when we added it."** Projects relicense. A package that was MIT 2 years ago may be GPL today. Or it may have added a dependency that is GPL. Without monthly re-scans, you are blind to license changes. **Total cost: $250,000-$2,000,000 in legal exposure and remediation** — GPL contamination discovered during due diligence (fundraising, acquisition) can block or devalue the deal.

* **Ignoring devDependencies in license scans.** DevDependencies are not shipped to production, but they ARE executed during builds. A GPL build tool that injects GPL code into your output is a contamination risk. Most license scanners have a --dev flag for a reason. **Total cost: $75,000-$250,000 in legal remediation** — "it was only a dev dependency" is not a universal defense against copyleft claims.

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
