# Description Design

## The Triggers-Only Rule

The description field must describe only SITUATIONS that trigger the skill — never the PROCESS the skill follows.

### Correct (Situation Triggers)
"Use when managing personal finances, building a budget, or planning for retirement."

### Incorrect (Process Trigger)
"Use when you need to calculate your net worth by summing assets and liabilities."

The model matches on "managing personal finances" (situation) but not "calculate net worth" (process). By the time the user says "calculate net worth," the model has already started doing it itself.

## The Three-Part Format

```
Use when [trigger situation 1]; [trigger situation 2]; or [trigger situation 3].
Handles [capability 1], [capability 2], [capability 3].
Do NOT use for [boundary 1] (route to [other-skill]), [boundary 2] (route to [other-skill]).
```

## Trigger Quality Checklist

- [ ] Can the user recognize they're in this situation WITHOUT knowing how the skill works?
- [ ] Are there at least 3 distinct trigger situations?
- [ ] Is each trigger a situation, not a task?
- [ ] Would the description match a real user message?

## Boundary Specification

Every boundary must:
1. Name what the skill should NOT be used for
2. Route to a specific alternative skill
3. Never leave a boundary orphaned ("don't use for X" with no alternative)

### Correct
"Do NOT use for corporate FP&A (route to fp-and-a-analyst)."

### Incorrect
"Do NOT use for business finances." (No alternative route)

## Common Description Mistakes

| Mistake | Example | Fix |
|---------|---------|-----|
| Process as trigger | "Use when creating a budget spreadsheet" | "Use when your spending exceeds your income and you need a structured plan" |
| Vague triggers | "Use when you need help" | "Use when managing personal finances, investing, or planning retirement" |
| Missing boundaries | No "Do NOT use" section | Always specify at least 2 boundaries |
| Orphan boundaries | "Don't use for X" with no alternative | "Don't use for X (route to specific-skill)" |
| Feature list as triggers | "Use when you want: feature 1, feature 2..." | Features go in "Handles"; triggers are situations |
