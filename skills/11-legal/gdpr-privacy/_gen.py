#!/usr/bin/env python3
"""Generate all GDPR privacy compliance markdown files."""
import os

BASE = "/Users/sp.vm/Documents/Projects/Skills/skills/11-legal/gdpr-privacy"

def append_skill_md():
    path = os.path.join(BASE, "SKILL.md")
    with open(path, "a") as f:
        f.write(SKILL_PART2)
    print(f"Appended {len(SKILL_PART2)} bytes to SKILL.md")

SKILL_PART2 = ""
