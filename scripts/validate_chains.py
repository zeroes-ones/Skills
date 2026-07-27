#!/usr/bin/env python3
"""
Bidirectional Chain Validator — verifies symmetric chain references across all skills.

Every chain edge MUST be symmetric:
  - If skill-A has feeds_into: ["skill-B"]
  - Then skill-B MUST have consumes_from: ["skill-A"]

Usage:
    python3 scripts/validate_chains.py           # Check all skills
    python3 scripts/validate_chains.py --json    # JSON output for CI
    python3 scripts/validate_chains.py --fix     # Suggest fixes (advisory)
"""

import os
import re
import sys
import json
import argparse

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

SKILLS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'skills')


def find_all_skills():
    """Find all SKILL.md files, return {skill_name: filepath}."""
    skills = {}
    for root, dirs, files in os.walk(SKILLS_DIR):
        for f in files:
            if f == 'SKILL.md':
                path = os.path.join(root, f)
                name = os.path.basename(os.path.dirname(path))
                skills[name] = path
    return skills


def parse_chain(filepath):
    """Parse chain from a SKILL.md frontmatter. Returns (consumes_from, feeds_into) or (None, None)."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return [], []

    parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
    if len(parts) < 3:
        return [], []

    try:
        fm = yaml.safe_load(parts[1])
    except Exception:
        return [], []

    if not isinstance(fm, dict):
        return [], []

    chain = fm.get('chain', {})
    if not isinstance(chain, dict):
        return [], []

    consumes = chain.get('consumes_from', []) or []
    feeds = chain.get('feeds_into', []) or []

    # Normalize: ensure lists
    if isinstance(consumes, str):
        consumes = [consumes]
    if isinstance(feeds, str):
        feeds = [feeds]

    return [s.strip() for s in consumes if s], [s.strip() for s in feeds if s]


def validate_chains(skills, fix_mode=False):
    """Validate bidirectional chain symmetry."""
    # Build lookup: name -> (consumes_from, feeds_into, filepath)
    chain_map = {}
    for name, path in skills.items():
        consumes, feeds = parse_chain(path)
        chain_map[name] = (consumes, feeds, path)

    errors = []
    warnings = []
    all_skill_names = set(skills.keys())

    # Validate references point to existing skills
    for name, (consumes, feeds, path) in chain_map.items():
        for upstream in consumes:
            if upstream not in all_skill_names:
                errors.append({
                    'type': 'dangling_reference',
                    'skill': name,
                    'file': path,
                    'reference': upstream,
                    'direction': 'consumes_from',
                    'message': f"Skill '{name}' consumes_from '{upstream}' which does not exist",
                })

        for downstream in feeds:
            if downstream not in all_skill_names:
                errors.append({
                    'type': 'dangling_reference',
                    'skill': name,
                    'file': path,
                    'reference': downstream,
                    'direction': 'feeds_into',
                    'message': f"Skill '{name}' feeds_into '{downstream}' which does not exist",
                })

    # Validate bidirectional symmetry
    for name, (consumes, feeds, path) in chain_map.items():
        # Check: if A feeds_into B, then B must consume_from A
        for downstream in feeds:
            if downstream not in chain_map:
                continue  # Already caught as dangling
            down_consumes, _, down_path = chain_map[downstream]
            if name not in down_consumes:
                err = {
                    'type': 'asymmetric_chain',
                    'skill': name,
                    'file': path,
                    'target': downstream,
                    'target_file': down_path,
                    'direction': 'feeds_into',
                    'message': f"'{name}' feeds_into '{downstream}' but '{downstream}' does NOT consume_from '{name}'",
                }
                if fix_mode:
                    err['fix'] = f"Add '{name}' to consumes_from in {down_path}"
                errors.append(err)

        # Check: if A consumes_from B, then B must feed_into A
        for upstream in consumes:
            if upstream not in chain_map:
                continue  # Already caught as dangling
            _, up_feeds, up_path = chain_map[upstream]
            if name not in up_feeds:
                err = {
                    'type': 'asymmetric_chain',
                    'skill': name,
                    'file': path,
                    'target': upstream,
                    'target_file': up_path,
                    'direction': 'consumes_from',
                    'message': f"'{name}' consumes_from '{upstream}' but '{upstream}' does NOT feeds_into '{name}'",
                }
                if fix_mode:
                    err['fix'] = f"Add '{name}' to feeds_into in {up_path}"
                errors.append(err)

    # Warnings: skills with empty chains
    for name, (consumes, feeds, path) in chain_map.items():
        if '00-framework' in path:
            continue
        if not consumes and not feeds:
            warnings.append({
                'type': 'isolated_skill',
                'skill': name,
                'file': path,
                'message': f"Skill '{name}' has neither consumes_from nor feeds_into — isolated from the chain graph",
            })
        elif not consumes:
            warnings.append({
                'type': 'no_upstream',
                'skill': name,
                'file': path,
                'message': f"Skill '{name}' has no consumes_from — no upstream dependencies declared",
            })
        elif not feeds:
            warnings.append({
                'type': 'no_downstream',
                'skill': name,
                'file': path,
                'message': f"Skill '{name}' has no feeds_into — no downstream consumers declared",
            })

    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description='Bidirectional chain symmetry validator')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--fix', action='store_true', help='Suggest fixes for asymmetric chains')
    parser.add_argument('--name', type=str, help='Check only a specific skill')
    args = parser.parse_args()

    skills = find_all_skills()

    if args.name:
        if args.name not in skills:
            print(f"ERROR: Skill '{args.name}' not found", file=sys.stderr)
            sys.exit(1)
        skills = {args.name: skills[args.name]}

    errors, warnings = validate_chains(skills, fix_mode=args.fix)

    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    GREEN = '\033[0;32m'
    NC = '\033[0m'

    if args.json:
        output = {
            'skills_checked': len(skills),
            'errors': len(errors),
            'warnings': len(warnings),
            'error_details': errors,
            'warning_details': warnings,
        }
        print(json.dumps(output, indent=2))
    else:
        print(f"=== Chain Symmetry Validator ===")
        print(f"Skills checked: {len(skills)}")
        print()

        if errors:
            print(f"{RED}ERRORS ({len(errors)}):{NC}")
            # Group by type
            asymmetric = [e for e in errors if e['type'] == 'asymmetric_chain']
            dangling = [e for e in errors if e['type'] == 'dangling_reference']

            if asymmetric:
                print(f"\n  {RED}Asymmetric chains ({len(asymmetric)}):{NC}")
                for e in asymmetric:
                    print(f"    ✗ {e['message']}")
                    if 'fix' in e:
                        print(f"      Fix: {e['fix']}")

            if dangling:
                print(f"\n  {RED}Dangling references ({len(dangling)}):{NC}")
                for e in dangling:
                    print(f"    ✗ {e['message']}")

        if warnings:
            print(f"\n{YELLOW}WARNINGS ({len(warnings)}):{NC}")
            for w in warnings:
                print(f"  ⚠ {w['message']}")

        if not errors and not warnings:
            print(f"{GREEN}✓ All chain references are symmetric. No dangling references.{NC}")

        print()
        if errors:
            print(f"{RED}Chain validation FAILED: {len(errors)} error(s){NC}")
        else:
            print(f"{GREEN}Chain validation PASSED{NC}")

    sys.exit(1 if errors else 0)


if __name__ == '__main__':
    main()
