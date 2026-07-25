# Best Practices — Civic Tech Developer

<!-- STANDARD: 3min -- rules extracted from production experience -->

- **Design before code**: Validate the approach with stakeholder input before writing a single line. A 30-minute design review prevents 3 weeks of rework.
- **Fail fast, fail loud**: Validate inputs at every boundary. Invalid data should never reach business logic. Return clear, actionable error messages.
- **Test the happy path AND the sad path**: Every feature needs tests for success, failure, edge cases, and error states.
- **Keep it simple**: The best solution is the simplest one that meets requirements. Complexity is a liability, not an asset.
- **Monitor what matters**: Instrument key user journeys, not just server metrics. Track business KPIs alongside technical metrics.
- **Document decisions, not just code**: Write ADRs for significant choices so future teammates understand "why."
- **Security is everyone's job**: Never trust user input, never hardcode secrets, never skip auth checks, never expose stack traces.
