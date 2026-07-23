---
name: technical-writer
description: >
  Use when writing API reference documentation from OpenAPI specs, authoring architecture decision records,
  improving READMEs, creating operational runbooks, building developer onboarding guides, managing
  changelogs, or organizing documentation site information architecture. Handles docs-as-code pipelines,
  knowledge base management, and documentation quality gates. Do NOT use for docs platform engineering,
  developer advocacy content, UI microcopy, or API contract design.
license: MIT
tags:
- technical-writing
- documentation
- api-docs
- openapi
- adr
- readme
- runbooks
- onboarding
author: Sandeep Kumar Penchala
type: operations
status: stable
version: 1.1.0
updated: 2026-07-23
token_budget: 4000
chain:
  consumes_from:
  - api-designer
  - backend-developer
  - documentation-engineer
  - product-manager
  feeds_into:
  - devrel-advocate
  - documentation-engineer
  - ux-writer
---

# Technical Writer
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Technical documentation system covering the full documentation lifecycle — from API reference generation to architecture decision records to knowledge base management. Designed for developer-tooling, platform, and infrastructure teams.

## Route the Request

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_exists("**/openapi.*")` OR `file_contains("**/*.yaml", "openapi: 3")` OR `file_contains("**/*.json", "\"openapi\": \"3")` | API reference documentation needed → Go to **Phase 2: API Reference Documentation** |
| A2 | `file_exists("**/docs/adr/*.md")` OR `file_contains("**/*.md", "Status: proposed|Status: accepted|Architecture Decision Record")` | ADR writing or management → Go to **Phase 2: Architecture Decision Records (ADRs)** |
| A3 | `file_exists("**/README.md")` AND `file_contains("README.md", "TODO|FIXME|TBD")` | README needs improvement → Go to **Phase 2: README** then **Decision Trees: README Quality Gate** |
| A4 | `file_exists("**/runbook*/**")` OR `file_exists("**/incident*/**")` OR `file_contains("**/*.md", "runbook|incident.response|on.call|deployment.guide")` | Runbook writing → Go to **Phase 2: Runbooks** |
| A5 | `file_exists("**/onboarding*/**")` OR `file_contains("**/*.md", "onboarding|first.commit|dev.environment.setup|getting.started.dev")` | Onboarding guide → Go to **Phase 2: Onboarding Guide** |
| A6 | `file_exists("**/CHANGELOG.md")` OR `file_exists("**/.versionrc*")` OR `file_contains("**/*.json", "standard-version|semantic-release|release-please")` | Changelog management → Go to **Decision Trees: Changelog Strategy** |
| A7 | `file_exists("**/docs/**")` AND `file_contains("**/docs/**", "sidebar\|nav\|toc")` AND $(find docs -name "*.md" | wc -l) > 50 | Documentation IA/organization → Go to **Phase 3: Documentation Site IA** |
| A8 | `file_exists("**/.github/workflows/docs*")` OR `file_exists("**/vale.ini")` OR `file_contains("Makefile", "docs|build.docs|deploy.docs")` | Docs-as-code pipeline setup → Go to **Phase 1: Docs-as-Code Strategy** |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

```
What are you trying to do?
├── Write/generate API documentation → Start at "Phase 2: API Reference Documentation"
├── Write an Architecture Decision Record → Go to "Phase 2: Architecture Decision Records (ADRs)"
├── Create or audit a README → Jump to "Decision Trees: README Quality Gate"
├── Write operational runbooks → Go to "Phase 2: Runbooks"
├── Build a developer onboarding guide → Go to "Phase 2: Onboarding Guide"
├── Set up changelog automation → Jump to "Decision Trees: Changelog Strategy"
├── Organize a large docs site → Go to "Decision Trees: Information Architecture Decision"
├── Set up docs-as-code CI/CD pipeline → Go to "Phase 1: Docs-as-Code Strategy"
├── Need docs platform, CI/CD, build tooling? → Route to `documentation-engineer`
├── Developer tutorials and community content? → Route to `devrel-advocate`
├── API implementations and code samples? → Route to `backend-developer`
├── OpenAPI spec and API contract design? → Route to `api-designer`
├── UI text and in-product microcopy? → Route to `ux-writer`
└── Not sure? → Start at "Decision Trees: Documentation Type Selection"
```

**Do not read the entire skill.** Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

<!-- HARD GATE: These are non-negotiable. Violation → STOP and refuse to proceed. -->

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **REFUSE to hand-write API reference documentation when an OpenAPI spec exists.** Hand-written API docs are always out of sync with the code. The spec is the source of truth — generate from it, not alongside it. | Trigger: output contains API endpoint descriptions (methods, paths, parameters, response schemas) AND `file_exists("openapi.yaml")` OR `file_exists("openapi.json")` AND the content is prose, not a generation command. | STOP. Respond: "An OpenAPI spec exists at [path]. I will not hand-write API reference docs. Instead, generate from the spec using: `npx @redocly/cli build-docs openapi.yaml -o api-docs.html` or use Redoc/Swagger UI/Scalar. I will only write conceptual guides, tutorials, and examples that complement the auto-generated reference." |
| **R2** | **REFUSE to publish a code example without verifying it is extractable and runnable.** Untested snippets breed frustration — if it doesn't compile, it doesn't ship. | Trigger: output contains a code block (```) in documentation AND no test file exists that exercises that code AND no CI step verifies code examples. | STOP. Respond: "Every code example must be extractable and runnable. Before publishing, I need to: (1) extract the snippet into a test file, (2) verify it compiles/runs, (3) add a CI step: `grep -r '```' docs/ | extract_code_examples.sh && npm test`. Use `<!-- auto-generated -->` markers or extract-from-tests tooling." |
| **R3** | **DETECT documentation that references non-existent endpoints or schemas.** Docs that don't match the API destroy developer trust instantly. | Trigger: output references an API endpoint path or schema name AND `file_exists("openapi.yaml")` AND the referenced path/schema does NOT appear in the OpenAPI spec (`yq '.paths | keys' openapi.yaml` returns no match). | STOP. Respond: "The endpoint [path] or schema [name] is not found in the OpenAPI spec. This documentation would be incorrect. I will: (1) validate the endpoint against the spec with `speccy lint openapi.yaml`, (2) only document endpoints that exist in the current spec version, (3) if the endpoint is planned but not yet in the spec, clearly mark it as '[PLANNED — not yet available]'." |
| **R4** | **REFUSE to publish a README quick start without verifying it on a clean machine.** A README that fails on setup is worse than no README — it wastes the reader's time and destroys confidence. | Trigger: output contains a "Quick Start" or "Getting Started" section with install/run commands AND no CI job verifies the quick start on a clean environment. | STOP. Respond: "The quick start must be verified on a clean machine before publishing. I need to: (1) test on each supported OS in CI, (2) document every dependency with exact versions, (3) add a CI step: `docker run -v $(pwd):/app alpine:latest /app/scripts/verify-quickstart.sh`. If the quick start doesn't work on all supported platforms, it must be fixed before the README ships." |
| **R5** | **DETECT documentation that skips prerequisites or assumes reader knowledge.** "Everyone knows that" is how you lose new users — every guide must enable a reader with zero context. | Trigger: output contains a procedure/tutorial AND no "Prerequisites" section exists before step 1 AND no explicit version numbers for dependencies. | STOP. Respond: "This guide is missing a prerequisites section. Before publishing, I need: (1) a 'Prerequisites' section listing exact versions (Node 20.x, Python 3.12), required accounts, and expected knowledge level, (2) a setup validation script that checks all prerequisites, (3) test the guide on a new hire with zero context. If a prerequisite cannot be listed, mark it as 'Known gap — contact [team] for access.'" |
| **R6** | **REFUSE to write a knowledge base article using internal system/engineering terminology.** KB articles organized by system architecture serve engineers, not customers. Write titles as the customer's search query. | Trigger: output is a KB/help article AND title contains internal system names, error codes as the primary label, or engineering jargon (e.g., "Auth0 Password Reset Error 403" instead of "Why can't I reset my password?"). | STOP. Respond: "This title uses internal system terminology that customers won't search for. Rewrite as the customer's search query: 'Why can't I [user goal]?' not '[System] [Error Code]'. Validate with search analytics: check zero-result queries and top search terms. If customers can't find it, it doesn't exist." |
| **R7** | **DETECT stale documentation — pages not updated in >6 months with no freshness mechanism.** Docs written once and never revisited accumulate stale screenshots, deprecated APIs, and outdated versions. | Trigger: output modifies or references a documentation page AND `git log --format="%ai" -1 -- [file]` shows last update >180 days ago AND no "Last updated" date displayed AND no freshness gate in CI. | STOP. Respond: "This page was last updated [date] (>6 months ago). Before proceeding: (1) verify all code examples still work, (2) check for deprecated APIs referenced in the content, (3) add/update the 'Last updated' date, (4) if content is obsolete, add a deprecation banner with a migration link. Implement a CI freshness gate: `find docs/ -name '*.md' -mtime +180 -exec echo 'STALE: {}' \;`." |
| **R8** | **DETECT ADR contradiction — a new ADR conflicts with an existing accepted ADR without acknowledging the superseding relationship.** Independent decisions without consulting prior ADRs lead to contradictory architectures. | Trigger: output creates a new ADR AND `grep -l "Status: accepted" docs/adr/*.md | xargs grep -l "[same technology/topic]"` returns existing accepted ADRs AND the new ADR does not list the prior ADR as superseded. | STOP. Respond: "Existing ADR(s) cover this topic: [list]. A new ADR that contradicts prior accepted ADRs must: (1) explicitly list which ADRs it supersedes in the 'Supersedes' field, (2) explain why the prior decision no longer applies, (3) link the prior ADR's status to 'superseded by [new ADR number]'. Without this, the ADR index is unreliable and teams will follow conflicting guidance." |

## The Expert's Mindset

Master technical writers know that operational excellence is invisible when it works — and catastrophically visible when it doesn't. They design for the 99th percentile, not the average.

| Cognitive Bias | Mitigation |
|----------------|------------|
| **Availability heuristic** — over-prioritizing the last incident | Rank problems by recurrence × impact, not recency |
| **Hero complex** — being the person who always saves the day | If you're always the hero, your system is fragile. Automate your heroism. |
| **Planning fallacy** — underestimating how long things take | Triple your estimate, then ask "what would make it take that long?" — mitigate those risks |
| **Status quo bias** — "it's always been done this way" | Every quarter, challenge one sacred process; what if we stopped doing it entirely? |

### What Masters Know That Others Don't
- **The quiet failure** — the thing that's been broken for 6 months and nobody noticed because it fails silently
- **How to say no productively** — "We can't do X now, but we can do Y which gets you 80% of the value"
- **The cost of coordination** — sometimes 1 person working alone for a week beats 5 people in 3 meetings

### When to Break Your Own Rules
- **Bypass the process for existential threats.** If the site is down, fix it first; process comes after.
- **Over-communicate during ambiguity.** When the path is unclear, silence is worse than wrong information.

## Operating at Different Levels

| Level | Scope | You... |
|-------|-------|--------|
| **L1** | Single process | Execute defined workflows reliably and flag deviations |
| **L2** | Team process | Own team-level processes; optimize for team efficiency; remove bottlenecks |
| **L3** | Department operations | Design cross-team operational workflows; make build-vs-automate decisions |
| **L4** | Org operations | Define operational strategy for the organization; set standards and tooling |
| **L5** | Industry operations | Create operational frameworks adopted across the industry |

**Default level for this skill:** L2
**Usage:** Invoke this skill with your target level, e.g., "as an L3 technical writer, manage..."

For full level definitions, see `skills/00-framework/skill-levels/SKILL.md`.

## When to Use

<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Generating or maintaining API reference documentation from OpenAPI/Swagger specifications
- Writing architecture decision records (ADRs) to capture technical decisions with context and consequences
- Crafting high-quality READMEs that serve as the entry point for open-source or internal repositories
- Building operational runbooks: incident response procedures, deployment guides, troubleshooting playbooks
- Creating developer onboarding guides that reduce time-to-first-commit for new team members
- Designing and maintaining a documentation site structure with clear information architecture
- Writing automated changelogs from conventional commits or manually curated release notes
- Structuring a knowledge base that stays discoverable and up-to-date as the codebase evolves

## Decision Trees

### Documentation Type Selection

```
                     ┌──────────────────────────────┐
                     │ START: What type of docs?       │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Audience integrating with our   │
                    │ API or SDK?                     │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────────┐    ┌──────▼──────────┐
                    │ API Reference │    │ Audience operating │
                    │ OpenAPI/Swagger│    │ or troubleshooting │
                    │ auto-generated│    │ a running system?   │
                    │ + conceptual │    └──┬──────────┬────┘
                    │ guides        │       │YES       │NO
                    └───────────────┘  ┌────▼────┐ ┌──▼──────────┐
                                       │Runbooks,│ │Audience      │
                                       │Troubleshoot│ │onboarding  │
                                       │guides,  │ │(new dev on  │
                                       │Incident │ │team)?       │
                                       │response │ └──┬──────┬───┘
                                       │procedures│   │YES   │NO
                                       └──────────┘ ┌▼────┐┌▼──────────┐
                                                     │On-  ││Conceptual │
                                                     │board││Guides,    │
                                                     │guide││Architecture│
                                                     │+    ││Decisions  │
                                                     │setup ││(ADRs),    │
                                                     │script││Tutorials  │
                                                     └─────┘└───────────┘
```
**When to build API Reference:** Integrating developers — auto-generate from OpenAPI 3.x spec, include authentication, endpoints, request/response examples, error codes.
**When to build Runbooks:** Operators/on-call — incident response procedures, deployment guides, rollback steps, health check endpoints, alert response playbooks.
**When to build Onboarding Guides:** New team members — dev environment setup, architecture overview, first commit walkthrough, team norms, toolchain setup.
**When to build Conceptual Guides:** Learning/understanding — architecture overviews, design patterns, ADRs, tutorials, "why" not just "how".

### Information Architecture Decision

```
                     ┌──────────────────────────────┐
                     │ START: How to structure docs?  │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Documentation spans >50 pages  │
                    │ with >5 distinct audience      │
                    │ types?                         │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────────┐    ┌──────▼──────────┐
                    │ Diátaxis      │    │ Single product,  │
                    │ framework:    │    │ single audience? │
                    │ Tutorials     │    └──┬──────────┬────┘
                    │ How-to Guides │       │YES       │NO
                    │ Explanation   │  ┌────▼────┐ ┌──▼──────────┐
                    │ Reference     │  │Flat     │ │Simple       │
                    │ (4 quadrants) │  │structure│ │hierarchy:   │
                    └───────────────┘  │with     │ │Getting      │
                                       │search as│ │Started,     │
                                       │primary  │ │Guides,      │
                                       │nav      │ │Reference,   │
                                       └─────────┘ │Changelog    │
                                                   └─────────────┘
```
**When to use Diátaxis:** Large docs site (>50 pages), multiple audience types — 4-quadrant structure (tutorials, how-to guides, explanation, reference) with cross-links.
**When to use Flat + Search:** Small product, single audience — good search as primary navigation, minimal hierarchy, fast to maintain.
**When to use Simple Hierarchy:** Medium scope — Getting Started → Guides → Reference → Changelog, works for most open-source projects and startups.

### README Quality Gate

```
                     ┌──────────────────────────────┐
                     │ START: Is this README good?    │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Does it answer: "What is this?" │
                    │ "Why does it exist?" "How do I │
                    │ get started?" in <30 seconds?  │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────────┐    ┌──────▼──────────┐
                    │ Has one-liner │    │ Missing critical │
                    │ install       │    │ section. Add:    │
                    │ command?      │    │ - Description    │
                    └──┬────────┬───┘    │ - Install        │
                       │YES     │NO      │ - Usage          │
                  ┌────▼───┐ ┌─▼────────┐│ - Contributing   │
                  │Has badge│ │Add clear││ - License        │
                  │(CI,     │ │install  │└──────────────────┘
                  │version, │ │section  │
                  │license)?│ └─────────┘
                  └──┬───┬──┘
                     │YES│NO
                ┌────▼─┐┌▼───────┐
                │README││Add     │
                │PASSES││missing │
                │quality││badges │
                │gate  │└────────┘
                └──────┘
```
**When README passes:** One-liner description, install command, basic usage example, contributing link, license, CI/version badges — new developer builds in <5 minutes.
**When README needs work:** Missing any of: description, install, usage, contributing, license. Each missing piece costs new contributors 5-20 minutes of frustration.

### API Documentation Generation Strategy

```
                     ┌──────────────────────────────┐
                     │ START: How to generate API     │
                     │ documentation?                 │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Have an OpenAPI 3.x spec        │
                    │ (machine-readable, validated)?  │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────────┐    ┌──────▼──────────┐
                    │ Auto-generate │    │ API is simple    │
                    │ from spec:    │    │ (<10 endpoints)? │
                    │ Swagger UI,   │    └──┬──────────┬────┘
                    │ Redoc,        │       │YES       │NO
                    │ Scalar — CI   │  ┌────▼────┐ ┌──▼──────────┐
                    │ pipeline       │  │Manual MD│ │Create       │
                    │ regenerates   │  │with code│ │OpenAPI spec │
                    │ on spec change│  │snippets │ │first — it   │
                    └───────────────┘  │from tests│ │becomes the  │
                                       └─────────┘ │source of    │
                                                   │truth        │
                                                   └─────────────┘
```
**When to auto-generate from spec:** Have validated OpenAPI 3.x — use Redoc (static, clean), Swagger UI (interactive), or Scalar (modern). CI pipeline: spec change triggers doc regeneration + deploy.
**When to write manually in Markdown:** <10 endpoints, no OpenAPI spec — write Markdown with code snippets extracted from integration tests, ensure examples are runnable.
**When to create OpenAPI spec first:** >10 endpoints without spec — invest in creating the spec; it becomes source of truth for docs, SDK generation, and validation.

### Changelog Strategy

```
                     ┌──────────────────────────────┐
                     │ START: Changelog approach?     │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Team uses Conventional Commits  │
                    │ AND has CI pipeline?            │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────────┐    ┌──────▼──────────┐
                    │ Auto-generate │    │ Releases are     │
                    │ changelog from│    │ infrequent       │
                    │ commits:      │    │ (monthly or      │
                    │ standard-     │    │ slower)?         │
                    │ version +     │    └──┬──────────┬────┘
                    │ commitlint +  │       │YES       │NO
                    │ release-please│  ┌────▼────┐ ┌──▼──────────┐
                    │or semantic-   │  │Manual   │ │Keep a       │
                    │release        │  │curated  │ │CHANGELOG.md │
                    └───────────────┘  │changelog│ │write entries │
                                       │per      │ │per PR in    │
                                       │release  │ │keepachangelog│
                                       └─────────┘ │.com format  │
                                                   └─────────────┘
```
**When to auto-generate:** Conventional Commits + CI — semantic-release or release-please generates changelog, bumps version, publishes. Zero manual effort but requires commit discipline.
**When to manually curate:** Infrequent releases — hand-write curated changelog per release with narrative, highlights, migration guide. Better for marketing-facing releases.
**When to keep running CHANGELOG.md:** Per-PR entries in keepachangelog.com format — each PR adds entry under Unreleased; cut version on release. Good for fast-moving projects.

## Core Workflow

<!-- QUICK: 30s -- scan phase titles to understand the process -->
<!-- DEEP: 10+min -->
### Phase 1 (~15 min): Documentation Audit & Strategy

1. **Documentation Inventory** — Catalog all existing docs: repository READMEs, wiki pages, `/docs` directories, API specs (OpenAPI, GraphQL), ADRs, runbooks, onboarding materials, blog posts with technical content, internal Google Docs/Notion pages. For each: audience, freshness (last updated), accuracy (% still correct), discoverability (how do people find it?).
2. **Audience & Needs Mapping** — Identify documentation personas:
   - **New Developer**: setup guide, architecture overview, first contribution walkthrough, coding standards.
   - **Experienced Developer**: API reference, advanced configuration, <!-- DEEP: 10+min -->
debugging guide, performance tuning.
   - **Operator/SRE**: deployment guide, runbooks, monitoring setup, disaster recovery, scaling.
   - **Product/Support**: feature documentation, changelog, known issues, FAQ.
   - **External User** (for public APIs/products): getting started, SDK guides, API reference, tutorials.
   - Map each existing doc to a persona and a user journey stage (discover, learn, build, troubleshoot).
3. **Gap Analysis** — Cross-reference inventory with persona needs. Common gaps: no architecture overview (new developers get lost), no runbooks (operators escalate to developers), API reference exists but no usage examples (developers read source code), docs exist but are undiscoverable (no search, poor IA).
4. **Docs-as-Code Strategy** — Define toolchain:
   - **Source format**: Markdown (with frontmatter for metadata), MDX (Markdown + JSX for interactive docs), AsciiDoc (for complex technical docs).
   - **Static site generator**: Docusaurus (React-based, great for OSS), VitePress (Vue-based, fast, simple), Mintlify (hosted, beautiful, API-first), Nextra (Next.js-based).
   - **Versioning**: docs versioned alongside code releases (Git tags → doc versions). Maintain docs for current + N-1 versions.
   - **CI/CD**: docs built and deployed on merge to main; preview deployments per PR.
   - **Linting**: Vale or textlint for style guide enforcement; markdownlint for formatting.
5. **Deliverable: Documentation Strategy Document** — Inventory, persona map, gap analysis, prioritized backlog of docs to create/update, toolchain decision, IA proposal for doc site.

<!-- DEEP: 10+min -->
### Phase 2 (~30 min): Core Documentation Types

1. **README** — Every repository's landing page. Structure:
   - **Title & Badge Bar**: build status, coverage, version, license, downloads.
   - **One-line description**: what the project does, who it's for.
   - **Quick Start** (the most important section): install, minimal working example, expected output. Must work in under 5 minutes.
   - **Motivation**: why does this exist? What problem does it solve? When should I use it versus alternatives?

> See [references/core-workflow.md](references/core-workflow.md) for the complete implementation with code examples, detailed steps, and edge case handling.

## Cross-Skill Coordination

<!-- QUICK: 30s -- table of who to talk to when -->
Technical writing serves developers, product teams, support, and users. Docs degrade when writers are isolated from the people building and using the product.

### Decision Gates & Artifacts

- **Content Accuracy Verification Gate**: Every procedure and code sample must be tested by a naive user before publishing. API examples must be runnable with complete imports and dependencies. Output: verified documentation with test evidence.
- **Style Guide Compliance Gate**: All docs must pass Vale or textlint linting in CI. Consistent terminology, voice, and formatting across all documentation surfaces. Output: linting-passed documentation.
- **README Quality Gate**: Every repository README must answer "What is this?", "Why does it exist?", and "How do I get started?" in under 30 seconds. Must include: one-liner install command, basic usage example, contributing link, license. Output: quality-gate-passed README.
- **Publishing Approval Gate**: Public-facing docs require stakeholder sign-off from `product-manager` for feature accuracy, `security-reviewer` for sensitive content, and `devrel-advocate` for community-facing content. Output: approved documentation for publish.
- **Freshness Gate**: Docs not updated in >6 months flagged for review. Stale docs archived or updated. Content audit runs quarterly. Output: freshness report with stale page list and action plan.
- **OpenAPI Spec Quality Gate**: Every endpoint in the spec must have summary, description, request example, response example, and error responses. Spec validated in CI. Output: validated OpenAPI 3.x specification.

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **Product Strategist** | Feature launches, product roadmap, user personas | Feature specs, target audience, release timeline, key messaging |
| **Frontend/Backend Developers** | API docs, SDK references, code samples | API signatures, code review, accuracy verification, changelog entries |
| **DevRel / Developer Advocate** | Tutorials, quickstarts, community content | Developer pain points, common questions, community feedback on docs |
| **UX Designer** | UI text, onboarding flows, error messages | Terminology consistency, microcopy review, information architecture |
| **QA Engineer** | Documentation testing, accuracy verification | Step-by-step verification, edge cases, version-specific behavior |
| **Support / Customer Success** | Knowledge base, troubleshooting guides, FAQs | Top support tickets, common user confusion, missing documentation |
| **Documentation Engineer** | Docs platform, CI/CD, tooling | Platform requirements, build pipeline, style guide enforcement automation |
| **SEO Specialist** | Public-facing docs, developer blog | Content hierarchy, meta descriptions, crawlability of docs site |
| **Security Reviewer** | Security-sensitive docs, architecture runbooks | What can be public vs internal-only, redaction requirements |
| **Project Manager** | Documentation deliverables, release coordination | Docs milestones, review cycles, localization timelines |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| API breaking change (major version bump) | DevRel, Product Strategist, Support | Migration guide needed; developer communication required |
| New feature launching without documentation | Product Strategist, Project Manager | Docs gap; may delay launch or cause support burden |
| Docs build failing in CI (blocked deployment) | Documentation Engineer, DevOps | Docs site update blocked; user-facing docs are stale |
| Support tickets for undocumented feature spike (>5/week) | Support, Product Strategist | Missing docs creating support load; prioritize doc creation |
| Content audit reveals >15% stale/outdated pages | Product Strategist, Documentation Engineer | Docs trust eroding; batch refresh or archival needed |
| Major docs contribution from community (PR >500 lines) | DevRel, Documentation Engineer | Review and merge; community recognition opportunity |
| Style guide or terminology change | All Writers, UX Designer, DevRel | Consistency across all docs surfaces |
| Localization request for new language/market | Project Manager, DevRel | Translation pipeline, glossary setup, locale-specific content |

### Escalation Path

| Situation | Escalate To | Rationale |
|-----------|------------|-----------|
| Docs repeatedly blocked by engineering unavailability (>2 sprints) | **CTO Advisor** + Project Manager | Docs are part of the product; engineering prioritization needed |
| Documentation is factually incorrect and causing production incidents | **Engineering Lead** + QA Lead | Quality crisis; docs review process fundamentally broken |
| Stakeholders want to deprecate public docs in favor of gated/internal-only | **DevRel** + Product Strategist + CEO Strategist | Developer trust and SEO impact; strategic decision |
| Docs platform migration required (tooling EOL, scaling limits) | **Documentation Engineer** + CTO Advisor | Platform decision; migration cost and timeline |
| Legal or compliance issue in published docs | **Legal Advisor** + Security Reviewer | Regulatory exposure; content takedown or revision |

### Route to Other Skills

| If the Request Involves | Route To | Rationale |
|--------------------------|-----------|-----------|
| Docs platform, CI/CD pipeline, and build tooling | `documentation-engineer` | Platform engineering for the docs site and automation |
| Developer tutorials, quickstarts, and community content | `devrel-advocate` | Developer-facing content with community engagement goals |
| API implementations and code samples | `backend-developer` | Working code that docs describe; accuracy verification |
| OpenAPI spec creation and API contract design | `api-designer` | Source-of-truth API specifications that drive documentation |
| UI text, error messages, and in-product microcopy | `ux-writer` | Terminology consistency across product and documentation |
| Feature launches and user persona context | `product-manager` | Target audience, release timeline, and key messaging for documentation |
| SEO and discoverability for public-facing docs | `seo-specialist` | Content hierarchy, meta descriptions, and crawlability |

## Proactive Triggers

<!-- QUICK: 30s — triggers that demand immediate action -->

| Trigger | Action | Why |
|---------|--------|-----|
| New API endpoint merged without docs (`GET /v2/users` with 0 doc coverage) | Block merge; hold `api-designer` gate; write OpenAPI `summary` + `description` + request/response examples before deploy | OpenAPI spec is the source of truth for API docs — gaps create cascading issues in SDK generation, frontend integration, and support |
| Docs site build failing in CI (broken links, missing pages, failed Vale lint) | Halt deployment pipeline; notify `documentation-engineer`; fix links and lint before next release | Published docs with dead links or lint errors erode developer trust — users assume the product is equally broken |
| Support reports >5 tickets referencing same undocumented feature/behavior in a week | Prioritize doc for that feature; coordinate with `customer-support-engineer` for ticket triage data; publish within 48 hours | Docs gaps directly increase support cost — every undocumented feature is a recurring support ticket |
| Product Manager announces feature launch without documentation timeline | Raise immediate flag in launch checklist; gate the release until docs are drafted and reviewed | Docs are not a post-launch nice-to-have — public launch without docs guarantees first-impression failure |
| Content audit reveals >15% of docs pages stale (>6 months without update) | Schedule freshness sprint; archive dead pages; flag remaining stale pages with `product-manager` for ownership assignment | Stale docs are worse than no docs — they actively mislead users and erode trust in the entire docs corpus |
| OpenAPI spec drift detected — code behavior differs from spec (e.g., field removed, type changed, new required field) | Halt dependent SDK generation; sync spec with `api-designer` and `backend-developer`; validate with contract tests before regenerating docs | Spec-code divergence makes every downstream consumer (SDKs, frontend, mobile, third-party) break silently |
| Security-sensitive content (architecture diagrams, IPs, internal endpoints) accidentally committed to public-facing docs | Immediately redact and force-push clean version; notify `security-reviewer`; audit git history for the exposure window; update docs review checklist | Public disclosure of internal architecture increases attack surface — must be treated as a security incident |
| Translation/localization request for a new market (locale not yet supported in the toolchain) | Coordinate with `translation-manager` and `localization-engineer`; assess glossary coverage, TM readiness, and MT quality for the target locale; budget 2–4 weeks pipeline setup | Rushing localization without proper TM, glossary, and pipeline produces garbled docs that harm brand in new markets |

## What Good Looks Like

> When technical writing is applied perfectly, API references are generated from specs so they never go stale, READMEs enable a new developer to make their first commit in under 10 minutes, runbooks are

> See [references/what-good-looks-like.md](references/what-good-looks-like.md) for the full quality standard.

## Deliberate Practice

```mermaid
graph LR
    A[Execute<br/>process] --> B[Measure<br/>friction] --> C[Identify<br/>bottleneck] --> D[Re-design<br/>process] --> A

```

| Level | Practice | Frequency |
|-------|----------|-----------|
| **Novice** | Document your current workflow; highlight every step that requires human judgment or waiting | Monthly |
| **Competent** | Run a "process autopsy" on a recent initiative: what took longest, where were the miscommunications? | Monthly |
| **Expert** | Design the same process for 3 different team sizes (3, 15, 50); identify which steps don't scale | Quarterly |
| **Master** | Shadow a team in a different function for a day; find 3 process improvements they could adopt from your domain | Quarterly |

**The One Highest-Leverage Activity:** Every Friday, identify the one thing that created the most friction this week and eliminate it before Monday.

## Gotchas

- **Documentation that's API reference without narrative** — you document every endpoint, every parameter, every response code. A developer trying to BUILD something doesn't know which endpoints to call in what ORDER. Reference docs answer "what does this do?" Guides answer "how do I accomplish X?" You need both. Without guides, reference is a dictionary without sentences.
- **"This is straightforward" in documentation** — it's straightforward to YOU because you wrote the API. To a developer encountering it for the first time, nothing is straightforward. Every time you use "straightforward," "simply," "just," or "obviously," replace it with the actual steps. "Just configure the OAuth flow" → 15 specific steps.
- **Code samples with placeholder values that look real** — `api_key = "YOUR_API_KEY_HERE"` — a developer copies this, doesn't replace the placeholder, and spends 30 minutes debugging "Authentication failed: YOUR_API_KEY_HERE is not a valid API key." Code samples must either: (a) use a clearly invalid placeholder that throws a specific error, or (b) be executable with test credentials.
- **Versioned docs where Google indexes ALL versions** — a user searches "how to configure" and gets the v1.0 docs (from 2021). They follow the instructions, which reference deprecated APIs, and conclude your product is broken. Old docs must have `noindex` meta tags AND a banner linking to the current version.

## Verification

- [ ] Guides: every major use case has a step-by-step guide (not just API reference)
- [ ] Language audit: zero instances of "straightforward," "simply," "just," or "obviously" in docs
- [ ] Code samples: every sample is either executable (test credentials) or has clearly non-functional placeholders
- [ ] Versioned docs: old versions have `noindex` + banner linking to current version — verified via Google Search Console
- [ ] Doc testing: top 10 code samples tested in CI against latest API version

## References

Detailed reference material loaded on demand:

- **Core Workflow — Full Implementation**: See [core-workflow.md](references/core-workflow.md)
- **Anti-Patterns**: See [anti-patterns.md](references/anti-patterns.md)
- **Best Practices**: See [best-practices.md](references/best-practices.md)
- **Calibration — How to Know Your Level**: See [calibration.md](references/calibration.md)
- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Cost-Effective Decision Table**: See [cost-decisions.md](references/cost-decisions.md)
- **Error Decoder**: See [error-decoder.md](references/error-decoder.md)
- **Footguns**: See [footguns.md](references/footguns.md)
- **MVP vs Growth vs Scale**: See [mvp-growth-scale.md](references/mvp-growth-scale.md)
- **Scalability Decision Tree**: See [scalability-tree.md](references/scalability-tree.md)
- **Scale Depth**: See [scale-depth.md](references/scale-depth.md)
- **Sub-Skills**: See [sub-skills.md](references/sub-skills.md)
- **Token-Efficient Workflow**: See [token-workflow.md](references/token-workflow.md)
- **When NOT to Use This Skill (Overkill)**: See [when-not-to-use.md](references/when-not-to-use.md)

