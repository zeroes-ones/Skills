---
name: git-submodules
description: >
  Use when sharing code across multiple repositories and evaluating git
  submodules, git subtree, or alternative approaches; when managing vendor
  dependencies that need local modification; when extracting a subdirectory
  from a monorepo into its own repository while preserving git history; when
  troubleshooting submodule CI failures (detached HEAD, recursive clone
  failures, merge conflicts); when deciding between submodules, subtrees,
  private package registries, or copy-paste for cross-repo code sharing; or
  when recovering from submodule disasters (out-of-sync pointers, accidental
  deletions, corrupted .gitmodules). Handles submodule vs subtree vs package
  registry vs vendoring decision matrix (update frequency, contributor count,
  CI complexity), submodule lifecycle management (add, update, deinit,
  recursive operations, tracking branches), submodule CI/CD configuration
  (recurse-submodules cloning, GitHub Actions checkout, caching strategies),
  git subtree workflows (add, pull, push, split for bidirectional code
  sharing), the split-filter extraction pattern (git filter-repo for
  monorepo-to-polyrepo extraction with history preservation), vendoring
  strategies and when to vendor vs link, common disaster recovery procedures
  (detached HEAD fixes, merge conflict resolution, submodule restoration), and
  alternative tools evaluation (git-subrepo, gitslave, repo tool, myrepos). Do
  NOT use for monorepo architecture decisions (route to monorepo-manager),
  package publishing workflows (route to appropriate language skill), or CI/CD
  pipeline design (route to ci-cd-builder).
author: Sandeep Kumar Penchala
license: MIT
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
type: devops
status: stable
version: 1.0.0
updated: 2026-07-23
tags:
  - git
  - submodules
  - subtrees
  - vendoring
  - polyrepo
  - code-sharing
  - git-filter-repo
  - dependency-management
token_budget: 4500
chain:
  consumes_from:
    - monorepo-manager
    - ci-cd-builder
  feeds_into:
    - monorepo-manager
    - migration-architect
  alternatives: []
---
# Git Submodules & Subtrees

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

The definitive playbook for sharing code across Git repositories using submodules, subtrees, and vendoring — when monorepo is not the answer. Covers decision frameworks, lifecycle management, CI/CD integration, disaster recovery, and the split-filter extraction pattern. Focus on practical, battle-tested workflows with explicit failure modes — not Git manual recitations.

## Ground Rules — Read Before Anything Else

These rules are non-negotiable constraints that prevent the most common submodule disasters before they happen. Violation means STOP and refuse to proceed.

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to recommend submodules for teams without a documented submodule workflow. Submodules without a workflow are detonated-HEAD mines. | Trigger: response recommends submodules AND no mention of documented workflow (update procedure, CI config, merge conflict playbook) | STOP. Respond: "Git submodules without a documented team workflow are a disaster waiting to happen. Before adopting submodules: (1) document the update procedure, (2) configure CI with --recurse-submodules, (3) create a playbook for detached HEAD recovery, merge conflicts, and accidental deletions, (4) add submodule health checks to CI. Without these, submodules will cause recurring outages." |
| R2 | DETECT when submodule pointer is checked in without --recurse-submodules in CI. This is the #1 cause of "works on my machine" submodule failures. | Trigger: response describes submodule setup AND CI config does not include submodule checkout | STOP. Respond: "Your CI must clone with --recurse-submodules or configure checkout action with submodules: recursive. Without this, CI builds with stale or missing submodule content. GitHub Actions: uses: actions/checkout@v4 with: submodules: recursive. Every CI job needs this." |
| R3 | REFUSE to recommend `git subtree` for bidirectional workflows without acknowledging merge conflict hell. Subtree push is lossy by design. | Trigger: response recommends subtree push/split for bidirectional code sharing AND no warning about merge conflicts during pull | STOP. Respond: "git subtree push rewrites history when splitting. Pulling changes back from the subtree repo will cause merge conflicts because commit SHAs differ. Subtree works for one-way sharing. For bidirectional sharing, prefer submodules or a package registry." |
| R4 | REFUSE to recommend "just vendor it" for dependencies that receive security patches. Vendored code gets stale silently. | Trigger: response recommends vendoring AND dependency has frequent releases AND no update mechanism described | STOP. Respond: "Vendoring without an update mechanism is a security risk. You must have: (1) automated monitoring for upstream releases, (2) a documented update procedure, (3) a CI check alerting when vendored code is >30 days behind upstream. Without these, you ship known vulnerabilities." |
| R5 | REFUSE to execute `git submodule deinit` or `rm -rf .git/modules` without confirming user has no uncommitted changes in submodules. This deletes work. | Trigger: response contains submodule deinit/removal commands AND no prior check for uncommitted submodule changes | STOP. Respond: "Before removing a submodule: (1) cd into submodule, (2) git status for uncommitted changes, (3) git push any unpushed commits, (4) cd back, (5) only then run removal. Skipping steps 1-3 permanently deletes work." |
| R6 | DETECT when submodule tracking branch is not configured. Detached HEAD is the default submodule state. | Trigger: response adds a submodule AND .gitmodules does not include branch config | STOP. Respond: "Submodules default to detached HEAD. Add: git config -f .gitmodules submodule.path.to.sub.branch main. Then: git submodule update --remote to track the branch tip." |
| R7 | REFUSE to recommend submodules for repos with >20 submodules. Recursive operations become brittle at scale. | Trigger: response recommends submodules AND repo has or would have >20 submodule entries | STOP. Respond: "Submodules do not scale beyond ~20 entries. Recursive clones slow, CI becomes unwieldy, probability of out-of-sync approaches 100%. Evaluate: git-subrepo, monorepo migration, or private package registry." |
| **R8** | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| **R9** | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |

- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset

You are a Git internals expert who has recovered from every submodule disaster: detached HEADs, orphaned .git/modules directories, submodule merge conflicts that spanned 40 commits, and the special hell of `git subtree split` rewriting history. Your mental model:

* **Submodules are pointers, not content.** A submodule is just a commit SHA stored in the parent tree. Everything else — the actual files, the .git directory, the working tree — is derived. When you understand this, all submodule behavior becomes predictable.
* **The tool is not the problem — the workflow is.** Git submodules work at Google, Meta, and thousands of open-source projects. The difference is they have documented, enforced workflows. Without them, submodules are footguns. With them, they are infrastructure.
* **Vendoring is a liability, not just a dependency.** Every vendored line of code is code you are now responsible for maintaining, securing, and updating. Treat vendoring as a decision to fork, not a convenience.
* **History preservation matters.** `git filter-repo` and `git subtree split` exist because history has value — blame, bisect, provenance. The difference between a good extraction and a bad one is whether `git log` still works afterward.
* **CI is the enforcement mechanism.** Whatever workflow you design, CI must enforce it. Submodule health checks should run on every PR. A stale submodule should fail CI as aggressively as a failing test.

## Operating at Different Levels

* **Quick scan (30s):** Check .gitmodules exists, submodule count, tracking branch config, submodule update status. Flag: detached HEAD in submodules, submodules without branch config, >20 submodule entries.
* **Triage (10min):** Verify all submodule pointers are reachable (no orphaned SHAs). Run `git submodule status --recursive`. Check CI config for submodule checkout. Verify .gitmodules has no stale entries.
* **Deep workflow design (full session):** Full cross-repo code sharing architecture: decision matrix analysis, submodule/subtree/vendor selection, CI integration, disaster recovery playbooks, team training materials, migration plan.
* **Crisis mode (submodule broken, CI red, deployment blocked):** Identify failure: detached HEAD? merge conflict? missing submodule? Apply the appropriate recovery from the Disaster Recovery decision tree. Get CI green first, then diagnose root cause.

### Scale Depth

#### Solo (1-3 repos, occasional code sharing)
Use GitHub template repos or copy-paste with clear attribution. Avoid submodules entirely — the operational overhead exceeds the benefit. Pin shared code with a `SHARED_VERSION` comment and periodically diff against upstream.

#### Small Team (3-10 repos, shared library co-developed by 2-3 engineers)
Submodules with branch tracking (`branch = main`) plus a weekly automated CI job that opens PRs when submodule SHAs drift. One `.gitmodules` template copied across repos. Document the update cadence in the repo README.

#### Medium Org (10-50 repos, 5-15 submodules across repos)
Full submodule health monitoring: detached HEAD audit, reachability check, CI caching with `.gitmodules` hash. Pre-commit hooks for submodule hygiene. Disaster recovery playbook with documented runbooks for top-5 failure modes. **Transition trigger:** When submodule count exceeds 15 or consumer repos exceed 10, invest in automated health monitoring — manual audits cannot keep up.

#### Enterprise (50+ repos, polyglot codebase, cross-team dependencies)
Dedicated code-sharing architecture role. Submodule + subtree + package registry strategy per dependency type. Automated submodule update PRs with CI gating (Renovate/Dependabot configured per submodule). Submodule health dashboard visible to all teams. Migration playbook for subtree → submodule → package registry transitions. Annual re-evaluation: is submodule still the right pattern, or has the dependency matured to justify a package registry? **Transition trigger:** When multiple teams maintain separate submodule update cadences, invest in shared automation and a code-sharing governance board.

## When to Use

Use git-submodules when sharing code across repositories and the alternatives (monorepo, package registry) are not viable — the focus is on Git-native code sharing mechanisms and their operational implications.

* Deciding between submodules, subtree, vendoring, and package registries for cross-repo code sharing
* Adding a shared library as a submodule and configuring tracking branches
* Setting up CI/CD to correctly clone and update submodules
* Extracting a subdirectory from a monorepo into its own repo with full history preservation
* Setting up bidirectional code sharing with `git subtree` (push/pull/split)
* Managing vendor dependencies that require local modifications
* Recovering from submodule disasters: detached HEAD, merge conflicts, accidental deletion
* Auditing submodule health: stale pointers, orphaned commits, incorrect .gitmodules
* Evaluating alternative tools: git-subrepo, gitslave, repo tool, myrepos

Do NOT use git-submodules for monorepo architecture decisions (route to monorepo-manager). Do NOT use for package publishing workflows (route to appropriate language skill). Do NOT use for CI/CD pipeline design (route to ci-cd-builder).

## Route the Request

#

## Auto-Route by Artifacts (Check Filesystem First)

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_exists(".gitmodules")` AND `file_contains(".gitmodules", "[submodule")` | Active submodules -> Go to **Core Workflow: Phase 1 — Submodule Health Audit** |
| A2 | `file_contains(".gitmodules", "submodule.*url.*=")` AND submodule dir has uncommitted changes | Dirty submodule -> Jump to **Decision Trees: Disaster Recovery** |
| A3 | `file_exists(".gitmodules")` with entries for directories that no longer exist | Orphaned submodule entries -> Jump to **Decision Trees: Submodule Cleanup** |
| A4 | `grep -r "git subtree" Makefile CMakeLists.txt package.json scripts/` | Subtree workflow detected -> Go to **Core Workflow: Phase 3 — Subtree Audit** |
| A5 | `file_exists("vendor/")` OR `file_exists("third_party/")` with >10 directories | Vendoring pattern -> Jump to **Decision Trees: Vendoring Assessment** |
| A6 | User mentions "extract" + "subdirectory" + "history" | Split-filter needed -> Go to **Core Workflow: Phase 2 — Split-Filter Extraction** |
| A7 | No submodule/subtree/vendor files | New cross-repo sharing decision -> Jump to **Decision Trees: Code Sharing Strategy** |

#

## Intent Route (Ask the User)

```
What git submodule/subtree task are you working on?
|-- Deciding how to share code across repos -> Jump to "Decision Trees: Code Sharing Strategy"
|-- Adding a new submodule to my repo -> Go to "Core Workflow: Phase 1 — Add Submodule"
|-- Fixing a broken submodule (detached HEAD, conflicts) -> Jump to "Decision Trees: Disaster Recovery"
|-- Extracting a subdirectory into its own repo -> Go to "Core Workflow: Phase 2 — Split-Filter"
|-- Setting up CI for submodules -> Go to "Core Workflow: Phase 4 — CI Integration"
|-- Managing vendor dependencies -> Jump to "Decision Trees: Vendoring Assessment"
|-- Evaluating alternatives to submodules -> Jump to "Decision Trees: Alternative Tools"
|-- Auditing existing submodule health -> Go to "Core Workflow: Phase 1 — Health Audit"
```

## Core Workflow **(STANDARD)**
<!-- Full 131 lines extracted to references/core-workflow.md -->

#

## Phase 1: Submodule Health Audit
Execute in order. Do not skip steps.
1. INVENTORY ALL SUBMODULES
2. DETACHED HEAD CHECK
...
> 📎 **[references/core-workflow.md](references/core-workflow.md)** — 131 lines of detailed guidance

## Decision Trees **(QUICK)**

#

## Error Decoder — War Stories from the Trenches

**(STANDARD)**

When this domain goes wrong, it goes wrong in predictable ways. Here are the most common failure signatures, their root causes, and the fix you'll reach for after you've been burned once.

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| `git submodule update --init --recursive` in CI returns success but the submodule directory is empty — builds fail with "file not found" | The CI runner (GitHub Actions `actions/checkout@v4`) checks out the repo with `submodules: false` by default. The submodule update command runs but has no `.gitmodules` file to read because the checkout didn't include it. | Set `submodules: recursive` in the checkout action, not as a separate step. If you must use a separate step, run `git submodule sync --recursive` first to re-link the `.gitmodules` paths before `update`. | CI checkout behavior is the #1 source of submodule failures. The `.gitmodules` file lives in the parent repo — if the checkout step doesn't fetch it, no submodule command will work. |
| Developer runs `git push` on the parent repo — CI passes, deployment succeeds, but the submodule pointer is at a commit that doesn't exist on the remote | The developer committed and pushed inside the submodule directory, then committed the new pointer in the parent. But they forgot to `git push` inside the submodule first. The parent references a commit hash that only exists on their local machine. | Add a pre-push hook in the parent repo: `git submodule foreach 'git push'` before the parent push. Or use a CI check that verifies `git ls-remote <submodule-url> <commit-hash>` succeeds for every submodule pointer before merging. | Submodules create a distributed reference graph — a pointer in the parent is only valid if the target commit exists at the submodule remote. This is a push-order dependency that no amount of documentation will fix. |
| Developer runs `git pull` on the parent — gets merge conflicts in `.gitmodules` and the submodule pointer. Spends 45 minutes untangling the submodule state. | Two teammates changed the submodule pointer to different commits and also modified `.gitmodules` (one added `branch = main`, the other added `shallow = true`). Git treats `.gitmodules` as a regular file and the submodule pointer as a tree entry — they can conflict independently. | Standardize `.gitmodules` options in a team policy (e.g., `branch` is always set, `shallow` is always unset). Use `git submodule absorbgitdirs` to normalize submodule state. For conflicts: `git checkout --ours .gitmodules && git submodule update` is usually correct. | Submodule conflicts are two-dimensional — file conflicts in `.gitmodules` AND tree conflicts in the index. Resolving one without the other leaves the submodule in a corrupt state. |
| CI pipeline clones the repo — `git clone --recurse-submodules` takes 8 minutes for a repo with 12 submodules, each of which has its own submodules | Every submodule is a full clone including all history. One submodule is a fork of `llvm-project` (2GB). The CI runner downloads 4.7GB of Git history for 3 files of shared code. | Switch to `git clone --recurse-submodules --shallow-submodules --depth=1` for CI. Or partially convert the heaviest submodules to `git subtree` — subtree bakes the code into the parent repo at merge time, eliminating clone overhead entirely. | Submodule clone time grows linearly with the number and size of submodules. A 30-second checkout becomes an 8-minute checkout — and it gets worse every time someone adds another shared dependency. |
| `git submodule update --remote` silently succeeds but the submodule is now on a random commit from the remote's default branch — production deploys untested code | `--remote` updates to the HEAD of the submodule's tracked branch (default: the remote's default branch), not the pinned commit. A developer ran this during a hotfix, didn't notice the pointer changed, and committed the result. | Never use `git submodule update --remote` outside of a deliberate dependency update workflow. Use `git submodule update --init --recursive` (no `--remote`) for checkout. For updates: branch → PR → CI runs against the new pointer → merge. | `--remote` is a footgun masquerading as a convenience flag. It silently unpins your dependencies. If you need floating submodule refs, you probably need a package manager, not submodules. |

## Code Sharing Strategy Selection

```
How should you share code across repositories?
|-- Evaluation criteria (score each option 1-5):
|   |-- Update frequency: how often does shared code change?
|   |-- Contributor count: how many people modify the shared code?
|   |-- Consumer count: how many repos depend on this code?
|   |-- CI complexity tolerance: how much CI config overhead is acceptable?
|   |-- History importance: does blame/log history need to be preserved?
|   |-- Security sensitivity: is this auth, crypto, or security-critical code?

|-- Pattern 1: Git Submodules
|   |-- Best when: 2-10 consumers, infrequent updates (weekly-monthly), dedicated owners
|   |-- Pros: exact version pinning, clear dependency declaration, native Git
|   |-- Cons: detached HEAD risk, CI complexity, merge conflict pain
|   |-- Scores well on: history preservation (5), contributor clarity (4)
|   |-- Scores poorly on: CI simplicity (2), update frequency (2)

|-- Pattern 2: Git Subtree
|   |-- Best when: 1-3 consumers, code modified in consumer repo, one-way sync acceptable
|   |-- Pros: no separate clone step, code is just files in the repo
|   |-- Cons: history bloat (without --squash), push rewrites history, complex merge resolution
|   |-- Scores well on: CI simplicity (5), consumer experience (4)
|   |-- Scores poorly on: bidirectional sharing (1), contributor clarity (2)

|-- Pattern 3: Private Package Registry
|   |-- Best when: 5+ consumers, frequent updates (daily), mature CI/CD pipeline
|   |-- Pros: versioned releases, CI/CD independent, ecosystem tooling (npm, pip, maven)
|   |-- Cons: registry infrastructure, release process overhead, version compatibility matrix
|   |-- Scores well on: CI simplicity (5), consumer count scalability (5)
|   |-- Scores poorly on: local modification workflow (1), setup cost (2)

|-- Pattern 4: Vendoring (copy-paste + track)
|   |-- Best when: 1-2 consumers, need local modifications, dependency is small and stable
|   |-- Pros: zero tool complexity, full control, no external dependency at build time
|   |-- Cons: security patching nightmare, drift from upstream, no automated updates
|   |-- Scores well on: CI simplicity (5), local modification (5)
|   |-- Scores poorly on: security maintenance (1), update tracking (1)

|-- RECOMMENDATION MATRIX:
|   |-- Frequent updates + many consumers + mature CI -> Package Registry
|   |-- Infrequent updates + few consumers + need history -> Submodules
|   |-- Code modified locally + one-way sync -> Subtree
|   |-- Small, stable dep + need modifications + no registry -> Vendoring
|   |-- NEVER: Submodules without CI automation, Vendoring without update tracking
```

#

## Disaster Recovery

```
What submodule disaster are you facing?
|-- Detached HEAD after git submodule update
|   |-- Cause: submodule is pinned to a commit, not tracking a branch
|   |-- Fix (temporary): cd <submodule> && git checkout main
|   |-- Fix (permanent): git config -f .gitmodules submodule.<path>.branch main
|   |-- Then: git submodule update --remote -- <path>
|   |-- Verify: git submodule status shows branch tip, not detached

|-- Submodule merge conflict in parent repo
|   |-- Cause: two branches updated the same submodule pointer to different SHAs
|   |-- Fix: git checkout --theirs -- <submodule-path> OR git checkout --ours -- <submodule-path>
|   |-- Then: git add <submodule-path>
|   |-- Then: verify the chosen SHA is the right one: cd <submodule> && git log -1
|   |-- Prevention: use git submodule update --remote before merging branches

|-- Accidental submodule deletion (directory empty after clone)
|   |-- Cause: .gitmodules has entry but submodule not initialized
|   |-- Fix: git submodule update --init --recursive
|   |-- If .gitmodules has wrong entry: git submodule deinit <path>, edit .gitmodules, git submodule add <url> <path>
|   |-- If .git/modules/<path> is missing: remove from .gitmodules and .git/config, re-add submodule

|-- Submodule points to commit that no longer exists (force push upstream)
|   |-- Cause: upstream repo history was rewritten (force push, rebase, squash merge)
|   |-- Fix: cd <submodule> && git fetch origin && git log origin/main --oneline
|   |-- Find the equivalent commit in the new history (same changes, different SHA)
|   |-- Update parent pointer: cd .. && git add <submodule-path> && git commit -m "Update submodule after upstream rebase"
|   |-- Prevention: NEVER force-push to repos used as submodules. Use branches/tags.

|-- "fatal: No url found for submodule path" during clone
|   |-- Cause: .gitmodules missing or has stale entry, or submodule URL is relative and base URL unknown
|   |-- Fix: git submodule sync --recursive (syncs .git/config URLs from .gitmodules)
|   |-- If .gitmodules is corrupted: restore from another branch: git checkout main -- .gitmodules
|   |-- Then: git submodule update --init --recursive
```

#

## Vendoring Assessment

```
Should you vendor this dependency?
|-- VENDORING CHECKLIST (all must be true):
|   |-- Dependency is small (<5K LOC) and stable (<1 release per quarter)
|   |-- You need to make local modifications that cannot be upstreamed
|   |-- You have automated monitoring for upstream releases (Dependabot/Renovate on vendor dir)
|   |-- You have a documented update procedure that takes <1 hour
|   |-- The dependency is NOT security-critical (auth, crypto, network parsing)
|   |-- You are willing to accept maintenance responsibility for this code
|
|-- Vendoring Strategy Options:
|   |-- Go-style: vendor/ directory at repo root, managed by go mod vendor
|   |-- Third-party style: third_party/<dep-name>/ with README tracking upstream version
|   |-- Monorepo vendoring: copy into internal/ directory with namespace prefix
|
|-- Vendoring Maintenance:
|   |-- Track upstream version: VENDOR_VERSION file alongside vendored code
|   |-- Diff against upstream: script that diffs vendor dir against upstream tag
|   |-- Update cadence: quarterly for stable deps, monthly for active deps
|   |-- CI check: alert if vendor dir is >90 days behind upstream (fail CI at 180 days)
|
|-- When to UN-VENDOR:
|   |-- Dependency has >4 releases per year -> migrate to package registry
|   |-- Multiple repos need the same vendored code -> extract to shared submodule/package
|   |-- Security vulnerability disclosed -> patch immediately or un-vendor and use upstream
```

#

## Submodule Health Monitoring

```
How to prevent submodule problems before they cause outages:
|-- Automated Health Checks (CI, runs on every PR):
|   |-- git submodule status --recursive (are all submodules initialized?)
|   |-- git submodule foreach 'git rev-parse HEAD' (is HEAD detached?)
|   |-- git submodule foreach 'git fetch origin && git status -uno' (are we up to date?)
|   |-- For tracking-branch submodules: git submodule foreach 'git rev-list --count HEAD..origin/main'
|   |   |-- 0 commits behind: up to date
|   |   |-- 1-10 commits behind: acceptable (within sprint)
|   |   |-- 10-50 commits behind: warning (getting stale)
|   |   |-- 50+ commits behind: alert (security risk for sensitive deps)

|-- Monthly Audit (scheduled CI job):
|   |-- Reachability: git submodule foreach 'git cat-file -t HEAD' (all SHAs exist?)
|   |-- Orphan check: compare .gitmodules entries with actual directories
|   |-- Auth check: verify CI tokens still have access to all submodule repos
|   |-- Size check: git submodule foreach 'du -sh .git' (any submodule bloated?)
|   |   |-- >500MB .git: consider shallow clone or partial clone for CI

|-- Dashboard Metrics:
|   |-- Submodule staleness by repo (commits behind tracking branch)
|   |-- Submodule CI checkout time (trending slower = need cache tuning)
|   |-- Submodule-related CI failure rate (target: <1%)
|   |-- Submodule update PR merge time (target: <48 hours)

|-- Proactive Update Cadence:
|   |-- Security-critical deps (auth, crypto, network parsing): weekly automated update PR
|   |-- Active deps (>1 release/month): bi-weekly automated update PR
|   |-- Stable deps (<1 release/quarter): monthly automated update PR
|   |-- Pinned-to-specific-version: quarterly review (is the pinned version still correct?)
```

#

## Submodule Migration Patterns

```
How to migrate BETWEEN submodule-based and other code-sharing strategies:
|-- FROM Submodules TO Monorepo:
|   |-- Step 1: Identify the submodule content to merge into monorepo
|   |-- Step 2: Use git-filter-repo to extract submodule content with history
|   |-- Step 3: Merge the extracted history into monorepo at target path
|   |   |-- git remote add extracted ../extracted-repo
|   |   |-- git fetch extracted
|   |   |-- git merge --allow-unrelated-histories extracted/main
|   |-- Step 4: Update monorepo code to use merged code (remove submodule references)
|   |-- Step 5: Archive original submodule repo (read-only, with pointer to new location)

|-- FROM Submodules TO Package Registry:
|   |-- Step 1: Set up package registry (npm, Maven, PyPI, private registry)
|   |-- Step 2: Add package.json/setup.py/pom.xml to submodule repo
|   |-- Step 3: Publish initial version to registry
|   |-- Step 4: Consumer-by-consumer: switch from submodule to package dependency
|   |   |-- Remove submodule: git submodule deinit, rm -rf .git/modules, git rm
|   |   |-- Add package: npm install @org/lib@1.0.0
|   |-- Step 5: After all consumers migrated: archive submodule repo

|-- FROM Vendoring TO Submodules:
|   |-- Step 1: Create a new repo with the vendored code + its commit history
|   |   |-- Use git-filter-repo on original monorepo if the code was extracted
|   |-- Step 2: Push to a new shared repo
|   |-- Step 3: Consumer-by-consumer: remove vendored code, add submodule
|   |-- Step 4: Update CI to handle submodule checkout
|   |-- Step 5: Set up update monitoring (Dependabot for submodules)

|-- FROM Package Registry TO Submodules (RARE):
|   |-- Only when: need local modifications, registry unavailable, strict version pinning
|   |-- Step 1: git submodule add the package's source repo
|   |-- Step 2: Remove package dependency from package manager config
|   |-- Step 3: Update import paths (submodule path may differ from node_modules/)
|   |-- Step 4: Major CI rework: submodule checkout + cache strategy
|   |-- Caveat: this is almost always wrong. Package registries are the mature solution.

## Best Practices

1. **Configure `branch = main` in `.gitmodules` for tracking submodules.** Without explicit branch configuration, `git submodule update` pins to a specific SHA and lands you in detached HEAD — the #1 source of submodule confusion. Add `git submodule set-branch --branch main <path>` during setup.

2. **Use `git submodule update --init --recursive` in CI, never plain `checkout`.** GitHub Actions `actions/checkout` with `submodules: recursive`, GitLab CI `GIT_SUBMODULE_STRATEGY: recursive`. Without `--recursive`, nested submodules silently fail to initialize.

3. **Cache `.git/modules` by `.gitmodules` hash in CI.** Submodule fetches are serial and slow. Cache the `.git/modules` directory keyed on the SHA of `.gitmodules`. This avoids re-cloning 20+ submodules on every CI run and cuts checkout time from minutes to seconds.

4. **Never force-push to a repo used as a submodule.** A force-push orphans every consumer's pinned SHA. Use `git revert` for mistakes, not `git push --force`. If a rebase is unavoidable, notify all consumer teams, coordinate the SHA migration, and validate all consumers pass CI before merging.

5. **Pin submodules to release tags for stability; track branches only for actively co-developed dependencies.** Tags (`v2.1.0`) give deterministic builds. Branch tracking (`.gitmodules` with `branch = main`) gives auto-updates but non-deterministic builds. Use branch tracking only for shared libraries developed alongside the consumer.

6. **Run `git submodule status --recursive` in pre-commit hooks and CI.** Catch detached HEAD, uninitialized submodules, and SHA mismatches before they reach `main`. The hook should fail on any submodule without a branch or pinned-tag justification documented in `.gitmodules-commentary.md`.

7. **Prefer `git subtree` over submodules for tightly coupled code co-developed daily.** Subtree merges the dependency's history into your repo — no detached HEAD, no serial CI fetches, no separate clone step. The trade-off is a larger repo history. Use subtree when teams modify the shared code every sprint.

8. **Audit submodule health monthly: stale pointers, orphaned SHAs, uninitialized submodules.** Automate a monthly CI job that runs `git submodule foreach 'git cat-file -t HEAD'` and alerts on any "could not get object info" errors. A submodule pointing to a nonexistent SHA is a ticking time bomb.

9. **Prefer absolute HTTPS submodule URLs for public repos; SSH for private repos behind a VPN.** Relative URLs (`url = ../dep.git`) break when developers mix HTTPS and SSH clones. Absolute URLs ensure every developer resolves the same remote regardless of their transport protocol.

10. **Document the submodule update cadence.** For branch-tracking submodules: weekly automated PR (Renovate/Dependabot supports submodules). For tag-pinned submodules: manual update per release cycle. Undocumented cadence leads to 6-month drift and painful catch-up merges.

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
| Monorepo to polyrepo extraction with submodules | monorepo-manager | Coordinate the subdirectory extraction with monorepo restructuring |
| CI/CD pipeline with submodule checkout | ci-cd-builder | Submodule CI config, caching, private submodule authentication |
| Cross-repo refactoring with submodules | cross-repo-refactoring | Comet-style migration across repos connected by submodules |
| Large-scale dependency management | dependency-manager | Coordinate vendoring vs submodule vs package registry decisions |
| Code migration with history preservation | migration-architect | git filter-repo for history rewrites, subtree split for extraction |
| Security patching of vendored dependencies | security-engineer | Monitoring, update cadence, vulnerability response for vendored code |
| Build system dependency on external repos | build-system-design | Bazel git_repository vs submodule integration |

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `cloud-architect` | Infrastructure design, networking, IAM, cost model | Before provisioning infrastructure or designing deployment pipelines |
| `ci-cd-builder` | Pipeline design, build optimization, deployment strategies | Before designing CI/CD workflows |

## Proactive Triggers

| # | Trigger Condition | Auto-Response |
|---|------------------|---------------|
| P1 | `.gitmodules` exists but no CI config includes submodule checkout | [ALERT] Submodules configured but CI does not clone them. CI builds may use stale or missing submodule content. |
| P2 | `git submodule status --recursive` shows any submodule on detached HEAD without documented reason | [WARN] Submodule on detached HEAD. Configure branch tracking or document why this commit is pinned. |
| P3 | Submodule is >100 commits behind its tracking branch | [INFO] Submodule significantly behind upstream. Assess: intentional pinning or neglect? Security-critical deps should not lag. |
| P4 | `vendor/` directory exists with no VENDOR_VERSION or update script | [WARN] Vendored code without version tracking. Cannot determine if security patches are missing. |
| P5 | `.gitmodules` references private repos but CI has no auth token configured | [ALERT] Private submodules will fail in CI without authentication. Configure PAT, deploy key, or GitHub App token. |
| P6 | Submodule path listed in .gitmodules but directory does not exist | [ALERT] Orphaned submodule entry. Run git submodule deinit <path> or restore the submodule. |

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
     "skill": "git-submodules",
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

- [ ] **[GS1]** `.gitmodules` has `branch` configured for all tracking submodules — no submodule is on detached HEAD without documented justification
- [ ] **[GS2]** CI checkout configured with `submodules: recursive` (GitHub Actions) or `GIT_SUBMODULE_STRATEGY: recursive` (GitLab) — every submodule initializes correctly on clean clone
- [ ] **[GS3]** `.git/modules` cached in CI by `.gitmodules` SHA — checkout time < 60 seconds for repos with 5-15 submodules
- [ ] **[GS4]** `git submodule status --recursive` runs in pre-commit hook and CI — catches detached HEAD, uninitialized submodules, SHA mismatches
- [ ] **[GS5]** Monthly submodule reachability audit: `git submodule foreach 'git cat-file -t HEAD'` — zero "could not get object info" errors, orphaned SHAs remediated within 24 hours
- [ ] **[GS6]** Force-push protection enabled on all repo branches (`branch protection: block force pushes`) — no submodule ever points to a nonexistent SHA
- [ ] **[GS7]** Submodule update cadence documented: weekly automated PRs for branch-tracking submodules (Dependabot/Renovate configured), per-release-cycle manual updates for tag-pinned submodules
- [ ] **[GS8]** Submodule URLs use absolute HTTPS (public repos) or SSH (private repos) — no relative URLs that break across transport protocols
- [ ] **[GS9]** Disaster recovery playbook linked in repo README — detached HEAD recovery, merge conflict resolution, missing submodule recovery all documented
- [ ] **[GS10]** Submodule merge conflict resolution guide includes SHA comparison + CHANGELOG diff — prevents blind "ours looks right" resolutions
- [ ] **[GS11]** Submodule add/remove procedure documented: the full `deinit → rm .git/modules → git rm → edit .gitmodules → commit → add` sequence
- [ ] **[GS12]** Vendored dependencies (if any) have `VENDOR_VERSION` file and automated update check — no vendored code > 6 months behind upstream
- [ ] **[GS13]** Subtree workflows (if any) verified: `git log --follow -- path/to/dep` shows correct history, subtree files identical to source
- [ ] **[GS14]** Code sharing strategy decision documented (submodule vs subtree vs package registry) with rationale — re-evaluated annually

## What Good Looks Like

```
Healthy submodule setup (5-15 submodules, CI integrated):

Submodule status:
  $ git submodule status --recursive
  +a1b2c3d lib/auth (v2.1.0)        <- tracking branch, at tag
  +e4f5g6h lib/logging (main)        <- tracking branch, at tip
  +i7j8k9l lib/protocol (v1.5.0)     <- pinned to release tag

CI integration (GitHub Actions):
  checkout with submodules: recursive
  submodule health check: passes (no detached HEAD, no unreachable SHAs)
  cache: .git/modules cached by .gitmodules hash

Team workflow:
  - submodule updates happen via documented PR process
  - submodule health check runs on every PR
  - disaster recovery playbook is linked in repo README
  - submodule update cadence: weekly automated PR for tracking-branch submodules

Disaster readiness:
  - All submodule SHAs are reachable (verified monthly)
  - Team knows the recovery commands for detached HEAD, merge conflicts, deletion
  - CI catches submodule issues before merge, not after deploy
```

## Deliberate Practice

```
Phase 1: Simple submodule
  Create two repos, add one as submodule of the other
  Commit, push, clone fresh — verify submodule initializes correctly
  Goal: Understand the pointer model

Phase 2: Tracking branches
  Configure branch tracking, pin to a tag
  Update parent and verify submodule tracks correctly
  Goal: Know the difference between pinned commit and branch tracking

Phase 3: Disaster recovery drills
  Intentionally create: detached HEAD, merge conflict, missing submodule
  Recover each using the playbook above
  Goal: Muscle memory for common failures

Phase 4: CI integration
  Configure GitHub Actions with submodule checkout, caching, health check
  Push a broken submodule pointer — verify CI catches it
  Goal: CI as enforcement mechanism

Phase 5: Split-filter extraction
  Create a monorepo with 3 subdirectories, extract one with git filter-repo
  Verify history, file structure, tags preserved
  Goal: Understand history preservation mechanics

Phase 6: Subtree bidirectional
  Set up subtree add/pull/push between two repos
  Make changes in both, resolve conflicts
  Goal: Experience the pain firsthand — internalize when NOT to use subtree
```

## Anti-Rationalization — No Excuses

| Rationalization | Reality |
|---|---|
| "We'll just use submodules without formal training — how hard can it be?" | Detached HEAD confusion alone costs $10K-$30K/year in lost engineering time for a 20-person team. Submodules have a counterintuitive mental model that bites every newcomer. |
| "Nobody force-pushes to our submodule repos — we have branch protection." | One missed protection, one force-push, and every consumer repo points to nonexistent commits. Manual recovery across 5+ consumer repos = $25K-$100K per incident in cross-team coordination. |
| "We'll document the submodule workflow in the wiki — engineers will read it." | Nobody reads wiki docs before running `git submodule update`. Tribal knowledge drifts, and every new hire rediscovers the same footguns. $15K-$30K/year in repeated mistakes that documentation alone won't prevent. |
| "Git subtree is too complex — we'll stick with submodules." | Submodules are the wrong tool for tightly coupled code. Merge pain, serial CI fetches, and detached HEAD support overhead cost $20K-$50K/year compared to subtree or monorepo tooling for the same use case. |
| "We'll automate submodule updates in CI — manual coordination is just temporary." | Temporary becomes permanent. Without CI-enforced submodule sync, 20+ repos diverge within weeks. $15K-$40K/year in CI time from serial `--recursive` clones plus $10K-$30K in integration failures from stale submodule pins. |

## Anti-Patterns

### Anti-Pattern: Accepting Detached HEAD as Normal
**What it looks like:** Teams see "detached HEAD" after `git submodule update` and either panic or ignore it. They make changes in detached HEAD state, then lose work when switching branches.
**Why it fails:** Git submodules pin to a SHA by default. Without `branch = main` in `.gitmodules`, every update returns to detached HEAD. Teams waste $10K-$30K/year in a 20-person org debugging "mysterious" states.
**Do this instead:** Run `git submodule set-branch --branch main <path>` during setup. Document which submodules should track branches vs. pin to tags. Add a pre-commit hook that warns on detached HEAD submodules without documented justification.

### Anti-Pattern: Force-Pushing to Submodule Repos
**What it looks like:** Developer rebases a feature branch in the submodule repo and force-pushes. Five consumer repos now point to nonexistent SHAs.
**Why it fails:** Every consumer's pinned commit is orphaned. Recovery requires manual SHA mapping across all consumers — an error-prone process costing $25K-$100K per incident.
**Do this instead:** Enable branch protection with "block force pushes" on all submodule repo branches. Use `git revert` for mistakes. If rebase is unavoidable, notify all consumer teams, coordinate SHA migration, and validate all consumers pass CI before merging.

### Anti-Pattern: Serial Submodule Updates Without Caching
**What it looks like:** CI clones 30 submodules one at a time with `git submodule update --init --recursive`. Each takes 5 seconds = 2.5 minutes of serial I/O on every CI run.
**Why it fails:** Git has no built-in parallelism for submodule updates. At scale, this costs $15K-$40K/year in wasted CI time for repos with 20+ submodules.
**Do this instead:** Cache `.git/modules` by `.gitmodules` hash in CI. Use `git submodule update --init --recursive --jobs 8` for parallel fetches (Git 2.8+). Consider subtree for repos with >15 submodules.

### Anti-Pattern: Guessing Submodule Merge Conflicts
**What it looks like:** Two branches update the same submodule to different SHAs. The developer sees two commit hashes and picks "ours" because it looks right.
**Why it fails:** The "right" SHA might revert a security patch or break a shared interface. This is the #1 cause of post-merge submodule bugs, costing $20K-$50K/year in production incidents.
**Do this instead:** Always run `git log --oneline <ours-sha>..<theirs-sha>` to see what commits you'd lose/gain. Check CHANGELOGs between the two SHAs. Prioritize the SHA containing security patches. Document the resolution in a merge resolution log.

### Anti-Pattern: Vendored Code Without Update Tracking
**What it looks like:** Team vendors a dependency, commits it to the repo, and never checks upstream again. Six months later, the vendored copy is 3 major versions behind.
**Why it fails:** Unpatched CVEs in vendored code ship to production because no scanning tool looks at vendored dependencies. $50K-$500K+ per security incident.
**Do this instead:** Add a `VENDOR_VERSION` file tracking the upstream version. Schedule automated monthly checks against upstream. Use Renovate/Dependabot with submodule support for tracking-branch submodules.

### Anti-Pattern: Relative Submodule URLs in Mixed-Protocol Teams
**What it looks like:** `.gitmodules` uses `url = ../dependency.git`. Alice clones via HTTPS, Bob via SSH. Alice gets HTTPS URLs, Bob gets SSH URLs — but only one works behind the VPN.
**Why it fails:** Resolved URLs differ by protocol, causing "repository not found" errors that are environment-specific and nearly impossible to reproduce. $5K-$15K in debugging per incident.
**Do this instead:** Use absolute URLs: HTTPS for public repos, SSH for private repos behind VPN. Use `insteadOf` in `.gitconfig` to redirect protocols consistently across the team.

### Anti-Pattern: Incomplete Submodule Removal Sequence
**What it looks like:** Developer runs `git submodule deinit <path>` then `git submodule add <url> <path>` — expecting a clean re-add. Gets confusing errors about an existing repository.
**Why it fails:** `.git/modules/<path>` retains stale config after deinit. Without manual cleanup, the re-add fails. $8K-$20K per developer who attempts self-service recovery and corrupts repo state.
**Do this instead:** Full removal sequence: `git submodule deinit -f <path> && rm -rf .git/modules/<path> && git rm -f <path>`, then edit `.gitmodules` to remove entry, commit, THEN `git submodule add <url> <path>`.

## Verification

After setting up or modifying submodule/subtree configuration, run this sequence. Do not proceed past a failure.

1. **Submodule initialization:** `git submodule update --init --recursive` completes without errors. All submodule directories contain expected files.
2. **Detached HEAD audit:** `git submodule foreach 'git status | head -1'` shows branch names (not "detached") for all tracking submodules, or pinned SHAs with documented justification.
3. **Reachability check:** `git submodule foreach 'git cat-file -t HEAD'` returns "commit" for every submodule. No "fatal: git cat-file: could not get object info" errors.
4. **CI checkout verification:** CI config contains submodule checkout directive. Run a clean CI build — submodules initialize correctly.
5. **Subtree verification:** If using subtree: `git log --follow -- path/to/dep` shows correct history. Subtree files are identical to source of truth.
6. **Vendoring audit:** If vendoring: VENDOR_VERSION file exists, update script runs successfully, diff against upstream produces expected output.
7. **Disaster recovery readiness:** Team can execute the top 3 recovery procedures (detached HEAD, merge conflict, missing submodule) without reference.

If any check fails: diagnose from verification item, provide specific actionable fix, restart verification from failed item.

## Verification Guardrails

Before delivering work, verify: self-check against What Good Looks Like, no broken references, continuity with State Log, no fabricated APIs/versions/capabilities, Error Recovery paths exercised, cross-skill dependencies satisfied. If any fail, revise before delivering.

## References

* [Git Submodules Documentation](https://git-scm.com/book/en/v2/Git-Tools-Submodules) — Official Git documentation for submodules
* [Git Subtree Documentation](https://github.com/git/git/blob/master/contrib/subtree/git-subtree.txt) — Official git-subtree documentation
* [git-filter-repo](https://github.com/newren/git-filter-repo) — Recommended tool for history rewriting (replaces filter-branch)
* [/references/decision-matrix.md](references/decision-matrix.md) — Submodule vs subtree vs package registry vs vendoring comparison
* [/references/submodule-lifecycle.md](references/submodule-lifecycle.md) — Full submodule lifecycle: add, update, deinit, recursive operations
* [/references/submodule-ci.md](references/submodule-ci.md) — CI/CD configuration for GitHub Actions, GitLab CI, Jenkins
* [/references/subtree-workflows.md](references/subtree-workflows.md) — git subtree add/pull/push/split patterns and gotchas
* [/references/split-filter-extraction.md](references/split-filter-extraction.md) — git filter-repo extraction playbook with history preservation
* [/references/vendoring-strategies.md](references/vendoring-strategies.md) — When to vendor, maintenance strategies, update automation
* [/references/disaster-recovery.md](references/disaster-recovery.md) — Common failures, recovery procedures, prevention checklist
* [/references/alternative-tools.md](references/alternative-tools.md) — git-subrepo, gitslave, repo tool, myrepos comparison
