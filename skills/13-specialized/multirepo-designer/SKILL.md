---
name: multirepo-designer
description: >
  Use when designing multi-repository architectures, deciding repo granularity, managing
  cross-repo dependencies, orchestrating CI/CD across repos, publishing shared libraries,
  managing breaking changes, establishing repo ownership models, designing cross-repo
  testing strategies, or migrating between mono and multi-repo topologies. Handles repo
  boundary design, versioning strategies, shared library publishing workflows, cross-repo
  CI orchestration, breaking change management, tool selection (Nx, Turborepo, Lerna,
  Rush, Bazel, pnpm workspaces, Changesets), and repo discoverability patterns. Do NOT
  use for monorepo tooling configuration (route to monorepo-manager), CI/CD pipeline
  implementation (route to ci-cd-builder), or API design (route to api-designer).
license: MIT
allowed-tools: Read Grep Glob
tags:
  - multirepo
  - multi-repo
  - polyrepo
  - repo-architecture
  - cross-repo
  - versioning
  - dependency-management
  - shared-libraries
  - breaking-changes
  - ci-cd-orchestration
author: Sandeep Kumar Penchala
type: specialized
status: stable
version: 1.0.0
released: 2025-06-23
updated: 2026-07-24
token_budget: 4000
chain:
  consumes_from:
    - monorepo-manager
    - system-architect
    - devops-engineer
  feeds_into:
    - backend-developer
    - fullstack-developer
    - ci-cd-builder
compatible_with:
  - monorepo-manager
  - polyrepo-strategy
  - migration-architect
  - cross-repo-refactoring
  - platform-engineer
  - code-reviewer
changelog:
  - version: 1.0.0
    date: 2025-06-23
    changes:
      - Initial release. Multi-repo architecture design, split granularity decisions, cross-repo dependency management, shared library publishing, breaking change rollouts, and CI/CD orchestration across repos.
---
# Multirepo Designer
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Veteran architect's playbook for designing, governing, and operating multi-repository architectures at scale. Covers when and how to split repos, cross-repo dependency management, shared library publishing, versioning strategies, breaking change orchestration, repo discovery, ownership models, and migration patterns between mono and multi-repo topologies.

## Route the Request

<!-- QUICK: 30s -- auto-route first, then intent-route -->

#

## Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_exists(".gitmodules")` OR `file_contains("Makefile|justfile", "trigger-downstream|cross-repo|sync-deps")` | Cross-repo coordination infrastructure detected. Jump to **Decision Trees** — Cross-Repo CI/CD Orchestration. |
| A2 | `file_contains(".github/workflows/*.yml", "repository_dispatch|workflow_call|reusable")` across >3 directories | Multi-repo CI orchestration in use. Jump to **Core Workflow** — Phase 3 (Cross-Repo CI/CD). |
| A3 | `file_exists("renovate.json") OR file_exists(".github/dependabot.yml")` AND `gh repo list --limit 50 --json name | jq length` > 10 | Cross-repo dependency automation active. Jump to **Decision Trees** — Shared Library Strategy. |
| A4 | `file_contains("*.md", "breaking.change|migration.guide|UPGRADING|CHANGELOG")` AND `file_contains("*.md", "deprecated|removed in|will be removed")` | Breaking change migration artifacts. Jump to **Core Workflow** — Phase 5 (Breaking Change Rollout). |
| A5 | `file_contains("CODEOWNERS|OWNERS", "*")` AND repo count > 5 | Repo ownership model defined. Jump to **Decision Trees** — Ownership & CODEOWNERS. |
| A6 | `file_contains("*.json|*.yaml|*.toml", ""name".*"@")` AND multiple repos publish to registry | Internal package publishing in use. Jump to **Core Workflow** — Phase 4 (Shared Library Publishing). |
| A7 | `file_contains("*", "git.filter-repo|git.subtree|mono.*to.*multi|split.*monorepo|multi.*to.*mono")` | Migration in progress or planned. Jump to **Decision Trees** — Mono↔Multi Migration. |
| A8 | `file_contains("docker-compose.yml|docker-compose.*.yml", "container_name.*repo|depends_on.*repo")` across >3 repos | Cross-repo integration testing setup. Jump to **Core Workflow** — Phase 6 (Cross-Repo Testing). |

#

## Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

```
What are you trying to do?
├── DECIDE repo topology
│   ├── Monorepo vs multirepo decision → Jump to "Decision Trees" — Monorepo vs Multirepo
│   ├── How granular should repos be? → Jump to "Decision Trees" — Split Granularity
│   └── When should I split/merge repos? → Jump to "Decision Trees" — Mono↔Multi Migration
├── MANAGE cross-repo dependencies
│   ├── Share internal libraries across repos → Jump to "Decision Trees" — Shared Library Strategy
│   ├── Version internal packages across repos → Jump to "Core Workflow" — Phase 4
│   └── Handle breaking changes across repos → Jump to "Core Workflow" — Phase 5
├── ORCHESTRATE across repos
│   ├── CI/CD pipelines across multiple repos → Jump to "Decision Trees" — Cross-Repo CI/CD
│   ├── Test changes that span multiple repos → Jump to "Core Workflow" — Phase 6
│   └── Coordinate releases across repos → Jump to "Core Workflow" — Phase 3
├── GOVERN the repo ecosystem
│   ├── Set up CODEOWNERS and team ownership → Jump to "Decision Trees" — Ownership & CODEOWNERS
│   ├── Make repos discoverable → Jump to "Core Workflow" — Phase 2
│   └── Evaluate multirepo tooling (Nx, Lerna, Bazel) → Jump to "Decision Trees" — Tool Selection
├── Need monorepo tooling configuration → Invoke monorepo-manager skill instead
├── Need CI/CD pipeline implementation → Invoke ci-cd-builder skill instead
├── Need API contract design → Invoke api-designer skill instead
├── Need team org design → Invoke engineering-manager skill instead
└── Not sure? → Describe your repo count, team topology, and coordination pain points
```

Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

<!-- HARD GATE: These are non-negotiable. Violation → STOP and refuse to proceed. -->

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **REFUSE to split into micro-repos without a coupling measurement.** Splitting repos without understanding cross-repo change frequency creates coordination hell — every feature spans 3-5 PRs across repos. | Trigger: proposing repo split AND no coupling analysis present: `grep -rn "cross.repo|coupling|change.frequency" decision-doc.md | wc -l` returns 0 | STOP. Respond: "Measure coupling first. Analyze git history for cross-repo PR frequency over the last 6 months. If >30% of PRs touch the same set of repos, keep them together. Splitting before understanding coupling creates more coordination problems than it solves." |
| **R2** | **REFUSE to set up shared libraries without a versioning strategy.** Unversioned internal packages cause 'works on my machine' failures across every consuming repo. A breaking change in the shared library silently breaks every downstream consumer. | Trigger: proposing internal package publish AND no versioning strategy (semver, automated changelog, CI version bump) mentioned | STOP. Respond: "Every shared library MUST have: (1) semantic versioning (breaking.minor.patch), (2) automated changelog generation from conventional commits, (3) CI-enforced version bump on merge, (4) a documented deprecation policy (minimum 2 minor versions before removal). Without these, shared libraries are a shared liability." |
| **R3** | **REFUSE to recommend breaking changes without a multi-repo migration playbook.** In multirepo, you cannot atomically update all consumers. A single breaking change without migration tooling creates cascading CI failures across 10+ repos. | Trigger: proposing breaking API/contract/schema change AND no migration plan with: (1) deprecation timeline, (2) automated migration tool/script, (3) consumer notification, (4) monitoring dashboard | STOP. Respond: "Breaking changes in multirepo need: (1) Add new interface alongside old — ship as minor, (2) Deprecate old with runtime warnings + migration guide — ship next minor, (3) Announce removal date with automated PRs to consumers — minimum 4-week window, (4) Monitor consumer adoption, (5) Remove old interface only after all consumers are on new version + 1 release buffer. Without automated migration tooling (codemods, upgrade scripts), each consumer manually ports — days of wasted engineering time." |
| **R4** | **DETECT and WARN about copy-paste dependency duplication.** When the same code exists in 3+ repos, any bug fix must be applied in 3+ places — and it won't be. The 3rd repo always gets forgotten, creating security and correctness drift. | Trigger: `grep -rn "shared|common|util|helper" —include="*.ts" —include="*.js" —include="*.go" —include="*.py"` across >2 repos detects identical function signatures | WARN: "Code duplication detected across [N] repos. Every bug fix or security patch must now be applied N times. Extract to a shared library when: (1) code is duplicated in ≥3 repos, (2) the duplicated code changes >2x/year, (3) the duplication surface >50 lines. Until extracted, add a comment at each duplicate site linking to the canonical source." |
| **R5** | **REFUSE to allow repos without CODEOWNERS.** Every repo without an owner is an orphan — no one reviews PRs, fixes CVEs, or maintains CI. Orphan repos accumulate security vulnerabilities and become the #1 vector for supply chain attacks. | Trigger: `gh repo list —limit 100 —json name | jq -r '.[].name' | while read r; do gh api repos/ORG/\ —jq '.name' 2>/dev/null; done` reveals repos without CODEOWNERS file | STOP. Respond: "Repos without CODEOWNERS detected: [list]. Every repo must have: (1) CODEOWNERS file with at least 2 owners, (2) documented team ownership in repo description, (3) CI check requiring CODEOWNERS review. Without this, no one is accountable for the repo's security, maintenance, or quality." |
| **R6** | **DETECT and WARN about version drift across repos.** When Repo A uses react@18.2, Repo B uses react@18.3, and the shared design-system uses react@17.0 — cross-repo integration tests pass locally but fail in CI because npm resolves different versions. | Trigger: `for f in */package.json; do jq -r '.dependencies.react // .devDependencies.react // empty' \; done | sort -u | wc -l` returns >1 for any framework-level dependency | WARN: "Version drift detected for [dependency]. Maintain a canonical version manifest in a shared config repo. Use Renovate or Dependabot with grouped updates across repos. Enforce version ranges with a lockstep policy: all repos must be within 1 minor version of each other for shared framework dependencies." |
| **R7** | **STOP and ASK before creating a new repo.** Every new repo adds: a CI pipeline to maintain, a CODEOWNERS file, dependency updates, security scanning, and onboarding docs. New repos should be the last resort, not the default. | Trigger: proposing a new repo AND no justification addressing: (1) why existing repos cannot absorb this code, (2) the CI/CD pipeline burden, (3) the ownership and maintenance plan | STOP. Ask: "Why can't this code live in an existing repo? What are the 3 specific problems that a new repo solves that adding to an existing repo would create? Every new repo is a 10-year commitment to CI, security, and maintenance. Justify the boundary with: independent deploy cadence, independent team ownership, and independent security classification." |

- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset

Masters of multirepo design don't just split code — they split along **team boundaries, release cadences, and security domains.** They understand that every repo boundary is a coordination tax: each additional repo adds a PR, a CI run, and a review cycle to every cross-cutting change.

| Cognitive Bias | Mitigation |
|----------------|------------|
| **Splitting fever** — reflexively creating repos for every new project without evaluating the coupling cost | Before creating a new repo, calculate: cross-repo PRs this will generate per sprint x minutes per cross-repo PR x engineer count. If >2 hours/week/team, keep it together |
| **Monorepo nostalgia** — merging repos because "Google does it" without Google's $500M tooling investment | Evaluate: do you have the build caching, affected detection, and merge queue infrastructure that makes monorepos viable? If not, merging creates a slow monolith, not a fast monorepo |
| **Shared-library absolutism** — extracting every duplicated 10-line function into a package, creating dependency hell for trivial code | The cost of publishing + versioning + updating a shared package must be less than the cost of maintaining duplication. Threshold: <3 consumers, <50 lines, changes <1x/year -> keep duplicated |
| **Tool-as-strategy** — picking Nx or Bazel before deciding what problem you are solving | Always start with the problem: "Our 15 repos have 40% cross-repo PRs and CI takes 90 minutes." Then ask: "Does the tool solve THIS problem?" Don't let tool selection drive architecture |

#

## What Masters Know That Others Don't
- **Repo granularity is a function of team autonomy, not code size.** Two teams that never coordinate on releases should not share a repo — even if the code is only 200 lines. One team that ships together daily should not be split — even if the codebase is 500K lines.
- **Every shared library is a promise.** When you publish @org/design-system@2.0.0, you are promising every consumer that this API will be stable until 3.0.0. Breaking that promise costs every consumer hours of migration. The more consumers, the more conservative the API must be.
- **Cross-repo CI is the canary.** If your cross-repo CI takes >20 minutes or fails >10% of the time, your repo boundaries are wrong — either repos are too coupled (merge them) or CI tooling is inadequate (invest in it). Healthy multirepo: cross-repo CI passes >95% of the time and completes in <10 minutes.

#

## When to Break Your Own Rules
- **Ship the prototype as a new repo, then decide boundaries.** When exploring a new product idea, create a single new repo and move fast. Don't pre-optimize repo boundaries for code that might be thrown away. After 3 months of shipping, measure actual cross-repo coupling — THEN split or consolidate.
- **Skip the shared library for truly stable code.** If the shared code hasn't changed in 18 months and has zero open bugs, copy-paste is more resilient than a dependency. A copied function can't break your build when someone else upgrades it.
- **Accept temporary duplication during a migration.** When migrating from mono to multi, some code will exist in both the old monorepo and the new micro-repos during the transition window. That's OK — duplication is a temporary cost you pay for zero-downtime migration.

## Operating at Different Levels

| Level | Scope | Time Budget | Key Actions |
|-------|-------|-------------|-------------|
| **Quick** | Triage a repo boundary question | 5 minutes | Identify team topology, count cross-repo PR %, check CODEOWNERS coverage. Deliverable: one-line recommendation with top-3 risks. |
| **Standard** | Design a multi-repo architecture for a product area | 30 minutes | Map team-to-repo alignment, define shared library boundaries, design cross-repo CI orchestration, establish versioning strategy. Deliverable: boundary map + shared library catalog + CI orchestration diagram. |
| **Deep** | Full multi-repo strategy for an organization | 2-4 hours | Full coupling analysis from git history, team topology mapping, repo granularity heatmap, shared library lifecycle design, breaking change playbook, migration roadmap with cost estimates. Deliverable: architecture decision record + implementation plan. |

**Default level for this skill:** Standard (30min)

## When to Use

- You are deciding how to split a growing monorepo into independently deployable repos
- You need to design cross-repo dependency management: how repos discover, consume, and update shared libraries
- You are establishing versioning and release strategies for internal packages consumed by 5+ other repos
- You need to orchestrate CI/CD so that a change in Repo A triggers the right tests in Repos B, C, and D
- You are planning a breaking change in a shared library and need a migration playbook for 10+ consumer repos
- You are evaluating multirepo tooling: Nx distributed task execution, Lerna independent mode, Bazel cross-repo builds, pnpm workspace catalogs, Changesets for multi-package versioning
- You need to establish repo discoverability: how developers find the right repo, understand its purpose, and know who owns it
- You are designing CODEOWNERS, team ownership models, and contribution workflows across an org with 20+ repos
- You need a cross-repo testing strategy: contract tests, integration tests across repo boundaries, end-to-end tests spanning multiple services
- You are migrating from monorepo to multirepo (or reverse) and need a migration pattern that preserves velocity

#

## Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | monorepo-manager | Monorepo structure, build orchestration, dependency governance — the starting state for the split |
| **Before** | system-architect | Bounded context map, service topology, team boundaries — the architectural rationale for repo boundaries |
| **This** | multirepo-designer | Repo boundary design, cross-repo dependency management, shared library publishing, breaking change playbook |
| **After** | ci-cd-builder | Cross-repo CI pipelines with event-driven triggering, contract tests, and deployment orchestration |
| **After** | backend-developer | Service implementations within their designated repo boundaries with proper shared library consumption |
| **After** | fullstack-developer | Feature delivery across frontend and backend repos with coordinated release management |

Common chains:
- **Chain**: system-architect -> multirepo-designer -> ci-cd-builder — Architect defines bounded contexts; multirepo designer translates to repo boundaries; CI/CD builder orchestrates pipelines.
- **Chain**: monorepo-manager -> multirepo-designer -> backend-developer — Monorepo manager identifies extraction candidates; multirepo designer plans the split; backend developer implements services in new repos.

## Decision Trees

#

## Decision Trees — Quick Index
<!-- 366 lines of decision trees extracted to references/decision-trees.md -->

| # | Decision | When to Use |
|---|----------|-------------|
| 1 | Monorepo vs Multirepo | Team size, coupling, deployment frequency |
| 2 | Split Granularity | Bounded context boundaries, team autonomy |
| 3 | Shared Library Strategy | Internal vs external consumers, versioning |
| 4 | Cross-Repo CI/CD | Build ordering, release orchestration |
| 5 | Breaking Change Rollout | Migration windows, deprecation policies |
| 6 | Ownership & Discoverability | CODEOWNERS, catalog, service discovery |

> 📎 **Full decision trees (366 lines):** [references/decision-trees.md](references/decision-trees.md)

## Core Workflow
<!-- Full 46 lines extracted to references/core-workflow.md -->

#

## Phase 1 (~15 min): Coupling Analysis & Team Topology Mapping
1. Map all teams to their repos. Draw Conway alignment: does each repo have one clear owner?
2. Analyze cross-repo PR frequency over last 6 months: `git log --oneline --all | grep -i "#[0-9]" | sort | uniq -c`
3. Identify hotspots: repos with >30% cross-repo PRs are candidates for merging. Repos with <5% are correctly isolated.
...
> 📎 **[references/core-workflow.md](references/core-workflow.md)** — 46 lines of detailed guidance

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

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **System Architect** | Before splitting repos or defining boundaries | Bounded context map, service topology, coupling analysis results, repo boundary rationale |
| **Monorepo Manager** | Before extracting from a monorepo or merging into one | Current monorepo structure, build graph, affected detection configuration, package boundaries |
| **CI/CD Builder** | When setting up cross-repo CI pipelines | Cross-repo dependency graph, required CI triggers for each dependency type, shared workflow templates |
| **Backend Developer** | When defining shared library APIs | API stability requirements, versioning strategy, deprecation windows, migration guides |
| **Fullstack Developer** | When coordinating frontend-backend repo boundaries | API contracts, contract test setup, coordinated release timing |
| **DevOps Engineer** | When setting up internal registries and cross-repo infrastructure | Internal registry requirements, CI runner provisioning, repository_dispatch webhook setup |
| **Platform Engineer** | When building repo discovery and developer portals | Repo metadata standards, catalog integration, CODEOWNERS automation |
| **QA Engineer** | When designing cross-repo testing | Contract test frameworks, integration test environments, test impact analysis |
| **Engineering Manager** | When defining team-to-repo ownership | Team topology, CODEOWNERS assignments, review SLAs, escalation paths |
| **CTO Advisor** | For strategic repo topology decisions | Build-vs-buy for multirepo tooling, migration cost estimates, org-wide repo standards |

#

## Escalation Path

| Situation | Escalate To | Rationale |
|-----------|------------|-----------|
| Cross-repo coupling >40% despite documented boundaries | **System Architect** + CTO Advisor | Architecture drift; bounded contexts are wrong or unenforced |
| Shared library breaking change blocks 5+ teams for >2 weeks | **CTO Advisor** + VP Engineering | Migration velocity crisis; broken change management process |
| Repo sprawl — >100 repos with no discoverability | **Platform Engineer** + CTO Advisor | Developer productivity crisis; developer portal investment needed |
| Cross-repo CI takes >30 minutes and fails >20% of the time | **DevOps Engineer** + CI/CD Builder | CI infrastructure inadequate; investment or repo topology change needed |
| 3+ teams cannot agree on repo boundaries for a shared domain | **System Architect** + Engineering Manager | Conway's Law violation; team topology and repo topology must be aligned |

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `system-architect` | System context, integration points, architectural constraints | Before specialized implementation — understand the system it fits into |

## Proactive Triggers

| Trigger | Notify | Why |
|---------|--------|-----|
| Shared library major version bump (breaking change) published | All Consumer Teams, System Architect, CI/CD Builder | Migration window starts; automated PRs incoming; 4-week deadline for consumers |
| Cross-repo CI failure rate exceeds 10% for any dependency chain | DevOps, Affected Teams, CI/CD Builder | CI trust eroding; investigate contract drift, flaky tests, or infrastructure issues |
| New repo created without CODEOWNERS or team assignment | Platform Engineer, Engineering Manager | Orphan risk; repo must have owners within 48 hours or be archived |
| Dependency version drift detected across >5 repos for a framework dependency | All Consumer Teams, Platform Engineer | Runtime inconsistency risk; Renovate grouped update PR needed |
| Repo with zero commits in 6+ months (archival candidate) | Repo Owner, Engineering Manager | Maintenance burden; archive or document continued need |
| Cross-repo PR rate exceeds 30% for two repos that were supposed to be independent | System Architect, Affected Teams | Repo boundary failure; evaluate merge or extracted shared library |
| Internal package has >3 different major versions in use across consumer repos | All Consumer Teams, System Architect | Version fragmentation; standardize or accept migration debt |
| Breaking change migration progress stalls (<50% adoption after 2 weeks) | Team Leads, CTO Advisor | Blocked migration; investigate tools, docs, or competing priorities |
| CI runner concurrency exhausted due to cross-repo PR storm (Renovate opens 40+ PRs simultaneously) | DevOps, Platform Engineer | CI queue delays; batch Renovate updates or increase runner capacity |

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
     "skill": "multirepo-designer",
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

## What Good Looks Like

#

## BEFORE (Anti-pattern)
> A 50-person engineering org with 30 repos. No CODEOWNERS on 12 repos. Shared utilities copy-pasted across 8 repos with independent bug fixes applied inconsistently. Breaking changes announced in Slack with "heads up, we changed the API." Cross-repo CI: each team discovers breakage when their own CI fails after merging from main. Renovate opens 30 unrelated PRs daily, overwhelming review capacity. New hires take 2 weeks to understand which repo does what. Version drift: 4 different React versions across 15 frontend repos.

#

## AFTER (Healthy Multirepo)
> **Repo boundaries aligned to team topology.** Each team owns 1-3 repos — all have CODEOWNERS with >=2 reviewers. Shared code lives in 5 internal packages published to a private npm registry with strict semver and automated changelogs. **Breaking changes follow a 5-phase playbook**: new API ships alongside old -> deprecation with runtime warnings -> automated codemod tested against all consumers -> automated PRs to all consumer repos -> old API removed only after 100% adoption. **Cross-repo CI**: upstream repo triggers downstream CI via repository_dispatch; contract tests gate merges; Renovate groups updates weekly into <=5 PRs per repo. **Repo discoverability**: Backstage catalog indexes all repos by team, language, and status. New hires find the right repo in <5 minutes. **Zero version drift**: Renovate with grouped updates enforces all repos stay within 1 minor version of each other for framework dependencies.

> See [references/what-good-looks-like.md](references/what-good-looks-like.md) for the full quality standard.

## Deliberate Practice

```mermaid
graph LR
    A[Map team-repo topology] --> B[Measure cross-repo coupling] --> C[Redesign boundaries] --> D[Run migration simulation] --> A
```

| Level | Practice | Frequency |
|-------|----------|-----------|
| **Novice** | Take a 10-repo org and map every cross-repo dependency. Write a one-page ADR recommending 3 boundary changes with rationale. | Monthly |
| **Competent** | Design the shared library publishing pipeline for a hypothetical org with 20 consumer repos. Include: versioning strategy, CI triggers, breaking change playbook, and onboarding docs. Compare with an existing open-source multi-package project (e.g., Babel, Jest). | Quarterly |
| **Expert** | Take your own org's repo topology. Run a full coupling analysis from 6 months of git history. Propose 3 alternative topologies (monorepo, pure multirepo, hybrid) with quantified trade-offs per topology: CI time, cross-repo PR count, onboarding time, and operational cost. | Quarterly |
| **Master** | Design a repo governance framework that survives team reorgs. Include: repo creation checklist, archival criteria, CODEOWNERS rotation policy, contribution SLAs, and automated drift detection. Socialize and iterate with engineering leadership. | Annually |

**The One Highest-Leverage Activity:** Every quarter, do a "repo boundary audit." Take your 3 most coupled repos (highest cross-repo PR %). Ask: "If we merged these, what would break? If we split these differently, what would improve?" Write down your conclusions — over a year, you'll build an intuition for healthy boundaries.

## Anti-Rationalization Table

| What They Say | What It Really Means | The Reframe |
|---------------|---------------------|-------------|
| "We'll extract it to a shared library later." | "We don't want to do the extraction work now, so we'll pay 10x later when it's duplicated 8 times and each copy has diverged." | Extract when duplication reaches 3 copies, not when it's convenient. The extraction cost grows linearly with duplication count, but the divergence cost grows exponentially. |
| "Let's just create a new repo — it's cleaner." | "I don't want to understand the existing repo structure well enough to find where this code should live." | Every new repo is a 10-year commitment to CI, security, and maintenance. The "cleaner" repo is clean for 2 weeks — then it accumulates its own tech debt, just in a different place. |
| "We'll handle breaking changes by telling everyone in Slack." | "We don't want to invest in migration tooling, so we'll externalize the cost onto every consumer team." | Slack is not a migration strategy. Every hour you save by not building a codemod, every consumer team spends 10 hours migrating manually. Multiply by N consumer teams. |
| "The monorepo tools will catch up to our scale." | "We're betting our entire development velocity on a tooling roadmap we don't control." | Evaluate tools on what exists today, not what's promised. If the current tooling can't handle your scale, split now and merge later if the tools improve. |
| "We don't need CODEOWNERS — everyone knows who owns what." | "When the person who 'knows' leaves, this repo becomes an orphan overnight with no documentation." | Tribal knowledge is a single point of failure. CODEOWNERS is the bus-factor insurance — it costs 2 minutes to set up and prevents days of confusion when someone leaves. |
| "Copy-paste is fine for now — it's just 20 lines." | "We're planting 20 seeds of divergence. In 18 months, those 20 lines will be 20 different implementations with 20 different bug fixes applied to 18 of them." | Copy-paste is only acceptable when: the code hasn't changed in 12+ months AND you've documented that it's intentionally duplicated with a link to the canonical source. Otherwise, it's latent technical debt. |
| "We'll add cross-repo CI later — let's just get the repos set up first." | "We're deferring the hard part. Without cross-repo CI, every downstream breakage is discovered by the downstream team, eroding trust across the org." | Cross-repo CI is not a nice-to-have — it's the feedback loop that makes multirepo viable. Without it, you're running blind. Each downstream breakage costs 2-4 hours of debugging across two teams. |

## Gotchas

- **Shared library major version bump without consumer migration tooling.** You publish `design-system@3.0.0` with 12 breaking changes. Two days later, 15 consumer repos have broken CI. Each team spends 4-8 hours manually updating imports, props, and theme tokens. Teams that are on PTO or focused on other priorities don't discover the breakage until their next deploy — 2 weeks later. **Total cost: $30K-$80K in wasted engineering hours across 15 teams, plus $10K-$50K in delayed feature delivery from blocked deploys.** Fix: Never ship a breaking change without an automated migration script (codemod) tested against ALL consumer repos in CI. Open automated PRs to every consumer repo simultaneously. Track adoption and escalate laggards.
- **Reproducible builds fail because internal packages resolve differently across repos.** Repo A pins `@org/shared-utils@1.2.3` in its lockfile. Repo B uses a caret range `^1.2.3` and gets `1.3.0` from the registry. CI in Repo A passes (uses lockfile), CI in Repo B passes (gets latest compatible), but when both deploy together, they load different versions of `shared-utils` into the same browser bundle. A subtle behavior change in 1.3.0 causes a production bug that takes 6 hours to root-cause because "it works on my machine" and both CIs were green. **Total cost: $20K-$60K per incident in debugging time, plus $50K-$200K in revenue impact if the bug affects a customer-facing production path.** Fix: Use Renovate with grouped PRs to keep all repos within the same minor version. Add a CI check that verifies all consumer repos resolve the same version of shared dependencies. For libraries with runtime side effects, use exact version pinning.
- **Cross-repo CI feedback loop exceeding 30 minutes.** Repo A merges a change to `shared-auth@2.1.0`. Renovate opens PRs in Repos B through J. Each CI takes 15 minutes. Repo B's CI fails — root cause: the shared-auth change broke JWT token parsing. The engineer who made the change has already started their next task. By the time they context-switch back, 45 minutes have passed. Over 200 such cross-repo changes per year, the cumulative context-switching cost alone is $50K-$150K in lost productivity. **Total cost: $40K-$100K/year in CI wait time + $50K-$150K/year in context-switching overhead = $90K-$250K/year total.** Fix: Run downstream CI BEFORE merging the upstream change — use PR-level cross-repo CI that gates the merge. Cache shared dependencies aggressively. Use npm/pip/gradle build caches. Target <10 minutes for cross-repo CI feedback.
- **org-wide Renovate/Dependabot opening 40+ PRs every Monday morning.** Every repo has Renovate configured independently. A new React 19 patch release triggers 15 PRs across 15 frontend repos. A new ESLint plugin version triggers 12 PRs. TypeScript 5.5 triggers 18 PRs. Total: 45 PRs every Monday. Developer review capacity: ~8 PRs/day across the team. Pile-up creates a 5-day review backlog. Critical security patches get buried in the noise. One CVE patch (lodash prototype pollution) sits unreviewed for 12 days because it's PR #37 in the queue. **Total cost: $30K-$80K/year in review overhead + $20K-$200K in security exposure from delayed CVE patches.** Fix: Group Renovate updates into weekly batches. Pin non-critical dependencies to auto-merge on CI green. Separate security patches into their own high-priority PR stream with SLA-based review requirements (<24 hours for critical, <72 hours for high). Limit open Renovate PRs to <=5 per repo at any time.
- **Git submodules silently pointing to wrong commits after git operations.** Team A uses `@org/core-lib` as a git submodule in 3 repos. A developer runs `git checkout feature-branch` — the submodule pointer stays on the old commit. They make changes, run tests (which pass — using the wrong submodule version), and merge. Production breaks because the submodule commit doesn't match what CI tested. This happens 2-3 times per quarter. Each incident takes 2-4 hours to diagnose because "it passed CI" and the submodule commit SHA looks correct (it's the commit that CI tested — it's just not the one the developer intended). **Total cost: $15K-$40K/year in debugging submodule state issues, plus $20K-$80K in production incidents from version mismatches.** Fix: Replace git submodules with internal package registry + version pinning. If submodules are unavoidable, add a CI check: `git submodule status --recursive | grep -v "^ "` (warns on dirty/unpinned submodules). Never merge if submodules are in detached HEAD state.
- **Multi-language shared library maintenance creating NxM compatibility matrix.** You have a shared protobuf/OpenAPI schema consumed by 3 Go services, 2 TypeScript frontends, 1 Python data pipeline, and 1 Rust performance service. Each language has its own client library repo generated from the schema. A schema change requires updating 7 repos — but the Go generator produces different default values than the TypeScript generator, and the Python generator handles optional fields differently than Rust. A field marked `optional` in proto3 generates `*string` in Go (nil-able), `string | undefined` in TypeScript, `Optional[str]` in Python (has a `.is_set()` method), and `Option<String>` in Rust. A null value flows through Go, hits the TypeScript frontend, and triggers a runtime crash because TypeScript didn't receive the field at all (not `undefined`, just absent). **Total cost: $100K-$500K/year in multi-language client maintenance, plus $50K-$200K/year in cross-language integration bugs.** Fix: Centralize schema ownership in one repo with language-agnostic tests (JSON schema validation, protobuf conformance tests). Generate all language clients from a single CI pipeline and publish simultaneously. Add cross-language integration tests that verify behavior parity for null handling, defaults, and edge cases across ALL generated clients.
- **Breaking change in a shared infra repo (Docker base image, Terraform module, CI template) cascading silently.** A platform engineer updates the base Docker image from `node:20-alpine` to `node:22-alpine` in the `shared-infra` repo. The change passes their own CI (which tests the image build, not the 25 downstream services using it). Three weeks later, the `payments-service` team does a routine deploy. Their build uses the new base image. Node 22 removed a deprecated crypto API that payments-service relied on. The service crashes in production during payment processing at 3 PM on a Friday. The payments team spends 4 hours debugging, never suspecting the base image change because "we didn't change anything." **Total cost: $60K-$150K in incident response and lost revenue during the outage, plus $30K-$80K in cross-team debugging to trace the root cause.** Fix: Shared infra changes must trigger smoke tests in ALL downstream repos BEFORE merge. Use repository_dispatch to fan out. Pinned versions with Renovate for base images (never `:latest` or `:alpine` without a digest). Add a "what changed" diff in every Renovate PR for shared infra.
- **Internal package abandoned because the original author left the company.** `@org/ml-utils@1.5.0` has 8 consumer repos and zero maintainers. The original author (a senior ML engineer) left 14 months ago. The package has 3 open CVEs, 12 stale dependabot PRs, and a blocking bug that prevents upgrading to Python 3.12. Every consumer team assumes "someone else" maintains it. When Python 3.11 goes EOL, all 8 consumer repos are blocked — but no team has the context or confidence to fix the package, because the test coverage is 23% and the codebase uses esoteric numpy patterns the author never documented. **Total cost: $80K-$200K in migration costs when 8 teams must either fork+fix or replace the abandoned package, plus $30K-$100K in delayed platform upgrades.** Fix: Every published internal package must have >=2 named maintainers from different teams (bus factor). Automate maintainer rotation via CODEOWNERS. Add a CI check: if the last commit to a shared package is >90 days old, flag for maintainer review. Run `npm audit` / `pip-audit` on all internal packages weekly and auto-assign CVEs to maintainers with SLAs.
- **Repo naming conventions degrading discoverability at 100+ repos.** Over 4 years, repos accumulate with inconsistent naming: `api-gateway`, `gateway-api`, `platform-gateway`, `gateway-v2`, `gateway-service`, `services-gateway`. New hires searching for "how to add a route to the gateway" find 6 repos and cannot determine which is canonical. They pick the wrong one, implement against a deprecated gateway, and discover their mistake during code review 3 days later. This happens ~15 times/year across different domains (auth, payments, search). **Total cost: $15K-$40K/year in misdirected engineering effort + $10K-$30K/year in onboarding friction for new hires.** Fix: Enforce a repo naming convention: `[team]-[domain]-[purpose]` or `[org]-[function]`. Example: `platform-api-gateway`, `auth-sso-service`, `data-ml-pipeline`. Add a repo description template: "Owned by [team]. [One-sentence purpose]. Status: [active|maintenance|deprecated]. Language: [primary]." Index all repos in a developer portal (Backstage, Compass) with search by team, language, and domain.
- **Monorepo-to-multirepo split without preserving git history.** You split a 3-year-old monorepo into 8 service repos using `cp -r` instead of `git filter-repo`. Every file shows "Initial commit" with today's date and your name as author. The original authors, commit messages explaining WHY code was written, and PR discussions are lost. Six months later, an engineer debugging a production issue in `billing-service` runs `git blame` — every line says "Initial commit, Migration Engineer, 2025-04-01." They can't trace the logic to the original PR, can't find the design discussion, and can't ask the original author (who left 18 months ago). A 2-hour debugging session becomes a 3-day archaeology project. **Total cost: $40K-$100K in lost historical context across all split repos, compounding every time someone needs to understand legacy code (~$5K-$10K per incident x dozens of incidents over the repos' lifetime).** Fix: Use `git filter-repo` with `--path` and `--path-rename` to extract directories into separate repos while preserving full commit history, authors, and dates. Validate with `git log --follow [key-file]` that history is intact. Never use `cp -r` + `git init` for repo splits. The history is the most valuable artifact — more valuable than the code itself.

## Verification

- [ ] Every repo has CODEOWNERS with >=2 individuals from the owning team
- [ ] Cross-repo coupling measured: `git log --all --oneline --since="6 months ago" | grep "cross-repo\|depends-on" | wc -l` — <15% of total PRs
- [ ] Shared libraries publish to internal registry with semver: `npm view @org/shared-lib versions` shows proper version history
- [ ] Breaking change playbook artifact exists: migration guide + codemod + consumer adoption dashboard
- [ ] Cross-repo CI: upstream PR triggers downstream CI, downstream green before upstream merges
- [ ] Zero submodules for actively developed code: `find . -name .gitmodules | xargs grep "url" | wc -l` == 0 or all submodules have justification in ADR
- [ ] Repo discoverability: new hire can find the correct repo for any domain in <5 minutes using search or catalog
- [ ] No orphan repos: `gh repo list --limit 200 --json name,updatedAt | jq '.[] | select(.updatedAt < "2024-01-01")'` returns zero unaccounted repos
- [ ] Version drift within tolerance: all consumer repos within 1 minor version of each other for shared framework dependencies
- [ ] Internal package maintainer bus factor >=2: every published package has >=2 named maintainers in CODEOWNERS

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

- **Build System & Cross-Repo Orchestration**: See [references/build-system-cross-repo.md](references/build-system-cross-repo.md)
- **Breaking Change Management**: See [references/breaking-change-management.md](references/breaking-change-management.md)
- **Repo Governance & Ownership**: See [references/repo-governance-ownership.md](references/repo-governance-ownership.md)
- **Shared Library Publishing & Versioning**: See [references/shared-library-publishing.md](references/shared-library-publishing.md)
- **Tool Selection & Decision Matrix**: See [references/tool-selection-matrix.md](references/tool-selection-matrix.md)
- **Monolith Decomposition Patterns**: See [references/monolith-decomposition.md](references/monolith-decomposition.md)
- **Anti-Patterns Catalog**: See [references/anti-patterns.md](references/anti-patterns.md)
- **Calibration**: See [references/calibration.md](references/calibration.md)
- **Scale Depth: Solo -> Small -> Medium -> Enterprise**: See [references/scale-depth.md](references/scale-depth.md)
- **Footguns**: See [references/footguns.md](references/footguns.md)
- **Error Decoder**: See [references/error-decoder.md](references/error-decoder.md)
- **Sub-Skills**: See [references/sub-skills.md](references/sub-skills.md)
- **What Good Looks Like**: See [references/what-good-looks-like.md](references/what-good-looks-like.md)
