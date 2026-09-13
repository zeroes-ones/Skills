# Coherence Models — how layered caches stay consistent (Decision Tree 3)

> Multi-layer caches need *both* a precedence rule (which layer wins) and a propagation rule (how
> invalidation moves between them). Either one alone leaves an observable state that matches nothing
> in the system (R5).

---

## The coherence models

| Model | Rule between layers | Requires | Fails when |
|-------|--------------------|----------|-----------|
| **Single-writer** | Exactly one layer may write; others read through | Discipline that no other layer fills independently | A second layer starts writing "temporarily" and never stops |
| **TTL-ordered** | Inner layer's TTL < outer layer's TTL, strictly | A documented ordering and a test for it | The ordering is assumed, not asserted; an outer layer outlives the inner and serves older data |
| **Event-propagated** | Invalidation is broadcast to every layer | A broker the layers all subscribe to | A layer misses the event and has no TTL bound on how long it stays wrong |
| **Version-stamped** | Every value carries a version; readers take the highest | Clock-independent versioning (do not use wall clocks) | Versions are compared across layers that never saw the same history |
| **Read-through only** | Only the innermost layer holds state; outer layers are pure policy | No independent state in outer layers | A CDN or browser caches content it is not supposed to hold |

**The rule to write down.** For each layer: *which* layer wins on conflict, and *how* an invalidation
reaches it. If either answer is "it'll expire eventually", the model is undefined (R5).

---

## Propagation is a measurement, not an assumption

The staleness budget (R4) is only meaningful if propagation is inside it. Record the observed
propagation time per layer, in order (browser → CDN → service), and make it the input to the budget
rather than a guess — see `verification-recipes.md` §4.3.
