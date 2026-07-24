# Cross-Agent Directory Standard: `~/.agents/skills/`

## Overview

`~/.agents/skills/` is the emerging de facto standard for sharing skill definitions across 15+ AI agent terminals. It provides a single source of truth for skill content while allowing per-agent overrides and normalization.

## Directory Structure

```
~/.agents/
├── skills/
│   ├── core/                    # Shared skill definitions (symlinked into agent dirs)
│   │   ├── code-reviewer/
│   │   │   ├── SKILL.md
│   │   │   └── references/
│   │   ├── api-designer/
│   │   │   ├── SKILL.md
│   │   │   └── references/
│   │   └── ...
│   ├── overrides/               # Per-agent overrides (copied, not symlinked)
│   │   ├── claude-code/
│   │   │   └── code-reviewer/
│   │   │       └── SKILL.md     # Claude-specific frontmatter or content
│   │   ├── copilot-cli/
│   │   │   └── api-designer/
│   │   │       └── SKILL.md     # Copilot-specific frontmatter
│   │   ├── cursor/
│   │   ├── codex/
│   │   ├── gemini-cli/
│   │   └── openclaw/
│   ├── cache/                   # Pre-processed skill bundles
│   │   ├── claude-code/
│   │   ├── copilot-cli/
│   │   └── ...
│   ├── skills-manifest.json     # Master manifest for auto-discovery
│   └── skills-manifest.lock     # Pinned versions with content hashes
├── state/                       # Cross-agent state (handoffs, ledgers, contracts)
├── artifacts/                   # Shared output files (ADRs, specs, configs)
├── logs/                        # Agent execution logs
└── tmp/                         # Temporary working files (auto-cleaned)
```

## Key Principles

1. **Core is canonical.** `~/.agents/skills/core/` holds the authoritative skill definitions. Every agent symlinks from here for shared skills.

2. **Overrides are exceptions.** `~/.agents/skills/overrides/` exists only for agent-specific differences that cannot be resolved through frontmatter normalization. Overrides are copied (not symlinked) to prevent accidental core modification.

3. **Manifest drives discovery.** Agents read `skills-manifest.json` to discover available skills without scanning the entire filesystem.

4. **Content hashing prevents drift.** `skills-manifest.lock` stores SHA-256 hashes of each skill file. Regenerate the manifest when hashes change.

5. **Cache is generated.** `cache/` directories are build artifacts — never edit them directly. They're produced by the normalization pipeline from core + overrides.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `AGENTS_HOME` | `~/.agents` | Root of agent directory tree |
| `AGENTS_SKILLS_CORE` | `$AGENTS_HOME/skills/core` | Canonical skill definitions |
| `AGENTS_SKILLS_OVERRIDES` | `$AGENTS_HOME/skills/overrides` | Per-agent overrides |
| `AGENTS_SKILLS_CACHE` | `$AGENTS_HOME/skills/cache` | Pre-processed bundles |
| `AGENTS_SKILLS_MANIFEST` | `$AGENTS_HOME/skills/skills-manifest.json` | Manifest path |

## Manifest Format

See [skills-manifest-format.md](skills-manifest-format.md) for the full JSON schema.

## Adoption Status (as of 2026-07)

| Agent | Status | Notes |
|-------|--------|-------|
| Claude Code | Native support | Reads from `.claude/skills/`, supports symlinks |
| Copilot CLI | Native support | Reads from `.copilot/skills/`, validates frontmatter |
| Cursor | Via `.cursorrules` | Reads `.cursor/skills/` with rules integration |
| OpenAI Codex | Via symlink | Reads `.codex/skills/` |
| Gemini CLI | Via symlink | Reads `.gemini/skills/` |
| OpenCode | Native support | Reads `.opencode/skills/` |
| OpenClaw | Via symlink | Reads `.openclaw/skills/` |
| Windsurf | Via symlink | Reads `.windsurf/skills/` |
| Cody (Sourcegraph) | Via symlink | Reads `.cody/skills/` |
| Continue | Via symlink | Reads `.continue/skills/` |
| Aider | Via symlink | Reads `.aider/skills/` |
| Amazon Q Developer | Via symlink | Reads `.amazonq/skills/` |
| Tabby | Partial | Plugin-based loading |
| Codeium | Partial | Plugin-based loading |
| Cody (JetBrains) | Via symlink | Reads `.cody/skills/` in IDE config |

## Integrity Verification

```bash
# Verify no symlinks are broken
find ~/.agents/skills/core -type l -! -exec test -e {} \; -print

# Verify manifest matches filesystem
sha256sum ~/.agents/skills/core/*/SKILL.md | diff - <(jq -r '.skills[] | "\(.sha256)  \(.path)"' ~/.agents/skills/skills-manifest.json)
```
