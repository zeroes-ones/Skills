#!/usr/bin/env python3
"""
pull_ohlcv.py -- MCP-payload-on-disk -> CSV, with provenance headers.

Stdlib only. No network of its own.

The agent host persists every large MCP tool result to
    <session>/agents/<id>/tool-results/mcp__tradingview__mcp-tv-get-ohlcv-*.txt
as one JSON payload per call.  This script reads those bytes and turns them into
the CSV shape the sibling studies use: a `date,open,high,low,close,volume` table
behind `# PROVENANCE:` headers.  It never calls the network.

Same discipline as ../frontier-test/pull_ohlcv.py: one payload per call grouped
by the payload's own `symbol` field, pages merged, de-duplicated on the session
date, and two pages that disagree on a shared date refuse to merge.

Two families of series are written here and they must not be confused:

  PRICE  -- a tradable ETF price.  `close` is a price.  Price-only: no
            dividends or distributions are included.
  YIELD  -- an index level quoted in percent per annum (TVC:US02Y, TVC:US03M,
            TVC:US10Y, TVC:US30Y, TVC:VIX).  `close` is NOT a price and no
            price return may be compounded from it.  These are used only as
            state variables (regime filters, cash accrual, option-implied vol)
            and always behind an explicit conversion.

The host truncates a big tool result INLINE but writes the complete payload to
disk, which is what makes this offline conversion possible.  A payload that came
back small enough to fit inline was never written; those are re-issued by hand
and their absence is reported rather than papered over.

USAGE
    py -3 pull_ohlcv.py --results <dir>[,<dir>...] --out data --pull-date YYYY-MM-DD
"""

import argparse
import datetime
import glob
import hashlib
import json
import os
import sys

# The file name is the symbol the rest of the toolchain expects; the source
# symbol is what the data source was asked for.
FILENAME_FOR_SYMBOL = {
    "AMEX:SPY": "SPY",
    "NASDAQ:QQQ": "QQQ",
    "AMEX:IWM": "IWM",
    "AMEX:MDY": "MDY",
    "AMEX:DIA": "DIA",
    "NASDAQ:TLT": "TLT",
    "AMEX:TLH": "TLH",
    "AMEX:EDV": "EDV",
    "NASDAQ:IEF": "IEF",
    "NASDAQ:SHY": "SHY",
    "AMEX:TIP": "TIP",
    "AMEX:LQD": "LQD",
    "AMEX:HYG": "HYG",
    "NASDAQ:EMB": "EMB",
    "AMEX:BIL": "BIL",
    "AMEX:GLD": "GLD",
    "AMEX:SLV": "SLV",
    "AMEX:GDX": "GDX",
    "AMEX:DBC": "DBC",
    "AMEX:VNQ": "VNQ",
    "AMEX:EEM": "EEM",
    "AMEX:EFA": "EFA",
    "AMEX:EWJ": "EWJ",
    "AMEX:FXI": "FXI",
    "AMEX:ILF": "ILF",
    "AMEX:EWZ": "EWZ",
    "AMEX:UUP": "UUP",
    "AMEX:XLE": "XLE",
    "AMEX:XLU": "XLU",
    "AMEX:XLK": "XLK",
    "AMEX:XLP": "XLP",
    "AMEX:XLV": "XLV",
    "TVC:VIX": "VIX",
    "TVC:US03M": "US03M",
    "TVC:US02Y": "US02Y",
    "TVC:US10Y": "US10Y",
    "TVC:US30Y": "US30Y",
    "TVC:DXY": "DXY",
}

# Symbols whose `close` is NOT a price.  Stated in the header so no downstream
# step can silently treat them as tradable.
NON_PRICE_SYMBOLS = {
    "TVC:US03M": "3-month US Treasury bill YIELD, percent per annum",
    "TVC:US02Y": "2-year US Treasury YIELD, percent per annum",
    "TVC:US10Y": "10-year US Treasury YIELD, percent per annum",
    "TVC:US30Y": "30-year US Treasury YIELD, percent per annum",
    "TVC:VIX": "CBOE VIX index level, in volatility points (a volatility, "
               "not a tradable price and not a yield)",
    "TVC:DXY": "US Dollar Index level (an index level, not a tradable ETF "
               "price; UUP is the tradable proxy)",
}

HEADER_FIELDS = "date,open,high,low,close,volume"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(newline="\n")

EPOCH = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)


def utc_date(ts):
    """Session date = UTC calendar date of the bar timestamp.

    Epoch arithmetic rather than datetime.fromtimestamp(), because the yield
    histories reach back before 1970 and this host's fromtimestamp() refuses a
    negative timestamp with OSError EINVAL.
    """
    return (EPOCH + datetime.timedelta(seconds=int(ts))).date()


def load_payloads(results_dirs):
    """Return {source_symbol: [(path, payload), ...]} from every payload file."""
    by_symbol = {}
    seen = set()
    n_files = 0
    for results_dir in results_dirs:
        pattern = os.path.join(results_dir,
                               "mcp__tradingview__mcp-tv-get-ohlcv-*.txt")
        for path in sorted(glob.glob(pattern), key=os.path.getmtime):
            with open(path, "rb") as fh:
                raw = fh.read()
            digest = hashlib.sha256(raw).hexdigest()
            if digest in seen:
                continue
            seen.add(digest)
            n_files += 1
            try:
                payload = json.loads(raw.decode("utf-8"))
            except (ValueError, UnicodeDecodeError) as exc:
                print("  SKIP (not JSON: %s) %s" % (exc, os.path.basename(path)))
                continue
            if not payload.get("success"):
                sym = payload.get("symbol") or "(unknown)"
                print("  FAIL (success=false) %-12s %s"
                      % (sym, str(payload.get("error"))[:70]))
                continue
            sym = payload.get("symbol")
            if sym not in FILENAME_FOR_SYMBOL:
                print("  SKIP (unmapped symbol %r) %s"
                      % (sym, os.path.basename(path)))
                continue
            by_symbol.setdefault(sym, []).append((path, payload))
    print("  files read (after de-duplication by content): %d" % n_files)
    return by_symbol


def merge_symbol(source_symbol, pages):
    bars = {}
    for path, payload in pages:
        b = payload["bars"]
        n = len(b["t"])
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
    return bars


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
    lines.append("# PROVENANCE: date is the exchange session date, rendered as "
                 "the UTC calendar date of the bar timestamp")
    if source_symbol in NON_PRICE_SYMBOLS:
        lines.append("# PROVENANCE: *** NOT A TRADABLE PRICE SERIES ***. %s. "
                     "The `close` column is not a price; no price return may be "
                     "compounded from it."
                     % NON_PRICE_SYMBOLS[source_symbol])
    else:
        lines.append("# PROVENANCE: volume is as reported by the source, in "
                     "shares (unadjusted for splits)")
        lines.append("# PROVENANCE: PRICE-ONLY series. No dividends or "
                     "distributions. Not a total-return series.")
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
                    help="comma-separated agent tool-results directories")
    ap.add_argument("--out", required=True)
    ap.add_argument("--pull-date", required=True)
    ap.add_argument("--only", default="")
    args = ap.parse_args(argv)

    dirs = [d for d in args.results.split(",") if d.strip()]
    only = set(x.strip().upper() for x in args.only.split(",") if x.strip())
    os.makedirs(args.out, exist_ok=True)

    by_symbol = load_payloads(dirs)
    print("")
    print("PAYLOADS FOUND")
    for sym in sorted(by_symbol):
        print("  %-12s %d page(s)" % (sym, len(by_symbol[sym])))
    print("")
    print("MERGE + WRITE")
    written = []
    for sym in sorted(by_symbol):
        name = FILENAME_FOR_SYMBOL[sym]
        if only and name not in only:
            continue
        bars = merge_symbol(sym, by_symbol[sym])
        interval = by_symbol[sym][0][1].get("interval", "1D")
        path = os.path.join(args.out, name + "_1d.csv")
        n, first, last = write_csv(path, sym, bars, by_symbol[sym], interval,
                                   args.pull_date)
        print("  %-6s -> %-14s rows=%-6d %s .. %s"
              % (name, os.path.basename(path), n, first.isoformat(),
                 last.isoformat()))
        written.append(name)
    unresolved = sorted(set(FILENAME_FOR_SYMBOL) - set(by_symbol))
    print("")
    print("REQUESTED BUT NO PAYLOAD ON DISK (failed to resolve, or the "
          "response was small enough to stay inline):")
    for sym in unresolved:
        print("  %s" % sym)
    print("")
    print("DONE: %d file(s)" % len(written))
    return 0


if __name__ == "__main__":
    sys.exit(main())
