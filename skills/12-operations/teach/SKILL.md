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

## Ground Rules — Read Before Anything Else

These rules prevent teaching anti-patterns that waste the learner's time and degrade retention.

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to teach without pre-assessment. Teaching at the wrong level (too easy = boredom, too hard = frustration) wastes the session. | Trigger: teaching session starts AND no `.teach/pre-assessment.md` exists AND no pre-assessment questions have been asked | STOP. Respond: "I need to assess your current knowledge first. Answer these 3-5 questions: [domain-specific questions at beginner/intermediate/advanced levels]. This ensures the curriculum matches your actual skill level, not your self-reported level." |
| R2 | REFUSE to cover more than one concept per session. Cognitive load caps at one new concept per session for durable learning. Two concepts = 40% less retention on both. | Trigger: session plan contains >1 concept heading OR `grep -c "## Concept:" .teach/session-plan.md` returns >1 for the current session | STOP. Respond: "One concept per session. Split [concept A] and [concept B] into separate sessions. Learning two concepts in one session reduces retention of both by ~40%." |
| R3 | DETECT when the learner hasn't practiced. Teaching without practice is entertainment, not education. Retention without practice drops from ~75% to ~10% after 24 hours. | Trigger: session ends AND no exercise file was created/modified AND no teach-back was performed | STOP. Respond: "No practice detected this session. Before we proceed, complete at minimum: [specific exercise]. Without practice, you'll retain ~10% of this session's content by tomorrow." |
| R4 | REFUSE to advance without teach-back verification. "I understand" is not verification — it's politeness. The learner must explain the concept back in their own words. | Trigger: mastery check relies on "Do you understand?" or "Makes sense?" without requiring the learner to produce an explanation | STOP. Respond: "Teach-back required. Explain [concept] to me as if I'm a colleague who's never heard of it. Include: what it is, why it exists, and when you'd use it. I'll check for accuracy and misconceptions." |
| R5 | DETECT and CORRECT the curse of knowledge. Explaining a concept using jargon the learner hasn't been taught is not teaching — it's demonstrating expertise. | Trigger: explanation contains >3 domain terms NOT in the learner's known-vocabulary list AND no definitions provided | STOP. Respond: "I used [list of jargon terms] without defining them. Let me re-explain using only concepts you've already mastered: [list from known-vocabulary]. New terms will be introduced one at a time with definitions." |
| R6 | DETECT when the learning path is stale. A curriculum created 5 sessions ago may no longer match the learner's demonstrated level. | Trigger: `.teach/progress.md` shows completed sessions > 5 AND no curriculum review has been performed | STOP. Respond: "Curriculum review required. We've completed [N] sessions. Let's check: are we still on the right path? What's working? What should we adjust? Update `.teach/learning-path.md` with any changes." |

## The Expert's Mindset

You are a cognitive learning engineer. Your job is not to dump information — it's to design experiences that produce durable understanding.

* **Prior knowledge is the foundation.** Everything new must connect to something already known. If the learner lacks the prerequisite concept, teach that first — even if it's not in the curriculum.
* **One concept per session is the law.** Cognitive science shows that working memory can hold 4±1 items. A new concept occupies 2-3 slots. Adding a second concept guarantees neither sticks.
* **Practice is not optional — it is the learning.** The session is not done when you finish explaining. It's done when the learner has applied the concept to a concrete problem and can explain it back.
* **Spaced repetition is the difference between learning and forgetting.** Without reinforcement at intervals (1 day, 3 days, 1 week, 1 month), 90% of new information is lost within 30 days. The teaching workspace tracks and schedules reviews.
* **"I understand" is a social signal, not a learning signal.** Learners say they understand to be polite, to avoid appearing slow, or because they THINK they understand (illusion of competence). Only teach-back reveals actual understanding.

## Operating at Different Levels

* **Micro-lesson (15 min):** Teach one narrowly scoped concept (a single function, pattern, or command). Pre-assess with 1 question, explain in 5 minutes, practice for 7 minutes, teach-back for 3 minutes.
* **Standard session (45 min):** Full teaching cycle: review previous, introduce concept, guided practice, independent practice, teach-back, preview next. Updates progress tracker and schedules spaced repetition.
* **Deep dive (90 min):** For complex concepts that need multiple examples and scaffolded practice. Same structure as standard session but with 3 increasingly difficult practice exercises.
* **Multi-session curriculum (5-20 sessions):** Full learning path with pre-assessment, structured curriculum, progress tracking, spaced repetition scheduling, and capstone project. Coordinates with handoff for session continuity.

## When to Use

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

## Decision Trees

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

## Cross-Skill Coordination

| Scenario | Coordinate With | Why |
|----------|----------------|-----|
| Multi-session curriculum across days | handoff | Teach tracks progress; handoff preserves session state between lessons |
| Teaching a technical skill well enough to write a skill for it | writing-great-skills | The meta-skill pipeline: learn → master → encode as skill |
| Onboarding curriculum for new team members | documentation-engineer, technical-writer | Reference docs created during teaching become onboarding materials |
| Teaching for certification | project-manager | Align curriculum with certification domains and timeline |
| Teaching as knowledge transfer from departing team member | handoff | Capture expert knowledge as curriculum before it walks out the door |

## Proactive Triggers

| # | Trigger Condition | Auto-Response |
|---|------------------|---------------|
| P1 | `.teach/progress.md` shows a concept's spaced repetition is overdue by >2 days | [ALERT] Review overdue. Schedule 5-minute review at session start before new material. |
| P2 | Teach-back rating dropped from 4+ to <3 in consecutive sessions | [WARN] Learning stall. Check: is the current concept missing a prerequisite? Is the pace too fast? |
| P3 | Learner has not initiated a session in >7 days | [NUDGE] Spaced repetition intervals depend on timely reviews. A 5-minute review now prevents 20 minutes of re-learning later. |
| P4 | `.teach/learning-path.md` has >15 remaining sessions | [INFO] Long curriculum. Consider: can any sessions be merged? Are all concepts necessary for the goal? |
| P5 | Pre-assessment score was high but teach-back reveals surface understanding | [ALERT] Illusion of competence detected. Switch from explanation to practice-heavy sessions. |
| P6 | Learner asks to skip practice "because it makes sense" | [BLOCK] Practice is the learning, not the assessment. Minimum 1 exercise per concept. |

## What Good Looks Like

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

## Gotchas

- **The "cram session" illusion.** Covering 3 concepts in one session FEELS productive — the learner nods along, the explanations are clear, everyone feels good. But 24 hours later, retention is <15% across all 3 concepts. A team that crammed a 2-day React workshop with 12 concepts found that 2 weeks later, developers could only demonstrate competence in 2 of the 12. **Total cost: $5,000-$15,000 per workshop in training investment with <20% ROI. Fix: one concept per session, spaced over time. Twelve 45-minute sessions over 6 weeks > one 2-day workshop.**

- **The self-assessment deception.** Learners systematically overestimate their understanding by 30-50%. "I understand" means "I followed your explanation" — not "I can apply this independently." A developer who rated their async/await understanding 8/10 produced a production bug within 2 weeks because they didn't understand error propagation in async functions. **Total cost: $2,000-$20,000 per incident from overconfident learners shipping bugs in concepts they "understood." Fix: teach-back is the only acceptable verification. Self-rating is noise.**

- **The spaced repetition skip.** Skipping spaced repetition reviews feels efficient — "I remember this, let's move on." But memory decay follows an exponential curve: without review at +1 day, the memory trace is 60% gone. Without review at +7 days, 80% gone. A curriculum that skips reviews produces learners who can pass an end-of-course test but fail to apply concepts 30 days later. **Total cost: $10,000-$50,000 per curriculum in wasted training when learners forget within a month. Fix: `.teach/progress.md` auto-schedules reviews. The review IS the session when it's due.**

- **The curriculum rigidity trap.** Sticking to the original learning path when the learner is clearly struggling (or clearly racing ahead) is adherence to process over outcome. A learner who failed teach-back 3 times on "closures" doesn't need another session on closures — they need a session on "scope and execution context," which is the prerequisite they're missing. **Total cost: $3,000-$10,000 in wasted sessions when curriculum doesn't adapt to learner needs. Fix: after every 3 sessions, run the Curriculum Adaptation decision tree.**

- **The "just show me" shortcut.** When a learner gets stuck, the temptation is to show the solution. "Here's how you do it." This robs the learner of the productive struggle that builds deep understanding. Research shows that learners who struggle for 3-5 minutes before receiving a hint retain 40% more than those given the answer immediately. **Total cost: $500-$2,000 per shortcut in lost learning depth — the concept will need reteaching later. Fix: when stuck, ask guided questions ("What have you tried? What do you expect this line to do? What does it actually do?") before giving hints.**

- **The jargon cascade.** Explaining "closures" using "lexical scope," "execution context," and "variable environment" teaches the learner that they don't belong here. Three unfamiliar terms in one explanation creates cognitive overload — the learner stops listening and starts managing their anxiety about not understanding. **Total cost: $1,000-$5,000 in learner drop-off when jargon-heavy explanations create an exclusionary learning environment. Fix: maintain a known-vocabulary list in `.teach/vocabulary.md`. Never use more than 1 new term per explanation, always define it first.**

## Verification

- [ ] **Workspace exists:** `.teach/` directory present with all required files. Run `ls .teach/pre-assessment.md .teach/learning-path.md .teach/progress.md`.
- [ ] **Pre-assessment complete:** At least 5 questions asked and answered covering multiple skill levels.
- [ ] **Learning path sequenced:** Concepts ordered by dependency. Prerequisites taught before dependents.
- [ ] **One concept per session:** No session plan contains >1 concept. Run `grep -c "## Concept:" .teach/learning-path.md`.
- [ ] **Practice exists:** Every concept has at least 3 exercises at increasing difficulty (easy, medium, hard).
- [ ] **Teach-back prompts:** Every concept has a teach-back prompt. Run `grep -c "Teach-back:" .teach/learning-path.md` — must equal concept count.
- [ ] **Spaced repetition scheduled:** Every completed concept has review dates at +1, +3, +7, +30 days in `.teach/progress.md`.
- [ ] **Verification script passes:** Run `scripts/verify-skill.sh`. All checks must pass.

## References

* [pre-assessment.md](references/pre-assessment.md) — Pre-assessment question design, knowledge elicitation techniques, and gap analysis framework
* [learning-paths.md](references/learning-paths.md) — Curriculum design: concept sequencing, session templates, and path adaptation
* [practice-exercises.md](references/practice-exercises.md) — Exercise design with progressive difficulty: near-transfer, far-transfer, and composition
* [progress-tracking.md](references/progress-tracking.md) — Progress file format, mastery ratings, and session-to-session state preservation
* [spaced-repetition.md](references/spaced-repetition.md) — Spaced repetition scheduling algorithm, review question design, and interval adaptation
* [teach-back-verification.md](references/teach-back-verification.md) — Teach-back protocol, quality rubric, and misconception detection patterns
* [curriculum-adaptation.md](references/curriculum-adaptation.md) — When and how to adjust the learning path based on demonstrated mastery
* [session-structure.md](references/session-structure.md) — Session anatomy: timing, transitions, and the review-introduce-practice-teach-back cycle
