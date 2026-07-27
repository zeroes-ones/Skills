#!/usr/bin/env python3
"""Material Design 3 compliance checker.

stdlib-only tool for automated MD3 auditing. Four subcommands:
  contrast   — WCAG 2.2 contrast ratio between two hex colors
  touch-target — touch-target dimension check against MD3 48x48 dp minimum
  component  — validate component dimensions against MD3 spec
  batch      — JSON-driven batch audit producing a scored report

Scorecard rubric: starts at 100, -10 per violation.
  90-100 = ship
  70-80  = fix before release
  <70    = systematic rework required

Usage:
  python3 md3_checker.py contrast "#8E8E93" "#FFFFFF"
  python3 md3_checker.py touch-target 40 40
  python3 md3_checker.py component button-filled height 36
  python3 md3_checker.py batch audit.json
"""

import argparse
import json
import math
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional


# ──────────────────────────────────────────────────────────────────────
# Material Design 3 component spec reference
# ──────────────────────────────────────────────────────────────────────

COMPONENT_SPECS: Dict[str, Dict[str, float]] = {
    "button-filled":        {"height": 40},
    "button-tonal":         {"height": 40},
    "button-outlined":      {"height": 40},
    "button-text":          {"height": 40},
    "fab-regular":          {"size": 56},
    "fab-small":            {"size": 40},
    "fab-large":            {"size": 96},
    "nav-bar":              {"height": 80},
    "nav-rail":             {"width": 80},
    "dialog":               {"corner-radius": 28},
    "chip":                 {"height": 32},
    "snackbar-single":      {"height": 48},
    "snackbar-two":         {"height": 68},
    "text-field-filled":    {"height": 56},
    "text-field-outlined":  {"height": 56},
    "switch":               {"touch-target": 48},
    "checkbox":             {"touch-target": 48},
    "radio":                {"touch-target": 48},
    "list-item-single":     {"min-height": 56},
    "list-item-two":        {"min-height": 72},
    "list-item-three":      {"min-height": 88},
    "top-app-bar-small":    {"height": 64},
    "top-app-bar-medium":   {"height": 112},
    "top-app-bar-large":    {"height": 152},
}


# ──────────────────────────────────────────────────────────────────────
# Color utilities
# ──────────────────────────────────────────────────────────────────────


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Convert hex color string to (R, G, B) tuple."""
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 3:
        hex_color = "".join(c * 2 for c in hex_color)
    if len(hex_color) != 6:
        raise ValueError(f"Invalid hex color: {hex_color}")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def linearize(channel: int) -> float:
    """Convert sRGB channel to linear value."""
    srgb = channel / 255.0
    if srgb <= 0.04045:
        return srgb / 12.92
    return math.pow((srgb + 0.055) / 1.055, 2.4)


def relative_luminance(hex_color: str) -> float:
    """Compute WCAG 2.2 relative luminance for a hex color."""
    r, g, b = hex_to_rgb(hex_color)
    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)


def contrast_ratio(fg: str, bg: str) -> float:
    """Compute WCAG 2.2 contrast ratio between two colors."""
    l1 = relative_luminance(fg)
    l2 = relative_luminance(bg)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


# ──────────────────────────────────────────────────────────────────────
# Check result types
# ──────────────────────────────────────────────────────────────────────


@dataclass
class CheckResult:
    """Single audit check result."""
    name: str
    passed: bool
    detail: str
    check_type: str
    score: int = 0  # -10 if failed, 0 if passed


@dataclass
class AuditReport:
    """Full batch audit report."""
    total_checks: int = 0
    passed: int = 0
    failed: int = 0
    score: int = 100
    violations: List[str] = field(default_factory=list)
    results: List[CheckResult] = field(default_factory=list)


# ──────────────────────────────────────────────────────────────────────
# Check functions
# ──────────────────────────────────────────────────────────────────────


def check_contrast(name: str, fg: str, bg: str, large_text: bool = False) -> CheckResult:
    """Check contrast ratio against MD3/WCAG 2.2 thresholds.

    MD3 thresholds: 4.5:1 for normal text, 3:1 for large text
    (>18pt or >14pt bold).
    """
    ratio = contrast_ratio(fg, bg)
    threshold = 3.0 if large_text else 4.5
    passed = ratio >= threshold
    detail = f"Contrast {ratio:.2f} {'≥' if passed else '<'} {threshold:.1f}"
    if not passed:
        suggestion = _contrast_fix_suggestion(fg, bg)
        detail += f". Fix: {suggestion}"
    return CheckResult(
        name=name,
        passed=passed,
        detail=detail,
        check_type="contrast",
        score=0 if passed else -10,
    )


def _contrast_fix_suggestion(fg: str, bg: str) -> str:
    """Generate a fix suggestion for a failed contrast check."""
    fg_lum = relative_luminance(fg)
    bg_lum = relative_luminance(bg)
    if bg_lum > 0.5:
        return "darken foreground or use MD3 on-surface token"
    else:
        return "lighten foreground or use MD3 on-primary token"


def check_touch_target(name: str, width: float, height: float) -> CheckResult:
    """Check touch-target size against MD3 48x48 dp minimum."""
    min_size = 48.0
    passed = width >= min_size and height >= min_size
    if passed:
        detail = f"Target {width}x{height} dp ≥ {min_size}x{min_size} dp"
    else:
        detail = (
            f"Target {width}x{height} dp < {min_size}x{min_size} dp. "
            f"Expand touch area to 48x48 dp or use a visible indicator "
            f"like an icon within the touch target."
        )
    return CheckResult(
        name=name,
        passed=passed,
        detail=detail,
        check_type="touch-target",
        score=0 if passed else -10,
    )


def check_component(
    name: str, element: str, property: str, actual: float
) -> CheckResult:
    """Validate a component dimension against the MD3 component spec table."""
    spec = COMPONENT_SPECS.get(element)

    if spec is None:
        return CheckResult(
            name=name,
            passed=False,
            detail=f"Unknown component element: {element}",
            check_type="component",
            score=-10,
        )

    expected = spec.get(property)
    if expected is None:
        return CheckResult(
            name=name,
            passed=False,
            detail=f"Unknown property '{property}' for {element}. "
            f"Known properties: {', '.join(spec.keys())}",
            check_type="component",
            score=-10,
        )

    passed = actual == expected
    if passed:
        detail = (
            f"{element} {property}: {actual}dp matches spec ({expected}dp)"
        )
    else:
        detail = (
            f"{element} {property}: {actual}dp does not match spec ({expected}dp). "
            f"Adjust {property} to {expected}dp."
        )
    return CheckResult(
        name=name,
        passed=passed,
        detail=detail,
        check_type="component",
        score=0 if passed else -10,
    )


# ──────────────────────────────────────────────────────────────────────
# Batch processing
# ──────────────────────────────────────────────────────────────────────


def run_batch(audit_json_path: str) -> AuditReport:
    """Run a batch audit from a JSON file."""
    with open(audit_json_path, "r") as f:
        data = json.load(f)

    report = AuditReport()
    checks = data.get("checks", [])

    for check in checks:
        check_type = check.get("type", "")
        name = check.get("name", f"unnamed-{check_type}")

        if check_type == "contrast":
            large_text = check.get("large_text", False)
            result = check_contrast(name, check["fg"], check["bg"], large_text)
        elif check_type == "touch-target":
            result = check_touch_target(
                name, float(check["w"]), float(check["h"])
            )
        elif check_type == "component":
            result = check_component(
                name,
                check["element"],
                check["property"],
                float(check["actual"]),
            )
        else:
            result = CheckResult(
                name=name,
                passed=False,
                detail=f"Unknown check type: {check_type}",
                check_type="unknown",
                score=-10,
            )

        report.results.append(result)
        report.total_checks += 1
        if result.passed:
            report.passed += 1
        else:
            report.failed += 1
            report.score += result.score
            report.violations.append(result.detail)

    # Clamp score to 0-100
    report.score = max(0, min(100, report.score))
    return report


# ──────────────────────────────────────────────────────────────────────
# Output formatting
# ──────────────────────────────────────────────────────────────────────


def format_result(result: CheckResult) -> str:
    """Format a single check result."""
    status = "PASSED" if result.passed else "FAILED"
    return f"[{status}] {result.name}: {result.detail}"


def format_report(report: AuditReport) -> str:
    """Format a full audit report as JSON."""
    return json.dumps(
        {
            "score": report.score,
            "total_checks": report.total_checks,
            "passed": report.passed,
            "failed": report.failed,
            "violations": report.violations,
            "results": [
                {
                    "name": r.name,
                    "passed": r.passed,
                    "detail": r.detail,
                }
                for r in report.results
            ],
        },
        indent=2,
    )


def format_report_compact(report: AuditReport) -> str:
    """Format a compact score-only report."""
    return json.dumps(
        {
            "score": report.score,
            "violations": report.violations,
        },
        indent=2,
    )


# ──────────────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Material Design 3 compliance checker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s contrast "#8E8E93" "#FFFFFF"
  %(prog)s touch-target 40 40
  %(prog)s component button-filled height 36
  %(prog)s batch audit.json
  %(prog)s batch audit.json --compact
        """,
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # contrast subcommand
    contrast_parser = subparsers.add_parser("contrast", help="Check contrast ratio")
    contrast_parser.add_argument("fg", help="Foreground hex color")
    contrast_parser.add_argument("bg", help="Background hex color")
    contrast_parser.add_argument("--name", default="contrast-check", help="Element name")
    contrast_parser.add_argument(
        "--large-text", action="store_true", help="Use 3:1 large-text threshold"
    )

    # touch-target subcommand
    touch_target_parser = subparsers.add_parser(
        "touch-target", help="Check touch-target size against 48dp minimum"
    )
    touch_target_parser.add_argument("width", type=float, help="Target width in dp")
    touch_target_parser.add_argument("height", type=float, help="Target height in dp")
    touch_target_parser.add_argument(
        "--name", default="touch-target-check", help="Element name"
    )

    # component subcommand
    component_parser = subparsers.add_parser(
        "component", help="Validate component dimension against MD3 spec"
    )
    component_parser.add_argument("element", help="Component element name")
    component_parser.add_argument("property", help="Property to validate")
    component_parser.add_argument(
        "actual", type=float, help="Actual measured value in dp"
    )
    component_parser.add_argument(
        "--name", default="component-check", help="Element name"
    )

    # batch subcommand
    batch_parser = subparsers.add_parser("batch", help="Run batch audit from JSON")
    batch_parser.add_argument("audit_file", help="Path to audit JSON file")
    batch_parser.add_argument(
        "--compact",
        action="store_true",
        help="Output compact score-only format",
    )

    args = parser.parse_args()

    if args.command == "contrast":
        result = check_contrast(args.name, args.fg, args.bg, args.large_text)
        print(format_result(result))
        sys.exit(0 if result.passed else 1)

    elif args.command == "touch-target":
        result = check_touch_target(args.name, args.width, args.height)
        print(format_result(result))
        sys.exit(0 if result.passed else 1)

    elif args.command == "component":
        result = check_component(args.name, args.element, args.property, args.actual)
        print(format_result(result))
        sys.exit(0 if result.passed else 1)

    elif args.command == "batch":
        report = run_batch(args.audit_file)
        if args.compact:
            print(format_report_compact(report))
        else:
            print(format_report(report))
        sys.exit(0 if report.score >= 70 else 1)


if __name__ == "__main__":
    main()
