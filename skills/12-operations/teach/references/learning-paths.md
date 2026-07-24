# Learning Paths

## Curriculum Design

A learning path is a topologically sorted sequence of concepts where prerequisites are taught before dependents.

## Path Format

```markdown
# Learning Path: [Topic]

## Goal
By the end of this curriculum, the learner will be able to [concrete outcome].

## Prerequisites
- [What the learner must already know before starting]

## Sessions

### Session 1: [Concept Name]
- Prerequisites: [none or concept from previous session]
- Learning objective: "You will be able to [concrete action]"
- Why this matters: [real-world problem this concept solves]
- Approximate time: [15/30/45/90 min]
- Status: [pending | active | completed]

### Session 2: [Concept Name]
...
```

## Sequencing Rules

1. **Foundations first:** Core concepts before advanced patterns
2. **Dependency ordering:** If concept B requires understanding concept A, A comes first
3. **Motivation ordering:** If possible, teach WHY (problem) before HOW (solution)
4. **Complexity gradient:** Each session should be 10-20% harder than the previous
5. **Victory early:** The first session should produce a visible, satisfying result

## Curriculum Templates

### Language Learning (10 sessions)
1. Syntax & types → 2. Control flow → 3. Functions → 4. Data structures → 5. Error handling → 6. I/O → 7. Modules → 8. Testing → 9. Async/concurrency → 10. Ecosystem & tooling

### Framework Learning (8 sessions)
1. Philosophy & mental model → 2. Project structure → 3. Core abstraction → 4. Data flow → 5. Routing/navigation → 6. State management → 7. Testing → 8. Deployment

### Codebase Onboarding (5 sessions)
1. Architecture overview → 2. Development workflow → 3. Key module deep-dive → 4. Testing & debugging → 5. First contribution (guided)

## Adaptation Triggers

| Signal | Action |
|--------|--------|
| 3 consecutive teach-backs rated 5/5 | Accelerate: skip concepts the learner already demonstrates |
| Teach-back drops below 3/5 | Decelerate: add prerequisite session, break concept into smaller pieces |
| Learner asks "why" questions beyond curriculum | Enrich: add advanced optional sessions |
| Learner disengages (short responses, no questions) | Re-engage: check if pace is wrong, goal is still relevant, or external factors |
