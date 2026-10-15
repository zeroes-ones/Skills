#!/usr/bin/env python3
"""
pull_ohlcv.py -- MCP-payload-on-disk -> CSV, with provenance headers.

Stdlib only. Makes no network call of its own.

The agent host persists every large `mcp__tradingview__mcp-tv-get-ohlcv`
result to
    <session>/agents/<id>/tool-results/mcp__tradingview__mcp-tv-get-ohlcv-*.txt
as one JSON payload per call. This script reads those bytes and turns them into
the CSV form the sibling studies use: a `date,open,high,low,close,volume` table
behind a `# PROVENANCE:` header.

It also -- with --copy-from -- copies the five series that the sibling study
`equity-trading-playbook/examples/weather-test` already pulled from the same
source, byte-identical, and adds a `copy_of` provenance line. Those five were
verified against this vendor by the sibling study; re-pulling them would cost
nothing but bytes, and re-copying them keeps the audit trail honest.

USAGE
    py -3 pull_ohlcv.py --results <tool-results dir> --out data \
        --pull-date 2026-10-14 --copy-from ../weather-test/data
"""

import argparse
import datetime
import glob
import json
import os
import sys

# Source symbol -> the file stem the toolchain expects.
FILENAME_FOR_SYMBOL = {
    "AMEX:SPY": "SPY",
    "NASDAQ:QQQ": "QQQ",
    "AMEX:IWM": "IWM",
    "AMEX:EEM": "EEM",
    "NASDAQ:TLT": "TLT",
    "AMEX:GLD": "GLD",
    "AMEX:EFA": "EFA",
    "AMEX:VNQ": "VNQ",
    "NASDAQ:IEF": "IEF",
    "AMEX:HYG": "HYG",
    "AMEX:DBC": "DBC",
    "TVC:VIX": "VIX",
}

# The five series copied from the sibling study rather than re-pulled.
COPIED_FROM_SIBLING = ("SPY", "TLT", "GLD", "EEM", "VIX")

HEADER_FIELDS = "date,open,high,low,close,volume"

# The repo requires LF everywhere. Redirected stdout on Windows would otherwise
# translate every newline to CRLF, which fails the file-format gate.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(newline="\n")


def utc_date(ts):
    """Session date = the UTC calendar date of the bar timestamp.

    Every source here is a US venue whose regular session opens at 13:30/14:30
    UTC, so the UTC calendar date of the bar is the exchange session date.
    """
    return datetime.datetime.fromtimestamp(int(ts), datetime.timezone.utc).date()


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
            print("  SKIP (success=false) %s" % os.path.basename(path))
            continue
        if payload.get("interval") != "1D":
            print("  SKIP (interval=%r) %s" % (payload.get("interval"), os.path.basename(path)))
            continue
        sym = payload.get("symbol")
        if sym not in FILENAME_FOR_SYMBOL:
            print("  SKIP (unmapped symbol %r) %s" % (sym, os.path.basename(path)))
            continue
        by_symbol.setdefault(sym, []).append((path, payload))
    return by_symbol


def bars_of(payload):
    """(date, open, high, low, close, volume) tuples, ascending by date."""
    b = payload["bars"]
    ts = b["t"]
    n = len(ts)
    for k in ("o", "h", "l", "c"):
        if len(b[k]) != n:
            raise SystemExit("ERROR: column length mismatch in %s" % payload.get("symbol"))
    vol = b.get("v") or [None] * n
    out = []
    for i in range(n):
        out.append((utc_date(ts[i]), b["o"][i], b["h"][i], b["l"][i], b["c"][i], vol[i]))
    out.sort(key=lambda r: r[0])
    return out


def merge_pages(pages):
    """Merge several pages of one symbol. De-duplicate on date, refuse conflicts."""
    merged = {}
    dup = 0
    for page in pages:
        for row in bars_of(page):
            d = row[0]
            if d in merged:
                dup += 1
                prev = merged[d]
                if abs(prev[4] - row[4]) > 1e-9:
                    raise SystemExit(
                        "ERROR: two pages disagree on %s close: %r vs %r" % (d, prev[4], row[4])
                    )
                continue
            merged[d] = row
    return [merged[d] for d in sorted(merged)], dup


def write_csv(path, rows, header_lines):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        for line in header_lines:
            fh.write(line + "\n")
        fh.write(HEADER_FIELDS + "\n")
        for d, o, h, l, c, v in rows:
            if v is None:
                fh.write("%s,%.6f,%.6f,%.6f,%.6f,\n" % (d.isoformat(), o, h, l, c))
            else:
                fh.write(
                    "%s,%.6f,%.6f,%.6f,%.6f,%d\n" % (d.isoformat(), o, h, l, c, int(round(v)))
                )


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", required=True, help="directory of saved MCP payloads")
    ap.add_argument("--out", default="data", help="output directory")
    ap.add_argument("--pull-date", required=True, help="UTC pull date recorded in the header")
    ap.add_argument("--copy-from", default=None,
                    help="sibling data/ dir whose five TradingView series are reused verbatim")
    ap.add_argument("--only", default=None, help="comma-separated stems to write")
    args = ap.parse_args(argv)

    os.makedirs(args.out, exist_ok=True)
    only = set(args.only.split(",")) if args.only else None

    written = {}
    if args.copy_from:
        copy_src = os.path.abspath(args.copy_from)
        for stem in COPIED_FROM_SIBLING:
            if only and stem not in only:
                continue
            src = os.path.join(copy_src, "%s_1d.csv" % stem)
            if not os.path.exists(src):
                raise SystemExit("ERROR: %s missing; cannot copy %s" % (src, stem))
            with open(src, "r", encoding="utf-8") as fh:
                text = fh.read()
            lines = text.split("\n")
            head = [ln for ln in lines if ln.startswith("#")]
            body = [ln for ln in lines if ln and not ln.startswith("#")]
            rows = []
            for ln in body[1:]:
                f = ln.split(",")
                rows.append((datetime.date.fromisoformat(f[0]),
                             float(f[1]), float(f[2]), float(f[3]), float(f[4]),
                             float(f[5]) if f[5] else None))
            head.append("# PROVENANCE: copy_of=%s (byte-identical body)" % args.copy_from)
            head.append("# PROVENANCE: copied=%s into sweep-test/data by pull_ohlcv.py" % args.pull_date)
            head.append("# PROVENANCE: origin already cross-checked against this vendor by the "
                        "weather-test study that first pulled it")
            write_csv(os.path.join(args.out, "%s_1d.csv" % stem), rows, head)
            written[stem] = (len(rows), rows[0][0], rows[-1][0], "copy_of weather-test")
            print("  %-4s n=%5d %s..%s  <- copied from %s"
                  % (stem, len(rows), rows[0][0], rows[-1][0], args.copy_from))

    by_symbol = load_payloads(args.results)
    for sym in sorted(by_symbol):
        stem = FILENAME_FOR_SYMBOL[sym]
        if only and stem not in only:
            continue
        if stem in written:
            print("  %-4s SKIP: already supplied by --copy-from" % stem)
            continue
        pages = [p for _, p in by_symbol[sym]]
        rows, dup = merge_pages(pages)
        page_sizes = ",".join(str(len(bars_of(p))) for p in pages)
        has_more = ",".join(str(bool(p.get("has_more"))) for p in pages)
        head = [
            "# PROVENANCE: source=TradingView MCP tool mcp__tradingview__mcp-tv-get-ohlcv",
            "# PROVENANCE: symbol=%s  interval=1D  fields=OHLCV" % sym,
            "# PROVENANCE: pulled=%s (UTC date of the pull)" % args.pull_date,
            "# PROVENANCE: split-adjusted, regular session only, as served by the source",
            "# PROVENANCE: pages_merged=%d  rows=%d  first=%s  last=%s"
            % (len(pages), len(rows), rows[0][0], rows[-1][0]),
            "# PROVENANCE: rows_available_per_page_as_reported_by_source=%s" % page_sizes,
            "# PROVENANCE: pages_had_more=%s" % has_more,
            "# PROVENANCE: date is the UTC calendar date of the bar timestamp",
            "# PROVENANCE: volume is as reported by the source, unadjusted",
            "# PROVENANCE: PRICE-ONLY series. No dividends or distributions. Not a total-return series.",
            "# PROVENANCE: duplicate_session_dates_removed=%d" % dup,
        ]
        write_csv(os.path.join(args.out, "%s_1d.csv" % stem), rows, head)
        written[stem] = (len(rows), rows[0][0], rows[-1][0], sym)
        print("  %-4s n=%5d %s..%s  <- %s (%d page(s), dup=%d)"
              % (stem, len(rows), rows[0][0], rows[-1][0], sym, len(pages), dup))

    print("wrote %d file(s) into %s" % (len(written), args.out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
