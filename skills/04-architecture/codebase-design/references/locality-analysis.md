# Locality Analysis

## What Is Locality?

**Locality** measures whether related code lives close together. High locality means files that change together are in the same directory. Low locality means related concepts are scattered across the codebase — the primary cause of "tribal knowledge" where only senior developers know which files to touch for a given change.

## Locality Score

### Co-Change Frequency
Run `git log --name-only --since="90 days ago" | sort | uniq -c | sort -rn`. High co-change counts indicate coupled files.

### Spatial Distance
Measure directory tree distance between co-changing files. Same directory = distance 0. Sibling directories = distance 1. Different top-level directories = distance 3+.

### Conceptual Distance
Do the files share domain language? Same entity names, same business concepts? Low conceptual distance with high spatial distance is a strong locality violation.

## Locality Score Formula
```
LocalityScore = 1 / (SpatialDistance × CoChangeFrequency)
```
Lower score = worse locality. Score < 0.1 triggers co-location consideration.

## Co-Location Decision Framework

1. Collect co-change data (last 90 days, minimum 5 co-changes to qualify)
2. For each file pair with co-change count ≥ 5 and spatial distance ≥ 2, compute locality score
3. Group files by domain concept
4. Propose directory reorganization: move files with score < 0.1 into shared directories
5. Validate: does the new grouping reduce the average spatial distance for co-changing files?

## Red Flags

- Three or more files in different directories change together in >80% of commits touching any one of them
- New developers consistently miss files when making changes in a domain area
- Code review comments frequently say "you also need to update X" where X is in a different directory
