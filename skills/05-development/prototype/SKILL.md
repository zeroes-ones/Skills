---
name: prototype
description: >
  Use when a design question has no clear answer and needs empirical evidence; when comparing
  two approaches and static analysis is inconclusive; when exploring an unfamiliar API or library
  before committing; or when a team is debating implementation trade-offs without data. Handles
  rapid throwaway prototype construction, single-question isolation (one prototype answers one
  question), time-boxed experimentation (20 min max), git-worktree isolation for clean disposal,
  decision documentation from prototype results, and empirical evidence collection. Do NOT use
  for production feature implementation (route to appropriate developer skill), writing tests
  (route to qa-engineer), API design (route to api-designer), or performance benchmarking
  (route to performance-engineer).
author: Sandeep Kumar Penchala
license: MIT
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
type: development
status: stable
version: 1.0.0
updated: 2026-07-23
tags:
  - prototype
  - throwaway
  - experimentation
  - empirical-evidence
  - time-boxed
  - spike
  - isolation
token_budget: 3500
chain:
  consumes_from:
    - brainstorming
    - system-architect
    - fullstack-developer
  feeds_into:
    - fullstack-developer
    - backend-developer
    - frontend-developer
  alternatives:
    - source-driven-development
---

# Prototype

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Build the smallest possible working prototype to answer exactly ONE design question, then throw it away. Never ship prototype code. Use git-worktree or temp directory for isolation. Time-box to 20 minutes maximum. The output is not code — it is a decision with empirical evidence.

## Ground Rules — Read Before Anything Else

These rules prevent prototype code from becoming production code and ensure experiments answer questions rather than create them.

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to answer more than ONE question per prototype. A prototype that tries to answer multiple questions answers none of them well — the evidence is confounded and the decision remains unclear. | Trigger: prototype scope document lists > 1 question to answer OR prototype code addresses multiple independent concerns | STOP. "One prototype, one question. Which question is the highest priority? We'll answer that one with this prototype. The other questions get their own prototypes." |
| R2 | REFUSE to let prototype code enter the production codebase. Prototype code is scaffolding — it has no tests, no error handling, no edge case coverage. It is correct enough to answer a question, not correct enough to ship. | Trigger: user mentions "saving this code", "building on top of this", "this is close to production-ready", or copies prototype files into the main source tree | STOP. "HARD GATE: Prototype code never ships. It answers a question, then it is deleted. Saving prototype code means shipping code that was designed for exploration, not correctness. Start fresh with production-quality code informed by what we learned." |
| R3 | DETECT and PREVENT the "I'll just clean this up later" rationalization. Prototype code that is "good enough to keep" is the #1 source of production defects that trace back to experimental scaffolding. | Trigger: user says "this is almost production-ready", "I'll just clean it up", "we can iterate on this", or "it's working, why rewrite?" | STOP. "Prototype code has hidden costs: missing error handling, untested edge cases, hardcoded values. Rewriting from scratch with production discipline costs 20% more than iterating on a prototype but eliminates 80% of the defect sources. Delete the prototype. Build the real version." |
| R4 | REFUSE to exceed the 20-minute time box. If the question cannot be answered in 20 minutes of coding, the question is too broad — split it into smaller questions. | Trigger: prototype has been running > 20 minutes AND the design question remains unanswered | STOP. "Time box expired. The question is too broad for a single prototype. What sub-question can we answer in 20 minutes? Split: [narrower question A], [narrower question B]. Pick one." |
| R5 | REFUSE to prototype without a clear falsifiable hypothesis. "Let's just play with the API" is exploration, not prototyping. A prototype tests a specific claim: "Approach X will work for our use case because Y." | Trigger: user cannot state the hypothesis as "We believe [X] because [Y]. The prototype will disprove this if [Z] happens." | STOP. "A prototype without a hypothesis is play, not experimentation. State the hypothesis: 'We believe [specific approach] will work because [reasoning]. The prototype will disprove this if [falsifiable condition].' Without this, we cannot interpret the results." |
| R6 | REFUSE to prototype in the main working directory. Prototype isolation is non-negotiable — use git-worktree or a temp directory outside the main source tree. | Trigger: prototype files created in the main source tree (not in a git-worktree, not in a /tmp-equivalent-isolated directory) | STOP. "Prototype must be isolated. Use `git worktree add ../proto-experiment` or create a temp directory. Isolation prevents accidental contamination of the main codebase and makes disposal clean — delete the directory, the prototype is gone." |
| R7 | DETECT when prototype results are being over-interpreted. A 20-minute prototype proves ALMOST NOTHING about production behavior. It answers "is this approach viable?" not "is this approach production-grade?" | Trigger: user draws conclusions about performance, scalability, reliability, or security from prototype results | WARN. "A 20-minute prototype measures viability, not production characteristics. Performance numbers from a prototype are off by 2-10x. Scalability claims are untested. Reliability is nonexistent. Use these results ONLY to decide whether to invest in a real implementation — not to claim production readiness." |

## The Expert's Mindset

You are an experimentalist who treats every prototype as a disposable scientific instrument. Your mental model:

* **The prototype is a question, not a product.** Every line of code in a prototype exists to answer a question. When the question is answered, the code has no further purpose. Treating prototype code as an asset is like keeping the questionnaire after the survey is complete.
* **Speed beats correctness.** A prototype that takes 2 hours to write is a failed prototype — it should have been split into smaller questions. Prioritize getting to the answer over getting the code right. Hardcoded values, mocked dependencies, and copy-pasted snippets are not just acceptable — they are required.
* **Isolation is discipline, not inconvenience.** The purpose of git-worktree isolation is not to make your life harder — it is to make disposal automatic. If prototype code is in the same directory as production code, it will survive. If it is in a separate directory, `rm -rf` solves the problem.
* **The answer matters, not the code.** The output artifact of prototyping is a decision document, not a codebase. If you spend more time writing the decision document than writing the prototype, you probably built too much prototype.

### What Masters Know That Others Don't

- **That 20 minutes is the correct unit of prototyping** — longer than 20 minutes and you're building, not experimenting. Shorter and you haven't given the question enough time to reveal its answer.
- **The anti-shipping pattern catalog** — every prototype that became production code followed the same 5-step path: "this is close" → "I'll clean it up" → "we need to ship" → "we'll refactor later" → production incident.
- **When a prototype reveals the question was wrong** — the best prototype outcome is "this approach won't work." It saves you from building the wrong thing. Celebrate negative results — they are more valuable than positive ones because they eliminate paths.

## Operating at Different Levels

| Level | Scope | You... |
|-------|-------|--------|
| **L1** | Single API call or library function | 5-minute prototype. Test one function call with one input. Answer: "Does this API do what we think?" |
| **L2** | Feature spike or approach comparison | Full 20-minute prototype. Test one design question with working (but throwaway) code. Answer: "Is Approach A viable?" |
| **L3** | Architecture spike across components | 2-3 linked 20-minute prototypes. Each answers a sub-question. Produce decision document synthesizing results. |
| **L4** | Technology evaluation (new framework, database, platform) | Multi-session prototyping with comparison matrix. Coordinate with system-architect for evaluation criteria. |
| **L5** | Organizational practice | Define prototyping standards, time-box discipline, and disposal protocols. Train teams on hypothesis-driven experimentation. |

**Default level for this skill:** L2

## When to Use

- Two approaches seem equally valid and static analysis cannot decide between them
- Exploring an unfamiliar API, library, or framework before committing to it in the architecture
- A team debate about implementation trade-offs has no data — "it depends" without evidence
- A design question emerged from brainstorming that needs empirical resolution
- Before writing a complex algorithm — prototype the core logic to verify the approach
- When a stakeholder asks "how long would X take?" and you need a spike to estimate

### When NOT to Use

- Production feature implementation (route to appropriate developer skill)
- Writing test suites (route to qa-engineer)
- Performance benchmarking with statistical rigor (route to performance-engineer)
- API contract design (route to api-designer)
- Security testing or penetration testing (route to security-reviewer)
- Code that will be needed for more than 20 minutes (that's implementation, not prototyping)

## Route the Request

### Auto-Route by Context

| # | Condition | Action |
|---|-----------|--------|
| A1 | User asks "should we use X or Y?" with no code yet | Go to **Core Workflow** — Phase 1 (Form Hypothesis) |
| A2 | User has a specific design question ("can we use library X for our use case?") | Go to **Core Workflow** — Phase 2 (Build) |
| A3 | User built a prototype and is asking "what now?" | Jump to **Decision Trees: Disposal Protocol** |
| A4 | User is debating with their team about an approach | Jump to **Decision Trees: Approach Comparison** |
| A5 | User is exploring a new technology/library/API | Go to **Core Workflow** — Phase 1 (scope the question tightly) |
| A6 | User says "I just want to see if this works" | Go to **Core Workflow** — Phase 1. Extract the hypothesis first. |

### Intent Route

```
What are you trying to do?
├── ANSWER a specific design question with code → Start at "Core Workflow" — Phase 1
├── COMPARE two approaches empirically → Jump to "Decision Trees > Approach Comparison"
├── EXPLORE an unfamiliar API/library → Go to "Core Workflow" — Phase 1 (tight scope)
├── DISPOSE of a prototype properly → Jump to "Decision Trees > Disposal Protocol"
├── DOCUMENT what was learned from a prototype → "Core Workflow" — Phase 3
└── Not sure? → Start at "Ground Rules" then "Core Workflow"
```

## Core Workflow

### Phase 1: Form the Hypothesis

Before writing any code, define what you are testing and why.

```
1. STATE THE DESIGN QUESTION
   |-- Ask: "What is the ONE design decision this prototype will inform?"
   |-- Must be a decision, not an exploration. "Which approach is faster?" is a decision.
   |   "Let's see how this library works" is exploration — narrow it to a decision.
   |-- Output: One-sentence design question.

2. STATE THE HYPOTHESIS
   |-- Format: "We believe [Approach X] will work for our use case because [Y].
   |   The prototype will disprove this if [Z] happens."
   |-- The hypothesis must be FALSIFIABLE — there must be a clear failure condition.
   |-- Bad: "We believe Redis will work." (not falsifiable — "work" is undefined)
   |   Good: "We believe Redis Pub/Sub will deliver messages to all subscribers within
   |   50ms for payloads under 1KB. The prototype disproves this if any delivery exceeds
   |   50ms in a 3-node local setup."
   |-- Output: Falsifiable hypothesis statement.

3. SCOPE THE PROTOTYPE
   |-- Ask: "What is the MINIMUM code needed to test this hypothesis?"
   |-- Strip everything that does not directly contribute to answering the question.
   |-- No error handling (unless error behavior IS the question).
   |-- No tests (the prototype IS the test).
   |-- No configuration files, no CI/CD, no documentation beyond inline comments.
   |-- Estimate: "Can this be built in 20 minutes?" If no → split the question.
   |-- Output: Scoped prototype plan with estimated time.
```

### Phase 2: Build and Run

```
4. CREATE ISOLATED ENVIRONMENT
   |-- Option A (preferred): git worktree
   |   `git worktree add --detach ../proto-YYYY-MM-DD-[topic]`
   |-- Option B: temp directory entirely outside the repo
   |   `mkdir ~/prototypes/proto-YYYY-MM-DD-[topic] && cd $_`
   |-- Verify isolation: `git status` in main repo shows no changes.
   |-- Output: Isolated working directory.

5. BUILD THE PROTOTYPE
   |-- START A TIMER. 20 minutes. No exceptions.
   |-- Write the minimum code. Hardcoded values, mocked deps, inline everything.
   |-- At 10 minutes: check progress. Are you halfway to answering the question?
   |   If building infrastructure → you've lost focus. Return to the hypothesis.
   |-- At 18 minutes: STOP adding features. Test the hypothesis now.
   |-- At 20 minutes: TIMER DONE. Stop regardless of state.

6. TEST THE HYPOTHESIS
   |-- Run the prototype against the falsifiable condition.
   |-- Record: HYPOTHESIS CONFIRMED / HYPOTHESIS DISPROVED / INCONCLUSIVE.
   |-- Record the EVIDENCE. What numbers? What behavior? What surprised you?
   |-- If INCONCLUSIVE: the question was too broad or the prototype too narrow.
   |   Document why and what narrower question to try next.
```

### Phase 3: Decide and Dispose

```
7. DOCUMENT THE DECISION
   |-- Create a decision record in the main repo (not the prototype directory):
   |   Format: docs/decisions/YYYY-MM-DD-[topic]-prototype-result.md
   |-- Include: hypothesis, prototype approach, results, decision, evidence quality.
   |-- Evidence quality: HIGH (clear result), MEDIUM (result with caveats), LOW (inconclusive).
   |-- Output: Decision document committed to main repo.

8. DISPOSE OF THE PROTOTYPE
   |-- Option A: `git worktree remove ../proto-YYYY-MM-DD-[topic]`
   |-- Option B: `rm -rf ~/prototypes/proto-YYYY-MM-DD-[topic]`
   |-- Verify: prototype code is GONE. No trace in the main repo.
   |-- The decision document IS the artifact. The code was the instrument.
```

## Decision Trees

### Approach Comparison

```
                     ┌──────────────────────┐
                     │ Two (or more)          │
                     │ approaches to compare  │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼──────────┐
                     │ Can the comparison be  │
                     │ resolved by reading    │
                     │ docs/source?           │
                     └──────┬─────────┬─────┘
                            │YES       │NO
                            ▼          ▼
                   ┌──────────────┐ ┌──────────────────┐
                   │ Read the docs.│ │ Identify the KEY   │
                   │ No prototype  │ │ DIFFERENTIATOR:    │
                   │ needed. Decide│ │ what do these       │
                   │ now.          │ │ approaches do       │
                   └──────────────┘ │ DIFFERENTLY that    │
                                    │ matters?            │
                                    └──────┬─────────┬───┘
                                           │
                                ┌──────────▼──────────┐
                                │ Can the differentiator │
                                │ be tested in < 20 min? │
                                └──────┬─────────┬─────┘
                                       │YES       │NO
                                       ▼          ▼
                              ┌──────────────┐ ┌──────────────────┐
                              │ Build ONE      │ │ Split into N       │
                              │ prototype that │ │ smaller questions. │
                              │ exercises the  │ │ Each gets its own  │
                              │ differentiator.│ │ 20-min prototype.  │
                              │ Compare results│ └──────────────────┘
                              │ for both.      │
                              └──────────────┘
```

### Disposal Protocol

```
                     ┌──────────────────────┐
                     │ Prototype complete.    │
                     │ Hypothesis tested.     │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼──────────┐
                     │ Is the decision doc    │
                     │ committed to main repo?│
                     └──────┬─────────┬─────┘
                            │NO        │YES
                            ▼          ▼
                   ┌──────────────┐ ┌──────────────────┐
                   │ Write and      │ │ Is the prototype    │
                   │ commit the     │ │ directory isolated  │
                   │ decision doc   │ │ from main repo?     │
                   │ first. Do not  │ └──────┬─────────┬───┘
                   │ dispose without│        │YES       │NO
                   │ documentation. │        ▼          ▼
                   └──────────────┘ ┌──────────────┐ ┌──────────────────┐
                                    │ Delete the     │ │ Move prototype     │
                                    │ prototype      │ │ files to isolated  │
                                    │ directory:     │ │ directory FIRST,   │
                                    │ rm -rf or      │ │ then delete.       │
                                    │ git worktree   │ │ NEVER delete from  │
                                    │ remove.        │ │ within main tree.  │
                                    └──────────────┘ └──────────────────┘
```

### Time-Box Enforcement

```
                     ┌──────────────────────┐
                     │ Prototype started.     │
                     │ Timer: 20:00           │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼──────────┐
                     │ 10:00 check: Are you  │
                     │ building infra or     │
                     │ testing hypothesis?   │
                     └──────┬─────────┬─────┘
                            │INFRA     │HYPOTHESIS
                            ▼          ▼
                   ┌──────────────┐ ┌──────────────────┐
                   │ STOP. Return  │ │ Continue. At 18:00:│
                   │ to hypothesis. │ │ STOP adding. Test │
                   │ What is the    │ │ what you have.    │
                   │ MINIMUM code?  │ │ At 20:00: STOP    │
                   │ Split if needed│ │ regardless.       │
                   └──────────────┘ └──────────────────┘
```

### Question Scoping

```
                     ┌──────────────────────┐
                     │ Design question to     │
                     │ answer by prototype    │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼──────────┐
                     │ Can you describe the   │
                     │ MINIMUM code to test   │
                     │ this in < 3 sentences? │
                     └──────┬─────────┬─────┘
                            │YES       │NO
                            ▼          ▼
                   ┌──────────────┐ ┌──────────────────┐
                   │ Good. Estimate │ │ Question is too    │
                   │ time. If > 20  │ │ broad. Split:      │
                   │ min → split.   │ │ "What is the ONE   │
                   │ If ≤ 20 → build│ │ thing we most need │
                   └──────────────┘ │ to know?" Prototype │
                                    │ that first.         │
                                    └──────────────────┘
```

### Evidence Quality Assessment

```
                     ┌──────────────────────┐
                     │ Prototype results      │
                     │ obtained               │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼──────────┐
                     │ Was the hypothesis     │
                     │ CLEARLY confirmed or   │
                     │ disproved?             │
                     └──────┬─────────┬─────┘
                            │YES                 │NO
                            ▼                    ▼
                   ┌──────────────┐ ┌──────────────────┐
                   │ QUALITY: HIGH │ │ Were the results    │
                   │ Decision can  │ │ directionally clear │
                   │ be made with  │ │ but with caveats?   │
                   │ confidence.   │ └──────┬─────────┬───┘
                   └──────────────┘        │YES       │NO
                                           ▼          ▼
                                  ┌──────────────┐ ┌──────────────────┐
                                  │ QUALITY:      │ │ QUALITY: LOW      │
                                  │ MEDIUM        │ │ Do not make the   │
                                  │ Decision can  │ │ decision from this│
                                  │ be made with  │ │ prototype. Re-    │
                                  │ caveats noted.│ │ scope with tighter│
                                  └──────────────┘ │ question.         │
                                                   └──────────────────┘
```

## Cross-Skill Coordination

| Scenario | Coordinate With | Why |
|----------|----------------|-----|
| Prototype question emerged from brainstorming | brainstorming | Brainstorming identified the uncertainty; prototype resolves it empirically. Return decision to brainstorming. |
| Prototype tests an architectural assumption | system-architect | Architectural decisions affect system design; system-architect defines evaluation criteria for prototype |
| Prototype results inform production implementation | fullstack-developer, backend-developer, frontend-developer | Decision document hands off to developer who builds the real implementation — with empirical evidence, not guesses |
| Multiple technologies being evaluated | system-architect | System-architect provides evaluation dimensions (scalability, maintainability, team capability) |
| Prototype reveals API design implications | api-designer | API behavior discovered in prototype may inform contract design |
| Prototype involves database or data model questions | database-designer | Database behavior (query patterns, indexing, consistency) may need schema expertise |
| Prototype reveals performance characteristics | performance-engineer | If prototype shows performance concerns, escalate to proper benchmarking — prototype measurements are directional only |

## Proactive Triggers

| # | Trigger Condition | Auto-Response |
|---|------------------|---------------|
| P1 | User starts building infrastructure (config files, CI, project scaffolding) during prototype time | [ALERT] "You're building scaffolding, not testing a hypothesis. A prototype has no config files, no CI, no project structure. What is the MINIMUM code to answer the question?" |
| P2 | User mentions keeping or iterating on prototype code | [GATE] "Prototype code never ships. The decision document is the artifact. We'll dispose of the code after we document what we learned." |
| P3 | Prototype exceeds 20 minutes without answering the question | [SPLIT] "Time box exceeded. The question is too broad. What sub-question can we answer in 20 minutes? Let's scope down." |
| P4 | User draws production conclusions from prototype results | [WARN] "Prototype results are directional. Performance is 2-10x off. Reliability is untested. Use these results ONLY to decide whether to proceed — not to guarantee production behavior." |
| P5 | Prototype code appears in the main source tree | [ISOLATE] "Prototype code detected in main repo. Move to isolated directory immediately. Use git worktree or temp directory." |
| P6 | User cannot articulate the hypothesis | [REQUIRE] "A prototype without a hypothesis is exploration, not experimentation. State: 'We believe [X] because [Y]. The prototype disproves this if [Z].'" |

## What Good Looks Like

```
BEFORE (Unstructured Experimentation):
"Let's try out this new GraphQL library. I'll set up a project,
add the dependencies, configure TypeScript, set up the schema,
and build a few queries to see how it feels."
→ 3 hours later: has a half-built GraphQL server with no clear
  decision reached but plenty of code "worth keeping."

AFTER (Disciplined Prototype):
QUESTION: "Can we use graphql-yoga to replace our REST endpoints
for the user profile page, given our requirement of < 200ms
response time for queries joining 3 data sources?"

HYPOTHESIS: "We believe graphql-yoga with DataLoader batching will
resolve a 3-source user profile query in < 200ms. The prototype
disproves this if any query exceeds 200ms in local testing."

SCOPE: One schema (User + Posts + Comments), one resolver chain
using DataLoader, in-memory mock data (1000 users, 50 posts/user).

BUILD (18 min):
- 1 file: index.ts with hardcoded schema, mocked data, single query
- No TypeScript config (use ts-node --esm), no tests, no error handling
- Timer: built in 14 minutes. 4 minutes to test.

RESULT: 3-source query averaged 78ms locally. HYPOTHESIS CONFIRMED.
Caveat: local in-memory data. Real database may add latency.

DECISION: Proceed with graphql-yoga for user profile. Prototype
suggests latency target is achievable. Note: need database-benchmark
follow-up before production deployment.

DISPOSE: rm -rf ../proto-2026-07-23-graphql-yoga
Decision doc committed: docs/decisions/2026-07-23-graphql-yoga-viability.md

Total time: 22 minutes. Decision made with evidence.
```

## Deliberate Practice

### Exercise 1: Hypothesis Extraction (5 min)
Take your last 3 "I was just trying something out" coding sessions. For each, write the hypothesis you were testing. If you cannot write one, you were playing, not prototyping. Repeat until every coding session has a hypothesis.

### Exercise 2: 20-Minute Constraint Drill (20 min)
Pick a design question from your current work. Set a 20-minute timer. Build the prototype. When the timer goes off, STOP — even if it's not working. Document: did you answer the question? If not, what was too broad? Split and repeat.

### Exercise 3: Disposal Practice (5 min)
Find prototype or spike code in your current project that survived. For each file: write the decision it informed (if any), then delete it. If the code is in production, write a ticket to replace it with production-quality code. Count how many prototype files you found — this number IS your prototype discipline gap.

### Exercise 4: One-Question Discipline (10 min)
Look at a prototype you built recently. Count how many design questions it attempted to answer. If > 1, split the prototype's results: which question did it ACTUALLY answer? Which were confounded? Rewrite as separate prototype plans.

### Exercise 5: Evidence Quality Audit (15 min)
Review your last 5 prototype-based decisions. Rate each as HIGH/MEDIUM/LOW evidence quality. For LOW-quality decisions: what would a better prototype have looked like? If you made a production decision on LOW-quality evidence, flag it for revisit.

## Gotchas

- **"I'll just clean this up later" — the $500K lie.** The most expensive four words in prototyping. A fintech startup built a "prototype" payment integration to test an API. The prototype had no idempotency handling, no retry logic, and hardcoded test credentials. The PM said "ship it and we'll clean it up next sprint." Next sprint became next quarter. Six months later, a network blip caused duplicate charges. Refunds, compliance fines, and lost merchant trust: $340K. The cleanup would have taken 3 days. **Total cost: $200K-$500K per prototype-that-shipped in duplicate charges, data corruption, compliance fines, and customer trust erosion. Prevent: enforce disposal protocol. Prototype code is deleted before production code is written.**

- **The prototype that answered the wrong question.** A team prototyped WebSocket performance to answer "can we do real-time updates?" The prototype showed 10K concurrent connections with < 5ms latency. They shipped WebSockets. The real question should have been "can our mobile users on 3G in rural areas maintain WebSocket connections?" Battery drain and connection drops made the feature unusable for 60% of users. The prototype tested the wrong variable. **Total cost: $80K-$200K in misdirected development effort and feature rollback. Prevent: Phase 1, Step 1 — verify the question is what you actually need to know, not what's easiest to prototype.**

- **The prototype that became the architecture.** A team prototyped an event-driven architecture with a simple in-memory message bus to answer "does event-driven fit our mental model?" The prototype was clean and simple. They adopted the pattern but never replaced the in-memory bus with a persistent one. First production restart: all unprocessed events lost. Customer orders disappeared. The prototype's architecture choice (in-memory) was an implementation shortcut, not a design decision — but it became both. **Total cost: $50K-$150K in lost data, recovery effort, and architecture remediation. Prevent: document prototype shortcuts explicitly. "We used X as a shortcut. In production, replace with Y." The document is the bridge between prototype and production.**

- **The time-box that someone "extended by an hour."** A developer's 20-minute prototype to test a database query pattern turned into a 4-hour "deep dive" because they "were almost there." The additional 3.5 hours produced zero new information — the answer was clear at 18 minutes (the query pattern works). The extra time was spent making the prototype "nicer" — refactoring, adding comments, making it "presentable." At $150/hr, that's $525 of engineering time spent polishing throwaway code. **Total cost: $5K-$20K per year per engineer in prototype overruns from "just a few more minutes" creep. Prevent: the time box is a HARD STOP. When the timer ends, you stop typing. No exceptions. No "one more minute."**

- **The two-questions-in-one-prototype trap.** A team prototyped "can we use Kafka for both event streaming AND request-response patterns?" The prototype mixed both use cases. Kafka worked for streaming but the request-response pattern required unnatural workarounds. The team couldn't separate the results — the streaming success masked the request-response failure. They shipped Kafka for both, and the request-response system required a $65K rewrite to REST 8 weeks later. **Total cost: $30K-$100K per confounded prototype in reimplementation cost. Prevent: one question per prototype. ALWAYS. If you have two questions, you have two prototypes.**

- **The "the docs say it works, we don't need a prototype" assumption.** A team read the Stripe Connect docs and decided it would work for their multi-vendor marketplace. Skip the prototype, start building. Two sprints in, they discovered Stripe Connect's onboarding flow required every vendor to have a US bank account — 40% of their vendors were international. The assumption "docs imply it works for us" cost $120K in wasted development and a 6-week delay while they switched to a different payment provider. **Total cost: $40K-$150K per skipped prototype based on documentation assumptions. Prevent: docs describe what an API CAN do. A prototype tests what it CAN do FOR YOUR USE CASE. These are different things.**

- **The prototype-in-prod that nobody knew was a prototype.** A senior engineer built a "quick prototype" of a caching layer to test Redis. They used the main repo because "it was just for testing." Six months later, the engineer had left the company. The caching code was in production with no tests, no documentation, and a hardcoded TTL that expired during peak traffic. On-call had no idea the caching layer was a prototype. Incident cost: $85K in downtime and emergency fix effort. **Total cost: $50K-$200K per undocumented prototype-in-production in incident response and institutional knowledge loss. Prevent: Ground Rule R6 — NEVER prototype in the main repo. Isolation is not optional.**

## Verification

- [ ] **Ground Rules:** All 7 ground rules checked. No prototype code in main repo. No multi-question prototypes.
- [ ] **Single question:** Prototype addresses exactly ONE design question. Scope document confirms singular focus.
- [ ] **Falsifiable hypothesis:** Hypothesis stated in "We believe X because Y. Disproven if Z" format. Failure condition is specific and testable.
- [ ] **Time box respected:** Prototype completed in ≤ 20 minutes. Timer was started and honored. No extensions granted.
- [ ] **Isolation verified:** Prototype directory is outside main repo. `git status` in main repo shows no prototype files.
- [ ] **Decision documented:** Decision record committed to main repo. Includes hypothesis, approach, results, decision, and evidence quality rating.
- [ ] **Prototype disposed:** Prototype directory deleted. `rm -rf` or `git worktree remove` confirmed. No trace remains.
- [ ] **Evidence quality rated:** HIGH (clear result), MEDIUM (result with caveats), or LOW (inconclusive). Production decisions not made on LOW quality evidence.
- [ ] **Prototype shortcuts documented:** Any implementation shortcuts that differ from production intent are documented in the decision record.

If any check fails: return to the corresponding phase, resolve, and restart verification from that item.

## References

- **(../references/prototype-isolation.md)** — Git worktree setup guide for prototype isolation. Commands, cleanup procedures, and handling nested dependencies. Comparison with temp directory and Docker-based isolation approaches.
- **(../references/time-boxing.md)** — The 20-minute time box methodology. Timer protocols, 10-minute checkpoint, 18-minute feature freeze. Evidence that prototype value plateaus after 20 minutes and what to do when the timer expires.
- **(../references/decision-documentation.md)** — Template and protocol for prototype decision records. Includes hypothesis format, evidence quality assessment rubric, and archive structure for organizational learning from prototypes.
- **(../references/throwaway-discipline.md)** — The psychology and practice of throwing away code. Anti-patterns (sunk cost, "almost production"), disposal rituals, and organizational culture change for treating prototypes as disposable instruments.
- **(../references/question-scoping.md)** — Methodology for scoping design questions to be prototype-answerable. Question splitting algorithms, falsifiability criteria, and the "can you describe the minimum code in 3 sentences?" test.
- **(../references/empirical-evidence.md)** — Framework for evaluating prototype evidence quality. HIGH/MEDIUM/LOW classification criteria, confounded variable detection, and when prototype evidence is sufficient for a production decision.
- **(../references/anti-shipping-patterns.md)** — Catalog of the 10 most common ways prototype code enters production. Each pattern includes detection signals, real-world case studies, and prevention mechanisms.
- **(../references/git-worktree-setup.md)** — Practical guide to using git-worktree for prototype isolation. Commands, cleanup, handling uncommitted changes, and integration with the disposal protocol.
