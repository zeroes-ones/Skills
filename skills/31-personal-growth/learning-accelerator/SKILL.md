---
name: "learning-accelerator"
description: "Use when accelerating skill acquisition. Handles meta-learning audits, spaced repetition, memory palaces, deliberate practice, Feynman technique, interleaving, retrieval practice, Zettelkasten synthesis, and plateau-busting. Do NOT use for formal curriculum design or corporate training."
license: MIT
author: Sandeep Kumar Penchala
type: personal-growth
status: stable
version: 1.0.0
updated: 2026-08-02
tags: [meta-learning, spaced-repetition, anki, memory, zettelkasten, deliberate-practice, transfer]
token_budget: 4000
chain:
  consumes_from: [productivity-master]
  feeds_into: [decision-engineer]
  alternatives: []
---
# Learning Accelerator
Portability: personal-growth / study workflows

<!-- QUICK: 30s -->
One-line: A compact skill-acquisition system combining spaced repetition + deliberate practice + knowledge synthesis for durable learning and transfer.

## RESEARCH_PREREQUISITE
| Code | Requirement |
|------|-------------|
| RP1  | Defined target skill & performance goal |
| RP2  | 30–60 minute initial study block available |
| RP3  | Anki (or SRS) installed or note tool for flashcards |
| RP4  | Collection of core learning materials (3 sources) |
| RP5  | A practice environment or coach where possible |
| RP6  | Willingness to schedule 20–60 minute daily practice |
| RP7  | Ability to record short teaching sessions (video/notes) |
| RP8  | Storage for a Zettelkasten or notes vault |

## Iterative Research Loop
| Loop | Purpose | Input | Output |
|------|---------|-------|--------|
| 0 | Skill definition | Performance goal | Observable behaviors to train |
| 1 | Micro-skills mapping | Task decomposition | Drill list and metrics |
| 2 | SRS build | Core facts & mnemonics | Anki deck / spaced plan |
| 3 | Synthesis & transfer | Notes and practice logs | Zettelkasten notes and demonstration |

## Quickstart (30s)
1. Write the target skill and a measurable performance outcome.
2. Create 5 flashcards capturing core facts or steps.
3. Schedule 20 minutes daily for practice starting today.
4. Teach the first concept to an imaginary student for 5 minutes (Feynman).

<!-- STANDARD: 3min -->
## Ground Rules
- Mechanical triggers: after each practice session, record one micro-improvement.
- Negative constraints: avoid broad passive reading without retrieval practice.
- Fidelity: start with smaller, high-feedback drills rather than large unguided practice.
- Review cadence: daily SRS + weekly deliberate practice + monthly consolidation session.

## Decision Tree (deeper)
Start
|
+- Is the skill mostly declarative? -> Yes -> Build SRS deck (facts, definitions) -> Add cloze cards
|                                 -> No -> Emphasize drills, deliberate practice, and feedback loops
|
+- Plateau after 2 weeks? -> Yes -> Add interleaving, variability, and error-seeking practice
|                         -> No -> Continue progression and increase difficulty gradually
|
+- Need transfer to real-world? -> Yes -> Create applied project and teach-back -> Measure performance
|                             -> No -> Continue focused drills

## Core Workflow
STANDARD: Skill definition & micro-skills
1. Define a clear performance metric and a minimum viable demonstration (e.g., "deliver a 10-min talk with 3 takeaways", or "solve 10 problems in 30 minutes").
2. Decompose into micro-skills and prioritize drills by leverage and feedback quality.

STANDARD: Deliberate Practice
1. Pick the highest-leverage micro-skill and design focused drills with immediate feedback.
2. Ensure a feedback loop: self-record, tutor feedback, or automated check (unit tests, scored problems).
3. Use short, frequent sessions with rest and reflection.

STANDARD: Spaced Repetition & Memory
1. Convert objective facts and procedural steps into cloze/deletion flashcards.
2. Use initial dense reviews over the first days, then rely on SRS for spacing.
3. For sequences and numbers, consider Memory Palace (method of loci) or PAO for ordered recall.

DEEP: Knowledge Synthesis <!-- DEEP: 10+min -->
1. Use Zettelkasten permanent notes: Atomic note, unique ID, one idea per note, linked to related notes.
2. After practice sessions, create a synthesis note with: what worked, surprising errors, concepts to test, and an experiment.
3. War story: a learner built Zettelkasten notes tied to weekly practice and discovered cross-domain analogies that accelerated transfer (math techniques applied to programming optimization problems).
4. Edge case: when evidence is scarce, tag notes as "hypothesis" and schedule tests.
5. Exercise: after a practice week, write three permanent notes linking drills, feedback, and an experiment to validate.

DEEP: Plateau Breaking <!-- DEEP: 10+min -->
1. Introduce interleaving: alternate related skill drills to force discrimination and contextual retrieval.
2. Increase variability: practice under different constraints (time pressure, altered tools, different problem sets).
3. Use deliberate error-seeking: design drills to provoke common mistakes and practice recovery.
4. Failure narrative: a violinist practiced only slow scales and struggled with tempo; adding variable-speed drills and metronome practice broke a plateau within weeks.
5. Exercise: replace 20% of drill time with interleaved tasks for 2 weeks; expected outcome: improved generalization.

## Expanded Error Decoder (5-8 rows)
| Error Message / Pitfall | Root Cause | Fix | Lesson |
|-------------------------|------------|-----|--------|
| "I forget everything after a week" | No spaced repetition or poor encoding | Create minimal Anki deck, use cloze cards and daily reviews | Spacing + good encoding is necessary for retention |
| "Practice feels stagnant" | No feedback or unrealistic drills | Add objective feedback, shorten feedback loop, escalate difficulty | Feedback is the engine of improvement |
| "Too many resources, no focus" | Lack of clear target | Pick 1–2 core sources and a performance metric; ignore others | Constraints accelerate progress |
| "I plateaued despite hours" | Low-quality practice or lack of variability | Introduce interleaving, feedback, and deliberate error practice | Hours must be deliberate and targeted |
| "Transfer fails" | Isolated practice, no applied projects | Build applied projects and teach-backs to force transfer | Transfer requires context and retrieval practice |
| "Card overload" | Overproduction of SRS cards | Pare deck to the essentials and use hierarchical note linking | Quality > quantity for recall cards |

## Best Practices (8-10)
1. Start with a clear performance metric (observable and measurable).
2. Use micro-goals: 1–2 drills per session with clear feedback.
3. Build a minimal SRS deck for core declarative facts; avoid turning everything into cards.
4. Combine SRS with applied deliberate practice — one supports the other.
5. Teach weekly (Feynman) to expose gaps and consolidate understanding.
6. Use evidence logs: record date, drill, metric, feedback, and actionable insight.
7. Prioritize high-feedback environments (coaches, tests, code judges) when possible.
8. Schedule periodic consolidation weeks to integrate notes into Zettelkasten and plan experiments.
9. Avoid resource glut: limit new material intake to 1–2 sources per month.
10. When stuck, perform a week-long diagnosis: measure practice quality, feedback, and variability.

## Production Checklist (12 items)
- [ ] Performance metric defined and documented
- [ ] Micro-skill decomposition completed
- [ ] Minimal Anki/SRS deck created for declarative essentials
- [ ] 4-week practice schedule (daily slots) set
- [ ] Feedback source identified (coach, peer, auto tests)
- [ ] Evidence log template created
- [ ] Zettelkasten vault initialized and linked to practice notes
- [ ] One applied project defined for transfer testing
- [ ] Two teach-back sessions scheduled in first 4 weeks
- [ ] Interleaving plan defined for week 3 onward
- [ ] Error-seeking drills defined for common mistakes
- [ ] Monthly consolidation & reflection slot scheduled

## Metrics & Measurement (concrete)
- Drill accuracy: % correct on targeted drills (target: +15% relative improvement in 4 weeks).
- SRS retention: retention rate for core cards (target >=80% over 30 days).
- Transfer test score: performance on applied project or test (target: pass threshold within 8 weeks).
- Feedback rate: number of corrective feedback instances per practice hour (target >=1/30 min).
- Time-on-task quality: ratio of deliberate practice minutes to total practice minutes (target >=0.75).

## Exercises & Templates
Exercise 1 — 10-minute Feynman drill
1. Pick a concept and write an explanation as if teaching a 12-year-old for 5 minutes.
2. Identify jargon and replace with simple language; note gaps and schedule 2 drills to fix.
Expected outcome: 1–2 targeted gaps to practice.

Exercise 2 — 15-minute SRS microdeck
1. Create 5 cloze cards from the current week's key facts.
2. Do a single review session and schedule daily SRS for next 7 days.
Expected outcome: immediate familiarity and retention startup.

Template: Evidence Log (one line per session)
- Date | Skill | Drill | Duration | Metric | Feedback | Next action

## Decision Tree (applicability)
Start
|
+- Skill type: Declarative? -> Yes -> Build SRS + light drills
|                        -> No -> Prioritize deliberate practice
|
+- Facing plateau? -> Yes -> Introduce interleaving & variability
|                 -> No -> Continue scaling difficulty
|
+- Need performance under pressure? -> Simulate test conditions and teach-back
|
## Cross-Skill Coordination (expanded)
| Skill | Role | Coordination Pattern |
|-------|------|----------------------|
| productivity-master | Scheduling | Reserve deep practice blocks and enforce recovery windows |
| decision-engineer | Prioritization | Help prioritize learning investments and run EV analysis for time allocation |
| life-architect | Alignment | Ensure chosen skills map to long-term vision and portfolio needs |

## What Good Looks Like (concrete)
- After 8 weeks: measurable improvement on drill metrics (>=15% improvement) and SRS retention >=80%.
- Transfer: successful application of skill in a real or simulated task with pass threshold met.
- Evidence: organized Zettelkasten entries linking concepts, drills, and experiments.

## References (5-8)
- Ericsson, A., Krampe, R., & Tesch-Römer, C. (1993). The role of deliberate practice in the acquisition of expert performance. Psychological Review.
- Oakley, B. & Sejnowski, T. (2018). Learning How to Learn.
- Roediger, H. L., & Butler, A. C. (2011). The critical role of retrieval practice in long-term retention. Trends in Cognitive Sciences.
- Ahrens, S. (2017). How to Take Smart Notes (Zettelkasten method).
- Tools: Anki, SuperMemo, Obsidian, Toggl, feedback platforms (Codewars, LeetCode for programming).

## Scale Depth (expanded)
Solo: personal Anki deck, applied project, weekly teach-back; tools: Anki, Obsidian.
Small: peer practice pods and reciprocal feedback; tools: Zoom recordings, shared evidence logs.
Medium: cohort-based accelerator with mentors, assessment rubrics, and benchmarks; tools: LMS + cohort dashboards.
Enterprise: route to internal learning teams to scale curriculum with measurement systems.

## Anti-Hallucination
- [VERIFIED] Deliberate practice and spaced repetition are strongly supported by research for skill retention.
- [COMMON-PRACTICE] Zettelkasten aids long-term synthesis for creative connections.
- [INFERRED] Error-seeking practice accelerates robustness but needs careful framing to avoid demotivation.
- [UNKNOWN] Exact SRS parameters (ease factors) should be tuned per individual and material.
