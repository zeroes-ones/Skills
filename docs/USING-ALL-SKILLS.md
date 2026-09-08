# Using & Incorporating All 298 Skills — Complete Guide

Plain instructions for getting the **full library** into your projects and agents, and for
using skills alone or chained together. Companion to `docs/USING-IN-PROJECTS.md` (3 modes +
dependency table); this guide is the "how do I actually use *all* of them" reference.

---

## 1. Get all skills into your machine and project

**One-time machine install** (clones to `~/.zeroes-ones/skills`, symlinks into every agent):

```bash
curl -sSL https://raw.githubusercontent.com/zeroes-ones/Skills/main/scripts/install.sh | bash
# alt: npx @zeroes-ones/skills init        (needs node)
```

**Per project — activate all 298:**

```bash
cd your-project
skills-init            # default = FULL (all 298 skills, all 37 domains)
skills-init --principles   # also append the always-on operating rules to CLAUDE.md/AGENTS.md
skills-init --status       # confirm: tier full · count of linked SKILL.md
```

Verify the links exist: `ls your-project/.claude/skills/ | head` (should list skill names —
this is the one-level-deep `skills-flat` view every agent scanner can read).

**Claude Code plugin route** (per-domain or all-in-one):

```
/plugin marketplace add zeroes-ones/Skills
/plugin install zeroes-ones-all@zeroes-ones-skills      # all 298 skills + always-on hook
# or per domain: /plugin install finance@zeroes-ones-skills, strategy@…, …
/plugin install flagship-senior-engineering@zeroes-ones-skills   # curated 30-skill dev set
```

**Registry route (skills.sh):** `npx skills add zeroes-ones/Skills` then
`npx skills use zeroes-ones/Skills@<skill-name>` for single skills.

---

## 2. How the agent uses a skill (know this first)

- Every skill is one folder `skills/<domain>/<skill-name>/SKILL.md` (also reachable as
  `<skill-name>` in the flat layer your agents link).
- The **frontmatter `description`** is the discovery key: it always says
  "Use when… Handles… Do NOT use for…". Agents match your request against these
  descriptions automatically and load the skill that fits.
- Activation is **automatic by default**; you can also force it:
  - Claude Code / Cursor / Copilot style: `/<skill-name>` (e.g. `/code-reviewer`)
  - Plain text: "act as the <skill-name> skill" or paste the description
  - Unsure which skill fits? Tell the agent: *"consult the `using-agent-skills` meta-router"*
    — it maps task types → the right skills.
- Loaded skill behavior: the `SKILL.md` body drives the agent (ground rules, decision
  trees, `Core Workflow`, `Verification` = how it proves completion, anti-hallucination
  guardrails). Deep material stays in `references/` (loaded only when the agent needs it);
  sections are marked `(QUICK)/(STANDARD)/(DEEP)` for progressive disclosure.

---

## 3. The three activation tiers (when 298 is too much)

`skills-init` supports subsets; switch anytime by re-running:

```bash
skills-init --solo     # 8 core skills (personal projects)
skills-init --grow     # 18 skills (project gaining traction)
skills-init            # full: all 298 (default, team/company)
```

Solo = `ceo-strategist product-manager fullstack-developer code-reviewer qa-engineer
security-reviewer ci-cd-builder gdpr-privacy`; `--grow` adds strategy/UX/arch/backend/
devops/security leads. `--full` links the whole `skills-flat` layer.

---

## 4. Finding the right skill

- **Browse the catalog:** README domain table (37 rows), or
  `python3 scripts/build-skill-index.py` for a searchable index.
- **Visual graph:** open `docs/graph-explorer/index.html` (also live at
  https://zeroes-ones.github.io/Skills/) — click any skill to see what it consumes from /
  feeds into.
- **CLI search:** `grep -rl "<keyword>" skills/*/*/SKILL.md` (from a checkout), or
  `npx skills find <name>` once the repo is indexed on skills.sh. The shipped npm CLI bins
  are `skills-init / skills-update / skills-validate / skills-lint` — there is no
  `skills-find` binary.
- **Router skills:** `using-agent-skills` (framework) routes any task to the right skill;
  `senior-engineer-mode-router` picks the engineering mode first.

---

## 5. Using skills in real work — concrete patterns

### A. Single skill (one request)
```
"Review this PR for correctness and security — /code-reviewer"
"Design the database schema for our multi-tenant SaaS — /database-designer"
"Help me structure the pre-seed pitch — /ceo-strategist" (etc.)
```
Result: the agent follows that skill's workflow and its **Verification** section before
declaring done.

### B. Chaining skills (the library's real power)
Skills declare dependencies in frontmatter `chain: consumes_from / feeds_into`
(1,916 validated edges). Hand a **chain** as one request:

```
"Take this idea to a shipped feature: idea-to-spec → system-architect →
 backend-developer → code-reviewer, and only mark done after the review passes."
```

Typical product chain: `business-strategist` → `idea-to-spec` → `ux-researcher` →
`ui-ux-designer` → `backend-developer` + `frontend-developer` → `code-reviewer` →
`shipping-and-launch`. The agent follows each skill's `Core Workflow` and passes artifacts
(decision gates, verification evidence) between steps.

### C. Skills as a bounded workflow (Mode B — measured runs)
For anything you want gated/recorded/scored rather than conversational:

```bash
bash scripts/project-init.sh .                      # scaffolds .agent/ workspace
# edit .agent/manifests/<flow>.yaml — nodes = skills, plus gates/loops/payloads
python3 scripts/workflow-runner.py --manifest .agent/manifests/<flow>.yaml
python3 scripts/run-effectiveness.py --state .agent/state/<run>.json
python3 scripts/skill-sli-report.py --dir .agent/state/
```
Every skill is already a valid graph node (its Verification section is the completion
check); adding an explicit `workflow:` frontmatter contract makes it first-class
(30 skills today; 296 eligible).

---

## 6. Per-agent cheat sheet

| Agent | Linked dir (install.sh / skills-init) | Notes |
|---|---|---|
| Claude Code | `.claude/skills` | auto-discovery; `/<name>`; plugin + SessionStart hook supported |
| Generic agents | `.agents/skills` (universal) | most scanners read one-level `<name>/SKILL.md` |
| Cursor | `.cursor/skills` | `.cursor/rules` optional; auto + `/name` |
| GitHub Copilot CLI | `.github/skills` | auto-discovery of skills dir |
| Codex CLI | `.codex/skills` | auto-discovery |
| Gemini CLI | `.gemini/skills` | auto-discovery |
| Windsurf / Cline / OpenCode | `.windsurf/skills` `.cline/skills` `.opencode/skills` | same one-level convention |

If your agent supports hooks, the SessionStart hook (installed with the
`zeroes-ones-all` plugin) injects the always-on principles; otherwise
`skills-init --principles` covers any agent via `CLAUDE.md`/`AGENTS.md`.

---

## 7. Keep it healthy (updates, verification, contribution)

```bash
skills-update                 # git pull the library (fresh skills/fixes)
skills-validate               # governance suite must pass
python3 scripts/eval-routing.py        # routing health baseline
python3 scripts/emit-skill-registry.py --check   # metadata drift
python3 scripts/regression-scope.py <skill>      # dependents before you edit a skill
```

Contributing a skill? See `CONTRIBUTING-SKILLS.md` and `SKILL-QUALITY-STANDARDS.md`; new
skills must pass the 16 pre-commit gates (template sections, examples, chain edges, …).

---

## 8. Troubleshooting

- **Agent can't find skills** → links missing? `ls .claude/skills` empty → re-run
  `skills-init`. Old store? → `skills-update` (needs the flat layer).
- **Wrong skill activates** → routing is vocabulary-based today (rank-1 ~43% on the
  canonical baseline). Be explicit: name the skill (`/name`) or rephrase with its trigger
  words ("Use when"-style). Semantic routing is the active roadmap item.
- **Session rules not injected** → hooks snapshot at session start; restart the session.
  Fallback for any agent: `skills-init --principles`.
- **Big context** → skills load their full body by default; prefer `(QUICK)` sections and
  tell the agent "use only the (QUICK)/decision-tree sections first". Compiled/minified
  loading (86% smaller) is available via `scripts/compile-skills.sh` for executors that
  read the compiled artifact.
