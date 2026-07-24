# Leading Words

## What Are Leading Words?

Compact pretrained concepts that anchor model behavior in the fewest possible tokens. Instead of explaining "test-first development" in 200 words, you write "red-green-refactor" — the model already knows what this means from its training data.

## Leading Word Catalog

| Leading Word | Tokens Saved | What It Anchors |
|-------------|-------------|-----------------|
| red-green-refactor | ~150 | Test-driven development cycle |
| tracer bullet | ~200 | End-to-end thin slice before depth |
| tight loop | ~100 | Rapid iteration with fast feedback |
| strangler fig | ~250 | Incremental legacy system replacement |
| circuit breaker | ~180 | Failure isolation pattern |
| bulkhead | ~150 | Resource isolation pattern |
| two-phase commit | ~200 | Distributed transaction protocol |
| eventual consistency | ~150 | Distributed data consistency model |
| single source of truth | ~100 | No duplication principle |
| progressive disclosure | ~150 | Information architecture pattern |
| diminishing returns | ~100 | Cost-benefit inflection point |
| curse of knowledge | ~120 | Expert-blindness cognitive bias |

## When to Use Leading Words

- The concept is well-known in the domain
- Explaining it would cost 100+ tokens
- The model's training data reliably includes the concept
- The concept is stable (won't change meaning)

## When NOT to Use

- Domain-specific jargon the model might not know
- Concepts you invented (not in training data)
- Ambiguous terms with multiple meanings
- Terms that differ across ecosystems (e.g., "service" means different things in different contexts)

## Testing Leading Words

To test if a leading word works: replace the explanation with just the leading word. If the model's behavior is identical, the leading word is effective. If behavior degrades, the model doesn't know the term or interprets it differently.
