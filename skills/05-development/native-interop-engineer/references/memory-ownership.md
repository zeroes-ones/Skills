# Memory Ownership

<!-- DEEP: 5+min -- allocator, owner, freer, lifetime, arenas and handle safety -->

## The rule

**Every pointer crossing the boundary has a named allocator, owner, freer and lifetime.** This is R1, and
it is the highest-value rule in the skill because most FFI defects are an allocation mismatch.

The failure it prevents is specific and nasty: memory allocated on one side and freed on the other with
a **different allocator** corrupts the heap — and it works in testing, because the two allocators happen
to agree in that build.

## The ownership matrix

For every pointer, one row must be filled in. An unfilled row is the defect.

| Pointer | Allocated by | Freed by | Lifetime ends | Notes |
|---|---|---|---|---|
| Buffer passed in | caller | caller | when the call returns | the callee must not retain it |
| Result buffer returned | callee | caller, using the callee's free function | caller decides | the deallocator must travel with the type |
| Opaque handle | callee | callee (`*_destroy`) | the handle's lifetime | a stale handle must fail loudly |
| String returned | callee | caller, per the documented rule | caller decides | encoding and ownership stated together |
| Callback reference | caller | caller, before teardown | callback lifetime | must not outlive its registration |

**"Freed by the allocating side" is the safe default.** When that is impossible, the allocating side must
provide the deallocator. There is no third option that is safe.

## Why allocator mismatch is so dangerous

```text
Side A allocates with allocator A        →  pointer P
P crosses the boundary
Side B frees with allocator B            →  undefined behaviour

In a debug build:    both may use the same underlying allocator → works
In a release build:  different allocators, different arenas     → corruption
With a different CRT:  different heaps entirely                 → immediate crash
```

The three reasons it hides:

1. **A shared runtime** makes the allocators coincide.
2. **A debug allocator** may paper over the mismatch.
3. **The corruption is delayed** — the free succeeds, and a later allocation fails.

**The consequence for testing:** an ownership mismatch cannot be validated by "it ran and did not crash".
It requires either a documented contract or a tool (a sanitizer, a heap checker).

## Lifetime, not just ownership

Ownership says *who frees*; lifetime says *how long it stays valid*. Both are needed.

| Lifetime pattern | Contract |
|---|---|
| Caller-owned, valid for the call | the callee must not retain it — the common and safest case |
| Caller-owned, explicit length | the length must be passed; a bare pointer is unusable |
| Callee-owned, valid until a documented event | state the event (the next call, an explicit release, the handle's destroy) |
| Shared, reference-counted | state who increments and decrements, and whether it is atomic |
| Arena-scoped | released in bulk when the arena is destroyed |

**The dangerous case is "valid until something happens"**, because the caller must know when. Prefer
explicit lifetimes ("valid until this handle is destroyed") over implicit ones ("valid until the next
call") — the first is checkable, the second is a convention.

## Arenas at the boundary

An arena is the pattern that makes ownership trivially symmetric:

```c
/*
  The caller creates an arena, passes it in, and destroys it.
  Everything the callee allocates comes from the arena.
  There is exactly ONE free, and it is on the caller's side.
*/
Arena *arena = arena_create();
Result r = do_work(arena, input);       /* callee allocates only from the arena */
use_result(&r);
arena_destroy(arena);                   /* one call releases everything */
```

Why it is the best pattern when it fits:

| Benefit | Detail |
|---|---|
| One ownership decision | the arena's owner frees everything |
| No per-pointer negotiation | the callee cannot accidentally leak |
| Bulk cleanup on the error path | unwind by destroying the arena |
| No allocator mismatch possible | all allocations come from the same allocator |

**When it does not fit:** long-lived objects, or objects that must outlive the arena. Those need explicit
handles with explicit destroy functions.

## Handles

The handle is the boundary's object reference, and it needs more care than a plain pointer.

| Requirement | Why |
|---|---|
| Opaque to the caller | layout freedom; prevents accidental structure access |
| A destroy function travels with it | the allocating side owns the deallocation |
| Staleness fails loudly | a reused or freed handle must error, not silently work |
| Generation counter or registry | the mechanism that detects staleness |
| Thread-safety stated | may it be used from another thread? Concurrently? |

**The staleness problem:** if handles are addresses, a freed handle may later be reallocated to a
different object, so a stale use silently touches the wrong thing — the worst possible failure mode.
A generation counter (handle = index + generation) makes a stale handle detectable.

## Reference counting at the boundary

Where a shared object must be reference-counted:

| Decision | Options |
|---|---|
| Atomic or not | atomic if it may cross threads; state which |
| Who increments | state per path |
| Who decrements | state per path |
| What happens at zero | destroy, or return to a pool — state which |
| Cycle handling | none, or a weak reference — state which |

**The defect that always appears:** an unbalanced increment or decrement on an error path. The count
leaks (or frees early) only when an error occurs, so it survives happy-path testing.

## Preventing the mismatch, mechanically

| Technique | Effect |
|---|---|
| One allocator for the whole boundary | the single most effective prevention |
| Route allocation through the caller's allocator (a callback) | the callee never owns an allocator |
| The arena pattern | one owner, one free |
| The deallocator travels with the type | impossible to free with the wrong function |
| A static assertion on struct layout | catches layout drift before runtime |
| Sanitizers in CI | catches the mismatch the moment it happens |
| Ownership attributes/annotations where the language supports them | `#[must_use]`, `[[nodiscard]]`, ownership annotations, `_Owned`/`_Borrowed` markers |

**The caller-provided allocator is under-used and very effective.** If the callee allocates through a
function pointer the caller supplied, the allocators cannot differ by construction.

## Reviewing an ownership contract

```text
For every pointer at the boundary:
  1. Who allocates it? (which side, which allocator)
  2. Who frees it? (which side, which function)
  3. When does its lifetime end? (an explicit event)
  4. Does any path differ? (an error path that frees, or does not)
  5. Is the deallocator available to the freeing side? (a function, not a convention)
  6. Can a stale reference be used? (handle staleness, use-after-free)
```

Question 4 is where contracts break: the happy path is documented and the error path leaks. That is why
the arena pattern is valuable — the error path unwinds by destroying the arena, the same as the success
path.

## Checklist

- [ ] Every crossing pointer has a filled ownership-matrix row (R1)
- [ ] Memory is freed on the allocating side, or by a deallocator that side provides
- [ ] Every pointer's lifetime is explicit, ending at a named event
- [ ] The error path's ownership is identical to the happy path's, or explicitly documented
- [ ] An arena is used where the lifetime permits it
- [ ] Handles are opaque, have a destroy function, and fail loudly when stale
- [ ] Reference counts are balanced on every path, including errors
- [ ] Allocation routes through one allocator, ideally one supplied by the caller
- [ ] Sanitizers run in CI on the boundary's tests
- [ ] The ownership contract is reviewed by the pointer checklist above, not by reading call sites
