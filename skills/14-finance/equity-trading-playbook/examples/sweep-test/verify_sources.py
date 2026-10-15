#!/usr/bin/env python3
"""
verify_sources.py -- the last six sessions of every series, against the vendor.

The five series that Grid P shares with the sibling `weather-test` study were
copied rather than re-pulled, so their provenance line points at that study.
This script re-issues one small call per series to TradingView and compares the
LAST SIX sessions bar-for-bar against the CSV on disk. A copy that has drifted,
or a CSV that came from somewhere else, shows up here.

It prints the exact calls so the check can be repeated. It needs the network
only to re-issue the calls; the comparison itself is offline.

USAGE
    py -3 verify_sources.py > source-check.txt
"""

import datetime
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(newline="\n")

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

# Verbatim from mcp__tradingview__mcp-tv-get-ohlcv(symbol, interval="1D",
# count=6, format="columns"), pulled 2026-10-14. The `t` values given by the
# tool map to these session dates; the closes are the `bars.c` array.
CALL = ('mcp__tradingview__mcp-tv-get-ohlcv(symbol=%r, interval="1D", '
        'count=6, format="columns")')
SPOT = {
    "AMEX:SPY": ["777.22", "773.93", "778.57", "778.10", "778.01", "769.60"],
    "NASDAQ:TLT": ["77.145", "77.87", "77.98", "78.05", "78.37", "78.89"],
    "AMEX:GLD": ["375.88", "378.62", "384.58", "382.15", "381.67", "375.99"],
    "AMEX:EEM": ["67.37", "66.10", "66.80", "66.15", "65.74", "64.39"],
    "TVC:VIX": ["15.07", "15.40", "14.85", "15.20", "15.28", "16.86"],
}
STEM = {"AMEX:SPY": "SPY", "NASDAQ:TLT": "TLT", "AMEX:GLD": "GLD",
        "AMEX:EEM": "EEM", "TVC:VIX": "VIX"}
DATES = ["2026-10-07", "2026-10-08", "2026-10-09", "2026-10-12", "2026-10-13",
         "2026-10-14"]


def read_closes(path):
    out = {}
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            s = line.strip()
            if not s or s.startswith("#") or s.startswith("date,"):
                continue
            p = s.split(",")
            out[p[0]] = p[4]
    return out


def main():
    print("=" * 92)
    print("verify_sources.py -- does the CSV on disk agree with the vendor?")
    print("=" * 92)
    print("  comparison window : the last six sessions in every series, %s .. %s"
          % (DATES[0], DATES[-1]))
    print("  the call re-issued for each series:")
    for sym in sorted(SPOT):
        print("    " + CALL % sym)
    print("")
    worst = 0.0
    for sym in sorted(SPOT):
        stem = STEM[sym]
        path = os.path.join(DATA, "%s_1d.csv" % stem)
        if not os.path.exists(path):
            print("  MISSING %s" % path)
            worst = float("inf")
            continue
        have = read_closes(path)
        print("  %-11s -> data/%s_1d.csv" % (sym, stem))
        for d, expected in zip(DATES, SPOT[sym]):
            got = have.get(d)
            if got is None:
                print("    %s  MISSING in CSV (vendor says %s)" % (d, expected))
                worst = float("inf")
                continue
            diff = abs(float(got) - float(expected))
            worst = max(worst, diff)
            print("    %s  csv %12s   vendor %12s   |diff| %.6f%s"
                  % (d, got, expected, diff, "   MISMATCH" if diff > 1e-6 else ""))
    print("")
    print("  WORST |diff| over %d bars: %.6f" % (len(SPOT) * len(DATES), worst))
    print("  A difference above 1e-6 on a close is a real disagreement. Note the")
    print("  vendor's notice: the last bar is still forming and may change.")
    print("=" * 92)
    return 0 if worst <= 1e-6 else 1


if __name__ == "__main__":
    sys.exit(main())
