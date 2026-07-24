# Seam Identification

## What Is a Seam?

A **seam** is a place in the code where behavior can change independently on either side. It's the natural boundary where one module's concerns end and another's begin. Good seams enable independent testing, independent deployment, and independent evolution.

## Finding Natural Seams

### 1. Extension Points
Where does the code have natural "plug-in" points? Strategy pattern implementations, dependency injection sites, and callback registrations are pre-existing seams.

### 2. Test Boundaries
What do you mock or stub in tests? Every mock boundary is a seam — the production code and the mocked code change independently.

### 3. Config Boundaries
Where does configuration cross into behavior? The line between "what the system is configured to do" and "what the system does" is a seam.

### 4. Rate-of-Change Boundaries
Which parts of the code change at different frequencies? Stable infrastructure vs. volatile business rules — separate them with a seam.

### 5. Team Ownership Boundaries
Which teams own which code? Conway's Law says seams should align with team boundaries. A module owned by two teams is an artificial seam waiting to be split.

## Seam Scoring Checklist

For candidate boundary A|B, score 1 point for each YES:

1. A and B change at different rates
2. A can be tested independently from B
3. A has different performance characteristics than B
4. A has different error-handling needs
5. A serves different caller personas
6. B can be replaced without changing A

**Score:** 6/6 = natural seam | 4-5/6 = candidate | <4/6 = artificial boundary
