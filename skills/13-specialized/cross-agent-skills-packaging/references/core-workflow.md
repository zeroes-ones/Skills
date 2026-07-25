## Core Workflow

<!-- QUICK: 30s -- scan phase titles to understand the process -->
<!-- DEEP: 10+min -->

### Phase 1 (~15 min): Cross-Agent Health Audit
**Input:** Any system with `~/.agents/` or per-agent skill directories
**Steps:** 1) Scan all agent directories for skill symlinks 2) Check for broken symlinks 3) Verify `skills-manifest.json` exists and is up-to-date 4) Check for skills without PROCESS_TREE.md (if Claude Code in portability list) 5) Detect vendor-specific frontmatter leakage
**Output:** Health report with prioritized fixes (broken links, missing files, manifest staleness)

<!-- DEEP: 10+min -->
### Phase 2 (~25 min): Cross-Agent Structure Setup
**Input:** Clean system or migration from single-agent deployment
**Steps:** 1) Create `~/.agents/skills/{core,overrides,cache}/` directory tree 2) Set environment variables (`AGENTS_HOME`, `AGENTS_SKILLS_CORE`, etc.) 3) Move existing skills to `core/` 4) Create per-agent directories (`~/.claude/skills/`, `~/.copilot/skills/`, etc.) 5) Symlink core skills into each agent directory 6) Generate PROCESS_TREE.md for Claude Code-bound skills 7) Generate initial `skills-manifest.json` with lock file
**Output:** Fully wired cross-agent skill deployment with manifest-based discovery

<!-- DEEP: 10+min -->
### Phase 3 (~20 min): Frontmatter Normalization & Deployment
**Input:** Skills in `core/` with full frontmatter
**Steps:** 1) For each skill, for each target agent: parse frontmatter 2) Strip fields not in target agent's supported set 3) Map fields to agent-specific equivalents 4) Add required agent-specific fields 5) Validate output against agent schema 6) Write normalized copy to `cache/<agent>/` 7) Symlink from agent directory to cache (or core if no normalization needed)
**Output:** Every agent has valid, field-correct skill frontmatter

<!-- DEEP: 10+min -->
### Phase 4 (~15 min): CI/CD Integration
**Input:** Git repository with skills in `skills/` directory
**Steps:** 1) Create pre-commit hook: regenerate manifest on SKILL.md changes 2) Create GitHub Actions workflow: deploy on push to main 3) Add compatibility test gate: block deployment if any agent fails load test 4) Add symlink health check to daily CI cron 5) Configure manifest staleness alert (>7 days without regeneration)
**Output:** Fully automated deployment pipeline with quality gates

### Quick Reference: Packaging Commands

```bash
# HEALTH AUDIT: Check for broken symlinks across all agents
find ~/.claude/skills/ ~/.copilot/skills/ ~/.cursor/skills/ ~/.codex/skills/ \
     ~/.gemini/skills/ ~/.opencode/skills/ -type l ! -exec test -e {} \; -print

# MANIFEST: Generate skills-manifest.json from core/ skills
for d in ~/.agents/skills/core/*/; do
  name=$(basename "$d")
  hash=$(find "$d" -type f -exec sha256sum {} \; | sort | sha256sum | cut -d' ' -f1)
  # Extract metadata from SKILL.md frontmatter and write to manifest
done

# SYMLINK: Deploy a skill to all agent directories
SKILL="code-reviewer"
for agent in claude copilot cursor codex gemini opencode openclaw windsurf cody continue aider amazonq; do
  mkdir -p ~/.${agent}/skills/
  ln -sf ~/.agents/skills/core/${SKILL} ~/.${agent}/skills/${SKILL}
done

# NORMALIZE: Strip vendor-specific fields for Copilot CLI
sed -i '/^cursorRules:/d; /^geminiDirectives:/d; /^codexOpenAPI:/d; /^opencodeTOML:/d' \
  ~/.agents/skills/cache/copilot-cli/${SKILL}/SKILL.md

# VERIFY: Check that PROCESS_TREE.md exists for all Claude Code skills
for skill in ~/.agents/skills/core/*/; do
  test -f "${skill}PROCESS_TREE.md" || echo "MISSING PROCESS_TREE.md: ${skill}"
done
```

