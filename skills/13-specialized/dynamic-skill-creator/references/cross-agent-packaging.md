## Cross-Agent Packaging

Generated skills must work across all major AI agent platforms. Add this section to the generated skill's frontmatter:

```yaml
# Cross-Agent Compatibility (append to generated skill frontmatter)
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
```

**Per-agent considerations:**
- **Claude Code:** Requires `PROCESS_TREE.md` in skill directory for advanced routing. Generate this if the skill uses complex multi-phase workflows.
- **Copilot CLI:** Validates frontmatter strictly — ensure no vendor-specific fields leak into the shared format.
- **Cursor:** Integrates with `.cursorrules` — if the skill has domain-specific linting rules, generate a `.cursorrules` snippet.
- **Gemini CLI:** Uses Google-style directives — if the skill has security constraints, format them as "Safety: [constraint]" prefixes.
- **OpenClaw/Codex:** Follow the `~/.agents/skills/` emerging standard with symlink-based sharing.

For full cross-agent deployment, invoke `cross-agent-skills-packaging` after skill generation. The generated skill's frontmatter and structure are already compatible — packaging handles directory setup, manifest generation, and per-agent normalization.
