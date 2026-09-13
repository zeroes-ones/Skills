# ABI Choice

<!-- STANDARD: 3min -- what ABI to expose, and why a C ABI is the portable default -->

## The choice, stated

When you expose a boundary, you choose an **ABI** — the binary contract about names, calling
conventions, type layouts and error representation. The choice determines who can call it.

| ABI | Portability | Expressiveness | Use when |
|---|---|---|---|
| **C ABI** | very high — every toolchain agrees | low — scalars, pointers, structs with C layout | the default for any boundary others call |
| **C++ ABI** | low — mangling, STL layout and exception ABI differ per compiler | high | all participants use the same toolchain (private) |
| **Language runtime ABI** (e.g. a VM's) | only within that runtime | high | the boundary is internal to one runtime |
| **Sandboxed module ABI** (e.g. WASM) | high, and isolated | medium, via imports/exports | untrusted code, or portability plus isolation |
| **COM-like interface tables** | high | medium | a stable object interface across compilers |

**The rule: a boundary that others call should be a C ABI.** It is the only thing every toolchain on
every platform agrees on, and the portability is worth more than the expressiveness.

## Why the C++ ABI is not portable

| Hazard | Effect |
|---|---|
| **Name mangling** | the same signature mangles differently per compiler; the symbol is not found |
| **Standard-library layout** | `std::string`, `std::vector`, `std::map` layouts differ between implementations and versions |
| **Exception ABI** | unwinding across a module built with a different exception model is undefined |
| **Vtable layout** | base-class layout and RTTI are implementation-defined |
| **Allocator ownership** | memory allocated in one module and freed in another with a different allocator corrupts the heap |

Any one of these breaks at the next compiler upgrade. The full treatment belongs to
`library-linkage-architect` (`plugin-abi.md`); the interop consequence is that a C ABI avoids all five.

## The C ABI toolkit

Everything below is portable across compilers and platforms:

| Construct | Portable? | Note |
|---|---|---|
| Scalars (`int`, `float`, fixed-width types) | yes | prefer fixed-width (`int32_t`, `uint64_t`) over `int`/`long` |
| Pointers to opaque types | yes | the foundation of handle-based designs |
| Structs of scalars and pointers | yes, **if the layout is fixed** | pack and alignment must be agreed and asserted |
| `char*` strings | yes, with an agreed encoding | state UTF-8 and the lifetime |
| Function pointers | yes | the callback mechanism, with its own contract |
| Arrays as pointer + length | yes | never pass an array without its length |
| Unions / tagged unions | yes, if the layout is fixed | useful for result types |
| Bitfields | **no** | layout is implementation-defined; use explicit masks |
| Enums | yes, with a fixed underlying type | state the width |

**Fixed-width integers and explicit layout are the two habits that make a C ABI stable.** `long` is 32
bits on one platform and 64 on another; a struct without a declared packing may align differently.

## Opaque handles, not exposed structures

The single most valuable technique, and it belongs to both this skill and `library-linkage-architect`:

```c
/* ❌ The layout is a permanent promise; the caller allocates it */
typedef struct { int width; int height; int channels; } Image;

/* ✅ Opaque: the layout is private, and can change */
typedef struct Image Image;              /* incomplete type */
Image *image_create(int w, int h, int c);
int    image_width(const Image *img);
void   image_destroy(Image *img);        /* the deallocator travels with the type */
```

Three benefits at once:

1. **The layout is free to change** without breaking callers.
2. **Allocation is unambiguous** — `image_create` allocates, `image_destroy` frees, both on the same side.
3. **The handle is cheap to pass** — no serialisation, no copy.

**The requirement it creates:** handle lifetime. A stale handle must fail loudly, not silently work. A
generation counter or a registry entry that is invalidated on destroy is the standard mitigation.

## Layout agreements, when a struct must be public

Where a caller *must* see the layout (a small message struct, a fixed header), pin it:

```c
/* Declare the layout explicitly and assert it at build time */
struct MessageHeader {
    uint32_t version;
    uint32_t length;
    uint64_t timestamp;
};
_Static_assert(sizeof(struct MessageHeader) == 16, "layout changed");
_Static_assert(offsetof(struct MessageHeader, timestamp) == 8, "layout changed");
```

The static assertions are the point: they turn a silent layout change into a compile error. Without them,
a compiler or platform difference changes the layout and corrupts every call.

## Error representation in the ABI

| Mechanism | Portability | Safety |
|---|---|---|
| Return an `int` code + out-parameters | very high | safe; requires every caller to check |
| Return a result struct `{ ok, value, error }` | high, if the layout is fixed | safe and typed |
| Sentinel value | high | **unsafe** if the sentinel is also a valid value |
| Exception across the boundary | none | undefined behaviour in most runtimes |
| `errno`-style global | high, single-threaded only | fragile; broken under concurrency |

**The C ABI has no exceptions.** That is a limitation and also a safety feature: it forces the error
contract to be explicit (see `error-propagation.md`).

## Versioning the boundary

| Technique | Use |
|---|---|
| A version function called first | refuse an incompatible module before any other call |
| A capability/feature query | the caller asks what is available, rather than inferring from a version number |
| A versioned struct with a `struct_size` field | the callee reads only the fields the caller declares — the classic extensible-struct pattern |
| Reserved fields | room for additions without a size change |

The `struct_size` pattern deserves naming, because it is the portable way to evolve a struct:

```c
typedef struct {
    uint32_t struct_size;   /* the caller sets sizeof(MyStruct) for ITS version */
    uint32_t flags;
    /* ... fields added later; the callee must not read beyond struct_size ... */
} Options;

/* The callee checks struct_size before touching a field added after the caller's version */
```

## What the ABI does not cover

Being explicit about the gaps is part of the contract:

| Not covered by the ABI | Where it belongs |
|---|---|
| Who frees a returned pointer | the ownership contract (R1) |
| Which thread a callback arrives on | the threading contract (R4) |
| What a failure means | the error contract (R3) |
| How long a pointer stays valid | the lifetime contract |
| Whether the callee is thread-safe | the thread-safety statement |

**The ABI says how to call; the contract says how to use.** A boundary with a documented ABI and an
undocumented contract is half-designed.

## Checklist

- [ ] The ABI is stated, and it is a C ABI unless all callers share a toolchain
- [ ] Fixed-width integer types are used, not `int`/`long`
- [ ] Public struct layouts are declared, packed deliberately, and asserted at build time
- [ ] Bitfields are avoided at the boundary
- [ ] Handles are opaque, with a deallocator that travels with the type
- [ ] Handle staleness fails loudly, not silently
- [ ] Errors use an explicit mechanism; no sentinel collisions
- [ ] The boundary is versioned, with a version or capability query
- [ ] The extensible-struct pattern is used where a struct must grow
- [ ] The gaps (ownership, threads, errors, lifetime) are documented as contract, not assumed from the ABI
