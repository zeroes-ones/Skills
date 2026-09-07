# Git & CI Efficiency — When to Commit, When to Push, How to Save CI Credits

How this repo (and any project using its tooling) spends the minimum necessary git and CI
resources while keeping every gate honest. The rule that runs through all of it: **local checks
are free, CI credits are not — so run everything cheap locally first, and make every CI run
count.**

## 1. When to commit

| Commit when... | Don't commit when... |
|---|---|
| One logical change is complete and self-contained (atomic commits) | Half-done work or "WIP" chunks that break the suite |
| The change passes the local gates it affects | Formatting churn mixed into a logic change (separate them) |
| Frontmatter/body edits pass `lint-workflow.py` / `lint-template.py` for the touched skills | Unrelated edits bundled into one commit (hard to revert, review, bisect) |
| Generated artifacts are regenerated consistently (e.g., `.skills-compiled/` if tracked, audit report) | Stray files, `__pycache__`, `*.tmp`, local state/memory JSONL (`.gitignore` handles these) |

A good default cadence: commit at each green local gate, push at each completed feature/fix —
not after every keystroke, not only at end of day.

## 2. When to push (and when to defer)

- **Push when the change is CI-ready**: local gates green for the touched scope
  (`bash scripts/run-ci-locally.sh` or at least the per-file lints), commit message describes the
  what+why.
- **Defer pushing when**: you are still iterating (local commits are enough), the change is
  docs-only or generated-output-only, or CI is already red on the branch from someone else's
  work — fix or rebase locally first.
- **Batch related pushes**: several small skill tweaks are cheaper as one PR run than N
  sequential pushes, because CI cancels-and-restarts on each new push (see concurrency below).

## 3. How to save CI credits (this repo's own playbook)

1. **Local gate first, always.** `bash scripts/run-ci-locally.sh` mirrors CI locally. For a quick
   skill edit, the per-file lints are enough before commit: `lint-workflow.py`, `lint-yaml.py`,
   `lint-template.py`, then `git diff --check`.
2. **Know which gates are cheap vs. expensive.** Cheap (seconds, run always): workflow
   validators + engine self-tests + golden evals (`validate-workflows.py --selftest`,
   `workflow-runner.py --selftest`, `eval-skill.sh --all`). Expensive (minutes): full
   `validate-skills.sh` across 297 skills, markdownlint over the whole corpus, hooks install.
   Run the expensive ones once per push/PR, not per commit.
3. **Only re-run what changed.** The new `workflow-graphs` CI job (engine + golden + dogfood) is
   fast by design; job-level path filters (skills/** vs docs/**) stop unrelated files from
   triggering full-corpus jobs — add `paths` filters to the workflow when you need job-level
   skipping.
4. **Cancel superseded runs.** The workflow uses a `concurrency` group with
   `cancel-in-progress: true`, so a new push on the same PR cancels the previous run instead of
   paying for both.
5. **Cache dependencies.** PyYAML installs use a pip cache so repeated runs don't re-download.
6. **Docs-only / code-only classification.** If a change touches only `docs/**`, `*.md` guides,
   or README, skip the heavyweight skill-validation jobs and run just markdown lint + link check;
   if it touches only `scripts/` tooling, run the tooling self-tests, not per-skill template
   lint. Put this policy in job `if:` conditions or path filters.
7. **Informational steps are free.** Benchmark, exporter counts, and SLI reports run as
   non-blocking informational steps (`step_pass`) — they print data without failing the job.
8. **Merge batching.** Land related skill PRs together so integration CI runs once, not per PR.
9. **Avoid CI churn from generated files.** Regenerate derived artifacts locally in the same
   commit that changes their source, so CI never sees an inconsistent pair.
10. **Watch the dogfood gate.** `repo-self-check` (workflow-graphs job) runs the repo's own
    quality gates as a graph; if it escalates, you are paying CI credits to discover what a local
    `run-ci-locally.sh` run would have found for free.

## 4. Where the policy lives "everywhere"

- **Contributors:** CONTRIBUTING-SKILLS.md Step 4 (validate continuously) — run the full local
  suite before push; see this guide for when to commit/push.
- **CI:** `.github/workflows/validate.yml` — concurrency cancel-in-progress, pip cache, and the
  fast `workflow-graphs` job.
- **Local mirror:** `scripts/run-ci-locally.sh` — identical steps locally so CI credits are only
  spent on the final confirmation.
- **Skill docs:** `docs/using-for-any-project.md` and `QUICKSTART.md` point here for the
  commit/push cadence.

## 5. The 30-second rule

If the local mirror is green for your change and it is one logical unit with a clear message:
commit. If it is the last commit of the logical unit and the branch's CI history is clean: push.
If CI already ran green for an identical change (docs-only, regenerated artifacts): skip the
re-run by batching or path filters rather than burning another run.
