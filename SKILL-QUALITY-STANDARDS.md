# Skill Quality Standards

> **Author:** Sandeep Kumar Penchala
> **Version:** 2.0.0
> **Purpose:** Define the 10/10 quality bar for every skill in this library

---

## Quality Philosophy

Every skill in this repository must be a skill you'd want to use yourself:

1. **Depth over breadth** — A skill goes deep on its domain. It doesn't skim 20 topics; it masters 5.
2. **Actionable over academic** — Every section tells you what to DO, not what to think about.
3. **Concrete over abstract** — Decision trees, comparison tables, specific metrics, code patterns. No "it depends" without the framework to decide.
4. **Opinionated where justified** — Best practices backed by data and experience. Not all options are equal.
5. **Agent-agnostic** — Works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI, or any agent that reads SKILL.md.
6. **Domain-agnostic** — Universal frameworks applicable to any industry (healthcare, fintech, gaming, e-commerce, government, open source). Industry specifics live in `references/`, not in core SKILL.md.
7. **Scale-aware** — Every skill covers Solo → Small → Medium → Enterprise. What's overkill at one scale is essential at another.
8. **Coordination-aware** — Every skill knows which other skills it must coordinate with, when to escalate, and what to communicate at each scale.

## File Structure

```
skill-name/
├── SKILL.md              # Instructions (~250-550 lines, ~3000-4000 token budget, dense, actionable)
├── scripts/              # Deterministic tools (Python/bash)
│   └── analyze.py
├── references/           # Deep knowledge loaded as needed
│   ├── guide-1.md
│   └── guide-2.md
└── assets/               # Templates, samples, configuration
    ├── template-1.md
    └── sample.json
```

## The 10/10 Quality Bar

A skill earns 10/10 only when it passes ALL of these tests:

### The 30-Second Test
Someone who has never used this skill can open it, read the quickstart section, and produce something useful in under a minute. The quickstart must be a **single copy-paste executable block** — not "install X, then Y, then run Z".

### The Footgun Test
Someone who has used this skill 10 times still discovers a gotcha they didn't know about. This means footguns must include **war stories** (real failure narratives with before/after code) and **error decoders** (exact error message → root cause → fix).

### The Handoff Test
The output of this skill is in the exact format the next skill in the chain expects. Each skill defines its output contract clearly — file format, schema, location — so the consuming skill knows exactly what to expect.

### The Checklist Test
Running the checklist catches all common errors before they reach production. Every checklist item references a **numbered standard** so the user can go directly to the rule and fix it.

### The Neighbor Test
Reading this skill tells you exactly which skill to use next, what that skill needs from you, and what it produces. Cross-skill integration examples show actual command sequences.

### Progressive Disclosure Test
Every section has three depth levels marked inline:
- `<!-- QUICK: 30s -->` — A one-liner or small table. The entire skill is parseable in 30 seconds.
- `<!-- STANDARD: 3min -->` — Working knowledge with code examples, commands, and metrics.
- `<!-- DEEP: 10+min -->` — Edge cases, war stories, failure narratives, advanced patterns.

### The Token Budget Test
The skill's frontmatter declares a `token_budget` (how many tokens the agent should expect to spend). Quick sections are under 500 tokens. The full skill is under 3000 tokens.

### The "What Good Looks Like" Test
Every Quickstart section ends with a concrete description of what success produces — the visual outcome, expected file size, opened in what app, etc.

---

## Frontmatter Requirements

Every SKILL.md MUST start with:

```yaml
---
name: "kebab-case-name"
description: "One line: who uses this, when, for what, what it produces. 200 chars max."
author: Sandeep Kumar Penchala
type: archetype           # strategy | product | design | architecture | development | quality | devops | security | data | growth | legal | operations | specialized
status: stable            # draft | stable | deprecated
version: "x.y.z"
updated: YYYY-MM-DD
tags: [tag1, tag2]
dependencies:
  tools: [tool1, tool2]
  packages: [package1]
  permissions: [perm1]
output:
  type: "file-format"
  path_hint: "path/"
chain:
  consumes_from: ["skill-a"]
  feeds_into: ["skill-b"]
  alternatives: ["skill-c"]
---
```

---

## Critical Additions for 10/10

Every skill MUST include these elements that separate good (7/10) skills from 10/10:

### 1. Progressive Disclosure Markers
```markdown
## Section Title
<!-- QUICK: 30s -->
One-liner summary here.

<!-- STANDARD: 3min -->
Detailed explanation with code/commands here.

<!-- DEEP: 10+min -->
War story, edge cases, failure narrative here.
```

### 2. Error Decoders
```markdown
### Error Decoder
| Error Message | Root Cause | Fix |
|--------------|------------|-----|
| "Error X" | What actually went wrong | Exact command/code fix |
```

### 3. Time Estimates on Workflow Steps
```markdown
### Phase 2: Implementation (~30 min)
1. **Do:** ...
2. **Verify:** ...
3. **Recover:** ...
```

### 4. "What Good Looks Like"
```markdown
**What good looks like:** The output opens correctly in the expected tool, structure matches requirements, no placeholder content remains.
```

### 5. Cross-Skill Integration Examples
```markdown
### Cross-Skill Integration
```bash
# Run skill A → produce output → pass to skill B
skill-a-command && skill-b-command
```
```

### 6. Token Budget in Frontmatter
```yaml
token_budget: 3500  # estimated tokens this skill consumes (~250-550 lines)
```

### 7. Domain-Specific Checklist Reference IDs
```markdown
## Production Readiness Checklist
- [ ] **[API1]** OpenAPI 3.1 specification complete with all paths, schemas, and security schemes
- [ ] **[API2]** Error responses follow RFC 7807 Problem Details across all endpoints
...
- [ ] **[API14]** Consumer-facing changelog maintained with deprecation timelines
```
IDs use domain prefixes (API, EM, DE, VP, SE, etc.) for traceability across skills.

### 8. Before/After Code in Footguns
```markdown
| Footgun | Broken | Fixed |
|---------|--------|-------|
| Issue | ```broken code``` | ```fixed code``` |
```

---

## SKILL.md Quality Checklist (10/10)

Every SKILL.md must pass ALL of these gates:

### Structure
- [ ] YAML frontmatter with ALL required fields including token_budget, type, version, updated, chain
- [ ] `<!-- QUICK: 30s -->` markers on every section — entire skill parseable in 30 seconds
- [ ] `<!-- STANDARD: 3min -->` markers on every section — working knowledge tier
- [ ] `<!-- DEEP: 10+min -->` markers on at least 3 sections — war stories and edge cases
- [ ] `## When to Use` — 5+ specific trigger conditions with examples
- [ ] `## Decision Trees` — At least 1 ASCII decision tree for key choices
- [ ] `## Core Workflow` — 3-6 phases, each with concrete steps, time estimates, and outputs
- [ ] `## Best Practices` — 8+ specific, actionable practices
- [ ] `## Error Decoder` — At least 3 common errors mapped to root causes and fixes
- [ ] `## Production Checklist` — 12+ items, each referencing a numbered standard
- [ ] `## Cross-Skill Coordination` — Actual command/snippet demonstrated
- [ ] `## What Good Looks Like` — Concrete description of success output
- [ ] `## References` — Lists all references/ and assets/ files with descriptions

### Content Quality
- [ ] No filler paragraphs — every sentence carries information
- [ ] Decision frameworks included (when X, do Y; when A, prefer B)
- [ ] Trade-off analysis present (not just "use this", but "use this when... vs that when...")
- [ ] Specific metrics mentioned (not "fast" but "< 100ms p95")
- [ ] Anti-patterns explicitly called out with before/after code
- [ ] At least one comparison table or decision matrix
- [ ] Language/stack specific guidance where relevant

### References Quality
- [ ] Each reference document is 50+ lines of dense content
- [ ] References are modular — loaded only when needed
- [ ] References link back to SKILL.md concepts
- [ ] References include code examples, config samples, or templates

### Assets Quality
- [ ] Templates use `{{placeholder}}` syntax for fill-in fields
- [ ] Templates include usage instructions and examples
- [ ] Configuration samples are copy-paste ready

---

## Anti-Patterns (What to Avoid)

| Anti-Pattern | Example (7/10) | Fix (10/10) |
|---|---|---|
| **Vague advice** | "Write good tests" | "Write tests for: happy path, null inputs, boundary values, error states, concurrency edge cases. Each test covers exactly one scenario." |
| **Missing tradeoffs** | "Use microservices" | "Use microservices when: team size > 20, independent deploy needs, different scaling profiles. Use monolith when: team < 8, tight coupling, simple domain" |
| **Academic fluff** | "Consider the implications" | "Bad architecture costs: 40% longer feature delivery after year 1, 3x onboarding time. Good architecture: < 1 day to add new API endpoint." |
| **No metrics** | "Make it fast" | "p95 < 200ms, p99 < 500ms, cold start < 2s, 60fps animations" |
| **One-size-fits-all** | "Always use TypeScript" | "TypeScript: teams > 3, long-lived projects, public APIs. JavaScript: quick scripts, prototypes, serverless functions < 100 lines" |
| **Missing verification** | "Deploy to production" | "Deploy: canary 5% → monitor 10min → 25% → monitor 10min → 100%. Rollback if: error rate > 0.1% OR p95 latency +20%" |
| **No war story** | "Caching can cause staleness" | "Engineer spent 4 hours debugging stale cache: Redis TTL was 1 hour but documentation said 5 minutes. Root cause: config file deployed from stale branch." |
| **No error decoder** | "Handle errors properly" | "Common error: `ECONNREFUSED` → DB not started. Fix: `docker compose up -d db` before running service." |
| **No time estimates** | "Set up CI/CD" | "Set up CI/CD (~45 min): 15 min write config, 10 min test pipeline, 20 min secure secrets" |
| **No what-good-looks-like** | "Create the API" | "What good looks like: `curl http://localhost:8000/health` returns `{\"status\":\"ok\"}` within 5ms. OpenAPI spec renders in Swagger UI at `/docs`." |

---

## Quality Grades

| Grade | Criteria |
|---|---|
| **10/10** | All checklist items ✓, all 10/10 tests pass, war stories present, error decoders present, progressive disclosure complete, token budget declared, "what good looks like" in every section |
| **A (Production)** | All checklist items ✓, 1+ reference doc, 1+ asset, basic progressive disclosure |
| **B (Usable)** | Most checklist items ✓, basic references |
| **C (Draft)** | SKILL.md exists but lacks depth |
| **F (Reject)** | Generic content, no depth, missing structure |

**Target: Every skill in this repository must be 10/10 grade.**

---

## Review Process

1. **Self-review:** Author runs through 10/10 checklist before submission
2. **Peer review:** Another domain expert reviews for depth, accuracy, and war story authenticity
3. **Agent testing:** Skill is tested with at least one AI agent (Claude Code, Copilot CLI) to verify it produces correct outputs
4. **30-second test:** Someone unfamiliar with the skill reads only the Quick sections and can produce useful output
5. **Footgun test:** A 10-time user reviews the footgun section and confirms they learned something new
6. **Periodic audit:** Skills reviewed quarterly against latest industry standards

---

*This document itself should be reviewed and updated as the skill library matures.*
