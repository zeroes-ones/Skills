#!/usr/bin/env python3
"""
pull_data.py -- build data/*.csv for the index-options study.

Stdlib only. No network of its own. LF output.

TWO DATA STEPS, both recorded in this run's stdout:

  1. CARRY. The five long series this study needs (SPY, QQQ, IWM, VIX, US03M)
     are already on disk in the sibling study `../../equity-trading-playbook/
     examples/frontier-test/data/`, pulled with the SAME MCP tool on 2026-10-14.
     They are carried into `data/` behind a provenance header that names where
     they came from. Carrying is only allowed after the carried file proves it
     is the file it claims to be (a SHA-256 of the body is recomputed and the
     header's own row/first/last claims are re-checked against the body).

  2. FRESH PULL + OVERLAP CHECK. This session issued four new
     `mcp__tradingview__mcp-tv-get-ohlcv` calls (SPY, QQQ, IWM, VIX at
     count=1500) on 2026-10-15. The agent host persisted those payloads to
     <session>/agents/<id>/tool-results/*.txt. This script reads those bytes and
     compares the overlapping sessions against the carried file, row for row.
     A mismatch is reported, never smoothed over. The fresh payloads are also
     written to `data/_check_<SYM>_recent.csv` as an audit trail; they are NOT
     an input to any strategy.

USAGE
    py -3 pull_data.py --results <tool-results dir> \
        --sibling ../frontier-test/data --out data \
        --carry-date 2026-10-14 --check-date 2026-10-15
"""

import argparse
import datetime
import glob
import hashlib
import io
import json
import os
import sys

HEADER_FIELDS = "date,open,high,low,close,volume"

# filename -> the source symbol the data source was asked for
CARRIED = [
    ("SPY", "AMEX:SPY"),
    ("QQQ", "NASDAQ:QQQ"),
    ("IWM", "AMEX:IWM"),
    ("VIX", "TVC:VIX"),
    ("US03M", "TVC:US03M"),
]

# The fresh validation pull of this session asked for these four.
FRESH = {"AMEX:SPY": "SPY", "NASDAQ:QQQ": "QQQ",
         "AMEX:IWM": "IWM", "TVC:VIX": "VIX"}

# Symbols whose `close` is NOT a price and must never be compounded as one.
NOT_A_PRICE = {"US03M"}

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(newline="\n")

EPOCH = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)


def utc_date(ts):
    """UTC calendar date of a bar timestamp, without datetime.fromtimestamp().

    fromtimestamp() is not used because the cash series reaches back to 1954 and
    the host may refuse a pre-1970 value; the epoch arithmetic cannot.
    """
    return (EPOCH + datetime.timedelta(seconds=int(ts))).date()


def read_body(path):
    """(meta_lines, {date: (o,h,l,c,v)}, order) from an existing study CSV."""
    meta, rows, order = [], {}, []
    with io.open(path, "r", encoding="utf-8-sig", newline="") as fh:
        for line in fh:
            line = line.rstrip("\r\n")
            if not line.strip():
                continue
            if line.startswith("#"):
                meta.append(line)
                continue
            if line.startswith("date,"):
                continue
            f = line.split(",")
            d = datetime.date.fromisoformat(f[0])
            rows[d] = (f[1], f[2], f[3], f[4], f[5])
            order.append(d)
    return meta, rows, order


def body_sha256(path):
    """SHA-256 of the CSV BODY only (provenance comments excluded), so the hash
    of a carried series identifies its data and not its header text."""
    h = hashlib.sha256()
    with io.open(path, "r", encoding="utf-8-sig", newline="") as fh:
        for line in fh:
            line = line.rstrip("\r\n")
            if line.startswith("#") or not line.strip():
                continue
            if line.startswith("date,"):
                continue
            h.update(line.encode("utf-8"))
            h.update(b"\n")
    return h.hexdigest()


def header_claim(meta, key):
    """Pull `key=<value>` out of the provenance comments, or None."""
    for line in meta:
        if line.startswith("# PROVENANCE:"):
            body = line[len("# PROVENANCE:"):]
            for field in body.split():
                if field.startswith(key + "="):
                    return field.split("=", 1)[1]
    return None


def write_csv(path, series_name, source_symbol, rows, order, prov_lines):
    lines = ["# PROVENANCE: source=TradingView MCP tool "
             "mcp__tradingview__mcp-tv-get-ohlcv",
             "# PROVENANCE: symbol=%s  interval=1D  fields=OHLCV"
             % source_symbol]
    lines.extend(prov_lines)
    lines.append("# PROVENANCE: date is the exchange session date, rendered as "
                 "the UTC calendar date of the bar timestamp")
    if series_name in NOT_A_PRICE:
        lines.append("# PROVENANCE: *** NOT A PRICE SERIES ***. TVC:US03M is a "
                     "YIELD INDEX (3-month US Treasury bill, percent per annum). "
                     "The `close` column is an annualised yield in percent, not a "
                     "tradable price. No price-return may be computed from it; it "
                     "is used only as the cash-accrual rate.")
    else:
        lines.append("# PROVENANCE: split-adjusted, regular session only")
        lines.append("# PROVENANCE: volume is as reported by the source, in "
                     "shares (unadjusted for splits)")
    lines.append("# PROVENANCE: PRICE-ONLY series. No dividends or "
                 "distributions. Not a total-return series.")
    lines.append(HEADER_FIELDS)
    for d in order:
        o, h, l, c, v = rows[d]
        lines.append("%s,%s,%s,%s,%s,%s" % (d.isoformat(), o, h, l, c, v))
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")


def load_fresh(results_dir):
    """{source_symbol: {date: (o,h,l,c,v)}} from the persisted MCP payloads."""
    pattern = os.path.join(results_dir, "mcp__tradingview__mcp-tv-get-ohlcv-*.txt")
    out = {}
    for path in sorted(glob.glob(pattern), key=os.path.getmtime):
        with io.open(path, "r", encoding="utf-8") as fh:
            raw = fh.read()
        try:
            payload = json.loads(raw)
        except ValueError:
            continue
        sym = payload.get("symbol")
        if sym not in FRESH:
            continue
        b = payload["bars"]
        n = len(b["t"])
        rows = {}
        for i in range(n):
            rows[utc_date(b["t"][i])] = (float(b["o"][i]), float(b["h"][i]),
                                         float(b["l"][i]), float(b["c"][i]),
                                         b["v"][i])
        out.setdefault(sym, {}).update(rows)
        print("  payload %-46s symbol=%-11s bars=%d  interval=%s  has_more=%s"
              % (os.path.basename(path), sym, n, payload.get("interval"),
                 payload.get("has_more")))
    return out


def fmt(x):
    return "%.6f" % x


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", required=True)
    ap.add_argument("--sibling", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--carry-date", required=True)
    ap.add_argument("--check-date", required=True)
    args = ap.parse_args(argv)

    if not os.path.isdir(args.out):
        os.makedirs(args.out)

    print("=" * 78)
    print("STEP 1 -- CARRY: verify then copy the long series from the sibling study")
    print("=" * 78)
    print("Sibling directory: %s" % args.sibling)
    carried = {}
    carry_hash = {}
    for name, src in CARRIED:
        spath = os.path.join(args.sibling, "%s_1d.csv" % name)
        if not os.path.isfile(spath):
            raise SystemExit("ERROR: sibling series missing: %s" % spath)
        meta, rows, order = read_body(spath)
        # Re-check the header's own claims against the body it is attached to.
        c_rows = header_claim(meta, "rows")
        c_first = header_claim(meta, "first")
        c_last = header_claim(meta, "last")
        actual = (len(order), order[0].isoformat(), order[-1].isoformat())
        claimed = (int(c_rows) if c_rows else None, c_first, c_last)
        sha = body_sha256(spath)
        ok = (claimed == actual)
        print("  %-6s %-11s rows=%-6d first=%s last=%s  header_claim_matches=%s  "
              "sha256(body)=%s"
              % (name, src, actual[0], actual[1], actual[2], ok, sha[:16]))
        if not ok:
            raise SystemExit("ERROR: %s header claims %r but the body holds %r"
                             % (name, claimed, actual))
        carried[name] = (rows, order)
        carry_hash[name] = sha

    print("")
    print("=" * 78)
    print("STEP 2 -- FRESH PULL (%s) and OVERLAP CHECK against the carried files"
          % args.check_date)
    print("=" * 78)
    fresh = load_fresh(args.results)
    print("")
    print("  %-6s %-6s %-6s %-9s %s" %
          ("series", "fresh", "shared", "identical", "note"))
    check_rows = []
    for src, name in sorted(FRESH.items(), key=lambda kv: kv[1]):
        if src not in fresh:
            print("  %-6s %-6s %-6s %-9s %s"
                  % (name, "-", "-", "-", "NO FRESH PAYLOAD FOUND"))
            check_rows.append((name, 0, 0, 0, "no_fresh_payload"))
            continue
        rows, order = carried[name]
        fr = fresh[src]
        shared = sorted(set(fr) & set(rows))
        ident = 0
        diffs = []
        for d in shared:
            a = rows[d]
            b = (fmt(fr[d][0]), fmt(fr[d][1]), fmt(fr[d][2]), fmt(fr[d][3]),
                 "" if fr[d][4] is None else str(fr[d][4]))
            if a[:4] == b[:4]:
                ident += 1
            else:
                diffs.append((d, a[:4], b[:4]))
        note = "%d OHLC mismatch(es)" % len(diffs)
        if diffs:
            for d, a, b in diffs[:5]:
                note += "\n        %s carried=%s fresh=%s" % (d, a, b)
        print("  %-6s %-6d %-6d %-9d %s" % (name, len(fr), len(shared), ident, note))
        check_rows.append((name, len(fr), len(shared), ident, note))
        # audit trail
        cpath = os.path.join(args.out, "_check_%s_recent.csv" % name)
        fo = sorted(fr)
        prov = ["# PROVENANCE: VALIDATION FIXTURE -- this session's own fresh pull",
                "# PROVENANCE: pulled=%s  bars=%d  symbol=%s"
                % (args.check_date, len(fo), src),
                "# PROVENANCE: NOT AN INPUT TO ANY STRATEGY. Audit trail only."]
        frows = {d: (fmt(fr[d][0]), fmt(fr[d][1]), fmt(fr[d][2]), fmt(fr[d][3]),
                     "" if fr[d][4] is None else str(fr[d][4])) for d in fo}
        write_csv(cpath, name, src, frows, fo, prov)

    print("")
    print("=" * 78)
    print("STEP 3 -- WRITE data/*.csv")
    print("=" * 78)
    for name, src in CARRIED:
        rows, order = carried[name]
        prov = [
            "# PROVENANCE: pulled=%s (UTC date of the sibling pull)" % args.carry_date,
            "# PROVENANCE: CARRIED from ../frontier-test/data/%s_1d.csv -- same "
            "tool, same pull date" % name,
            "# PROVENANCE: carried_by=pull_data.py  carried=%s" % args.check_date,
            "# PROVENANCE: VERIFIED before carry: the sibling header's own "
            "rows/first/last claims were re-checked against its body and matched",
            "# PROVENANCE: sha256(body of the carried file)=%s" % carry_hash[name],
            "# PROVENANCE: rows=%d  first=%s  last=%s"
            % (len(order), order[0].isoformat(), order[-1].isoformat()),
        ]
        dpath = os.path.join(args.out, "%s_1d.csv" % name)
        write_csv(dpath, name, src, rows, order, prov)
        dsha = body_sha256(dpath)
        same = (dsha == carry_hash[name])
        print("  %-6s -> %-28s rows=%-6d  body_sha256_unchanged=%s"
              % (name, os.path.basename(dpath), len(order), same))
        if not same:
            raise SystemExit("ERROR: carried copy of %s differs from its source"
                             % name)

    print("")
    print("DONE. %d carried series + %d validation fixtures in %s"
          % (len(CARRIED), len(check_rows), args.out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
