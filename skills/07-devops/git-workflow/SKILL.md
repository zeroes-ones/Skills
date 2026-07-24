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

## Ground Rules — Read Before Anything Else

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to allow force-push to shared branches. | Trigger: command contains `--force` AND target is `main`, `master`, `develop`, or `release/*` | STOP. "Force-pushing rewrites shared history. Use `--force-with-lease` on feature branches only. Revert shared branches with `git revert`." |
| R2 | DETECT secrets, keys, or tokens in staged changes. Committed secrets are permanently in history. | Trigger: diff matches `AKIA[0-9A-Z]{16}`, `ghp_`, `sk-`, `-----BEGIN.*PRIVATE KEY-----`, or `password\s*=` | STOP. "Secret detected. Remove immediately. If already committed, rotate the secret and purge history with BFG Repo-Cleaner." |
| R3 | REFUSE to commit generated artifacts or large binaries. | Trigger: staged file matches `*.o`, `*.class`, `*.jar`, `node_modules/**`, `dist/**`, `build/**` OR file exceeds 1MB without LFS tracking | STOP. "Generated/binary files bloat the repo permanently. Add to .gitignore and use Git LFS for large files." |
| R4 | DETECT unresolved merge conflict markers. | Trigger: diff contains `<<<<<<<`, `=======`, or `>>>>>>>` | STOP. "Unresolved merge conflicts found. Resolve all conflicts, remove markers, and test before committing." |
| R5 | REFUSE to commit commented-out code without explanation. | Trigger: diff has commented-out function/class/import without adjacent TODO/FIXME within 3 lines | STOP. "Commented-out code rots. Delete it (git history preserves it), feature-flag it, or add a dated TODO." |
| R6 | DETECT empty or non-conventional commit messages. | Trigger: message is empty, equals "fix"/"wip"/"tmp"/"." or does not match Conventional Commits format | STOP. "Use `type(scope): description` format. Description must explain WHY, minimum 10 characters." |
| R7 | REFUSE to merge PR with failing CI. | Trigger: merging PR where CI status is failure, error, or pending | STOP. "CI checks are failing. Fix issues, rebase on latest main, ensure all checks pass, then merge." |

## The Expert's Mindset

- **Every commit is a save point.** Commit working slices of ~50-150 lines. If the build breaks, bisect finds the exact commit. If you need to revert, you lose minimal work. Commit like you are playing a game with no autosave.
- **The history tells a story.** A git log should read like a narrative of decisions, not a dump of file changes. Each commit message explains WHY the change exists -- the diff shows WHAT changed.
- **Main is always shippable.** Trunk-based development means main/master is always green, always deployable. If main is broken, all work stops. Protect main with branch protection rules, required reviews, and CI gates.
- **Worktrees over stash.** Git stash is a stack of forgotten changes. Git worktrees give you parallel working directories on different branches -- no context switching cost, no lost work, no stash conflicts. Use worktrees when an agent needs to work on multiple branches simultaneously.
- **Bisectability is the ultimate test.** If you cannot `git bisect` to find the exact commit that introduced a bug, your commits are too large or your history is not clean. Every commit should pass tests independently.

## Operating at Different Levels

- **Quick scan (30s):** Check branch status (`git status`), recent commits (`git log --oneline -10`), verify main is not diverged, check for uncommitted work or dirty worktrees.
- **Standard engagement (10min):** Review PR diff for atomicity, check commit message quality, verify CI status, run pre-commit hooks, squash fixup commits, rebase on main if behind.
- **Deep dive (full session):** Audit full repository history for secrets and large files, restructure commit history for clarity, set up branch protection rules, configure Git hooks, establish versioning and changelog automation.
- **Crisis mode (broken main, bad merge, lost work):** Triage: identify the breaking commit with `git bisect`, revert the breaking change, communicate to team. Use `git reflog` for lost commits. Never force-push to shared branches.

## When to Use

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

## Core Workflow

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

## Decision Trees

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

## Cross-Skill Coordination

| Scenario | Coordinate With | Why |
|----------|----------------|-----|
| CI/CD pipeline that runs on commits | ci-cd-builder | Hook configuration must align with pipeline stages |
| Monorepo with multiple teams committing | monorepo-manager | Branch protection, CODEOWNERS, affected-project detection |
| Release process with changelogs and versioning | release-manager | SemVer bump decisions, release notes, tag conventions |
| Commit signing and supply chain security | security-engineer | GPG signing, commit verification, SLSA provenance |
| Pre-commit testing strategy | qa-engineer | Which tests run pre-commit vs pre-push vs CI |
| Documentation versioning alongside code | documentation-engineer | Versioned docs, changelog integration |
| Incident: need to bisect and revert | incident-responder | Finding the breaking commit, safe revert strategy |

## Proactive Triggers

| # | Trigger Condition | Auto-Response |
|---|------------------|---------------|
| P1 | `git status` shows >50 modified files without commits in last 2 hours | [WARN] Large uncommitted change set. Break into atomic commits with `git add -p`. |
| P2 | Branch has diverged from main by >20 commits | [WARN] Branch is stale. Rebase on main to avoid complex merge conflicts later. |
| P3 | `git stash list` shows >3 stashes older than 7 days | [ALERT] Stashes are rotting. Pop or apply each stash, commit or discard. |
| P4 | Repository has no `.gitignore` or missing common patterns | [ALERT] Risk of committing generated files and secrets. Add .gitignore with OS, editor, and language-specific patterns. |
| P5 | No Git hooks configured in repository | [INFO] Consider setting up pre-commit hooks for linting, secret scanning, and commit message validation. |
| P6 | `git log --oneline` shows consecutive commits with same message | [WARN] Duplicate commit messages suggest fixup/squash opportunity before merging. |

## What Good Looks Like

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

1. **The 10-Commit Challenge:** Take a feature you built in one large commit. Rebuild it as 5-10 atomic commits where each commit message tells a clear story. Verify each commit passes tests independently using `git rebase -i --exec "npm test"`.

2. **Worktree Parallelism:** Set up 3 git worktrees on the same repository. In worktree A, develop a feature. In worktree B, fix a critical bug on main. In worktree C, review a teammate's PR. Switch between them without stashing or committing WIP.

3. **Bisect Drill:** Have a colleague introduce a bug in one of 20 commits without telling you which one. Use `git bisect` to find it in under 5 steps. Time yourself. Master `git bisect run` for automated bisection.

4. **History Rewrite:** Create a branch with 15 messy commits (wip messages, mixed concerns, one commit that adds a secret file). Use interactive rebase to produce 5 clean atomic commits with proper messages, and use BFG to remove the secret from history.

5. **Merge Conflict Gauntlet:** Have two branches make conflicting changes to the same 5 files (different refactors, renamed functions, moved files). Merge them without losing any work. Practice with `git mergetool` and understand when to accept theirs vs ours vs manually resolve.

## Gotchas

- **Force-pushing to main destroys the team's afternoon.** An engineer force-pushes a rebased main, overwriting 3 teammates' merged PRs. The reflog saves the commits, but coordination to re-apply takes 2 hours across 4 engineers. **Total cost: $1,500-$3,000 in lost productivity per incident.** Fix: Enable branch protection with force-push disabled on shared branches.

- **Committing node_modules bloats the repo forever.** A developer runs `git add .` without a .gitignore, commits 200MB of node_modules. Every clone from that point forward downloads those 200MB -- even after the files are removed from HEAD, they remain in history. For a team of 20 with CI runners, that is 4GB of wasted transfer per day. **Total cost: $500-$2,000/year in storage, bandwidth, and slower CI.** Fix: Set up .gitignore before the first commit. Use `git filter-branch` or BFG to purge if already committed.

- **A committed AWS key costs thousands in crypto mining.** A developer accidentally commits an AWS access key to a public GitHub repo. Within 5 minutes, bots scan the commit, extract the key, and spin up $50,000 worth of EC2 instances for cryptocurrency mining before AWS detects the anomaly. **Total cost: $10,000-$50,000 in unauthorized cloud charges.** Fix: Pre-commit secret scanning (gitleaks, detect-secrets). If a secret is committed, rotate it immediately -- revoking the key is the only reliable fix.

- **Squash-merging loses bisect granularity.** A team squashes a 50-commit feature branch into one commit on main. A bug introduced in commit 14 of 50 is now impossible to bisect -- the entire feature is one commit. Debugging time goes from 30 minutes (bisect) to 4 hours (manual code review). **Total cost: $1,000-$3,000 per incident in debugging time.** Fix: Squash only when individual commits are not meaningful. For well-structured features, use rebase-merge.

- **Stale branches accumulate merge debt exponentially.** A feature branch sits unmerged for 3 weeks while main advances by 200 commits. When the developer finally merges, there are 47 conflicts across 15 files. Resolution takes 6 hours instead of the 30 minutes it would have taken if rebased weekly. **Total cost: $1,500-$4,000 per stale branch in merge resolution time.** Fix: Rebase feature branches on main at least every 2-3 days. Set up CI to flag branches >5 commits behind main.

- **Annotated tags vs lightweight tags cause deployment confusion.** A team tags releases with lightweight tags (`git tag v1.2.0`). When debugging a production issue, they cannot determine WHO created the tag, WHEN it was created, or WHAT the release notes were. The wrong version is rolled back, causing an additional 2 hours of downtime. **Total cost: $5,000-$20,000 in downtime and incorrect rollback.** Fix: Always use annotated tags (`git tag -a`). Include release notes in the tag message. Sign tags with GPG for supply chain integrity.

- **`git add .` in a monorepo commits other teams' changes.** In a monorepo, a developer runs `git add .` from the root, accidentally staging 20 files across 5 projects that other teams were working on. The commit message says "fix login bug" but includes unrelated changes. Code review catches it, but 1 hour is wasted untangling the commit. **Total cost: $500-$1,500 per incident in review and untangling.** Fix: Use `git add -p` or `git add path/to/specific/files`. Configure IDE to stage only files in the current project.

## Verification

- [ ] Run `git log --oneline -20`: every commit message follows Conventional Commits format with meaningful descriptions
- [ ] Run `git log --oneline --diff-filter=A -- "*.key" "*.pem" "*.p12"`: no secret files found in repository history
- [ ] Run `git log --oneline -- "node_modules/*" "dist/*" "build/*" "*.class" "*.jar"`: no generated/artifacts in history
- [ ] Run `git branch --no-merged main`: all active branches are less than 5 days old and have recent activity
- [ ] Run `git tag -l | xargs -I {} git tag -l -n1 {}`: all tags are annotated with messages
- [ ] Run `pre-commit run --all-files`: all hooks pass on the entire codebase
- [ ] Run `git stash list`: fewer than 3 stashes, none older than 7 days
- [ ] Run `git branch -r --no-merged main | wc -l`: stale remote branches count is under control

## References

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
