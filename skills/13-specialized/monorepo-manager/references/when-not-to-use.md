# When NOT to Use This Skill (Overkill)

- **Single repository with <3 packages**: A monorepo is the answer to multi-package coordination. With 1 repo, 1 package, there's nothing to coordinate. Use a normal repo structure.
- **Solo developer**: Monorepo tooling exists to coordinate teams. You are one person. You don't need Turborepo, Nx, workspace protocols, or dependency boundary enforcement.
- **Packages that evolve independently with different release cycles**: If package A releases weekly and package B releases quarterly, they don't benefit from atomic commits. Polyrepo with semver is better.
- **Mixed-language projects with no shared dependency graph**: If you have a Python service and a Go service that share nothing, monorepo gives you only the downsides (large clones, slow CI) without the benefits (shared code, atomic changes).
- **You're already successfully using a polyrepo**: Don't migrate for the sake of "modern best practice." If your polyrepo CI is fast, dependencies are versioned, and devs aren't frustrated, stay put.
