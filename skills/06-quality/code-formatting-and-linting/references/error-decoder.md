# Error Decoder — Long Form

<!-- DEEP: 5+min -- the symptom catalogue in long form, with causes and fixes -->

The compressed table lives in `SKILL.md`. This file carries the full diagnosis.

## 1. The same formatting comment keeps appearing in reviews

**Symptom:** different reviewers raise the same style points; the discussion recurs on unrelated PRs.
**Mechanism:** the convention is enforced by humans, so it is applied inconsistently and only where someone notices. Each occurrence costs a review round-trip.
**Diagnosis:** grep the review history for style words ("indent", "whitespace", "quote", "wrap").

**Fix:** automate it, and remove it from the review checklist so the omission is structural rather than a matter of discipline.
**Recurrence guard:** no formatting item appears in the review template (CR4).

## 2. Unformatted code is on the main branch despite a pre-commit hook

**Symptom:** the hook exists and is documented, yet the standard is not universal.
**Mechanism:** the hook is skippable with `--no-verify`, absent in a fresh clone, absent in a web editor, and bypassed by dependency bots. Any of these leaves a hole.
**Diagnosis:** commit with `--no-verify` and push; does CI fail?

**Fix:** CI must be the authority; the hook stays for speed only.
**Recurrence guard:** the escape test is a verification step (CR5, CR6).

## 3. A single commit destroys `git blame` for the whole file

**Symptom:** every line attributes to a "style: apply formatter" commit; history is useless for archaeology.
**Mechanism:** a whole-codebase reformat landed without isolation and without a blame-ignore entry (R3).
**Diagnosis:** `git log --oneline -- <file>` shows one enormous commit; `.git-blame-ignore-revs` is absent.

**Fix:** add the reformat's SHA to `.git-blame-ignore-revs` with a dated comment, configure `blame.ignoreRevsFile`, and verify blame on a pre-reformat line.
**Recurrence guard:** every future formatting commit is recorded, and blame is verified after landing (CR9).

## 4. A feature PR has 5,000 changed lines

**Symptom:** reviewers cannot find the actual change; the description says "mostly formatting".
**Mechanism:** the formatter ran across the repo during functional work, mixing the two.
**Diagnosis:** does the diff contain both whitespace-only and logic changes? (`git diff -w` shows the logic.)

**Fix:** split — land a formatting-only commit first, then the feature on top.
**Recurrence guard:** the reformat isolation check is part of the policy (R3).

## 5. The linter was disabled in CI and never re-enabled

**Symptom:** a comment in the workflow says "temporarily disabled"; it dates from months ago.
**Mechanism:** the gate produced noise — usually generated files or a legacy baseline — and the fastest unblock was to remove it. The noise was never fixed, so the gate never returned.
**Diagnosis:** search the workflow for commented-out lint steps.

**Fix:** fix the noise (exclusions, a baseline), then re-enable. Add the suppression budget so a future exceedance is visible rather than fatal.
**Recurrence guard:** the suppression count and the exclusion check (CR10, CR13).

## 6. Thousands of lint findings on the first run

**Symptom:** enabling the gate blocks every PR immediately.
**Mechanism:** the gate was turned on for a legacy codebase with no baseline, so every file is a violation.
**Diagnosis:** was the count measured before enabling? Was the autofixable set applied first?

**Fix:** apply the autofixable set, then gate on no-new-findings rather than zero findings.
**Recurrence guard:** the legacy baseline requirement (CR17).

## 7. Every save produces a diff

**Symptom:** the developer formats, saves, and the file changes again; or two tools keep rewriting each other.
**Mechanism:** overlapping formatters, or an `.editorconfig` value that disagrees with the formatter's config.
**Diagnosis:** compare the editor's settings (indentation, line width) with the formatter's config.

**Fix:** one formatter per language, and make the shared values agree.
**Recurrence guard:** the alignment rule in the portable policy, verified by a save test.

## 8. CI fails on code that passes locally

**Symptom:** a clean local check, a red CI check, on the same commit.
**Mechanism:** a different tool version, or a config resolved from a different path, or a plugin present locally and absent in CI.
**Diagnosis:** print the resolved config path and the tool version in both environments.

**Fix:** pin the version, resolve the config from the repository root, and install the same plugins.
**Recurrence guard:** version pinning is a checklist item (CR2, CR5).

## 9. Generated files appear in every lint report

**Symptom:** the gate names files nobody wrote; the report is dominated by them.
**Mechanism:** no exclusion, or an exclusion pattern that does not match the actual path (R6).
**Diagnosis:** generate a file into the supposedly excluded directory and run the check.

**Fix:** exclude by path and header marker, and verify the pattern matches.
**Recurrence guard:** the exclusion verification step (CR10, CR11).

## 10. A suppression count nobody watches

**Symptom:** the number of suppressions rose from 20 to 400 over a year, unnoticed.
**Mechanism:** no visible metric and no budget, so each suppression looked locally reasonable (R4).
**Diagnosis:** run the suppression report; compare against a month ago.

**Fix:** report the count per language in CI, set a budget from the current count, and review stale suppressions on a cadence.
**Recurrence guard:** the budget and the report (CR12, CR13).

## 11. A rule is effectively disabled

**Symptom:** the rule is enabled in config, but its findings never appear.
**Mechanism:** hundreds of site suppressions, or a global disable added to silence one site.
**Diagnosis:** run the suppression report filtered to that rule.

**Fix:** either the rule is wrong for the repository (relax it globally with a recorded reason) or the suppressions were lazy (fix the sites).
**Recurrence guard:** the top-rules breakdown in the report (CR13).

## 12. A security finding was suppressed to unblock a release

**Symptom:** a shipped defect that the linter had already identified.
**Mechanism:** the suppression policy did not distinguish security-relevant rules, and the release deadline applied pressure (Anti-Hallucination).
**Diagnosis:** grep config and source for suppressions of injection, secret, or deserialisation rules.

**Fix:** revert the suppression, fix the finding, or escalate to `appsec-engineer` with a recorded decision.
**Recurrence guard:** the security carve-out is absolute and checked in verification (CR14).

## 13. The style gate stopped gating merges

**Symptom:** unformatted code is merging again, with the CI job green.
**Mechanism:** the CI job was renamed, and branch protection references the old name — so the required check no longer exists and merges proceed.
**Diagnosis:** compare the required check names in branch protection against the workflow's job names.

**Fix:** update the branch protection rule to the new name.
**Recurrence guard:** the check-name verification step (CR8).

## 14. A dependency bot's PR fails the style check

**Symptom:** every bot PR is red; someone has to fix it manually each week.
**Mechanism:** the bot's output is unformatted and in scope — often a lockfile that should be excluded, or generated source.
**Diagnosis:** inspect which file the bot changed and whether it should be excluded or formatted.

**Fix:** exclude lockfiles and generated output; where the bot writes source, let CI format it on the bot's branch.
**Recurrence guard:** an explicit bot policy rather than an exemption (CR7).

## 15. The style check takes twelve minutes

**Symptom:** developers batch their work and push with `--no-verify`; the gate is theatre.
**Mechanism:** whole-repo checks on every PR, no caching, no scoping, no parallel jobs.
**Diagnosis:** time the job on a typical PR; check whether it is scoped to changed files.

**Fix:** scope to changed files, cache the tool's cache, split format and lint, and run the full check on the main branch only.
**Recurrence guard:** the time budget is a checklist item (CR16).

## 16. A new language was added and has no style enforcement

**Symptom:** a new service or app appears with no formatter, no linter and no CI job.
**Mechanism:** onboarding a language was treated as creating a directory, not as extending the policy (R5).
**Diagnosis:** does every language in the repo have a CI job matching its name?

**Fix:** extend the policy: `.editorconfig` section, one formatter, one linter, exclusions, a CI job, a suppression budget — then verify with a deliberate failure.
**Recurrence guard:** the language-onboarding procedure, with the deliberate-failure acceptance test (CR2, CR3).

## The triage rule

Three findings — **no CI formatting check**, **bare suppressions**, and **generated files in scope** — are
detectable with the sweep in `anti-patterns.md` and account for most style-practice failures. Check those
three before any deeper review: the first means enforcement does not exist, the second means exceptions
are unbounded, and the third means the gate is producing the noise that gets it disabled.
