# ABI Stability

<!-- DEEP: 5+min -- the breaking-change list, opaque types, reserved space, versioning -->

## What an ABI is

The **application binary interface** is everything two separately-compiled units must agree on to
call each other: symbol names, calling conventions, type layouts, sizes and alignment, the vtable
layout of polymorphic types, exception handling, and the meaning of every exported symbol.

An **API** is a source-level contract. An **ABI** is a binary-level one. They break independently,
and that independence is the source of the worst failures: an API-compatible change that is
ABI-breaking compiles perfectly and corrupts at runtime.

## The breaking-change list

**Adding to a published type or interface is the dangerous direction**, because it is the one that
looks safe.

| Change | ABI verdict | Why |
|---|---|---|
| **Add a field to a struct the caller allocates** | **BREAKING** | the caller allocates the old size; the new field lies outside its allocation, or overlaps the next field |
| **Add a virtual method to a published base class** | **BREAKING** | existing subclasses carry the old vtable layout; the new slot is not where the caller expects |
| **Add a parameter to a function** | **BREAKING** | calling convention and stack/register layout change |
| **Change a field's type to one of a different size** | **BREAKING** | layout shifts for every subsequent field |
| **Change a field's offset by reordering** | **BREAKING** | same effect, and it looks like a tidy-up |
| **Change an enum's underlying type** | **BREAKING** | size and value representation change |
| **Add a new enum member** | **BREAKING** in a switch without a default; **COMPATIBLE** otherwise | depends on how consumers handle unknowns |
| **Change a function's signature's const-ness or noexcept-ness** | **BREAKING** in C++ | it is part of the mangled name and the exception contract |
| **Add an exported symbol** | **COMPATIBLE** | unknown symbols do not affect existing callers — but check for collisions |
| **Add a symbol to a library without exporting it** | **COMPATIBLE** | invisible to consumers |
| **Remove or rename an exported symbol** | **BREAKING** | the loader cannot resolve it |
| **Change a soname/major version** | **BREAKING** by definition | the loader stops resolving the old name |
| **Change behaviour while keeping the signature** | **COMPATIBLE** at ABI, breaking at contract | state which; document it |
| **Change a default value** | **COMPATIBLE** at ABI, breaking at contract | compiled callers already baked in the old default |
| **Change error semantics** | **COMPATIBLE** at ABI, breaking at contract | callers branch on it |
| **Change a dependency's ABI requirement** | **BREAKING** transitively | your ABI now depends on theirs |

**The pattern:** *adding to something the caller allocates or subclasses* and *removing from
anything* are the two dangerous directions. Adding a new free function is safe; adding a field is
not, even though both feel like "adding".

## The two mechanisms that make addition safe

### Opaque types with accessors

Instead of exposing a struct the caller allocates, expose a handle and functions.

```c
/* ❌ Every field addition is a breaking change */
typedef struct { int width; int height; } CanvasV1;

/* ✅ The layout is private; accessors can be added freely */
typedef struct Canvas Canvas;          /* incomplete type */
Canvas *canvas_create(int w, int h);
int     canvas_width(const Canvas *c);
/* Adding canvas_dpi() later breaks nothing */
```

The caller never sizes the type, so the layout can change. This is the single highest-leverage ABI
technique, and it costs one indirection.

**Caveat:** the caller must not need to know the size (for stack allocation or embedding). If it
does, you have traded an allocation for a constraint — state which you chose.

### Reserved space

Where a struct must be public, reserve room up front.

```c
typedef struct {
    int  width;
    int  height;
    void *reserved[4];      /* future fields, or a pointer to an extended block */
} Config;
```

The reserved block absorbs future additions within the same size. Document the reservation so a
future maintainer does not "clean it up".

For vtables and class layouts, the equivalent is **reserved virtual slots** — declare more virtual
functions than you need and keep them in use, or expose an extension interface rather than growing
the base class.

## Versioning strategies

| Strategy | How it works | Fits |
|---|---|---|
| **Soname major bump** | the shared object's name carries a major version; the loader resolves by name | any dynamic library |
| **Symbol versioning** | one library exports multiple versions of a symbol; the loader picks per consumer | a library that must keep old and new behaviour side by side |
| **Versioned entry points** | `open_v2()` alongside `open()` | a C ABI where a new signature is required |
| **Pinned bundle** | one release ships one tested set of everything | applications and runtimes that control the whole process |
| **Extension interface** | a query function returns a pointer to a versioned capability table | plugins and drivers |
| **Language-level versioning** | the package manager and compiler enforce compatibility | source-package ecosystems |

**A soname is a promise to the loader.** Changing it is the mechanism by which the system knows an
incompatible change happened; documenting the change without changing the name means the loader will
happily bind an incompatible library.

## Detecting breaks automatically

ABI compatibility must be *checked*, not reviewed. Two levels:

```bash
# Level 1: the exported symbol inventory — cheap and catches removal/rename
# (toolchain-specific; the shape is the same everywhere)
nm -D --defined-only libfoo.so | awk '{print $3}' | sort > abi-$(date +%F).txt
diff abi-previous.txt abi-current.txt

# Level 2: a structural ABI diff — catches layout and signature changes
# e.g. abi-compliance-checker, abi-dumper, or the platform's equivalent
```

Put level 1 in the pipeline as a required check. Add level 2 where the consumer count is large or
the release cadence is fast.

**What this catches that review misses:** a reordered struct, a widened enum, a removed symbol that
nothing in the codebase still calls but an external consumer does.

## The compatibility policy, written down

An ABI policy answers these, and nothing below is optional if the surface is public:

| Question | Why it must be answered |
|---|---|
| What is the public surface? | an unlisted symbol is either private or a mistake |
| What may change within a major version? | additive-only is the usual answer; say so |
| What forces a major version? | the breaking-change list above |
| How are consumers told? | changelog entry, deprecation warning, and a symbol kept for one cycle |
| How long is a deprecated symbol kept? | one major cycle, or a stated window |
| Who verifies compatibility? | a pipeline check, named |
| What is the fallback when a break is accidental? | re-export the old symbol, or provide both |

## What a plugin ABI must be

If the boundary is an extension point, the ABI has an extra requirement: it must be **stable across
compilers**, because plugins are built by third parties with their own toolchain.

| Approach | Portability | Notes |
|---|---|---|
| **C ABI** | high | the lowest common denominator; opaque handles and function pointers |
| **C++ ABI** | low | STL layout, name mangling and exception ABI are not portable across compilers, or even versions |
| **COM-like interface tables** | high | a vtable of function pointers with a query mechanism |
| **WASM** | high, and sandboxed | a genuinely portable, isolated boundary; adds marshalling cost |

**Never pass a C++ object with a standard-library member across a plugin boundary** unless every
participant uses the same toolchain version. The failure appears at the first compiler upgrade.

## Checklist

- [ ] The public surface is declared and equals the exported surface
- [ ] Published types the caller allocates are opaque, or have reserved space
- [ ] Published classes will not grow a virtual method within a major version
- [ ] No function gains a parameter within a major version; new entry points are versioned
- [ ] The soname (or platform equivalent) changes on an incompatible change
- [ ] A symbol inventory is diffed automatically per release
- [ ] Deprecated symbols are kept for a stated window with a warning
- [ ] The breaking-change list is written into the policy, not implied
- [ ] Plugin boundaries use a compiler-portable ABI
- [ ] Every ABI rule is recorded where a new maintainer will find it (R3)
