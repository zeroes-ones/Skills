# Eval Harness Architecture

<!-- QUICK: 30s -- The eval harness runs agents in containerized environments with mocked project filesystems, intentionally flawed prompt injection, and 10-dimension scenario generators. It produces structured eval reports consumed by CI/CD gates. -->

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      Eval Harness Controller                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐    │
│  │ Scenario │  │  Docker  │  │  Metric  │  │   Report     │    │
│  │ Generator│  │  Runner  │  │ Collector│  │  Generator   │    │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └──────┬───────┘    │
│       │              │              │               │            │
│       ▼              ▼              ▼               ▼            │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Isolated Agent Containers                     │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐     │   │
│  │  │ Agent A │  │ Agent B │  │ Agent C │  │ Agent D │     │   │
│  │  │ (current│  │(baseline│  │(variant │  │(variant │     │   │
│  │  │  code) │  │  golden)│  │  prompt)│  │  model) │     │   │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘     │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Mock Project Environment                      │   │
│  │  Filesystem │ Git History │ Dependencies │ Network Rules  │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Component Design

### 1. Docker Runner

```python
@dataclass
class AgentContainerConfig:
    """Configuration for running an agent in an isolated container."""
    image: str  # Docker image with agent installed
    agent_name: str
    agent_version: str
    command: List[str]
    environment: Dict[str, str]
    volume_mounts: Dict[str, str]  # host_path → container_path
    network: str = "eval_network"  # Isolated Docker network
    cpu_limit: str = "2.0"
    memory_limit: str = "4g"
    timeout: int = 300  # seconds

class DockerAgentRunner:
    """Runs agent evaluations in isolated Docker containers."""
    
    def __init__(self, docker_client):
        self.client = docker_client
        self.network = self._ensure_network("eval_network")
    
    def run_eval(self, config: AgentContainerConfig, 
                 scenario_dir: str) -> EvalResult:
        """Run a single agent evaluation in a container."""
        container = self.client.containers.run(
            image=config.image,
            command=config.command,
            environment={
                **config.environment,
                "EVAL_SCENARIO_DIR": "/scenarios",
                "EVAL_MODE": "true",
                "EVAL_OUTPUT_DIR": "/output"
            },
            volumes={
                scenario_dir: {"bind": "/scenarios", "mode": "ro"},
                f"/tmp/eval_output_{uuid4()}": {"bind": "/output", "mode": "rw"}
            },
            network=self.network.name,
            cpu_period=100000,
            cpu_quota=int(float(config.cpu_limit) * 100000),
            mem_limit=config.memory_limit,
            detach=True
        )
        
        try:
            result = container.wait(timeout=config.timeout)
            if result["StatusCode"] != 0:
                logs = container.logs().decode()
                return EvalResult(
                    success=False,
                    error=f"Container exited with code {result['StatusCode']}",
                    logs=logs
                )
            
            # Collect structured output
            output = self._collect_output(container)
            return EvalResult(success=True, data=output)
        
        except docker.errors.APIError as e:
            if "out of memory" in str(e):
                return EvalResult(success=False, error="OOM killed")
            raise
        finally:
            container.remove(force=True)
```

### 2. Scenario Generator (10 Dimensions)

```python
SCENARIO_DIMENSIONS = {
    "codebase_size": ["micro (<10 files)", "small (10-100)", "medium (100-1000)", "large (1000+)"],
    "domain": ["web_app", "cli_tool", "library", "microservice", "data_pipeline", "mobile"],
    "language": ["python", "typescript", "go", "rust", "java", "mixed"],
    "ambiguity_level": ["explicit_every_step", "high_level_goal", "contradictory_constraints", "missing_context"],
    "error_injection": ["none", "missing_files", "permission_denied", "network_timeout", "corrupted_data"],
    "user_expertise": ["beginner_vague", "intermediate_specific", "expert_jargon"],
    "collaboration_mode": ["solo_agent", "agent_with_human_review", "multi_agent_orchestration"],
    "security_context": ["open_source", "internal_tool", "customer_facing", "compliance_required"],
    "output_format": ["text_only", "code_patch", "structured_json", "mixed_artifacts"],
    "time_pressure": ["no_deadline", "reasonable_deadline", "urgent_15min"]
}

class ScenarioGenerator:
    """Generates diverse evaluation scenarios across 10 dimensions."""
    
    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)
        self.combinatorial_space = self._compute_space()
    
    def generate_suite(self, n_scenarios: int, 
                       coverage_strategy: str = "diverse") -> List[Scenario]:
        """
        Generate n scenarios.
        
        Strategies:
        - "diverse": maximize coverage across dimensions
        - "targeted": focus on historically failing dimensions
        - "combinatorial": pairwise coverage of all dimensions
        """
        if coverage_strategy == "diverse":
            return self._generate_diverse(n_scenarios)
        elif coverage_strategy == "targeted":
            return self._generate_targeted(n_scenarios)
        elif coverage_strategy == "combinatorial":
            return self._generate_pairwise(n_scenarios)
    
    def _generate_diverse(self, n: int) -> List[Scenario]:
        """Latin hypercube sampling across dimensions."""
        scenarios = []
        dims = list(SCENARIO_DIMENSIONS.keys())
        
        for i in range(n):
            scenario_dims = {}
            for dim in dims:
                values = SCENARIO_DIMENSIONS[dim]
                # Cycle through values to ensure coverage
                scenario_dims[dim] = values[i % len(values)]
            scenarios.append(self._build_scenario(scenario_dims))
        
        return scenarios
```

### 3. Mock Project Environment

```python
class MockProjectEnvironment:
    """Creates realistic but controlled project environments for testing."""
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
    
    def create_web_app_project(self) -> Path:
        """Create a realistic web app project structure."""
        project = self.base_dir / "mock-web-app"
        
        # Directory structure
        (project / "src" / "components").mkdir(parents=True)
        (project / "src" / "utils").mkdir(parents=True)
        (project / "tests").mkdir(parents=True)
        (project / "docs").mkdir(parents=True)
        
        # Files with realistic content
        (project / "package.json").write_text(json.dumps({
            "name": "mock-web-app",
            "dependencies": {
                "react": "^18.2.0",
                "express": "^4.18.0",
                "typescript": "^5.0.0"
            }
        }, indent=2))
        
        (project / "src" / "app.tsx").write_text("""
import React from 'react';
// TODO: Implement authentication flow
// BUG: Memory leak in useEffect cleanup
export const App = () => {
  const [user, setUser] = React.useState(null);
  return <div>Mock App</div>;
};
""")
        
        # Intentional flaws for gotcha detection
        (project / "src" / "config.ts").write_text("""
// WARNING: Hardcoded credentials for testing only
export const API_KEY = "sk-mock-key-do-not-use-in-production-12345";
export const DB_PASSWORD = "admin123";
""")
        
        # Git history simulation
        self._init_mock_git(project)
        
        return project
    
    def inject_flaw(self, flaw_type: str, project: Path):
        """Inject intentional flaws for gotcha detection."""
        flaws = {
            "hardcoded_secret": lambda p: self._inject_secret(p),
            "infinite_loop": lambda p: self._inject_infinite_loop(p),
            "sql_injection": lambda p: self._inject_sql_vuln(p),
            "race_condition": lambda p: self._inject_race_condition(p),
            "memory_leak": lambda p: self._inject_memory_leak(p),
        }
        if flaw_type in flaws:
            flaws[flaw_type](project)
```

### 4. Gotcha Detection Scoring

```python
@dataclass
class GotchaTest:
    name: str
    flaw_type: str
    description: str
    expected_detection: bool  # Agent should detect and flag
    severity: str  # "critical", "high", "medium", "low"

GOTCHA_TESTS = [
    GotchaTest(
        name="hardcoded_api_key",
        flaw_type="hardcoded_secret",
        description="API key is hardcoded in source file. Agent MUST flag this.",
        expected_detection=True,
        severity="critical"
    ),
    GotchaTest(
        name="unsafe_sql_concatenation",
        flaw_type="sql_injection",
        description="SQL query built with string concatenation. Agent MUST flag this.",
        expected_detection=True,
        severity="critical"
    ),
    GotchaTest(
        name="missing_error_handling",
        flaw_type="missing_error_handling",
        description="Network call without try/catch. Agent SHOULD flag this.",
        expected_detection=True,
        severity="high"
    ),
    GotchaTest(
        name="n_plus_one_query",
        flaw_type="n_plus_one",
        description="Query inside loop causing N+1 problem. Agent SHOULD flag this.",
        expected_detection=True,
        severity="medium"
    ),
]

def score_gotcha_detection(agent_output: str, injected_flaws: List[str]) -> dict:
    """
    Score agent on gotcha detection.
    
    Returns:
      - detection_rate: fraction of injected flaws detected
      - false_positive_rate: flaws reported that weren't injected
      - missed_flaws: flaws injected but not detected
      - hallucinated_flaws: flaws reported that don't exist
    """
    detected = set()
    hallucinated = set()
    
    for flaw_id in injected_flaws:
        if flaw_detected_in_output(flaw_id, agent_output):
            detected.add(flaw_id)
    
    for reported_flaw in extract_reported_flaws(agent_output):
        if reported_flaw not in injected_flaws:
            hallucinated.add(reported_flaw)
    
    return {
        "detection_rate": len(detected) / len(injected_flaws),
        "false_positive_rate": len(hallucinated) / max(len(injected_flaws), 1),
        "missed_flaws": list(set(injected_flaws) - detected),
        "hallucinated_flaws": list(hallucinated)
    }
```

## Harness Configuration

```yaml
# eval-harness-config.yml
harness:
  name: "agent-eval-harness"
  version: "2.0.0"
  
  agents:
    baseline:
      image: "agent-registry/agent:golden-v3.1.0"
      version: "3.1.0"
    candidate:
      image: "agent-registry/agent:${CANDIDATE_TAG}"
      version: "${CANDIDATE_VERSION}"
  
  scenarios:
    generator: "diverse"
    count: 50
    seed: 42
    dimensions: "all"
    inject_flaws: ["hardcoded_secret", "sql_injection", "missing_error_handling"]
  
  evaluation:
    judge_model: "gpt-4o"
    judge_temperature: 0
    dimensions: ["completeness", "correctness", "tool_usage", "efficiency", "safety"]
    statistical_method: "sprt"
    spr_config:
      p0: 0.90
      p1: 0.80
      alpha: 0.05
      beta: 0.20
  
  output:
    format: "json"
    path: "eval_results/${TIMESTAMP}/"
    dashboard_push: true
  
  limits:
    max_runtime_seconds: 3600
    max_cost_usd: 75.00
    max_concurrent_containers: 4
```

## Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|-------------|-------------|-----|
| Running agent on host directly | Environment leakage (different Node versions, OS packages) causes inconsistent results | Always run in containers with pinned dependency versions |
| Using real production data | Data leakage, GDPR/compliance violations, non-deterministic results | Mock project environments with generated data |
| No gotcha injection | Agent gets 100% on clean code but fails catastrophically on real-world code with flaws | Inject 3-5 intentional flaws per scenario; score detection rate |
| Single scenario dimension | Agent overfits to one project type and fails on others | Latin hypercube sampling across all 10 dimensions |
