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



## The Mental Model Shift
* **The agent is your apprentice, not your peer.** It has encyclopedic general knowledge but zero domain-specific judgment. Your job is to provide the judgment framework — the "when NOT to do X" that general knowledge lacks. The most valuable sentence in any skill is "Do NOT use [approach] when [condition]."
* **Research reveals what expertise conceals.** You know your domain so well that you've forgotten what's hard about it. Research CVEs, post-mortems, and Stack Overflow questions to rediscover the pain points. The gotchas that make you say "oh right, that got me too in 2018" are the ones that matter.
* **Structure is the message.** Agents pattern-match against structure before they process content. A well-structured decision tree communicates more in 30 lines than 300 lines of prose explanation. Tables beat paragraphs. ASCII trees beat tables. Ground rules as mechanical triggers beat prose admonitions.
* **The bootstrap test is the ultimate quality gate.** Ask: "If I fed this skill to a fresh agent with no other skills loaded, could that agent generate a 10/10* skill for any domain?" If the answer is no, you have gaps. This is why the Phase 0 discovery questions, the domain mapping table, the quality rubric, and the gotcha research guide must be complete.



## Cognitive Biases That Corrupt Skill Creation
| Bias | How It Manifests | Antidote |
|-------|------------------|----------|
| **Curse of knowledge** | Skipping fundamental gotchas because "everyone knows that" — writing for experts, not for the agent who has no context | Research what beginners ask on Stack Overflow. The most-upvoted questions are what your skill needs to cover. |
| **Overconfidence bias** | Assuming you can write a 10/10* skill in 2 hours without research — "I've been doing this for 15 years" | Time-box research: 60% of skill-building time on domain research (CVEs, post-mortems, incident reports), 40% on structuring. |
| **Completion bias** | Satisfied when validation passes — "6/6 checks, ship it!" — ignoring that validation measures structure, not substance | Manual review after validation: read every gotcha aloud, verify every dollar figure against a real source, trace every decision tree path to a terminal node. |
| **Template fixation** | Filling sections mechanically without adapting to the domain — "Section 5 says 'Gotchas' so I'll list 10 random warnings" | Every section must serve the domain. A Kubernetes skill's gotchas are about misconfigurations and RBAC; a healthcare skill's are about PHI exposure and audit trails. |
| **Novelty seeking** | Inventing new section formats, table structures, or heading conventions because "this domain is different" | Default to repository standard. The format is battle-tested. If your domain genuinely needs a new section, justify it against at least 3 existing 10/10* skills that don't have it. |



## What Skill Creators Know That Others Don't
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



## Auto-Route (No User Input Required)
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



## Intent Route (Ask the User)
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

┌──────────────────────────────────┐

> 📎 Full content extracted to [references/decision-trees.md](references/decision-trees.md) — 127 lines of detailed guidance, patterns, and code examples.

## Core Workflow

This is the complete skill generation protocol — Phase 0 through Phase 10. Each phase builds on the ...

> 📎 See [references/core-workflow.md](references/core-workflow.md) for complete guidance (323 lines).
## The Skill Quality Rubric

This is how to grade ANY skill. Use it to audit existing skills and self-assess ...

> 📎 Full content extracted to [references/the-skill-quality-rubric.md](references/the-skill-quality-rubric.md) — 16 lines of detailed guidance, patterns, and code examples.

## Domain Mapping Table

Map user requests to skill categories and template references:

> 📎 Full content extracted to [references/domain-mapping-table.md](references/domain-mapping-table.md) — 20 lines of detailed guidance, patterns, and code examples.

## Gotchas — Skill Creation Footguns

These are the specific, expensive mistakes made when CREATING skills — not gener...

> 📎 Full content extracted to [references/gotchas---skill-creation-footguns.md](references/gotchas---skill-creation-footguns.md) — 23 lines of detailed guidance, patterns, and code examples.

## Error Recovery — Skill Creation Failures

- **Generated skill fails `validate-skills.sh`:** Run `bash scripts/validate-ski...

> 📎 Full content extracted to [references/error-recovery---skill-creation-failures.md](references/error-recovery---skill-creation-failures.md) — 15 lines of detailed guidance, patterns, and code examples.

## Verification Guardrails

Run these checks on every generated skill before declaring it complete. ALL must...

> 📎 Full content extracted to [references/verification-guardrails.md](references/verification-guardrails.md) — 21 lines of detailed guidance, patterns, and code examples.

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



## Communication Triggers

| Trigger | Notify | Why |
|---|---|---|
| Generated skill introduces a new category directory | System Architect, Documentation Engineer | New categories affect repository organization and navigation — must align with existing taxonomy |
| Generated skill's chain connections create asymmetry in the graph | All affected skill maintainers | Chain asymmetry causes routing failures — agents can't navigate the skill graph correctly |
| Generated skill fails the self-recreation test | Writing Great Skills | The meta-skill itself may have gaps — if it can't recreate itself, it can't reliably generate other skills |
| Generated skill references a template skill that has been deprecated | Code Reviewer, Qa Engineer | Deprecated templates may encode outdated patterns — ensure generated skill uses current best practices |
| Multiple generated skills for the same domain detected | Product Strategist | Duplicate skills create routing ambiguity — consolidate or differentiate with clear boundary descriptions |



## Escalation Path

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



## Cross-Skills Integration

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

1. **Research before you write.** 60% of skill-building time should be domain re...

> 📎 Full content extracted to [references/best-practices.md](references/best-practices.md) — 25 lines of detailed guidance, patterns, and code examples.

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



## How the State Log Works
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



## State Log Schema

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



## Anti-Drift Check
<!-- AGENT: Run this check at the start of each new phase -->

Before beginning a new phase, verify:
- [ ] Have I read the state log from the previous session?
- [ ] Do any prior decisions constrain what I'm about to do?
- [ ] Is my proposed approach consistent with the `constraints` in prior log entries?
- [ ] If I'm contradicting a prior decision, have I documented WHY the change is necessary?

## Production Checklist

- [ ] **[S1]** Skill name is kebab-case, unique across the repository, and descr...

> 📎 Full content extracted to [references/production-checklist.md](references/production-checklist.md) — 22 lines of detailed guidance, patterns, and code examples.

## What Good Looks Like

> The generated skill is indistinguishable from a hand-crafted 10/10* skill. Every section is domain-specific — ground rules cite real CVEs, gotchas reference actual post-mortems with specific dollar costs, decision trees encode years of practitioner experience in choosing the right approach. The anti-rationalization table reflects deep psychological understanding of developer cognitive biases — the "Why It Feels Right" column makes domain experts uncomfortable because it's exactly what they've told themselves. Chain connections are complete and symmetric, validation passes 6/6, and the skill integrates seamlessly into the 188+ skill ecosystem. A domain expert reading the skill would say "yes, this captures exactly what goes wrong and how to prevent it." The ultimate confirmation: the skill's own workflow is concrete enough that a fresh agent could follow it to recreate the skill itself — the bootstrap invariant holds, guaranteeing quality across every future generation.

## Minimal Viable Skill (MVS) Template

When speed is critical and domain depth can be added later, produce this compact...

> 📎 Full content extracted to [references/minimal-viable-skill-mvs-template.md](references/minimal-viable-skill-mvs-template.md) — 25 lines of detailed guidance, patterns, and code examples.

## Cross-Agent Packaging

Generated skills must work across all major AI agent platforms. Add this section...

> 📎 Full content extracted to [references/cross-agent-packaging.md](references/cross-agent-packaging.md) — 17 lines of detailed guidance, patterns, and code examples.

## References

Detailed reference material loaded on demand:

- **Anti-Rationalization**: See [anti-rationalization.md](references/anti-rationalization.md)
- **Best Practices**: See [best-practices.md](references/best-practices.md)
- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Deliberate Practice**: See [deliberate-practice.md](references/deliberate-practice.md)
- **Error Recovery**: See [error-recovery.md](references/error-recovery.md)
- **Gotchas**: See [gotchas.md](references/gotchas.md)
- **Scale Depth: Operating at Different Levels**: See [scale-depth.md](references/scale-depth.md)
- **State Log**: See [state-log.md](references/state-log.md)
- **Verification Guardrails**: See [verification-guardrails.md](references/verification-guardrails.md)
- **What Good Looks Like**: See [what-good-looks-like.md](references/what-good-looks-like.md)



## External Resources

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
