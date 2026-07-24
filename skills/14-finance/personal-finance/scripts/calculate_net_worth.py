#!/usr/bin/env python3
"""Calculate net worth from CSV of assets and liabilities.

Input CSV format:
type,name,value
asset,Checking Account,5000.00
asset,401k,85000.00
liability,Credit Card,3200.00
liability,Mortgage,250000.00

Usage: python calculate_net_worth.py --input finances.csv
"""

import csv
import argparse
from collections import defaultdict


def calculate_net_worth(filepath: str) -> dict:
    categories = defaultdict(lambda: {"total": 0.0, "items": []})

    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            value = float(row["value"])
            item_type = row["type"].strip().lower()
            name = row["name"].strip()
            categories[item_type]["total"] += value
            categories[item_type]["items"].append((name, value))

    total_assets = categories.get("asset", {}).get("total", 0)
    total_liabilities = categories.get("liability", {}).get("total", 0)
    net_worth = total_assets - total_liabilities

    return {
        "total_assets": total_assets,
        "total_liabilities": total_liabilities,
        "net_worth": net_worth,
        "assets": categories.get("asset", {}).get("items", []),
        "liabilities": categories.get("liability", {}).get("items", []),
    }


def main():
    parser = argparse.ArgumentParser(description="Calculate net worth from CSV")
    parser.add_argument("--input", "-i", required=True, help="CSV file with type,name,value columns")
    parser.add_argument("--monthly-gross", type=float, help="Monthly gross income for ratio calculations")
    args = parser.parse_args()

    result = calculate_net_worth(args.input)

    print("=" * 50)
    print("NET WORTH STATEMENT")
    print("=" * 50)
    print(f"\nASSETS: ${result['total_assets']:,.2f}")
    for name, value in result["assets"]:
        print(f"  {name}: ${value:,.2f}")

    print(f"\nLIABILITIES: ${result['total_liabilities']:,.2f}")
    for name, value in result["liabilities"]:
        print(f"  {name}: ${value:,.2f}")

    print(f"\n{'=' * 50}")
    print(f"NET WORTH: ${result['net_worth']:,.2f}")
    print(f"{'=' * 50}")

    if args.monthly_gross:
        annual_income = args.monthly_gross * 12
        ratio = result["net_worth"] / annual_income if annual_income > 0 else 0
        print(f"\nNet Worth to Income Ratio: {ratio:.2f}x")
        if ratio < 0.5:
            print("  Status: BELOW AVERAGE -- focus on increasing savings rate")
        elif ratio < 1.5:
            print("  Status: AVERAGE")
        elif ratio < 3.0:
            print("  Status: ABOVE AVERAGE")
        else:
            print("  Status: EXCELLENT")


if __name__ == "__main__":
    main()
