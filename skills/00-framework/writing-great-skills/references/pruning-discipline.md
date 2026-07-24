# Pruning Discipline

## The No-Op Test

For every sentence in a skill, ask: "If I delete this sentence, does the model's behavior change?"

- If behavior is IDENTICAL → the sentence is no-op. Delete it.
- If behavior changes → the sentence carries information. Keep it.

## Single Source of Truth

Every concept, rule, or definition appears exactly once in the skill. If it's needed in multiple places:
1. Define it once (authoritative location)
2. Link to it from elsewhere
3. Never copy-paste

Violation example: "Always use parameterized queries" appears in both Ground Rules AND Gotchas. On next edit, one gets updated, the other doesn't → divergence → random model behavior.

## Systematic Pruning Workflow

```
1. NO-OP PASS: Delete every sentence where removal changes nothing
2. SEDIMENT PASS: Move definitions from steps → references
3. DUPLICATION PASS: Consolidate identical content
4. MERGE PASS: Combine similar Ground Rules, Gotchas
5. EXTERNALIZE PASS: Push large reference blocks to references/*.md
6. MEASURE: wc -l body content. If still >500, repeat from step 1.
```

## What NOT to Prune

- Mechanical triggers (required for enforcement)
- Completion criteria (required for step termination)
- Dollar-quantified gotcha costs (required for severity communication)
- Negative constraints in Ground Rules (required for safety)
- Reference links (required for progressive disclosure)

## Pruning Anti-Patterns

| Anti-Pattern | Why It Fails |
|-------------|--------------|
| Pruning all examples | Model loses concrete guidance → behavior degrades |
| Pruning Ground Rules to save tokens | Safety rules are not optional |
| Pruning completion criteria | Steps become un-terminated → model drifts |
| Pruning "just this once" | Sets precedent → skill creeps back within 3 edits |
