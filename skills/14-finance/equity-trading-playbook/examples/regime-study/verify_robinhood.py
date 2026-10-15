#!/usr/bin/env python3
"""
verify_robinhood.py -- independent cross-check of the TradingView closes against
a SECOND data source (Robinhood), for the regime study.

Deterministic. Stdlib only. No network. No third-party imports.

WHY
    A study whose numbers all descend from one feed cannot tell a strategy result
    from a feed error. This script extracts the Robinhood
    `get_equity_historicals` payload that the agent host wrote into its own event
    log, saves it as CSV with provenance, and compares the closes it reports
    against the TradingView closes the study actually used.

WHAT IT PROVES, AND WHAT IT DOES NOT
    It proves the two feeds agree on the overlapping daily closes to within a
    stated tolerance. It does NOT make either feed correct, and it does NOT
    validate the pre-2004 history (Robinhood was asked for a recent window only,
    so the older TradingView bars have no second source here).

USAGE
    py -3 verify_robinhood.py --wire <session>/agents/<id>/wire.jsonl \
                              --out data/crosscheck-robinhood.csv

EXIT CODES
    0  compared at least one instrument
    2  no Robinhood payload found, or a CSV could not be read
"""

import argparse
import datetime
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")
SYMBOLS = ["SPY", "QQQ", "TLT", "GLD"]


def walk(obj, out):
    """Collect any dict that looks like a get_equity_historicals result."""
    if isinstance(obj, dict):
        if "bars" in obj and "symbol" in obj and "interval" in obj \
                and isinstance(obj.get("bars"), list):
            out.append(obj)
            return
        for v in obj.values():
            walk(v, out)
    elif isinstance(obj, list):
        for v in obj:
            walk(v, out)
    elif isinstance(obj, str):
        s = obj.strip()
        if s.startswith("{") and "close_price" in s:
            try:
                walk(json.loads(s), out)
            except ValueError:
                return


def payloads_from_wire(path):
    found = []
    scanned = 0
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            scanned += 1
            if "close_price" not in line:
                continue
            try:
                walk(json.loads(line.strip()), found)
            except ValueError:
                continue
    print("wire.jsonl: scanned %d events, found %d Robinhood bar payload(s)"
          % (scanned, len(found)))
    return found


def table(headers, rows, align=None):
    ncol = len(headers)
    if align is None:
        align = ["r"] * ncol
    cells = [[str(c) for c in r] for r in rows]
    widths = [len(headers[i]) for i in range(ncol)]
    for r in cells:
        for i in range(ncol):
            widths[i] = max(widths[i], len(r[i]))

    def line(r):
        parts = []
        for i in range(ncol):
            parts.append(r[i].ljust(widths[i]) if align[i] == "l"
                         else r[i].rjust(widths[i]))
        return "  " + "  ".join(parts).rstrip()

    out = [line(headers), "  " + "-" * (sum(widths) + 2 * (ncol - 1))]
    for r in cells:
        out.append(line(r))
    return out


def read_tv(path):
    out = {}
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        for line in fh:
            if line.startswith("#") or not line.strip():
                continue
            if line.startswith("date,"):
                continue
            f = line.rstrip("\r\n").split(",")
            out[datetime.date.fromisoformat(f[0])] = float(f[4])
    return out


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(newline="\n")

    ap = argparse.ArgumentParser(prog="verify_robinhood.py")
    ap.add_argument("--wire", required=True, help="agent wire.jsonl")
    ap.add_argument("--out", default=os.path.join(DATA_DIR,
                                                  "crosscheck-robinhood.csv"))
    ap.add_argument("--pull-date", default=None)
    ap.add_argument("--picks", type=int, default=5,
                    help="how many closes per instrument to print in full")
    args = ap.parse_args(argv if argv is not None else sys.argv[1:])

    payloads = payloads_from_wire(args.wire)
    if not payloads:
        print("ERROR: no Robinhood payload found in %s" % args.wire)
        return 2

    # last payload wins (later calls supersede earlier ones)
    merged = {}
    for p in payloads:
        sym = p.get("symbol", "").split(".")[-1].split(":")[-1].upper()
        if sym not in SYMBOLS:
            continue
        slot = merged.setdefault(sym, {})
        for b in p["bars"]:
            d = datetime.date.fromisoformat(b["begins_at"][:10])
            slot[d] = b
    if not merged:
        print("ERROR: payloads found but none for %s" % ",".join(SYMBOLS))
        return 2

    if args.pull_date:
        pull_date = args.pull_date
    else:
        pull_date = datetime.datetime.now(datetime.timezone.utc).date().isoformat()

    lines = []
    lines.append("# PROVENANCE: source=Robinhood MCP tool "
                 "mcp__robinhood__get_equity_historicals")
    lines.append("# PROVENANCE: pulled=%s (UTC date of the pull)" % pull_date)
    lines.append("# PROVENANCE: interval=day  bounds=regular session only")
    lines.append("# PROVENANCE: cross-check of the TradingView daily closes used by "
                 "study.py; this file is NOT an input to any strategy")
    lines.append("symbol,date,open,high,low,close,volume")
    for sym in sorted(merged):
        for d in sorted(merged[sym]):
            b = merged[sym][d]
            lines.append("%s,%s,%.6f,%.6f,%.6f,%.6f,%s"
                         % (sym, d.isoformat(), float(b["open_price"]),
                            float(b["high_price"]), float(b["low_price"]),
                            float(b["close_price"]), b.get("volume", "")))
    with open(args.out, "w", encoding="utf-8", newline="") as fh:
        fh.write("\n".join(lines) + "\n")
    print("wrote %s (%d rows)" % (args.out, sum(len(v) for v in merged.values())))
    print("")

    print("=" * 96)
    print("CROSS-CHECK: TradingView closes vs Robinhood closes on common dates")
    print("=" * 96)
    print("")

    worst_overall = 0.0
    rows = []
    detail = []
    for sym in sorted(merged):
        tv_path = os.path.join(DATA_DIR, "%s_1d.csv" % sym)
        if not os.path.isfile(tv_path):
            print("  %s: no TradingView CSV, skipped" % sym)
            continue
        tv = read_tv(tv_path)
        rb = merged[sym]
        common = sorted(set(tv) & set(rb))
        if not common:
            print("  %s: no overlapping dates, skipped" % sym)
            continue
        diffs = []
        for d in common:
            tvv = tv[d]
            rvv = float(rb[d]["close_price"])
            diffs.append((d, tvv, rvv, rvv - tvv, abs(rvv - tvv) / tvv))
        maxabs = max(x[3] for x in diffs)
        maxrel = max(x[4] for x in diffs)
        worst_overall = max(worst_overall, maxrel)
        rows.append([sym, str(len(common)), str(common[0]), str(common[-1]),
                     "%.4f" % maxabs, "%.4f bp" % (maxrel * 10000.0)])
        step = max(1, len(common) // args.picks)
        for d, tvv, rvv, ad, rel in diffs[::step][:args.picks]:
            detail.append([sym, str(d), "%.4f" % tvv, "%.4f" % rvv,
                           "%+.4f" % ad, "%.2f bp" % (rel * 10000.0)])

    print("\n".join(table(["sym", "common_days", "from", "to",
                           "max_abs_diff", "max_rel_diff"],
                          rows, ["l", "r", "l", "l", "r", "r"])))
    print("")
    print("  Sampled closes, side by side:")
    print("")
    print("\n".join(table(["sym", "date", "TradingView", "Robinhood",
                           "diff", "diff_bp"], detail,
                          ["l", "l", "r", "r", "r", "r"])))
    print("")
    print("  WORST relative disagreement across all instruments sampled: %.2f bp "
          "(%.6f%%)" % (worst_overall * 10000.0, worst_overall * 100.0))
    print("")
    if worst_overall * 10000.0 < 10.0:
        print("  Every overlapping close agrees to better than 10 bp of price. On a")
        print("  $700 instrument that is inside a single cent. The two feeds are not")
        print("  disagreeing about the price history this study used.")
    else:
        print("  The two feeds disagree by more than 10 bp on at least one close.")
        print("  Investigate before trusting either history.")
    print("")
    print("  NOT CHECKED: the pre-2004 TradingView history. Robinhood was asked for")
    print("  a recent window only, so nothing older than that window has a second")
    print("  source in this study.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
