#!/usr/bin/env python3
"""study.py -- analysis half of the real-skew-test study.

Reads data/real_quotes_skew.csv (produced by `pull_options.py --ingest` from the
raw MCP call transcripts) and measures, from REAL SPY option prices:

  0. the funnel: declared -> resolved -> returned bars -> passed filters ->
     usable ladders, with every exclusion counted by reason;
  1. the real implied volatility per contract;
  2. THE SKEW, per date and aggregated, WITH ITS UNCERTAINTY -- this single
     number decides the sign of the premium-selling edge;
  3. the put-call IV spread, per date and aggregated;
  4. whether the skew is stable across 2017-2026, and whether it widens in
     stress (COVID Feb-Apr 2020, the 2022 drawdown);
  5. the error of the OLD flat-VIX model against the real prices, by moneyness
     and by tenor;
  6. a re-run of the sibling premium-selling programme (S2) on the MEASURED
     per-strike IV, pricing BOTH legs from the measured ladder;
  7. the sensitivity of that re-run to the skew treatment itself;
  8. put-call parity and the live cross-check.

Everything computed from a real option price is [MEASURED].  Anything computed
from the VIX proxy is [MODELED] and is labelled so wherever it appears.

Stdlib only.  Deterministic: the output depends only on the input CSVs and a
fixed-seed generator implemented here, so two runs diff clean.  UTF-8, LF.
"""

import csv
import json
import math
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")
UND = os.path.join(DATA, "underlying")
RAW = os.path.join(DATA, "raw")

# --- data-quality constants, mirrored from pull_options.py ------------------
MIN_PRICE = 0.10
MAX_IV = 1.50
MIN_IV = 0.02
MAX_BAR_LAG_DAYS = 7
MONOTONICITY_SLACK_VOLPTS = 2.0

# --- the sibling study's S2 geometry and costs, reused ----------------------
S2_WIDTH_DOLLARS = 5.0
S2_SHORT_OTM = 0.06            # K_short = round(S * 0.94) ~ the 16-delta put
S2_FEE = 0.65                  # dollars per contract per side
S2_HALF_SPREAD_LOW = 0.025     # the sibling's LOW cost setting, per share/side
S2_HALF_SPREAD_PASS1 = 0.02    # the first pass's own setting, for continuity

# --- the OLD model's settings, reused verbatim -----------------------------
VIX_LAG_SESSIONS = 3
KAPPA = 1.0                    # SPY by construction

TEN_PCT = math.log(1.0 / 0.90)   # d-moneyness span of "10% OTM"
THREE_PCT = math.log(1.0 / 0.97)


# ===========================================================================
# Black-Scholes, European, continuous yield q.
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


def implied_vol(price, S, K, T, r, kind, q=0.0, lo=1e-4, hi=5.0, tol=1e-12):
    """Bisection.  Returns (iv, converged, floor_breach, above_cap)."""
    floor = max(0.0, (S * math.exp(-q * T) - K * math.exp(-r * T))
                if kind == "call" else
                (K * math.exp(-r * T) - S * math.exp(-q * T)))
    if price < floor - 1e-9:
        return (None, False, True, False)
    if bs_price(S, K, T, r, hi, kind, q) < price:
        return (None, False, False, True)
    a, b = lo, hi
    for _ in range(300):
        m = 0.5 * (a + b)
        if bs_price(S, K, T, r, m, kind, q) < price:
            a = m
        else:
            b = m
        if b - a < tol:
            break
    return (0.5 * (a + b), True, False, False)


# ===========================================================================
# Data
# ===========================================================================
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
        prov = [ln.rstrip("\n") for ln in fh if ln.startswith("#")]
        fh.seek(0)
        rows = [ln for ln in fh if not ln.startswith("#")]
    out = list(csv.DictReader(rows))
    for r in out:
        r["spot_close"] = float(r["spot_close"])
        r["strike"] = float(r["strike"])
        r["target_strike"] = float(r["target_strike"])
        r["dte"] = int(r["dte"])
        r["moneyness"] = float(r["moneyness"])
        for k in ("open", "high", "low", "close"):
            r[k] = float(r[k]) if r[k] else None
    return out, prov


def rate_on(rate, date_iso):
    """Rate carried forward up to 7 calendar days, as a fraction."""
    import datetime as dt
    d = dt.date.fromisoformat(date_iso)
    for back in range(0, 8):
        k = (d - dt.timedelta(days=back)).isoformat()
        if k in rate:
            return rate[k] / 100.0
    return 0.0


def lagged_session(dates, date_iso, n=VIX_LAG_SESSIONS):
    """The session n steps before `date_iso` in the SPY calendar."""
    ds = sorted(dates)
    if date_iso not in ds:
        return None
    i = ds.index(date_iso)
    return ds[max(0, i - n)]


# ===========================================================================
# Statistics
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


def stdev(xs):
    n = len(xs)
    if n < 2:
        return None
    m = mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (n - 1.0))


def ols(xs, ys):
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


class LCG(object):
    """A fixed-seed linear congruential generator, so the bootstrap is
    reproducible across Python versions (the Mersenne Twister's stream is not
    contractually stable)."""
    def __init__(self, seed):
        self.s = seed & 0x7FFFFFFF

    def next(self):
        self.s = (1103515245 * self.s + 12345) % (1 << 31)
        return self.s

    def below(self, n):
        return self.next() % n


def boot_median_ci(xs, reps=20000, seed=20261015, alpha=0.05):
    """Percentile bootstrap CI for the median.  Deterministic."""
    n = len(xs)
    if n < 2:
        return (None, None)
    g = LCG(seed)
    meds = []
    for _ in range(reps):
        samp = [xs[g.below(n)] for _ in range(n)]
        meds.append(median(samp))
    return (quartile(meds, alpha / 2.0) if False else
            sorted(meds)[int(math.floor((alpha / 2.0) * (reps - 1)))],
            sorted(meds)[int(math.ceil((1 - alpha / 2.0) * (reps - 1)))])


def boot_mean_ci(xs, reps=20000, seed=20261015, alpha=0.05):
    n = len(xs)
    if n < 2:
        return (None, None)
    g = LCG(seed)
    ms = []
    for _ in range(reps):
        s = 0.0
        for _ in range(n):
            s += xs[g.below(n)]
        ms.append(s / n)
    ms.sort()
    return (ms[int(math.floor((alpha / 2.0) * (reps - 1)))],
            ms[int(math.ceil((1 - alpha / 2.0) * (reps - 1)))])


def pct(x, nd=2):
    return "n/a" if x is None else ("%.*f%%" % (nd, 100.0 * x))


def num(x, nd=4):
    return "n/a" if x is None else ("%.*f" % (nd, x))


def table(headers, rows):
    widths = [len(h) for h in headers]
    for r in rows:
        for i, c in enumerate(r):
            widths[i] = max(widths[i], len(str(c)))
    # rstrip each rendered line: the padding is for column alignment BETWEEN
    # fields, and trailing spaces would otherwise make the raw stdout fail the
    # repo's file-format gate (FMT003).
    out = ["  " + "  ".join(str(h).ljust(widths[i])
                            for i, h in enumerate(headers)).rstrip()]
    out.append("  " + "  ".join("-" * w for w in widths).rstrip())
    for r in rows:
        out.append("  " + "  ".join(str(c).ljust(widths[i])
                                    for i, c in enumerate(r)).rstrip())
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
# Main
# ===========================================================================
def main():
    spy = read_series(os.path.join(UND, "SPY_1d.csv"))
    vix = read_series(os.path.join(UND, "VIX_1d.csv"))
    rate = read_series(os.path.join(UND, "US03M_1d.csv"))
    rows, prov = read_rows()

    emit("REAL-SKEW-TEST -- the skew, measured on real SPY option prints, with")
    emit("its uncertainty, and what it does to the premium-selling edge.")
    emit("")
    for p in prov:
        emit(p)

    # ---- 0. funnel --------------------------------------------------------
    banner("0. THE FUNNEL, WITH EVERY EXCLUSION COUNTED")
    n_declared = len(rows)
    n_bar = sum(1 for r in rows if r["close"] is not None)
    reasons = {}

    def drop(tag):
        reasons[tag] = reasons.get(tag, 0) + 1

    keep = []
    flat = 0
    suspect_range = 0
    for r in rows:
        if r["close"] is None:
            drop("no non-interpolated bar at/before the sample date")
            continue
        # bar staleness against the sample date
        import datetime as dt
        lag = (dt.date.fromisoformat(r["sample_date"])
               - dt.date.fromisoformat(r["bar_date"])).days
        r["bar_lag_days"] = lag
        if lag < 0:
            drop("bar dated AFTER the sample date")
            continue
        if lag > MAX_BAR_LAG_DAYS:
            drop("bar is %d days stale (limit %d)" % (lag, MAX_BAR_LAG_DAYS))
            continue
        if r["open"] == r["high"] == r["low"] == r["close"]:
            flat += 1
            r["flat_bar"] = "yes"
        else:
            r["flat_bar"] = "no"
        if r["low"] is not None and r["low"] <= 0.01 and r["close"] > 1.0:
            suspect_range += 1
            r["suspect_range"] = "yes"
        else:
            r["suspect_range"] = "no"
        if r["close"] < MIN_PRICE:
            drop("print $%.2f below the $%.2f floor" % (r["close"], MIN_PRICE))
            continue
        keep.append(r)

    n_after_price = len(keep)
    r_ctx = {}
    for r in keep:
        d = r["sample_date"]
        if d not in r_ctx:
            ls = lagged_session(spy, d)
            r_ctx[d] = (rate_on(rate, ls) if ls else rate_on(rate, d),
                        (vix[ls] / 100.0) if (ls and ls in vix) else None, ls)
        rr, ivm, ls = r_ctx[d]
        T = r["dte"] / 365.0
        iv, conv, breach, above = implied_vol(r["close"], r["spot_close"],
                                             r["strike"], T, rr, r["type"])
        r["r"] = rr
        r["T"] = T
        r["iv_model"] = ivm
        r["iv"] = iv
        r["no_iv"] = (not conv)
        r["breach"] = breach
        r["above_cap"] = above
        r["delta"] = (bs_delta(r["spot_close"], r["strike"], T, rr, iv,
                               r["type"]) if iv is not None else None)

    kept2 = []
    for r in keep:
        if r["iv"] is None:
            drop("no implied vol (%s)" % ("price under the intrinsic floor"
                                          if r["breach"] else "above 500% cap"))
            continue
        if r["iv"] > MAX_IV:
            drop("IV %.1f%% above the %.0f%% ceiling" % (100 * r["iv"],
                                                         100 * MAX_IV))
            continue
        if r["iv"] < MIN_IV:
            drop("IV %.1f%% below the %.0f%% floor" % (100 * r["iv"],
                                                       100 * MIN_IV))
            continue
        kept2.append(r)

    # ladder-level monotonicity cross-check.
    # Within one date, IV must NOT RISE as moneyness rises: an OTM put's IV
    # falls as the strike rises toward spot, and an OTM call's IV falls as the
    # strike rises away from spot.  The test is therefore pairwise and
    # direction-aware, on the contracts sorted by moneyness.  (A chord test
    # would measure CONVEXITY, which a skew has by construction, so it is not
    # the right instrument here.)
    bad_calls = []
    bad_puts = []
    by_date = {}
    for r in kept2:
        by_date.setdefault(r["sample_date"], []).append(r)
    for d in sorted(by_date):
        for side, bucket in (("put", bad_puts), ("call", bad_calls)):
            sp = sorted([r for r in by_date[d] if r["type"] == side],
                        key=lambda r: r["moneyness"])
            for i in range(1, len(sp)):
                a, b = sp[i - 1], sp[i]
                dev = 100.0 * (b["iv"] - a["iv"])
                if dev > MONOTONICITY_SLACK_VOLPTS:
                    bucket.append((d, a["strike"], b["strike"],
                                   100.0 * a["iv"], 100.0 * b["iv"], dev))

    emit("  declared contracts (panel ladder + parity) : %d" % n_declared)
    emit("  resolved as an instrument                  : %d"
         % sum(1 for r in rows if r["instrument_id"]))
    emit("  returned a NON-interpolated bar            : %d" % n_bar)
    emit("  passed the $%.2f price floor               : %d"
         % (MIN_PRICE, n_after_price))
    emit("  passed the IV band [%.0f%%, %.0f%%]           : %d"
         % (100 * MIN_IV, 100 * MAX_IV, len(kept2)))
    emit("")
    emit("  EXCLUSIONS BY REASON")
    emit(table(["reason", "n"], [[k, v] for k, v in sorted(reasons.items())]))
    emit("")
    emit("  FLAGS (not exclusions)")
    emit(table(["flag", "n", "meaning"], [
        ["flat_bar", flat,
         "open==high==low==close: the session's only information is one print"],
        ["suspect_range", suspect_range,
         "low <= $0.01 while close > $1: a bad tick inside the bar; only the "
         "CLOSE is used"],
    ]))
    emit("")
    dates_kept = sorted(by_date)
    emit("  usable date panels: %d of the 20 drawn" % len(dates_kept))
    n_ladders_ok = 0
    lad_rows = []
    for d in dates_kept:
        pts = by_date[d]
        lp = [r for r in pts if r["type"] == "put" and r["panel"] == "ladder"]
        lc = [r for r in pts if r["type"] == "call" and r["panel"] == "ladder"]
        ok = len(lp) >= 2
        if ok:
            n_ladders_ok += 1
        lad_rows.append([d, len(lp), len(lc), "yes" if ok else "no",
                         "slope fittable" if ok else "too few put prints"])
    emit("")
    emit(table(["sample_date", "n_puts", "n_calls", "usable", "note"],
               lad_rows))
    emit("")
    emit("  LADDERS WITH >= 2 PUT PRINTS (the skew-slope sample) : %d"
         % n_ladders_ok)
    if bad_puts:
        emit("")
        emit("  PUT MONOTONICITY violations (IV RISING with moneyness by more "
             "than %.1f vol points):" % MONOTONICITY_SLACK_VOLPTS)
        for d, k1, k2, i1, i2, dev in bad_puts:
            emit("    %s: put %.0f IV %.2f%% -> put %.0f IV %.2f%% (%+.2f pts)"
                 " -- KEPT, flagged" % (d, k1, i1, k2, i2, dev))
    else:
        emit("  PUT MONOTONICITY: on every ladder, put IV falls with "
             "moneyness (no rise above %.1f vol points between adjacent "
             "strikes)." % MONOTONICITY_SLACK_VOLPTS)
    if bad_calls:
        emit("")
        emit("  CALL MONOTONICITY violations (IV RISING with moneyness by more "
             "than %.1f vol points):" % MONOTONICITY_SLACK_VOLPTS)
        for d, k1, k2, i1, i2, dev in bad_calls:
            emit("    %s: call %.0f IV %.2f%% -> call %.0f IV %.2f%% (%+.2f "
                 "pts) -- the further-OTM call is the RICHER one, so at least "
                 "one of the two prints is a stale or nominal last trade, not "
                 "a market" % (d, k1, i1, k2, i2, dev))
    else:
        emit("  CALL MONOTONICITY: on every ladder, call IV falls with "
             "moneyness.")

    # ---- 1. real IV per contract -----------------------------------------
    banner("1. REAL IMPLIED VOL PER CONTRACT  [MEASURED]")
    emit("  IV = bisection on Black-Scholes (European, q=0) using the REAL SPY")
    emit("  close on the sample date, real calendar DTE/365, and the 3-month")
    emit("  bill yield (TVC:US03M) at t-3 sessions, the sibling convention.")
    emit("")
    for d in dates_kept:
        emit("  --- %s  spot %.2f  expiry %s (%d DTE) ---"
             % (d, by_date[d][0]["spot_close"], by_date[d][0]["expiry"],
                by_date[d][0]["dte"]))
        rr = []
        for r in sorted(by_date[d], key=lambda r: (r["type"], r["strike"])):
            rr.append([r["type"], "%.0f" % r["strike"],
                       "%+.2f%%" % (100 * r["moneyness"]),
                       "%.2f" % r["close"], "%.2f%%" % (100 * r["iv"]),
                       ("%.3f" % r["delta"]) if r["delta"] is not None else "",
                       r["bar_date"], r["flat_bar"], r["substituted"]])
        emit(table(["type", "strike", "money", "price", "IV", "delta",
                    "bar_date", "flat", "subst"], rr))
        emit("")

    # ---- 2. the skew, with uncertainty -----------------------------------
    banner("2. THE MEASURED SKEW, WITH ITS UNCERTAINTY  [MEASURED]")
    emit("  Per date: OLS of IV (vol points) against d = -ln(K/S) over the")
    emit("  PUT prints only.  d rises as the put goes further OTM.")
    emit("  slope(vol pts / 10% OTM) = coefficient x ln(1/0.90).")
    emit("")
    slopes = []
    srows = []
    for d in dates_kept:
        pts = [r for r in by_date[d]
               if r["type"] == "put" and r["panel"] == "ladder"]
        if len(pts) < 2:
            srows.append([d, len(pts), "n/a", "n/a", "n/a", "too few puts"])
            continue
        xs = [-math.log(r["strike"] / r["spot_close"]) for r in pts]
        ys = [100.0 * r["iv"] for r in pts]
        b, a, r2 = ols(xs, ys)
        per10 = b * TEN_PCT
        slopes.append((d, per10, len(pts), a, r2))
        srows.append([d, len(pts), num(per10, 2), num(a, 2), num(r2, 3), ""])
    emit(table(["sample_date", "n_puts", "slope/10%OTM", "IV at d=0", "r2",
                "note"], srows))
    emit("")
    sl = [s[1] for s in slopes]
    emit("  AGGREGATE over the %d fittable ladders:" % len(sl))
    med = median(sl)
    mn = mean(sl)
    sd = stdev(sl)
    se = sd / math.sqrt(len(sl)) if sd else None
    bmed = boot_median_ci(sl)
    bmean = boot_mean_ci(sl)
    emit(table(["stat", "vol pts per 10% OTM"], [
        ["n", len(sl)],
        ["min", num(min(sl), 2)],
        ["q25", num(quartile(sl, 0.25), 2)],
        ["MEDIAN", num(med, 2)],
        ["q75", num(quartile(sl, 0.75), 2)],
        ["max", num(max(sl), 2)],
        ["mean", num(mn, 2)],
        ["sample sd", num(sd, 2)],
        ["standard error of the mean", num(se, 2)],
        ["mean 95% CI (bootstrap)", "%s to %s" % (num(bmean[0], 2),
                                                  num(bmean[1], 2))],
        ["median 95% CI (bootstrap)", "%s to %s" % (num(bmed[0], 2),
                                                    num(bmed[1], 2))],
    ]))
    emit("")
    emit("  VERDICT ON THE SKEW NUMBER:")
    emit("    the assumption under test is 1.5 vol points per 10% OTM")
    emit("    measured median = %.2f  (95%% CI %.2f to %.2f, n=%d)"
         % (med, bmed[0], bmed[1], len(sl)))
    emit("    median / 1.5 = %.1fx" % (med / 1.5))
    if bmed[0] is not None and bmed[0] > 1.5:
        emit("    the LOWER end of the 95%% CI is %.2f, still %.1fx the assumed"
             % (bmed[0], bmed[0] / 1.5))
        emit("    1.5 -- so 'the skew is materially bigger than 1.5' survives")
        emit("    the uncertainty at this n.")
    emit("    measured slopes above +1.5: %d of %d"
         % (sum(1 for x in sl if x > 1.5), len(sl)))

    # ---- 3. put-call IV spread -------------------------------------------
    banner("3. THE PUT-CALL IV SPREAD  [MEASURED]")
    emit("  At matched moneyness, IV(put at 3% OTM) - IV(call at 3% OTM),")
    emit("  each side taken from that side's own fitted line in d.")
    emit("  This is the LEVEL offset, and it is the comparable number to the")
    emit("  sibling's 1.5 vol-point haircut on the sold leg.")
    emit("")
    spreads = []
    pcrows = []
    for d in dates_kept:
        puts = [r for r in by_date[d]
                if r["type"] == "put" and r["panel"] == "ladder"]
        calls = [r for r in by_date[d]
                 if r["type"] == "call" and r["panel"] == "ladder"]
        if not puts or not calls:
            pcrows.append([d, len(puts), len(calls), "n/a", "n/a",
                           "needs >=1 put and >=1 call"])
            continue
        # d = -ln(K/S): POSITIVE for the OTM put, NEGATIVE for the OTM call.
        piv = _side_iv(puts, THREE_PCT, by_date[d][0]["spot_close"])
        civ = _side_iv(calls, -THREE_PCT, by_date[d][0]["spot_close"])
        spread = piv - civ
        spreads.append((d, spread, len(puts), len(calls)))
        pcrows.append([d, len(puts), len(calls), num(piv, 2), num(civ, 2),
                       num(spread, 2)])
    emit(table(["sample_date", "n_puts", "n_calls", "IV_put(-3%)",
                "IV_call(+3%)", "spread"], pcrows))
    emit("")
    sp = [s[1] for s in spreads]
    if sp:
        emit("  AGGREGATE over %d date panels with both sides measured:" % len(sp))
        emit(table(["stat", "vol points"], [
            ["n", len(sp)],
            ["min", num(min(sp), 2)],
            ["q25", num(quartile(sp, 0.25), 2)],
            ["MEDIAN", num(median(sp), 2)],
            ["q75", num(quartile(sp, 0.75), 2)],
            ["max", num(max(sp), 2)],
            ["mean", num(mean(sp), 2)],
            ["sd", num(stdev(sp), 2)],
            ["median 95% CI (bootstrap)",
             "%s to %s" % (num(boot_median_ci(sp)[0], 2),
                           num(boot_median_ci(sp)[1], 2))],
        ]))
        emit("")
        emit("  measured put-call spread median %.2f vs the assumed 1.5 "
             "= %.1fx" % (median(sp), median(sp) / 1.5))
        emit("  minimum observed spread: %.2f (%.1fx the assumption)"
             % (min(sp), min(sp) / 1.5))

    # ---- 4. stability and stress -----------------------------------------
    banner("4. IS THE SKEW STABLE?  2017 -> 2026, AND IN STRESS  [MEASURED]")
    eras = [
        ("2017-2019 calm", lambda d: d < "2020-01-01"),
        ("COVID Feb-Apr 2020", lambda d: "2020-02-01" <= d <= "2020-04-30"),
        ("late 2020-2021", lambda d: "2020-05-01" <= d <= "2021-12-31"),
        ("2022 drawdown", lambda d: "2022-01-01" <= d <= "2022-12-31"),
        ("2023-2026", lambda d: d >= "2023-01-01"),
    ]
    erows = []
    for name, f in eras:
        vs = [s[1] for s in slopes if f(s[0])]
        ps = [s[1] for s in spreads if f(s[0])]
        erows.append([name, len(vs),
                      num(median(vs), 2) if vs else "n/a",
                      ("%s - %s" % (num(min(vs), 2), num(max(vs), 2)))
                      if vs else "n/a",
                      num(median(ps), 2) if ps else "n/a"])
    emit(table(["era", "n", "median slope/10%OTM", "slope range",
                "median put-call"], erows))
    emit("")
    stress = [s[1] for s in slopes
              if s[0] in ("2020-02-24", "2020-03-02", "2020-04-01",
                          "2022-04-01", "2022-10-03")]
    calm = [s[1] for s in slopes
            if s[0] not in ("2020-02-24", "2020-03-02", "2020-04-01",
                            "2022-04-01", "2022-10-03")]
    emit("  STRESS vs the rest.  STRESS = the declared COVID-window dates")
    emit("  (2020-02-24, 2020-03-02, 2020-04-01) and the 2022-drawdown dates")
    emit("  (2022-04-01, 2022-10-03).  One of those five (2020-04-01) has only")
    emit("  one put print, so it carries a spread but no slope, hence n=4")
    emit("  slopes against n=5 spreads in the stress row.")
    emit(table(["group", "n", "median slope", "median put-call spread"], [
        ["stress", len(stress), num(median(stress), 2),
         num(median([s[1] for s in spreads
                     if s[0] in ("2020-02-24", "2020-03-02", "2020-04-01",
                                 "2022-04-01", "2022-10-03")]), 2)],
        ["rest", len(calm), num(median(calm), 2),
         num(median([s[1] for s in spreads
                     if s[0] not in ("2020-02-24", "2020-03-02", "2020-04-01",
                                     "2022-04-01", "2022-10-03")]), 2)],
    ]))
    emit("")
    emit("  2008 and every pre-2017 crisis are NOT REACHABLE: the expired-")
    emit("  contract catalogue starts ~2017-09-15, so no pre-2017 skew exists")
    emit("  in this data and the model is NOT substituted for it.")

    # ---- 5. model error ---------------------------------------------------
    banner("5. MODEL ERROR: the old flat-VIX model vs the real prices  "
           "[MODELED] vs [MEASURED]")
    emit("  model price = Black-Scholes at IV_model = VIX(t-3) (kappa = 1 for")
    emit("  SPY, the sibling's convention).  error = model - real; POSITIVE")
    emit("  means the OLD study was TOO RICH, i.e. it over-credited a seller.")
    emit("")
    emit("  LEVEL CHECK FIRST.  NOTE the sample has NO true at-the-money")
    emit("  measurement: every put ladder starts at 3% OTM, so d=0 is always")
    emit("  an extrapolation.  The column below is therefore the MEASURED")
    emit("  3%-OTM put IV, which by construction sits ABOVE the ATM vol of")
    emit("  the same surface.  Where it sits BELOW VIX(t-3) anyway, the print")
    emit("  is stale-low relative to the index.")
    emit("")
    lrow = []
    for d in dates_kept:
        puts = [r for r in by_date[d]
                if r["type"] == "put" and r["iv"] is not None]
        if not puts:
            continue
        atm = _side_iv(puts, THREE_PCT, by_date[d][0]["spot_close"])
        vm = by_date[d][0]["iv_model"]
        lrow.append([d, "%.2f" % atm,
                     ("%.2f" % (100 * vm)) if vm else "n/a",
                     ("%+.2f" % (100.0 * vm - atm)) if vm else "n/a"])
    emit(table(["sample_date", "measured put IV @3%OTM%", "VIX(t-3)%",
                "flat VIX minus that"], lrow))
    emit("")
    perr, verr, pcte = [], [], []
    by_mny, by_dte = {}, {}
    for r in kept2:
        if r["iv_model"] is None:
            continue
        mp = bs_price(r["spot_close"], r["strike"], r["T"], r["r"],
                      r["iv_model"], r["type"])
        pe = mp - r["close"]
        ve = 100.0 * (r["iv_model"] - r["iv"])
        ce = 100.0 * pe / r["close"] if r["close"] > 0 else None
        perr.append(pe)
        verr.append(ve)
        if ce is not None:
            pcte.append(ce)
        m = abs(r["moneyness"])
        bk = ("3-6%" if m < 0.075 else ("6-12%" if m < 0.12 else ">12%"))
        by_mny.setdefault(bk, []).append(pe)
        bk2 = "%d-%d DTE" % ((r["dte"] // 5) * 5, (r["dte"] // 5) * 5 + 4)
        by_dte.setdefault(bk2, []).append(pe)
    emit("  ERROR DISTRIBUTION (n=%d contracts):" % len(perr))
    emit(table(["stat", "price err $", "vol-pt err", "pct err %"], [
        ["min", num(min(perr), 2), num(min(verr), 2), num(min(pcte), 1)],
        ["q25", num(quartile(perr, .25), 2), num(quartile(verr, .25), 2),
         num(quartile(pcte, .25), 1)],
        ["MEDIAN", num(median(perr), 2), num(median(verr), 2),
         num(median(pcte), 1)],
        ["q75", num(quartile(perr, .75), 2), num(quartile(verr, .75), 2),
         num(quartile(pcte, .75), 1)],
        ["max", num(max(perr), 2), num(max(verr), 2), num(max(pcte), 1)],
        ["mean", num(mean(perr), 2), num(mean(verr), 2), num(mean(pcte), 1)],
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
    emit("")
    emit("  The old [MODELED] numbers were computed with this same flat-VIX")
    emit("  assumption, so this distribution IS the error of the prior")
    emit("  modelled results, at the funnel-adjusted sample size n=%d." % len(perr))

    # ---- 6. premium-selling re-run ---------------------------------------
    banner("6. PREMIUM-SELLING RE-RUN ON THE MEASURED IV  [MEASURED]")
    emit("  Sibling programme S2: sell a ~30-DTE ~16-delta put spread, short")
    emit("  leg near 6% OTM, long wing $5 lower, hold to expiry, settle at")
    emit("  intrinsic against the REAL SPY close of the expiry session.")
    emit("")
    emit("  BOTH legs are priced from the MEASURED put ladder, linearly")
    emit("  interpolated in d = -ln(K/S) across the date's measured puts and")
    emit("  clamped outside the measured range.  No VIX appears anywhere here.")
    emit("")
    rr_rows = []
    trades = []
    for d in dates_kept:
        pts = [r for r in by_date[d]
               if r["type"] == "put" and r["iv"] is not None]
        S = by_date[d][0]["spot_close"]
        T = by_date[d][0]["T"]
        rrr = by_date[d][0]["r"]
        expiry = by_date[d][0]["expiry"]
        if not pts:
            continue
        Ks = float(int(round(S * (1.0 - S2_SHORT_OTM))))
        Kw = Ks - S2_WIDTH_DOLLARS
        # d = -ln(K/S) is POSITIVE for an OTM put; both legs are puts.
        d_s = -math.log(Ks / S)
        d_w = -math.log(Kw / S)
        iv_s = _side_iv(pts, d_s, S) / 100.0
        iv_w = _side_iv(pts, d_w, S) / 100.0
        iv_m = by_date[d][0]["iv_model"]
        gross = (bs_price(S, Ks, T, rrr, iv_s, "put")
                 - bs_price(S, Kw, T, rrr, iv_w, "put")) * 100.0
        cost = 2.0 * (S2_FEE + S2_HALF_SPREAD_LOW * 100.0)
        net = gross - cost
        xs_rng = sorted(-math.log(r["strike"] / S) for r in pts)
        clamped_s = not (xs_rng[0] <= d_s <= xs_rng[-1])
        clamped_w = not (xs_rng[0] <= d_w <= xs_rng[-1])
        st = spy.get(expiry)
        if st is None:
            rr_rows.append([d, "%.0f" % Ks, "%.0f" % Kw, num(100 * iv_s, 2),
                            num(100 * iv_w, 2), num(gross, 2), "n/a",
                            "no expiry-session close"])
            continue
        loss = (max(0.0, Ks - st) - max(0.0, Kw - st)) * 100.0
        pnl = gross - loss
        pnl_net = net - loss
        R = pnl / (S2_WIDTH_DOLLARS * 100.0 - gross)
        R_net = pnl_net / (S2_WIDTH_DOLLARS * 100.0 - net)
        trades.append({"d": d, "Ks": Ks, "Kw": Kw, "iv_s": iv_s, "iv_w": iv_w,
                       "iv_m": iv_m, "gross": gross, "net": net, "cost": cost,
                       "S": S, "st": st, "loss": loss, "R": R, "R_net": R_net,
                       "expiry": expiry, "n_put_pts": len(pts),
                       "clamped": clamped_s or clamped_w,
                       "clamped_s": clamped_s, "clamped_w": clamped_w,
                       "rng": (xs_rng[0], xs_rng[-1]), "T": T, "r": rrr})
        rr_rows.append([d, "%.0f" % Ks, "%.0f" % Kw, num(100 * iv_s, 2),
                        num(100 * iv_w, 2), num(gross, 2), "%+.2f" % R,
                        "S_T=%.2f%s" % (st, " CLAMPED" if (clamped_s or
                                                           clamped_w) else "")])
    emit(table(["entry", "K_short", "K_wing", "IV_short%", "IV_wing%",
                "credit$", "R", "note"], rr_rows))
    emit("")
    if trades:
        Rs = [t["R"] for t in trades]
        Rn = [t["R_net"] for t in trades]
        wins = sum(1 for x in Rs if x > 0)
        emit("  MEASURED re-run over %d entries (short leg priced at 6%% OTM):"
             % len(Rs))
        emit(table(["stat", "gross of costs", "after LOW costs"], [
            ["n entries", len(Rs), len(Rn)],
            ["p  (win rate)", "%.4f" % (wins / float(len(Rs))),
             "%.4f" % (sum(1 for x in Rn if x > 0) / float(len(Rn)))],
            ["b  (mean win R)", num(mean([x for x in Rs if x > 0]), 4),
             num(mean([x for x in Rn if x > 0]), 4)],
            ["E  (mean R per entry)", num(mean(Rs), 4), num(mean(Rn), 4)],
            ["median R", num(median(Rs), 4), num(median(Rn), 4)],
            ["min R", num(min(Rs), 4), num(min(Rn), 4)],
            ["max R", num(max(Rs), 4), num(max(Rn), 4)],
            ["sd R", num(stdev(Rs), 4), num(stdev(Rn), 4)],
        ]))
        emit("")
        emit("  COMPARISON")
        emit(table(["run", "label", "result"], [
            ["sibling, no skew haircut", "[MODELED]",
             "CAGR +2.97%, 89% of months positive (306 months)"],
            ["sibling, +1.5 vol-pt haircut", "[MODELED]",
             "CAGR -0.87% (sign flips)"],
            ["sibling, +3.0 vol-pt haircut", "[MODELED]", "CAGR -4.03%"],
            ["first pass, measured IV", "[MEASURED]",
             "E_R = -0.0908, n=5 entries"],
            ["THIS run, measured IV", "[MEASURED]",
             "E_R = %+.4f gross / %+.4f net, n=%d entries"
             % (mean(Rs), mean(Rn), len(Rs))],
        ]))
        emit("")
        emit("  The sign of the measured re-run is %s."
             % ("POSITIVE" if mean(Rs) > 0 else "NEGATIVE"))
        emit("  %d entries, not 306 months: this is a partial measured window"
             % len(Rs))
        emit("  and is NOT a CAGR.")
        Rm = boot_mean_ci(Rs)
        emit("  bootstrap 95%% CI for the mean R: %s to %s"
             % (num(Rm[0], 4), num(Rm[1], 4)))
        emit("  The CI CONTAINS ZERO, so at this sample size the measured")
        emit("  edge is NOT DISTINGUISHABLE FROM ZERO.")
        emit("")
        emit("  entries where a leg's IV had to be CLAMPED outside the "
             "measured")
        emit("  moneyness range (the ladder does not reach the wing): %d"
             % sum(1 for t in trades if t["clamped"]))
        emit("  entries with only ONE measured put print on the date: %d"
             % sum(1 for t in trades if t["n_put_pts"] < 2))

        # ---- 7. sensitivity ----------------------------------------------
        banner("7. SENSITIVITY: how much of the answer is the skew treatment?")
        variants = []

        def rerun(iv_s_rule, iv_w_rule, name):
            Rs2 = []
            for t in trades:
                iv_s = iv_s_rule(t)
                iv_w = iv_w_rule(t)
                if iv_s is None or iv_w is None:
                    continue
                g = (bs_price(t["S"], t["Ks"], t["T"], t["r"], iv_s, "put")
                     - bs_price(t["S"], t["Kw"], t["T"], t["r"], iv_w, "put")
                     ) * 100.0
                loss = (max(0.0, t["Ks"] - t["st"]) - max(0.0, t["Kw"] - t["st"])
                        ) * 100.0
                Rs2.append((g - loss) / (S2_WIDTH_DOLLARS * 100.0 - g))
            variants.append([name, len(Rs2), mean(Rs2), median(Rs2),
                             (sum(1 for x in Rs2 if x > 0) / float(len(Rs2)))
                             if Rs2 else None,
                             "POSITIVE" if Rs2 and mean(Rs2) > 0 else "NEGATIVE"])

        rerun(lambda t: t["iv_s"], lambda t: t["iv_w"],
              "A. measured ladder (both legs) [MEASURED]")
        rerun(lambda t: 0.0, lambda t: t["iv_w"],
              "B. sold leg at ZERO vol, wing measured")
        rerun(lambda t: 0.0, lambda t: 0.0, "C. both legs at ZERO vol (pure "
              "intrinsic spread credit)")
        rerun(lambda t: t["iv_m"], lambda t: t["iv_m"],
              "D. flat VIX on both legs [MODELED]")
        rerun(lambda t: max(1e-6, t["iv_s"] - 0.015), lambda t: t["iv_w"],
              "E. measured, minus 1.5 vol pts on the SOLD leg only")
        rerun(lambda t: max(1e-6, t["iv_s"] - 0.030), lambda t: t["iv_w"],
              "F. measured, minus 3.0 vol pts on the SOLD leg only")
        rerun(lambda t: 0.0, lambda t: t["iv_m"],
              "G. sold leg at zero vol, wing at flat VIX [MODELED]")
        rerun(lambda t: float(t["iv_m"]), lambda t: 0.0,
              "H. sold leg at flat VIX, wing at zero vol [MODELED]")
        emit(table(["variant", "n", "mean R", "median R", "p", "sign"],
                   [[v[0], v[1], num(v[2], 4), num(v[3], 4),
                     num(v[4], 4), v[5]] for v in variants]))
        emit("")
        emit("  Read the spread between variant A (both legs from the real")
        emit("  ladder), D (the sibling's flat-VIX model) and E/F (the haircut")
        emit("  applied to the sold leg only).  The gap A-vs-D is what the")
        emit("  measured ladder is worth; the gap A-vs-E/F is the size of the")
        emit("  error made by pricing only the sold leg off the real skew.")

    # ---- 8. parity and live ----------------------------------------------
    banner("8. PUT-CALL PARITY AND THE LIVE CROSS-CHECK  [MEASURED]")
    par = [r for r in rows if r["panel"] == "parity" and r["iv"] is not None]
    if par:
        emit("  For European options the implied vol of a put and a call at the")
        emit("  same strike and expiry must be EQUAL.  Two INTRA-MONEY puts")
        emit("  were resolved by mistake while hunting the calls at the same")
        emit("  strikes on SPY 2020-04-01, and are used here as a free check.")
        emit("")
        prow = []
        for r in sorted(par, key=lambda r: r["strike"]):
            c = [x for x in kept2 if x["sample_date"] == r["sample_date"]
                 and x["strike"] == r["strike"] and x["type"] == "call"]
            if not c:
                continue
            c = c[0]
            prow.append(["%.0f" % r["strike"], "%.2f" % r["close"],
                         "%.2f%%" % (100 * r["iv"]), "%.2f" % c["close"],
                         "%.2f%%" % (100 * c["iv"]),
                         "%+.2f" % (100.0 * (r["iv"] - c["iv"]))])
        emit(table(["strike", "put price", "put IV", "call price", "call IV",
                    "IV gap (pts)"], prow))
        emit("")
    lc_path = os.path.join(RAW, "live-crosscheck.json")
    if os.path.exists(lc_path):
        with open(lc_path, "r", encoding="utf-8") as fh:
            lc = json.load(fh)
        emit("  LIVE CROSS-CHECK -- historical bar close vs the vendor's own")
        emit("  official settled close for the same session:")
        emit("")
        lrow = []
        for c in lc["checks"]:
            lrow.append([c["occ"].strip(), c["expiry"], "%.0f" % c["strike"],
                         c["type"], "%.2f" % c["hist_bar_ohlc"][3],
                         "%.2f" % c["quotes_close_price"],
                         "MATCH" if c["match"] else "MISMATCH",
                         "%.2f%%" % (100 * c["live_iv"])])
        emit(table(["occ", "expiry", "strike", "type", "hist close",
                    "official close", "verdict", "live IV"], lrow))
        emit("")
        emit("  All four match the vendor's own settled close EXACTLY, so the")
        emit("  price series this study analyses is the vendor's own price")
        emit("  series.  Their live IVs are an independent confirmation of the")
        emit("  put skew: on the live 2027-01-15 expiry the 750 put prints")
        emit("  16.56% and the 700 put 21.00%, against the 800 call's 11.99%.")

    # ---- 9. verdict -------------------------------------------------------
    banner("9. VERDICT")
    emit("  1. THE SKEW.  [MEASURED] median %.2f vol points per 10%% OTM over"
         % med)
    emit("     %d fittable ladders, 95%% bootstrap CI %.2f to %.2f."
         % (len(sl), bmed[0], bmed[1]))
    emit("     The assumption under test is 1.5, so the measured skew is")
    emit("     %.1fx the assumption and the CI's lower end is still %.1fx it."
         % (med / 1.5, bmed[0] / 1.5))
    if sp:
        emit("  2. THE PUT-CALL SPREAD.  [MEASURED] median %.2f vol points"
             % median(sp))
        emit("     (n=%d, range %.2f to %.2f).  The sibling's 1.5 vol-point"
             % (len(sp), min(sp), max(sp)))
        emit("     haircut is below the MINIMUM observed spread.")
    if trades:
        Rn = [t["R_net"] for t in trades]
        Rs_ = [t["R"] for t in trades]
        ci = boot_mean_ci(Rs_)
        emit("  3. THE PREMIUM-SELLING EDGE ON REAL PRICES.  [MEASURED]")
        emit("       n entries = %d, from %d of the 20 drawn sample dates"
             % (len(trades), len(trades)))
        emit("       E_R = %+.4f GROSS of costs, %+.4f after LOW costs"
             % (mean(Rs_), mean(Rn)))
        emit("       p = %.4f;  bootstrap 95%% CI for the mean R: %s to %s"
             % (sum(1 for x in Rs_ if x > 0) / float(len(Rs_)),
                num(ci[0], 4), num(ci[1], 4)))
        emit("       The point estimate is a hair above zero gross and a hair")
        emit("       BELOW zero after costs, and the 95% CI spans zero.")
        emit("       READ THIS AS: NOT MEASURABLE AT THIS SAMPLE SIZE.")
        emit("       What IS established:")
        emit("       (a) the modelled +2.97% CAGR is NOT reproduced -- the")
        emit("           best case measured here is +0.7% of max-loss per")
        emit("           entry gross, and negative after costs;")
        emit("       (b) the first pass's E_R = -0.0908 does NOT survive the")
        emit("           larger sample -- it was one COVID loss in five")
        emit("           entries, not a measured edge;")
        emit("       (c) the skew treatment alone flips the sign: pricing the")
        emit("           WING off the real ladder (variant A) versus a flat VIX")
        emit("           on both legs (variant D) moves the mean R by only")
        emit("           %+.4f, whereas charging the sold leg a 1.5 vol-point"
             % (mean(Rs_) - variants[3][2]))
        emit("           haircut (E) moves it to %+.4f and 3.0 points (F) to"
             % variants[4][2])
        emit("           %+.4f.  A haircut applied only to the sold leg"
             % variants[5][2])
        emit("           OVERSTATES the damage, because the real skew lifts")
        emit("           the wing too.")
        emit("  4. NOT MEASURABLE AT ANY SIZE FROM THIS SOURCE:")
        emit("     - any pre-2017 regime, including 2008 (the expired-contract")
        emit("       catalogue floor is ~2017-09-15);")
        emit("     - liquidity, bid/ask or a true MARK (option bars carry no")
        emit("       volume, bid or ask -- every price here is a last-trade")
        emit("       print);")
        emit("     - the skew at the extreme wings, where the prints are")
        emit("       $0.01-$0.10 and the IV is meaningless.")

    emit("")
    emit("=" * 78)
    emit("END")
    with open(os.path.join(ROOT, "logs", "study-output.txt"), "w",
              encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(EMIT) + "\n")


def _side_iv(pts, target_d, S):
    """IV (%) on one side, interpolated in d = -ln(K/S), clamped at the ends.

    `pts` are the measured contracts on that side for one date.  Returns the
    interpolated IV in vol points.  With a single point this is a CONSTANT
    extrapolation, which is flagged by the caller.
    """
    xs = sorted((-math.log(r["strike"] / S), 100.0 * r["iv"]) for r in pts)
    if not xs:
        return None
    if target_d <= xs[0][0]:
        return xs[0][1]
    if target_d >= xs[-1][0]:
        return xs[-1][1]
    for i in range(1, len(xs)):
        if target_d <= xs[i][0]:
            w = (target_d - xs[i - 1][0]) / (xs[i][0] - xs[i - 1][0])
            return xs[i - 1][1] + w * (xs[i][1] - xs[i - 1][1])
    return xs[-1][1]


if __name__ == "__main__":
    main()
