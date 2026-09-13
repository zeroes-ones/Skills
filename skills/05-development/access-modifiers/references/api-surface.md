# API Surface

<!-- DEEP: 5+min -- designing the surface as a contract, with the explicit-list practice -->

## The inversion

The defect this file exists to prevent:

```text
Defect:      the public surface is "everything that is not private"
             → the surface grows with every commit
             → it grows by accident, and each addition is a promise
             → nobody can say what the library promises, because nobody chose

Practice:    the default is the most restrictive modifier that compiles
             → the surface is the short LIST of declarations deliberately published
             → each entry is a decision with an owner
```

This is R2, and it is the single highest-leverage change in this skill: inverting the default means the surface shrinks rather than grows, and every addition is visible in review.

## The surface list

An explicit file, diffed in review:

```text
# public-api.txt — the promises this library makes
Client
  Client.connect(url, options) -> Client
  Client.close()
  Client.on(event, handler)

Config
  Config.timeout         (read-only)
  Config.retries         (read-only)

Errors
  ConnectionError
  TimeoutError
```

Three properties make it useful:

| Property | Why |
|---|---|
| It is **short** | if it is not short, the default was not inverted |
| It is **diffable** | an accidental addition appears in the diff |
| It is **reviewable as a whole** | you can see the promise set at a glance |

**Generate it, don't hand-write it** where the toolchain can: a symbol dump, an API-extractor report, a `pub use` audit. A generated list cannot drift from reality; a hand-written one will.

## What each entry promises

Every published declaration makes four promises, and it is worth being conscious of all four:

| Promise | The question it answers |
|---|---|
| **Existence** | this will keep existing |
| **Signature** | the shape will not change incompatibly |
| **Behaviour** | the documented effect will hold |
| **Semantics** | the contract (errors, guarantees, ordering) will hold |

The fourth is the one most often broken without a signature change — a method that stops being thread-safe, an error that changes type, a guarantee that becomes best-effort. All four need the same care because consumers depend on all four.

## The layers above the source surface

A library has **several** surfaces, and they must be consistent:

| Layer | Mechanism | Owner |
|---|---|---|
| **Source** | access modifiers | this skill |
| **Binary** | symbol export, ABI | `library-linkage-architect` |
| **Wire** | REST/GraphQL contract, versioning | `api-designer` |
| **Documentation** | what is described as public | `documentation-engineer` |
| **Runtime authorization** | who may call it at runtime | `iam-architect` |

**The consistency rule:** a declaration public in source but absent from the docs is a documentation gap; public in source but not exported at the binary level is a build defect; public in source and unreachable at runtime is an authorization question — three different problems that all present as "it doesn't work for the consumer".

Conversely: **internal in source but exported in the binary** is the dangerous direction, because the binary surface is what determines ABI compatibility. `library-linkage-architect` covers that side; this skill must at least flag the mismatch.

## Designing the surface, deliberately

```text
1. List the USE CASES the library must enable.
   Not the entities, not the types — the tasks a consumer performs.

2. Derive the minimum declarations each use case needs.
   → this is the candidate surface. Expect it to be smaller than you assumed.

3. For every candidate, ask: could this be inferred, defaulted, or composed
   from something already published?
   ├── Yes → remove it; a smaller surface is a smaller promise
   └── No  → keep it

4. For everything NOT in the candidate set → the restrictive modifier.
   (this is the inversion: the default is internal/private, not public)

5. Name each kept declaration's consumer — the use case from step 1.
   ├── Cannot name one → remove it (R1)
   └── Named → it is justified

6. Decide the extension story SEPARATELY (R6):
   ├── No extension → keep it closed (final / sealed / no open / no public trait)
   └── Extension intended → publish the contract, document it, test a subclass
```

## Surface design heuristics

| Heuristic | Why |
|---|---|
| **Fewer, coarser types** | each exported type is a promise; a hundred small types is a hundred promises |
| **Interfaces over concrete types** | an interface can be implemented differently; a concrete class constrains you |
| **Explicit over inferred** | an inferred return type publishes whatever the implementation happens to produce |
| **Values over references to mutable state** | returning a reference to internal state leaks the representation |
| **Errors as a documented set** | an unlisted error type is still part of the surface |
| **No public constructors where an invariant exists** | an unexported constructor plus a factory keeps the invariant |
| **Parameters as a named options type** | adding an option later is then not a breaking change |

That last one deserves emphasis, because it is the most common avoidable breaking change:

```text
def connect(url, timeout, retries, retry_delay)      → adding a 5th argument is breaking
def connect(url, options)                            → adding an options field is compatible
```

## Widening and narrowing

| Change | Source surface | Breaking? |
|---|---|---|
| private → internal | widening | no |
| internal → public | widening | no (a new promise) |
| public → internal | **narrowing** | **yes** |
| public → private | **narrowing** | **yes** |
| public → open | widening the extension promise | no, but it is a stronger contract to keep |
| open → public | narrowing the extension promise | **yes**, for existing subclasses |

**The asymmetry is the whole argument for starting narrow.** Narrowing is a coordinated migration with a deprecation window, a consumer notification, and a version bump. Widening is a one-line change.

## Retiring a public declaration

Never remove directly. The sequence, and it is the same in every language:

```text
1. ANNOUNCE     mark it deprecated; name the replacement and the removal version
2. WARN         it still works, and it emits a warning the consumer will see
3. PUBLISH      a migration note, and a codemod where possible
4. WINDOW       it keeps working for the full announced period
5. REMOVE       only at the announced version, after the window
```

The three failures in that sequence, all common: removing without a window; announcing without a warning mechanism (so nobody sees it); and never removing at all (so the deprecation was theatre). The window length is a judgement — long enough for a small consumer to act, and stated rather than implied.

## The API-surface checklist

- [ ] The public surface is an explicit list, generated where the toolchain allows (R2)
- [ ] The list is diffed in review, so growth is visible
- [ ] Every entry names the use case it serves (R1)
- [ ] Nothing is public only because another public declaration references it
- [ ] The source surface and the binary surface are consistent (with `library-linkage-architect`)
- [ ] The source surface and the documentation agree
- [ ] Extension points are separate decisions with documented contracts (R6)
- [ ] Options are passed as a named type, so additions are not breaking
- [ ] Every retirement follows the announce → warn → window → remove sequence
- [ ] The promise level (exists / signature / behaviour / semantics) is recorded for each entry
