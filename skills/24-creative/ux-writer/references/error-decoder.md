# Error Decoder

<!-- DEEP: 5min -- each entry includes a diagnostic grep pattern and step-by-step recovery loop for automation -->

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Error message "Authentication failed" on password reset flow -- users think account is hacked; actual issue: expired reset token | Generic auth error reused from login page for password reset. Error describes system state, not user situation. Users interpret "authentication failed" as intrusion. | **Detect:** Auth-related error strings without expired/session-related alternatives

**Fix:** Write error messages as [what happened] + [user impact] + [concrete next action]. For password reset: "This reset link expired after 30 minutes. Your password has not been changed. Request a new link below."

**Auto-recovery:** 1. Audit error messages for user-perspective check. 2. Map errors to user scenarios. 3. Rewrite using template. 4. Test comprehension with users. 5. Quarterly audit to catch regressions. | An error message that describes system state instead of user situation creates confusion and support tickets. The detection pattern catches system-oriented errors and the auto-recovery loop rewrites from the user perspective. |
| Consent comprehension <50% -- users do not know what they agreed to | Single checkbox or "Continue" button with pre-checked consent. "Continue" is a navigation verb, not a consent verb. No comprehension check. | **Detect:** Single consent button AND missing granular/checkbox language

**Fix:** Split consent into granular options -- one per purpose. Use "I agree to share [specific data] with [named recipient] for [explicit purpose]." Add comprehension check. Require explicit opt-in per category.

**Auto-recovery:** 1. Audit consent flow for granularity. 2. If single checkbox, split by purpose. 3. Add comprehension questions. 4. Verify legal compliance. 5. Test with users: >=90% must correctly explain consent. | "Continue" is not a consent verb. The detection pattern catches single-button consent flows and the auto-recovery loop enforces granular, verified consent per GDPR Art. 7. |
| High support tickets for "how do I..." -- users cannot understand the interface | UI copy written at 10th-12th grade reading level for a population averaging 6th-8th grade. Flesch-Kincaid check was never run. | **Detect:** Readability check returns > grade 8 for patient-facing strings

**Fix:** Simplify to <=6th grade for patient-facing content. Replace clinical terms with plain language. Short sentences (<=15 words). Active voice. Add tooltips for necessary clinical terms.

**Auto-recovery:** 1. Check all strings for grade level. 2. Simplify copy to target grade 6. 3. Add inline definitions for clinical terms. 4. Re-test readability. 5. Monitor for regressions. | Readability is a safety issue in clinical contexts. The detection pattern catches high-grade-level copy and the auto-recovery loop enforces plain language with inline definitions. |
| Translation quality complaints -- "the Spanish version does not make sense" | Concatenated strings, English idioms, hardcoded plurals, no translator context comments. String fragments cannot be translated independently. | **Detect:** Concatenated strings, sprintf, or template literals without ICU MessageFormat

**Fix:** Rewrite all strings in ICU MessageFormat. Replace idioms with literal language. Add translator comments for context.

**Auto-recovery:** 1. Audit for concatenation, idioms, plurals. 2. Migrate concatenated strings to ICU. 3. Replace idioms with literal language. 4. Inject translator context. 5. Test with pseudo-localization. | String concatenation breaks translation in every language. The detection pattern catches concatenation patterns and the auto-recovery loop migrates to ICU MessageFormat with translator comments. |
| Accessibility audit fails -- missing alt text, heading skips (H1 to H3), non-descriptive link text ("click here") | Content accessibility treated as a dev task, not a writing task. Alt text, heading hierarchy, and link text are content design decisions. | **Detect:** alt="" or aria-hidden in medical/clinical content specs

**Fix:** Add descriptive alt text for all images. Fix heading hierarchy: no skipped levels. Rewrite link text to be descriptive out of context.

**Auto-recovery:** 1. Run a11y audit for content violations. 2. Generate alt text for medical images. 3. Fix heading hierarchy. 4. Rewrite link text. 5. Re-audit to zero content violations. | Accessibility is a content design decision, not a development task. The detection pattern catches content-level a11y violations and the auto-recovery loop fixes alt text, headings, and link text. |
| Trust survey score drops 15 points in one quarter -- users rate the app as "insensitive" | Tone mismatch: cheerful gamification language used in a serious clinical context. Users with chronic conditions feel unheard. | **Detect:** Exclamation-heavy language AND clinical/oncology string presence in same file

**Fix:** Audit all strings for tone-context alignment. Replace celebratory language with compassionate acknowledgment. Use a condition-appropriate register.

**Auto-recovery:** 1. Audit tone-context alignment. 2. Map appropriate register per condition. 3. Rewrite flagged strings with compassionate tone. 4. Review with patient advisory board. 5. Re-survey trust NPS at 30 and 90 days. | Cheerful language in a clinical context signals that the product does not understand the user experience. The detection pattern catches tone mismatches and the auto-recovery loop enforces condition-appropriate register. |
