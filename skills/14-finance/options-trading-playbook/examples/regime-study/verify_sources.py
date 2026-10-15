#!/usr/bin/env python3
"""verify_sources.py - prove the price data is real, and say which feed to trust.

No network: everything is already on disk.  Three checks on real numbers.

 CHECK 1  Yahoo primary vs the moomoo OpenD audit trail, over the overlapping
          2006-10-02+ window, comparing DAILY RETURNS (the invariant that
          survives a corporate-action convention difference) and counting
          "stale" bars - consecutive sessions whose close repeats to 4 decimals.
          Absolute levels are NOT comparable between the two: moomoo folds
          dividends in on its own schedule, so 2006-10-02 SPY reads 108.59 on
          moomoo and 133.08 on Yahoo.  Returns are the fair test; stale-bar
          counts are what decide which feed to trust.

 CHECK 2  Yahoo ^VIX vs the TradingView TVC:VIX fixture captured verbatim from
          `mcp__tradingview__mcp-tv-get-ohlcv` (data/_tvcheck_VIX.csv).

 CHECK 3  Yahoo SPY vs the TradingView AMEX:SPY fixture captured verbatim from
          `mcp__tradingview__mcp-tv-get-ohlcv` (data/_tvcheck_SPY.csv).
          Both sides are split-adjusted traded prices, so levels must match
          tightly here - this is the check that certifies the primary series.

Exit code is 0 when the PRIMARY series is certified (checks 2 and 3 pass).
CHECK 1 is a diagnosis of the second feed, not a gate on the primary one;
its finding is printed with counts and is restated in FINDINGS.md.

  py -3 verify_sources.py
"""
import csv
import io
import os
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

RET_TOL_PP = 0.30        # a return pair differing by more than this is flagged
INDEX_TOL_ABS = 0.05     # VIX / SPY level agreement band vs TradingView


def read_series(path):
    with io.open(path, encoding="utf-8") as fh:
        lines = [l for l in fh.read().split("\n") if l.strip() and not l.startswith("#")]
    return {r["date"]: r for r in csv.DictReader(lines)}


def read_tv_fixture(path):
    """TradingView fixture keyed by UTC session date."""
    with io.open(path, encoding="utf-8") as fh:
        lines = [l for l in fh.read().split("\n") if l.strip() and not l.startswith("#")]
    out = {}
    for r in csv.DictReader(lines):
        d = datetime.fromtimestamp(int(r["t"]), timezone.utc).strftime("%Y-%m-%d")
        out[d] = r
    return out


def stale_bars(series, key="close"):
    """Sessions whose close repeats the previous session's close exactly.

    A multi-day run of byte-identical closes on a liquid ETF is a feed defect,
    not a market event.
    """
    dates = sorted(series)
    n = 0
    runs = []
    run = 1
    for i in range(1, len(dates)):
        a, b = series[dates[i - 1]][key], series[dates[i]][key]
        if a is not None and a == b:
            n += 1
            run += 1
        else:
            if run > 1:
                runs.append((run, dates[i - run], dates[i - 1]))
            run = 1
    if run > 1:
        runs.append((run, dates[len(dates) - run], dates[-1]))
    runs.sort(reverse=True)
    return n, runs


def compare_returns(label, a, b, key, tol_pct):
    da, db = sorted(a), sorted(b)
    pos_a = {d: i for i, d in enumerate(da)}
    pos_b = {d: i for i, d in enumerate(db)}
    common = sorted(set(a) & set(b))
    if len(common) < 3:
        print("  {}: only {} common dates -> FAIL".format(label, len(common)))
        return None
    diffs, skipped = [], 0
    for i in range(1, len(common)):
        d0, d1 = common[i - 1], common[i]
        if pos_a[d1] - pos_a[d0] != 1 or pos_b[d1] - pos_b[d0] != 1:
            skipped += 1
            continue
        try:
            ra = float(a[d1][key]) / float(a[d0][key]) - 1.0
            rb = float(b[d1][key]) / float(b[d0][key]) - 1.0
        except (KeyError, ValueError, ZeroDivisionError):
            continue
        diffs.append((abs(ra - rb) * 100.0, d1))
    if not diffs:
        print("  {}: no comparable pairs -> FAIL".format(label))
        return None
    diffs.sort(reverse=True)
    vals = sorted(d[0] for d in diffs)
    med = vals[len(vals) // 2]
    p95 = vals[int(len(vals) * 0.95)]
    over = [d for d in diffs if d[0] > tol_pct]
    print("  {}: {} pairs ({} skipped non-adjacent) | median diff {:.4f} pp | "
          "p95 {:.4f} pp | worst {:.3f} pp on {} | {} over {:.2f} pp".format(
              label, len(diffs), skipped, med, p95, diffs[0][0], diffs[0][1],
              len(over), tol_pct))
    for v, d in over[:5]:
        print("      big diff {}: {:.3f} pp".format(d, v))
    return over


def compare_levels(label, a, b, key, tol_abs):
    common = sorted(set(a) & set(b))
    if not common:
        print("  {}: NO OVERLAP -> FAIL".format(label))
        return False
    worst, worst_d, over = 0.0, None, 0
    for d in common:
        try:
            va, vb = float(a[d][key]), float(b[d][key])
        except (KeyError, ValueError):
            continue
        diff = abs(va - vb)
        if diff > tol_abs:
            over += 1
        if diff > worst:
            worst, worst_d = diff, d
    ok = over == 0
    print("  {}: {} common dates, worst |diff| = {:.4f} on {} (tol {:.2f}) -> {}".format(
        label, len(common), worst, worst_d, tol_abs, "OK" if ok else "FAIL"))
    return ok


def main():
    try:
        sys.stdout.reconfigure(newline="\n", encoding="utf-8")
    except (AttributeError, ValueError):
        pass

    certified = True

    print("CHECK 1 - primary (Yahoo) vs audit trail (moomoo OpenD), DAILY RETURNS")
    for sym in ["SPY", "QQQ", "IWM", "EEM"]:
        p1 = os.path.join(DATA, "{}_1d.csv".format(sym))
        p2 = os.path.join(DATA, "{}_1d_moomoo.csv".format(sym))
        if not (os.path.exists(p1) and os.path.exists(p2)):
            print("  {}: missing file -> SKIP".format(sym))
            continue
        y, m = read_series(p1), read_series(p2)
        compare_returns("{} close".format(sym), y, m, "close", RET_TOL_PP)
        n_y, runs_y = stale_bars(y)
        n_m, runs_m = stale_bars(m)
        print("      stale bars: yahoo={} (over {} sessions) moomoo={} (over {} sessions)".format(
            n_y, len(y), n_m, len(m)))
        for tag, runs in (("yahoo", runs_y), ("moomoo", runs_m)):
            for ln, s, e in runs[:2]:
                print("        {} repeated close {} sessions {} .. {}".format(tag, ln, s, e))
    print("  interpretation: this is a diagnosis of the second feed.  Absolute levels")
    print("  differ by construction (dividend convention); returns are the fair test,")
    print("  and repeated identical closes mark a feed defect.")

    print("\nCHECK 2 - primary VIX (Yahoo ^VIX) vs TradingView TVC:VIX fixture")
    p1, p2 = os.path.join(DATA, "VIX_1d.csv"), os.path.join(DATA, "_tvcheck_VIX.csv")
    if os.path.exists(p1) and os.path.exists(p2):
        certified &= compare_levels("VIX close", read_series(p1),
                                    read_tv_fixture(p2), "close", INDEX_TOL_ABS)
    else:
        print("  MISSING {} -> cannot certify".format(
            "_tvcheck_VIX.csv" if not os.path.exists(p2) else "VIX_1d.csv"))
        print("  this fixture is captured by hand from the MCP tool (pull_data.py")
        print("  cannot recreate it): mcp__tradingview__mcp-tv-get-ohlcv with")
        print("  symbol=TVC:VIX, interval=1D, count=30, format=columns")
        certified = False

    print("\nCHECK 3 - primary SPY (Yahoo, split-adjusted) vs TradingView AMEX:SPY fixture")
    p1, p2 = os.path.join(DATA, "SPY_1d.csv"), os.path.join(DATA, "_tvcheck_SPY.csv")
    if os.path.exists(p1) and os.path.exists(p2):
        certified &= compare_levels("SPY close", read_series(p1),
                                    read_tv_fixture(p2), "close", INDEX_TOL_ABS)
    else:
        print("  MISSING {} -> cannot certify".format(
            "_tvcheck_SPY.csv" if not os.path.exists(p2) else "SPY_1d.csv"))
        print("  this fixture is captured by hand from the MCP tool (pull_data.py")
        print("  cannot recreate it): mcp__tradingview__mcp-tv-get-ohlcv with")
        print("  symbol=AMEX:SPY, interval=1D, count=10, format=columns")
        certified = False

    print("\n{}".format(
        "PRIMARY SERIES CERTIFIED by TradingView (checks 2 and 3)"
        if certified else "PRIMARY SERIES NOT CERTIFIED"))
    return 0 if certified else 1


if __name__ == "__main__":
    sys.exit(main())
