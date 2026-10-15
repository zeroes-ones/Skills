#!/usr/bin/env python3
"""study.py -- analysis half of the real-quotes-test study.

Reads the provenance-tagged CSVs produced by `pull_options.py --ingest` and
measures, from REAL option prices:

  1. the real implied volatility per contract (bisection on Black-Scholes);
  2. the real skew per sample date, and its aggregate;
  3. the error of the OLD model (Black-Scholes at a VIX-derived implied vol
     with the sibling study's 3-session lag) against the real prices;
  4. the IV term structure, where two expiries were measured on one date;
  5. a re-run of the sibling premium-selling programme using the MEASURED
     per-strike IV instead of one VIX IV;
  6. whether the skew is stable across the measured dates.

Everything computed from a real option price is [MEASURED].  Anything computed
from the VIX proxy is [MODELED] and is labelled so wherever it appears.

Stdlib only.  Deterministic: the output depends only on the input CSVs, so two
runs diff clean.  UTF-8, LF.
"""

import csv
import math
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")
UND = os.path.join(DATA, "underlying")

# --- the sibling study's cost settings, reused verbatim for the re-run -------
S2_WIDTH_DOLLARS = 5.0        # short put and long wing, $5 apart
S2_FEE = 0.65                 # dollars per contract per side
S2_HALF_SPREAD = 0.02         # dollars per SHARE per side

# The VIX lag and relative-vol clip the sibling model used.  Reproduced so the
# model-error measurement is against the SAME model, not a strawman.
VIX_LAG_SESSIONS = 3
KAPPA_LOOKBACK = 60
KAPPA_CLIP = (0.60, 2.00)


# ===========================================================================
# Black-Scholes, European, continuous yield q.  The only pricer here.
# ===========================================================================
def ncdf(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def bs_price(S, K, T, r, sigma, kind, q=0.0):
    if T <= 0.0 or sigma <= 0.0:
        return max(0.0, (S - K) if kind == "call" else (K - S))
    sq = sigma * math.sqrt(T)
    d1 = (math.log(S / K) + (r - q + 0.5 * sigma * sigma) * T) / sq
    d2 = d1 - sq
    if kind == "call":
        return S * math.exp(-q * T) * ncdf(d1) - K * math.exp(-r * T) * ncdf(d2)
    return K * math.exp(-r * T) * ncdf(-d2) - S * math.exp(-q * T) * ncdf(-d1)


def bs_delta(S, K, T, r, sigma, kind, q=0.0):
    if T <= 0.0 or sigma <= 0.0:
        return 0.0
    sq = sigma * math.sqrt(T)
    d1 = (math.log(S / K) + (r - q + 0.5 * sigma * sigma) * T) / sq
    if kind == "call":
        return math.exp(-q * T) * ncdf(d1)
    return math.exp(-q * T) * (ncdf(d1) - 1.0)


def implied_vol(price, S, K, T, r, kind, q=0.0, lo=1e-4, hi=5.0, tol=1e-10):
    """Bisection.  Returns (iv, converged, intrinsic_floor_breach).

    A price below the no-arbitrage floor (discounted intrinsic) has no implied
    vol; that is reported, never silently clamped to a number.
    """
    floor = max(0.0, (S * math.exp(-q * T) - K * math.exp(-r * T)) if kind == "call"
                else (K * math.exp(-r * T) - S * math.exp(-q * T)))
    if price < floor - 1e-9:
        return (None, False, True)
    if bs_price(S, K, T, r, hi, kind, q) < price:
        return (None, False, False)          # above the 500% cap
    a, b = lo, hi
    for _ in range(200):
        m = 0.5 * (a + b)
        if bs_price(S, K, T, r, m, kind, q) < price:
            a = m
        else:
            b = m
        if b - a < tol:
            break
    return (0.5 * (a + b), True, False)


# ===========================================================================
# Data
# ===========================================================================
def read_series(path):
    """{iso_date: close} from a provenance-tagged OHLCV CSV."""
    with open(path, "r", encoding="utf-8") as fh:
        rows = [ln for ln in fh if not ln.startswith("#")]
    rdr = csv.reader(rows)
    header = next(rdr)
    ci = header.index("close")
    return {r[0]: float(r[ci]) for r in rdr if r}


def read_ladder():
    path = os.path.join(DATA, "real_quotes_ladder.csv")
    with open(path, "r", encoding="utf-8") as fh:
        prov = [ln.rstrip("\n") for ln in fh if ln.startswith("#")]
        fh.seek(0)
        rows = [ln for ln in fh if not ln.startswith("#")]
    rdr = csv.DictReader(rows)
    out = []
    for r in rdr:
        if not r.get("close"):
            continue
        r["spot_close"] = float(r["spot_close"])
        r["strike"] = float(r["strike"])
        r["dte"] = int(r["dte"])
        r["target_pct"] = float(r["target_pct"])
        r["moneyness"] = float(r["moneyness"])
        r["close"] = float(r["close"])
        r["open"] = float(r["open"])
        out.append(r)
    return out, prov


def read_all_plan():
    path = os.path.join(DATA, "real_quotes_ladder.csv")
    with open(path, "r", encoding="utf-8") as fh:
        rows = [ln for ln in fh if not ln.startswith("#")]
    return list(csv.DictReader(rows))


# ===========================================================================
# Statistics helpers
# ===========================================================================
def median(xs):
    s = sorted(xs)
    n = len(s)
    if n == 0:
        return None
    return s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2])


def quartile(xs, p):
    s = sorted(xs)
    if not s:
        return None
    i = p * (len(s) - 1)
    lo = int(math.floor(i))
    hi = int(math.ceil(i))
    if lo == hi:
        return s[lo]
    return s[lo] + (s[hi] - s[lo]) * (i - lo)


def mean(xs):
    return sum(xs) / float(len(xs)) if xs else None


def ols(xs, ys):
    """(slope, intercept, r2) for a simple least-squares fit."""
    n = len(xs)
    if n < 2:
        return (None, None, None)
    mx, my = mean(xs), mean(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    if sxx == 0:
        return (None, None, None)
    sxy = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    b = sxy / sxx
    a = my - b * mx
    syy = sum((y - my) ** 2 for y in ys)
    return (b, a, (b * b * sxx / syy) if syy else None)


def pct(x, nd=2):
    return "n/a" if x is None else ("%.*f%%" % (nd, 100.0 * x))


def num(x, nd=4):
    return "n/a" if x is None else ("%.*f" % (nd, x))


def table(headers, rows):
    widths = [len(h) for h in headers]
    for r in rows:
        for i, c in enumerate(r):
            widths[i] = max(widths[i], len(str(c)))
    out = ["  " + "  ".join(str(h).ljust(widths[i]) for i, h in enumerate(headers))]
    out.append("  " + "  ".join("-" * w for w in widths))
    for r in rows:
        out.append("  " + "  ".join(str(c).ljust(widths[i]) for i, c in enumerate(r)))
    return "\n".join(out)


EMIT = []
def emit(s=""):
    EMIT.append(s)
    print(s)


def banner(t):
    emit("")
    emit("=" * 78)
    emit(t)
    emit("=" * 78)


# ===========================================================================
# The IV model the OLD study used -- [MODELED]
# ===========================================================================
def build_vix_context(sample_date, sym, under, vix, rate):
    """The sibling model's implied vol for `sym` on `sample_date`.

    IV_model = VIX(t - 3 sessions)/100 * kappa(sym, t - 3 sessions)
    kappa = clip(RV60(sym)/RV60(SPY), 0.60, 2.00); 1.0 for SPY by construction.
    Returns (iv_model, vix_used, kappa_used, r_used).
    """
    dates = sorted(under["SPY"].keys())
    idx = dates.index(sample_date) if sample_date in dates else None
    if idx is None:
        return (None, None, None, None)
    k = max(0, idx - VIX_LAG_SESSIONS)
    lag = dates[k]
    # VIX / rate carried forward up to 7 calendar days
    def cf(d, series):
        for back in range(0, 8):
            from datetime import date, timedelta
            dd = (date.fromisoformat(d) - timedelta(days=back)).isoformat()
            if dd in series:
                return series[dd]
        return None
    v = cf(lag, vix)
    r = cf(lag, rate)
    if v is None:
        return (None, None, None, None)
    kap = 1.0
    if sym != "SPY":
        rv_s = rv60(under[sym], dates, k)
        rv_p = rv60(under["SPY"], dates, k)
        if rv_s and rv_p:
            kap = min(max(rv_s / rv_p, KAPPA_CLIP[0]), KAPPA_CLIP[1])
    return (v / 100.0 * kap, v, kap, (r / 100.0 if r else 0.0))


def rv60(series, dates_ref, idx, n=None):
    """Realised vol (annualised stdev of log returns) over n sessions ending at
    dates_ref[idx].  Uses the series' own calendar intersection."""
    if n is None:
        n = KAPPA_LOOKBACK
    ds = sorted(series.keys())
    end = dates_ref[idx]
    j = None
    for i, d in enumerate(ds):
        if d == end:
            j = i
            break
        if d > end:
            j = i - 1
            break
    if j is None or j < n:
        return None
    rets = []
    for i in range(j - n + 1, j + 1):
        a, b = series[ds[i - 1]], series[ds[i]]
        if a > 0:
            rets.append(math.log(b / a))
    if len(rets) < 2:
        return None
    m = mean(rets)
    var = sum((x - m) ** 2 for x in rets) / (len(rets) - 1)
    return math.sqrt(var) * math.sqrt(252.0)


# ===========================================================================
# Main
# ===========================================================================
def main():
    under = {
        "SPY": read_series(os.path.join(UND, "SPY_1d.csv")),
        "QQQ": read_series(os.path.join(UND, "QQQ_1d.csv")),
        "IWM": read_series(os.path.join(UND, "IWM_1d.csv")),
    }
    vix = read_series(os.path.join(UND, "VIX_1d.csv"))
    rate = read_series(os.path.join(UND, "US03M_1d.csv"))
    meas, prov = read_ladder()
    plan = read_all_plan()

    emit("REAL-QUOTES-TEST -- measured option prices, measured skew, and what")
    emit("the old MODELED numbers got wrong.")
    emit("")
    for p in prov:
        emit(p)

    # ---- 1. real IV per contract -----------------------------------------
    banner("1. REAL IMPLIED VOL PER CONTRACT  [MEASURED]")
    emit("  IV = bisection on Black-Scholes (European, q=0) using the REAL")
    emit("  underlying close on the sample date, real calendar DTE/365, and the")
    emit("  3-month bill yield (TVC:US03M) as the risk-free proxy.")
    emit("")
    ctx = {}
    for sym in ("SPY", "QQQ", "IWM"):
        for d in sorted(set(r["sample_date"] for r in meas if r["underlying"] == sym)):
            ctx[(sym, d)] = build_vix_context(d, sym, under, vix, rate)

    for r in meas:
        S, K, T = r["spot_close"], r["strike"], r["dte"] / 365.0
        key = (r["underlying"], r["sample_date"])
        ivm, vv, kk, rr = ctx[key]
        r["r"] = rr if rr is not None else 0.0
        r["T"] = T
        r["vix_used"] = vv
        r["kappa_used"] = kk
        r["iv_model"] = ivm
        iv, ok, breach = implied_vol(r["close"], S, K, T, r["r"], r["type"])
        r["iv_real"] = iv
        r["iv_converged"] = ok
        r["iv_breach"] = breach
        r["delta"] = (bs_delta(S, K, T, r["r"], iv, r["type"])
                      if iv is not None else None)

    rows = []
    for r in sorted(meas, key=lambda r: (r["underlying"], r["sample_date"],
                                         r["type"], r["strike"])):
        rows.append([r["underlying"], r["sample_date"], r["expiry"], r["dte"],
                     r["type"], "%.2f" % r["strike"],
                     "%.4f" % r["moneyness"], r["spot_close"],
                     "%.2f" % r["close"],
                     ("%.2f" % (100 * r["iv_real"])) if r["iv_real"] else "n/a",
                     ("%.3f" % r["delta"]) if r["delta"] is not None else "n/a",
                     ("%.2f" % r["vix_used"]) if r["vix_used"] else "n/a",
                     ("%.2f" % (100 * r["iv_model"])) if r["iv_model"] else "n/a"])
    emit(table(["und", "date", "expiry", "dte", "type", "strike", "money",
                "spot", "price", "IV_real%", "delta", "VIX_lag", "IV_model%"],
               rows))
    good = [r for r in meas if r["iv_real"] is not None]
    emit("")
    emit("  contracts with a real bar: %d of %d planned" % (len(meas), len(plan)))
    emit("  contracts with a real IV  : %d" % len(good))
    emit("  no implied vol (price under the no-arbitrage floor): %d"
         % sum(1 for r in meas if r["iv_breach"]))
    emit("  no implied vol (above the 500%% cap)               : %d"
         % sum(1 for r in meas if not r["iv_converged"] and not r["iv_breach"]))

    # ---- 2. measured skew -------------------------------------------------
    banner("2. THE MEASURED SKEW  [MEASURED]")
    emit("  Fit, per sample date, of IV against d = -ln(K/S) using the PUT")
    emit("  ladder only (OTM puts).  d increases as the put goes further OTM.")
    emit("  slope_per_10pct_OTM = coefficient * ln(1/0.90) vol points.")
    emit("")
    skew_rows = []
    skew_slopes = []
    for sym in ("SPY", "QQQ", "IWM"):
        for d in sorted(set(r["sample_date"] for r in meas
                            if r["underlying"] == sym)):
            puts = [r for r in meas if r["underlying"] == sym
                    and r["sample_date"] == d and r["type"] == "put"
                    and r["iv_real"] is not None]
            calls = [r for r in meas if r["underlying"] == sym
                     and r["sample_date"] == d and r["type"] == "call"
                     and r["iv_real"] is not None]
            if len(puts) < 2:
                skew_rows.append([sym, d, len(puts), "n/a", "n/a", "n/a",
                                  "n/a", "too few puts"])
                continue
            xs = [-math.log(r["strike"] / r["spot_close"]) for r in puts]
            ys = [100.0 * r["iv_real"] for r in puts]
            b, a, r2 = ols(xs, ys)
            per10 = b * math.log(1.0 / 0.90) if b is not None else None
            pc = None
            if calls:
                # put-call IV spread at the closest common moneyness (~3% OTM)
                p3 = min(puts, key=lambda r: abs(abs(r["moneyness"]) - 0.03))
                c3 = min(calls, key=lambda r: abs(abs(r["moneyness"]) - 0.03))
                pc = 100.0 * (p3["iv_real"] - c3["iv_real"])
            skew_rows.append([sym, d, len(puts),
                              num(per10, 2), num(r2, 3), num(a, 2),
                              num(pc, 2), ""])
            if per10 is not None:
                skew_slopes.append((sym, d, per10, pc))
    emit(table(["und", "date", "n_puts", "slope_10%OTM", "r2", "iv_atm%",
                "put-call%", "note"], skew_rows))

    emit("")
    emit("  AGGREGATE (one observation per underlying-date with >=2 puts):")
    sl = [s[2] for s in skew_slopes]
    if sl:
        emit(table(["stat", "slope vol pts per 10% OTM"], [
            ["n", len(sl)],
            ["min", num(min(sl), 2)],
            ["q25", num(quartile(sl, 0.25), 2)],
            ["median", num(median(sl), 2)],
            ["q75", num(quartile(sl, 0.75), 2)],
            ["max", num(max(sl), 2)],
            ["mean", num(mean(sl), 2)],
        ]))
    pcs = [s[3] for s in skew_slopes if s[3] is not None]
    if pcs:
        emit("")
        emit("  put-call IV spread (vol points, put minus call, ~3% OTM):")
        emit(table(["stat", "put-call vol pts"], [
            ["n", len(pcs)],
            ["min", num(min(pcs), 2)],
            ["median", num(median(pcs), 2)],
            ["max", num(max(pcs), 2)],
            ["mean", num(mean(pcs), 2)],
        ]))
    emit("")
    emit("  COMPARISON WITH THE ASSUMED 1.5 VOL POINTS:")
    if sl:
        above = sum(1 for x in sl if x > 1.5)
        emit("    measured slopes above +1.5 vol pts/10%% OTM : %d of %d"
             % (above, len(sl)))
        emit("    median measured slope                     : %.2f vol pts"
             % median(sl))
        emit("    the sibling study's flip point            : -1.5 vol pts")
        emit("    NOTE the sign convention differs: the sibling applied a")
        emit("    haircut of 1.5 vol points to the SOLD leg only, which is a")
        emit("    LEVEL offset, not a slope.  The comparable measured number is")
        emit("    the level difference between the ~16-delta put and ATM, see 5.")

    # ---- 3. model error ---------------------------------------------------
    banner("3. MODEL ERROR: the old VIX-derived model vs the real prices  [MODELED] vs [MEASURED]")
    emit("  model price = Black-Scholes at IV_model = VIX(t-3)/100 * kappa.")
    emit("  error = model - real.  A positive price error means the OLD study")
    emit("  was TOO RICH, i.e. it over-credited the option seller.")
    emit("")
    err_rows = []
    perr, verr, pcterr = [], [], []
    by_mny = {}
    by_dte = {}
    for r in sorted(meas, key=lambda r: (r["underlying"], r["sample_date"],
                                         r["type"], r["strike"])):
        if r["iv_model"] is None:
            continue
        mp = bs_price(r["spot_close"], r["strike"], r["T"], r["r"],
                      r["iv_model"], r["type"])
        pe = mp - r["close"]
        ve = (100.0 * (r["iv_model"] - r["iv_real"])) if r["iv_real"] else None
        ce = (100.0 * pe / r["close"]) if r["close"] > 0 else None
        err_rows.append([r["underlying"], r["sample_date"], r["type"],
                         "%.2f" % r["strike"], "%.4f" % r["moneyness"],
                         "%.2f" % r["close"], "%.2f" % mp,
                         "%+.2f" % pe, num(ve, 2), num(ce, 1)])
        perr.append(pe)
        if ve is not None:
            verr.append(ve)
        if ce is not None:
            pcterr.append(ce)
        m = abs(r["moneyness"])
        bk = ("3-6%" if m < 0.075 else ("6-12%" if m < 0.12 else ">12%"))
        by_mny.setdefault(bk, []).append(pe)
        bk2 = "%d-%d DTE" % ((r["dte"] // 10) * 10, (r["dte"] // 10) * 10 + 9)
        by_dte.setdefault(bk2, []).append(pe)
    emit(table(["und", "date", "type", "strike", "money", "real$", "model$",
                "price_err$", "vol_err_pt", "pct_err%"], err_rows))
    emit("")
    emit("  ERROR DISTRIBUTION (n=%d contracts with a real IV):" % len(perr))
    emit(table(["stat", "price err $", "vol-pt err", "pct err %"], [
        ["min", num(min(perr), 2), num(min(verr), 2), num(min(pcterr), 1)],
        ["q25", num(quartile(perr, .25), 2), num(quartile(verr, .25), 2),
         num(quartile(pcterr, .25), 1)],
        ["median", num(median(perr), 2), num(median(verr), 2),
         num(median(pcterr), 1)],
        ["q75", num(quartile(perr, .75), 2), num(quartile(verr, .75), 2),
         num(quartile(pcterr, .75), 1)],
        ["max", num(max(perr), 2), num(max(verr), 2), num(max(pcterr), 1)],
        ["mean", num(mean(perr), 2), num(mean(verr), 2), num(mean(pcterr), 1)],
    ]))
    emit("")
    emit("  by moneyness band (price error $):")
    emit(table(["band", "n", "median", "mean"],
               [[k, len(v), num(median(v), 2), num(mean(v), 2)]
                for k, v in sorted(by_mny.items())]))
    emit("")
    emit("  by tenor bucket (price error $):")
    emit(table(["bucket", "n", "median", "mean"],
               [[k, len(v), num(median(v), 2), num(mean(v), 2)]
                for k, v in sorted(by_dte.items())]))

    # ---- 4. term structure ------------------------------------------------
    banner("4. IV TERM STRUCTURE  [MEASURED]")
    emit("  One date (SPY 2020-03-02), two expiries, three common strikes.")
    term = [r for r in meas if r["panel"] == "term"]
    short = [r for r in meas if r["underlying"] == "SPY"
             and r["sample_date"] == "2020-03-02" and r["dte"] == 46]
    trows = []
    for k in (300.0, 278.0, 328.0):
        a = [r for r in short if r["strike"] == k and r["type"] == "put"
             or (r["strike"] == k and r["type"] == "call"
                 and any(t["strike"] == k for t in term))]
        longr = [r for r in short if r["strike"] == k]
        shortr = [r for r in term if r["strike"] == k]
        if not longr or not shortr:
            continue
        lo, sh = longr[0], shortr[0]
        trows.append([lo["type"], "%.0f" % k, "%d" % sh["dte"],
                      ("%.2f" % (100 * sh["iv_real"])) if sh["iv_real"] else "n/a",
                      "%.2f" % sh["close"], "%d" % lo["dte"],
                      ("%.2f" % (100 * lo["iv_real"])) if lo["iv_real"] else "n/a",
                      "%.2f" % lo["close"]])
    if trows:
        emit(table(["type", "strike", "dte_short", "IV_short%", "px_short",
                    "dte_long", "IV_long%", "px_long"], trows))
        emit("")
        emit("  Read: the LONGER expiry is richer in absolute price but its IV")
        emit("  is the comparable number.  Only 3 strikes were measured.")
    else:
        emit("  Not measurable from the pulled set.")

    # ---- 5. premium-selling re-run ---------------------------------------
    banner("5. PREMIUM-SELLING RE-RUN WITH THE MEASURED IV  [MEASURED]")
    emit("  Sibling programme S2: each month sell a ~30-DTE put spread, short")
    emit("  leg near 6% OTM (~16 delta), long wing $5 lower, hold to expiry,")
    emit("  settle against the REAL underlying close.")
    emit("")
    emit("  Here the SHORT leg is priced at the IV measured on the ladder,")
    emit("  linearly interpolated in log-moneyness across the measured points;")
    emit("  the WING at the wing's own moneyness.  No VIX is used anywhere in")
    emit("  this section -- that is the whole point of the re-run.")
    emit("")
    rr_rows = []
    Rs = []
    for sym in ("SPY", "QQQ", "IWM"):
        for d in sorted(set(r["sample_date"] for r in meas
                            if r["underlying"] == sym)):
            pts = [r for r in meas if r["underlying"] == sym
                   and r["sample_date"] == d and r["iv_real"] is not None
                   and r["panel"] == "ladder"]
            if len(pts) < 2:
                rr_rows.append([sym, d, "n/a", "n/a", "n/a", "n/a", "n/a",
                                "n/a", "ladder too short"])
                continue
            S = pts[0]["spot_close"]
            T = pts[0]["T"]
            rrr = pts[0]["r"]
            expiry = pts[0]["expiry"]

            def iv_at(m):
                """IV (%) interpolated at log-moneyness m = ln(K/S)."""
                xs = [math.log(r["strike"] / S) for r in pts]
                ys = [100.0 * r["iv_real"] for r in pts]
                order = sorted(range(len(xs)), key=lambda i: xs[i])
                xs = [xs[i] for i in order]
                ys = [ys[i] for i in order]
                if m <= xs[0]:
                    return ys[0]
                if m >= xs[-1]:
                    return ys[-1]
                for i in range(1, len(xs)):
                    if m <= xs[i]:
                        w = (m - xs[i - 1]) / (xs[i] - xs[i - 1])
                        return ys[i - 1] + w * (ys[i] - ys[i - 1])
                return ys[-1]

            Ks = S * 0.94                       # short leg ~6% OTM
            Ks = round(Ks)                      # nearest listed dollar
            Kw = Ks - S2_WIDTH_DOLLARS
            iv_s = iv_at(math.log(Ks / S)) / 100.0
            iv_w = iv_at(math.log(Kw / S)) / 100.0
            cr_gross = (bs_price(S, Ks, T, rrr, iv_s, "put")
                        - bs_price(S, Kw, T, rrr, iv_w, "put")) * 100.0
            cost = 2.0 * (S2_FEE + S2_HALF_SPREAD * 100.0)
            cr_net = cr_gross - cost
            # settlement against the REAL close of the expiry session
            closes = under[sym]
            st = closes.get(expiry)
            if st is None:
                rr_rows.append([sym, d, "%.0f" % Ks, "%.0f" % Kw,
                                num(iv_s * 100, 2), num(iv_w * 100, 2),
                                num(cr_gross, 2), "n/a", "no expiry close"])
                continue
            loss = (max(0.0, Ks - st) - max(0.0, Kw - st)) * 100.0
            pnl = cr_gross - loss
            R = pnl / (S2_WIDTH_DOLLARS * 100.0 - cr_gross)
            Rs.append(R)
            rr_rows.append([sym, d, "%.0f" % Ks, "%.0f" % Kw,
                            num(iv_s * 100, 2), num(iv_w * 100, 2),
                            num(cr_gross, 2), "%+.2f" % R,
                            "S_T=%.2f" % st])
    emit(table(["und", "entry", "K_short", "K_wing", "IV_short%", "IV_wing%",
                "credit$", "R", "note"], rr_rows))
    emit("")
    if Rs:
        wins = sum(1 for x in Rs if x > 0)
        emit("  MEASURED programme over the %d entries above:" % len(Rs))
        emit(table(["stat", "value"], [
            ["n entries", len(Rs)],
            ["p  (win rate)", "%.4f" % (wins / float(len(Rs)))],
            ["b  (mean win R)", num(mean([x for x in Rs if x > 0]), 4)],
            ["E  (mean R per entry)", num(mean(Rs), 4)],
            ["median R", num(median(Rs), 4)],
            ["min R", num(min(Rs), 4)],
            ["max R", num(max(Rs), 4)],
        ]))
        emit("")
        emit("  COMPARISON WITH THE SIBLING [MODELED] RESULT:")
        emit("    sibling, no skew haircut : CAGR +2.97%, 89% of months positive")
        emit("    sibling, +1.5 vol pts    : CAGR -0.87% (sign FLIPS)")
        emit("    sibling, +3.0 vol pts    : CAGR -4.03%")
        emit("    this re-run, measured IV : E_R = %+.4f, sign %s"
             % (mean(Rs), "POSITIVE" if mean(Rs) > 0 else "NEGATIVE"))
        emit("    NOTE: %d measured entries, not 306 months.  This is a partial" % len(Rs))
        emit("    measured window and is NOT a CAGR.")
    else:
        emit("  NOT RUNNABLE: no date had a usable 2+ point put ladder.")

    # ---- 6. skew over time ------------------------------------------------
    banner("6. IS THE SKEW STABLE?  [MEASURED]")
    emit("  One row per measured date, ordered in time.  A single assumed")
    emit("  number is defensible only if these do not move much.")
    emit("")
    tt = sorted([s for s in skew_slopes], key=lambda s: s[1])
    if tt:
        emit(table(["date", "und", "slope_10%OTM", "put-call%"],
                   [[s[1], s[0], num(s[2], 2),
                     num(s[3], 2) if s[3] is not None else "n/a"] for s in tt]))
        emit("")
        emit("  STRESS CHECK: the deepest stress date measured is 2020-03-02")
        emit("  (COVID).  2008 is NOT reachable -- the Robinhood expired-contract")
        emit("  catalogue starts at 2017-09-15, so no pre-2017 crisis exists in")
        emit("  this data.")
    else:
        emit("  No date produced a fittable skew.")

    banner("END")
    with open(os.path.join(ROOT, "logs", "study-output.txt"), "w",
              encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(EMIT) + "\n")


if __name__ == "__main__":
    main()
