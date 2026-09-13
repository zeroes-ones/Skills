# CI Integration

<!-- STANDARD: 3min -- scoping to changed files, caching the check, and keeping it fast -->

## The governing constraint

**A slow gate is a disabled gate.** If the check takes ten minutes, people route around it — they push with `--no-verify`, they batch changes, they ask for an exemption. Speed is a correctness property here, not an optimisation.

Target: under two minutes for a typical PR.

## The job shape

```yaml
name: Style

on: [pull_request, push]

jobs:
  format:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }        # needed for a changed-files diff
      - uses: actions/setup-node@v4
        with: { cache: npm }
      - run: npm ci
      - name: Check formatting
        run: npx prettier --check .

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - uses: actions/setup-node@v4
        with: { cache: npm }
      - run: npm ci
      - name: Lint
        run: npx eslint .
```

Three properties of that shape:

| Property | Why |
|---|---|
| **Two separate jobs** | formatting and linting fail differently, and are configured differently |
| **`fetch-depth: 0`** | a changed-files diff needs the full history, or it silently compares against nothing |
| **Tool cache enabled** | install time often dominates a small check |

## Scoping to changed files

The single biggest speed win on a large repository.

```yaml
- name: Format changed files only
  run: |
    BASE="${{ github.event.pull_request.base.sha || 'origin/main' }}"
    files=$(git diff --name-only --diff-filter=ACMR "$BASE"...HEAD)
    [ -z "$files" ] && exit 0
    npx prettier --check $files
```

Five details that make a changed-files check correct:

1. **`--diff-filter=ACMR`** — Added, Copied, Modified, Renamed. Excludes deletions (nothing to check) and avoids passing a deleted path.
2. **Quote the file list carefully** — paths with spaces break an unquoted expansion.
3. **Handle the empty case** — a diff with no relevant files must succeed, not fail on an empty argument list.
4. **Do not scope the *full* check away entirely** — run the complete check on the main branch, or periodically, so the untouched files are eventually covered.
5. **Scope the formatter and the linter identically** — a scoped formatter with an unscoped linter (or vice versa) produces inconsistent results.

```yaml
# The full check, on the main branch, so nothing stays uncovered forever
full-check:
  if: github.ref == 'refs/heads/main'
  steps:
    - run: npx prettier --check . && npx eslint .
```

## Caching

| Tool | What to cache | Effect |
|---|---|---|
| ESLint | `.eslintcache` (`--cache`) | large on repeated runs |
| ruff | `--cache-dir` | meaningful |
| ktlint / detekt | the Gradle cache | large |
| Prettier | nothing (fast enough) | — |
| tool dependencies | the package manager cache | install time is often the bottleneck |

```yaml
- uses: actions/setup-node@v4
  with: { cache: npm }              # dependency cache
- uses: actions/cache@v4
  with:
    path: .eslintcache
    key: eslint-${{ github.sha }}
    restore-keys: eslint-            # partial hit on the nearest prior run
```

## Running lint and format in a monorepo

Three viable shapes, chosen by repo size:

| Shape | When | Trade |
|---|---|---|
| **Single job, whole repo** | small repos | simplest; slowest |
| **Changed-files scoping** | medium, active | fast; leaves untouched files uncovered |
| **Per-package matrix** | monorepos with independent packages | parallel; more config, and a shared policy still needed |

```yaml
# Per-package matrix — parallel, and each package's own tools run in its own environment
strategy:
  matrix:
    package: [web, services, mobile]
steps:
  - run: make -C packages/${{ matrix.package }} lint
```

**The monorepo requirement:** whatever the shape, the *policy* stays single (see `../portable-policy.md`). A matrix of packages, each with its own style philosophy, is not one standard.

## Making it binding

```text
1. Mark the jobs as REQUIRED checks in branch protection.
2. Confirm they run on every PR, including from bots and forks.
3. Confirm an admin cannot merge around them as routine practice.
4. Confirm the check name in the PR matches the job name (a renamed job silently
   stops being required, because the required check no longer exists).
```

**The renamed-job trap is common and silent:** renaming a CI job removes its "required" status, because branch protection references the name. Style enforcement then quietly stops gating merges, and nobody notices until unformatted code lands.

## Failure messages

The message determines whether the failure is actionable.

```yaml
- name: Check formatting
  run: |
    if ! npx prettier --check .; then
      echo "::error::Formatting check failed. Run: npm run fmt"
      echo "Then commit the result. Do not hand-edit the formatting."
      exit 1
    fi
```

The message says **what failed**, **the one command that fixes it**, and **what not to do**. A message that just says "process exited with 1" costs every developer a minute.

## The bot problem

Automated commits — dependency bots, generators, release scripts — must pass the same check.

| Situation | Handling |
|---|---|
| A dependency bot updates a lockfile | lockfiles are excluded, so it passes (see `generated-and-vendored.md`) |
| A bot updates a source file | it must be formatted; if the bot cannot format, CI fixes and commits on the bot branch |
| A release script writes a file | the script formats its output |
| A fork PR | the check runs, but secrets/caches may be unavailable — degrade gracefully, do not skip |

**Do not exempt bots.** An exemption means the standard applies to humans and not to automation, which is exactly backwards — automation is where the drift accumulates.

## Checklist

- [ ] Format and lint are separate CI jobs
- [ ] `fetch-depth: 0` where a changed-files diff is used
- [ ] The check is scoped to changed files for PRs, with a full check on the main branch
- [ ] The empty-diff case succeeds rather than failing
- [ ] Tool caches are configured
- [ ] The check runs within a stated time budget (target: under two minutes)
- [ ] The jobs are required checks in branch protection
- [ ] The required check names still match the job names (no silent rename)
- [ ] Automated commits are subject to the same check
- [ ] Failure messages name the fix command
