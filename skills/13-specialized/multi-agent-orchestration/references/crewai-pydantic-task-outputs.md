# CrewAI Pydantic Task Outputs

Reference for multi-agent-orchestration SKILL.md — CrewAI 0.30+ structured output patterns.

## Pydantic Output Models

CrewAI enforces structured output via Pydantic BaseModel on Task definitions:

```python
from pydantic import BaseModel, Field
from crewai import Task, Agent

class CodeReviewOutput(BaseModel):
    file_reviewed: str = Field(description="Path to reviewed file")
    issues_found: int = Field(description="Count of issues")
    severity: str = Field(description="low | medium | high | critical")
    recommendations: list[str] = Field(description="Actionable fixes")
    approved: bool = Field(description="Pass/fail gate")

review_task = Task(
    description="Review src/auth.py for security issues",
    expected_output="CodeReviewOutput model instance",
    output_pydantic=CodeReviewOutput,
    agent=security_agent
)
```

## Multi-Agent Output Chaining

```
┌──────────┐  CodeReviewOutput  ┌──────────┐
│ Reviewer │───────────────────▶│ Fixer    │
│ Agent    │                    │ Agent    │
└──────────┘                    └──────────┘
                                      │
                              FixOutput │
                                      ▼
                               ┌──────────┐
                               │ Verifier │
                               │ Agent    │
                               └──────────┘
```

**Output contract rules:**
1. Each agent defines its output Pydantic model — never pass raw dict between agents.
2. Downstream agent validates upstream model before processing.
3. If validation fails, reject and request re-generation with validation errors.

## Hierarchical Crew Pattern

```python
from crewai import Crew, Process

manager = Agent(role="Engineering Manager", allow_delegation=True)
coder = Agent(role="Senior Developer", allow_delegation=False)
reviewer = Agent(role="Code Reviewer", allow_delegation=False)

crew = Crew(
    agents=[manager, coder, reviewer],
    tasks=[design_task, code_task, review_task],
    process=Process.hierarchical  # Manager delegates
)
result = crew.kickoff()
```

## Structured State Passing

Between crews, use Pydantic as the serialization boundary:

```python
class InterCrewState(BaseModel):
    architecture_decision: ArchitectureDecision
    implementation_plan: list[str]
    risk_register: list[dict]
    state_hash: str  # SHA-256 for integrity

# Crew A output → validated → Crew B input
state = InterCrewState(**crew_a_output.model_dump())
crew_b.kickoff(inputs=state.model_dump())
```

## Gotcha: Schema Drift

If Agent A changes output schema without updating Agent B's input validation → silent field
misses. **Fix:** Shared Pydantic models in a `schemas/` package; CI check for schema
compatibility between adjacent agents.
