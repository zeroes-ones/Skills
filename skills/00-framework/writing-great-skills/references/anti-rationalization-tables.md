# Anti-Rationalization Tables

## What They Are

Anti-rationalization tables preempt the model's tendency to rationalize away constraints. They use an "Excuse | Reality" format that names the rationalization the model is likely to generate and counters it with the reality.

## Format

```markdown
| Excuse (What the model tells itself) | Reality (What's actually true) |
|--------------------------------------|-------------------------------|
| "I'll remember what to do next" | Context windows are ephemeral; you won't |
| "The git log tells the story" | Git shows what changed, not why or what's left |
| "It's only a short break" | Short breaks become long breaks; the ledger costs 2 minutes |
```

## When to Use

- When a constraint is likely to be rationalized away ("this doesn't apply right now")
- When the model has a known tendency to skip steps
- When past skill invocations showed the model ignoring a rule
- In the Ground Rules section for safety-critical constraints
- In Gotchas for learn-from-experience patterns

## Design Principles

1. **Name the rationalization exactly.** Use phrasing the model would actually generate internally.
2. **Counter with concrete reality.** Not "this is bad practice" but "context windows are ephemeral; you won't."
3. **Keep pairs compact.** Each excuse-reality pair should be <50 words total.
4. **Target known failure modes.** Don't invent rationalizations — use ones you've observed.

## Where to Place

- In **Ground Rules** → for safety constraints that must never be violated
- In **Gotchas** → for failure patterns with dollar-quantified costs
- In **Reference files** → for domain-specific rationalizations the model generates

## Anti-Patterns

| Anti-Pattern | Why It Fails |
|-------------|--------------|
| Generic excuses | "I'll do it later" applies to everything; name the specific context |
| Reality is motivational | "You can do it!" is not a counter-argument; use concrete consequences |
| Too many pairs | >10 pairs = the model ignores the table; limit to the most dangerous rationalizations |
| No observed basis | Inventing rationalizations the model doesn't actually generate wastes tokens |
