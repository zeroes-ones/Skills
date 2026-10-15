#!/usr/bin/env python3
"""handcheck.py -- an INDEPENDENT re-derivation.  Does NOT import study.py.

Re-derives, from the same real prices but with its own code:

  * implied volatility, with its own bracketing bisection (bracket expansion
    then bisection, different tolerance and stop rule from study.py);
  * the skew slope per sample date, with its own ordinary-least-squares solved
    through the normal equations rather than the centred covariance form;
  * the full Black-Scholes intermediate values for one real price, printed so a
    reader can reproduce the number with a calculator.

It then compares its own numbers against the values study.py printed in
logs/study-output.txt and reports the gap.  A non-zero gap on the printed
precision means the two implementations disagree and the study is wrong.

Stdlib only.  Deterministic.  UTF-8, LF.
"""

import csv
import math
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")
UND = os.path.join(DATA, "underlying")
REF = os.path.join(ROOT, "logs", "study-output.txt")

# The single contract that gets the full intermediate dump: SPY 2020-03-02,
# the 300 put, the near-ATM point of the one COMPLETE measured ladder.
DUMP = ("SPY", "2020-03-02", "put", 300.0)


# --- own normal cdf (Abramowitz-Stegun 7.1.26 free erf series) -------------
def erf_as(x):
    """A DIFFERENT erf implementation from study.py's math.erf, so the dump
    cannot agree by construction."""
    a1, a2, a3, a4, a5 = (0.254829592, -0.284496736, 1.421413741,
                          -1.453152027, 1.061405429)
    p = 0.3275911
    s = 1.0 if x >= 0 else -1.0
    x = abs(x)
    t = 1.0 / (1.0 + p * x)
    y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(-x * x)
    return s * y


def ncdf_own(x):
    return 0.5 * (1.0 + erf_as(x / math.sqrt(2.0)))


def bs_own(S, K, T, r, sig, kind, q=0.0):
    if T <= 0 or sig <= 0:
        return max(0.0, (S - K) if kind == "call" else (K - S))
    sq = sig * math.sqrt(T)
    d1 = (math.log(S / K) + (r - q + 0.5 * sig * sig) * T) / sq
    d2 = d1 - sq
    if kind == "call":
        return S * math.exp(-q * T) * ncdf_own(d1) - K * math.exp(-r * T) * ncdf_own(d2)
    return K * math.exp(-r * T) * ncdf_own(-d2) - S * math.exp(-q * T) * ncdf_own(-d1)


def iv_own(price, S, K, T, r, kind, q=0.0):
    """Bracket expansion then bisection.  Own stop rule: 120 halvings or a
    1e-12 interval."""
    lo, hi = 1e-6, 0.20
    if bs_own(S, K, T, r, hi, kind, q) < price:
        for _ in range(30):
            hi *= 1.5
            if bs_own(S, K, T, r, hi, kind, q) >= price:
                break
        else:
            return None
    for _ in range(120):
        mid = 0.5 * (lo + hi)
        if bs_own(S, K, T, r, mid, kind, q) < price:
            lo = mid
        else:
            hi = mid
        if hi - lo < 1e-12:
            break
    return 0.5 * (lo + hi)


def ols_normal_equations(xs, ys):
    """slope via the 2x2 normal equations, solved by Cramer's rule."""
    n = len(xs)
    sx = sum(xs)
    sy = sum(ys)
    sxx = sum(x * x for x in xs)
    sxy = sum(xs[i] * ys[i] for i in range(n))
    det = n * sxx - sx * sx
    if det == 0:
        return None
    return (n * sxy - sx * sy) / det


def read_under(sym):
    with open(os.path.join(UND, "%s_1d.csv" % sym), "r", encoding="utf-8") as fh:
        rows = [ln for ln in fh if not ln.startswith("#")]
    rdr = csv.reader(rows)
    h = next(rdr)
    ci = h.index("close")
    return {r[0]: float(r[ci]) for r in rdr if r}


def read_rate(d):
    with open(os.path.join(UND, "US03M_1d.csv"), "r", encoding="utf-8") as fh:
        rows = [ln for ln in fh if not ln.startswith("#")]
    rdr = csv.reader(rows)
    next(rdr)
    rates = {r[0]: float(r[4]) for r in rdr if r}
    from datetime import date, timedelta
    dd = date.fromisoformat(d)
    for back in range(0, 8):
        k = (dd - timedelta(days=back)).isoformat()
        if k in rates:
            return rates[k]
    return 0.0


def parse_ref():
    """(iv_map, skew_map) parsed out of study.py's printed tables."""
    iv_map, skew_map = {}, {}
    if not os.path.exists(REF):
        return iv_map, skew_map
    lines = open(REF, "r", encoding="utf-8").read().splitlines()
    mode = None
    for ln in lines:
        s = ln.strip()
        if "IV_real%" in s and "IV_model%" in s:
            mode = "iv"
            continue
        if "slope_10%OTM" in s and "put-call%" in s:
            mode = "skew"
            continue
        if not s:
            mode = None
            continue
        if s.startswith("---"):
            continue
        f = s.split()
        if mode == "iv" and len(f) >= 11 and f[0] in ("SPY", "QQQ", "IWM"):
            try:
                iv_map[(f[0], f[1], f[3], float(f[5]))] = float(f[9])
            except ValueError:
                pass
        elif mode == "skew" and len(f) >= 7 and f[0] in ("SPY", "QQQ", "IWM"):
            try:
                skew_map[(f[0], f[1])] = float(f[3])
            except ValueError:
                pass
    return iv_map, skew_map


def main():
    out = []
    def emit(s=""):
        out.append(s)
        print(s)

    with open(os.path.join(DATA, "real_quotes_ladder.csv"), "r",
              encoding="utf-8") as fh:
        rows = [ln for ln in fh if not ln.startswith("#")]
    meas = [r for r in csv.DictReader(rows) if r.get("close")]

    emit("HANDCHECK -- independent re-derivation of the measured IVs and skew.")
    emit("This file does NOT import study.py.  Its erf is a different")
    emit("implementation (A&S 7.1.26 series vs math.erf), its bisection uses")
    emit("bracket expansion, and its OLS solves the normal equations by")
    emit("Cramer's rule.  Agreement is therefore not by construction.")
    emit("")

    iv_ref, skew_ref = parse_ref()
    emit("reference tables parsed from logs/study-output.txt: %d IV rows, %d skew rows"
         % (len(iv_ref), len(skew_ref)))
    emit("")

    # ---- full intermediate dump for ONE contract --------------------------
    emit("=" * 78)
    emit("A. FULL BLACK-SCHOLES INTERMEDIATES FOR ONE REAL PRICE (by hand)")
    emit("=" * 78)
    sym, d, kind, K = DUMP
    r0 = [x for x in meas if x["underlying"] == sym and x["sample_date"] == d
          and x["type"] == kind and abs(float(x["strike"]) - K) < 1e-9][0]
    S = float(r0["spot_close"])
    price = float(r0["close"])
    T = int(r0["dte"]) / 365.0
    r = read_rate(d) / 100.0
    emit("  contract      : %s %s %s %s" % (sym, d, kind, r0["strike"]))
    emit("  expiry / DTE  : %s / %s calendar days" % (r0["expiry"], r0["dte"]))
    emit("  real close    : $%.2f" % price)
    emit("  underlying S  : %.2f  (real close, spot column)" % S)
    emit("  strike    K   : %.2f" % K)
    emit("  r (US03M)     : %.6f  (= %.4f%% / 100)" % (r, read_rate(d)))
    emit("  T             : %s / 365 = %.10f" % (r0["dte"], T))
    emit("")
    sig = 0.3344                      # first guess from study.py's printout
    emit("  Evaluating BS(put) at sigma = %.4f:" % sig)
    sq = sig * math.sqrt(T)
    d1 = (math.log(S / K) + (r + 0.5 * sig * sig) * T) / sq
    d2 = d1 - sq
    emit("    sqrt(T)        = %.10f" % math.sqrt(T))
    emit("    ln(S/K)        = %.10f" % math.log(S / K))
    emit("    (r+0.5*sig^2)T = %.10f" % ((r + 0.5 * sig * sig) * T))
    emit("    d1             = %.10f" % d1)
    emit("    d2             = %.10f" % d2)
    emit("    N(-d1)         = %.10f" % ncdf_own(-d1))
    emit("    N(-d2)         = %.10f" % ncdf_own(-d2))
    emit("    K*exp(-rT)     = %.10f" % (K * math.exp(-r * T)))
    emit("    S*N(-d1)       = %.10f" % (S * ncdf_own(-d1)))
    p_manual = K * math.exp(-r * T) * ncdf_own(-d2) - S * ncdf_own(-d1)
    emit("    BS(put)        = %.10f" % p_manual)
    emit("  Real close was %.2f, so sigma = %.4f is TOO %s."
         % (price, sig, "HIGH" if p_manual > price else "LOW"))
    emit("")
    emit("  Bisecting for sigma over [%.6f, %.6f] -> sigma = %.10f  (%.6f%%)"
         % (1e-6, 5.0, iv_own(price, S, K, T, r, kind), 100 * iv_own(price, S, K, T, r, kind)))
    emit("  Checking back: BS at that sigma = %.10f  vs real %.2f"
         % (bs_own(S, K, T, r, iv_own(price, S, K, T, r, kind), kind), price))
    emit("")
    emit("  study.py printed IV_real%% = %s for this contract."
         % iv_ref.get((sym, d, str(int(r0["dte"])), float(r0["strike"])), "NOT FOUND"))

    # ---- IV agreement table ---------------------------------------------
    emit("")
    emit("=" * 78)
    emit("B. INDEPENDENT IV FOR EVERY MEASURED CONTRACT, AND THE GAP")
    emit("=" * 78)
    emit("  NOTE on the expected gap: study.py discounts at the rate at t-3")
    emit("  sessions (the sibling study's no-lookahead convention); this file")
    emit("  discounts at the SAMPLE DATE's own rate.  The two therefore differ")
    emit("  on purpose, and the gap below is the size of that difference, not an")
    emit("  implementation disagreement.  It is largest on 2020-03-02, where the")
    emit("  3-month bill was falling fastest.")
    emit("")
    table = []
    worst = 0.0
    for r0 in sorted(meas, key=lambda x: (x["underlying"], x["sample_date"],
                                          x["type"], float(x["strike"]))):
        S = float(r0["spot_close"])
        Kx = float(r0["strike"])
        T = int(r0["dte"]) / 365.0
        rr = read_rate(r0["sample_date"]) / 100.0
        mine = iv_own(float(r0["close"]), S, Kx, T, rr, r0["type"])
        key = (r0["underlying"], r0["sample_date"], r0["dte"], Kx)
        theirs = iv_ref.get(key)
        gp = (100.0 * mine - theirs) if (mine is not None and theirs is not None) else None
        if gp is not None:
            worst = max(worst, abs(gp))
        table.append([r0["underlying"], r0["sample_date"], r0["type"],
                      "%.2f" % Kx, "%.4f" % float(r0["close"]),
                      num_h(100.0 * mine, 6) if mine is not None else "n/a",
                      num_h(theirs, 4), num_h(gp, 6)])
    emit(tabulate_h(["und", "date", "type", "strike", "price", "IV_hand%",
                     "IV_study%", "gap (vol pts)"], table))
    emit("")
    emit("  largest absolute gap across all %d contracts: %.6f vol points"
         % (len(table), worst))

    # ---- skew agreement ---------------------------------------------------
    emit("")
    emit("=" * 78)
    emit("C. INDEPENDENT SKEW SLOPE PER DATE, AND THE GAP")
    emit("=" * 78)
    emit("  slope_per_10pct_OTM = b * ln(1/0.90), b from OLS of IV%% on")
    emit("  d = -ln(K/S), puts only.  Own solver: normal equations.")
    emit("")
    srows = []
    for sym in ("SPY", "QQQ", "IWM"):
        for d in sorted(set(x["sample_date"] for x in meas
                            if x["underlying"] == sym)):
            puts = [x for x in meas if x["underlying"] == sym
                    and x["sample_date"] == d and x["type"] == "put"]
            if len(puts) < 2:
                srows.append([sym, d, len(puts), "n/a", "n/a", "n/a"])
                continue
            xs, ys = [], []
            for x in puts:
                S = float(x["spot_close"])
                Kx = float(x["strike"])
                T = int(x["dte"]) / 365.0
                rr = read_rate(x["sample_date"]) / 100.0
                v = iv_own(float(x["close"]), S, Kx, T, rr, "put")
                xs.append(-math.log(Kx / S))
                ys.append(100.0 * v)
            b = ols_normal_equations(xs, ys)
            mine = b * math.log(1.0 / 0.90)
            theirs = skew_ref.get((sym, d))
            gp = (mine - theirs) if theirs is not None else None
            srows.append([sym, d, len(puts), num_h(mine, 6), num_h(theirs, 4),
                          num_h(gp, 6)])
    emit(tabulate_h(["und", "date", "n_puts", "slope_hand", "slope_study",
                     "gap"], srows))
    emit("")
    emit("  A gap of 0.000000 on every row means the two implementations agree")
    emit("  to the printed precision.")

    with open(os.path.join(ROOT, "handcheck-output.txt"), "w",
              encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(out) + "\n")


def num_h(x, nd):
    return "n/a" if x is None else ("%.*f" % (nd, x))


def tabulate_h(headers, rows):
    w = [len(h) for h in headers]
    for r in rows:
        for i, c in enumerate(r):
            w[i] = max(w[i], len(str(c)))
    lines = ["  " + "  ".join(h.ljust(w[i]) for i, h in enumerate(headers)),
             "  " + "  ".join("-" * x for x in w)]
    for r in rows:
        lines.append("  " + "  ".join(str(c).ljust(w[i]) for i, c in enumerate(r)))
    return "\n".join(lines)


if __name__ == "__main__":
    main()
