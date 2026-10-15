#!/usr/bin/env python3
"""
carry_data.py -- build data/*.csv for the leg-count test.

The five series this study needs (AMEX:SPY, NASDAQ:QQQ, AMEX:IWM, TVC:VIX,
TVC:US03M at interval 1D) are the SAME series the sibling study
`../index-options-test` already pulled with
`mcp__tradingview__mcp-tv-get-ohlcv` on 2026-10-14.  They are carried, not
re-pulled: a fresh MCP pull returns ~1500 raw bars through the tool result,
which would put a price series into a reasoning context for no gain.

What this script does instead, per series:
  1. reads the sibling file and RE-CHECKS the header's own rows/first/last
     claims against the body it sits above;
  2. computes SHA-256 of the BODY (header stripped);
  3. writes data/<SYM>_1d.csv with the sibling's provenance lines plus this
     carry's own lines;
  4. re-checks the sibling's 2026-10-15 validation fixture
     (`_check_<SYM>_recent.csv`, 1500 sessions pulled fresh from the same tool
     on the same day) against the carried series, session by session, and
     reports the overlap and any mismatch.  Those fixtures are an AUDIT TRAIL
     and are never a strategy input.

Stdlib only.  No network.  Deterministic.  LF output.

USAGE
    py -3 carry_data.py
"""

import datetime
import hashlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SIBLING = os.path.abspath(os.path.join(HERE, "..", "index-options-test", "data"))
OUT = os.path.join(HERE, "data")

SERIES = ["SPY", "QQQ", "IWM", "VIX", "US03M"]
SYMBOL_OF = {
    "SPY": "AMEX:SPY", "QQQ": "NASDAQ:QQQ", "IWM": "AMEX:IWM",
    "VIX": "TVC:VIX", "US03M": "TVC:US03M",
}
CARRY_DATE = "2026-10-15"
SOURCE_PULL = "2026-10-14"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(newline="\n")


def split_header(path):
    """(header_lines, body_lines).  header = leading `#` and blank lines."""
    head, body, in_body = [], [], False
    with io.open(path, "r", encoding="utf-8-sig", newline="") as fh:
        for line in fh:
            s = line.rstrip("\r\n")
            if not in_body and (s.startswith("#") or not s.strip()):
                head.append(s)
                continue
            in_body = True
            body.append(s)
    return head, body


def header_claims(head):
    out = {}
    for line in head:
        txt = line.lstrip("#").strip()
        for key in ("rows", "first", "last"):
            tag = key + "="
            if tag in txt:
                for piece in txt.split():
                    if piece.startswith(tag):
                        out[key] = piece[len(tag):]
    return out


def body_stats(body):
    rows = [r for r in body if r and not r.startswith("date,")]
    return len(rows), rows[0].split(",")[0], rows[-1].split(",")[0]


def body_sha(body):
    h = hashlib.sha256()
    for r in body:
        h.update(r.encode("utf-8"))
        h.update(b"\n")
    return h.hexdigest()


def parse_ohlc(body):
    """{date_iso: (o,h,l,c)} from a body with a date,open,high,low,close header."""
    out = {}
    for r in body:
        if not r or r.startswith("date,"):
            continue
        f = r.split(",")
        out[f[0]] = (float(f[1]), float(f[2]), float(f[3]), float(f[4]))
    return out


def main():
    if not os.path.isdir(SIBLING):
        raise SystemExit("ERROR: sibling data dir not found: %s" % SIBLING)
    if not os.path.isdir(OUT):
        os.makedirs(OUT)

    print("=" * 78)
    print("CARRY DATA -- leg-count test")
    print("=" * 78)
    print("source dir  : %s" % SIBLING)
    print("source pull : %s (TradingView MCP, interval 1D)" % SOURCE_PULL)
    print("carry date  : %s" % CARRY_DATE)
    print("")

    summary, fixtures = [], []
    for sym in SERIES:
        src = os.path.join(SIBLING, "%s_1d.csv" % sym)
        if not os.path.isfile(src):
            raise SystemExit("ERROR: missing sibling series %s" % src)
        head, body = split_header(src)
        claims = header_claims(head)
        nrows, first, last = body_stats(body)
        sha = body_sha(body)

        ok = True
        for k, got in (("rows", str(nrows)), ("first", first), ("last", last)):
            if claims.get(k) != got:
                ok = False
                print("  %-6s HEADER CLAIM MISMATCH %s: header=%r body=%r"
                      % (sym, k, claims.get(k), got))
        if not ok:
            raise SystemExit("ERROR: refusing to carry %s -- header claim "
                             "does not match body" % sym)

        out_lines = []
        for line in head:
            out_lines.append(line)
        out_lines.append("# PROVENANCE: carried_by=carry_data.py  "
                         "carried=%s  from=%s" % (CARRY_DATE, src))
        out_lines.append("# PROVENANCE: CARRIED, not re-pulled. The five series "
                         "are the same 1D series the sibling study already "
                         "pulled on %s; re-pulling returns raw bars through a "
                         "tool result for no gain." % SOURCE_PULL)
        out_lines.append("# PROVENANCE: VERIFIED at carry: the source header's "
                         "own rows/first/last claims were re-checked against "
                         "the body it sits above and matched.")
        out_lines.append("# PROVENANCE: sha256(body of the carried file)=%s"
                         % sha)
        dst = os.path.join(OUT, "%s_1d.csv" % sym)
        with io.open(dst, "w", encoding="utf-8", newline="\n") as fh:
            for line in out_lines:
                fh.write(line + "\n")
            for line in body:
                fh.write(line + "\n")
        summary.append((sym, nrows, first, last, sha[:16]))
        print("  %-6s rows=%-6d first=%s last=%s  sha256(body)=%s..."
              % (sym, nrows, first, last, sha[:16]))

        # ---- validation fixture, if the sibling kept one
        fix = os.path.join(SIBLING, "_check_%s_recent.csv" % sym)
        if os.path.isfile(fix):
            fh, fb = split_header(fix)
            fresh = parse_ohlc(fb)
            carried = parse_ohlc(body)
            overlap = [d for d in fresh if d in carried]
            mism = [d for d in overlap if fresh[d] != carried[d]]
            fixtures.append((sym, len(fresh), len(overlap), len(mism)))
            fh_out = list(fh)
            fh_out.append("# PROVENANCE: carried_by=carry_data.py  carried=%s"
                          % CARRY_DATE)
            fh_out.append("# PROVENANCE: AUDIT TRAIL ONLY -- never a strategy "
                          "input.")
            fh_out.append("# PROVENANCE: re-checked at carry against "
                          "%s_1d.csv: overlap=%d sessions, OHLC mismatches=%d"
                          % (sym, len(overlap), len(mism)))
            with io.open(os.path.join(OUT, "_check_%s_recent.csv" % sym),
                         "w", encoding="utf-8", newline="\n") as out:
                for line in fh_out:
                    out.write(line + "\n")
                for line in fb:
                    out.write(line + "\n")

    print("")
    print("VALIDATION FIXTURES (fresh 2026-10-15 pull by the sibling study, "
          "re-checked here)")
    print("  %-6s %10s %12s %12s" % ("series", "fresh rows", "overlap",
                                     "OHLC mismatch"))
    tot_ov = tot_mm = 0
    for sym, nf, nov, nmm in fixtures:
        tot_ov += nov
        tot_mm += nmm
        print("  %-6s %10d %12d %12d" % (sym, nf, nov, nmm))
    print("  %-6s %10s %12d %12d" % ("TOTAL", "", tot_ov, tot_mm))
    if tot_mm:
        raise SystemExit("ERROR: the carried series DISAGREE with the fresh "
                         "validation pull on %d sessions" % tot_mm)
    print("")
    print("  %d overlapping sessions, 0 OHLC mismatches." % tot_ov)
    print("")
    print("Files written to %s" % OUT)


if __name__ == "__main__":
    main()
