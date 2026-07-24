#!/usr/bin/env python3
"""Generator script for SKILL.md files.

Generates two skills:
  - event-driven-architect (04-architecture): Event-driven systems, brokers, ES/CQRS, schemas
  - product-analyst (02-product): Product metrics, experimentation, cohorts, funnels

Usage:
  python3 _gen_skills.py                  # generate both
  python3 _gen_skills.py event-driven-architect  # generate one
"""

import os, sys

BASE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Skill body templates - the full markdown content after YAML frontmatter.
# The generator reads existing SKILL.md files and rebuilds them with
# consistent frontmatter. Edit the SKILL.md files directly, then re-run
# this script to regenerate with updated frontmatter definitions below.
# ---------------------------------------------------------------------------

EVENT_DRIVEN_ARCHITECT_BODY = os.path.join(
    BASE, "skills", "04-architecture", "event-driven-architect", "SKILL.md"
)
PRODUCT_ANALYST_BODY = os.path.join(
    BASE, "skills", "02-product", "product-analyst", "SKILL.md"
)


def extract_body(filepath):
    """Read the body (everything after the closing '---' of frontmatter)."""
    with open(filepath) as f:
        content = f.read()
    parts = content.split("---", 2)
    if len(parts) >= 3:
        return parts[2].lstrip("\n")
    return ""


def build_frontmatter(fm):
    lines = ["---"]
    lines.append(f"name: {fm['name']}")
    lines.append("description: >")
    for line in fm["description"].split("\n"):
        lines.append(f"  {line.strip()}")
    lines.append("license: MIT")
    lines.append("tags:")
    for t in fm["tags"]:
        lines.append(f"- {t}")
    lines.append("author: Sandeep Kumar Penchala")
    lines.append(f"type: {fm['type']}")
    lines.append("status: stable")
    lines.append("version: 1.0.0")
    lines.append("updated: 2026-07-24")
    lines.append("token_budget: 4000")
    lines.append("chain:")
    lines.append("  consumes_from:")
    for c in fm["chain"]["consumes_from"]:
        lines.append(f"  - {c}")
    lines.append("  feeds_into:")
    for f in fm["chain"]["feeds_into"]:
        lines.append(f"  - {f}")
    lines.append("---")
    return "\n".join(lines)


# ---- Frontmatter definitions ----

EDA_FM = {
    "name": "event-driven-architect",
    "description": (
        "Use when designing event-driven systems, choosing message brokers (Kafka, RabbitMQ, "
        "SQS/SNS, EventBridge), implementing event sourcing or CQRS, designing event schemas and "
        "versioning strategies, or debugging eventual consistency issues. Handles broker selection "
        "with trade-off analysis, event schema design with Avro/Protobuf/JSON Schema, dead-letter "
        "queue patterns, idempotency and ordering guarantees, event-driven choreography vs "
        "orchestration, and exactly-once/at-least-once delivery semantics. Do NOT use for REST API "
        "design, database schema design, or synchronous RPC architectures."
    ),
    "tags": ["event-driven", "kafka", "rabbitmq", "event-sourcing", "cqrs", "messaging", "pub-sub", "schema-registry"],
    "type": "architecture",
    "chain": {
        "consumes_from": ["api-designer", "backend-developer", "database-designer", "system-architect"],
        "feeds_into": ["backend-developer", "ci-cd-builder", "database-designer", "devops-engineer",
                       "observability-engineer", "performance-engineer", "qa-engineer", "security-engineer"],
    },
}

PA_FM = {
    "name": "product-analyst",
    "description": (
        "Use when defining product metrics and KPIs, designing A/B tests and experiments, "
        "building product dashboards, performing cohort and retention analysis, conducting "
        "funnel and conversion analysis, setting up product analytics tooling (Amplitude, "
        "Mixpanel, PostHog), or making data-informed product decisions. Handles North Star "
        "metric definition, experiment design with statistical rigor (MDE, sample size, "
        "significance), retention and churn modeling, feature adoption measurement, user "
        "segmentation, and product analytics instrumentation. Do NOT use for business "
        "financial modeling, marketing attribution, or data pipeline engineering."
    ),
    "tags": ["product-analytics", "ab-testing", "metrics", "kpi", "retention", "funnel", "experimentation", "cohort"],
    "type": "product",
    "chain": {
        "consumes_from": ["ab-testing-specialist", "analytics-engineer", "data-engineer", "product-manager", "ux-researcher"],
        "feeds_into": ["analytics-engineer", "data-scientist", "data-visualization-engineer", "growth-engineer", "product-manager"],
    },
}

SKILLS = {
    "event-driven-architect": {
        "dir": "skills/04-architecture/event-driven-architect",
        "fm": EDA_FM,
        "body_source": EVENT_DRIVEN_ARCHITECT_BODY,
    },
    "product-analyst": {
        "dir": "skills/02-product/product-analyst",
        "fm": PA_FM,
        "body_source": PRODUCT_ANALYST_BODY,
    },
}


def generate(skill_id, skill_def):
    out_dir = os.path.join(BASE, skill_def["dir"])
    os.makedirs(out_dir, exist_ok=True)

    body = extract_body(skill_def["body_source"])
    if not body:
        body = "\n# SKILL.md body not found - source file missing.\n"

    fm = build_frontmatter(skill_def["fm"])
    content = fm + "\n" + body
    out_path = os.path.join(out_dir, "SKILL.md")
    with open(out_path, "w") as f:
        f.write(content)
    lines = content.count("\n")
    print(f"Generated: {out_path}  ({lines} lines, {len(content)} bytes)")


if __name__ == "__main__":
    targets = sys.argv[1:] if len(sys.argv) > 1 else list(SKILLS.keys())
    for sid in targets:
        if sid in SKILLS:
            generate(sid, SKILLS[sid])
        else:
            print(f"Unknown skill: {sid}")
            print(f"Available: {', '.join(SKILLS.keys())}")
