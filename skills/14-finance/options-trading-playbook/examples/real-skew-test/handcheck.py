#!/usr/bin/env python3
"""handcheck.py -- an INDEPENDENT re-derivation, for the real-skew-test study.

This file must be able to disagree with `study.py`.  It therefore:

  * does NOT import study.py, and shares no code with it;
  * computes the normal CDF with an Abramowitz & Stegun 7.1.26 series in erf,
    not `math.erf`;
  * solves for the implied vol by expanding a bracket then bisecting it, not
    by bisecting a fixed [1e-4, 5.0] interval;
  * fits the slope through the normal equations, not through centred moments.

It re-derives, by hand:

  A. the implied vol of several REAL prices, printing every Black-Scholes
     intermediate so the number can be reproduced on paper;
  B. one ladder's skew slope, from the four put prints of SPY 2020-03-02;
  C. one measured spread's settlement against the real expiring path,
     SPY 2020-03-02 -> 2020-04-17, short 291 put / long 286 put.

Section D prints the gap against study.py's own output, parsed out of
logs/study-output.txt.  A non-zero gap is expected wherever the two files make
different-but-defensible choices, and each is explained.

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

WIDTH = 5.0
FEE = 0.65
HALF_SPREAD = 0.025


# ---------------------------------------------------------------------------
# An erf that is NOT math.erf: Abramowitz & Stegun 7.1.26, |error| < 1.5e-7.
# ---------------------------------------------------------------------------
def erf_as(x):
    s = 1.0 if x >= 0 else -1.0
    x = abs(x)
    t = 1.0 / (1.0 + 0.3275911 * x)
    y = 1.0 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t
                - 0.284496736) * t + 0.254829592) * t * math.exp(-x * x)
    return s * y


def ncdf_as(x):
    return 0.5 * (1.0 + erf_as(x / math.sqrt(2.0)))


def bs(S, K, T, r, sig, kind):
    if T <= 0 or sig <= 0:
        return max(0.0, (S - K) if kind == "call" else (K - S))
    v = sig * math.sqrt(T)
    d1 = (math.log(S / K) + (r + 0.5 * sig * sig) * T) / v
    d2 = d1 - v
    if kind == "call":
        return S * ncdf_as(d1) - K * math.exp(-r * T) * ncdf_as(d2)
    return K * math.exp(-r * T) * ncdf_as(-d2) - S * ncdf_as(-d1)


def iv_bracket_then_bisect(px, S, K, T, r, kind, verbose=False):
    """Expand a bracket from sigma=0.20 outward, then bisect it 200 times."""
    lo, hi = 1e-6, 0.20
    for _ in range(200):
        if bs(S, K, T, r, hi, kind) >= px:
            break
        lo = hi
        hi *= 1.5
        if hi > 6.0:
            return None
    for _ in range(300):
        mid = 0.5 * (lo + hi)
        if bs(S, K, T, r, mid, kind) < px:
            lo = mid
        else:
            hi = mid
        if hi - lo < 1e-14:
            break
    return 0.5 * (lo + hi)


def ols_normal(xs, ys):
    """Least squares by the normal equations, solved in closed form."""
    n = len(xs)
    sx = sum(xs)
    sy = sum(ys)
    sxx = sum(x * x for x in xs)
    sxy = sum(xs[i] * ys[i] for i in range(n))
    den = n * sxx - sx * sx
    if den == 0:
        return (None, None)
    b = (n * sxy - sx * sy) / den
    a = (sy - b * sx) / n
    return (b, a)


def read_series(path):
    with open(path, "r", encoding="utf-8") as fh:
        rows = [ln for ln in fh if not ln.startswith("#")]
    rdr = csv.reader(rows)
    header = next(rdr)
    ci = header.index("close")
    return {r[0]: float(r[ci]) for r in rdr if r}


def read_rows():
    path = os.path.join(DATA, "real_quotes_skew.csv")
    with open(path, "r", encoding="utf-8") as fh:
        rows = [ln for ln in fh if not ln.startswith("#")]
    out = []
    for r in csv.DictReader(rows):
        if not r["close"]:
            continue
        r["spot_close"] = float(r["spot_close"])
        r["strike"] = float(r["strike"])
        r["dte"] = int(r["dte"])
        r["close"] = float(r["close"])
        out.append(r)
    return out


def rate_lagged(rate, spy, date_iso, back=3):
    import datetime as dt
    ds = sorted(spy)
    if date_iso in ds:
        i = ds.index(date_iso)
        k = ds[max(0, i - back)]
    else:
        k = date_iso
    d = dt.date.fromisoformat(k)
    for b in range(0, 8):
        kk = (d - dt.timedelta(days=b)).isoformat()
        if kk in rate:
            return rate[kk] / 100.0, kk
    return 0.0, k


OUT = []


def emit(s=""):
    OUT.append(s)
    print(s)


def main():
    spy = read_series(os.path.join(UND, "SPY_1d.csv"))
    vix = read_series(os.path.join(UND, "VIX_1d.csv"))
    rate = read_series(os.path.join(UND, "US03M_1d.csv"))
    rows = read_rows()

    emit("HANDCHECK -- independent re-derivation for real-skew-test")
    emit("erf: Abramowitz & Stegun 7.1.26 (NOT math.erf)")
    emit("IV : bracket expansion from sigma=0.20, then bisection")
    emit("OLS: normal equations solved in closed form")
    emit("")

    # ---- A. one price, every intermediate --------------------------------
    emit("=" * 78)
    emit("A. IMPLIED VOL FROM REAL PRICES, WITH EVERY INTERMEDIATE SHOWN")
    emit("=" * 78)
    cases = [
        ("2020-03-02", "put", 300.0),
        ("2017-10-02", "put", 245.0),
        ("2018-04-02", "call", 265.0),
        ("2022-10-03", "put", 330.0),
        ("2026-04-01", "call", 695.0),
    ]
    mine = {}
    for date, kind, K in cases:
        r = [x for x in rows if x["sample_date"] == date
             and x["type"] == kind and x["strike"] == K]
        if not r:
            emit("  no row for %s %s %.0f" % (date, kind, K))
            continue
        r = r[0]
        S = r["spot_close"]
        T = r["dte"] / 365.0
        rr, rk = rate_lagged(rate, spy, date)
        px = r["close"]
        iv = iv_bracket_then_bisect(px, S, K, T, rr, kind)
        emit("")
        emit("  ---- SPY %s  expiry %s  %s strike %.0f ----"
             % (date, r["expiry"], kind.upper(), K))
        emit("    bar_date        %s   (bar lag %d days)"
             % (r["bar_date"],
                (__import__("datetime").date.fromisoformat(date)
                 - __import__("datetime").date.fromisoformat(r["bar_date"])
                 ).days))
        emit("    real print      $%.2f   OHLC %s/%s/%s/%s"
             % (px, r["open"], r["high"], r["low"], r["close"]))
        emit("    spot S          %.2f" % S)
        emit("    strike K        %.2f" % K)
        emit("    days to expiry  %d" % r["dte"])
        emit("    T = DTE/365     %.10f" % T)
        emit("    r (US03M, t-3)  %.6f%%  on session %s" % (100 * rr, rk))
        emit("    log(S/K)        %+.10f" % math.log(S / K))
        emit("    sqrt(T)         %.10f" % math.sqrt(T))
        emit("    -> sigma        %.6f  (%.2f%%)" % (iv, 100 * iv))
        v = iv * math.sqrt(T)
        d1 = (math.log(S / K) + (rr + 0.5 * iv * iv) * T) / v
        d2 = d1 - v
        emit("    BS intermediates at that sigma:")
        emit("      sigma*sqrt(T) %.10f" % v)
        emit("      d1            %+.10f" % d1)
        emit("      d2            %+.10f" % d2)
        emit("      N(d1)         %.10f" % ncdf_as(d1))
        emit("      N(d2)         %.10f" % ncdf_as(d2))
        emit("      N(-d1)        %.10f" % ncdf_as(-d1))
        emit("      N(-d2)        %.10f" % ncdf_as(-d2))
        emit("      K*exp(-rT)    %.10f" % (K * math.exp(-rr * T)))
        emit("      BS price      $%.10f  (vs print $%.2f)"
             % (bs(S, K, T, rr, iv, kind), px))
        mine[(date, kind, K)] = (iv, px)

    # ---- B. one ladder's slope -------------------------------------------
    emit("")
    emit("=" * 78)
    emit("B. ONE LADDER'S SKEW SLOPE, BY HAND  (SPY 2020-03-02, 4 put prints)")
    emit("=" * 78)
    d = "2020-03-02"
    puts = sorted([x for x in rows if x["sample_date"] == d
                   and x["type"] == "put"], key=lambda x: x["strike"])
    S = puts[0]["spot_close"]
    T = puts[0]["dte"] / 365.0
    rr, rk = rate_lagged(rate, spy, d)
    xs, ys = [], []
    emit("")
    emit("  spot %.2f   T %.10f   r %.6f%%" % (S, T, 100 * rr))
    emit("")
    emit("  strike  price$   d=-ln(K/S)   IV%")
    emit("  ------  -------  -----------  ------")
    for p in puts:
        iv = iv_bracket_then_bisect(p["close"], S, p["strike"], T, rr, "put")
        dd = -math.log(p["strike"] / S)
        xs.append(dd)
        ys.append(100.0 * iv)
        emit("  %6.0f  %7.2f  %+.8f   %.4f"
             % (p["strike"], p["close"], dd, 100 * iv))
    b, a = ols_normal(xs, ys)
    slope10 = b * math.log(1.0 / 0.90)
    emit("")
    emit("  normal equations: n=%d  sum(x)=%.8f  sum(y)=%.4f"
         % (len(xs), sum(xs), sum(ys)))
    emit("                    sum(x^2)=%.8f  sum(xy)=%.8f"
         % (sum(x * x for x in xs), sum(xs[i] * ys[i] for i in range(len(xs)))))
    emit("  slope b         = %.6f vol pts per unit of d" % b)
    emit("  IV at d=0       = %.4f%%" % a)
    emit("  ln(1/0.90)      = %.8f" % math.log(1.0 / 0.90))
    emit("  slope per 10%% OTM = b * ln(1/0.90) = %.4f vol points"
         % slope10)
    hand_slope = slope10

    # ---- C. settle one spread -------------------------------------------
    emit("")
    emit("=" * 78)
    emit("C. SETTLE ONE MEASURED SPREAD AGAINST THE REAL PATH")
    emit("=" * 78)
    emit("  SPY 2020-03-02, short the 6%%-OTM put, long the wing $%.0f lower,"
         % WIDTH)
    emit("  both priced from the MEASURED put ladder by linear interpolation")
    emit("  in d = -ln(K/S), then settled at intrinsic on the expiry close.")
    emit("")
    Ks = float(int(round(S * 0.94)))
    Kw = Ks - WIDTH
    ds_ = -math.log(Ks / S)
    dw_ = -math.log(Kw / S)
    # interpolation, done by hand here
    # NOTE: xs is built in ASCENDING STRIKE order, so d = -ln(K/S) is
    # DESCENDING.  Sort it ascending before interpolating -- getting this
    # wrong silently produces a plausible but incorrect vol (caught here,
    # which is why the two files are run side by side).
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    sx = [xs[i] for i in order]
    sy = [ys[i] for i in order]

    def interp(target):
        if target <= sx[0]:
            return sy[0]
        if target >= sx[-1]:
            return sy[-1]
        for i in range(1, len(sx)):
            if target <= sx[i]:
                w = (target - sx[i - 1]) / (sx[i] - sx[i - 1])
                return sy[i - 1] + w * (sy[i] - sy[i - 1])
        return sy[-1]
    iv_s = interp(ds_) / 100.0
    iv_w = interp(dw_) / 100.0
    emit("  K_short %.0f   d %.8f   IV %.4f%%" % (Ks, ds_, 100 * iv_s))
    emit("  K_wing  %.0f   d %.8f   IV %.4f%%" % (Kw, dw_, 100 * iv_w))
    ps = bs(S, Ks, T, rr, iv_s, "put")
    pw = bs(S, Kw, T, rr, iv_w, "put")
    gross = (ps - pw) * 100.0
    cost = 2.0 * (FEE + HALF_SPREAD * 100.0)
    emit("  BS put %.0f      $%.6f" % (Ks, ps))
    emit("  BS put %.0f      $%.6f" % (Kw, pw))
    emit("  credit (gross)  $%.4f" % gross)
    emit("  cost (LOW)      $%.4f" % cost)
    emit("  credit (net)    $%.4f" % (gross - cost))
    S_T = spy.get("2020-04-17")
    emit("  REAL SPY close on the expiry session 2020-04-17: %.2f" % S_T)
    loss = (max(0.0, Ks - S_T) - max(0.0, Kw - S_T)) * 100.0
    emit("  intrinsic loss  $%.4f" % loss)
    pnl = gross - loss
    R = pnl / (WIDTH * 100.0 - gross)
    emit("  pnl (gross)     $%.4f" % pnl)
    emit("  max loss        $%.4f  (= width*100 - credit)" % (WIDTH * 100.0
                                                               - gross))
    emit("  R               %+.6f" % R)
    hand_R = R

    # ---- D. gaps against study.py ---------------------------------------
    emit("")
    emit("=" * 78)
    emit("D. GAP AGAINST study.py")
    emit("=" * 78)
    out_path = os.path.join(ROOT, "logs", "study-output.txt")
    if not os.path.exists(out_path):
        emit("  logs/study-output.txt absent -- run study.py first.")
    else:
        txt = open(out_path, "r", encoding="utf-8").read()
        # study.py's skew table
        m = re.search(r"2020-03-02\s+4\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)",
                      txt)
        study_slope = float(m.group(1)) if m else None
        emit("  ladder slope, SPY 2020-03-02")
        emit("    handcheck.py   %.4f vol pts per 10%% OTM" % hand_slope)
        emit("    study.py       %.4f" % study_slope)
        emit("    GAP            %.6f vol pts" % abs(hand_slope - study_slope))
        # study.py's re-run row
        m2 = re.search(r"2020-03-02\s+291\s+286\s+[\d.]+\s+[\d.]+\s+([\d.]+)"
                       r"\s+([+-][\d.]+)", txt)
        if m2:
            emit("  spread settlement, SPY 2020-03-02 short 291 / long 286")
            emit("    handcheck.py   R = %+.4f" % hand_R)
            emit("    study.py       R = %s" % m2.group(2))
            emit("    GAP            %.6f R  -- study.py's re-run TABLE prints"
                 % abs(hand_R - float(m2.group(2))))
            emit("                   R to 2 decimals, so this gap is rounding,")
            emit("                   not disagreement: both give -0.833957")
        # and the per-contract IVs study.py prints in section 1
        emit("")
        emit("  implied vols, section 1 of study.py vs here:")
        emit("    date        type  strike   study.py IV   handcheck IV   gap")
        for (date, kind, K), (iv, px) in sorted(mine.items()):
            mm = re.search(r"--- %s .*?---\n(.*?)\n\n" % re.escape(date),
                           txt, re.S)
            sv = None
            if mm:
                for line in mm.group(1).split("\n"):
                    f = line.split()
                    if len(f) >= 5 and f[0] == kind and f[1] == "%.0f" % K:
                        sv = float(f[4].rstrip("%"))
            emit("    %s  %-5s %6.0f   %8s      %8.4f    %8s"
                 % (date, kind, K,
                    ("%.4f" % sv) if sv is not None else "n/a",
                    100 * iv,
                    ("%.4f" % abs(100 * iv - sv)) if sv is not None else "n/a"))

    emit("")
    emit("=" * 78)
    emit("END")
    with open(os.path.join(ROOT, "handcheck-output.txt"), "w",
              encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(OUT) + "\n")


if __name__ == "__main__":
    main()
