# Error Propagation

<!-- DEEP: 5+min -- result codes, result types, and why exceptions must not cross -->

## The two prohibitions

**1. Never let a panic or exception unwind across a foreign frame.** In most runtimes this is undefined
behaviour: the foreign frame does not have the machinery to unwind correctly, so the result ranges from a
clean abort to corrupted state. A process that aborts with no message immediately after a foreign call is
usually this defect.

**2. Never encode failure in a value that is also a legitimate success.** A sentinel collides eventually,
under exactly the input nobody tested, and the failure becomes silent success — the worst outcome
available.

Both are R3.

## The mechanisms, ranked by safety

| Mechanism | Safety | Cost | Note |
|---|---|---|---|
| **Out-parameter result code** + out message | safest | one extra argument | works across every ABI; requires every caller to check |
| **Result struct** (tagged union) | safe and typed | one struct return | requires a fixed layout |
| **Exception caught at the boundary and converted** | safe | a little overhead | catching is fine; *unwinding across* is not |
| **Sentinel value** | unsafe if it can be valid | none | acceptable only when provably impossible |
| **`errno`-style global** | fragile | none | single-threaded only; broken under concurrency |
| **Log only** | unacceptable | none | undiagnosable from the caller's side |

## The result-code pattern, done well

```c
typedef enum {
    OK = 0,
    ERR_INVALID_ARGUMENT,
    ERR_NOT_FOUND,
    ERR_IO,
    ERR_INTERNAL
} Status;

/* The code is the contract; the message is for humans */
Status do_work(const Input *in, Output *out, char *err_buf, size_t err_len);

/* Caller: */
char err[256];
Output out;
Status s = do_work(&in, &out, err, sizeof err);
if (s != OK) {
    /* convert to the caller's language's error type, with the message */
}
```

Three requirements that make it work:

1. **Every call is checked.** An unchecked code repeats the same failure silently. Provide a helper that
   converts a code into a language-native error, so the idiom is one line.
2. **The message buffer has a stated size and truncation rule.** A pointer without a length is unusable
   (see `strings-and-encodings.md`).
3. **The codes are stable.** They cross the boundary, so they are part of the ABI; changing a meaning is
   a breaking change.

## The result-struct pattern

```c
typedef struct {
    Status status;
    union {
        Output ok;      /* valid when status == OK */
        struct { uint32_t code; uint32_t detail; } err;  /* valid otherwise */
    } value;
} Result;

Result do_work(const Input *in);
```

Advantages: the error and the value cannot be confused, and there is no out-parameter to forget.
Requirement: the union's layout must be fixed and asserted, and the caller must check `status` before
reading `value`.

**The C++/Rust version** of the same idea is the idiomatic result type, converted at the boundary to a
C-compatible representation.

## Catching an exception at the boundary

Catching is correct; unwinding across is not.

```rust
// The extern "C" ABI forbids unwinding across it.
// (The real code also carries the no_mangle attribute, shown in prose above.)
pub extern "C" fn do_work(in_ptr: *const Input, out: *mut Output) -> i32 {
    // The boundary is the ONLY place a panic may be caught
    let result = std::panic::catch_unwind(|| {
        // work that might panic
    });
    match result {
        Ok(Ok(v))  => { /* write v to out */  0 }
        Ok(Err(e)) => { /* map e to a code */ e.code() }
        Err(_)     => ERR_INTERNAL,   // a panic was caught and converted
    }
}
```

The important properties:

| Property | Why |
|---|---|
| `catch_unwind` at the boundary | the panic never reaches the foreign frame |
| A converted error code | the foreign side gets a typed failure, not an abort |
| A stable panic→code mapping | `ERR_INTERNAL`, with detail logged, not exposed |
| The `extern "C"` signature | unwinding is not permitted to cross it |

**The equivalent in other languages:** a try/catch around the boundary body, converting to a return code;
or the runtime's own mechanism (N-API exposes exception propagation helpers; JNI exposes exception-check
APIs — use them rather than letting an exception escape the native method).

## The sentinel trap, concretely

```c
/* ❌ -1 is a valid count for "unknown"; the caller cannot distinguish */
int count_items(void);       /* returns -1 ... for an error, or for unknown? */

/* ❌ NULL is a valid value here */
char *get_label(int id);     /* does NULL mean "no label" or "failed"? */

/* ✅ An explicit status separates the two */
Status count_items(int *out_count);
```

The rule: **the sentinel must be impossible as a legitimate value**, and that must be provable from the
type or the documented domain, not from convention. If you cannot prove it, use a result.

## Error codes across the boundary

| Requirement | Detail |
|---|---|
| Stable numeric values | they are in the ABI; reordering them breaks callers |
| Documented meaning | a code with no meaning is a support ticket |
| A mapping to each caller's error type | so the caller's idiom is not violated |
| A generic fallback | an unknown code must still be handleable |
| Severity or category | useful for the caller's retry/abort decision |

**The mapping matters more than it appears.** A Rust caller wants a `Result`, a Java caller wants an
exception, a Python caller wants an exception. The boundary provides codes; a thin layer per language
converts them into the idiom that language expects. Without that layer, every call site writes the
conversion, differently.

## Failures that cannot be represented

Some failures cannot cross as an error code:

| Failure | Reality | What to do |
|---|---|---|
| A panic/abort in a third-party native library | the process may die | isolate the boundary in a subprocess where it matters |
| A fatal signal (segmentation fault) | process-fatal | isolate, and treat as a crash rather than an error |
| An out-of-memory condition on one side | may be unrecoverable there | attempt to report, and accept the process may not survive |
| A stack overflow | process-fatal | bound recursion at the boundary |
| A hung call | the caller waits forever | put a timeout on the boundary where the mechanism allows, or isolate |

**The honest design response:** where a failure cannot be represented, the boundary must be *isolated*
(a subprocess, a worker) rather than protected by error codes. Claiming to handle a process-fatal failure
with a return code is a design fiction.

## Testing error paths

```text
For every crossing point, exercise:
  1. Success — the value is what the caller expects
  2. Each documented error code — the caller receives the right code
  3. An unknown code — the caller does not crash or mis-handle it
  4. A panic/thrown exception on the other side — caught, converted, no abort
  5. A resource failure (allocation failure) — reported, not crashed
  6. The message buffer at its boundary (exactly full, and truncated)
  7. A call after a previous failure — state is not corrupted by the earlier failure
```

Step 4 and step 7 are the two that find real defects. Step 4 catches the cross-frame unwind; step 7
catches a converter that leaves state inconsistent after a failure.

## Checklist

- [ ] No panic or exception unwinds across a foreign frame (R3)
- [ ] Failures are distinguishable from success on every path (R3)
- [ ] No sentinel is used where it could be a valid value
- [ ] Every call's result is checked, with a one-line conversion helper per language
- [ ] Error codes are stable and documented, with a mapping to each caller's error type
- [ ] The error message buffer has a stated size and truncation rule
- [ ] Un-representable failures are handled by isolation, not by a return code
- [ ] The error paths are tested, including unknown codes and post-failure state
- [ ] The panic-to-code mapping is stable and logs the detail rather than exposing it
