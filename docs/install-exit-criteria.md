# Install Exit Criteria — What "Installable" Means for This Repo

**Definition of done:** the repo is *installable* when **every documented install channel** works
on a clean machine from the documented one-liner — no undocumented prerequisites beyond the
standard toolchain (`bash`, `git`, `curl`, optionally `node`/`npm`) — and each channel has a
concrete, repeatable verification. Exit criteria below are the checklist; anything not machine-
verifiable in CI is an explicit **gate** owned by a named person.

The three public distribution channels documented in `README.md` (Distribution section):

| Channel | Entry point |
|---|---|
| **Shell** | `curl -sSL https://raw.githubusercontent.com/zeroes-ones/Skills/main/scripts/install.sh \| bash` |
| **npm** | `npx @zeroes-ones/skills init` (also `skills-init`, `skills-update` bins) |
| **skills.sh registry** | `npx skills add zeroes-ones/Skills` |
| **Claude plugin marketplace** | `/plugin marketplace add zeroes-ones/Skills` |

---

## Exit criteria

### EC-1 … EC-3 — Shell install (verified in CI on push to `main`)
- **EC-1** `https://raw.githubusercontent.com/zeroes-ones/Skills/main/scripts/install.sh` returns
  HTTP 200 and is valid bash (`bash -n`).
  *Verify:* `curl -s -o /dev/null -w "%{http_code}" <url>` → `200`; CI `test-shell-install`.
- **EC-2** Fresh install exits 0 and produces: store at `~/.zeroes-ones/skills` containing
  **298** `SKILL.md` under `skills/` and **298** entries in `skills-flat/`, plus global agent
  symlinks (`.claude/skills`, `.agents/skills`, …) and `~/.local/bin/skills-init` +
  `skills-update`.
  *Verify:* isolated-`HOME` end-to-end run — CI `test-shell-install` job does exactly this.
- **EC-3** Installed `skills-init` (copied from `scripts/init-project.sh`) supports **both**
  activation modes: default = all 298 skills (flat, one level deep); `--solo` = 8,
  `--grow` = 18 by name; `--status` reports tier + count; switching modes replaces this
  script's own links; pre-existing user content in an agent dir is never deleted.
  *Verify:* counts after each mode via `find -L <agent-dir> -name SKILL.md | wc -l` → 298 / 8 / 18 —
  CI `test-shell-install` job.

### EC-4 … EC-7 — npm package (EC-6/EC-7 are external gates)
- **EC-4** `package.json` declares a bin named `skills` (the npm package short name) so the
  documented `npx @zeroes-ones/skills init` invocation resolves; it dispatches to
  `scripts/init-project.sh`. Every declared bin file exists.
  *Verify:* CI `test-npm-package` job (`node` reads `package.json`, checks each bin path).
- **EC-5** `npm pack` succeeds and the tarball contains the bin scripts + docs; no local
  build step is required between checkout and publish (`prepublishOnly` = lint + validate).
  *Verify:* CI `test-npm-package` job runs `npm pack` against the tarball contents.
- **EC-6** **GATE (owner: Sandeep, needs npm token):** `npm publish --access public` for
  `@zeroes-ones/skills`. Verify with `npm view @zeroes-ones/skills version` (returns a version,
  not 404).
- **EC-7** **GATE (post-publish):** on a clean machine with Node ≥ 16,
  `npx @zeroes-ones/skills init` bootstraps `~/.zeroes-ones/skills` on first use, then activates
  skills in the current project (default 298; `--solo`/`--grow`/`--status` work).

### EC-8 … EC-9 — skills.sh registry (EC-9 is an external gate)
- **EC-8** Repo is natively indexable: canonical `skills/<category>/<name>/SKILL.md` tree with
  unique frontmatter `name` + `description`, and skills declared in
  `.claude-plugin/marketplace.json` exist at their declared depth.
  *Verify:* structural checks already in CI (`validate.yml`, marketplace generator); no mirror
  repo needed (see `docs/distribution-best-in-class.md` §4.1).
- **EC-9** **GATE (post-push, indexing is telemetry-driven, minutes–hours):**
  `npx skills add zeroes-ones/Skills`, then confirm discovery with `npx skills find <skill-name>`
  (e.g. `system-architect`). If auto-discovery misses: skills.sh request-indexing issue flow
  (`docs/plugin-marketplace-publishing.md` §3).

### EC-10 … EC-11 — Claude plugin marketplace (EC-11 is an external gate)
- **EC-10** `.claude-plugin/marketplace.json` is well-formed JSON; every plugin `skills:` path
  exists with skill children (regenerated + validated by `scripts/emit-marketplace.py`, checked
  in CI `test-plugin-manifests`).
- **EC-11** **GATE (needs Claude Code CLI):** `/plugin marketplace add zeroes-ones/Skills`, then
  `/plugin install zeroes-ones-all@zeroes-ones-skills` succeeds; optionally
  `claude plugin validate .` in CI once the CLI is available.

### EC-12 — Docs truth
- **EC-12** Every install command shown in `README.md` / `QUICKSTART.md` matches verified
  behavior (channels above), and docs link to this file. Reviewed on each install-related change.

---

## Status (this change)

| ID | Criterion | Status | Where verified |
|---|---|---|---|
| EC-1 | raw URL + bash syntax | ✅ | curl 200 (2026-09-07); CI |
| EC-2 | fresh shell install 298/298 + symlinks | ✅ | local isolated-HOME e2e; CI `test-shell-install` |
| EC-3 | dual-mode `skills-init` | ✅ | local e2e (298/8/18, mode switch, foreign-dir keep); CI |
| EC-4 | `skills` bin + dispatcher | ✅ | local `bash -n` + dispatcher run; CI |
| EC-5 | `npm pack` clean | ✅ (CI runs on push) | CI `test-npm-package` |
| EC-6 | **npm published** | ⛔ GATE | needs `npm publish` (owner token) |
| EC-7 | `npx … init` on clean machine | ⛔ GATE | after EC-6 |
| EC-8 | skills.sh-indexable layout | ✅ | structural, CI |
| EC-9 | skills.sh index populated | ⛔ GATE | `npx skills add` + `find` after push |
| EC-10 | marketplace.json valid | ✅ | generator + CI |
| EC-11 | Claude plugin install works | ⛔ GATE | needs Claude Code CLI |
| EC-12 | docs match behavior | ✅ | this change |

**Owned external gates (cannot be completed from the repo):** EC-6 (npm token),
EC-7 (post-publish), EC-9 (registry indexing), EC-11 (Claude Code CLI session).
The one-time launch checklist with exact commands and done-boxes for every owner action
(including enabling GitHub Pages for the graph explorer) is in
[`docs/owner-next-actions.md`](owner-next-actions.md).
