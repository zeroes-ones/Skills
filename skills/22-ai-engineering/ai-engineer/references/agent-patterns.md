# Agent Architecture Patterns

## Pattern 1: ReAct (Reasoning + Acting)

```
Thought → Action → Observation → Thought → Action → ... → Final Answer
```

**When to use:** Tasks requiring tool use with reasoning between steps (research, data gathering, multi-step analysis).

```python
def react_agent(task, tools, max_steps=10):
    messages = [{"role": "system", "content": REACT_SYSTEM_PROMPT}]
    messages.append({"role": "user", "content": task})
    
    for step in range(max_steps):
        response = llm.chat(messages, tools=tools)
        
        if response.has_final_answer():
            return response.final_answer
        
        # Execute tool
        tool_result = execute_tool(response.tool_call)
        messages.append({"role": "assistant", "content": response.thought})
        messages.append({"role": "tool", "content": tool_result})
    
    raise AgentTimeout("Max steps reached without final answer")
```

## Pattern 2: Plan-Execute

```
Task → Planner generates steps → Executor runs step 1 → Validate → 
Executor runs step 2 → Validate → ... → Final Synthesis
```

**When to use:** Predictable, sequential tasks with clear dependencies.

## Pattern 3: Router Agent

```
Query → Classifier identifies intent → Route to specialized handler → Response
```

**When to use:** Multi-domain system (customer support: billing/tech/account).

## Pattern 4: Multi-Agent Orchestration

```
Orchestrator → Agent A (research) + Agent B (analysis) → Orchestrator synthesizes → Output
```

**When to use:** Complex tasks requiring diverse expertise.

## Agent Safety Checklist

- [ ] Max steps: 10 (prevents infinite loops)
- [ ] Timeout: 120s (prevents hanging)
- [ ] Deadlock detector: abort if 3 consecutive steps produce same output
- [ ] Tool allowlist: agent can only call registered tools
- [ ] Rate limiting: max 5 tool calls per second
- [ ] Cost tracking: log tokens + cost per agent run
- [ ] Human escalation: if confidence < 0.7, ask human
