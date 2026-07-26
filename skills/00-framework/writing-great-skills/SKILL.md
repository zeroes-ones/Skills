---
name: writing-great-skills
description: >
  Use when writing a new skill for an AI agent (Claude Code, Copilot CLI, Cursor, Codex, Gemini
  CLI); when editing or improving an existing skill; when a skill produces inconsistent results;
  when designing the invocation pattern for a skill; when setting token budgets and chain
  configurations; or when testing skill routing across consumer agents. Handles skill structure
  (YAML frontmatter, invocation, decision tree, body, routing), trigger design (unique phrases,
  avoiding false positives, Trigger vs context), decision tree construction (MECE, fail-safe
  fallback, 3-Option Rule), token budget calibration, and cross-agent testing (Claude Code, Copilot
  CLI, Cursor, Codex, Gemini CLI). Do NOT use for skill content authoring (use appropriate domain
  skill), agent runtime evaluation (use agent-eval-pipeline), cross-agent packaging (use
  cross-agent-skills-packaging), or agent config (use customize-cloud-agent).
author: Sandeep Kumar Penchala
license: MIT
output: "skill"
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
type: framework
status: stable
version: 1.0.0
updated: 2026-07-23
tags:
  - skill-authoring
  - meta-skill
  - token-efficiency
  - pruning
  - progressive-disclosure
  - failure-modes
  - anti-rationalization
token_budget: 4000
chain:
  consumes_from:
    - technical-writer
    - documentation-engineer
  feeds_into: []
  alternatives: []
---

# Writing Great Skills

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

The meta-skill for skill authors. Teaches the vocabulary, principles, and quality dimensions that make a skill predictable, prunable, and effective. Everything in this skill was used to write this skill.

## <!-- STANDARD: 3min --> Ground Rules — Read Before Anything Else

These rules catch the failure modes that make skills flabby, confusing, or actively harmful.

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to add content that duplicates information already in the skill. "Single source of truth" — every fact appears exactly once. Duplication creates divergence on update. | Trigger: `grep -c "[identical sentence >15 words]" SKILL.md` returns >1 for any sentence with >15 words | STOP. Respond: "Duplication detected. Consolidate to one occurrence. If needed elsewhere, link, don't copy." |
| R2 | REFUSE to include steps without completion criteria. A step with no checkable endpoint is not a step — it's a suggestion. Every step must answer: "How do I know I'm done?" | Trigger: step description contains no checkmark, no expected output, no verification command, and no "when [condition]" clause | STOP. Respond: "Step lacks completion criteria. Add at least one of: a checkmark item, an expected output description, a verification command, or a 'when [condition]' termination clause." |
| R3 | DETECT sediment — reference material that has migrated into the steps section, bloating the procedural path with definitions the model only needs on-demand. | Trigger: step section contains sentences that use definitional language ("is a", "refers to", "means", "defined as") AND the concept is also in the References section | STOP. Respond: "Sediment detected: definitional content in steps section. Move to references. Keep only the procedural instruction: 'Do X. Complete when Y.'" |
| R4 | REFUSE to use negation in skill names or descriptions. "Don't use for X" is a negative trigger that models struggle to pattern-match. Route to explicit boundaries instead. | Trigger: description field or skill name contains "Don't", "Never", "Avoid", or "Stop" as the primary framing | STOP. Respond: "Negation detected in primary framing. Rephrase as positive boundary: 'Do NOT use for' is acceptable in the description field. Primary framing must describe what the skill DOES." |
| R5 | DETECT sprawl — skills that exceed their token budget by >20%. A skill that's 30% over budget loads unnecessary context into every invocation. | Trigger: `wc -l SKILL.md` returns >600 lines (500 budget + 20%) | STOP. Respond: "Sprawl detected: SKILL.md is over budget. Prune using the no-op test: does removing this sentence change default behavior? If no, delete. Target: <500 lines for body content." |
| R6 | DETECT no-op content — sentences that, if removed, change nothing about what the model actually does. "Remember to write clean code" changes zero behavior. | Trigger: sentence passes the no-op test: if deleted, model behavior is identical | STOP. Respond: "No-op content detected. This sentence does not change default model behavior. Replace with a concrete constraint or delete." |
| R7 | REFUSE to describe process in the description field. The description field describes triggers — what situation to use the skill in. Process belongs in Core Workflow. | Trigger: description contains procedural language ("first", "then", "step", "start by", "followed by") | STOP. Respond: "Process language detected in description field. Description must describe only TRIGGERS. Move procedural content to Core Workflow. Format: 'Use when [triggers]. Handles [capabilities]. Do NOT use for [boundaries].'" |
| R8 | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| R9 | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |

## The Expert's Mindset

You are a skill architect. Your job is to encode expertise into tokens that reliably produce expert behavior. Every word you write costs context budget. Every sentence you don't write saves it.

* **The model is the user, not the human.** Skills are read by AI agents, not humans. Write for pattern-matching, not skimming. Structure trumps prose. Tables beat paragraphs. Decision trees beat explanation.
* **Tokens are budget, not free.** A 500-line skill costs ~4,000 tokens every time it's invoked. A sentence that saves 1 token but costs 50 tokens to include is a net loss. Prune ruthlessly.
* **Predictability beats cleverness.** A skill that works the same way every time is more valuable than one that's sometimes brilliant and sometimes confused. Structure enforces predictability.
* **Progressive disclosure is the architecture.** The model should see steps first, reference second, external links third. Each layer is progressively more expensive to load. Push material outward.
* **Anti-rationalization is design.** Models rationalize away constraints. "I'll just handle this edge case" becomes scope creep. Anti-rationalization tables preemptively counter these with excuse-reality pairs.

## Operating at Different Levels

* **Skill audit (15 min):** Run quality dimensions against an existing skill: is description triggers-only? Are steps checkable? Is reference material in references? Is there duplication? Are there no-op sentences?
* **Skill edit (30 min):** Fix one failure mode in an existing skill. Prune sediment, add completion criteria to steps, rewrite description to triggers-only format, remove no-op content.
* **Skill composition (45 min):** Design how 2+ skills interact. User-invoked skill orchestrates model-invoked skills. Define handoff artifacts, coordination points, and invocation conditions.
* **New skill (2-4 hours):** Full authoring cycle: define triggers and boundaries, design information hierarchy, write steps with completion criteria, push reference material outward, add anti-rationalization tables, test for failure modes.

## <!-- QUICK: 30s --> When to Use

Use writing-great-skills when the quality of skill authoring directly affects agent behavior.

* Writing a new skill from scratch — follow the full authoring cycle
* Editing an existing skill that produces inconsistent or wrong results
* Auditing a skill collection for quality: duplication, sediment, sprawl, no-op content
* Designing skill composition: which skills are user-invoked, which are model-invoked, how they coordinate
* Debugging a skill that fires when it shouldn't (description problem) or doesn't fire when it should (trigger problem)
* Pruning a skill that has grown beyond its token budget

Do NOT use writing-great-skills for writing code documentation, API docs, user manuals, or README files (route to technical-writer or documentation-engineer). Do NOT use for writing prompts that aren't structured as skills.

## <!-- QUICK: 30s --> Route the Request

### Auto-Route by Artifacts

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("SKILL.md", "Use when")` AND `file_contains("SKILL.md", "Handles")` AND `file_contains("SKILL.md", "Do NOT use")` | Description format looks correct → Jump to **Decision Trees: Description Audit** |
| A2 | `file_contains("SKILL.md", "^## Ground Rules")` AND NOT `file_contains("SKILL.md", "Mechanical Trigger")` | Ground rules missing mechanical triggers → Jump to **Decision Trees: Ground Rules Audit** |
| A3 | `wc -l SKILL.md` > 500 (body only, after frontmatter) | Skill over token budget → Jump to **Decision Trees: Pruning Strategy** |
| A4 | `file_contains("SKILL.md", "chain:")` AND `file_contains("SKILL.md", "consumes_from:")` | Skill composition analysis → Jump to **Decision Trees: Composition Audit** |
| A5 | No SKILL.md found, user wants to create a skill | Fresh authoring → Go to **Core Workflow: Phase 1 — Skill Blueprint** |

### Intent Route (Ask the User)

```
What skill authoring task are you working on?
|-- Writing a brand new skill → Start at "Core Workflow: Phase 1"
|-- Editing/improving an existing skill → Jump to "Decision Trees: Failure Mode Diagnosis"
|-- Auditing multiple skills for quality → Jump to "Decision Trees: Quality Audit"
|-- Designing how skills compose together → Jump to "Decision Trees: Composition"
|-- Debugging a skill that fires wrong → Jump to "Decision Trees: Description Debugging"
|-- Pruning a skill that's over token budget → Jump to "Decision Trees: Pruning Strategy"
```

## <!-- STANDARD: 3min --> Core Workflow

### Phase 1: Skill Blueprint

Define what the skill does before writing a single line.

```
1. DEFINE TRIGGERS (not process)
   |-- "Use when [situation 1]; [situation 2]; or [situation 3]."
   |-- Triggers are EXTERNAL situations the user encounters, not INTERNAL steps the skill takes
   |-- Test: Can the user recognize this situation WITHOUT knowing how the skill works?

2. DEFINE CAPABILITIES (what the skill handles)
   |-- "Handles [capability 1], [capability 2], and [capability 3]."
   |-- Capabilities are the tasks the skill performs, listed as nouns/gerunds

3. DEFINE BOUNDARIES (what the skill routes away)
   |-- "Do NOT use for [boundary 1] (route to [other-skill])."
   |-- Each boundary MUST name a specific alternative skill

4. DRAFT THE DESCRIPTION (one paragraph)
   |-- Format: "Use when [triggers]. Handles [capabilities]. Do NOT use for [boundaries]."
```

### Phase 2: Design the Information Hierarchy

Structure the skill for progressive disclosure.

```
1. STEPS (in-skill, high priority, always loaded)
   |-- Procedural: "Do X. Complete when Y."
   |-- Ordered, checkable, exhaustive for the primary workflow
   |-- Every step has a completion criterion

2. REFERENCE (in-skill, low priority, loaded on-demand)
   |-- Definitions, rules, tables the model consults when needed
   |-- Ground Rules, Gotchas, Verification checklists live here

3. EXTERNAL (out-of-skill, loaded only when explicitly referenced)
   |-- Linked reference files in references/ directory
   |-- Detailed guides, templates, examples, calculators
```

### Phase 3: Write Steps with Completion Criteria

```
1. WRITE THE PRIMARY WORKFLOW (Core Workflow section)
   |-- Ordered phases: Phase 1 → Phase 2 → Phase 3
   |-- Each phase: numbered steps within a code block or step diagram
   |-- Each step: action + completion criterion

2. ADD DECISION TREES (Decision Trees section)
   |-- 3+ decision trees covering common branching decisions
   |-- ASCII-art tree format preferred
   |-- Each leaf is an ACTION or ROUTE to another section

3. ADD ROUTING LOGIC (Route the Request section)
   |-- Auto-Route: filesystem condition → immediate action
   |-- Intent Route: user question → directed jump to section
```

### Phase 4: Add Anti-Rationalization

Preempt the model's tendency to rationalize away constraints.

```
1. GROUND RULES TABLE
   |-- Columns: Negative Constraint | Mechanical Trigger | Violation Response
   |-- Negative constraints: things the model MUST NOT do
   |-- Mechanical triggers: grep-able conditions that detect violations
   |-- 5-7 rules covering the most dangerous failure modes

2. GOTCHAS SECTION
   |-- Each gotcha: situation → consequence → dollar cost → fix
   |-- Dollar quantification makes the cost concrete ($X-$Y in timeframe)
   |-- Minimum 5 gotchas, each with a specific dollar range

3. PROACTIVE TRIGGERS TABLE
   |-- Conditions that fire automatically
   |-- Each trigger: detectable condition → automatic response
```

## <!-- STANDARD: 3min --> Decision Trees

### Failure Mode Diagnosis

```
                     ┌──────────────────────┐
                     │ Skill producing wrong     │
                     │ or inconsistent output    │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼──────────┐
                     │ Boundary violation?      │
                     └──────┬─────────┬───────┘
                            │YES       │NO
                            ▼          ▼
                     ┌──────────┐ ┌──────────────────┐
                     │ FIX:      │ │ Ordering violation?   │
                     │ Add       │ └──────┬─────────┬─────┘
                     │ boundary  │        │YES       │NO
                     └──────────┘        ▼          ▼
                                   ┌──────────┐ ┌──────────────────┐
                                   │ FIX: Add  │ │ No-op (model does    │
                                   │ completion│ │ nothing)?            │
                                   │ criteria  │ └──────┬─────────┬─────┘
                                   └──────────┘        │YES       │NO
                                                       ▼          ▼
                                                ┌──────────┐ ┌──────────────────┐
                                                │ FIX:      │ │ Sprawl (too much)?  │
                                                │ Widen     │ └──────┬─────────┬─────┘
                                                │ triggers  │        │YES       │NO
                                                └──────────┘        ▼          ▼
                                                              ┌──────────┐ ┌──────────┐
                                                              │ FIX:      │ │ ESCALATE │
                                                              │ Prune,    │ │ Unknown  │
                                                              │ add scope │ │ mode     │
                                                              └──────────┘ └──────────┘
```

### Pruning Strategy

```
                     ┌──────────────────────┐
                     │ SKILL.md > 500 lines    │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼──────────┐
                     │ Run no-op test: if       │
                     │ removed, does behavior   │
                     │ change?                  │
                     └──────┬─────────┬───────┘
                            │YES       │NO
                            ▼          ▼
                     ┌──────────┐ ┌──────────┐
                     │ KEEP      │ │ DELETE    │
                     └──────────┘ └──────────┘

                     Still over budget?
                     → Identify sediment: definitions in steps
                     → Move to references/
                     → Still over? Merge similar Ground Rules
```

### Description Debugging

```
                     ┌──────────────────────┐
                     │ Skill fires when it       │
                     │ SHOULDN'T                 │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼──────────┐
                     │ Process language in       │
                     │ description?              │
                     └──────┬─────────┬───────┘
                            │YES       │NO
                            ▼          ▼
                     ┌──────────┐ ┌──────────────────┐
                     │ FIX:      │ │ Overlapping triggers │
                     │ Rewrite to│ │ with another skill?  │
                     │ triggers- │ └──────┬─────────┬─────┘
                     │ only      │        │YES       │NO
                     └──────────┘        ▼          ▼
                                   ┌──────────┐ ┌──────────────────┐
                                   │ FIX:      │ │ Missing "Do NOT     │
                                   │ Narrow    │ │ use" boundaries?    │
                                   │ trigger   │ └──────┬─────────┬─────┘
                                   └──────────┘        │YES       │NO
                                                       ▼          ▼
                                                ┌──────────┐ ┌──────────┐
                                                │ Widen     │ │ ADD      │
                                                │ boundaries│ │ boundaries│
                                                └──────────┘ └──────────┘
```

### Composition Audit

```
                     ┌──────────────────────┐
                     │ Skill references other     │
                     │ skills in chain/body       │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼──────────┐
                     │ User-invoked or          │
                     │ model-invoked?           │
                     └──────┬─────────┬───────┘
                            │          │
                     ┌──────┘          └──────┐
                     ▼                       ▼
              ┌──────────────┐        ┌──────────────┐
              │ USER-INVOKED  │        │ MODEL-INVOKED  │
              │ Cost: cognitive│       │ Cost: context  │
              │ load. Zero     │       │ budget.        │
              │ context when   │       │ Autonomous     │
              │ not used.      │       │ invocation.    │
              └──────┬─────────┘        └──────┬─────────┘
                     │                        │
              ┌──────▼─────────┐       ┌──────▼─────────┐
              │ Orchestrates    │       │ Trigger narrow   │
              │ model-invoked?  │       │ enough?          │
              └──┬─────────┬────┘       └──┬─────────┬────┘
                │YES       │NO            │YES       │NO
                ▼          ▼              ▼          ▼
         ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
         │ GOOD      │ │ Consider  │ │ GOOD     │ │ Narrow    │
         │ Clear     │ │ model-    │ │          │ │ trigger or│
         │ orchest-  │ │ invoked?  │ │          │ │ raise to  │
         │ ration    │ └──────────┘ │          │ │ user-     │
         └──────────┘              └──────────┘ │ invoked   │
                                                └──────────┘
```

### Quality Audit

Score each skill 0-1 on 12 dimensions:

```
[ ] DESCRIPTION: Triggers only. "Use when / Handles / Do NOT use" format.
[ ] BOUNDARIES: Every boundary names an alternative skill.
[ ] GROUND RULES: 5-7 negative constraints with mechanical triggers.
[ ] STEPS: Every step has completion criteria.
[ ] DECISION TREES: 3+ trees covering branching decisions.
[ ] GOTCHAS: 5+ gotchas with dollar-quantified costs.
[ ] NO-OP SCORE: <5% of sentences pass the no-op test.
[ ] DUPLICATION: Zero sentences >15 words appearing more than once.
[ ] SEDIMENT: Zero definitional content in steps sections.
[ ] TOKEN BUDGET: Body content <500 lines.
[ ] PORTABILITY: Portability target declared.
[ ] REFERENCES: 8 linked reference files, all links resolve.

Target: 10+ for "great", 8+ for "good", <8 needs work.
```

## Cross-Skill Coordination

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `technical-writer` | Documentation standards, clarity principles, audience analysis | Before writing skill documentation for end users |
| `documentation-engineer` | Doc infrastructure, automation pipelines, format standards | When building automated skill validation or generation pipelines |
| `teach` | Learning principles, scaffolding patterns, assessment design | When designing a skill that teaches other skills |

| Scenario | Coordinate With | Why |
|----------|----------------|-----|
| Writing a skill about a technical domain | That domain's skill | Domain expert defines what; writing-great-skills defines how to encode it |
| Auditing a skill collection | All skills in the collection | Quality audit against the 12 dimensions |
| Designing skill composition | The skills being composed | Defines orchestration pattern, handoff artifacts, invocation conditions |

## Error Recovery

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Skill fires on wrong triggers or doesn't fire when it should | Description field contains process language ("first", "then", "step") instead of trigger-only language | Rewrite description using ONLY trigger conditions. Test: can a user recognize the situation WITHOUT knowing how the skill works? | **Process in description = misfire.** Descriptions are grep-matched by agents. Process words match random conversations. Trigger words match specific situations. |
| Agent ignores a ground rule during execution | The ground rule lacks a Mechanical Trigger — a grep-able condition the agent can detect | Every ground rule must have: (1) a negative constraint, (2) a mechanical trigger (grep-able), and (3) a violation response (exact text). Without all three, the rule is aspirational, not enforced | **Rules without mechanical triggers are wishes.** Agents cannot enforce "be careful." They CAN enforce "if grep finds X, respond with Y." |
| Skill exceeds 500 lines but all content seems necessary | Sediment: reference material that crept into the skill body instead of staying in reference files | Run the no-op test on every paragraph: "If I delete this, does a specific agent behavior change?" If no, move to references or delete. Dollar-quantify gotchas to make failure costs visible | **Every line costs tokens.** A 600-line skill costs 20% more per invocation. Prune sediment first, then push detail to reference files. |
| Agent completes work but produces wrong output format | Skill defines what to DO but not what COMPLETION looks like | Every phase must end with a completion criterion: a checkable condition the agent can verify. | **Without completion criteria, agents don't know when they're done.** Every step needs a verifiable exit condition. |

## State Log

This skill maintains a **decision ledger** for skill authoring sessions.

### How the State Log Works

1. **On session start:** Check `.copilot/session-state/decision-ledger.json` for prior authoring decisions.
2. **After each major decision:** Record skill architecture choices, section placement, and token budget allocations.
3. **Before completing work:** Verify all structural decisions are documented.
4. **On context recovery:** Read the last 5 entries before proposing changes.

### Anti-Drift Check

- [ ] Have I read the state log from the previous session?
- [ ] Do any prior section-placement or budget decisions constrain what I'm about to do?
- [ ] Is my approach consistent with the 12-section template?
- [ ] If I'm contradicting a prior decision, have I documented WHY?

## Proactive Triggers

| # | Trigger Condition | Auto-Response |
|---|------------------|---------------|
| P1 | `grep -c "^## " SKILL.md` returns <12 | [ALERT] Skill missing required sections. Map against the 12-section template. |
| P2 | `grep -c "Mechanical Trigger" SKILL.md` returns 0 | [FAIL] Ground rules lack mechanical triggers. Every constraint needs a grep-able detection condition. |
| P3 | `wc -l SKILL.md | awk '{print $1}'` > 600 | [WARN] Skill >20% over token budget. Run no-op test and sediment check. |
| P4 | Description contains "first", "then", "step", "start by" | [FIX] Process language in description. Rewrite to triggers-only format. |
| P5 | `grep -c '\$[0-9]' SKILL.md` < 5 | [WARN] Fewer than 5 dollar-quantified gotchas. Quantify the cost of each failure mode. |
| P6 | Reference link count < 8 | [FIX] Insufficient references. Push material outward: 8 linked reference files minimum. |

## What Good Looks Like

### Before (Novice Skill)
```markdown
# My Skill
This skill helps you do things.

## How to Use
1. Figure out the problem
2. Solve it
3. Check your work

## Tips
- Write clean code
- Remember to test
```

Problems: No triggers, no boundaries, no completion criteria, no-op tips, no ground rules, no gotchas, no decision trees, no references.

### After (Great Skill)
```markdown
---
name: example-skill
description: >
  Use when [trigger]. Handles [capabilities].
  Do NOT use for [boundary] (route to [other-skill]).
---

# Example Skill
> **Portability target:** Spec-level.

## Ground Rules — Read Before Anything Else
| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to [bad action]... | Trigger: [grep-able condition] | STOP. "[exact response]" |

## Core Workflow
### Phase 1: [Name]
1. DO [action]. |-- Complete when [checkable condition].

## Decision Trees
### [Tree Name]
[ASCII tree with leaf actions]

## Gotchas
- **[Gotcha].** **Total cost: $X-$Y.** Fix: [action].

## Verification Guardrails

Before delivering work, the agent must verify:

- [ ] **Self-check against What Good Looks Like:** All deliverables meet the quality bar defined above
- [ ] **No broken references:** All file paths, URLs, and skill references resolve correctly
- [ ] **Continuity with State Log:** No prior decisions contradicted without documented rationale
- [ ] **Anti-hallucination check:** No fabricated APIs, version numbers, or capabilities asserted
- [ ] **Error Recovery paths exercised:** Failure modes documented and recovery steps tested
- [ ] **Cross-skill dependencies satisfied:** All upstream skill outputs consumed as documented

If any checkbox fails, revise before delivering. When all pass, add to the state log.

## References
* ref-example.md
```

## Deliberate Practice

### Exercise 1: Trigger vs Process Audit (10 min)
Take 5 existing skills. Read only their description fields. For each: can you tell WHEN to invoke the skill without knowing HOW it works? Rewrite any process-disguised-as-trigger descriptions.

### Exercise 2: No-Op Elimination (15 min)
Take one of your own skills. For every sentence: "If I delete this, does the model's behavior change?" Mark KEEP or DELETE. Calculate no-op score: DELETE / total. Target: <5%.

### Exercise 3: Sediment Mining (15 min)
Scan a skill's Core Workflow and Decision Trees. Flag every definitional sentence. Move them to references/. How many lines recovered?

### Exercise 4: Mechanical Trigger Workshop (20 min)
For each Ground Rule in a skill, write a grep command that would detect the violation. Test each grep on sample output. Unenforceable rules → rewrite.

### Exercise 5: Skill Compression (20 min)
Take a 700-line skill. Run no-op elimination, sediment mining, and merge similar Ground Rules. Can you get it under 500 lines without losing functionality?

### <!-- DEEP: 10+min --> Error Decoder

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| The description-as-process anti-pattern. Description fields read as process-triggers ("Use when you need to calculate a budget") rather than situation-triggers | The model matches on the situation, not the process. A skill with process-triggers fires late or not at all | Describe the SITUATION the user is in, not the task the skill performs. "Use when the user mentions money," not "Use when you need to calculate a budget" | **$0 in direct cost but infinite in missed utility** — the skill never fires when it should. Process-triggers are invisible to the model's situation-matching. |
| The duplication divergence trap. Two sections that both explain a concept will diverge within 3 edits | The model reads contradictory information and behavior becomes random. Divergent copies create inconsistent output | Every concept appears exactly once. References link to the authoritative definition. Run `grep -c` to detect repeated sentences >15 words | **$5,000-$20,000 in debugging inconsistent model behavior.** Duplication guarantees divergence on update; single-source-of-truth prevents it. |
| The premises-completion failure mode. Skills complete after step 1 because step 1 produces output that looks like a valid completion | The model rationalizes: "I identified the problem, task complete." Remaining 6 steps are never reached | Every step must have a completion criterion requiring an artifact or state visibly incomplete until the full workflow finishes | **$500-$5,000 per occurrence in wasted sessions.** Completion criteria prevent premature termination by making incompleteness visible. |
| The no-op inflation death spiral. Skills accumulate "advice sentences" that add no behavioral change | Advice sentences cost tokens but change zero behavior. Accumulated over revisions, half the skill becomes dead weight | Run the no-op test on every sentence during every revision: "If deleted, does model behavior change?" If no, delete | **2,000+ wasted tokens per invocation. At 10 invocations/day, 20,000 tokens/day of zero-value context.** No-op sentences are pure context waste with no behavioral impact. |
| The ground-rules-without-teeth problem. A ground rule without a mechanical trigger is unenforceable | The model reads the rule, nods, and proceeds to not follow it. Without detection, rules are suggestions, not constraints | Every ground rule must include a grep command or filesystem check that detects the violation. Enforceable rules have triggers | **$10,000-$100,000 in security incidents from skills with unenforceable rules.** Mechanical triggers turn suggestions into enforceable constraints. |
| The composition confusion problem. A skill lists multiple sub-skills without an orchestration pattern | The model invokes all sub-skills simultaneously — 5x context budget and conflicting outputs | Specify orchestration pattern in chain section: sequential vs parallel vs conditional. Define handoff artifacts between skills | **$2-$50 per invocation in excess API costs, plus $200-$2,000 in engineer time reconciling conflicts.** Explicit orchestration prevents context explosion. |

## <!-- DEEP: 10+min --> Anti-Rationalization — No Excuses

| Rationalization | Reality |
|----------------|---------|
| "The skill is clear to me, so the model will understand it" | Models don't share your context; instructions that feel obvious to you are ambiguous to an LLM with zero prior knowledge of your intent |
| "I'll add examples later, the rules are enough" | Rules without examples are guidelines the model rationalizes away; one concrete counterexample prevents 10 misinterpretations |
| "Longer skills are more thorough" | Skills over 500 lines suffer from context dilution; the model forgets early instructions by the time it reads later ones |
| "If the model violates a rule, I'll add a stronger warning" | Stronger language doesn't work; only mechanical triggers (grep checks, filesystem verification) change model behavior |
| "This edge case is so obvious I don't need to document it" | The undocumented edge case is the one the model hits at 3 AM in production; every observed failure pattern must be encoded |

## <!-- DEEP: 10+min --> Verification

- [ ] **Description audit:** "Use when / Handles / Do NOT use" format. No process language. Triggers are situations.
- [ ] **Ground rules enforceable:** Every ground rule has a mechanical trigger.
- [ ] **Steps have completion criteria:** Every Core Workflow step has a checkable endpoint.
- [ ] **No duplication:** Zero sentences >15 words appearing more than once.
- [ ] **No-op score <5%:** DELETE count / total sentences < 0.05.
- [ ] **Zero sediment:** No definitional sentences in Core Workflow or Decision Trees.
- [ ] **Token budget:** Body content <500 lines.
- [ ] **References resolve:** All 8 reference links point to existing files.
- [ ] **Portability:** Portability target declared. No vendor-specific frontmatter.
- [ ] **Verification script passes:** Run `scripts/verify-skill.sh`.

## References

* [information-hierarchy.md](references/information-hierarchy.md) — The information hierarchy ladder: steps → reference → external, progressive disclosure architecture
* [steps-vs-reference.md](references/steps-vs-reference.md) — Distinguishing procedural steps (ordered, checkable) from reference material (on-demand, definitional)
* [leading-words.md](references/leading-words.md) — Compact pretrained concepts (red-green-refactor, tracer bullet, tight loop) for token-efficient anchoring
* [failure-modes.md](references/failure-modes.md) — Catalog of 6 skill failure modes: premature completion, duplication, sediment, sprawl, no-op, negation
* [pruning-discipline.md](references/pruning-discipline.md) — The no-op test, single source of truth principle, and systematic pruning workflow
* [invocation-strategy.md](references/invocation-strategy.md) — User-invoked vs model-invoked: cost tradeoffs, orchestration patterns, invocation conditions
* [description-design.md](references/description-design.md) — Writing descriptions that are triggers-only with boundary specification and routing
* [anti-rationalization-tables.md](references/anti-rationalization-tables.md) — Designing anti-rationalization tables with excuse-reality pairs that preempt model rationalizations

