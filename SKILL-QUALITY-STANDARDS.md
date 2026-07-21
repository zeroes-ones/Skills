# Skill Quality Standards

> **Author:** Sandeep Kumar Penchala  
> **Version:** 1.0.0  
> **Purpose:** Define the world-class quality bar for every skill in this library

---

## Quality Philosophy

Every skill in this repository must be **the best skill of its kind in the world**. This means:

1. **Depth over breadth** — A skill goes deep on its domain. It doesn't skim 20 topics; it masters 5.
2. **Actionable over academic** — Every section tells you what to DO, not what to think about.
3. **Concrete over abstract** — Decision trees, comparison tables, specific metrics, code patterns. No "it depends" without the framework to decide.
4. **Opinionated where justified** — Best practices backed by data and experience. Not all options are equal.
5. **Agent-agnostic** — Works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI, or any agent that reads SKILL.md.
6. **Domain-agnostic** — Universal frameworks applicable to ANY industry (healthcare, fintech, gaming, e-commerce, government, open source). Industry specifics live in `references/`, not in core SKILL.md.
7. **Scale-aware** — Every skill covers Solo → Small → Medium → Enterprise. What's overkill at one scale is essential at another.
8. **Coordination-aware** — Every skill knows which other skills it must coordinate with, when to escalate, and what to communicate at each scale.

## File Structure

```
skill-name/
├── SKILL.md              # Instructions (~150-250 lines, dense, actionable)
├── scripts/              # Deterministic tools (Python/bash)
│   └── analyze.py
├── references/           # Deep knowledge loaded as needed
│   ├── guide-1.md
│   └── guide-2.md
└── assets/               # Templates, samples, configuration
    ├── template-1.md
    └── sample.json
```

## SKILL.md Quality Checklist

Every SKILL.md must pass ALL of these gates:

### Structure
- [ ] YAML frontmatter: `name` (kebab-case), `description` (one line with trigger keywords), `author: Sandeep Kumar Penchala`
- [ ] `## When to Use` — 5+ specific trigger conditions with examples
- [ ] `## Core Workflow` — 3-6 phases, each with concrete steps and outputs
- [ ] `## Best Practices` — 8+ specific, actionable practices
- [ ] `## Production Checklist` — 12+ items, each checkable with specific criteria
- [ ] `## References` — Lists all references/ and assets/ files with descriptions

### Content Quality
- [ ] No filler paragraphs — every sentence carries information
- [ ] Decision frameworks included (when X, do Y; when A, prefer B)
- [ ] Trade-off analysis present (not just "use this", but "use this when... vs that when...")
- [ ] Specific metrics mentioned (not "fast" but "< 100ms p95")
- [ ] Anti-patterns explicitly called out with fixes
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

## Anti-Patterns (What to Avoid)

| Anti-Pattern | Example | Fix |
|---|---|---|
| **Vague advice** | "Write good tests" | "Write tests for: happy path, null inputs, boundary values, error states, concurrency edge cases" |
| **Missing tradeoffs** | "Use microservices" | "Use microservices when: team size > 20, independent deploy needs, different scaling profiles. Use monolith when: team < 8, tight coupling, simple domain" |
| **Academic fluff** | "Consider the implications of architectural decisions" | "Bad architecture costs: 40% longer feature delivery after year 1, 3x onboarding time. Good architecture: < 1 day to add new API endpoint" |
| **No metrics** | "Make it fast" | "p95 < 200ms, p99 < 500ms, cold start < 2s, 60fps animations" |
| **One-size-fits-all** | "Always use TypeScript" | "TypeScript: teams > 3, long-lived projects, public APIs. JavaScript: quick scripts, prototypes, serverless functions < 100 lines" |
| **Missing verification** | "Deploy to production" | "Deploy: canary 5% → monitor 10min → 25% → monitor 10min → 100%. Rollback if: error rate > 0.1% OR p95 latency +20%" |

## Domain Coverage Standards

Each of the 13 domains must cover the full company value chain:

| Domain | Thinking Level | Skills Required |
|---|---|---|
| 01-strategy | CEO/CTO/VP | Vision, strategy, fundraising, org design, competitive analysis |
| 02-product | CPO/PM/UXR | Discovery, prioritization, user research, spec writing |
| 03-design | Design Director | Design systems, interaction, visual, accessibility, brand |
| 04-architecture | Principal/Architect | System design, API design, database design, decisions |
| 05-development | Senior/Staff Engineer | Backend, frontend, mobile, fullstack |
| 06-quality | QA Lead/Security | Testing, code review, security review |
| 07-devops | DevOps/SRE | CI/CD, observability, containers, cloud, infra |
| 08-security | CISO/Security | Threat modeling, compliance, incident response |
| 09-data | Data/ML Engineer | Data pipelines, analytics, ML/AI |
| 10-growth | Growth/SEO | SEO, content, growth experiments |
| 11-legal | GC/Privacy | Legal, GDPR, regulatory compliance |
| 12-operations | PM/Scrum/Writer | Project mgmt, agile, documentation |
| 13-specialized | Specialist | Monorepo, migration, performance, chaos |

## Grading Rubric

| Grade | Criteria |
|---|---|
| **A+ (World-class)** | All checklist items ✓, 3+ reference docs, 2+ assets, decision matrices, anti-patterns, metrics throughout |
| **A (Production)** | All checklist items ✓, 1+ reference doc, 1+ asset |
| **B (Usable)** | Most checklist items ✓, basic references |
| **C (Draft)** | SKILL.md exists but lacks depth |
| **F (Reject)** | Generic content, no depth, missing structure |

**Target: Every skill in this repository must be Grade A or above.**

## Review Process

1. **Self-review:** Author runs through checklist before submission
2. **Peer review:** Another domain expert reviews for depth and accuracy
3. **Agent testing:** Skill is tested with at least one AI agent (Claude Code, Copilot CLI) to verify it produces correct outputs
4. **Periodic audit:** Skills reviewed quarterly against latest industry standards

---

*This document itself should be reviewed and updated as the skill library matures.*
