# Legacy Migration

<!-- DEEP: 5+min -- the isolated reformat, .git-blame-ignore-revs, and branch coordination -->

## The problem

A codebase that has never been formatted, and a formatter that would change most of it.

Running the formatter produces a diff touching tens of thousands of lines. If that lands inside functional work, three things break at once:

| What breaks | Why it matters |
|---|---|
| **Review** | nobody can review 40,000 changed lines; the real change hides in the noise |
| **`git blame`** | every line now points at the reformat, and history becomes useless |
| **Open branches** | every in-flight branch conflicts on nearly every file |

This is R3, and the mitigation is isolation plus a blame-ignore entry.

## The procedure

```text
1. FREEZE        pick a quiet window; announce it in advance
2. ISOLATE       a dedicated commit that changes ONLY formatting
                 ├── no functional change, no renames, no dependency bumps
                 └── verify: the formatter's own check passes, nothing else changed
3. RECORD        add that commit's SHA to .git-blame-ignore-revs
4. CONFIGURE     git blame to use it (locally and in the repository)
5. LAND          merge it; announce the SHA
6. REBASE        every open branch rebases ONCE, immediately
7. ENFORCE       turn on the CI gate AFTER the reformat is merged, not before
```

**Step 7 is the one teams get wrong.** Enabling the gate before the reformat means every branch fails on unrelated files, which is how the gate gets disabled in week one.

## The formatting-only commit, verified

The commit must change nothing functional. Verify it:

```bash
# 1. The formatter agrees — there is nothing left to change
make fmt-check          # must exit 0

# 2. Nothing but formatting changed.
#    A whitespace-insensitive diff should be EMPTY:
git diff -w HEAD~1 HEAD -- '*.go'      # -w ignores whitespace
git diff -w HEAD~1 HEAD -- '*.py'

# 3. No renames, no mode changes crept in:
git diff --summary HEAD~1 HEAD | grep -E "rename|mode change" || echo "clean"

# 4. The change is confined to source files, not lockfiles or configs:
git diff --name-only HEAD~1 HEAD | grep -E "lock|package.json|go.sum" || echo "clean"
```

Checks 2 and 4 are the ones that catch a reformat that quietly included something else.

## `.git-blame-ignore-revs`

The file that makes blame usable after a reformat.

```text
# .git-blame-ignore-revs
# Formatting-only commits. git blame skips these and attributes the line
# to the change that actually wrote it.
#
# To use: git config blame.ignoreRevsFile .git-blame-ignore-revs
#   (and set it in the repo's git config so CI and everyone's tooling agrees)

# 2026-09-13 — repo-wide Prettier adoption
a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0

# 2026-09-20 — ruff format on the services package
b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1
```

Three requirements:

| Requirement | Detail |
|---|---|
| One SHA per line | comments with `#`, blank lines ignored |
| Full 40-character SHA | abbreviated SHAs may not be matched |
| A dated comment above each | so a reader knows what the reformat was |

Configure it once, in the repository, so nobody has to remember:

```bash
# Local: everyone
git config blame.ignoreRevsFile .git-blame-ignore-revs

# Repository-wide (so a clone inherits it)
git config --local blame.ignoreRevsFile .git-blame-ignore-revs
# …and document the one command in CONTRIBUTING, since git config is not cloned
```

**Verify it works** — this is the deliverable, not the file's existence:

```bash
# Pick a line that existed BEFORE the reformat, and check who blame names.
git blame -L <line>,<line> <file>
#   → must name the original author and the original commit,
#     NOT the reformat commit
```

## Coordinating open branches

The rebase is unavoidable; make it cheap and predictable.

| Practice | Effect |
|---|---|
| Announce a date and a freeze window | branches land or wait deliberately |
| Land when branch count is lowest | fewer conflicts to resolve |
| Provide a one-command rebase | nobody invents their own approach |
| Offer to do it for in-flight branches | a single expert rebasing is faster than ten people learning |
| Never reformat *and* rebase in one step | isolate, so a conflict is obviously formatting |

**The one-command rebase:**

```bash
# On each open branch
git fetch origin
git rebase origin/main          # resolves once, in the formatting-only commit
make fmt                        # belt and braces: re-run the formatter on the result
git diff --quiet || git commit -am "style: apply formatter after rebase"
```

Because the reformat commit is formatting-only, the conflicts it produces are almost always resolvable by "take the formatter's output" — which is a mechanical decision, not a judgement call.

## The alternative that avoids the big-bang reformat

For very large or very active codebases, incremental adoption avoids the freeze entirely:

| Approach | How |
|---|---|
| **Directory-by-directory** | format one package per PR; gate that package |
| **File-by-file on touch** | format only files a change already touches; enforce via "changed files must be formatted" |
| **Baseline linting** | gate on *no new findings*, which needs no reformat at all for the lint side |
| **Pre-commit on changed files only** | the gate applies to new work while old code waits |

```yaml
# "Changed files must be formatted" — no big-bang reformat needed
- name: Format changed files
  run: |
    files=$(git diff --name-only --diff-filter=ACMR origin/main...HEAD)
    [ -z "$files" ] || npx prettier --check $files
```

**The trade:** incremental adoption never requires a freeze, but it leaves the codebase inconsistent for months and the "unformatted" state persists in files nobody touches. Choose it when the freeze would be more expensive than the inconsistency.

## Choosing an approach

```text
How large is the codebase, and how many branches are typically open?
├── Small, few branches → one isolated reformat; ignore it in blame; done
├── Large but quiet     → one isolated reformat, with an announced freeze
└── Large and very active ↓
    Is a freeze of a few hours affordable?
    ├── Yes → a scheduled reformat window (cleanest end state)
    └── No  → INCREMENTAL: format changed files only, and gate on that
              ├── Accept the inconsistent state for a period, with an end date
              └── Track progress: what fraction of files are formatted
    Either way:
    ├── Never mix a reformat with functional changes (R3)
    └── Record every formatting commit in .git-blame-ignore-revs
```

## Checklist

- [ ] The reformat is a dedicated, formatting-only commit (R3)
- [ ] Nothing functional changed — verified with a whitespace-insensitive diff
- [ ] No lockfiles, configs or renames crept into the reformat commit
- [ ] The commit SHA is in `.git-blame-ignore-revs`, with a dated comment
- [ ] `blame.ignoreRevsFile` is configured, and the one-time command is documented
- [ ] `git blame` on a pre-reformat line names the original author (verified)
- [ ] Open branches were announced, and each rebased once
- [ ] The CI gate was enabled **after** the reformat merged, not before
- [ ] If incremental, progress is tracked against an end date
- [ ] The reformat commit is announced so nobody mistakes it for a functional change
