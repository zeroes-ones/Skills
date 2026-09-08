#!/usr/bin/env python3
"""emit-skill-registry.py — machine-readable registry generator (stdlib only, P11).

Walks skills/<domain>/<name>/SKILL.md, parses frontmatter (yaml_shim, stdlib),
and emits one machine-readable record per skill so downstream tooling and CI
drift checks never depend on hand-maintained metadata:

    name, domain, version, status, type, license, author, updated,
    token_budget, tags, raw_words, est_tokens, description flags/length,
    chain: {consumes_from: [...], feeds_into: [...]}

Usage:
    python3 scripts/emit-skill-registry.py                # JSON to stdout
    python3 scripts/emit-skill-registry.py --out FILE     # write artifact
    python3 scripts/emit-skill-registry.py --check        # exit 1 if any record
                                                          # fails required-field gate
Exit codes: 0 ok; 1 records failed the required-field gate (--check) or IO error.
"""

import argparse
import json
import os
import re
import sys

REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SKILLS = os.path.join(REPO, "skills")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from yaml_shim import safe_load  # noqa: E402  (stdlib fallback; real yaml when available upstream)

REQUIRED_FIELDS = ["name", "version", "status", "type", "license", "token_budget"]


def _strip_markers(text):
    return re.sub(r"\s*\*\*\((?:QUICK|STANDARD|DEEP)\)\*\*\s*", "", text or "")


def _scan():
    records = []
    for domain_dir in sorted(os.listdir(SKILLS)):
        domain_path = os.path.join(SKILLS, domain_dir)
        if not os.path.isdir(domain_path):
            continue
        for name_dir in sorted(os.listdir(domain_path)):
            skill_md = os.path.join(domain_path, name_dir, "SKILL.md")
            if not os.path.isfile(skill_md):
                continue
            content = open(skill_md, encoding="utf-8").read()
            parts = re.split(r"^---\s*$", content, maxsplit=2, flags=re.MULTILINE)
            fm = safe_load(parts[1]) if len(parts) >= 3 else {}
            body = parts[2] if len(parts) >= 3 else content
            desc = fm.get("description", "")
            chain = fm.get("chain", {}) if isinstance(fm.get("chain"), dict) else {}
            records.append({
                "name": fm.get("name", name_dir),
                "path": f"skills/{domain_dir}/{name_dir}/SKILL.md",
                "domain": domain_dir,
                "version": fm.get("version"),
                "status": fm.get("status"),
                "type": fm.get("type"),
                "license": fm.get("license"),
                "author": fm.get("author"),
                "updated": fm.get("updated"),
                "token_budget": fm.get("token_budget"),
                "tags": fm.get("tags") if isinstance(fm.get("tags"), list) else [],
                "raw_words": len(body.split()),
                "est_tokens": int(len(body.split()) * 1.33),
                "description": {
                    "chars": len(desc),
                    "has_use_when": "Use when" in desc,
                    "has_handles": "Handles" in desc,
                    "has_do_not_use": "Do NOT use" in desc,
                },
                "chain": {
                    "consumes_from": chain.get("consumes_from", []),
                    "feeds_into": chain.get("feeds_into", []),
                },
            })
    return records


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=None, help="write registry JSON to FILE")
    ap.add_argument("--check", action="store_true", help="gate on required fields")
    args = ap.parse_args()

    records = _scan()
    missing = []
    for r in records:
        absent = [f for f in REQUIRED_FIELDS if r.get(f) in (None, "")]
        if absent:
            missing.append((r["name"], absent))

    payload = {
        "version": "1.0.0",
        "generated_by": "scripts/emit-skill-registry.py",
        "count": len(records),
        "records": records,
    }

    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, ensure_ascii=False)
        print(f"wrote {len(records)} records to {args.out}")
    else:
        print(json.dumps(payload, indent=2, ensure_ascii=False))

    if args.check:
        if missing:
            print(f"FAIL: {len(missing)} records missing required fields:", file=sys.stderr)
            for name, fields in missing[:10]:
                print(f"  {name}: missing {fields}", file=sys.stderr)
            return 1
        print(f"registry gate OK: all {len(records)} records have required fields")
    return 0


if __name__ == "__main__":
    sys.exit(main())
