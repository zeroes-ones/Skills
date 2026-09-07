#!/usr/bin/env python3
"""
lint-workflow.py — lint the optional `workflow:` frontmatter block of a SKILL.md (stdlib only).

Implements the L0 node contract (WORKFLOW-SYSTEM.md Section 1):

    workflow:
      artifacts:
        inputs:  [name, ...]       # optional list of strings
        outputs: [name, ...]       # optional list of strings
      completion:
        criteria: ["...", ...]     # optional list of strings (default: skill Verification section)
        evidence: required|optional
      iteration:
        max: 3                     # optional int >= 1 (default 1)
        on_exhaustion: escalate|next|fail
      escalate_to: [target, ...]   # optional list of strings (node ids or skill names)

The block is OPTIONAL and ADDITIVE: a SKILL.md without it lints clean (default mode).
The block must stay inside the Safe YAML Subset. Unknown keys and type violations are errors,
so typos fail loudly instead of silently changing loop behavior.

Usage:
    python3 scripts/lib/lint-workflow.py skills/13-specialized/<name>/SKILL.md
    python3 scripts/lib/lint-workflow.py --all          # scan every skill (advisory coverage)
    python3 scripts/lib/lint-workflow.py --selftest     # inline self-checks
Exit code 0 = clean, 1 = lint errors found.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
sys.path.insert(0, os.path.join(ROOT, "scripts", "lib"))

from lib import safe_yaml  # noqa: E402  (after path insert above)

SKILLS_DIR = os.path.join(ROOT, "skills")
ALLOWED_TOP = {"artifacts", "completion", "iteration", "escalate_to"}
ALLOWED_ARTIFACT = {"inputs", "outputs"}
ALLOWED_COMPLETION = {"criteria", "evidence"}
ALLOWED_ITERATION = {"max", "on_exhaustion"}
EXHAUSTIONS = ("escalate", "next", "fail")
EVIDENCES = ("required", "optional")

FRONT_RE = re.compile(r"^---\s*\n(.*?)\n---\s*$", re.S | re.M)


def extract_workflow_block(skill_text):
    """Return the raw text of the `workflow:` block from a SKILL.md, or None."""
    m = FRONT_RE.search(skill_text)
    if not m:
        return None
    front = m.group(1).splitlines()
    lines = []
    started = False
    indent = None
    for raw in front:
        if not started:
            if re.match(r"^workflow:\s*$", raw):
                started = True
            continue
        if raw.strip() == "" or raw.lstrip().startswith("#"):
            continue
        ind = len(raw) - len(raw.lstrip(" "))
        if ind == 0:
            break  # next top-level frontmatter key
        if indent is None:
            indent = ind
        if ind < indent:
            break
        lines.append(raw)
    if not started:
        return None
    return "\n".join(lines) + "\n" if lines else ""


def lint_workflow_block(text, where="workflow:"):
    """Validate one parsed `workflow:` block body (already split from its key)."""
    errors = []
    if text is None or text.strip() == "":
        return errors  # absent block = default mode
    # The block is captured indented under its frontmatter key; dedent before parsing.
    lines = [ln for ln in text.splitlines() if ln.strip()]
    if lines:
        min_indent = min(len(ln) - len(ln.lstrip(" ")) for ln in lines)
        text = "\n".join(ln[min_indent:] if len(ln) >= min_indent else ln for ln in lines)
    try:
        data = safe_yaml.parse(text)
    except safe_yaml.SafeYamlError as exc:
        return ["%s: yaml error: %s" % (where, exc)]
    if not isinstance(data, dict):
        return ["%s: block must be a mapping" % where]

    for key in data:
        if key not in ALLOWED_TOP:
            errors.append("%s: unknown key %r (allowed: %s)"
                          % (where, key, ", ".join(sorted(ALLOWED_TOP))))

    artifacts = data.get("artifacts") or {}
    if artifacts:
        if not isinstance(artifacts, dict):
            errors.append("%s: artifacts must be a mapping" % where)
        else:
            for key in artifacts:
                if key not in ALLOWED_ARTIFACT:
                    errors.append("%s: artifacts has unknown key %r" % (where, key))
                elif not _is_str_list(artifacts[key]):
                    errors.append("%s: artifacts.%s must be a list of strings" % (where, key))

    completion = data.get("completion") or {}
    if completion:
        if not isinstance(completion, dict):
            errors.append("%s: completion must be a mapping" % where)
        else:
            for key in completion:
                if key not in ALLOWED_COMPLETION:
                    errors.append("%s: completion has unknown key %r" % (where, key))
            criteria = completion.get("criteria")
            if criteria is not None and not _is_str_list(criteria):
                errors.append("%s: completion.criteria must be a list of strings" % where)
            ev = completion.get("evidence")
            if ev is not None and ev not in EVIDENCES:
                errors.append("%s: completion.evidence must be required|optional" % where)

    iteration = data.get("iteration") or {}
    if iteration:
        if not isinstance(iteration, dict):
            errors.append("%s: iteration must be a mapping" % where)
        else:
            for key in iteration:
                if key not in ALLOWED_ITERATION:
                    errors.append("%s: iteration has unknown key %r" % (where, key))
            mx = iteration.get("max")
            if mx is not None and (not isinstance(mx, int) or isinstance(mx, bool) or mx < 1):
                errors.append("%s: iteration.max must be an integer >= 1" % where)
            oe = iteration.get("on_exhaustion")
            if oe is not None and oe not in EXHAUSTIONS:
                errors.append("%s: iteration.on_exhaustion must be %s"
                              % (where, "|".join(EXHAUSTIONS)))

    esc = data.get("escalate_to")
    if esc is not None and not _is_str_list(esc):
        errors.append("%s: escalate_to must be a list of strings" % where)
    return errors


def _is_str_list(value):
    return isinstance(value, list) and all(isinstance(v, str) for v in value)


def lint_skill_file(path):
    """Lint one SKILL.md. Returns (errors, has_block)."""
    try:
        text = open(path, encoding="utf-8").read()
    except OSError as exc:
        return ["unreadable: %s" % exc], False
    block = extract_workflow_block(text)
    if block is None:
        return [], False
    return lint_workflow_block(block, where="%s workflow:" % os.path.relpath(path, ROOT)), True


def _find_all_skills():
    found = []
    if not os.path.isdir(SKILLS_DIR):
        return found
    for domain in sorted(os.listdir(SKILLS_DIR)):
        dpath = os.path.join(SKILLS_DIR, domain)
        if not os.path.isdir(dpath):
            continue
        for name_dir in sorted(os.listdir(dpath)):
            skill_file = os.path.join(dpath, name_dir, "SKILL.md")
            if os.path.isfile(skill_file):
                found.append(skill_file)
    return found


def _selftest():
    results = []
    valid_block = (
        "  artifacts:\n"
        "    inputs: [brief, system-context]\n"
        "    outputs: [spec]\n"
        "  completion:\n"
        "    criteria:\n"
        "      - 'Every explicit requirement has a matching section'\n"
        "      - 'Open questions are resolved or flagged'\n"
        "    evidence: required\n"
        "  iteration:\n"
        "    max: 3\n"
        "    on_exhaustion: escalate\n"
        "  escalate_to: [human-gate]\n"
    )
    results.append(("valid full block accepted", lint_workflow_block(valid_block) == []))

    results.append(("absent block = clean", lint_workflow_block(None) == []))

    bad_key = "  loops: 2\n" + valid_block
    results.append(("unknown top key flagged",
                    any("unknown key 'loops'" in e for e in lint_workflow_block(bad_key))))

    bad_criteria = "  completion:\n    criteria: nope\n"
    results.append(("criteria non-list flagged",
                    any("criteria must be a list" in e for e in lint_workflow_block(bad_criteria))))

    bad_max = "  iteration:\n    max: 0\n"
    results.append(("iteration.max < 1 flagged",
                    any("max must be an integer >= 1" in e for e in lint_workflow_block(bad_max))))

    bad_ev = "  completion:\n    evidence: sometimes\n"
    results.append(("evidence enum flagged",
                    any("evidence must be required|optional" in e
                        for e in lint_workflow_block(bad_ev))))

    bad_exhaust = "  iteration:\n    on_exhaustion: giveup\n"
    results.append(("on_exhaustion enum flagged",
                    any("on_exhaustion must be" in e for e in lint_workflow_block(bad_exhaust))))

    sample = "---\nname: demo\ndescription: demo\nworkflow:\n  artifacts:\n    outputs: [x]\n---\nbody\n"
    block = extract_workflow_block(sample)
    results.append(("frontmatter extraction finds block", block is not None and block.strip() != ""))
    sample2 = "---\nname: demo\ndescription: demo\n---\nbody\n"
    results.append(("frontmatter without workflow -> None",
                    extract_workflow_block(sample2) is None))

    failed = [name for name, ok in results if not ok]
    for name, ok in results:
        print("%s %s" % ("PASS" if ok else "FAIL", name))
    print("selftest: %d checks, %d failed" % (len(results), len(failed)))
    return 1 if failed else 0


def main(argv=None):
    import argparse

    ap = argparse.ArgumentParser(description="Lint optional workflow: frontmatter blocks")
    ap.add_argument("files", nargs="*", help="SKILL.md paths")
    ap.add_argument("--all", action="store_true", help="scan every skill")
    ap.add_argument("--selftest", action="store_true", help="run inline self-checks")
    args = ap.parse_args(argv)

    if args.selftest:
        return _selftest()

    targets = list(args.files)
    if args.all or not targets:
        targets = _find_all_skills()
    if not targets:
        print("no skill files to lint")
        return 0

    any_error = False
    declared = 0
    for path in targets:
        errors, has_block = lint_skill_file(path)
        if has_block:
            declared += 1
        if errors:
            any_error = True
            print("FAIL %s" % path)
            for e in errors:
                print("     - %s" % e)
    if args.all:
        print("scanned %d skills; %d declare a workflow: block" % (len(targets), declared))
    return 1 if any_error else 0


if __name__ == "__main__":
    sys.exit(main())
