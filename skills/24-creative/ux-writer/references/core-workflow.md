# Core Workflow — Full Implementation

<!-- QUICK: 30s -- scan phase titles to understand the process -->

### Phase 1 (~20 min): Product Copy Design

Design the words that guide users through the product experience.

1. **Onboarding flows**: Progressive disclosure. Each screen = one concept. "Let's set up your treatment plan" not "Configure clinical parameters." Use benefit language: "This helps us show you relevant information" not "This populates the database."
2. **Empty states**: Never show a blank screen. "You haven't logged any symptoms yet. Tap + to start tracking." Include illustration + CTA. For clinical dashboards: "No lab results available. They'll appear here once your provider shares them."
3. **Loading states**: Explain the wait. "Retrieving your health records…" beats a spinner. For long clinical loads: "Gathering your complete health history — this may take up to 30 seconds. Thanks for your patience."
4. **Success confirmations**: Confirm what happened + what's next. "Your symptoms were logged. View your trend report →" Not just a checkmark.
5. **Modals and dialogs**: Title = action. Body = consequence. Buttons = verb + object. "Delete Symptom Log — This removes all entries from March. This can't be undone. [Cancel] [Delete Entries]"

### Phase 2 (~25 min): Medical Disclaimers

Craft disclaimers that protect legally without degrading the user experience.

1. **When to show**: Before clinical decision support results, before treatment cost estimates, on any page containing medical advice, before data sharing with third parties, on AI-generated health content.
2. **How to phrase**: Lead with the limitation, not the liability shield. "This tool provides information, not medical advice. Always consult your doctor before making health decisions." Not: "Company X assumes no liability for…"
3. **Placement patterns**:
   - **Inline**: Short disclaimer adjacent to specific content. "This is an estimate based on your plan. Actual costs may vary."
   - **Modal**: Critical safety warnings requiring acknowledgment. "This medication may interact with [drug]. Please review with your doctor."
   - **Footer**: Persistent general disclaimer. "This app does not replace professional medical advice."
4. **Regulatory requirements**: FDA 21 CFR Part 11 for electronic records, HIPAA for PHI, GDPR Art. 9 for health data in EU, FTC Health Breach Notification Rule, state-specific telehealth consent laws.
5. **Progressive disclosure**: Show essential disclaimer inline, link to full legal text. Never dump 5,000 words of legalese into a 300px modal.

### Phase 3 (~25 min): Consent Language Design

Design consent flows that are truly informed — not just legally compliant.

1. **Informed consent UX**:
   - **Pre-consent summary**: 3 bullet points max. What data, why, who sees it. "Your symptom logs help us personalize your care plan. Only your care team can see them."
   - **Granular options**: Separate toggles for treatment, research, marketing, third-party sharing. Default all to OFF.
   - **Comprehension check**: Ask one question to confirm understanding. "In your own words, who can see your health data?" with multiple-choice options.
   - **Withdrawal pathways**: "You can change these settings anytime in Settings > Privacy. Withdrawing consent won't affect your care."
2. **Reading levels by audience**:
   - Patient-facing: ≤6th grade. "We'll use your health info to give you better care. You can say no anytime."
   - Caregiver-facing: ≤8th grade. "Your child's treatment data helps us track progress and adjust the care plan."
   - Provider-facing: Professional level with clear summaries.
3. **Consent for minors**: Age of consent varies by jurisdiction (13-18). Parental consent flows with child assent language for ages 7-17.
4. **Research consent**: Distinguish between treatment consent and research consent explicitly. "Participating in this study is separate from your treatment. Declining won't affect your care."

### Phase 4 (~20 min): Health Literacy Messaging

Make health information understandable to everyone, regardless of education level.

1. **Plain language principles**:
   - ≤8th grade reading level (target ≤6th for patient-facing)
   - Active voice: "Take this medicine with food" not "This medication should be administered with meals"
   - Short sentences: ≤15 words per sentence
   - Common words: "high blood pressure" not "hypertension"; "blood thinner" not "anticoagulant"
   - Define unavoidable clinical terms inline: "Hemophilia (a condition where blood doesn't clot normally)"
2. **Visual reinforcement**: Every written instruction pairs with an illustration. Pill identification = photo. Injection site = anatomical diagram. Treatment schedule = calendar visualization.
3. **Translations and localization**: Design English source strings for translatability. Avoid idioms ("feeling under the weather"), cultural references, and English-only wordplay. Allow 30% text expansion for Romance languages, 40% for German.
4. **Readability testing tools**: Flesch-Kincaid Grade Level, SMOG Index, PEMAT (Patient Education Materials Assessment Tool). Test with actual patients from your target demographic.

### Phase 5 (~20 min): Error Message Design for Health Contexts

Error messages in health apps carry higher stakes. Design for trust preservation.

1. **Session timeout**: "Your session timed out to protect your privacy. Your last entry was saved. Log in again to continue." Never: "Session expired."
2. **Clinical data save failure**: "We couldn't save your last entry. Don't close this screen — your data is still visible here. Try saving again or take a screenshot." Provide recovery path.
3. **Connectivity loss during data entry**: "Connection lost. Your entries since [timestamp] are saved on your device and will sync when you're back online."
4. **Medication interaction warning**: "This medication may interact with [drug name] in your profile. Please contact your doctor before taking it." Red banner, not subtle toast.
5. **Lab result unavailable**: "Your lab results aren't ready yet. We'll notify you when they are — typically within 24-48 hours." Set expectations.
6. **Generic error replacement rule**: Never show "Error 500" or stack traces. Every error = what happened + what it means for the user + what to do next.

### Phase 6 (~25 min): Voice and Tone Systems

Define how your health product sounds in different contexts.

1. **Voice dimensions (stable)**:
   - **Clear**: Jargon-free, concrete, scannable
   - **Compassionate**: Acknowledges emotion, never dismissive
   - **Trustworthy**: Evidence-based, accurate, transparent about limitations
   - **Empowering**: Gives users agency, never paternalistic
2. **Tone shifts (context-dependent)**:
   - **Sensitive health topics** (cancer, mental health, sexual health): Compassionate + gentle. "We understand this is difficult. Take your time. You're not alone."
   - **Clinical information** (lab results, treatment plans): Professional + clear. "Your A1C is 7.2%, down from 8.1%. This shows your treatment plan is working."
   - **Treatment adherence** (medication reminders, PT exercises): Encouraging + specific. "You've taken your medication 5 days in a row. That's a new record! 🎉"
   - **Urgent safety** (drug interactions, critical results): Direct + actionable. "Important: Contact your doctor before taking this medication. [View interaction details]"
   - **Errors and setbacks**: Supportive + solution-focused. "It looks like you missed your last 2 doses. That's okay — here's what to do now."
3. **Tone anti-patterns**: Never cheerful for serious conditions ("Congrats on your diabetes!"), never clinical-jargon with patients, never blame the user ("You entered an invalid value"), never minimize ("Just a little lump").

### Phase 7 (~20 min): Content Design Systems

Build reusable, scalable content infrastructure.

1. **Reusable content patterns**: Error message template, empty state template, confirmation message template, disclaimer snippet library, consent language components, notification templates (push, email, in-app).
2. **Content tokens**: Define variables for product name, company name, support contact, app store links. Use `{{product_name}}` not hardcoded strings.
3. **Localization-ready string design**:
   - Never concatenate strings: `"You have " + count + " messages"` breaks in every language
   - Use ICU MessageFormat: `{count, plural, one {# message} other {# messages}}`
   - Provide translator context comments: `/* Button: initiates medication refill. Max 20 chars. */`
4. **Character limits per component**:
   - Push notification title: 40 chars
   - Push notification body: 120 chars
   - Button label: 25 chars (20 for mobile)
   - Modal title: 50 chars
   - Toast/ snackbar: 80 chars
   - Tooltip: 150 chars
   - Error message body: 200 chars
5. **Content audit**: Quarterly review of all strings. Flag outdated medical claims, broken links, non-inclusive language, reading level regressions.

### Phase 8 (~15 min): Microcopy Testing

Test whether your words actually work.

1. **A/B testing error messages**: Test trust impact. "Something went wrong" vs "We hit a snag — your data is safe." Measure: task completion rate, support tickets generated, trust survey score.
2. **Comprehension testing**: 5-second test — show the consent screen for 5 seconds, then ask: "What did you just agree to?" If >80% can't answer correctly, rewrite.
3. **Trust impact of phrasings**: "We share your data with partners" vs "Your data helps us improve care for everyone." Test trust before and after with Likert scale.
4. **Click-through on CTAs**: "Learn more" vs "See how this works" vs "Understand your results." Measure actual clicks.
5. **Readability validation**: Run every patient-facing string through Flesch-Kincaid. Flag anything above 8th grade. Test with users who have limited health literacy.

### Phase 9 (~15 min): Accessibility in Content

Ensure content is accessible to all users.

1. **Screen reader content**: Every non-decorative image needs alt text. Medical diagrams need descriptive alt text: "Diagram showing the ankle joint with labels for tibia, fibula, and talus bones. Arrow indicates common sprain site." Provide text alternatives for infographics and charts.
2. **Alt text for medical diagrams**: "Illustration of the heart showing four chambers. Left ventricle highlighted in red to indicate the site of the myocardial infarction described below."
3. **Plain language alternatives**: For every clinical term, provide a tooltip or parenthetical with plain language: "Myocardial infarction (heart attack)." Ensure screen readers can access these alternatives.
4. **Link text**: Never "click here" or "read more." Use descriptive links: "View your full lab results" or "Learn about treatment options."
5. **Reading order**: Content must make sense when linearized. Headings must follow hierarchy (H1 → H2 → H3, no skips).
6. **Cognitive accessibility**: Allow users to hide complex medical explanations behind "Show plain-language version" toggles. Provide summaries before detailed clinical reports.
