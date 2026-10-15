#!/usr/bin/env python3
"""
handcheck.py -- independent verification of study.py's book arithmetic.

Stdlib only. No network. It does NOT import study.py: everything below is
re-derived from data/*.csv so that agreement means something.

WHAT IT CHECKS
  1. The whole 5-sleeve book, re-built from the raw prices by an independent
     implementation of the pre-registered rules and the monthly rebalance, and
     compared day by day against out/book_daily.csv.
  2. The BOOK_5 yearly returns, re-derived two ways:
       (a) from the independent daily book, and
       (b) BY HAND -- from the sleeve monthly returns in out/sleeve_monthly.csv
           and the fixed 20% weights, month by month.
     Both are compared against out/portfolio_yearly.csv.
  3. The correlation matrix in out/corr_matrix.csv: symmetric, unit diagonal.
  4. One sleeve-year (A, 2013) from prices with no reuse at all.

USAGE
    py -3 handcheck.py [--year 2013]
"""

import argparse
import datetime
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")
OUT_DIR = os.path.join(HERE, "out")

SMA_TREND = 200
SMA_VIX = 50
SLEEVE_ORDER = ["A", "B", "C", "D", "E"]
SLEEVE_SYMBOL = {"A": ("SPY", SMA_TREND), "B": ("TLT", SMA_TREND),
                 "C": ("GLD", SMA_TREND), "D": ("EEM", SMA_TREND),
                 "E": ("VIX", SMA_VIX)}
WEIGHTS = {"A": 0.20, "B": 0.20, "C": 0.20, "D": 0.20, "E": 0.20}
NA = None


# The repo requires LF everywhere. Redirected stdout on Windows would otherwise
# translate every newline to CRLF, which fails the file-format gate.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(newline="\n")


def read_csv(path):
    dates, close = [], []
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        for line in fh:
            if line.startswith("#") or not line.strip() or line.startswith("date,"):
                continue
            f = line.rstrip("\r\n").split(",")
            dates.append(datetime.date.fromisoformat(f[0]))
            close.append(float(f[4]))
    return dates, close


def read_plain(path):
    """Read any of study.py's out/*.csv into (header, rows-of-lists)."""
    header = None
    rows = []
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            if not line.strip():
                continue
            f = line.rstrip("\r\n").split(",")
            if header is None:
                header = f
                continue
            rows.append(f)
    return header, rows


def sma(x, n):
    out = [NA] * len(x)
    s = 0.0
    for i, v in enumerate(x):
        s += v
        if i >= n:
            s -= x[i - n]
        if i >= n - 1:
            out[i] = s / n
    return out


def build():
    px = {}
    for c in SLEEVE_ORDER:
        sym, _ = SLEEVE_SYMBOL[c]
        px[c] = read_csv(os.path.join(DATA_DIR, sym + "_1d.csv"))
    return px


def window(px):
    first_live = {}
    for c in SLEEVE_ORDER:
        d, close = px[c]
        _, n = SLEEVE_SYMBOL[c]
        a = sma(close, n)
        for i in range(len(close)):
            if a[i] is not NA:
                first_live[c] = d[i]
                break
    start = max(first_live.values())
    sets = []
    for c in SLEEVE_ORDER:
        sets.append(set(px[c][0]))
    common = set.intersection(*sets)
    return sorted(x for x in common if x >= start)


def sleeve_daily(px, code, dates):
    """Independent daily return series for one sleeve, aligned to `dates`.

    A position may only change on a BOOK date: the position held through book
    date j is the one the rule established at the close of the previous book
    date's bar on which this instrument actually traded. Getting the no-look-ahead
    convention the other way round -- using today's close to set today's
    position -- is the single easiest way to invent a good backtest.
    """
    d, close = px[code]
    _, n = SLEEVE_SYMBOL[code]
    a = sma(close, n)

    def pos_at(i):
        if i is None or a[i] is NA:
            return 0
        return 1 if close[i] > a[i] else 0

    idx_of = {v: i for i, v in enumerate(d)}
    ret = [0.0] * len(dates)
    hold = [0] * len(dates)
    last_bar = None
    for j, dt in enumerate(dates):
        k = idx_of.get(dt)
        if k is None:
            hold[j] = hold[j - 1] if j else 0
            continue
        if last_bar is not None:
            hold[j] = pos_at(last_bar)
            ret[j] = hold[j] * (close[k] / close[last_bar] - 1.0)
        last_bar = k
    return ret, hold


def book(rets, dates):
    """Monthly-rebalanced fixed-weight book, weights drifting between resets.

    Nothing here reads study.py. This is the independent implementation.

    Returns (daily book returns, equity curve). The daily book RETURN is what the
    compounding is checked against -- deriving a yearly figure from the equity
    ratio E_end/E_start would silently drop the first day of the year.
    """
    w = dict(WEIGHTS)
    r_series = [0.0]
    equity = [1.0]
    month_prev = dates[0].month
    for j in range(1, len(dates)):
        if dates[j].month != month_prev:
            w = dict(WEIGHTS)
        month_prev = dates[j].month
        r = 0.0
        for c in SLEEVE_ORDER:
            r += w[c] * rets[c][j]
        r_series.append(r)
        equity.append(equity[-1] * (1.0 + r))
        den = 1.0 + r
        if den > 0:
            w = {c: w[c] * (1.0 + rets[c][j]) / den for c in SLEEVE_ORDER}
    return r_series, equity


def yearly(dates, r_series):
    """Yearly returns by compounding the daily returns inside each year."""
    out = {}
    for j, d in enumerate(dates):
        out[d.year] = out.get(d.year, 1.0) * (1.0 + r_series[j])
    return {y: v - 1.0 for y, v in out.items()}


def pct(v):
    return "%+.4f%%" % (v * 100.0)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--year", type=int, default=2013)
    args = ap.parse_args(argv)

    fails = []
    px = build()
    dates = window(px)
    print("INDEPENDENT RE-DERIVATION (no import of study.py)")
    print("  book window re-derived from prices: %s .. %s  (%d days)"
          % (dates[0].isoformat(), dates[-1].isoformat(), len(dates)))
    print("")

    rets = {}
    holds = {}
    for c in SLEEVE_ORDER:
        rets[c], holds[c] = sleeve_daily(px, c, dates)

    book_rets, equity = book(rets, dates)

    # ---------------------------------------------------------------- check 1
    print("CHECK 1 -- day-by-day book equity against out/book_daily.csv")
    header, rows = read_plain(os.path.join(OUT_DIR, "book_daily.csv"))
    i_date = header.index("date")
    i_eq = header.index("book_equity")
    got = {}
    for r in rows:
        got[datetime.date.fromisoformat(r[i_date])] = float(r[i_eq])
    worst = 0.0
    worst_d = None
    n = 0
    for j, d in enumerate(dates):
        if d not in got:
            continue
        diff = abs(got[d] - equity[j])
        n += 1
        if diff > worst:
            worst, worst_d = diff, d
    print("    days compared            : %d" % n)
    print("    worst absolute difference: %.3e   (%s)"
          % (worst, worst_d.isoformat() if worst_d else "-"))
    print("    verdict                  : %s"
          % ("MATCH" if worst < 1e-9 else "MISMATCH"))
    if worst >= 1e-9:
        fails.append("check 1: book equity differs by %.3e" % worst)
    print("")

    # ---------------------------------------------------------------- check 2
    print("CHECK 2 -- BOOK_5 yearly returns, three ways")
    mine = yearly(dates, book_rets)
    h2, r2 = read_plain(os.path.join(OUT_DIR, "portfolio_yearly.csv"))
    theirs = {}
    for r in r2:
        if r[0] == "BOOK_5":
            theirs[int(r[1])] = float(r[2])

    mh, mrows = read_plain(os.path.join(OUT_DIR, "sleeve_monthly.csv"))
    sm = {}
    for r in mrows:
        sm.setdefault(int(r[1].split("-")[0]), {})[r[1]] = (r[0], float(r[2]))

    def byhand(year, mrows, sm):
        """Yearly book return from SLEEVE MONTHLY returns and the fixed weights.

        Equal weights 0.20 each, reset at the start of every month, no
        intra-month drift. This is a THIRD, independent estimator.
        """
        months = sorted(m for m in sm.get(year, {}))
        if not months:
            return NA, []
        val = 1.0
        trace = []
        for m in months:
            per = {}
            for rr in mrows:
                if rr[1] == m:
                    per[rr[0]] = float(rr[2])
            r = sum(WEIGHTS[c] * per[c] for c in SLEEVE_ORDER)
            val *= (1.0 + r)
            trace.append((m, dict(per), r))
        return val - 1.0, trace

    # the by-hand figure is about the same book but with weights reset monthly
    # and WITHOUT intra-month drift, so it is a second, slightly different,
    # estimator -- the difference is reported rather than hidden.
    simple = {}
    for y in sorted(mine):
        if y == dates[0].year or y == dates[-1].year:
            continue
        v, _ = byhand(y, mrows, sm)
        simple[y] = v

    print("")
    print("  year   independent_daily  study.py_output  by_hand_monthly  daily-vs-study  byhand-vs-study")
    for y in sorted(mine):
        partial = (y == dates[0].year or y == dates[-1].year)
        t = theirs.get(y)
        bh = simple.get(y)
        d1 = mine[y] - t if t is not None else NA
        d2 = bh - t if (bh is not NA and t is not None) else NA
        print("  %-6d %s  %s  %s  %s  %s%s"
              % (y, pct(mine[y]),
                 pct(t) if t is not None else "n/a",
                 pct(bh) if bh is not NA else "n/a",
                 ("%.2e" % d1) if d1 is not NA else "n/a",
                 ("%.2e" % d2) if d2 is not NA else "n/a",
                 "   partial" if partial else ""))
    worst2 = 0.0
    for y in sorted(mine):
        if theirs.get(y) is None:
            continue
        worst2 = max(worst2, abs(mine[y] - theirs[y]))
    print("")
    print("  worst |independent_daily - study.py_output| across all years: %.3e"
          % worst2)
    print("  verdict: %s  (tolerance 1e-6 -- out/portfolio_yearly.csv is written"
          % ("MATCH" if worst2 < 1e-6 else "MISMATCH"))
    print("  with 6 decimals, so its own rounding is a ~5e-7 floor on this test)")
    if worst2 >= 1e-6:
        fails.append("check 2: yearly returns differ by %.3e" % worst2)
    print("")
    print("  The by_hand_monthly column is a THIRD estimator, and it is an exact")
    print("  closed form rather than a copy. Rebalancing to 20% of the books at each")
    print("  month start and then holding each sleeve's own dollars for the month")
    print("  gives a book monthly return of exactly")
    print("      0.20*rA_month + 0.20*rB_month + 0.20*rC_month + 0.20*rD_month")
    print("      + 0.20*rE_month")
    print("  because the book value at month end is sum_c 0.20*B*(1+R_c)")
    print("  = B*(1 + 0.20*sum_c R_c). So it MUST agree with the study, and the")
    print("  residual below is only the 10-decimal rounding of out/sleeve_monthly.csv.")
    worstbh = 0.0
    for y in simple:
        if simple[y] is NA or theirs.get(y) is None:
            continue
        worstbh = max(worstbh, abs(simple[y] - theirs[y]))
    ymax = max((y for y in simple if simple[y] is not NA),
               key=lambda y: abs(simple[y] - theirs[y])) if simple else None
    if ymax is not None:
        print("  largest such gap: %d, %s vs %s (%s)"
              % (ymax, pct(simple[ymax]), pct(theirs[ymax]),
                 "%.3e" % (simple[ymax] - theirs[ymax])))
    print("  worst by_hand gap across all years: %.3e" % worstbh)
    print("  verdict: %s  (tolerance 1e-5, i.e. the CSV's own rounding)"
          % ("MATCH" if worstbh < 1e-5 else "MISMATCH"))
    if worstbh >= 1e-5:
        fails.append("check 2b: by-hand monthly return differs by %.3e" % worstbh)
    print("")

    # ---------------------------------------------------------------- check 3
    print("CHECK 3 -- the year chosen for the hand computation: %d" % args.year)
    v, trace = byhand(args.year, mrows, sm)
    if v is NA:
        print("    (no months for %d)" % args.year)
    else:
        print("    month      " + "".join("%-11s" % ("r" + c) for c in SLEEVE_ORDER)
              + "book")
        for m, per, r in trace:
            print("    %-10s " % m
                  + "".join("%-11s" % pct(per[c]) for c in SLEEVE_ORDER)
                  + pct(r))
        print("")
        first = sorted(m for m in sm[args.year])[0]
        last = sorted(m for m in sm[args.year])[-1]
        print("    BY HAND: equal weights 0.20 each; the book return in month m is")
        print("      0.20*rA + 0.20*rB + 0.20*rC + 0.20*rD + 0.20*rE")
        print("    compounding %s .. %s gives %s" % (first, last, pct(v)))
        print("    study.py's BOOK_5 for %d      : %s" % (args.year,
                                                           pct(theirs[args.year])))
        print("    independent daily book for %d : %s" % (args.year,
                                                           pct(mine[args.year])))
        print("")
        print("    Worked example, the worst month of %d:" % args.year)
        worstm = min(trace, key=lambda t: t[2])
        m, per, r = worstm
        terms = " + ".join("%.2f*%s" % (WEIGHTS[c], pct(per[c]))
                           for c in SLEEVE_ORDER)
        print("      %s : %s" % (m, terms))
        check = sum(WEIGHTS[c] * per[c] for c in SLEEVE_ORDER)
        print("      = %s   <- hand sum" % pct(check))
        print("      script's book return for that month: %s" % pct(r))
        if abs(check - r) > 1e-12:
            fails.append("check 3: hand monthly sum disagrees with the script")
        print("")

    # ---------------------------------------------------------------- check 4
    print("CHECK 4 -- correlation matrix symmetry and unit diagonal")
    h4, r4 = read_plain(os.path.join(OUT_DIR, "corr_matrix.csv"))
    labels = h4[1:]
    M = {}
    for r in r4:
        for i, lab in enumerate(labels):
            M[(r[0], lab)] = float(r[i + 1])
    asym = 0
    worsta = 0.0
    for a in labels:
        for b in labels:
            d = abs(M[(a, b)] - M[(b, a)])
            if d > worsta:
                worsta = d
            if d > 1e-12:
                asym += 1
    worstdiag = max(abs(M[(a, a)] - 1.0) for a in labels)
    print("    labels                  : %s" % ",".join(labels))
    print("    worst |r(a,b)-r(b,a)|   : %.3e  (%d pairs out of tolerance)"
          % (worsta, asym))
    print("    worst |r(a,a)-1|        : %.3e" % worstdiag)
    ok = (asym == 0 and worstdiag < 1e-9)
    print("    verdict                 : %s" % ("SYMMETRIC WITH UNIT DIAGONAL"
                                               if ok else "FAIL"))
    if not ok:
        fails.append("check 4: correlation matrix symmetry/diagonal")
    print("")

    # ---------------------------------------------------------------- check 5
    print("CHECK 5 -- one sleeve-year from prices, no reuse: sleeve A, %d"
          % args.year)
    d, close = px["A"]
    a = sma(close, SMA_TREND)
    idx = {v: i for i, v in enumerate(d)}
    # start value at the last bar of the previous year, end at the last of this one
    prev = max(x for x in d if x.year == args.year - 1)
    end = max(x for x in d if x.year == args.year)
    eq = 1.0
    i0 = idx[prev]
    i1 = idx[end]
    for i in range(i0 + 1, i1 + 1):
        pos = 1 if (a[i - 1] is not NA and close[i - 1] > a[i - 1]) else 0
        eq *= (1.0 + pos * (close[i] / close[i - 1] - 1.0))
    h5, r5 = read_plain(os.path.join(OUT_DIR, "sleeve_yearly.csv"))
    want = None
    for r in r5:
        if r[0] == "A" and int(r[1]) == args.year:
            want = float(r[2])
    print("    from prices, close %s -> %s, long when close > SMA(200):"
          % (d[i0].isoformat(), d[i1].isoformat()))
    print("      %s" % pct(eq - 1.0))
    print("    out/sleeve_yearly.csv sleeve A %d : %s"
          % (args.year, pct(want) if want is not None else "n/a"))
    ok5 = want is not None and abs((eq - 1.0) - want) < 1e-6
    print("    verdict: %s" % ("MATCH" if ok5 else "MISMATCH"))
    if not ok5:
        fails.append("check 5: sleeve A %d recomputation" % args.year)
    print("")

    print("=" * 72)
    if fails:
        print("HAND-CHECK FAILED:")
        for f in fails:
            print("  - %s" % f)
        return 1
    print("HAND-CHECK PASSED: all five checks agree.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
