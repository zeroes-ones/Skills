# Skills Library

> **Author:** Sandeep Kumar Penchala  
> **Goal:** A practical, comprehensive skills library that helps you build products end-to-end — from idea to production, solo to enterprise.

A collection of agent-agnostic skills covering the **full company lifecycle** — from CEO vision through architecture, development, security, compliance, and operations. Each skill includes decision trees, scale depth guidance, cross-skill coordination, reference documents, templates, and production checklists.

**106 skills across 25 domains. 1,130 chain edges with 0 asymmetries. 150+ reference documents. 30+ asset templates.**

### Cross-Skill Chain System

Every skill declares its place in the dependency graph via YAML `chain:` blocks:

```yaml
chain:
  consumes_from: [api-designer, database-designer]   # What must complete BEFORE this skill
  feeds_into: [frontend-developer, code-reviewer, qa-engineer]  # What needs this skill's output NEXT
```

If `backend-developer` feeds into `code-reviewer`, then `code-reviewer` consumes from `backend-developer`. All 1,032 edges are **bidirectionally symmetric** — verified programmatically with 0 asymmetries. See [`COORDINATION-MATRIX.md`](COORDINATION-MATRIX.md) for the full phase-by-phase dependency map.

## Philosophy

We focus on what actually matters when building software:

- **Deep, not wide** — Each skill masters its domain. No surface-level coverage.
- **Do, don't ponder** — Every section tells you what to DO, with concrete steps.
- **Concrete frameworks** — Decision trees, comparison tables, specific metrics, code patterns. No hand-waving.
- **Opinionated from experience** — Practices backed by real-world results, not theory.
- **Industry-agnostic** — Frameworks apply to healthcare, fintech, gaming, e-commerce, government, open source, and more. Industry specifics live in `references/`.
- **Scales with you** — Every skill covers Solo → Small → Medium → Enterprise. What's overkill today might be essential tomorrow.
- **Knows its neighbors** — Every skill maps which other skills it coordinates with, when to escalate, and what to communicate.
- **Works anywhere** — Compatible with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI, and any agent that reads SKILL.md files.

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

The `chain:` block in YAML frontmatter declares each skill's upstream/downstream dependencies. Skills coordinate via specific decision gates and shared artifacts — not vague "talk to X" references. All chain edges are symmetric across the 101-skill graph.

This keeps `SKILL.md` focused (~250-550 lines, ~3000-4000 token budget) while making deep expertise available when needed.

## Skill Domains

| # | Domain | Skills | Focus |
|---|--------|--------|-------|
| 01 | **Strategy** | CEO Strategist, CTO Advisor, Business Strategist, Product Strategist | Vision, fundraising, org design, competitive strategy, board management |
| 02 | **Product** | Idea-to-Spec, Product Manager, UX Researcher | Discovery, prioritization, user research, PRDs, roadmaps |
| 03 | **Design** | UI/UX Designer, Accessibility Auditor, Brand Guidelines | Design systems, WCAG 2.2 AA/AAA, visual identity, motion design |
| 04 | **Architecture** | System Architect, API Designer, Database Designer, Networking Engineer | C4 model, ADRs, REST/GraphQL/gRPC, schema, VPC, DNS, CDN, zero trust |
| 05 | **Development** | Backend, Frontend, Mobile, Fullstack, Localization, Translation Manager | Multi-language, platform HIG, offline-first, RTL, i18n/l10n, MT pipelines |
| 06 | **Quality** | Code Reviewer, QA Engineer, Security Reviewer, Accessibility Testing | 6-dimension review, test strategy, OWASP, a11y CI/CD gates |
| 07 | **DevOps** | DevOps, CI/CD, Observability, Docker/K8s, Cloud Architect, Platform Engineer, SRE, Release Manager, FinOps | IaC, GitOps, SLOs, IDP, error budgets, release trains, cloud cost |
| 08 | **Security** | Security Engineer, Compliance Officer, Incident Responder | Threat modeling, SOC 2/ISO 27001, IR phases, forensics |
| 09 | **Data & AI** | Data Engineer, Analytics Engineer, ML/AI Engineer, Data Scientist, DBRE | ETL/ELT, dbt, LLM patterns, RAG, statistical analysis, database reliability |
| 10 | **Growth** | SEO Specialist, Content Strategist, Growth Engineer, DevRel Advocate | Technical SEO, E-E-A-T, A/B testing, developer community, API advocacy |
| 11 | **Legal** | Legal Advisor, GDPR/Privacy, Regulatory Specialist | SaaS contracts, DPAs, fundraising legal, global regulations |
| 12 | **Operations** | Project Manager, Scrum Master, Technical Writer, TPM, Customer Support | RAID, agile ceremonies, Diátaxis, cross-team programs, support workflows |
| 13 | **Specialized** | Monorepo Manager, Migration Architect, Performance Engineer, Chaos Engineer, Documentation Engineer | Monorepo tooling, strangler fig, profiling, chaos experiments, docs-as-code |
| 14 | **Finance** | Algorithmic Trader, Market Data Engineer, Quantitative Analyst | Trading strategies, market data pipelines, options analysis, quantitative modeling |
| 15 | **Sales** | Sales Engineer, RevOps Manager, BizDev Manager, Marketing Manager, Demand Generation, Partnerships Manager | Revenue operations, CRM, pipeline analytics, go-to-market, channel partnerships |
| 16 | **People** | HR Manager, People Ops, Recruiting | Employee lifecycle, compensation, benefits, performance, talent acquisition |
| 17 | **Customer Success** | Customer Success Manager, Account Manager | Health scoring, retention, expansion revenue, proactive account management |
| 18 | **Corporate Finance** | FP&A Analyst, Accountant, Treasury Manager | Financial modeling, budgeting, cash flow, tax, treasury operations |
| 19 | **Governance** | Board Manager, Investor Relations | Board prep, cap table, investor updates, governance compliance |
| 20 | **Hardware** | Embedded Engineer, Firmware Developer, Hardware Architect | Embedded systems, firmware, PCB design, IoT architecture |
| 21 | **Health Clinical** | Clinical Informatics, Community Ops, Crisis Response, Medical Content Reviewer, Patient Experience Researcher, Patient Health Educator | FHIR/HL7, EHR integration, clinical review, patient research, health education |
| 22 | **AI Engineering** | LLM Engineer, AI Safety Health Reviewer, MLOps Engineer, AI Safety Engineer, Business Intelligence Engineer | RAG, prompt engineering, model safety, ML pipelines, BI semantic layer |
| 23 | **Trust & Safety** | Trust & Safety Engineer, Content Policy Manager, Privacy Engineer | Abuse detection, medical misinformation, BAA/DSAR, consent infrastructure |
| 24 | **Creative** | UX Writer, Product Marketing Manager, Medical Illustrator | Product copy, health literacy, clinical value props, medical visualization |
| 25 | **Engineering Leadership** | Staff Engineer, Engineering Manager, Director Engineering, VP Engineering | IC leadership, people management, org design, executive strategy |

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

**Example workflow — idea to production (full lifecycle):**

```
ceo-strategist → idea-to-spec → product-manager → ux-researcher
→ ui-ux-designer → accessibility-auditor → ux-writer
→ system-architect → api-designer → database-designer → networking-engineer
→ backend-developer → frontend-developer → mobile-developer → fullstack-developer
→ code-reviewer → qa-engineer → security-reviewer → accessibility-testing
→ ci-cd-builder → docker-kubernetes → cloud-architect → observability-engineer
→ performance-engineer → chaos-engineer → security-engineer → compliance-officer
→ legal-advisor → gdpr-privacy → documentation-engineer → technical-writer
```

### Booting a New Project from Scratch

See [`PROJECT-BOOTSTRAP.md`](PROJECT-BOOTSTRAP.md) for the full 10-phase navigation guide — which skills to invoke at each phase, what order, and why.

Minimal path for an MVP:
```
ceo-strategist → product-manager → ui-ux-designer → system-architect
→ backend-developer → frontend-developer → code-reviewer → ci-cd-builder
```

## Deployment — One Command, All Projects

Skills are deployed once globally via symlinks — every project (existing and new) gets them automatically.

### Quick Start

```bash
# One-time global install
curl -sSL https://raw.githubusercontent.com/zeroes-ones/Skills/main/scripts/install.sh | bash
```

This clones the library to `~/.zeroes-ones/skills/`, creates global symlinks for all your agents, installs convenience commands, and sets up auto-activation for new projects.

| Command | What It Does |
|---------|-------------|
| `skills-init` | Activate all 106 skills in current project (team/company default) |
| `skills-init --solo` | Activate 8 essential skills (personal/weekend projects) |
| `skills-init --grow` | Activate 18 skills (project gaining users/traction) |
| `skills-init --status` | Show current tier and skill count |
| `skills-update` | Pull latest skills — all symlinked projects update instantly |

### Tiered Activation — Match Skills to Project Maturity

Skills scale with your project. Start lean, expand as you grow:

```bash
# Personal side project — just the essentials
cd ~/code/my-app
skills-init --solo       # 8 skills: CEO, product, fullstack, code review, QA, CI/CD, security, GDPR

# Project is gaining users — need architecture, UX, backend depth
skills-init --grow        # 18 skills: adds system design, API design, UX, backend, security engineering

# Startup or team project — full 106 skills
skills-init               # All 25 domains, 106 skills, full lifecycle coverage
```

**Auto-activation:** When you `cd` into any git repo, the shell prompts you to activate skills. It auto-detects the right tier based on your project location and structure.

### Using Skills in Any Project

Then in your agent:
```
/ceo-strategist      # Start with strategy
/product-manager     # Define the product
/system-architect    # Design the architecture
/backend-developer   # Build it
```

### Supported Agents

| Agent | Skill Directory | How to Invoke |
|-------|----------------|---------------|
| **Claude Code** | `.claude/skills/` | `/{skill-name}` |
| **GitHub Copilot CLI** | `.copilot/skills/` | `/copilot-skill {name}` |
| **Cursor** | `.cursor/skills/` | `@skill-{name}` |
| **OpenClaw** | `.openclaw/workspace/skills/` | `/{name}` |
| **Gemini CLI** | `.gemini/skills/` | Paste content or custom injection |

### Keeping Skills Updated

```bash
skills-update   # Pulls latest from GitHub — all symlinked projects see changes instantly
```

### Troubleshooting

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| `skills-init: command not found` | PATH missing | Add `export PATH="$HOME/.local/bin:$PATH"` to `~/.zshrc` |
| Agent doesn't see skills | Symlinks broken | Run `skills-init` again inside the project |
| Skills load but no references | References in wrong path | Symlinks handle this — ensure `~/.zeroes-ones/skills/` is intact |
| Skill too verbose for quick tasks | Agent reads full SKILL.md | Agent reads scale-appropriate section (~200 lines). Use `## Decision Trees` as entry point. |
| "Cannot update protected ref" | GPG key not on GitHub | Add GPG key at https://github.com/settings/gpg/new |

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
| [`scripts/upgrade_to_10.py`](scripts/upgrade_to_10.py) | First-pass upgrade — applies progressive disclosure, token budgets, error decoders, and checklist numbering |
| [`scripts/upgrade_to_10_v2.py`](scripts/upgrade_to_10_v2.py) | Second-pass upgrade — domain-specific error decoders, what-good-looks-like, cross-skill integration, token budget tuning |

## Contributing

1. Read [`SKILL-QUALITY-STANDARDS.md`](SKILL-QUALITY-STANDARDS.md) — the 10/10 quality bar
2. Read [`AGNOSTIC-PRINCIPLES.md`](AGNOSTIC-PRINCIPLES.md) — universal by default, specific by reference
3. Read [`SCALE-DEPTH-FRAMEWORK.md`](SCALE-DEPTH-FRAMEWORK.md) — every skill covers Solo→Small→Medium→Enterprise
4. Follow the four-layer architecture: SKILL.md + scripts/ + references/ + assets/
5. Every `SKILL.md` must pass the 10/10 checklist:
   - Full YAML frontmatter with `name`, `description`, `author`, `type`, `version`, `updated`, `token_budget`, `output`, `chain`
   - `<!-- QUICK: 30s -->` markers for progressive disclosure
   - `## Route the Request` — ASCII decision tree routing to the right skill
   - `## Ground Rules — Read Before Anything Else` — 5 domain-specific guardrails
   - `## Decision Trees` — at least 2 concrete decision frameworks
   - `## Core Workflow` — 4 phases with time estimates
   - `## Cross-Skill Coordination` — table of upstream/downstream skills with communication triggers
   - `## Best Practices` — 8 actionable practices with code/config examples
   - `## Error Decoder` — 5 war stories with symptom, root cause, fix, and lesson
   - `## Production Checklist` — 14 items with domain-specific IDs (e.g., API1-API14, EM1-EM14)
   - `## Scale Depth` — Solo → Startup → Scale-up → Enterprise
   - `## What Good Looks Like` — aspirational outcome statement
   - Token budget declared in frontmatter (~3000-4000 target)
6. YAML frontmatter: `name`, `description`, `author: Sandeep Kumar Penchala`, `type`, `version`, `updated`, `token_budget`
7. No fluff — if a sentence doesn't help someone DO something, cut it
8. Test with at least one AI agent before submitting
9. After manual edits, run `python3 scripts/upgrade_to_10.py && python3 scripts/upgrade_to_10_v2.py` to re-sync all quality markers

## License

MIT — Sandeep kumar Penchala
