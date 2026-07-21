# Sandeep Kumar Penchala Skills Library

> **Author:** Sandeep Kumar Penchala  
> **Goal:** The best AI agent skills on the planet — for building the world's best products.

A comprehensive, agent-agnostic skills library covering the **full company lifecycle** — from CEO vision through architecture, development, security, compliance, and operations. Every skill includes decision trees, scale depth guidance, cross-skill coordination, deep references, templates, and production checklists.

**50+ skills across 13 domains. 100+ reference documents. 20+ asset templates.**

## Philosophy

Every skill must be **the best of its kind in the world**:

- **Depth over breadth** — Masters 5 topics, doesn't skim 20. Goes to the root.
- **Actionable over academic** — Every line tells you what to DO, not what to ponder.
- **Concrete over abstract** — Decision trees, comparison tables, specific metrics, code patterns.
- **Opinionated where data-backed** — Best practices earned through experience, not theory.
- **Domain-agnostic** — Universal frameworks for ANY industry: healthcare, fintech, gaming, e-commerce, government, open source. Industry specifics live in `references/`.
- **Scale-aware** — Every skill covers Solo → Small → Medium → Enterprise. What's overkill at one scale is essential at another.
- **Coordination-aware** — Every skill knows which other skills to coordinate with, when to escalate, and what to communicate.
- **Agent-agnostic** — Works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI, or any SKILL.md-compatible agent.

See [`SKILL-QUALITY-STANDARDS.md`](SKILL-QUALITY-STANDARDS.md) for our quality bar and review process.

## Skill Architecture

Each skill follows a four-layer structure:

```
skill-name/
├── SKILL.md              # Instructions: workflow, best practices, checklist
├── scripts/              # Deterministic tools (Python/bash — run, don't read)
├── references/           # Deep knowledge loaded on demand
│   ├── decision-guide.md
│   └── patterns-catalog.md
└── assets/               # Templates, samples, configurations
    ├── template.md
    └── sample.json
```

This keeps `SKILL.md` lean (~150-250 lines) while making deep expertise available when needed.

## Skill Domains

| # | Domain | Skills | Focus |
|---|--------|--------|-------|
| 01 | **Strategy & Leadership** | CEO Strategist, CTO Advisor, Business Strategist | Vision, fundraising, org design, competitive strategy, board management |
| 02 | **Product Management** | Idea-to-Spec, Product Manager, UX Researcher | Discovery, prioritization, user research, PRDs, roadmaps |
| 03 | **Design** | UI/UX Designer, Accessibility Auditor, Brand Guidelines | Design systems, WCAG 2.2 AA/AAA, visual identity, motion design |
| 04 | **Architecture** | System Architect, API Designer, Database Designer | C4 model, ADRs, REST/GraphQL/gRPC, schema design, normalization |
| 05 | **Development** | Backend, Frontend, Mobile, Fullstack Developer | Multi-language, platform HIG, offline-first, performance |
| 06 | **Quality** | Code Reviewer, QA Engineer, Security Reviewer | 6-dimension review, test strategy, OWASP, SAST |
| 07 | **DevOps & Infra** | DevOps, CI/CD Builder, Observability, Docker/K8s, Cloud Architect | IaC, GitOps, SLOs, container security, Well-Architected |
| 08 | **Security** | Security Engineer, Compliance Officer, Incident Responder | Threat modeling, SOC 2/ISO 27001, IR phases, forensics |
| 09 | **Data & AI** | Data Engineer, Analytics Engineer, ML/AI Engineer | ETL/ELT, dbt, LLM patterns, RAG, MLOps, responsible AI |
| 10 | **Growth** | SEO Specialist, Content Strategist, Growth Engineer | Technical SEO, E-E-A-T, A/B testing, growth loops |
| 11 | **Legal & Compliance** | Legal Advisor, GDPR/Privacy, Regulatory Specialist | SaaS contracts, DPAs, fundraising legal, global regulations |
| 12 | **Operations** | Project Manager, Scrum Master, Technical Writer | RAID, agile ceremonies, Diátaxis, docs-as-code |
| 13 | **Specialized** | Monorepo Manager, Migration Architect, Performance Engineer, Chaos Engineer, Documentation Engineer | Monorepo tooling, strangler fig, profiling, chaos experiments |

## Usage

### Quick Start — Invoking a Skill

```bash
# Claude Code / OpenClaw
/{skill-name}

# GitHub Copilot CLI
/copilot-skill {skill-name}

# Cursor
@skill-{skill-name}
```

**Example workflow — idea to production:**

```
ceo-strategist → idea-to-spec → product-manager → ux-researcher
→ ui-ux-designer → system-architect → api-designer → database-designer
→ backend-developer → frontend-developer → mobile-developer
→ code-reviewer → qa-engineer → security-reviewer → security-engineer
→ ci-cd-builder → docker-kubernetes → cloud-architect → observability-engineer
→ performance-engineer → chaos-engineer → compliance-officer → legal-advisor
```

### Booting a New Project from Scratch

See [`PROJECT-BOOTSTRAP.md`](PROJECT-BOOTSTRAP.md) for the full 10-phase navigation guide — which skills to invoke at each phase, what order, and why.

Minimal path for an MVP:
```
ceo-strategist → product-manager → ui-ux-designer → system-architect
→ backend-developer → frontend-developer → code-reviewer → ci-cd-builder
```

## Deployment

### Choosing Your Agent

These skills are **agent-agnostic** — they work with any AI coding agent that supports SKILL.md or custom instructions. Choose the agent you already use:

| Agent | Skill Format | How Skills Load | Best For |
|-------|-------------|-----------------|----------|
| **Claude Code** | `.claude/skills/` | Auto-loaded from directory | Terminal-native, full project context |
| **GitHub Copilot CLI** | `.copilot/skills/` | `/copilot-skill {name}` | GitHub-integrated, PR-focused |
| **Cursor** | `.cursor/skills/` | `@skill-{name}` in chat | IDE-native, visual context |
| **OpenClaw** | `.openclaw/workspace/skills/` | `/{name}` in workspace | Custom agent orchestration |
| **Gemini CLI** | Custom instructions injection | Paste SKILL.md content | Google ecosystem projects |

### Installation

#### Claude Code (Recommended)
```bash
git clone https://github.com/zeroes-ones/Skills.git ~/skills-library
mkdir -p ~/.claude/skills/
cp -r ~/skills-library/skills/* ~/.claude/skills/
```
Verify: run `/{ceo-strategist}` in Claude Code — it should load the CEO strategist skill.

#### GitHub Copilot CLI
```bash
git clone https://github.com/zeroes-ones/Skills.git ~/skills-library
mkdir -p ~/.copilot/skills/
cp -r ~/skills-library/skills/* ~/.copilot/skills/
```
Verify: run `/copilot-skill ceo-strategist` — should load the skill context.

#### Cursor
```bash
git clone https://github.com/zeroes-ones/Skills.git ~/skills-library
mkdir -p ~/.cursor/skills/
cp -r ~/skills-library/skills/* ~/.cursor/skills/
```
Verify: type `@skill-ceo-strategist` in Cursor chat — should load the skill.

#### OpenClaw
```bash
git clone https://github.com/zeroes-ones/Skills.git ~/skills-library
mkdir -p ~/.openclaw/workspace/skills/
cp -r ~/skills-library/skills/* ~/.openclaw/workspace/skills/
```
Verify: run `/{ceo-strategist}` in your OpenClaw workspace.

#### Staying Up to Date
```bash
cd ~/skills-library
git pull origin main
cp -r skills/* ~/.claude/skills/  # or your agent's directory
```

### Selective Installation

You don't need all 45 skills. Install only the domains you need:

```bash
# Example: only strategy and development domains
cp -r ~/skills-library/skills/01-strategy ~/.claude/skills/
cp -r ~/skills-library/skills/05-development ~/.claude/skills/

# Example: only security and compliance
cp -r ~/skills-library/skills/08-security ~/.claude/skills/
cp -r ~/skills-library/skills/11-legal ~/.claude/skills/
```

### Troubleshooting

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| Agent doesn't recognize skill | Wrong install directory | Check your agent's docs for the correct skills directory path |
| Skill loads but no domain knowledge | References not copied | Ensure `references/` directories were copied alongside `SKILL.md` |
| Skill is too verbose for quick tasks | Agent reads entire SKILL.md | Skills are designed to be skimmed — agent reads scale-appropriate section (~200 lines). If still too slow, use the `## Decision Trees` section as entry point. |
| Skill missing for my domain | Coverage gap | Open an issue with your use case. Meanwhile, skills are domain-agnostic — the closest domain skill likely applies. |

## Core Framework Documents

| Document | Purpose |
|----------|---------|
| [`AGNOSTIC-PRINCIPLES.md`](AGNOSTIC-PRINCIPLES.md) | Universal skill design — domain-agnostic, industry-agnostic, project-agnostic |
| [`SCALE-DEPTH-FRAMEWORK.md`](SCALE-DEPTH-FRAMEWORK.md) | Solo → Small → Medium → Enterprise depth pattern for every skill |
| [`COORDINATION-MATRIX.md`](COORDINATION-MATRIX.md) | Cross-skill coordination — who talks to whom, when, and why |
| [`WISDOM-FRAMEWORK.md`](WISDOM-FRAMEWORK.md) | MVP-first, cost-effective, token-efficient decision making |
| [`TECH-STACK-DECISIONS.md`](TECH-STACK-DECISIONS.md) | Technology selection by project archetype with cost projections |
| [`PROJECT-BOOTSTRAP.md`](PROJECT-BOOTSTRAP.md) | Complete lifecycle navigation — which skills to invoke at each of 10 phases |
| [`SUB-SKILL-MAP.md`](SUB-SKILL-MAP.md) | 150+ sub-skills across all domains with industry variations |
| [`SKILL-QUALITY-STANDARDS.md`](SKILL-QUALITY-STANDARDS.md) | 10/10 grading rubric with progressive disclosure, error decoders, war stories, and 8 quality tests |
| [`scripts/upgrade_to_10.py`](scripts/upgrade_to_10.py) | Batch upgrade tool — applies progressive disclosure, token budgets, error decoders, and checklist numbering to all 56 skills |

## Contributing

1. Read [`SKILL-QUALITY-STANDARDS.md`](SKILL-QUALITY-STANDARDS.md) — the 10/10 quality bar
2. Read [`AGNOSTIC-PRINCIPLES.md`](AGNOSTIC-PRINCIPLES.md) — universal by default, specific by reference
3. Read [`SCALE-DEPTH-FRAMEWORK.md`](SCALE-DEPTH-FRAMEWORK.md) — every skill covers Solo→Small→Medium→Enterprise
4. Follow the four-layer architecture: SKILL.md + scripts/ + references/ + assets/
5. Every `SKILL.md` must pass the 10/10 checklist:
   - Full YAML frontmatter with `type`, `version`, `updated`, `token_budget`, `output`, `chain`
   - `<!-- QUICK: 30s -->` markers on every section for progressive disclosure
   - `## Error Decoder` — at least 7 common errors mapped to root cause and fix
   - `## Production Checklist` items numbered with `[S1]`, `[S2]`, etc. referencing standards
   - Time estimates on every workflow phase (`(~15 min)`)
   - "What good looks like" description after decision trees
   - Token budget declared in frontmatter
6. YAML frontmatter: `name`, `description`, `author: Sandeep Kumar Penchala`, `type`, `version`, `updated`, `token_budget`
7. No fluff — if a sentence doesn't help someone DO something, cut it
8. Test with at least one AI agent before submitting
9. After manual edits, run `python3 scripts/upgrade_to_10.py` to re-sync progressive disclosure markers and validation

## License

MIT — Sandeep kumar Penchala
