# Throwaway Discipline: The Psychology of Disposal

## Why We Resist Throwing Away Code
- **Sunk cost fallacy:** "I spent time on this, it must have value." Time spent ≠ value created.
- **Perfectionism:** "If I just clean it up a bit..." The cleanup instinct is how prototypes become production code.
- **Organizational pressure:** "We need to ship fast, can't we use what we have?" Shipping prototype code is borrowing time at 500% interest.
- **Attachment:** "This is clever code." Clever prototype code is the most dangerous — it's clever in isolation, catastrophic in production.

## Disposal Rituals
1. Document the decision (the artifact is the decision, not the code).
2. Commit the decision document to the main repo.
3. Delete the prototype directory.
4. Verify deletion: `ls [prototype-path]` returns "No such file or directory."
5. (Optional) Celebrate. Negative results are victories — they eliminated a wrong path.

## Organizational Culture Change
- Celebrate disposal as completion, not deletion as loss.
- Track "prototype survivorship" as a metric. Goal: 0 prototype files in production.
- Post-incident: check if the incident traces to prototype code. If yes, add to the case study catalog.
