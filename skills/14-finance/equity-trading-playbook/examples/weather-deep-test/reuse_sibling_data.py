#!/usr/bin/env python3
"""
reuse_sibling_data.py -- extend this study's own pull of a symbol with the
longer history already on disk from a sibling study, after verifying the
overlap row-for-row.

WHY THIS EXISTS.  A single get_ohlcv response caps at 8000 bars and the host
only persists a tool result to disk when it is big enough to be truncated.
SPY since 1993 is 8485 bars, so re-issuing the request yields the SAME 8000
trailing bars -- there is no way to page further back for a 1D series, because
`date_to=next_date_to` only pages when `has_more` is true and for a symbol with
more history than the cap the cap simply truncates the OLD end.

WHAT IT DOES.  ../frontier-test/data/SPY_1d.csv already holds SPY from
1993-01-29, pulled from the same MCP tool on the same date, and that study
independently cross-checked its prices against a second broker (see its README).
So this script:

  1. re-pulls nothing;
  2. VERIFIES the sibling file against THIS study's own independent pull of the
     same symbol over the overlapping window;
  3. refuses to proceed if any overlapping row disagrees, EXCEPT the very last
     bar, which the data source itself flags as still forming;
  4. writes the union to <out>/<NAME>_1d.csv with provenance naming exactly
     which rows came from where.

USAGE
    py -3 reuse_sibling_data.py --data data --sibling ../frontier-test/data --name SPY
"""

import argparse
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


def split_rows(rows):
    out = {}
    order = []
    for r in rows:
        key = r.split(",", 1)[0]
        out[key] = r
        order.append(key)
    return out, order


def price_part(row):
    """date,o,h,l,c,v -> the first five fields (everything but volume)."""
    return ",".join(row.split(",")[:5])


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, help="this study's data dir")
    ap.add_argument("--sibling", required=True, help="sibling study's data dir")
    ap.add_argument("--name", required=True, help="file stem, e.g. SPY")
    ap.add_argument("--note", default="", help="what this reuse is for")
    args = ap.parse_args(argv)

    mine_path = os.path.join(args.data, args.name + "_1d.csv")
    sib_path = os.path.join(args.sibling, args.name + "_1d.csv")

    sib_prov, sib_header, sib_rows = read_file(sib_path)
    my_prov, my_header, my_rows = read_file(mine_path)
    if sib_header != my_header:
        raise SystemExit("ERROR: header mismatch: %r vs %r" % (sib_header, my_header))

    sib, sib_order = split_rows(sib_rows)
    mine, my_order = split_rows(my_rows)

    overlap = [d for d in my_order if d in sib]
    print("VERIFY OVERLAP")
    print("  sibling %s: %d rows, %s .. %s"
          % (sib_path, len(sib_order), sib_order[0], sib_order[-1]))
    print("  this study %s: %d rows, %s .. %s"
          % (mine_path, len(my_order), my_order[0], my_order[-1]))
    print("  overlapping dates: %d" % len(overlap))

    identical, last_bar_exceptions, disagreements = 0, [], []
    last_date = my_order[-1]
    for d in overlap:
        if sib[d] == mine[d]:
            identical += 1
        elif d == last_date and price_part(sib[d]) == price_part(mine[d]):
            last_bar_exceptions.append(
                "      %s volume differs (sibling %s vs this study %s) -- the "
                "final bar is still forming"
                % (d, sib[d].split(",")[-1], mine[d].split(",")[-1]))
        else:
            disagreements.append("      %s: %r vs %r" % (d, sib[d], mine[d]))
    print("  identical rows:      %d" % identical)
    print("  last-bar exceptions: %d" % len(last_bar_exceptions))
    for line in last_bar_exceptions:
        print(line)
    if disagreements:
        print("  DISAGREEMENTS: %d" % len(disagreements))
        for line in disagreements[:20]:
            print(line)
        raise SystemExit("ERROR: sibling and this study disagree on real rows; "
                         "refusing to merge")

    only_sib = [d for d in sib_order if d not in mine]
    print("  rows only in the sibling file: %d (%s .. %s)"
          % (len(only_sib), only_sib[0] if only_sib else "-",
             only_sib[-1] if only_sib else "-"))
    if not only_sib:
        print("  nothing to add")
        return 0

    merged = [sib[d] for d in only_sib] + [mine[d] for d in my_order]
    lines = []
    lines.append("# PROVENANCE: source=TradingView MCP tool "
                 "mcp__tradingview__mcp-tv-get-ohlcv")
    lines.append("# PROVENANCE: symbol reassembled from TWO files: %s "
                 "(rows before %s) + %s (rows from %s on)"
                 % (os.path.basename(sib_path), my_order[0],
                    os.path.basename(mine_path), my_order[0]))
    lines.append("# PROVENANCE: reuse_note=%s" % (args.note or "n/a"))
    lines.append("# PROVENANCE: overlap_verified: %d overlapping dates, %d "
                 "identical, %d last-bar volume-only exception(s), 0 "
                 "disagreements" % (len(overlap), identical,
                                    len(last_bar_exceptions)))
    for p in sib_prov:
        lines.append("# PROVENANCE: sibling: " + p)
    for p in my_prov:
        lines.append("# PROVENANCE: this-study: " + p)
    lines.append("# PROVENANCE: rows=%d  first=%s  last=%s"
                 % (len(merged), merged[0].split(",")[0],
                    merged[-1].split(",")[0]))
    lines.append("# PROVENANCE: PRICE-ONLY series. No dividends or "
                 "distributions. Not a total-return series.")
    lines.append(sib_header)
    for r in merged:
        lines.append(r)
    with open(mine_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    print("")
    print("WROTE %s  rows=%d  %s .. %s"
          % (mine_path, len(merged), merged[0].split(",")[0],
             merged[-1].split(",")[0]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
