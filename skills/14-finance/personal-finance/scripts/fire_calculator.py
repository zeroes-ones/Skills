#!/usr/bin/env python3
"""FIRE (Financial Independence Retire Early) calculator.

Usage: python fire_calculator.py --annual-expenses 50000 --portfolio 200000
       --annual-contribution 30000 --expected-return 0.07
"""

import argparse
import math


def years_to_fi(expenses, portfolio, contribution, annual_return, withdrawal_rate=0.04):
    """Calculate years to FI using compound growth formula."""
    fi_number = expenses / withdrawal_rate
    r = annual_return

    if portfolio >= fi_number:
        return 0, fi_number

    if contribution <= 0:
        return float("inf"), fi_number

    try:
        years = math.log((fi_number * r / contribution) + 1) / math.log(1 + r)
    except (ValueError, ZeroDivisionError):
        return float("inf"), fi_number

    return round(years, 1), round(fi_number)


def main():
    parser = argparse.ArgumentParser(description="FIRE calculator")
    parser.add_argument("--annual-expenses", "-e", type=float, required=True,
                        help="Annual expenses in retirement")
    parser.add_argument("--portfolio", "-p", type=float, required=True,
                        help="Current investment portfolio value")
    parser.add_argument("--annual-contribution", "-c", type=float, required=True,
                        help="Annual contributions to investments")
    parser.add_argument("--expected-return", "-r", type=float, default=0.07,
                        help="Expected real annual return (default: 0.07)")
    parser.add_argument("--age", type=int, help="Current age for timeline context")
    args = parser.parse_args()

    ret = args.expected_return

    print("=" * 55)
    print("FIRE CALCULATOR")
    print("=" * 55)
    print(f"\nAnnual expenses: ${args.annual_expenses:,.0f}")
    print(f"Current portfolio: ${args.portfolio:,.0f}")
    print(f"Annual contributions: ${args.annual_contribution:,.0f}")
    print(f"Expected real return: {ret*100:.1f}%")

    rates = [
        (0.04, "4% (Traditional 30yr)"),
        (0.035, "3.5% (Early FIRE 40yr)"),
        (0.033, "3.33% (Conservative)"),
        (0.03, "3% (Perpetual)"),
    ]

    print(f"\n{'Withdrawal Rate':<28} {'FI Number':>14} {'Years to FI':>12}")
    print("-" * 55)

    for rate, label in rates:
        years, fi_num = years_to_fi(args.annual_expenses, args.portfolio,
                                     args.annual_contribution, ret, rate)
        if years == float("inf"):
            yrs_str = "Never"
        else:
            yrs_str = f"{years:.1f} years"
            if args.age:
                yrs_str += f" (age {args.age + int(years)})"
        print(f"{label:<28} ${fi_num:>13,.0f}  {yrs_str:>12}")

    print(f"\n{'=' * 55}")
    print("COAST FIRE ANALYSIS")
    print(f"{'=' * 55}")
    coast_years = [10, 15, 20, 25, 30]
    for years in coast_years:
        fi_target = args.annual_expenses / 0.04
        coast_number = fi_target / ((1 + ret) ** years)
        status = "ACHIEVED" if args.portfolio >= coast_number else f"Need ${coast_number:,.0f}"
        if args.age:
            print(f"  Coast to age {args.age + years}: {status}")
        else:
            print(f"  Coast in {years} years: {status}")


if __name__ == "__main__":
    main()
