# Marshalling

<!-- STANDARD: 3min -- data shapes, conversion cost, handles versus structures versus serialisation -->

## The four shapes, ranked by cost

| Shape | Per-crossing cost | Stability | Use when |
|---|---|---|---|
| **Primitives** | lowest — a register or stack slot | highest | the data genuinely is a few scalars |
| **Handle** (opaque reference) | very low — one word | high (layout private) | an object, not its contents, is what crosses |
| **Structure by layout** | low — no conversion | **brittle** — layout must match exactly | both sides share an ABI and you assert the layout |
| **Structure by accessors** | moderate — one call per field | high | a structure must cross but layouts differ |
| **Serialised** (JSON, binary, protobuf) | highest — encode + copy + decode | high | an object graph must cross, or the sides are decoupled |

**The ordering is the design guidance:** reach for the cheapest shape that satisfies the requirement.

## The cost model

A crossing's cost is roughly:

```text
per_crossing = abi_overhead + conversion + copy + allocation + guard_acquire

total = per_crossing × crossings_per_operation
```

**The second term often dominates.** A 0.2 µs conversion called a million times costs 200 ms; a 5 µs
conversion called ten times costs 50 µs. Teams optimise the first term and ignore the second.

**The design move that fixes the second term:** cross once with everything needed, rather than N times
with a piece each. Bulk transfer, batched calls, or an iterator handle.

## Handles: the default choice for objects

```c
/* ❌ The whole object crosses, and its layout is now a promise */
int process_image(Image img, Image *out);

/* ✅ A handle crosses; the callee owns the object and its layout */
ImageHandle process_image(ImageHandle in);   /* returns a new handle */
```

| Benefit | Detail |
|---|---|
| No serialisation | one word crosses |
| Layout freedom | the object's structure can change |
| Cheap repeated access | many operations on one handle cost one word each |
| Natural ownership | the handle has a destroy function |

**The cost:** the caller cannot inspect the object without a round trip. For introspection-heavy work,
provide a small accessor set rather than exposing the structure.

## Structures: layout or accessors

**By layout** is fastest and most brittle:

```c
/* Both sides must agree exactly: field order, sizes, alignment, packing */
struct Point { float x; float y; };
_Static_assert(sizeof(struct Point) == 8, "layout drift");
```

The static assertion is mandatory, because without it a compiler or platform difference changes the
layout silently.

**By accessors** is stable and slower:

```c
float point_get_x(PointHandle p);
float point_get_y(PointHandle p);
/* Internals can change freely; the caller makes N calls instead of one */
```

**The decision:** if both sides are built together with identical ABIs and the structure is small and
stable, layout is fine. Otherwise use accessors — the cost is predictable, and the stability is real.

## Collections

| Approach | Cost | Use when |
|---|---|---|
| Per-element crossing | crossing count × per-crossing cost | small collections, or genuinely per-element work |
| Bulk transfer (pointer + length) | one crossing + a copy | large collections, fixed layout |
| Iterator handle | one crossing + N cheap moves | large collections, layout must stay private |
| Serialised whole | encode + copy + decode | the collection is an object graph |

**The anti-pattern:** iterating a large collection by crossing once per element. The fix is an iterator
handle or a bulk transfer, and it is usually a large, structural improvement rather than a micro-one.

## Strings

| Concern | Requirement |
|---|---|
| Encoding | state it; UTF-8 is the safe default |
| Length | pass it explicitly; a bare `char*` forces a scan and truncates at an embedded NUL |
| Lifetime | the ownership contract states who frees and when |
| Copy cost | a per-call string conversion on a hot path is a measurable cost |
| Invalidity | a non-decodable sequence must be handled, not assumed away |

**The UTF-8 default is worth restating**, because platform-native encodings (UTF-16 on some runtimes,
a locale-specific code page on others) cause corruption rather than errors when they meet.

## Asynchronous data

Where the shape includes a future or a callback, the marshalling contract has two more clauses:

| Clause | Detail |
|---|---|
| Where does the result arrive? | on which thread, and through which mechanism |
| Who owns the result? | the same ownership rules apply at the resolution, not the call |
| What if the caller goes away first? | cancellation semantics, and lifetime bounds |
| Is the operation cancelable? | if so, what happens to already-allocated memory |

**The lifetime clause is the one that produces use-after-frees:** a callback resolving after the caller
has been destroyed. Bound it explicitly (see `callbacks-and-reentrancy.md`).

## Choosing a shape, condensed

```text
What crosses?
├── Scalars → primitives. Done.
├── An object the callee manipulates → HANDLE. Default choice.
├── A small structure, identical ABI, asserted layout → BY LAYOUT.
├── A structure, layouts differ or unknown → BY ACCESSORS.
├── A collection, large or iterated → BULK TRANSFER or an ITERATOR HANDLE.
├── A collection, small and one-shot → per-element crossing; measure it.
├── An object graph → SERIALISE. Accept the cost; it is usually the slowest.
└── A callback/future → plus the async clauses above.
Then:
  ├── Count the crossings per operation (the number that usually matters)
  └── Measure the per-crossing cost with a harness (R2)
```

## Checklist

- [ ] The shape is chosen from the cost ranking, not by default
- [ ] Handles are used where an object rather than its contents is what crosses
- [ ] Public struct layouts are asserted at build time, or avoided via accessors
- [ ] Collections are bulk-transferred or iterator-handled, not crossed per element
- [ ] String encoding and length are explicit; UTF-8 is the stated default
- [ ] Async results state their arriving thread, ownership and cancellation semantics
- [ ] The crossing count per operation is known, and the per-crossing cost is measured (R2)
- [ ] The measurement names its harness, so the comparison can be repeated (R5)
