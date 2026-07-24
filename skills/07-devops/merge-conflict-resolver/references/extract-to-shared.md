# Extract to Shared Module

Decision framework and workflow for the extract-to-shared resolution strategy with abstraction design guidelines.

## When to Extract

Both sides introduce the same concept with incompatible implementations AND:
1. The concept is genuinely shared (not coincidental similarity)
2. Extracting reduces future conflict surface
3. A clean abstraction can be defined without forcing it

## Workflow

1. Create the shared module/function with a clean interface
2. Update OURS to use the shared implementation
3. Update THEIRS to use the shared implementation
4. Verify both sides' tests pass with the shared code
5. Document the abstraction in the resolution log

## Abstraction Design Guidelines

- Single responsibility: the shared module does one thing well
- Clean interface: minimal surface area, clear contracts
- Backward compatible: existing callers work without modification
- Tested independently: shared module has its own tests

## Anti-Patterns

- Premature abstraction: extracting before the pattern is clear
- God module: one shared module for everything
- Leaky abstraction: exposing implementation details of either side
