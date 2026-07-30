---
name: git-workflow
description: >
  Use when designing Git branching strategies, writing commits, managing releases,
  resolving merge conflicts, setting up Git hooks, automating changelogs, or
  establishing versioning conventions. Handles trunk-based development, atomic
  commits, descriptive commit messages (Conventional Commits), git worktrees for
  parallel agent work, semantic versioning (SemVer), changelogs written for humans,
  the Save Point Pattern for incremental commits, merge vs rebase decision
  frameworks, and Git hooks for pre-commit and pre-push quality gates. Do NOT use
  for CI/CD pipeline configuration (route to ci-cd-builder), monorepo tooling
  (route to monorepo-manager), release coordination (route to release-manager), or
  platform engineering (route to platform-engineer).
author: Sandeep Kumar Penchala
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
license: MIT
type: devops
status: stable
version: 1.0.0
updated: 2026-07-23
tags:
  - git
  - version-control
  - trunk-based-development
  - semantic-versioning
  - conventional-commits
  - git-worktrees
  - changelog
  - merge-rebase
token_budget: 4000
chain:
  consumes_from:
    - ci-cd-builder
    - devops-engineer
    - monorepo-manager
  feeds_into:
    - ci-cd-builder
    - release-manager
    - devops-engineer
  alternatives: []
---
# Git Workflow and Versioning

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

End-to-end Git workflow and versioning discipline covering trunk-based development, atomic commits, git worktrees for parallel agent work, semantic versioning, human-readable changelogs, and merge-vs-rebase decision frameworks. Treat every commit as a save point in a game -- commit working slices frequently, never lose progress, always be able to roll back.
<!-- QUICK: 30s -->
## <!-- DEEP: 5+min --> RESEARCH_PREREQUISITE — Execute Before Any Output

**This is a HARD GATE. Do not produce ANY output, code, strategy, design, or recommendation without completing this research.**

Before you act, you MUST execute every applicable research step. Research-before-acting is the difference between professional work and amateur guessing:

| # | Research Step | Why It Matters | Where to Look |
|---|--------------|----------------|----------------|
| **RP1** | **Verify domain currency.** Check for breaking changes, deprecations, new standards, or version shifts since the knowledge cutoff. | [STALE_RISK] Outdated advice breaks real systems. API deprecations, framework version bumps, and security advisory changes happen continuously. Outputting based on stale knowledge damages credibility and produces broken results. | Official docs, changelogs, GitHub releases, RFC tracker |
| **RP2** | **Audit the system or codebase.** Read relevant files. Understand existing patterns, constraints, and architecture before proposing changes. | [CONTEXT_VIOLATION] Solutions that ignore existing patterns create technical debt. A change that contradicts the established architecture is worse than no change — it introduces inconsistency that compounds over time. | Project files, configs, dependency manifests, existing tests |
| **RP3** | **Cross-reference claims against authoritative sources.** Every factual assertion needs a verifiable source. Mark each: [VERIFIED], [COMPUTED], or [ESTIMATED]. | [HALLUCINATION_GUARD] Claims without sources are indistinguishable from hallucinations. The #1 cause of incorrect output is treating assumptions as facts. Source tagging prevents this. | Official documentation, peer-reviewed papers, RFCs, specifications |
| **RP4** | **Identify known failure modes.** Before recommending, list what commonly breaks. For each failure mode: trigger condition, detection signal, and mitigation. | [FAILURE_BLINDNESS] Every domain has known failure patterns. Output that doesn't address them is dangerously incomplete. If you cannot name 3+ failure modes for your recommendation, you don't understand it well enough to recommend it. | Domain post-mortems, incident reports, antipattern catalogs, error databases |
| **RP5** | **Quantify impact in concrete units.** Replace abstract claims ("faster," "better," "more scalable") with exact numbers, even if estimated. | [VAGUENESS_PENALTY] "Faster" is unverifiable. "Reduces p95 latency from 340ms to 120ms (±15ms)" is verifiable. Abstract adjectives hide ignorance behind confidence. Concrete numbers expose gaps. | Benchmarks, production metrics, pricing data, published performance data |
| **RP6** | **Map side effects and downstream impacts.** What else breaks? Which dependencies are affected? Which downstream consumers need updating? | [CASCADE_BLINDNESS] Changes to one component ripple outward. A fix in module A can break module B that depends on A's old behavior. Map the blast radius before acting. | Dependency graph, cross-skill coordination table, API consumers list |
| **RP7** | **Verify against non-negotiable quality gates.** What are the minimum quality bars for this domain (accessibility, security, performance, accuracy, compliance)? | [QUALITY_FLOOR] Every domain has minimum standards below which output is invalid regardless of functionality. Missing WCAG AA = broken. Leaking credentials = broken. Silent data loss = broken. | Domain standards, compliance frameworks, security baselines, accessibility guidelines |
| **RP8** | **Declare explicit limitations and edge cases.** What does this NOT handle? What are the known boundaries? What scenarios are explicitly out of scope? | [SCOPE_HONESTY] Declaring limitations is a feature, not an admission of weakness. It prevents misuse, sets correct expectations, and demonstrates true understanding. Every solution has boundaries — naming them is professional. | This SKILL.md, domain literature, edge case databases |

**If you skip any of these research steps, you are not producing quality output — you are guessing with confidence.** Guessing wastes time, breaks systems, and destroys trust. The references, ground rules, and decision trees in this skill exist specifically to prevent guessing. Use them.

> **Compliance:** Research must be executed before any substantial output. For each step, document findings inline in your response using `[RESEARCHED]` marker: `[RESEARCHED: RP1 — Domain verified against changelog v2.4. No breaking changes since cutoff.]`. Partial research = partial quality. Zero research = zero credibility.



### 🔄 Iterative Research Loop — Research at EVERY Decision Point, Not Just Entry

**The RP1-RP8 cycle above is NOT a one-time gate.** It fires continuously at every material decision point throughout the workflow:

| Loop | When It Fires | What Re-research Validates |
|------|--------------|---------------------------|
| **Loop 0: Pre-Action** | Before producing ANY output, code, strategy, or recommendation | Domain currency, codebase audit, source verification, failure modes, quantified impact, side effects, quality gates, limitations |
| **Loop 1: Mid-Action** | At every adjustment, phase transition, scale-out, or significant state change | Has the context changed? Are the original assumptions still valid? Has new information invalidated the Loop 0 conclusions? |
| **Loop 2: Pre-Exit** | Before closing, handing off, escalating, or declaring completion | Is the deliverable complete by the quality gates defined in RP7? Are all limitations declared (RP8)? Have failure modes been addressed (RP4)? |
| **Loop 3: Post-Action** | After completion: compare expected vs. actual outcome | What was the efficiency ratio (actual / theoretical max)? What learnings emerged? What should be fed back into the pattern database for future decisions? |

**Integration into Core Workflow:**

Every decision point in a skill's Core Workflow must be marked with:
```
[RESEARCH LOOP: Re-execute RP1-RP8 before proceeding to next phase]
```

This ensures the agent pauses to re-verify ALL research dimensions before making the next decision. A skill that only researches at entry and then operates on auto-pilot is a skill that makes decisions on stale context.

**Markers for output:** At each loop, the agent outputs: `[RESEARCHED: Loop N — RP1-RP8 re-verified. Key delta from previous loop: ...]`

**Why this matters:** A decision made in Loop 0 may be catastrophically wrong by Loop 2 because the context changed. Markets move. Requirements shift. Dependencies update. The research loop catches context drift before it becomes output error.

> **Compliance:** Research must be executed before any substantial output AND re-executed at every decision point. For each research loop, document findings inline. Partial research = partial quality. Zero research = zero credibility. Stale research = dangerous confidence.



## Ground Rules — Read Before Anything Else
<!-- STANDARD: 3min -->

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to allow force-push to shared branches. | Trigger: command contains `--force` AND target is `main`, `master`, `develop`, or `release/*` | STOP. "Force-pushing rewrites shared history. Use `--force-with-lease` on feature branches only. Revert shared branches with `git revert`." |
| R2 | DETECT secrets, keys, or tokens in staged changes. Committed secrets are permanently in history. | Trigger: diff matches `AKIA[0-9A-Z]{16}`, `ghp_`, `sk-`, `-----BEGIN.*PRIVATE KEY-----`, or `password\s*=` | STOP. "Secret detected. Remove immediately. If already committed, rotate the secret and purge history with BFG Repo-Cleaner." |
| R3 | REFUSE to commit generated artifacts or large binaries. | Trigger: staged file matches `*.o`, `*.class`, `*.jar`, `node_modules/**`, `dist/**`, `build/**` OR file exceeds 1MB without LFS tracking | STOP. "Generated/binary files bloat the repo permanently. Add to .gitignore and use Git LFS for large files." |
| R4 | DETECT unresolved merge conflict markers. | Trigger: diff contains `<<<<<<<`, `=======`, or `>>>>>>>` | STOP. "Unresolved merge conflicts found. Resolve all conflicts, remove markers, and test before committing." |
| R5 | REFUSE to commit commented-out code without explanation. | Trigger: diff has commented-out function/class/import without adjacent TODO/FIXME within 3 lines | STOP. "Commented-out code rots. Delete it (git history preserves it), feature-flag it, or add a dated TODO." |
| R6 | DETECT empty or non-conventional commit messages. | Trigger: message is empty, equals "fix"/"wip"/"tmp"/"." or does not match Conventional Commits format | STOP. "Use `type(scope): description` format. Description must explain WHY, minimum 10 characters." |
| R7 | REFUSE to merge PR with failing CI. | Trigger: merging PR where CI status is failure, error, or pending | STOP. "CI checks are failing. Fix issues, rebase on latest main, ensure all checks pass, then merge." |
| **R8** | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| **R9** | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |

- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset
<!-- STANDARD: 3min -->

- **Every commit is a save point.** Commit working slices of ~50-150 lines. If the build breaks, bisect finds the exact commit. If you need to revert, you lose minimal work. Commit like you are playing a game with no autosave.
- **The history tells a story.** A git log should read like a narrative of decisions, not a dump of file changes. Each commit message explains WHY the change exists -- the diff shows WHAT changed.
- **Main is always shippable.** Trunk-based development means main/master is always green, always deployable. If main is broken, all work stops. Protect main with branch protection rules, required reviews, and CI gates.
- **Worktrees over stash.** Git stash is a stack of forgotten changes. Git worktrees give you parallel working directories on different branches -- no context switching cost, no lost work, no stash conflicts. Use worktrees when an agent needs to work on multiple branches simultaneously.
- **Bisectability is the ultimate test.** If you cannot `git bisect` to find the exact commit that introduced a bug, your commits are too large or your history is not clean. Every commit should pass tests independently.

## Operating at Different Levels
<!-- STANDARD: 3min -->

- **Quick scan (30s):** Check branch status (`git status`), recent commits (`git log --oneline -10`), verify main is not diverged, check for uncommitted work or dirty worktrees.
- **Standard engagement (10min):** Review PR diff for atomicity, check commit message quality, verify CI status, run pre-commit hooks, squash fixup commits, rebase on main if behind.
- **Deep dive (full session):** Audit full repository history for secrets and large files, restructure commit history for clarity, set up branch protection rules, configure Git hooks, establish versioning and changelog automation.
- **Crisis mode (broken main, bad merge, lost work):** Triage: identify the breaking commit with `git bisect`, revert the breaking change, communicate to team. Use `git reflog` for lost commits. Never force-push to shared branches.

## When to Use
<!-- STANDARD: 3min -->

- Designing a branching strategy for a team or project
- Writing atomic, well-structured commits with descriptive messages
- Managing parallel workstreams with git worktrees
- Setting up Git hooks for pre-commit linting, testing, and secret scanning
- Automating semantic versioning and changelog generation
- Deciding between merge and rebase for integrating branches
- Cleaning up commit history before merging (squashing, reordering, splitting)
- Auditing a repository for secrets, large files, or sensitive data in history
- Establishing branch protection rules and required CI checks
- Recovering lost commits or resolving complex merge conflicts

**When NOT to use:** CI/CD pipeline design (ci-cd-builder), monorepo tooling (monorepo-manager), release coordination across teams (release-manager), or platform engineering workflows (platform-engineer).

## Route the Request
<!-- STANDARD: 3min -->

```
What Git task are you working on?
|-- Writing a commit -> Jump to "Core Workflow: Phase 1 - The Atomic Commit"
|-- Branching strategy -> Jump to "Decision Trees: Branching Strategy"
|-- Merge vs rebase decision -> Jump to "Decision Trees: Merge vs Rebase"
|-- Setting up Git hooks -> Go to "Core Workflow: Phase 2 - Quality Gates"
|-- Managing parallel work -> Jump to "Decision Trees: Worktree Strategy"
|-- Versioning and changelogs -> Jump to "Decision Trees: Versioning"
|-- Cleaning up history -> Jump to "Decision Trees: History Rewriting"
|-- Recovering lost work -> Jump to "Decision Trees: Recovery"
```

## Core Workflow **(STANDARD)**
<!-- STANDARD: 3min -->

### Phase 1: The Atomic Commit (Save Point Pattern)

```
1. CHECK CURRENT STATE
   |-- git status: know exactly what changed
   |-- git diff: review changes before staging
   |-- git stash list: any forgotten stashes?

2. STAGE ATOMICALLY
   |-- One logical change per commit (50-150 lines ideal)
   |-- git add -p for partial staging: split large changes into atomic commits
   |-- If fixing a bug AND refactoring: two separate commits
   |-- NEVER git add . blindly -- review every hunk

3. WRITE THE MESSAGE
   |-- Conventional Commits: type(scope): subject
   |   |-- feat: new feature
   |   |-- fix: bug fix
   |   |-- docs: documentation
   |   |-- refactor: code change that neither fixes nor adds
   |   |-- perf: performance improvement
   |   |-- test: adding or fixing tests
   |   |-- build: build system or dependencies
   |   |-- ci: CI configuration
   |   |-- chore: other changes
   |-- Subject: imperative mood, max 72 chars, no period at end
   |-- Body (after blank line): WHAT and WHY, not HOW. Wrap at 72 chars.
   |-- Footer: BREAKING CHANGE: description or Closes #123

4. VERIFY BEFORE COMMITTING
   |-- git diff --cached: review exactly what will be committed
   |-- Run pre-commit hooks manually if not automated
   |-- Build and test locally if possible
   |-- git commit -m "..." (or use editor for multi-line messages)

5. PUSH SAFELY
   |-- git pull --rebase origin main (stay current)
   |-- git push origin feature/branch-name
   |-- NEVER git push --force to shared branches
```

  Complete when: `git diff --cached` shows exactly one logical change with a conventional commit message, pre-commit hooks pass, and `git log -1` shows a well-formed commit with body explaining the WHY.

### Phase 2: Quality Gates (Git Hooks)

```
1. INSTALL HOOKS FRAMEWORK
   |-- Option A: pre-commit framework (Python)
   |   |-- pip install pre-commit
   |   |-- Create .pre-commit-config.yaml
   |   |-- pre-commit install --install-hooks
   |-- Option B: lefthook (Go, fast)
   |   |-- lefthook install
   |   |-- Configure lefthook.yml
   |-- Option C: husky (Node.js)
   |   |-- npx husky install
   |   |-- npx husky add .husky/pre-commit "npm test"

2. PRE-COMMIT CHECKS (run on staged files only)
   |-- Secret scanning: detect-secrets, gitleaks, or truffleHog
   |-- Linting: eslint, ruff, shellcheck, markdownlint
   |-- Formatting: prettier, black, gofmt
   |-- Type checking: tsc --noEmit, mypy
   |-- Unit tests: only run tests related to changed files
   |-- Forbidden patterns: console.log, debugger, .only in tests

3. COMMIT-MSG HOOK
   |-- Enforce Conventional Commits format
   |-- Maximum subject line length (72 chars)
   |-- Require body for large diffs (>200 lines)

4. PRE-PUSH CHECKS
   |-- Full test suite (unit + integration)
   |-- Build verification
   |-- Branch naming convention check
```

  Complete when: `pre-commit run --all-files` passes with zero failures, commit-msg hook enforces conventional commit format, and pre-push hook runs the full test suite successfully.

### Phase 3: Versioning and Changelogs

```
1. DETERMINE VERSION BUMP
   |-- Breaking change -> MAJOR version (1.0.0 -> 2.0.0)
   |-- New feature (backward compatible) -> MINOR (1.0.0 -> 1.1.0)
   |-- Bug fix (backward compatible) -> PATCH (1.0.0 -> 1.0.1)
   |-- Use Conventional Commits to auto-determine bump type

2. GENERATE CHANGELOG
   |-- Keep a Changelog format: https://keepachangelog.com/
   |-- Sections: Added, Changed, Deprecated, Removed, Fixed, Security
   |-- Write for humans, not machines: explain impact, not just commit titles
   |-- Link to relevant issues/PRs

3. TAG THE RELEASE
   |-- git tag -a v1.2.0 -m "Release v1.2.0: Add dark mode support"
   |-- Annotated tags (git tag -a) include author, date, message
   |-- Push tags: git push origin v1.2.0 or git push --tags
```

  Complete when: version bump type is determined from commit history, changelog follows Keep a Changelog format with human-readable impact descriptions, and an annotated tag is pushed to the remote.
  Complete when: Pipeline runs end-to-end in under 15 minutes with parallelized stages.
  Complete when: Rollback tested — can revert to previous version within 5 minutes of detection.
  Complete when: Secrets scan runs in CI and blocks merge on any detected credential.
  Complete when: Infrastructure drift detection enabled — Terraform plan shows zero unmanaged changes.
  Complete when: Runbook documented and tested via game day exercise with < 3 action items.

## Decision Trees **(QUICK)**
<!-- STANDARD: 3min -->

### Branching Strategy

```
What type of project?
|-- Solo/small team (1-5 developers) -> Trunk-Based Development
|   |-- All work on short-lived feature branches (<2 days)
|   |-- Merge to main multiple times per day
|   |-- Feature flags for incomplete work
|   |-- CI runs on every push to main
|-- Medium team (5-50) -> GitHub Flow
|   |-- Feature branches from main
|   |-- PR with required review + CI pass
|   |-- Squash merge or rebase merge to main
|   |-- Deploy from main after merge
|-- Large team/OSS -> GitFlow (only if release cadence is slow)
|   |-- main: production releases only
|   |-- develop: integration branch
|   |-- feature/*: new work
|   |-- release/*: release preparation
|   |-- hotfix/*: emergency production fixes
|   |-- WARNING: GitFlow adds complexity. Use only if you have scheduled releases with freeze periods.
|-- Monorepo -> Trunk-based with branch protection
|   |-- All teams commit to main
|   |-- CI validates affected projects only
|   |-- Release branches cut from main for deployment
```

### Merge vs Rebase

```
Context: integrating feature branch into main
|-- Feature branch is PRIVATE (only you work on it)
|   |-- Use REBASE: git rebase main && git push --force-with-lease
|   |-- Creates linear history, cleaner than merge commits
|   |-- Each commit must still pass tests (rebase runs hooks per commit)
|-- Feature branch is SHARED (others depend on it)
|   |-- Use MERGE: git merge main (creates merge commit)
|   |-- Preserves history exactly, avoids force-push coordination nightmare
|   |-- Merge commits document when integration happened
|-- Pull request squash-merging
|   |-- Squash all commits into one clean commit
|   |-- Best for: feature branches with many "wip"/"fix typo" commits
|   |-- Loses: granular history within the feature
|   |-- Preserves: clean main branch history
|-- Pull request rebase-merging
|   |-- Rebase feature commits onto main tip, then fast-forward merge
|   |-- Best for: well-structured feature branches with meaningful individual commits
|   |-- Preserves: granular commit history
|   |-- Requires: each commit to be atomic and well-described
```

### Worktree Strategy

```
When to use git worktree:
|-- Hotfix while deep in feature work
|   |-- git worktree add ../hotfix-branch hotfix/critical-fix
|   |-- Work on hotfix in separate directory
|   |-- No need to stash, commit WIP, or switch branches
|-- Code review while developing
|   |-- git worktree add ../review-pr-123 main
|   |-- git fetch origin pull/123/head:pr-123
|   |-- Review in separate directory without disturbing current work
|-- Parallel agent work
|   |-- Each agent gets its own worktree
|   |-- No branch switching conflicts
|   |-- Clear isolation: agent A works in ~/worktrees/feature-a, agent B in ~/worktrees/feature-b
|-- Testing against different dependency versions
|   |-- git worktree add ../test-old-deps old-release-tag
|   |-- Run tests in parallel without environment pollution
```

### History Rewriting

```
What needs fixing?
|-- Bad commit message on last commit -> git commit --amend
|   |-- Only if NOT pushed to shared branch
|   |-- git commit --amend -m "new message"
|-- Forgot to include a file in last commit
|   |-- git add forgotten-file
|   |-- git commit --amend --no-edit
|-- Need to reorder/squash/split last N commits
|   |-- git rebase -i HEAD~N
|   |-- Interactive rebase opens editor:
|   |   |-- pick = use commit
|   |   |-- reword = change message
|   |   |-- squash = combine with previous
|   |   |-- fixup = combine, discard message
|   |   |-- drop = remove commit
|   |   |-- edit = stop for amending
|-- Need to remove a file from entire history (secret leak)
|   |-- git filter-branch --index-filter "git rm --cached --ignore-unmatch secret.key" HEAD
|   |-- Or use BFG Repo-Cleaner: bfg --delete-files secret.key
|   |-- Coordinate with all contributors: they must re-clone
|-- Need to split a commit into multiple
|   |-- git rebase -i HEAD~N, mark commit as "edit"
|   |-- git reset HEAD^ (unstages but keeps changes)
|   |-- Stage and commit in smaller chunks
|   |-- git rebase --continue
```

### Recovery

```
What did you lose?
|-- Lost commits (deleted branch, reset too far) -> git reflog
|   |-- git reflog: shows all HEAD movements for last 90 days
|   |-- Find the lost commit hash
|   |-- git checkout -b recovered-branch <hash>
|-- Accidentally committed to wrong branch
|   |-- git reset HEAD~1 --soft (undo commit, keep changes staged)
|   |-- git stash (or switch branches and apply)
|   |-- Switch to correct branch, apply changes, commit
|-- Discarded uncommitted changes
|   |-- IDE local history (VSCode, IntelliJ keep their own undo)
|   |-- git fsck --lost-found (may recover dangling blobs, unlikely for uncommitted)
|   |-- Prevention: commit early, commit often. "Save Point Pattern"
|-- Merge conflict nightmare
|   |-- git merge --abort (cancel merge, return to pre-merge state)
|   |-- Retry with smaller chunks: rebase instead of merge
|   |-- git mergetool: use visual diff tool (meld, kdiff3, vscode)
|-- Detached HEAD state
|   |-- git checkout -b new-branch-name (create branch at current position)
|   |-- Or: git switch -c new-branch-name
```

## Gotchas
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

| Gotcha | Cost | Fix |
|--------|------|-----|
| `git push --force` on a shared branch — overwrites teammates' commits that were pushed after your last fetch; their work is lost and unrecoverable unless they have a local copy | $10K-$50K in lost engineering work and team trust | Never `--force` to shared branches; use `--force-with-lease` which checks that your local ref matches the remote before overwriting; configure branch protection to reject force pushes on `main` and release branches |
| `git add .` without reviewing — commits secrets, large binaries, debug logs, and temporary files into the repository history where they live forever | $5K-$30K in secret rotation, repo size bloat, and `.gitignore` cleanup | Always use `git add -p` for interactive staging; maintain a comprehensive `.gitignore`; run `git diff --cached` before every commit; use pre-commit hooks to block secrets and large files |
| Rebasing a shared branch — rewriting history that others have based work on; every teammate's local branch now diverges and requires force-push recovery | $20K-$100K in team-wide git recovery and merge conflict resolution | Only rebase private branches that nobody else depends on; once a branch is pushed and shared, use merge commits instead; communicate branch state changes to the team |
| Squash-merging without preserving the PR description — the squash commit has a generic "Fix bug" message and the design rationale from the PR body is lost | $5K-$20K in lost context when debugging 6 months later | Configure squash-merge to use PR title + body as the commit message; every commit on `main` should be self-contained with the WHY in the body; link back to the PR for full discussion history |

## Error Decoder — War Stories from the Trenches
<!-- STANDARD: 3min -->

**(STANDARD)**

When this domain goes wrong, it goes wrong in predictable ways. Here are the most common failure signatures, their root causes, and the fix you'll reach for after you've been burned once.

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| `git push --force` to a shared branch overwrites 3 days of teammate commits — force push was enabled on the branch protection rule | The branch protection rule required linear history but didn't have "Restrict force pushes" enabled. A developer resolved a rebase incorrectly, force-pushed their local (which was 3 days behind origin), and wiped 14 commits. GitHub has the original commits in the reflog but only for 30 days | Immediately: `git push -f origin <last-known-good-SHA>:<branch>` to restore from reflog. Prevent: enable "Restrict force pushes" on all shared branches. Set branch protection to require PRs and dismiss stale reviews on new commits. Add a `pre-push` hook that warns on `--force` to shared branches | Force-push to shared branches is a loaded gun with no safety. Branch protection's "require linear history" doesn't prevent force push — it only enforces that the resulting history is linear. "Restrict force pushes" is a separate toggle. Enable both. |
| `git rebase main` produces 40 conflicts across 15 files — the branch was behind `main` by 200 commits after 3 weeks | The branch diverged slowly. Each day behind main adds 7-15 new commits. After 3 weeks, 200 commits touch 80% of the same files in the feature branch. Git's 3-way merge sees changes in both branches and flags every hunk as a conflict | Rebase daily, not weekly. Set CI to flag branches > 5 commits behind main. For already-diverged branches: `git rebase --onto main <first-commit-hash>~1 feature` to rebase only the feature commits. Use `git range-diff` to verify that the rebased commits have the same diff as the originals | Merge debt compounds exponentially. A branch 1 day behind main might have 0 conflicts. 3 weeks behind: 47 conflicts. The cost of rebasing is linear if you do it daily; exponential if you batch it. CI enforcement is cheaper than manual discipline. |
| Conventional Commits linter blocks every PR after someone changes the config — "type 'chore' is not allowed" but the repo has 300 existing `chore:` commits | The commitlint config was copied from another repo that only allows `feat, fix, docs, ci`. This repo's convention uses `chore, refactor, test, perf` as well. The CI check runs on PRs but validates ALL commits in the PR — including the most recent one that uses a now-disallowed type | Audit commit history: `git log --oneline --format="%s" | sed 's/:.*//' | sort | uniq -c` to see what types are actually used. Configure commitlint with the union of historical types. Add `ignores: [(commit) => commit.startsWith('Merge')]` to skip merge commits. Run the linter on the PR title only, not every commit | CI linting must match the repo's actual conventions, not an imported config. Historical commits are the ground truth — if 300 commits use `chore:`, the linter must accept `chore:`. Otherwise, CI becomes a gate that blocks work, not a guard that improves quality. |
| `git worktree` creates a new branch but `git push` fails with `fatal: The current branch has no upstream branch` — CI can't find the branch | Worktrees create local branches without setting upstream tracking. The developer commits, pushes manually, but CI triggers only on branch creation events. The branch exists locally but GitHub has no record until the first push — and `git worktree add` doesn't auto-push | Add `git push --set-upstream origin <branch>` after worktree creation. Configure `push.autoSetupRemote = true` in `~/.gitconfig`. Use `gh pr create --head <branch>` to create the PR and the remote branch in one command | Worktrees decouple branch creation from remote existence. The branch exists locally but only locally — CI can't run on it. Always push immediately after creating a worktree branch. |
| `git commit --amend` on a pushed commit causes a divergent branch — the next `git pull` produces a merge commit that undoes the amendment | The developer amended a commit that was already pushed (damn). Then they ran `git pull` which fetched the original commit from origin and merged it back into the amended history. The result: a merge commit that re-adds the old version alongside the amended version | Use `git commit --amend` only on unpushed commits. If already pushed: `git push --force-with-lease` (but communicate to all branch collaborators first). Enable branch protection "Require linear history" to prevent merge commits from re-introducing old history. Add a `pre-push` hook: `git log origin/<branch>..HEAD --oneline | wc -l` — if 0, warn on amend | Amending pushed commits creates a history fork. The next pull merges both versions together. The only safe amend is an unpushed amend. After push, use `--force-with-lease` (with coordination) or accept the original commit and add a new one. |
| Git hooks defined in `.git/hooks/` work on developer's machine but not on any other developer's machine — the `.git/hooks/` directory isn't versioned | Someone manually copied a `pre-commit` hook into `.git/hooks/` and it worked for them. But `.git/hooks/` is local to the clone — it's not tracked in Git. Every other developer and CI runner lacks the hook | Use a hooks manager: `pre-commit` (Python framework), `husky` (Node.js), or `lefthook` (cross-language). Configure hooks in a versioned file (`.pre-commit-config.yaml`, `.husky/pre-commit`, `lefthook.yml`). CI must run the SAME hooks as pre-commit to prevent mismatches | `.git/hooks/` is a local directory. Hooks placed there are invisible to version control and unreproducible. Always use a hooks manager that stores configuration in the repo and installs hooks via `pre-commit install` or `husky install`. |

## Best Practices
<!-- STANDARD: 3min -->

1. **Trunk-based development with short-lived feature branches.** Branch from `main`, merge back within 1-3 days. Branches older than 5 days accumulate merge debt exponentially — a 3-week-old branch behind 200 commits generates 47 conflicts across 15 files. CI enforces: flag branches >5 commits behind main.

2. **PR review workflow: small, focused, reviewed within 4 business hours.** PRs should be 200-400 lines (one logical change). Require ≥1 approval before merge. Stale reviews (>24 hours) trigger auto-reassignment. CODEOWNERS enforces domain expertise on critical paths. The review is about correctness and design intent — formatting and linting belong in pre-commit hooks.

3. **Rebase for feature branches, merge for release branches, never squash blindly.** `git pull --rebase` keeps feature branch history linear and bisectable. `git merge --no-ff` for release branches preserves the merge commit as a release marker. Squash-merge only when individual commits are not independently meaningful — squashing a well-structured 15-commit feature destroys bisect granularity.

4. **Conventional Commits enforced at the commit-msg hook level.** `type(scope): description` with type ∈ {feat, fix, docs, refactor, perf, test, build, ci, chore}. Subject line ≤72 chars, imperative mood, no period at end. Body after blank line: WHAT and WHY, not HOW. BREAKING CHANGE footer triggers MAJOR version bump. CI rejects commits that violate the format.

5. **Monorepo: CODEOWNERS, sparse checkout, and affected-project detection.** In monorepos, `git add .` from root is catastrophic — it stages other teams' changes. Use `git add -p` or path-specific staging. CI must detect which projects changed and only build/test those. Polyrepo: enforce consistent conventions across repos with shared pre-commit configs and commit message templates.

6. **Protected branches: require PR reviews, status checks, and linear history.** Enable on `main`, `master`, `develop`, `release/*`: require ≥1 approving review, dismiss stale reviews on new commits, require status checks (CI, lint, test), require branches to be up-to-date before merging, disallow force pushes. These 5 protections prevent 90% of git disasters.

7. **Pre-commit hooks catch problems before they reach the PR.** Secret scanning (gitleaks, detect-secrets) blocks accidental credential commits. Linting and formatting (eslint, ruff, prettier) enforce style consistently. Forbidden patterns check (`console.log`, `debugger`, `.only` in tests) prevent development artifacts from shipping. Run on staged files only — full-repo scans belong in CI, not in the commit path.

8. **Sign commits with GPG or SSH keys — verified commits are the supply chain baseline.** Configure `git config --global commit.gpgsign true`. GitHub displays "Verified" badge on signed commits. Unsigned commits cannot be proven authentic — they could come from anyone with commit access. For SLSA Level 2+ compliance, commit signing is mandatory.

9. **Annotated tags (`git tag -a`) for releases, never lightweight tags.** Annotated tags include: tagger identity, timestamp, message (release notes). When debugging a production issue, `git tag -l -n1 v1.2.0` shows who created the tag, when, and what it contains. Lightweight tags are just a pointer — they answer none of these questions. Sign tags with GPG for supply chain integrity.

10. **Git worktrees for parallel work — never stash, never context-switch.** `git worktree add ../feature-branch feature/branch` creates a parallel working directory. Work on a feature in one worktree, fix a critical bug on `main` in another, review a PR in a third. No stashing, no WIP commits, no lost context. Clean up stale worktrees with `git worktree prune` weekly.

## Error Recovery **(STANDARD)**
<!-- STANDARD: 3min -->

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
<!-- STANDARD: 3min -->

| Scenario | Coordinate With | Why |
|----------|----------------|-----|
| CI/CD pipeline that runs on commits | ci-cd-builder | Hook configuration must align with pipeline stages |
| Monorepo with multiple teams committing | monorepo-manager | Branch protection, CODEOWNERS, affected-project detection |
| Release process with changelogs and versioning | release-manager | SemVer bump decisions, release notes, tag conventions |
| Commit signing and supply chain security | security-engineer | GPG signing, commit verification, SLSA provenance |
| Pre-commit testing strategy | qa-engineer | Which tests run pre-commit vs pre-push vs CI |
| Documentation versioning alongside code | documentation-engineer | Versioned docs, changelog integration |
| Incident: need to bisect and revert | incident-responder | Finding the breaking commit, safe revert strategy |

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `cloud-architect` | Infrastructure design, networking, IAM, cost model | Before provisioning infrastructure or designing deployment pipelines |
| `ci-cd-builder` | Pipeline design, build optimization, deployment strategies | Before designing CI/CD workflows |

## Proactive Triggers
<!-- STANDARD: 3min -->

| # | Trigger Condition | Auto-Response |
|---|------------------|---------------|
| P1 | `git status` shows >50 modified files without commits in last 2 hours | [WARN] Large uncommitted change set. Break into atomic commits with `git add -p`. |
| P2 | Branch has diverged from main by >20 commits | [WARN] Branch is stale. Rebase on main to avoid complex merge conflicts later. |
| P3 | `git stash list` shows >3 stashes older than 7 days | [ALERT] Stashes are rotting. Pop or apply each stash, commit or discard. |
| P4 | Repository has no `.gitignore` or missing common patterns | [ALERT] Risk of committing generated files and secrets. Add .gitignore with OS, editor, and language-specific patterns. |
| P5 | No Git hooks configured in repository | [INFO] Consider setting up pre-commit hooks for linting, secret scanning, and commit message validation. |
| P6 | `git log --oneline` shows consecutive commits with same message | [WARN] Duplicate commit messages suggest fixup/squash opportunity before merging. |

## State Log
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.
## Production Checklist **(STANDARD)**
<!-- STANDARD: 3min -->

- [ ] **[GIT1]** Branch protection rules enabled on `main`, `master`, `develop`, `release/*`: require PR reviews, dismiss stale reviews, require status checks, require branches up-to-date, disallow force pushes
- [ ] **[GIT2]** Required PR reviews: ≥1 approving review before merge, CODEOWNERS enforcing domain expertise on critical paths (auth, payments, infrastructure)
- [ ] **[GIT3]** CI status checks required before merge: all tests pass, linting passes, build succeeds, no security vulnerabilities
- [ ] **[GIT4]** Pre-commit hooks configured via `pre-commit`, `lefthook`, or `husky`: secret scanning, linting, formatting, forbidden pattern detection on staged files
- [ ] **[GIT5]** Commit message convention enforced at commit-msg hook level: Conventional Commits format, subject ≤72 chars, imperative mood, body required for diffs >200 lines
- [ ] **[GIT6]** Signed commits required: GPG or SSH key signing configured, GitHub displays "Verified" badge — unsigned commits blocked from protected branches
- [ ] **[GIT7]** `.gitignore` maintained with OS, editor, language-specific, and framework-specific patterns — no `node_modules`, `dist`, `build`, `.env` in history
- [ ] **[GIT8]** Git LFS configured for files >1MB: tracked patterns cover binaries, assets, datasets — CI validates LFS is tracking new large files
- [ ] **[GIT9]** Stale branch cleanup: branches >14 days without activity flagged and archived, merged branches deleted automatically by CI
- [ ] **[GIT10]** Annotated tags required for releases: `git tag -a v1.2.0 -m "Release notes"`, signed with GPG — lightweight tags blocked from release pipeline
- [ ] **[GIT11]** Merge strategy documented and enforced: rebase for feature branches (linear history), `--no-ff` for release branches (preserve merge markers), squash only for trivial/unstructured branches
- [ ] **[GIT12]** Trunk-based development: feature branches merged within 1-3 days, CI flags branches >5 commits behind main and >10 days old
- [ ] **[GIT13]** Secret scanning in CI and pre-commit: gitleaks or detect-secrets runs on every push, blocks commits containing secrets — if committed, rotate immediately and purge history with BFG

## What Good Looks Like
<!-- STANDARD: 3min -->

```
FEATURE: Add two-factor authentication

Commit history (git log --oneline):
  a1b2c3d feat(auth): add TOTP secret generation and QR code endpoint
  e4f5g6h feat(auth): implement TOTP verification with rate limiting
  i7j8k9l feat(auth): add backup recovery codes with one-way hash storage
  m0n1o2p docs(auth): document 2FA setup and recovery flow
  q3r4s5t test(auth): add integration tests for full 2FA enrollment flow

Bad alternative (anti-pattern):
  x1y2z3w wip
  a4b5c6d more wip
  d7e8f9g add 2fa, fix typo, update docs, refactor auth, fix tests
```

## Deliberate Practice
<!-- STANDARD: 3min -->

1. **The 10-Commit Challenge:** Take a feature you built in one large commit. Rebuild it as 5-10 atomic commits where each commit message tells a clear story. Verify each commit passes tests independently using `git rebase -i --exec "npm test"`.

2. **Worktree Parallelism:** Set up 3 git worktrees on the same repository. In worktree A, develop a feature. In worktree B, fix a critical bug on main. In worktree C, review a teammate's PR. Switch between them without stashing or committing WIP.

3. **Bisect Drill:** Have a colleague introduce a bug in one of 20 commits without telling you which one. Use `git bisect` to find it in under 5 steps. Time yourself. Master `git bisect run` for automated bisection.

4. **History Rewrite:** Create a branch with 15 messy commits (wip messages, mixed concerns, one commit that adds a secret file). Use interactive rebase to produce 5 clean atomic commits with proper messages, and use BFG to remove the secret from history.

5. **Merge Conflict Gauntlet:** Have two branches make conflicting changes to the same 5 files (different refactors, renamed functions, moved files). Merge them without losing any work. Practice with `git mergetool` and understand when to accept theirs vs ours vs manually resolve.

## Anti-Hallucination
<!-- STANDARD: 3min -->

| Rationalization | Reality |
|---|---|
| "Branch protection is for large teams — we're only 5 engineers." | One force-push to main overwrites teammates' merged PRs. Recovery takes 2 hours across 4 engineers = $1,500-$3,000 per incident. Branch protection takes 5 minutes to enable and prevents this forever. |
| "We'll clean up the git history later — just ship the messy commits." | Dirty history accumulates exponentially. Future `git bisect` sessions take 4x longer navigating "wip" and "fix typo" commits. $10K-$30K/year in wasted debugging time across the team. Squash-merge is free. |
| "Secrets in the repo? We'll rotate the keys next sprint." | Bots scan every public commit within 5 minutes. If the repo is public or becomes public later, that AWS key funds $50K in crypto mining before you notice. Rotate on detection — every minute matters. |
| "Everyone knows not to commit node_modules or .env files." | One `git add .` without a proper .gitignore = 200MB of permanent repo bloat. Every clone from that point downloads those 200MB forever. For a team of 20 with CI runners, that's 4GB/day of wasted bandwidth. $2K-$5K/year. |
| "We don't need a documented merge strategy — just merge when ready." | Undefined workflow = 2-3 hrs/week per engineer in merge confusion, rebase-vs-merge debates, and accidental overwrites. $15K-$30K/year in friction that a one-page merge strategy doc eliminates. |

## Anti-Patterns
<!-- STANDARD: 3min -->

- **Force-pushing to main destroys the team's afternoon.** An engineer force-pushes a rebased main, overwriting 3 teammates' merged PRs. The reflog saves the commits, but coordination to re-apply takes 2 hours across 4 engineers. **Total cost: $1,500-$3,000 in lost productivity per incident.** Fix: Enable branch protection with force-push disabled on shared branches.

- **Committing node_modules bloats the repo forever.** A developer runs `git add .` without a .gitignore, commits 200MB of node_modules. Every clone from that point forward downloads those 200MB -- even after the files are removed from HEAD, they remain in history. For a team of 20 with CI runners, that is 4GB of wasted transfer per day. **Total cost: $500-$2,000/year in storage, bandwidth, and slower CI.** Fix: Set up .gitignore before the first commit. Use `git filter-branch` or BFG to purge if already committed.

- **A committed AWS key costs thousands in crypto mining.** A developer accidentally commits an AWS access key to a public GitHub repo. Within 5 minutes, bots scan the commit, extract the key, and spin up $50,000 worth of EC2 instances for cryptocurrency mining before AWS detects the anomaly. **Total cost: $10,000-$50,000 in unauthorized cloud charges.** Fix: Pre-commit secret scanning (gitleaks, detect-secrets). If a secret is committed, rotate it immediately -- revoking the key is the only reliable fix.

- **Squash-merging loses bisect granularity.** A team squashes a 50-commit feature branch into one commit on main. A bug introduced in commit 14 of 50 is now impossible to bisect -- the entire feature is one commit. Debugging time goes from 30 minutes (bisect) to 4 hours (manual code review). **Total cost: $1,000-$3,000 per incident in debugging time.** Fix: Squash only when individual commits are not meaningful. For well-structured features, use rebase-merge.

- **Stale branches accumulate merge debt exponentially.** A feature branch sits unmerged for 3 weeks while main advances by 200 commits. When the developer finally merges, there are 47 conflicts across 15 files. Resolution takes 6 hours instead of the 30 minutes it would have taken if rebased weekly. **Total cost: $1,500-$4,000 per stale branch in merge resolution time.** Fix: Rebase feature branches on main at least every 2-3 days. Set up CI to flag branches >5 commits behind main.

- **Annotated tags vs lightweight tags cause deployment confusion.** A team tags releases with lightweight tags (`git tag v1.2.0`). When debugging a production issue, they cannot determine WHO created the tag, WHEN it was created, or WHAT the release notes were. The wrong version is rolled back, causing an additional 2 hours of downtime. **Total cost: $5,000-$20,000 in downtime and incorrect rollback.** Fix: Always use annotated tags (`git tag -a`). Include release notes in the tag message. Sign tags with GPG for supply chain integrity.

- **`git add .` in a monorepo commits other teams' changes.** In a monorepo, a developer runs `git add .` from the root, accidentally staging 20 files across 5 projects that other teams were working on. The commit message says "fix login bug" but includes unrelated changes. Code review catches it, but 1 hour is wasted untangling the commit. **Total cost: $500-$1,500 per incident in review and untangling.** Fix: Use `git add -p` or `git add path/to/specific/files`. Configure IDE to stage only files in the current project.

## Verification
<!-- STANDARD: 3min -->

- [ ] Run `git log --oneline -20`: every commit message follows Conventional Commits format with meaningful descriptions
- [ ] Run `git log --oneline --diff-filter=A -- "*.key" "*.pem" "*.p12"`: no secret files found in repository history
- [ ] Run `git log --oneline -- "node_modules/*" "dist/*" "build/*" "*.class" "*.jar"`: no generated/artifacts in history
- [ ] Run `git branch --no-merged main`: all active branches are less than 5 days old and have recent activity
- [ ] Run `git tag -l | xargs -I {} git tag -l -n1 {}`: all tags are annotated with messages
- [ ] Run `pre-commit run --all-files`: all hooks pass on the entire codebase
- [ ] Run `git stash list`: fewer than 3 stashes, none older than 7 days
- [ ] Run `git branch -r --no-merged main | wc -l`: stale remote branches count is under control

## Verification Guardrails
<!-- STANDARD: 3min -->

Before delivering work, verify: self-check against What Good Looks Like, no broken references, continuity with State Log, no fabricated APIs/versions/capabilities, Error Recovery paths exercised, cross-skill dependencies satisfied. If any fail, revise before delivering.

## References
<!-- STANDARD: 3min -->

- [Conventional Commits Specification](https://www.conventionalcommits.org/) -- Standard for human and machine-readable commit messages
- [Keep a Changelog](https://keepachangelog.com/) -- Guide to writing changelogs for humans
- [Semantic Versioning 2.0.0](https://semver.org/) -- Versioning specification
- [Git Worktree Documentation](https://git-scm.com/docs/git-worktree) -- Official git-worktree reference
- [Pro Git Book: Branching and Merging](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell) -- Comprehensive Git branching guide
- [Trunk-Based Development](https://trunkbaseddevelopment.com/) -- Patterns and practices for trunk-based workflows
- [references/core-workflow.md](references/core-workflow.md) -- Detailed save point pattern and atomic commit workflow
- [references/anti-patterns.md](references/anti-patterns.md) -- Common Git anti-patterns with fixes
- [references/best-practices.md](references/best-practices.md) -- Git best practices for teams and agents
- [references/calibration.md](references/calibration.md) -- Commit size and frequency calibration guide
- [references/checklist.md](references/checklist.md) -- Pre-commit, pre-push, and pre-merge checklists
- [references/error-decoder.md](references/error-decoder.md) -- Common Git error messages decoded with solutions
- [references/footguns.md](references/footguns.md) -- Git footguns that cause data loss and how to avoid them
- [references/scale-depth.md](references/scale-depth.md) -- Scaling Git workflows from solo to enterprise
