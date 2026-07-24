# Symbolic Link Strategy

## Core Decision: Symlink vs Copy

```
                         ┌─────────────────────┐
                         │ Is this skill       │
                         │ identical across    │
                         │ ALL agents?         │
                         └──────────┬──────────┘
                                    │
                         ┌──────────▼──────────┐
                         │ YES                 │ NO
                    ┌────▼────┐          ┌─────▼──────────┐
                    │ SYMLINK │          │ Does this agent │
                    │ from    │          │ need different  │
                    │ core/   │          │ content than    │
                    └─────────┘          │ other agents?   │
                                         └──┬──────────┬───┘
                                            │YES       │NO
                                      ┌─────▼──┐  ┌───▼──────────┐
                                      │ COPY to│  │ Strip agent-  │
                                      │ over-  │  │ specific      │
                                      │ rides/ │  │ fields from   │
                                      │ <agent>│  │ frontmatter   │
                                      └────────┘  │ → SYMLINK     │
                                                  └───────────────┘
```

## When to Symlink (Shared Skills)

Symlink shared skills from `~/.agents/skills/core/<skill>/` to each agent's skill directory. This ensures a single source of truth.

**Conditions for symlink:**
- Skill content is identical across all target agents
- Frontmatter normalization handles agent-specific field stripping
- No agent-specific overrides needed in the SKILL.md body

**Symlink command:**
```bash
ln -s ~/.agents/skills/core/code-reviewer ~/.claude/skills/code-reviewer
ln -s ~/.agents/skills/core/code-reviewer ~/.copilot/skills/code-reviewer
ln -s ~/.agents/skills/core/code-reviewer ~/.cursor/skills/code-reviewer
```

**Verification:**
```bash
# Check all symlinks resolve
find ~/.claude/skills/ -type l -exec test ! -e {} \; -print
find ~/.copilot/skills/ -type l -exec test ! -e {} \; -print
```

## When to Copy (Agent-Specific Overrides)

Copy to `~/.agents/skills/overrides/<agent>/<skill>/` when an agent needs different content than the core version.

**Triggers for copy:**
- Agent requires a `PROCESS_TREE.md` that doesn't belong in the core skill
- Agent-specific body content (e.g., Gemini CLI directive blocks embedded in Markdown)
- Frontmatter fields that cannot be stripped (they're embedded in the body content)
- Agent-specific reference files needed

**Copy workflow:**
1. Copy core skill to `~/.agents/skills/overrides/<agent>/<skill>/`
2. Modify the override copy for agent-specific needs
3. Symlink the override into the agent directory: `ln -s ~/.agents/skills/overrides/<agent>/<skill> ~/.<agent>/skills/<skill>`

**Precedence rules:**
1. `overrides/<agent>/<skill>/` takes precedence over `core/<skill>/`
2. If no override exists, use `core/<skill>/` directly
3. Never symlink an override into `core/` — overrides are agent-specific by definition

## Hashing for Deduplication and Change Detection

```bash
# Generate SHA-256 hash of a skill's content
find ~/.agents/skills/core/code-reviewer -type f -exec sha256sum {} \; | sort | sha256sum

# Detect which skills changed since last manifest generation
diff <(jq -r '.skills[] | "\(.name) \(.sha256)"' ~/.agents/skills/skills-manifest.lock) \
     <(for d in ~/.agents/skills/core/*/; do
         name=$(basename "$d")
         hash=$(find "$d" -type f -exec sha256sum {} \; | sort | sha256sum | cut -d' ' -f1)
         echo "$name $hash"
       done)
```

## Symlink Health Monitoring

**Critical checks to run in CI or pre-commit hooks:**
```bash
#!/usr/bin/env bash
# Check for broken symlinks across all agent directories
BROKEN=0
for agent_dir in ~/.claude/skills ~/.copilot/skills ~/.cursor/skills ~/.codex/skills ~/.gemini/skills ~/.opencode/skills; do
  if [ -d "$agent_dir" ]; then
    while IFS= read -r link; do
      if [ ! -e "$link" ]; then
        echo "BROKEN: $link → target missing"
        BROKEN=$((BROKEN + 1))
      fi
    done < <(find "$agent_dir" -type l)
  fi
done
[ "$BROKEN" -gt 0 ] && echo "Found $BROKEN broken symlinks" && exit 1
echo "All symlinks healthy"
```

## Gotcha: Agent Upgrade Breaks Symlinks

When an agent terminal upgrades and changes its directory structure (e.g., Claude Code moves from `~/.claude/skills/` to `~/.claude/agents/skills/`), all symlinks break. This has been reported to cost teams $10K+ in debugging broken skill references.

**Mitigation:**
- Store the target base path in a variable (`AGENT_SKILL_DIR_CLAUDE`)
- Run symlink health checks in CI daily
- Pin agent versions and test symlink paths on upgrade

## Gotcha: Relative Symlinks Break on Agent Resolve

Some agents resolve symlinks before reading, causing relative path references (`../references/`) inside SKILL.md to break. The symlink resolves to `~/.agents/skills/core/<skill>/references/` but the agent resolves paths relative to the symlink location.

**Mitigation:**
- Use absolute paths for internal references when targeting symlink-resolving agents
- Test with `readlink -f` to verify path resolution
