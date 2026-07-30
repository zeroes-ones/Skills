#!/usr/bin/env python3
"""
Add RESEARCH_PREREQUISITE section to all SKILL.md files that don't already have one.

This enforces the RUNTIME gate: when any skill is invoked, the agent MUST research
before producing output. The RP section is read by the consuming agent and serves
as a hard prerequisite — skip research = invalid output.

Usage:
    python3 scripts/add-research-prerequisite.py [--dry-run] [--skill-dir PATH]
"""

import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_DIR = os.path.join(REPO_ROOT, "skills")

UNIVERSAL_RP = """## <!-- DEEP: 5+min --> RESEARCH_PREREQUISITE — Execute Before Any Output

**This is a HARD GATE. Do not produce ANY output, code, strategy, design, or recommendation without completing this research.**

Before you act, you MUST execute every applicable research step. Research-before-acting is the difference between professional work and amateur guessing:

| # | Research Step | Why It Matters | Where to Look |
|---|--------------|----------------|----------------|
| **RP1** | **Verify domain currency.** Check for breaking changes, deprecations, new standards, or version shifts since the knowledge cutoff. | [STALE_RISK] Outdated advice breaks real systems. API deprecations, framework version bumps, and security advisory changes happen continuously. Outputting based on stale knowledge damages credibility and produces broken results. | Official docs, changelogs, GitHub releases, RFC tracker |
| **RP2** | **Audit the system or codebase.** Read relevant files. Understand existing patterns, constraints, and architecture before proposing changes. | [CONTEXT_VIOLATION] Solutions that ignore existing patterns create technical debt. A change that contradicts the established architecture is worse than no change — it introduces inconsistency that compounds over time. | Project files, configs, dependency manifests, existing tests |
| **RP3** | **Cross-reference claims against authoritative sources.** Every factual assertion needs a verifiable source. Mark each: [VERIFIED], [COMPUTED], or [ESTIMATED]. | [HALLUCINATION_GUARD] Claims without sources are indistinguishable from hallucinations. The #1 cause of incorrect output is treating assumptions as facts. Source tagging prevents this. | Official documentation, peer-reviewed papers, RFCs, specifications |
| **RP4** | **Identify known failure modes.** Before recommending, list what commonly breaks. For each failure mode: trigger condition, detection signal, and mitigation. | [FAILURE_BLINDNESS] Every domain has known failure patterns. Output that doesn't address them is dangerously incomplete. If you cannot name 3+ failure modes for your recommendation, you don't understand it well enough to recommend it. | Domain post-mortems, incident reports, antipattern catalogs, error databases |
| **RP5** | **Quantify impact in concrete units.** Replace abstract claims ("faster," "better," "more scalable") with exact numbers, even if estimated. | [VAGUENESS_PENALTY] "Faster" is unverifiable. "Reduces p95 latency from 340ms to 120ms (±15ms)" is verifiable. Abstract adjectives hide ignorance behind confidence. Concrete numbers expose gaps. | Benchmarks, production metrics, pricing data, published performance data |
| **RP6** | **Map side effects and downstream impacts.** What else breaks? Which dependencies are affected? Which downstream consumers need updating? | [CASCADE_BLINDNESS] Changes to one component ripple outward. A fix in module A can break module B that depends on A's old behavior. Map the blast radius before acting. | Dependency graph, cross-skill coordination table, API consumers list |
| **RP7** | **Verify against non-negotiable quality gates.** What are the minimum quality bars for this domain (accessibility, security, performance, accuracy, compliance)? | [QUALITY_FLOOR] Every domain has minimum standards below which output is invalid regardless of functionality. Missing WCAG AA = broken. Leaking credentials = broken. Silent data loss = broken. | Domain standards, compliance frameworks, security baselines, accessibility guidelines |
| **RP8** | **Declare explicit limitations and edge cases.** What does this NOT handle? What are the known boundaries? What scenarios are explicitly out of scope? | [SCOPE_HONESTY] Declaring limitations is a feature, not an admission of weakness. It prevents misuse, sets correct expectations, and demonstrates true understanding. Every solution has boundaries — naming them is professional. | This SKILL.md, domain literature, edge case databases |

**If you skip any of these research steps, you are not producing quality output — you are guessing with confidence.** Guessing wastes time, breaks systems, and destroys trust. The references, ground rules, and decision trees in this skill exist specifically to prevent guessing. Use them.

> **Compliance:** Research must be executed before any substantial output. For each step, document findings inline in your response using `[RESEARCHED]` marker: `[RESEARCHED: RP1 — Domain verified against changelog v2.4. No breaking changes since cutoff.]`. Partial research = partial quality. Zero research = zero credibility.
"""


def has_research_prerequisite(content):
    """Check if skill already has a RESEARCH_PREREQUISITE section."""
    return bool(re.search(
        r'RESEARCH[_ ]PREREQUISITE|RESEARCH[_ ]PREREQ|HARD GATE.*[Rr]esearch|Execute Before Any (Strategy|Output|Decision)',
        content, re.IGNORECASE
    ))


def find_insertion_point(lines):
    """
    Find where to insert RP section.
    Strategy: insert after description block, before the first operational section.
    Look for '## Route', '## Anti-Hallucination', '## Ground Rules' — whichever comes first.
    If none found, insert after the first ## heading.
    """
    patterns = [
        r'^##\s*(<!--[^>]*>\s*)?Route the Request',
        r'^##\s*(<!--[^>]*>\s*)?Anti.Hallucination',
        r'^##\s*(<!--[^>]*>\s*)?Ground Rules',
        r'^##\s*(<!--[^>]*>\s*)?The Expert',
        r'^##\s*(<!--[^>]*>\s*)?Operating at Different',
        r'^##\s*(<!--[^>]*>\s*)?When to Use',
    ]

    earliest = None
    for i, line in enumerate(lines):
        for pat in patterns:
            if re.match(pat, line):
                if earliest is None or i < earliest:
                    earliest = i
                break
        if earliest is not None:
            break

    if earliest is not None:
        # Find the blank line before this section header
        insert_line = earliest
        # Walk back to find a blank line or start of file for clean insertion
        while insert_line > 0 and lines[insert_line - 1].strip() == '':
            insert_line -= 1
        return insert_line

    # Fallback: insert after the first ## heading
    for i, line in enumerate(lines):
        if line.startswith('##'):
            return i

    # Absolute fallback: after line 10 (description usually ends by then)
    return min(10, len(lines))


def add_rp_to_skill(filepath, dry_run=False):
    """Add RESEARCH_PREREQUISITE to a single SKILL.md file."""
    with open(filepath, 'r') as f:
        content = f.read()

    if has_research_prerequisite(content):
        return 'skipped', 'already has RP'

    lines = content.split('\n')
    insert_at = find_insertion_point(lines)

    # Build new content with RP section inserted
    rp_lines = UNIVERSAL_RP.split('\n')
    new_lines = lines[:insert_at] + rp_lines + [''] + lines[insert_at:]
    new_content = '\n'.join(new_lines)

    if dry_run:
        return 'dry-run', f'would insert at line {insert_at + 1}'

    with open(filepath, 'w') as f:
        f.write(new_content)
    return 'added', f'inserted at line {insert_at + 1}'


def main():
    dry_run = '--dry-run' in sys.argv

    # Optional: target a specific skill
    target_dir = None
    for i, arg in enumerate(sys.argv):
        if arg == '--skill-dir' and i + 1 < len(sys.argv):
            target_dir = sys.argv[i + 1]

    if target_dir:
        filepath = os.path.join(target_dir, 'SKILL.md')
        if not os.path.exists(filepath):
            filepath = target_dir  # might be a direct path
        status, msg = add_rp_to_skill(filepath, dry_run=dry_run)
        print(f"  [{status.upper()}] {os.path.basename(os.path.dirname(filepath))}: {msg}")
        return

    # Process all skills
    stats = {'added': 0, 'skipped': 0, 'dry-run': 0, 'error': 0}
    for root, dirs, files in os.walk(SKILLS_DIR):
        if 'SKILL.md' in files:
            # Verify this is a skill directory (depth 3 from skills/)
            # skills/XX-domain/skill-name/SKILL.md
            rel = os.path.relpath(root, SKILLS_DIR)
            parts = rel.split(os.sep)
            if len(parts) == 2:  # domain/skill-name
                try:
                    status, msg = add_rp_to_skill(os.path.join(root, 'SKILL.md'), dry_run=dry_run)
                    stats[status] += 1
                    print(f"  [{status.upper()}] {parts[1]}: {msg}")
                except Exception as e:
                    stats['error'] += 1
                    print(f"  [ERROR] {parts[1]}: {e}")

    print(f"\nSummary: {stats['added']} added, {stats['skipped']} skipped, {stats['error']} errors")
    if dry_run:
        print("DRY RUN — no files were modified. Remove --dry-run to apply.")


if __name__ == '__main__':
    main()
