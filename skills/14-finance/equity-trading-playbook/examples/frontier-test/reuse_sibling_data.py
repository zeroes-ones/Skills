#!/usr/bin/env python3
"""
reuse_sibling_data.py -- extend SPY_1d.csv back to 1993 from the sibling study's
already-pulled file, after verifying the overlap row-for-row.

WHY THIS EXISTS. A single get_ohlcv response is capped at 8000 bars, and the
host only persists a tool result to disk when it is big enough to be truncated.
SPY since 1993 is 8485 bars, so the 1993-01-29..1994-12-29 page (485 bars) came
back INLINE and was never written to a file. Re-issuing that page and hoping it
truncates is not a plan.

WHAT IT DOES INSTEAD. ../regime-study/data/SPY_1d.csv already holds SPY from
1993-01-29 to 2026-10-14, pulled from the same MCP tool on the same date, and
that study independently cross-checked its prices against a second broker
(see its README). So this script:

  1. re-pulls nothing;
  2. VERIFIES the sibling file against THIS study's own independent pull of the
     same symbol over the overlapping window (data/SPY_1d.csv, 8000 bars);
  3. refuses to proceed if any overlapping row disagrees, EXCEPT the very last
     bar, which the data source itself flags as still forming;
  4. writes the union (sibling rows before the overlap + this study's rows) to
     data/SPY_1d.csv with provenance that says exactly which rows came from
     where and what was verified.

The exception for the final bar is not a fudge: every one of the four symbols
cross-checked this way differed by exactly one row -- the last bar -- and only in
its volume, which is what "the last bar is still forming" means. Every other
number, in every other row, was identical.

USAGE
    py -3 reuse_sibling_data.py --dir . --sibling ../regime-study/data
"""

import argparse
import datetime
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(newline="\n")



def read_file(path):
    provenance, header, rows = [], None, []
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        for line in fh:
            if line.startswith("# PROVENANCE:"):
                provenance.append(line[len("# PROVENANCE:"):].rstrip("\r\n").strip())
                continue
            if line.startswith("#") or not line.strip():
                continue
            if line.startswith("date,"):
                header = line.rstrip("\r\n")
                continue
            rows.append(line.rstrip("\r\n"))
    if header is None:
        raise SystemExit("ERROR: no header row in %s" % path)
    return provenance, header, rows


def key_date(row):
    return datetime.date.fromisoformat(row.split(",")[0])


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True, help="this study's directory")
    ap.add_argument("--sibling", required=True,
                    help="directory holding the sibling study's <SYMBOL>_1d.csv")
    ap.add_argument("--symbol", default="SPY",
                    help="which series to extend (default SPY)")
    args = ap.parse_args(argv)

    FNAME = args.symbol + "_1d.csv"

    mine_path = os.path.join(args.dir, "data", FNAME)
    sib_path = os.path.join(args.sibling, FNAME)
    for p in (mine_path, sib_path):
        if not os.path.isfile(p):
            raise SystemExit("ERROR: missing %s" % p)

    sib_prov, header, sib_rows = read_file(sib_path)
    mine_prov, header2, mine_rows = read_file(mine_path)
    if header2 != header:
        raise SystemExit("ERROR: header mismatch: %r vs %r" % (header, header2))

    sib_by_date = {key_date(r): r for r in sib_rows}
    mine_by_date = {key_date(r): r for r in mine_rows}

    print("VERIFY OVERLAP")
    print("  sibling %s: %d rows, %s .. %s"
          % (os.path.relpath(sib_path), len(sib_rows),
             key_date(sib_rows[0]).isoformat(), key_date(sib_rows[-1]).isoformat()))
    print("  this study %s: %d rows, %s .. %s"
          % (os.path.relpath(mine_path), len(mine_rows),
             key_date(mine_rows[0]).isoformat(), key_date(mine_rows[-1]).isoformat()))

    overlap = sorted(set(sib_by_date) & set(mine_by_date))
    if len(overlap) < 1000:
        raise SystemExit("ERROR: overlap is only %d rows; refusing to merge"
                         % len(overlap))

    last_overlap = overlap[-1]
    mismatches = []
    last_bar_only = []
    for d in overlap:
        a, b = sib_by_date[d], mine_by_date[d]
        if a == b:
            continue
        if d == last_overlap:
            fa, fb = a.split(","), b.split(",")
            if fa[:5] == fb[:5]:
                last_bar_only.append((d, fa[5], fb[5]))
                continue
        mismatches.append((d, a, b))

    print("  overlapping rows:   %d" % len(overlap))
    print("  identical rows:     %d" % (len(overlap) - len(mismatches)
                                        - len(last_bar_only)))
    print("  last-bar exceptions:%d" % len(last_bar_only))
    for d, va, vb in last_bar_only:
        print("      %s volume differs (sibling %s vs this study %s) -- the final "
              "bar is still forming" % (d.isoformat(), va, vb))
    if mismatches:
        print("  MISMATCHES: %d" % len(mismatches))
        for d, a, b in mismatches[:10]:
            print("      %s\n        sibling %s\n        this    %s" % (d, a, b))
        raise SystemExit("ERROR: overlapping rows disagree; refusing to merge")

    extra_dates = sorted(set(sib_by_date) - set(mine_by_date))
    print("  rows only in the sibling file: %d (%s .. %s)"
          % (len(extra_dates),
             extra_dates[0].isoformat() if extra_dates else "-",
             extra_dates[-1].isoformat() if extra_dates else "-"))
    if not extra_dates:
        print("  nothing to add; the file already covers the sibling's window")
        return 0

    # Union: sibling rows that predate this study's own window, then this
    # study's own rows, untouched. The forming last bar therefore comes from
    # THIS study's pull, which is the copy the study actually read.
    merged = [sib_by_date[d] for d in extra_dates] + mine_rows
    dates = [key_date(r) for r in merged]
    if any(dates[i] >= dates[i + 1] for i in range(len(dates) - 1)):
        raise SystemExit("ERROR: merged dates are not strictly increasing")

    out = []
    out.append("# PROVENANCE: source=TradingView MCP tool "
               "mcp__tradingview__mcp-tv-get-ohlcv")
    for line in mine_prov:
        if line.startswith("symbol="):
            out.append("# PROVENANCE: %s" % line)
            break
    out.append("# PROVENANCE: assembled by pull_ohlcv.py + reuse_sibling_data.py")
    out.append("# PROVENANCE: rows=%d  first=%s  last=%s"
               % (len(merged), dates[0].isoformat(), dates[-1].isoformat()))
    out.append("# PROVENANCE: rows %s .. %s were RE-PULLED this session "
               "(%d rows, the 8000-bar page cap) by pull_ohlcv.py"
               % (key_date(mine_rows[0]).isoformat(),
                  key_date(mine_rows[-1]).isoformat(), len(mine_rows)))
    out.append("# PROVENANCE: rows %s .. %s were CARRIED from "
               "../regime-study/data/SPY_1d.csv (same tool, pulled 2026-10-14); "
               "that page came back inline and was never persisted"
               % (extra_dates[0].isoformat(), extra_dates[-1].isoformat()))
    out.append("# PROVENANCE: VERIFIED -- all %d overlapping rows are identical "
               "between the carried file and this session's own pull, except the "
               "final bar (%s), whose volume differs because the data source "
               "flags it as still forming"
               % (len(overlap), last_overlap.isoformat()))
    out.append("# PROVENANCE: split-adjusted, regular session only")
    out.append("# PROVENANCE: PRICE-ONLY series. No dividends or distributions. "
               "Not a total-return series.")
    out.append("# PROVENANCE: carried_from=%s" % os.path.relpath(
        sib_path, os.path.dirname(os.path.dirname(os.path.abspath(mine_path)))))
    out.append(header)
    out.extend(merged)

    with open(mine_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(out) + "\n")

    print("")
    print("WROTE %s  rows=%d  %s .. %s"
          % (os.path.relpath(mine_path), len(merged),
             dates[0].isoformat(), dates[-1].isoformat()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
