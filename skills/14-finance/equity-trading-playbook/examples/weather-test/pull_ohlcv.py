#!/usr/bin/env python3
"""
pull_ohlcv.py -- MCP-payload-on-disk -> CSV, with provenance headers.

Stdlib only. No network of its own.

The agent host persists every large MCP tool result to
    <session>/agents/<id>/tool-results/mcp__tradingview__mcp-tv-get-ohlcv-*.txt
as one JSON payload per call. This script reads those bytes and turns them into
the CSV form the sibling studies use: a `date,open,high,low,close,volume` table
behind a `# PROVENANCE:` header. It never calls the network; re-issuing the MCP
calls is a separate, manual step documented in README.md.

PAGES.  A single get_ohlcv response holds at most 8000 bars in column form.
A symbol with more history comes back as several pages; this script groups the
payloads by their own `symbol` field, merges the pages, de-duplicates on the
session date and refuses to merge two pages that disagree on a shared date.

USAGE
    py -3 pull_ohlcv.py --results <tool-results dir> --out data \
        --pull-date 2026-10-14 [--only VIX,EEM]
"""

import argparse
import datetime
import glob
import json
import os
import sys

# The two studies that share this data directory use these names. The file name
# is the symbol the rest of the toolchain expects; the source symbol is what the
# data source was asked for.
FILENAME_FOR_SYMBOL = {
    "AMEX:SPY": "SPY",
    "NASDAQ:QQQ": "QQQ",
    "NASDAQ:TLT": "TLT",
    "AMEX:GLD": "GLD",
    "AMEX:EEM": "EEM",
    "TVC:VIX": "VIX",
}

HEADER_FIELDS = "date,open,high,low,close,volume"


# The repo requires LF everywhere. Redirected stdout on Windows would otherwise
# translate every newline to CRLF, which fails the file-format gate.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(newline="\n")


def utc_date(ts):
    """Session date = the UTC calendar date of the bar timestamp."""
    return datetime.datetime.fromtimestamp(int(ts), datetime.timezone.utc).date()


def load_payloads(results_dir):
    """Return {source_symbol: [payload, ...]} for every get_ohlcv payload found."""
    pattern = os.path.join(results_dir, "mcp__tradingview__mcp-tv-get-ohlcv-*.txt")
    paths = sorted(glob.glob(pattern), key=os.path.getmtime)
    if not paths:
        raise SystemExit("ERROR: no get_ohlcv payloads under %s" % results_dir)

    by_symbol = {}
    order = []
    for path in paths:
        with open(path, "r", encoding="utf-8") as fh:
            raw = fh.read()
        try:
            payload = json.loads(raw)
        except ValueError as exc:
            print("  SKIP (not JSON: %s) %s" % (exc, os.path.basename(path)))
            continue
        if not payload.get("success"):
            print("  SKIP (success=false) %s" % os.path.basename(path))
            continue
        sym = payload.get("symbol")
        if sym not in FILENAME_FOR_SYMBOL:
            print("  SKIP (unmapped symbol %r) %s" % (sym, os.path.basename(path)))
            continue
        by_symbol.setdefault(sym, []).append((path, payload))
        order.append(sym)
    return by_symbol


def merge_symbol(source_symbol, pages):
    """Merge the pages of one symbol into a single date-sorted bar table."""
    bars = {}
    page_report = []
    for path, payload in pages:
        b = payload["bars"]
        n = len(b["t"])
        page_report.append((os.path.basename(path), n, payload.get("has_more")))
        for i in range(n):
            d = utc_date(b["t"][i])
            row = (float(b["o"][i]), float(b["h"][i]), float(b["l"][i]),
                   float(b["c"][i]), b["v"][i])
            if d in bars:
                prev = bars[d]
                if (prev[0], prev[1], prev[2], prev[3]) != row[:4]:
                    raise SystemExit(
                        "ERROR: %s has two pages that disagree on %s: %r vs %r"
                        % (source_symbol, d.isoformat(), prev[:4], row[:4]))
                continue
            bars[d] = row
    interval = pages[0][1].get("interval", "1D")
    return bars, page_report, interval


def write_csv(path, source_symbol, bars, pages, interval, pull_date,
              extra_provenance):
    dates = sorted(bars.keys())
    first, last = dates[0], dates[-1]
    lines = []
    lines.append("# PROVENANCE: source=TradingView MCP tool "
                 "mcp__tradingview__mcp-tv-get-ohlcv")
    lines.append("# PROVENANCE: symbol=%s  interval=%s  fields=OHLCV"
                 % (source_symbol, interval))
    lines.append("# PROVENANCE: pulled=%s (UTC date of the pull)" % pull_date)
    lines.append("# PROVENANCE: split-adjusted, regular session only")
    lines.append("# PROVENANCE: pages_merged=%d  rows=%d  first=%s  last=%s"
                 % (len(pages), len(dates), first.isoformat(), last.isoformat()))
    rows_per_page = ",".join(str(r[1]) for r in pages)
    lines.append("# PROVENANCE: rows_available_per_page_as_reported_by_source=%s"
                 % rows_per_page)
    lines.append("# PROVENANCE: date is the exchange session date, rendered as the "
                 "UTC calendar date of the bar timestamp")
    lines.append("# PROVENANCE: volume is as reported by the source, in shares "
                 "(unadjusted for splits)")
    lines.append("# PROVENANCE: PRICE-ONLY series. No dividends or distributions. "
                 "Not a total-return series.")
    for line in extra_provenance:
        lines.append("# PROVENANCE: %s" % line)
    lines.append(HEADER_FIELDS)
    for d in dates:
        o, h, l, c, v = bars[d]
        vs = "" if v is None else str(v)
        lines.append("%s,%.6f,%.6f,%.6f,%.6f,%s"
                     % (d.isoformat(), o, h, l, c, vs))
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return len(dates), first, last


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", required=True,
                    help="agent tool-results directory holding the MCP payloads")
    ap.add_argument("--out", required=True, help="output directory for data/*.csv")
    ap.add_argument("--pull-date", required=True, help="YYYY-MM-DD of the pull")
    ap.add_argument("--only", default="",
                    help="comma-separated FILENAME names to write, e.g. VIX,EEM")
    args = ap.parse_args(argv)

    only = set(x.strip().upper() for x in args.only.split(",") if x.strip())
    os.makedirs(args.out, exist_ok=True)
    by_symbol = load_payloads(args.results)

    print("PAYLOADS FOUND")
    for sym in sorted(by_symbol):
        print("  %-10s %d page(s)" % (sym, len(by_symbol[sym])))
    print("")

    print("MERGE + WRITE")
    written = []
    for sym in sorted(by_symbol):
        name = FILENAME_FOR_SYMBOL[sym]
        if only and name not in only:
            print("  %-10s skipped (not in --only)" % name)
            continue
        bars, pages, interval = merge_symbol(sym, by_symbol[sym])
        rows_per_page = ",".join(str(r[1]) for r in pages)
        extra = ["raw_bars_seen_across_pages=%s" % rows_per_page,
                 "pages_had_more=%s"
                 % ",".join(str(r[2]) for r in pages)]
        if len(pages) > 1:
            extra.append("duplicate_session_dates_removed=%d"
                         % (sum(r[1] for r in pages) - len(bars)))
        path = os.path.join(args.out, name + "_1d.csv")
        n, first, last = write_csv(path, sym, bars, pages, interval,
                                   args.pull_date, extra)
        print("  %-10s -> %s  rows=%d  %s .. %s"
              % (name, os.path.basename(path), n,
                 first.isoformat(), last.isoformat()))
        written.append((name, n, first, last))
    if not written:
        raise SystemExit("ERROR: nothing written")
    print("")
    print("DONE: %d file(s)" % len(written))
    return 0


if __name__ == "__main__":
    sys.exit(main())
