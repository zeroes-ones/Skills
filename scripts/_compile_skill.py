#!/usr/bin/env python3
"""
_compile_skill.py — Python compiler for SKILL.md → XML
Called by compile-skills.sh. Parses YAML frontmatter, extracts sections,
and generates minified XML with token budget metadata.
"""

import sys, os, re, json, datetime, xml.etree.ElementTree as ET
from pathlib import Path


def parse_frontmatter(text):
    """Extract YAML frontmatter and body from SKILL.md content."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", text, re.DOTALL)
    if not m:
        return {}, text
    raw = m.group(1)
    body = m.group(2)
    data = {}
    multiline_key = None
    multiline_val = []
    list_key = None
    list_val = []

    for line in raw.split("\n"):
        # Handle list items under a key
        if list_key is not None:
            list_match = re.match(r"^\s+-\s+(.*)", line)
            if list_match:
                list_val.append(list_match.group(1).strip())
                continue
            else:
                data[list_key] = list_val
                list_key = None
                list_val = []

        # Handle multiline values (key: >)
        if multiline_key is not None:
            if re.match(r"^\s{2,}", line) or (line.strip() and ":" not in line):
                multiline_val.append(line.strip())
                continue
            else:
                data[multiline_key] = " ".join(multiline_val)
                multiline_key = None
                multiline_val = []

        # Skip empty lines
        if not line.strip():
            continue

        # Check for "key: >" (multiline indicator)
        m_multi = re.match(r"^(\w[\w_-]*):\s*>\s*$", line)
        if m_multi:
            multiline_key = m_multi.group(1)
            multiline_val = []
            continue

        # Check for "key:" with list indicator (next lines will be "- item")
        m_list = re.match(r"^(\w[\w_-]*):\s*$", line)
        if m_list:
            list_key = m_list.group(1)
            list_val = []
            continue

        # Simple key: value
        m_kv = re.match(r'^(\w[\w_-]*):\s*["' + "'" + r"]?(.*?)[" + "'" + r"]?\s*$", line)
        if m_kv:
            data[m_kv.group(1)] = m_kv.group(2).strip()

    # Close any open multiline or list
    if multiline_key is not None:
        data[multiline_key] = " ".join(multiline_val)
    if list_key is not None:
        data[list_key] = list_val

    # Parse nested chain structure from raw frontmatter
    chain_match = re.search(
        r"^chain:\s*\n((?:\s+.*\n)*)", raw, re.MULTILINE
    )
    if chain_match:
        chain_block = chain_match.group(1)
        consumes = []
        feeds = []
        current = None
        for line in chain_block.split("\n"):
            if "consumes_from:" in line:
                current = "consumes"
                continue
            elif "feeds_into:" in line:
                current = "feeds"
                continue
            m_item = re.search(r"-\s+(.+)", line)
            if m_item and current == "consumes":
                consumes.append(m_item.group(1).strip())
            elif m_item and current == "feeds":
                feeds.append(m_item.group(1).strip())
        if consumes or feeds:
            data["chain"] = {"consumes_from": consumes, "feeds_into": feeds}

    return data, body


def extract_sections(body):
    """Extract named sections from markdown body. Returns dict of section_name -> content."""
    sections = {}
    known = [
        "## Route the Request",
        "## Anti-Rationalization",
        "## Ground Rules",
        "## The Expert.s Mindset",
        "## Operating at Different Levels",
        "## When to Use",
        "## Decision Trees",
        "## Core Workflow",
        "## Cross-Skill Coordination",
        "## Proactive Triggers",
        "## What Good Looks Like",
        "## Deliberate Practice",
        "## Gotchas",
        "## Verification",
        "## References",
    ]
    positions = []
    for heading in known:
        pattern = re.escape(heading)
        for m in re.finditer(r"^" + pattern, body, re.MULTILINE):
            positions.append((m.start(), heading))
    positions.sort(key=lambda x: x[0])
    for i, (pos, heading) in enumerate(positions):
        end = positions[i + 1][0] if i + 1 < len(positions) else len(body)
        content = body[pos:end].strip()
        sections[heading] = content
    return sections


def estimate_tokens(text):
    """Estimate token count using tiktoken if available, else word-count fallback."""
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
    except ImportError:
        return len(text.split())


def maybe_parse_intent_table(section_content):
    """Parse auto-route table rows from Route the Request section."""
    rows = []
    table_pattern = re.compile(
        r"^\|\s*([A-Z]\d+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|",
        re.MULTILINE,
    )
    for m in table_pattern.finditer(section_content):
        rows.append({
            "id": m.group(1),
            "pattern": m.group(2).strip(),
            "action": m.group(3).strip(),
        })
    return rows


def parse_ascii_tree(text):
    """Parse ASCII tree structures into node/branch representations."""
    nodes = []
    current_node = None
    current_branches = []
    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped:
            continue
        # Detect node labels (lines starting with tree chars, ending with ?)
        if re.match(r"^[├└│].*[?]$", stripped) or "──" in stripped:
            if current_node and current_branches:
                nodes.append({
                    "type": "node",
                    "label": current_node,
                    "branches": list(current_branches),
                })
            label = re.sub(r"^[├└│─\s]+", "", stripped)
            current_node = label.rstrip("?")
            current_branches = []
        elif re.match(r"^[├└│]", stripped):
            branch = re.sub(r"^[├└│─\s]+", "", stripped)
            current_branches.append(branch)
        elif current_node is not None:
            current_branches.append(stripped)
    if current_node and current_branches:
        nodes.append({
            "type": "node",
            "label": current_node,
            "branches": list(current_branches),
        })
    return nodes


def parse_ground_rules(section_content):
    """Parse ground rules table into rule structures."""
    rules = []
    # Match table rows: | **R#** | **CONSTRAINT** rest | Trigger: TRIGGER | RESPONSE |
    # Handle multi-line cells by joining continuation lines
    # First, collapse multi-line rows onto single lines
    cleaned = re.sub(r"\n\s*\|", " |", section_content)
    pattern = re.compile(
        r"\|\s*\*\*([R]\d+)\*\*\s*\|"
        r"\s*\*\*(.+?)\*\*[.]?\s*(.+?)\s*\|"
        r"\s*Trigger:\s*(.+?)\s*\|"
        r"\s*(.+?)\s*\|",
    )
    for m in pattern.finditer(cleaned):
        rid = m.group(1)
        constraint = (m.group(2).strip() + ". " + m.group(3).strip()).strip()
        trigger = m.group(4).strip()
        violation = m.group(5).strip()
        # Clean markdown formatting
        constraint = re.sub(r"\*\*", "", constraint).strip()
        trigger = re.sub(r"\*\*", "", trigger).strip()
        violation = re.sub(r"\*\*", "", violation).strip()
        rules.append({
            "id": rid,
            "constraint": constraint[:300],
            "trigger": trigger[:200],
            "violation": violation[:200],
        })
    return rules


def parse_gotchas(section_content):
    """Parse gotchas section extracting dollar amounts and patterns."""
    gotchas = []
    items = re.split(r"\n-\s+", section_content)
    gid = 1
    for item in items:
        if not item.strip():
            continue
        # Skip the section heading
        if item.strip().startswith("## "):
            continue
        costs = re.findall(r"\$(\d[\d,]*(?:\.\d+)?[KMB]?)", item)
        cost = 0
        if costs:
            try:
                c = costs[0].replace(",", "")
                if c.endswith("B"):
                    cost = int(float(c[:-1]) * 1_000_000_000)
                elif c.endswith("M"):
                    cost = int(float(c[:-1]) * 1_000_000)
                elif c.endswith("K"):
                    cost = int(float(c[:-1]) * 1_000)
                else:
                    cost = int(float(c))
            except ValueError:
                pass
        text = re.sub(r"\*\*", "", item)
        text = re.sub(r"\$[\d,]+[KMB]?", "", text)
        text = " ".join(text.split())
        gotchas.append({
            "id": f"G{gid}",
            "cost": cost,
            "pattern": text[:100],
            "text": text[:400],
        })
        gid += 1
    return gotchas


def parse_anti_rationalization(section_content):
    """Parse anti-rationalization table into excuse/reality pairs."""
    excuses = []
    # Pattern: | "rationalization text" | reality text |
    pattern = re.compile(
        r'\|\s*"(.+?)"\s*\|\s*(.+?)\s*\|',
        re.DOTALL,
    )
    idx = 1
    for m in pattern.finditer(section_content):
        excuse = m.group(1).strip()
        reality = m.group(2).strip()
        # Skip header rows
        if excuse.lower() in ("rationalization",) or "---|---" in excuse:
            continue
        excuses.append({"id": str(idx), "pattern": excuse[:200], "reality": reality[:400]})
        idx += 1
    return excuses


def parse_workflow(section_content):
    """Parse core workflow phases from ### Phase N headers."""
    phases = []
    pattern = re.compile(
        r"###\s*Phase\s*(\d+)\s*\(~(\d+)\s*min\)[:]\s*(.+?)\n(.*?)(?=\n###|\Z)",
        re.DOTALL,
    )
    for m in pattern.finditer(section_content):
        phases.append({
            "id": m.group(1),
            "minutes": m.group(2),
            "name": m.group(3).strip(),
            "description": " ".join(m.group(4).strip().split()[:50]),
        })
    return phases


def parse_levels(section_content):
    """Parse operating levels table."""
    levels = []
    pattern = re.compile(
        r"\|\s*\*\*(L\d)[^*]*\*\*\s*\|\s*(.+?)\s*\|",
        re.DOTALL,
    )
    for m in pattern.finditer(section_content):
        lid = re.sub(r"\*\*", "", m.group(1)).strip()
        desc = m.group(2).strip()
        levels.append({"id": lid, "name": desc[:60], "description": desc})
    return levels


def parse_verification(section_content):
    """Parse checklist items from verification section."""
    items = []
    for m in re.finditer(r"-\s*\[[ x]\]\s*(.+)", section_content):
        items.append(m.group(1).strip())
    return items


def parse_cross_skill(section_content):
    """Parse cross-skill coordination tables for upstream/downstream."""
    upstream = []
    up_pattern = re.compile(
        r"\|\s*`([^`]+)`\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|",
        re.DOTALL,
    )
    for m in up_pattern.finditer(section_content):
        name = m.group(1).strip()
        provides = m.group(2).strip()
        when = m.group(3).strip()
        if any(kw in provides for kw in ["Upstream", "Downstream", "Trigger", "What"]):
            continue
        upstream.append({"name": name, "provides": provides, "when": when})
    return {"upstream": upstream, "downstream": []}


def parse_proactive_triggers(section_content):
    """Parse proactive triggers table into rule-like structures."""
    rules = []
    pattern = re.compile(
        r"\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|",
        re.DOTALL,
    )
    idx = 1
    for m in pattern.finditer(section_content):
        trigger_text = m.group(1).strip()
        action = m.group(2).strip()
        why = m.group(3).strip()
        if "Trigger" in trigger_text and "Action" in action:
            continue
        rules.append({
            "id": f"PT{idx}",
            "trigger": trigger_text[:150],
            "constraint": action[:150],
            "violation": why[:150],
        })
        idx += 1
    return rules


def compile_skill(input_path):
    """Compile a single SKILL.md file to minified XML with metadata."""
    md_path = (
        os.path.join(input_path, "SKILL.md")
        if os.path.isdir(input_path)
        else input_path
    )
    if not os.path.isfile(md_path):
        raise FileNotFoundError(f"SKILL.md not found at {md_path}")

    with open(md_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    original_tokens = estimate_tokens(raw_text)

    # Parse frontmatter and body
    frontmatter, body = parse_frontmatter(raw_text)
    skill_name = frontmatter.get(
        "name", os.path.basename(os.path.dirname(md_path))
    )
    skill_version = frontmatter.get("version", "1.0.0")
    skill_author = frontmatter.get("author", "Unknown")
    skill_type = frontmatter.get("type", "general")
    skill_budget = str(frontmatter.get("token_budget", "3000"))

    # Extract markdown sections
    sections = extract_sections(body)

    # Build XML
    root = ET.Element(
        "skill",
        {
            "name": skill_name,
            "version": skill_version,
            "author": skill_author,
            "type": skill_type,
            "budget": skill_budget,
        },
    )

    compiled_sections = []
    trimmed_sections = []

    # ── Route ────────────────────────────────────────────────────────────
    route_content = sections.get("## Route the Request", "")
    if route_content:
        route_el = ET.SubElement(root, "route")
        for intent in maybe_parse_intent_table(route_content):
            ET.SubElement(
                route_el,
                "intent",
                {"id": intent["id"], "pattern": intent["pattern"][:80]},
            ).text = intent["action"][:200]
        compiled_sections.append("route")

    # ── Rules (Ground Rules + Proactive Triggers merged) ─────────────────
    rules_content = sections.get("## Ground Rules", "")
    proactive_content = sections.get("## Proactive Triggers", "")
    if rules_content or proactive_content:
        rules_el = ET.SubElement(root, "rules")
        for rule in parse_ground_rules(rules_content):
            r_el = ET.SubElement(
                rules_el,
                "rule",
                {"id": rule["id"], "trigger": rule["trigger"][:150]},
            )
            ET.SubElement(r_el, "constraint").text = rule["constraint"][:200]
            ET.SubElement(r_el, "violation").text = rule["violation"][:200]
        for pt in parse_proactive_triggers(proactive_content):
            r_el = ET.SubElement(
                rules_el,
                "rule",
                {"id": pt["id"], "trigger": "WHEN " + pt["trigger"][:140]},
            )
            ET.SubElement(r_el, "constraint").text = pt["constraint"][:200]
            ET.SubElement(r_el, "violation").text = pt["violation"][:200]
        compiled_sections.append("rules")

    # ── Decisions ────────────────────────────────────────────────────────
    decisions_content = sections.get("## Decision Trees", "")
    if decisions_content:
        decisions_el = ET.SubElement(root, "decisions")
        sub_trees = re.split(r"\n###\s+", decisions_content)
        tid = 1
        for sub in sub_trees:
            if not sub.strip():
                continue
            # Skip the ## Decision Trees heading itself
            if sub.strip().startswith("## "):
                continue
            lines = sub.split("\n", 1)
            name = lines[0].strip() if lines else f"tree-{tid}"
            content = lines[1] if len(lines) > 1 else ""
            tree_el = ET.SubElement(
                decisions_el,
                "tree",
                {"id": f"D{tid}", "name": name[:60]},
            )
            for node in parse_ascii_tree(content):
                node_el = ET.SubElement(
                    tree_el,
                    "node",
                    {"type": "choice", "label": node["label"][:80]},
                )
                for branch in node["branches"]:
                    ET.SubElement(
                        node_el, "branch", {"condition": branch[:120]}
                    )
            tid += 1
        compiled_sections.append("decisions")

    # ── Gotchas ──────────────────────────────────────────────────────────
    gotchas_content = sections.get("## Gotchas", "")
    if gotchas_content:
        gotchas_el = ET.SubElement(root, "gotchas")
        for g in parse_gotchas(gotchas_content):
            ET.SubElement(
                gotchas_el,
                "gotcha",
                {
                    "id": g["id"],
                    "cost": str(g["cost"]),
                    "pattern": g["pattern"][:120],
                },
            ).text = g["text"][:300]
        compiled_sections.append("gotchas")

    # ── Workflow ─────────────────────────────────────────────────────────
    workflow_content = sections.get("## Core Workflow", "")
    if workflow_content:
        workflow_el = ET.SubElement(root, "workflow")
        for phase in parse_workflow(workflow_content):
            ET.SubElement(
                workflow_el,
                "phase",
                {
                    "id": phase["id"],
                    "minutes": phase["minutes"],
                    "name": phase["name"][:60],
                },
            ).text = phase["description"][:200]
        compiled_sections.append("workflow")

    # ── Levels ───────────────────────────────────────────────────────────
    levels_content = sections.get("## Operating at Different Levels", "")
    if levels_content:
        levels_el = ET.SubElement(root, "levels")
        for lvl in parse_levels(levels_content):
            ET.SubElement(
                levels_el,
                "level",
                {"id": lvl["id"], "name": lvl["name"]},
            ).text = lvl["description"][:200]
        compiled_sections.append("levels")

    # ── Anti-Rationalization ─────────────────────────────────────────────
    anti_content = sections.get("## Anti-Rationalization", "")
    if anti_content:
        anti_el = ET.SubElement(root, "anti_rationalization")
        for excuse in parse_anti_rationalization(anti_content):
            ET.SubElement(
                anti_el,
                "excuse",
                {
                    "id": excuse["id"],
                    "pattern": excuse["pattern"][:120],
                },
            ).text = excuse["reality"][:300]
        compiled_sections.append("anti_rationalization")

    # ── Chain (Cross-Skill Coordination) ─────────────────────────────────
    chain_fm = frontmatter.get("chain", None)
    cross_skill = sections.get("## Cross-Skill Coordination", "")
    if chain_fm or cross_skill:
        chain_el = ET.SubElement(root, "chain")
        if isinstance(chain_fm, dict):
            consumes = chain_fm.get("consumes_from", [])
            feeds = chain_fm.get("feeds_into", [])
            if isinstance(consumes, list):
                for c in consumes:
                    ET.SubElement(chain_el, "upstream").text = str(c)
            if isinstance(feeds, list):
                for f in feeds:
                    ET.SubElement(chain_el, "downstream").text = str(f)
        cs_data = parse_cross_skill(cross_skill)
        for up in cs_data.get("upstream", [])[:15]:
            ET.SubElement(
                chain_el, "upstream", {"skill": up["name"]}
            ).text = up.get("provides", "")[:100]
        compiled_sections.append("chain")

    # ── Checklist (Verification) ─────────────────────────────────────────
    verification_content = sections.get("## Verification", "")
    if verification_content:
        checklist_el = ET.SubElement(root, "checklist")
        for item in parse_verification(verification_content):
            ET.SubElement(checklist_el, "item").text = item[:200]
        compiled_sections.append("checklist")

    # ── Identify trimmed sections ────────────────────────────────────────
    trim_map = [
        ("## The Expert.s Mindset", "mindset"),
        ("## Deliberate Practice", "practice"),
        ("## References", "references"),
        ("## What Good Looks Like", "what_good_looks_like"),
        ("## When to Use", "when_to_use"),
    ]
    trimmed_sections = [name for heading, name in trim_map if heading in sections]

    # ── Generate XML ─────────────────────────────────────────────────────
    ET.indent(root, space="  ")
    xml_str = ET.tostring(root, encoding="unicode", xml_declaration=True)
    # Minify: collapse whitespace between tags
    xml_str = re.sub(r">\s+<", "><", xml_str)
    xml_str = re.sub(r"  +", " ", xml_str)

    compiled_tokens = estimate_tokens(xml_str)
    reduction = (
        round((1 - compiled_tokens / original_tokens) * 100, 1)
        if original_tokens > 0
        else 0
    )

    metadata = {
        "name": skill_name,
        "original_tokens": original_tokens,
        "compiled_tokens": compiled_tokens,
        "reduction_pct": reduction,
        "sections_compiled": compiled_sections,
        "sections_trimmed": trimmed_sections,
        "compiled_at": datetime.datetime.utcnow().strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        ),
    }

    return {"name": skill_name, "xml": xml_str, "metadata": metadata}


# ─── CLI Entry Points ────────────────────────────────────────────────────────

def cmd_compile():
    """Compile a single skill directory."""
    input_path = sys.argv[2]
    output_dir = sys.argv[3]
    result = compile_skill(input_path)

    skill_out = os.path.join(output_dir, result["name"])
    os.makedirs(skill_out, exist_ok=True)

    xml_path = os.path.join(skill_out, "skill.xml")
    with open(xml_path, "w", encoding="utf-8") as f:
        f.write(result["xml"])

    meta_path = os.path.join(skill_out, "metadata.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(result["metadata"], f, indent=2)

    # Print summary to stdout for bash to capture
    print(json.dumps({
        "name": result["name"],
        "original": result["metadata"]["original_tokens"],
        "compiled": result["metadata"]["compiled_tokens"],
        "reduction": result["metadata"]["reduction_pct"],
    }))


def cmd_verify():
    """Verify all compiled output."""
    output_dir = sys.argv[2]
    errors = []
    total_skills = 0
    total_original = 0
    total_compiled = 0

    for dirpath, _, files in os.walk(output_dir):
        if "metadata.json" not in files:
            continue
        meta_path = os.path.join(dirpath, "metadata.json")
        xml_path = os.path.join(dirpath, "skill.xml")
        try:
            with open(meta_path) as f:
                meta = json.load(f)
            with open(xml_path) as f:
                xml_content = f.read()
            # Validate XML well-formedness
            try:
                ET.fromstring(xml_content)
            except ET.ParseError as e:
                errors.append(f"XML malformed in {dirpath}: {e}")
                continue

            total_skills += 1
            total_original += meta.get("original_tokens", 0)
            total_compiled += meta.get("compiled_tokens", 0)

        except Exception as e:
            errors.append(f"Error processing {dirpath}: {e}")

    avg_reduction = (
        round((1 - total_compiled / total_original) * 100, 1)
        if total_original > 0
        else 0
    )

    print(
        json.dumps(
            {
                "total_skills": total_skills,
                "total_original_tokens": total_original,
                "total_compiled_tokens": total_compiled,
                "avg_reduction_pct": avg_reduction,
                "errors": errors,
            },
            indent=2,
        )
    )

    sys.exit(0 if not errors else 1)


def cmd_estimate():
    """Quick token estimate for a file."""
    path = sys.argv[2]
    with open(path, "r") as f:
        text = f.read()
    tokens = estimate_tokens(text)
    print(tokens)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python3 _compile_skill.py <command> [args]",
            file=sys.stderr,
        )
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "compile":
        cmd_compile()
    elif cmd == "verify":
        cmd_verify()
    elif cmd == "estimate":
        cmd_estimate()
    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)
