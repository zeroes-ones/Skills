## Best Practices

1. **Research before you write.** 60% of skill-building time should be domain research. The best skills cite real incidents, real CVEs, and real post-mortems. A skill written from memory alone is a confident summary of one person's experience — a skill written from research encodes the collective wisdom of the industry.

2. **Every ground rule must be testable.** If you can't write a behavioral eval for it, it's not a ground rule. "Be careful with authentication" fails — what does the agent DO differently? "Never store JWT in localStorage — use httpOnly cookies with SameSite=Strict" passes — the agent can mechanically verify client-side storage mechanisms.

3. **Gotchas need dollar figures from real incidents.** Search for breach costs (IBM annual report), downtime calculations (hourly revenue × outage hours), and migration horror stories (developer time × hourly rate). A gotcha without a dollar amount is a platitude. The dollar figure is what convinces the agent to prioritize prevention.

4. **Decision trees must have "when NOT to use" branches.** The most valuable part of a decision tree is knowing when to say NO. "Use microservices" is easy. "Use microservices when team > 20 AND independent deploy cycles needed. Do NOT use when team < 8 OR tight coupling exists between services" is expert.

5. **Chain connections are not optional.** Orphaned skills are undiscoverable. Every skill connects to at least 2 upstream and 2 downstream skills. The chain router depends on these edges — an unconnected skill exists in isolation. Search the repository before declaring chain connections empty.

6. **Anti-rationalization is psychological defense.** Understand the cognitive bias behind each rationalization. "We're too small to be a target" = optimism bias + normalcy bias. "The framework handles security" = diffusion of responsibility + authority bias toward framework authors. The "Why It Feels Right" column must evoke uncomfortable recognition.

7. **Production checklists are the agent's "done" signal.** Without a checklist, the agent doesn't know when to stop generating output. Every checklist item must be binary (yes/no) and mechanically verifiable. Use domain-specific prefix IDs for traceability across skills.

8. **Validate after EVERY generation.** Run `validate-skills.sh` (or manual verification) before declaring a skill complete. Validation measures structure; manual review measures substance. Both are required. A skill that passes validation but fails manual review is not done.

9. **Token budget discipline.** Every line must earn its cost. If you can say it in 1 line instead of 3, do it. Move reference material to `references/` directory. Run the no-op test: does removing this sentence change default agent behavior? If no, delete. The compiler will minify further — start lean.

10. **This skill must be able to recreate itself.** The ultimate test: can dynamic-skill-creator generate a new dynamic-skill-creator that passes all quality checks? If the answer is no, fix this skill. If the answer is yes, every other skill generation is a solved problem. This is the bootstrap invariant that guarantees quality across the entire repository.

11. **Default to the repository standard when uncertain.** When in doubt about format, section ordering, table structure, or heading conventions, reference existing 10/10* skills — mobile-developer, backend-developer, code-reviewer, security-reviewer, writing-great-skills. Their formats are battle-tested across thousands of agent invocations. Novelty in format is a bug, not a feature.

12. **Admit what you cannot know.** If generating a skill for a domain where pricing, features, or APIs change rapidly (cloud services, SaaS tools, third-party APIs), flag it in the frontmatter and add a gotcha about verification. The agent should NOT trust pricing-specific advice older than 6 months without re-verification.
