# Using zeroes-ones/Skills in Your Projects — Runbook

Plain-language guide for three usage modes. Skills are **markdown prompts your agent
reads** — nothing in this repo executes tasks for you; your agent does the work, and
this repo supplies the expertise (skills), optional orchestration (workflow engine),
and measurement (tooling).

---

## Mode A — "Just use the skills with my agent" (simplest)

```bash
# 1) One-time machine install: clone to ~/.zeroes-ones/skills + symlink into
#    ~/.claude/skills, ~/.cursor/skills, ~/.copilot/skills, ... (10 agents)
curl -sSL https://raw.githubusercontent.com/zeroes-ones/Skills/main/scripts/install.sh | bash

# 2) Per project: activate skills inside that project
cd your-project
skills-init              # all 298 skills        (or: --solo 8 / --grow 18)
skills-init --principles # optional: append always-on rules to CLAUDE.md/AGENTS.md
skills-init --status     # see tier + linked skill count
```

That's it. The agent auto-discovers skills by their frontmatter description
("Use when… Handles… Do NOT use for…") and loads the matching one when your task fits.
Optional pointer for stronger routing: add to your project's `CLAUDE.md`/`AGENTS.md` —
"Consult the `using-agent-skills` skill before starting." Updates later: `skills-update`.

**Alternative install:** `npx @zeroes-ones/skills init` (needs node) or, for Claude Code,
`/plugin marketplace add zeroes-ones/Skills` → `/plugin install zeroes-ones-all@zeroes-ones-skills`.

---

## Mode B — Skills as an executable workflow engine (bounded, measured runs)

For turning a multi-step job into a gated, recorded, scored run (skills become graph
nodes; Verification sections are the completion checks):

```bash
# Scaffold a project's .agent/ workspace (manifests/, state/, memory/, README)
bash scripts/project-init.sh /path/to/project

# Author a manifest: nodes (= skills), gates, loops, payload handoffs (YAML)
#   .agent/manifests/<flow>.yaml — see workflow/manifests/*.yaml for examples

# Run + measure
python3 scripts/workflow-runner.py --manifest .agent/manifests/<flow>.yaml
python3 scripts/run-effectiveness.py --state .agent/state/<run>.json   # score 0-100
python3 scripts/skill-sli-report.py --dir .agent/state/                # completion, escalation rate
```

Needs only `python3` (standard library — no pip packages).

---

## Mode C — Maintainer / contributor: quality & measurement tooling

```bash
./scripts/validate-skills.sh              # governance suite (14/14 green = exit 0)
./scripts/run-evals.sh --tier 1           # structural evals (43/43)
python3 scripts/eval-routing.py           # routing health: rank-1 / top-N / MRR / violations
python3 scripts/emit-skill-registry.py --check   # metadata drift gate (299/299)
python3 scripts/check-token-budget.py     # compiled-tokens vs declared token_budget contract
python3 scripts/regression-scope.py <skill>      # dependents to re-test before editing a skill
python3 scripts/grade-golden.py           # deterministic RED→GREEN grading (no LLM judge)
```

All stdlib python3; run from the repo root.

---

## Dependency truth table ("do these work by themselves?")

| Thing | Standalone? | Requires |
|---|---|---|
| Using skills (Mode A) | ✅ | An agent + cloned files |
| Workflow engine (Mode B) | ✅ | `python3` (stdlib) |
| All validate/eval/registry/budget/grade/regression scripts | ✅ | `python3` (stdlib) |
| Tier-2 routing eval (`run-routing-evals.js`) | ⚠️ | `node` — use `python3 scripts/eval-routing.py` instead |
| Tier-3 behavioral eval (`run-behavioral-evals.js`) | ⚠️ | `node` + real agent transcripts |
| LLM-judge / drift monitors (`behavioral-evals.py`) | ❌ | OpenAI/Anthropic API keys |
| npm CLI (`npx @zeroes-ones/skills`) | ⚠️ | node/npm to install the CLI |
| `skills-update` | — | git (pulls latest) |

---

## How the always-on principles reach your agent (two paths)

1. **Plugin hook (Claude Code):** installing the `zeroes-ones-all` plugin registers a
   SessionStart hook (`plugins/zeroes-ones-all/hooks/`) that injects the ~280-token
   operating-principles block every session. Verify with `/hooks` in Claude Code.
2. **File overlay (any agent):** `skills-init --principles` appends the same block to your
   project's `CLAUDE.md` (or `AGENTS.md`) — idempotent; safe for agents without hook support.

Both inject `hooks/always-on-principles.md` content: routing pointer + Think Before
Coding / Simplicity First / Surgical Changes / Goal-Driven Execution + verification rules.

---

## Troubleshooting

- **Agent doesn't see skills** → confirm symlinks: `ls -la .claude/skills` (should point at
  the flat store). Re-run `skills-init`.
- **`skills-init` clones every run** → store lives in `~/.zeroes-ones/skills`; set
  `SKILLS_HOME=/custom/path` to relocate.
- **Hook not firing (Claude Code)** → hooks are snapshotted at session start; restart the
  session, confirm the plugin is installed (`/plugin`), and check `/hooks`.
- **Scripts crash with `ModuleNotFoundError: yaml`** → they now fall back to the bundled
  `scripts/yaml_shim.py`; if you still see it, you are running an old copy — `skills-update`.
