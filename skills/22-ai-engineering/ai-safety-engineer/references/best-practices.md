# Best Practices

<!-- DEEP: 10+min -->

- **Guardrails are the first line of defense, not the only one.** The best safety architecture has: good model behavior (safety training), good prompt design (clear boundaries), good guardrails (input and output filtering), good content (grounded RAG), and good human oversight (sampling and escalation). If any layer is missing, the others must be stronger.
- **Prompt injection will succeed eventually.** When it does, the guardrail must catch the output. Design for the scenario where the model complies with an injection attack — the guardrail should prevent the harmful output from reaching the user. This is defense in depth.
- **In health apps, the most dangerous failure is the one that sounds right.** An AI that says "take 50mg of prednisone daily for your bleed" sounds authoritative and may be followed. This is more dangerous than obvious nonsense. Test for confident-sounding wrong answers specifically (quote your own content incorrectly, invent clinical guidelines, make up research findings).
- **Red-teaming is a team sport, not a solo exercise.** A single person will miss attack vectors. Have at least 3 people conduct independent red-teaming. Use diverse perspectives (clinician, security engineer, product manager, patient advocate). Each finds different bypass methods.
- **Model providers change their safety behavior without notice.** OpenAI's GPT-4o may refuse a request today and comply tomorrow after a model update. Re-run your safety test set after every model update. Never assume model safety behavior is stable.
- **Bias in health AI is a patient safety issue, not just a fairness issue.** An AI that gives worse advice to non-English speakers, dismisses symptoms more for women, or recommends less aggressive treatment based on demographics can directly harm patients. Test for demographic parity in response quality. Include representative test cases for your patient population.
