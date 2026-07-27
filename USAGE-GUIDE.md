# Usage Guide — How to Get the Most Out of Every Skill

> **Audience:** Anyone using this library — from solo developers to enterprise teams.
> **Covers:** Skill anatomy, progressive disclosure, chaining, error decoders, decision trees, common patterns, and tips.

---

## Table of Contents

1. [How Skills Work](#how-skills-work)
2. [Anatomy of a Skill](#anatomy-of-a-skill)
3. [Progressive Disclosure: Read What You Need](#progressive-disclosure-read-what-you-need)
4. [Skill Chaining: Building Pipelines](#skill-chaining-building-pipelines)
5. [Error Decoders: Learning from War Stories](#error-decoders-learning-from-war-stories)
6. [Decision Trees: Making Choices](#decision-trees-making-choices)
7. [Operating at Different Levels](#operating-at-different-levels)
8. [Production Checklists: Don't Ship Without This](#production-checklists-dont-ship-without-this)
9. [Common Patterns](#common-patterns)
10. [What to Expect at Each Quality Tier](#what-to-expect-at-each-quality-tier)
11. [Tips for Taking Maximum Advantage](#tips-for-taking-maximum-advantage)

---

## How Skills Work

Each skill is a **SKILL.md file** — a self-contained instruction set that an AI agent reads and follows. When you type `/skill-name: your request`, the agent:

1. Loads the skill's frontmatter (YAML metadata)
2. Reads the Route the Request section to confirm this is the right skill
3. Follows the Decision Tree to pick the correct workflow branch
4. Executes the Core Workflow phases
5. Checks the Production Checklist before delivering output
6. Handles errors using the Error Decoder

Skills are **agent-agnostic** — they work with Claude Code, Copilot CLI, Cursor, OpenClaw, and Gemini CLI. No configuration needed.

---

## Anatomy of a Skill

Every SKILL.md has these sections, in order:

```
┌─────────────────────────────────────────────────────────┐
│ YAML FRONTMATTER                                        │
│ name, description, chain (dependencies), token_budget   │
├─────────────────────────────────────────────────────────┤
│ # Route the Request                                     │
│ "Is this really a {domain} problem? If not, redirect."  │
├─────────────────────────────────────────────────────────┤
│ # Ground Rules                                          │
│ Non-negotiable constraints. Violate = abort.            │
├─────────────────────────────────────────────────────────┤
│ # The Expert's Mindset                                  │
│ Mental models, cognitive biases, what masters know      │
├─────────────────────────────────────────────────────────┤
│ ## When to Use                                          │
│ Decision table: this skill vs alternatives              │
├─────────────────────────────────────────────────────────┤
│ ## Decision Trees                                       │
│ Branching logic: "If X, go to Phase A. If Y, Phase B."  │
├─────────────────────────────────────────────────────────┤
│ ## Core Workflow                                        │
│ 3-6 phases with time estimates and completion criteria  │
├─────────────────────────────────────────────────────────┤
│ ## Best Practices                                       │
│ 8+ specific, actionable practices with concrete metrics │
├─────────────────────────────────────────────────────────┤
│ ## Error Decoder                                        │
│ War stories: Symptom → Root Cause → Fix → Lesson        │
├─────────────────────────────────────────────────────────┤
│ ## Production Checklist                                 │
│ 12+ items, each referencing a numbered standard         │
├─────────────────────────────────────────────────────────┤
│ ## Operating at Different Levels                        │
│ L1 Apprentice → L5 Transformative: what changes at each │
├─────────────────────────────────────────────────────────┤
│ ## Cross-Skill Coordination                             │
│ Upstream/downstream tables, handoff gates, escalation   │
├─────────────────────────────────────────────────────────┤
│ ## What Good Looks Like                                 │
│ Concrete description of successful output               │
├─────────────────────────────────────────────────────────┤
│ ## References                                           │
│ Deep reference docs, sub-skills, external sources       │
└─────────────────────────────────────────────────────────┘
```

### Frontmatter: What the Chain Block Means

```yaml
chain:
  consumes_from: [api-designer, database-designer]  # Must run BEFORE this skill
  feeds_into: [frontend-developer, code-reviewer]    # Needs this skill's output NEXT
```

All edges are **bidirectionally symmetric**. If `backend-developer` feeds into `code-reviewer`, then `code-reviewer` consumes from `backend-developer`. Run `python3 scripts/audit-library.py` to verify 0 asymmetries across all 1,675 edges.

---

## Progressive Disclosure: Read What You Need

Every section has three depth levels. You choose how deep to go:

```markdown
## Section Title
<!-- QUICK: 30s -->
One paragraph. The gist. Read this first.

<!-- STANDARD: 3min -->
Working knowledge. Code examples, commands, metrics, comparison tables.
Read this to actually do the work.

<!-- DEEP: 10+min -->
War stories, edge cases, failure narratives, advanced patterns.
Read this when you're debugging at 2am or mastering the domain.
```

**Pattern:** Start with QUICK. If you need to execute, read STANDARD. If something breaks or you're optimizing, read DEEP.

**Coverage:** 214/214 skills have QUICK and STANDARD markers. 209/214 have DEEP markers (5 health/clinical procedural skills are exempt).

---

## Skill Chaining: Building Pipelines

Skills don't work in isolation. They form pipelines:

```
idea-to-spec → system-architect → backend-developer → code-reviewer → qa-engineer
                                                    → security-reviewer
                                                    → performance-engineer
```

### How to Chain

**Option 1: Sequential invocation**
```
/idea-to-spec: I want to build a task manager for remote teams
/system-architect: Design architecture for the task manager spec
/backend-developer: Build the API based on the architecture
/code-reviewer: Review the backend code
```

**Option 2: Fan-out (parallel)**
```
/backend-developer: Build the task manager API
/frontend-developer: Build the task manager UI (use the same API spec)
/code-reviewer: Review both backend and frontend
```

**Option 3: Automated pipeline**
```bash
# skills-init creates symlinks. Agents auto-resolve chains.
# When code-reviewer is invoked, it knows to look for backend-developer output.
```

### Reading the Chain Graph

Use [`COORDINATION-MATRIX.md`](COORDINATION-MATRIX.md) to see the full dependency graph. It maps which skills feed into which at each project phase.

---

## Error Decoders: Learning from War Stories

This is the most valuable section in any skill. It's not hypothetical — it's real failures that happened to real engineers.

```markdown
| Symptom | Root Cause | Fix | Lesson |
|---------|------------|-----|--------|
| "Connection refused on port 5432" | PostgreSQL wasn't started. Docker compose only brought up the app container. | `docker compose up -d db` before starting the app. | Always verify infrastructure before debugging application code. |
```

**How to use Error Decoders:**
1. **Before starting:** Skim the Error Decoder to know what can go wrong
2. **When stuck:** Search the table for your error message
3. **After fixing:** Read the Lesson column — it's the preventive wisdom
4. **Contributing:** Every Lesson must be a real war story, not generic advice

**Domain-specific formats:** Non-code domains (HR, recruiting, trust & safety, design auditing) use adapted formats like negative constraints tables instead of Symptom→Fix. See [`SKILL-QUALITY-STANDARDS.md`](SKILL-QUALITY-STANDARDS.md#error-decoder-formats-by-domain) for the full calibration.

---

## Decision Trees: Making Choices

Every skill has at least one ASCII decision tree. They encode the skill's core judgment:

```
New project — which architecture?
├── Solo developer, < 10K users expected → Monolith
│   └── Simple domain (CRUD heavy) → Rails/Django monolith
│   └── Real-time needs (chat, collab) → Go/Elixir monolith
├── Small team (2-5), 10K-100K users → Modular Monolith
│   └── Extract services when: team > 8 OR deploy frequency mismatch
└── Team > 8, 100K+ users → Microservices
    └── Start with 3-5 services. Add more when: independent scaling needed
```

**How to use Decision Trees:**
1. Start at the top
2. Answer each branch honestly (don't optimize for the future you might have)
3. The leaf node tells you exactly what to do — not "it depends"

---

## Operating at Different Levels

Every skill maps competency from L1 (Apprentice) to L5 (Transformative):

| Level | Who | What Changes |
|-------|-----|-------------|
| **L1 Apprentice** | New to the domain | Follows recipes exactly. Needs explicit steps. |
| **L2 Practitioner** | 6 months experience | Adapts recipes to context. Starts recognizing patterns. |
| **L3 Professional** | 2+ years | Designs new patterns. Teaches others. Anticipates failure modes. |
| **L4 Expert** | 5+ years | Creates frameworks. Mentors L1-L3. Architectural decisions. |
| **L5 Transformative** | 10+ years | Redefines the domain. Industry influence. Novel solutions. |

**How to use:** Read the level that matches your experience. If you're L2, skip L4-L5 content — it'll distract you. If you're L4, L1-L2 content will feel obvious — that's correct.

---

## Production Checklists: Don't Ship Without This

Every code/deployment skill has a Production Checklist with 12+ items. Each item references a numbered standard:

```markdown
- [ ] **[API1]** OpenAPI 3.1 specification complete with all paths and schemas
- [ ] **[API7]** Rate limiting configured per endpoint tier
- [ ] **[API12]** All secrets in vault, not in code or env files
```

**How to use:**
1. Before shipping, run through the checklist
2. Every unchecked item is a potential production incident
3. The reference IDs (API1, API7, etc.) let you trace standards across skills
4. 210/214 skills have production checklists (4 framework meta-skills are exempt)

---

## Common Patterns

### Pattern 1: The Solo SaaS (8 skills)

```
idea-to-spec → system-architect → backend-developer → frontend-developer
                                 → code-reviewer → qa-engineer → docker-kubernetes
```

See: [`examples/logsnap-solo-to-scale/`](examples/logsnap-solo-to-scale/)

### Pattern 2: The Full-Stack Team (15-20 skills)

```
product-manager → ux-researcher → ui-ux-designer → system-architect
                → backend-developer → frontend-developer
                → code-reviewer → qa-engineer → security-reviewer
                → ci-cd-builder → observability-engineer → cloud-architect
```

### Pattern 3: The Security Audit (5 skills)

```
security-reviewer → appsec-engineer → cloud-security → compliance-officer → incident-responder
```

### Pattern 4: The Data Pipeline (6 skills)

```
data-engineer → analytics-engineer → data-scientist → ml-engineer → mlops-engineer
```

### Pattern 5: The Pre-Launch Legal Review (3 skills)

```
legal-advisor → gdpr-privacy → regulatory-specialist
```

---

## What to Expect at Each Quality Tier

Skills in this library are all 10/10 quality. Here's what that means in practice:

| Quality Marker | What You Get |
|---------------|-------------|
| **Route the Request** | Never invokes the wrong skill. Redirects to the correct one automatically. |
| **Ground Rules** | Non-negotiable constraints with mechanical triggers. If violated, the agent aborts. |
| **Decision Trees** | 3+ branches per skill. No paralysis — every leaf is an action. |
| **Core Workflow** | 3-6 phases with time estimates. You always know what's next and how long. |
| **Error Decoder** | 3+ real war stories per skill. Exact error message → exact fix. |
| **Production Checklist** | 12+ items with traceable standard IDs. Run it before every ship. |
| **Progressive Disclosure** | QUICK/STANDARD/DEEP on every section. Read only what you need. |
| **Cross-Skill Coordination** | Exact handoff artifacts and decision gates. No vague "talk to X". |
| **Token Budget** | Declared upfront. Agent knows how much context to allocate. |
| **Chain Symmetry** | 1,675 edges, 0 asymmetries. Verified programmatically. |

---

## Tips for Taking Maximum Advantage

### 1. Start with QUICK, Go DEEP Only When Stuck

The QUICK markers give you the gist in 30 seconds per section. Read all QUICK sections first. Only descend into STANDARD when you're implementing, and DEEP when you're debugging or mastering.

### 2. Chain Skills, Don't Isolate Them

The real power is in pipelines. One skill's output is the next skill's input. Use the `chain:` block in each skill's frontmatter to understand dependencies.

### 3. Run the Production Checklist Before Every Ship

This alone prevents 80% of production incidents. The checklists encode years of hard-won experience.

### 4. Read the Error Decoder Before You Start

Knowing what can go wrong before you begin saves hours of debugging. The Lesson column is the condensed wisdom.

### 5. Use Tiered Activation

Don't activate all 214 skills at once. Use `--solo` (8 skills) for prototypes, `--grow` (18) for side projects, `--full` (214) for enterprise. See [`examples/logsnap-solo-to-scale/`](examples/logsnap-solo-to-scale/).

### 6. Verify Chain Symmetry

Run `python3 scripts/audit-library.py` to verify that all 1,675 chain edges are symmetric. If `A feeds_into B`, then `B consumes_from A` must hold.

### 7. Contribute War Stories

The Error Decoder sections are living documents. When you encounter a new failure, add it — with the exact symptom, root cause, fix, and lesson. Future users (including future you) will thank you.

### 8. Cross-Reference with Examples

Don't just read skills in isolation. Study the examples in [`examples/`](examples/) to see how skills chain together in real projects:

- **LogSnap** — Solo engineer going from idea to $25K MRR using tiered activation
- **Orchestra Platform** — Full team building an enterprise platform with all 56 skills
- **UOA Options Trading** — Domain-specific pipeline (finance + data + trading)

---

## Quick Reference

| Need | Command / Action |
|------|-----------------|
| Install globally | `curl -sSL https://.../install.sh \| bash` |
| Activate in project | `skills-init` |
| Activate solo tier (8 skills) | `skills-init --solo` |
| Update all skills | `skills-update` |
| Audit library quality | `python3 scripts/audit-library.py` |
| See chain graph | Open [`COORDINATION-MATRIX.md`](COORDINATION-MATRIX.md) |
| Invoke a skill | `/skill-name: your request` |
| Read quality standards | [`SKILL-QUALITY-STANDARDS.md`](SKILL-QUALITY-STANDARDS.md) |
| See examples | [`examples/`](examples/) |

---

*214 skills. 29 domains. 1,675 symmetric chain edges. 9.9/10 quality. Works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI.*
