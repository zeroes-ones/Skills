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

### Auto-Route by Artifacts (Check Filesystem First)

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_exists(".gitmodules")` AND `file_contains(".gitmodules", "[submodule")` | Active submodules -> Go to **Core Workflow: Phase 1 — Submodule Health Audit** |
| A2 | `file_contains(".gitmodules", "submodule.*url.*=")` AND submodule dir has uncommitted changes | Dirty submodule -> Jump to **Decision Trees: Disaster Recovery** |
| A3 | `file_exists(".gitmodules")` with entries for directories that no longer exist | Orphaned submodule entries -> Jump to **Decision Trees: Submodule Cleanup** |
| A4 | `grep -r "git subtree" Makefile CMakeLists.txt package.json scripts/` | Subtree workflow detected -> Go to **Core Workflow: Phase 3 — Subtree Audit** |
| A5 | `file_exists("vendor/")` OR `file_exists("third_party/")` with >10 directories | Vendoring pattern -> Jump to **Decision Trees: Vendoring Assessment** |
| A6 | User mentions "extract" + "subdirectory" + "history" | Split-filter needed -> Go to **Core Workflow: Phase 2 — Split-Filter Extraction** |
| A7 | No submodule/subtree/vendor files | New cross-repo sharing decision -> Jump to **Decision Trees: Code Sharing Strategy** |

### Intent Route (Ask the User)

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

## Core Workflow

### Phase 1: Submodule Health Audit

Execute in order. Do not skip steps.

```
1. INVENTORY ALL SUBMODULES
   |-- List all submodules: git submodule status --recursive
   |-- For each submodule, record: path, pinned commit SHA, configured branch, remote URL
   |-- Count: total submodules (warn if >20)
   |-- Check for stale entries: submodules in .gitmodules whose paths do not exist

2. DETACHED HEAD CHECK
   |-- For each submodule: cd <path> && git status | head -1
   |-- If "HEAD detached at": submodule is NOT tracking a branch
   |-- Fix: git config -f ../.gitmodules submodule.<path>.branch main
   |-- Then: git submodule update --remote -- <path>

3. REACHABILITY CHECK
   |-- For each submodule, verify the pinned SHA exists in the remote:
   |   |-- cd <path> && git fetch origin
   |   |-- git cat-file -t <pinned-sha>
   |   |-- If fails: pinned commit has been force-pushed away or repo deleted
   |-- Document all unreachable SHAs — these are ticking time bombs

4. DIVERGENCE CHECK
   |-- Compare pinned SHA with remote branch tip:
   |   |-- cd <path> && git rev-list --count HEAD..origin/main
   |-- If >50 commits behind: submodule is significantly stale
   |-- Assess: is this intentional (known-good version) or neglect?
   |-- Flag: security-sensitive deps (auth libs, crypto) more than 30 days behind

5. CI VERIFICATION
   |-- Check CI config for submodule checkout:
   |   |-- GitHub Actions: actions/checkout@v4 with: submodules: recursive
   |   |-- GitLab CI: GIT_SUBMODULE_STRATEGY: recursive
   |   |-- Jenkins: git clone --recurse-submodules
   |-- Verify: do all CI jobs that touch code have submodule checkout?
```

### Phase 2: Split-Filter Extraction (Monorepo to Polyrepo)

```
1. PREPARE THE EXTRACTION
   |-- Identify the subdirectory to extract: path/to/lib
   |-- Verify the subdirectory has meaningful independent history
   |-- Install git-filter-repo: pip install git-filter-repo
   |-- Clone a fresh copy (never filter in-place): git clone <monorepo> extraction-workdir

2. FILTER THE HISTORY
   |-- Extract only the subdirectory, preserving its internal structure:
   |   |-- cd extraction-workdir
   |   |-- git filter-repo --subdirectory-filter path/to/lib --force
   |-- Verify: git log --oneline | head -20 (should show only commits touching path/to/lib)
   |-- Verify: file structure at root is the lib contents, not path/to/lib/lib/...
   |-- Clean: git reflog expire --expire=now --all && git gc --prune=now --aggressive

3. PUSH TO NEW REPO
   |-- Create empty remote repo (GitHub/GitLab/etc.)
   |-- git remote add origin <new-repo-url>
   |-- git push -u origin --all
   |-- git push -u origin --tags
   |-- Verify: git log in new repo shows correct history, git blame works on key files

4. UPDATE ORIGINAL MONOREPO
   |-- Option A: Replace extracted code with submodule pointer
   |   |-- rm -rf path/to/lib
   |   |-- git submodule add <new-repo-url> path/to/lib
   |-- Option B: Replace with subtree
   |   |-- git subtree add --prefix=path/to/lib <new-repo-url> main --squash
   |-- Option C: Archive (if lib is fully independent, no ongoing changes needed)
```

### Phase 3: Subtree Workflow

```
1. ADDING A SUBTREE (one-time)
   |-- git subtree add --prefix=path/to/dep <remote-url> <branch> --squash
   |-- --squash: condenses entire remote history into one merge commit
   |-- Without --squash: full history imported (use for ongoing bidirectional sharing)

2. PULLING UPDATES (one-way sync)
   |-- git subtree pull --prefix=path/to/dep <remote-url> <branch> --squash
   |-- Resolve merge conflicts if local changes to subtree files exist
   |-- After pull: subtree files are updated in working tree, commit the merge

3. PUSHING CHANGES BACK (bidirectional)
   |-- Make changes in path/to/dep within the parent repo
   |-- Commit those changes
   |-- git subtree push --prefix=path/to/dep <remote-url> <branch>
   |-- WARNING: This rewrites history. Subsequent pulls will conflict.
   |-- Best practice: push immediately after making changes, minimize divergence

4. SPLITTING A SUBTREE (extract to standalone)
   |-- git subtree split --prefix=path/to/dep -b split-branch
   |-- This creates a new branch with only the subtree's history
   |-- Push split-branch to new remote: git push <new-remote> split-branch:main
```

### Phase 4: CI Integration

```
1. GITHUB ACTIONS SUBMODULE SETUP
   |-- Checkout with submodules:
   |   |-- uses: actions/checkout@v4
   |   |   with:
   |   |     submodules: recursive
   |   |     token: ${{ secrets.SUBMODULE_PAT }}  # for private submodules
   |-- Caching submodules:
   |   |-- uses: actions/cache@v4
   |   |   with:
   |   |     path: .git/modules
   |   |     key: submodules-${{ hashFiles('.gitmodules') }}
   |-- Submodule health check job:
   |   |-- git submodule status --recursive
   |   |-- git submodule foreach 'git fetch origin && git status'
   |   |-- Fail CI if any submodule is on detached HEAD (unless intentional)

2. GITLAB CI SUBMODULE SETUP
   |-- variables:
   |     GIT_SUBMODULE_STRATEGY: recursive
   |     GIT_SUBMODULE_DEPTH: 1  # shallow clone submodules for speed
   |-- For private submodules: configure deploy keys or CI job tokens

3. COMMON CI FAILURES AND FIXES
   |-- "fatal: could not read Username": private submodule without auth -> configure PAT/deploy key
   |-- "fatal: reference is not a tree": pinned commit force-pushed -> update submodule pointer
   |-- "error: Server does not allow request for unadvertised object": shallow clone -> set GIT_SUBMODULE_DEPTH: 0
```

## Decision Trees

### Code Sharing Strategy Selection

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

### Disaster Recovery

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

### Vendoring Assessment

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

## Proactive Triggers

| # | Trigger Condition | Auto-Response |
|---|------------------|---------------|
| P1 | `.gitmodules` exists but no CI config includes submodule checkout | [ALERT] Submodules configured but CI does not clone them. CI builds may use stale or missing submodule content. |
| P2 | `git submodule status --recursive` shows any submodule on detached HEAD without documented reason | [WARN] Submodule on detached HEAD. Configure branch tracking or document why this commit is pinned. |
| P3 | Submodule is >100 commits behind its tracking branch | [INFO] Submodule significantly behind upstream. Assess: intentional pinning or neglect? Security-critical deps should not lag. |
| P4 | `vendor/` directory exists with no VENDOR_VERSION or update script | [WARN] Vendored code without version tracking. Cannot determine if security patches are missing. |
| P5 | `.gitmodules` references private repos but CI has no auth token configured | [ALERT] Private submodules will fail in CI without authentication. Configure PAT, deploy key, or GitHub App token. |
| P6 | Submodule path listed in .gitmodules but directory does not exist | [ALERT] Orphaned submodule entry. Run git submodule deinit <path> or restore the submodule. |

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

## Gotchas

* **Submodule detached HEAD is the default, not a bug.** Git submodules pin to a specific commit SHA by design. Without `branch = main` in `.gitmodules`, every `git submodule update` puts you back in detached HEAD. Teams waste hours on this because it looks like an error but is actually expected behavior. **Total cost: $10K-$30K in lost engineering time per year for a 20-person team debugging "mysterious" detached HEAD states.**

* **Force-pushing to a repo used as a submodule destroys every consumer.** If you rebase or force-push to a repo that is a submodule of 5 other repos, all 5 repos now point to commits that do not exist. The fix requires every consumer to find the equivalent commit in the new history — a manual, error-prone process. **Total cost: $25K-$100K per force-push incident across all consumer teams, depending on consumer count and submodule criticality.**

* **`git submodule update --recursive` is secretly sequential.** Git updates submodules one at a time. With 30 submodules, each taking 5 seconds to fetch, that is 2.5 minutes of serial I/O on every clone. There is no built-in parallelism. Teams discover this at scale and have to write custom parallel clone scripts. **Total cost: $15K-$40K/year in wasted CI time for repos with 20+ submodules.**

* **Submodule merge conflicts look like binary gibberish to developers.** When two branches update the same submodule to different SHAs, the merge conflict is a raw SHA comparison. Most developers guess ("ours looks right?"), pick wrong, and ship broken dependencies. This is the #1 cause of post-merge submodule bugs. **Total cost: $20K-$50K/year in production incidents caused by incorrect submodule merge conflict resolution.**

* **Vendored code that is 12 months behind upstream contains known CVEs.** The average vendored dependency without automated update tracking falls 6-18 months behind upstream. During that window, multiple CVEs are disclosed and patched upstream while your vendored copy ships them to production. **Total cost: $50K-$500K+ per security incident depending on data exposure, plus regulatory fines if PII is involved.**

* **`git subtree push` silently drops commits if the split prefix is wrong.** If you specify `--prefix=lib` but the actual directory is `src/lib`, git subtree will split nothing and push an empty branch — overwriting the remote. Recovery requires restoring from the parent repo, which may itself be out of date. **Total cost: $10K-$30K in lost work and recovery effort when a subtree push overwrites the wrong remote branch.**

* **Relative submodule URLs break when the parent repo is cloned via SSH vs HTTPS.** If `.gitmodules` uses `url = ../dependency.git` (relative), and one developer clones via HTTPS while another uses SSH, the resolved URLs differ. This causes "repository not found" errors that are environment-specific and maddeningly hard to reproduce. **Total cost: $5K-$15K in debugging per incident across a team that uses mixed transport protocols.**

* **`git submodule deinit` followed by `git submodule add` does NOT restore the submodule correctly.** The `.git/modules/<path>` directory retains stale config. The correct sequence is: `git submodule deinit -f <path>`, `rm -rf .git/modules/<path>`, `git rm -f <path>`, edit `.gitmodules` to remove entry, commit, THEN `git submodule add <url> <path>`. Missing the `.git/modules` cleanup causes confusing errors about existing repository. **Total cost: $8K-$20K per developer who attempts self-service submodule recovery and corrupts the repo state.**

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
