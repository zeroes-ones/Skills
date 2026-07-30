#!/usr/bin/env python3
"""
Updates the universal RESEARCH_PREREQUISITE in all SKILL.md files to include
the Iterative Research Loop pattern — research at every decision point, not just entry.

This transforms RP from a one-time gate into a continuous research cycle.
"""
import os, sys, re

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The old closing line to find and the new iterative section to insert after it
OLD_CLOSING = """> **Compliance:** Research must be executed before any substantial output."""

ITERATIVE_LOOP_ADDITION = """
### 🔄 Iterative Research Loop — Research at EVERY Decision Point, Not Just Entry

**The RP1-RP8 cycle above is NOT a one-time gate.** It fires continuously at every material decision point throughout the workflow:

| Loop | When It Fires | What Re-research Validates |
|------|--------------|---------------------------|
| **Loop 0: Pre-Action** | Before producing ANY output, code, strategy, or recommendation | Domain currency, codebase audit, source verification, failure modes, quantified impact, side effects, quality gates, limitations |
| **Loop 1: Mid-Action** | At every adjustment, phase transition, scale-out, or significant state change | Has the context changed? Are the original assumptions still valid? Has new information invalidated the Loop 0 conclusions? |
| **Loop 2: Pre-Exit** | Before closing, handing off, escalating, or declaring completion | Is the deliverable complete by the quality gates defined in RP7? Are all limitations declared (RP8)? Have failure modes been addressed (RP4)? |
| **Loop 3: Post-Action** | After completion: compare expected vs. actual outcome | What was the efficiency ratio (actual / theoretical max)? What learnings emerged? What should be fed back into the pattern database for future decisions? |

**Integration into Core Workflow:**

Every decision point in a skill's Core Workflow must be marked with:
```
[RESEARCH LOOP: Re-execute RP1-RP8 before proceeding to next phase]
```

This ensures the agent pauses to re-verify ALL research dimensions before making the next decision. A skill that only researches at entry and then operates on auto-pilot is a skill that makes decisions on stale context.

**Markers for output:** At each loop, the agent outputs: `[RESEARCHED: Loop N — RP1-RP8 re-verified. Key delta from previous loop: ...]`

**Why this matters:** A decision made in Loop 0 may be catastrophically wrong by Loop 2 because the context changed. Markets move. Requirements shift. Dependencies update. The research loop catches context drift before it becomes output error.

> **Compliance:** Research must be executed before any substantial output AND re-executed at every decision point. For each research loop, document findings inline. Partial research = partial quality. Zero research = zero credibility. Stale research = dangerous confidence.
"""


def already_has_iterative_loop(content):
    """Check if skill already has the Iterative Research Loop section."""
    return bool(re.search(r'Iterative Research Loop|🔄.*Iterative|research.*every.*decision.*point|Loop 0.*Pre-Action', content, re.IGNORECASE))


def add_iterative_loop(filepath, dry_run=False):
    with open(filepath, 'r') as f:
        content = f.read()
    
    if already_has_iterative_loop(content):
        return 'skipped', 'already has iterative loop'
    
    if OLD_CLOSING not in content:
        return 'skipped', 'no universal RP found (may have domain-specific RP only)'
    
    # Find the end of the compliance paragraph (after OLD_CLOSING line)
    idx = content.index(OLD_CLOSING)
    # Find end of this line
    end_of_line = content.index('\n', idx)
    # Find the next blank line or ## heading after the compliance line
    rest = content[end_of_line + 1:]
    # The compliance line is followed by more text on the same paragraph. Find where the paragraph ends.
    # The paragraph ends at the next blank line or ## heading
    para_end = end_of_line
    for ch in content[end_of_line + 1:]:
        if ch == '\n':
            para_end += 1
            # Check if next line is blank or a heading
            next_pos = para_end + 1
            if next_pos >= len(content) or content[next_pos] == '\n' or content[next_pos:next_pos+2] == '##':
                break
        else:
            para_end += 1
    
    if dry_run:
        line_num = content[:end_of_line].count('\n') + 1
        return 'dry-run', f'would add iterative loop after line ~{line_num}'
    
    # Insert the iterative loop after the compliance paragraph
    new_content = content[:para_end + 1] + '\n' + ITERATIVE_LOOP_ADDITION + '\n' + content[para_end + 1:]
    
    with open(filepath, 'w') as f:
        f.write(new_content)
    return 'added', 'iterative loop inserted'


def main():
    dry_run = '--dry-run' in sys.argv
    skills_dir = os.path.join(REPO_ROOT, 'skills')
    stats = {'added': 0, 'skipped': 0, 'error': 0, 'dry-run': 0}
    
    target = None
    for i, arg in enumerate(sys.argv):
        if arg == '--skill-dir' and i + 1 < len(sys.argv):
            target = sys.argv[i + 1]
    
    count = 0
    for root, dirs, files in os.walk(skills_dir):
        if 'SKILL.md' in files:
            rel = os.path.relpath(root, skills_dir)
            parts = rel.split(os.sep)
            if len(parts) == 2:
                skill_name = parts[1]
                if target and skill_name != target:
                    continue
                try:
                    status, msg = add_iterative_loop(os.path.join(root, 'SKILL.md'), dry_run=dry_run)
                    stats[status] += 1
                    count += 1
                    if count <= 10 or status == 'added':
                        print(f"  [{status.upper()}] {skill_name}: {msg}")
                except Exception as e:
                    stats['error'] += 1
                    print(f"  [ERROR] {skill_name}: {e}")
    
    print(f"\nSummary: {stats['added']} updated, {stats['skipped']} skipped, {stats['error']} errors")
    if dry_run:
        print("DRY RUN — no files were modified.")


if __name__ == '__main__':
    main()
