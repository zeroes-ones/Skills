# How Bloom Filters Work — The "Definitely No" Data Structure

> Original explainer for interview prep and learning. [research-source: title-only]

## What a Bloom filter is

A Bloom filter is a space-efficient probabilistic set. It answers one question: **"is X in the set?"** with two possible answers: **"definitely not"** (never wrong) or **"probably yes"** (may be wrong — a **false positive**). There are no false negatives. It uses far less memory than storing the actual elements, at the cost of a tunable false-positive rate.

## How it works (the core idea)

1. Start with a **bit array of m bits**, all 0.
2. Choose **k hash functions**. To add an element, set the k bits `h₁(x) … hₖ(x)` to 1.
3. To query an element, check the same k bits: if **any is 0** → definitely not present. If **all are 1** → probably present (the bits may have been set by other elements — that's the false positive).

**Why false positives happen:** different elements can set overlapping bits; an element never added can still find all its k bits set by others.

## The math (interviewers like the intuition, not the formula)

- False-positive rate ≈ `(1 − e^(−kn/m))^k`, minimized around **k = (m/n)·ln 2** hash functions.
- Memory vs accuracy: ~**10 bits per element** gives ~1% false positives; ~5 bits gives ~10%. Space grows linearly with `n`, independent of element size — a 1 GB element costs the same as a 1-byte key.
- The trade-off axis: **m/n (memory per element)** and **k (hash count)** set the false-positive rate; more memory or more hashes → fewer false positives (up to the optimum k).

## Why it's used (classic applications)

| Application | What the filter saves |
|---|---|
| **Cache protection / "never cache miss to DB"** | If a key is definitely-not-cached, skip the DB lookup for nonexistent keys (avoids cache-penetration storms on hot missing keys) |
| **Spell checkers / word lists** | Space-efficient "is this a known word" pre-check |
| **Databases (LSM trees, e.g., LevelDB/RocksDB, Cassandra)** | Before reading a file/SSTable, "could this key exist here?" — skips most disk reads |
| **Content/URL dedupe (crawlers)** | "Have we seen this URL?" — false positives just mean a wasted re-check |
| **Distributed caches / CDN** | Cheap "maybe exists" gate at the edge |
| **Blocked lists** | "Is this ID blocked?" with tiny memory (false positive = harmless re-check) |

The unifying pattern: **avoid an expensive lookup when the answer is cheaply "definitely no."**

## Limitations (know these so you don't over-sell it)

- **No deletion** (standard Bloom filter). Deleting requires a **counting Bloom filter** (counters instead of bits) or a different structure (Cuckoo filter) — at more memory.
- **No enumeration** — you can't list members; it only answers membership queries.
- **False positives are tunable but never zero.** When a "probably yes" matters, follow with a real lookup.
- **Adding many elements degrades the rate** — size `m` for the expected max `n` up front.

## Interview answer skeleton

"A Bloom filter is a probabilistic membership set: k hashes set k bits, and a query is 'definitely no' if any bit is 0, 'probably yes' if all are set — so false positives exist but false negatives don't. Memory is ~m/n bits per element regardless of element size, with the false-positive rate tuned by m and k. I use it to gate expensive lookups — cache-penetration checks, DB SSTable reads, dedupe — where a rare false positive just triggers a harmless follow-up check."

## Anti-patterns

- ❌ Using it where a false positive has real cost (e.g., authorizing access) — the "probably yes" must always be verified.
- ❌ Forgetting it can't delete elements, then needing removals.
- ❌ Sizing `m` for today's `n` and letting the FP rate climb as the set grows.
- ❌ Claiming it stores elements — it stores only membership evidence.

## Deliberate-practice drills

1. **Hand-simulate:** m=8 bits, k=2 hashes; add "cat","dog"; query "cat", "fox" (a false positive); explain why.
2. **Tuning drill:** for n=1M elements at 1% FP, estimate m and k; verify with the formula.
3. **Design drill:** cache-penetration protection for a key-value cache — where exactly does the filter sit and what does a 'probably yes' do?
4. **Limits drill:** when would you need a counting/Cuckoo filter instead?
5. **Interview drill:** "how do you stop a hot missing key from hammering your DB?" — answer with the Bloom filter gate.

## References
- See also: redis-use-cases.md, distributed-systems-101.md (this repo)
- `database-designer` SKILL.md — indexing, LSM/read-path optimization
- `performance-engineer` SKILL.md — avoiding redundant work
