#!/usr/bin/env python3
"""
handcheck.py -- re-derive p, b, E, p* and b* for ONE strategy-year from the raw
trade log, printing every intermediate so a human can check the arithmetic, then
compare against the value study.py reported.

Deterministic. Stdlib only.

WHY
    The trade-level formulas are the part of this study most likely to be wrong
    silently: one sign error in E, or averaging losses without flipping the sign,
    produces plausible-looking numbers. This script does the sums by hand from
    the trade log and prints the comparison against study.py's per-year.csv.

    It is deliberately NOT independent of the SIMULATION -- both read the same
    tradelog, which study.py wrote. What it checks is the ARITHMETIC, which is
    where a mistake would be invisible. The independent check of the SIMULATION
    is the Robinhood cross-check of the price series (verify_robinhood.py).

USAGE
    py -3 handcheck.py                     # default: SPY / S1 / 1994
    py -3 handcheck.py SPY S1 2000

EXIT CODES
    0  matched
    1  MISMATCH between the hand computation and study.py's output
    2  input missing
"""

import csv
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT = ("SPY", "S1", "1994")


def table(headers, rows, align=None):
    ncol = len(headers)
    if align is None:
        align = ["r"] * ncol
    cells = [[str(c) for c in r] for r in rows]
    widths = [len(headers[i]) for i in range(ncol)]
    for r in cells:
        for i in range(ncol):
            widths[i] = max(widths[i], len(r[i]))

    def line(r):
        parts = []
        for i in range(ncol):
            parts.append(r[i].ljust(widths[i]) if align[i] == "l"
                         else r[i].rjust(widths[i]))
        return "  " + "  ".join(parts).rstrip()

    out = [line(headers), "  " + "-" * (sum(widths) + 2 * (ncol - 1))]
    for r in cells:
        out.append(line(r))
    return out


def rd(path, year):
    """Read the trade log for one calendar year (grouped by EXIT date).

    R is recomputed from the PRICES, exactly as study.py does:
        R = (exit_px - entry_px) / (entry_px - stop_px)
    The pnl/risk columns are the same quantity rounded to 2 dp for the sibling
    engine's currency maths; using them here instead would introduce a ~4e-6
    disagreement that is a rounding artefact, not a real difference.
    """
    rows = []
    with open(path, "r", encoding="utf-8", newline="") as fh:
        for line in fh:
            if line.startswith("#") or not line.strip() or line.startswith("trade_id"):
                continue
            f = line.rstrip("\r\n").split(",")
            if int(f[2][:4]) == int(year):
                rows.append(dict(tid=f[0], open=f[1], close=f[2],
                                 pnl=float(f[3]), risk=float(f[4]),
                                 entry_px=float(f[6]), stop_px=float(f[7]),
                                 exit_px=float(f[8]),
                                 R=(float(f[8]) - float(f[6]))
                                   / (float(f[6]) - float(f[7]))))
    return rows


def streaks_check():
    """Validate the pre-registered L formula against the realised worst streak.

    L = ln(N)/ln(1/(1-p)) is a PREDICTION of how many consecutive losses to
    expect somewhere in a record of N trades. It is easy to state and easy to
    never check. This counts the actual worst losing run per strategy and puts
    the two side by side.
    """
    import glob
    print("=" * 88)
    print("LOSING-STREAK CHECK -- is the pre-registered L formula in the right ballpark?")
    print("=" * 88)
    print("")
    print("  L_pred  = ln(N)/ln(1/(1-p)), the pre-registered expected longest")
    print("            losing streak, computed from the trade log")
    print("  L_actual= the longest run of consecutive non-winning trades actually")
    print("            recorded (a breakeven trade counts as ending a run)")
    print("")
    rows = []
    for path in sorted(glob.glob(os.path.join(HERE, "tradelogs", "*.csv"))):
        base = os.path.basename(path)[:-4]
        inst, strat = base.split("_")[0], base.split("_")[1]
        rs = []
        with open(path, "r", encoding="utf-8", newline="") as fh:
            for line in fh:
                if line.startswith("#") or line.startswith("trade_id") \
                        or not line.strip():
                    continue
                f = line.rstrip("\r\n").split(",")
                rs.append((float(f[8]) - float(f[6])) / (float(f[6]) - float(f[7])))
        n = len(rs)
        wins = sum(1 for x in rs if x > 0)
        loss = sum(1 for x in rs if x < 0)
        if wins + loss == 0:
            continue
        p = wins / (wins + loss)
        l_pred = math.log(n) / math.log(1.0 / (1.0 - p))
        best = cur = 0
        for x in rs:
            if x <= 0:
                cur += 1
                best = max(best, cur)
            else:
                cur = 0
        rows.append([inst, strat, str(n), "%.4f" % p, "%.2f" % l_pred,
                     str(best), "%.2f" % (l_pred / best) if best else "n/a"])
    print("\n".join(table(["inst", "strat", "n_trades", "p", "L_pred",
                           "L_actual", "L_pred/L_actual"],
                          rows, ["l", "l", "r", "r", "r", "r", "r"])))
    print("")
    ratios = [float(r[6]) for r in rows if r[6] != "n/a"]
    print("  Ratio range: %.2f to %.2f. The formula is an order-of-magnitude guide,"
          % (min(ratios), max(ratios)))
    print("  not a bound: on SPY S2 the realised worst run (15) exceeded the")
    print("  prediction (12.82). Plan for the streak the formula names, and do not")
    print("  treat it as a ceiling -- that is exactly how a live account gets")
    print("  surprised by a sample that looked fine in backtest.")
    return 0


def main(argv=None):
    # Emit LF on every platform: the repository requires LF, and Python's
    # text-mode translation would otherwise write CRLF to a redirected stdout.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(newline="\n")

    argv = list(sys.argv[1:] if argv is None else argv)

    if argv and argv[0] == "--streaks":
        return streaks_check()

    sym, strat, year = (argv + list(DEFAULT))[:3] if argv else DEFAULT

    log = os.path.join(HERE, "tradelogs", "%s_%s.csv" % (sym, strat))
    peryear = os.path.join(HERE, "per-year.csv")
    if not os.path.isfile(log) or not os.path.isfile(peryear):
        print("ERROR: need %s and %s" % (log, peryear))
        return 2

    rows = rd(log, year)
    print("=" * 88)
    print("HAND CHECK -- %s %s, calendar year %s (trades grouped by EXIT date)" % (sym, strat, year))
    print("=" * 88)
    print("")
    print("  raw trades read from %s" % os.path.relpath(log, HERE))
    print("")
    print("  %-10s %-12s %-12s %14s %14s %16s" %
          ("trade_id", "open", "close", "pnl", "risk", "R = pnl/risk"))
    print("  " + "-" * 84)
    for r in rows:
        print("  %-10s %-12s %-12s %14.2f %14.2f %16.6f"
              % (r["tid"], r["open"], r["close"], r["pnl"], r["risk"], r["R"]))
    print("")
    print("  (R is recomputed from entry_px / stop_px / exit_px, the same way")
    print("   study.py does it. pnl/risk is the same number rounded to 2 dp.)")
    print("")

    rs = [r["R"] for r in rows]
    wins = [x for x in rs if x > 0]
    loss = [-x for x in rs if x < 0]
    be = len(rs) - len(wins) - len(loss)
    decided = len(wins) + len(loss)

    if decided == 0 or not wins or not loss:
        print("")
        print("  R multiples: %s" % ", ".join("%.6f" % x for x in rs))
        print("")
        print("  This year cannot be hand-checked with these formulas: it has")
        print("    n=%d trades, %d wins, %d losses" % (len(rs), len(wins), len(loss)))
        print("  b = avg_win/avg_loss is undefined when either side is empty, and")
        print("  study.py reports n/a for exactly this reason (see section 3 of its")
        print("  report, and the per-year table's p/b/E columns).")
        return 2

    print("  R multiples: %s" % ", ".join("%.6f" % x for x in rs))
    print("  n total        = %d" % len(rs))
    print("  wins (R>0)     = %d   %s" % (len(wins), ["%.6f" % x for x in wins]))
    print("  losses (R<0)   = %d   %s" % (len(loss), ["%.6f" % x for x in loss]))
    print("  breakeven(R=0) = %d  (excluded from the win-rate denominator)" % be)
    print("  decided        = %d" % decided)
    print("")

    p = len(wins) / decided
    avg_win = sum(wins) / len(wins)
    avg_loss = sum(loss) / len(loss)
    b = avg_win / avg_loss
    E = p * b - (1.0 - p)
    pstar = 1.0 / (1.0 + b)
    bstar = (1.0 - p) / p

    print("  p       = wins / decided      = %d / %d = %.6f" % (len(wins), decided, p))
    print("  avg_win = sum(wins) / n_wins  = %.6f / %d = %.6f"
          % (sum(wins), len(wins), avg_win))
    print("  avg_loss= sum(loss) / n_loss  = %.6f / %d = %.6f"
          % (sum(loss), len(loss), avg_loss))
    print("  b       = avg_win / avg_loss  = %.6f / %.6f = %.6f"
          % (avg_win, avg_loss, b))
    print("  E       = p*b - (1-p)         = %.6f*%.6f - %.6f = %.6f"
          % (p, b, 1.0 - p, E))
    print("  p*      = 1/(1+b)             = 1/(1+%.6f) = %.6f" % (b, pstar))
    print("  b*      = (1-p)/p             = %.6f/%.6f = %.6f"
          % (1.0 - p, p, bstar))
    print("")
    print("  ALGEBRAIC CROSS-CHECK OF E. The raw-R expectancy per trade is")
    print("    p*avg_win - (1-p)*avg_loss")
    raw_E = p * avg_win - (1.0 - p) * avg_loss
    print("    = %.6f*%.6f - %.6f*%.6f = %.6f"
          % (p, avg_win, 1.0 - p, avg_loss, raw_E))
    print("  and E = p*b - (1-p) divides that by the average loss:")
    print("    raw_E / avg_loss = %.6f / %.6f = %.6f"
          % (raw_E, avg_loss, raw_E / avg_loss))
    print("  which equals E = %.6f to %.2e. So E is in AVERAGE-LOSS UNITS,"
          % (E, abs(E - raw_E / avg_loss)))
    print("  not raw R, and the two formulations are algebraically identical.")
    print("")

    # what study.py reported
    found = None
    with open(peryear, "r", encoding="utf-8", newline="") as fh:
        for f in csv.DictReader(fh):
            if f["instrument"] == sym and f["strategy"] == strat \
                    and f["year"] == str(year):
                found = f
                break
    if not found:
        print("  ERROR: %s/%s/%s not found in per-year.csv" % (sym, strat, year))
        return 2

    print("  STUDY.PY REPORTED (per-year.csv):")
    print("    n_trades = %s   p = %s   b = %s   E = %s"
          % (found["n_trades"], found["p"], found["b"], found["E"]))
    print("")
    print("  HAND COMPUTED:")
    print("    n_trades = %d   p = %.6f   b = %.6f   E = %.6f"
          % (len(rs), p, b, E))
    print("")
    # per-year.csv stores p/b/E to 6 decimals, so the comparison tolerance must
    # absorb that rounding (5e-7) and nothing more.
    ok = (int(found["n_trades"]) == len(rs)
          and abs(float(found["p"]) - p) <= 1e-6
          and abs(float(found["b"]) - b) <= 1e-6
          and abs(float(found["E"]) - E) <= 1e-6)
    if ok:
        print("  MATCH: the script and the hand computation agree to 6 dp.")
        return 0
    print("  MISMATCH -- investigate before trusting the trade-level tables.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
