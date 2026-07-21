# Universal Skill System — Design for the World's Best Skills

> **Status:** Design Specification v1.0  
> **Date:** 2026-07-21  
> **Scope:** All 27 skills — document creation, engineering, product, design, security, devops, content, utilities  
> **Goal:** One template to rule them all. Every skill feels like it belongs to the same system. A user can pick up any skill cold and know exactly where to find what they need.

---

## Table of Contents

1. [Philosophy & Design Principles](#1-philosophy--design-principles)
2. [Universal Metadata Schema](#2-universal-metadata-schema)
3. [Universal Skill Anatomy](#3-universal-skill-anatomy)
4. [Progressive Disclosure System](#4-progressive-disclosure-system)
5. [Cross-Reference Graph](#5-cross-reference-graph)
6. [Skill Archetypes & Adaptations](#6-skill-archetypes--adaptations)
7. [Voice & Style Guide](#7-voice--style-guide)
8. [Quality Standard — The Goldilocks Test](#8-quality-standard--the-goldilocks-test)
9. [Migration Plan: All 27 Skills](#9-migration-plan-all-27-skills)
10. [Skill Graph Visualized](#10-skill-graph-visualized)
11. [Automation & Maintenance](#11-automation--maintenance)

---

## 1. Philosophy & Design Principles

### The Core Insight

A skill is not a document. A skill is a **conversation starter between two agents**: the one who wrote it and the one executing it. Every section exists to answer a question the executor will ask:

- *"Should I use this right now?"* → Identity + When to Use
- *"Give me the fastest path to a result."* → Quickstart
- *"What's the right way to do this?"* → Standards
- *"Walk me through it step by step."* → Playbook
- *"What breaks silently?"* → Footguns
- *"Did I do it right?"* → Checklist
- *"What do I do next?"* → See Also

### Seven Design Principles

| # | Principle | Means |
|---|-----------|-------|
| 1 | **One skeleton, many bodies** | Every skill follows the same 8-section anatomy. Content adapts; structure does not. |
| 2 | **Progressive by default** | Every section has three depth levels. The user gets value at 30 seconds, 3 minutes, or 30 minutes. |
| 3 | **Every section ends with action** | No paragraphs that only describe. Every section says "Do this now" or "Now you know X — here's what to do with it." |
| 4 | **Footguns are sacred** | What breaks silently is more valuable than what works. Document the failure modes. |
| 5 | **Skills know their neighbors** | Every skill has cross-references. The skill graph is explicit, not implicit. |
| 6 | **Output contracts** | Every skill states what it produces, in what format, and how the next skill in the chain consumes it. |
| 7 | **Self-validating** | Every skill ends with a checklist that, if passed, guarantees a production-ready result. |

### What Makes a Skill "World's Best"

A skill is production-grade when it passes these tests:

1. **The 30-second test:** Someone who has never used this skill can open it, read the quickstart, and produce something useful in under a minute.
2. **The footgun test:** Someone who has used this skill 10 times still discovers a gotcha they didn't know about, saving them a future debugging session.
3. **The handoff test:** The output of this skill is in the exact format the next skill in the chain expects.
4. **The checklist test:** Running the checklist catches all common errors before they reach production.
5. **The neighbor test:** Reading this skill tells you exactly which skill to use next and what it needs from you.
6. **The progressive disclosure test:** Every section is parseable at 30 seconds (marker), 3 minutes (standard), and 10+ minutes (deep with war stories).
7. **The error decoder test:** Common errors are mapped to root cause and exact fix — no search engine needed.
8. **The what-good-looks-like test:** Every quickstart describes the concrete success output (file size, expected response, visual outcome).
9. **The token budget test:** Frontmatter declares token_budget so the agent knows what it's loading.

---

## 2. Universal Metadata Schema

Every skill starts with identical frontmatter. No variation, no missing fields.

```yaml
---
name: "skill-name"
description: "One sentence. Who uses this, when, for what, what it produces."
type: "archetype"           # creation | engineering | product | design | quality | ops | content | utility | specialty
status: "stable"             # draft | stable | deprecated | sunsetting
version: "1.0.0"
updated: "2026-07-21"
license: "MIT"
domain: "domain-category"    # e.g., document-creation, backend-engineering, mobile-development
author: "username"
tags:
  - "keyword1"
  - "keyword2"
dependencies:
  tools: ["tool1", "tool2"]
  packages: ["package1", "package2"]
  permissions: ["perm1", "perm2"]
output:
  type: "file-format"        # e.g., .docx, .pptx, .xlsx, code, spec, config
  path_hint: "generated/{category}/"
chain:
  consumes_from: ["skill-a", "skill-b"]   # What skills feed into this one
  feeds_into: ["skill-c", "skill-d"]      # What skills consume this skill's output
  alternatives: ["skill-e"]               # Similar skills for different contexts
---
```

### Required Fields — No Exceptions

| Field | Why Required |
|-------|-------------|
| `name` | Identity. Must match filename. |
| `description` | The trigger — this is what the agent reads to decide if this skill applies. Must be one sentence, under 200 chars, answer "who, when, what output." |
| `type` | Enables category-based routing and template selection. |
| `status` | Prevents use of deprecated skills. |
| `version` | Enables change tracking and migration. |
| `updated` | Enables staleness detection. |
| `tags` | Enables search and discovery. |

### Optional but Strongly Recommended

| Field | Why |
|-------|-----|
| `domain` | Groups related skills for UI rendering. |
| `dependencies` | Prevents "command not found" midway through execution. |
| `output` | Enables chain-of-skills automation (skills pipeline). |
| `chain` | The skill graph — essential for the pipeline architecture. |
| `token_budget` | Informs the agent how many tokens this skill consumes (~word_count × 0.75). Enables token-aware loading. |

---

## 3. Universal Skill Anatomy

Every skill follows exactly this 8-section skeleton. Sections always appear in this order. Each section has a required minimal form and an optional expanded form.

### The Skeleton

```
[Frontmatter]
[H1 Title]

[Section 1] IDENTITY
  - 1a. Quick summary (1-2 sentences: what, who, why)
  - 1b. When to use (bullet conditions)
  - 1c. When NOT to use (critical — prevents misuse)

[Section 2] QUICKSTART
  - One paragraph of what this skill produces
  - One terminal command or code snippet that produces real output
  - One example result (what "done" looks like)

[Section 3] STANDARDS
  - The conventions, rules, and patterns this skill enforces
  - Each standard is a rule, not advice (imperative)
  - If there are competing valid approaches, name both and specify when to pick which

[Section 4] PLAYBOOK
  - Step-by-step workflow
  - Each step: What to do → How to verify it worked → What to do if it didn't
  - Include the exact commands, code, or configuration

[Section 5] FOOTGUNS
  - What breaks silently and how to avoid it
  - Each entry: Symptom → Cause → Prevention → Detection

[Section 6] OUTPUT
  - What this skill produces (files, formats, structures)
  - Where output goes (path conventions)
  - How the next skill in the chain consumes this output

[Section 7] CHECKLIST
  - Numbered verification items
  - Each item is binary: pass or fail
  - Running the full checklist guarantees production readiness

[Section 8] SEE ALSO
  - Adjacent skills (chain references)
  - Reference links (documentation standards, spec URLs)
  - Related tools or packages
```

### Section-by-Section Detail

#### Section 1: IDENTITY

Answers: "Should I use this right now?"

Must contain:
- One-sentence summary of the skill's purpose
- Bullet list of trigger conditions ("Use this when...")
- Bullet list of anti-triggers ("Do NOT use this when...")
- If applicable, a one-liner on what the skill produces

**Creation archetype example:**
```
Use this when you need to create or edit a .docx file with formatting, tables,
images, or tracked changes. Do NOT use this for .doc files — convert them first.
Do NOT use this for PDFs, spreadsheets, or Google Docs.
```

**Engineering archetype example:**
```
Use this when you're building a FastAPI backend from scratch or adding
production features (auth, database, async workers). Do NOT use this for
Django monoliths, pure Go backends, or serverless functions.
```

#### Section 2: QUICKSTART

Answers: "Give me the fastest path to a result."

Must contain:
- One paragraph: "This skill produces [output] by doing [approach]."
- One code block: a complete, runnable command or script
- One sentence: "When this completes, you'll have [output]."

**Creation example:**
```
This skill creates a .docx file with formatted content by running a Node.js
script that uses the docx library.

```bash
node create-document.js
```

When this completes, you'll have output.docx in the current directory.
```

**Engineering example:**
```
This skill scaffolds a FastAPI service with auth, database, and background
workers by generating files from templates.

```bash
uvicorn app.main:app --reload
```

When this completes, you'll have a running API at http://localhost:8000/docs.
```

#### Section 3: STANDARDS

Answers: "What's the right way to do this?"

Rules for this section:
- Every standard is an imperative rule, not a suggestion
- Group related standards under subheadings
- Include at least one code example per standard

Bad: "You may want to consider using type hints."
Good: "Every function must have complete type hints. Use mypy --strict to verify."

#### Section 4: PLAYBOOK

Answers: "Walk me through it step by step."

Rules:
- Numbered steps in execution order
- Each step has exactly three parts: **What to do** | **How to verify** | **What to do if it fails**
- Steps are concrete: they contain actual commands, code, or file paths

Step template:
```
### Step N: [Action Name]

1. **[Do]:** <exact command or code block>
2. **[Verify]:** <what success looks like — a log line, file output, test pass>
3. **[Recover]:** <what to do if verification fails — common fix or rollback>
```

#### Section 5: FOOTGUNS

Answers: "What breaks silently and how do I avoid it?"

The most valuable section. Each footgun follows this schema:

| Symptom | Cause | Prevention | Detection |
|---------|-------|------------|-----------|
| What you see when it breaks | Why it happens under the hood | How to avoid it in the first place | How to catch it if it happens |

Include at least 3 footguns minimum for any skill. The office skills (docx, pptx, xlsx) should have 10-20.

#### Section 6: OUTPUT

Answers: "What does this produce and what format is it in?"

Must include:
- List of output files with types
- Directory structure (if applicable)
- How downstream skills consume each output file
- Chain compatibility section: "This output is consumed by [skill names]."

#### Section 7: CHECKLIST

Answers: "Did I do it right?"

Rules:
- Each item is binary: pass or fail
- Each item references a specific section of Standards or Playbook
- Running all checks should take under 2 minutes (automate if longer)
- Format: `- [ ] <action or condition> — <reference to standard>`

#### Section 8: SEE ALSO

Answers: "What do I use next? What else should I know?"

Must include:
- Chain references: which skills consume this skill's output
- Chain references: which skills this skill consumes from
- Alternatives: similar skills for different contexts
- External references: documentation, spec URLs, standards bodies

---

## 4. Progressive Disclosure System

Every section in every skill has three depth levels, clearly marked.

### Marking Convention

```markdown
<!-- QUICK: 30 seconds → one sentence or one command -->
The core principle: <one line>

<!-- STANDARD: 3 minutes → the meat -->
<3-5 paragraphs of core content with code examples>

<!-- DEEP: 10+ minutes → edge cases, war stories, diagnostics -->
<Extended discussion of failure modes, corner cases, and advanced patterns>

<!-- END DEEP -->
```

### What Each Level Must Contain

| Level | Time | Depth | Required Content |
|-------|------|-------|-----------------|
| QUICK | 30s | One-liner | A single principle, command, or insight the user walks away with |
| STANDARD | 3 min | Working knowledge | Enough to complete the task correctly, with code/commands |
| DEEP | 10+ min | Mastery | Footguns, edge cases, performance implications, alternatives comparison |

### Rules

- QUICK sections must be parseable on their own — if someone reads only the quick lines across all sections, they have a valid mental model.
- DEEP sections are always below a fold — the STANDARD content is complete without them.
- Not every section needs all three levels. A checklist section may only need QUICK + STANDARD. A footguns section should always have DEEP.
- The comment markers are optional in the rendered output but must be present in the source for maintainability.

---

## 5. Cross-Reference Graph

### Complete Skill Dependency Map

```
idea-to-spec
  └─ feeds → product-manager (validates requirements)
  └─ feeds → database-design (creates schema from spec)
  └─ feeds → api-documentation (creates API spec)
       └─ feeds → python-backend / backend-engineer (implements API)
       └─ feeds → web-frontend (consumes API)
       └─ feeds → react-native (consumes API)
            └─ validates via → qa-testing
            └─ hardens via → security-appsec
            └─ monitors via → analytics-observability
            └─ deploys via → devops-ci-cd
            └─ documents via → api-documentation
            └─ optimizes via → content-seo (web only)

ui-ux-design
  └─ feeds → web-frontend (component specs)
  └─ feeds → react-native (component specs)
  └─ feeds → frontend-design (visual direction)
       └─ validated by → mobile-accessibility (mobile)
       └─ validated by → qa-testing (a11y audit)

health-compliance
  └─ overlays → python-backend (PHI safeguards)
  └─ overlays → react-native (local encryption)
  └─ pairs with → community-moderation (PHI in UGC)
  └─ pairs with → mobile-accessibility (health-specific a11y)

schedule
  └─ creates → morning (scheduled brief)

consolidate-memory
  └─ maintains → all user memory

setup-cowork
  └─ prerequisites → all other skills

STANDALONE (output consumed by humans, not skills):
  docx / pptx / xlsx / pdf / morning

pdf-reading
  └─ prerequisites → pdf (if manipulation needed after reading)
```

### Cross-Reference Format (Section 8 of Every Skill)

```
## SEE ALSO

### Chain — use after this skill
- [skill-name](skill-name.md) — what it consumes from this skill

### Chain — use before this skill
- [skill-name](skill-name.md) — what this skill expects as input

### Alternatives (different approach, same domain)
- [skill-name](skill-name.md) — when to choose this instead

### References
- [Title](URL) — brief description of what this reference covers
```

---

## 6. Skill Archetypes & Adaptations

Not all skills are the same kind of thing. The universal skeleton adapts differently for each archetype.

### Archetype Matrix

| Archetype | Examples | Section Emphasis | Voice | Code Density |
|-----------|----------|-----------------|-------|-------------|
| **Creation** | docx, pptx, xlsx, pdf | Playbook +++, Footguns +++, Quickstart +++ | Imperative commands | Very high |
| **Engineering** | python-backend, web-frontend, react-native, database-design | Standards +++, Checklist +++, Output ++ | Architecture-first | High |
| **Product/Strategy** | product-manager, idea-to-spec | Identity +++, Output +++, See Also ++ | Process-oriented | Low |
| **Design** | ui-ux-design, frontend-design | Standards +++, Playbook ++, Checklist ++ | Guided principles | Medium |
| **Quality** | qa-testing, security-appsec | Checklist +++, Playbook +++, Footguns ++ | Rule enforcement | Medium |
| **Ops** | devops-ci-cd, analytics-observability | Playbook +++, Checklist +++, Standards ++ | Infrastructure | Medium |
| **Content** | content-seo | Standards +++, Checklist ++, Footguns ++ | Strategy + Technical | Medium |
| **Utility** | schedule, consolidate-memory, setup-cowork | Quickstart +++, Playbook ++ | Task automation | Low |
| **Specialty** | health-compliance, community-moderation, mobile-accessibility | Identity +++, Standards +++, Footguns ++, See Also +++ | Compliance + Risk | Medium |

### Archetype-Specific Section Guidance

#### Creation Archetype (docx, pptx, xlsx, pdf)

These skills need the most footgun documentation because they interact with complex file formats.

```
Section emphasis:
  QUICKSTART:   "Run this one command to get output" — essential
  PLAYBOOK:     "Step 1: setup → Step 2: generate → Step 3: verify" — detailed
  FOOTGUNS:     "These 12 things corrupt your file" — the most valuable section
  CHECKLIST:    "Verify with these tools before delivering"
  STANDARDS:    Lighter — the tool API docs already exist
```

#### Engineering Archetype (python-backend, web-frontend, react-native, database-design)

These skills need strong standards and checklists because they produce production code.

```
Section emphasis:
  STANDARDS:    "This is the architecture. Follow it." — authoritative
  CHECKLIST:    "20 items that catch every common production issue"
  PLAYBOOK:     "Implement this feature following this exact flow"
  FOOTGUNS:     "These patterns look correct but fail in production"
  QUICKSTART:   "Scaffold a new service in 30 seconds"
```

#### Product/Strategy Archetype (product-manager, idea-to-spec)

These skills produce documents, not code. Their output is consumed by other skills.

```
Section emphasis:
  IDENTITY:     "What kind of document this produces and who reads it"
  OUTPUT:       "Exact file structure and format — critical for chain consumption"
  PLAYBOOK:     "Interview → synthesize → write → validate"
  STANDARDS:    "These sections are mandatory in every PRD"
```

#### Utility Archetype (schedule, consolidate-memory, setup-cowork)

These are short, task-specific skills. They should stay short — the skeleton is minimal.

```
Section emphasis:
  QUICKSTART:   "What you need to know to complete this task"
  PLAYBOOK:     "Step-by-step — the whole skill is a playbook"
  IDENTITY:     "When to use — very specific trigger conditions"
```

---

## 7. Voice & Style Guide

### Tone

| Attribute | Standard |
|-----------|----------|
| Voice | **Imperative, direct.** "Do X. Verify Y. Never do Z." |
| Person | Second person ("you") — the agent is being addressed. |
| Confidence | **Absolute.** No "consider," "you may want to," "it's often best to." Say "Do X" or "Never do Y." |
| Hedging | Reserved for true uncertainty. "If your scale exceeds 10M rows, consider partitioning. Otherwise, don't." |
| Error tone | **Neutral and factual.** "This corrupts the file" not "Be careful, this can be dangerous!" |

### Formatting Rules

- **Code blocks** for every command and code snippet
- **Bold** for key concepts, rule statements, and section headers within prose
- **Italic** sparingly — only for introducing a new term
- **Tables** for comparison, configuration, and checklists
- **Bullet lists** for unordered items (tools, footguns, conditions)
- **Numbered lists** for ordered steps in playbooks
- No emojis anywhere (except by user request)
- No decorative ASCII art except for architecture diagrams
- No `#` characters in hex color values in YAML frontmatter (use short form `FF0000`)
- No inline HTML unless required for formatting

### Section Opening Convention

Every section opens with a one-line QUICK marker followed by the section's core principle:

```markdown
## 1. IDENTITY

<!-- QUICK: 30 seconds → know when to use this skill -->
Use this skill when <condition>. Do NOT use it when <contracondition>.
```

### Code Block Conventions

```python
# Every code block has a comment explaining what it does
# NOT a comment explaining basic Python syntax
result = do_the_thing()  # ← good: explains intent
x = x + 1               # ← bad: explains syntax
```

- Language tags on all code blocks
- Type hints in all Python/TypeScript
- Async/await with proper error handling
- Never show `pip install` for preinstalled packages
- Always show the `import` line

---

## 8. Quality Standard — The Goldilocks Test

### For Every Skill, It Must Be:

**Not too hot** (too abstract):
- ✗ "When building a backend, consider using appropriate architectural patterns"
- ✓ "Stack: FastAPI + Pydantic v2 + SQLAlchemy 2.x + Alembic + PostgreSQL + Redis"
- ✗ "Users appreciate well-designed interfaces"
- ✓ "Touch targets minimum 44x44pt. Color contrast >= 4.5:1 for body text."

**Not too cold** (too specific to one edge case):
- ✗ "When using pptxgenjs 3.12.2 on Node 18.17 with the 'Futura' font on a Mac, you need to..."
- ✓ "pptxgenjs hex colors must never include # or 8 digits — FF0000 not #FF0000"
- ✗ "In our specific deployment we found that..."
- ✓ "If you use cursor-based pagination, include cursor, has_more, and limit in the response."

**Just right** (general + specific where it matters):
- ✓ "The principle is X. Here's exactly how to implement it. Here's what breaks if you do it wrong."

### The 80/20 Rule

Spend 80% of the skill's content on:
1. The 20% of patterns that do 80% of the work
2. The 20% of mistakes that cause 80% of the failures

The remaining 20% of content covers edge cases and niche scenarios.

### Token Budget Guidelines

| Skill Type | Target (tokens) | Notes |
|-----------|----------------|-------|
| Utility | 500-1500 | schedule, consolidate-memory, setup-cowork |
| Creation | 1500-3000 | docx, pptx, xlsx, pdf, pdf-reading |
| Engineering | 2000-4000 | python-backend, web-frontend, react-native, backend-engineer, database-design |
| Product/Design | 1500-3000 | product-manager, ui-ux-design, frontend-design, idea-to-spec |
| Quality/Security | 2000-3000 | qa-testing, security-appsec, api-documentation |
| Ops | 2000-3000 | devops-ci-cd, analytics-observability |
| Content | 1500-2500 | content-seo |
| Specialty | 2500-4000 | health-compliance, community-moderation, mobile-accessibility |
| Morning | 3000-5000 | Exception: it's a full artifact generator with design spec |

---

## 9. Migration Plan: All 27 Skills

### Phase 1: Template + Archetypes (Foundation)

| # | Skill | Archetype | Action | Key Changes |
|---|-------|-----------|--------|-------------|
| 1 | **Skill Template** | (meta-skill) | Create | The universal skeleton SKILL.md — the master reference document |

### Phase 2: Creation Archetype (4 skills)

| # | Skill | Archetype | Action | Key Changes |
|---|-------|-----------|--------|-------------|
| 2 | **docx** | creation | Rewrite | Add frontmatter (version, type, dependencies, chain, tags). Add Identity section (when to use / not use). Add Output section. Add See Also section. Convert gotchas table to footguns section. Add progressive disclosure markers. |
| 3 | **pptx** | creation | Rewrite | Same as docx. Keep design ideas section (it's unique value). Keep 15+ gotchas as footguns. Add checklist. |
| 4 | **xlsx** | creation | Rewrite | Same pattern. Keep financial model section — it's domain-specific excellence. Expand footguns. Add checklist. |
| 5 | **pdf** | creation | Rewrite | Merge with pdf-reading knowledge — they should be one skill or clearly chained. Add footguns. Add output section. Add see also to pdf-reading. |
| 6 | **pdf-reading** | utility | Refactor | Add frontmatter, identity, chain to pdf skill. Keep as utility if kept separate; otherwise merge into pdf. |

### Phase 3: Engineering Archetype (6 skills)

| # | Skill | Archetype | Action | Key Changes |
|---|-------|-----------|--------|-------------|
| 7 | **backend-engineer** | engineering | Rewrite | Add frontmatter (version, chain to python-backend, tags). Add quickstart. Add footguns section (N+1 queries, sync-in-async, missing indexes). Add output section. Add see also chain to database-design, devops-ci-cd, security-appsec. |
| 8 | **python-backend** | engineering | Rewrite | Add frontmatter. Add quickstart (scaffold a FastAPI app). Add footguns. Add output section (file structure). Chain to/from backend-engineer. |
| 9 | **web-frontend** | engineering | Rewrite | Add frontmatter. Add footguns (hydration errors, server/client mismatch, stale closures). Chain to/from ui-ux-design, content-seo, qa-testing. |
| 10 | **react-native** | engineering | Rewrite | Add frontmatter. Add footguns (bridge thread blocking, native module linking, reanimated v2 vs v3). Chain to/from mobile-accessibility, community-moderation. |
| 11 | **database-design** | engineering | Rewrite | Add frontmatter. Add quickstart (one CREATE TABLE + index). Add footguns (over-indexing, SELECT *, N+1 in migration loops). Chain to backend-engineer, python-backend. |
| 12 | **api-documentation** | engineering | Rewrite | Add frontmatter. Add quickstart (one endpoint spec). Add footguns (spec/drift, missing error responses, wrong pagination format). Chain to/from backend-engineer, web-frontend, react-native. |

### Phase 4: Product/Design Archetype (5 skills)

| # | Skill | Archetype | Action | Key Changes |
|---|-------|-----------|--------|-------------|
| 13 | **idea-to-spec** | product | Rewrite | Add frontmatter. Add output section (exact file tree). Add footguns (scope creep, missing edge cases, skipping Phase 1). Chain to product-manager, database-design, api-documentation. |
| 14 | **product-manager** | product | Rewrite | Add frontmatter. Add quickstart (one PRD template to fill). Add footguns (solution-first thinking, missing non-goals). Chain to/from idea-to-spec. |
| 15 | **ui-ux-design** | design | Rewrite | Add frontmatter. Add footguns (handoff gap, missing states). Chain to web-frontend, react-native, frontend-design. |
| 16 | **frontend-design** | design | Rewrite | Add frontmatter. Add quickstart. Chain to/from ui-ux-design, web-frontend. |
| 17 | **content-seo** | content | Rewrite | Add frontmatter. Add footguns (canonical chain breaks, hreflang errors). Chain to web-frontend. |

### Phase 5: Quality/Security Archetype (3 skills)

| # | Skill | Archetype | Action | Key Changes |
|---|-------|-----------|--------|-------------|
| 18 | **qa-testing** | quality | Rewrite | Add frontmatter. Move anti-patterns to footguns section. Add output section (test report format). Chain to every engineering skill. |
| 19 | **security-appsec** | quality | Rewrite | Add frontmatter. Add quickstart. Add footguns (common OWASP misses). Chain to all engineering + ops skills. |
| 20 | **analytics-observability** | ops | Rewrite | Add frontmatter. Add footguns (PII in logs, sampling bias). Chain to devops-ci-cd, all engineering skills. |

### Phase 6: Ops Archetype (1 skill)

| # | Skill | Archetype | Action | Key Changes |
|---|-------|-----------|--------|-------------|
| 21 | **devops-ci-cd** | ops | Rewrite | Add frontmatter. Add quickstart (one Dockerfile + pipeline). Add footguns (secret leaks, :latest tags, no health checks). Chain to all engineering. |

### Phase 7: Specialty Archetype (3 skills — already closest to target)

| # | Skill | Archetype | Action | Key Changes |
|---|-------|-----------|--------|-------------|
| 22 | **health-compliance** | specialty | Polish | Already the richest metadata. Add progressive disclosure markers. Add quickstart. Add footguns (BAA gotchas, PHI in push notifications). Ensure chain to community-moderation, mobile-accessibility. |
| 23 | **community-moderation** | specialty | Polish | Already strong. Add quickstart. Expand footguns (false positives in medical keyword flagging, burnout in human moderators). Chain to health-compliance, react-native. |
| 24 | **mobile-accessibility** | specialty | Polish | Already strong. Add quickstart. Expand footguns (label duplication, focus trapping). Chain to react-native, qa-testing. |

### Phase 8: Utility Archetype (5 skills)

| # | Skill | Archetype | Action | Key Changes |
|---|-------|-----------|--------|-------------|
| 25 | **schedule** | utility | Light refactor | Add frontmatter. Keep short — utility skills should stay lean. |
| 26 | **consolidate-memory** | utility | Light refactor | Add frontmatter. Keep short. |
| 27 | **setup-cowork** | utility | Light refactor | Add frontmatter. Keep procedural. |
| 28 | **morning** | utility | Maintain | Already deeply specified. Just add frontmatter. Note: exceptionally long due to full design spec — this is intentional. |

### Migration Priority

```
P0 (MVP — do first):   6 creation + engineering skills that are most-used
  → docx, pptx, xlsx, pdf, backend-engineer, python-backend

P1 (Core — do second): 8 remaining engineering + product + quality skills
  → web-frontend, react-native, database-design, api-documentation,
     idea-to-spec, product-manager, qa-testing, security-appsec

P2 (Polish):            5 design + ops + content skills
  → ui-ux-design, frontend-design, content-seo, devops-ci-cd, analytics-observability

P3 (Complete):          5 utilities + 3 specialties (polish only)
  → schedule, consolidate-memory, setup-cowork, morning, pdf-reading
  → health-compliance, community-moderation, mobile-accessibility
```

---

## 10. Skill Graph Visualized

```
                                    +-----------------+
                                    |  consolidate-   |
                                    |  memory          |
                                    +--------+--------+
                                             | (maintains)
                                             v
+----------------+               +-----------------------+
|  setup-cowork  |---prereq----->|   ALL OTHER SKILLS    |
+----------------+               +-----------+-----------+
                                             |
          +-----------------+                |
          |   idea-to-spec  |----------------+
          +--------+--------+
                   |
                   v
          +-----------------+       +----------------------+
          | product-manager |       |   database-design    |
          +--------+--------+       +----------+-----------+
                   |                           |
                   v                           v
          +------------------+     +-----------------------+
          |   ui-ux-design   |     |   api-documentation   |
          +--+-----+---------+     +-----------+-----------+
             |     |                           |
             v     v                           v
    +----------+  +-----------+     +----------------------+
    |frontend-  |  |mobile-    |     |  backend-engineer   |
    |design     |  |accessibility|    +----+-----+-----+---+
    +-----+-----+  +-----+-----+         |     |     |
          |              |               v     v     v
          v              v     +-------------------------------+
    +----------+  +----------+ | python-backend                |
    |web-      |  |react-    | | database-design               |
    |frontend  |  |native    | | security-appsec               |
    +----+-----+  +----+-----+ +---------------+---------------+
         |             |                         |
         v             v                         v
    +----------------------------------------------------+
    |              qa-testing                             |
    |              security-appsec                        |
    +----------------------------------------------------+
                         |
                         v
    +----------------------------------------------------+
    |  devops-ci-cd (deploys everything above)           |
    |  analytics-observability (monitors all)            |
    +----------------------------------------------------+


    STANDALONE SKILLS (output consumed by humans, not skills):
    +------+ +------+ +------+ +-----+ +--------+
    | docx | | pptx | | xlsx | | pdf | | morning |
    +------+ +------+ +------+ +-----+ +--------+

    OVERLAY SKILLS (modify behavior of other skills):
    +--------------------+ +-----------------------+
    | health-compliance   | | community-moderation  |
    +--------------------+ +-----------------------+

    UTILITY SKILLS (task automation, not domain-specific):
    +----------+ +--------------------+ +---------------+
    | schedule | | consolidate-memory | | setup-cowork  |
    +----------+ +--------------------+ +---------------+
```

---

## 11. Automation & Maintenance

### CI Enforcement (for the skills pipeline)

Every skill in the repo must pass these checks:

```
1. Frontmatter completeness check
   - All required fields present
   - type matches an allowed archetype
   - chain.feeds_into and chain.consumes_from reference existing skills
   - No dangling skill references

2. Section structure check
   - All 8 required sections present
   - Sections in correct order
   - No empty sections (except DEEP which is optional)

3. Cross-reference validation
   - Every skill mentioned in "See Also" exists
   - Every skill in chain fields exists
   - No circular chains (A -> B -> A)

4. Quickstart executability check
   - Every code block in QUICKSTART sections is syntactically valid
   - Every command references a real tool/package

5. Staleness check
   - updated field within 90 days, or status is "stable"
   - If status="deprecated", must have a migration path reference
```

### Versioning Policy

- **Major bump** (2.0.0): Section structure change, archetype change, significant rewrite
- **Minor bump** (1.1.0): New section added, new footguns, expanded coverage
- **Patch bump** (1.0.1): Bug fix, typo, clarified language, updated dependency versions

### Review Cadence

| Skill Status | Review Frequency | Trigger |
|-------------|-----------------|---------|
| stable | Quarterly | No trigger needed -- scheduled |
| draft | Per-commit | After each content change |
| deprecated | Never (remove after sunset) | No action until removal |

### Skill Health Metrics

Track per skill:

- **Freshness:** Days since `updated` field was last changed
- **Cross-ref health:** % of chain references that resolve to existing skills
- **Execution success:** % of quickstart commands that run without error (if testable)
- **Footgun density:** Number of footguns / total tokens (target > 0.01)
- **Checklist pass rate:** If automated, % of check items that pass on first run

---

## Appendix A: Complete Template Shell

```markdown
---
name: "skill-name"
description: "One sentence: who uses this, when, for what, what it produces."
type: "archetype"
status: "draft" | "stable" | "deprecated"
version: "1.0.0"
updated: "2026-07-21"
license: "MIT"
domain: "domain"
author: "username"
tags:
  - "tag1"
  - "tag2"
dependencies:
  tools: ["tool"]
  packages: ["package"]
  permissions: []
output:
  type: "file-format"
  path_hint: "path/"
chain:
  consumes_from: ["upstream-skill"]
  feeds_into: ["downstream-skill"]
  alternatives: ["alternative-skill"]
---

# Skill Title

> One-sentence summary of what this skill does. The "elevator pitch."

## 1. IDENTITY

<!-- QUICK: 30 seconds — know when to use this skill -->
**Use this skill when** you need to <condition>.

**Do NOT use this skill when** <contracondition>. Instead, use <alternative>.

## 2. QUICKSTART

<!-- QUICK: 30 seconds — produce something real -->
<One paragraph describing what this skill produces at minimum.>
<One command or code snippet that produces real output.>
<One example of what "done" looks like.>

## 3. STANDARDS

<!-- QUICK: 30 seconds — the non-negotiable rules -->
These rules apply every time you use this skill.

<!-- STANDARD: 3 minutes — the conventions -->
<Numbered or bulleted list of conventions with examples.>

<!-- DEEP: 10+ minutes — why these standards exist -->
<Trade-offs, alternatives considered, historical context.>

## 4. PLAYBOOK

<!-- QUICK: 30 seconds — the workflow in one line -->
1. Setup -> 2. Execute -> 3. Verify -> 4. Deliver

<!-- STANDARD: 3 minutes — detailed steps -->
### Step 1: <Name>
1. **Do:** <exact command or code>
2. **Verify:** <what success looks like>
3. **Recover:** <what to do if verification fails>

### Step 2: <Name>
1. **Do:** ...
2. **Verify:** ...
3. **Recover:** ...

## 5. FOOTGUNS

<!-- QUICK: 30 seconds — what most commonly breaks -->
The most common failure: <one-line description>.

<!-- STANDARD: 3 minutes — the gotcha table -->
| Symptom | Cause | Prevention | Detection |
|---------|-------|------------|-----------|
| <what you see> | <why it happens> | <how to avoid> | <how to catch> |

<!-- DEEP: 10+ minutes — war stories -->
<Extended failure narratives and edge cases.>

## 6. OUTPUT

<!-- QUICK: 30 seconds — what this produces -->
This skill produces: <file type>, <format>, <count>.

<!-- STANDARD: 3 minutes — output structure -->
<File tree or format specification.>
<How downstream skills consume this output.>

## 7. CHECKLIST

<!-- STANDARD: 3 minutes — verify everything -->
- [ ] <Item 1 — binary pass/fail>
- [ ] <Item 2 — binary pass/fail>
- [ ] <Item 3 — binary pass/fail>

All items must pass before declaring success.

## 8. SEE ALSO

### Chain — use after this skill
- [skill-name](link) — what it takes from this skill

### Chain — use before this skill
- [skill-name](link) — what this skill expects

### Alternatives
- [skill-name](link) — when to use this instead

### References
- [Title](URL) — description

---
```

## Appendix B: Quick Reference Card

### Skill Creation Cheat Sheet

| Step | What | Why |
|------|------|-----|
| 1 | Choose archetype | Determines section emphasis + voice |
| 2 | Fill frontmatter | Required: name, description, type, status, version, updated, tags |
| 3 | Write Identity | "Use when / Don't use when" — prevents misuse |
| 4 | Write Quickstart | Must produce real output in one command |
| 5 | Write Standards | Rules, not advice. Imperative voice. |
| 6 | Write Playbook | Step → Verify → Recover. Every step concrete. |
| 7 | Write Footguns | Minimum 3. Use symptom/cause/prevention/detection table. |
| 8 | Write Output | File types, paths, chain compatibility |
| 9 | Write Checklist | Binary pass/fail. References Standards + Playbook. |
| 10 | Write See Also | Chain references to real neighboring skills |
| 11 | Add progressive markers | QUICK / STANDARD / DEEP comments at each section |
| 12 | Validate | Run through Goldilocks test. Check cross-refs resolve. |

### Validation Checklist for a New Skill

- [ ] Frontmatter: all required fields present
- [ ] Frontmatter: chain references resolve to existing skills
- [ ] Quickstart: would this produce output in < 60 seconds?
- [ ] Standards: are they rules, not suggestions?
- [ ] Playbook: does every step have a verification + recovery?
- [ ] Footguns: minimum 3 in symptom/cause/prevention/detection format
- [ ] Output: does it say how downstream skills consume this?
- [ ] Checklist: binary items only, no ambiguous items
- [ ] See Also: does it reference real neighboring skills?
- [ ] Voice: no hedging ("consider," "you may want to")
- [ ] Goldilocks: not too abstract, not too specific
- [ ] Progressive: QUICK lines parseable on their own

---

*End of Design Specification v1.0*
