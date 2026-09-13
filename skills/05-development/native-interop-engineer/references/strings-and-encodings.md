# Strings and Encodings

<!-- STANDARD: 3min -- encoding, lifetime and copy cost at the boundary -->

## The three things that must be stated

Every string crossing a boundary needs all three, and omitting any one causes corruption rather than an
error.

| Property | Why it must be stated | The default-safe choice |
|---|---|---|
| **Encoding** | platform-native encodings differ; a mismatch corrupts silently | UTF-8 |
| **Length** | a bare `char*` forces a scan and truncates at an embedded NUL | explicit byte length |
| **Lifetime / ownership** | who frees it, and when | the allocating side frees |

## Encoding

| Encoding | Reality | Risk |
|---|---|---|
| **UTF-8** | the portable default; every modern platform handles it | embedded NUL only if the string is treated as bytes |
| UTF-16 | native on some runtimes and platforms | a conversion is required at every crossing; a mis-conversion yields mojibake |
| UTF-32 | rare in interchange | size assumptions |
| Platform code page / ANSI | locale-dependent | two machines can disagree; corruption with no error |
| Latin-1 / ISO-8859-1 | legacy | bytes above 0x7F mean different things |

**State UTF-8 and mean it.** The failure mode of a mismatch is not an exception; it is a string that looks
correct in one locale and corrupted in another, which is a defect that reaches users before it reaches a
developer.

## Length, and the embedded NUL

```c
/* ❌ Forces a scan, and silently truncates at an embedded NUL */
Status set_name(const char *name);

/* ✅ Explicit length: no scan, no truncation surprise */
Status set_name(const char *name, size_t len);
```

The embedded NUL is the subtle case: a string that *can* contain one (user input, a serialised payload, a
UTF-16 buffer reinterpreted as bytes) is not a C string, and treating it as one truncates it silently.

**The rule:** if the data is text and could plausibly contain a NUL byte, pass a length. The cost of the
extra parameter is negligible; the cost of silent truncation is a data-integrity defect.

## Encoding-conversion cost

Where the two sides use different encodings, a conversion is required — and it is a per-crossing cost.

| Situation | Cost |
|---|---|
| Both UTF-8, passed by reference | no conversion, no copy |
| Both UTF-8, copied across | one copy |
| UTF-8 ↔ UTF-16 conversion | a conversion plus an allocation, per crossing |
| Re-encoding per call on a hot path | measurable, and often avoidable by converting once |

**The hot-path fix:** convert once at the boundary of the bulk operation rather than per item. A
conversion performed inside a loop over a collection is the common shape of this defect.

## Lifetime patterns

| Pattern | Contract | Safety |
|---|---|---|
| Caller-owned, valid for the call | the callee must not retain it | high |
| Caller-owned with an explicit length | as above, plus the length | high |
| Callee-owned, valid until a named event | state the event | medium |
| Callee-owned, caller-frees | the callee must provide the deallocator | medium |
| Static / interned | never freed | high, if genuinely immutable |
| Borrowed from a buffer the caller knows about | the caller must keep the buffer alive | medium — requires discipline |

**The dangerous default is "valid until something happens"** (see `memory-ownership.md`). Prefer an
explicit lifetime, because it is checkable.

## Returned strings

The pattern that removes the ambiguity, and the one to prefer:

```c
/* ✅ The callee provides the deallocator; the caller cannot get it wrong */
char *get_label(int id);              /* returns a string the caller owns */
void  free_string(char *s);           /* the ONLY correct way to free it */

/* ❌ The caller must guess how to free it — and will guess wrong */
char *get_label(int id);              /* free with what? free()? a runtime free? nothing? */
```

Providing `free_string` makes the ownership unambiguous at the type level, which is the strongest
available signal.

## Text is not always text

Some boundary payloads look like strings but are bytes:

| Payload | Treat as |
|---|---|
| A serialised protobuf/JSON blob | bytes, with a length |
| A base64-encoded value | bytes/ASCII with a length |
| An encrypted buffer | bytes |
| A path | text, but encoding-sensitive; state the convention |
| A filename from another filesystem | bytes on some platforms — do not assume UTF-8 |
| A user's display name | text; may contain any valid sequence, and may be invalid |

**The general rule:** if you are not going to interpret it as text, do not pass it as a string. A byte
buffer with a length is honest and avoids an accidental conversion.

## Invalid sequences

A text API can receive an invalid sequence (truncated UTF-8, a lone surrogate). The contract must say
what happens:

| Option | Note |
|---|---|
| Reject with an error | safest for data integrity |
| Replace with a replacement character | tolerant; lossy, and must be stated |
| Pass through unchanged | only if the other side also treats it as bytes |
| Panic/throw | never across the boundary |

**State the choice.** An unstated policy means the runtime's default applies, and the runtime's default
may differ between the two sides.

## Testing strings

```text
1. ASCII only — the trivial case, must pass
2. Non-ASCII (accents, CJK, emoji) — must round-trip exactly
3. An embedded NUL, where the data is bytes — must not truncate
4. The longest permitted string — must not overflow or truncate silently
5. The empty string — must not be treated as an error or a null
6. An invalid sequence — must follow the stated policy
7. A string produced on side B and consumed on side A, and the reverse — both directions
```

Step 3 and step 6 are the two that find real defects. Step 7 catches an asymmetry where a conversion is
applied on one direction only.

## Checklist

- [ ] The encoding is stated, and UTF-8 is the default
- [ ] Length is passed explicitly wherever the data could contain a NUL or is not plain C text
- [ ] The ownership and lifetime of every string is in the ownership contract (R1)
- [ ] Strings returned to the caller come with the deallocator that must be used
- [ ] Byte payloads are passed as buffers with lengths, not as strings
- [ ] The policy for invalid sequences is stated
- [ ] Encoding conversion is done once per bulk operation, not per item on a hot path
- [ ] The string tests above are implemented, including the round-trip in both directions
