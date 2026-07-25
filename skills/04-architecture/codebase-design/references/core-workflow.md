## Core Workflow

```
DESIGN → MINIMIZE → SEAM → ADAPT → VERIFY
   ↑___________________________________|
              (iterate)
```

### Phase 1: Module Inventory

**Goal:** Catalog all modules in scope and classify each by depth.

```
┌──────────────────────────────────────────────────┐
│              MODULE INVENTORY                      │
│                                                    │
│  For each module:                                  │
│  1. Count public methods (interface cost)          │
│  2. Estimate lines of behavior (non-delegation)    │
│  3. Compute depth = behavior / interface           │
│  4. Classify:                                      │
│     ├── depth >= 3.0 → DEEP (keep, celebrate)      │
│     ├── 1.0 <= depth < 3.0 → MODERATE (investigate)│
│     └── depth < 1.0 → SHALLOW (mark for action)    │
│                                                    │
│  Output: depth scorecard for every module          │
└──────────────────────────────────────────────────┘
```

**Steps:**
1. List every module (class, file, package) in the target scope
2. For each, count public methods/symbols — this is the **interface cost**
3. Estimate lines of implementation (non-delegation, non-getter/setter logic) — this is **behavior**
4. Compute depth = behavior / interface cost
5. Classify modules as deep, moderate, or shallow

**Checkpoint:** Depth scorecard complete. All shallow modules flagged.

---

### Phase 2: Interface Minimization

**Goal:** Reduce the public surface of every module to the absolute minimum.

```
┌──────────────────────────────────────────────────┐
│           INTERFACE MINIMIZATION                   │
│                                                    │
│  For each method in the public interface:          │
│    Q1: Is this method called by external code?     │
│         NO → Make private (or delete)              │
│         YES → Continue                             │
│    Q2: Can this be combined with another method?   │
│         YES → Merge and reduce parameter count     │
│         NO → Continue                              │
│    Q3: Does this expose implementation detail?     │
│         YES → Hide behind abstraction              │
│         NO → Keep (justified)                      │
│                                                    │
│  After minimization: re-compute depth              │
└──────────────────────────────────────────────────┘
```

**Steps:**
1. List every public method/symbol
2. Apply the three questions above to each
3. Combine methods where possible (e.g., `setX()` + `setY()` → `configure(options)`)
4. Use default parameters instead of overloads
5. Narrow return types (return concrete types, not internal representations)
6. Hide implementation classes behind interfaces
7. Re-compute depth after minimization

**Checkpoint:** Interface minimized. Depth improved (ideally >3.0).

---

### Phase 3: Seam Identification

**Goal:** Find natural boundaries where modules can be cleanly separated.

```
┌──────────────────────────────────────────────────┐
│              SEAM IDENTIFICATION                   │
│                                                    │
│  Seam checklist for candidate boundary A|B:        │
│  ✓ A and B change at different rates               │
│  ✓ A can be tested independently from B            │
│  ✓ A has different performance characteristics     │
│  ✓ A has different error-handling needs            │
│  ✓ A serves different caller personas              │
│  ✓ B can be replaced without changing A            │
│                                                    │
│  Score: 6/6 = natural seam, 4-5/6 = candidate,     │
│         <4/6 = artificial boundary (reconsider)    │
└──────────────────────────────────────────────────┘
```

**Steps:**
1. Identify all candidate boundaries in the module inventory
2. Score each candidate against the seam checklist
3. Natural seams (5-6/6): proceed to Phase 4
4. Candidates (4/6): investigate — is the boundary worth formalizing?
5. Artificial (<4/6): do not add adapters here; look for better seams

**Checkpoint:** Seam map complete. Adapter targets identified.

---

### Phase 4: Adapter Placement

**Goal:** Place adapters at identified seams to decouple modules.

```
┌──────────────────────────────────────────────────┐
│              ADAPTER PLACEMENT                     │
│                                                    │
│  Module A  ───[raw]──→  Module B  (tight couple)  │
│       ↓                                ↑           │
│  Module A  ───[Adapter]──→  Interface  ←── Module B│
│                                                    │
│  Select adapter type by seam characteristics:      │
│  ├── Translation: different data formats           │
│  ├── Facade: simplify complex subsystem            │
│  ├── Anti-Corruption: protect domain from external │
│  └── Bridge: abstract over multiple implementations│
└──────────────────────────────────────────────────┘
```

**Steps:**
1. For each natural seam, select the appropriate adapter pattern
2. Define the interface that the adapter will expose
3. Implement the adapter with minimal surface area
4. Verify that Module A now depends only on the interface, not Module B
5. Update callers to use the adapter

**Checkpoint:** All natural seams have adapters. Coupling reduced.

---

### Phase 5: Deletion Test Verification

**Goal:** Validate that every module earns its existence.

```
┌──────────────────────────────────────────────────┐
│              DELETION TEST                         │
│                                                    │
│  For each module M:                                │
│  1. Imagine deleting M entirely                    │
│  2. What breaks?                                   │
│     ├── Nothing → M is dead code. Delete it.       │
│     ├── Only tests → M is test-only. Reassess.     │
│     ├── Callers can be trivially updated → Delete  │
│     └── Callers need significant rewrite → Keep    │
│  3. For kept modules:                              │
│     ├── Can callers use M's dependency directly?   │
│     │   YES → M is a pass-through. Delete it.       │
│     └── Does M add real behavior? → Keep, with     │
│         updated depth score                        │
└──────────────────────────────────────────────────┘
```

**Steps:**
1. Run the deletion test on every module in inventory
2. Delete modules that fail (dead code, pass-throughs, trivial wrappers)
3. Update callers of deleted modules to use the underlying dependency directly
4. Re-run depth analysis on remaining modules
5. Document decisions in ADR format

**Checkpoint:** All remaining modules pass the deletion test. Codebase is leaner.

---

### Iterate

After Phase 5, return to Phase 1 with the leaner codebase. Each iteration should increase the average module depth.
