# Installing Skills — Every Channel, All vs Individual

> **Read this if you want the library in a project and you are not sure which command to run.**
> Every command below was executed against this checkout. Counts shown are what the commands
> compute at runtime, not hardcoded numbers.

## 0. Which channel should I use?

| You want | Channel | Command |
|---|---|---|
| One command, nothing to think about | **Shell** | `curl -sSL .../install.sh \| bash` |
| npm-native, no clone | **npx** | `npx @zeroes-ones/skills init` |
| A specific subset in one project | **Tier / individual** | `skills-init --solo` · `--grow` · `--skill <name>` |
| Skills inside Claude Code as a plugin | **Plugin** | `/plugin install flagship-senior-engineering@zeroes-ones-skills` |
| No filesystem changes at all | **MCP** | `python3 scripts/mcp-skill-server.py` |

The first two install a **store** (the whole library) and optionally activate it. The rest choose
**what a given project sees**.

## 1. Shell install (canonical)

```bash
curl -sSL https://raw.githubusercontent.com/zeroes-ones/Skills/main/scripts/install.sh | bash
```

Clones the library to `~/.zeroes-ones/skills/`, creates global symlinks for every detected agent,
and installs the `skills-init` / `skills-update` convenience commands. Re-running it updates.

Then activate per project:

```bash
cd your-project
skills-init                # all skills
skills-init --solo         # 8 essential
skills-init --grow         # 18
skills-init --skill code-reviewer --skill tdd-guide
```

## 2. npm / npx install

```bash
npx @zeroes-ones/skills init        # activate all skills in the current project
npx @zeroes-ones/skills update      # install/update the ~/.zeroes-ones store
npx @zeroes-ones/skills validate    # run the governance suite (dev tool)
npx @zeroes-ones/skills lint        # run the markdown linter (dev tool)
```

**How this works:** the npm package ships the *CLI*, not the skill files. On first `init` the CLI
clones the library to `~/.zeroes-ones/skills` (via `bootstrap_store` in `scripts/init-project.sh`)
and then activates from that store. This is deliberate — the skill corpus is large and git is a
better distribution channel for it than the npm tarball. The practical consequence: **your first
`npx ... init` needs network access and `git`**, and every later run is local.

Every subcommand also exists as a named bin after a global install:

| Bin | Equivalent |
|---|---|
| `skills-init` | `npx @zeroes-ones/skills init` |
| `skills-update` | `npx @zeroes-ones/skills update` |
| `skills-validate` | `npx @zeroes-ones/skills validate` |
| `skills-lint` | `npx @zeroes-ones/skills lint` |

## 3. All vs individual — how activation works

`skills-init` links into **10 agent directories** (`.agents/skills`, `.claude/skills`,
`.copilot/skills`, `.github/skills`, `.cursor/skills`, `.codex/skills`, `.gemini/skills`,
`.windsurf/skills`, `.cline/skills`, `.opencode/skills`). What goes in them depends on the mode:

| Mode | Command | What is linked | Result |
|---|---|---|---|
| **Full** (default) | `skills-init` · `skills-init --full` | **one symlink** to the whole `skills-flat` layer | every skill, discoverable |
| **Solo** | `skills-init --solo` | 8 individual skill directories | essentials only |
| **Grow** | `skills-init --grow` | 18 individual skill directories | essentials + scale-up |
| **Individual** | `skills-init --skill <name>` | one directory per named skill | exactly what you asked for |

### Individual selection

```bash
skills-init --skill code-reviewer                    # one skill
skills-init --skill code-reviewer --skill tdd-guide  # repeatable
skills-init --skill code-reviewer,tdd-guide          # comma-separated
```

Rules that matter:

- **Unknown names fail loudly.** A typo exits non-zero and activates nothing, rather than leaving
  you with an empty install that looks like success.
- **Repeatable and comma-separated forms mix freely.**
- **Mode switching replaces the installer's own links only.** Pre-existing directories with real
  content are never deleted; they are reported and skipped.

### Full mode is one symlink, not 320

Full mode links `skills-flat` as a single symlink. That means adding a skill to the library
requires **no re-activation** in consuming projects — the symlink already covers it. Solo/grow/
individual modes link by name, so they do need a re-run to pick up a newly named skill.

### Checking and switching

```bash
skills-init --status                                  # current tier + linked count
skills-init --solo                                    # switch down
skills-init                                           # switch back to full
```

`.skills-tier` in the project records the current mode, so the installer can tell whether it is
switching tiers or re-applying the same one.

## 4. Claude Code plugin

```bash
/plugin marketplace add zeroes-ones/Skills
/plugin install flagship-senior-engineering@zeroes-ones-skills
```

Installs a curated set as one plugin. Use this when you want the library inside Claude Code's own
plugin system rather than as a project symlink layer.

## 5. MCP server (no filesystem changes)

```bash
python3 scripts/mcp-skill-server.py --selftest     # verify first
```

Serves 8 tools over stdio (`list_skills`, `get_skill`, `get_skill_contract`, `search_skills`,
`get_skill_graph`, `list_workflows`, `validate_manifest`, `run_workflow`). This installs *no files*:
it serves *capability*, so an agent retrieves a skill on demand instead of scanning a directory.
See [`mcp-server.md`](mcp-server.md), including a troubleshooting table.

## 6. Verify any install

```bash
skills-init --status
find -L .claude/skills -name SKILL.md | wc -l    # linked skill count
python3 scripts/mcp-skill-server.py --selftest   # MCP only
bash scripts/validate-skills.sh                  # in a dev checkout
```

## 7. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `npx ... init` appears to do nothing | No `git`, or no network on first run | Install `git`; the first run must clone the store |
| `Skills store not found` | `SKILLS_HOME` is set but does not exist | Unset it to allow auto-bootstrap, or point it at a real checkout |
| `unknown skill '<name>'` | Name not in the flat layer | `ls ~/.zeroes-ones/skills/skills-flat` or use MCP `search_skills` |
| Skills not visible to the agent | Agent directory not linked, or agent needs a restart | `skills-init --status`; restart the session so discovery re-runs |
| Existing skills disappeared | Pre-existing non-symlink dirs are skipped by design, never deleted | Check whether the directory was a real directory, not an installer link |
| Count looks wrong | Older docs quoted frozen numbers | Run `skills-init --status`; counts are computed from the corpus |

## 8. Uninstall / reset

The installer only ever removes **its own symlinks** back into the library. Delete the agent
directories (`.claude/skills` etc.) to de-activate, and remove `~/.zeroes-ones/skills` to delete the
store. Real directories with user content are never touched.

## See also

- [`install-exit-criteria.md`](install-exit-criteria.md) — what "installable" means, with evidence
- [`agent-support-matrix.md`](agent-support-matrix.md) — per-agent discovery layouts
- [`mcp-server.md`](mcp-server.md) — MCP install and tool reference
- [`owner-next-actions.md`](owner-next-actions.md) — owner-gated publish steps
