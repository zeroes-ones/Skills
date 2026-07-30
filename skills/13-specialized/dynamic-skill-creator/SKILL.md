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

## Error Recovery
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

| Symptom | Root Cause | Fix |
|---------|-----------|-----|
| Generated skill has generic gotchas copied from other skills — "hardcoded credentials in source code" appears in unrelated domains | Failure to research domain-specific postmortems, CVEs, and incident reports during skill generation | Re-run research phase targeting domain-specific incident databases. For each gotcha, require a real-world citation (CVE, postmortem link, incident report). Gotchas are the highest-token-cost section — generic ones waste 80% of the section's value |
| Decision tree has overlapping branches — same outcome from two different paths | Branches not MECE (Mutually Exclusive, Collectively Exhaustive). Ambiguous decision criteria | Draw the tree on paper first. For each node, verify: (1) every possible input falls into exactly one branch, (2) no input can match two branches simultaneously. Use mutually exclusive conditions |
| Generated skill is 10x too short — 200 lines vs 600+ line standard | Only the decision tree was generated; all other sections skipped. Model stopped after the first major section | Re-run with explicit section checklist. Order: Decision Tree first (highest value), then Gotchas, then Core Workflow, then remaining sections. Verify: word count > 5000, all 15 standard sections present |
| Cross-Skill Coordination table references skills that don't exist | Upstream/downstream skill names fabricated from training data without verification | Check `skills/` directory to verify each referenced skill exists at the path listed. Use only skill names from the actual repository inventory |
| Dollar-quantified gotcha costs are obviously wrong — $1M for a typo fix | Costs hallucinated without real incident data. Model fills in plausible-sounding but fictional numbers | Cross-reference each cost with: (1) public breach reports, (2) cloud provider outage postmortems, (3) SRE incident writeups. If no real incident found, mark cost as `[ESTIMATE]` and note the assumption |

## Gotchas
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

| Gotcha | Cost | Fix |
|--------|------|-----|
| Generating a skill from memory without domain research — the "I know this domain" fallacy | $20K-$50K in wasted iterations; skill passes lint but produces wrong advice because gotchas are generic and decision trees miss domain-specific branches | Research phase is non-negotiable: spend 30+ minutes reading postmortems, CVEs, incident reports, and stack overflow threads for gotcha material before writing a single section. Memory is not research |
| Copying trigger patterns from other skills — "use when building... or designing... or implementing..." matches everything | $10K-$30K in routing failures; trigger phrase too generic causes false activation on unrelated tasks across the entire skill fleet | Use the `grep` uniqueness test: if your trigger phrase appears in >3 other skills' SKILL.md decision trees, it's too generic. Craft triggers with domain-specific nouns: "openapi 3.1" not "api design" |
| Decision tree with >7 options at a single node — cognitive overload for the routing agent | $5K-$15K in misrouting failures; agents presented with >7 options degrade to random selection or default fallback | Follow the 3-Option Rule: every decision tree node should offer 3 options, maximum 5. If you have more, create a parent node that splits the options into categories first |
| Missing the "I don't know" branch in every decision tree — agent forced to pick wrong option when uncertain | $15K-$40K in hallucinated advice; agent forced into a branch that doesn't fit the query produces confident but wrong output | Every decision tree branch must end with: either a concrete action path OR an explicit "route to general-purpose agent with context" fallback. No dead ends |
| Token budget not calibrated — skill is 800 lines but model has 200K context vs 32K | $10K-$25K in truncated execution; skill exceeds model's effective context window, losing the last 40% of sections during inference | Write skill for the 32K-token agent constraint. Budget: YAML frontmatter ~500 tokens, Description ~100, Decision Tree ~3000, Core Workflow ~2000, Gotchas ~2000, remaining sections ~2000. Total: ~10K tokens |
| Skill contains vendor-specific frontmatter fields that break on non-Claude platforms | $30K-$80K in portability debt; skill silently fails or degrades on Copilot, Gemini, Cursor because it uses Claude-specific YAML keys | Portability test: run `grep -r "model:" skills/your-skill/SKILL.md` — if found, remove. No `claude:` fields, no `model:` overrides, no `temperature:` in SKILL.md frontmatter. All vendor config lives in consumer-agent-specific files |
| Generated skill has no script/ or references/ directory — all prose, no executable verification | $15K-$30K in unverifiable advice; skill makes claims (e.g., "run roi-gate.sh") but the script doesn't exist in the skill directory | For every script referenced in the skill body, create it in `skills/skill-name/scripts/`. For every external reference, create it in `skills/skill-name/references/`. Lint check: `ls skills/skill-name/scripts/` must not be empty |
## <!-- DEEP: 5+min --> RESEARCH_PREREQUISITE — Execute Before Any Output

**This is a HARD GATE. Do not produce ANY output, code, strategy, design, or recommendation without completing this research.**

Before you act, you MUST execute every applicable research step. Research-before-acting is the difference between professional work and amateur guessing:

| # | Research Step | Why It Matters | Where to Look |
|---|--------------|----------------|----------------|
| **RP1** | **Verify domain currency.** Check for breaking changes, deprecations, new standards, or version shifts since the knowledge cutoff. | [STALE_RISK] Outdated advice breaks real systems. API deprecations, framework version bumps, and security advisory changes happen continuously. Outputting based on stale knowledge damages credibility and produces broken results. | Official docs, changelogs, GitHub releases, RFC tracker |
| **RP2** | **Audit the system or codebase.** Read relevant files. Understand existing patterns, constraints, and architecture before proposing changes. | [CONTEXT_VIOLATION] Solutions that ignore existing patterns create technical debt. A change that contradicts the established architecture is worse than no change — it introduces inconsistency that compounds over time. | Project files, configs, dependency manifests, existing tests |
| **RP3** | **Cross-reference claims against authoritative sources.** Every factual assertion needs a verifiable source. Mark each: [VERIFIED], [COMPUTED], or [ESTIMATED]. | [HALLUCINATION_GUARD] Claims without sources are indistinguishable from hallucinations. The #1 cause of incorrect output is treating assumptions as facts. Source tagging prevents this. | Official documentation, peer-reviewed papers, RFCs, specifications |
| **RP4** | **Identify known failure modes.** Before recommending, list what commonly breaks. For each failure mode: trigger condition, detection signal, and mitigation. | [FAILURE_BLINDNESS] Every domain has known failure patterns. Output that doesn't address them is dangerously incomplete. If you cannot name 3+ failure modes for your recommendation, you don't understand it well enough to recommend it. | Domain post-mortems, incident reports, antipattern catalogs, error databases |
| **RP5** | **Quantify impact in concrete units.** Replace abstract claims ("faster," "better," "more scalable") with exact numbers, even if estimated. | [VAGUENESS_PENALTY] "Faster" is unverifiable. "Reduces p95 latency from 340ms to 120ms (±15ms)" is verifiable. Abstract adjectives hide ignorance behind confidence. Concrete numbers expose gaps. | Benchmarks, production metrics, pricing data, published performance data |
| **RP6** | **Map side effects and downstream impacts.** What else breaks? Which dependencies are affected? Which downstream consumers need updating? | [CASCADE_BLINDNESS] Changes to one component ripple outward. A fix in module A can break module B that depends on A's old behavior. Map the blast radius before acting. | Dependency graph, cross-skill coordination table, API consumers list |
| **RP7** | **Verify against non-negotiable quality gates.** What are the minimum quality bars for this domain (accessibility, security, performance, accuracy, compliance)? | [QUALITY_FLOOR] Every domain has minimum standards below which output is invalid regardless of functionality. Missing WCAG AA = broken. Leaking credentials = broken. Silent data loss = broken. | Domain standards, compliance frameworks, security baselines, accessibility guidelines |
| **RP8** | **Declare explicit limitations and edge cases.** What does this NOT handle? What are the known boundaries? What scenarios are explicitly out of scope? | [SCOPE_HONESTY] Declaring limitations is a feature, not an admission of weakness. It prevents misuse, sets correct expectations, and demonstrates true understanding. Every solution has boundaries — naming them is professional. | This SKILL.md, domain literature, edge case databases |

**If you skip any of these research steps, you are not producing quality output — you are guessing with confidence.** Guessing wastes time, breaks systems, and destroys trust. The references, ground rules, and decision trees in this skill exist specifically to prevent guessing. Use them.

> **Compliance:** Research must be executed before any substantial output. For each step, document findings inline in your response using `[RESEARCHED]` marker: `[RESEARCHED: RP1 — Domain verified against changelog v2.4. No breaking changes since cutoff.]`. Partial research = partial quality. Zero research = zero credibility.



### 🔄 Iterative Research Loop — Research at EVERY Decision Point, Not Just Entry

**The RP1-RP8 cycle above is NOT a one-time gate.** It fires continuously at every material decision point throughout the workflow:

| Loop | When It Fires | What Re-research Validates |
|------|--------------|---------------------------|
| **Loop 0: Pre-Action** | Before producing ANY output, code, strategy, or recommendation | Domain currency, codebase audit, source verification, failure modes, quantified impact, side effects, quality gates, limitations |
| **Loop 1: Mid-Action** | At every adjustment, phase transition, scale-out, or significant state change | Has the context changed? Are the original assumptions still valid? Has new information invalidated the Loop 0 conclusions? |
| **Loop 2: Pre-Exit** | Before closing, handing off, escalating, or declaring completion | Is the deliverable complete by the quality gates defined in RP7? Are all limitations declared (RP8)? Have failure modes been addressed (RP4)? |
| **Loop 3: Post-Action** | After completion: compare expected vs. actual outcome | What was the efficiency ratio (actual / theoretical max)? What learnings emerged? What should be fed back into the pattern database for future decisions? |

**Integration into Core Workflow:**

Every decision point in a skill's Core Workflow must be marked with:
```
[RESEARCH LOOP: Re-execute RP1-RP8 before proceeding to next phase]
```

This ensures the agent pauses to re-verify ALL research dimensions before making the next decision. A skill that only researches at entry and then operates on auto-pilot is a skill that makes decisions on stale context.

**Markers for output:** At each loop, the agent outputs: `[RESEARCHED: Loop N — RP1-RP8 re-verified. Key delta from previous loop: ...]`

**Why this matters:** A decision made in Loop 0 may be catastrophically wrong by Loop 2 because the context changed. Markets move. Requirements shift. Dependencies update. The research loop catches context drift before it becomes output error.

> **Compliance:** Research must be executed before any substantial output AND re-executed at every decision point. For each research loop, document findings inline. Partial research = partial quality. Zero research = zero credibility. Stale research = dangerous confidence.



## Anti-Hallucination
<!-- STANDARD: 3min -->

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
<!-- STANDARD: 3min -->

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
| R11 | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| R12 | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |

- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.

## The Expert's Mindset
<!-- STANDARD: 3min -->

You are not just writing a SKILL.md — you are encoding years of domain expertise into tokens that reliably produce expert behavior in an AI agent. The agent will follow your instructions literally, pattern-match against your decision trees, and internalize your ground rules as non-negotiable constraints. Every sentence you write shapes thousands of future agent decisions.

## The Mental Model Shift
<!-- STANDARD: 3min -->
- **The agent is your apprentice, not your peer.** It has encyclopedic general knowledge but zero domain-specific judgment. Your job is to provide the judgment framework — the "when NOT to do X" that general knowledge lacks. The most valuable sentence in any skill is "Do NOT use [approach] when [condition]."
- **Research reveals what expertise conceals.** You know your domain so well that you've forgotten what's hard about it. Research CVEs, post-mortems, and Stack Overflow questions to rediscover the pain points. The gotchas that make you say "oh right, that got me too in 2018" are the ones that matter.
- **Structure is the message.** Agents pattern-match against structure before they process content. A well-structured decision tree communicates more in 30 lines than 300 lines of prose explanation. Tables beat paragraphs. ASCII trees beat tables. Ground rules as mechanical triggers beat prose admonitions.
- **The bootstrap test is the ultimate quality gate.** Ask: "If I fed this skill to a fresh agent with no other skills loaded, could that agent generate a 10/10* skill for any domain?" If the answer is no, you have gaps. This is why the Phase 0 discovery questions, the domain mapping table, the quality rubric, and the gotcha research guide must be complete.

## Cognitive Biases That Corrupt Skill Creation
<!-- STANDARD: 3min -->
| Bias | How It Manifests | Antidote |
|-------|------------------|----------|
| **Curse of knowledge** | Skipping fundamental gotchas because "everyone knows that" — writing for experts, not for the agent who has no context | Research what beginners ask on Stack Overflow. The most-upvoted questions are what your skill needs to cover. |
| **Overconfidence bias** | Assuming you can write a 10/10* skill in 2 hours without research — "I've been doing this for 15 years" | Time-box research: 60% of skill-building time on domain research (CVEs, post-mortems, incident reports), 40% on structuring. |
| **Completion bias** | Satisfied when validation passes — "6/6 checks, ship it!" — ignoring that validation measures structure, not substance | Manual review after validation: read every gotcha aloud, verify every dollar figure against a real source, trace every decision tree path to a terminal node. |
| **Template fixation** | Filling sections mechanically without adapting to the domain — "Section 5 says 'Gotchas' so I'll list 10 random warnings" | Every section must serve the domain. A Kubernetes skill's gotchas are about misconfigurations and RBAC; a healthcare skill's are about PHI exposure and audit trails. |
| **Novelty seeking** | Inventing new section formats, table structures, or heading conventions because "this domain is different" | Default to repository standard. The format is battle-tested. If your domain genuinely needs a new section, justify it against at least 3 existing 10/10* skills that don't have it. |

## What Skill Creators Know That Others Don't
<!-- STANDARD: 3min -->
- **Gotchas sourced from real incidents are 10x more persuasive than generic warnings.** "Misconfigured S3 bucket exposes customer data" is forgettable. "Capital One's 2019 breach: $190M in fines + $80M remediation because a single S3 bucket had `AuthenticatedUsers: READ` — the exact misconfiguration this gotcha prevents" is unforgettable.
- **The anti-rationalization table is the hardest and most important section.** It takes 30+ minutes to write well because you must identify the lies developers tell themselves AND understand the psychology behind those lies. "We're too small to be a target" = optimism bias + normalcy bias. "The framework handles security" = diffusion of responsibility + authority bias toward framework authors.
- **Chain connections determine discoverability, not just correctness.** A brilliant skill with empty `chain_feeds_into` is invisible to the chain router. When agents navigate the skill graph, orphaned skills don't appear in any routing path. Every skill needs at least 2 upstream and 2 downstream connections.
- **The quality rubric must be self-referential.** The rubric in this skill is what you use to grade generated skills. It must be specific enough that two independent evaluators would assign the same grade to the same skill. "8/10 (Good)" is worthless. "8/10: Domain-specific ground rules with some examples, but 3 ground rules lack violation stories" is actionable.

## When to Use
<!-- STANDARD: 3min -->

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
<!-- STANDARD: 3min -->

<!-- TWO-TIER ROUTING: Auto-Route table (machine) → Intent Route tree (human fallback) -->

## Auto-Route (No User Input Required)
<!-- STANDARD: 3min -->
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
<!-- STANDARD: 3min -->
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
<!-- STANDARD: 3min -->

### Decision Tree 1: Skill Generation vs. Boost vs. Audit

```
        ┌── INPUT: What does the user want?
        │
   ┌────┴────────────┐
   │                 │
   ▼                 ▼
"generate/create"  "boost/improve/upgrade"
   │                 │
   ▼                 ▼
Phase 0: Discovery  Skill Boost Strategy
   │                 │
   ├─ Domain known?  ├─ Audit current score
   │  ├─ YES → Map   │  ├─ < 5/10 → Full regen
   │  └─ NO → Ask    │  ├─ 5-7/10 → Targeted boost
   │                 │  └─ 8+/10 → Polish only
   ▼                 ▼
Full Generation    Upgrade Protocol
```

### Decision Tree 2: Skill Complexity Tier Selection

```
        ┌── INPUT: Domain scope and risk level
        │
   ┌────┴────────────────┐
   │                     │
   ▼                     ▼
Simple tool/pattern   Security/finance/healthcare
   │                     │
   ▼                     ▼
TRIVIAL (200-400 lines) CRITICAL assessment
   │                     │
   │                ┌────┴────┐
   │                │         │
   │                ▼         ▼
   │           Production   Life-safety
   │           security      or compliance
   │                │         │
   │                ▼         ▼
   │           STANDARD    CRITICAL
   │          (400-700)   (600-1000)
   ▼
Minimal sections:     Full sections:
description,          description, ground rules,
core workflow,         anti-hallucination,
gotchas, references    verification, error decoder,
                       decision trees, scale depth
```

### Decision Tree 3: Skill Boundary Check — New Skill or Extend Existing?

```
        ┌── INPUT: Proposed skill domain
        │
   ┌────┴────────────────────┐
   │                         │
   ▼                         ▼
Overlaps > 50% with        Unique domain with
existing skill?             < 30% overlap?
   │                         │
   ▼                         ▼
EXTEND existing skill       CREATE new skill
   │                         │
   ├─ Add workflow phase     ├─ Check chain connections
   ├─ Add decision tree      ├─ upstream: who calls this?
   ├─ Add gotchas            └─ downstream: who does this feed?
   └─ Update cross-skill
      coordination
```

### Decision Tree 4: Token Budget and Content Density

```
        ┌── INPUT: Skill line count and complexity
        │
   ┌────┴────────────────┐
   │                     │
   ▼                     ▼
Line count < 400       Line count > 700 (standard)
                        or > 1000 (critical)
   │                     │
   ▼                     ▼
Room to expand:        PRUNE aggressively:
add examples,           │
anti-patterns,          ├─ Move references to references/
scale depth             ├─ Remove redundant examples
                        ├─ Use progressive disclosure (Tier 1/2/3)
                        └─ Verify: does each sentence change behavior?
```

## Core Workflow
<!-- STANDARD: 3min -->

This is the complete skill generation protocol — Phase 0 through Phase 10. Each phase builds on the ...

> 📎 See [references/core-workflow.md](references/core-workflow.md) for complete guidance (323 lines).
## The Skill Quality Rubric
<!-- STANDARD: 3min -->

This is how to grade ANY skill. Use it to audit existing skills and self-assess ...

> 📎 Full content extracted to [references/the-skill-quality-rubric.md](references/the-skill-quality-rubric.md) — 16 lines of detailed guidance, patterns, and code examples.

## Domain Mapping Table
<!-- STANDARD: 3min -->

Map user requests to skill categories and template references:

> 📎 Full content extracted to [references/domain-mapping-table.md](references/domain-mapping-table.md) — 20 lines of detailed guidance, patterns, and code examples.

## Gotchas — Skill Creation Footguns
<!-- STANDARD: 3min -->

These are the specific, expensive mistakes made when CREATING skills — not gener...

> 📎 Full content extracted to [references/gotchas---skill-creation-footguns.md](references/gotchas---skill-creation-footguns.md) — 23 lines of detailed guidance, patterns, and code examples.

## Error Recovery — Skill Creation Failures
<!-- STANDARD: 3min -->

- **Generated skill fails `validate-skills.sh`:** Run `bash scripts/validate-ski...

> 📎 Full content extracted to [references/error-recovery---skill-creation-failures.md](references/error-recovery---skill-creation-failures.md) — 15 lines of detailed guidance, patterns, and code examples.

## Verification
<!-- STANDARD: 3min -->

| # | Complete when... | Verify |
|---|-----------------|--------|
| ☐ | Complete when Generated skill passes all 10 ground rules (R1-R10) | `grep -c "TODO\|TBD\|\[Coming soon\]" generated-skill.md` returns 0 |
| ☐ | Complete when Skill contains 6+ dollar-quantified gotchas ($X,XXX+) | `grep -c '\$[0-9]' generated-skill.md` returns 10+ for standard, 15+ for security |
| ☐ | Complete when Anti-rationalization table has 6+ rows in 4-column format | `grep -c "Temptation\|Feels Right\|Devastating Reality\|Prevention" generated-skill.md` returns 24+ |
| ☐ | Complete when Decision trees use ASCII art with YES/NO branching | Verify `├──`, `└──`, `│` characters appear in at least 3 decision trees |
| ☐ | Complete when Chain connections declared (consumes_from AND feeds_into non-empty) | `grep "chain_consumes_from\|chain_feeds_into" generated-skill.md` shows populated arrays |
| ☐ | Complete when Skill passes the self-recreation (bootstrap) test | Could this skill generate itself at 10/10* quality following its own workflow? |
| ☐ | Complete when Token budget within limits (standard < 700 lines, critical < 1000) | `wc -l generated-skill.md` is within budget |
| ☐ | Complete when Phase 0 discovery questions answered before content generation | 5+ of 8 discovery questions addressed in skill preamble |
| ☐ | Complete when Error recovery paths exercised for top 3 failure modes | Simulate each failure → verify recovery path produces actionable output |
| ☐ | Complete when Skill validates against repository conventions (format, section ordering) | Diff against existing 10/10* skill — no structural deviations |

## Verification Guardrails
<!-- STANDARD: 3min -->

Run these checks on every generated skill before declaring it complete. ALL must...

> 📎 Full content extracted to [references/verification-guardrails.md](references/verification-guardrails.md) — 21 lines of detailed guidance, patterns, and code examples.

## Cross-Skill Coordination
<!-- STANDARD: 3min -->

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
<!-- STANDARD: 3min -->

| Trigger | Notify | Why |
|---|---|---|
| Generated skill introduces a new category directory | System Architect, Documentation Engineer | New categories affect repository organization and navigation — must align with existing taxonomy |
| Generated skill's chain connections create asymmetry in the graph | All affected skill maintainers | Chain asymmetry causes routing failures — agents can't navigate the skill graph correctly |
| Generated skill fails the self-recreation test | Writing Great Skills | The meta-skill itself may have gaps — if it can't recreate itself, it can't reliably generate other skills |
| Generated skill references a template skill that has been deprecated | Code Reviewer, Qa Engineer | Deprecated templates may encode outdated patterns — ensure generated skill uses current best practices |
| Multiple generated skills for the same domain detected | Product Strategist | Duplicate skills create routing ambiguity — consolidate or differentiate with clear boundary descriptions |

## Escalation Path
<!-- STANDARD: 3min -->

```
Skill fails validation? → Run verbose checks → Fix in order (frontmatter → sections → chain) → Re-validate
Chain asymmetry detected? → Identify direction of asymmetry → Fix consuming skill's feeds_into OR producing skill's consumes_from → Re-validate symmetry
Generated skill is hollow (passes validation but lacks substance)? → Return to Phase 0 → Re-research domain → Rebuild from ground rules up
Self-recreation test fails? → Escalate to writing-great-skills → Audit the dynamic-skill-creator's own Phases for gaps → Update this skill
Domain mapping table missing entry for common domain? → Add entry → Verify template reference is still a 10/10* skill → Submit as improvement to this skill
```

## Operating at Different Levels
<!-- STANDARD: 3min -->

| Scale | Team | What Changes | What to Skip | Transition Trigger |
|-------|------|-------------|-------------|-------------------|
| **Solo** | 1 | Quick MVS generation. 5 ground rules, 5 gotchas, 4 anti-rationalization entries. 300-400 lines. Research time: 30-45 min. Generate from the Minimal Viable Skill template. | Skip full 12-section build. Skip reference files. Skip behavioral eval creation. Skip chain YAML files (frontmatter chain connections only). | When a second person needs to use the skill — MVS lacks the depth for multi-user consumption |
| **Small** | 2-10 | Full 12-section skill. 8 ground rules, 8 gotchas, 6 anti-rationalization entries. 500-600 lines. Research time: 2-3 hours. Complete chain connections with symmetry verification. | Skip behavioral eval scenarios (use verification guardrails only). Skip cross-agent packaging. Skip drift monitoring. Skip external reference files (link to web resources instead). | When the skill is used by 3+ different agent types (Claude Code, Copilot, Cursor) — need cross-agent compatibility |
| **Medium** | 10-50 | Full skill + behavioral eval scenarios + reference files. 9-10 ground rules, 10+ gotchas, 7-8 anti-rationalization entries. 700-900 lines. Research time: 4-6 hours. Complete chain YAML, reference file creation, eval scenario design. | Skip drift monitoring automation. Skip cross-agent manifest generation (do manual packaging). Skip comprehensive domain research archive (keep gotcha sources in comments). | When the skill is part of a CI/CD pipeline — needs automated validation and behavioral evals |
| **Enterprise** | 50+ | Full skill + references + evals + chain orchestration + drift monitoring tests + cross-agent packaging + domain research archive. 10 ground rules, 15+ gotchas, 8+ anti-rationalization entries. 900-1200 lines. Research time: 8-12 hours. All reference files created, eval pipeline integrated, chain YAML validated, monitoring dashboards configured. | Nothing — at enterprise scale, all depth is justified. Even drift monitoring pays for itself in preventing quality decay across hundreds of agent invocations. | When the skill is mission-critical — incorrect output has regulatory, financial, or safety consequences |

## Cross-Skills Integration
<!-- STANDARD: 3min -->

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
<!-- STANDARD: 3min -->

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

## Error Decoder — War Stories from the Trenches
<!-- STANDARD: 3min -->

**(STANDARD)**

When this domain goes wrong, it goes wrong in predictable ways. Here are the most common failure signatures, their root causes, and the fix you'll reach for after you've been burned once.

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Generated skill passes all 12 mandatory section checks with perfect scores. Agent loads the skill → ignores the ground rules entirely, defaults to training-data behavior. "The skill says never do X, but the agent did X on the very first request" | Validation measures structure, not behavioral compliance. The skill has correct headers, valid frontmatter, complete sections — but the ground rules aren't specific enough to override the agent's strong training-data priors. The agent defaults to what it "knows" from training, not what the skill instructs | Run behavioral validation: design 3 test scenarios that specifically test each ground rule. For a "never use eval()" rule, give the agent a task where `eval()` is the shortest path. If the agent uses `eval()`, the rule needs to be stronger — add dollar-quantified consequences, mechanical triggers, and a violation response. Structure alone doesn't change behavior | Skill validation measures compliance with the rubric. Behavioral validation measures compliance with the rules. They're different things. A skill that scores 10/10 on the rubric can still produce 0/10 output if the ground rules don't override the agent's training defaults. Test behavior, not structure |
| Skill frontmatter has 25 fields — every field from every agent's spec. Agent loads the skill but silently drops 3 fields that aren't in its schema. The skill partially works — core instructions load, but tool restrictions and token budget are ignored. User can't tell the skill is degraded | Maximalist frontmatter: "include everything, let the agent sort it out." But agents silently drop unknown fields rather than erroring. The fields that were dropped controlled tool access and context limits — the skill loaded without them, producing unbounded output that exhausted the token budget | Target-specific validation: test that every frontmatter field is actually consumed by each target agent. For Copilot CLI, validate that `allowed-tools` actually restricts tools. For Claude Code, validate that `token_budget` actually limits output. Maintain a compatibility matrix: field → supported agents. Flag fields that are silently dropped — they create false confidence | Frontmatter fields that are silently ignored are a security risk, not just a compatibility issue. If `allowed-tools: Read` is ignored, the agent has unrestricted tool access and the user doesn't know. Validation must test consumption, not just presence. A field in the frontmatter that the agent doesn't read is a lie |
| Gotcha section cites dollar figures: "This mistake costs $10K-$50K." User asks: "Where did you get these numbers?" No source. The gotcha is plausible but fabricated — the agent synthesized a realistic-sounding cost without any reference. Credibility of the entire skill collapses | Gotcha costs generated by LLM without source verification. The agent is good at producing plausible-sounding numbers that have no basis in reality. The $10K-$50K range is realistic enough to pass review but specific enough to be questioned — and it can't be defended without a source | For every gotcha, find at least one real incident or calculate from first principles: downtime_hours × revenue_rate + remediation_hours × $150/hr. Cite the source: "Source: GitLab 2017 database outage — $1.2M in SLA credits + 18 hours engineering time." If no real incident exists, calculate with documented methodology. Never use LLM-generated dollar figures without verification | Unverifiable dollar figures are the fastest way to destroy a skill's credibility. The user will test one claim, find it unsourced, and doubt everything else. Every dollar figure must be traceable: either to a public incident or to a documented calculation. "It sounded reasonable" is not a source |
| Decision tree has 8 levels of nesting — agent can't parse the indentation reliably. Takes wrong branch at level 4 and follows it through levels 5-8. Output is technically valid but follows the wrong decision path — correct structure, wrong domain context | ASCII decision trees are parsed by LLMs as text, not as structured logic. Deep nesting creates ambiguity: when at level 4, is the next indented line a sub-option or a sibling? The agent resolves ambiguity using training-data patterns, which are often wrong for this specific domain. No validation that the agent actually follows the tree correctly | Limit decision trees to 4 levels max. For deeper logic, use numbered lists with explicit "goto" references: "If YES → go to section 3.2." Test tree traversal: for each leaf node, verify the agent can navigate from root to that leaf when given the matching inputs. Add a verification step: "You are now at decision point: [X]. Confirm you reached this point by restating the conditions that led here" | ASCII decision trees are a visual format being parsed by a text model. Deep nesting creates parsing ambiguity that the model resolves inconsistently. Shallower trees with explicit navigation are more reliable than deep trees with implicit indentation semantics. Test actual traversal, not just structural completeness |
| Generated skill is 8,000 tokens → exceeds the 4,000 token budget for the target agent. Agent loads the skill, hits the token limit mid-section, and truncates. Truncation happens in the middle of the Ground Rules section — the last 3 rules (the most specific ones) are missing. Agent operates without critical constraints | Token budget specified in skill metadata but not validated against actual file size. The skill generator produced comprehensive content without considering the consumption environment's limits. Token counting doesn't account for the agent's system prompt and conversation overhead — the "4,000 token budget" means 4,000 total, not 4,000 for the skill alone | Calculate skill token budget: target_agent_total_budget − system_prompt_overhead − min_conversation_tokens = max_skill_tokens. For a 4,000 token agent: ~1,500 system + ~500 conversation + ~2,000 skill. Generate skill to 1,800 token target (10% safety margin). Validate token count in CI: fail if skill exceeds budget. Implement progressive disclosure: references/ for deep content, SKILL.md for essential instructions | Token budgets are hard limits, not guidelines. A skill that exceeds the budget is silently truncated — the agent loads partial instructions but doesn't know which parts are missing. Token counting must account for total consumption, not just the skill file. Progressive disclosure (SKILL.md essentials + references/ deep dives) is the architectural pattern for staying within budget |
| Skill created for "healthcare-compliance" domain → passes all validation. Deployed. User reports: "There's already a healthcare-compliance skill — now there are two, and the agent randomly picks one." The duplicate was created 3 months ago by a different team, stored in a different directory, and wasn't in the manifest the creator checked | No duplicate detection before skill creation. The `skills-manifest.json` the creator referenced was stale. The existing skill used a different naming convention (`healthcare-compliance` vs `healthcare_compliance`) so exact-name matching didn't catch it. Both skills are valid and both are in the agent's skill directory — non-deterministic routing | Before creating a skill, search: (1) `grep -r "name:" skills/` for similar names, (2) compare descriptions with cosine similarity against all existing skills, (3) check skills-manifest.json for functional overlap. If a similar skill exists: extend it as a sub-skill instead of creating a duplicate. Implement manifest-level duplicate detection: reject skills with >80% description similarity to an existing skill | Duplicate skills create non-deterministic agent behavior — the user gets different quality depending on which skill loads. The cost of creating a duplicate is not the creation time — it's every future user's degraded experience when the wrong skill fires. Duplicate detection is an essential gate in the skill creation pipeline |

## Best Practices
<!-- STANDARD: 3min -->

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
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.

## How the State Log Works
<!-- STANDARD: 3min -->
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
<!-- STANDARD: 3min -->

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
<!-- STANDARD: 3min -->
<!-- AGENT: Run this check at the start of each new phase -->

Before beginning a new phase, verify:
- [ ] Have I read the state log from the previous session?
- [ ] Do any prior decisions constrain what I'm about to do?
- [ ] Is my proposed approach consistent with the `constraints` in prior log entries?
- [ ] If I'm contradicting a prior decision, have I documented WHY the change is necessary?

## Production Checklist
<!-- STANDARD: 3min -->

- [ ] **[S1]** Skill name is kebab-case, unique across the repository, and descr...

> 📎 Full content extracted to [references/production-checklist.md](references/production-checklist.md) — 22 lines of detailed guidance, patterns, and code examples.

## What Good Looks Like
<!-- STANDARD: 3min -->

> The generated skill is indistinguishable from a hand-crafted 10/10* skill. Every section is domain-specific — ground rules cite real CVEs, gotchas reference actual post-mortems with specific dollar costs, decision trees encode years of practitioner experience in choosing the right approach. The anti-rationalization table reflects deep psychological understanding of developer cognitive biases — the "Why It Feels Right" column makes domain experts uncomfortable because it's exactly what they've told themselves. Chain connections are complete and symmetric, validation passes 6/6, and the skill integrates seamlessly into the 188+ skill ecosystem. A domain expert reading the skill would say "yes, this captures exactly what goes wrong and how to prevent it." The ultimate confirmation: the skill's own workflow is concrete enough that a fresh agent could follow it to recreate the skill itself — the bootstrap invariant holds, guaranteeing quality across every future generation.

## Minimal Viable Skill (MVS) Template
<!-- STANDARD: 3min -->

When speed is critical and domain depth can be added later, produce this compact...

> 📎 Full content extracted to [references/minimal-viable-skill-mvs-template.md](references/minimal-viable-skill-mvs-template.md) — 25 lines of detailed guidance, patterns, and code examples.

## Cross-Agent Packaging
<!-- STANDARD: 3min -->

Generated skills must work across all major AI agent platforms. Add this section...

> 📎 Full content extracted to [references/cross-agent-packaging.md](references/cross-agent-packaging.md) — 17 lines of detailed guidance, patterns, and code examples.

## References
<!-- STANDARD: 3min -->

Detailed reference material loaded on demand:

- **Anti-Rationalization**: See [anti-rationalization.md](references/anti-rationalization.md)
- **Best Practices**: See [best-practices.md](references/best-practices.md)
- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Deliberate Practice**: See [deliberate-practice.md](references/deliberate-practice.md)
- **Error Recovery**: See [error-recovery.md](references/error-recovery.md)
- **Gotchas**: See [gotchas.md](references/gotchas.md)
- **State Log**: See [state-log.md](references/state-log.md)
- **Verification Guardrails**: See [verification-guardrails.md](references/verification-guardrails.md)
- **What Good Looks Like**: See [what-good-looks-like.md](references/what-good-looks-like.md)

## External Resources
<!-- STANDARD: 3min -->

- **Skill Template — Annotated**: Full annotated template with section-by-section guidance for every mandatory section. Shows exactly what each section must contain with inline examples. Study existing 10/10* skills: `skills/05-development/mobile-developer/SKILL.md`, `skills/05-development/backend-developer/SKILL.md`.
- **Quality Rubric — Detailed**: 10-dimension quality scoring guide with specific examples of 6/10, 8/10, and 10/10* for each dimension. See `SKILL-QUALITY-STANDARDS.md` in repository root.
- **Domain Research Protocol**: Step-by-step research methodology for any domain: CVE database search, Hacker News post-mortem mining, Stack Overflow war story collection, industry report extraction. Use web search + CVE databases + GitHub issues for gotcha discovery.
- **Gotcha Research Guide**: Finding real-world dollar-quantified incidents: breach cost databases, downtime calculators, migration cost estimation formulas, and source citation format.
- **Chain Architecture Guide**: How to connect new skills to the 821+ edge graph: finding natural upstream/downstream relationships, creating chain YAML entries, verifying symmetry, and handling new domain introduction. See `scripts/skill-router.py` for live chain verification.
- **Writing Great Skills**: See `skills/00-framework/writing-great-skills/SKILL.md` — The foundational meta-skill for skill authoring. Covers vocabulary, failure modes, pruning, and progressive disclosure architecture.
- **Skill Quality Standards**: See `SKILL-QUALITY-STANDARDS.md` — Repository-wide quality standards document. Defines the 10/10 quality bar, the 30-second test, the footgun test, the handoff test, and the checklist test.
- **Coordination Matrix**: See `COORDINATION-MATRIX.md` — Auto-generated matrix of all chain connections across 188+ skills, organized by project phase.
- **Validation Scripts**: `scripts/validate-skills.sh`, `scripts/skill-router.py`, `scripts/behavioral-evals.py` — Automated governance checks, routing verification, and behavioral testing.
- **Template Skills (10/10* reference)**: `skills/05-development/mobile-developer/SKILL.md`, `skills/05-development/backend-developer/SKILL.md`, `skills/06-quality/code-reviewer/SKILL.md`, `skills/06-quality/security-reviewer/SKILL.md` — Battle-tested skill structures.
