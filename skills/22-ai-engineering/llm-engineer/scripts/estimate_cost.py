#!/usr/bin/env python3
"""LLM cost estimator — projects daily/monthly costs from token usage.

Usage: python estimate_cost.py --model gpt-4o --input-tokens 500 --output-tokens 200 --requests 10000
"""

import argparse
import sys

# Pricing per 1M tokens (USD, approximate as of mid-2025)
PRICING = {
    "gpt-4o":               {"input": 2.50,  "output": 10.00},
    "gpt-4o-mini":          {"input": 0.15,  "output": 0.60},
    "gpt-4-turbo":          {"input": 10.00, "output": 30.00},
    "gpt-4":                {"input": 30.00, "output": 60.00},
    "gpt-3.5-turbo":        {"input": 0.50,  "output": 1.50},
    "gpt-3.5-turbo-16k":    {"input": 3.00,  "output": 4.00},
    "claude-3-opus":        {"input": 15.00, "output": 75.00},
    "claude-3.5-sonnet":    {"input": 3.00,  "output": 15.00},
    "claude-3-sonnet":      {"input": 3.00,  "output": 15.00},
    "claude-3-haiku":       {"input": 0.25,  "output": 1.25},
    "gemini-1.5-pro":       {"input": 1.25,  "output": 5.00},
    "gemini-1.5-flash":     {"input": 0.075, "output": 0.30},
    "text-embedding-3-small": {"input": 0.02, "output": 0.0},
    "text-embedding-3-large": {"input": 0.13, "output": 0.0},
    "text-embedding-ada-002": {"input": 0.10, "output": 0.0},
}


def main():
    parser = argparse.ArgumentParser(description="Estimate LLM API costs")
    parser.add_argument("--model", required=True, choices=list(PRICING.keys()),
                       help="Model name")
    parser.add_argument("--input-tokens", type=int, default=500,
                       help="Average input tokens per request (default: 500)")
    parser.add_argument("--output-tokens", type=int, default=200,
                       help="Average output tokens per request (default: 200)")
    parser.add_argument("--requests", type=int, required=True,
                       help="Estimated requests per day")
    parser.add_argument("--budget", type=float, help="Monthly budget cap (USD)")
    args = parser.parse_args()

    pricing = PRICING[args.model]
    input_cost_per_req = (args.input_tokens / 1_000_000) * pricing["input"]
    output_cost_per_req = (args.output_tokens / 1_000_000) * pricing["output"]
    cost_per_req = input_cost_per_req + output_cost_per_req

    daily_cost = cost_per_req * args.requests
    monthly_cost = daily_cost * 30.44  # avg days/month
    annual_cost = daily_cost * 365.25

    print("=" * 55)
    print("LLM COST ESTIMATOR")
    print("=" * 55)
    print(f"Model:              {args.model}")
    print(f"Input tokens/req:   {args.input_tokens:,}")
    print(f"Output tokens/req:  {args.output_tokens:,}")
    print(f"Input cost:         ${pricing['input']:.2f}/1M tokens")
    print(f"Output cost:        ${pricing['output']:.2f}/1M tokens")
    print()
    print(f"Cost per request:   ${cost_per_req:.6f}")
    print(f"Requests/day:       {args.requests:,}")
    print(f"{'=' * 55}")
    print(f"DAILY cost:         ${daily_cost:,.2f}")
    print(f"MONTHLY cost:       ${monthly_cost:,.2f}")
    print(f"ANNUAL cost:        ${annual_cost:,.2f}")
    print(f"{'=' * 55}")

    # Cost-saving alternatives
    print("\nCOST COMPARISON (same token counts):")
    for alt_model, alt_price in sorted(PRICING.items(), key=lambda x: x[1]["input"] + x[1]["output"]):
        if alt_model == args.model:
            continue
        alt_cost = ((args.input_tokens / 1_000_000) * alt_price["input"] +
                    (args.output_tokens / 1_000_000) * alt_price["output"])
        alt_monthly = alt_cost * args.requests * 30.44
        savings = monthly_cost - alt_monthly
        if savings > 0:
            print(f"  {alt_model:<25} ${alt_monthly:>10,.2f}/mo  "
                  f"(save ${savings:,.2f}/mo, {savings/monthly_cost*100:.0f}%)")

    if args.budget:
        print(f"\nBUDGET CHECK (cap: ${args.budget:,.2f}/month)")
        if monthly_cost <= args.budget:
            print(f"  ✅ Within budget — ${args.budget - monthly_cost:,.2f} headroom")
        else:
            excess = monthly_cost - args.budget
            print(f"  ❌ Over budget by ${excess:,.2f}/month")
            # How many requests fit in budget?
            budget_requests = int(args.budget / (cost_per_req * 30.44))
            print(f"  Max requests/day within budget: {budget_requests:,} "
                  f"({(1 - budget_requests/args.requests)*100:.0f}% reduction)")
            sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
