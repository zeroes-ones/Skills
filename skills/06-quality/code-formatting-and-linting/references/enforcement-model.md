# Enforcement Model

<!-- DEEP: 5+min -- the format-on-write → hook → CI → branch-protection ladder, and why CI is the authority -->

## The ladder

Four layers, each catching what the previous one let through. Only the last is authoritative.

| Layer | When | Catches | Can be bypassed? |
|---|---|---|---|
| **1. Editor / format-on-save** | while typing | most issues before the developer notices | yes (the editor is misconfigured) |
| **2. Pre-commit hook** | at commit time | issues the editor missed | **yes** (`--no-verify`, fresh clone, web UI) |
| **3. CI check** | at push/PR | everything the hook missed, including bot commits | **no** — this is the authority |
| **4. Branch protection** | at merge | a failing check being merged anyway | no |

**The rule (R2):** enforcement lives at layer 3. Layers 1 and 2 exist for developer speed; layer 4 makes layer 3 binding.

## Why the hook cannot be the authority

| Reason | Detail |
|---|---|
| It is skippable | `git commit --no-verify` exists and is used under time pressure |
| It is absent in a fresh clone | hooks are not cloned; they must be installed |
| It is absent in web editors | a GitHub web edit does not run local hooks |
| Automated commits bypass it | dependency bots, generators and release scripts |
| It can be uninstalled by a tool | some package managers and IDEs manage hooks |

Any of these means the standard holds for careful developers and not for the rest — which is not a standard.

**The correct use of a hook:** fast feedback. It catches the common case in under a second, before the developer loses context. Its value is speed, not enforcement.

## Wiring CI as the authority

```yaml
# Two separate jobs, named so failures are actionable
jobs:
  format:
    steps:
      - name: Check formatting
        run: make fmt-check          # mechanical: must be clean, no exceptions

  lint:
    steps:
      - name: Lint
        run: make lint               # semantic: gate with a baseline
```

Two jobs, not one, for three reasons:

1. **The failure message is actionable.** "Formatting differs" and "three lint findings" need different responses.
2. **They can be configured differently.** Formatting may autofix in CI; the lint gate should not.
3. **They can be cached and parallelised differently.**

Then make it binding:

- Mark the checks **required** in branch protection.
- Ensure they run on **every** change, including bot PRs.
- Do not allow an admin override as routine practice.

## The autofix question

CI may **fix** formatting, because the fix is deterministic:

```yaml
# Deterministic: CI may apply it
- name: Format and commit if needed
  run: |
    make fmt
    if ! git diff --quiet; then
      git commit -am "style: apply formatter"
      git push
    fi
```

CI may **not** fix lint findings in general, because a lint fix may change behaviour. The exceptions are rules explicitly marked safe-autofix.

| Category | CI behaviour |
|---|---|
| Formatting | may autofix and push |
| Lint rules with a safe autofix | may autofix, if the set is reviewed and version-pinned |
| Lint rules without a safe autofix | must fail the build |
| Security-relevant rules | must fail the build; never autofix, never suppress |

**The trap with formatting autofix in CI:** it creates a commit nobody reviewed, and on a shared branch it can race. Prefer format-and-check on PR branches, and format-and-commit only where the branch is single-writer.

## What to check, precisely

| Check | Command shape | Fails when |
|---|---|---|
| Formatting | `fmt --check` (or `fmt` then `git diff --exit-code`) | any file differs from the formatter's output |
| Linting | `lint` (exit code) | any finding above the severity threshold |
| Lint baseline (legacy) | `lint --baseline` or a no-new-findings comparison | a new finding appears |

**The baseline check** is the pattern that makes legacy adoption possible: gate on *no new findings* rather than *zero findings*. See `legacy-migration.md`.

## Making it fast enough to survive

| Technique | Effect |
|---|---|
| Scope to changed files | the largest win on a large repo |
| Separate format and lint jobs | parallel, separately cacheable |
| Cache the tool's cache directory | significant for ESLint, ruff, ktlint |
| Exclude generated code | removes work entirely |
| Run full checks on the main branch only | full coverage without slowing every PR |

A slow gate is a gate that gets disabled. Speed is a correctness property here.

## Verifying the enforcement actually works

Do not assume; demonstrate each layer:

```text
1. Create a branch with a deliberately unformatted file.
   → CI MUST fail. If it passes, the gate is not wired.

2. Commit with `--no-verify` to skip the hook, then push.
   → CI MUST still fail. If it passes, the hook was the only enforcement.

3. Create a branch that adds a lint finding above the threshold.
   → CI MUST fail, with a message naming the rule and the file.

4. Let a dependency bot open a PR with an unformatted change.
   → CI MUST run on it. If bots bypass checks, the standard is not universal.

5. Confirm the check is REQUIRED in branch protection.
   → Attempt to merge with the check failing; it must be blocked.
```

Step 2 is the one that catches the most common misconfiguration: a repo that believes it enforces style because a hook exists.

## The editor layer

Worth configuring because it removes the problem rather than reporting it:

| Practice | Effect |
|---|---|
| Format on save, enabled by default in repo settings | developers never see the issue |
| Share the editor config (`.vscode/settings.json`) committed to the repo | one standard, not per-developer preference |
| Recommend the formatter extension in the repo | new contributors get the right tool |
| Document the one-liner to install hooks | makes layer 2 actually present |

**Note the asymmetry:** the editor layer may be opinionated (format on save), because it costs nothing when it is wrong — the CI check is what decides.

## Checklist

- [ ] CI is the authority, and the hook is described as a convenience (R2)
- [ ] Formatting and linting are separate jobs with separate failure messages
- [ ] The formatting check fails on any difference, with no exception mechanism
- [ ] The lint gate exists, with a baseline where legacy code is involved
- [ ] The checks are marked required in branch protection
- [ ] Automated commits are subject to the same checks
- [ ] CI may autofix formatting only; lint fixes are reviewed
- [ ] Security-relevant lint rules always fail the build
- [ ] Each layer's enforcement has been demonstrated by a deliberate failure
- [ ] The gate runs within a stated time budget
