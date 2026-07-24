#!/usr/bin/env python3
"""Structured output validator — ensures LLM responses parse correctly (JSON, XML, regex).

Usage: python validate_output.py --responses responses.jsonl --format json --threshold 0.99
"""

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter


def validate_json(text: str) -> tuple:
    """Try to parse as JSON. Returns (ok, error_msg)."""
    # Try direct parse
    try:
        json.loads(text)
        return True, ""
    except json.JSONDecodeError:
        pass

    # Try to extract JSON from markdown code blocks
    md_match = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', text, re.DOTALL)
    if md_match:
        try:
            json.loads(md_match.group(1))
            return True, ""
        except json.JSONDecodeError:
            pass

    # Try to find JSON-like content
    brace_match = re.search(r'\{.*\}', text, re.DOTALL)
    if brace_match:
        try:
            json.loads(brace_match.group(0))
            return True, ""
        except json.JSONDecodeError:
            return False, f"JSON parse failed: found braces but invalid JSON"

    return False, "No JSON structure found"


def validate_xml(text: str) -> tuple:
    """Try to parse as XML. Returns (ok, error_msg)."""
    md_match = re.search(r'```(?:xml)?\s*\n?(.*?)\n?```', text, re.DOTALL)
    candidate = md_match.group(1) if md_match else text
    try:
        ET.fromstring(f"<root>{candidate}</root>")
        return True, ""
    except ET.ParseError as e:
        return False, str(e)


def validate_regex(text: str, pattern: str) -> tuple:
    """Check if text matches regex pattern."""
    ok = bool(re.search(pattern, text, re.DOTALL))
    return ok, "" if ok else f"No match for pattern: {pattern[:80]}"


def main():
    parser = argparse.ArgumentParser(description="Validate structured LLM output")
    parser.add_argument("--responses", required=True, help="JSONL file with LLM responses")
    parser.add_argument("--format", choices=["json", "xml", "regex"], required=True,
                       help="Expected output format")
    parser.add_argument("--regex-pattern", help="Regex pattern (required when --format=regex)")
    parser.add_argument("--threshold", type=float, default=0.99,
                       help="Pass rate threshold (default: 0.99)")
    parser.add_argument("--response-key", default="response",
                       help="Key for response text in JSONL (default: response)")
    args = parser.parse_args()

    if args.format == "regex" and not args.regex_pattern:
        print("ERROR: --regex-pattern required when --format=regex", file=sys.stderr)
        sys.exit(2)

    passed = 0
    failed = 0
    error_types = Counter()
    failures = []

    with open(args.responses) as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                text = entry.get(args.response_key, "")
            except json.JSONDecodeError:
                failed += 1
                error_types["jsonl_parse_error"] += 1
                continue

            if args.format == "json":
                ok, err = validate_json(text)
            elif args.format == "xml":
                ok, err = validate_xml(text)
            else:
                ok, err = validate_regex(text, args.regex_pattern)

            if ok:
                passed += 1
            else:
                failed += 1
                error_types[err[:60]] += 1
                failures.append({"index": i, "error": err, "text": text[:100]})

    total = passed + failed
    pass_rate = passed / total if total > 0 else 0

    print("=" * 55)
    print("STRUCTURED OUTPUT VALIDATION")
    print("=" * 55)
    print(f"Format:     {args.format}")
    print(f"Responses:  {total:,}")
    print(f"Passed:     {passed:,} ({pass_rate*100:.1f}%)")
    print(f"Failed:     {failed:,} ({(1-pass_rate)*100:.1f}%)")
    print(f"Threshold:  {args.threshold*100:.0f}%")
    print()

    if error_types:
        print("ERROR TYPES:")
        for err, count in error_types.most_common(5):
            print(f"  [{count:>4}] {err}")

    print(f"\n{'=' * 55}")
    if pass_rate >= args.threshold:
        print(f"VERDICT: PASS ✅ — {pass_rate*100:.1f}% >= {args.threshold*100:.0f}% threshold")
        sys.exit(0)
    else:
        print(f"VERDICT: FAIL ❌ — {pass_rate*100:.1f}% < {args.threshold*100:.0f}% threshold")
        print(f"\nFirst 3 failures:")
        for f in failures[:3]:
            print(f"  [{f['index']}] {f['error']}")
            print(f"       text: {f['text'][:120]}...")
        sys.exit(1)


if __name__ == "__main__":
    main()
