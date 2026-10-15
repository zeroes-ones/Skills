#!/usr/bin/env python3
"""make-results.py -- wrap the verbatim stdout of study.py and handcheck.py
into RESULTS.md, so the report cannot drift from the run.

Usage:  py -3 make-results.py
"""

import os

ROOT = os.path.dirname(os.path.abspath(__file__))
LOGS = os.path.join(ROOT, "logs")

HEADER = """# RESULTS -- real-skew-test

**Every table below is the VERBATIM stdout of a real run**, pasted by
`make-results.py` from `logs/study-output.txt` and `handcheck-output.txt`.  The
labels are not decoration:

- **`[MEASURED]`** -- derived from a real Robinhood option print.
- **`[MODELED]`** -- derived from the VIX proxy.

Nothing in this file is edited by hand.  Regenerate with:

```bash
py -3 study.py && py -3 handcheck.py && py -3 make-results.py
```

---

## A. The study

"""


def detab(t):
    """The transcripts are TAB-separated; render them readably rather than
    embedding literal tabs (markdownlint rejects tab indentation)."""
    return "\n".join(ln.replace("\t", "  ").rstrip()
                     for ln in t.rstrip("\n").split("\n"))


def main():
    study = open(os.path.join(LOGS, "study-output.txt"),
                 encoding="utf-8").read()
    hand = open(os.path.join(ROOT, "handcheck-output.txt"),
                encoding="utf-8").read()
    calllog = open(os.path.join(LOGS, "mcp-call-log.tsv"),
                   encoding="utf-8").read()
    plan = open(os.path.join(LOGS, "plan-output.txt"),
                encoding="utf-8").read()

    out = [HEADER, "```\n" + detab(study) + "\n```\n"]
    out.append("\n---\n\n## B. The independent hand-check\n\n")
    out.append("`handcheck.py` shares no code with `study.py` (a different `erf`, "
               "a bracket-expansion bisection, and OLS through the normal "
               "equations).  Section D of its output is the gap.\n\n")
    out.append("```\n" + detab(hand) + "\n```\n")
    out.append("\n---\n\n## C. The call budget\n\n")
    out.append("```\n" + detab(calllog) + "\n```\n")
    out.append("\n---\n\n## D. The declared plan, as emitted before the pull\n\n")
    out.append("```\n" + detab(plan) + "\n```\n")
    with open(os.path.join(ROOT, "RESULTS.md"), "w", encoding="utf-8",
              newline="\n") as fh:
        fh.write("".join(out))
    print("wrote RESULTS.md (%d bytes)" % os.path.getsize(
        os.path.join(ROOT, "RESULTS.md")))


if __name__ == "__main__":
    main()
