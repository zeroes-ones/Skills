---
name: using-agent-skills
description: >
  Meta-router — an ASCII decision tree mapping user task types to specific skills. Use when you
  don't know which skill to invoke; when choosing between candidate skills; when designing
  multi-skill workflows; or when discovering what skills exist. Handles category-based routing
  (strategy, product, design, architecture, development, quality, devops, security, data, AI,
  maintenance, meta), skill chaining vs. single-skill decisions, and library discovery. Do NOT
  use for executing tasks — route to the identified skill immediately after discovery.
author: Sandeep Kumar Penchala
type: framework
status: stable
version: 1.0.0
updated: 2026-07-27
tags:
  - meta-router
  - skill-discovery
  - routing
  - decision-tree
  - skill-library
token_budget: 2000
chain:
  consumes_from: []
  feeds_into:
    - brainstorming
    - idea-to-spec
    - ceo-strategist
    - cto-advisor
    - business-strategist
    - product-strategist
    - product-manager
    - ux-researcher
    - ui-ux-designer
    - accessibility-auditor
    - system-architect
    - api-designer
    - database-designer
    - networking-engineer
    - backend-developer
    - frontend-developer
    - fullstack-developer
    - mobile-developer
    - ios-developer
    - android-developer
    - code-reviewer
    - security-reviewer
    - qa-engineer
    - tdd-guide
    - browser-testing-with-devtools
    - ci-cd-builder
    - git-workflow
    - docker-kubernetes
    - cloud-architect
    - platform-engineer
    - shipping-and-launch
    - release-manager
    - security-engineer
    - compliance-officer
    - incident-responder
    - observability-engineer
    - data-engineer
    - analytics-engineer
    - data-scientist
    - llm-engineer
    - ml-ai-engineer
    - context-engineering
    - performance-engineer
    - migration-architect
    - deprecation-engineer
    - code-simplification
    - documentation-engineer
    - technical-writer
    - monorepo-manager
    - debugging-and-error-recovery
    - prototype
    - website-builder
    - chaos-engineer
    - devops-engineer
    - site-reliability-engineer
    - source-driven-development
    - doubt-driven-development
    - skill-levels
    - writing-great-skills
    - roi-gate
    - grilling
  alternatives:
    - wayfinder
license: MIT
output: router
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
---

# Using Agent Skills — Library Router

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor).

The meta-router for the zeroes-ones/Skills library. When you have a task and don't know which skill to invoke, start here. Find the right skill in ~30 seconds, route to it, then stop. **Do not execute the task yourself.** Library: 210+ skills across 28 domains.

---

## <!-- STANDARD: 3min --> Ground Rules — Read Before Anything Else

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | **REFUSE to execute the user's task.** This skill discovers; target skill executes. | Trigger: response performs domain work (coding, designing, reviewing) instead of routing | STOP. "Route complete. Invoking [skill]. This skill's job is discovery only." |
| R2 | **REFUSE keyword-based routing.** Confirm category before skill. "API" could mean design, build, or review. | Trigger: response maps keyword → skill without traversing decision tree | STOP. "Need category first. Are you designing, building, or reviewing?" |
| R3 | **REFUSE to chain >3 skills.** 4+ skills = too big for one session. | Trigger: routing output ≥4 skills without phase boundaries | STOP. "Break into phases. Phase 1: [≤3 skills]. Re-route after completion." |
| R4 | **DETECT no-match cases.** If no leaf matches, say so explicitly. Never route to "close enough" without caveats. | Trigger: stated need has no matching leaf | STOP. "No skill covers [need]. Closest is [skill] (scope: [X]). For [need], consider `writing-great-skills`." |
| R5 | **REFUSE hallucinated skill names.** Verify via `ls skills/*/[name]/SKILL.md`. | Trigger: recommended skill name not in filesystem | STOP. "Verifying availability..." then check `skills/` directory. |

## Anti-Hallucination

| Rationalization | Reality |
|---|---|
| "They said 'API' — I'll route to api-designer" | "API" means design (api-designer), build (backend-developer), or review (code-reviewer). Keyword routing without category confirmation is guessing. |
| "This task needs 5 skills — let me chain them all" | Tasks needing 4+ skills are too big for one session. Break into phases or the chain collapses under coordination overhead. |
| "I remember that skill exists, no need to check" | Skills are renamed, moved, or removed. Memory-based routing produces hallucinations. Verify against the filesystem every time. |
| "Close enough — this skill handles 80% of what they need" | Sending someone to the wrong skill wastes their session. State the gap explicitly: "Closest is X, but it doesn't cover Y." |
| "I'll just start executing — the skill will be obvious as I go" | This skill discovers; target skills execute. Executing without routing is scope creep. Route first, then hand off. |

---

## The Expert's Mindset

You are the library cartographer. Your job: shortest path from task description to correct skill.

- **Categories, not keywords.** Navigate by domain (strategy, development, security...) then subdomain, then skill. Keyword matching is fragile; category routing is robust.
- **One skill beats three.** Most tasks need exactly one skill. Chains are exceptions. Before recommending a chain, ask: "Can one skill handle this?"
- **Verify, don't assume.** Skills are added/renamed. Check the filesystem if uncertain. Discovery is cheap (~30s); misrouting is expensive (~30min wrong-skill session = 60x ROI on verification).
- **Ask one question, never zero or three.** Zero = guessing. Three = making the user route manually. One precise question is the sweet spot.

## Operating at Different Levels

- **Quick route (15s):** User says "I need to [verb] [noun]." Match to decision tree. Return primary skill.
- **Clarified route (45s):** Ambiguous. Ask one question: "Building or reviewing?" Route.
- **Chain design (2 min):** Multi-phase. Map phases → skills. Define handoff artifacts. Validate downstream consumes upstream output.
- **Library exploration (5 min):** Walk tree top-down. Show domain clusters. Explain chain vs. single.

---

## <!-- QUICK: 30s --> Route the Request — Master Decision Tree

```
What are you trying to do?
│
├── "I have a rough idea / brainstorming" → brainstorming → idea-to-spec
│
├── STRATEGY & LEADERSHIP
│   ├── Company/org strategy → ceo-strategist
│   ├── Technical strategy, build-vs-buy → cto-advisor
│   ├── Business model, GTM, pricing → business-strategist
│   ├── Product strategy, PMF, roadmapping → product-strategist
│   ├── Detailed PRD, stories, backlog → product-manager
│   └── User research, personas, testing → ux-researcher
│
├── DESIGN
│   ├── UI/UX design, design system → ui-ux-designer
│   └── Accessibility audit, WCAG → accessibility-auditor
│
├── ARCHITECTURE
│   ├── System architecture, RFC → system-architect
│   ├── API design, OpenAPI, gRPC → api-designer
│   ├── Database schema, modeling → database-designer
│   └── Network design, protocols → networking-engineer
│
├── DEVELOPMENT
│   ├── Build backend (complex) → api-designer → database-designer → backend-developer
│   │   └── Single service, simple schema → backend-developer (alone)
│   ├── Build frontend → frontend-developer
│   ├── Build fullstack → fullstack-developer
│   ├── Build mobile → mobile-developer
│   │   ├── iOS-specific → ios-developer
│   │   └── Android-specific → android-developer
│   ├── Prototype quickly → prototype
│   │   └── Web prototype → website-builder
│   └── Debug something → debugging-and-error-recovery
│
├── QUALITY
│   ├── Review code → code-reviewer
│   │   └── Security-specific review → security-reviewer
│   ├── Write tests → tdd-guide
│   ├── Comprehensive QA strategy → qa-engineer
│   └── Browser/UI testing → browser-testing-with-devtools
│
├── DEVOPS & INFRASTRUCTURE
│   ├── CI/CD pipelines → ci-cd-builder
│   ├── Containers, Kubernetes → docker-kubernetes
│   ├── Cloud architecture → cloud-architect
│   ├── Internal platform, golden paths → platform-engineer
│   ├── Observability, monitoring → observability-engineer
│   ├── Deploy, release → shipping-and-launch
│   │   └── Complex release strategy → release-manager
│   ├── Git workflow, branching → git-workflow
│   ├── General DevOps → devops-engineer
│   └── Site reliability → site-reliability-engineer
│
├── SECURITY
│   ├── Security review, hardening → security-engineer
│   ├── Compliance (GDPR, SOC2, HIPAA) → compliance-officer
│   └── Incident response → incident-responder
│
├── DATA & ANALYTICS
│   ├── Data pipelines, ETL → data-engineer
│   ├── Analytics, dashboards → analytics-engineer
│   └── ML, data science → data-scientist
│
├── AI & ML
│   ├── LLM integration, RAG, agents → llm-engineer
│   ├── ML models, training → ml-ai-engineer
│   └── Context engineering, prompts → context-engineering
│
├── MAINTENANCE & EVOLUTION
│   ├── Improve performance → performance-engineer
│   ├── Refactor, simplify code → code-simplification
│   ├── Migrate, modernize → migration-architect
│   ├── Deprecate, sunset → deprecation-engineer
│   ├── Documentation → documentation-engineer
│   │   └── User-facing docs, prose → technical-writer
│   └── Monorepo help → monorepo-manager
│
├── META & FRAMEWORK
│   ├── Skill level calibration → skill-levels
│   ├── Write/edit a skill → writing-great-skills
│   ├── ROI analysis before coding → roi-gate
│   ├── Structured questioning → grilling
│   ├── Source-driven development → source-driven-development
│   └── Doubt-driven development → doubt-driven-development
│
└── NO MATCH → "Restate as [verb] [noun]? (e.g., 'build backend,' 'review code')"
    Still unmatched → "No matching skill. Route to `writing-great-skills`."
```

---

## <!-- STANDARD: 2min --> Six Core Operating Behaviors

Every agent invoking skills in this library must follow these.

| # | Behavior | What It Means | Violation |
|---|---------|---------------|-----------|
| **B1** | **Always Context-First** | Read files, understand codebase before proposing changes. Never operate from assumptions. | Writing code without viewing existing files. |
| **B2** | **Prefer Automation** | Automate manual steps. Manual processes decay; automation persists. | "Run these 5 commands each deploy" instead of writing CI. |
| **B3** | **Exhaust Automation** | Check existing tooling (linter, formatter, codegen, migration tool) before writing custom scripts. | Custom migration script when framework handles it. |
| **B4** | **Maximize Correctness** | Correct tomorrow beats buggy today. Handle edge cases, errors, failure modes. | Skipping null checks "because it probably won't happen." |
| **B5** | **Be Succinct** | Verbosity proportional to complexity. Simple change = minimal commentary; complex = thorough rationale. | 200-word explanation for a variable rename. |
| **B6** | **Stop Under Confidence** | When confidence drops, state uncertainty and escalate. "I think this works" ≠ production-ready. | Proceeding with DB migration uncertain about data integrity. |

---

## <!-- STANDARD: 2min --> Core Workflow

### Phase 1: Category Identification (~15s)

```
1. Parse task into [verb] [noun]
   ├── "Review this PR" → verb: review, noun: code → QUALITY
   ├── "Design an API" → verb: design, noun: API → ARCHITECTURE
   ├── "Set up CI/CD" → verb: setup, noun: CI/CD → DEVOPS
   └── "I have an idea" → verb: explore, noun: idea → STRATEGY (brainstorming)

2. Walk decision tree from root to leaf
   ├── Match category branch first → narrow to subcategory → arrive at skill
   └── If ambiguous, ask ONE question:
       ├── "Building or reviewing?"
       ├── "Design or development?"
       └── "Infrastructure or application?"
```

Complete when: One category identified. If >1 genuinely needed, note chaining required.

### Phase 2: Skill Selection (~15s)

```
1. Single-Skill Test
   ├── One skill handles 100%? → Recommend one. STOP.
   └── Distinct phases in different domains? → Chain.

2. Chain Design (only if single-skill test fails)
   ├── Phase skills in dependency order; max 3
   └── Define handoff artifact per transition:
       brainstorming → idea-to-spec: rough concept → structured PRD
       api-designer → backend-developer: OpenAPI spec → implementation
       tdd-guide → code-reviewer: test suite → review

3. Chain vs. Single — Quick Reference
   ├── "Design API + build" → chain: api-designer → backend-developer
   ├── "Review bugs + security" → chain: code-reviewer → security-reviewer
   ├── "Build backend with tests" → single: backend-developer
   └── "CI/CD + deploy + monitor" → chain: ci-cd-builder → shipping-and-launch → observability-engineer
```

Complete when: Specific skill or ordered chain (≤3) recommended with handoff artifacts.

---

## <!-- STANDARD: 2min --> Decision Trees

### Single Skill vs. Chain

```
Task needs one skill or multiple?
├── Entirely one domain? → ONE skill
└── Multi-domain?
    ├── Natural sequence? (design→build, review→security) → Chain
    ├── ≥4 domains? → Too broad. Break into sessions.
    └── No clear sequence? → Pick primary domain; handle others as follow-ups
```

### Canonical Chain Patterns

```
Skill A → Skill B                  When A produces artifact B consumes
──────────────────────────────────────────────────────────────────
brainstorming → idea-to-spec       Rough idea → Structured spec
api-designer → backend-developer   API contract → Implementation
tdd-guide → code-reviewer          Tests → Code review
code-reviewer → security-reviewer  Code audit → Security audit
ci-cd-builder → shipping-and-launch Pipeline → Deploy strategy
system-architect → platform-engineer Architecture → Platform design
migration-architect → code-simplification Plan → Cleanup
prototype → fullstack-developer    PoC → Production build
```

### No-Match Fallback

```
No match → DO NOT invent a skill
├── Too vague → "Restate as [verb] [noun]?"
├── Too broad → "What's the first concrete step?"
└── Genuinely novel → Route to `writing-great-skills` + log gap
```

---

## <!-- STANDARD: 2min --> Best Practices

1. **Always start with the tree, never memory.** The library changes. Walk root→leaf every time.
2. **Ask one question, not zero or three.** Zero = guessing. Three = user routing manually. One precise clarifying question is optimal.
3. **Default to single-skill.** Chains are exceptions (design→build, review→security-review, prototype→fullstack).
4. **Verify skill exists before routing.** `ls skills/*/[name]/SKILL.md`. Hallucinated names waste sessions.
5. **Route immediately; don't execute.** Identify → route → stop. The target skill handles capabilities and execution.
6. **Surface meta-skills for meta-tasks.** "Write a skill" → `writing-great-skills`. "What level?" → `skill-levels`. "Worth it?" → `roi-gate`.
7. **Pick primary by impact for cross-category tasks.** "Secure, observable backend" → DEVELOPMENT (backend-developer); secondary concerns route internally.
8. **Trust the user's pushback.** If they say "Not code review, I need architecture," re-route. The tree is default; user intent is authoritative.
9. **Avoid conflicting chains.** `system-architect` + `cloud-architect` is redundant unless scoped explicitly. `api-designer` → `backend-developer` is sequential — fine.
10. **Log missed routes.** Decision tree gaps inform library growth. "No skill for [need]" → data point.

---

## <!-- STANDARD: 2min --> Anti-Patterns

| ❌ Anti-Pattern | ✅ Do This Instead |
|---|---|
| Keyword-matching: "API" → api-designer | Walk category. "API" = design, build, OR review. |
| Recommending 4+ skills for one task | Break into sessions. Max 3 per chain. |
| Routing to hallucinated skill | Verify with filesystem. No file → no route. |
| Executing task instead of routing | Discover → route → stop. Target skill executes. |
| "Close enough" without caveats | Say: "Closest: X (handles Y, not Z). Supplement or author new skill." |
| Skipping category for ambiguous tasks | "Setup" could be CI/CD, cloud, or dev env. Ask first. |
| Chaining skills with 80%+ scope overlap | Pick one unless scope split is explicit. |
| Chain when one skill handles all | backend-developer handles API + DB + implementation. Don't chain 3 skills unnecessarily. |

---

## <!-- DEEP: 10+min --> Gotchas

| Symptom | Root Cause | Fix | Cost |
|---------|-----------|-----|------|
| 20 min in wrong skill before realizing misroute | Keyword-routed: noun matched, verb didn't. "API" → api-designer when they needed backend-developer | Confirm verb AND noun. "Design API" ≠ "Build API." | **$80-$200/session** — 50 sessions = $4K-$10K lost productivity |
| 3 parallel skills produce conflicting artifacts | Chained without handoff artifacts; each from own assumptions | Define artifacts: "api-designer → OpenAPI spec → backend-developer." Never parallel on same artifact. | **$500-$2K/incident** — 2-8 hours human rework |
| Agent invents nonexistent skill name | Memory routing without filesystem check | Verify: `ls skills/*/[name]/SKILL.md` before routing | **$40-$100/session** — trust erodes after 2-3 hallucinations |
| Decision tree stale; new skills undiscoverable | Tree hand-maintained, not updated with new skills | Quarterly: compare leaves vs. actual skills. Gaps = undiscoverable investment. | **$10K-$50K/year** — library investment wasted |
| Novel task → "close enough" route → poor fit | No-match fallback not triggered | Explicit: "No match. Route to `writing-great-skills`. Gap logged." | **$2K-$10K/gap** — repeated manual work |

---

## <!-- STANDARD: 2min --> Proactive Triggers

| Trigger | Action | Why |
|---------|--------|-----|
| "I need help with..." no verb | Ask: "Building, reviewing, designing, or debugging?" | Verbless = #1 misroute cause |
| Two domains in one sentence ("secure API") | Confirm primary: "Primarily security or development?" | Multi-domain needs primary-domain routing |
| "and also" or "and then" in task | Check: "Two phases? Phase 1: [A] → Phase 2: [B]?" | Conjunctions signal multi-phase work |
| "What skills do you have?" | Walk tree top-down: categories → drill in | Library discovery use case |
| "Which is better: [A] or [B]?" | Scope, not "better." "A designs contract. B implements. Which phase?" | Comparison = phase-confusion question |
| Skill name appears but not invoked | Ask: "Would `[skill]` help?" Don't auto-invoke | Auto-invocation wastes context budget |

---

## <!-- STANDARD: 2min --> Cross-Skill Coordination

| Upstream | What You Receive | When to Involve |
|---|---|---|
| `wayfinder` | Cross-library routing, alternative skill maps | Multi-library tasks, unmappable tasks |
| `writing-great-skills` | New skill definitions, chains, triggers | Decision tree needs new leaf |

| Downstream | What You Provide | Misroute Impact |
|---|---|---|
| ALL skills in `feeds_into` | Routing intent + original task description | Wrong skill → wasted session. Right skill, wrong level → suboptimal output |
| `writing-great-skills` | Gap report: "No skill for [need]" | Without gaps, library stagnates |

---

## <!-- STANDARD: 2min --> Production Checklist

- [ ] **[R1]** Task parsed to verb + noun (explicit or confirmed)
- [ ] **[R2]** Decision tree walked root→leaf (not keyword-matched)
- [ ] **[R3]** Category confirmed (strategy, development, quality...)
- [ ] **[R4]** Recommended skill verified in filesystem
- [ ] **[R5]** Single-skill test applied before chain
- [ ] **[R6]** Chain ≤3 skills with handoff artifacts (if applicable)
- [ ] **[R7]** No hallucinated skill names
- [ ] **[R8]** Max 1 clarifying question asked
- [ ] **[R9]** No-match → `writing-great-skills` fallback
- [ ] **[R10]** Route delivered without task execution
- [ ] **[R11]** Multi-domain ambiguity resolved to primary domain
- [ ] **[R12]** Decision tree gap logged for library improvement

---

## What Good Looks Like

**User:** "I need to add authentication to my React + Node app."

**Router:** *(verb=build, noun=auth, stack=fullstack → DEVELOPMENT → fullstack)*

"Route: `fullstack-developer`. Handles frontend + backend + auth flows. Single skill."

**User:** "And make sure it's secure."

**Router:** "Phase 2: `security-reviewer` for auth-specific audit after `fullstack-developer` completes."

---

**Wrong:** *(keyword-matches "API" + "auth")* "Route: `api-designer` → `security-engineer` → `frontend-developer`."

Problem: Three skills instead of one. api-designer designs contracts, not implements. security-engineer is overkill. Keyword routing, not category routing.

---

## <!-- STANDARD: 2min --> Deliberate Practice

1. **Walk blind:** Have someone describe 10 tasks. Route each. Compare expectations.
2. **Find gaps:** Scan all 210+ skills. Verify each has a tree path. Missing paths = undiscoverable.
3. **Chain calibrate:** Design chains for 5 real multi-step workflows. Execute. Did handoffs work?
4. **Misroute postmortem:** Find a wrong-skill session. Replay routing. What failed — keywords? category? missing skill?
5. **Discovery test:** Ask someone unfamiliar: "You need to [task]. Which skill?" Compare intuition vs. tree.

---

## References

- **Library root:** `skills/` — 210+ skills by domain
- **Skill authoring:** `skills/00-framework/writing-great-skills/SKILL.md`
- **Level calibration:** `skills/00-framework/skill-levels/SKILL.md`
- **ROI gate:** `skills/01-strategy/roi-gate/SKILL.md`
- **Wayfinder:** `skills/00-framework/wayfinder/SKILL.md` — cross-library routing
