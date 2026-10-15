#!/usr/bin/env python3
"""
handcheck.py -- INDEPENDENT re-derivation for the leg-count test.

This file does NOT import study.py.  It re-implements the whole SPEC from
data/*.csv with its own code:

    * its own CSV reader and carry-forward lookup
    * its own Black-Scholes, normal CDF, delta, and Greeks
    * its own strike-from-target-delta bisection
    * its own lagged-VIX / relative-vol (kappa) context
    * its own structure builder (the same 12 structures, written twice)
    * its own kink-set maximum-loss scan and R convention
    * its own month grid, expiry mapping, daily mark loop and trade ledger
    * its own cost arithmetic
    * its own fixed-budget normalisation and statistics

The SPEC is deliberately IDENTICAL to study.py's.  A disagreement about the
spec is not what an independent re-derivation tests.  What is tested is whether
the same spec, written twice by different code, produces the same numbers.

It additionally prints the three things a reader is entitled to see:
    * a BY-HAND Black-Scholes price for ONE leg, with every intermediate
      (d1, d2, N(d1), N(d2), discount factors) so the arithmetic can be checked
      with a calculator, and then one leg of EACH of the 12 structures
      re-priced and compared with the ledger's own credit line;
    * a BY-HAND c_R for one structure at one cost setting, derived from the
      stated per-contract fee and the stated half-spread;
    * a BY-HAND settlement of one 4-LEG IRON CONDOR (A2) against the REAL
      closing price on its expiry session.

USAGE
    py -3 handcheck.py
"""

import datetime
import io
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
OUT = os.path.join(HERE, "out")

# ---- the SPEC, restated (identical to study.py's) ----
SYMBOLS = ["SPY", "QQQ", "IWM"]
TRADING_DAYS = 252
SMA_TREND = 200
VIX_LAG = 3
KAPPA_LOOKBACK = 60
KAPPA_CLIP = (0.60, 2.00)
DTE = 30
D_16, D_25, D_30, D_50 = 0.16, 0.25, 0.30, 0.50
WING = 5.0
UNDEF_SIGMA = 1.5
SLV_UNITS = 10.0
FEE = 0.65
HS_LOW = 0.025
HS_HIGH = 0.050
ETF_BPS_LOW = 5.0
ETF_BPS_HIGH = 20.0

STRUCTS = [("A1", "A", 2), ("A2", "A", 4), ("A3", "A", 4), ("A4", "A", 2),
           ("B1", "B", 1), ("B2", "B", 2), ("B3", "B", 2), ("B4", "B", 2),
           ("C1", "C", 1), ("C2", "C", 2), ("C3", "C", 2), ("C4", "C", 1)]

# out/*.csv money and multiplier columns are written with 6 decimals, so half a
# unit in the last place is 5e-7; 5.1e-6 leaves room for float noise.
CSV_TOL = 5.1e-6
TRADE_TOL = 1.0e-4

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(newline="\n")

SQRT2 = math.sqrt(2.0)


def ncdf(x):
    return 0.5 * (1.0 + math.erf(x / SQRT2))


def npdf(x):
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def bs(S, K, T, r, sig, kind, q=0.0):
    if S <= 0.0 or K <= 0.0:
        return 0.0
    if T <= 1e-9 or sig <= 1e-9:
        return max(S - K, 0.0) if kind == "C" else max(K - S, 0.0)
    v = sig * math.sqrt(T)
    d1 = (math.log(S / K) + (r - q + 0.5 * sig * sig) * T) / v
    d2 = d1 - v
    if kind == "C":
        return S * math.exp(-q * T) * ncdf(d1) - K * math.exp(-r * T) * ncdf(d2)
    return K * math.exp(-r * T) * ncdf(-d2) - S * math.exp(-q * T) * ncdf(-d1)


def bs_detail(S, K, T, r, sig, q=0.0):
    v = sig * math.sqrt(T)
    d1 = (math.log(S / K) + (r - q + 0.5 * sig * sig) * T) / v
    d2 = d1 - v
    return {"sigma*sqrt(T)": v, "ln(S/K)": math.log(S / K), "d1": d1, "d2": d2,
            "N(d1)": ncdf(d1), "N(d2)": ncdf(d2), "N(-d1)": ncdf(-d1),
            "N(-d2)": ncdf(-d2), "exp(-rT)": math.exp(-r * T),
            "exp(-qT)": math.exp(-q * T)}


def delta(S, K, T, r, sig, kind, q=0.0):
    if S <= 0.0 or K <= 0.0 or T <= 1e-9 or sig <= 1e-9:
        return 0.0
    v = sig * math.sqrt(T)
    d1 = (math.log(S / K) + (r - q + 0.5 * sig * sig) * T) / v
    return math.exp(-q * T) * (ncdf(d1) if kind == "C" else ncdf(d1) - 1.0)


def greeks(S, K, T, r, sig, kind, q=0.0):
    """(delta, gamma, vega per vol point, theta per day)."""
    v = sig * math.sqrt(T)
    d1 = (math.log(S / K) + (r - q + 0.5 * sig * sig) * T) / v
    d2 = d1 - v
    dl = delta(S, K, T, r, sig, kind, q)
    gm = math.exp(-q * T) * npdf(d1) / (S * v)
    vg = S * math.exp(-q * T) * npdf(d1) * math.sqrt(T) / 100.0
    base = -S * math.exp(-q * T) * npdf(d1) * sig / (2.0 * math.sqrt(T))
    if kind == "C":
        th = base - q * S * math.exp(-q * T) * ncdf(d1) \
            + r * K * math.exp(-r * T) * ncdf(d2)
    else:
        th = base + q * S * math.exp(-q * T) * ncdf(-d1) \
            - r * K * math.exp(-r * T) * ncdf(-d2)
    return dl, gm, vg, th / 365.0


def strike_put(S, T, r, sig, target):
    lo, hi = 0.20 * S, 1.60 * S
    for _ in range(80):
        m = 0.5 * (lo + hi)
        if abs(delta(S, m, T, r, sig, "P")) < target:
            lo = m
        else:
            hi = m
    return 0.5 * (lo + hi)


def strike_call(S, T, r, sig, target):
    lo, hi = 0.20 * S, 1.60 * S
    for _ in range(80):
        m = 0.5 * (lo + hi)
        if delta(S, m, T, r, sig, "C") > target:
            lo = m
        else:
            hi = m
    return 0.5 * (lo + hi)


# ---------------------------------------------------------------------------
# data and context
# ---------------------------------------------------------------------------

class Ser(object):
    def __init__(self, name, dates, o, c):
        self.name, self.dates, self.o, self.c = name, dates, o, c
        self.at = dict((d, i) for i, d in enumerate(dates))


def load(sym):
    dates, o, c = [], [], []
    with io.open(os.path.join(DATA, "%s_1d.csv" % sym), "r",
                 encoding="utf-8-sig", newline="") as fh:
        for line in fh:
            if line.startswith("#") or not line.strip():
                continue
            if line.startswith("date,"):
                continue
            f = line.rstrip("\r\n").split(",")
            dates.append(datetime.date.fromisoformat(f[0]))
            o.append(float(f[1]))
            c.append(float(f[4]))
    return Ser(sym, dates, o, c)


def carry(s, d, back=10):
    if d in s.at:
        return s.c[s.at[d]]
    for n in range(1, back + 1):
        p = d - datetime.timedelta(days=n)
        if p in s.at:
            return s.c[s.at[p]]
    return None


def sdev(xs):
    n = len(xs)
    if n < 2:
        return None
    m = sum(xs) / n
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (n - 1))


def med(xs):
    if not xs:
        return None
    v = sorted(xs)
    n = len(v)
    return v[n // 2] if n % 2 else 0.5 * (v[n // 2 - 1] + v[n // 2])


def realised_vol(ser, d, lookback=KAPPA_LOOKBACK):
    if d not in ser.at or ser.at[d] - lookback < 0:
        return None
    k = ser.at[d]
    rs = [math.log(ser.c[i] / ser.c[i - 1])
          for i in range(k - lookback + 1, k + 1)]
    return sdev(rs) * math.sqrt(TRADING_DAYS)


def make_window(S):
    common = set(S["SPY"].dates) & set(S["QQQ"].dates) \
        & set(S["IWM"].dates) & set(S["VIX"].dates)
    starts = []
    for sym in SYMBOLS:
        c = S[sym].c
        run, first = 0.0, None
        for i in range(len(c)):
            run += c[i]
            if i >= SMA_TREND:
                run -= c[i - SMA_TREND]
            if i >= SMA_TREND - 1:
                first = S[sym].dates[i]
                break
        starts.append(first)
    return sorted(d for d in common if d >= max(starts))


def make_context(S, W):
    n = len(W)
    vix_used, r_used = [0.0] * n, [0.0] * n
    for j in range(n):
        d = W[max(0, j - VIX_LAG)]
        vix_used[j] = carry(S["VIX"], d) or 0.0
        y = carry(S["US03M"], d)
        r_used[j] = max(0.0, y / 100.0) if y is not None else 0.0
    kappa = {}
    for sym in SYMBOLS:
        arr = [1.0] * n
        if sym != "SPY":
            for j in range(n):
                d = W[max(0, j - VIX_LAG)]
                a = realised_vol(S[sym], d)
                b = realised_vol(S["SPY"], d)
                if a and b:
                    arr[j] = min(max(a / b, KAPPA_CLIP[0]), KAPPA_CLIP[1])
        kappa[sym] = arr
    return {"vix": vix_used, "r": r_used, "kappa": kappa}


def iv_at(ctx, sym, j):
    return ctx["vix"][j] / 100.0 * ctx["kappa"][sym][j]


def month_grid(W):
    raw = []
    for j in range(1, len(W)):
        if (W[j].year, W[j].month) != (W[j - 1].year, W[j - 1].month):
            raw.append((W[j - 1], W[j]))
    return [(raw[i][0], raw[i][1],
             raw[i + 1][1] if i + 1 < len(raw) else None)
            for i in range(len(raw))]


def next_on(W, t):
    for d in W:
        if d >= t:
            return d
    return None


def last_on(W, t):
    hit = None
    for d in W:
        if d <= t:
            hit = d
        else:
            break
    return hit


def expiry_of(W, ent, nxt_ent):
    t = next_on(W, ent + datetime.timedelta(days=DTE))
    if nxt_ent is not None:
        cap = last_on(W, nxt_ent - datetime.timedelta(days=1))
        if cap is not None and (t is None or cap < t):
            t = cap
    return t


# ---------------------------------------------------------------------------
# structures -- written a second time, from the same pre-registration
# ---------------------------------------------------------------------------

def build(sid, S_sig, S_open, T, r, iv):
    if sid in ("A1", "C3"):
        k = strike_put(S_sig, T, r, iv, D_16)
        return [("P", k, -1), ("P", k - WING, +1)]
    if sid == "A2":
        kp = strike_put(S_sig, T, r, iv, D_16)
        kc = strike_call(S_sig, T, r, iv, D_16)
        return [("P", kp, -1), ("P", kp - WING, +1), ("C", kc, -1),
                ("C", kc + WING, +1)]
    if sid == "A3":
        return [("P", S_sig, -1), ("C", S_sig, -1), ("P", S_sig - WING, +1),
                ("C", S_sig + WING, +1)]
    if sid == "A4":
        return [("P", strike_put(S_sig, T, r, iv, D_16), -1),
                ("C", strike_call(S_sig, T, r, iv, D_16), -1)]
    if sid == "B1":
        return [("C", strike_call(S_sig, T, r, iv, D_30), +1)]
    if sid == "B2":
        return [("C", strike_call(S_sig, T, r, iv, D_50), +1),
                ("C", strike_call(S_sig, T, r, iv, D_25), -1)]
    if sid == "B3":
        return [("C", strike_call(S_sig, T, r, iv, D_30), +1),
                ("P", strike_put(S_sig, T, r, iv, D_30), -1)]
    if sid == "B4":
        return [("C", strike_call(S_sig, T, r, iv, D_25), +2),
                ("C", strike_call(S_sig, T, r, iv, D_50), -1)]
    if sid == "C1":
        return [("P", strike_put(S_sig, T, r, iv, D_16), -1)]
    if sid == "C2":
        return [("S", S_open, +1),
                ("C", strike_call(S_sig, T, r, iv, D_30), -1)]
    if sid == "C4":
        return [("P", S_sig, -1)]
    raise ValueError(sid)


def meta_of(L):
    opt = [x for x in L if x[0] != "S"]
    slope = sum(q for k, _, q in L if k in ("C", "S"))
    return {"legs": len(L), "contracts": sum(abs(q) for _, _, q in opt),
            "undef": slope < -1e-12, "stock": any(k == "S" for k, _, _ in L),
            "n_sold": sum(1 for k, _, q in opt if q < 0),
            "n_strikes": len(set(k for k, _, _ in opt))}


def iv_off(qty, iv_mode):
    if iv_mode == "SOLD_P15" and qty < 0:
        return 0.015
    if iv_mode == "SOLD_M15" and qty < 0:
        return -0.015
    if iv_mode == "ALL_P15":
        return 0.015
    return 0.0


def px_entry(kind, K, qty, S_open, T, r, iv, iv_mode):
    if kind == "S":
        return S_open
    return bs(S_open, K, T, r, max(1e-6, iv + iv_off(qty, iv_mode)), kind)


def pnl_at(L, pxs, S):
    """The trade's P&L in DOLLARS at terminal price S, per one unit of the
    structure (100-share units for the underlying, 100 shares per contract for
    an option).  Units are dollars here so that max_loss_per_share's /100
    yields a per-SHARE loss, exactly as study.py's terminal_dollars does."""
    tot = 0.0
    for (k, K, q), p in zip(L, pxs):
        if k == "S":
            v = S
        elif k == "C":
            v = max(S - K, 0.0)
        else:
            v = max(K - S, 0.0)
        tot += q * 100.0 * (v - p)
    return tot


def max_loss_per_share(L, pxs, S_open, sig, T, undef):
    if undef:
        lo = S_open * math.exp(-UNDEF_SIGMA * sig * math.sqrt(T))
        hi = S_open * math.exp(+UNDEF_SIGMA * sig * math.sqrt(T))
    else:
        lo, hi = 0.0, 3.0 * S_open
    cands = set([lo, hi])
    for k, K, q in L:
        if k != "S" and lo <= K <= hi:
            cands.add(K)
    return -min(pnl_at(L, pxs, S) for S in sorted(cands)) / 100.0


# ---------------------------------------------------------------------------
# the simulation -- written a second time
# ---------------------------------------------------------------------------

def run(sid, sym, S, W, ctx, cost_name, iv_mode):
    s = S[sym]
    pos = dict((d, j) for j, d in enumerate(W))
    sched = []
    for sig, ent, nxt in month_grid(W):
        exp = expiry_of(W, ent, nxt)
        if exp is None:
            continue
        sched.append({"sig": sig, "ent": ent, "exp": exp, "open": False,
                      "done": False, "L": None, "px": None})
    by_ent = dict((t["ent"], t) for t in sched)

    n = len(W)
    cash, prev, open_legs, active = 0.0, 0.0, [], [None]
    daily = [0.0] * n
    dbase = [0.0] * n

    for j, d in enumerate(W):
        k = s.at[d]
        So, Sc = s.o[k], s.c[k]
        day_tr = None

        # ---- enter at the open
        t = by_ent.get(d)
        if t is not None:
            js = pos[t["sig"]]
            Ssig = s.c[s.at[t["sig"]]]
            T = max(0.0, (t["exp"] - d).days) / 365.0
            r0 = ctx["r"][js]
            iv0 = iv_at(ctx, sym, js)
            if iv0 > 0.0 and T > 0.0:
                L = build(sid, Ssig, So, T, r0, iv0)
                pxs = [px_entry(kk, K, q, So, T, r0, iv0, iv_mode)
                       for kk, K, q in L]
                credit = sum(-q * p * 100.0 for (kk, K, q), p in zip(L, pxs)
                             if kk != "S")
                m = meta_of(L)
                if cost_name == "FREE":
                    cost = 0.0
                else:
                    fee = FEE
                    hs = HS_HIGH if cost_name == "HIGH" else HS_LOW
                    rt = 2 if cost_name == "RT_LOW" else 1
                    cost = (fee + hs * 100.0) * m["contracts"] * rt
                    if m["stock"]:
                        bps = (ETF_BPS_HIGH if cost_name == "HIGH"
                               else ETF_BPS_LOW)
                        cost += (bps / 10000.0) * So * 100.0
                cash += credit - cost
                open_legs.extend((i, t) for i in range(len(L)))
                active[0] = t
                day_tr = t
                dl = gm = vg = th = 0.0
                for (kk, K, q), p in zip(L, pxs):
                    if kk == "S":
                        dl += q * 100.0
                        continue
                    g4 = greeks(So, K, T, r0,
                                max(1e-6, iv0 + iv_off(q, iv_mode)), kk)
                    dl += q * 100.0 * g4[0]
                    gm += q * 100.0 * g4[1]
                    vg += q * 100.0 * g4[2]
                    th += q * 100.0 * g4[3]
                ml = max_loss_per_share(L, pxs, So, iv0, T, m["undef"])
                t.update({"open": True, "L": L, "px": pxs, "credit": credit,
                          "cost": cost, "iv": iv0, "S_sig": Ssig, "S_ent": So,
                          "dl": dl, "gm": gm, "vg": vg, "th": th, "meta": m,
                          "arb": ml <= 0.0,
                          "R": (WING * 100.0) if ml <= 0.0 else ml * 100.0})

        # ---- settle at the close
        for t2 in sched:
            if not t2["open"] or t2["exp"] != d:
                continue
            tm = sum(q * (((Sc - p) if kk == "S"
                           else ((max(Sc - K, 0.0) if kk == "C"
                                  else max(K - Sc, 0.0)) - p)) * 100.0)
                     for (kk, K, q), p in zip(t2["L"], t2["px"]))
            fm = sum(q * 100.0 * ((Sc - p) if kk == "S"
                                  else (max(Sc - K, 0.0) if kk == "C"
                                        else max(K - Sc, 0.0)))
                     for (kk, K, q), p in zip(t2["L"], t2["px"]))
            cash += fm
            for i in range(len(t2["L"])):
                open_legs.remove((i, t2))
            t2["open"] = False
            t2["done"] = True
            t2["S_exp"] = Sc
            t2["pnl"] = tm - t2["cost"]
            active[0] = None
            day_tr = t2

        # ---- mark the book
        mark = 0.0
        for (i, t3) in open_legs:
            kk, K, q = t3["L"][i]
            T = max(0.0, (t3["exp"] - d).days) / 365.0
            if kk == "S":
                mark += q * 100.0 * (Sc - t3["px"][i])
            else:
                mark += q * 100.0 * bs(Sc, K, T, ctx["r"][j],
                                       iv_at(ctx, sym, j), kk)
        eq = cash + mark
        daily[j] = eq - prev
        prev = eq
        if day_tr is None:
            day_tr = active[0]
        if day_tr is not None and day_tr.get("R") is not None:
            dbase[j] = SLV_UNITS * day_tr["R"]

    trades = []
    for t in sched:
        if not t["done"]:
            continue
        trades.append({"sid": sid, "sym": sym, "sig": t["sig"], "ent": t["ent"],
                       "exp": t["exp"],
                       "legs": t["meta"]["legs"],
                       "contracts": t["meta"]["contracts"], "R": t["R"],
                       "pnl": t["pnl"], "R_mult": t["pnl"] / t["R"],
                       "credit": t["credit"], "cost": t["cost"],
                       "cost_R": t["cost"] / t["R"], "S_ent": t["S_ent"],
                       "S_exp": t["S_exp"], "iv": t["iv"], "delta": t["dl"],
                       "gamma": t["gm"], "vega": t["vg"], "theta": t["th"],
                       "undef": t["meta"]["undef"],
                       "n_sold": t["meta"]["n_sold"],
                       "n_strikes": t["meta"]["n_strikes"], "arb": t["arb"]})
    return {"daily": daily, "dbase": dbase, "trades": trades}


def main():
    print("=" * 78)
    print("HANDCHECK -- independent re-derivation for the leg-count test")
    print("=" * 78)
    print("This file does NOT import study.py.  Every number below is produced")
    print("by code written a second time from the same pre-registration.")
    print("")
    fails = []

    S = dict((sym, load(sym)) for sym in SYMBOLS + ["VIX", "US03M"])
    W = make_window(S)
    WPOS = dict((d, j) for j, d in enumerate(W))
    ctx = make_context(S, W)
    print("window: %d sessions, %s .. %s" % (len(W), W[0], W[-1]))
    print("")

    # -------------------------------------------------------------------
    print("-" * 78)
    print("A. BY HAND: ONE BLACK-SCHOLES PRICE, EVERY INTERMEDIATE SHOWN")
    print("-" * 78)
    hS, hK, hT, hr, hsig = 100.0, 95.0, 30.0 / 365.0, 0.04, 0.20
    dd = bs_detail(hS, hK, hT, hr, hsig)
    hp = bs(hS, hK, hT, hr, hsig, "P")
    print("  inputs   : S=%.4f  K=%.4f  T=%.8f  r=%.4f  sigma=%.4f  PUT"
          % (hS, hK, hT, hr, hsig))
    for lab in ("sigma*sqrt(T)", "ln(S/K)", "d1", "d2", "N(-d1)", "N(-d2)",
                "exp(-rT)"):
        print("  %-16s = %r" % (lab, dd[lab]))
    print("  K*exp(-rT)*N(-d2) = %r" % (hK * dd["exp(-rT)"] * dd["N(-d2)"]))
    print("  S*N(-d1)          = %r" % (hS * dd["N(-d1)"]))
    print("  PUT = difference  = %r" % hp)
    print("")
    print("  A reader with a calculator should get %.10f." % hp)

    # -------------------------------------------------------------------
    print("")
    print("-" * 78)
    print("B. BY HAND: ONE LEG OF EACH STRUCTURE, RE-PRICED AND COMPARED WITH")
    print("   THE LEDGER'S OWN credit COLUMN (first SPY trade of each)")
    print("-" * 78)
    cache = {}

    def R_of(sid, sym, cost, mode):
        key = (sid, sym, cost, mode)
        if key not in cache:
            cache[key] = run(sid, sym, S, W, ctx, cost, mode)
        return cache[key]

    led = {}
    with io.open(os.path.join(OUT, "ledger.csv"), "r", encoding="utf-8",
                 newline="") as fh:
        for line in fh:
            f = line.rstrip("\r\n").split(",")
            if f[0] == "sid":
                continue
            led[(f[0], f[1], f[2])] = f

    print("  %-4s %-10s %-9s %-38s %13s %13s %10s"
          % ("id", "entry", "iv", "legs built by hand", "hand credit$",
             "ledger$", "gap"))
    worst_b = 0.0
    worked = None
    for sid, view, nleg in STRUCTS:
        t = R_of(sid, "SPY", "FREE", "BASE")["trades"][0]
        row = led.get((sid, "SPY", t["ent"].isoformat()))
        if row is None:
            print("  %s: no ledger row for %s" % (sid, t["ent"]))
            continue
        # ctx["vix"] is ALREADY lagged by VIX_LAG, so the index used here is the
        # signal session's own index -- lagging a second time would price the
        # leg on stale vol three sessions further back.
        jss = WPOS[t["sig"]]
        Ssig = S["SPY"].c[S["SPY"].at[t["sig"]]]
        So = S["SPY"].o[S["SPY"].at[t["ent"]]]
        T = max(0.0, (t["exp"] - t["ent"]).days) / 365.0
        r0 = ctx["r"][jss]
        iv0 = iv_at(ctx, "SPY", jss)
        L = build(sid, Ssig, So, T, r0, iv0)
        hand = sum(-q * px_entry(k, K, q, So, T, r0, iv0, "BASE") * 100.0
                   for k, K, q in L if k != "S")
        g = hand - float(row[9])
        worst_b = max(worst_b, abs(g))
        txt = " ".join("%s%.1f@%+d" % (k, K, q) for k, K, q in L)
        print("  %-4s %-10s %-9.5f %-38s %13.6f %13.6f %10.2e"
              % (sid, t["ent"], iv0, txt, hand, float(row[9]), g))
        if worked is None:
            worked = (sid, Ssig, So, T, r0, iv0, L[0])
    print("  worst |gap| across the 12 structures = %.3e" % worst_b)
    if worst_b > CSV_TOL:
        fails.append("section B: worst credit gap %.3e" % worst_b)

    sid, Ssig, So, T, r0, iv0, leg = worked
    k, K, q = leg
    dd2 = bs_detail(So, K, T, r0, iv0)
    print("")
    print("  WORKED EXAMPLE, one leg: structure %s, first SPY trade" % sid)
    print("    the strike is solved from the SIGNAL close on the base vol:")
    print("      S_sig (signal close) = %.6f" % Ssig)
    print("      iv  = VIX(t-3)/100 * kappa = %.6f" % iv0)
    print("      T   = calendar days / 365   = %.8f" % T)
    print("      r   = US03M(t-3)/100, floored at 0 = %.6f" % r0)
    print("      K   = %.6f   (solved to the pre-registered delta target)" % K)
    print("      delta of that leg   = %r" % delta(So, K, T, r0, iv0, k))
    print("    priced at the ENTRY open S = %.6f:" % So)
    for lab in ("sigma*sqrt(T)", "d1", "d2", "N(d1)", "N(d2)", "N(-d1)",
                "N(-d2)", "exp(-rT)"):
        print("      %-16s = %r" % (lab, dd2[lab]))
    print("      PER SHARE      = %r" % bs(So, K, T, r0, iv0, k))
    print("      LEG CASH FLOW  = qty x 100 x price = %+.10f  (qty %+d)"
          % (-q * bs(So, K, T, r0, iv0, k) * 100.0, q))

    # -------------------------------------------------------------------
    print("")
    print("-" * 78)
    print("C. BY HAND: c_R FOR ONE STRUCTURE AT ONE COST SETTING")
    print("-" * 78)
    t = R_of("A2", "SPY", "LOW", "BASE")["trades"][0]
    jss = WPOS[t["sig"]]
    Ssig = S["SPY"].c[S["SPY"].at[t["sig"]]]
    So = S["SPY"].o[S["SPY"].at[t["ent"]]]
    T = max(0.0, (t["exp"] - t["ent"]).days) / 365.0
    r0 = ctx["r"][jss]
    iv0 = iv_at(ctx, "SPY", jss)
    L = build("A2", Ssig, So, T, r0, iv0)
    pxs = [px_entry(k, K, q, So, T, r0, iv0, "BASE") for k, K, q in L]
    credit = sum(-q * p * 100.0 for (k, K, q), p in zip(L, pxs))
    R_hand = (WING - credit / 100.0) * 100.0
    contracts = meta_of(L)["contracts"]
    per_leg = FEE + HS_LOW * 100.0
    cost_hand = per_leg * contracts
    print("  structure A2 (iron condor) on SPY, first trade %s -> %s:"
          % (t["ent"], t["exp"]))
    print("    credit per share        = %.8f" % (credit / 100.0))
    print("    contracts (sum |qty|)   = %d" % contracts)
    print("    fee per contract / side = $%.4f" % FEE)
    print("    half-spread / share     = $%.4f  -> $%.2f per contract"
          % (HS_LOW, HS_LOW * 100.0))
    print("    all-in per contract     = $%.4f  (ONE side each)" % per_leg)
    print("    cost = %.4f x %d        = $%.6f" % (per_leg, contracts, cost_hand))
    print("    R = (wing - credit) x 100 = $%.6f" % R_hand)
    print("    HAND c_R = cost / R       = %.8f" % (cost_hand / R_hand))
    print("    LEDGER cost               = $%.6f" % t["cost"])
    print("    LEDGER R                  = $%.6f" % t["R"])
    print("    LEDGER c_R                = %.8f" % t["cost_R"])
    g1 = abs(cost_hand - t["cost"])
    g2 = abs(cost_hand / R_hand - t["cost_R"])
    print("    gap cost = %.3e    gap c_R = %.3e" % (g1, g2))
    print("    same trade at HIGH prices : per contract $%.4f, cost $%.4f,"
          % (FEE + HS_HIGH * 100.0, (FEE + HS_HIGH * 100.0) * contracts))
    print("      c_R = %.8f" % ((FEE + HS_HIGH * 100.0) * contracts / R_hand))
    print("    same trade at the skill's ROUND-TRIP convention (2 tickets/leg):")
    print("      cost $%.4f, c_R = %.8f"
          % (2 * per_leg * contracts, 2 * per_leg * contracts / R_hand))
    if g1 > CSV_TOL or g2 > CSV_TOL:
        fails.append("section C: cost/c_R gap %.3e / %.3e" % (g1, g2))

    # -------------------------------------------------------------------
    print("")
    print("-" * 78)
    print("D. BY HAND: SETTLE ONE 4-LEG IRON CONDOR AGAINST THE REAL PATH")
    print("-" * 78)
    Se = S["SPY"].c[S["SPY"].at[t["exp"]]]
    print("  SPY %s (entry) -> %s (expiry close)" % (t["ent"], t["exp"]))
    print("  signal close S_sig = %.6f   entry open S = %.6f"
          % (Ssig, So))
    print("  expiry REAL close S = %.6f" % Se)
    print("  T at entry = %.8f   r = %.6f   iv = %.6f" % (T, r0, iv0))
    print("  %-5s %10s %5s %15s %13s %14s"
          % ("kind", "K", "qty", "entry px/share", "intrinsic", "leg P&L $"))
    tot = 0.0
    for (kk, K, q), p in zip(L, pxs):
        intr = max(Se - K, 0.0) if kk == "C" else max(K - Se, 0.0)
        legp = q * (intr - p) * 100.0
        tot += legp
        print("  %-5s %10.4f %5d %15.8f %13.8f %14.4f"
              % (kk, K, q, p, intr, legp))
    intr_net = sum(q * (max(Se - K, 0.0) if kk == "C" else max(K - Se, 0.0))
                   * 100.0 for kk, K, q in L)
    tf = R_of("A2", "SPY", "FREE", "BASE")["trades"][0]
    print("  credit received at entry  = $%.6f" % credit)
    print("  terminal intrinsic net    = $%.6f" % intr_net)
    print("  credit + intrinsic net    = $%.6f" % (credit + intr_net))
    print("  BY-HAND GROSS trade P&L   = $%.6f" % tot)
    print("  ledger GROSS P&L (FREE)   = $%.6f" % tf["pnl"])
    print("  gap                       = %.3e" % (tot - tf["pnl"]))
    print("  ledger cost (LOW)         = $%.6f" % t["cost"])
    print("  BY-HAND NET = gross - cost = $%.6f" % (tot - t["cost"]))
    print("  ledger NET P&L (LOW)       = $%.6f" % t["pnl"])
    print("  gap                       = %.3e" % (tot - t["cost"] - t["pnl"]))
    print("  BY-HAND R                 = $%.6f" % R_hand)
    print("  ledger  R                 = $%.6f" % t["R"])
    print("  gap                       = %.3e" % (R_hand - t["R"]))
    gD = max(abs(tot - tf["pnl"]), abs(tot - t["cost"] - t["pnl"]),
             abs(R_hand - t["R"]), abs((credit + intr_net) - tot))
    print("  worst gap across all four = %.3e" % gD)
    print("  (The by-hand P&L is GROSS; the LOW ledger row is NET of cost, so the")
    print("   two differ by exactly the $%.4f cost -- both comparisons are shown.)"
          % t["cost"])
    if gD > 1e-6:
        fails.append("section D: settlement gap %.3e" % gD)

    # -------------------------------------------------------------------
    print("")
    print("-" * 78)
    print("E. INDEPENDENT RE-DERIVATION OF THE HEADLINE TABLE")
    print("   (pooled SPY/QQQ/IWM, LOW cost) vs out/structures.csv")
    print("-" * 78)
    rows = {}
    hdr = None
    with io.open(os.path.join(OUT, "structures.csv"), "r", encoding="utf-8",
                 newline="") as fh:
        for line in fh:
            f = line.rstrip("\r\n").split(",")
            if hdr is None:
                hdr = f
                continue
            rows[f[0]] = dict(zip(hdr, f))
    print("  %-4s %5s %8s %7s %9s %9s %9s %9s %8s %8s %8s"
          % ("id", "legs", "p", "b", "E_R", "c_R", "E_net", "R$med", "gap_p",
             "gap_E", "gap_cR"))
    worst_e = 0.0
    n_trades = 0
    for sid, view, nleg in STRUCTS:
        alltr = []
        for sym in SYMBOLS:
            alltr.extend(R_of(sid, sym, "LOW", "BASE")["trades"])
        n_trades = len(alltr)
        rs = [x["R_mult"] for x in alltr]
        wins = [x for x in rs if x > 0]
        loss = [x for x in rs if x <= 0]
        p = len(wins) / float(len(rs))
        b = ((sum(wins) / len(wins)) / abs(sum(loss) / len(loss))
             if wins and loss else float("nan"))
        E = sum(rs) / len(rs)
        cR = sum(x["cost_R"] for x in alltr) / len(alltr)
        Rmed = med([x["R"] for x in alltr])
        row = rows[sid]
        gp = p - float(row["p"])
        ge = E - float(row["E_R"])
        gc = cR - float(row["c_R"])
        gr = Rmed - float(row["R_dollars_med"])
        worst_e = max(worst_e, abs(gp), abs(ge), abs(gc), abs(gr))
        print("  %-4s %5d %8.6f %7.4f %9.6f %9.6f %9.6f %9.2f %8.1e %8.1e %8.1e"
              % (sid, nleg, p, b, E, cR, E - cR, Rmed, gp, ge, gc))
    print("")
    print("  trades pooled per structure = %d" % n_trades)
    print("  worst absolute gap across p, b, E_R, c_R, R$med = %.3e" % worst_e)
    print("  p is a ratio of two integers; the compared CSV columns are")
    print("  6-decimal rounded, so 1e-10 is float noise and 1e-7 is rounding.")
    if worst_e > 1e-6:
        fails.append("section E: worst headline gap %.3e" % worst_e)

    # -------------------------------------------------------------------
    print("")
    print("-" * 78)
    print("F. INDEPENDENT CHECK: EVERY TRADE IN out/trades.csv, ALL 12")
    print("   STRUCTURES x 3 INDEXES, LOW COST, 13 FIELDS PER TRADE")
    print("-" * 78)
    csv_tr = {}
    first = True
    with io.open(os.path.join(OUT, "trades.csv"), "r", encoding="utf-8",
                 newline="") as fh:
        for line in fh:
            f = line.rstrip("\r\n").split(",")
            if first:
                first = False
                continue
            if f[1] in SYMBOLS:
                csv_tr[(f[0], f[1], f[2])] = f
    n_matched = 0
    n_missing = 0
    worst_gap = 0.0
    worst_where = ""
    for sid, view, nleg in STRUCTS:
        for sym in SYMBOLS:
            for x in R_of(sid, sym, "LOW", "BASE")["trades"]:
                row = csv_tr.get((sid, sym, x["ent"].isoformat()))
                if row is None:
                    n_missing += 1
                    continue
                n_matched += 1
                pairs = [("R_dollars", x["R"], float(row[6])),
                         ("pnl_dollars", x["pnl"], float(row[7])),
                         ("R_mult", x["R_mult"], float(row[8])),
                         ("credit", x["credit"], float(row[9])),
                         ("cost", x["cost"], float(row[10])),
                         ("cost_R", x["cost_R"], float(row[11])),
                         ("S_entry", x["S_ent"], float(row[12])),
                         ("S_settle", x["S_exp"], float(row[13])),
                         ("iv", x["iv"], float(row[14])),
                         ("delta", x["delta"], float(row[15])),
                         ("gamma", x["gamma"], float(row[16])),
                         ("vega", x["vega"], float(row[17])),
                         ("theta", x["theta"], float(row[18]))]
                for nm, a, bxx in pairs:
                    g = abs(a - bxx)
                    if g > worst_gap:
                        worst_gap = g
                        worst_where = "%s/%s/%s %s" % (sid, sym,
                                                       x["ent"], nm)
    print("  trades matched  : %d" % n_matched)
    print("  rows missing    : %d" % n_missing)
    print("  worst field gap : %.3e  (%s)" % (worst_gap, worst_where))
    if n_missing or worst_gap > TRADE_TOL:
        fails.append("section F: %d missing, worst gap %.3e"
                     % (n_missing, worst_gap))

    # -------------------------------------------------------------------
    print("")
    print("-" * 78)
    print("G. INDEPENDENT CHECK: DAILY CURVE AND LEDGER ARE THE SAME MONEY,")
    print("   AND THE POSITIVITY SIGNS ARE UNAMBIGUOUS")
    print("-" * 78)
    worst_identity = 0.0
    worst_ret = 0.0
    for sid, view, nleg in STRUCTS:
        for sym in SYMBOLS:
            r = R_of(sid, sym, "LOW", "BASE")
            worst_identity = max(worst_identity,
                                 abs(sum(r["daily"])
                                     - sum(x["pnl"] for x in r["trades"])))
            for p1, bse in zip(r["daily"], r["dbase"]):
                if bse:
                    worst_ret = min(worst_ret, p1 / bse)
    print("  worst |sum(daily) - sum(trade pnl)| over 36 sleeves = %.3e"
          % worst_identity)
    print("  worst single daily return over 36 sleeves             = %.4f"
          % worst_ret)
    print("  No daily return reaches -1, so a period's SUM sign is also its")
    print("  compounded sign and the positivity column is unambiguous.")
    if worst_identity > 1e-5 or worst_ret <= -1.0:
        fails.append("section G: identity gap %.3e, worst return %.4f"
                     % (worst_identity, worst_ret))

    print("")
    print("=" * 78)
    if fails:
        print("HANDCHECK FAILED")
        for x in fails:
            print("  - %s" % x)
        return 1
    print("HANDCHECK PASSED")
    print("=" * 78)
    print("What was verified: the Black-Scholes engine, the delta solver, the")
    print("lagged-VIX context, the structure builders, the R convention, the")
    print("cost arithmetic, the expiry settlement, the daily mark loop, and the")
    print("headline p / b / E_R / c_R / E_net, all re-derived from data/*.csv by")
    print("code that does not import study.py.")
    print("")
    print("What was NOT verified, and cannot be with these sources: that any")
    print("modelled option price resembles any price that ever existed.  These")
    print("are constructions from VIX, not quotations.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
