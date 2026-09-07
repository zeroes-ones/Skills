# Owner Next Actions — One-Time Launch Checklist

Everything below needs a credential or a settings toggle only the repo owner can provide.
They are documented here so they can be completed later in ~10 minutes. Each item lists the
exact action, the verification command, and a done-box. Cross-references:
`docs/install-exit-criteria.md` (EC-1…EC-12) and `docs/plugin-marketplace-publishing.md`.

---

## 1. Enable GitHub Pages — makes the graph explorer live ✅ DONE (2026-09-07)
Explorer is fully built (`docs/graph-explorer/`), its deploy workflow
(`.github/workflows/deploy-pages.yml`) is green, and Pages is now enabled with
**Source: GitHub Actions**.

- [x] **Action:** GitHub web UI → **Settings → Pages → Source: "GitHub Actions"**.
- [x] **Verify:** "Deploy Graph Explorer to GitHub Pages" workflow → **success**;
      live at **https://zeroes-ones.github.io/Skills/** (verified: HTTP 200, explorer
      v2 with domain chips + pathfinder served).

## 2. Publish the npm package (EC-6)
`@zeroes-ones/skills` is publish-ready (bins + tarball contents verified in CI); it has never
been published (registry 404 today).

- [ ] **Prereq:** npm token with publish rights to the `@zeroes-ones` scope.
- [ ] **Action:** from a clean checkout of `main`:
      `npm publish --access public` (`prepublishOnly` runs lint + validate automatically).
- [ ] **Verify:** `npm view @zeroes-ones/skills version` returns a version (not 404).

## 3. Post-publish `npx` smoke check (EC-7)
- [ ] **Action:** on a clean machine with Node ≥ 16:
      `npx @zeroes-ones/skills init` — should bootstrap `~/.zeroes-ones/skills` on first use and
      activate skills in the current project (default 298; `--solo` 8 / `--grow` 18 / `--status`).
- [ ] **Also:** `npx @zeroes-ones/skills update` and `npx @zeroes-ones/skills --help` resolve.

## 4. Claude Code plugin marketplace install (EC-11)
- [ ] **Action:** inside Claude Code:
      `/plugin marketplace add zeroes-ones/Skills`
      `/plugin install zeroes-ones-all@zeroes-ones-skills` (or `/plugin install <domain>@zeroes-ones-skills`)
- [ ] **Optional CI wiring:** `claude plugin validate .` from a checkout, added to the lint job.

## 5. skills.sh registry — already live, keep as periodic check (EC-8/EC-9)
Detail pages already resolve (`skills.sh/zeroes-ones/Skills/<name>` → 200). Periodic check:
- [ ] `npx skills find system-architect` returns the skill; `npx skills add zeroes-ones/Skills` works.

---

**Status:** item 1 (Pages) is **done** — explorer v2 live at `https://zeroes-ones.github.io/Skills/`.
Items 2–4 (npm publish EC-6, post-publish npx check EC-7, Claude plugin install EC-11) are the
remaining owner-gated launch steps. Claude Code plugin install (EC-11) was verified in a
maintainer session (marketplace add + `zeroes-ones-all` 298 skills + flagship 30); item 4's
checkbox documents the end-user flow. Everything code-side is done, verified, and CI-green.
