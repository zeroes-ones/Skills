# Session Structure

## Session Anatomy

Every teach session follows a rigid structure. Deviation reduces learning effectiveness.

```
REVIEW (5 min) ──→ INTRODUCE (10-15 min) ──→ GUIDED PRACTICE (10 min)
                                                    │
RECORD (2 min) ←── TEACH-BACK (5 min) ←── INDEPENDENT PRACTICE (10-15 min)
```

## Phase Timing (45-Minute Session)

| Phase | Duration | Purpose | Teacher Role |
|-------|----------|---------|-------------|
| Review | 5 min | Reinforce previous concepts, spaced repetition | Question-asker, not explainer |
| Introduce | 10-15 min | Present new concept with motivation and example | Explainer, connector |
| Guided Practice | 10 min | Work through example together | Guide, think-aloud partner |
| Independent Practice | 10-15 min | Learner applies concept alone | Silent observer, hint-giver (only when stuck) |
| Teach-Back | 5 min | Verify understanding | Evaluator, misconception detector |
| Record | 2 min | Update progress, schedule reviews | Scribe |

## Phase Transitions

Transitions are vulnerable moments where learning momentum can be lost.

### Review → Introduce
- Bridge sentence: "Last time we learned [X]. Today we'll build on that with [Y], which solves the problem of [Z]."
- Do NOT: "Any questions before we start?" (invites derailment)

### Introduce → Guided Practice
- "Let's try this together. I'll guide, you drive."
- Open editor/terminal to the starting point

### Guided → Independent
- "Now try this on your own. I'll be here if you get stuck for more than a few minutes."
- Close or minimize your guidance, give the learner full control

### Independent → Teach-Back
- "Great work. Now, imagine I'm a colleague who missed this session. Explain [concept] to me."

### Teach-Back → Record
- "Here's what I heard: [summary]. Here's what we'll cover next time: [preview]."

## Time Management

| Situation | Response |
|-----------|----------|
| Running over on Introduce | Cut the last example (not the motivation or the concept) |
| Guided Practice taking too long | Simplify the example mid-stream: "Let's skip the edge case for now" |
| Independent Practice unfinished | End on time. Unfinished exercise becomes optional homework |
| Teach-back reveals major gaps | Extend session by 10 min for re-teach OR schedule dedicated re-teach session |
| Running short | Add a bonus exercise or preview next concept with "try to guess how this works" |

## Environment Setup

At session start:
1. Verify `.teach/` workspace is intact
2. Check that tools/environment needed for practice are available
3. Confirm `.teach/progress.md` is current
4. Load spaced repetition review queue

At session end:
1. Update `.teach/progress.md` with session results
2. Schedule next spaced repetition reviews
3. If using handoff, update `.handoff/ledger.md`
