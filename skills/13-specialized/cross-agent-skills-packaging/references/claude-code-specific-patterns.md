# Claude Code Specific Patterns

## `.claude/skills/` Directory

Claude Code reads skills from `~/.claude/skills/` (configurable via `~/.claude/settings.json` `skillsDirectory`). Skills are loaded at session start and included in the system prompt's `available_skills` block.

## PROCESS_TREE.md Convention

**CRITICAL:** Claude Code requires a `PROCESS_TREE.md` file in each skill directory for detection. Without it, the skill is invisible even with a valid `SKILL.md` and working symlink.

**Minimum PROCESS_TREE.md:**
```markdown
# Process Tree: <skill-name>
- Skill: <skill-name>
- Version: 1.0.0
- Type: specialized
```

**Full PROCESS_TREE.md:**
```markdown
# Process Tree: code-reviewer

## Entry Point
- File: SKILL.md
- Frontmatter: YAML (name, description, tags, type, status, version)

## Decision Flow
1. Auto-route conditions check filesystem state
2. Intent-route tree presents user choices
3. Ground rules gate execution (negative constraints)
4. Core workflow executes phased process
5. Cross-skill coordination routes to other skills

## Dependencies
- References: 14 files in references/
- External tools: git, gh CLI
- Cross-skill: api-designer → code-reviewer → qa-engineer

## Output Artifacts
- Code review report (Markdown)
- Severity-graded findings (critical/high/medium/low)
- Suggested fixes with code snippets
```

**When PROCESS_TREE.md is missing:**
- Claude Code silently ignores the skill
- No error message in logs
- Skill appears to be "deployed" but never loads
- Debugging requires checking `~/.claude/logs/` for skill loading events

## Claude Code Frontmatter

Standard YAML frontmatter with no vendor-specific fields:

```yaml
name: code-reviewer
description: Six-dimension code review covering security, performance, quality...
license: MIT
tags: [code-review, security, quality]
author: Sandeep Kumar Penchala
type: quality
status: stable
version: 2.1.0
```

Claude Code silently ignores unrecognized fields — they won't cause rejection but won't appear in the agent's context either.

## Skills Repository Conventions

Claude Code's official skill repository (`claude-code/skills`) follows these conventions:
- Each skill is a directory with `SKILL.md` + `references/` + `PROCESS_TREE.md`
- Skills are organized by category (development, quality, devops, etc.)
- `PROCESS_TREE.md` acts as the skill's table of contents and discovery mechanism

## Issue #31005

**Tracking:** Claude Code issue #31005 proposes deprecating `PROCESS_TREE.md` in favor of manifest-based discovery via `skills-manifest.json`. Until this is resolved:

1. **Always include `PROCESS_TREE.md`** for Claude Code compatibility
2. **Generate `PROCESS_TREE.md` from manifest** as a build step in the packaging pipeline
3. **Monitor issue #31005** for the deprecation timeline

**Automated PROCESS_TREE.md generation from manifest:**
```bash
#!/usr/bin/env bash
# Generate PROCESS_TREE.md for a skill from skills-manifest.json
SKILL_NAME="$1"
MANIFEST="$HOME/.agents/skills/skills-manifest.json"

jq -r --arg name "$SKILL_NAME" '
  .skills[] | select(.name == $name) |
  "# Process Tree: \(.displayName // .name)\n\n" +
  "## Entry Point\n- File: \(.path)\n- Version: \(.version)\n\n" +
  "## Portability\n- Verified on: \(.portability | join(", "))\n\n" +
  "## Dependencies\n- Skills: \(.dependencies | join(", ") // "none")\n" +
  "\(if .chain then "- Consumes from: \(.chain.consumesFrom // [] | join(", "))\n- Feeds into: \(.chain.feedsInto // [] | join(", "))" else "" end)\n\n" +
  "## Metadata\n- Type: \(.type // "unknown")\n- Status: \(.status // "unknown")\n- Token Budget: \(.tokenBudget // "N/A")\n"
' "$MANIFEST"
```

## Symlink Behavior

Claude Code resolves symlinks before reading. This means:
- Relative paths in `SKILL.md` (e.g., `../references/foo.md`) resolve RELATIVE TO THE SYMLINK TARGET, not the symlink location
- If core is at `~/.agents/skills/core/code-reviewer/` and symlink is at `~/.claude/skills/code-reviewer/`, `readlink -f ~/.claude/skills/code-reviewer/references/foo.md` resolves correctly

## Claude Code Settings Integration

```json
// ~/.claude/settings.json
{
  "skillsDirectory": "~/.claude/skills",
  "skillsManifest": "~/.agents/skills/skills-manifest.json",
  "skillAutoDiscovery": true,
  "skillCacheEnabled": true
}
```
