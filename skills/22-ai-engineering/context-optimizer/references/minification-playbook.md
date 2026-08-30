# Minification Playbook — Lossless Reductions

> Apply in order. All are lossless (or gated) — no retention test needed, but the cache prefix (R5) is never touched.

## 1. Dedup (highest ROI, zero risk)

- Hash every paragraph; merge pairs with Jaccard similarity > 0.85.
- Catches copy-pasted code blocks, duplicate error messages, repeated instructions.
- Run BEFORE any compression — deduping first means compression wastes no tokens on duplicates.

## 2. Exclusion (second, gated by relevance)

- Drop files never referenced by the task (relevance gate: not included in the last N turns, no import/ref path).
- Drop known noise classes outright: lockfiles, minified bundles, compiled artifacts, `.pyc`, `.DS_Store`.
- Never exclude Level 1 (rules) or Level 4 (error output) without explicit override.

## 3. Whitespace and structure collapse

- Collapse whitespace in non-code text.
- Strip comments from source files (unless the task is documentation).
- Remove decorative markdown (horizontal rules, redundant emphasis) — never remove semantic markers (headings, code fences).

## 4. Truncation of noise

- Truncate long string literals > 500 chars to `"...[truncated {N} chars]"`.
- Trim error output to the last 50 lines + full stack trace (L4 rule) — never excluded, never raw.

## 5. What you may NOT minify

- The frozen cache prefix (R5).
- L1 rules / instructions.
- User-authored requirements.
- Constraint-bearing content (security, compliance, format specs) — keep verbatim.

## Verification

- The payload still answers the held-out question set (cheap smoke test).
- `diff` of the stable prefix across requests is empty.
- Measured token delta committed per step.
