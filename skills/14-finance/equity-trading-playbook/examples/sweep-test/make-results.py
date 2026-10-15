#!/usr/bin/env python3
"""
make_results.py -- rebuild RESULTS.md by slicing the captured stdout of study.py.

Every figure in RESULTS.md is pasted from run-output.txt, so the report cannot
drift away from a run that actually happened. `--check` is the freshness gate:
it regenerates in memory and compares the hash with the file on disk.

USAGE
    py -3 make-results.py            # writes RESULTS.md
    py -3 make-results.py --check    # exit 0 if RESULTS.md is current, 1 if stale
"""

import hashlib
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(newline="\n")

HERE = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.join(HERE, "run-output.txt")
OUT = os.path.join(HERE, "RESULTS.md")

SEP = "=" * 100

PREAMBLE = """# RESULTS -- a multiple-testing-controlled sweep of moving-average trend books

**Generated file. Do not hand-edit.** Every line below is the verbatim stdout of
one real run of `study.py`, written by `make-results.py` from `run-output.txt`.
The grid design is declared inside `study.py` as constants, above every
computation that uses them.

    py -3 study.py > run-output.txt      # the run this report is sliced from
    py -3 make-results.py                # rebuild this file
    py -3 make-results.py --check        # freshness gate

Companions: [`README.md`](README.md) (design, sources, commands),
[`FINDINGS.md`](FINDINGS.md) (the honest narrative),
[`handcheck-output.txt`](handcheck-output.txt) (an independent re-derivation),
[`out/`](out) (machine-readable tables).

---

"""


def build(text):
    lines = text.split("\n")
    parts = []
    buf = []
    title = None
    i = 0
    n = len(lines)
    while i < n:
        if (lines[i].startswith("====") and i + 2 < n
                and lines[i + 2].startswith("====") and lines[i + 1].strip()):
            # the buffer that just ended belongs to the title captured BEFORE this
            # banner, not to the banner itself
            if buf:
                parts.append((title, buf))
                buf = []
            title = lines[i + 1].strip()
            i += 3
            continue
        buf.append(lines[i])
        i += 1
    if buf:
        parts.append((title, buf))

    out = [PREAMBLE]
    for t, body in parts:
        text_body = "\n".join(body).rstrip("\n")
        if not text_body.strip():
            continue
        if t is None:
            out.append("```text\n%s\n```\n" % text_body)
        else:
            out.append("## %s\n\n```text\n%s\n```\n" % (t, text_body))
    return "\n".join(out)


def main(argv):
    if not os.path.exists(RUN):
        raise SystemExit("ERROR: %s missing -- run `py -3 study.py > run-output.txt` first" % RUN)
    with open(RUN, "r", encoding="utf-8") as fh:
        content = build(fh.read())
    digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
    if "--check" in argv:
        if not os.path.exists(OUT):
            print("STALE: %s does not exist" % OUT)
            return 1
        with open(OUT, "r", encoding="utf-8") as fh:
            have = fh.read()
        if have == content:
            print("current: RESULTS.md matches run-output.txt (sha256 %s)" % digest[:16])
            return 0
        print("STALE: RESULTS.md does not match run-output.txt (want %s)" % digest[:16])
        return 1
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(content)
    print("wrote %s (%d bytes, sha256 %s)" % (OUT, len(content), digest[:16]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
