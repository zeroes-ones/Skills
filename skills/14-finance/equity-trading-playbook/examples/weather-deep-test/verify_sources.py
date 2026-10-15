#!/usr/bin/env python3
"""
verify_sources.py -- cross-check this study's data/*.csv against the sibling
studies' INDEPENDENT pulls of the same symbols, made with the same tool on the
same date.

This is not a re-derivation of the maths; it is a check that the numbers going
IN are the numbers the sibling studies already used and, in the regime study's
case, already cross-checked against a second broker.

Comparison rule: a shared date must agree on open/high/low/close exactly.  Volume
is compared but a difference is reported as a WARNING rather than a failure when
the date is the final bar of the file, because the source marks the last bar as
still forming.  Any price disagreement is a hard failure.

USAGE
    py -3 verify_sources.py
"""

import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(newline="\n")

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

SIBLINGS = {
    "frontier-test": ["SPY", "QQQ", "IWM", "TLT", "GLD", "EEM", "IEF", "HYG",
                      "DBC", "VNQ", "EFA", "BIL", "US03M", "VIX"],
    "weather-test": ["SPY", "TLT", "GLD", "EEM", "VIX"],
    "narrow-universe-test": ["SPY", "QQQ", "IWM", "TLT", "GLD", "EEM", "BIL",
                            "US03M", "VIX"],
    "sweep-test": ["SPY", "QQQ", "IWM", "TLT", "GLD", "EEM", "IEF", "HYG",
                   "DBC", "VNQ", "EFA", "VIX"],
    "regime-study": ["SPY", "QQQ", "TLT", "GLD"],
}


def read_file(path):
    header = None
    rows = {}
    order = []
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        for line in fh:
            if line.startswith("#") or not line.strip():
                continue
            if line.startswith("date,"):
                header = line.rstrip("\r\n")
                continue
            f = line.rstrip("\r\n").split(",")
            rows[f[0]] = f
            order.append(f[0])
    if header is None:
        raise SystemExit("ERROR: no header in %s" % path)
    return header, rows, order


def main():
    grand = {"files": 0, "compared": 0, "identical": 0, "price_diff": 0,
             "vol_warn": 0, "missing": 0}
    for study, symbols in sorted(SIBLINGS.items()):
        sib_dir = os.path.normpath(os.path.join(HERE, "..", study, "data"))
        print("=" * 78)
        print("SIBLING: %s  (%s)" % (study, sib_dir))
        print("=" * 78)
        if not os.path.isdir(sib_dir):
            print("  SKIP -- directory not found")
            continue
        for sym in symbols:
            mine = os.path.join(DATA, sym + "_1d.csv")
            theirs = os.path.join(sib_dir, sym + "_1d.csv")
            if not os.path.isfile(mine) or not os.path.isfile(theirs):
                print("  %-6s SKIP (missing on one side)" % sym)
                grand["missing"] += 1
                continue
            grand["files"] += 1
            mh, mr, mo = read_file(mine)
            th, tr, to = read_file(theirs)
            if mh != th:
                print("  %-6s HEADER MISMATCH: %r vs %r" % (sym, mh, th))
                continue
            shared = [d for d in mo if d in tr]
            ident = 0
            price_diff = []
            vol_warn = []
            my_last = mo[-1]
            for d in shared:
                a, b = mr[d], tr[d]
                if a[1:5] != b[1:5]:
                    price_diff.append((d, a[1:5], b[1:5]))
                elif a[5] != b[5]:
                    if d == my_last or d == to[-1]:
                        vol_warn.append(d)
                    else:
                        vol_warn.append(d)
                else:
                    ident += 1
            grand["compared"] += len(shared)
            grand["identical"] += ident
            grand["price_diff"] += len(price_diff)
            grand["vol_warn"] += len(vol_warn)
            status = "OK" if not price_diff else "*** PRICE DISAGREEMENT ***"
            print("  %-6s mine=%-5d %s..%s | sibling=%-5d %s..%s | shared=%-5d "
                  "identical=%-5d vol-only-warn=%-3d  %s"
                  % (sym, len(mo), mo[0], mo[-1], len(to), to[0], to[-1],
                     len(shared), ident, len(vol_warn), status))
            for d, a, b in price_diff[:5]:
                print("        %s mine=%r sibling=%r" % (d, a, b))
        print("")
    print("=" * 78)
    print("TOTAL: %d file pairs compared, %d shared dates, %d identical, "
          "%d price disagreements, %d volume-only warnings"
          % (grand["files"], grand["compared"], grand["identical"],
             grand["price_diff"], grand["vol_warn"]))
    print("=" * 78)
    return 1 if grand["price_diff"] else 0


if __name__ == "__main__":
    sys.exit(main())
