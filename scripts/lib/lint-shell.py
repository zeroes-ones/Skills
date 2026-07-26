#!/usr/bin/env python3
"""Shell script linter for .sh files in the repository.

Enforces shell scripting best practices without requiring shellcheck.
Zero external dependencies — stdlib only.

Usage:
    python3 scripts/lib/lint-shell.py [file ...]        # Lint specific .sh files
    python3 scripts/lib/lint-shell.py --all              # Lint all .sh files
    python3 scripts/lib/lint-shell.py --changed          # Lint git-changed .sh files
"""

import os
import re
import sys
import subprocess

RULES = []

def rule(code, severity, message):
    def decorator(func):
        RULES.append((code, severity, message, func))
        return func
    return decorator


@rule("SHL001", "error", "Missing shebang (#!/usr/bin/env bash)")
def check_shebang(filepath, lines):
    """Executable .sh files must start with a shebang."""
    # Only check files with .sh extension or in scripts/ directories
    if not (filepath.endswith('.sh') or '/scripts/' in filepath):
        return []
    if not lines or not lines[0].startswith('#!'):
        return [(1, "Missing shebang (#!/usr/bin/env bash)")]
    # Check for common patterns
    if '#!/usr/bin/env bash' not in lines[0] and '#!/bin/bash' not in lines[0] and '#!/bin/sh' not in lines[0]:
        return [(1, f"Non-standard shebang: {lines[0].rstrip()} (use #!/usr/bin/env bash)")]
    return []


@rule("SHL002", "error", "Missing 'set -euo pipefail'")
def check_strict_mode(filepath, lines):
    """Shell scripts should use strict error handling."""
    if not filepath.endswith('.sh'):
        return []
    # Check for set -e or set -euo pipefail in first 20 non-comment lines
    found_e = False
    found_u = False
    found_pipefail = False
    for i, line in enumerate(lines[:20], 1):
        stripped = line.strip()
        if stripped.startswith('#'):
            continue
        if 'set -e' in stripped:
            found_e = True
        if 'set -u' in stripped:
            found_u = True
        if 'pipefail' in stripped:
            found_pipefail = True
        if 'set -euo pipefail' in stripped:
            return []

    missing = []
    if not found_e:
        missing.append('-e')
    if not found_u:
        missing.append('-u')
    if not found_pipefail:
        missing.append('-o pipefail')
    if missing:
        return [(3, f"Missing 'set {' '.join(missing)}' — use 'set -euo pipefail'")]
    return []


@rule("SHL003", "warning", "Unquoted variable expansion: {var}")
def check_unquoted_variables(filepath, lines):
    """Flag potentially unquoted variable expansions."""
    errors = []
    # Simple heuristic: $VAR not inside double quotes on the same line
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith('#'):
            continue
        if 'echo' in stripped:
            continue
        # Find ${VAR} or $VAR not inside double quotes
        # This is a simplified check — shellcheck does this properly
        matches = re.findall(r'(?<!")\$(\{?[A-Za-z_][A-Za-z0-9_]*\}?)', stripped)
        # Filter out things in echo or comments
        if matches and 'echo' not in stripped:
            pass  # Too many false positives without proper parsing
    return errors


def _get_non_shell_lines(lines):
    """Identify line numbers that are inside non-shell contexts (Python/awk/heredocs).

    Returns a set of 1-indexed line numbers that should be skipped by
    shell-specific checks like SHL004 (assignment spacing).

    Tracks:
      - awk scripts: awk '...' (multi-line, may start mid-line after |)
      - python -c heredocs: python3 -c "..." spanning multiple lines
      - Heredoc blocks: <<DELIM ... DELIM
    """
    skip_lines = set()
    in_awk = False
    awk_quote = None  # ' or "
    in_python_c = False
    in_heredoc = False
    heredoc_delim = None

    for i, line in enumerate(lines, 1):
        # ── Already inside a non-shell context ──
        if in_awk:
            skip_lines.add(i)
            # Awk closes on a line that is just the closing quote (optionally
            # followed by pipe/redirect)
            if re.match(r"^\s*" + re.escape(awk_quote) + r"\s*(\||;|\).*)?$", line):
                in_awk = False
                awk_quote = None
            continue

        if in_python_c:
            skip_lines.add(i)
            # Python -c closes when we hit the matching quote at end of line
            stripped = line.rstrip()
            if re.search(r'"\s*(?:[|;]|\).*)?$', stripped) and not re.search(r'python3?\s+-c', line):
                in_python_c = False
            continue

        if in_heredoc:
            skip_lines.add(i)
            if heredoc_delim and line.strip() == heredoc_delim:
                in_heredoc = False
                heredoc_delim = None
            continue

        # ── Detect entry into non-shell contexts ──
        stripped = line.strip()

        # Awk: can start at line beginning or mid-line after | awk
        awk_start_single = re.search(r'\bawk\s+(?:-[a-zA-Z]+\s+\S+\s+)*\'', stripped)
        awk_start_double = re.search(r'\bawk\s+(?:-[a-zA-Z]+\s+\S+\s+)*"', stripped)
        awk_match = awk_start_single or awk_start_double

        if awk_match:
            awk_quote = "'" if awk_start_single else '"'
            # Check if this is a single-line awk (quote closes on same line)
            quote_pos = awk_match.end()
            rest = stripped[quote_pos-1:]  # from the opening quote onward
            # Single-line: if opening quote closes later on the same line
            # (awk body with matching close-quote, then optional pipe/redirect)
            if re.search(re.escape(awk_quote) + r'\s*(?:\||;|\).*)?$', rest[1:]):
                in_awk = False  # single-line, don't skip
            else:
                in_awk = True
                skip_lines.add(i)
            continue

        # Python -c: heredoc-style multi-line string
        if re.search(r'python3?\s+-c\s+"', stripped) or re.search(r"python3?\s+-c\s+'", stripped):
            # Check if single-line
            if (re.search(r'python3?\s+-c\s+"[^"]*"\s*$', stripped) or
                re.search(r"python3?\s+-c\s+'[^']*'\s*$", stripped)):
                continue  # single-line, don't skip
            in_python_c = True
            skip_lines.add(i)
            continue

        # Heredoc: <<DELIM (e.g., <<'EOF')
        hd_match = re.match(r".*<<-?\s*'?(\w+)'?\s*$", stripped)
        if hd_match:
            in_heredoc = True
            heredoc_delim = hd_match.group(1)
            continue

    return skip_lines

@rule("SHL004", "error", "Variable assignment has spaces around '=': '{line}'")
def check_assignment_spaces(filepath, lines):
    """Variable assignment should not have spaces around =."""
    skip_lines = _get_non_shell_lines(lines)
    errors = []
    for i, line in enumerate(lines, 1):
        if i in skip_lines:
            continue
        stripped = line.strip()
        if stripped.startswith('#'):
            continue
        # Look for ' = ' pattern in variable-like assignments (but not in test conditions)
        if re.match(r'^[A-Za-z_][A-Za-z0-9_]*\s*=\s', stripped) and ' = ' in stripped:
            if not stripped.startswith('[ ') and not stripped.startswith('[['):
                errors.append((i, f"Variable assignment has spaces around '='"))
        # Also catch 'export VAR = value'
        if re.match(r'^(export|local|readonly)\s+\w+\s*=\s', stripped) and ' = ' in stripped:
            errors.append((i, f"Variable assignment has spaces around '='"))
    return errors


@rule("SHL005", "warning", "Use [[ ]] instead of [ ] for test conditions")
def check_test_brackets(filepath, lines):
    """Prefer [[ ]] over [ ] for bash scripts."""
    errors = []
    if '#!/bin/sh' in lines[0] if lines else '':
        return []  # sh doesn't support [[ ]]

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith('#'):
            continue
        if re.match(r'^(if|elif|while)\s+\[', stripped):
            errors.append((i, "Use [[ ]] instead of [ ] for test conditions"))
        if re.match(r'^\[\[?\s', stripped) and stripped.startswith('[') and not stripped.startswith('[['):
            errors.append((i, "Use [[ ]] instead of [ ] for test conditions"))
    return errors


@rule("SHL006", "warning", "Backticks used for command substitution (use $())")
def check_backtick_substitution(filepath, lines):
    """Use $(command) instead of `command`."""
    skip_lines = _get_non_shell_lines(lines)
    errors = []
    for i, line in enumerate(lines, 1):
        if i in skip_lines:
            continue
        stripped = line.strip()
        if stripped.startswith('#'):
            continue
        if '`' in stripped and not stripped.strip().startswith('```'):
            # Skip sed commands where backticks are literal replacement chars
            if re.match(r'^\s*sed\b', stripped) or 'sed ' in stripped:
                continue
            # Check if it's a command substitution (heuristic: `something` with executable-like content)
            backtick_regions = re.findall(r'`([^`]+)`', stripped)
            for region in backtick_regions:
                if any(kw in region for kw in ['$', '\\', '|', 'grep', 'sed', 'awk', 'find', 'basename', 'dirname', '|', ';']):
                    errors.append((i, f"Backticks used for command substitution (use $())"))
                    break
    return errors


@rule("SHL007", "warning", "echo used without -e or -n flag — consider printf for portability")
def check_echo_vs_printf(filepath, lines):
    """Recommend printf for complex output."""
    errors = []
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith('#'):
            continue
        if stripped.startswith('echo ') and ('\\n' in stripped or '\\t' in stripped or '\\033' in stripped):
            errors.append((i, "echo with escape sequences — consider printf for portability"))
    return errors


@rule("SHL008", "error", "Trap missing for cleanup on temp files or background processes")
def check_trap_cleanup(filepath, lines):
    """Scripts that create temp files should have a trap for cleanup."""
    errors = []
    has_mktemp = any('mktemp' in line for line in lines)
    has_trap = any('trap' in line for line in lines)
    if has_mktemp and not has_trap:
        errors.append((1, "Script uses mktemp but has no trap for cleanup"))
    return errors


@rule("SHL009", "error", "Tab character used for indentation (use spaces)")
def check_tabs(filepath, lines):
    """Shell scripts should use spaces, not tabs."""
    errors = []
    for i, line in enumerate(lines, 1):
        if line.startswith('\t') and not line.strip().startswith('#'):
            errors.append((i, "Tab character used for indentation (use spaces)"))
            break  # One error per file is enough
    return errors


@rule("SHL010", "error", "read without -r flag (backslash interpretation risk)")
def check_read_without_r(filepath, lines):
    """Use read -r to prevent backslash interpretation."""
    errors = []
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith('#') or not stripped.startswith('read '):
            continue
        if re.match(r'^read\s+(?!.*-r\b)', stripped):
            errors.append((i, "read without -r flag (use 'read -r' to prevent backslash interpretation)"))
    return errors


def lint_file(filepath, rules_to_run=None):
    """Run all shell rules against a single file."""
    if not filepath.endswith('.sh'):
        return []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except (UnicodeDecodeError, IOError) as e:
        return [(0, "SHL000", "error", f"Cannot read file: {e}")]

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


def get_changed_sh_files():
    """Get git-changed .sh files."""
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
            capture_output=True, text=True
        )
        staged = [f.strip() for f in result.stdout.split('\n') if f.strip().endswith('.sh')]
        result2 = subprocess.run(
            ['git', 'diff', '--name-only', '--diff-filter=ACM'],
            capture_output=True, text=True
        )
        unstaged = [f.strip() for f in result2.stdout.split('\n') if f.strip().endswith('.sh')]
        return sorted(set(staged + unstaged))
    except Exception:
        return []


def get_all_sh_files(root='.'):
    """Walk repo and return all .sh files."""
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d != 'node_modules']
        for f in filenames:
            if f.endswith('.sh'):
                files.append(os.path.join(dirpath, f))
    return sorted(files)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Shell script linter')
    parser.add_argument('files', nargs='*', help='.sh files to lint')
    parser.add_argument('--all', action='store_true', help='Lint all .sh files')
    parser.add_argument('--changed', action='store_true', help='Lint git-changed .sh files')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--no-color', action='store_true', help='Disable colors')
    parser.add_argument('--errors-only', action='store_true', help='Only show errors')
    parser.add_argument('--rules', help='Comma-separated rule codes')
    args = parser.parse_args()

    if args.all:
        target_files = get_all_sh_files()
    elif args.changed:
        target_files = get_changed_sh_files()
    elif args.files:
        target_files = [f for f in args.files if f.endswith('.sh')]
    else:
        target_files = get_changed_sh_files()
        if not target_files:
            target_files = get_all_sh_files()

    if not target_files:
        print("No .sh files to lint.")
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
            print(f"{GREEN}✓{NC} {len(target_files)} files checked, no issues found.")
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
