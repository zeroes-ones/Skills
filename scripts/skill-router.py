#!/usr/bin/env python3
"""
Dynamic Skill Routing Runtime — Logic Layer of the 10/10 Architecture Stack
=============================================================================
Translates the 1,130-edge markdown chain graph into an executable DAG.

Features:
- --stats: Graph statistics (total skills, edges, orphans)
- --graph: Full DAG as JSON
- --upstream SKILL: Show all upstream dependencies
- --downstream SKILL: Show all downstream consumers
- --lite SKILL: Token-efficient Route+Ground Rules only
- --list: All available skills
- --portability TARGET: Filter by Claude/Copilot/Gemini compatibility
"""
import os, sys, yaml, json, argparse, re
from pathlib import Path
from collections import defaultdict

SKILLS_DIR = Path(__file__).parent.parent / 'skills'

def load_skill_metadata(skill_path):
    with open(skill_path) as f:
        content = f.read()
    parts = content.split('---', 2)
    if len(parts) < 3:
        return None
    try:
        return yaml.safe_load(parts[1])
    except:
        return None

def build_graph():
    graph = {}
    name_to_path = {}
    for root, dirs, files in os.walk(SKILLS_DIR):
        for f in files:
            if f == 'SKILL.md':
                if '00-framework' in root:
                    continue
                path = os.path.join(root, f)
                meta = load_skill_metadata(path)
                if not meta or 'name' not in meta:
                    continue
                name = meta['name']
                chain = meta.get('chain', {})
                graph[name] = {
                    'consumes_from': chain.get('consumes_from', []),
                    'feeds_into': chain.get('feeds_into', []),
                    'description': meta.get('description', ''),
                    'portability': meta.get('portability', 'any'),
                    'path': path,
                }
                name_to_path[name] = path
    return graph, name_to_path

def get_upstream(skill_name, graph, depth=5, visited=None):
    if visited is None:
        visited = set()
    if skill_name not in graph or depth <= 0 or skill_name in visited:
        return []
    visited.add(skill_name)
    upstream = []
    for u in graph[skill_name].get('consumes_from', []):
        if u in graph:
            upstream.append(u)
            upstream.extend(get_upstream(u, graph, depth - 1, visited))
    return list(set(upstream))

def get_downstream(skill_name, graph, depth=5, visited=None):
    if visited is None:
        visited = set()
    if skill_name not in graph or depth <= 0 or skill_name in visited:
        return []
    visited.add(skill_name)
    downstream = []
    for d in graph[skill_name].get('feeds_into', []):
        if d in graph:
            downstream.append(d)
            downstream.extend(get_downstream(d, graph, depth - 1, visited))
    return list(set(downstream))

def get_lite_content(skill_path):
    with open(skill_path) as f:
        content = f.read()
    parts = content.split('---', 2)
    if len(parts) < 3:
        return content[:2000]
    body = parts[2]
    route = ''
    rules = ''
    route_match = re.search(r'## Route the Request\n(.*?)(?=\n## )', body, re.DOTALL)
    if route_match:
        route = route_match.group(0)
    rules_match = re.search(r'## Ground Rules[^\n]*\n(.*?)(?=\n## )', body, re.DOTALL)
    if rules_match:
        rules = rules_match.group(0)
    return f"{route}\n\n{rules}"

def fuzzy_find(skill_name, graph):
    skill_lower = skill_name.lower().strip()
    for name in graph:
        if skill_lower == name.lower() or skill_lower in name.lower():
            return name
    matches = [n for n in graph if skill_lower.replace('-', '') in n.replace('-', '')]
    if len(matches) == 1:
        return matches[0]
    return None

def main():
    parser = argparse.ArgumentParser(description='Skill Router — Dynamic Skill Graph Orchestrator')
    parser.add_argument('query', nargs='?', help='Skill name or search term')
    parser.add_argument('--upstream', action='store_true', help='Show upstream dependencies')
    parser.add_argument('--downstream', action='store_true', help='Show downstream consumers')
    parser.add_argument('--lite', action='store_true', help='Output Route+Ground Rules (token-efficient)')
    parser.add_argument('--list', action='store_true', help='List all available skills')
    parser.add_argument('--graph', action='store_true', help='Output full DAG as JSON')
    parser.add_argument('--stats', action='store_true', help='Show graph statistics')
    parser.add_argument('--portability', default=None, help='Filter by portability target')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    graph, name_to_path = build_graph()

    if args.stats:
        total = len(graph)
        with_up = sum(1 for v in graph.values() if v['consumes_from'])
        with_down = sum(1 for v in graph.values() if v['feeds_into'])
        total_edges = sum(len(v['consumes_from']) + len(v['feeds_into']) for v in graph.values())
        orphans = sum(1 for v in graph.values() if not v['consumes_from'] and not v['feeds_into'])
        stats = {
            'total_skills': total,
            'skills_with_upstream': with_up,
            'skills_with_downstream': with_down,
            'total_edges': total_edges,
            'orphan_skills': orphans,
            'graph_density': round(total_edges / max(total, 1), 2),
        }
        print(json.dumps(stats, indent=2))
        return

    if args.graph:
        out = {}
        for name, data in graph.items():
            if args.portability and args.portability not in data['portability']:
                continue
            out[name] = {'consumes_from': data['consumes_from'], 'feeds_into': data['feeds_into']}
        print(json.dumps(out, indent=2))
        return

    if args.list:
        skills = sorted(graph.keys())
        if args.portability:
            skills = [s for s in skills if args.portability in graph[s]['portability']]
        if args.json:
            print(json.dumps(skills))
        else:
            print(f"\n{len(skills)} skills available:\n")
            for s in skills:
                print(f"  {s}")
        return

    if not args.query:
        parser.print_help()
        return

    match = fuzzy_find(args.query, graph)
    if not match:
        print(f"Skill '{args.query}' not found in graph", file=sys.stderr)
        sys.exit(1)

    data = graph[match]

    if args.lite:
        print(f"# Lite: {match}\n")
        print(get_lite_content(data['path']))
        return

    if args.upstream:
        upstream = get_upstream(match, graph)
        if args.json:
            print(json.dumps(upstream))
        else:
            print(f"\nUpstream for '{match}' ({len(upstream)} total):\n")
            for u in sorted(upstream):
                desc = graph[u]['description'][:100] if u in graph else ''
                print(f"  <- {u}: {desc}")
        return

    if args.downstream:
        downstream = get_downstream(match, graph)
        if args.json:
            print(json.dumps(downstream))
        else:
            print(f"\nDownstream from '{match}' ({len(downstream)} total):\n")
            for d in sorted(downstream):
                desc = graph[d]['description'][:100] if d in graph else ''
                print(f"  -> {d}: {desc}")
        return

    upstream = get_upstream(match, graph)
    downstream = get_downstream(match, graph)
    print(f"\n=== {match} ===")
    print(f"Portability: {data['portability']}")
    print(f"Description: {data['description'][:200]}")
    print(f"\nUpstream ({len(upstream)}):")
    for u in sorted(upstream)[:20]:
        print(f"  <- {u}")
    if len(upstream) > 20:
        print(f"  ... and {len(upstream) - 20} more")
    print(f"\nDownstream ({len(downstream)}):")
    for d in sorted(downstream)[:20]:
        print(f"  -> {d}")
    if len(downstream) > 20:
        print(f"  ... and {len(downstream) - 20} more")
    print(f"\nPath: {data['path']}")

if __name__ == '__main__':
    main()
