#!/usr/bin/env python3
"""Compare avalanche vs snowball debt payoff strategies.

Input CSV format:
name,balance,apr,min_payment
Credit Card,10000.00,24.99,250.00
Student Loan,20000.00,5.50,200.00
Auto Loan,15000.00,6.99,350.00

Usage: python debt_payoff_plan.py --input debts.csv --monthly-extra 500
"""

import csv
import argparse
import copy


def simulate_payoff(debts: list, extra: float, method: str = "avalanche") -> dict:
    """Simulate debt payoff and return summary."""
    debts = copy.deepcopy(debts)

    if method == "avalanche":
        sort_key = lambda d: -d["apr"]
    else:
        sort_key = lambda d: d["balance"]

    total_interest = 0.0
    months = 0
    payoff_order = []

    while any(d["balance"] > 0 for d in debts):
        # Sort and pick target
        active = sorted([d for d in debts if d["balance"] > 0], key=sort_key)
        if not active:
            break
        target = active[0]

        months += 1
        available = extra

        # Pay minimums on all, extra to target
        for debt in debts:
            if debt["balance"] <= 0:
                continue
            monthly_rate = debt["apr"] / 100 / 12
            interest = debt["balance"] * monthly_rate
            total_interest += interest
            debt["balance"] += interest

            payment = min(debt["min_payment"], debt["balance"])
            debt["balance"] -= payment

            if debt is target:
                extra_payment = min(available, debt["balance"])
                debt["balance"] -= extra_payment
                available -= extra_payment

            if debt["balance"] <= 0.01:
                debt["balance"] = 0
                if debt["name"] not in payoff_order:
                    payoff_order.append((debt["name"], months))

        if months > 1200:  # 100-year safety
            break

    return {
        "total_interest": round(total_interest, 2),
        "months": months,
        "years": round(months / 12, 1),
        "payoff_order": payoff_order,
    }


def main():
    parser = argparse.ArgumentParser(description="Compare debt payoff strategies")
    parser.add_argument("--input", "-i", required=True, help="CSV file: name,balance,apr,min_payment")
    parser.add_argument("--monthly-extra", "-e", type=float, default=0, help="Extra payment per month beyond minimums")
    args = parser.parse_args()

    debts = []
    with open(args.input) as f:
        for row in csv.DictReader(f):
            debts.append({
                "name": row["name"].strip(),
                "balance": float(row["balance"]),
                "apr": float(row["apr"]),
                "min_payment": float(row["min_payment"]),
            })

    total_debt = sum(d["balance"] for d in debts)

    print("=" * 60)
    print("DEBT PAYOFF COMPARISON: AVALANCHE vs SNOWBALL")
    print("=" * 60)
    print(f"\nTotal debt: ${total_debt:,.2f}")
    print(f"Extra payment per month: ${args.monthly_extra:,.2f}\n")

    avalanche = simulate_payoff(debts, args.monthly_extra, "avalanche")
    snowball = simulate_payoff(debts, args.monthly_extra, "snowball")

    print("AVALANCHE (Highest APR First):")
    print(f"  Total interest: ${avalanche['total_interest']:,.2f}")
    print(f"  Time to debt-free: {avalanche['months']} months ({avalanche['years']} years)")
    print(f"  Payoff order: {' -> '.join(d[0] for d in avalanche['payoff_order'])}")

    print(f"\nSNOWBALL (Smallest Balance First):")
    print(f"  Total interest: ${snowball['total_interest']:,.2f}")
    print(f"  Time to debt-free: {snowball['months']} months ({snowball['years']} years)")
    print(f"  Payoff order: {' -> '.join(d[0] for d in snowball['payoff_order'])}")

    diff = snowball["total_interest"] - avalanche["total_interest"]
    print(f"\n{'=' * 60}")
    print(f"Snowball costs ${diff:,.2f} MORE in interest")
    if diff < 500:
        print("RECOMMENDATION: Snowball may be worth it for psychological wins")
    elif diff < 2000:
        print("RECOMMENDATION: Avalanche recommended, snowball acceptable if motivation is an issue")
    else:
        print("RECOMMENDATION: Use avalanche -- the savings are too large to ignore")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
