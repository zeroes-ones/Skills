#!/usr/bin/env python3
"""Prompt evaluation harness — runs test cases against an LLM endpoint and reports metrics.

Usage: python run_eval.py --endpoint $URL --test-cases cases.jsonl --threshold 0.85
"""

import argparse
import json
import sys
import time
import requests
from collections import defaultdict


def load_test_cases(path: str) -> list:
    cases = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                cases.append(json.loads(line))
    return cases


def call_llm(endpoint: str, prompt: str, headers: dict = None, timeout: int = 60) -> dict:
    """Send prompt to LLM endpoint, expect JSON response with 'response' key."""
    if headers is None:
        headers = {"Content-Type": "application/json"}

    payload = {"prompt": prompt}
    resp = requests.post(endpoint, json=payload, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def check_response(response: dict, expected: dict) -> dict:
    """Check response against expected criteria. Returns dict of check results."""
    results = {}
    actual_text = response.get("response", "")

    # Length check
    if "min_length" in expected:
        results["length_ok"] = len(actual_text) >= expected["min_length"]

    # Keyword presence
    if "must_contain" in expected:
        results["keywords_ok"] = all(kw.lower() in actual_text.lower() for kw in expected["must_contain"])

    # Forbidden content
    if "must_not_contain" in expected:
        results["forbidden_ok"] = not any(fb.lower() in actual_text.lower() for fb in expected["must_not_contain"])

    # Structured output parse
    if "parse_as" in expected and expected["parse_as"] == "json":
        try:
            json.loads(actual_text)
            results["parse_ok"] = True
        except json.JSONDecodeError:
            results["parse_ok"] = False

    # Regex match
    if "regex" in expected:
        import re
        results["regex_ok"] = bool(re.search(expected["regex"], actual_text))

    return results


def main():
    parser = argparse.ArgumentParser(description="LLM prompt evaluation harness")
    parser.add_argument("--endpoint", required=True, help="LLM API endpoint URL")
    parser.add_argument("--test-cases", required=True, help="JSONL file with test cases")
    parser.add_argument("--threshold", type=float, default=0.85, help="Pass threshold (default: 0.85)")
    parser.add_argument("--header", action="append", help="HTTP header in key:value format", default=[])
    parser.add_argument("--timeout", type=int, default=60, help="Request timeout in seconds")
    args = parser.parse_args()

    headers = {}
    for h in args.header:
        k, v = h.split(":", 1)
        headers[k.strip()] = v.strip()

    cases = load_test_cases(args.test_cases)
    if not cases:
        print("ERROR: No test cases loaded.", file=sys.stderr)
        sys.exit(2)

    print("=" * 60)
    print("LLM PROMPT EVALUATION HARNESS")
    print("=" * 60)
    print(f"Endpoint:  {args.endpoint}")
    print(f"Test cases: {len(cases)}")
    print(f"Threshold: {args.threshold * 100:.0f}%")
    print()

    passed = 0
    failed = 0
    failures = []
    check_counts = defaultdict(lambda: {"passed": 0, "total": 0})
    latencies = []

    for i, case in enumerate(cases):
        case_id = case.get("id", f"case_{i}")
        prompt = case["prompt"]
        expected = case.get("expected", {})

        try:
            start = time.time()
            response = call_llm(args.endpoint, prompt, headers, args.timeout)
            elapsed = time.time() - start
            latencies.append(elapsed)

            results = check_response(response, expected)

            all_ok = all(results.values()) if results else True
            for check_name, ok in results.items():
                check_counts[check_name]["total"] += 1
                if ok:
                    check_counts[check_name]["passed"] += 1

            if all_ok:
                passed += 1
                print(f"  [{i+1}/{len(cases)}] {case_id}: PASS ({elapsed:.2f}s)")
            else:
                failed += 1
                failures.append({"id": case_id, "results": results, "response": response.get("response", "")[:200]})
                print(f"  [{i+1}/{len(cases)}] {case_id}: FAIL ({elapsed:.2f}s) — {results}")

        except Exception as e:
            failed += 1
            failures.append({"id": case_id, "error": str(e)})
            print(f"  [{i+1}/{len(cases)}] {case_id}: ERROR — {e}")

    # Summary
    score = passed / len(cases) if cases else 0
    print(f"\n{'=' * 60}")
    print(f"RESULTS: {passed}/{len(cases)} passed ({score*100:.1f}%)")
    print(f"Threshold: {args.threshold * 100:.0f}%")

    if latencies:
        latencies.sort()
        print(f"\nLATENCY (n={len(latencies)}):")
        print(f"  p50: {latencies[len(latencies)//2]*1000:.0f}ms")
        p95_idx = int(len(latencies) * 0.95)
        print(f"  p95: {latencies[p95_idx]*1000:.0f}ms")
        print(f"  p99: {latencies[int(len(latencies)*0.99)]*1000:.0f}ms")
        print(f"  max: {max(latencies)*1000:.0f}ms")

    if check_counts:
        print(f"\nPER-CHECK RESULTS:")
        for check, counts in sorted(check_counts.items()):
            pct = counts["passed"] / counts["total"] * 100 if counts["total"] > 0 else 0
            print(f"  {check}: {counts['passed']}/{counts['total']} ({pct:.0f}%)")

    print(f"\n{'=' * 60}")
    if score >= args.threshold:
        print(f"VERDICT: PASS ✅ — {score*100:.1f}% >= {args.threshold*100:.0f}% threshold")
        sys.exit(0)
    else:
        print(f"VERDICT: FAIL ❌ — {score*100:.1f}% < {args.threshold*100:.0f}% threshold")
        print(f"\nFailed cases ({len(failures)}):")
        for f in failures:
            print(f"  - {f['id']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
