# Context Pollution Patterns

## Overview

Context pollution occurs when irrelevant, redundant, or misleading information enters the context window and degrades agent performance. This reference catalogs the most common pollution vectors and their fixes.

## Pattern 1: The "Just In Case" Inclusion

**Symptom:** Entire directories included without filtering. Agent receives 40 files but only needs 6.

**Detection:** `jq '.context.files | length' context.json` — if count > 15 for a standard task, investigate.

**Cost:** ~$0.02-0.05 per unnecessary file per request. At scale: hundreds per month.

**Fix:** Mandatory relevance scoring. No file enters context without score > 0.4 and explicit inclusion reason.

## Pattern 2: Stale Context Drift

**Symptom:** Files that were relevant 10 turns ago persist in context despite the task having moved on.

**Detection:** Track `last_referenced_turn` per file. Files with `current_turn - last_referenced_turn > 5` are stale.

**Cost:** Stale files occupy 15-30% of context budget in long sessions, forcing eviction of newly relevant files.

**Fix:** Per-turn relevance decay. Apply 0.8x multiplier for each unreferenced turn. Evict when score drops below threshold.

## Pattern 3: Error Echo Chamber

**Symptom:** Same error output included across multiple turns, causing the agent to fixate on a resolved issue.

**Detection:** Hash error outputs. If the same hash appears in 3+ turns, pollution confirmed.

**Cost:** Agent wastes 2-5 extra turns re-analyzing resolved errors. At $0.05/turn: $0.10-0.25 per incident.

**Fix:** Track resolved errors. Strip resolved errors from Level 4 in subsequent turns. Include only unresolved errors.

## Pattern 4: Redundant Information from Multiple Sources

**Symptom:** The same information appears from a README, a docstring, a comment, and a spec file — all included.

**Detection:** Paragraph-level deduplication (Jaccard > 0.85). Flag files with > 30% duplicate content.

**Cost:** 10-20% of context budget wasted on duplicates in documentation-heavy repos.

**Fix:** Content-aware deduplication during assembly. Keep the most authoritative source (spec > docstring > comment).

## Pattern 5: Configuration File Sprawl

**Symptom:** Every `.yaml`, `.json`, `.toml`, `.env.example` in the repo gets included.

**Detection:** Count config files in context. If > 3 for a non-config task, sprawl confirmed.

**Cost:** Config files average 200-500 tokens. 10 unnecessary configs = 2K-5K wasted tokens per request.

**Fix:** Only include config files if the task involves configuration changes. Otherwise, max 1 config file (the most relevant one).

## Pattern 6: The Log File Trap

**Symptom:** Entire log files (often 50K+ tokens) included because "the error might be in there."

**Detection:** Any file > 500 lines with `.log` extension in context → immediate flag.

**Cost:** A single 50K-token log file at Anthropic pricing: $0.15 per request. 100 requests/day: $15/day wasted.

**Fix:** Log files are Level 4, not Level 3. Always trim to relevant time window. Use grep to extract only error/warn lines.

## Prevention Checklist

- [ ] Every file in context has a recorded inclusion reason
- [ ] No file persists beyond 5 unreferenced turns
- [ ] Resolved errors are purged from subsequent turns
- [ ] Content deduplication runs before every context submission
- [ ] Config files capped at 3 unless task is config-related
- [ ] Log files always trimmed to < 50 lines unless debugging
