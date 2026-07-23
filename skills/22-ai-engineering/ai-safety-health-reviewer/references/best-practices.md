# Best Practices

<!-- DEEP: 10+min -->

1. **Red-team for medical scenarios systematically**: Design adversarial prompts that simulate drug-seeking behavior, symptom exaggeration (doctor-shopping), contraindication probing, pediatric dosing requests, and off-label use inquiries. Red-team before every major release and after any fine-tuning. Track red-team pass rates as a release gate.

2. **Tier disclaimers by content risk level — never use boilerplate**: Educational content ("Talk to your doctor") vs. symptom information ("This is not a diagnosis — see a healthcare provider if symptoms persist") vs. treatment-adjacent content ("Do not change medications based on this information — consult your prescribing physician immediately"). Disclaimers must reflect actual regulatory status (investigational vs. cleared device).

3. **Calibrate confidence thresholds per medical domain**: A 90% confidence score for dermatology image classification means something very different than 90% for mental health triage. Set domain-specific confidence thresholds informed by clinical risk. Below-threshold outputs route to human review or are suppressed. Never surface raw confidence to patients.

4. **Design for differential diagnosis risk explicitly**: Health AI outputs — even educational ones — can anchor patients on a specific diagnosis, delaying appropriate care. Structure outputs to present multiple possibilities, emphasize uncertainty, and direct to in-person evaluation rather than implying a definitive answer.

5. **Implement pediatric and adolescent guardrails as a separate layer**: Children and adolescents have distinct safety profiles — age-appropriate language, parental consent considerations, mandatory escalation for eating disorders/self-harm, and different crisis resources (e.g., Trevor Project for LGBTQ+ youth). These guardrails must be applied before adult-oriented safety checks.

6. **Deploy emergency keyword detection with zero false-negative tolerance**: Keywords indicating suicidal ideation, self-harm, violence, or acute medical emergencies (chest pain, stroke symptoms, anaphylaxis) must trigger immediate crisis protocol regardless of context. The cost of a false positive (showing crisis resources unnecessarily) is orders of magnitude lower than a false negative.

7. **Detect medical hallucinations with retrieval verification, not just confidence scores**: LLMs can confidently fabricate drug names, clinical trial results, and guideline citations. Implement NLI-based hallucination detection that cross-references every factual medical claim against a trusted knowledge base (DrugBank, UpToDate, PubMed). Flag claims that cannot be verified — don't just flag low-confidence outputs.

8. **Version-lock clinical knowledge bases and audit update cadence**: Medical knowledge evolves rapidly — guidelines change, drugs are recalled, trials are retracted. The KB version used for verification must be tracked alongside every safety decision. Set maximum staleness SLAs (e.g., KB frozen for >90 days triggers automatic review). Document which KB version was active for every safety incident.
