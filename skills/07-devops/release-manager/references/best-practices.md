# Best Practices

<!-- STANDARD: 3min -- rules extracted from production experience -->
<!-- DEEP: 10+min -->
- **Release trains create predictability**: teams know exactly when their code ships. This reduces "is my change in prod?" anxiety and makes planning possible.
- **Code freeze means CODE FREEZE**: only bug fixes and security patches after the freeze deadline. Feature work goes to the next train. No exceptions without release commander + CTO approval.
- **Go/No-Go is not a democracy**: the release commander makes the final call. A clear decision-maker prevents deadlocks. Rotate the role to share risk awareness.
- **Rollback is a feature, not a failure**: if rollback takes > 10 minutes, it's broken. Practice rollbacks monthly. A smooth rollback is better than a heroic hotfix.
- **Feature flags have a lifecycle**: every flag must have an owner and removal date. Flags older than 60 days become technical debt. Use flag removal as a release checklist item.
- **Release notes are for humans, not computers**: auto-generated changelogs are a start. Add a 1-paragraph summary, known issues, and upgrade instructions written by a person.
- **Every release needs a rollback plan**: if you can't describe how to undo a change in < 3 sentences, it shouldn't be in the release.
- **Database migrations are the #1 cause of rollback failures**: always have a downgrade migration tested. If a migration is irreversible, it goes in a separate, carefully planned release.
- **Post-release monitoring is mandatory**: the first 24 hours after deploy is when most regressions surface. Keep the deployer on-call for at least 24 hours post-release.
- **Release retrospectives compound**: each retro should produce < 5 action items. Track them across releases. If the same issue appears in 3 consecutive retros, escalate to engineering leadership.
