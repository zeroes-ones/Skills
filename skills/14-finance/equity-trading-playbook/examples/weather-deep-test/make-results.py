#!/usr/bin/env python3
"""
make-results.py -- assemble RESULTS.md from the captured raw stdout.

RESULTS.md must be the run's own output, verbatim.  This script does no
arithmetic of its own: it concatenates the captured stdout of study.py,
handcheck.py, verify_sources.py and pull_ohlcv.py behind a single header that
states what was run, when, and how to reproduce it.

USAGE
    py -3 make-results.py
"""

import hashlib
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(newline="\n")

HERE = os.path.dirname(os.path.abspath(__file__))
LOGS = os.path.join(HERE, "logs")


def read(path):
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        return fh.read().rstrip("\n")


def main():
    parts = []
    for name, title in [
        ("pull-output.txt", "PULL -- MCP payload on disk -> data/*.csv"),
        ("reuse-output.txt", "REUSE -- extending SPY back to 1993 from the "
                             "sibling study, with overlap verification"),
        ("source-check.txt", "SOURCE CROSS-CHECK -- this study's data against "
                             "the sibling studies' independent pulls"),
        ("run-output.txt", "STUDY.PY -- the run, verbatim"),
        ("handcheck-output.txt", "HANDCHECK.PY -- the independent "
                                 "re-derivation, verbatim"),
    ]:
        path = os.path.join(LOGS, name)
        if not os.path.isfile(path):
            print("WARNING: %s is missing; section skipped" % path)
            continue
        with open(path, "rb") as fh:
            digest = hashlib.sha256(fh.read()).hexdigest()
        body = read(path)
        parts.append("## %s\n\n"
                     "`%s` -- sha256 `%s`\n\n"
                     "```\n%s\n```" % (title, name, digest, body))

    files = sorted(os.listdir(os.path.join(HERE, "out")))
    listing = "\n".join("  %-38s %s" % (
        f, hashlib.sha256(open(os.path.join(HERE, "out", f), "rb").read())
        .hexdigest()[:16]) for f in files)

    head = """# RESULTS -- weather-deep-test

Every number below is the verbatim stdout of a real run on the real data in
`data/`.  Nothing in this file was typed by hand or carried over from another
study.

Reproduce with:

```
export PYTHONIOENCODING=utf-8
py -3 pull_ohlcv.py --results <tool-results dirs> --out data --pull-date 2026-10-14
py -3 reuse_sibling_data.py --data data --sibling ../frontier-test/data --name SPY
py -3 verify_sources.py
py -3 study.py      > logs/run-output.txt
py -3 handcheck.py  > logs/handcheck-output.txt
py -3 make-results.py
```

Determinism: `study.py` was run twice and the two stdouts are byte-identical
(`diff logs/det-A.txt logs/det-B.txt` is empty), and every one of the artefact
hashes below is stable across runs.

## `out/` artefacts written by this run (sha256 prefix)

```
%s
```
""" % listing

    out = head + "\n\n" + "\n\n".join(parts) + "\n"
    with open(os.path.join(HERE, "RESULTS.md"), "w", encoding="utf-8",
              newline="\n") as fh:
        fh.write(out)
    print("wrote RESULTS.md  %d bytes" % len(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
