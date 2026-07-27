#!/usr/bin/env python3
"""YAML frontmatter linter for SKILL.md files.

Validates that every SKILL.md has valid, complete, well-formatted YAML frontmatter.
Zero external dependencies beyond pyyaml (stdlib fallback for basic checks).

Usage:
    python3 scripts/lib/lint-yaml.py [file ...]       # Lint specific SKILL.md files
    python3 scripts/lib/lint-yaml.py --all             # Lint all SKILL.md files
    python3 scripts/lib/lint-yaml.py --changed         # Lint git-changed SKILL.md files
"""

import os
import re
import sys
import subprocess

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


# ── Rule Registry ──────────────────────────────────────────────────────────
RULES = []

def rule(code, severity, message):
    def decorator(func):
        RULES.append((code, severity, message, func))
        return func
    return decorator


@rule("YML001", "error", "Missing YAML frontmatter delimiters (---)")
def check_frontmatter_exists(filepath, lines):
    """File must have YAML frontmatter enclosed in ---."""
    errors = []
    content = ''.join(lines)
    parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
    if len(parts) < 3:
        errors.append((1, "Missing YAML frontmatter delimiters (---)"))
    return errors


@rule("YML002", "error", "YAML parse error")
def check_yaml_valid(filepath, lines):
    """Frontmatter must be valid YAML."""
    errors = []
    content = ''.join(lines)
    parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
    if len(parts) < 3:
        return errors
    try:
        yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        # Find approximate line number
        line_num = 1 + parts[0].count('\n')
        errors.append((line_num, f"YAML parse error: {str(e).split(chr(10))[0]}"))
    except Exception as e:
        line_num = 1 + parts[0].count('\n')
        errors.append((line_num, f"YAML parse error: {e}"))
    return errors


@rule("YML003", "error", "Missing required field: '{field}'")
def check_required_fields(filepath, lines):
    """Required fields must be present in frontmatter."""
    REQUIRED = {'name', 'description', 'license'}
    errors = []
    content = ''.join(lines)
    parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
    if len(parts) < 3:
        return errors
    try:
        fm = yaml.safe_load(parts[1])
        if not isinstance(fm, dict):
            return [(1, "Frontmatter must be a YAML mapping")]
        for field in REQUIRED:
            if field not in fm:
                errors.append((1, f"Missing required field: '{field}'"))
    except Exception:
        pass
    return errors


@rule("YML004", "error", "Description exceeds 1024 characters ({length} chars)")
def check_description_length(filepath, lines):
    """description field must be ≤1024 characters."""
    errors = []
    content = ''.join(lines)
    parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
    if len(parts) < 3:
        return errors
    try:
        fm = yaml.safe_load(parts[1])
        if isinstance(fm, dict) and 'description' in fm:
            desc = fm['description']
            if desc and len(str(desc)) > 1024:
                errors.append((1, f"Description exceeds 1024 characters ({len(str(desc))} chars)"))
    except Exception:
        pass
    return errors


@rule("YML010", "warning", "Description is {length} chars (approaching 1024 limit — trim to stay safe)")
def check_description_length_warning(filepath, lines):
    """Warn when description is ≥900 characters (approaching the 1024 limit)."""
    errors = []
    content = ''.join(lines)
    parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
    if len(parts) < 3:
        return errors
    try:
        fm = yaml.safe_load(parts[1])
        if isinstance(fm, dict) and 'description' in fm:
            desc = fm['description']
            if desc and len(str(desc)) >= 900 and len(str(desc)) <= 1024:
                errors.append((1, f"Description is {len(str(desc))} chars (approaching 1024 limit — trim to stay safe)"))
    except Exception:
        pass
    return errors


@rule("YML005", "error", "name '{name}' does not match directory '{dirname}'")
def check_name_matches_directory(filepath, lines):
    """The name field should match the parent directory name."""
    errors = []
    content = ''.join(lines)
    parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
    if len(parts) < 3:
        return errors
    try:
        fm = yaml.safe_load(parts[1])
        if isinstance(fm, dict) and 'name' in fm:
            dirname = os.path.basename(os.path.dirname(filepath))
            if fm['name'] != dirname:
                errors.append((1, f"name '{fm['name']}' does not match directory '{dirname}'"))
    except Exception:
        pass
    return errors


@rule("YML006", "warning", "Missing recommended field: '{field}'")
def check_recommended_fields(filepath, lines):
    """Recommended fields should be present."""
    RECOMMENDED = {'author', 'type', 'status', 'version', 'tags', 'chain'}
    errors = []
    content = ''.join(lines)
    parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
    if len(parts) < 3:
        return errors
    try:
        fm = yaml.safe_load(parts[1])
        if isinstance(fm, dict):
            for field in RECOMMENDED:
                if field not in fm:
                    errors.append((1, f"Missing recommended field: '{field}'"))
    except Exception:
        pass
    return errors


@rule("YML007", "warning", "Description should use 'Use when... Handles... Do NOT use for...' format")
def check_description_format(filepath, lines):
    """Description must follow the trigger-capability-boundary format."""
    errors = []
    content = ''.join(lines)
    parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
    if len(parts) < 3:
        return errors
    try:
        fm = yaml.safe_load(parts[1])
        if isinstance(fm, dict) and 'description' in fm:
            desc = str(fm['description'])
            missing = []
            if 'Use when' not in desc:
                missing.append('Use when')
            if 'Handles' not in desc:
                missing.append('Handles')
            if 'Do NOT use' not in desc:
                missing.append('Do NOT use')
            if missing:
                errors.append((1, f"Description missing trigger phrases: {', '.join(missing)}"))
    except Exception:
        pass
    return errors


@rule("YML008", "error", "chain.consumes_from references non-existent skill: '{skill}'")
def check_chain_references_valid(filepath, lines):
    """Chain references must point to existing skill directories."""
    errors = []
    content = ''.join(lines)
    parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
    if len(parts) < 3:
        return errors
    try:
        fm = yaml.safe_load(parts[1])
        if isinstance(fm, dict) and 'chain' in fm:
            chain = fm['chain']
            skills_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(filepath))), 'skills')
            # If we're inside skills/, go up to the skills root
            if 'skills/' in filepath:
                parts_path = filepath.split('skills/')
                if len(parts_path) >= 2:
                    skills_dir = os.path.join(parts_path[0], 'skills')

            for direction in ['consumes_from', 'feeds_into']:
                for skill_name in chain.get(direction, []):
                    if isinstance(skill_name, str):
                        # Check if a directory with that skill name exists
                        found = False
                        for root, dirs, files in os.walk(skills_dir):
                            if os.path.basename(root) == skill_name and 'SKILL.md' in files:
                                found = True
                                break
                        if not found:
                            errors.append((1, f"chain.{direction} references non-existent skill: '{skill_name}'"))
    except Exception:
        pass
    return errors


@rule("YML009", "warning", "Frontmatter key ordering non-standard: expected keys {expected}")
def check_key_ordering(filepath, lines):
    """Frontmatter keys should follow the standard ordering convention."""
    STANDARD_ORDER = ['name', 'description', 'license', 'author', 'type', 'status',
                       'version', 'updated', 'tags', 'token_budget', 'chain',
                       'allowed-tools', 'portability']
    errors = []
    content = ''.join(lines)
    parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
    if len(parts) < 3:
        return errors

    # Extract keys in order from raw YAML text (not parsed dict — order matters)
    yaml_text = parts[1]
    key_order = []
    for line in yaml_text.split('\n'):
        m = re.match(r'^(\w[\w-]*)\s*:', line)
        if m and not line.startswith(' ') and not line.startswith('\t'):
            key_order.append(m.group(1))

    # Check if keys follow standard order (allow missing keys)
    ordered_keys = [k for k in STANDARD_ORDER if k in key_order]
    actual_indexed = [(k, key_order.index(k)) for k in ordered_keys]
    if actual_indexed != sorted(actual_indexed, key=lambda x: x[1]):
        # Find what's out of order
        expected_in_order = [k for k in STANDARD_ORDER if k in key_order]
        if key_order != expected_in_order:
            errors.append((1, f"Frontmatter key ordering non-standard. Expected: {expected_in_order[:8]}..."))
    return errors


@rule("YML010", "error", "YAML uses tabs for indentation (use spaces)")
def check_yaml_indentation(filepath, lines):
    """YAML frontmatter must use spaces, not tabs."""
    errors = []
    content = ''.join(lines)
    parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
    if len(parts) < 3:
        return errors
    yaml_text = parts[1]
    for i, line in enumerate(yaml_text.split('\n'), 1):
        if line.startswith('\t'):
            errors.append((i + 1, "YAML uses tabs for indentation (use spaces)"))
            break
    return errors


# ── Lint Engine ────────────────────────────────────────────────────────────

def lint_file(filepath, rules_to_run=None):
    """Run all YAML rules against a single SKILL.md file."""
    if not os.path.basename(filepath) == 'SKILL.md':
        return []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except (UnicodeDecodeError, IOError) as e:
        return [(0, "YML000", "error", f"Cannot read file: {e}")]

    all_errors = []
    for code, severity, template, check_fn in RULES:
        if rules_to_run and code not in rules_to_run:
            continue
        try:
            for line_num, msg in check_fn(filepath, lines):
                all_errors.append((line_num, code, severity, msg))
        except Exception as e:
            all_errors.append((0, code, "error", f"Rule {code} crashed: {e}"))

    return sorted(all_errors, key=lambda x: (x[0], x[1]))


def get_all_skill_files(root='skills'):
    """Find all SKILL.md files."""
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        for f in filenames:
            if f == 'SKILL.md':
                files.append(os.path.join(dirpath, f))
    return sorted(files)


def get_changed_skill_files():
    """Get git-changed SKILL.md files."""
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
            capture_output=True, text=True
        )
        staged = [f.strip() for f in result.stdout.split('\n') if f.strip().endswith('/SKILL.md')]
        result2 = subprocess.run(
            ['git', 'diff', '--name-only', '--diff-filter=ACM'],
            capture_output=True, text=True
        )
        unstaged = [f.strip() for f in result2.stdout.split('\n') if f.strip().endswith('/SKILL.md')]
        return sorted(set(staged + unstaged))
    except Exception:
        return []


def main():
    import argparse
    parser = argparse.ArgumentParser(description='YAML frontmatter linter for SKILL.md files')
    parser.add_argument('files', nargs='*', help='SKILL.md files to lint')
    parser.add_argument('--all', action='store_true', help='Lint all SKILL.md files')
    parser.add_argument('--changed', action='store_true', help='Lint git-changed SKILL.md files')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--no-color', action='store_true', help='Disable colors')
    parser.add_argument('--errors-only', action='store_true', help='Only show errors')
    parser.add_argument('--rules', help='Comma-separated rule codes')
    args = parser.parse_args()

    if args.all:
        target_files = get_all_skill_files()
    elif args.changed:
        target_files = get_changed_skill_files()
    elif args.files:
        target_files = [f for f in args.files if os.path.basename(f) == 'SKILL.md']
    else:
        target_files = get_changed_skill_files()
        if not target_files:
            target_files = get_all_skill_files()

    if not target_files:
        print("No SKILL.md files to lint.")
        sys.exit(0)

    rule_filter = set(args.rules.split(',')) if args.rules else None

    total_errors = 0
    total_warnings = 0
    all_results = []

    RED = '\033[0;31m' if not args.no_color else ''
    YELLOW = '\033[1;33m' if not args.no_color else ''
    GREEN = '\033[0;32m' if not args.no_color else ''
    NC = '\033[0m' if not args.no_color else ''

    for filepath in target_files:
        if not os.path.exists(filepath):
            continue
        errors = lint_file(filepath, rule_filter)
        if args.errors_only:
            errors = [e for e in errors if e[2] == 'error']

        if errors:
            error_count = sum(1 for e in errors if e[2] == 'error')
            warn_count = sum(1 for e in errors if e[2] == 'warning')
            total_errors += error_count
            total_warnings += warn_count

            if args.json:
                all_results.append({
                    'file': filepath,
                    'errors': error_count,
                    'warnings': warn_count,
                    'issues': [{'line': e[0], 'code': e[1], 'severity': e[2], 'message': e[3]} for e in errors]
                })
            else:
                print(f"{filepath}:")
                for line_num, code, severity, msg in errors:
                    marker = f"{RED}error{NC}" if severity == 'error' else f"{YELLOW}warning{NC}"
                    print(f"  {line_num}:{line_num}  {marker}  {code}  {msg}")

    if args.json:
        import json
        print(json.dumps({
            'files_checked': len(target_files),
            'files_with_issues': len(all_results),
            'total_errors': total_errors,
            'total_warnings': total_warnings,
            'results': all_results
        }, indent=2))

    if not args.json:
        print()
        if total_errors == 0 and total_warnings == 0:
            print(f"{GREEN}✓{NC} {len(target_files)} SKILL.md files checked, no issues found.")
        else:
            parts = []
            if total_errors:
                parts.append(f"{RED}{total_errors} error(s){NC}")
            if total_warnings:
                parts.append(f"{YELLOW}{total_warnings} warning(s){NC}")
            print(f"{len(target_files)} files checked, {', '.join(parts)}")

    sys.exit(1 if total_errors > 0 else 0)


if __name__ == '__main__':
    main()
