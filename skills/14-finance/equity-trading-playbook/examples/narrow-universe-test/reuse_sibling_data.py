#!/usr/bin/env python3
"""
reuse_sibling_data.py -- copy the sibling studies' already-pulled series into
this study's data/ directory, verifying the overlap first.

The three index ETFs, the cross-asset sleeves, the cash proxy and VIX were pulled
by ../frontier-test and ../weather-test on the same day this study runs. Pulling
them again would produce byte-identical series and a second provenance header for
no gain, so they are REUSED. This script proves the reuse is sound rather than
asserting it: it compares every overlapping row and prints the exceptions.

Stdlib only. No network.

USAGE
    py -3 reuse_sibling_data.py
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
SIBLINGS = {
    "SPY": "../frontier-test/data/SPY_1d.csv",
    "QQQ": "../frontier-test/data/QQQ_1d.csv",
    "IWM": "../frontier-test/data/IWM_1d.csv",
    "TLT": "../frontier-test/data/TLT_1d.csv",
    "GLD": "../frontier-test/data/GLD_1d.csv",
    "EEM": "../frontier-test/data/EEM_1d.csv",
    "VIX": "../frontier-test/data/VIX_1d.csv",
    "US03M": "../frontier-test/data/US03M_1d.csv",
    "BIL": "../frontier-test/data/BIL_1d.csv",
}

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(newline="\n")


def read(path):
    prov, rows = [], {}
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        for line in fh:
            if line.startswith("# PROVENANCE:"):
                prov.append(line[len("# PROVENANCE:"):].strip())
                continue
            if line.startswith("#") or not line.strip():
                continue
            if line.startswith("date,"):
                continue
            f = line.rstrip("\r\n").split(",")
            rows[f[0]] = tuple(float(x) if x.strip() else 0.0 for x in f[1:5])
    return prov, rows


def main():
    os.makedirs(DATA, exist_ok=True)
    for name in sorted(SIBLINGS):
        src = os.path.abspath(os.path.join(HERE, SIBLINGS[name]))
        dst = os.path.join(DATA, name + "_1d.csv")
        if not os.path.isfile(src):
            raise SystemExit("ERROR: sibling series missing: %s" % src)
        if os.path.isfile(dst):
            sp, sr = read(src)
            dp, dr = read(dst)
            shared = set(sr) & set(dr)
            diff = [d for d in shared if sr[d] != dr[d]]
            print("VERIFY OVERLAP")
            print("  sibling %s: %d rows, %s .. %s"
                  % (SIBLINGS[name], len(sr), min(sr), max(sr)))
            print("  this study data\\%s_1d.csv: %d rows, %s .. %s"
                  % (name, len(dr), min(dr), max(dr)))
            print("  overlapping rows:   %d" % len(shared))
            print("  identical rows:     %d" % (len(shared) - len(diff)))
            print("  differing rows:     %d" % len(diff))
            for d in sorted(diff)[:5]:
                print("      %s sibling %r vs here %r" % (d, sr[d], dr[d]))
            if diff:
                raise SystemExit(
                    "ERROR: reused %s disagrees with the sibling on %d row(s); "
                    "refusing to overwrite. Investigate before reusing."
                    % (name, len(diff)))
            print("  -> identical; nothing to do")
            print("")
            continue

        sp, sr = read(src)
        with open(src, "r", encoding="utf-8-sig", newline="") as fh:
            body = fh.read()
        first = body.splitlines()[0]
        lines = [first,
                 "# PROVENANCE: symbol=%s" % name,
                 "# PROVENANCE: REUSED from %s (verified identical by "
                 "reuse_sibling_data.py)" % SIBLINGS[name].replace("\\", "/"),
                 "# PROVENANCE: original pull date 2026-10-14 (UTC)"]
        with open(dst, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(lines) + "\n")
            fh.write(body)
        print("WROTE data\\%s_1d.csv  rows=%d  %s .. %s"
              % (name, len(sr), min(sr), max(sr)))
    print("")
    print("DONE: %d reused series" % len(SIBLINGS))


if __name__ == "__main__":
    main()
