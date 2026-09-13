# Threading and Affinity

<!-- STANDARD: 3min -- attaching threads, affinity, and the runtime's guard -->

## Three distinct properties, often conflated

| Property | Question | Getting it wrong produces |
|---|---|---|
| **Thread safety** | may this object be touched from multiple threads at once? | data races, corruption |
| **Thread affinity** | must this object be touched from one specific thread? | corruption or crashes that look random |
| **Thread attachment** | has this thread been introduced to the runtime? | undefined behaviour, intermittent crashes |

They are independent. An object may be thread-safe but have affinity (safe from many threads, but only
one at a time), or be attached but not thread-safe (known to the runtime, still racy).

**The contract must state all three** for every object that crosses or is held across the boundary.

## Thread attachment

A thread the runtime does not know about cannot safely call into it.

| Runtime | Attachment | Detachment |
|---|---|---|
| JVM | `AttachCurrentThread` (or as-daemon) | `DetachCurrentThread` before the thread exits |
| CPython | `PyGILState_Ensure` for the thread's duration | `PyGILState_Release` |
| Node | do not attach — use the threadsafe-function mechanism instead | n/a |
| .NET | runtime-specific interop attachment | runtime-specific |

**Two rules for attachment:**

1. **Attach before the first call into the runtime**, not lazily on first use of some API.
2. **Detach before the thread exits.** An attached thread that exits without detaching leaves the runtime
   holding resources for a thread that no longer exists.

**The defect signature:** an intermittent crash under load, where load is what causes the native side to
use additional threads. Single-threaded tests always pass.

## Affinity, in the common runtimes

| Runtime | Affinity rules |
|---|---|
| Node | JS runs on the main thread; values may not be touched off it without the threadsafe mechanism |
| JVM | no general affinity, but some UI frameworks require the UI thread, and some APIs require the main thread |
| .NET | similar: some frameworks require the UI/STA thread |
| iOS/Android UI | UI objects have strict main-thread affinity |
| Embedded interpreters | usually single-threaded: all calls must come from one thread, or be locked |
| Most native libraries | state their own rules; assume none |

**The general pattern:** runtimes that expose a language to callbacks usually have *one* thread where the
language is valid, and everything else must marshal to it. That is the rule to state and to enforce.

## The guard, restated as a threading rule

The guard (a GIL, an event loop, a lock) is the mechanism the runtime uses to protect its state.

| Property of the guard | Consequence |
|---|---|
| Held while touching runtime state | required |
| Released during long native work | required, or the runtime serialises on you |
| Must not be re-acquired while held | a deadlock (see `callbacks-and-reentrancy.md`) |
| Its acquisition may block | so holding it during I/O blocks the whole runtime |

**The two mistakes, both directions:**

```text
❌ Hold the guard for the whole native call     → every other thread waits; the runtime serialises
❌ Release the guard and keep using runtime state → corruption
✅ Acquire, take what you need, release, work, re-acquire, publish the result
```

## Choosing where the work happens

```text
Is the work CPU-heavy and independent of runtime state?
├── Yes → release the guard, do the work, re-acquire → publish
└── No (it touches runtime state throughout) ↓
    Can it be restructured to touch state only at the ends?
    ├── Yes → restructure, then release the guard for the middle
    └── No  → accept that the runtime is serialised for this call; measure the impact

Is the work I/O-bound?
├── Yes → never hold the guard; the whole runtime would wait on the I/O
└── No  → the above applies
```

## Concurrency contracts to state

For every object held across the boundary:

| Contract | Options |
|---|---|
| Thread safety | "safe for concurrent use" / "safe, one thread at a time" / "not safe" |
| Affinity | "any thread" / "the creating thread" / "the runtime's main thread" |
| Lifetime across threads | "must outlive all uses" / "reference-counted; see the ownership contract" |
| Locking | "internally locked" / "the caller must lock" / "lock-free for reads, locked for writes" |
| Destruction | "may be destroyed from any thread" / "only from the creating thread" |

**"Not stated" is not an option.** If the contract is silent, each caller invents one, and they will
disagree.

## Testing threading

```text
1. Concurrent use from N threads.
     → data races surface under a race detector
2. Use from a thread the runtime does not know about.
     → must be attached by design; asserts the attachment path
3. Long native call, other threads still responsive.
     → asserts the guard is released around the work
4. Callback arriving on a native thread.
     → asserts attachment and marshalling
5. Teardown while a thread is mid-call.
     → asserts the lifetime contract
6. Race detector and thread sanitizer in CI.
     → the only reliable way to find races before production
```

**Steps 3 and 4 are the two that find the real defects**, and step 6 is the only way to be confident
about steps 1 and 5.

## The performance interaction

Threading decisions are performance decisions:

| Decision | Performance effect |
|---|---|
| Holding the guard during the work | serialises the entire runtime |
| Releasing it | enables parallelism; requires care |
| Per-call attachment | expensive; attach once per thread |
| Marshalling every callback to one thread | serialises callbacks; measure it |
| A thread per crossing | pathological; use a pool |

**Measure the boundary's threading cost**, because it is often larger than the marshalling cost that gets
the attention.

## Checklist

- [ ] Thread safety, affinity and attachment are stated separately for every crossing object
- [ ] Every runtime-touching thread is attached before its first call, and detached before exit
- [ ] The guard is acquired to touch runtime state, and released around long or I/O-bound work
- [ ] The guard is never re-acquired while held (no callback re-entrancy)
- [ ] Callbacks state their arrival thread and any marshalling they require
- [ ] The destruction thread rules are stated
- [ ] Concurrency is tested under a race detector or thread sanitizer in CI
- [ ] Teardown-during-call is tested
- [ ] The threading cost is measured where callbacks are marshalled
