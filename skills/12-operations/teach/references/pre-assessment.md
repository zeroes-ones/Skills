# Pre-Assessment

## Purpose

Pre-assessment establishes the learner's actual skill level — not their self-reported level. It identifies knowledge gaps, prerequisite deficiencies, and areas of unconscious competence.

## Question Design Principles

1. **Demonstration over self-rating:** "Write a function that..." not "Rate your skills 1-10"
2. **Edge case probing:** "What happens when [edge case]?" — reveals depth, not just surface knowledge
3. **Multi-level sampling:** At least 1 question at each: beginner, intermediate, advanced, expert
4. **Gap-seeking, not pass/fail:** The goal is to find what they DON'T know, not to grade them
5. **Time-bound:** 5-8 questions, 15-minute limit. Long assessments cause fatigue and disengagement

## Question Template by Level

### Beginner
"What is [core concept]? Can you give an example?"

### Intermediate
"Write a [function/component/query] that [does X]. What would you test?"

### Advanced
"When would you use [pattern A] instead of [pattern B]? What tradeoffs are you making?"

### Expert
"How would you design [system] to handle [failure mode]? What are the hidden costs of your approach?"

## Gap Analysis Output

```markdown
# Gap Analysis: [Topic]

## Goal
[What the learner wants to be able to DO]

## Known
- [Concept]: [demonstrates understanding with example]
- [Concept]: [surface understanding, can state but not apply]

## Gaps
### BLOCKING (prerequisites)
- [Gap]: Cannot proceed without this

### ORDERING (builds on other concepts)
- [Gap]: Depends on [prerequisite concept]

### NICE_TO_HAVE
- [Gap]: Would deepen understanding but not block progress
```

## Common Pre-Assessment Pitfalls

| Pitfall | Why It Fails | Fix |
|---------|-------------|-----|
| "How comfortable are you with X?" | Comfort ≠ competence. People are comfortable with bad habits. | "Show me how you would..." |
| Multiple choice only | Recognition ≠ recall. Multiple choice tests pattern matching, not understanding. | Require open-ended responses |
| Skipping pre-assessment | Teaching at the wrong level wastes the session | Always assess, even if brief (3 questions) |
| Same questions for every learner | Different goals need different baselines | Tailor to the stated learning goal |
