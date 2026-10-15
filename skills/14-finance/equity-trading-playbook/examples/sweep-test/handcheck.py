#!/usr/bin/env python3
"""
handcheck.py -- an INDEPENDENT re-derivation of this study's headline numbers.

It does not import study.py and shares none of its code. It re-reads data/*.csv,
re-builds the calendar and the window from scratch, re-implements the rule with
explicit DOLLAR accounting (study.py works in returns), and recomputes:

  * the Grid-P evaluation window and four named configurations' full-window
    CAGR / Sharpe / max drawdown / positive-year fraction / t;
  * the Bonferroni critical |t| by bisection on the normal CDF (study.py uses
    Acklam's inverse-CDF rational approximation -- a different algorithm),
    including published reference values for m = 1, 12, 30, 56;
  * one calendar year of the pre-registered default BY HAND, with the arithmetic
    printed so a reader can follow it;
  * the max-positivity configuration's headline statistics.

Every comparison prints the two values and the gap. A gap that is not a
rounding artifact is a bug in one of the two files, and this script is the one
that is allowed to be wrong.

USAGE
    py -3 handcheck.py [--year 2015]
"""

import argparse
import datetime
import math
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(newline="\n")

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
OUT = os.path.join(HERE, "out")

GRID_P = ["SPY", "QQQ", "IWM", "EEM", "TLT", "GLD", "EFA", "VNQ"]
DEFAULT_SYMS = ["SPY", "QQQ", "IWM", "EEM"]
NMAX = 250
ANNUALISE = 252
ALPHA = 0.05


# --------------------------------------------------------------------------
# data -- read the CSVs a second time, with a different reader
# --------------------------------------------------------------------------

def read_csv(path):
    rows = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            s = line.strip()
            if not s or s.startswith("#") or s.startswith("date,"):
                continue
            p = s.split(",")
            y, m, d = p[0].split("-")
            rows.append((datetime.date(int(y), int(m), int(d)), float(p[4])))
    return rows


def load(sym):
    return read_csv(os.path.join(DATA, "%s_1d.csv" % sym))


def mean(xs):
    return sum(xs) / len(xs)


def stdev(xs):
    if len(xs) < 2:
        return None
    m = mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def normal_cdf(z):
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def critical_t(m, alpha=ALPHA):
    """Two-sided Bonferroni critical |t| by bisection. Independent of Acklam."""
    target = 1.0 - (alpha / m) / 2.0
    lo, hi = 0.0, 12.0
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if normal_cdf(mid) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


# --------------------------------------------------------------------------
# the rule, in dollars
# --------------------------------------------------------------------------

def signals_full(closes, n):
    """close > SMA(n), computed over the instrument's FULL history."""
    out = [0] * len(closes)
    run = 0.0
    for i, c in enumerate(closes):
        run += c
        if i >= n:
            run -= closes[i - n]
        if i >= n - 1:
            out[i] = 1 if c > run / n else 0
    return out


def positions(full_dates, full_closes, win_dates, n, mode):
    """The position a sleeve HOLDS on each session of the window (0 or 1).

    The signal is read on the instrument's own array -- including the bars
    BEFORE the window, so the rule is live on the window's first session. The
    position held on session i is the signal read at the previous session; in
    monthly mode it is written only on the first trading day of a month.
    """
    fmap = {}
    for i, d in enumerate(full_dates):
        fmap[d] = i
    sig = signals_full(full_closes, n)
    pos = [0] * len(win_dates)
    for i in range(1, len(win_dates)):
        prev = fmap[win_dates[i]] - 1
        if mode == "daily":
            pos[i] = sig[prev]
        elif i == 1 or win_dates[i].month != win_dates[i - 1].month:
            pos[i] = sig[prev]
        else:
            pos[i] = pos[i - 1]
    return pos


def book_equity(win_dates, win_prices, configs, full, mode, start_value=100.0):
    """Dollar accounting of an equal-weight book. Returns (equity, daily_rets)."""
    n = len(win_dates)
    k = len(configs)
    pos = []
    for sym, ma_n in configs:
        rows = full[sym]
        fd = [r[0] for r in rows]
        fc = [r[1] for r in rows]
        pos.append(positions(fd, fc, win_dates, ma_n, mode))
    eq = [0.0] * n
    ret = [0.0] * n
    dollars = [start_value / k] * k
    eq[0] = start_value
    for i in range(1, n):
        if mode == "daily" or win_dates[i].month != win_dates[i - 1].month:
            # the book is reset to 1/k per sleeve: every day in daily mode, and on
            # the first trading day of each month in monthly mode
            dollars = [eq[i - 1] / k] * k
        for j, (sym, _ma) in enumerate(configs):
            p0 = win_prices[sym][i - 1]
            p1 = win_prices[sym][i]
            # a long sleeve holds p1/p0; a flat sleeve holds cash
            if pos[j][i]:
                dollars[j] = dollars[j] * (p1 / p0)
        total = sum(dollars)
        eq[i] = total
        ret[i] = total / eq[i - 1] - 1.0
    return eq, ret


def stats(dates, rets):
    body = rets[1:]
    sd = stdev(body)
    mu = mean(body)
    sharpe = (mu / sd * math.sqrt(ANNUALISE)) if sd and sd > 0 else None
    t = (mu / sd * math.sqrt(len(body))) if sd and sd > 0 else None
    years = (dates[-1] - dates[0]).days / 365.25
    eq_end = 1.0
    for v in body:
        eq_end *= (1.0 + v)
    cagr = (eq_end ** (1.0 / years) - 1.0) if years > 0 else None
    return sharpe, t, cagr


def yearly(dates, rets):
    acc = {}
    for i in range(1, len(rets)):
        y = dates[i].year
        acc[y] = acc.get(y, 1.0) * (1.0 + rets[i])
    return {y: acc[y] - 1.0 for y in acc}


def period_key(kind, d):
    if kind == "Y":
        return (d.year,)
    if kind == "Q":
        return (d.year, (d.month - 1) // 3 + 1)
    if kind == "M":
        return (d.year, d.month)
    raise ValueError(kind)


def period_span(kind, key):
    if kind == "Y":
        return datetime.date(key[0], 1, 1), datetime.date(key[0], 12, 31)
    if kind == "Q":
        s = datetime.date(key[0], 3 * key[1] - 2, 1)
        e = (datetime.date(key[0], 12, 31) if key[1] == 4
             else datetime.date(key[0], 3 * key[1] + 1, 1) - datetime.timedelta(days=1))
        return s, e
    s = datetime.date(key[0], key[1], 1)
    e = (datetime.date(key[0], 12, 31) if key[1] == 12
         else datetime.date(key[0], key[1] + 1, 1) - datetime.timedelta(days=1))
    return s, e


def period_positivity(dates, rets, kind):
    """(positive, complete, fraction, worst) over COMPLETE calendar periods only."""
    acc = {}
    for i in range(1, len(rets)):
        k = period_key(kind, dates[i])
        acc[k] = acc.get(k, 1.0) * (1.0 + rets[i])
    lo, hi = dates[0], dates[-1]
    vals = []
    for k in sorted(acc):
        s, e = period_span(kind, k)
        if s >= lo and e <= hi:
            vals.append(acc[k] - 1.0)
    pos = sum(1 for v in vals if v > 0)
    return pos, len(vals), (pos / len(vals) if vals else None), (min(vals) if vals else None)


def subsets_count(n_items, sizes=(1, 2, 3, 4)):
    """Count of subsets by explicit enumeration -- an independent grid-size check."""
    def rec(start, left, acc):
        if left == 0:
            return 1
        total = 0
        for i in range(start, n_items - left + 1):
            total += rec(i + 1, left - 1, acc + 1)
        return total
    return sum(rec(0, r, 0) for r in sizes)


def max_drawdown_of_equity(eq):
    peak = eq[0]
    worst = 0.0
    for v in eq:
        if v > peak:
            peak = v
        dd = (peak - v) / peak
        if dd > worst:
            worst = dd
    return worst


# --------------------------------------------------------------------------
# grid metadata read back from the real run
# --------------------------------------------------------------------------

def read_grid_csv(path):
    rows = {}
    with open(path, "r", encoding="utf-8") as fh:
        header = fh.readline().strip().split(",")
        for line in fh:
            vals = line.strip().split(",")
            if len(vals) != len(header):
                continue
            rows[vals[0]] = dict(zip(header, vals))
    return rows


def read_kv_csv(path):
    out = {}
    with open(path, "r", encoding="utf-8") as fh:
        fh.readline()
        for line in fh:
            a, b = line.strip().split(",")
            out[a] = b
    return out


def gap(a, b):
    if a is None or b is None:
        return "n/a"
    return "%.3e" % abs(a - b)


def check_config(cid, gridcsv, win_dates, win_prices, full, worst):
    """Recompute one configuration from the grid file and print the gaps."""
    row = gridcsv.get(cid)
    if row is None:
        print("  %-46s NOT FOUND in out/grid_P.csv" % cid)
        return worst
    syms = row["instruments"].split("+")
    ma_n = int(row["ma_days"])
    mode = row["rebalance"]
    eq, ret = book_equity(win_dates, win_prices, [(s, ma_n) for s in syms], full, mode)
    sharpe, t, cagr = stats(win_dates, ret)
    mdd = max_drawdown_of_equity(eq)
    ypos, yn, yfrac, _ = period_positivity(win_dates, ret, "Y")
    g = {k: float(row[k]) for k in ("cagr", "sharpe", "maxdd", "years_frac", "t")}
    print("  %s" % cid)
    print("    CAGR      hand %11.6f   grid %11.6f   gap %s" % (cagr, g["cagr"], gap(cagr, g["cagr"])))
    print("    Sharpe    hand %11.6f   grid %11.6f   gap %s" % (sharpe, g["sharpe"], gap(sharpe, g["sharpe"])))
    print("    maxDD     hand %11.6f   grid %11.6f   gap %s" % (-mdd, g["maxdd"], gap(-mdd, g["maxdd"])))
    print("    pos years hand %11.6f   grid %11.6f   gap %s  (%d of %d)"
          % (yfrac, g["years_frac"], gap(yfrac, g["years_frac"]), ypos, yn))
    print("    t         hand %11.6f   grid %11.6f   gap %s" % (t, g["t"], gap(t, g["t"])))
    return max(worst, abs(cagr - g["cagr"]), abs(sharpe - g["sharpe"]),
               abs(-mdd - g["maxdd"]), abs(yfrac - g["years_frac"]), abs(t - g["t"]))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--year", type=int, default=2015)
    args = ap.parse_args(argv)

    full = {s: load(s) for s in GRID_P}
    date_sets = {s: set(d for d, _ in full[s]) for s in GRID_P}
    split = {s: ([r[0] for r in full[s]], [r[1] for r in full[s]]) for s in GRID_P}
    all_dates = sorted(set.intersection(*date_sets.values()))
    first_ok = max(full[s][NMAX - 1][0] for s in GRID_P)
    win_dates = [d for d in all_dates if d >= first_ok]
    win_prices = {}
    for s in GRID_P:
        fmap = dict(full[s])
        win_prices[s] = [fmap[d] for d in win_dates]
    years = (win_dates[-1] - win_dates[0]).days / 365.25

    print("=" * 96)
    print("handcheck.py -- an independent re-derivation (does not import study.py)")
    print("=" * 96)
    print("  re-read from disk : data/<SYM>_1d.csv for %d instruments" % len(GRID_P))
    print("  bars per instrument: " + ", ".join("%s=%d" % (s, len(full[s])) for s in GRID_P))
    print("  common calendar   : %d sessions, %s .. %s"
          % (len(all_dates), all_dates[0], all_dates[-1]))
    print("  window            : %d sessions, %s .. %s  (%.4f years)"
          % (len(win_dates), win_dates[0], win_dates[-1], years))
    print("  complete years    : %d .. %d (%d)"
          % (win_dates[0].year + 1, win_dates[-1].year - 1, win_dates[-1].year - 1 - win_dates[0].year))
    print("  the moving average is computed over each instrument's FULL history, so the")
    print("  rule is live on the window's first session (a naive window-only SMA would")
    print("  leave every sleeve flat for the first N-1 sessions of the window).")

    gridcsv = read_grid_csv(os.path.join(OUT, "grid_P.csv"))
    worst = 0.0

    print("")
    print("-- CHECK 0: the declared grid size, enumerated from scratch " + "-" * 40)
    n_book = subsets_count(len(GRID_P))
    declared = n_book * 5 * 2
    with open(os.path.join(OUT, "grid_P.csv"), "r", encoding="utf-8") as fh:
        rows_in_file = sum(1 for _ in fh) - 1
    print("    1/2/3/4-subsets of %d instruments, enumerated by recursion = %d books"
          % (len(GRID_P), n_book))
    print("    x 5 moving averages x 2 rebalance modes                     = %d declared" % declared)
    print("    rows actually present in out/grid_P.csv                     = %d" % rows_in_file)
    print("    -> %s" % ("MATCH" if declared == rows_in_file else "MISMATCH"))

    print("")
    print("-- CHECK 1: full-window statistics, recomputed in dollars " + "-" * 41)
    cases = [
        "N200-monthly-SPY",
        "N50-daily-TLT+GLD",
        "N250-daily-SPY+QQQ+IWM+EEM",
        "N200-monthly-" + "+".join(DEFAULT_SYMS),
        "N150-monthly-SPY+GLD",
    ]
    for cid in cases:
        worst = check_config(cid, gridcsv, win_dates, win_prices, full, worst)

    print("")
    print("-- CHECK 2: Bonferroni critical |t| by bisection on the normal CDF " + "-" * 28)
    bon = read_kv_csv(os.path.join(OUT, "bonferroni.csv"))
    m = int(bon["m"])
    crit_hand = critical_t(m)
    crit_file = float(bon["critical_t"])
    print("    m                 : %d  (from out/bonferroni.csv)" % m)
    print("    per-test alpha    : %.12f (from out/bonferroni.csv)" % (ALPHA / m))
    print("    critical |t| hand : %.8f" % crit_hand)
    print("    critical |t| file : %.8f   gap %s" % (crit_file, gap(crit_hand, crit_file)))
    worst = max(worst, abs(crit_hand - crit_file))
    for mm, ref in ((1, 1.959964), (12, 2.864971), (30, 3.143611), (56, 3.322324)):
        c = critical_t(mm)
        print("    cross-check m=%-5d -> %.4f  (published reference %.4f, gap %.2e)"
              % (mm, c, ref, abs(c - ref)))

    print("")
    print("-- CHECK 3: the pre-registered default over %d, computed by hand " % args.year + "-" * 28)
    cfg = [(s, 200) for s in DEFAULT_SYMS]
    eq, ret = book_equity(win_dates, win_prices, cfg, full, "monthly")
    idx = [i for i, d in enumerate(win_dates) if d.year == args.year]
    i0, i1 = idx[0], idx[-1]
    print("    the book is %d equal sleeves, %.4f%% each, N=200, monthly rebalance."
          % (len(cfg), 100.0 / len(cfg)))
    print("    a sleeve holds the bar-to-bar price move on every session it is long and")
    print("    holds cash on every session it is flat; the book is the sum of the sleeves.")
    print("    the year runs %s .. %s (%d sessions)." % (win_dates[i0], win_dates[i1], len(idx)))
    print("    convention: a calendar-year return is the product of the returns EARNED on")
    print("    the year's sessions, i.e. measured from the prior session's close -- the same")
    print("    convention study.py uses, so the base is the session before %s." % win_dates[i0])
    print("    equity on the session before the year = %.10f  (%s)"
          % (eq[i0 - 1], win_dates[i0 - 1]))
    print("    equity on the last  %d session       = %.10f  (%s)"
          % (args.year, eq[i1], win_dates[i1]))
    byhand = eq[i1] / eq[i0 - 1] - 1.0
    print("    year return by hand = (%.10f / %.10f) - 1" % (eq[i1], eq[i0 - 1]))
    print("                        = %+.10f = %+.6f%%" % (byhand, 100 * byhand))
    drow = gridcsv["N200-monthly-" + "+".join(DEFAULT_SYMS)]
    ys = yearly(win_dates, ret)
    complete = list(range(win_dates[0].year + 1, win_dates[-1].year))
    print("    the grid's own year list for this configuration contains %d complete years"
          % int(drow["years_n"]))
    print("    recomputed calendar-year returns, all years present in the window:")
    for y in sorted(ys):
        mark = "" if y in complete else "  (incomplete, excluded from positivity)"
        print("      %d %+10.4f%%%s" % (y, 100 * ys[y], mark))
    if args.year in complete:
        print("    the %d value above must also be recoverable from the grid's own stats."
              % args.year)
        print("    grid worst_year=%s, and %d's return is %+.6f%% (by hand %+.6f%%, gap %.2e)"
              % (drow["worst_year"], args.year, 100 * ys[args.year], 100 * byhand,
                 abs(ys[args.year] - byhand)))

    print("")
    print("-- CHECK 4: the max-positivity configurations, recomputed " + "-" * 42)
    pos = []
    with open(os.path.join(OUT, "positivity.csv"), "r", encoding="utf-8") as fh:
        fh.readline()
        for line in fh:
            pos.append(line.strip().split(","))
    for r in pos:
        if r[1] != "at positive CAGR":
            continue
        cid = r[2]
        row = gridcsv.get(cid)
        if row is None:
            print("    %s not in out/grid_P.csv" % cid)
            continue
        syms = row["instruments"].split("+")
        eq, ret = book_equity(win_dates, win_prices,
                              [(s, int(row["ma_days"])) for s in syms], full, row["rebalance"])
        kind = r[0]
        npos, nn, frac, worstp = period_positivity(win_dates, ret, kind)
        _, _, cagr = stats(win_dates, ret)
        print("    %-2s %s" % (kind, cid))
        print("      positive %-8s hand %3d/%3d = %.6f   file %-8s = %.6f   gap %s"
              % ({"Y": "years", "Q": "quarters", "M": "months"}[kind], npos, nn, frac,
                 r[3], float(r[4]), gap(frac, float(r[4]))))
        print("      worst %-8s hand %.6f%s"
              % ({"Y": "year", "Q": "quarter", "M": "month"}[kind], worstp,
                 "" if kind != "Y" else
                 "   grid worst_year %.6f   gap %s"
                 % (float(row["worst_year"]), gap(worstp, float(row["worst_year"])))))
        print("      CAGR hand %.6f   file %.6f   gap %s"
              % (cagr, float(r[5]), gap(cagr, float(r[5]))))
        worst = max(worst, abs(frac - float(r[4])), abs(cagr - float(r[5])))

    print("")
    print("-- CHECK 5: the rule is live on the window's first session " + "-" * 40)
    eq, ret = book_equity(win_dates, win_prices, [(s, 200) for s in DEFAULT_SYMS], full, "monthly")
    print("    the window's first session is %s; a sleeve with a live signal there is" % win_dates[0])
    print("    NOT flat on day one. First ten sessions of the default's equity curve:")
    for i in range(10):
        print("      %s  equity %10.6f   day return %+.6f%%"
              % (win_dates[i], eq[i], 100 * ret[i]))

    print("")
    print("-- CHECK 6: the 70/30 split boundary, rebuilt independently " + "-" * 40)
    n_all = len(win_dates)
    split = int(math.floor(0.70 * (n_all - 1)))
    print("    split index = floor(0.70 x (n-1)) = floor(0.70 x %d) = %d" % (n_all - 1, split))
    print("    in-sample  : %s .. %s  (%d sessions)" % (win_dates[0], win_dates[split], split + 1))
    print("    held out   : %s .. %s  (%d sessions, first is a base day)"
          % (win_dates[split], win_dates[-1], n_all - split))
    for cid in ("N200-monthly-SPY",
                "N150-monthly-SPY+GLD",
                "N250-daily-SPY+QQQ+IWM+EEM",
                "N200-monthly-" + "+".join(DEFAULT_SYMS)):
        row = gridcsv.get(cid)
        if row is None:
            continue
        syms = row["instruments"].split("+")
        eq, ret = book_equity(win_dates, win_prices,
                              [(s, int(row["ma_days"])) for s in syms], full, row["rebalance"])
        is_d, is_r = win_dates[:split + 1], ret[:split + 1]
        oos_d, oos_r = win_dates[split:], [0.0] + ret[split + 1:]
        s_is, _, c_is = stats(is_d, is_r)
        s_oos, _, c_oos = stats(oos_d, oos_r)
        ipos, in_, ifrac, _ = period_positivity(is_d, is_r, "Y")
        opos, on_, ofrac, _ = period_positivity(oos_d, oos_r, "Y")
        print("    %s" % cid)
        print("      IS  Sharpe hand %10.6f  file %10.6f  gap %s"
              % (s_is, float(row["is_sharpe"]), gap(s_is, float(row["is_sharpe"]))))
        print("      IS  CAGR   hand %10.6f  file %10.6f  gap %s"
              % (c_is, float(row["is_cagr"]), gap(c_is, float(row["is_cagr"]))))
        print("      IS  pos yrs hand %3d/%-3d %8.6f  file %3s/%-3s %8s  (sub-period positivity)"
              % (ipos, in_, ifrac, row["is_years_pos"], row["is_years_n"],
                 row["is_years_frac"]))
        print("      OOS Sharpe hand %10.6f  file %10.6f  gap %s"
              % (s_oos, float(row["oos_sharpe"]), gap(s_oos, float(row["oos_sharpe"]))))
        print("      OOS CAGR   hand %10.6f  file %10.6f  gap %s"
              % (c_oos, float(row["oos_cagr"]), gap(c_oos, float(row["oos_cagr"]))))
        print("      OOS pos yrs hand %3d/%-3d %8.6f  file %3s/%-3s %8s  (sub-period positivity)"
              % (opos, on_, ofrac, row["oos_years_pos"], row["oos_years_n"],
                 row["oos_years_frac"]))
        worst = max(worst, abs(s_is - float(row["is_sharpe"])),
                    abs(c_is - float(row["is_cagr"])),
                    abs(s_oos - float(row["oos_sharpe"])),
                    abs(c_oos - float(row["oos_cagr"])),
                    abs(ifrac - float(row["is_years_frac"])),
                    abs(ofrac - float(row["oos_years_frac"])))

    print("")
    print("=" * 96)
    print("  WORST GAP ACROSS EVERY CHECK: %.3e" % worst)
    print("  A gap at 1e-10 or below is the CSV's own 6-decimal rounding. Above that, one")
    print("  of the two files is wrong. The independent implementation is the one that is")
    print("  allowed to be wrong; if they disagree, the hand arithmetic in CHECK 3 is the")
    print("  tie-breaker, because it is printed and can be followed line by line.")
    print("=" * 96)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
