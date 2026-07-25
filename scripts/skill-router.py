#!/usr/bin/env python3
"""
Dynamic Skill Routing Runtime — Logic Layer of the 10/10 Architecture Stack
=============================================================================
Translates the 1,130-edge markdown chain graph into an executable DAG.
Instead of relying on the LLM to read markdown and figure out transitions,
this orchestrator programmatically enforces skill routing, dependency
resolution, and state handoff.

Architecture:  10/10 Maturity Stack
  ├── Structural Layer: 1,130-edge Graph + 4K Token Cap ✅ (SKILL.md files)
  ├── Logic Layer:      Python Orchestrator + Dynamic Routers    (this file)
  ├── Validation Layer:  Evals Harness + LLM Drift Monitors      (evals/)
  └── Ecosystem Layer:   Open-source battle testing              (CI/CD + model matrix)

Usage:
    python scripts/skill-router.py "Build a REST API with JWT auth"
    python scripts/skill-router.py --json "I need threat modeling for my app"
    python scripts/skill-router.py --chain "ceo-strategist -> product-manager"
    python scripts/skill-router.py --graph    # Print full DAG stats
    python scripts/skill-router.py --state    # Show state ledger

Exit codes: 0=route found, 1=no route, 2=graph error
"""

import json
import os
import re
import sys
import yaml
from collections import defaultdict, deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# ─── Configuration ───────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
STATE_LEDGER = REPO_ROOT / ".skills-compiled" / "state-ledger.json"
STATE_LEDGER.parent.mkdir(parents=True, exist_ok=True)

# Directories that use numbered prefixes in headings (validator-exempt)
NUMBERED_HEADING_DIRS = {"00-framework"}

# ─── Data Structures ─────────────────────────────────────────────────────────

@dataclass
class SkillNode:
    """A single skill in the routing graph."""
    id: str                          # e.g., "backend-developer"
    path: Path                       # filesystem path
    name: str                        # display name from frontmatter
    description: str                 # trigger description
    chain_consumes: list[str] = field(default_factory=list)
    chain_feeds: list[str] = field(default_factory=list)
    triggers: list[str] = field(default_factory=list)
    anti_triggers: list[str] = field(default_factory=list)
    token_budget: int = 500
    portability: str = ""
    domain: str = ""                 # e.g., "05-development"


@dataclass
class RouteResult:
    """Result of a routing query."""
    primary_skill: SkillNode
    confidence: float               # 0.0-1.0
    upstream_skills: list[SkillNode] = field(default_factory=list)
    downstream_skills: list[SkillNode] = field(default_factory=list)
    chain_path: list[str] = field(default_factory=list)
    rationale: str = ""


class StateLedger:
    """Records every micro-decision gate passed across the 1,130-chain edges.
    Prevents context drift when multiple agents interact with the workspace."""

    def __init__(self, path: Path = STATE_LEDGER):
        self.path = path
        self.data = self._load()

    def _load(self) -> dict:
        if self.path.exists():
            with open(self.path) as f:
                return json.load(f)
        return {"version": "1.0.0", "transitions": [], "decisions": [],
                "current_skill": None, "session_id": None}

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=2, default=str)

    def record_transition(self, from_skill: str, to_skill: str, trigger: str):
        self.data["transitions"].append({
            "from": from_skill, "to": to_skill, "trigger": trigger,
            "timestamp": _timestamp()
        })
        self.data["current_skill"] = to_skill
        self.save()

    def record_decision(self, gate: str, choice: str, rationale: str):
        self.data["decisions"].append({
            "gate": gate, "choice": choice, "rationale": rationale,
            "timestamp": _timestamp()
        })
        self.save()

    def get_current_skill(self) -> Optional[str]:
        return self.data.get("current_skill")

    def get_recent_transitions(self, n: int = 10) -> list[dict]:
        return self.data.get("transitions", [])[-n:]


def _timestamp() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()


# ─── Graph Builder ───────────────────────────────────────────────────────────

class SkillGraph:
    """Directed graph of all skills with chain: consumes/feeds edges."""

    def __init__(self, skills_dir: Path = SKILLS_DIR):
        self.skills_dir = skills_dir
        self.nodes: dict[str, SkillNode] = {}
        self._adj_out: dict[str, list[str]] = defaultdict(list)  # A -> B means A feeds B
        self._adj_in: dict[str, list[str]] = defaultdict(list)   # B -> A means B consumes A
        self._trigger_index: dict[str, list[str]] = defaultdict(list)  # trigger word -> skill ids
        self._build()

    def _parse_frontmatter_yaml(self, filepath: Path) -> Optional[dict]:
        """Extract YAML frontmatter between --- delimiters."""
        try:
            with open(filepath) as f:
                content = f.read()
        except (OSError, UnicodeDecodeError):
            return None

        parts = content.split("---", 2)
        if len(parts) < 3:
            return None
        try:
            return yaml.safe_load(parts[1]) or {}
        except yaml.YAMLError:
            return None

    def _extract_triggers(self, description: str) -> tuple[list[str], list[str]]:
        """Parse 'Use when...' triggers and 'Do NOT use for...' anti-triggers."""
        triggers = []
        anti_triggers = []

        use_match = re.search(r'Use when\s*(.*?)(?:\.\s*Handles|$)', description, re.IGNORECASE)
        if use_match:
            # Split on commas, extract key phrases
            phrases = re.findall(r'[\w\s-]+(?=,|$)', use_match.group(1))
            triggers = [p.strip().lower() for p in phrases if len(p.strip()) > 3]

        not_match = re.search(r'Do NOT use for\s*(.*?)(?:\.|$)', description, re.IGNORECASE)
        if not_match:
            phrases = re.findall(r'[\w\s-]+(?=,|$)', not_match.group(1))
            anti_triggers = [p.strip().lower() for p in phrases if len(p.strip()) > 3]

        return triggers, anti_triggers

    def _parse_chain(self, chain: dict) -> tuple[list[str], list[str]]:
        """Parse chain: consumes_from and feeds_into from frontmatter."""
        consumes = []
        feeds = []
        if isinstance(chain, dict):
            raw_consumes = chain.get("consumes_from", chain.get("consumes", []))
            raw_feeds = chain.get("feeds_into", chain.get("feeds", []))
            consumes = [c.strip().lower().replace(" ", "-") for c in raw_consumes if c]
            feeds = [f.strip().lower().replace(" ", "-") for f in raw_feeds if f]
        return consumes, feeds

    def _build(self):
        """Scan all SKILL.md files and construct the directed graph."""
        if not self.skills_dir.exists():
            return

        for skill_md in sorted(self.skills_dir.rglob("SKILL.md")):
            rel_path = skill_md.relative_to(self.skills_dir)
            parts = rel_path.parts

            # Skip framework directory (special handling)
            if parts[0] in NUMBERED_HEADING_DIRS:
                continue

            skill_id = parts[-2] if len(parts) >= 2 else skill_md.parent.name
            domain = parts[0] if parts else ""

            fm = self._parse_frontmatter_yaml(skill_md)
            if not fm:
                continue

            name = fm.get("name", skill_id)
            description = fm.get("description", "")
            triggers, anti_triggers = self._extract_triggers(description)
            consumes, feeds = self._parse_chain(fm.get("chain", {}))
            token_budget = fm.get("token_budget", 500)
            portability = fm.get("portability", "")

            node = SkillNode(
                id=skill_id,
                path=skill_md,
                name=name,
                description=description,
                chain_consumes=consumes,
                chain_feeds=feeds,
                triggers=triggers,
                anti_triggers=anti_triggers,
                token_budget=token_budget,
                portability=portability,
                domain=domain,
            )

            self.nodes[skill_id] = node

            # Build adjacency
            for feed_target in feeds:
                self._adj_out[skill_id].append(feed_target)
                self._adj_in[feed_target].append(skill_id)

            # Build trigger index
            for trigger in triggers:
                self._trigger_index[trigger].append(skill_id)

    def get_node(self, skill_id: str) -> Optional[SkillNode]:
        return self.nodes.get(skill_id)

    def get_upstream(self, skill_id: str, depth: int = 1) -> list[SkillNode]:
        """Get skills this skill consumes from (BFS up to depth)."""
        result = []
        visited = {skill_id}
        queue = deque([(skill_id, 0)])

        # Start from nodes that feed INTO this skill
        for source in self._adj_in.get(skill_id, []):
            if source not in visited and source in self.nodes:
                visited.add(source)
                result.append(self.nodes[source])
                if depth > 1:
                    queue.append((source, 1))

        while queue:
            current, d = queue.popleft()
            if d >= depth:
                continue
            for source in self._adj_in.get(current, []):
                if source not in visited and source in self.nodes:
                    visited.add(source)
                    result.append(self.nodes[source])
                    queue.append((source, d + 1))

        return result

    def get_downstream(self, skill_id: str, depth: int = 1) -> list[SkillNode]:
        """Get skills this skill feeds into (BFS up to depth)."""
        result = []
        visited = {skill_id}
        queue = deque([(skill_id, 0)])

        for target in self._adj_out.get(skill_id, []):
            if target not in visited and target in self.nodes:
                visited.add(target)
                result.append(self.nodes[target])
                if depth > 1:
                    queue.append((target, 1))

        while queue:
            current, d = queue.popleft()
            if d >= depth:
                continue
            for target in self._adj_out.get(current, []):
                if target not in visited and target in self.nodes:
                    visited.add(target)
                    result.append(self.nodes[target])
                    queue.append((target, d + 1))

        return result

    def find_chain_path(self, from_skill: str, to_skill: str) -> Optional[list[str]]:
        """BFS shortest path between two skills in the chain graph."""
        if from_skill not in self.nodes or to_skill not in self.nodes:
            return None

        visited = {from_skill}
        queue = deque([(from_skill, [from_skill])])

        while queue:
            current, path = queue.popleft()
            if current == to_skill:
                return path

            for neighbor in self._adj_out.get(current, []):
                if neighbor not in visited and neighbor in self.nodes:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return None

    def stats(self) -> dict:
        """Return graph statistics."""
        edges_out = sum(len(v) for v in self._adj_out.values())
        edges_in = sum(len(v) for v in self._adj_in.values())
        orphaned = [nid for nid in self.nodes
                    if not self._adj_in.get(nid) and not self._adj_out.get(nid)]
        return {
            "total_nodes": len(self.nodes),
            "total_edges": edges_out,  # directed edges
            "orphaned_skills": len(orphaned),
            "orphaned_list": orphaned[:10],
            "max_out_degree": max((len(v) for v in self._adj_out.values()), default=0),
            "max_in_degree": max((len(v) for v in self._adj_in.values()), default=0),
            "trigger_index_size": len(self._trigger_index),
            "domains": len({n.domain for n in self.nodes.values()}),
        }


# ─── Router ──────────────────────────────────────────────────────────────────

class SkillRouter:
    """Routes user queries to the correct skill using trigger matching and
    chain graph traversal. Enforces transitions programmatically."""

    # Curated keyword-to-skill mappings for high-precision routing
    # Built from analyzing 1062 trigger keywords across 183 skills
    CURATED_ROUTES: dict[str, list[str]] = {
        "api": ["api-designer", "backend-developer", "secure-api-design"],
        "rest": ["api-designer", "backend-developer"],
        "graphql": ["api-designer"],
        "jwt": ["backend-developer", "secure-api-design", "security-reviewer"],
        "auth": ["backend-developer", "security-reviewer", "iam-architect"],
        "database": ["database-designer", "database-reliability-engineer"],
        "schema": ["database-designer", "codebase-design"],
        "sql": ["database-designer"],
        "nosql": ["database-designer"],
        "threat model": ["security-reviewer", "security-engineer"],
        "vulnerability": ["vulnerability-management", "security-reviewer"],
        "penetration test": ["offensive-security", "security-reviewer"],
        "owasp": ["security-reviewer", "appsec-engineer"],
        "kubernetes": ["docker-kubernetes", "cloud-architect", "devops-engineer"],
        "docker": ["docker-kubernetes", "devops-engineer"],
        "terraform": ["devops-engineer", "cloud-architect"],
        "ci/cd": ["ci-cd-builder", "devops-engineer"],
        "pipeline": ["ci-cd-builder", "devops-engineer"],
        "react": ["frontend-developer"],
        "next.js": ["frontend-developer", "fullstack-developer"],
        "vue": ["frontend-developer"],
        "frontend": ["frontend-developer"],
        "backend": ["backend-developer"],
        "fullstack": ["fullstack-developer"],
        "mobile": ["mobile-developer", "ios-developer", "android-developer"],
        "ios": ["ios-developer", "mobile-developer"],
        "android": ["android-developer", "mobile-developer"],
        "test": ["qa-engineer", "code-reviewer"],
        "review": ["code-reviewer"],
        "security": ["security-reviewer", "security-engineer"],
        "compliance": ["compliance-officer", "gdpr-privacy"],
        "privacy": ["privacy-engineer", "gdpr-privacy"],
        "monitoring": ["observability-engineer", "site-reliability-engineer"],
        "observability": ["observability-engineer"],
        "prometheus": ["observability-engineer"],
        "grafana": ["observability-engineer"],
        "architecture": ["system-architect", "cloud-architect"],
        "system design": ["system-architect"],
        "microservice": ["system-architect", "backend-developer"],
        "cloud": ["cloud-architect", "devops-engineer"],
        "aws": ["cloud-architect", "devops-engineer"],
        "azure": ["cloud-architect"],
        "gcp": ["cloud-architect"],
        "product": ["product-manager", "product-strategist"],
        "ux": ["ui-ux-designer", "ux-researcher"],
        "design system": ["ui-ux-designer"],
        "accessibility": ["accessibility-auditor", "accessibility-testing"],
        "data": ["data-engineer", "data-scientist", "analytics-engineer"],
        "ml": ["ml-engineer", "ml-ai-engineer", "data-scientist"],
        "ai": ["ai-engineer", "ml-ai-engineer", "llm-engineer"],
        "llm": ["llm-engineer", "ai-engineer"],
        "blockchain": ["blockchain-developer"],
        "smart contract": ["smart-contract-auditor", "blockchain-developer"],
        "zkp": ["zkp-engineer", "cryptographic-engineer"],
        "game": ["gameplay-programmer", "game-engine-architect"],
        "unity": ["gameplay-programmer", "game-engine-architect"],
        "unreal": ["gameplay-programmer", "game-engine-architect"],
        "health": ["healthcare-security", "hipaa-technical-implementation"],
        "hipaa": ["hipaa-technical-implementation", "healthcare-security"],
        "fda": ["health-regulatory-submission"],
        "finance": ["financial-security", "algorithmic-trader"],
        "trading": ["algorithmic-trader", "market-data-engineer"],
        "desktop": ["desktop-developer", "macos-developer"],
        "macos": ["macos-developer", "desktop-developer"],
        "windows": ["desktop-developer"],
        "linux": ["devops-engineer", "site-reliability-engineer"],
        "prd": ["product-manager"],
        "roadmap": ["product-manager", "technical-program-manager"],
        "okr": ["product-strategist", "ceo-strategist"],
        "strategy": ["ceo-strategist", "business-strategist"],
        "hiring": ["recruiting", "engineering-manager"],
        "interview": ["recruiting", "hr-manager"],
        "performance review": ["engineering-manager", "hr-manager"],
        "oncall": ["site-reliability-engineer", "incident-responder"],
        "incident": ["incident-responder", "site-reliability-engineer"],
        "migration": ["migration-architect"],
        "refactor": ["code-reviewer", "migration-architect"],
        "debug": ["debugging-and-error-recovery", "code-reviewer"],
        "crash": ["debugging-and-error-recovery", "site-reliability-engineer"],
        "performance": ["performance-engineer", "site-reliability-engineer"],
        "optimize": ["performance-engineer", "code-reviewer"],
    }

    def __init__(self, graph: SkillGraph, ledger: StateLedger):
        self.graph = graph
        self.ledger = ledger

    def route(self, query: str, current_skill: Optional[str] = None) -> RouteResult:
        """Route a user query to the best-matching skill.

        Strategy (in order):
        1. Curated keyword routing — high-precision mapping for ~80 common domains
        2. If current_skill exists and query maps to a downstream skill, route there
        3. Match query against trigger words in skill descriptions
        4. Fall back to semantic keyword matching against skill names
        """
        query_lower = query.lower()

        # Strategy 0: Curated keyword routing (highest precision)
        for keyword, skill_ids in self.CURATED_ROUTES.items():
            if keyword in query_lower:
                for sid in skill_ids:
                    node = self.graph.nodes.get(sid)
                    if node:
                        upstream = self.graph.get_upstream(node.id)
                        return RouteResult(
                            primary_skill=node,
                            confidence=0.80 if keyword in query_lower.split() else 0.65,
                            upstream_skills=upstream,
                            rationale=f"Curated route: keyword '{keyword}' → {node.id}"
                        )

        # Strategy 1: Check if this is a chain transition from current skill
        if current_skill and current_skill in self.graph.nodes:
            current = self.graph.nodes[current_skill]
            downstream = self.graph.get_downstream(current_skill)
            for ds in downstream:
                if any(t in query_lower for t in ds.triggers):
                    self.ledger.record_transition(current_skill, ds.id, query)
                    return RouteResult(
                        primary_skill=ds,
                        confidence=0.85,
                        upstream_skills=[current],
                        chain_path=self.graph.find_chain_path(current_skill, ds.id) or [],
                        rationale=f"Chain transition: {current_skill} → {ds.id} (matched trigger: {query})"
                    )

        # Strategy 2: Trigger word matching with scoring
        scored: list[tuple[int, SkillNode]] = []
        for trigger, skill_ids in self.graph._trigger_index.items():
            if trigger in query_lower:
                for sid in skill_ids:
                    node = self.graph.nodes.get(sid)
                    if node:
                        # Bonus for exact phrase match
                        score = 2 if trigger in query_lower else 1
                        # Bonus for anti-trigger absence
                        if not any(at in query_lower for at in node.anti_triggers):
                            score += 1
                        scored.append((score, node))

        # Deduplicate and sort by score descending
        seen = set()
        unique_scored = []
        for score, node in sorted(scored, key=lambda x: -x[0]):
            if node.id not in seen:
                seen.add(node.id)
                unique_scored.append((score, node))

        if unique_scored:
            best_score, best_node = unique_scored[0]
            confidence = min(0.95, best_score / 5.0)

            # Get upstream dependencies
            upstream = self.graph.get_upstream(best_node.id)

            if current_skill and current_skill != best_node.id:
                self.ledger.record_transition(current_skill, best_node.id, query)

            return RouteResult(
                primary_skill=best_node,
                confidence=confidence,
                upstream_skills=upstream,
                rationale=f"Matched {best_score} trigger(s) in query"
            )

        # Strategy 3: Semantic keyword matching with skill name/domain scoring
        keyword_scored = []
        for skill_id, node in self.graph.nodes.items():
            score = 0
            name_words = set(skill_id.replace("-", " ").split())
            query_words = set(query_lower.split())

            # Exact skill ID match in query
            if skill_id.replace("-", " ") in query_lower:
                score += 10
            # Partial word matches
            matches = name_words & query_words
            score += len(matches) * 2

            # Check description for keyword overlap
            desc_lower = node.description.lower()
            for word in query_words:
                if len(word) > 3 and word in desc_lower:
                    score += 0.5

            if score > 0:
                keyword_scored.append((score, node))

        # Sort by score descending
        keyword_scored.sort(key=lambda x: -x[0])

        if keyword_scored:
            best_score, best_node = keyword_scored[0]
            confidence = min(0.7, best_score / 15.0)
            return RouteResult(
                primary_skill=best_node,
                confidence=confidence,
                rationale=f"Semantic match: '{best_node.id}' (score: {best_score:.1f})"
            )

        # No route found
        return RouteResult(
            primary_skill=None,  # type: ignore
            confidence=0.0,
            rationale="No matching skill found. Try rephrasing your query."
        )

    def resolve_chain(self, skill_chain: str) -> Optional[list[SkillNode]]:
        """Resolve a chain like 'ceo-strategist -> product-manager -> backend-developer'."""
        skill_ids = [s.strip().lower().replace(" ", "-") for s in skill_chain.split("->")]
        nodes = []
        for sid in skill_ids:
            node = self.graph.get_node(sid)
            if not node:
                # Try fuzzy match
                for nid, n in self.graph.nodes.items():
                    if sid in nid or nid in sid:
                        node = n
                        break
            if not node:
                print(f"ERROR: Skill '{sid}' not found in graph", file=sys.stderr)
                return None
            nodes.append(node)
        return nodes


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Dynamic Skill Routing Runtime — executable chain graph orchestrator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "Build a REST API with JWT auth"
  %(prog)s --json "I need threat modeling"
  %(prog)s --chain "ceo-strategist -> product-manager -> backend-developer"
  %(prog)s --graph
  %(prog)s --state
        """
    )
    parser.add_argument("query", nargs="?", help="User query to route")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--chain", metavar="CHAIN",
                        help="Resolve a skill chain (e.g., 'a -> b -> c')")
    parser.add_argument("--graph", action="store_true", help="Print graph statistics")
    parser.add_argument("--state", action="store_true", help="Show state ledger")
    parser.add_argument("--current", metavar="SKILL_ID",
                        help="Current active skill for transition routing")

    args = parser.parse_args()

    graph = SkillGraph()
    ledger = StateLedger()

    # --graph: Print graph stats
    if args.graph:
        stats = graph.stats()
        if args.json:
            print(json.dumps(stats, indent=2))
        else:
            print(f"Skill Graph Statistics")
            print(f"═══════════════════════")
            print(f"  Total nodes:  {stats['total_nodes']}")
            print(f"  Total edges:  {stats['total_edges']}")
            print(f"  Domains:      {stats['domains']}")
            print(f"  Orphaned:     {stats['orphaned_skills']} skills")
            print(f"  Max out-degree: {stats['max_out_degree']}")
            print(f"  Max in-degree:  {stats['max_in_degree']}")
            print(f"  Trigger index:  {stats['trigger_index_size']} keywords")
            if stats['orphaned_list']:
                print(f"  Orphaned (first 10): {', '.join(stats['orphaned_list'])}")
        return 0

    # --state: Show ledger
    if args.state:
        recent = ledger.get_recent_transitions(20)
        if args.json:
            print(json.dumps(ledger.data, indent=2))
        else:
            print(f"State Ledger — {len(ledger.data['transitions'])} transitions, "
                  f"{len(ledger.data['decisions'])} decisions")
            print(f"Current skill: {ledger.get_current_skill() or 'none'}")
            if recent:
                print(f"\nRecent transitions:")
                for t in recent:
                    print(f"  {t['from']} → {t['to']}  ({t['trigger'][:60]}...)")
        return 0

    # --chain: Resolve and validate a chain
    if args.chain:
        router = SkillRouter(graph, ledger)
        nodes = router.resolve_chain(args.chain)
        if not nodes:
            return 1
        if args.json:
            chain_data = {
                "chain": args.chain,
                "nodes": [{"id": n.id, "name": n.name, "domain": n.domain,
                           "token_budget": n.token_budget} for n in nodes],
                "valid": all(graph.find_chain_path(nodes[i].id, nodes[i+1].id)
                            for i in range(len(nodes)-1))
            }
            print(json.dumps(chain_data, indent=2))
        else:
            print(f"Chain: {' → '.join(n.id for n in nodes)}")
            for i, node in enumerate(nodes):
                print(f"  {i+1}. {node.name} ({node.id}) — {node.domain}")
                upstream = graph.get_upstream(node.id)
                downstream = graph.get_downstream(node.id)
                if upstream:
                    print(f"      Consumes: {', '.join(n.id for n in upstream[:3])}")
                if downstream:
                    print(f"      Feeds:    {', '.join(n.id for n in downstream[:3])}")
                if i < len(nodes) - 1:
                    path = graph.find_chain_path(node.id, nodes[i+1].id)
                    if path:
                        print(f"      Path to next: {' → '.join(path)}")
                    else:
                        print(f"      ⚠ No direct edge to {nodes[i+1].id}")
        return 0

    # --query: Route a natural language query
    if args.query:
        router = SkillRouter(graph, ledger)
        result = router.route(args.query, args.current)

        if args.json:
            output = {
                "query": args.query,
                "routed_to": result.primary_skill.id if result.primary_skill else None,
                "confidence": result.confidence,
                "rationale": result.rationale,
                "upstream": [n.id for n in result.upstream_skills],
                "downstream": [n.id for n in result.downstream_skills],
                "chain_path": result.chain_path,
            }
            print(json.dumps(output, indent=2))
        else:
            if not result.primary_skill:
                print(f"No route found for: {args.query}")
                print(f"Rationale: {result.rationale}")
                return 1

            print(f"Query:  {args.query}")
            print(f"Route:  {result.primary_skill.name} ({result.primary_skill.id})")
            print(f"Confidence: {result.confidence:.0%}")
            print(f"Rationale:  {result.rationale}")
            print(f"Domain:     {result.primary_skill.domain}")
            print(f"Path:       {result.primary_skill.path}")
            if result.upstream_skills:
                print(f"Upstream:   {', '.join(n.id for n in result.upstream_skills[:5])}")
            if result.chain_path:
                print(f"Chain:      {' → '.join(result.chain_path)}")

        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
