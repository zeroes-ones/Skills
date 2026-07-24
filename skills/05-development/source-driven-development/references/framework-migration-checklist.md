# Framework Migration Checklist

## Source-Driven Migration Protocol

Every major version migration must be traceable to official migration guides and changelogs.

## Phase 1: Pre-Migration Audit

- [ ] Extract current version: `npm list <pkg> --depth=0`, `pip show <pkg>`, `go list -m <module>`
- [ ] Fetch official migration guide for target version
- [ ] Read ALL intermediate release notes between current and target version
- [ ] Identify every breaking change listed in the migration guide
- [ ] Run `grep -rn` for every deprecated API in your codebase
- [ ] Create a migration impact matrix: `{deprecated_call} → {replacement} → {file_paths}`

## Phase 2: Compatibility Assessment

- [ ] Check if any transitive dependencies have not yet upgraded to target version
- [ ] Verify TypeScript types compatibility (`npm ls @types/* --depth=0`)
- [ ] Check CI/test version matrix compatibility
- [ ] Test migration guide code examples in isolation before applying to codebase

## Phase 3: Incremental Upgrade

```
1. Create migration branch: git checkout -b migrate/{pkg}-v{X}-to-v{Y}
2. Update version pin in dependency file (exact, no ^ or ~)
3. Run install: npm install / pip install / go get
4. Apply one breaking change at a time (one commit per deprecated API replacement)
5. Run tests after each commit
6. Update all citations to target version
```

## Phase 4: Citation Updates

- [ ] Update every `[Source: ..., Version: v{old}]` to `[Source: ..., Version: v{new}]`
- [ ] Verify new doc URLs (doc sites may restructure between majors)
- [ ] Add migration guide citation to PR description:
  ```
  Migration: {framework} v{old} → v{new}
  Guide: {URL to official migration guide}
  Breaking changes addressed: {count}
  ```

## Phase 5: Post-Migration Verification

- [ ] Full test suite passes at new version
- [ ] No deprecation warnings in console/logs
- [ ] CI pipeline runs against new version
- [ ] Staging deployment smoke tests pass
- [ ] Performance benchmarks unchanged (±5%)
- [ ] Update `CONTRIBUTING.md` / team onboarding docs with new version

## Common Migration Patterns

### React 18 → 19
- [ ] Replace `forwardRef` with direct `ref` prop
- [ ] Remove `React.lazy` workarounds (native in 19)
- [ ] Check `useOptimistic` signature (changed from 18 experimental)
- [ ] [Source: React v19 Upgrade Guide, URL: https://react.dev/blog/2024/04/25/react-19-upgrade-guide]

### Next.js 13 → 14 → 15
- [ ] Pages Router → App Router migration (if applicable)
- [ ] `generateStaticParams` async signature
- [ ] Caching semantics changed (14.2 → 15)
- [ ] [Source: Next.js Upgrade Guide, URL: https://nextjs.org/docs/app/building-your-application/upgrading]

### Prisma 4 → 5
- [ ] `findUnique` no longer accepts `rejectOnNotFound`
- [ ] `$transaction` API changed for interactive transactions
- [ ] [Source: Prisma v5 Upgrade Guide, URL: https://www.prisma.io/docs/orm/more/upgrade-guides/upgrading-versions/upgrading-to-prisma-5]

### FastAPI 0.100 → 0.115
- [ ] Pydantic v2 migration (if still on v1)
- [ ] `jsonable_encoder` behavior changes
- [ ] [Source: FastAPI Release Notes, URL: https://fastapi.tiangolo.com/release-notes/]
