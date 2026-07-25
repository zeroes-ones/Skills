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

