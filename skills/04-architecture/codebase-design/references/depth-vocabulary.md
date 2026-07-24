# Depth Vocabulary

## Core Definitions

**Module:** A unit of code with a public interface and private implementation. Could be a class, file, package, or namespace — the pattern is orthogonal to language.

**Depth:** The ratio of behavior provided to interface cost. Depth = behavior_lines / public_methods. A module with 300 lines of behavior and 3 public methods has depth 100. A module with 15 lines of behavior and 12 public methods has depth 1.25.

**Interface Cost:** The cognitive load imposed on callers. Measured as the number of public methods, parameters, and concepts a caller must understand. Higher interface cost means more to learn, more to go wrong, more to maintain.

**Behavior Value:** The useful work the module performs — data transformation, business logic, I/O orchestration, computation. Does NOT include delegation (passing to another module), getter/setter boilerplate, or logging — those are infrastructure, not behavior.

## Depth Classifications

| Classification | Depth Range | Action |
|---------------|-------------|--------|
| Deep | > 3.0 | Preserve. These modules are the codebase's assets. |
| Moderate | 1.0 - 3.0 | Acceptable. Monitor for interface growth. |
| Shallow | < 1.0 | Refactor or decompose. These are liabilities. |
| Critically Shallow | < 0.5 | Immediate action required. Delete if possible. |

## Key Insight

Deep modules are rare and precious. Most codebases have 80% shallow modules and 20% deep ones. The goal is to invert that ratio by consolidating shallow modules into fewer, deeper ones.

## Related Concepts

**Seam:** A place where behavior changes independently — the natural boundary between modules that evolve at different rates.

**Leverage:** How many callers benefit from a module's behavior. High depth × high leverage = high-value module.

**Locality:** Whether related code lives close together. High locality means co-changing files are in the same directory.
