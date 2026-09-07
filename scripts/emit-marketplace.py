#!/usr/bin/env python3
"""emit-marketplace.py — generate the Claude Code marketplace for this library.

Schema verified against Claude Code 2.1.222 (2026-09): a marketplace repo contains
`.claude-plugin/marketplace.json` declaring plugins whose `source` is a RELATIVE DIR
inside the marketplace repo; each plugin dir carries `plugin.json` with component paths
(here `skills: ["./skills"]`) whose children are skill dirs at one level of nesting.

Generated catalog (idempotent, stdlib only):
  - `plugins/zeroes-ones-all/`  -> skills symlinked to ../../skills-flat (all 297)
  - `plugins/<domain>/`         -> one per domain, skills symlinked to ../../skills/<domain>
  - `plugins/flagship-<id>/`    -> one per flagship/*.json, skills symlinked to the
                                   curated skill names (../../skills-flat/<name>)

Usage:
    python3 scripts/emit-marketplace.py              # write marketplace.json + plugins/
    python3 scripts/emit-marketplace.py --check      # verify committed outputs are fresh
"""
import argparse
import json
import os
import re
import sys

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


def domain_of(skill_name):
    """Find skills/<domain>/<name> for a skill name (or None)."""
    for d in sorted(os.listdir(os.path.join(ROOT, "skills"))):
        if os.path.isfile(os.path.join(ROOT, "skills", d, skill_name, "SKILL.md")):
            return d
    return None


def _plugin_file(pid, desc):
    return {
        "name": pid,
        "version": VERSION,
        "description": desc,
        "author": AUTHOR,
        "skills": ["./skills"],
    }


def _write_plugin_json(pid, desc):
    d = os.path.join(ROOT, "plugins", pid)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "plugin.json"), "w", encoding="utf-8") as f:
        json.dump(_plugin_file(pid, desc), f, indent=2)
        f.write("\n")


def _ensure_symlink(link, target_rel):
    """Create/replace plugins/<pid>/skills (dir) symlink -> target_rel. Idempotent."""
    if os.path.islink(link):
        if os.readlink(link) != target_rel:
            os.remove(link)
            os.symlink(target_rel, link)
        return
    if os.path.exists(link):
        raise SystemExit(f"ERROR: {os.path.relpath(link, ROOT)} exists and is not a "
                         f"symlink; remove it first (wanted symlink -> {target_rel})")
    os.symlink(target_rel, link)


def _skill_symlinks(pid, names):
    """plugins/<pid>/skills/ is a real dir whose children symlink to skills-flat/<name>."""
    d = os.path.join(ROOT, "plugins", pid, "skills")
    os.makedirs(d, exist_ok=True)
    for nm in names:
        _ensure_symlink(os.path.join(d, nm), "../../../skills-flat/%s" % nm)


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
    all_kids = skill_dirs(os.path.join(ROOT, "skills-flat"))
    plugins.append({
        "name": "zeroes-ones-all",
        "description": "All %d skills in one plugin (flat discovery layer)" % len(all_kids),
        "source": "./plugins/zeroes-ones-all",
    })

    # flagship sets from flagship/*.json
    flagship_dir = os.path.join(ROOT, "flagship")
    if os.path.isdir(flagship_dir):
        for fn in sorted(os.listdir(flagship_dir)):
            if not fn.endswith(".json"):
                continue
            try:
                fs = json.load(open(os.path.join(flagship_dir, fn), encoding="utf-8"))
            except Exception:
                print("WARN: unreadable flagship file %s" % fn, file=sys.stderr)
                continue
            names = [s["name"] for s in fs.get("skills", [])]
            pid = "flagship-%s" % fs["id"]
            plugins.append({
                "name": pid,
                "description": "%s — %d curated skills: %s"
                               % (fs.get("title", fs["id"]), len(names),
                                  ", ".join(names[:8]) + ("…" if len(names) > 8 else "")),
                "source": "./plugins/%s" % pid,
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
                       "covering the full company lifecycle (one plugin per domain, "
                       "zeroes-ones-all over the flat layer, plus flagship sets)",
        "plugins": plugins,
    }


def write_outputs(catalog):
    """Materialize plugin dirs + marketplace.json. Returns dict of written bytes."""
    files = {}

    # zeroes-ones-all
    pid = "zeroes-ones-all"
    desc = next(p["description"] for p in catalog["plugins"] if p["name"] == pid)
    _write_plugin_json(pid, desc)
    _ensure_symlink(os.path.join(ROOT, "plugins", pid, "skills"), "../../skills-flat")

    # flagship plugins
    flagship_dir = os.path.join(ROOT, "flagship")
    if os.path.isdir(flagship_dir):
        for fn in sorted(os.listdir(flagship_dir)):
            if not fn.endswith(".json"):
                continue
            fs = json.load(open(os.path.join(flagship_dir, fn), encoding="utf-8"))
            pid = "flagship-%s" % fs["id"]
            desc = next(p["description"] for p in catalog["plugins"] if p["name"] == pid)
            _write_plugin_json(pid, desc)
            _skill_symlinks(pid, [s["name"] for s in fs.get("skills", [])])

    # per-domain plugins
    for entry in catalog["plugins"]:
        pid = entry["name"]
        if pid == "zeroes-ones-all" or pid.startswith("flagship-"):
            continue
        domain_dir = None
        for d in sorted(os.listdir(os.path.join(ROOT, "skills"))):
            if re.sub(r"^\d+-", "", d) == pid and \
                    os.path.isdir(os.path.join(ROOT, "skills", d)):
                domain_dir = d
                break
        if domain_dir is None:
            continue
        _write_plugin_json(pid, entry["description"])
        _ensure_symlink(os.path.join(ROOT, "plugins", pid, "skills"),
                        "../../skills/%s" % domain_dir)

    mkt = json.dumps(catalog, indent=2) + "\n"
    files[os.path.join(ROOT, ".claude-plugin", "marketplace.json")] = mkt.encode("utf-8")
    return files


def validate_catalog(catalog):
    ok = True
    for p in catalog["plugins"]:
        sdir = os.path.normpath(os.path.join(ROOT, p["source"].lstrip("./")))
        pj = os.path.join(sdir, "plugin.json")
        sl = os.path.join(sdir, "skills")
        if not os.path.isfile(pj):
            ok = False
            print("WARN: missing plugin.json: %s" % p["source"])
            continue
        if os.path.islink(sl):
            resolved = os.path.normpath(os.path.join(os.path.dirname(sl), os.readlink(sl)))
            if not skill_dirs(resolved):
                ok = False
                print("WARN: no skill children under resolved skills of %s" % p["name"])
        else:
            # flagship style: real dir with per-skill symlinks
            kids = skill_dirs(sl)
            if not kids:
                ok = False
                print("WARN: no skill children under %s/skills" % p["name"])
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out",
                    default=os.path.join(ROOT, ".claude-plugin", "marketplace.json"))
    ap.add_argument("--check", action="store_true",
                    help="verify committed marketplace.json + plugins/ are fresh (exit 1 on drift)")
    args = ap.parse_args()

    catalog = build()
    files = write_outputs(catalog)
    if not validate_catalog(catalog):
        raise SystemExit(1)

    if args.check:
        drifted = []
        for path, content in files.items():
            rel = os.path.relpath(path, ROOT)
            if not os.path.isfile(path):
                drifted.append(f"{rel}: MISSING")
            elif open(path, "rb").read() != content:
                drifted.append(f"{rel}: STALE")
        if drifted:
            print("Marketplace outputs are stale. Regenerate with:")
            print("  python3 scripts/emit-marketplace.py")
            for line in drifted:
                print(f"  - {line}")
            sys.exit(1)
        print("✓ marketplace outputs are fresh (%d plugins)" % len(catalog["plugins"]))
        return

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(json.dumps(catalog, indent=2) + "\n")
    print("wrote marketplace: %d plugins (%s)" % (len(catalog["plugins"]), catalog["name"]))
    print("plugin dirs: %d" % len(catalog["plugins"]))


if __name__ == "__main__":
    main()
