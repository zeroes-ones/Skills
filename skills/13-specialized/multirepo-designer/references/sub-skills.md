# Sub-Skills: Related Skills & Dependency Map

The Multirepo Designer skill depends on and integrates with several other skills in the framework. Below is the dependency map and coordination guide.

## Direct Dependencies (Required Knowledge)

| Skill | Relationship | When to Invoke |
|-------|-------------|----------------|
| **system-architect** | Prerequisite | Architecture decisions, C4 diagrams, ADRs before repo design |
| **codebase-design** | Prerequisite | Module boundaries, package structure within each repo |
| **monorepo-manager** | Sibling | Compare monorepo vs polyrepo trade-offs for each decision |
| **ci-cd-builder** | Prerequisite | Cross-repo CI pipelines, reusable workflows |
| **api-designer** | Prerequisite | Contract design (OpenAPI, Protobuf) that crosses repo boundaries |
| **database-designer** | Prerequisite | Data ownership boundaries when splitting repos |

## Coordinating Skills (Invoke Together)

| Skill | Coordination Pattern | Example |
|-------|---------------------|---------|
| **polyrepo-strategy** | Invoke first for strategy, then multirepo-designer for implementation | Strategic decision → detailed repo topology |
| **repo-scaffolding** | multirepo-designer designs → scaffolding implements | Design 5-repo layout → scaffold each repo |
| **dependency-governance** | multirepo-designer defines boundaries → governance enforces them | Define allowed deps → configure OPA rules |
| **cross-repo-refactoring** | multirepo-designer identifies target state → refactoring executes migration | New repo boundary → extract code |
| **build-system-design** | multirepo-designer chooses granularity → build system implements | Repo topology → Nx/Bazel configuration |
| **deprecation-engineer** | multirepo-designer plans lifecycle → deprecation manages end-of-life | Archive repo → deprecate APIs, migrate consumers |
| **migration-architect** | multirepo-designer designs target → migration executes transition | Monolith → 8 services → migration roadmap |

## Skill Invocation Order (Typical Workflow)

```
1. system-architect     → Define system boundaries, quality attributes
2. database-designer    → Define data ownership per bounded context
3. api-designer         → Define API contracts between boundaries
4. multirepo-designer   → Map bounded contexts to repos, define governance
5. monorepo-manager     → Validate: would monorepo be better for any clusters?
6. ci-cd-builder        → Design cross-repo CI/CD pipelines
7. repo-scaffolding     → Generate repo templates with tooling
8. build-system-design  → Configure Nx/Bazel for the repo topology
```

## Skill Level Context

The Multirepo Designer is a **Level 2+ skill** (Specialized). It assumes:
- You already understand basic software architecture (Level 0-1)
- You have experience with at least one build system (Maven, Gradle, npm, Bazel)
- You've worked in a team with 3+ repositories

If you're new to multirepo design, start with:
1. `codebase-design` — for module boundary fundamentals
2. `monorepo-manager` — to understand the monorepo alternative
3. Then return to multirepo-designer

## Output Handoff Format

When handing off from multirepo-designer to other skills, provide:
```yaml
repo_topology:
  repos:
    - name: auth
      owner: identity-team
      language: go
      dependencies: [contracts, toolkit]
      database: auth-db (PostgreSQL, owned by auth)
    - name: billing
      owner: commerce-team
      language: go
      dependencies: [contracts, toolkit]
      database: billing-db (PostgreSQL, owned by billing)
  contracts_repo: contracts
  shared_infra: [toolkit, ci-templates, terraform-modules]
  governance: team-owned (CODEOWNERS per repo)
  versioning: independent semver, ^ ranges for shared libs
```
