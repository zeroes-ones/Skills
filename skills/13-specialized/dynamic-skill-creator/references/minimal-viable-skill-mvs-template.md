## Minimal Viable Skill (MVS) Template

When speed is critical and domain depth can be added later, produce this compact but complete structure. MVS is 10/10 quality in its sections but domain-light — fewer gotchas, fewer ground rules, fewer decision trees. Use only when the user explicitly requests speed or the domain is well-understood.

```markdown
---
name: {skill-name}
description: {triggers-only one-paragraph description}
author: Sandeep Kumar Penchala
license: MIT
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
type: {category-type}
status: stable
version: 1.0.0
updated: {date}
tags: [{3-5 tags}]
token_budget: 3000
chain:
  consumes_from: [{at least 2}]
  feeds_into: [{at least 2}]
  alternatives: []
---

# {Skill Title}
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.
