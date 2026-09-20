#!/usr/bin/env python3
"""
Skill Library Auditor — Domain-Calibrated Quality Reporting.

Encodes the scoring rubric from SKILL-QUALITY-STANDARDS.md.
Produces an *indicative* library rating that accounts for domain-appropriate
format variations (negative constraints, routing tables, etc.).

This is a REPORT, not a gate: the score is a weighted composite of structural
proxies (section presence, marker counts), not a correctness check. By default
it exits 0 regardless of the score and is not wired into CI. Pass --min-score
to turn it into an explicit, opt-in gate.

Usage:
    python3 scripts/audit-library.py               # Full report (exit 0)
    python3 scripts/audit-library.py --brief       # Summary only
    python3 scripts/audit-library.py --json        # Machine-readable output
    python3 scripts/audit-library.py --min-score 9 # Opt-in gate (exit 1 below floor)
"""

import os, re, sys, json, argparse
from collections import defaultdict, Counter

SKILLS_DIR = "skills"
EXCLUDE_DIRS = {".git", "__pycache__", "node_modules", ".github"}

# ── Domain-specific calibration ──────────────────────────────────

# Skills that legitimately use non-standard error decoder formats
# Format: skill_name -> reason
ADAPTED_ERROR_DECODER = {
    # People/HR — negative constraints instead of error tables
    "recruiting", "resume-writer", "hr-manager", "interview-coach",
    "people-ops", "job-search-strategist",
    # Trust & Safety — constraint violation model
    "privacy-engineering", "trust-safety-engineer", "patient-community-safety",
    "applying-llm-guardrails", "content-policy-manager", "data-security",
    # Design auditing — routing tables or Step|Action|Why
    "apple-hig-expert", "material-design-expert", "fintech-ui-designer",
    "game-ui-designer", "healthcare-ui-designer", "ui-ux-designer",
    "brand-guidelines",
    # Operations — routing/decision tables
    "project-manager", "scrum-master", "technical-writer",
    "customer-support-engineer", "event-planner", "teach", "wayfinder",
    "handoff", "technical-program-manager",
    # Strategy
    "roi-gate",
    # Data
    "ab-testing-specialist", "data-visualization-engineer", "data-engineer",
    "database-reliability-engineer", "ml-ai-engineer", "data-scientist",
    "analytics-engineer", "ml-engineer",
    # Framework meta-skills
    "using-agent-skills", "writing-great-skills", "agent-persona-orchestrator",
    "skill-levels",
    # Product
    "product-manager", "ux-researcher", "idea-to-spec", "brainstorming",
    "grilling", "product-analyst",
    # Architecture
    "desktop-architecture-patterns", "feature-flag-architect",
    # Specialized
    "brownfield-adoption-planner", "incremental-implementation",
    # Creator/Finance
    "fintech-app-developer", "marketplace-platform-builder",
    # Social Impact
    "education-access-developer",
    # Sales
    "partnerships-manager",
    # Growth
    "content-strategist",
    # AI Engineering
    "business-intelligence-engineer", "ai-safety-health-reviewer",
    "context-compaction-strategies", "mcp-management",
    "doubt-driven-development", "agent-eval-pipeline",
}

# Skills legitimately omitting Best Practices / Production Checklist
NO_BEST_PRACTICES = {
    "using-agent-skills", "writing-great-skills", "agent-persona-orchestrator",
    "skill-levels",  # framework meta-skills
    "community-operations-manager", "crisis-response-manager",
    "medical-content-reviewer", "patient-health-educator",
    "patient-experience-researcher",  # health/clinical
}

NO_PROD_CHECKLIST = {
    "using-agent-skills", "writing-great-skills", "agent-persona-orchestrator",
    "skill-levels",  # framework meta-skills
}

# Skills legitimately omitting DEEP markers
NO_DEEP_MARKER = {
    "community-operations-manager", "crisis-response-manager",
    "medical-content-reviewer", "patient-health-educator",
    "patient-experience-researcher",  # health/clinical procedural
}


def collect_skills():
    """Walk skills/ directory and return list of (path, content, name, category)."""
    skills = []
    for dirpath, dirnames, filenames in os.walk(SKILLS_DIR):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        if "SKILL.md" in filenames:
            path = os.path.join(dirpath, "SKILL.md")
            with open(path) as fh:
                content = fh.read()
            name_match = re.search(r"name:\s*(\S+)", content)
            name = name_match.group(1) if name_match else os.path.basename(dirpath)
            category = dirpath.split("/")[1] if "/" in dirpath else "unknown"
            skills.append((path, content, name, category))
    return sorted(skills, key=lambda s: s[2])


def has_section(content, section_name):
    """Check if a ## Section heading exists."""
    return bool(re.search(rf"^#+\s+{re.escape(section_name)}", content, re.MULTILINE))


def has_any_table(content):
    """Check for any markdown table (≥3 pipe-separated columns)."""
    return bool(re.search(r"^\|.+\|.+\|.+\|", content, re.MULTILINE))


def has_progressive_marker(content, marker):
    """Check for <!-- MARKER: ... --> comment."""
    return marker in content


def audit(skills):
    """Run full domain-calibrated audit."""
    total = len(skills)
    results = {
        "total": total,
        "sections": {},
        "progressive": {"QUICK": 0, "STANDARD": 0, "DEEP": 0},
        "error_decoder": {"standard_4col": 0, "adapted": 0, "missing": 0},
        "best_practices": {"present": 0, "exempt": 0, "missing": 0},
        "prod_checklist": {"present": 0, "exempt": 0, "missing": 0},
        "deep_marker": {"present": 0, "exempt": 0, "missing": 0},
        "workflow_readiness": {"declared": 0, "eligible": 0},
    }

    # Required skeleton sections
    skeleton_sections = [
        "Route the Request", "Ground Rules", "When to Use",
        "Decision Tree", "Core Workflow", "Cross-Skill Coordination",
        "What Good Looks Like", "References",
    ]

    for sec in skeleton_sections:
        results["sections"][sec] = sum(1 for _, c, _, _ in skills if has_section(c, sec))

    # Best Practices & Production Checklist
    for _, content, name, _ in skills:
        if has_section(content, "Best Practices"):
            results["best_practices"]["present"] += 1
        elif name in NO_BEST_PRACTICES:
            results["best_practices"]["exempt"] += 1
        else:
            results["best_practices"]["missing"] += 1

        if has_section(content, "Production Checklist"):
            results["prod_checklist"]["present"] += 1
        elif name in NO_PROD_CHECKLIST:
            results["prod_checklist"]["exempt"] += 1
        else:
            results["prod_checklist"]["missing"] += 1

    # Operating at Different Levels (Scale Depth)
    results["scale_depth"] = sum(
        1 for _, c, _, _ in skills if has_section(c, "Operating at Different Levels")
    )

    # Error Decoder — domain-calibrated
    for _, content, name, _ in skills:
        has_4col = bool(re.search(
            r"\|\s*(?:Symptom|Error (?:Message|Pattern|Scenario))[^|]*\|"
            r"\s*(?:Root Cause|Cause|Trigger)[^|]*\|"
            r"\s*(?:Fix|Resolution|Solution|Remediation)[^|]*\|"
            r"\s*(?:Lesson|Prevention|Takeaway)",
            content,
        ))
        has_some_table = has_any_table(content)
        is_adapted = name in ADAPTED_ERROR_DECODER

        if has_4col:
            results["error_decoder"]["standard_4col"] += 1
        elif is_adapted and has_some_table:
            results["error_decoder"]["adapted"] += 1
        elif is_adapted and not has_some_table:
            results["error_decoder"]["missing"] += 1  # adapted domain, but no table at all
        elif not is_adapted and not has_4col:
            results["error_decoder"]["missing"] += 1  # should have 4col but doesn't

    # Progressive disclosure
    for _, content, _, _ in skills:
        if has_progressive_marker(content, "<!-- QUICK"):
            results["progressive"]["QUICK"] += 1
        if has_progressive_marker(content, "<!-- STANDARD"):
            results["progressive"]["STANDARD"] += 1
        if has_progressive_marker(content, "<!-- DEEP"):
            results["progressive"]["DEEP"] += 1

    # DEEP marker — domain-calibrated
    for _, content, name, _ in skills:
        if has_progressive_marker(content, "<!-- DEEP"):
            results["deep_marker"]["present"] += 1
        elif name in NO_DEEP_MARKER:
            results["deep_marker"]["exempt"] += 1
        else:
            results["deep_marker"]["missing"] += 1

    # Workflow readiness — optional `workflow:` frontmatter (L0 node contract) declared in the
    # frontmatter, and eligibility (has Core Workflow + Verification to serve as default
    # completion-criteria source). Adoption metric only; not part of the overall quality score.
    for _, content, _, _ in skills:
        front = re.search(r"^---\s*\n(.*?)\n---\s*$", content, re.S | re.M)
        if front and re.search(r"(?m)^workflow:\s*$", front.group(1)):
            results["workflow_readiness"]["declared"] += 1
        if has_section(content, "Core Workflow") and has_section(content, "Verification"):
            results["workflow_readiness"]["eligible"] += 1

    # ── Scoring ──
    scores = {}

    # Skeleton: average of 8 section scores
    skeleton_vals = [results["sections"][s] * 10 / total for s in skeleton_sections]
    scores["skeleton"] = sum(skeleton_vals) / len(skeleton_vals)

    # Error Decoder: (standard_4col + adapted) / total
    ed_covered = results["error_decoder"]["standard_4col"] + results["error_decoder"]["adapted"]
    scores["error_decoder"] = ed_covered * 10 / total

    # Best Practices: present / (total - exempt)
    bp_denom = total - results["best_practices"]["exempt"]
    scores["best_practices"] = results["best_practices"]["present"] * 10 / bp_denom if bp_denom else 10

    # Production Checklist: present / (total - exempt)
    pc_denom = total - results["prod_checklist"]["exempt"]
    scores["prod_checklist"] = results["prod_checklist"]["present"] * 10 / pc_denom if pc_denom else 10

    # Scale Depth
    scores["scale_depth"] = results["scale_depth"] * 10 / total

    # Progressive Disclosure
    pd_vals = [results["progressive"][m] for m in ["QUICK", "STANDARD", "DEEP"]]
    scores["progressive_disclosure"] = sum(v * 10 / total for v in pd_vals) / 3

    # Workflow readiness adoption (declared / eligible) — informational, excluded from overall
    wr = results["workflow_readiness"]
    scores["workflow_readiness"] = wr["declared"] * 10 / wr["eligible"] if wr["eligible"] else 0.0

    # Overall
    weights = {
        "skeleton": 1.0,
        "error_decoder": 1.0,
        "best_practices": 0.8,
        "prod_checklist": 0.8,
        "scale_depth": 1.0,
        "progressive_disclosure": 1.0,
    }
    weighted_sum = sum(scores[k] * weights[k] for k in weights)
    weight_sum = sum(weights.values())
    scores["overall"] = weighted_sum / weight_sum

    results["scores"] = scores
    return results


def print_report(results, brief=False):
    """Pretty-print audit results."""
    total = results["total"]
    scores = results["scores"]
    sec = results["sections"]
    prog = results["progressive"]
    ed = results["error_decoder"]

    if not brief:
        print(f"""
╔══════════════════════════════════════════════════════════════════╗
║         SKILL LIBRARY AUDIT — {total} skills (domain-calibrated)       ║
╠══════════════════════════════════════════════════════════════════╣
║  Dimension                  Score    Detail                     ║
╠══════════════════════════════════════════════════════════════════╣""")

        dims = [
            ("Skeleton (must-haves)", "skeleton",
             f"{sec['Route the Request']}/{sec['Ground Rules']}/{sec['When to Use']}/"
             f"{sec['Decision Tree']}/{sec['Core Workflow']}/"
             f"{sec['Cross-Skill Coordination']}/{sec['What Good Looks Like']}/{sec['References']}"),
            ("Error Decoder", "error_decoder",
             f"4col:{ed['standard_4col']} adapted:{ed['adapted']} missing:{ed['missing']}"),
            ("Best Practices", "best_practices",
             f"{results['best_practices']['present']} present, "
             f"{results['best_practices']['exempt']} exempt, "
             f"{results['best_practices']['missing']} missing"),
            ("Production Checklist", "prod_checklist",
             f"{results['prod_checklist']['present']} present, "
             f"{results['prod_checklist']['exempt']} exempt, "
             f"{results['prod_checklist']['missing']} missing"),
            ("Scale Depth (Op@Levels)", "scale_depth",
             f"{results['scale_depth']}/{total} with L1-L5"),
            ("Progressive Disclosure", "progressive_disclosure",
             f"Q:{prog['QUICK']} S:{prog['STANDARD']} D:{prog['DEEP']}"),
            ("Workflow Readiness", "workflow_readiness",
             f"{results['workflow_readiness']['declared']} declared / "
             f"{results['workflow_readiness']['eligible']} eligible"),
        ]

        for label, key, detail in dims:
            print(f"║  {label:<26s} {scores[key]:>4.1f}    {detail:<30s}║")

        print(f"""╠══════════════════════════════════════════════════════════════════╣
║  {'OVERALL':<26s} {scores['overall']:>4.1f}/10                                      ║
╚══════════════════════════════════════════════════════════════════╝""")

    else:
        print(f"Library rating: {scores['overall']:.1f}/10 ({total} skills)")
        print("(REPORT, not a gate: exits 0 unless --min-score is given; not wired into CI.)")

    # Warnings
    if ed["missing"] > 0:
        print(f"\n⚠  {ed['missing']} skills have no error-prevention mechanism at all")
    if results["best_practices"]["missing"] > 0:
        print(f"⚠  {results['best_practices']['missing']} skills missing Best Practices (non-exempt)")
    if results["prod_checklist"]["missing"] > 0:
        print(f"⚠  {results['prod_checklist']['missing']} skills missing Production Checklist (non-exempt)")
    if results["deep_marker"]["missing"] > 0:
        print(f"⚠  {results['deep_marker']['missing']} skills missing DEEP marker (non-exempt)")


def main():
    parser = argparse.ArgumentParser(description="Domain-calibrated skill library auditor")
    parser.add_argument("--brief", action="store_true", help="Summary only")
    parser.add_argument("--json", action="store_true", help="Machine-readable JSON output")
    parser.add_argument("--min-score", type=float, default=None,
                        help="Gate mode: exit 1 if the overall score is below this floor "
                             "(reports, never silently: an unset floor means exit 0)")
    args = parser.parse_args()

    skills = collect_skills()
    results = audit(skills)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print_report(results, brief=args.brief)

    if args.min_score is None:
        # This tool is a report by design: its score is a weighted composite of
        # structural proxies, not a correctness gate. Say so rather than implying
        # a green light, and only fail when the caller sets an explicit floor.
        if not args.json:
            print("\nThis is a report, not a gate (no --min-score set → exit 0).")
        return 0

    overall = results["scores"]["overall"]
    if overall < args.min_score:
        print(f"\nFAIL: overall {overall:.1f}/10 is below the --min-score floor {args.min_score:.1f}.")
        return 1
    print(f"\nPASS: overall {overall:.1f}/10 ≥ floor {args.min_score:.1f}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
