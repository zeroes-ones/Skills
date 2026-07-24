# Skills Manifest Format: `skills-manifest.json`

## Overview

`skills-manifest.json` is the master index that enables agent auto-discovery of skills in `~/.agents/skills/`. Agents read this manifest at startup to know what skills are available without scanning the entire filesystem.

## JSON Schema

```json
{
  "$schema": "https://agents-standard.org/skills-manifest-v1.schema.json",
  "version": "1.0.0",
  "generated": "2026-07-24T12:00:00Z",
  "generator": "cross-agent-skills-packaging/1.0.0",
  "skills": [
    {
      "name": "code-reviewer",
      "displayName": "Code Reviewer",
      "version": "2.1.0",
      "description": "Six-dimension code review with security, performance, quality grading",
      "author": "Sandeep Kumar Penchala",
      "license": "MIT",
      "type": "quality",
      "status": "stable",
      "path": "core/code-reviewer/SKILL.md",
      "sha256": "a1b2c3d4e5f6...",
      "dependencies": [],
      "tags": ["code-review", "security", "quality", "six-dimension"],
      "portability": ["claude-code", "copilot-cli", "cursor", "opencode", "openclaw", "gemini-cli"],
      "tokenBudget": 4000,
      "chain": {
        "consumesFrom": ["api-designer", "backend-developer"],
        "feedsInto": ["qa-engineer", "security-reviewer"]
      },
      "overrides": {
        "gemini-cli": "overrides/gemini-cli/code-reviewer/SKILL.md",
        "codex": "overrides/codex/code-reviewer/SKILL.md"
      }
    }
  ],
  "conflicts": [],
  "stats": {
    "totalSkills": 42,
    "withOverrides": 3,
    "brokenSymlinks": 0,
    "lastFullScan": "2026-07-24T12:00:00Z"
  }
}
```

## Field Reference

### Top-Level Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `$schema` | string | No | JSON Schema URL for validation |
| `version` | string | Yes | Manifest format version (semver) |
| `generated` | string | Yes | ISO 8601 timestamp of manifest generation |
| `generator` | string | Yes | Tool/version that generated the manifest |
| `skills` | array | Yes | Array of skill entries |
| `conflicts` | array | No | Array of conflict entries (see below) |
| `stats` | object | No | Aggregate statistics |

### Skill Entry Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Machine-readable skill identifier (kebab-case) |
| `displayName` | string | No | Human-readable name |
| `version` | string | Yes | Semantic version of the skill |
| `description` | string | Yes | One-line description for agent routing |
| `author` | string | No | Skill author |
| `license` | string | No | SPDX license identifier |
| `type` | string | No | Skill category (strategy, development, quality, etc.) |
| `status` | string | No | stable, beta, deprecated |
| `path` | string | Yes | Relative path from skills root to SKILL.md |
| `sha256` | string | Yes | SHA-256 hash of the skill directory contents |
| `dependencies` | array | No | Names of skills this skill depends on |
| `tags` | array | No | Search/discovery tags |
| `portability` | array | No | Agent terminals this skill is verified on |
| `tokenBudget` | number | No | Estimated token consumption |
| `chain` | object | No | `consumesFrom` and `feedsInto` arrays |
| `overrides` | object | No | Map of agent → override path |
| `deprecated` | object | No | `since`, `replacedBy`, `message` for deprecated skills |

### Conflict Entry Fields

```json
{
  "conflicts": [
    {
      "skill": "code-reviewer",
      "agents": ["claude-code", "copilot-cli"],
      "field": "token_budget",
      "claudeValue": 4000,
      "copilotValue": 3000,
      "resolution": "per-agent-override",
      "resolvedAt": "2026-07-24T12:00:00Z"
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `skill` | string | Skill name with conflict |
| `agents` | array | Agents that disagree |
| `field` | string | Conflicting field name |
| `<agent>Value` | any | Per-agent values for the conflicting field |
| `resolution` | string | How the conflict was resolved (per-agent-override, common-subset, core-wins) |
| `resolvedAt` | string | When the conflict was resolved |

## Incremental Manifest Rebuild

When skills change, regenerate only the affected entries rather than the entire manifest:

```bash
#!/usr/bin/env bash
# Incremental manifest update
MANIFEST="$HOME/.agents/skills/skills-manifest.json"
LOCK="$HOME/.agents/skills/skills-manifest.lock"

for skill_dir in "$HOME/.agents/skills/core"/*/; do
  name=$(basename "$skill_dir")
  current_hash=$(find "$skill_dir" -type f -exec sha256sum {} \; | sort | sha256sum | cut -d' ' -f1)
  stored_hash=$(jq -r ".skills[] | select(.name==\"$name\") | .sha256" "$LOCK" 2>/dev/null || echo "")

  if [ "$current_hash" != "$stored_hash" ]; then
    echo "Changed: $name (rebuilding entry)"
    # Regenerate entry for this skill
    # ... (extract metadata from SKILL.md, compute new hash, update manifest)
  fi
done
```

## Version Tracking

The manifest lock file (`skills-manifest.lock`) pins versions:

```json
{
  "code-reviewer": {
    "version": "2.1.0",
    "sha256": "a1b2c3d4e5f6...",
    "lastModified": "2026-07-24T12:00:00Z"
  }
}
```

## Agent Integration

Agents read the manifest at startup:

- **Claude Code:** Reads `skills-manifest.json` to populate the `available_skills` block in its system prompt.
- **Copilot CLI:** Reads manifest to discover skills; validates `portability` array includes "copilot-cli".
- **Cursor:** Reads manifest to generate `.cursorrules` `@skill:` directives.
- **Codex:** Reads manifest to generate `skills.json` at `.codex/skills/skills.json`.
- **Gemini CLI:** Reads manifest to populate `settings.yaml` skills block.
