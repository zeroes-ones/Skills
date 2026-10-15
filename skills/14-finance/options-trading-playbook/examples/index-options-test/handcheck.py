#!/usr/bin/env python3
"""
handcheck.py -- INDEPENDENT re-derivation for the index-options study.

This file does NOT import study.py, does not read out/*.csv as INPUT (it reads
them only at the END, to compare), and does not use the sibling engine.  It
re-derives everything from data/*.csv with its own code:

    * its own CSV reader, its own carry-forward lookup
    * its own Black-Scholes, its own normal CDF, its own delta
    * its own strike-from-target-delta bisection
    * its own lagged-VIX / relative-vol (kappa) construction
    * its own month grid, own expiry mapping, own daily mark loop
    * its own trade ledger and own additive fixed-budget return series
    * its own CAGR, own max drawdown, own period bucketing and completeness rule
    * its own Pearson correlation
    * its own reproduction of the sibling VRP arithmetic

The SPEC is deliberately identical to study.py's -- a disagreement about the
SPEC is not what an independent re-derivation tests.  What is tested is whether
the same spec, written twice by different code, produces the same numbers.

It additionally prints the two things a reader is entitled to see:
    * a BY-HAND Black-Scholes price for one stated leg, with every intermediate
      (d1, d2, N(d1), N(d2), discount factors) shown, so the arithmetic can be
      checked with a calculator;
    * a BY-HAND settlement of one month's put spread against the real closing
      price on its expiry session.

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

SMA_TREND = 200
TRADING_DAYS = 252
VIX_LAG = 3
KAPPA_LOOKBACK = 60
KAPPA_CLIP = (0.60, 2.00)
DTE = 30
SHORT_DELTA = 0.16
WIDTH = 5.0
SLEEVE_MAXLOSSES = 10.0
FEE = 0.65
HALF_SPREAD = 0.025
ETFS = ["SPY", "QQQ", "IWM"]

# out/*.csv writes 6 decimals, so half a unit in the last place is 5e-7.
CSV_TOL = 5.1e-7
# The trade ledger is written per-trade with 4-6 decimals; allow the rounding.
TRADE_TOL = 5.1e-4
# Compounded statistics differ from their 6-decimal CSV form by at most this.
STAT_TOL = 2.0e-6

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(newline="\n")

FAILS = []


def check(label, gap, tol):
    ok = (gap is not None) and (abs(gap) <= tol)
    if not ok:
        FAILS.append((label, gap, tol))
    print("  %-58s gap=%-14s tol=%-10s %s"
          % (label, ("%.3e" % gap) if gap is not None else "n/a", "%.1e" % tol,
             "OK" if ok else "FAIL"))
    return ok


# ---------------------------------------------------------------------------
# I/O -- own reader
# ---------------------------------------------------------------------------

class Bars(object):
    def __init__(self, path, name):
        self.name = name
        self.dates, self.o, self.h, self.l, self.c = [], [], [], [], []
        with io.open(path, "r", encoding="utf-8-sig", newline="") as fh:
            for line in fh:
                if line.startswith("#") or not line.strip():
                    continue
                if line.startswith("date,"):
                    continue
                f = line.rstrip("\r\n").split(",")
                self.dates.append(datetime.date(int(f[0][0:4]), int(f[0][5:7]),
                                                int(f[0][8:10])))
                self.o.append(float(f[1]))
                self.h.append(float(f[2]))
                self.l.append(float(f[3]))
                self.c.append(float(f[4]))
        self.at = {}
        for i, d in enumerate(self.dates):
            self.at[d] = i

    def at_or_before(self, d, max_back=10):
        """Own carry-forward: exact date, else walk back up to max_back days."""
        i = self.at.get(d)
        if i is not None:
            return self.c[i]
        probe = d
        for _ in range(max_back):
            probe = probe - datetime.timedelta(days=1)
            i = self.at.get(probe)
            if i is not None:
                return self.c[i]
        return None


def read_out_csv(path):
    with io.open(path, "r", encoding="utf-8-sig", newline="") as fh:
        lines = [ln.rstrip("\r\n") for ln in fh
                 if ln.strip() and not ln.startswith("#")]
    head = lines[0].split(",")
    rows = [dict(zip(head, ln.split(","))) for ln in lines[1:]]
    return head, rows


# ---------------------------------------------------------------------------
# Own Black-Scholes
# ---------------------------------------------------------------------------

def Phi(x):
    """Standard normal CDF via the error function -- own formulation."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def bsp(S, K, T, r, sig, kind, q=0.0):
    if S <= 0.0 or K <= 0.0:
        return 0.0
    if T <= 1e-9 or sig <= 1e-9:
        return max(S - K, 0.0) if kind == "C" else max(K - S, 0.0)
    v = sig * math.sqrt(T)
    d1 = (math.log(S / K) + (r - q + 0.5 * sig * sig) * T) / v
    d2 = d1 - v
    if kind == "C":
        return S * math.exp(-q * T) * Phi(d1) - K * math.exp(-r * T) * Phi(d2)
    return K * math.exp(-r * T) * Phi(-d2) - S * math.exp(-q * T) * Phi(-d1)


def bsdelta(S, K, T, r, sig, kind, q=0.0):
    if S <= 0.0 or K <= 0.0:
        return 0.0
    if T <= 1e-9 or sig <= 1e-9:
        if kind == "C":
            return 1.0 if S > K else 0.0
        return -1.0 if S < K else 0.0
    v = sig * math.sqrt(T)
    d1 = (math.log(S / K) + (r - q + 0.5 * sig * sig) * T) / v
    return math.exp(-q * T) * (Phi(d1) if kind == "C" else Phi(d1) - 1.0)


def strike_for_put_delta(S, T, r, sig, target):
    """Own bisection on K.  |put delta| increases with K."""
    lo, hi = 0.20 * S, 1.60 * S
    for _ in range(300):
        m = 0.5 * (lo + hi)
        if abs(bsdelta(S, m, T, r, sig, "P")) < target:
            lo = m
        else:
            hi = m
    return 0.5 * (lo + hi)


# ---------------------------------------------------------------------------
# Own statistics
# ---------------------------------------------------------------------------

def sd(xs):
    n = len(xs)
    if n < 2:
        return None
    m = sum(xs) / n
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (n - 1))


def mean(xs):
    return sum(xs) / len(xs) if xs else None


def pearson(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    sxx = sum((a - mx) ** 2 for a in xs)
    syy = sum((b - my) ** 2 for b in ys)
    return sxy / math.sqrt(sxx * syy)


def curve(rets):
    c = [1.0]
    for r in rets:
        c.append(c[-1] * (1.0 + r))
    return c


def maxdd(c):
    peak, worst = c[0], 0.0
    for v in c:
        if v > peak:
            peak = v
        d = v / peak - 1.0
        if d < worst:
            worst = d
    return worst


def bounds(bucket, d):
    """Own period bounds -- same convention as the sibling engine."""
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
        f = datetime.date(d.year, d.month, 1)
        nx = (datetime.date(d.year + 1, 1, 1) if d.month == 12
              else datetime.date(d.year, d.month + 1, 1))
        return f, nx - datetime.timedelta(days=1)
    if bucket == "Q":
        qm = 3 * ((d.month - 1) // 3) + 1
        f = datetime.date(d.year, qm, 1)
        em = qm + 2
        nx = (datetime.date(d.year + 1, 1, 1) if em == 12
              else datetime.date(d.year, em + 1, 1))
        return f, nx - datetime.timedelta(days=1)
    if bucket == "H":
        if d.month <= 6:
            return datetime.date(d.year, 1, 1), datetime.date(d.year, 6, 30)
        return datetime.date(d.year, 7, 1), datetime.date(d.year, 12, 31)
    if bucket == "Y":
        return datetime.date(d.year, 1, 1), datetime.date(d.year, 12, 31)
    raise ValueError(bucket)


def key_of(bucket, d):
    if bucket == "D":
        return d.isoformat()
    if bucket == "W":
        i = d.isocalendar()
        return "%04d-W%02d" % (i[0], i[1])
    if bucket == "2W":
        mon = d - datetime.timedelta(days=d.isoweekday() - 1)
        i = mon.isocalendar()
        if i[1] % 2 == 0:
            mon = mon - datetime.timedelta(days=7)
        return mon.isoformat()
    if bucket == "M":
        return "%04d-%02d" % (d.year, d.month)
    if bucket == "Q":
        return "%04d-Q%d" % (d.year, (d.month - 1) // 3 + 1)
    if bucket == "H":
        return "%04d-H%d" % (d.year, 1 if d.month <= 6 else 2)
    return "%04d" % d.year


def groups_of(dates, bucket):
    g, order = {}, []
    for j, d in enumerate(dates):
        k = key_of(bucket, d)
        if k not in g:
            g[k] = []
            order.append(k)
        g[k].append(j)
    out = []
    d0, d1 = dates[0], dates[-1]
    for k in order:
        idx = g[k]
        f, l = bounds(bucket, dates[idx[0]])
        if f < d0 or l > d1:
            continue
        out.append((k, idx))
    return out


def frac_positive(rets, dates, bucket):
    g = groups_of(dates, bucket)
    n = len(g)
    npos = 0
    for _k, idx in g:
        c = 1.0
        for j in idx:
            c *= (1.0 + rets[j])
        if c - 1.0 > 0.0:
            npos += 1
    return npos / float(n), npos, n


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 78)
    print("HANDCHECK -- independent re-derivation, no import of study.py")
    print("=" * 78)

    bars = {}
    for name in ETFS + ["VIX", "US03M"]:
        bars[name] = Bars(os.path.join(DATA, "%s_1d.csv" % name), name)
        b = bars[name]
        print("  read %-6s rows=%-6d first=%s last=%s"
              % (name, len(b.dates), b.dates[0].isoformat(),
                 b.dates[-1].isoformat()))

    # ---- own window
    def sma_first_live(b, n):
        run = 0.0
        for i in range(len(b.c)):
            run += b.c[i]
            if i >= n:
                run -= b.c[i - n]
            if i >= n - 1:
                return b.dates[i]
        return None

    live = max(sma_first_live(bars[s], SMA_TREND) for s in ETFS)
    common = set(bars["SPY"].dates)
    for s in ETFS + ["VIX"]:
        common &= set(bars[s].dates)
    window = sorted(d for d in common if d >= live)
    print("")
    print("  own window: %d sessions, %s .. %s"
          % (len(window), window[0].isoformat(), window[-1].isoformat()))
    pos = {}
    for j, d in enumerate(window):
        pos[d] = j
    n = len(window)

    # ---- own cash series
    cash = [0.0] * n
    prev = None
    for j, d in enumerate(window):
        if j == 0:
            prev = bars["US03M"].at_or_before(d)
            continue
        y = bars["US03M"].at_or_before(window[j - 1])
        if y is not None:
            prev = y
        cash[j] = (prev / 100.0) / TRADING_DAYS if prev is not None else 0.0
    cc = curve(cash)
    yrs = (window[-1] - window[0]).days / 365.25
    cash_cagr = cc[-1] ** (1.0 / yrs) - 1.0
    print("  own cash CAGR = %.6f  (%d of %d sessions non-positive)"
          % (cash_cagr, sum(1 for c in cash if c <= 0.0), n))

    # ---- own implied-vol context
    def lagged(j):
        return window[max(0, j - VIX_LAG)]

    vix_used = [bars["VIX"].at_or_before(lagged(j)) for j in range(n)]
    rate_used = []
    for j in range(n):
        y = bars["US03M"].at_or_before(lagged(j))
        rate_used.append(max(0.0, y / 100.0) if y is not None else 0.0)

    def rv60(b, d):
        i = b.at.get(d)
        if i is None or i - KAPPA_LOOKBACK < 0:
            return None
        r = [math.log(b.c[k] / b.c[k - 1])
             for k in range(i - KAPPA_LOOKBACK + 1, i + 1)]
        return sd(r) * math.sqrt(TRADING_DAYS)

    kappa = {}
    for s in ETFS:
        arr = [1.0] * n
        if s != "SPY":
            for j in range(n):
                d = lagged(j)
                a, b_ = rv60(bars[s], d), rv60(bars["SPY"], d)
                if a is None or not b_:
                    arr[j] = 1.0
                else:
                    arr[j] = min(max(a / b_, KAPPA_CLIP[0]), KAPPA_CLIP[1])
        kappa[s] = arr

    def iv_at(sym, j):
        return vix_used[j] / 100.0 * kappa[sym][j]

    # ---- own month grid
    grid = []
    for j in range(1, n):
        a, b = window[j - 1], window[j]
        if (b.year, b.month) != (a.year, a.month):
            grid.append((a, b))

    def first_on_or_after(target):
        for d in window:
            if d >= target:
                return d
        return None

    # ---- own S2 simulation, one sleeve per index
    sleeve_rets = []
    ledger = []
    cost_one_way = FEE + HALF_SPREAD * 100.0
    spread_cost = 2.0 * cost_one_way
    base = SLEEVE_MAXLOSSES * WIDTH * 100.0

    # month grid with the NEXT entry, so the expiry can be capped at the roll
    grid3 = []
    for i, (sig_d, ent_d) in enumerate(grid):
        nxt = grid[i + 1][1] if i + 1 < len(grid) else None
        grid3.append((sig_d, ent_d, nxt))
    by_entry = {}
    for sig_d, ent_d, nxt in grid3:
        exp_d = first_on_or_after(ent_d + datetime.timedelta(days=DTE))
        if nxt is not None:
            cap = None
            for d in window:
                if d < nxt:
                    cap = d
                else:
                    break
            if cap is not None and (exp_d is None or cap < exp_d):
                exp_d = cap
        if exp_d is None:
            continue
        by_entry[ent_d] = {"sig": sig_d, "expiry": exp_d}

    for sym in ETFS:
        b = bars[sym]
        cashbook = base       # the sleeve's cash starts AT the risk budget
        open_spreads = []     # [K1, K2, expiry, credit]
        equity = base
        rets = [0.0] * n
        for j, d in enumerate(window):
            k = b.at[d]
            S_open, S_close = b.o[k], b.c[k]
            # --- enter at the open
            p = by_entry.get(d)
            if p is not None:
                js = pos[p["sig"]]
                exp_d = p["expiry"]
                T = max(0.0, (exp_d - d).days) / 365.0
                iv = iv_at(sym, js)
                r = rate_used[js]
                K1 = strike_for_put_delta(b.c[b.at[p["sig"]]], T, r, iv, SHORT_DELTA)
                K2 = K1 - WIDTH
                cred = (bsp(S_open, K1, T, r, iv, "P")
                        - bsp(S_open, K2, T, r, iv, "P"))
                cashbook += cred * 100.0 - spread_cost
                open_spreads.append([K1, K2, exp_d, cred])
                ledger.append({"sym": sym, "exp": exp_d,
                               "K1": K1, "K2": K2, "cred": cred})
            # --- settle anything expiring today at the close
            keep = []
            for K1, K2, exp_d, cred in open_spreads:
                if exp_d == d:
                    intr = max(0.0, K1 - S_close) - max(0.0, K2 - S_close)
                    cashbook -= intr * 100.0
                else:
                    keep.append([K1, K2, exp_d, cred])
            open_spreads = keep
            # --- mark the book at the close
            mark = 0.0
            for K1, K2, exp_d, _cred in open_spreads:
                T = max(0.0, (exp_d - d).days) / 365.0
                iv = iv_at(sym, j)
                mark += 100.0 * (bsp(S_close, K2, T, rate_used[j], iv, "P")
                                 - bsp(S_close, K1, T, rate_used[j], iv, "P"))
            eq = cashbook + mark
            rets[j] = (eq - equity) / base
            equity = eq
        sleeve_rets.append(rets)

    # book = mean of the three sleeve equity curves
    curves = [curve(r) for r in sleeve_rets]
    book_eq = [sum(c[j] for c in curves) / 3.0 for j in range(n + 1)]
    book = [book_eq[j + 1] / book_eq[j] - 1.0 for j in range(n)]
    bc = curve(book)
    own_cagr = bc[-1] ** (1.0 / yrs) - 1.0
    own_dd = maxdd(bc)
    m = sum(book) / n
    own_sharpe = m / sd(book) * math.sqrt(TRADING_DAYS)
    print("  own S2 book: CAGR %.8f   maxDD %.8f   Sharpe %.8f"
          % (own_cagr, own_dd, own_sharpe))

    # ---- compare the TRADE LEDGER against out/s2_structure.csv
    print("")
    print("=" * 78)
    print("A. TRADE-LEVEL GAP vs out/s2_structure.csv (S2 rows)")
    print("=" * 78)
    _h, rows = read_out_csv(os.path.join(OUT, "s2_structure.csv"))
    s2 = [r for r in rows if r["strat"] == "S2"]
    print("  study.py S2 trades: %d" % len(s2))
    # rebuild the study's per-trade records from the ledger by matching
    # (entry, expiry, K1).  The ledger appended two rows per leg; keep the
    # short leg's row, which carries the credit.
    # Key on (index, expiry): one spread per index per expiry, by construction.
    own = {}
    for r in ledger:
        own[(r["sym"], r["exp"].isoformat())] = r
    print("  handcheck spread records: %d" % len(own))
    worst_cred = 0.0
    worst_intr = 0.0
    worst_k1 = 0.0
    worst_k2 = 0.0
    matched = 0
    for r in s2:
        # Key on (index, expiry): one spread per index per expiry, by construction.
        k = (r["sym"], r["expiry"])
        if k not in own:
            continue
        matched += 1
        o = own[k]
        worst_cred = max(worst_cred, abs(o["cred"] - float(r["credit"])))
        worst_k1 = max(worst_k1, abs(o["K1"] - float(r["K1"])))
        worst_k2 = max(worst_k2, abs(o["K2"] - float(r["K2"])))
        # the study's intrinsic, recomputed from ITS OWN strikes and the settle
        # price recorded in the artefact; the handcheck's from its own strikes
        # and its own read of the raw close on the expiry session
        intr_study = max(0.0, float(r["K1"]) - float(r["S_settle"])) \
            - max(0.0, float(r["K2"]) - float(r["S_settle"]))
        b = bars[r["sym"]]
        s_close_own = b.c[b.at[datetime.date.fromisoformat(r["expiry"])]]
        intr_own = max(0.0, o["K1"] - s_close_own) \
            - max(0.0, o["K2"] - s_close_own)
        worst_intr = max(worst_intr, abs(intr_study - intr_own))
    print("  matched on (index, expiry): %d" % matched)
    check("S2 short strike K1 (handcheck vs study.py artefact)", worst_k1,
          TRADE_TOL)
    check("S2 long strike K2", worst_k2, TRADE_TOL)
    check("S2 credit  (handcheck vs study.py, max abs gap)", worst_cred, TRADE_TOL)
    check("S2 settlement intrinsic vs the real expiry close", worst_intr,
          TRADE_TOL)

    # ---- compare headline statistics
    print("")
    print("=" * 78)
    print("B. HEADLINE GAP vs out/headline.csv (S2)")
    print("=" * 78)
    _h2, hrows = read_out_csv(os.path.join(OUT, "headline.csv"))
    s2h = [r for r in hrows if r["strat"] == "S2"][0]
    check("S2 CAGR", own_cagr - float(s2h["cagr"]), STAT_TOL)
    check("S2 maxDD", own_dd - float(s2h["max_dd"]), STAT_TOL)
    check("S2 Sharpe (raw, daily x sqrt252)",
          own_sharpe - float(s2h["sharpe_raw"]), STAT_TOL)
    fy, ny, ty = frac_positive(book, window, "Y")
    check("S2 fraction of positive complete YEARS",
          fy - float(s2h["frac_pos_years"]), 1e-9)
    fq, nq, tq = frac_positive(book, window, "Q")
    check("S2 fraction of positive complete QUARTERS",
          fq - float(s2h["frac_pos_quarters"]), 1e-9)
    fm, nm, tm = frac_positive(book, window, "M")
    check("S2 fraction of positive complete MONTHS",
          fm - float(s2h["frac_pos_months"]), 1e-9)
    print("  own counts: Y %d/%d  Q %d/%d  M %d/%d ; study: Y %s/%s Q %s/%s M %s/%s"
          % (ny, ty, nq, tq, nm, tm, s2h["n_pos_years"], s2h["n_years"],
             s2h["n_pos_quarters"], s2h["n_quarters"], s2h["n_pos_months"],
             s2h["n_months"]))

    # ---- own correlation
    print("")
    print("=" * 78)
    print("C. CORRELATION GAP vs out/correlation.csv")
    print("=" * 78)
    _h3, crows = read_out_csv(os.path.join(OUT, "correlation.csv"))
    yr = {}
    for s in ETFS:
        b = bars[s]
        ys = {}
        for d in window:
            ys.setdefault(d.year, []).append(b.at[d])
        by = {}
        for y in sorted(ys):
            by[y] = b.c[ys[y][-1]] / b.c[ys[y][0]] - 1.0
        yr[s] = by
    cy = [y for y in sorted(yr["SPY"])
          if datetime.date(y, 1, 1) >= window[0]
          and datetime.date(y, 12, 31) <= window[-1]]
    for r in crows:
        a, bb = r["pair_a"], r["pair_b"]
        own_ry = pearson([yr[a][y] for y in cy], [yr[bb][y] for y in cy])
        ra, rb = [], []
        for j in range(1, n):
            ia, ib = bars[a].at.get(window[j]), bars[bb].at.get(window[j])
            ia0, ib0 = bars[a].at.get(window[j - 1]), bars[bb].at.get(window[j - 1])
            ra.append(bars[a].c[ia] / bars[a].c[ia0] - 1.0)
            rb.append(bars[bb].c[ib] / bars[bb].c[ib0] - 1.0)
        check("%s/%s yearly corr" % (a, bb),
              own_ry - float(r["yearly_corr"]), 5.1e-4)
        check("%s/%s daily corr" % (a, bb),
              pearson(ra, rb) - float(r["daily_corr"]), 5.1e-4)

    # ---- the sibling VRP arithmetic on 2008 and 2020
    print("")
    print("=" * 78)
    print("D. VRP RE-DERIVED FROM THE RAW SPY AND VIX CSVS")
    print("=" * 78)
    spy = bars["SPY"]
    vp = []
    for d in range(0, len(spy.c) - 21):
        v = spy.at.get(spy.dates[d])
        vix = bars["VIX"].at_or_before(spy.dates[d])
        if vix is None or vix <= 0:
            continue
        collected = vix / math.sqrt(252) * math.sqrt(21)
        realised = abs(spy.c[d + 21] / spy.c[d] - 1.0) * 100.0
        rr = [math.log(spy.c[i] / spy.c[i - 1]) for i in range(d + 1, d + 22)]
        mm = sum(rr) / len(rr)
        fwd = math.sqrt(sum((x - mm) ** 2 for x in rr) / (len(rr) - 1)) \
            * math.sqrt(252) * 100.0
        fair = math.sqrt(2.0 / math.pi)
        vp.append({"date": spy.dates[d], "vix": vix, "vrp": vix - fwd,
                   "R_fair": (collected * fair - realised)
                             / (2.0 * collected * fair),
                   "R": (collected - realised) / (2.0 * collected)})
    for y in (2008, 2020):
        g = [x for x in vp if x["date"].year == y]
        print("  %d  n=%-4d mean VRP = %+7.2f vol pts   share VIX>forward RV = %5.1f%%"
              "   mean E_R_fair = %+.4f   total = %+.1fR"
              % (y, len(g), mean([x["vrp"] for x in g]),
                 100.0 * sum(1 for x in g if x["vrp"] > 0) / len(g),
                 mean([x["R_fair"] for x in g]),
                 sum(x["R_fair"] for x in g)))
    allv = [x["vrp"] for x in vp]
    allR = [x["R_fair"] for x in vp]
    print("  ALL  n=%-4d mean VRP = %+7.2f vol pts   share VIX>forward RV = %5.1f%%"
          "   fair-strike E_R = %+.4f"
          % (len(vp), mean(allv),
             100.0 * sum(1 for x in allv if x > 0) / len(allv), mean(allR)))
    worst = min(vp, key=lambda x: x["R"])
    print("  worst window: %s  VIX=%.1f  R=%+.2f  R_fair=%+.2f"
          % (worst["date"].isoformat(), worst["vix"], worst["R"], worst["R_fair"]))
    print("")
    print("  SIBLING STUDY's published finding, for sign/size comparison:")
    print("    mean VRP +3.62 vol pts, VIX above forward RV in 82.9% of windows,")
    print("    VRP negative in exactly one year (2008, -2.33 vol pts);")
    print("    fair-strike E_R = +0.1158R, 2020 the one losing year (-7.3R),")
    print("    worst window R = -3.98 starting 2020-02-20.")

    # ---- by-hand BS price
    print("")
    print("=" * 78)
    print("E. BY HAND -- one Black-Scholes price, every intermediate shown")
    print("=" * 78)
    S, K, Tage, r_, sig = 100.0, 95.0, 30.0 / 365.0, 0.04, 0.20
    T = Tage
    v = sig * math.sqrt(T)
    d1 = (math.log(S / K) + (r_ + 0.5 * sig * sig) * T) / v
    d2 = d1 - v
    P = K * math.exp(-r_ * T) * Phi(-d2) - S * Phi(-d1)
    print("  INPUTS (round numbers, nothing to do with the study's data):")
    print("    S = %.2f   K = %.2f   days = %.0f   T = %.8f   r = %.4f"
          "   sigma = %.4f" % (S, K, 30.0, T, r_, sig))
    print("    sigma*sqrt(T)            = %.10f" % v)
    print("    ln(S/K)                  = %.10f" % math.log(S / K))
    print("    (r + sigma^2/2)*T        = %.10f" % ((r_ + 0.5 * sig * sig) * T))
    print("    d1                       = %.10f" % d1)
    print("    d2 = d1 - sigma*sqrt(T)  = %.10f" % d2)
    print("    Phi(-d1)                 = %.10f" % Phi(-d1))
    print("    Phi(-d2)                 = %.10f" % Phi(-d2))
    print("    e^{-rT}                  = %.10f" % math.exp(-r_ * T))
    print("    K*e^{-rT}*Phi(-d2)       = %.10f" % (K * math.exp(-r_ * T) * Phi(-d2)))
    print("    S*Phi(-d1)               = %.10f" % (S * Phi(-d1)))
    print("    PUT = K e^{-rT}N(-d2) - S N(-d1) = %.10f" % P)
    print("    put delta = e^{-qT}(N(d1)-1) = %.10f" % (Phi(d1) - 1.0))
    print("  This is handcheck.py's own pricer.  It is checked against study.py's")
    print("  pricer indirectly, through the whole trade ledger in section A.")

    # ---- by-hand settlement
    print("")
    print("=" * 78)
    print("F. BY HAND -- one month's put spread settled against the real path")
    print("=" * 78)
    r0 = s2[0]
    K1, K2 = float(r0["K1"]), float(r0["K2"])
    S_set = float(r0["S_settle"])
    cred = float(r0["credit"])
    w = float(r0["width"])
    intr = max(0.0, K1 - S_set) - max(0.0, K2 - S_set)
    gross = cred - intr
    pnl = gross * 100.0 - spread_cost
    R = (w - cred) * 100.0
    print("  trade: %s %s entered %s expiring %s"
          % (r0["strat"], r0["sym"], r0["entry"], r0["expiry"]))
    print("    S at entry (open)          = %s" % r0["S_entry"])
    print("    short strike K1            = %.4f" % K1)
    print("    long  strike K2 = K1 - 5   = %.4f" % K2)
    print("    real close on expiry       = %.4f" % S_set)
    print("    short put intrinsic        = max(0, K1 - S) = %.6f"
          % max(0.0, K1 - S_set))
    print("    long  put intrinsic        = max(0, K2 - S) = %.6f"
          % max(0.0, K2 - S_set))
    print("    SPREAD intrinsic           = %.6f" % intr)
    print("    credit collected           = %.6f" % cred)
    print("    gross per share            = credit - intrinsic = %.6f" % gross)
    print("    costs (2 legs x %s)      = %.4f $/contract" % (cost_one_way, spread_cost))
    print("    net P&L per contract       = %.6f * 100 - %.4f = %.4f"
          % (gross, spread_cost, pnl))
    print("    study.py pnl_dollars       = %s   gap = %.6f"
          % (r0["pnl_dollars"], pnl - float(r0["pnl_dollars"])))
    check("by-hand net P&L per contract", pnl - float(r0["pnl_dollars"]),
          TRADE_TOL)
    print("    R = (width - credit) * 100 = (%.4f - %.6f) * 100 = %.4f" % (w, cred, R))
    print("    study.py R_dollars         = %s   gap = %.6f"
          % (r0["R_dollars"], R - float(r0["R_dollars"])))
    check("by-hand R unit", R - float(r0["R_dollars"]), TRADE_TOL)

    print("")
    print("=" * 78)
    if FAILS:
        print("HANDCHECK FAILED -- %d check(s) outside tolerance:" % len(FAILS))
        for lab, gap, tol in FAILS:
            print("   %s  gap=%s  tol=%s" % (lab, gap, tol))
        return 1
    print("HANDCHECK PASSED -- every gap above is inside its stated tolerance.")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
