#!/usr/bin/env python3
"""
Inject anti-hallucination ground rules and state-log sections into all SKILL.md files.

Adds two standardized sections to every skill:
1. Anti-Hallucination Ground Rules (injected into Ground Rules section)
2. State Log / Decision Ledger section (injected before Production Checklist)

Usage:
    python3 scripts/inject-anti-hallucination.py          # dry-run: show what would change
    python3 scripts/inject-anti-hallucination.py --apply  # apply changes
    python3 scripts/inject-anti-hallucination.py --stats  # show coverage stats
"""

import re
import sys
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parent.parent

# ─── Anti-Hallucination Ground Rules Block ───────────────────────────────────

ANTI_HALLUCINATION_RULES = """- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
"""

# ─── State Log / Decision Ledger Section ─────────────────────────────────────

STATE_LOG_SECTION = """## State Log

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.

### How the State Log Works
<!-- AGENT: Read this before starting work, update after each phase -->

1. **On session start:** Check `.copilot/session-state/decision-ledger.json` for any prior decisions relevant to this domain. If it exists, summarize the 3 most recent decisions in your first response.
2. **After each major decision:** Append to the ledger:
   ```json
   {
     "timestamp": "ISO-8601",
     "skill": "{this-skill-name}",
     "phase": "Phase 3: Implementation",
     "decision": "What was decided",
     "rationale": "Why this choice over alternatives",
     "constraints": ["constraint-1", "constraint-2"],
     "alternatives_considered": ["alt-1", "alt-2"],
     "reversible": true
   }
   ```
3. **Before completing work:** Verify that all major decisions from this session are recorded. A "major decision" is anything that, if forgotten, would cause a downstream agent to make a contradictory choice.
4. **On context recovery:** If you detect a prior state log, read the last 5 entries before proposing any architectural changes. Cite the prior decisions you're building on.

### State Log Schema

| Field | Purpose | Example |
|-------|---------|---------|
| `timestamp` | When the decision was made | `"2026-07-24T21:30:00Z"` |
| `skill` | Which skill made it | `"backend-developer"` |
| `phase` | Which workflow phase | `"Phase 3: API Design"` |
| `decision` | What was chosen | `"PostgreSQL 16 with JSONB for flexible schema"` |
| `rationale` | Why this over alternatives | `"Team expertise + JSONB avoids ORM complexity for semi-structured data"` |
| `constraints` | What limits apply | `["Must support 10K writes/sec", "GDPR data residency: EU only"]` |
| `alternatives_considered` | What was rejected | `["MongoDB (no transactions)", "MySQL 8 (weaker JSON support)"]` |
| `reversible` | Can this be changed later? | `true` (migration possible) or `false` (irreversible choice) |

### Anti-Drift Check
<!-- AGENT: Run this check at the start of each new phase -->

Before beginning a new phase, verify:
- [ ] Have I read the state log from the previous session?
- [ ] Do any prior decisions constrain what I'm about to do?
- [ ] Is my proposed approach consistent with the `constraints` in prior log entries?
- [ ] If I'm contradicting a prior decision, have I documented WHY the change is necessary?
"""

# ─── Patterns for Detection ─────────────────────────────────────────────────

# These patterns determine if a skill already has anti-hallucination or state-log content
ANTI_HALLUCINATION_SIGNATURES = [
    r"admit.*uncertain|never fabricate|don't invent|do not guess|flag.*knowledge cutoff",
    r"hallucinat.*prevent|anti.?hallucination",
    r"distinguish.*know.*infer|verified.*common.?practice.*inferred",
]

STATE_LOG_SIGNATURES = [
    r"state log|state ledger|decision ledger",
    r"decision log|session state.*log",
    r"record.*decision.*rationale|maintain.*state.*log",
    r"## State Log",  # Already has the section
]


def has_anti_hallucination(content: str) -> bool:
    """Check if skill already has anti-hallucination guardrails."""
    for pattern in ANTI_HALLUCINATION_SIGNATURES:
        if re.search(pattern, content, re.IGNORECASE):
            return True
    return False


def has_state_log(content: str) -> bool:
    """Check if skill already has state log mechanism."""
    for pattern in STATE_LOG_SIGNATURES:
        if re.search(pattern, content, re.IGNORECASE):
            return True
    return False


def find_injection_point_for_rules(content: str) -> Optional[int]:
    """
    Find where to inject anti-hallucination rules.
    Best: after the last line of the existing Ground Rules section.
    Strategy: find the Ground Rules heading, then find the last numbered rule or bullet
    that belongs to it, and inject right after.
    """
    lines = content.split("\n")
    gr_start = None
    gr_end = None

    for i, line in enumerate(lines):
        if re.match(r"^## Ground Rules", line):
            gr_start = i
        if gr_start is not None and re.match(r"^## (?!Ground Rules)", line) and i > gr_start:
            gr_end = i
            break

    if gr_start is None:
        return None

    if gr_end is None:
        gr_end = len(lines)

    # Find the last bullet or numbered line within Ground Rules
    for i in range(gr_end - 1, gr_start, -1):
        stripped = lines[i].strip()
        if stripped.startswith("- ") or re.match(r"^\d+\.", stripped):
            return i + 1  # Inject after this line

    # Fallback: inject right before the next section after Ground Rules
    return gr_end


def find_injection_point_for_state_log(content: str) -> Optional[int]:
    """
    Find where to inject the State Log section.
    Best: right before the Production Checklist or Verification Guardrails section.
    """
    # Priority targets for injection (before these sections)
    priority_targets = [
        r"^## Production Checklist",
        r"^## Verification Guardrails",
        r"^## What Good Looks Like",
        r"^## Cross-Skill Coordination",
        r"^## References",
    ]

    lines = content.split("\n")
    for pattern in priority_targets:
        for i, line in enumerate(lines):
            if re.match(pattern, line):
                # Insert a blank line before and the section before the target
                return i

    return None


def inject_rules(content: str) -> str:
    """Inject anti-hallucination ground rules."""
    injection_point = find_injection_point_for_rules(content)
    if injection_point is None:
        return content

    lines = content.split("\n")
    # Add blank line separator then the rules
    injection_lines = [""] + ANTI_HALLUCINATION_RULES.strip().split("\n")
    lines = lines[:injection_point] + injection_lines + lines[injection_point:]
    return "\n".join(lines)


def inject_state_log(content: str, skill_name: str) -> str:
    """Inject State Log section."""
    injection_point = find_injection_point_for_state_log(content)
    if injection_point is None:
        return content

    # Replace {this-skill-name} placeholder
    state_log_content = STATE_LOG_SECTION.replace("{this-skill-name}", skill_name)

    lines = content.split("\n")
    injection_lines = [""] + state_log_content.strip().split("\n") + [""]
    lines = lines[:injection_point] + injection_lines + lines[injection_point:]
    return "\n".join(lines)


def get_skill_name(skill_path: Path) -> str:
    """Extract skill name from directory name."""
    return skill_path.parent.name


def process_skill(skill_path: Path, apply: bool = False) -> dict:
    """Process a single skill file. Returns stats."""
    with open(skill_path) as f:
        content = f.read()

    skill_name = get_skill_name(skill_path)
    result = {
        "path": str(skill_path.relative_to(REPO_ROOT)),
        "name": skill_name,
        "had_anti_hallucination": has_anti_hallucination(content),
        "had_state_log": has_state_log(content),
        "injected_rules": False,
        "injected_state_log": False,
    }

    new_content = content

    if not result["had_anti_hallucination"]:
        result["injected_rules"] = True
        new_content = inject_rules(new_content)

    if not result["had_state_log"]:
        result["injected_state_log"] = True
        new_content = inject_state_log(new_content, skill_name)

    if apply and (result["injected_rules"] or result["injected_state_log"]):
        with open(skill_path, "w") as f:
            f.write(new_content)

    return result


def main():
    apply = "--apply" in sys.argv
    stats_only = "--stats" in sys.argv

    if apply:
        print("⚠️  APPLY MODE — will modify files. Dry-run first to review.\n")

    skill_files = sorted(REPO_ROOT.rglob("skills/**/SKILL.md"))
    # Exclude framework skills from main scan (they're special)
    skill_files = [f for f in skill_files if "00-framework" not in str(f)]

    if stats_only:
        # Only framework skills
        framework_files = sorted((REPO_ROOT / "skills" / "00-framework").rglob("SKILL.md"))
        skill_files = framework_files + skill_files

    results = []
    for sf in skill_files:
        result = process_skill(sf, apply=apply)
        results.append(result)

    # Stats
    total = len(results)
    with_anti = sum(1 for r in results if r["had_anti_hallucination"])
    with_state = sum(1 for r in results if r["had_state_log"])
    would_inject_rules = sum(1 for r in results if r["injected_rules"])
    would_inject_state = sum(1 for r in results if r["injected_state_log"])

    print(f"\n{'='*60}")
    print(f"  Anti-Hallucination & State-Log Injection Report")
    print(f"{'='*60}")
    print(f"  Skills scanned:          {total}")
    print(f"  Already have anti-hall:  {with_anti} ({with_anti*100//total}%)")
    print(f"  Already have state log:  {with_state} ({with_state*100//total}%)")
    action_rules = "Would inject" if not apply else "Injected"
    action_state = "Would inject" if not apply else "Injected"
    print(f"  {action_rules} rules:     {would_inject_rules}")
    print(f"  {action_state} state log:  {would_inject_state}")
    print(f"{'='*60}")

    if not apply:
        print("\n💡 Run with --apply to apply changes.")
        # Show a sample of what would change
        changed = [r for r in results if r["injected_rules"] or r["injected_state_log"]]
        if changed:
            print(f"\nSample of {len(changed)} skills that would be modified:")
            for r in changed[:5]:
                tags = []
                if r["injected_rules"]:
                    tags.append("+anti-hallucination")
                if r["injected_state_log"]:
                    tags.append("+state-log")
                print(f"  {r['name']}: {', '.join(tags)}")
    else:
        print("\n✅ Changes applied. Run validate-skills.sh to verify.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
