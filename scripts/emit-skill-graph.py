#!/usr/bin/env python3
"""
Emit the skill-chain graph for the visual graph explorer.

Reads every skills/<domain>/<name>/SKILL.md, extracts the YAML `chain:`
frontmatter (consumes_from / feeds_into), computes a deterministic
force-directed layout, and writes:

  docs/graph-explorer/skill-graph.json   — machine-readable graph (nodes+links)
  docs/graph-explorer/index.html         — self-contained explorer page
                                           (built from template.html; embeds the
                                           graph so it works from file://)

Mirrors the parsing of scripts/validate_chains.py (needs PyYAML, which GitHub
ubuntu runners ship). Deterministic: no timestamps, fixed random seed — reruns
are byte-identical, which the CI freshness gate relies on.

Usage:
    python3 scripts/emit-skill-graph.py            # write outputs
    python3 scripts/emit-skill-graph.py --check    # verify committed outputs are fresh
    python3 scripts/emit-skill-graph.py --json-only
"""

import os
import re
import sys
import json
import math
import random
import argparse
import tempfile
import filecmp

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_DIR = os.path.join(ROOT, "skills")
OUT_DIR = os.path.join(ROOT, "docs", "graph-explorer")
TEMPLATE = os.path.join(OUT_DIR, "template.html")
INDEX_HTML = os.path.join(OUT_DIR, "index.html")
GRAPH_JSON = os.path.join(OUT_DIR, "skill-graph.json")
SEED = 42
LAYOUT_WIDTH = 1600.0
LAYOUT_HEIGHT = 1150.0
LAYOUT_ITERS = 220
DESC_MAX = 280


def find_skills():
    """{skill_name: {'path': abs, 'domain': '03-design', 'rel': 'skills/03-design/name'}}"""
    out = {}
    for root, dirs, files in os.walk(SKILLS_DIR):
        if "SKILL.md" in files:
            path = os.path.join(root, "SKILL.md")
            name = os.path.basename(root)
            domain = os.path.basename(os.path.dirname(root))
            out[name] = {
                "path": path,
                "domain": domain,
                "rel": os.path.relpath(root, ROOT).replace(os.sep, "/"),
            }
    return out


def parse_frontmatter(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    parts = re.split(r"^---\s*$", content, maxsplit=2, flags=re.MULTILINE)
    if len(parts) < 3:
        return {}
    try:
        fm = yaml.safe_load(parts[1])
    except Exception:
        return {}
    return fm if isinstance(fm, dict) else {}


def chain_lists(fm):
    chain = fm.get("chain") or {}
    if not isinstance(chain, dict):
        chain = {}
    consumes = chain.get("consumes_from") or []
    feeds = chain.get("feeds_into") or []
    return [x for x in (consumes if isinstance(consumes, list) else []) if isinstance(x, str)], \
           [x for x in (feeds if isinstance(feeds, list) else []) if isinstance(x, str)]


def domain_label(domain):
    return re.sub(r"^\d+-", "", domain)


def force_layout(names, links):
    """Deterministic Fruchterman–Reingold. Returns {name: (x, y)}."""
    rng = random.Random(SEED)
    n = len(names)
    idx = {nm: i for i, nm in enumerate(names)}
    pos = {}
    for nm in names:
        pos[nm] = [rng.uniform(0, LAYOUT_WIDTH), rng.uniform(0, LAYOUT_HEIGHT)]
    if n == 1:
        return {names[0]: (LAYOUT_WIDTH / 2, LAYOUT_HEIGHT / 2)}

    k = math.sqrt(LAYOUT_WIDTH * LAYOUT_HEIGHT / n)
    adj = [[] for _ in range(n)]
    for a, b in links:
        i, j = idx[a], idx[b]
        adj[i].append(j)
        adj[j].append(i)
    temp = max(LAYOUT_WIDTH, LAYOUT_HEIGHT) / 10.0

    for _ in range(LAYOUT_ITERS):
        disp = [[0.0, 0.0] for _ in range(n)]
        # repulsion (O(n^2) — 297 nodes is fine)
        for i in range(n):
            for j in range(i + 1, n):
                dx = pos[names[i]][0] - pos[names[j]][0]
                dy = pos[names[i]][1] - pos[names[j]][1]
                dist = math.hypot(dx, dy) or 1e-9
                force = k * k / dist
                fx, fy = force * dx / dist, force * dy / dist
                disp[i][0] += fx
                disp[i][1] += fy
                disp[j][0] -= fx
                disp[j][1] -= fy
        # attraction along edges
        for i in range(n):
            for j in adj[i]:
                if j <= i:
                    continue
                dx = pos[names[i]][0] - pos[names[j]][0]
                dy = pos[names[i]][1] - pos[names[j]][1]
                dist = math.hypot(dx, dy) or 1e-9
                force = dist * dist / k
                fx, fy = force * dx / dist, force * dy / dist
                disp[i][0] -= fx
                disp[i][1] -= fy
                disp[j][0] += fx
                disp[j][1] += fy
        # apply with cooling + light centering gravity
        for i in range(n):
            d = math.hypot(disp[i][0], disp[i][1]) or 1e-9
            step = min(d, temp)
            pos[names[i]][0] += disp[i][0] / d * step
            pos[names[i]][1] += disp[i][1] / d * step
            pos[names[i]][0] += (LAYOUT_WIDTH / 2 - pos[names[i]][0]) * 0.002
            pos[names[i]][1] += (LAYOUT_HEIGHT / 2 - pos[names[i]][1]) * 0.002
        temp *= 0.97

    # normalize into a margin box
    xs = [pos[nm][0] for nm in names]
    ys = [pos[nm][1] for nm in names]
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)
    m = 60
    sx = (LAYOUT_WIDTH - 2 * m) / (maxx - minx or 1)
    sy = (LAYOUT_HEIGHT - 2 * m) / (maxy - miny or 1)
    scale = min(sx, sy)
    cx = (LAYOUT_WIDTH - (maxx - minx) * scale) / 2
    cy = (LAYOUT_HEIGHT - (maxy - miny) * scale) / 2
    return {
        nm: (cx + (pos[nm][0] - minx) * scale, cy + (pos[nm][1] - miny) * scale)
        for nm in names
    }


def build_graph():
    skills = find_skills()
    names = sorted(skills)
    nodes = {}
    for nm in names:
        info = skills[nm]
        fm = parse_frontmatter(info["path"])
        desc = (fm.get("description") or "").strip()
        desc = re.sub(r"\s+", " ", desc)[:DESC_MAX]
        nodes[nm] = {
            "id": nm,
            "domain": info["domain"],
            "label": domain_label(info["domain"]),
            "desc": desc,
            "type": fm.get("type") or "",
            "path": info["rel"],
        }

    # Directed arrows: source feeds target. Both directions of the chain
    # contract (feeds_into on the producer, consumes_from on the consumer)
    # describe the same directed pair, so collect into a set.
    arrows = set()
    dangling = []
    for nm in names:
        fm = parse_frontmatter(skills[nm]["path"])
        consumes, feeds = chain_lists(fm)
        for t in feeds:
            if t in nodes:
                arrows.add((nm, t))
            else:
                dangling.append((nm, "feeds_into", t))
        for c in consumes:
            if c in nodes:
                arrows.add((c, nm))
            else:
                dangling.append((nm, "consumes_from", c))

    undirected = {tuple(sorted((a, b))) for a, b in arrows}
    links = [{"s": a, "b": b} for a, b in sorted(undirected)]
    arrow_pairs = sorted(arrows)
    arrow_idx = set(arrow_pairs)

    # per-node link direction for arrow rendering
    for lk in links:
        s, t = lk["s"], lk["b"]
        fwd = (s, t) in arrow_idx
        rev = (t, s) in arrow_idx
        lk["dir"] = "both" if (fwd and rev) else ("in" if rev else "out")

    pos = force_layout(names, [(lk["s"], lk["b"]) for lk in links])
    for nm in names:
        nodes[nm]["x"] = round(pos[nm][0], 1)
        nodes[nm]["y"] = round(pos[nm][1], 1)

    degree = {nm: 0 for nm in names}
    for lk in links:
        degree[lk["s"]] += 1
        degree[lk["b"]] += 1
    hubs = sorted(degree.items(), key=lambda kv: -kv[1])[:15]

    domains = {}
    for nm in names:
        domains.setdefault(nodes[nm]["label"], []).append(nm)

    stats = {
        "nodes": len(names),
        "directed_edges": len(arrows),
        "undirected_edges": len(links),
        "dangling_refs": len(dangling),
        "avg_degree": round(2.0 * len(links) / max(1, len(names)), 2),
        "hubs": [{"id": nm, "degree": d} for nm, d in hubs],
        "domains": {label: len(v) for label, v in sorted(domains.items())},
    }
    graph = {
        "schema": 1,
        "stats": stats,
        "nodes": [nodes[nm] for nm in names],
        "links": links,
    }
    return graph, dangling


def render_index(graph):
    if not os.path.isfile(TEMPLATE):
        print(f"ERROR: template not found at {TEMPLATE}", file=sys.stderr)
        sys.exit(1)
    with open(TEMPLATE, "r", encoding="utf-8") as f:
        html = f.read()
    data = json.dumps(graph, ensure_ascii=False, separators=(",", ":"))
    data = data.replace("<", "\\u003c")  # safe inside <script> block
    if "__GRAPH_JSON__" not in html:
        print("ERROR: template missing __GRAPH_JSON__ placeholder", file=sys.stderr)
        sys.exit(1)
    return html.replace("__GRAPH_JSON__", data)


def main():
    ap = argparse.ArgumentParser(description="Emit skill-chain graph for the explorer")
    ap.add_argument("--check", action="store_true",
                    help="verify committed docs/graph-explorer outputs are fresh (exit 1 on drift)")
    ap.add_argument("--json-only", action="store_true", help="only write skill-graph.json")
    args = ap.parse_args()

    graph, dangling = build_graph()
    if dangling:
        print(f"WARNING: {len(dangling)} dangling chain refs skipped:", file=sys.stderr)
        for who, kind, ref in dangling[:10]:
            print(f"  {who} -> {kind}: {ref}", file=sys.stderr)

    os.makedirs(OUT_DIR, exist_ok=True)
    json_bytes = (json.dumps(graph, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    index_bytes = render_index(graph).encode("utf-8")

    if args.check:
        expected = {GRAPH_JSON: json_bytes, INDEX_HTML: index_bytes}
        drifted = []
        for path, content in expected.items():
            if not os.path.isfile(path):
                drifted.append(f"{os.path.relpath(path, ROOT)}: MISSING")
                continue
            with open(path, "rb") as f:
                if f.read() != content:
                    drifted.append(f"{os.path.relpath(path, ROOT)}: STALE")
        if drifted:
            print("Graph explorer outputs are stale. Regenerate with:")
            print("  python3 scripts/emit-skill-graph.py")
            for line in drifted:
                print(f"  - {line}")
            sys.exit(1)
        print("✓ graph explorer outputs are fresh (index.html + skill-graph.json)")
        return

    with open(GRAPH_JSON, "w", encoding="utf-8") as f:
        f.write(json_bytes.decode("utf-8"))
    if not args.json_only:
        with open(INDEX_HTML, "w", encoding="utf-8") as f:
            f.write(index_bytes.decode("utf-8"))

    s = graph["stats"]
    print(f"✓ wrote {os.path.relpath(GRAPH_JSON, ROOT)} and "
          f"{os.path.relpath(INDEX_HTML, ROOT) if not args.json_only else '(json only)'}")
    print(f"  nodes={s['nodes']}  directed_edges={s['directed_edges']}  "
          f"undirected_edges={s['undirected_edges']}  avg_degree={s['avg_degree']}")
    print(f"  domains={len(s['domains'])}  dangling_refs={s['dangling_refs']}")
    print("  top hubs:", ", ".join(f"{h['id']}({h['degree']})" for h in s["hubs"][:8]))


if __name__ == "__main__":
    main()
