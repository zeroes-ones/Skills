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
| **R8: ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| **R9: RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |

- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset
<!-- STANDARD: 3min -->

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
<!-- STANDARD: 3min -->

**L1 — Single-File, Single-Hunk Conflict**
One conflict in one file. Quick resolution with intent tracing still required. Verify: build the file, run the test for that module. Time: 5-15 minutes.

**L2 — Multi-File, Related Conflicts (3-8 files)**
Conflicts spread across files that share a feature boundary. Trace the feature's intent from the PR. Resolve in dependency order (shared utilities first, then consumers). Verify: full module build and test suite. Time: 30-90 minutes.

**L3 — Cross-Module Conflict (8-20 files)**
Interdependent conflicts across modules with different owners. Trace intent to multiple PRs. Use extract-to-shared pattern for overlapping abstractions. Verify: integration test suite. Time: 2-4 hours.

**L4 — Multi-Branch Merge (20+ files, multiple feature branches)**
Dozens of conflicts from parallel development streams. Build a conflict dependency graph. Resolve in dependency order. Coordinate with branch owners for conflicting design decisions. Verify: full CI pipeline locally. Time: 4-8 hours.

## When to Use
<!-- STANDARD: 3min -->

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
<!-- STANDARD: 3min -->


## Auto-Route by Artifacts
<!-- STANDARD: 3min -->

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


## Intent Route
<!-- STANDARD: 3min -->

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

## Core Workflow **(STANDARD)**
<!-- STANDARD: 3min -->
<!-- Full 121 lines extracted to references/core-workflow.md -->


## Phase 1: Conflict Inventory
<!-- STANDARD: 3min -->
List all conflicted files and their hunk count. Build the resolution queue.
# List conflicted files
git diff --name-only --diff-filter=U
...
> 📎 **[references/core-workflow.md](references/core-workflow.md)** — 121 lines of detailed guidance

## Decision Trees **(QUICK)**
<!-- STANDARD: 3min -->

### Decision Tree 1: Merge vs Rebase Decision

        ┌── INPUT: Which operation to use for integrating branches?
        │
   ┌────┴────────────────────┐
   │                         │
   ▼                         ▼
Feature branch → main        Long-running branch
(short-lived, <1 week)       diverged significantly
   │                         │
   ▼                         ▼
Rebase preferred             Merge preferred
git rebase main              git merge main
   │                         │
   ▼                         ▼
Clean linear history         Preserves context of
Resolve conflicts            when/how branches
commit-by-commit             diverged
   │                         │
   ▼                    ┌────┴────┐
If >5 conflicts         │         │
during rebase →         ▼         ▼
switch to merge        Shared     Feature
   │                  branch      branch into
   ▼                  (release)   main
Avoid rebasing           │         │
shared branches          ▼         ▼
(rewrites public      Always merge  Merge creates
history)              --no-ff to     merge commit
                      preserve       (document the
                      branch tip     integration point)

### Decision Tree 2: Conflict Resolution Strategy

        ┌── INPUT: For each conflicted hunk — which strategy?
        │
   ┌────┴────────────────────┬──────────────┐
   │                         │              │
   ▼                         ▼              ▼
One side completely          Both sides     Changes are
subsumes the other           introduce      semantically
   │                         same concept   incompatible
   ▼                         │              │
Is subsumed intent           ▼              ▼
still satisfied?        extract-to-shared  manual-merge
   │                    Create shared       or escalate
┌──┴──┐                 abstraction         │
│     │                 both can use        ▼
▼     ▼                    │              Document both
YES   NO                   ▼              intents, flag
│     │                 Verify both       for human
▼     ▼                 sides compile     decision
accept-that-side       against shared    │
(with rationale)       interface         ▼
│ must trace intent    │              NEVER resolve
▼                      ▼              by discarding
Record in              Best for       one side without
resolution log         utility fn,    explicit strategy
                       config, types  selection

### Decision Tree 3: Post-Resolution Verification

        ┌── INPUT: Conflict resolved — what verification is needed?
        │
   ┌────┴────────────────────┬──────────────┐
   │                         │              │
   ▼                         ▼              ▼
Build verification           Test suite     Semantic check
   │                         │              │
   ▼                         ▼              ▼
Does it compile?             Run affected   Are both sides'
   │                         tests only     intents actually
┌──┴──┐                      │              preserved?
│     │                 ┌────┴────┐         │
▼     ▼                 │         │    ┌────┴────┐
YES   NO                ▼         ▼    │         │
│     │               All pass  Fail   ▼         ▼
▼     ▼                 │         │    YES       NO
Continue Re-resolve     ▼         ▼    │         │
to next the hunk     Continue  Investigate ▼     ▼
hunk   with correct    │        fix before  Done   Flag as
│      intent          ▼        proceeding         semantic
▼                      Verify                             conflict
Proceed to next        linter                │
hunk until all         passes too            ▼
resolved                                      Escalate to
│                                             human review
▼
git merge --continue
or git rebase --continue


## Resolution Strategy Selection
<!-- STANDARD: 3min -->

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


## Intent Source Prioritization
<!-- STANDARD: 3min -->

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


## Semantic Conflict Detection
<!-- STANDARD: 3min -->

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


## Conflict Pattern Classification
<!-- STANDARD: 3min -->

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


## When to Extract to Shared Module
<!-- STANDARD: 3min -->

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

## Gotchas
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

| Gotcha | Cost | Fix |
|--------|------|-----|
| Accepting `ours` or `theirs` without tracing intent — a developer resolves 47 merge conflicts by blindly accepting one side; 3 weeks later, a critical bug fix from the rejected side is discovered missing in production | $50K-$200K in production regression from lost code | Never accept a side without tracing intent for every hunk; Phase 2 (Intent Tracing) is mandatory, not optional; default to manual-merge when intent is unclear |
| Merge succeeds textually but fails semantically — the code compiles and tests pass, but both sides added the same function under different names; the duplicate logic causes unpredictable behavior at runtime | $30K-$100K in semantic bugs discovered days after merge | After resolution, grep for similar logic patterns across the merged file; run integration tests that exercise both code paths; add semantic conflict detection to the resolution checklist |
| Skipping the full test suite after resolution — individual hunk tests pass but the integration between resolved hunks breaks; the merge is pushed and CI catches it 10 minutes later | $5K-$30K in CI cycle waste and team trust erosion | Always run the full test suite before completing the merge; `npm test` (not just scoped tests); if CI would have caught it, you should catch it locally first |

## Error Decoder — War Stories from the Trenches
<!-- STANDARD: 3min -->

**(STANDARD)**

When this domain goes wrong, it goes wrong in predictable ways. Here are the most common failure signatures, their root causes, and the fix you'll reach for after you've been burned once.

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| `git merge` succeeds with zero conflict markers but the build fails with "undefined method `calculate_total` for Order" | Semantic conflict — Branch A renamed `calculate_total` to `compute_total` and refactored all callers. Branch B added a NEW caller of `calculate_total` in a different file. Git sees no textual conflict because no lines overlap. The merge is clean; the code is broken | Run `git diff main...feature` (three-dot diff) to see what EACH branch changed relative to the merge base. Check for renames: `git log --diff-filter=R --name-only`. After merge, search for deleted symbols: `grep -r "calculate_total"` — if found, a semantic conflict exists | Textual merge succeeds when semantic merge fails. Renamed methods, moved files, and changed defaults don't produce conflict markers but produce broken builds. Three-dot diffs against the merge base reveal semantic conflicts that two-dot diffs hide. |
| Resolving conflicts in a 1,200-line minified JSON file — every hunk is "the whole file changed" because the file is single-line | A `package-lock.json` or auto-generated Swagger spec was minified as a single line. Both branches modified different dependencies, but Git sees the entire single-line file as one big conflict. The conflict markers make the JSON invalid, so even partial resolution is untestable | Before branching: reformat minified files with `jq .`, `prettier --write`, or `python -m json.tool`. Commit the formatted version in a separate "prep for merge" commit. Resolve conflicts on the formatted file, then re-minify after merge. Add a `.gitattributes` rule: `*.json diff=json` with a custom JSON diff driver | Minified files are unmergable. Git works on lines, and a 1-line file has one line to conflict on. Always reformat auto-generated artifacts before they enter a branch where merge conflicts are expected. |
| Three-way merge shows "BASE" as empty because `git merge-base` returns the wrong ancestor | One branch was rebased onto main but never force-pushed. The other branch was rebased onto an older commit and squashed. Their histories share no common ancestor because the rebase rewrote the commit hashes. Git falls back to an empty-tree merge base — every single line in both branches appears as "added" | Find the true common ancestor: `git log --all --oneline --graph | head -80` and visually identify where the branches diverged. Use `git merge-file` with an explicit base: extract the ancestor file with `git show <ancestor-sha>:<path>`. Document the true merge base in the merge commit message | Rebase rewrites history, including the merge base. When both branches are rebased independently, Git can't find the common ancestor. The consequence is catastrophic: every line in every file becomes a conflict. Never rebase both sides of a pending merge. |
| Resolving conflicts for 2 hours, then `git merge --continue` fails with "fatal: you have not concluded your merge" | A file was resolved and `git add`-ed, but the file still had merge conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`) somewhere below the visible fold. The markers were in a JSDoc comment at line 847 — not visible without scrolling | Before `git add`: `grep -rn "^<\{7\}\|^=\{7\}\|^>\{7\}" .` to scan for remaining conflict markers. CI should block any PR with `<<<<<<<` in tracked files. Add a `pre-commit` hook: `git diff --cached | grep -E '^\+.*<<<<<<<' && exit 1` | Merged files with lingering conflict markers pass `git add` and produce syntactically invalid code. Always grep for markers before staging. A CI check catches them, but finding the missed hunk post-merge requires re-reading every file. |
| `git rebase --continue` asks for a commit message — the message is the wrong one from 5 commits ago | During a rebase, one commit applied cleanly (no conflict) and Git auto-continued past it. A later commit conflicted, was resolved, and `rebase --continue` presents the commit message from the auto-resolved commit, not the resolved one. The wrong message gets attached to the resolution | Run `git rebase --edit-todo` and verify the sequence of commits before continuing. Use `git log --oneline HEAD..REBASE_HEAD` to see which commits are pending. For long rebases, prefix commit messages with `[REBASE]` temporarily to make message attribution errors obvious | `rebase --continue` doesn't tell you which commit's message you're editing. If auto-resolution skipped a commit, the message index is off by one. Always verify the commit subject matches the diff in the rebase-todo. |
| Binary file conflict — a `.png` or `.pdf` changed in both branches with no way to visually diff | Two designers updated the same logo file independently. Git can't merge binary files — it flags the entire file as conflicted and offers "ours" or "theirs" as the only resolution. There's no way to see which pixels changed | Use `git checkout --theirs -- logo.png && git checkout --ours -- logo-v2.png` to extract both versions and diff visually. For non-image binaries: `git show OURS:file.pdf > ours.pdf && git show THEIRS:file.pdf > theirs.pdf && diff-pdf ours.pdf theirs.pdf`. Add `*.png merge=binary-keep-both` to `.gitattributes` to auto-duplicate conflicting binaries | Git can't diff binary files — resolution becomes a binary choice. Always extract both versions to named files for external comparison. For frequently-changing binaries (logos, diagrams), keep source files (SVG, Figma) versioned and treat binaries as build artifacts. |

## Best Practices
<!-- STANDARD: 3min -->

1. **Trace intent before touching a single conflict marker.** Run `git log --oneline --all --graph` to understand what each branch was trying to accomplish. Read the PR descriptions and commit messages for both sides. Document the intent in the merge commit message. Conflict resolution without intent tracing produces code that compiles but is semantically wrong.

2. **Resolve conflicts hunk-by-hunk with verification between each.** Resolve one conflict hunk, save, run the build and relevant tests. If green, move to the next hunk. If red, you know exactly which resolution caused the failure. Batch resolution — resolving all 15 conflicts then testing — means 2 hours of unwinding to find which one broke.

3. **Use a three-way merge tool, not a side-by-side diff.** Tools like `meld`, `kdiff3`, or VS Code's three-way merge show the common ancestor alongside both branches. This reveals what each side changed relative to the original — essential for understanding whether the conflict is additive (both sides added different features) or contradictory (one side fixed what the other refactored).

4. **Classify each conflict before choosing a resolution strategy.** Syntactic conflicts (same line edited differently) are resolved with a merge tool. Semantic conflicts (both branches compile but produce contradictory behavior) require reading both implementations and possibly rewriting. Structural conflicts (file rename, directory move) need `git mv` awareness. Each type demands a different strategy.

5. **Run the full test suite locally before pushing the merge.** CI is for verification, not discovery. If your merge breaks CI, you've blocked the team. Run `git merge --no-commit` followed by the full test suite. Only push when all tests pass locally. For large merges (>20 files), also run integration and E2E tests locally.

6. **Write merge commit messages that explain the resolution, not just "merge branch X."** Document: which conflicts appeared, which strategy was used for each, and any design decisions made during resolution. This is the decision log for future investigators. A merge commit that says "fixed merge conflicts" is useless when someone asks "why does auth now depend on the billing module?"

7. **Detect semantic conflicts that Git cannot see.** Two branches can merge cleanly but produce broken behavior: one adds a null check, the other removes the code that could produce null. Use `git diff A...B` (triple-dot) to see what changed on the merged branch since the common ancestor. Run integration tests that exercise both branches' changes together.

8. **Treat `git merge --abort` as the last resort, not the first reflex.** Aborting discards every resolved hunk — 2 hours of careful work gone. Before aborting: save a patch file (`git diff > /tmp/merge-progress.patch`), document which hunks are resolved in the state log, and only abort if you've identified a fundamental incompatibility that requires branch restructuring.

9. **Establish binary file merge protocols before they happen.** Git cannot meaningfully diff binaries (`.psd`, `.sqlite`, `.xlsx`). Establish a protocol: design files use "newest timestamp wins," databases require manual reconciliation, ML artifacts use DVC with content hashes. Document the protocol in CONTRIBUTING.md. Without one, each binary conflict becomes an ad-hoc negotiation at merge time.

10. **Add architecture-boundary checks to your merge verification.** A merge that compiles and passes tests can still violate architectural constraints (a pure-logic package suddenly depends on a database driver). Run `dependency-cruiser` or `eslint-plugin-boundaries` during merge verification. If the merge introduces a new cross-package dependency, flag it for architectural review before pushing.

## Cross-Skill Coordination
<!-- STANDARD: 3min -->

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

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `cloud-architect` | Infrastructure design, networking, IAM, cost model | Before provisioning infrastructure or designing deployment pipelines |
| `ci-cd-builder` | Pipeline design, build optimization, deployment strategies | Before designing CI/CD workflows |

## Proactive Triggers
<!-- STANDARD: 3min -->

| Trigger | Detection | Action |
|---------|----------|--------|
| **Mid-merge state** | `.git/MERGE_HEAD` exists | "You have an in-progress merge. I'll inventory the conflicts and begin resolution." |
| **Mid-rebase state** | `.git/rebase-apply` or `.git/rebase-merge` exists | "You have an in-progress rebase. I'll show the conflict inventory first." |
| **Conflict markers in files** | `grep -r '<<<<<<<' --include='*.ts' --include='*.js' .` finds markers | "I found conflict markers in [N] files. Let me trace intent for each hunk." |
| **`git status` shows `both modified`** | `git status --porcelain \| grep '^UU'` | "There are unmerged files. Let me inventory the conflicts." |
| **Merge conflict on PR** | GitHub PR shows "This branch has conflicts" | "The PR has conflicts with the base branch. I'll resolve them locally and push." |
| **User enters a merge/rebase that fails** | `git merge` or `git rebase` exits non-zero with conflict message | Intercept: "The operation paused with conflicts. I'll take over resolution." |
| **Semantic conflict detected post-merge** | Tests fail after clean merge; or logic inspection finds contradictions | "The merge succeeded textually but produced a semantic conflict. I'll re-examine the merged code." |

## State Log
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.


## How the State Log Works
<!-- STANDARD: 3min -->
<!-- AGENT: Read this before starting work, update after each phase -->

1. **On session start:** Check `.copilot/session-state/decision-ledger.json` for any prior decisions relevant to this domain. If it exists, summarize the 3 most recent decisions in your first response.
2. **After each major decision:** Append to the ledger:

   ```json
   {
     "timestamp": "ISO-8601",
     "skill": "merge-conflict-resolver",
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


## State Log Schema
<!-- STANDARD: 3min -->

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


## Anti-Drift Check
<!-- STANDARD: 3min -->
<!-- AGENT: Run this check at the start of each new phase -->

Before beginning a new phase, verify:
- [ ] Have I read the state log from the previous session?
- [ ] Do any prior decisions constrain what I'm about to do?
- [ ] Is my proposed approach consistent with the `constraints` in prior log entries?
- [ ] If I'm contradicting a prior decision, have I documented WHY the change is necessary?

## Production Checklist **(STANDARD)**
<!-- STANDARD: 3min -->

- [ ] **[MC-01]** Conflict inventory captured: `git diff --name-only --diff-filter=U` lists all conflicted files with hunk counts; resolution order documented (shared utilities first, then consumers)
- [ ] **[MC-02]** Intent traced for both sides of every conflict: `git log --oneline --all --graph` reviewed; PR descriptions and commit messages read; intent documented in merge commit or state log
- [ ] **[MC-03]** Conflict classification complete before resolution: each conflict tagged as syntactic, semantic, or structural; resolution strategy chosen per classification
- [ ] **[MC-04]** Three-way merge tool configured and used (meld, kdiff3, or VS Code three-way); side-by-side diff with common ancestor visible
- [ ] **[MC-05]** Hunk-by-hunk resolution with verification: resolve one conflict → save → build → run relevant tests → green before moving to next hunk
- [ ] **[MC-06]** Full test suite passes locally before push: unit + integration + relevant E2E tests; CI is for verification, not discovery
- [ ] **[MC-07]** Architecture-boundary checks pass: `dependency-cruiser` or equivalent confirms no new cross-package dependencies introduced by the merge
- [ ] **[MC-08]** Semantic conflict detection exercised: integration tests that specifically exercise both branches' changes together pass
- [ ] **[MC-09]** Binary file merge protocol followed: design files use "newest timestamp wins," databases reconciled manually, ML artifacts use DVC content hashes
- [ ] **[MC-10]** Merge commit message documents: conflicts encountered, strategies used per conflict, design decisions made during resolution; not "fixed merge conflicts"
- [ ] **[MC-11]** No conflict markers remain in any tracked file: `grep -r "<<<<<<<" .` returns empty; verification script run
- [ ] **[MC-12]** Submodule conflicts resolved with security-awareness: CHANGELOG diffed between SHAs; security patches prioritized; CI check confirms resolved SHA is not older than main minus security commits
- [ ] **[MC-13]** Pre-merge checklist completed: branch owners notified for design-level conflicts, extract-to-shared decisions have consensus, `git merge --abort` considered only as last resort with progress saved as patch
- [ ] **[MC-14]** Post-merge verification: CI pipeline green after push, deployment smoke tests pass, monitoring dashboards show no regression in error rates or latency

## What Good Looks Like
<!-- STANDARD: 3min -->

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
<!-- STANDARD: 3min -->


## Exercise 1: Intent Tracing Drill (15 min)
<!-- STANDARD: 3min -->
Take a merged PR with known conflicts. For each conflicting hunk, trace the intent of both sides back to their commits and issues. Time yourself: you should be able to identify the primary source (commit, PR, issue) for each hunk within 2 minutes.


## Exercise 2: Strategy Selection Speedrun (10 min)
<!-- STANDARD: 3min -->
Given 10 conflict scenarios (description of OURS vs THEIRS changes), select the correct resolution strategy (accept-ours, accept-theirs, manual-merge, extract-to-shared) within 30 seconds each. Check against expert answers.


## Exercise 3: Semantic Conflict Detection (20 min)
<!-- STANDARD: 3min -->
Review 5 merge commits that introduced bugs despite clean textual merges. For each, identify the semantic conflict that testing caught. Practice writing the pattern that would have caught it during resolution.


## Exercise 4: Multi-Hunk Dependency Resolution (30 min)
<!-- STANDARD: 3min -->
Set up a scenario with 5+ interrelated conflict hunks across 3 files. Resolve them in dependency order, verifying after each. Compare your resolution order to the optimal dependency graph.


## Exercise 5: The No-Abort Challenge (45 min)
<!-- STANDARD: 3min -->
A colleague creates a deliberately difficult merge conflict (10+ hunks, semantic traps). Resolve it from inventory to completion without using `--abort`. Time yourself. Review each resolution decision afterward.

## Anti-Hallucination
<!-- STANDARD: 3min -->

| Rationalization | Reality |
|---|---|
| "`git merge --abort` and restart — it's cleaner than working through the mess." | Every resolved hunk is lost. 2 hours of careful conflict resolution = $300 in direct time wasted, plus $14,700+ in delayed feature delivery if the merge was on a release critical path. Abort should be the last resort, not the first reflex. |
| "Just `git checkout --ours` on everything — we'll review the other side's changes later." | Blindly accepting "ours" discards the other branch's intent entirely. If their side fixed a critical bug or implemented a dependency your team needs, you've reintroduced the bug or lost the feature. $5K-$50,000 per incident. |
| "The merge looks clean — no conflicts reported, so nothing to worry about." | Git only detects textual conflicts, not semantic ones. Two branches that rename the same function to different names, or add incompatible assumptions about a data structure, merge cleanly and fail at runtime. $10K-$30K in post-merge debugging. |
| "I don't need to understand what the other branch was trying to do — just resolve the markers." | Mechanical conflict resolution without understanding intent produces syntactically valid, semantically broken code. $5K-$25K in production bugs traced back to merge-resolution decisions made without context. |
| "We'll handle the merge conflicts during the release window — there's not that many." | Late-stage merge under time pressure forces rushed decisions. Quality of resolution drops, testing gets skipped, and regressions slip through. $15K-$40K in post-release hotfixes and rollbacks that a calm, pre-window merge would have avoided. |

## Anti-Patterns
<!-- STANDARD: 3min -->

### Anti-Pattern: The --abort reflex
**What it looks like:** `git merge --abort` or `git rebase --abort` used as the first response when conflicts get messy. "It's cleaner to restart than work through this."
**Why it fails:** Every resolved hunk is lost. 2 hours of careful work = $300 in direct time, plus $14,700+ in delayed feature delivery if the merge was on a release critical path. Abort trains the brain that conflict resolution is disposable.
**Do this instead:** Before aborting: save a patch file (`git diff > merge-progress.patch`), document resolved hunks in the state log, escalate within the team. Only abort when a fundamental incompatibility requires branch restructuring — not when you feel overwhelmed.

### Anti-Pattern: Accepting "mine" without reading "theirs"
**What it looks like:** `git checkout --ours` applied to every conflicted file. "We'll review their changes later." The merge completes but the other branch's intent is discarded.
**Why it fails:** If the other side fixed a critical bug or implemented a dependency your team needs, you've reintroduced the bug or lost the feature. $5K-$50K per incident. Blind ours-resolution is the fastest path to a broken merge.
**Do this instead:** For each conflict, read both sides completely. Use a three-way merge tool to see the common ancestor. If ours is correct, document WHY in the merge commit — don't just assume.

### Anti-Pattern: Semantic conflicts that merge cleanly
**What it looks like:** Git reports no conflicts, merge completes cleanly, CI passes. But one branch added a null check while the other removed the code path that could produce null. The bug reaches production silently.
**Why it fails:** $20K-$100K per incident. Git only detects textual conflicts, not behavioral ones. The most expensive merges are the ones with zero conflict markers.
**Do this instead:** Run `git diff A...B` (triple-dot) to see what changed since the common ancestor. Run integration tests that exercise both branches' changes together. Build semantic conflict detection into CI: flag merges where both branches touch the same function.

### Anti-Pattern: Batching conflict resolution without per-hunk verification
**What it looks like:** Resolve all 15 conflicts at once, save everything, then run the build. Build fails. Now binary-search through 15 resolutions to find the culprit.
**Why it fails:** $3K-$10K in wasted debugging time. Each wrong guess costs 10-15 minutes. With hunk-by-hunk verification, you'd catch the issue immediately — 2 minutes of rework instead of 2 hours.
**Do this instead:** Resolve one hunk → save → build → run relevant tests → green? Move to next hunk. Red? Fix immediately. Never resolve more than one hunk without verification.

### Anti-Pattern: No verification between resolutions
**What it looks like:** Skipping the build-and-test step between hunk resolutions because "it's just a small change to a config file." Three hunks later, the build fails — and now you don't know which hunk broke it.
**Why it fails:** $8K in wasted debugging time per incident. If the unverified merge reaches CI and breaks the pipeline for the team: $25K in blocked productivity for the entire engineering org.
**Do this instead:** Verify after every hunk, no exceptions. "It's just a small change" is exactly when verification is fastest and most valuable. Skip verification only when you're willing to binary-search through your own work.

### Anti-Pattern: Lost intent context
**What it looks like:** Conflicts resolved mechanically — markers removed, code compiles, merge pushed. Two months later someone asks "why did we resolve the auth conflict this way?" Nobody knows. The decision died with the resolver.
**Why it fails:** $10K to re-investigate the original intent. If the wrong resolution causes a security vulnerability: $30K in audit, remediation, and compliance fallout.
**Do this instead:** Document intent and resolution rationale in the merge commit message. Template: "Conflict in [file]: [branch A] was [intent], [branch B] was [intent]. Resolution: [strategy] because [reasoning]." This is the decision log for future investigators.

### Anti-Pattern: Extract-to-shared without consensus
**What it looks like:** During conflict resolution, you notice both branches added similar utilities. You extract a shared module to avoid duplication, merge, and push. Neither original author was consulted.
**Why it fails:** The new abstraction doesn't fit both use cases cleanly. One team works around it, introducing technical debt. The abstraction must be refactored or reverted. $15K-$40K in rework across both teams.
**Do this instead:** Extract-to-shared is a design decision, not a merge tactic. File a follow-up issue. Defer the extraction to a separate PR with both original authors as reviewers. In the merge, keep both implementations and add a TODO linking to the extraction issue.

### Anti-Pattern: Binary file conflicts without a resolution protocol
**What it looks like:** Two designers commit different versions of `hero-banner.psd` or two data engineers update `seed-data.sqlite` on parallel branches. Git offers no meaningful diff — just "Binary files differ." Both contributors guess.
**Why it fails:** $10K-$60K per incident. Wrong binary ships to production — corrupted SQLite with stale pricing data processes 1,200 orders at incorrect amounts over 4 hours.
**Do this instead:** Store binary assets in content-addressable storage (S3 with versioning, DVC for ML artifacts). Commit only content hashes in Git. Establish protocol: newest timestamp wins for design files, manual reconciliation for databases. Pre-commit hook warns when binaries >1MB are staged without hash file.

### Anti-Pattern: Merge that compiles but violates architectural boundaries
**What it looks like:** Conflict in `packages/auth` resolved by accepting both branches' changes — one added a database import, the other added Redis. Code compiles, tests pass. But now auth (a pure-logic package) has two infrastructure dependencies.
**Why it fails:** $20K-$80K in architectural debt remediation. Three months later, `packages/ui` test fails because it transitively pulls in PostgreSQL driver through auth — a driver that doesn't compile on macOS CI. Two weeks to untangle.
**Do this instead:** Run architecture-boundary checks during merge verification (`dependency-cruiser`, `eslint-plugin-boundaries`). If merge introduces a new cross-package dependency, flag for architectural review before accepting. Maintain a dependency graph as a build artifact.

### Anti-Pattern: Submodule conflicts that silently revert security patches
**What it looks like:** Two branches update the same submodule to different SHAs — one for a security patch (v2.1.1), the other for a feature release (v2.2.0). Resolver picks the feature branch SHA without noticing the security patch reversion.
**Why it fails:** $8K-$25K per incident. The vulnerability goes live for 11 days before a scanner catches it. Security team spends 80 engineering-hours at $200/hr investigating the exposure window.
**Do this instead:** Diff CHANGELOG between the two SHAs. Prioritize the one containing security patches. Add CI check: fail if resolved submodule SHA is older than main minus security-related commits. Enable Dependabot/Renovate on submodule references.

## Verification
<!-- STANDARD: 3min -->

| # | Complete when... | Verify |
|---|-----------------|--------|
| ☐ | Complete when No conflict markers remain in any tracked file — zero `<<<<<<<`, `=======`, or `>>>>>>>` in the working tree | `grep -r '<<<<<<<' $(git ls-files) && echo "FAIL" \|\| echo "PASS"` |
| ☐ | Complete when All files staged after resolution — `git status` shows only resolved files staged, no unstaged diffs from resolution work | `git diff --name-only --cached` lists all resolved files; `git diff --name-only` is empty |
| ☐ | Complete when Build succeeds with resolved code — `make build` or equivalent passes on first attempt | CI build green; no compilation errors or missing imports from incomplete resolution |
| ☐ | Complete when Tests pass for both sides of the conflict — test suites from both merged branches pass against resolved code | Run test suite from branch A and branch B; both pass with zero regressions |
| ☐ | Complete when Intent of both changes preserved — resolution doesn't silently drop functionality from either side | Code review confirms each original commit's intent is reflected in the resolution; resolution log documents trade-offs |
| ☐ | Complete when Resolution log written — documents: conflict source (branch/PR), intent of each side, resolution strategy, why this strategy was chosen, and verification steps taken | Resolution log committed alongside merge; references both original PR/commit SHAs |
| ☐ | Complete when Semantic conflicts checked — no cross-hunk dependencies broken; renamed/moved symbols resolved; submodule SHAs not regressed | Cross-reference all changed symbols; verify no function call targets moved/deleted in other hunks |
| ☐ | Complete when CI pipeline green — all gates pass: lint, type-check, unit tests, integration tests, build | CI dashboard shows all checks passing on the merge commit |

## Verification Guardrails
<!-- STANDARD: 3min -->

Before delivering work, verify: self-check against What Good Looks Like, no broken references, continuity with State Log, no fabricated APIs/versions/capabilities, Error Recovery paths exercised, cross-skill dependencies satisfied. If any fail, revise before delivering.

## References
<!-- STANDARD: 3min -->

- [references/hunk-analysis.md](references/hunk-analysis.md) — Detailed methodology for analyzing individual conflict hunks, classifying complexity, and identifying dependency relationships between hunks
- [references/intent-tracing.md](references/intent-tracing.md) — Step-by-step guide to tracing each side of a conflict back to its commit, PR, and issue with source hierarchy prioritization
- [references/resolution-strategies.md](references/resolution-strategies.md) — Deep dive into each resolution strategy with examples, risk profiles, and when each is most appropriate
- [references/source-identification.md](references/source-identification.md) — Techniques for identifying the primary source of a change: git blame, log searching, PR/issue linking, and author context
- [references/conflict-patterns.md](references/conflict-patterns.md) — Catalog of conflict patterns (textual, structural, semantic) with recognition heuristics and resolution templates
- [references/verification-gates.md](references/verification-gates.md) — Per-hunk and per-phase verification gates: build checks, test selection, semantic validation, and CI pipeline integration
- [references/extract-to-shared.md](references/extract-to-shared.md) — Decision framework and workflow for the extract-to-shared resolution strategy with abstraction design guidelines
- [references/resolution-documentation.md](references/resolution-documentation.md) — Template and best practices for the resolution log: what to record, format conventions, and long-term maintenance
