#!/usr/bin/env python3
"""
generate_synthetic.py -- build examples/logs/illustrative-year-synthetic.csv

WHAT THIS IS
    A seeded, deterministic generator for a SYNTHETIC trade log. Nothing in the
    output is market data. There is no instrument, no exchange, no backtest and
    no result here. The log exists so that the timeframe-performance-statistics
    engine can be demonstrated on a series with realistic STRUCTURE:

      * positive expectancy, but a GENUINELY MARGINAL one -- the pooled win rate
        sits only a few percentage points above its own break-even win rate, so
        the demonstration shows a book you cannot yet prove an edge on;
      * CLUSTERED losses -- a two-state regime chain, plus one forced risk-off
        window, so the cumulative P&L series has a real drawdown and
        non-trivial period autocorrelation instead of being white noise;
      * multiple symbols, so the log is not one instrument wearing four names;
      * a mix of holding periods, so the review-cadence question is live.

HOW TO REPRODUCE
    py -3 examples/logs/generate_synthetic.py
    # writes examples/logs/illustrative-year-synthetic.csv
    # identical bytes on every run, on every platform, with any Python 3

    Seeds and constants are all named below. Changing any of them changes the
    log -- which is fine, but then every number quoted in the docs is stale, so
    re-run the engine and re-paste its output.

Stdlib only. No network. No third-party imports.
"""

import os
import random
from datetime import date, timedelta

# --- named, so a reader can change them and see what moves -------------------
SEED = 20260414            # fixed: the log is reproducible byte for byte
N_TRADES = 120             # the demo is a 120-trade book
START = date(2025, 1, 6)   # first possible open date
END = date(2026, 3, 6)     # last possible close date  (~14 months)
SYMBOLS = ["SYN-A", "SYN-B", "SYN-C", "SYN-D"]

# --- regime model -----------------------------------------------------------
P_STAY_GOOD = 0.90         # persistence of the calm regime
P_STAY_BAD = 0.75          # persistence of the risk-off regime (bad spells cluster)
P_WIN_GOOD = 0.70
P_WIN_BAD = 0.48
WIN_R_GOOD = (0.80, 1.45)
WIN_R_BAD = (0.70, 1.20)
LOSS_R_GOOD = (0.60, 1.05)
LOSS_R_BAD = (0.90, 1.50)

# one deliberately forced risk-off window, so a drawdown exists in a known place
STRESS_FROM = date(2025, 9, 15)
STRESS_TO = date(2025, 10, 31)
P_WIN_STRESS = 0.34
LOSS_R_STRESS = (1.00, 1.60)

# a small tail: outsized losses (the thing every small-sample statistic hates)
P_TAIL = 0.03
P_TAIL_STRESS = 0.06
TAIL_R = (1.80, 2.40)

# risk unit in currency, so R-multiples are derivable
RISK_MIN = 90
RISK_MAX = 130
RISK_STEP = 5

HOLD_MIN = 2               # calendar days
HOLD_MAX = 21              # calendar days -- mean lands near two weeks

OUT_NAME = "illustrative-year-synthetic.csv"


def week_start(d):
    """Monday on or before d -- the ISO week this date belongs to."""
    return d - timedelta(days=d.isoweekday() - 1)


def build_regime_chain(rng, weeks):
    """Two-state Markov chain, one state per ISO week, with a forced risk-off window."""
    chain = []
    state = "good"
    for wk_start in weeks:
        if state == "good":
            state = "good" if rng.random() < P_STAY_GOOD else "bad"
        else:
            state = "bad" if rng.random() < P_STAY_BAD else "good"
        s = state
        if STRESS_FROM <= wk_start <= STRESS_TO:
            s = "stress"
        chain.append((wk_start, s))
    return dict(chain)


def regime_for(week_map, d):
    """The ISO-week Monday of `d`, used as the key into the per-week regime chain."""
    return week_map.get(week_start(d), "good")


def build_close_dates(rng):
    """120 close dates spread across ~14 months, weekday-only, irregular gaps."""
    dates = []
    cur = week_start(START + timedelta(days=14))
    while len(dates) < N_TRADES and cur <= END:
        if cur.isoweekday() <= 5:
            dates.append(cur)
        gap = rng.choice([1, 1, 2, 2, 3, 3, 4, 5])
        cur = cur + timedelta(days=gap)
        while cur.isoweekday() > 5:
            cur = cur + timedelta(days=1)
    return dates[:N_TRADES]


def draw_hold(rng):
    return rng.randint(HOLD_MIN, HOLD_MAX)


def draw_risk(rng):
    steps = (RISK_MAX - RISK_MIN) // RISK_STEP
    return RISK_MIN + RISK_STEP * rng.randint(0, steps)


def draw_r_multiple(rng, regime):
    tail_p = P_TAIL_STRESS if regime == "stress" else P_TAIL
    if rng.random() < tail_p:
        lo, hi = TAIL_R
        return -rng.uniform(lo, hi)
    if regime == "stress":
        if rng.random() < P_WIN_STRESS:
            lo, hi = WIN_R_BAD
            return rng.uniform(lo, hi)
        lo, hi = LOSS_R_STRESS
        return -rng.uniform(lo, hi)
    if regime == "good":
        if rng.random() < P_WIN_GOOD:
            lo, hi = WIN_R_GOOD
            return rng.uniform(lo, hi)
        lo, hi = LOSS_R_GOOD
        return -rng.uniform(lo, hi)
    if rng.random() < P_WIN_BAD:
        lo, hi = WIN_R_BAD
        return rng.uniform(lo, hi)
    lo, hi = LOSS_R_BAD
    return -rng.uniform(lo, hi)


def header_comments(rows):
    """Data-derived, so the header cannot drift from the file it describes."""
    return [
        "# PROVENANCE: SYNTHETIC / ILLUSTRATIVE -- invented trade log. NOT market data. NOT a backtest. NOT a result. It carries no market information whatsoever and must never be quoted as a finding about any instrument, strategy or period.",
        "# PROVENANCE: generated by examples/logs/generate_synthetic.py at fixed seed SEED=%d, stdlib only, byte-identical on every run." % SEED,
        "# PROVENANCE: %d invented closed trades, close dates %s .. %s (%d calendar days), four invented symbols (%s)."
        % (len(rows), rows[0]["close_date"], rows[-1]["close_date"],
           (date.fromisoformat(rows[-1]["close_date"])
            - date.fromisoformat(rows[0]["close_date"])).days,
           "..".join(SYMBOLS)),
        "# PROVENANCE: designed to be a MARGINAL book -- a pooled win rate only a few points above its break-even win rate -- with CLUSTERED losses (a two-state regime chain plus a forced risk-off window %s..%s) so that drawdown and period autocorrelation are non-trivial."
        % (STRESS_FROM.isoformat(), STRESS_TO.isoformat()),
        "# PROVENANCE: pnl is invented currency in units of an invented risk unit (%d..%d per trade); it is not dollars earned by anyone."
        % (RISK_MIN, RISK_MAX),
        "# Columns: trade_id,open_date,close_date,pnl,risk,symbol",
        "#   pnl  = realised P&L in invented currency for that closed trade (may be negative)",
        "#   risk = the planned per-trade risk unit, so R-multiples can be derived downstream",
        "# Open dates are close_date minus a %d..%d calendar-day holding period, so the"
        % (HOLD_MIN, HOLD_MAX),
        "# average holding period lands near two weeks -- which is what makes the review-",
        "# cadence question ('weekly or monthly?') a live one for this log.",
    ]


def main():
    rng = random.Random(SEED)

    weeks = []
    wk = week_start(START)
    while wk <= END:
        weeks.append(wk)
        wk = wk + timedelta(days=7)
    week_map = build_regime_chain(rng, weeks)

    close_dates = build_close_dates(rng)

    rows = []
    for i, cd in enumerate(close_dates, 1):
        regime = regime_for(week_map, cd)
        hold = draw_hold(rng)
        od = cd - timedelta(days=hold)
        risk = draw_risk(rng)
        r = draw_r_multiple(rng, regime)
        pnl = round(risk * r, 2)
        rows.append({
            "trade_id": "SYN%03d" % i,
            "open_date": od.isoformat(),
            "close_date": cd.isoformat(),
            "pnl": pnl,
            "risk": risk,
            "symbol": SYMBOLS[(i - 1) % len(SYMBOLS)],
            "regime": regime,
        })

    here = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(here, OUT_NAME)
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        for c in header_comments(rows):
            fh.write(c + "\n")
        fh.write("trade_id,open_date,close_date,pnl,risk,symbol\n")
        for r in rows:
            fh.write("%s,%s,%s,%.2f,%d,%s\n" % (
                r["trade_id"], r["open_date"], r["close_date"],
                r["pnl"], r["risk"], r["symbol"]))

    wins = len([r for r in rows if r["pnl"] > 0])
    losses = len([r for r in rows if r["pnl"] < 0])
    flat = len(rows) - wins - losses
    gp = sum(r["pnl"] for r in rows if r["pnl"] > 0)
    gl = -sum(r["pnl"] for r in rows if r["pnl"] < 0)
    net = gp - gl
    holds = [(date.fromisoformat(r["close_date"]) - date.fromisoformat(r["open_date"])).days
             for r in rows]
    by_regime = {}
    for r in rows:
        by_regime.setdefault(r["regime"], []).append(r["pnl"])

    print("wrote %s" % out_path)
    print("  seed            : %d (fixed -- byte-identical reruns)" % SEED)
    print("  trades          : %d" % len(rows))
    print("  close span      : %s .. %s" % (rows[0]["close_date"], rows[-1]["close_date"]))
    print("  wins/losses/flat: %d / %d / %d" % (wins, losses, flat))
    print("  gross profit    : %.2f" % gp)
    print("  gross loss      : %.2f" % gl)
    print("  net             : %.2f" % net)
    print("  win rate (excl. flat): %.6f" % (wins / (wins + losses)))
    avg_win = gp / wins if wins else 0.0
    avg_loss = gl / losses if losses else 0.0
    payoff = avg_win / avg_loss if avg_loss else float("inf")
    be_wr = 1.0 / (1.0 + payoff) if payoff != float("inf") else 0.0
    wr = wins / (wins + losses) if (wins + losses) else 0.0
    se = (wr * (1.0 - wr) / (wins + losses)) ** 0.5 if (wins + losses) else 0.0
    print("  avg win / avg loss: %.2f / %.2f  (payoff %.6f)" % (avg_win, avg_loss, payoff))
    print("  break-even win rate: %.6f" % be_wr)
    print("  edge vs break-even : %.6f  (2 x se_win_rate = %.6f -> %s)"
          % (wr - be_wr, 2 * se, "PASS" if (wr - be_wr) > 2 * se else "FAIL"))
    print("  expectancy/trade   : %.2f" % (net / len(rows)))
    print("  holding period  : min %d / mean %.2f / max %d calendar days"
          % (min(holds), sum(holds) / len(holds), max(holds)))
    for k in sorted(by_regime):
        v = by_regime[k]
        print("  regime %-6s   : %3d trades, net %10.2f" % (k, len(v), sum(v)))
    print("")
    print("REMINDER: this is a synthetic demonstration log. It says nothing about")
    print("any market, instrument, strategy or period. Do not quote it as a finding.")


if __name__ == "__main__":
    main()
