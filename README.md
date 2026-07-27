# Skills Library

> **Author:** Sandeep Kumar Penchala
> **Goal:** A practical, comprehensive skills library that helps you build products end-to-end — from idea to production, solo to enterprise.

A collection of agent-agnostic skills covering the **full company lifecycle** — from CEO vision through architecture, development, security, compliance, and operations. Each skill includes decision trees, scale depth guidance, cross-skill coordination, reference documents, templates, and production checklists.

**210+ skills across 28 domains. 1,675 chain edges with 0 asymmetries. 2,085+ reference documents. 5 personas, 3 hook types, 8 cross-tool commands, 3-tier evals, npm distribution.**

### Cross-Skill Chain System

Every skill declares its place in the dependency graph via YAML `chain:` blocks:

```yaml
chain:
  consumes_from: [api-designer, database-designer]   # What must complete BEFORE this skill
  feeds_into: [frontend-developer, code-reviewer, qa-engineer]  # What needs this skill's output NEXT

```

If `backend-developer` feeds into `code-reviewer`, then `code-reviewer` consumes from `backend-developer`. All 1,130 edges are **bidirectionally symmetric** — verified programmatically with 0 asymmetries. See [`COORDINATION-MATRIX.md`](COORDINATION-MATRIX.md) for the full phase-by-phase dependency map.

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

The `chain:` block in YAML frontmatter declares each skill's upstream/downstream dependencies. Skills coordinate via specific decision gates and shared artifacts — not vague "talk to X" references. All 1,675 chain edges are symmetric across the 188-skill graph.

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
| 26 | **Web3** | Smart Contract Auditor, Cryptographic Engineer, ZKP Engineer | EVM security audit, MPC/FHE/TEE, zero-knowledge circuits, constraint verification |
| 27 | **Framework** | Skill Levels, Writing Great Skills | Skill authoring, competency taxonomy, quality dimensions, anti-rationalization |

## Quality Status

**All 188 skills rated 10/10** with full section coverage across 12 required core sections:

| Section | Coverage | Description |
|---------|----------|-------------|
| Route the Request | 188/188 | Entry-point router directing to correct skill/mode |
| Ground Rules — Read Before Anything Else | 188/188 | Non-negotiable rules with mechanical triggers and violation responses |
| The Expert's Mindset | 188/188 | Mental models, what masters know, cognitive bias awareness |
| Operating at Different Levels | 188/188 | Solo → Small → Medium → Enterprise scale depth |
| When to Use | 188/188 | Decision table: use this skill vs alternatives |
| Decision Trees | 188/188 | Branching logic for key design/architecture choices |
| Core Workflow | 188/188 | Phased workflow with time estimates and completion criteria |
| Cross-Skill Coordination | 188/188 | Upstream/downstream tables, communication triggers, escalation paths |
| Proactive Triggers | 188/188 | Trigger → Action → Why for events requiring immediate attention |
| What Good Looks Like | 188/188 | Concrete aspirational outcome statement |
| Deliberate Practice | 188/188 | Exercises to build instinct before production use |
| References | 188/188 | Deep reference documents and external sources |

**Beyond the 12 core sections**, every skill also includes:
- **Error Recovery** — Symptom → Root Cause → Fix → Lesson decoder (5+ war stories)
- **State Log** — Decision ledger with anti-drift checks for cross-session continuity
- **Verification Guardrails** — Self-check checklist the agent runs before delivering work
- **Anti-Hungination** — "NOT VERIFIED" + "Flag your knowledge cutoff" guardrails

**Chain symmetry:** 1,675 edges with **0 asymmetries** — verified programmatically.

## Personas — The "Who" Layer

Skills define *how* to do work. Personas define *who* does the work. This 3-layer architecture adds role-based enforcement on top of skills:

```
Layer 3: Commands (/review, /build, /test) → The "when"
Layer 2: Personas (code-reviewer, security-auditor) → The "who"
Layer 1: Skills (210+ SKILL.md files) → The "how"

```

| Persona | Role | Allowed Tools | Default Skills |
|---------|------|--------------|----------------|
| **code-reviewer** | Read-only reviewer. No code changes | Read, Grep, Glob | code-reviewer, code-simplification |
| **security-auditor** | Security-focused auditor | Read, Grep, Glob, Bash (read-only) | security-reviewer, appsec-engineer |
| **test-engineer** | Test-first engineer. Write tests before code | Read, Write, Edit, Bash | tdd-guide, qa-engineer |
| **web-perf-auditor** | Performance optimization | Read, Grep, Bash (profile) | performance-engineer, web-perf-auditor |

**Rules:** Personas cannot invoke other personas. Run multiple personas in parallel fan-out, then merge results. See `personas/README.md`.

## Hooks — Automatic Skill Injection

Three hook types trigger skills automatically based on agent events:

| Hook | Trigger | Action |
|------|---------|--------|
| **session-start** | Agent session begins | Injects `using-agent-skills` meta-router for skill discovery |
| **simplify-ignore** | Code simplification runs | Protects marked code blocks from accidental deletion |
| **sdd-cache** | WebFetch call | Caches responses with HTTP revalidation headers |

Hooks are registered in `hooks/hooks.json` and activated per-agent. See `hooks/` directory.

## Command Wrappers — One Command, Every Tool

Eight slash commands work identically across Claude Code, Gemini CLI, and Copilot CLI:

| Command | Routes To | Best For |
|---------|-----------|----------|
| `/spec` | idea-to-spec | Feature specification from rough ideas |
| `/plan` | project-manager + scrum-master | Sprint planning and backlog grooming |
| `/build` | fullstack-developer + backend-developer + frontend-developer | Implementation |
| `/test` | tdd-guide + qa-engineer | Test-first development |
| `/review` | code-reviewer persona | Read-only code review |
| `/code-simplify` | code-simplification | Simplify without breaking |
| `/webperf` | performance-engineer + web-perf-auditor persona | Performance audit |
| `/ship` | shipping-and-launch + release-manager | Production release |

**Parity verified:** `scripts/validate-commands.js` checks all 3 tool directories have identical command coverage.

## 3-Tier Evaluation System

| Tier | What It Tests | Tool | Status |
|------|--------------|------|--------|
| **Tier 1** | Structural validation — frontmatter, sections, chain symmetry | `scripts/run-evals.sh` | 34/43 pass |
| **Tier 2** | TF-IDF routing precision — do prompts route to correct skills? | `scripts/run-routing-evals.js` | 68.8% rank-1 |
| **Tier 3** | Behavioral evals — headless agent output against expectations | `scripts/run-behavioral-evals.js` | 13 seed scenarios |

Run: `./scripts/run-evals.sh --tier all`

## Distribution — npm & Shell

```bash
# Shell install (one command)
curl -sSL https://raw.githubusercontent.com/zeroes-ones/Skills/main/scripts/install.sh | bash

# npm install
npx @zeroes-ones/skills init

```

## Brownfield Adoption

Existing project? See [`COMPARISON.md`](COMPARISON.md) and the `brownfield-adoption-planner` skill — 4-phase gated rollout starting with read-only safety skills, zero risk to production code.

## New & Notable Skills

| Skill | Domain | Purpose |
|-------|--------|---------|
| `using-agent-skills` | Framework | Meta-router — ASCII decision tree mapping tasks → skills |
| `agent-persona-orchestrator` | Framework | Persona lifecycle: fan-out, merge, conflict resolution |
| `incremental-implementation` | Development | Vertical slices, feature flags, atomic commits |
| `brownfield-adoption-planner` | Specialized | Phased skill adoption into legacy codebases |

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

**Brownfield (existing project)?** Use `brownfield-adoption-planner` — 4-phase gated rollout: read-only safety skills → context + characterization tests → development for new features → devops/observability. Zero risk to production code on day one.

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
| `skills-init` | Activate all 188 skills in current project (team/company default) |
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

# Startup or team project — full 188 skills
skills-init               # All 27 domains, 188 skills, full lifecycle coverage

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
| [`COMPARISON.md`](COMPARISON.md) | Competitive comparison — vs addyosmani/agent-skills, Pocock's Superpowers |
| [`SCALE-DEPTH-FRAMEWORK.md`](SCALE-DEPTH-FRAMEWORK.md) | Solo → Small → Medium → Enterprise depth pattern for every skill |
| [`COORDINATION-MATRIX.md`](COORDINATION-MATRIX.md) | Cross-skill coordination — who talks to whom, when, and why |
| [`WISDOM-FRAMEWORK.md`](WISDOM-FRAMEWORK.md) | MVP-first, cost-effective, token-efficient decision making |
| [`TECH-STACK-DECISIONS.md`](TECH-STACK-DECISIONS.md) | Technology selection by project archetype with cost projections |
| [`PROJECT-BOOTSTRAP.md`](PROJECT-BOOTSTRAP.md) | Complete lifecycle navigation — greenfield and brownfield paths |
| [`SUB-SKILL-MAP.md`](SUB-SKILL-MAP.md) | 2,000+ sub-skills across all domains with industry variations |
| [`SKILL-QUALITY-STANDARDS.md`](SKILL-QUALITY-STANDARDS.md) | 10/10 grading rubric with progressive disclosure, error recovery, state logs, and 12 governance gates |
| [`personas/README.md`](personas/README.md) | Persona architecture — 3-layer design, parallel fan-out, merge patterns |
| [`hooks/SIMPLIFY-IGNORE.md`](hooks/SIMPLIFY-IGNORE.md) | Code block protection — marking sections as immutable during simplification |
| [`hooks/SDD-CACHE.md`](hooks/SDD-CACHE.md) | WebFetch cache with HTTP revalidation |
| [`scripts/lint.sh`](scripts/lint.sh) | Master lint runner — 5 categories (files, markdown, yaml, shell, template) with --fix, --json, --ci |
| [`scripts/validate-skills.sh`](scripts/validate-skills.sh) | Pre-commit/pre-push governance — 12 automated validation gates |
| [`scripts/run-evals.sh`](scripts/run-evals.sh) | 3-tier evaluation harness — structural, routing, behavioral |
| [`scripts/validate-commands.js`](scripts/validate-commands.js) | Cross-tool command parity validator |
| [`.githooks/pre-commit`](.githooks/pre-commit) | Git pre-commit hook — 13-gate lint & validate before every commit |

## Linting & Validation

The repository has a comprehensive, zero-dependency linting system that enforces quality across all files.

### Quick Reference

```bash
# Run all linters on changed files
./scripts/lint.sh

# Run all linters on the entire repo
./scripts/lint.sh --all

# Auto-fix formatting issues (trailing whitespace, line endings, final newlines)
./scripts/lint.sh --fix

# Check only YAML frontmatter
./scripts/lint.sh --category yaml

# Check only markdown style
./scripts/lint.sh --category markdown

# CI-friendly JSON output
./scripts/lint.sh --all --json --ci

# Template compliance check (14 sections, anti-hallucination, gotchas, decision trees)
./scripts/lint.sh --category template

```

### Lint Categories

| Category | Script | Rules | Checks |
|----------|--------|-------|--------|
| **files** | `scripts/lib/lint-files.py` | 7 (FMT001-007) | UTF-8, LF endings, trailing whitespace, final newline, tabs, mixed indent, empty files |
| **markdown** | `scripts/lib/lint-markdown.py` | 14 (MD001-051) | Heading structure, blank lines, code fence language, bare URLs, duplicate headings |
| **yaml** | `scripts/lib/lint-yaml.py` | 10 (YML001-010) | Frontmatter validity, description ≤1024, required fields, name=dir, chain refs, trigger format |
| **shell** | `scripts/lib/lint-shell.py` | 10 (SHL001-010) | Shebang, `set -euo pipefail`, `[[ ]]` vs `[ ]`, backticks→`$()`, `read -r`, trap cleanup |
| **template** | `scripts/lib/lint-template.py` | 20+ checks | 14 required sections, anti-hallucination guardrails, dollar-quantified gotchas, ground rules, completion criteria, decision trees, chain connectivity |

### Pre-Commit Hook

The `.githooks/pre-commit` hook runs a 13-gate system on every commit:

| Gate | Check | Blocks Commit? |
|------|-------|---------------|
| G0 | Script integrity (SHA256 manifest) | Yes |
| G1 | File format (UTF-8, LF, no trailing whitespace, final newline, no tabs) | Yes |
| G2 | Shell script (shebang, strict mode, quoting, trap) | Yes |
| G3 | JSON validity | Yes |
| G4 | YAML frontmatter (valid, description ≤1024, trigger format, name=dir, chain refs) | Yes |
| G5 | Markdown style (headings, blank lines, code fences, duplicate headings) | Yes |
| G6 | Template compliance (14 sections, anti-hallucination, gotchas, ground rules) | Yes |
| G7 | Completion criteria (≥8 "Complete when") | No (warning) |
| G8 | Decision trees (≥3 under ## Decision Trees) | No (warning) |
| G9 | Chain connectivity (consumes_from + feeds_into) | Yes |
| G10 | Reference link integrity | No (warning) |
| G11 | Per-skill artifacts (verify-skill.sh + references/) | No (warning) |
| G12 | Portability target | No (warning) |

### Installing the Pre-Commit Hook

```bash
git config core.hooksPath .githooks

```

## Contributing

1. Read [`SKILL-QUALITY-STANDARDS.md`](SKILL-QUALITY-STANDARDS.md) — the 10/10 quality bar
2. Read [`AGNOSTIC-PRINCIPLES.md`](AGNOSTIC-PRINCIPLES.md) — universal by default, specific by reference
3. Read [`SCALE-DEPTH-FRAMEWORK.md`](SCALE-DEPTH-FRAMEWORK.md) — every skill covers Solo→Small→Medium→Enterprise
4. Follow the four-layer architecture: SKILL.md + scripts/ + references/ + assets/
5. Install the pre-commit hook: `git config core.hooksPath .githooks`
6. Run the lint suite before committing: `./scripts/lint.sh --all`
7. Auto-fix formatting issues: `./scripts/lint.sh --fix`
8. Verify all 12 governance gates pass: `bash scripts/validate-skills.sh`
9. No fluff — if a sentence doesn't help someone DO something, cut it
10. Test with at least one AI agent before submitting

## License

MIT — Sandeep kumar Penchala
