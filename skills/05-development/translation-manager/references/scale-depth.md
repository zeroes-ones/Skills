# Scale Depth: Solo → Small → Medium → Enterprise

<!-- STANDARD: 3min -->

### Solo
Single developer handles translations via crowd-sourced or basic PO files. Focus: getting strings translated at all. Skip: translation memory, QA pipelines, context notes. Coordination: with developers on string freeze timing.

### Small Team
Dedicated translation manager, localization platform (Crowdin/Phrase), 1-3 target languages. Focus: consistent terminology, basic i18n. Coordination: with engineering on ICU message format, with content team on source string quality.

### Medium Team
Translation team (PM + linguists + reviewers), 5-10 languages, CI-embedded l10n pipeline. Focus: translation memory, automated QA, context-rich strings. Coordination: with product on string feature gating, with marketing on market-specific messaging.

### Enterprise
Full l10n program, 20+ languages, machine translation with human review, custom glossaries per locale. Focus: regional compliance, scalable content operations. Coordination: with legal on localized ToS/Privacy, with support on translated knowledge base.

### Transition Triggers
| From → To | Trigger |
|-----------|---------|
| Solo → Small | Second language beyond English; manual string management breaking |
| Small → Medium | Operating in 5+ languages; translation errors causing customer complaints |
| Medium → Enterprise | Regulatory need for certified translations; operating in 20+ locales |
