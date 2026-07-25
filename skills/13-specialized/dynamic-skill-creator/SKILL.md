---
name: dynamic-skill-creator
description: >
  Use when creating, upgrading, or auditing SKILL.md files to 10/10* production-quality standards.
  Handles the complete skill-building methodology: 12 mandatory sections, ground rules with violation
  examples, anti-rationalization tables, dollar-quantified gotchas, ASCII decision trees, error
  recovery protocols, verification guardrails, scale-depth matrices, cross-skill coordination,
  and sub-skill references. Accepts a domain/task description and produces a validated, chain-ready
  skill file. Bootstrap-capable — can recreate itself and all 188+ repository skills. Do NOT use
  for writing code documentation, API docs, user manuals, or general content — route to
  technical-writer or documentation-engineer.
author: Sandeep Kumar Penchala
license: MIT
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
type: specialized
status: stable
version: 1.0.0
updated: 2026-07-24
tags:
  - meta-skill
  - skill-generation
  - skill-authoring
  - quality-automation
  - bootstrap
token_budget: 4500
chain:
  consumes_from:
    - writing-great-skills
    - code-reviewer
    - technical-writer
    - system-architect
    - product-strategist
    - qa-engineer
    - security-reviewer
    - documentation-engineer
  feeds_into:
    - writing-great-skills
    - agent-eval-pipeline
    - cross-agent-skills-packaging
  alternatives: []
---

# Dynamic Skill Creator
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

The meta-skill that generates 10/10* production-quality skills. This skill encodes the complete methodology used to build all 185+ skills in this repository. Follow it to produce skills indistinguishable from hand-crafted ones — every section domain-specific, every gotcha dollar-quantified from real incidents, every decision tree encoding years of practitioner wisdom.

## Anti-Rationalization — No Excuses

| Rationalization | Reality |
|---|---:|
| "I know this domain cold — I don't need to research it for gotchas." | Domain expertise ≠ skill-writing expertise. You'll miss CVEs you've never heard of, post-mortems you've never read, and footguns that bite developers differently than they bite you. Researching reveals the gap between what you know and what the agent needs to know. Skills without research read as confident but shallow — the agent spots the gaps in the first 3 gotchas. |
| "I'll copy-paste from a similar skill and tweak the names." | You'll inherit ground rules that don't apply, gotchas that reference wrong technologies, and chain connections to skills that have nothing to do with this domain. The agent will execute instructions meant for React Native when you're building a Kubernetes skill. 3 hours of editing later, you'll still find stragglers. Template FROM a similar skill — don't COPY it. |
| "The template handles quality — I just need to fill in the blanks." | The template is scaffolding, not substance. A hollow shell passes structure validation but the agent produces garbage because the ground rules say "Be careful with auth" instead of "Never embed JWT secrets in client-side code — use httpOnly cookies with SameSite=Strict." 60% of skill-building time should be domain research, 40% structuring. |
| "Validation passes, so the skill is good." | Validation checks structure, not substance. A skill can pass 6/6 governance checks with every section filled and still be worthless — generic ground rules, gotchas without dollar figures ("can be expensive"), decision trees copied from another domain. Green checkmarks measure format compliance, not practical utility. Manual review: read every gotcha, verify every dollar figure, test every decision tree path. |
| "One skill can cover multiple related domains — it saves maintenance." | Broad skills lack depth. "Cloud Security" helps no one because AWS IAM specifics, GCP IAM specifics, and Azure RBAC specifics are fundamentally different. The agent reads "use IAM roles" and applies the wrong platform's model. Narrow scope, deep expertise. One skill = one domain. Use sub-skills for variants. |
| "I'll add the production checklist and anti-rationalization table later — those are the hardest sections." | These sections are the agent's psychological defense system. Without anti-rationalization, the agent falls for optimism bias ("we're too small to be a target"). Without a production checklist, the agent doesn't know when to stop generating output. You're shipping a skill with no brakes and no steering. The hardest sections are the most important. |
| "Generic ground rules are fine — the agent will figure out the specifics." | "Write secure code" means nothing when the agent faces a choice between OAuth2 PKCE (correct) and implicit flow (dangerous). Generic ground rules are the #1 cause of skills producing plausible-looking but dangerous output. Every ground rule must be testable: "Never store JWT in localStorage — use httpOnly cookies" is testable. "Be secure" is not. |
| "Token budget doesn't matter — I'll let the compiler minify later." | A 2,500-line skill consumes 40%+ of the agent's context window before it processes a single user instruction. The agent skips sections, misses ground rules, and produces incomplete output because it ran out of room. Rich content ≠ verbose content. Every line must earn its token cost. Target 400-700 lines for standard skills, 600-1000 for security/critical. |

## Ground Rules — Read Before Anything Else

These rules govern skill CREATION, not general software development. Violation means STOP — the generated skill is incomplete.

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|---|---|---|
| R1 | REFUSE to generate a skill without completing Phase 0 (Discovery). A skill built without domain research is a confidence trap — it looks complete but teaches the agent wrong patterns. | Trigger: User says "create a skill for X" and you haven't asked at least 5 of the 8 Phase 0 discovery questions before generating content | STOP. Respond: "Before generating this skill, I need to understand: (1) domain/task scope, (2) problem it solves, (3) target user, (4) complexity tier, (5) upstream/downstream chain connections, (6) reference skills to model from, (7) top 3 most expensive mistakes, (8) top 3 rationalizations. Which of these can you answer?" |
| R2 | DETECT placeholder content in generated skills — "TODO", "TBD", "Add examples here", "[Coming soon]", "..." in any section. Placeholder content trains the agent that incompleteness is acceptable. | Trigger: `grep -n "TODO\|TBD\|\[Coming soon\]\|\.\.\." generated-skill.md` returns any matches | STOP. Respond: "Placeholder content detected at [lines]. Every section must be fully fleshed out before the skill is usable. Return to the relevant Phase and complete the section." |
| R3 | REFUSE to generate gotchas without dollar figures ($X,XXX+). "Can be expensive" is a platitude. The agent needs concrete cost anchoring to prioritize prevention. | Trigger: `grep -c "\$[0-9]" generated-skill.md` returns < 10 for a standard skill or < 15 for a security/critical skill | STOP. Respond: "Insufficient dollar-quantified gotchas. Each gotcha must include a specific cost impact: downtime hours × revenue rate, breach fines, migration costs, or lost-install conversion impact. Research real incidents via CVE databases, post-mortems, and HN incident threads." |
| R4 | DETECT anti-rationalization tables that don't follow the 4-column format: "The Temptation \| Why It Feels Right \| The Devastating Reality \| Prevention". Other formats (2-column, bullet lists) fail to provide the psychological defense the agent needs. | Trigger: `grep -c "Temptation\|Feels Right\|Devastating Reality\|Prevention" generated-skill.md` returns < 24 (6 rows × 4 columns) | STOP. Respond: "Anti-rationalization table format violation. Must be exactly 4 columns: The Temptation \| Why It Feels Right \| The Devastating Reality \| Prevention. Minimum 6 rows, each row exposing the psychological bias behind the rationalization." |
| R5 | DETECT decision trees without YES/NO branching or ASCII art characters (`├──`, `└──`, `│`, `▼`). Text-only if/else trees lack the visual decision structure agents use for pattern matching. | Trigger: Decision tree section uses only `if/else` prose with no ASCII box-drawing characters | STOP. Respond: "Decision trees must use ASCII art with YES/NO branches. Minimum 3 trees, each with at least 2 levels of branching. Use characters: ┌─┐└─┘├─┤│▼. Verify rendering in raw markdown before declaring complete." |
| R6 | DETECT orphaned skills — generated skill has empty `chain_consumes_from` or `chain_feeds_into` in its frontmatter. Orphaned skills are undiscoverable through the chain router and exist in isolation. | Trigger: `chain_consumes_from: []` OR `chain_feeds_into: []` in generated frontmatter | STOP. Respond: "Chain connections are mandatory. Every skill must declare at least 1 consumes_from AND 1 feeds_into. Search existing skills for related domains, identify natural upstream/downstream relationships, and populate chain connections." |
| R7 | DETECT ground rules in generated skills that lack concrete violation examples. "Be careful with authentication" is not a ground rule. "Never store JWT secrets in client-side code — use httpOnly cookies with SameSite=Strict" is. | Trigger: `grep -c '"Be careful\|"Make sure\|"Always remember\|"Consider\|"Try to' generated-skill.md` returns > 0 | STOP. Respond: "Generic ground rules detected. Every ground rule must be: domain-specific, actionable (tells agent EXACTLY what to do or not do), testable by behavioral evals, and illustrated with a concrete violation example showing what happens when broken." |
| R8 | REFUSE to declare a skill complete until it passes the self-recreation test: could this skill, as written, generate a new version of ITSELF at 10/10* quality? If the instructions are circular or self-referential without concrete processes, they fail. | Trigger: Reading the skill's own Phase 0-9 workflow — does it produce enough domain-specific content to regenerate itself? | STOP. Respond: "Self-recreation test failed. The skill's workflow must be concrete enough that following it — with no external knowledge — produces a complete skill. If a Phase says 'research the domain' without specifying HOW to research, the workflow is incomplete." |
| R9 | DETECT token budget violations — standard skill > 700 lines or security/critical skill > 1000 lines. Token bloat reduces the agent's available context for actual task execution. | Trigger: `wc -l generated-skill.md` returns > 700 (standard) or > 1000 (security/critical) | STOP. Respond: "Token budget exceeded. Target 400-700 lines for standard skills, 600-1000 for security/critical. Prune using the no-op test: does removing this sentence change default agent behavior? If no, delete it. Move reference material to references/ directory." |
| R10 | DEFAULT to repository conventions when uncertain. Every repository has format conventions, section ordering, and style patterns. When in doubt about how to structure a section, reference existing 10/10 skills as templates — never invent a new pattern. | Trigger: Generated skill uses a section format, heading style, or table structure not found in any existing 10/10 skill in this repository | STOP. Respond: "Format deviation detected. When uncertain, reference existing 10/10* skills: mobile-developer, backend-developer, security-reviewer, code-reviewer, writing-great-skills. Their section formats are battle-tested across hundreds of agent invocations. Default to the repository standard." |


- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset

You are not just writing a SKILL.md — you are encoding years of domain expertise into tokens that reliably produce expert behavior in an AI agent. The agent will follow your instructions literally, pattern-match against your decision trees, and internalize your ground rules as non-negotiable constraints. Every sentence you write shapes thousands of future agent decisions.

### The Mental Model Shift
* **The agent is your apprentice, not your peer.** It has encyclopedic general knowledge but zero domain-specific judgment. Your job is to provide the judgment framework — the "when NOT to do X" that general knowledge lacks. The most valuable sentence in any skill is "Do NOT use [approach] when [condition]."
* **Research reveals what expertise conceals.** You know your domain so well that you've forgotten what's hard about it. Research CVEs, post-mortems, and Stack Overflow questions to rediscover the pain points. The gotchas that make you say "oh right, that got me too in 2018" are the ones that matter.
* **Structure is the message.** Agents pattern-match against structure before they process content. A well-structured decision tree communicates more in 30 lines than 300 lines of prose explanation. Tables beat paragraphs. ASCII trees beat tables. Ground rules as mechanical triggers beat prose admonitions.
* **The bootstrap test is the ultimate quality gate.** Ask: "If I fed this skill to a fresh agent with no other skills loaded, could that agent generate a 10/10* skill for any domain?" If the answer is no, you have gaps. This is why the Phase 0 discovery questions, the domain mapping table, the quality rubric, and the gotcha research guide must be complete.

### Cognitive Biases That Corrupt Skill Creation
| Bias | How It Manifests | Antidote |
|-------|------------------|----------|
| **Curse of knowledge** | Skipping fundamental gotchas because "everyone knows that" — writing for experts, not for the agent who has no context | Research what beginners ask on Stack Overflow. The most-upvoted questions are what your skill needs to cover. |
| **Overconfidence bias** | Assuming you can write a 10/10* skill in 2 hours without research — "I've been doing this for 15 years" | Time-box research: 60% of skill-building time on domain research (CVEs, post-mortems, incident reports), 40% on structuring. |
| **Completion bias** | Satisfied when validation passes — "6/6 checks, ship it!" — ignoring that validation measures structure, not substance | Manual review after validation: read every gotcha aloud, verify every dollar figure against a real source, trace every decision tree path to a terminal node. |
| **Template fixation** | Filling sections mechanically without adapting to the domain — "Section 5 says 'Gotchas' so I'll list 10 random warnings" | Every section must serve the domain. A Kubernetes skill's gotchas are about misconfigurations and RBAC; a healthcare skill's are about PHI exposure and audit trails. |
| **Novelty seeking** | Inventing new section formats, table structures, or heading conventions because "this domain is different" | Default to repository standard. The format is battle-tested. If your domain genuinely needs a new section, justify it against at least 3 existing 10/10* skills that don't have it. |

### What Skill Creators Know That Others Don't
- **Gotchas sourced from real incidents are 10x more persuasive than generic warnings.** "Misconfigured S3 bucket exposes customer data" is forgettable. "Capital One's 2019 breach: $190M in fines + $80M remediation because a single S3 bucket had `AuthenticatedUsers: READ` — the exact misconfiguration this gotcha prevents" is unforgettable.
- **The anti-rationalization table is the hardest and most important section.** It takes 30+ minutes to write well because you must identify the lies developers tell themselves AND understand the psychology behind those lies. "We're too small to be a target" = optimism bias + normalcy bias. "The framework handles security" = diffusion of responsibility + authority bias toward framework authors.
- **Chain connections determine discoverability, not just correctness.** A brilliant skill with empty `chain_feeds_into` is invisible to the chain router. When agents navigate the skill graph, orphaned skills don't appear in any routing path. Every skill needs at least 2 upstream and 2 downstream connections.
- **The quality rubric must be self-referential.** The rubric in this skill is what you use to grade generated skills. It must be specific enough that two independent evaluators would assign the same grade to the same skill. "8/10 (Good)" is worthless. "8/10: Domain-specific ground rules with some examples, but 3 ground rules lack violation stories" is actionable.

## When to Use

- User says "I need a skill for [domain]" or "create a skill for [task]" — full skill generation from scratch
- User says "boost this skill from 6/10 to 10/10*" — targeted enhancement of an existing skill
- User says "generate a SKILL.md for [domain/role/task]" — direct skill file generation
- User describes a domain and asks "is there a skill for this?" — domain analysis + skill boundary check
- User needs to onboard a new domain into the skill repository — complete skill lifecycle from discovery to validation
- User asks "what makes a 10/10* skill?" — quality rubric education and skill auditing
- User needs to regenerate a skill that has drifted from quality standards — audit → gap analysis → targeted regeneration
- User wants to validate an existing skill against 10/10* standards — quality audit with specific improvement recommendations

Do NOT use dynamic-skill-creator for: writing code documentation (route to technical-writer), creating README files (route to documentation-engineer), writing API docs (route to api-designer), or editing individual sections of existing skills (route to writing-great-skills). Do NOT use for generating non-skill content like blog posts, tutorials, or marketing copy.

## Route the Request

<!-- TWO-TIER ROUTING: Auto-Route table (machine) → Intent Route tree (human fallback) -->

### Auto-Route (No User Input Required)
Evaluate these conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|---|---|
| A1 | `file_contains(user_message, "generate.*skill\|create.*skill\|build.*skill\|write.*skill")` AND `file_contains(user_message, "[domain]\|[role]\|[task]")` | Full generation protocol. Jump to **Core Workflow** — Phase 0 (Discovery). |
| A2 | `file_contains(user_message, "boost\|improve\|upgrade\|enhance")` AND `file_contains(user_message, "skill")` AND `file_exists("path/to/existing/SKILL.md")` | Skill boost mode. Jump to **Decision Trees** — Skill Boost Strategy. |
| A3 | `file_contains(user_message, "audit\|validate\|check\|review")` AND `file_contains(user_message, "skill")` | Audit mode. Jump to **Decision Trees** — Quality Audit. |
| A4 | `file_contains(user_message, "domain.*analysis\|what.*category\|which.*template")` AND NOT `file_contains(user_message, "create\|generate")` | Domain analysis only. Jump to **Domain Mapping Table** section. |
| A5 | User message contains only a domain name with no action verb (e.g., "Kubernetes", "GraphQL API") | Assume full generation. Proceed to **Core Workflow** — Phase 0 and ask discovery questions. |
| A6 | `file_contains(user_message, "minimal\|quick\|fast\|MVS")` AND `file_contains(user_message, "skill")` | Minimal Viable Skill path. Jump to **Decision Trees** — MVS vs Full Skill. |
| A7 | `file_contains(user_message, "recreate\|regenerate\|rebuild\|dynamic-skill-creator")` AND `file_contains(user_message, "itself\|self")` | Bootstrap test. Jump to **Core Workflow** — Phase 10 (Self-Recreation Test). |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

```
What are you trying to do?
├── Create a brand new skill from scratch → Start at "Core Workflow > Phase 0: Discovery"
├── Boost an existing skill from 6/10 to 10/10* → Go to "Decision Trees > Skill Boost Strategy"
├── Generate a skill for a specific domain → Go to "Domain Mapping Table" → match domain to template → Core Workflow Phase 0
├── Audit a skill for quality → Go to "Decision Trees > Quality Audit"
├── Validate a skill against 10/10* standards → Go to "Verification Guardrails" → run through checklist
├── Need a quick Minimal Viable Skill (MVS) → Go to "Minimal Viable Skill Template" → generate compact version
├── Not sure if a new skill is needed → Go to "Decision Trees > Skill Boundary Check"
├── Need to understand skill quality standards → Go to "The Skill Quality Rubric" section
├── Need to connect a skill to the chain graph → Go to "Cross-Skill Coordination" → chain connection protocol
├── Fix a skill that failed validation → Go to "Error Recovery" → "Generated skill fails validation"
└── Recreate this skill (bootstrap test) → Start at "Core Workflow > Phase 10 (Self-Recreation Test)"
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Decision Trees

### Skill Generation Strategy

```
                     ┌──────────────────────────────────┐
                     │ START: What kind of skill        │
                     │ generation is needed?            │
                     └─────────────┬────────────────────┘
                                   │
              ┌────────────────────▼────────────────────┐
              │ Is this a brand new skill               │
              │ (no existing file)?                     │
              └────┬──────────────────────┬─────────────┘
                   │ YES                  │ NO
                   ▼                      ▼
        ┌──────────────────┐    ┌──────────────────────┐
        │ Full Generation   │    │ Is the existing skill│
        │ Protocol:         │    │ rated < 7/10?        │
        │ Phase 0 → Phase 9 │    └──┬───────────────┬───┘
        │ Complete all       │       │ YES           │ NO
        │ 10 phases          │       ▼               ▼
        └──────────────────┘  ┌────────────┐  ┌──────────────┐
                              │ Full Rebuild│  │ Targeted     │
                              │ from Phase 0│  │ Enhancement: │
                              │  — existing │  │ Audit → Gap  │
                              │  is template│  │ Analysis →   │
                              │  only       │  │ Phase 2-9    │
                              └────────────┘  │ on gaps only │
                                              └──────────────┘
```
**When full generation:** New domain, no prior skill, or existing skill is fundamentally wrong (wrong ground rules, broken decision trees).  
**When targeted enhancement:** Existing skill has good structure but weak gotchas, missing anti-rationalization, or insufficient verification guardrails. Don't rebuild — enhance.

### MVS vs Full 10/10* Skill

```
                     ┌──────────────────────────────────┐
                     │ START: What depth is needed?      │
                     └─────────────┬────────────────────┘
                                   │
              ┌────────────────────▼────────────────────┐
              │ Is speed more important                  │
              │ than completeness right now?            │
              └────┬──────────────────────┬─────────────┘
                   │ YES                  │ NO
                   ▼                      ▼
        ┌──────────────────┐    ┌──────────────────────┐
        │ MVS Path:         │    │ Is this a security,  │
        │ 5 ground rules,   │    │ compliance, or       │
        │ 5 gotchas, 4 anti-│    │ critical infra skill?│
        │ rationalization,  │    └──┬───────────────┬───┘
        │ 300-400 lines.    │       │ YES           │ NO
        │ Ship in 90 min.   │       ▼               ▼
        └──────────────────┘  ┌────────────┐  ┌──────────────┐
                              │ Full 10/10*│  │ Full 10/10*  │
                              │ Extended:  │  │ Standard:    │
                              │ 600-1000   │  │ 400-700 lines│
                              │ lines, full│  │ All 12+      │
                              │ security   │  │ sections     │
                              │ depth      │  │ fleshed out  │
                              └────────────┘  └──────────────┘
```
**When MVS:** User needs a skill urgently, domain is well-understood, and the skill will be enhanced later. MVS is NOT "low quality" — it's full 10/10 quality but domain-light (fewer gotchas, fewer decision trees).  
**When NOT MVS:** Security, compliance, healthcare, financial, or critical infrastructure domains. These demand full gotcha depth from day one — an incomplete security skill is dangerous.

### Skill Boundary Check

```
                     ┌──────────────────────────────────┐
                     │ START: Does this domain need     │
                     │ a new skill?                     │
                     └─────────────┬────────────────────┘
                                   │
              ┌────────────────────▼────────────────────┐
              │ Does an existing skill already cover    │
              │ this domain (check by name + description│
              │ + tags)?                                │
              └────┬──────────────────────┬─────────────┘
                   │ YES                  │ NO
                   ▼                      ▼
        ┌──────────────────┐    ┌──────────────────────┐
        │ REUSE: Route to   │    │ Is this a distinct   │
        │ existing skill.   │    │ domain with unique   │
        │ If enhancement    │    │ ground rules AND     │
        │ needed, open a PR │    │ unique gotchas?      │
        │ on existing skill.│    └──┬───────────────┬───┘
        └──────────────────┘       │ YES           │ NO
                                   ▼               ▼
                            ┌────────────┐  ┌──────────────┐
                            │ CREATE new │  │ Consider sub- │
                            │ skill via  │  │ skill of an   │
                            │ Phase 0-9  │  │ existing      │
                            │ protocol   │  │ parent skill  │
                            └────────────┘  └──────────────┘
```
**When to create a sub-skill instead:** The domain is a specialization of an existing skill (e.g., "iOS Developer" is a sub-specialization of "Mobile Developer"). The parent skill handles 70% of the domain; the sub-skill adds the 30% platform-specific content.  
**When a new skill is warranted:** The domain has fundamentally different ground rules, gotchas, decision trees, and chain connections from any existing skill.

### Domain Mapping Decision

```
                     ┌──────────────────────────────────┐
                     │ START: Which template skill      │
                     │ should I model from?             │
                     └─────────────┬────────────────────┘
                                   │
              ┌────────────────────▼────────────────────┐
              │ Is this a development/engineering skill? │
              └────┬──────────────────────┬─────────────┘
                   │ YES                  │ NO
                   ▼                      ▼
        ┌──────────────────┐    ┌──────────────────────┐
        │ Model from:       │    │ Is this a security    │
        │ backend-developer,│    │ or compliance skill?  │
        │ mobile-developer, │    └──┬───────────────┬───┘
        │ or frontend-      │       │ YES           │ NO
        │ developer         │       ▼               ▼
        └──────────────────┘  ┌────────────┐  ┌──────────────┐
                              │ Model from │  │ Use Domain    │
                              │ security-  │  │ Mapping Table │
                              │ reviewer,  │  │ to find       │
                              │ compliance-│  │ closest match │
                              │ officer    │  │ in repository │
                              └────────────┘  └──────────────┘
```
**When no template exists:** This is a genuinely new domain type. Start from the Minimal Viable Skill template and build the 12 sections from scratch. Model decision trees and ground rules from the closest related skill. Flag this as a pioneering skill in the frontmatter description.

## Core Workflow

This is the complete skill generation protocol — Phase 0 through Phase 10. Each phase builds on the previous. Skip phases only if you're in targeted enhancement mode (audit → identify gaps → fill only those gaps).

### Phase 0: Discovery & Domain Analysis (~15 min)

Before writing ANY content, answer these 8 questions. The answers determine the entire structure of the generated skill.

**1. What domain/task does this skill cover?**
Be specific. "React Native mobile development" — not "mobile development." "PostgreSQL database administration" — not "databases." The name becomes the skill's directory name and frontmatter `name` field.

**2. What problem does it solve?**
What does the agent produce after using this skill? A working React Native app with offline support? A hardened Kubernetes deployment? A HIPAA-compliant data pipeline? This becomes the "What Good Looks Like" paragraph.

**3. Who is the target user (agent persona)?**
Is this for backend developers, mobile developers, security engineers, data scientists, or a generalist? The persona determines the assumed knowledge level. A skill for security engineers can assume knowledge of OWASP; a skill for generalists must explain basic security concepts.

**4. What's the complexity tier?**
- **Tier 1 (core specialized):** Narrow domain, deep expertise. E.g., iOS Developer, GraphQL Engineer. 400-600 lines.
- **Tier 2 (broad applicable):** Wide domain, moderate depth. E.g., Fullstack Developer, DevOps Engineer. 500-700 lines.
- **Tier 3 (security/critical):** High-stakes domain. E.g., Security Reviewer, HIPAA Implementation. 600-1000 lines.

**5. What existing skills should it connect to (upstream/downstream)?**
Search the repository for related skills. A "Kubernetes Developer" skill should consume from `docker-kubernetes`, `devops-engineer`, `cloud-architect` and feed into `site-reliability-engineer`, `security-engineer`.

**6. Are there existing reference skills to model from?**
Identify 2-3 top-tier skills in related domains. Study their ground rules, gotchas, decision trees. Template from them — don't copy. The mobile-developer skill serves as a template for any platform-specific development skill. The security-reviewer skill serves as a template for any security domain skill.

**7. What are the 3 most expensive mistakes in this domain?**
These become gotchas. Research: search "[domain] expensive bug" on Hacker News, search "[domain] post-mortem", search CVE database for domain-specific vulnerabilities, search "[domain] outage cost" on Google. Each mistake should have a verifiable dollar figure from a real incident.

**8. What are the 3 most common rationalizations?**
These become anti-rationalization entries. Ask: "What lies do practitioners in this domain tell themselves?" For each rationalization, identify the cognitive bias behind it: optimism bias, normalcy bias, sunk cost fallacy, authority bias, Dunning-Kruger effect, diffusion of responsibility.

**Output:** A discovery document (in memory — do not create files) answering all 8 questions. This document drives all subsequent phases.

### Phase 1: Structural Scaffolding (~10 min)

**1. Determine the category directory.**
Map the domain to a category directory. Use this mapping:
- Strategy/leadership → `01-strategy/`
- Product management → `02-product/`
- Design/UX → `03-design/`
- Architecture → `04-architecture/`
- Development → `05-development/`
- Quality/testing → `06-quality/`
- DevOps/infrastructure → `07-devops/`
- Security → `08-security/`
- Data/AI → `09-data/`
- Growth/marketing → `10-growth/`
- Legal/compliance → `11-legal/`
- Operations → `12-operations/`
- Specialized/emerging → `13-specialized/`

If no category fits, use `13-specialized/`. Only create a new category with strong justification (at least 3 planned skills).

**2. Generate the YAML frontmatter.**
```yaml
---
name: {kebab-case-name}
description: >
  Use when {triggers}. Handles {capabilities}. Do NOT use for {boundaries}.
author: Sandeep Kumar Penchala
license: MIT
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
type: {matching category type}
status: stable
version: 1.0.0
updated: {today's date}
tags: [{3-8 domain-specific tags}]
token_budget: {estimated based on tier}
chain:
  consumes_from: [{at least 2 upstream skills}]
  feeds_into: [{at least 2 downstream skills}]
  alternatives: []
---
```
**Critical:** The description must follow the triggers-only format: "Use when [situation]. Handles [capabilities]. Do NOT use for [boundaries]." No process language in the description field.

**3. Create the file and directory structure.**
```bash
mkdir -p skills/{category}/{skill-name}/references/
```
The file path must match: `skills/{category}/{skill-name}/SKILL.md`

**Output:** Frontmatter written, directory created, file scaffolded.

### Phase 2: Domain-Specific Ground Rules (~20 min)

Ground rules are the HARDEST section to write well. They must be:
- **Domain-specific:** Not "Be careful with auth" but "Never embed API keys in client-side code — use OAuth2 PKCE with secure token storage"
- **Actionable:** The agent can mechanically check for violations
- **Testable:** A behavioral eval can verify the agent follows the rule
- **Violation-illustrated:** Each rule shows exactly what happens when broken

**Research process for ground rules:**
1. Search OWASP Top 10 for the domain's technology stack
2. Search CWE Top 25 for domain-specific weakness categories
3. Search "[domain] common mistakes" on Stack Overflow (sort by votes)
4. Search "[domain] production incident" on Hacker News
5. Identify platform-specific constraints (OS limits, framework quirks, language footguns)
6. For each finding, formulate as: "REFUSE/DETECT [bad thing] → Mechanical Trigger → Violation Response"

**Ground rule format (non-negotiable):**
| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|---|---|---|
| R1 | REFUSE [action] | Trigger: [grep-able condition] | STOP. Respond: "[Exact message with fix]" |

**Target:** 6-10 ground rules. Standard skills: 6-8. Security/critical skills: 8-10.

**What good looks like for Phase 2:** Every ground rule is domain-specific. No rule could be copied into a different skill without modification. A domain expert reads the rules and says "yes, these are exactly the 8 things that go wrong in this domain."

### Phase 3: Decision Trees (~25 min)

Build 3-5 ASCII decision trees. Each tree must have:
- A clear START node with a decision question
- At least 2 levels of YES/NO branching
- Terminal nodes with concrete recommendations
- "When NOT to use" guidance at terminal nodes
- ASCII box-drawing characters: `┌─┐└─┘├─┤│▼`

**Decision trees to build (in priority order):**

**1. Architecture/approach selection tree**
The core "what technology/approach should I use?" question. E.g., for a mobile skill: Native vs React Native vs Flutter vs PWA. For a database skill: PostgreSQL vs MongoDB vs DynamoDB. Include performance benchmarks, team skill requirements, and deployment complexity at terminal nodes.

**2. Pattern selection tree**
A common implementation choice. E.g., CQRS vs CRUD, Event-driven vs Request-response, Microservices vs Monolith, REST vs GraphQL vs gRPC. Terminal nodes must include: "Use [pattern] when [3 conditions]. Do NOT use when [2 conditions]."

**3. Safety/security decision tree**
A security-critical choice. E.g., Self-hosted vs managed service, Encrypt at rest vs application-level encryption, OAuth2 vs API keys. Terminal nodes must include worst-case scenarios for wrong choices.

**4. Scale/deployment decision tree**
A deployment or scaling decision. E.g., Serverless vs Container vs VM, Single-region vs Multi-region, CDN vs origin-only. Terminal nodes must include cost estimates and latency comparisons.

**5. Domain-specific workflow tree (optional for standard skills, required for security/critical)**
A decision that's unique to this domain. E.g., for a healthcare skill: "PHI data handling: de-identify vs encrypt vs tokenize."

**ASCII tree formatting rules:**
- Use `┌─┐` for start nodes, `└─┘` for terminal nodes
- Branch with `├──` and `└──`, vertical lines with `│`
- Label branches with `YES` and `NO`
- Include a brief explanation paragraph after each tree
- Verify rendering in raw markdown — no broken characters

**What good looks like for Phase 3:** An agent facing the domain's core architectural question can follow the decision tree to a concrete recommendation in under 30 seconds. The tree encodes 5+ years of practitioner experience in choosing the right approach.

### Phase 4: Core Workflow Phases (~35 min)

Design 8-10 progressive phases that mirror the real development/execution lifecycle for this domain.

**Phase structure pattern:**
```
### Phase N (~time estimate): Phase Title
1. **Action verb:** Concrete step with exact commands, code, or configuration
2. **Action verb:** Next concrete step
3. **Verify:** What to check to confirm the phase is complete
**Output:** Tangible deliverable from this phase
```

**Phase template (adapt to domain):**
- **Phase 0:** Discovery/Requirements gathering — What problem are we solving? What are the constraints?
- **Phase 1:** Setup/Environment — Tool installation, project scaffolding, configuration
- **Phase 2:** Core Architecture — System design, component structure, data flow
- **Phase 3:** Primary Implementation — The main feature/system/process being built
- **Phase 4:** Integration — Connecting with external systems, APIs, databases
- **Phase 5:** Error Handling & Edge Cases — What goes wrong and how to handle it
- **Phase 6:** Performance Optimization — Profiling, benchmarking, optimization
- **Phase 7:** Security Hardening — Threat modeling, vulnerability remediation, security testing
- **Phase 8:** Testing & Validation — Unit, integration, e2e, load testing
- **Phase 9:** Deployment & Monitoring — Production deployment, observability, alerting

**For non-development domains (strategy, operations, design):** Adapt the phases to the domain's workflow. A "Business Strategist" skill's phases would be market analysis → model design → financial projection → validation → iteration. A "Technical Writer" skill's phases would be audience analysis → outline → draft → review → publish.

**What good looks like for Phase 4:** A practitioner can follow the phases sequentially and produce a complete, production-quality output. Each phase has time estimates that are realistic. No phase says "think about X" — every phase says "DO X" with concrete steps.

### Phase 5: Gotchas (~25 min)

Research and document 10+ dollar-quantified gotchas. This is where the skill earns its 10/10* rating — generic warnings get 6/10; dollar-quantified incident-backed gotchas get 10/10*.

**Gotcha research protocol:**
1. **CVE database search:** Search NVD for domain-specific CVEs (e.g., "react native CVE", "kubernetes CVE"). For each CVE, calculate: breach cost (IBM average: $4.45M), remediation hours × engineer hourly rate ($150/hr), downtime hours × revenue/hour.
2. **Hacker News post-mortems:** Search `site:news.ycombinator.com "[domain] outage" OR "[domain] breach" OR "[domain] bug"`. Extract the cost figures from the post-mortem.
3. **Cloud provider outage reports:** AWS, GCP, Azure publish post-mortems with impact analysis. Extract the customer impact costs.
4. **Stack Overflow:** Search "[domain] most expensive mistake" or "[domain] cost us". The war stories have real dollar figures.
5. **Industry reports:** IBM Cost of a Data Breach report, Google SRE book incident chapters, Honeycomb outage post-mortems.

**Gotcha format (each must follow this pattern):**
```
- **Gotcha title with dollar figure in first sentence.** Description of the temptation and what goes wrong.
  **Total cost: $XX,XXX-$XXX,XXX in [specific impact — not just "costs"].**
  Fix: [3-5 concrete prevention steps — exact commands, configuration, architecture changes].
```

**Target:** 10+ gotchas for standard skills, 15+ for security/critical skills. Every gotcha must have a SPECIFIC dollar range. "Can be expensive" → reject. "$15,000-$50,000 in lost installs from negative reviews" → accept.

**What good looks like for Phase 5:** A domain expert reads the gotchas and says "I wish I had read this before my $50,000 mistake in 2021." Every gotcha references a real incident class (even if anonymized).

### Phase 6: Anti-Rationalization Table (~20 min)

The anti-rationalization table is the agent's psychological defense system. It preempts the lies practitioners tell themselves.

**Research process for anti-rationalization:**
1. For each gotcha from Phase 5, ask: "What rationalization leads to this mistake?"
2. For each rationalization, identify the cognitive bias: optimism bias ("it won't happen to us"), normalcy bias ("this is how everyone does it"), sunk cost ("we've already invested in this approach"), authority bias ("the framework authors know best"), Dunning-Kruger ("we know enough, we don't need experts"), diffusion of responsibility ("security team handles that").
3. For each rationalization, craft the "Why It Feels Right" — the genuine, psychologically valid reason this feels reasonable. This is the hardest column. It must make the reader think "yeah, I've thought that."

**Format (4 columns, non-negotiable):**
| The Temptation | Why It Feels Right | The Devastating Reality | Prevention |
|---|---|---|---|
| "The specific rationalization" | The genuine, valid-feeling reason this is tempting | The concrete, dollar-quantified outcome | The specific counter-action |

**Target:** 6+ entries for standard skills, 8+ for security/critical skills.

**What good looks like for Phase 6:** A practitioner reads the table and feels personally called out by at least 3 entries. The "Why It Feels Right" column makes them uncomfortable because it's exactly what they've told themselves.

### Phase 7: Error Recovery & Verification (~20 min)

**Error Recovery — 5+ scenarios:**
Each scenario must have:
- **Error description:** The exact error message or symptom
- **Root cause:** Why this happens in this domain specifically
- **Step-by-step recovery:** Numbered steps with exact commands
- **Prevention:** How to avoid it next time

**Error scenarios to cover:**
1. Deployment/release failure (most common)
2. Data corruption or loss (most expensive)
3. Security incident response (most urgent)
4. Performance degradation (most insidious)
5. Dependency/third-party failure (most unpredictable)
6. Configuration drift (most preventable)
7. Authentication/authorization failure (most user-impacting)

**Verification Guardrails — 10+ binary checklist items:**
Each item must be:
- Binary: pass/fail, yes/no — no "mostly" or "partially"
- Actionable: the agent can mechanically check it
- Domain-specific: not "tests pass" but "all 12 offline-mode test scenarios pass on a throttled 3G connection"

**Format:**
```
- [ ] **[PREFIX-1]** Specific, binary check that the agent can verify mechanically
- [ ] **[PREFIX-2]** Next check with domain-specific prefix (e.g., MOB, API, SEC, DB)
```

**Target:** 5+ error scenarios, 10+ verification guardrails.

### Phase 8: Scale Depth Matrix (~15 min)

Cover all four scales: Solo → Small → Medium → Enterprise.

**For each scale, answer:**
- **What changes:** Tools, processes, depth of application
- **What to skip:** What's overkill at this scale
- **Transition trigger:** What signals it's time to move to the next scale
- **Coordination model:** Who coordinates with whom at this scale
- **Domain-specific scaling concern:** What breaks at this scale in this specific domain

**Format:** Table with columns: Scale, What Changes, What to Skip, Transition Trigger.

**Cross-skills Integration table:**
| Step | Skill | What it produces |
|---|---|---|
| **Before** | {upstream skills} | {what they produce for this skill} |
| **This** | {this skill} | {what this skill produces} |
| **After** | {downstream skills} | {what they produce from this skill's output} |

### Phase 9: Cross-Skill Integration (~15 min)

**Upstream skills table:**
| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `{skill-name}` | Specific artifact, data, or decision | The trigger condition for involving this skill |

**Downstream skills table:**
| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `{skill-name}` | Specific artifact or decision | What happens if this skill's output is delayed |

**Communication triggers table:**
| Trigger | Notify | Why |
|---|---|---|
| Specific detectable event | Which skill to notify | Why this matters to the downstream skill |

**Escalation path (ASCII tree):**
```
{Specific problem}? → {First escalation target} → {Second escalation target}
```

**Common chains:**
```
- **Chain**: {skill-1} → {skill-2} → {skill-3} — {description of what flows through this chain}
```

### Phase 10: Quality Validation (~15 min)

**Automated checks:**
```bash
bash scripts/validate-skills.sh          # 6/6 governance checks
python3 scripts/skill-router.py --chain {name}  # Chain connectivity verification
```

**Manual checks (run through every item):**
- [ ] All 12+ mandatory sections present and non-empty
- [ ] YAML frontmatter has name, description, category, tier, chain_feeds_into (≥1), chain_consumes_from (≥1)
- [ ] Frontmatter description is one paragraph, triggers-only format
- [ ] At least 3 ASCII decision trees with YES/NO branching
- [ ] At least 6 ground rules, each with concrete violation example
- [ ] At least 10 gotchas with dollar figures ($X,XXX+)
- [ ] Anti-rationalization table has exactly 4 columns and 6+ rows
- [ ] Error Recovery has 5+ scenarios with step-by-step commands
- [ ] Verification Guardrails has 10+ binary [ ] checklist items
- [ ] Cross-Skill tables have upstream AND downstream
- [ ] Scale Depth covers Solo→Small→Medium→Enterprise with transition triggers
- [ ] Production Checklist has 13+ items with domain-specific prefixes
- [ ] No placeholder/TODO/TBD/"[...]" content anywhere
- [ ] File path matches pattern: skills/{category}/{skill-name}/SKILL.md
- [ ] Token budget: 400-700 lines (standard), 600-1000 (security/critical)

**The self-recreation test (ULTIMATE GATE):**
Read the generated skill from top to bottom. Ask: "If I fed this skill to a fresh agent with no other skills loaded, could that agent generate a 10/10* skill for any domain?" If the answer is no, identify which Phase's instructions are incomplete and return to that Phase.

**Output:** A validated, chain-connected, production-quality SKILL.md file ready for agent consumption.

## The Skill Quality Rubric

This is how to grade ANY skill. Use it to audit existing skills and self-assess generated skills.

| Dimension | 6/10 (Adequate) | 8/10 (Good) | 10/10* (World-Class) |
|-----------|----------------|-------------|---------------------|
| **Ground Rules** | Generic rules ("Be careful with auth"), no examples, 3-4 rules | Domain-specific rules, some violation examples, 5-6 rules | Every rule has concrete violation story + mechanical trigger + exact STOP response, 6-10 rules |
| **Gotchas** | "Be careful" warnings, 3-5 entries, no dollar figures | Some dollar figures ($X,XXX+), 6-8 entries, mostly domain-specific | 10+ gotchas with breakout cost calculations from real incidents, every entry has dollar range + specific prevention |
| **Anti-Rationalization** | 2-3 generic entries ("It works on my machine"), 2-column format | 4-5 domain entries, 3-4 columns, some psychological insight | 6+ entries with 4-column format + psychological bias identified, "Why It Feels Right" is uncomfortably accurate |
| **Decision Trees** | Text-only if/else, 1-2 trees, no when-NOT-to-use guidance | Simple ASCII tree, 2 trees, some branching | 3+ multi-level ASCII trees with YES/NO branching + when-NOT-to-use at terminal nodes |
| **Error Recovery** | "Check logs" advice, 1-2 scenarios | 2-3 specific scenarios, some step-by-step commands | 5+ scenarios with exact commands, root cause analysis, escalation triggers, and prevention measures |
| **Verification** | 3-5 generic checks ("tests pass"), no prefix IDs | 7-9 domain checks, some binary, some prefix IDs | 10+ binary checks with domain-specific prefix IDs covering security, performance, accessibility, correctness |
| **Scale Depth** | Mentioned scale levels exist, no depth | Brief per-level guidance, table format | Full Solo→Enterprise matrix with transition triggers, coordination models, and domain-specific scaling concerns |
| **Cross-Skill** | Lists upstream/downstream in frontmatter only | Table with what-receives/provides, some communication triggers | Upstream table + downstream table + communication triggers + escalation path + common chains |
| **Chain Connectivity** | Connected to 1-2 skills, symmetric edges unverified | Connected to 3-4 skills, most edges symmetric | Part of 3+ meaningful chain paths, all edges symmetric, chain YAML entries created |
| **Token Efficiency** | >800 lines (bloated), redundant content, no pruning | 500-700 lines, some sediment | 400-700 lines (rich but dense — no no-op content); security/critical: 600-1000. Every line earns its token cost |

## Domain Mapping Table

Map user requests to skill categories and template references:

| User Says | Category | Template Skill to Model From | Key Sections to Adapt |
|-----------|---------|------------------------------|----------------------|
| "I need a skill for Kubernetes" | 07-devops | docker-kubernetes, devops-engineer | Ground rules (pod security, RBAC), decisions (deployment strategy, ingress design), gotchas (misconfigured resource limits, orphaned PVs) |
| "Create a skill for data analytics" | 09-data | data-engineer, analytics-engineer | Decisions (pipeline architecture, batch vs streaming), gotchas (data quality drift, schema evolution), errors (pipeline backpressure failures) |
| "I need a GraphQL API skill" | 05-development | api-designer, backend-developer | Ground rules (N+1 prevention, query depth limiting), decisions (REST vs GraphQL), gotchas (unbounded queries, missing dataloaders) |
| "Skill for incident response" | 08-security | incident-responder, security-engineer | Ground rules (don't destroy evidence, preserve chain of custody), workflow (triage→contain→eradicate→recover), decisions (isolate vs shut down) |
| "Build skill for healthcare compliance" | 11-legal | gdpr-privacy, compliance-officer, hipaa-technical-implementation | Ground rules (HIPAA-specific: BAAs, PHI de-identification, audit controls), gotchas (PHI exposure in logs, unauthorized access), verification (audit trail completeness, access review cadence) |
| "I need a skill for React/Next.js" | 05-development | frontend-developer | Ground rules (SSR security, hydration mismatches), decisions (SSR vs SSG vs ISR), gotchas (bundle size, layout shift from missing Suspense boundaries) |
| "Create skill for AWS architecture" | 07-devops | cloud-architect, finops-engineer | Ground rules (IAM least privilege, public S3 block), decisions (EC2 vs ECS vs Lambda), gotchas (misconfigured security groups, orphaned elastic IPs) |
| "Skill for mobile security testing" | 08-security | security-reviewer, mobile-developer | Ground rules (certificate pinning, jailbreak detection), decisions (static vs dynamic analysis), gotchas (hardcoded API keys in APK, insecure data storage) |
| "I need a skill for CI/CD pipelines" | 07-devops | ci-cd-builder, devops-engineer | Ground rules (secret management in pipelines, artifact integrity), decisions (GitHub Actions vs GitLab CI vs Jenkins), gotchas (pipeline credential leakage, untested deployment scripts) |
| "Create a skill for API security testing" | 08-security | security-reviewer, api-designer | Ground rules (OWASP API Top 10, rate limiting enforcement), decisions (automated scanning vs manual review), gotchas (broken object-level authorization, excessive data exposure) |
| "Skill for FinOps cost optimization" | 07-devops | finops-engineer, cloud-architect | Ground rules (resource tagging mandate, budget alert thresholds), decisions (reserved vs spot vs on-demand), gotchas (orphaned resources, unmonitored data transfer costs) |
| "I need a skill for game development" | 05-development | game-developer, gameplay-programmer | Ground rules (frame budget awareness, asset pipeline), decisions (Unity vs Unreal vs Godot), gotchas (memory fragmentation, shader compilation stutter) |

**Using the mapping table:** Find the closest match to the user's request. The "Template Skill" column tells you which existing 10/10* skills to reference for structure. The "Key Sections to Adapt" column tells you which sections need the most domain-specific customization. Never copy-paste — template FROM, not copy.

## Gotchas — Skill Creation Footguns

These are the specific, expensive mistakes made when CREATING skills — not general development gotchas.

- **Copy-pasting from a similar skill without domain adaptation → 3+ hours of cleanup to purge domain-specific content that doesn't apply.** A "Kubernetes Developer" skill built by copy-pasting "Docker Developer" retains ground rules about Dockerfile optimization, gotchas about layer caching, and chain connections to container security that have nothing to do with Kubernetes. The agent executes instructions for the wrong domain. **Total cost: $5,000-$15,000 in wasted agent invocations producing wrong-domain output before someone notices the skill is broken.** Fix: Template FROM a similar skill — study its structure, adapt every section to the new domain. Start with a blank file and write each section from scratch, referencing the template only for format.

- **Insufficient domain research → 185-line skeleton that passes validation but produces zero practical value.** A skill with generic ground rules ("Be careful with authentication"), no dollar-quantified gotchas, and decision trees that say "Use the right tool for the job" passes 6/6 governance checks but the agent produces the same output it would without the skill. Users waste time reading a skill that adds nothing. **Total cost: $10,000-$30,000 in lost productivity from teams trusting a hollow skill, plus reputational damage when a generated 10/10* skill produces 6/10 output.** Fix: Invest 60% of skill-building time in domain research. Every ground rule must be testable. Every gotcha must cite a real incident class. Read your skill and ask: "Does this tell the agent anything it couldn't have guessed from its training data?"

- **Orphaned chain connections → skill that no agent can discover through routing.** The skill router depends on chain edges to navigate the skill graph. A skill with `chain_feeds_into: []` sits in the filesystem but never appears in any routing path. The skill exists — the agent never finds it. **Total cost: $15,000-$50,000 in duplicated effort when teams create shadow skills because they don't know the existing one exists, plus chain router blind spots that cause agents to route to less-specific skills.** Fix: After generating a skill, search the repository for related skills. Map at least 2 upstream (what this skill needs) and 2 downstream (who needs this skill) connections. Create chain YAML entries if the repository uses them. Verify with `skill-router.py --chain {name}`.

- **Generic ground rules → agent applies wrong rules to wrong context.** "Be secure" means nothing. The agent defaults to training-data security patterns, which may be wrong for this domain. A "Healthcare API" skill needs "Never log PHI in plaintext — use structured logging with automatic PII redaction." A generic skill says "Don't log sensitive data" — the agent logs patient names and addresses because it doesn't know those count as "sensitive" in this context. **Total cost: $50,000-$500,000 in compliance violations from agent output that followed the letter of the ground rules but violated domain-specific regulations (HIPAA, GDPR, PCI-DSS).** Fix: Every ground rule must be domain-specific and testable. If you can't write a behavioral eval that verifies the rule, it's not specific enough.

- **Missing anti-rationalization table → agent falls for cognitive biases the table would have prevented.** The anti-rationalization table is the agent's psychological defense. A skill without it is like a seatbeltless car — fine until the first crash. The agent encounters a situation where the "easy wrong path" feels right, and without the anti-rationalization preemption, it takes it. **Total cost: $20,000-$100,000 in production incidents from agent decisions that "felt right" at the time — missing data backups, skipping security reviews, deferring technical debt.** Fix: Spend 20+ minutes on the anti-rationalization table. For each entry, identify the psychological bias. Test: does the "Why It Feels Right" column make you uncomfortable because you've had that exact thought?

- **Token budget ignored → 2,500-line skill that consumes 40% of the agent's context window.** The agent loads the entire skill at invocation time. A bloated skill leaves insufficient context for the actual task. The agent skips sections, misses ground rules, and produces incomplete output. **Total cost: $5,000-$20,000 per quarter in degraded agent performance — tasks fail or produce incomplete output because the skill consumed too much context budget.** Fix: Target 400-700 lines for standard skills, 600-1000 for security/critical. Run the no-op test: does removing this sentence change default agent behavior? If no, delete. Move reference material to `references/` directory.

- **Skipping verification guardrails → agent never knows when the task is complete.** Without a production checklist, the agent has no "done" signal. It either stops too early (incomplete output) or continues generating indefinitely (wasted tokens on unnecessary refinement). **Total cost: $10,000-$40,000 in agent runtime waste — 30% of invocations either under-produce or over-produce because there's no completion criteria.** Fix: Include 13+ binary checklist items in the Production Checklist. Each item must be a yes/no question the agent can mechanically verify. Use domain-specific prefix IDs (e.g., S1-S14, API1-API14).

- **Neglecting the self-recreation test → skill that can't bootstrap.** A dynamic-skill-creator that can't recreate itself is a contradiction. If the instructions aren't concrete enough to regenerate this very skill, they're not concrete enough to generate any skill reliably. **Total cost: The entire skill ecosystem degrades because the generator skill itself is the weakest link — every generated skill inherits the generator's blind spots.** Fix: After generating any skill, run the self-recreation test: read the skill's Phase 0-9 workflow and ask "Could a fresh agent follow these instructions to recreate this skill?" If any Phase says "research the domain" without specifying HOW, the workflow is incomplete.

- **Using 2-column anti-rationalization instead of 4-column → psychological defense gap.** A 2-column format ("Rationalization | Reality") is better than nothing but misses the crucial columns: "Why It Feels Right" (the empathy column that makes agents recognize their own biases) and "Prevention" (the action column that tells agents what to do instead). **Total cost: $5,000-$15,000 in agent rationalization failures because the table doesn't address the psychological root of the rationalization.** Fix: Always use 4 columns: The Temptation | Why It Feels Right | The Devastating Reality | Prevention. The "Why It Feels Right" column is what makes the rationalization recognizable.

- **Generating a skill for a domain where pricing/features change rapidly without flagging it.** Cloud services, SaaS tools, and API platforms change pricing and features monthly. A skill generated today with specific pricing advice ("use AWS t3.medium at $0.0416/hr") is wrong in 6 months. **Total cost: $2,000-$10,000 in wasted implementation time when teams build against outdated pricing models or deprecated API features.** Fix: In the skill's frontmatter description, add: "⚠️ Pricing and feature details reflect [date]. Verify current pricing before implementation." Flag pricing-sensitive gotchas with verification dates.

## Error Recovery — Skill Creation Failures

- **Generated skill fails `validate-skills.sh`:** Run `bash scripts/validate-skills.sh --verbose` to get detailed failure output. Fix failures in order: (1) frontmatter YAML syntax errors first (these cascade), (2) missing required fields (name, description, type, status, version, chain), (3) section presence (check all mandatory sections exist), (4) chain symmetry (consumes_from and feeds_into edges must be symmetric across the repository). Re-validate after each fix batch. If the script doesn't exist in this environment, run manual validation using the Verification Guardrails checklist instead.

- **Generated skill has no chain connections:** Search the repository for related skills using `grep -rl "name:.*{keyword}" skills/` to find skills with similar names, tags, or domains. Identify natural upstream skills (what this skill needs to receive) and natural downstream skills (who needs this skill's output). If this is a genuinely new domain with no obvious connections, connect to infrastructure skills (ci-cd-builder, devops-engineer) and quality skills (code-reviewer, qa-engineer) as default upstream/downstream. Never leave chain fields empty.

- **Gotchas are too generic — no dollar figures or real incidents:** Restart Phase 5 from scratch. Search `"[domain] breach cost"` on Google, search CVE database at nvd.nist.gov for domain-specific vulnerabilities, search "site:news.ycombinator.com [domain] outage" for post-mortems. For each result, extract: what went wrong, the reported dollar cost, and the prevention measure. If no dollar cost is reported, calculate: estimated downtime hours × industry revenue rate + remediation hours × $150/hr. Replace generic warnings with incident-backed gotchas.

- **Generated skill is too short (<300 lines):** Insufficient discovery. Return to Phase 0 and answer all 8 discovery questions in writing (not mentally). Each answer should generate 50+ lines of content when expanded into its respective section. Common culprit: questions 7 (expensive mistakes) and 8 (rationalizations) were answered superficially. Re-research: spend 15+ minutes per question searching for real incidents and cognitive biases.

- **Anti-rationalization entries feel weak or generic:** For each rationalization, ask "what psychological bias drives this?" (optimism bias, normalcy bias, sunk cost fallacy, authority bias, Dunning-Kruger effect, diffusion of responsibility, status quo bias, hyperbolic discounting). Map the bias to the domain. "We're too small to be a target" → optimism bias + normalcy bias. "The framework handles security" → diffusion of responsibility + authority bias. Rewrite the "Why It Feels Right" column to evoke recognition: "because security is someone else's problem, and the framework authors are smarter than you" — honest, uncomfortable, and psychologically accurate.

- **Decision trees render incorrectly in raw markdown:** Verify ASCII characters are using the correct Unicode code points. Box-drawing characters: `┌` (U+250C), `┐` (U+2510), `└` (U+2514), `┘` (U+2518), `├` (U+251C), `┤` (U+2524), `│` (U+2502), `─` (U+2500). Common failure: using `|` (pipe character U+007C) instead of `│` (box drawing U+2502). Test by viewing the raw markdown file — if any box-drawing characters appear as `?` or empty boxes, the terminal encoding is wrong. Fall back to `+`, `-`, `|` characters if Unicode box-drawing isn't available.

- **Token budget exceeded (>700 lines standard, >1000 security):** Run the pruning protocol: (1) Check for duplication — `grep -c "[sentence]" SKILL.md` for sentences >15 words that appear multiple times. Consolidate to one occurrence. (2) Check for sediment — `grep "is a\|refers to\|means\|defined as" SKILL.md` to find definitional content in procedural sections. Move to references/. (3) Run the no-op test on every sentence: if removing it changes nothing about agent behavior, delete it. (4) Merge similar ground rules — two rules about authentication can often be one rule with a broader mechanical trigger. Target: <700 lines for standard, <1000 for security/critical.

## Verification Guardrails

Run these checks on every generated skill before declaring it complete. ALL must pass.

- [ ] **[GEN1]** All 12 mandatory sections present with non-empty content — no section has fewer than 3 lines of substantive content
- [ ] **[GEN2]** YAML frontmatter validates — `name`, `description`, `type`, `status`, `version`, `updated`, `chain` (with `consumes_from` ≥1 and `feeds_into` ≥1) all present and parseable
- [ ] **[GEN3]** Frontmatter description is triggers-only — one paragraph, no line breaks, format: "Use when [triggers]. Handles [capabilities]. Do NOT use for [boundaries]."
- [ ] **[GEN4]** At least 3 ASCII decision trees present, each with YES/NO branching at 2+ levels, terminal nodes with "when to use" and "when NOT to use" guidance
- [ ] **[GEN5]** At least 6 ground rules, each with: negative constraint, mechanical trigger, violation response — and every rule is domain-specific (could not be copied to a different skill)
- [ ] **[GEN6]** At least 10 gotchas with dollar figures ($X,XXX+) from real incident classes — grep for `$[0-9]` returns 20+ matches (10 minimum × 2 mentions each)
- [ ] **[GEN7]** Anti-rationalization table has exactly 4 columns (The Temptation | Why It Feels Right | Devastating Reality | Prevention) and 6+ rows — psychological bias identified in at least 3 entries
- [ ] **[GEN8]** Error Recovery has 5+ scenarios, each with: error description, root cause, step-by-step recovery, and prevention — every step is a concrete command, not advice
- [ ] **[GEN9]** Verification Guardrails (this section) has 10+ binary `[ ]` checklist items with domain-specific prefix IDs
- [ ] **[GEN10]** Cross-Skill tables include upstream (what receives) AND downstream (what provides) — both tables have at least 3 rows each
- [ ] **[GEN11]** Scale Depth covers Solo→Small→Medium→Enterprise — each level has what-changes, what-to-skip, and transition-trigger columns
- [ ] **[GEN12]** Production Checklist has 13+ items with domain-specific prefix IDs (e.g., S1-S17, not generic numbers)
- [ ] **[GEN13]** No placeholder content — `grep "TODO\|TBD\|\[Coming soon\]\|\.\.\." SKILL.md` returns zero matches
- [ ] **[GEN14]** File path matches `skills/{category}/{skill-name}/SKILL.md` — directory name is kebab-case, matches frontmatter `name` field
- [ ] **[GEN15]** Token budget: standard skill 400-700 lines, security/critical 600-1000 lines — `wc -l SKILL.md` within target range
- [ ] **[GEN16]** Self-recreation test passes — reading the skill's workflow produces enough concrete instructions to regenerate itself
- [ ] **[GEN17]** Every dollar figure in gotchas is verifiable against at least one real-world incident — source traceable to CVE, post-mortem, or industry report

## Cross-Skill Coordination

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `writing-great-skills` | Skill authoring vocabulary, failure modes (premature completion, duplication, sediment, sprawl), pruning methodology, anti-rationalization design, progressive disclosure architecture | When generating a new skill — ensures the generated skill follows repository-wide quality patterns and avoids known failure modes |
| `code-reviewer` | Quality standards framework, anti-pattern catalogs for the target domain, severity grading methodology | When the generated skill needs domain-specific ground rules and gotchas — code reviewer provides the "what goes wrong in production" research |
| `technical-writer` | Documentation standards, clarity principles, information hierarchy design | When the generated skill needs clear, unambiguous language in its description and workflow sections |
| `system-architect` | Domain architecture patterns, ADR templates, technology decision frameworks | When the generated skill covers an architecture-heavy domain — provides the decision tree content and trade-off analysis |
| `product-strategist` | Domain analysis methodology, user persona frameworks, competitive landscape research | When the generated skill targets a product-oriented domain — provides the discovery and requirements analysis framework |
| `qa-engineer` | Test strategy patterns, verification methodology, behavioral eval design | When designing the verification guardrails and error recovery scenarios for the generated skill |
| `security-reviewer` | Security threat models, CVE research methodology, vulnerability classification frameworks | When the generated skill covers a security or compliance domain — provides the security-specific ground rules and gotcha research |
| `documentation-engineer` | Skill reference file structure, external link management, document generation pipelines | When the generated skill needs reference files, templates, or external documentation links |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `writing-great-skills` | Complete, validated SKILL.md files that embody the repository's quality standards — serves as exemplar for skill authoring education | Skill authors lack reference examples of 10/10* quality — quality drift accelerates across the repository |
| `agent-eval-pipeline` | Domain-specific behavioral eval scenarios embedded in the generated skill's verification guardrails | Eval pipeline can't test domain-specific behavior — agents operate without domain-appropriate quality gates |
| `cross-agent-skills-packaging` | Normalized, chain-connected skill files ready for cross-agent deployment and manifest generation | Packaging pipeline can't process skills that lack standard structure — cross-agent compatibility breaks |
| (any specialized skill) | Complete, validated skill file for the target domain — ready for agent consumption and chain routing | Teams lack domain-specific guidance — agents default to training-data patterns which may be wrong for the domain |

### Communication Triggers

| Trigger | Notify | Why |
|---|---|---|
| Generated skill introduces a new category directory | System Architect, Documentation Engineer | New categories affect repository organization and navigation — must align with existing taxonomy |
| Generated skill's chain connections create asymmetry in the graph | All affected skill maintainers | Chain asymmetry causes routing failures — agents can't navigate the skill graph correctly |
| Generated skill fails the self-recreation test | Writing Great Skills | The meta-skill itself may have gaps — if it can't recreate itself, it can't reliably generate other skills |
| Generated skill references a template skill that has been deprecated | Code Reviewer, Qa Engineer | Deprecated templates may encode outdated patterns — ensure generated skill uses current best practices |
| Multiple generated skills for the same domain detected | Product Strategist | Duplicate skills create routing ambiguity — consolidate or differentiate with clear boundary descriptions |

### Escalation Path

```
Skill fails validation? → Run verbose checks → Fix in order (frontmatter → sections → chain) → Re-validate
Chain asymmetry detected? → Identify direction of asymmetry → Fix consuming skill's feeds_into OR producing skill's consumes_from → Re-validate symmetry
Generated skill is hollow (passes validation but lacks substance)? → Return to Phase 0 → Re-research domain → Rebuild from ground rules up
Self-recreation test fails? → Escalate to writing-great-skills → Audit the dynamic-skill-creator's own Phases for gaps → Update this skill
Domain mapping table missing entry for common domain? → Add entry → Verify template reference is still a 10/10* skill → Submit as improvement to this skill
```

## Operating at Different Levels

| Scale | Team | What Changes | What to Skip | Transition Trigger |
|-------|------|-------------|-------------|-------------------|
| **Solo** | 1 | Quick MVS generation. 5 ground rules, 5 gotchas, 4 anti-rationalization entries. 300-400 lines. Research time: 30-45 min. Generate from the Minimal Viable Skill template. | Skip full 12-section build. Skip reference files. Skip behavioral eval creation. Skip chain YAML files (frontmatter chain connections only). | When a second person needs to use the skill — MVS lacks the depth for multi-user consumption |
| **Small** | 2-10 | Full 12-section skill. 8 ground rules, 8 gotchas, 6 anti-rationalization entries. 500-600 lines. Research time: 2-3 hours. Complete chain connections with symmetry verification. | Skip behavioral eval scenarios (use verification guardrails only). Skip cross-agent packaging. Skip drift monitoring. Skip external reference files (link to web resources instead). | When the skill is used by 3+ different agent types (Claude Code, Copilot, Cursor) — need cross-agent compatibility |
| **Medium** | 10-50 | Full skill + behavioral eval scenarios + reference files. 9-10 ground rules, 10+ gotchas, 7-8 anti-rationalization entries. 700-900 lines. Research time: 4-6 hours. Complete chain YAML, reference file creation, eval scenario design. | Skip drift monitoring automation. Skip cross-agent manifest generation (do manual packaging). Skip comprehensive domain research archive (keep gotcha sources in comments). | When the skill is part of a CI/CD pipeline — needs automated validation and behavioral evals |
| **Enterprise** | 50+ | Full skill + references + evals + chain orchestration + drift monitoring tests + cross-agent packaging + domain research archive. 10 ground rules, 15+ gotchas, 8+ anti-rationalization entries. 900-1200 lines. Research time: 8-12 hours. All reference files created, eval pipeline integrated, chain YAML validated, monitoring dashboards configured. | Nothing — at enterprise scale, all depth is justified. Even drift monitoring pays for itself in preventing quality decay across hundreds of agent invocations. | When the skill is mission-critical — incorrect output has regulatory, financial, or safety consequences |

### Cross-Skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | writing-great-skills | Skill authoring methodology, failure mode catalog, pruning techniques, quality dimensions |
| **Before** | code-reviewer, security-reviewer, qa-engineer | Domain-specific anti-patterns, CVE research, test strategy patterns for the target domain |
| **This** | dynamic-skill-creator | Complete, validated, chain-ready SKILL.md at 10/10* quality for the target domain |
| **After** | agent-eval-pipeline | Behavioral eval execution against the generated skill's ground rules and verification guardrails |
| **After** | cross-agent-skills-packaging | Normalized, manifest-ready skill package deployed across all agent platforms |

Common chains:
- **Discovery to deployment**: writing-great-skills → dynamic-skill-creator → cross-agent-skills-packaging — Define quality standards, generate domain-specific skill, package for multi-agent deployment
- **Security domain pipeline**: security-reviewer → dynamic-skill-creator → agent-eval-pipeline → security-reviewer — Security reviewer provides threat models, skill creator builds security skill, eval pipeline verifies security behavior, security reviewer validates output
- **Domain expansion**: product-strategist → dynamic-skill-creator → (new domain skill) — Product strategist identifies new domain, skill creator generates skill, new skill integrates into chain graph

## Proactive Triggers

Surface these without being asked during skill generation:

| Trigger | Immediate Action | Rationale |
|---|---|---|
| User says "I need a skill for [domain]" without specifying scope | Ask Phase 0 discovery questions before generating ANY content. Do not assume scope. "Finance app" could mean personal finance tracking, algorithmic trading, or enterprise banking compliance — three completely different skills. 🔴 | Incorrect scope assumption wastes 2+ hours of generation time on the wrong skill. A skill for the wrong scope is worse than no skill — it actively misleads |
| User mentions a domain where pricing/features change rapidly (cloud services, SaaS tools, API platforms) | Flag in the generated skill's frontmatter description: "⚠️ Pricing and feature details reflect [date]. Verify current pricing before implementation." Add a gotcha about outdated pricing advice. 🟡 | Pricing-specific advice ages in months. A skill recommending AWS t3.medium at $0.0416/hr is wrong when pricing changes — agents make cost decisions based on stale data |
| User says "just make it quick, I don't need full quality" | Offer the MVS path but warn: "An MVS skill is 10/10 quality in its sections but domain-light — fewer gotchas, fewer ground rules. For security, compliance, or critical infrastructure domains, MVS is dangerous. I recommend full quality." 🟠 | Pressure to ship fast is the #1 cause of hollow skills. An MVS for a security domain is a ticking time bomb — it gives false confidence without the defensive depth |
| User provides a domain but can't answer Phase 0 discovery questions | Pause generation. "I need domain-specific input to build a quality skill. Without knowing the top 3 expensive mistakes in this domain, the gotchas section will be generic. Can you connect me with a domain expert or provide incident reports?" 🔴 | Generating a skill without domain input produces a hollow shell. The agent can synthesize structure but not domain wisdom — that must come from research or expert input |
| Generated skill's gotchas only cite generic costs ("$10K-$50K") without source references | Re-research: for each gotcha, find at least one real incident. If no specific incident exists for the dollar range, calculate: downtime_hours × revenue_rate + remediation_hours × $150/hr. Replace generic ranges with calculated specifics. 🟡 | Generic dollar figures feel made up. Incident-backed figures are persuasive and accurate. The difference is $10K-$50K (generic) vs $10K-$50K in lost installs from negative reviews — a 0.5-star rating drop can reduce install conversion by 30% (App Store data)" (specific) |
| User asks to generate a skill that's a minor variant of an existing skill | Redirect: "This domain appears to be a specialization of [existing skill]. Consider creating a sub-skill in the existing skill's references/ directory instead of a standalone skill. This preserves chain connections and avoids graph fragmentation." 🟡 | Minor variant skills fragment the chain graph and confuse routing. Sub-skills provide specialization without duplication |
| Generated skill passes all validation but the user reports "the agent still gives bad advice" | Run the behavioral eval: design 3 test scenarios for the generated skill's ground rules. Test whether the agent actually follows the rules or defaults to training-data patterns. The gap is usually: ground rules are correctly written but the agent's training data overrides them for common patterns. 🟠 | Validation measures structure, not behavioral compliance. A perfectly formatted skill can still produce wrong output if ground rules aren't specific enough to override training defaults |

## Best Practices

1. **Research before you write.** 60% of skill-building time should be domain research. The best skills cite real incidents, real CVEs, and real post-mortems. A skill written from memory alone is a confident summary of one person's experience — a skill written from research encodes the collective wisdom of the industry.

2. **Every ground rule must be testable.** If you can't write a behavioral eval for it, it's not a ground rule. "Be careful with authentication" fails — what does the agent DO differently? "Never store JWT in localStorage — use httpOnly cookies with SameSite=Strict" passes — the agent can mechanically verify client-side storage mechanisms.

3. **Gotchas need dollar figures from real incidents.** Search for breach costs (IBM annual report), downtime calculations (hourly revenue × outage hours), and migration horror stories (developer time × hourly rate). A gotcha without a dollar amount is a platitude. The dollar figure is what convinces the agent to prioritize prevention.

4. **Decision trees must have "when NOT to use" branches.** The most valuable part of a decision tree is knowing when to say NO. "Use microservices" is easy. "Use microservices when team > 20 AND independent deploy cycles needed. Do NOT use when team < 8 OR tight coupling exists between services" is expert.

5. **Chain connections are not optional.** Orphaned skills are undiscoverable. Every skill connects to at least 2 upstream and 2 downstream skills. The chain router depends on these edges — an unconnected skill exists in isolation. Search the repository before declaring chain connections empty.

6. **Anti-rationalization is psychological defense.** Understand the cognitive bias behind each rationalization. "We're too small to be a target" = optimism bias + normalcy bias. "The framework handles security" = diffusion of responsibility + authority bias toward framework authors. The "Why It Feels Right" column must evoke uncomfortable recognition.

7. **Production checklists are the agent's "done" signal.** Without a checklist, the agent doesn't know when to stop generating output. Every checklist item must be binary (yes/no) and mechanically verifiable. Use domain-specific prefix IDs for traceability across skills.

8. **Validate after EVERY generation.** Run `validate-skills.sh` (or manual verification) before declaring a skill complete. Validation measures structure; manual review measures substance. Both are required. A skill that passes validation but fails manual review is not done.

9. **Token budget discipline.** Every line must earn its cost. If you can say it in 1 line instead of 3, do it. Move reference material to `references/` directory. Run the no-op test: does removing this sentence change default agent behavior? If no, delete. The compiler will minify further — start lean.

10. **This skill must be able to recreate itself.** The ultimate test: can dynamic-skill-creator generate a new dynamic-skill-creator that passes all quality checks? If the answer is no, fix this skill. If the answer is yes, every other skill generation is a solved problem. This is the bootstrap invariant that guarantees quality across the entire repository.

11. **Default to the repository standard when uncertain.** When in doubt about format, section ordering, table structure, or heading conventions, reference existing 10/10* skills — mobile-developer, backend-developer, code-reviewer, security-reviewer, writing-great-skills. Their formats are battle-tested across thousands of agent invocations. Novelty in format is a bug, not a feature.

12. **Admit what you cannot know.** If generating a skill for a domain where pricing, features, or APIs change rapidly (cloud services, SaaS tools, third-party APIs), flag it in the frontmatter and add a gotcha about verification. The agent should NOT trust pricing-specific advice older than 6 months without re-verification.

## Deliberate Practice
<!-- QUICK: 30s -- exercises to build skill-creation mastery -->

| Exercise | Skill Targeted | Success Criteria | Time Investment |
|----------|---------------|------------------|-----------------|
| **Recreate an existing 10/10 skill from memory** | Section mastery, domain knowledge encoding | Generated skill passes 6/6 validation and matches original on gotcha count (±1), ground rules count (±1), and decision tree depth (±1 level) | 3-5 hours |
| **Generate a skill for a domain you know nothing about** | Domain research protocol, requirement extraction | Skill passes 6/6 validation; domain expert review finds no factual errors in gotchas; anti-rationalization table names at least 3 domain-specific cognitive biases correctly | 4-8 hours |
| **Audit a skill and identify all quality gaps** | Quality rubric application, forensic review | Find 100% of missing mandatory sections, 90%+ of gotchas that need dollar quantification, and all broken reference links | 1-2 hours |
| **Upgrade a 6/10 skill to 10/10** | Gap-to-excellence mapping, gotcha research | Original skill passes ≤ 3/6 checks; upgraded skill passes 6/6; gotcha count increases by 5+ with dollar figures; anti-rationalization table added or expanded 3+ rows | 2-4 hours |
| **Generate a skill in under 2 hours (MVS mode)** | Speed, prioritization, template fluency | MVS passes validation on all present sections; includes at least 3 gotchas with dollar figures, 4 ground rules, 2 decision trees, and complete frontmatter | 2 hours |
| **Create a skill that references 3+ related skills correctly** | Chain architecture, cross-skill coordination | consumes_from and feeds_into entries are symmetric; communication triggers reference the correct skill names; escalation path is consistent with existing chain graph | 1-2 hours |


## State Log

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.

### How the State Log Works
<!-- AGENT: Read this before starting work, update after each phase -->

1. **On session start:** Check `.copilot/session-state/decision-ledger.json` for any prior decisions relevant to this domain. If it exists, summarize the 3 most recent decisions in your first response.
2. **After each major decision:** Append to the ledger:
   ```json
   {
     "timestamp": "ISO-8601",
     "skill": "dynamic-skill-creator",
     "phase": "Phase 3: Implementation",
     "decision": "What was decided",
     "rationale": "Why this choice over alternatives",
     "constraints": ["constraint-1", "constraint-2"],
     "alternatives_considered": ["alt-1", "alt-2"],
     "reversible": true
   }
   ```
3. **Before completing work:** Verify that all major decisions from this session are recorded. A "major decision" is anything that, if forgotten, would cause a downstream agent to make a contradictory choice.
4. **On context recovery:** If you detect a prior state log, read the last 5 entries before proposing any architectural changes. Cite the prior decisions you're building on.

### State Log Schema

| Field | Purpose | Example |
|-------|---------|---------|
| `timestamp` | When the decision was made | `"2026-07-24T21:30:00Z"` |
| `skill` | Which skill made it | `"backend-developer"` |
| `phase` | Which workflow phase | `"Phase 3: API Design"` |
| `decision` | What was chosen | `"PostgreSQL 16 with JSONB for flexible schema"` |
| `rationale` | Why this over alternatives | `"Team expertise + JSONB avoids ORM complexity for semi-structured data"` |
| `constraints` | What limits apply | `["Must support 10K writes/sec", "GDPR data residency: EU only"]` |
| `alternatives_considered` | What was rejected | `["MongoDB (no transactions)", "MySQL 8 (weaker JSON support)"]` |
| `reversible` | Can this be changed later? | `true` (migration possible) or `false` (irreversible choice) |

### Anti-Drift Check
<!-- AGENT: Run this check at the start of each new phase -->

Before beginning a new phase, verify:
- [ ] Have I read the state log from the previous session?
- [ ] Do any prior decisions constrain what I'm about to do?
- [ ] Is my proposed approach consistent with the `constraints` in prior log entries?
- [ ] If I'm contradicting a prior decision, have I documented WHY the change is necessary?

## Production Checklist

- [ ] **[S1]** Skill name is kebab-case, unique across the repository, and descriptive of the domain
- [ ] **[S2]** Category directory exists or is created — matches one of the established category directories in `skills/`
- [ ] **[S3]** YAML frontmatter passes YAML validation — no invalid escapes, unclosed quotes, or formatting errors
- [ ] **[S4]** All 12 mandatory sections present with non-empty content — Route the Request, Ground Rules, Expert's Mindset, When to Use, Decision Trees, Core Workflow, Gotchas, Anti-Rationalization, Error Recovery, Verification Guardrails, Cross-Skill Coordination, Scale Depth
- [ ] **[S5]** Ground rules: 6+ domain-specific rules, each with negative constraint, mechanical trigger, and violation response — no rule could be copied to a different domain
- [ ] **[S6]** Decision trees: 3+ ASCII trees with YES/NO branching at 2+ levels, terminal nodes include when-to-use AND when-NOT-to-use guidance
- [ ] **[S7]** Gotchas: 10+ with dollar figures ($X,XXX+) sourced from real incident classes — every gotcha has a specific, calculable cost impact
- [ ] **[S8]** Anti-rationalization: 6+ entries with exactly 4 columns (The Temptation | Why It Feels Right | Devastating Reality | Prevention) — at least 3 entries identify the psychological bias
- [ ] **[S9]** Error Recovery: 5+ scenarios with step-by-step commands — error description, root cause, recovery steps, and prevention for each
- [ ] **[S10]** Verification Guardrails: 10+ binary `[ ]` checklist items with domain-specific prefix IDs (not generic numbers)
- [ ] **[S11]** Cross-Skill Coordination: upstream table (3+ rows) and downstream table (3+ rows) filled, communication triggers defined (5+), escalation path clear with ASCII tree
- [ ] **[S12]** Chain connectivity: at least 1 consumes_from + 1 feeds_into in frontmatter, chain YAML entries created and validated for symmetry
- [ ] **[S13]** No placeholder/TODO/TBD content — `grep "TODO\|TBD\|\[Coming soon\]\|\.\.\." SKILL.md` returns zero matches
- [ ] **[S14]** Token budget: 400-700 lines for standard skills, 600-1000 for security/critical infrastructure skills
- [ ] **[S15]** File size: 15-30KB for standard skills, 25-50KB for security/critical skills — dense, substantive, no filler
- [ ] **[S16]** Validation passes: `scripts/validate-skills.sh` returns 6/6 PASS (or manual equivalent if script unavailable)
- [ ] **[S17]** Behavioral evals: at least 3 test scenarios designed for the skill's ground rules — each scenario tests one specific ground rule violation
- [ ] **[S18]** Self-recreation test: reading this skill's Phase 0-9 workflow would enable a fresh agent to recreate this skill at 10/10* quality
- [ ] **[S19]** Proactive triggers: 5-8 triggers defined with severity indicators (🔴🟡🟠) — surface domain-specific issues without being asked
- [ ] **[S20]** Every gotcha's dollar figure is traceable to at least one real-world source — CVE, post-mortem, industry report, or calculated from published metrics

## What Good Looks Like

> The generated skill is indistinguishable from a hand-crafted 10/10* skill. Every section is domain-specific — ground rules cite real CVEs, gotchas reference actual post-mortems with specific dollar costs, decision trees encode years of practitioner experience in choosing the right approach. The anti-rationalization table reflects deep psychological understanding of developer cognitive biases — the "Why It Feels Right" column makes domain experts uncomfortable because it's exactly what they've told themselves. Chain connections are complete and symmetric, validation passes 6/6, and the skill integrates seamlessly into the 188+ skill ecosystem. A domain expert reading the skill would say "yes, this captures exactly what goes wrong and how to prevent it." The ultimate confirmation: the skill's own workflow is concrete enough that a fresh agent could follow it to recreate the skill itself — the bootstrap invariant holds, guaranteeing quality across every future generation.

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

## Anti-Rationalization — No Excuses
| Rationalization | Reality |
|---|---:|
| "{domain rationalization 1}" | {harsh reality with dollar figure} |
| "{domain rationalization 2}" | {harsh reality} |
| "{domain rationalization 3}" | {harsh reality} |
| "{domain rationalization 4}" | {harsh reality} |

## Route the Request
[Auto-Route table + Intent Route ASCII tree — mandatory, even in MVS]

## Ground Rules
[5-6 rules with mechanical triggers and violation responses — mandatory]

## When to Use
[5+ bullet list of trigger conditions]

## Decision Trees
[2+ ASCII trees with YES/NO branching]

## Core Workflow
[Phase 0-5 minimum — can skip Phases 6-9 for MVS]

## Gotchas
[5+ with dollar figures — mandatory]

## Error Recovery
[3+ scenarios with step-by-step commands — mandatory]

## Verification Guardrails
[8+ binary checkbox items — mandatory]

## Cross-Skill Coordination
[Upstream/Downstream tables — mandatory, at least 2 rows each]

## Production Checklist
[10+ items with prefix IDs — mandatory]

## What Good Looks Like
[Paragraph describing ideal outcome]

## References
[Links to deeper reference files and external resources]
```

**When to use MVS:** User needs a skill in under 2 hours, domain is non-critical (not security, compliance, healthcare, finance), and the skill will be enhanced to full 10/10* within 2 weeks.
**When NOT to use MVS:** Security, compliance, healthcare, financial, or critical infrastructure domains. These demand full gotcha depth from day one — an incomplete security skill is worse than no skill.

## Cross-Agent Packaging

Generated skills must work across all major AI agent platforms. Add this section to the generated skill's frontmatter:

```yaml
# Cross-Agent Compatibility (append to generated skill frontmatter)
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
```

**Per-agent considerations:**
- **Claude Code:** Requires `PROCESS_TREE.md` in skill directory for advanced routing. Generate this if the skill uses complex multi-phase workflows.
- **Copilot CLI:** Validates frontmatter strictly — ensure no vendor-specific fields leak into the shared format.
- **Cursor:** Integrates with `.cursorrules` — if the skill has domain-specific linting rules, generate a `.cursorrules` snippet.
- **Gemini CLI:** Uses Google-style directives — if the skill has security constraints, format them as "Safety: [constraint]" prefixes.
- **OpenClaw/Codex:** Follow the `~/.agents/skills/` emerging standard with symlink-based sharing.

For full cross-agent deployment, invoke `cross-agent-skills-packaging` after skill generation. The generated skill's frontmatter and structure are already compatible — packaging handles directory setup, manifest generation, and per-agent normalization.

## References

- **Skill Template — Annotated**: Full annotated template with section-by-section guidance for every mandatory section. Shows exactly what each section must contain with inline examples. Study existing 10/10* skills: `skills/05-development/mobile-developer/SKILL.md`, `skills/05-development/backend-developer/SKILL.md`.
- **Quality Rubric — Detailed**: 10-dimension quality scoring guide with specific examples of 6/10, 8/10, and 10/10* for each dimension. See `SKILL-QUALITY-STANDARDS.md` in repository root.
- **Domain Research Protocol**: Step-by-step research methodology for any domain: CVE database search, Hacker News post-mortem mining, Stack Overflow war story collection, industry report extraction. Use web search + CVE databases + GitHub issues for gotcha discovery.
- **Gotcha Research Guide**: Finding real-world dollar-quantified incidents: breach cost databases, downtime calculators, migration cost estimation formulas, and source citation format.
- **Chain Architecture Guide**: How to connect new skills to the 821+ edge graph: finding natural upstream/downstream relationships, creating chain YAML entries, verifying symmetry, and handling new domain introduction. See `scripts/skill-router.py` for live chain verification.
- **Writing Great Skills**: See `skills/00-framework/writing-great-skills/SKILL.md` — The foundational meta-skill for skill authoring. Covers vocabulary, failure modes, pruning, and progressive disclosure architecture.
- **Skill Quality Standards**: See `SKILL-QUALITY-STANDARDS.md` — Repository-wide quality standards document. Defines the 10/10 quality bar, the 30-second test, the footgun test, the handoff test, and the checklist test.
- **Scale Depth Framework**: See `SCALE-DEPTH-FRAMEWORK.md` — Universal framework for Solo→Small→Medium→Enterprise depth levels used across all skills.
- **Coordination Matrix**: See `COORDINATION-MATRIX.md` — Auto-generated matrix of all chain connections across 188+ skills, organized by project phase.
- **Validation Scripts**: `scripts/validate-skills.sh`, `scripts/skill-router.py`, `scripts/behavioral-evals.py` — Automated governance checks, routing verification, and behavioral testing.
- **Template Skills (10/10* reference)**: `skills/05-development/mobile-developer/SKILL.md`, `skills/05-development/backend-developer/SKILL.md`, `skills/06-quality/code-reviewer/SKILL.md`, `skills/06-quality/security-reviewer/SKILL.md` — Battle-tested skill structures.
