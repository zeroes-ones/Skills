# Performance at the Boundary

<!-- STANDARD: 3min -- measuring per-crossing cost and counting crossings -->

## The two numbers

```text
per_crossing_cost      the overhead of one crossing, independent of the work
crossings_per_operation how many times the boundary is crossed to do the operation

total_boundary_cost = per_crossing_cost × crossings_per_operation
```

**The second number usually dominates, and it is the one that is rarely measured.** Teams optimise the
first (a faster conversion) while crossing a million times, when a bulk transfer would have removed
999,999 crossings.

This is R2: a boundary with no measured cost cannot be argued about or optimised.

## The measurement harness

```text
Measure these four, in isolation, on a stated machine:

1. Empty crossing         the ABI overhead floor (a no-op call across the boundary)
2. Typical crossing       real arguments, typical payload size
3. The work alone         the same operation in pure language A
4. The work alone         the same operation in pure language B

Then:  is (empty + typical + B_work) < A_work?
       If not, the boundary loses — regardless of B's speed.
```

The empty crossing is the number people forget, and it is the floor: no boundary can be cheaper than it.

## What contributes to the per-crossing cost

| Contributor | Typical order |
|---|---|
| ABI overhead (call setup, register save) | nanoseconds |
| Runtime guard acquisition (GIL, event loop hop) | hundreds of nanoseconds to microseconds |
| Type conversion | nanoseconds to microseconds, per field |
| Memory allocation | microseconds |
| Memory copy | nanoseconds per byte |
| Serialisation | microseconds to milliseconds, per payload |
| Thread marshalling | microseconds, and it serialises |

**The guard hop and the serialisation are the two big ones**, and they are the two that a "just pass a
struct" design ignores.

## Reducing the crossing count

The structural fixes, in order of leverage:

| Fix | Effect |
|---|---|
| **Bulk transfer** instead of per-element crossing | N crossings → 1 |
| **Iterator handle** instead of per-element accessor calls | N crossings → 1 + N cheap moves |
| **Batched calls** (accept an array, return an array) | N calls → 1 |
| **Handle instead of serialisation** | removes the encode/decode per crossing |
| **Warm the path** (attach the thread once, cache the guard path) | removes per-call setup |
| **Amortise** (do more work per crossing) | fewer crossings for the same total work |

**The first three are the ones that produce order-of-magnitude changes.** The others are refinements.

## Reducing the per-crossing cost

| Fix | Effect | Risk |
|---|---|---|
| Remove a copy (borrow instead of copy) | large, for big payloads | lifetime must be proven safe |
| Avoid allocation per crossing (reuse a buffer, use an arena) | large | ownership must be clear |
| Cheaper representation (binary instead of JSON) | medium-large | schema coupling |
| Fewer conversions (fixed layout instead of accessors) | medium | layout brittleness |
| Release the guard around the work | large if the work is long | correctness discipline required |
| Cache the resolved symbol/function pointer | small but free | none |

**Every row trades something.** The measurement is what makes the trade explicit.

## The common defects

| Defect | Symptom | Fix |
|---|---|---|
| Per-element crossing on a large collection | cost grows linearly with collection size, dominated by overhead | bulk transfer or iterator handle |
| Serialising a large object per call | microseconds of encode/decode per call, often more than the work | handle-based access |
| Holding the guard for the whole call | the runtime serialises; throughput collapses under concurrency | release around the work |
| Attaching a thread per call | expensive setup on every call | attach once per thread |
| Allocating a buffer per crossing | allocation cost per call | reuse, or an arena |
| Copying a large payload for safety | the copy dominates | borrow with a proven lifetime |

## Interpreting a profile

When the boundary appears in a profile:

```text
Is the time in the crossing itself (conversion, copy, guard) or in the work?
├── In the crossing → reduce the cost or the count (the fixes above)
└── In the work → the boundary is not the problem; optimise the work

Is the cost O(1) or O(n) in the payload?
├── O(n) → the copy or the serialisation dominates; consider borrowing or a handle
└── O(1) → the overhead dominates; reduce the crossing count

Does the cost scale with thread count?
├── Yes → guard contention; release the guard around the work
└── No  → not a concurrency bottleneck
```

## Reporting

```text
Boundary cost — <capability> — <date>

Harness: <language A> <version> ↔ <language B> <version>, <machine>, <N> iterations, median

| Measurement            | Value      |
|------------------------|------------|
| empty crossing         | 0.31 µs    |
| typical crossing       | 1.9 µs     |
| work in language A     | 480 µs     |
| work in language B     | 61 µs      |
| crossings per operation| 1,024      |
| boundary total         | 1.95 ms    |
| total B                | 2.01 ms    |
| total A                | 0.48 ms    |

Verdict: FFI LOSES for this shape. B's kernel is 8× faster, but 1,024 crossings at
1.9 µs cost 1.95 ms — four times the pure-A total. Fix the crossing count first
(bulk transfer), then re-measure: expected 0.52 ms.
```

That report is the deliverable: two numbers, a verdict, and the structural fix that changes the verdict.

## Checklist

- [ ] The empty crossing and a typical crossing are both measured (R2)
- [ ] The work is measured in both languages, for comparison
- [ ] The crossing count per operation is counted, not assumed
- [ ] The harness and machine are named, so the measurement is repeatable (R5)
- [ ] The boundary's cost is compared against the non-FFI alternative
- [ ] The verdict is stated (FFI wins or loses for this shape), with the numbers
- [ ] Where the boundary dominates, the structural fix (crossing count) is considered before micro-optimisation
- [ ] The result is re-measured after the fix, using the same harness
