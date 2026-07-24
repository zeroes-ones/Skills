# Test Harness Architecture

## Components

```
┌─────────────────────────────────────┐
│         Test Runner                  │
│  ┌─────────┐  ┌──────────────────┐  │
│  │Agent    │  │  Eval Harness    │  │
│  │Container│──│  - Input injector │  │
│  │         │  │  - Output capture  │  │
│  │         │  │  - Grader engine   │  │
│  └─────────┘  │  - Stats analyzer  │  │
│               └──────────────────┘  │
│  ┌────────────────────────────────┐ │
│  │     Results Database            │ │
│  │  - Run metadata                 │ │
│  │  - Agent inputs/outputs         │ │
│  │  - Grades & confidence          │ │
│  │  - Statistical summaries        │ │
│  └────────────────────────────────┘ │
└─────────────────────────────────────┘
```

## Mocking External Dependencies
- File system: tmpfs with seeded test files
- Network: mock HTTP server with recorded responses
- Tools: instrumented wrappers that log all calls
- Other agents: mock agents with scripted responses

## Parallelization
- Each test case is independent → embarrassingly parallel
- Run N containers simultaneously (N = CPU cores - 1)
- Aggregate results after all runs complete
