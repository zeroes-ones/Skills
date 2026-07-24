# Spaced Repetition

## The Forgetting Curve

Without reinforcement, newly learned information decays on an exponential curve:
- After 1 day: ~40% retained
- After 3 days: ~25% retained
- After 7 days: ~15% retained
- After 30 days: ~5% retained

Spaced repetition interrupts this curve by recalling information just before it's forgotten, strengthening the memory trace each time.

## Scheduling Algorithm

```
Initial intervals: +1 day, +3 days, +7 days, +30 days

At each review:
  RECALLED SUCCESSFULLY → Double the interval: +6d, +14d, +60d, +120d
  FORGOTTEN (could not recall) → Reset to +1 day. Flag for mini re-teach.
  PARTIAL RECALL (hesitant, incomplete) → Keep same interval. Note weak areas.
```

## Review Question Design

A good review question:
1. Requires active recall (no notes, no code completion)
2. Tests the core concept, not trivia
3. Has one correct answer but encourages explanation
4. Takes <2 minutes to answer

### Example
```
REVIEW: Promises (taught 07-20, review at 07-21)

Question: "You need to fetch data from 3 APIs and combine the results.
           Write the code structure. What happens if one API fails?"

Expected: Shows Promise.all with .then() or async/await. Mentions that
          Promise.all fails fast — one rejection rejects all. Alternative:
          Promise.allSettled for partial success.
```

## Review Workflow

1. **Ask the review question** — no warm-up, no hints
2. **Wait for response** — do not interrupt or scaffold
3. **Evaluate:** RECALLED / PARTIAL / FORGOTTEN
4. **If FORGOTTEN:** 2-minute mini re-teach with a different example
5. **Update schedule:** Adjust interval in `.teach/progress.md`

## When Reviews Are Overdue

If a review is >2 days past due:
- Do NOT skip it — the memory trace is critically weak
- Shorten the review to 2 minutes
- If forgotten, reset to +1 day regardless of previous interval
- Review at START of next session before new material

## Review Stack Limit

Maximum 5 active reviews per session. If more are due:
1. Prioritize: most recently taught first (highest decay risk)
2. Defer older, well-established concepts (long intervals = stronger memories)
3. Schedule catch-up reviews in a dedicated review-only session
