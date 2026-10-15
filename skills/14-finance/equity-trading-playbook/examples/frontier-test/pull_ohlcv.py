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

Same discipline as ../weather-test/pull_ohlcv.py and ../regime-study/pull_ohlcv.py:
one payload per call, grouped by the payload's own `symbol` field, pages merged,
de-duplicated on the session date, and two pages that disagree on a shared date
refuse to merge.

ONE DIFFERENCE FROM THE SIBLINGS: this study also needs a CASH proxy, and the
only long-history cash series the data source exposes over OHLCV is a
YIELD INDEX (TVC:US03M, the 3-month Treasury bill yield in percent per annum),
not a price. Its rows are still written here in the same six-column shape, but
the provenance header says so in as many words: for US03M the `close` column is
a PERCENT-PER-ANNUM YIELD, not a price, and nothing downstream may compound it
as a price return.

USAGE
    py -3 pull_ohlcv.py --results <tool-results dir> --out data \
        --pull-date 2026-10-14 [--only US03M,BIL]
"""

import argparse
import datetime
import glob
import json
import os
import sys

# The file name is the symbol the rest of the toolchain expects; the source
# symbol is what the data source was asked for.
FILENAME_FOR_SYMBOL = {
    "AMEX:SPY": "SPY",
    "NASDAQ:QQQ": "QQQ",
    "NASDAQ:TLT": "TLT",
    "AMEX:GLD": "GLD",
    "AMEX:EEM": "EEM",
    "TVC:VIX": "VIX",
    "AMEX:IWM": "IWM",
    "AMEX:DBC": "DBC",
    "AMEX:VNQ": "VNQ",
    "NASDAQ:IEF": "IEF",
    "AMEX:EFA": "EFA",
    "AMEX:HYG": "HYG",
    "AMEX:BIL": "BIL",
    "TVC:US03M": "US03M",
}

# Symbols whose `close` is NOT a price. Stated in the header so no downstream
# step can silently treat them as tradable.
YIELD_INDEX_SYMBOLS = {"TVC:US03M"}

HEADER_FIELDS = "date,open,high,low,close,volume"


# The repo requires LF everywhere. Redirected stdout on Windows would otherwise
# translate every newline to CRLF, which fails the file-format gate.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(newline="\n")


EPOCH = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)


def utc_date(ts):
    """Session date = the UTC calendar date of the bar timestamp.

    Arithmetic on the epoch rather than datetime.fromtimestamp(), because the
    cash proxy's history reaches back before 1970 and this host's
    fromtimestamp() refuses a negative timestamp with OSError EINVAL.
    """
    return (EPOCH + datetime.timedelta(seconds=int(ts))).date()


def load_payloads(results_dir):
    """Return {source_symbol: [(path, payload), ...]} for every get_ohlcv payload."""
    pattern = os.path.join(results_dir, "mcp__tradingview__mcp-tv-get-ohlcv-*.txt")
    paths = sorted(glob.glob(pattern), key=os.path.getmtime)
    if not paths:
        raise SystemExit("ERROR: no get_ohlcv payloads under %s" % results_dir)

    by_symbol = {}
    for path in paths:
        with open(path, "r", encoding="utf-8") as fh:
            raw = fh.read()
        try:
            payload = json.loads(raw)
        except ValueError as exc:
            print("  SKIP (not JSON: %s) %s" % (exc, os.path.basename(path)))
            continue
        if not payload.get("success"):
            print("  SKIP (success=false: %s) %s"
                  % (str(payload.get("error"))[:60], os.path.basename(path)))
            continue
        sym = payload.get("symbol")
        if sym not in FILENAME_FOR_SYMBOL:
            print("  SKIP (unmapped symbol %r) %s" % (sym, os.path.basename(path)))
            continue
        by_symbol.setdefault(sym, []).append((path, payload))
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


def write_csv(path, source_symbol, bars, pages, interval, pull_date):
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
    lines.append("# PROVENANCE: pages_had_more=%s"
                 % ",".join(str(r[2]) for r in pages))
    lines.append("# PROVENANCE: date is the exchange session date, rendered as the "
                 "UTC calendar date of the bar timestamp")
    if source_symbol in YIELD_INDEX_SYMBOLS:
        lines.append("# PROVENANCE: *** NOT A PRICE SERIES ***. This symbol is a "
                     "YIELD INDEX (3-month US Treasury bill, percent per annum). "
                     "The `close` column is an annualised yield in percent, not a "
                     "tradable price. It has no volume. No price-return may be "
                     "computed from it; it is used only as the cash-accrual rate.")
    else:
        lines.append("# PROVENANCE: volume is as reported by the source, in shares "
                     "(unadjusted for splits)")
    lines.append("# PROVENANCE: PRICE-ONLY series. No dividends or distributions. "
                 "Not a total-return series.")
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
                    help="comma-separated FILENAME names to write, e.g. US03M,BIL")
    args = ap.parse_args(argv)

    only = set(x.strip().upper() for x in args.only.split(",") if x.strip())
    os.makedirs(args.out, exist_ok=True)
    by_symbol = load_payloads(args.results)

    print("PAYLOADS FOUND")
    for sym in sorted(by_symbol):
        print("  %-12s %d page(s)" % (sym, len(by_symbol[sym])))
    print("")

    print("MERGE + WRITE")
    written = []
    for sym in sorted(by_symbol):
        name = FILENAME_FOR_SYMBOL[sym]
        if only and name not in only:
            print("  %-12s skipped (not in --only)" % name)
            continue
        bars, pages, interval = merge_symbol(sym, by_symbol[sym])
        path = os.path.join(args.out, name + "_1d.csv")
        n, first, last = write_csv(path, sym, bars, pages, interval,
                                   args.pull_date)
        print("  %-12s -> %s  rows=%d  %s .. %s"
              % (name, os.path.basename(path), n, first.isoformat(),
                 last.isoformat()))
        written.append((name, n, first, last))
    if not written:
        raise SystemExit("ERROR: nothing written")
    print("")
    print("DONE: %d file(s)" % len(written))
    return 0


if __name__ == "__main__":
    sys.exit(main())
