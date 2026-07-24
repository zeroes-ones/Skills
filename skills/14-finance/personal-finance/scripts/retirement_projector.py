#!/usr/bin/env python3
"""Monte Carlo retirement success probability calculator.

Usage: python retirement_projector.py --portfolio 500000 --annual-contribution 20000
       --years 30 --withdrawal-rate 4 --expenses 50000
"""

import argparse
import random
import math
import sys


def simulate(portfolio, annual_contribution, years_to_retire, retirement_years,
             withdrawal_rate, annual_return, annual_std, simulations=10000):
    """Monte Carlo simulation of retirement success."""
    successes = 0
    final_portfolios = []

    for _ in range(simulations):
        balance = portfolio

        # Accumulation phase
        for _ in range(years_to_retire):
            ret = random.gauss(annual_return, annual_std)
            balance = balance * (1 + ret) + annual_contribution
            if balance <= 0:
                break

        if balance <= 0:
            final_portfolios.append(0)
            continue

        # Distribution phase
        annual_withdrawal = balance * (withdrawal_rate / 100)
        for _ in range(retirement_years):
            ret = random.gauss(annual_return, annual_std)
            balance = balance * (1 + ret) - annual_withdrawal
            annual_withdrawal *= 1.03  # Inflation adjustment
            if balance <= 0:
                break

        final_portfolios.append(balance)
        if balance > 0:
            successes += 1

    success_rate = successes / simulations * 100
    final_portfolios.sort()
    median = final_portfolios[len(final_portfolios) // 2]
    worst10 = final_portfolios[len(final_portfolios) // 10]

    return success_rate, median, worst10


def main():
    parser = argparse.ArgumentParser(description="Monte Carlo retirement simulator")
    parser.add_argument("--portfolio", "-p", type=float, required=True,
                        help="Current portfolio value")
    parser.add_argument("--annual-contribution", "-c", type=float, required=True,
                        help="Annual contribution amount")
    parser.add_argument("--years", "-y", type=int, required=True,
                        help="Years until retirement")
    parser.add_argument("--retirement-years", "-r", type=int, default=30,
                        help="Years in retirement (default: 30)")
    parser.add_argument("--withdrawal-rate", "-w", type=float, default=4.0,
                        help="Initial withdrawal rate percentage (default: 4.0)")
    parser.add_argument("--return", type=float, default=0.07,
                        help="Expected annual real return (default: 0.07 = 7%%)")
    parser.add_argument("--std", type=float, default=0.15,
                        help="Annual return standard deviation (default: 0.15)")
    parser.add_argument("--simulations", "-s", type=int, default=10000,
                        help="Number of Monte Carlo simulations (default: 10000)")
    args = parser.parse_args()

    print("=" * 55)
    print("RETIREMENT MONTE CARLO SIMULATION")
    print("=" * 55)
    print(f"\nPortfolio: ${args.portfolio:,.0f}")
    print(f"Annual contribution: ${args.annual_contribution:,.0f}")
    print(f"Years to retirement: {args.years}")
    print(f"Retirement duration: {args.retirement_years} years")
    print(f"Withdrawal rate: {args.withdrawal_rate}%")
    print(f"Expected return: {args.return*100:.1f}% (±{args.std*100:.1f}%)")
    print(f"\nRunning {args.simulations:,} simulations...\n")

    success_rate, median_final, worst10 = simulate(
        args.portfolio, args.annual_contribution, args.years,
        args.retirement_years, args.withdrawal_rate,
        args.return, args.std, args.simulations
    )

    print(f"Success rate: {success_rate:.1f}%")
    print(f"Median ending portfolio: ${median_final:,.0f}")
    print(f"10th percentile (worst case): ${worst10:,.0f}")

    if success_rate >= 95:
        print("\nVERDICT: HIGH CONFIDENCE -- plan is robust")
    elif success_rate >= 85:
        print("\nVERDICT: MODERATE -- consider increasing contributions or reducing withdrawals")
    elif success_rate >= 70:
        print("\nVERDICT: BORDERLINE -- significant risk of depletion")
    else:
        print("\nVERDICT: HIGH RISK -- plan needs adjustment:")
        print("  - Increase savings rate or contributions")
        print("  - Delay retirement by 2-5 years")
        print("  - Reduce withdrawal rate to 3.5% or lower")


if __name__ == "__main__":
    main()
