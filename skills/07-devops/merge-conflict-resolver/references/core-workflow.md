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
