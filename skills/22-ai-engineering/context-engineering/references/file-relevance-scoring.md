# File Relevance Scoring

## Overview

How to score every candidate file for context inclusion. A file should earn its way into the context window — no free passes.

## The Scoring Formula

```
relevance(file) = 0.35 * recency_score(file) 
                + 0.30 * proximity_score(file) 
                + 0.25 * semantic_score(file) 
                + 0.10 * size_penalty(file)
```

## Factor 1: Recency Score (0.35 weight)

How recently was this file changed? Files changed in the current task's diff are most relevant.

```
recency_score = 1.0 if file in current git diff
              = 0.8 if file in last commit
              = 0.5 if file modified this week
              = 0.3 if file modified this month
              = 0.1 if file modified > 1 month ago

Boost: +0.2 if file was edited by the agent in the current session
```

**Data source:** `git diff --name-only HEAD`, `git log --since="7 days ago" --name-only`

## Factor 2: Proximity Score (0.30 weight)

How close is this file in the dependency graph to files the agent is actively editing?

```
proximity_score = 1.0 if file is in the active edit set (Priority A)
                = 0.8 if direct dependency (imported by a Priority A file)
                = 0.5 if 2 hops away (dependency of a dependency)
                = 0.3 if 3 hops away
                = 0.1 if 4+ hops away
                = 0.0 if no path in dependency graph

Special: test files for Priority A source → assigned 0.7 regardless of hop distance
```

**Data source:** Dependency graph from `pycg` (Python), `madge` (JS/TS), `depcruise` (JS/TS), or language server.

## Factor 3: Semantic Score (0.25 weight)

How semantically similar is the file's content to the task description?

```
semantic_score = cosine_similarity(
    embed(task_description),
    embed(file_summary)  // First 200 tokens + function/class names
)

Thresholds:
  > 0.8 → Highly relevant (same feature area)
  0.6-0.8 → Moderately relevant
  0.4-0.6 → Weakly relevant
  < 0.4 → Likely irrelevant
```

Use the cheapest available embedding model (`text-embedding-3-small` or local `all-MiniLM-L6-v2`).

## Factor 4: Size Penalty (0.10 weight)

Very large files degrade context quality. Penalize them slightly.

```
size_penalty = min(1.0, 500 / max(file_lines, 1))
            = 1.0 for files < 500 lines (no penalty)
            = 0.5 for 1000-line files
            = 0.25 for 2000-line files
            = 0.1 for 5000+ line files (heavily penalized)
```

## Decay and Boost Rules

| Condition | Multiplier |
|-----------|-----------|
| File included in last 3 turns but never referenced | 0.5x |
| File referenced by agent (tool call, edit, mention) | 1.3x |
| File explicitly requested by agent | 1.5x (overrides all decay) |
| File is a config file (.yaml, .json, .toml, .env) | 0.7x (unless agent is editing config) |
| File is a generated file (*.generated.*, *.min.*) | 0.1x (almost never relevant) |

## Scoring Pipeline

```
Raw file list → Recency scoring → Proximity scoring → Semantic scoring 
→ Size penalty → Decay/Boost → Final score → Sort descending → Threshold filter
```

## Minimum Thresholds

- **Production tasks:** 0.4 minimum (conservative — avoid missing context)
- **Exploratory tasks:** 0.3 minimum (allow broader context)
- **Debugging tasks:** 0.2 minimum (may need unusual files)
- **Never:** drop below 0.2 — at that point the file is noise
