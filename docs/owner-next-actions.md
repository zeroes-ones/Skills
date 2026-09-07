# Owner Next Actions — One-Time Launch Checklist

Everything below needs a credential or a settings toggle only the repo owner can provide.
They are documented here so they can be completed later in ~10 minutes. Each item lists the
exact action, the verification command, and a done-box. Cross-references:
`docs/install-exit-criteria.md` (EC-1…EC-12) and `docs/plugin-marketplace-publishing.md`.

---

## 1. Enable GitHub Pages — makes the graph explorer live
The explorer is fully built (`docs/graph-explorer/`) and its deploy workflow
(`.github/workflows/deploy-pages.yml`) is green-ready; it currently fails only because Pages
is not enabled for the repo (API enablement returns 403 with the current PAT).

- [ ] **Action:** GitHub web UI → **Settings → Pages → Source: "GitHub Actions"** (or use a
      Pages-scoped token: `gh api --method POST repos/zeroes-ones/Skills/pages -f build_type=workflow`).
- [ ] **Verify:** trigger or wait for the "Deploy Graph Explorer to GitHub Pages" workflow →
      green; open `https://zeroes-ones.github.io/Skills/` and confirm the graph renders.

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
      activate skills in the current project (default 297; `--solo` 8 / `--grow` 18 / `--status`).
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

**Status:** items 1–4 are the remaining owner-gated launch steps after the installability work
and the graph-explorer build (`origin/main` `c390792a`). Everything code-side is done, verified,
and CI-green.
