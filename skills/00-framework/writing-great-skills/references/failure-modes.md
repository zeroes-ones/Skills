# Failure Modes

## The Six Failure Modes of Skills

### 1. Premature Completion
The model completes after step 1 because step 1's output looks like a valid final output.
- **Detection:** Step 1 produces a complete-looking artifact; model declares "Done!"
- **Fix:** Every step must produce an artifact that is visibly INCOMPLETE until the full workflow finishes. Use intermediate artifacts (drafts, partial files).

### 2. Duplication
The same information appears in multiple places, diverging over successive edits.
- **Detection:** `grep` for identical sentences >15 words across the skill file.
- **Fix:** Single source of truth. Every concept appears exactly once. Link, don't copy.

### 3. Sediment
Reference material (definitions, explanations) migrates into steps sections.
- **Detection:** Definitional language ("is a", "means") in Core Workflow or Decision Trees.
- **Fix:** Move definitions to references. Keep steps procedural.

### 4. Sprawl
The skill exceeds its token budget, loading unnecessary context into every invocation.
- **Detection:** `wc -l` on body content >500 lines.
- **Fix:** No-op elimination → sediment mining → merge similar rules → push to external.

### 5. No-Op
Sentences that change nothing about model behavior but cost tokens.
- **Detection:** "If I delete this sentence, does behavior change?" If no → no-op.
- **Fix:** Delete or replace with a concrete constraint.

### 6. Negation
Primary framing uses negation ("Don't use for X"), which models struggle to pattern-match.
- **Detection:** "Don't", "Never", "Avoid" as primary framing in description or name.
- **Fix:** Rephrase as positive boundary. "Do NOT use for" is acceptable in descriptions.

## Failure Mode Interactions

These modes compound: duplication + no-op = double the dead weight. Sediment + sprawl = skill is both bloated and confusing. Premature completion + no-op = model stops early and the rest was dead weight anyway.
