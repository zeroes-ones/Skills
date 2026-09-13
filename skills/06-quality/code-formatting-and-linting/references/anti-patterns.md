# Anti-Patterns

<!-- STANDARD: 3min -- the style anti-pattern catalogue with detection heuristics -->

## 1. Review-enforced style

**Symptom:** the same formatting comment appears across reviews; the style guide has a checklist section.
**Cause:** the convention lives in a document, not a tool (R1).
**Detection:** read the review comment history for "indent", "whitespace", "quote", "line length".

**Fix:** automate it, then delete it from the review checklist.

## 2. Hook-only enforcement

**Symptom:** unformatted code on the main branch despite a hook existing.
**Cause:** authority placed in a skippable layer (R2).
**Detection:** is there a CI job that runs the formatter's check mode? If not, enforcement is a convenience.

```bash
grep -rn "prettier\|eslint\|swiftlint\|ktlint\|ruff" .github/workflows/ 2>/dev/null | head
# empty → the hook is the only enforcement
```

**Fix:** add the CI check as the authority; keep the hook for speed.

## 3. Two authorities

**Symptom:** the formatter and a style document disagree; contributors ask which wins.
**Cause:** the policy was not reduced to one source.
**Detection:** does the style document describe the tool's output, or assert independent rules?

**Fix:** one authority. The document describes the tool's output and links to the config.

## 4. Unisolated reformat

**Symptom:** a single commit touching 40,000 lines; `git blame` points at it everywhere.
**Cause:** the reformat was not dedicated and not blame-ignored (R3).
**Detection:** is the reformat commit recorded in `.git-blame-ignore-revs`?

```bash
test -f .git-blame-ignore-revs && wc -l .git-blame-ignore-revs || echo "MISSING"
```

**Fix:** isolate the commit, record the SHA, and verify blame names the original author.

## 5. Reformat inside a feature diff

**Symptom:** a feature PR with thousands of changed lines; reviewers cannot see the feature.
**Cause:** the formatter ran across the repo during functional work (R3).
**Detection:** does the diff contain both formatting and logic changes?

**Fix:** separate commits; land the reformat first.

## 6. Bare suppression

**Symptom:** `// eslint-disable`, `# noqa`, `@Suppress("ALL")` with no rule and no reason.
**Cause:** the suppression was added to unblock, not to except (R4).
**Detection:**

```bash
grep -rnE "eslint-disable$|# noqa$|nolint$|swiftlint:disable$" src/ | head
```

**Fix:** name the rule, add the reason, narrow the scope.

## 7. Global rule disable for one site

**Symptom:** a rule turned off in config because one file needed an exception.
**Cause:** the site exception was escalated to a policy change.
**Detection:** compare the config's disabled rules against the suppressions in source.

**Fix:** scope the suppression; only disable a rule globally with a recorded policy reason.

## 8. Suppression creep

**Symptom:** a rising suppression count nobody watches.
**Cause:** no visible metric and no budget (R4).
**Detection:** run the suppression report twice, a month apart.

**Fix:** report the count per language in CI, with a budget and a review cadence.

## 9. Security rule suppressed to ship

**Symptom:** a security-relevant rule disabled in config or at a site to make a release.
**Cause:** the policy did not carve out security rules.
**Detection:** grep the config and the source for suppressions of injection/secret/deserialisation rules.

**Fix:** revert; fix the finding or escalate to `appsec-engineer`. Never suppress to ship.

## 10. One tool stretched across languages

**Symptom:** the linter reports odd findings in a language it does not really own; those findings get suppressed.
**Cause:** a single-tool decision across a polyglot repo (R5).
**Detection:** does the tool's documentation list the language as supported, or merely parse it?

**Fix:** per-language tools; unify the policy, not the tool.

## 11. Overlapping formatters

**Symptom:** every save produces a diff because two formatters disagree on the same file.
**Cause:** two tools configured for one scope (R5).
**Detection:** check the ignore scope of each formatter; overlap is the defect.

**Fix:** one formatter per language; remove the overlap or narrow the scopes.

## 12. Generated files in scope

**Symptom:** the gate reports files nobody wrote and nobody may edit.
**Cause:** no exclusion, or an exclusion that does not apply (R6).
**Detection:** generate a file into a supposedly excluded path and run the check.

**Fix:** exclude by path and header marker, and verify it applies.

## 13. Unpinned formatter version

**Symptom:** a dependency bump reformats the whole repo unexpectedly.
**Cause:** the formatter version floats.
**Detection:** is the version in a lockfile or a pinned devDependency?

**Fix:** pin it; upgrade deliberately, with the reformat isolated.

## 14. CI and local disagree

**Symptom:** a clean local check, a failing CI check.
**Cause:** different tool versions, or a different config resolution path.
**Detection:** print the resolved config and version in both environments.

**Fix:** pin the version; resolve the config from the repository root.

## 15. Gate enabled with no baseline

**Symptom:** thousands of findings on day one; the release is blocked or the gate is disabled.
**Cause:** the gate was turned on for legacy code without a baseline.
**Detection:** was the finding count measured before enabling the gate?

**Fix:** fix the autofixable set, then gate on no-new-findings.

## 16. Slow gate

**Symptom:** the style check takes ten minutes; people push with `--no-verify` and batch changes.
**Cause:** whole-repo checks on every PR, no caching, no scoping.
**Detection:** time the job on a typical PR.

**Fix:** scope to changed files, cache, split jobs, run the full check on main.

## 17. Renamed CI job silently unrequired

**Symptom:** style stops gating merges; unformatted code lands.
**Cause:** branch protection references the job name, and the job was renamed.
**Detection:** do the required check names in branch protection still match the workflow's job names?

**Fix:** update the branch protection rule when renaming a job.

## 18. Bots exempted

**Symptom:** automated commits carry unformatted code; the standard is not universal.
**Cause:** the bot was exempted to avoid noise.
**Detection:** does a dependency-bot PR run the style check?

**Fix:** subject automation to the same check; format the bot's output.

## Detection sweep

```bash
SRC="${1:-.}"

echo "== .editorconfig present? =="
test -f .editorconfig && echo "  yes" || echo "  NONE — no portable intent layer"

echo "== CI runs a formatting check? =="
grep -rnE "prettier --check|fmt-check|swiftformat --lint|dart format --output=none|ruf+ format --check" .github/workflows/ 2>/dev/null | head -3 || echo "  NONE — enforcement may be hook-only"

echo "== CI runs a lint gate? =="
grep -rnE "eslint|swiftlint|ktlint|detekt|clippy|golangci|ruff check|shellcheck|clang-tidy" .github/workflows/ 2>/dev/null | head -3 || echo "  NONE"

echo "== bare suppressions (no rule, no reason) =="
grep -rnE "eslint-disable[[:space:]]*$|# ?noqa[[:space:]]*$|nolint[[:space:]]*$|swiftlint:disable[[:space:]]*$" "$SRC" 2>/dev/null | head -5 || echo "  none found"

echo "== suppression total =="
grep -rInE "eslint-disable|noqa|nolint|@Suppress|swiftlint:disable|allow\(clippy" "$SRC" 2>/dev/null | wc -l | xargs echo "  count:"

echo "== blame-ignore file present? =="
test -f .git-blame-ignore-revs && echo "  yes" || echo "  NONE — a past reformat is not ignored"

echo "== generated/vendored excluded? =="
for f in .prettierignore .eslintignore; do test -f "$f" && echo "  $f: $(wc -l < $f) entries"; done
find . -maxdepth 2 -name "vendor" -o -maxdepth 2 -name "dist" 2>/dev/null | head -3

echo "== overlapping formatters? =="
ls .prettierrc* biome.json .clang-format rustfmt.toml 2>/dev/null | tr '\n' ' '; echo

echo "== is the check scoped to changed files? =="
grep -rnE "git diff --name-only|--diff-filter" .github/workflows/ 2>/dev/null | head -2 || echo "  no — full-repo check on every PR (may be slow)"
```

Interpretation: **a `.editorconfig`-less repo has no portable intent**, and **CI with no formatting check** means enforcement is a convenience. **Bare suppressions** and **no `.git-blame-ignore-revs`** are standalone findings — the first is an unbounded exception, the second means history is already damaged if a reformat happened.
