#!/usr/bin/env python3
"""
AI Cost Estimator — Token-based cost projection from traffic estimates.

Usage:
    python estimate_cost.py --rps 100 [--model gpt-4o-mini] [--input-tokens 500] [--output-tokens 300]
"""

import argparse

MODEL_PRICES = {
    "gpt-4o":             {"input": 2.50,  "output": 10.00},
    "gpt-4o-mini":        {"input": 0.15,  "output": 0.60},
    "claude-3.5-sonnet":  {"input": 3.00,  "output": 15.00},
    "claude-3-haiku":     {"input": 0.25,  "output": 1.25},
    "gemini-2.5-flash":   {"input": 0.15,  "output": 0.60},
    "gemini-2.5-pro":     {"input": 1.25,  "output": 10.00},
}

def main():
    parser = argparse.ArgumentParser(description="AI cost estimator")
    parser.add_argument("--rps", type=float, required=True, help="Requests per second (average)")
    parser.add_argument("--model", default="gpt-4o-mini", choices=list(MODEL_PRICES.keys()))
    parser.add_argument("--input-tokens", type=int, default=500, help="Average input tokens per request")
    parser.add_argument("--output-tokens", type=int, default=300, help="Average output tokens per request")
    args = parser.parse_args()
    
    prices = MODEL_PRICES[args.model]
    daily_requests = args.rps * 86400
    
    daily_input_cost = daily_requests * args.input_tokens * prices["input"] / 1_000_000
    daily_output_cost = daily_requests * args.output_tokens * prices["output"] / 1_000_000
    daily_total = daily_input_cost + daily_output_cost
    monthly_total = daily_total * 30
    
    print(f"\n=== AI Cost Estimate ===")
    print(f"Model: {args.model}")
    print(f"RPS: {args.rps} ({daily_requests:,.0f} requests/day)")
    print(f"Tokens/request: {args.input_tokens} in + {args.output_tokens} out")
    print()
    print(f"Daily input cost:  ${daily_input_cost:,.2f}")
    print(f"Daily output cost: ${daily_output_cost:,.2f}")
    print(f"Daily total:       ${daily_total:,.2f}")
    print(f"Monthly total:     ${monthly_total:,.2f}")
    print()
    
    if monthly_total > 1000:
        print("WARNING: Monthly cost exceeds $1,000. Consider:")
        print("  - Downgrade to cheaper model")
        print("  - Semantic caching (30% savings typical)")
        print("  - Prompt compression (trim system prompt)")
        print("  - Batch processing (50% discount)")
    
    # Show alternatives
    print("\n--- Alternative Models ---")
    for alt_model, alt_prices in MODEL_PRICES.items():
        if alt_model == args.model:
            continue
        alt_input = daily_requests * args.input_tokens * alt_prices["input"] / 1_000_000
        alt_output = daily_requests * args.output_tokens * alt_prices["output"] / 1_000_000
        alt_total = (alt_input + alt_output) * 30
        savings = monthly_total - alt_total
        sign = "SAVE" if savings > 0 else "COST"
        print(f"  {alt_model:<25} ${alt_total:,.2f}/mo  ({sign} ${abs(savings):,.2f})")

if __name__ == "__main__":
    main()
