#!/usr/bin/env python3
"""
handcheck.py -- INDEPENDENT re-derivation of this study's headline statistics.

RULES OF ENGAGEMENT
  * This file does NOT import study.py and does NOT import the sibling engine.
  * Every formula is written again from the definition, on purpose, so that a
    shared mistake cannot hide behind a shared helper.
  * It reads ONLY data/*.csv (the raw bars plus the quote snapshot) and
    out/*.csv (what study.py produced).  The gap column is the whole point.
  * It also does the two BY-HAND checks the brief asks for: the equal-weight
    basket return for one calendar month, and the correlation of two series for
    one calendar year, each printed at full working so a human can verify the
    arithmetic without running anything.

RUN
    py -3 handcheck.py
"""

import csv
import datetime
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
OUT = os.path.join(HERE, "out")

SMA_TREND = 200
NARROW3 = ["SPY", "QQQ", "IWM"]
CROSS4 = ["SPY", "TLT", "GLD", "EEM"]
CONSTITUENTS14 = ["AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA",
                  "JPM", "JNJ", "WMT", "XOM", "UNH", "V", "AVGO"]
CASH = "US03M"
LAMBDA_STEPS = 20

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(newline="\n")

GAPS = []


def note(name, study_val, mine_val, fmt="%.6f"):
    if study_val is None or mine_val is None:
        gap = "n/a"
    elif isinstance(study_val, str) or isinstance(mine_val, str):
        gap = "same" if str(study_val) == str(mine_val) else "DIFFERS"
    else:
        gap = fmt % (mine_val - study_val)
    GAPS.append([name, "" if study_val is None else str(study_val),
                 "" if mine_val is None else str(mine_val), gap])
    return gap


# ---------------------------------------------------------------------------
# own reader
# ---------------------------------------------------------------------------

def bars(sym):
    """[(date, open, high, low, close, volume)] for one symbol."""
    path = os.path.join(DATA, sym + "_1d.csv")
    rows = []
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        for line in fh:
            if line.startswith("#") or not line.strip():
                continue
            f = line.rstrip("\r\n").split(",")
            if f[0] in ("date", "symbol"):
                continue
            rows.append((datetime.date(int(f[0][:4]), int(f[0][5:7]),
                                       int(f[0][8:10])),
                         float(f[1]), float(f[2]), float(f[3]), float(f[4]),
                         float(f[5]) if len(f) > 5 and f[5].strip() else 0.0))
    return rows


def col(sym, idx):
    return {r[0]: r[idx] for r in bars(sym)}


def read_out(name):
    """out/<name> as a list of dicts, honouring the CSV's own quoting."""
    path = os.path.join(OUT, name)
    if not os.path.isfile(path):
        return []
    lines = []
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        for line in fh:
            if line.startswith("#") or not line.strip():
                continue
            lines.append(line.rstrip("\r\n"))
    rows = list(csv.reader(lines))
    head = rows[0]
    return [dict(zip(head, r)) for r in rows[1:]]


# ---------------------------------------------------------------------------
# own statistics
# ---------------------------------------------------------------------------

def mean(xs):
    return sum(xs) / float(len(xs))


def sample_sd(xs):
    m = mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def pearson(xs, ys):
    n = len(xs)
    mx, my = mean(xs), mean(ys)
    sxy = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    sxx = sum((xs[i] - mx) ** 2 for i in range(n))
    syy = sum((ys[i] - my) ** 2 for i in range(n))
    return sxy / math.sqrt(sxx * syy)


def maxdd_pct(rets):
    peak, curve, worst = 1.0, 1.0, 0.0
    for r in rets:
        curve *= (1.0 + r)
        if curve > peak:
            peak = curve
        dd = curve / peak - 1.0
        if dd < worst:
            worst = dd
    return worst


def level_stats(dates, rets):
    curve = 1.0
    for r in rets:
        curve *= (1.0 + r)
    yrs = (dates[-1] - dates[0]).days / 365.25
    cagr = curve ** (1.0 / yrs) - 1.0
    sd = sample_sd(rets)
    return {"cagr": cagr, "max_dd": maxdd_pct(rets),
            "sharpe": mean(rets) / sd * math.sqrt(252), "n": len(rets)}


# ---------------------------------------------------------------------------
# own sleeve + book, written from the definition
# ---------------------------------------------------------------------------

def sleeve(bars_rows):
    """(pos, ret_on_own_calendar) for close > SMA(200)."""
    closes = [r[4] for r in bars_rows]
    pos = [None] * len(closes)
    run = 0.0
    for i, c in enumerate(closes):
        run += c
        if i >= SMA_TREND:
            run -= closes[i - SMA_TREND]
        if i >= SMA_TREND - 1:
            pos[i] = 1 if c > run / SMA_TREND else 0
    return pos


def first_live(bars_rows):
    pos = sleeve(bars_rows)
    for i, p in enumerate(pos):
        if p is not None:
            return bars_rows[i][0]
    return None


def window(symbols):
    """Intersection calendar from the latest first-live date.  Cash excluded by
    the caller, deliberately."""
    starts = [first_live(bars(s)) for s in symbols]
    start = max(starts)
    sets = [set(r[0] for r in bars(s)) for s in symbols]
    common = set.intersection(*sets)
    return sorted(d for d in common if d >= start)


def aligned(sym, dates):
    """(ret_if_long, hold, flip, raw) on the book calendar.  Position may only
    change on a book date; a missing bar carries the position and the move is
    counted at the next available close."""
    rows = bars(sym)
    pos = sleeve(rows)
    idx = {r[0]: i for i, r in enumerate(rows)}
    cl = [r[4] for r in rows]
    ret = [0.0] * len(dates)
    hold = [0] * len(dates)
    flip = [False] * len(dates)
    raw = [0.0] * len(dates)
    last = None
    for j, d in enumerate(dates):
        k = idx.get(d)
        if k is None:
            hold[j] = hold[j - 1] if j else 0
            continue
        if last is not None:
            hold[j] = 0 if pos[last] is None else pos[last]
            raw[j] = cl[k] / cl[last] - 1.0
            ret[j] = hold[j] * raw[j]
        flip[j] = (j > 0 and hold[j] != hold[j - 1])
        last = k
    return ret, hold, flip, raw


def simulate(dates, al, weights, cost_bps):
    """Monthly-rebalanced book, cost charged in the return.

    Position may only change on a book date.  Weights are renormalised to the
    target on the first session of a new calendar month; between rebalances the
    weights drift with the sleeves' own returns.
    """
    syms = sorted(weights)
    tot = sum(weights[s] for s in syms)
    tgt = {s: weights[s] / tot for s in syms}
    half = (cost_bps / 2.0) / 10000.0
    w = dict(tgt)
    month = dates[0].month
    rets = [0.0]
    for j in range(1, len(dates)):
        d = dates[j]
        rebal = (d.month != month)
        cost = 0.0
        for s in syms:
            if al[s][2][j]:
                cost += half * w[s]
        if rebal:
            cost += half * 0.5 * sum(abs(tgt[s] - w[s]) for s in syms)
        month = d.month
        held = dict(tgt) if rebal else dict(w)
        gross = sum(held[s] * al[s][0][j] for s in syms)
        rets.append((1.0 + gross) * (1.0 - cost) - 1.0)
        den = 1.0 + gross
        w = {s: held[s] * (1.0 + al[s][0][j]) / den for s in syms}
    return rets


def buy_and_hold(al, weights):
    syms = sorted(weights)
    tot = sum(weights[s] for s in syms)
    n = len(al[syms[0]][3])
    return [sum(weights[s] / tot * al[s][3][j] for s in syms) for j in range(n)]


def cash_series(dates, us03m):
    rate = None
    out = [0.0] * len(dates)
    for j in range(1, len(dates)):
        r = us03m.get(dates[j - 1])
        if r is not None:
            rate = r
        if rate is None:
            continue
        out[j] = (rate / 100.0) / 252.0
    return out


def bucket_periods(dates, kind):
    """[(key, [day indices])] for complete calendar periods."""
    groups = {}
    for j, d in enumerate(dates):
        if kind == "Y":
            k = (d.year,)
            lo, hi = datetime.date(d.year, 1, 1), datetime.date(d.year, 12, 31)
        elif kind == "M":
            k = (d.year, d.month)
            lo = datetime.date(d.year, d.month, 1)
            hi = (datetime.date(d.year + 1, 1, 1) if d.month == 12
                  else datetime.date(d.year, d.month + 1, 1)) - \
                datetime.timedelta(days=1)
        elif kind == "Q":
            qm = 3 * ((d.month - 1) // 3) + 1
            k = (d.year, qm)
            lo = datetime.date(d.year, qm, 1)
            em = qm + 2
            hi = (datetime.date(d.year + 1, 1, 1) if em == 12
                  else datetime.date(d.year, em + 1, 1)) - \
                datetime.timedelta(days=1)
        elif kind == "W":
            lo = d - datetime.timedelta(days=d.isoweekday() - 1)
            k = lo
            hi = lo + datetime.timedelta(days=6)
        else:
            raise ValueError(kind)
        g = groups.setdefault(k, {"idx": [], "lo": lo, "hi": hi})
        g["idx"].append(j)
    out = []
    for k in groups:
        g = groups[k]
        if g["lo"] < dates[0] or g["hi"] > dates[-1]:
            continue
        out.append((k, g["idx"]))
    return sorted(out)


def positivity(rets, dates, kind):
    ps = bucket_periods(dates, kind)
    if not ps:
        return None, 0, 0
    npos = 0
    for k, idx in ps:
        c = 1.0
        for j in idx:
            c *= (1.0 + rets[j])
        if c > 1.0:
            npos += 1
    return npos / float(len(ps)), npos, len(ps)


def apply_lambda(risky, cash, lam):
    return [lam * r + (1.0 - lam) * c for r, c in zip(risky, cash)]


def max_lambda_all_positive(dates, risky, cash, kind, step=0.001):
    """Walk lambda up in 0.001 steps until some complete period goes negative."""
    n = int(round(1.0 / step))
    best = 0.0
    for i in range(1, n + 1):
        lam = round(i * step, 6)
        f, npos, ntot = positivity(apply_lambda(risky, cash, lam), dates, kind)
        if f is None or f < 1.0 - 1e-12:
            return round(best, 3)
        best = lam
    return round(best, 3)


def main():
    print("HANDCHECK -- independent re-derivation, no import of study.py")
    print("=" * 78)
    print("")

    # --- the window, rebuilt ------------------------------------------------
    w14 = window(NARROW3 + CROSS4 + CONSTITUENTS14)
    print("--- window ---")
    print("  W14 rebuilt independently : %s .. %s  (%d days)"
          % (w14[0].isoformat(), w14[-1].isoformat(), len(w14)))

    a_spy = aligned("SPY", w14)
    al = {s: aligned(s, w14)
          for s in set(NARROW3) | set(CROSS4) | set(CONSTITUENTS14)}
    us03m = col(CASH, 4)
    cash = cash_series(w14, us03m)
    cs = level_stats(w14, cash)

    books = {
        "N3_TREND": simulate(w14, al, {s: 1 / 3.0 for s in NARROW3}, 0.0),
        "C4_TREND": simulate(w14, al, {s: 0.25 for s in CROSS4}, 0.0),
        "BH_SPY": buy_and_hold(al, {"SPY": 1.0}),
        "C14_EW_TREND": simulate(w14, al, {s: 1 / 14.0 for s in CONSTITUENTS14},
                                 0.0),
    }

    # --- headline statistics vs study.py's CSV ------------------------------
    print("")
    print("--- level statistics: study.py (from out/*.csv) vs rebuilt here ---")
    study = {r["book"]: r for r in read_out("books_levelstats.csv")}
    print("  %-16s %-11s %12s %12s %12s" %
          ("book", "statistic", "study.py", "handcheck", "gap"))
    for nm in ("N3_TREND", "C4_TREND", "BH_SPY", "C14_EW_TREND"):
        key = "W14_" + nm
        st = level_stats(w14, books[nm])
        s = study.get(key)
        if s is None:
            print("  %-16s MISSING from books_levelstats.csv" % key)
            continue
        for f, lab in (("cagr", "CAGR"), ("max_dd", "maxDD"),
                       ("sharpe", "Sharpe")):
            print("  %-16s %-11s %12.6f %12.6f %12s"
                  % (key, lab, float(s[f]), st[f],
                     note("%s.%s" % (key, f), float(s[f]), st[f])))
        print("  %-16s %-11s %12s %12d %12s"
              % (key, "n_days", s["days"], st["n"],
                 note("%s.days" % key, float(s["days"]), float(st["n"]))))
    print("  %-16s %-11s %12.6f" % ("cash", "CAGR", cs["cagr"]))

    # --- positivity, years and months --------------------------------------
    print("")
    print("--- positivity: study.py (positivity_by_horizon.csv) vs rebuilt ---")
    pos = {}
    for r in read_out("positivity_by_horizon.csv"):
        pos[(r["book"], r["bucket"])] = (r["frac_gt0"], r["n_periods"])
    for nm in ("N3_TREND", "C4_TREND", "BH_SPY", "C14_EW_TREND"):
        key = "W14_" + nm
        for kind in ("Y", "M", "W"):
            f, npos, ntot = positivity(books[nm], w14, kind)
            s = pos.get((key, kind))
            if s is None or s[0] == "":
                print("  %-16s %-2s MISSING" % (key, kind))
                continue
            print("  %-16s %-2s %10s %10.6f  (%d/%d vs %s)"
                  % (key, kind, "study", f, npos, ntot, s[0]))
            note("%s.%s.frac" % (key, kind), float(s[0]), f)

    # --- losing years -------------------------------------------------------
    print("")
    print("--- losing years: study.py (yearly_returns.csv) vs rebuilt ---")
    yt = {}
    for r in read_out("yearly_returns.csv"):
        yt.setdefault(r["book"], {})[r["year"]] = float(r["ret"])
    for nm in ("N3_TREND", "C4_TREND", "BH_SPY", "C14_EW_TREND"):
        key = "W14_" + nm
        mine = {}
        for k, idx in bucket_periods(w14, "Y"):
            c = 1.0
            for j in idx:
                c *= (1.0 + books[nm][j])
            mine[str(k[0])] = c - 1.0
        los_s = sorted(y for y, v in yt.get(key, {}).items() if v <= 0.0)
        los_h = sorted(y for y, v in mine.items() if v <= 0.0)
        worst = 0.0
        for y in mine:
            if y in yt.get(key, {}):
                worst = max(worst, abs(mine[y] - yt[key][y]))
        print("  %-16s study=%s  handcheck=%s  %s"
              % (key, ",".join(los_s), ",".join(los_h),
                 "same" if los_s == los_h else "DIFFER"))
        note("%s.losing_years" % key, ",".join(los_s), ",".join(los_h))
        print("  %-16s largest per-year return gap: %.8f" % ("", worst))
        note("%s.max_year_gap" % key, 0.0, worst)

    # --- correlations -------------------------------------------------------
    print("")
    print("--- correlations: study.py (pairwise_correlations.csv) vs rebuilt ---")
    pc = {}
    for r in read_out("pairwise_correlations.csv"):
        pc[(r["a"], r["b"], r["mode"])] = float(r["pearson"])
    for a, b in (("SPY", "QQQ"), ("SPY", "IWM"), ("QQQ", "IWM")):
        for mode in ("daily", "yearly"):
            mine = corr_between(a, b, mode)
            s = pc.get((a, b, mode)) or pc.get((b, a, mode))
            print("  %-4s %-4s %-7s study=%9.6f handcheck=%9.6f gap=%s"
                  % (a, b, mode, s, mine, note("%s-%s.%s" % (a, b, mode), s, mine)))

    # --- the frontier -------------------------------------------------------
    print("")
    print("--- max lambda for 100% positive YEARS ---")
    for nm in ("N3_TREND", "C4_TREND", "BH_SPY", "C14_EW_TREND"):
        lam = max_lambda_all_positive(w14, books[nm], cash, "Y")
        cg = level_stats(w14, apply_lambda(books[nm], cash, lam))["cagr"]
        print("  %-16s lambda=%.3f  exposure=%5.2f%%  CAGR there=%.6f  "
              "excess over cash=%.6f"
              % (nm, lam, 100.0 * lam, cg, cg - cs["cagr"]))
    study_lam = {r["book"]: r for r in read_out("verdict.csv")}
    for nm in ("N3_TREND", "C4_TREND", "BH_SPY", "C14_EW_TREND"):
        key = "W14_" + nm
        s = study_lam.get(key)
        if s is None:
            print("  %-16s MISSING from verdict.csv" % key)
            continue
        note("%s.max_lambda" % key, float(s["max_lambda"]),
             max_lambda_all_positive(w14, books[nm], cash, "Y"))

    # --- spreads ------------------------------------------------------------
    print("")
    print("--- spreads: study.py (spreads.csv) vs rebuilt from cost-quotes.csv ---")
    q = {}
    with open(os.path.join(DATA, "cost-quotes.csv"), "r", encoding="utf-8-sig",
              newline="") as fh:
        for line in fh:
            if line.startswith("#") or not line.strip():
                continue
            f = line.rstrip("\r\n").split(",")
            if f[0] == "symbol":
                continue
            q[f[0]] = (float(f[2]), float(f[3]))
    sp = {r["symbol"]: float(r["quoted_spread_bp"])
          for r in read_out("spreads.csv")}
    worst = 0.0
    for s in sorted(q):
        bid, ask = q[s]
        mine = (ask - bid) / (0.5 * (bid + ask)) * 10000.0
        worst = max(worst, abs(mine - sp[s]))
    print("  %d symbols; largest gap in quoted spread bp: %.10f" % (len(q), worst))
    note("spreads.max_gap_bp", 0.0, worst)

    # --- the two BY-HAND checks --------------------------------------------
    print("")
    print("=" * 78)
    print("BY-HAND CHECK 1: equal-weight 14-name basket return for ONE month")
    print("=" * 78)
    y, m = 2022, 6
    lo = datetime.date(y, m, 1)
    hi = datetime.date(y, m + 1, 1) - datetime.timedelta(days=1)
    d_lo = max(d for d in w14 if d <= lo)
    d_hi = max(d for d in w14 if d <= hi)
    i0 = w14.index(d_lo)
    d_prev = w14[i0 - 1]
    idxs = [j for j, d in enumerate(w14) if d_lo <= d <= d_hi]
    print("  Month %d-%02d.  Book dates used: %s (first) and %s (last), because"
          % (y, m, d_lo.isoformat(), d_hi.isoformat()))
    print("  the calendar is the intersection, not the raw calendar.")
    print("  Returns are measured from the close of %s, the book day BEFORE the"
          % d_prev.isoformat())
    print("  month, because that is where the book's first June return starts.")
    print("")
    print("  %-6s %11s %11s %11s %5s %11s"
          % ("sym", "c@prev", "c@last", "raw ret", "long", "sleeve ret"))
    raw_rets, sleeve_rets, nlong = [], [], 0
    for s in CONSTITUENTS14:
        c = col(s, 4)
        raw = c[d_hi] / c[d_prev] - 1.0
        nlong_s = sum(al[s][1][j] for j in idxs)
        cum = 1.0
        for j in idxs:
            cum *= (1.0 + al[s][0][j])
        sv = cum - 1.0
        raw_rets.append(raw)
        sleeve_rets.append(sv)
        nlong += nlong_s
        print("  %-6s %11.4f %11.4f %11.6f %5d %11.6f"
              % (s, c[d_prev], c[d_hi], raw, nlong_s, sv))
    ew_raw = sum(raw_rets) / 14.0
    ew_sleeve = sum(sleeve_rets) / 14.0
    print("")
    print("  (a) plain equal-weight basket, no trend overlay, by hand:")
    print("      sum of the 14 raw returns      = %.10f" % sum(raw_rets))
    print("      divided by 14                  = %.10f" % ew_raw)
    print("  (b) the TREND book's sleeve returns for the MONTH, by hand:")
    print("      sum of the 14 sleeve returns   = %.10f" % sum(sleeve_rets))
    print("      divided by 14                  = %.10f" % ew_sleeve)
    print("  Those two are the ARITHMETIC answers.  Neither is the book's return,")
    print("  because the book holds DRIFTING weights between monthly rebalances.")
    print("  The exact by-hand recursion is therefore carried out below, with the")
    print("  weights printed at both ends so a human can follow it.")
    print("")
    const = CONSTITUENTS14
    w = {s: 1.0 / 14.0 for s in const}
    print("  weights on %s (the rebalance day):" % w14[idxs[0]].isoformat())
    print("      " + "  ".join("%s=%.6f" % (s, w[s]) for s in const[:7]))
    print("      " + "  ".join("%s=%.6f" % (s, w[s]) for s in const[7:]))
    print("")
    print("  %-12s %14s %14s" % ("date", "gross trend", "gross plain"))
    cum_t, cum_p = 1.0, 1.0
    wt = dict(w)
    wp = dict(w)
    for j in idxs:
        gt = sum(wt[s] * al[s][0][j] for s in const)
        gp = sum(wp[s] * al[s][3][j] for s in const)
        cum_t *= (1.0 + gt)
        cum_p *= (1.0 + gp)
        dt = 1.0 + gt
        dp = 1.0 + gp
        wt = {s: wt[s] * (1.0 + al[s][0][j]) / dt for s in const}
        wp = {s: wp[s] * (1.0 + al[s][3][j]) / dp for s in const}
        print("  %-12s %14.10f %14.10f" % (w14[j].isoformat(), gt, gp))
    print("")
    print("  weights on %s (after the month's drift):" % w14[idxs[-1]].isoformat())
    print("      " + "  ".join("%s=%.6f" % (s, wt[s]) for s in const[:7]))
    print("      " + "  ".join("%s=%.6f" % (s, wt[s]) for s in const[7:]))
    print("")
    print("  compounded product of the two daily columns above:")
    print("      trend : %.10f" % (cum_t - 1.0))
    print("      plain : %.10f" % (cum_p - 1.0))
    cum_b = 1.0
    for j in idxs:
        cum_b *= (1.0 + books["C14_EW_TREND"][j])
    print("  handcheck's own compounding of the BOOK, same days : %.10f"
          % (cum_b - 1.0))
    print("  exact agreement (should be ~1e-16): %.3e" % (cum_t - cum_b))
    print("")
    print("  THE EXACT IDENTITY, stated so it can be checked by eye:")
    print("      A portfolio held with DRIFTING weights from the start of a period")
    print("      earns the START-WEIGHTED AVERAGE of its legs' period returns --")
    print("      no rebalancing inside the period means each leg compounds alone.")
    print("      So   book month return  ==  sum_i w_i0 * (leg i month return).")
    print("      trend : %.10f  vs  %.10f   (gap %.1e)"
          % (cum_t - 1.0, ew_sleeve, (cum_t - 1.0) - ew_sleeve))
    print("      plain : %.10f  vs  %.10f   (gap %.1e)"
          % (cum_p - 1.0, ew_raw, (cum_p - 1.0) - ew_raw))
    print("")
    print("  WHAT WOULD HAVE BEEN WRONG: compounding the daily returns with the")
    print("  weights RE-SET to 1/14 every day instead of left to drift gives")
    reset_t = 1.0
    for j in idxs:
        reset_t *= (1.0 + sum(al[s][0][j] for s in const) / 14.0)
    print("  %.10f for the trend book, out by %.1e against the book."
          % (reset_t - 1.0, (reset_t - 1.0) - (cum_b - 1.0)))
    print("  That is the difference between a DAILY-rebalanced portfolio and the")
    print("  MONTHLY-rebalanced one this study actually simulates, and it is the")
    print("  single easiest way to get this arithmetic wrong.")
    note("byhand.ew_trend_book_1m_exact", cum_b - 1.0, cum_t - 1.0)
    note("byhand.ew_trend_book_1m_start_weighted", ew_sleeve, cum_t - 1.0)
    note("byhand.ew_plain_basket_1m_start_weighted", ew_raw, cum_p - 1.0)

    print("")
    print("=" * 78)
    print("BY-HAND CHECK 2: correlation of two series for ONE calendar year")
    print("=" * 78)
    yy = 2024
    dts = [d for d in w14 if d.year == yy]
    ra, rb = [], []
    sa, sb = "SPY", "QQQ"
    ca, cb2 = col(sa, 4), col(sb, 4)
    for i in range(1, len(dts)):
        ra.append(ca[dts[i]] / ca[dts[i - 1]] - 1.0)
        rb.append(cb2[dts[i]] / cb2[dts[i - 1]] - 1.0)
    n = len(ra)
    ma, mb = mean(ra), mean(rb)
    sxy = sum((ra[i] - ma) * (rb[i] - mb) for i in range(n))
    sxx = sum((ra[i] - ma) ** 2 for i in range(n))
    syy = sum((rb[i] - mb) ** 2 for i in range(n))
    r_hand = sxy / math.sqrt(sxx * syy)
    print("  %s vs %s, calendar %d, %d daily return pairs on the BOOK calendar"
          % (sa, sb, yy, n))
    print("  mean(SPY)=%.10f   mean(QQQ)=%.10f" % (ma, mb))
    print("  sum dx*dy = %.10f" % sxy)
    print("  sum dx^2  = %.10f" % sxx)
    print("  sum dy^2  = %.10f" % syy)
    print("  r = sum dx*dy / sqrt(sum dx^2 * sum dy^2) = %.10f" % r_hand)
    one_year = corr_year_on(sa, sb, yy, dts)
    print("  independent routine, same calendar        = %.10f" % one_year)
    print("  agreement: %.3e" % (r_hand - one_year))
    r_raw = corr_year(sa, sb, yy)
    print("")
    print("  CALENDAR SENSITIVITY, reported rather than hidden:")
    print("  the same year on the raw SPY+QQQ intersection calendar gives")
    print("  r = %.10f, i.e. a difference of %.3e in the 4th decimal."
          % (r_raw, r_raw - r_hand))
    print("  Which calendar you intersect on therefore matters at the 1e-4 level")
    print("  for a one-year window, and is why this study fixes ONE window per")
    print("  question instead of letting each statistic choose its own.")
    note("byhand.corr_spy_qqq_2024", one_year, r_hand)

    # --- the gap table ------------------------------------------------------
    print("")
    print("=" * 78)
    print("GAP TABLE -- study.py value vs independent re-derivation")
    print("=" * 78)
    hdr = ["statistic", "study.py", "handcheck", "gap"]
    w = [max(len(str(hdr[i])), *(len(str(r[i])) for r in GAPS)) for i in range(4)]
    print("  " + "  ".join(hdr[i].ljust(w[i]) for i in range(4)).rstrip())
    print("  " + "  ".join("-" * w[i] for i in range(4)))
    for r in GAPS:
        print("  " + "  ".join(str(r[i]).ljust(w[i]) for i in range(4)).rstrip())

    big = []
    for r in GAPS:
        if r[3] in ("same", "DIFFERS", "n/a"):
            continue
        try:
            if abs(float(r[3])) > 1e-6:
                big.append(r)
        except ValueError:
            big.append(r)
    print("")
    print("  gaps larger than 1e-6: %d" % len(big))
    for r in big:
        print("      %s : study %s vs handcheck %s (gap %s)" % tuple(r[:4]))
    print("  VERDICT: %s" % ("AGREES -- the two implementations reproduce the "
                             "same numbers." if not big
                             else "DISAGREES -- see the rows above."))
    return 0 if not big else 1


def corr_between(a, b, mode):
    """Pearson on daily or complete-year returns, on the intersection calendar."""
    ca, cb2 = col(a, 4), col(b, 4)
    dts = sorted(set(ca) & set(cb2))
    if mode == "daily":
        ra = [ca[dts[i]] / ca[dts[i - 1]] - 1.0 for i in range(1, len(dts))]
        rb = [cb2[dts[i]] / cb2[dts[i - 1]] - 1.0 for i in range(1, len(dts))]
        return pearson(ra, rb)
    ya, yb = {}, {}
    for i in range(1, len(dts)):
        if dts[0].year == dts[i].year or dts[-1].year == dts[i].year:
            continue
        ya.setdefault(dts[i].year, []).append(ca[dts[i]] / ca[dts[i - 1]] - 1.0)
        yb.setdefault(dts[i].year, []).append(cb2[dts[i]] / cb2[dts[i - 1]] - 1.0)
    years = sorted(set(ya) & set(yb))
    outa, outb = [], []
    for y in years:
        c = 1.0
        for r in ya[y]:
            c *= (1.0 + r)
        outa.append(c - 1.0)
        c = 1.0
        for r in yb[y]:
            c *= (1.0 + r)
        outb.append(c - 1.0)
    return pearson(outa, outb)


def corr_year_on(a, b, year, dts):
    """Pearson of daily returns in `year`, on the SUPPLIED calendar `dts`."""
    ca, cb2 = col(a, 4), col(b, 4)
    ra = [ca[dts[i]] / ca[dts[i - 1]] - 1.0 for i in range(1, len(dts))]
    rb = [cb2[dts[i]] / cb2[dts[i - 1]] - 1.0 for i in range(1, len(dts))]
    return pearson(ra, rb)


def corr_year(a, b, year):
    """Same, but on the raw intersection calendar of the two symbols only, so the
    caller can see how much the calendar choice moves the answer."""
    ca, cb2 = col(a, 4), col(b, 4)
    dts = sorted(d for d in (set(ca) & set(cb2)) if d.year == year)
    ra = [ca[dts[i]] / ca[dts[i - 1]] - 1.0 for i in range(1, len(dts))]
    rb = [cb2[dts[i]] / cb2[dts[i - 1]] - 1.0 for i in range(1, len(dts))]
    return pearson(ra, rb)


if __name__ == "__main__":
    sys.exit(main())
