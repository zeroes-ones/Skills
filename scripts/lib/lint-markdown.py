#!/usr/bin/env python3
"""Markdown linter for SKILL.md and other markdown files.

Enforces consistent formatting across all markdown files in the repository.
Zero external dependencies — stdlib only.

Usage:
    python3 scripts/lib/lint-markdown.py [file ...]     # Lint specific files
    python3 scripts/lib/lint-markdown.py --all           # Lint all .md files
    python3 scripts/lib/lint-markdown.py --changed       # Lint git-changed .md files
    python3 scripts/lib/lint-markdown.py --fix           # Auto-fix where possible
"""

import os
import re
import sys
import subprocess
from collections import defaultdict

# ── Rule Registry ──────────────────────────────────────────────────────────
# Each rule: (code, severity, message_template, check_function)
# severity: 'error' (blocks commit) or 'warning' (advisory)
RULES = []

def rule(code, severity, message):
    """Decorator to register a lint rule."""
    def decorator(func):
        RULES.append((code, severity, message, func))
        return func
    return decorator


@rule("MD001", "warning", "Heading level skips: H{current} → H{next} (jumped {skip} levels)")
def check_heading_increment(filepath, lines):
    """Heading levels should only increment by one level at a time."""
    errors = []
    prev_level = 0
    for i, line in enumerate(lines, 1):
        m = re.match(r'^(#{1,6})\s', line)
        if m:
            level = len(m.group(1))
            if prev_level > 0 and level > prev_level + 1:
                errors.append((i, f"Heading level skips: H{prev_level} → H{level} (jumped {level - prev_level - 1} levels)"))
            prev_level = level
    return errors


@rule("MD009", "error", "Trailing whitespace")
def check_trailing_whitespace(filepath, lines):
    """No trailing spaces or tabs at end of lines."""
    errors = []
    for i, line in enumerate(lines, 1):
        if line.rstrip('\n') != line.rstrip(' \t\n'):
            errors.append((i, "Trailing whitespace"))
    return errors


@rule("MD012", "error", "Multiple consecutive blank lines ({count} blank lines)")
def check_consecutive_blank_lines(filepath, lines):
    """No more than 1 consecutive blank line."""
    errors = []
    blank_count = 0
    for i, line in enumerate(lines, 1):
        if line.strip() == '':
            blank_count += 1
        else:
            if blank_count > 2:  # Allow one blank separator + the actual blank
                errors.append((i - 1, f"Multiple consecutive blank lines ({blank_count} blank lines)"))
            blank_count = 0
    return errors


@rule("MD022", "warning", "Heading missing surrounding blank lines")
def check_heading_blank_lines(filepath, lines):
    """Headings should be surrounded by blank lines."""
    errors = []
    for i, line in enumerate(lines, 1):
        m = re.match(r'^#{1,6}\s', line)
        if m:
            # Check line before (if not first line)
            if i > 1 and lines[i - 2].strip() != '':
                errors.append((i, "Blank line required before heading"))
            # Check line after (if not last line)
            if i < len(lines) and lines[i].strip() != '' and not lines[i].startswith('>'):
                errors.append((i, "Blank line required after heading"))
    return errors


@rule("MD026", "warning", "Heading ends with punctuation: '{char}'")
def check_heading_punctuation(filepath, lines):
    """No trailing punctuation in headings: .,;:!?"""
    errors = []
    for i, line in enumerate(lines, 1):
        m = re.match(r'^#{1,6}\s+(.+)$', line)
        if m:
            heading = m.group(1).rstrip()
            # Allow leading punctuation (like ## "Quote") and dashed headings
            if heading and heading[-1] in '.,;:!?':
                errors.append((i, f"Heading ends with punctuation: '{heading[-1]}'"))
    return errors


@rule("MD031", "error", "Fenced code block missing surrounding blank lines")
def check_code_block_blank_lines(filepath, lines):
    """Blank lines should surround fenced code blocks."""
    errors = []
    in_block = False
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith('```') or stripped.startswith('~~~'):
            if not in_block:
                # Opening fence — check blank line before
                if i > 1 and lines[i - 2].strip() != '' and not lines[i - 2].strip().startswith('|'):
                    errors.append((i, "Blank line required before fenced code block"))
                in_block = True
            else:
                # Closing fence — check blank line after
                if i < len(lines) and lines[i].strip() != '':
                    errors.append((i, "Blank line required after fenced code block"))
                in_block = False
    return errors


@rule("MD040", "warning", "Fenced code block missing language specifier")
def check_code_block_language(filepath, lines):
    """Fenced code blocks should have a language specified."""
    errors = []
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped in ('```', '~~~'):
            errors.append((i, "Fenced code block missing language specifier"))
    return errors


@rule("MD041", "error", "First line must be a top-level heading or YAML frontmatter")
def check_first_line_heading(filepath, lines):
    """First line in file should be a top-level heading or frontmatter delimiter."""
    errors = []
    if lines and not lines[0].startswith('#') and not lines[0].startswith('---'):
        errors.append((1, "File must start with a top-level heading (# ) or YAML frontmatter (---)"))
    return errors


@rule("MD047", "error", "File must end with exactly one trailing newline")
def check_final_newline(filepath, lines):
    """Files should end with a single newline."""
    errors = []
    with open(filepath, 'rb') as f:
        content = f.read()
    if not content:
        return errors
    # Check for trailing newline(s)
    if not content.endswith(b'\n'):
        errors.append((len(lines), "File missing trailing newline"))
    elif content.endswith(b'\n\n'):
        errors.append((len(lines), "File has multiple trailing newlines"))
    return errors


@rule("MD048", "error", "Duplicate heading: '{heading}'")
def check_duplicate_headings(filepath, lines):
    """No duplicate headings within the same file."""
    errors = []
    seen = {}
    for i, line in enumerate(lines, 1):
        m = re.match(r'^#{1,6}\s+(.+?)(?:\s*\*\*\((?:QUICK|STANDARD|DEEP)\)\*\*\s*)?$', line)
        if m:
            heading = m.group(1).strip().lower()
            if heading in seen:
                errors.append((i, f"Duplicate heading: '{m.group(1).strip()}' (first seen at line {seen[heading]})"))
            else:
                seen[heading] = i
    return errors


@rule("MD049", "error", "ATX heading missing space after #: '{heading}'")
def check_heading_space(filepath, lines):
    """ATX headings must have a space after the # markers."""
    errors = []
    for i, line in enumerate(lines, 1):
        if re.match(r'^#{1,6}[^#\s]', line):
            errors.append((i, f"ATX heading missing space after #"))
    return errors


@rule("MD050", "warning", "Bare URL should use angle brackets: {url}")
def check_bare_urls(filepath, lines):
    """Bare URLs should be enclosed in angle brackets."""
    errors = []
    # Match URLs not in angle brackets, not in markdown links, not in code blocks
    for i, line in enumerate(lines, 1):
        # Skip code blocks and markdown links
        bare = re.findall(r'(?<!<)(?<!\]\()(?:https?://[^\s\)\]>]+)', line)
        for url in bare:
            # Don't flag URLs that are part of markdown links [text](url)
            if f']({url})' not in line and f'({url})' not in line:
                errors.append((i, f"Bare URL should use angle brackets: {url}"))
    return errors


@rule("MD051", "error", "Tab character used for indentation (use spaces)")
def check_no_tabs(filepath, lines):
    """No tab characters in markdown files."""
    errors = []
    for i, line in enumerate(lines, 1):
        if '\t' in line:
            errors.append((i, "Tab character used for indentation (use spaces)"))
    return errors


# ── Lint Engine ────────────────────────────────────────────────────────────

def lint_file(filepath, rules_to_run=None, fix=False):
    """Run all rules against a single file. Returns list of (line, code, severity, message)."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except (UnicodeDecodeError, IOError) as e:
        return [(0, "MD000", "error", f"Cannot read file: {e}")]

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


def get_changed_files():
    """Get list of changed .md files from git."""
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
            capture_output=True, text=True, cwd=os.getcwd()
        )
        staged = [f.strip() for f in result.stdout.split('\n') if f.strip().endswith('.md')]
        result2 = subprocess.run(
            ['git', 'diff', '--name-only', '--diff-filter=ACM'],
            capture_output=True, text=True, cwd=os.getcwd()
        )
        unstaged = [f.strip() for f in result2.stdout.split('\n') if f.strip().endswith('.md')]
        return sorted(set(staged + unstaged))
    except Exception:
        return []


def get_all_md_files(root='.'):
    """Walk repo and return all .md files."""
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip hidden dirs and node_modules
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d != 'node_modules']
        for f in filenames:
            if f.endswith('.md'):
                files.append(os.path.join(dirpath, f))
    return sorted(files)


def format_output(filepath, errors, show_code=True, color=True):
    """Format lint errors for console output."""
    if not errors:
        return None

    RED = '\033[0;31m' if color else ''
    YELLOW = '\033[1;33m' if color else ''
    GREEN = '\033[0;32m' if color else ''
    NC = '\033[0m' if color else ''

    lines = [f"{filepath}:"]
    for line_num, code, severity, msg in errors:
        marker = f"{RED}error{NC}" if severity == 'error' else f"{YELLOW}warning{NC}"
        prefix = f"  {line_num}:{line_num}  {marker}  " if show_code else f"  {line_num}:{line_num}  {marker}  "
        lines.append(f"{prefix}{code}  {msg}")
    return '\n'.join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Markdown linter for skills repo')
    parser.add_argument('files', nargs='*', help='Files to lint')
    parser.add_argument('--all', action='store_true', help='Lint all .md files')
    parser.add_argument('--changed', action='store_true', help='Lint git-changed .md files')
    parser.add_argument('--fix', action='store_true', help='Auto-fix issues where possible')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--no-color', action='store_true', help='Disable colors')
    parser.add_argument('--errors-only', action='store_true', help='Only show errors, not warnings')
    parser.add_argument('--rules', help='Comma-separated rule codes to run (default: all)')
    args = parser.parse_args()

    # Determine files to lint
    if args.all:
        target_files = get_all_md_files()
    elif args.changed:
        target_files = get_changed_files()
    elif args.files:
        target_files = args.files
    else:
        target_files = get_changed_files()
        if not target_files:
            target_files = get_all_md_files()

    if not target_files:
        print("No markdown files to lint.")
        sys.exit(0)

    rule_filter = set(args.rules.split(',')) if args.rules else None

    total_errors = 0
    total_warnings = 0
    all_results = []

    for filepath in target_files:
        if not os.path.exists(filepath):
            continue
        errors = lint_file(filepath, rule_filter, fix=args.fix)
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
                output = format_output(filepath, errors, color=not args.no_color)
                if output:
                    print(output)

    if args.json:
        import json
        print(json.dumps({
            'files_checked': len(target_files),
            'files_with_issues': len(all_results),
            'total_errors': total_errors,
            'total_warnings': total_warnings,
            'results': all_results
        }, indent=2))

    # Summary
    if not args.json:
        print()
        if total_errors == 0 and total_warnings == 0:
            print(f"\033[0;32m✓\033[0m {len(target_files)} files checked, no issues found.")
        else:
            parts = []
            if total_errors:
                parts.append(f"\033[0;31m{total_errors} error(s)\033[0m")
            if total_warnings:
                parts.append(f"\033[1;33m{total_warnings} warning(s)\033[0m")
            print(f"{len(target_files)} files checked, {', '.join(parts)}")

    sys.exit(1 if total_errors > 0 else 0)


if __name__ == '__main__':
    main()
