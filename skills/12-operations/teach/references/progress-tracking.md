# Progress Tracking

## Progress File Format

`.teach/progress.md` is the single source of truth for the learner's journey. It survives sessions and enables handoff coordination.

```markdown
# Progress: [Topic]

## Learner
- Name: [optional]
- Started: [YYYY-MM-DD]
- Goal: [concrete outcome]

## Session Log

### [YYYY-MM-DD] Session [N]: [Concept]
- Status: [completed | in_progress | skipped]
- Teach-back rating: [1-5]
- Mastery: [NOT_MASTERED | SURFACE | APPLIED | DEEP]
- Exercises completed: [N]/3
- Notes: [observations, struggles, breakthroughs]

## Spaced Repetition Schedule

| Concept | Taught | +1d | +3d | +7d | +30d | Status |
|---------|--------|-----|-----|-----|------|--------|
| Promises | 07-20 | ✓ | ✓ | 07-27 | 08-19 | ON_TRACK |
| Closures | 07-18 | ✓ | ✓ | ✓ | 08-17 | ON_TRACK |
```

## Mastery Levels

| Level | Description | Teach-Back Indicator |
|-------|-------------|---------------------|
| NOT_MASTERED | Cannot explain or apply the concept | Incorrect explanation, cannot complete Level 1 exercise |
| SURFACE | Can state the concept but cannot apply or connect | Correct definition, cannot complete Level 2 exercise |
| APPLIED | Can apply the concept to familiar problems | Completes Level 1-2 exercises, explains with examples |
| DEEP | Can apply to novel problems and connect to other concepts | Completes all 3 levels, connects to other concepts unprompted |

## Session-to-Session State

Between sessions, `.teach/progress.md` preserves:
- Which concepts have been taught and at what mastery level
- Spaced repetition schedule and review status
- Current position in the learning path
- Any concepts that were re-taught or need re-teaching
- Learner notes and observations

## Coordination with Handoff

When using teach + handoff:
- `.teach/progress.md` → `.handoff/ledger.md` (copy session state)
- `.handoff/ledger.md` → resume command includes `.teach/` path
- After session: update BOTH progress and ledger
