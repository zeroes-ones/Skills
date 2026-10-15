#!/usr/bin/env python3
"""
pull_ohlcv.py -- extract TradingView MCP OHLCV payloads that a session wrote to
disk, merge the pages per symbol, and write one CSV per symbol with provenance.

Deterministic. Stdlib only. No network. No third-party imports.

WHY THIS EXISTS
    The TradingView MCP tool `mcp__tradingview__mcp-tv-get-ohlcv` returns each
    page as a JSON object of parallel arrays. The agent host persists a large
    tool result to a file under the session's `tool-results/` directory, and
    also appends the raw result to its own event log (`wire.jsonl`). This
    script reads those already-on-disk bytes and turns them into reproducible
    CSV. It does NOT call the network itself -- so a re-run of the ANALYSIS
    needs no network at all, and the pulled CSVs are the frozen input.

INPUT SOURCES (both are session-local paths, given explicitly on the CLI)
    --results DIR   a directory of `*.txt` tool-result files (whole file = one
                    JSON payload)
    --wire PATH     a `wire.jsonl` agent event log; each line is an event, and
                    a tool result appears as event.result.output holding the
                    payload as a JSON string

USAGE
    py -3 pull_ohlcv.py --results <session>/agents/<id>/tool-results \
                        --wire    <session>/agents/<id>/wire.jsonl \
                        --out     data

    py -3 pull_ohlcv.py --results D --out data --only AMEX:SPY

EXIT CODES
    0  ran, at least one symbol written
    2  no payload was found, or a payload was malformed
"""

import argparse
import datetime
import glob
import json
import os
import re
import sys

PULL_SOURCE = "TradingView MCP tool mcp__tradingview__mcp-tv-get-ohlcv"
BAR_KEYS = ("t", "o", "h", "l", "c", "v")


class PullError(Exception):
    pass


# ---------------------------------------------------------------------------
# Locating payloads
# ---------------------------------------------------------------------------

def looks_like_ohlcv(obj):
    if not isinstance(obj, dict):
        return False
    bars = obj.get("bars")
    if not isinstance(bars, dict) or "symbol" not in obj:
        return False
    return all(k in bars for k in BAR_KEYS)


def walk_for_payloads(obj, out):
    """Find every OHLCV payload anywhere inside a decoded JSON value.

    A tool result is stored as `event.result.output` holding the payload as a
    JSON *string*, so a string that decodes to an object is walked too.
    """
    if looks_like_ohlcv(obj):
        out.append(obj)
        return
    if isinstance(obj, dict):
        for v in obj.values():
            walk_for_payloads(v, out)
    elif isinstance(obj, list):
        for v in obj:
            walk_for_payloads(v, out)
    elif isinstance(obj, str):
        s = obj.strip()
        if s.startswith("{") and "\"bars\"" in s:
            try:
                walk_for_payloads(json.loads(s), out)
            except ValueError:
                return


def payloads_from_results_dir(path):
    """Each *.txt in the tool-results dir holds one complete payload."""
    files = sorted(glob.glob(os.path.join(path, "*.txt")))
    if not files:
        raise PullError("no *.txt tool-result files under %s" % path)
    found = []
    for f in files:
        with open(f, "r", encoding="utf-8", errors="replace") as fh:
            raw = fh.read()
        raw = raw.strip()
        if not raw:
            continue
        try:
            obj = json.loads(raw)
        except ValueError:
            # A spill file is always one whole JSON object; if it is not, skip
            # it loudly rather than guessing at a repair.
            print("  skip (not whole JSON): %s" % os.path.basename(f))
            continue
        walk_for_payloads(obj, found)
    return found


def payloads_from_wire(path):
    """Tool results are appended to the event log as JSON strings."""
    found = []
    total = 0
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            total += 1
            if "bars" not in line:
                continue
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
            except ValueError:
                continue
            walk_for_payloads(ev, found)
    print("  wire.jsonl: scanned %d events, found %d OHLCV payload(s)"
          % (total, len(found)))
    return found


# ---------------------------------------------------------------------------
# Merging
# ---------------------------------------------------------------------------

def merge_payloads(payloads):
    """Group bars by symbol, de-duplicate on the bar timestamp, sort ascending.

    Returns {symbol: {"rows": [(ts,o,h,l,c,v), ...],
                      "pages": int, "interval": str, "window_available": int}}
    """
    by_symbol = {}
    for p in payloads:
        sym = p["symbol"]
        bars = p["bars"]
        n = len(bars["t"])
        for k in BAR_KEYS:
            if len(bars[k]) != n:
                raise PullError("%s: bars.%s has %d values, expected %d"
                                % (sym, k, len(bars[k]), n))
        slot = by_symbol.setdefault(sym, {
            "rows": {}, "pages": 0, "interval": p.get("interval", "?"),
            "windows": [], "raw_count": 0,
        })
        slot["pages"] += 1
        slot["raw_count"] += n
        if p.get("window_available") is not None:
            slot["windows"].append(p["window_available"])
        for i in range(n):
            ts = int(bars["t"][i])
            slot["rows"][ts] = (
                ts,
                float(bars["o"][i]),
                float(bars["h"][i]),
                float(bars["l"][i]),
                float(bars["c"][i]),
                float(bars["v"][i]),
            )
        wa = p.get("window_available")
        if wa is not None:
            slot["window_available"] = wa
    for sym, slot in by_symbol.items():
        slot["rows"] = [slot["rows"][ts] for ts in sorted(slot["rows"])]
    return by_symbol


def session_date(ts):
    """The bar timestamp is the session open; its UTC calendar date is the
    session date for every US session (13:30Z under EDT, 14:30Z under EST)."""
    return datetime.datetime.fromtimestamp(ts, datetime.timezone.utc).date()


def bar_time(ts):
    return datetime.datetime.fromtimestamp(ts, datetime.timezone.utc).strftime("%H:%MZ")


# ---------------------------------------------------------------------------
# Writing
# ---------------------------------------------------------------------------

def write_csv(path, symbol, slot, pull_date, tool_filter):
    rows = slot["rows"]
    if not rows:
        raise PullError("%s: no bars" % symbol)
    first = session_date(rows[0][0])
    last = session_date(rows[-1][0])
    times = sorted(set(bar_time(r[0]) for r in rows))

    lines = []
    lines.append("# PROVENANCE: source=%s" % PULL_SOURCE)
    lines.append("# PROVENANCE: symbol=%s  interval=%s  fields=OHLCV" %
                 (symbol, slot["interval"]))
    lines.append("# PROVENANCE: pulled=%s (UTC date of the pull)" % pull_date)
    lines.append("# PROVENANCE: split-adjusted, regular session only")
    lines.append("# PROVENANCE: tool=%s" % tool_filter)
    lines.append("# PROVENANCE: pages_merged=%d  rows=%d  first=%s  last=%s"
                 % (slot["pages"], len(rows), first, last))
    if slot["windows"]:
        lines.append("# PROVENANCE: rows_available_per_page_as_reported_by_source=%s"
                     % ",".join(str(x) for x in slot["windows"]))
    lines.append("# PROVENANCE: date is the exchange session date, rendered as "
                 "the UTC calendar date of the bar timestamp (bar times present: %s)"
                 % ",".join(times))
    lines.append("# PROVENANCE: volume is as reported by the source, in shares "
                 "(unadjusted for splits)")
    lines.append("date,open,high,low,close,volume")
    for ts, o, h, l, c, v in rows:
        lines.append("%s,%.6f,%.6f,%.6f,%.6f,%.0f"
                     % (session_date(ts).isoformat(), o, h, l, c, v))

    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write("\n".join(lines) + "\n")
    return first, last, len(rows)


def safe_name(symbol):
    """SPY_1d.csv, not AMEX_SPY_1d.csv: the CSV is named by the ticker the
    strategy study refers to. The full `EXCHANGE:TICKER` symbol travels in the
    provenance header instead."""
    ticker = symbol.split(":")[-1]
    return re.sub(r"[^A-Za-z0-9._-]", "_", ticker)


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(newline="\n")

    ap = argparse.ArgumentParser(prog="pull_ohlcv.py")
    ap.add_argument("--results", default=None, help="tool-results directory")
    ap.add_argument("--wire", default=None, help="wire.jsonl event log")
    ap.add_argument("--out", required=True, help="output directory for CSVs")
    ap.add_argument("--pull-date", default=None,
                    help="ISO date to stamp as the pull date (default: today UTC)")
    ap.add_argument("--only", default=None,
                    help="comma-separated symbol allow-list, e.g. AMEX:SPY")
    args = ap.parse_args(argv if argv is not None else sys.argv[1:])

    if not args.results and not args.wire:
        print("ERROR: give --results and/or --wire", file=sys.stderr)
        return 2

    if args.pull_date:
        pull_date = args.pull_date
    else:
        pull_date = datetime.datetime.now(datetime.timezone.utc).date().isoformat()

    payloads = []
    if args.results:
        print("results dir: %s" % args.results)
        got = payloads_from_results_dir(args.results)
        print("  found %d OHLCV payload(s)" % len(got))
        payloads.extend(got)
    if args.wire:
        print("wire log   : %s" % args.wire)
        payloads.extend(payloads_from_wire(args.wire))

    if not payloads:
        print("ERROR: no OHLCV payload found in the given sources", file=sys.stderr)
        return 2

    by_symbol = merge_payloads(payloads)

    only = None
    if args.only:
        only = set(x.strip() for x in args.only.split(",") if x.strip())

    os.makedirs(args.out, exist_ok=True)
    print("")
    print("%-16s %6s %8s %8s %-12s %-12s %s"
          % ("symbol", "pages", "rawbars", "rows", "first", "last", "csv"))
    written = 0
    for sym in sorted(by_symbol):
        if only and sym not in only:
            continue
        slot = by_symbol[sym]
        raw_total = slot["raw_count"]
        path = os.path.join(args.out, safe_name(sym) + "_1d.csv")
        first, last, n = write_csv(path, sym, slot, pull_date, PULL_SOURCE)
        print("%-16s %6d %8d %8d %-12s %-12s %s"
              % (sym, slot["pages"], raw_total, n, first, last,
                 os.path.basename(path)))
        written += 1

    if written == 0:
        print("ERROR: no symbol matched --only", file=sys.stderr)
        return 2
    print("")
    print("wrote %d CSV file(s) to %s" % (written, args.out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
