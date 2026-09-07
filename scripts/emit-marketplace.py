#!/usr/bin/env python3
"""emit-marketplace.py — generate .claude-plugin/marketplace.json from the library.

Mirrors how skills.sh / Claude marketplaces structure catalogs: a marketplace manifest
lists plugins, each plugin declares a component path whose CHILDREN are skill dirs
(<dir>/<name>/SKILL.md at one level of nesting — the same contract every agent scanner
and the Claude plugin loader use).

Generated catalog (idempotent, stdlib only):
  - one plugin per domain:  skills: ["./skills/<domain>"]   (children = that domain's skills)
  - one aggregated plugin:  skills: ["./skills-flat"]        (children = all 297 skills)

Entries use `strict: false` so the marketplace entry itself carries the definition and no
per-plugin .claude-plugin/plugin.json is required for discovery; add real plugin.json
manifests inside dedicated plugin repos when moving to strict mode.

Usage: python3 scripts/emit-marketplace.py [--out .claude-plugin/marketplace.json]
"""
import argparse
import glob
import json
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

def frontmatter_name(skill_dir):
    """Pull canonical `name:` and `description:` from a SKILL.md frontmatter (light parse)."""
    p = os.path.join(skill_dir, "SKILL.md")
    try:
        txt = open(p, encoding="utf-8").read()
    except OSError:
        return None, ""
    head = txt.split("---", 2)[1] if txt.startswith("---") else txt
    name = None
    for ln in head.splitlines():
        if ln.startswith("name:") and name is None:
            name = ln.split(":", 1)[1].strip().strip("\"'")
        if ln.startswith("description:"):
            break
    return name, head

def skill_dirs(path):
    """Directories under path that contain SKILL.md at one level of nesting."""
    found = []
    if os.path.isdir(path):
        for child in sorted(os.listdir(path)):
            if os.path.isfile(os.path.join(path, child, "SKILL.md")):
                found.append(child)
    return found

def build():
    domains = []
    for d in sorted(os.listdir(os.path.join(ROOT, "skills"))):
        dp = os.path.join(ROOT, "skills", d)
        if not os.path.isdir(dp):
            continue
        kids = skill_dirs(dp)
        if kids:
            domains.append((d, kids))

    plugins = []
    for d, kids in domains:
        plugins.append({
            "name": re.sub(r"^\d+-", "", d),   # '00-framework' -> 'framework' (kebab-case)
            "description": "%d skills: %s, … (%s)"
                            % (len(kids), ", ".join(kids[:6]), d),
            "version": "1.0.0",
            "category": d.split("-", 1)[-1],
            "source": "github",
            "repo": "zeroes-ones/Skills",
            "ref": "main",
            "strict": False,
            "skills": ["./skills/%s" % d],
        })

    all_kids = skill_dirs(os.path.join(ROOT, "skills-flat"))
    plugins.insert(0, {
        "name": "zeroes-ones-all",
        "description": "All %d skills in one plugin (flat discovery layer)" % len(all_kids),
        "version": "1.0.0",
        "category": "full-library",
        "source": "github",
        "repo": "zeroes-ones/Skills",
        "ref": "main",
        "strict": False,
        "skills": ["./skills-flat"],
    })

    return {
        "name": "zeroes-ones-skills",
        "owner": {"name": "Sandeep Kumar Penchala",
                  "email": "sandeepkumarp@outlook.com"},
        "plugins": plugins,
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(ROOT, ".claude-plugin", "marketplace.json"))
    args = ap.parse_args()

    catalog = build()
    total = sum(len(p["skills"]) for p in catalog["plugins"] if p["skills"])
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)
        f.write("\n")

    # Self-validate: every declared skills path exists and has skill children.
    ok = True
    for p in catalog["plugins"]:
        for rel in p.get("skills", []):
            full = os.path.normpath(os.path.join(ROOT, rel.lstrip("./")))
            kids = skill_dirs(full)
            if not kids:
                ok = False
                print("WARN: no skill children under %s" % rel)
    print("wrote %s: %d plugins (%s)" % (args.out, len(catalog["plugins"]), catalog["name"]))
    print("declared skill dirs across plugins: %s" % total)
    if not ok:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
