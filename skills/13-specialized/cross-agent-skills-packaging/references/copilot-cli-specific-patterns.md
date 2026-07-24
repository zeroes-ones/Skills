# Copilot CLI Specific Patterns

## `.copilot/skills/` Directory

Copilot CLI reads skills from `~/.copilot/skills/`. Skills are loaded at session start and rendered in the system prompt's `<available_skills>` block. Each skill is invoked via `<skill>` tags.

## Frontmatter Validation

Copilot CLI performs **strict frontmatter validation** — unlike Claude Code (which silently ignores unknown fields), Copilot CLI will **REJECT** a skill if it contains unrecognized frontmatter fields.

**Fields that Copilot CLI REJECTS:**
- `cursorRules` (Cursor-specific)
- `geminiDirectives` (Gemini CLI-specific)
- `codexOpenAPI` (Codex-specific)
- `opencodeTOML` (OpenCode-specific)
- Any field not in its recognized set

**Fields that Copilot CLI REQUIRES:**
- `name` — skill identifier (must match directory name)
- `description` — one-line routing description
- `portability` — list of supported agents

**Fields that Copilot CLI ACCEPTS (optional):**
- `author`, `license`, `tags`, `type`, `status`, `version`, `updated`, `token_budget`, `chain`

## Portability Field

Copilot CLI REQUIRES the `portability` field in frontmatter:

```yaml
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
```

Without this field, Copilot CLI will log a warning and may not load the skill. The value should list all agent terminals where the skill has been verified.

## Skill Invocation Mechanics

When Copilot CLI loads a skill, it:
1. Parses the YAML frontmatter
2. Validates all fields against its recognized set
3. Rejects skills with unrecognized fields (fatal error)
4. Extracts `name`, `description`, `portability`
5. Renders the skill in the `<available_skills>` block
6. Makes the skill invocable via `<skill>` tags in user messages

**Example available_skills block rendered by Copilot CLI:**
```xml
<available_skills>
<skill>
  <name>code-reviewer</name>
  <description>Six-dimension code review covering security, performance, quality...</description>
  <location>user</location>
</skill>
</available_skills>
```

## Token Budget

Copilot CLI respects the `token_budget` field if present. It uses this value to estimate context window consumption and may prioritize or deprioritize skills based on available context.

## Pre-Deployment Checklist for Copilot CLI

Before deploying a skill to Copilot CLI:

1. **Strip all vendor-specific fields:** Remove `cursorRules`, `geminiDirectives`, `codexOpenAPI`, `opencodeTOML`
2. **Add `portability` field:** List all verified agent terminals
3. **Validate YAML syntax:** Frontmatter must be valid YAML between `---` delimiters
4. **Check field types:** `tags` must be an array, `version` must be a string, `token_budget` must be a number
5. **Test load:** Actually load the skill in Copilot CLI and verify it appears in `<available_skills>`

## Common Deployment Failures

| Error | Cause | Fix |
|-------|-------|-----|
| "Unrecognized field: cursorRules" | Cursor-specific field in shared skill | Strip `cursorRules` before deploying to Copilot |
| "Missing required field: portability" | `portability` field absent | Add `portability: works with Claude Code, Copilot CLI, Cursor...` |
| "Invalid YAML in frontmatter" | Malformed YAML (indentation, special chars) | Validate with `yamllint` |
| "Skill not found in available_skills" | Directory name doesn't match `name` field | Ensure directory name == `name` in frontmatter |
| "tags must be an array" | `tags: code-review` (string, not array) | Change to `tags: [code-review]` |

## Gotcha: Silent Skill Drop

If a skill passes Copilot CLI's frontmatter validation but the body content contains directives that conflict with Copilot CLI's prompt format (e.g., `<skill>` tags embedded in Markdown without escaping), the skill loads but produces garbled output. Always test skills end-to-end in Copilot CLI, not just frontmatter validation.

## Gotcha: portability Field Drift

Teams sometimes update the `portability` field to add a new agent but forget to actually test on that agent. The field says "works with Gemini CLI" but the skill fails there. The `portability` field is a claim, not a guarantee — always verify with the compatibility testing matrix.
