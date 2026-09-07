#!/usr/bin/env python3
"""skill-factory.py — create a skill draft on demand (stdlib only).

Steer: skills should be created dynamically when a task needs a capability the library lacks,
then used immediately as graph nodes / agents / sub-agents. This generator scaffolds a compact,
convention-shaped SKILL.md draft (name/description/portability/optional workflow: node contract,
identity + core sections) in seconds.

Usage:
    python3 scripts/skill-factory.py --name changelog-writer \
        --description "Drafts release notes from git history and issue labels." \
        --workflow                                   # add a workflow: node contract
    python3 scripts/skill-factory.py --name X --out /tmp/dir          # write elsewhere
    python3 scripts/skill-factory.py --name X --dry-run               # print, don't write

Next steps printed after generation: fill the domain sections, run lint-workflow/lint-template,
add a golden case, and register the skill in the router/chain. Drafts are status: draft until
they pass the gates. To run it as an agent/sub-agent, reference it in a workflow manifest node;
engine nodes driven by agent_executor.py are the sub-agents, and supervisor workers fan out to
them.
"""

import argparse
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _frontmatter(name, description, workflow):
    lines = [
        "---",
        "name: %s" % name,
        "description: >",
        "  %s" % description,
        "author: Sandeep Kumar Penchala",
        "license: MIT",
        "portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI",
        "type: framework",
        "status: draft",
        "version: 1.0.0",
        "updated: %s" % time.strftime("%Y-%m-%d"),
        "tags: [dynamic, on-demand]",
        "token_budget: 2500",
        "chain:",
        "  consumes_from: []",
        "  feeds_into: []",
    ]
    if workflow:
        lines += [
            "workflow:",
            "  artifacts:",
            "    outputs: [%s-result]" % name,
            "  completion:",
            "    criteria:",
            "      - The task described in the request is addressed with concrete output",
            "    evidence: required",
            "  escalate_to: [human-gate]",
        ]
    lines.append("---")
    return "\n".join(lines)


_BODY = """# {title}

> Draft generated on demand by scripts/skill-factory.py. Status: draft — fill the domain
> sections, then run the gates (lint-workflow, lint-template) and add a golden case before use.

## Route the Request
<!-- QUICK: 30s -->
TODO: define the intents this skill handles and route each to the core workflow.

## When to Use
<!-- QUICK: 30s -->
- TODO: when the request matches the description above.

## When NOT to Use
- TODO: name adjacent skills that should own this instead.

## Ground Rules
<!-- QUICK: 30s -->
| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|---------------------|--------------------|--------------------|
| G1 | TODO | TODO | TODO |

## Core Workflow
1. TODO: intake and understand the task (Phase 1)
2. TODO: execute the domain work (Phase 2)
3. TODO: verify output against the request with evidence (Phase 3)

## Verification
| # | Complete when | Verify |
|---|---------------|--------|
| 1 | Complete when the task from the request is addressed | Review output against every stated requirement |
"""


def build(name, description, workflow):
    body = _BODY.format(title=name.replace("-", " ").title())
    return _frontmatter(name, description, workflow) + "\n" + body


def main(argv=None):
    ap = argparse.ArgumentParser(description="Create a skill draft on demand")
    ap.add_argument("--name", required=True, help="kebab-case skill name")
    ap.add_argument("--description", required=True, help="one-line purpose (Use when ...)")
    ap.add_argument("--workflow", action="store_true", help="include a workflow: node contract")
    ap.add_argument("--domain", default="13-specialized", help="skills/<domain> to write into")
    ap.add_argument("--out", help="write SKILL.md into this directory instead of the repo")
    ap.add_argument("--dry-run", action="store_true", help="print the draft, do not write")
    args = ap.parse_args(argv)

    name = args.name.lower().replace("_", "-")
    text = build(name, args.description, args.workflow)
    if args.dry_run:
        print(text)
        return 0
    if args.out:
        os.makedirs(args.out, exist_ok=True)
        path = os.path.join(args.out, "SKILL.md")
        refs = os.path.join(args.out, "references")
    else:
        dpath = os.path.join(ROOT, "skills", args.domain, name)
        path = os.path.join(dpath, "SKILL.md")
        refs = os.path.join(dpath, "references")
        os.makedirs(dpath, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    os.makedirs(refs, exist_ok=True)
    print("created draft: %s" % path)
    print("next: fill the TODO sections; run:")
    print("  python3 scripts/lib/lint-workflow.py %s" % path)
    print("  python3 scripts/validate-workflows.py --coverage   # name must resolve")
    print("  bash scripts/eval-skill.sh <name>                  # after adding golden cases")
    return 0


if __name__ == "__main__":
    sys.exit(main())
