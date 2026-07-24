# Frontmatter Normalization

## Problem Statement

Different AI agent terminals support different YAML frontmatter fields. A skill written for Claude Code may use fields (`cursorRules`, `geminiDirectives`, `codexOpenAPI`) that Copilot CLI rejects as unrecognized. Conversely, Copilot CLI's `portability` field may be ignored (harmlessly) by Claude Code.

## Field Compatibility Matrix

| Field | Claude Code | Copilot CLI | Cursor | Codex | Gemini CLI | OpenCode | OpenClaw |
|-------|------------|-------------|--------|-------|-----------|----------|----------|
| `name` | ✅ | ✅ | ✅ | ✅ (→ `info.title`) | ✅ | ✅ | ✅ |
| `description` | ✅ | ✅ | ✅ | ✅ (→ `info.description`) | ✅ | ✅ | ✅ |
| `author` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `license` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `tags` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `type` | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| `status` | ✅ | ✅ (validated) | ✅ | ❌ | ✅ | ✅ | ✅ |
| `version` | ✅ | ✅ | ✅ | ✅ (→ `info.version`) | ✅ | ✅ | ✅ |
| `updated` | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| `token_budget` | ✅ | ✅ (respected) | ✅ | ❌ | ✅ | ✅ | ✅ |
| `portability` | ⚠️ (ignored) | ✅ (required) | ⚠️ (ignored) | ❌ | ⚠️ (ignored) | ✅ | ✅ |
| `chain` | ✅ | ⚠️ (ignored) | ⚠️ (ignored) | ❌ | ⚠️ (ignored) | ✅ | ✅ |
| `cursorRules` | ❌ | ❌ (REJECTS) | ✅ | ❌ | ❌ | ❌ | ❌ |
| `geminiDirectives` | ❌ | ❌ (REJECTS) | ❌ | ❌ | ✅ | ❌ | ❌ |
| `codexOpenAPI` | ❌ | ❌ (REJECTS) | ❌ | ✅ | ❌ | ❌ | ❌ |
| `opencodeTOML` | ❌ | ❌ (REJECTS) | ❌ | ❌ | ❌ | ✅ | ❌ |

**Key:** ✅ = Supported and used | ⚠️ = Supported but ignored/passive | ❌ = Unsupported (may cause rejection or silent drop)

## Normalization Pipeline

```
Source SKILL.md frontmatter
         │
         ▼
┌─────────────────────┐
│ 1. PARSE YAML       │  Parse all frontmatter into a canonical dict
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ 2. STRIP unsupported│  Remove fields not in target agent's supported set
│    fields per agent │  Claude: strip cursorRules, geminiDirectives, codexOpenAPI
│                     │  Copilot: strip cursorRules, geminiDirectives, codexOpenAPI, opencodeTOML
│                     │  Cursor: strip geminiDirectives, codexOpenAPI, opencodeTOML
│                     │  Codex: strip all except name→title, description, version
│                     │  Gemini: strip cursorRules, codexOpenAPI, opencodeTOML
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ 3. MAP common fields│  Map canonical field names to agent equivalents
│    to agent format  │  Codex: name → info.title, description → info.description
│                     │  Gemini: description → directive summary
│                     │  Cursor: tags → cursorRules auto-generation
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ 4. ADD agent-       │  Add fields required by the target agent
│    specific fields  │  Copilot: add portability if missing
│                     │  Cursor: add cursorRules if missing
│                     │  Codex: wrap in OpenAPI info block
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ 5. VALIDATE against │  Check all required fields present
│    agent schema     │  Copilot: name, description, portability required
│                     │  Claude: name, description required
│                     │  Cursor: name, description required
└────────┬────────────┘
         │
         ▼
   Output: agent-normalized SKILL.md
```

## Normalization Script (Python)

```python
#!/usr/bin/env python3
"""Normalize SKILL.md frontmatter for a target agent."""
import yaml
import sys
from pathlib import Path

# Supported fields per agent
AGENT_FIELDS = {
    "claude-code": {"name", "description", "author", "license", "tags", "type", "status", "version", "updated", "token_budget", "chain"},
    "copilot-cli": {"name", "description", "author", "license", "tags", "type", "status", "version", "updated", "token_budget", "portability", "chain"},
    "cursor": {"name", "description", "author", "license", "tags", "type", "status", "version", "updated", "token_budget", "cursorRules", "chain"},
    "codex": {"name", "description", "author", "license", "tags", "version"},
    "gemini-cli": {"name", "description", "author", "license", "tags", "type", "status", "version", "updated", "token_budget", "geminiDirectives"},
    "opencode": {"name", "description", "author", "license", "tags", "type", "status", "version", "updated", "token_budget", "opencodeTOML"},
}

REQUIRED_FIELDS = {
    "claude-code": {"name", "description"},
    "copilot-cli": {"name", "description", "portability"},
    "cursor": {"name", "description"},
    "codex": {"name", "description", "version"},
    "gemini-cli": {"name", "description"},
    "opencode": {"name", "description"},
}

def normalize_frontmatter(skill_path: Path, target_agent: str) -> dict:
    """Parse, strip, map, add, validate for target agent."""
    with open(skill_path) as f:
        content = f.read()
    
    # Extract YAML frontmatter between --- markers
    parts = content.split("---", 2)
    if len(parts) < 3:
        raise ValueError("No YAML frontmatter found")
    
    frontmatter = yaml.safe_load(parts[1])
    supported = AGENT_FIELDS.get(target_agent, set())
    required = REQUIRED_FIELDS.get(target_agent, set())
    
    # Step 2: Strip unsupported fields
    normalized = {k: v for k, v in frontmatter.items() if k in supported}
    
    # Step 3: Map fields (Codex special case)
    if target_agent == "codex":
        normalized = {
            "info": {
                "title": normalized.pop("name", "untitled"),
                "description": normalized.pop("description", ""),
                "version": normalized.pop("version", "1.0.0"),
            },
            **normalized
        }
    
    # Step 4: Add agent-specific fields
    if target_agent == "copilot-cli" and "portability" not in normalized:
        normalized["portability"] = "works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI"
    
    # Step 5: Validate required fields
    missing = required - set(normalized.keys())
    # For Codex, check info block
    if target_agent == "codex" and "info" in normalized:
        missing = required - {"name", "description", "version"}
    
    if missing:
        print(f"WARNING: Missing required fields for {target_agent}: {missing}", file=sys.stderr)
    
    return normalized

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <SKILL.md> <target-agent>", file=sys.stderr)
        sys.exit(1)
    
    result = normalize_frontmatter(Path(sys.argv[1]), sys.argv[2])
    print(yaml.dump(result, default_flow_style=False, sort_keys=False))
```

## Gotchas

1. **Copilot CLI REJECTS unknown fields.** If a field like `cursorRules` leaks into the frontmatter, Copilot CLI will reject the entire skill. Always strip unrecognized fields.

2. **Silent field drops.** Claude Code silently ignores `portability` — no error, no warning, the field just doesn't exist. If your workflow depends on that field being present in Claude Code context, it won't be there.

3. **Codex field mapping is lossy.** Codex maps `name → info.title` which means `name` is no longer a top-level field. If downstream tooling expects `name` at the top level, it will break.

4. **Gemini CLI directive blocks are inline Markdown, not frontmatter.** Gemini CLI reads `## DIRECTIVE: <name>` blocks in the body, not YAML frontmatter. Normalization must handle body content, not just frontmatter.
