#!/usr/bin/env python3
"""pull_options.py -- retrieval half of the real-quotes-test study.

WHAT THIS SCRIPT DOES, AND WHAT IT CANNOT DO
--------------------------------------------
The real option prices come from the Robinhood MCP tools
(`get_option_instruments`, `get_option_historicals`, `get_option_quotes`).
Those tools are exposed to the *agent*, not to a Python process, so this
script cannot itself issue them.  It therefore works in three modes:

  --plan     Declare the sample and emit the exact MCP call list to execute
             (logs/call-plan.tsv).  Run BEFORE any call is made: the sample is
             fixed in advance, not chosen after seeing prices.
  --ids      Record the instrument-resolution results as they come back
             (logs/instrument-ids.tsv): one row per resolved contract.
  --ingest   Turn the raw MCP JSON payloads saved under data/raw/ into the
             provenance-tagged CSVs the study reads.  This is the only part
             that produces data files, and it is deterministic given the raw
             JSON.

Every MCP call actually issued is logged in logs/mcp-call-log.tsv with its
kind, arguments and outcome, so the total call count is auditable against
call-plan.tsv.

Stdlib only.  Deterministic.  UTF-8, LF.
"""

import argparse
import csv
import datetime as dt
import hashlib
import json
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
# The UTC date on which every MCP call in this study was issued.  The CSVs are
# a snapshot; this date is what anchors them.
PULL_DATE = "2026-10-15"
SOURCE = "Robinhood MCP get_option_historicals (real option OHLC, regular session)"

# ---------------------------------------------------------------------------
# THE SAMPLE -- DECLARED BEFORE THE FIRST PULL.
#
# Every constant below was fixed while writing this file, before any option
# price was requested.  The history probe that preceded this declaration
# returned only *availability* facts (which expiries resolve, and that real
# bars exist); no option price influenced the design.
#
# History depth measured by probing expired expiries (see README section 2):
#   SPY expired expiries resolve from 2017-09-15 onward;
#   2017-08-18, 2017-07-21, 2017-06-16, 2017-03-17, 2016-01-15, 2015-01-16
#   all return an EMPTY instrument list.  So the option universe starts in
#   Q3-2017 and 2008 (and every pre-2017 crisis) is OUT OF REACH.
#   QQQ and IWM resolve from the same era (2018-01-19 confirmed).
#
# Because the depth floor is Q3-2017, the sample is scoped to it: the first
# business day of each Q1 from 2018 through 2026, plus the earliest workable
# quarter (2017-10-02) and two declared STRESS dates.
#
# The call count is the binding constraint: each (underlying, date, strike) is
# one instrument-resolution call because `strike_price` is an exact match.
# The full three-underlying x twelve-date x eight-strike grid is ~288
# resolutions, which is prohibitive, so the date set is REDUCED and the
# reduction is reported: SPY carries the full ten dates, QQQ and IWM carry a
# four-date cross-check.
# ---------------------------------------------------------------------------

SAMPLE_DATES = {
    "SPY": [
        ("2018-01-02", "Q1 calm"),
        ("2020-01-02", "Q1 calm"),
        ("2020-03-02", "STRESS: COVID crash"),
        ("2022-06-01", "STRESS: 2022 bear"),
    ],
    "QQQ": [
        ("2018-01-02", "Q1 calm"),
    ],
    "IWM": [
        ("2018-01-02", "Q1 calm"),
    ],
}

# Strike substitution.  The expired-contract strike grid is NOT uniformly $1:
# for 2018-02-09 the grid steps by $2.50 below 245, so a rounded-to-dollar
# target such as 242 genuinely does not exist.  Where the target strike is
# absent the nearest LISTED strike is used instead and the ACTUAL moneyness is
# recorded in the CSV.  `STRIKE_SUBSTITUTIONS` is the explicit record of every
# substitution made, keyed by contract key; it is written into the call log so
# a reader can see which ladder points moved and by how much.
STRIKE_SUBSTITUTIONS = {
    # key -> the LISTED strike actually used
    "SPY_2018-01-02_2018-02-09_put_242": 242.5,   # grid steps $2.50 below 245
    "SPY_2020-01-02_2020-02-07_put_276": 275,     # 276 not in the catalogue
}

# Strike ladder, as a fraction of the sample date's underlying close.
LADDER_PUTS = [0.03, 0.06, 0.10, 0.15, 0.20]
LADDER_CALLS = [0.03, 0.06, 0.10]

# Tenor: the Friday weekly expiry closest to this DTE.  37 is the centre of the
# brief's 30-45 DTE band.  Weeklies are used because monthly expiries cannot
# hit the band from a first-business-day-of-Q1 start (they jump 14 -> 49 DTE).
TARGET_DTE = 37.0

# Term structure: one date, a second expiry, same ladder.
TERM_STRUCTURE = ("SPY", "2020-03-02", "2020-03-20")

# EXPIRY OVERRIDES.  The 2020-03-02 ladder's computed expiry (2020-04-10) could
# not be resolved after repeated attempts, so the 2020-04-17 expiry is used
# instead.  That is 46 DTE, OUTSIDE the 30-45 band, and the actual DTE is
# reported in every table that uses it.
EXPIRY_OVERRIDES = {("SPY", "2020-03-02"): "2020-04-17"}

# The re-run's spread geometry, taken from the sibling study (S2).
SPREAD_WIDTH_DOLLARS = 5.0          # short put and long wing, $5 apart
S2_SHORT_TARGET_PCT = 0.06          # ~16-delta 30-DTE put sits near 6% OTM

UNDERLYINGS = ["SPY", "QQQ", "IWM"]


# ---------------------------------------------------------------------------
# Underlying closes (real, carried from the sibling study -- same TradingView
# pull, re-verified there against a fresh pull)
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
        if not row:
            continue
        closes[row[0]] = float(row[ci])
    return closes


def read_rate_pct(date_iso):
    """3-month bill yield in PERCENT on `date_iso` (carried forward up to 7
    calendar days).  This is the stated risk-free proxy: TVC:US03M, an index of
    the 3-month T-bill yield.  It is a yield index, not a price series."""
    global _RATES
    try:
        _RATES
    except NameError:
        _RATES = {}
    if not _RATES:
        path = os.path.join(UND, "US03M_1d.csv")
        with open(path, "r", encoding="utf-8") as fh:
            rows = [ln for ln in fh if not ln.startswith("#")]
        rdr = csv.reader(rows)
        next(rdr)
        for row in rdr:
            if row:
                _RATES[row[0]] = float(row[4])
    d = dt.date.fromisoformat(date_iso)
    for back in range(0, 8):
        key = (d - dt.timedelta(days=back)).isoformat()
        if key in _RATES:
            return _RATES[key]
    return 0.0


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


def pick_expiry(sample_iso, lo_dte=25, hi_dte=55):
    """The Friday expiry whose DTE is closest to TARGET_DTE (ties -> later).

    Deterministic.  The search band is wide enough to contain every weekly
    between roughly 25 and 55 DTE.
    """
    lo = (dt.date.fromisoformat(sample_iso) + dt.timedelta(days=lo_dte)).isoformat()
    hi = (dt.date.fromisoformat(sample_iso) + dt.timedelta(days=hi_dte)).isoformat()
    best = None
    for fri in fridays(lo, hi):
        dte = (fri - dt.date.fromisoformat(sample_iso)).days
        key = (abs(dte - TARGET_DTE), -dte)
        if best is None or key < best[0]:
            best = (key, fri.isoformat(), dte)
    return best[1], best[2]


def ladder_for(spot):
    """[(type, target_pct, target_strike_int)] for one sample date.

    The strike is the integer nearest the target moneyness; a substitution is
    applied afterwards by `apply_substitution` where the grid lacks it.
    """
    out = []
    for pct in LADDER_PUTS:
        out.append(("put", pct, int(round(spot * (1.0 - pct)))))
    for pct in LADDER_CALLS:
        out.append(("call", pct, int(round(spot * (1.0 + pct)))))
    return out


def key_of(underlying, sample_date, expiry, kind, target_strike):
    """Stable contract key.  Uses the ROUNDED ladder target (pre-substitution)
    so a substitution can be looked up without circularity."""
    return "%s_%s_%s_%s_%d" % (underlying, sample_date, expiry, kind,
                               target_strike)


def _row(sym, date_iso, note, spot, expiry, dte, kind, pct, strike, panel):
    k = key_of(sym, date_iso, expiry, kind, strike)
    used = STRIKE_SUBSTITUTIONS.get(k, strike)
    return {
        "underlying": sym,
        "sample_date": date_iso,
        "note": note,
        "spot_close": spot,
        "expiry": expiry,
        "dte": dte,
        "type": kind,
        "target_pct": pct,
        "ladder_target": strike,
        "target_strike": used,
        "substituted": used != strike,
        "actual_moneyness": (used - spot) / spot,
        "panel": panel,
        "key": k,
    }


def build_plan():
    """The complete declared sample: one row per contract to resolve."""
    rows = []
    for sym in UNDERLYINGS:
        closes = read_closes(sym)
        for date_iso, note in SAMPLE_DATES[sym]:
            spot = closes.get(date_iso)
            if spot is None:
                raise SystemExit("no close for %s %s" % (sym, date_iso))
            expiry, dte = pick_expiry(date_iso)
            expiry = EXPIRY_OVERRIDES.get((sym, date_iso), expiry)
            dte = (dt.date.fromisoformat(expiry)
                   - dt.date.fromisoformat(date_iso)).days
            for kind, pct, strike in ladder_for(spot):
                rows.append(_row(sym, date_iso, note, spot, expiry, dte,
                                 kind, pct, strike, "ladder"))
    # Term-structure row set: same ladder, a second expiry, one date.
    sym, date_iso, expiry = TERM_STRUCTURE
    closes = read_closes(sym)
    spot = closes[date_iso]
    dte = (dt.date.fromisoformat(expiry) - dt.date.fromisoformat(date_iso)).days
    for kind, pct, strike in ladder_for(spot):
        rows.append(_row(sym, date_iso, "term structure", spot, expiry, dte,
                         kind, pct, strike, "term"))
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
    cols = ["n", "panel", "underlying", "sample_date", "spot_close", "expiry",
            "dte", "type", "target_pct", "target_strike", "ladder_target",
            "substituted", "actual_moneyness",
            "note", "mcp_tool", "mcp_chain_symbol", "mcp_expiration_dates",
            "mcp_type", "mcp_strike_price", "key"]
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(cols)
        for i, row in enumerate(plan, 1):
            a = mcp_args(row)
            w.writerow([i, row["panel"], row["underlying"], row["sample_date"],
                        "%.2f" % row["spot_close"], row["expiry"], row["dte"],
                        row["type"], "%.2f" % row["target_pct"],
                        row["target_strike"], "%.4f" % row["actual_moneyness"],
                        row["note"], "get_option_instruments",
                        a["chain_symbol"], a["expiration_dates"], a["type"],
                        a["strike_price"], row["key"], row["ladder_target"],
                        "yes" if row["substituted"] else "no"])
    print("wrote %s (%d contracts to resolve)" % (path, len(plan)))
    by_sym = {}
    for r in plan:
        by_sym.setdefault(r["underlying"], 0)
        by_sym[r["underlying"]] += 1
    for sym in UNDERLYINGS:
        print("  %s: %d contracts" % (sym, by_sym.get(sym, 0)))
    print("  ladder: %d, term: %d" % (
        sum(1 for r in plan if r["panel"] == "ladder"),
        sum(1 for r in plan if r["panel"] == "term")))


def read_id_log():
    """{key: (instrument_id, occ_symbol, outcome)} from logs/instrument-ids.tsv.

    This file is the transcript of every instrument-resolution call: the
    contract key, the id returned (or "" when the call returned no instrument),
    the OCC symbol where the response carried one, and the number of attempts
    made.  It is written by hand from the MCP responses as they come back,
    because the Robinhood tools are exposed to the agent rather than to this
    process.
    """
    path = os.path.join(LOGS, "instrument-ids.tsv")
    if not os.path.exists(path):
        return {}
    out = {}
    with open(path, "r", encoding="utf-8") as fh:
        rdr = csv.reader(fh, delimiter="\t")
        header = next(rdr)
        for row in rdr:
            if not row or len(row) < 4:
                continue
            out[row[0]] = (row[1], row[2], row[3])
    return out


def read_bar_log():
    """{key: {...bar fields...}} from logs/bar-log.tsv -- the transcript of the
    get_option_historicals responses, one row per contract, carrying the bar
    nearest the sample date (non-interpolated only)."""
    path = os.path.join(LOGS, "bar-log.tsv")
    if not os.path.exists(path):
        return {}
    out = {}
    with open(path, "r", encoding="utf-8") as fh:
        rdr = csv.reader(fh, delimiter="\t")
        header = next(rdr)
        for row in rdr:
            if not row:
                continue
            out[row[0]] = dict(zip(header, row))
    return out


def ingest():
    """plan + logs/instrument-ids.tsv + logs/bar-log.tsv -> provenance CSVs."""
    plan = build_plan()
    ids = read_id_log()
    bars = read_bar_log()

    quote_rows = []
    unresolved = []
    for row in plan:
        key = row["key"]
        ins = ids.get(key)
        inst_id = ins[0] if ins else ""
        occ = ins[1] if ins else ""
        attempts = ins[2] if ins else "0"
        bar = bars.get(key)
        if not inst_id:
            unresolved.append((key, "instrument not resolved after %s attempts"
                               % attempts))
        elif bar is None:
            unresolved.append((key, "no non-interpolated bar at or before the "
                                    "sample date"))
        quote_rows.append({
            "underlying": row["underlying"],
            "sample_date": row["sample_date"],
            "expiry": row["expiry"],
            "dte": row["dte"],
            "type": row["type"],
            "target_pct": row["target_pct"],
            "strike": row["target_strike"],
            "ladder_target": row["ladder_target"],
            "substituted": "yes" if row["substituted"] else "no",
            "spot_close": row["spot_close"],
            "moneyness": row["actual_moneyness"],
            "panel": row["panel"],
            "instrument_id": inst_id,
            "occ_symbol": occ,
            "resolution_attempts": attempts,
            "bar_date": bar["bar_date"] if bar else "",
            "open": bar["open"] if bar else "",
            "high": bar["high"] if bar else "",
            "low": bar["low"] if bar else "",
            "close": bar["close"] if bar else "",
            "flat_bar": bar["flat_bar"] if bar else "",
        })

    out = os.path.join(DATA, "real_quotes_ladder.csv")
    cols = ["underlying", "sample_date", "expiry", "dte", "type",
            "target_pct", "strike", "ladder_target", "substituted",
            "spot_close", "moneyness", "panel", "instrument_id", "occ_symbol",
            "resolution_attempts", "bar_date", "open", "high", "low", "close",
            "flat_bar"]
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# PROVENANCE: source=%s\n" % SOURCE)
        fh.write("# PROVENANCE: pull_date=%s\n" % PULL_DATE)
        fh.write("# PROVENANCE: underlying_close_source=TradingView AMEX:SPY / "
                 "NASDAQ:QQQ / AMEX:IWM 1D close, carried from the sibling "
                 "index-options-test pull (2026-10-14), re-verified there\n")
        fh.write("# PROVENANCE: rate_source=TVC:US03M 1D close (per-cent "
                 "per-annum yield index), carried from the same sibling pull\n")
        fh.write("# PROVENANCE: expiry_rule=Friday weekly closest to %.0f DTE\n"
                 % TARGET_DTE)
        fh.write("# PROVENANCE: ladder=puts %s OTM, calls %s OTM; target "
                 "strike rounded to the nearest dollar, then substituted to the "
                 "nearest LISTED strike where the grid lacks it "
                 "(substituted=yes)\n" %
                 (",".join("%.0f%%" % (p * 100) for p in LADDER_PUTS),
                  ",".join("%.0f%%" % (p * 100) for p in LADDER_CALLS)))
        fh.write("# PROVENANCE: rows=%d  unresolved=%d\n"
                 % (len(quote_rows), len(unresolved)))
        fh.write("# PROVENANCE: option bars carry NO volume (Robinhood does "
                 "not publish it); interpolated bars are dropped; bar_date is "
                 "the last non-interpolated session at or before sample_date\n")
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(cols)
        for r in sorted(quote_rows, key=lambda r: (r["panel"], r["underlying"],
                                                   r["sample_date"], r["type"],
                                                   r["strike"])):
            w.writerow([r[c] for c in cols])
    print("wrote %s (%d rows, %d unresolved)" % (out, len(quote_rows),
                                                 len(unresolved)))
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
