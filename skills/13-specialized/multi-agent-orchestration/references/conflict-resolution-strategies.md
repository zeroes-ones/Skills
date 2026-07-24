# Conflict Resolution Strategies

## Strategy 1: Majority Vote
3+ agents produce outputs → majority wins.
- Requires: odd number of agents, independent reasoning
- Risk: correlated errors across agents using same model

## Strategy 2: Arbiter Agent
Conflicting agents A, B → third agent C evaluates both → C chooses.
- Requires: arbiter must be equally or more capable
- Risk: arbiter bias toward one style

## Strategy 3: Human Escalation
Conflict on critical path → present both options with trade-offs → human decides.
- For: security vulnerabilities, architectural decisions, budget allocation

## Strategy 4: Confidence-Weighted Merge
Each agent outputs with confidence score → weight by confidence.
- Requires: agents must self-assess confidence
- Risk: overconfident wrong answers dominate

## Strategy 5: Constraint-Based Filtering
Apply hard constraints to filter outputs → remaining options are valid.
- Example: "Must be OWASP compliant" → filter non-compliant suggestions
