# Unknown Discovery

## Known Unknowns vs Unknown Unknowns

- **Known unknowns:** "We don't know which database to use." We know the question, we don't know the answer.
- **Unknown unknowns:** We don't even know what questions to ask. These are the most dangerous — they surface as surprises during implementation.

## Recursive Questioning Technique

For each known unknown, ask: "What would we need to know to answer this?" The answer is a sub-unknown. Then ask again. Repeat until hitting foundational questions — things you can look up or measure directly.

### Example

```
Known unknown: "We don't know which database to use."

Q1: "What would we need to know to answer this?"
A1: "We'd need to know our query patterns."

Q2: "What would we need to know to understand our query patterns?"
A2: "We'd need to know what queries the current system runs."

Q3: "What would we need to know to find that out?"
A3: "We'd need access to production query logs."

→ Foundational question: "Can we get access to production query logs?"
→ Answer: Yes → ticket: analyze query logs
→ Answer: No → UNKNOWABLE with current constraints
```

## Unknown Discovery Triggers

Techniques for finding what you don't know you don't know:

| Technique | Question | Output |
|-----------|----------|--------|
| Boundary probing | "What happens at the edges of this system?" | Edge case unknowns |
| Failure mode analysis | "What are 5 ways this could fail?" | Risk unknowns |
| Assumption hunting | "What are we assuming that might not be true?" | Assumption unknowns |
| Constraint questioning | "What if [constraint] didn't exist?" | Design space unknowns |
| Comparator analysis | "How do similar systems handle this?" | Best practice unknowns |
| Stakeholder interviews | "What keeps you up at night about this?" | Organizational unknowns |

## Unknown Lifecycle

```
UNKNOWN → CLASSIFIED → TICKETED → INVESTIGATING → KNOWN
                                                   ↓
                                             UNKNOWABLE (terminal)
```

## When to Stop Discovering

Stop recursive questioning when:
1. You hit a question that can be answered with a 5-minute search or measurement
2. You hit a question that requires access you cannot get (declared UNKNOWABLE)
3. You've gone 5 levels deep — diminishing returns beyond this point
4. The sub-questions are no longer about the original domain
