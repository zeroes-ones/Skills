# Joint-Rule Contradiction — when every rule is right and the set is wrong

> The most generalisable idea in the source corpus: rules can each be locally correct and jointly
> unsatisfiable. The defect is not in any rule; it is in their intersection, which nobody checked
> because rules are reviewed one at a time.

---

## The canonical case

A module scope had **no legal spelling**. Two rules constrained it:

| Rule | Requirement | Legal spellings |
|------|-------------|-----------------|
| R-A | Scope modifiers must be **explicit** — no implicit default | `ios/DeeplyDomain` + explicit `internal` |
| R-B | Scope declarations must not be **redundant** — no restating the default | `ios/DeeplyDomain` alone |

Read alone, each is defensible. R-A exists because implicit defaults hide intent across a large
multi-language tree. R-B exists because restating a default is noise that desynchronises when the
default changes. Applied together, the declaration `ios/DeeplyDomain` in the `internal` tree
requires both a modifier and no modifier.

**Nothing in either rule is a bug.** The bug is the empty cell where they cross. It surfaces as a
build error, in a file whose author has done nothing wrong, with a message that names neither rule.

The encoded fix is an invariant, not a patch:

> **Every scope must have a legal spelling in every tree.**

That sentence is testable. It is the artefact this technique produces, and it prevents the hole
reopening when either rule is later refined.

---

## The matrix method

The general procedure. It takes twenty minutes and it is mechanical.

### Step 1 — Enumerate the constrained dimensions

Identify every dimension *any* rule cares about for the declaration in question. Do not start from
the new rule, or you will reproduce the new rule's view of the world.

```
Worked example: a build-graph scope declaration

  Dimension 1: TREE         {ios, android, shared}
  Dimension 2: VISIBILITY   {internal, public, private}
  Dimension 3: LOCATION     {root, subdirectory}
```

### Step 2 — Build the product

```
              internal              public              private
ios
  root        ?                     ?                   ?
  subdir      ?                     ?                   ?
android
  root        ?                     ?                   ?
  subdir      ?                     ?                   ?
shared
  root        ?                     ?                   ?
  subdir      ?                     ?                   ?
```

### Step 3 — Fill each cell with a legal spelling, or mark it impossible

A cell is legal if a spelling exists that satisfies **all** rules simultaneously. Cite the spelling,
not a rule name.

```
              internal                    public                     private
ios
  root        `ios/DeeplyDomain`           `ios/DeeplyDomain` + export ✗ (R5)   ✗ (private at root is unrepresentable)
  subdir      `ios/DeeplyDomain/Sub`       `ios/DeeplyDomain/Sub` + export      ✗ (R5)
android
  root        `android:domain`             ✗ (R5: no export concept)            ✗ (R5)
  subdir      `android:domain:sub`         ✗ (R5)                               ✗ (R5)
shared
  root        `shared:domain`              `shared:domain` + export             ✗ (R5)
  subdir      `shared:domain:sub`          `shared:domain:sub` + export         ✗ (R5)
```

The `✗ (R5)` cells are the finding: they are not violations by the author, they are **holes in the
rule set**. Each one is either a rule to narrow or a documented impossibility.

### Step 4 — Decide per empty cell

| Empty cell class | Action |
|------------------|--------|
| Reachable by a plausible author, and a real use case exists | **Narrow a rule.** The newer rule created the hole; narrow it. |
| Reachable but the use case is genuinely invalid | **Document the impossibility** in the rule set's own tests, so it is a decision not a surprise |
| Not reachable (an excluded tree, a deprecated platform) | Record the exclusion explicitly with its reason |

### Step 5 — Encode the invariant as a test

The matrix is an artefact; the test is the enforcement. The invariant form is always:

```
"every <dimension> has a legal spelling in every <other dimension>"
```

Encode it so the hole cannot reopen when someone refines either rule eight months from now.

---

## Three more real contradictions

These are the same defect under different names. They are recorded because each has a different
surface symptom, and the surface symptom is what makes them hard to recognise.

### Contradiction by grandfathering

A gate that runs in `--delta` mode splits findings into "introduced by this change" (blocking) and
"pre-existing" (advisory). This is a legitimate, well-motivated design: a corpus with known debt
cannot be blocked by that debt.

The contradiction: a rule that *only ever* fires on pre-existing code can never block. Grandfathering
is correct; a rule that is entirely grandfathered is decoration. The check that exposes it is to
ask, for each rule, **"has this rule ever blocked a commit?"** A rule that has never blocked is a
rule that does not constrain anything.

### Contradiction by section-set mismatch

A template declares 22 required sections. A validator enforces a subset (the 12 "core" sections),
skipping six as too generic to require. A different linter enforces a different subset. Each list is
defensible alone; together they produce documents that pass one check and fail another with no
indication that the lists disagree.

**Detection:** for every pair of validators over the same artefact class, diff their requirement
sets. The empty cells are the sections that are required by one and not checked by the other.

### Contradiction by severity

A rule is `blocking` in a pre-commit hook and `advisory` in CI, or vice versa. Both severities are
reasonable in isolation. The contradiction is that the *same* violation has two outcomes depending
on the path the developer took, which teaches the team which path to take.

**Detection:** for every rule, list its severity in every context where it runs, and require the
list to have one entry.

---

## Bidirectional consistency

A rule of the form "A and B must agree" has two directions, and only one is usually implemented.

```
Direction 1 (forward):  for every A, there is a B           → frequently checked
Direction 2 (reverse):  for every B, there is an A           → frequently a no-op
```

The failure is not hypothetical: a specification-versus-API checker had the reverse direction
written as a deliberate no-op, `if not fuzzy_found: pass  # Don't fail on extras`. The specification
silently fell to **41 documented paths while the API served 114**, and nothing failed because
nothing was checking the direction that would have noticed.

### Why the reverse direction decays to a no-op

Writing the forward direction is easy: you have the list of A's, and you look up each one in B.
Writing the reverse requires enumerating B, which is usually **not** a static list — it is the
output of a generator, the union of several sources, or the contents of a database. The reverse
direction therefore requires a way to enumerate B, and if that enumeration is hard, the honest move
(a failure) is much less attractive than the convenient one (a `pass` with a comment).

**Design rule:** if a consistency check cannot enumerate one side, that is a defect in the
enumeration capability, not a reason to skip the direction. Make the enumeration possible; then
check both ways.

### The one-way check in other clothes

| One-way check | The direction that rots |
|---------------|-------------------------|
| Freshness gate (`emit --check`) | Source→artefact is checked; artefact→source (is every artefact reachable?) is not |
| Schema validator | Documented→implemented is checked; implemented→documented is not |
| Chain symmetry validator | Only useful when both directions are compared; a one-directional version drifts silently |
| Dependency lockfile | Declared→locked is checked; locked→used (is every locked dep actually needed?) is not |

The pattern: the easy direction is always checked, and the easy direction is always the one whose
failure is already visible. Rot happens in the direction nobody wrote.

---

## Contradiction-check procedure, condensed

1. Collect every rule that constrains the declaration, **including rules in other tools**.
2. Extract the dimensions each rule cares about.
3. Build the product of the dimensions.
4. Fill each cell with a legal spelling, or mark it empty.
5. Every empty cell is a rule set defect: narrow a rule, or document the impossibility.
6. Encode "every X has a legal spelling in every Y" as a test.
7. Separately: for every "A must agree with B" rule, write the reverse direction and prove it is
   not a no-op.
