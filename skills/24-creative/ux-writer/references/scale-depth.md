# Scale Depth: Solo → Small → Medium → Enterprise

<!-- DEEP: 10+min -->

### Solo (1 writer, 1 product)
- **What changes**: You write everything. Spreadsheet for string tracking. One general disclaimer. Flesch-Kincaid check in Word. No A/B testing — judgment calls.
- **What to skip**: Content design system, content tokens, automated tone scoring, multi-jurisdiction consent, continuous testing.
- **Coordination**: Weekly sync with designer. Monthly review with legal for disclaimers.

### Small Team (2-5 writers, 2-3 products)
- **What changes**: Shared content guidelines. Glossary in a wiki. Disclaimers in a shared library. Manual readability checks. Basic A/B testing on critical flows. 5-10 languages.
- **What to skip**: Full content design system (shared templates are enough), automated readability monitoring, continuous trust NPS tracking.
- **Coordination**: Bi-weekly content review. Quarterly voice/tone audit. Monthly sync with translation team.

### Medium Team (5-15 writers, multi-product)
- **What changes**: Content design system with tokens. TMS integration for strings. Automated readability checks in CI. A/B testing program. Designated clinical content reviewer. 20-30 languages. Per-feature disclaimers.
- **What to skip**: AI-assisted tone scoring (manual review at this scale), fully automated consent personalization.
- **Coordination**: Weekly content design system review. Bi-weekly cross-product consistency audit. Quarterly accessibility audit.

### Enterprise (15+ writers, global products)
- **What changes**: Full content design system with API-driven strings. Automated tone and readability scoring in CI/CD. Multi-jurisdiction consent engine. Continuous experimentation across all copy. Dedicated health literacy specialist. 30+ languages with locale-specific disclaimers. WCAG AAA content accessibility.
- **What's full production**: Content ops function. Brand voice AI training. Real-time translation quality monitoring. Trust NPS as a KPI. Regulatory change monitoring for disclaimer updates.
- **Coordination**: Daily content system standup. Weekly experimentation review. Monthly regulatory alignment. Quarterly board-level trust report.

### Transition Triggers
- **Solo → Small**: >200 strings, second product launch, first international market
- **Small → Medium**: >1000 strings, >10 languages, first FDA-regulated product, consent complexity exceeds manual management
- **Medium → Enterprise**: >5000 strings, multi-jurisdiction regulatory requirements, patient safety-critical content
