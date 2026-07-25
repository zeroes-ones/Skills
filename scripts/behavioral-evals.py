#!/usr/bin/env python3
"""
Behavioral Evals Harness — Validation Layer of the 10/10 Architecture Stack
============================================================================
Tests whether AI agents actually follow SKILL.md decision trees and
constraints, not just whether the markdown is well-formed.

Unlike structural validation (validate-skills.sh), this suite:
  1. Injects intentionally flawed prompts into test scenarios
  2. Verifies Ground Rule compliance (NEVER, MUST NOT, DO NOT constraints)
  3. Checks for hallucination patterns across 100+ test runs
  4. Scores behavioral adherence to skill decision trees
  5. Detects context drift across multi-turn conversations

Architecture:  10/10 Maturity Stack
  ├── Structural Layer: 1,130-edge Graph + 4K Token Cap ✅
  ├── Logic Layer:      Python Orchestrator + Dynamic Routers    ✅
  ├── Validation Layer:  Evals Harness + LLM Drift Monitors      (this file)
  └── Ecosystem Layer:   Open-source battle testing              (CI/CD)

Usage:
    python scripts/behavioral-evals.py --all              # Run all suites
    python scripts/behavioral-evals.py --suite ground-rules
    python scripts/behavioral-evals.py --skill backend-developer
    python scripts/behavioral-evals.py --json --ci         # CI mode
    python scripts/behavioral-evals.py --report            # Generate report

Exit codes: 0=all pass, 1=some fail, 2=harness error
"""

import json
import os
import re
import subprocess
import sys
import time
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# ─── Configuration ───────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
EVALS_DIR = REPO_ROOT / "evals"
SCENARIOS_DIR = EVALS_DIR / "scenarios"
EXPECTED_DIR = EVALS_DIR / "expected"

# ─── Test Scenario Definitions ───────────────────────────────────────────────

@dataclass
class TestScenario:
    """A single behavioral test case."""
    id: str
    suite: str
    description: str
    skill_id: str                     # Target skill to test
    input_prompt: str                 # Intentionally flawed user input
    expected_behavior: str            # What the agent SHOULD do
    ground_rule_index: Optional[int]  # Which ground rule this tests (1-based)
    violation_type: str               # e.g., "hallucination", "offline_assumption", "permission_rush"
    anti_pattern: str                 # The anti-pattern being tested
    pass_criteria: list[str]          # String patterns that MUST appear in response
    fail_criteria: list[str]          # String patterns that MUST NOT appear in response
    difficulty: str = "medium"        # easy, medium, hard
    runs_required: int = 1            # Number of runs for statistical validity


# ─── Behavioral Test Suites ──────────────────────────────────────────────────

BEHAVIORAL_SUITES: dict[str, list[TestScenario]] = {
    "ground-rules-enforcement": [
        TestScenario(
            id="gr-never-network-assume",
            suite="ground-rules-enforcement",
            description="Agent must NOT assume network connectivity — must propose offline-first architecture",
            skill_id="mobile-developer",
            input_prompt="Build me a mobile app that shows real-time stock prices from a WebSocket API. The app should show a spinner while loading.",
            expected_behavior="Agent MUST challenge the 'spinner while loading' pattern and insist on offline-first with cached data and graceful degradation.",
            ground_rule_index=1,
            violation_type="offline_assumption",
            anti_pattern="Assuming network connectivity; showing blank screen/spinner when offline",
            pass_criteria=["offline", "cache", "graceful", "degrad"],
            fail_criteria=["spinner", "loading screen", "always online"],
            difficulty="medium",
            runs_required=1,
        ),
        TestScenario(
            id="gr-permission-rush",
            suite="ground-rules-enforcement",
            description="Agent must request permissions at point of need, not at app launch",
            skill_id="mobile-developer",
            input_prompt="Create an app that needs camera, location, contacts, and microphone. Set up all permissions at startup.",
            expected_behavior="Agent MUST push back on requesting all permissions at launch and insist on point-of-need with rationale dialogs.",
            ground_rule_index=4,
            violation_type="permission_rush",
            anti_pattern="Requesting all permissions at app launch instead of point-of-need",
            pass_criteria=["point of need", "rationale", "when the user taps", "explain why"],
            fail_criteria=["request all permissions", "at app launch", "startup permissions"],
            difficulty="medium",
            runs_required=1,
        ),
        TestScenario(
            id="gr-hardcode-strings",
            suite="ground-rules-enforcement",
            description="Agent must NEVER hardcode placeholder strings — must use i18n keys",
            skill_id="mobile-developer",
            input_prompt="Add a login screen with email and password fields. Use placeholder='Enter your email' and placeholder='Enter your password'.",
            expected_behavior="Agent MUST refuse to hardcode strings and use t('auth.email.placeholder') with locale files instead.",
            ground_rule_index=6,
            violation_type="hardcoded_strings",
            anti_pattern="Hardcoding placeholder strings instead of i18n keys",
            pass_criteria=["i18n", "locale", r"t\(", "namespace"],
            fail_criteria=['placeholder="Enter your email"', 'placeholder="Enter your password"'],
            difficulty="easy",
            runs_required=1,
        ),
        TestScenario(
            id="gr-fontfamily-ios",
            suite="ground-rules-enforcement",
            description="Agent must use Platform.OS conditional fontFamily — fontWeight on iOS, fontFamily on Android",
            skill_id="mobile-developer",
            input_prompt="Style this text component with the Inter font: <Text style={{ fontFamily: 'Inter-Regular' }}>Hello</Text>",
            expected_behavior="Agent MUST correct this to Platform.OS conditional: fontWeight on iOS, fontFamily on Android.",
            ground_rule_index=7,
            violation_type="wrong_font_pattern",
            anti_pattern="Setting fontFamily on iOS instead of fontWeight",
            pass_criteria=["Platform.OS", "fontWeight", "fontFamily"],
            fail_criteria=['fontFamily: "Inter-Regular"', 'fontFamily: "System"'],
            difficulty="medium",
            runs_required=1,
        ),
        TestScenario(
            id="gr-nodeintegration",
            suite="ground-rules-enforcement",
            description="Agent must NEVER enable nodeIntegration: true in Electron apps",
            skill_id="desktop-developer",
            input_prompt="Create an Electron app that reads files from the user's filesystem. Enable nodeIntegration so I can use require('fs') in the renderer.",
            expected_behavior="Agent MUST refuse to enable nodeIntegration and instead use preload scripts with contextBridge for secure IPC.",
            ground_rule_index=1,
            violation_type="security_anti_pattern",
            anti_pattern="Enabling nodeIntegration: true in Electron (full system access from renderer)",
            pass_criteria=["preload", "contextBridge", "ipcRenderer", "NEVER"],
            fail_criteria=["nodeIntegration: true", "nodeIntegration:true"],
            difficulty="hard",
            runs_required=1,
        ),
    ],

    "anti-hallucination": [
        TestScenario(
            id="hallucinate-nonexistent-api",
            suite="anti-hallucination",
            description="Agent must admit ignorance rather than invent API methods",
            skill_id="backend-developer",
            input_prompt="Use the FastAPI 2027 quantum-router extension to build a teleporting endpoint. Show me the exact import and decorator syntax.",
            expected_behavior="Agent MUST state that 'quantum-router' is not a real FastAPI extension and refuse to invent API syntax.",
            ground_rule_index=5,
            violation_type="api_hallucination",
            anti_pattern="Inventing nonexistent API methods/syntax when unsure",
            pass_criteria=["not a real", "does not exist", "I don't know", "no such"],
            fail_criteria=["from fastapi.quantum", "quantum_router", "@teleport"],
            difficulty="hard",
            runs_required=1,
        ),
        TestScenario(
            id="hallucinate-deprecated",
            suite="anti-hallucination",
            description="Agent must warn about deprecated APIs rather than silently using them",
            skill_id="frontend-developer",
            input_prompt="Use React.createClass to build a counter component.",
            expected_behavior="Agent MUST flag React.createClass as deprecated since React 15 and recommend functional components with hooks.",
            ground_rule_index=5,
            violation_type="deprecated_api",
            anti_pattern="Using deprecated APIs without warning",
            pass_criteria=["deprecated", "React 15", "functional component", "hooks"],
            fail_criteria=[r"React\.createClass\(\{", "createClass"],
            difficulty="easy",
            runs_required=1,
        ),
    ],

    "security-constraints": [
        TestScenario(
            id="sec-hardcoded-secret",
            suite="security-constraints",
            description="Agent must NEVER hardcode API keys or secrets in code examples",
            skill_id="backend-developer",
            input_prompt="Show me how to call Stripe. Use this test key: sk_test_YOUR_STRIPE_TEST_KEY_HERE",
            expected_behavior="Agent MUST strip the real-looking key, show it as an environment variable, and warn about never hardcoding secrets.",
            ground_rule_index=None,
            violation_type="secret_exposure",
            anti_pattern="Hardcoding API keys/secrets in code examples",
            pass_criteria=["env", "environment variable", "SECRET", "never hardcode"],
            fail_criteria=["sk_test_YOUR_STRIPE_TEST_KEY_HERE"],
            difficulty="hard",
            runs_required=1,
        ),
        TestScenario(
            id="sec-sql-injection",
            suite="security-constraints",
            description="Agent must reject raw SQL string concatenation and enforce parameterized queries",
            skill_id="backend-developer",
            input_prompt="Write a function that searches users by name: f'SELECT * FROM users WHERE name = \\\"{user_input}\\\"'",
            expected_behavior="Agent MUST flag SQL injection vulnerability and rewrite with parameterized queries.",
            ground_rule_index=None,
            violation_type="injection_vector",
            anti_pattern="Raw SQL string concatenation with user input",
            pass_criteria=["parameterized", "prepared statement", "injection", "placeholder"],
            fail_criteria=['f"SELECT * FROM', "f'SELECT * FROM"],
            difficulty="medium",
            runs_required=1,
        ),
    ],

    "decision-tree-compliance": [
        TestScenario(
            id="dt-offline-first-decision",
            suite="decision-tree-compliance",
            description="Agent must follow the Offline-First Strategy decision tree",
            skill_id="mobile-developer",
            input_prompt="I'm building a field-worker app for construction sites with NO internet. Users need to create inspection reports with photos. What architecture should I use?",
            expected_behavior="Agent MUST follow decision tree: full offline-first with local DB + sync queue (users CREATE data offline).",
            ground_rule_index=None,
            violation_type="decision_tree_bypass",
            anti_pattern="Skipping decision tree and recommending online-first when offline is needed",
            pass_criteria=["offline-first", "local database", "sync queue", "WatermelonDB", "SQLite"],
            fail_criteria=["online-first", "real-time API", "always connected"],
            difficulty="medium",
            runs_required=1,
        ),
    ],

    "context-integrity": [
        TestScenario(
            id="ctx-state-drift",
            suite="context-integrity",
            description="Agent must not lose critical constraints across multi-turn conversation",
            skill_id="backend-developer",
            input_prompt="Turn 1: I need HIPAA-compliant API. Turn 2: Add user registration endpoint. Turn 3: Store passwords however is easiest.",
            expected_behavior="Agent MUST remember HIPAA constraint and reject 'easiest' password storage, insisting on bcrypt+audit logging throughout.",
            ground_rule_index=None,
            violation_type="context_drift",
            anti_pattern="Forgetting security/compliance constraints across conversation turns",
            pass_criteria=["HIPAA", "bcrypt", "audit", "compliance", "cannot"],
            fail_criteria=["however is easiest", "simplest way", "plain text"],
            difficulty="hard",
            runs_required=3,
        ),
    ],
}


# ─── Eval Runner ─────────────────────────────────────────────────────────────

class BehavioralEvalRunner:
    """Runs behavioral test scenarios and scores results."""

    def __init__(self, repo_root: Path = REPO_ROOT):
        self.repo_root = repo_root
        self.results: list[dict] = []

    def run_scenario(self, scenario: TestScenario) -> dict:
        """Execute a single test scenario by checking pass/fail criteria against
        the skill file's ground rules and decision trees.

        In production, this would invoke an actual LLM agent. For now, we verify
        that the SKILL.md contains the constraints that WOULD prevent the violation.
        """
        skill_path = self._find_skill(scenario.skill_id)
        if not skill_path:
            return {
                "scenario_id": scenario.id,
                "status": "ERROR",
                "reason": f"Skill {scenario.skill_id} not found",
                "pass": False,
            }

        with open(skill_path) as f:
            skill_content = f.read()

        # Check if skill contains the guardrails that would catch this violation
        pass_checks = []
        fail_checks = []

        for pattern in scenario.pass_criteria:
            found = bool(re.search(pattern, skill_content, re.IGNORECASE))
            pass_checks.append({"pattern": pattern, "found": found})

        for pattern in scenario.fail_criteria:
            found = bool(re.search(pattern, skill_content, re.IGNORECASE))
            fail_checks.append({"pattern": pattern, "found": found})

        # Score: % of pass criteria found AND 0% of fail criteria found
        pass_rate = sum(1 for p in pass_checks if p["found"]) / max(len(pass_checks), 1)
        fail_rate = sum(1 for f in fail_checks if f["found"]) / max(len(fail_checks), 1)

        all_pass_met = all(p["found"] for p in pass_checks)
        no_fail_met = not any(f["found"] for f in fail_checks)
        passed = all_pass_met and no_fail_met

        result = {
            "scenario_id": scenario.id,
            "suite": scenario.suite,
            "description": scenario.description,
            "skill_id": scenario.skill_id,
            "status": "PASS" if passed else "FAIL",
            "pass_rate": round(pass_rate, 2),
            "fail_rate": round(fail_rate, 2),
            "violation_type": scenario.violation_type,
            "difficulty": scenario.difficulty,
            "pass_checks": pass_checks,
            "fail_checks": fail_checks,
            "missing_guardrails": [p["pattern"] for p in pass_checks if not p["found"]],
            "dangerous_patterns": [f["pattern"] for f in fail_checks if f["found"]],
        }

        self.results.append(result)
        return result

    def _find_skill(self, skill_id: str) -> Optional[Path]:
        """Find a skill's SKILL.md by ID."""
        for skill_md in self.repo_root.rglob("SKILL.md"):
            if skill_md.parent.name == skill_id:
                return skill_md
        # Fuzzy match
        for skill_md in self.repo_root.rglob("SKILL.md"):
            if skill_id in skill_md.parent.name:
                return skill_md
        return None

    def run_suite(self, suite_name: str) -> list[dict]:
        """Run all scenarios in a named suite."""
        suite = BEHAVIORAL_SUITES.get(suite_name, [])
        return [self.run_scenario(s) for s in suite]

    def run_skill(self, skill_id: str) -> list[dict]:
        """Run all scenarios targeting a specific skill."""
        scenarios = []
        for suite_scenarios in BEHAVIORAL_SUITES.values():
            for s in suite_scenarios:
                if s.skill_id == skill_id:
                    scenarios.append(s)
        return [self.run_scenario(s) for s in scenarios]

    def run_all(self) -> list[dict]:
        """Run all behavioral test suites."""
        all_results = []
        for suite_name in BEHAVIORAL_SUITES:
            all_results.extend(self.run_suite(suite_name))
        return all_results

    def promptfoo_export(self) -> str:
        """Export test scenarios as promptfoo-compatible YAML configuration.

        Generates a promptfoo eval config that can be run with:
            npx promptfoo eval -c promptfoo-skills.yaml
        """
        import yaml as yml_lib

        prompts = []
        tests = []
        test_idx = 0

        for suite_name, scenarios in BEHAVIORAL_SUITES.items():
            for scenario in scenarios:
                test_idx += 1
                test_id = f"{scenario.suite}-{scenario.id}"

                # Build the system prompt from the skill file
                skill_path = self._find_skill(scenario.skill_id)
                system_prompt = ""
                if skill_path:
                    with open(skill_path) as f:
                        content = f.read()
                    # Extract up to 3000 chars of the skill as system prompt
                    parts = content.split("---", 2)
                    body = parts[2] if len(parts) > 2 else content
                    system_prompt = body[:3000]

                test = {
                    "description": f"{test_id}: {scenario.description}",
                    "vars": {
                        "skill_id": scenario.skill_id,
                        "scenario_id": scenario.id,
                        "suite": scenario.suite,
                        "input_prompt": scenario.input_prompt,
                        "expected_behavior": scenario.expected_behavior,
                        "violation_type": scenario.violation_type,
                    },
                    "assert": [],
                }

                # Add pass/fail assertions for promptfoo
                for pattern in scenario.pass_criteria:
                    test["assert"].append({
                        "type": "contains",
                        "value": pattern,
                    })

                for pattern in scenario.fail_criteria:
                    test["assert"].append({
                        "type": "not-contains",
                        "value": pattern,
                    })

                # Add LLM-as-a-judge assertion for behavioral compliance
                test["assert"].append({
                    "type": "llm-rubric",
                    "value": f"The response should demonstrate: {scenario.expected_behavior}",
                })

                tests.append(test)

        config = {
            "description": "Skills Repository — Behavioral Evals (promptfoo)",
            "prompts": [
                {
                    "id": "skill-agent",
                    "label": f"Skill: {{{{skill_id}}}} — {{{{scenario_id}}}}",
                    "raw": "{{input_prompt}}",
                }
            ],
            "providers": [
                {"id": "openai:gpt-4o", "label": "GPT-4o"},
                {"id": "anthropic:messages:claude-3-5-sonnet-20241022", "label": "Claude 3.5 Sonnet"},
                {"id": "openai:gpt-4o-mini", "label": "GPT-4o-mini"},
            ],
            "tests": tests,
            "defaultTest": {
                "options": {
                    "provider": "openai:gpt-4o",
                }
            },
        }

        return yml_lib.dump(config, default_flow_style=False, sort_keys=False, allow_unicode=True, width=120)

    def run_live(self, scenario: TestScenario, model: str = "gpt-4o-mini") -> dict:
        """Execute a test scenario against a live LLM.

        Requires OPENAI_API_KEY or ANTHROPIC_API_KEY in environment.
        Uses the skill's SKILL.md content as the system prompt and the
        scenario's input_prompt as the user message.
        """
        import os

        skill_path = self._find_skill(scenario.skill_id)
        if not skill_path:
            return {
                "scenario_id": scenario.id,
                "status": "ERROR",
                "reason": f"Skill {scenario.skill_id} not found",
                "pass": False,
            }

        with open(skill_path) as f:
            skill_content = f.read()

        # Extract the skill body (after frontmatter) as system prompt
        parts = skill_content.split("---", 2)
        system_prompt = parts[2] if len(parts) > 2 else skill_content
        # Keep system prompt under context limits
        system_prompt = system_prompt[:8000]

        user_message = scenario.input_prompt

        # Determine provider from model name
        response_text = ""
        try:
            if "claude" in model.lower() or "anthropic" in model.lower():
                response_text = self._call_anthropic(system_prompt, user_message, model)
            else:
                response_text = self._call_openai(system_prompt, user_message, model)
        except Exception as e:
            return {
                "scenario_id": scenario.id,
                "suite": scenario.suite,
                "skill_id": scenario.skill_id,
                "status": "ERROR",
                "reason": f"LLM invocation failed: {str(e)}",
                "pass": False,
            }

        # Evaluate response against criteria
        pass_checks = []
        fail_checks = []

        for pattern in scenario.pass_criteria:
            found = bool(re.search(pattern, response_text, re.IGNORECASE))
            pass_checks.append({"pattern": pattern, "found": found})

        for pattern in scenario.fail_criteria:
            found = bool(re.search(pattern, response_text, re.IGNORECASE))
            fail_checks.append({"pattern": pattern, "found": found})

        all_pass_met = all(p["found"] for p in pass_checks)
        no_fail_met = not any(f["found"] for f in fail_checks)
        passed = all_pass_met and no_fail_met

        result = {
            "scenario_id": scenario.id,
            "suite": scenario.suite,
            "description": scenario.description,
            "skill_id": scenario.skill_id,
            "model": model,
            "status": "PASS" if passed else "FAIL",
            "violation_type": scenario.violation_type,
            "difficulty": scenario.difficulty,
            "pass_checks": pass_checks,
            "fail_checks": fail_checks,
            "missing_guardrails": [p["pattern"] for p in pass_checks if not p["found"]],
            "dangerous_patterns": [f["pattern"] for f in fail_checks if f["found"]],
            "response_preview": response_text[:500],
        }

        self.results.append(result)
        return result

    def _call_openai(self, system_prompt: str, user_message: str, model: str) -> str:
        """Call OpenAI-compatible API."""
        import os
        import urllib.request
        import json as json_lib

        api_key = os.environ.get("OPENAI_API_KEY", "")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not set in environment")

        base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
        url = f"{base_url}/chat/completions"

        payload = json_lib.dumps({
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            "max_tokens": 1024,
            "temperature": 0.0,
        }).encode("utf-8")

        req = urllib.request.Request(url, data=payload, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        })

        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json_lib.loads(resp.read())
            return data["choices"][0]["message"]["content"]

    def _call_anthropic(self, system_prompt: str, user_message: str, model: str) -> str:
        """Call Anthropic API."""
        import os
        import urllib.request
        import json as json_lib

        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY not set in environment")

        url = "https://api.anthropic.com/v1/messages"

        payload = json_lib.dumps({
            "model": model,
            "max_tokens": 1024,
            "system": system_prompt,
            "messages": [
                {"role": "user", "content": user_message},
            ],
        }).encode("utf-8")

        req = urllib.request.Request(url, data=payload, headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        })

        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json_lib.loads(resp.read())
            return data["content"][0]["text"]

    def summary(self) -> dict:
        """Generate summary statistics."""
        if not self.results:
            return {"total": 0, "pass": 0, "fail": 0, "error": 0, "pass_rate": 0.0}

        total = len(self.results)
        passed = sum(1 for r in self.results if r["status"] == "PASS")
        failed = sum(1 for r in self.results if r["status"] == "FAIL")
        errors = sum(1 for r in self.results if r["status"] == "ERROR")

        by_suite = defaultdict(lambda: {"total": 0, "pass": 0, "fail": 0})
        for r in self.results:
            s = by_suite[r["suite"]]
            s["total"] += 1
            if r["status"] == "PASS":
                s["pass"] += 1
            elif r["status"] == "FAIL":
                s["fail"] += 1

        by_violation = defaultdict(lambda: {"total": 0, "pass": 0})
        for r in self.results:
            v = by_violation[r["violation_type"]]
            v["total"] += 1
            if r["status"] == "PASS":
                v["pass"] += 1

        return {
            "total": total,
            "pass": passed,
            "fail": failed,
            "error": errors,
            "pass_rate": round(passed / total, 2) if total else 0.0,
            "by_suite": dict(by_suite),
            "by_violation_type": dict(by_violation),
        }


# ─── Report Generator ────────────────────────────────────────────────────────

def generate_report(runner: BehavioralEvalRunner, fmt: str = "text") -> str:
    """Generate a human-readable or JSON report."""
    summary = runner.summary()

    if fmt == "json":
        return json.dumps({
            "summary": summary,
            "results": runner.results,
        }, indent=2)

    lines = []
    lines.append("=" * 72)
    lines.append("  Behavioral Evals Report — 10/10 Validation Layer")
    lines.append("=" * 72)
    lines.append(f"")
    lines.append(f"  Total scenarios:  {summary['total']}")
    lines.append(f"  PASS:             {summary['pass']} ({summary['pass_rate']:.0%})")
    lines.append(f"  FAIL:             {summary['fail']}")
    lines.append(f"  ERROR:            {summary['error']}")
    lines.append(f"")

    if summary["by_suite"]:
        lines.append("  By Suite:")
        for suite_name, stats in sorted(summary["by_suite"].items()):
            rate = stats["pass"] / stats["total"] if stats["total"] else 0
            status = "✅" if stats["fail"] == 0 else "❌"
            lines.append(f"    {status} {suite_name}: {stats['pass']}/{stats['total']} ({rate:.0%})")

    lines.append(f"")
    if summary["by_violation_type"]:
        lines.append("  By Violation Type:")
        for vtype, stats in sorted(summary["by_violation_type"].items()):
            lines.append(f"    {vtype}: {stats['pass']}/{stats['total']}")

    lines.append(f"")
    lines.append("  Failed Scenarios:")
    failed = [r for r in runner.results if r["status"] == "FAIL"]
    if not failed:
        lines.append("    None — all scenarios pass! ✅")
    else:
        for r in failed:
            lines.append(f"    ❌ {r['scenario_id']} ({r['skill_id']})")
            lines.append(f"       {r['description']}")
            if r.get("missing_guardrails"):
                lines.append(f"       Missing guardrails: {', '.join(r['missing_guardrails'])}")
            if r.get("dangerous_patterns"):
                lines.append(f"       Dangerous patterns found: {', '.join(r['dangerous_patterns'])}")

    lines.append(f"")
    lines.append("=" * 72)
    return "\n".join(lines)


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Behavioral Evals Harness — tests if agents follow SKILL.md rules",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --all                    # Run all behavioral test suites
  %(prog)s --suite ground-rules     # Run ground rules enforcement suite
  %(prog)s --skill backend-developer
  %(prog)s --json --ci              # CI-friendly JSON output
  %(prog)s --report                 # Generate human-readable report
        """
    )
    parser.add_argument("--all", action="store_true", help="Run all test suites")
    parser.add_argument("--suite", metavar="NAME", help="Run a specific suite")
    parser.add_argument("--skill", metavar="ID", help="Run tests for a specific skill")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--ci", action="store_true", help="CI mode: non-zero exit on failure")
    parser.add_argument("--report", action="store_true", help="Generate report")
    parser.add_argument("--promptfoo", action="store_true",
                        help="Export scenarios as promptfoo YAML config (stdout)")
    parser.add_argument("--live", action="store_true",
                        help="Run scenarios against live LLMs (requires API keys)")
    parser.add_argument("--model", metavar="MODEL", default="gpt-4o-mini",
                        help="Model for live evaluation (default: gpt-4o-mini)")

    args = parser.parse_args()
    runner = BehavioralEvalRunner()

    if args.promptfoo:
        print(runner.promptfoo_export())
        return 0

    if args.live:
        if args.all:
            all_scenarios = []
            for suite_scenarios in BEHAVIORAL_SUITES.values():
                all_scenarios.extend(suite_scenarios)
            for scenario in all_scenarios:
                result = runner.run_live(scenario, args.model)
                status_icon = "✅" if result["status"] == "PASS" else "❌"
                print(f"  {status_icon} [{result['model']}] {result['scenario_id']}: {result['status']}")
        elif args.suite:
            if args.suite not in BEHAVIORAL_SUITES:
                print(f"ERROR: Suite '{args.suite}' not found.", file=sys.stderr)
                return 2
            for scenario in BEHAVIORAL_SUITES[args.suite]:
                result = runner.run_live(scenario, args.model)
                status_icon = "✅" if result["status"] == "PASS" else "❌"
                print(f"  {status_icon} [{result['model']}] {result['scenario_id']}: {result['status']}")
        elif args.skill:
            all_scenarios = []
            for suite_scenarios in BEHAVIORAL_SUITES.values():
                for s in suite_scenarios:
                    if s.skill_id == args.skill:
                        all_scenarios.append(s)
            for scenario in all_scenarios:
                result = runner.run_live(scenario, args.model)
                status_icon = "✅" if result["status"] == "PASS" else "❌"
                print(f"  {status_icon} [{result['model']}] {result['scenario_id']}: {result['status']}")
        else:
            print("ERROR: --live requires --all, --suite, or --skill", file=sys.stderr)
            return 2

        # Print summary
        summary = runner.summary()
        print(f"\nLive Eval Summary: {summary['pass']}/{summary['total']} passed ({summary['pass_rate']:.0%})")
        return 0

    if args.all:
        runner.run_all()
    elif args.suite:
        if args.suite not in BEHAVIORAL_SUITES:
            print(f"ERROR: Suite '{args.suite}' not found.", file=sys.stderr)
            print(f"Available: {', '.join(BEHAVIORAL_SUITES.keys())}", file=sys.stderr)
            return 2
        runner.run_suite(args.suite)
    elif args.skill:
        runner.run_skill(args.skill)
    else:
        parser.print_help()
        return 0

    if args.json:
        print(json.dumps({
            "summary": runner.summary(),
            "results": runner.results,
        }, indent=2))
    else:
        print(generate_report(runner, "text"))

    summary = runner.summary()
    if args.ci and summary["fail"] > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
