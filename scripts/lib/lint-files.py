#!/usr/bin/env python3
"""File format linter — validates encoding, line endings, and whitespace.

Checks all text files in the repository for consistent formatting:
- UTF-8 encoding
- LF line endings (no CRLF)
- No trailing whitespace
- Files end with exactly one newline
- No tab indentation in whitespace-significant files

Usage:
    python3 scripts/lib/lint-files.py [file ...]       # Lint specific files
    python3 scripts/lib/lint-files.py --all             # Lint all text files
    python3 scripts/lib/lint-files.py --changed         # Lint git-changed text files
    python3 scripts/lib/lint-files.py --fix             # Auto-fix line endings and whitespace
"""

import os
import re
import sys
import subprocess

# File extensions that should use spaces (not tabs)
SPACE_INDENTED = {'.md', '.py', '.sh', '.yaml', '.yml', '.json', '.js', '.ts', '.css', '.html'}

RULES = []

def rule(code, severity, message):
    def decorator(func):
        RULES.append((code, severity, message, func))
        return func
    return decorator


@rule("FMT001", "error", "File is not valid UTF-8")
def check_utf8_encoding(filepath, lines):
    """File must be valid UTF-8 encoded."""
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
        content.decode('utf-8')
    except UnicodeDecodeError as e:
        return [(0, f"Not valid UTF-8: {e}")]
    return []


@rule("FMT002", "error", "File has CRLF line endings (use LF)")
def check_crlf(filepath, lines):
    """All text files must use LF line endings."""
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
        if b'\r\n' in content:
            # Find first occurrence
            pos = content.index(b'\r\n')
            line_num = content[:pos].count(b'\n') + 1
            return [(line_num, "File has CRLF line endings (use LF)")]
    except Exception:
        pass
    return []


@rule("FMT003", "error", "Trailing whitespace on {count} line(s)")
def check_trailing_whitespace(filepath, lines):
    """No trailing spaces or tabs at end of lines."""
    errors = []
    trailing_count = 0
    first_line = None
    for i, line in enumerate(lines):
        if line.endswith(' \n') or line.endswith('\t\n'):
            trailing_count += 1
            if first_line is None:
                first_line = i + 1
    if trailing_count > 0:
        errors.append((first_line, f"Trailing whitespace on {trailing_count} line(s)"))
    return errors


@rule("FMT004", "error", "File does not end with a newline")
def check_final_newline_exists(filepath, lines):
    """File must end with exactly one newline."""
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
    except Exception:
        return []

    if not content:
        return []
    if not content.endswith(b'\n'):
        return [(len(lines), "File does not end with a newline")]
    if content.endswith(b'\n\n'):
        return [(len(lines), "File ends with multiple newlines")]
    return []


@rule("FMT005", "error", "Tab indentation in space-indented file ({ext} files use spaces)")
def check_tab_indentation(filepath, lines):
    """Files with certain extensions must use spaces, not tabs."""
    ext = os.path.splitext(filepath)[1].lower()
    if ext not in SPACE_INDENTED:
        return []
    for i, line in enumerate(lines, 1):
        if line.startswith('\t'):
            return [(i, f"Tab indentation in space-indented file ({ext} files use spaces)")]
    return []


@rule("FMT006", "error", "File is empty (0 bytes)")
def check_empty_file(filepath, lines):
    """Empty files should not exist in the repo."""
    try:
        if os.path.getsize(filepath) == 0:
            return [(0, "File is empty (0 bytes)")]
    except Exception:
        pass
    return []


@rule("FMT007", "warning", "File has mixed indentation (both spaces and tabs)")
def check_mixed_indentation(filepath, lines):
    """Mixed indentation makes diffs unpredictable."""
    has_tabs = False
    has_spaces = False
    for line in lines:
        if line.startswith('\t'):
            has_tabs = True
        elif line.startswith('  '):
            has_spaces = True
        if has_tabs and has_spaces:
            return [(1, "Mixed indentation (both spaces and tabs)")]
    return []


def fix_file(filepath):
    """Auto-fix common formatting issues: CRLF→LF, trailing whitespace, final newline."""
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
    except Exception:
        return False, "Cannot read file"

    original = content

    # Fix 1: CRLF → LF
    content = content.replace(b'\r\n', b'\n')
    content = content.replace(b'\r', b'\n')

    # Fix 2: Strip trailing whitespace per line
    lines = content.split(b'\n')
    fixed_lines = []
    for line in lines:
        fixed_lines.append(line.rstrip(b' \t'))
    content = b'\n'.join(fixed_lines)

    # Fix 3: Ensure exactly one trailing newline
    content = content.rstrip(b'\n') + b'\n'

    if content == original:
        return False, "No fixes needed"

    try:
        with open(filepath, 'wb') as f:
            f.write(content)
        return True, "Fixed CRLF, trailing whitespace, final newline"
    except Exception as e:
        return False, f"Cannot write file: {e}"


def lint_file(filepath, rules_to_run=None):
    """Run all format rules against a single file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        lines = []
    except IOError as e:
        return [(0, "FMT000", "error", f"Cannot read file: {e}")]

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


def get_changed_text_files():
    """Get git-changed text files."""
    TEXT_EXTS = {'.md', '.py', '.sh', '.yaml', '.yml', '.json', '.js', '.ts', '.css', '.html',
                 '.txt', '.cfg', '.ini', '.toml', '.xml', '.svg', '.gitignore', '.env.example'}
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
            capture_output=True, text=True
        )
        staged = [f.strip() for f in result.stdout.split('\n')
                  if any(f.strip().endswith(ext) for ext in TEXT_EXTS)]
        result2 = subprocess.run(
            ['git', 'diff', '--name-only', '--diff-filter=ACM'],
            capture_output=True, text=True
        )
        unstaged = [f.strip() for f in result2.stdout.split('\n')
                    if any(f.strip().endswith(ext) for ext in TEXT_EXTS)]
        return sorted(set(staged + unstaged))
    except Exception:
        return []


def get_all_text_files(root='.'):
    """Walk repo and return text files."""
    TEXT_EXTS = {'.md', '.py', '.sh', '.yaml', '.yml', '.json', '.js', '.ts', '.css', '.html',
                 '.txt', '.cfg', '.ini', '.toml', '.xml', '.svg'}
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames
                       if not d.startswith('.') and d != 'node_modules' and d != '__pycache__']
        for f in filenames:
            if os.path.splitext(f)[1].lower() in TEXT_EXTS:
                files.append(os.path.join(dirpath, f))
    return sorted(files)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='File format linter')
    parser.add_argument('files', nargs='*', help='Files to lint')
    parser.add_argument('--all', action='store_true', help='Lint all text files')
    parser.add_argument('--changed', action='store_true', help='Lint git-changed text files')
    parser.add_argument('--fix', action='store_true', help='Auto-fix formatting issues')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--no-color', action='store_true', help='Disable colors')
    parser.add_argument('--errors-only', action='store_true', help='Only show errors')
    parser.add_argument('--rules', help='Comma-separated rule codes')
    args = parser.parse_args()

    if args.all:
        target_files = get_all_text_files()
    elif args.changed:
        target_files = get_changed_text_files()
    elif args.files:
        target_files = args.files
    else:
        target_files = get_changed_text_files()
        if not target_files:
            target_files = get_all_text_files()

    if not target_files:
        print("No text files to lint.")
        sys.exit(0)

    # If --fix, apply fixes to all files
    if args.fix:
        fixed_count = 0
        for filepath in target_files:
            if not os.path.exists(filepath):
                continue
            fixed, msg = fix_file(filepath)
            if fixed:
                print(f"  Fixed: {filepath} — {msg}")
                fixed_count += 1
        print(f"\n✓ Fixed {fixed_count} file(s)")
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
            print(f"{GREEN}✓{NC} {len(target_files)} files checked, no formatting issues.")
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
