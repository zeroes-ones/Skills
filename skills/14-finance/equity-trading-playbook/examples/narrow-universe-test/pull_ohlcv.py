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

Same discipline as ../frontier-test/pull_ohlcv.py, ../weather-test/pull_ohlcv.py
and ../regime-study/pull_ohlcv.py: one payload per call, grouped by the payload's
own `symbol` field, pages merged, de-duplicated on the session date, and two
payloads that disagree on a shared date refuse to merge.

TWO DIFFERENCES FROM THE SIBLINGS:

  1. Several symbols were pulled MORE THAN ONCE with different `date_from`
     arguments (the first pass asked for 2010+, a later pass for 2004+, to reach
     back far enough for the long-window basket). Those payloads overlap. They
     are merged into one series rather than treated as a conflict, because the
     source returns the same split-adjusted values for a shared date; a genuine
     OHLC disagreement still aborts.

  2. The source symbol is NOT always what the brief named. Six of the fourteen
     constituents resolved only under a different exchange prefix, and one
     (WMT) resolved only as NASDAQ:WMT. The mapping below is the one that
     actually worked; every failure is recorded in pull-output.txt.

USAGE
    py -3 pull_ohlcv.py --results <tool-results dir> --out data \
        --pull-date 2026-10-14 [--only AAPL,MSFT]
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
    # --- the three index ETFs ---
    "AMEX:SPY": "SPY",
    "NASDAQ:QQQ": "QQQ",
    "AMEX:IWM": "IWM",
    # --- the cross-asset four-sleeve book the weather-test built ---
    "NASDAQ:TLT": "TLT",
    "AMEX:GLD": "GLD",
    "AMEX:EEM": "EEM",
    # --- cash ---
    "TVC:US03M": "US03M",
    "AMEX:BIL": "BIL",
    # --- volatility reference ---
    "TVC:VIX": "VIX",
    # --- the fourteen declared constituents ---
    "NASDAQ:AAPL": "AAPL",
    "NASDAQ:MSFT": "MSFT",
    "NASDAQ:NVDA": "NVDA",
    "NASDAQ:AMZN": "AMZN",
    "NASDAQ:GOOGL": "GOOGL",
    "NASDAQ:META": "META",
    "NASDAQ:TSLA": "TSLA",
    "NYSE:JPM": "JPM",
    "NYSE:JNJ": "JNJ",
    "NASDAQ:WMT": "WMT",
    "NYSE:XOM": "XOM",
    "NYSE:UNH": "UNH",
    "NYSE:V": "V",
    "NASDAQ:AVGO": "AVGO",
}

# Symbols whose `close` is NOT a price. Stated in the header so no downstream
# step can silently treat them as tradable.
YIELD_INDEX_SYMBOLS = {"TVC:US03M"}

# Source symbols that were ASKED FOR and REFUSED. Recorded so the README can
# state which brief-supplied tickers did not resolve as written.
REFUSED = [
    ("AMEX:JPM", "NYSE:JPM"),
    ("AMEX:JNJ", "NYSE:JNJ"),
    ("AMEX:WMT", "NASDAQ:WMT"),
    ("AMEX:XOM", "NYSE:XOM"),
    ("AMEX:UNH", "NYSE:UNH"),
    ("AMEX:V", "NYSE:V"),
    ("AMEX:AVGO", "NASDAQ:AVGO"),
    ("NYSE:WMT", "NASDAQ:WMT"),
]

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
    """Return ({source_symbol: [(path, payload), ...]}, failures)."""
    pattern = os.path.join(results_dir, "mcp__tradingview__mcp-tv-get-ohlcv-*.txt")
    paths = sorted(glob.glob(pattern), key=os.path.getmtime)
    if not paths:
        raise SystemExit("ERROR: no get_ohlcv payloads under %s" % results_dir)

    by_symbol = {}
    failures = []
    skipped = 0
    for path in paths:
        with open(path, "r", encoding="utf-8") as fh:
            raw = fh.read()
        try:
            payload = json.loads(raw)
        except ValueError as exc:
            print("  SKIP (not JSON: %s) %s" % (exc, os.path.basename(path)))
            skipped += 1
            continue
        if not payload.get("success"):
            failures.append((os.path.basename(path), str(payload.get("error"))))
            continue
        sym = payload.get("symbol")
        if sym not in FILENAME_FOR_SYMBOL:
            print("  SKIP (unmapped symbol %r) %s" % (sym, os.path.basename(path)))
            skipped += 1
            continue
        by_symbol.setdefault(sym, []).append((path, payload))
    return by_symbol, failures, skipped


def merge_symbol(source_symbol, pages):
    """Merge every payload of one symbol into a single date-sorted bar table."""
    bars = {}
    page_report = []
    conflicts = []
    dup_dates = 0
    for path, payload in pages:
        b = payload["bars"]
        n = len(b["t"])
        page_report.append((os.path.basename(path), n, payload.get("has_more"),
                            payload.get("date_from_effective")))
        for i in range(n):
            d = utc_date(b["t"][i])
            row = (float(b["o"][i]), float(b["h"][i]), float(b["l"][i]),
                   float(b["c"][i]), b["v"][i])
            if d in bars:
                prev = bars[d]
                if (prev[0], prev[1], prev[2], prev[3]) != row[:4]:
                    conflicts.append((d, prev[:4], row[:4],
                                      os.path.basename(path)))
                    continue
                dup_dates += 1
                continue
            bars[d] = row
    if conflicts:
        for d, a, c, p in conflicts[:5]:
            print("    CONFLICT %s: %r vs %r  (%s)"
                  % (d.isoformat(), a, c, p))
        raise SystemExit(
            "ERROR: %s has %d payload(s) that disagree with another payload on "
            "a shared date; refusing to merge."
            % (source_symbol, len(conflicts)))
    interval = pages[0][1].get("interval", "1D")
    return bars, page_report, interval, dup_dates


def write_csv(path, source_symbol, bars, pages, interval, pull_date, dup_dates):
    dates = sorted(bars.keys())
    first, last = dates[0], dates[-1]
    lines = []
    lines.append("# PROVENANCE: source=TradingView MCP tool "
                 "mcp__tradingview__mcp-tv-get-ohlcv")
    lines.append("# PROVENANCE: symbol=%s  interval=%s  fields=OHLCV"
                 % (source_symbol, interval))
    lines.append("# PROVENANCE: pulled=%s (UTC date of the pull)" % pull_date)
    lines.append("# PROVENANCE: pages_merged=%d  rows=%d  first=%s  last=%s"
                 % (len(pages), len(dates), first.isoformat(), last.isoformat()))
    lines.append("# PROVENANCE: duplicate_dates_collapsed=%d (payloads of the "
                 "same symbol pulled with different date_from windows share a "
                 "date and agreed on OHLC)" % dup_dates)
    rows_per_page = ",".join(str(r[1]) for r in pages)
    lines.append("# PROVENANCE: rows_per_payload=%s" % rows_per_page)
    if source_symbol in YIELD_INDEX_SYMBOLS:
        lines.append("# PROVENANCE: *** NOT A PRICE SERIES ***. This symbol is a "
                     "YIELD INDEX (3-month US Treasury bill, percent per annum). "
                     "The `close` column is an annualised yield in percent, not a "
                     "tradable price. It has no volume. No price-return may be "
                     "computed from it; it is used only as the cash-accrual rate.")
    else:
        lines.append("# PROVENANCE: PRICE-ONLY series. No dividends or "
                     "distributions. Not a total-return series. Volume is as "
                     "reported by the source, in shares, unadjusted for splits.")
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
                    help="comma-separated FILENAME names to write, e.g. AAPL,MSFT")
    args = ap.parse_args(argv)

    only = set(x.strip().upper() for x in args.only.split(",") if x.strip())
    os.makedirs(args.out, exist_ok=True)
    by_symbol, failures, skipped = load_payloads(args.results)

    print("PAYLOADS FOUND")
    for sym in sorted(by_symbol):
        print("  %-16s %d payload(s)" % (sym, len(by_symbol[sym])))
    print("")
    print("PAYLOADS REFUSED BY THE SOURCE (success=false)")
    if failures:
        for name, err in failures:
            print("  %s" % name)
            print("      %s" % err[:110])
    else:
        print("  (none)")
    print("")
    print("SYMBOLS ASKED FOR THAT DID NOT RESOLVE AS WRITTEN")
    for asked, worked in REFUSED:
        print("  %-14s -> refused; %s resolved instead" % (asked, worked))
    print("")

    print("MERGE + WRITE")
    written = []
    for sym in sorted(by_symbol):
        name = FILENAME_FOR_SYMBOL[sym]
        if only and name not in only:
            continue
        bars, pages, interval, dup = merge_symbol(sym, by_symbol[sym])
        path = os.path.join(args.out, name + "_1d.csv")
        n, first, last = write_csv(path, sym, bars, pages, interval,
                                   args.pull_date, dup)
        written.append(name)
        print("  %-8s -> %-12s rows=%-6d %s .. %s  (dup dates collapsed %d)"
              % (name, os.path.basename(path), n, first.isoformat(),
                 last.isoformat(), dup))

    print("")
    print("DONE: %d file(s); %d payload(s) skipped as unmapped" %
          (len(written), skipped))


if __name__ == "__main__":
    main()
