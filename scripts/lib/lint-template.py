#!/usr/bin/env python3
"""
Skill template compliance checker — validates SKILL.md against the full
14-section template with all structural requirements.

Runs as a fast grep-level check (<100ms per file). Used by pre-commit hook.

Usage:
    python3 scripts/lib/lint-template.py --changed   # Check git-staged SKILL.md files
    python3 scripts/lib/lint-template.py file1 file2  # Check specific files
"""

import os
import re
import sys
import subprocess

# ── 16 Required Core Sections ──────────────────────────────────────────────
REQUIRED_SECTIONS = {
    'Route the Request',
    'Ground Rules',
    "The Expert's Mindset",
    'Operating at Different Levels',
    'When to Use',
    'When NOT to Use',
    'Decision Trees',
    'Core Workflow',
    'Best Practices',
    'Error Decoder',
    'Cross-Skill Coordination',
    'Proactive Triggers',
    'What Good Looks Like',
    'Deliberate Practice',
    'References',
    'Gotchas',
    'Anti-Patterns',
    'Verification',
    'Error Recovery',
    'State Log',
    'Production Checklist',
    'Anti-Rationalization',
}

# ── Anti-Hallucination Guardrails ──────────────────────────────────────────
ANTI_HALLUCINATION_PHRASES = [
    'Admit uncertainty',
    'Flag your knowledge cutoff',
    'Never guess security',
    '[VERIFIED]',
]

# ── Checks ─────────────────────────────────────────────────────────────────

class SkillChecker:
    def __init__(self, filepath):
        self.filepath = filepath
        self.errors = []
        self.warnings = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.content = f.read()
        except Exception as e:
            self.errors.append(f"Cannot read file: {e}")
            self.content = ""

    @property
    def body(self):
        """Content after YAML frontmatter."""
        parts = re.split(r'^---\s*$', self.content, maxsplit=2, flags=re.MULTILINE)
        if len(parts) < 3:
            return ""
        return parts[2]

    @property
    def headings(self):
        """Set of all ## level headings in body (stripped of time annotations)."""
        found = set()
        for m in re.finditer(r'^## (.+)$', self.body, re.MULTILINE):
            # Strip time annotations like **(QUICK: 30s)** and **(STANDARD: 3min)**
            heading = re.sub(r'\s*\*\*\((?:QUICK|STANDARD|DEEP)(?::\s*[^)]+)?\)\*\*\s*$', '', m.group(1))
            heading = heading.strip()
            found.add(heading)
        return found

    def check_required_sections(self):
        """All 12+ required core sections must be present."""
        found = self.headings
        # Fuzzy-match Ground Rules (can have "— Read Before Anything Else" suffix)
        has_ground_rules = any(h.startswith('Ground Rules') for h in found)
        if has_ground_rules:
            found = {h for h in found if not h.startswith('Ground Rules')}
            found.add('Ground Rules')

        # Fuzzy-match Decision Trees
        has_decision_trees = any(h.startswith('Decision Trees') for h in found)
        if has_decision_trees:
            found = {h for h in found if not h.startswith('Decision Trees')}
            found.add('Decision Trees')

        # Fuzzy-match Verification
        has_verification = any('Verification' in h for h in found)
        if has_verification:
            found = {h for h in found if 'Verification' not in h}
            found.add('Verification')

        missing = REQUIRED_SECTIONS - found
        if missing:
            self.errors.append(f"Missing required sections: {', '.join(sorted(missing))}")

    def check_anti_hallucination(self):
        """Must have all 4 guardrail phrases. ## Anti-Hallucination heading checked for level correctness."""
        # Content check: all 4 phrases must be present (blocking)
        missing = [p for p in ANTI_HALLUCINATION_PHRASES if p not in self.content]
        if missing:
            self.errors.append(f"Missing anti-hallucination guardrails: {', '.join(missing)}")
        # Heading level check: if present, must be ## not ### (catches the automation-engineer bug)
        if re.search(r'^###\s+Anti-Hallucination', self.body, re.MULTILINE):
            self.errors.append("Anti-Hallucination heading must be '## Anti-Hallucination' (level-2), not '###' (level-3)")
        elif not re.search(r'^## Anti-Hallucination\s*$', self.body, re.MULTILINE):
            self.warnings.append("Missing '## Anti-Hallucination' section (ensure guardrail phrases are in a dedicated level-2 section)")

    def check_gotchas_quantified(self):
        """Must have at least 5 dollar-quantified gotchas."""
        count = len(re.findall(r'\$[\d,]+', self.content))
        if count < 5:
            self.errors.append(f"Only {count} dollar-quantified references (minimum 5 required for gotchas). Each gotcha needs a dollar cost like $500-$5,000.")

    def check_ground_rules_structure(self):
        """Ground Rules must have 'Mechanical Trigger' AND 'Violation Response' columns."""
        if 'Mechanical Trigger' not in self.content:
            self.errors.append("Ground Rules missing 'Mechanical Trigger' column")
        if 'Violation Response' not in self.content:
            self.errors.append("Ground Rules missing 'Violation Response' column")

    def check_completion_criteria(self):
        """Must have at least 8 'Complete when' statements."""
        count = len(re.findall(r'Complete when', self.body, re.IGNORECASE))
        if count < 8:
            self.errors.append(f"Only {count} completion criteria (minimum 8 'Complete when' statements required)")

    def check_decision_trees(self):
        """Must have at least 3 decision trees (### sub-headings under Decision Trees)."""
        # Find the Decision Trees section
        dt_match = re.search(r'^## Decision Trees.*?\n(.*?)(?=^## |\Z)', self.body, re.MULTILINE | re.DOTALL)
        if dt_match:
            dt_section = dt_match.group(1)
            tree_count = len(re.findall(r'^### ', dt_section, re.MULTILINE))
            if tree_count < 3:
                self.errors.append(f"Only {tree_count} decision tree(s) (minimum 3 required under ## Decision Trees)")

    def check_cross_skill_table(self):
        """Must have upstream table with at least 1 entry."""
        if '| Upstream Skill' not in self.body:
            self.errors.append("Missing Cross-Skill Coordination upstream table (| Upstream Skill | ... |)")

    def _parse_frontmatter(self):
        """Parse YAML frontmatter and return dict, or None on failure."""
        parts = re.split(r'^---\s*$', self.content, maxsplit=2, flags=re.MULTILINE)
        if len(parts) < 3:
            return None
        try:
            import yaml
            return yaml.safe_load(parts[1]) or {}
        except Exception:
            return None

    def check_description_triggers(self):
        """Description must have 'Use when', 'Handles', and 'Do NOT use'."""
        fm = self._parse_frontmatter()
        if fm is None or 'description' not in fm:
            return
        desc = str(fm['description'])
        for phrase in ['Use when', 'Handles', 'Do NOT use']:
            if phrase not in desc:
                self.errors.append(f"Description missing '{phrase}' trigger phrase")

    def check_description_length(self):
        """Description must be ≤1024 characters. Warn at ≥900 chars (safety margin)."""
        fm = self._parse_frontmatter()
        if fm is None or 'description' not in fm:
            return
        desc = str(fm['description'])
        if len(desc) > 1024:
            self.errors.append(f"Description is {len(desc)} characters (maximum 1024)")
        elif len(desc) >= 900:
            self.warnings.append(f"Description is {len(desc)} characters (approaching 1024 limit, trim to stay safe)")

    def check_name_matches_dir(self):
        """name field must match parent directory name."""
        parts = re.split(r'^---\s*$', self.content, maxsplit=2, flags=re.MULTILINE)
        if len(parts) < 3:
            return
        name_match = re.search(r'^name:\s*(\S+)', parts[1], re.MULTILINE)
        if name_match:
            name = name_match.group(1).strip()
            dirname = os.path.basename(os.path.dirname(self.filepath))
            if name != dirname:
                self.errors.append(f"name '{name}' does not match directory '{dirname}'")

    def check_portability_target(self):
        """Must declare a portability target."""
        if 'Portability target' not in self.content:
            self.errors.append("Missing portability target declaration (e.g., '> **Portability target:** Spec-level.')")

    def check_token_budget(self):
        """Body must be ≤500 lines (advisory)."""
        body_lines = self.body.count('\n') + 1
        if body_lines > 600:
            self.warnings.append(f"Body is {body_lines} lines (budget: 500, hard max: 600)")

    def check_best_practices(self):
        """Best Practices must have at least 8 numbered items."""
        bp_match = re.search(r'^## Best Practices.*?\n(.*?)(?=^## |\Z)', self.body, re.MULTILINE | re.DOTALL)
        if bp_match:
            bp_section = bp_match.group(1)
            numbered = len(re.findall(r'^\d+\.\s', bp_section, re.MULTILINE))
            if numbered < 8:
                self.warnings.append(f"Best Practices has only {numbered} numbered items (recommend 10+)")

    def check_production_checklist(self):
        """Production Checklist must have at least 10 CR items."""
        pc_match = re.search(r'^## Production Checklist.*?\n(.*?)(?=^## |\Z)', self.body, re.MULTILINE | re.DOTALL)
        if pc_match:
            pc_section = pc_match.group(1)
            cr_items = len(re.findall(r'CR\d+', pc_section))
            if cr_items < 10:
                self.warnings.append(f"Production Checklist has only {cr_items} CR items (recommend 12+)")

    def check_error_decoder_format(self):
        """Error Decoder must have a table with at least 3 columns (Symptom | Root Cause | Fix | Lesson)."""
        ed_match = re.search(r'^## Error Decoder.*?\n(.*?)(?=^## |\Z)', self.body, re.MULTILINE | re.DOTALL)
        if ed_match:
            ed_section = ed_match.group(1)
            # Count pipe-separated columns in the header row
            header_match = re.search(r'^\|(.+)\|', ed_section, re.MULTILINE)
            if header_match:
                cols = [c.strip() for c in header_match.group(1).split('|') if c.strip()]
                if len(cols) < 3:
                    self.warnings.append(f"Error Decoder table has only {len(cols)} columns (recommend 4: Symptom|Root Cause|Fix|Lesson)")
            else:
                self.warnings.append("Error Decoder section exists but no table found")

    def check_anti_patterns_content(self):
        """Anti-Patterns must have at least 5 ❌/✅ pairs."""
        ap_match = re.search(r'^## Anti-Patterns.*?\n(.*?)(?=^## |\Z)', self.body, re.MULTILINE | re.DOTALL)
        if ap_match:
            ap_section = ap_match.group(1)
            cross_count = len(re.findall(r'❌', ap_section))
            if cross_count < 3:
                self.warnings.append(f"Anti-Patterns has only {cross_count} patterns (recommend 5+)")

    def check_progressive_disclosure(self):
        """At least 3 sections must have QUICK markers."""
        quick_count = len(re.findall(r'\*\*\(QUICK', self.body))
        quick_count += len(re.findall(r'<!-- QUICK:', self.body))
        if quick_count < 3:
            self.errors.append(f"Only {quick_count} QUICK markers found (minimum 3 required for progressive disclosure)")

    def check_chain_connectivity(self):
        """Must have consumes_from and feeds_into in chain."""
        if 'consumes_from' not in self.content:
            self.errors.append("Missing 'consumes_from' in chain frontmatter (no upstream dependencies)")
        if 'feeds_into' not in self.content:
            self.errors.append("Missing 'feeds_into' in chain frontmatter (no downstream connections)")

    def check_verify_script_exists(self):
        """Must have scripts/verify-skill.sh."""
        skill_dir = os.path.dirname(self.filepath)
        verify_script = os.path.join(skill_dir, 'scripts', 'verify-skill.sh')
        if not os.path.exists(verify_script):
            self.errors.append("Missing scripts/verify-skill.sh")
        elif not os.access(verify_script, os.X_OK):
            self.errors.append("scripts/verify-skill.sh is not executable (run: chmod +x)")

    def check_references_dir(self):
        """Must have references/ directory."""
        refs_dir = os.path.join(os.path.dirname(self.filepath), 'references')
        if not os.path.isdir(refs_dir):
            self.errors.append("Missing references/ directory")

    def check_reference_links(self):
        """All references/*.md links must resolve."""
        for m in re.finditer(r'\(references/([^)]+\.md)\)', self.body):
            ref_file = os.path.join(os.path.dirname(self.filepath), 'references', m.group(1))
            if not os.path.exists(ref_file):
                self.errors.append(f"Broken reference link: references/{m.group(1)}")

    def check_no_duplicate_headings(self):
        """No duplicate ## headings."""
        seen = {}
        for m in re.finditer(r'^## (.+)$', self.body, re.MULTILINE):
            heading = re.sub(r'\s*\*\*\((?:QUICK|STANDARD|DEEP)(?::\s*[^)]+)?\)\*\*\s*$', '', m.group(1)).strip().lower()
            if heading in seen:
                self.warnings.append(f"Duplicate heading: '{m.group(1).strip()}' (first at line ~{seen[heading]})")
            else:
                # Approximate line number
                line_num = self.body[:m.start()].count('\n') + 1
                seen[heading] = line_num

    def run_all(self):
        """Run all checks against this file."""
        # Structure checks
        self.check_required_sections()
        self.check_anti_hallucination()
        self.check_gotchas_quantified()
        self.check_ground_rules_structure()
        self.check_completion_criteria()
        self.check_decision_trees()
        self.check_cross_skill_table()
        self.check_portability_target()
        self.check_chain_connectivity()
        self.check_progressive_disclosure()

        # Content checks
        self.check_description_triggers()
        self.check_description_length()
        self.check_name_matches_dir()
        self.check_no_duplicate_headings()
        self.check_reference_links()
        self.check_best_practices()
        self.check_production_checklist()
        self.check_error_decoder_format()
        self.check_anti_patterns_content()

        # File structure checks
        self.check_verify_script_exists()
        self.check_references_dir()

        # Advisory
        self.check_token_budget()

        return self.errors, self.warnings


def get_changed_skill_files():
    """Get git-staged SKILL.md files."""
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
            capture_output=True, text=True
        )
        files = [f.strip() for f in result.stdout.split('\n') if f.strip().endswith('/SKILL.md')]
        return sorted(files)
    except Exception:
        return []


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Skill template compliance checker')
    parser.add_argument('files', nargs='*', help='SKILL.md files to check')
    parser.add_argument('--changed', action='store_true', help='Check git-staged SKILL.md files')
    parser.add_argument('--no-color', action='store_true', help='Disable colors')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    if args.changed:
        target_files = get_changed_skill_files()
    elif args.files:
        target_files = [f for f in args.files if f.endswith('/SKILL.md') or os.path.basename(f) == 'SKILL.md']
    else:
        target_files = get_changed_skill_files()

    if not target_files:
        print("No SKILL.md files to check.")
        sys.exit(0)

    # Skip framework skills
    target_files = [f for f in target_files if '00-framework' not in f]

    if not target_files:
        sys.exit(0)

    RED = '\033[0;31m' if not args.no_color else ''
    YELLOW = '\033[1;33m' if not args.no_color else ''
    GREEN = '\033[0;32m' if not args.no_color else ''
    NC = '\033[0m' if not args.no_color else ''

    total_errors = 0
    total_warnings = 0

    for filepath in target_files:
        if not os.path.exists(filepath):
            continue

        checker = SkillChecker(filepath)
        errors, warnings = checker.run_all()

        if errors or warnings:
            print(f"\n{filepath}:")
            for e in errors:
                print(f"  {RED}✗{NC} {e}")
                total_errors += 1
            for w in warnings:
                print(f"  {YELLOW}⚠{NC} {w}")
                total_warnings += 1

    if total_errors == 0 and total_warnings == 0:
        print(f"{GREEN}✓{NC} {len(target_files)} skill(s) pass template compliance")
        sys.exit(0)
    else:
        parts = []
        if total_errors:
            parts.append(f"{RED}{total_errors} error(s){NC}")
        if total_warnings:
            parts.append(f"{YELLOW}{total_warnings} warning(s){NC}")
        print(f"\n{len(target_files)} skill(s) checked: {', '.join(parts)}")
        sys.exit(1 if total_errors > 0 else 0)


if __name__ == '__main__':
    main()
