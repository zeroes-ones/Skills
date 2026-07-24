# Hunk Analysis Methodology

Detailed methodology for analyzing individual conflict hunks, classifying complexity, and identifying dependency relationships between hunks.

## Hunk Anatomy

A conflict hunk consists of three sections delimited by markers:
- `<<<<<<<` HEAD (OURS) — the current branch's version
- `=======` — separator between the two versions
- `>>>>>>>` branch-name (THEIRS) — the incoming branch's version

## Complexity Classification

| Level | Lines Changed | Characteristics |
|-------|-------------|----------------|
| Trivial | 1-3 lines | Whitespace, import order, comment changes |
| Simple | 4-10 lines | Single function/block modified, clear intent |
| Moderate | 11-30 lines | Multiple blocks, refactored code, renamed symbols |
| Complex | 31+ lines | Structural changes, new abstractions, moved code |

## Dependency Detection

Hunks are dependent if they share any of: same function, same import, same type definition, same control flow path. Resolve shared dependencies first, then their consumers.

## Risk Assessment

HIGH: >3 hunks in critical-path code, or semantic overlap with other conflicted files.
MEDIUM: 2-3 hunks in moderate complexity code.
LOW: 1 hunk in isolated module or non-critical path.
