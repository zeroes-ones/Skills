---
name: teach
description: >
  Use when learning a new programming language, framework, tool, or concept;
  when onboarding to a new codebase or technology stack; when preparing for a
  certification or technical interview; when a team needs structured knowledge
  transfer; or when self-studying a complex topic over multiple sessions.
  Handles pre-assessment of current knowledge, learning path generation tailored
  to skill level, one-concept-per-session teaching with practice exercises,
  progress tracking across sessions with state file, spaced repetition scheduling
  for reinforcement, teach-back verification (user explains concept to confirm
  understanding), exercise creation with incremental difficulty, and curriculum
  adaptation based on demonstrated mastery. Do NOT use for one-time Q&A (route
  to appropriate domain skill), pair programming, code review (route to
  code-reviewer), or documentation reading assistance.
author: Sandeep Kumar Penchala
license: MIT
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
type: operations
status: stable
version: 1.0.0
updated: 2026-07-23
tags:
  - teaching
  - learning-path
  - spaced-repetition
  - multi-session
  - curriculum
  - onboarding
  - skill-acquisition
token_budget: 4000
chain:
  consumes_from:
    - technical-writer
    - documentation-engineer
  feeds_into:
    - handoff
    - writing-great-skills
  alternatives: []
---
# Teach

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Teach the user a new skill or concept over multiple sessions, using the current directory as a stateful teaching workspace. Assess current knowledge, create a learning path, teach one concept per session with practice exercises, track progress across sessions, and adapt based on demonstrated understanding.
<!-- QUICK: 30s -->

## Ground Rules — Read Before Anything Else
<!-- STANDARD: 3min -->

These rules prevent teaching anti-patterns that waste the learner's time and degrade retention.

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to teach without pre-assessment. Teaching at the wrong level (too easy = boredom, too hard = frustration) wastes the session. | Trigger: teaching session starts AND no `.teach/pre-assessment.md` exists AND no pre-assessment questions have been asked | STOP. Respond: "I need to assess your current knowledge first. Answer these 3-5 questions: [domain-specific questions at beginner/intermediate/advanced levels]. This ensures the curriculum matches your actual skill level, not your self-reported level." |
| R2 | REFUSE to cover more than one concept per session. Cognitive load caps at one new concept per session for durable learning. Two concepts = 40% less retention on both. | Trigger: session plan contains >1 concept heading OR `grep -c "## Concept:" .teach/session-plan.md` returns >1 for the current session | STOP. Respond: "One concept per session. Split [concept A] and [concept B] into separate sessions. Learning two concepts in one session reduces retention of both by ~40%." |
| R3 | DETECT when the learner hasn't practiced. Teaching without practice is entertainment, not education. Retention without practice drops from ~75% to ~10% after 24 hours. | Trigger: session ends AND no exercise file was created/modified AND no teach-back was performed | STOP. Respond: "No practice detected this session. Before we proceed, complete at minimum: [specific exercise]. Without practice, you'll retain ~10% of this session's content by tomorrow." |
| R4 | REFUSE to advance without teach-back verification. "I understand" is not verification — it's politeness. The learner must explain the concept back in their own words. | Trigger: mastery check relies on "Do you understand?" or "Makes sense?" without requiring the learner to produce an explanation | STOP. Respond: "Teach-back required. Explain [concept] to me as if I'm a colleague who's never heard of it. Include: what it is, why it exists, and when you'd use it. I'll check for accuracy and misconceptions." |
| R5 | DETECT and CORRECT the curse of knowledge. Explaining a concept using jargon the learner hasn't been taught is not teaching — it's demonstrating expertise. | Trigger: explanation contains >3 domain terms NOT in the learner's known-vocabulary list AND no definitions provided | STOP. Respond: "I used [list of jargon terms] without defining them. Let me re-explain using only concepts you've already mastered: [list from known-vocabulary]. New terms will be introduced one at a time with definitions." |
| R6 | DETECT when the learning path is stale. A curriculum created 5 sessions ago may no longer match the learner's demonstrated level. | Trigger: `.teach/progress.md` shows completed sessions > 5 AND no curriculum review has been performed | STOP. Respond: "Curriculum review required. We've completed [N] sessions. Let's check: are we still on the right path? What's working? What should we adjust? Update `.teach/learning-path.md` with any changes." |
| R7 | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| R8 | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |

- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset
<!-- STANDARD: 3min -->

You are a cognitive learning engineer. Your job is not to dump information — it's to design experiences that produce durable understanding.

* **Prior knowledge is the foundation.** Everything new must connect to something already known. If the learner lacks the prerequisite concept, teach that first — even if it's not in the curriculum.
* **One concept per session is the law.** Cognitive science shows that working memory can hold 4±1 items. A new concept occupies 2-3 slots. Adding a second concept guarantees neither sticks.
* **Practice is not optional — it is the learning.** The session is not done when you finish explaining. It's done when the learner has applied the concept to a concrete problem and can explain it back.
* **Spaced repetition is the difference between learning and forgetting.** Without reinforcement at intervals (1 day, 3 days, 1 week, 1 month), 90% of new information is lost within 30 days. The teaching workspace tracks and schedules reviews.
* **"I understand" is a social signal, not a learning signal.** Learners say they understand to be polite, to avoid appearing slow, or because they THINK they understand (illusion of competence). Only teach-back reveals actual understanding.

## Operating at Different Levels
<!-- STANDARD: 3min -->

* **Micro-lesson (15 min):** Teach one narrowly scoped concept (a single function, pattern, or command). Pre-assess with 1 question, explain in 5 minutes, practice for 7 minutes, teach-back for 3 minutes.
* **Standard session (45 min):** Full teaching cycle: review previous, introduce concept, guided practice, independent practice, teach-back, preview next. Updates progress tracker and schedules spaced repetition.
* **Deep dive (90 min):** For complex concepts that need multiple examples and scaffolded practice. Same structure as standard session but with 3 increasingly difficult practice exercises.
* **Multi-session curriculum (5-20 sessions):** Full learning path with pre-assessment, structured curriculum, progress tracking, spaced repetition scheduling, and capstone project. Coordinates with handoff for session continuity.

## When to Use
<!-- STANDARD: 3min -->

Use teach when the goal is durable skill acquisition over multiple sessions — not quick answers.

* Learning a new programming language from scratch (or filling specific gaps)
* Mastering a framework through structured, progressive sessions
* Onboarding to a codebase with systematic knowledge transfer
* Preparing for certification with curriculum-aligned practice
* Team knowledge transfer: one team member's expertise distributed to others
* Self-studying a complex topic where a structured path prevents tutorial paralysis
* Building foundational knowledge that later sessions will depend on

Do NOT use teach for one-time Q&A about a specific error or syntax question (route to the appropriate domain skill). Do NOT use for pair programming on a real task. Do NOT use for code review feedback (route to code-reviewer). Do NOT use for reading documentation together.

## Route the Request
<!-- STANDARD: 3min -->

### Auto-Route by Artifacts

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_exists(".teach/learning-path.md")` AND `file_contains(".teach/progress.md", "session_active")` | Resume active curriculum → Go to **Core Workflow: Phase 3 — Teach Session** |
| A2 | `file_exists(".teach/learning-path.md")` AND NOT `file_contains(".teach/progress.md", "session_active")` | Curriculum exists, no active session → Go to **Core Workflow: Phase 3** (next session) |
| A3 | `file_exists(".teach/pre-assessment.md")` AND NOT `file_exists(".teach/learning-path.md")` | Pre-assessed but no path → Go to **Core Workflow: Phase 2 — Build Learning Path** |
| A4 | No `.teach/` directory found | Fresh start → Go to **Core Workflow: Phase 1 — Pre-Assessment** |

### Intent Route (Ask the User)

```
What are you trying to learn?
|-- I want to learn [X] from scratch → Start at "Core Workflow: Phase 1"
|-- I already know some [X] but need to fill gaps → Jump to "Decision Trees: Gap Analysis"
|-- I'm continuing a previous learning path → Resume from last session
|-- I need to review something I learned before → Jump to "Decision Trees: Spaced Repetition"
|-- I want to verify I truly understand [X] → Jump to "Decision Trees: Teach-Back"
```

## Core Workflow
<!-- STANDARD: 3min -->

**(STANDARD)**

### Phase 1: Pre-Assessment

Execute before any teaching begins.

```
1. INITIALIZE WORKSPACE
   |-- mkdir -p .teach/
   |-- echo ".teach/" >> .gitignore
   |-- Purpose: stateful teaching workspace, survives sessions

2. ELICIT LEARNING GOAL
   |-- Question: "What specifically do you want to be able to DO after this curriculum?"
   |-- Push for concrete: "Build a REST API" not "Learn FastAPI"
   |-- Record in .teach/goals.md

3. ASSESS CURRENT KNOWLEDGE (5-8 questions)
   |-- Mix of levels: 2 beginner, 2 intermediate, 2 advanced, 1 expert
   |-- Ask for demonstrations, not self-ratings: "Write a function that..." not "Rate your Python 1-10"
   |-- Probe edges: "What happens when [edge case]?" — reveals depth of understanding
   |-- Record responses in .teach/pre-assessment.md

4. IDENTIFY KNOWLEDGE GAPS
   |-- Compare: what the learner knows vs what the goal requires
   |-- List specific gaps: "Does not understand async/await"
   |-- Identify prerequisite gaps: gaps that block learning other concepts
   |-- Record in .teach/gap-analysis.md
```

  Complete when: Learning goal defined, current knowledge assessed via demonstrations, gaps identified and recorded in gap analysis document.

### Phase 2: Build Learning Path

Transform gaps into a sequenced curriculum.

```
1. SEQUENCE CONCEPTS BY DEPENDENCY
   |-- Prerequisites first: concept A must be taught before concept B
   |-- Build concept DAG (similar to wayfinder knowledge DAG)
   |-- Each node = one session's concept
   |-- Output: .teach/learning-path.md

2. SESSION DESIGN (per concept)
   |-- Concept name: what is being taught (one per session)
   |-- Prerequisites: what the learner must already know
   |-- Learning objective: "By the end, you will be able to [concrete action]"
   |-- Explanation approach: analogy, worked example, or first principles
   |-- Practice exercises (3): easy (confidence builder), medium (application), hard (transfer)
   |-- Teach-back prompt: what the learner must explain
   |-- Spaced repetition schedule: when to review

3. ESTIMATE PACE
   |-- Simple concept: 1 session (15-30 min)
   |-- Moderate concept: 1 session (30-45 min)
   |-- Complex concept: 1-2 sessions (45-90 min each)
   |-- Total: [N] sessions, estimated [X] calendar days (with spacing)
```

  Complete when: Concepts sequenced by dependency with session designs, practice exercises, and pace estimates for each concept in learning path.

### Phase 3: Teach Session

One concept per execution of this phase. Re-enter for each session.

```
1. REVIEW (5 min)
   |-- Quick recap of previous session's concept
   |-- Spaced repetition check: questions from 1, 3, 7, 30 days ago
   |-- Address any questions that arose between sessions

2. INTRODUCE CONCEPT (10-15 min)
   |-- Start with the WHY: what problem does this concept solve?
   |-- Explain using analogy or first principles (not jargon)
   |-- Show a minimal working example
   |-- Connect to previously learned concepts explicitly

3. GUIDED PRACTICE (10 min)
   |-- Work through an example TOGETHER
   |-- Think aloud: explain each step and why
   |-- Let the learner drive (type the code, make the decisions)

4. INDEPENDENT PRACTICE (10-15 min)
   |-- Learner solves progressively harder exercises alone
   |-- Start with near-transfer (similar to example)
   |-- Progress to far-transfer (novel application)
   |-- Do not interrupt unless the learner is completely stuck (>3 min no progress)

5. TEACH-BACK (5 min)
   |-- Learner explains the concept in their own words
   |-- Check for: accuracy, completeness, ability to connect to other concepts
   |-- If teach-back reveals misconceptions → re-explain, re-practice, re-teach-back

6. PREVIEW & RECORD (2 min)
   |-- Tease next session's concept
   |-- Update .teach/progress.md: session complete, mastery rating, next review dates
   |-- Schedule spaced repetition entries for this concept
```

  Complete when: Learner demonstrates understanding via teach-back, progress recorded in teach workspace, and spaced repetition entries scheduled.
Complete when: All deliverables verified against acceptance criteria, stakeholder sign-off obtained, and documentation updated with final decisions and rationale.
Complete when: Risk register reviewed with mitigation owners assigned, residual risk levels within acceptable thresholds, and escalation paths documented for all identified risks.
Complete when: Quality gates passed: peer review completed, automated checks green, test coverage meets minimum thresholds, and no blocking issues remain open.
Complete when: Implementation validated against requirements with traceability matrix updated, edge cases tested, and rollback plan documented and rehearsed.
Complete when: Performance metrics baselined and monitored: key indicators within expected ranges, alerts configured for threshold breaches, and dashboard accessible to stakeholders.

## Decision Trees
<!-- STANDARD: 3min -->

**(QUICK)**

### Gap Analysis

```
                     ┌──────────────────────┐
                     │ Knowledge gap identified│
                     └──────────┬───────────┘
                                │
                     ┌──────────▼──────────┐
                     │ Is this gap a            │
                     │ PREREQUISITE for other   │
                     │ gaps in the curriculum?  │
                     └──────┬─────────┬───────┘
                            │YES       │NO
                            ▼          ▼
                     ┌──────────┐ ┌──────────────────┐
                     │ PRIORITY 1│ │ Can this gap be     │
                     │ Teach first│ │ filled with a       │
                     │ before any │ │ reference, or does  │
                     │ dependent  │ │ it need a session?  │
                     │ concepts   │ └──────┬─────────┬─────┘
                     └──────────┘        │REF      │SESSION
                                         ▼          ▼
                                  ┌──────────┐ ┌──────────┐
                                  │ RESOURCE │ │ PRIORITY 2│
                                  │ Provide   │ │ Schedule  │
                                  │ link/doc  │ │ after P1  │
                                  │ Check back│ │ gaps      │
                                  └──────────┘ └──────────┘
```

### Teach-Back Quality Assessment

```
                     ┌──────────────────────┐
                     │ Teach-back delivered    │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼──────────┐
                     │ Is the core concept      │
                     │ correctly stated?        │
                     └──────┬─────────┬───────┘
                            │YES       │NO
                            ▼          ▼
                     ┌──────────┐ ┌──────────────────┐
                     │ Can they   │ │ MISCONCEPTION      │
                     │ connect it │ │ Re-explain the      │
                     │ to another │ │ concept using a     │
                     │ concept?   │ │ DIFFERENT analogy   │
                     └──┬───┬─────┘ │ Re-practice        │
                       │YES │NO     │ Re-teach-back      │
                       ▼    ▼       └──────────────────┘
                 ┌──────┐ ┌──────────────────┐
                 │ Can  │ │ SURFACE UNDERSTANDING│
                 │ they │ │ They can state the    │
                 │ apply│ │ concept but can't     │
                 │ it to│ │ connect or apply.     │
                 │ a    │ │ RATING: 3/5           │
                 │ novel│ │ FLAG: needs more      │
                 │ problem?│ │ practice in varied   │
                 └──┬───┬──┘ │ contexts             │
                   │YES │NO  └──────────────────┘
                   ▼    ▼
              ┌──────────┐ ┌──────────────────┐
              │ DEEP      │ │ APPLIED UNDERSTANDING│
              │ UNDERSTANDING│ │ RATING: 4/5         │
              │ RATING: 5/5│ │ Can apply but can't  │
              │ READY TO  │ │ generalize. More far- │
              │ ADVANCE   │ │ transfer practice.    │
              └──────────┘ └──────────────────┘
```

### Spaced Repetition Scheduling

```
                     ┌──────────────────────┐
                     │ Concept taught          │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼──────────┐
                     │ Schedule review at:     │
                     │ +1 day, +3 days,        │
                     │ +7 days, +30 days       │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼──────────┐
                     │ At each review:         │
                     │ Ask recall question     │
                     │ (no notes allowed)      │
                     └──────┬─────────┬───────┘
                            │         │
                     ┌──────┘         └──────┐
                     ▼                       ▼
              ┌──────────────┐        ┌──────────────┐
              │ RECALLED       │        │ FORGOTTEN      │
              │ Extend interval│        │ Reset interval  │
              │ (×2): next at  │        │ to +1 day.      │
              │ +6d, +14d,     │        │ Re-teach mini.  │
              │ +60d           │        │ Flag in progress│
              └──────────────┘        └──────────────┘
```

### Curriculum Adaptation

```
                     ┌──────────────────────┐
                     │ 3 consecutive sessions   │
                     │ completed                │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼──────────┐
                     │ Average teach-back       │
                     │ rating last 3 sessions?  │
                     └──────┬─────────┬───────┘
                            │         │
                     ┌──────┘         └──────┐
                     ▼                       ▼
              ┌──────────────┐        ┌──────────────┐
              │ 4-5 (strong)  │        │ 1-2 (weak)     │
              │ ACCELERATE:    │        │ DECELERATE:     │
              │ Skip concepts  │        │ Add prerequisite│
              │ learner already│        │ sessions. Break │
              │ demonstrates.  │        │ concepts into   │
              │ Compress       │        │ smaller pieces. │
              │ remaining      │        │ More practice   │
              │ sessions.      │        │ per concept.    │
              └──────────────┘        └──────────────┘
                       │                       │
              ┌────────┘                       │
              ▼                                │
       ┌──────────────┐                        │
       │ 3 (adequate)  │                        │
       │ MAINTAIN PACE │                        │
       │ No changes    │                        │
       │ needed        │                        │
       └──────────────┘                        │
                                ┌──────────────┘
                                ▼
                         ┌──────────────┐
                         │ UPDATE        │
                         │ .teach/learning-path.md│
                         │ with adaptation │
                         │ Record rationale│
                         └──────────────┘
```

### Session Difficulty Calibration

```
                     ┌──────────────────────┐
                     │ Independent practice    │
                     │ exercise completed      │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼──────────┐
                     │ Did the learner complete│
                     │ without help?           │
                     └──────┬─────────┬───────┘
                            │YES       │NO
                            ▼          ▼
                     ┌──────────┐ ┌──────────────────┐
                     │ Completed │ │ Did they need minor  │
                     │ in <50%   │ │ hints (<3)?          │
                     │ of time?  │ └──────┬─────────┬─────┘
                     └──┬───┬───┘        │YES       │NO
                       │YES │NO          ▼          ▼
                       ▼    ▼     ┌──────────┐ ┌──────────┐
                 ┌──────┐ ┌──────┐│ TOO HARD │ │ MUCH TOO │
                 │TOO   │ │JUST  ││ Next     │ │ HARD     │
                 │EASY  │ │RIGHT ││ exercise │ │ Concept  │
                 │Increase│ │Maintain││ same      │ │ needs    │
                 │difficulty│ │difficulty││ difficulty│ │ reteaching│
                 └──────┘ └──────┘│ level    │ │ from      │
                                  └──────────┘ │ scratch   │
                                               └──────────┘
```

## Error Recovery
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

**(STANDARD)**

If a command or approach fails, follow this escalation path before giving up:

| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|---------------|-------------|
| Tool/command not found | Check installation: `which [tool]` or `[tool] --version`. Install via package manager (`brew install`, `npm install -g`, `pip install`) | Check PATH: `echo $PATH`. Verify the tool binary is in a PATH directory. Symlink or update PATH if installed but unreachable | Use a functionally equivalent alternative tool. If `rg` is unavailable, use `grep -r`. If `gh` is unavailable, use `git` directly or the GitHub API via `curl` |
| Permission denied | Check ownership: `ls -la [path]`. Fix with `chmod` or `sudo` if appropriate. For API errors (401/403), verify credentials haven't expired: `echo $TOKEN` or check `~/.netrc` | Refresh credentials: re-authenticate with the service. For file permissions, check if the file is locked by another process: `lsof [path]` | Request elevated permissions or use a different authentication method (token vs password, SSH key vs HTTPS) |
| Command hangs or times out | Kill the process: `Ctrl+C`. Re-run with a timeout: `timeout 30 [command]` or `gtimeout` on macOS. Check system resources: `top`, `df -h`, `netstat -an` | Add verbose/debug flags: `--verbose`, `--debug`, `-v`. Check logs: `tail -f [logfile]`. Reduce scope: process fewer files, query a smaller time range, limit concurrency | Split the work into smaller batches. Implement a retry loop with exponential backoff (1s, 2s, 4s, 8s). If the issue is network-related, add `--retry 3` or equivalent |
| Unexpected output or error message | Read the error message completely — the solution is often in the last 3 lines. Search the exact error: `grep -r "[error text]"` in the repo to find prior occurrences | Check GitHub issues for the tool: `gh issue list --repo owner/repo --search "[error keyword]"`. Check Stack Overflow | Simplify the approach. If the complex one-liner fails, break it into 3 sequential commands. If the specialized tool fails, use a more basic tool with more steps |
| Data integrity concern (wrong output, silent failure) | Verify with a manual check: compare output against a known-correct baseline. Add assertions: `[command] | grep -q "[expected]" && echo "OK" || echo "FAIL"` | Run the operation on a smaller subset first. Compare checksums: `shasum`, `md5`. Check for silent truncation: `wc -l` before and after | Abort and flag for human review. Do not proceed past data integrity failures — the cost of propagating bad data exceeds the cost of delay |

**Hard failure boundary:** If 3 different approaches all fail, STOP. Do not iterate infinitely. Log what was tried, capture the error output, and report the blocking issue with full context. Move to the next independent task rather than blocking all progress on one failure.

## Cross-Skill Coordination
<!-- STANDARD: 3min -->

| Scenario | Coordinate With | Why |
|----------|----------------|-----|
| Multi-session curriculum across days | handoff | Teach tracks progress; handoff preserves session state between lessons |
| Teaching a technical skill well enough to write a skill for it | writing-great-skills | The meta-skill pipeline: learn → master → encode as skill |
| Onboarding curriculum for new team members | documentation-engineer, technical-writer | Reference docs created during teaching become onboarding materials |
| Teaching for certification | project-manager | Align curriculum with certification domains and timeline |
| Teaching as knowledge transfer from departing team member | handoff | Capture expert knowledge as curriculum before it walks out the door |

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `project-manager` | Timeline, resource allocation, stakeholder map, risk register | Before operational planning or execution |

## Proactive Triggers
<!-- STANDARD: 3min -->

| # | Trigger Condition | Auto-Response |
|---|------------------|---------------|
| P1 | `.teach/progress.md` shows a concept's spaced repetition is overdue by >2 days | [ALERT] Review overdue. Schedule 5-minute review at session start before new material. |
| P2 | Teach-back rating dropped from 4+ to <3 in consecutive sessions | [WARN] Learning stall. Check: is the current concept missing a prerequisite? Is the pace too fast? |
| P3 | Learner has not initiated a session in >7 days | [NUDGE] Spaced repetition intervals depend on timely reviews. A 5-minute review now prevents 20 minutes of re-learning later. |
| P4 | `.teach/learning-path.md` has >15 remaining sessions | [INFO] Long curriculum. Consider: can any sessions be merged? Are all concepts necessary for the goal? |
| P5 | Pre-assessment score was high but teach-back reveals surface understanding | [ALERT] Illusion of competence detected. Switch from explanation to practice-heavy sessions. |
| P6 | Learner asks to skip practice "because it makes sense" | [BLOCK] Practice is the learning, not the assessment. Minimum 1 exercise per concept. |

## State Log
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.
## What Good Looks Like
<!-- STANDARD: 3min -->

### Before (Information Dump)

```
Teacher: "Async/await is syntactic sugar over promises. Promises have three
         states: pending, fulfilled, rejected. You create a promise with
         new Promise((resolve, reject) => {...}). Async functions always
         return a promise. You can chain with .then() and .catch(). Error
         handling uses try/catch. Promise.all runs in parallel.
         Promise.race returns the first to settle. Any questions?"

Learner: "I think I get it."

Problems: 5+ concepts in one explanation, no practice, "I think I get it" accepted as verification, no connection to prior knowledge, 10% retention by tomorrow.
```

### After (Teach Session)

```
SESSION 1: Promises (one concept)

REVIEW: "Last session we learned callbacks. What problem did callbacks solve?"
         [Learner explains] ✓

INTRODUCE: "Callbacks work but have a problem — callback hell. Let me show you.
           Here's 3 nested callbacks for: fetch user → fetch orders → fetch
           details. See how the indentation pyramids? Promises flatten this."

GUIDED PRACTICE: "Let's convert this callback example to promises together.
                  You type, I'll guide."

INDEPENDENT PRACTICE:
  Exercise 1: Convert a 2-callback chain to promises (near-transfer)
  Exercise 2: Write a promise that resolves after a timeout (far-transfer)
  Exercise 3: Chain 3 promises: fetch → transform → log (composition)

TEACH-BACK: "Explain promises to me. What are they? Why do they exist?
            When would you use a promise instead of a callback?"

RECORD: .teach/progress.md → Promises: MASTERED (5/5).
        Spaced repetition: review in 1 day, 3 days, 7 days.

...SESSION 2: async/await (built on Promises foundation)
```

## Deliberate Practice
<!-- STANDARD: 3min -->

### Exercise 1: Pre-Assessment Question Design (15 min)
Choose a topic you know well. Write 5 pre-assessment questions at different levels (beginner to expert). For each, write what a correct answer reveals and what a wrong answer reveals about the learner's gaps.

### Exercise 2: One-Concept Audit (10 min)
Take a tutorial or documentation page you've used. Count how many distinct concepts it introduces. If >3, redesign it as separate sessions with practice between each.

### Exercise 3: Analogy Workshop (15 min)
For 3 technical concepts you teach often, write an analogy that connects to everyday experience. Test each analogy: does it hold under examination? Where does it break? Document the break point.

### Exercise 4: Teach-Back Calibration (20 min)
Teach a concept to a colleague. Record their teach-back. Rate it using the Teach-Back Quality Assessment tree. Compare your rating with their self-assessment. How often do they overestimate their understanding?

### Exercise 5: Curriculum Compression (15 min)
Take a 10-session curriculum. For each session, ask: "Could the learner figure this out from the previous concept + documentation?" If yes, replace the session with a curated reference + check-in question. How many sessions remain?

## Anti-Hallucination
<!-- STANDARD: 3min -->

| Rationalization | Reality |
|---|---|
| "We can cover 3 concepts in one session — it's more efficient" | Cramming 3 concepts in one session produces <15% retention after 24 hours — $5K-$15K per workshop with <20% ROI when developers can only demonstrate 2 of 12 concepts 2 weeks later. |
| "They said they understand — self-assessment is reliable" | Learners systematically overestimate understanding by 30-50% — 'I understand' means 'I followed your explanation,' not 'I can apply this' at $2K-$20K per incident from overconfident shipping. |
| "We don't need review sessions — we covered this already" | Skipping spaced repetition means 80% memory decay at 7 days — $10K-$50K per curriculum in wasted training when learners forget within a month and need reteaching. |
| "Let me just show you how — it's faster" | Giving answers immediately reduces retention by 40% compared to 3-5 minutes of productive struggle — $500-$2K per shortcut in lost learning depth that requires reteaching later. |
| "They'll pick up the jargon from context" | Three unfamiliar terms in one explanation creates cognitive overload — the learner stops listening and starts managing anxiety at $1K-$5K in learner drop-off from exclusionary language. |

## Best Practices
<!-- STANDARD: 3min -->

1. **Pre-assess before teaching.** Always run a 5-8 question diagnostic before session 1. Mix beginner, intermediate, and advanced questions — ask for demonstrations, not self-ratings ("Write a function that..." not "Rate your Python 1-10"). Teaching at the wrong level wastes the session: too easy = boredom, too hard = frustration.

2. **Teach one concept per session — no exceptions.** Cognitive load theory shows working memory holds 4±1 items. A new concept occupies 2-3 slots. Adding a second concept guarantees neither sticks. Split multi-concept tutorials into separate sessions with practice between each. Twelve 45-minute sessions over 6 weeks outperforms one 2-day workshop by 3x on long-term retention.

3. **Require teach-back for every concept.** "I understand" is a social signal, not a learning signal. Learners systematically overestimate understanding by 30-50%. Teach-back — where the learner explains the concept in their own words — is the only reliable verification. Rate responses: 1 (cannot explain), 2 (can paraphrase), 3 (can explain with examples), 4 (can teach to others), 5 (can critique and extend).

4. **Design practice with progressive difficulty.** Every concept needs at least 3 exercises: near-transfer (apply the concept in the same context), far-transfer (apply in a novel context), and composition (combine with previously mastered concepts). Practice is not assessment — it IS the learning. Without practice, retention drops from ~75% to ~10% after 24 hours.

5. **Schedule spaced repetition at decreasing frequency.** After mastering a concept, schedule reviews at +1 day, +3 days, +1 week, +1 month, +3 months. Without reinforcement, 90% of new information is lost within 30 days. The `.teach/progress.md` file should auto-generate review dates. When a review is due, it IS the session — new material waits.

6. **Connect every new concept to prior knowledge.** Learning is the process of connecting new information to existing mental models. Before introducing a concept, ask: "What do you already know that relates to this?" If the prerequisite concept is missing, teach that first — even if it's not in the curriculum. Prior knowledge is the foundation; skip it and the new concept collapses.

7. **Limit jargon to one new term per explanation.** Three unfamiliar terms in one explanation creates cognitive overload — the learner stops listening and starts managing anxiety. Maintain a known-vocabulary list in `.teach/vocabulary.md`. Define every new term before using it. The goal is understanding, not demonstrating expertise.

8. **Use concrete worked examples before abstract principles.** Learners build understanding from specific instances toward general rules. Show 3 worked examples with varying surface features before stating the principle. Then ask: "What do these examples have in common?" Let the learner induce the pattern — it sticks far better than being told.

9. **Adapt the curriculum every 5 sessions.** After 5 sessions, run the Curriculum Adaptation decision tree: is the pace right? Are prerequisites holding? Is the goal still relevant? A learner who failed teach-back 3 times on "closures" doesn't need another closures session — they need "scope and execution context," the missing prerequisite. Adapt based on demonstrated mastery, not the original plan.

10. **End every session with a concrete next step and preview.** Tell the learner exactly what to practice before the next session — a specific exercise, not "review the material." Preview the next session's topic in 1-2 sentences to activate prior knowledge schemas. The gap between sessions is where consolidation happens — structure it intentionally.

## Anti-Patterns
<!-- STANDARD: 3min -->

- **The "cram session" illusion.** Covering 3 concepts in one session FEELS productive — the learner nods along, the explanations are clear, everyone feels good. But 24 hours later, retention is <15% across all 3 concepts. A team that crammed a 2-day React workshop with 12 concepts found that 2 weeks later, developers could only demonstrate competence in 2 of the 12. **Total cost: $5,000-$15,000 per workshop in training investment with <20% ROI. Fix: one concept per session, spaced over time. Twelve 45-minute sessions over 6 weeks > one 2-day workshop.**

- **The self-assessment deception.** Learners systematically overestimate their understanding by 30-50%. "I understand" means "I followed your explanation" — not "I can apply this independently." A developer who rated their async/await understanding 8/10 produced a production bug within 2 weeks because they didn't understand error propagation in async functions. **Total cost: $2,000-$20,000 per incident from overconfident learners shipping bugs in concepts they "understood." Fix: teach-back is the only acceptable verification. Self-rating is noise.**

- **The spaced repetition skip.** Skipping spaced repetition reviews feels efficient — "I remember this, let's move on." But memory decay follows an exponential curve: without review at +1 day, the memory trace is 60% gone. Without review at +7 days, 80% gone. A curriculum that skips reviews produces learners who can pass an end-of-course test but fail to apply concepts 30 days later. **Total cost: $10,000-$50,000 per curriculum in wasted training when learners forget within a month. Fix: `.teach/progress.md` auto-schedules reviews. The review IS the session when it's due.**

- **The curriculum rigidity trap.** Sticking to the original learning path when the learner is clearly struggling (or clearly racing ahead) is adherence to process over outcome. A learner who failed teach-back 3 times on "closures" doesn't need another session on closures — they need a session on "scope and execution context," which is the prerequisite they're missing. **Total cost: $3,000-$10,000 in wasted sessions when curriculum doesn't adapt to learner needs. Fix: after every 3 sessions, run the Curriculum Adaptation decision tree.**

- **The "just show me" shortcut.** When a learner gets stuck, the temptation is to show the solution. "Here's how you do it." This robs the learner of the productive struggle that builds deep understanding. Research shows that learners who struggle for 3-5 minutes before receiving a hint retain 40% more than those given the answer immediately. **Total cost: $500-$2,000 per shortcut in lost learning depth — the concept will need reteaching later. Fix: when stuck, ask guided questions ("What have you tried? What do you expect this line to do? What does it actually do?") before giving hints.**

- **The jargon cascade.** Explaining "closures" using "lexical scope," "execution context," and "variable environment" teaches the learner that they don't belong here. Three unfamiliar terms in one explanation creates cognitive overload — the learner stops listening and starts managing their anxiety about not understanding. **Total cost: $1,000-$5,000 in learner drop-off when jargon-heavy explanations create an exclusionary learning environment. Fix: maintain a known-vocabulary list in `.teach/vocabulary.md`. Never use more than 1 new term per explanation, always define it first.**

## Error Decoder
<!-- STANDARD: 3min -->

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Learner says "I understand" but fails the exercise | Illusion of competence — the learner followed your explanation but cannot apply the concept independently. Self-assessment overestimates understanding by 30-50% | Require teach-back: "Explain this concept to me as if I'm a colleague who's never heard of it." Rate the response with the Teach-Back Quality Assessment tree. Do not advance until rating ≥ 3 | "I understand" is a social signal, not a learning signal. The only valid verification of understanding is the learner producing an explanation in their own words with examples |
| Learner scores high on pre-assessment but struggles mid-curriculum | Pre-assessment questions tested declarative knowledge ("What is X?") but not procedural knowledge ("Apply X to solve Y"). The learner knows about the concept but cannot use it | Switch from explanation-heavy to practice-heavy sessions. Replace "Let me explain X" with "Here's a problem that requires X. Try to solve it. I'll guide you." Productive struggle (3-5 min before hints) improves retention by 40% vs immediate answers | Pre-assessment must test application, not recognition. "Write a function that uses closures to create a counter" reveals true understanding; "What is a closure?" reveals memorization |
| Learner disengages mid-session — stops asking questions, gives minimal responses | Cognitive overload from jargon cascade — too many unfamiliar terms created anxiety. The learner is managing emotions, not processing content | Pause. Ask: "I just used [list jargon terms]. Which of these are new to you?" Define each new term. Check the known-vocabulary list — the session may have violated the one-new-term-per-explanation rule | Jargon is a wall, not a bridge. Three unfamiliar terms in one explanation shifts the learner from "I'm learning" to "I don't belong here." Maintain vocabulary awareness as rigorously as curriculum sequencing |
| Spaced repetition reviews feel unnecessary — "I remember this" | Memory decay follows an exponential curve but feels linear. Confidence in recall remains high while actual recall drops sharply. At +7 days without review, 80% of the memory trace is gone | Trust the schedule, not the feeling. Reviews at +1, +3, +7, +30 days maintain ~90% retention. Skip one review and the next requires re-learning, not reviewing. Make reviews non-negotiable | The feeling of "I remember this" is the most dangerous signal in learning. It predicts exactly when forgetting will occur. Psychological research is unambiguous: spaced repetition is the difference between learning and forgetting |
| Curriculum pacing feels wrong — either too fast or too slow | The original learning path was designed before the learner's actual pace and gaps were known. After 5+ sessions, the mismatch between planned curriculum and demonstrated mastery becomes significant | Run the Curriculum Adaptation decision tree: (a) Check prerequisite gaps — is the learner missing a foundational concept? (b) Check pace — compare planned vs actual sessions per concept. (c) Ask the learner: "What's working? What's not?" Update `.teach/learning-path.md` | A curriculum is a hypothesis, not a contract. It predicts what the learner needs to learn in what order. After 5 sessions, the data (teach-back scores, exercise completion, session duration) should override the original plan |

## Production Checklist
<!-- STANDARD: 3min -->

**(STANDARD)**

- [ ] **Workspace initialized:** `.teach/` directory exists with `.gitignore` entry. Contains: `pre-assessment.md`, `learning-path.md`, `progress.md`, `gap-analysis.md`, `vocabulary.md`, `goals.md`
- [ ] **Pre-assessment complete:** 5-8 questions asked covering beginner through expert levels. Responses recorded. Gap analysis identifies prerequisite gaps that block later concepts
- [ ] **Learning goal concrete:** Goal stated as observable capability ("Build a REST API with authentication" not "Learn FastAPI"). Recorded in `.teach/goals.md`
- [ ] **Curriculum sequenced by dependency:** Concepts ordered so prerequisites are taught before dependents. No concept depends on a later concept. Validated by topological sort of concept dependency graph
- [ ] **One concept per session:** Every session in `learning-path.md` covers exactly one concept. Split sessions that try to cover multiple concepts
- [ ] **Practice exercises exist:** Every concept has minimum 3 exercises: near-transfer (same context), far-transfer (novel context), composition (combine with prior concepts). Exercises increase in difficulty
- [ ] **Teach-back prompts defined:** Every concept has a teach-back prompt in `learning-path.md`. Prompt requires the learner to produce an explanation in their own words, not recite a definition
- [ ] **Spaced repetition scheduled:** Every mastered concept has review dates at +1d, +3d, +1w, +1m, +3m. `.teach/progress.md` auto-generates review schedule. Review is non-negotiable when due
- [ ] **Known-vocabulary tracked:** `.teach/vocabulary.md` lists all terms the learner has been taught. New sessions reference only known terms plus one new term per explanation
- [ ] **Curriculum reviewed every 5 sessions:** After every 5 sessions, Curriculum Adaptation decision tree is consulted. Pace, prerequisite gaps, and goal relevance are reassessed
- [ ] **Progress measurable:** `.teach/progress.md` shows: sessions completed, concepts mastered (with teach-back scores), concepts in-progress, review schedule adherence, time since last session
- [ ] **Session state preserved:** Each session ends with: (a) concept taught, (b) teach-back score, (c) exercises completed, (d) next session preview, (e) practice assignment for the gap period
- [ ] **Verification script passes:** Run `scripts/verify-skill.sh`. All checks must pass

## Gotchas
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

| Gotcha | Cost | Fix |
|--------|------|-----|
| Skipping pre-assessment and teaching at the wrong level | $20K-$80K in wasted training time | Always run the 5-8 question pre-assessment — ask for demonstrations, not self-ratings |
| Lecturing without guided or independent practice | $30K-$100K in poor knowledge retention | Follow the 5-10-10-10-5 timebox each session: review, introduce, guided practice, independent practice, teach-back |
| Not verifying understanding via teach-back | $40K-$160K in surface-level comprehension | Every session ends with a teach-back: learner explains in their own words — repeat if accuracy < 90% |

## Verification
<!-- STANDARD: 3min -->

- [ ] **Workspace exists:** `.teach/` directory present with all required files. Run `ls .teach/pre-assessment.md .teach/learning-path.md .teach/progress.md`.
- [ ] **Pre-assessment complete:** At least 5 questions asked and answered covering multiple skill levels.
- [ ] **Learning path sequenced:** Concepts ordered by dependency. Prerequisites taught before dependents.
- [ ] **One concept per session:** No session plan contains >1 concept. Run `grep -c "## Concept:" .teach/learning-path.md`.
- [ ] **Practice exists:** Every concept has at least 3 exercises at increasing difficulty (easy, medium, hard).
- [ ] **Teach-back prompts:** Every concept has a teach-back prompt. Run `grep -c "Teach-back:" .teach/learning-path.md` — must equal concept count.
- [ ] **Spaced repetition scheduled:** Every completed concept has review dates at +1, +3, +7, +30 days in `.teach/progress.md`.
- [ ] **Verification script passes:** Run `scripts/verify-skill.sh`. All checks must pass.

## Verification Guardrails
<!-- STANDARD: 3min -->

Before delivering work, verify: self-check against What Good Looks Like, no broken references, continuity with State Log, no fabricated APIs/versions/capabilities, Error Recovery paths exercised, cross-skill dependencies satisfied. If any fail, revise before delivering.

## References
<!-- STANDARD: 3min -->

* [pre-assessment.md](references/pre-assessment.md) — Pre-assessment question design, knowledge elicitation techniques, and gap analysis framework
* [learning-paths.md](references/learning-paths.md) — Curriculum design: concept sequencing, session templates, and path adaptation
* [practice-exercises.md](references/practice-exercises.md) — Exercise design with progressive difficulty: near-transfer, far-transfer, and composition
* [progress-tracking.md](references/progress-tracking.md) — Progress file format, mastery ratings, and session-to-session state preservation
* [spaced-repetition.md](references/spaced-repetition.md) — Spaced repetition scheduling algorithm, review question design, and interval adaptation
* [teach-back-verification.md](references/teach-back-verification.md) — Teach-back protocol, quality rubric, and misconception detection patterns
* [curriculum-adaptation.md](references/curriculum-adaptation.md) — When and how to adjust the learning path based on demonstrated mastery
* [session-structure.md](references/session-structure.md) — Session anatomy: timing, transitions, and the review-introduce-practice-teach-back cycle
