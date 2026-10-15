#!/usr/bin/env python3
"""
make-results.py -- render RESULTS.md from a REAL run.

It formats; it never calculates.  Everything in RESULTS.md comes either from
`run-output.txt` (the captured stdout of `study.py`) or from `out/*.csv`.  If a
number is not in one of those two places it does not appear in RESULTS.md.

USAGE
    py -3 make-results.py
"""

import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.join(HERE, "run-output.txt")
OUT = os.path.join(HERE, "out")
DEST = os.path.join(HERE, "RESULTS.md")
HAND = os.path.join(HERE, "handcheck-output.txt")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(newline="\n")

CSV_ORDER = [
    ("headline.csv", "Headline book metrics"),
    ("trade_stats.csv", "Trade-level statistics"),
    ("positivity_by_horizon.csv", "Positivity by horizon"),
    ("frontier.csv", "The lambda frontier"),
    ("frontier_end.csv", "Where the frontier ends"),
    ("correlation.csv", "Correlation of the three indices"),
    ("cost_sensitivity.csv", "Cost sensitivity"),
    ("skew_sensitivity.csv", "Skew sensitivity"),
    ("iv_stress.csv", "IV and term-structure stress"),
    ("dividend_sensitivity.csv", "Dividend sensitivity"),
    ("vrp.csv", "VRP by 21-day window (SPY, 1990-2026)"),
    ("s2_structure.csv", "Per-trade option structure (S2 and S4)"),
    ("spy_only.csv", "SPY-only, longest window"),
]


def read(path):
    with io.open(path, "r", encoding="utf-8", newline="") as fh:
        return fh.read()


def fence(text, lang=""):
    return "```%s\n%s```\n" % (lang, text if text.endswith("\n") else text + "\n")


def main():
    for p in (RUN,):
        if not os.path.isfile(p):
            raise SystemExit("ERROR: %s missing -- run study.py first" % p)

    run = read(RUN)
    parts = []
    parts.append("""# index-options-test -- RESULTS

Every table below is pasted verbatim from a real run of `study.py`
(`run-output.txt`), or dumped from `out/*.csv`.  Nothing here was retyped.

> ## READ THIS BEFORE ANY NUMBER
>
> **Every option price in this study is `[MODELED]`, not `[VERIFIED]`.**
> Historical option quotes are not available from the sources used here.
> Each leg is priced with Black-Scholes on an implied vol built from the real
> VIX series, and each spread is settled at intrinsic against the REAL index
> closing price on its expiry session.
>
> The option model cannot see, and therefore does not price:
>
> 1. **any bid/ask spread in the quote** -- a flat per-contract spread IS
>    charged as a COST, but the quote itself is a mid;
> 2. **skew** -- one implied vol prices every strike, so the sold leg is priced
>    at the same vol as the wings; a sensitivity on this is section 13c;
> 3. **term structure** -- the primary run prices the 30-DTE spread and the
>    60-DTE hedge at the same vol; a `sqrt(30/D)` variant is reported;
> 4. **early exercise and assignment** -- these are AMERICAN, physically settled
>    products, priced here as EUROPEAN;
> 5. **pin risk** -- the expiry session's close decides everything;
> 6. **dividends** -- the price series is price-only; a sensitivity is section 13b;
> 7. **margin, buying power, liquidity, partial fills, legging risk, tax**;
> 8. **overlapping monthly structures** -- the tenor is capped at the next roll,
>    so a monthly programme never holds two cycles at once.

---

## The run

""")
    parts.append(fence(run))
    parts.append("\n---\n\n## Artefact tables (`out/*.csv`)\n")
    for name, title in CSV_ORDER:
        path = os.path.join(OUT, name)
        if not os.path.isfile(path):
            continue
        body = read(path)
        lines = body.split("\n")
        n = len([ln for ln in lines if ln.strip()]) - 1
        parts.append("### %s -- `out/%s` (%d rows)\n\n" % (title, name, n))
        if name == "vrp.csv" and n > 40:
            parts.append("First 25 rows only; the full file is on disk.\n\n")
            parts.append(fence("\n".join(lines[:26])))
        else:
            parts.append(fence(body))

    if os.path.isfile(HAND):
        parts.append("\n---\n\n## Independent re-derivation (`handcheck.py`)\n\n")
        parts.append(fence(read(HAND)))

    with io.open(DEST, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("".join(parts))
    print("wrote RESULTS.md (%d bytes)" % os.path.getsize(DEST))
    return 0


if __name__ == "__main__":
    sys.exit(main())
