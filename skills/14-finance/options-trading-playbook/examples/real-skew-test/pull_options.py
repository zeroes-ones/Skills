#!/usr/bin/env python3
"""pull_options.py -- retrieval half of the real-skew-test study.

WHAT THIS SCRIPT DOES, AND WHAT IT CANNOT DO
--------------------------------------------
The real option prices come from the Robinhood MCP tools
(`get_option_instruments`, `get_option_historicals`, `get_option_quotes`).
Those tools are exposed to the *agent*, not to a Python process, so this
script cannot itself issue them.  It therefore works in two modes:

  --plan     Declare the sample and emit the exact MCP call list to execute
             (logs/call-plan.tsv).  Run BEFORE any call is made: the sample is
             fixed in advance, not chosen after seeing prices.
  --ingest   Turn the raw MCP call transcripts saved under logs/ into the
             provenance-tagged CSV the study reads.  Deterministic given the
             transcripts.

Every MCP call actually issued is logged in logs/mcp-call-log.tsv with its
kind and outcome, so the total call count is auditable against call-plan.tsv.

WHAT PASS ONE PROVED AND THIS RUNS ON
-------------------------------------
`../real-quotes-test` established, with real calls:
  * the working path is get_option_chains -> get_option_instruments ->
    get_option_historicals, and `state="expired"` reaches expired contracts;
  * `expiration_dates` must be a SINGLE date (a comma-separated list is empty);
  * the `strike_price` filter is FLAKY -- a query for a contract that provably
    exists returns empty ~45% of the time on the first attempt, so every
    resolution is retried and the attempt count is recorded.  A single empty
    result is NOT evidence of absence;
  * the strike grid is NOT uniformly $1 (it steps by $2.50 in some ranges), so
    the actual strike used is recorded and substitutions are flagged;
  * expired SPY history starts ~2017-09-15; 2008 is UNREACHABLE and the model
    is never substituted for it;
  * the dominant data-quality threat is that bars are LAST-TRADE PRINTS, not
    marks: $0.01-$0.04 prints produced absurd IVs and drove the tails.

Stdlib only.  Deterministic.  UTF-8, LF.
"""

import argparse
import csv
import datetime as dt
import hashlib
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")
RAW = os.path.join(DATA, "raw")
LOGS = os.path.join(ROOT, "logs")
UND = os.path.join(DATA, "underlying")

# ---------------------------------------------------------------------------
# Provenance
# ---------------------------------------------------------------------------
# The UTC date on which every MCP call in this study was issued.
PULL_DATE = "2026-10-15"
SOURCE = ("Robinhood MCP get_option_historicals (real option OHLC, regular "
          "session)")

# ---------------------------------------------------------------------------
# THE SAMPLE -- DECLARED BEFORE THE FIRST PRICE WAS PULLED.
#
# History depth, established by pass one and re-probed here: SPY expired
# expiries resolve from 2017-09-15 onward; 2017-08-18 and everything earlier
# returns an EMPTY instrument list.  2008 and every pre-2017 crisis are OUT OF
# REACH; the model is never substituted for them.
# ---------------------------------------------------------------------------

# One sample date per half-year period from the earliest workable depth, plus
# two declared STRESS dates inside the COVID window (Feb-Apr 2020).  2020-03-02
# is pass one's own stress date, kept so the two studies share a panel; it is
# also inside the COVID window.
SAMPLE_DATES = [
    ("2017-10-02", "H2-2017 calm"),
    ("2018-04-02", "H1-2018 volmageddon aftermath"),
    ("2018-10-01", "H2-2018 pre-Q4 selloff"),
    ("2019-04-01", "H1-2019 calm"),
    ("2019-10-01", "H2-2019 calm"),
    ("2020-02-24", "STRESS: COVID selloff onset"),
    ("2020-03-02", "STRESS: COVID crash"),
    ("2020-04-01", "STRESS: COVID window"),
    ("2020-10-01", "H2-2020 recovery"),
    ("2021-04-01", "H1-2021 calm"),
    ("2021-10-01", "H2-2021 calm"),
    ("2022-04-01", "STRESS: 2022 drawdown"),
    ("2022-10-03", "STRESS: 2022 drawdown trough"),
    ("2023-04-03", "H1-2023"),
    ("2023-10-02", "H2-2023 rate shock"),
    ("2024-04-01", "H1-2024"),
    ("2024-10-01", "H2-2024"),
    ("2025-04-01", "H1-2025"),
    ("2025-10-01", "H2-2025"),
    ("2026-04-01", "H1-2026"),
]

# Underlying.  SPY carries the full declared grid.  QQQ was declared as a
# SECONDARY, to be pulled only if the call budget allowed.  It was NOT pulled,
# and the reduction is reported rather than hidden: the flaky strike filter cost
# ~1.35 resolution calls per contract on SPY (161 calls for 120 contracts, plus
# 6 wasted on the Good Friday expiry), and every remaining call was spent
# completing SPY's 20 dates -- which is what the headline n depends on.  QQQ
# therefore contributes nothing to this study, and no QQQ row exists in the CSV.
UNDERLYINGS = ["SPY"]
DEFERRED_UNDERLYINGS = ["QQQ"]

# Strike ladder, as a fraction of the sample date's underlying close.
# 4 puts + 2 calls = 6 contracts per date, as declared.
LADDER_PUTS = [0.03, 0.06, 0.10, 0.15]
LADDER_CALLS = [0.03, 0.06]

# Tenor: the Friday expiry closest to the CENTRE of the brief's 30-45 DTE band,
# i.e. 37.5 DTE.  Ties resolve to the LATER expiry (deterministic).
TARGET_DTE = 37.5
EXPIRY_BAND_DTE = (30, 45)

# EXPIRY OVERRIDE -- declared ONCE, during the pull, and reported rather than
# hidden.  2020-03-02 + 39 calendar days = 2020-04-10, which is GOOD FRIDAY:
# the US equity market was closed that day, so the expiry does not exist and
# all six resolution calls for it returned an empty instrument list.  The
# in-band substitute that was actually listed is 2020-04-09 (38 DTE, Thursday).
# That expiry resolved but carried NO print for five of the six declared
# strikes, so the ladder was re-declared onto 2020-04-17 (46 DTE, Friday) --
# the nearest expiry with a full set of prints.  46 DTE is OUTSIDE the 30-45
# band and is flagged in every table that uses it.  The same expiry was used by
# the sibling `real-quotes-test` study for the same date, so the two studies
# share a panel.
EXPIRY_OVERRIDES = {
    ("SPY", "2020-03-02"): "2020-04-17",
}

# EXTRA CONTRACTS -- declared during the pull, reported rather than hidden.
# Two INTRA-MONEY puts for 2020-04-01 were resolved by mistake while hunting
# the 3%- and 6%-OTM CALLS at the same strikes (the vendor returns put and call
# together when `type` is omitted and the response order varies).  They are
# kept, not discarded, because for European options put and call implied vols
# at the same strike and expiry must be EQUAL, so they are a free parity check
# on the whole measurement.  They are excluded from the skew fit (panel
# "parity" is filtered out) and used only in the parity section.
EXTRA_CONTRACTS = [
    ("SPY", "2020-04-01", "2020-05-08", "put", 254, 254, "parity"),
    ("SPY", "2020-04-01", "2020-05-08", "put", 261, 261, "parity"),
]

# --- data-quality constants (declared up front, applied in study.py) --------
# MIN_PRICE: a print below this is at or near the $0.01 minimum tick.  Ten ticks
#   is the smallest print that can be told apart from a stale/nominal last
#   trade; pass one measured $0.01-$0.04 prints implying 7-8% IV, which is not
#   a credible market level.  $0.10 = 10 ticks.
MIN_PRICE = 0.10
# MAX_IV / MIN_IV: hard sanity band on a single implied vol.
MAX_IV = 1.50
MIN_IV = 0.02
# MAX_BAR_LAG_DAYS: a bar whose session is more than this many CALENDAR days
#   before the sample date is too stale to be a mark for that date.  One
#   calendar week is the most that can be defended.
MAX_BAR_LAG_DAYS = 7
# MONOTONICITY_SLACK_VOLPTS: within one ladder, IV is expected to be broadly
#   monotone in moneyness.  A deviation larger than this flags the ladder.
MONOTONICITY_SLACK_VOLPTS = 2.0

# Resolution attempt sequence, stated so the call budget is auditable:
#   ATTEMPTS_EXACT attempts at the exact target strike, then one attempt each at
#   the listed neighbours below (dollars offset).  The first strike that
#   resolves is used; the substitution and the attempt count are recorded.
ATTEMPTS_EXACT = 4
NEIGHBOUR_OFFSETS = [-1.0, 1.0, -2.5, 2.5, -2.0, 2.0, -5.0, 5.0]
ATTEMPTS_NEIGHBOUR = 1

# The re-run's spread geometry, taken from the sibling study (S2):
# short ~16-delta 30-DTE put, $5-wide spread, settled at intrinsic.
SPREAD_WIDTH_DOLLARS = 5.0
S2_SHORT_TARGET_PCT = 0.06     # a ~16-delta 37-DTE put sits near 6% OTM
DTE = 37                       # the sibling's nominal 30-DTE is 27-30 actual


# ---------------------------------------------------------------------------
# Underlying closes
# ---------------------------------------------------------------------------
def read_closes(sym):
    """{iso_date: close} for one underlying, from data/underlying/<SYM>_1d.csv."""
    path = os.path.join(UND, "%s_1d.csv" % sym)
    closes = {}
    with open(path, "r", encoding="utf-8") as fh:
        rows = [ln for ln in fh if not ln.startswith("#")]
    rdr = csv.reader(rows)
    header = next(rdr)
    ci = header.index("close")
    for row in rdr:
        if row:
            closes[row[0]] = float(row[ci])
    return closes


# ---------------------------------------------------------------------------
# Expiry selection
# ---------------------------------------------------------------------------
def fridays(lo_iso, hi_iso):
    """All Fridays in [lo, hi] inclusive."""
    lo = dt.date.fromisoformat(lo_iso)
    hi = dt.date.fromisoformat(hi_iso)
    d = lo + dt.timedelta(days=(4 - lo.weekday()) % 7)
    out = []
    while d <= hi:
        out.append(d)
        d += dt.timedelta(days=7)
    return out


def pick_expiry(sample_iso):
    """(expiry_iso, dte) -- the Friday whose DTE is closest to TARGET_DTE.

    Deterministic; ties resolve to the LATER expiry.
    """
    lo = (dt.date.fromisoformat(sample_iso)
          + dt.timedelta(days=EXPIRY_BAND_DTE[0])).isoformat()
    hi = (dt.date.fromisoformat(sample_iso)
          + dt.timedelta(days=EXPIRY_BAND_DTE[1])).isoformat()
    best = None
    for fri in fridays(lo, hi):
        dte = (fri - dt.date.fromisoformat(sample_iso)).days
        key = (abs(dte - TARGET_DTE), -dte)
        if best is None or key < best[0]:
            best = (key, fri.isoformat(), dte)
    return best[1], best[2]


def ladder_for(spot):
    """[(type, target_pct, target_strike)] for one sample date."""
    out = []
    for pct in LADDER_PUTS:
        out.append(("put", pct, int(round(spot * (1.0 - pct)))))
    for pct in LADDER_CALLS:
        out.append(("call", pct, int(round(spot * (1.0 + pct)))))
    return out


def key_of(underlying, sample_date, expiry, kind, target_strike):
    return "%s_%s_%s_%s_%d" % (underlying, sample_date, expiry, kind,
                               target_strike)


def build_plan(underlyings=None):
    """The complete declared sample: one row per contract to resolve."""
    if underlyings is None:
        underlyings = UNDERLYINGS
    rows = []
    for sym in underlyings:
        closes = read_closes(sym)
        for date_iso, note in SAMPLE_DATES:
            spot = closes.get(date_iso)
            if spot is None:
                raise SystemExit("no close for %s %s" % (sym, date_iso))
            expiry, dte = pick_expiry(date_iso)
            expiry = EXPIRY_OVERRIDES.get((sym, date_iso), expiry)
            dte = (dt.date.fromisoformat(expiry)
                   - dt.date.fromisoformat(date_iso)).days
            for kind, pct, strike in ladder_for(spot):
                rows.append({
                    "underlying": sym,
                    "sample_date": date_iso,
                    "note": note,
                    "spot_close": spot,
                    "expiry": expiry,
                    "dte": dte,
                    "type": kind,
                    "target_pct": pct,
                    "target_strike": strike,
                    "moneyness_target": ((strike - spot) / spot),
                    "panel": "ladder",
                    "key": key_of(sym, date_iso, expiry, kind, strike),
                })
    for sym, date_iso, expiry, kind, target, listed, panel in EXTRA_CONTRACTS:
        closes = read_closes(sym)
        spot = closes[date_iso]
        dte = (dt.date.fromisoformat(expiry)
               - dt.date.fromisoformat(date_iso)).days
        rows.append({
            "underlying": sym,
            "sample_date": date_iso,
            "note": "parity check (ITM put at a call strike)",
            "spot_close": spot,
            "expiry": expiry,
            "dte": dte,
            "type": kind,
            "target_pct": float("nan"),
            "target_strike": target,
            "moneyness_target": ((listed - spot) / spot),
            "panel": panel,
            "key": "%s_%s_%s_%s_%dx" % (sym, date_iso, expiry, kind, target),
        })
    return rows


def mcp_args(row):
    return {
        "chain_symbol": row["underlying"],
        "expiration_dates": row["expiry"],
        "type": row["type"],
        "strike_price": "%.4f" % row["target_strike"],
        "state": "expired",
    }


# ---------------------------------------------------------------------------
# Modes
# ---------------------------------------------------------------------------
def write_plan():
    plan = build_plan()
    os.makedirs(LOGS, exist_ok=True)
    path = os.path.join(LOGS, "call-plan.tsv")
    cols = ["n", "panel", "underlying", "sample_date", "note", "spot_close",
            "expiry", "dte", "type", "target_pct", "target_strike",
            "moneyness_target", "mcp_tool", "mcp_chain_symbol",
            "mcp_expiration_dates", "mcp_type", "mcp_strike_price", "mcp_state",
            "key"]
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(cols)
        for i, row in enumerate(plan, 1):
            a = mcp_args(row)
            w.writerow([i, row["panel"], row["underlying"], row["sample_date"],
                        row["note"], "%.2f" % row["spot_close"], row["expiry"],
                        row["dte"], row["type"],
                        ("%.2f" % row["target_pct"]
                         if row["target_pct"] == row["target_pct"] else ""),
                        row["target_strike"],
                        "%.6f" % row["moneyness_target"],
                        "get_option_instruments", a["chain_symbol"],
                        a["expiration_dates"], "", a["strike_price"],
                        a["state"], row["key"]])
    print("wrote %s (%d contracts to resolve)" % (path, len(plan)))
    for panel in ("ladder", "parity"):
        n = sum(1 for r in plan if r["panel"] == panel)
        if n:
            print("  panel %-7s: %d contracts" % (panel, n))
    dates = sorted(set(r["sample_date"] for r in plan))
    print("  dates: %d" % len(dates))
    print("  --- expiry grid (sample_date -> expiry, DTE) ---")
    for d in dates:
        e = sorted(set((r["expiry"], r["dte"]) for r in plan
                       if r["sample_date"] == d))
        print("  %s -> %s" % (d, "  ".join("%s (%d DTE)" % x for x in e)))
    return plan


def read_tsv(name):
    path = os.path.join(LOGS, name)
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as fh:
        rdr = csv.reader(fh, delimiter="\t")
        header = next(rdr, None)
        if header is None:
            return []
        return [dict(zip(header, r)) for r in rdr if r]


def ingest():
    """logs/*.tsv -> data/real_quotes_skew.csv (provenance-tagged)."""
    plan = build_plan()
    ids = {r["key"]: r for r in read_tsv("instrument-ids.tsv")}
    bars = {r["key"]: r for r in read_tsv("bar-log.tsv")}

    rows = []
    funnel = {"declared": len(plan), "resolved": 0, "bar": 0}
    unresolved = []
    for row in plan:
        key = row["key"]
        ins = ids.get(key)
        bar = bars.get(key)
        inst_id = ins["instrument_id"] if ins else ""
        strike_used = (float(ins["strike_used"])
                       if ins and ins.get("strike_used")
                       else float(row["target_strike"]))
        if inst_id:
            funnel["resolved"] += 1
        else:
            unresolved.append((key, "instrument not resolved after %s attempts"
                               % (ins["attempts"] if ins else "0")))
        if bar and bar.get("close"):
            funnel["bar"] += 1
        elif inst_id:
            unresolved.append((key, "resolved but no NON-interpolated bar at "
                                    "or before the sample date"))
        rows.append({
            "underlying": row["underlying"],
            "sample_date": row["sample_date"],
            "note": row["note"],
            "spot_close": row["spot_close"],
            "expiry": row["expiry"],
            "dte": row["dte"],
            "type": row["type"],
            "panel": row["panel"],
            "target_strike": row["target_strike"],
            "strike": strike_used,
            "moneyness": (strike_used - row["spot_close"]) / row["spot_close"],
            "instrument_id": inst_id,
            "occ_symbol": ins.get("occ_symbol", "") if ins else "",
            "resolution_attempts": ins.get("attempts", "0") if ins else "0",
            "substituted": (ins.get("substituted", "no") if ins else "no"),
            "bar_date": bar.get("bar_date", "") if bar else "",
            "open": bar.get("open", "") if bar else "",
            "high": bar.get("high", "") if bar else "",
            "low": bar.get("low", "") if bar else "",
            "close": bar.get("close", "") if bar else "",
        })

    out = os.path.join(DATA, "real_quotes_skew.csv")
    cols = ["underlying", "sample_date", "note", "spot_close", "expiry", "dte",
            "type", "panel", "target_strike", "strike", "moneyness",
            "instrument_id", "occ_symbol", "resolution_attempts",
            "substituted", "bar_date", "open", "high", "low", "close"]
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# PROVENANCE: source=%s\n" % SOURCE)
        fh.write("# PROVENANCE: pull_date=%s\n" % PULL_DATE)
        fh.write("# PROVENANCE: underlying_close_source=TradingView "
                 "AMEX:SPY 1D close, carried from the sibling "
                 "index-options-test pull (2026-10-14)\n")
        fh.write("# PROVENANCE: rate_source=TVC:US03M 1D close (per-cent "
                 "per-annum yield index), carried from the same sibling pull\n")
        fh.write("# PROVENANCE: expiry_rule=Friday weekly closest to %.1f DTE "
                 "(centre of the 30-45 band); ONE declared override: "
                 "SPY 2020-03-02 -> 2020-04-17 (Good Friday closed 2020-04-10)\n"
                 % TARGET_DTE)
        fh.write("# PROVENANCE: ladder=puts %s OTM, calls %s OTM; target strike "
                 "rounded to the nearest dollar, then substituted to a "
                 "neighbouring LISTED strike where the grid lacks it "
                 "(substituted=yes)\n" %
                 (",".join("%.0f%%" % (p * 100) for p in LADDER_PUTS),
                  ",".join("%.0f%%" % (p * 100) for p in LADDER_CALLS)))
        fh.write("# PROVENANCE: declared=%d resolved=%d returned_bar=%d\n"
                 % (funnel["declared"], funnel["resolved"], funnel["bar"]))
        fh.write("# PROVENANCE: option bars carry NO volume (Robinhood does not "
                 "publish it); only NON-interpolated bars are accepted; "
                 "bar_date is the last non-interpolated session at or before "
                 "sample_date\n")
        fh.write("# PROVENANCE: filters applied in study.py, not here: "
                 "price >= $%.2f, %.0f%% >= IV >= %.0f%%, bar lag <= %d days\n"
                 % (MIN_PRICE, MAX_IV * 100, MIN_IV * 100, MAX_BAR_LAG_DAYS))
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(cols)
        for r in sorted(rows, key=lambda r: (r["panel"], r["sample_date"],
                                             r["type"], r["strike"])):
            w.writerow([("%.2f" % r[c]) if isinstance(r[c], float) else r[c]
                        for c in cols])
    print("wrote %s (%d declared rows)" % (out, len(rows)))
    print("  FUNNEL: declared=%d  resolved_as_instrument=%d  returned_bar=%d"
          % (funnel["declared"], funnel["resolved"], funnel["bar"]))
    for key, why in unresolved:
        print("  UNRESOLVED %s: %s" % (key, why))
    with open(out, "r", encoding="utf-8") as fh:
        body = "".join(ln for ln in fh if not ln.startswith("#"))
    print("  sha256(body)=%s" % hashlib.sha256(body.encode()).hexdigest())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", action="store_true")
    ap.add_argument("--ingest", action="store_true")
    a = ap.parse_args()
    if a.plan:
        write_plan()
    if a.ingest:
        ingest()
    if not (a.plan or a.ingest):
        ap.print_help()


if __name__ == "__main__":
    main()
