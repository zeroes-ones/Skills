# Per-Agent Directory Mapping

Complete mapping of skill directories for every known AI agent terminal that supports skill loading. All paths are relative to the user's home directory (`~`).

## Directory Convention Table

| Agent Terminal | Skill Directory | Config File | Frontmatter Format | Symlink Safe? | Auto-Discovery |
|---------------|----------------|-------------|-------------------|---------------|----------------|
| **Claude Code** | `~/.claude/skills/` | `~/.claude/settings.json` | YAML frontmatter | Yes | Via `PROCESS_TREE.md` |
| **Copilot CLI** | `~/.copilot/skills/` | `~/.copilot/config.yml` | YAML frontmatter (validated) | Yes | Via `available_skills` block |
| **Cursor** | `~/.cursor/skills/` | `~/.cursorrules` | YAML + `.cursorrules` directives | Yes | Via `.cursorrules` index |
| **OpenAI Codex** | `~/.codex/skills/` | `~/.codex/config.json` | OpenAPI-style descriptors | Yes | Via `skills.json` |
| **Gemini CLI** | `~/.gemini/skills/` | `~/.gemini/settings.yaml` | Google-style directive blocks | Partial | Via `skills.yaml` |
| **OpenCode** | `~/.opencode/skills/` | `~/.opencode/config.toml` | TOML + Markdown hybrid | Yes | Via config |
| **OpenClaw** | `~/.openclaw/skills/` | `~/.openclaw/config.json` | JSON + Markdown | Yes | Via config |
| **Windsurf** | `~/.windsurf/skills/` | `~/.windsurf/config.json` | JSON | Yes | Via config |
| **Cody (Sourcegraph)** | `~/.cody/skills/` | `~/.cody/config.json` | JSON | Yes | Via config |
| **Continue** | `~/.continue/skills/` | `~/.continue/config.json` | YAML | Yes | Via config |
| **Aider** | `~/.aider/skills/` | `~/.aider.conf.yml` | YAML | Yes | Via config |
| **Amazon Q Developer** | `~/.amazonq/skills/` | `~/.amazonq/config.json` | JSON | Yes | Via config |
| **Tabby** | `~/.tabby/skills/` | `~/.tabby/config.toml` | Plugin manifest | Plugin-based | Via plugin registry |
| **Codeium** | `~/.codeium/skills/` | `~/.codeium/config.json` | Plugin manifest | Plugin-based | Via plugin registry |
| **Cody (JetBrains)** | `<IDE config>/cody/skills/` | IDE settings | JSON | No (IDE-managed) | Via IDE plugin |

## Agent-Specific Quirks

### Claude Code
- **PROCESS_TREE.md convention:** Skill structure MUST include a `PROCESS_TREE.md` at the root of each skill directory for Claude Code to detect it. Without this file, the skill is invisible to Claude Code even if `SKILL.md` exists and the symlink is valid.
- **Settings integration:** `~/.claude/settings.json` can specify `"skillsDirectory"` override.
- **Frontmatter:** Uses standard YAML. Fields: `name`, `description`, `license`, `tags`, `author`, `type`, `status`, `version`.
- **Issue #31005:** Tracking Claude Code's `PROCESS_TREE.md` requirement — may be deprecated in favor of manifest-based discovery.

### Copilot CLI
- **Frontmatter validation:** Copilot CLI validates frontmatter fields and will REJECT skills with unrecognized fields. Vendor-specific fields from other agents (e.g., `cursorRules`, `geminiDirectives`) MUST be stripped before deployment to Copilot CLI.
- **Portability field:** Copilot CLI requires a `portability` field in frontmatter (e.g., `portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI`).
- **Skill invocation:** Skills are invoked via `<skill>` blocks in the system prompt, mapped from the `available_skills` configuration. The skill name in the manifest MUST match exactly.
- **Token budget:** Respects `token_budget` field if present.

### Cursor
- **.cursorrules integration:** Skills can be referenced from `.cursorrules` with directives like `@skill:code-reviewer`. The `.cursor/skills/` directory is scanned at startup.
- **Frontmatter:** Uses standard YAML. Additional fields: `cursorRules` (array of `.cursorrules` directives to auto-generate).
- **Index file:** `.cursor/skills/index.json` for faster discovery (generated, not manual).

### OpenAI Codex
- **OpenAPI-style descriptors:** Codex expects skill metadata in OpenAPI-influenced format. A `skills.json` at `.codex/skills/skills.json` acts as an index.
- **Frontmatter quirks:** Requires `openapi`-style `info` block with `title`, `version`, `description`. Maps `name` → `info.title`.

### Gemini CLI
- **Google-style directives:** Uses directive blocks in the format `## DIRECTIVE: <name>` within SKILL.md. The `description` field in YAML frontmatter is used as the directive summary.
- **Settings:** `~/.gemini/settings.yaml` with `skills:` block for enable/disable.
- **Partial symlink safety:** Gemini CLI may resolve symlinks to their target before reading, which can cause issues with relative reference paths. Use absolute paths in references when targeting Gemini CLI.

## Symlink Strategy Per Agent

| Agent | Symlink Strategy | Notes |
|-------|-----------------|-------|
| Claude Code | `ln -s ~/.agents/skills/core/<skill> ~/.claude/skills/<skill>` | Add `PROCESS_TREE.md` in skill root |
| Copilot CLI | `ln -s ~/.agents/skills/core/<skill> ~/.copilot/skills/<skill>` | Strip unrecognized frontmatter fields |
| Cursor | `ln -s ~/.agents/skills/core/<skill> ~/.cursor/skills/<skill>` | Generate `.cursorrules` directives |
| Codex | `ln -s ~/.agents/skills/core/<skill> ~/.codex/skills/<skill>` | Generate `skills.json` index |
| Gemini CLI | `ln -s ~/.agents/skills/core/<skill> ~/.gemini/skills/<skill>` | Use absolute reference paths |
| Others | `ln -s ~/.agents/skills/core/<skill> ~/.<agent>/skills/<skill>` | Standard symlink pattern |

## Quick Setup Command

```bash
# Symlink a shared skill to all agent directories
for agent in claude copilot cursor codex gemini opencode openclaw windsurf cody continue aider amazonq; do
  mkdir -p ~/.${agent}/skills/
  ln -sf ~/.agents/skills/core/cross-agent-skills-packaging ~/.${agent}/skills/cross-agent-skills-packaging
done
```
