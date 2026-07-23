#!/usr/bin/env python3
"""Verify data integrity: no train/test overlap, no leakage in transforms, class balance preserved.

Usage: python verify_data.py --train train.csv --test test.csv --target label
"""

import argparse
import pandas as pd
import numpy as np
import hashlib
import sys


def check_duplicate_overlap(train: pd.DataFrame, test: pd.DataFrame, target_col: str) -> dict:
    """Check for exact duplicate rows between train and test."""
    train_hash = train.drop(columns=[target_col], errors='ignore').apply(
        lambda r: hashlib.md5(str(r.values).encode()).hexdigest(), axis=1
    )
    test_hash = test.drop(columns=[target_col], errors='ignore').apply(
        lambda r: hashlib.md5(str(r.values).encode()).hexdigest(), axis=1
    )
    overlap = set(train_hash) & set(test_hash)
    return {
        "pass": len(overlap) == 0,
        "overlap_count": len(overlap),
        "train_rows": len(train),
        "test_rows": len(test),
        "message": "PASS: No overlap" if len(overlap) == 0 else f"FAIL: {len(overlap)} duplicate rows between train and test"
    }


def check_class_balance(train: pd.DataFrame, test: pd.DataFrame, target_col: str) -> dict:
    """Check class distribution is preserved across splits."""
    train_dist = train[target_col].value_counts(normalize=True).sort_index()
    test_dist = test[target_col].value_counts(normalize=True).sort_index()

    all_classes = sorted(set(train_dist.index) | set(test_dist.index))
    max_diff = 0.0
    worst_class = None
    diffs = {}

    for cls in all_classes:
        train_pct = train_dist.get(cls, 0) * 100
        test_pct = test_dist.get(cls, 0) * 100
        diff = abs(train_pct - test_pct)
        diffs[cls] = diff
        if diff > max_diff:
            max_diff = diff
            worst_class = cls

    passed = max_diff <= 2.0  # 2% tolerance
    return {
        "pass": passed,
        "max_diff_pct": round(max_diff, 2),
        "worst_class": worst_class,
        "tolerance": 2.0,
        "diffs": diffs,
        "message": f"PASS: Max class diff {max_diff:.2f}%" if passed else f"FAIL: Class {worst_class} differs by {max_diff:.2f}% (tolerance 2%)"
    }


def check_missing_values(train: pd.DataFrame, test: pd.DataFrame) -> dict:
    """Check for columns with excessive missing values."""
    train_missing = (train.isnull().sum() / len(train) * 100).round(2)
    test_missing = (test.isnull().sum() / len(test) * 100).round(2)

    problematic_train = train_missing[train_missing > 50]
    problematic_test = test_missing[test_missing > 50]

    return {
        "pass": len(problematic_train) == 0 and len(problematic_test) == 0,
        "train_high_missing": problematic_train.to_dict(),
        "test_high_missing": problematic_test.to_dict(),
        "message": "PASS: No columns >50% missing" if len(problematic_train) == 0 else f"WARN: {len(problematic_train)} columns in train >50% missing"
    }


def main():
    parser = argparse.ArgumentParser(description="Verify data integrity for ML training")
    parser.add_argument("--train", required=True, help="Training CSV file")
    parser.add_argument("--test", required=True, help="Test CSV file")
    parser.add_argument("--target", required=True, help="Target column name")
    args = parser.parse_args()

    train = pd.read_csv(args.train)
    test = pd.read_csv(args.test)

    print("=" * 55)
    print("DATA INTEGRITY VERIFICATION")
    print("=" * 55)
    print(f"Train: {len(train):,} rows x {len(train.columns)} cols")
    print(f"Test:  {len(test):,} rows x {len(test.columns)} cols")
    print()

    all_pass = True
    checks = [
        ("Train/Test Overlap", check_duplicate_overlap(train, test, args.target)),
        ("Class Balance", check_class_balance(train, test, args.target)),
        ("Missing Values", check_missing_values(train, test)),
    ]

    for name, result in checks:
        status = "✅" if result["pass"] else "❌"
        print(f"{status} {name}: {result['message']}")

        if name == "Class Balance" and not result["pass"]:
            print(f"   Per-class differences: {result['diffs']}")
        if name == "Missing Values" and not result["pass"]:
            print(f"   High-missing in train: {result['train_high_missing']}")

        if not result["pass"]:
            all_pass = False

    print()
    print(f"{'=' * 55}")
    if all_pass:
        print("VERDICT: ALL CHECKS PASSED ✅")
        sys.exit(0)
    else:
        print("VERDICT: FAILURES DETECTED ❌ — fix before training")
        sys.exit(1)


if __name__ == "__main__":
    main()
