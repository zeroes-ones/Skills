# Split & Merge Migration Playbooks

Playbooks for migrating between monorepo and polyrepo architectures. Both directions are high-risk, multi-month efforts that require careful planning.

## Monorepo -> Polyrepo (Split)

### Preconditions
- Monorepo build time >15min despite all caching optimizations.
- Teams have diverging release cadences.
- Security boundaries require separate access controls.

### Migration Steps

1. **Identify extraction candidates by team boundary**, not by code type. Extract "checkout-service" not "utils-repo."
2. **Establish shared CI templates FIRST.** Without them, you get N inconsistent pipelines.
3. **Extract one repo at a time**, starting with the lowest-coupling service.
4. **Preserve git history** using `git filter-repo --subdirectory-filter`.
5. **Convert monorepo imports to package dependencies** in internal registry.
6. **Dual-CI during migration:** monorepo CI + new repo CI run for 2 sprints.
7. **Archive old code in monorepo** after migration verified.

**Timeline:** 2-4 weeks per repo. Full migration for 10-repo split: 3-6 months.

## Polyrepo -> Monorepo (Merge)

### Preconditions
- >30% of PRs touch multiple repos.
- "Waiting for another team's release" is a recurring complaint.
- Monorepo tooling (Nx, Turborepo, Bazel) is proven in a pilot.

### Migration Steps

1. **Merge only highly-coupled repos.** Do not merge everything.
2. **Set up monorepo tooling FIRST** in a pilot repo.
3. **Merge repos one at a time**, preserving git history (`git merge --allow-unrelated-histories`).
4. **Unify tooling:** one linter config, one TS config, one CI pipeline.
5. **Redirect old repos:** archive with README pointing to monorepo path.

**Timeline:** 1-2 weeks per repo. Full migration for 5-repo merge: 2-3 months.

## Common Failure Modes
- Splitting without CI governance -> N inconsistent pipelines.
- Merging without monorepo tooling -> unmanageably slow builds.
- "Big bang" migration instead of incremental -> extended downtime and rollback difficulty.
