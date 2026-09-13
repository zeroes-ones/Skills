# Staleness and TTL — why a TTL without an owner is a decision nobody made

> A TTL is a *statement about acceptable error*, so it converts directly into how much wrong data a
> user can see. This file shows that conversion so the number is chosen deliberately, not by feel.

---

## The arithmetic, worked

```
write rate for a key class      = 40 writes/hour  → 1 write / 90 s
TTL                             = 300 s
average age when a stale read occurs = TTL / 2 = 150 s
probability a random read is stale   ≈ 150 / 90  → > 1 (the entry is stale most of its life)
```

The point is not the exact number — it is that **a 300 s TTL on data written every 90 s means most
reads are of a value that has already changed.** That is a business decision ("users may see a price
that changed two minutes ago"), and R4 requires it be owned. Choosing the number by feel hides the
decision rather than making it.

**The staleness budget is the deliverable.** Write down, per key class, the maximum age a reader may
see, who owns that number, and what alert fires when the observed age exceeds it. A TTL that is not
derived from that budget is a guess wearing a number's clothing.
