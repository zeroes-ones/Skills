# Extension Points

<!-- STANDARD: 3min -- abstractions versus internals, and how to choose what to expose -->

## The rule, and why it is the first one

**Expose abstractions, not internals.** Every extension point is a promise, and an abstraction can be
re-implemented while a concrete interface cannot.

```text
INTERNAL (becomes a permanent promise)      ABSTRACTION (survives internal change)

struct DbRow { cols: Vec<String> }          trait DocumentStore {
  fn get_row(id) -> DbRow                       fn load(id) -> Document
                                                 fn save(Document)
                                             }
```

The left one binds a database result shape for as long as the extension ships. The right one describes
what the extension wants to do, and can be re-implemented on a different storage engine without the
extension noticing.

## The test for a proposed extension point

```text
For every proposed point, ask in order:

1. Does it expose a data structure, a type, or a protocol the host uses internally?
   ├── Yes → REJECT, or ABSTRACT it first. Internals are promises you cannot keep cheaply.
   └── No → continue

2. Does it express WHAT the extension wants, or HOW the host currently does it?
   ├── How → ABSTRACT. The "how" changes; the "what" is stable.
   └── What → continue

3. Can the host change its implementation without the extension noticing?
   ├── No  → ABSTRACT further, or do not expose it
   └── Yes → continue

4. Is the surface small?
   ├── No  → narrow it. A large surface is a large promise.
   └── Yes → continue

5. Can it be versioned independently?
   ├── No  → it will force a whole-platform version bump; consider splitting
   └── Yes → assign a stability tier
```

Points that fail steps 1–3 are the ones that make a platform permanently expensive to change.

## What to expose, by extension class

| Extension class | Expose | Do not expose |
|---|---|---|
| Theme/appearance | A token schema; a named set of appearance properties | The host's rendering internals |
| Content/data provider | A fetch/query abstraction; a result model the extension defines | The host's storage schema |
| Build/transform step | An input/output abstraction; a declared capability set | The host's compiler or AST internals |
| Integration/connector | An event model; a declared set of endpoints | The host's internal event bus implementation |
| Automation/scripting | A capability-gated API surface; a stable set of operations | The host's object graph |
| AI/LLM extension | A prompt/tool contract; the model interface | The host's model client internals |

**The pattern:** expose the *intent* level (query, transform, fetch, notify) and keep the *mechanism*
level (schema, AST, bus, object graph) private.

## The stability tiers

Every point gets one. The tier is what makes the contract honest.

| Tier | Promise | Use for |
|---|---|---|
| **STABLE** | will not break without a major version, deprecation window, migration note | points extensions depend on |
| **EXPERIMENTAL** | may change, with notice; extensions opt in | new points, under evaluation |
| **INTERNAL** | no promise; may change any time | points that exist for the host's own use |

Three rules that make the tiers work:

1. **Extensions declare the tier they target**, so the host knows what was assumed.
2. **Promotion is a one-way door.** An EXPERIMENTAL point that extensions depend on becomes STABLE by
   the fact of that dependency; promoting it is a commitment, so promote deliberately.
3. **Demotion is a break.** Moving STABLE to EXPERIMENTAL is a stability event, not a filing change.

## Surface narrowing techniques

| Technique | Effect |
|---|---|
| Capability-gated operations | the extension can only do what it requested, per operation |
| Handle-based access (opaque IDs) | internals stay private; the extension holds references |
| Event subscription rather than polling internals | the host decides what is observable |
| Declarative descriptors rather than code | the extension describes intent; the host implements |
| A small verb set with parameters | fewer symbols, easier versioning |
| Async callbacks rather than synchronous access | the host controls timing and lifetime |

**The handle technique is the highest-leverage** and the easiest to apply: expose `ProjectId` and
operations, not `Project`. The extension never sees the structure, so the structure is free to change.

## The cost of a wide surface

| Surface size | Consequence |
|---|---|
| Small, intent-level | internal change is cheap; the platform can evolve |
| Large, mechanism-level | every internal change is a public break; the platform freezes |

The freeze is gradual and rarely noticed: each exposed internal type removes one more degree of freedom,
until the core cannot be refactored without breaking the ecosystem. That is the failure R1 prevents.

## Extension point review

Before adding a point:

- [ ] It is intent-level, not mechanism-level
- [ ] It exposes no host-internal type, structure or protocol
- [ ] The host could change its implementation without the extension noticing
- [ ] It has a stability tier
- [ ] It can be versioned independently of the rest of the surface
- [ ] Its capability implications are stated (what it lets an extension do)
- [ ] It is documented at the level the extension author needs, not the host's internals
- [ ] A removal path exists if it is ever retired (deprecation window defined)
