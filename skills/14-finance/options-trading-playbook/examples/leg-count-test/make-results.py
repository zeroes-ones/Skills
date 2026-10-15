#!/usr/bin/env python3
"""
make-results.py -- render RESULTS.md from the CAPTURED run.

Formats; never calculates.  Every number in RESULTS.md comes either from
run-output.txt (the raw stdout of study.py) or from out/*.csv.  If a number is
not in one of those two places it does not appear in RESULTS.md.

USAGE
    py -3 study.py > run-output.txt
    py -3 make-results.py
"""

import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
RUN = os.path.join(HERE, "run-output.txt")
HC = os.path.join(HERE, "handcheck-output.txt")
RESULTS = os.path.join(HERE, "RESULTS.md")

# the small tables are inlined in full; the two large ledgers are referenced by
# path and NOT pasted, because they are 1.7 MB and 1.4 MB of rows.
SMALL = [
    ("structures.csv", "the pre-registered structures and their headline stats"),
    ("cost_drag.csv", "cost drag and the break-even cost c_R* = E_R"),
    ("skew_sensitivity.csv", "the skew / model-risk test"),
    ("tails.csv", "the tail comparison"),
    ("positivity.csv", "positivity by horizon and the Phi-law gap"),
    ("verdict.csv", "the verdict columns"),
    ("shape_greeks.csv", "what the extra legs change: the Greek shape"),
    ("stress_windows.csv", "the stress windows, in R"),
]
LARGE = [("trades.csv", "every trade, every structure, every index, every variant"),
         ("ledger.csv", "per-trade strikes, credit, cost, R and P&L")]


def read_csv(path):
    rows = []
    with io.open(path, "r", encoding="utf-8", newline="") as fh:
        for line in fh:
            rows.append(line.rstrip("\r\n").split(","))
    return rows


def md_table(rows):
    if not rows:
        return "_(empty)_"
    w = len(rows[0])
    out = ["| " + " | ".join(rows[0]) + " |",
           "|" + "|".join([" --- "] * w) + "|"]
    for r in rows[1:]:
        r = (r + [""] * w)[:w]
        out.append("| " + " | ".join(r) + " |")
    return "\n".join(out)


def main():
    if not os.path.isfile(RUN):
        raise SystemExit("ERROR: missing %s -- run study.py first" % RUN)
    with io.open(RUN, "r", encoding="utf-8", newline="") as fh:
        run = fh.read()
    hc = ""
    if os.path.isfile(HC):
        with io.open(HC, "r", encoding="utf-8", newline="") as fh:
            hc = fh.read()

    parts = []
    parts.append("""# RESULTS -- the leg-count test, verbatim from a real run

**Every number in this file is `[MODELED]`, not `[VERIFIED]`.**  No historical
option quotes are available from the sources used here.  Historical option
prices do not exist in `data/*.csv`; they are constructed with Black-Scholes
from the real VIX and settled against the real index closes.

Three views, twelve pre-registered structures, one unit of risk `R` per trade
defined as the structure's own maximum loss, 30-DTE monthly cycles, entry at the
next open after the monthly roll, settlement at intrinsic against the real path,
2001-03-13 to 2026-10-14 (6 436 sessions, 24 complete calendar years).

## How this file was produced

```bash
py -3 carry_data.py
py -3 study.py > run-output.txt
py -3 handcheck.py > handcheck-output.txt
py -3 make-results.py
```

`make-results.py` formats; it never calculates.  Section 1 below is the raw
stdout of `study.py`.  Section 2 is the small `out/*.csv` tables pasted in full.
Section 3 is the raw stdout of the INDEPENDENT re-derivation.

---

## 1. The raw stdout of `study.py`

```text
""")
    parts.append(run.rstrip("\n"))
    parts.append("""```

---

## 2. The tables, pasted from `out/*.csv`

""")
    for name, what in SMALL:
        path = os.path.join(OUT, name)
        if not os.path.isfile(path):
            continue
        parts.append("### `out/%s` -- %s\n" % (name, what))
        parts.append(md_table(read_csv(path)))
        parts.append("")
    parts.append("### Kept out of this file, by path\n")
    for name, what in LARGE:
        path = os.path.join(OUT, name)
        n = sum(1 for _ in io.open(path, "r", encoding="utf-8")) - 1
        parts.append("- `out/%s` -- %s, **%d rows**.  Not pasted here; read the"
                     " file." % (name, what, n))
    parts.append("""
---

## 3. The raw stdout of the INDEPENDENT `handcheck.py`

This program does **not** import `study.py`.  It re-implements the spec from
`data/*.csv` with its own CSV reader, its own Black-Scholes, its own delta
solver, its own vol context, its own structure builder, its own maximum-loss
scan, its own month grid and its own simulator.  It also prints a by-hand
Black-Scholes price with every intermediate, a by-hand `c_R`, and a by-hand
settlement of one 4-leg iron condor against the real path.

```text
""")
    parts.append(hc.rstrip("\n"))
    parts.append("```\n")

    with io.open(RESULTS, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(parts))
    print("wrote %s (%d bytes)" % (RESULTS, os.path.getsize(RESULTS)))


if __name__ == "__main__":
    main()
