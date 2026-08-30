#!/usr/bin/env python3
"""Token Efficiency — Cost Calculator and Baseline Analyzer.

Zero external dependencies (stdlib only). Source of truth for the token-efficiency
skill's Phase 1 (Measure), Phase 2 (Budget), Phase 3 (Cache), and monitoring.

Pricing policy: DEFAULT_PRICES below are [VERIFIED 2026-08-29] SNAPSHOTS.
Prices drift quarterly. In production, pass --price or --prices-file with your
own verified figures; the script warns on stderr whenever it uses a snapshot
default or a fallback estimate so stale math is never silent.

Usage:
    python3 scripts/token-cost-calculator.py --analyze requests.jsonl
    python3 scripts/token-cost-calculator.py --budget MODEL WINDOW TASK_TYPE
    python3 scripts/token-cost-calculator.py --cache requests.jsonl
    python3 scripts/token-cost-calculator.py --trend jan.jsonl feb.jsonl mar.jsonl
    python3 scripts/token-cost-calculator.py --check-budget budget.json window
    python3 scripts/token-cost-calculator.py --optimize requests.jsonl
    python3 scripts/token-cost-calculator.py --optimize r.jsonl --cache-target 0.90 --input-trim 0.2 --output-trim 0.35
    python3 scripts/token-cost-calculator.py --analyze r.jsonl --prices-file prices.json
    python3 scripts/token-cost-calculator.py --analyze r.jsonl --price my-model:2:8:0.2

Input format (JSON Lines; one request per line):
    {"model": "claude-sonnet-4", "task_type": "chat", "input_tokens": 12000,
     "output_tokens": 800, "cache_read_tokens": 0, "cache_creation_tokens": 48000,
     "latency_ms": 900, "success": true, "ts": "2026-08-29T12:00:00Z"}

--prices-file format (JSON object: model -> [input, output, cached_read] per 1M USD):
    {"my-model": [2.0, 8.0, 0.2], "claude-sonnet-4": [3.2, 16.0, 0.32]}
"""

import argparse
import json
import os
import sys

# ── Verified pricing per 1M tokens (USD): {model: (input, output, cached_read)} ──
DEFAULT_PRICES = {
    "claude-sonnet-4":   (3.00, 15.00, 0.30),
    "claude-opus-4":     (15.00, 75.00, 1.50),
    "claude-haiku-3.5":  (0.80, 4.00, 0.08),
    "gpt-4o":            (2.50, 10.00, 1.25),
    "gpt-4o-mini":       (0.15, 0.60, 0.075),
    "gemini-1.5-pro":    (1.25, 5.00, 0.3125),
    "gemini-1.5-flash":  (0.075, 0.30, 0.01875),
}
FALLBACK_PRICE = (3.00, 15.00, 0.30)
SNAPSHOT_DATE = "2026-08-29"  # [VERIFIED] date for DEFAULT_PRICES


def load_prices(overrides, prices_file=None):
    """Build the price table, tracking which models were explicitly verified.

    Returns (prices, explicit_models): prices maps model -> (input, output,
    cached); explicit_models is the set of models supplied by the operator via
    --price or --prices-file (never silent snapshot usage).
    """
    prices = dict(DEFAULT_PRICES)
    explicit = set()
    if prices_file:
        if not os.path.exists(prices_file):
            print(f"  ERROR: no such prices file: {prices_file}", file=sys.stderr)
            sys.exit(2)
        try:
            with open(prices_file) as fh:
                cfg = json.load(fh)
        except (json.JSONDecodeError, OSError) as e:
            print(f"  ERROR: cannot read prices file {prices_file}: {e}", file=sys.stderr)
            sys.exit(2)
        for model, spec in cfg.items():
            if isinstance(spec, (list, tuple)) and len(spec) == 3:
                prices[model] = tuple(float(x) for x in spec)
                explicit.add(model)
            else:
                print(f"  WARN: ignoring bad prices-file entry '{model}' (want [in, out, cached])", file=sys.stderr)
    for spec in overrides or []:
        try:
            model, inp, outp, cache = spec.split(":")
            prices[model] = (float(inp), float(outp), float(cache))
            explicit.add(model)
        except ValueError:
            print(f"  WARN: ignoring bad --price spec '{spec}' (want model:in:out:cache)", file=sys.stderr)
    return prices, explicit


def warn_snapshot(model, explicit_models):
    """Warn when a model's price comes from the snapshot table or the fallback,
    so stale math is never silent. Writes to stderr; one warning per model."""
    if model in explicit_models:
        return
    if model in DEFAULT_PRICES:
        print(f"  WARNING: using SNAPSHOT default pricing for '{model}' "
              f"([VERIFIED {SNAPSHOT_DATE}]) — prices drift quarterly; "
              f"pass --price or --prices-file for current figures", file=sys.stderr)
    else:
        print(f"  WARNING: '{model}' has no configured price — using fallback "
              f"$3.00/$15.00/$0.30 per 1M (estimate only). Supply --price "
              f"model:in:out:cache or --prices-file", file=sys.stderr)


def load_requests(path):
    if not os.path.exists(path):
        print(f"  ERROR: no such file: {path}", file=sys.stderr)
        sys.exit(2)
    rows = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows


def request_cost(row, prices, explicit_models=None, warned=None):
    raw_model = row.get("model", "unknown")
    model = raw_model if raw_model in prices else "unknown"  # fallback bucket
    inp, outp, cache = prices.get(model, FALLBACK_PRICE)
    if explicit_models is not None and warned is not None:
        warn_key = raw_model if raw_model not in prices else model
        if warn_key not in warned:
            warn_snapshot(warn_key, explicit_models)
            warned.add(warn_key)
    in_tok = row.get("input_tokens", 0)
    out_tok = row.get("output_tokens", 0)
    cr_tok = row.get("cache_read_tokens", 0)
    cc_tok = row.get("cache_creation_tokens", 0)
    # Cache-creation tokens are billed at the uncached input rate; cache-read
    # tokens at the cached rate; the remaining input at the uncached rate.
    cost = (cc_tok + (in_tok - cr_tok)) * inp / 1_000_000
    cost += cr_tok * cache / 1_000_000
    cost += out_tok * outp / 1_000_000
    return cost


def analyze(path, prices, explicit_models=None, warned=None):
    rows = load_requests(path)
    if not rows:
        print(f"  ERROR: no parseable requests in {path}", file=sys.stderr)
        sys.exit(2)
    by_task = {}
    total_cost = 0.0
    total_in = total_out = total_cr = 0
    for r in rows:
        task = r.get("task_type", "unknown")
        by_task.setdefault(task, []).append(r)
        total_cost += request_cost(r, prices, explicit_models, warned)
        total_in += r.get("input_tokens", 0)
        total_out += r.get("output_tokens", 0)
        total_cr += r.get("cache_read_tokens", 0)

    print(f"Baseline analysis: {len(rows)} requests from {path}")
    print(f"  Total input tokens:   {total_in:>12,}")
    print(f"  Total output tokens:  {total_out:>12,}")
    print(f"  Cache-read tokens:    {total_cr:>12,}  (hit share of input: {100.0 * total_cr / max(total_in, 1):.1f}%)")
    print(f"  Total estimated cost: ${total_cost:,.2f}")
    print(f"  Avg cost/request:     ${total_cost / len(rows):.4f}")
    print()
    print(f"  {'Task type':<18} {'Requests':>9} {'Avg in':>9} {'Avg out':>9} {'Cost':>10} {'$/done':>10}")
    print(f"  {'-'*18} {'-'*9} {'-'*9} {'-'*9} {'-'*10} {'-'*10}")
    for task, rs in sorted(by_task.items(), key=lambda kv: -sum(request_cost(r, prices, explicit_models, warned) for r in kv[1])):
        cost = sum(request_cost(r, prices, explicit_models, warned) for r in rs)
        done = sum(1 for r in rs if r.get("success", True))
        print(f"  {task:<18} {len(rs):>9} {sum(r.get('input_tokens', 0) for r in rs) / len(rs):>9,.0f} "
              f"{sum(r.get('output_tokens', 0) for r in rs) / len(rs):>9,.0f} ${cost:>9,.2f} "
              f"${cost / max(done, 1):>10,.4f}")
    return 0


def budget(model, window, task_type, prices, explicit_models=None, warned=None):
    if explicit_models is not None and warned is not None and model not in warned:
        warn_snapshot(model, explicit_models)
        warned.add(model)
    inp, outp, cache = prices.get(model, FALLBACK_PRICE)
    caps = {
        "debugging": (0.50, 0.05),
        "feature":   (0.55, 0.10),
        "codegen":   (0.50, 0.15),
        "chat":      (0.45, 0.05),
        "extraction": (0.40, 0.03),
        "classification": (0.40, 0.01),
        "review":    (0.60, 0.05),
    }
    in_share, out_share = caps.get(task_type, (0.50, 0.10))
    usable = 0.80 * window  # 20% margin below the window (Ground Rule R3)
    in_cap = int(usable * in_share)
    out_cap = int(usable * out_share)
    print(f"Budget for model={model} window={window:,} task_type={task_type}")
    print(f"  Usable budget (80% of window): {usable:,.0f} tokens")
    print(f"  input_cap:  {in_cap:>10,} tokens  (~${in_cap * inp / 1_000_000:.4f}/request uncached)")
    print(f"  output_cap: {out_cap:>10,} tokens  (~${out_cap * outp / 1_000_000:.4f}/request)")
    print(f"  margin:     {window - usable:,.0f} tokens")
    return 0


def cache_check(path, prices, explicit_models=None, warned=None):
    rows = load_requests(path)
    if not rows:
        print(f"  ERROR: no parseable requests in {path}", file=sys.stderr)
        sys.exit(2)
    for r in rows:
        request_cost(r, prices, explicit_models, warned)  # fire snapshot warnings
    cr = sum(r.get("cache_read_tokens", 0) for r in rows)
    cc = sum(r.get("cache_creation_tokens", 0) for r in rows)
    inp = sum(r.get("input_tokens", 0) for r in rows)
    hit = 100.0 * cr / max(inp, 1)
    print(f"Cache check: {len(rows)} requests")
    print(f"  Input tokens:        {inp:>12,}")
    print(f"  Cache-read tokens:   {cr:>12,}")
    print(f"  Cache-creation:      {cc:>12,}")
    print(f"  Hit rate (read/input): {hit:.1f}%")
    if hit >= 60:
        print("  RESULT: PASS (hit rate >= 60%)")
        return 0
    print("  RESULT: FAIL (hit rate < 60%) — run the prefix-stability audit (Decision Tree 2)")
    return 1


def trend(paths, prices, explicit_models=None, warned=None):
    totals = []
    for p in paths:
        rows = load_requests(p)
        cost = sum(request_cost(r, prices, explicit_models, warned) for r in rows)
        totals.append((p, len(rows), cost))
    print(f"{'Period':<24} {'Requests':>9} {'Cost':>10}")
    for name, n, cost in totals:
        print(f"  {name:<24} {n:>9} ${cost:>9,.2f}")
    if len(totals) >= 2:
        prev, cur = totals[-2], totals[-1]
        if prev[2] > 0:
            growth = 100.0 * (cur[2] - prev[2]) / prev[2]
            print(f"  Period-over-period cost growth: {growth:+.1f}%")
            if growth > 20:
                print("  RESULT: ALERT — growth > 20% (Proactive Trigger: investigate now)")
                return 1
    print("  RESULT: OK")
    return 0


def check_budget(path, window):
    if not os.path.exists(path):
        print(f"  ERROR: no such file: {path}", file=sys.stderr)
        return 2
    with open(path) as fh:
        cfg = json.load(fh)
    usable = 0.80 * window
    problems = 0
    for task, b in cfg.items():
        total = b.get("input_cap", 0) + b.get("output_cap", 0) + b.get("margin", 0)
        if total > usable:
            print(f"  FAIL: {task} caps+margin {total:,} > usable {usable:,.0f}", file=sys.stderr)
            problems += 1
    if problems:
        print("  RESULT: budget exceeds usable window for some task types", file=sys.stderr)
        return 1
    print(f"  RESULT: PASS — all task budgets within {usable:,.0f} usable tokens")
    return 0


def optimize(path, prices, explicit_models=None, warned=None,
             cache_target=0.90, input_trim=0.20, output_trim=0.35):
    """Project per-lever savings for a baseline and recommend the strategy mix.

    All projections are [ESTIMATED] — they model 'if lever X is applied', not
    measured results. The lever ladder is fixed: stabilize the cache first, then
    reduce, then compress, then cap output. Run --analyze after each change to
    measure actuals.
    """
    rows = load_requests(path)
    if not rows:
        print(f"  ERROR: no parseable requests in {path}", file=sys.stderr)
        sys.exit(2)

    current = sum(request_cost(r, prices, explicit_models, warned) for r in rows)
    total_in = sum(r.get("input_tokens", 0) for r in rows)
    total_cr = sum(r.get("cache_read_tokens", 0) for r in rows)
    total_out = sum(r.get("output_tokens", 0) for r in rows)
    cur_hit = 100.0 * total_cr / max(total_in, 1)

    # Lever 1: cache stabilization — project hit rate rising to cache_target
    #   current cached-read tokens stay; the rest of input becomes cached reads.
    input_cost_now = current - sum(r.get("output_tokens", 0) * prices.get(r.get("model", "unknown"), FALLBACK_PRICE)[1] / 1_000_000 for r in rows)
    new_cr = int(total_in * cache_target)
    delta_cr = max(new_cr - total_cr, 0)
    # Approximate: shifting delta_cr tokens from uncached input to cached reads.
    def _rate(model):
        return prices.get(model, FALLBACK_PRICE)
    avg_in = sum(r.get("input_tokens", 0) * _rate(r.get("model", "unknown"))[0] for r in rows) / max(total_in, 1)
    avg_cr = sum(r.get("cache_read_tokens", 0) * _rate(r.get("model", "unknown"))[2] for r in rows) / max(total_cr, 1) if total_cr else 0
    cache_saving = delta_cr * (avg_in - avg_cr) / 1_000_000

    # Lever 2: reduce (dedup/exclusion) — trim input_trim fraction of uncached input
    uncached_in = max(total_in - total_cr, 0)
    reduce_saving = uncached_in * input_trim * avg_in / 1_000_000

    # Lever 3: compress — trim the remaining uncached input after reduction
    remaining = max(uncached_in * (1 - input_trim), 0)
    compress_saving = remaining * input_trim * avg_in / 1_000_000

    # Lever 4: cap output — trim output_trim fraction of output tokens
    avg_out = sum(r.get("output_tokens", 0) * _rate(r.get("model", "unknown"))[1] for r in rows) / max(total_out, 1)
    output_saving = total_out * output_trim * avg_out / 1_000_000

    n = len(rows)
    month_mult = 22.0 * (500.0 / max(n, 1))  # scale to 500 req/day, 22 days

    print(f"Budget optimization projection from {n} requests in {path}")
    print(f"  Current cost (sample):      ${current:,.2f}")
    print(f"  Current cache hit rate:     {cur_hit:.1f}%")
    print()
    print("  Lever ladder (apply in this order) — [ESTIMATED] projections per month:")
    print(f"    L1 Stabilize cache (hit rate {cur_hit:.0f}% -> {cache_target*100:.0f}%)  ${cache_saving * month_mult:>10,.2f}")
    print(f"    L2 Reduce input (dedup/exclude {input_trim*100:.0f}%)                 ${reduce_saving * month_mult:>10,.2f}")
    print(f"    L3 Compress remaining (retention-gated {input_trim*100:.0f}%)         ${compress_saving * month_mult:>10,.2f}")
    print(f"    L4 Cap output (trim {output_trim*100:.0f}%)                           ${output_saving * month_mult:>10,.2f}")
    total = cache_saving + reduce_saving + compress_saving + output_saving
    print(f"  Combined monthly projection: ${total * month_mult:,.2f}")
    print()
    if cur_hit < 60:
        print("  RECOMMENDATION: fix caching FIRST (L1) — it is the cheapest lever and")
        print("  compounds the others. Never compress before stabilizing the cache.")
    print("  NOTE: projections are [ESTIMATED]. Re-run --analyze after each lever to")
    print("  measure actuals and confirm retention/quality held.")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Token efficiency cost calculator")
    ap.add_argument("--analyze", metavar="requests.jsonl")
    ap.add_argument("--budget", nargs=3, metavar=("MODEL", "WINDOW", "TASK_TYPE"))
    ap.add_argument("--cache", metavar="requests.jsonl")
    ap.add_argument("--trend", nargs="+", metavar="period.jsonl")
    ap.add_argument("--check-budget", nargs=2, metavar=("budget.json", "WINDOW"))
    ap.add_argument("--optimize", metavar="requests.jsonl",
                    help="project per-lever savings and recommend the strategy mix")
    ap.add_argument("--cache-target", type=float, default=0.90, help="projected hit rate for --optimize (default 0.90)")
    ap.add_argument("--input-trim", type=float, default=0.20, help="projected input trim for --optimize (default 0.20)")
    ap.add_argument("--output-trim", type=float, default=0.35, help="projected output trim for --optimize (default 0.35)")
    ap.add_argument("--price", action="append", metavar="model:in:out:cache",
                    help="override pricing, e.g. --price my-model:2:8:0.2 (repeatable)")
    ap.add_argument("--prices-file", metavar="prices.json",
                    help="JSON object model -> [input, output, cached_read] per 1M USD")
    args = ap.parse_args()
    prices, explicit = load_prices(args.price, args.prices_file)
    warned = set()

    if args.analyze:
        return analyze(args.analyze, prices, explicit, warned)
    if args.budget:
        model, window, task = args.budget
        return budget(model, int(window), task, prices, explicit, warned)
    if args.cache:
        return cache_check(args.cache, prices, explicit, warned)
    if args.trend:
        return trend(args.trend, prices, explicit, warned)
    if args.check_budget:
        return check_budget(args.check_budget[0], int(args.check_budget[1]))
    if args.optimize:
        return optimize(args.optimize, prices, explicit, warned,
                        cache_target=args.cache_target, input_trim=args.input_trim,
                        output_trim=args.output_trim)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
