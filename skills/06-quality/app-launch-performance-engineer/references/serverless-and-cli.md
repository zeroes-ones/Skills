# Serverless and CLI Cold Start

<!-- STANDARD: 3min -- module-graph cold start in interpreted runtimes -->

## The governing insight

In an interpreted runtime, **start-up is the import graph.** The handler is rarely the cost; the
modules it pulls in are.

```
Serverless invocation:
  allocate instance → start runtime → import every module the entry imports
                   → (this is the cold start) → run the handler

CLI invocation:
  start interpreter → import the framework → import its dependencies
                   → (this is the latency) → run the command
```

Both are the same phenomenon with different names, and in both the fix is the same: **import less, and
later.**

## Measuring the import graph

### Python

The interpreter ships the measurement. From the Python documentation: `-X importtime` "shows how long
each import takes. It shows module name, cumulative time (including nested imports) and self time
(excluding nested imports)", with a documented caveat that its output "may be broken in multi-threaded
application".

```bash
# Per-module import cost, sorted by cumulative time
python -X importtime -c 'import myapp' 2>&1 | sort -t'|' -k2 -rn | head -30
```

The distinction that matters: **cumulative** time tells you which top-level import is expensive;
**self** time tells you which module is actually doing the work. Target the high-self-time modules
first — they are the real cost, not the ones that merely aggregate.

### Node.js

```bash
# Where does start-up time go?
node --cpu-prof --cpu-prof-dir=/tmp/prof app.js
# Or instrument module load times directly:
node -e 'const M=require("module");const o=M._load;M._load=function(r,p,i){const t=Date.now();const x=o.apply(this,arguments);console.log(Date.now()-t,r);return x}'
```

The Node equivalent of the same insight: the require/import graph at module scope is the cold-start
cost, and a bundler that tree-shakes the entry often removes most of it.

### Other runtimes

| Runtime | Instrument |
|---|---|
| Ruby | `ruby -rprofile`, or `--yjit-stats` for compilation |
| Java/JVM | `-Xlog:class+load`, class-data sharing statistics |
| .NET | ReadyToRun/startup tracing |
| Go | compile-time (AOT) — start-up is small; the analogue is binary size and init order |

## The fix order

```
1. Remove module-scope work
     Anything that executes at import (reading config, connecting, registering)
     is on the critical path for every invocation.
2. Defer imports
     Move `import X` inside the function that needs it. The module is not loaded
     unless that path runs.
3. Bundle and tree-shake the entry
     A bundler that analyses the entry can drop unreachable modules entirely,
     which is a larger win than deferring them.
4. Split a monolith entry
     A handler that imports the whole framework for one endpoint pays the whole graph.
     Per-endpoint entries pay only what they need.
5. Reduce the dependency graph
     Fewer dependencies is the durable fix; deferral is the local one.
6. Provision warmth where the platform supports it
     Only after 1-5. Warm capacity hides the cost; it does not remove it,
     and it bills (see finops-engineer).
```

Steps 1–3 are mechanical and usually large. Step 6 is the one teams reach for first, and it is the one
that converts an engineering problem into a recurring bill.

## The CLI case, which is worse

A serverless function is cold *sometimes*. **A CLI is cold every single invocation.**

```text
CLI latency = interpreter start + import graph + command work

For a small command, the import graph dominates by an order of magnitude:
  interpreter start    ~30 ms
  framework import     ~400 ms    ← the problem
  actual command       ~20 ms
```

The classic cause: a package `__init__.py` (or equivalent) that imports the whole framework so that
convenience imports work, executed even for a one-line command.

**The fix:** make the package's top-level import lazy. Keep the convenience API, load it on first
attribute access. This is a well-known pattern precisely because the cost is so visible.

```python
# ❌ In the package's __init__.py — every CLI invocation pays for everything
from .core import App, Config, Router, Plugin, ...

# ✅ Same file: the framework loads only when actually used
__all__ = ["App", "Config", "Router", "Plugin"]

def __getattr__(name):
    if name in __all__:
        from . import core
        return getattr(core, name)
    raise AttributeError(name)
```

## Reporting

```text
Cold-start attribution — <function or command> — <date>

Method: N cold invocations (new instance / new process), <runtime version>, median

| Phase                     | Median  |
|---------------------------|---------|
| runtime start             |   34 ms |
| import graph (module scope)|  418 ms |
| handler / command work     |   22 ms |
| --------------------------|---------|
| total                      |  474 ms |

Top import contributions (cumulative / self):
  framework          412 ms cumulative /  18 ms self   ← aggregates, not the culprit
  framework.config   388 ms cumulative / 210 ms self   ← THE cost (does I/O at import)
  framework.plugins  160 ms cumulative /  95 ms self
```

The `self` column is the actionable one. The high-cumulative/low-self module is a pass-through; the
high-self module is where the time is spent, and `framework.config` doing I/O at import is the
finding.

## The traps

| Trap | Why it hurts |
|---|---|
| Optimising the handler | it is rarely the cost; the import graph is |
| Reading cumulative time as the ranking | cumulative includes children; self time is the work |
| Deferring imports that a bundler could remove | tree-shaking is a bigger, permanent win |
| Reaching for provisioned warmth first | it bills, and it hides the cost rather than removing it |
| Ignoring module-scope side effects | a config read or a connection at import is on every path |
| Measuring one invocation | a single run is noise; measure N and take the median |
| Measuring warm only | a warm invocation measures nothing about cold start |

## Checklist

- [ ] Cold start is measured cold (new instance / new process), N runs, median reported
- [ ] The import graph is measured with the runtime's own tooling, not estimated
- [ ] Self time is used for ranking, with cumulative used only to find the top-level entry points
- [ ] Module-scope side effects (config, connections, registrations) are inventoried
- [ ] Module-scope work is removed or deferred
- [ ] The entry is bundled and tree-shaken where the runtime allows
- [ ] A monolithic entry is split per endpoint/command where the graph is large
- [ ] Warmth is considered only after the code-level fixes, with its cost accounted
- [ ] The attribution is recorded with the method, so the comparison can hold it constant (R5)
