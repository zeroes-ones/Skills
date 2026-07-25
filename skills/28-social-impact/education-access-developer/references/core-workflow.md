# Core Workflow — Education Access Developer Full Implementation

<!-- QUICK: 30s -- scan phase titles to understand the process -->

### Phase 1 (~20 min): Discovery & Scoping
1. **Understand the problem**: What is the user trying to accomplish? What's the current pain point?
2. **Define success criteria**: Be specific -- "user can complete checkout in under 30 seconds with 99.9% success rate."
3. **Identify constraints**: Budget, timeline, existing systems, compliance, team capabilities.
4. **Scope the work**: What's in scope? What's explicitly out? Write this down to prevent scope creep.

### Phase 2 (~30 min): Design & Architecture
1. **Choose the approach**: Walk through each decision tree. Document why each path was chosen.
2. **Design the data model**: Entities, relationships, constraints. Use database-designer skill if needed.
3. **Design the API/interface**: Contracts before implementation. Inputs, outputs, error states.
4. **Design for failure**: What happens when the DB is down? When the API times out? When the user is offline?
5. **Security review**: Threat model the design. Where are the trust boundaries?

### Phase 3 (~60 min): Implementation
1. **Set up project structure**: Follow conventions. Configure linting, formatting, type checking.
2. **Build the data layer**: Models, migrations, seed data. Test with real data.
3. **Build business logic**: Core algorithms, validation, state machines. This is where the value lives.
4. **Build the interface/API**: Controllers, middleware, error handling. Consistent error formats.
5. **Wire it together**: Connect layers. Test integration. Fix mismatches between design and build.

### Phase 4 (~30 min): Testing & Quality
1. **Unit tests**: Test business logic in isolation. Happy path, error states, edge cases.
2. **Integration tests**: Test the wiring. Does the API talk to the database correctly?
3. **End-to-end tests**: Test the full user journey. This is what users actually experience.
4. **Performance test**: Does it handle expected load? Where are the bottlenecks?
5. **Accessibility test**: Can everyone use it? Keyboard nav, screen reader, color contrast.

### Phase 5 (~20 min): Deployment & Monitoring
1. **Deploy to staging**: Verify in an environment that mirrors production.
2. **Run the checklist**: Go through every item in checklist.md. Don't skip.
3. **Deploy to production**: Follow the runbook. Have rollback plan ready.
4. **Monitor**: Watch dashboards for the first hour. Error rates, latency, business metrics.
5. **Post-deploy review**: What went well? What could be better? Update runbook.

### Phase 6 (~15 min): Documentation & Handoff
1. **Update documentation**: What changed? Why? How does it work now?
2. **Write post-mortem if needed**: Blameless. Focus on process improvements.
3. **Handoff to team**: Brief the team on what shipped and any known issues.
