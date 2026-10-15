#!/usr/bin/env python3
"""pull_data.py - download the real daily price history for the regime study.

Writes one CSV per symbol into ./data/ with a provenance header block.
Prints only row counts and date ranges, never raw bars.

Sources and why each is used
----------------------------
Primary series (data/<SYM>_1d.csv)
    Yahoo Finance chart JSON endpoint, full available history:
      SPY 1993-01-29, QQQ 1999-03-10, IWM 2000-05-26, EEM 2003-04-14,
      ^VIX 1990-01-02.
    Long history matters here because the study is about regimes and years -
    the 2000-02 bear and the 2008 crisis are half the point.
    Prices are SPLIT-ADJUSTED traded prices (dividends are not added back), so
    an OHLC level is the price a stop or a fill actually referenced.  This is
    the same convention TradingView reports, and the two agree exactly on the
    recent overlap (verify_sources.py CHECK 3).
    A `close_tr` column carries the total-return (dividend-reinvested) close
    from the same response.  Nothing in the study trades on it; it exists so
    RESULTS.md can state how far the price-only CAGR understates buy-and-hold.

Moomoo audit trail (data/<SYM>_1d_moomoo.csv)
    The same bars from the moomoo vendor feed over the local OpenD channel
    (127.0.0.1:11111) via the official `moomoo` SDK - the vendor behind the
    hosted `mcp__moomoo__*` tools, callable from a script so bars go straight
    to disk instead of into an agent context window.  Daily, forward-adjusted
    (qfq); the feed retains ~20 years, so this starts 2006-10-02.
    Its absolute levels differ from Yahoo's because moomoo folds dividends in
    on its own schedule, so verify_sources.py compares DAILY RETURNS, not
    levels - returns are the invariant that survives an adjustment convention.

VIX note
    The moomoo feed does not carry the VIX index: US.VIX returns ret=-1 on the
    local kline channel, and the hosted `mcp__moomoo__quote_history_kline` tool
    rejects the call on its ktype/autype enums.  VIX therefore comes from Yahoo
    ^VIX and is cross-checked against TradingView's TVC:VIX by verify_sources.py.

Usage
-----
  py -3 pull_data.py            # refresh every symbol
  py -3 pull_data.py --check    # report what is on disk, download nothing
"""
import argparse
import csv
import io
import json
import os
import sys
import time
import urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

ETF_SYMBOLS = ["SPY", "QQQ", "IWM", "EEM"]
VIX_SYMBOL = "VIX"
ALL_SYMBOLS = ETF_SYMBOLS + [VIX_SYMBOL]

OPEND_HOST, OPEND_PORT = "127.0.0.1", 11111
COLS_FULL = ["date", "open", "high", "low", "close", "volume", "close_tr"]
COLS_MOOMOO = ["date", "open", "high", "low", "close", "volume"]


def provenance(source, symbol_name, interval, adjustment, note):
    pulled = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return [
        "# source: {}".format(source),
        "# symbol: {}".format(symbol_name),
        "# pull_date_utc: {}".format(pulled),
        "# interval: {}".format(interval),
        "# adjustment: {}".format(adjustment),
        "# note: {}".format(note),
    ]


def write_csv(path, header_lines, columns, rows):
    tmp = path + ".tmp"
    with io.open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        for line in header_lines:
            fh.write(line + "\n")
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(columns)
        for r in rows:
            w.writerow(r)
    os.replace(tmp, path)
    return len(rows)


def _f4(v):
    return "" if v is None else "{:.4f}".format(float(v))


# ---------------------------------------------------------------- moomoo ----

def pull_moomoo(symbol):
    """Daily history from the moomoo vendor feed over the local OpenD channel."""
    import moomoo as ft
    from moomoo import KLType, AuType

    code = "US." + symbol
    ctx = ft.OpenQuoteContext(host=OPEND_HOST, port=OPEND_PORT)
    # OpenD needs an explicit end date; a start-only call returns an empty frame.
    end = datetime.now().strftime("%Y-%m-%d")
    rows = {}
    try:
        page_key = None
        pages = 0
        while True:
            ret, data, page_key = ctx.request_history_kline(
                code, start="1990-01-01", end=end, ktype=KLType.K_DAY,
                autype=AuType.QFQ, max_count=1000, page_req_key=page_key,
            )
            if ret != 0:
                raise RuntimeError("request_history_kline ret={} {}".format(ret, data))
            pages += 1
            for _, r in data.iterrows():
                key = str(r["time_key"])[:10]
                rows[key] = (key, _f4(r["open"]), _f4(r["high"]), _f4(r["low"]),
                             _f4(r["close"]), "{:.0f}".format(float(r["volume"])))
            if not page_key:
                break
            if pages > 40:
                raise RuntimeError("pagination did not terminate")
            time.sleep(0.35)
    finally:
        ctx.close()

    ordered = [rows[k] for k in sorted(rows)]
    prov = provenance(
        "moomoo vendor feed via local OpenD 127.0.0.1:11111 ({}); same feed as the "
        "hosted mcp__moomoo__* tools".format(code),
        symbol, "1d", "forward-adjusted (qfq) per moomoo convention",
        "audit-trail copy for return cross-check; feed retains ~20 years so it "
        "starts 2006-10-02; levels not comparable to Yahoo (different dividend convention)",
    )
    path = os.path.join(DATA, "{}_1d_moomoo.csv".format(symbol))
    return write_csv(path, prov, COLS_MOOMOO, ordered), ordered[0][0], ordered[-1][0]


# ----------------------------------------------------------------- yahoo ----

def yahoo_series(ticker):
    """Full daily history (split-adjusted OHLC + total-return close)."""
    url = ("https://query1.finance.yahoo.com/v8/finance/chart/{}"
           "?period1=0&period2={}&interval=1d&events=div".format(
               ticker.replace("^", "%5E"), int(time.time())))
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    doc = json.loads(urllib.request.urlopen(req, timeout=60).read())
    res = doc["chart"]["result"][0]
    ts, q = res["timestamp"], res["indicators"]["quote"][0]
    adj_blocks = res["indicators"].get("adjclose")
    adj = adj_blocks[0]["adjclose"] if adj_blocks else q["close"]
    rows = {}
    for i, t in enumerate(ts):
        c = q["close"][i]
        if c is None:
            continue
        d = datetime.fromtimestamp(t, timezone.utc).strftime("%Y-%m-%d")
        tr = adj[i] if (adj and adj[i] is not None) else c
        rows[d] = (d, _f4(q["open"][i]), _f4(q["high"][i]), _f4(q["low"][i]),
                   _f4(c), "{:.0f}".format(float(q["volume"][i] or 0)), _f4(tr))
    return [rows[k] for k in sorted(rows)]


def pull_yahoo(symbol, ticker, is_index):
    ordered = yahoo_series(ticker)
    if is_index:
        prov = provenance(
            "Yahoo Finance chart API {}".format(ticker),
            symbol, "1d", "unadjusted index level (no splits, no dividends)",
            "CBOE VIX 30-day constant-maturity implied vol on SPX; moomoo has no "
            "VIX index feed; cross-checked vs TradingView TVC:VIX (agrees within $0.01)",
        )
    else:
        prov = provenance(
            "Yahoo Finance chart API {}".format(ticker),
            symbol, "1d", "split-adjusted traded OHLC; close_tr = total-return close",
            "primary study series; OHLC are actual traded price levels (what a stop "
            "references); close_tr is dividend-reinvested and is used only to "
            "quantify dividend drag, never to trade; split-adjusted close verified "
            "exactly against TradingView",
        )
    path = os.path.join(DATA, "{}_1d.csv".format(symbol))
    return write_csv(path, prov, COLS_FULL, ordered), ordered[0][0], ordered[-1][0]


# ------------------------------------------------------------------ disk ----

def disk_report():
    out = []
    for sym in ALL_SYMBOLS:
        for suffix in ("", "_moomoo"):
            p = os.path.join(DATA, "{}_1d{}.csv".format(sym, suffix))
            if not os.path.exists(p):
                out.append((sym + suffix, "MISSING", "", ""))
                continue
            with io.open(p, encoding="utf-8") as fh:
                body = [l for l in fh.read().split("\n")
                        if l.strip() and not l.startswith("#")]
            dates = [l.split(",")[0] for l in body[1:]]
            out.append((sym + suffix, str(len(dates)), dates[0], dates[-1]))
    return out


def main():
    try:
        sys.stdout.reconfigure(newline="\n", encoding="utf-8")
    except (AttributeError, ValueError):
        pass

    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if not os.path.isdir(DATA):
        os.makedirs(DATA)

    if args.check:
        print("{:<12} {:>7} {:<12} {:<12}".format("file", "rows", "first", "last"))
        for name, n, a, b in disk_report():
            print("{:<12} {:>7} {:<12} {:<12}".format(name, n, a, b))
        return 0

    failures = []
    print("pulling daily history -> {}".format(DATA))

    print("\n[primary] Yahoo full history")
    for sym in ETF_SYMBOLS:
        try:
            n, a, b = pull_yahoo(sym, sym, is_index=False)
            print("  {:<4} {:>6} rows  {} -> {}".format(sym, n, a, b))
        except Exception as exc:
            failures.append((sym, "{}: {}".format(type(exc).__name__, exc)))
            print("  {:<4} FAILED {}".format(sym, exc))
    try:
        n, a, b = pull_yahoo(VIX_SYMBOL, "^VIX", is_index=True)
        print("  {:<4} {:>6} rows  {} -> {}".format("VIX", n, a, b))
    except Exception as exc:
        failures.append(("VIX", "{}: {}".format(type(exc).__name__, exc)))
        print("  {:<4} FAILED {}".format("VIX", exc))

    print("\n[audit trail] moomoo OpenD vendor feed")
    for sym in ETF_SYMBOLS:
        try:
            n, a, b = pull_moomoo(sym)
            print("  {:<4} {:>6} rows  {} -> {}".format(sym, n, a, b))
        except Exception as exc:
            failures.append((sym + "_moomoo", "{}: {}".format(type(exc).__name__, exc)))
            print("  {:<4} FAILED {}".format(sym, exc))

    if failures:
        print("\nFAILURES ({}):".format(len(failures)))
        for sym, msg in failures:
            print("  {} -> {}".format(sym, msg))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
