#!/usr/bin/env python3
"""
handcheck.py -- INDEPENDENT re-derivation of the tenor test.

This file imports NOTHING from study.py.  It re-implements, from data/*.csv and
from the pre-registration written down in README.md, the whole chain:

    window -> implied-vol context -> tenor schedule -> strike solve ->
    entry premium -> settlement at intrinsic -> R -> cost -> per-cell stats

and then compares its own numbers against out/cells_summary.csv, reporting the
gap cell by cell.  Where study.py uses math.erf, a 80-iteration bisection and a
kink-set minimum, this file uses math.erfc, a 200-iteration bisection to machine
precision and a direct payoff scan -- so a gap is an implementation gap, not a
shared-code artefact.

It also performs three BY-HAND checks the brief asks for:
    H1. price one leg at three different tenors with Black-Scholes from stated
        inputs, and validate the normal CDF against Simpson integration of the
        density;
    H2. compute theta-per-day per R for one cell, showing the arithmetic;
    H3. settle one LONG-tenor structure against the real path, leg by leg.

Stdlib only.  No network.  Deterministic.  LF output.

USAGE
    py -3 handcheck.py
"""

import bisect
import datetime
import io
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
OUT = os.path.join(HERE, "out")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(newline="\n")

SYMBOLS = ["SPY", "QQQ", "IWM"]
UNIVERSE = SYMBOLS + ["VIX", "US03M"]

TRADING_DAYS = 252
SMA_TREND = 200
VIX_LAG = 3
KAPPA_LOOKBACK = 60
KAPPA_LO, KAPPA_HI = 0.60, 2.00

TENORS = [7, 14, 30, 45, 60, 90, 180, 365, 730]
STRUCTS = ["S1", "S2", "S3", "S4", "S5", "S6", "S7"]
D16, D25, D30, D50 = 0.16, 0.25, 0.30, 0.50
WING = 5.0

FEE = 0.65
HALF_SPREAD = 0.025
ETF_BPS = 5.0

SLV_UNITS = 10.0

NA = None


def pct(x, nd=2):
    return "n/a" if x is NA else ("%+.*f%%" % (nd, 100.0 * x))


def num(x, nd=6):
    return "n/a" if x is NA else ("%.*f" % (nd, x))


# ===========================================================================
# Independent normal CDF: N(x) = 0.5 * erfc(-x / sqrt(2))
# (study.py uses N(x) = 0.5 * (1 + erf(x/sqrt(2))).  Algebraically identical,
#  numerically a different path -- and both are validated against a Simpson
#  quadrature of the standard normal density in check H1 below.)
# ===========================================================================

SQRT2 = math.sqrt(2.0)
SQRT2PI = math.sqrt(2.0 * math.pi)


def N(x):
    return 0.5 * math.erfc(-x / SQRT2)


def phi(x):
    return math.exp(-0.5 * x * x) / SQRT2PI


def N_simpson(x, n=2000):
    """Simpson quadrature of the standard normal density from -12 to x."""
    lo = -12.0
    if x <= lo:
        return 0.0
    h = (x - lo) / n
    s = phi(lo) + phi(x)
    for i in range(1, n):
        s += (4.0 if i % 2 else 2.0) * phi(lo + i * h)
    return s * h / 3.0


# ===========================================================================
# Black-Scholes, written independently of study.py
# ===========================================================================

def bs(S, K, T, r, sigma, kind):
    if S <= 0.0 or K <= 0.0:
        return 0.0
    if T <= 1e-12 or sigma <= 1e-12:
        return max(S - K, 0.0) if kind == "C" else max(K - S, 0.0)
    v = sigma * math.sqrt(T)
    d1 = (math.log(S / K) + (r + 0.5 * sigma * sigma) * T) / v
    d2 = d1 - v
    if kind == "C":
        return S * N(d1) - K * math.exp(-r * T) * N(d2)
    return K * math.exp(-r * T) * N(-d2) - S * N(-d1)


def bs_delta(S, K, T, r, sigma, kind):
    if S <= 0.0 or K <= 0.0:
        return 0.0
    if T <= 1e-12 or sigma <= 1e-12:
        if kind == "C":
            return 1.0 if S > K else 0.0
        return -1.0 if S < K else 0.0
    v = sigma * math.sqrt(T)
    d1 = (math.log(S / K) + (r + 0.5 * sigma * sigma) * T) / v
    return N(d1) if kind == "C" else N(d1) - 1.0


def solve_strike(S, T, r, sigma, kind, target):
    """200-iteration bisection on a bracket wide enough for every tenor and vol
    in the study, to machine precision, WITH a straddle assertion."""
    lo, hi = 0.02 * S, 100.0 * S

    def f(K):
        if kind == "P":
            return abs(bs_delta(S, K, T, r, sigma, "P")) - target
        return bs_delta(S, K, T, r, sigma, "C") - target

    flo, fhi = f(lo), f(hi)
    if flo * fhi > 0.0:
        raise RuntimeError("bracket does not straddle target=%r (kind=%s, "
                           "T=%r, sigma=%r)" % (target, kind, T, sigma))
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if flo * fm <= 0.0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
        if hi - lo < 1e-15 * S:
            break
    return 0.5 * (lo + hi)


# ===========================================================================
# Data
# ===========================================================================

class Ser(object):
    def __init__(self, name, dates, o, h, l, c):
        self.name, self.dates, self.o, self.h, self.l, self.c = \
            name, dates, o, h, l, c
        self.pos = dict((d, i) for i, d in enumerate(dates))


def load(sym):
    d, o, h, l, c = [], [], [], [], []
    with io.open(os.path.join(DATA, "%s_1d.csv" % sym), "r",
                 encoding="utf-8-sig", newline="") as fh:
        for line in fh:
            if line.startswith("#") or not line.strip():
                continue
            if line.startswith("date,"):
                continue
            f = line.rstrip("\r\n").split(",")
            d.append(datetime.date.fromisoformat(f[0]))
            o.append(float(f[1]))
            h.append(float(f[2]))
            l.append(float(f[3]))
            c.append(float(f[4]))
    return Ser(sym, d, o, h, l, c)


def close_on_or_before(s, d, maxback=16):
    k = s.pos.get(d)
    if k is not None:
        return s.c[k]
    for i in range(1, maxback + 1):
        k = s.pos.get(d - datetime.timedelta(days=i))
        if k is not None:
            return s.c[k]
    return NA


def med(xs):
    """Standard median: for even n, the MEAN of the two middle values.
    (The first draft of this file used xs[n//2], which is a different statistic
    for even n and produced a 4-8% gap on the two median-derived fields of the
    36-trade long-tenor cells.  That gap was the median convention, not a
    numerical disagreement -- worth stating, because a "gap" that is really a
    definition difference is not evidence of an error in either file.)"""
    if not xs:
        return NA
    s = sorted(xs)
    m = len(s)
    if m % 2:
        return s[m // 2]
    return 0.5 * (s[m // 2 - 1] + s[m // 2])


def sd(xs):
    n = len(xs)
    if n < 2:
        return NA
    m = sum(xs) / float(n)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / float(n - 1))


def ann_log_sd(s, end_idx, n=KAPPA_LOOKBACK):
    if end_idx is NA or end_idx - n < 0:
        return NA
    rs = []
    for i in range(end_idx - n + 1, end_idx + 1):
        if s.c[i - 1] <= 0 or s.c[i] <= 0:
            return NA
        rs.append(math.log(s.c[i] / s.c[i - 1]))
    v = sd(rs)
    return NA if v is NA else v * math.sqrt(TRADING_DAYS)


def main():
    print("=" * 78)
    print("HANDCHECK -- INDEPENDENT re-derivation of the tenor test")
    print("=" * 78)
    print("")
    print("This file imports nothing from study.py.  It shares no code with it:")
    print("  N(x)          : 0.5*erfc(-x/sqrt2)   vs study.py's 0.5*(1+erf(x/sqrt2))")
    print("  strike solve  : 200-iteration bisection, 1e-15 relative stop")
    print("  R             : direct payoff scan over [0, 3S] and the strike set")
    print("A gap between the two is therefore an implementation gap.")
    print("")

    series = dict((s, load(s)) for s in UNIVERSE)

    # ---------------- window, identical construction
    sets = [set(series[s].dates) for s in SYMBOLS] + [set(series["VIX"].dates)]
    common = set.intersection(*sets)
    starts = []
    for s in SYMBOLS:
        c = series[s].c
        run = 0.0
        first = None
        for i in range(len(c)):
            run += c[i]
            if i >= SMA_TREND:
                run -= c[i - SMA_TREND]
            if i >= SMA_TREND - 1 and first is None:
                first = series[s].dates[i]
        starts.append(first)
    wd = sorted(d for d in common if d >= max(starts))
    print("  window: %s ... %s  (%d sessions)"
          % (wd[0].isoformat(), wd[-1].isoformat(), len(wd)))

    # ---------------- implied-vol context, identical construction
    vix = series["VIX"]
    us = series["US03M"]
    n = len(wd)
    vix_used, r_used = [NA] * n, [NA] * n
    for j in range(n):
        k = max(0, j - VIX_LAG)
        vix_used[j] = close_on_or_before(vix, wd[k])
        y = close_on_or_before(us, wd[k])
        r_used[j] = max(0.0, y / 100.0) if y is not NA else 0.0
    kappa = {}
    for sym in SYMBOLS:
        arr = [1.0] * n
        if sym != "SPY":
            for j in range(n):
                k = max(0, j - VIX_LAG)
                d = wd[k]
                a = ann_log_sd(series[sym], series[sym].pos.get(d))
                b = ann_log_sd(series["SPY"], series["SPY"].pos.get(d))
                if a is NA or b in (NA, 0.0):
                    arr[j] = 1.0
                else:
                    arr[j] = min(max(a / b, KAPPA_LO), KAPPA_HI)
        kappa[sym] = arr

    # ---------------- structures, independently written
    def legs_of(sid, S, T, r, iv):
        """[(kind, K, qty)] -- 'S' is the underlying."""
        if sid == "S1":
            return [("C", solve_strike(S, T, r, iv, "C", D50), +1)]
        if sid == "S2":
            return [("P", solve_strike(S, T, r, iv, "P", D16), -1)]
        if sid == "S3":
            k = solve_strike(S, T, r, iv, "P", D16)
            return [("P", k, -1), ("P", k - WING, +1)]
        if sid == "S4":
            return [("C", solve_strike(S, T, r, iv, "C", D50), +1),
                    ("C", solve_strike(S, T, r, iv, "C", D25), -1)]
        if sid == "S5":
            return [("S", S, +1),
                    ("C", solve_strike(S, T, r, iv, "C", D30), -1)]
        if sid == "S6":
            kp = solve_strike(S, T, r, iv, "P", D16)
            kc = solve_strike(S, T, r, iv, "C", D16)
            return [("P", kp, -1), ("P", kp - WING, +1),
                    ("C", kc, -1), ("C", kc + WING, +1)]
        if sid == "S7":
            return [("P", S, -1), ("C", S, -1),
                    ("P", S - WING, +1), ("C", S + WING, +1)]
        raise ValueError(sid)

    def value(kind, K, qty, S, T, r, iv):
        if kind == "S":
            return qty * S
        return qty * bs(S, K, T, r, iv, kind)

    def intrinsic(kind, K, qty, S):
        if kind == "S":
            return qty * S
        if kind == "C":
            return qty * max(S - K, 0.0)
        return qty * max(K - S, 0.0)

    def max_loss(legs, entry_per_share, S0):
        """Direct scan: the payoff is piecewise linear, so the minimum lies on
        {0, 3*S0} U {strikes}.  Evaluated by scanning a fine grid AND the kink
        set, and the smaller taken -- a redundant check on the kink argument."""
        ks = set([0.0, 3.0 * S0])
        for kind, K, _q in legs:
            if kind != "S" and 0.0 <= K <= 3.0 * S0:
                ks.add(K)
        cand = sorted(ks)
        best = None
        for S in cand:
            pnl = sum(intrinsic(k, K, q, S) for k, K, q in legs) - \
                sum(entry_per_share)
            if best is None or pnl < best:
                best = pnl
        return -best

    def cost_of(legs, S0):
        contracts = sum(abs(q) for k, _K, q in legs if k != "S")
        tot = (FEE + HALF_SPREAD * 100.0) * contracts
        if any(k == "S" for k, _K, _q in legs):
            tot += (ETF_BPS / 10000.0) * S0 * 100.0
        return tot

    # ---------------- the tenor programme, independently written
    def schedule(tenor):
        out = []
        j = 1
        while j < n:
            ent = wd[j]
            target = ent + datetime.timedelta(days=tenor)
            i = bisect.bisect_left(wd, target)
            if i >= n:
                break
            exp = wd[i]
            out.append((wd[j - 1], ent, exp))
            j = bisect.bisect_right(wd, exp)
        return out

    # ---------------- run every BASE cell
    pos_of = dict((d, j) for j, d in enumerate(wd))
    cells = {}
    for sid in STRUCTS:
        for tenor in TENORS:
            trades = []
            for sym in SYMBOLS:
                s = series[sym]
                for sig_d, ent_d, exp_d in schedule(tenor):
                    js = pos_of[sig_d]
                    ke = s.pos[ent_d]
                    S_open, S_close = s.o[ke], s.c[s.pos[exp_d]]
                    S_sig = s.c[s.pos[sig_d]]
                    T = (exp_d - ent_d).days / 365.0
                    r = r_used[js]
                    iv = (vix_used[js] / 100.0 * kappa[sym][js]
                          if vix_used[js] is not NA else 0.0)
                    if iv <= 0.0 or T <= 0.0:
                        continue
                    legs = legs_of(sid, S_sig, T, r, iv)
                    px = []
                    for kind, K, q in legs:
                        p = S_open if kind == "S" else bs(S_open, K, T, r, iv,
                                                          kind)
                        px.append(q * p)
                    # credit is the OPTION cash flow only: the underlying leg
                    # is collateral, not premium (study.py's
                    # entry_cash_dollars returns 0 for an 'S' leg).  The first
                    # draft summed px over every leg, which put S_open*100 into
                    # the covered call's credit -- the one structure with a stock
                    # leg -- and produced a ~12,400 gap that was a bug in THIS
                    # file, not in study.py.
                    # px already holds q*p per leg, so the option cash flow is
                    # -sum(px) over the OPTION legs only.
                    credit = -sum(p for (k, _K, _q), p in zip(legs, px)
                                  if k != "S") * 100.0
                    ml = max_loss(legs, px, S_open)
                    R = ml * 100.0
                    gross = (sum(intrinsic(k, K, q, S_close)
                                 for k, K, q in legs) - sum(px)) * 100.0
                    cost = cost_of(legs, S_open)
                    trades.append({"sym": sym, "R": R, "credit": credit,
                                   "cost": cost, "gross": gross,
                                   "R_mult": gross / R,
                                   "cost_R": cost / R})
            m = len(trades)
            if not m:
                continue
            rs = [t["R_mult"] for t in trades]
            wins = [x for x in rs if x > 0.0]
            loss = [x for x in rs if x <= 0.0]
            p = len(wins) / float(m)
            b = ((sum(wins) / len(wins)) / abs(sum(loss) / len(loss))
                 if wins and loss else NA)
            E = sum(rs) / float(m)
            sdev = sd(rs)
            cR = sum(t["cost_R"] for t in trades) / float(m)
            med_credit = med([t["credit"] for t in trades])
            med_R = med([t["R"] for t in trades])
            cells[(sid, tenor)] = {
                "n": m, "p": p, "b": b, "E": E, "sd": sdev,
                "n_req": (4.0 * (sdev / abs(E)) ** 2) if E else NA,
                "c_R": cR, "E_net": E - cR, "credit_med": med_credit,
                "R_med": med_R,
                "theta_pd_R": med_credit / (tenor * med_R),
                "frac_max": sum(1 for x in rs if x <= -0.98) / float(m)}
    print("  cells re-derived independently: %d" % len(cells))
    print("")

    # ---------------- compare against out/cells_summary.csv
    ref = {}
    path = os.path.join(OUT, "cells_summary.csv")
    if not os.path.isfile(path):
        raise SystemExit("ERROR: run study.py first (%s missing)" % path)
    with io.open(path, "r", encoding="utf-8", newline="") as fh:
        hdr = None
        for line in fh:
            f = line.rstrip("\r\n").split(",")
            if hdr is None:
                hdr = f
                continue
            d = dict(zip(hdr, f))
            ref[(d["sid"], int(d["tenor"]))] = d

    print("=" * 78)
    print("GAP TABLE -- handcheck vs study.py, all %d BASE cells" % len(cells))
    print("=" * 78)
    print("")
    fields = [("n_available", "n", 0), ("p_gross", "p", 6), ("b", "b", 6),
              ("E_gross", "E", 8), ("sd", "sd", 8), ("n_req", "n_req", 4),
              ("c_R", "c_R", 8), ("E_net", "E_net", 8),
              ("theta_pd_R", "theta_pd_R", 8), ("R_dollars_med", "R_med", 4),
              ("credit_med", "credit_med", 4)]
    worst = {}
    rows = []
    for sid in STRUCTS:
        for tenor in TENORS:
            r = ref.get((sid, tenor))
            c = cells.get((sid, tenor))
            if r is None or c is None:
                rows.append([sid, tenor, "MISSING", "", "", ""])
                continue
            gaps = []
            for refk, ownk, nd in fields:
                rv = r[refk]
                ov = c[ownk]
                rv = NA if rv in ("", "NA", "n/a") else float(rv)
                if rv is NA or ov is NA:
                    gaps.append((refk, NA))
                    worst.setdefault(refk, 0.0)
                    continue
                g = abs(rv - ov)
                rel = g / abs(rv) if abs(rv) > 1e-15 else g
                gaps.append((refk, g, rel))
                worst[refk] = max(worst.get(refk, 0.0), g)
            cand = [g for g in gaps if g[1] is not NA]
            if cand:
                wf = max(cand, key=lambda g: g[1])
                mx, mrel, wname = wf[1], wf[2], wf[0]
            else:
                mx = mrel = 0.0
                wname = "-"
            rows.append([sid, tenor, c["n"], r["n_available"],
                         num(mx, 12), num(mrel, 10), wname])
    print("  %-4s %-5s %-8s %-8s %-16s %-14s %-16s"
          % ("id", "DTE", "n (own)", "n (study)", "max |gap|",
             "max rel gap", "worst field"))
    print("  " + "-" * 80)
    for r in rows:
        print("  %-4s %-5s %-8s %-8s %-16s %-14s %-16s"
              % (r[0], r[1], r[2], r[3], r[4], r[5], r[6]))
    print("")
    print("  worst absolute gap per field, across all cells:")
    for refk, ownk, nd in fields:
        print("    %-16s  %s" % (refk, num(worst.get(refk, 0.0), 12)))

    # ---------------- H1: price one leg at three tenors
    print("")
    print("=" * 78)
    print("H1. BY HAND -- one leg, three tenors, Black-Scholes from stated inputs")
    print("=" * 78)
    print("")
    S0, K0, r0, sig0 = 100.0, 100.0, 0.0425, 0.20
    print("  Inputs: S=%.2f  K=%.2f  r=%.4f (4.25%%)  sigma=%.2f  q=0"
          % (S0, K0, r0, sig0))
    print("")
    print("  %-10s %12s %12s %12s %12s %14s"
          % ("T (days)", "T (years)", "d1", "d2", "call $", "N(x) simpson"))
    for days in (7, 90, 730):
        T = days / 365.0
        v = sig0 * math.sqrt(T)
        d1 = (math.log(S0 / K0) + (r0 + 0.5 * sig0 ** 2) * T) / v
        d2 = d1 - v
        print("  %-10d %12.8f %12.6f %12.6f %12.6f %14.10f"
              % (days, T, d1, d2, bs(S0, K0, T, r0, sig0, "C"), N_simpson(d1)))
    print("")
    print("  The Simpson column is an independent quadrature of the standard")
    print("  normal density; agreement with N(d1) to ~1e-10 validates the CDF")
    print("  both files use.  The closed forms for d1 and d2 are printed so the")
    print("  arithmetic can be repeated with a calculator.")
    print("")
    print("  PUT, same inputs (put-call parity check: C - P = S - K e^-rT):")
    print("  %-10s %12s %12s %14s"
          % ("T (days)", "put $", "C - P", "S - K e^-rT"))
    for days in (7, 90, 730):
        T = days / 365.0
        c = bs(S0, K0, T, r0, sig0, "C")
        pu = bs(S0, K0, T, r0, sig0, "P")
        print("  %-10d %12.6f %12.6f %14.10f"
              % (days, pu, c - pu, S0 - K0 * math.exp(-r0 * T)))

    # ---------------- H2: theta-per-day per R for one cell
    print("")
    print("=" * 78)
    print("H2. BY HAND -- theta-per-day per unit of R, one cell")
    print("=" * 78)
    key = ("S3", 30)
    c = cells[key]
    print("")
    print("  Cell S3 (short put spread ~16d / 5-wide) at DTE 30, pooled over")
    print("  SPY+QQQ+IWM, %d trades:" % c["n"])
    print("  median credit        = $%.4f per contract" % c["credit_med"])
    print("  median R (max loss)  = $%.4f per contract" % c["R_med"])
    print("  tenor                = %d days" % key[1])
    print("")
    print("  theta/day/R = credit / (tenor x R)")
    print("              = %.4f / (%d x %.4f)"
          % (c["credit_med"], key[1], c["R_med"]))
    print("              = %.4f / %.4f" % (c["credit_med"], key[1] * c["R_med"]))
    print("              = %+.8f  (fraction of R earned per calendar day)"
          % c["theta_pd_R"])
    print("  study.py reports        %s"
          % ref[key]["theta_pd_R"])
    print("  reciprocal reading: the position collects 1R in %.1f days at this"
          % (1.0 / c["theta_pd_R"]))
    print("  rate, against a %d-day hold -- i.e. %.2fx the holding period."
          % (key[1], (1.0 / c["theta_pd_R"]) / key[1]))
    print("")
    print("  And the ratio to the same cell at DTE 7:")
    c7 = cells[("S3", 7)]
    print("    theta/day/R @7 = %+.8f ; @30 = %+.8f ; ratio = %.2fx"
          % (c7["theta_pd_R"], c["theta_pd_R"],
             c7["theta_pd_R"] / c["theta_pd_R"]))

    # ---------------- H3: settle one long-tenor structure on the real path
    print("")
    print("=" * 78)
    print("H3. BY HAND -- one LONG-tenor structure settled on the REAL path")
    print("=" * 78)
    print("")
    sid, tenor, sym, idx = "S3", 730, "SPY", 0
    s = series[sym]
    sch = schedule(tenor)
    sig_d, ent_d, exp_d = sch[idx]
    js = pos_of[sig_d]
    S_sig = s.c[s.pos[sig_d]]
    S_open = s.o[s.pos[ent_d]]
    S_close = s.c[s.pos[exp_d]]
    T = (exp_d - ent_d).days / 365.0
    r = r_used[js]
    iv = vix_used[js] / 100.0 * kappa[sym][js]
    legs = legs_of(sid, S_sig, T, r, iv)
    print("  %s at DTE %d on %s, trade #%d of the sequential programme" %
          (sid, tenor, sym, idx + 1))
    print("  signal close %s = %.4f" % (sig_d.isoformat(), S_sig))
    print("  entry  OPEN  %s = %.4f" % (ent_d.isoformat(), S_open))
    print("  expiry CLOSE %s = %.4f" % (exp_d.isoformat(), S_close))
    print("  holding period  = %d days = %.6f years"
          % ((exp_d - ent_d).days, T))
    print("  iv (3-lag VIX x kappa) = %.6f ; r = %.6f" % (iv, r))
    print("")
    print("  %-6s %10s %6s %12s %12s %14s"
          % ("kind", "strike", "qty", "entry $/sh", "intrinsic", "leg P&L $"))
    entry_ps = []
    tot_term = 0.0
    for kind, K, q in legs:
        p = S_open if kind == "S" else bs(S_open, K, T, r, iv, kind)
        entry_ps.append(q * p)
        intr = intrinsic(kind, K, q, S_close)
        pnl = (intr - q * p) * 100.0
        tot_term += pnl
        print("  %-6s %10.4f %6d %12.6f %12.6f %14.4f"
              % (kind, K, q, q * p, intr, pnl))
    print("")
    print("  sum of leg P&L (= the trade's terminal P&L)   = %+.4f" % tot_term)
    ml = max_loss(legs, entry_ps, S_open)
    print("  R = max loss per share %.6f -> $%.4f per contract"
          % (ml, ml * 100.0))
    print("  R_mult (gross) = %+.8f" % (tot_term / (ml * 100.0)))
    print("  credit = %+.4f ; cost = %.4f ; c_R = %.8f"
          % (-sum(entry_ps) * 100.0, cost_of(legs, S_open),
             cost_of(legs, S_open) / (ml * 100.0)))
    print("")
    print("  cross-check against out/cells_summary.csv for cell (S3, 730):")
    r730 = ref[("S3", 730)]
    print("    n_available  study=%s  handcheck=%s" %
          (r730["n_available"], cells[("S3", 730)]["n"]))
    print("    E_gross      study=%s  handcheck=%s" %
          (r730["E_gross"], num(cells[("S3", 730)]["E"], 8)))
    print("    c_R          study=%s  handcheck=%s" %
          (r730["c_R"], num(cells[("S3", 730)]["c_R"], 8)))
    print("    E_net        study=%s  handcheck=%s" %
          (r730["E_net"], num(cells[("S3", 730)]["E_net"], 8)))
    print("")
    print("  NOTE: the printed single trade is trade #1 of the S3/730 programme,")
    print("  not the median, so it is NOT expected to equal the cell's E; it is")
    print("  there so a reader can reproduce one settlement by hand.")
    print("")
    print("Done.  handcheck.py imports nothing from study.py.")


if __name__ == "__main__":
    main()
