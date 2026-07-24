# Conflict Patterns

Catalog of conflict patterns (textual, structural, semantic) with recognition heuristics and resolution templates.

## Textual Conflicts

- **Adjacent-line**: Different changes on adjacent lines. Resolution: interleave both if they don't overlap logically.
- **Same-line**: Exact same line modified by both. Resolution: one must win or a new combined line must be written.
- **Interleaved**: Alternating blocks from each side. Resolution: reconstruct the intended merged logic.

## Structural Conflicts

- **Import-reorder**: Import statements reorganized differently. Resolution: merge both import sets, deduplicate, sort.
- **Function-moved**: Same function moved to different locations. Resolution: pick one location, update all callers.
- **File-split**: One side split a file the other side modified. Resolution: apply modifications to the split files.
- **Rename-collision**: Same symbol renamed differently. Resolution: agree on one name, apply consistently.

## Semantic Conflicts

- **Logic-inversion**: One side negates the other's assumption. Resolution: identify the correct assumption, fix the dependent logic.
- **Contract-change**: Function signature vs call site mismatch. Resolution: update call sites or revert signature change.
- **Initialization-order**: Setup steps conflict. Resolution: determine correct initialization order, restructure.
- **Data-flow**: Data shape changes conflict with consumers. Resolution: create migration or adapter layer.
