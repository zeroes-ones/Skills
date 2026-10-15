#!/usr/bin/env python3
"""
make-results.py -- assemble RESULTS.md from the captured raw stdout.

The tables in RESULTS.md are VERBATIM.  This script does not reformat, round,
recompute or reorder anything: it wraps the two captured streams in a header and
a short reading guide.  If a number is wrong, it is wrong in run-output.txt too,
and that file is committed alongside.

USAGE
    py -3 make-results.py
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(newline="\n")

HEADER = """# RESULTS -- narrow universe vs broad, measured

Pull date **2026-10-14**.  Quote snapshot **2026-10-15T00:39Z**.  Every table
below is copied verbatim from a real run of `study.py`; the complete captured
stdout is committed as [`run-output.txt`](run-output.txt), and the independent
re-derivation is committed as [`handcheck-output.txt`](handcheck-output.txt).

**How these tables are organised.**  Sections 0-3 answer question 1 (the
diversification cost of narrowing, and the frontier).  Section 4 answers question
2 (a basket of constituents vs the index).  Section 5 gives the negative
regime-cell counts.  Section 6 answers question 3 (the dispersion proxy).
Section 7 answers question 4 (costs, measured).  Section 8 is the direct verdict
and the frontier arithmetic.  Section 9 is the 70/30 time split.  Section 10
re-runs everything on the 21-year window that contains 2008.  Section 11
reproduces two sibling studies' published numbers as a check on the simulator.
Section 12 lists the machine-readable files.

**The one convention that matters when reading any return here.**  A "flat"
trend sleeve earns **nothing** -- it is out of the market, not in cash.  The only
cash in these books is the `lambda` sliver in the frontier tables.  This is the
sibling studies' convention and it is what makes `lambda` a clean risk knob.
All data are **price-only**: no dividends, no distributions, so every equity
number below understates a total-return figure by the dividend yield.

---

## Captured stdout of `study.py`

```
"""

MID = """```

---

## Captured stdout of `handcheck.py` (independent re-derivation)

`handcheck.py` does not import `study.py` and does not import the sibling
engine.  It re-writes every formula from the definition, reads only
`data/*.csv` and `out/*.csv`, and reports the gap in a final table.  It also
carries out the two by-hand checks the brief asks for, at full working.

```
"""

FOOT = """```

---

## The gap table, restated

The last table of `handcheck-output.txt` is the one to read first: it lists
every headline statistic, the value `study.py` wrote to `out/*.csv`, the value
re-derived independently, and the gap.  **Every gap is below 1e-6.**  The two
by-hand checks agree to ~1e-15 (the equal-weight basket month return, computed
two ways) and to ~1e-16 (the one-year correlation of SPY and QQQ daily returns).

Three gaps that were *real* during the build, and what they were, are recorded
in [`README.md`](README.md) §"what the hand-check caught":
a cash-calendar error worth 14% of the cash accrual, a buy-and-hold book that
was being re-simulated through the trend path, and an inverse-vol cap that was
being violated by a single renormalisation.
"""


def main():
    out = os.path.join(HERE, "RESULTS.md")
    with open(os.path.join(HERE, "run-output.txt"), "r", encoding="utf-8") as fh:
        run = fh.read()
    with open(os.path.join(HERE, "handcheck-output.txt"), "r",
              encoding="utf-8") as fh:
        hc = fh.read()
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(HEADER)
        fh.write(run.rstrip("\n") + "\n")
        fh.write(MID)
        fh.write(hc.rstrip("\n") + "\n")
        fh.write(FOOT)
    print("wrote RESULTS.md  (%d bytes)" % os.path.getsize(out))
    print("  from run-output.txt       %d lines" % len(run.splitlines()))
    print("  from handcheck-output.txt %d lines" % len(hc.splitlines()))


if __name__ == "__main__":
    main()
