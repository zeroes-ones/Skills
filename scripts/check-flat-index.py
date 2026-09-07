#!/usr/bin/env python3
"""check-flat-index.py — verify the agent discovery layer (skills-flat/).

Invariants:
  1. Exactly one flat entry per real skill (297 today), one level deep.
  2. No duplicate skill names across domains (a name collision would silently
     overwrite a link in the flat view).
  3. Every skills-flat/<name>/SKILL.md resolves to a real file (broken symlink
     or missing dir fails).

Usage: python3 scripts/check-flat-index.py   (stdlib only, exits nonzero on drift)
"""
import glob
import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
FLAT = os.path.join(ROOT, "skills-flat")

errors = []

# 1+2: real skills and duplicate names
dups = {}
for s in glob.glob(os.path.join(ROOT, "skills", "*", "*", "SKILL.md")):
    name = os.path.basename(os.path.dirname(s))
    dups.setdefault(name, []).append(s)
collisions = {k: v for k, v in dups.items() if len(v) > 1}
if collisions:
    errors.append("duplicate skill names would collide in flat view: %s"
                  % {k: v for k, v in collisions.items()})

# 3: flat layer resolvable
if not os.path.isdir(FLAT):
    errors.append("missing skills-flat/ — run scripts/build-flat-index.sh")
else:
    flat = set(os.listdir(FLAT))
    missing = set(dups) - flat
    if missing:
        errors.append("flat layer missing %d skills (run scripts/build-flat-index.sh): %s"
                      % (len(missing), sorted(missing)[:5]))
    broken = [n for n in flat if not os.path.isfile(os.path.join(FLAT, n, "SKILL.md"))]
    if broken:
        errors.append("unresolvable flat entries: %s" % broken[:5])
    if flat - set(dups):
        errors.append("stale flat entries (not real skills): %s"
                      % sorted(flat - set(dups))[:5])

if errors:
    for e in errors:
        print("FAIL: " + e)
    sys.exit(1)
print("agent discovery layer OK: %d/%d skills flat-resolvable, no collisions"
      % (len(dups), len(dups)))
