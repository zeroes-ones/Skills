#!/usr/bin/env python3
"""emit-marketplace.py — generate the Claude Code marketplace for this library.

Schema verified against Claude Code 2.1.222 (2026-09): a marketplace repo contains
`.claude-plugin/marketplace.json` declaring plugins whose `source` is a RELATIVE DIR
inside the marketplace repo; each plugin dir carries `plugin.json` with component paths
(here `skills: ["./skills"]`) whose children are skill dirs at one level of nesting.

Generated catalog (idempotent, stdlib only):
  - `plugins/zeroes-ones-all/`  -> skills symlinked to ../../../skills-flat (all 297)
  - `plugins/<domain>/`         -> one per domain, skills symlinked to ../../../skills/<domain>

`plugin.json` is the authority per plugin; skills dirs are symlinks (like the committed
`skills-flat` layer) so nothing is duplicated.

Usage: python3 scripts/emit-marketplace.py [--out .claude-plugin/marketplace.json]
"""
import argparse
import json
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
AUTHOR = {"name": "Sandeep Kumar Penchala", "email": "sandeepkumarp@outlook.com"}
VERSION = "1.0.0"


def skill_dirs(path):
    """Directories under path that contain SKILL.md at one level of nesting."""
    found = []
    if os.path.isdir(path):
        for child in sorted(os.listdir(path)):
            if os.path.isfile(os.path.join(path, child, "SKILL.md")):
                found.append(child)
    return found


def _plugin_file(pid, desc):
    return {
        "name": pid,
        "version": VERSION,
        "description": desc,
        "author": AUTHOR,
        "skills": ["./skills"],
    }


def _ensure_skills_link(pid, target_rel):
    """plugins/<pid>/skills -> target_rel (relative to the plugin dir). Idempotent."""
    link = os.path.join(ROOT, "plugins", pid, "skills")
    if os.path.islink(link):
        if os.readlink(link) != target_rel:
            os.remove(link)
            os.symlink(target_rel, link)
        return
    if os.path.exists(link):
        raise SystemExit(
            f"ERROR: {os.path.relpath(link, ROOT)} exists and is not a symlink; "
            f"remove it first (wanted symlink -> {target_rel})")
    os.symlink(target_rel, link)


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
    # zeroes-ones-all first: the whole flat layer
    all_kids = skill_dirs(os.path.join(ROOT, "skills-flat"))
    plugins.append({
        "name": "zeroes-ones-all",
        "description": "All %d skills in one plugin (flat discovery layer)" % len(all_kids),
        "source": "./plugins/zeroes-ones-all",
    })
    # then one plugin per domain
    for d, kids in domains:
        pid = re.sub(r"^\d+-", "", d)  # '00-framework' -> 'framework' (kebab-case)
        plugins.append({
            "name": pid,
            "description": "%d skills: %s, … (%s)" % (len(kids), ", ".join(kids[:6]), d),
            "source": "./plugins/%s" % pid,
        })

    return {
        "name": "zeroes-ones-skills",
        "owner": AUTHOR,
        "description": "Zeroes & Ones skills library: 297 agent-agnostic skills "
                       "covering the full company lifecycle (one plugin per domain + "
                       "zeroes-ones-all over the flat layer)",
        "plugins": plugins,
    }


def write_plugin_dirs(catalog):
    """Materialize plugins/<id>/plugin.json + the skills symlink for every plugin."""
    os.makedirs(os.path.join(ROOT, "plugins"), exist_ok=True)
    # all -> flat layer
    pid = "zeroes-ones-all"
    desc = next(p["description"] for p in catalog["plugins"] if p["name"] == pid)
    os.makedirs(os.path.join(ROOT, "plugins", pid), exist_ok=True)
    with open(os.path.join(ROOT, "plugins", pid, "plugin.json"), "w", encoding="utf-8") as f:
        json.dump(_plugin_file(pid, desc), f, indent=2)
        f.write("\n")
    _ensure_skills_link(pid, "../../skills-flat")

    # per-domain plugins
    for entry in catalog["plugins"]:
        if entry["name"] == "zeroes-ones-all":
            continue
        pid = entry["name"]
        domain_dir = None
        for d in sorted(os.listdir(os.path.join(ROOT, "skills"))):
            if re.sub(r"^\d+-", "", d) == pid and os.path.isdir(os.path.join(ROOT, "skills", d)):
                domain_dir = d
                break
        if domain_dir is None:
            continue
        os.makedirs(os.path.join(ROOT, "plugins", pid), exist_ok=True)
        with open(os.path.join(ROOT, "plugins", pid, "plugin.json"), "w", encoding="utf-8") as f:
            json.dump(_plugin_file(pid, entry["description"]), f, indent=2)
            f.write("\n")
        _ensure_skills_link(pid, "../../skills/%s" % domain_dir)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(ROOT, ".claude-plugin", "marketplace.json"))
    args = ap.parse_args()

    catalog = build()
    write_plugin_dirs(catalog)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)
        f.write("\n")

    # Self-validate: every plugin source dir exists, has plugin.json, and its skills
    # symlink resolves to a dir with skill children.
    ok = True
    for p in catalog["plugins"]:
        sdir = os.path.normpath(os.path.join(ROOT, p["source"].lstrip("./")))
        pj = os.path.join(sdir, "plugin.json")
        sl = os.path.join(sdir, "skills")
        if not (os.path.isfile(pj) and os.path.islink(sl)):
            ok = False
            print("WARN: plugin dir incomplete: %s" % p["source"])
            continue
        resolved = os.path.normpath(os.path.join(os.path.dirname(sl), os.readlink(sl)))
        if not skill_dirs(resolved):
            ok = False
            print("WARN: no skill children under resolved skills of %s" % p["name"])
    print("wrote %s: %d plugins (%s)" % (args.out, len(catalog["plugins"]), catalog["name"]))
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
