# Multi-Agent Debugging

## Common Failure Modes
1. **Silent corruption:** Agent output passes schema but is semantically wrong
2. **State starvation:** Agent lacks context to make correct decision
3. **Infinite delegation loop:** A→B→C→A (circular)
4. **Premature convergence:** Agents agree on wrong answer (groupthink)
5. **Context poisoning:** Bad output from agent N corrupts agents N+1, N+2...

## Debugging Techniques

### Trace Each Agent's Input/Output
Log every agent's input state and output state. Replay with modifications.

### Inject Intentional Failures
Kill agents mid-execution, corrupt state, send invalid inputs. Does topology recover?

### Differential Testing
Run same topology with different models. Do outputs converge or diverge?

### State Diff Analysis
Compare state before and after each agent. What changed? Was it correct?

### Agent-Level Unit Tests
Test each agent in isolation with known inputs → expected outputs before composing.
