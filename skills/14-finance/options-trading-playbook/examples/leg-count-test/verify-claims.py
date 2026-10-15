#!/usr/bin/env python3
"""
verify-claims.py -- check every number transcribed by hand into FINDINGS.md and
README.md against the study's OWN output.

This is a transcription check, not a re-derivation: handcheck.py already tests
the arithmetic.  This file exists because the tables in FINDINGS.md were typed by
hand from run-output.txt, and a typed number is the easiest thing in the world to
get wrong.

USAGE
    py -3 verify-claims.py
"""

import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
RUN = os.path.join(HERE, "run-output.txt")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(newline="\n")


def read_csv(name):
    rows = []
    with io.open(os.path.join(OUT, name), "r", encoding="utf-8",
                 newline="") as fh:
        hdr = None
        for line in fh:
            f = line.rstrip("\r\n").split(",")
            if hdr is None:
                hdr = f
                continue
            rows.append(dict(zip(hdr, f)))
    return rows


def read_text(path):
    with io.open(path, "r", encoding="utf-8", newline="") as fh:
        return fh.read()


def parse_run_tables(text):
    """{section_marker: [(id, legs, p, b, E_R, c_R, E_net)]} from TEST 1."""
    out = {}
    cur = None
    for line in text.split("\n"):
        m = re.match(r"  View ([ABC]) -- ", line)
        if m:
            cur = m.group(1)
            out[cur] = {}
            continue
        if cur is None:
            continue
        f = line.split()
        if len(f) == 11 and re.match(r"^[ABC][1-4]$", f[0]) and f[1].isdigit():
            out[cur][f[0]] = {"legs": int(f[1]), "ctr": int(f[2]),
                              "p": float(f[3]), "b": float(f[4]),
                              "E_R": float(f[5]), "c_R": float(f[6]),
                              "E_net": float(f[7])}
        if f and f[0] == "MONOTONE":
            out.setdefault("_flags", {})["mono_" + cur] = f[-1]
    return out


def main():
    findings = read_text(os.path.join(HERE, "FINDINGS.md"))
    readme = read_text(os.path.join(HERE, "README.md"))
    run = read_text(RUN)
    struct = dict((r["sid"], r) for r in read_csv("structures.csv"))
    tails = dict((r["sid"], r) for r in read_csv("tails.csv"))
    pos = dict((r["sid"], r) for r in read_csv("positivity.csv"))
    verdict = dict((r["sid"], r) for r in read_csv("verdict.csv"))
    cost = dict((r["sid"], r) for r in read_csv("cost_drag.csv"))
    skew = dict((r["sid"], r) for r in read_csv("skew_sensitivity.csv"))
    shape = dict((r["sid"], r) for r in read_csv("shape_greeks.csv"))
    stress = {}
    for r in read_csv("stress_windows.csv"):
        stress[(r["sid"], r["window"])] = r

    t1 = parse_run_tables(run)

    checks = []
    fails = []

    def chk(label, got, want, tol=5e-5):
        ok = (got is not None and want is not None and abs(got - want) <= tol)
        checks.append((label, "ok" if ok else "MISMATCH", got, want))
        if not ok:
            fails.append("%s: got %r want %r" % (label, got, want))

    def squash(t):
        """Collapse all whitespace runs, so a needle is not defeated by the
        markdown's own line wrapping."""
        return " ".join(t.split())

    def has(label, needle, where=None):
        hay = squash(where if where is not None else findings)
        needle = squash(needle)
        ok = needle in hay
        checks.append((label, "ok" if ok else "MISSING", needle, "-"))
        if not ok:
            fails.append("%s: %r not found" % (label, needle))

    # ---- the run's own reported E_net must equal the CSV's
    for view, ids in t1.items():
        if view.startswith("_"):
            continue
        for sid, r in ids.items():
            chk("TEST1 %s E_net run vs csv" % sid, r["E_net"],
                float(struct[sid]["E_net"]))
            chk("TEST1 %s c_R run vs csv" % sid, r["c_R"],
                float(struct[sid]["c_R"]))
            chk("TEST1 %s legs run vs csv" % sid, float(r["legs"]),
                float(struct[sid]["legs"]))
            chk("TEST1 %s ctr run vs csv" % sid, float(r["ctr"]),
                float(struct[sid]["contracts"]))

    # ---- the monotonicity verdict the run printed
    for v, flag in t1.get("_flags", {}).items():
        chk("monotone %s = NO" % v, 1.0 if flag == "NO" else 0.0, 1.0)

    # ---- §1 numbers typed into FINDINGS
    f1 = {"A1": (2, 0.8976, 0.181, 0.0599, 0.0321, 0.0140, 0.0181, 181),
          "A4": (2, 0.8769, 0.470, 0.2893, 0.2303, 0.0258, 0.2045, 2045),
          "A2": (4, 0.8573, 0.353, 0.1596, 0.0915, 0.0313, 0.0602, 602),
          "A3": (4, 0.4194, 1.451, 0.0279, 0.0271, 0.1387, -0.1116, -1116),
          "B1": (1, 0.2298, 1.464, -0.4336, -0.4271, 0.0275, -0.4546, -4546),
          "B2": (2, 0.4510, 1.448, 0.1040, 0.0953, 0.0428, 0.0525, 525),
          "B4": (2, 0.4804, 0.262, -0.3939, -0.2121, 0.0263, -0.2384, -2384),
          "B3": (2, 0.4946, 0.963, -0.0290, -0.0005, 0.0007, -0.0012, -12),
          "C1": (1, 0.9031, 0.220, 0.1021, 0.0027, 0.0004, 0.0023, 23),
          "C4": (1, 0.7625, 0.602, 0.2215, 0.0085, 0.0003, 0.0081, 81),
          "C2": (2, 0.6841, 0.880, 0.2858, 0.0118, 0.0008, 0.0109, 109),
          "C3": (2, 0.8976, 0.181, 0.0599, 0.0321, 0.0140, 0.0181, 181)}
    for sid, (lg, p, b, ef, er, cr, en, e10k) in f1.items():
        chk("%s legs" % sid, float(struct[sid]["legs"]), float(lg))
        chk("%s p" % sid, float(struct[sid]["p"]), p)
        chk("%s b" % sid, float(struct[sid]["b"]), b, 5e-4)
        chk("%s E_form" % sid, float(struct[sid]["E_form"]), ef)
        chk("%s E_R" % sid, float(struct[sid]["E_R"]), er)
        chk("%s c_R" % sid, float(struct[sid]["c_R"]), cr)
        chk("%s E_net" % sid, float(struct[sid]["E_net"]), en)
        chk("%s E$/10k" % sid, float(struct[sid]["E_net_per_10k"]), e10k, 0.6)

    # ---- §1 p / p* cross-reference
    pstars = {"A1": (0.8976, 0.8469), "A2": (0.8573, 0.7393),
              "A3": (0.4194, 0.4080), "A4": (0.8769, 0.6801),
              "B1": (0.2298, 0.4058), "B2": (0.4510, 0.4085),
              "B3": (0.4946, 0.5093), "B4": (0.4804, 0.7926),
              "C1": (0.9031, 0.8194), "C2": (0.6841, 0.5321),
              "C4": (0.7625, 0.6243), "C3": (0.8976, 0.8469)}
    for sid, (p, ps) in pstars.items():
        chk("%s p*" % sid, float(struct[sid]["p_star"]), ps)

    # ---- §2 cost
    f2 = {"A1": (2, 2, 6.30, 454.35, 0.0140, 0.0251, 0.0280, 0.0321, 14.59),
          "A2": (4, 4, 12.60, 407.25, 0.0313, 0.0561, 0.0625, 0.0915, 37.26),
          "A3": (4, 4, 12.60, 139.38, 0.1387, 0.2488, 0.2775, 0.0271, 3.78),
          "A4": (2, 2, 6.30, 287.44, 0.0258, 0.0462, 0.0515, 0.2303, 66.20),
          "B2": (2, 2, 6.30, 171.95, 0.0428, 0.0768, 0.0856, 0.0953, 16.38),
          "C1": (1, 1, 3.15, 11754.07, 0.0004, 0.0006, 0.0007, 0.0027, 31.17),
          "C2": (2, 1, 9.34, 12271.05, 0.0008, 0.0026, 0.0017, 0.0118, 144.48),
          "C4": (1, 1, 3.15, 12134.48, 0.0003, 0.0006, 0.0007, 0.0085, 102.67)}
    for sid, (lg, ct, costd, rd, cl, ch, crt, cs, csd) in f2.items():
        chk("%s contracts" % sid, float(struct[sid]["contracts"]), ct)
        chk("%s cost$" % sid, float(cost[sid]["cost_dollars_med"]), costd, 0.01)
        chk("%s R$med" % sid, float(struct[sid]["R_dollars_med"]), rd, 0.01)
        chk("%s c_R LOW" % sid, float(cost[sid]["c_R_LOW"]), cl)
        chk("%s c_R HIGH" % sid, float(cost[sid]["c_R_HIGH"]), ch, 5.1e-5)
        chk("%s c_R RT" % sid, float(cost[sid]["c_R_RT"]), crt)
        chk("%s c_R* " % sid, float(cost[sid]["c_R_star_r"]), cs)
        chk("%s c_R* $" % sid, float(cost[sid]["c_R_star_dollars"]), csd, 0.01)

    # ---- §3 skew
    f3 = {"A3": (4, 2, 4, 0.0271, 1.3680, -0.2924, 0.0620, 190.68, 50.48),
          "A2": (4, 2, 4, 0.0915, 0.1352, -0.0857, 0.0402, 55.06, 1.478),
          "A4": (2, 2, 2, 0.2303, 0.1222, -0.0925, 0.1222, 35.13, 0.531),
          "A1": (2, 1, 2, 0.0321, 0.0477, -0.0378, 0.0172, 21.67, 1.486),
          "C4": (1, 1, 1, 0.0085, 0.0017, -0.0017, 0.0017, 20.83, 0.203),
          "B2": (2, 1, 2, 0.0953, 0.1187, -0.0925, -0.0218, 20.40, 1.246),
          "C2": (2, 1, 1, 0.0118, 0.0015, -0.0015, 0.0015, 18.66, 0.129),
          "B3": (2, 1, 2, -0.0005, 0.0015, -0.0015, -0.0000, 17.98, 2.916),
          "B4": (2, 1, 2, -0.2121, 0.0399, -0.0358, -0.0238, 16.36, 0.188),
          "B1": (1, 0, 1, -0.4271, 0.0000, 0.0000, -0.0666, 8.96, 0.156),
          "C1": (1, 1, 1, 0.0027, 0.0011, -0.0010, 0.0011, 12.95, 0.415)}
    for sid, (lg, sold, strk, er, dp, dm, da, dd, rat) in f3.items():
        chk("%s skew sold" % sid, float(skew[sid]["n_sold_legs"]), sold, 0.0)
        chk("%s skew strikes" % sid,
            float(skew[sid]["n_distinct_strikes"]), strk, 0.0)
        chk("%s skew E_R" % sid, float(skew[sid]["E_R_base"]), er)
        chk("%s dE sold+" % sid, float(skew[sid]["dE_sold_plus1.5"]), dp)
        chk("%s dE sold-" % sid, float(skew[sid]["dE_sold_minus1.5"]), dm)
        chk("%s dE all+" % sid, float(skew[sid]["dE_all_plus1.5"]), da)
        chk("%s |dE|$" % sid, float(skew[sid]["abs_dE_max_dollars"]), dd, 0.01)
        chk("%s |dE|/|E|" % sid, float(skew[sid]["abs_dE_over_absE"]), rat,
            5e-3)

    # ---- §4 tails
    f4 = {"A1": (-1.015, -1.015, -3.17, -1.02, -2.77, -1.3, -2.6, 0.2, -1.8),
          "A2": (-1.035, -1.036, -3.12, -1.03, -2.41, -0.3, -2.4, 0.8, -2.0),
          "A3": (-1.625, -1.766, -40.20, -1.54, -10.78, 0.6, -3.5, -10.8,
                 -12.8),
          "A4": (-2.475, -3.231, -6.04, -2.09, -1.23, -0.1, -6.0, 0.5, -5.6),
          "B1": (-1.096, -1.146, -133.12, -1.10, -11.28, -13.9, -14.1, -3.6,
                 -6.5),
          "B2": (-1.142, -1.182, -18.87, -1.10, -6.34, -6.8, -9.1, 6.7, -3.6),
          "B3": (-0.132, -0.192, -0.76, -0.13, -0.33, -0.4, -0.5, 0.0, -0.3),
          "B4": (-1.021, -1.035, -65.04, -0.91, -5.78, -1.4, -1.9, -3.6, -3.8),
          "C1": (-0.089, -0.149, -0.28, -0.08, -0.10, -0.1, -0.3, 0.0, -0.2),
          "C2": (-0.154, -0.213, -0.52, -0.16, -0.27, -0.3, -0.5, 0.3, -0.3),
          "C4": (-0.137, -0.196, -0.43, -0.14, -0.17, -0.2, -0.4, 0.2, -0.3)}
    for sid, (w1, w1t, dd, wm, wy, s8t, s8d, s20t, s20d) in f4.items():
        chk("%s worst1%%" % sid, float(tails[sid]["worst1pct_R"]), w1, 5e-4)
        chk("%s worst1trade" % sid, float(tails[sid]["worst1_trade_R"]), w1t,
            5e-4)
        chk("%s ddBudget" % sid, float(tails[sid]["dd_budget_R"]), dd, 5e-3)
        chk("%s worstM" % sid, float(tails[sid]["worst_month_R"]), wm, 5e-3)
        chk("%s worstY" % sid, float(tails[sid]["worst_year_R"]), wy, 5e-3)
        # the stress cells are transcribed to ONE decimal, so the tolerance is
        # half a unit in the last printed place.
        chk("%s 2008 tot" % sid,
            float(stress[(sid, "2008 GFC")]["tot_R"]), s8t, 0.06)
        chk("%s 2008 dd" % sid,
            float(stress[(sid, "2008 GFC")]["dd_R"]), s8d, 0.06)
        chk("%s 2020 tot" % sid,
            float(stress[(sid, "2020 COVID")]["tot_R"]), s20t, 0.06)
        chk("%s 2020 dd" % sid,
            float(stress[(sid, "2020 COVID")]["dd_R"]), s20d, 0.06)
    chk("A1 tot_R", float(tails["A1"]["tot_R"]), 9.82, 5e-3)
    chk("A2 tot_R", float(tails["A2"]["tot_R"]), 28.00, 5e-3)
    chk("C3 worst1%", float(tails["C3"]["worst1pct_R"]), -1.015, 5e-4)

    # ---- §5 positivity
    f5 = {"A1": (0.43, 88.6, 54.9, -33.7, 80.4, -21.9, 83.3, -16.8),
          "A4": (1.00, 86.6, 61.4, -25.2, 86.3, -17.1, 91.7, -7.5),
          "A2": (0.97, 83.7, 61.0, -22.6, 81.4, -12.8, 87.5, -4.1),
          "A3": (0.08, 44.8, 51.0, 6.2, 53.9, -2.3, 50.0, 3.3),
          "B1": (-1.04, 22.5, 38.2, 15.6, 20.6, 9.5, 4.2, 10.7),
          "B2": (0.33, 47.4, 53.9, 6.5, 56.9, -0.2, 54.2, 8.9),
          "B3": (-0.04, 53.6, 49.5, -4.1, 57.8, -8.7, 58.3, -10.1),
          "B4": (-2.50, 41.2, 23.5, -17.6, 16.7, -6.1, 0.0, 0.6),
          "C1": (0.39, 88.6, 54.4, -34.1, 85.3, -27.7, 83.3, -18.3),
          "C4": (0.77, 75.2, 58.8, -16.4, 77.5, -12.5, 83.3, -5.5),
          "C2": (0.86, 69.9, 59.7, -10.2, 79.4, -12.9, 83.3, -3.0),
          "C3": (0.43, 88.6, 54.9, -33.7, 80.4, -21.9, 83.3, -16.8)}
    for sid, (sh, m, ml, mg, q, qg, y, yg) in f5.items():
        r = pos[sid]
        chk("%s sharpe" % sid, float(r["sharpe"]), sh, 0.006)
        chk("%s pos_M" % sid, 100 * float(r["pos_M"]), m, 0.06)
        chk("%s pos_M_law" % sid, 100 * float(r["pos_M_law"]), ml, 0.06)
        chk("%s pos_M_gap" % sid, 100 * float(r["pos_M_gap"]), mg, 0.06)
        chk("%s pos_Q" % sid, 100 * float(r["pos_Q"]), q, 0.06)
        chk("%s pos_Q_gap" % sid, 100 * float(r["pos_Q_gap"]), qg, 0.06)
        chk("%s pos_Y" % sid, 100 * float(r["pos_Y"]), y, 0.06)
        chk("%s pos_Y_gap" % sid, 100 * float(r["pos_Y_gap"]), yg, 0.06)

    # ---- §6 shape
    f6 = {"A1": (10.7, -3.10, -4.92, 1.91, 3.68),
          "A2": (-0.1, -6.13, -9.50, 3.51, 3.34),
          "A3": (-1.2, -6.30, -5.63, 2.03, 1.17),
          "A4": (-1.3, -8.09, -23.74, 9.25, 2.51),
          "B1": (31.0, 5.86, 17.05, -6.30, 1.16),
          "B2": (25.1, 1.21, 3.70, -1.19, 1.47),
          "B3": (60.2, 0.20, 0.33, 0.57, 97.09),
          "B4": (0.9, 4.18, 11.95, -4.62, 3.56),
          "C1": (15.5, -3.91, -11.65, 4.74, 93.91),
          "C2": (69.0, -5.86, -17.05, 6.30, 98.84),
          "C4": (46.6, -6.57, -19.29, 8.06, 97.62)}
    for sid, (d, g, v, t, rn) in f6.items():
        r = shape[sid]
        chk("%s delta" % sid, float(r["mean_net_delta"]), d, 0.06)
        chk("%s gamma" % sid, float(r["mean_net_gamma"]), g, 0.006)
        chk("%s vega" % sid, float(r["mean_net_vega"]), v, 0.006)
        chk("%s theta" % sid, float(r["mean_net_theta"]), t, 0.006)
        chk("%s R/notional%%" % sid, 100 * float(struct[sid]["R_over_S100"]),
            rn, 0.006)

    # ---- §7 verdict
    f7 = {"A4": (0.2045, -2.475, -6.04, 0.0826, 2045, 86),
          "A2": (0.0602, -1.035, -3.12, 0.0582, 602, 61),
          "A1": (0.0181, -1.015, -3.17, 0.0178, 181, 55),
          "A3": (-0.1116, -1.625, -40.20, -0.0687, -1116, 179),
          "B2": (0.0525, -1.142, -18.87, 0.0459, 525, 145),
          "B3": (-0.0012, -0.132, -0.76, -0.0091, -12, 2),
          "B4": (-0.2384, -1.021, -65.04, -0.2335, -2384, 61),
          "B1": (-0.4546, -1.096, -133.12, -0.4146, -4546, 185),
          "C2": (0.0109, -0.154, -0.52, 0.0709, 109, 2),
          "C4": (0.0081, -0.137, -0.43, 0.0591, 81, 2),
          "C1": (0.0023, -0.089, -0.28, 0.0256, 23, 2),
          "C3": (0.0181, -1.015, -3.17, 0.0178, 181, 55)}
    for sid, (en, w1, dd, ept, e10k, u25) in f7.items():
        r = verdict[sid]
        chk("%s verdict E_net" % sid, float(r["E_net"]), en)
        chk("%s verdict worst1%%" % sid, float(r["worst1pct_R"]), w1, 5e-4)
        chk("%s verdict dd" % sid, float(r["dd_budget_R"]), dd, 5e-3)
        chk("%s edge_per_tail" % sid, float(r["edge_per_tail"]), ept, 5e-5)
        chk("%s E$/10k" % sid, float(r["E_net_per_10k"]), e10k, 0.6)
        chk("%s u@25k" % sid, float(r["units_at_25k"]), u25, 0.0)

    # ---- §8 capital
    f8 = {"A2": (3.34, 407, 363, 61, 68), "A1": (3.68, 454, 427, 55, 58),
          "C3": (3.68, 454, 427, 55, 58), "A3": (1.17, 139, 43.6, 179, 572),
          "A4": (2.51, 287, 967, 86, 25), "C1": (93.91, 11754, 37194, 2, 0),
          "C2": (98.84, 12271, 39123, 2, 0), "C4": (97.62, 12134, 38516, 2, 0),
          "B3": (97.09, 12064, 38323, 2, 0)}
    for sid, (rn, rm, r5, u_med, u_now) in f8.items():
        chk("%s R/not%%" % sid, 100 * float(struct[sid]["R_over_S100"]), rn,
            0.006)
        chk("%s R$med" % sid, float(struct[sid]["R_dollars_med"]), rm, 1.0)
        chk("%s R$recent" % sid, float(struct[sid]["R_dollars_recent"]), r5,
            1.0)
        chk("%s u@25k" % sid, float(struct[sid]["units_at_25k"]), u_med, 0.0)
        chk("%s u@25k recent" % sid,
            float(struct[sid]["units_at_25k_recent"]), u_now, 0.0)
    chk("A2 R/not 5yr -> 68", float(25000 // float(
        struct["A2"]["R_dollars_recent"])), 68, 0.0)

    # ---- n_req
    nreq = {"A1": 214.1, "A2": 50.3, "A3": 17265.7, "A4": 16.7, "B1": 31.8,
            "B2": 646.1, "B3": 13197.2, "B4": 14.5, "C1": 99.9, "C2": 61.5,
            "C3": 214.1, "C4": 60.5}
    for sid, v in nreq.items():
        chk("%s n_req" % sid, float(struct[sid]["n_req"]), v, 0.06)
    chk("all n_trades = 918", float(struct["A1"]["n_trades"]), 918, 0.0)

    # ---- README's headline claims must actually appear
    has("README monotone claim", "is **not** monotone", where=readme)
    has("README one-of-four claim", "in **one** of the four comparisons",
        where=readme)
    has("README no-survive claim", "**No 4-leg structure survives",
        where=readme)
    has("README A3 budget flag", "A3 (iron butterfly)", where=readme)
    has("README B4 correction", "the brief's wording is wrong", where=readme)
    has("README sibling match", "K1 = 108.9730", where=readme)
    has("FINDINGS legs-buy-shape", "Legs buy shape. They do not reliably buy")
    has("FINDINGS five conditions",
        "The conditions under which a complex structure IS the right answer")
    has("FINDINGS A2 vs A1 skew reversal",
        "does not survive the skew haircut")
    has("FINDINGS n_req table", "17 266")
    has("FINDINGS B4 second-worst", "second-worst")
    has("FINDINGS A3 13x drawdown", "13× worse")
    has("FINDINGS 2008 factor of 4", "by a factor of 4")
    has("FINDINGS leg count is not the variable",
        "Leg count is not the variable that matters")
    has("README R$/notional caveat",
        "`R/notional %` is printed for exactly this", where=readme)

    print("=" * 78)
    print("VERIFY CLAIMS -- FINDINGS.md / README.md vs the study's own output")
    print("=" * 78)
    print("  %d checks run" % len(checks))
    bad = [c for c in checks if c[1] != "ok"]
    print("  %d MISMATCH / MISSING" % len(bad))
    if bad:
        print("")
        for c in bad:
            print("  %-8s %-46s got=%r want=%r" % (c[1], c[0], c[2], c[3]))
    print("")
    if fails:
        print("VERIFY CLAIMS FAILED (%d)" % len(fails))
        return 1
    print("VERIFY CLAIMS PASSED -- every transcribed number matches out/*.csv"
          " and run-output.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
