#!/usr/bin/env python3
"""
handcheck.py -- INDEPENDENT re-derivation of the positivity frontier.

This file does NOT import study.py, does not read out/*.csv as INPUT (it only
reads them at the end, to compare), and does not use the sibling engine.  It
re-derives everything from data/*.csv with its own code:

    * its own CSV reader
    * its own SMA(200) and trend position
    * its own book window, its own sleeve-to-book-date alignment
    * its own book simulator, including its own cost model
    * its own cash accrual
    * its own bucket keys and its own period-completeness rule
    * its own frontier loop and its own CAGR

The specifications are the same as study.py's -- deliberately, since a
disagreement about the SPEC is not what an independent re-derivation tests.  What
is tested is whether the same spec, written twice by different code, produces the
same numbers.  Any gap is printed per cell; a gap larger than the stated
tolerance fails the script.

It additionally does the two things a reader is entitled to see:
    * a DAY-BY-DAY worked example -- the sleeve returns, the weights, the
      rebalance, the cost, the book return, the cash accrual and r(lambda) for a
      handful of consecutive 2015 sessions, so the arithmetic can be checked by
      eye;
    * an INDEPENDENT re-derivation of the frontier's endpoint (the largest lambda
      at which every complete year is positive) at the same 0.001 resolution.

USAGE
    py -3 handcheck.py [--dir .]
"""

import argparse
import datetime
import math
import os
import sys

SMA_TREND = 200
TRADING_DAYS_PER_YEAR = 252
LAMBDA_STEPS = 20
BUCKETS = ["D", "W", "2W", "M", "Q", "H", "Y"]
TOLERANCE = 1e-9          # for the internal, by-hand checks
CSV_TOLERANCE = 5.1e-7    # out/*.csv writes 6 decimals, so half a ulp is 5e-7
TRAIL_TOLERANCE = 1.3e-6  # out/book_daily_*.csv writes 8 decimals; compounding
                          # 252 of them accumulates at most 252 * 5e-9 = 1.26e-6
EXACT_TOLERANCE = 1e-9    # for checks that must be exact, not rounded

BOOK = "R4"
BOOK_WEIGHTS = {"SPY": 0.25, "TLT": 0.25, "GLD": 0.25, "EEM": 0.25}
LONG_BOOK = "R2L"
LONG_WEIGHTS = {"SPY": 0.5, "QQQ": 0.5}

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(newline="\n")


# ---------------------------------------------------------------------------
# I/O
# ---------------------------------------------------------------------------

def read_series(path):
    dates, closes = [], []
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        for line in fh:
            if line.startswith("#") or not line.strip():
                continue
            if line.startswith("date,"):
                continue
            f = line.rstrip("\r\n").split(",")
            dates.append(datetime.date.fromisoformat(f[0]))
            closes.append(float(f[4]))
    return dates, closes


def read_out_csv(path):
    """Read one of study.py's artefact CSVs into (headers, rows-as-lists)."""
    headers, rows = None, []
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        for line in fh:
            if line.startswith("#") or not line.strip():
                continue
            f = line.rstrip("\r\n").split(",")
            if headers is None:
                headers = f
                continue
            rows.append(f)
    return headers, rows


# ---------------------------------------------------------------------------
# Own SMA + trend + alignment
# ---------------------------------------------------------------------------

def moving_average(x, n):
    out = [None] * len(x)
    run = 0.0
    for i in range(len(x)):
        run += x[i]
        if i >= n:
            run -= x[i - n]
        if i >= n - 1:
            out[i] = run / float(n)
    return out


class Trend(object):
    """Own implementation of the same rule: long iff close > SMA(200)."""

    def __init__(self, name, dates, closes):
        self.name = name
        self.dates = dates
        self.closes = closes
        self.at = {d: i for i, d in enumerate(dates)}
        avg = moving_average(closes, SMA_TREND)
        self.avg = avg
        self.long = [None] * len(closes)
        self.first_live = None
        for i in range(len(closes)):
            if avg[i] is None:
                continue
            self.long[i] = closes[i] > avg[i]
            if self.first_live is None:
                self.first_live = dates[i]

    def book_window(self, other_names_at):
        """Own union/intersection logic: dates in EVERY instrument of the set,
        at or after the first date on which this rule is computable."""
        sets = [set(other_names_at[n]) for n in other_names_at]
        self._others = [self]
        return sets

    def aligned(self, book_dates):
        """Own alignment: hold the position established at the close of the
        previous BOOK date's bar; measure the move from that bar's close."""
        n = len(book_dates)
        ret = [0.0] * n
        held = [0] * n
        flip = [False] * n
        prev_bar = None
        for j, d in enumerate(book_dates):
            k = self.at.get(d)
            if k is None:
                ret[j] = 0.0
                held[j] = held[j - 1] if j else 0
                continue
            if prev_bar is not None:
                p = self.long[prev_bar]
                held[j] = 1 if p else 0
                ret[j] = held[j] * (self.closes[k] / self.closes[prev_bar] - 1.0)
            flip[j] = (j > 0 and held[j] != held[j - 1])
            prev_bar = k
        return ret, held, flip


def build(names, series_dir):
    trends = {}
    for n in names:
        d, c = read_series(os.path.join(series_dir, n + "_1d.csv"))
        trends[n] = Trend(n, d, c)
    start = max(trends[n].first_live for n in names)
    common = set(trends[names[0]].dates)
    for n in names[1:]:
        common &= set(trends[n].dates)
    book_dates = sorted(d for d in common if d >= start)
    aligned = {n: trends[n].aligned(book_dates) for n in names}
    return book_dates, aligned


# ---------------------------------------------------------------------------
# Own book simulator
# ---------------------------------------------------------------------------

def run_book(book_dates, aligned, weights, round_trip_bps):
    """Own simulator.  Returns (rets, gross, held, costs).

    `held[j]` is the weight actually held through book date j -- the target set on
    a rebalance day, otherwise the weights drifted by the previous day's sleeve
    returns.  The book's own return is therefore NOT a fixed-weight blend of the
    sleeve returns except on rebalance days, and the worked example below prints
    `held` so a reader can reproduce gross from it exactly.
    """
    names = sorted(weights)
    tot = sum(weights[n] for n in names)
    target = {n: weights[n] / tot for n in names}
    half = (round_trip_bps / 2.0) / 10000.0

    w = dict(target)
    prev_month = book_dates[0].month
    rets = [0.0]
    grosses = [0.0]
    costs = [0.0]
    held = [dict(target)]
    for j in range(1, len(book_dates)):
        cost = 0.0
        for n in names:
            if aligned[n][2][j]:
                cost += half * w[n]
        this_month = book_dates[j].month
        if this_month != prev_month:
            cost += half * 0.5 * sum(abs(target[n] - w[n]) for n in names)
        w_held = (dict(target) if this_month != prev_month else dict(w))
        prev_month = this_month
        gross = sum(w_held[n] * aligned[n][0][j] for n in names)
        held.append(dict(w_held))
        grosses.append(gross)
        costs.append(cost)
        rets.append((1.0 + gross) * (1.0 - cost) - 1.0)
        den = 1.0 + gross
        w = {n: w_held[n] * (1.0 + aligned[n][0][j]) / den for n in names}
    return rets, grosses, held, costs


def run_cash(book_dates, series_dir):
    d, y = read_series(os.path.join(series_dir, "US03M" + "_1d.csv"))
    at = {dd: i for i, dd in enumerate(d)}
    prev = None
    out, used = [0.0] * len(book_dates), [None] * len(book_dates)
    for j in range(1, len(book_dates)):
        k = at.get(book_dates[j - 1])
        if k is not None:
            prev = y[k]
        if prev is None:
            continue
        used[j] = prev
        out[j] = (prev / 100.0) / TRADING_DAYS_PER_YEAR
    return out, used


# ---------------------------------------------------------------------------
# Own bucketing
# ---------------------------------------------------------------------------

def bucket_key(bucket, d):
    if bucket == "D":
        return d.isoformat()
    if bucket == "W":
        y, w, _ = d.isocalendar()
        return "%04d-W%02d" % (y, w)
    if bucket == "2W":
        mon = d - datetime.timedelta(days=d.isoweekday() - 1)
        if mon.isocalendar()[1] % 2 == 0:
            mon = mon - datetime.timedelta(days=7)
        return mon.isoformat()
    if bucket == "M":
        return "%04d-%02d" % (d.year, d.month)
    if bucket == "Q":
        return "%04d-Q%d" % (d.year, (d.month - 1) // 3 + 1)
    if bucket == "H":
        return "%04d-H%d" % (d.year, 1 if d.month <= 6 else 2)
    if bucket == "Y":
        return "%04d" % d.year
    raise ValueError(bucket)


def span(bucket, d):
    if bucket == "D":
        return d, d
    if bucket == "W":
        mon = d - datetime.timedelta(days=d.isoweekday() - 1)
        return mon, mon + datetime.timedelta(days=6)
    if bucket == "2W":
        mon = d - datetime.timedelta(days=d.isoweekday() - 1)
        if mon.isocalendar()[1] % 2 == 0:
            mon = mon - datetime.timedelta(days=7)
        return mon, mon + datetime.timedelta(days=13)
    if bucket == "M":
        first = datetime.date(d.year, d.month, 1)
        nxt = (datetime.date(d.year + 1, 1, 1) if d.month == 12
               else datetime.date(d.year, d.month + 1, 1))
        return first, nxt - datetime.timedelta(days=1)
    if bucket == "Q":
        qm = 3 * ((d.month - 1) // 3) + 1
        end_m = qm + 2
        nxt = (datetime.date(d.year + 1, 1, 1) if end_m == 12
               else datetime.date(d.year, end_m + 1, 1))
        return datetime.date(d.year, qm, 1), nxt - datetime.timedelta(days=1)
    if bucket == "H":
        if d.month <= 6:
            return datetime.date(d.year, 1, 1), datetime.date(d.year, 6, 30)
        return datetime.date(d.year, 7, 1), datetime.date(d.year, 12, 31)
    if bucket == "Y":
        return datetime.date(d.year, 1, 1), datetime.date(d.year, 12, 31)
    raise ValueError(bucket)


def period_returns(book_dates, rets, bucket):
    """Own grouping + own completeness rule + own compounding."""
    order, groups = [], {}
    for j, d in enumerate(book_dates):
        k = bucket_key(bucket, d)
        if k not in groups:
            groups[k] = []
            order.append(k)
        groups[k].append(j)
    d0, d1 = book_dates[0], book_dates[-1]
    out = []
    for k in order:
        idx = groups[k]
        first, last = span(bucket, book_dates[idx[0]])
        if first < d0 or last > d1:
            continue
        curve = 1.0
        for j in idx:
            curve *= (1.0 + rets[j])
        out.append((k, curve - 1.0))
    return out


def frac_positive(book_dates, rets, bucket):
    ps = period_returns(book_dates, rets, bucket)
    if not ps:
        return None
    return sum(1 for _, r in ps if r > 0.0) / float(len(ps))


def cagr(book_dates, rets):
    curve = 1.0
    for r in rets:
        curve *= (1.0 + r)
    yrs = (book_dates[-1] - book_dates[0]).days / 365.25
    return curve ** (1.0 / yrs) - 1.0


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def compare(label, got, want, tol, failures):
    gap = abs(got - want) if (got is not None and want is not None) else float("inf")
    if gap > tol:
        failures.append((label, got, want, gap))
    return gap


def frontier_table(book_dates, risky, cash):
    rows = {}
    for i in range(LAMBDA_STEPS + 1):
        lam = round(i / float(LAMBDA_STEPS), 6)
        r = [lam * a + (1.0 - lam) * b for a, b in zip(risky, cash)]
        rows[lam] = {b: frac_positive(book_dates, r, b) for b in BUCKETS}
        rows[lam]["cagr"] = cagr(book_dates, r)
    return rows


def endpoint(book_dates, risky, cash, bucket="Y", step=0.001):
    """Own bisection: largest lambda with every complete period positive."""
    def allpos(lam):
        r = [lam * a + (1.0 - lam) * b for a, b in zip(risky, cash)]
        ps = period_returns(book_dates, r, bucket)
        return bool(ps) and all(v > 0.0 for _, v in ps)

    if not allpos(0.0):
        return None
    lo = 0.0
    for i in range(1, int(round(1.0 / step)) + 1):
        lam = round(i * step, 6)
        if allpos(lam):
            lo = lam
        else:
            break
    return lo


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=".")
    args = ap.parse_args(argv)
    root = os.path.abspath(args.dir)
    data = os.path.join(root, "data")
    out = os.path.join(root, "out")
    failures = []
    max_gap = 0.0

    print("=" * 78)
    print("HANDCHECK -- independent re-derivation, no import of study.py")
    print("=" * 78)
    print("")

    # ---- (1) the primary book -------------------------------------------
    book_dates, aligned = build(sorted(BOOK_WEIGHTS), data)
    risky, rgross, rheld, rcost = run_book(book_dates, aligned, BOOK_WEIGHTS, 0.0)
    cash, cash_used = run_cash(book_dates, data)
    print("(1) %s rebuilt from data/*.csv: %d book dates, %s..%s"
          % (BOOK, len(book_dates), book_dates[0].isoformat(),
             book_dates[-1].isoformat()))
    mine = frontier_table(book_dates, risky, cash)

    hdr, want = read_out_csv(os.path.join(out, "frontier_%s_rt0.csv" % BOOK))
    lam_col = hdr.index("lambda")
    got_rows = {}
    for r in want:
        got_rows[round(float(r[lam_col]), 2)] = r
    print("    comparing %d lambda rows x 7 buckets against out/frontier_%s_rt0.csv"
          % (len(got_rows), BOOK))
    for lam, row in sorted(mine.items()):
        w = got_rows.get(round(lam, 2))
        if w is None:
            failures.append(("missing lambda %.2f" % lam, None, None, float("inf")))
            continue
        for b in BUCKETS:
            g = compare("%s lam=%.2f %s" % (BOOK, lam, b), row[b],
                        float(w[hdr.index(b)]), CSV_TOLERANCE, failures)
            max_gap = max(max_gap, g)
    print("    max absolute gap across the strict frontier: %.3e" % max_gap)
    print("")

    # ---- (2) the long-window book ---------------------------------------
    ld, la = build(sorted(LONG_WEIGHTS), data)
    lrisky = run_book(ld, la, LONG_WEIGHTS, 0.0)[0]
    lcash, _ = run_cash(ld, data)
    print("(2) %s rebuilt: %d book dates, %s..%s" % (LONG_BOOK, len(ld),
                                                     ld[0].isoformat(),
                                                     ld[-1].isoformat()))
    lmine = frontier_table(ld, lrisky, lcash)
    hdr2, want2 = read_out_csv(os.path.join(out, "frontier_%s_rt0.csv" % LONG_BOOK))
    lam_col2 = hdr2.index("lambda")
    g2 = {round(float(r[lam_col2]), 2): r for r in want2}
    for lam, row in sorted(lmine.items()):
        w = g2.get(round(lam, 2))
        if w is None:
            failures.append(("missing lambda %.2f" % lam, None, None, float("inf")))
            continue
        for b in BUCKETS:
            gap = compare("%s lam=%.2f %s" % (LONG_BOOK, lam, b), row[b],
                          float(w[hdr2.index(b)]), CSV_TOLERANCE, failures)
            max_gap = max(max_gap, gap)
    print("    max absolute gap across both strict frontiers: %.3e" % max_gap)
    print("")

    # ---- (3) cash identity ----------------------------------------------
    print("(3) CASH IDENTITY -- r(0) must be r_cash exactly")
    cc = cagr(book_dates, cash)
    gap = compare("cash identity cagr", cc, mine[0.0]["cagr"],
                  EXACT_TOLERANCE, failures)
    print("    independent cash CAGR   %.10f" % cc)
    print("    independent r(0) CAGR   %.10f" % mine[0.0]["cagr"])
    print("    gap                     %.3e" % gap)
    print("")

    # ---- (4) the endpoint -----------------------------------------------
    print("(4) ENDPOINT -- largest lambda with every complete year positive")
    ep = endpoint(book_dates, risky, cash, "Y")
    print("    independent bisection: %s" % ("n/a" if ep is None else "%.3f" % ep))
    hdr3, want3 = read_out_csv(os.path.join(out, "frontier_end.csv"))
    st = None
    for r in want3:
        if r[0] == BOOK and r[1] == "Y":
            st = r
    study_ep = float(st[3]) if st and st[3] else None
    print("    study.py reported    : %s"
          % ("n/a" if study_ep is None else "%.3f" % study_ep))
    if study_ep is not None and ep is not None:
        print("    gap                  : %.6f" % abs(ep - study_ep))
        if abs(ep - study_ep) > EXACT_TOLERANCE:
            failures.append(("endpoint Y", ep, study_ep, abs(ep - study_ep)))
    print("")

    # ---- (5) day-by-day worked example ----------------------------------
    print("(5) WORKED EXAMPLE -- the arithmetic, day by day")
    print("    Four consecutive book dates around 2015's largest book move, at")
    print("    lambda = 0.25.")
    print("    The book is 25% each; cost is 0 bps here, so r_risky is gross.")
    print("")
    names = sorted(BOOK_WEIGHTS)
    # Pick the four consecutive 2015 sessions containing that year's largest
    # absolute book move, so the example shows something other than flat days.
    y15 = [j for j, d in enumerate(book_dates) if d.year == 2015]
    peak = max(y15, key=lambda j: abs(sum(BOOK_WEIGHTS[n] * aligned[n][0][j]
                                          for n in names)))
    sel = [j for j in range(max(peak - 2, y15[0]), peak + 2) if j <= y15[-1]]
    print("    column 1 is the sleeve return on that session; the four weight")
    print("    columns are the weights ACTUALLY HELD through it, which drift away")
    print("    from 25% between rebalances.")
    print("")
    hdr = (["date"] + ["%s_ret" % n for n in names]
           + ["%s_w" % n for n in names] + ["gross", "risky_ret", "cash_ret",
                                            "r(0.25)"])
    print(("    " + " ".join("%-10s" % c for c in hdr)).rstrip())
    for j in sel:
        rr = sum(rheld[j][nn] * aligned[nn][0][j] for nn in names)
        rl = 0.25 * rr + 0.75 * cash[j]
        print(("    " + " ".join(
            ["%-10s" % book_dates[j].isoformat()]
            + ["%-10.6f" % aligned[nn][0][j] for nn in names]
            + ["%-10.6f" % rheld[j][nn] for nn in names]
            + ["%-10.8f" % rr, "%-10.8f" % rr, "%-10.8f" % cash[j],
               "%-10.10f" % rl])).rstrip())
    print("")
    # hand-compound those four dates and compare to the study's own daily trail
    hb, hw = read_out_csv(os.path.join(out, "book_daily_%s_rt0.csv" % BOOK))
    di = hb.index("date")
    bi = hb.index("book_ret")
    ci = hb.index("cash_ret")
    by = {r[di]: r for r in hw}
    for j in sel:
        key = book_dates[j].isoformat()
        if key not in by:
            continue
        r0 = float(by[key][bi])
        c0 = float(by[key][ci])
        hand_r = sum(rheld[j][nn] * aligned[nn][0][j] for nn in names)
        print("    %s  study book_ret %.8f vs hand %.8f   |gap| %.3e"
              % (key, r0, hand_r, abs(r0 - hand_r)))
        print("              study cash_ret %.8f vs hand %.8f   |gap| %.3e"
              % (c0, cash[j], abs(c0 - cash[j])))
    print("")

    # ---- (6) one year, one lambda, by hand ------------------------------
    print("(6) ONE YEAR AT ONE LAMBDA, COMPOUNDED BY HAND")
    year = 2015
    lam = 0.25
    idx = [j for j, d in enumerate(book_dates) if d.year == year]
    hand = 1.0
    for j in idx:
        hand *= 1.0 + (lam * risky[j] + (1.0 - lam) * cash[j])
    hand -= 1.0
    hy, hyr = read_out_csv(os.path.join(out, "yearly_%s_rt0.csv" % BOOK))
    ycol = hy.index("year")
    lcol = hy.index("lam_%s" % ("%.2f" % lam))
    row = [r for r in hyr if r[ycol] == str(year)][0]
    study_v = float(row[lcol])
    print("    hand: prod over 2015's %d book dates of (1 + 0.25*r_risky + 0.75*r_cash)"
          % len(idx))
    print("    hand  %.10f" % hand)
    print("    study %.10f   (out/yearly_%s_rt0.csv, lam_0.25, year %d)"
          % (study_v, BOOK, year))
    print("    gap   %.3e" % abs(hand - study_v))
    if abs(hand - study_v) > CSV_TOLERANCE:
        failures.append(("2015 at lam 0.25", hand, study_v, abs(hand - study_v)))
    print("    (that gap is the 6-decimal rounding of the yearly CSV.)")
    # and the same year against study's 8-decimal daily trail, which is exact enough
    hb2, hw2 = read_out_csv(os.path.join(out, "book_daily_%s_rt0.csv" % BOOK))
    bi2 = hb2.index("book_ret")
    ci2 = hb2.index("cash_ret")
    hand8 = 1.0
    n8 = 0
    for r in hw2:
        if not r[hb2.index("date")].startswith("%d-" % year):
            continue
        hand8 *= 1.0 + (lam * float(r[bi2]) + (1.0 - lam) * float(r[ci2]))
        n8 += 1
    hand8 -= 1.0
    print("    and recomputed from study's 8-decimal daily trail over %d sessions:"
          % n8)
    print("      %.12f   |gap vs hand %.3e" % (hand8, abs(hand8 - hand)))
    if abs(hand8 - hand) > TRAIL_TOLERANCE:
        failures.append(("2015 at lam 0.25 (8-dp trail)", hand, hand8,
                         abs(hand8 - hand)))
    print("")
    print("    the sleeve returns that built it (unweighted), first and last")
    print("    session of the year, with the book's own return at lambda=1:")
    for j in (idx[0], idx[-1]):
        print("      %s  %s   risky %.8f  cash %.8f  r(0.25) %.8f"
              % (book_dates[j].isoformat(),
                 "  ".join("%s %.6f" % (n, aligned[n][0][j]) for n in names),
                 risky[j], cash[j], lam * risky[j] + (1.0 - lam) * cash[j]))
    print("")

    # ---- verdict --------------------------------------------------------
    print("=" * 78)
    if failures:
        print("HANDCHECK FAILED: %d cell(s) outside tolerance %.0e"
              % (len(failures), TOLERANCE))
        for f in failures[:20]:
            print("   %s: hand=%r study=%r gap=%r" % f)
        return 1
    print("HANDCHECK PASSED: two independent implementations agree on every cell")
    print("  max absolute gap over both frontier tables: %.3e" % max_gap)
    print("  that gap is the 6-decimal rounding of out/*.csv, not a disagreement;")
    print("  the CSV tolerance is %.1e (half a unit in the last written place)."
          % CSV_TOLERANCE)
    print("  the exact checks (cash identity, endpoint bisection) held to %.0e;"
          % EXACT_TOLERANCE)
    print("  the 8-decimal-trail recomputation of 2015 at lambda=0.25 held to %.1e."
          % TRAIL_TOLERANCE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
