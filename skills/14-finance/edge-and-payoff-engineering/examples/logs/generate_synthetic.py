#!/usr/bin/env python3
"""
generate_synthetic.py -- build examples/logs/illustrative-cohorts-synthetic.csv

WHAT THIS IS
    A seeded, deterministic generator for a SYNTHETIC trade ledger. Nothing in
    the output is market data. There is no instrument, no exchange, no backtest
    and no result here. The file exists so that the edge-and-payoff engine can be
    demonstrated on a ledger whose COHORT STRUCTURE is known by construction:

      SETUP-TREND   clearly positive      -- a payoff above its break-even
      SETUP-FADE    clearly negative      -- a payoff below its break-even
      SETUP-EVENT   marginal, n < 30      -- a gross number thinner than cost
      SETUP-CREDIT  the disposition trap  -- a HIGH win rate and a TERRIBLE
                                             payoff: p ~ 0.62, b ~ 0.50, so
                                             b < (1-p)/p and it loses money
                                             while winning most trades

    That fourth cohort is the whole point of the skill. It is the shape a real
    negative trader's ledger has, and it is a maths error, not bad luck.

    The win/loss COUNTS per setup are fixed exactly (not sampled), so the four
    cohort verdicts are stable across runs: KEEP, KILL, INSUFFICIENT, KILL.

HOW TO REPRODUCE
    py -3 examples/logs/generate_synthetic.py
    # writes examples/logs/illustrative-cohorts-synthetic.csv
    # identical bytes on every run, on every platform, with any Python 3

    Every seed and constant is named below. Changing one changes the log -- which
    is fine, but then every number quoted in the docs is stale, so re-run the
    engine and re-paste its output.

Stdlib only. No network. No third-party imports.
"""

import os
import random
from datetime import date, timedelta

# --- named, so a reader can change them and see what moves -------------------
SEED = 20261014                 # fixed: the ledger is reproducible byte for byte
START = date(2025, 5, 1)        # first possible close date
END = date(2026, 9, 30)         # last possible close date (~17 months)

SYMBOLS = ["SYN-A", "SYN-B", "SYN-C", "SYN-D", "SYN-E"]

# risk unit in currency: a flat-ish $150..$250 so that R is comparable across
# trades and the currency never contaminates the payoff ratio
RISK_MIN = 150
RISK_MAX = 250
RISK_STEP = 10

# round-trip cost in currency: commission + exchange/regulatory fees + half the
# bid-ask spread, per closed trade. Mean lands near $6, i.e. about 0.03R against
# a mean risk of $200 -- small enough to look harmless, large enough to matter.
COST_MIN = 4.00
COST_MAX = 8.00
COST_STEP = 0.25

# SETUPS: (name, n_trades, n_wins, win_R_range, loss_R_range,
#          dte_range, symbol_weights, p_long)
SETUPS = [
    ("SETUP-TREND",  62, 31, (1.45, 1.75), (0.95, 1.10), (20, 60),
     {"SYN-A": 0.30, "SYN-B": 0.25, "SYN-C": 0.20, "SYN-D": 0.15, "SYN-E": 0.10}, 0.70),
    ("SETUP-FADE",   60, 25, (0.85, 1.05), (1.00, 1.15), (5, 30),
     {"SYN-A": 0.10, "SYN-B": 0.15, "SYN-C": 0.25, "SYN-D": 0.30, "SYN-E": 0.20}, 0.40),
    ("SETUP-EVENT",  23, 12, (0.95, 1.10), (1.00, 1.12), (2, 10),
     {"SYN-A": 0.20, "SYN-B": 0.20, "SYN-C": 0.20, "SYN-D": 0.20, "SYN-E": 0.20}, 0.50),
    ("SETUP-CREDIT", 55, 34, (0.35, 0.65), (0.85, 1.15), (25, 70),
     {"SYN-A": 0.25, "SYN-B": 0.20, "SYN-C": 0.15, "SYN-D": 0.20, "SYN-E": 0.20}, 0.35),
]

OUT_NAME = "illustrative-cohorts-synthetic.csv"


def draw_close_dates(rng, n):
    """n weekday close dates spread across START..END with irregular gaps."""
    dates = []
    span = (END - START).days
    cur = START
    while len(dates) < n and cur <= END:
        if cur.isoweekday() <= 5:
            dates.append(cur)
        gap = rng.choice([1, 1, 1, 2, 2, 2, 3, 3])
        cur = cur + timedelta(days=gap)
        while cur.isoweekday() > 5:
            cur = cur + timedelta(days=1)
    if len(dates) < n:
        raise RuntimeError("date window too narrow for %d trades (span %d days)"
                           % (n, span))
    return dates[:n]


def draw_risk(rng):
    steps = (RISK_MAX - RISK_MIN) // RISK_STEP
    return RISK_MIN + RISK_STEP * rng.randint(0, steps)


def draw_cost(rng):
    steps = int(round((COST_MAX - COST_MIN) / COST_STEP))
    return round(COST_MIN + COST_STEP * rng.randint(0, steps), 2)


def draw_symbol(rng, weights):
    names = sorted(weights.keys())
    r = rng.random()
    acc = 0.0
    for name in names:
        acc += weights[name]
        if r < acc:
            return name
    return names[-1]


def build_setup_sequence(rng):
    """Exact win/loss counts per setup, then shuffled so the cohorts interleave."""
    seq = []
    for name, n, wins, _wr, _lr, _dte, _sym, _pl in SETUPS:
        for i in range(n):
            seq.append((name, i < wins))
    rng.shuffle(seq)
    return seq


def build_rows(rng):
    seq = build_setup_sequence(rng)
    n = len(seq)
    close_dates = draw_close_dates(rng, n)
    param = {s[0]: s for s in SETUPS}

    rows = []
    for i, (setup, is_win) in enumerate(seq, 1):
        _name, _n, _w, wr, lr, dte_r, sym_w, p_long = param[setup]
        cd = close_dates[i - 1]
        hold = rng.randint(2, max(3, dte_r[1] - 1))
        od = cd - timedelta(days=hold)
        risk = draw_risk(rng)
        cost = draw_cost(rng)
        lo, hi = wr if is_win else lr
        r = rng.uniform(lo, hi)
        if not is_win:
            r = -r
        pnl = round(risk * r, 2)
        dte = rng.randint(dte_r[0], dte_r[1])
        ivr = rng.randint(5, 95)
        side = "long" if rng.random() < p_long else "short"
        rows.append({
            "trade_id": "SYN%03d" % i,
            "open_date": od.isoformat(),
            "close_date": cd.isoformat(),
            "pnl": pnl,
            "risk": risk,
            "cost": cost,
            "setup": setup,
            "symbol": draw_symbol(rng, sym_w),
            "dte": dte,
            "iv_rank": ivr,
            "side": side,
        })
    rows.sort(key=lambda r: (r["close_date"], r["trade_id"]))
    return rows


def stats(vals):
    """p, avg win, avg loss, b, E and b* for a list of R-multiples."""
    n = len(vals)
    wins = [v for v in vals if v > 0]
    losses = [-v for v in vals if v < 0]
    p = (len(wins) / (len(wins) + len(losses))) if (wins or losses) else 0.0
    aw = (sum(wins) / len(wins)) if wins else 0.0
    al = (sum(losses) / len(losses)) if losses else 0.0
    b = (aw / al) if al else float("inf")
    E = sum(vals) / n if n else 0.0
    b_star = ((1.0 - p) / p) if p > 0 else float("inf")
    return n, p, aw, al, b, E, b_star


def aggregate(rows):
    """Per-setup and pooled aggregates, computed from the rows actually written."""
    by_setup = {}
    for r in rows:
        by_setup.setdefault(r["setup"], []).append(r["pnl"] / r["risk"])

    mean_cost = sum(r["cost"] for r in rows) / len(rows)
    mean_risk = sum(r["risk"] for r in rows) / len(rows)
    c_R = mean_cost / mean_risk
    pooled = stats([r["pnl"] / r["risk"] for r in rows])
    return by_setup, pooled, mean_cost, mean_risk, c_R


def header_comments(rows):
    """Data-derived, so the header cannot drift from the file it describes."""
    return [
        "# PROVENANCE: SYNTHETIC / ILLUSTRATIVE -- invented trade ledger. NOT market data. NOT a backtest. NOT a result. It carries no market information whatsoever and must never be quoted as a finding about any instrument, strategy or period.",
        "# PROVENANCE: generated by examples/logs/generate_synthetic.py at fixed seed SEED=%d, stdlib only, byte-identical on every run." % SEED,
        "# PROVENANCE: %d invented closed trades, close dates %s .. %s, five invented symbols, four invented setup tags."
        % (len(rows), rows[0]["close_date"], rows[-1]["close_date"]),
        "# PROVENANCE: pnl is invented currency in units of an invented risk unit ($%d..$%d per trade); it is not dollars earned by anyone."
        % (RISK_MIN, RISK_MAX),
        "# PROVENANCE: `cost` is an invented per-trade round-trip cost ($%.2f..$%.2f), so cost drag is non-zero and E_net differs from E."
        % (COST_MIN, COST_MAX),
        "# PROVENANCE: the four setups are constructed, not discovered -- one positive, one negative, one marginal with n<30, and one deliberate DISPOSITION-EFFECT TRAP (high win rate, payoff below (1-p)/p).",
        "# Columns: trade_id,open_date,close_date,pnl,risk,cost,setup,symbol,dte,iv_rank,side",
        "#   setup   = the cohort tag. This is the field that makes cohort attribution possible.",
        "#   risk    = the planned per-trade risk in currency, so R-multiples are derivable.",
        "#   cost    = commission + fees + half-spread for that closed trade.",
        "#   dte     = days to expiration at entry (invented, but plausibly shaped per setup).",
        "#   iv_rank = 0-100, invented.",
    ]


def main():
    rng = random.Random(SEED)
    rows = build_rows(rng)
    by_setup, pooled, mean_cost, mean_risk, c_R = aggregate(rows)

    here = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(here, OUT_NAME)
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        for c in header_comments(rows):
            fh.write(c + "\n")
        fh.write("trade_id,open_date,close_date,pnl,risk,cost,setup,symbol,dte,iv_rank,side\n")
        for r in rows:
            fh.write("%s,%s,%s,%.2f,%d,%.2f,%s,%s,%d,%d,%s\n" % (
                r["trade_id"], r["open_date"], r["close_date"], r["pnl"],
                r["risk"], r["cost"], r["setup"], r["symbol"], r["dte"],
                r["iv_rank"], r["side"]))

    print("wrote %s" % out_path)
    print("  seed             : %d (fixed -- byte-identical reruns)" % SEED)
    print("  trades           : %d" % len(rows))
    print("  close span       : %s .. %s" % (rows[0]["close_date"], rows[-1]["close_date"]))
    print("  mean risk        : %.2f currency (1R)" % mean_risk)
    print("  mean cost/trade  : %.2f currency" % mean_cost)
    print("  cost drag c_R    : %.6f R" % c_R)
    print("")
    print("  setup          n     p        avg_win  avg_loss  b        b*       E        E_net")
    for name in sorted(by_setup):
        n, p, aw, al, b, E, bs = stats(by_setup[name])
        print("  %-13s %3d   %-8.4f %-8.4f %-9.4f %-8.4f %-8.4f %-8.4f %-8.4f"
              % (name, n, p, aw, al, b, bs, E, E - c_R))
    n, p, aw, al, b, E, bs = pooled
    print("  %-13s %3d   %-8.4f %-8.4f %-9.4f %-8.4f %-8.4f %-8.4f %-8.4f"
          % ("POOLED", n, p, aw, al, b, bs, E, E - c_R))
    print("")
    print("  Reminder: every setup above is CONSTRUCTED. This file proves the engine")
    print("  works; it proves nothing whatsoever about any market or strategy.")


if __name__ == "__main__":
    main()
