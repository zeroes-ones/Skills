---
name: merge-conflict-resolver
description: >
  Use when a git merge or rebase produces conflicts that need systematic resolution; when conflicts span multiple files with interdependent changes; when the intent behind conflicting changes is unclear; when merging long-running feature branches; or when rebasing onto a significantly diverged base. Handles hunk-by-hunk conflict resolution with intent tracing, primary source identification (commit message, PR, issue) for each side of a conflict, resolution strategy selection (accept-ours, accept-theirs, manual-merge, extract-to-shared), build-and-test verification after each resolution, merge completion without --abort, conflict pattern recognition (textual, semantic, structural), and resolution documentation. Do NOT use for choosing merge vs rebase strategy (route to git-workflow), preventing conflicts proactively (route to git-workflow), or CI/CD pipeline issues (route to ci-cd-builder).
license: MIT
author: Sandeep Kumar Penchala
type: devops
status: stable
version: 1.0.0
updated: 2026-07-23
tags:
  - git
  - merge-conflicts
  - rebase
  - conflict-resolution
  - version-control
  - devops
token_budget: 4000
chain:
  consumes_from:
    - git-workflow
    - code-reviewer
  feeds_into:
    - ci-cd-builder
    - release-manager
    - qa-engineer
  alternatives: []
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
---

# Merge Conflict Resolver
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Hunk-by-hunk merge conflict resolution traced to intent. Work through an in-progress git merge or rebase conflict systematically, resolving each conflict by tracing intent back to each side's primary source, then finish the operation — never `--abort` without explicit user direction.

## Ground Rules — Read Before Anything Else

These rules are non-negotiable. A violation of any rule means the resolution is unsound and must be redone.

| Rule | Mechanical Trigger | Violation Response |
|------|-------------------|-------------------|
| **R1: NEVER —abort without explicit user direction** | User types "just abort" or "start over" | Confirm: "Are you sure? All in-progress resolutions will be lost. Type CONFIRM to proceed." |
| **R2: DETECT when resolution ignores one side's intent entirely** | A hunk resolves to 100% OURS or 100% THEIRS without an explicit strategy selection | Halt. Ask: "This resolution discards all changes from [SIDE]. What is your reason for rejecting their intent?" |
| **R3: REFUSE to resolve conflict without tracing each side to primary source** | Conflict resolution begins without commit message/PR/issue lookup for both sides | Block. Require: "I need to trace the intent behind both conflicting changes before resolving. Let me look up the commit, PR, or issue for each side." |
| **R4: DETECT semantic conflicts (code merges cleanly but logic is wrong)** | Merge succeeds with no conflict markers but introduces logical contradictions | Flag: "This merged cleanly but I detect a semantic conflict — [EXPLANATION]. The code compiles but the logic is inconsistent." |
| **R5: REFUSE to batch-resolve conflicts (must be hunk-by-hunk)** | User says "just accept theirs for everything" or similar blanket resolution | Reject: "Batch resolution loses intent. Each hunk represents an independent decision. I'll walk through them one at a time." |
| **R6: VERIFY build and tests after each resolution before proceeding** | A hunk is marked resolved but build/test hasn't run | Pause: "I need to verify this resolution compiles and passes tests before moving to the next hunk." |
| **R7: DOCUMENT every resolution decision with rationale** | A hunk is resolved without recording strategy and source | Append to resolution log: strategy used, source traced, rationale, and verification result. |

## The Expert's Mindset

Conflict resolution masters see what novices miss. They don't race to green; they excavate intent.

| Cognitive Bias | What Novices Do | What Masters Do |
|---------------|----------------|----------------|
| **Familiarity bias** | Accept their own changes because they understand them | Read both sides equally, trace unfamiliar code back to its author's intent |
| **Recency bias** | Prefer the side they just worked on | Evaluate both sides by the strength of their reasoning, not their timestamp |
| **Completion bias** | Rush to finish the merge regardless of correctness | Slow down at each hunk — a working merge with semantic bugs is worse than an unresolved one |
| **Authority bias** | Accept a senior engineer's changes without scrutiny | Verify every change against its stated intent, regardless of who wrote it |
| **Sunk-cost fallacy** | Stick with a bad resolution because they've already invested time | Discard a flawed resolution and re-approach the hunk from scratch |
| **Overconfidence** | Assume they understand both sides without reading the source context | Read the full commit message, PR description, and linked issue for every conflicting hunk |

The master resolver treats each conflict marker as a door into another developer's thought process. They don't just diff lines — they reconstruct the mental model that produced each change.

## Operating at Different Levels

**L1 — Single-File, Single-Hunk Conflict**
One conflict in one file. Quick resolution with intent tracing still required. Verify: build the file, run the test for that module. Time: 5-15 minutes.

**L2 — Multi-File, Related Conflicts (3-8 files)**
Conflicts spread across files that share a feature boundary. Trace the feature's intent from the PR. Resolve in dependency order (shared utilities first, then consumers). Verify: full module build and test suite. Time: 30-90 minutes.

**L3 — Cross-Module Conflict (8-20 files)**
Interdependent conflicts across modules with different owners. Trace intent to multiple PRs. Use extract-to-shared pattern for overlapping abstractions. Verify: integration test suite. Time: 2-4 hours.

**L4 — Multi-Branch Merge (20+ files, multiple feature branches)**
Dozens of conflicts from parallel development streams. Build a conflict dependency graph. Resolve in dependency order. Coordinate with branch owners for conflicting design decisions. Verify: full CI pipeline locally. Time: 4-8 hours.

## When to Use

**Use this skill when:**
- A `git merge` or `git rebase` is in-progress with unresolved conflicts
- Conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`) exist in working tree files
- `.git/MERGE_HEAD` or `.git/rebase-apply` (or `.git/rebase-merge`) exists
- `git status` shows `both modified` files
- Conflicts span multiple files with interdependent changes
- The intent behind conflicting changes is unclear or undocumented
- A long-running feature branch needs to merge into a significantly diverged base
- You're rebasing onto a base that has undergone substantial refactoring

**Do NOT use this skill for:**
- Choosing merge vs rebase strategy → route to `git-workflow`
- Preventing conflicts proactively (branching strategy, communication) → route to `git-workflow`
- CI/CD pipeline configuration for merge gates → route to `ci-cd-builder`
- Post-merge release coordination → route to `release-manager`
- General code review of the merged result → route to `code-reviewer`

## Route the Request

### Auto-Route by Artifacts

Check these signals in order. The first match determines routing:

```
Check .git/MERGE_HEAD exists?     → YES → merge-conflict-resolver (merge in progress)
                                   → NO  → continue

Check .git/rebase-apply or
.git/rebase-merge exists?          → YES → merge-conflict-resolver (rebase in progress)
                                   → NO  → continue

Check conflict markers in working
tree (<<<<<<< in tracked files)?   → YES → merge-conflict-resolver (unresolved markers)
                                   → NO  → route to git-workflow (proactive strategy)
```

Quick detection command:
```bash
test -f .git/MERGE_HEAD && echo "MERGE_IN_PROGRESS" || \
  test -d .git/rebase-apply -o -d .git/rebase-merge && echo "REBASE_IN_PROGRESS" || \
  git diff --name-only --diff-filter=U | head -1 | grep -q . && echo "CONFLICTS_PRESENT" || \
  echo "NO_CONFLICT"
```

### Intent Route

```
User says: "resolve conflicts" or
           "fix merge" or
           "I'm stuck on a rebase"
  └─ Do they have conflict markers or git state?
       ├─ YES → merge-conflict-resolver
       └─ NO → git-workflow (proactive strategy)

User says: "merge this branch"
  └─ Is a merge/rebase already in progress?
       ├─ YES → merge-conflict-resolver (resolve first, then complete)
       └─ NO → git-workflow (strategy selection, then merge)
```

## Core Workflow

### Phase 1: Conflict Inventory

List all conflicted files and their hunk count. Build the resolution queue.

```bash
# List conflicted files
git diff --name-only --diff-filter=U

# Count hunks per file
for f in $(git diff --name-only --diff-filter=U); do
  echo "$f: $(grep -c '^<<<<<<<' "$f") hunks"
done
```

Output a **Conflict Inventory Table**:

| File | Hunks | OURS Branch | THEIRS Branch | Risk |
|------|-------|-------------|---------------|------|
| src/auth/login.ts | 3 | feature/2fa | main | HIGH |
| src/auth/session.ts | 1 | feature/2fa | main | LOW |
| src/api/middleware.ts | 2 | feature/2fa | main | MEDIUM |

Risk assessment: HIGH = >3 hunks, or changes to critical paths, or semantic overlap with other files. MEDIUM = 2-3 hunks, moderate complexity. LOW = 1 hunk, simple textual conflict.

### Phase 2: Intent Tracing per Hunk

For each hunk, trace OURS and THEIRS to their primary source. This is the heart of the skill.

**Step 2a: Identify the commits that touched the conflicting lines**

```bash
# For each conflicted file, find the commits on each side
git log --oneline --no-merges MERGE_HEAD..MERGE_HEAD^1 -- <file>   # OURS commits
git log --oneline --no-merges MERGE_HEAD^2..MERGE_HEAD -- <file>   # THEIRS commits (for merge)
# For rebase:
git log --oneline --no-merges HEAD..REBASE_HEAD -- <file>           # being applied
```

**Step 2b: Extract commit messages and trace to PR/issue**

```bash
# Get full commit message for the relevant commit
git log -1 --format="%B" <commit-hash>

# Find PR number if present (GitHub merge commits)
git log -1 --format="%B" <commit-hash> | grep -oP 'Merge pull request #\K\d+'

# Find issue references
git log -1 --format="%B" <commit-hash> | grep -oP '#\d+'
```

**Step 2c: Build intent summary for each side**

```
Hunk: src/auth/login.ts, lines 45-72
OURS (feature/2fa):   Adds TOTP-based 2FA challenge after password auth.
                      Commit: a1b2c3d "Implement TOTP 2FA flow"
                      PR: #1842 "Add two-factor authentication"
                      Issue: #1838 "MFA requirement for SOC2 compliance"

THEIRS (main):        Refactored auth pipeline to support pluggable auth providers.
                      Commit: e5f6g7h "Extract auth to provider pattern"
                      PR: #1901 "Pluggable authentication providers"
                      Issue: #1895 "Auth extensibility for SSO integration"
```

### Phase 3: Resolution Strategy Selection

For each hunk, select exactly one strategy:

| Strategy | When to Use | Risk |
|----------|------------|------|
| **accept-ours** | THEIRS is a refactor that our feature already accounts for; or THEIRS changes were superseded by OURS | MEDIUM — verify no lost functionality |
| **accept-theirs** | OURS is now redundant (merged into THEIRS refactor); or THEIRS fixes a bug our feature depends on | MEDIUM — verify our feature intent is preserved |
| **manual-merge** | Both sides add independent, non-overlapping value; or intent of both sides must be preserved | HIGH — requires understanding both intents deeply |
| **extract-to-shared** | Both sides introduce the same concept with different implementations; both need to coexist | HIGHEST — structural change, creates new abstraction |

If no strategy clearly fits, **default to manual-merge**. Never default to accept-ours or accept-theirs.

### Phase 4: Hunk-by-Hunk Resolution

Process hunks in dependency order. For each hunk:

1. **Read the conflict markers** — understand exactly what differs
2. **Review the intent summary** from Phase 2
3. **Select resolution strategy** using the decision tree (see Decision Trees section)
4. **Apply the resolution** — edit the file to remove conflict markers
5. **Stage the resolved file**: `git add <file>`
6. **Verify**: build and run relevant tests
7. **Document**: record strategy, source, rationale in resolution log
8. **Proceed** to next hunk only after verification passes

```bash
# After resolving a hunk and staging:
git add <resolved-file>
# Build verification
npm run build -- --scope=<affected-package>   # or equivalent
# Test verification
npm test -- --testPathPattern=<affected-module>
```

If verification fails, re-examine the hunk. A failure means the resolution broke something — do not proceed.

### Phase 5: Merge Completion

After all hunks are resolved and verified:

1. **Final full build**: `npm run build` (or equivalent)
2. **Full test suite**: `npm test` (or equivalent)
3. **Conflict resolution log review**: confirm every hunk has a documented resolution
4. **Complete the operation**:
   ```bash
   # For merge:
   git commit --no-edit   # uses the auto-generated merge message
   # For rebase:
   git rebase --continue
   ```
5. **Post-resolution validation**: run the full CI pipeline locally if available

## Decision Trees

### Resolution Strategy Selection

```
For each conflicted hunk:
  │
  ├─ Does one side's change completely subsume the other?
  │   ├─ YES → Is the subsumed side's intent still satisfied?
  │   │   ├─ YES → accept-the-side-that-subsume (accept-ours or accept-theirs)
  │   │   └─ NO  → manual-merge (preserve the subsumed intent differently)
  │   └─ NO  → continue
  │
  ├─ Are both sides introducing the same concept with different implementations?
  │   ├─ YES → extract-to-shared (create a shared abstraction both use)
  │   └─ NO  → continue
  │
  ├─ Can the changes coexist without semantic conflict?
  │   ├─ YES → manual-merge (interleave both changes)
  │   └─ NO  → continue
  │
  └─ Is there a clear correctness argument for one side?
      ├─ YES → accept-that-side (with explicit rationale)
      └─ NO  → manual-merge (escalate to human if unresolvable)
```

### Intent Source Prioritization

When tracing intent, prefer sources in this order:

```
Intent Source Hierarchy:
  │
  ├─ 1. Linked issue (most authoritative — captures "why")
  │   └─ Contains: problem statement, requirements, acceptance criteria
  │
  ├─ 2. PR description
  │   └─ Contains: approach, trade-offs, design decisions
  │
  ├─ 3. Commit message body
  │   └─ Contains: implementation rationale, context
  │
  ├─ 4. Commit message subject
  │   └─ Contains: summary, but may lack nuance
  │
  ├─ 5. Code comments in the conflicting region
  │   └─ Contains: developer notes, but may be stale
  │
  └─ 6. Diff context (least authoritative — describes "what")
      └─ Contains: changed lines, but not why they changed
```

### Semantic Conflict Detection

A semantic conflict exists when the merge succeeds textually but the resulting code has logical errors. Detection patterns:

```
Check after every manual-merge and accept-* resolution:
  │
  ├─ Duplicate logic check:
  │   Did both sides add the same function/logic under different names?
  │   → grep for similar logic patterns across the merged file
  │
  ├─ Inverted condition check:
  │   Did one side negate a condition the other side depends on?
  │   → Trace control flow: if-else, guard clauses, early returns
  │
  ├─ Missing dependency check:
  │   Does one side's change reference a symbol the other side removed/renamed?
  │   → Verify all imports, function calls, and variable references resolve
  │
  ├─ Order-of-operations check:
  │   Did both sides add initialization/setup steps that now run in wrong order?
  │   → Trace execution order in the merged function
  │
  └─ Contract violation check:
      Did one side change a function signature the other side calls?
      → Check all call sites of modified functions
```

### Conflict Pattern Classification

Classify each conflict hunk into one of these patterns:

```
Conflict Markers Detected:
  │
  ├─ Textual: Same lines modified differently
  │   ├─ Adjacent-line: different changes on adjacent lines (easy)
  │   ├─ Same-line: exact same line modified by both (medium)
  │   └─ Interleaved: alternating blocks from each side (hard)
  │
  ├─ Structural: Changes to code organization
  │   ├─ Import-reorder: import statements reorganized differently
  │   ├─ Function-moved: same function moved to different locations
  │   ├─ File-split: one side split a file the other side modified
  │   └─ Rename-collision: same symbol renamed differently on each side
  │
  └─ Semantic: Code intent conflicts
      ├─ Logic-inversion: one side negates the other's assumption
      ├─ Contract-change: function signature vs call site mismatch
      ├─ Initialization-order: setup steps from both sides conflict
      └─ Data-flow: one side changes data shape the other side consumes
```

### When to Extract to Shared Module

The extract-to-shared strategy is the most invasive and should be used deliberately:

```
Both sides introduce similar but incompatible implementations:
  │
  ├─ Is the concept genuinely shared (not coincidental similarity)?
  │   ├─ NO → manual-merge (keep separate implementations)
  │   └─ YES → continue
  │
  ├─ Will extracting to shared reduce future conflict surface?
  │   ├─ NO → manual-merge (one-time conflict, not worth the refactor)
  │   └─ YES → continue
  │
  ├─ Can the shared abstraction be cleanly defined?
  │   ├─ NO → manual-merge (don't force a bad abstraction)
  │   └─ YES → extract-to-shared
  │
  └─ Extract-to-shared workflow:
      1. Create the shared module/function with a clean interface
      2. Update OURS to use the shared implementation
      3. Update THEIRS to use the shared implementation
      4. Verify both sides' tests pass with the shared code
      5. Document the abstraction in the resolution log
```

## Cross-Skill Coordination

| Skill | Relationship | Handoff Trigger |
|-------|-------------|----------------|
| **git-workflow** | Consumer | Before merging: "Should I merge or rebase?" → git-workflow decides strategy, merge-conflict-resolver executes |
| **code-reviewer** | Consumer | After resolution: "Review the merged result for logic errors" → code-reviewer audits the resolved code |
| **ci-cd-builder** | Producer | After merge completion: "Validate the merge in CI" → ci-cd-builder ensures pipeline runs clean |
| **qa-engineer** | Producer | After merge: "Test the merged result for regressions" → qa-engineer runs targeted test suite |
| **release-manager** | Producer | After merge to release branch: "This merge is ready for release" → release-manager coordinates deployment |

**Coordination protocol**: When merge-conflict-resolver feeds into another skill, it passes along:
1. The resolution log (all hunk resolutions with rationale)
2. The intent trace (commit/PR/issue for each side of each conflict)
3. Verification results (build and test pass status for each resolution)

## Proactive Triggers

| Trigger | Detection | Action |
|---------|----------|--------|
| **Mid-merge state** | `.git/MERGE_HEAD` exists | "You have an in-progress merge. I'll inventory the conflicts and begin resolution." |
| **Mid-rebase state** | `.git/rebase-apply` or `.git/rebase-merge` exists | "You have an in-progress rebase. I'll show the conflict inventory first." |
| **Conflict markers in files** | `grep -r '<<<<<<<' --include='*.ts' --include='*.js' .` finds markers | "I found conflict markers in [N] files. Let me trace intent for each hunk." |
| **`git status` shows `both modified`** | `git status --porcelain \| grep '^UU'` | "There are unmerged files. Let me inventory the conflicts." |
| **Merge conflict on PR** | GitHub PR shows "This branch has conflicts" | "The PR has conflicts with the base branch. I'll resolve them locally and push." |
| **User enters a merge/rebase that fails** | `git merge` or `git rebase` exits non-zero with conflict message | Intercept: "The operation paused with conflicts. I'll take over resolution." |
| **Semantic conflict detected post-merge** | Tests fail after clean merge; or logic inspection finds contradictions | "The merge succeeded textually but produced a semantic conflict. I'll re-examine the merged code." |

## What Good Looks Like

```
COMMIT: a1b2c3d              COMMIT: e5f6g7h
"Add TOTP 2FA flow"          "Extract auth to provider pattern"
PR #1842 ──┐                 PR #1901 ──┐
           │                            │
           ▼                            ▼
    ┌──────────┐               ┌──────────────┐
    │  OURS    │               │   THEIRS     │
    │ TOTP     │               │  Pluggable   │
    │ challenge│               │  providers   │
    └────┬─────┘               └──────┬───────┘
         │                            │
         └──────────┬─────────────────┘
                    │
                    ▼
         ┌─────────────────┐
         │  CONFLICT HUNK  │
         │  src/auth/      │
         │  login.ts:45-72 │
         └────────┬────────┘
                  │
     ┌────────────┼────────────┐
     ▼            ▼            ▼
 ┌───────┐  ┌──────────┐  ┌──────────┐
 │accept │  │ manual-  │  │ extract- │
 │-ours  │  │ merge    │  │ to-shared│
 │       │  │          │  │          │
 │R: OURS│  │R: Both   │  │R: New    │
 │already│  │add value,│  │shared    │
 │covers │  │interleave│  │auth      │
 │refactor│  │          │  │provider  │
 └───┬───┘  └────┬─────┘  └────┬─────┘
     │           │              │
     └───────────┼──────────────┘
                 ▼
         ┌──────────────┐
         │ VERIFY:      │
         │ ✓ build      │
         │ ✓ unit tests │
         │ ✓ integration│
         └──────┬───────┘
                ▼
         ┌──────────────┐
         │ DOCUMENT:    │
         │ resolution   │
         │ log entry    │
         └──────┬───────┘
                ▼
         ┌──────────────┐
         │ NEXT HUNK    │
         └──────────────┘
```

Each hunk gets its own resolution pathway. No shortcuts. No batch acceptance. The resolution log serves as an audit trail connecting each conflict back to its source intent.

## Deliberate Practice

### Exercise 1: Intent Tracing Drill (15 min)
Take a merged PR with known conflicts. For each conflicting hunk, trace the intent of both sides back to their commits and issues. Time yourself: you should be able to identify the primary source (commit, PR, issue) for each hunk within 2 minutes.

### Exercise 2: Strategy Selection Speedrun (10 min)
Given 10 conflict scenarios (description of OURS vs THEIRS changes), select the correct resolution strategy (accept-ours, accept-theirs, manual-merge, extract-to-shared) within 30 seconds each. Check against expert answers.

### Exercise 3: Semantic Conflict Detection (20 min)
Review 5 merge commits that introduced bugs despite clean textual merges. For each, identify the semantic conflict that testing caught. Practice writing the pattern that would have caught it during resolution.

### Exercise 4: Multi-Hunk Dependency Resolution (30 min)
Set up a scenario with 5+ interrelated conflict hunks across 3 files. Resolve them in dependency order, verifying after each. Compare your resolution order to the optimal dependency graph.

### Exercise 5: The No-Abort Challenge (45 min)
A colleague creates a deliberately difficult merge conflict (10+ hunks, semantic traps). Resolve it from inventory to completion without using `--abort`. Time yourself. Review each resolution decision afterward.

## Gotchas

### Gotcha 1: The --abort reflex ($15,000+)
The cost of `git merge --abort` or `git rebase --abort` as a reflex when conflicts get messy. Every hunk you've already resolved is lost. On a complex merge with 2 hours of work in, aborting means restarting from zero — that's $150/hr × 2 hours = $300 of direct time, plus $14,700+ in delayed feature delivery if the merge was on the critical path for a release.

### Gotcha 2: Accepting "mine" without reading "theirs" ($5,000-$50,000)
Blindly `git checkout --ours` on every conflicted file discards the other side's intent entirely. If the other side fixed a critical bug or implemented a feature your team depends on, you've just re-introduced the bug or lost the feature. The cost ranges from a $5,000 bug-fix redo to a $50,000 production incident.

### Gotcha 3: Semantic conflicts that merge cleanly ($20,000-$100,000)
The most expensive gotcha. Git merges the text perfectly — no conflict markers, no warnings. But the merged code has contradictory logic: one side assumes a value is always defined, the other added a null path. The bug reaches production. Detection cost: $5,000 in debugging. Fix cost: $3,000. Reputation cost: $12,000+. If it causes a data loss incident: $80,000+.

### Gotcha 4: Batching conflict resolution ($3,000-$10,000)
Resolving all conflicts at once without verifying between hunks. A resolution in file A breaks file B's assumption. You discover this only after resolving everything. Now you have to unwind: which of the 15 resolutions caused the failure? Each wrong guess costs time. With hunk-by-hunk verification, you'd catch the issue after the first bad resolution — 2 minutes of rework instead of 2 hours.

### Gotcha 5: No verification between resolutions ($8,000-$25,000)
Skipping the build-and-test step between hunk resolutions because "it's just a small change." Three hunks later, the build fails. Was it hunk 1, 2, or 3? Without per-hunk verification, you're binary-searching through your resolutions. Cost: $8,000 in wasted debugging time. If the unverified merge reaches CI and breaks the pipeline for the team: $25,000 in blocked productivity.

### Gotcha 6: Lost intent context ($10,000-$30,000)
Resolving conflicts without tracing intent. Two months later, someone asks: "Why did we resolve the auth conflict this way?" Nobody knows. The decision dies with the resolver. Cost: $10,000 to re-investigate. If the wrong resolution causes a security vulnerability: $30,000 in audit, remediation, and compliance fallout.

### Gotcha 7: Extract-to-shared without consensus ($15,000-$40,000)
Extracting a shared abstraction during conflict resolution without consulting the original authors. The new abstraction doesn't fit both use cases cleanly. One team works around it, introducing technical debt. The abstraction must be refactored or reverted. Cost: $15,000-$40,000 in rework across both teams.

## Verification

Run these checks before declaring the conflict resolution complete:

```bash
# 1. Verify no conflict markers remain in any tracked file
grep -r '<<<<<<<' $(git ls-files) && echo "FAIL: Conflict markers still present" || echo "PASS"

# 2. Verify all files are staged
git diff --name-only --diff-filter=U | grep -q . && echo "FAIL: Unstaged conflicted files" || echo "PASS"

# 3. Verify build succeeds
npm run build  # or: make build, cargo build, etc.
# Check exit code: must be 0

# 4. Verify tests pass
npm test  # or: make test, cargo test, etc.
# Check exit code: must be 0

# 5. Verify resolution log exists and covers all hunks
test -f .merge-conflict-resolution-log.md || echo "FAIL: Resolution log missing"

# 6. Semantic conflict check: grep for duplicated function definitions
grep -n 'function\|const.*=.*(' <resolved-file> | sort -t: -k2 | uniq -d -f1 && \
  echo "WARN: Possible duplicate definitions" || echo "PASS"

# 7. Verify no unstaged changes (clean working tree aside from merge state)
git diff --name-only | grep -q . && echo "WARN: Unstaged changes detected" || echo "PASS"
```

## References

- [references/hunk-analysis.md](references/hunk-analysis.md) — Detailed methodology for analyzing individual conflict hunks, classifying complexity, and identifying dependency relationships between hunks
- [references/intent-tracing.md](references/intent-tracing.md) — Step-by-step guide to tracing each side of a conflict back to its commit, PR, and issue with source hierarchy prioritization
- [references/resolution-strategies.md](references/resolution-strategies.md) — Deep dive into each resolution strategy with examples, risk profiles, and when each is most appropriate
- [references/source-identification.md](references/source-identification.md) — Techniques for identifying the primary source of a change: git blame, log searching, PR/issue linking, and author context
- [references/conflict-patterns.md](references/conflict-patterns.md) — Catalog of conflict patterns (textual, structural, semantic) with recognition heuristics and resolution templates
- [references/verification-gates.md](references/verification-gates.md) — Per-hunk and per-phase verification gates: build checks, test selection, semantic validation, and CI pipeline integration
- [references/extract-to-shared.md](references/extract-to-shared.md) — Decision framework and workflow for the extract-to-shared resolution strategy with abstraction design guidelines
- [references/resolution-documentation.md](references/resolution-documentation.md) — Template and best practices for the resolution log: what to record, format conventions, and long-term maintenance
